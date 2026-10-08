# oubliai-client

Full native `fastmcp.Client` integration for the Oubliai Telnyx MCP server.
Wraps the protocol surface — catalog, workspaces, renderer resource, tasks,
handlers — without reimplementing MCP, an agent loop, or a renderer.

## Install

From the repository root, after a `.venv` exists:

```bash
uv pip install --python .venv -e packages/server -e 'packages/client[dev]'
```

The `dev` extra pins `pytest` and `pytest-asyncio` for the test suite.

## Connect

`connect(target, *, auth=..., progress_handler=..., ...)` returns an
`OubliaiConnection` (a configured `fastmcp.Client`). Use it as an async
context manager.

Bearer token for tests and CI:

```python
from oubliai_client import connect, bearer

async with connect("http://127.0.0.1:8000/mcp", auth=bearer("user-token")) as conn:
    ...
```

Real Telnyx OAuth login (browser flow):

```python
from pathlib import Path
from oubliai_client import connect, oauth, file_token_storage

async with connect(
    url,
    auth=oauth(mcp_url=url, token_storage=file_token_storage(Path.home() / ".oubliai" / "tokens")),
) as conn:
    ...
```

The first run opens the consent page; tokens persist in the `FileTreeStore`
directory. `bearer(token)` and `oauth(**kwargs)` return `fastmcp.client.auth`
objects; `file_token_storage(directory)` returns a `FileTreeStore`.

## Catalog

The model-visible tools are exactly `MODEL_VISIBLE_TOOLS = ("search",
"get_schema", "execute", "generate_prefab_ui")`. The wrappers return the
native `fastmcp.client.client.CallToolResult` — use `.content`,
`.structured_content`, `.data`, `.is_error`, `.meta` directly; results are
never stringified.

```python
from oubliai_client import search, get_schema, execute, list_model_visible_tools

found = await search(conn, "list available phone numbers")
schema = await get_schema(conn, ["ListAvailablePhoneNumbers"])
out = await execute(conn, "return await call_tool('ListAvailablePhoneNumbers', {})")
tools = await list_model_visible_tools(conn)
```

## Workspaces

`WORKSPACE_DOMAINS` holds the 14 server apps. `open_workspace(conn, domain)`
returns a frozen `WorkspacePayload` whose `.raw` is the untouched `$prefab`
payload for a host, plus `.result`, `.prefab_version`, `.view`,
`.tool_names`.

```python
from oubliai_client import open_workspace

ws = await open_workspace(conn, "numbers")
assert ws.prefab_version == "0.3"
```

## Renderer resource

The MCP App host page is advertised at `RENDERER_URI` with
`RENDERER_MIME`. `read_renderer_resource(conn)` returns a frozen
`RendererResource` with `.uri`, `.mime_type`, `.html`, `.meta`, `.csp`,
`.permissions`. `find_renderer_resource(conn)` lists it without reading.
`generate_ui(conn, code)` calls the `generate_prefab_ui` tool.

## Tasks

`await_telnyx_resource_task(conn, *, kind, resource_id, poll_interval_seconds,
max_polls)` starts the `await_telnyx_resource` tool and returns a
`fastmcp_tasks.ToolTask`. Await it directly, or use `wait_for(task,
timeout=...)` to get the final `CallToolResult`. `task.status()` and
`task.cancel()` come from `ToolTask`.

```python
from oubliai_client import await_telnyx_resource_task, wait_for

task = await await_telnyx_resource_task(conn, kind="number_order", resource_id="no-1")
result = await task  # or await wait_for(task, timeout=30.0)
```

## Handlers

Adapters for the supported client-side hooks: `ProgressRecorder`,
`LogRecorder`, `NotificationRecorder`, `elicitation_handler(response)`,
`decline`, `cancel`, `sampling_handler(response)`, and `roots(paths)` for
converting local paths to `file://` URIs. The negotiated protocol (the
server selects 2026-07-28) drives any `elicitation/action` InputRequired
rounds automatically; the handlers only record or answer them.

```python
from oubliai_client import ProgressRecorder, LogRecorder

recorder = ProgressRecorder()
async with connect(url, progress_handler=recorder, log_handler=LogRecorder()) as conn:
    ...
```

## ClientGroup

`group({name: client})` wraps multiple connections in a
`fastmcp.client.group.ClientGroup`; `group_from_mcp_config(config)` builds
one from an MCP config dict.

## Testing

From `packages/client/`:

```bash
cd packages/client && DENO_NO_PACKAGE_JSON=1 ../../.venv/bin/python -m pytest -q
```

The marker `deno` marks tests that need the Deno runtime for
`generate_prefab_ui` compilation; `DENO_NO_PACKAGE_JSON=1` keeps Deno from
picking up the repo root `package.json`. In-process fixtures build the real
server with a mock Telnyx transport and a static bearer token, so no
credentials or live calls are needed.

## What is NOT verified live

The OAuth consent/entitlement flow, real Telnyx account entitlements, and
actual telecom delivery (number orders completing, messages sending, calls
placing) are user gates. The test fixtures prove client/server mechanics
against the pinned OpenAPI snapshot; they do not prove live delivery or
load performance.
