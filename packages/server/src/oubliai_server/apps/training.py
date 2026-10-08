"""Training workspace: fine-tuning jobs (schema: /ai/fine_tuning/jobs; list has no paging).

Only the documented job lifecycle exists: create, list, retrieve, cancel
(`domains/training/AGENTS.md`).
"""

from fastmcp.apps.app import FastMCPApp
from prefab_ui.app import PrefabApp
from prefab_ui.rx import STATE
from pydantic import BaseModel

from oubliai_server.apps.recipes import (
    ColumnSpec,
    ListSpec,
    confirm_action,
    list_workspace,
    register_confirmed_backend,
    register_detail_backend,
    register_list_backend,
)

GENERATED_TOOLS = frozenset(
    {"get_finetuningjob_public_finetuning_get", "create_new_finetuningjob_public_finetuning_post",
     "get_finetuningjob_public_finetuning__job_id__get",
     "cancel_new_finetuningjob_public_finetuning_post"}
)
# Registered MCP name: operationId up to the first `__` (FastMCP default rule).
JOB_GET = "get_finetuningjob_public_finetuning"
JOB_CANCEL = "cancel_new_finetuningjob_public_finetuning_post"
CONFIRMED_ACTIONS = (JOB_CANCEL,)


# Creating a fine-tuning job incurs training cost, so it is not a one-click form: run
# create_new_finetuningjob_public_finetuning_post explicitly through execute.
FORM_MODELS: dict[str, type[BaseModel]] = {}
COLUMNS = (
    ColumnSpec("model", "Model"),
    ColumnSpec("status", "Status"),
    ColumnSpec("training_file", "Training file"),
    ColumnSpec("created_at", "Created", format="date"),
)

app = FastMCPApp("oubliai-training")

jobs_list = register_list_backend(
    app,
    name="finetuning_jobs_list",
    spec=ListSpec(
        tool="get_finetuningjob_public_finetuning_get", data_path=("data",), columns=COLUMNS, paging="none"
    ),
)
jobs_get = register_detail_backend(app, name="finetuning_jobs_get", tool=JOB_GET, id_param="job_id")
jobs_cancel = register_confirmed_backend(
    app, name="finetuning_jobs_cancel", tool=JOB_CANCEL, id_param="job_id"
)


def _cancel_action() -> None:
    confirm_action(
        label="Cancel job",
        title="Cancel fine-tuning job",
        description="Stops the in-progress job; trained tokens so far are billed.",
        backend=jobs_cancel,
        resource_id_rx=STATE.selected.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Fine-tuning jobs",
        list_backend=jobs_list,
        columns=COLUMNS,
        detail_backend=jobs_get,
        detail_fields=(("id", "ID"), ("status", "Status"), ("trained_tokens", "Trained tokens")),
        actions=(_cancel_action,),
        paging="none",
        notes=(
            "Creating a job incurs training cost: run create_new_finetuningjob_public_finetuning_post "
            "(model, training_file) explicitly through execute.",
            "Job objects are returned bare (no data envelope).",
        ),
    )


@app.ui("training_workspace", description="Open the Telnyx fine-tuning workspace.")
def training_workspace() -> PrefabApp:
    return workspace()
