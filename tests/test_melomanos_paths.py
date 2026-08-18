"""Tests for the Python interpreter resolver in melomanos_paths."""

from __future__ import annotations

import os
import sys

import pytest

import melomanos_paths as paths


def test_resolve_python_honors_explicit_override() -> None:
    previous = os.environ.get("MELOMANOS_PYTHON")
    os.environ["MELOMANOS_PYTHON"] = sys.executable
    try:
        assert paths.resolve_python() == sys.executable
    finally:
        if previous is None:
            os.environ.pop("MELOMANOS_PYTHON", None)
        else:
            os.environ["MELOMANOS_PYTHON"] = previous


def test_resolve_python_rejects_missing_override() -> None:
    previous = os.environ.get("MELOMANOS_PYTHON")
    os.environ["MELOMANOS_PYTHON"] = str(
        paths.WORKSPACE_DIR / "not-a-real-interpreter.exe"
    )
    try:
        with pytest.raises(RuntimeError):
            paths.resolve_python()
    finally:
        if previous is None:
            os.environ.pop("MELOMANOS_PYTHON", None)
        else:
            os.environ["MELOMANOS_PYTHON"] = previous


def test_python_executable_is_resolved_at_import_time() -> None:
    assert paths.PYTHON_EXECUTABLE
