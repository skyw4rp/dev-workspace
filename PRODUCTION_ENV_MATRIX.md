# Production Environment Matrix — Melómanos Marketplace

**Purpose:** Single reference for environment variables across **local**, **Docker dev**, and **production**.  
**Companion docs:** [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md), [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md)  
**Rule:** **Never commit production secrets.** Only [`backend/.env.example`](../backend/.env.example) is tracked in git.

---

## Environment summary

| Environment | Frontend | Backend | Database | Config storage |
|-------------|----------|---------|----------|----------------|
| **Local dev** | `npm run dev` :3000 | `run.py` / uvicorn :8000 | SQLite or local Postgres | `backend/.env.local` |
| **Local Docker** | `npm run dev` :3000 | Compose `api` :8000 | Compose `db` | `backend/.env.docker` |
| **Production** | Vercel | VPS Docker `api` | VPS Docker `db` (internal) | Vercel dashboard + VPS `/opt/melomanos/.env.production` (not in git) |

**Staging:** not used for MVP. Rehearse with local Docker prod compose before cutover.

---

## Production URLs (approved)

| Surface | URL |
|---------|-----|
| Frontend (canonical) | `https://melomanos.cl` |
| Frontend (alias) | `https://www.melomanos.cl` |
| API | `https://api.melomanos.cl` |
| WebPay return base (when enabled) | `https://melomanos.cl/orders` |
| WebPay callback (placeholder) | `https://api.melomanos.cl/payments/webpay/callback` |

---

## Backend variables (FastAPI / Pydantic Settings)

Loaded from process environment. Production file example: `/opt/melomanos/.env.production` on VPS (permissions `600`, owner deploy user).

| Variable | Required (prod) | Local default | Production value / notes |
|----------|-----------------|---------------|---------------------------|
| `DATABASE_URL` | **Yes** | SQLite or `localhost` Postgres | `postgresql+psycopg2://melomanos:STRONG_PASSWORD@db:5432/melomanos` — host `db` = Compose service name |
| `SECRET_KEY` | **Yes** | dev placeholder | `openssl rand -hex 32` — rotating logs out all users |
| `ALGORITHM` | **Yes** | `HS256` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | **Yes** | `30` | `30` (adjust if UX requires) |
| `ADMIN_KEY` | **Yes** | optional in dev | Strong random; `x-admin-key` header — **never** expose to frontend |
| `PAYMENT_PROVIDER_MODE` | **Yes** | `simulate` | `simulate` until WebPay go-live decision; then `webpay_placeholder` or future prod mode |
| `WEBPAY_CALLBACK_SECRET` | If WebPay | test secret | Must match webhook config; min 32 chars recommended |
| `WEBPAY_RETURN_URL_BASE` | If WebPay | `http://localhost:3000/orders` | `https://melomanos.cl/orders` |
| `CORS_ORIGINS` | **Yes** | `http://localhost:3000,http://127.0.0.1:3000` | `https://melomanos.cl,https://www.melomanos.cl` — comma-separated, **no wildcard** |
| `DB_POOL_PRE_PING` | No | `true` | `true` |
| `DB_POOL_SIZE` | No | `5` | `5` (raise if connection errors at scale) |
| `DB_POOL_MAX_OVERFLOW` | No | `10` | `10` |
| `DB_POOL_TIMEOUT` | No | `30` | `30` |
| `DB_POOL_RECYCLE` | No | unset | `1800` recommended for long-lived VPS |
| `OPENAI_API_KEY` | No | unset | Omit or set if NL search enabled |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | unchanged |
| `OPENAI_NL_SEARCH_ENABLED` | No | `false` | **`false` in prod** until cost reviewed |
| `OPENAI_NL_MAX_REQUESTS_PER_DAY` | No | `100` | lower if enabled |
| `OPENAI_NL_CACHE_TTL_HOURS` | No | `24` | unchanged |

### Not in Pydantic Settings (local `run.py` only)

| Variable | Production |
|----------|------------|
| `APP_HOST` | N/A — uvicorn in Docker uses `0.0.0.0:8000` |
| `APP_PORT` | `8000` internal |
| `APP_RELOAD` | **`false`** — never reload in prod |

---

## Frontend variables (Vercel)

Set in **Vercel → Project → Settings → Environment Variables** (Production scope).

| Variable | Required (prod) | Local | Production |
|----------|-----------------|-------|------------|
| `NEXT_PUBLIC_API_URL` | **Yes** | `http://127.0.0.1:8000` when unset | `https://api.melomanos.cl` |
| `NEXT_PUBLIC_PAYMENT_PROVIDER_MODE` | No | unset / localStorage | Match backend: `simulate` or `webpay_placeholder` |

**E2E only** (not production):

| Variable | Default |
|----------|---------|
| `E2E_BASE_URL` | `http://localhost:3000` |
| `E2E_API_URL` | `http://127.0.0.1:8000` |

---

## Caddy / infrastructure (Phase 2+)

Not application env vars — documented for operator.

| Item | Value |
|------|-------|
| `ACME_EMAIL` | Operator email for Let's Encrypt (Caddy config) |
| Public ports on VPS | `80`, `443` only (SSH restricted) |
| Postgres port | **Not** published to host in prod compose |

---

## Secrets handling

### Generation

```bash
# JWT signing
openssl rand -hex 32

# Admin key / WebPay callback secret
openssl rand -base64 32
```

### Storage

| Secret | Where stored | Never |
|--------|--------------|-------|
| `SECRET_KEY`, `ADMIN_KEY`, `WEBPAY_*`, DB password | VPS `.env.production` + password manager | Git, Slack, screenshots |
| Vercel env vars | Vercel encrypted env | Client-side bundle except `NEXT_PUBLIC_*` |
| SSH keys | Operator machine + VPS `authorized_keys` | Password SSH login |

### Rotation

| Secret | Effect of rotation | Procedure |
|--------|-------------------|-----------|
| `SECRET_KEY` | All JWTs invalid | Maintenance window; redeploy API |
| `ADMIN_KEY` | Old admin clients fail | Update operator browser/admin scripts |
| `WEBPAY_CALLBACK_SECRET` | Old webhooks rejected | Coordinate with payment provider |
| DB password | API cannot connect | Update Postgres + `DATABASE_URL`; restart API |

### What must not be in frontend

- `SECRET_KEY`, `ADMIN_KEY`, `WEBPAY_CALLBACK_SECRET`, `DATABASE_URL`, `OPENAI_API_KEY`

---

## Local vs production quick reference

| Concern | Local | Production |
|---------|-------|------------|
| API URL | `http://127.0.0.1:8000` | `https://api.melomanos.cl` |
| CORS | localhost:3000 | melomanos.cl origins |
| DB | SQLite OK | PostgreSQL only |
| HTTPS | Optional | Required |
| Payment | `simulate` typical | Business decision before beta |
| File uploads | N/A (URLs only) | N/A (URLs only) |

---

## Phase 3 implementation checklist (env-related)

When coding Phase 3, update this matrix if new variables are added:

- [ ] `CORS_ORIGINS` in `app/core/config.py`
- [ ] `NEXT_PUBLIC_API_URL` in `frontend/src/lib/api.ts`
- [ ] [`backend/.env.example`](../backend/.env.example) production section
- [ ] Vercel env documented in [`frontend/README.md`](../frontend/README.md)

---

*Last updated: Production Deployment Phase 3 — CORS_ORIGINS and NEXT_PUBLIC_API_URL wired in code.*
