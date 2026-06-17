# Migration to standard Melomanos layout

Safe, reversible plan to move three separate repos under one root folder.

**Status:** Prepared — **do not run the move steps until preconditions are met.**

Related: [README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md) (path config and env vars).

---

## 1. Preconditions

Complete these checks **before** moving anything.

### All repos clean

From each repo root, confirm no uncommitted work:

```powershell
cd C:\melomanos_market
git status --short

cd C:\melomanos-frontend
git status --short

cd C:\melomanos_workspace
git status --short
```

Each command should print nothing (or only untracked files you intend to keep or commit first). Commit or stash anything you need to keep.

### All commits pushed

```powershell
cd C:\melomanos_market
git fetch origin
git status

cd C:\melomanos-frontend
git fetch origin
git status

cd C:\melomanos_workspace
git fetch origin
git status
```

Resolve any “ahead of origin” state before migration (push or note commits you are willing to lose on rollback).

### Backup recommendation

Moving folders preserves git history, but a backup avoids pain if something goes wrong:

1. **Preferred:** Ensure all three repos are pushed to remote (see above).
2. **Optional file backup:** Copy each folder to a dated archive, e.g.:
   ```powershell
   $stamp = Get-Date -Format "yyyy-MM-dd"
   Copy-Item -Recurse C:\melomanos_market "C:\Backups\melomanos_market_$stamp"
   Copy-Item -Recurse C:\melomanos-frontend "C:\Backups\melomanos-frontend_$stamp"
   Copy-Item -Recurse C:\melomanos_workspace "C:\Backups\melomanos_workspace_$stamp"
   ```
3. **Do not** run migration while a `finish_task.py` release or audit is in progress.

### Current paths (source)

| Role | Path | Git branch |
|------|------|------------|
| Backend | `C:\melomanos_market` | `main` |
| Frontend | `C:\melomanos-frontend` | `master` |
| Workspace | `C:\melomanos_workspace` | (workspace repo) |

### Target paths (destination)

```
C:\melomanos\
├── backend\      ← was C:\melomanos_market
├── frontend\     ← was C:\melomanos-frontend
└── workspace\    ← was C:\melomanos_workspace
```

| Role | Path |
|------|------|
| Backend | `C:\melomanos\backend` |
| Frontend | `C:\melomanos\frontend` |
| Workspace | `C:\melomanos\workspace` |

Workspace scripts (`melomanos_paths.py`) read `MELOMANOS_*_DIR` env vars first, then fall back to legacy defaults. **After migration you must set the env vars** (or scripts will still look at the old `C:\melomanos_*` paths).

---

## 2. Step-by-step migration (PowerShell)

Run in an **elevated or normal** PowerShell window. Close Cursor terminals that use the old paths before step 3.

### 2.1 Create root folder

```powershell
New-Item -ItemType Directory -Path C:\melomanos -Force
```

Confirm `C:\melomanos` is empty (or only contains files you placed there intentionally).

### 2.2 Stop running backend / frontend / Node / Python safely

**A. Stop the dev launcher (if running)**

- In the terminal running `py run_melomanos.py`, press **Enter** or **Ctrl+C** and wait for “Melomanos stopped.”

**B. Clear stale listeners on dev ports (recommended)**

From workspace (still at old path for now):

```powershell
cd C:\melomanos_workspace
py run_melomanos.py --kill-stale
```

This targets processes on ports **8000** (backend) and **3000** (frontend). It does not kill arbitrary Python/Node processes.

**C. Verify ports are free**

```powershell
netstat -ano | findstr ":8000"
netstat -ano | findstr ":3000"
```

No `LISTENING` lines should remain for those ports. If they do, note the PID and stop only that process:

```powershell
taskkill /PID <pid> /F
```

**D. Close extra dev terminals**

Stop any manual `py run.py`, `npm run dev`, or Playwright runs in separate terminals.

**E. Close IDEs using old folders (recommended)**

Close Cursor/VS Code windows rooted at `C:\melomanos_market`, `C:\melomanos-frontend`, or `C:\melomanos_workspace` so nothing holds file locks during the move.

### 2.3 Move each folder

Use `Move-Item` (same volume — fast rename). Order does not matter if source paths still exist.

