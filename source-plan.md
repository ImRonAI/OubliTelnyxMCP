# telnyx-fastmcp-rewrite - Work Plan

## TL;DR (For humans)
<!-- Fill this LAST, after the detailed plan below is written, so it summarizes the REAL plan. -->
<!-- Plain English for a non-engineer: NO file paths, NO todo numbers, NO wave/agent/tool names. -->

**What you'll get:** A bring-your-own-key Telnyx workspace: one remote server, a reusable client, and interactive generative views that can be embedded in another application's UI. It covers communications including fax/email/video and external meeting bots, AI agents/voice/inference/training/RAG, and storage, with a facilitator using an existing agent runtime.

**Why this approach:** Build on FastMCP's OpenAPI provider rather than duplicating the Telnyx API. Native discovery and bounded code execution keep the full catalog out of the model's initial context; the native generator remains directly visible so hosts can render its UI.

**What it will NOT do:** Invent a new agent loop, queue, UI interpreter or authentication protocol. It will not put a meeting bot in Telnyx Rooms or claim host microphone access, OAuth compatibility, or assistant-to-widget delivery without the corresponding test evidence.

**Effort:** XL — full-platform integration, not a small wrapper.
**Risk:** High — native primitives are documented, but cross-runtime facilitator UI delivery, resource-bound OAuth and live media require early compatibility proofs.
**Decisions to sanity-check:** User-account credentials; four model-visible tools; one embeddable workspace; no default duplicate Telnyx MCP proxy; explicit separation of ordinary runtime persistence from the requested Telnyx KV adapter.

Your next move: review the compatibility gates and ordered build. Implementation belongs to a separate worker session; this document does not claim implementation has started.

---

> TL;DR (machine): XL / high integration risk; 6 waves, 27 implementation tasks, 4 final verification tasks; server -> client/facilitator -> domain workflows -> Generative UI/embed -> release evidence.

## Scope
### Must have

**Product:** an embeddable Telnyx communications and AI workspace, backed by one remote FastMCP server. A user brings their Telnyx credentials; an external agent or the workspace facilitator discovers and operates that account. The same tools power chat, interactive forms, dashboards, voice/video controls, and other applications embedding the workspace.

This document replaces `.omo/plans/telnyx-fastmcp-server.md` and all of its additive amendments. It is a build plan, not a claim that a server or UI already exists. Research baseline: local `openapi.json`, installed FastMCP 4.0.10, MCP 2.2.0, Prefab 0.20.2, and official documentation retrieved during this rewrite. Pin the compatible baseline; do not silently track `main` or claim a documentation example is a live integration test.

User decisions: domain `oubliai.com`; plan endpoint `https://oubliai.com/mcp` (no assumption of a separately approved subdomain); API-key and OAuth entry paths; Code Mode enabled; at most four model-visible tools; special/hidden endpoints registered but disabled; first-class communications, video, external meeting bot, facilitator, AI agents/voice/inference/training/RAG, and storage UI. Meetings bot is for Zoom/Google Meet/Teams/Webex, **not** Telnyx Rooms. Store means both a catalog UI and the requested Telnyx KV storage adapter.

### Evidence keys and reading order

| Key | Primary source | What it proves / limits |
|---|---|---|
| E1 | `openapi.json`, `paths`, `components`, `webhooks`; original `fastmcp-llms.txt` and `fastmcp-llms-full.txt` | Endpoint/schema inventory, not successful execution or account entitlement. Use `(method,path)` as operation identity, not operationId alone. |
| E2 | https://gofastmcp.com/integrations/openapi ; local `docs/fastmcp/openapi-integration.md`; installed `fastmcp/server/providers/openapi/{provider,components,routing}.py` | `OpenAPIProvider`, `from_openapi`, ordered RouteMap, name/component hooks, flattened schemas, client-based requests. |
| E3 | https://gofastmcp.com/servers/transforms/code-mode ; `docs/fastmcp/code-mode.md`; installed `fastmcp/experimental/transforms/code_mode.py` | Native Search/GetSchemas/execute, bounded Monty execution, intermediates stay in execution. Experimental API; does not promise persistent workflow execution. |
| E4 | https://gofastmcp.com/apps/generative ; installed `fastmcp/apps/generative.py:53-159` | Native generator takes `code` and optional `data`; registers renderer metadata and component lookup. No built-in LLM, tool-result-reference resolver, or Telnyx client inside the sandbox. |
| E5 | https://gofastmcp.com/apps/fastmcp-app ; `docs/fastmcp/fastmcp-app.md` | Provider composition; model/app visibility; function-reference CallTool resolution. Visibility is not a substitute for authorization. |
| E6 | https://modelcontextprotocol.io/extensions/apps/build ; https://apps.extensions.modelcontextprotocol.io/api/classes/app-bridge.AppBridge.html ; https://github.com/modelcontextprotocol/ext-apps/tree/main/examples/basic-host | Official embedding bridge and example sandbox host; tool/resource forwarding; input/result notifications. Use this rather than hand-rolled postMessage plumbing. |
| E7 | https://prefab.prefect.io/docs/styling/themes ; https://prefab.prefect.io/docs/reference/app ; installed `prefab_ui/app.py:123-176`, `prefab_ui/themes/base.py:113-222` | Theme/CSS/mode/assets; explicit token mapping is possible. Arbitrary parent-app CSS does not automatically enter an iframe. |
| E8 | `docs/fastmcp/{tasks,sessions,storage-backends,http-deployment,auth,authorization}.md`; https://gofastmcp.com/clients/client | Native task extension, Docket backends, user state, auth, client. Neither Telnyx KV nor EventStore is a substitute for Docket's queue. |
| E9 | `docs/telnyx-oauth-as-metadata.json`; https://api.telnyx.com/.well-known/oauth-authorization-server | Telnyx advertises OAuth/DCR/PKCE; does not prove issuance for Oubliai's resource/audience. |
| E10 | https://developers.telnyx.com/api-reference/assistants/assistant-chat-beta ; `openapi.json` assistant chat / MCP server / integration secret schemas | Existing assistant runtime and chat API. End-to-end MCP tool use, credential propagation and UI-result forwarding still need the compatibility gate. |
| E11 | `openapi.json` `/meeting_sessions*`; `/Users/tims-stuff/.agents/skills/telnyx-meeting-bot/SKILL.md`; https://github.com/team-telnyx/ai/blob/main/guides/meeting-bot.md | Third-party meeting lifecycle, assistant attachment, transcript/artifact contracts; not Telnyx Room bot integration. |
| E12 | https://github.com/team-telnyx/webrtc/tree/main/packages/js ; https://developers.telnyx.com/docs/development/webrtc/js-sdk/how-to/configure-network-firewall ; installed `fastmcp/apps/config.py:21-82` | Browser audio SDK and requested microphone permissions; host grants/network/device remain runtime conditions. |

### 1. Server first: use the OpenAPI integration as the implementation

1. Load the pinned spec once at startup. Build one canonical operation inventory; generate tools with `OpenAPIProvider`. Do not write 1,382 endpoint wrappers or a second generic HTTP executor.
2. Retain all source operations in the inventory, including OAuth protocol, hidden, experimental, alternate-host, SSE and WebSocket entries. Each has exactly one implementation disposition: native provider, native provider with documented normalization, narrow protocol adapter, or registered-disabled with reason. Count source paths and operations separately. Disabled is accounted-for, **not working**. Release reports callable coverage and disabled coverage separately.
3. The normalization layer is data-only and justified per exception: resolve effective server URL, version-prefix duplicates, duplicate/truncated names, and route metadata. Preserve the original spec. Use an explicit reviewed names map with collision checks; namespace+suffix lengths must fit host limits. Do not indiscriminately prepend `/v2` to already-versioned paths. Do not assume the supplied HTTP client honors path/operation `servers` overrides.
4. Reuse an async HTTP client per verified upstream origin and lifecycle; inject request-scoped credentials without mutating shared headers. RouteMap decides component type, component hooks attach source metadata/tags/annotations, and authorization runs at execution. Classify SQL/query POSTs and action endpoints explicitly: HTTP verb alone does not establish permission or safety.
5. Preserve output validation by default; record narrowly scoped exceptions supported by a failing contract test. Multipart, file bytes, downloaded PDF/audio, SSE and WebSockets get wire-format tests and official SDK/protocol adapters where the generic provider is insufficient. A WSS operation does not become callable merely by flipping Visibility.
6. Keep all ordinary Telnyx tools behind a native discovery transform; no duplicated proxy to Telnyx's hosted MCP. Original operation names stay traceable in the inventory even where an MCP-safe name differs.

### 2. Context discipline: a small catalog, bounded results

Target default model-visible surface: **`search`, `get_schema`, `execute`, `generate_prefab_ui`**. Use native CodeMode with native Search/GetSchemas on the operations provider/child server; keep the native generator outside that transform so its `_meta.ui.resourceUri` is directly advertised. Component lookup and domain backend tools remain discoverable behind Code Mode; UI-only backends remain available to authenticated app actions, not model discovery. The catalog/Store is a workspace page and resource, not a fifth pinned tool. Verify this composition before building domain UIs.

