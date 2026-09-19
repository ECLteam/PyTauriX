"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from collections.abc import Callable
from types import ModuleType
from typing import TYPE_CHECKING

from pytaurix import AppHandle
from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_SINGLE_INSTANCE,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = [
    "init",
]

if PLUGIN_SINGLE_INSTANCE:
    _single_instance_mod: ModuleType = _pytaurix_plugins_mod.single_instance
else:
    raise ImportError(
        "Enable the `plugin-single-instance` feature for `pytaurix` crate to use this plugin."
    )


if TYPE_CHECKING:

    def init(callback: Callable[[AppHandle, list[str], str], None] | None, /) -> Plugin:
        """[tauri_plugin_single_instance::init](https://docs.rs/tauri-plugin-single-instance/latest/tauri_plugin_single_instance/fn.init.html)

        Args:
            callback: `(app_handle, args, cwd)`
        """
        ...

else:
    init = _single_instance_mod.init
