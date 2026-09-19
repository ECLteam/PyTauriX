from pydantic import RootModel
from pytaurix import Commands
from pytaurix.ipc import Channel, JavaScriptChannelId
from pytaurix.webview import WebviewWindow

commands = Commands()

Msg = RootModel[str]


@commands.command()
async def command(
    body: JavaScriptChannelId[Msg], webview_window: WebviewWindow
) -> None:
    channel: Channel[Msg] = body.channel_on(webview_window.as_ref_webview())

    # 👇 you should do this as background task, here just keep it simple as a example
    channel.send_model(Msg("message"))
