"""在所有开发平台上执行 Python 测试。"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    """运行 pyfuture 的测试与覆盖率报告。"""
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "python/pyfuture/tests/",
            "--cov",
            "--cov-report=xml",
            "--cov-report=html",
        ],
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
