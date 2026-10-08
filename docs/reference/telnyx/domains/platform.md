# platform

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| GET | /.well-known/oauth-authorization-server | GetOAuthAuthorizationServerMetadata | OAuth Discovery |
| GET | /.well-known/oauth-protected-resource | GetOAuthProtectedResourceMetadata | OAuth Discovery |
| GET | /10dlc/brand | GetBrands | Brands |
| POST | /10dlc/brand | CreateBrandPost | Brands |
| GET | /10dlc/brand/feedback/{brandId} | GetBrandFeedbackById | Brands |
| GET | /10dlc/brand/smsOtp/{referenceId} | GetBrandSmsOtpStatus | Brands |
| GET | /10dlc/brand/{brandId} | GetBrand | Brands |
| PUT | /10dlc/brand/{brandId} | UpdateBrand | Brands |
| DELETE | /10dlc/brand/{brandId} | DeleteBrand | Brands |
| GET | /10dlc/brand/{brandId}/externalVetting | ListExternalVettings | Brands |
| POST | /10dlc/brand/{brandId}/externalVetting | PostOrderExternalVetting | Brands |
| PUT | /10dlc/brand/{brandId}/externalVetting | PutExternalVettingRecord | Brands |
| PUT | /10dlc/brand/{brandId}/revet | RevetBrand | Brands |
| GET | /10dlc/brand/{brandId}/smsOtp | GetBrandSmsOtpStatusByBrandId | Brands |
| POST | /10dlc/brand/{brandId}/smsOtp | TriggerBrandSmsOtp | Brands |
| GET | /10dlc/brand_feedback/{brandId} | GetBrandFeedbackById_2 | Brands |
| GET | /10dlc/enum/{endpoint} | GetEnumEndpoint | Enum |
| GET | /access_ip_address | ListAccessIpAddresses | IP Addresses |
| POST | /access_ip_address | CreateAccessIpAddress | IP Addresses |
| GET | /access_ip_address/{access_ip_address_id} | GetAccessIpAddress | IP Addresses |
| DELETE | /access_ip_address/{access_ip_address_id} | DeleteAccessIpAddress | IP Addresses |
| GET | /access_ip_ranges | ListAccessIpRanges | IP Ranges |
| POST | /access_ip_ranges | CreateAccessIPRange | IP Ranges |
| DELETE | /access_ip_ranges/{access_ip_range_id} | DeleteAccessIpRange | IP Ranges |
| POST | /actions/purchase/esims | PurchaseESim | SIM Cards |
| POST | /actions/register/sim_cards | RegisterSimCards | SIM Cards |
| GET | /addresses | FindAddresses | Addresses |
| POST | /addresses | CreateAddress | Addresses |
| POST | /addresses/actions/validate | ValidateAddress | Addresses |
| GET | /addresses/{id} | GetAddress | Addresses |
| DELETE | /addresses/{id} | DeleteAddress | Addresses |
| GET | /advanced_orders | list_advanced_orders_v2 | Advanced Number Orders |
| POST | /advanced_orders | create_advanced_order_v2 | Advanced Number Orders |
| PATCH | /advanced_orders/{advanced-order-id}/requirement_group | update_advanced_order_v2 | Advanced Number Orders |
| GET | /advanced_orders/{order_id} | get_advanced_order_v2 | Advanced Number Orders |
| GET | /audit_events | ListAuditLogs | Audit Logs |
| GET | /authentication_providers | FindAuthenticationProviders | Authentication Providers |
| POST | /authentication_providers | CreateAuthenticationProvider | Authentication Providers |
| GET | /authentication_providers/{id} | GetAuthenticationProvider | Authentication Providers |
| PATCH | /authentication_providers/{id} | UpdateAuthenticationProvider | Authentication Providers |
| DELETE | /authentication_providers/{id} | DeleteAuthenticationProvider | Authentication Providers |
| GET | /billing_groups | ListBillingGroups | Billing Groups |
| POST | /billing_groups | CreateBillingGroup | Billing Groups |
| GET | /billing_groups/{id} | GetBillingGroup | Billing Groups |
| PATCH | /billing_groups/{id} | UpdateBillingGroup | Billing Groups |
| DELETE | /billing_groups/{id} | DeleteBillingGroup | Billing Groups |
| GET | /bulk_sim_card_actions | ListBulkSimCardActions | SIM Card Actions |
| GET | /bundle_pricing/billing_bundles | GetUserBillingBundles | Bundles |
| GET | /bundle_pricing/billing_bundles/{bundle_id} | GetBillingBundleById | Bundles |
| GET | /bundle_pricing/user_bundles | GetUserBundles | User Bundles |
| POST | /bundle_pricing/user_bundles/bulk | CreateUserBundlesBulk | User Bundles |
| GET | /bundle_pricing/user_bundles/unused | GetUnusedUserBundles | User Bundles |
| GET | /bundle_pricing/user_bundles/{user_bundle_id} | GetUserBundleById | User Bundles |
| DELETE | /bundle_pricing/user_bundles/{user_bundle_id} | DeactivateUserBundle | User Bundles |
| GET | /bundle_pricing/user_bundles/{user_bundle_id}/resources | GetUserBundleResources | User Bundles |
| GET | /call_control_applications | ListCallControlApplications | Call Control Applications |
| POST | /call_control_applications | CreateCallControlApplication | Call Control Applications |
| GET | /call_control_applications/{id} | RetrieveCallControlApplication | Call Control Applications |
| PATCH | /call_control_applications/{id} | UpdateCallControlApplication | Call Control Applications |
| DELETE | /call_control_applications/{id} | DeleteCallControlApplication | Call Control Applications |
| GET | /call_events | ListCallEvents | Debugging |
| GET | /call_reasons | listCallReasons | Reference Data |
| POST | /call_reasons/validate | validateCallReasons | Reference Data |
| POST | /calls | DialCall | Call Commands |
| GET | /calls/{call_control_id} | RetrieveCallStatus | Call Information |
| POST | /calls/{call_control_id}/actions/answer | AnswerCall | Call Commands |
| POST | /calls/{call_control_id}/actions/bridge | BridgeCall | Call Commands |
| PUT | /calls/{call_control_id}/actions/client_state_update | UpdateClientState | Call Commands |
| POST | /calls/{call_control_id}/actions/conversation_relay_start | CallStartConversationRelay | Call Commands |
| POST | /calls/{call_control_id}/actions/conversation_relay_stop | CallStopConversationRelay | Call Commands |
| POST | /calls/{call_control_id}/actions/enqueue | EnqueueCall | Call Commands |
| POST | /calls/{call_control_id}/actions/fork_start | StartCallFork | Call Commands |
| POST | /calls/{call_control_id}/actions/fork_stop | StopCallFork | Call Commands |
| POST | /calls/{call_control_id}/actions/gather | GatherCall | Call Commands |
| POST | /calls/{call_control_id}/actions/gather_stop | StopCallGather | Call Commands |
| POST | /calls/{call_control_id}/actions/gather_using_audio | GatherUsingAudio | Call Commands |
| POST | /calls/{call_control_id}/actions/gather_using_speak | GatherUsingSpeak | Call Commands |
| POST | /calls/{call_control_id}/actions/hangup | HangupCall | Call Commands |
| POST | /calls/{call_control_id}/actions/leave_queue | LeaveQueue | Call Commands |
| POST | /calls/{call_control_id}/actions/pay | PayCall | Call Commands |
| POST | /calls/{call_control_id}/actions/playback_start | StartCallPlayback | Call Commands |
| POST | /calls/{call_control_id}/actions/playback_stop | StopCallPlayback | Call Commands |
| POST | /calls/{call_control_id}/actions/record_pause | PauseCallRecording | Call Commands |
| POST | /calls/{call_control_id}/actions/record_resume | ResumeCallRecording | Call Commands |
| POST | /calls/{call_control_id}/actions/record_start | StartCallRecord | Call Commands |
| POST | /calls/{call_control_id}/actions/record_stop | StopCallRecording | Call Commands |
| POST | /calls/{call_control_id}/actions/refer | ReferCall | Call Commands |
| POST | /calls/{call_control_id}/actions/reject | RejectCall | Call Commands |
| POST | /calls/{call_control_id}/actions/send_dtmf | SendDTMF | Call Commands |
| POST | /calls/{call_control_id}/actions/send_sip_info | SendSIPInfo | Call Commands |
| POST | /calls/{call_control_id}/actions/siprec_start | StartSiprecSession | Call Commands |
| POST | /calls/{call_control_id}/actions/siprec_stop | StopSiprecSession | Call Commands |
| POST | /calls/{call_control_id}/actions/speak | SpeakCall | Call Commands |
| POST | /calls/{call_control_id}/actions/streaming_start | StartCallStreaming | Call Commands |
| POST | /calls/{call_control_id}/actions/streaming_stop | StopCallStreaming | Call Commands |
| POST | /calls/{call_control_id}/actions/suppression_start | noiseSuppressionStart | Call Commands |
| POST | /calls/{call_control_id}/actions/suppression_stop | noiseSuppressionStop | Call Commands |
| POST | /calls/{call_control_id}/actions/switch_supervisor_role | SwitchSupervisorRole | Call Commands |
| POST | /calls/{call_control_id}/actions/transcription_start | StartCallTranscription | Call Commands |
| POST | /calls/{call_control_id}/actions/transcription_stop | StopCallTranscription | Call Commands |
| POST | /calls/{call_control_id}/actions/transfer | TransferCall | Call Commands |
| GET | /charges_breakdown | GetMonthlyChargesBreakdown |  |
| GET | /charges_summary | GetMonthlyChargesSummary |  |
| GET | /comments | ListComments | Phone Number Orders |
| POST | /comments | CreateComment | Phone Number Orders |
| GET | /comments/{id} | RetrieveComment | Phone Number Orders |
| PATCH | /comments/{id}/read | MarkCommentRead | Phone Number Orders |
| GET | /compute/funcs/{id}/logs | GetComputeFunctionLogs | functions |
| GET | /compute/funcs/{id}/logs/export | GetComputeFunctionLogExport | functions |
| PUT | /compute/funcs/{id}/logs/export | SetComputeFunctionLogExport | functions |
| DELETE | /compute/funcs/{id}/logs/export | DeleteComputeFunctionLogExport | functions |
| GET | /compute/funcs/{id}/metric_aggregates | GetComputeFunctionMetricAggregates | functions |
| GET | /compute/funcs/{id}/revisions | ListComputeFunctionRevisions | functions |
| GET | /compute/funcs/{id}/ship_inspection | GetComputeFunctionShipInspection | functions |
| GET | /conferences | ListConferences | Conference Commands |
| POST | /conferences | CreateConference | Conference Commands |
| GET | /conferences/{conference_id}/participants | ListConferenceParticipants | Conference Commands |
| GET | /conferences/{id} | RetrieveConference | Conference Commands |
| POST | /conferences/{id}/actions/end | EndConference | Conference Commands |
| POST | /conferences/{id}/actions/gather_using_audio | ConferenceGatherUsingAudio | Conference Commands |
| POST | /conferences/{id}/actions/hold | HoldConferenceParticipants | Conference Commands |
| POST | /conferences/{id}/actions/join | JoinConference | Conference Commands |
| POST | /conferences/{id}/actions/leave | LeaveConference | Conference Commands |
| POST | /conferences/{id}/actions/mute | MuteConferenceParticipants | Conference Commands |
| POST | /conferences/{id}/actions/play | PlayConferenceAudio | Conference Commands |
| POST | /conferences/{id}/actions/record_pause | PauseConferenceRecording | Conference Commands |
| POST | /conferences/{id}/actions/record_resume | ResumeConferenceRecording | Conference Commands |
| POST | /conferences/{id}/actions/record_start | StartConferenceRecording | Conference Commands |
| POST | /conferences/{id}/actions/record_stop | StopConferenceRecording | Conference Commands |
| POST | /conferences/{id}/actions/send_dtmf | ConferenceSendDTMF | Conference Commands |
| POST | /conferences/{id}/actions/speak | SpeakTextToConference | Conference Commands |
| POST | /conferences/{id}/actions/stop | StopConferenceAudio | Conference Commands |
| POST | /conferences/{id}/actions/unhold | UnholdConferenceParticipants | Conference Commands |
| POST | /conferences/{id}/actions/unmute | UnmuteConferenceParticipants | Conference Commands |
| POST | /conferences/{id}/actions/update | UpdateConference | Conference Commands |
| GET | /conferences/{id}/participants/{participant_id} | RetrieveConferenceParticipant | Conference Commands |
| PATCH | /conferences/{id}/participants/{participant_id} | UpdateConferenceParticipant | Conference Commands |
| GET | /connections | ListConnections | Connections |
| GET | /connections/count | CountConnections | Connections |
| GET | /connections/{connection_id}/active_calls | ListConnectionActiveCalls | Call Information |
| GET | /connections/{id} | RetrieveConnection | Connections |
| GET | /credential_connections | ListCredentialConnections | Credential Connections |
| POST | /credential_connections | CreateCredentialConnection | Credential Connections |
| GET | /credential_connections/{id} | RetrieveCredentialConnection | Credential Connections |
| PATCH | /credential_connections/{id} | UpdateCredentialConnection | Credential Connections |
| DELETE | /credential_connections/{id} | DeleteCredentialConnection | Credential Connections |
| POST | /credential_connections/{id}/actions/check_registration_status | CheckRegistrationStatus | Credential Connections |
| GET | /customer_service_records | ListCustomerServiceRecords | Customer Service Record |
| POST | /customer_service_records | CreateCustomerServiceRecord | Customer Service Record |
| GET | /customer_service_records/{customer_service_record_id} | GetCustomerServiceRecord | Customer Service Record |
| GET | /dialogflow_connections/{connection_id} | GetDialogflowConnection | Dialogflow Integration |
| POST | /dialogflow_connections/{connection_id} | CreateDialogflowConnection | Dialogflow Integration |
| PUT | /dialogflow_connections/{connection_id} | UpdateDialogflowConnection | Dialogflow Integration |
| DELETE | /dialogflow_connections/{connection_id} | DeleteDialogflowConnection | Dialogflow Integration |
| GET | /dir | listAllDirs | Display Identity Records |
| GET | /dir/document_types | listDocumentTypes | Reference Data |
| GET | /dir/{dir_id} | getDirByIdSimple | Display Identity Records |
| PATCH | /dir/{dir_id} | updateDirSimple | Display Identity Records |
| DELETE | /dir/{dir_id} | deleteDirSimple | Display Identity Records |
| GET | /dir/{dir_id}/comments | listCommentsSimple | Comments |
| POST | /dir/{dir_id}/comments | createCommentSimple | Comments |
| POST | /dir/{dir_id}/loa | renderDirLoa | Display Identity Records |
| GET | /dir/{dir_id}/phone_number_batches | listDirPhoneNumberBatchesSimplified | Phone Number Batches |
| GET | /dir/{dir_id}/phone_number_batches/{batch_id} | getDirPhoneNumberBatchSimplified | Phone Number Batches |
| GET | /dir/{dir_id}/references | listDirReferences | DIR References |
| POST | /dir/{dir_id}/references | submitDirReferences | DIR References |
| PATCH | /dir/{dir_id}/references/{ref_type}/{slot} | updateDirReference | DIR References |
| POST | /dir/{dir_id}/submit | submitDirSimple | Display Identity Records |
| GET | /document_links | ListDocumentLinks | Documents |
| GET | /documents | ListDocuments | Documents |
| POST | /documents | CreateDocument | Documents |
| GET | /documents/{id} | RetrieveDocument | Documents |
| PATCH | /documents/{id} | UpdateDocument | Documents |
| DELETE | /documents/{id} | DeleteDocument | Documents |
| GET | /documents/{id}/download | DownloadDocument | Documents |
| GET | /documents/{id}/download_link | getDocumentDownloadLink | Documents |
| GET | /dynamic_emergency_addresses | ListDynamicEmergencyAddresses | Dynamic Emergency Addresses |
| POST | /dynamic_emergency_addresses | CreateDynamicEmergencyAddress | Dynamic Emergency Addresses |
| GET | /dynamic_emergency_addresses/{id} | GetDynamicEmergencyAddress | Dynamic Emergency Addresses |
| DELETE | /dynamic_emergency_addresses/{id} | DeleteDynamicEmergencyAddress | Dynamic Emergency Addresses |
| GET | /dynamic_emergency_endpoints | ListDynamicEmergencyEndpoints | Dynamic Emergency Endpoints |
| POST | /dynamic_emergency_endpoints | CreateDynamicEmergencyEndpoint | Dynamic Emergency Endpoints |
| GET | /dynamic_emergency_endpoints/{id} | GetDynamicEmergencyEndpoint | Dynamic Emergency Endpoints |
| DELETE | /dynamic_emergency_endpoints/{id} | DeleteDynamicEmergencyEndpoint | Dynamic Emergency Endpoints |
| GET | /enterprises | listEnterprises | Enterprises |
| POST | /enterprises | createEnterprise | Enterprises |
| GET | /enterprises/{enterprise_id} | getEnterprise | Enterprises |
| PUT | /enterprises/{enterprise_id} | updateEnterprise | Enterprises |
| DELETE | /enterprises/{enterprise_id} | deleteEnterprise | Enterprises |
| POST | /enterprises/{enterprise_id}/branded_calling | activateBrandedCalling | Enterprises |
| GET | /enterprises/{enterprise_id}/dir | listDirsForEnterprise | Display Identity Records |
| POST | /enterprises/{enterprise_id}/dir | createDir | Display Identity Records |
| GET | /enterprises/{enterprise_id}/reputation | getReputationSettings | Reputation |
| POST | /enterprises/{enterprise_id}/reputation | enableReputationSettings | Reputation |
| DELETE | /enterprises/{enterprise_id}/reputation | disableReputationSettings | Reputation |
| PATCH | /enterprises/{enterprise_id}/reputation/frequency | updateReputationFrequency | Reputation |
| POST | /enterprises/{enterprise_id}/reputation/loa | generateReputationLoa | Reputation |
| PATCH | /enterprises/{enterprise_id}/reputation/loa | replaceReputationLoa | Reputation |
| GET | /enterprises/{enterprise_id}/reputation/remediation | listReputationRemediations | Reputation |
| GET | /enterprises/{enterprise_id}/reputation/remediation/{remediation_id} | getReputationRemediation | Reputation |
| GET | /external_connections | ListExternalConnections | External Connections |
| POST | /external_connections | CreateExternalConnection | External Connections |
| GET | /external_connections/log_messages | ListExternalConnectionLogMessages | External Connections |
| GET | /external_connections/log_messages/{id} | GetExternalConnectionLogMessage | External Connections |
| DELETE | /external_connections/log_messages/{id} | DeleteExternalConnectionLogMessage | External Connections |
| GET | /external_connections/{id} | GetExternalConnection | External Connections |
| PATCH | /external_connections/{id} | UpdateExternalConnection | External Connections |
| DELETE | /external_connections/{id} | DeleteExternalConnection | External Connections |
| GET | /external_connections/{id}/civic_addresses | ListCivicAddresses | External Connections |
| GET | /external_connections/{id}/civic_addresses/{address_id} | GetExternalConnectionCivicAddress | External Connections |
| PATCH | /external_connections/{id}/locations/{location_id} | updateLocation | External Connections |
| GET | /external_connections/{id}/releases | ListExternalConnectionReleases | External Connections |
| GET | /external_connections/{id}/releases/{release_id} | GetExternalConnectionRelease | External Connections |
| GET | /external_connections/{id}/uploads | ListExternalConnectionUploads | External Connections |
| POST | /external_connections/{id}/uploads | CreateExternalConnectionUpload | External Connections |
| POST | /external_connections/{id}/uploads/refresh | RefreshExternalConnectionUploads | External Connections |
| GET | /external_connections/{id}/uploads/status | GetExternalConnectionUploadsStatus | External Connections |
| GET | /external_connections/{id}/uploads/{ticket_id} | GetExternalConnectionUpload | External Connections |
| POST | /external_connections/{id}/uploads/{ticket_id}/retry | RetryUpload | External Connections |
| POST | /external_requirements/{regulatory_requirement_id}/sub_number_orders/{sub_number_order_id} | createExternalRequirement | Requirement Groups |
| GET | /fqdn_connections | ListFqdnConnections | FQDN Connections |
| POST | /fqdn_connections | CreateFqdnConnection | FQDN Connections |
| GET | /fqdn_connections/{fqdn_connection_id}/fqdn_authentication | RetrieveFqdnAuthentication | FQDN Connections |
| PATCH | /fqdn_connections/{fqdn_connection_id}/fqdn_authentication | UpdateFqdnAuthentication | FQDN Connections |
| GET | /fqdn_connections/{id} | RetrieveFqdnConnection | FQDN Connections |
| PATCH | /fqdn_connections/{id} | UpdateFqdnConnection | FQDN Connections |
| DELETE | /fqdn_connections/{id} | DeleteFqdnConnection | FQDN Connections |
| GET | /fqdns | ListFqdns | FQDNs |
| POST | /fqdns | CreateFqdn | FQDNs |
| GET | /fqdns/{id} | RetrieveFqdn | FQDNs |
| PATCH | /fqdns/{id} | UpdateFqdn | FQDNs |
| DELETE | /fqdns/{id} | DeleteFqdn | FQDNs |
| GET | /global_ip_allowed_ports | ListGlobalIpAllowedPorts | Global IPs |
| GET | /global_ip_assignment_health | GetGlobalIpAssignmentHealth | Global IPs |
| GET | /global_ip_assignments | ListGlobalIpAssignments | Global IPs |
| POST | /global_ip_assignments | CreateGlobalIpAssignment | Global IPs |
| GET | /global_ip_assignments/usage | GetGlobalIpAssignmentUsage | Global IPs |
| GET | /global_ip_assignments/{id} | GetGlobalIpAssignment | Global IPs |
| PATCH | /global_ip_assignments/{id} | UpdateGlobalIpAssignment | Global IPs |
| DELETE | /global_ip_assignments/{id} | DeleteGlobalIpAssignment | Global IPs |
| GET | /global_ip_assignments_usage | GetGlobalIpAssignmentUsage_2 | Global IPs |
| GET | /global_ip_health_check_types | ListGlobalIpHealthCheckTypes | Global IPs |
| GET | /global_ip_health_checks | ListGlobalIpHealthChecks | Global IPs |
| POST | /global_ip_health_checks | CreateGlobalIpHealthCheck | Global IPs |
| GET | /global_ip_health_checks/{id} | GetGlobalIpHealthCheck | Global IPs |
| DELETE | /global_ip_health_checks/{id} | DeleteGlobalIpHealthCheck | Global IPs |
| GET | /global_ip_latency | GetGlobalIpLatency | Global IPs |
| GET | /global_ip_protocols | ListGlobalIpProtocols | Global IPs |
| GET | /global_ip_usage | GetGlobalIpUsage | Global IPs |
| GET | /global_ips | ListGlobalIps | Global IPs |
| POST | /global_ips | CreateGlobalIp | Global IPs |
| GET | /global_ips/{id} | GetGlobalIp | Global IPs |
| DELETE | /global_ips/{id} | DeleteGlobalIp | Global IPs |
| GET | /inexplicit_number_orders | ListInexplicitNumberOrders | Inexplicit Number Orders |
| POST | /inexplicit_number_orders | CreateInexplicitNumberOrder | Inexplicit Number Orders |
| GET | /inexplicit_number_orders/{id} | RetrieveInexplicitNumberOrder | Inexplicit Number Orders |
| GET | /integration_secrets | list_integration_secrets | Integration Secrets |
| POST | /integration_secrets | create_integration_secret | Integration Secrets |
| DELETE | /integration_secrets/{id} | delete_integration_secret | Integration Secrets |
| GET | /ip_connections | ListIpConnections | IP Connections |
| POST | /ip_connections | CreateIpConnection | IP Connections |
| GET | /ip_connections/{id} | RetrieveIpConnection | IP Connections |
| PATCH | /ip_connections/{id} | UpdateIpConnection | IP Connections |
| DELETE | /ip_connections/{id} | DeleteIpConnection | IP Connections |
| GET | /ips | ListIps | IPs |
| POST | /ips | CreateIp | IPs |
| GET | /ips/{id} | RetrieveIp | IPs |
| PATCH | /ips/{id} | UpdateIp | IPs |
| DELETE | /ips/{id} | DeleteIp | IPs |
| POST | /ledger_billing_group_reports | CreateBillingGroupReport | Reports |
| GET | /ledger_billing_group_reports/{id} | GetBillingGroupReport | Reports |
| GET | /legacy/reporting/usage_reports/number_lookup | getTelcoDataUsageReports | Telco Data Usage Reports |
| POST | /legacy/reporting/usage_reports/number_lookup | submitTelcoDataUsageReport | Telco Data Usage Reports |
| GET | /legacy/reporting/usage_reports/number_lookup/{id} | getTelcoDataUsageReport | Telco Data Usage Reports |
| DELETE | /legacy/reporting/usage_reports/number_lookup/{id} | deleteTelcoDataUsageReport | Telco Data Usage Reports |
| GET | /legacy_reporting/usage_reports/number_lookup | getTelcoDataUsageReports_2 | Telco Data Usage Reports |
| POST | /legacy_reporting/usage_reports/number_lookup | submitTelcoDataUsageReport_2 | Telco Data Usage Reports |
| GET | /legacy_reporting/usage_reports/number_lookup/{id} | getTelcoDataUsageReport_2 | Telco Data Usage Reports |
| DELETE | /legacy_reporting/usage_reports/number_lookup/{id} | deleteTelcoDataUsageReport_2 | Telco Data Usage Reports |
| POST | /machine-payments/account-credit | createMachinePaymentAccountCredit | Machine Payments |
| GET | /managed_accounts | ListManagedAccounts | Managed Accounts |
| POST | /managed_accounts | CreateManagedAccount | Managed Accounts |
| GET | /managed_accounts/allocatable_global_outbound_channels | ListAllocatableGlobalOutboundChannels | Managed Accounts |
| GET | /managed_accounts/{id} | RetrieveManagedAccount | Managed Accounts |
| PATCH | /managed_accounts/{id} | UpdateManagedAccount | Managed Accounts |
| POST | /managed_accounts/{id}/actions/disable | DisableManagedAccount | Managed Accounts |
| POST | /managed_accounts/{id}/actions/enable | EnableManagedAccount | Managed Accounts |
| PATCH | /managed_accounts/{id}/update_global_channel_limit | UpdateManagedAccountGlobalChannelLimit | Managed Accounts |
| POST | /messages | SendMessage | Messages |
| POST | /messages/alphanumeric/sender/id | SendAlphanumericSenderIdMessage | Messages |
| POST | /messages/alphanumeric_sender_id | SendAlphanumericSenderIdMessage_2 | Messages |
| GET | /messages/group/{message_id} | GetGroupMmsMessages | Messages |
| POST | /messages/group_mms | CreateGroupMmsMessage | Messages |
| POST | /messages/long_code | CreateLongCodeMessage | Messages |
| POST | /messages/number_pool | CreateNumberPoolMessage | Messages |
| POST | /messages/rcs | SendRCSMessage | RCS |
| GET | /messages/rcs/deeplinks/{agent_id} | GenerateRCSDeeplink | RCS |
| GET | /messages/rcs_deeplinks/{agent_id} | GenerateRCSDeeplink_2 | RCS |
| POST | /messages/schedule | ScheduleMessage | Messages |
| POST | /messages/short_code | CreateShortCodeMessage | Messages |
| GET | /messages/{id} | GetMessage | Messages |
| DELETE | /messages/{id} | CancelMessage | Messages |
| GET | /mobile_network_operators | GetMobileNetworkOperators | Mobile Network Operators |
| GET | /mobile_push_credentials | ListPushCredentials | Push Credentials |
| POST | /mobile_push_credentials | CreatePushCredential | Push Credentials |
| GET | /mobile_push_credentials/{push_credential_id} | GetPushCredentialById | Push Credentials |
| DELETE | /mobile_push_credentials/{push_credential_id} | DeletePushCredentialById | Push Credentials |
| GET | /networks | ListNetworks | Networks |
| POST | /networks | CreateNetwork | Networks |
| GET | /networks/{id} | GetNetwork | Networks |
| PATCH | /networks/{id} | UpdateNetwork | Networks |
| DELETE | /networks/{id} | DeleteNetwork | Networks |
| GET | /networks/{id}/default_gateway | GetDefaultGateway | Networks |
| POST | /networks/{id}/default_gateway | CreateDefaultGateway | Networks |
| DELETE | /networks/{id}/default_gateway | DeleteDefaultGateway | Networks |
| GET | /networks/{id}/network_interfaces | ListNetworkInterfaces | Networks |
| GET | /notification_channels | ListNotificationChannels | Notifications |
| POST | /notification_channels | CreateNotificationChannels | Notifications |
| GET | /notification_channels/{id} | GetNotificationChannel | Notifications |
| PATCH | /notification_channels/{id} | UpdateNotificationChannel | Notifications |
| DELETE | /notification_channels/{id} | DeleteNotificationChannel | Notifications |
| GET | /notification_event_conditions | FindNotificationsEventsConditions | Notifications |
| GET | /notification_events | FindNotificationsEvents | Notifications |
| GET | /notification_profiles | FindNotificationsProfiles | Notifications |
| POST | /notification_profiles | CreateNotificationProfile | Notifications |
| GET | /notification_profiles/{id} | GetNotificationProfile | Notifications |
| PATCH | /notification_profiles/{id} | UpdateNotificationProfile | Notifications |
| DELETE | /notification_profiles/{id} | DeleteNotificationProfile | Notifications |
| GET | /notification_settings | ListNotificationSettings | Notifications |
| POST | /notification_settings | CreateNotificationSetting | Notifications |
| GET | /notification_settings/{id} | GetNotificationSetting | Notifications |
| DELETE | /notification_settings/{id} | DeleteNotificationSetting | Notifications |
| GET | /number_block_orders | ListNumberBlockOrders | Phone Number Block Orders |
| POST | /number_block_orders | CreateNumberBlockOrder | Phone Number Block Orders |
| GET | /number_block_orders/{number_block_order_id} | RetrieveNumberBlockOrder | Phone Number Block Orders |
| GET | /number_lookup/{phone_number} | LookupNumber | Number Lookup |
| GET | /number_orders | ListNumberOrders | Phone Number Orders |
| POST | /number_orders | CreateNumberOrder | Phone Number Orders |
| GET | /number_orders/{number_order_id} | RetrieveNumberOrder | Phone Number Orders |
| PATCH | /number_orders/{number_order_id} | UpdateNumberOrder | Phone Number Orders |
| GET | /number_reservations | ListNumberReservations | Phone Number Reservations |
| POST | /number_reservations | CreateNumberReservation | Phone Number Reservations |
| GET | /number_reservations/{number_reservation_id} | RetrieveNumberReservation | Phone Number Reservations |
| POST | /number_reservations/{number_reservation_id}/actions/extend | ExtendNumberReservationExpiryTime | Phone Number Reservations |
| GET | /oauth/authorize | AuthorizeOAuth | OAuth Protocol |
| GET | /oauth/clients | ListOAuthClients | OAuth Clients |
| POST | /oauth/clients | CreateOAuthClient | OAuth Clients |
| GET | /oauth/clients/{id} | GetOAuthClient | OAuth Clients |
| PUT | /oauth/clients/{id} | UpdateOAuthClient | OAuth Clients |
| DELETE | /oauth/clients/{id} | DeleteOAuthClient | OAuth Clients |
| GET | /oauth/consent/{consent_token} | GetOAuthConsentToken | OAuth Protocol |
| GET | /oauth/grants | ListOAuthGrants | OAuth Grants |
| POST | /oauth/grants | CreateOAuthGrant | OAuth Protocol |
| GET | /oauth/grants/{id} | GetOAuthGrant | OAuth Grants |
| DELETE | /oauth/grants/{id} | RevokeOAuthGrant | OAuth Grants |
| POST | /oauth/introspect | IntrospectOAuthToken | OAuth Protocol |
| GET | /oauth/jwks | GetOAuthJWKS | OAuth Protocol |
| POST | /oauth/register | RegisterOAuthClient | OAuth Protocol |
| POST | /oauth/token | ExchangeOAuthToken | OAuth Protocol |
| GET | /oauth_clients | ListOAuthClients_2 | OAuth Clients |
| POST | /oauth_clients | CreateOAuthClient_2 | OAuth Clients |
| GET | /oauth_clients/{id} | GetOAuthClient_2 | OAuth Clients |
| PUT | /oauth_clients/{id} | UpdateOAuthClient_2 | OAuth Clients |
| DELETE | /oauth_clients/{id} | DeleteOAuthClient_2 | OAuth Clients |
| GET | /oauth_grants | ListOAuthGrants_2 | OAuth Grants |
| GET | /oauth_grants/{id} | GetOAuthGrant_2 | OAuth Grants |
| DELETE | /oauth_grants/{id} | RevokeOAuthGrant_2 | OAuth Grants |
| POST | /operator_connect/actions/refresh | OperatorConnectRefresh | External Connections |
| GET | /organizations/users | ListOrganizationUsers | Organization Users |
| GET | /organizations/users/users_groups_report | GetOrganizationUsersGroupsReport | Organization Users |
| GET | /organizations/users/{id} | GetOrganizationUser | Organization Users |
| POST | /organizations/users/{id}/actions/remove | DeleteOrganizationUser | Organization Users |
| GET | /ota_updates | ListOtaUpdates | OTA updates |
| GET | /ota_updates/{id} | GetOtaUpdate | OTA updates |
| GET | /payment/auto_recharge_prefs | GetAutoRechargePrefs | AutoRechargePreferences |
| PATCH | /payment/auto_recharge_prefs | UpdateAutoRechargePrefs | AutoRechargePreferences |
| GET | /phone_number_blocks/jobs | ListPhoneNumberBlocksJobs | Phone Number Blocks Background Jobs |
| GET | /phone_number_blocks/jobs/{id} | GetPhoneNumberBlocksJob | Phone Number Blocks Background Jobs |
| POST | /portability_checks | PostPortabilityCheck | Phone Number Porting |
| GET | /porting/events | listPortingEvents | Porting Orders |
| GET | /porting/events/{id} | showPortingEvent | Porting Orders |
| POST | /porting/events/{id}/republish | republishPortingEvent | Porting Orders |
| GET | /porting/loa_configurations | ListLoaConfigurations | Porting Orders |
| POST | /porting/loa_configurations | CreateLoaConfiguration | Porting Orders |
| POST | /porting/loa_configurations/preview | PreviewLoaConfigurationParams | Porting Orders |
| GET | /porting/loa_configurations/{id} | GetLoaConfiguration | Porting Orders |
| PATCH | /porting/loa_configurations/{id} | UpdateLoaConfiguration | Porting Orders |
| DELETE | /porting/loa_configurations/{id} | DeleteLoaConfiguration | Porting Orders |
| GET | /porting/loa_configurations/{id}/preview | PreviewLoaConfiguration | Porting Orders |
| GET | /porting/reports | ListPortingReports | Porting Orders |
| POST | /porting/reports | CreatePortingReport | Porting Orders |
| GET | /porting/reports/{id} | GetPortingReport | Porting Orders |
| GET | /porting_orders | ListPortingOrders | Porting Orders |
| POST | /porting_orders | CreatePortingOrder | Porting Orders |
| GET | /porting_orders/exception_types | ListExceptionTypes | Porting Orders |
| GET | /porting_orders/phone_number_configurations | ListPhoneNumberConfigurations | Porting Orders |
| POST | /porting_orders/phone_number_configurations | CreatePhoneNumberConfigurations | Porting Orders |
| GET | /porting_orders/{id} | GetPortingOrder | Porting Orders |
| PATCH | /porting_orders/{id} | UpdatePortingOrder | Porting Orders |
| DELETE | /porting_orders/{id} | DeletePortingOrder | Porting Orders |
| POST | /porting_orders/{id}/actions/activate | ActivatePortingOrder | Porting Orders |
| POST | /porting_orders/{id}/actions/cancel | CancelPortingOrder | Porting Orders |
| POST | /porting_orders/{id}/actions/confirm | ConfirmPortingOrder | Porting Orders |
| POST | /porting_orders/{id}/actions/share | SharePortingOrder | Porting Orders |
| GET | /porting_orders/{id}/activation_jobs | ListPortingOrderActivationJobs | Porting Orders |
| GET | /porting_orders/{id}/activation_jobs/{activationJobId} | GetPortingOrdersActivationJob | Porting Orders |
| PATCH | /porting_orders/{id}/activation_jobs/{activationJobId} | UpdatePortingOrdersActivationJob | Porting Orders |
| GET | /porting_orders/{id}/additional_documents | ListAdditionalDocuments | Porting Orders |
| POST | /porting_orders/{id}/additional_documents | CreateAdditionalDocuments | Porting Orders |
| DELETE | /porting_orders/{id}/additional_documents/{additional_document_id} | DeleteAdditionalDocument | Porting Orders |
| GET | /porting_orders/{id}/allowed_foc_windows | ListAllowedFocWindows | Porting Orders |
| GET | /porting_orders/{id}/comments | ListPortingOrderComments | Porting Orders |
| POST | /porting_orders/{id}/comments | CreatePortingOrderComment | Porting Orders |
| GET | /porting_orders/{id}/loa_template | GetPortingOrderLoaTemplate | Porting Orders |
| GET | /porting_orders/{id}/requirements | ListPortingOrderRequirements | Porting Orders |
| GET | /porting_orders/{id}/sub_request | GetPortingOrderSubRequest | Porting Orders |
| GET | /porting_orders/{id}/verification_codes | ListVerificationCodes | Porting Orders |
| POST | /porting_orders/{id}/verification_codes/send | SendPortingVerificationCodes | Porting Orders |
| GET | /porting_orders/{porting_order_id}/action_requirements | listPortingActionRequirements | Porting Orders |
| POST | /porting_orders/{porting_order_id}/action_requirements/{id}/initiate | initiatePortingActionRequirement | Porting Orders |
| GET | /porting_orders/{porting_order_id}/phone_number_blocks | listPortingPhoneNumberBlocks | Porting Orders |
| POST | /porting_orders/{porting_order_id}/phone_number_blocks | createPortingPhoneNumberBlock | Porting Orders |
| DELETE | /porting_orders/{porting_order_id}/phone_number_blocks/{id} | deletePortingPhoneNumberBlock | Porting Orders |
| GET | /porting_orders/{porting_order_id}/phone_number_extensions | listPortingPhoneNumberExtensions | Porting Orders |
| POST | /porting_orders/{porting_order_id}/phone_number_extensions | createPortingPhoneNumberExtension | Porting Orders |
| DELETE | /porting_orders/{porting_order_id}/phone_number_extensions/{id} | deletePortingPhoneNumberExtension | Porting Orders |
| GET | /portouts | ListPortoutRequest | Number Portout |
| GET | /portouts/events | listPortoutEvents | Number Portout |
| GET | /portouts/events/{id} | showPortoutEvent | Number Portout |
| POST | /portouts/events/{id}/republish | republishPortoutEvent | Number Portout |
| GET | /portouts/rejections/{portout_id} | ListPortoutRejections | Number Portout |
| GET | /portouts/reports | ListPortoutReports | Number Portout |
| POST | /portouts/reports | CreatePortoutReport | Number Portout |
| GET | /portouts/reports/{id} | GetPortoutReport | Number Portout |
| GET | /portouts/{id} | FindPortoutRequest | Number Portout |
| GET | /portouts/{id}/comments | FindPortoutComments | Number Portout |
| POST | /portouts/{id}/comments | PostPortRequestComment | Number Portout |
| GET | /portouts/{id}/supporting_documents | GetPortRequestSupportingDocuments | Number Portout |
| POST | /portouts/{id}/supporting_documents | PostPortRequestSupportingDocuments | Number Portout |
| PATCH | /portouts/{id}/{status} | UpdatePortoutStatus | Number Portout |
| GET | /pricing/products | listPricingProducts | Pricing |
| GET | /pricing/products/{slug} | getProductPricing | Pricing |
| GET | /private_wireless_gateways | GetPrivateWirelessGateways | Private Wireless Gateways |
| POST | /private_wireless_gateways | CreatePrivateWirelessGateway | Private Wireless Gateways |
| GET | /private_wireless_gateways/{id} | GetPrivateWirelessGateway | Private Wireless Gateways |
| DELETE | /private_wireless_gateways/{id} | DeleteWirelessGateway | Private Wireless Gateways |
| GET | /pronunciation_dicts | ListPronunciationDicts | Pronunciation Dictionaries |
| POST | /pronunciation_dicts | CreatePronunciationDict | Pronunciation Dictionaries |
| GET | /pronunciation_dicts/{id} | GetPronunciationDict | Pronunciation Dictionaries |
| PATCH | /pronunciation_dicts/{id} | UpdatePronunciationDict | Pronunciation Dictionaries |
| DELETE | /pronunciation_dicts/{id} | DeletePronunciationDict | Pronunciation Dictionaries |
| GET | /public_internet_gateways | ListPublicInternetGateways | Public Internet Gateways |
| POST | /public_internet_gateways | CreatePublicInternetGateway | Public Internet Gateways |
| GET | /public_internet_gateways/{id} | GetPublicInternetGateway | Public Internet Gateways |
| DELETE | /public_internet_gateways/{id} | DeletePublicInternetGateway | Public Internet Gateways |
| GET | /queues | ListQueues | Queue Commands |
| POST | /queues | CreateQueue | Queue Commands |
| GET | /queues/{queue_name} | RetrieveCallQueue | Queue Commands |
| POST | /queues/{queue_name} | UpdateQueue | Queue Commands |
| DELETE | /queues/{queue_name} | DeleteQueue | Queue Commands |
| GET | /queues/{queue_name}/calls | ListQueueCalls | Queue Commands |
| GET | /queues/{queue_name}/calls/{call_control_id} | RetrieveCallFromQueue | Queue Commands |
| PATCH | /queues/{queue_name}/calls/{call_control_id} | UpdateCallInQueue | Queue Commands |
| DELETE | /queues/{queue_name}/calls/{call_control_id} | RemoveQueueCall | Queue Commands |
| GET | /rcs/agents | ListRcsAgents | RCS Agents |
| POST | /rcs/agents | CreateRcsAgent | RCS Agents |
| GET | /rcs/agents/{id} | RetrieveRcsAgent | RCS Agents |
| PATCH | /rcs/agents/{id} | UpdateRcsAgent | RCS Agents |
| GET | /rcs/agents/{id}/carrier_approvals | ListRcsAgentCarrierApprovals | RCS Agents |
| POST | /rcs/agents/{id}/launch | LaunchRcsAgent | RCS Agents |
| POST | /rcs/agents/{id}/submit | SubmitRcsAgent | RCS Agents |
| GET | /rcs/agents/{id}/test_devices | ListRcsAgentTestDevices | RCS Agents |
| POST | /rcs/agents/{id}/test_devices | AddRcsAgentTestDevice | RCS Agents |
| DELETE | /rcs/agents/{id}/test_devices/{test_device_id} | RemoveRcsAgentTestDevice | RCS Agents |
| GET | /rcs/brands | ListRcsBrands | RCS Brands |
| POST | /rcs/brands | CreateRcsBrand | RCS Brands |
| GET | /rcs/brands/{id} | RetrieveRcsBrand | RCS Brands |
| PATCH | /rcs/brands/{id} | UpdateRcsBrand | RCS Brands |
| POST | /rcs/brands/{id}/submit | SubmitRcsBrand | RCS Brands |
| GET | /recording_transcriptions | getRecordingTranscriptions | Call Recordings |
| GET | /recording_transcriptions/{recording_transcription_id} | getRecordingTranscription | Call Recordings |
| DELETE | /recording_transcriptions/{recording_transcription_id} | deleteRecordingTranscription | Call Recordings |
| GET | /recordings | GetRecordings | Call Recordings |
| POST | /recordings/actions/delete | DeleteRecordings | Call Recordings |
| GET | /recordings/{recording_id} | GetRecording | Call Recordings |
| DELETE | /recordings/{recording_id} | DeleteRecording | Call Recordings |
| GET | /regions | ListRegions | Regions |
| GET | /regulatory_requirements | ListRegulatoryRequirements | Regulatory Requirements |
| GET | /reports/cdr_usage_reports/sync | GetCDRUsageReportSync | CDR Usage Reports |
| POST | /reports/mdr_usage_reports | SubmitUsageReport | MDR Usage Reports |
| GET | /reports/mdr_usage_reports/sync | GetMDRUsageReportSync | MDR Usage Reports |
| DELETE | /reports/mdr_usage_reports/{id} | DeleteUsageReport | MDR Usage Reports |
| GET | /requirement_groups | GetRequirementGroups | Requirement Groups |
| POST | /requirement_groups | CreateRequirementGroup | Requirement Groups |
| GET | /requirement_groups/{id} | GetRequirementGroup | Requirement Groups |
| PATCH | /requirement_groups/{id} | UpdateRequirementGroup | Requirement Groups |
| DELETE | /requirement_groups/{id} | DeleteRequirementGroup | Requirement Groups |
| POST | /requirement_groups/{id}/submit_for_approval | SubmitRequirementGroup | Requirement Groups |
| GET | /requirement_types | ListRequirementTypes | Requirement Types |
| GET | /requirement_types/{id} | RetrieveRequirementType | Requirement Types |
| GET | /requirements | ListRequirements | Requirements |
| GET | /requirements/{id} | RetrieveDocumentRequirements | Requirements |
| POST | /requirements/{id}/versions | CreateRequirementVersion | Requirements |
| DELETE | /requirements/{id}/versions/pending | CancelPendingRequirementVersion | Requirements |
| GET | /room_compositions | ListRoomCompositions | Room Compositions |
| POST | /room_compositions | CreateRoomComposition | Room Compositions |
| GET | /room_compositions/{room_composition_id} | ViewRoomComposition | Room Compositions |
| DELETE | /room_compositions/{room_composition_id} | DeleteRoomComposition | Room Compositions |
| GET | /room_participants | ListRoomParticipants | Room Participants |
| GET | /room_participants/{room_participant_id} | ViewRoomParticipant | Room Participants |
| GET | /room_recordings | ListRoomRecordings | Room Recordings |
| DELETE | /room_recordings | DeleteRoomRecordings | Room Recordings |
| GET | /room_recordings/{room_recording_id} | ViewRoomRecording | Room Recordings |
| DELETE | /room_recordings/{room_recording_id} | DeleteRoomRecording | Room Recordings |
| GET | /room_sessions | ListRoomSessions | Room Sessions |
| GET | /room_sessions/{room_session_id} | ViewRoomSession | Room Sessions |
| POST | /room_sessions/{room_session_id}/actions/end | EndSession | Room Sessions |
| POST | /room_sessions/{room_session_id}/actions/kick | KickParticipantInSession | Room Sessions |
| POST | /room_sessions/{room_session_id}/actions/mute | MuteParticipantInSession | Room Sessions |
| POST | /room_sessions/{room_session_id}/actions/unmute | UnmuteParticipantInSession | Room Sessions |
| GET | /room_sessions/{room_session_id}/participants | RetrieveListRoomParticipants | Room Sessions |
| GET | /rooms | ListRooms | Rooms |
| POST | /rooms | CreateRoom | Rooms |
| GET | /rooms/{room_id} | ViewRoom | Rooms |
| PATCH | /rooms/{room_id} | UpdateRoom | Rooms |
| DELETE | /rooms/{room_id} | DeleteRoom | Rooms |
| POST | /rooms/{room_id}/actions/generate_join_client_token | CreateRoomClientToken | Rooms Client Tokens |
| POST | /rooms/{room_id}/actions/refresh_client_token | RefreshRoomClientToken | Rooms Client Tokens |
| GET | /rooms/{room_id}/sessions | RetrieveListRoomSessions | Rooms |
| GET | /session_analysis/metadata | GetSessionAnalysisMetadata | Session Analysis |
| GET | /session_analysis/metadata/{record_type} | GetSessionAnalysisRecordTypeMetadata | Session Analysis |
| GET | /session_analysis/{record_type}/{event_id} | GetSessionAnalysis | Session Analysis |
| GET | /seti/black_box_test_results | GetBlackBoxTestResults | SETI Observability |
| GET | /short_codes | ListShortCodes | Short Codes |
| GET | /short_codes/{id} | RetrieveShortCode | Short Codes |
| PATCH | /short_codes/{id} | UpdateShortCode | Short Codes |
| GET | /sim_card_actions | ListSimCardActions | SIM Card Actions |
| GET | /sim_card_data_usage_notifications | ListDataUsageNotifications | SIM Cards |
| POST | /sim_card_data_usage_notifications | PostSimCardDataUsageNotification | SIM Cards |
| GET | /sim_card_data_usage_notifications/{id} | GetSimCardDataUsageNotification | SIM Cards |
| PATCH | /sim_card_data_usage_notifications/{id} | PatchSimCardDataUsageNotification | SIM Cards |
| DELETE | /sim_card_data_usage_notifications/{id} | DeleteSimCardDataUsageNotifications | SIM Cards |
| GET | /sim_card_group_actions | GetSimCardGroupActions | SIM Card Group Actions |
| GET | /sim_card_groups | GetAllSimCardGroups | SIM Card Groups |
| POST | /sim_card_groups | CreateSimCardGroup | SIM Card Groups |
| GET | /sim_card_groups/{id} | GetSimCardGroup | SIM Card Groups |
| PATCH | /sim_card_groups/{id} | UpdateSimCardGroup | SIM Card Groups |
| DELETE | /sim_card_groups/{id} | DeleteSimCardGroup | SIM Card Groups |
| POST | /sim_card_groups/{id}/actions/remove_private_wireless_gateway | RemoveSimCardGroupPrivateWirelessGateway | SIM Card Groups |
| POST | /sim_card_groups/{id}/actions/remove_wireless_blocklist | RemoveWirelessBlocklistForSimCardGroup | SIM Card Groups |
| POST | /sim_card_groups/{id}/actions/set_private_wireless_gateway | SetPrivateWirelessGatewayForSimCardGroup | SIM Card Groups |
| POST | /sim_card_groups/{id}/actions/set_wireless_blocklist | SetWirelessBlocklistForSimCardGroup | SIM Card Groups |
| POST | /sim_card_order_preview | PreviewSimCardOrders | SIM Card Orders |
| GET | /sim_card_orders | GetSimCardOrders | SIM Card Orders |
| POST | /sim_card_orders | CreateSimCardOrder | SIM Card Orders |
| GET | /sim_card_orders/{id} | GetSimCardOrder | SIM Card Orders |
| GET | /sim_cards | GetSimCards | SIM Cards |
| POST | /sim_cards/actions/bulk_set_public_ips | SetPublicIPsBulk | SIM Cards |
| POST | /sim_cards/actions/validate_registration_codes | ValidateRegistrationCodes | SIM Cards |
| GET | /sim_cards/{id} | GetSimCard | SIM Cards |
| PATCH | /sim_cards/{id} | UpdateSimCard | SIM Cards |
| DELETE | /sim_cards/{id} | DeleteSimCard | SIM Cards |
| POST | /sim_cards/{id}/actions/disable | DisableSimCard | SIM Cards |
| POST | /sim_cards/{id}/actions/enable | EnableSimCard | SIM Cards |
| POST | /sim_cards/{id}/actions/remove_public_ip | RemoveSimCardPublicIp | SIM Cards |
| POST | /sim_cards/{id}/actions/set_public_ip | SetSimCardPublicIp | SIM Cards |
| POST | /sim_cards/{id}/actions/set_standby | SetSimCardStandby | SIM Cards |
| GET | /sim_cards/{id}/activation_code | GetSimCardActivationCode | SIM Cards |
| GET | /sim_cards/{id}/public_ip | GetSimCardPublicIp | SIM Cards |
| GET | /sim_cards/{id}/wireless_connectivity_logs | GetWirelessConnectivityLogs | SIM Cards |
| POST | /siprec_connectors | createSiprecConnector | SIPREC Connectors |
| GET | /siprec_connectors/{connector_name} | getSiprecConnector | SIPREC Connectors |
| PUT | /siprec_connectors/{connector_name} | updateSiprecConnector | SIPREC Connectors |
| DELETE | /siprec_connectors/{connector_name} | deleteSiprecConnector | SIPREC Connectors |
| GET | /sub_number_orders | ListSubNumberOrders | Phone Number Orders |
| POST | /sub_number_orders/report | CreateSubNumberOrdersReport | Phone Number Orders |
| GET | /sub_number_orders/report/{report_id} | GetSubNumberOrdersReport | Phone Number Orders |
| GET | /sub_number_orders/report/{report_id}/download | DownloadSubNumberOrdersReport | Phone Number Orders |
| POST | /sub_number_orders/{id}/requirement_group | updateSubNumberOrderRequirementGroup | Requirement Groups |
| GET | /sub_number_orders/{sub_number_order_id} | GetSubNumberOrder | Phone Number Orders |
| PATCH | /sub_number_orders/{sub_number_order_id} | UpdateSubNumberOrder | Phone Number Orders |
| PATCH | /sub_number_orders/{sub_number_order_id}/cancel | CancelSubNumberOrder | Phone Number Orders |
| POST | /sub_number_orders_report | CreateSubNumberOrdersReport_2 | Phone Number Orders |
| GET | /sub_number_orders_report/{report_id} | GetSubNumberOrdersReport_2 | Phone Number Orders |
| GET | /sub_number_orders_report/{report_id}/download | DownloadSubNumberOrdersReport_2 | Phone Number Orders |
| GET | /telephony_credentials | FindTelephonyCredentials | Credentials |
| POST | /telephony_credentials | CreateTelephonyCredential | Credentials |
| GET | /telephony_credentials/{id} | GetTelephonyCredential | Credentials |
| PATCH | /telephony_credentials/{id} | UpdateTelephonyCredential | Credentials |
| DELETE | /telephony_credentials/{id} | DeleteTelephonyCredential | Credentials |
| POST | /telephony_credentials/{id}/token | CreateTelephonyCredentialToken | Access Tokens |
| GET | /terms_of_service/agreements | listTermsOfServiceAgreements | Terms of Service |
| GET | /terms_of_service/agreements/{agreement_id} | getTermsOfServiceAgreement | Terms of Service |
| POST | /terms_of_service/branded_calling/agree | agreeToBrandedCallingTos | Terms of Service |
| GET | /terms_of_service/info | getTermsOfServiceInfo | Terms of Service |
| POST | /terms_of_service/number_reputation/agree | agreeNumberReputationTermsOfService | Terms of Service |
| GET | /terms_of_service/status | getTermsOfServiceStatus | Terms of Service |
| GET | /texml/Accounts/{account_sid}/Calls | GetTexmlCalls | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls | InitiateTexmlCall | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Calls/{call_sid} | GetTexmlCall | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls/{call_sid} | UpdateTexmlCall | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json | FetchTeXMLCallRecordings | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings.json | StartTeXMLCallRecording | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls/{call_sid}/Recordings/{recording_sid}.json | UpdateTeXMLCallRecording | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec.json | StartTeXMLSiprecSession | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls/{call_sid}/Siprec/{siprec_sid}.json | UpdateTeXMLSiprecSession | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams.json | StartTeXMLCallStreaming | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Calls/{call_sid}/Streams/{streaming_sid}.json | UpdateTeXMLCallStreaming | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Conferences | GetTexmlConferences | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Conferences/{conference_sid} | GetTexmlConference | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Conferences/{conference_sid} | UpdateTexmlConference | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants | GetTexmlConferenceParticipants | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants | DialTexmlConferenceParticipant | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label} | GetTexmlConferenceParticipant | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label} | UpdateTexmlConferenceParticipant | TeXML REST Commands |
| DELETE | /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Participants/{call_sid_or_participant_label} | DeleteTexmlConferenceParticipant | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings | GetTexmlConferenceRecordings | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Conferences/{conference_sid}/Recordings.json | FetchTeXMLConferenceRecordings | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Queues | GetTexmlQueues | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Queues | CreateTexmlQueue | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Queues/{queue_sid} | GetTexmlQueue | TeXML REST Commands |
| POST | /texml/Accounts/{account_sid}/Queues/{queue_sid} | UpdateTexmlQueue | TeXML REST Commands |
| DELETE | /texml/Accounts/{account_sid}/Queues/{queue_sid} | DeleteTexmlQueue | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Recordings.json | GetTeXMLCallRecordings | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json | GetTeXMLCallRecording | TeXML REST Commands |
| DELETE | /texml/Accounts/{account_sid}/Recordings/{recording_sid}.json | DeleteTeXMLCallRecording | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Transcriptions.json | GetTeXMLRecordingTranscriptions | TeXML REST Commands |
| GET | /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json | GetTeXMLRecordingTranscription | TeXML REST Commands |
| DELETE | /texml/Accounts/{account_sid}/Transcriptions/{recording_transcription_sid}.json | DeleteTeXMLRecordingTranscription | TeXML REST Commands |
| POST | /texml/calls/{connection_id} | CreateTexmlCall | TeXML REST Commands |
| POST | /texml/secrets | CreateTexmlSecret | TeXML REST Commands |
| GET | /texml_applications | FindTexmlApplications | TeXML Applications |
| POST | /texml_applications | CreateTexmlApplication | TeXML Applications |
| GET | /texml_applications/{id} | GetTexmlApplication | TeXML Applications |
| PATCH | /texml_applications/{id} | UpdateTexmlApplication | TeXML Applications |
| DELETE | /texml_applications/{id} | DeleteTexmlApplication | TeXML Applications |
| GET | /traffic/policy/profiles | GetTrafficPolicyProfiles | Traffic Policy Profiles |
| POST | /traffic/policy/profiles | CreateTrafficPolicyProfile | Traffic Policy Profiles |
| GET | /traffic/policy/profiles/{id} | GetTrafficPolicyProfile | Traffic Policy Profiles |
| PATCH | /traffic/policy/profiles/{id} | UpdateTrafficPolicyProfile | Traffic Policy Profiles |
| DELETE | /traffic/policy/profiles/{id} | DeleteTrafficPolicyProfile | Traffic Policy Profiles |
| GET | /traffic_policy_profiles | GetTrafficPolicyProfiles_2 | Traffic Policy Profiles |
| POST | /traffic_policy_profiles | CreateTrafficPolicyProfile_2 | Traffic Policy Profiles |
| GET | /traffic_policy_profiles/{id} | GetTrafficPolicyProfile_2 | Traffic Policy Profiles |
| PATCH | /traffic_policy_profiles/{id} | UpdateTrafficPolicyProfile_2 | Traffic Policy Profiles |
| DELETE | /traffic_policy_profiles/{id} | DeleteTrafficPolicyProfile_2 | Traffic Policy Profiles |
| GET | /uac_connections | ListUacConnections | UAC Connections |
| POST | /uac_connections | CreateUacConnection | UAC Connections |
| GET | /uac_connections/{id} | RetrieveUacConnection | UAC Connections |
| PATCH | /uac_connections/{id} | UpdateUacConnection | UAC Connections |
| DELETE | /uac_connections/{id} | DeleteUacConnection | UAC Connections |
| POST | /uac_connections/{id}/actions/check_registration_status | CheckUacConnectionRegistrationStatus | UAC Connections |
| GET | /usage_reports | GetUsageReports | Usage Reports (BETA) |
| GET | /usage_reports/options | ListUsageReportsOptions | Usage Reports (BETA) |
| GET | /user/addresses | FindUserAddress | UserAddresses |
| POST | /user/addresses | CreateUserAddress | UserAddresses |
| GET | /user/addresses/{id} | GetUserAddress | UserAddresses |
| GET | /user_addresses | FindUserAddress_2 | UserAddresses |
| POST | /user_addresses | CreateUserAddress_2 | UserAddresses |
| GET | /user_addresses/{id} | GetUserAddress_2 | UserAddresses |
| GET | /user_tags | GetUserTags | User Tags |
| POST | /v2/bot_challenge | createBotChallenge | Bot Signup |
| GET | /v2/bot_sessions | createBotSession | Bot Signup |
| POST | /v2/bot_signup | createBotSignup | Bot Signup |
| POST | /v2/bot_signup/resend_magic_link | resendBotSignupMagicLink | Bot Signup |
| POST | /v2/payment/stored_payment_transactions | createStoredPaymentTransaction | Stored Payment Transactions |
| GET | /v2/whatsapp/business_accounts | ListWabas | Whatsapp Business Accounts |
| GET | /v2/whatsapp/business_accounts/{id} | GetSingleWaba | Whatsapp Business Accounts |
| DELETE | /v2/whatsapp/business_accounts/{id} | deleteWaba | Whatsapp Business Accounts |
| GET | /v2/whatsapp/business_accounts/{id}/settings | GetWabaSettings | Whatsapp Business Accounts |
| PATCH | /v2/whatsapp/business_accounts/{id}/settings | PatchWabaSettings | Whatsapp Business Accounts |
| GET | /v2/whatsapp/message_templates | ListWhatsappTemplates | Whatsapp Message Templates |
| POST | /v2/whatsapp/message_templates | PostWhatsappTemplate | Whatsapp Message Templates |
| GET | /v2/whatsapp/user_data | GetWhatsappUserData | Whatsapp Business Accounts |
| PATCH | /v2/whatsapp/user_data | PatchWhatsappUserData | Whatsapp Business Accounts |
| GET | /v2/whatsapp_message_templates/{id} | GetWhatsappTemplate | Whatsapp Message Templates |
| PATCH | /v2/whatsapp_message_templates/{id} | PatchWhatsappTemplate | Whatsapp Message Templates |
| DELETE | /v2/whatsapp_message_templates/{id} | DeleteWhatsappTemplate | Whatsapp Message Templates |
| GET | /virtual_cross_connects | ListVirtualCrossConnects | Virtual Cross Connects |
| POST | /virtual_cross_connects | CreateVirtualCrossConnect | Virtual Cross Connects |
| GET | /virtual_cross_connects/{id} | GetVirtualCrossConnect | Virtual Cross Connects |
| PATCH | /virtual_cross_connects/{id} | UpdateVirtualCrossConnect | Virtual Cross Connects |
| DELETE | /virtual_cross_connects/{id} | DeleteVirtualCrossConnect | Virtual Cross Connects |
| POST | /web_search | CreateWebSearch | Web Search |
| POST | /web_search/contents | CreateWebSearchContents | Contents |
| POST | /web_search/research | CreateWebSearchResearch | Research |
| GET | /web_search/research/{task_id} | GetWebSearchResearchStatus | Research |
| GET | /webhook_deliveries | GetWebhookDeliveries | Webhooks |
| GET | /whatsapp/business_accounts | ListWabas_2 | Whatsapp Business Accounts |
| GET | /whatsapp/business_accounts/{id} | GetSingleWaba_2 | Whatsapp Business Accounts |
| DELETE | /whatsapp/business_accounts/{id} | deleteWaba_2 | Whatsapp Business Accounts |
| GET | /whatsapp/business_accounts/{id}/settings | GetWabaSettings_2 | Whatsapp Business Accounts |
| PATCH | /whatsapp/business_accounts/{id}/settings | PatchWabaSettings_2 | Whatsapp Business Accounts |
| GET | /whatsapp/message_templates | ListWhatsappTemplates_2 | Whatsapp Message Templates |
| POST | /whatsapp/message_templates | PostWhatsappTemplate_2 | Whatsapp Message Templates |
| GET | /whatsapp/message_templates/{id} | GetWhatsappTemplate_2 | Whatsapp Message Templates |
| PATCH | /whatsapp/message_templates/{id} | PatchWhatsappTemplate_2 | Whatsapp Message Templates |
| DELETE | /whatsapp/message_templates/{id} | DeleteWhatsappTemplate_2 | Whatsapp Message Templates |
| GET | /wireguard_interfaces | ListWireguardInterfaces | WireGuard Interfaces |
| POST | /wireguard_interfaces | CreateWireguardInterface | WireGuard Interfaces |
| GET | /wireguard_interfaces/{id} | GetWireguardInterface | WireGuard Interfaces |
| DELETE | /wireguard_interfaces/{id} | DeleteWireguardInterface | WireGuard Interfaces |
| GET | /wireguard_peers | ListWireguardPeers | WireGuard Interfaces |
| POST | /wireguard_peers | CreateWireguardPeer | WireGuard Interfaces |
| GET | /wireguard_peers/{id} | GetWireguardPeer | WireGuard Interfaces |
| PATCH | /wireguard_peers/{id} | UpdateWireguardPeer | WireGuard Interfaces |
| DELETE | /wireguard_peers/{id} | DeleteWireguardPeer | WireGuard Interfaces |
| GET | /wireguard_peers/{id}/config | GetWireguardPeerConfig | WireGuard Interfaces |
| GET | /wireless/regions | WirelessRegionsGetAll | Wireless Regions |
| GET | /wireless_blocklist_values | WirelessBlocklistsGetAll | Wireless Blocklists |
| GET | /wireless_blocklists | GetWirelessBlocklistsGateways | Wireless Blocklists |
| POST | /wireless_blocklists | CreateWirelessBlocklist | Wireless Blocklists |
| GET | /wireless_blocklists/{id} | GetWirelessBlocklist | Wireless Blocklists |
| PATCH | /wireless_blocklists/{id} | UpdateWirelessBlocklist | Wireless Blocklists |
| DELETE | /wireless_blocklists/{id} | DeleteWirelessBlocklist | Wireless Blocklists |
| POST | /x402/credit_account | settleX402Payment | x402 Payment Transactions |
| GET | /x402/credit_account/payments | listX402Payments | x402 Payment Transactions |
| GET | /x402/credit_account/payments/{id} | getX402Payment | x402 Payment Transactions |
| POST | /x402/credit_account/quote | createX402Quote | x402 Payment Transactions |
| POST | /v1/chat/completions | x402_v1ChatCompletions | x402 |
| POST | /v1/audio/transcriptions | x402_v1AudioTranscriptions | x402 |
