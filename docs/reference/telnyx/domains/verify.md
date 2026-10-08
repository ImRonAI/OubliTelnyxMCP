# verify

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| PUT | /10dlc/brand/{brandId}/smsOtp | VerifyBrandSmsOtp | Brands |
| POST | /customer_service_records/phone_number_coverages | VerifyPhoneNumberCoverage | Customer Service Record |
| GET | /dir/{dir_id}/verify_email | getDirEmailVerificationStatus | Email Verification |
| POST | /dir/{dir_id}/verify_email | requestDirEmailVerification | Email Verification |
| POST | /dir/{dir_id}/verify_email/confirm | confirmDirEmailVerification | Email Verification |
| POST | /email_domains/{domain_id}/verify | verifyEmailDomainDnsRecords | Email Domain DNS Records |
| POST | /phone_numbers/actions/verify_ownership | VerifyPhoneNumberOwnership | Phone Number Configurations |
| POST | /porting_orders/{id}/verification_codes/verify | VerifyPortingVerificationCodes | Porting Orders |
| POST | /v2/whatsapp/phone_numbers/{phone_number}/verify | VerifyWhatsappPhoneNumber | Whatsapp Phone Numbers |
| GET | /verifications/by_phone_number/{phone_number} | ListVerifications | Verify |
| POST | /verifications/by_phone_number/{phone_number}/actions/verify | VerifyVerificationCodeByPhoneNumber | Verify |
| POST | /verifications/call | CreateVerificationCall | Verify |
| POST | /verifications/flashcall | CreateFlashcallVerification | Verify |
| POST | /verifications/sms | CreateVerificationSms | Verify |
| POST | /verifications/whatsapp | CreateWhatsappVerification | Verify |
| GET | /verifications/{verification_id} | RetrieveVerification | Verify |
| POST | /verifications/{verification_id}/actions/verify | VerifyVerificationCodeById | Verify |
| POST | /verified_numbers/{phone_number}/actions/verify | VerifyVerificationCode | Verified Numbers |
| GET | /verify_profiles | ListProfiles | Verify |
| POST | /verify_profiles | CreateVerifyProfile | Verify |
| GET | /verify_profiles/templates | ListProfileMessageTemplates | Verify |
| POST | /verify_profiles/templates | CreateMessageTemplate | Verify |
| PATCH | /verify_profiles/templates/{template_id} | UpdateMessageTemplate | Verify |
| GET | /verify_profiles/{verify_profile_id} | GetVerifyProfile | Verify |
| PATCH | /verify_profiles/{verify_profile_id} | UpdateVerifyProfile | Verify |
| DELETE | /verify_profiles/{verify_profile_id} | DeleteProfile | Verify |
| POST | /whatsapp/phone_numbers/{phone_number}/verify | VerifyWhatsappPhoneNumber_2 | Whatsapp Phone Numbers |
