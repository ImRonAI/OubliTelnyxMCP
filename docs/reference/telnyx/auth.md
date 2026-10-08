# auth.md

Not an agent? You're probably looking for the [authentication overview](https://developers.telnyx.com/api/v2/overview#authentication) or the [signup portal](https://portal.telnyx.com).

You are an agent. This document tells you how to register a credential for **Telnyx** and call the API. Follow the steps in order; do not skip ahead. The Telnyx REST API and the remote MCP server both live at `https://api.telnyx.com/v2` and share the same credential — there is no separate MCP token.

## Discover

Before registering, discover what Telnyx offers and which auth methods are available. The canonical `agent_auth` discovery surfaces are:

- **RFC 8414 authorization-server metadata** — `GET https://telnyx.com/.well-known/oauth-authorization-server` returns a JSON document with `authorization_endpoint`, `token_endpoint`, `grant_types_supported`, `scopes_supported`, and (when relevant) `register_uri` for dynamic client registration.
- **MCP server card** — `GET https://telnyx.com/.well-known/mcp/server-card.json` describes the live MCP server at `https://api.telnyx.com/v2/mcp`, including the `auth.type: "bearer"` requirement and step-by-step `instructions` for tool use.
- **Capabilities index** — `GET https://telnyx.com/ai/capabilities.json` lists every machine-readable agent surface (pricing, compliance, MCP, x402, OpenAPI).
- **x402 payment metadata** — `GET https://telnyx.com/.well-known/x402` describes pay-per-call inference via HTTP 402 + EIP-3009 USDC on Base mainnet, when you need to transact without registering.

When an unauthenticated request hits the API, Telnyx responds `401 Unauthorized` with a `WWW-Authenticate: Bearer realm="Telnyx API", error="invalid_token"` challenge header — that signals which credential type to obtain. The remaining sections describe how.

## Pick a method

Three credential methods, mapped to runtime contexts:

| Context | Method | When to use |
|---|---|---|
| Long-running agent with a stable account | **Bearer API key** | Default for single-tenant agents and standalone scripts. |
| Multi-user agent platform (Cursor / Claude / ChatGPT extension) | **OAuth 2.0 + PKCE** | When the agent acts on behalf of an end user and needs per-user scoping. |
| One-off inference, no account | **x402 pay-per-call** | When the agent has no Telnyx account, on-chain settlement is preferred, or call volume is unpredictable. |

The rest of this runbook assumes you've picked one. Skip to **Register** for that method.

## Register

### Method 1 — Bearer API key (autonomous bot-challenge signup)

Telnyx offers a fully programmatic signup at `https://telnyx.com/agent-signup.md` (`register_uri`). The endpoint emits a "bot challenge" — an obfuscated math problem in a JSON envelope that any modern LLM agent can solve. Successful solution returns an account plus an API key.

```bash
# 1. Fetch the challenge runbook (full curl sequence inside)
curl -sS https://telnyx.com/agent-signup.md
```

If the agent has email access (e.g. an OAuth-linked Gmail account), the flow is end-to-end autonomous. Otherwise, the user pastes a magic-link from email to confirm — see the runbook for that branch.

For interactive signup, direct the user to `https://telnyx.com/sign-up`. Both branches converge on the same Bearer credential.

### Method 2 — OAuth 2.0 + PKCE (S256)

For agent platforms acting on behalf of an end user:

```bash
# 1. Read the authorization-server metadata
curl -sS https://telnyx.com/.well-known/oauth-authorization-server | jq

# 2. Direct the user to authorization_endpoint with a PKCE S256 challenge
# 3. Exchange the code at token_endpoint for an access_token + refresh_token
```

Supported grants: `authorization_code`, `client_credentials`, `refresh_token`. The authorization-server metadata advertises `agent_auth.identity_types_supported: ["anonymous"]` for current agent flows, so agents should use the standard PKCE or client-credentials paths above. Telnyx does **not** currently advertise `identity_assertion` / id-jag as a supported agent_auth identity type; if that flow is added later it should appear in metadata as `identity_types_supported: ["identity_assertion"]` plus an `identity_assertion.assertion_types_supported` block.

