# Authentication Guidelines

Own user-bound authentication/authorization only; work in this assigned directory. Inherit root/server rules. No custom OAuth server or token lifecycle if the native provider covers the requirement.

Read `docs/reference/fastmcp/pages/auth.md`, `authorization.md`, `http-deployment.md`, selected-release token/OAuth reference snapshots, and `docs/reference/contracts/FAST_MCP_AND_UI.md`. Telnyx issuer metadata lives in `docs/reference/telnyx/oauth-authorization-server.json`; it advertises a service, not proof that it issues a token for our audience.

Native provider options are `TokenVerifier`, `RemoteAuthProvider`, `OAuthProxy`, `MultiAuth` and the selected public verifier APIs. Choose direct remote verification only with correct issuer/audience/resource evidence. Never disable audience checks. MCP-facing and upstream credentials are distinct. The verified FastMCP4 OAuthProxy source swaps the validated proxy token for an upstream `AccessToken`; use that documented framework behavior rather than copying private store lookups.

The authorization docs describe scope/role checks and explain that visibility/list filtering is not the complete execution check. Enforce the operation on search, execute, direct calls, resources and UI actions. A successful key validation does not invent all scopes or account entitlements. Never mutate one shared client's Authorization header across concurrent users. Native request dependencies carry this user's verified access context.

Record good/expired/wrong-audience/wrong-user/missing-grant behavior; distinguish transient/429 validation failure from valid authentication. No credentials in examples, logs or reference snapshots.

## Assigned directory
Project target: `packages/server/src/oubliai_server/auth`. Change into this directory before development. This copy is a planning template; the project scaffold is not installed until the worker applies it.
