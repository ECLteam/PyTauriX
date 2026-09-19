"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from types import ModuleType
from typing import TYPE_CHECKING

from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_FS,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = [
    "init",
]

if PLUGIN_FS:
    _fs_mod: ModuleType = _pytaurix_plugins_mod.fs
else:
    raise ImportError(
        "Enable the `plugin-fs` feature for `pytaurix` crate to use this plugin."
    )


if TYPE_CHECKING:

    def init() -> Plugin:
        """[tauri_plugin_fs::init](https://docs.rs/tauri-plugin-fs/latest/tauri_plugin_fs/fn.init.html)"""
        ...

else:
    init = _fs_mod.init
