"""`build_client_storage`: FastMCP-documented storage backends, always Fernet-encrypted."""

import fastmcp
import pytest
from cryptography.fernet import Fernet
from key_value.aio.errors import DecryptionError
from key_value.aio.stores.filetree import FileTreeStore
from key_value.aio.stores.memory import MemoryStore
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

from oubliai_server.runtime.storage import ENCRYPTION_KEY_ENV, STORAGE_URL_ENV, build_client_storage


@pytest.fixture
def key() -> str:
    return Fernet.generate_key().decode()


def test_default_is_encrypted_filetree_under_fastmcp_home(key, tmp_path, monkeypatch):
    monkeypatch.setattr(fastmcp.settings, "home", tmp_path)
    store = build_client_storage({ENCRYPTION_KEY_ENV: key})
    assert isinstance(store, FernetEncryptionWrapper)
    inner = store.key_value
    assert isinstance(inner, FileTreeStore)
    assert str(tmp_path / "oubliai-storage") in str(inner._data_directory)


async def test_memory_backend_is_encrypted_at_rest(key):
    store = build_client_storage({ENCRYPTION_KEY_ENV: key, STORAGE_URL_ENV: "memory://"})
    assert isinstance(store.key_value, MemoryStore)
    await store.put("k", {"a": 1}, collection="c")
    assert await store.get("k", collection="c") == {"a": 1}
    raw = await store.key_value.get("k", collection="c")
    assert raw is not None and raw != {"a": 1}


async def test_file_backend_persists_and_refuses_wrong_key(key, tmp_path):
    env = {ENCRYPTION_KEY_ENV: key, STORAGE_URL_ENV: f"file://{tmp_path}"}
    first = build_client_storage(env)
    assert isinstance(first.key_value, FileTreeStore)
    await first.put("k", {"a": 1}, collection="c")
    second = build_client_storage(env)
    assert await second.get("k", collection="c") == {"a": 1}
    other = build_client_storage({**env, ENCRYPTION_KEY_ENV: Fernet.generate_key().decode()})
    with pytest.raises(DecryptionError):
        await other.get("k", collection="c")


def test_redis_backend_is_constructed_without_connecting(key):
    store = build_client_storage(
        {ENCRYPTION_KEY_ENV: key, STORAGE_URL_ENV: "redis://localhost:6379/0"}
    )
    assert isinstance(store.key_value, RedisStore)


def test_missing_key_and_unknown_scheme_fail_fast(key):
    with pytest.raises(SystemExit, match=ENCRYPTION_KEY_ENV):
        build_client_storage({})
    with pytest.raises(SystemExit, match="memory://"):
        build_client_storage({ENCRYPTION_KEY_ENV: key, STORAGE_URL_ENV: "s3://bucket"})
