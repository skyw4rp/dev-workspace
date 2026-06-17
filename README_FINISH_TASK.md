# Melomanos finish task (v2)

Automates **Quality Gate → commit → push** across all three Melómanos repos: **backend**, **frontend**, and **workspace**. Commit messages are suggested from **actual changed files**, not only the roadmap.

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

- Runs `git status` on backend, frontend, and **workspace**
- Shows changed files and suggested messages per repo
- Shows **Roadmap Auto-Advance** preview (current task, next task, can advance, multi-phase safety)
- Does **not** run audit, commit, or push

### Auto-advance roadmap (no Y/N prompt)

```powershell
py finish_task.py --advance-roadmap
```

After a successful release, advances `MVP_ROADMAP.md` without asking `Advance MVP_ROADMAP.md current task? (Y/N)`.

Still requires Quality Gate pass and at least one successful commit/push.

**Multi-phase safety:** If the active task looks like an in-progress multi-phase epic (e.g. WebPay with Phase 1 done), `--advance-roadmap` is **refused** unless you also pass `--force-advance-roadmap`. See [ROADMAP_ADVANCE_POLICY.md](./ROADMAP_ADVANCE_POLICY.md).

### Force advance (override multi-phase safety)

```powershell
py finish_task.py --advance-roadmap --force-advance-roadmap
```

Use only when the entire roadmap item is truly complete or you are intentionally correcting the roadmap after manual verification.

## Flow

1. **Quality Gate** — `py run_audit.py` (skipped in `--dry-run`)
2. **Git status** — list changed files in backend, frontend, and workspace
3. **Smart commit prompts** — file-based suggestion per repo (+ roadmap fallback for app repos)
4. **Confirmation** — `Proceed? (Y/N)` if any repo will commit
5. **Backend / frontend commit + push** — immediate when accepted
6. **PROJECT_STATUS** — optional update (`Update PROJECT_STATUS.md? (Y/N)`)
7. **Roadmap Auto-Advance** — optional advance of `MVP_ROADMAP.md` (see below)
8. **Workspace commit + push** — runs **last**, so the push includes final `PROJECT_STATUS.md` and roadmap-focus updates

## Three-repo automation

| Repo | Branch | When it commits |
|------|--------|-----------------|
| Backend | `main` | Step 5 — after `Proceed? (Y/N)` |
| Frontend | `master` | Step 5 — after `Proceed? (Y/N)` |
| Workspace | `main` | Step 8 — after PROJECT_STATUS and roadmap updates |

Workspace uses the same prompt style as backend/frontend (ENTER / custom message / **SKIP**).

If you skipped workspace at the initial prompt but later accepted a **PROJECT_STATUS** or **roadmap** update that modified workspace files, you are prompted again before the deferred workspace commit.

### When manual commits are still needed

- You answered **SKIP** for a repo and still want to ship it later
- Quality Gate failed (no commits run)
- You aborted at **Proceed? (Y/N)**
- Git push failed partway (fix locally, then commit/push by hand)
- Changes outside the three Melómanos repos (there are no other repos in this workflow)
- Custom partial commits (specific files only) — `finish_task.py` always runs `git add .` per repo

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

### Workspace commit messages

Priority order for **workspace** repo paths:

| Priority | Changed files match | Suggested message |
|----------|---------------------|-------------------|
| **A** | `finish_task.py`, `roadmap_advance.py`, `project_status.py`, `run_melomanos.py`, `melomanos_paths.py` | `Improve workspace automation` |
| **B** | `AGENT_RULES.md`, `AI_OS_OVERVIEW.md`, `ROADMAP_ADVANCE_POLICY.md`, `ARCHITECTURE.md`, `BUSINESS_RULES.md`, `TESTING_STRATEGY.md` | `Update AI Operating System documentation` |
| **C** | `README*` | `Update workspace documentation` |
| **D** | `PROJECT_STATUS.md` only | `Update workspace project status` |
| **E** | Fallback | `Update workspace` |

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

### Prompt example (workspace)

```
Workspace changes detected:
- finish_task.py
- ROADMAP_ADVANCE_POLICY.md

Suggested commit message:
Improve workspace automation

Press ENTER to accept, type a custom message, or type SKIP.
(SKIP = this repo will not be committed.)
>
```

| Input | Result |
|-------|--------|
| **ENTER** | Uses suggested message (deferred commit after status/roadmap) |
| **Custom text** | Uses your message |
| **SKIP** | Workspace is **not** committed; release continues |

### Prompt example (backend)
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

Roadmap active task: Payment Provider Integration (WebPay placeholder)

Backend changes detected:
- AGENT_RULES.md
- AI_OS_OVERVIEW.md

Suggested commit message (ai_os_docs):
Update AI Operating System documentation

