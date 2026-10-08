# Runtime Guidelines

Own documented lifespan, task, session/cache/event-store and observability configuration. Inherit root/server guidance and work here before commands/edits.

## Exact framework contracts
From `docs/reference/fastmcp/pages/tasks.md`, Enabling Background Tasks:
```python
from fastmcp_tasks import TasksExtension
mcp.add_extension(TasksExtension())
```
“Only tools can be task-enabled; resources, resource templates, and prompts do not carry `task=`.” Background task tools require async functions; negotiated protocol behavior must be read for the pinned release. Do not copy FastMCP3 task imports into FastMCP4 code.

CodeMode has bounded time/memory/call limits; it is not an hour-long meeting observer or durable transaction. Use native TasksExtension/Docket for supported job execution. EventStore replay, application session state and a task queue are different responsibilities. Sources: `tasks.md`, `code-mode.md`, `sessions.md`, `storage-backends.md`, `lifespan.md`, `telemetry.md`.

The installed native `BaseStore` owns managed-entry timestamps and expiry behavior; the account KV adapter may use those framework hooks and official SDK calls, but cannot invent atomic CAS, distributed locks or a Docket backend. Use native persistent stores for multi-worker runtime needs. Cache only safe reads with principal/authorization/input/version partitioning. No blind retries of ambiguous mutations. Read middleware docs and use the shortest sufficient native stack; do not implement a parallel log/cache/rate-limit framework.

## Assigned directory
Project target: `packages/server/src/oubliai_server/stores`. Change into this directory before development. This copy is a planning template; the project scaffold is not installed until the worker applies it.