- Search: top five brief matches by default, with family tags; fetch compact schema only for chosen tools. Full schema is available explicitly. Do not expose ListTools over the full catalog as a routine model tool.
- Execute: native Monty limits, 30 seconds/100 MB baseline and 25 nested calls per execution; return selected fields, counts, IDs, or short summaries. No waiting an hour for a meeting inside execute.
- UI: model generates the view and queries; native `CallTool` actions fetch pages into UI state. Avoid model-mediated copying of datasets into `data`. `data` remains useful for small already-available values. Do not invent a hidden data-reference API.
- Polling: the client/worker handles progress, meeting events, and task polling; do not add every tick/transcript fragment to the LLM conversation. Explicit user questions determine what gets summarized into model context.
- Measure initial tool schema bytes, search result size, selected-schema size, output size, and model calls per scenario. A fixed small catalog is achievable; **zero context impact is not**. No false universal token or host tool-count limit.
- Keep UI entry metadata, task capability, and multi-round input results intact. If a nested call cannot preserve them, use a direct invocation by the application/client. A <=4 model listing does not prohibit the client from calling a known backend tool by name.

### 3. BYOK, state and the Store

BYOK means Telnyx requests use the connected user's credential and account. It does not mean the Oubliai backend cannot process their data, nor that a valid key proves all scopes or features. Do not infer a stable account ID from the key text. Any key-derived principal identifies that credential only until a documented account identity is available.

- **Key path:** native FastMCP TokenVerifier extension point with a documented verification request; distinguish invalid credentials from entitlement/429/transient failures. Use a backend connection identity for the embedded app; never expose an account-wide key to generated code or a shared frontend bundle.
- **OAuth path:** reuse FastMCP's OAuthProxy/RemoteAuthProvider and verifiers, not a new authorization server. First test Telnyx issuer/audience/resource behavior. Use RemoteAuthProvider only if tokens are issued for this resource. Otherwise use OAuthProxy with its documented upstream-token storage/access pattern and a registered Telnyx client. Never disable audience verification to force it to work, and never forward an Oubliai access token as a Telnyx key.
- **Scopes:** source from actual grants and documented operation requirements. The earlier guessed method-to-scope table is not authoritative. Narrow denied operations remain denied through search, execute, direct calls and UI.
- **Runtime state:** native memory backends for local development; native Redis/Valkey-backed Docket and key-value stores for multi-worker sessions/events/work. Partition cache entries by principal, authorization, arguments and version. No cache of mutations; no blind retry after an ambiguous write.
- **TelnyxKVStore:** keep the explicitly requested adapter as an account-owned document/preferences store through the native AsyncKeyValue interface. Contract-test get/put/delete/batch/expiration semantics. Namespace creation is an explicit setup action, not a side effect of the first read. Do not advertise atomic claims/CAS, transactional isolation, task durability or Redis equivalence without a documented primitive and tests. No unauthenticated fallback into another user's store.
- **Catalog Store:** browse domains, operation details and supported profiles; activate permitted registered-disabled features only after their adapter is validated. Favorites affect workspace navigation, not the four-tool model list. One catalog, no separate marketplace backend.

### 4. Client second: make the server usable by applications

Ship a small Python integration package built on `fastmcp.Client`; preserve native tools/resources/prompts/completion, OAuth/bearer auth, protocol negotiation, structured results, progress/log handlers, elicitation/sampling handlers, caching, task lifecycle, notifications and teardown. Use native FastMCP CLI for inspect/list/call and remote bridging; do not build another CLI framework to duplicate it. Include ClientGroup as an optional integration example, not automatic Telnyx proxying.

**Benefit to server:** repeatable conformance tests, connection lifecycle, capability negotiation, bounded retries where documented, accurate handling of task and input-required results. **Benefit to app:** tool metadata plus UI resource loading, backend-only credentials, explicit pending/error states, and an interface shared by human clicks and agent calls. FastMCP Client is not a browser renderer or an LLM agent.

### 5. Facilitator: present in the workspace, executed by an existing agent runtime

When Claude or another MCP host connects, that host's agent already provides orchestration. Do not start a redundant facilitator behind every tool call.

For the standalone/embedded workspace, include a facilitator chat backed by a **Telnyx AI Assistant** in the user's account: use native assistant chat and its MCP/tool configuration, with documented integration-secret authentication. The facilitator selects tools, explains results, generates Prefab UI code, and requests user input. Use native Missions for autonomous/durable agent workflows where their documented run semantics fit; use FastMCP Tasks for server-side operations. No bespoke LLM planning/tool-calling loop, invented message bus, or recursive facilitator calling itself.

Before acceptance, prove the complete path: workspace user -> native assistant conversation -> Oubliai MCP authenticated as that user -> Telnyx operation -> assistant reply/UI. Also prove that the generator tool result (or its validated UI artifact) can reach AppBridge. The existence of a chat endpoint does not prove this entire chain. If native assistant chat omits the required tool/UI payload, record that as a blocking integration gap; do not silently replace it with a homemade runtime or claim generative UI is complete. Existing-app integrations may instead attach their existing agent and pass its actual tool-call stream/results to AppBridge.

The facilitator is also available as an assistant selection for **external meeting sessions**, using Telnyx's native `assistant` attachment. It is never silently attached to a Telnyx Video Room. Session controls and the meeting observer are separate from the conversational model.

Specific current evidence: `openapi.json:101530-101577` defines AssistantChatReq (`content`, `conversation_id`, optional `stream`) and AssistantChatResponse (`content` only). The stream description promises `delta`, `done` and `error`, not MCP App resource/tool-result events. Thus native facilitator text chat is documented, while automatic native-assistant-to-generative-widget delivery is a **compatibility gate, not a confirmed feature**. Do not label this gate green from successful text chat alone.

### 6. App last: native Generative UI, reusable domain views, official embedding

Use the existing `GenerativeUI` provider unchanged where possible, `FastMCPApp` for domain backend/UI organization, and Prefab for reusable tables/forms/charts/controls. One workspace with domain pages replaces the earlier proliferation of separately deployed apps. A common list/detail/form pattern provides access to the long tail of operations; tested domain recipes cover common workflows. Do not infer semantic charts from field names or rebuild Prefab's component framework.

**Actual generation flow:** the host/facilitator discovers the relevant Telnyx tools and Prefab components; writes Prefab Python using the documented imports; invokes the directly advertised generator; the host forwards partial arguments; the native renderer displays the preview; server-side sandbox execution validates the complete result. UI actions call tools directly and populate state. Streamed preview requires host support; final render remains the required fallback. Native generator needs Prefab, Deno for server validation, and browser Pyodide/CSP assets.

**Embedding into another application:** provide a small framework-neutral browser adapter built around official `@modelcontextprotocol/ext-apps` AppBridge and its basic-host example. The application's backend uses the FastMCP client; the browser receives the tool UI resource/metadata, forwards input/result lifecycle through AppBridge, and routes UI tool/resource requests back to that user's backend connection. Use official sandbox/origin checks, not new postMessage conventions. Expose mount/unmount/theme/auth-connection callbacks; a React wrapper is thin convenience, not a second app implementation. Product code for this adapter is application glue, not a new protocol.

The official AppBridge reference explicitly supports `new AppBridge(null, hostInfo, capabilities)` with host-provided `oncalltool` handlers, as well as a connected JS MCP client with automatic forwarding. Use the former for the Python FastMCP-backed embed; preserve native `sendToolInput`, partial-input, final-result and teardown notifications. Do not hand a Python Client object to the JavaScript constructor or invent a browser FastMCP Python runtime.

**Matching design systems:** accept the integrator's color, surface, typography, radius, spacing and light/dark tokens at mount. Map them to MCP host context/styles and Prefab `Theme`/document CSS; send changes through the native host-context mechanism. Use semantic tokens in recipes, inherit host mode, bundle or authorize fonts. Default to host styling when present. A finite token mapping yields first-render consistency; arbitrary proprietary components/layout rules do not transfer automatically across an iframe. Test the same domain view in two differently themed host fixtures, including a runtime theme switch.

**Audio/video:** real-time connections use Telnyx's existing browser SDKs in a stable developer-authored media surface; generated UI controls the surrounding workflow. Do not regenerate the live PeerConnection with each model turn. `ResourcePermissions(microphone/camera)` requests access; actual grant, autoplay, ICE and SDK compatibility need host tests. Own-host browser support is a test target, not a guarantee without testing. Provide phone-supervisor fallback where supported. A recording player is not proof of live media.

### Must NOT have (guardrails, anti-slop, scope boundaries)

