"""Update PROJECT_STATUS.md sections via markers (stdlib only)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

STATUS_FILE = Path(__file__).resolve().parent / "PROJECT_STATUS.md"

MARKER_LAST_QG_START = "<!-- STATUS:LAST_QUALITY_GATE_START -->"
MARKER_LAST_QG_END = "<!-- STATUS:LAST_QUALITY_GATE_END -->"
MARKER_LATEST_RELEASE_START = "<!-- STATUS:LATEST_RELEASE_START -->"
MARKER_LATEST_RELEASE_END = "<!-- STATUS:LATEST_RELEASE_END -->"


def _replace_between_markers(
    content: str,
    start_marker: str,
    end_marker: str,
    body: str,
) -> str:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise ValueError(
            f"Missing or invalid markers in {STATUS_FILE.name}: "
            f"{start_marker!r} / {end_marker!r}",
        )
    insert_at = start_idx + len(start_marker)
    return content[:insert_at] + "\n" + body.rstrip() + "\n" + content[end_idx:]


def _release_line(committed: bool, message: str) -> str:
    if committed and message.strip():
        return message.strip()
    return "No changes."


def build_last_quality_gate_section(
    *,
    timestamp: str | None = None,
    backend_tests: str = "PASSED",
    frontend_build: str = "PASSED",
    e2e_tests: str = "PASSED",
    full_audit: str = "PASSED",
) -> str:
    when = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""## Last Quality Gate

- Date: {when}
- Backend tests: {backend_tests}
- Frontend build: {frontend_build}
- E2E tests: {e2e_tests}
- Full audit: {full_audit}"""


def build_latest_release_section(
    *,
    backend_line: str,
    frontend_line: str,
    timestamp: str | None = None,
) -> str:
    when = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""## Latest Release

- Backend: {backend_line}
- Frontend: {frontend_line}
- Quality Gate: PASSED
- Date: {when}"""


def update_project_status(
    *,
    backend_committed: bool,
    backend_message: str,
    frontend_committed: bool,
    frontend_message: str,
    timestamp: str | None = None,
) -> None:
    if not STATUS_FILE.is_file():
        raise FileNotFoundError(f"Status file not found: {STATUS_FILE}")

    when = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")
    content = STATUS_FILE.read_text(encoding="utf-8")

    qg_body = build_last_quality_gate_section(timestamp=when)
    release_body = build_latest_release_section(
        backend_line=_release_line(backend_committed, backend_message),
        frontend_line=_release_line(frontend_committed, frontend_message),
        timestamp=when,
    )

    content = _replace_between_markers(
        content,
        MARKER_LAST_QG_START,
        MARKER_LAST_QG_END,
        qg_body,
    )
    content = _replace_between_markers(
        content,
        MARKER_LATEST_RELEASE_START,
        MARKER_LATEST_RELEASE_END,
        release_body,
    )

    STATUS_FILE.write_text(content, encoding="utf-8", newline="\n")
