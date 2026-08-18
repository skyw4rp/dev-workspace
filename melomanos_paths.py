"""Central path resolution for Melomanos workspace scripts.

Paths resolve from environment variables first, then fall back to the
default layout under ``C:\\developments\\apps\\melomanos\\``. See README_PROJECT_LAYOUT.md.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

_MELOMANOS_ROOT = Path(r"C:\developments\apps\melomanos")
_DEFAULT_BACKEND = _MELOMANOS_ROOT / "backend"
_DEFAULT_FRONTEND = _MELOMANOS_ROOT / "frontend"
_DEFAULT_WORKSPACE = _MELOMANOS_ROOT / "workspace"


def _resolve_dir(env_var: str, default: Path) -> Path:
    value = os.environ.get(env_var, "").strip()
    if value:
        return Path(value).expanduser()
    return default


BACKEND_DIR = _resolve_dir("MELOMANOS_BACKEND_DIR", _DEFAULT_BACKEND)
FRONTEND_DIR = _resolve_dir("MELOMANOS_FRONTEND_DIR", _DEFAULT_FRONTEND)
WORKSPACE_DIR = _resolve_dir("MELOMANOS_WORKSPACE_DIR", _DEFAULT_WORKSPACE)

ROADMAP_FILE = BACKEND_DIR / "MVP_ROADMAP.md"
BACKEND_STATUS_FILE = BACKEND_DIR / "PROJECT_STATUS.md"
WORKSPACE_STATUS_FILE = WORKSPACE_DIR / "PROJECT_STATUS.md"


def _venv_python(venv_dir: Path) -> Path | None:
    scripts_subdir = "Scripts" if os.name == "nt" else "bin"
    exe_name = "python.exe" if os.name == "nt" else "python"
    candidate = venv_dir / scripts_subdir / exe_name
    return candidate if candidate.is_file() else None


def resolve_python() -> str:
    """Deterministically select the Python interpreter for backend/tooling subprocesses.

    Precedence: an explicit ``MELOMANOS_PYTHON`` override, then the
    project-local ``backend/venv``, then ``python3``/``python``/``py`` on
    PATH, then the interpreter currently running this process. No step
    depends on an undisclosed machine-specific path.
    """
    override = os.environ.get("MELOMANOS_PYTHON", "").strip()
    if override:
        if not Path(override).is_file():
            raise RuntimeError(
                f"MELOMANOS_PYTHON={override!r} does not point to an existing file."
            )
        return override

    venv_python = _venv_python(BACKEND_DIR / "venv")
    if venv_python is not None:
        return str(venv_python)

    for name in ("python3", "python", "py"):
        found = shutil.which(name)
        if found:
            return found

    return sys.executable


PYTHON_EXECUTABLE = resolve_python()