- No custom discovery engine, schema flattener, LLM loop, workflow queue, iframe protocol, UI interpreter or replacement auth system when a documented framework feature exists.
- No simultaneous activation of every auth provider, every cache store and competing transforms merely to tick a feature box. Account for framework alternatives explicitly below.
- No proxy to Telnyx's original MCP in the default product; no bot inside Telnyx's own video rooms.
- No automatic domain/DNS changes, namespace creation, purchases, messages or outbound calls during planning or generic live verification. Controlled test recipients/accounts are explicit integration-test prerequisites.
- No claims that absent OpenAPI endpoints prove a platform feature impossible; no claims that registered tools prove complete live coverage; no promise of exactly-once remote writes from local claims alone.
- No assumption that all webhooks use the same signing contract, all paginated endpoints use the same cursor, all inference models accept the same inputs, or every account has all products enabled.
- No hard-coded default LLM model from an old example; use the user's configured available model/assistant.
- No fabricated full-domain identity resolution: a common inbox is an application view over provider records/events with explicit source IDs and explicit contact links, not a native Telnyx cross-channel conversation API.

### Native FastMCP feature disposition

### Concrete Telnyx tools and domain UI

Names below are **actual source operationIds**, not invented friendly tool names. FastMCP may normalize/truncate them; the generated mapping exposes the exact registered MCP name. These examples describe each area's working surface; `docs/operations.json` generated in task 1 supplies the exhaustive operation-by-operation inventory. UI writes invoke these same tools, not a parallel REST implementation.

Recounted from the local source with all OpenAPI HTTP methods: **933 paths, 1,382 operations, 96 top-level webhook definitions**. `/ai/` alone has **176 operations**; the previous "112 AI ops" was a path/operation mix-up. Meetings have **15 operations**, email inboxes **27**, video room/session/participant/recording/composition prefixes together **25**, and fax plus fax applications **11**. Counts are source snapshot counts, not account availability.

| Area | Concrete tool examples from source | Workspace experience / boundary |
|---|---|---|
| Phone/SIP/Call Control | `DialCall`, `RetrieveCallStatus`, `AnswerCall`, `BridgeCall`, `SpeakCall`, `TransferCall`, `HangupCall`, `StartCallTranscription`, `StartCallStreaming`, `StartCallRecord`, `SwitchSupervisorRole`, `ListConnectionActiveCalls` | Call console, status/transcript, recordings, supervisor controls; asynchronous events determine actual call state. SIP applications/connections/TeXML/conferences remain fully covered by inventory. |
| AI Voice | `CallStartAIAssistant`, `CallJoinAIAssistant`, `CallStopAIAssistant`, `CallAddMessagesToAIAssistant`, `CallStartConversationRelay`, `CallStopConversationRelay` | Assistant selection, conversation controls, text injection; acceptance does not prove playback. Barge/whisper routing tested on actual call topology. |
| WebRTC | `FindTelephonyCredentials`, `CreateTelephonyCredential`, `GetTelephonyCredential`, `UpdateTelephonyCredential`, `CreateTelephonyCredentialToken`, `DeleteTelephonyCredential` | Stable browser softphone via official SDK; JWT minting stays backend-side. Mic permissions/ICE/host acceptance tested. |
| SMS/MMS | `SendMessage`, `CreateGroupMmsMessage`, `GetGroupMmsMessages`, `CreateLongCodeMessage`, `CreateNumberPoolMessage`, `SendAlphanumericSenderIdMessage` | Composer, media, per-channel records/status, messaging-profile/registration configuration; available message history verified rather than fabricated. |
| WhatsApp | `SendWhatsappMessage`, `ListWabas`, `ListWhatsappTemplates`, `PostWhatsappTemplate`, `GetWhatsappConversationWindow`, `GetWhatsappCallingSettings` | Templates/media/conversation-window-aware controls, WABA and phone setup. Calling settings alone are not proof of arbitrary WhatsApp call control. Handle versioned-path aliases carefully. |
| RCS | `SendRCSMessage`, `GenerateRCSDeeplink`, `ListRcsAgents`, `CreateRcsAgent`, `ListRcsAgentCarrierApprovals`, `SubmitRcsAgent`, `LaunchRcsAgent`, `ListRCSCapabilitiesOfAPhoneNumber` | Rich message composition, agents/brands/test numbers and carrier approvals; show actual availability. |
| **E-fax** | `SendFax`, `ListFaxes`, `ViewFax`, `CancelFax`, `RefreshFax`, `DeleteFax`; `ListFaxApplications`, `CreateFaxApplication`, `GetFaxApplication`, `UpdateFaxApplication`, `DeleteFaxApplication` | First-class inbox/outbox, PDF upload/preview/download, pages/status/routing; resend is another explicit send, not automatic timeout retry. |
| Email sending/domains | `CreateEmailMessage`, `CreateEmailMessageBatch`, `ListEmailMessages`, `CancelScheduledEmailMessage`, `RescheduleEmailMessage`, `CreateEmailTemplate`, `RenderEmailTemplate`, `createEmailDomain`, `listEmailDomainDnsRecords`, `verifyEmailDomainDnsRecords`, `createEmailDomainWebhook` | Send/schedule/templates and domain DNS setup. Ownership/inbound verification required; preserve existing MX. Email events/validation/blocks/unsubscribe groups included. |
| Agentic email inbox | `CreateEmailInbox`, `ListEmailInboxes`, `GetEmailInbox`, `ListEmailInboxMessages`, `ListEmailInboxThreads`, `GetEmailInboxThread`, `ReplyToEmailInboxMessage`, `ReplyAllToEmailInboxMessage`, `ForwardEmailInboxMessage`, `CreateEmailReplyDraft`, `SendEmailDraft`, `AddEmailInboxMessageLabels`, `AddEmailInboxFilterEntries` | Thread/read/search/triage/draft/reply. Facilitation uses native agent runtime plus authenticated tools. Domain webhook names/signing verified separately; absent top-level email webhook schemas are not filled in by guessing. |
| Verify | `CreateVerificationSms`, `CreateVerificationCall`, `CreateFlashcallVerification`, `CreateWhatsappVerification`, `RetrieveVerification`, `VerifyVerificationCodeById`, `VerifyVerificationCodeByPhoneNumber` | Channel picker, create/check status, profile management; no inferred additional OTP transports. |
| Numbers and routing support | `ListAvailablePhoneNumbers`, `ListPhoneNumbers`, `CreateNumberOrder`, associated order/number configuration and porting operations in inventory | Search/order/configure/port, routing to channel applications; task/poll where provider creates asynchronous jobs. |
| Telnyx Video Rooms | `ListRooms`, `CreateRoom`, `ViewRoom`, `UpdateRoom`, `CreateRoomClientToken`, `RefreshRoomClientToken`, `ListRoomSessions`, `MuteParticipantInSession`, `UnmuteParticipantInSession`, `KickParticipantInSession`, `EndSession`, `ListRoomRecordings`, `CreateRoomComposition` | Rooms/participants/recordings and native Video SDK join controls. **No Meeting Bot participant inside these rooms.** Post-recording STT/inference is an explicit workflow, not a native Room transcript claim. |
| External meeting bot (all 15) | `listMeetingSessions`, `createMeetingSession`, `retrieveMeetingSession`, `updateMeetingSession`, `deleteMeetingSession`, `sendChatMeetingSession`, `speakMeetingSession`, `stopSpeakingMeetingSession`, `listMeetingSessionArtifacts`, `createMeetingSessionArtifact`, `retrieveMeetingSessionArtifact`, `listMeetingSessionEvents`, `listMeetingSessionRecordings`, `deleteMeetingSessionRecordingMedia`, `listMeetingSessionTranscript` | Zoom/Meet/Teams/Webex attendance, admission state, assistant attachment, live transcript/chat/speak, artifacts/recordings. Stop participation is distinct from delete recording media. |
| AI Assistants and testing | `get_assistants_public_assistants_get`, `create_new_assistant_public_assistants_post`, `import_assistants_public_assistants_import_post`, `get_assistant_tests_public_assistants_tests_get`, `create_assistant_test_public_assistants_tests_post`, `ListTestSuiteRuns`, `TriggerTestSuiteRuns`; all assistant CRUD/version/tools endpoints | Assistant editor, supported voice/tools/knowledge setup, import, versions/tests and results. Use exact schema; no made-up Assistant SDK method names. |
| Facilitator conversation | `assistant_chat_public_assistants__assistant_id__chat_post`, `assistant_sms_chat_assistants__assistant_id__chat_sms_post`, `create_new_conversation_public_conversations_post`, `get_conversations_public_conversations_get` | User-owned assistant chat; explicit outbound SMS separate from ordinary chat. UI event delivery gap described above must be resolved. |
| Missions | `get_public_missions_missions`, `post_public_missions_missions`, `post_public_missions_missions_mission_id_runs`, `get_public_missions_missions_mission_id_runs_run_id`, `post_public_missions_missions_mission_id_runs_run_id_cancel`, `GetMissionRunEvent`, `GetMissionRunStep`, `UpdateMissionRunStep`, `ListMissionRunAgents` | Native mission/run/plan/events/knowledge/tools/MCP configuration, pause/resume/cancel where specified. Do not replace native orchestration with custom scheduler. |
| AI inference | `create_openai_chat_completion`, `list_openai_models`, `create_openai_embeddings`, `list_openai_embedding_models`, `create_anthropic_message`, `chat_public_openai_responses_completions_post`, `chat_public_responses_completions_post`, `PostSummary`, `create_typesafe_systemone` | Model/inference playground, structured/streaming requests per actual endpoint support. Old hidden model/chat paths remain accounted for and disabled as agreed. |
| Training / fine-tuning | `get_finetuningjob_public_finetuning_get`, `create_new_finetuningjob_public_finetuning_post`, `get_finetuningjob_public_finetuning__job_id__get`, `cancel_new_finetuningjob_public_finetuning_post` | Documented job creation/list/status/cancel and input requirements; not an invented general model-training platform. |
| RAG / collections | `ListCollections`, `CreateCollection`, `GetCollection`, `UpdateCollection`, `GetCollectionSettings`, `ListCollectionSources`, `SearchCollectionDocuments`; source/settings mutations in inventory | Collection/source management and retrieval grounded in returned documents; ingestion progress/failure visible. |
| Embeddings / clustering | `PostEmbedding`, `PostEmbeddingUrl`, `GetTasksByStatus`, `GetEmbeddingTask`, `GetEmbeddingBuckets`, `GetBucketName`, `PostEmbeddingSimilaritySearch`, `compute_new_cluster_public_text_clusters_post`, `GetClusterImage` | URL/bucket embedding jobs, status/similarity search, cluster output. `GetClusterImage` is not automatically an interactive graph API. |
| Memory / insights / integrations | `ListMemoryProfiles`, `RecallMemories`, `RememberFact`, `IngestSession`, `ForgetProfile`, `ListMemorySources`, `aggregate_conversation_insights`, `create_insight_group`, `create_mcp_server`, `list_mcp_servers`, `list_integrations_public_integrations_get` | Agent memory and insight configuration; tools/MCP server/integration-secret management scoped to user. |
| Speech / voices | `generateSpeech`, `listVoices`, `listSttProviders`, `audio_public_audio_transcriptions_post`, `submitSttRequest`, `getSttRequest`, `listVoiceClones`, `createVoiceCloneFromUpload`, `getVoiceCloneSample`, `listVoiceDesigns`, `createVoiceDesign`, `getVoiceDesignSample`; pronunciation dictionaries | TTS playback/STT upload and batch jobs, voice design/clone/library; special WebSocket operations disabled until adapter tests pass. |
| KV / SQL | `ListKvNamespaces`, `CreateKvNamespace`, `GetKvNamespace`, `ListKvKeys`, `GetKvKey`, `PutKvKey`, `DeleteKvKey`, `DeleteKvNamespace`; `ListSqlDatabases`, `CreateSqlDatabase`, `GetSqlDatabase`, `QuerySqlDatabase`, `DeleteSqlDatabase` | Namespace/key editor and SQL console; requested FastMCP store adapter uses documented primitives only. |
| CloudFS / media / migrations / buckets | `ListCloudfsFilesystems`, `CreateCloudfsFilesystem`, `UpdateCloudfsFilesystem`, `RotateCloudfsMetaToken`, `CreatePresignedObjectUrl`, `GetBucketUsage`, `GetStorageAPIUsage`, `ListMigrations`, `CreateMigration`, `StopMigration`; full `/media` operations | Assets for fax/MMS/speech, filesystem management, migration progress, usage. S3 object list/put/get is a separate official protocol adapter, not generated from absent OpenAPI entries. |
| Remaining platform | Every account/billing/network/wireless/notification/registration/integration operation in E1 | Common catalog/operation inspector and generated forms; scope is not dropped merely because it is not a named custom dashboard. |

