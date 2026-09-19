"""Original FFI interface for the log plugin."""

from types import ModuleType
from typing import TYPE_CHECKING, Literal

from typing_extensions import TypedDict, Unpack

from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_LOG,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = ["Builder", "BuilderArgs"]

if PLUGIN_LOG:
    _log_mod: ModuleType = _pytaurix_plugins_mod.log
else:
    raise ImportError(
        "Enable the `plugin-log` feature for `pytaurix` crate to use this plugin."
    )


class BuilderArgs(TypedDict, total=False):
    """Optional configuration accepted by :meth:`Builder.build`."""

    level: Literal["off", "error", "warn", "info", "debug", "trace"]
    targets: list[Literal["stdout", "stderr", "log_dir", "webview"]]
    file_name: str
    clear_targets: bool


if TYPE_CHECKING:

    class Builder:
        """Build the Tauri log plugin."""

        @staticmethod
        def build(**kwargs: Unpack[BuilderArgs]) -> Plugin:
            """Create a log plugin for explicit application registration."""
            ...
else:
    Builder = _log_mod.Builder
