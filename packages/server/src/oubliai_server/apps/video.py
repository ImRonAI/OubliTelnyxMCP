"""Video workspace: Telnyx Rooms (schema: /rooms, /room_recordings).

No meeting bot inside Rooms; join tokens come from CreateRoomClientToken
(`domains/video/AGENTS.md`).
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
    {"ListRooms", "ViewRoom", "CreateRoom", "DeleteRoom", "CreateRoomClientToken",
     "ListRoomRecordings"}
)
CONFIRMED_ACTIONS = ("DeleteRoom",)


class RoomInput(BaseModel):
    """`CreateRoom` request body (all optional in the schema)."""

    unique_name: str | None = Field(default=None, title="Unique name")
    max_participants: int | None = Field(default=None, title="Max participants")
    enable_recording: bool = Field(default=False, title="Enable recording")
    webhook_event_url: str | None = Field(default=None, title="Webhook event URL")


FORM_MODELS = {"CreateRoom": RoomInput}
COLUMNS = (
    ColumnSpec("unique_name", "Name"),
    ColumnSpec("max_participants", "Max participants"),
    ColumnSpec("enable_recording", "Recording"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-video")

rooms_list = register_list_backend(
    app, name="rooms_list", spec=ListSpec(tool="ListRooms", data_path=("data",), columns=COLUMNS)
)
rooms_get = register_detail_backend(app, name="rooms_get", tool="ViewRoom", id_param="room_id")
rooms_create = register_form_backend(app, name="rooms_create", tool="CreateRoom", model=RoomInput)
rooms_delete = register_confirmed_backend(app, name="rooms_delete", tool="DeleteRoom", id_param="room_id")


def _delete_action() -> None:
    confirm_action(
        label="Delete room",
        title="Delete room",
        description="Ends any active session and removes the room.",
        backend=rooms_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Video rooms",
        list_backend=rooms_list,
        columns=COLUMNS,
        detail_backend=rooms_get,
        detail_fields=(("data.id", "ID"), ("data.unique_name", "Name"), ("data.active_session_id", "Active session")),
        create_form=(RoomInput, rooms_create),
        actions=(_delete_action,),
        notes=("Join tokens: CreateRoomClientToken. Recordings: ListRoomRecordings.",),
    )


@app.ui("video_workspace", description="Open the Telnyx video rooms workspace.")
def video_workspace() -> PrefabApp:
    return workspace()
