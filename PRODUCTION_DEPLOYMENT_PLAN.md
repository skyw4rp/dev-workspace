# Production Deployment Plan — Melómanos Marketplace

**Document type:** Phased execution plan (Cursor / operator playbook)  
**Historical technical reference:** [`PRODUCTION_DEPLOYMENT_SCOPE_REPORT.md`](PRODUCTION_DEPLOYMENT_SCOPE_REPORT.md)
**Current operational disposition:** **DEFERRED / NOT AUTHORIZED**

> ## CURRENT-STATUS NOTICE — NOT EXECUTABLE
>
> Production Deployment is **DEFERRED / NOT AUTHORIZED** pending UX and product-readiness evidence. No deployment, infrastructure, cloud, domain, database, environment, secret, or production work is authorized. This plan’s phases, operator instructions, architecture, and checklists are preserved as historical technical planning only and must not be interpreted as current commands. A future executor requires a new explicit human decision before using this document as execution instructions. [`PROJECT_STATUS.md`](PROJECT_STATUS.md) is the sole cross-repository operational authority.

**Historical roadmap reference:** Production Deployment — [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md)
**Historical policy:** Do **not** mark the deployment milestone complete or advance `MVP_ROADMAP.md` until **all phases below are DONE**. See [`QUALITY_GATE.md`](QUALITY_GATE.md).

---

## Approved architecture (Option B)

| Layer | Choice | Production URL |
|-------|--------|----------------|
| **Frontend** | Vercel (Next.js) | `https://melomanos.cl`, `https://www.melomanos.cl` |
| **Backend API** | FastAPI in Docker on single VPS | `https://api.melomanos.cl` |
| **Database** | PostgreSQL 15 on same VPS (Docker volume) | Internal only (`db:5432`) |
| **TLS / reverse proxy** | Caddy 2 (Docker) | Automatic Let's Encrypt |
| **Staging** | **Skipped for MVP** | Local Docker + Closed Beta on prod |
| **File storage** | **None** | Dispute/video = external URLs only |

**Operator:** single maintainer (Ernesto).  
**Target region:** VPS in **São Paulo** or **US East** (latency/cost tradeoff — validate from Chile after Phase 5).

---

## Historical Cursor instruction — non-operative

```
Historical instruction only: To continue Production Deployment, implement the next TODO phase only.
Read PRODUCTION_DEPLOYMENT_PLAN.md, PRODUCTION_ENV_MATRIX.md, and DEPLOYMENT_RUNBOOK.md.
Set the target phase Status to IN_PROGRESS before coding or infra work.
When the phase completion checklist is fully satisfied, set Status to DONE.
Do not start the following phase in the same session unless explicitly asked.
Do not advance MVP_ROADMAP.md until Phase 5 is DONE.
```

---

## Historical execution rules — non-operative

1. **Only one phase may be `IN_PROGRESS` at a time.**
2. **Do not cut over to production** until Phase 5 checklist is complete.
3. **No secrets in git** — use [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md) + host/Vercel secret stores.
4. **PostgreSQL only in production** — no SQLite.
5. **Run Quality Gate** before milestone close (`py -m pytest`, `npm run build`, `npm run test:e2e`).
6. **Follow [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md)** for every production deploy.

---

## Related documents

| Document | Purpose |
|----------|---------|
| [`PRODUCTION_DEPLOYMENT_SCOPE_REPORT.md`](PRODUCTION_DEPLOYMENT_SCOPE_REPORT.md) | Pre-implementation audit |
| [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md) | Environment variables by layer |
| [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md) | Migrate, deploy, backup, rollback, checklist |
| [`backend/README_DEPLOYMENT.md`](../backend/README_DEPLOYMENT.md) | Docker prod compose, commands, VPS paths |
| [`backend/.env.production.example`](../backend/.env.production.example) | Production env template |
| [`backend/README.md`](../backend/README.md) | Local/Docker dev setup |
| [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) | Milestone definition |

---

## Phase overview

| Phase | Title | Status |
|-------|-------|--------|
| **1** | Deployment architecture & decision docs | **DONE** |
| **2** | Dockerization & production compose (+ Caddy) | **DONE** |
| **3** | Production configuration (CORS, API URL) | **TODO** |
| **4** | CI migration smoke + deploy checklist validation | **TODO** |
| **5** | Production cutover & release readiness | **TODO** |

---

## Phase 1 — Deployment architecture & decision docs

**Status:** DONE

### Goal

Lock Option B architecture and publish operator-facing deployment documentation.

### Deliverables (completed)

| File | Content |
|------|---------|
| [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md) | This plan — phases, approved architecture |
| [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md) | Env vars, secrets, local vs prod |
| [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md) | DNS, migrate, backup, rollback, checklist |

### Out of scope (Phase 1)

- Docker/Caddy file changes
- VPS or Vercel provisioning
- DNS cutover
- Code changes (`CORS`, `API_BASE`, `/health`)
- Roadmap advance

### Validation

- [x] Architecture documented and approved (Option B)
- [x] DNS plan documented (`melomanos.cl`, `api.melomanos.cl`)
- [x] Env matrix and secrets policy documented
- [x] Migration, backup, rollback, manual checklist documented
- [x] Phase 2 tasks listed
- [x] No code or infrastructure changes

---

## Phase 2 — Dockerization & production compose

**Status:** DONE

### Goal

Extend existing [`backend/docker-compose.yml`](../backend/docker-compose.yml) for production: Caddy TLS, no public Postgres/API ports, healthchecks.

### Deliverables (completed)

