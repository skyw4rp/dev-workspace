"""Tests for workspace dev launcher helpers."""

from __future__ import annotations

import run_melomanos as launcher


def test_backend_command_uses_current_interpreter() -> None:
    cmd = launcher._backend_command()
    assert len(cmd) == 2
    assert cmd[1] == "run.py"


def test_backend_start_env_disables_reload() -> None:
    env = launcher._backend_start_env()
    assert env["APP_RELOAD"] == "false"
    assert env["APP_HOST"] == "127.0.0.1"
    assert env["APP_PORT"] == "8000"


def test_stale_ports_include_frontend_fallback() -> None:
    assert 3001 in launcher.STALE_PORTS
    assert 8000 in launcher.STALE_PORTS


def test_build_local_cors_origins_includes_lan_ip() -> None:
    origins = launcher.build_local_cors_origins(lan_ip="192.168.1.81").split(",")
    assert "http://192.168.1.81:3000" in origins
    assert "http://[::1]:3000" in origins


def test_backend_start_env_includes_cors() -> None:
    env = launcher._backend_start_env()
    assert "CORS_ORIGINS" in env
    assert "http://localhost:3000" in env["CORS_ORIGINS"]
    assert env["CORS_ALLOW_PRIVATE_NETWORK"] == "true"
