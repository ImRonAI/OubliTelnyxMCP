import json
from pathlib import Path

import fastmcp
import pytest
from fastmcp.mcp_config import MCPConfig, RemoteMCPServer
from fastmcp.utilities.mcp_server_config import MCPServerConfig

import oubliai_server.__main__ as entry

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PACKAGE_ROOT.parents[1]


def test_fastmcp_json_is_valid_server_config():
    config = MCPServerConfig.from_file(PACKAGE_ROOT / "fastmcp.json")
    assert config.source.entrypoint == "create_server"
    assert config.deployment.transport == "http"


def test_project_mcp_json_points_clients_at_oauth_http_server():
    config = MCPConfig.model_validate(json.loads((REPO_ROOT / "mcp.json").read_text()))
    server = config.mcpServers["oubliai-telnyx"]
    assert isinstance(server, RemoteMCPServer)
    assert server.transport == "http"
    assert server.auth == "oauth"


def test_create_server_refuses_to_start_without_host_origin_guard(monkeypatch):
    for name in entry.REQUIRED_ENV:
        monkeypatch.setenv(name, '["http://localhost:*"]' if name.endswith("URIS") else "x" * 16)
    monkeypatch.setattr(fastmcp.settings, "http_host_origin_protection", False)
    with pytest.raises(SystemExit, match="FASTMCP_HTTP_HOST_ORIGIN_PROTECTION"):
        entry.create_server()


def test_run_options_carry_browser_cors_from_env(monkeypatch):
    """`main()` must hand FastMCP the CORS middleware and trusted origins for the browser
    host; without them the packages/app host cannot reach `/mcp` cross-origin."""
    monkeypatch.setenv("OUBLIAI_BROWSER_ORIGINS", '["http://localhost:8080"]')
    options = entry.run_options()
    assert options["transport"] == "http"
    assert options["allowed_origins"] == ["http://localhost:8080"]
    assert len(options["middleware"]) == 1

    monkeypatch.delenv("OUBLIAI_BROWSER_ORIGINS")
    options = entry.run_options()
    assert "middleware" not in options and "allowed_origins" not in options


def test_env_example_names_every_required_variable_and_no_values():
    """`.env.example` is the deployment checklist: it must list every variable
    `create_server` requires plus the browser-CORS and Host/Origin guard settings,
    and it must not carry secret values."""
    example = (PACKAGE_ROOT / ".env.example").read_text()
    names = {
        line.split("=", 1)[0]
        for line in example.splitlines()
        if line and not line.startswith("#") and "=" in line
    }
    for required in entry.REQUIRED_ENV:
        assert required in names, required
    for setting in (
        "OUBLIAI_BROWSER_ORIGINS",
        "FASTMCP_HTTP_HOST_ORIGIN_PROTECTION",
        "FASTMCP_HTTP_ALLOWED_HOSTS",
        "OUBLIAI_STORAGE_URL",
        "FASTMCP_DOCKET_URL",
        "FASTMCP_STATELESS_HTTP",
    ):
        assert setting in names, setting
    secrets = ("OUBLIAI_TELNYX_CLIENT_SECRET", "OUBLIAI_JWT_SIGNING_KEY", entry.ENCRYPTION_KEY_ENV)
    for line in example.splitlines():
        key, _, value = line.partition("=")
        if key in secrets:
            assert value == "", f"{key} must be left blank in .env.example"
