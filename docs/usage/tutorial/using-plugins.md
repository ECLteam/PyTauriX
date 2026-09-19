# Using Tauri Plugins

The Tauri team and community have developed some [plugins](https://tauri.app/plugin/), you can use them by:

1. Official Tauri plugins usually provide corresponding JavaScript APIs, which you can use directly on the frontend.
2. Write your own Rust functions using pyo3 and expose them to Python: <https://github.com/ECLteam/PyTauriX/discussions/45#discussioncomment-11870767>

    **We encourage you to distribute plugins written in this way to benefit the entire community 💪.**

In addition, PyTauriX has already integrated some official Tauri plugins. Below, we use [tauri-plugin-notification] as an example to demonstrate how to use pytaurix-integrated plugins.

[tauri-plugin-notification]: https://github.com/tauri-apps/tauri-plugin-notification

## Plugin binding inventory

This table records bindings presently in the repository. During the alpha
phase, it is not a compatibility guarantee: only the infrastructure-wave
plugins called out in the [roadmap](../../roadmap.md) have focused API tests.
Every plugin still requires its Cargo feature and explicit Python registration.

| Plugin/Features | JS Docs | Rust Docs | Python Docs |
|:------:|:-------:|:---------:|:-----------:|
| [plugin-autostart] | [JS docs][autostart-js-docs] | [Rust docs][autostart-rs-docs] | [Python docs][pytaurix.plugins.autostart] |
| [plugin-clipboard-manager] | [JS docs][clipboard-js-docs] | [Rust docs][clipboard-rs-docs] | [Python docs][pytaurix.plugins.clipboard_manager] |
| [plugin-cli] | [JS docs][cli-js-docs] | [Rust docs][cli-rs-docs] | [Python docs][pytaurix.plugins.cli] |
| [plugin-deep-link] | [JS docs][deep-link-js-docs] | [Rust docs][deep-link-rs-docs] | [Python docs][pytaurix.plugins.deep_link] |
| [plugin-dialog] | [JS docs][dialog-js-docs] | [Rust docs][dialog-rs-docs] | [Python docs][pytaurix.plugins.dialog] |
| [plugin-fs] | [JS docs][fs-js-docs] | [Rust docs][fs-rs-docs] | [Python docs][pytaurix.plugins.fs] |
| [plugin-global-shortcut] | [JS docs][global-shortcut-js-docs] | [Rust docs][global-shortcut-rs-docs] | [Python docs][pytaurix.plugins.global_shortcut] |
| [plugin-http] | [JS docs][http-js-docs] | [Rust docs][http-rs-docs] | [Python docs][pytaurix.plugins.http] |
| [plugin-log] | [JS docs][log-js-docs] | [Rust docs][log-rs-docs] | [Python docs][pytaurix.plugins.log] |
| [plugin-notification] | [JS docs][notification-js-docs] | [Rust docs][notification-rs-docs] | [Python docs][pytaurix.plugins.notification] |
| [plugin-opener] | [JS docs][opener-js-docs] | [Rust docs][opener-rs-docs] | [Python docs][pytaurix.plugins.opener] |
| [plugin-os] | [JS docs][os-js-docs] | [Rust docs][os-rs-docs] | [Python docs][pytaurix.plugins.os] |
| [plugin-persisted-scope] | - | [Rust docs][persisted-scope-rs-docs] | [Python docs][pytaurix.plugins.persisted_scope] |
| [plugin-positioner] | [JS docs][positioner-js-docs] | [Rust docs][positioner-rs-docs] | [Python docs][pytaurix.plugins.positioner] |
| [plugin-process] | [JS docs][process-js-docs] | [Rust docs][process-rs-docs] | [Python docs][pytaurix.plugins.process] |
| [plugin-shell] | [JS docs][shell-js-docs] | [Rust docs][shell-rs-docs] | [Python docs][pytaurix.plugins.shell] |
| [plugin-single-instance] | - | [Rust docs][single-instance-rs-docs] | [Python docs][pytaurix.plugins.single_instance] |
| [plugin-store] | [JS docs][store-js-docs] | [Rust docs][store-rs-docs] | [Python docs][pytaurix.plugins.store] |
| [plugin-stronghold] | [JS docs][stronghold-js-docs] | [Rust docs][stronghold-rs-docs] | [Python docs][pytaurix.plugins.stronghold] |
| [plugin-updater] | [JS docs][updater-js-docs] | [Rust docs][updater-rs-docs] | [Python docs][pytaurix.plugins.updater] |
| [plugin-upload] | [JS docs][upload-js-docs] | [Rust docs][upload-rs-docs] | [Python docs][pytaurix.plugins.upload] |
| [plugin-websocket] | [JS docs][websocket-js-docs] | [Rust docs][websocket-rs-docs] | [Python docs][pytaurix.plugins.websocket] |
| [plugin-window-state] | [JS docs][window-state-js-docs] | [Rust docs][window-state-rs-docs] | [Python docs][pytaurix.plugins.window_state] |

[plugin-autostart]: https://tauri.app/plugin/autostart/
[autostart-js-docs]: https://tauri.app/reference/javascript/autostart/
[autostart-rs-docs]: https://docs.rs/tauri-plugin-autostart/

[plugin-clipboard-manager]: https://tauri.app/plugin/clipboard/
[clipboard-js-docs]: https://tauri.app/reference/javascript/clipboard-manager/
[clipboard-rs-docs]: https://docs.rs/tauri-plugin-clipboard-manager/

[plugin-cli]: https://tauri.app/plugin/cli/
[cli-js-docs]: https://tauri.app/reference/javascript/cli/
[cli-rs-docs]: https://docs.rs/tauri-plugin-cli/

[plugin-deep-link]: https://tauri.app/plugin/deep-linking/
[deep-link-js-docs]: https://tauri.app/reference/javascript/deep-link/
[deep-link-rs-docs]: https://docs.rs/tauri-plugin-deep-link/

[plugin-dialog]: https://tauri.app/plugin/dialog/
[dialog-js-docs]: https://tauri.app/reference/javascript/dialog/
[dialog-rs-docs]: https://docs.rs/tauri-plugin-dialog/

[plugin-fs]: https://tauri.app/plugin/file-system/
[fs-js-docs]: https://tauri.app/reference/javascript/fs/
[fs-rs-docs]: https://docs.rs/tauri-plugin-fs/

[plugin-global-shortcut]: https://tauri.app/plugin/global-shortcut/
[global-shortcut-js-docs]: https://tauri.app/reference/javascript/global-shortcut/
[global-shortcut-rs-docs]: https://docs.rs/tauri-plugin-global-shortcut/

[plugin-http]: https://tauri.app/plugin/http-client/
[http-js-docs]: https://tauri.app/reference/javascript/http/
[http-rs-docs]: https://docs.rs/tauri-plugin-http/

[plugin-log]: https://tauri.app/plugin/logging/
[log-js-docs]: https://tauri.app/reference/javascript/log/
[log-rs-docs]: https://docs.rs/tauri-plugin-log/

[plugin-notification]: https://tauri.app/plugin/notification/
[notification-js-docs]: https://tauri.app/reference/javascript/notification/
[notification-rs-docs]: https://docs.rs/tauri-plugin-notification/

[plugin-opener]: https://tauri.app/plugin/opener/
[opener-js-docs]: https://tauri.app/reference/javascript/opener/
[opener-rs-docs]: https://docs.rs/tauri-plugin-opener/

[plugin-os]: https://tauri.app/plugin/os-info/
[os-js-docs]: https://tauri.app/reference/javascript/os/
[os-rs-docs]: https://docs.rs/tauri-plugin-os/

[plugin-persisted-scope]: https://tauri.app/plugin/persisted-scope/
[persisted-scope-rs-docs]: https://docs.rs/tauri-plugin-persisted-scope/

[plugin-positioner]: https://tauri.app/plugin/positioner/
[positioner-js-docs]: https://tauri.app/reference/javascript/positioner/
[positioner-rs-docs]: https://docs.rs/tauri-plugin-positioner/

[plugin-process]: https://tauri.app/plugin/process/
[process-js-docs]: https://tauri.app/reference/javascript/process/
[process-rs-docs]: https://docs.rs/tauri-plugin-process/

[plugin-shell]: https://tauri.app/plugin/shell/
[shell-js-docs]: https://tauri.app/reference/javascript/shell/
[shell-rs-docs]: https://docs.rs/tauri-plugin-shell/

[plugin-single-instance]: https://tauri.app/plugin/single-instance/
[single-instance-rs-docs]: https://docs.rs/tauri-plugin-single-instance/

[plugin-store]: https://tauri.app/plugin/store/
[store-js-docs]: https://tauri.app/reference/javascript/store/
[store-rs-docs]: https://docs.rs/tauri-plugin-store/

[plugin-stronghold]: https://tauri.app/plugin/stronghold/
[stronghold-js-docs]: https://tauri.app/reference/javascript/stronghold/
[stronghold-rs-docs]: https://docs.rs/tauri-plugin-stronghold/

[plugin-updater]: https://tauri.app/plugin/updater/
[updater-js-docs]: https://tauri.app/reference/javascript/updater/
[updater-rs-docs]: https://docs.rs/tauri-plugin-updater/

[plugin-upload]: https://tauri.app/plugin/upload/
[upload-js-docs]: https://tauri.app/reference/javascript/upload/
[upload-rs-docs]: https://docs.rs/tauri-plugin-upload/

[plugin-websocket]: https://tauri.app/plugin/websocket/
[websocket-js-docs]: https://tauri.app/reference/javascript/websocket/
[websocket-rs-docs]: https://docs.rs/tauri-plugin-websocket/

[plugin-window-state]: https://tauri.app/plugin/window-state/
[window-state-js-docs]: https://tauri.app/reference/javascript/window-state/
[window-state-rs-docs]: https://docs.rs/tauri-plugin-window-state/

## Using the plugin

### Install tauri plugin

All PyTauriX plugins are just Python bindings, which means you need to [initialize the underlying Tauri extensions normally](https://github.com/tauri-apps/tauri-plugin-notification/blob/665d8f08bcf2e8af3c0f95af12ca1f06d71a0d6d/README.md#install):

```bash
pnpm tauri add notification
```

The above command will perform the following steps (which you can also do manually):

- Add `tauri-plugin-notification` as a Rust dependency in `Cargo.toml`.
- Add `@tauri-apps/plugin-notification` as a frontend dependency in `package.json`

    ??? tip "This step is optional"
        If you only use the global API (`window.__TAURI__.notification`) on the frontend, you can skip this step.

- Register the core plugin with tauri

    ```rust  title="src-tauri/src/lib.rs"
    // i.e., `builder_factory` function of python binding
    |_args, _kwargs| {
        let builder = tauri::Builder::default()
            .plugin(tauri_plugin_notification::init());  // 👈
        Ok(builder)
    },
    ```

    ???+ tip "registering plugin from python"
        In PyTauriX alpha, plugins are registered directly from Python:

        ```python title="src-tauri/python/tauri_app/__init__.py"
        --8<-- "docs/snippets/tutorial/using_plugins/registering.py"
        ```

        This depends on your preference, but for [pytaurix_wheel][], plugins can only be registered in this way (since you don't have access to the Rust code).

- Add the [permissions](https://tauri.app/security/capabilities/) to your capabilities file

    ```json title="src-tauri/capabilities/default.json"
    {
        // ...
        "permissions": [
            // ...
            "notification:default"
        ],
    }
    ```

### Expose the pyo3 bindings to python

Enable the `pytaurix` feature:

```diff title="src-tauri/Cargo.toml"
[dependencies]
# ...
-pytaurix = { version = "*" }
+pytaurix = { version = "*", features = ["plugin-notification"] }
```

### Use plugin API from python

The PyTauriX API maps very well to the original Rust API of the plugin. You can refer to the [plugin-notification], [Js docs][notification-js-docs], [Rust docs][notification-rs-docs] and [Python docs][pytaurix.plugins.notification] to understand how to use it:

!!! tip
    `pytaurix.plugins` is bundled with the `pytaurix` distribution. Alpha
    builds are distributed only through GitHub Release artifacts or the
    internal package index; they are not published to PyPI.

```python title="src-tauri/python/tauri_app/__init__.py"
--8<-- "docs/snippets/tutorial/using_plugins/plugin.py"
```
