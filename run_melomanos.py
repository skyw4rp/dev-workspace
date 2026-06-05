"""Start Melomanos backend and frontend with readiness checks."""

from __future__ import annotations

import argparse
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BACKEND_DIR = Path(r"C:\melomanos_market")
FRONTEND_DIR = Path(r"C:\melomanos-frontend")

BACKEND_URL = "http://127.0.0.1:8000"
BACKEND_HEALTH_URL = "http://127.0.0.1:8000/listings?limit=1"
FRONTEND_URL = "http://localhost:3000"
FRONTEND_FALLBACK_URL = "http://localhost:3001"

BACKEND_PORT = 8000
FRONTEND_PORT = 3000
FRONTEND_FALLBACK_PORT = 3001

READY_TIMEOUT_SEC = 30
READY_POLL_INTERVAL_SEC = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Melomanos dev environment launcher (backend + frontend)."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check if backend and frontend are reachable; do not start.",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Start services, wait until ready, print READY, exit (leave processes running).",
    )
    parser.add_argument(
        "--kill-stale",
        action="store_true",
        help="Kill processes listening on ports 8000 and 3000 before starting.",
    )
    return parser.parse_args()


def start_process(command: list[str], cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(
        command,
        cwd=cwd,
        shell=sys.platform == "win32",
    )


def terminate_process(proc: subprocess.Popen | None) -> None:
    if proc is None or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)


def is_url_ready(url: str, *, timeout_sec: float = 5.0) -> bool:
    try:
        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout_sec) as response:
            return 200 <= response.status < 500
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False


def is_port_listening(port: int, host: str = "127.0.0.1") -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except OSError:
        return False


def wait_until_ready(label: str, url: str) -> bool:
    deadline = time.monotonic() + READY_TIMEOUT_SEC
    while time.monotonic() < deadline:
        if is_url_ready(url):
            print(f"{label} READY")
            return True
        time.sleep(READY_POLL_INTERVAL_SEC)
    print(f"{label} not ready after {READY_TIMEOUT_SEC}s ({url})")
    return False


def get_listening_pids(port: int) -> list[int]:
    """Return PIDs listening on a TCP port (Windows netstat)."""
    result = subprocess.run(
        ["netstat", "-ano"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode != 0:
        return []

    pids: set[int] = set()
    pattern = re.compile(rf":{port}\s")
    for line in result.stdout.splitlines():
        upper = line.upper()
        if "LISTENING" not in upper:
            continue
        if not pattern.search(line):
            continue
        parts = line.split()
        if not parts:
            continue
        try:
            pids.add(int(parts[-1]))
        except ValueError:
            continue
    return sorted(pids)


def kill_stale_on_ports(ports: list[int]) -> None:
    current_pid = os.getpid()
    for port in ports:
        for pid in get_listening_pids(port):
            if pid == current_pid:
                continue
            print(f"Killing stale process PID {pid} on port {port}")
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/F"],
                capture_output=True,
                shell=False,
            )


def check_readiness(*, strict_frontend_port: bool) -> bool:
    backend_ok = wait_until_ready("Backend", BACKEND_HEALTH_URL)
    frontend_ok = wait_until_ready("Frontend", FRONTEND_URL)
    if backend_ok and frontend_ok:
        print("Melomanos READY")
        return True

    if strict_frontend_port and not frontend_ok:
        if is_port_listening(FRONTEND_FALLBACK_PORT) and is_url_ready(
            FRONTEND_FALLBACK_URL
        ):
            print(
                "ERROR: Frontend is reachable on port 3001, not 3000. "
                "E2E expects http://localhost:3000. "
                "Re-run with --kill-stale to free port 3000."
            )
    print("Melomanos NOT READY")
    return False


def validate_paths() -> None:
    if not BACKEND_DIR.is_dir():
        print(f"Backend path not found: {BACKEND_DIR}")
        sys.exit(1)
    if not FRONTEND_DIR.is_dir():
        print(f"Frontend path not found: {FRONTEND_DIR}")
        sys.exit(1)


def print_urls() -> None:
    print()
    print(f"Backend:  {BACKEND_URL}")
    print(f"Frontend: {FRONTEND_URL}")
    print()


def main() -> None:
    args = parse_args()

    if args.check:
        print("Checking Melomanos readiness...\n")
        ok = check_readiness(strict_frontend_port=False)
        sys.exit(0 if ok else 1)

    validate_paths()

    if args.kill_stale:
        print("Clearing stale processes on ports 8000 and 3000...\n")
        kill_stale_on_ports([BACKEND_PORT, FRONTEND_PORT])
        time.sleep(1)

    print("Starting Melomanos...\n")
    print_urls()

    backend_proc: subprocess.Popen | None = None
    frontend_proc: subprocess.Popen | None = None
    keep_running = False

    try:
        backend_proc = start_process(["py", "run.py"], BACKEND_DIR)
        frontend_proc = start_process(["npm", "run", "dev"], FRONTEND_DIR)

        if not wait_until_ready("Backend", BACKEND_HEALTH_URL):
            sys.exit(1)

        if not wait_until_ready("Frontend", FRONTEND_URL):
            strict = not args.kill_stale
            if (
                strict
                and is_port_listening(FRONTEND_FALLBACK_PORT)
                and is_url_ready(FRONTEND_FALLBACK_URL)
            ):
                print(
                    "ERROR: Frontend started on port 3001 instead of 3000. "
                    "E2E expects http://localhost:3000. "
                    "Stop the process and re-run with --kill-stale."
                )
            sys.exit(1)

        print("Melomanos READY")
        print_urls()

        if args.no_wait:
            keep_running = True
            print("Automation mode: leaving backend and frontend running.")
            return

        print("Press CTRL+C or Enter to stop both.\n")
        try:
            input()
        except EOFError:
            print("\nEOF on input; waiting for CTRL+C...")
            while True:
                time.sleep(3600)
    except KeyboardInterrupt:
        print("\nStopping Melomanos...")
    finally:
        if not keep_running:
            terminate_process(frontend_proc)
            terminate_process(backend_proc)
            print("Melomanos stopped.")


if __name__ == "__main__":
    main()
