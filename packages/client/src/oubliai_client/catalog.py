from fastmcp.client.client import CallToolResult
from mcp.types import Tool

from oubliai_client.connection import OubliaiConnection

MODEL_VISIBLE_TOOLS = (
    "execute",
    "generate_prefab_ui",
    "get_schema",
    "search",
)


async def list_model_visible_tools(connection: OubliaiConnection) -> list[Tool]:
    tools_by_name = {tool.name: tool for tool in await connection.list_tools()}
    return [
        tools_by_name[name]
        for name in MODEL_VISIBLE_TOOLS
        if name in tools_by_name
    ]


async def search(connection: OubliaiConnection, query: str) -> CallToolResult:
    return await connection.call_tool("search", {"query": query})


async def get_schema(
    connection: OubliaiConnection, tools: list[str]
) -> CallToolResult:
    return await connection.call_tool("get_schema", {"tools": tools})


async def execute(connection: OubliaiConnection, code: str) -> CallToolResult:
    return await connection.call_tool("execute", {"code": code})
