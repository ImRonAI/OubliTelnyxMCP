# Python demo on oubliai_client

`workspace_demo.py` walks the four model-visible tools, opens the numbers
workspace, reads the renderer resource, and tracks a number-order task.

## Run

From the repository root, after an editable install:

```bash
uv pip install --python .venv -e packages/server -e 'packages/client[dev]'
```

Start the local server (or point `mcp.json` at a deployed host), then:

```bash
.venv/bin/python examples/python/workspace_demo.py
```

`main()` reads `mcpServers.oubliai-telnyx.url` from the root `mcp.json`
and authenticates with `oauth(mcp_url=url, token_storage=file_token_storage(~/.oubliai/tokens))`.
The first run opens a browser consent page. **Running the demo performs a
real Telnyx login — a user gate.**

## Test (no live login)

```bash
cd examples/python && DENO_NO_PACKAGE_JSON=1 ../../.venv/bin/python -m pytest -q
```

The tests in `test_demo_against_fixture.py` build the real in-process server
(`build_server` + a mock Telnyx transport + a static bearer token) and exercise
each demo function against it. No credentials leave the loopback fixture.
