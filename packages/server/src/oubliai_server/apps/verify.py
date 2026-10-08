"""Verify workspace: verify profiles and verifications (schema: /verify_profiles, /verifications).

Only the documented OTP transports exist as generated tools; a verification's provider
status decides validity (`domains/verify/AGENTS.md`).
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
    {"ListProfiles", "GetVerifyProfile", "CreateVerifyProfile", "DeleteProfile",
     "CreateVerificationSms", "RetrieveVerification", "VerifyVerificationCodeById"}
)
CONFIRMED_ACTIONS = ("DeleteProfile",)


class VerifyProfileInput(BaseModel):
    """`CreateVerifyProfile` scalar fields (channel objects sms/call/... via execute)."""

    name: str = Field(title="Profile name")
    language: str | None = Field(default=None, title="Language")
    webhook_url: str | None = Field(default=None, title="Webhook URL")
    webhook_failover_url: str | None = Field(default=None, title="Webhook failover URL")


FORM_MODELS = {"CreateVerifyProfile": VerifyProfileInput}
COLUMNS = (
    ColumnSpec("name", "Name"),
    ColumnSpec("language", "Language"),
    ColumnSpec("webhook_url", "Webhook"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-verify")

profiles_list = register_list_backend(
    app, name="verify_profiles_list", spec=ListSpec(tool="ListProfiles", data_path=("data",), columns=COLUMNS)
)
profiles_get = register_detail_backend(
    app, name="verify_profiles_get", tool="GetVerifyProfile", id_param="verify_profile_id"
)
profiles_create = register_form_backend(
    app, name="verify_profiles_create", tool="CreateVerifyProfile", model=VerifyProfileInput
)
profiles_delete = register_confirmed_backend(
    app, name="verify_profiles_delete", tool="DeleteProfile", id_param="verify_profile_id"
)


def _delete_action() -> None:
    confirm_action(
        label="Delete profile",
        title="Delete verify profile",
        description="Verifications can no longer be created with this profile.",
        backend=profiles_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Verify profiles",
        list_backend=profiles_list,
        columns=COLUMNS,
        detail_backend=profiles_get,
        detail_fields=(("data.id", "ID"), ("data.name", "Name"), ("data.language", "Language")),
        create_form=(VerifyProfileInput, profiles_create),
        actions=(_delete_action,),
        notes=(
            "Sending a code (CreateVerificationSms/Call/Flashcall/Whatsapp) is a live side effect; "
            "run it through execute. Check codes with VerifyVerificationCodeById.",
        ),
    )


@app.ui("verify_workspace", description="Open the Telnyx Verify workspace.")
def verify_workspace() -> PrefabApp:
    return workspace()
