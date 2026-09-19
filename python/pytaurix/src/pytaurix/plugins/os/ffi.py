"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from types import ModuleType
from typing import TYPE_CHECKING

from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_OS,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = ["init"]

if PLUGIN_OS:
    _os_mod: ModuleType = _pytaurix_plugins_mod.os
else:
    raise ImportError(
        "Enable the `plugin-os` feature for `pytaurix` crate to use this plugin."
    )


if TYPE_CHECKING:

    def init() -> Plugin:
        """[tauri_plugin_os::init](https://docs.rs/tauri-plugin-os/latest/tauri_plugin_os/fn.init.html)"""
        ...

else:
    init = _os_mod.init
