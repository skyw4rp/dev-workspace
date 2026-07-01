"""Start Melomanos backend and frontend with readiness checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from melomanos_paths import BACKEND_DIR, FRONTEND_DIR, WORKSPACE_DIR

BACKEND_URL = "http://127.0.0.1:8000"
BACKEND_HEALTH_URL = "http://127.0.0.1:8000/health"
BACKEND_LISTINGS_PROBE_URL = "http://127.0.0.1:8000/listings?limit=1"
FRONTEND_URL = "http://localhost:3000"
FRONTEND_FALLBACK_URL = "http://localhost:3001"

BACKEND_PORT = 8000
FRONTEND_PORT = 3000
FRONTEND_FALLBACK_PORT = 3001
STALE_PORTS = (BACKEND_PORT, FRONTEND_PORT, FRONTEND_FALLBACK_PORT)

LOG_DIR = WORKSPACE_DIR / "logs"
BACKEND_LOG = LOG_DIR / "backend.log"
FRONTEND_LOG = LOG_DIR / "frontend.log"

BACKEND_LOGIN_URL = "http://127.0.0.1:8000/auth/login"
BROWSER_ORIGIN = "http://localhost:3000"
DEMO_LOGIN_EMAIL = "daniela.review@demo.melomanos.local"
DEMO_LOGIN_PASSWORD = "devpassword12"
DEMO_LOGIN_FALLBACK_EMAIL = "buyer@example.com"
UI_LOGIN_SPEC = "e2e/demo-daniela-login.spec.ts"

READY_TIMEOUT_SEC = 30
READY_POLL_INTERVAL_SEC = 2

LOCAL_CORS_BASE = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://[::1]:3000",
    "http://[::1]:3001",
)


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
        help="Kill processes listening on ports 8000, 3000, and 3001 before starting.",
    )
    parser.add_argument(
        "--e2e-webpay",
        action="store_true",
        help="Start backend with WebPay placeholder env (Phase 6 E2E).",
    )
    parser.add_argument(
        "--auto-migrate",
        action="store_true",
        help="Run `alembic upgrade head` when the database is behind migration head.",
    )
    parser.add_argument(
        "--skip-migration-check",
        action="store_true",
        help="Skip Alembic current-vs-head check (not recommended for local dev).",
    )
    parser.add_argument(
        "--skip-ui-login-smoke",
        action="store_true",
        help="On --check, skip Playwright UI login smoke (API + CORS smokes still run).",
    )
    return parser.parse_args()


def _backend_command() -> list[str]:
    return [sys.executable, "run.py"]


def _frontend_command() -> list[str]:
    if sys.platform == "win32":
        return ["cmd.exe", "/c", "npm", "run", "dev"]
    return ["npm", "run", "dev"]


def _backend_start_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = {
        "APP_RELOAD": "false",
        "APP_HOST": "127.0.0.1",
        "APP_PORT": str(BACKEND_PORT),
        "CORS_ORIGINS": build_local_cors_origins(),
        "CORS_ALLOW_PRIVATE_NETWORK": "true",
    }
    if extra:
        env.update(extra)
    return env


def local_lan_ip() -> str | None:
    """Best-effort primary LAN IPv4 (used for Next.js Network URL CORS)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return None


def build_local_cors_origins(*, lan_ip: str | None = None) -> str:
    """Dev CORS list: localhost, IPv6 loopback, and optional LAN IP for ports 3000/3001."""
    origins = list(LOCAL_CORS_BASE)
    ip = lan_ip if lan_ip is not None else local_lan_ip()
    if ip:
        origins.append(f"http://{ip}:3000")
        origins.append(f"http://{ip}:3001")
    return ",".join(origins)


def detect_frontend_url() -> tuple[str, int] | None:
    """Return the frontend URL/port that is actually serving HTTP."""
    if is_url_ready(FRONTEND_URL):
        return FRONTEND_URL, FRONTEND_PORT
    if is_url_ready(FRONTEND_FALLBACK_URL):
        return FRONTEND_FALLBACK_URL, FRONTEND_FALLBACK_PORT
    return None