```powershell
Move-Item -Path C:\melomanos_market -Destination C:\melomanos\backend
Move-Item -Path C:\melomanos-frontend -Destination C:\melomanos\frontend
Move-Item -Path C:\melomanos_workspace -Destination C:\melomanos\workspace
```

Verify:

```powershell
Test-Path C:\melomanos\backend\.git
Test-Path C:\melomanos\frontend\.git
Test-Path C:\melomanos\workspace\.git
```

All three should return `True`. Legacy paths should no longer exist:

```powershell
Test-Path C:\melomanos_market      # False
Test-Path C:\melomanos-frontend    # False
Test-Path C:\melomanos_workspace   # False
```

### 2.4 Set user environment variables (persistent)

Set **User** scope variables (no admin required). **Close and reopen** terminals and Cursor after this.

```powershell
[System.Environment]::SetEnvironmentVariable("MELOMANOS_BACKEND_DIR", "C:\melomanos\backend", "User")
[System.Environment]::SetEnvironmentVariable("MELOMANOS_FRONTEND_DIR", "C:\melomanos\frontend", "User")
[System.Environment]::SetEnvironmentVariable("MELOMANOS_WORKSPACE_DIR", "C:\melomanos\workspace", "User")
```

Optional — current session only (until window closes):

```powershell
$env:MELOMANOS_BACKEND_DIR = "C:\melomanos\backend"
$env:MELOMANOS_FRONTEND_DIR = "C:\melomanos\frontend"
$env:MELOMANOS_WORKSPACE_DIR = "C:\melomanos\workspace"
```

Confirm resolution (new terminal):

```powershell
cd C:\melomanos\workspace
py -c "import melomanos_paths as p; print(p.BACKEND_DIR); print(p.FRONTEND_DIR); print(p.WORKSPACE_DIR)"
```

Expected output:

```
C:\melomanos\backend
C:\melomanos\frontend
C:\melomanos\workspace
```

---

## 3. Validation commands

Run from the new workspace after env vars are active.

### 3.1 Status and path wiring (no servers required)

```powershell
cd C:\melomanos\workspace
py project_status.py --check
py finish_task.py --dry-run
```

- `project_status.py --check` → exit code **0**, all markers OK.
- `finish_task.py --dry-run` → exit code **0**, shows git status for backend/frontend at new paths.

### 3.2 Start dev environment

```powershell
cd C:\melomanos\workspace
py run_melomanos.py --kill-stale --no-wait
py run_melomanos.py --check
```

- `--kill-stale --no-wait` starts backend + frontend, waits until ready, leaves processes running.
- `--check` → exit code **0** when both URLs respond.

### 3.3 Full workflow (when ready)

**Quality Gate only:**

```powershell
cd C:\melomanos\workspace
py run_audit.py
```

**Full finish workflow** (interactive — audit, commit, push):

```powershell
cd C:\melomanos\workspace
py finish_task.py
```

Use `py finish_task.py --dry-run` first if you only want a preview.

---

## 4. Rollback plan

If something fails, reverse the move and remove env vars. **Stop all Melomanos processes first** (section 2.2).

### 4.1 Move folders back

Only if `C:\melomanos\backend`, `frontend`, and `workspace` exist and legacy paths do not:

```powershell
Move-Item -Path C:\melomanos\backend -Destination C:\melomanos_market
Move-Item -Path C:\melomanos\frontend -Destination C:\melomanos-frontend
Move-Item -Path C:\melomanos\workspace -Destination C:\melomanos_workspace
```

Optional — remove empty root:

```powershell
Remove-Item C:\melomanos -Force -ErrorAction SilentlyContinue
```

### 4.2 Clear environment variables

Remove User-scope variables:

```powershell
[System.Environment]::SetEnvironmentVariable("MELOMANOS_BACKEND_DIR", $null, "User")
[System.Environment]::SetEnvironmentVariable("MELOMANOS_FRONTEND_DIR", $null, "User")
[System.Environment]::SetEnvironmentVariable("MELOMANOS_WORKSPACE_DIR", $null, "User")
```

Clear current session:

```powershell
Remove-Item Env:MELOMANOS_BACKEND_DIR -ErrorAction SilentlyContinue
Remove-Item Env:MELOMANOS_FRONTEND_DIR -ErrorAction SilentlyContinue
Remove-Item Env:MELOMANOS_WORKSPACE_DIR -ErrorAction SilentlyContinue
```

