import httpx2
from fastmcp import Client

from oubliai_server import build_server
from oubliai_server.apps import ALL_APPS
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.server import OAUTH_PROTOCOL_TAG
from oubliai_server.spec import _operations, foreign_server_routes


def _offline_client() -> httpx2.AsyncClient:
    def refuse(request: httpx2.Request) -> httpx2.Response:
        raise AssertionError(f"unexpected network call: {request.url}")

    return make_telnyx_client(
        "https://api.telnyx.com/v2", transport=httpx2.MockTransport(refuse)
    )


async def test_default_model_visible_tools(telnyx_spec):
    server = build_server(telnyx_spec, client=_offline_client())
    async with Client(server) as client:
        names = sorted(tool.name for tool in await client.list_tools())
    assert names == ["execute", "generate_prefab_ui", "get_schema", "search"]


async def test_generative_ui_keeps_app_metadata(telnyx_spec):
    server = build_server(telnyx_spec, client=_offline_client())
    async with Client(server) as client:
        tools = {tool.name: tool for tool in await client.list_tools()}
    meta = tools["generate_prefab_ui"].meta or {}
    assert "ui" in meta, meta


async def test_search_reaches_generated_telnyx_operations(telnyx_spec):
    server = build_server(telnyx_spec, client=_offline_client())
    async with Client(server) as client:
        result = await client.call_tool("search", {"query": "send an SMS message"})
    text = result.content[0].text
    assert f"of {_expected_tool_count(telnyx_spec)} tools" in text
    assert "- SendMessage:" in text


def _excluded_operation_ids(spec) -> set[str]:
    foreign = foreign_server_routes(spec)
    return {
        operation["operationId"]
        for method, path, operation in _operations(spec)
        if OAUTH_PROTOCOL_TAG in operation.get("tags", []) or (method, path) in foreign
    }


def _expected_tool_count(spec) -> int:
    # Generated operations minus exclusions, plus the native `await_telnyx_resource` task
    # tool and one model-visible workspace entry per domain app (backends are app-only).
    return sum(1 for _ in _operations(spec)) - len(_excluded_operation_ids(spec)) + 1 + len(ALL_APPS)


async def test_oauth_protocol_and_foreign_server_operations_are_excluded(telnyx_spec):
    excluded = _excluded_operation_ids(telnyx_spec)
    assert {
        "ExchangeOAuthToken",
        "IntrospectOAuthToken",
        "RegisterOAuthClient",
        "CreateOAuthGrant",
        "x402_v1ChatCompletions",
        "TranscriptionOverWs",
    } <= excluded
    server = build_server(telnyx_spec, client=_offline_client())
    async with Client(server) as client:
        result = await client.call_tool("get_schema", {"tools": sorted(excluded)})
    assert result.content[0].text == f"Tools not found: {', '.join(sorted(excluded))}"


async def test_no_fastmcp_collision_suffixes(telnyx_spec):
    """Every `_N` tool name must be Telnyx's own operationId, never a FastMCP tiebreak."""
    from fastmcp.server.providers.openapi import OpenAPIProvider

    from oubliai_server.server import build_operations

    operations = build_operations(telnyx_spec, _offline_client())
    provider = next(p for p in operations.providers if isinstance(p, OpenAPIProvider))
    names = {tool.name for tool in await provider.list_tools()}
    operation_ids = {operation["operationId"] for _, _, operation in _operations(telnyx_spec)}
    tiebreaks = {
        name
        for name in names
        if name not in operation_ids and name.rsplit("_", 1)[-1].isdigit()
    }
    assert tiebreaks == set()
    assert {
        "Get_insights_for_a_conversation",
        "Get_conversation_messages",
        "Create_initial_plan",
        "Add_steps_to_plan",
    } <= names


async def test_search_lists_workspace_entries_but_not_backends(telnyx_spec):
    server = build_server(telnyx_spec, client=_offline_client())
    async with Client(server) as client:
        result = await client.call_tool("search", {"query": "phone numbers workspace"})
    text = result.content[0].text
    assert "- numbers_workspace" in text
    assert "numbers_list" not in text


async def test_server_owned_telnyx_client_is_closed_on_shutdown(telnyx_spec, monkeypatch):
    """`build_server` creates the Telnyx client when none is injected; it must close it via lifespan."""
    import oubliai_server.server as server_module

    created: list[httpx2.AsyncClient] = []
    real_factory = server_module.make_telnyx_client

    def recording_factory(base_url, **kwargs):
        client = real_factory(base_url, transport=httpx2.MockTransport(lambda r: httpx2.Response(500)))
        created.append(client)
        return client

    monkeypatch.setattr(server_module, "make_telnyx_client", recording_factory)
    server = build_server(telnyx_spec)
    async with Client(server):
        assert created and not created[0].is_closed
    assert created[0].is_closed


async def test_injected_telnyx_client_stays_caller_owned(telnyx_spec):
    client = _offline_client()
    async with Client(build_server(telnyx_spec, client=client)):
        pass
    assert not client.is_closed
