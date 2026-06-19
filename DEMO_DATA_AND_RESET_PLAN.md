# Demo Data & Factory Reset Plan — Melómanos

**Date:** 2026-06-17  
**Status:** Design document — **no implementation yet**  
**Scope:** Electronic-music-only vinyl marketplace demo/seed/reset tooling

**Context:** Melómanos needs repeatable, safe demo data for **Daniela UX review** ([`PREVIEW_DEPLOYMENT_PLAN.md`](PREVIEW_DEPLOYMENT_PLAN.md)), local development, and future demos — without touching production data.

**Rules for this effort:**

- Do **not** implement code in this step
- Do **not** modify roadmap or milestones
- Do **not** run against production databases

**Companion docs:** [`PREVIEW_DEPLOYMENT_PLAN.md`](PREVIEW_DEPLOYMENT_PLAN.md), [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md), [`backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md)

---

## Executive summary

Introduce a **`backend/scripts/demo_data.py`** CLI that:

1. **Seeds** deterministic, **electronic-music-only** marketplace data at three sizes (small / medium / large)
2. **Resets** to factory-empty state (migrations kept, demo rows removed)
3. **Creates** individual test users (buyer, seller) and documents **admin** access (`ADMIN_KEY`, not a DB role today)
4. **Blocks** destructive operations in production unless explicit multi-step dangerous confirmation

Cover art uses **local fictional assets** under `backend/demo_assets/covers/` — no scraped or copyrighted album art.

---

## 1. Use cases

| # | Use case | Actor | Command / flow |
|---|----------|-------|----------------|
| U1 | Seed demo marketplace for Daniela UX review | Operator | `seed --size medium` on **preview** DB |
| U2 | Reset DB to factory-empty | Developer | `reset --factory` (local/preview only) |
| U3 | Create manual test buyer | Developer | `create-user --role buyer` |
| U4 | Create manual test seller | Developer | `create-user --role seller` (+ optional shipping/payout profile) |
| U5 | Admin access for dispute panel | Operator | Configure `ADMIN_KEY`; optional seed user for login context only |
| U6 | Re-seed during development | Developer | `reset --factory` → `seed --size small` |
| U7 | Avoid accidental production reset | System | Environment guard + typed confirmation + URL/host checks |

### User journey: Daniela preview (medium seed)

```
Operator: preview VPS + migrate
    → demo_data.py seed --size medium
    → share preview URL + daniela.review@ account
Daniela: UX review (no reset needed)
Operator: teardown preview OR reset --factory before next seed
```

### User journey: local dev loop

```
Developer: docker compose up db
    → alembic upgrade head
    → demo_data.py seed --size small
    … work …
    → demo_data.py reset --factory
    → demo_data.py seed --size small
```

---

## 2. Data strategy

All seeded entities are **synthetic** and **marked** (see §6) so reset can target demo rows reliably.

### Entity coverage

| Entity | Seed in | Notes |
|--------|---------|-------|
| **Users** | Phase 1–2 | Buyers, sellers, Daniela reviewer; `@example.com` or `@demo.melomanos.local` emails |
| **Sellers** | Phase 2 | Subset of users with listings + shipping profile |
| **Buyers** | Phase 2 | Subset with favorites, orders, messages |
| **Listings** | Phase 2 | Electronic genres only; mix `new` / `used` (used require `video_url` placeholder) |
| **Messages** | Phase 3 | Safe collector questions; no contact leaks |
| **Orders** | Phase 3 | Multiple statuses for UI tabs |
| **Reviews** | Phase 3 | Post-completion reviews for reputation UI |
| **Disputes** | Phase 3 | 1 open + 1 resolved (admin UI) |
| **Notifications** | Phase 3 | Bell/dropdown/page coverage |
| **Subscriptions / plans** | Phase 2 | `free`, `pack`, `pro` on different sellers |
| **Seller shipping profiles** | Phase 2 | Chile couriers (Starken, Chilexpress, etc.) |
| **Seller payout profiles** | Phase 2 | Placeholder bank fields (fake RUT/account) |

### Deterministic naming

| Pattern | Example |
|---------|---------|
| Demo email domain | `@demo.melomanos.local` or `@example.com` (E2E-aligned) |
| Demo user prefix | `demo_buyer_01`, `demo_seller_03` |
| Listing title prefix | `[Demo] …` optional in logs; fictional artist/title in UI |
| Metadata flag | `users.email LIKE '%@demo.melomanos.local'` OR dedicated `demo_seed_batch_id` column (Phase 4 optional) |

**Preferred MVP marker:** deterministic email domain `@demo.melomanos.local` + documented seed user list in `README_DEMO_DATA.md`. Avoid schema change in Phase 1 unless reset proves ambiguous.

### Implementation approach

- **Phase 1–2:** Use existing **services/API internals** (same validation as production) where possible — not raw SQL inserts that bypass business rules
- **Phase 3:** Orchestrated scenarios (order lifecycle, dispute) via service layer
- **Idempotent seed (stretch):** `seed --size X` after `reset --factory` is clean; re-run without reset may duplicate — document **always reset first** until idempotent design lands

### Cover images (listings)

Current `VinylListing` model has no `cover_image_url` field. Plan options (pick at implementation):

| Option | Description |
|--------|-------------|
| **A (recommended)** | Add optional `cover_image_url` on listing OR link `release_id` to seeded `vinyl_releases.cover_image_url` |
| **B** | Frontend-only placeholder by genre until backend field exists |
| **C** | Static demo CDN path in description (not ideal) |

**Recommendation:** Option A via `release_id` + seeded releases, or nullable `cover_image_url` on listing — implement in Phase 2 with URLs pointing to served demo assets.

---

## 3. Electronic-only content

**Genre policy:** All seeded listings must use **`genre = "Electronic"`** (or app convention) with **subgenre** from approved list only.

### Approved subgenres (seed pool)

House, Deep House, Microhouse, Minimal, Techno, Dub Techno, Electro, Ambient, IDM, Breakbeat, Drum & Bass, Acid, Trance, Experimental

### Forbidden in seed data

Rock, Jazz, Pop, Reggaeton, Metal, Hip-Hop, Latin pop, Soundtrack compilations marketed as non-electronic, etc.

### Fictional catalog rules

| Field | Rule |
|-------|------|
| **Artist** | Fictional names — e.g. "Lumen Arc", "Subfloor Unit", "Patagonia Drift" |
| **Title** | Fictional — e.g. "Modular Dawn EP", "Greyscale Transit" |
| **Label** | Fictional — e.g. "Melómanos Test Press", "Andes Rhythm Co." |
| **Year** | 1995–2024 weighted toward 2010–2020 |
| **City** | Chilean cities — Santiago, Valparaíso, Concepción, La Serena |
| **Price** | CLP 8,000–85,000; respect `price_clp >= 1000` |
| **Condition** | Discogs grades M–G mix |
| **Used listings** | ~25% of medium/large; `video_url` = stable public test URL (e.g. operator-hosted sample or `https://example.com/demo-video.mp4`) |

### Validation

Seed module exports `ALLOWED_SUBGENRES` frozenset; seed + tests reject anything outside list.

---

## 4. Demo images / cover art strategy

### Principles

| Rule | Detail |
|------|--------|
| No scraping | Never fetch Discogs/Spotify/Beatport art |
| No copyrighted art | No real album covers |
| Synthetic / owned | Generate or commission abstract genre art; store in repo |
| Fictional mapping | `house_01.jpg` ≠ claiming to be a real release |
| Fallback | `default_vinyl.jpg` when mapping missing |

### Directory layout

```
backend/demo_assets/covers/
  house_01.jpg
  house_02.jpg
  deep_house_01.jpg
  techno_01.jpg
  dub_techno_01.jpg
  minimal_01.jpg
  microhouse_01.jpg
  electro_01.jpg
  ambient_01.jpg
  idm_01.jpg
  breakbeat_01.jpg
  dnb_01.jpg
  acid_01.jpg
  trance_01.jpg
  experimental_01.jpg
  default_vinyl.jpg
  … (target 20–40 files total)
```

### Image creation (pre-implementation)

1. **Abstract SVG/PNG** — gradient + geometric patterns per subgenre (script-generated, committed to repo)
2. **Simple AI-generated abstract art** — operator-reviewed, license-safe, no artist/album names
3. **Uniform dimensions** — e.g. 600×600 JPEG, < 80 KB each

### Serving URLs

| Environment | URL pattern |
|-------------|-------------|
| Local | `http://127.0.0.1:8000/static/demo/covers/{filename}` (FastAPI StaticFiles mount) |
| Preview | `https://api-preview.melomanos.cl/static/demo/covers/{filename}` |
| Production | **Do not mount demo static** on production API (guard: only if `DEMO_ASSETS_ENABLED=true`) |

### Assignment algorithm

```
cover = covers[(hash(listing_id + subgenre) % len(subgenre_covers))]
else default_vinyl.jpg
```

---

## 5. Dataset sizes

### Small — quick local testing

| Entity | Count |
|--------|-------|
| Users | 4 (2 sellers, 2 buyers) |
| Listings | 8 |
| Orders | 2 |
| Messages | 2 |
| Reviews | 1 |
| Disputes | 0 |
| Notifications | 4 |
| Shipping profiles | 2 |
| Payout profiles | 1 |

**Time target:** seed < 10 s

### Medium — Daniela UX review

| Entity | Count |
|--------|-------|
| Users | 12 (5 sellers, 5 buyers, 1 Daniela reviewer, 1 extra) |
| Listings | 24 |
| Orders | 8 (status mix) |
| Messages | 6 |
| Reviews | 5 |
| Disputes | 2 (1 open, 1 resolved) |
| Notifications | 15 |
| Shipping profiles | 5 |
| Payout profiles | 3 |
| Plans | free ×2, pack ×2, pro ×1 sellers |

**Time target:** seed < 30 s

### Large — browsing / stress demo

| Entity | Count |
|--------|-------|
| Users | 40 |
| Listings | 120 |
| Orders | 30 |
| Messages | 25 |
| Reviews | 20 |
| Disputes | 5 |
| Notifications | 50 |
| Shipping profiles | 15 |
| Payout profiles | 10 |

**Time target:** seed < 2 min

---

## 6. Safety model

### Environment guard layers

| Layer | Check |
|-------|-------|
| **L1 — Env flag** | `MELOMANOS_DEMO_MODE=1` required for seed/reset (or `APP_ENV` in `local`, `preview`, `development`) |
| **L2 — Database URL** | Block if host matches production patterns (configurable denylist) |
| **L3 — Explicit prod flag** | `DATABASE_URL` contains `melomanos_prod` or production host → **hard block** unless `--i-know-this-is-production` |
| **L4 — Typed confirmation** | `reset --factory` requires typing `RESET DEMO DATA` |
| **L5 — Dangerous prod reset** | If L3 overridden, require typing full string: `DELETE ALL DATA ON PRODUCTION` |

### Production block (default)

```
❌ reset --factory on production → EXIT 1
❌ seed without MELOMANOS_DEMO_MODE on production → EXIT 1
```

### Backup reminder

Before `reset --factory`, print:

```
⚠️  Destructive operation. All application data will be deleted.
    Migrations will remain applied.
    Recommended: pg_dump backup first (see DEPLOYMENT_RUNBOOK §6)
```

Optional `--force` skips interactive confirm on local only (never production).

### Demo markers & logs

- Log: `[demo_data] environment=local size=medium batch=demo-2026-06-17`
- Log counts: users created, listings created, etc.
- Warn if seed run against non-empty DB without `--force`

### Admin model (current codebase)

There is **no `is_admin` user column**. Admin panel uses **`ADMIN_KEY`** header ([`app/dependencies/admin.py`](../backend/app/dependencies/admin.py)).

| Command | Behavior |
|---------|----------|
| `create-admin` | Print reminder to set `ADMIN_KEY`; optionally create `demo_admin@demo.melomanos.local` user for login only — admin API still needs header |

---

## 7. Commands proposal

**Entry point:** `backend/scripts/demo_data.py` (invoke as `py scripts/demo_data.py …` from `backend/`)

```bash
# Seed datasets
py scripts/demo_data.py seed --size small
py scripts/demo_data.py seed --size medium
py scripts/demo_data.py seed --size large

# Factory reset (destructive)
py scripts/demo_data.py reset --factory
py scripts/demo_data.py reset --factory --force          # local only, skip confirm

# Individual users
py scripts/demo_data.py create-user --role buyer  [--email ...] [--password ...] [--name ...]
py scripts/demo_data.py create-user --role seller [--email ...] [--password ...] [--name ...] [--plan free|pack|pro]
py scripts/demo_data.py create-admin              # ADMIN_KEY guidance + optional demo user

# Help / status
py scripts/demo_data.py status                    # show env, demo mode, row counts (optional Phase 4)
py scripts/demo_data.py --help
```

### Flags (cross-cutting)

| Flag | Purpose |
|------|---------|
| `--dry-run` | Print plan, no writes |
| `--force` | Seed on non-empty DB / skip local confirm (never prod) |
| `--batch-id` | Tag seed run for future selective delete |

### Docker preview usage

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec api \
  py scripts/demo_data.py seed --size medium
```

Requires `MELOMANOS_DEMO_MODE=1` in preview `.env`.

---

## 8. Factory reset definition

### What factory reset does

| Action | Yes/No |
|--------|--------|
| Alembic migrations remain at `head` | ✅ Yes |
| All application rows removed | ✅ Yes (ordered FK-safe deletes) |
| Demo + non-demo data removed | ✅ Yes — **full wipe** (factory = empty marketplace) |
| Schema / tables remain | ✅ Yes |
| Optional admin user recreated | ⚙️ `--recreate-admin-user` flag (optional) |
| Demo assets on disk (`demo_assets/`) | ✅ Untouched (files, not DB) |
| Docker volumes | ⚠️ Optional `reset --factory --drop-volume` for dev only (document separately) |

### Delete order (respect FKs)

```
dispute_evidence → order_disputes → payment_events → checkout_sessions
→ notifications → reviews → messages → favorites → orders
→ vinyl_listings → seller_payout_profiles → seller_shipping_profiles
→ users
```

(Adjust to match actual model graph at implementation time.)

### After reset

- Table counts ≈ 0 (except `alembic_version`)
- `seed` can repopulate
- **No demo data** until next seed

### Production

**Blocked by default.** Factory reset on production requires impossible-by-default flags; operator should use **restore from backup** instead ([`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md)).

