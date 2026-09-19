# ruff: noqa: D102
# pyright: reportPrivateUsage=false

"""[tauri::self](https://docs.rs/tauri/latest/tauri/index.html)"""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator, Mapping, Sequence
from enum import Enum, auto
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    LiteralString,
    Never,
    NewType,
    NoReturn,
    Protocol,
    Required,
    Self,
    Union,
    final,
)

from pydantic import NonNegativeInt
from typing_extensions import (
    TypeAliasType,
    TypedDict,
    TypeVar,
    Unpack,
    deprecated,
)

from pytaurix.ffi._ext_mod import pytaurix_mod
from pytaurix.ffi._typing import Pyo3PathFrom, Pyo3PathInto

__all__ = [
    "IS_DEV",
    "RESTART_EXIT_CODE",
    "VERSION",
    "App",
    "AppHandle",
    "Assets",
    "Builder",
    "BuilderArgs",
    "CloseRequestApi",
    "Context",
    "CursorIcon",
    "DragDropEvent",
    "DragDropEventType",
    "Emitter",
    "Event",
    "EventId",
    "EventTarget",
    "EventTargetType",
    "ExitRequestApi",
    "ImplEmitter",
    "ImplListener",
    "ImplManager",
    "Listener",
    "LogicalRect",
    "Manager",
    "PhysicalRect",
    "Position",
    "PositionType",
    "Rect",
    "RunEvent",
    "RunEventType",
    "Size",
    "SizeType",
    "Theme",
    "Url",
    "UserAttentionType",
    "WebviewEvent",
    "WebviewEventType",
    "WebviewUrl",
    "WebviewUrlType",
    "WindowEvent",
    "WindowEventType",
    "builder_factory",
    "context_factory",
    "webview_version",
]

if TYPE_CHECKING:
    from pytaurix.ffi.ipc import Invoke


_T = TypeVar("_T", infer_variance=True)


class _InvokeHandlerProto(Protocol):
    def __call__(self, invoke: Invoke, /) -> Any: ...


_AppRunCallbackType = Callable[["AppHandle", "RunEventType"], None]

_EventHandlerType = Callable[["Event"], None]

_PhysicalPositionF64 = tuple[float, float]
"""[tauri::PhysicalPosition](https://docs.rs/tauri/latest/tauri/struct.PhysicalPosition.html)"""
_PhysicalPositionI32 = tuple[int, int]
"""[tauri::PhysicalPosition](https://docs.rs/tauri/latest/tauri/struct.PhysicalPosition.html)"""
_LogicalPositionF64 = tuple[float, float]
"""[tauri::LogicalPosition](https://docs.rs/tauri/latest/tauri/struct.LogicalPosition.html)"""
_PhysicalSizeU32 = tuple[NonNegativeInt, NonNegativeInt]
"""[tauri::PhysicalSize](https://docs.rs/tauri/latest/tauri/struct.PhysicalSize.html)"""
_LogicalSizeF64 = tuple[float, float]
"""[tauri::PhysicalSize](https://docs.rs/tauri/latest/tauri/struct.LogicalSize.html)"""

_VecPathBuf = list[Path]
"""[tauri::DragDropEvent::Enter::paths](https://docs.rs/tauri/latest/tauri/enum.DragDropEvent.html#variant.Enter.field.paths)"""

# TODO: export this type in rust [ext_mod::utils::assets] namespace
_AssetKey = TypeAliasType("_AssetKey", str)
"""[tauri::utils::assets::AssetKey](https://docs.rs/tauri-utils/latest/tauri_utils/assets/struct.AssetKey.html)"""

_ConfigInto = TypeAliasType("_ConfigInto", dict[str, Any])
"""[tauri::Config](https://docs.rs/tauri/latest/tauri/struct.Config.html)"""
_ConfigFrom = TypeAliasType("_ConfigFrom", Mapping[str, Any])
"""[tauri::Config](https://docs.rs/tauri/latest/tauri/struct.Config.html)"""


RESTART_EXIT_CODE: Final[int] = pytaurix_mod.RESTART_EXIT_CODE
"""[tauri::RESTART_EXIT_CODE](https://docs.rs/tauri/latest/tauri/constant.RESTART_EXIT_CODE.html)

The exit code on `RunEvent::ExitRequested` when `AppHandle` is called.
"""
VERSION: Final[LiteralString] = pytaurix_mod.VERSION
"""[tauri::VERSION](https://docs.rs/tauri/latest/tauri/constant.VERSION.html)

The Tauri version.
"""
IS_DEV: Final[bool] = pytaurix_mod.IS_DEV
"""[tauri::is_dev](https://docs.rs/tauri/latest/tauri/fn.is_dev.html)

Whether we are running in development mode or not.
"""


