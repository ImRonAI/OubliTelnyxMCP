"""Speech workspace: voice designs (schema: /voice_designs; listVoices returns {voices: [...]}).

generateSpeech and voice samples return binary audio and are not table-bound
(`domains/speech/AGENTS.md`).
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
    {"listVoiceDesigns", "getVoiceDesign", "createVoiceDesign", "deleteVoiceDesign",
     "listVoices", "listSttProviders", "generateSpeech"}
)
CONFIRMED_ACTIONS = ("deleteVoiceDesign",)


class VoiceDesignInput(BaseModel):
    """`createVoiceDesign` scalar fields."""

    name: str | None = Field(default=None, title="Name")
    text: str = Field(title="Sample text")
    prompt: str = Field(title="Voice description")
    language: str | None = Field(default=None, title="Language")


FORM_MODELS = {"createVoiceDesign": VoiceDesignInput}
COLUMNS = (
    ColumnSpec("name", "Name"),
    ColumnSpec("provider", "Provider"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-speech")

designs_list = register_list_backend(
    app,
    name="voice_designs_list",
    spec=ListSpec(tool="listVoiceDesigns", data_path=("data",), columns=COLUMNS),
)
designs_get = register_detail_backend(app, name="voice_designs_get", tool="getVoiceDesign", id_param="id")
designs_create = register_form_backend(
    app, name="voice_designs_create", tool="createVoiceDesign", model=VoiceDesignInput
)
designs_delete = register_confirmed_backend(
    app, name="voice_designs_delete", tool="deleteVoiceDesign", id_param="id"
)
voices_list = register_list_backend(
    app,
    name="voices_list",
    spec=ListSpec(tool="listVoices", data_path=("voices",), columns=(), paging="none"),
)


def _delete_action() -> None:
    confirm_action(
        label="Delete voice design",
        title="Delete voice design",
        description="Removes the design and its generated samples.",
        backend=designs_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Voice designs",
        list_backend=designs_list,
        columns=COLUMNS,
        detail_backend=designs_get,
        detail_fields=(("data.id", "ID"), ("data.name", "Name"), ("data.provider", "Provider")),
        create_form=(VoiceDesignInput, designs_create),
        actions=(_delete_action,),
        notes=(
            "Catalog voices: listVoices (voices array); STT providers: listSttProviders.",
            "generateSpeech and voice samples return binary audio; fetch them through execute.",
        ),
    )


@app.ui("speech_workspace", description="Open the Telnyx speech workspace.")
def speech_workspace() -> PrefabApp:
    return workspace()
