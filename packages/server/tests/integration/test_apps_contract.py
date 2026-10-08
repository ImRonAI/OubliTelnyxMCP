"""Domain workspaces over the real HTTP stack: discovery, rendering, BYOK, confirm gates.

Model path: `search` -> `execute(call_tool('<domain>_workspace'))` returns a `$prefab`
payload. Renderer path: the payload's `toolCall` references are identity-addressed
backend names, callable directly; each backend runs the generated Telnyx tool with the
caller's own bearer token.
"""

import json

import httpx2
import pytest
from fastmcp.exceptions import ToolError
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.server.providers.addressing import hashed_backend_name
from fastmcp.utilities.tests import asgi_client
from fastmcp_tasks import TasksExtension

from oubliai_server import build_server
from oubliai_server.apps import ALL_APPS
from oubliai_server.apps import numbers as numbers_app
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.server import build_operations
from oubliai_server.spec import collision_names

ROWS = {"data": [{"id": "n1", "phone_number": "+15550001", "status": "active"}],
        "meta": {"total_pages": 1, "total_results": 1, "page_number": 1, "page_size": 25}}


def _server(spec, handler):
    return build_server(
        spec,
        client=make_telnyx_client("https://api.telnyx.com/v2", transport=httpx2.MockTransport(handler)),
        auth=StaticTokenVerifier(tokens={"user-token": {"client_id": "u", "scopes": []}}),
        tasks=TasksExtension(url="memory://"),
    )


def _tool_refs(node, acc: list[str]) -> list[str]:
    if isinstance(node, dict):
        if node.get("action") == "toolCall":
            acc.append(node["tool"])
        for value in node.values():
            _tool_refs(value, acc)
    elif isinstance(node, list):
        for value in node:
            _tool_refs(value, acc)
    return acc


async def test_every_referenced_generated_tool_exists_in_the_catalog(telnyx_spec):
    """Each app's GENERATED_TOOLS must be registered names on the operations child."""
    from fastmcp.server.providers.openapi import OpenAPIProvider

    operations = build_operations(
        telnyx_spec,
        make_telnyx_client("https://api.telnyx.com/v2", transport=httpx2.MockTransport(lambda r: httpx2.Response(500))),
    )
    provider = next(p for p in operations.providers if isinstance(p, OpenAPIProvider))
    registered = {tool.name for tool in await provider.list_tools()}
    overrides = collision_names(telnyx_spec)

    def registered_name(operation_id: str) -> str:
        # FastMCP: `mcp_names` override (slugified: spaces -> `_`), else the operationId up to
        # the first `__`, capped at 56 characters (openapi-integration.md, "Component Names").
        if operation_id in overrides:
            return overrides[operation_id].replace(" ", "_")
        return operation_id.split("__")[0][:56]

    for app in ALL_APPS:
        module = __import__(f"oubliai_server.apps.{app.name.removeprefix('oubliai-')}", fromlist=["GENERATED_TOOLS"])
        missing = {registered_name(name) for name in module.GENERATED_TOOLS} - registered
        assert missing == set(), (app.name, missing)


@pytest.mark.parametrize("app", ALL_APPS, ids=lambda app: app.name)
async def test_workspace_entry_reachable_via_execute(telnyx_spec, app):
    server = _server(telnyx_spec, lambda request: httpx2.Response(500))
    entry = f"{app.name.removeprefix('oubliai-')}_workspace"
    async with asgi_client(server, auth="user-token") as client:
        listed = sorted(tool.name for tool in await client.list_tools())
        result = await client.call_tool("execute", {"code": f"return await call_tool('{entry}', {{}})"})
    assert listed == ["execute", "generate_prefab_ui", "get_schema", "search"]
    payload = result.structured_content
    assert payload["$prefab"] == {"version": "0.3"}
    refs = _tool_refs(payload, [])
    assert refs and all(ref.split("_", 1)[0].isalnum() and len(ref.split("_", 1)[0]) == 12 for ref in refs)
    assert set(refs) <= set(payload["_meta"]["fastmcp"]["toolNames"])


async def test_list_backend_passes_caller_token_to_telnyx(telnyx_spec):
    received: list[httpx2.Request] = []

    def telnyx(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        return httpx2.Response(200, json=ROWS)

    server = _server(telnyx_spec, telnyx)
    backend = hashed_backend_name(numbers_app.app.name, "numbers_list")
    async with asgi_client(server, auth="user-token") as client:
        result = await client.call_tool(backend, {"page_number": 2, "page_size": 10})
    assert result.structured_content == {"rows": ROWS["data"], "meta": ROWS["meta"]}
    (request,) = received
    assert request.method == "GET"
    assert request.url.path == "/v2/phone_numbers"
    assert dict(request.url.params) == {"page[number]": "2", "page[size]": "10"}
    assert request.headers["authorization"] == "Bearer user-token"


async def test_confirmed_backend_refuses_without_matching_token(telnyx_spec):
    received: list[httpx2.Request] = []

    def telnyx(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        return httpx2.Response(200, json={"data": {"id": "n1"}})

    server = _server(telnyx_spec, telnyx)
    backend = hashed_backend_name(numbers_app.app.name, "numbers_delete")
    async with asgi_client(server, auth="user-token") as client:
        with pytest.raises(ToolError, match="Confirmation does not match"):
            await client.call_tool(backend, {"resource_id": "n1", "confirm": "wrong"})
        assert received == []
        await client.call_tool(backend, {"resource_id": "n1", "confirm": "n1"})
    (request,) = received
    assert (request.method, request.url.path) == ("DELETE", "/v2/phone_numbers/n1")
    assert request.headers["authorization"] == "Bearer user-token"


async def test_backends_are_not_reachable_through_execute(telnyx_spec):
    """App-only backends are excluded from the CodeMode catalog (host-visible only)."""
    server = _server(telnyx_spec, lambda request: httpx2.Response(500))
    async with asgi_client(server, auth="user-token") as client:
        result = await client.call_tool(
            "execute", {"code": "return await call_tool('numbers_list', {})"}, raise_on_error=False
        )
    assert result.is_error
    assert "numbers_list" in json.dumps([c.model_dump() for c in result.content])


@pytest.mark.parametrize(
    ("app_module", "backend", "path"),
    [
        ("storage", "kv_namespaces_list", "/v2/storage/kvs"),
        ("speech", "voice_designs_list", "/v2/voice_designs"),
    ],
)
async def test_bracketed_page_params_reach_telnyx(telnyx_spec, app_module, backend, path):
    """Some schema operations declare literal `page[number]`/`page[size]` query params.

    FastMCP exposes those names flat (no `page` object), so the recipe must send what the
    generated tool actually declares, or paging is silently dropped.
    """
    import importlib

    received: list[httpx2.Request] = []

    def telnyx(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        return httpx2.Response(200, json={"data": [], "meta": {"total_pages": 3}})

    module = importlib.import_module(f"oubliai_server.apps.{app_module}")
    server = _server(telnyx_spec, telnyx)
    async with asgi_client(server, auth="user-token") as client:
        await client.call_tool(
            hashed_backend_name(module.app.name, backend), {"page_number": 2, "page_size": 10}
        )
    (request,) = received
    assert request.url.path == path
    assert dict(request.url.params) == {"page[number]": "2", "page[size]": "10"}
