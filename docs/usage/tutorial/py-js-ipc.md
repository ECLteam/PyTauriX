# IPC between Python and JavaScript

!!! tip
    **See [concepts/ipc](../concepts/ipc.md) for more information.**

!!! tip
    **Also, see [Async Recipes](../concepts/async.md) for how to work smoothly with asynchronous PyTauriX.**

---

pytaurix implements the same IPC API as tauri. You can use it through [pytaurix.Commands][].

This tutorial will demonstrate how to use pytaurix's IPC API by rewriting the `fn greet` command in `src-tauri/src/lib.rs` in Python.

## Enable pytaurix ipc permission

pytaurix internally implements IPC through `tauri-plugin-pytaurix`.
You need to add it to the dependencies so that you can enable its permission in tauri.

```toml title="src-tauri/Cargo.toml"
# ...

[dependencies]
# ...
tauri-plugin-pytaurix = { version = "0.8" }  # (1)!
```

1. This is the version at the time of writing this tutorial. There may be a newer version of pytaurix available when you use it.

Refer to <https://tauri.app/security/capabilities/> to add the permission:

```json title="src-tauri/capabilities/default.json"
{
    // ...
    "permissions": [
        // ...
        "pytaurix:default"
    ]
}
```

## IPC in python

### install dependencies

pytaurix relies on [pydantic](https://github.com/pydantic/pydantic) for serialization and validation, and on [anyio](https://github.com/agronholm/anyio) for `asyncio`/`trio` support.

Therefore, you need to install these dependencies:

```toml title="src-tauri/pyproject.toml"
# ...

[project]
# ...
dependencies = [
    # ...
    "pydantic == 2.*",
    "anyio == 4.*"
]
```

!!! tip
    After adding dependencies, you need to use commands like `uv sync` or `uv pip install` to synchronize your dependency environment.

### add command

see [concepts/ipc](../concepts/ipc.md) for more information.

```python title="src-tauri/python/tauri_app/__init__.py"
--8<-- "docs/snippets/tutorial/invoke_handler.py:command"
```

### generate invoke handler for app

```python title="src-tauri/python/tauri_app/__init__.py"
--8<-- "docs/snippets/tutorial/invoke_handler.py"
```

## IPC in JavaScript

pytaurix provides an API similar to the [`invoke`](https://tauri.app/reference/javascript/api/namespacecore/#invoke) function in `@tauri-apps/api/core` through `@pytaurix/api`.

First, install it: `#!bash pnpm add @pytaurix/api`.

Now, you can invoke the command from your JavaScript code:

```ts title="src/main.ts"
--8<-- "docs/snippets/tutorial/cammand.ts:invoke"
```
