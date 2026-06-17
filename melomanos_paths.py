"""Central path resolution for Melomanos workspace scripts.

Paths resolve from environment variables first, then fall back to the
current (pre-migration) layout. See README_PROJECT_LAYOUT.md.
"""

from __future__ import annotations

import os
from pathlib import Path

_DEFAULT_BACKEND = Path(r"C:\melomanos_market")
_DEFAULT_FRONTEND = Path(r"C:\melomanos-frontend")
_DEFAULT_WORKSPACE = Path(r"C:\melomanos_workspace")


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
