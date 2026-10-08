from collections.abc import AsyncIterator, Callable

import httpx2
import pytest
from fastmcp import Client, FastMCP
from fastmcp.client.transports import ClientTransport
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.tests import asgi_client
from fastmcp_tasks import TasksExtension

from oubliai_server import build_server
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.spec import load_telnyx_spec

TelnyxHandler = Callable[[httpx2.Request], httpx2.Response]
MockTelnyx = Callable[[TelnyxHandler], httpx2.AsyncClient]
RealServer = Callable[[TelnyxHandler | None], FastMCP]


def _refuse_telnyx(request: httpx2.Request) -> httpx2.Response:
    raise AssertionError(f"unexpected Telnyx request: {request.method} {request.url}")


@pytest.fixture(scope="session")
def telnyx_spec():
    return load_telnyx_spec()


@pytest.fixture
async def mock_telnyx() -> AsyncIterator[MockTelnyx]:
    clients: list[httpx2.AsyncClient] = []

    def create(handler: TelnyxHandler) -> httpx2.AsyncClient:
        client = make_telnyx_client(
            "https://api.telnyx.com/v2",
            transport=httpx2.MockTransport(handler),
        )
        clients.append(client)
        return client

    yield create

    for client in clients:
        await client.aclose()


@pytest.fixture
def real_server(telnyx_spec, mock_telnyx: MockTelnyx) -> RealServer:
    def create(handler: TelnyxHandler | None = None) -> FastMCP:
        return build_server(
            telnyx_spec,
            client=mock_telnyx(handler or _refuse_telnyx),
            auth=StaticTokenVerifier(
                tokens={"user-token": {"client_id": "client", "scopes": []}}
            ),
            tasks=TasksExtension(url="memory://"),
        )

    return create


@pytest.fixture
async def http_client(
    real_server: RealServer,
) -> AsyncIterator[Client[ClientTransport]]:
    async with asgi_client(real_server(), auth="user-token") as client:
        yield client
