import httpx2
from fastmcp.utilities.tests import asgi_client

from oubliai_client import execute


async def test_get_user_balance_propagates_connected_bearer(real_server) -> None:
    received: list[httpx2.Request] = []

    def telnyx(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        return httpx2.Response(
            200,
            json={
                "data": {
                    "record_type": "balance",
                    "pending": "10.00",
                    "balance": "300.00",
                    "credit_limit": "100.00",
                    "available_credit": "400.00",
                    "currency": "USD",
                }
            },
        )

    async with asgi_client(real_server(telnyx), auth="user-token") as client:
        result = await execute(
            client,
            'return await call_tool("GetUserBalance", {})',
        )

    assert not result.is_error, result.content
    (request,) = received
    assert request.method == "GET"
    assert request.url.path == "/v2/balance"
    assert request.headers["authorization"] == "Bearer user-token"
    assert result.structured_content == {
        "data": {
            "record_type": "balance",
            "pending": "10.00",
            "balance": "300.00",
            "credit_limit": "100.00",
            "available_credit": "400.00",
            "currency": "USD",
        }
    }
