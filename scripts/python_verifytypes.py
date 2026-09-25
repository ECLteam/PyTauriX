"""在所有开发平台上执行 Python 公共类型接口检查。"""

from __future__ import annotations

import subprocess
import sys

PACKAGES = (
    "pyfuture",
    "pyo3_utils",
    "pytaurix",
    "pytaurix.plugins",
    "pytaurix_utils",
    "pytaurix_wheel",
)


def main() -> int:
    """用 Pyright 逐一验证公开包的类型信息。"""
    pnpm = "pnpm.cmd" if sys.platform == "win32" else "pnpm"
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    for package in PACKAGES:
        if subprocess.run(
            [
                pnpm,
                "pyright",
                "--pythonversion",
                python_version,
                "--verifytypes",
                package,
                "--ignoreexternal",
            ],
            check=False,
        ).returncode:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
