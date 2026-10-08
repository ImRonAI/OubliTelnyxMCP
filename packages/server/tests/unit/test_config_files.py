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
