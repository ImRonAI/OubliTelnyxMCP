"""Demo functions against the in-process server fixture; no live Telnyx calls."""

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

from workspace_demo import (
    open_numbers,
    renderer_info,
    show_catalog,
    summarize,
    track_number_order,
)

TelnyxHandler = Callable[[httpx2.Request], httpx2.Response]


def _refuse_telnyx(request: httpx2.Request) -> httpx2.Response:
    raise AssertionError(f"unexpected Telnyx request: {request.method} {request.url}")


@pytest.fixture(scope="session")
def telnyx_spec():
    return load_telnyx_spec()


@pytest.fixture
async def mock_telnyx() -> AsyncIterator[Callable[[TelnyxHandler], httpx2.AsyncClient]]:
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
def real_server(telnyx_spec, mock_telnyx) -> Callable[[TelnyxHandler | None], FastMCP]:
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
async def http_client(real_server) -> AsyncIterator[Client[ClientTransport]]:
    async with asgi_client(real_server(), auth="user-token") as client:
        yield client


async def test_summarize_lists_the_four_model_visible_tools(
    http_client: Client[ClientTransport],
    capsys: pytest.CaptureFixture[str],
) -> None:
    await summarize(http_client)
    out = capsys.readouterr().out
    assert "server:" in out
    for name in ("search", "get_schema", "execute", "generate_prefab_ui"):
        assert f"- {name}" in out


async def test_show_catalog_prints_search_and_schema_results(
    http_client: Client[ClientTransport],
    capsys: pytest.CaptureFixture[str],
) -> None:
    await show_catalog(http_client)
    out = capsys.readouterr().out
    assert out.count("ListAvailablePhoneNumbers") >= 1


async def test_open_numbers_prints_the_prefab_version(
    http_client: Client[ClientTransport],
    capsys: pytest.CaptureFixture[str],
) -> None:
    await open_numbers(http_client)
    out = capsys.readouterr().out
    assert "workspace numbers: prefab 0.3" in out


async def test_renderer_info_prints_mime_and_uri(
    http_client: Client[ClientTransport],
    capsys: pytest.CaptureFixture[str],
) -> None:
    await renderer_info(http_client)
    out = capsys.readouterr().out
    assert "ui://prefab/generative.html" in out
    assert "text/html;profile=mcp-app" in out


async def test_track_number_order_prints_success(
    real_server,
    capsys: pytest.CaptureFixture[str],
) -> None:
    received: list[httpx2.Request] = []
    statuses = ["pending", "success"]

    def handler(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        assert request.url.path == "/v2/number_orders/no-1"
        status = statuses[min(len(received) - 1, len(statuses) - 1)]
        return httpx2.Response(200, json={"data": {"id": "no-1", "status": status}})

    async with asgi_client(real_server(handler), auth="user-token") as client:
        await track_number_order(client, "no-1", poll_seconds=0.01)

    out = capsys.readouterr().out
    assert "no-1: success (polls=2)" in out
