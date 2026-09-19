# State Management

Ref:

- <https://tauri.app/develop/state-management/>
- [pytaurix.State][]
- [pytaurix.Manager.state][]
- [pytaurix.Manager.manage][]

PyTauriX implements state management API consistent with Rust Tauri. Reading Tauri's documentation is like reading PyTauriX's documentation.

## Managing and Accessing State

```python
--8<-- "docs/snippets/tutorial/state_management/managing_accessing.py"
```

## State injection in `Commands`

You can inject state into any Command, with any type and any parameter name, as long as you use `Annotated[T, State()]` as its type annotation.

!!! note
    You must [Manager.manage][pytaurix.Manager.manage] these states before you invoke the command, or the invocation will be rejected.

```python
--8<-- "docs/snippets/tutorial/state_management/state_injection.py"
```
