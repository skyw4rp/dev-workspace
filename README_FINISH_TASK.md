# Melomanos finish task (v2)

Automates **Quality Gate → commit → push** for backend and frontend. Commit messages are suggested from **actual changed files**, not only the roadmap.

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
- Does **not** run audit, commit, or push

## Flow

1. **Quality Gate** — `py run_audit.py` (skipped in `--dry-run`)
2. **Git status** — list changed files per repo
3. **Smart commit prompts** — file-based suggestion + optional roadmap fallback
4. **Confirmation** — `Proceed? (Y/N)` if any repo will commit
5. **Final summary** — per-repo outcome

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

| Repo | Path | Branch |
|------|------|--------|
| Backend | `C:\melomanos_market` | `main` |
| Frontend | `C:\melomanos-frontend` | `master` |

Each git command is printed before it runs. The script stops on the first failing git command. No force push; no history rewrite.

## Project status (optional)

After a successful run (not aborted), you may be asked to update `PROJECT_STATUS.md`. See [README_STATUS.md](./README_STATUS.md).
