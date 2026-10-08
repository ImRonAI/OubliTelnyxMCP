from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from fastmcp.client.client import CallToolResult
from mcp.types import BlobResourceContents, Resource, TextResourceContents

from oubliai_client.connection import OubliaiConnection

# Installed prefab-ui 0.20.2 defines these values in
# `.venv/lib/python3.12/site-packages/prefab_ui/generative.py:43-44`; FastMCP's
# GenerativeUI provider registers them at `fastmcp/apps/generative.py:151-157`.
RENDERER_URI = "ui://prefab/generative.html"
RENDERER_MIME = "text/html;profile=mcp-app"


@dataclass(frozen=True)
class RendererResource:
    uri: str
    mime_type: str
    html: str
    meta: Mapping[str, Any] | None

    @property
    def csp(self) -> Mapping[str, Any] | None:
        ui = self._ui_meta
        csp = ui.get("csp") if ui is not None else None
        return csp if isinstance(csp, Mapping) else None

    @property
    def permissions(self) -> Mapping[str, Any] | None:
        ui = self._ui_meta
        permissions = ui.get("permissions") if ui is not None else None
        return permissions if isinstance(permissions, Mapping) else None

    @property
    def _ui_meta(self) -> Mapping[str, Any] | None:
        if self.meta is None:
            return None
        ui = self.meta.get("ui")
        return ui if isinstance(ui, Mapping) else None


def _renderer_resource_from_contents(
    contents: Sequence[TextResourceContents | BlobResourceContents],
) -> RendererResource:
    if len(contents) != 1 or not isinstance(contents[0], TextResourceContents):
        raise ValueError("renderer resource must contain exactly one text item")
    content = contents[0]
    if content.mime_type != RENDERER_MIME:
        raise ValueError(
            f"renderer MIME must be {RENDERER_MIME!r}, got {content.mime_type!r}"
        )
    return RendererResource(
        uri=str(content.uri),
        mime_type=content.mime_type,
        html=content.text,
        # GenerativeUI writes AppConfig at meta["ui"] in
        # `fastmcp/apps/generative.py:151-157`.
        meta=content.meta,
    )


async def find_renderer_resource(connection: OubliaiConnection) -> Resource:
    for resource in await connection.list_resources():
        if str(resource.uri) == RENDERER_URI:
            return resource
    raise LookupError(f"renderer resource not found: {RENDERER_URI}")


async def read_renderer_resource(connection: OubliaiConnection) -> RendererResource:
    contents = await connection.read_resource(RENDERER_URI)
    return _renderer_resource_from_contents(contents)


async def generate_ui(connection: OubliaiConnection, code: str) -> CallToolResult:
    return await connection.call_tool("generate_prefab_ui", {"code": code})
