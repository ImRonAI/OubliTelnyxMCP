# ai

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| POST | /10dlc/brand/{brandId}/2faEmail | ResendBrand2faEmail | Brands |
| GET | /10dlc/campaign | GetCampaigns | Campaign |
| POST | /10dlc/campaign/acceptSharing/{campaignId} | AcceptCampaign | Campaign |
| GET | /10dlc/campaign/usecase/cost | GetCampaignCost | Campaign |
| GET | /10dlc/campaign/usecase_cost | GetCampaignCost_2 | Campaign |
| GET | /10dlc/campaign/{campaignId} | GetCampaign | Campaign |
| PUT | /10dlc/campaign/{campaignId} | UpdateCampaign | Campaign |
| DELETE | /10dlc/campaign/{campaignId} | DeactivateCampaign | Campaign |
| POST | /10dlc/campaign/{campaignId}/appeal | AppealCampaign | Campaign |
| GET | /10dlc/campaign/{campaignId}/mnoMetadata | GetCampaignMnoMetadata | Campaign |
| GET | /10dlc/campaign/{campaignId}/operationStatus | GetCampaignOperationStatus | Campaign |
| GET | /10dlc/campaign/{campaignId}/osr/attributes | GetCampaignOsrAttributes | Campaign |
| GET | /10dlc/campaign/{campaignId}/osr_attributes | GetCampaignOsrAttributes_2 | Campaign |
| GET | /10dlc/campaign/{campaignId}/sharing | GetCampaignSharingStatus | Campaign |
| POST | /10dlc/campaignBuilder | PostCampaign | Campaign |
| GET | /10dlc/campaignBuilder/brand/{brandId}/usecase/{usecase} | GetUsecaseQualification | Campaign |
| GET | /10dlc/partnerCampaign/sharedByMe | GetPartnerCampaignsSharedByUser | Shared Campaigns |
| GET | /10dlc/partnerCampaign/{campaignId}/sharing | GetPartnerCampaignSharingStatus | Shared Campaigns |
| GET | /10dlc/partner_campaigns | GetSharedCampaigns | Shared Campaigns |
| GET | /10dlc/partner_campaigns/{campaignId} | GetSharedCampaign | Shared Campaigns |
| PATCH | /10dlc/partner_campaigns/{campaignId} | UpdateSharedCampaign | Shared Campaigns |
| POST | /10dlc/phoneNumberAssignmentByProfile | PostAssignMessagingProfileToCampaign | Bulk Phone Number Campaigns |
| GET | /10dlc/phoneNumberAssignmentByProfile/{taskId} | GetAssignmentTaskStatus | Bulk Phone Number Campaigns |
| GET | /10dlc/phoneNumberAssignmentByProfile/{taskId}/phoneNumbers | GetPhoneNumberStatus | Bulk Phone Number Campaigns |
| GET | /10dlc/phone_number_campaigns | GetAllPhoneNumberCampaigns | Phone Number Campaigns |
| POST | /10dlc/phone_number_campaigns | CreatePhoneNumberCampaign | Phone Number Campaigns |
| GET | /10dlc/phone_number_campaigns/{phoneNumber} | GetSinglePhoneNumberCampaign | Phone Number Campaigns |
| PUT | /10dlc/phone_number_campaigns/{phoneNumber} | PutPhoneNumberCampaign | Phone Number Campaigns |
| DELETE | /10dlc/phone_number_campaigns/{phoneNumber} | DeletePhoneNumberCampaign | Phone Number Campaigns |
| POST | /ai/anthropic/v1/messages | create_anthropic_message | Anthropic Messages |
| GET | /ai/assistants | get_assistants_public_assistants_get | Assistants |
| POST | /ai/assistants | create_new_assistant_public_assistants_post | Assistants |
| POST | /ai/assistants/import | import_assistants_public_assistants_import_post | Assistants |
| GET | /ai/assistants/tags | get_all_assistant_tags | Assistants |
| GET | /ai/assistants/tests | get_assistant_tests_public_assistants_tests_get | Assistants |
| POST | /ai/assistants/tests | create_assistant_test_public_assistants_tests_post | Assistants |
| GET | /ai/assistants/tests/test-suites | fetch_test_suites_public_assistants_tests_test_suites_get | Assistants |
| GET | /ai/assistants/tests/test-suites/{suite_name}/runs | ListTestSuiteRuns | Assistants |
| POST | /ai/assistants/tests/test-suites/{suite_name}/runs | TriggerTestSuiteRuns | Assistants |
| GET | /ai/assistants/tests/{test_id} | get_assistant_test_public_assistants_tests__test_id__get | Assistants |
| PUT | /ai/assistants/tests/{test_id} | update_assistant_test_public_assistants_tests__test_id__put | Assistants |
| DELETE | /ai/assistants/tests/{test_id} | delete_assistant_test_public_assistants_tests__test_id__delete | Assistants |
| GET | /ai/assistants/tests/{test_id}/runs | ListTestRuns | Assistants |
| POST | /ai/assistants/tests/{test_id}/runs | trigger_test_run_public_assistants_tests__test_id__runs_post | Assistants |
| GET | /ai/assistants/tests/{test_id}/runs/{run_id} | get_test_run_public_assistants_tests__test_id__runs__run_id__get | Assistants |
| GET | /ai/assistants/{assistant_id} | get_assistant_public_assistants__assistant_id__get | Assistants |
| POST | /ai/assistants/{assistant_id} | update_assistant_public_assistants__assistant_id__post | Assistants |
| DELETE | /ai/assistants/{assistant_id} | delete_assistant_public_assistants__assistant_id__delete | Assistants |
| GET | /ai/assistants/{assistant_id}/canary-deploys | get_canary_deploy_assistants__assistant_id__canary_deploys_get | Assistants |
| POST | /ai/assistants/{assistant_id}/canary-deploys | CreateCanaryDeploy | Assistants |
| PUT | /ai/assistants/{assistant_id}/canary-deploys | UpdateCanaryDeploy | Assistants |
| DELETE | /ai/assistants/{assistant_id}/canary-deploys | DeleteCanaryDeploy | Assistants |
| POST | /ai/assistants/{assistant_id}/chat | assistant_chat_public_assistants__assistant_id__chat_post | Assistants |
| POST | /ai/assistants/{assistant_id}/chat/sms | assistant_sms_chat_assistants__assistant_id__chat_sms_post | Assistants |
| POST | /ai/assistants/{assistant_id}/clone | clone_assistant_public_assistants__assistant_id__clone_post | Assistants |
| POST | /ai/assistants/{assistant_id}/instructions/enhance | enhance_assistant_instructions_public_assistants__assist_14cwph5 | Assistants |
| GET | /ai/assistants/{assistant_id}/scheduled_events | get_scheduled_events | Assistants |
| POST | /ai/assistants/{assistant_id}/scheduled_events | create_scheduled_event | Assistants |
| GET | /ai/assistants/{assistant_id}/scheduled_events/{event_id} | get_scheduled_event | Assistants |
| DELETE | /ai/assistants/{assistant_id}/scheduled_events/{event_id} | delete_scheduled_event | Assistants |
| POST | /ai/assistants/{assistant_id}/tags | add_assistant_tag | Assistants |
| DELETE | /ai/assistants/{assistant_id}/tags/{tag} | remove_assistant_tag | Assistants |
| GET | /ai/assistants/{assistant_id}/texml | get_assistant_texml_public_assistants__assistant_id__texml_get | Assistants |
| PUT | /ai/assistants/{assistant_id}/tools/{tool_id} | add_assistant_tool | Assistants |
| DELETE | /ai/assistants/{assistant_id}/tools/{tool_id} | remove_assistant_tool | Assistants |
| POST | /ai/assistants/{assistant_id}/tools/{tool_id}/test | TestAssistantTool | Assistants |
| GET | /ai/assistants/{assistant_id}/versions | ListAssistantVersions | Assistants |
| GET | /ai/assistants/{assistant_id}/versions/{version_id} | GetAssistantVersion | Assistants |
| POST | /ai/assistants/{assistant_id}/versions/{version_id} | UpdateAssistantVersion | Assistants |
| DELETE | /ai/assistants/{assistant_id}/versions/{version_id} | DeleteAssistantVersion | Assistants |
| POST | /ai/assistants/{assistant_id}/versions/{version_id}/promote | PromoteAssistantVersion | Assistants |
| POST | /ai/audio/transcriptions | audio_public_audio_transcriptions_post | Audio |
| POST | /ai/chat/completions | chat_public_chat_completions_post | Chat |
| GET | /ai/clusters | list_all_requested_clusters_public_text_clusters_get | Clusters |
| POST | /ai/clusters | compute_new_cluster_public_text_clusters_post | Clusters |
| GET | /ai/clusters/{task_id} | fetch_cluster_by_task_id_public_text_clusters__task_id__get | Clusters |
| DELETE | /ai/clusters/{task_id} | delete_cluster_by_task_id_public_text_clusters__task_id__delete | Clusters |
| GET | /ai/clusters/{task_id}/graph | GetClusterImage | Clusters |
| GET | /ai/collections | ListCollections | AI Collections |
| POST | /ai/collections | CreateCollection | AI Collections |
| GET | /ai/collections/slug/{slug} | GetCollectionBySlug | AI Collections |
| GET | /ai/collections/{uuid} | GetCollection | AI Collections |
| PATCH | /ai/collections/{uuid} | UpdateCollection | AI Collections |
| DELETE | /ai/collections/{uuid} | DeleteCollection | AI Collections |
| GET | /ai/collections/{uuid}/settings | GetCollectionSettings | AI Collections |
| PUT | /ai/collections/{uuid}/settings | ReplaceCollectionSettings | AI Collections |
| PATCH | /ai/collections/{uuid}/settings | UpdateCollectionSettings | AI Collections |
| GET | /ai/collections/{uuid}/sources | ListCollectionSources | AI Collections |
| POST | /ai/collections/{uuid}/sources | AddCollectionSource | AI Collections |
| PUT | /ai/collections/{uuid}/sources | ReplaceCollectionSources | AI Collections |
| DELETE | /ai/collections/{uuid}/sources/{sourceId} | RemoveCollectionSource | AI Collections |
| GET | /ai/conversation_histories | SearchConversationHistories | Conversation Histories |
| GET | /ai/conversations | get_conversations_public_conversations_get | Conversations |
| POST | /ai/conversations | create_new_conversation_public_conversations_post | Conversations |
| GET | /ai/conversations/conversation-insights/aggregates | aggregate_conversation_insights | Conversations |
| GET | /ai/conversations/insight-groups | get_all_insight_groups | Conversations |
| POST | /ai/conversations/insight-groups | create_insight_group | Conversations |
| GET | /ai/conversations/insight-groups/{group_id} | get_insight_group_by_id | Conversations |
| PUT | /ai/conversations/insight-groups/{group_id} | update_insight_group_by_id | Conversations |
| DELETE | /ai/conversations/insight-groups/{group_id} | delete_insight_group_by_id | Conversations |
| POST | /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/assign | assign_insight_to_group | Conversations |
| DELETE | /ai/conversations/insight-groups/{group_id}/insights/{insight_id}/unassign | unassign_insight_from_group | Conversations |
| GET | /ai/conversations/insights | get_all_insights | Conversations |
| POST | /ai/conversations/insights | create_insight | Conversations |
| GET | /ai/conversations/insights/{insight_id} | get_insight_by_id | Conversations |
| PUT | /ai/conversations/insights/{insight_id} | update_insight_by_id | Conversations |
| DELETE | /ai/conversations/insights/{insight_id} | delete_insight_by_id | Conversations |
| GET | /ai/conversations/{conversation_id} | get_conversation_by_id_public_conversations_get | Conversations |
| PUT | /ai/conversations/{conversation_id} | update_conversation_by_id_public_conversations_put | Conversations |
| DELETE | /ai/conversations/{conversation_id} | delete_conversation_by_id_public_conversations_delete | Conversations |
| GET | /ai/conversations/{conversation_id}/conversations-insights | get_conversations_public__conversation_id__insights_get | Conversations |
| POST | /ai/conversations/{conversation_id}/message | add_new_message | Conversations |
| GET | /ai/conversations/{conversation_id}/messages | get_conversations_public__conversation_id__messages_get | Conversations |
| GET | /ai/embeddings | GetTasksByStatus | Embeddings |
| POST | /ai/embeddings | PostEmbedding | Embeddings |
| GET | /ai/embeddings/buckets | GetEmbeddingBuckets | Embeddings |
| GET | /ai/embeddings/buckets/{bucket_name} | GetBucketName | Embeddings |
| DELETE | /ai/embeddings/buckets/{bucket_name} | DeleteEmbeddingBucket | Embeddings |
| POST | /ai/embeddings/similarity-search | PostEmbeddingSimilaritySearch | Embeddings |
| POST | /ai/embeddings/url | PostEmbeddingUrl | Embeddings |
| GET | /ai/embeddings/{task_id} | GetEmbeddingTask | Embeddings |
| GET | /ai/fine_tuning/jobs | get_finetuningjob_public_finetuning_get | Fine Tuning |
| POST | /ai/fine_tuning/jobs | create_new_finetuningjob_public_finetuning_post | Fine Tuning |
| GET | /ai/fine_tuning/jobs/{job_id} | get_finetuningjob_public_finetuning__job_id__get | Fine Tuning |
| POST | /ai/fine_tuning/jobs/{job_id}/cancel | cancel_new_finetuningjob_public_finetuning_post | Fine Tuning |
| GET | /ai/integrations | list_integrations_public_integrations_get | Integrations |
| GET | /ai/integrations/connections | list_user_integrations_public_integrations_connections_get | Integrations |
| GET | /ai/integrations/connections/{user_connection_id} | GetUserIntegration | Integrations |
| DELETE | /ai/integrations/connections/{user_connection_id} | delete_integration_connection | Integrations |
| GET | /ai/integrations/{integration_id} | list_integration_by_id_public_integrations__integration_id__get | Integrations |
| GET | /ai/knowledge/collections/{slug}/documents | SearchCollectionDocuments | AI Collections |
| GET | /ai/mcp_servers | list_mcp_servers | MCP Servers |
| POST | /ai/mcp_servers | create_mcp_server | MCP Servers |
| GET | /ai/mcp_servers/{mcp_server_id} | get_mcp_server | MCP Servers |
| PUT | /ai/mcp_servers/{mcp_server_id} | update_mcp_server | MCP Servers |
| DELETE | /ai/mcp_servers/{mcp_server_id} | delete_mcp_server | MCP Servers |
| GET | /ai/memory/namespaces/{namespace}/operations/{operation_id} | GetMemoryOperation | Operations |
| GET | /ai/memory/namespaces/{namespace}/profiles | ListMemoryProfiles | Profiles |
| DELETE | /ai/memory/namespaces/{namespace}/profiles/{profile_id} | ForgetProfile | Profiles |
| POST | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/ingest | IngestSession | Memory |
| GET | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/memories | ListMemories | Profiles |
| GET | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/memories/{memory_id} | GetMemory | Profiles |
| POST | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/recall | RecallMemories | Memory |
| POST | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/remember | RememberFact | Memory |
| GET | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/sources | ListMemorySources | Sources |
| GET | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/sources/{source_id} | GetMemorySource | Sources |
| DELETE | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/sources/{source_id} | ForgetSource | Sources |
| GET | /ai/memory/namespaces/{namespace}/profiles/{profile_id}/summary | GetProfileSummary | Memory |
| GET | /ai/memory/namespaces/{namespace}/settings | GetNamespaceSettings | Settings |
| PATCH | /ai/memory/namespaces/{namespace}/settings | UpdateNamespaceSettings | Settings |
| GET | /ai/missions | get_public_missions_missions | Missions |
| POST | /ai/missions | post_public_missions_missions | Missions |
| GET | /ai/missions/events | get_public_missions_missions_events | Missions |
| GET | /ai/missions/runs | get_public_missions_missions_runs | Missions |
| GET | /ai/missions/{mission_id} | get_public_missions_missions_mission_id | Missions |
| PUT | /ai/missions/{mission_id} | put_public_missions_missions_mission_id | Missions |
| DELETE | /ai/missions/{mission_id} | delete_public_missions_missions_mission_id | Missions |
| POST | /ai/missions/{mission_id}/clone | post_public_missions_missions_mission_id_clone | Missions |
| GET | /ai/missions/{mission_id}/knowledge-bases | get_public_missions_missions_mission_id_knowledge_bases | Missions |
| POST | /ai/missions/{mission_id}/knowledge-bases | post_public_missions_missions_mission_id_knowledge_bases | Missions |
| GET | /ai/missions/{mission_id}/knowledge-bases/{knowledge_base_id} | GetMissionKnowledgeBase | Missions |
| PUT | /ai/missions/{mission_id}/knowledge-bases/{knowledge_base_id} | PutMissionKnowledgeBase | Missions |
| DELETE | /ai/missions/{mission_id}/knowledge-bases/{knowledge_base_id} | DeleteMissionKnowledgeBase | Missions |
| GET | /ai/missions/{mission_id}/mcp-servers | get_public_missions_missions_mission_id_mcp_servers | Missions |
| POST | /ai/missions/{mission_id}/mcp-servers | post_public_missions_missions_mission_id_mcp_servers | Missions |
| GET | /ai/missions/{mission_id}/mcp-servers/{mcp_server_id} | GetMissionMcpServer | Missions |
| PUT | /ai/missions/{mission_id}/mcp-servers/{mcp_server_id} | PutMissionMcpServer | Missions |
| DELETE | /ai/missions/{mission_id}/mcp-servers/{mcp_server_id} | DeleteMissionMcpServer | Missions |
| GET | /ai/missions/{mission_id}/runs | get_public_missions_missions_mission_id_runs | Missions |
| POST | /ai/missions/{mission_id}/runs | post_public_missions_missions_mission_id_runs | Missions |
| GET | /ai/missions/{mission_id}/runs/{run_id} | get_public_missions_missions_mission_id_runs_run_id | Missions |
| PATCH | /ai/missions/{mission_id}/runs/{run_id} | patch_public_missions_missions_mission_id_runs_run_id | Missions |
| POST | /ai/missions/{mission_id}/runs/{run_id}/cancel | post_public_missions_missions_mission_id_runs_run_id_cancel | Missions |
| GET | /ai/missions/{mission_id}/runs/{run_id}/events | get_public_missions_missions_mission_id_runs_run_id_events | Missions |
| POST | /ai/missions/{mission_id}/runs/{run_id}/events | post_public_missions_missions_mission_id_runs_run_id_events | Missions |
| GET | /ai/missions/{mission_id}/runs/{run_id}/events/{event_id} | GetMissionRunEvent | Missions |
| POST | /ai/missions/{mission_id}/runs/{run_id}/pause | post_public_missions_missions_mission_id_runs_run_id_pause | Missions |
| GET | /ai/missions/{mission_id}/runs/{run_id}/plan | get_public_missions_missions_mission_id_runs_run_id_plan | Missions |
| POST | /ai/missions/{mission_id}/runs/{run_id}/plan | post_public_missions_missions_mission_id_runs_run_id_plan | Missions |
| POST | /ai/missions/{mission_id}/runs/{run_id}/plan/steps | post_public_missions_missions_mission_id_runs_run_id_plan_steps | Missions |
| GET | /ai/missions/{mission_id}/runs/{run_id}/plan/steps/{step_id} | GetMissionRunStep | Missions |
| PATCH | /ai/missions/{mission_id}/runs/{run_id}/plan/steps/{step_id} | UpdateMissionRunStep | Missions |
| POST | /ai/missions/{mission_id}/runs/{run_id}/resume | post_public_missions_missions_mission_id_runs_run_id_resume | Missions |
| GET | /ai/missions/{mission_id}/runs/{run_id}/telnyx-agents | ListMissionRunAgents | Missions |
| POST | /ai/missions/{mission_id}/runs/{run_id}/telnyx-agents | CreateMissionRunAgent | Missions |
| DELETE | /ai/missions/{mission_id}/runs/{run_id}/telnyx-agents/{telnyx_agent_id} | DeleteMissionRunAgent | Missions |
| GET | /ai/missions/{mission_id}/tools | get_public_missions_missions_mission_id_tools | Missions |
| POST | /ai/missions/{mission_id}/tools | post_public_missions_missions_mission_id_tools | Missions |
| GET | /ai/missions/{mission_id}/tools/{tool_id} | get_public_missions_missions_mission_id_tools_tool_id | Missions |
| PUT | /ai/missions/{mission_id}/tools/{tool_id} | put_public_missions_missions_mission_id_tools_tool_id | Missions |
| DELETE | /ai/missions/{mission_id}/tools/{tool_id} | delete_public_missions_missions_mission_id_tools_tool_id | Missions |
| GET | /ai/models | get_models_public_models_get | Chat |
| POST | /ai/openai/chat/completions | create_openai_chat_completion | OpenAI Chat |
| POST | /ai/openai/embeddings | create_openai_embeddings | OpenAI Embeddings |
| GET | /ai/openai/embeddings/models | list_openai_embedding_models | OpenAI Embeddings |
| GET | /ai/openai/models | list_openai_models | OpenAI Chat |
| POST | /ai/openai/responses | chat_public_openai_responses_completions_post | OpenAI Chat |
| POST | /ai/responses | chat_public_responses_completions_post | Chat |
| POST | /ai/summarize | PostSummary | Chat |
| GET | /ai/tools | list_tools | Assistants |
| POST | /ai/tools | create_tool_post | Assistants |
| GET | /ai/tools/{tool_id} | get_tool_tool_id | Assistants |
| PATCH | /ai/tools/{tool_id} | update_tool_tool_id | Assistants |
| DELETE | /ai/tools/{tool_id} | delete_tool_tool_id | Assistants |
| POST | /ai/typesafe/v1/systemone | create_typesafe_systemone | Decision Models |
| GET | /available_phone_number_blocks | ListAvailablePhoneNumberBlocks | Phone Number Search |
| GET | /available_phone_numbers | ListAvailablePhoneNumbers | Phone Number Search |
| GET | /balance | GetUserBalance | Billing |
| GET | /bulk_sim_card_actions/{id} | GetBulkSimCardAction | SIM Card Actions |
| POST | /calls/{call_control_id}/actions/ai_assistant_add_messages | CallAddMessagesToAIAssistant | Call Commands |
| POST | /calls/{call_control_id}/actions/ai_assistant_join | CallJoinAIAssistant | Call Commands |
| POST | /calls/{call_control_id}/actions/ai_assistant_start | CallStartAIAssistant | Call Commands |
| POST | /calls/{call_control_id}/actions/ai_assistant_stop | CallStopAIAssistant | Call Commands |
| POST | /calls/{call_control_id}/actions/gather_using_ai | callGatherUsingAI | Call Commands |
| GET | /detail_records | SearchDetailRecords | Detail Records |
| GET | /dir/{dir_id}/infringement_claims | listInfringementClaimsForDir | Infringement Claims |
| PUT | /dir/{dir_id}/infringement_update | updateDirInfringement | Infringement Claims |
| GET | /dir/{dir_id}/verify_email | getDirEmailVerificationStatus | Email Verification |
| POST | /dir/{dir_id}/verify_email | requestDirEmailVerification | Email Verification |
| POST | /dir/{dir_id}/verify_email/confirm | confirmDirEmailVerification | Email Verification |
| GET | /email_blocks | listEmailBlocks | Email Suppressions |
| POST | /email_blocks | createEmailBlock | Email Suppressions |
| GET | /email_blocks/export | exportEmailBlocks | Email Suppressions |
| POST | /email_blocks/import | createEmailBlockImport | Email Suppression Imports |
| GET | /email_blocks/import/{id} | showEmailBlockImport | Email Suppression Imports |
| GET | /email_blocks/{id} | showEmailBlock | Email Suppressions |
| DELETE | /email_blocks/{id} | deleteEmailBlock | Email Suppressions |
| GET | /email_blocks/{id}/events | listEmailBlockEvents | Email Suppressions |
| GET | /email_domains | listEmailDomains | Email Domains |
| POST | /email_domains | createEmailDomain | Email Domains |
| GET | /email_domains/{domain_id}/dns_records | listEmailDomainDnsRecords | Email Domain DNS Records |
| POST | /email_domains/{domain_id}/rotate_dkim | rotateEmailDomainDKIMKey | Email Domains |
| POST | /email_domains/{domain_id}/verify | verifyEmailDomainDnsRecords | Email Domain DNS Records |
| GET | /email_domains/{domain_id}/webhooks | listEmailDomainWebhooks | Email Webhooks |
| POST | /email_domains/{domain_id}/webhooks | createEmailDomainWebhook | Email Webhooks |
| GET | /email_domains/{domain_id}/webhooks/{id} | getEmailDomainWebhook | Email Webhooks |
| PATCH | /email_domains/{domain_id}/webhooks/{id} | updateEmailDomainWebhook | Email Webhooks |
| DELETE | /email_domains/{domain_id}/webhooks/{id} | deleteEmailDomainWebhook | Email Webhooks |
| GET | /email_domains/{id} | getEmailDomain | Email Domains |
| PATCH | /email_domains/{id} | updateEmailDomain | Email Domains |
| DELETE | /email_domains/{id} | deleteEmailDomain | Email Domains |
| GET | /email_domains/{id}/health | getEmailDomainHealth | Email Domains |
| GET | /email_events | ListEmailEvents | Email Events |
| GET | /email_events/stats | GetEmailEventStats | Email Events |
| GET | /email_inboxes | ListEmailInboxes | Email Inboxes |
| POST | /email_inboxes | CreateEmailInbox | Email Inboxes |
| GET | /email_inboxes/{id} | GetEmailInbox | Email Inboxes |
| DELETE | /email_inboxes/{id} | DeleteEmailInbox | Email Inboxes |
| GET | /email_inboxes/{inbox_id}/drafts | ListEmailDrafts | Email Drafts |
| POST | /email_inboxes/{inbox_id}/drafts | CreateEmailDraft | Email Drafts |
| GET | /email_inboxes/{inbox_id}/drafts/{draft_id} | GetEmailDraft | Email Drafts |
| PUT | /email_inboxes/{inbox_id}/drafts/{draft_id} | UpdateEmailDraft | Email Drafts |
| PATCH | /email_inboxes/{inbox_id}/drafts/{draft_id} | PatchEmailDraft | Email Drafts |
| DELETE | /email_inboxes/{inbox_id}/drafts/{draft_id} | DeleteEmailDraft | Email Drafts |
| POST | /email_inboxes/{inbox_id}/drafts/{draft_id}/send | SendEmailDraft | Email Drafts |
| GET | /email_inboxes/{inbox_id}/filters | ListEmailInboxFilters | Email Inboxes |
| POST | /email_inboxes/{inbox_id}/filters | AddEmailInboxFilterEntries | Email Inboxes |
| PUT | /email_inboxes/{inbox_id}/filters | ReplaceEmailInboxFilters | Email Inboxes |
| DELETE | /email_inboxes/{inbox_id}/filters | RemoveEmailInboxFilterEntries | Email Inboxes |
| GET | /email_inboxes/{inbox_id}/messages | ListEmailInboxMessages | Email Inboxes |
| PATCH | /email_inboxes/{inbox_id}/messages/{message_id} | UpdateEmailInboxMessage | Email Inboxes |
| POST | /email_inboxes/{inbox_id}/messages/{message_id}/actions/forward | ForwardEmailInboxMessage | Email Inboxes |
| POST | /email_inboxes/{inbox_id}/messages/{message_id}/actions/reply | ReplyToEmailInboxMessage | Email Inboxes |
| POST | /email_inboxes/{inbox_id}/messages/{message_id}/actions/reply_all | ReplyAllToEmailInboxMessage | Email Inboxes |
| POST | /email_inboxes/{inbox_id}/messages/{message_id}/drafts | CreateEmailReplyDraft | Email Drafts |
| POST | /email_inboxes/{inbox_id}/messages/{message_id}/labels | AddEmailInboxMessageLabels | Email Inboxes |
| DELETE | /email_inboxes/{inbox_id}/messages/{message_id}/labels | RemoveEmailInboxMessageLabels | Email Inboxes |
| GET | /email_inboxes/{inbox_id}/threads | ListEmailInboxThreads | Email Inboxes |
| GET | /email_inboxes/{inbox_id}/threads/{thread_id} | GetEmailInboxThread | Email Inboxes |
| POST | /email_inboxes/{inbox_id}/threads/{thread_id}/labels | AddEmailInboxThreadLabels | Email Inboxes |
| DELETE | /email_inboxes/{inbox_id}/threads/{thread_id}/labels | RemoveEmailInboxThreadLabels | Email Inboxes |
| GET | /email_messages | ListEmailMessages | Email Messages |
| POST | /email_messages | CreateEmailMessage | Email Messages |
| DELETE | /email_messages | DeleteEmailMessagesByAddress | Email Messages |
| POST | /email_messages/batch | CreateEmailMessageBatch | Email Messages |
| GET | /email_messages/{email_id}/events | ListEmailMessageEvents | Email Messages |
| GET | /email_messages/{email_id}/recipients | ListEmailMessageRecipients | Email Messages |
| GET | /email_messages/{email_id}/recipients/{recipient_id} | GetEmailMessageRecipient | Email Messages |
| PATCH | /email_messages/{email_id}/schedule | RescheduleEmailMessage | Email Messages |
| DELETE | /email_messages/{email_id}/schedule | CancelScheduledEmailMessage | Email Messages |
| GET | /email_messages/{id} | GetEmailMessage | Email Messages |
| DELETE | /email_messages/{id} | DeleteEmailMessage | Email Messages |
| GET | /email_templates | ListEmailTemplates | Email Templates |
| POST | /email_templates | CreateEmailTemplate | Email Templates |
| GET | /email_templates/{id} | GetEmailTemplate | Email Templates |
| PUT | /email_templates/{id} | ReplaceEmailTemplate | Email Templates |
| PATCH | /email_templates/{id} | UpdateEmailTemplate | Email Templates |
| DELETE | /email_templates/{id} | DeleteEmailTemplate | Email Templates |
| POST | /email_templates/{id}/render | RenderEmailTemplate | Email Templates |
| GET | /email_threads | ListEmailThreads | Email Threads |
| GET | /email_threads/{thread_id} | GetEmailThread | Email Threads |
| GET | /email_unsubscribe_groups | listUnsubscribeGroups | Email Unsubscribe Groups |
| POST | /email_unsubscribe_groups | createUnsubscribeGroup | Email Unsubscribe Groups |
| GET | /email_unsubscribe_groups/{id} | showUnsubscribeGroup | Email Unsubscribe Groups |
| PATCH | /email_unsubscribe_groups/{id} | updateUnsubscribeGroup | Email Unsubscribe Groups |
| DELETE | /email_unsubscribe_groups/{id} | deleteUnsubscribeGroup | Email Unsubscribe Groups |
| GET | /email_unsubscribe_groups/{id}/suppressions | listGroupSuppressions | Email Unsubscribe Groups |
| POST | /email_unsubscribe_groups/{id}/suppressions | addGroupSuppression | Email Unsubscribe Groups |
| DELETE | /email_unsubscribe_groups/{id}/suppressions/{email} | removeGroupSuppression | Email Unsubscribe Groups |
| POST | /email_validations | CreateEmailValidation | Email Validations |
| POST | /email_validations/batch | CreateEmailValidationBatch | Email Validations |
| GET | /email_validations/batch/{id} | GetEmailValidationBatch | Email Validations |
| GET | /external_requirements/{regulatory_requirement_id}/sub_number_orders/{sub_number_order_id} | getExternalRequirement | Requirement Groups |
| GET | /infringement_claims/{claim_id} | getInfringementClaim | Infringement Claims |
| POST | /infringement_claims/{claim_id}/contest | contestInfringementClaim | Infringement Claims |
| GET | /legacy/reporting/batch/detail/records/speech/to/text | getSttRequests | Speech to Text Batch Reports |
| POST | /legacy/reporting/batch/detail/records/speech/to/text | submitSttRequest | Speech to Text Batch Reports |
| GET | /legacy/reporting/batch/detail/records/speech/to/text/{id} | getSttRequest | Speech to Text Batch Reports |
| DELETE | /legacy/reporting/batch/detail/records/speech/to/text/{id} | deleteSttRequest | Speech to Text Batch Reports |
| GET | /legacy/reporting/batch_detail_records/messaging | getMdrRequests | MDR Detailed Reports |
| POST | /legacy/reporting/batch_detail_records/messaging | submitMdrRequest | MDR Detailed Reports |
| GET | /legacy/reporting/batch_detail_records/messaging/{id} | getMdrRequest | MDR Detailed Reports |
| DELETE | /legacy/reporting/batch_detail_records/messaging/{id} | deleteMdrRequest | MDR Detailed Reports |
| GET | /legacy/reporting/batch_detail_records/speech_to_text | getSttRequests_2 | Speech to Text Batch Reports |
| POST | /legacy/reporting/batch_detail_records/speech_to_text | submitSttRequest_2 | Speech to Text Batch Reports |
| GET | /legacy/reporting/batch_detail_records/speech_to_text/{id} | getSttRequest_2 | Speech to Text Batch Reports |
| DELETE | /legacy/reporting/batch_detail_records/speech_to_text/{id} | deleteSttRequest_2 | Speech to Text Batch Reports |
| GET | /legacy/reporting/batch_detail_records/voice | getCdrRequests | CDR Reports |
| POST | /legacy/reporting/batch_detail_records/voice | submitCdrRequest | CDR Reports |
| GET | /legacy/reporting/batch_detail_records/voice/fields | getCdrsAvailableFields | CDR Reports |
| GET | /legacy/reporting/batch_detail_records/voice/{id} | getCdrRequest | CDR Reports |
| DELETE | /legacy/reporting/batch_detail_records/voice/{id} | deleteCdrRequest | CDR Reports |
| GET | /legacy_reporting/batch_detail_records/messaging | getMdrRequests_2 | MDR Detailed Reports |
| POST | /legacy_reporting/batch_detail_records/messaging | submitMdrRequest_2 | MDR Detailed Reports |
| GET | /legacy_reporting/batch_detail_records/messaging/{id} | getMdrRequest_2 | MDR Detailed Reports |
| DELETE | /legacy_reporting/batch_detail_records/messaging/{id} | deleteMdrRequest_2 | MDR Detailed Reports |
| GET | /legacy_reporting/batch_detail_records/voice | getCdrRequests_2 | CDR Reports |
| POST | /legacy_reporting/batch_detail_records/voice | submitCdrRequest_2 | CDR Reports |
| GET | /legacy_reporting/batch_detail_records/voice/fields | getCdrsAvailableFields_2 | CDR Reports |
| GET | /legacy_reporting/batch_detail_records/voice/{id} | getCdrRequest_2 | CDR Reports |
| DELETE | /legacy_reporting/batch_detail_records/voice/{id} | deleteCdrRequest_2 | CDR Reports |
| GET | /messaging/profiles/{id}/metrics | GetDetailedProfileMetrics | Messaging |
| GET | /messaging_profiles/{id}/metrics | GetDetailedProfileMetrics_2 | Messaging |
| GET | /messaging_url_domains | ListMessagingUrlDomains | Messaging URL Domains |
| GET | /noise_suppression_engines | listNoiseSuppressionEngines | Noise Suppression Engines |
| GET | /phone_numbers/{phone_number_id}/voicemail | GetVoicemail | Voicemail |
| POST | /phone_numbers/{phone_number_id}/voicemail | CreateVoicemail | Voicemail |
| PATCH | /phone_numbers/{phone_number_id}/voicemail | UpdateVoicemail | Voicemail |
| GET | /porting/uk_carriers | listPortingUKCarriers | Porting Orders |
| GET | /reports/mdrs | GetPaginatedMdrs | MDR Detail Reports |
| GET | /reports/wdrs | GetPaginatedWdrs | WDR Detail Reports |
| GET | /sim_card_actions/{id} | GetSimCardAction | SIM Card Actions |
| GET | /sim_card_group_actions/{id} | GetSimCardGroupAction | SIM Card Group Actions |
| GET | /sim_cards/{id}/device_details | GetSimCardDeviceDetails | SIM Cards |
| POST | /storage/sqldbs/{id}/actions/query | QuerySqlDatabase | sql databases |
| POST | /texml/ai_calls/{connection_id} | InitiateTexmlAICall | TeXML REST Commands |
| GET | /text-to-speech/voices | listVoices | Text To Speech Commands |
| GET | /traffic/policy/profiles/services | GetTrafficPolicyProfileServices | Traffic Policy Profiles |
| GET | /traffic_policy_profiles/services | GetTrafficPolicyProfileServices_2 | Traffic Policy Profiles |
| GET | /webhook_deliveries/{id} | GetWebhookDelivery | Webhooks |
| GET | /wireless/detail/records/reports | GetWdrReports | Reporting |
| POST | /wireless/detail/records/reports | CreateWdrReport | Reporting |
| GET | /wireless/detail/records/reports/{id} | GetWdrReport | Reporting |
| DELETE | /wireless/detail/records/reports/{id} | DeleteWdrReport | Reporting |
| GET | /wireless/detail_records_reports | GetWdrReports_2 | Reporting |
| POST | /wireless/detail_records_reports | CreateWdrReport_2 | Reporting |
| GET | /wireless/detail_records_reports/{id} | GetWdrReport_2 | Reporting |
| DELETE | /wireless/detail_records_reports/{id} | DeleteWdrReport_2 | Reporting |