| File | Content |
|------|---------|
| [`backend/docker-compose.prod.yml`](../backend/docker-compose.prod.yml) | Caddy + healthchecks; internal api/db |
| [`backend/deployment/Caddyfile`](../backend/deployment/Caddyfile) | `api.melomanos.cl` → `api:8000` |
| [`backend/.env.production.example`](../backend/.env.production.example) | Production env placeholders |
| [`backend/README_DEPLOYMENT.md`](../backend/README_DEPLOYMENT.md) | Compose commands, VPS layout, migrations |
| [`backend/app/main.py`](../backend/app/main.py) | `GET /health` liveness endpoint |
| [`backend/tests/test_health.py`](../backend/tests/test_health.py) | Health endpoint test |

### Out of scope (Phase 2)

- VPS or Vercel provisioning
- DNS cutover
- Env-driven CORS in app code (Phase 3)
- CI (Phase 4)

### Validation

- [x] `docker compose -f docker-compose.yml -f docker-compose.prod.yml config` succeeds (after `cp .env.production.example .env.production`)
- [x] Caddyfile committed (no certs in repo)
- [x] `py -m pytest` passes (includes `test_health.py`)

---

## Phase 3 — Production configuration (code)

**Status:** DONE

### Goal

Make frontend and backend configurable for production URLs and CORS.

### Deliverables (completed)

| Area | Change |
|------|--------|
| Backend | `CORS_ORIGINS` in [`app/core/config.py`](../backend/app/core/config.py); used in [`app/main.py`](../backend/app/main.py) |
| Backend tests | [`tests/test_cors_config.py`](../backend/tests/test_cors_config.py) |
| Frontend | `NEXT_PUBLIC_API_URL` in [`frontend/src/lib/api.ts`](../frontend/src/lib/api.ts) |
| Env examples | [`backend/.env.example`](../backend/.env.example), [`backend/.env.production.example`](../backend/.env.production.example), [`frontend/.env.example`](../frontend/.env.example) |
| Docs | Env matrix, runbook, [`frontend/README.md`](../frontend/README.md) Vercel notes |

**Note:** `GET /health` shipped in Phase 2; optional DB ping deferred.

### Out of scope

- Vercel project creation (Phase 5)

### Validation

- [x] Local smoke with prod-like env vars documented
- [x] `npm run build` passes
- [x] `py -m pytest` passes

---

## Phase 4 — CI & deployment validation

**Status:** DONE

### Goal

Automate migration smoke and formalize manual deploy checklist.

### Deliverables (completed)

| Area | Change |
|------|--------|
| Backend CI | [`.github/workflows/ci.yml`](../backend/.github/workflows/ci.yml) — Postgres 15 service, `alembic upgrade head`, pytest |
| Frontend CI | [`.github/workflows/ci.yml`](../frontend/.github/workflows/ci.yml) — `npm ci`, `npm run build` |
| Checklist helper | [`backend/scripts/pre_deploy_checklist.py`](../backend/scripts/pre_deploy_checklist.py) |
| Runbook | Pre-deploy checklist, prod-compose rehearsal, health/rollback/logs (§8, §13, Appendix C) |
| Testing docs | [`backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md) — CI section |

### Out of scope

- E2E in CI (deferred — local Quality Gate only)
- Remote GitHub Actions execution (requires push to GitHub)

### Validation

- [x] `py -m pytest` passes locally
- [x] `npm run build` passes locally
- [x] Workflow YAML structure reviewed locally
- [ ] GitHub Actions green on default branch (after push to remote)

---

## Phase 5 — Production cutover & release readiness

**Status:** TODO — **operator checklist ready** (cutover not performed)

### Goal

Live HTTPS deployment; milestone Quality Gate; docs update.

### Operator checklist (preparation complete)

**Use:** [`PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md`](PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md)  
**Locked stack:** [`PRODUCTION_DEPLOYMENT_DECISION_REPORT.md`](PRODUCTION_DEPLOYMENT_DECISION_REPORT.md) — DigitalOcean GRU, Cloudflare, Vercel, UptimeRobot, pg_dump + B2.

### Scope

- Register/configure DNS
- Provision VPS + Vercel
- Set production secrets per env matrix
- First deploy: migrate, smoke, uptime monitor
- Backup cron verified
- Update `PROJECT_STATUS.md`, `ARCHITECTURE.md`, `TESTING_STRATEGY.md`, `RELEASE_NOTES.md`
- `finish_task.py` (only after all phases DONE)

### Validation

- `https://melomanos.cl` loads
- `https://api.melomanos.cl/` or `/health` returns OK
- Register → login → listing browse smoke on production
- Quality Gate full pass

---

## Provider assumptions (Phase 1 lock)

| Role | Assumed provider | Notes |
|------|------------------|-------|
| Frontend | **Vercel** (Hobby/Pro) | GitHub integration; env vars in dashboard |
| VPS | **DigitalOcean Basic 4 GB** — **`gru1` (São Paulo)** | See [`PRODUCTION_DEPLOYMENT_DECISION_REPORT.md`](PRODUCTION_DEPLOYMENT_DECISION_REPORT.md) |
| Domain | **melomanos.cl** via NIC Chile or reseller | Apex + `www` → Vercel; `api` → VPS A record |
| TLS (API) | **Caddy** + Let's Encrypt | Auto-renew |
| TLS (frontend) | **Vercel** | Auto |
| Uptime | **UptimeRobot** (free) | Ping API health + homepage |
| Backups | **cron + pg_dump** → off-VPS | Backblaze B2 or encrypted local — pick at Phase 5 |

**Estimated cost:** USD **10–18/month** at launch (see scope report §8).

---

*Last updated: Phase 5 preparation — operator checklist created; no VPS cutover.*
