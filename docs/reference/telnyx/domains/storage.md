# storage

Rows are derived from `docs/reference/telnyx/operation-index.json`; use exact pointers and security from the OpenAPI source.

| method | path | operationId | tags |
|---|---|---|---|
| GET | /custom_storage_credentials/{connection_id} | GetCustomStorageCredentials | Call Recordings |
| POST | /custom_storage_credentials/{connection_id} | CreateCustomStorageCredentials | Call Recordings |
| PUT | /custom_storage_credentials/{connection_id} | UpdateCustomStorageCredentials | Call Recordings |
| DELETE | /custom_storage_credentials/{connection_id} | DeleteCustomStorageCredentials | Call Recordings |
| GET | /media | ListMediaStorage | Media Storage API |
| POST | /media | CreateMediaStorage | Media Storage API |
| GET | /media/{media_name} | GetMediaStorage | Media Storage API |
| PUT | /media/{media_name} | UpdateMediaStorage | Media Storage API |
| DELETE | /media/{media_name} | DeleteMediaStorage | Media Storage API |
| GET | /media/{media_name}/download | DownloadMedia | Media Storage API |
| GET | /storage/buckets/{bucketName}/ssl_certificate | GetStorageSSLCertificates | Bucket SSL Certificate |
| PUT | /storage/buckets/{bucketName}/ssl_certificate | AddStorageSSLCertificate | Bucket SSL Certificate |
| DELETE | /storage/buckets/{bucketName}/ssl_certificate | RemoveStorageSSLCertificate | Bucket SSL Certificate |
| GET | /storage/buckets/{bucketName}/usage/api | GetStorageAPIUsage | Bucket Usage |
| GET | /storage/buckets/{bucketName}/usage/storage | GetBucketUsage | Bucket Usage |
| POST | /storage/buckets/{bucketName}/{objectName}/presigned_url | CreatePresignedObjectUrl | Presigned Object URLs |
| GET | /storage/cloudfs | ListCloudfsFilesystems | cloudfs filesystems |
| POST | /storage/cloudfs | CreateCloudfsFilesystem | cloudfs filesystems |
| GET | /storage/cloudfs/{id} | GetCloudfsFilesystem | cloudfs filesystems |
| PATCH | /storage/cloudfs/{id} | UpdateCloudfsFilesystem | cloudfs filesystems |
| DELETE | /storage/cloudfs/{id} | DeleteCloudfsFilesystem | cloudfs filesystems |
| POST | /storage/cloudfs/{id}/actions/rotate-meta-token | RotateCloudfsMetaToken | cloudfs filesystems |
| GET | /storage/kvs | ListKvNamespaces | kv namespaces |
| POST | /storage/kvs | CreateKvNamespace | kv namespaces |
| GET | /storage/kvs/{id} | GetKvNamespace | kv namespaces |
| DELETE | /storage/kvs/{id} | DeleteKvNamespace | kv namespaces |
| GET | /storage/kvs/{id}/keys | ListKvKeys | kv keys |
| GET | /storage/kvs/{id}/keys/{key} | GetKvKey | kv keys |
| PUT | /storage/kvs/{id}/keys/{key} | PutKvKey | kv keys |
| DELETE | /storage/kvs/{id}/keys/{key} | DeleteKvKey | kv keys |
| GET | /storage/migration_source_coverage | ListMigrationSourceCoverage | Data Migration |
| GET | /storage/migration_sources | ListMigrationSources | Data Migration |
| POST | /storage/migration_sources | CreateMigrationSource | Data Migration |
| GET | /storage/migration_sources/{id} | GetMigrationSource | Data Migration |
| DELETE | /storage/migration_sources/{id} | DeleteMigrationSource | Data Migration |
| GET | /storage/migrations | ListMigrations | Data Migration |
| POST | /storage/migrations | CreateMigration | Data Migration |
| GET | /storage/migrations/{id} | GetMigration | Data Migration |
| POST | /storage/migrations/{id}/actions/stop | StopMigration | Data Migration |
| GET | /storage/sqldbs | ListSqlDatabases | sql databases |
| POST | /storage/sqldbs | CreateSqlDatabase | sql databases |
| GET | /storage/sqldbs/{id} | GetSqlDatabase | sql databases |
| DELETE | /storage/sqldbs/{id} | DeleteSqlDatabase | sql databases |
| POST | /storage/sqldbs/{id}/actions/query | QuerySqlDatabase | sql databases |
