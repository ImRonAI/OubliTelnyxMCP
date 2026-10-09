"""Repository-root entrypoint for hosts that look for `server.py`.

Horizon entrypoint: `server.py:create_server`. The factory lives in
`packages/server/src/oubliai_server/__main__.py`; this file only makes that
source tree importable and re-exports the factory. Dependencies come from the
root `requirements.txt` (same pins as `packages/server/pyproject.toml`).
"""

import sys
from pathlib import Path

_SERVER_SRC = Path(__file__).resolve().parent / "packages" / "server" / "src"
if str(_SERVER_SRC) not in sys.path:
    sys.path.insert(0, str(_SERVER_SRC))

from oubliai_server.__main__ import create_server  # noqa: E402

__all__ = ["create_server"]
