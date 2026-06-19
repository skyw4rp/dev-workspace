# Production Deployment — Phase 5 Operator Checklist

**Purpose:** Step-by-step checklist for **live cutover** using the approved stack.  
**Status:** Preparation document — **no infrastructure provisioned yet**  
**Operator:** Single maintainer (Ernesto)

**Approved stack (locked):**

| Layer | Provider / tech |
|-------|-----------------|
| Frontend | **Vercel** → `melomanos.cl`, `www.melomanos.cl` |
| Backend API | **DigitalOcean Droplet** — São Paulo **`gru1`** |
| Database | **PostgreSQL 15** (Docker, same VPS, internal only) |
| TLS / reverse proxy | **Caddy 2** + Let's Encrypt |
| DNS | **Cloudflare** (free) |
| Monitoring | **UptimeRobot** (free) |
| Backups | **Daily `pg_dump`** on VPS; **Backblaze B2** off-site (configure after launch) |

**Companion docs:**

- [`PRODUCTION_DEPLOYMENT_DECISION_REPORT.md`](PRODUCTION_DEPLOYMENT_DECISION_REPORT.md) — locked decisions
- [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md) — phase overview
- [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md) — migrate, backup, rollback detail
- [`backend/README_DEPLOYMENT.md`](../backend/README_DEPLOYMENT.md) — Docker compose commands
- [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md) — full env reference

**VPS layout:**

```
/opt/melomanos/
  backups/                 # pg_dump archives (local retention)
  repo/                    # git clone
    backend/               # docker compose working directory
      .env.production      # secrets — chmod 600, never commit
      docker-compose.yml
      docker-compose.prod.yml
      deployment/Caddyfile
```

---

## How to use this document

1. Complete sections **1–6** before first deploy.
2. Execute **7–10** on cutover day.
3. Configure **11–12** within 24 h of go-live (B2 can follow within first week).
4. Review **13** before every deploy; use **14** for final go/no-go.

Check boxes as you go. Record dates and IPs in the sign-off at the end.

---

## 1. Accounts to create

| # | Account | Purpose | Plan | Done |
|---|---------|---------|------|:----:|
| 1 | **DigitalOcean** | VPS (Droplet), Cloud Firewall, optional snapshots | Pay-as-you-go | [ ] |
| 2 | **Vercel** | Frontend hosting + domains | Hobby (upgrade to Pro if needed) | [ ] |
| 3 | **Cloudflare** | DNS for `melomanos.cl` | Free | [ ] |
| 4 | **NIC Chile–accredited registrar** | Register / own `melomanos.cl` | Annual `.cl` fee | [ ] |
| 5 | **GitHub** | Source repos (backend + frontend) — already exist | — | [ ] |
| 6 | **UptimeRobot** | External uptime monitors | Free (50 monitors) | [ ] |
| 7 | **Backblaze B2** | Off-site backup bucket (post-launch OK) | Pay per GB | [ ] |
| 8 | **Password manager** | Master copy of all secrets | — | [ ] |

**Optional (later):** Transbank / WebPay production credentials when leaving `simulate` mode.

---

## 2. DigitalOcean Droplet specs

Create **one** Droplet in **São Paulo (`gru1`)**.

| Setting | Value |
|---------|-------|
| **Image** | Ubuntu **22.04 LTS** |
| **Plan** | Basic |
| **Size** | **2 vCPU, 4 GB RAM, 80 GB SSD** (~$24/mo) |
| **Region** | **São Paulo — `gru1`** |
| **Authentication** | SSH key only (no password) |
| **Hostname** | e.g. `melomanos-api-gru1` |
| **Monitoring** | Enable DO monitoring agent (optional, free) |
| **Backups** | DO automated backups optional (~20% extra); MVP uses manual `pg_dump` |

**After create — record:**

| Field | Value |
|-------|-------|
| Droplet public IPv4 | __________________ |
| Droplet ID | __________________ |
| Deploy SSH user | e.g. `deploy` (non-root) |

**Cloud Firewall (attach to Droplet):**

| Direction | Protocol | Port | Source |
|-----------|----------|------|--------|
| Inbound | TCP | 22 | Your home/office IP (or VPN) |
| Inbound | TCP | 80 | `0.0.0.0/0`, `::/0` |
| Inbound | TCP | 443 | `0.0.0.0/0`, `::/0` |
| Outbound | All | All | Allow (default) |

- [ ] Droplet created in `gru1`
- [ ] Cloud Firewall attached
- [ ] Public IPv4 recorded

---

## 3. Required DNS records (Cloudflare)

