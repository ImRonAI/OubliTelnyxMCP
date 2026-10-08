from typing import Literal

from fastmcp.client.client import CallToolResult
from fastmcp_tasks import ToolTask, call_tool_task

from oubliai_client.connection import OubliaiConnection

ResourceKind = Literal["number_order", "kv_namespace"]


async def await_telnyx_resource_task(
    connection: OubliaiConnection,
    *,
    kind: ResourceKind,
    resource_id: str,
    poll_interval_seconds: float | None = None,
    max_polls: int | None = None,
) -> ToolTask:
    arguments: dict[str, str | float | int] = {
        "kind": kind,
        "resource_id": resource_id,
    }
    if poll_interval_seconds is not None:
        arguments["poll_interval_seconds"] = poll_interval_seconds
    if max_polls is not None:
        arguments["max_polls"] = max_polls
    return await call_tool_task(connection, "await_telnyx_resource", arguments)


async def wait_for(
    task: ToolTask,
    *,
    timeout: float = 300.0,
) -> CallToolResult:
    await task.wait(timeout=timeout)
    return await task.result()


__all__ = [
    "ToolTask",
    "await_telnyx_resource_task",
    "call_tool_task",
    "wait_for",
]
