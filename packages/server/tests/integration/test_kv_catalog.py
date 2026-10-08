"""Telnyx KV is served by the generated tools, not by a hand-written store.

`PutKvKey`, `GetKvKey`, `DeleteKvKey` and `ListKvKeys` are schema operations; FastMCP's
OpenAPIProvider turns them into tools that carry the caller's token. This test pins
that contract end to end over HTTP so no parallel REST adapter is ever needed.
"""

import httpx2
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.tests import asgi_client
from fastmcp_tasks import TasksExtension

from oubliai_server import build_server
from oubliai_server.runtime.http import make_telnyx_client

KV_TOOLS = ("ListKvNamespaces", "CreateKvNamespace", "GetKvNamespace", "DeleteKvNamespace",
            "ListKvKeys", "GetKvKey", "PutKvKey", "DeleteKvKey")


async def test_generated_kv_tools_round_trip_bytes_with_caller_token(telnyx_spec):
    received: list[httpx2.Request] = []

    def telnyx(request: httpx2.Request) -> httpx2.Response:
        received.append(request)
        if request.method == "PUT":
            return httpx2.Response(201)
        if request.method == "GET" and request.url.path.endswith("/keys/cache/entry"):
            return httpx2.Response(200, content=b'{"hello": "kv"}', headers={"content-type": "application/json"})
        if request.method == "DELETE":
            return httpx2.Response(200)
        return httpx2.Response(404, json={"errors": [{"code": "10005"}]})

    server = build_server(
        telnyx_spec,
        client=make_telnyx_client("https://api.telnyx.com/v2", transport=httpx2.MockTransport(telnyx)),
        auth=StaticTokenVerifier(tokens={"user-token": {"client_id": "u", "scopes": []}}),
        tasks=TasksExtension(url="memory://"),
    )
    async with asgi_client(server, auth="user-token") as client:
        schema = await client.call_tool("get_schema", {"tools": list(KV_TOOLS)})
        put = await client.call_tool(
            "PutKvKey", {"id": "ns1", "key": "cache/entry", "ttl_secs": 30, "body": '{"hello": "kv"}'}
        )
        got = await client.call_tool("GetKvKey", {"id": "ns1", "key": "cache/entry"})
        deleted = await client.call_tool("DeleteKvKey", {"id": "ns1", "key": "cache/entry"})
        missing = await client.call_tool(
            "GetKvKey", {"id": "ns1", "key": "cache/missing"}, raise_on_error=False
        )

    text = schema.content[0].text
    assert "Tools not found" not in text
    for name in KV_TOOLS:
        assert f"### {name}" in text
    assert not put.is_error and not deleted.is_error
    assert got.structured_content == {"result": {"hello": "kv"}}
    assert missing.is_error and "404" in missing.content[0].text

    put_request, get_request, delete_request, _ = received
    assert put_request.method == "PUT"
    assert put_request.url.raw_path.startswith(b"/v2/storage/kvs/ns1/keys/cache%2Fentry")
    assert put_request.url.params["ttl_secs"] == "30"
    assert put_request.headers["content-type"] == "application/octet-stream"
    assert put_request.content == b'{"hello": "kv"}'
    assert get_request.method == "GET" and delete_request.method == "DELETE"
    assert {r.headers["authorization"] for r in received} == {"Bearer user-token"}
