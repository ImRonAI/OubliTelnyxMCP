# Repository Guidelines

## Working location and ownership
Change into the exact directory assigned to your task before searching, editing, or running package commands. Confirm `pwd`. Read this root file and every ancestor/local `AGENTS.md` for that directory. Paths in these guides are repository-relative; resolve them against the repository root, not your current directory. Do not edit another owner's package without coordination. The coordinator owns shared reference metadata and cross-package contracts.

## Mandatory source order
Read `docs/reference/SOURCE_INDEX.md` and `docs/architecture/VERIFIED_DECISIONS.md`. Use the selected package's installed public API/types and pinned reference snapshot before writing code. For Telnyx requests, the canonical schema is `docs/reference/telnyx/openapi.json`; follow its operation, request, response and security references. Documentation from another release or SDK generation is not a valid substitute. If no supported contract exists, record the blocker and stop; do not invent signatures, fields, event names, tools or behavior.

## Framework/SDK-only architecture
The server and full Python client use standalone FastMCP. The application facilitator uses native AI SDK `ToolLoopAgent`; UI uses native FastMCP `GenerativeUI`/Prefab and official MCP Apps AppBridge. Use documented configuration, public SDK calls and extension hooks. Do not implement another discovery engine, agent loop, renderer, iframe protocol, media stack or queue. Keep default model-visible discovery to `search`, `get_schema`, `execute`, `generate_prefab_ui`; app-only tools are a separate visibility category, not permission bypasses.

## Safety and evidence
BYOK requests must stay bound to the connected user's account. Never copy transcript credentials into files, prompts or logs. No live purchases, message sends, calls, DNS changes or destructive tests without explicit authorization. Registered-disabled operations are not working coverage. SDK fixtures prove mechanics, not live delivery or load performance. Preserve the existing root HTML dossier and original schema files.

## Commands and status
This initialization creates documentation and folders only. Product manifests/scripts/tests do not exist merely because a folder exists. Derive build/test commands from the package's actual manifest when implemented; do not invent successful command output. Root HTML/source-plan still require the verified facilitator/host corrections documented in VERIFIED_DECISIONS.

## Assigned directory
Project target: `.`. Change into this directory before development. This copy is a planning template; the project scaffold is not installed until the worker applies it.
