# Preview Deployment Plan — Daniela UX Review

**Date:** 2026-06-17  
**Audience:** Daniela (hosting/design, UX review), Ernesto (operator)  
**Status:** Planning document — **no infrastructure deployed**

**This is NOT:**

- Production cutover ([`PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md`](PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md))
- Closed Beta launch
- Public marketing or SEO launch
- A permanent staging environment (preview may be torn down after review)

**Production architecture (unchanged for later):** Vercel + DigitalOcean VPS + PostgreSQL + Caddy + Cloudflare → `melomanos.cl` / `api.melomanos.cl`.

**Companion docs:** [`PRODUCTION_DEPLOYMENT_DECISION_REPORT.md`](PRODUCTION_DEPLOYMENT_DECISION_REPORT.md), [`PRODUCTION_ENV_MATRIX.md`](PRODUCTION_ENV_MATRIX.md), [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md)

---

## 1. Purpose

### Why this exists

Daniela owns **hosting/design and UX review** but **cannot access localhost**. She needs a **temporary, internet-reachable** Melómanos instance to evaluate:

- Visual design, layout, and brand feel on real devices
- Navigation, copy, and Chilean-market UX (Spanish UI)
- Core buyer/seller flows without installing dev tools

### What this preview is

| Is | Is not |
|----|--------|
| Private-ish preview for **one reviewer + operator** | Public launch |
| **Disposable** stack and database | Production database |
| **Simulated payments only** | Real money / Transbank live |
| **Seed + test accounts** | Real user data |
| Practice run for **same architecture** as production | Final DNS on apex domain |

### Success criteria

- Daniela can open a URL from home/mobile and complete review flows in **< 30 min** without Ernesto on a call
- No production secrets, no real payments, no indexable marketing site
- Feedback captured in structured form (see §9 **DANIELA_UX_REVIEW_BRIEF**)
- Preview can be **destroyed** after review without affecting production plans

---

## 2. Recommended preview architecture

### Options compared

| Criterion | **A. Vercel preview + temp VPS + preview DB** | B. Vercel + local tunnel (ngrok/Cloudflare Tunnel) | C. Full production stack early |
|-----------|-----------------------------------------------|------------------------------------------------------|--------------------------------|
| **Daniela access** | ✅ Stable HTTPS URLs | ⚠️ URL changes / tunnel drops | ✅ Stable URLs |
| **Mirrors prod stack** | ✅ Same Vercel + Docker + Caddy pattern | ❌ Backend unlike prod | ✅ Identical |
| **Safety (isolation)** | ✅ Separate DB + env | ✅ Local DB only | ❌ Risk to prod data/DNS |
| **Ops burden** | Medium (one-time setup) | Low start, high babysitting | High; premature |
| **Cost** | ~$12–24/mo while active | ~$0–20/mo | Production cost + mistakes |
| **Uptime for async review** | ✅ Good | ❌ Poor (PC must stay on) | ✅ Good |
| **Teardown** | ✅ Drop preview droplet / Vercel env | ✅ Stop tunnel | ❌ Hard to unwind |

### **Recommendation: Option A**

**Vercel Preview deployment (frontend) + temporary DigitalOcean VPS (backend) + isolated preview PostgreSQL.**

Rationale:

1. **Daniela needs reliability** — she reviews on her schedule; tunnels tied to Ernesto’s laptop fail that.
2. **Same shape as production** — surfaces real CORS, TLS, and latency issues without cutting over `melomanos.cl`.
3. **Safe isolation** — preview DB and secrets are separate; production Phase 5 checklist stays untouched.
4. **Cheaper than full prod** — can use **same DO region (`gru1`)** with a **smaller Droplet** or a **second compose project** on one VM only if cost-sensitive (prefer **separate preview DB volume** either way).

### Suggested preview URLs (pick one naming scheme)

| Layer | Recommended URL | DNS |
|-------|-----------------|-----|
| Frontend | `https://preview.melomanos.cl` | Cloudflare → Vercel (Preview env or dedicated Vercel project) |
| API | `https://api-preview.melomanos.cl` | Cloudflare → Preview VPS (**grey cloud**, Caddy TLS) |

**If `melomanos.cl` is not registered yet:** use Vercel default `*.vercel.app` for frontend + `api-preview.<operator-domain>` or DO floating IP with self-signed avoided via Caddy on a throwaway subdomain.

### Preview topology

```
Daniela (browser)
    │
    ├─► preview.melomanos.cl ──► Vercel (Preview / dedicated project)
    │
    └─► api-preview.melomanos.cl ──► DO VPS (gru1) ──► Caddy ──► FastAPI
                                              │
                                              └─► PostgreSQL 15 (preview volume only)
```

