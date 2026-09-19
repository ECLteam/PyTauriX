from pytaurix import Commands
from pytaurix.ipc import InvokeException

commands = Commands()


@commands.command()
async def command() -> None:
    raise InvokeException("error message")
