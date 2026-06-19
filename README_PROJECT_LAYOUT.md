# Melomanos project layout

This document describes where Melomanos repos live today, the recommended future layout, and how to migrate without breaking workspace scripts.

## Current layout (today)

Single root folder for Melomanos development:

```
C:\melomanos\
├── backend\     # backend (git: main)
├── frontend\    # frontend (git: master)
└── workspace\   # dev scripts, PROJECT_STATUS.md, finish workflow
```

Workspace Python scripts resolve these paths via `melomanos_paths.py`. With no environment variables set, defaults match the paths above.

## Legacy layout (pre-migration)

If repos still live at the old paths, set env vars (see below) or move folders into `C:\melomanos\`:

```
C:\
├── melomanos_market\      # was backend
├── melomanos-frontend\    # was frontend
└── melomanos_workspace\   # was workspace
```

## Recommended future layout

Same as **current layout** — migration to `C:\melomanos\` is complete when all three repos live under that root.

## Path configuration (`melomanos_paths.py`)

All workspace scripts import paths from `melomanos_paths.py`:

| Symbol | Purpose |
|--------|---------|
| `BACKEND_DIR` | Backend repo root |
| `FRONTEND_DIR` | Frontend repo root |
| `WORKSPACE_DIR` | Workspace repo root |
| `ROADMAP_FILE` | `BACKEND_DIR / MVP_ROADMAP.md` |
| `BACKEND_STATUS_FILE` | `BACKEND_DIR / PROJECT_STATUS.md` |
| `WORKSPACE_STATUS_FILE` | `WORKSPACE_DIR / PROJECT_STATUS.md` |

Resolution order: **environment variable → default (current layout)**.

## Required environment variables (after migration)

Set these only if repos are **not** at `C:\melomanos\{backend,frontend,workspace}` (e.g. legacy paths):

| Variable | Example | Default (no env var) |
|----------|---------|----------------------|
| `MELOMANOS_BACKEND_DIR` | `C:\melomanos\backend` | `C:\melomanos\backend` |
| `MELOMANOS_FRONTEND_DIR` | `C:\melomanos\frontend` | `C:\melomanos\frontend` |
| `MELOMANOS_WORKSPACE_DIR` | `C:\melomanos\workspace` | `C:\melomanos\workspace` |

### PowerShell (session)

```powershell
$env:MELOMANOS_BACKEND_DIR = "C:\melomanos\backend"
$env:MELOMANOS_FRONTEND_DIR = "C:\melomanos\frontend"
$env:MELOMANOS_WORKSPACE_DIR = "C:\melomanos\workspace"
```

### PowerShell (persistent, user)

```powershell
[System.Environment]::SetEnvironmentVariable("MELOMANOS_BACKEND_DIR", "C:\melomanos\backend", "User")
[System.Environment]::SetEnvironmentVariable("MELOMANOS_FRONTEND_DIR", "C:\melomanos\frontend", "User")
[System.Environment]::SetEnvironmentVariable("MELOMANOS_WORKSPACE_DIR", "C:\melomanos\workspace", "User")
```

Restart the terminal after persistent changes.

## Migration plan

1. **Stop running services** — close `run_melomanos.py`, local API, and frontend dev server.
2. **Create root** — `mkdir C:\melomanos`
3. **Move repos** (git history preserved):
   - `C:\melomanos_market` → `C:\melomanos\backend`
   - `C:\melomanos-frontend` → `C:\melomanos\frontend`
   - `C:\melomanos_workspace` → `C:\melomanos\workspace`
4. **Set environment variables** (see above) **or** update machine/user PATH habits to `cd C:\melomanos\workspace`.
5. **Do not change** backend/frontend application code for this layout step.
6. **Validate** (from workspace directory):

   ```powershell
   cd C:\melomanos\workspace
   py run_melomanos.py --check
   py finish_task.py --dry-run
   py project_status.py --check
   ```

7. **Update bookmarks / IDE workspace roots** to the new paths.
8. **Optional:** add a small `C:\melomanos\README.md` pointing to `workspace\` for scripts.

### Rollback

Move folders back to the original names and set `MELOMANOS_*` env vars to those legacy paths (or clear them if defaults are changed again).

## Commands before vs after migration

| Task | Before (current) | After migration |
|------|------------------|-----------------|
| Workspace scripts | `cd C:\melomanos_workspace` | `cd C:\melomanos\workspace` |
| Start backend only | `cd C:\melomanos_market` | `cd C:\melomanos\backend` |
| Start frontend only | `cd C:\melomanos-frontend` | `cd C:\melomanos\frontend` |
| Dev launcher | `py run_melomanos.py` | Same (from workspace dir) |
| Quality Gate | `py run_audit.py` | Same |
| Finish workflow | `py finish_task.py` | Same |
| Status check | `py project_status.py --check` | Same |

Script **invocation** is unchanged; only the **working directory** and underlying repo paths change.

## Scripts using `melomanos_paths.py`

- `run_melomanos.py` — backend/frontend launch paths
- `run_audit.py` — audit `cwd` for pytest, build, E2E
- `finish_task.py` — git repos and workspace root
- `project_status.py` — workspace status file and roadmap
- `roadmap_advance.py` — roadmap and status file paths

## Documentation with legacy paths

These README files still show `C:\melomanos_*` paths for the **current** layout. After migration, substitute `C:\melomanos\backend`, `C:\melomanos\frontend`, and `C:\melomanos\workspace`, or rely on env vars and run commands from the new workspace folder:

- `README_LOCAL_RUN.md`
- `README_RUN_MELOMANOS.md`
- `README_AUDIT.md`
- `README_FINISH_TASK.md`
- `README_STATUS.md`

## Verify paths without starting services

```powershell
py -c "import melomanos_paths as p; print(p.BACKEND_DIR); print(p.FRONTEND_DIR); print(p.WORKSPACE_DIR)"
```

Expected today (no env vars): `C:\melomanos_market`, `C:\melomanos-frontend`, `C:\melomanos_workspace`.