1. Register **`melomanos.cl`** at NIC-accredited registrar.
2. Add site to **Cloudflare**; update registrar nameservers to Cloudflare NS.
3. Add records:

| Name | Type | Content | Proxy (orange cloud) | Purpose |
|------|------|---------|----------------------|---------|
| `@` | `A` or `CNAME` | Per **Vercel** domain instructions | Per Vercel docs | Apex → frontend |
| `www` | `CNAME` | `cname.vercel-dns.com` (or Vercel-provided) | Per Vercel docs | www → frontend |
| `api` | `A` | **Droplet public IPv4** | **DNS only (grey cloud)** | API → VPS / Caddy |

**Critical:** `api` must be **grey cloud (DNS only)** so Caddy can obtain Let's Encrypt certificates via HTTP-01 on the VPS.

**Vercel:** Project → Settings → Domains → add `melomanos.cl` and `www.melomanos.cl`.

**Verify propagation:**

```bash
dig +short melomanos.cl
dig +short www.melomanos.cl
dig +short api.melomanos.cl
```

- [ ] Nameservers point to Cloudflare
- [ ] `api` A record → Droplet IP (grey cloud)
- [ ] Vercel domains configured for apex + www
- [ ] `dig` returns expected targets

---

## 4. Required Vercel environment variables

**Project → Settings → Environment Variables → scope: Production**

| Variable | Required | Example value | Notes |
|----------|----------|---------------|-------|
| `NEXT_PUBLIC_API_URL` | **Yes** | `https://api.melomanos.cl` | No trailing slash |
| `NEXT_PUBLIC_PAYMENT_PROVIDER_MODE` | No | `simulate` | Match backend when WebPay enabled |

**Do not set on Vercel:** `SECRET_KEY`, `ADMIN_KEY`, `DATABASE_URL`, `WEBPAY_CALLBACK_SECRET`.

After changing `NEXT_PUBLIC_*` vars → **Redeploy** production.

- [ ] `NEXT_PUBLIC_API_URL` set for Production
- [ ] Production deployment succeeded after env change

---

## 5. Required backend `.env.production` vars

**Path on VPS:** `/opt/melomanos/repo/backend/.env.production`  
**Template:** [`backend/.env.production.example`](../backend/.env.production.example)

Generate secrets locally (`openssl rand -hex 32`); store master copy in password manager.

| Variable | Required | Notes |
|----------|----------|-------|
| `POSTGRES_USER` | Yes | `melomanos` |
| `POSTGRES_DB` | Yes | `melomanos` |
| `POSTGRES_PASSWORD` | Yes | Strong random; must match `DATABASE_URL` |
| `DATABASE_URL` | Yes | `postgresql+psycopg2://melomanos:PASSWORD@db:5432/melomanos` |
| `SECRET_KEY` | Yes | Rotating logs out all users |
| `ALGORITHM` | Yes | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Yes | e.g. `30` |
| `ADMIN_KEY` | Yes | `x-admin-key` header; never expose to frontend |
| `CORS_ORIGINS` | Yes | `https://melomanos.cl,https://www.melomanos.cl` |
| `PAYMENT_PROVIDER_MODE` | Yes | `simulate` until WebPay go-live |
| `WEBPAY_CALLBACK_SECRET` | If WebPay | Min 32 chars |
| `WEBPAY_RETURN_URL_BASE` | If WebPay | `https://melomanos.cl/orders` |
| `ACME_EMAIL` | Yes | Email for Let's Encrypt (Caddy) |
| `OPENAI_API_KEY` | No | Omit unless NL search enabled in prod |
| `OPENAI_NL_SEARCH_ENABLED` | No | **`false` recommended at launch** |

**Permissions:**

```bash
chmod 600 .env.production
chown deploy:deploy .env.production   # adjust user
```

- [ ] `.env.production` created from example (no placeholders left)
- [ ] `POSTGRES_PASSWORD` matches password in `DATABASE_URL`
- [ ] File permissions `600`
- [ ] Secrets saved in password manager

---

## 6. VPS bootstrap steps

Run as root or sudo on fresh Droplet (Ubuntu 22.04).

### 6.1 System prep

```bash
apt update && apt upgrade -y
timedatectl set-timezone America/Santiago
```

### 6.2 Create deploy user

```bash
adduser deploy
usermod -aG sudo deploy
mkdir -p /home/deploy/.ssh
cp ~/.ssh/authorized_keys /home/deploy/.ssh/
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys
```

Harden SSH (`/etc/ssh/sshd_config`): disable password auth, optionally disable root login → `systemctl restart sshd`.

### 6.3 Install Docker

```bash
# Official Docker Engine + Compose plugin (see docs.docker.com)
curl -fsSL https://get.docker.com | sh
usermod -aG docker deploy
```

