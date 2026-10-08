# Decisions 2026-10-07: domain apps, background tasks, storage

Addendum to `VERIFIED_DECISIONS.md`. Every item is either an installed FastMCP 4.0.10 /
prefab-ui 0.20.2 / py-key-value-aio 0.4.6 behaviour that was executed in
`packages/server/tests`, or a value read from `docs/reference/telnyx/openapi.json`.

## Executed findings

1. **`tools/list` does not filter `meta.ui.visibility`.** `fastmcp/server/server.py:869-876`
   lists app-only tools and leaves filtering to the host; CodeMode's catalog
   (`fastmcp/server/transforms/catalog.py:202`) applies `is_model_visible`. Therefore domain
   `FastMCPApp` providers are added to the *operations* child before `CodeMode`
   (`server.build_operations`). Result over HTTP: `tools/list` stays exactly
   `execute, generate_prefab_ui, get_schema, search`; `search` surfaces the 14
   `<domain>_workspace` entries; `execute(call_tool('<domain>_workspace', {}))` returns the
   `$prefab` payload. Backends (`visibility=["app"]`) are excluded from the CodeMode
   catalog and callable only by their identity-addressed name `<12-hex>_<name>`
   (`fastmcp.server.providers.addressing.hashed_backend_name`), which is what the payload's
   `toolCall` references and `_meta.fastmcp.toolNames` carry.
2. **Backends reach Telnyx only through generated tools.** A `@app.tool()` body calls
   `ctx.fastmcp.call_tool("<operationId>", args)`; the shared `httpx2` client carries the
   caller's token (`auth/passthrough.py`). Verified: `numbers_list` produced
   `GET /v2/phone_numbers?page[number]=2&page[size]=10` with `Authorization: Bearer <caller>`.
   A `CallTool("<operationId>")` string from the UI is hash-prefixed with the app's hash and
   fails as unknown, so UI actions reference backends by function only.
3. **Destructive and cost actions are confirmed server-side in the UI path.**
   `register_confirmed_backend` raises `ToolError` unless `confirm == resource_id`; the UI
   exposes it through a prefab `Dialog`. `CreateNumberOrder`, `SendMessage`, `SendFax`,
   `CreateEmailMessage`, `DialCall`, `CreateMessagingProfile` (requires a list field no form
   can supply) and fine-tuning job creation are not form-backed; they stay explicit
   `execute` calls. **Scope of the gate:** it protects the renderer path (a click on a
   workspace) from accidental side effects. The model path is the generated catalog as the
   schema declares it; an authenticated account owner can run `DeletePhoneNumber` through
   `execute` exactly as through the Telnyx API. Hiding "dangerous" operations from CodeMode
   was considered and rejected: the schema carries no destructive/cost marker
   (`x-endpoint-cost` is latency cost, not money), so any denylist would be invented, and
   AGENTS.md "Registered-disabled operations are not working coverage" forbids pretending
   hidden operations are covered. Live-action policy (no purchases/sends/calls in tests)
   governs our tests, not the user's own account.
4. **Form models mirror schema request bodies.** Each app's `FORM_MODELS` maps an
   operationId to a pydantic model whose field names are a subset of that operation's
   request-body properties (tested). `Form.from_model` skips nested/list fields, so those
   stay reachable through `execute`.
5. **Background tasks are the native `TasksExtension`.** Registered on the root in
   `build_server` (mounted-child extensions do not propagate). One task-enabled tool,
   `await_telnyx_resource` (`runtime/tasks.py`), polls `RetrieveNumberOrder` or
   `GetKvNamespace` until the schema's terminal statuses (`success|failure`;
   `provision_ok|provision_failed|delete_failed` — `deleting` is transitional per the
   schema description, deletion completes as a 404). `build_tasks_extension` refuses a
   non-`memory://` Docket URL without `FASTMCP_TASKS_ENCRYPTION_KEY` (tasks.md "Credentials
   at Rest": snapshots hold the caller's token and are plaintext by default). Verified via `call_tool_task`
   over HTTP: three polls, each `Bearer user-token`; exhaustion raises; `execute` runs it
   in the foreground; `tools/list` unchanged. OpenAPI-generated tools are
   `TaskConfig(mode="forbidden")` by FastMCP and cannot be task-enabled.
6. **Telnyx KV is served by the generated tools, not an adapter.** `PutKvKey`
   (octet-stream body, `ttl_secs`), `GetKvKey`, `DeleteKvKey`, `ListKvKeys` work end to end
   under BYOK (`tests/integration/test_kv_catalog.py`). A `key_value.BaseStore` subclass
   over Telnyx KV was rejected: store hooks cannot call MCP tools, so it would have been a
   hand-written REST path around the catalog, and `OAuthProxy.client_storage` runs outside
   any user request, where no caller token exists and no server-wide key is allowed.
7. **OAuthProxy storage is encrypted and selectable.** `runtime/storage.py::build_client_storage`
   wraps `MemoryStore` / `FileTreeStore` (V1 sanitizers, default under `fastmcp.settings.home`)
   / `RedisStore(url=...)` in `FernetEncryptionWrapper(Fernet(OUBLIAI_STORAGE_ENCRYPTION_KEY))`,
   per `storage-backends.md` "Server-Side OAuth Token Storage". Verified: ciphertext at
   rest, persistence across instances, wrong key raises `DecryptionError`, OAuth routes
   unchanged with the wrapped store.

8. **Paging follows each generated tool's own schema.** Most list operations declare a
   `page` deepObject (FastMCP exposes one `page` object); `ListKvNamespaces` and
   `listVoiceDesigns` declare literal `page[number]`/`page[size]` names. The list recipe
   reads the generated tool's input schema and sends whichever shape it declares (tested
   over HTTP for both). The server-created Telnyx client is closed by a FastMCP `lifespan`;
   injected clients stay caller-owned (OpenAPIProvider never closes injected clients).

## Review record

Two independent Oracle reviews (framework fidelity; correctness/security) were run after
implementation. Fixed: bracketed paging dropped for two operations; `CreateMessagingProfile`
form could never satisfy `whitelisted_destinations`; fine-tuning create removed from forms
(cost); Redis Docket without snapshot key; `deleting` treated as terminal; unclosed
server-owned client. Rejected: hiding destructive operations from CodeMode (see item 3).

## Blockers / unverified (recorded, not worked around)

- How a KV namespace is "provisioned with TTL support" (PutKvKey 409) is not in the schema.
- Redis (`RedisStore`, Docket `redis://`) is construction-tested only; no Redis here.
  Multi-replica deployment and `FASTMCP_TASKS_ENCRYPTION_KEY` rotation are acceptance gates.
- In-memory Docket cancellation is cooperative (at most one in-flight poll completes).
- The host must treat a `$prefab` payload returned by `execute` as renderable; `execute`
  itself carries no `meta.ui.resourceUri` (the Prefab renderer resources remain listed).
- `DeleteKvKey` returns 200 whether or not the key existed.
