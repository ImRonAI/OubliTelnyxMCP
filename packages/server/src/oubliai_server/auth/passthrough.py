"""Forward the connected user's own bearer token to Telnyx (BYOK)."""

from collections.abc import Generator

import httpx2
from fastmcp.server.dependencies import get_access_token


class MissingUserTokenError(RuntimeError):
    """Raised when a Telnyx request is attempted without an authenticated user."""


class TelnyxUserBearerAuth(httpx2.Auth):
    """Set `Authorization` from the MCP request's access token.

    FastMCP's OpenAPI tools do not forward the inbound `authorization` header, so the
    token is attached here. There is deliberately no server-wide fallback key: every
    upstream call is bound to the caller's account.
    """

    def auth_flow(
        self, request: httpx2.Request
    ) -> Generator[httpx2.Request, httpx2.Response, None]:
        access_token = get_access_token()
        if access_token is None:
            raise MissingUserTokenError(
                "No authenticated user token is available for this Telnyx request."
            )
        request.headers["Authorization"] = f"Bearer {access_token.token}"
        yield request