Meeting-specific contract: retain last transcript cursor when a timeout returns null next cursor; use event seq for event paging; `joined_at`/actual status establish attendance; `deleteMeetingSession` stops/cancels but retains record; artifact generation is asynchronous and not blanket-idempotent, with the documented segment cap. Assistant sessions have their own restrictions (including `barge_in: true` rejection); validate current schema/docs rather than reusing a scribe payload. The `unknown` platform enum is not proof of support for Telnyx Rooms or arbitrary URLs.

The unified Inbox links source records and verified events across channels. It does not promise historical content that Telnyx does not expose, automatic identity matching across email/phone, or a native common messaging data model. UI badges distinguish synchronized, partial, unavailable and permission-denied data.

### Native FastMCP feature coverage table

"All features" means every documented public feature family has a purpose, supported profile, or explicit incompatibility; it does not mean activating mutually exclusive deployments at once. No invented extension is needed to demonstrate extension support: TasksExtension already does that.

| Feature family | Included use / profile | Acceptance evidence |
|---|---|---|
| OpenAPIProvider / from_openapi | Canonical REST tools; RouteMap, route_map_fn, component hook, mcp_names, tags | Source-to-tool mapping and wire contracts per serialization class |
| Tools / structured content / annotations / binary content | Full API catalog plus narrow documented SDK adapters | Input/output/error/media tests; no binary decoded as text |
| Resources / templates / prompts | Domain instructions, source schemas, webhook catalog, workflow recipes and account views | List/read/get and authorization tests |
| Completions | Prompt/template domain, event and account ID suggestions | Known prefix + empty/denied cases; no claim of universal tool-argument autocomplete |
| Context / dependency injection / lifespan | Request credential, client/store lifecycles, progress/log access | Concurrent identity isolation and client teardown |
| CodeMode / Search / GetSchemas | Default three execution/discovery tools | Catalog-size, chained-call and denial tests |
| BM25SearchTransform / RegexSearchTransform | Alternative no-CodeMode compatibility profile, not stacked on default | Native two-tool search/call behavior; same policy |
| GetTags / ListTools / custom discovery factories | Native optional catalog views available to app/admin client; full ListTools not model default | Catalog paging and unchanged model tool budget |
| Namespace / ToolTransform / visibility | Conflict-free composition, narrowly justified ergonomic transforms, permitted per-user selection | Names remain traceable; direct calls cannot bypass disabled state |
| Versioning / VersionFilter / fingerprinting | Pin upgrade behavior and native schema fingerprint checks | Real compatibility change fixture, not fabricated Telnyx webhook versions |
| ResourcesAsTools / PromptsAsTools | Optional tool-only-host profile with generated utilities behind discovery | Read/get parity without increasing default model listing |
| Local / aggregate / FastMCP provider / composition | One root, shared components, one operations child, domain FastMCPApp providers | Mount/lifespan/policy propagation |
| Filesystem / skills providers | Native loading for reviewed recipes/skills; explicit allowed roots | Only configured content accessible; missing directory handled |
| ProxyProvider / ClientGroup | Optional integration profile for an integrator's existing services | Local upstream stand-in; no default duplicate Telnyx MCP |
| Custom provider / custom transform / custom sandbox | Native extension points remain available; no speculative implementation | Compatibility fixture documents extension contract; built-in implementations preferred |
| Elicitation (form/URL where supported) / sampling / roots | Native supported protocol flow for user input; client handlers; server-owned inference separately | Negotiated modes tested; unsupported mode yields explicit result, not guessed API |
| Background tasks / task extension | Long-running jobs and observer workers through native TasksExtension/Docket | Start/status/result/cancel/restart; nested-call limitations tested |
| Session state / UserSession / SessionId | User preferences and app conversation/session handles | Same principal reconnect and cross-principal rejection |
| Storage backends / wrappers | Memory local; native persistent stores and encryption/prefix wrappers where needed; requested KV adapter limited to proven semantics | TTL, expiry, tenant partition, no credential fallback |
| HTTP / Streamable HTTP / ASGI / custom routes | Remote default, health/readiness and authenticated app endpoints; signed channel webhooks | Real HTTP negotiation, stream/progress, route auth |
| EventStore / SSE resume / stateless configuration | Native compatible transport configuration; separate from durable job execution | Reconnect/replay tests on supported protocol; no universal persistence claim |
| stdio / legacy SSE / remote bridge | Compatibility test profiles, not separate production servers | Native transport examples and graceful capability fallback |
| JWT/introspection/static/custom token verification | Appropriate verified key/OAuth credentials | Expired, wrong-audience, wrong-user and transient-validation cases |
| RemoteAuthProvider / OAuthProxy / MultiAuth | Both user entry modes; choose OAuth route from actual audience test | Full resource discovery and token exchange test with correct audience |
| OIDC/full OAuth/third-party auth providers / identity assertion | Framework-provided optional deployment adapters; not separate user-account system for BYOK | Config fixtures only unless explicitly deployed; no Telnyx identity-assertion claim |
| Authorization / scopes / roles / step-up | Documented scopes; roles only if integrator actually supplies a role model | Check lists and execution in all paths; step-up where supported |
| Middleware logging / timing / errors / rate limits | Native classes, shortest sufficient stack; no payload secrets | Error fidelity, telemetry and load tests |
| Retry / caching / response limits | Read/idempotent retry only; principal-aware safe reads; preserve valid schemas | Ambiguous write not repeated; private result not shared; oversized result readable through paging |
| Ping / dereferencing / tool injection | Compatibility profiles only where needed; dereference once | No hidden fifth model tool or duplicated schema expansion |
| OpenTelemetry / icons / pagination / cache hints | Native observability/metadata; component lists paginated, upstream pages separately handled | Trace IDs without payloads; schema/metadata tests |
| FastMCPApp / Prefab / custom HTML / permissions | Domain workspace and stable SDK media surfaces | Actual action, denied action, teardown and host capability test |
| GenerativeUI / component search / sandbox | Native rendering and runtime component reference | Generator is directly visible with resource metadata; streaming/final render tests |
| Approval / Choice / FormInput / FileUpload | Native interaction providers used in relevant domain workflows | UI action reaches intended endpoint once; rejected/cancelled input stays rejected |
| CLI / fastmcp.json / inspect / install / generate-cli / testing | Reuse native commands and project schema; examples for integrators | Configuration loads; native CLI works; no unsolicited edits to user's client config |
| Hosted deployment / sandboxed-agent patterns / client-only package | Document compatible deployment/integration options, not extra hosting products | Reproducible local/container run; documented dependencies |

