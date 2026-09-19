# Async And Callbacks

!!! info
    FastAPI has a brief tutorial about `async` that you might find interesting: <https://fastapi.tiangolo.com/async/>

PyTauriX/Tauri runtime model:

1. The main thread is used for Tauri App's window/webview event loop
2. Tauri (Rust part) uses [tokio multi-threaded async runtime] to execute asynchronous code like IPC commands
3. PyTauriX uses [anyio.from_thread.BlockingPortal][] async runtime in a separate thread to execute asynchronous code like IPC commands

[tokio multi-threaded async runtime]: https://docs.rs/tokio/1.46.0/tokio/runtime/index.html#multi-thread-scheduler

---

You might notice that some Tauri/PyTauriX APIs use synchronous callbacks, such as:

- `Listener` ([Tauri](https://docs.rs/tauri/2.6.0/tauri/trait.Listener.html)/[PyTauriX][pytaurix.Listener])
- `AppHandle::on_menu_event` ([Tauri](https://docs.rs/tauri/2.6.0/tauri/struct.AppHandle.html#method.on_menu_event)/[PyTauriX][pytaurix.AppHandle.on_menu_event])
- etc.

These synchronous callbacks execute either in the main thread or in Tauri's tokio multi-threaded async runtime. However, one thing is certain: they will never execute in PyTauriX's anyio async runtime.

Unlike the tokio runtime in Rust, Python's async runtimes (`anyio`/`asyncio`/`trio`) are not thread-safe.

!!! info "Thread safety references"

    - <https://anyio.readthedocs.io/en/stable/threads.html>
    - <https://docs.python.org/3/library/asyncio-task.html#asyncio.run_coroutine_threadsafe>

This means you cannot directly use Python's async APIs (like [anyio.create_task_group][]) and async synchronization primitives (like [anyio.Event][]) in these synchronous callbacks (i.e., in another thread): [pytaurix/pytaurix#132].

[pytaurix/pytaurix#132]: https://github.com/ECLteam/PyTauriX/issues/132

Fortunately, anyio provides some methods to achieve this, such as [BlockingPortal.call][anyio.from_thread.BlockingPortal.call], etc: <https://anyio.readthedocs.io/en/stable/threads.html#calling-asynchronous-code-from-an-external-thread>.

However, using this approach directly is not very ergonomic. Therefore, `pytaurix` provides some utility tools to simplify this process since `v0.7`.

## Async Tools

The [pytaurix_utils.async_tools][] module provides some tools to simplify the process of using async APIs in synchronous callbacks/contexts.

!!! tip
    `pytaurix_utils` is distributed as part of the [`pytaurix`](https://pypi.org/project/pytaurix/) package on PyPI.
    Therefore, running `pip install pytaurix` will also install it.

First, let's add [AsyncTools][pytaurix_utils.async_tools.AsyncTools] to the [App State](../tutorial/state-management.md):

```python
--8<-- "docs/snippets/concepts/async/async_tools_state.py"
```

Then we can access it through [Manager.state](../tutorial/state-management.md#managing-and-accessing-state) API or [`command state injection`](../tutorial/state-management.md#state-injection-in-commands).

### Run Async Code in Sync Callbacks

The [AsyncTools.to_sync][pytaurix_utils.async_tools.AsyncTools.to_sync] method allows you to convert an async function to a sync function, so you can use it in/as synchronous callbacks.

```python
--8<-- "docs/snippets/concepts/async/to_sync.py"
```

!!! tip
    Alternatively, you can use [BlockingPortal.call][anyio.from_thread.BlockingPortal.call] or [BlockingPortal.start_task_soon][anyio.from_thread.BlockingPortal.start_task_soon] directly, as it has better performance (no need to instantiate a new function).

    See following [AsyncTools.portal](#access-raw-blockingportal).

### Run Blocking Code in Async Context

> Ref: <https://anyio.readthedocs.io/en/stable/threads.html#>
>
> Practical asynchronous applications occasionally need to run network, file or computationally expensive operations. Such operations would normally block the asynchronous event loop, leading to performance issues. The solution is to run such code in worker threads. Using worker threads lets the event loop continue running other tasks while the worker thread runs the blocking call.

The [AsyncTools.to_async][pytaurix_utils.async_tools.AsyncTools.to_async] method allows you to convert a sync function to an async function, so you won't block the async event loop.

```python
--8<-- "docs/snippets/concepts/async/to_async.py"
```

!!! tip
    This method exists more as a symmetric counterpart to `to_sync`.
    In practical applications, you might prefer to use [anyio.to_thread.run_sync][], as it has better performance (no need to instantiate a new function).

### Run Async Code in Background

You can use the [TaskGroup.start_soon][anyio.abc.TaskGroup.start_soon] method to run an async function in the background.

```python
--8<-- "docs/snippets/concepts/async/start_soon_in_background.py"
```

### Access Raw `BlockingPortal`

You can access the `BlockingPortal` you passed when instantiating `AsyncTools` through [AsyncTools.portal][pytaurix_utils.async_tools.AsyncTools.portal].
