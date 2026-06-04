"""Melomanos finish workflow v2: Quality Gate, then commit + push only where needed."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from project_status import update_project_status

WORKSPACE = Path(__file__).resolve().parent
BACKEND = Path(r"C:\melomanos_market")
FRONTEND = Path(r"C:\melomanos-frontend")
BACKEND_BRANCH = "main"
FRONTEND_BRANCH = "master"


@dataclass
class RepoState:
    name: str
    repo: Path
    branch: str
    has_changes: bool
    message: str = ""

    @property
    def release_action(self) -> str:
        if not self.has_changes or not self.message:
            return "SKIP"
        return "Commit + Push"

    @property
    def will_commit(self) -> bool:
        return self.has_changes and bool(self.message)


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


def git_status_short(repo: Path) -> str:
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
    return result.stdout.strip()


def has_git_changes(repo: Path) -> bool:
    return bool(git_status_short(repo))


def print_repo_status(name: str, has_changes: bool) -> None:
    print(f"{name}:")
    print("Changes detected" if has_changes else "Clean")
    print()


def prompt_commit_message(name: str) -> str:
    print(f"{name} commit message:")
    return input("> ").strip()


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
    print(f"Frontend:\n{frontend.release_action}\n")
    if frontend.message:
        print(f"Message:\n{frontend.message}\n")


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
        return "Skipped (no commit message)"
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
    print(f"Audit:\n{'PASSED' if audit_passed else 'FAILED'}\n")
    if aborted:
        print("Status:\nABORTED\n")
    else:
        print("Status:\nSUCCESS\n")


def main() -> None:
    print("Melomanos finish task v2\n")

    run_quality_gate()

    backend_changes = has_git_changes(BACKEND)
    frontend_changes = has_git_changes(FRONTEND)

    print_repo_status("Backend", backend_changes)
    print_repo_status("Frontend", frontend_changes)

    backend_message = prompt_commit_message("Backend") if backend_changes else ""
    if backend_changes:
        print()
    frontend_message = prompt_commit_message("Frontend") if frontend_changes else ""

    backend = RepoState(
        "Backend",
        BACKEND,
        BACKEND_BRANCH,
        backend_changes,
        backend_message,
    )
    frontend = RepoState(
        "Frontend",
        FRONTEND,
        FRONTEND_BRANCH,
        frontend_changes,
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
