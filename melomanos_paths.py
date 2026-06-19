"""Central path resolution for Melomanos workspace scripts.

Paths resolve from environment variables first, then fall back to the
default layout under ``C:\\melomanos\\``. See README_PROJECT_LAYOUT.md.
"""

from __future__ import annotations

import os
from pathlib import Path

_MELOMANOS_ROOT = Path(r"C:\melomanos")
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
