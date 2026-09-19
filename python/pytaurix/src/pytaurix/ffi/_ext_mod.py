import sys
from importlib.metadata import (
    EntryPoint,
    distribution,
    entry_points,  # pyright: ignore[reportUnknownVariableType]
)
from os import getenv
from types import ModuleType
from typing import TYPE_CHECKING

__all__ = ["EXT_MOD", "pytaurix_mod"]

_SPECIFIC_DIST = getenv("_PYTAURIX_DIST")
"""specify the package distribution name of a pytaurix app to load the extension module."""


def _load_ext_mod() -> ModuleType:
    # See: `crates/pytaurix/src/_post_init_pyi.py`.
    if getattr(sys, "_pytaurix_standalone", False):
        return sys.modules["__pytaurix_ext_mod__"]

    group = "pytaurix"
    name = "ext_mod"
    eps = (
        entry_points(group=group, name=name)
        if not _SPECIFIC_DIST
        else distribution(_SPECIFIC_DIST).entry_points.select(group=group, name=name)  # pyright: ignore[reportUnknownMemberType]
    )
    eps = tuple[EntryPoint, ...](eps)

    if len(eps) == 0:
        raise RuntimeError("No `pytaurix` entry point is found")
    elif len(eps) > 1:
        msg_list: list[tuple[str, str]] = []
        for ep in eps:
            # See: <https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata>
            # for more attributes of `dist`.
            name = ep.dist.name if ep.dist else "UNKNOWN"
            msg_list.append((name, repr(ep)))

        prefix = "\n    - "
        msg = prefix.join(f"{name}: {ep}" for name, ep in msg_list)
        raise RuntimeError(
            f"Exactly one `pytaurix` entry point is expected, but got:{prefix}{msg}"
        )

    ext_mod = eps[0].load()
    assert isinstance(ext_mod, ModuleType)

    return ext_mod


def _load_pytaurix_mod(ext_mod: ModuleType) -> ModuleType:
    try:
        pytaurix_mod = ext_mod.pytaurix
    except AttributeError as e:
        raise RuntimeError(
            "submodule `pytaurix` is not found in the extension module"
        ) from e

    assert isinstance(pytaurix_mod, ModuleType)
    return pytaurix_mod


if TYPE_CHECKING:
    EXT_MOD: ModuleType
    """The extension module of `pytaurix` app.

    It will be loaded from `entry_points(group="pytaurix", name="ext_mod")`.

    Usually you don't need to use it, unless you want to write plugins for `pytaurix`.
    """
    pytaurix_mod: ModuleType
    """The python module of `pytaurix`.

    Equivalent to `EXT_MOD.pytaurix`.
    """

else:
    EXT_MOD = _load_ext_mod()
    pytaurix_mod = _load_pytaurix_mod(EXT_MOD)
