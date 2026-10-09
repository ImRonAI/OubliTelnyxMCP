# Decisions 2026-10-08 — Python client, TypeScript application, examples

Companion to `VERIFIED_DECISIONS.md`. Records what was verified from installed sources before
and during implementation of `packages/client`, `packages/app` and `examples/*`, and what remains
a user-owned acceptance gate. Fill-in sections are completed as each wave lands.

## Verified before implementation (installed source, not docs)

- Workspaces: `oubliai_server.apps.ALL_APPS` has **14** entries (numbers, messaging, fax, verify,
  video, meetings, email, voice, ai, rag, speech, storage, training, platform).
- AI SDK `ai/test` exports `MockLanguageModelV4` (and V3); the executed research probe
  (`docs/architecture/SDK_PROBE_RESULT.json`) used **V4** with `doStream` fixtures.
- `@ai-sdk/mcp` 2.0.66 exports `createMCPClient`, `mcpAppClientCapabilities`,
  `readMCPAppResource`, `splitMCPAppTools`; UI parts carry `toolMetadata.app`.
- `@modelcontextprotocol/ext-apps` 2.0.3: `AppBridge`, `PostMessageTransport`,
  `RESOURCE_MIME_TYPE`, `getToolUiResourceUri`, `buildAllowAttribute` on the `app-bridge` subpath;
  host and sandbox must be different origins (`docs/reference/mcp-apps/official-serving.ts`).
  `docs/reference/mcp-apps/host-styles.md` does not exist; the host-style/theme helpers used by
  the proven probe live in `.omo/ulw-research/build-verdict/probe-js/basic-host/src/`.
- `@telnyx/video` 1.0.2 main declaration exports `initialize()`/`Room`, not the
  `createLocalParticipant` shown in `docs/reference/telnyx/sdk/video.md`; the installed `.d.ts`
  is authoritative.
- `fastmcp.utilities.tests.asgi_client` exists (line ~409) alongside `asgi_server` and
  `run_server_async`; `fastmcp_tasks.call_tool_task` / `ToolTask` are the task client APIs
  (there is no `fastmcp.client.tasks`).

## Client (`packages/client`)

Package `oubliai_client` (`packages/client/src/oubliai_client`), a thin layer over FastMCP's
`fastmcp.Client`; nothing in it bypasses the documented client API. Public surface
(`__init__.__all__`): `connect`/`OubliaiConnection`/`server_summary` (connection), `bearer`,
`oauth(mcp_url=...)`, `file_token_storage` (auth; FastMCP `BearerAuth`/`OAuth`/FileTree storage),
`MODEL_VISIBLE_TOOLS`, `list_model_visible_tools`, `search`, `get_schema`, `execute` (catalog),
`WORKSPACE_DOMAINS`, `WorkspacePayload`, `open_workspace` (workspaces: `execute` → `$prefab` 0.3),
`RENDERER_URI`, `RENDERER_MIME`, `RendererResource`, `find_renderer_resource`,
`read_renderer_resource`, `generate_ui` (ui), `ToolTask`, `call_tool_task`,
`await_telnyx_resource_task`, `wait_for` (tasks; `fastmcp_tasks` API), `ProgressRecorder`,
`LogRecorder`, `NotificationRecorder`, `elicitation_handler`, `decline`, `cancel`,
`sampling_handler`, `roots` (handlers), `group`, `group_from_mcp_config` (FastMCP `ClientGroup`).

