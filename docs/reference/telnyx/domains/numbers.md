# numbers

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| GET | /10dlc/phoneNumberAssignmentByProfile/{taskId}/phoneNumbers | GetPhoneNumberStatus | Bulk Phone Number Campaigns |
| POST | /addresses/{id}/actions/accept_suggestions | acceptAddressSuggestions | Addresses |
| GET | /available_phone_numbers | ListAvailablePhoneNumbers | Phone Number Search |
| GET | /dir/{dir_id}/phone_numbers | listDirPhoneNumbersSimplified | Phone Numbers |
| POST | /dir/{dir_id}/phone_numbers | addDirPhoneNumbersSimplified | Phone Numbers |
| DELETE | /dir/{dir_id}/phone_numbers | deleteDirPhoneNumbersSimplified | Phone Numbers |
| GET | /enterprises/{enterprise_id}/reputation/numbers | listReputationNumbers | Reputation |
| POST | /enterprises/{enterprise_id}/reputation/numbers | associateReputationNumbers | Reputation |
| POST | /enterprises/{enterprise_id}/reputation/numbers/refresh | refreshReputationNumbers | Reputation |
| GET | /enterprises/{enterprise_id}/reputation/numbers/{phone_number} | getPhoneNumberReputation | Reputation |
| DELETE | /enterprises/{enterprise_id}/reputation/numbers/{phone_number} | disassociateReputationNumber | Reputation |
| POST | /enterprises/{enterprise_id}/reputation/remediation | submitReputationRemediation | Reputation |
| GET | /external_connections/{id}/phone_numbers | ListExternalConnectionPhoneNumbers | External Connections |
| GET | /external_connections/{id}/phone_numbers/{phone_number_id} | GetExternalConnectionPhoneNumber | External Connections |
| PATCH | /external_connections/{id}/phone_numbers/{phone_number_id} | UpdateExternalConnectionPhoneNumber | External Connections |
| GET | /list | GetAllNumbersChannelZones | Voice Channels |
| GET | /list/{channel_zone_id} | GetNumbersChannelZones | Voice Channels |
| GET | /messaging/hosted/numbers | ListMessagingHostedNumbers | Messaging |
| POST | /messaging/rcs/bulk_capabilities | ListRCSCapabilitiesOfAPhoneNumbersBatch | RCS |
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
| GET | /messaging_profiles/{id}/phone_numbers | ListProfilePhoneNumbers | Profiles |
| GET | /mobile_phone_numbers/messaging | ListMobilePhoneNumbersWithMessagingSettings | Mobile Number Settings |
| GET | /mobile_phone_numbers/{id}/messaging | GetMobilePhoneNumberMessagingSettings | Mobile Number Settings |
| GET | /number_order_phone_numbers | RetrieveOrderPhoneNumbers | Phone Number Orders |
| POST | /number_order_phone_numbers/{id}/requirement_group | updateNumberOrderPhoneNumberRequirementGroup | Requirement Groups |
| GET | /number_order_phone_numbers/{number_order_phone_number_id} | GetNumberOrderPhoneNumber | Phone Number Orders |
| PATCH | /number_order_phone_numbers/{number_order_phone_number_id} | UpdateNumberOrderPhoneNumber | Phone Number Orders |
| POST | /numbers_features | PostNumbersFeatures | numbers features |
| POST | /phone_number_blocks/jobs/delete_phone_number_block | CreatePhoneNumberBlockDeletionJob | Phone Number Blocks Background Jobs |
| GET | /phone_numbers | ListPhoneNumbers | Phone Number Configurations |
| POST | /phone_numbers/actions/verify_ownership | VerifyPhoneNumberOwnership | Phone Number Configurations |
| GET | /phone_numbers/csv_downloads | ListCsvDownloads | CSV Downloads |
| POST | /phone_numbers/csv_downloads | CreateCsvDownload | CSV Downloads |
| GET | /phone_numbers/csv_downloads/{id} | GetCsvDownload | CSV Downloads |
| GET | /phone_numbers/jobs | ListPhoneNumbersJobs | Bulk Phone Number Operations |
| POST | /phone_numbers/jobs/delete_phone_numbers | CreateDeletePhoneNumbersJob | Bulk Phone Number Operations |
| POST | /phone_numbers/jobs/update_emergency_settings | CreatePhoneNumbersJobUpdateEmergencySettings | Bulk Phone Number Operations |
| POST | /phone_numbers/jobs/update_phone_numbers | CreateUpdatePhoneNumbersJob | Bulk Phone Number Operations |
| GET | /phone_numbers/jobs/{id} | RetrievePhoneNumbersJob | Bulk Phone Number Operations |
| GET | /phone_numbers/messaging | ListPhoneNumbersWithMessagingSettings | Number Settings |
| GET | /phone_numbers/regulatory_requirements | ListRegulatoryRequirementsPhoneNumbers | Regulatory Requirements |
| GET | /phone_numbers/slim | SlimListPhoneNumbers | Phone Number Configurations |
| GET | /phone_numbers/voice | ListPhoneNumbersWithVoiceSettings | Phone Number Configurations |
| GET | /phone_numbers/{id} | RetrievePhoneNumber | Phone Number Configurations |
| PATCH | /phone_numbers/{id} | UpdatePhoneNumber | Phone Number Configurations |
| DELETE | /phone_numbers/{id} | DeletePhoneNumber | Phone Number Configurations |
| PATCH | /phone_numbers/{id}/actions/bundle_status_change | PhoneNumberBundleStatusChange | Phone Number Configurations |
| POST | /phone_numbers/{id}/actions/enable_emergency | EnablePhoneNumberEmergency | Phone Number Configurations |
| GET | /phone_numbers/{id}/messaging | GetPhoneNumberMessagingSettings | Number Settings |
| PATCH | /phone_numbers/{id}/messaging | UpdatePhoneNumberMessagingSettings | Number Settings |
| GET | /phone_numbers/{id}/voice | GetPhoneNumberVoiceSettings | Phone Number Configurations |
| PATCH | /phone_numbers/{id}/voice | UpdatePhoneNumberVoiceSettings | Phone Number Configurations |
| GET | /phone_numbers/{phone_number_id}/voicemail | GetVoicemail | Voicemail |
| POST | /phone_numbers/{phone_number_id}/voicemail | CreateVoicemail | Voicemail |
| PATCH | /phone_numbers/{phone_number_id}/voicemail | UpdateVoicemail | Voicemail |
| GET | /phone_numbers_regulatory_requirements | ListRegulatoryRequirementsPhoneNumbers_2 | Regulatory Requirements |
| POST | /porting_orders/{id}/verification_codes/verify | VerifyPortingVerificationCodes | Porting Orders |
| GET | /porting_orders/{porting_order_id}/associated_phone_numbers | listPortingAssociatedPhoneNumbers | Porting Orders |
| POST | /porting_orders/{porting_order_id}/associated_phone_numbers | createPortingAssociatedPhoneNumber | Porting Orders |
| DELETE | /porting_orders/{porting_order_id}/associated_phone_numbers/{id} | deletePortingAssociatedPhoneNumber | Porting Orders |
| GET | /porting_phone_numbers | ListPortingPhoneNumbers | Porting Orders |
| GET | /reputation/numbers | listReputationNumbersSimplified | Reputation |
| GET | /reputation/numbers/{phone_number} | getPhoneNumberReputationSimplified | Reputation |
| DELETE | /reputation/numbers/{phone_number} | disassociateReputationNumberSimplified | Reputation |
| GET | /v2/mobile_phone_numbers | listMobilePhoneNumbers | Mobile Phone Numbers |
| GET | /v2/mobile_phone_numbers/{id} | retrieveMobilePhoneNumber | Mobile Phone Numbers |
| PATCH | /v2/mobile_phone_numbers/{id} | updateMobilePhoneNumber | Mobile Phone Numbers |
| GET | /v2/whatsapp/business_accounts/{id}/phone_numbers | ListWabaPhones | Whatsapp Business Accounts |
| POST | /v2/whatsapp/business_accounts/{id}/phone_numbers | InitializeWhatsappVerification | Whatsapp Phone Numbers |
| GET | /v2/whatsapp/phone_numbers | ListWhatsappPhoneNumbers | Whatsapp Phone Numbers |
| GET | /v2/whatsapp/phone_numbers/{phone_number} | GetWhatsappPhoneNumber | Whatsapp Phone Numbers |
| DELETE | /v2/whatsapp/phone_numbers/{phone_number} | DeleteWhatsappPhoneNumber | Whatsapp Phone Numbers |
| GET | /v2/whatsapp/phone_numbers/{phone_number}/calling_settings | GetWhatsappCallingSettings | Whatsapp Phone Numbers |
| PATCH | /v2/whatsapp/phone_numbers/{phone_number}/calling_settings | PatchWhatsappCallingSettings | Whatsapp Phone Numbers |
| GET | /v2/whatsapp/phone_numbers/{phone_number}/conversation_window | GetWhatsappConversationWindow | Whatsapp Phone Numbers |
| GET | /v2/whatsapp/phone_numbers/{phone_number}/conversational_components | GetWhatsappConversationalComponents | Whatsapp Phone Numbers |
| PATCH | /v2/whatsapp/phone_numbers/{phone_number}/conversational_components | PatchWhatsappConversationalComponents | Whatsapp Phone Numbers |
| GET | /v2/whatsapp/phone_numbers/{phone_number}/profile | GetWhatsappProfile | Whatsapp Phone Numbers |
| PATCH | /v2/whatsapp/phone_numbers/{phone_number}/profile | PatchWhatsappProfile | Whatsapp Phone Numbers |
| GET | /v2/whatsapp/phone_numbers/{phone_number}/profile/photo | GetWhatsappProfilePhoto | Whatsapp Phone Numbers |
| POST | /v2/whatsapp/phone_numbers/{phone_number}/profile/photo | PostWhatsappProfilePhoto | Whatsapp Phone Numbers |
| DELETE | /v2/whatsapp/phone_numbers/{phone_number}/profile/photo | DeleteWhatsappProfilePhoto | Whatsapp Phone Numbers |
| POST | /v2/whatsapp/phone_numbers/{phone_number}/resend_verification | ResendWhatsappVerification | Whatsapp Phone Numbers |
| POST | /v2/whatsapp/phone_numbers/{phone_number}/verify | VerifyWhatsappPhoneNumber | Whatsapp Phone Numbers |
| GET | /verified_numbers | ListVerifiedNumbers | Verified Numbers |
| POST | /verified_numbers | CreateVerifiedNumber | Verified Numbers |
| GET | /verified_numbers/{phone_number} | GetVerifiedNumber | Verified Numbers |
| DELETE | /verified_numbers/{phone_number} | DeleteVerifiedNumber | Verified Numbers |
| POST | /verified_numbers/{phone_number}/actions/verify | VerifyVerificationCode | Verified Numbers |
| GET | /whatsapp/business_accounts/{id}/phone_numbers | ListWabaPhones_2 | Whatsapp Business Accounts |
| POST | /whatsapp/business_accounts/{id}/phone_numbers | InitializeWhatsappVerification_2 | Whatsapp Phone Numbers |
| GET | /whatsapp/phone_numbers | ListPhoneNumbers_2 | Whatsapp Phone Numbers |
| GET | /whatsapp/phone_numbers/{phone_number} | GetWhatsappPhoneNumber_2 | Whatsapp Phone Numbers |
| DELETE | /whatsapp/phone_numbers/{phone_number} | DeleteWhatsappPhoneNumber_2 | Whatsapp Phone Numbers |
| GET | /whatsapp/phone_numbers/{phone_number}/calling_settings | GetWhatsappCallingSettings_2 | Whatsapp Phone Numbers |
| PATCH | /whatsapp/phone_numbers/{phone_number}/calling_settings | PatchWhatsappCallingSettings_2 | Whatsapp Phone Numbers |
| GET | /whatsapp/phone_numbers/{phone_number}/conversation_window | GetWhatsappConversationWindow_2 | Whatsapp Phone Numbers |
| GET | /whatsapp/phone_numbers/{phone_number}/conversational_components | GetWhatsappConversationalComponents_2 | Whatsapp Phone Numbers |
| PATCH | /whatsapp/phone_numbers/{phone_number}/conversational_components | PatchWhatsappConversationalComponents_2 | Whatsapp Phone Numbers |
| GET | /whatsapp/phone_numbers/{phone_number}/profile | GetWhatsappProfile_2 | Whatsapp Phone Numbers |
| PATCH | /whatsapp/phone_numbers/{phone_number}/profile | PatchWhatsappProfile_2 | Whatsapp Phone Numbers |
| GET | /whatsapp/phone_numbers/{phone_number}/profile/photo | GetWhatsappProfilePhoto_2 | Whatsapp Phone Numbers |
| POST | /whatsapp/phone_numbers/{phone_number}/profile/photo | PostWhatsappProfilePhoto_2 | Whatsapp Phone Numbers |
| DELETE | /whatsapp/phone_numbers/{phone_number}/profile/photo | DeleteWhatsappProfilePhoto_2 | Whatsapp Phone Numbers |
| POST | /whatsapp/phone_numbers/{phone_number}/resend_verification | ResendWhatsappVerification_2 | Whatsapp Phone Numbers |
| POST | /whatsapp/phone_numbers/{phone_number}/verify | VerifyWhatsappPhoneNumber_2 | Whatsapp Phone Numbers |
