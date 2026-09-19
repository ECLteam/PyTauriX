# DO NOT import any `pytaurix` API here,
# Otherwise, in **user** code, if `pytaurix` is imported first and then `pytaurix_wheel`,
# it will cause a circular import issue:
# `user` -> `pytaurix` -> `pytaurix_wheel.ext_mod` -> `pytaurix.__init__` -> `pytaurix` -> `pytaurix.__init__` -> ...

"""PyTauriX precompiled wheels.

Due to the limitations of circular imports, we cannot import the `pytaurix` module in `__init__.py`,
so the related APIs are placed in the [pytaurix_wheel.lib][] module.
"""
