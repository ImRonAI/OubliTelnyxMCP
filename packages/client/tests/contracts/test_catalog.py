from fastmcp import Client, FastMCP
from fastmcp.client.client import CallToolResult

from oubliai_client import (
    MODEL_VISIBLE_TOOLS,
    execute,
    get_schema,
    list_model_visible_tools,
    search,
)


def _catalog_server() -> FastMCP:
    server = FastMCP("catalog-contract")

    @server.tool(name="search")
    async def search_tool(query: str) -> dict[str, str]:
        return {"query": query}

    @server.tool(name="get_schema")
    async def get_schema_tool(tools: list[str]) -> dict[str, list[str]]:
        return {"tools": tools}

    @server.tool(name="execute")
    async def execute_tool(code: str) -> dict[str, str]:
        return {"code": code}

    @server.tool(name="generate_prefab_ui")
    async def generate_prefab_ui_tool() -> dict[str, bool]:
        return {"ok": True}

    @server.tool(name="host_only")
    async def host_only_tool() -> dict[str, bool]:
        return {"hidden": True}

    return server


async def test_model_visible_listing_is_bounded_to_four_native_tools() -> None:
    async with Client(_catalog_server()) as client:
        tools = await list_model_visible_tools(client)

    assert tuple(tool.name for tool in tools) == MODEL_VISIBLE_TOOLS


async def test_catalog_wrappers_preserve_native_results() -> None:
    async with Client(_catalog_server()) as client:
        search_result = await search(client, "phone numbers")
        schema_result = await get_schema(client, ["ListAvailablePhoneNumbers"])
        execute_result = await execute(client, "return 42")

    assert isinstance(search_result, CallToolResult)
    assert search_result.structured_content == {"query": "phone numbers"}
    assert isinstance(schema_result, CallToolResult)
    assert schema_result.structured_content == {
        "tools": ["ListAvailablePhoneNumbers"]
    }
    assert isinstance(execute_result, CallToolResult)
    assert execute_result.structured_content == {"code": "return 42"}
