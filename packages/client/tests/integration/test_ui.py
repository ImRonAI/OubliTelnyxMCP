import pytest
from fastmcp import Client
from fastmcp.client.transports import ClientTransport
from mcp.types import TextResourceContents

from oubliai_client.ui import (
    RENDERER_MIME,
    RENDERER_URI,
    _renderer_resource_from_contents,
    find_renderer_resource,
    generate_ui,
    read_renderer_resource,
)


async def test_find_and_read_renderer_resource(
    http_client: Client[ClientTransport],
) -> None:
    listed = await find_renderer_resource(http_client)
    renderer = await read_renderer_resource(http_client)

    assert str(listed.uri) == RENDERER_URI
    assert listed.mime_type == RENDERER_MIME
    assert renderer.uri == RENDERER_URI
    assert renderer.mime_type == RENDERER_MIME
    assert renderer.html
    assert renderer.csp is not None
    assert "https://cdn.jsdelivr.net" in {
        *renderer.csp.get("connectDomains", []),
        *renderer.csp.get("resourceDomains", []),
    }
    assert renderer.meta is not None
    assert renderer.permissions == renderer.meta["ui"].get("permissions")


def test_renderer_resource_refuses_wrong_mime() -> None:
    contents = TextResourceContents(
        uri=RENDERER_URI,
        mime_type="text/plain",
        text="not an MCP App",
    )

    with pytest.raises(ValueError, match="renderer MIME"):
        _renderer_resource_from_contents([contents])


@pytest.mark.deno
async def test_generate_ui_uses_documented_code_input(
    http_client: Client[ClientTransport],
) -> None:
    tool = next(
        item for item in await http_client.list_tools() if item.name == "generate_prefab_ui"
    )
    assert "code" in tool.input_schema["properties"]
    assert "code" in tool.input_schema["required"]

    result = await generate_ui(
        http_client,
        "from prefab_ui.app import PrefabApp\n"
        "from prefab_ui.components import Column, Heading, Text\n"
        "with PrefabApp() as app:\n"
        "    with Column():\n"
        "        Heading('Generated UI')\n"
        "        Text('Rendered by the installed provider.')",
    )

    assert not result.is_error, result.content
    assert result.structured_content is not None
    assert "$prefab" in result.structured_content
