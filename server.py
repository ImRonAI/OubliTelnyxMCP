"""Repository-root entrypoint for hosts that look for `server.py`.

Horizon entrypoint: `server.py:create_server`. The factory lives in
`packages/server/src/oubliai_server/__main__.py`; this file only re-exports it
(install `requirements.txt` first so `oubliai_server` is importable).
"""

from oubliai_server.__main__ import create_server

__all__ = ["create_server"]
