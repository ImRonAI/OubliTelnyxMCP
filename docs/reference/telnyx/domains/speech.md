# speech

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| POST | /ai/audio/transcriptions | audio_public_audio_transcriptions_post | Audio |
| GET | /legacy/reporting/batch/detail/records/speech/to/text | getSttRequests | Speech to Text Batch Reports |
| POST | /legacy/reporting/batch/detail/records/speech/to/text | submitSttRequest | Speech to Text Batch Reports |
| GET | /legacy/reporting/batch/detail/records/speech/to/text/{id} | getSttRequest | Speech to Text Batch Reports |
| DELETE | /legacy/reporting/batch/detail/records/speech/to/text/{id} | deleteSttRequest | Speech to Text Batch Reports |
| GET | /legacy/reporting/batch_detail_records/speech_to_text | getSttRequests_2 | Speech to Text Batch Reports |
| POST | /legacy/reporting/batch_detail_records/speech_to_text | submitSttRequest_2 | Speech to Text Batch Reports |
| GET | /legacy/reporting/batch_detail_records/speech_to_text/{id} | getSttRequest_2 | Speech to Text Batch Reports |
| DELETE | /legacy/reporting/batch_detail_records/speech_to_text/{id} | deleteSttRequest_2 | Speech to Text Batch Reports |
| GET | /legacy/reporting/usage_reports/speech_to_text | getSttUsageReportSync | Speech to text Usage Reports |
| GET | /legacy_reporting/usage_reports/speech_to_text | getSttUsageReportSync_2 | Speech to text Usage Reports |
| GET | /speech-to-text/providers | listSttProviders | Speech To Text Capabilities |
| GET | /speech-to-text/transcription | TranscriptionOverWs | Speech To Text over WebSockets |
| GET | /text-to-speech/speech | TextToSpeechOverWs | Text To Speech Commands |
| POST | /text-to-speech/speech | generateSpeech | Text To Speech Commands |
| GET | /text-to-speech/voices | listVoices | Text To Speech Commands |
| POST | /v1/audio/speech | x402_v1AudioSpeech | x402 |
