# Melomanos audit

Single-command validation for backend and frontend.

## Requirements

Before running the audit, start both services:

| Service | URL |
|---------|-----|
| Backend | http://127.0.0.1:8000 |
| Frontend | http://localhost:3000 |

Example (separate terminals or use `run_melomanos.py`):

```powershell
cd C:\melomanos_market
py run.py
```

```powershell
cd C:\melomanos-frontend
npm run dev
```

E2E tests also expect test users (`buyer@example.com` / `seller@example.com`, password `devpassword12`); the Playwright global setup registers them if missing.

Install Playwright browsers once in the frontend repo:

```powershell
cd C:\melomanos-frontend
npx playwright install chromium
```

## Run

```powershell
cd C:\melomanos_workspace
py run_audit.py
```

## Steps (sequential)

1. **Backend tests** — `py -m pytest` in `C:\melomanos_market`
2. **Frontend build** — `npm run build` in `C:\melomanos-frontend`
3. **Playwright E2E** — `npm run test:e2e` in `C:\melomanos-frontend`

The audit stops on the first failing step and exits with a non-zero code.

## Success output

```
================================
Melomanos audit passed
================================
```
