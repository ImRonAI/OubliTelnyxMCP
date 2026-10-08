"""Every domain workspace: shape, visibility, confirm gating, and schema-bound form models."""

import json

import pytest
from fastmcp.apps.app import FastMCPApp
from prefab_ui.app import PrefabApp

from oubliai_server.apps import ALL_APPS
from oubliai_server.spec import _operations

EXPECTED_APP_NAMES = {
    "oubliai-numbers",
    "oubliai-messaging",
    "oubliai-fax",
    "oubliai-verify",
    "oubliai-video",
    "oubliai-meetings",
    "oubliai-email",
    "oubliai-voice",
    "oubliai-ai",
    "oubliai-rag",
    "oubliai-speech",
    "oubliai-storage",
    "oubliai-training",
    "oubliai-platform",
}


def _module(app: FastMCPApp):
    import importlib

    return importlib.import_module(f"oubliai_server.apps.{app.name.removeprefix('oubliai-')}")


def _request_body_schema(spec, operation_id: str) -> dict:
    def deref(node):
        while isinstance(node, dict) and "$ref" in node:
            node = spec["components"]["schemas"][node["$ref"].split("/")[-1]]
        return node

    for _, _, operation in _operations(spec):
        if operation.get("operationId") != operation_id:
            continue
        content = operation["requestBody"]["content"]
        schema = deref(next(iter(content.values()))["schema"])
        properties: dict = {}
        required: list[str] = []
        for part in schema.get("allOf", [schema]):
            part = deref(part)
            properties.update(part.get("properties", {}))
            required += part.get("required", [])
        return {"properties": properties, "required": required}
    raise AssertionError(f"{operation_id} not in schema")


def test_all_fourteen_domain_apps_are_registered():
    assert {app.name for app in ALL_APPS} == EXPECTED_APP_NAMES
    assert len({app.name for app in ALL_APPS}) == len(ALL_APPS)


@pytest.mark.parametrize("app", ALL_APPS, ids=lambda app: app.name)
async def test_workspace_entry_is_the_only_model_visible_tool(app):
    tools = await app.list_tools()
    entries = [t for t in tools if t.meta["ui"]["visibility"] == ["model"]]
    backends = [t for t in tools if t.meta["ui"]["visibility"] == ["app"]]
    assert [t.name for t in entries] == [f"{app.name.removeprefix('oubliai-')}_workspace"]
    assert backends, "every workspace needs at least one app-only backend"


@pytest.mark.parametrize("app", ALL_APPS, ids=lambda app: app.name)
def test_generated_tools_constant_covers_schema_operations(app, telnyx_spec):
    module = _module(app)
    operation_ids = {op["operationId"] for _, _, op in _operations(telnyx_spec)}
    unknown = set(module.GENERATED_TOOLS) - operation_ids
    assert unknown == set(), f"{app.name} references tools absent from the schema: {unknown}"


@pytest.mark.parametrize("app", ALL_APPS, ids=lambda app: app.name)
def test_form_models_only_use_schema_request_fields(app, telnyx_spec):
    module = _module(app)
    for operation_id, model in module.FORM_MODELS.items():
        body = _request_body_schema(telnyx_spec, operation_id)
        fields = set(model.model_fields)
        assert fields <= set(body["properties"]), (operation_id, fields - set(body["properties"]))
        # A form that cannot supply a required field can never succeed against the schema.
        missing_required = set(body["required"]) - fields
        assert missing_required == set(), (operation_id, missing_required)


@pytest.mark.parametrize("app", ALL_APPS, ids=lambda app: app.name)
async def test_workspace_renders_with_dialog_gated_actions(app):
    entry = next(t for t in await app.list_tools() if t.meta["ui"]["visibility"] == ["model"])
    result = await entry.run({})
    payload = result.structured_content
    assert payload["$prefab"] == {"version": "0.3"}
    text = json.dumps(payload)
    assert '"type": "DataTable"' in text
    assert payload["view"]["onMount"]["action"] == "toolCall"
    module = _module(app)
    if module.CONFIRMED_ACTIONS:
        assert '"type": "Dialog"' in text
    # Destructive/cost tools must never be reachable from onMount or a row click.
    for tool_name in module.CONFIRMED_ACTIONS:
        assert tool_name not in json.dumps(payload["view"]["onMount"])


def test_entry_returns_prefab_app_type():
    for app in ALL_APPS:
        fn = _module(app).workspace
        assert isinstance(fn(), PrefabApp)
