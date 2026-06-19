# Melómanos Testing Optimization Report

**Date:** 2026-06-17  
**Scope:** Backend pytest, frontend build, Playwright E2E, workspace release tooling, CI, deployment validation  
**Action taken:** Audit only — no code or workflow changes

**Related docs:** [`backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md), [`QUALITY_GATE.md`](QUALITY_GATE.md), [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md), [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md)

---

## Executive summary

Melómanos has a **mature local quality gate** for an MVP: 239 backend tests, 33 Playwright E2E specs, frontend production build, and a workspace orchestrator (`run_audit.py` → `finish_task.py`) that ties release to `PROJECT_STATUS.md`. Phase 4 added **split-repo GitHub Actions** (backend: Postgres migration smoke + pytest; frontend: build only).

The main optimization opportunity is **tiered gates**: today every release runs the full ~2.5 min pytest suite plus full E2E (~5–15+ min with live stack), even for doc-only or backend-only changes. The slowest cost is **E2E serial execution** and **pytest DB reset per test** (`drop_all` / `create_all`), not individual test logic.

**Top recommendations (low maintenance):**

1. Add **fast / full / release / deploy** gate tiers (document + script flags).
2. Add **`npm run lint`** to frontend CI (cheap, already in `package.json`).
3. Extend `run_audit.py` with `--skip-e2e` and `--backend-only` for iterative work.
4. Set `MELOMANOS_*_DIR` env vars (or update path defaults) so workspace scripts resolve `C:\melomanos\` reliably.

---

## 1. Current validation flow

### 1.1 Repository layout

| Repo | Path (current dev) | Default in `melomanos_paths.py` | Branch |
|------|--------------------|----------------------------------|--------|
| Backend | `C:\melomanos\backend` | `C:\melomanos_market` | `main` |
| Frontend | `C:\melomanos\frontend` | `C:\melomanos-frontend` | `master` |
| Workspace | `C:\melomanos\workspace` | `C:\melomanos_workspace` | `main` |

Workspace scripts (`run_audit.py`, `finish_task.py`, `project_status.py`) depend on `MELOMANOS_BACKEND_DIR`, `MELOMANOS_FRONTEND_DIR`, `MELOMANOS_WORKSPACE_DIR` when not using legacy defaults. See [`README_PROJECT_LAYOUT.md`](README_PROJECT_LAYOUT.md).

### 1.2 Validation layers (documented pyramid)

```
        ┌─────────────────────┐
        │  E2E — 33 specs     │  Playwright, live backend + frontend
        ├─────────────────────┤
        │  Frontend build     │  next build + TypeScript
        ├─────────────────────┤
        │  Backend — 239 tests│  pytest + SQLite (conftest)
        └─────────────────────┘
```

### 1.3 Local developer flow

| Step | Command | When | Prerequisites |
|------|---------|------|---------------|
| Backend only | `cd backend && py -m pytest` | Every backend change | None |
| Frontend only | `cd frontend && npm run build` | UI / types changes | None |
| Lint (optional) | `cd frontend && npm run lint` | Ad hoc | Not in Quality Gate |
| E2E | `cd frontend && npm run test:e2e` | User flows, release | Backend :8000, frontend :3000 |
| Dev stack | `py run_melomanos.py` (workspace) | Before E2E | Kills stale ports optional |
| WebPay E2E | `py run_melomanos.py --e2e-webpay` | WebPay specs | Special backend env |
| Full audit | `py run_audit.py` (workspace) | Pre-release | E2E stack must be up |
| Release | `py finish_task.py` | Milestone close | Runs audit first, then git |

### 1.4 `run_audit.py` (workspace)

Sequential three-step audit:

1. `[1/3]` `py -m pytest` in backend  
2. `[2/3]` `npm run build` in frontend  
3. `[3/3]` `npm run test:e2e` in frontend  

**Does not run:** Alembic migration smoke, ESLint, deployment compose validation, or `/health` probe.

### 1.5 `finish_task.py` (workspace)

Release orchestrator v2:

1. Optional `--dry-run` (plan only, no audit)
2. **`run_quality_gate()`** → invokes `run_audit.py` (full audit)
3. Interactive **Proceed? (Y/N)**
4. Smart commit messages per repo (backend / frontend / workspace)
5. `update_project_status()` → writes marker sections in `PROJECT_STATUS.md`
6. Optional `--advance-roadmap` → `MVP_ROADMAP.md` + status focus updates
7. Workspace commit last (includes updated status)

Flags: `--skip-backend`, `--skip-frontend`, `--skip-workspace`, custom `--*-message`.

### 1.6 `project_status.py` (workspace)

- Maintains `PROJECT_STATUS.md` via HTML comment markers (`<!-- STATUS:LAST_QUALITY_GATE_* -->`, etc.)
- Called from `finish_task.py` after successful release commits
- CLI: `--check` (marker validation), `--update-manual`, default summary print
- **Always records QG as PASSED** when called from release path (does not re-run tests)

### 1.7 CI (GitHub Actions — Phase 4)

| Repo | Workflow | Trigger | Steps |
|------|----------|---------|-------|
| Backend | `.github/workflows/ci.yml` | push/PR → `main`, `master` | Postgres 15 → `alembic upgrade head` → `alembic current` → `pytest` |
| Frontend | `.github/workflows/ci.yml` | push/PR → `main`, `master` | `npm ci` → `npm run build` |

**Not in CI:** E2E, ESLint, workspace `run_audit.py`, deployment compose, security scans.

### 1.8 Deployment validation (manual / docs)

| Artifact | Purpose |
|----------|---------|
| [`backend/scripts/pre_deploy_checklist.py`](../backend/scripts/pre_deploy_checklist.py) | Prints operator checklist; optional `docker compose config` |
| [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md) | Pre-deploy checklist, migrate, health, logs, rollback |
| [`backend/README_DEPLOYMENT.md`](../backend/README_DEPLOYMENT.md) | Compose commands, CI reference |
| Docker prod compose | `docker-compose.prod.yml` + Caddy — validated locally via `config`, not automated in audit |

### 1.9 E2E architecture

- **Tool:** Playwright (`playwright.config.ts`)
- **Specs:** 4 files — `melomanos.spec.ts` (20), `webpay-checkout.spec.ts` (8), `webpay-lifecycle.spec.ts` (3), `notifications.spec.ts` (2) → **33 tests**
- **Config:** `workers: 1`, `fullyParallel: false`, `timeout: 60_000` ms, Chromium only
- **global-setup:** Asserts backend (`/listings?limit=1`) + frontend reachable; registers test users; prepares seller account
- **Env overrides:** `E2E_BASE_URL`, `E2E_API_URL`, `E2E_*_EMAIL`, `E2E_PASSWORD`

### 1.10 Backend test architecture

- **29 test modules**, **239 tests** (2026-06-17 baseline)
- **DB:** SQLite file; **`autouse` fixture** runs `Base.metadata.drop_all()` + `create_all()` **before every test**
- **Env:** `conftest.py` pins test secrets, `PAYMENT_PROVIDER_MODE=simulate`, `CORS_ORIGINS` localhost
- **Style:** API integration tests via `TestClient`; OpenAI mocked in NL search tests
- **No pytest markers** for fast/slow/integration (only `@pytest.mark.parametrize` in a few files)

---

## 2. Strengths

1. **Broad backend coverage** across marketplace domains: orders/escrow, payments (simulate + WebPay placeholder), disputes, admin, notifications, messaging safety, subscriptions, NL search.
2. **Clear Definition of Done** linking tests, build, E2E, git, and docs (`TESTING_STRATEGY.md`, `QUALITY_GATE.md`).
3. **Release automation** with dry-run, skip flags, and roadmap integration reduces operator error.
4. **E2E covers real journeys** — full order lifecycle, disputes, admin resolution, WebPay placeholder, notifications — not just smoke clicks.
5. **CI migration smoke** validates Alembic on **empty PostgreSQL** (production-relevant path separate from pytest SQLite).
6. **Test env isolation** in `conftest.py` prevents local `.env.local` WebPay settings from breaking the default suite.
7. **Deployment docs + checklist script** provide a path to Phase 5 without ad-hoc ops knowledge.
8. **Stable E2E selectors** (`data-testid` on notifications) and global setup reduce repeated manual prep.

---

## 3. Weaknesses

1. **Single monolithic Quality Gate** — `finish_task.py` always runs full E2E; no tier for backend-only or docs-only changes.
2. **pytest uses SQLite; production uses PostgreSQL** — CI validates migrations on Postgres, but **239 tests never run against Postgres**. Driver/SQL dialect edge cases can slip through.
3. **Per-test schema rebuild is expensive** — ~142 s total runtime; **setup dominates** (0.8–1.2 s per test for DB reset + login fixtures), not test bodies.
4. **E2E not in CI** — regressions discovered only at release time; requires manual stack management.
5. **E2E serial (`workers: 1`)** — safe but slow; no sharding or smoke subset.
6. **No frontend unit/component tests** — only build + E2E; UI logic errors may surface late.
7. **ESLint not gated** — `npm run lint` exists but is excluded from audit, CI, and Quality Gate.
8. **`run_audit.py` gaps** — no Alembic smoke, no `/health` check, no compose config, no lint.
9. **Path defaults mismatch** — scripts default to legacy `C:\melomanos_market` paths; current layout is `C:\melomanos\{backend,frontend,workspace}` unless env vars are set.
10. **`PROJECT_STATUS.md` drift** — marker sections updated by automation, but body sections (e.g. Active task) can lag roadmap.
11. **`project_status.py` trusts audit** — records PASSED without verifying individual step outcomes programmatically.
12. **WebPay E2E split brain** — default pytest uses `simulate`; WebPay lifecycle specs need `--e2e-webpay` backend mode (documented but easy to forget).
13. **Three repos, three CIs** — no unified “monorepo status” badge; workspace has no CI of its own.

---

## 4. Slowest / most expensive checks

Measured locally (2026-06-17, Windows, representative hardware):

| Check | Approx. duration | Cost drivers |
|-------|------------------|--------------|
| **Playwright E2E (33 tests)** | **~5–15+ min** | Browser, serial workers, real HTTP, global-setup, long flows (disputes, lifecycle) |
| **`py -m pytest` (239 tests)** | **~2.4 min** | `drop_all`/`create_all` × 239; repeated register/login in fixtures |
| **`npm run build`** | **~5–10 s** | Next.js compile + TypeScript |
| **Backend CI (GitHub)** | **~3–5 min est.** | Postgres service wait + pip install + migrate + pytest |
| **Frontend CI (GitHub)** | **~2–3 min est.** | `npm ci` + build |
| **`alembic upgrade head` (empty PG)** | **~5–15 s** | Fast; high value |
| **`finish_task.py` (full)** | **Audit + human confirm + git** | Dominated by E2E + pytest |

**Slowest individual pytest tests (call phase):** admin pagination (~1.8 s). **Dominant cost:** fixture setup (DB reset), not business logic.

**Most expensive in operator time:** E2E prerequisite debugging (stack not up, wrong payment mode, stale DB state).

---

## 5. Missing professional checks

Checks common in production-grade teams but **not present** today:

| Category | Gap |
|----------|-----|
| **Static analysis** | No Ruff/mypy/flake8 on backend; ESLint not in CI |
| **Coverage** | No pytest-cov thresholds or trend tracking |
| **PR fast feedback** | No “smoke” pytest subset or path-based test selection |
| **E2E automation** | No Playwright in GitHub Actions (services/containers) |
| **Contract / API** | No OpenAPI schema diff or consumer-driven contracts |
| **Security** | No dependency audit (`pip audit`, `npm audit`), secret scanning, SAST |
| **Performance** | No load/soak tests for listings search or checkout |
| **Migration rollback** | Forward-only policy (documented); no automated downgrade tests |
| **Staging** | No pre-prod environment (explicit MVP decision) |
| **Observability tests** | No automated check of structured logs / correlation IDs in CI |
| **Branch protection** | Not verified in repo settings (requires GitHub config) |
| **Deployment verification** | No automated post-deploy smoke against `/health` (Phase 5) |

---

## 6. Recommended test levels

### 6.1 Fast check (~3 min)

**When:** Every commit, iterative development, backend-only PRs.

| Step | Command |
|------|---------|
| Backend | `py -m pytest -q` *(future: `-m "not slow"` subset)* |
| Frontend (if touched) | `npm run build` |
| Optional | `npm run lint` |

**Skip:** E2E, full audit, migration smoke (unless Alembic files changed).

### 6.2 Full quality gate (~10–20 min)

**When:** Before merge, feature complete, pre-`finish_task.py`.

| Step | Command |
|------|---------|
| Backend | `py -m pytest` |
| Frontend | `npm run build` |
| E2E | `npm run test:e2e` *(stack up via `run_melomanos.py`)* |

**Equivalent today:** `py run_audit.py` (workspace).

### 6.3 Release gate (~15–25 min + git)

**When:** Milestone completion, roadmap advance.

| Step | Command / action |
|------|------------------|
| Full quality gate | `py run_audit.py` |
| Release workflow | `py finish_task.py` (+ optional `--advance-roadmap`) |
| Docs | `PROJECT_STATUS.md`, release notes, roadmap |
| Remote CI | Confirm GitHub Actions green on pushed SHAs |

**Today:** Fully implemented via `finish_task.py`; missing CI confirmation step in script.

### 6.4 Deployment gate (pre–production cutover)

**When:** Phase 5 deploy, hotfix to VPS.

| Step | Command / action |
|------|------------------|
| CI green | Backend + frontend GitHub Actions |
| Checklist | `py scripts/pre_deploy_checklist.py --compose-config` |
| Compose validate | `docker compose -f docker-compose.yml -f docker-compose.prod.yml config` |
| Backup | `pg_dump` per runbook §6 |
| Migrate | `docker compose … exec api alembic upgrade head` |
| Health | `curl -sS https://api.melomanos.cl/health` |
| Smoke | Login, browse, order (manual) |
| Rollback plan | Previous image tag + backup restore documented |

**Today:** Documented in runbook; not wired into `run_audit.py` or CI.

---

## 7. Easy improvements (low maintenance cost)

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| 1 | **Document tiered gates** in `TESTING_STRATEGY.md` + `QUALITY_GATE.md` | Low | High — clarifies when to run what |
| 2 | **`run_audit.py` flags:** `--skip-e2e`, `--skip-build`, `--backend-only` | Low | High — saves 5–15 min on backend-only work |
| 3 | **Frontend CI:** add `npm run lint` | Low | Medium — catches obvious issues early |
| 4 | **Set `MELOMANOS_*_DIR`** in dev shell profile or update `melomanos_paths.py` defaults to `C:\melomanos\` | Low | High — fixes silent wrong-repo audits |
| 5 | **pytest `-m smoke`** — mark ~15–20 critical tests (auth, order create, payment simulate) | Medium | Medium — ~30 s fast path |
| 6 | **`run_melomanos.py --check`** before E2E in docs/scripts | Low | Medium — clearer failure messages |
| 7 | **`finish_task.py --skip-audit`** with explicit `--audit-passed` guard | Low | Medium — escape hatch when E2E already run |
| 8 | **Backend CI:** cache Alembic revision id as artifact / echo in logs | Low | Low — easier deploy audit trail |
| 9 | **Use `/health` in `run_melomanos.py`** instead of `/listings?limit=1` | Low | Low — aligns with deployment probe |
| 10 | **Single `TESTING_OPTIMIZATION_REPORT.md` → link from runbook** | Done | Reference for operators |

### pytest performance (medium effort, defer unless suite > 400 tests)

- Replace per-test `drop_all`/`create_all` with **transaction rollback** or **session-scoped DB** for read-heavy tests.
- Use **`pytest-xdist`** only after fixing shared-state tests (reservations concurrency test may conflict).

---

## 8. What NOT to add yet

| Item | Reason to defer |
|------|-----------------|
| **Full E2E in GitHub Actions** | Flaky, slow, needs 3 services; MVP local gate is sufficient until post-cutover |
| **80% coverage mandate** | High maintenance; team size doesn't justify enforcement yet |
| **Visual regression (Percy, etc.)** | Cost/complexity; UI still evolving |
| **k6 / load testing** | No production traffic baseline; premature |
| **Staging environment** | Explicit MVP decision (Option B, no staging) |
| **Multi-browser E2E matrix** | Chromium-only is adequate for MVP |
| **Contract testing infrastructure** | API surface stable but small team; pytest integration tests suffice |
| **Automated downgrade migration tests** | Forward-only policy; restore-from-backup instead |
| **Dependabot + auto-merge** | Needs branch protection and CI stability first |
| **Workspace repo CI** | Scripts are thin wrappers; validate via manual dry-run |

---

## 9. Recommended implementation plan

### Phase A — Documentation & ergonomics (1–2 hours)

1. Add **tiered gate table** to `TESTING_STRATEGY.md` and `QUALITY_GATE.md` (fast / full / release / deploy).
2. Document required **`MELOMANOS_*_DIR`** for `C:\melomanos\` layout in `README_PROJECT_LAYOUT.md`.
3. Link this report from `DEPLOYMENT_RUNBOOK.md` and `backend/README_DEPLOYMENT.md`.

### Phase B — Script flags (2–4 hours)

1. Extend `run_audit.py`:
   - `--skip-e2e`
   - `--skip-frontend`
   - `--migration-smoke` (optional local `alembic upgrade head` against compose Postgres)
2. Extend `finish_task.py`:
   - `--skip-audit` (requires `--confirm-audit-passed` or similar safety)
   - Print reminder to verify GitHub Actions after push

### Phase C — CI quick wins (1–2 hours)

1. Frontend workflow: add `npm run lint` step after build.
2. Backend workflow: fail fast on migration step before pytest (already ordered correctly).
3. Add workflow status badges to backend/frontend README (optional).

### Phase D — Fast pytest subset (half day)

1. Introduce `@pytest.mark.smoke` on ~20 critical tests.
2. Document: `py -m pytest -m smoke` for fast check.
3. Optional: run smoke mark in a dedicated quick CI job on PRs (parallel to full suite initially).

### Phase E — Post-cutover (Phase 5)

1. Automated post-deploy `curl /health` in runbook checklist (manual → scripted).
2. Re-evaluate E2E in CI with `docker compose` + Playwright container.
3. UptimeRobot + backup cron verification as deployment gate items.

---

## Appendix A — File reference

| File | Role |
|------|------|
| [`backend/tests/`](../backend/tests/) | 29 modules, 239 pytest tests |
| [`backend/tests/conftest.py`](../backend/tests/conftest.py) | SQLite, env pins, per-test DB reset |
| [`frontend/e2e/`](../frontend/e2e/) | 33 Playwright tests |
| [`frontend/playwright.config.ts`](../frontend/playwright.config.ts) | Serial E2E, 60 s timeout |
| [`workspace/run_audit.py`](run_audit.py) | pytest → build → E2E |
| [`workspace/finish_task.py`](finish_task.py) | Quality Gate + git + status + roadmap |
| [`workspace/project_status.py`](project_status.py) | `PROJECT_STATUS.md` marker updates |
| [`workspace/run_melomanos.py`](run_melomanos.py) | Dev stack launcher for E2E |
| [`backend/.github/workflows/ci.yml`](../backend/.github/workflows/ci.yml) | Postgres migrate + pytest |
| [`frontend/.github/workflows/ci.yml`](../frontend/.github/workflows/ci.yml) | npm build |
| [`backend/scripts/pre_deploy_checklist.py`](../backend/scripts/pre_deploy_checklist.py) | Deploy operator checklist |

## Appendix B — Metrics baseline (2026-06-17)

| Metric | Value |
|--------|-------|
| Backend tests | 239 |
| Backend test files | 29 |
| E2E tests | 33 |
| pytest duration (full) | ~142 s |
| npm build duration | ~5–10 s |
| CI E2E | Not run |
| pytest markers (smoke/slow) | None |

---

*Audit complete. No implementation performed. Next step: Phase A documentation sync or Phase B `run_audit.py` flags per team priority.*
