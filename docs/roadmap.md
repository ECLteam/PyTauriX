# PyTauriX alpha roadmap

PyTauriX is an independent Apache-2.0 fork of PyTauri. It targets Python
3.11+ and the stable desktop APIs of Tauri 2.11 on Windows, macOS, and Linux.
The first release series is internal-only (`0.1.0-alpha.N`); it is not
compatible with PyTauri 0.8 and is not published to public registries.

## API layers

- `pytaurix.raw` is the stable low-level API. It mirrors supported stable
  desktop Tauri concepts and leaves their lifecycle visible.
- `pytaurix` is the Pythonic layer. `Application` centralizes the normal
  context/builder lifecycle while retaining `Application.builder` for native
  configuration.
- `pytaurix.plugins.<name>` contains explicit plugin bindings. A plugin is
  available only when its Rust feature is enabled and it is registered with
  the app builder.

## Capability ledger

| Capability | Alpha status | Validation | Platform |
| --- | --- | --- | --- |
| App, AppHandle, context, manager, event and IPC | migrated | Rust/Python integration tests | desktop |
| Window, WebviewWindow, menus, tray, paths, images | migrated baseline; Tauri 2.11 parity review required | API inventory plus GUI smoke test | desktop |
| WebView page/load/download/new-window/resource callbacks | planned | callback and error-boundary integration tests | platform-dependent desktop |
| Size constraints and newer WebView options | planned | constructor and resize tests | desktop |
| Rust-generic extension APIs | native extension escape hatch | compile example | desktop |
| Android/iOS and Tauri `unstable` APIs | out of scope | n/a | unsupported |
| legacy plugin bindings | compile-verified on Windows; API behavior review pending | `tauri-app` desktop smoke | desktop, plugin-specific |
| updater | Python metadata check with local-protocol coverage; signature download/install unverified | signed update fixture | desktop |
| log, store, stronghold and cli plugins | initial raw bindings implemented; lifecycle and platform review remains | focused Rust/Python tests plus desktop smoke | per official support table |

Every row must move to **migrated**, **unsupported with rationale**, or
**native extension escape hatch** before an API-stable release. The ledger is
the release gate; unsupported APIs must never appear as silently incomplete
Python wrappers.

## Plugin inventory

The Windows smoke example compiles and registers the following legacy bindings:
`autostart`, `clipboard-manager`, `deep-link`, `dialog`, `fs`,
`global-shortcut`, `http`, `notification`, `opener`, `os`,
`persisted-scope`, `positioner`, `process`, `shell`, `single-instance`,
`updater`, `upload`, `websocket`, and `window-state`. Registration is not an
API compatibility claim: each plugin still needs permission-denial and
success-path tests before the alpha API is frozen.

The first infrastructure wave is deliberately ordered as follows:

| Plugin | Current state | Required acceptance test |
| --- | --- | --- |
| `updater` | Python builder and metadata check; local available/no-update/error-path coverage | signed local manifest plus download verification; installation requires a disposable platform fixture |
| `log` | Python builder; Windows registration compile verified | file target creation and Rust/Python error logging test |
| `store` | Python store operations with black-box integration coverage | scoped persistence and corrupted-file error test |
| `stronghold` | explicit Argon2 salt-path builder; encrypted vault round-trip unit coverage | desktop registration and no-secret-in-logs test |
| `cli` | Python match retrieval and explicit-argument integration coverage | configured arguments/subcommands forwarded into Python |

Only a feature plus explicit `AppBuilder.plugin(...)` registration counts as
support. JavaScript-only availability or a transitive Cargo dependency does
not.

## Updating upstream

The fork keeps `upstream` pointed at `pytauri/pytauri`. Dependency bots may
open update PRs, but a maintainer must validate all supported desktop targets
before merging a Tauri minor upgrade. Security updates use the same matrix on
an expedited path.
