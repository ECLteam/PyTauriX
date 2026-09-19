"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from types import ModuleType
from typing import TYPE_CHECKING

from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_UPLOAD,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = [
    "init",
]

if PLUGIN_UPLOAD:
    _upload_mod: ModuleType = _pytaurix_plugins_mod.upload
else:
    raise ImportError(
        "Enable the `plugin-upload` feature for `pytaurix` crate to use this plugin."
    )


if TYPE_CHECKING:

    def init() -> Plugin:
        """[tauri_plugin_upload::init](https://docs.rs/tauri-plugin-upload/latest/tauri_plugin_upload/fn.init.html)"""
        ...

else:
    init = _upload_mod.init
