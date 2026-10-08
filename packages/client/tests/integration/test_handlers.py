from pathlib import Path

import mcp_types
import pytest
from fastmcp import Client, Context, FastMCP

from oubliai_client.handlers import (
    LogRecorder,
    NotificationRecorder,
    ProgressEvent,
    ProgressRecorder,
    cancel,
    decline,
    elicitation_handler,
    roots,
    sampling_handler,
)


def elicitation_request(message: str) -> mcp_types.InputRequiredResult:
    return mcp_types.InputRequiredResult(
        result_type="input_required",
        input_requests={
            "answer": mcp_types.ElicitRequest(
                method="elicitation/create",
                params=mcp_types.ElicitRequestFormParams(
                    message=message,
                    requested_schema={
                        "type": "object",
                        "properties": {"value": {"type": "string"}},
                        "required": ["value"],
                    },
                ),
            )
        },
    )


async def test_recorders_capture_real_server_events() -> None:
    server = FastMCP("handler-events")
    progress = ProgressRecorder()
    logs = LogRecorder()
    notifications = NotificationRecorder()

    @server.tool
    async def emit_events(ctx: Context) -> str:
        await ctx.report_progress(1, 2, "halfway")
        await ctx.info("ready", logger_name="fixture")
        await ctx.send_notification(mcp_types.ToolListChangedNotification())
        return "done"

    client = Client(
        server,
        log_handler=logs,
        message_handler=notifications,
        progress_handler=progress,
    )
    async with client:
        result = await client.call_tool("emit_events", {})

    assert result.data == "done"
    assert progress.events == [ProgressEvent(1, 2, "halfway")]
    assert [(message.level, message.logger, message.data) for message in logs.messages] == [
        ("info", "fixture", {"msg": "ready", "extra": None})
    ]
    assert any(
        isinstance(notification, mcp_types.ToolListChangedNotification)
        for notification in notifications.notifications
    )


async def test_elicitation_helpers_drive_modern_input_rounds() -> None:
    server = FastMCP("handler-elicitation")

    @server.tool
    async def ask(ctx: Context) -> str | mcp_types.InputRequiredResult:
        if ctx.input_responses is None:
            return elicitation_request("Answer?")
        response = ctx.input_responses["answer"]
        if response.action != "accept" or response.content is None:
            return response.action
        return response.content["value"]

    async with Client(
        server, mode="auto", elicitation_handler=elicitation_handler("yes")
    ) as client:
        assert client.protocol_version == "2026-07-28"
        accepted = await client.call_tool("ask", {})
    assert accepted.data == "yes"

    async with Client(server, mode="auto", elicitation_handler=decline) as client:
        declined = await client.call_tool("ask", {})
    assert declined.data == "decline"

    async with Client(server, mode="auto", elicitation_handler=cancel) as client:
        cancelled = await client.call_tool("ask", {})
    assert cancelled.data == "cancel"


async def test_sampling_and_roots_helpers_drive_modern_input_rounds(
    tmp_path: Path,
) -> None:
    server = FastMCP("handler-inputs")
    root_uris = roots(path for path in (tmp_path, tmp_path / "nested"))

    @server.tool
    async def request_inputs(ctx: Context) -> str | mcp_types.InputRequiredResult:
        if ctx.input_responses is None:
            return mcp_types.InputRequiredResult(
                result_type="input_required",
                input_requests={
                    "sample": mcp_types.CreateMessageRequest(
                        method="sampling/createMessage",
                        params=mcp_types.CreateMessageRequestParams(
                            messages=[
                                mcp_types.SamplingMessage(
                                    role="user",
                                    content=mcp_types.TextContent(
                                        type="text", text="Say hi"
                                    ),
                                )
                            ],
                            max_tokens=10,
                        ),
                    ),
                    "roots": mcp_types.ListRootsRequest(method="roots/list"),
                },
            )

        sampled = ctx.input_responses["sample"]
        listed = ctx.input_responses["roots"]
        assert isinstance(sampled, mcp_types.CreateMessageResult)
        assert isinstance(sampled.content, mcp_types.TextContent)
        assert isinstance(listed, mcp_types.ListRootsResult)
        return f"{sampled.content.text}|{','.join(str(root.uri) for root in listed.roots)}"

    async with Client(
        server,
        mode="auto",
        sampling_handler=sampling_handler("hi"),
        roots=root_uris,
    ) as client:
        result = await client.call_tool("request_inputs", {})

    assert result.data == f"hi|{','.join(root_uris)}"


async def test_adjacent_resource_prompt_and_completion_round_trip() -> None:
    server = FastMCP("handler-adjacent")

    @server.resource("echo://{value}")
    def echo(value: str) -> str:
        return value

    @server.prompt
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    @server.completion
    def complete(ref, argument, context):
        if isinstance(ref, mcp_types.PromptReference) and argument.name == "name":
            return [name for name in ("Ada", "Alan") if name.startswith(argument.value)]
        return None

    async with Client(server) as client:
        resource = await client.read_resource("echo://value")
        prompt = await client.get_prompt("greet", {"name": "Ada"})
        completion = await client.complete(
            mcp_types.PromptReference(type="ref/prompt", name="greet"),
            {"name": "name", "value": "A"},
        )

    assert resource[0].text == "value"
    assert prompt.messages[0].content.text == "Hello, Ada!"
    assert completion.values == ["Ada", "Alan"]
