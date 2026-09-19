# ruff: noqa: D102

"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from types import ModuleType
from typing import TYPE_CHECKING, Any, TypedDict

from typing_extensions import Unpack

from pytaurix import ImplManager
from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_UPDATER,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = [
    "Builder",
    "BuilderArgs",
    "UpdateMetadata",
    "check",
]

if PLUGIN_UPDATER:
    _updater_mod: ModuleType = _pytaurix_plugins_mod.updater
else:
    raise ImportError(
        "Enable the `plugin-updater` feature for `pytaurix` crate to use this plugin."
    )


class BuilderArgs(TypedDict, total=False):
    """[tauri_plugin_updater::Builder](https://docs.rs/tauri-plugin-updater/latest/tauri_plugin_updater/struct.Builder.html)"""


class UpdateMetadata(TypedDict):
    """Metadata for an available update, without downloading its artifact."""

    body: str | None
    current_version: str
    version: str
    date: str | None
    target: str
    download_url: str
    signature: str
    raw_json: Any


if TYPE_CHECKING:

    class Builder:
        """[tauri_plugin_updater::Builder](https://docs.rs/tauri-plugin-updater/latest/tauri_plugin_updater/struct.Builder.html)"""

        @staticmethod
        def build(**kwargs: Unpack[BuilderArgs]) -> Plugin: ...

    def check(
        manager: ImplManager,
        /,
        *,
        endpoints: list[str] | None = None,
    ) -> UpdateMetadata | None:
        """Check endpoints and return available update metadata without downloading."""
        ...

else:
    Builder = _updater_mod.Builder
    check = _updater_mod.check
