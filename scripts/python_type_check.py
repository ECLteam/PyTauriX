"""在所有开发平台上执行完整 Python 类型检查。"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    """按当前解释器版本运行 Pyright，避免误判新版标准库语法。"""
    pnpm = "pnpm.cmd" if sys.platform == "win32" else "pnpm"
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return subprocess.run(
        [pnpm, "pyright", "--pythonversion", python_version, "."], check=False
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
