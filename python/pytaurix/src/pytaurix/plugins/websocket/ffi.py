"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from types import ModuleType
from typing import TYPE_CHECKING

from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_WEBSOCKET,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = [
    "init",
]

if PLUGIN_WEBSOCKET:
    _websocket_mod: ModuleType = _pytaurix_plugins_mod.websocket
else:
    raise ImportError(
        "Enable the `plugin-websocket` feature for `pytaurix` crate to use this plugin."
    )


if TYPE_CHECKING:

    def init() -> Plugin:
        """[tauri_plugin_websocket::init](https://docs.rs/tauri-plugin-websocket/latest/tauri_plugin_websocket/fn.init.html)"""
        ...

else:
    init = _websocket_mod.init
