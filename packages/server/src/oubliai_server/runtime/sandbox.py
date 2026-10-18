"""Runtime environment for the Prefab Pyodide sandbox behind `generate_prefab_ui`.

GenerativeUI validates generated code in Prefab's sandbox, "a persistent Deno subprocess
running Pyodide" ("Deno must be installed on the host", prefab.prefect.io, Generative UI).
Hosted platforms that install only Python packages get Deno from its official PyPI
redistribution (`deno`, `find_deno_bin()`). Prefab finds it with `shutil.which("deno")` and
passes `os.environ` to the subprocess, so the documented Deno variables apply:
`DENO_DIR` (cache directory; must be writable, and hosted filesystems are only guaranteed
writable in temporary space) and `DENO_NO_PACKAGE_JSON` (a repository `package.json` would
otherwise take over `npm:pyodide` resolution).
"""

import os
import tempfile
from pathlib import Path


def prepare_prefab_sandbox_env() -> None:
    os.environ.setdefault("DENO_DIR", str(Path(tempfile.gettempdir()) / "deno"))
    os.environ.setdefault("DENO_NO_PACKAGE_JSON", "1")
    os.environ.setdefault("DENO_NO_UPDATE_CHECK", "1")
    try:
        from deno import find_deno_bin
    except ImportError:
        return
    try:
        deno_dir = str(Path(find_deno_bin()).parent)
    except FileNotFoundError:
        return
    path = os.environ.get("PATH", "")
    if deno_dir not in path.split(os.pathsep):
        os.environ["PATH"] = os.pathsep.join(filter(None, (deno_dir, path)))
