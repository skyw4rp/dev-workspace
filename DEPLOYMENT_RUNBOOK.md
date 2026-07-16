# Deployment Runbook — Melómanos Marketplace

> **DEFERRED / NOT AUTHORIZED / NON-EXECUTABLE.** Production Deployment is deferred. This runbook preserves technical history and conditional procedure; it does not authorize a deployment, cutover, infrastructure, cloud, domain, database, environment, secret, production, build, test, or runtime action. No deployment-related action may begin without a new explicit human decision recorded in [`PROJECT_STATUS.md`](PROJECT_STATUS.md). `NEXT_ACTION_QUEUE.md`, `backend/MVP_ROADMAP.md`, and any roadmap, queue, mission brief, plan, report, checklist, or runbook cannot authorize execution by themselves.
>
> All "current," "approved," "deploy," "execute," "pre-deploy," and "deploy day" wording below is historical or conditional reference material only, not present authorization.

**Purpose:** Historical/conditional operator reference for production deployment, migration, backup, and recovery.
**Architecture:** Historically proposed Option B — Vercel frontend + VPS (Docker: Caddy, FastAPI, PostgreSQL).
**Companion docs:** [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md), [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md)

**Status:** **DEFERRED / NOT AUTHORIZED / NON-EXECUTABLE** — Phase 4 historical CI and validation documentation; production cutover not performed.

---

## 1. Target architecture

> **DEFERRED / NOT AUTHORIZED / NON-EXECUTABLE.** Production Deployment is deferred. This runbook preserves technical history and conditional procedure; it does not authorize a deployment, cutover, infrastructure, cloud, domain, database, environment, secret, production, build, test, or runtime action. No deployment-related action may begin without a new explicit human decision recorded in [`PROJECT_STATUS.md`](PROJECT_STATUS.md). `NEXT_ACTION_QUEUE.md`, `backend/MVP_ROADMAP.md`, and any roadmap, queue, mission brief, plan, report, checklist, or runbook cannot authorize execution by themselves.
>
> All "current," "approved," "deploy," "execute," "pre-deploy," and "deploy day" wording below is historical or conditional reference material only, not present authorization.

```
Internet
   │
   ├─► melomanos.cl / www.melomanos.cl ──► Vercel (Next.js, TLS automatic)
   │
   └─► api.melomanos.cl ──► VPS :443 ──► Caddy (TLS) ──► api:8000 (FastAPI)
                                              │
                                              └─► db:5432 (PostgreSQL, private)
```

| Component | Technology | Operator access |
|-----------|------------|-----------------|
| Frontend | Vercel + Next.js | Vercel dashboard, Git push |
| API | Docker + uvicorn | SSH to VPS, `docker compose` |
| TLS (API) | Caddy 2 | Caddyfile in repo (Phase 2) |
| Database | PostgreSQL 15 volume | `docker exec` / `psql` via compose |

**No staging environment** for MVP. Validate on local Docker prod compose before each production release.

---

## 2. DNS plan

Domain: **melomanos.cl** (register via NIC Chile or accredited reseller).

| Host | Type | Target | Purpose |
|------|------|--------|---------|
| `@` (apex) | `A` or `ALIAS` | Vercel DNS per Vercel docs | Primary site |
| `www` | `CNAME` | `cname.vercel-dns.com` (or Vercel-provided) | www alias |
| `api` | `A` | VPS public IPv4 | Backend API + WebPay callback |

**Vercel domain setup:** Project → Settings → Domains → add `melomanos.cl` and `www.melomanos.cl`.

**TTL:** 300–3600 s during migration; increase after stable.

**Verification (before cutover):**

```bash
dig +short melomanos.cl
dig +short www.melomanos.cl
dig +short api.melomanos.cl
```

---

## 3. Required environment variables

Full matrix: [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md).

**Minimum before first API deploy:**

- VPS: `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `ADMIN_KEY`, `PAYMENT_PROVIDER_MODE`
- Vercel: `NEXT_PUBLIC_API_URL=https://api.melomanos.cl`
- Phase 3+: `CORS_ORIGINS=https://melomanos.cl,https://www.melomanos.cl`

---

## 4. Secrets handling

