"""Update PROJECT_STATUS.md sections via markers (stdlib only)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from melomanos_paths import WORKSPACE_STATUS_FILE
from governance_authority import (
    AuthorityError,
    load_authority,
    observe_repository_heads,
    parse_authority_text,
    require_authorized,
)

STATUS_FILE = WORKSPACE_STATUS_FILE

MARKER_LAST_QG_START = "<!-- STATUS:LAST_QUALITY_GATE_START -->"
MARKER_LAST_QG_END = "<!-- STATUS:LAST_QUALITY_GATE_END -->"
MARKER_LATEST_RELEASE_START = "<!-- STATUS:LATEST_RELEASE_START -->"
MARKER_LATEST_RELEASE_END = "<!-- STATUS:LATEST_RELEASE_END -->"

REQUIRED_MARKERS = (
    MARKER_LAST_QG_START,
    MARKER_LAST_QG_END,
    MARKER_LATEST_RELEASE_START,
    MARKER_LATEST_RELEASE_END,
)


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
    mission_id: str,
    backend_committed: bool,
    backend_message: str,
    frontend_committed: bool,
    frontend_message: str,
    timestamp: str | None = None,
) -> None:
    require_authorized(
        mission_id,
        "status_write",
        STATUS_FILE,
        observed_heads=observe_repository_heads(),
    )
    if not STATUS_FILE.is_file():
        raise FileNotFoundError(f"Status file not found: {STATUS_FILE}")

    when = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")
    content = STATUS_FILE.read_text(encoding="utf-8")
    load_authority(STATUS_FILE)

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

    # The marker update may not replace, remove, or corrupt canonical authority.
    parse_authority_text(content)
    STATUS_FILE.write_text(content, encoding="utf-8", newline="\n")
    load_authority(STATUS_FILE)


def extract_between_markers(
    content: str,
    start_marker: str,
    end_marker: str,
) -> str | None:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        return None
    body_start = start_idx + len(start_marker)
    return content[body_start:end_idx].strip()


def verify_status_file(*, mission_id: str) -> tuple[bool, list[str]]:
    require_authorized(
        mission_id,
        "governance_scripts",
        STATUS_FILE,
        observed_heads=observe_repository_heads(),
    )
    errors: list[str] = []
    if not STATUS_FILE.is_file():
        errors.append(f"File not found: {STATUS_FILE}")
        return False, errors

    content = STATUS_FILE.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in content:
            errors.append(f"Missing marker: {marker}")
    try:
        load_authority(STATUS_FILE)
    except AuthorityError as error:
        errors.append(f"Invalid canonical authority: {error}")
    return not errors, errors


def print_status_summary(mission_id: str) -> int:
    print(f"PROJECT_STATUS.md: {STATUS_FILE}\n")

    ok, errors = verify_status_file(mission_id=mission_id)
    if not ok:
        for err in errors:
            print(f"ERROR: {err}")
        print("\nStatus: ERROR")
        return 1

    content = STATUS_FILE.read_text(encoding="utf-8")

    qg_section = extract_between_markers(
        content, MARKER_LAST_QG_START, MARKER_LAST_QG_END
    )
    release_section = extract_between_markers(
        content, MARKER_LATEST_RELEASE_START, MARKER_LATEST_RELEASE_END
    )

    print("--- Last Quality Gate ---")
    print(qg_section or "(empty)")
    print()

    print("--- Latest Release ---")
    print(release_section or "(empty)")
    print()

    authority = load_authority(STATUS_FILE)
    print("--- Canonical Operational Mission ---")
    print(f"{authority.mission.mission_id} ({authority.mission.status})")
    print()

    print("Status: OK")
    return 0


def run_check(mission_id: str) -> int:
    require_authorized(
        mission_id,
        "governance_scripts",
        STATUS_FILE,
        observed_heads=observe_repository_heads(),
    )
    print(f"Checking {STATUS_FILE}\n")
    ok, errors = verify_status_file(mission_id=mission_id)
    if ok:
        for marker in REQUIRED_MARKERS:
            print(f"OK   {marker}")
        print("\nOverall: OK")
        return 0

    for err in errors:
        print(f"ERROR   {err}")
    for marker in REQUIRED_MARKERS:
        if STATUS_FILE.is_file():
            content = STATUS_FILE.read_text(encoding="utf-8")
            if marker in content:
                print(f"OK   {marker}")
            else:
                print(f"ERROR   Missing marker: {marker}")
    print("\nOverall: ERROR")
    return 1


def run_update_manual(mission_id: str) -> int:
    try:
        update_project_status(
            mission_id=mission_id,
            backend_committed=False,
            backend_message="",
            frontend_committed=False,
            frontend_message="",
        )
    except (FileNotFoundError, ValueError) as err:
        print(f"ERROR: {err}")
        return 1

    print(f"Updated {STATUS_FILE}")
    print("- Backend: No changes.")
    print("- Frontend: No changes.")
    print("- Quality Gate: PASSED")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print or update Melomanos PROJECT_STATUS.md."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify PROJECT_STATUS.md exists and required markers are present.",
    )
    parser.add_argument(
        "--update-manual",
        action="store_true",
        help="Update status sections for manual testing (no changes, QG passed).",
    )
    parser.add_argument("--mission-id", required=True, help="Exact canonical mission ID.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.check:
        try:
            sys.exit(run_check(args.mission_id))
        except AuthorityError as error:
            print(f"ERROR: {error}")
            sys.exit(1)
    if args.update_manual:
        try:
            sys.exit(run_update_manual(args.mission_id))
        except AuthorityError as error:
            print(f"ERROR: {error}")
            sys.exit(1)
    try:
        require_authorized(
            args.mission_id,
            "governance_scripts",
            STATUS_FILE,
            observed_heads=observe_repository_heads(),
        )
        sys.exit(print_status_summary(args.mission_id))
    except AuthorityError as error:
        print(f"ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
