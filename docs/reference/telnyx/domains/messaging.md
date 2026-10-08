# messaging

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| POST | /10dlc/phoneNumberAssignmentByProfile | PostAssignMessagingProfileToCampaign | Bulk Phone Number Campaigns |
| GET | /alphanumeric_sender_ids | ListAlphanumericSenderIds | Messaging |
| POST | /alphanumeric_sender_ids | CreateAlphanumericSenderId | Messaging |
| GET | /alphanumeric_sender_ids/{id} | GetAlphanumericSenderId | Messaging |
| DELETE | /alphanumeric_sender_ids/{id} | DeleteAlphanumericSenderId | Messaging |
| GET | /legacy/reporting/batch_detail_records/messaging | getMdrRequests | MDR Detailed Reports |
| POST | /legacy/reporting/batch_detail_records/messaging | submitMdrRequest | MDR Detailed Reports |
| GET | /legacy/reporting/batch_detail_records/messaging/{id} | getMdrRequest | MDR Detailed Reports |
| DELETE | /legacy/reporting/batch_detail_records/messaging/{id} | deleteMdrRequest | MDR Detailed Reports |
| GET | /legacy/reporting/usage_reports/messaging | getMdrUsageReports | MDR Usage Reports |
| POST | /legacy/reporting/usage_reports/messaging | submitMdrUsageReport | MDR Usage Reports |
| GET | /legacy/reporting/usage_reports/messaging/{id} | getMdrUsageReport | MDR Usage Reports |
| DELETE | /legacy/reporting/usage_reports/messaging/{id} | deleteMdrUsageReport | MDR Usage Reports |
| GET | /legacy_reporting/batch_detail_records/messaging | getMdrRequests_2 | MDR Detailed Reports |
| POST | /legacy_reporting/batch_detail_records/messaging | submitMdrRequest_2 | MDR Detailed Reports |
| GET | /legacy_reporting/batch_detail_records/messaging/{id} | getMdrRequest_2 | MDR Detailed Reports |
| DELETE | /legacy_reporting/batch_detail_records/messaging/{id} | deleteMdrRequest_2 | MDR Detailed Reports |
| GET | /legacy_reporting/usage_reports/messaging | getMdrUsageReports_2 | MDR Usage Reports |
| POST | /legacy_reporting/usage_reports/messaging | submitMdrUsageReport_2 | MDR Usage Reports |
| GET | /legacy_reporting/usage_reports/messaging/{id} | getMdrUsageReport_2 | MDR Usage Reports |
| DELETE | /legacy_reporting/usage_reports/messaging/{id} | deleteMdrUsageReport_2 | MDR Usage Reports |
| POST | /messages/whatsapp | SendWhatsappMessage | Whatsapp messaging |
| GET | /messaging/hosted/numbers | ListMessagingHostedNumbers | Messaging |
| POST | /messaging/profiles/{id}/actions/regenerate/secret | RegenerateMessagingProfileSecret | Messaging |
| GET | /messaging/profiles/{id}/alphanumeric/sender/ids | ListProfileAlphanumericSenderIds | Messaging |
| GET | /messaging/profiles/{id}/metrics | GetDetailedProfileMetrics | Messaging |
| GET | /messaging/rcs/agents | ListRCSAgents | RCS |
| GET | /messaging/rcs/agents/{id} | GetRCSAgentById | RCS |
| PATCH | /messaging/rcs/agents/{id} | UpdateRCSAgentById | RCS |
| POST | /messaging/rcs/bulk_capabilities | ListRCSCapabilitiesOfAPhoneNumbersBatch | RCS |
| GET | /messaging/rcs/capabilities/{agent_id}/{phone_number} | ListRCSCapabilitiesOfAPhoneNumber | RCS |
| PUT | /messaging/rcs/test_number_invite/{id}/{phone_number} | InviteATestNumberToRCS | RCS |
| GET | /messaging/tollfree/verification/requests/{id}/status/history | GetVerificationStatusHistory | Verification Requests |
| GET | /messaging_hosted_number_orders | ListMessagingHostedNumberOrders | Hosted Numbers |
| POST | /messaging_hosted_number_orders | CreateMessagingHostedNumberOrder | Hosted Numbers |
| POST | /messaging_hosted_number_orders/eligibility_numbers_check | CheckEligibilityNumbers | Hosted Numbers |
| GET | /messaging_hosted_number_orders/{id} | GetMessagingHostedNumberOrder | Hosted Numbers |
| DELETE | /messaging_hosted_number_orders/{id} | DeleteMessagingHostedNumberOrder | Hosted Numbers |
| POST | /messaging_hosted_number_orders/{id}/actions/file_upload | UploadMessagingHostedNumberOrderFile | Hosted Numbers |
| POST | /messaging_hosted_number_orders/{id}/validation_codes | ValidateVerificationCodesForMessagingHostedNumberOrder | Hosted Numbers |
| POST | /messaging_hosted_number_orders/{id}/verification_codes | CreateVerificationCodesForMessagingHostedNumberOrder | Hosted Numbers |
| GET | /messaging_hosted_numbers | ListMessagingHostedNumbers_2 | Messaging |
| GET | /messaging_hosted_numbers/{id} | GetMessagingHostedNumber | Messaging |
| PATCH | /messaging_hosted_numbers/{id} | UpdateMessagingHostedNumber | Messaging |
| DELETE | /messaging_hosted_numbers/{id} | DeleteMessagingHostedNumber | Hosted Numbers |
| POST | /messaging_numbers/bulk_updates | BulkUpdateMessagingSettingsOnPhoneNumbers | Number Settings |
| GET | /messaging_numbers/bulk_updates/{order_id} | GetBulkUpdateMessagingSettingsOnPhoneNumbersStatus | Number Settings |
| POST | /messaging_numbers_bulk_updates | BulkUpdateMessagingSettingsOnPhoneNumbers_2 | Number Settings |
| GET | /messaging_numbers_bulk_updates/{order_id} | GetBulkUpdateMessagingSettingsOnPhoneNumbersStatus_2 | Number Settings |
| GET | /messaging_optouts | ListOptOuts | Opt-Out Management |
| GET | /messaging_profile_metrics | GetProfileMetrics | Messaging |
| GET | /messaging_profiles | ListMessagingProfiles | Profiles |
| POST | /messaging_profiles | CreateMessagingProfile | Profiles |
| GET | /messaging_profiles/{id} | RetrieveMessagingProfile | Profiles |
| PATCH | /messaging_profiles/{id} | UpdateMessagingProfile | Profiles |
| DELETE | /messaging_profiles/{id} | DeleteMessagingProfile | Profiles |
| POST | /messaging_profiles/{id}/actions/regenerate_secret | RegenerateMessagingProfileSecret_2 | Messaging |
| GET | /messaging_profiles/{id}/alphanumeric_sender_ids | ListProfileAlphanumericSenderIds_2 | Messaging |
| GET | /messaging_profiles/{id}/metrics | GetDetailedProfileMetrics_2 | Messaging |
| GET | /messaging_profiles/{id}/phone_numbers | ListProfilePhoneNumbers | Profiles |
| GET | /messaging_profiles/{id}/short_codes | ListProfileShortCodes | Profiles |
| GET | /messaging_profiles/{profile_id}/autoresp_configs | GetAutorespConfigs | Opt-Out Management |
| POST | /messaging_profiles/{profile_id}/autoresp_configs | CreateAutorespConfig | Opt-Out Management |
| GET | /messaging_profiles/{profile_id}/autoresp_configs/{autoresp_cfg_id} | GetAutorespConfig | Opt-Out Management |
| PUT | /messaging_profiles/{profile_id}/autoresp_configs/{autoresp_cfg_id} | UpdateAutoRespConfig | Opt-Out Management |
| DELETE | /messaging_profiles/{profile_id}/autoresp_configs/{autoresp_cfg_id} | DeleteAutorespConfig | Opt-Out Management |
| GET | /messaging_tollfree/verification/requests | ListVerificationRequests | Verification Requests |
| POST | /messaging_tollfree/verification/requests | SubmitVerificationRequest | Verification Requests |
| GET | /messaging_tollfree/verification/requests/{id} | GetVerificationRequest | Verification Requests |
| PATCH | /messaging_tollfree/verification/requests/{id} | UpdateVerificationRequest | Verification Requests |
| DELETE | /messaging_tollfree/verification/requests/{id} | DeleteVerificationRequest | Verification Requests |
| GET | /messaging_tollfree/verification/requests/{id}/status_history | GetVerificationStatusHistory_2 | Verification Requests |
| GET | /messaging_url_domains | ListMessagingUrlDomains | Messaging URL Domains |
| GET | /mobile_phone_numbers/messaging | ListMobilePhoneNumbersWithMessagingSettings | Mobile Number Settings |
| GET | /mobile_phone_numbers/{id}/messaging | GetMobilePhoneNumberMessagingSettings | Mobile Number Settings |
| GET | /phone_numbers/messaging | ListPhoneNumbersWithMessagingSettings | Number Settings |
| GET | /phone_numbers/{id}/messaging | GetPhoneNumberMessagingSettings | Number Settings |
| PATCH | /phone_numbers/{id}/messaging | UpdatePhoneNumberMessagingSettings | Number Settings |
| GET | /reports/mdr_usage_reports | GetMdrUsageReports | MDR Usage Reports |
| GET | /reports/mdr_usage_reports/{id} | GetUsageReport | MDR Usage Reports |
