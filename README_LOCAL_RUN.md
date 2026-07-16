# Melomanos — local run

Path layout: [README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md) (env vars `MELOMANOS_*_DIR`).

## Backend only

```powershell
cd C:\melomanos_market
py run.py
```

API: http://127.0.0.1:8000

## Frontend only

```powershell
cd C:\melomanos-frontend
py run_frontend.py
```

App: http://localhost:3000

## Backend + frontend

```powershell
cd C:\melomanos_workspace
py run_melomanos.py
```

- Backend: http://127.0.0.1:8000  
- Frontend: http://localhost:3000  

Press **Enter** or **CTRL+C** in the launcher terminal to stop both processes.

See [README_RUN_MELOMANOS.md](./README_RUN_MELOMANOS.md) for `--check`, `--no-wait`, and `--kill-stale`.
# Operational authority

These local commands are references only and do not authorize execution. Read and parse the canonical JSON block in `PROJECT_STATUS.md` first; run a command only for its exact `READY` mission and explicitly allowed action class.