Tests: **47 passed** (`DENO_NO_PACKAGE_JSON=1 ../../.venv/bin/python -m pytest -q`): 11 unit, 5
contract, 18 integration-style tests (parametrised cases make up the rest). `tests/conftest.py`
builds the **real** server (`real_server`) with FastMCP's `StaticTokenVerifier` and an
`httpx2.MockTransport` for Telnyx, so every integration test exercises the actual `/mcp` HTTP path.
Proven: `tools/list` returns exactly the 4 model-visible tools; the connected bearer reaches Telnyx
unchanged (`test_byok.py`); wrong token → connection rejected, Telnyx 4xx surfaces as a tool error,
malformed input and unknown tool names are rejected (`test_failures.py`); `await_telnyx_resource`
task completes, cancels, exhausts, and `wait_for` times out (`test_tasks.py`, scenario C2); all 14
workspaces return `$prefab` 0.3 and the renderer resource has MIME `text/html;profile=mcp-app`
(scenario C3). The renderer round-trip is marked `deno` because Prefab's bundler needs Deno.
Not verified live: OAuth consent through the client (`oauth()` only constructs FastMCP's `OAuth`),
real telecom delivery (README "What is NOT verified live").

## Application (`packages/app`)

Toolchain: node ≥ 22, pnpm, TypeScript strict NodeNext, esbuild (`build.mjs` → `dist/host`,
`dist/sandbox`, `dist/serve.js`), vitest 5 for contracts, `@playwright/test` 1.63 for e2e. Pinned
runtime deps: `ai` 7.0.127, `@ai-sdk/mcp` 2.0.66, `@ai-sdk/openai-compatible` 3.0.66,
`@modelcontextprotocol/{client,core,server}` 2.3.0, `@modelcontextprotocol/ext-apps` 2.0.3,
`zod` 4.2.0, `@telnyx/webrtc` 2.27.10, `@telnyx/video` 1.0.2.

Module map (`src/`): `mcp/` (`createOubliaiMcpClient({url, token})` over
`StreamableHTTPClientTransport` with `requestInit.headers`, `listModelVisibleToolNames`,
`callExecute`, `readRendererResource`); `agent/` (`createModel` → `createOpenAICompatible` from
`OUBLIAI_MODEL_*` or `ModelNotConfiguredError`; `createFacilitator` = native `ToolLoopAgent` +
`stepCountIs`; `extractToolParts` keeps `toolMetadata.app`; `createChatRouter` POST `/api/chat`
→ 400 / 503 `model_not_configured` / 401 `no_connection` / `pipeUIMessageStreamToResponse`);
`host/` (official ext-apps basic-host vendored verbatim except `// oubliai:` edits: ports, build-time
`__OUBLIAI_ALLOWED_REFERRER__`, `/healthz`, dev-only `/api/connection`, chat-route mount);
`workspace/` (`WORKSPACE_DOMAINS` = the 14 server domains, `openWorkspace`, `buildRenderPlan`);
`theme/` (`applyTheme`/`applyThemeWithPrefab` → `sendHostContextChange`; Prefab variables ride
the `McpUiHostContext` index signature because `McpUiStyles` is a closed 76-key record);
`media/` (`mintVoiceToken`/`mintRoomToken` via `execute` under the user's token,
`createVoiceSession` TelnyxRTC gated on `getUserMedia`, `createVideoSession` via
`@telnyx/video` `initialize()` — the installed `.d.ts` has no `createLocalParticipant`).

Tests: `pnpm typecheck` clean; vitest **55 passed / 11 files** against the real server fixture
(`tests/fixtures/static_token_server.py` = real `build_server` + mocked Telnyx, bearer
`e2e-token`); Playwright **22 passed** (`host-smoke`, `media-permissions` ×3, `workspaces` ×15,
`host-policy-denial` ×3). Proven against the real server over HTTP:
- `tools/list` returns exactly the 4 model-visible tools; `splitMCPAppTools` appVisible = 0;
  hidden `<12hex>_<name>` backends remain callable by name, which is how Prefab view actions
  reach Telnyx with the user's auth (not a permission bypass: same bearer).
- Scenario A1: `ToolLoopAgent` + `MockLanguageModelV4` drives `execute`, result keeps
  `structuredContent` and `toolMetadata.app` (`tests/contracts/agent.test.ts`).
- Scenario A2: every one of the 14 workspaces mounts the official sandbox on `:8081` with `csp=`
  from the renderer resource `_meta`, AppBridge initialises, and the view shows a value from that
  domain's mocked Telnyx list response (13 fixture entries added, each shaped from the
  operation's 200 schema in `docs/reference/telnyx/openapi.json`). Theme toggle flips
  `html[data-theme]` on host and view; dark palette measured in the live DOM as `oklch(0.985 0 0)`
  text on `oklch(0.145 0 0)` background. Screenshots `test-results/workspace-numbers-{light,dark}.png`.
- Scenario A3: sandbox embedding from a foreign loopback origin (`http://[::1]:8080`) is refused
  by the vendored `sandbox.ts` referrer check (page error "Embedding domain not allowed", no inner
  iframe); a renderer resource whose MIME is rewritten on the wire to `text/html` is refused by the
  vendored `implementation.ts` check (`lastError: Unsupported MIME type: text/html`, no mount).
- Media: permission denial mints nothing and connects nothing; grant mints one token and starts
  one voice session; `pagehide` disconnects exactly once.

Finding: the Prefab renderer (`prefab_ui/renderer/app.html`) registers no
`ui/resource-teardown` handler, so `teardownResource({})` rejects with "Method not found". The
vendored `unmount()` originally aborted before removing the iframe; it now uses the try/catch
shown in the installed `app-bridge.d.ts` teardown example and still calls `close()` + removes the
frame. Renderer behaviour, not changed. `tsconfig.json` excludes `src/host` and `tests/e2e` from
`tsc` (pre-existing); Playwright's transform compiles the specs.

Side fix while wiring the host: the server Prefab view paginated twice
(`70f441f server(apps): avoid duplicate workspace pagination`).

## Examples

`examples/python/workspace_demo.py` reads root `mcp.json`, connects with the real client API
(`summarize`, `show_catalog`, `open_numbers`, `renderer_info`, `track_number_order`) and is pinned
by `test_demo_against_fixture.py` (**5 passed**) against the same real-server fixture as the client
tests. `examples/embed` embeds a workspace through the `packages/app` host and the official
two-origin sandbox: `src/index.html` + `src/embed.ts` (`WorkspaceEmbed` connect/open/close/
setTheme/closeOnPageHide), served on `:8090` by `serve.mjs`, bundling the `packages/app` TypeScript
sources directly via `link:` (one SDK copy, nothing forked, no `packages/app` changes). Playwright
**3 passed** (`tests/embed.spec.ts`): connect, 14 options, sandbox mount with CSP, inner view
shows the fixture number before and after theme toggle, Close → `teardownResource` then
`close()` (iframe count 0), `pagehide` closes the bridge, rejected token → error banner and no
iframe, `:8081/index.html` → 404. Screenshot `examples/embed/test-results/embed-numbers.png`.

## Deployment readiness

Checklist file: `packages/server/.env.example` (pinned by
`tests/unit/test_config_files.py::test_env_example_names_every_required_variable_and_no_values`,
which fails if a variable `create_server` requires goes missing or a secret gets a value).

**Entry point.** Browser-facing deployments start with `python -m oubliai_server`. `fastmcp run
fastmcp.json` runs the same `create_server` factory but cannot pass the `OUBLIAI_BROWSER_ORIGINS`
CORS middleware (`runtime/cors.py`, FastMCP emits no CORS headers by itself), so the `packages/app`
host and `examples/embed` cannot reach `/mcp` from a browser through it. `fastmcp inspect
src/oubliai_server/__main__.py:create_server` shows 4 tools / 29 resources — this is what Horizon sees.
Because Horizon detects `requirements.txt`/`pyproject.toml` and a `server.py` at the repository
root, the root carries `requirements.txt` (`./packages/server`) and `server.py` re-exporting
`create_server`; entrypoint `server.py:create_server` gives the identical 4/29 inventory
(pinned by `test_repo_root_entrypoint_reexports_the_server_factory`, which also asserts the root
`requirements.txt` equals the `pyproject.toml` dependency list). First Horizon build failed: the
manifest lacked `fastmcp[tasks]` (`fastmcp_tasks`) and the `py-key-value-aio`
`filetree`/`redis`/`wrappers-encryption` extras the storage module imports — the dev venv had them
transitively. Fixed and re-proved with a clean `uv venv` install from `requirements.txt`.

**Environment (all verified against installed FastMCP 4.0.10 settings and `__main__.py`).**

| Variable | Required | Read by |
|---|---|---|
| `OUBLIAI_BASE_URL`, `OUBLIAI_TELNYX_CLIENT_ID`, `OUBLIAI_TELNYX_CLIENT_SECRET`, `OUBLIAI_JWT_SIGNING_KEY`, `OUBLIAI_ALLOWED_CLIENT_REDIRECT_URIS` (JSON list) | yes | `__main__.REQUIRED_ENV` → `auth/provider.py::build_auth` (OAuthProxy) |
| `OUBLIAI_STORAGE_ENCRYPTION_KEY` (Fernet) | yes | `runtime/storage.py::build_client_storage` |
| `OUBLIAI_STORAGE_URL` (`memory://`, `file://`, `redis://`, `rediss://`) | no (default FileTree, single instance) | `runtime/storage.py` |
| `FASTMCP_HTTP_HOST_ORIGIN_PROTECTION=true`, `FASTMCP_HTTP_ALLOWED_HOSTS` (JSON list) | yes, **process environment** (not `fastmcp.json` `deployment.env`) | FastMCP settings; `create_server` refuses to start otherwise |
| `OUBLIAI_BROWSER_ORIGINS` (JSON list of exact origins; `"*"` refused) | for browser hosts | `__main__.run_options` → `run(middleware=..., allowed_origins=...)` |
| `FASTMCP_DOCKET_URL` (+ `FASTMCP_TASKS_ENCRYPTION_KEY` when not `memory://`) | no | `runtime/tasks.py::build_tasks_extension` |
| `FASTMCP_STATELESS_HTTP=true` | for multi-worker/serverless | FastMCP settings (new transport per request) |
| `FASTMCP_HOST`, `FASTMCP_PORT` | no (127.0.0.1:8000) | FastMCP settings |

**Prefect Horizon (FastMCP's documented managed host; free personal tier).** From
`fastmcp-llms-full.txt` "Prefect Horizon": deploy = sign in at horizon.prefect.io with GitHub →
select the repo (public or private) → configure *Server name* (determines
`https://<name>.fastmcp.app/mcp`), *Entrypoint* (`fastmcp run` syntax —
`packages/server/src/oubliai_server/__main__.py:create_server`), *Authentication* toggle → Deploy;
redeploys on every push to `main`, preview deployments per PR. Dependencies are detected from a
`requirements.txt`/`pyproject.toml` in the repo (ours is `packages/server/pyproject.toml`). The CLI
offers `fastmcp login`/`whoami` only (signed in as tim@cato-labs.com); there is no CLI deploy.
Facts the documentation does **not** state and which therefore remain U2 gates, not assumptions:
whether the entrypoint may live in a monorepo sub-directory with the `pyproject.toml` beside it,
how environment variables are set, custom domains, and Redis provisioning. Horizon's own
*Authentication* must stay **off** for this server: the user's Telnyx identity (BYOK passthrough)
comes from our `OAuthProxy`, and a second OAuth layer in front of it would hide the Telnyx consent
flow the live acceptance test proved (`DECISIONS_2026-10-08_live_oauth.md`).

**Vercel (fallback; `cato-labs.com` already resolves to Vercel).** FastMCP's HTTP deployment
guide lists Vercel as a PaaS target with the generic requirement "Python 3.10+ and an HTTP port";
it documents nothing Vercel-specific. Serverless instances would need `FASTMCP_STATELESS_HTTP=true`
plus `OUBLIAI_STORAGE_URL=redis://…` and a Redis `FASTMCP_DOCKET_URL` (+`FASTMCP_TASKS_ENCRYPTION_KEY`),
and the introspection cache (`INTROSPECTION_CACHE_TTL_SECONDS = 60`) is per process, so many cold
instances could exceed Telnyx's 5/60 s introspection limit. Not attempted.

**Redis gate.** `redis://` storage/Docket are construction-tested only; no Redis server exists
locally and none was authorised. Any multi-replica deployment must run a Redis acceptance first.

**DNS.** `cato-labs.com` → 216.198.79.1 (Vercel), nameservers at Squarespace; no `mcp.`/`app.`
records exist. Creating them is a user action (root `AGENTS.md`: no DNS changes without explicit
authorisation) — gate U5. Two distinct browser origins are needed (host and sandbox), e.g.
`app.cato-labs.com` and `sandbox.cato-labs.com`. Only the **host** origin calls `/mcp`
(`src/host/connection.ts`, `src/mcp/client.ts`); the sandbox never contacts the server directly
(view tool calls travel over the AppBridge to the host), so `OUBLIAI_BROWSER_ORIGINS` lists the
host origin only.

**After deploy.** Register `<OUBLIAI_BASE_URL>/auth/callback` on a Telnyx OAuth client
(`POST /v2/oauth_clients`, 32 scopes, PKCE) — U3; replace the URL in root `mcp.json` (validated by
`test_project_mcp_json_points_clients_at_oauth_http_server`); run the real-user login — U7.

## User-owned acceptance gates (reported, not invented)

| ID | Gate |
|----|------|
| U1 | Model provider: `OUBLIAI_MODEL_BASE_URL`, `OUBLIAI_MODEL_API_KEY`, `OUBLIAI_MODEL_ID`; which Telnyx inference path is OpenAI-wire-compatible is unverified. |
| U2 | Horizon deployment through the Prefect Horizon web UI (GitHub repo import, env vars, Redis for >1 replica). |
| U3 | Telnyx OAuth client for the public hostname (`<OUBLIAI_BASE_URL>/auth/callback`, 32 scopes) and its secrets. |
| U4 | Live media acceptance (real mic/camera grant, controlled number/room, explicit authorization). |
| U5 | DNS/Vercel hostnames under `cato-labs.com` for the two app origins. |
| U6 | GitHub repository visibility and whether the 7 MB schema originals are committed. |
| U7 | Real-user OAuth login run after deployment. |
