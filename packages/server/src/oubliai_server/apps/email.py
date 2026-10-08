"""Email workspace: outbound email messages (schema: /email_messages, cursor paged).

Domains, inboxes and drafts stay on their own generated tools; DNS records are only
read and verified, never replaced (`domains/email/AGENTS.md`).
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
    {"ListEmailMessages", "GetEmailMessage", "DeleteEmailMessage", "ListEmailInboxes",
     "CreateEmailInbox", "listEmailDomains", "listEmailDomainDnsRecords",
     "verifyEmailDomainDnsRecords"}
)
CONFIRMED_ACTIONS = ("DeleteEmailMessage",)


class EmailInboxInput(BaseModel):
    """`CreateEmailInbox` request body."""

    username: str | None = Field(default=None, title="Inbox username")
    domain_id: str | None = Field(default=None, title="Domain ID")


FORM_MODELS = {"CreateEmailInbox": EmailInboxInput}
COLUMNS = (
    ColumnSpec("status", "Status"),
    ColumnSpec("from", "From"),
    ColumnSpec("subject", "Subject"),
    ColumnSpec("id", "ID"),
)

app = FastMCPApp("oubliai-email")

messages_list = register_list_backend(
    app,
    name="email_messages_list",
    spec=ListSpec(tool="ListEmailMessages", data_path=("data",), columns=COLUMNS, paging="none"),
)
messages_get = register_detail_backend(
    app, name="email_messages_get", tool="GetEmailMessage", id_param="id"
)
messages_delete = register_confirmed_backend(
    app, name="email_messages_delete", tool="DeleteEmailMessage", id_param="id"
)
inboxes_create = register_form_backend(
    app, name="email_inboxes_create", tool="CreateEmailInbox", model=EmailInboxInput
)


def _delete_action() -> None:
    confirm_action(
        label="Delete message",
        title="Delete email message",
        description="Removes the message record.",
        backend=messages_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Email messages",
        list_backend=messages_list,
        columns=COLUMNS,
        detail_backend=messages_get,
        detail_fields=(("data.id", "ID"), ("data.status", "Status"), ("data.subject", "Subject")),
        create_form=(EmailInboxInput, inboxes_create),
        actions=(_delete_action,),
        paging="none",
        notes=(
            "ListEmailMessages pages with page_size/page_cursor; this view shows the first page.",
            "Sending (CreateEmailMessage) is a live side effect: run it through execute.",
            "Domains: listEmailDomains, listEmailDomainDnsRecords, verifyEmailDomainDnsRecords.",
        ),
    )


@app.ui("email_workspace", description="Open the Telnyx email workspace.")
def email_workspace() -> PrefabApp:
    return workspace()
