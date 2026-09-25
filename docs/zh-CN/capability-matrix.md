# 核心能力清单

本清单以 Tauri `2.11.5` 的稳定桌面 API 为基线，记录 PyTauriX 当前
`pytaurix.raw` 绑定的实际状态。它不是功能宣传页：每一行都必须有源码与测试证据，
未被真实桌面测试覆盖的能力不得标为“已验证”。

## 状态定义

- **已验证**：存在公开绑定，且有对应 Rust 或 Python 集成测试。
- **已绑定，待验证**：存在公开绑定，但尚缺真实桌面场景测试。
- **待实现**：尚未发现稳定的公开 Python 映射。
- **风险项**：已有绑定，但异常、线程或平台语义尚不满足 alpha 门槛。

## 第一轮审计

| 垂直切片 | 状态 | 当前证据 | 下一步验收 |
| --- | --- | --- | --- |
| 应用、构建器、上下文与状态 | MockRuntime 回归通过；待原生桌面验证 | `Manager` 的首次/重复注册、`state`、`try_state` 与未注册错误由 `tests/pytaurix-test` 覆盖 | 三平台原生桌面启动、退出与重启测试 |
| 事件与应用生命周期 | 部分 MockRuntime 回归通过；待原生桌面验证 | `tests/pytaurix-test` 覆盖 `listen`、`once`、解除监听及监听回调异常交由 `sys.unraisablehook`；`RunEvent` 生命周期仍缺测试 | 三平台原生事件回调、窗口销毁后行为与应用生命周期测试 |
| IPC 与 Python 命令 | 已验证 | `Channel`、`Invoke`、`InvokeResolver` 绑定；`tests/pytaurix-test/tests/ipc.rs` 已通过真实 IPC | 补充异常、并发命令与取消场景 |
| 窗口与 WebView 基础生命周期 | 已绑定，待验证 | `WebviewWindow`、`Webview`、构建器及关闭/销毁、窗口事件绑定已存在 | 创建、隐藏、销毁、多窗口与回调线程测试 |
| 新窗口、下载、页面加载、资源请求、尺寸约束 | 待实现 | 当前公开类型中未发现 `on_download`、页面加载或资源请求回调、尺寸约束的稳定映射 | 以 Tauri 2.11.5 稳定接口逐项绑定并写桌面测试 |
| 菜单与托盘 | 已绑定，待验证 | `Menu`、菜单事件、`TrayIcon` 与托盘事件均有 Rust/Python 映射 | 菜单点击、托盘点击、动态更新及平台差异测试 |
| 路径、资源与权限 | 已绑定，待验证 | `PathResolver`、`Assets`、Tauri capability 文件已存在 | 资源目录与权限拒绝的三平台测试 |
| 图像与窗口外观 | 已绑定，待验证 | `Image`、窗口尺寸/位置、主题与效果类型已导出 | 图标、主题、DPI 与边界尺寸测试 |
| 插件注册基础 | 已绑定，待验证 | `Plugin`、`AppHandle.plugin` 和 `pytaurix.plugins` 已存在 | 首批五个插件的显式 feature 与注册测试 |
| 回调异常、GIL 与调度 | 风险项（部分缓解） | `Listener` 回调异常现在只交给 Python `sys.unraisablehook`，不会主动 panic；其它回调仍使用 `unwrap_unraisable_py_result`，且事件转换仍有 `expect` 路径 | 将相同边界安全策略扩展至 App、窗口/WebView、托盘和插件回调，并补 GIL/线程测试 |

## 实施顺序

1. 已完成“应用状态与事件”的 MockRuntime 回归基线；下一步补三平台原生桌面验证，并扩展回调边界安全处理。
2. 完成“窗口与 WebView 生命周期”切片，优先补齐新窗口、下载、页面加载、资源请求与尺寸约束。
3. 为菜单、托盘、路径、资源和权限补齐三平台烟雾测试。
4. 在核心门槛全部通过后，再逐个复审并启用 `updater`、`log`、`store`、`stronghold`、`cli`。

每次新增绑定必须同时更新本表、关联可运行示例，并加入至少一个可自动执行的测试。
