# Production Deployment — Infrastructure Decision Report

**Date:** 2026-06-17  
**Purpose:** Lock infrastructure choices before **Production Deployment Phase 5** (cutover).  
**Status:** Decision document — **no implementation in this step**

**Approved architecture (unchanged):**

| Layer | Choice |
|-------|--------|
| Frontend | Vercel (Next.js) → `melomanos.cl`, `www.melomanos.cl` |
| Backend | FastAPI (Docker) on single VPS → `api.melomanos.cl` |
| Database | PostgreSQL 15 (Docker, same VPS, internal only) |
| Reverse proxy / TLS | Caddy 2 + Let's Encrypt |
| Staging | None (local Docker prod compose + Closed Beta on prod) |

**Context:** Chilean vinyl marketplace (Melómanos). Single operator (Ernesto).  
**Traffic expectations:** launch (very low) → Closed Beta (tens) → early growth (hundreds–low thousands).

**Optimization priorities:** low cost, simplicity, reliability, easy recovery, minimal ops burden.

**Companion docs:** [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md), [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md), [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md)

---

## Executive summary

Melómanos should deploy **Option B** as already approved, with these **final locked decisions**:

| Decision | Choice |
|----------|--------|
| **VPS provider** | **DigitalOcean** — Droplet in **São Paulo (`gru1`)** |
| **MVP server size** | **2 vCPU, 4 GB RAM, 80 GB SSD** (~$24/mo) |
| **Domain ownership** | Register **`melomanos.cl`** via **NIC Chile–accredited registrar** |
| **DNS** | **Cloudflare** (free plan) — apex/`www` → Vercel, `api` → VPS |
| **Monitoring** | **UptimeRobot** (free) — 2 HTTP monitors on homepage + `GET /health` |
| **Backups** | **Daily `pg_dump`** on VPS + **weekly off-site** to **Backblaze B2** |
| **Expected monthly cost (launch → ~1k users)** | **~USD 18–28/mo** (VPS dominates; scales mainly by VPS resize) |

**Budget alternative:** Hetzner **CPX22** (Ashburn, US) at ~€7/mo saves ~$15/mo but adds ~80–100 ms RTT from Chile — acceptable for Closed Beta, revisit if UX feels slow.

**Operator workload:** ~1–2 h/month routine (patch reboot, backup verify, deploy) + ~15 min/deploy via runbook.

---

## 1. VPS provider comparison

All three are suitable for Docker Compose (Caddy + API + Postgres). None require Kubernetes for this MVP.

### Summary table

| Criterion | Hetzner Cloud | DigitalOcean | Vultr |
|-----------|---------------|--------------|-------|
| **Chile latency** | ⚠️ No SA region; US East ~120–150 ms from Santiago | ✅ **São Paulo ~35–55 ms** | ✅ **São Paulo ~35–55 ms** |
| **Reliability** | ✅ Excellent uptime reputation | ✅ Good; mature SLA on paid tiers | ✅ Good; occasional maintenance notices |
| **Operational simplicity** | ✅ Simple panel, great docs; EU-centric | ✅ **Best for solo ops** — familiar UX, snapshots, firewalls | ⚠️ Adequate; slightly more DIY feel |
| **Cost (2 vCPU / 4 GB)** | ✅ **~€6.49/mo** (CPX22, 80 GB) | ⚠️ **~$24/mo** (Basic 4 GB) | ⚠️ **~$24/mo** (High Frequency 4 GB, SA) |
| **Docker / Ubuntu** | ✅ Native cloud-init images | ✅ 1-click Docker or Ubuntu 22.04 | ✅ Ubuntu + user-data |
| **Snapshots / recovery** | ✅ Backups add-on (~20% extra) | ✅ **Droplet snapshots** (manual, simple) | ✅ Snapshots + auto backup option |
| **Firewall** | ✅ Cloud firewall | ✅ **Cloud Firewalls** (easy rules) | ✅ Firewall groups |
| **Recommendation** | **Budget pick** | **✅ Primary pick** | **Strong latency alternative** |

### Hetzner Cloud

**Pros:** Lowest cost per spec (CPX22: 2 vCPU, 4 GB, 80 GB NVMe). Predictable billing. Strong community for self-hosting.

