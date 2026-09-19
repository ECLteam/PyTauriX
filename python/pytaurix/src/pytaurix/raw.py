"""Stable, close-to-Tauri desktop bindings.

``pytaurix.raw`` is the low-level API surface of PyTauriX. Names, argument
ordering, and lifecycle semantics intentionally follow the corresponding
stable Tauri 2 desktop APIs. Higher-level conveniences live at the package
root and must not remove access to this module.
"""

# ``raw`` deliberately exposes the complete extension surface as its stable
# low-level escape hatch. The extension module has no static export manifest.
from pytaurix.ffi import *  # noqa: F403  # pyright: ignore[reportWildcardImportFromLibrary]
