"""Melomanos finish workflow v2: Quality Gate, then commit + push only where needed."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from project_status import update_project_status
from roadmap_advance import (
    ROADMAP_FILE,
    apply_roadmap_advance,
    preview_roadmap_advance,
    update_backend_status_focus,
    update_workspace_roadmap_focus,
)

WORKSPACE = Path(__file__).resolve().parent
BACKEND = Path(r"C:\melomanos_market")
FRONTEND = Path(r"C:\melomanos-frontend")
BACKEND_BRANCH = "main"
FRONTEND_BRANCH = "master"

AI_OS_DOC_MARKERS = (
    "ai_os_overview",
    "agent_rules",
    "architecture.md",
    "business_rules",
    "testing_strategy",
    "quality_gate",
    ".cursor/rules",
)
WORKSPACE_DOC_MARKERS = (
    "project_status",
    "mvp_roadmap",
    "readme",
)


@dataclass
class SuggestionResult:
    message: str | None
    source: str
    warn_mismatch: bool = False


@dataclass
class RepoState:
    name: str
    repo: Path
    branch: str
    has_changes: bool
    changed_files: list[str]
    message: str = ""

    @property
    def release_action(self) -> str:
        if not self.has_changes or not self.message:
            return "SKIP"
        return "Commit + Push"

    @property
    def will_commit(self) -> bool:
        return self.has_changes and bool(self.message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Melomanos release: Quality Gate, smart commits, push."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show git status and suggested messages only; no audit, commit, or push.",
    )
    parser.add_argument(
        "--advance-roadmap",
        action="store_true",
        help="After successful release, auto-advance MVP_ROADMAP.md without prompting.",
    )
    return parser.parse_args()


def print_command(command: list[str], cwd: Path) -> None:
    print(f"  cwd: {cwd}")
    print(f"  cmd: {' '.join(command)}\n")


def run_command(command: list[str], cwd: Path) -> int:
    print_command(command, cwd)
    if not cwd.is_dir():
        print(f"ERROR: Path not found: {cwd}")
        return 1
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=sys.platform == "win32",
    )
    return result.returncode


def format_git_status_file(raw_line: str) -> str:
    """Extract the filename from a git status --short line exactly as git reports it.

    git status --short format: XY<space>filename
    where XY is always two status characters (e.g. ' M', 'M ', '??', 'MM', 'R ').
    The filename starts at position 3.  For renames git emits 'old -> new'; we keep
    the destination path.  We do NOT strip() first because that would eat the leading
    space in codes like ' M', shifting the filename left.
    """
    if len(raw_line) < 4:
        return raw_line.strip()
    path_part = raw_line[3:]
    if " -> " in path_part:
        path_part = path_part.split(" -> ")[-1]
    return path_part.strip().replace("\\", "/")


def parse_changed_files(status_output: str) -> list[str]:
    files: list[str] = []
    for line in status_output.splitlines():
        if not line.strip():
            continue
        files.append(format_git_status_file(line))
    return files


def git_status_data(repo: Path, *, echo: bool = True) -> tuple[str, list[str]]:
    if echo:
        print_command(["git", "status", "--short"], repo)
    if not repo.is_dir():
        print(f"ERROR: Repository path not found: {repo}")
        sys.exit(1)
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo,
        capture_output=True,
        text=True,
        shell=sys.platform == "win32",
    )
    if result.returncode != 0:
        print(f"ERROR: git status failed in {repo} (exit {result.returncode})")
        sys.exit(result.returncode)
    output = result.stdout
    return output, parse_changed_files(output)


def print_repo_status(name: str, has_changes: bool) -> None:
    print(f"{name}:")
    if not has_changes:
        print("Clean")
    print()


def read_active_task_from_roadmap(roadmap_path: Path) -> str | None:
    if not roadmap_path.is_file():
        return None
    text = roadmap_path.read_text(encoding="utf-8")
    match = re.search(
        r"## Current Active Task\s*\n+(?:###\s+(.+?)\s*(?:\n|$))",
        text,
    )
    if not match:
        return None
    return match.group(1).strip()


def format_task_for_commit(task: str) -> str:
    words = task.strip().split()
    return " ".join(
        "MVP" if word.upper() == "MVP" else word.lower() for word in words
    )


def _combined_paths(files: list[str]) -> str:
    return " ".join(files).lower()


def _is_doc_file(path: str) -> bool:
    lower = path.lower()
    return (
        lower.endswith(".md")
        or lower.endswith(".mdc")
        or "readme" in Path(lower).name
    )


def is_mostly_documentation(files: list[str]) -> bool:
    if not files:
        return False
    doc_count = sum(1 for f in files if _is_doc_file(f))
    return doc_count >= len(files) * 0.5


def paths_contain(files: list[str], *needles: str) -> bool:
    combined = _combined_paths(files)
    return any(needle.lower() in combined for needle in needles)


def repo_feature_suffix(repo_label: str) -> str:
    return "backend" if repo_label == "Backend" else "frontend"


def build_feature_message(feature: str, repo_label: str) -> str:
    formatted = format_task_for_commit(feature)
    suffix = repo_feature_suffix(repo_label)
    if suffix in formatted:
        return f"Add {formatted}"
    return f"Add {formatted} {suffix}"


def roadmap_task_matches_files(task: str, files: list[str]) -> bool:
    combined = _combined_paths(files)
    task_lower = task.lower()
    checks = (
        ("admin", ("admin",)),
        ("payout", ("payout", "seller_payout")),
        ("dispute", ("dispute",)),
        ("shipping", ("shipping",)),
        ("subscription", ("subscription",)),
        ("escrow", ("escrow", "order")),
    )
    for keyword, file_hints in checks:
        if keyword in task_lower:
            return any(hint in combined for hint in file_hints)
    return True


def suggest_from_changed_files(
    files: list[str],
    repo_label: str,
    active_task: str | None,
) -> SuggestionResult:
    suffix = repo_feature_suffix(repo_label)

    if paths_contain(files, "seller_payout", "payout_profile", "test_seller_payout"):
        return SuggestionResult(
            message=f"Add seller payout profile {suffix}",
            source="payout",
        )

    if is_mostly_documentation(files):
        if paths_contain(files, *AI_OS_DOC_MARKERS):
            return SuggestionResult(
                message="Update AI Operating System documentation",
                source="ai_os_docs",
            )
        return SuggestionResult(
            message="Update workspace documentation",
            source="workspace_docs",
        )

    if paths_contain(files, "admin", "test_admin"):
        return SuggestionResult(
            message=f"Add admin panel MVP {suffix}",
            source="admin",
        )

    if paths_contain(
        files,
        "dispute",
        "test_dispute",
        "dispute_resolution",
        "order_dispute",
    ):
        return SuggestionResult(
            message=f"Add dispute resolution {suffix}",
            source="dispute",
        )

    if active_task:
        warn = not roadmap_task_matches_files(active_task, files)
        return SuggestionResult(
            message=build_feature_message(active_task, repo_label),
            source="roadmap",
            warn_mismatch=warn,
        )

    return SuggestionResult(message=None, source="manual")


def print_changed_files_summary(name: str, files: list[str]) -> None:
    print(f"{name} changes detected:")
    for path in files:
        print(f"- {path}")
    print()


def prompt_smart_commit_message(
    name: str,
    files: list[str],
    suggestion: SuggestionResult | None,
) -> str:
    print_changed_files_summary(name, files)

    if suggestion and suggestion.message:
        print("Suggested commit message:")
        print(suggestion.message)
        print()
        if suggestion.warn_mismatch:
            print("WARNING:")
            print(
                "Suggested message is based on roadmap, but changed files "
                "may not match."
            )
            print("Please review before accepting.")
            print()
        print("Press ENTER to accept, type a custom message, or type SKIP.")
        print("(SKIP = this repo will not be committed.)")
        line = input("> ").strip()
        if line.upper() == "SKIP":
            print(f"{name}: skipped (no commit for this repo).\n")
            return ""
        if line == "":
            return suggestion.message
        return line

    print(f"{name} commit message:")
    line = input("> ").strip()
    if line.upper() == "SKIP":
        print(f"{name}: skipped (no commit for this repo).\n")
        return ""
    return line


def run_quality_gate() -> None:
    print("\n=== Quality Gate ===\n")
    code = run_command(["py", "run_audit.py"], WORKSPACE)
    if code != 0:
        print("\nQuality Gate failed. Fix errors before committing.")
        sys.exit(code)
    print("\nQuality Gate passed.\n")


def print_release_summary(backend: RepoState, frontend: RepoState) -> None:
    print("================================")
    print("Release Summary")
    print("================================\n")
    print(f"Backend:\n{backend.release_action}\n")
    if backend.message:
        print(f"Message:\n{backend.message}\n")
    elif backend.has_changes:
        print("Message:\n(skipped)\n")
    print(f"Frontend:\n{frontend.release_action}\n")
    if frontend.message:
        print(f"Message:\n{frontend.message}\n")
    elif frontend.has_changes:
        print("Message:\n(skipped)\n")


def confirm_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt}\n> ").strip().upper()
        if answer in ("Y", "YES"):
            return True
        if answer in ("N", "NO"):
            return False
        print("Please enter Y or N.")


def confirm_proceed() -> bool:
    return confirm_yes_no("Proceed? (Y/N)")


def commit_and_push(state: RepoState) -> str:
    print(f"\n--- {state.name} ({state.repo}) ---\n")

    steps = [
        ["git", "add", "."],
        ["git", "commit", "-m", state.message],
        ["git", "push", "origin", state.branch],
    ]
    for command in steps:
        code = run_command(command, state.repo)
        if code != 0:
            print(f"\nERROR: {state.name} git step failed (exit {code})")
            sys.exit(code)

    return "Committed and pushed"


def final_outcome(state: RepoState, result: str | None) -> str:
    if result:
        return result
    if not state.has_changes:
        return "Clean"
    if not state.message:
        return "Skipped (SKIP or empty message)"
    return "Not committed"


def print_final_summary(
    *,
    backend: RepoState,
    frontend: RepoState,
    backend_result: str | None,
    frontend_result: str | None,
    audit_passed: bool,
    aborted: bool,
) -> None:
    print("\n================================")
    print("MELÓMANOS RELEASE SUMMARY")
    print("================================\n")
    print(f"Backend:\n{final_outcome(backend, backend_result)}\n")
    print(f"Frontend:\n{final_outcome(frontend, frontend_result)}\n")
    print(f"Audit:\n{'PASSED' if audit_passed else 'FAILED / SKIPPED'}\n")
    if aborted:
        print("Status:\nABORTED\n")
    else:
        print("Status:\nSUCCESS\n")


def show_roadmap_advance_preview() -> None:
    preview = preview_roadmap_advance(ROADMAP_FILE)
    print("--- Roadmap Auto-Advance Preview ---")
    print(f"Current active task: {preview.current_task or '(not detected)'}")
    if preview.backlog_complete:
        print("Next detected task: (none — backlog complete)")
    else:
        print(f"Next detected task: {preview.next_task or '(not detected)'}")
    if preview.warnings:
        for warning in preview.warnings:
            print(f"WARNING: {warning}")
    print(f"Can auto-advance: {'YES' if preview.can_advance else 'NO'}")
    print()


def release_had_successful_commit(
    backend_result: str | None,
    frontend_result: str | None,
) -> bool:
    return (
        backend_result == "Committed and pushed"
        or frontend_result == "Committed and pushed"
    )


def commit_roadmap_docs(repo: Path, branch: str, message: str) -> None:
    status = subprocess.run(
        ["git", "status", "--short", "MVP_ROADMAP.md", "PROJECT_STATUS.md"],
        cwd=repo,
        capture_output=True,
        text=True,
        shell=sys.platform == "win32",
    )
    if status.returncode != 0 or not status.stdout.strip():
        print("No roadmap/status doc changes to commit in backend.\n")
        return

    steps = [
        ["git", "add", "MVP_ROADMAP.md", "PROJECT_STATUS.md"],
        ["git", "commit", "-m", message],
        ["git", "push", "origin", branch],
    ]
    for command in steps:
        code = run_command(command, repo)
        if code != 0:
            print(f"\nERROR: Roadmap doc commit failed (exit {code})")
            sys.exit(code)
    print("Committed and pushed roadmap/status docs in backend.\n")


def maybe_advance_roadmap(
    *,
    auto: bool,
    audit_passed: bool,
    aborted: bool,
    backend_result: str | None,
    frontend_result: str | None,
) -> None:
    if not audit_passed or aborted:
        return
    if not release_had_successful_commit(backend_result, frontend_result):
        print("Roadmap auto-advance skipped (no successful commit/push).\n")
        return

    preview = preview_roadmap_advance(ROADMAP_FILE)
    if not preview.can_advance:
        print("Roadmap auto-advance skipped:")
        for warning in preview.warnings:
            print(f"  - {warning}")
        print()
        return

    print()
    should_advance = auto
    if not auto:
        should_advance = confirm_yes_no("Advance MVP_ROADMAP.md current task? (Y/N)")

    if not should_advance:
        print("MVP_ROADMAP.md unchanged.\n")
        return

    previous_task = preview.current_task
    if not previous_task:
        print("WARNING: Current Active Task not detected; roadmap not modified.\n")
        return

    try:
        new_text, next_task, backlog_complete = apply_roadmap_advance(
            previous_task=previous_task,
        )
        ROADMAP_FILE.write_text(new_text, encoding="utf-8", newline="\n")
        update_workspace_roadmap_focus(
            current_task=next_task,
            last_completed=previous_task,
        )
        update_backend_status_focus(
            current_task=next_task,
            last_completed=previous_task,
        )
    except (OSError, ValueError) as err:
        print(f"WARNING: Roadmap auto-advance failed: {err}")
        print("MVP_ROADMAP.md was not modified.\n")
        return

    next_label = next_task or "None (backlog complete)"
    print(f"Advanced roadmap: completed {previous_task!r} → active {next_label!r}")
    if backlog_complete:
        print(f"Status: {next_label}")
    print(f"Updated {ROADMAP_FILE}")
    print(f"Updated {WORKSPACE / 'PROJECT_STATUS.md'}")
    print(f"Updated {BACKEND / 'PROJECT_STATUS.md'}\n")

    commit_message = (
        f"Advance roadmap: complete {previous_task}, active {next_label}"
    )
    commit_roadmap_docs(BACKEND, BACKEND_BRANCH, commit_message)
    print(
        "Note: workspace PROJECT_STATUS.md was updated locally; "
        "commit the workspace repo separately if needed.\n"
    )


def show_dry_run_suggestion(name: str, files: list[str], active_task: str | None) -> None:
    if not files:
        print(f"{name}: Clean\n")
        return
    result = suggest_from_changed_files(files, name, active_task)
    print_changed_files_summary(name, files)
    if result.message:
        print(f"Suggested commit message ({result.source}):")
        print(result.message)
        if result.warn_mismatch:
            print()
            print("WARNING: Roadmap suggestion may not match changed files.")
    else:
        print("Suggested commit message: (manual prompt required)")
    print()


def collect_repo_messages(
    *,
    backend_files: list[str],
    frontend_files: list[str],
    active_task: str | None,
    interactive: bool,
) -> tuple[str, str]:
    backend_message = ""
    if backend_files:
        if interactive:
            suggestion = suggest_from_changed_files(
                backend_files, "Backend", active_task
            )
            backend_message = prompt_smart_commit_message(
                "Backend", backend_files, suggestion
            )
        else:
            backend_message = ""

    frontend_message = ""
    if frontend_files:
        if interactive:
            suggestion = suggest_from_changed_files(
                frontend_files, "Frontend", active_task
            )
            frontend_message = prompt_smart_commit_message(
                "Frontend", frontend_files, suggestion
            )
        else:
            frontend_message = ""

    return backend_message, frontend_message


def main() -> None:
    args = parse_args()
    print("Melomanos finish task v2\n")

    active_task = read_active_task_from_roadmap(BACKEND / "MVP_ROADMAP.md")

    _, backend_files = git_status_data(BACKEND, echo=not args.dry_run)
    _, frontend_files = git_status_data(FRONTEND, echo=not args.dry_run)

    if args.dry_run:
        print("=== DRY RUN (no audit, commit, or push) ===\n")
        if active_task:
            print(f"Roadmap active task: {active_task}\n")
        show_dry_run_suggestion("Backend", backend_files, active_task)
        show_dry_run_suggestion("Frontend", frontend_files, active_task)
        show_roadmap_advance_preview()
        print("Dry run complete.\n")
        return

    run_quality_gate()

    backend_changes = bool(backend_files)
    frontend_changes = bool(frontend_files)

    if active_task:
        print(f"Roadmap active task: {active_task}\n")

    print_repo_status("Backend", backend_changes)
    print_repo_status("Frontend", frontend_changes)

    backend_message, frontend_message = collect_repo_messages(
        backend_files=backend_files,
        frontend_files=frontend_files,
        active_task=active_task,
        interactive=True,
    )

    backend = RepoState(
        "Backend",
        BACKEND,
        BACKEND_BRANCH,
        backend_changes,
        backend_files,
        backend_message,
    )
    frontend = RepoState(
        "Frontend",
        FRONTEND,
        FRONTEND_BRANCH,
        frontend_changes,
        frontend_files,
        frontend_message,
    )

    backend_result: str | None = None
    frontend_result: str | None = None
    aborted = False

    if backend.will_commit or frontend.will_commit:
        print()
        print_release_summary(backend, frontend)
        if not confirm_proceed():
            print("\nAborted. No commits were made.\n")
            aborted = True
            print_final_summary(
                backend=backend,
                frontend=frontend,
                backend_result=None,
                frontend_result=None,
                audit_passed=True,
                aborted=True,
            )
            sys.exit(0)

        if backend.will_commit:
            backend_result = commit_and_push(backend)
        if frontend.will_commit:
            frontend_result = commit_and_push(frontend)

    print_final_summary(
        backend=backend,
        frontend=frontend,
        backend_result=backend_result,
        frontend_result=frontend_result,
        audit_passed=True,
        aborted=aborted,
    )

    if not aborted:
        maybe_update_project_status(
            backend=backend,
            frontend=frontend,
            backend_result=backend_result,
            frontend_result=frontend_result,
        )
        maybe_advance_roadmap(
            auto=args.advance_roadmap,
            audit_passed=True,
            aborted=aborted,
            backend_result=backend_result,
            frontend_result=frontend_result,
        )


def maybe_update_project_status(
    *,
    backend: RepoState,
    frontend: RepoState,
    backend_result: str | None,
    frontend_result: str | None,
) -> None:
    print()
    if not confirm_yes_no("Update PROJECT_STATUS.md? (Y/N)"):
        print("PROJECT_STATUS.md unchanged.\n")
        return

    try:
        update_project_status(
            backend_committed=backend_result == "Committed and pushed",
            backend_message=backend.message,
            frontend_committed=frontend_result == "Committed and pushed",
            frontend_message=frontend.message,
        )
    except (OSError, ValueError) as err:
        print(f"ERROR: Could not update PROJECT_STATUS.md: {err}")
        sys.exit(1)

    print(f"Updated {WORKSPACE / 'PROJECT_STATUS.md'}\n")


if __name__ == "__main__":
    main()
