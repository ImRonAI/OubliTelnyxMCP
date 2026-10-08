## A client that reuses FastMCP rather than replacing it

The client package is the reusable integration surface for applications and services. Its core is `fastmcp.Client`, with small typed configuration and documented lifecycle helpers. It is not another implementation of the MCP transport, another generic Telnyx executor or a new agent framework. The browser rendering bridge is a separate official JavaScript surface.

### Three integration modes

| Mode | Who supplies the agent | Who holds the credential | How UI appears |
|---|---|---|---|
| Existing MCP host | Claude or the connecting host | Its authenticated connection and our server's upstream binding | Host renders `ui://` resources and generator results when supported. |
| Existing application's backend | The integrator's existing agent, if any | Backend connection scoped to that application's user | Official AppBridge mounts views in the application and forwards tool/resource requests. |
| Standalone Oubliai workspace | User-owned Telnyx facilitator assistant | User-scoped backend connection; secret references where documented | Native agent-to-UI delivery must pass its compatibility gate; text chat alone does not prove it. |

An integration may embed a single fax, email or RAG panel instead of the entire workspace. Applications do not need to adopt the Store navigation, host a second agent, or expose a long-lived Telnyx key to the browser in order to use the same operations.

### Native client feature coverage

| Capability | Benefit to the server | Benefit to the application |
|---|---|---|
| HTTP transport and protocol negotiation | Repeatable transport-level conformance | One managed connection instead of handwritten JSON-RPC. |
| Tools and structured results | Accurate errors, schemas and metadata testing | Same outcomes for human actions and agent calls. |
| Resources, templates, prompts and completion | Reference/workflow surfaces remain discoverable | UI resource loading, instructions and scoped suggestions. |
| Progress and logs | Observable long-running work | Progress display without conversation flooding. |
| Elicitation handlers | Negotiated requests get explicit outcomes | User approval/input handled as an application interaction. |
| Sampling and roots handlers | Capability-aware server behavior | Integrator may supply its own model or permitted local context. |
| Tasks/status/results/cancel | Native job lifecycle is exercised | Client polls and cancels tasks instead of making the agent wait. |
| OAuth/bearer authentication | Test identity boundaries and renewal | BYOK key and OAuth entry modes with correct audience handling. |
| Caching/version selection | Compatibility and private-cache tests | Safe repeated reads where declared, stable integration behavior. |
| Notifications and ClientGroup | Optional multi-service interoperability | Integrator can opt into its existing services without a default Telnyx proxy. |

### Credentials: two boundaries, not one magic token

An MCP-facing OAuth credential proves access to Oubliai's resource. A Telnyx credential authorizes the upstream account. They may be related through a documented OAuth exchange, but they are not assumed identical. A token issued for another audience must not be accepted because it happens to have a valid signature.

BYOK does not establish account entitlements. A key may be valid while a product operation is unavailable or forbidden. A failed balance request could be a permission or transient/rate-limit condition rather than an invalid key. Verification must distinguish those states. The server necessarily processes requests and responses; the product cannot honestly claim the operator sees nothing simply because the user's key is used.

### The facilitator is an existing agent runtime

When another MCP host connects, its model already acts as the facilitator. For the standalone workspace, use a Telnyx AI Assistant and its native chat/MCP-tool configuration. The facilitator can discover operations, explain outcomes, request user input and generate a view. Native Missions may orchestrate supported autonomous workflows. Native FastMCP Tasks run server work. These are different responsibilities, not three queues that need to be invented.

The local assistant chat schema exposes required `content` and `conversation_id`, optional `stream`, and a response containing `content`. Its streaming description promises text `delta`, `done` and `error`. It does not document an MCP Apps tool-result stream. Therefore automatic routing of the assistant's generator artifact into the embedded host is not confirmed yet.

### Facilitator compatibility gate

Before calling the standalone agent-driven UI complete, prove this chain with recorded evidence:

1. User starts a native assistant conversation with that user's account.
2. Assistant discovers and invokes the compact Oubliai MCP tools using a documented, user-bound integration credential.
3. The server makes a permitted Telnyx request for the same account.
4. The assistant returns the real outcome, with refused operations remaining refused.
5. The generated UI artifact or actual tool event reaches AppBridge, including the necessary renderer resource and input/result lifecycle.

A successful text reply proves only text chat. If the native runtime omits the UI payload we need, document that integration gap. Do not quietly replace the native runtime with a handmade tool loop and still describe the result as framework-native. Existing applications that already provide an agent can pass their actual tool-call inputs/results to AppBridge directly through the documented host interface.

### Polling and teardown are application work

Task progress, meeting transcripts and call state do not need to be added to the language model's history on every tick. Keep provider cursors in the user-scoped observer/client state; show current state in the UI; summarize only when asked or when an authorized rule requires it. Preserve cursors when an empty response supplies no new position.

Every connection, bridge, interval, observer and browser media resource has an owner and a close path. A reconnect must not switch identity, reuse another user's cache, duplicate a message or silently recreate a billable call. The implementation tests both successful operation and cancellation, permission denial, missing capabilities and connection loss.
