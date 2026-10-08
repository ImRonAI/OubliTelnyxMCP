# OpenAPI Provider Guidelines

Own only source-operation indexing, documented normalization and native provider configuration. Work in this assigned directory; inherit root and server rules.

## Source contracts
Read `docs/reference/telnyx/openapi.json` for exact `(method,path)`, `operationId`, parameters, requestBody/content, responses, effective servers and security. Resolve `$ref` from the source; do not infer schema types from endpoint descriptions. Read `docs/reference/fastmcp/pages/openapi-integration.md` before configuring mapping or hooks.

Verbatim native mapping example:
```python
from fastmcp.server.providers.openapi import RouteMap, MCPType
RouteMap(mcp_type=MCPType.TOOL)
```
The documented types are `TOOL`, `RESOURCE`, `RESOURCE_TEMPLATE`, `EXCLUDE`; rules are ordered and the first match is used. The docs describe `mcp_component_fn` as an in-place hook: “The result of the function is ignored.” Source: OpenAPI integration, Advanced Customization.

Provider constructor/import details must be confirmed against pinned public exports before use. Keep original operation identity even where the MCP name is normalized/truncated. Verify duplicate naming and already-versioned path cases; do not blindly prepend `/v2` or assume client.base_url respects operation-level servers. Retain disabled-operation reasons and separate source/callable counts. Do not generate 1,382 custom Python wrappers.

## Assigned directory
Project target: `packages/server/src/oubliai_server/api`. Change into this directory before development. This copy is a planning template; the project scaffold is not installed until the worker applies it.