**Lifetime:** Provision for **2–4 weeks** of UX review, then snapshot or delete.

---

## 3. Access control

Preview is **not secret security** — treat as **obscure + low exposure**, not authentication-hardened staging.

| Control | Implementation |
|---------|----------------|
| **Obscure URLs** | Use `preview.` / `api-preview.` subdomains; **do not** link from social, homepage, or search-indexed pages |
| **No indexing** | `robots.txt` disallow all on preview frontend; optional `<meta name="robots" content="noindex,nofollow">` |
| **Vercel Deployment Protection** | If available on plan: password-protect preview deployments (extra layer) |
| **Test users only** | No open registration marketing; optional disable public register later — for UX review, **seed accounts** suffice |
| **Seed data only** | Chilean-flavored fake listings; no PII of real people |
| **No real payments** | `PAYMENT_PROVIDER_MODE=simulate` (**recommended**). Use `webpay_placeholder` only if Daniela must see WebPay UI copy (still no real money) |
| **Admin** | `ADMIN_KEY` **not shared** with Daniela unless admin UI review is in scope; if needed, share via password manager, one-time |
| **Cloudflare** | Optional IP allowlist for `api-preview` (Daniela + Ernesto IPs) — only if static IPs known |
| **Rate limit** | Optional Caddy or Cloudflare basic rate limit on preview API |

**Share via:** private message (Signal/WhatsApp/email) — not public docs with live passwords.

---

## 4. Environment variables

Use **separate** preview secrets (generate new `SECRET_KEY`, `ADMIN_KEY`, DB password). Never reuse production values.

### Frontend (Vercel — Preview environment or dedicated preview project)

| Variable | Preview value | Notes |
|----------|---------------|-------|
| `NEXT_PUBLIC_API_URL` | `https://api-preview.melomanos.cl` | Must match preview API |
| `NEXT_PUBLIC_PAYMENT_PROVIDER_MODE` | `simulate` | Or `webpay_placeholder` for UI-only WebPay screens |

### Backend (VPS — `.env.preview` or `.env.production` on preview host only)

| Variable | Preview value | Notes |
|----------|---------------|-------|
| `DATABASE_URL` | `postgresql+psycopg2://melomanos:PREVIEW_PASSWORD@db:5432/melomanos_preview` | **Separate DB name** |
| `POSTGRES_USER` | `melomanos` | |
| `POSTGRES_DB` | `melomanos_preview` | Not `melomanos` prod name |
| `POSTGRES_PASSWORD` | Strong random | Preview-only |
| `SECRET_KEY` | Strong random | Preview-only |
| `ALGORITHM` | `HS256` | |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | |
| `ADMIN_KEY` | Strong random | Operator only |
| `CORS_ORIGINS` | `https://preview.melomanos.cl` | Add Vercel preview URL if using `*.vercel.app` |
| `PAYMENT_PROVIDER_MODE` | **`simulate`** | No live WebPay |
| `WEBPAY_CALLBACK_SECRET` | Optional dummy | Only if testing placeholder webhook |
| `WEBPAY_RETURN_URL_BASE` | `https://preview.melomanos.cl/orders` | |
| `ACME_EMAIL` | Operator email | Caddy Let's Encrypt |
| `OPENAI_NL_SEARCH_ENABLED` | `false` | Avoid preview API cost |

### Database

| Item | Preview |
|------|---------|
| Engine | PostgreSQL 15 (Docker) |
| Volume | **Dedicated** `postgres_preview_data` volume |
| Migrations | `alembic upgrade head` on empty preview DB |
| Data | Seed script / manual seed after migrate |

### CORS note

If Vercel serves frontend at both `preview.melomanos.cl` and a `*.vercel.app` alias, set:

```
CORS_ORIGINS=https://preview.melomanos.cl,https://<project>.vercel.app
```

---

## 5. Seed data / test users

Align with existing E2E conventions where useful ([`frontend/e2e/helpers/constants.ts`](../frontend/e2e/helpers/constants.ts)).

### Recommended accounts

| Role | Email | Password | Purpose |
|------|-------|----------|---------|
| **Buyer** | `buyer@example.com` | `devpassword12` | Browse, buy, favorites, messages |
| **Seller** | `seller@example.com` | `devpassword12` | List vinyl, shipping profile, orders |
| **Daniela reviewer** | `daniela.review@melomanos.cl` | *(unique strong password — share privately)* | Her primary login; buyer+seller views |
| **Admin** | — | — | Operator only via `ADMIN_KEY` + `/admin` (not for Daniela unless requested) |

### Seed content (minimum)

