# Melomanos audit

Tiered validation for backend and frontend. Repo paths: `melomanos_paths.py` ([README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md)).

Default layout (no env vars):

| Repo | Path |
|------|------|
| Backend | `C:\melomanos\backend` |
| Frontend | `C:\melomanos\frontend` |
| Workspace | `C:\melomanos\workspace` |

Override with `MELOMANOS_BACKEND_DIR`, `MELOMANOS_FRONTEND_DIR`, `MELOMANOS_WORKSPACE_DIR`.

## Gate tiers

| Tier | Command | Steps | Starts local stack? |
|------|---------|-------|---------------------|
| **Fast Gate** | `py run_audit.py --backend-only` | pytest only | No |
| **Quality Gate** | `py run_audit.py --skip-e2e` | pytest + `npm run build` | No |
| **Full audit** | `py run_audit.py` | pytest + build + Playwright E2E | **Yes, if needed** |
| **Release Gate** | `py finish_task.py` | Full audit, then commit/push + status updates | **Yes, if needed** |

Run from the workspace directory:

```powershell
cd C:\melomanos\workspace
py run_audit.py --help
```

## Requirements

### Fast Gate / Quality Gate

No running services required (pytest uses isolated SQLite; build is offline). Stack is **not** started.

### Full audit (E2E)

**Full audit auto-starts the local stack** when backend and frontend are not already reachable:

| Service | Probe URL |
|---------|-----------|
| Backend | `http://127.0.0.1:8000/health` or `/listings?limit=1` |
| Frontend | `http://localhost:3000` |

Behavior:

1. **Checking E2E prerequisites…**
2. If both are already up → **Backend READY**, **Frontend READY**, **E2E prerequisites READY** (no restart).
3. If either is down → **Starting local stack for E2E…** → `py run_melomanos.py --kill-stale --no-wait`
4. Wait for readiness, then run Playwright.

If the stack does not become ready within the timeout, the audit fails with:

```powershell
py run_melomanos.py --kill-stale --no-wait
```

Manual start (optional, same as automation):

```powershell
cd C:\melomanos\workspace
py run_melomanos.py --kill-stale --no-wait
```

E2E tests expect test users (`buyer@example.com` / `seller@example.com`, password `devpassword12`); Playwright global setup registers them if missing.

Install Playwright browsers once in the frontend repo:

```powershell
cd C:\melomanos\frontend
npx playwright install chromium
```

## Steps (sequential)

The audit runs only the steps for the selected tier. It stops on the first failure.

| Step | Fast | Quality | Full |
|------|:----:|:-------:|:----:|
| Backend — `py -m pytest` in `backend/` | ✓ | ✓ | ✓ |
| Frontend — `npm run build` in `frontend/` | | ✓ | ✓ |
| E2E stack check / auto-start | | | ✓ (if E2E runs) |
| Playwright — `npm run test:e2e` in `frontend/` | | | ✓ |

## Success output

```
================================
Melomanos audit passed
================================
```

## Related docs

- [`QUALITY_GATE.md`](./QUALITY_GATE.md) — Definition of Done
- [`../backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md) — testing pyramid and CI
- [`TESTING_OPTIMIZATION_REPORT.md`](./TESTING_OPTIMIZATION_REPORT.md) — audit and optimization notes
# Operational authority

Audit commands are technical references, not standing permission to execute. First parse the canonical JSON authority block in `PROJECT_STATUS.md` and require the exact mission, `READY`, and the named validation action. A gate remains read-only unless that command is explicitly authorized.
