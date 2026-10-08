"""Real GenerativeUI execution: Prefab code validated in the Deno/Pyodide sandbox.

Needs `deno` on PATH (and network on first run, to fetch Pyodide). Prefab passes the
process environment to Deno; `DENO_NO_PACKAGE_JSON=1` (official Deno setting) stops Deno
from resolving npm packages through an unrelated ancestor `package.json`.
"""

import shutil

import httpx2
import pytest
from fastmcp import Client

from oubliai_server import build_server
from oubliai_server.runtime.http import make_telnyx_client

pytestmark = pytest.mark.skipif(shutil.which("deno") is None, reason="deno not installed")

CODE = """\
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text
with PrefabApp() as app:
    with Column():
        Heading("Oubliai")
        Text("Generated in the Pyodide sandbox.")
"""


async def test_generate_prefab_ui_runs_in_sandbox(telnyx_spec, monkeypatch):
    monkeypatch.setenv("DENO_NO_PACKAGE_JSON", "1")
    telnyx = make_telnyx_client(
        "https://api.telnyx.com/v2",
        transport=httpx2.MockTransport(lambda request: httpx2.Response(500)),
    )
    async with Client(build_server(telnyx_spec, client=telnyx)) as client:
        result = await client.call_tool("generate_prefab_ui", {"code": CODE})

    assert not result.is_error
    view = result.structured_content
    assert view["$prefab"] == {"version": "0.3"}
    assert '"content": "Oubliai"' in str(view).replace("'", '"')
