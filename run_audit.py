"""Run Melomanos backend tests, frontend build, and E2E audit."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from melomanos_paths import BACKEND_DIR, FRONTEND_DIR, PYTHON_EXECUTABLE, WORKSPACE_DIR
from run_melomanos import (
    BACKEND_HEALTH_URL,
    FRONTEND_URL,
    READY_POLL_INTERVAL_SEC,
    READY_TIMEOUT_SEC,
    is_url_ready,
)

BACKEND = BACKEND_DIR
FRONTEND = FRONTEND_DIR

BACKEND_PROBE_URLS = (
    "http://127.0.0.1:8000/health",
    BACKEND_HEALTH_URL,
)
MANUAL_STACK_CMD = "py run_melomanos.py --kill-stale --no-wait"

STEP_BACKEND = {
    "key": "backend",
    "title": "Backend tests",
    "command": [PYTHON_EXECUTABLE, "-m", "pytest"],
    "cwd": BACKEND,
}
STEP_FRONTEND_BUILD = {
    "key": "frontend_build",
    "title": "Frontend build",
    "command": ["npm", "run", "build"],
    "cwd": FRONTEND,
}
STEP_E2E = {
    "key": "e2e",
    "title": "Playwright E2E",
    "command": ["npm", "run", "test:e2e"],
    "cwd": FRONTEND,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Melomanos audit — tiered validation (backend, build, E2E).",
        epilog=(
            "Gate tiers:\n"
            "  Fast Gate       py run_audit.py --backend-only\n"
            "  Quality Gate    py run_audit.py --skip-e2e\n"
            "  Full audit      py run_audit.py  (auto-starts local stack for E2E if needed)\n"
            "  Release Gate    py finish_task.py  (runs full audit, then git release)\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--backend-only",
        action="store_true",
        help="Fast Gate: run backend pytest only (skip frontend build and E2E).",
    )
    mode.add_argument(
        "--skip-e2e",
        action="store_true",
        help="Quality Gate: run pytest and frontend build; skip Playwright E2E.",
    )
    return parser.parse_args()


def select_steps(args: argparse.Namespace) -> list[dict]:
    if args.backend_only:
        return [STEP_BACKEND]
    if args.skip_e2e:
        return [STEP_BACKEND, STEP_FRONTEND_BUILD]
    return [STEP_BACKEND, STEP_FRONTEND_BUILD, STEP_E2E]


def is_backend_ready() -> bool:
    return any(is_url_ready(url, timeout_sec=3.0) for url in BACKEND_PROBE_URLS)


def is_frontend_ready() -> bool:
    return is_url_ready(FRONTEND_URL, timeout_sec=3.0)


def wait_for_e2e_stack(*, timeout_sec: int = READY_TIMEOUT_SEC) -> bool:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if is_backend_ready() and is_frontend_ready():
            return True
        time.sleep(READY_POLL_INTERVAL_SEC)
    return False


def fail_e2e_prerequisites(reason: str) -> None:
    print(f"\nERROR: {reason}")
    print("\nE2E requires backend and frontend running:")
    print("  Backend:  http://127.0.0.1:8000")
    print("  Frontend: http://localhost:3000")
    print("\nStart the stack manually from the workspace directory:")
    print(f"  {MANUAL_STACK_CMD}")
    sys.exit(1)


def ensure_e2e_stack() -> None:
    """Ensure backend + frontend are up before Playwright; start stack if needed."""
    print("\nChecking E2E prerequisites...\n")

    backend_ok = is_backend_ready()
    frontend_ok = is_frontend_ready()

    if backend_ok:
        print("Backend READY")
    if frontend_ok:
        print("Frontend READY")

    if backend_ok and frontend_ok:
        print("\nE2E prerequisites READY\n")
        return

    print("\nStarting local stack for E2E...\n")

    if not WORKSPACE_DIR.is_dir():
        fail_e2e_prerequisites(f"Workspace path not found: {WORKSPACE_DIR}")

    result = subprocess.run(
        [PYTHON_EXECUTABLE, "run_melomanos.py", "--kill-stale", "--no-wait"],
        cwd=WORKSPACE_DIR,
        shell=sys.platform == "win32",
    )
    if result.returncode != 0:
        fail_e2e_prerequisites(
            "Local stack failed to start (run_melomanos.py exited with an error)."
        )

    if not wait_for_e2e_stack(timeout_sec=READY_TIMEOUT_SEC):
        fail_e2e_prerequisites(
            f"Stack did not become ready within {READY_TIMEOUT_SEC}s after launch."
        )

    print("Backend READY")
    print("Frontend READY")
    print("\nE2E prerequisites READY\n")


def run_step(index: int, total: int, title: str, command: list[str], cwd: Path) -> None:
    label = f"[{index}/{total}] {title}"
    print(f"\n{label}\n")
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
        print(f"\nERROR: {label} failed (exit code {result.returncode})")
        sys.exit(result.returncode)


def main() -> None:
    args = parse_args()
    steps = select_steps(args)
    total = len(steps)

    if args.backend_only:
        print("Melomanos audit — Fast Gate (--backend-only)\n")
    elif args.skip_e2e:
        print("Melomanos audit — Quality Gate (--skip-e2e)\n")
    else:
        print("Melomanos audit — Full audit (pytest + build + E2E)\n")
        print(
            "Full audit auto-starts the local stack for E2E when backend and "
            "frontend are not already running.\n"
        )

    for index, step in enumerate(steps, start=1):
        if step["key"] == "e2e":
            ensure_e2e_stack()
        run_step(index, total, step["title"], step["command"], step["cwd"])

    print("\n================================")
    print("Melomanos audit passed")
    print("================================\n")


if __name__ == "__main__":
    main()
