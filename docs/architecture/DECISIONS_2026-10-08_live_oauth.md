# Decisions 2026-10-08 — live Telnyx OAuth acceptance (localhost)

Executed against live Telnyx with a real confidential OAuth client, our server on
`http://localhost:18771`, and `fastmcp.Client(..., auth=OAuth(...))`. No credentials are
recorded here; the OAuth client is `oubliai-local-dev` (`client_id 8qI2tC7qexVUVvItjkzVpA`,
redirect `http://localhost:18771/auth/callback`, PKCE required, grants
`authorization_code`+`refresh_token`, all 32 scopes).

## Findings that changed code

1. **The schema's OAuth scope does not exist on the live service.** `openapi.json`
   `components.securitySchemes.oauthClientAuth` declares a single scope `admin`.
   `POST /v2/oauth_clients` with `allowed_scopes: ["admin"]` returns 422 code 10027:
   "must be a subset of account_management.read, …, wireless.write" (32 scopes). The same
   request with `numbers.read` returns 200. Reproduced with raw `curl`, independent of
   this repository. Decision: `spec.oauth_endpoints()` keeps URLs from the schema but
   takes `scopes` from Telnyx's RFC 8414 metadata
   (`docs/reference/telnyx/oauth-authorization-server.json`, `scopes_supported`), refreshed
   from `https://api.telnyx.com/.well-known/oauth-authorization-server` on 2026-10-08
   (only change vs. the prior copy: `code_challenge_methods_supported` is now `["S256"]`).
   This is the one documented exception to "schema as-is" and it exists because the schema
   value is rejected by Telnyx itself. The OAuthProxy advertises and requests all 32 scopes
   because the server exposes every Telnyx operation. Test:
   `tests/unit/test_spec_helpers.py::test_oauth_scopes_come_from_telnyx_authorization_server_metadata`.

2. **Telnyx rate-limits token introspection to 5 requests / 60 s per client**
   (`ratelimit-limit: 5, 5;w=60`; the 6th call returns 429 code 10011). FastMCP's
   `IntrospectionTokenVerifier` introspects on every request by default (documented:
   "Caching is disabled by default to preserve real-time revocation semantics"), so the
   live session died after five MCP requests with `invalid_token` 401. Decision: enable the
   documented `cache_ttl_seconds` (`auth/provider.py::INTROSPECTION_CACHE_TTL_SECONDS = 60`).
   Consequence: upstream revocation takes effect within 60 s, not instantly. Test:
   `tests/unit/test_auth_provider.py::test_introspection_results_are_cached_within_telnyx_rate_limit`.

## Verified live (2026-10-07 17:50–18:08 PDT)

- `POST /mcp` without token → 401 + `WWW-Authenticate: Bearer resource_metadata=…`.
- `/.well-known/oauth-protected-resource/mcp` and `/.well-known/oauth-authorization-server`
  → 200, 32 scopes, `code_challenge_methods_supported: ["S256"]`.
- Dynamic client registration (`POST /register` 201) → `/authorize` 302 → FastMCP consent
  page (200/302) → Telnyx portal consent → `GET /auth/callback` 302 → `POST /token` 200.
- `IntrospectionTokenVerifier` with `client_auth_method="client_secret_basic"` is accepted
  by `POST /v2/oauth/introspect` (200, `active: true` for the user token; `active: false`
  for an API key or garbage — API keys are not OAuth tokens and are still rejected).
  `client_secret_post` was also accepted. The live metadata has
  `introspection_endpoint_auth_methods_supported: null`.
- `list_tools` → exactly `execute, generate_prefab_ui, get_schema, search`.
- `search("phone numbers")` → "50 of 1386 tools".
- `execute("return await call_tool('ListPhoneNumbers', {'page': {'size': 2}})")` →
  `is_error=False`, structured `data` of 2 live phone-number records under the user's own
  token (BYOK confirmed end to end; no server-wide key is configured).
- `execute("return await call_tool('numbers_workspace', {})")` → `$prefab` payload (5.3 kB).
- Upstream token TTL from Telnyx: `expires_in=1800`; a refresh token is issued; refresh
  expiry is not reported (FastMCP falls back to 31536000 s).

## Schema defects observed (recorded, not patched in the schema)

- `GET /v2/oauth/clients` (schema path, `ListOAuthClients`) → 404 code 10005. The duplicate
  `GET /v2/oauth_clients` (`ListOAuthClients_2`) → 200. The live service serves the
  underscore path only; both remain in the catalog as generated.
- `oauthClientAuth.scopes = {admin}` as above.

## Not verified

- Refresh-token exchange was not exercised (session shorter than 1800 s).
- `fastmcp.Client` with in-memory token storage re-prompts for consent on every run; the
  probe used `FileTreeStore` with the V1 sanitizers (required per `storage-backends.md`).