| Data | Count | Notes |
|------|-------|-------|
| Listings | 8–15 | Mix new/used, genres, price ranges CLP, Santiago/other cities |
| Orders | 2–3 | One pending, one completed path for seller/buyer tabs |
| Messages | 1 thread | Buyer → seller on a listing |
| Notifications | Few | So bell UI is visible for seller |
| Reviews / reputation | Optional | 1–2 for trust badges |

**Script approach (Phase 4):** extend E2E setup patterns or one-off `seed_preview.py` — **not implemented in this doc**.

---

## 6. Daniela review workflow

### Before she starts (Ernesto)

1. Confirm preview URLs load (frontend + `/health` on API).
2. Send **DANIELA_UX_REVIEW_BRIEF** (§9) + credentials via private channel.
3. Confirm payments are **simulate** — no card charges.

### Daniela — session flow

| Step | Action |
|------|--------|
| 1 | Open **`https://preview.melomanos.cl`** (or agreed URL) on desktop + phone |
| 2 | Log in as **`daniela.review@melomanos.cl`** (or buyer/seller accounts for role-specific flows) |
| 3 | Walk through **§9 test flows** |
| 4 | Fill feedback template (Google Doc / Notion / markdown — operator provides link) |
| 5 | Optional: screenshots + short screen recordings for layout bugs |

### Flows to test (priority order)

1. **First impression** — homepage, branding, trust, Spanish copy
2. **Browse & search** — listings grid, filters, listing detail
3. **Buyer** — login, favorite, message seller, create order, simulate payment
4. **Seller** — sell flow, used listing + video requirement, shipping profile
5. **Orders** — buying/selling tabs, order detail, status labels
6. **Messages & notifications** — bell, `/notifications`, `/messages`
7. **Profile** — subscription card, Digging Score, reputation
8. **Mobile** — repeat key flows on phone viewport
9. **Admin** *(optional)* — only if Ernesto enables and shares access

### Feedback to capture

- Confusing labels or steps (Spanish copy)
- Visual hierarchy / spacing / typography
- Missing trust signals for Chilean buyers
- Broken or awkward flows (with URL + steps)
- **Not in scope:** backend bugs unless they block UX; file as separate tech debt

---

## 7. Safety checklist

Complete before sharing URL with Daniela.

| # | Rule | Done |
|---|------|:----:|
| 1 | **No production DB** — preview uses `melomanos_preview` or separate volume | [ ] |
| 2 | **No production secrets** — all keys regenerated for preview | [ ] |
| 3 | **No real payments** — `PAYMENT_PROVIDER_MODE=simulate` (or placeholder only) | [ ] |
| 4 | **No real users** — seed data only; no imported prod dumps | [ ] |
| 5 | **No public marketing** — no posts, ads, or SEO for preview URL | [ ] |
| 6 | **No index** — robots noindex on preview frontend | [ ] |
| 7 | **ADMIN_KEY** not in frontend env or chat logs | [ ] |
| 8 | **Teardown date** agreed (e.g. +14 days after review) | [ ] |
| 9 | Preview **not** wired to `melomanos.cl` apex or production API | [ ] |
| 10 | Quality Gate passed on commit deployed to preview (operator) | [ ] |

---

## 8. Implementation phases

**Do not start until Ernesto explicitly approves Option A.** No roadmap advance.

| Phase | Title | Scope | Owner | Status |
|-------|-------|-------|-------|--------|
| **1** | Preview deployment decisions | Lock URLs, Option A, access model, teardown date | Ernesto + Daniela | TODO |
| **2** | Deploy preview backend | DO Droplet (or preview compose), Caddy, `.env.preview`, migrate | Ernesto | TODO |
| **3** | Deploy preview frontend | Vercel preview project/env, `NEXT_PUBLIC_API_URL`, DNS `preview.` | Ernesto | TODO |
| **4** | Seed data & reviewer access | Migrations, seed listings, Daniela account, smoke test | Ernesto | TODO |
| **5** | Daniela UX audit | Daniela runs §9 brief; feedback delivered | Daniela | TODO |

### Phase 1 deliverables

- [ ] Preview URLs chosen (`preview.` + `api-preview.`)
- [ ] Daniela review window dates
- [ ] Payment mode: `simulate` confirmed
- [ ] Feedback channel (Doc/Notion/issue list)

### Phase 2–4 (operator reference — not executed now)

Reuse [`backend/docker-compose.prod.yml`](../backend/docker-compose.prod.yml) pattern with preview env file and **separate** DB volume. Commands mirror [`backend/README_DEPLOYMENT.md`](../backend/README_DEPLOYMENT.md) with preview hostnames in Caddyfile.

### Phase 5 exit

- Daniela submits completed **DANIELA_UX_REVIEW_BRIEF**
- Ernesto triages UX items into backlog
- Preview stack **scheduled for teardown** or kept frozen until Closed Beta prep

---

