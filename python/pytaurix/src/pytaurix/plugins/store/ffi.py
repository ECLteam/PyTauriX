"""Original FFI interface for the store plugin."""

from types import ModuleType
from typing import TYPE_CHECKING, Any

from pytaurix import ImplManager
from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_STORE,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)

__all__ = ["Store", "init", "load"]

if PLUGIN_STORE:
    _store_mod: ModuleType = _pytaurix_plugins_mod.store
else:
    raise ImportError(
        "Enable the `plugin-store` feature for `pytaurix` crate to use this plugin."
    )

if TYPE_CHECKING:

    def init() -> Plugin:
        """Create the store plugin for explicit application registration."""
        ...

    def load(manager: ImplManager, path: str, /) -> "Store":
        """Load a JSON store relative to the application data directory."""
        ...

    class Store:
        """A persisted JSON key-value store."""

        def get(self, key: str, /) -> Any | None:
            """Return the value for ``key``, or ``None`` when absent."""
            ...

        def set(self, key: str, value: Any, /) -> None:
            """Set ``key`` to a JSON-serializable value."""
            ...

        def has(self, key: str, /) -> bool:
            """Return whether ``key`` exists."""
            ...

        def delete(self, key: str, /) -> bool:
            """Delete ``key`` and return whether it existed."""
            ...

        def clear(self, /) -> None:
            """Remove every key from the in-memory store."""
            ...

        def keys(self, /) -> list[str]:
            """Return all keys in insertion order."""
            ...

        def entries(self, /) -> list[tuple[str, Any]]:
            """Return every key-value pair."""
            ...

        def save(self, /) -> None:
            """Persist the in-memory store to disk."""
            ...

        def reload(self, /) -> None:
            """Reload persisted data and configured defaults."""
            ...

        def reload_ignore_defaults(self, /) -> None:
            """Reload persisted data without applying configured defaults."""
            ...
else:
    init = _store_mod.init
    load = _store_mod.load
    Store = _store_mod.Store
