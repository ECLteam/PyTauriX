<!-- Do not use any **relative link** and  **GitHub-specific syntax** ！-->
<!-- Do not rename or move the file -->

# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

## Environment setup

Make sure you have installed `Rust`, `Python`, `uv`, `Node.js`, `pnpm`, `tauri-cli` and Tauri Prerequisites as documented.

Also, you need `bash`. If you are on Windows, you can use [Git for Windows](https://gitforwindows.org/).

Fork the [PyTauriX repository](https://github.com/ECLteam/PyTauriX) on GitHub.

```bash
#!/bin/bash

# clone your fork locally
git clone git@github.com:your_name_here/PyTauriX.git
cd PyTauriX
# create a branch for local development
git checkout -b branch-name

# install dev dependencies and build frontend assets
pnpm install
pnpm -r run build

# activate virtual environment
uv venv --python-preference=only-system
source .venv/bin/activate
# or Windows: `source .venv/Scripts/activate`

# install dev dependencies and tools
uv sync

# Init pre-commit (installed by `uv sync`)
# https://pre-commit.com/#3-install-the-git-hook-scripts
pre-commit install
pre-commit run --all-files
```

That's all! Now, you can start to develop.

## IDE setup

We strongly recommend using `VSCode` with the extensions in `.vscode/extensions.json`.

These extensions will help you to format, lint, type-check, and debug your code.

### Debug

TODO

- check `.vscode/launch.json` and [codelldb][] for debugging `py/rs` from python.
- check [vscode/python-debugging](https://code.visualstudio.com/docs/python/debugging#_debugging-by-attaching-over-a-network-connection) for debugging `py/rs` from rust.

## Source code

- **python**: members in `/pyproject.toml`
- **rust**: menbers in `/Cargo.toml`
- **frontend**: members in `/package.json`

## Testing

We use [pytest](https://docs.pytest.org/en/stable/) and `cargo test` to test our code.

## Documentation

### Python and Toturial

We use [mkdocs](https://www.mkdocs.org), [mkdocs-material](https://squidfunk.github.io/mkdocs-material) and [mkdocstrings](https://mkdocstrings.github.io) to build our documentation.

The documentation source code is in `docs/`, `docs/snippets/`, `docs/scripts/`, and `mkdocs.yml`.

Live-reloading main docs:

```bash
mkdocs serve  # --dirty # 👈 optional to speed up hot-reload
```

!!! tip "Docs references"
    - [mkdocs/getting-started](https://www.mkdocs.org/getting-started/)
    - [mkdocs-material/getting-started](https://squidfunk.github.io/mkdocs-material/getting-started/)
    - [mkdocstrings/usage](https://mkdocstrings.github.io/python/usage/)

!!! tip
    We use `Google` style to write python docstrings, please refer to:

    - [mkdocstrings-python's documentation](https://mkdocstrings.github.io/python/usage/docstrings/google/)
    - [Napoleon's documentation](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
    - [Griffe's documentation](https://mkdocstrings.github.io/griffe/docstrings/)

### Rust

```bash
cargo doc
```

### Frontend

TODO

## PR

- PRs should target the `main` branch.
- Keep branches up to date by `rebase` before merging.
- Do not add multiple unrelated things in same PR.
- Do not submit PRs where you just take existing lines and reformat them without changing what they do.
- Do not change other parts of the code that are not yours for formatting reasons.
- Do not use your clone's main branch to make a PR - create a branch and PR that.

### Edit `CHANGELOG.md`

If you have made the corresponding changes, please record them in `CHANGELOG.md`.

### Commit message convention

Commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/),
or `pre-commit` will reject your commit.

!!! info
    If you don't know how to finish these, it's okay, feel free to initiate a PR, we will help you continue.

## CI checks

We will check your commits on GitHub Actions, and your PR will only be merged if it passes the CI checks.

You can run these checks locally by executing `pre-commit run --all-files` in **bash**.

> Usually, you don't need to do this manually, because `pre-commit` will automatically run these checks on each commit as long as you have installed the git hooks via `pre-commit install`.

!!! tip
    Some slow checks are not run locally by default. If you really want to run them, pass `--hook-stage=manual`. You can also look at `.pre-commit-config.yaml` and run the individual checks yourself if you prefer.

---

## 😢

!!! warning
    The following 👇 content is for the maintainers of this project, may be you don't need to read it.

---

## 发布与部署

当前项目仅保留本地构建与验证流程；不配置自动文档部署、包发布或 GitHub Release 自动化。
