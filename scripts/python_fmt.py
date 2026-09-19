"""在所有开发平台上执行 Python 自动检查与格式化。"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    """依次执行 Ruff 检查和格式化。"""
    commands = (
        (sys.executable, "-m", "ruff", "check", ".", "--fix"),
        (sys.executable, "-m", "ruff", "format", "."),
    )
    for command in commands:
        if subprocess.run(command, check=False).returncode:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
