"""App-only backend tools that execute generated Telnyx tools through FastMCP.

Each helper registers a `@app.tool()` (visibility `["app"]`) on a `FastMCPApp`. The body
does exactly one thing: `await ctx.fastmcp.call_tool(<generated tool name>, args)`, so the
OpenAPI-generated catalog remains the only execution path and the caller's token reaches
Telnyx through the shared client. Nothing here speaks HTTP.
"""

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from fastmcp import Context
from fastmcp.apps.app import FastMCPApp
from fastmcp.exceptions import ToolError
from fastmcp.tools import ToolResult
from pydantic import BaseModel

Paging = Literal["page", "cursor", "none"]
Backend = Callable[..., Any]
Payload = dict[str, Any]


@dataclass(frozen=True)
class ColumnSpec:
    """One DataTable column bound to a field of the listed resource."""

    key: str
    header: str
    format: str | None = None


@dataclass(frozen=True)
class ListSpec:
    """How a workspace lists its primary resource through a generated tool."""

    tool: str
    data_path: tuple[str, ...]
    columns: tuple[ColumnSpec, ...]
    paging: Paging = "page"
    static_args: Mapping[str, Any] = field(default_factory=dict)


def _payload(result: ToolResult) -> Payload:
    if result.structured_content is not None:
        return dict(result.structured_content)
    if result.content:
        first = result.content[0]
        text = getattr(first, "text", None)
        if text:
            loaded = json.loads(text)
            if isinstance(loaded, dict):
                return loaded
            return {"result": loaded}
    return {}


def _register(app: FastMCPApp, fn: Backend, *, name: str, description: str) -> Backend:
    """Register `fn` under `name`; `CallTool(fn)` resolves through `fn.__name__`, so align it."""
    fn.__name__ = name
    fn.__qualname__ = name
    return app.tool(fn, name=name, description=description)


def _walk(payload: Payload, path: tuple[str, ...]) -> Any:
    node: Any = payload
    for part in path:
        if not isinstance(node, dict):
            return []
        node = node.get(part)
    return node if node is not None else []


async def _page_args(ctx: Context, tool: str, number: int, size: int) -> dict[str, Any]:
    """Page arguments in the exact shape the generated tool declares.

    FastMCP's OpenAPI provider exposes a `page` deepObject parameter as one `page` object,
    but operations that declare literal `page[number]`/`page[size]` query names keep those
    flat names. Read the tool's own input schema instead of assuming one shape.
    """
    generated = await ctx.fastmcp.get_tool(tool)
    properties = generated.parameters.get("properties", {}) if generated else {}
    if "page[number]" in properties or "page[size]" in properties:
        return {"page[number]": number, "page[size]": size}
    return {"page": {"number": number, "size": size}}


def register_list_backend(app: FastMCPApp, *, name: str, spec: ListSpec) -> Backend:
    """Register a list backend returning `{"rows": [...], "meta": {...}}`."""

    async def _run(ctx: Context, args: dict[str, Any]) -> Payload:
        result = await ctx.fastmcp.call_tool(spec.tool, {**spec.static_args, **args})
        payload = _payload(result)
        return {"rows": _walk(payload, spec.data_path), "meta": payload.get("meta", {})}

    if spec.paging == "page":

        async def list_by_page(ctx: Context, page_number: int = 1, page_size: int = 25) -> dict:
            return await _run(ctx, await _page_args(ctx, spec.tool, page_number, page_size))

        return _register(app, list_by_page, name=name, description=f"List via {spec.tool}")

    if spec.paging == "cursor":

        async def list_by_cursor(ctx: Context, cursor: str | None = None, limit: int = 25) -> dict:
            args: dict[str, Any] = {"limit": limit}
            if cursor:
                args["cursor"] = cursor
            return await _run(ctx, args)

        return _register(app, list_by_cursor, name=name, description=f"List via {spec.tool}")

    async def list_all(ctx: Context) -> dict:
        return await _run(ctx, {})

    return _register(app, list_all, name=name, description=f"List via {spec.tool}")


def register_detail_backend(app: FastMCPApp, *, name: str, tool: str, id_param: str) -> Backend:
    """Register a detail backend: `resource_id` -> generated retrieve tool."""

    async def detail(ctx: Context, resource_id: str) -> dict:
        return _payload(await ctx.fastmcp.call_tool(tool, {id_param: resource_id}))

    return _register(app, detail, name=name, description=f"Retrieve via {tool}")


def register_form_backend(
    app: FastMCPApp, *, name: str, tool: str, model: type[BaseModel]
) -> Backend:
    """Register a create backend fed by `Form.from_model(model)` (`arguments={"data": ...}`)."""

    async def create(ctx: Context, data: BaseModel) -> dict:
        return _payload(await ctx.fastmcp.call_tool(tool, data.model_dump(exclude_none=True)))

    # FastMCP builds the input schema from the annotations; bind the concrete form model so
    # `Form.from_model(model)` submissions (`arguments={"data": {...}}`) validate against it.
    create.__annotations__["data"] = model

    return _register(app, create, name=name, description=f"Create via {tool}")


def register_confirmed_backend(
    app: FastMCPApp,
    *,
    name: str,
    tool: str,
    id_param: str,
    extra_args: Mapping[str, Any] | None = None,
) -> Backend:
    """Register a destructive/cost action that runs only when `confirm == resource_id`."""
    extras = dict(extra_args or {})

    async def confirmed(ctx: Context, resource_id: str, confirm: str) -> dict:
        if confirm != resource_id:
            raise ToolError(
                f"Confirmation does not match: type the resource id {resource_id!r} to run {tool}."
            )
        return _payload(await ctx.fastmcp.call_tool(tool, {id_param: resource_id, **extras}))

    return _register(app, confirmed, name=name, description=f"Confirmed {tool}")
