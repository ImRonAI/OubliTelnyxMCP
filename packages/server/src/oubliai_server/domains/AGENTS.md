# Server Guidelines

Work from this package or the exact assigned child directory; inherit root guidance. Own FastMCP server composition, Telnyx operation mapping, execution-time authorization, async client lifecycle and runtime stores/tasks. Do not add an application agent loop here.

## Documented contracts
FastMCP's OpenAPI documentation states: “By default, FastMCP converts **every endpoint** in your OpenAPI specification into an MCP **Tool**.” Use `OpenAPIProvider` or `FastMCP.from_openapi()`, not a handwritten endpoint catalog/executor. Source: `docs/reference/fastmcp/pages/openapi-integration.md`, Create a Server / Route Mapping; official https://gofastmcp.com/integrations/openapi.

The native CodeMode documentation defines `search`, `get_schema`, `execute`. Keep these on the operations composition and expose native `GenerativeUI` outside that transform to preserve directly advertised UI metadata. Sources: `docs/reference/fastmcp/pages/code-mode.md`; `docs/reference/contracts/FAST_MCP_AND_UI.md`; verified research result in VERIFIED_DECISIONS. Do not stack competing catalog replacement transforms by default.

Native HTTP deployment supports `mcp.http_app()` and explicit parent lifespan propagation. Custom HTTP routes do not automatically inherit MCP auth. Sources: `http-deployment.md`, ASGI Application / Health Checks / Integration with Web Frameworks.

## Agent boundary
Map ordinary source operations once. Special hosts, WSS, SSE, binary/multipart and naming collisions require source-backed adapters/normalization and tests. Never count disabled entries as executable. UI/domain definitions live under this package's `apps`; browser hosting lives in the application package. Test commands must come from this package's actual manifest once present.

## Assigned directory
Project target: `packages/server/src/oubliai_server/domains`. Change into this directory before development. This copy is a planning template; the project scaffold is not installed until the worker applies it.
