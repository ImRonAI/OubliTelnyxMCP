# fax

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| GET | /fax_applications | ListFaxApplications | Programmable Fax Applications |
| POST | /fax_applications | CreateFaxApplication | Programmable Fax Applications |
| GET | /fax_applications/{id} | GetFaxApplication | Programmable Fax Applications |
| PATCH | /fax_applications/{id} | UpdateFaxApplication | Programmable Fax Applications |
| DELETE | /fax_applications/{id} | DeleteFaxApplication | Programmable Fax Applications |
| GET | /faxes | ListFaxes | Programmable Fax Commands |
| POST | /faxes | SendFax | Programmable Fax Commands |
| GET | /faxes/{id} | ViewFax | Programmable Fax Commands |
| DELETE | /faxes/{id} | DeleteFax | Programmable Fax Commands |
| POST | /faxes/{id}/actions/cancel | CancelFax | Programmable Fax Commands |
| POST | /faxes/{id}/actions/refresh | RefreshFax | Programmable Fax Commands |