Log in as `deploy` and verify: `docker compose version`.

### 6.4 Directory layout

```bash
sudo mkdir -p /opt/melomanos/backups
sudo chown -R deploy:deploy /opt/melomanos
cd /opt/melomanos
git clone <backend-repo-url> repo
# Or clone monorepo and use repo/backend — match your git layout
```

### 6.5 Production env file

```bash
cd /opt/melomanos/repo/backend
cp .env.production.example .env.production
nano .env.production   # paste real values
chmod 600 .env.production
```

### 6.6 Validate compose config

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
```

- [ ] System updated; timezone `America/Santiago`
- [ ] `deploy` user + SSH key auth
- [ ] Docker + Compose installed
- [ ] `/opt/melomanos/backups` exists
- [ ] Backend repo cloned
- [ ] `.env.production` in place
- [ ] `docker compose … config` succeeds

---

## 7. Docker Compose deploy commands

From **`/opt/melomanos/repo/backend`** as `deploy`:

### First deploy (build + start stack)

```bash
cd /opt/melomanos/repo/backend
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Verify containers

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f caddy
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f api
```

### Routine update (new release)

```bash
cd /opt/melomanos/repo/backend
git pull origin main
docker compose -f docker-compose.yml -f docker-compose.prod.yml build api
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

- [ ] Stack up (`ps` shows api, db, caddy healthy/running)
- [ ] Caddy obtained TLS cert (no ACME errors in logs)

---

## 8. Alembic migration command

**When:** After stack is up, **before** accepting user traffic.

```bash
cd /opt/melomanos/repo/backend
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api \
  alembic upgrade head
```

Verify:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api \
  alembic current
```

- [ ] `alembic upgrade head` completed without error
- [ ] `alembic current` shows head revision

---

## 9. Health check validation

### From operator machine

```bash
curl -sS https://api.melomanos.cl/health
```

**Expected:** HTTP 200, body similar to:

```json
{"status":"ok","service":"melomanos-api"}
```

### Additional probes

```bash
curl -sS -o /dev/null -w "%{http_code}" https://api.melomanos.cl/
curl -sS -o /dev/null -w "%{http_code}" https://melomanos.cl
```

### On VPS (internal)

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api \
  python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read())"
```

- [ ] `https://api.melomanos.cl/health` → 200
- [ ] `https://melomanos.cl` → 200 (Vercel)
- [ ] No secrets in `/health` response

---

## 10. Manual smoke test checklist

Perform in browser (incognito) or with test accounts.

| # | Test | Pass |
|---|------|:----:|
| 1 | Homepage loads at `https://melomanos.cl` | [ ] |
| 2 | Register new account | [ ] |
| 3 | Login / logout | [ ] |
| 4 | Browse listings | [ ] |
| 5 | View listing detail | [ ] |
| 6 | Seller: create listing (new vinyl) | [ ] |
| 7 | Buyer: create order from listing | [ ] |
| 8 | Simulate payment (if `PAYMENT_PROVIDER_MODE=simulate`) | [ ] |
| 9 | Orders page shows order | [ ] |
| 10 | Messages / notifications bell (if enabled) | [ ] |
| 11 | Profile / subscription card loads | [ ] |
| 12 | Admin panel with production `ADMIN_KEY` (operator only) | [ ] |
| 13 | CORS: no browser console errors on API calls from frontend | [ ] |

**Record:** test account emails used, any failures, git SHA deployed.

---

## 11. Monitoring setup (UptimeRobot)