Client-specific coverage: native HTTP/in-memory/stdio transports and negotiation; tool results including errors/media; resource/template/prompt/completion operations; progress/log notifications; form and URL elicitation where negotiated; sampling and roots handlers; task polling/cancellation; bearer/OAuth/M2M/CIMD auth as supported integration profiles; response-cache isolation; ClientGroup; UI extension capability advertised by our embedding client. These are native client responsibilities; they are not all server tools.

## Verification strategy
Test decision: TDD with pytest/pytest-asyncio and the installed HTTP client's mock transport; browser integration with the official basic-host fixture and Playwright. Existing framework behavior gets characterization tests first, rather than rewriting it. The commands below refer to tests to be created during implementation, not tests claimed to exist now.

Evidence directory: `.omo/evidence/telnyx-fastmcp/`; each task writes its RED/GREEN results and relevant HTTP/browser artifacts. No production code is written by this planning run.

Three mandatory end-to-end scenario families:
1. **Happy:** user A discovers a Telnyx operation, executes it via the native framework, renders a generated view, and acts from that view. Exactly four default model tools; request uses A's upstream credential; AppBridge receives real UI metadata and final content.
2. **Edge:** expired credential, denied operation, empty page, malformed deepObject/body, 429, ambiguous mutation timeout, pending meeting admission, interrupted job and disabled feature. The UI reports the actual condition; no cross-user data or automatic duplicate mutation.
3. **Adjacent regression:** user B sees no A data; plain MCP clients can call tools without Apps; native resources/prompts/completion/tasks retain their semantics; a theme change does not recreate an active media connection.

Completion gates: every source operation has an audited disposition; every normal enabled operation is represented by a working adapter and validated schema/wire contract; every requested domain has UI/actions and failure coverage. All supplied spec webhooks are represented as reference resources; real receiver handlers require the actual channel signing contract. Do not equate a row count with implemented behavior.

Performance gates: default visible tool count <=4 and initial serialized tool listing <=32 KiB; default search returns <=5 candidates; compact schema fetch and result projections avoid full-catalog responses; normal summary outputs <=32 KiB with explicit pagination/artifact handling rather than corrupting schemas. Measure cold startup and warm discovery on fixed fixture hardware, plus concurrent two-tenant load, and set a recorded regression baseline before optimization. Never present bytes/4 as a measured tokenizer count.

Run `uv run pytest tests/unit tests/integration -q`, `uv run pytest tests/e2e -q`, `uv run ruff check src tests`, `uv run basedpyright src`, and browser package `npm run test:e2e` / `npm run build`. Live product tests are separate and report `verified`, `blocked: credential/entitlement/recipient`, or `not run`. A skipped or mock-only telephony/media/OAuth test never counts as a live pass. Agent-executed QA must not silently purchase, message or dial real recipients.

## Execution strategy
### Parallel execution waves
Order follows the requested architecture: validate native contracts -> OpenAPI server -> reusable client/facilitator -> domain operations -> embedded Generative UI -> release verification. The small risk probes happen first so downstream work does not build on false assumptions.

| Wave | Tasks | Parallel subagents and exclusive ownership | Deliverable |
|---|---|---|---|
| 0: contract proofs | 1-4 | Spec analyst (1), framework/discovery analyst (2), auth/facilitator analyst (3), embedding analyst (4) | Evidence-backed contracts; integration blockers visible before feature work |
| 1: server | 5-9 | Provider/wire lane (5-6 sequential); auth lane (7); lifecycle/state lane (8); lead assembles (9) | BYOK Streamable HTTP server and four-tool surface |
| 2: client/facilitator | 10-13 | Client lane (10-11 sequential); facilitator lane (12); store lane (13) | Reusable client and existing-runtime facilitator; no custom model loop |
| 3: domains | 14-19 | Communications lane (14-15); realtime/meetings lane (16-17); AI/storage lane (18-19) | Tested operations/workflows for all requested areas |
| 4: app/embedding | 20-24 | Embed/theme lane (20-21); recipes lane (22); media lane (23); lead integrates workspace (24) | Host-themed Generative UI workspace plus live media surfaces |
| 5: delivery | 25-27 | Packaging/docs lane (25); coverage/perf lane (26); QA lead (27 after both) | Reproducible release with honest compatibility/coverage report |

Use subagents for disjoint modules and independent verification, not for five competing implementations of the same server. The lead owns composition files and shared contracts. Each delegate receives its task, exact dependency outputs, allowed paths, binary stop condition and required evidence. Server/client/app share one catalog and authorization policy. Reviewers are read-only. No mandated agent-specific comments in product source.

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1-4 | none | 5-24 | each other |
| 5 | 1,2 | 6,9,14-19 | 7,8 |
| 6 | 5 | 9,14-19 | 7,8 |
| 7 | 3 | 9-24 | 5,6,8 |
| 8 | 1,2,3 | 9,13,16-19 | 5-7 |
| 9 | 5-8 | 10-24 | none (assembly) |
| 10 | 9 | 11,12,20 | 13 |
| 11 | 10 | 17,27 | 12,13 |
| 12 | 3,9,10 | 24,27 | 11,13 |
| 13 | 1,7,8,9 | 19,24 | 10-12 |
| 14-15 | 6,7,9,10 | 22,24 | 16-19 |
| 16 | 6-11 | 17,23,24 | 14,15,18,19 |
| 17 | 11,12,16 | 22,24 | 14,15,18,19 |
| 18 | 6-10,12 | 22,24 | 14-17,19 |
| 19 | 6-10,13 | 22,24 | 14-18 |
| 20 | 4,10 | 21,23,24 | 22 |
| 21 | 20 | 24,27 | 22,23 |
| 22 | 14-19 | 24 | 20,21,23 |
| 23 | 16,20 | 24,27 | 21,22 |
| 24 | 12-23 | 25-27 | none (assembly) |
| 25-26 | 24 | 27 | each other |
| 27 | 25,26 | F1-F4 | none |

## Todos
> Implementation + Test = ONE todo. Never separate.
<!-- APPEND TASK BATCHES BELOW THIS LINE WITH edit/apply_patch - never rewrite the headers above. -->
- [ ] 1. Pin the source inventory and establish coverage accounting
  - Files: `pyproject.toml`, `uv.lock`, `src/oubliai/catalog.py`, `tests/contracts/test_inventory.py`, `docs/operations.json` (generated from the untouched root `openapi.json`). Read local instructions first; preserve user files.
  - Native basis: E1/E2. Count all HTTP methods supported by OpenAPI, resolve effective server/path metadata, retain webhook definitions separately. Record input SHA-256 and dependency versions. Map `(method,path)` to original operationId and MCP name; deterministic collision resolution with explicit map, no silent overwrites.
  - Depends: none; Wave 0 spec lane. Acceptance/QA: `uv run pytest tests/contracts/test_inventory.py -q` proves every source operation appears once and detects an injected duplicate-name collision, non-local reference and alternate-host case. Emit actual counts instead of copying previous claimed counts.
  - Evidence: `task-01-inventory.json` + test output. Commit only if requested: `test(catalog): pin complete source inventory`.

- [ ] 2. Prove the native four-tool discovery and UI boundary
  - Files: `tests/contracts/test_discovery_composition.py`, `tests/contracts/test_nested_calls.py`. References: E2-E5/E8 and installed CodeMode source.
  - Wave 0 framework lane, depends none. Assemble a tiny in-memory operations child with CodeMode Search/GetSchemas/execute, and a parent directly serving GenerativeUI. Put Prefab component lookup in the discoverable catalog using native provider scoping. No custom search/execute implementation.
  - QA: `uv run pytest tests/contracts/test_discovery_composition.py tests/contracts/test_nested_calls.py -q`: listing is exactly four, search/schema resolve real underlying tools, chained arithmetic/mock API calls return a projection, directly advertised generator has `ui.resourceUri`. Negative: denied/app-only tool stays inaccessible to model; nested task/input-required/UI metadata behavior is recorded rather than presumed. If native composition cannot meet the four-tool and metadata contract, stop and report the incompatibility before app work.
  - Evidence: `task-02-catalog.json`, `task-02-nested-results.json`. Commit if requested: `test(fastmcp): establish discovery and app contracts`.

