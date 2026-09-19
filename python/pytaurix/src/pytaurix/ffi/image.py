# ruff: noqa: D102

"""[tauri::image](https://docs.rs/tauri/latest/tauri/image/index.html)"""

from typing import (
    TYPE_CHECKING,
    Self,
)

from pytaurix.ffi._ext_mod import pytaurix_mod

__all__ = [
    "Image",
]

_image_mod = pytaurix_mod.image

if TYPE_CHECKING:

    class Image:
        """[tauri::image::Image](https://docs.rs/tauri/latest/tauri/image/struct.Image.html)"""

        def __new__(cls, rgba: bytes, width: int, height: int, /) -> Self: ...
        @property
        def rgba(self) -> bytes: ...
        @property
        def width(self) -> int: ...
        @property
        def height(self) -> int: ...

else:
    Image = _image_mod.Image
