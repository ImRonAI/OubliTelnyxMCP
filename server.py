"""Prefect Horizon & FastMCP CLI entrypoint (`server.py` / `server.py:mcp` / `server.py:create_server`).

FastMCP's `FileSystemSource` requires a top-level `FastMCP` instance named `mcp` (or `server` / `app`)
when invoked as `fastmcp inspect server.py` or `fastmcp run server.py` without `:object`.
During build-time inspection (`fastmcp inspect`) when runtime auth secrets are not yet injected,
this module falls back to an unauthenticated `build_server()` instance so all four model-facing
tools (`search`, `get_schema`, `execute`, `generate_prefab_ui`) and UI resources are discoverable.
"""

import os
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "packages" / "server" / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import fastmcp
from fastmcp import FastMCP

from oubliai_server.__main__ import (
    PLATFORM_AUTH_ENV,
    REQUIRED_ENV,
    SINGLE_TENANT_ACCESS_TOKEN_ENV,
    SINGLE_TENANT_API_KEY_ENV,
    create_server as _strict_create_server,
)
from oubliai_server.server import build_server
from oubliai_server.spec import load_telnyx_spec


def _has_runtime_auth_env() -> bool:
    if os.environ.get(SINGLE_TENANT_API_KEY_ENV):
        return True
    return all(bool(os.environ.get(name)) for name in REQUIRED_ENV)


def create_server() -> FastMCP:
    """Create the FastMCP server for Prefect Horizon or `fastmcp inspect`."""
    if _has_runtime_auth_env():
        if os.environ.get(SINGLE_TENANT_API_KEY_ENV) and not (
            os.environ.get(SINGLE_TENANT_ACCESS_TOKEN_ENV)
            or os.environ.get(PLATFORM_AUTH_ENV)
        ):
            # On Prefect Horizon, platform auth gates `/mcp` in front of the container.
            os.environ[PLATFORM_AUTH_ENV] = "true"
        if fastmcp.settings.http_host_origin_protection is not True:
            fastmcp.settings.http_host_origin_protection = True
        return _strict_create_server()
    return build_server(load_telnyx_spec(), mask_error_details=True)


mcp: FastMCP = create_server()
server: FastMCP = mcp
app: FastMCP = mcp
