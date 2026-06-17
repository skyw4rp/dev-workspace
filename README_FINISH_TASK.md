# Melomanos finish task (v2)

Automates **Quality Gate → commit → push** for backend and frontend. Commit messages are suggested from **actual changed files**, not only the roadmap.

Repo paths are resolved by `melomanos_paths.py` — see [README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md).

## Requirements

Backend and frontend must be running before `run_audit.py` (E2E step). See [README_AUDIT.md](./README_AUDIT.md) and [README_RUN_MELOMANOS.md](./README_RUN_MELOMANOS.md).

Prep servers for automation:

```powershell
cd C:\melomanos_workspace
py run_melomanos.py --kill-stale --no-wait
py run_melomanos.py --check
```

## Run

```powershell
cd C:\melomanos_workspace
py finish_task.py
```

### Dry run (preview only)

```powershell
py finish_task.py --dry-run
```

- Runs `git status` on backend and frontend
- Shows changed files and suggested messages
- Shows **Roadmap Auto-Advance** preview (current task, next task, can advance)
- Does **not** run audit, commit, or push

### Auto-advance roadmap (no prompt)

```powershell
py finish_task.py --advance-roadmap
```

After a successful release, advances `MVP_ROADMAP.md` without asking `Advance MVP_ROADMAP.md current task? (Y/N)`.

Still requires Quality Gate pass and at least one successful commit/push.

## Flow

1. **Quality Gate** — `py run_audit.py` (skipped in `--dry-run`)
2. **Git status** — list changed files per repo
3. **Smart commit prompts** — file-based suggestion + optional roadmap fallback
4. **Confirmation** — `Proceed? (Y/N)` if any repo will commit
5. **Final summary** — per-repo outcome
6. **PROJECT_STATUS** — optional update (`Update PROJECT_STATUS.md? (Y/N)`)
7. **Roadmap Auto-Advance** — optional advance of `MVP_ROADMAP.md` (see below)

## Smart Commit Messages

Suggestions inspect `git status --short` paths. **Priority order:**

| Priority | Changed files match | Suggested message (backend example) |
|----------|---------------------|-------------------------------------|
| **A** | `seller_payout`, `payout_profile`, `test_seller_payout` | `Add seller payout profile backend` |
| **B** | Mostly `.md` / `.mdc` / `.cursor/rules` / README | `Update AI Operating System documentation` if AI OS paths; else `Update workspace documentation` |
| **C** | `admin`, `test_admin` | `Add admin panel MVP backend` |
| **D** | `dispute`, `test_dispute`, `order_dispute` | `Add dispute resolution backend` |
| **E** | Fallback | Current Active Task from `MVP_ROADMAP.md` → `Add <task> backend` |

Frontend uses the same logic with `frontend` suffix (except pure documentation messages).

### Documentation safety

If a repo’s changes are **mostly documentation**, the script does **not** suggest a business feature name from the roadmap. It suggests AI OS or workspace documentation updates instead.

### Roadmap mismatch warning

If priority **E** (roadmap) is used and changed files do not obviously match the active task (e.g. roadmap says Admin but files are unrelated), you see:

```
WARNING:
Suggested message is based on roadmap, but changed files may not match.
Please review before accepting.
```

**Override manually** when you shipped multiple milestones, docs + code, or the roadmap active task moved ahead of your branch.

### Prompt example

```
Backend changes detected:
- app/models/seller_payout_profile.py
- app/services/seller_payout.py
- tests/test_seller_payout_profile.py

Suggested commit message:
Add seller payout profile backend

Press ENTER to accept, type a custom message, or type SKIP.
(SKIP = this repo will not be committed.)
>
```

| Input | Result |
|-------|--------|
| **ENTER** | Uses suggested message |
| **Custom text** | Uses your message |
| **SKIP** | That repo is **not** committed; release continues safely |

### When to override manually

- Mixed changes (payout code + docs) — pick the message that matches what you are releasing
- Roadmap mismatch warning shown
- Partial commit — use custom message or **SKIP** one repo
- Workspace-only work in backend repo — prefer doc suggestion or custom `Update … documentation`

## Example (dry run)

```powershell
py finish_task.py --dry-run
```

```
=== DRY RUN (no audit, commit, or push) ===

Roadmap active task: Admin Panel MVP

Backend changes detected:
- app/models/seller_payout_profile.py
- tests/test_seller_payout_profile.py

Suggested commit message (payout):
Add seller payout profile backend

Dry run complete.
```

## Repositories

Default paths (override with `MELOMANOS_*_DIR` env vars — see [README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md)):

| Repo | Path | Branch |
|------|------|--------|
| Backend | `C:\melomanos_market` | `main` |
| Frontend | `C:\melomanos-frontend` | `master` |

Each git command is printed before it runs. The script stops on the first failing git command. No force push; no history rewrite.

## Project status (optional)

After a successful run (not aborted), you may be asked to update `PROJECT_STATUS.md`. See [README_STATUS.md](./README_STATUS.md).

## Roadmap Auto-Advance

After a **successful** release (Quality Gate passed, not aborted, at least one repo committed and pushed), `finish_task.py` can update the roadmap for you.

### Prompt

```
Advance MVP_ROADMAP.md current task? (Y/N)
```

Skipped with `--advance-roadmap` (auto-advances when safe).

### What it does (when you answer Y)

1. Reads **Current Active Task** from backend `MVP_ROADMAP.md` (`melomanos_paths.ROADMAP_FILE`)
2. Appends that task to the **Completed** table (if not already there)
3. Removes it from **Current Priority Queue** and renumbers remaining items
4. Sets the next **TODO/READY** queue item as **Current Active Task** (`Status: READY`)
5. Updates workspace and backend `PROJECT_STATUS.md` (paths from `melomanos_paths.py`)
6. Commits and pushes `MVP_ROADMAP.md` + backend `PROJECT_STATUS.md` in the backend repo

If the queue has no remaining **TODO/READY** items:

```
Current Active Task: None
Status: Backlog complete / needs planning
```

### Safety (will not advance)

| Condition | Result |
|-----------|--------|
| Quality Gate failed | Skipped |
| Release aborted | Skipped |
| No successful commit/push | Skipped |
| Current Active Task not detected | Warning; file unchanged |
| Priority queue not parseable | Warning; file unchanged |
| Parsing uncertain / write error | Warning; file unchanged |

### Dry-run preview example

```
--- Roadmap Auto-Advance Preview ---
Current active task: Payment Provider Integration (WebPay placeholder)
Next detected task: Notifications
Can auto-advance: YES
```

### When to override manually

- Shipped work that does **not** match the current active task
- Multiple milestones in one release
- Roadmap structure was edited by hand and no longer matches expected sections
- You need custom **Completed** notes or milestone counts beyond auto-increment

In those cases, answer **N** and edit `MVP_ROADMAP.md` manually (or ask Cursor with the usual prompt).
