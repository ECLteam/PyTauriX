<!-- This file is the Chinese project entry and is included by docs/index.md. -->
<!-- Use absolute links only: it is rendered by both GitHub and MkDocs. -->

# PyTauriX

PyTauriX 是独立维护的 Python Tauri 桌面应用框架。它通过 [PyO3] 将 Python
应用、Tauri 运行时和 TypeScript 前端桥接在一起。

## 文档与状态

- [中文文档](https://eclteam.github.io/PyTauriX/)：项目主入口、迁移说明与发布边界。
- [English documentation](https://eclteam.github.io/PyTauriX/en/)：完整英文说明与 API 参考。
- [能力清单与 Alpha 门槛](https://eclteam.github.io/PyTauriX/roadmap/)
- [从 PyTauri 0.8 迁移](https://eclteam.github.io/PyTauriX/migration-from-pytauri-0.8/)

## 项目结构

- `crates/`：Rust crate、Tauri 插件和底层绑定。
- `python/`：Python 发行包与构建工具。
- `docs/`：中英文文档；`docs/snippets/` 仅保存文档嵌入的示例片段。
- `examples/`：可独立运行的应用示例。
- `tests/`：跨 Python、Rust 与 Tauri 的集成测试。

## 开始使用

请使用 Python 3.11+ 与 Rust 1.83+。开发本仓库时，先安装锁定依赖，再运行集成测试：

```powershell
uv run --package pytaurix-test --no-dev cargo test -p pytaurix-test --features test --locked
```

低层、接近 Tauri 的接口位于 `pytaurix.raw`；Pythonic 生命周期和资源管理接口位于
`pytaurix`；插件使用 `pytaurix.plugins.<name>` 并以 Cargo feature 与
`AppBuilder.plugin(...)` 显式启用。

## 开源与归属

项目使用 Apache-2.0 许可证，并保留上游归属说明，详见
[UPSTREAM.md](https://github.com/ECLteam/PyTauriX/blob/main/UPSTREAM.md)。
Tauri 是 Commons Conservancy 下 Tauri Program 的商标；PyTauriX 为独立社区项目，
并未获得 Tauri 官方背书或支持。

[PyO3]: https://github.com/PyO3/pyo3