## 9. Deliverable for Daniela

Copy the section below into a shared doc or email when preview is live.

---

# DANIELA_UX_REVIEW_BRIEF

**Project:** Melómanos — marketplace de vinilos (Chile)  
**Preview URL:** `https://preview.melomanos.cl` *(replace when live)*  
**Review window:** _______________  
**Contact:** Ernesto — _______________

### Important

- This is a **private preview**, not the public site.
- **No real money** — payments are simulated.
- Use **test accounts** only; data is fake seed content.
- You may use **desktop and mobile**.

### Your login

| Field | Value |
|-------|-------|
| Email | `daniela.review@melomanos.cl` *(or as sent privately)* |
| Password | *(sent separately)* |

**Other test accounts** (same password if operator confirms):

| Role | Email |
|------|-------|
| Buyer | `buyer@example.com` |
| Seller | `seller@example.com` |

---

### What to test

Please spend **45–90 minutes** total. Mark each **Pass / Fail / Notes**.

#### A. First impression (10 min)

- [ ] Homepage feels trustworthy for buying vinyl in Chile
- [ ] Brand, colors, typography match Melómanos vision
- [ ] Spanish copy reads naturally (not machine-translated feel)
- [ ] Navigation is obvious (browse, sell, login, profile)

#### B. Browse & discovery (10 min)

- [ ] Listing grid is easy to scan (cover, price CLP, condition)
- [ ] Listing detail page answers: what, who sells, how much, condition
- [ ] Seller card / reputation visible where expected

#### C. Buyer journey (15 min)

Log in as **buyer** (or your reviewer account).

- [ ] Login / logout smooth
- [ ] Add favorite; find it again in Favorites
- [ ] Send a message to seller (safe question — no phone/email in text)
- [ ] Start purchase / order flow
- [ ] Complete **simulated** payment (no real card)
- [ ] Find order under Orders → Buying

#### D. Seller journey (15 min)

Log in as **seller**.

- [ ] Open Sell / publish listing (new vinyl)
- [ ] Try **used** listing — video URL requirement clear?
- [ ] Shipping profile understandable
- [ ] See order in Orders → Selling

#### E. Messages & notifications (10 min)

- [ ] Messages page layout
- [ ] Notification bell — unread count, dropdown, mark read
- [ ] `/notifications` page

#### F. Profile & trust (5 min)

- [ ] Profile / subscription / Digging Score presentation
- [ ] Anything missing for buyer confidence?

#### G. Mobile (15 min)

Repeat **B + C** on phone (or narrow browser).

- [ ] Tap targets, menus, forms usable
- [ ] No horizontal scroll / clipped text

---

### Questions to answer (short prose)

1. **First 10 seconds:** What do you think this site sells, and to whom?
2. **Trust:** Would you feel safe buying a used record here? What would increase trust?
3. **Clarity:** What was the most confusing step? Where did you hesitate?
4. **Visual design:** What feels strongest? What feels unfinished or off-brand?
5. **Chile context:** Price in CLP, shipping, Spanish tone — anything wrong for local users?
6. **Priority fixes:** List your **top 5** UX changes before Closed Beta (ordered).

---

### How to report feedback

| Method | Details |
|--------|---------|
| **Preferred** | Fill this brief + numbered list in shared doc: _______________ |
| **Bugs blocking UX** | Step to reproduce + URL + screenshot |
| **Nice-to-have** | Label as *polish* vs *must-fix* |
| **Screenshots / video** | Optional; attach to doc or shared folder |

**Do not** post preview URL or passwords on public channels.

---

### Out of scope for this review

- Real WebPay / bank payments
- Legal/compliance copy final sign-off
- Performance load testing
- Admin dispute resolution (unless Ernesto asks)

---

*End of DANIELA_UX_REVIEW_BRIEF*

---

## Cost estimate (preview only)

| Item | While active (~2–4 weeks) |
|------|---------------------------|
| DO Droplet 2 GB–4 GB `gru1` | ~$12–24/mo |
| Vercel | $0 (Hobby preview) |
| Cloudflare DNS | $0 |
| **Total** | **~$12–24/mo** prorated |

Teardown eliminates ongoing cost.

---

## Related documents

| Doc | Use |
|-----|-----|
| [`PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md`](PRODUCTION_DEPLOYMENT_PHASE5_CHECKLIST.md) | Real launch — **after** preview feedback |
| [`PRODUCTION_DEPLOYMENT_DECISION_REPORT.md`](PRODUCTION_DEPLOYMENT_DECISION_REPORT.md) | Locked prod stack |
| [`frontend/e2e/`](../frontend/e2e/) | Reference flows for seed/smoke |

---

*Planning only — no infrastructure provisioned. Roadmap not advanced.*
