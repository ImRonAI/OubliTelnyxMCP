from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.tests import asgi_client
from fastmcp_tasks import TasksExtension

from oubliai_client import MODEL_VISIBLE_TOOLS, get_schema, list_model_visible_tools, search
from oubliai_server import build_server


async def test_authenticated_server_catalog_uses_client_wrappers() -> None:
    server = build_server(
        auth=StaticTokenVerifier(
            tokens={"user-token": {"client_id": "client", "scopes": []}}
        ),
        tasks=TasksExtension(url="memory://"),
    )

    async with asgi_client(server, auth="user-token") as client:
        tools = await list_model_visible_tools(client)
        search_result = await search(client, "list available phone numbers")
        schema_result = await get_schema(client, ["ListAvailablePhoneNumbers"])

    assert tuple(tool.name for tool in tools) == MODEL_VISIBLE_TOOLS
    assert "ListAvailablePhoneNumbers" in search_result.content[0].text
    assert "ListAvailablePhoneNumbers" in schema_result.content[0].text