def wait_for_frontend_url() -> tuple[str, int] | None:
    """Poll until the frontend responds on port 3000 or 3001."""
    deadline = time.monotonic() + READY_TIMEOUT_SEC
    while time.monotonic() < deadline:
        detected = detect_frontend_url()
        if detected:
            return detected
        time.sleep(READY_POLL_INTERVAL_SEC)
    return None


def tail_log(log_path: Path, *, lines: int = 40) -> None:
    if not log_path.is_file():
        print(f"(log file not found: {log_path})")
        return
    content = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not content:
        print(f"(log file empty: {log_path})")
        return
    print(f"--- tail {log_path} ---")
    for line in content[-lines:]:
        print(line)
    print(f"--- end {log_path.name} ---")


def start_logged_process(
    label: str,
    command: list[str],
    cwd: Path,
    log_path: Path,
    env: dict[str, str] | None = None,
    *,
    detached: bool = False,
) -> subprocess.Popen:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_handle = open(log_path, "w", encoding="utf-8", buffering=1)
    proc_env = os.environ.copy()
    if env:
        proc_env.update(env)

    popen_kwargs: dict = {
        "cwd": cwd,
        "env": proc_env,
        "stdout": log_handle,
        "stderr": subprocess.STDOUT,
        "shell": False,
    }
    if detached and sys.platform == "win32":
        popen_kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        )

    print(f"Starting {label}: {' '.join(command)}")
    print(f"  cwd={cwd}")
    print(f"  log={log_path}")
    return subprocess.Popen(command, **popen_kwargs)


def assert_process_running(
    proc: subprocess.Popen | None,
    label: str,
    log_path: Path,
) -> None:
    if proc is None:
        print(f"ERROR: {label} process was not started.")
        sys.exit(1)
    time.sleep(0.75)
    code = proc.poll()
    if code is not None:
        print(f"ERROR: {label} exited immediately with code {code}.")
        tail_log(log_path)
        sys.exit(1)


def start_process(
    command: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.Popen:
    """Legacy helper — prefer start_logged_process."""
    proc_env = os.environ.copy()
    if env:
        proc_env.update(env)
    return subprocess.Popen(
        command,
        cwd=cwd,
        shell=False,
        env=proc_env,
    )


def webpay_e2e_env() -> dict[str, str]:
    return {
        "PAYMENT_PROVIDER_MODE": "webpay_placeholder",
        "WEBPAY_CALLBACK_SECRET": "e2e-webpay-callback-secret",
        "WEBPAY_RETURN_URL_BASE": "http://localhost:3000/orders",
    }


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


def local_dev_env() -> dict[str, str]:
    """Env vars injected into frontend dev server for consistent API routing."""
    return {
        "NEXT_PUBLIC_API_URL": BACKEND_URL,
    }


def ensure_frontend_env_local() -> None:
    """Create frontend/.env.local when missing so manual `npm run dev` hits local API."""
    path = FRONTEND_DIR / ".env.local"
    if path.is_file():
        return
    lines = [
        "# Created by run_melomanos.py — local API base (no trailing slash)",
        f"NEXT_PUBLIC_API_URL={BACKEND_URL}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created {path} with NEXT_PUBLIC_API_URL={BACKEND_URL}\n")


def _post_form(url: str, fields: dict[str, str], *, origin: str | None = None) -> tuple[int, str]:
    body = urllib.parse.urlencode(fields).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if origin:
        headers["Origin"] = origin
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=5.0) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def _header_get(headers: dict[str, str], name: str) -> str | None:
    target = name.lower()
    for key, value in headers.items():
        if key.lower() == target:
            return value
    return None


def _options_preflight(
    url: str,
    *,
    origin: str,
    private_network: bool = False,
) -> tuple[int, dict[str, str], str]:
    headers = {
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    }
    if private_network:
        headers["Access-Control-Request-Private-Network"] = "true"
    request = urllib.request.Request(url, method="OPTIONS", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=5.0) as response:
            hdrs = {k: v for k, v in response.headers.items()}
            return response.status, hdrs, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        hdrs = {k: v for k, v in exc.headers.items()}
        return exc.code, hdrs, exc.read().decode("utf-8", errors="replace")


