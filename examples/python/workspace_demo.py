"""Workspace and task demo on top of oubliai_client.

Loads the MCP URL from the repository root mcp.json, then drives search,
workspaces, the renderer resource, and a long-running number-order task.
No live Telnyx calls are made in tests; running main() performs a real
Telnyx OAuth login (user gate).
"""

import asyncio
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from oubliai_client import (
    OubliaiConnection,
    ProgressRecorder,
    await_telnyx_resource_task,
    connect,
    file_token_storage,
    get_schema,
    list_model_visible_tools,
    oauth,
    open_workspace,
    read_renderer_resource,
    search,
    server_summary,
    wait_for,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MCP_CONFIG = REPO_ROOT / "mcp.json"
TOKEN_DIR = Path.home() / ".oubliai" / "tokens"


def _mcp_url(config_path: Path = MCP_CONFIG) -> str:
    config = json.loads(config_path.read_text())
    url = config["mcpServers"]["oubliai-telnyx"]["url"]
    if not isinstance(url, str) or not url:
        raise ValueError("mcp.json: mcpServers.oubliai-telnyx.url missing")
    return url


async def summarize(connection: OubliaiConnection) -> None:
    info = server_summary(connection)
    print(f"server: {info['name']} {info['version']} (protocol {info['protocol_version']})")
    tools = await list_model_visible_tools(connection)
    print(f"tools ({len(tools)}):")
    for tool in tools:
        print(f"- {tool.name}")


async def show_catalog(connection: OubliaiConnection) -> None:
    found = await search(connection, "list available phone numbers")
    print("search:", found.structured_content)
    schema = await get_schema(connection, ["ListAvailablePhoneNumbers"])
    print("schema:", schema.structured_content)


async def open_numbers(connection: OubliaiConnection) -> None:
    workspace = await open_workspace(connection, "numbers")
    print(f"workspace numbers: prefab {workspace.prefab_version}")
    print("tools:", ", ".join(workspace.tool_names))


async def renderer_info(connection: OubliaiConnection) -> None:
    renderer = await read_renderer_resource(connection)
    print(f"renderer: {renderer.uri} ({renderer.mime_type})")
    if renderer.csp is not None:
        print("csp:", dict(renderer.csp))


async def track_number_order(
    connection: OubliaiConnection,
    order_id: str,
    *,
    poll_seconds: float = 1.0,
    recorder: ProgressRecorder | None = None,
) -> None:
    task = await await_telnyx_resource_task(
        connection,
        kind="number_order",
        resource_id=order_id,
        poll_interval_seconds=poll_seconds,
    )
    result = await wait_for(task, timeout=30.0)
    payload: Mapping[str, Any] = result.structured_content or {}
    print(f"number order {order_id}: {payload.get('status')} (polls={payload.get('polls')})")
    if recorder is not None:
        print(f"progress events: {len(recorder.events)}")


async def main() -> None:
    url = _mcp_url()
    print(f"NOTE: this performs a real Telnyx OAuth login against {url}")
    print(f"Tokens persist under {TOKEN_DIR} (FileTreeStore).")
    async with connect(
        url,
        auth=oauth(mcp_url=url, token_storage=file_token_storage(TOKEN_DIR)),
    ) as connection:
        await summarize(connection)
        await show_catalog(connection)
        await open_numbers(connection)
        await renderer_info(connection)
        await track_number_order(connection, "demo-order-1")


if __name__ == "__main__":
    print("Demo requires a real Telnyx login; run only when authorized.")
    asyncio.run(main())
