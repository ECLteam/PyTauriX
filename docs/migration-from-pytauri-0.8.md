# Migrating from PyTauri 0.8

PyTauriX is a clean-break fork. Do not mix `pytauri` and `pytaurix` packages
in the same application, and do not expect a compatibility shim.

| PyTauri 0.8 | PyTauriX alpha |
| --- | --- |
| `import pytauri` | `import pytaurix` |
| `pytauri.ffi` | `pytaurix.raw` for the supported low-level contract |
| `pytauri_plugins.<name>` | `pytaurix.plugins.<name>` |
| `tauri-plugin-pytauri-api` | `@pytaurix/api` |
| ad-hoc `builder_factory().build(...)` | still supported, or use `Application.create().build(...)` |

The new package requires Python 3.11+. Start by replacing imports, then run
the type checker and revalidate application lifecycle and plugin registration.
The alpha release intentionally has no compatibility namespace for the old
`pytauri` module, so an incomplete migration fails early.
