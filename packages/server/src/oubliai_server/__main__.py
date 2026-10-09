"""HTTP entry point: `fastmcp run fastmcp.json` or `python -m oubliai_server`.

Host, port and path come from `fastmcp.json` `deployment` or FastMCP's `FASTMCP_HOST`,
`FASTMCP_PORT` and `FASTMCP_STREAMABLE_HTTP_PATH` settings. The Host/Origin guard comes
from FastMCP's `FASTMCP_HTTP_HOST_ORIGIN_PROTECTION` / `FASTMCP_HTTP_ALLOWED_HOSTS`
settings, which must be set in the process environment: `fastmcp run` applies
`deployment.env` after `fastmcp.settings` is loaded.

OAuthProxy state is persisted through `runtime/storage.py` (`OUBLIAI_STORAGE_URL`,
encrypted with the required `OUBLIAI_STORAGE_ENCRYPTION_KEY`). Background tasks use
FastMCP's `FASTMCP_DOCKET_*` settings.

Browser hosts (the `packages/app` page) connect to `/mcp` cross-origin; set
`OUBLIAI_BROWSER_ORIGINS` (JSON list of exact origins) so `main()` adds FastMCP's documented
CORS middleware and trusts those origins. `fastmcp run fastmcp.json` cannot pass middleware,
so browser-facing deployments start with `python -m oubliai_server`.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

# Ensure packages/server/src is importable when invoked directly via file path
_SERVER_SRC = Path(__file__).resolve().parent.parent
if str(_SERVER_SRC) not in sys.path:
    sys.path.insert(0, str(_SERVER_SRC))

import fastmcp
from fastmcp import FastMCP

from oubliai_server.auth.provider import build_auth
from oubliai_server.runtime.cors import browser_cors_middleware, browser_origins_from_env
from oubliai_server.runtime.storage import ENCRYPTION_KEY_ENV, build_client_storage
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.server import build_server
from oubliai_server.spec import default_base_url, load_telnyx_spec

REQUIRED_ENV = (
    "OUBLIAI_BASE_URL",
    "OUBLIAI_TELNYX_CLIENT_ID",
    "OUBLIAI_TELNYX_CLIENT_SECRET",
    "OUBLIAI_JWT_SIGNING_KEY",
    "OUBLIAI_ALLOWED_CLIENT_REDIRECT_URIS",
    ENCRYPTION_KEY_ENV,
)


def _require_env() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
    return {name: os.environ[name] for name in REQUIRED_ENV}


def _require_host_origin_protection() -> None:
    if fastmcp.settings.http_host_origin_protection is not True:
        raise SystemExit(
            "Set FASTMCP_HTTP_HOST_ORIGIN_PROTECTION=true and FASTMCP_HTTP_ALLOWED_HOSTS "
            "(JSON list containing the public hostname) in the process environment."
        )


SINGLE_TENANT_API_KEY_ENV = "OUBLIAI_TELNYX_API_KEY"
SINGLE_TENANT_ACCESS_TOKEN_ENV = "OUBLIAI_ACCESS_TOKEN"
_MIN_ACCESS_TOKEN_LENGTH = 24


def _single_tenant_server(spec: dict[str, Any], api_key: str) -> FastMCP:
    """Single-tenant mode: the server's own Telnyx key is used upstream and `/mcp` is gated by
    FastMCP's `StaticTokenVerifier` with one shared bearer (`OUBLIAI_ACCESS_TOKEN`).

    Use for a single operator's own account only: every caller who holds the access token
    acts as that account. For per-user accounts use the OAuthProxy mode (default)."""
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

    access_token = os.environ.get(SINGLE_TENANT_ACCESS_TOKEN_ENV, "")
    if len(access_token) < _MIN_ACCESS_TOKEN_LENGTH:
        raise SystemExit(
            f"{SINGLE_TENANT_ACCESS_TOKEN_ENV} must be set to a random secret of at least "
            f"{_MIN_ACCESS_TOKEN_LENGTH} characters when {SINGLE_TENANT_API_KEY_ENV} is used."
        )
    auth = StaticTokenVerifier(
        tokens={access_token: {"client_id": "oubliai-operator", "scopes": []}}
    )
    client = make_telnyx_client(default_base_url(spec), api_key=api_key)
    return build_server(spec, client=client, auth=auth, mask_error_details=True)


def create_server() -> FastMCP:
    _require_host_origin_protection()
    spec = load_telnyx_spec()
    api_key = os.environ.get(SINGLE_TENANT_API_KEY_ENV)
    if api_key:
        return _single_tenant_server(spec, api_key)
    env = _require_env()
    auth = build_auth(
        spec,
        base_url=env["OUBLIAI_BASE_URL"],
        client_id=env["OUBLIAI_TELNYX_CLIENT_ID"],
        client_secret=env["OUBLIAI_TELNYX_CLIENT_SECRET"],
        jwt_signing_key=env["OUBLIAI_JWT_SIGNING_KEY"],
        allowed_client_redirect_uris=json.loads(env["OUBLIAI_ALLOWED_CLIENT_REDIRECT_URIS"]),
        client_storage=build_client_storage(),
    )
    return build_server(spec, auth=auth, mask_error_details=True)


def run_options() -> dict[str, Any]:
    """Keyword arguments for `FastMCP.run()`; CORS only when browser origins are configured."""
    options: dict[str, Any] = {"transport": "http"}
    origins = browser_origins_from_env(os.environ)
    if origins:
        options["middleware"] = browser_cors_middleware(origins)
        options["allowed_origins"] = origins
    return options


def main() -> None:
    create_server().run(**run_options())


if __name__ == "__main__":
    main()
