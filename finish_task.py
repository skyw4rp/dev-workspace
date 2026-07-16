"""Melomanos finish workflow v2: Quality Gate, then commit + push only where needed."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from melomanos_paths import BACKEND_DIR, FRONTEND_DIR, WORKSPACE_DIR
from governance_authority import AuthorityError, observe_repository_heads, require_actions
from project_status import update_project_status
from roadmap_advance import (
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
    skipped: bool = False
    warn_mismatch: bool = False

    @property
    def release_action(self) -> str:
        if self.skipped:
            return "SKIP"
        if not self.has_changes:
            return "Clean"
        if not self.message:
            return "SKIP"
        return "Commit + Push"

    @property
    def will_commit(self) -> bool:
        return (
            not self.skipped
            and self.has_changes
            and bool(self.message)
        )


@dataclass
class RoadmapPlan:
    preview: RoadmapAdvancePreview
    summary: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Melomanos release: Quality Gate, smart commits, push."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show release plan only; no audit, commit, or push.",
    )
    parser.add_argument("--mission-id", required=True, help="Exact canonical mission ID.")
    parser.add_argument(
        "--advance-roadmap",
        action="store_true",
        help="After successful release, advance MVP_ROADMAP.md when policy allows.",
    )
    parser.add_argument(
        "--force-advance-roadmap",
        action="store_true",
        help="Override multi-phase safety when used with --advance-roadmap.",
    )
    parser.add_argument("--backend-message", default=None, help="Custom backend commit message.")
    parser.add_argument("--frontend-message", default=None, help="Custom frontend commit message.")
    parser.add_argument("--workspace-message", default=None, help="Custom workspace commit message.")
    parser.add_argument("--skip-backend", action="store_true", help="Skip backend commit/push.")
    parser.add_argument("--skip-frontend", action="store_true", help="Skip frontend commit/push.")
    parser.add_argument("--skip-workspace", action="store_true", help="Skip workspace commit/push.")
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


def resolve_repo_message(
    files: list[str],
    *,
    repo_label: str,
    active_task: str | None,
    custom_message: str | None,
    skipped: bool,
    workspace: bool = False,
) -> tuple[str, bool]:
    if skipped or not files:
        return "", False

    if custom_message:
        return custom_message, False

    suggestion = (
        suggest_workspace_message(files)
        if workspace
        else suggest_from_changed_files(files, repo_label, active_task)
    )
    return suggestion.message or "", suggestion.warn_mismatch


def build_repo_state(
    name: str,
    repo: Path,
    branch: str,
    files: list[str],
    *,
    active_task: str | None,
    custom_message: str | None,
    skipped: bool,
    workspace: bool = False,
) -> RepoState:
    message, warn_mismatch = resolve_repo_message(
        files,
        repo_label=name,
        active_task=active_task,
        custom_message=custom_message,
        skipped=skipped,
        workspace=workspace,
    )
    return RepoState(
        name=name,
        repo=repo,
        branch=branch,
        has_changes=bool(files),
        changed_files=files,
        message=message,
        skipped=skipped,
        warn_mismatch=warn_mismatch,
    )


def plan_roadmap_advance(*, advance_flag: bool, force_flag: bool) -> RoadmapPlan:
    preview = preview_roadmap_advance(ROADMAP_FILE)

    if not advance_flag:
        if preview.multi_phase_safety:
            return RoadmapPlan(
                preview=preview,
                summary=(
                    "Will skip - Roadmap advance skipped by policy: "
                    "multi-phase or IN_PROGRESS."
                ),
            )
        return RoadmapPlan(
            preview=preview,
            summary="Will skip (use --advance-roadmap to enable).",
        )

    if not preview.can_advance:
        warnings = "; ".join(preview.warnings) or "roadmap not ready"
        return RoadmapPlan(
            preview=preview,
            summary=f"Will skip - {warnings}.",
        )

    if preview.multi_phase_safety and not force_flag:
        return RoadmapPlan(
            preview=preview,
            summary=(
                "Will skip - multi-phase epic safety "
                "(use --force-advance-roadmap to override)."
            ),
        )

    next_label = preview.next_task or "None (backlog complete)"
    return RoadmapPlan(
        preview=preview,
        summary=f"Will auto-advance → active task: {next_label}.",
    )


def roadmap_should_advance(plan: RoadmapPlan) -> bool:
    return plan.summary.startswith("Will auto-advance")


def run_quality_gate(mission_id: str) -> None:
    require_actions(
        mission_id,
        ("product_tests", "product_build"),
        observed_heads=observe_repository_heads(),
    )
    print("\n=== Quality Gate ===\n")
    code = run_command(["py", "run_audit.py"], WORKSPACE)
    if code != 0:
        print("\nQuality Gate failed. Fix errors before committing.")
        sys.exit(code)
    print("\nQuality Gate passed.\n")


def _print_repo_plan(state: RepoState) -> None:
    print(f"{state.name}:")
    print(state.release_action)
    if state.message:
        print(f"Message:\n{state.message}")
    elif state.skipped:
        print("Message:\n(skipped via --skip-* flag)")
    elif state.has_changes:
        print("Message:\n(no suggestion - use --*-message or --skip-*)")
    else:
        print("Message:\n(none)")
    if state.warn_mismatch:
        print("WARNING: Suggested message may not match changed files.")
    print()


def print_release_summary(
    backend: RepoState,
    frontend: RepoState,
    workspace: RepoState,
    roadmap_plan: RoadmapPlan,
) -> None:
    print("================================")
    print("Release Summary")
    print("================================\n")
    _print_repo_plan(backend)
    _print_repo_plan(frontend)
    _print_repo_plan(workspace)
    print("Project Status:")
    print("Will update automatically\n")
    print("Roadmap:")
    print(roadmap_plan.summary)
    print()
    if workspace.will_commit:
        print(
            "Note: Workspace commit runs after PROJECT_STATUS and roadmap "
            "updates so the push includes final status state.\n"
        )


def confirm_proceed() -> bool:
    while True:
        answer = input("Proceed? (Y/N)\n> ").strip().upper()
        if answer in ("Y", "YES"):
            return True
        if answer in ("N", "NO"):
            return False
        print("Please enter Y or N.")


def commit_and_push(state: RepoState, mission_id: str) -> str:
    require_actions(
        mission_id,
        ("stage", "commit", "push"),
        observed_heads=observe_repository_heads(),
    )
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
    if state.skipped:
        return "Skipped (--skip-* flag)"
    if not state.has_changes:
        return "Clean"
    if not state.message:
        return "Skipped (no message)"
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


def release_had_successful_commit(
    backend_result: str | None,
    frontend_result: str | None,
) -> bool:
    return (
        backend_result == "Committed and pushed"
        or frontend_result == "Committed and pushed"
    )


def commit_roadmap_docs(repo: Path, branch: str, message: str, mission_id: str) -> None:
    require_actions(
        mission_id,
        ("stage", "commit", "push"),
        observed_heads=observe_repository_heads(),
    )
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


def execute_roadmap_advance(
    plan: RoadmapPlan,
    *,
    mission_id: str,
    force_advance: bool,
    aborted: bool,
    backend_result: str | None,
    frontend_result: str | None,
) -> None:
    if aborted:
        return

    if not roadmap_should_advance(plan):
        print(f"{plan.summary}\n")
        return

    if not release_had_successful_commit(backend_result, frontend_result):
        print("Roadmap auto-advance skipped (no successful backend/frontend commit/push).\n")
        return

    preview = plan.preview
    previous_task = preview.current_task
    if not previous_task:
        print("WARNING: Current Active Task not detected; roadmap not modified.\n")
        return

    try:
        new_text, next_task, backlog_complete = apply_roadmap_advance(
            mission_id=mission_id,
            previous_task=previous_task,
            force_advance=force_advance or preview.multi_phase_safety,
        )
        ROADMAP_FILE.write_text(new_text, encoding="utf-8", newline="\n")
        update_workspace_roadmap_focus(
            mission_id=mission_id,
            current_task=next_task,
            last_completed=previous_task,
        )
        update_backend_status_focus(
            mission_id=mission_id,
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
    commit_roadmap_docs(BACKEND, BACKEND_BRANCH, commit_message, mission_id)


def maybe_commit_workspace(
    workspace: RepoState,
    *,
    mission_id: str,
    custom_message: str | None,
    aborted: bool,
) -> str | None:
    if aborted or workspace.skipped:
        return None

    _, current_files = git_status_data(WORKSPACE, echo=True)
    if not current_files:
        return None

    message = workspace.message or custom_message or ""
    if not message:
        suggestion = suggest_workspace_message(current_files)
        message = suggestion.message or ""
    if not message:
        print("Workspace: skipped (no commit message).\n")
        return None

    state = RepoState(
        "Workspace",
        WORKSPACE,
        WORKSPACE_BRANCH,
        True,
        current_files,
        message,
    )
    return commit_and_push(state, mission_id)


def update_project_status_after_release(
    *,
    mission_id: str,
    backend: RepoState,
    frontend: RepoState,
    backend_result: str | None,
    frontend_result: str | None,
    aborted: bool,
) -> None:
    if aborted:
        return

    try:
        update_project_status(
            mission_id=mission_id,
            backend_committed=backend_result == "Committed and pushed",
            backend_message=backend.message,
            frontend_committed=frontend_result == "Committed and pushed",
            frontend_message=frontend.message,
        )
    except (OSError, ValueError) as err:
        print(f"ERROR: Could not update PROJECT_STATUS.md: {err}")
        sys.exit(1)

    print(f"Updated {WORKSPACE / 'PROJECT_STATUS.md'}\n")


def show_dry_run_plan(
    *,
    backend: RepoState,
    frontend: RepoState,
    workspace: RepoState,
    roadmap_plan: RoadmapPlan,
    active_task: str | None,
) -> None:
    print("=== DRY RUN (no audit, commit, or push) ===\n")
    if active_task:
        print(f"Roadmap active task: {active_task}\n")

    for state in (backend, frontend, workspace):
        if not state.changed_files:
            print(f"{state.name}: Clean\n")
            continue
        print(f"{state.name} changes detected:")
        for path in state.changed_files:
            print(f"- {path}")
        print()
        if state.message:
            print(f"Chosen commit message:\n{state.message}\n")
        elif state.skipped:
            print("Chosen action: SKIP (--skip-* flag)\n")
        else:
            print("Chosen action: SKIP (no suggested message)\n")
        if state.warn_mismatch:
            print("WARNING: Suggested message may not match changed files.\n")

    print("Project Status:")
    print("Will update automatically\n")
    print("Roadmap:")
    print(roadmap_plan.summary)
    preview = roadmap_plan.preview
    if preview.current_task:
        print(f"  Current active task: {preview.current_task}")
    if preview.backlog_complete:
        print("  Next detected task: (none - backlog complete)")
    elif preview.next_task:
        print(f"  Next detected task: {preview.next_task}")
    if preview.multi_phase_signals:
        for signal in preview.multi_phase_signals:
            print(f"  Signal: {signal}")
    print("\nInteractive prompts: none (only Proceed? in a real run)\n")
    print("Dry run complete.\n")


def main() -> None:
    args = parse_args()
    print("Melomanos finish task v2\n")

    # Guard before every roadmap/git read, audit, write, stage, commit, or push.
    # A dry run is still an operational inspection and requires explicit consent.
    requested_actions = (
        ("read_only_inspection",)
        if args.dry_run
        else (
            "product_tests",
            "product_build",
            "status_write",
            "roadmap_promotion",
            "stage",
            "commit",
            "push",
        )
    )
    try:
        require_actions(
            args.mission_id,
            requested_actions,
            observed_heads=observe_repository_heads(),
        )
    except AuthorityError as error:
        print(f"STOP: canonical authority denied finish_task: {error}")
        sys.exit(1)

    active_task = read_active_task_from_roadmap(BACKEND / "MVP_ROADMAP.md")
    roadmap_plan = plan_roadmap_advance(
        advance_flag=args.advance_roadmap,
        force_flag=args.force_advance_roadmap,
    )

    _, backend_files = git_status_data(BACKEND, echo=not args.dry_run)
    _, frontend_files = git_status_data(FRONTEND, echo=not args.dry_run)
    _, workspace_files = git_status_data(WORKSPACE, echo=not args.dry_run)

    backend = build_repo_state(
        "Backend",
        BACKEND,
        BACKEND_BRANCH,
        backend_files,
        active_task=active_task,
        custom_message=args.backend_message,
        skipped=args.skip_backend,
    )
    frontend = build_repo_state(
        "Frontend",
        FRONTEND,
        FRONTEND_BRANCH,
        frontend_files,
        active_task=active_task,
        custom_message=args.frontend_message,
        skipped=args.skip_frontend,
    )
    workspace = build_repo_state(
        "Workspace",
        WORKSPACE,
        WORKSPACE_BRANCH,
        workspace_files,
        active_task=active_task,
        custom_message=args.workspace_message,
        skipped=args.skip_workspace,
        workspace=True,
    )

    if args.dry_run:
        show_dry_run_plan(
            backend=backend,
            frontend=frontend,
            workspace=workspace,
            roadmap_plan=roadmap_plan,
            active_task=active_task,
        )
        return

    run_quality_gate(args.mission_id)

    if active_task:
        print(f"Roadmap active task: {active_task}\n")

    backend_result: str | None = None
    frontend_result: str | None = None
    workspace_result: str | None = None
    aborted = False

    print_release_summary(backend, frontend, workspace, roadmap_plan)
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
        backend_result = commit_and_push(backend, args.mission_id)
    if frontend.will_commit:
        frontend_result = commit_and_push(frontend, args.mission_id)

    if not aborted:
        update_project_status_after_release(
            mission_id=args.mission_id,
            backend=backend,
            frontend=frontend,
            backend_result=backend_result,
            frontend_result=frontend_result,
            aborted=aborted,
        )
        execute_roadmap_advance(
            plan=roadmap_plan,
            mission_id=args.mission_id,
            force_advance=args.force_advance_roadmap,
            aborted=aborted,
            backend_result=backend_result,
            frontend_result=frontend_result,
        )
        workspace_result = maybe_commit_workspace(
            workspace,
            mission_id=args.mission_id,
            custom_message=args.workspace_message,
            aborted=aborted,
        )

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


if __name__ == "__main__":
    main()
