# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read first
`AGENTS.md` files (root and one per working directory) are binding. Before touching a package, read the root `AGENTS.md`, the package's `AGENTS.md`, `docs/reference/SOURCE_INDEX.md` and `docs/architecture/VERIFIED_DECISIONS.md`. VERIFIED_DECISIONS overrides everything else.

**Stale planning material:** the root HTML dossier (`index.html`, `server.html`, `app.html`, …), `source-plan.md` and `.omo/plans/*.md` predate VERIFIED_DECISIONS. Their facilitator/host choices are outdated, and the `.omo` plans use an old `telnyx_mcp` layout with BM25 discovery. They are history, not specs. Keep them as they are; don't edit or delete them.

## Project state
This is a monorepo ("oubliai") for a Telnyx MCP product. `packages/server` works end to end in tests: composition, BYOK token passthrough, Telnyx OAuth over Streamable HTTP, 14 domain workspaces, background tasks, encrypted OAuth storage. `packages/client` and `packages/app` are still manifest-only scaffolds, as are most `src/` subdirectories. A folder existing doesn't mean the feature is implemented. Build and test commands come from each package's manifest, so check it before assuming any script exists.

## Pinned stack (docs/reference/contracts/FAST_MCP_AND_UI.md)
- Python 3.12, `fastmcp==4.0.10` (extras `apps`, `code-mode`; CodeMode runs in the `pydantic_monty` sandbox), `mcp==2.2.0`, `prefab-ui==0.20.2` (imported as `prefab_ui`), `httpx2` (FastMCP's HTTP client; it is not `httpx`)
- JS (Node ≥22): `ai@7.0.127`, `@ai-sdk/mcp@2.0.66`, `@modelcontextprotocol/ext-apps@2.0.3`
- The root `.venv` (managed by uv) already has fastmcp/mcp/prefab_ui/fastmcp_tasks/key_value installed. Deno (Homebrew) is on PATH; the GenerativeUI server-side validation needs it plus `DENO_NO_PACKAGE_JSON=1` (a stray `~/package.json` otherwise breaks the npm:pyodide resolution).

## Commands
```bash
# packages/server (verified). pytest uses asyncio_mode=auto, so async tests need no marker
uv pip install --python ../../.venv -e '.[dev]'
DENO_NO_PACKAGE_JSON=1 ../../.venv/bin/python -m pytest -q
../../.venv/bin/python -m pytest tests/unit/test_passthrough_auth.py::test_refuses_without_user_token
```
Other packages (same pattern; counts as of 2026-10-09):
- `packages/client`: `uv pip install --python ../../.venv -e '.[dev]'` then `DENO_NO_PACKAGE_JSON=1 ../../.venv/bin/python -m pytest -q` (47 passed; `deno` marker for the renderer round-trip).
- `examples/python`: `DENO_NO_PACKAGE_JSON=1 ../../.venv/bin/python -m pytest -q` (5 passed).
- `packages/app`: `pnpm install && pnpm typecheck && pnpm test` (vitest 55 passed against the real-server fixture `tests/fixtures/static_token_server.py`) `&& pnpm build && DENO_NO_PACKAGE_JSON=1 pnpm test:e2e` (Playwright 22 passed; host :8080, sandbox :8081).
- `examples/embed`: `pnpm install && DENO_NO_PACKAGE_JSON=1 pnpm test:e2e` (Playwright 3 passed; page :8090, reuses the app sandbox :8081). Requires `packages/app` built first.
If these commands don't match a package's current manifest, trust the manifest. Don't invent output.

Run over HTTP from `packages/server` with `python -m oubliai_server` (`fastmcp run fastmcp.json` runs the same factory but cannot pass the browser CORS middleware; see `OUBLIAI_BROWSER_ORIGINS` below). Variable checklist: `packages/server/.env.example`.
```bash
OUBLIAI_BASE_URL=https://mcp.example.com OUBLIAI_TELNYX_CLIENT_ID=... OUBLIAI_TELNYX_CLIENT_SECRET=... \
OUBLIAI_JWT_SIGNING_KEY=... OUBLIAI_ALLOWED_CLIENT_REDIRECT_URIS='["https://claude.ai/api/mcp/auth_callback"]' \
OUBLIAI_STORAGE_ENCRYPTION_KEY=<Fernet key> OUBLIAI_STORAGE_URL=redis://... \
FASTMCP_HTTP_HOST_ORIGIN_PROTECTION=true FASTMCP_HTTP_ALLOWED_HOSTS='["mcp.example.com"]' \
../../.venv/bin/fastmcp run fastmcp.json --port 8000
```
Environment, all read by `__main__.create_server` / FastMCP. Two auth modes, chosen by whether `OUBLIAI_TELNYX_API_KEY` is set:
- **Single-tenant (demo):** `OUBLIAI_TELNYX_API_KEY` (the operator's own Telnyx key, used for every upstream call via `make_telnyx_client(api_key=...)`) + `OUBLIAI_ACCESS_TOKEN` (>=24-char random secret; `/mcp` is gated by FastMCP's `StaticTokenVerifier` with that single bearer). The OAuthProxy variables below are then not required. Everyone holding the access token acts as that Telnyx account — only for one operator's own account.
- **Per-user BYOK (default):** the OAuthProxy variables below; the connected user's own Telnyx token is forwarded.
- `OUBLIAI_BASE_URL`, `OUBLIAI_TELNYX_CLIENT_ID`, `OUBLIAI_TELNYX_CLIENT_SECRET`, `OUBLIAI_JWT_SIGNING_KEY`, `OUBLIAI_ALLOWED_CLIENT_REDIRECT_URIS` (JSON list) — OAuthProxy.
- `OUBLIAI_BROWSER_ORIGINS` (optional JSON list of exact origins, e.g. `["https://app.cato-labs.com"]`): browser hosts such as the `packages/app` page call `/mcp` cross-origin and FastMCP emits no CORS headers by itself. When set, `python -m oubliai_server` adds the FastMCP-documented `CORSMiddleware` (MCP headers allowed, `mcp-session-id` exposed) via `run(middleware=..., allowed_origins=...)` — `runtime/cors.py`. `"*"` is refused. `fastmcp run fastmcp.json` cannot pass middleware, so browser-facing deployments must use the module entry point.
- `OUBLIAI_STORAGE_ENCRYPTION_KEY` (required Fernet key; `python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'`) and `OUBLIAI_STORAGE_URL` (`memory://`, `file://<path>`, `redis://…`/`rediss://…`; unset = `FileTreeStore` under `fastmcp.settings.home/oubliai-storage`) — `runtime/storage.py::build_client_storage`, always wrapped in `FernetEncryptionWrapper`, passed as OAuthProxy `client_storage`.
- `FASTMCP_DOCKET_URL` (default `memory://`), `FASTMCP_DOCKET_CONCURRENCY`, `FASTMCP_DOCKET_NAME`, `FASTMCP_DOCKET_WORKER_NAME` — `runtime/tasks.py::build_tasks_extension`. Any non-`memory://` Docket **requires** `FASTMCP_TASKS_ENCRYPTION_KEY` (startup refuses otherwise; task snapshots hold the caller's token).
- Config files:
  - `packages/server/fastmcp.json` is the server config: factory entrypoint `create_server`, HTTP deployment.
  - Root `mcp.json` is the standard `mcpServers` client config (remote URL, `auth: "oauth"`), validated against FastMCP's `MCPConfig`. `fastmcp discover`, `fastmcp list mcp.json` and MCP clients use it. Change its URL when you deploy.
- **The Host/Origin guard must be set in the process environment**, not in `fastmcp.json` `deployment.env`. In-process `fastmcp run` (no `environment` section) applies `deployment.env` after `fastmcp.settings` is loaded; this was checked: a foreign Host still got 401 instead of 421. `create_server()` refuses to start unless `fastmcp.settings.http_host_origin_protection` is true. `mask_error_details=True` is set in code.
- `<OUBLIAI_BASE_URL>/auth/callback` must be registered as a redirect URI on the Telnyx OAuth client.
- OAuthProxy state is persisted through `build_client_storage` (encrypted). Default FileTree storage is single-instance; use `OUBLIAI_STORAGE_URL=redis://…` (plus a Redis `FASTMCP_DOCKET_URL`) for multiple replicas. Redis is an acceptance gate: no Redis is available locally, so it is construction-tested only.

Server tests use the in-memory `fastmcp.Client(server)` and an `httpx2.MockTransport` passed through `make_telnyx_client(..., transport=...)`. They never hit Telnyx. HTTP tests (`tests/integration/test_http.py`, `test_tasks.py`, `test_apps_contract.py`, `test_kv_catalog.py`) use `fastmcp.utilities.tests.asgi_server`/`asgi_client` with FastMCP's `StaticTokenVerifier` (the in-memory transport does not support `auth=`). Pass `tasks=TasksExtension(url="memory://")` to `build_server` in tests so a repo `.env` cannot redirect Docket. The `telnyx_spec` fixture in `tests/conftest.py` loads the canonical schema once per session.

## Architecture (verified path)
Three packages, each owned separately:

- **`packages/server` → `oubliai_server`**: a FastMCP server. Telnyx operations come from `OpenAPIProvider` / `FastMCP.from_openapi()` over the canonical schema `docs/reference/telnyx/openapi.json`. Don't hand-write an endpoint catalog. An *operations* child server carries the native `CodeMode` transform (`search`, `get_schema`, `execute`) and is mounted into a parent server that exposes native `GenerativeUI` (`generate_prefab_ui`) **outside** the CodeMode transform, so the UI metadata stays directly advertised. By default the model sees exactly those four tools. `.omo/ulw-research/build-verdict/probe_server.py` is the minimal executed proof of this composition. Entry point: `oubliai_server.build_server(spec, client=...)` in `server.py`. Upstream auth is `auth/passthrough.py::TelnyxUserBearerAuth`, an `httpx2.Auth` that copies the caller's `get_access_token()` onto each Telnyx request and raises if there is none. There is intentionally no server-wide key. The schema has 1382 operations. `build_operations` excludes 11 of them through FastMCP `route_maps`/`route_map_fn`, leaving 1371 tools:
  - operations tagged `OAuth Protocol` (token exchange, introspection, registration, grants), which belong to the auth layer
  - operations whose own `servers` differ from `servers[0]` (x402 and `wss://`), because `OpenAPIProvider` only calls `servers[0]`

  Name collisions are resolved by `spec.collision_names()` (`mcp_names` from each colliding operation's schema `summary`, e.g. `Get_conversation_messages`); no FastMCP `_2` tiebreaks remain (tested).

  **Domain apps (`apps/`)**: 14 `FastMCPApp` providers (`oubliai-<domain>`, one per `docs/reference/telnyx/domains/*.md`), built from the shared recipe in `apps/recipes/` (`register_list_backend`/`register_detail_backend`/`register_form_backend`/`register_confirmed_backend` + `list_workspace`/`confirm_action`). They are added to the **operations child before CodeMode**: FastMCP's `tools/list` does not filter `meta.ui.visibility` (host-side), but CodeMode's catalog does, so the model still sees exactly four tools and discovers `<domain>_workspace` entries through `search`; `execute(call_tool('numbers_workspace', {}))` returns the `$prefab` payload. Backends are app-only and callable by identity name `<hash>_<name>` (`fastmcp.server.providers.addressing.hashed_backend_name`); each one runs a generated tool via `ctx.fastmcp.call_tool(...)`, so BYOK holds and nothing re-implements REST. In the UI path, destructive tools run only through `register_confirmed_backend` (server-side `confirm == resource_id`) behind a prefab `Dialog`; live side effects such as `SendMessage`, `DialCall`, `CreateNumberOrder`, `CreateMessagingProfile`, fine-tuning creation are explicit `execute` calls, never forms. The model path is the generated catalog as the schema declares it (no invented destructive denylist). List recipes send paging in the shape the generated tool declares (`page` object vs literal `page[number]`/`page[size]`). Each app declares `GENERATED_TOOLS`, `FORM_MODELS` (fields ⊆ the schema request body, tested) and `CONFIRMED_ACTIONS`.

  **Background tasks (`runtime/tasks.py`)**: FastMCP `TasksExtension` on the root (`build_server(tasks=...)`); one task-enabled tool `await_telnyx_resource(kind, resource_id)` on the operations child polls `RetrieveNumberOrder` / `GetKvNamespace` until the schema's terminal statuses, with `Progress`. Clients start it with `fastmcp_tasks.call_tool_task`; through `execute` it runs in the foreground. Generated tools cannot be task-enabled (FastMCP marks them `forbidden`).

  **Telnyx KV**: served by the generated `PutKvKey`/`GetKvKey`/`DeleteKvKey`/`ListKvKeys` tools (tested end to end); there is deliberately no `BaseStore` adapter over Telnyx KV. See `docs/architecture/DECISIONS_2026-10-07_apps_tasks_storage.md`.

  **HTTP auth (OAuth-only, decided):** `auth/provider.py::build_auth` returns FastMCP `OAuthProxy`. It runs Telnyx's confidential-client authorization-code flow with our client credentials and validates upstream tokens with `IntrospectionTokenVerifier`. Endpoint URLs come from the schema's `oauthClientAuth` scheme via `spec.oauth_endpoints()`; **scopes come from `docs/reference/telnyx/oauth-authorization-server.json` (`scopes_supported`, 32 scopes)** because live Telnyx rejects the schema's only scope `admin` (422 on `POST /v2/oauth_clients`, verified 2026-10-08 — see `docs/architecture/DECISIONS_2026-10-08_live_oauth.md`). Telnyx limits `POST /v2/oauth/introspect` to 5 requests/60 s per client, so the verifier uses FastMCP's documented `cache_ttl_seconds` (`INTROSPECTION_CACHE_TTL_SECONDS = 60`); revocation lands within 60 s. The Telnyx OAuth client must list `<OUBLIAI_BASE_URL>/auth/callback` as a redirect URI, allow `authorization_code`+`refresh_token`, and allow every scope you want users to grant; register it via `POST /v2/oauth_clients` (the schema's `/oauth/clients` path returns 404 live). Raw API keys are deliberately **not** accepted. `get_access_token().token` is the user's Telnyx token, so the passthrough needs no changes. Custom routes don't inherit MCP auth. Subdirs: `domains/<telnyx-domain>` (mirrors `docs/reference/telnyx/domains/*.md`), `apps/` (UI definitions), `auth/`, `runtime/`, `stores/`.
- **`packages/client` → `oubliai_client`**: the full native `fastmcp.Client` integration (tasks, notifications, elicitation, sampling, OAuth). It keeps structured content and metadata instead of stringifying. Not an agent runtime.
- **`packages/app` → `oubliai-app`**: TypeScript. Uses AI SDK `ToolLoopAgent` with the `@ai-sdk/mcp` adapter as the facilitator. Rendering goes through the official ext-apps `AppBridge` plus the basic-host sandbox (`docs/reference/mcp-apps/official-*.ts`). UI metadata lives at `toolMetadata.app` (not `toolMetadata.mcp.app`).
- **`examples/embed`, `examples/python`**: consumers of the packages above.

**Rejected paths. Do not reintroduce:** a Pydantic-AI result-mapping facilitator; the AI SDK experimental React renderer; patching CSP or iframe isolation to load Prefab assets; a custom renderer, postMessage relay, discovery engine, agent loop or queue; Telnyx Assistant Chat as a UI event transport.

## Reference material
- Telnyx: `docs/reference/telnyx/openapi.json` (canonical; root `openapi.json`/`telnyx-openapi.json` are preserved originals), `operation-index.json`, `domains/*.md`, `auth.md`, OAuth metadata JSON.
- FastMCP docs snapshot: `docs/reference/fastmcp/pages/*.md`, `client/*.md`, `llms-full.txt`. When docs and the installed 4.0.10 API disagree, the installed API wins. Check it in `.venv/lib/python3.12/site-packages/fastmcp`.
- JS public types: `docs/reference/ai-sdk/*.d.ts`, `docs/reference/mcp-apps/app-bridge-public-types.d.ts`.
- If no source-backed contract exists for something, record it as a blocker. Don't guess signatures, fields or event names.

## Safety
- BYOK: every Telnyx call is bound to the connected user's token, and caches/handlers stay scoped to that user.
- Never perform live purchases, sends, calls, DNS changes or destructive Telnyx tests without explicit authorization. Tests use mock transports.
- Registered-but-disabled operations don't count as coverage.
