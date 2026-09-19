# Using Unreleased Commits

Since `v0.5`, all `pytaurix` packages support installation from a Git repository via branch, commit `SHA`, or PR (pull request).

## Install Rust crate from source

> ref: <https://doc.rust-lang.org/cargo/reference/overriding-dependencies.html#the-patch-section>

Append this to your `Cargo.toml` file:

```toml
[patch.crates-io]
pytaurix = { git = "https://github.com/ECLteam/PyTauriX.git", branch = "main" }
pytaurix-core = { git = "https://github.com/ECLteam/PyTauriX.git", branch = "main" }
tauri-plugin-pytaurix = { git = "https://github.com/ECLteam/PyTauriX.git", branch = "main" }
# other pytaurix dependencies which you need ...
```

This will force all your dependencies to use `pytaurix` from Git instead of `crates.io`.

## Install Python package from source

> ref: <https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-sources>

Append this to your `pyproject.toml` file:

```toml
[tool.uv.sources]
pytaurix = { git = 'https://github.com/ECLteam/PyTauriX.git', branch = "main", subdirectory = "python/pytaurix" }
# other pytaurix dependencies which you need ...
```

!!! tip
    You can check the `[tool.uv.workspace]` section in [pyproject.toml] to find the `subdirectory` for each package.

    [pyproject.toml]: https://github.com/ECLteam/PyTauriX/blob/main/pyproject.toml

## Install JS package from source

> Inspired by: <https://vite.dev/guide/#using-unreleased-commits>

Thanks to <https://pkg.pr.new/>, you can install JS package from specific branch, commit `SHA`, or PR with:

```bash
# or pnpm, yarn, bun, whatever
npm i https://pkg.pr.new/@pytaurix/api@main
```

!!! tip
    To replace the pytaurix version used by dependencies transitively, you should use [npm overrides] or [pnpm overrides].

    [npm overrides]: https://docs.npmjs.com/cli/v11/configuring-npm/package-json#overrides
    [pnpm overrides]: https://pnpm.io/settings#overrides
