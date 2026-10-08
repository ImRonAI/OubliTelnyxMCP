"""Static-token FastMCP fixture server for the packages/app TypeScript tests.

Builds the real Oubliai MCP server against a mocked Telnyx HTTP transport, binds
it to a real localhost port, prints `OUBLIAI_FIXTURE_URL=<url>` (single line,
flushed) for the vitest global setup, and exits cleanly on SIGTERM/SIGINT.

The accepted bearer token is `e2e-token`. Every mocked Telnyx request is logged
to stderr as `TELNYX <method> <path> auth=<present|absent>`; token values are
never logged.
"""

from __future__ import annotations

import asyncio
import json
import signal
import sys
from pathlib import Path
from typing import Any

import httpx2
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.tests import run_server_async
from fastmcp_tasks import TasksExtension

from oubliai_server import build_server
from oubliai_server.runtime.http import make_telnyx_client
from oubliai_server.spec import load_telnyx_spec

FIXTURE_TOKEN = "e2e-token"
RESPONSES_PATH = Path(__file__).with_name("telnyx_mock_responses.json")

TOKEN_PATTERN = "{id}"


def _load_responses() -> dict[str, dict[str, Any]]:
    with RESPONSES_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _make_handler(responses: dict[str, dict[str, Any]]):
    def telnyx(request: httpx2.Request) -> httpx2.Response:
        auth_header = request.headers.get("authorization")
        auth_state = "present" if auth_header else "absent"
        print(
            f"TELNYX {request.method} {request.url.path} auth={auth_state}",
            file=sys.stderr,
            flush=True,
        )
        key = f"{request.method} {request.url.path}"
        entry = responses.get(key)
        if entry is None and TOKEN_PATTERN in key:
            base = key.split(TOKEN_PATTERN)[0].rstrip("/")
            entry = responses.get(f"{base}/{TOKEN_PATTERN}") or responses.get(
                f"{request.method} {base}/{TOKEN_PATTERN}"
            )
        if entry is None:
            return httpx2.Response(
                404,
                json={
                    "errors": [
                        {
                            "code": "10039",
                            "title": "Resource not found",
                            "detail": f"No fixture for {request.method} {request.url.path}",
                            "source": {
                                "pointer": request.url.path,
                            },
                        }
                    ]
                },
            )
        content_type = entry.get("content_type")
        if content_type == "text/plain":
            return httpx2.Response(
                entry["status"],
                content=str(entry["body"]),
                headers={"content-type": content_type},
            )
        return httpx2.Response(entry["status"], json=entry["body"])

    return telnyx


async def _main() -> None:
    responses = _load_responses()
    spec = load_telnyx_spec()
    client = make_telnyx_client(
        "https://api.telnyx.com/v2",
        transport=httpx2.MockTransport(_make_handler(responses)),
    )
    server = build_server(
        spec,
        client=client,
        auth=StaticTokenVerifier(
            tokens={FIXTURE_TOKEN: {"client_id": "e2e", "scopes": []}}
        ),
        tasks=TasksExtension(url="memory://"),
        mask_error_details=False,
    )

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop_event.set)

    async with run_server_async(server, host="127.0.0.1") as url:
        print(f"OUBLIAI_FIXTURE_URL={url}", flush=True)
        await stop_event.wait()


if __name__ == "__main__":
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        pass