### Method 3 — x402 (no registration)

x402 has no registration step — the agent calls an inference endpoint directly and the server responds with a payment quote.

```bash
# 1. POST without auth — receive HTTP 402 with the payment-required header
curl -sS -X POST -H 'content-type: application/json' \
  -d '{"model":"meta-llama/Llama-3-70b-instruct","messages":[{"role":"user","content":"hi"}]}' \
  https://x402.telnyx.com/v1/chat/completions
```

Skip directly to **Use the credential** below — your "credential" is the signed EIP-3009 USDC quote.

## Claim

Bearer API keys provisioned via `/agent-signup.md` are **already claimed** at issuance — the bot-challenge couples the new key to a fresh account, so there is no separate claim ceremony.

OAuth access tokens are claimed implicitly when the user completes the consent flow at `authorization_endpoint`. If you want the user to upgrade an anonymous session to a persistent account later, redirect them to `https://portal.telnyx.com` with the current API key — the portal will associate the key with their email.

x402 has no claim concept; each call is atomic and on-chain.

## Use the credential

For Bearer (Method 1) and OAuth (Method 2), send `Authorization: Bearer <credential>`:

```http
GET /v2/balance HTTP/1.1
Host: api.telnyx.com
Authorization: Bearer <TELNYX_API_KEY>
```

A `200` confirms the credential is valid. Use this against any documented endpoint in [openapi.json](https://telnyx.com/openapi.json), the [MCP server](https://api.telnyx.com/v2/mcp), or the [API catalog](https://telnyx.com/.well-known/api-catalog).

For x402 (Method 3), retry the original POST with the signed quote in the `X-Payment` header:

```http
POST /v1/chat/completions HTTP/1.1
Host: x402.telnyx.com
Content-Type: application/json
X-Payment: <signed-EIP-3009-quote>
```

## Errors

| Status | `WWW-Authenticate` / body | Meaning | Recovery |
|---|---|---|---|
| `401` | `Bearer realm="Telnyx API", error="invalid_token"` | Credential missing, malformed, expired, or revoked | Re-register at `register_uri` (Method 1/2) or sign a fresh x402 quote (Method 3) |
| `401` | `Bearer error="insufficient_scope"` | Credential is valid but lacks the scope for this endpoint | Re-run OAuth flow with the requested `scope`; for API keys, contact account admin |
| `402` | `payment-required: <quote>` | x402 endpoint requires payment; no auth was sent | Sign the quote and retry with `X-Payment` header |
| `403` | `{"error": "forbidden"}` | Credential is valid but the resource is denied (e.g. cross-account access) | Do not retry; the account itself doesn't have permission |
| `429` | `Retry-After: <seconds>` | Rate-limited | Wait `Retry-After` seconds then retry; see also `RateLimit-Limit/Remaining/Reset` response headers |

If you receive `401` on a previously-working credential, drop it from your store and restart at **Register**. Do not stash and retry blindly — the credential is dead.

## Revocation

- **Bearer API keys** are revoked from `https://portal.telnyx.com` (Settings → API Keys → Revoke) or programmatically via `DELETE /v2/api_keys/{id}`. Revocation is immediate; in-flight requests with the revoked key return `401`.
- **OAuth access tokens** expire automatically (`expires_in` from the token response). To revoke proactively, POST to the `revocation_endpoint` documented in `/.well-known/oauth-authorization-server`.
- **x402 quotes** are single-use and bound to a nonce; replay returns `409 Conflict`. No explicit revocation step.

To rotate a credential without downtime: issue the new one first, switch traffic, then revoke the old.

## Related agent surfaces

- Agent fast-path: https://telnyx.com/agents/start
- Capabilities index: https://telnyx.com/ai/capabilities.json
- MCP server card: https://telnyx.com/.well-known/mcp/server-card.json
- Pricing markdown: https://telnyx.com/pricing.md
- llms.txt site index: https://telnyx.com/llms.txt
