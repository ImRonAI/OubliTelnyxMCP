import json

from oubliai_server.spec import (
    OAUTH_AS_METADATA_PATH,
    collision_names,
    foreign_server_routes,
    oauth_endpoints,
)


def test_oauth_endpoints_come_from_canonical_schema(telnyx_spec):
    endpoints = oauth_endpoints(telnyx_spec)
    assert {k: v for k, v in endpoints.items() if k != "scopes"} == {
        "authorization_url": "https://api.telnyx.com/v2/oauth/authorize",
        "token_url": "https://api.telnyx.com/v2/oauth/token",
        "introspection_url": "https://api.telnyx.com/v2/oauth/introspect",
    }


def test_oauth_scopes_come_from_telnyx_authorization_server_metadata(telnyx_spec):
    """Live Telnyx rejects the schema's `admin` scope (422 on POST /v2/oauth_clients,
    2026-10-08); the RFC 8414 metadata lists the 32 scopes the service actually accepts."""
    metadata = json.loads(OAUTH_AS_METADATA_PATH.read_text(encoding="utf-8"))
    scopes = oauth_endpoints(telnyx_spec)["scopes"]
    assert scopes == metadata["scopes_supported"]
    assert len(scopes) == 32
    assert "admin" not in scopes
    assert {"numbers.read", "numbers.write", "messaging.write", "voice.write"} <= set(scopes)


def test_foreign_server_routes(telnyx_spec):
    assert foreign_server_routes(telnyx_spec) == {
        ("POST", "/v1/chat/completions"),
        ("POST", "/v1/audio/speech"),
        ("POST", "/v1/audio/transcriptions"),
        ("GET", "/speech-to-text/transcription"),
    }


def test_collision_names_use_schema_summaries(telnyx_spec):
    assert collision_names(telnyx_spec) == {
        "get_conversations_public__conversation_id__insights_get": "Get insights for a conversation",
        "get_conversations_public__conversation_id__messages_get": "Get conversation messages",
        "post_public_missions_missions_mission_id_runs_run_id_plan": "Create initial plan",
        "post_public_missions_missions_mission_id_runs_run_id_plan_steps": "Add step(s) to plan",
    }
