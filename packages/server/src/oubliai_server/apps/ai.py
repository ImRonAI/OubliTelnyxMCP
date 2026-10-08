"""AI workspace: assistants (schema: /ai/assistants; list returns {data: [...]} without paging).

Registered names for the FastAPI-style operationIds are FastMCP's defaults
(`get_assistant_public_assistants`, ...) as computed in `spec.collision_names`.
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
    {"get_assistants_public_assistants_get", "create_new_assistant_public_assistants_post",
     "get_assistant_public_assistants__assistant_id__get",
     "delete_assistant_public_assistants__assistant_id__delete",
     "get_conversations_public_conversations_get",
     "get_conversations_public__conversation_id__messages_get"}
)
# Registered MCP names: operationId up to the first `__` (FastMCP default rule).
ASSISTANT_GET = "get_assistant_public_assistants"
ASSISTANT_DELETE = "delete_assistant_public_assistants"
CONFIRMED_ACTIONS = (ASSISTANT_DELETE,)


class AssistantInput(BaseModel):
    """`create_new_assistant_public_assistants_post` scalar fields."""

    name: str = Field(title="Name")
    instructions: str = Field(title="Instructions")
    model: str | None = Field(default=None, title="Model ID")
    description: str | None = Field(default=None, title="Description")
    greeting: str | None = Field(default=None, title="Greeting")


FORM_MODELS = {"create_new_assistant_public_assistants_post": AssistantInput}
COLUMNS = (
    ColumnSpec("name", "Name"),
    ColumnSpec("model", "Model"),
    ColumnSpec("description", "Description"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-ai")

assistants_list = register_list_backend(
    app,
    name="assistants_list",
    spec=ListSpec(
        tool="get_assistants_public_assistants_get", data_path=("data",), columns=COLUMNS, paging="none"
    ),
)
assistants_get = register_detail_backend(
    app, name="assistants_get", tool=ASSISTANT_GET, id_param="assistant_id"
)
assistants_create = register_form_backend(
    app, name="assistants_create", tool="create_new_assistant_public_assistants_post", model=AssistantInput
)
assistants_delete = register_confirmed_backend(
    app, name="assistants_delete", tool=ASSISTANT_DELETE, id_param="assistant_id"
)


def _delete_action() -> None:
    confirm_action(
        label="Delete assistant",
        title="Delete assistant",
        description="Removes the assistant and its versions.",
        backend=assistants_delete,
        resource_id_rx=STATE.selected.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="AI assistants",
        list_backend=assistants_list,
        columns=COLUMNS,
        detail_backend=assistants_get,
        detail_fields=(("id", "ID"), ("name", "Name"), ("model", "Model")),
        create_form=(AssistantInput, assistants_create),
        actions=(_delete_action,),
        paging="none",
        notes=(
            "Assistant retrieve/create return the bare object (no data envelope).",
            "Conversations: get_conversations_public_conversations_get; messages via the tool "
            "registered as Get_conversation_messages (schema summary, collision override).",
        ),
    )


@app.ui("ai_workspace", description="Open the Telnyx AI assistants workspace.")
def ai_workspace() -> PrefabApp:
    return workspace()
