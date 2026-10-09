import asyncio
from collections.abc import Callable

import httpx2
import pytest
from fastmcp.exceptions import ToolError
from fastmcp.utilities.tests import asgi_client

from oubliai_client.tasks import await_telnyx_resource_task, wait_for


def _status_handler(
    statuses: list[str],
    path: str,
    received: list[httpx2.Request],
) -> Callable[[httpx2.Request], httpx2.Response]:
    def handler(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        assert request.url.path == path
        status = statuses[min(len(received) - 1, len(statuses) - 1)]
        return httpx2.Response(200, json={"data": {"id": request.url.path.rsplit("/", 1)[-1], "status": status}})

    return handler


async def test_await_telnyx_resource_task_completes(real_server) -> None:
    received: list[httpx2.Request] = []
    handler = _status_handler(
        ["pending", "pending", "success"],
        "/v2/number_orders/5bd1ad8e-5e2d-4c74-9b0a-1f3f3a3c7f01",
        received,
    )

    async with asgi_client(real_server(handler), auth="user-token") as client:
        task = await await_telnyx_resource_task(
            client,
            kind="number_order",
            resource_id="5bd1ad8e-5e2d-4c74-9b0a-1f3f3a3c7f01",
            poll_interval_seconds=0.01,
        )
        result = await task

    assert result.structured_content == {
        "kind": "number_order",
        "resource_id": "5bd1ad8e-5e2d-4c74-9b0a-1f3f3a3c7f01",
        "status": "success",
        "polls": 3,
    }
    assert len(received) == 3


async def test_wait_for_returns_completed_result(real_server) -> None:
    received: list[httpx2.Request] = []
    handler = _status_handler(
        ["pending", "provision_ok"],
        "/v2/storage/kvs/9f1c2b7e-0d2a-4e5b-8a7c-2b4f6d8e0a13",
        received,
    )

    async with asgi_client(real_server(handler), auth="user-token") as client:
        task = await await_telnyx_resource_task(
            client,
            kind="kv_namespace",
            resource_id="9f1c2b7e-0d2a-4e5b-8a7c-2b4f6d8e0a13",
            poll_interval_seconds=0.01,
        )
        result = await wait_for(task, timeout=5.0)

    assert result.structured_content == {
        "kind": "kv_namespace",
        "resource_id": "9f1c2b7e-0d2a-4e5b-8a7c-2b4f6d8e0a13",
        "status": "provision_ok",
        "polls": 2,
    }


async def test_await_telnyx_resource_task_cancels(real_server) -> None:
    received: list[httpx2.Request] = []
    handler = _status_handler(
        ["pending"],
        "/v2/number_orders/no-2",
        received,
    )

    async with asgi_client(real_server(handler), auth="user-token") as client:
        task = await await_telnyx_resource_task(
            client,
            kind="number_order",
            resource_id="no-2",
            poll_interval_seconds=0.2,
        )
        while not received:
            await asyncio.sleep(0.02)
        await task.cancel()
        seen = len(received)
        await asyncio.sleep(0.6)
        assert (await task.status()).status == "cancelled"

    assert len(received) <= seen + 1


async def test_await_telnyx_resource_task_exhaustion_raises(real_server) -> None:
    received: list[httpx2.Request] = []
    handler = _status_handler(
        ["pending"],
        "/v2/number_orders/no-3",
        received,
    )

    async with asgi_client(real_server(handler), auth="user-token") as client:
        task = await await_telnyx_resource_task(
            client,
            kind="number_order",
            resource_id="no-3",
            poll_interval_seconds=0.01,
            max_polls=2,
        )
        with pytest.raises(ToolError, match="did not reach a terminal state"):
            await task

    assert len(received) == 2


async def test_wait_for_times_out_and_task_can_be_cancelled(real_server) -> None:
    received: list[httpx2.Request] = []
    handler = _status_handler(
        ["pending"],
        "/v2/number_orders/no-4",
        received,
    )

    async with asgi_client(real_server(handler), auth="user-token") as client:
        task = await await_telnyx_resource_task(
            client,
            kind="number_order",
            resource_id="no-4",
            poll_interval_seconds=0.2,
        )
        with pytest.raises(TimeoutError, match="within 0.01s"):
            await wait_for(task, timeout=0.01)
        await task.cancel()
        assert (await task.status()).status == "cancelled"
