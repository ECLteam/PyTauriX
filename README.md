<!-- 中文项目入口；内容会由 docs/index.md 嵌入。 -->
<!-- 请仅使用绝对链接，确保 GitHub 与 MkDocs 的渲染一致。 -->

# PyTauriX

PyTauriX 是独立维护的 Python Tauri 桌面应用框架。它通过 [PyO3] 将 Python
应用、Tauri 运行时和 TypeScript 前端桥接在一起。

## 文档与状态

- [中文文档](https://github.com/ECLteam/PyTauriX/tree/main/docs)：项目主入口、使用说明与开发文档。
- [英文文档](https://github.com/ECLteam/PyTauriX/tree/main/docs/en)：英文入口；教程和 API 参考位于 `docs/usage/` 与 `docs/reference/`。
- [能力清单与开发计划](https://github.com/ECLteam/PyTauriX/blob/main/docs/roadmap.md)

## 项目结构

- `crates/`：Rust 组件、Tauri 插件和底层绑定。
- `python/`：Python 发行包与构建工具。
- `docs/`：中英文文档、文档示例片段与本地 API 参考生成器。
- `examples/`：可独立运行的应用示例。
- `scripts/`：开发检查与测试入口。
- `tests/`：跨 Python、Rust 与 Tauri 的集成测试。

## 开始使用

请使用 Python 3.11+ 与 Rust 1.83+。开发本仓库时，先安装锁定依赖，再运行集成测试：

```powershell
uv run --package pytaurix-test --no-dev cargo test -p pytaurix-test --features test --locked
```

低层、接近 Tauri 的接口位于 `pytaurix.raw`；Python 风格的生命周期和资源管理接口位于
`pytaurix`；插件使用 `pytaurix.plugins.<name>` 并以 Cargo 特性与
`AppBuilder.plugin(...)` 显式启用。

## 开源与归属

项目使用 Apache-2.0 许可证；其开发来源说明见
[UPSTREAM.md](https://github.com/ECLteam/PyTauriX/blob/main/UPSTREAM.md)。
Tauri 是 Commons Conservancy 下 Tauri Program 的商标；PyTauriX 为独立社区项目，
并未获得 Tauri 官方背书或支持。

[PyO3]: https://github.com/PyO3/pyo3
