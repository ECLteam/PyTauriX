from time import sleep
from typing import Annotated

from pytaurix import Commands, State
from pytaurix_utils.async_tools import AsyncTools

commands = Commands()


@commands.command()
async def command_handler(async_tools: Annotated[AsyncTools, State()]) -> None:
    # ⭐ Convert a synchronous blocking function to an asynchronous one
    @async_tools.to_async
    def some_blocking_task(secs: int) -> None:
        print("Running a blocking task...")
        sleep(secs)

    # ⭐ Run blocking task in a separate worker thread
    await some_blocking_task(1)
