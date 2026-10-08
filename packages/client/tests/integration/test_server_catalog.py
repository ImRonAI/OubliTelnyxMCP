from fastmcp import Client
from fastmcp.client.transports import ClientTransport

from oubliai_client import MODEL_VISIBLE_TOOLS, get_schema, list_model_visible_tools, search


async def test_authenticated_server_catalog_uses_client_wrappers(
    http_client: Client[ClientTransport],
) -> None:
    tools = await list_model_visible_tools(http_client)
    search_result = await search(http_client, "list available phone numbers")
    schema_result = await get_schema(http_client, ["ListAvailablePhoneNumbers"])

    assert tuple(tool.name for tool in tools) == MODEL_VISIBLE_TOOLS
    assert "ListAvailablePhoneNumbers" in search_result.content[0].text
    assert "ListAvailablePhoneNumbers" in schema_result.content[0].text
