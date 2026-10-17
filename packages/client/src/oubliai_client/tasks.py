import asyncio
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
) -> ToolTask:
    return await call_tool_task(
        connection, "await_telnyx_resource", {"kind": kind, "resource_id": resource_id}
    )


async def wait_for(
    task: ToolTask,
    *,
    timeout: float = 72 * 3600.0,
) -> CallToolResult:
    """Drive the task to its result; answers `input_required` through the client's
    handlers (clients/tasks.md: `task.result()`), bounded by `timeout`."""
    return await asyncio.wait_for(task.result(), timeout)


__all__ = [
    "ToolTask",
    "await_telnyx_resource_task",
    "call_tool_task",
    "wait_for",
]
