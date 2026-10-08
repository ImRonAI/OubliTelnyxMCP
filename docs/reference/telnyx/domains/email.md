# email

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| POST | /10dlc/brand/{brandId}/2faEmail | ResendBrand2faEmail | Brands |
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
| GET | /phone_numbers/{phone_number_id}/voicemail | GetVoicemail | Voicemail |
| POST | /phone_numbers/{phone_number_id}/voicemail | CreateVoicemail | Voicemail |
| PATCH | /phone_numbers/{phone_number_id}/voicemail | UpdateVoicemail | Voicemail |
