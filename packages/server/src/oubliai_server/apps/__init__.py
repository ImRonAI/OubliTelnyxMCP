"""Domain FastMCPApp providers. Mounted on the operations child before CodeMode.

`ALL_APPS` is the single import point for `server.build_operations`. App names must be
unique server-wide (fastmcp-app.md, "Composition and namespacing").
"""

from fastmcp.apps.app import FastMCPApp

from oubliai_server.apps import (
    ai,
    email,
    fax,
    meetings,
    messaging,
    numbers,
    platform,
    rag,
    speech,
    storage,
    training,
    verify,
    video,
    voice,
)

ALL_APPS: tuple[FastMCPApp, ...] = (
    numbers.app,
    messaging.app,
    fax.app,
    verify.app,
    video.app,
    meetings.app,
    email.app,
    voice.app,
    ai.app,
    rag.app,
    speech.app,
    storage.app,
    training.app,
    platform.app,
)

__all__ = ["ALL_APPS"]