if TYPE_CHECKING:
    from pytaurix.ffi.image import Image
    from pytaurix.ffi.menu import Menu, MenuEvent
    from pytaurix.ffi.path import PathResolver
    from pytaurix.ffi.plugin import Plugin
    from pytaurix.ffi.tray import TrayIcon, TrayIconEventType
    from pytaurix.ffi.webview import WebviewWindow
    from pytaurix.ffi.window import Monitor

    def webview_version() -> str:
        """[tauri::webview_version](https://docs.rs/tauri/latest/tauri/fn.webview_version.html)

        Get WebView/Webkit version on current platform.
        """
        ...

    @final
    class App:
        """[Tauri::app](https://docs.rs/tauri/latest/tauri/struct.App.html)

        !!! warning
            This class is not thread-safe, and should not be shared between threads.

            - You can only use it on the thread it was created on.
            - And you need to ensure it is garbage collected on the thread it was created on,
                otherwise it will cause memory leaks.
        """

        def run_on_main_thread(self, handler: Callable[[], object], /) -> None:
            """Runs the given closure on the main thread.

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

        def handle(self, /) -> AppHandle:
            """Get a handle to this app, which can be used to interact with the app from another thread."""
            ...

        def run(self, callback: _AppRunCallbackType | None = None, /) -> NoReturn:
            """Consume and run this app, will block until the app is exited.

            Args:
                callback: a callback function that will be called on each event.
                    It will be called on the same thread that the app was created on,
                    so you should not block in this function.

            !!! note
                This function will call `std::process::exit` at the end to terminate the entire process,
                which means the Python interpreter cannot be properly finalized.
                If this is a problem for you, please use [pytaurix.App.run_return][].

            !!! warning
                If `callback` is specified, it must not raise an exception,
                otherwise it is logical undefined behavior, and in most cases, the program will panic.
            """
            ...

        def run_return(self, callback: _AppRunCallbackType | None = None, /) -> int:
            """Consume and run this application, returning its intended exit code.

            !!! warning
                `callback` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

        @deprecated(
            """When called in a loop (as suggested by the name), this function will busy-loop.
            To re-gain control of control flow after the app has exited, use `App::run_return` instead.
            See <https://docs.rs/tauri/latest/tauri/struct.App.html#method.run_iteration> for more details.""",
            category=None,
        )
        def run_iteration(self, callback: _AppRunCallbackType | None = None, /) -> None:
            """Run this app iteratively without consuming it, calling `callback` on each iteration.

            Args:
                callback: a callback function that will be called on each iteration.

            !!! warning
                `callback` has the same restrictions as [App.run][pytaurix.App.run].

            !!! tip
                Approximately 2ms per calling in debug mode.
            """

        def cleanup_before_exit(self, /) -> None:
            """Runs necessary cleanup tasks before exiting the process.

            **You should always exit the tauri app immediately after this function returns and not use any tauri-related APIs.**
            """

    @final
    class AppHandle:
        """[tauri::AppHandle](https://docs.rs/tauri/latest/tauri/app/struct.AppHandle.html)"""

        def run_on_main_thread(self, handler: Callable[[], object], /) -> None:
            """Runs the given closure on the main thread.

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

        def plugin(self, plugin: Plugin, /) -> None: ...
        def remove_plugin(self, plugin: str, /) -> bool: ...
        def exit(self, exit_code: int, /) -> None: ...
        def restart(self, /) -> Never: ...
        def request_restart(self, /) -> None: ...

        if sys.platform == "darwin":

            def set_dock_visibility(self, visible: bool, /) -> None: ...

        def on_menu_event(self, handler: Callable[[Self, MenuEvent], None], /) -> None:
            """Registers a global menu event listener.

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """

        def on_tray_icon_event(
            self, handler: Callable[[Self, TrayIconEventType], None], /
        ) -> None:
            """Registers a global tray icon menu event listener.

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """

        def tray_by_id(self, id: str, /) -> TrayIcon | None: ...  # noqa: A002
        def remove_tray_by_id(self, id: str, /) -> TrayIcon | None: ...  # noqa: A002
        def config(self) -> _ConfigInto: ...
        def primary_monitor(self) -> Monitor | None: ...
        def monitor_from_point(self, x: float, y: float, /) -> Monitor | None: ...
        def available_monitors(self) -> list[Monitor]: ...
        def cursor_position(self) -> _PhysicalPositionF64: ...
        def set_theme(self, theme: Theme | None, /) -> None: ...
        def default_window_icon(self, /) -> Image | None:
            """Returns the default window icon.

            !!! warning
                Each time you call this function, a new image instance will be created.
                So you should cache the result if you need to use it multiple times.
            """

        def menu(self) -> Menu | None: ...
        def set_menu(self, menu: Menu, /) -> Menu | None: ...
        def remove_menu(self) -> Menu | None: ...
        def hide_menu(self) -> None: ...
        def show_menu(self) -> None: ...
        def cleanup_before_exit(self) -> None: ...
        def invoke_key(self) -> str: ...

    @final
    class Builder:
        """[tauri::Builder](https://docs.rs/tauri/latest/tauri/struct.Builder.html)

        use [builder_factory][pytaurix.builder_factory] to instantiate this class.

        !!! warning
            This class is not thread-safe, and should not be shared between threads.

            - You can only use it on the thread it was created on.
            - And you need to ensure it is garbage collected on the thread it was created on,
                otherwise it will cause memory leaks.
        """

        def build(self, context: Context, **kwargs: Unpack[BuilderArgs]) -> App:
            """[tauri::Builder::build](https://docs.rs/tauri/latest/tauri/struct.Builder.html#method.build)

            Consume this builder and build an app with the given `BuilderArgs`.

            Args:
                context: use [context_factory][pytaurix.context_factory] to get it.
                **kwargs: see [BuilderArgs][pytaurix.BuilderArgs] for details.
            """
            ...

    @final
    class Context:
        """[tauri::Context](https://docs.rs/tauri/latest/tauri/struct.Context.html)"""

        def set_assets(self, assets: Assets, /) -> None:
            """Use custom assets instead of the assets bundled by Tauri.

            To make this work:

            - You need to enable the `tauri/custom-protocol` feature.
                - Or build using `tauri build`.
            - Set `frontendDist` in `tauri.conf.json` to an empty directory (do not set it to a URL).
                - Or generate `Context` via:

                    ```rust
                    use tauri::{generate_context, test::noop_assets};

                    let context = generate_context!(assets=noop_assets());
                    ```

                    then we will use this method to set the assets.

                    see: <https://github.com/tauri-apps/tauri/pull/9141>
            """

    @final
    class RunEvent:
        """[tauri::RunEvent](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html)"""

        @final
        class Exit:
            """[tauri::RunEvent::Exit](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.Exit)"""

        @final
        class ExitRequested:
            """[tauri::RunEvent::ExitRequested](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.ExitRequested)"""

            code: int | None
            api: ExitRequestApi

        @final
        class WindowEvent:
            """[tauri::RunEvent::WindowEvent](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.WindowEvent)"""

            label: str
            event: WindowEventType

        @final
        class WebviewEvent:
            """[tauri::RunEvent::WebviewEvent](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.WebviewEvent)"""

            label: str
            event: WebviewEventType

        @final
        class Ready:
            """[tauri::RunEvent::Ready](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.Ready)"""

        @final
        class Resumed:
            """[tauri::RunEvent::Resumed](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.Resumed)"""

        @final
        class MainEventsCleared:
            """[tauri::RunEvent::MainEventsCleared](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.MainEventsCleared)"""

        @final
        class MenuEvent(tuple[MenuEvent]):
            """[tauri::RunEvent::MenuEvent](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.MenuEvent)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: MenuEvent
            __match_args__ = ("_0",)

            def __new__(cls, _0: MenuEvent, /) -> Self: ...

        @final
        class TrayIconEvent(tuple[TrayIconEventType]):
            """[tauri::RunEvent::TrayIconEvent](https://docs.rs/tauri/latest/tauri/enum.RunEvent.html#variant.TrayIconEvent)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: TrayIconEventType
            __match_args__ = ("_0",)

            def __new__(cls, _0: TrayIconEventType, /) -> Self: ...

        @final
        class _NonExhaustive:
            """Reserved for `#[non_exhaustive]`"""

        # When adding new variants, remember to update `RunEventType`.

    @final
    class ExitRequestApi:
        """[tauri::ExitRequestApi](https://docs.rs/tauri/latest/tauri/struct.ExitRequestApi.html)"""

        def prevent_exit(self, /) -> None: ...

    @final
    class CloseRequestApi:
        """[tauri::CloseRequestApi](https://docs.rs/tauri/latest/tauri/struct.CloseRequestApi.html)"""

        def prevent_close(self, /) -> None: ...

    @final
    class DragDropEvent:
        """[tauri::DragDropEvent](https://docs.rs/tauri/latest/tauri/enum.DragDropEvent.html)"""

        @final
        class Enter:
            """[tauri::DragDropEvent::Enter](https://docs.rs/tauri/latest/tauri/enum.DragDropEvent.html#variant.Enter)"""

            paths: _VecPathBuf
            position: _PhysicalPositionF64

        @final
        class Over:
            """[tauri::DragDropEvent::Over](https://docs.rs/tauri/latest/tauri/enum.DragDropEvent.html#variant.Over)"""

            position: _PhysicalPositionF64

        @final
        class Drop:
            """[tauri::DragDropEvent::Drop](https://docs.rs/tauri/latest/tauri/enum.DragDropEvent.html#variant.Drop)"""

            paths: _VecPathBuf
            position: _PhysicalPositionF64

        @final
        class Leave:
            """[tauri::DragDropEvent::Leave](https://docs.rs/tauri/latest/tauri/enum.DragDropEvent.html#variant.Leave)"""

        @final
        class _NonExhaustive:
            """Reserved for `#[non_exhaustive]`"""

        # When adding new variants, remember to update `DragDropEventType`.

    @final
    class WebviewEvent:
        """[tauri::WebviewEvent](https://docs.rs/tauri/latest/tauri/enum.WebviewEvent.html)"""

        @final
        class DragDrop(tuple["DragDropEventType"]):
            """[tauri::WebviewEvent::DragDrop](https://docs.rs/tauri/latest/tauri/enum.WebviewEvent.html#variant.DragDrop)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: DragDropEventType
            __match_args__ = ("_0",)

            def __new__(cls, _0: DragDropEventType, /) -> Self: ...

        @final
        class _NonExhaustive:
            """Reserved for `#[non_exhaustive]`"""

        # When adding new variants, remember to update `WebviewEventType`.

    @final
    class WindowEvent:
        """[tauri::WindowEvent](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html)"""

        @final
        class Resized(tuple[_PhysicalSizeU32]):
            """[tauri::WindowEvent::Resized](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.Resized)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: _PhysicalSizeU32
            __match_args__ = ("_0",)

            def __new__(cls, _0: _PhysicalSizeU32, /) -> Self: ...

        @final
        class Moved(tuple[_PhysicalPositionI32]):
            """[tauri::WindowEvent::Moved](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.Moved)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: _PhysicalPositionI32
            __match_args__ = ("_0",)

            def __new__(cls, _0: _PhysicalPositionI32, /) -> Self: ...

        @final
        class CloseRequested:
            """[tauri::WindowEvent::CloseRequested](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.CloseRequested)"""

            api: CloseRequestApi

        @final
        class Destroyed:
            """[tauri::WindowEvent::Destroyed](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.Destroyed)"""

        @final
        class Focused(tuple[bool]):
            """[tauri::WindowEvent::Focused](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.Focused)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: bool
            __match_args__ = ("_0",)

            def __new__(cls, _0: bool, /) -> Self: ...

        @final
        class ScaleFactorChanged:
            """[tauri::WindowEvent::ScaleFactorChanged](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.ScaleFactorChanged)"""

            scale_factor: float
            new_inner_size: _PhysicalSizeU32

        @final
        class DragDrop(tuple["DragDropEventType"]):
            """[tauri::WindowEvent::DragDrop](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.DragDrop)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: DragDropEventType
            __match_args__ = ("_0",)

            def __new__(cls, _0: DragDropEventType, /) -> Self: ...

        @final
        class ThemeChanged(tuple["Theme"]):
            """[tauri::WindowEvent::ThemeChanged](https://docs.rs/tauri/latest/tauri/enum.WindowEvent.html#variant.ThemeChanged)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: Theme
            __match_args__ = ("_0",)

            def __new__(cls, _0: Theme, /) -> Self: ...

        @final
        class _NonExhaustive:
            """Reserved for `#[non_exhaustive]`"""

        # When adding new variants, remember to update `WindowEventType`.

    def builder_factory(*args: Any, **kwargs: Any) -> Builder:
        """A factory function for creating a `Builder` instance.

        This is the closure passed from the Rust side when initializing the pytaurix pyo3 module.
        `args` and `kwargs` will be passed to this closure.
        """
        ...

    def context_factory(*args: Any, **kwargs: Any) -> Context:
        """A factory function for creating a `Context` instance.

        This is the closure passed from the Rust side when initializing the pytaurix pyo3 module.
        `args` and `kwargs` will be passed to this closure.
        """
        ...

    @final
    class Manager:
        """[tauri::Manager](https://docs.rs/tauri/latest/tauri/trait.Manager.html)"""

        @staticmethod
        def app_handle(slf: ImplManager, /) -> AppHandle:
            """The application handle associated with this manager."""
            ...

        @staticmethod
        def get_webview_window(slf: ImplManager, label: str, /) -> WebviewWindow | None:
            """Fetch a single webview window from the manager."""
            ...

        @staticmethod
        def webview_windows(slf: ImplManager, /) -> dict[str, WebviewWindow]:
            """Fetch all managed webview windows."""
            ...

        @staticmethod
        def manage(slf: ImplManager, state: object, /) -> bool:
            """Add `state` to the state managed by the application.

            If the state for the `T` type has previously been set, the state is unchanged and false is returned.
            Otherwise true is returned.
            """
            ...

        @staticmethod
        def state(slf: ImplManager, state_type: type[_T], /) -> _T:
            """Retrieves the managed state for the type `T`.

            Raises:
                Exception: Panics if the state for the type `T` has not been previously [managed][pytaurix.ffi.lib.Manager].
                    Use [try_state][pytaurix.ffi.lib.Manager.try_state] for a non-panicking version.
            """
            ...

        @staticmethod
        def try_state(slf: ImplManager, state_type: type[_T], /) -> _T | None:
            """Attempts to retrieve the managed state for the type `T`.

            Returns `Some` if the state has previously been `managed`. Otherwise returns `None`.
            """
            ...

        @staticmethod
        def path(slf: ImplManager, /) -> PathResolver:
            """The path resolver is a helper class for general and application-specific path APIs."""
            ...

    @final
    class Event:
        """[tauri::Event](https://docs.rs/tauri/latest/tauri/struct.Event.html)"""

        @property
        def id(self) -> EventId:
            """The `EventId` of the handler that was triggered."""
            ...

        @property
        def payload(self) -> str:
            """The event payload."""
            ...

    @final
    class Listener:
        """[tauri::Listener](https://docs.rs/tauri/latest/tauri/trait.Listener.html)

        See also: <https://tauri.app/develop/calling-rust/#event-system>

        # Examples

        ```python
        from pydantic import BaseModel
        from pytaurix import AppHandle, Event, Listener


        class Payload(BaseModel):  # or `RootModel`
            url: str
            num: int


        def listen(app_handle: AppHandle) -> None:
            def handler(event: Event):
                assert event.id == event_id

                serialized_event = Payload.model_validate_json(event.payload)
                print(serialized_event.url, serialized_event.num)

            event_id = Listener.listen(app_handle, "event_name", handler)
        ```
        """

        @staticmethod
        def listen(
            slf: ImplListener,
            event: str,
            handler: _EventHandlerType,
            /,
        ) -> EventId:
            """Listen to an emitted event on this manager.

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

        @staticmethod
        def once(
            slf: ImplListener,
            event: str,
            handler: _EventHandlerType,
            /,
        ) -> EventId:
            """Listen to an event on this manager only once.

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

        @staticmethod
        def unlisten(
            slf: ImplListener,
            id: EventId,  # noqa: A002
            /,
        ) -> None:
            """Remove an event listener."""
            ...

        @staticmethod
        def listen_any(
            slf: ImplListener,
            event: str,
            handler: _EventHandlerType,
            /,
        ) -> EventId:
            """Listen to an emitted event to any target.

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

        @staticmethod
        def once_any(
            slf: ImplListener,
            event: str,
            handler: _EventHandlerType,
            /,
        ) -> EventId:
            """Listens once to an emitted event to any target .

            !!! warning
                `handler` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

    @final
    class Position:
        """[tauri::Position](https://docs.rs/tauri/latest/tauri/enum.Position.html)"""

        @final
        class Physical(tuple[_PhysicalPositionI32]):
            """[tauri::Position::Physical](https://docs.rs/tauri/latest/tauri/enum.Position.html#variant.Physical)

            !!! warning
                This is actually a `Class` disguised as an `NamedTuple`.
                See also: <https://pyo3.rs/v0.23.4/class.html#pyclass-enums>.
            """

            _0: _PhysicalPositionI32
            __match_args__ = ("_0",)

            def __new__(cls, _0: _PhysicalPositionI32, /) -> Self: ...

        @final
        class Logical(tuple[_LogicalPositionF64]):
            """[tauri::Position::Logical](https://docs.rs/tauri/latest/tauri/enum.Position.html#variant.Logical)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: _LogicalPositionF64
            __match_args__ = ("_0",)

            def __new__(cls, _0: _LogicalPositionF64, /) -> Self: ...

    @final
    class Size:
        """[tauri::Size](https://docs.rs/tauri/latest/tauri/enum.Size.html)"""

        @final
        class Physical(tuple[_PhysicalSizeU32]):
            """[tauri::Size::Physical](https://docs.rs/tauri/latest/tauri/enum.Size.html#variant.Physical)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: _PhysicalSizeU32
            __match_args__ = ("_0",)

            def __new__(cls, _0: _PhysicalSizeU32, /) -> Self: ...

        @final
        class Logical(tuple[_LogicalSizeF64]):
            """[tauri::Size::Logical](https://docs.rs/tauri/latest/tauri/enum.Size.html#variant.Logical)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: _LogicalSizeF64
            __match_args__ = ("_0",)

            def __new__(cls, _0: _LogicalSizeF64, /) -> Self: ...

    @final
    class Rect:
        """[tauri::Rect](https://docs.rs/tauri/latest/tauri/struct.Rect.html)"""

        def __new__(
            cls,
            /,
            *,
            position: PositionType,
            size: SizeType,
        ) -> Self: ...

        @property
        def position(self) -> PositionType: ...
        @property
        def size(self) -> SizeType: ...

    @final
    class PhysicalRect:
        """[tauri::PhysicalRect](https://docs.rs/tauri/latest/tauri/struct.PhysicalRect.html)"""

        def __new__(
            cls,
            /,
            *,
            position: _PhysicalPositionI32,
            size: _PhysicalSizeU32,
        ) -> Self: ...

        @property
        def position(self) -> _PhysicalPositionI32: ...
        @property
        def size(self) -> _PhysicalSizeU32: ...

    @final
    class LogicalRect:
        """[tauri::LogicalRect](https://docs.rs/tauri/latest/tauri/struct.LogicalRect.html)"""

        def __new__(
            cls,
            /,
            *,
            position: _LogicalPositionF64,
            size: _LogicalSizeF64,
        ) -> Self: ...

        @property
        def position(self) -> _LogicalPositionF64: ...
        @property
        def size(self) -> _LogicalSizeF64: ...

    @final
    class EventTarget:
        """[tauri::EventTarget](https://docs.rs/tauri/latest/tauri/enum.EventTarget.html)"""

        @final
        class Any:
            """Any and all event targets."""

            def __new__(cls, /) -> Self: ...

        @final
        class AnyLabel:
            """Any `Window`, `Webview` or `WebviewWindow` that have this label."""

            label: str
            """Target label."""

            def __new__(cls, label: str, /) -> Self: ...

        @final
        class App:
            """App and AppHandle targets."""

            def __new__(cls, /) -> Self: ...

        @final
        class Window:
            """`Window` target."""

            label: str
            """window label."""

            def __new__(cls, label: str, /) -> Self: ...

        @final
        class Webview:
            """Webview target."""

            label: str
            """webview label."""

            def __new__(cls, label: str, /) -> Self: ...

        @final
        class WebviewWindow:
            """WebviewWindow target."""

            label: str
            """webview window label."""

            def __new__(cls, label: str, /) -> Self: ...

        @final
        class _NonExhaustive:
            """Reserved for `#[non_exhaustive]`"""

        # When adding new variants, remember to update `EventTargetType`.

    class Emitter:
        """[tauri::Emitter](https://docs.rs/tauri/latest/tauri/trait.Emitter.html)"""

        @staticmethod
        def emit_str(
            slf: ImplEmitter,
            event: str,
            payload: str,
            /,
        ) -> None:
            """Similar to [`Emitter::emit`] but the payload is json serialized."""
            ...

        @staticmethod
        def emit_str_to(
            slf: ImplEmitter,
            target: EventTargetType,
            event: str,
            payload: str,
            /,
        ) -> None:
            """Similar to [`Emitter::emit_to`] but the payload is json serialized."""
            ...

        @staticmethod
        def emit_str_filter(
            slf: ImplEmitter,
            event: str,
            payload: str,
            filter: Callable[[EventTargetType], bool],  # noqa: A002
            /,
        ) -> None:
            """Similar to [`Emitter::emit_filter`] but the payload is json serialized.

            !!! warning
                `filter` has the same restrictions as [App.run][pytaurix.App.run].
            """
            ...

    @final
    class Theme(Enum):
        """[tauri::Theme](https://docs.rs/tauri/latest/tauri/enum.Theme.html)

        !!! warning
            See [pytaurix.ffi.menu.NativeIcon][].
        """

        Light = auto()
        Dark = auto()
        _NonExhaustive = object()

    @final
    class UserAttentionType(Enum):
        """[tauri::UserAttentionType](https://docs.rs/tauri/latest/tauri/enum.UserAttentionType.html)"""

        Critical = auto()
        Informational = auto()

    @final
    class CursorIcon(Enum):
        """[tauri::CursorIcon](https://docs.rs/tauri/latest/tauri/enum.CursorIcon.html)"""

        Default = auto()
        Crosshair = auto()
        Hand = auto()
        Arrow = auto()
        Move = auto()
        Text = auto()
        Wait = auto()
        Help = auto()
        Progress = auto()
        NotAllowed = auto()
        ContextMenu = auto()
        Cell = auto()
        VerticalText = auto()
        Alias = auto()
        Copy = auto()
        NoDrop = auto()
        Grab = auto()
        Grabbing = auto()
        AllScroll = auto()
        ZoomIn = auto()
        ZoomOut = auto()
        EResize = auto()
        NResize = auto()
        NeResize = auto()
        NwResize = auto()
        SResize = auto()
        SeResize = auto()
        SwResize = auto()
        WResize = auto()
        EwResize = auto()
        NsResize = auto()
        NeswResize = auto()
        NwseResize = auto()
        ColResize = auto()
        RowResize = auto()
        _NonExhaustive = object()

    @final
    class WebviewUrl:
        """[tauri::WebviewUrl](https://docs.rs/tauri/latest/tauri/enum.WebviewUrl.html)"""

        @final
        class External(tuple["Url"]):
            """[tauri::WebviewUrl::External](https://docs.rs/tauri/latest/tauri/enum.WebviewUrl.html#variant.External)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: Url
            __match_args__ = ("_0",)

            def __new__(cls, _0: Url, /) -> Self: ...

        @final
        class App(tuple[Pyo3PathInto]):
            """[tauri::WebviewUrl::App](https://docs.rs/tauri/latest/tauri/enum.WebviewUrl.html#variant.App)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: Pyo3PathInto
            __match_args__ = ("_0",)

            def __new__(cls, _0: Pyo3PathFrom, /) -> Self: ...

        @final
        class CustomProtocol(tuple["Url"]):
            """[tauri::WebviewUrl::CustomProtocol](https://docs.rs/tauri/latest/tauri/enum.WebviewUrl.html#variant.CustomProtocol)

            !!! warning
                See [pytaurix.ffi.lib.Position.Physical][].
            """

            _0: Url
            __match_args__ = ("_0",)

            def __new__(cls, _0: Url, /) -> Self: ...

        @final
        class _NonExhaustive:
            """Reserved for `#[non_exhaustive]`"""

        # When adding new variants, remember to update `WebviewUrlType`.

else:
    webview_version = pytaurix_mod.webview_version
    App = pytaurix_mod.App
    AppHandle = pytaurix_mod.AppHandle
    Builder = pytaurix_mod.Builder
    Context = pytaurix_mod.Context
    RunEvent = pytaurix_mod.RunEvent
    ExitRequestApi = pytaurix_mod.ExitRequestApi
    CloseRequestApi = pytaurix_mod.CloseRequestApi
    DragDropEvent = pytaurix_mod.DragDropEvent
    WebviewEvent = pytaurix_mod.WebviewEvent
    WindowEvent = pytaurix_mod.WindowEvent
    builder_factory = pytaurix_mod.builder_factory
    context_factory = pytaurix_mod.context_factory
    Manager = pytaurix_mod.Manager
    Event = pytaurix_mod.Event
    Listener = pytaurix_mod.Listener
    Position = pytaurix_mod.Position
    Size = pytaurix_mod.Size
    Rect = pytaurix_mod.Rect
    PhysicalRect = pytaurix_mod.PhysicalRect
    LogicalRect = pytaurix_mod.LogicalRect
    EventTarget = pytaurix_mod.EventTarget
    Emitter = pytaurix_mod.Emitter
    Theme = pytaurix_mod.Theme
    UserAttentionType = pytaurix_mod.UserAttentionType
    CursorIcon = pytaurix_mod.CursorIcon
    WebviewUrl = pytaurix_mod.WebviewUrl


class BuilderArgs(TypedDict, total=False):
    """[tauri::Builder](https://docs.rs/tauri/latest/tauri/struct.Builder.html)"""

    invoke_handler: Required[_InvokeHandlerProto | None]
    """ Use [Commands][pytaurix.ipc.Commands] to get it.

    !!! warning
        The implement of `invoke_handler` must never raise an exception,
        otherwise it is considered logical undefined behavior.
        Additionally, `invoke_handler` must not block.

    !!! warning
        If you do not specify `invoke_handler`,
        `pytaurix` will not register the `tauri-plugin-pytaurix` plugin,
        which means you cannot use `pyInvoke` in the frontend to call `Commands`
        (you will receive an error like ["plugin pytaurix not found"]).
        If this is indeed the behavior you expect, explicitly pass [None][].

        ["plugin pytaurix not found"]: https://github.com/ECLteam/PyTauriX/issues/110
    """
    setup: Callable[[AppHandle], object]
    """See rust `tauri::Builder::setup`"""
    plugins: Sequence[Plugin]
    """See rust `tauri::Builder::plugin`"""


RunEventType = TypeAliasType(
    "RunEventType",
    RunEvent.Exit
    | RunEvent.ExitRequested
    | RunEvent.WindowEvent
    | RunEvent.WebviewEvent
    | RunEvent.Ready
    | RunEvent.Resumed
    | RunEvent.MainEventsCleared
    | RunEvent.MenuEvent
    | RunEvent.TrayIconEvent
    | RunEvent._NonExhaustive,
)
"""See [RunEvent][pytaurix.ffi.RunEvent] for details."""

DragDropEventType = TypeAliasType(
    "DragDropEventType",
    DragDropEvent.Enter
    | DragDropEvent.Over
    | DragDropEvent.Drop
    | DragDropEvent.Leave
    | DragDropEvent._NonExhaustive,
)
"""See [DragDropEvent][pytaurix.ffi.DragDropEvent] for details."""

WebviewEventType = TypeAliasType(
    "WebviewEventType",
    WebviewEvent.DragDrop | WebviewEvent._NonExhaustive,
)
"""See [WebviewEvent][pytaurix.ffi.WebviewEvent] for details."""

WindowEventType = TypeAliasType(
    "WindowEventType",
    WindowEvent.Resized
    | WindowEvent.Moved
    | WindowEvent.CloseRequested
    | WindowEvent.Destroyed
    | WindowEvent.Focused
    | WindowEvent.ScaleFactorChanged
    | WindowEvent.DragDrop
    | WindowEvent.ThemeChanged
    | WindowEvent._NonExhaustive,
)
"""See [WindowEvent][pytaurix.ffi.WindowEvent] for details."""

ImplManager = TypeAliasType("ImplManager", Union[App, AppHandle, "WebviewWindow"])

EventId = NewType("EventId", int)
"""[tauri::EventId](https://docs.rs/tauri/latest/tauri/type.EventId.html)"""

ImplListener = ImplManager

PositionType = TypeAliasType("PositionType", Position.Physical | Position.Logical)
"""See [Position][pytaurix.ffi.Position] for details."""

SizeType = TypeAliasType("SizeType", Size.Physical | Size.Logical)
"""See [Size][pytaurix.ffi.Size] for details."""


class Assets(ABC):
    """[tauri::Assets](https://docs.rs/tauri/latest/tauri/trait.Assets.html)

    This is an abstract class that you can subclass to implement a custom asset loader.

    See `tauri::Assets` rust docs for more details.

    !!! warning
        The implement has the same restrictions as [App.run][pytaurix.App.run].
    """

    @abstractmethod
    def get(self, key: _AssetKey, /) -> bytes | None: ...
    @abstractmethod
    def iter(self, /) -> Iterator[tuple[str, bytes]]: ...

    # TODO: `def csp_hashes`
    # blocked by: <https://github.com/tauri-apps/tauri/issues/12756>

    def setup(self, _app: AppHandle, /) -> object:
        return None


Url = TypeAliasType("Url", str)
"""[tauri::Url](https://docs.rs/tauri/latest/tauri/struct.Url.html#method.parse)"""

ImplEmitter = ImplManager

EventTargetType = TypeAliasType(
    "EventTargetType",
    EventTarget.Any
    | EventTarget.AnyLabel
    | EventTarget.App
    | EventTarget.Window
    | EventTarget.Webview
    | EventTarget.WebviewWindow
    | EventTarget._NonExhaustive,
)
"""See [EventTarget][pytaurix.ffi.EventTarget] for details."""

WebviewUrlType = TypeAliasType(
    "WebviewUrlType",
    WebviewUrl.External
    | WebviewUrl.App
    | WebviewUrl.CustomProtocol
    | WebviewUrl._NonExhaustive,
)
"""See [WebviewUrl][pytaurix.ffi.WebviewUrl] for details."""
