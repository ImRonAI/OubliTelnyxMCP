import pytest

from oubliai_server.spec import load_telnyx_spec


@pytest.fixture(scope="session")
def telnyx_spec():
    return load_telnyx_spec()