**Cons:** No South America POP — nearest useful regions are **Ashburn (US)** or **Singapore**. Chilean users see higher API latency than GRU-hosted rivals. Support timezone EU-biased.

**Verdict:** Choose if **cost > latency** for Closed Beta. Plan migration or second region only if latency complaints appear.

### DigitalOcean

**Pros:** **`gru1` (São Paulo)** region — best practical latency for Chile without local VPS niche providers. Clear docs, cloud firewalls, snapshots, monitoring agent optional. Single-operator friendly.

**Cons:** ~3× Hetzner price for comparable 4 GB tier. Bandwidth overage possible at scale (unlikely at MVP traffic).

**Verdict:** **Recommended primary provider** — balances Chile latency, recovery (snapshots), and ops simplicity for one person.

### Vultr

**Pros:** São Paulo available; competitive specs/pricing; hourly billing good for experiments.

**Cons:** Panel and docs slightly less polished than DO for first-time solo ops. Less Melómanos project precedent (plan/docs already reference Hetzner/DO).

**Verdict:** Valid alternative if DO account/billing issues arise; not the default recommendation.

### **Decision: DigitalOcean (São Paulo `gru1`)**

Rationale: Chile-facing marketplace; API snappiness matters for browse/checkout; single operator benefits from DO snapshots + firewall UX; ~$24/mo is acceptable for MVP.

---

## 2. VPS sizing

Stack on one VM: **Caddy + FastAPI (uvicorn) + PostgreSQL 15 + Docker overhead + OS**.

### Estimates by phase

| Phase | Concurrent users (order of magnitude) | vCPU | RAM | Storage | Notes |
|-------|-------------------------------------|------|-----|---------|-------|
| **Launch** | < 10 | 1–2 | **4 GB** | 40–80 GB | Postgres + API fit comfortably; headroom for migrations |
| **Closed Beta** | ~10–50 | 2 | **4 GB** | 80 GB | Same box; monitor RAM during peak |
| **~100 users** | ~20–40 concurrent peak | 2 | **4 GB** | 80 GB | Still sufficient if NL search off; watch DB connections |
| **~1000 users** | ~50–150 concurrent peak | **4** | **8 GB** | **160 GB** | Vertical resize; add connection pool tuning before second server |

**Storage drivers:** listings/orders/messages text — small; no file blobs on VPS. 80 GB is ample for OS + Docker + DB + **local backup staging** (7 daily dumps).

### **MVP size (locked)**

| Spec | Value |
|------|-------|
| vCPU | **2** |
| RAM | **4 GB** |
| SSD | **80 GB** |
| Provider SKU | DigitalOcean **Basic Droplet** — 2 vCPU / 4 GB / 80 GB SSD — **`gru1`** |

**Resize trigger:** sustained RAM > 75%, swap use, or Postgres OOM → upgrade to 8 GB before optimizing code.

---

## 3. Domain strategy

### `.cl` registry reality

**`melomanos.cl`** is under **NIC Chile** (`.cl` ccTLD). Registration must go through an **accredited registrar** or NIC directly. Pricing typically **~USD 15–35/year** depending on registrar and promotions.

### Options analyzed

| Approach | Domain ownership | DNS | Pros | Cons |
|----------|------------------|-----|------|------|
| **NIC Chile / accredited local registrar** | ✅ Direct `.cl` | Registrar DNS or export NS | Official; supports Chilean billing/RUT if needed | UI varies; apex DNS can be fiddly |
| **Registrar + Cloudflare DNS** | ✅ At registrar | **Cloudflare (free)** | Free DNS, fast propagation, DDoS edge for `api`, easy records | Must point NS to Cloudflare after purchase |
| **Cloudflare Registrar** | ✅ If `.cl` supported on account | Built-in | Single pane | `.cl` availability varies by account/region |
| **Vercel DNS only** | At registrar | Vercel for apex/www only | Simple frontend | **Poor fit for `api` subdomain** to VPS — split DNS still needed |

### DNS record plan (Cloudflare)

| Host | Type | Target |
|------|------|--------|
| `@` (apex) | `A` / `CNAME` | Vercel (per Vercel docs for apex) |
| `www` | `CNAME` | Vercel |
| `api` | `A` | VPS public IPv4 |
| — | Proxy | **`api` → DNS only (grey cloud)** so Caddy on VPS terminates TLS with Let's Encrypt |

