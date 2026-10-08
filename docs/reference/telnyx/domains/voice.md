# voice

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| GET | /channel_zones | GetChannelZones | Voice Channels |
| PUT | /channel_zones/{channel_zone_id} | PatchChannelZone | Voice Channels |
| GET | /inbound_channels | ListInboundChannels | Voice Channels |
| PATCH | /inbound_channels | UpdateOutboundChannels | Voice Channels |
| GET | /invoices | ListInvoices |  |
| GET | /invoices/{id} | GetInvoiceById |  |
| GET | /legacy/reporting/batch_detail_records/voice | getCdrRequests | CDR Reports |
| POST | /legacy/reporting/batch_detail_records/voice | submitCdrRequest | CDR Reports |
| GET | /legacy/reporting/batch_detail_records/voice/fields | getCdrsAvailableFields | CDR Reports |
| GET | /legacy/reporting/batch_detail_records/voice/{id} | getCdrRequest | CDR Reports |
| DELETE | /legacy/reporting/batch_detail_records/voice/{id} | deleteCdrRequest | CDR Reports |
| GET | /legacy/reporting/usage_reports/voice | getCdrUsageReports | CDR Usage Reports |
| POST | /legacy/reporting/usage_reports/voice | submitCdrUsageReport | CDR Usage Reports |
| GET | /legacy/reporting/usage_reports/voice/{id} | getCdrUsageReport | CDR Usage Reports |
| DELETE | /legacy/reporting/usage_reports/voice/{id} | deleteCdrUsageReport | CDR Usage Reports |
| GET | /legacy_reporting/batch_detail_records/voice | getCdrRequests_2 | CDR Reports |
| POST | /legacy_reporting/batch_detail_records/voice | submitCdrRequest_2 | CDR Reports |
| GET | /legacy_reporting/batch_detail_records/voice/fields | getCdrsAvailableFields_2 | CDR Reports |
| GET | /legacy_reporting/batch_detail_records/voice/{id} | getCdrRequest_2 | CDR Reports |
| DELETE | /legacy_reporting/batch_detail_records/voice/{id} | deleteCdrRequest_2 | CDR Reports |
| GET | /legacy_reporting/usage_reports/voice | getCdrUsageReports_2 | CDR Usage Reports |
| POST | /legacy_reporting/usage_reports/voice | submitCdrUsageReport_2 | CDR Usage Reports |
| GET | /legacy_reporting/usage_reports/voice/{id} | getCdrUsageReport_2 | CDR Usage Reports |
| DELETE | /legacy_reporting/usage_reports/voice/{id} | deleteCdrUsageReport_2 | CDR Usage Reports |
| GET | /list | GetAllNumbersChannelZones | Voice Channels |
| GET | /list/{channel_zone_id} | GetNumbersChannelZones | Voice Channels |
| GET | /outbound_voice_profiles | ListOutboundVoiceProfiles | Outbound Voice Profiles |
| POST | /outbound_voice_profiles | CreateVoiceProfile | Outbound Voice Profiles |
| GET | /outbound_voice_profiles/{id} | GetOutboundVoiceProfile | Outbound Voice Profiles |
| PATCH | /outbound_voice_profiles/{id} | UpdateOutboundVoiceProfile | Outbound Voice Profiles |
| DELETE | /outbound_voice_profiles/{id} | DeleteOutboundVoiceProfile | Outbound Voice Profiles |
| GET | /phone_numbers/voice | ListPhoneNumbersWithVoiceSettings | Phone Number Configurations |
| GET | /phone_numbers/{id}/voice | GetPhoneNumberVoiceSettings | Phone Number Configurations |
| PATCH | /phone_numbers/{id}/voice | UpdatePhoneNumberVoiceSettings | Phone Number Configurations |
| GET | /phone_numbers/{phone_number_id}/voicemail | GetVoicemail | Voicemail |
| POST | /phone_numbers/{phone_number_id}/voicemail | CreateVoicemail | Voicemail |
| PATCH | /phone_numbers/{phone_number_id}/voicemail | UpdateVoicemail | Voicemail |
| POST | /sim_cards/actions/bulk_disable_voice | DisableVoiceBulk | SIM Cards |
| POST | /sim_cards/actions/bulk_enable_voice | EnableVoiceBulk | SIM Cards |
| POST | /sim_cards/{id}/actions/disable_voice | DisableVoiceSimCard | SIM Cards |
| POST | /sim_cards/{id}/actions/enable_voice | EnableVoiceSimCard | SIM Cards |
| GET | /text-to-speech/voices | listVoices | Text To Speech Commands |
| GET | /v2/mobile_voice_connections | listMobileVoiceConnections | Mobile Voice Connections |
| POST | /v2/mobile_voice_connections | createMobileVoiceConnection | Mobile Voice Connections |
| GET | /v2/mobile_voice_connections/{id} | retrieveMobileVoiceConnection | Mobile Voice Connections |
| PATCH | /v2/mobile_voice_connections/{id} | updateMobileVoiceConnection | Mobile Voice Connections |
| DELETE | /v2/mobile_voice_connections/{id} | deleteMobileVoiceConnection | Mobile Voice Connections |
| GET | /voice_clones | listVoiceClones | Voice Clones |
| POST | /voice_clones | createVoiceClone | Voice Clones |
| POST | /voice_clones/from_upload | createVoiceCloneFromUpload | Voice Clones |
| PATCH | /voice_clones/{id} | updateVoiceClone | Voice Clones |
| DELETE | /voice_clones/{id} | deleteVoiceClone | Voice Clones |
| GET | /voice_clones/{id}/sample | getVoiceCloneSample | Voice Clones |
| GET | /voice_designs | listVoiceDesigns | Voice Designs |
| POST | /voice_designs | createVoiceDesign | Voice Designs |
| GET | /voice_designs/{id} | getVoiceDesign | Voice Designs |
| PATCH | /voice_designs/{id} | updateVoiceDesign | Voice Designs |
| DELETE | /voice_designs/{id} | deleteVoiceDesign | Voice Designs |
| GET | /voice_designs/{id}/sample | getVoiceDesignSample | Voice Designs |
| DELETE | /voice_designs/{id}/versions/{version} | deleteVoiceDesignVersion | Voice Designs |
| GET | /voice_sdk_call_reports | ListVoiceSdkCallReports | Voice SDK Stats |
| GET | /voice_sdk_call_reports/{call_id} | GetVoiceSdkCallReport | Voice SDK Stats |