1. Generate secrets locally (`openssl rand -hex 32`).
2. Store master copy in **password manager** (1Password, Bitwarden, etc.).
3. Copy to VPS `/opt/melomanos/.env.production` — `chmod 600`, owned by deploy user.
4. Copy public frontend vars to **Vercel** dashboard (Production environment).
5. **Never** commit `.env.production`, `.env.local`, or `.env.docker` with real values.

Pre-deploy grep (from repo root, optional):

```bash
# Ensure no accidental secret files staged
git status --ignored | findstr /i "env.production env.local env.docker"
```

---

## 5. Migration process (Alembic)

**When:** Before first production traffic; again on every release that includes new Alembic revisions.

**Prerequisites:** Postgres running; `DATABASE_URL` set; API container image includes latest code.

### First-time (empty database)

```bash
# On VPS, from backend directory with prod compose
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api \
  alembic upgrade head
```

### Routine deploy (new revisions)

```bash
# 1. Backup first (see §6)
# 2. Pull new image / rebuild
docker compose -f docker-compose.yml -f docker-compose.prod.yml build api
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d api

# 3. Migrate
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api \
  alembic upgrade head

# 4. Verify revision
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api \
  alembic current
```

### Local rehearsal (before prod)

```powershell
cd backend
docker compose up -d db
# set DATABASE_URL in .env.docker to postgresql://postgres:postgres@localhost:5432/melomanos
alembic upgrade head
py -m pytest -q
```

### Rollback of migrations

Alembic **downgrade** scripts are not maintained for all revisions. **Default policy: forward-only.**

- If a bad migration shipped: restore DB from backup (§6) and redeploy previous API image tag.
- Do not run `alembic downgrade` in production unless a tested downgrade path exists.

---

## 6. Backup approach

### What to backup

- **PostgreSQL** full logical dump (`pg_dump`) — includes users, orders, escrow, disputes, notifications.

### Schedule (production)

| Frequency | Retention | Method |
|-----------|-----------|--------|
| Daily 03:00 America/Santiago | 7 daily | `pg_dump` → compressed file |
| Weekly Sunday | 4 weekly | same |
| Before each deploy | 1 manual | operator-triggered |

### Example backup command

```bash
BACKUP_DIR=/opt/melomanos/backups
STAMP=$(date +%Y%m%d_%H%M%S)
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T db \
  pg_dump -U melomanos -d melomanos --no-owner --format=custom \
  > "$BACKUP_DIR/melomanos_${STAMP}.dump"
gzip -f "$BACKUP_DIR/melomanos_${STAMP}.dump"
```

### Off-site copy

Copy latest dump to **Backblaze B2**, S3, or encrypted offline storage at least weekly.

**Not backed up in MVP:** Vercel build artifacts (reproducible from git); dispute/video **external URLs** (third-party hosting).

### Restore procedure

1. Stop API: `docker compose ... stop api`
2. Restore:

```bash
gunzip -c melomanos_YYYYMMDD_HHMMSS.dump.gz | \
  docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T db \
  pg_restore -U melomanos -d melomanos --clean --if-exists
```

3. Start API; run smoke tests (login, orders list).
4. Document incident in runbook appendix.

**RTO target (MVP):** < 4 hours manual restore.

---

## 7. Rollback approach

### Frontend (Vercel)

1. Vercel → Deployments → select last green deployment → **Promote to Production**.
2. Verify `NEXT_PUBLIC_API_URL` unchanged.

### Backend (VPS)

1. Identify previous git tag / image digest.
2. `git checkout <tag>` or pull previous image.
3. `docker compose ... up -d --build api`
4. **Do not downgrade DB** unless restoring from backup (§6).
5. Smoke: `curl -sS https://api.melomanos.cl/health` → 200

### When to rollback

- API 5xx sustained after deploy
- Migration failure
- Payment/webhook regression after WebPay config change

### When **not** to rollback

- JWT secret rotation (expected logout) — communicate to beta users
- Single-user error — investigate logs first (`docker compose logs api --tail=200`)

---

## 8. Manual deploy checklist

Use for **every** production release. Copy to appendix and date when complete.

### Pre-deploy

