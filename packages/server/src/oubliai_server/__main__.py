"""HTTP entry point: `fastmcp run fastmcp.json` or `python -m oubliai_server`.

Host, port and path come from `fastmcp.json` `deployment` or FastMCP's `FASTMCP_HOST`,
`FASTMCP_PORT` and `FASTMCP_STREAMABLE_HTTP_PATH` settings. The Host/Origin guard comes
from FastMCP's `FASTMCP_HTTP_HOST_ORIGIN_PROTECTION` / `FASTMCP_HTTP_ALLOWED_HOSTS`
settings, which must be set in the process environment: `fastmcp run` applies
`deployment.env` after `fastmcp.settings` is loaded.

OAuthProxy state is persisted through `runtime/storage.py` (`OUBLIAI_STORAGE_URL`,
encrypted with the required `OUBLIAI_STORAGE_ENCRYPTION_KEY`). Background tasks use
FastMCP's `FASTMCP_DOCKET_*` settings.
"""

import json
import os

import fastmcp
from fastmcp import FastMCP

from oubliai_server.auth.provider import build_auth
from oubliai_server.runtime.storage import ENCRYPTION_KEY_ENV, build_client_storage
from oubliai_server.server import build_server
from oubliai_server.spec import load_telnyx_spec

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


def create_server() -> FastMCP:
    env = _require_env()
    _require_host_origin_protection()
    spec = load_telnyx_spec()
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


def main() -> None:
    create_server().run(transport="http")


if __name__ == "__main__":
    main()
