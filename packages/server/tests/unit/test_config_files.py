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


def test_repo_root_entrypoint_reexports_the_server_factory():
    """Horizon reads `requirements.txt` and `server.py` at the repository root; they must
    install packages/server and expose the same `create_server` factory as `fastmcp.json`."""
    import importlib.util

    import tomllib

    requirements = {
        line.strip()
        for line in (REPO_ROOT / "requirements.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }
    pyproject = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text())
    # Horizon installs this file with `uv pip install -r`; the local package line is what puts
    # `oubliai_server` in site-packages, the pins mirror the manifest for installers that drop extras.
    assert "./packages/server" in requirements
    assert requirements - {"./packages/server"} == set(pyproject["project"]["dependencies"])
    spec = importlib.util.spec_from_file_location("root_server", REPO_ROOT / "server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.create_server is entry.create_server


def test_create_server_single_tenant_mode_needs_only_key_and_access_token(monkeypatch):
    """With `OUBLIAI_TELNYX_API_KEY` + `OUBLIAI_ACCESS_TOKEN` set, the OAuthProxy variables are
    not required: `/mcp` is gated by FastMCP's `StaticTokenVerifier` and Telnyx calls use the
    server key (single-tenant demo mode)."""
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

    for name in entry.REQUIRED_ENV:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("OUBLIAI_TELNYX_API_KEY", "KEY_demo")
    monkeypatch.setenv("OUBLIAI_ACCESS_TOKEN", "shared-access-token-123456")
    monkeypatch.setenv("OUBLIAI_STORAGE_URL", "memory://")
    monkeypatch.setattr(fastmcp.settings, "http_host_origin_protection", True)
    server = entry.create_server()
    assert isinstance(server.auth, StaticTokenVerifier)
    assert "shared-access-token-123456" in server.auth.tokens


def test_single_tenant_mode_refuses_short_access_token(monkeypatch):
    for name in entry.REQUIRED_ENV:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("OUBLIAI_TELNYX_API_KEY", "KEY_demo")
    monkeypatch.setenv("OUBLIAI_ACCESS_TOKEN", "short")
    monkeypatch.setattr(fastmcp.settings, "http_host_origin_protection", True)
    with pytest.raises(SystemExit, match="OUBLIAI_ACCESS_TOKEN"):
        entry.create_server()