- [ ] **Backend GitHub Actions** green on merge commit (pytest + Alembic migration smoke on PostgreSQL)
- [ ] **Frontend GitHub Actions** green (`npm run build`)
- [ ] Local Quality Gate: `py -m pytest`, `npm run build` (E2E optional pre-cutover)
- [ ] Optional: `py scripts/pre_deploy_checklist.py --compose-config` from `backend/`
- [ ] Migration revisions reviewed (`alembic history`)
- [ ] [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md) updated if new env vars
- [ ] Production backup taken (§6)
- [ ] Maintenance note prepared (if JWT secret or breaking change)

### Frontend (Vercel)

- [ ] Merge to production branch
- [ ] Vercel build succeeded
- [ ] `NEXT_PUBLIC_API_URL` = `https://api.melomanos.cl`
- [ ] Spot-check `https://melomanos.cl` homepage

### Backend (VPS)

- [ ] SSH to VPS as deploy user
- [ ] `git pull` (or deploy artifact) — target tagged release
- [ ] `.env.production` unchanged or intentionally updated
- [ ] `docker compose -f docker-compose.yml -f docker-compose.prod.yml build`
- [ ] `alembic upgrade head` (§5)
- [ ] `docker compose ... up -d`
- [ ] `docker compose ps` — all healthy
- [ ] `GET /health` returns 200 (see §13)

### Post-deploy smoke

- [ ] `GET https://api.melomanos.cl/health` → 200 (`{"status":"ok","service":"melomanos-api"}`)
- [ ] Register or login test account
- [ ] Browse listings
- [ ] Create test order (simulate payment if enabled)
- [ ] Admin panel with production `ADMIN_KEY` (operator only)
- [ ] UptimeRobot green

### Sign-off

| Field | Value |
|-------|-------|
| Date | |
| Operator | Ernesto |
| Git SHA (backend) | |
| Git SHA (frontend) | |
| Alembic revision | |
| Notes | |

---

## 9. Provider assumptions

| Service | Assumption | Action at Phase 5 |
|---------|------------|---------------------|
| **Vercel** | Hobby or Pro; GitHub repo connected | Create project, link domain |
| **VPS** | Hetzner CPX22 **or** DO $12/mo; Ubuntu 22.04+ | Create VM, harden SSH, install Docker |
| **Domain** | `melomanos.cl` registered | Configure DNS per §2 |
| **Caddy** | Official image; persistent `/data` for certs | Add in Phase 2 compose |
| **Uptime** | UptimeRobot free — 2 monitors | API + homepage |
| **Backups** | cron on VPS + optional B2 | Implement at Phase 5 |

**Firewall (VPS):** allow `22` (restricted IP if possible), `80`, `443`; deny all else.

---

## 10. Phase 2 deliverables (complete)

Production Docker foundation is in [`backend/README_DEPLOYMENT.md`](../backend/README_DEPLOYMENT.md).

| Artifact | Path |
|----------|------|
| Prod compose override | [`backend/docker-compose.prod.yml`](../backend/docker-compose.prod.yml) |
| Caddy config | [`backend/deployment/Caddyfile`](../backend/deployment/Caddyfile) |
| Env template | [`backend/.env.production.example`](../backend/.env.production.example) |

**Validate locally:**

```bash
cd backend
cp .env.production.example .env.production   # first time only
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
```

## 11. Phase 3 deliverables (complete)

Runtime configuration for production URLs and CORS:

| Area | Implementation |
|------|----------------|
| Backend CORS | `CORS_ORIGINS` env → [`backend/app/core/config.py`](../backend/app/core/config.py) → [`backend/app/main.py`](../backend/app/main.py) |
| Frontend API | `NEXT_PUBLIC_API_URL` → [`frontend/src/lib/api.ts`](../frontend/src/lib/api.ts) |
| Env templates | [`backend/.env.example`](../backend/.env.example), [`backend/.env.production.example`](../backend/.env.production.example), [`frontend/.env.example`](../frontend/.env.example) |

**Vercel (Production scope):** set `NEXT_PUBLIC_API_URL=https://api.melomanos.cl`.

**VPS `.env.production`:** set `CORS_ORIGINS=https://melomanos.cl,https://www.melomanos.cl` (must match Vercel domains).

**Validate:**

```bash
cd backend && py -m pytest tests/test_cors_config.py -q
cd frontend && npm run build
```

