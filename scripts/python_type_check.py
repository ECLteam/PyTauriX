"""在所有开发平台上执行完整 Python 类型检查。"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    """在当前 uv 虚拟环境中运行 Pyright。"""
    pnpm = "pnpm.cmd" if sys.platform == "win32" else "pnpm"
    return subprocess.run([pnpm, "pyright", "."], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
