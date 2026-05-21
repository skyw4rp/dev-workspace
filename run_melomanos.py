"""Start Melomanos backend and frontend together."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(r"C:\melomanos_market")
FRONTEND_DIR = Path(r"C:\melomanos-frontend")

BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:3000"


def start_process(command: list[str], cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(
        command,
        cwd=cwd,
        shell=sys.platform == "win32",
    )


def main() -> None:
    if not BACKEND_DIR.is_dir():
        print(f"Backend path not found: {BACKEND_DIR}")
        sys.exit(1)
    if not FRONTEND_DIR.is_dir():
        print(f"Frontend path not found: {FRONTEND_DIR}")
        sys.exit(1)

    print("Starting Melomanos...\n")
    print(f"Backend:\n{BACKEND_URL}\n")
    print(f"Frontend:\n{FRONTEND_URL}\n")
    print("Press CTRL+C to stop both.\n")

    backend_proc: subprocess.Popen | None = None
    frontend_proc: subprocess.Popen | None = None

    try:
        backend_proc = start_process(["py", "run.py"], BACKEND_DIR)
        frontend_proc = start_process(["npm", "run", "dev"], FRONTEND_DIR)

        input("Melomanos is running. Press Enter to stop...\n")
    except KeyboardInterrupt:
        print("\nStopping Melomanos...")
    finally:
        for proc in (frontend_proc, backend_proc):
            if proc is None:
                continue
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
        print("Melomanos stopped.")


if __name__ == "__main__":
    main()
