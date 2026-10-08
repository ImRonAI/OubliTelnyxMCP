"""Browser hosts call the MCP endpoint cross-origin; FastMCP emits no CORS headers by itself.

`docs/reference/fastmcp/pages/http-deployment.md` ("CORS for Browser-Based Clients") is the
documented seam: `http_app(middleware=[Middleware(CORSMiddleware, ...)])` with the MCP headers
(`mcp-protocol-version`, `mcp-session-id`, `Authorization`, `Content-Type`) allowed and
`mcp-session-id` exposed, and exact origins rather than `*` in production.
"""

import httpx2
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.tests import asgi_server
from fastmcp_tasks import TasksExtension

from oubliai_server import build_server
from oubliai_server.runtime.cors import browser_cors_middleware

ORIGIN = "http://localhost:8080"


def _server(telnyx_spec):
    return build_server(
        telnyx_spec,
        auth=StaticTokenVerifier(tokens={"user-token": {"client_id": "user", "scopes": []}}),
        tasks=TasksExtension(url="memory://"),
    )


async def _preflight(app, origin: str) -> httpx2.Response:
    async with httpx2.AsyncClient(
        transport=httpx2.ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as http:
        return await http.options(
            "/mcp",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "authorization,content-type,mcp-protocol-version,mcp-session-id",
            },
        )


async def test_browser_origin_gets_cors_headers_for_mcp(telnyx_spec):
    server = _server(telnyx_spec)
    async with asgi_server(
        server, middleware=browser_cors_middleware([ORIGIN]), allowed_origins=[ORIGIN]
    ) as running:
        response = await _preflight(running.app, ORIGIN)

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ORIGIN
    allowed = {h.strip().lower() for h in response.headers["access-control-allow-headers"].split(",")}
    assert {"mcp-protocol-version", "mcp-session-id", "authorization", "content-type"} <= allowed


async def test_actual_response_exposes_session_header(telnyx_spec):
    """`Access-Control-Expose-Headers` belongs on actual responses (not preflights); without
    `mcp-session-id` there, browser JavaScript cannot read the session id (FastMCP guide)."""
    server = _server(telnyx_spec)
    async with asgi_server(
        server, middleware=browser_cors_middleware([ORIGIN]), allowed_origins=[ORIGIN]
    ) as running:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=running.app), base_url="http://127.0.0.1"
        ) as http:
            response = await http.post(
                "/mcp",
                headers={"Origin": ORIGIN, "Content-Type": "application/json"},
                json={},
            )

    assert response.headers["access-control-allow-origin"] == ORIGIN
    assert "mcp-session-id" in response.headers["access-control-expose-headers"].lower()


async def test_unlisted_origin_gets_no_cors_headers(telnyx_spec):
    server = _server(telnyx_spec)
    async with asgi_server(
        server, middleware=browser_cors_middleware([ORIGIN]), allowed_origins=[ORIGIN]
    ) as running:
        response = await _preflight(running.app, "https://evil.example")

    assert "access-control-allow-origin" not in response.headers


def test_browser_origins_from_env_rejects_wildcard():
    from oubliai_server.runtime.cors import browser_origins_from_env

    assert browser_origins_from_env({}) == []
    assert browser_origins_from_env({"OUBLIAI_BROWSER_ORIGINS": '["http://localhost:8080"]'}) == [
        "http://localhost:8080"
    ]
    import pytest

    with pytest.raises(SystemExit):
        browser_origins_from_env({"OUBLIAI_BROWSER_ORIGINS": '["*"]'})
