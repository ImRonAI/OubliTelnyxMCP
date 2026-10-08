from typing import Literal, TypeAlias, cast

import httpx2
from fastmcp import Client
from fastmcp.client.transports import ClientTransport, StreamableHttpTransport

OubliaiConnection: TypeAlias = Client[ClientTransport]


def connect(
    target: OubliaiConnection | str,
    *,
    auth: httpx2.Auth | Literal["oauth"] | str | None = None,
) -> OubliaiConnection:
    if isinstance(target, Client):
        return target
    transport = StreamableHttpTransport(target, auth=auth)
    return cast(OubliaiConnection, Client(transport))
