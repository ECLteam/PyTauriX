"""The tauri-app."""

from pytaurix import (
    builder_factory,
    context_factory,
)


def main() -> int:
    """Run the tauri-app."""
    app = builder_factory().build(
        context=context_factory(),
        invoke_handler=None,  # TODO
    )
    exit_code = app.run_return()
    return exit_code