**Important:** Orange-cloud (proxied) `api` breaks Caddy ACME HTTP-01 unless using Cloudflare origin certs (extra complexity). **Keep `api` unproxied** for MVP.

### **Decisions**

| Item | Choice |
|------|--------|
| **Domain ownership** | Register **`melomanos.cl`** at a **NIC Chile–accredited registrar** (e.g. NIC.cl portal or established Chilean reseller) |
| **DNS provider** | **Cloudflare** (free plan) — nameservers at registrar → Cloudflare |

---

## 4. Monitoring (MVP)

| Option | Cost | Fit for MVP |
|--------|------|-------------|
| **UptimeRobot** | Free (50 monitors, 5-min interval) | ✅ **Recommended** — enough for homepage + API health |
| **Better Stack** | Free tier limited; paid for on-call | Overkill for solo operator now |
| **DO Monitoring** | Free with Droplet | Useful supplement (CPU/RAM/disk); not a substitute for external uptime |
| **Raw cron + curl** | Free | Fragile; no alerting UI |

### **MVP monitoring setup (locked)**

| Monitor | URL | Interval | Alert |
|---------|-----|----------|-------|
| **Homepage** | `https://melomanos.cl` | 5 min | Email (UptimeRobot) |
| **API health** | `https://api.melomanos.cl/health` | 5 min | Email |

**Optional (Phase 5 day-1):** DO alert policy — disk > 80%, CPU > 90% for 5 min → email.

**Not in MVP:** APM, log aggregation, PagerDuty, synthetic checkout scripts (manual smoke post-deploy per runbook).

---

## 5. Backup strategy

**Goal:** Recover from operator error, bad migration, or VPS loss with **simple cron + off-site copy**.

### PostgreSQL backups

| Item | Policy |
|------|--------|
| **Method** | `pg_dump` custom format (`--format=custom`) via `docker compose exec -T db` |
| **Schedule** | **Daily 03:00** America/Santiago |
| **Pre-deploy** | **Manual dump** before every production release |
| **Local retention** | **7 daily** on VPS (`/opt/melomanos/backups/`, gzip) |
| **Off-site retention** | **4 weekly** copies on **Backblaze B2** (or DO Spaces if already on DO) |
| **Tooling** | `cron` + shell script; upload via **`rclone`** (B2 free egress to restore via download) |

### What is not backed up

- Vercel deployments (rebuild from git)
- External dispute/video URLs (third-party hosting)
- Docker images (rebuild from Dockerfile)

### Recovery targets (MVP)

| Metric | Target |
|--------|--------|
| **RPO** | ≤ 24 h (daily) — ≤ 1 h if pre-deploy dump taken |
| **RTO** | < 4 h manual (restore dump + redeploy compose) |

### **Decision:** cron + pg_dump + weekly B2 via rclone

---

## 6. Security checklist (minimum production)

| Area | Requirement |
|------|-------------|
| **Firewall** | Allow **22** (SSH, restrict to home IP if possible), **80**, **443** only. Deny all inbound else. Use **DO Cloud Firewall** + optionally `ufw` on host. |
| **SSH** | Key-based auth only; disable password login; non-root deploy user in `docker` group; no root SSH login. |
| **Secrets** | `.env.production` on VPS — `chmod 600`, owner deploy user; never in git. Vercel env for `NEXT_PUBLIC_*` only. Password manager master copy. |
| **TLS** | Caddy auto Let's Encrypt for `api.melomanos.cl`; Vercel TLS for frontend. HSTS default via Caddy/Vercel. |
| **Database exposure** | Postgres **not** published on host ports (prod compose `ports: !reset []`); only Docker network. |
| **ADMIN_KEY** | Backend env only; used via `x-admin-key` header; **never** in frontend or Vercel; rotate if leaked. |
| **CORS** | Explicit origins only (`melomanos.cl`, `www`) — no wildcard. |
| **Updates** | Unattended security updates OR monthly `apt upgrade` + reboot window. |
| **Backups** | Encrypted at rest on B2 bucket; bucket credentials not in git. |

---

## 7. Monthly cost estimate (USD)

