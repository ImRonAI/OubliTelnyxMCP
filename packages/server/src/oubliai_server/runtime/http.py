"""Shared async HTTP client for Telnyx REST calls."""

import httpx2

from oubliai_server.auth.passthrough import TelnyxUserBearerAuth

DEFAULT_TIMEOUT_SECONDS = 30.0


def make_telnyx_client(
    base_url: str,
    *,
    transport: httpx2.AsyncBaseTransport | None = None,
    api_key: str | None = None,
) -> httpx2.AsyncClient:
    """Build the client used by the OpenAPI provider; `transport` is for tests.

    Default (BYOK): `TelnyxUserBearerAuth` forwards the connected user's own token.
    `api_key` (single-tenant mode, `OUBLIAI_TELNYX_API_KEY`): every upstream call carries the
    server's Telnyx key instead, so the MCP layer must gate callers itself.
    """
    auth: httpx2.Auth = (
        TelnyxUserBearerAuth() if api_key is None else _ServerApiKeyAuth(api_key)
    )
    return httpx2.AsyncClient(
        base_url=base_url,
        auth=auth,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        transport=transport,
    )


class _ServerApiKeyAuth(httpx2.Auth):
    def __init__(self, api_key: str) -> None:
        self._header = f"Bearer {api_key}"

    def auth_flow(self, request: httpx2.Request):
        request.headers["Authorization"] = self._header
        yield request
