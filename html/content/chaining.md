## The server is the platform boundary

The server is not a new Telnyx SDK. Its central implementation is FastMCP's existing OpenAPIProvider, configured with the pinned Telnyx schema, reusable asynchronous HTTP clients, native mapping hooks, execution-time authorization, and lifecycle management. That creates a source-traceable catalog without writing a wrapper for every REST operation. Custom code is confined to application policy and documented protocol gaps.

### How a request travels

1. The client authenticates to the Oubliai MCP resource. The server resolves the user's upstream Telnyx connection without conflating an Oubliai OAuth access token with a Telnyx token.
2. The agent searches the authorized catalog. Native Code Mode provides a compact, request-scoped tool search. It receives only selected candidates, not 1,382 full tool definitions.
3. The agent requests parameter details for the chosen tools. Native GetSchemas can return compact descriptions or the complete schema when the operation requires it.
4. The agent invokes native execute. Inside its bounded sandbox, `await call_tool(name, arguments)` resolves the actual registered tool through the normal execution pipeline. The native OpenAPI tool serializes the path, query, headers and body, then makes the Telnyx request with this user's credential.
5. The execution returns a selected outcome. The agent can return identifiers and counts rather than replaying every intermediate response into the conversation.
6. A UI action can use the same operation directly through the client and AppBridge. Clicks do not need to become extra conversational agent turns.

### The four model-visible tools

| Tool | Native responsibility | Why it earns a place |
|---|---|---|
| `search` | Native Code Mode Search | Find the appropriate operations and component reference tools on demand. |
| `get_schema` | Native Code Mode GetSchemas | Retrieve the contracts for only the chosen tools. |
| `execute` | Native CodeMode/Monty | Chain calls and compute a small final answer without exporting all intermediate data. |
| `generate_prefab_ui` | Native GenerativeUI provider | Directly advertised UI metadata allows an Apps-capable host to load the renderer. |

The operations child carries Code Mode. The root exposes the generator outside that transform. A no-network probe against installed FastMCP 4.0.10 produced these four names, preserved `ui.resourceUri` on the generator, and executed an arithmetic tool through the child. Its listing was 6,527 bytes. This is proof of the small composition, not proof of all Telnyx operations, browser rendering or facilitator integration.

### Chaining example: execute a query, keep the intermediate data local

The following is **illustrative planned use**, not a claim of a live Telnyx run. MCP-safe names must come from the generated mapping, and actual argument constraints must be obtained from the source schema.

```python
# Within FastMCP's native execute sandbox:
result = await call_tool("ListPhoneNumbers", {
    "page": {"number": 1, "size": 20}
})
numbers = result.get("data", [])
return {
    "page_count": len(numbers),
    "numbers": [item["phone_number"] for item in numbers],
    "pagination": result.get("meta", {})
}
```

Native chaining is sequential where data dependency requires it. It is not a transaction: if the second of three remote mutations fails, FastMCP does not roll back Telnyx. If Telnyx offers an idempotency key or `command_id`, use that operation's actual contract. Never retry an ambiguous billable or destructive action solely because the MCP connection timed out.

### Chaining example: establish a call, then manage it as a live process

The intended workflow is discover the dial/assistant/transcription operations, submit the authorized call request, capture its provider IDs, and wait for evidence of the actual call lifecycle. Subsequent commands target those IDs. Starting an assistant before its call is ready is not assumed safe; readiness comes from documented status or events.

An hour-long call or meeting must not run inside the 30-second Code Mode sandbox. The initiating operation returns its IDs. A native background task or application observer tracks provider state. The client/UI consumes progress and updates directly, while the agent receives only requested summaries or significant outcomes. This separates short tool chaining from durable activity.

### What context efficiency does—and does not—mean

The initial catalog is bounded. Search results default to five brief candidates; selected schemas are fetched as needed. Code execution can reduce intermediate results before returning them. UI data should load through native CallTool into UI state instead of being pasted through the model. Pagination stays pagination; truncation must not corrupt the declared output schema.

These mechanisms reduce context pressure. They do **not** make results free, guarantee zero context disruption, or guarantee that a host never injects tool results into its own conversation. The plan measures listing bytes, search payloads, selected schemas, returned summaries and model turns. A native generator accepts `code` and `data`; it does not provide an undocumented server-side data-handle resolver.

### Why not stack every discovery feature

FastMCP offers both search transforms and Code Mode discovery. Stacking replacements for the same catalog can hide tools behind another set of synthetic tools or lose the intended metadata boundary. The default uses one Code Mode discovery path. BM25SearchTransform and RegexSearchTransform are compatibility profiles, not additional default search layers. Their authorization behavior must match the default.

### Safety is not a tool annotation

Read-only/destructive/idempotent hints describe intended behavior. They are not permissions, approvals or enforcement. Authorization is checked when operations run, including direct calls, UI actions, resources and nested Code Mode calls. Approval UI must be connected to server-side execution policy; merely displaying a confirmation card is insufficient.

SQL queries, chargeable calls, message sends, number purchases, recording deletion, identity/routing changes and source ingestion have distinct effects. Policy must follow documented operations, not only the HTTP verb. In-memory tests cannot prove a real call was heard, a fax delivered, a meeting attended or a model trained.

### Scalability without another architecture

Load the schema once. Pool upstream clients by verified effective origin. Keep request identity in request-scoped dependencies rather than mutable global headers. Use native lifespans to own and close resources. Partition private caches by principal, authorization, input and version. Use native persistent backends for the runtime features that actually require them.

The Telnyx KV adapter is useful for account-owned preferences/documents. It is not assumed to provide atomic claims, distributed locks, Docket queues, native TTL or transactional isolation. Those are separate contracts and stay with supported runtime backends unless proven otherwise.