- [ ] 3. Prove BYOK/OAuth and native facilitator integration contracts
  - Files: `tests/contracts/test_auth_contract.py`, `tests/contracts/test_facilitator_contract.py`, `docs/compatibility.md`. References: E8-E10 and exact AssistantChat/MCP server configuration schemas.
  - Wave 0 auth lane, depends none. Verify correct resource/audience handling, per-user upstream credential retrieval and scope interpretation. Verify native Telnyx Assistant chat can invoke the four-tool MCP surface and return usable tool/UI events or artifact references to the workspace. Prefer documented native runtime, not a custom loop.
  - QA: `uv run pytest tests/contracts/test_auth_contract.py tests/contracts/test_facilitator_contract.py -q`: local issuer and transport fixtures prove good/wrong audience, isolated credentials and assistant tool-result forwarding. Authorized native service integration is separately required for live readiness; an unavailable auth flow/tool event remains a named blocker. Do not create shared credentials or register external clients silently.
  - Evidence: `task-03-auth.json`, `task-03-facilitator.json` with redacted live or blocked status. Commit if requested: `test(auth): verify user-scoped native agent path`.

- [ ] 4. Prove official AppBridge, native renderer and host-token theming
  - Files: `web/tests/contracts/embed.spec.ts`, two minimal host fixture pages, `web/package.json`. References: E4-E7, official basic-host.
  - Wave 0 embedding lane. Reuse official AppBridge/sandbox example with mock MCP-backed data and the real Prefab renderer. Test direct generator metadata, final rendering, partial input if supported, tool-action round trip, and host theme variables. Do not rewrite the renderer.
  - QA: `npm --prefix web run test:contracts`: two fixture themes visibly/computationally differ in configured colors/fonts/radius, action invokes expected mock, denied mic and blocked CDN show explicit fallback. Capture screenshots and computed styles; no real media claim from fake devices.
  - Evidence: `task-04-{light,dark}.png`, `task-04-capabilities.json`; clean browser teardown. Commit if requested: `test(embed): verify native app host contract`.

- [ ] 5. Compose the canonical OpenAPI providers and domain catalog
  - Files: `src/oubliai/openapi.py`, `src/oubliai/catalog.py`, `tests/unit/test_openapi.py`. Depends 1-2; Wave 1 provider lane. References E1/E2.
  - Use OpenAPIProvider and documented hooks. Partition only where effective origin/serialization requires it. Register ordinary operations once, attach family/source/tags/annotations, and retain disabled special entries with explicit status. Maintain separate app catalog resources and webhook reference schemas. No per-endpoint generated Python wrapper files.
  - QA: `uv run pytest tests/unit/test_openapi.py -q`: mapping reconciles to inventory; required parameters/deepObject/empty bodies output schemas remain valid; collision and duplicate-v2 fixtures fail safely. Disabled WSS/x402 cannot be executed accidentally.
  - Evidence: `task-05-coverage.json`. Commit if requested: `feat(server): compose native OpenAPI catalog`.

- [ ] 6. Validate HTTP/media adapters and upstream execution semantics
  - Files: `src/oubliai/transport.py`, small `src/oubliai/adapters/` only for evidenced exceptions, `tests/contracts/test_wire.py`. Depends 5; Wave 1 provider lane. References E1/E2/E12 and official channel SDKs.
  - Reuse async HTTP pooling and native SDKs; keep exact schema content types. Cover JSON/deepObject/array/form/multipart/octet/PDF/audio/SSE; support separate SDK route for WebRTC/S3/video where documented. Implement read/idempotent retries only with endpoint-specific rules; no blanket 5-rps platform assumption.
  - QA: `uv run pytest tests/contracts/test_wire.py -q`: mock records exact host/path/query/body/content-type; binary round-trip hashes match; 429/read timeout handled; ambiguous POST timeout is not blindly resent; external origin cannot receive another credential.
  - Evidence: `task-06-wire.json`; Commit if requested: `feat(transport): cover documented serialization gaps`.

- [ ] 7. Implement native auth composition and execution-time authorization
  - Files: `src/oubliai/auth.py`, `tests/integration/test_identity.py`. Depends 3; Wave 1 auth lane. References E8-E10.
  - Wire chosen native verifier/OAuth provider/MultiAuth path from the contract gate. Keep upstream connection credentials distinct from app sessions. Fail closed on absent principal. Scope data is reviewed against actual grants/operation requirements; do not manufacture scopes. Request-specific client auth never mutates a global default key.
  - QA: `uv run pytest tests/integration/test_identity.py -q`: two simultaneous users on search, execute, direct calls, resources and UI actions reach only their account; wrong audience/expired/missing scopes denied; 429 during verification isn't reported as successful authentication.
  - Evidence: `task-07-isolation.json`. Commit if requested: `feat(auth): enforce BYOK across execution surfaces`.

- [ ] 8. Configure native lifecycle, stores, tasks and observability
  - Files: `src/oubliai/runtime.py`, `tests/integration/test_runtime.py`. Depends 1-3; Wave 1 state lane. References E8.
  - Native composable lifespans own clients, stores, TasksExtension and teardown. Use native logging/timing/errors, bounded rate controls and private read caches only where isolation proven. Persistent Docket backend for workers; shared request-state keys for multi-round requests; EventStore for supported replay separately. Emit metadata/trace IDs without credential/payload logging.
  - QA: `uv run pytest tests/integration/test_runtime.py -q`: TTL/expiry, task progress/cancel, restart/resume and user isolation; malformed state rejected. Redis integration fixtures prove multi-worker behavior. Distinguish Docket redelivery from exactly-once Telnyx side effects.
  - Evidence: `task-08-runtime.json`; Commit if requested: `feat(runtime): configure native persistence and tasks`.

- [ ] 9. Assemble and exercise the remote server
  - Files: `src/oubliai/server.py`, `fastmcp.json`, `tests/e2e/test_server_http.py`. Depends 5-8; Wave 1 lead.
  - One factory and one ASGI composition; follow native HTTP deployment/lifespan/auth route mounting. Default four-tool discovery composition from task 2, correct icons/instructions/resources/prompts, per-domain disabled statuses, health/readiness. Additional application HTTP routes require their own verified authentication; custom_route does not inherit MCP auth.
  - QA: `uv run pytest tests/e2e/test_server_http.py -q`; `uv run fastmcp inspect fastmcp.json` after checking native CLI options. Spawn uvicorn on a test-owned port, `curl --fail http://127.0.0.1:$PORT/health`, real FastMCP Client lists/calls via HTTP and confirms <=4 tools. Missing auth and forbidden Host fail as configured; stop owned PID.
  - Evidence: `task-09-http.json`, `task-09-teardown.txt`. Commit if requested: `feat(server): expose Streamable HTTP application`.

- [ ] 10. Deliver the reusable native FastMCP client
  - Files: `src/oubliai/client.py`, `examples/client.py`, `tests/integration/test_client.py`. Depends 9; Wave 2 client lane. References E8 + official client docs.
  - Thin configuration/context manager around Client, not a second MCP implementation. Preserve raw ToolResult metadata and structured content. Integrator supplies per-user connection/auth and handlers. Prefer existing native CLI/remote bridge for terminal usage.
  - QA: `uv run pytest tests/integration/test_client.py -q`: HTTP tools/resources/prompts/completion, auth renewal fixture, cancellation, concurrent users and deterministic close; malformed result/connection loss returns actual error.
  - Evidence: `task-10-client.json`. Commit if requested: `feat(client): package reusable native client integration`.

- [ ] 11. Wire client interactivity and capability profiles
  - Files: `src/oubliai/client_handlers.py`, `tests/integration/test_capabilities.py`, `examples/client_group.py`. Depends 10; Wave 2 client lane.
  - Native elicitation, sampling, roots, logs, progress, tasks and notifications. Explicit auto/legacy profiles; unsupported capability shown honestly. ClientGroup opt-in only. App extension/resource support exposed by the host backend. Prompt changes/results only when meaningful, not every polling tick.
  - QA: `uv run pytest tests/integration/test_capabilities.py -q`: approved/declined input; task completion/cancel; requested sample/roots handled; no credentials/data in log messages; unsupported protocol branch deterministic.
  - Evidence: `task-11-capabilities.json`. Commit if requested: `feat(client): preserve native interactive capabilities`.

