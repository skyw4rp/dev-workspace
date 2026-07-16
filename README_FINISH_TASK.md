# Melomanos finish task (v2)

Automates **Quality Gate → commit → push** across all three Melómanos repos: **backend**, **frontend**, and **workspace**. Commit messages are suggested from **actual changed files** and applied automatically.

**One confirmation:** the only normal interactive prompt is `Proceed? (Y/N)`.

Repo paths are resolved by `melomanos_paths.py` — see [README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md).

## Requirements

Backend and frontend must be running before `run_audit.py` (E2E step). See [README_AUDIT.md](./README_AUDIT.md) and [README_RUN_MELOMANOS.md](./README_RUN_MELOMANOS.md).

Prep servers for automation:

```powershell
cd C:\melomanos\workspace
py run_melomanos.py --kill-stale --no-wait
py run_melomanos.py --check
```

## Run

```powershell
cd C:\melomanos\workspace
py finish_task.py
```

Shows a **Release Summary** (repos, messages, project status, roadmap plan), then asks once:

```
Proceed? (Y/N)
```

Suggested commit messages are used automatically — no per-repo ENTER prompts.

### Dry run (preview only)

```powershell
py finish_task.py --dry-run
```

Shows the full release plan with **no prompts**:

- Changed files per repo
- **Chosen** commit messages (auto-suggested or from flags)
- Skipped repos (via flags or no suggestion)
- `Project Status: Will update automatically`
- Roadmap decision (skip / auto-advance / blocked)
- `Interactive prompts: none`

### Custom commit messages

```powershell
py finish_task.py --backend-message "Add webpay checkout backend"
py finish_task.py --frontend-message "Add webpay checkout frontend"
py finish_task.py --workspace-message "Improve workspace automation"
```

### Skip repos

```powershell
py finish_task.py --skip-backend
py finish_task.py --skip-frontend
py finish_task.py --skip-workspace
```

Combine as needed:

```powershell
py finish_task.py --skip-frontend --workspace-message "Update workspace docs only"
```

### Roadmap flags

```powershell
# Default: never advances roadmap interactively
py finish_task.py

# Advance when policy allows (simple READY task)
py finish_task.py --advance-roadmap

# Override multi-phase safety (entire epic verified complete)
py finish_task.py --advance-roadmap --force-advance-roadmap
```

**Default roadmap behavior:**

| Active task | Flags | Result |
|-------------|-------|--------|
| Multi-phase / IN_PROGRESS | *(none)* | Skip — prints policy message |
| Simple / READY | *(none)* | Skip — use `--advance-roadmap` |
| Any | `--advance-roadmap` | Advance if policy allows |
| Multi-phase | `--advance-roadmap` | Blocked — prints warning |
| Multi-phase | `--advance-roadmap --force-advance-roadmap` | Forced advance |

See [ROADMAP_ADVANCE_POLICY.md](./ROADMAP_ADVANCE_POLICY.md).

## Flow

1. **Quality Gate** — `py run_audit.py` (skipped in `--dry-run`)
2. **Git status** — backend, frontend, workspace
3. **Auto-resolve messages** — suggestions or CLI overrides; skip flags applied
4. **Release Summary** — repos, messages, project status, roadmap plan
5. **Proceed? (Y/N)** — the only normal interactive question
6. **Backend / frontend commit + push** — when not skipped and message exists
7. **PROJECT_STATUS** — updated **automatically** on success (no prompt)
8. **Roadmap advance** — only with `--advance-roadmap` (+ `--force-advance-roadmap` if needed)
9. **Workspace commit + push** — runs **last** (includes final status / roadmap-focus)

## Three-repo automation

| Repo | Branch | When it commits |
|------|--------|-----------------|
| Backend | `main` | Step 6 — after `Proceed? (Y/N)` |
| Frontend | `master` | Step 6 — after `Proceed? (Y/N)` |
| Workspace | `main` | Step 9 — after PROJECT_STATUS and roadmap updates |

### Release Summary example

```
================================
Release Summary
================================

Backend:
Commit + Push
Message:
Add seller payout profile backend

Frontend:
SKIP
Message:
(skipped via --skip-* flag)

Workspace:
Commit + Push
Message:
Improve workspace automation

Project Status:
Will update automatically

Roadmap:
Will skip - Roadmap advance skipped by policy: multi-phase or IN_PROGRESS.
```

### When manual commits are still needed

- You passed `--skip-*` for a repo
- Quality Gate failed (no commits run)
- You answered **N** at `Proceed? (Y/N)`
- Git push failed partway (fix locally, then commit/push by hand)
- No suggested message and no `--*-message` flag (repo shown as SKIP)
- Custom partial commits (`finish_task.py` always runs `git add .` per repo)

