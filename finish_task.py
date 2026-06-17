"""Melomanos finish workflow v2: Quality Gate, then commit + push only where needed."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from melomanos_paths import BACKEND_DIR, FRONTEND_DIR, WORKSPACE_DIR
from project_status import update_project_status
from roadmap_advance import (
    MULTI_PHASE_WARNING,
    ROADMAP_FILE,
    RoadmapAdvancePreview,
    apply_roadmap_advance,
    preview_roadmap_advance,
    update_backend_status_focus,
    update_workspace_roadmap_focus,
)

WORKSPACE = WORKSPACE_DIR
BACKEND = BACKEND_DIR
FRONTEND = FRONTEND_DIR
BACKEND_BRANCH = "main"
FRONTEND_BRANCH = "master"
WORKSPACE_BRANCH = "main"

WORKSPACE_AUTOMATION_FILES = (
    "finish_task.py",
    "roadmap_advance.py",
    "project_status.py",
    "run_melomanos.py",
    "melomanos_paths.py",
)
WORKSPACE_AI_OS_FILES = (
    "agent_rules.md",
    "ai_os_overview.md",
    "roadmap_advance_policy.md",
    "architecture.md",
    "business_rules.md",
    "testing_strategy.md",
)

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
        help="After successful release, auto-advance MVP_ROADMAP.md without Y/N prompt.",
    )
    parser.add_argument(
        "--force-advance-roadmap",
        action="store_true",
        help="Override multi-phase safety when used with --advance-roadmap or apply.",
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


def _file_basenames(files: list[str]) -> set[str]:
    return {Path(path).name.lower() for path in files}


def has_readme_file(files: list[str]) -> bool:
    return any(Path(path).name.upper().startswith("README") for path in files)


def suggest_workspace_message(files: list[str]) -> SuggestionResult:
    basenames = _file_basenames(files)
    if basenames & {name.lower() for name in WORKSPACE_AUTOMATION_FILES}:
        return SuggestionResult(
            message="Improve workspace automation",
            source="automation",
        )
    if paths_contain(files, *WORKSPACE_AI_OS_FILES):
        return SuggestionResult(
            message="Update AI Operating System documentation",
            source="ai_os_docs",
        )
    if has_readme_file(files):
        return SuggestionResult(
            message="Update workspace documentation",
            source="workspace_docs",
        )
    if len(files) == 1 and Path(files[0]).name.lower() == "project_status.md":
        return SuggestionResult(
            message="Update workspace project status",
            source="project_status",
        )
    return SuggestionResult(message="Update workspace", source="fallback")


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


def _print_repo_release_line(state: RepoState) -> None:
    print(f"{state.name}:\n{state.release_action}\n")
    if state.message:
        print(f"Message:\n{state.message}\n")
    elif state.has_changes:
        print("Message:\n(skipped)\n")


def print_release_summary(
    backend: RepoState,
    frontend: RepoState,
    workspace: RepoState,
) -> None:
    print("================================")
    print("Release Summary")
    print("================================\n")
    _print_repo_release_line(backend)
    _print_repo_release_line(frontend)
    _print_repo_release_line(workspace)
    print(
        "Note: Workspace commits run after PROJECT_STATUS and roadmap updates "
        "so the push includes final status state.\n"
    )


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


def print_multi_phase_warning(preview: RoadmapAdvancePreview) -> None:
    print(MULTI_PHASE_WARNING)
    for signal in preview.multi_phase_signals:
        print(f"  - {signal}")
    print()


def confirm_roadmap_advance(preview: RoadmapAdvancePreview) -> bool:
    if preview.multi_phase_safety:
        print_multi_phase_warning(preview)
        print("Type ADVANCE to confirm roadmap advance:")
        answer = input("> ").strip()
        if answer == "ADVANCE":
            return True
        if answer.upper() in ("Y", "YES"):
            print("Y alone is not enough for multi-phase epics. Type ADVANCE to confirm.")
        return False
    return confirm_yes_no("Advance MVP_ROADMAP.md current task? (Y/N)")


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
    workspace: RepoState,
    backend_result: str | None,
    frontend_result: str | None,
    workspace_result: str | None,
    audit_passed: bool,
    aborted: bool,
) -> None:
    print("\n================================")
    print("MELÓMANOS RELEASE SUMMARY")
    print("================================\n")
    print(f"Backend:\n{final_outcome(backend, backend_result)}\n")
    print(f"Frontend:\n{final_outcome(frontend, frontend_result)}\n")
    print(f"Workspace:\n{final_outcome(workspace, workspace_result)}\n")
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
    print(
        f"Multi-phase safety triggered: "
        f"{'YES' if preview.multi_phase_safety else 'NO'}"
    )
    if preview.multi_phase_signals:
        for signal in preview.multi_phase_signals:
            print(f"  Signal: {signal}")
    if preview.multi_phase_safety:
        print(
            "Note: interactive advance requires typing ADVANCE; "
            "--advance-roadmap requires --force-advance-roadmap."
        )
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
    force_advance: bool,
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

    if preview.multi_phase_safety and not force_advance:
        if auto:
            print("Roadmap auto-advance blocked: multi-phase epic safety.")
            print_multi_phase_warning(preview)
            print(
                "Refusing --advance-roadmap without --force-advance-roadmap.\n"
            )
            return

    print()
    should_advance = False
    if auto:
        should_advance = True
    else:
        should_advance = confirm_roadmap_advance(preview)

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
            force_advance=force_advance or preview.multi_phase_safety,
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


def maybe_commit_workspace(
    workspace: RepoState,
    *,
    aborted: bool,
) -> str | None:
    if aborted:
        return None

    _, current_files = git_status_data(WORKSPACE, echo=True)
    if not current_files:
        return None

    message = workspace.message
    if not message:
        suggestion = suggest_workspace_message(current_files)
        message = prompt_smart_commit_message("Workspace", current_files, suggestion)
        if not message:
            print("Workspace: skipped (no commit).\n")
            return None

    state = RepoState(
        "Workspace",
        WORKSPACE,
        WORKSPACE_BRANCH,
        True,
        current_files,
        message,
    )
    return commit_and_push(state)


def show_dry_run_suggestion(
    name: str,
    files: list[str],
    active_task: str | None,
    *,
    workspace: bool = False,
) -> None:
    if not files:
        print(f"{name}: Clean\n")
        return
    if workspace:
        result = suggest_workspace_message(files)
    else:
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
    workspace_files: list[str],
    active_task: str | None,
    interactive: bool,
) -> tuple[str, str, str]:
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

    workspace_message = ""
    if workspace_files:
        if interactive:
            suggestion = suggest_workspace_message(workspace_files)
            workspace_message = prompt_smart_commit_message(
                "Workspace", workspace_files, suggestion
            )
        else:
            workspace_message = ""

    return backend_message, frontend_message, workspace_message


def main() -> None:
    args = parse_args()
    print("Melomanos finish task v2\n")

    active_task = read_active_task_from_roadmap(BACKEND / "MVP_ROADMAP.md")

    _, backend_files = git_status_data(BACKEND, echo=not args.dry_run)
    _, frontend_files = git_status_data(FRONTEND, echo=not args.dry_run)
    _, workspace_files = git_status_data(WORKSPACE, echo=not args.dry_run)

    if args.dry_run:
        print("=== DRY RUN (no audit, commit, or push) ===\n")
        if active_task:
            print(f"Roadmap active task: {active_task}\n")
        show_dry_run_suggestion("Backend", backend_files, active_task)
        show_dry_run_suggestion("Frontend", frontend_files, active_task)
        show_dry_run_suggestion(
            "Workspace", workspace_files, active_task, workspace=True
        )
        show_roadmap_advance_preview()
        print("Dry run complete.\n")
        return

    run_quality_gate()

    backend_changes = bool(backend_files)
    frontend_changes = bool(frontend_files)
    workspace_changes = bool(workspace_files)

    if active_task:
        print(f"Roadmap active task: {active_task}\n")

    print_repo_status("Backend", backend_changes)
    print_repo_status("Frontend", frontend_changes)
    print_repo_status("Workspace", workspace_changes)

    backend_message, frontend_message, workspace_message = collect_repo_messages(
        backend_files=backend_files,
        frontend_files=frontend_files,
        workspace_files=workspace_files,
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
    workspace = RepoState(
        "Workspace",
        WORKSPACE,
        WORKSPACE_BRANCH,
        workspace_changes,
        workspace_files,
        workspace_message,
    )

    backend_result: str | None = None
    frontend_result: str | None = None
    workspace_result: str | None = None
    aborted = False

    if backend.will_commit or frontend.will_commit or workspace.will_commit:
        print()
        print_release_summary(backend, frontend, workspace)
        if not confirm_proceed():
            print("\nAborted. No commits were made.\n")
            aborted = True
            print_final_summary(
                backend=backend,
                frontend=frontend,
                workspace=workspace,
                backend_result=None,
                frontend_result=None,
                workspace_result=None,
                audit_passed=True,
                aborted=True,
            )
            sys.exit(0)

        if backend.will_commit:
            backend_result = commit_and_push(backend)
        if frontend.will_commit:
            frontend_result = commit_and_push(frontend)

    if not aborted:
        maybe_update_project_status(
            backend=backend,
            frontend=frontend,
            backend_result=backend_result,
            frontend_result=frontend_result,
        )
        maybe_advance_roadmap(
            auto=args.advance_roadmap,
            force_advance=args.force_advance_roadmap,
            audit_passed=True,
            aborted=aborted,
            backend_result=backend_result,
            frontend_result=frontend_result,
        )
        workspace_result = maybe_commit_workspace(workspace, aborted=aborted)

    print_final_summary(
        backend=backend,
        frontend=frontend,
        workspace=workspace,
        backend_result=backend_result,
        frontend_result=frontend_result,
        workspace_result=workspace_result,
        audit_passed=True,
        aborted=aborted,
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
