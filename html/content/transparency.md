## What is verified now

The source plan is grounded in the local Telnyx schema, installed FastMCP 4.0.10, MCP 2.2.0 and Prefab 0.20.2, plus official documentation. The local schema contains 933 paths, 1,382 operations and 96 webhook reference definitions. Earlier answers mixed paths and operations; this document uses operation counts where stated.

A no-network FastMCP composition probe produced the four requested model tools and retained native UI metadata on the directly advertised generator. A child arithmetic tool executed through Code Mode. The initial probe listing was 6,527 bytes. The probe did not call Telnyx or exercise a browser UI.

Native GenerativeUI's actual source registers code/data execution, component lookup and the renderer resource. Prefab exposes themes and CSS. Official AppBridge documentation exposes a host-supplied tool-handler mode, so the embed can keep its connection and long-lived account credential in the application backend.

## What is proposed application glue

Domain recipes, the Store workspace page, source-aware Omni Inbox, per-user credential binding, small client packaging, event correlation and explicit policy are the code we plan to build around those existing primitives. They are not already shipped framework features. The plan minimizes this glue and reuses native lifecycle, auth, stores, task management and UI actions.

The requested Telnyx KV adapter must be contract-tested. It can store account-owned documents/preferences, but its existence does not establish transactional isolation or make it a supported Docket backend. Namespace setup is explicit; the first ordinary user read must not silently create account resources.

## Compatibility gates that must pass

| Gate | What the existing evidence supports | What still needs real proof |
|---|---|---|
| OAuth for Oubliai | Telnyx advertises OAuth/DCR/PKCE. | Correct resource-bound issuer/audience and a complete user login/credential-forwarding path; never disable audience checks. |
| Facilitator tool execution | Telnyx has assistant chat and MCP/tool configuration. | Native runtime authenticates as the right user and calls the compact execution surface. |
| Facilitator-generated widget delivery | Assistant chat returns text and optionally text deltas. | Real generator/tool UI payload or artifact reaches AppBridge. Text success alone is insufficient. |
| Native generator embedding | Renderer metadata and official AppBridge API exist. | Browser host load, input/partial/final lifecycle, actions, CSP and teardown on the actual versions. |
| Host design-system matching | Host style variables and native Prefab themes exist. | Token mapping, first-render computed styles, fonts and live theme switching in two host fixtures. |
| Live media | Telnyx browser SDK and permission-request primitives exist. | Actual host permission grants, SDK signaling/ICE, audio/video, supervisor topology and teardown. |
| Special API protocols | Spec identifies alternate hosts, streams and socket operations. | Correct official adapter/wire semantics. Disabled entries stay visibly disabled until proven. |
| Channel webhook ingestion | Endpoint/event references exist for parts of the platform. | Signing/event contract for each actual channel, raw body verification, account correlation, delivery behavior. |

## Things the plan explicitly does not claim

- Zero model context use. Discovery, schemas and chosen results necessarily consume context; we measure and bound them.
- Automatic rollback of a remote tool chain or exactly-once Telnyx mutations after ambiguous failure.
- A native all-channel shared inbox, complete historical channel data, or automatic phone/email identity matching.
- Mic/WebRTC forbidden in every MCP Apps host—or guaranteed in every host. Permissions are host-dependent and tested.
- Native Meeting Bot support for Telnyx Rooms. The user requested external meeting platforms only.
- A general-purpose training platform beyond the actual model/job constraints of documented Telnyx fine-tuning operations.
- Every auth provider, transform and storage backend enabled simultaneously. Alternative FastMCP profiles are accounted for without bloating the default product.

## Review and document status

This is an implementation plan and a document deliverable, not a running product. Test commands and implementation files in the roadmap describe future work unless explicitly labeled as an already-run local probe.

Independent read-only review was attempted, but the available reviewer endpoint returned an authentication error. No independent approval is claimed. Document-browser checks and screenshots, when recorded in the local QA report, prove only the readability/navigation of this HTML dossier. They do not prove the future Telnyx server, facilitator, client or media integrations.

The earlier plan and its accumulating addenda are superseded by the rewritten plan. Where a requested capability cannot be established using the native runtime, the implementation must report the exact blocker instead of quietly inventing a replacement.
