"""Recipe helpers: FastMCPApp backends that call generated tools, and the shared workspace view."""

import json

import pytest
from fastmcp import Client, FastMCP
from fastmcp.apps.app import FastMCPApp
from fastmcp.exceptions import ToolError
from fastmcp.server.providers.addressing import hashed_backend_name
from prefab_ui.app import PrefabApp
from prefab_ui.rx import STATE
from pydantic import BaseModel

from oubliai_server.apps.recipes import (
    ColumnSpec,
    ListSpec,
    confirm_action,
    list_workspace,
    register_confirmed_backend,
    register_detail_backend,
    register_form_backend,
    register_list_backend,
)


class ThingInput(BaseModel):
    name: str


def _build():
    calls: list[tuple[str, dict]] = []
    ops = FastMCP("ops")

    @ops.tool()
    async def ListThings(page: dict | None = None) -> dict:
        calls.append(("ListThings", {"page": page}))
        return {"data": [{"id": "1", "name": "a"}], "meta": {"total_pages": 1}}

    @ops.tool()
    async def GetThing(id: str) -> dict:
        calls.append(("GetThing", {"id": id}))
        return {"data": {"id": id, "name": "a"}}

    @ops.tool()
    async def CreateThing(name: str) -> dict:
        calls.append(("CreateThing", {"name": name}))
        return {"data": {"id": "2", "name": name}}

    @ops.tool()
    async def DeleteThing(id: str) -> dict:
        calls.append(("DeleteThing", {"id": id}))
        return {}

    app = FastMCPApp("recipe-test")
    spec = ListSpec(
        tool="ListThings",
        data_path=("data",),
        columns=(ColumnSpec(key="id", header="ID"), ColumnSpec(key="name", header="Name")),
    )
    things_list = register_list_backend(app, name="things_list", spec=spec)
    things_get = register_detail_backend(app, name="things_get", tool="GetThing", id_param="id")
    things_create = register_form_backend(
        app, name="things_create", tool="CreateThing", model=ThingInput
    )
    things_delete = register_confirmed_backend(
        app, name="things_delete", tool="DeleteThing", id_param="id"
    )
    ops.add_provider(app)
    root = FastMCP("root")
    root.mount(ops)
    backends = {
        "list": things_list,
        "get": things_get,
        "create": things_create,
        "delete": things_delete,
    }
    return root, app, spec, backends, calls


async def test_backends_are_app_only_tools():
    _, app, _, _, _ = _build()
    tools = {tool.name: tool for tool in await app.list_tools()}
    assert set(tools) == {"things_list", "things_get", "things_create", "things_delete"}
    for tool in tools.values():
        assert tool.meta["ui"]["visibility"] == ["app"]


async def test_list_backend_calls_generated_tool_with_page_args():
    root, app, _, _, calls = _build()
    async with Client(root) as client:
        result = await client.call_tool(hashed_backend_name(app.name, "things_list"), {})
    assert result.structured_content == {
        "rows": [{"id": "1", "name": "a"}],
        "meta": {"total_pages": 1},
    }
    assert calls == [("ListThings", {"page": {"number": 1, "size": 25}})]


async def test_detail_and_form_backends_forward_arguments():
    root, app, _, _, calls = _build()
    async with Client(root) as client:
        detail = await client.call_tool(
            hashed_backend_name(app.name, "things_get"), {"resource_id": "7"}
        )
        created = await client.call_tool(
            hashed_backend_name(app.name, "things_create"), {"data": {"name": "new"}}
        )
    assert detail.structured_content == {"data": {"id": "7", "name": "a"}}
    assert created.structured_content == {"data": {"id": "2", "name": "new"}}
    assert ("GetThing", {"id": "7"}) in calls
    assert ("CreateThing", {"name": "new"}) in calls


async def test_confirmed_backend_requires_matching_confirmation():
    root, app, _, _, calls = _build()
    name = hashed_backend_name(app.name, "things_delete")
    async with Client(root) as client:
        with pytest.raises(ToolError, match="Confirmation does not match"):
            await client.call_tool(name, {"resource_id": "9", "confirm": "nope"})
        assert ("DeleteThing", {"id": "9"}) not in calls
        await client.call_tool(name, {"resource_id": "9", "confirm": "9"})
    assert ("DeleteThing", {"id": "9"}) in calls


def test_list_workspace_builds_prefab_app_wired_to_backends():
    _, _, spec, backends, _ = _build()

    def delete_action() -> None:
        confirm_action(
            label="Delete",
            title="Delete thing",
            description="Removes the thing.",
            backend=backends["delete"],
            resource_id_rx=STATE.selected.id,
        )

    view = list_workspace(
        title="Things",
        list_backend=backends["list"],
        columns=spec.columns,
        detail_backend=backends["get"],
        detail_fields=(("id", "ID"), ("name", "Name")),
        create_form=(ThingInput, backends["create"]),
        actions=(delete_action,),
        notes=("Test note",),
    )
    assert isinstance(view, PrefabApp)
    payload = view.to_json()
    assert payload["$prefab"] == {"version": "0.3"}
    text = json.dumps(payload)
    assert '"type": "DataTable"' in text
    assert '"paginated": false' in text
    assert '"type": "Dialog"' in text
    assert '"type": "Form"' in text
    assert "Test note" in text
    on_mount = payload["view"]["onMount"]
    assert on_mount["action"] == "toolCall"
    assert on_mount["tool"].endswith("things_list")
    assert payload["state"]["rows"] == []
