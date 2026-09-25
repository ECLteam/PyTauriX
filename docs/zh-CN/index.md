# PyTauriX 中文文档

PyTauriX 是独立维护的 PyTauri fork，为 Python 提供稳定桌面端 Tauri 2.11
绑定。当前版本是内部预览版 `0.1.0-alpha.N`，目标平台为 Windows、macOS、Linux，
Python 最低版本为 3.11。

## 当前边界

- 不兼容 PyTauri 0.8；旧 `pytauri` 导入不会被悄悄重导出。
- 仅支持稳定桌面 API；移动端和 Tauri `unstable` API 延后。
- 低层 API 位于 `pytaurix.raw`，Pythonic 生命周期 API 位于 `pytaurix`；插件通过
  `pytaurix.plugins.<name>`、Cargo feature 与 `AppBuilder.plugin(...)` 显式启用。
- alpha 仅通过 GitHub Release 工件或内部索引分发，不发布到公共包注册表。

## 快速开始

1. 使用 Python 3.11+、Rust 1.83+，并安装与 Tauri 对应的系统依赖。
2. 以仓库中的 `examples/tauri-app` 为起点，先执行前端依赖安装，再在 VS Developer
   Command Prompt（Windows）或对应平台工具链中运行 Tauri 开发命令。
3. 每次升级后先运行项目的锁定集成测试：

   ```powershell
   uv run --package pytaurix-test --no-dev cargo test -p pytaurix-test --features test --locked
   ```

## 文档导航

- [核心能力清单](capability-matrix.md)
- [Alpha 能力清单与发布门槛](../roadmap.md)
- [从 PyTauri 0.8 迁移](../migration-from-pytauri-0.8.md)
- [英文文档入口](../en/index.md)

英文文档保留完整的教程、示例和自动生成 API 参考。中文入口会优先维护架构、版本、
兼容性、发布与安全边界等对使用决策最关键的信息。
