from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.client.auth import BearerAuth, OAuth
from fastmcp.client.transports import StreamableHttpTransport

from oubliai_client import bearer, connect, file_token_storage, oauth


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


def test_connect_rejects_non_http_url() -> None:
    with pytest.raises(ValueError, match="Invalid HTTP/S URL"):
        connect("stdio://not-http")


def test_auth_helpers_return_native_fastmcp_providers(tmp_path: Path) -> None:
    storage = file_token_storage(tmp_path / "tokens")

    assert isinstance(bearer("secret"), BearerAuth)
    assert isinstance(oauth(scopes=["openid"], token_storage=storage), OAuth)


async def test_file_token_storage_persists_values(tmp_path: Path) -> None:
    directory = tmp_path / "tokens"
    storage = file_token_storage(directory)

    await storage.put("https://example.test/tokens", {"access_token": "redacted"})

    assert await storage.get("https://example.test/tokens") == {
        "access_token": "redacted"
    }
    assert directory.is_dir()
