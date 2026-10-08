"""RAG workspace: embedding buckets and tasks (schema: /ai/embeddings/buckets, /ai/embeddings).

GetEmbeddingBuckets returns {data: {buckets: [...]}}; pending ingestion is not searchable
completion (`domains/rag/AGENTS.md`).
"""

from fastmcp.apps.app import FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.rx import STATE
from pydantic import BaseModel, Field

from oubliai_server.apps.recipes import (
    ColumnSpec,
    ListSpec,
    confirm_action,
    list_workspace,
    register_confirmed_backend,
    register_detail_backend,
    register_form_backend,
    register_list_backend,
)

GENERATED_TOOLS = frozenset(
    {"GetEmbeddingBuckets", "GetBucketName", "DeleteEmbeddingBucket", "PostEmbeddingUrl",
     "GetTasksByStatus", "GetEmbeddingTask", "PostEmbeddingSimilaritySearch"}
)
CONFIRMED_ACTIONS = ("DeleteEmbeddingBucket",)


class EmbeddingUrlInput(BaseModel):
    """`PostEmbeddingUrl` request body."""

    url: str = Field(title="Web page URL")
    bucket_name: str = Field(title="Bucket name")


FORM_MODELS = {"PostEmbeddingUrl": EmbeddingUrlInput}
COLUMNS = (
    ColumnSpec("task_name", "Task"),
    ColumnSpec("status", "Status"),
    ColumnSpec("bucket", "Bucket"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-rag")

tasks_list = register_list_backend(
    app,
    name="embedding_tasks_list",
    spec=ListSpec(tool="GetTasksByStatus", data_path=("data",), columns=COLUMNS, paging="none"),
)
buckets_list = register_list_backend(
    app,
    name="embedding_buckets_list",
    spec=ListSpec(tool="GetEmbeddingBuckets", data_path=("data", "buckets"), columns=(), paging="none"),
)
tasks_get = register_detail_backend(
    app, name="embedding_tasks_get", tool="GetEmbeddingTask", id_param="task_id"
)
buckets_delete = register_confirmed_backend(
    app, name="embedding_buckets_delete", tool="DeleteEmbeddingBucket", id_param="bucket_name"
)
embed_url = register_form_backend(
    app, name="embedding_url_create", tool="PostEmbeddingUrl", model=EmbeddingUrlInput
)


def _delete_bucket_action() -> None:
    confirm_action(
        label="Delete bucket",
        title="Delete embedding bucket",
        description="Type the bucket name. All embedded documents in the bucket are removed.",
        backend=buckets_delete,
        resource_id_rx=STATE.selected.data.bucket,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Embedding tasks",
        list_backend=tasks_list,
        columns=COLUMNS,
        detail_backend=tasks_get,
        detail_fields=(("data.task_id", "Task ID"), ("data.status", "Status"), ("data.bucket", "Bucket")),
        create_form=(EmbeddingUrlInput, embed_url),
        actions=(_delete_bucket_action,),
        paging="none",
        row_id_key="task_id",
        notes=(
            "Buckets: GetEmbeddingBuckets (data.buckets), GetBucketName lists a bucket's documents.",
            "Search: PostEmbeddingSimilaritySearch. Pending tasks are not yet searchable.",
        ),
    )


@app.ui("rag_workspace", description="Open the Telnyx embeddings (RAG) workspace.")
def rag_workspace() -> PrefabApp:
    return workspace()
