"""Background tasks through FastMCP's native `TasksExtension` (Docket).

The extension is registered on the root server (`docs/reference/fastmcp/pages/tasks.md`,
"Enabling Background Tasks"); mounted-child extensions do not propagate. Task-enabled
tools must be native async functions, so OpenAPI-generated tools cannot carry `task=`.
The one task here polls an asynchronous Telnyx resource through the generated tools,
so the caller's token (captured in the task snapshot) still reaches Telnyx.
"""

import asyncio
import json
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Literal

from docket import Timeout
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Progress
from mcp.types import TextContent
from fastmcp.exceptions import ToolError
from fastmcp.tools import ToolResult
from fastmcp.utilities.tasks import TaskConfig
from fastmcp_tasks import TasksExtension
from fastmcp_tasks.settings import TasksSettings

ResourceKind = Literal["number_order", "kv_namespace"]


@dataclass(frozen=True)
class _Pollable:
    """A generated tool whose `data.status` reaches a terminal value (schema enums)."""

    tool: str
    id_param: str
    terminal: frozenset[str]


# Terminal states are the schema's own enums:
#   NumberOrderWithPhoneNumbers.status: pending | success | failure
#   KvNamespace.status: pending | provision_ok | provision_failed | deleting | delete_failed
#   (`deleting` is transitional: "Once deletion completes, the namespace no longer appears
#   in the API", so a completed delete surfaces as a 404 from GetKvNamespace, not a status.)
POLLABLE: dict[ResourceKind, _Pollable] = {
    "number_order": _Pollable("RetrieveNumberOrder", "number_order_id", frozenset({"success", "failure"})),
    "kv_namespace": _Pollable(
        "GetKvNamespace",
        "id",
        frozenset({"provision_ok", "provision_failed", "delete_failed"}),
    ),
}

SNAPSHOT_KEY_ENV = "FASTMCP_TASKS_ENCRYPTION_KEY"

# Foreground calls (direct, or `call_tool` inside CodeMode `execute`) are bounded by the
# tool `timeout` (tools.md, "Timeouts"); background runs by Docket's `Timeout` dependency
# (tools.md, "Timeouts vs Background Tasks"). The foreground bound stays under hosted
# request limits; a long wait belongs in a background task the client polls.
FOREGROUND_TIMEOUT = timedelta(seconds=120)
BACKGROUND_TIMEOUT = timedelta(hours=72)
POLL_INTERVAL = timedelta(seconds=5)


def build_tasks_extension() -> TasksExtension:
    """`TasksExtension()`, configured by its own `FASTMCP_DOCKET_*` settings (tasks.md,
    "Configuration"; default `memory://`).

    Task snapshots carry the caller's access token and headers (tasks.md, "Credentials at
    Rest"): with `memory://` they never leave the process; any other backend stores them as
    plaintext unless `FASTMCP_TASKS_ENCRYPTION_KEY` is set, so that key is required there.
    """
    extension = TasksExtension()
    url = extension.docket_settings.url
    key = TasksSettings().encryption_key
    if url != "memory://" and not (key and key.get_secret_value()):
        raise SystemExit(
            f"FASTMCP_DOCKET_URL={url!r} persists task snapshots (caller tokens) outside the "
            f"process; set {SNAPSHOT_KEY_ENV} so they are encrypted at rest."
        )
    return extension


def _payload(result: ToolResult) -> dict[str, Any]:
    if result.structured_content is not None:
        return result.structured_content
    for block in result.content:
        if isinstance(block, TextContent):
            loaded = json.loads(block.text)
            return loaded if isinstance(loaded, dict) else {"result": loaded}
    return {}


def _status(payload: dict[str, Any]) -> str:
    data = payload.get("data")
    if isinstance(data, dict) and isinstance(data.get("status"), str):
        return data["status"]
    raise ToolError(f"Response carries no data.status: {sorted(payload)}")


def register_task_tools(operations: FastMCP) -> None:
    """Register `await_telnyx_resource` on the operations child (hidden behind CodeMode)."""

    @operations.tool(
        task=TaskConfig(mode="optional", poll_interval=POLL_INTERVAL),
        timeout=FOREGROUND_TIMEOUT.total_seconds(),
        tags={"oubliai"},
    )
    async def await_telnyx_resource(
        kind: ResourceKind,
        resource_id: str,
        ctx: Context,
        progress: Progress = Progress(),
        timeout: Timeout = Timeout(BACKGROUND_TIMEOUT),
    ) -> dict[str, Any]:
        """Wait until a Telnyx resource's `data.status` is terminal.

        `number_order` -> RetrieveNumberOrder (terminal: success, failure).
        `kv_namespace` -> GetKvNamespace (terminal: provision_ok, provision_failed,
        delete_failed; `deleting` keeps waiting). Called directly by a task-capable client
        it runs as a background task (up to 72 hours); called inside `execute` it runs in
        the foreground and stops after 2 minutes.
        """
        target = POLLABLE[kind]
        polls = 0
        while True:
            polls += 1
            result = await ctx.fastmcp.call_tool(target.tool, {target.id_param: resource_id})
            status = _status(_payload(result))
            await progress.set_message(status)
            await progress.increment()
            if status in target.terminal:
                return {"kind": kind, "resource_id": resource_id, "status": status, "polls": polls}
            await asyncio.sleep(POLL_INTERVAL.total_seconds())