- [ ] 12. Connect the workspace facilitator to Telnyx's native agent runtime
  - Files: `src/oubliai/facilitator.py`, `resources/facilitator.md`, `tests/integration/test_facilitator.py`. Depends 3,9,10; Wave 2 facilitator lane. References E10 plus inventory's assistant/MCP/integration-secret operations.
  - Configure/select a user-owned Telnyx Assistant and conversation; configure its MCP server/tool auth through documented secret fields. It uses the same compact discovery surface and policies. Expose conversation lifecycle to client and UI; relay verified native tool/UI events according to task 3's contract. Existing-host-agent mode bypasses this service. Exclude facilitator entry methods from its own execution catalog to prevent recursion.
  - QA: `uv run pytest tests/integration/test_facilitator.py -q`: authenticated discovery->operation->reply/UI trace; two-user conversations cannot mix; rejected tool remains rejected; runtime lacking the required payload is explicitly blocked, not emulated with a handwritten LLM loop.
  - Evidence: `task-12-facilitator.json`. Commit if requested: `feat(agent): integrate native Telnyx facilitator`.

- [ ] 13. Implement the requested Telnyx KV store adapter narrowly
  - Files: `src/oubliai/stores/telnyx.py`, `tests/contracts/test_telnyx_store.py`. Depends 1,7-9; Wave 2 store lane. References exact KV schemas and native AsyncKeyValue interface.
  - Explicit selected user namespace; adapter covers proven document get/put/delete/batch semantics, serialized TTL with documented expiry behavior. Use existing FastMCP storage wrappers for namespace/encryption where applicable. No Docket backend, CAS, queue, lock manager or silent namespace creation.
  - QA: `uv run pytest tests/contracts/test_telnyx_store.py -q`: two-user isolation, expiry, partial batch failure, absent credential denied, setup creates namespace only when invoked. Surface capability limits in Store UI.
  - Evidence: `task-13-store.json`. Commit if requested: `feat(store): add account-owned KV document adapter`.

- [ ] 14. Complete fax and email operation/workflow contracts
  - Files: `src/oubliai/domains/fax.py`, `src/oubliai/domains/email.py`, `tests/domains/test_fax_email.py`. Depends 6,7,9,10; Wave 3 communications lane. References E1 and tool inventory below.
  - Generated tools are reused; add only upload/media orchestration and native task tracking where needed. First-class PDF send/receive/status/preview; email domains/DNS verification/inbox/search/reply/drafts/send/events. Agentic email runs through facilitator/native runtime, not a new autonomous polling engine. Fetch exact DNS records; never replace existing domain MX automatically.
  - QA: `uv run pytest tests/domains/test_fax_email.py -q`: binary PDF upload and fax status; inbound fax; email reply preserves IDs/thread, DNS incomplete status, attachment failure and duplicate event handling. Templates/schema are not proof of delivery; controlled live channel test has separate status.
  - Evidence: `task-14-fax-email.json`. Commit if requested: `feat(channels): integrate fax and agentic email workflows`.

- [ ] 15. Complete messaging, verification and number support
  - Files: `src/oubliai/domains/messaging.py`, `tests/domains/test_messaging.py`. Depends 6,7,9,10; Wave 3 communications lane.
  - SMS/MMS, WhatsApp, RCS, Verify, number inventory/ordering/configuration and registration use generated operations. Preserve channel identifiers and documented paging/status differences; no fabricated universal thread API or fallback channel send. Native prompts document multi-step operations.
  - QA: `uv run pytest tests/domains/test_messaging.py -q`: each channel's correct endpoint/payload/media, status transition and refusal/error; wrong-channel reply rejected; unavailable capability explicit; number-order acceptance not confused with completion.
  - Evidence: `task-15-messaging.json`. Commit if requested: `feat(channels): cover messaging and number operations`.

- [ ] 16. Complete voice, video management and event ingestion
  - Files: `src/oubliai/domains/voice.py`, `src/oubliai/domains/video.py`, `src/oubliai/events.py`, `tests/domains/test_realtime.py`. Depends 6-11; Wave 3 realtime lane. References E1/E12.
  - Generated Call Control/conference/room APIs; correlate asynchronous events by real provider IDs. Verify signatures/raw bodies per documented channel before accepting receiver events; dedupe exact IDs, retain source, principal and time. Public routes cannot select arbitrary other-user inboxes. Native tasks track slow jobs; no code-mode long-lived event loop. Call roles come from documented caller/callee/supervisor relationships, not assumed AI-agent whisper semantics.
  - QA: `uv run pytest tests/domains/test_realtime.py -q`: lifecycle out-of-order/duplicate event, raw signature tampering, supervisor role request and room token lifecycle. Text injection acknowledgment not falsely labeled spoken audio. Room management never starts a Meeting Bot.
  - Evidence: `task-16-realtime.json`. Commit if requested: `feat(realtime): integrate documented call and room controls`.

- [ ] 17. Add third-party meeting bot and facilitator attendance
  - Files: `src/oubliai/domains/meetings.py`, `tests/domains/test_meetings.py`. Depends 11,12,16; Wave 3 meetings lane. References E11 and exact meeting inventory.
  - Native session create/schedule/stop, speak/chat, event/transcript pagination, recordings/artifact generation. Assistant attachment uses native contract; do not pass incompatible schedule/barge flags. Durable native task observer persists cursor and terminal state with principal binding; no guarantee of exactly-once non-idempotent speech/artifact creation. Polling interval is a chosen responsiveness budget, not a measured latency guarantee.
  - QA: `uv run pytest tests/domains/test_meetings.py -q`: waiting/admission-denied/active/end; null cursor retains previous cursor; retry idempotency key does not rejoin; restart resumes transcript; artifact pending/failure/incomplete data shown; Telnyx Room URL rejected by our supported-platform workflow.
  - Evidence: `task-17-meetings.json`. Commit if requested: `feat(meetings): orchestrate native external meeting sessions`.

- [ ] 18. Complete AI agents, voice, inference, training and RAG
  - Files: `src/oubliai/domains/ai.py`, small focused modules as needed, `tests/domains/test_ai.py`. Depends 6-10,12; Wave 3 AI lane.
  - Reuse full assistant/test/version/Mission/conversation/memory/tool/MCP/integration APIs; inference and speech variants; fine-tuning jobs; RAG sources/collections/embedding/search/clusters. Long jobs use provider job IDs + native Tasks, not a new scheduler. Streaming inference uses a verified adapter when needed; do not blanket-disable it or route tokens through the model twice.
  - QA: `uv run pytest tests/domains/test_ai.py -q`: create/read/update schema fixtures, test job lifecycle, model rejection, RAG pending->ready/search and failed ingestion, cancel, paginated memory, stream termination. No claim of arbitrary training capabilities beyond documented job/model support.
  - Evidence: `task-18-ai.json`. Commit if requested: `feat(ai): cover agent inference training and RAG operations`.

- [ ] 19. Complete storage and remaining API coverage
  - Files: `src/oubliai/domains/storage.py`, `tests/domains/test_storage.py`, `tests/contracts/test_remaining_operations.py`. Depends 6-10,13; Wave 3 storage lane.
  - KV/SQL/CloudFS/media/migrations and bucket management use provider; object operations use documented Telnyx S3 auth/SDK separately. Treat SQL as potentially mutating irrespective of POST/read labels. Remaining account/billing/networking/wireless/etc operations stay fully discoverable and usable through the common inspector/forms; don't create unrelated bespoke subsystems.
  - QA: `uv run pytest tests/domains/test_storage.py tests/contracts/test_remaining_operations.py -q`: object bytes and signed URL contract, credential rejection, KV/SQL errors, migration pending/stop. Every inventory row reconciled; disabled alternate protocols retain reasons and cannot be falsely marked enabled.
  - Evidence: `task-19-storage-coverage.json`. Commit if requested: `feat(storage): integrate native storage and remaining catalog`.

- [ ] 20. Build the reusable official AppBridge embedding adapter
  - Files: `web/src/embed.ts`, `web/src/host.ts`, `web/tests/embed.spec.ts`; minimal authenticated backend glue in client package. Depends 4,10; Wave 4 embed lane. References E4-E6.
  - Adapt official basic-host with MCP metadata/resource/input/result flow, CSP and origin validation, user-scoped backend forwarding, cancellation and teardown. Parent application owns mount container, auth connection and optional existing agent; browser receives no account-wide Telnyx key. Framework-neutral entry with small React example only.
  - QA: `npm --prefix web run test:e2e -- embed.spec.ts`: two embedded sessions render and execute independent actions; denied resource/origin rejected; unmount closes intervals/bridge/media owned by component. Native generator final result renders without invented transport.
  - Evidence: `task-20-embed.png`, `task-20-actions.json`. Commit if requested: `feat(embed): integrate official MCP AppBridge`.

- [ ] 21. Apply host design tokens through native styling
  - Files: `web/src/theme.ts`, `resources/ui-style-guide.md`, `web/tests/theme.spec.ts`. Depends 20; Wave 4 theme lane. References E7 and official host-context styles.
  - Map provided tokens to supported host variables and Prefab Theme/CSS, handle fonts/CSP, light/dark, dimensions and updates. Recipes refer to semantic tokens; no hard-coded Telnyx branding overriding host. Missing tokens use native defaults. Do not scrape parent DOM or invent automatic arbitrary component-library conversion.
  - QA: `npm --prefix web run test:e2e -- theme.spec.ts`: computed styles + screenshots for two host themes and runtime switch; narrow/mobile, focus, keyboard and error states visible; no active media restart on theme update.
  - Evidence: `task-21-themes/`. Commit if requested: `feat(theme): inherit integrator design tokens`.

