import sys

from fastmcp import Client, FastMCP
from fastmcp.client.group import ClientGroup

from oubliai_client.group import group, group_from_mcp_config


def test_group_preserves_named_clients() -> None:
    server = FastMCP("group-construction")
    client = Client(server)

    clients = {"primary": client}
    client_group = group(clients)

    assert isinstance(client_group, ClientGroup)
    assert client_group.clients["primary"] is client


async def test_group_namespaces_and_routes_real_tool_calls() -> None:
    alpha = FastMCP("alpha")
    beta = FastMCP("beta")

    @alpha.tool
    def echo(value: str) -> str:
        return f"alpha:{value}"

    @beta.tool
    def echo(value: str) -> str:
        return f"beta:{value}"

    client_group = group({"alpha": Client(alpha), "beta": Client(beta)})
    async with client_group:
        tools = await client_group.list_tools()
        alpha_result = await client_group.call_tool("alpha_echo", {"value": "one"})
        beta_result = await client_group.call_tool("beta_echo", {"value": "two"})

    assert {tool.name for tool in tools} == {"alpha_echo", "beta_echo"}
    assert alpha_result.data == "alpha:one"
    assert beta_result.data == "beta:two"


def test_group_from_mcp_config_uses_native_factory_and_default_mode() -> None:
    client_group = group_from_mcp_config(
        {
            "mcpServers": {
                "fixture": {
                    "command": sys.executable,
                    "args": ["-c", "pass"],
                }
            }
        },
        default_mode="legacy",
    )

    assert isinstance(client_group, ClientGroup)
    assert set(client_group.clients) == {"fixture"}
    assert client_group.clients["fixture"].mode == "legacy"
