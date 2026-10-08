import httpx2
import pytest
from fastmcp.exceptions import ToolError
from fastmcp.utilities.tests import asgi_client
from mcp.shared.exceptions import MCPError


async def test_wrong_token_rejects_connection(real_server) -> None:
    with pytest.raises(MCPError, match="Server returned an error response"):
        async with asgi_client(real_server(), auth="wrong-token"):
            pass


async def test_telnyx_denied_operation_is_reported(real_server) -> None:
    def deny(_: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(403, json={"errors": [{"detail": "forbidden"}]})

    async with asgi_client(real_server(deny), auth="user-token") as client:
        with pytest.raises(ToolError, match="HTTP error 403: Forbidden"):
            await client.call_tool("GetUserBalance", {})


async def test_malformed_tool_input_is_rejected(http_client) -> None:
    with pytest.raises(ToolError, match="validation error"):
        await http_client.call_tool("search", {"query": ["not", "a", "string"]})


async def test_unknown_tool_is_rejected(http_client) -> None:
    with pytest.raises(ToolError, match="Unknown tool"):
        await http_client.call_tool("tool_that_does_not_exist", {})
