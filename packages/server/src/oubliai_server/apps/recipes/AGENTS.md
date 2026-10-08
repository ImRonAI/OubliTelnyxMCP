# Server-side FastMCP App Guidelines

Work here; inherit root/server guidance. Own native FastMCPApp providers, Prefab domain views/actions and directly exposed native GenerativeUI. Application browser hosting belongs to `packages/app`.

`docs/reference/fastmcp/pages/fastmcp-app.md` states `@app.ui()` entries return a `PrefabApp` and default to `visibility=["model"]`; `@app.tool()` backend tools default to `visibility=["app"]`, with `model=True` for both. `CallTool` supports a name or function reference; references resolve composition safely. These defaults do not bypass authorization or authorize a fifth model-visible tool. Follow the approved root discovery composition.

Read exact installed Prefab types and `docs/reference/prefab/` before using components, actions, `STATE`/`RESULT`, Theme or app fields. Use native FormInput/Approval/Choice/FileUpload when their documented contracts fit. Do not invent component props, transform result handles, or renderer events.

The documented `GenerativeUI` arguments are `tool_name`, `include_components_tool`, `components_tool_name`; its native tool accepts `code` and `data`. There is no verified `tool`/`arguments` fetching parameter on that native generator. Sources: `docs/reference/contracts/FAST_MCP_AND_UI.md`; https://gofastmcp.com/apps/generative. Large data should load through supported CallTool/UI state; do not add a custom generative execution engine. Recording player UI is not live audio/video proof.

## Assigned directory
Project target: `packages/server/src/oubliai_server/apps/recipes`. Change into this directory before development. This copy is a planning template; the project scaffold is not installed until the worker applies it.
