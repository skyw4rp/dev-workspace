# Production Deployment Scope Report — Melómanos Marketplace

**Document type:** Pre-implementation scope audit  
**Date:** 2026-06-18  
**Current operational disposition:** **DEFERRED / NOT AUTHORIZED**

> ## CURRENT-STATUS NOTICE — NOT EXECUTABLE
>
> Production Deployment is **DEFERRED / NOT AUTHORIZED** pending UX and product-readiness evidence. No deployment, infrastructure, cloud, domain, database, environment, secret, or production work is authorized. The scope, architecture, recommendations, phases, and checklists below are preserved as historical technical planning and must not be interpreted as current commands. A future executor requires a new explicit human decision before using this report as execution instructions. [`PROJECT_STATUS.md`](PROJECT_STATUS.md) is the sole cross-repository operational authority.

**Historical milestone reference:** Production Deployment (`backend/MVP_ROADMAP.md` — former Current Priority Queue #1)
**Historical status:** Planning only — **no deployment code or infrastructure changes in this document**

**Authority stack:** `BUSINESS_RULES.md` → `ARCHITECTURE.md` → `MVP_ROADMAP.md` → this report

---

## Executive summary

Production Deployment means taking the **existing FastAPI + Next.js + PostgreSQL** stack from local/dev Docker to a **stable, HTTPS-hosted environment** with documented secrets, migrations, and a manual deploy checklist. The codebase already has **backend Dockerfile**, **docker-compose (api + postgres)**, **Alembic**, and **env templates** — but **production gaps** remain: hardcoded CORS and frontend `API_BASE`, no `/health` endpoint, no CI migration smoke, no frontend in Compose, no production env docs for WebPay/Admin.

**Recommended MVP architecture:** **Split hosting (Option B-lite)** — **Vercel** for Next.js frontend + **single small VPS** (Hetzner/DigitalOcean) running **Docker Compose** (FastAPI + PostgreSQL + Caddy/nginx for API TLS and reverse proxy). Estimated **~USD 12–18/month** at launch; scales to ~$25–40/month at 1k users without re-architecture.

**Staging:** **Not required** for MVP — use local Docker + production beta flag (Closed Beta milestone) instead.

**Historical first implementation phase:** **Phase 1 — Deployment architecture & decisions** (domain, provider, env matrix, runbooks — no production cutover yet). This is not a current instruction.

---

## 1. Current roadmap definition

### Source: `backend/MVP_ROADMAP.md` (queue #1)

| Area | Roadmap text |
|------|----------------|
| **Business goal** | Run Melómanos on a **stable production environment** with **migrations, secrets, and monitoring**. |
| **Technical goal** | **Docker/production config**, **PostgreSQL**, **Alembic CI**, **health checks**, **env documentation**. |
| **Backend** | Production `DATABASE_URL`, **CORS origins**; **migration runbook**; **health endpoint hardening**. |
| **Frontend** | **Production build** + **API URL config**. |
| **Tests** | **CI:** pytest + migration smoke on clean DB; **Manual:** deploy checklist. |
| **Dependencies** | All core backend features migrated |
| **Complexity** | Medium |
| **Status** | TODO |

### Explicitly required (milestone DoD)

1. Production-ready **PostgreSQL** (`DATABASE_URL` in prod).
2. Production **CORS** allowing the live frontend origin(s).
3. **Migration runbook** (Alembic upgrade procedure documented and repeatable).
4. **Health endpoint** suitable for uptime checks (roadmap: “hardening” — implies more than root `/`).
5. **Frontend production build** with configurable **API base URL** (not `127.0.0.1:8000`).
6. **Env documentation** for all production secrets and toggles.
7. **CI:** pytest + **migration smoke on clean DB**.
8. **Manual deploy checklist** executed and recorded.
9. Quality Gate + commit + push + `PROJECT_STATUS.md` (per roadmap Rules).

### Implied (not spelled out)

- **HTTPS everywhere** (browser JWT, WebPay callbacks, admin panel).
- **Secrets not in git** (`.env.local`, `.env.docker` pattern already established).
- **PostgreSQL in production** (architecture authority; SQLite is dev/test only).
- **WebPay production config** when leaving placeholder (`PAYMENT_PROVIDER_MODE`, `WEBPAY_CALLBACK_SECRET`, `WEBPAY_RETURN_URL_BASE`) — implied by Closed Beta / Public Launch dependency on payment.
- **ADMIN_KEY** set in production for dispute resolution routes.
- **Backup/restore** minimum for escrow marketplace data (implied by “stable” + Public Launch “backup policy”).
- **Process manager / restart policy** (Docker `restart: unless-stopped` or systemd).
- **Logging** accessible to single operator (stdout + optional log tail).
- **CORS + credentials** for JWT Bearer from frontend domain.
- **Alembic revision `e8f9a0b1c2d3`** (notifications) and all prior migrations applied before beta.

### Out of scope (MVP milestone / defer)

| Item | Rationale |
|------|-----------|
| **Multi-region / HA** | Roadmap: low complexity launch; single operator. |
| **Kubernetes** | Overkill for MVP queue item. |
| **Full observability stack** (Datadog, Grafana) | Roadmap says “monitoring” — MVP = health check + logs; not full APM. |
| **Automated blue/green deploys** | Manual checklist sufficient for milestone. |
| **Dedicated staging environment** | Not in roadmap; Closed Beta can use prod + invite flag. |
| **S3/object storage service** | Dispute evidence and listing videos use **external URLs** today; no upload API. |
| **Real Transbank production SDK** | Payment Provider milestone shipped **placeholder**; production WebPay creds are a **business decision**, not this milestone’s core deliverable. |
| **Email/SMTP infrastructure** | Notifications MVP is in-app only. |
| **WAF / DDoS enterprise tier** | Defer; use provider defaults + rate limits in Closed Beta if needed. |
| **Public status page** | Public Launch milestone, not Production Deployment. |

### Current codebase baseline (relevant)

| Asset | State |
|-------|--------|
| `backend/Dockerfile` | Python 3.10-slim, uvicorn on 8000 |
| `backend/docker-compose.yml` | `api` + `postgres:15` volume |
| `backend/.env.example` | Documents local, docker, payment vars |
| `backend/app/main.py` | CORS **hardcoded** to `localhost:3000` |
| `frontend/src/lib/api.ts` | `API_BASE` **hardcoded** to `127.0.0.1:8000` |
| Health | Only `GET /` — no dedicated `/health` |
| CI | **None** (`.github/` absent); TESTING_STRATEGY lists CI as planned |
| Frontend Docker | **Not present** |

---

## 2. Recommended MVP deployment architecture

Target profile: **small Chilean vinyl marketplace**, **low traffic launch**, **low monthly cost**, **single operator (Ernesto)**, **fast recovery**, **easy maintenance**.

### Recommended topology (split, minimal ops)

```
                    ┌─────────────────────────┐
   Users (HTTPS)    │  Vercel (or similar)    │
        ──────────► │  Next.js production     │
                    │  NEXT_PUBLIC_API_URL    │
                    └───────────┬─────────────┘
                                │ HTTPS API calls
                                ▼
                    ┌─────────────────────────┐
                    │  VPS (single node)      │
                    │  ┌───────────────────┐│
                    │  │ Caddy or nginx      ││  TLS termination
                    │  │ api.melomanos.cl    ││
                    │  └─────────┬───────────┘│
                    │            ▼            │
                    │  ┌───────────────────┐│
                    │  │ FastAPI (Docker)  ││
                    │  └─────────┬───────────┘│
                    │            ▼            │
                    │  ┌───────────────────┐│
                    │  │ PostgreSQL 15     ││  (same VPS, Docker volume)
                    │  │ (not public)      ││
                    │  └───────────────────┘│
                    └─────────────────────────┘

   Domain: melomanos.cl (or .com) → Vercel; api.melomanos.cl → VPS
   SSL: Vercel automatic + Let's Encrypt on VPS (Caddy)
```

### Component choices

| Component | Recommendation | Notes |
|-----------|----------------|-------|
| **Backend hosting** | Single VPS, Docker Compose | Matches existing Dockerfile/compose; one SSH session for Ernesto |
| **Frontend hosting** | **Vercel** (Next.js native) | Free/hobby tier, auto SSL, git push deploy, no nginx tuning |
| **PostgreSQL** | **On same VPS** (Compose volume) for MVP | Cheapest; upgrade to managed PG when revenue/traffic justify |
| **File storage** | **None (MVP)** | Evidence/video = user-supplied URLs; revisit if upload feature added |
| **Domain** | `.cl` primary (e.g. `melomanos.cl`) | Chile-focused product; register via NIC Chile or reseller |
| **SSL** | Vercel (frontend) + Caddy/Let's Encrypt (API) | Required for JWT, WebPay callbacks, trust |

### Alternative (all-in-one VPS)

Run **Next.js standalone** + API + Postgres on one VPS behind nginx. **Lower moving parts count**, but Ernesto maintains Node + Python + TLS + static caching. Vercel split is **recommended** for faster iteration unless cost must be absolute minimum (one VPS only).

---

## 3. Infrastructure options

### Option A — Single VPS (everything on one box)

| | |
|--|--|
| **Layout** | nginx/Caddy → Next.js (`next start`) + FastAPI + PostgreSQL on one VM |
| **Complexity** | Medium — one server, multiple services, manual TLS |
| **Monthly cost** | **~USD 8–18** (Hetzner CPX22, DO Basic, Chile VPS) |
| **Scalability** | Vertical only; fine to ~1k MAU for this stack |
| **Recommended?** | **Acceptable** if Ernesto prefers one bill and one SSH target; slightly more ops than split |

### Option B — Frontend + Backend separated

| | |
|--|--|
| **Layout** | Vercel (frontend) + VPS or Railway/Fly (API + Postgres) |
| **Complexity** | **Low–medium** — best match for current stack (frontend not dockerized) |
| **Monthly cost** | **~USD 0–12** (Vercel hobby) + **~USD 8–15** (VPS) ≈ **$8–18** launch |
| **Scalability** | Frontend scales on CDN; API scales vertically then split DB |
| **Recommended?** | **Yes — primary recommendation** |

### Option C — Managed services (PaaS)

| | |
|--|--|
| **Layout** | e.g. Vercel + Railway/Render/Fly.io API + Neon/Supabase Postgres |
| **Complexity** | **Lowest ops** — click deploy, managed DB backups |
| **Monthly cost** | **~USD 15–35** launch (free tiers expire or limit connections) |
| **Scalability** | Good; vendor lock-in and Chile latency vary by region |
| **Recommended?** | **Good alternative** if Ernesto wants minimal SSH; watch **Postgres connection limits** and **WebPay callback URL** stability |

### Comparison summary

| Option | Complexity | Launch cost/mo | 1k users/mo | MVP fit |
|--------|------------|--------------|-------------|---------|
| A Single VPS | Medium | $8–18 | $18–35 | OK |
| **B Split (Vercel + VPS)** | **Low–med** | **$8–18** | **$20–40** | **Best** |
| C Managed PaaS | Low | $15–35 | $35–70 | Good if ops time > cost |

---

## 4. Environment strategy

### Environments

| Environment | Purpose | Data | When to use |
|-------------|---------|------|-------------|
| **Local** | Development | SQLite or local Postgres; `.env.local` | Daily dev (`run_melomanos.py`, pytest) |
| **Production** | Live beta/public | Postgres on VPS; secrets via host env / `.env.production` (not committed) | Closed Beta onward |

### Staging — necessary for MVP?

**No dedicated staging environment required** for Production Deployment milestone.

| Approach | Rationale |
|----------|-----------|
| **Local Docker Compose** | Rehearse migrations and env before prod (`docker compose up`, `alembic upgrade head`) |
| **Production + Closed Beta invite flag** | Next milestone adds allowlist; limits blast radius |
| **Optional “preview”** | Vercel preview deployments for frontend-only UI checks (API still points to prod or local — document clearly) |

Add staging **post-launch** if payment go-live or schema changes become frequent.

### Production environment variable matrix (minimum)

| Variable | Layer | Required | Notes |
|----------|-------|----------|-------|
| `DATABASE_URL` | Backend | Yes | `postgresql+psycopg2://...` — internal Docker network host `db` or localhost |
| `SECRET_KEY` | Backend | Yes | Strong random; rotate invalidates JWTs |
| `ALGORITHM` | Backend | Yes | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Backend | Yes | Default 30 |
| `ADMIN_KEY` | Backend | Yes (prod) | `x-admin-key` for admin/dispute resolution |
| `PAYMENT_PROVIDER_MODE` | Backend | Yes | `simulate` until real WebPay; then `webpay_placeholder` or future prod mode |
| `WEBPAY_CALLBACK_SECRET` | Backend | If WebPay | Must match Transbank/webhook config |
| `WEBPAY_RETURN_URL_BASE` | Backend | If WebPay | `https://melomanos.cl/orders` (prod domain) |
| `CORS_ORIGINS` | Backend | **New (impl)** | Comma-separated prod frontend URL(s) |
| `OPENAI_API_KEY` | Backend | Optional | NL search; can disable |
| `NEXT_PUBLIC_API_URL` | Frontend | **New (impl)** | `https://api.melomanos.cl` |
| `NEXT_PUBLIC_PAYMENT_PROVIDER_MODE` | Frontend | Optional | Match backend payment mode |

---

## 5. Security requirements (production minimum)

| Area | Requirement |
|------|-------------|
| **Secrets** | Never commit `.env.local`, `.env.docker`, production env files; use `.env.example` as template only |
| **JWT** | `SECRET_KEY` ≥ 32 bytes random; HTTPS only in production; short-ish token TTL (30 min default OK) |
| **HTTPS** | TLS on frontend and API; HSTS on API reverse proxy; no mixed-content API calls |
| **Database** | Postgres **not exposed** to public internet; strong password; firewall allow only Docker/internal |
| **Admin key** | Unique production `ADMIN_KEY`; not shared with test default `test-admin-key`; store in password manager |
| **WebPay webhook** | `WEBPAY_CALLBACK_SECRET` verified on callback; public URL must be stable HTTPS |
| **CORS** | Restrict to production frontend origin(s); remove blanket localhost in prod build |
| **Backups** | Daily automated Postgres dump (cron → encrypted storage or off-VPS copy); test restore quarterly |
| **SSH** | Key-only auth on VPS; non-root deploy user; automatic security updates |
| **Dispute evidence URLs** | User-supplied external links — document trust/abuse risk; no SSRF from server (current design: store URL only) |

---

## 6. Operations checklist (required before Closed Beta)

### Domain & TLS

- [ ] Register domain (e.g. `melomanos.cl`)
- [ ] DNS: `www` + apex → Vercel; `api` → VPS IP
- [ ] SSL active on frontend (Vercel) and API (Caddy/Let's Encrypt)
- [ ] Verify WebPay return URLs use production domain

### Environment & config

- [ ] Production `.env` / host secrets documented in runbook (not in git)
- [ ] `SECRET_KEY`, `ADMIN_KEY`, DB password generated and stored securely
- [ ] `NEXT_PUBLIC_API_URL` points to production API
- [ ] CORS includes production frontend origin
- [ ] Payment mode decision documented (`simulate` vs WebPay placeholder vs real)

### Database & migrations

- [ ] Postgres volume provisioned with persistent disk
- [ ] `alembic upgrade head` run once on empty prod DB (smoke test first)
- [ ] Migration rollback note: forward-only unless downgrade scripts exist
- [ ] Confirm all 29+ revisions applied (including `notifications`)

### Backup & recovery

- [ ] Daily `pg_dump` cron + retention (7 daily, 4 weekly minimum)
- [ ] Off-site copy (S3-compatible, Backblaze, or local encrypted download)
- [ ] **Recovery runbook:** restore dump to new volume, update `DATABASE_URL`, restart API
- [ ] RTO target for MVP: **< 4 hours** (single operator manual restore)

### Deploy & validation

- [ ] Manual deploy checklist completed (build, migrate, restart, smoke)
- [ ] Health check monitored (UptimeRobot free tier → `GET /health` or `/`)
- [ ] Critical path smoke: register, login, list listing, message, order create (simulate payment)
- [ ] Admin panel loads with production admin key
- [ ] Quality Gate green before each production deploy

### Monitoring (MVP level)

- [ ] Uptime ping on API health + frontend homepage
- [ ] Docker `restart: unless-stopped` on api + db
- [ ] Log retention: journald or docker logs; optional Loki later

---

## 7. Deployment phases

Break into five implementation phases (one **IN_PROGRESS** at a time). Aligns with roadmap deliverables without starting Closed Beta.

### Phase 1 — Deployment architecture & decisions

- Choose **Option B** (or documented alternative)
- Select providers (Vercel + Hetzner/DO), domain name, DNS plan
- Write **production env matrix** and **runbook outline**
- Document **staging decision** (local + prod beta only)
- **Deliverable:** `DEPLOYMENT.md` or expand `backend/README.md` production section — **no prod cutover**

### Phase 2 — Dockerization & production compose

- Extend Compose: optional **Caddy/nginx** service, healthcheck on `api`
- Production compose override (`docker-compose.prod.yml`): no public Postgres port
- Frontend: Vercel project linked OR add Next standalone to compose (if all-in-one)
- Add **`/health`** endpoint (DB ping optional)
- **Deliverable:** `docker compose -f docker-compose.yml -f docker-compose.prod.yml config` valid

### Phase 3 — Production configuration (code changes)

- Backend: `CORS_ORIGINS` from settings (env-driven)
- Frontend: `NEXT_PUBLIC_API_URL` replaces hardcoded `API_BASE`
- `.env.example` + `.env.production.example` updated
- WebPay return base URL production docs
- **Deliverable:** local prod-like smoke (`API_URL=https://... npm run build`)

### Phase 4 — CI & deployment validation

- GitHub Actions (or equivalent): **pytest** + **alembic upgrade on empty Postgres service**
- Optional: frontend `npm run build` in CI
- Manual **deploy checklist** markdown with checkboxes
- Rehearsal: deploy to VPS staging path or prod with maintenance flag
- **Deliverable:** CI green; checklist signed off

### Phase 5 — Release readiness & milestone close

- Production deploy executed
- Backups cron verified
- Uptime monitor configured
- Update `PROJECT_STATUS.md`, `ARCHITECTURE.md`, `TESTING_STRATEGY.md`, `RELEASE_NOTES.md`
- `finish_task.py` → Quality Gate → roadmap advance
- **Deliverable:** live HTTPS URL for Ernesto to begin Closed Beta prep

---

## 8. Cost estimate

Estimates in **USD/month**, Chile-friendly providers, **excluding** domain (~$15–25/year) and **excluding** real WebPay/Transbank fees.

### MVP launch (0–50 users, beta invite-only)

| Item | Option B (recommended) | Option A (all-in-one VPS) |
|------|------------------------|---------------------------|
| Frontend (Vercel Hobby) | $0 | — |
| VPS (2 vCPU, 4 GB) | $8–12 (Hetzner) / $12–18 (DO) | $8–18 |
| Postgres | $0 (on VPS) | $0 (on VPS) |
| Backups (off-VPS optional) | $0–2 | $0–2 |
| Uptime monitor | $0 | $0 |
| **Total** | **~$8–18/mo** | **~$8–20/mo** |

### First 100 users (~500–2k page views/day peak)

| Item | Est. monthly |
|------|----------------|
| Vercel | $0 (within hobby limits) |
| VPS | $12–18 (same box likely sufficient) |
| Managed DB upgrade (optional) | +$0–15 if moving PG off VPS |
| **Total** | **~$12–25/mo** |

### First 1,000 users (~10k–30k page views/day peak)

| Item | Est. monthly |
|------|----------------|
| Vercel Pro (if bandwidth/build limits hit) | $20 |
| VPS upgrade (4 vCPU, 8 GB) or 2nd read replica | $24–48 |
| Managed Postgres (Neon/DO) | $15–25 |
| CDN/logs (optional) | $0–10 |
| **Total** | **~$35–80/mo** |

At 1k users, **vertical scale + connection pool tuning** (`DB_POOL_*` already in config) should suffice before microservices.

---

## 9. Risks

### Technical risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hardcoded CORS/API URL blocks prod | Deploy broken | Phase 3 env-driven config |
| Missing migration on prod DB | 500 on order/notification create | CI migration smoke; deploy checklist |
| WebPay callback URL mismatch | Payments fail silently | Document `WEBPAY_RETURN_URL_BASE`; test in sandbox |
| SQLite accidentally in prod | Data loss, no concurrency | Enforce Postgres in prod runbook |
| Single VPS disk failure | Full outage | Daily backups + restore drill |
| JWT secret rotation | All users logged out | Planned maintenance window |
| No rate limiting | Abuse at launch | Closed Beta invite; add limits in beta milestone |

### Operational risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Single operator (Ernesto) | Bus factor, slow incident response | Runbooks, automated backups, simple architecture |
| Manual deploy errors | Downtime | Checklist; eventually CI deploy |
| Admin key leak | Full admin API access | Strong key, not in frontend, rotate if exposed |
| Dispute evidence external URLs | Broken links, malicious content | UX guidance; future upload service |

### Cost risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| OpenAI NL search enabled | Unexpected API bills | Keep disabled in prod until needed |
| Vercel bandwidth overage | Bill surprise | Monitor; static export only if needed |
| Managed PaaS tier creep | 3× VPS cost | Start VPS; migrate when revenue covers |

---

## 10. Recommendation

### Exact deployment architecture

**Option B (split):**

- **Frontend:** Vercel — GitHub integration, `NEXT_PUBLIC_API_URL=https://api.<domain>`
- **Backend + DB:** Hetzner Cloud **CPX22** (or DigitalOcean **Basic $12**) in **São Paulo** or **US East** (lowest latency/cost tradeoff for Chile; measure and move if needed)
- **Reverse proxy:** **Caddy 2** in Docker (automatic HTTPS)
- **Stack:** Existing `docker-compose.yml` extended for prod; Postgres internal only
- **File storage:** None for MVP

### Hosting providers

| Role | Provider | Why |
|------|----------|-----|
| Frontend | **Vercel** | Next.js 16 native, free SSL, minimal ops |
| API + Postgres | **Hetzner Cloud** or **DigitalOcean** | Predictable ~$10–12/mo, Docker-friendly |
| Domain | **NIC Chile** / Namecheap for `.cl` | Local trust for Chilean collectors |
| Uptime | **UptimeRobot** (free) | Ping `/health` |
| Backups | **cron + pg_dump** → Backblaze B2 or local encrypted | Cheapest reliable off-VPS |

### Estimated monthly cost

- **Launch / 100 users:** **USD 10–18/month**
- **1,000 users:** **USD 35–55/month** (VPS bump + optional managed DB)

### Expected implementation effort

| Phase | Effort (single developer) |
|-------|---------------------------|
| Phase 1 Architecture & docs | 0.5–1 day |
| Phase 2 Docker/prod compose + health | 1–2 days |
| Phase 3 Env-driven CORS/API URL | 1 day |
| Phase 4 CI + migration smoke + checklist | 1–2 days |
| Phase 5 First prod deploy + validation | 1 day |
| **Total** | **~4–7 days** |

Does **not** include real Transbank integration, legal pages, or Closed Beta features.

---

## References

| Document | Path |
|----------|------|
| MVP roadmap | `backend/MVP_ROADMAP.md` |
| Backend status | `backend/PROJECT_STATUS.md` |
| Workspace status | `workspace/PROJECT_STATUS.md` |
| Architecture | `backend/ARCHITECTURE.md` |
| Business rules | `backend/BUSINESS_RULES.md` |
| Testing strategy | `backend/TESTING_STRATEGY.md` |
| Release notes | `workspace/RELEASE_NOTES.md` |
| Docker compose | `backend/docker-compose.yml` |
| Env template | `backend/.env.example` |
| Notifications scope (pattern) | `workspace/NOTIFICATIONS_SCOPE_REPORT.md` |

---

*Report only — no deployment implementation, roadmap status change, or milestone advance performed.*
