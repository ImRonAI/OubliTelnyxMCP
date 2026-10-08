import base64
from urllib.parse import parse_qs

import httpx2
from fastmcp.server.auth import OAuthProxy
from key_value.aio.stores.memory import MemoryStore

from oubliai_server.auth.provider import build_auth

INTROSPECT_URL = "https://api.telnyx.com/v2/oauth/introspect"


def _build(spec, handler):
    return build_auth(
        spec,
        base_url="http://127.0.0.1:8000",
        client_id="oubliai-client",
        client_secret="client-secret-value",
        jwt_signing_key="test-signing-key-material",
        allowed_client_redirect_uris=["http://localhost:*"],
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(handler)),
        client_storage=MemoryStore(),
    )


def _introspection(active_tokens: set[str], seen: list[httpx2.Request]):
    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        token = parse_qs(request.content.decode())["token"][0]
        if token in active_tokens:
            return httpx2.Response(
                200, json={"active": True, "client_id": "oubliai-client", "scope": "numbers.read numbers.write"}
            )
        return httpx2.Response(200, json={"active": False})

    return handler


def test_proxy_targets_schema_endpoints(telnyx_spec):
    auth = _build(telnyx_spec, _introspection(set(), []))
    assert isinstance(auth, OAuthProxy)
    assert auth._upstream_authorization_endpoint == "https://api.telnyx.com/v2/oauth/authorize"
    assert auth._upstream_token_endpoint == "https://api.telnyx.com/v2/oauth/token"


async def test_introspection_accepts_active_telnyx_token(telnyx_spec):
    seen: list[httpx2.Request] = []
    auth = _build(telnyx_spec, _introspection({"telnyx-user-token"}, seen))
    access_token = await auth._token_validator.verify_token("telnyx-user-token")

    assert access_token is not None
    assert access_token.token == "telnyx-user-token"
    request = seen[0]
    assert str(request.url) == INTROSPECT_URL
    expected = base64.b64encode(b"oubliai-client:client-secret-value").decode()
    assert request.headers["authorization"] == f"Basic {expected}"


async def test_introspection_rejects_inactive_token(telnyx_spec):
    auth = _build(telnyx_spec, _introspection(set(), []))
    assert await auth._token_validator.verify_token("revoked") is None


async def test_introspection_results_are_cached_within_telnyx_rate_limit(telnyx_spec):
    """Live Telnyx limits POST /v2/oauth/introspect to 5 requests per 60 s per client
    (`ratelimit-limit: 5;w=60`, observed 2026-10-07; a 6th call returned 429 code 10011 and
    the proxy answered `invalid_token`). Repeated verification of the same token must be
    served from FastMCP's documented introspection cache, not from Telnyx."""
    seen: list[httpx2.Request] = []
    auth = _build(telnyx_spec, _introspection({"telnyx-user-token"}, seen))
    for _ in range(10):
        assert await auth._token_validator.verify_token("telnyx-user-token") is not None
    assert len(seen) == 1
