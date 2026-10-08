"""Server composition: OpenAPI operations behind CodeMode, plus native GenerativeUI.

Mirrors the executed fixture in `.omo/ulw-research/build-verdict/probe_server.py`:
CodeMode lives on the mounted operations server, and GenerativeUI is a provider of the
parent so its UI metadata stays directly advertised.
"""

from collections.abc import AsyncIterator
from typing import Any

import httpx2
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
from fastmcp.apps.generative import GenerativeUI
from fastmcp.experimental.transforms.code_mode import CodeMode
from fastmcp.server.providers.openapi import MCPType, OpenAPIProvider, RouteMap
from fastmcp.utilities.openapi import HTTPRoute

from fastmcp_tasks import TasksExtension

from oubliai_server.apps import ALL_APPS
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.runtime.tasks import build_tasks_extension, register_task_tools
from oubliai_server.spec import (
    collision_names,
    default_base_url,
    foreign_server_routes,
    load_telnyx_spec,
)

SERVER_NAME = "Oubliai Telnyx"
DEFAULT_MAX_TOOL_CALLS = 25

# Schema tag on the OAuth handshake operations (authorize, token, introspect, register,
# grants, JWKS, consent). They belong to the auth layer, not to the model's catalog.
OAUTH_PROTOCOL_TAG = "OAuth Protocol"


def build_operations(
    spec: dict[str, Any],
    client: httpx2.AsyncClient,
    *,
    max_tool_calls: int | None = DEFAULT_MAX_TOOL_CALLS,
    mask_error_details: bool | None = None,
) -> FastMCP:
    """Telnyx operations generated from the schema, discoverable only through CodeMode.

    `mask_error_details` must match the parent's: FastMCP warns at mount time otherwise,
    because upstream error details would leak through the mounted child.
    """
    excluded_routes = foreign_server_routes(spec)

    def exclude_foreign_servers(route: HTTPRoute, mcp_type: MCPType) -> MCPType | None:
        if (route.method.upper(), route.path) in excluded_routes:
            return MCPType.EXCLUDE
        return None

    operations = FastMCP("Telnyx operations", mask_error_details=mask_error_details)
    operations.add_provider(
        OpenAPIProvider(
            openapi_spec=spec,
            client=client,
            route_maps=[RouteMap(tags={OAUTH_PROTOCOL_TAG}, mcp_type=MCPType.EXCLUDE)],
            route_map_fn=exclude_foreign_servers,
            mcp_names=collision_names(spec),
            tags={"telnyx"},
        )
    )
    # Domain FastMCPApp providers sit under CodeMode: FastMCP lists app-only tools on
    # tools/list (host-side visibility filtering), but CodeMode's catalog applies
    # `is_model_visible`, so only the workspace entry points reach the model, via search.
    for domain_app in ALL_APPS:
        operations.add_provider(domain_app)
    register_task_tools(operations)
    operations.add_transform(CodeMode(max_tool_calls=max_tool_calls))
    return operations


def build_server(
    spec: dict[str, Any] | None = None,
    *,
    client: httpx2.AsyncClient | None = None,
    tasks: TasksExtension | None = None,
    **fastmcp_kwargs: Any,
) -> FastMCP:
    """Build the model-facing server: `search`, `get_schema`, `execute`, `generate_prefab_ui`.

    `tasks`: `None` builds the `TasksExtension` from `FASTMCP_DOCKET_*`; an instance is used
    as given. FastMCP refuses to start a task-enabled tool without the extension, and it
    lives on the root server only.
    """
    spec = spec if spec is not None else load_telnyx_spec()
    owned_client: httpx2.AsyncClient | None = None
    if client is None:
        # OpenAPIProvider treats an injected client as caller-owned and never closes it, so
        # the server closes the one it created itself (lifespan.md, "Basic Usage").
        client = owned_client = make_telnyx_client(default_base_url(spec))

    @lifespan
    async def close_owned_client(_: FastMCP) -> AsyncIterator[dict[str, Any]]:
        try:
            yield {}
        finally:
            if owned_client is not None:
                await owned_client.aclose()

    server = FastMCP(
        SERVER_NAME,
        providers=[GenerativeUI(include_components_tool=False)],
        lifespan=close_owned_client,
        **fastmcp_kwargs,
    )
    server.add_extension(tasks if tasks is not None else build_tasks_extension())
    server.mount(
        build_operations(spec, client, mask_error_details=fastmcp_kwargs.get("mask_error_details"))
    )
    return server
