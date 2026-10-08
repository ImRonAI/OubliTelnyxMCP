"""Background tasks: native TasksExtension on the root, `await_telnyx_resource` on the child.

`import fastmcp_tasks` enables task negotiation for every client in the process. Every
Telnyx call made by the task goes through the generated tools with the caller's token.
"""

import asyncio

import fastmcp_tasks  # noqa: F401  (registers the client-side tasks extension)
import httpx2
import pytest
from fastmcp.exceptions import ToolError
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.tests import asgi_client
from fastmcp_tasks import TasksExtension, call_tool_task

from oubliai_server import build_server
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.runtime.tasks import build_tasks_extension

TOOL = "await_telnyx_resource"


def _server(spec, statuses: list[str], path: str):
    """Telnyx mock answering `path` with `{"data": {"status": s}}`, one status per call."""
    received: list[httpx2.Request] = []

    def telnyx(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        assert request.url.path == path
        status = statuses[min(len(received) - 1, len(statuses) - 1)]
        return httpx2.Response(200, json={"data": {"id": "x", "status": status}})

    server = build_server(
        spec,
        client=make_telnyx_client("https://api.telnyx.com/v2", transport=httpx2.MockTransport(telnyx)),
        auth=StaticTokenVerifier(tokens={"user-token": {"client_id": "u", "scopes": []}}),
        tasks=TasksExtension(url="memory://"),
    )
    return server, received


def test_build_tasks_extension_reads_docket_env():
    ext = build_tasks_extension({"FASTMCP_DOCKET_URL": "memory://", "FASTMCP_DOCKET_CONCURRENCY": "3"})
    assert ext.docket_settings.url == "memory://"
    assert ext.docket_settings.concurrency == 3


async def test_number_order_poll_completes_in_background(telnyx_spec):
    server, received = _server(telnyx_spec, ["pending", "pending", "success"], "/v2/number_orders/no-1")
    async with asgi_client(server, auth="user-token") as client:
        task = await call_tool_task(
            client,
            TOOL,
            {"kind": "number_order", "resource_id": "no-1", "poll_interval_seconds": 0.01},
        )
        assert (await task.status()).status in {"working", "completed"}
        result = await task.result()
    assert result.structured_content == {
        "kind": "number_order",
        "resource_id": "no-1",
        "status": "success",
        "polls": 3,
    }
    assert len(received) == 3
    assert {r.headers.get("authorization") for r in received} == {"Bearer user-token"}


async def test_poll_exhaustion_fails(telnyx_spec):
    server, received = _server(telnyx_spec, ["pending"], "/v2/number_orders/no-2")
    async with asgi_client(server, auth="user-token") as client:
        task = await call_tool_task(
            client,
            TOOL,
            {"kind": "number_order", "resource_id": "no-2", "poll_interval_seconds": 0.01, "max_polls": 2},
        )
        with pytest.raises(ToolError, match="did not reach a terminal state"):
            await task.result()
    assert len(received) == 2


async def test_poll_cancel_stops_requests(telnyx_spec):
    server, received = _server(telnyx_spec, ["pending"], "/v2/number_orders/no-3")
    async with asgi_client(server, auth="user-token") as client:
        task = await call_tool_task(
            client,
            TOOL,
            {"kind": "number_order", "resource_id": "no-3", "poll_interval_seconds": 0.2},
        )
        while not received:
            await asyncio.sleep(0.02)
        await task.cancel()
        seen = len(received)
        await asyncio.sleep(0.6)
        assert (await task.status()).status == "cancelled"
    # Cancellation is cooperative: at most one in-flight poll may complete after cancel.
    assert len(received) <= seen + 1


async def test_task_tool_hidden_from_default_listing(telnyx_spec):
    server, _ = _server(telnyx_spec, ["pending"], "/v2/number_orders/none")
    async with asgi_client(server, auth="user-token") as client:
        names = sorted(tool.name for tool in await client.list_tools())
        search = await client.call_tool("search", {"query": "await telnyx resource"})
    assert names == ["execute", "generate_prefab_ui", "get_schema", "search"]
    assert TOOL in search.content[0].text


async def test_task_tool_runs_foreground_via_execute(telnyx_spec):
    server, received = _server(telnyx_spec, ["pending", "provision_ok"], "/v2/storage/kvs/ns-1")
    code = (
        "return await call_tool('await_telnyx_resource', "
        "{'kind': 'kv_namespace', 'resource_id': 'ns-1', 'poll_interval_seconds': 0.01})"
    )
    async with asgi_client(server, auth="user-token") as client:
        result = await client.call_tool("execute", {"code": code})
    assert result.structured_content == {
        "kind": "kv_namespace",
        "resource_id": "ns-1",
        "status": "provision_ok",
        "polls": 2,
    }
    assert len(received) == 2


def test_persistent_docket_requires_snapshot_encryption_key():
    """tasks.md "Credentials at Rest": Redis/Valkey snapshots hold the caller's token in plaintext
    unless FASTMCP_TASKS_ENCRYPTION_KEY is set. memory:// never leaves the process."""
    with pytest.raises(SystemExit, match="FASTMCP_TASKS_ENCRYPTION_KEY"):
        build_tasks_extension({"FASTMCP_DOCKET_URL": "redis://localhost:6379/0"})
    ext = build_tasks_extension(
        {"FASTMCP_DOCKET_URL": "redis://localhost:6379/0", "FASTMCP_TASKS_ENCRYPTION_KEY": "k" * 32}
    )
    assert ext.docket_settings.url == "redis://localhost:6379/0"
    assert build_tasks_extension({"FASTMCP_DOCKET_URL": "memory://"}).docket_settings.url == "memory://"


async def test_kv_namespace_deleting_is_not_terminal(telnyx_spec):
    """KvNamespace.status: `deleting` is transitional ("Once deletion completes, the namespace
    no longer appears in the API"); only provision_ok/provision_failed/delete_failed end a poll."""
    server, received = _server(telnyx_spec, ["deleting", "deleting", "delete_failed"], "/v2/storage/kvs/ns-del")
    async with asgi_client(server, auth="user-token") as client:
        task = await call_tool_task(
            client,
            TOOL,
            {"kind": "kv_namespace", "resource_id": "ns-del", "poll_interval_seconds": 0.01},
        )
        result = await task.result()
    assert result.structured_content["status"] == "delete_failed"
    assert result.structured_content["polls"] == 3
    assert len(received) == 3
