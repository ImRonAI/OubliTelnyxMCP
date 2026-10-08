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

_(filled in when T2.x land: public API, test counts, failure coverage)_

## Application (`packages/app`)

_(filled in: toolchain, module map, what Playwright proved against the real server)_

## Examples

_(filled in)_

## Deployment readiness

Checklist file: `packages/server/.env.example` (pinned by
`tests/unit/test_config_files.py::test_env_example_names_every_required_variable_and_no_values`,
which fails if a variable `create_server` requires goes missing or a secret gets a value).

**Entry point.** Browser-facing deployments start with `python -m oubliai_server`. `fastmcp run
fastmcp.json` runs the same `create_server` factory but cannot pass the `OUBLIAI_BROWSER_ORIGINS`
CORS middleware (`runtime/cors.py`, FastMCP emits no CORS headers by itself), so the `packages/app`
host and `examples/embed` cannot reach `/mcp` from a browser through it. `fastmcp inspect
src/oubliai_server/__main__.py:create_server` shows 4 tools / 29 resources — this is what Horizon sees.

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
