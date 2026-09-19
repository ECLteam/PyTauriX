"""Pythonic application construction built on :mod:`pytaurix.raw`."""

from collections.abc import Callable, Sequence
from typing import Any

from pytaurix import raw

__all__ = ["Application"]


class Application:
    """Owns a Tauri context and builder until an application is built.

    This deliberately small wrapper keeps the complete low-level builder
    available through :attr:`builder`; it only centralizes the common Python
    lifecycle for applications that do not need custom Rust bootstrap code.
    """

    def __init__(self, context: raw.Context, builder: raw.Builder, /) -> None:
        """Store the low-level context and builder used by this application."""
        self.context = context
        self.builder = builder

    @classmethod
    def create(
        cls,
        *,
        context_factory: Callable[..., raw.Context] = raw.context_factory,
        builder_factory: Callable[..., raw.Builder] = raw.builder_factory,
        context_args: Sequence[Any] = (),
        builder_args: Sequence[Any] = (),
    ) -> "Application":
        """Creates an application from the configured extension factories."""
        return cls(context_factory(*context_args), builder_factory(*builder_args))

    def build(
        self,
        invoke_handler: Any,
        *,
        setup: Callable[[raw.AppHandle], None] | None = None,
        plugins: Sequence[Any] | None = None,
    ) -> raw.App:
        """Builds the application without hiding low-level builder options."""
        kwargs: dict[str, Any] = {"invoke_handler": invoke_handler}
        if setup is not None:
            kwargs["setup"] = setup
        if plugins is not None:
            kwargs["plugins"] = list(plugins)
        return self.builder.build(self.context, **kwargs)
