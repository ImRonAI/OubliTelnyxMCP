import httpx2
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.tests import asgi_client, asgi_server
from key_value.aio.stores.memory import MemoryStore

from oubliai_server import build_server
from oubliai_server.auth.provider import build_auth
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.runtime.storage import ENCRYPTION_KEY_ENV, STORAGE_URL_ENV, build_client_storage
from oubliai_server.spec import oauth_scopes

PUBLIC_BASE_URL = "http://127.0.0.1"


def _refuse(request: httpx2.Request) -> httpx2.Response:
    raise AssertionError(f"unexpected network call: {request.url}")


def _oauth_server(spec, client_storage=None):
    auth = build_auth(
        spec,
        base_url=PUBLIC_BASE_URL,
        client_id="oubliai-client",
        client_secret="client-secret-value",
        jwt_signing_key="test-signing-key-material",
        allowed_client_redirect_uris=["http://localhost:*"],
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(_refuse)),
        client_storage=client_storage if client_storage is not None else MemoryStore(),
    )
    telnyx = make_telnyx_client(
        "https://api.telnyx.com/v2", transport=httpx2.MockTransport(_refuse)
    )
    return build_server(spec, client=telnyx, auth=auth)


async def _raw(server, method: str, path: str) -> httpx2.Response:
    async with asgi_server(server) as running:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=running.app), base_url=PUBLIC_BASE_URL
        ) as http:
            return await http.request(method, path)


async def test_mcp_endpoint_requires_bearer_token(telnyx_spec):
    response = await _raw(_oauth_server(telnyx_spec), "POST", "/mcp")
    assert response.status_code == 401
    assert response.headers["www-authenticate"].startswith("Bearer")


async def test_protected_resource_metadata(telnyx_spec):
    response = await _raw(
        _oauth_server(telnyx_spec), "GET", "/.well-known/oauth-protected-resource/mcp"
    )
    assert response.status_code == 200
    metadata = response.json()
    assert metadata["resource"].rstrip("/") == f"{PUBLIC_BASE_URL}/mcp"
    assert metadata["scopes_supported"] == oauth_scopes()


async def test_authorization_server_metadata_points_at_this_server(telnyx_spec):
    response = await _raw(
        _oauth_server(telnyx_spec), "GET", "/.well-known/oauth-authorization-server"
    )
    assert response.status_code == 200
    metadata = response.json()
    assert metadata["authorization_endpoint"] == f"{PUBLIC_BASE_URL}/authorize"
    assert metadata["scopes_supported"] == oauth_scopes()


async def test_caller_token_reaches_telnyx_over_http(telnyx_spec):
    """BYOK over the real HTTP stack: the verified bearer is what Telnyx receives.

    Uses FastMCP's documented test verifier so the transport/passthrough path is
    exercised without simulating Telnyx's consent page.
    """
    received: list[str | None] = []

    def telnyx(request: httpx2.Request) -> httpx2.Response:
        received.append(request.headers.get("authorization"))
        assert request.url.path == "/v2/balance"
        return httpx2.Response(200, json={"data": {"balance": "1.00", "currency": "USD"}})

    auth = StaticTokenVerifier(tokens={"user-token": {"client_id": "user", "scopes": []}})
    server = build_server(
        telnyx_spec,
        client=make_telnyx_client(
            "https://api.telnyx.com/v2", transport=httpx2.MockTransport(telnyx)
        ),
        auth=auth,
    )
    async with asgi_client(server, auth="user-token") as client:
        result = await client.call_tool(
            "execute", {"code": 'return await call_tool("GetUserBalance", {})'}
        )

    assert not result.is_error, result.content
    assert received == ["Bearer user-token"]


async def test_oauth_routes_work_with_encrypted_client_storage(telnyx_spec):
    """The deployed storage path (`build_client_storage`) backs the proxy without changes."""
    from cryptography.fernet import Fernet

    storage = build_client_storage(
        {ENCRYPTION_KEY_ENV: Fernet.generate_key().decode(), STORAGE_URL_ENV: "memory://"}
    )
    server = _oauth_server(telnyx_spec, client_storage=storage)
    denied = await _raw(server, "POST", "/mcp")
    metadata = await _raw(server, "GET", "/.well-known/oauth-protected-resource/mcp")
    assert denied.status_code == 401
    assert denied.headers["www-authenticate"].startswith("Bearer")
    assert metadata.status_code == 200
    assert metadata.json()["scopes_supported"] == oauth_scopes()


def test_mounted_operations_child_masks_error_details_like_the_parent(telnyx_spec, caplog):
    """FastMCP logs a warning at mount time when the parent masks errors but the child does not."""
    import logging

    with caplog.at_level(logging.WARNING, logger="fastmcp.server.server"):
        build_server(
            telnyx_spec,
            client=make_telnyx_client("https://api.telnyx.com/v2", transport=httpx2.MockTransport(_refuse)),
            mask_error_details=True,
        )
    assert not [r for r in caplog.records if "mask_error_details" in r.getMessage()]