---

## 9. Implementation phases

| Phase | Scope | Deliverables |
|-------|-------|--------------|
| **1** | CLI skeleton + safety guards + `create-user` | `demo_data.py`, env guards, buyer/seller creation, `README_DEMO_DATA.md` draft |
| **2** | Seed users/listings + electronic metadata + images | Subgenre pool, fictional catalog, `demo_assets/covers/`, static mount, medium size partial |
| **3** | Seed orders/messages/reviews/disputes/notifications | Full medium dataset; small/large sizes |
| **4** | Factory reset + docs + tests | `reset --factory`, FK-safe wipe, pytest suite, runbook/preview cross-links |

### Phase dependencies

```
Phase 1 (safety + users)
    → Phase 2 (listings + covers)
        → Phase 3 (transactions + social)
            → Phase 4 (reset + tests)
```

### Out of scope (later)

- Idempotent incremental seed without reset
- Web UI admin "reset demo"
- Import from CSV
- Real Discogs metadata

---

## 10. Testing plan

Add `backend/tests/test_demo_data.py` (and helpers) — run against SQLite test DB only.

| Test | Assert |
|------|--------|
| `test_create_user_buyer` | User exists, can login, no listings |
| `test_create_user_seller` | User + empty shipping profile optional |
| `test_seed_small_creates_listings` | Count ≥ 8 listings |
| `test_seed_electronic_only` | All listings `genre` electronic; subgenre in allowlist |
| `test_seed_cover_urls_or_fallback` | Every listing has URL or release cover; fallback used when unmapped |
| `test_seed_used_listings_have_video` | Used type → non-empty `video_url` |
| `test_reset_factory_clears_data` | seed → reset → user/listing count 0 |
| `test_reset_preserves_migrations` | `alembic_version` still at head |
| `test_production_guard_blocks_reset` | Simulated prod `DATABASE_URL` → exit non-zero |
| `test_production_guard_blocks_seed_without_demo_mode` | Same |
| `test_typed_confirmation_required` | Mock stdin without phrase → abort |

