import json
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import Literal, cast

from anyio import create_task_group
from anyio.abc import TaskGroup
from anyio.from_thread import start_blocking_portal
from pydantic import BaseModel, ConfigDict, RootModel
from pydantic.alias_generators import to_camel
from pytaurix import (
    AppHandle,
    Commands,
    Emitter,
    Event,
    Listener,
    builder_factory,
    context_factory,
)
from pytaurix.ipc import Channel, JavaScriptChannelId
from pytaurix.plugins import cli, store, updater
from pytaurix.webview import WebviewWindow

__all__ = ["app_handle_fixture"]

commands = Commands()


ChannelBody = RootModel[Literal["ping"]]


class _BaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Body(_BaseModel):
    ping: Literal["ping"]
    channel_id: JavaScriptChannelId[ChannelBody]


Pong = RootModel[Literal["pong"]]


async def channel_task(channel: Channel[ChannelBody]) -> None:
    channel.send_model(ChannelBody("ping"))


# NOTE: dont change the command name `command`,
# it is used in the `test/ipc.rs`.
@commands.command()
async def command(
    body: Body,
    app_handle: AppHandle,  # noqa: ARG001
    webview_window: WebviewWindow,
) -> Literal["pong"]:
    assert body.ping == "ping"

    channel = body.channel_id.channel_on(webview_window.as_ref_webview())

    await channel_task(channel)

    return "pong"


task_group: TaskGroup


# NOTE: dont change the func name `app_handle_fixture`,
# it is used in the `test/ipc.rs`.
@contextmanager
def app_handle_fixture() -> Iterator[AppHandle]:
    global task_group
    with (
        start_blocking_portal("asyncio") as portal,  # or `trio`
        portal.wrap_async_context_manager(portal.call(create_task_group)) as task_group,
    ):
        app = builder_factory().build(
            context=context_factory(),
            invoke_handler=commands.generate_handler(portal),
            plugins=(cli.init(), store.init(), updater.Builder.build()),
        )
        yield app.handle()


def test_event_system():
    """Test `Emitter` and `Listener` event system."""

    event_name = "ping"
    event_payload = Pong("pong")

    with app_handle_fixture() as app_handle:
        received_event: Event | None = None

        def handler(event: Event):
            nonlocal received_event
            received_event = event

        event_id = Listener.once(app_handle, event_name, handler)
        Emitter.emit(app_handle, event_name, event_payload)

        # TODO, FIXME: this is pyright bug, it mistakenly thinks `received_event` is `None`
        received_event = cast(Event | None, received_event)

        assert received_event is not None, f"event name `{event_name}` not received"
        assert received_event.id == event_id, "received event id mismatch"
        assert (
            Pong.model_validate_json(received_event.payload).root == event_payload.root
        ), "received event payload mismatch"


test_event_system()


def test_store_api():
    with app_handle_fixture() as app_handle:
        database = store.load(app_handle, "pytaurix-test-store.json")
        database.clear()
        database.set("answer", {"value": 42})
        assert database.get("answer") == {"value": 42}
        assert database.has("answer")
        assert database.entries() == [("answer", {"value": 42})]
        assert database.delete("answer")
        assert database.get("answer") is None


test_store_api()


def test_cli_api():
    with app_handle_fixture() as app_handle:
        matches = cli.get_matches_from(app_handle, ["pytaurix-test"])
        assert isinstance(matches, dict)
        assert isinstance(matches["args"], dict)
        assert matches["subcommand"] is None


test_cli_api()


class _UpdaterHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.endswith("/no-update"):
            self.send_response(204)
            self.end_headers()
            return

        body = json.dumps(
            {
                "version": "0.2.0",
                "notes": "Test update metadata only; no artifact is downloaded.",
                "pub_date": "2026-09-19T00:00:00Z",
                "url": "https://example.invalid/pytaurix-test-update.zip",
                "signature": "not-used-without-download",
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass


def test_updater_check_api():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _UpdaterHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    endpoint = f"http://127.0.0.1:{server.server_port}/update"
    try:
        with app_handle_fixture() as app_handle:
            metadata = updater.check(app_handle, endpoints=[endpoint])
            assert metadata is not None
            assert metadata["version"] == "0.2.0"
            assert metadata["current_version"] == "0.1.0"
            assert metadata["target"]
            assert metadata["raw_json"]["notes"].startswith("Test update metadata")
            assert (
                updater.check(app_handle, endpoints=[f"{endpoint}/no-update"]) is None
            )

            try:
                updater.check(app_handle)
            except RuntimeError as error:
                assert "endpoint" in str(error).lower()  # noqa: PT017
            else:
                raise AssertionError(
                    "an updater without configured endpoints must fail"
                )

            try:
                updater.check(app_handle, endpoints=["not a URL"])
            except RuntimeError as error:
                assert "invalid updater endpoint" in str(error)  # noqa: PT017
            else:
                raise AssertionError("an invalid updater endpoint must fail")
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


test_updater_check_api()