def check_browser_cors_smoke() -> bool:
    """urllib CORS/PNA preflight — not a real browser UI test."""
    status, headers, body = _options_preflight(
        BACKEND_LOGIN_URL,
        origin=BROWSER_ORIGIN,
        private_network=True,
    )
    if status != 200:
        print(
            f"Browser CORS preflight FAILED: HTTP {status} {body.strip()} "
            f"(Origin: {BROWSER_ORIGIN} -> {BACKEND_URL})"
        )
        return False
    if _header_get(headers, "Access-Control-Allow-Private-Network") != "true":
        print(
            "Browser CORS preflight FAILED: missing Access-Control-Allow-Private-Network: true. "
            "Chrome blocks fetch from localhost:3000 to 127.0.0.1:8000 without it."
        )
        return False
    if _header_get(headers, "Access-Control-Allow-Origin") != BROWSER_ORIGIN:
        print(
            "Browser CORS preflight FAILED: "
            f"allow-origin={_header_get(headers, 'Access-Control-Allow-Origin')!r}"
        )
        return False

    status, body = _post_form(
        BACKEND_LOGIN_URL,
        {
            "username": DEMO_LOGIN_EMAIL,
            "password": DEMO_LOGIN_PASSWORD,
            "grant_type": "password",
        },
        origin=BROWSER_ORIGIN,
    )
    if status != 200:
        print(f"Browser login POST FAILED: HTTP {status} {body[:120]}")
        return False
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        print("Browser login POST FAILED: invalid JSON")
        return False
    if not payload.get("access_token"):
        print("Browser login POST FAILED: no access_token in response")
        return False
    print(
        f"Browser CORS smoke OK (urllib PNA preflight: {BROWSER_ORIGIN} -> {BACKEND_URL})"
    )
    return True


def check_api_login_smoke() -> bool:
    """Direct POST /auth/login without browser Origin (server-side smoke)."""
    for email in (DEMO_LOGIN_EMAIL, DEMO_LOGIN_FALLBACK_EMAIL):
        status, body = _post_form(
            BACKEND_LOGIN_URL,
            {
                "username": email,
                "password": DEMO_LOGIN_PASSWORD,
                "grant_type": "password",
            },
        )
        if status == 200:
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                print(f"Backend login smoke FAILED for {email}: invalid JSON")
                return False
            if payload.get("access_token"):
                print(f"API login smoke OK ({email})")
                return True
        if status == 401:
            continue
        print(f"API login smoke FAILED for {email}: HTTP {status} {body[:120]}")
        return False

    print(
        "API login smoke skipped: no demo user found "
        f"({DEMO_LOGIN_EMAIL} or {DEMO_LOGIN_FALLBACK_EMAIL}). "
        "Run: cd backend && py -m app.demo seed --size medium"
    )
    return True


