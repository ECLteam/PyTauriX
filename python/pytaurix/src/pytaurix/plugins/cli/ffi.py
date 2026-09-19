"""Original FFI interface for the CLI plugin."""

from types import ModuleType
from typing import TYPE_CHECKING, Any, TypedDict

from pytaurix import ImplManager
from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_CLI,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = [
    "ArgData",
    "Matches",
    "SubcommandMatches",
    "get_matches",
    "get_matches_from",
    "init",
]

if not PLUGIN_CLI:
    raise ImportError(
        "Enable the `plugin-cli` feature for the `pytaurix` crate to use this plugin."
    )

_cli_mod: ModuleType = _pytaurix_plugins_mod.cli


class ArgData(TypedDict):
    """The value and number of occurrences for one CLI argument."""

    value: Any
    occurrences: int


class SubcommandMatches(TypedDict):
    """The matched subcommand and its recursively encoded matches."""

    name: str
    matches: "Matches"


class Matches(TypedDict):
    """Tauri CLI match data, mirroring ``tauri_plugin_cli::Matches``."""

    args: dict[str, ArgData]
    subcommand: SubcommandMatches | None


if TYPE_CHECKING:

    def init() -> Plugin:
        """Create the Tauri CLI plugin for ``AppBuilder.plugin``."""
        ...

    def get_matches(manager: ImplManager, /) -> Matches:
        """Return matches for the process command-line arguments."""
        ...

    def get_matches_from(manager: ImplManager, args: list[str], /) -> Matches:
        """Return matches after parsing the supplied argument vector."""
        ...
else:
    init = _cli_mod.init
    get_matches = _cli_mod.get_matches
    get_matches_from = _cli_mod.get_matches_from
