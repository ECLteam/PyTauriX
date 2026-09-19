"""Reject APIs removed by PyO3 0.29 before they reach compilation."""

from __future__ import annotations

import re
import sys
from pathlib import Path

FORBIDDEN = re.compile(
    r"FromPyObjectBound|extract_bound|Python::with_gil|\.allow_threads\(|"
    r"\.downcast_into::<|\.downcast::<"
)


def main() -> int:
    """Check Rust sources for PyO3 APIs removed in version 0.29."""
    matches: list[str] = []
    for path in Path(".").rglob("*.rs"):
        if "target" in path.parts:
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if FORBIDDEN.search(line):
                matches.append(f"{path}:{line_number}: {line}")

    if not matches:
        return 0

    print(
        "Found APIs removed by PyO3 0.29. Use the current PyO3 equivalents instead.",
        file=sys.stderr,
    )
    print("\n".join(matches), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
