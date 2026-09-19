"""Original FFI interface for the Stronghold plugin."""

from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_STRONGHOLD,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = ["Builder"]

if PLUGIN_STRONGHOLD:
    _stronghold_mod: ModuleType = _pytaurix_plugins_mod.stronghold
else:
    raise ImportError(
        "Enable the `plugin-stronghold` feature for the `pytaurix` crate to use this plugin."
    )

if TYPE_CHECKING:

    class Builder:
        """Builder for the supported Stronghold initialization mode."""

        @staticmethod
        def with_argon2(salt_path: Path, /) -> Plugin:
            """Create a plugin using an Argon2 salt file at ``salt_path``."""
            ...
else:
    Builder = _stronghold_mod.Builder
