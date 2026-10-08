# meetings

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| GET | /meeting_sessions | listMeetingSessions | Meeting Sessions |
| POST | /meeting_sessions | createMeetingSession | Meeting Sessions |
| GET | /meeting_sessions/{id} | retrieveMeetingSession | Meeting Sessions |
| PATCH | /meeting_sessions/{id} | updateMeetingSession | Meeting Sessions |
| DELETE | /meeting_sessions/{id} | deleteMeetingSession | Meeting Sessions |
| POST | /meeting_sessions/{id}/actions/send_chat | sendChatMeetingSession | Meeting Session Actions |
| POST | /meeting_sessions/{id}/actions/speak | speakMeetingSession | Meeting Session Actions |
| POST | /meeting_sessions/{id}/actions/stop_speaking | stopSpeakingMeetingSession | Meeting Session Actions |
| GET | /meeting_sessions/{id}/artifacts | listMeetingSessionArtifacts | Meeting Session Artifacts |
| POST | /meeting_sessions/{id}/artifacts | createMeetingSessionArtifact | Meeting Session Artifacts |
| GET | /meeting_sessions/{id}/artifacts/{artifact_id} | retrieveMeetingSessionArtifact | Meeting Session Artifacts |
| GET | /meeting_sessions/{id}/events | listMeetingSessionEvents | Meeting Session Data |
| DELETE | /meeting_sessions/{id}/recording_media | deleteMeetingSessionRecordingMedia | Meeting Session Data |
| GET | /meeting_sessions/{id}/recordings | listMeetingSessionRecordings | Meeting Session Data |
| GET | /meeting_sessions/{id}/transcript | listMeetingSessionTranscript | Meeting Session Data |