- [ ] 22. Build native Generative UI domain recipes and actions
  - Files: `src/oubliai/apps/`, `resources/recipes/`, `tests/integration/test_apps.py`, `web/tests/domains.spec.ts`. Depends 14-19; Wave 4 recipes lane. References E4/E5/E7 and inventory.
  - One shared list/detail/form/action pattern, specialized recipes for communications/AI/storage. FastMCPApp owns UI/backend visibility; native FormInput/Choice/FileUpload and declarative CallTool/SetState/SetInterval drive actual interactions. Use structured output and a short text summary, not the entire payload echoed into the conversation. Native GenerativeUI changes layout at request time; no new TelnyxUI subclass/data-reference engine.
  - QA: `uv run pytest tests/integration/test_apps.py -q` and `npm --prefix web run test:e2e -- domains.spec.ts`: every requested area has a discoverable view, real mock-backed action and failure state; malformed generated code reports native sandbox failure; blocked imports rejected; component lookup uses installed API.
  - Evidence: `task-22-domain-views/`. Commit if requested: `feat(apps): add generative domain workspace recipes`.

- [ ] 23. Integrate stable native voice/video media surfaces
  - Files: `web/src/media/`, `web/tests/media.spec.ts`, targeted browser-token backend. Depends 16,20; Wave 4 media lane. References E12 + verified Telnyx Video SDK documentation.
  - Use existing SDKs for softphone and room participation, short-lived browser credentials and teardown. Generated UI controls stable media widgets; mic/camera grant and host CSP/network checked. Monitor/whisper/barge topology must be proven on a controlled call, not inferred from an enum. No bot in Telnyx Rooms. Phone-supervisor fallback remains available where supported.
  - QA: `npm --prefix web run test:e2e -- media.spec.ts`: fake devices verify UI lifecycle only; controlled live loopback verifies audible monitor and each role separately, ICE connection and mute/end. Denied permissions/CDN/network produce actionable state; no call gets labeled connected solely from REST acceptance.
  - Evidence: `task-23-media-capabilities.json` includes per-host live/unverified statuses. Commit if requested: `feat(media): integrate official real-time browser SDKs`.

- [ ] 24. Assemble Store, Omni Inbox and facilitator workspace
  - Files: `src/oubliai/apps/workspace.py`, `web/src/workspace.ts`, `tests/integration/test_workspace.py`, `web/tests/workspace.spec.ts`. Depends 12-23; Wave 4 lead.
  - Single domain navigation/catalog Store, linked native account records and signed event history, explicit per-channel/source context and user-owned preferences. Facilitator chat is optional when host already supplies agent. Contact links explicit; historical coverage indicators say what is actually loaded. Host can embed one view or whole workspace. Feature-disabled cards explain reason; no enabling unsupported adapters.
  - QA: `uv run pytest tests/integration/test_workspace.py -q`; `npm --prefix web run test:e2e -- workspace.spec.ts`: fax->detail/send, email thread->draft/reply, meeting->artifact, RAG->search, Store->operation; two-user isolation and absent channel history are visibly correct. Agent-generated view receives theme and actual tool events.
  - Evidence: `task-24-workspace/`. Commit if requested: `feat(workspace): compose unified communications and AI app`.

- [ ] 25. Package the native server/client/app for integrators
  - Files: `Dockerfile`, `compose.yaml`, `.env.example`, `README.md`, `examples/embed/`, `docs/integration.md`. Depends 24; Wave 5 delivery lane.
  - Native fastmcp.json, pinned dependencies, Deno/Pyodide assets, optional Redis worker profile, HTTP URL configuration, discoverability card. Reuse native CLI; document three integration modes (MCP host, Python service, browser embedding) and required tokens/host permissions. No publishing, git remote, license choice or client config edits without user authorization.
  - QA: `uv run fastmcp inspect fastmcp.json`, `npm --prefix web run build`, `docker compose build`; start only project services, curl health/readiness, execute packaged example and tear down owned resources. Fail missing production auth/state configuration explicitly.
  - Evidence: `task-25-package.json` and teardown receipt. Commit if requested: `build: package documented integration surfaces`.

- [ ] 26. Run coverage, capability and context/performance regression gates
  - Files: `tests/contracts/test_coverage.py`, `tests/performance/`, `docs/coverage.md`, `docs/compatibility.md`. Depends 24; Wave 5 verification lane.
  - Reconcile source operations to adapters, scope/policy, view/common-form availability, serialization tests and disabled status; native feature matrix has test/profile/exclusion evidence. Benchmark fixed fixture catalog and outputs, native fingerprint drift, concurrent clients and account cache isolation. No claim every provider can be enabled simultaneously.
  - QA: `uv run pytest tests/contracts tests/performance -q`: four tools/byte/search caps; added unmatched spec operation fails; disabled entry not counted callable; response-schema change requires reviewed fingerprint; 20 concurrent mocked requests preserve user identity and finish without leaked clients.
  - Evidence: `task-26-coverage.json`, `task-26-benchmarks.json`. Commit if requested: `test: enforce coverage and context budgets`.

- [ ] 27. Exercise packaged product and produce the release evidence
  - Files: `tests/e2e/`, `docs/release-evidence.md`. Depends 25-26; Wave 5 QA lead.
  - Execute all automated commands in verification strategy, real HTTP client and real renderer interactions. Separately run authorized live read-only and controlled telecom/meeting/agent/media workflows. Unavailable credential/entitlement/host prerequisites are blocked capabilities, never passed by a mock. Run visual QA on actual generated outputs and two embed themes.
  - QA: full suite/build/type/lint success; happy/edge/regression scenarios above; every owned process/browser/container stopped. No implementation-complete declaration while a required supported path remains blocked; report the exact remaining contract instead.
  - Evidence: `task-27-release.json`, screenshot directory, `task-27-teardown.txt`. Commit if requested: `test: verify integrated product release`.

## Final verification wave
Run these read-only verifier lanes in parallel after all implementation tasks. Every issue must cite a requirement and failing evidence; artifact counts alone are not passes.
- [ ] F1. Plan compliance audit
  - Compare every scope/domain/native-feature row to coverage report, exact adapter/schema tests and app action evidence. Independently recompute inventory counts from source. Reject unexplained exclusions, disabled-as-working entries, or mock-only live claims. Evidence: `F1-compliance.md`.
- [ ] F2. Code quality review
  - Inspect composition and shared state for duplicated framework implementations, broad retry/caching bugs, per-user auth leakage, unnecessary module/class layers and oversized modules. Run lint/type/unit checks. Native framework extensions must have an evidenced need. Evidence: `F2-quality.md`.
- [ ] F3. Real manual QA
  - Use packaged HTTP server, native client and actual browser AppBridge host. Exercise fax/email/messaging/meeting/AI/RAG/storage workflows, renderer, two themes, denied inputs and teardown. Check live capability statuses separately. Evidence: `F3-qa.md` plus HTTP/action logs/screenshots.
- [ ] F4. Scope fidelity
  - Verify no Telnyx Room meeting bot, no default duplicate MCP proxy, <=4 model tools, BYOK key/OAuth contract, facilitator honest capability report, all requested domain UI and design-token integration. Reject unnecessary custom runtime/queue/search/rendering protocols. Evidence: `F4-scope.md`.

## Commit strategy

This planning run does not initialize git, commit, tag, publish or choose a license. During implementation, commit only if the user requests it; use task-sized verified increments and existing repository style. Preserve original spec and user changes. No empty wave-marker commits or automatic release tags. Exclude credentials and ephemeral runtime artifacts; keep small redacted evidence and source manifests.

## Success criteria

The plan-writing deliverable is complete when this document contains the ordered server/client/app work, exact domain tool examples, complete source-operation accounting rules, native feature dispositions, parallel lanes and evidence-backed limitations, and a read-only consistency review has been incorporated. This does not mark the future implementation complete.

The product is complete only when:
- Every operation in the pinned source is accounted for, normal enabled operations have working adapters and common UI access, and special disabled entries are visibly labeled with exact prerequisites.
- All requested communications, external meeting bot, AI agents/voice/inference/training/RAG and storage have tested domain views and correct actions.
- The model-visible default is at most four tools with the generator directly advertised; context/performance budgets are measured and met without losing output/schema correctness.
- BYOK key and OAuth paths, client capability handlers, tenant isolation, native task persistence and resource lifecycles pass real transport tests.
- External agents can render and interact; embedded applications can mount themed views; facilitator text/tool/UI claims have the corresponding native-runtime evidence. A blocked facilitator UI bridge is reported as incomplete rather than hidden.
- Actual browser media support is reported per host/version/network; only tested capabilities are claimed. Meeting bots are not implemented for Telnyx Rooms.
- Full tests/build/type/lint and all F1-F4 verdicts pass, with teardown receipts for owned resources and no reliance on fabricated provider guarantees.
