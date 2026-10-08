from pathlib import Path

import pytest
from fastmcp import Client, FastMCP
from fastmcp.client.auth import BearerAuth, OAuth
from fastmcp.client.transports import StreamableHttpTransport

from oubliai_client import bearer, connect, file_token_storage, oauth, server_summary


def test_connect_returns_existing_client_unchanged() -> None:
    client = Client("https://example.test/mcp")

    assert connect(client) is client


def test_connect_builds_native_http_transport() -> None:
    auth = bearer("user-token")

    client = connect("https://example.test/mcp", auth=auth)

    assert isinstance(client, Client)
    assert isinstance(client.transport, StreamableHttpTransport)
    assert client.transport.url == "https://example.test/mcp"
    assert client.transport.auth is auth


def test_connect_passes_documented_client_options() -> None:
    client = connect(
        "https://example.test/mcp",
        name="Oubliai test client",
        timeout=12,
        auto_initialize=False,
        init_timeout=3,
        verify=False,
        mode="legacy",
        input_required_max_rounds=4,
        cache=False,
    )

    assert client.name == "Oubliai test client"
    assert client.auto_initialize is False
    assert client.mode == "legacy"
    assert client.input_required_max_rounds == 4


def test_connect_rejects_non_http_url() -> None:
    with pytest.raises(ValueError, match="Invalid HTTP/S URL"):
        connect("stdio://not-http")


def test_auth_helpers_return_native_fastmcp_providers(tmp_path: Path) -> None:
    storage = file_token_storage(tmp_path / "tokens")

    assert isinstance(bearer("secret"), BearerAuth)
    assert isinstance(oauth(scopes=["openid"], token_storage=storage), OAuth)


def test_oauth_passes_documented_provider_options(tmp_path: Path) -> None:
    storage = file_token_storage(tmp_path / "tokens")
    provider = oauth(
        mcp_url="https://example.test/mcp",
        scopes="openid profile",
        client_name="Oubliai test client",
        token_storage=storage,
        additional_client_metadata={"software_statement": "verified"},
        callback_port=8765,
        callback_host="127.0.0.1",
        callback_timeout=10,
        client_metadata_url="https://example.test/client.json",
        client_id="client-id",
        client_secret="client-secret",
    )

    assert isinstance(provider, OAuth)


async def test_server_summary_uses_negotiated_public_metadata() -> None:
    server = FastMCP("Summary Server", instructions="Use the public tools.")

    async with Client(server) as client:
        summary = server_summary(client)

    assert summary["name"] == "Summary Server"
    assert summary["version"] is not None
    assert summary["protocol_version"] is not None
    assert summary["instructions"] == "Use the public tools."


async def test_file_token_storage_persists_values(tmp_path: Path) -> None:
    directory = tmp_path / "tokens"
    storage = file_token_storage(directory)

    await storage.put("https://example.test/tokens", {"access_token": "redacted"})

    assert await storage.get("https://example.test/tokens") == {
        "access_token": "redacted"
    }
    assert directory.is_dir()
