<!-- 英文说明由 docs/en/index.md 通过 pymdownx.snippets 嵌入。 -->
<!-- 请勿使用相对链接或 GitHub 专用 Markdown 语法。 -->

# PyTauriX

PyTauriX is an independent Python framework for Tauri desktop applications.
It connects Python applications, the Tauri runtime, and a TypeScript frontend
through [Pyo3].

For the primary Chinese documentation, visit the
[Chinese documentation portal].

[Chinese documentation portal]: https://eclteam.github.io/PyTauriX/zh-CN/

[Tauri]: https://github.com/tauri-apps/tauri
[Pyo3]: https://github.com/PyO3/pyo3

---

[![CI: docs]][CI: docs#link] [![msrv]][msrv#link] [![requires-python]][requires-python#link] [![Discord]][Discord#link]

Documentation: <https://eclteam.github.io/PyTauriX/en/>

Source Code: <https://github.com/ECLteam/PyTauriX/>

Development lineage: see [UPSTREAM.md](https://github.com/ECLteam/PyTauriX/blob/main/UPSTREAM.md).

[CI: docs]: https://github.com/ECLteam/PyTauriX/actions/workflows/docs.yml/badge.svg
[CI: docs#link]: https://github.com/ECLteam/PyTauriX/actions/workflows/docs.yml
[Discord]: https://img.shields.io/discord/1411349756202188942?logo=discord&label=discord
[Discord#link]: https://discord.gg/TaXhVp7Shw
[msrv]: https://img.shields.io/crates/msrv/pytaurix?logo=rust
[msrv#link]: https://rust-lang.github.io/rfcs/2495-min-rust-version.html
<!--
TODO: Switch to <https://shields.io/badges/py-pi-python-version>,
but need to add python version classifiers in `pyproject.toml` first.
See also <https://github.com/badges/shields/issues/5551>.
-->
[requires-python]: https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fpytaurix%2Fpytaurix%2Frefs%2Fheads%2Fmain%2Fpython%2Fpytaurix%2Fpyproject.toml&logo=python
[requires-python#link]: https://packaging.python.org/en/latest/specifications/core-metadata/#requires-python

---

This is a completely free and open-source project, but it is difficult to maintain without incentives and contributions from the community.

If you think this project is helpful, consider giving it a star [![GitHub Repo stars]][Github Repo], it would be very helpful for my work and studies. 🥺👉👈

[GitHub Repo stars]: https://img.shields.io/github/stars/ECLteam/PyTauriX?style=social
[Github Repo]: https://github.com/ECLteam/PyTauriX

---

## Features

> **TL;DR**
>
> You are hurry and just wanna see/run the demo? See [examples/tauri-app](https://github.com/ECLteam/PyTauriX/tree/main/examples/tauri-app).

[notification]: https://docs.rs/tauri-plugin-notification/latest/tauri_plugin_notification/

- Need Rust compiler, but **almost don't need to write Rust code**!
- Or use `pytaurix-wheel`, **you won't need the Rust compiler, everything can be done in Python**! Check out [examples/tauri-app-wheel](https://github.com/ECLteam/PyTauriX/tree/main/examples/tauri-app-wheel).
- Can be integrated with `tauri-cli` to build and package standalone executables!
    - Use `Cython` to protect your source code!
- No IPC (inter-process communication) overhead, secure and fast, thanks to [Pyo3]!
- Support Tauri official plugins(e.g., [notification]), and you can write your own plugins!

    ![demo](https://github.com/user-attachments/assets/14ad5b51-b333-4d80-b04b-af72c4179571)

- Natively support async python (`asyncio`, `trio` or `anyio`)
- **100%** [Type Completeness](https://microsoft.github.io/pyright/#/typed-libraries?id=type-completeness)
- Ergonomic API (and as close as possible to the Tauri Rust API)
    - [Automatically generated TypeScript types and client for IPC](https://github.com/ECLteam/PyTauriX/tree/main/examples/tauri-app/src/client)
    - Python

        ```python
        import sys

        from pydantic import BaseModel
        from pytaurix import (
            AppHandle,
            Commands,
        )
        from pytaurix.plugins.notification import NotificationExt

        commands: Commands = Commands()


        class Person(BaseModel):
            name: str


        class Greeting(BaseModel):
            message: str


        @commands.command()
        async def greet(body: Person, app_handle: AppHandle) -> Greeting:
            notification_builder = NotificationExt.builder(app_handle)
            notification_builder.show(title="Greeting", body=f"Hello, {body.name}!")

            return Greeting(
                message=f"Hello, {body.name}! You've been greeted from Python {sys.version}!"
            )
        ```

    - Frontend

        ```ts
        import { pyInvoke } from "@pytaurix/api";
        // or: `const { pyInvoke } = window.__TAURI__.pytaurix;`

        export interface Person {
            name: string;
        }

        export interface Greeting {
            message: string;
        }

        export async function greet(body: Person): Promise<Greeting> {
            return await pyInvoke("greet", body);
        }
        ```

- Can be integrated with [nicegui]/[gradio]/[FastAPI] to achieve a full-stack Python development experience (i.g., without `Node.js`). See [examples/nicegui-app](https://github.com/ECLteam/PyTauriX/tree/main/examples/nicegui-app).

## Release

We follow [Semantic Versioning 2.0.0](https://semver.org/).

Rust and its Python bindings, PyTauriX core and its plugins will keep the same `MAJOR.MINOR` version number.

| name | pypi | crates.io | npmjs |
|:-------:|:----:|:---------:|:-----:|
| 👉 **core** | - | - | - |
| pytaurix | [![pytaurix-pypi-v]][pytaurix-pypi] | [![pytaurix-crates-v]][pytaurix-crates] | |
| pytaurix-core | | [![pytaurix-core-crates-v]][pytaurix-core-crates] | |
| tauri-plugin-pytaurix | | [![tauri-plugin-pytaurix-crates-v]][tauri-plugin-pytaurix-crates] | [![pytaurix-api-npm-v]][pytaurix-api-npm] |
| 👉 **wheel** | - | - | - |
| pytaurix-wheel | [![pytaurix-wheel-pypi-v]][pytaurix-wheel-pypi] | | |
| 👉 **utils** | - | - | - |
| pyo3-utils | [![pyo3-utils-pypi-v]][pyo3-utils-pypi] | [![pyo3-utils-crates-v]][pyo3-utils-crates] | |
| codelldb | [![codelldb-pypi-v]][codelldb-pypi] | | |

[pytaurix-pypi-v]: https://img.shields.io/pypi/v/pytaurix
[pytaurix-pypi]: https://pypi.org/project/pytaurix
[pytaurix-crates-v]: https://img.shields.io/crates/v/pytaurix
[pytaurix-crates]: https://crates.io/crates/pytaurix
[pytaurix-core-crates-v]: https://img.shields.io/crates/v/pytaurix-core
[pytaurix-core-crates]: https://crates.io/crates/pytaurix-core
[pytaurix-wheel-pypi-v]: https://img.shields.io/pypi/v/pytaurix-wheel
[pytaurix-wheel-pypi]: https://pypi.org/project/pytaurix-wheel
[tauri-plugin-pytaurix-crates-v]: https://img.shields.io/crates/v/tauri-plugin-pytaurix
[tauri-plugin-pytaurix-crates]: https://crates.io/crates/tauri-plugin-pytaurix
[pytaurix-api-npm-v]:https://img.shields.io/npm/v/@pytaurix/api
[pytaurix-api-npm]: https://www.npmjs.com/package/@pytaurix/api
[pyo3-utils-pypi-v]: https://img.shields.io/pypi/v/pyo3-utils
[pyo3-utils-pypi]: https://pypi.org/project/pyo3-utils
[pyo3-utils-crates-v]: https://img.shields.io/crates/v/pyo3-utils
[pyo3-utils-crates]: https://crates.io/crates/pyo3-utils
[codelldb-pypi-v]: https://img.shields.io/pypi/v/codelldb
[codelldb-pypi]: https://pypi.org/project/codelldb

## Philosophy

### For Pythoneer

I hope `PyTauriX` can become an alternative to [pywebview] and [Pystray], leveraging Tauri's comprehensive features to offer Python developers a GUI framework and a batteries-included development experience similar to [electron] and [PySide].

> PyTauriX is inspired by [FastAPI] and [Pydantic], aiming to offer a similar development experience.

### For Rustacean

Through [Pyo3], I hope Rust developers can better utilize the Python ecosystem (e.g., building AI GUI applications with [PyTorch]).

Although Rust's lifetime and ownership system makes Rust code safer, Python's garbage collection (GC) will make life easier. 😆

[pywebview]: https://github.com/r0x0r/pywebview
[Pystray]: https://github.com/moses-palmer/pystray
[electron]: https://github.com/electron/electron
[PySide]: https://wiki.qt.io/Qt_for_Python
[FastAPI]: https://github.com/fastapi/fastapi
[Pydantic]: https://github.com/pydantic/pydantic
[PyTorch]: https://github.com/pytorch/pytorch
[nicegui]: https://github.com/zauberzeug/nicegui
[gradio]: https://github.com/gradio-app/gradio

## Credits

PyTauriX is a project that aims to provide Python bindings for [Tauri], a cross-platform webview GUI library. `Tauri` is a trademark of the Tauri Program within the Commons Conservancy and PyTauriX is not officially endorsed or supported by them. PyTauriX is an independent and community-driven effort that respects the original goals and values of Tauri. PyTauriX does not claim any ownership or affiliation with the Tauri Program.

## License

This project is licensed under the terms of the *Apache License 2.0*.
