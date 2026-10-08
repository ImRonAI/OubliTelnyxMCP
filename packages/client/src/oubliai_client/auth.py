from pathlib import Path

from fastmcp.client.auth import BearerAuth, OAuth
from key_value.aio.protocols import AsyncKeyValue
from key_value.aio.stores.filetree import (
    FileTreeStore,
    FileTreeV1CollectionSanitizationStrategy,
    FileTreeV1KeySanitizationStrategy,
)


def bearer(token: str) -> BearerAuth:
    return BearerAuth(token)


def oauth(
    *,
    scopes: str | list[str] | None = None,
    token_storage: AsyncKeyValue | None = None,
) -> OAuth:
    return OAuth(scopes=scopes, token_storage=token_storage)


def file_token_storage(directory: str | Path) -> FileTreeStore:
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return FileTreeStore(
        data_directory=path,
        key_sanitization_strategy=FileTreeV1KeySanitizationStrategy(path),
        collection_sanitization_strategy=FileTreeV1CollectionSanitizationStrategy(
            path
        ),
    )
