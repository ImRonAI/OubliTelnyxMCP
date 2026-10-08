"""Voice workspace: Call Control applications and connections (schema: /call_control_applications, /connections, /calls).

DialCall, HangupCall and the other call commands are live actions; command acceptance is
not audible execution (`domains/voice/AGENTS.md`).
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
    {"ListCallControlApplications", "RetrieveCallControlApplication",
     "CreateCallControlApplication", "DeleteCallControlApplication", "ListConnections",
     "DialCall", "RetrieveCallStatus", "HangupCall"}
)
CONFIRMED_ACTIONS = ("DeleteCallControlApplication",)


class CallControlApplicationInput(BaseModel):
    """`CreateCallControlApplication` scalar fields."""

    application_name: str = Field(title="Application name")
    webhook_event_url: str = Field(title="Webhook event URL")
    webhook_event_failover_url: str | None = Field(default=None, title="Webhook failover URL")
    active: bool = Field(default=True, title="Active")


FORM_MODELS = {"CreateCallControlApplication": CallControlApplicationInput}
COLUMNS = (
    ColumnSpec("application_name", "Application"),
    ColumnSpec("active", "Active"),
    ColumnSpec("webhook_api_version", "Webhook API"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-voice")

apps_list = register_list_backend(
    app,
    name="call_control_applications_list",
    spec=ListSpec(tool="ListCallControlApplications", data_path=("data",), columns=COLUMNS),
)
apps_get = register_detail_backend(
    app, name="call_control_applications_get", tool="RetrieveCallControlApplication", id_param="id"
)
apps_create = register_form_backend(
    app,
    name="call_control_applications_create",
    tool="CreateCallControlApplication",
    model=CallControlApplicationInput,
)
apps_delete = register_confirmed_backend(
    app, name="call_control_applications_delete", tool="DeleteCallControlApplication", id_param="id"
)


def _delete_action() -> None:
    confirm_action(
        label="Delete application",
        title="Delete Call Control application",
        description="Numbers routed to this application lose their voice routing.",
        backend=apps_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Call Control applications",
        list_backend=apps_list,
        columns=COLUMNS,
        detail_backend=apps_get,
        detail_fields=(("data.id", "ID"), ("data.application_name", "Name"), ("data.webhook_event_url", "Webhook")),
        create_form=(CallControlApplicationInput, apps_create),
        actions=(_delete_action,),
        notes=(
            "Calls: DialCall (connection_id, to, from) is a live action; RetrieveCallStatus and "
            "HangupCall take the call_control_id. Run them explicitly through execute.",
        ),
    )


@app.ui("voice_workspace", description="Open the Telnyx voice workspace.")
def voice_workspace() -> PrefabApp:
    return workspace()
