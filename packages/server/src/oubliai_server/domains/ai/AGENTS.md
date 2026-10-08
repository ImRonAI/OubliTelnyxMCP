# Domain Guidelines

Work in the assigned domain directory; inherit root/server/domain-parent guidance. This scope is generated Telnyx tools plus narrowly justified SDK/framework configuration and workflow prompts, not another implementation of the REST API.

## Exact source contract
Read `docs/reference/telnyx/domains/ai.md` and the canonical `docs/reference/telnyx/openapi.json`. For every operation follow its exact method/path, `operationId`, parameters, requestBody media type, response schema, effective server and security, including `$ref` definitions. Friendly names in plans are not guaranteed registered MCP names. Obtain them from the verified operation mapping.

Types and fields come from schema and selected SDK public declarations. Do not invent endpoint names, default model IDs, reply threading, webhook names/signatures, permissions, pagination cursors, idempotency or server state transitions. Domain reference pages must retain JSON pointers to source; summaries are navigation aids, not replacement contracts.

Reuse native OpenAPIProvider execution and official SDKs for non-REST protocol gaps. Use native progress/tasks only according to their negotiated framework behavior. Do not count registered-disabled protocols as implemented. Distinguish accepted, pending, completed, failed and unverified delivery based on real provider outputs. No live external side effects in generic tests. A common inbox retains explicit source/provider IDs; automatic cross-channel identity/history is not an established provider feature.

## Domain-specific restriction
Native assistants, AI Voice, Missions, tools/MCP servers, inference, memory and insights. Hosted Assistant Chat text is not a widget-event transport; app facilitator configuration belongs to the app package.

## Assigned directory
Project target: `packages/server/src/oubliai_server/domains/ai`. Change into this directory before development. This copy is a planning template; the project scaffold is not installed until the worker applies it.