**CI:** Include demo tests in standard `py -m pytest`; no separate Postgres required if SQLite-compatible.

---

## 11. Documentation plan

| Document | Action |
|----------|--------|
| **`backend/README_DEMO_DATA.md`** | **Create** — commands, sizes, safety, electronic-only policy, cover assets |
| [`DEPLOYMENT_RUNBOOK.md`](DEPLOYMENT_RUNBOOK.md) | Add note: **never** run demo reset on production; preview seed in Phase 4 of preview plan |
| [`PREVIEW_DEPLOYMENT_PLAN.md`](PREVIEW_DEPLOYMENT_PLAN.md) | Link to demo seed `--size medium` for Phase 4 seed step |
| [`backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md) | Mention demo_data test module after Phase 4 |
| [`backend/.env.example`](../backend/.env.example) | Document `MELOMANOS_DEMO_MODE` (when implemented) |

### README_DEMO_DATA.md outline (to create in Phase 1)

1. Purpose & safety warning
2. Prerequisites (`alembic upgrade head`, `MELOMANOS_DEMO_MODE`)
3. Command reference
4. Dataset sizes table
5. Default accounts (Daniela, buyer, seller)
6. Electronic-only policy
7. Cover assets licensing note
8. Troubleshooting

---

## Safety concerns (design review)

| Risk | Mitigation |
|------|------------|
| Accidental production wipe | Multi-layer guard + typed confirmation + denylist hosts |
| Copyright on cover art | Only repo-owned abstract art; legal review before commit |
| PII in demo data | Fictional names/emails only; no real RUT/bank numbers that match real people |
| Leaked demo passwords | Document `@example.com` / preview-only passwords; rotate on preview |
| Seed bypassing business rules | Use services, not raw SQL |
| `reset --factory` on preview with wrong URL | Denylist + require `MELOMANOS_DEMO_MODE=1` on preview VPS |
| Used listing video URL dead link | Host stable sample or document placeholder URL |
| Admin confusion (`create-admin`) | Clarify ADMIN_KEY vs user account |
| Non-idempotent re-seed | Document "reset then seed"; detect non-empty DB warning |
| Static demo files on prod API | `DEMO_ASSETS_ENABLED` false in production |

---

## Recommended first implementation phase

**Phase 1 — CLI + safety guards + create-user**

Why first:

- Unblocks manual testing and Daniela account creation **without** seed complexity
- Safety guards must exist **before** any destructive or bulk write command
- Small, testable surface (`test_create_user_*`, `test_production_guard_*`)

Phase 1 deliverables checklist:

- [ ] `scripts/demo_data.py` argparse skeleton
- [ ] `MELOMANOS_DEMO_MODE` / environment detection module
- [ ] `create-user --role buyer|seller`
- [ ] `create-admin` (document ADMIN_KEY)
- [ ] Production denylist + exit codes
- [ ] Draft `README_DEMO_DATA.md`

---

## Appendix — Default accounts (medium seed)

| Role | Email | Password | Notes |
|------|-------|----------|-------|
| Daniela reviewer | `daniela.review@demo.melomanos.local` | Generated; share privately | Primary UX account |
| Buyer | `buyer@example.com` | `devpassword12` | E2E-aligned |
| Seller | `seller@example.com` | `devpassword12` | E2E-aligned; pro plan optional |
| Extra seller | `demo_seller_02@demo.melomanos.local` | `demo-password-change-me` | Pack plan + shipping |

*(Passwords are placeholders in plan — use strong values on preview.)*

---

*Design only — no code, no data changes, roadmap not advanced.*
