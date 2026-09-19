from pytaurix import Commands
from pytaurix.ipc import Headers

commands = Commands()


@commands.command()
async def command(body: bytes, headers: Headers) -> None:  # noqa: ARG001
    print(headers)
