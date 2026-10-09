from unittest.mock import patch

import httpx2
import pytest
from fastmcp.server.auth import AccessToken

from oubliai_server.auth.passthrough import MissingUserTokenError
from oubliai_server.runtime.http import make_telnyx_client

PATCH_TARGET = "oubliai_server.auth.passthrough.get_access_token"


def _echo_auth_client() -> httpx2.AsyncClient:
    def echo(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"auth": request.headers.get("authorization")})

    return make_telnyx_client("https://api.telnyx.com/v2", transport=httpx2.MockTransport(echo))


async def test_forwards_connected_user_token():
    token = AccessToken(token="user-token", client_id="c", scopes=[])
    with patch(PATCH_TARGET, return_value=token):
        async with _echo_auth_client() as client:
            response = await client.get("/balance")
    assert response.json() == {"auth": "Bearer user-token"}


async def test_refuses_without_user_token():
    with patch(PATCH_TARGET, return_value=None):
        async with _echo_auth_client() as client:
            with pytest.raises(MissingUserTokenError):
                await client.get("/balance")


async def test_single_tenant_mode_uses_server_api_key_for_every_call():
    """`OUBLIAI_TELNYX_API_KEY` mode: the server's own Telnyx key is sent upstream regardless
    of the connected caller's token (callers are gated by a static bearer instead)."""
    caller = AccessToken(token="shared-access-token", client_id="c", scopes=[])

    def echo(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"auth": request.headers.get("authorization")})

    with patch(PATCH_TARGET, return_value=caller):
        async with make_telnyx_client(
            "https://api.telnyx.com/v2",
            transport=httpx2.MockTransport(echo),
            api_key="KEY_server_side",
        ) as client:
            response = await client.get("/balance")
    assert response.json() == {"auth": "Bearer KEY_server_side"}