Assumptions: DigitalOcean 4 GB GRU, Vercel Hobby, UptimeRobot free, B2 minimal storage, `.cl` domain amortized.

| Phase | VPS | Vercel | Domain | Monitoring | Backup (B2) | **Total/mo** |
|-------|-----|--------|--------|------------|-------------|--------------|
| **Launch** | $24 | $0 | ~$2 | $0 | ~$0.10 | **~$26** |
| **Closed Beta** | $24 | $0 | ~$2 | $0 | ~$0.25 | **~$26** |
| **~100 users** | $24 | $0–20* | ~$2 | $0 | ~$0.50 | **~$27–47** |
| **~1000 users** | $48** | $0–20* | ~$2 | $0 | ~$2 | **~$52–72** |

\* Vercel Hobby free until bandwidth/commercial limits; Pro ~$20/seat if required.  
\** Resize to 4 vCPU / 8 GB (~$48/mo on DO Basic tier) before adding second server.

### Budget stack (alternative)

| Phase | Hetzner CPX22 (US) + same rest | **Total/mo** |
|-------|--------------------------------|--------------|
| Launch → ~100 users | ~$7 VPS + ~$2 domain + ~$0.25 backup | **~$10** |
| ~1000 users | CPX31 or CPX41 (~€13–26) | **~$15–30** |

---

## 8. Final recommendation

### Infrastructure stack

```
Users (Chile)
    │
    ├─► melomanos.cl / www ──► Cloudflare DNS ──► Vercel (Next.js)
    │
    └─► api.melomanos.cl ──► Cloudflare DNS (DNS only) ──► DO VPS gru1
                                      │
                                      ├─► Caddy :443 (TLS)
                                      ├─► FastAPI :8000 (internal)
                                      └─► PostgreSQL 15 (internal volume)
```

### Locked decisions

| Component | Selection |
|-----------|-----------|
| **Provider** | DigitalOcean |
| **Region** | São Paulo (`gru1`) |
| **Server size** | 2 vCPU, 4 GB RAM, 80 GB SSD |
| **OS** | Ubuntu 22.04 LTS |
| **DNS** | Cloudflare (free); domain at NIC-accredited `.cl` registrar |
| **Monitoring** | UptimeRobot — homepage + `/health` |
| **Backups** | Daily pg_dump, 7-day local, weekly B2 off-site |
| **Frontend** | Vercel (unchanged) |

### Expected monthly cost

| Stage | Cost |
|-------|------|
| **Launch through Closed Beta (~100 users)** | **~USD 26/mo** |
| **Early growth (~1000 users)** | **~USD 52–72/mo** (after VPS resize + optional Vercel Pro) |

### Expected operator workload

| Activity | Frequency | Time |
|----------|-----------|------|
| Deploy (git pull, compose, migrate, smoke) | Per release | ~15–30 min |
| OS/security patches | Monthly | ~30 min |
| Backup spot-check (restore test to local Docker) | Quarterly | ~1 h |
| Uptime/monitor review | Weekly glance | ~5 min |
| Incident response (restore from dump) | Rare | 1–4 h |

**Total routine:** ~**1–2 hours/month** excluding feature development.

### Phase 5 readiness

This report **does not** start Phase 5. Before cutover, operator should:

1. Create DO Droplet (`gru1`, 4 GB) and apply firewall rules  
2. Register `melomanos.cl` and point NS to Cloudflare  
3. Configure Vercel project + env vars  
4. Provision B2 bucket + rclone on VPS  
5. Configure UptimeRobot monitors  
6. Execute [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md) checklist  

Update [`PRODUCTION_DEPLOYMENT_PLAN.md`](PRODUCTION_DEPLOYMENT_PLAN.md) provider table to reference this document when Phase 5 begins.

---

## Appendix — Decision log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-17 | DigitalOcean GRU 4 GB | Chile latency + solo ops |
| 2026-06-17 | Cloudflare DNS | Free, flexible apex + api split |
| 2026-06-17 | UptimeRobot free | Sufficient MVP external checks |
| 2026-06-17 | pg_dump + B2 | Cheapest reliable off-VPS recovery |
| 2026-06-17 | Hetzner CPX22 noted as budget alt | ~$17/mo savings, higher latency |

---

*Document only — no infrastructure provisioned. Roadmap not advanced.*
