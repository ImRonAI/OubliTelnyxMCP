"""Storage workspace: KV namespaces (schema: /storage/kvs) with SQL databases alongside.

Key values are octet-stream (PutKvKey/GetKvKey) and not table-bound; KV is not
transactional (`domains/storage/AGENTS.md`).
"""

from fastmcp.apps.app import FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.rx import STATE
from pydantic import BaseModel, Field

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

GENERATED_TOOLS = frozenset(
    {"ListKvNamespaces", "GetKvNamespace", "CreateKvNamespace", "DeleteKvNamespace",
     "ListKvKeys", "GetKvKey", "PutKvKey", "DeleteKvKey", "ListSqlDatabases",
     "CreateSqlDatabase", "DeleteSqlDatabase"}
)
CONFIRMED_ACTIONS = ("DeleteKvNamespace",)


class KvNamespaceInput(BaseModel):
    """`CreateKvNamespace` request body."""

    name: str = Field(title="Namespace name (lowercase letters, digits, hyphens)")


FORM_MODELS = {"CreateKvNamespace": KvNamespaceInput}
COLUMNS = (
    ColumnSpec("name", "Name"),
    ColumnSpec("status", "Status"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-storage")

namespaces_list = register_list_backend(
    app,
    name="kv_namespaces_list",
    spec=ListSpec(tool="ListKvNamespaces", data_path=("data",), columns=COLUMNS),
)
namespaces_get = register_detail_backend(
    app, name="kv_namespaces_get", tool="GetKvNamespace", id_param="id"
)
namespaces_create = register_form_backend(
    app, name="kv_namespaces_create", tool="CreateKvNamespace", model=KvNamespaceInput
)
namespaces_delete = register_confirmed_backend(
    app, name="kv_namespaces_delete", tool="DeleteKvNamespace", id_param="id"
)
keys_list = register_list_backend(
    app,
    name="kv_keys_list",
    spec=ListSpec(tool="ListKvKeys", data_path=("data",), columns=(), paging="none"),
)


def _delete_action() -> None:
    confirm_action(
        label="Delete namespace",
        title="Delete KV namespace",
        description="Deletes every key in the namespace. Status moves to deleting.",
        backend=namespaces_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="KV namespaces",
        list_backend=namespaces_list,
        columns=COLUMNS,
        detail_backend=namespaces_get,
        detail_fields=(("data.id", "ID"), ("data.name", "Name"), ("data.status", "Status")),
        create_form=(KvNamespaceInput, namespaces_create),
        actions=(_delete_action,),
        notes=(
            "A namespace is usable once status is provision_ok (poll with await_telnyx_resource).",
            "Keys: ListKvKeys(id, prefix, cursor); values via PutKvKey/GetKvKey/DeleteKvKey (octet-stream).",
            "SQL: ListSqlDatabases, CreateSqlDatabase, DeleteSqlDatabase.",
        ),
    )


@app.ui("storage_workspace", description="Open the Telnyx storage (KV) workspace.")
def storage_workspace() -> PrefabApp:
    return workspace()