Restart terminal. Scripts fall back to legacy defaults in `melomanos_paths.py`:

- `C:\melomanos_market`
- `C:\melomanos-frontend`
- `C:\melomanos_workspace`

Verify:

```powershell
cd C:\melomanos_workspace
py -c "import melomanos_paths as p; print(p.BACKEND_DIR); print(p.FRONTEND_DIR); print(p.WORKSPACE_DIR)"
```

### 4.3 Re-open Cursor at old paths

Open `C:\melomanos_workspace` (and backend/frontend folders) as before.

---

## 5. Cursor usage after migration

### Command center: workspace

Open **`C:\melomanos\workspace`** as the primary Cursor window for:

- `py run_melomanos.py`, `py run_audit.py`, `py finish_task.py`
- `py project_status.py`
- Cross-repo planning, status updates, and release workflow

Workspace scripts resolve backend/frontend via `MELOMANOS_*_DIR` — you do not need to hardcode old paths in prompts.

### Backend / frontend windows

Open separately when the task is **repo-specific**:

| Window root | Use for |
|-------------|---------|
| `C:\melomanos\backend` | API, models, pytest, `run.py`, backend-only changes |
| `C:\melomanos\frontend` | Next.js UI, components, Playwright, `npm run dev` |

You can use a multi-root workspace (`melomanos.code-workspace`) with all three folders; still treat **workspace** as the orchestration root for scripts.

### Where to paste prompts

| Prompt type | Paste in Cursor window |
|-------------|------------------------|
| Release, audit, roadmap advance, `PROJECT_STATUS.md` | **workspace** |
| SDD / project reports spanning backend + frontend | **workspace** (agent uses env paths) |
| Backend feature implementation, pytest fixes | **backend** |
| Frontend UI, E2E, build fixes | **frontend** |
| “Run validation” (`--check`, `--dry-run`, `run_audit.py`) | **workspace** terminal |

After migration, update any saved prompts or rules that mention `C:\melomanos_market` or `C:\melomanos-frontend` to the new paths (or say “use `melomanos_paths` / env vars”).

---

## 6. SDD recommendation

**Spec-Driven Development (SDD)** and project-level orchestration should stay **workspace-centric**; implementation stays in the repos that own the code.

### Run from workspace

- Milestone / release planning tied to `MVP_ROADMAP.md` and finish workflow
- Quality Gate and E2E orchestration (`run_audit.py`, `finish_task.py`)
- Cross-cutting reports (status summaries, audit results, “what shipped”)
- Prompts that read or update **roadmap**, **workspace** `PROJECT_STATUS.md`, or multi-repo checklists

### Run from backend or frontend

- Code changes, refactors, and tests confined to one repo
- “Implement endpoint X”, “fix component Y”, “add Playwright test Z”
- Local run/debug: `py run.py` (backend), `npm run dev` (frontend)

### Where docs live (after migration)

| Document | Location |
|----------|----------|
| `MVP_ROADMAP.md` | `C:\melomanos\backend` |
| Backend `PROJECT_STATUS.md` | `C:\melomanos\backend` |
| Workspace `PROJECT_STATUS.md` (Ernesto/Daniela snapshot) | `C:\melomanos\workspace` |
| Layout / migration / runbooks | `C:\melomanos\workspace` |
| AI OS / architecture / quality gate (if present) | Backend `.cursor/rules`, docs per repo layout |

SDD prompts that **author specs or reports** should reference workspace + backend roadmap paths; prompts that **implement** should be opened in the repo that contains the code under change.

---

## Quick checklist

- [ ] All three repos clean and pushed
- [ ] Backup or remote confirmed
- [ ] Dev servers stopped; ports 8000/3000 free
- [ ] `C:\melomanos` created
- [ ] Three `Move-Item` commands completed
- [ ] `MELOMANOS_*_DIR` user env vars set
- [ ] New terminal: path probe shows `C:\melomanos\...`
- [ ] `py project_status.py --check` → OK
- [ ] `py finish_task.py --dry-run` → OK
- [ ] `py run_melomanos.py --kill-stale --no-wait` + `--check` → OK
- [ ] Cursor reopened at `C:\melomanos\workspace`
