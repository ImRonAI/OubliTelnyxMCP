"""Background tasks through FastMCP's native `TasksExtension` (Docket).

The extension is registered on the root server (`docs/reference/fastmcp/pages/tasks.md`,
"Enabling Background Tasks"); mounted-child extensions do not propagate. Task-enabled
tools must be native async functions, so OpenAPI-generated tools cannot carry `task=`.
The one task here polls an asynchronous Telnyx resource through the generated tools,
so the caller's token (captured in the task snapshot) still reaches Telnyx.
"""

import asyncio
import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Literal

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Progress
from mcp.types import TextContent
from fastmcp.exceptions import ToolError
from fastmcp.tools import ToolResult
from fastmcp.utilities.tasks import TaskConfig
from fastmcp_tasks import TasksExtension

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

_ENV_TO_KWARG = {
    "FASTMCP_DOCKET_URL": "url",
    "FASTMCP_DOCKET_NAME": "name",
    "FASTMCP_DOCKET_WORKER_NAME": "worker_name",
    "FASTMCP_DOCKET_CONCURRENCY": "concurrency",
}


SNAPSHOT_KEY_ENV = "FASTMCP_TASKS_ENCRYPTION_KEY"


def build_tasks_extension(env: Mapping[str, str] | None = None) -> TasksExtension:
    """`TasksExtension` from the documented `FASTMCP_DOCKET_*` variables (default `memory://`).

    Task snapshots carry the caller's access token and headers (tasks.md, "Credentials at
    Rest"). With `memory://` they never leave the process; any other backend stores them
    as plaintext unless `FASTMCP_TASKS_ENCRYPTION_KEY` is set, so that key is required.
    """
    source = os.environ if env is None else env
    kwargs: dict[str, Any] = {}
    for variable, kwarg in _ENV_TO_KWARG.items():
        value = source.get(variable)
        if value:
            kwargs[kwarg] = int(value) if kwarg == "concurrency" else value
    url = kwargs.get("url", "memory://")
    if url != "memory://" and not source.get(SNAPSHOT_KEY_ENV):
        raise SystemExit(
            f"FASTMCP_DOCKET_URL={url!r} persists task snapshots (caller tokens) outside the "
            f"process; set {SNAPSHOT_KEY_ENV} so they are encrypted at rest."
        )
    return TasksExtension(**kwargs)


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
        task=TaskConfig(mode="optional", poll_interval=timedelta(seconds=2)),
        tags={"oubliai"},
    )
    async def await_telnyx_resource(
        kind: ResourceKind,
        resource_id: str,
        ctx: Context,
        poll_interval_seconds: float = 2.0,
        max_polls: int = 150,
        progress: Progress = Progress(),
    ) -> dict[str, Any]:
        """Poll a Telnyx resource until its `data.status` is terminal.

        `number_order` -> RetrieveNumberOrder (terminal: success, failure).
        `kv_namespace` -> GetKvNamespace (terminal: provision_ok, provision_failed,
        delete_failed; `deleting` keeps polling). Runs as a background task when the
        client opts in, otherwise synchronously (for example inside `execute`).
        """
        target = POLLABLE[kind]
        await progress.set_total(max_polls)
        status = "unknown"
        for polls in range(1, max_polls + 1):
            result = await ctx.fastmcp.call_tool(target.tool, {target.id_param: resource_id})
            status = _status(_payload(result))
            await progress.set_message(status)
            await progress.increment()
            if status in target.terminal:
                return {"kind": kind, "resource_id": resource_id, "status": status, "polls": polls}
            await asyncio.sleep(poll_interval_seconds)
        raise ToolError(
            f"{kind} {resource_id} did not reach a terminal state after {max_polls} polls "
            f"(last status {status!r})"
        )
