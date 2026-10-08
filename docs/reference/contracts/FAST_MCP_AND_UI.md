# Fast MCP and UI Contract

Resolved stack: fastmcp4.0.10, mcp2.2.0, prefab0.20.2, ai7.0.127, @ai-sdk/mcp2.0.66, @modelcontextprotocol/ext-apps2.0.3.

Authoritative type/declaration references:
- fastmcp docs snapshot: docs/reference/fastmcp/pages and docs/reference/fastmcp/client
- ai/mcp public declarations: docs/reference/ai-sdk/agent-public-types.d.ts, docs/reference/ai-sdk/mcp-public-types.d.ts, package metadata
- ui bridge types: docs/reference/mcp-apps/app-bridge-public-types.d.ts

Rules:
- Use public exports from the declarations above. Do not invent imports, renderer props, or wire aliases.
- Preserve structuredContent/metadata/UI resource wiring exactly; renderer output is not substitute for tool data.
- Rejected: Pydantic-AI result-mapping facilitator, patching app CSP to expose Prefab scripts, custom generative renderer, Meeting Bot in Telnyx Rooms.
