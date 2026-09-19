"""[tauri::plugin](https://docs.rs/tauri/latest/tauri/plugin/index.html)"""

from typing import (
    TYPE_CHECKING,
    final,
)

from pytaurix.ffi._ext_mod import pytaurix_mod

__all__ = ["Plugin"]

_plugin_mod = pytaurix_mod.plugin

if TYPE_CHECKING:

    @final
    class Plugin:
        """[tauri::plugin::Plugin](https://docs.rs/tauri/latest/tauri/plugin/trait.Plugin.html)"""

else:
    Plugin = _plugin_mod.Plugin
