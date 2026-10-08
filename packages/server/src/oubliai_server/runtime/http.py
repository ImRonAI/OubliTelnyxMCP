"""Shared async HTTP client for Telnyx REST calls."""

import httpx2

from oubliai_server.auth.passthrough import TelnyxUserBearerAuth

DEFAULT_TIMEOUT_SECONDS = 30.0


def make_telnyx_client(
    base_url: str, *, transport: httpx2.AsyncBaseTransport | None = None
) -> httpx2.AsyncClient:
    """Build the client used by the OpenAPI provider; `transport` is for tests."""
    return httpx2.AsyncClient(
        base_url=base_url,
        auth=TelnyxUserBearerAuth(),
        timeout=DEFAULT_TIMEOUT_SECONDS,
        transport=transport,
    )
