"""Loading of the canonical Telnyx OpenAPI schema."""

import json
import os
from pathlib import Path
from typing import Any

# packages/server/src/oubliai_server/spec.py -> repository root
_REPO_ROOT = Path(__file__).resolve().parents[4]
CANONICAL_SPEC_PATH = _REPO_ROOT / "docs" / "reference" / "telnyx" / "openapi.json"
# RFC 8414 metadata served at https://api.telnyx.com/.well-known/oauth-authorization-server.
# Used ONLY for `scopes_supported`: live Telnyx rejects the schema's single `admin` scope
# (POST /v2/oauth_clients -> 422, 2026-10-08) and accepts these 32 instead.
OAUTH_AS_METADATA_PATH = _REPO_ROOT / "docs" / "reference" / "telnyx" / "oauth-authorization-server.json"
SPEC_PATH_ENV = "OUBLIAI_TELNYX_OPENAPI"


def load_telnyx_spec(path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    """Read the Telnyx schema from `path`, `$OUBLIAI_TELNYX_OPENAPI`, or the canonical copy."""
    resolved = Path(path or os.environ.get(SPEC_PATH_ENV) or CANONICAL_SPEC_PATH)
    with resolved.open(encoding="utf-8") as handle:
        return json.load(handle)


def default_base_url(spec: dict[str, Any]) -> str:
    """Return the schema's first declared server URL."""
    return spec["servers"][0]["url"]


_HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
INTROSPECTION_OPERATION_ID = "IntrospectOAuthToken"
OAUTH_SECURITY_SCHEME = "oauthClientAuth"


def _operations(spec: dict[str, Any]):
    for path, item in spec["paths"].items():
        for method, operation in item.items():
            if method in _HTTP_METHODS and isinstance(operation, dict):
                yield method.upper(), path, operation


def oauth_scopes() -> list[str]:
    """Scopes Telnyx's authorization server actually accepts (`scopes_supported`)."""
    with OAUTH_AS_METADATA_PATH.open(encoding="utf-8") as handle:
        return list(json.load(handle)["scopes_supported"])


def oauth_endpoints(spec: dict[str, Any]) -> dict[str, Any]:
    """OAuth URLs from the schema's `oauthClientAuth` scheme and introspection operation;
    scopes from Telnyx's authorization-server metadata (see `OAUTH_AS_METADATA_PATH`)."""
    flow = spec["components"]["securitySchemes"][OAUTH_SECURITY_SCHEME]["flows"][
        "authorizationCode"
    ]
    introspection_path = next(
        path
        for _, path, operation in _operations(spec)
        if operation.get("operationId") == INTROSPECTION_OPERATION_ID
    )
    return {
        "authorization_url": flow["authorizationUrl"],
        "token_url": flow["tokenUrl"],
        "introspection_url": default_base_url(spec) + introspection_path,
        "scopes": oauth_scopes(),
    }


def foreign_server_routes(spec: dict[str, Any]) -> frozenset[tuple[str, str]]:
    """`(METHOD, path)` of operations whose own `servers` differ from the schema's first server.

    FastMCP's OpenAPIProvider sends every call to `servers[0]`, so these operations would
    reach the wrong host.
    """
    base_url = default_base_url(spec)
    return frozenset(
        (method, path)
        for method, path, operation in _operations(spec)
        if any(server.get("url") != base_url for server in operation.get("servers", []))
    )


# FastMCP's documented default component name: "the operationId ..., up to the first
# double underscore (`__`)", "limited to 56 characters" (openapi-integration.md).
_FASTMCP_NAME_MAX = 56


def collision_names(spec: dict[str, Any]) -> dict[str, str]:
    """`mcp_names` entries for operations whose default FastMCP names collide.

    Telnyx's FastAPI-style operationIds (e.g. `get_conversations_public__conversation_id__
    insights_get`) shorten to the same default name, and FastMCP would then disambiguate
    by arrival order (`..._2`). Each colliding operation is named by its schema `summary`,
    the field FastMCP itself uses when an operation has no operationId.
    """
    by_default_name: dict[str, list[dict[str, Any]]] = {}
    for _, _, operation in _operations(spec):
        default = operation["operationId"].split("__")[0][:_FASTMCP_NAME_MAX]
        by_default_name.setdefault(default, []).append(operation)
    return {
        operation["operationId"]: operation["summary"]
        for group in by_default_name.values()
        if len(group) > 1
        for operation in group
    }
