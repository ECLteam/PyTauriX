from datetime import datetime
from typing import Annotated

from anyio import sleep
from pydantic import RootModel
from pytaurix import AppHandle, Commands, Emitter, State
from pytaurix_utils.async_tools import AsyncTools

commands = Commands()


DatetimeModel = RootModel[datetime]


async def task_in_background(app_handle: AppHandle) -> None:
    while True:
        Emitter.emit(app_handle, "foo-event", DatetimeModel(datetime.now()))
        await sleep(1)


@commands.command()
async def command_handler(
    app_handle: AppHandle, async_tools: Annotated[AsyncTools, State()]
) -> None:
    # ⭐ Run a task in the background
    async_tools.task_group.start_soon(task_in_background, app_handle)
