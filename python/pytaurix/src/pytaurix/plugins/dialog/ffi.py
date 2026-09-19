# ruff: noqa: D102, D106

"""Original FFI interface module.

!!! warning
    All APIs under this module should not be considered stable.
    You should use the re-exported APIs under the top-level module.
"""

from collections.abc import Callable, Sequence
from enum import Enum, auto
from types import ModuleType
from typing import TYPE_CHECKING, Self, TypeAlias, final

from typing_extensions import TypeAliasType, TypedDict, Unpack

from pytaurix import ImplManager
from pytaurix.ffi._typing import Pyo3PathFrom, Pyo3PathInto
from pytaurix.plugin import Plugin
from pytaurix.plugins import (
    PLUGIN_DIALOG,
    _pytaurix_plugins_mod,  # pyright: ignore[reportPrivateUsage]
)
from pytaurix.webview import WebviewWindow

__all__ = [
    "DialogExt",
    "FileDialogBuilder",
    "FileDialogBuilderArgs",
    "FilePath",
    "ImplDialogExt",
    "MessageDialogBuilder",
    "MessageDialogBuilderArgs",
    "MessageDialogButtons",
    "MessageDialogButtonsType",
    "MessageDialogKind",
    "init",
]

if PLUGIN_DIALOG:
    _dialog_mod: ModuleType = _pytaurix_plugins_mod.dialog
else:
    raise ImportError(
        "Enable the `plugin-dialog` feature for `pytaurix` crate to use this plugin."
    )

_HasWindowHandleAndHasDisplayHandle: TypeAlias = WebviewWindow

# TODO: unify this type with [tauri_plugin_fs::FilePath]
# NOTE: In the future, we may use `Union[str, Path]` to distinguish between Union[FilePath::Url, FilePath::Path],
#       so we use `Pyo3PathInto` instead of `Pyo3PathFrom` here.
FilePath = TypeAliasType("FilePath", Pyo3PathInto)
"""[tauri_plugin_dialog::FilePath](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/enum.FilePath.html)"""

if TYPE_CHECKING:

    def init() -> Plugin:
        """[tauri_plugin_dialog::init](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/fn.init.html)"""
        ...

    @final
    class MessageDialogButtons:
        """[tauri_plugin_dialog::MessageDialogButtons](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/enum.MessageDialogButtons.html)"""

        @final
        class Ok: ...

        @final
        class OkCancel: ...

        @final
        class YesNo: ...

        @final
        class OkCustom(tuple[str]):
            _0: str
            __match_args__ = ("_0",)

            def __new__(cls, _0: str, /) -> Self: ...

        @final
        class OkCancelCustom(tuple[str, str]):
            _0: str
            _1: str
            __match_args__ = ("_0", "_1")

            def __new__(cls, _0: str, _1: str, /) -> Self: ...

        # When adding new variants, remember to update `MessageDialogButtonsType`.

    class MessageDialogKind(Enum):
        """[tauri_plugin_dialog::MessageDialogKind](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/enum.MessageDialogKind.html)"""

        Info = auto()
        Warning = auto()
        Error = auto()

    @final
    class MessageDialogBuilder:
        """[tauri_plugin_dialog::MessageDialogBuilder](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/struct.MessageDialogBuilder.html)"""

        def blocking_show(
            self, /, **kwargs: Unpack["MessageDialogBuilderArgs"]
        ) -> bool: ...

        def show(
            self,
            handler: Callable[[bool], object],
            /,
            **kwargs: Unpack["MessageDialogBuilderArgs"],
        ) -> None: ...

    class FileDialogBuilder:
        """[tauri_plugin_dialog::FileDialogBuilder](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/struct.FileDialogBuilder.html)"""

        def pick_file(
            self,
            handler: Callable[[FilePath | None], object],
            /,
            **kwargs: Unpack["FileDialogBuilderArgs"],
        ) -> None: ...

        def blocking_pick_file(
            self, /, **kwargs: Unpack["FileDialogBuilderArgs"]
        ) -> FilePath | None: ...

        def pick_files(
            self,
            handler: Callable[[list[FilePath] | None], object],
            /,
            **kwargs: Unpack["FileDialogBuilderArgs"],
        ) -> None: ...

        def blocking_pick_files(
            self, /, **kwargs: Unpack["FileDialogBuilderArgs"]
        ) -> list[FilePath] | None: ...

        def pick_folder(
            self,
            handler: Callable[[FilePath | None], object],
            /,
            **kwargs: Unpack["FileDialogBuilderArgs"],
        ) -> None: ...

        def blocking_pick_folder(
            self, /, **kwargs: Unpack["FileDialogBuilderArgs"]
        ) -> FilePath | None: ...

        def pick_folders(
            self,
            handler: Callable[[list[FilePath] | None], object],
            /,
            **kwargs: Unpack["FileDialogBuilderArgs"],
        ) -> None: ...

        def blocking_pick_folders(
            self, /, **kwargs: Unpack["FileDialogBuilderArgs"]
        ) -> list[FilePath] | None: ...

        def save_file(
            self,
            handler: Callable[[FilePath | None], object],
            /,
            **kwargs: Unpack["FileDialogBuilderArgs"],
        ) -> None: ...

        def blocking_save_file(
            self, /, **kwargs: Unpack["FileDialogBuilderArgs"]
        ) -> FilePath | None: ...

    @final
    class DialogExt:
        """[tauri_plugin_dialog::DialogExt](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/trait.DialogExt.html)"""

        @staticmethod
        def message(slf: "ImplDialogExt", message: str, /) -> MessageDialogBuilder: ...
        @staticmethod
        def file(slf: "ImplDialogExt", /) -> FileDialogBuilder: ...

else:
    init = _dialog_mod.init
    MessageDialogButtons = _dialog_mod.MessageDialogButtons
    MessageDialogKind = _dialog_mod.MessageDialogKind
    MessageDialogBuilder = _dialog_mod.MessageDialogBuilder
    FileDialogBuilder = _dialog_mod.FileDialogBuilder
    DialogExt = _dialog_mod.DialogExt

MessageDialogButtonsType = TypeAliasType(
    "MessageDialogButtonsType",
    MessageDialogButtons.Ok
    | MessageDialogButtons.OkCancel
    | MessageDialogButtons.YesNo
    | MessageDialogButtons.OkCustom
    | MessageDialogButtons.OkCancelCustom,
)
"""See [MessageDialogButtons][pytaurix.plugins.dialog.MessageDialogButtons] for details."""


class MessageDialogBuilderArgs(TypedDict, total=False):
    """[tauri_plugin_dialog::MessageDialogBuilder](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/struct.MessageDialogBuilder.html)"""

    title: str
    parent: _HasWindowHandleAndHasDisplayHandle
    buttons: MessageDialogButtonsType
    kind: MessageDialogKind


class FileDialogBuilderArgs(TypedDict, total=False):
    """[tauri_plugin_dialog::FileDialogBuilder](https://docs.rs/tauri-plugin-dialog/latest/tauri_plugin_dialog/struct.FileDialogBuilder.html)"""

    add_filter: tuple[str, Sequence[str]]
    """(name, extensions)"""
    set_directory: Pyo3PathFrom
    set_file_name: str
    set_parent: _HasWindowHandleAndHasDisplayHandle
    set_title: str
    set_can_create_directories: bool


ImplDialogExt: TypeAlias = ImplManager
"""The implementers of `DialogExt`."""
