# Tim: build-or-pivot verdict

## Verdict

**Tim... I can build this.** The requested product has a framework/SDK-backed architectural path. The original facilitator/host choices need a bounded correction; the FastMCP server, Python client, native tool chaining and native Generative UI do not need to be replaced.

This is a feasibility conclusion supported by primary-source review and executed SDK/browser fixtures—not a claim that the complete Telnyx product is implemented, every API entitlement is active, all hosts grant microphone access, or production scalability has already been measured.

## Supported stack

1. **Server:** FastMCP OpenAPIProvider plus its native naming/mapping/policy extension points; native CodeMode Search/GetSchemas/execute; directly exposed GenerativeUI. Native tasks/state/auth/lifespan continue to supply the runtime features. Source count and enabled coverage remain distinct. [S11,S21,O5]
2. **Python client:** fastmcp.Client remains the full integration/client-capability surface. Do not replace it with the AI SDK's intentionally lighter MCP adapter; notifications, resumable streams and task handling need the native client path as planned. [S1,S22; installed SDK client limitations]
3. **Application facilitator:** native AI SDK ToolLoopAgent plus released @ai-sdk/mcp metadata-preserving tools. Existing applications with their own agent can keep it. Model-provider configuration uses an existing compatible-provider factory, not a new Telnyx provider implementation. Actual model choice/availability and behavior require account integration testing. [S5,S6,S8-S10,S23,O7]
4. **Generated UI:** unchanged FastMCP GenerativeUI and actual Prefab validation/renderer. Isolated official Deno with documented dependency setting is part of the proven fixture environment. [S11-S13,O6]
5. **Embedding host:** official @modelcontextprotocol/ext-apps AppBridge and maintained basic-host sandbox/CSP implementation, not the tested experimental React renderer. This host rendered the actual generated fixture. [S14-S17,O9]
6. **Voice/video:** official Telnyx SDKs; stable SDK connection surfaces with generated workflow controls. External-host permissions and actual media routing are deployment conditions, not reasons to implement RTP/WebRTC ourselves. [S19,S20]
7. **Stores:** native runtime backends for Docket/OAuth/events; requested Telnyx KV adapter uses native BaseStore/ManagedEntry primitives plus provider SDK calls at documented extension seams, not homemade distributed semantics. [S21,O13]

## Executed evidence

- The HTTP server listed exactly execute, generate_prefab_ui, get_schema and search. Native CodeMode invoked the child arithmetic tool and returned7. [probe-js-result.json]
- Native ToolLoopAgent invoked the generator using its provided model fixture; the actual server-side Deno/Pyodide validation returned isError=false and a $prefab0.3 view. [probe-js-result.json]
- The UI-message output retained the raw structured result plus the app renderer URI, mimeType and CSP. Online examples' metadata nesting differed from the released source; release-matched code was used. [probe-js-result.json]
- A real browser initialized the official two-origin sandbox/AppBridge and displayed the inner heading and body from that actual generated artifact. No browser errors occurred in the final run. [browser-render-proof.png; observation O9]
- Declared host style variables reached the inner document. Full arbitrary-component design-system equivalence is not claimed; native Theme/CSS token configuration remains required. [O10]

## Paths rejected rather than patched

**Pydantic standard mapped-result path:** maintainer source drops metadata; the upstream Apps issue is open. Do not invent automatic preservation or quietly fork the SDK. [S2,S3]

**AI SDK experimental React renderer for stock Prefab assets:** installed CSP omits resource domains for script/style loading; browser blocked native assets. Do not patch SDK code or strip security. Official AppBridge host is the verified alternative. [S7,O8,O9]

**Telnyx Assistant Chat as widget-event transport:** its documented response is text, not a UI result stream. Keep it for native Telnyx assistant operations and meeting/voice use; do not rely on undocumented output events for application hosting.

## Product acceptance still required

Real-user OAuth consent/registration, account entitlements, chosen Telnyx model quality/tool behavior, controlled fax/call/meeting delivery, target-host mic/camera, concurrent identity isolation, persistence/restart and production load are integration/acceptance tests. None were performed using the exposed transcript key. They remain explicit gates, not architectural permission to write speculative engines.

No claim of zero application code: SDK configuration, documented handlers, authorization policy and domain UI definitions are necessary. No new discovery engine, agent loop, iframe protocol, renderer, queue or media implementation is necessary for the recommended path.

## Research limits and provenance

Five research delegates timed out with no useful returns; no independent reviewer approval is claimed. Primary-source and installed-release inspection, native SDK execution and real browser observations are the actual evidence. The source ledger, claim graph, intent diff and probe artifacts enumerate supported/refuted statements. Root HTML dossier has not been regenerated with these findings and still contains the previous facilitator proposal; do not treat it as the final corrected architecture until revised.

## Addenda

- 2026-10-07: [domain apps, background tasks, storage](DECISIONS_2026-10-07_apps_tasks_storage.md) — executed findings on FastMCPApp visibility, TasksExtension, encrypted OAuthProxy storage, and the rejected Telnyx KV store adapter.
- 2026-10-08: [live Telnyx OAuth acceptance](DECISIONS_2026-10-08_live_oauth.md) — schema scope `admin` rejected live (scopes now from RFC 8414 metadata), introspection rate limit (5/60 s) requires the documented introspection cache, full localhost login + BYOK `execute` verified.
