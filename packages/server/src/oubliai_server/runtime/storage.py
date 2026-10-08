"""Persistent, encrypted storage for FastMCP `OAuthProxy` state.

`OAuthProxy.client_storage` holds client registrations and the users' upstream Telnyx
tokens (collections `mcp-upstream-tokens`, `mcp-oauth-proxy-clients`, ...). FastMCP's
storage guide (`docs/reference/fastmcp/pages/storage-backends.md`, "Server-Side OAuth
Token Storage") requires explicit keys and `FernetEncryptionWrapper` around any custom
store, so every backend chosen here is wrapped before it is handed to `build_auth`.

Backends are the documented py-key-value-aio stores:
- unset `OUBLIAI_STORAGE_URL` -> `FileTreeStore` under `<fastmcp.settings.home>/oubliai-storage`
- `memory://`                 -> `MemoryStore` (tests, throwaway)
- `file://<path>`             -> `FileTreeStore` at `<path>`
- `redis://` / `rediss://`    -> `RedisStore` (multi-replica; acceptance gate: no Redis here)

A Redis-backed Docket (`FASTMCP_DOCKET_URL`) additionally needs
`FASTMCP_TASKS_ENCRYPTION_KEY` for task snapshots (tasks.md, "Credentials at Rest").
"""

import os
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import urlparse

import fastmcp
from cryptography.fernet import Fernet
from key_value.aio.protocols import AsyncKeyValue
from key_value.aio.stores.filetree import (
    FileTreeStore,
    FileTreeV1CollectionSanitizationStrategy,
    FileTreeV1KeySanitizationStrategy,
)
from key_value.aio.stores.memory import MemoryStore
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

ENCRYPTION_KEY_ENV = "OUBLIAI_STORAGE_ENCRYPTION_KEY"
STORAGE_URL_ENV = "OUBLIAI_STORAGE_URL"
DEFAULT_DIRECTORY_NAME = "oubliai-storage"
_SCHEMES = "memory://, file://<path>, redis://..., rediss://..."


def _fernet(env: Mapping[str, str]) -> Fernet:
    key = env.get(ENCRYPTION_KEY_ENV)
    if not key:
        raise SystemExit(
            f"Set {ENCRYPTION_KEY_ENV} to a Fernet key "
            "(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')."
        )
    try:
        return Fernet(key)
    except ValueError as error:
        raise SystemExit(f"{ENCRYPTION_KEY_ENV} is not a valid Fernet key: {error}") from error


def _filetree(directory: Path) -> FileTreeStore:
    """FileTreeStore with the V1 sanitizers the storage guide marks as required."""
    directory.mkdir(parents=True, exist_ok=True)  # the V1 strategies probe the filesystem
    return FileTreeStore(
        data_directory=directory,
        key_sanitization_strategy=FileTreeV1KeySanitizationStrategy(directory),
        collection_sanitization_strategy=FileTreeV1CollectionSanitizationStrategy(directory),
    )


def _backend(url: str | None) -> AsyncKeyValue:
    if not url:
        return _filetree(Path(fastmcp.settings.home) / DEFAULT_DIRECTORY_NAME)
    parsed = urlparse(url)
    if parsed.scheme == "memory":
        return MemoryStore()
    if parsed.scheme == "file":
        return _filetree(Path(parsed.netloc + parsed.path))
    if parsed.scheme in {"redis", "rediss"}:
        return RedisStore(url=url)
    raise SystemExit(f"{STORAGE_URL_ENV}={url!r} is not supported; use one of {_SCHEMES}")


def build_client_storage(env: Mapping[str, str] | None = None) -> FernetEncryptionWrapper:
    """Encrypted `client_storage` for `OAuthProxy`, selected from the environment."""
    source = os.environ if env is None else env
    fernet = _fernet(source)
    return FernetEncryptionWrapper(key_value=_backend(source.get(STORAGE_URL_ENV)), fernet=fernet)
