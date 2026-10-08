"""Messaging workspace: messaging profiles and outbound messages (schema: /messaging_profiles, /messages).

SMS/MMS, WhatsApp and RCS share navigation only; each channel keeps its own generated
tool and IDs (`domains/messaging/AGENTS.md`). Sending is an explicit confirmed action.
"""

from fastmcp.apps.app import FastMCPApp
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
    register_list_backend,
)

GENERATED_TOOLS = frozenset(
    {"ListMessagingProfiles", "RetrieveMessagingProfile", "CreateMessagingProfile",
     "DeleteMessagingProfile", "SendMessage", "GetMessage"}
)
CONFIRMED_ACTIONS = ("DeleteMessagingProfile",)


# `CreateMessagingProfile` requires `whitelisted_destinations` (array); Prefab's
# `Form.from_model` skips list fields, so no form can satisfy the schema. Creation stays an
# explicit `execute` call with the generated tool.
FORM_MODELS: dict[str, type[BaseModel]] = {}
COLUMNS = (
    ColumnSpec("name", "Name"),
    ColumnSpec("enabled", "Enabled"),
    ColumnSpec("webhook_url", "Webhook"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-messaging")

profiles_list = register_list_backend(
    app,
    name="messaging_profiles_list",
    spec=ListSpec(tool="ListMessagingProfiles", data_path=("data",), columns=COLUMNS),
)
profiles_get = register_detail_backend(
    app, name="messaging_profiles_get", tool="RetrieveMessagingProfile", id_param="id"
)
profiles_delete = register_confirmed_backend(
    app, name="messaging_profiles_delete", tool="DeleteMessagingProfile", id_param="id"
)


def _delete_action() -> None:
    confirm_action(
        label="Delete profile",
        title="Delete messaging profile",
        description="Numbers assigned to this profile stop sending through it.",
        backend=profiles_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Messaging profiles",
        list_backend=profiles_list,
        columns=COLUMNS,
        detail_backend=profiles_get,
        detail_fields=(("data.id", "ID"), ("data.name", "Name"), ("data.webhook_url", "Webhook")),
        actions=(_delete_action,),
        notes=(
            "CreateMessagingProfile requires whitelisted_destinations (ISO country codes list); "
            "run it through execute.",
            "The schema has no list-messages operation; use GetMessage by id.",
            "Sending (SendMessage, SendWhatsappMessage, SendRCSMessage) is a live side effect: run it "
            "explicitly through execute with the exact channel tool.",
        ),
    )


@app.ui("messaging_workspace", description="Open the Telnyx messaging profiles workspace.")
def messaging_workspace() -> PrefabApp:
    return workspace()