## Smart Commit Messages

Suggestions inspect `git status --short` paths. Applied automatically unless overridden by flags.

### Backend / frontend

| Priority | Changed files match | Suggested message (backend example) |
|----------|---------------------|-------------------------------------|
| **A** | `seller_payout`, `payout_profile`, `test_seller_payout` | `Add seller payout profile backend` |
| **B** | Mostly `.md` / `.mdc` / `.cursor/rules` / README | `Update AI Operating System documentation` if AI OS paths; else `Update workspace documentation` |
| **C** | `admin`, `test_admin` | `Add admin panel MVP backend` |
| **D** | `dispute`, `test_dispute`, `order_dispute` | `Add dispute resolution backend` |
| **E** | Fallback | Current Active Task from `MVP_ROADMAP.md` → `Add <task> backend` |

Frontend uses the same logic with `frontend` suffix (except pure documentation messages).

### Workspace

| Priority | Changed files match | Suggested message |
|----------|---------------------|-------------------|
| **A** | `finish_task.py`, `roadmap_advance.py`, `project_status.py`, `run_melomanos.py`, `melomanos_paths.py` | `Improve workspace automation` |
| **B** | `AGENT_RULES.md`, `AI_OS_OVERVIEW.md`, `ROADMAP_ADVANCE_POLICY.md`, etc. | `Update AI Operating System documentation` |
| **C** | `README*` | `Update workspace documentation` |
| **D** | `PROJECT_STATUS.md` only | `Update workspace project status` |
| **E** | Fallback | `Update workspace` |

### Roadmap mismatch warning

If a roadmap-based suggestion may not match changed files, the **Release Summary** shows a warning. Override with `--backend-message` / `--frontend-message`.

## Example (dry run)

```powershell
py finish_task.py --dry-run
```

```
=== DRY RUN (no audit, commit, or push) ===

Roadmap active task: Payment Provider Integration (WebPay placeholder)

Backend: Clean

Frontend: Clean

Workspace changes detected:
- finish_task.py
- README_FINISH_TASK.md

Chosen commit message:
Improve workspace automation

Project Status:
Will update automatically

Roadmap:
Will skip - Roadmap advance skipped by policy: multi-phase or IN_PROGRESS.
  Current active task: Payment Provider Integration (WebPay placeholder)
  Next detected task: Notifications
  Signal: contains 'Phase'
  Signal: Status is IN_PROGRESS
  Signal: contains 'Remaining'

Interactive prompts: none (only Proceed? in a real run)

Dry run complete.
```

## Repositories

| Repo | Path | Branch |
|------|------|--------|
| Backend | `C:\melomanos\backend` (or `C:\melomanos_market`) | `main` |
| Frontend | `C:\melomanos\frontend` (or `C:\melomanos-frontend`) | `master` |
| Workspace | `C:\melomanos\workspace` (or `C:\melomanos_workspace`) | `main` |

Each git command is printed before it runs. The script stops on the first failing git command. No force push; no history rewrite.

## Project status

After a successful run (not aborted), `PROJECT_STATUS.md` is updated **automatically**. See [README_STATUS.md](./README_STATUS.md).

## Roadmap Auto-Advance

After a **successful** backend or frontend commit/push, roadmap advance runs only when `--advance-roadmap` is set and policy allows.

**Policy:** [ROADMAP_ADVANCE_POLICY.md](./ROADMAP_ADVANCE_POLICY.md)

### What it does when advancing

1. Reads **Current Active Task** from `MVP_ROADMAP.md`
2. Appends task to **Completed** table
3. Promotes next queue item to **Current Active Task**
4. Updates workspace and backend `PROJECT_STATUS.md`
5. Commits/pushes roadmap docs in backend repo
6. Workspace commit (step 9) includes updated workspace status

### Examples

```powershell
# Preview full plan, no prompts
py finish_task.py --dry-run

# Normal release - one Proceed? prompt
py finish_task.py

# Skip frontend, custom backend message
py finish_task.py --skip-frontend --backend-message "Add webpay phase 2 backend"

# Advance simple milestone after release
py finish_task.py --advance-roadmap

# Force advance multi-phase epic (verified complete)
py finish_task.py --advance-roadmap --force-advance-roadmap
```
# Operational authority

`finish_task.py` is not a release authorization. Before any dry run, audit, test, build, write, staging, commit, push, or roadmap promotion, it requires an exact `READY` mission and each exact action class from the canonical `PROJECT_STATUS.md` JSON block. A token, report, gate PASS, queue, or roadmap cannot substitute.
