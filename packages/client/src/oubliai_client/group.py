from collections.abc import Mapping
from typing import Any

from fastmcp import Client
from fastmcp.client.client import ConnectMode
from fastmcp.client.group import ClientGroup
from fastmcp.mcp_config import MCPConfig


def group(clients: Mapping[str, Client[Any]]) -> ClientGroup:
    return ClientGroup(clients)


def group_from_mcp_config(
    config: MCPConfig | dict[str, Any], *, default_mode: ConnectMode = "auto"
) -> ClientGroup:
    return ClientGroup.from_config(config, default_mode=default_mode)
