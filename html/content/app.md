## Generative UI: what actually runs

The native `GenerativeUI` provider exposes `generate_prefab_ui(code, data)`, optional Prefab component lookup and the renderer resource. It executes Prefab Python in its sandbox and returns a rendered application representation. It is a renderer/validation layer—not an LLM agent, a Telnyx account client, or a workflow engine.

### The generation lifecycle

1. The existing host agent or configured facilitator decides what the user needs to see.
2. It discovers Telnyx operation schemas and Prefab components on demand.
3. It writes Prefab Python into the generator's `code` argument, using documented imports and the `PrefabApp` outer context.
4. An Apps-capable host loads the directly advertised renderer resource. If the host forwards partial arguments, the browser renderer progressively executes code that compiles and displays a preview.
5. The server executes the finished code in its own sandbox for validation. The final validated result replaces the preview.
6. Native UI actions call scoped server tools and place results in local UI state. Subsequent user requests may generate a revised view.

Browser-side streaming requires a supporting host. The final render is still the required fallback. The native implementation depends on Prefab and server-side Deno/Pyodide support and permits only the documented sandbox environment. Do not suggest importing a Telnyx SDK or arbitrary Python package inside generated code.

### Tool chaining and UI action chaining are different

**Agent tool chaining:** native `execute` calls backend tools sequentially and returns a compact outcome. It belongs on the server's bounded execution path.

**User interaction chaining:** Prefab actions such as CallTool, SetState and ShowToast compose a click/submission workflow. For example, a form calls a backend tool, puts the returned result into UI state, and shows success or an actual failure. These actions run through the authenticated app bridge, not through another model reasoning turn.

**Durable activity:** a meeting observer, report, embedding job or number-order wait is native task/provider-job work. It outlives a particular generated view and cannot be implemented by a browser animation or an execute script that sleeps indefinitely.

### Data stays out of the model when possible

For large account lists, generate a view that queries a page through native CallTool and stores it in UI state. Avoid asking the model to retype account records into the generator's `data` argument. Small already-available values may use `data`; the native API supports that explicitly. There is no verified native data-handle resolver, so the plan does not invent one.

The UI uses table pagination and selected fields; an export/download is an explicit action. A summary given to the model is not a substitute for the actual underlying records, and hiding a payload from a text response must not make it impossible for the authorized UI/client to retrieve it.

### One workspace, reusable domain views

FastMCPApp groups UI entry points and backend tools with native composition-safe references. Prefer common list/detail/form/action patterns, plus focused recipes for channels, AI and storage, rather than separately deploying a small application for every endpoint.

The Store is the catalog/navigation view. Favorites affect the user's workspace; they do not expand the model's four-tool listing. The Omni Inbox is a source-aware view across available provider records and verified events, not a new native Telnyx unified-conversation API. It shows partial/unavailable/history-not-loaded status rather than manufacturing a complete timeline.

### Embedding with the official bridge

```text
Existing application
  ├─ its user session and design tokens
  ├─ its existing agent OR the native Telnyx facilitator
  ├─ backend: FastMCP Client (user-scoped connection)
  └─ frontend: official AppBridge + sandboxed renderer
       ├─ input / partial input / final result notifications
       ├─ UI tool and resource requests → authenticated backend
       └─ host theme, dimensions, capabilities, teardown
```

AppBridge supports a connected JavaScript MCP client or a host-supplied handler path with `new AppBridge(null, hostInfo, capabilities)`. The latter fits a Python FastMCP client in the application's backend. It is documented application glue—not a new iframe protocol. The official basic-host example supplies the security and lifecycle starting point.

The integrator passes a container, user connection, supported capabilities and theme values. The adapter mounts a requested domain view or the full workspace, connects input/result lifecycle, and closes owned resources on unmount. The parent application retains its navigation and agent. A React wrapper can be thin convenience; it must not become a second implementation of the renderer.

### Design systems from the first render

The application supplies tokens for foreground/background/surfaces, accent and semantic colors, typography, border radius, spacing and color mode. The adapter maps those values to supported MCP host styles and native Prefab Theme/CSS. Recipes use semantic tokens instead of a fixed Telnyx-branded palette.

The proof is the same view mounted in two visually different applications, with computed-style checks and screenshots, plus a runtime theme change. Fonts must be bundled or allowed by the host's CSP. Parent application CSS does not magically cross the iframe boundary, and arbitrary proprietary component libraries do not become Prefab components by naming them.

### Live voice and video surfaces

Use Telnyx's official browser SDKs in a stable developer-authored media component. Generative views control the workflow around it. A new model response or theme switch must not destroy and recreate an active peer connection.

MCP Apps may request microphone/camera through ResourcePermissions. The host may honor or deny that request; browser permission, autoplay, network reachability, ICE and SDK compatibility also apply. We test capabilities per host. A successful request to start a call is not proof of audible audio or supervisor routing. A recording player is not live video participation.

Telnyx Rooms are supported as their own video product: room creation, participant management, join tokens, SDK participation, recordings/compositions and related workflows. The meeting bot stays on existing Zoom/Meet/Teams/Webex platforms; no native bot-in-Telnyx-Room integration is planned.

### Action safety and failure UI

Approval, Choice, FormInput and FileUpload are existing framework primitives. Use them for relevant interactions, but enforce permission and authorized execution on the server. A pretty Approval card cannot be the only security boundary. Decline/cancel must leave the operation unexecuted.

Every view exposes pending, empty, partial, denied, failed and successful state as appropriate. If an operation is registered but disabled because it needs an unvalidated adapter, the Store explains why; enabling a checkbox does not implement that adapter. No mock, schema inventory or screenshot is used as proof that a fax delivered, an AI model trained or a meeting bot spoke.
