"""Meetings workspace: Meeting Bot sessions (schema: /meeting_sessions).

listMeetingSessions has no pagination. Stop (deleteMeetingSession) and delete recording
media are different confirmed actions (`domains/meetings/AGENTS.md`).
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
    {"listMeetingSessions", "retrieveMeetingSession", "createMeetingSession",
     "deleteMeetingSession", "deleteMeetingSessionRecordingMedia",
     "listMeetingSessionTranscript", "listMeetingSessionEvents"}
)
CONFIRMED_ACTIONS = ("deleteMeetingSession", "deleteMeetingSessionRecordingMedia")


class MeetingSessionInput(BaseModel):
    """`createMeetingSession` scalar fields."""

    meeting_url: str = Field(title="Meeting URL")
    bot_name: str | None = Field(default=None, title="Bot name")
    join_at: str | None = Field(default=None, title="Join at (ISO-8601)")
    speak_on_enter: str | None = Field(default=None, title="Speak on enter")
    chat_on_enter: str | None = Field(default=None, title="Chat on enter")
    summarize_on_end: bool = Field(default=False, title="Summarize on end")


FORM_MODELS = {"createMeetingSession": MeetingSessionInput}
COLUMNS = (
    ColumnSpec("platform", "Platform"),
    ColumnSpec("status", "Status"),
    ColumnSpec("bot_name", "Bot"),
    ColumnSpec("meeting_url", "Meeting URL"),
)

app = FastMCPApp("oubliai-meetings")

sessions_list = register_list_backend(
    app,
    name="meeting_sessions_list",
    spec=ListSpec(tool="listMeetingSessions", data_path=("data",), columns=COLUMNS, paging="none"),
)
sessions_get = register_detail_backend(
    app, name="meeting_sessions_get", tool="retrieveMeetingSession", id_param="id"
)
sessions_create = register_form_backend(
    app, name="meeting_sessions_create", tool="createMeetingSession", model=MeetingSessionInput
)
sessions_stop = register_confirmed_backend(
    app, name="meeting_sessions_stop", tool="deleteMeetingSession", id_param="id"
)
media_delete = register_confirmed_backend(
    app, name="meeting_sessions_delete_media", tool="deleteMeetingSessionRecordingMedia", id_param="id"
)


def _stop_action() -> None:
    confirm_action(
        label="Stop session",
        title="Stop meeting session",
        description="The bot leaves the meeting; the session record is kept.",
        backend=sessions_stop,
        resource_id_rx=STATE.selected.data.id,
    )


def _delete_media_action() -> None:
    confirm_action(
        label="Delete recording media",
        title="Delete recording media",
        description="Deletes stored recording media for this session.",
        backend=media_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Meeting sessions",
        list_backend=sessions_list,
        columns=COLUMNS,
        detail_backend=sessions_get,
        detail_fields=(("data.id", "ID"), ("data.status", "Status"), ("data.status_detail", "Detail")),
        create_form=(MeetingSessionInput, sessions_create),
        actions=(_stop_action, _delete_media_action),
        paging="none",
        notes=("Transcript/events: listMeetingSessionTranscript (after cursor), listMeetingSessionEvents.",),
    )


@app.ui("meetings_workspace", description="Open the Telnyx Meeting Bot workspace.")
def meetings_workspace() -> PrefabApp:
    return workspace()
