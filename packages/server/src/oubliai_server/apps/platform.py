"""Platform workspace: addresses, with balance and billing groups alongside (schema: /addresses, /balance, /billing_groups).

Every remaining account operation stays reachable through the generated catalog; the
common form does not authorize otherwise denied operations (`domains/platform/AGENTS.md`).
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
    {"FindAddresses", "GetAddress", "CreateAddress", "DeleteAddress", "GetUserBalance",
     "ListBillingGroups", "CreateBillingGroup"}
)
CONFIRMED_ACTIONS = ("DeleteAddress",)


class AddressInput(BaseModel):
    """`CreateAddress` scalar fields (required ones first)."""

    first_name: str = Field(title="First name")
    last_name: str = Field(title="Last name")
    business_name: str = Field(title="Business name")
    street_address: str = Field(title="Street address")
    locality: str = Field(title="City / locality")
    country_code: str = Field(title="Country code (ISO 3166-1 alpha-2)")
    administrative_area: str | None = Field(default=None, title="State / region")
    postal_code: str | None = Field(default=None, title="Postal code")
    phone_number: str | None = Field(default=None, title="Phone number")
    customer_reference: str | None = Field(default=None, title="Customer reference")


FORM_MODELS = {"CreateAddress": AddressInput}
COLUMNS = (
    ColumnSpec("business_name", "Business"),
    ColumnSpec("street_address", "Street"),
    ColumnSpec("locality", "City"),
    ColumnSpec("country_code", "Country"),
)

app = FastMCPApp("oubliai-platform")

addresses_list = register_list_backend(
    app, name="addresses_list", spec=ListSpec(tool="FindAddresses", data_path=("data",), columns=COLUMNS)
)
addresses_get = register_detail_backend(app, name="addresses_get", tool="GetAddress", id_param="id")
addresses_create = register_form_backend(
    app, name="addresses_create", tool="CreateAddress", model=AddressInput
)
addresses_delete = register_confirmed_backend(
    app, name="addresses_delete", tool="DeleteAddress", id_param="id"
)
balance_get = register_list_backend(
    app,
    name="balance_get",
    spec=ListSpec(tool="GetUserBalance", data_path=("data",), columns=(), paging="none"),
)
billing_groups_list = register_list_backend(
    app,
    name="billing_groups_list",
    spec=ListSpec(tool="ListBillingGroups", data_path=("data",), columns=()),
)


def _delete_action() -> None:
    confirm_action(
        label="Delete address",
        title="Delete address",
        description="Addresses attached to numbers or emergency services cannot be deleted.",
        backend=addresses_delete,
        resource_id_rx=STATE.selected.data.id,
    )


def workspace() -> PrefabApp:
    return list_workspace(
        title="Addresses",
        list_backend=addresses_list,
        columns=COLUMNS,
        detail_backend=addresses_get,
        detail_fields=(("data.id", "ID"), ("data.business_name", "Business"), ("data.street_address", "Street")),
        create_form=(AddressInput, addresses_create),
        actions=(_delete_action,),
        notes=(
            "Balance: GetUserBalance. Billing groups: ListBillingGroups, CreateBillingGroup.",
            "Every other account, networking and registration operation is reachable through search/execute.",
        ),
    )


@app.ui("platform_workspace", description="Open the Telnyx account & platform workspace.")
def platform_workspace() -> PrefabApp:
    return workspace()
