#!/usr/bin/env bash
pnpm pyright --verifytypes codelldb --ignoreexternal && \
pnpm pyright --verifytypes pyfuture --ignoreexternal && \
pnpm pyright --verifytypes pyo3_utils --ignoreexternal && \
pnpm pyright --verifytypes pytaurix --ignoreexternal && \
pnpm pyright --verifytypes pytaurix.plugins --ignoreexternal && \
pnpm pyright --verifytypes pytaurix_utils --ignoreexternal && \
pnpm pyright --verifytypes pytaurix_wheel --ignoreexternal
