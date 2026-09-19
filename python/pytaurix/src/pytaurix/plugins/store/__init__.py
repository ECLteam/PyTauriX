"""Persistent key-value storage via `tauri-plugin-store`."""

from pytaurix.plugins.store.ffi import Store, init, load

__all__ = ["Store", "init", "load"]