def check_ui_login_playwright(*, frontend_url: str = FRONTEND_URL) -> bool:
    """Playwright E2E: Daniela demo login through the real login page UI."""
    spec_path = FRONTEND_DIR / "e2e" / "demo-daniela-login.spec.ts"
    if not spec_path.is_file():
        print(f"UI login smoke SKIPPED: missing {spec_path}")
        return True

    if not (FRONTEND_DIR / "node_modules" / "@playwright" / "test").is_dir():
        print(
            "UI login smoke SKIPPED: Playwright not installed "
            "(cd frontend && npm install && npx playwright install chromium)"
        )
        return True

    env = os.environ.copy()
    env["E2E_BASE_URL"] = frontend_url.rstrip("/")
    env["E2E_API_URL"] = BACKEND_URL

    cmd = (
        ["cmd.exe", "/c", "npx", "playwright", "test", UI_LOGIN_SPEC, "--reporter=line"]
        if sys.platform == "win32"
        else ["npx", "playwright", "test", UI_LOGIN_SPEC, "--reporter=line"]
    )

    print("UI login smoke: Playwright Daniela demo login (real browser UI)...")
    try:
        result = subprocess.run(
            cmd,
            cwd=FRONTEND_DIR,
            env=env,
            capture_output=True,
            text=True,
            shell=False,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        print("UI login smoke FAILED: Playwright timed out after 120s")
        return False

    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        print("UI login smoke FAILED: Daniela browser UI login did not pass")
        print("Re-run manually: cd frontend && npm run test:e2e:demo-login")
        return False

    print("UI login smoke OK (Playwright: Daniela demo login via browser UI)")
    return True


# Backward-compatible aliases for tests
check_demo_login = check_api_login_smoke
check_browser_login_cors = check_browser_cors_smoke


def wait_until_ready(label: str, url: str) -> bool:
    deadline = time.monotonic() + READY_TIMEOUT_SEC
    while time.monotonic() < deadline:
        if is_url_ready(url):
            print(f"{label} READY")
            return True
        time.sleep(READY_POLL_INTERVAL_SEC)
    print(f"{label} not ready after {READY_TIMEOUT_SEC}s ({url})")
    return False


def _pid_exists(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            capture_output=True,
            text=True,
            shell=False,
        )
        out = result.stdout.strip()
        return bool(out) and "No tasks are running" not in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def can_bind_port(host: str, port: int) -> bool:
    """True when the port can be bound (authoritative vs stale netstat rows on Windows)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
            return True
        except OSError:
            return False


def get_listening_pids(port: int) -> list[int]:
    """Return live PIDs listening on a TCP port (Windows netstat)."""
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
            pid = int(parts[-1])
        except ValueError:
            continue
        if _pid_exists(pid):
            pids.add(pid)
    return sorted(pids)


def kill_melomanos_frontend_processes_windows() -> None:
    """Stop Next.js dev servers started from the Melomanos frontend directory."""
    if sys.platform != "win32":
        return
    frontend_marker = str(FRONTEND_DIR).replace("\\", "\\\\")
    script = (
        "Get-CimInstance Win32_Process "
        "| Where-Object { "
        "$_.Name -eq 'node.exe' -and "
        f"$_.CommandLine -like '*{frontend_marker}*' "
        "} "
        "| ForEach-Object { "
        "Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue "
        "}"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        shell=False,
    )


def kill_melomanos_backend_processes_windows() -> None:
    """Stop uvicorn/reload orphan workers that hold port 8000 after the parent exits."""
    if sys.platform != "win32":
        return
    script = (
        "Get-CimInstance Win32_Process "
        "| Where-Object { "
        "$_.CommandLine -match 'run\\.py|app\\.main:app|uvicorn|multiprocessing\\.spawn' "
        "} "
        "| ForEach-Object { "
        "Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue "
        "}"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        shell=False,
    )


def kill_listeners_on_port_windows(port: int) -> None:
    """Stop processes bound to a port via Get-NetTCPConnection."""
    if sys.platform != "win32":
        return
    script = (
        f"$pids = Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue "
        "| Select-Object -ExpandProperty OwningProcess -Unique; "
        "foreach ($procId in $pids) { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue }"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        shell=False,
    )


def stop_existing_dev_servers() -> None:
    """Stop known dev ports before a fresh start."""
    kill_melomanos_backend_processes_windows()
    kill_melomanos_frontend_processes_windows()
    for port in STALE_PORTS:
        for pid in get_listening_pids(port):
            print(f"Killing PID {pid} on port {port}")
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                capture_output=True,
                shell=False,
            )
        kill_listeners_on_port_windows(port)
    time.sleep(1)


def wait_until_backend_stopped(*, timeout_sec: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if not is_url_ready(BACKEND_HEALTH_URL, timeout_sec=1.0):
            if can_bind_port("127.0.0.1", BACKEND_PORT):
                return True
        else:
            stop_existing_dev_servers()
        time.sleep(0.75)
    print("ERROR: Existing backend still responding on port 8000 after kill attempts.")
    return False


def wait_until_port_free(port: int, *, host: str = "127.0.0.1", timeout_sec: float = 20.0) -> bool:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if can_bind_port(host, port):
            return True
        time.sleep(0.5)
    remaining = get_listening_pids(port)
    print(
        f"Port {port} still in use"
        + (f" by PID(s): {remaining}" if remaining else " (netstat ghost or foreign process)")
    )
    return False


def kill_stale_on_ports(ports: list[int], *, max_rounds: int = 5) -> None:
    stop_existing_dev_servers()
    for round_idx in range(max_rounds):
        if all(can_bind_port("127.0.0.1", port) for port in ports):
            if not is_url_ready(BACKEND_HEALTH_URL, timeout_sec=1.0):
                return
        stop_existing_dev_servers()
        time.sleep(1)

    blocked: list[str] = []
    for port in ports:
        if not can_bind_port("127.0.0.1", port):
            pids = get_listening_pids(port)
            blocked.append(f"{port} -> {pids if pids else 'unidentified listener'}")
    if is_url_ready(BACKEND_HEALTH_URL, timeout_sec=1.0):
        blocked.append("8000 -> health probe still responds (stale uvicorn)")
    if blocked:
        print("ERROR: Could not free required ports:")
        for item in blocked:
            print(f"  {item}")
        print("Close Melómanos/uvicorn/Next.js manually and retry with --kill-stale.")
        print(f"See logs under {LOG_DIR} after a start attempt.")
        sys.exit(1)


def check_readiness(*, strict_frontend_port: bool, ui_login_smoke: bool = True) -> bool:
    backend_ok = check_backend_ready()
    detected = wait_for_frontend_url()
    if backend_ok and detected:
        url, port = detected
        print(f"Frontend READY ({url})")
        if ui_login_smoke:
            if not check_ui_login_playwright(frontend_url=url):
                print("Melomanos NOT READY")
                return False
        else:
            print("UI login smoke SKIPPED (--skip-ui-login-smoke)")
        if port != FRONTEND_PORT:
            print(
                f"NOTE: Frontend is on port {port}, not {FRONTEND_PORT}. "
                f"Open {url} in the browser."
            )
        else:
            print_browser_hint(url)
        print("Melomanos READY")
        return True

    if strict_frontend_port and detected is None:
        if is_port_listening(FRONTEND_FALLBACK_PORT) and is_url_ready(
            FRONTEND_FALLBACK_URL
        ):
            print(
                "ERROR: Frontend is reachable on port 3001, not 3000. "
                "E2E expects http://localhost:3000. "
                "Re-run with --kill-stale to free port 3000."
            )
        else:
            wait_until_ready("Frontend", FRONTEND_URL)
    elif detected is None:
        wait_until_ready("Frontend", FRONTEND_URL)
    print("Melomanos NOT READY")
    return False


def validate_paths() -> None:
    if not BACKEND_DIR.is_dir():
        print(f"Backend path not found: {BACKEND_DIR}")
        sys.exit(1)
    if not FRONTEND_DIR.is_dir():
        print(f"Frontend path not found: {FRONTEND_DIR}")
        sys.exit(1)


def ensure_database_migrations(
    *,
    auto_migrate: bool,
    skip_check: bool,
) -> None:
    """Abort (or auto-upgrade) when Postgres is behind Alembic head."""
    if skip_check:
        print("Skipping Alembic migration check (--skip-migration-check).\n")
        return

    script = BACKEND_DIR / "scripts" / "migration_status.py"
    if not script.is_file():
        print(f"WARNING: migration check script missing: {script}\n")
        return

    mode = "upgrade" if auto_migrate else "check"
    print(f"Checking Alembic migrations ({mode})...")
    cmd = [sys.executable, str(script), f"--{mode}"]
    result = subprocess.run(cmd, cwd=BACKEND_DIR, text=True, capture_output=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        if auto_migrate:
            print("ERROR: Auto-migrate failed. Fix Alembic/Postgres and retry.")
        else:
            print(
                "ERROR: Refusing to start — database migrations are not at Alembic head."
            )
            print(
                "Re-run with --auto-migrate to apply `alembic upgrade head` automatically."
            )
        sys.exit(1)
    print("Migrations OK (database at Alembic head).\n")


def check_backend_ready() -> bool:
    """Liveness, listings probe, API login smoke, and urllib CORS/PNA smoke."""
    health_ok = wait_until_ready("Backend /health", BACKEND_HEALTH_URL)
    if not health_ok:
        return False
    listings_ok = wait_until_ready("Backend /listings", BACKEND_LISTINGS_PROBE_URL)
    if not listings_ok:
        return False
    return check_api_login_smoke() and check_browser_cors_smoke()


def print_browser_hint(frontend_url: str = FRONTEND_URL) -> None:
    print(f"Open in browser: {frontend_url}/login")
    print("  (Use localhost - not the Next.js Network/LAN URL - for reliable login.)")


def print_urls(*, frontend_url: str = FRONTEND_URL) -> None:
    print()
    print(f"Backend:  {BACKEND_URL}")
    print(f"Frontend: {frontend_url}")
    print()


def main() -> None:
    args = parse_args()

    validate_paths()

    ensure_frontend_env_local()

    ensure_database_migrations(
        auto_migrate=args.auto_migrate,
        skip_check=args.skip_migration_check,
    )

    if args.check:
        print("Checking Melomanos readiness...\n")
        ok = check_readiness(
            strict_frontend_port=False,
            ui_login_smoke=not args.skip_ui_login_smoke,
        )
        sys.exit(0 if ok else 1)

    if args.kill_stale:
        print(f"Clearing stale processes on ports {', '.join(map(str, STALE_PORTS))}...\n")
        kill_stale_on_ports(list(STALE_PORTS))
        if not wait_until_backend_stopped():
            sys.exit(1)
        for port in (FRONTEND_PORT, FRONTEND_FALLBACK_PORT):
            if not wait_until_port_free(port):
                sys.exit(1)
        print("Ports cleared.\n")

    print("Starting Melomanos...\n")
    print_urls()

    backend_proc: subprocess.Popen | None = None
    frontend_proc: subprocess.Popen | None = None
    keep_running = False
    detached = args.no_wait

    try:
        backend_extra = webpay_e2e_env() if args.e2e_webpay else None
        if args.e2e_webpay:
            print("E2E WebPay mode: PAYMENT_PROVIDER_MODE=webpay_placeholder\n")
        backend_proc = start_logged_process(
            "backend",
            _backend_command(),
            BACKEND_DIR,
            BACKEND_LOG,
            env=_backend_start_env(backend_extra),
            detached=detached,
        )
        assert_process_running(backend_proc, "backend", BACKEND_LOG)

        frontend_proc = start_logged_process(
            "frontend",
            _frontend_command(),
            FRONTEND_DIR,
            FRONTEND_LOG,
            env=local_dev_env(),
            detached=detached,
        )
        assert_process_running(frontend_proc, "frontend", FRONTEND_LOG)

        if not check_backend_ready():
            print("ERROR: Backend readiness checks failed.")
            tail_log(BACKEND_LOG)
            sys.exit(1)

        assert_process_running(backend_proc, "backend", BACKEND_LOG)

        assert_process_running(backend_proc, "backend", BACKEND_LOG)

        detected = wait_for_frontend_url()
        if detected is None:
            print("ERROR: Frontend did not become ready.")
            tail_log(FRONTEND_LOG)
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

        frontend_url, frontend_port = detected
        print(f"Frontend READY ({frontend_url})")
        if frontend_port != FRONTEND_PORT:
            print(
                f"NOTE: Frontend bound to port {frontend_port} (3000 was busy). "
                f"Open {frontend_url} in the browser."
            )

        assert_process_running(frontend_proc, "frontend", FRONTEND_LOG)

        print("Melomanos READY")
        print_urls(frontend_url=frontend_url)
        print_browser_hint(frontend_url)
        print(f"Logs: {BACKEND_LOG} , {FRONTEND_LOG}")

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
