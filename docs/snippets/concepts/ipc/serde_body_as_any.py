# pyright: reportRedeclaration=none
# ruff: noqa: F811

from datetime import datetime

from pydantic import RootModel
from pytaurix import AppHandle, Commands

commands = Commands()

StrModel = RootModel[str]


# ⭐ OK
@commands.command()
async def command(body: datetime, app_handle: AppHandle) -> None: ...


# ⭐ OK
@commands.command()
async def command(body: str | int) -> bytes: ...


# ⭐ OK
@commands.command()
async def command(body: str | None) -> StrModel: ...


# ⭐ OK
@commands.command()
async def command() -> bool: ...