Create account at [uptimerobot.com](https://uptimerobot.com).

| Monitor name | URL | Type | Interval | Alert |
|--------------|-----|------|----------|-------|
| Melomanos homepage | `https://melomanos.cl` | HTTP(s) | 5 min | Email |
| Melomanos API health | `https://api.melomanos.cl/health` | HTTP(s) | 5 min | Email |

**Keyword monitor (optional):** API health body contains `"status":"ok"`.

**Optional — DigitalOcean alerts:** CPU > 90%, disk > 80% → email.

- [ ] Homepage monitor green
- [ ] API health monitor green
- [ ] Alert email verified (test notification)

---

## 12. Backup setup

### 12.1 Local daily backup (required at launch)

Create script `/opt/melomanos/backups/backup.sh` (example — adjust paths):

```bash
#!/bin/bash
set -euo pipefail
BACKUP_DIR=/opt/melomanos/backups
STAMP=$(date +%Y%m%d_%H%M%S)
cd /opt/melomanos/repo/backend
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T db \
  pg_dump -U melomanos -d melomanos --no-owner --format=custom \
  > "$BACKUP_DIR/melomanos_${STAMP}.dump"
gzip -f "$BACKUP_DIR/melomanos_${STAMP}.dump"
find "$BACKUP_DIR" -name 'melomanos_*.dump.gz' -mtime +7 -delete
```

```bash
chmod +x /opt/melomanos/backups/backup.sh
```

**Cron (deploy user):** `crontab -e`

```
0 3 * * * /opt/melomanos/backups/backup.sh >> /opt/melomanos/backups/backup.log 2>&1
```

**Before every deploy:** run backup manually.

### 12.2 Backblaze B2 off-site (within first week)

| Step | Action |
|------|--------|
| 1 | Create B2 bucket (private) |
| 2 | Create application key (minimal scope) |
| 3 | Install `rclone` on VPS; configure remote |
| 4 | Weekly cron: sync latest dump to B2; retain 4 weekly |

Credentials → password manager only; not in git.

- [ ] Local backup script tested (file created in `/opt/melomanos/backups/`)
- [ ] Daily cron installed
- [ ] Manual pre-cutover backup taken
- [ ] B2 bucket planned or configured (can follow within 7 days)

---

## 13. Rollback steps

### Frontend (Vercel)

1. Vercel → Deployments → last green deployment → **Promote to Production**
2. Confirm `NEXT_PUBLIC_API_URL` unchanged

### Backend (VPS)

1. Note failing git SHA; checkout previous tag/commit
2. Rebuild and restart:

```bash
cd /opt/melomanos/repo/backend
git checkout <previous-tag-or-sha>
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build api
```

3. **Do not downgrade DB** unless restoring from backup

### Database restore (bad migration / data loss)

1. Stop API: `docker compose … stop api`
2. Restore from latest good dump (see [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md) §6)
3. Start API; re-run smoke tests (§10)

### When to rollback

- Sustained API 5xx after deploy
- Migration failure
- Payment/webhook regression

- [ ] Previous git tag/SHA documented before each deploy
- [ ] Latest backup verified restorable (quarterly drill)

---

## 14. Final go / no-go checklist

Complete **immediately before** directing real users to production.

### Pre-cutover (code & CI)

| # | Item | Go |
|---|------|:--:|
| 1 | Quality Gate passed locally (`py run_audit.py` or `finish_task.py` dry-run) | [ ] |
| 2 | GitHub Actions green (backend + frontend) on release commit | [ ] |
| 3 | No open P0 bugs for auth, orders, payments | [ ] |

### Infrastructure

| # | Item | Go |
|---|------|:--:|
| 4 | Droplet `gru1` running; firewall 22/80/443 only | [ ] |
| 5 | DNS: `api` → Droplet (grey cloud); apex/www → Vercel | [ ] |
| 6 | `.env.production` complete; not in git | [ ] |
| 7 | Vercel `NEXT_PUBLIC_API_URL` = `https://api.melomanos.cl` | [ ] |
| 8 | CORS matches Vercel domains | [ ] |

### Deploy verification

| # | Item | Go |
|---|------|:--:|
| 9 | `docker compose … up -d --build` successful | [ ] |
| 10 | `alembic upgrade head` successful | [ ] |
| 11 | `https://api.melomanos.cl/health` → 200 | [ ] |
| 12 | `https://melomanos.cl` loads | [ ] |
| 13 | Manual smoke (§10) passed | [ ] |

### Ops readiness

| # | Item | Go |
|---|------|:--:|
| 14 | UptimeRobot monitors green | [ ] |
| 15 | Local backup cron active; pre-launch dump taken | [ ] |
| 16 | Rollback plan understood (§13) | [ ] |
| 17 | `DEPLOYMENT_RUNBOOK.md` reviewed | [ ] |

### Decision

| Field | Value |
|-------|-------|
| **Go / No-Go** | GO ☐  NO-GO ☐ |
| Date (America/Santiago) | |
| Operator | |
| Backend git SHA | |
| Frontend Vercel deployment URL / SHA | |
| Alembic revision | |
| Droplet IPv4 | |
| Notes | |

**NO-GO if any of:** health check fails, migration fails, smoke test fails, secrets missing, DNS not propagated, or backup not taken.

---

## After go-live (Phase 5 completion)

When all sections above are done and production is stable:

1. Update `PROJECT_STATUS.md`, `ARCHITECTURE.md`, `TESTING_STRATEGY.md`, `RELEASE_NOTES.md`
2. Mark Phase 5 **DONE** in [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md)
3. Run Quality Gate + `finish_task.py` with `--advance-roadmap` **only when explicitly ready**

---

*Checklist only — no live cutover performed. Roadmap not advanced.*
