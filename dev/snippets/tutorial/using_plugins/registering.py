from pytaurix import (
    builder_factory,
    context_factory,
)
from pytaurix.plugins import notification

app = builder_factory().build(
    context=context_factory(),
    invoke_handler=None,
    plugins=[notification.init()],  # 👈
)