Frontend: Clean

Workspace changes detected:
- finish_task.py
- roadmap_advance.py
- ROADMAP_ADVANCE_POLICY.md
- README_FINISH_TASK.md

Suggested commit message (automation):
Improve workspace automation

--- Roadmap Auto-Advance Preview ---
...

Dry run complete.
```

## Repositories

Default paths (override with `MELOMANOS_*_DIR` env vars — see [README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md)):

| Repo | Path | Branch |
|------|------|--------|
| Backend | `C:\melomanos\backend` (or `C:\melomanos_market`) | `main` |
| Frontend | `C:\melomanos\frontend` (or `C:\melomanos-frontend`) | `master` |
| Workspace | `C:\melomanos\workspace` (or `C:\melomanos_workspace`) | `main` |

Each git command is printed before it runs. The script stops on the first failing git command. No force push; no history rewrite.

## Project status (optional)

After a successful run (not aborted), you may be asked to update `PROJECT_STATUS.md`. See [README_STATUS.md](./README_STATUS.md).

## Roadmap Auto-Advance

After a **successful** release (Quality Gate passed, not aborted, at least one repo committed and pushed), `finish_task.py` can update the roadmap for you.

**Policy:** [ROADMAP_ADVANCE_POLICY.md](./ROADMAP_ADVANCE_POLICY.md) — advance only when the **entire** active roadmap item is complete, not after a single internal phase.

### Prompt (single-phase / READY milestones)

```
Advance MVP_ROADMAP.md current task? (Y/N)
```

### Prompt (multi-phase epic or IN_PROGRESS)

When the active task (or matching queue item) contains signals such as `Phase`, `Remaining`, `7 phases`, `IN_PROGRESS`, or unchecked `[ ]`:

```
WARNING: Current active task appears to be a multi-phase epic or still IN_PROGRESS.
Auto-advance may be premature.
  - contains 'Phase'
  - contains 'Remaining'
  - Status is IN_PROGRESS
Type ADVANCE to confirm roadmap advance:
>
```

- **`Y` / `YES` alone does not advance** in this case — you must type **`ADVANCE`** exactly.
- Skipped with `--advance-roadmap` only when multi-phase safety is **not** triggered.
- `--advance-roadmap` **without** `--force-advance-roadmap` is **refused** when multi-phase safety triggers.

### Flags

| Flag | Effect |
|------|--------|
| *(none)* | Interactive prompt after release (`Y/N` or `ADVANCE`) |
| `--advance-roadmap` | Auto-advance when safe (no multi-phase block) |
| `--force-advance-roadmap` | Override multi-phase safety (use with `--advance-roadmap` or after typing `ADVANCE`) |

### Examples

```powershell
# Preview active task, next task, and safety status
py finish_task.py --dry-run

# Normal release; prompted Y/N or ADVANCE if multi-phase
py finish_task.py

# Auto-advance only when not a multi-phase epic
py finish_task.py --advance-roadmap

# Override safety (entire epic verified complete)
py finish_task.py --advance-roadmap --force-advance-roadmap
```

### What it does (when you answer Y)

1. Reads **Current Active Task** from backend `MVP_ROADMAP.md` (`melomanos_paths.ROADMAP_FILE`)
2. Appends that task to the **Completed** table (if not already there)
3. Removes it from **Current Priority Queue** and renumbers remaining items
4. Sets the next **TODO/READY** queue item as **Current Active Task** (`Status: READY`)
5. Updates workspace and backend `PROJECT_STATUS.md` (paths from `melomanos_paths.py`)
6. Commits and pushes `MVP_ROADMAP.md` + backend `PROJECT_STATUS.md` in the backend repo
7. Commits and pushes workspace repo (includes updated workspace `PROJECT_STATUS.md`)

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
| **Multi-phase epic / IN_PROGRESS** (see policy) | Interactive: requires `ADVANCE`; `--advance-roadmap` refused unless `--force-advance-roadmap` |

### Dry-run preview example (WebPay — multi-phase safety ON)

```
--- Roadmap Auto-Advance Preview ---
Current active task: Payment Provider Integration (WebPay placeholder)
Next detected task: Notifications
Can auto-advance: YES
Multi-phase safety triggered: YES
  Signal: contains 'Phase'
  Signal: contains 'Remaining'
  Signal: Status is IN_PROGRESS
Note: interactive advance requires typing ADVANCE; --advance-roadmap requires --force-advance-roadmap.
```

### When to override manually

- Shipped work that does **not** match the current active task
- Multiple milestones in one release
- Roadmap structure was edited by hand and no longer matches expected sections
- You need custom **Completed** notes or milestone counts beyond auto-increment

In those cases, answer **N** and edit `MVP_ROADMAP.md` manually (or ask Cursor with the usual prompt).
