"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from types import ModuleType
from typing import TYPE_CHECKING

from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_SHELL,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = [
    "init",
]

if PLUGIN_SHELL:
    _shell_mod: ModuleType = _pytaurix_plugins_mod.shell
else:
    raise ImportError(
        "Enable the `plugin-shell` feature for `pytaurix` crate to use this plugin."
    )


if TYPE_CHECKING:

    def init() -> Plugin:
        """[tauri_plugin_shell::init](https://docs.rs/tauri-plugin-shell/latest/tauri_plugin_shell/fn.init.html)"""
        ...

else:
    init = _shell_mod.init
