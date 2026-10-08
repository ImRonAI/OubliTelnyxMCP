"""Numbers workspace: phone numbers and number orders (schema: /phone_numbers, /number_orders).

Ordering incurs cost and deleting a number is destructive; both run only through
confirmed backends (`domains/numbers/AGENTS.md`).
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
    {"ListPhoneNumbers", "RetrievePhoneNumber", "DeletePhoneNumber", "ListNumberOrders",
     "CreateNumberOrder", "RetrieveNumberOrder"}
)
CONFIRMED_ACTIONS = ("DeletePhoneNumber",)


class NumberOrderInput(BaseModel):
    """`CreateNumberOrder` request body (scalar fields; `phone_numbers` is supplied via execute)."""

    connection_id: str | None = Field(default=None, title="Connection ID")
    messaging_profile_id: str | None = Field(default=None, title="Messaging profile ID")
    billing_group_id: str | None = Field(default=None, title="Billing group ID")
    customer_reference: str | None = Field(default=None, title="Customer reference")


FORM_MODELS = {"CreateNumberOrder": NumberOrderInput}

app = FastMCPApp("oubliai-numbers")

numbers_list = register_list_backend(
    app,
    name="numbers_list",
    spec=ListSpec(
        tool="ListPhoneNumbers",
        data_path=("data",),
        columns=(
            ColumnSpec("phone_number", "Number"),
            ColumnSpec("status", "Status"),
            ColumnSpec("connection_name", "Connection"),
            ColumnSpec("country_iso_alpha2", "Country"),
        ),
    ),
)
orders_list = register_list_backend(
    app,
    name="number_orders_list",
    spec=ListSpec(tool="ListNumberOrders", data_path=("data",), columns=()),
)
numbers_get = register_detail_backend(
    app, name="numbers_get", tool="RetrievePhoneNumber", id_param="id"
)
numbers_delete = register_confirmed_backend(
    app, name="numbers_delete", tool="DeletePhoneNumber", id_param="id"
)
orders_create = register_form_backend(
    app, name="number_orders_create", tool="CreateNumberOrder", model=NumberOrderInput
)


def _delete_action() -> None:
    confirm_action(
        label="Delete number",
        title="Delete phone number",
        description="Releases the number from the account. This cannot be undone.",
        backend=numbers_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Phone numbers",
        list_backend=numbers_list,
        columns=(
            ColumnSpec("phone_number", "Number"),
            ColumnSpec("status", "Status"),
            ColumnSpec("connection_name", "Connection"),
            ColumnSpec("country_iso_alpha2", "Country"),
        ),
        detail_backend=numbers_get,
        detail_fields=(("data.id", "ID"), ("data.phone_number", "Number"), ("data.status", "Status")),
        actions=(_delete_action,),
        notes=(
            "Ordering numbers incurs cost: CreateNumberOrder requires the phone_numbers list and "
            "explicit authorization; use execute with the generated tool.",
            "Number orders are listed by ListNumberOrders; poll with await_telnyx_resource.",
        ),
    )


@app.ui("numbers_workspace", description="Open the Telnyx phone numbers workspace.")
def numbers_workspace() -> PrefabApp:
    return workspace()
