"""Run Melomanos backend tests, frontend build, and E2E audit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BACKEND = Path(r"C:\melomanos_market")
FRONTEND = Path(r"C:\melomanos-frontend")

STEPS = [
    {
        "title": "[1/3] Backend tests",
        "command": ["py", "-m", "pytest"],
        "cwd": BACKEND,
    },
    {
        "title": "[2/3] Frontend build",
        "command": ["npm", "run", "build"],
        "cwd": FRONTEND,
    },
    {
        "title": "[3/3] Playwright E2E",
        "command": ["npm", "run", "test:e2e"],
        "cwd": FRONTEND,
    },
]


def run_step(title: str, command: list[str], cwd: Path) -> None:
    print(f"\n{title}\n")
    print(f"  cwd: {cwd}")
    print(f"  cmd: {' '.join(command)}\n")

    if not cwd.is_dir():
        print(f"ERROR: Project path not found: {cwd}")
        sys.exit(1)

    result = subprocess.run(
        command,
        cwd=cwd,
        shell=sys.platform == "win32",
    )

    if result.returncode != 0:
        print(f"\nERROR: {title} failed (exit code {result.returncode})")
        sys.exit(result.returncode)


def main() -> None:
    print("Melomanos audit\n")

    for step in STEPS:
        run_step(step["title"], step["command"], step["cwd"])

    print("\n================================")
    print("Melomanos audit passed")
    print("================================\n")


if __name__ == "__main__":
    main()
