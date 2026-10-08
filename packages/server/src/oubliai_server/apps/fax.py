"""Fax workspace: faxes and fax applications (schema: /faxes, /fax_applications).

Refresh/cancel/delete are explicit confirmed actions; SendFax is a live send and only
the JSON variant is form-backed (`domains/fax/AGENTS.md`).
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
    {"ListFaxes", "ViewFax", "DeleteFax", "CancelFax", "RefreshFax", "SendFax",
     "ListFaxApplications", "CreateFaxApplication"}
)
CONFIRMED_ACTIONS = ("DeleteFax", "CancelFax")


class FaxApplicationInput(BaseModel):
    """`CreateFaxApplication` scalar fields."""

    application_name: str = Field(title="Application name")
    webhook_event_url: str = Field(title="Webhook event URL")
    webhook_event_failover_url: str | None = Field(default=None, title="Webhook failover URL")
    active: bool = Field(default=True, title="Active")


FORM_MODELS = {"CreateFaxApplication": FaxApplicationInput}
COLUMNS = (
    ColumnSpec("direction", "Direction"),
    ColumnSpec("from", "From"),
    ColumnSpec("to", "To"),
    ColumnSpec("status", "Status"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-fax")

faxes_list = register_list_backend(
    app, name="faxes_list", spec=ListSpec(tool="ListFaxes", data_path=("data",), columns=COLUMNS)
)
faxes_get = register_detail_backend(app, name="faxes_get", tool="ViewFax", id_param="id")
faxes_delete = register_confirmed_backend(app, name="faxes_delete", tool="DeleteFax", id_param="id")
faxes_cancel = register_confirmed_backend(app, name="faxes_cancel", tool="CancelFax", id_param="id")
fax_apps_create = register_form_backend(
    app, name="fax_applications_create", tool="CreateFaxApplication", model=FaxApplicationInput
)


def _cancel_action() -> None:
    confirm_action(
        label="Cancel fax",
        title="Cancel outbound fax",
        description="Stops a queued or in-progress fax.",
        backend=faxes_cancel,
        resource_id_rx=STATE.selected.data.id,
    )


def _delete_action() -> None:
    confirm_action(
        label="Delete fax",
        title="Delete fax record",
        description="Removes the fax record and its stored media.",
        backend=faxes_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Faxes",
        list_backend=faxes_list,
        columns=COLUMNS,
        detail_backend=faxes_get,
        detail_fields=(("data.id", "ID"), ("data.status", "Status"), ("data.media_url", "Media URL")),
        create_form=(FaxApplicationInput, fax_apps_create),
        actions=(_cancel_action, _delete_action),
        notes=(
            "SendFax is a live send (JSON body: connection_id, from, to, media_url); run it explicitly "
            "through execute. Multipart upload is not form-backed.",
            "RefreshFax re-fetches status only; status is not proof of delivery.",
        ),
    )


@app.ui("fax_workspace", description="Open the Telnyx fax workspace.")
def fax_workspace() -> PrefabApp:
    return workspace()