## 12. Phase 4 deliverables (complete)

### Continuous integration

| Repo | Workflow | Triggers | Steps |
|------|----------|----------|-------|
| Backend | [`.github/workflows/ci.yml`](../backend/.github/workflows/ci.yml) | push/PR → `main`, `master` | Postgres 15 → `alembic upgrade head` → `py -m pytest` |
| Frontend | [`.github/workflows/ci.yml`](../frontend/.github/workflows/ci.yml) | push/PR → `main`, `master` | `npm ci` → `npm run build` |

**E2E is not in CI** — run locally via Quality Gate before major releases.

### Local prod-compose rehearsal (before Phase 5 cutover)

Rehearse operator steps without DNS/TLS if needed:

```bash
cd backend
cp .env.production.example .env.production   # placeholders only
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api alembic upgrade head
curl -sS http://127.0.0.1:8000/health   # dev compose only; prod API is internal
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f api
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```

For full Caddy/TLS rehearsal, point `api.melomanos.cl` at the host via DNS or `/etc/hosts`.

**Checklist helper:**

```bash
cd backend
py scripts/pre_deploy_checklist.py
py scripts/pre_deploy_checklist.py --compose-config   # if Docker + .env.production exist
```

## 13. Operator quick reference (deploy day)

| Action | Command |
|--------|---------|
| **Migrate** | `docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api alembic upgrade head` |
| **Health** | `curl -sS https://api.melomanos.cl/health` |
| **Logs** | `docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f api` |
| **Restart API** | `docker compose -f docker-compose.yml -f docker-compose.prod.yml restart api` |
| **Rollback API** | Redeploy previous git tag + `docker compose ... up -d --build api` (§7); restore DB from backup if migration failed |

## 14. Phase 5 tasks (next — production cutover)

From [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md):

1. Register/configure DNS
2. Provision VPS + Vercel
3. Set production secrets per env matrix
4. First deploy: migrate, smoke, uptime monitor
5. Backup cron verified
6. Quality Gate + `finish_task.py` after live validation

---

## Appendix A — VPS directory layout (planned)

```
/opt/melomanos/
  .env.production      # secrets, chmod 600
  backups/             # pg_dump files
  repo/                # git clone of melomanos backend
  compose/             # docker-compose.yml + prod override + Caddyfile
```

---

## Appendix B — Useful commands

```bash
# Logs
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f api

# Health (production, after TLS)
curl -sS https://api.melomanos.cl/health

# Rollback API image (keep DB — see §7)
git checkout <previous-tag>
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build api

# DB shell
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec db \
  psql -U melomanos -d melomanos

# Disk usage
docker system df
df -h /opt/melomanos/backups
```

---

## Appendix C — Phase 4 dry-run sign-off

Local validation performed before first GitHub Actions run on remote:

| Field | Value |
|-------|-------|
| Date | 2026-06-17 |
| Operator | Ernesto |
| Backend pytest | `py -m pytest` — pass locally |
| Frontend build | `npm run build` — pass locally |
| Compose config | `docker compose … config` — pass when `.env.production` present |
| CI workflows | Created in backend + frontend repos; **remote green pending push** |
| Prod-compose rehearsal | Documented in §12; full TLS rehearsal deferred to Phase 5 |
| Notes | E2E remains local-only; not required in CI for MVP |

---

## References

| Document | Path |
|----------|------|
| Deployment plan | [`workspace/PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md) |
| Phase 5 checklist | [`workspace/PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md`](PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md) |
| Decision report | [`workspace/PRODUCTION_DEPLOYMENT_DECISION_REPORT.md`](PRODUCTION_DEPLOYMENT_DECISION_REPORT.md) |
| Env matrix | [`workspace/PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md) |
| Scope audit | [`workspace/PRODUCTION_DEPLOYMENT_SCOPE_REPORT.md`](PRODUCTION_DEPLOYMENT_SCOPE_REPORT.md) |
| Deployment guide | [`backend/README_DEPLOYMENT.md`](../backend/README_DEPLOYMENT.md) |
| Quality Gate | [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md) |

---

*Last updated: Production Deployment Phase 4 — GitHub Actions CI + deployment validation docs.*
