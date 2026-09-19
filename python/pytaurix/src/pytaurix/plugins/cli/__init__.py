"""Tauri command-line argument parsing."""

from pytaurix.plugins.cli.ffi import (
    ArgData,
    Matches,
    SubcommandMatches,
    get_matches,
    get_matches_from,
    init,
)

__all__ = [
    "ArgData",
    "Matches",
    "SubcommandMatches",
    "get_matches",
    "get_matches_from",
    "init",
]
