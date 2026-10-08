import pytest
from fastmcp import Client
from fastmcp.client.transports import ClientTransport

from oubliai_client.workspaces import WORKSPACE_DOMAINS, open_workspace
from oubliai_server.apps import ALL_APPS


def test_workspace_domains_match_server_apps() -> None:
    assert set(WORKSPACE_DOMAINS) == {
        app.name.removeprefix("oubliai-") for app in ALL_APPS
    }


@pytest.mark.parametrize("domain", WORKSPACE_DOMAINS)
async def test_open_workspace_preserves_prefab_result(
    http_client: Client[ClientTransport],
    domain: str,
) -> None:
    workspace = await open_workspace(http_client, domain)

    assert workspace.prefab_version == "0.3"
    assert workspace.raw is workspace.result.structured_content
    assert workspace.view is workspace.raw["view"]
    assert workspace.tool_names


async def test_open_workspace_rejects_unknown_domain(
    http_client: Client[ClientTransport],
) -> None:
    with pytest.raises(ValueError, match="unknown workspace domain"):
        await open_workspace(http_client, "unknown")
