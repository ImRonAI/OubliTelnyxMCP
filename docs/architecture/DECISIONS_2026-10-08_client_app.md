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

_(filled in: env var list, Horizon/Vercel steps, Redis gate)_

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
