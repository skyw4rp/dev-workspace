# Melomanos finish task (v2)

Automates **Quality Gate → commit → push** for backend and frontend. Commit messages are only requested when a repo has changes.

## Requirements

Same as the audit: backend and frontend must be running before `run_audit.py` (E2E step). See [README_AUDIT.md](./README_AUDIT.md).

## Run

```powershell
cd C:\melomanos_workspace
py finish_task.py
```

## Flow

1. **Quality Gate** — `py run_audit.py`  
   On failure: `Quality Gate failed. Fix errors before committing.` (no commits).
2. **Git status** — backend (`main`) and frontend (`master`).
3. **Prompts** — commit message only if that repo has changes (empty message = skip that repo).
4. **Confirmation** — if any repo will commit + push, shows a release summary and `Proceed? (Y/N)`. `N` aborts safely with no commits.
5. **Final summary** — `MELÓMANOS RELEASE SUMMARY` with per-repo outcome, audit, and status.

## Example

```
Backend:
Clean

Frontend:
Changes detected

Frontend commit message:
> Connect Digging Score to Frontend

================================
Release Summary
================================

Backend:
SKIP

Frontend:
Commit + Push

Message:
Connect Digging Score to Frontend

Proceed? (Y/N)
> Y
```

## Repositories

| Repo | Path | Branch |
|------|------|--------|
| Backend | `C:\melomanos_market` | `main` |
| Frontend | `C:\melomanos-frontend` | `master` |

Each git command is printed before it runs. The script stops on the first failing git command.

## Project status (optional)

After a successful run (not aborted), you may be asked to update `PROJECT_STATUS.md`. See [README_STATUS.md](./README_STATUS.md).
