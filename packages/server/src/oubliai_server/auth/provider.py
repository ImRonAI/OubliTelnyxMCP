"""Telnyx OAuth for MCP clients: FastMCP OAuthProxy over Telnyx's confidential-client flow."""

from typing import Any

import httpx2
from fastmcp.server.auth import OAuthProxy
from fastmcp.server.auth.providers.introspection import IntrospectionTokenVerifier
from key_value.aio.protocols import AsyncKeyValue

from oubliai_server.spec import oauth_endpoints

# Telnyx: 5 introspections / 60 s per client. Keep well under that while bounding how long
# a revoked upstream token keeps working.
INTROSPECTION_CACHE_TTL_SECONDS = 60


def build_auth(
    spec: dict[str, Any],
    *,
    base_url: str,
    client_id: str,
    client_secret: str,
    jwt_signing_key: str,
    allowed_client_redirect_uris: list[str],
    http_client: httpx2.AsyncClient | None = None,
    client_storage: AsyncKeyValue | None = None,
) -> OAuthProxy:
    """Proxy MCP-client OAuth to Telnyx and validate Telnyx tokens by introspection.

    Endpoints come from the schema's `oauthClientAuth` scheme; scopes from Telnyx's
    authorization-server metadata (see `spec.oauth_endpoints`). The proxy stores each
    user's upstream Telnyx token, so `get_access_token().token` is that user's own
    credential.

    Introspection results are cached for `INTROSPECTION_CACHE_TTL_SECONDS` because live
    Telnyx rate-limits `POST /v2/oauth/introspect` to 5 requests per 60 s per client
    (`ratelimit-limit: 5;w=60`; a 6th call returns 429 code 10011, observed 2026-10-07).
    Without the cache every MCP request introspects and the proxy answers `invalid_token`
    after five calls. Revocation is therefore honoured within the TTL, not instantly.
    """
    endpoints = oauth_endpoints(spec)
    verifier = IntrospectionTokenVerifier(
        introspection_url=endpoints["introspection_url"],
        client_id=client_id,
        client_secret=client_secret,
        client_auth_method="client_secret_basic",
        http_client=http_client,
        cache_ttl_seconds=INTROSPECTION_CACHE_TTL_SECONDS,
    )
    return OAuthProxy(
        upstream_authorization_endpoint=endpoints["authorization_url"],
        upstream_token_endpoint=endpoints["token_url"],
        upstream_client_id=client_id,
        upstream_client_secret=client_secret,
        token_verifier=verifier,
        base_url=base_url,
        valid_scopes=endpoints["scopes"],
        allowed_client_redirect_uris=allowed_client_redirect_uris,
        jwt_signing_key=jwt_signing_key,
        require_authorization_consent=True,
        client_storage=client_storage,
    )
