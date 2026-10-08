"""CORS for browser-based hosts that call the MCP endpoint directly.

FastMCP's Host/Origin guard (`allowed_origins`) only decides whether a request reaches MCP
session handling; it emits no CORS response headers. The documented seam for browser
JavaScript is Starlette's `CORSMiddleware` passed through `http_app(middleware=...)` with the
MCP headers allowed and `mcp-session-id` exposed, and exact origins in production
(`docs/reference/fastmcp/pages/http-deployment.md`, "CORS for Browser-Based Clients").

The application host in `packages/app` is exactly such a client (its page connects from
`http://<host-origin>` to `<OUBLIAI_BASE_URL>/mcp`), so the deployed server must list the
host origin in `OUBLIAI_BROWSER_ORIGINS`. ChatGPT/Claude-style hosts do not need this.
"""

import json
from collections.abc import Mapping

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

BROWSER_ORIGINS_ENV = "OUBLIAI_BROWSER_ORIGINS"
MCP_REQUEST_HEADERS = ("mcp-protocol-version", "mcp-session-id", "Authorization", "Content-Type")
MCP_EXPOSED_HEADERS = ("mcp-session-id",)


def browser_cors_middleware(origins: list[str]) -> list[Middleware]:
    """Starlette middleware list for `FastMCP.http_app(middleware=...)` / `run(middleware=...)`."""
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=list(MCP_REQUEST_HEADERS),
            expose_headers=list(MCP_EXPOSED_HEADERS),
        )
    ]


def browser_origins_from_env(env: Mapping[str, str]) -> list[str]:
    """Exact browser origins from `OUBLIAI_BROWSER_ORIGINS` (JSON list); empty when unset.

    A wildcard is refused: the FastMCP guide marks `allow_origins=["*"]` as unsafe in
    production, and this server authenticates every request with a user token.
    """
    raw = env.get(BROWSER_ORIGINS_ENV)
    if not raw:
        return []
    origins = json.loads(raw)
    if not isinstance(origins, list) or not all(isinstance(o, str) for o in origins):
        raise SystemExit(f"{BROWSER_ORIGINS_ENV} must be a JSON list of origin strings")
    if "*" in origins:
        raise SystemExit(f"{BROWSER_ORIGINS_ENV} must list exact origins, not '*'")
    return origins
