# Melomanos dev launcher (`run_melomanos.py`)

Starts backend (`C:\melomanos_market`) and frontend (`C:\melomanos-frontend`) with **readiness checks** before reporting success.

Required for local development and **Quality Gate / E2E** preparation (see [README_AUDIT.md](./README_AUDIT.md)).

## Commands

### Start dev environment (default)

```powershell
cd C:\melomanos_workspace
py run_melomanos.py
```

- Optionally clears nothing (use `--kill-stale` if ports are busy)
- Starts backend and frontend
- Polls until both respond (up to 30s, every 2s):
  - Backend: `http://127.0.0.1:8000/listings?limit=1`
  - Frontend: `http://localhost:3000`
- Prints `Backend READY`, `Frontend READY`, `Melomanos READY`
- Keeps running until **Enter** or **Ctrl+C**; then terminates child processes

### Check readiness only

```powershell
py run_melomanos.py --check
```

Does **not** start services. Exit code `0` if both URLs are reachable; `1` otherwise.

### Clean stale ports and start

```powershell
py run_melomanos.py --kill-stale
```

Kills Windows processes listening on ports **8000** and **3000**, then starts fresh.

Use when a previous dev server left ports occupied.

### Automation / CI prep (no interactive wait)

```powershell
py run_melomanos.py --kill-stale --no-wait
```

- Kills stale listeners on 8000/3000
- Starts backend + frontend
- Waits until ready
- Prints `Melomanos READY` and **exits** (processes keep running)
- Safe for Cursor/scripts that must not block on `input()`

Combine flags:

```powershell
py run_melomanos.py --check
py run_melomanos.py --no-wait
py run_melomanos.py --kill-stale --no-wait
```

## Port 3000 requirement

E2E expects **http://localhost:3000**. If Next.js binds to **3001** because 3000 is taken, the launcher **fails** unless you used `--kill-stale` first.

## Output example

```
Starting Melomanos...

Backend:  http://127.0.0.1:8000
Frontend: http://localhost:3000

Backend READY
Frontend READY
Melomanos READY

Backend:  http://127.0.0.1:8000
Frontend: http://localhost:3000

Press CTRL+C or Enter to stop both.
```

## URLs

| Service | URL |
|---------|-----|
| Backend API | http://127.0.0.1:8000 |
| Frontend app | http://localhost:3000 |

## Related

- [README_LOCAL_RUN.md](./README_LOCAL_RUN.md) — run backend or frontend alone
- [README_FINISH_TASK.md](./README_FINISH_TASK.md) — release workflow after Quality Gate
- [README_AUDIT.md](./README_AUDIT.md) — `run_audit.py` (requires dev servers up)
