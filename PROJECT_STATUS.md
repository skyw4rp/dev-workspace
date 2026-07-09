# Melómanos Market — Project Status

Living snapshot for product and quality status. Updated manually or via `py finish_task.py` after a successful release.

<!-- STATUS:LAST_QUALITY_GATE_START -->
## Last Quality Gate

- Date: 2026-06-30 23:15
- Backend tests: PASSED
- Frontend build: PASSED
- E2E tests: PASSED
- Full audit: PASSED
<!-- STATUS:LAST_QUALITY_GATE_END -->

<!-- STATUS:LATEST_RELEASE_START -->
## Latest Release

- Backend: Add production deployment backend
- Frontend: Add dispute resolution frontend
- Quality Gate: PASSED
- Date: 2026-06-30 23:15
<!-- STATUS:LATEST_RELEASE_END -->

<!-- STATUS:ROADMAP_FOCUS_START -->
## Roadmap Focus

- **Current Active Task:** Production Deployment
- **Last completed task:** Notifications
<!-- STATUS:ROADMAP_FOCUS_END -->

## AI Dev OS Foundation Sync

- **Sync date:** 2026-06-17
- **Audit reference:** `AI_DEV_OS_PROJECT_SCAN.md`
- **Foundation report:** `AI_DEV_OS_FOUNDATION_SYNC_REPORT.md`
- **New governance artifacts:** `AI_CONTEXT.md`, `TASKS.md`, `SPEC.md`, `DESIGN.md`, `RELEASE_NOTES.md`

## Bounded Autonomous Mission Execution (2026-07-08)

- **Guide:** `MISSION_EXECUTION_GUIDE.md`
- **Queue:** `NEXT_ACTION_QUEUE.md`
- **M-001:** DONE — `reports/missions/M-001_EXECUTION_REPORT.md`
- **Pattern:** One mission → one execution report → one gate review
- Does **not** replace Visual Polish human PASS or Quality Gate DoD

## AI Dev OS Stack + Tool Intelligence (2026-07-09)

- **Stack constraints:** `STACK_CONSTRAINTS.md`
- **Frontend:** Next.js + TypeScript + Tailwind
- **Backend:** FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Primary implementation tool:** Cursor
- **v0:** Optional UI prototype only; never backend/auth/DB/reservations/security/tests/production
- **UI mission candidates:** M-011–M-015 (listing card, explore filters, product detail, empty states, mobile nav)
- **Next recommended mission (not auto-executed):** **M-002** — Profile UX audit (TYPE A)

## Current Phase & Focus

| Field | Value |
|-------|-------|
| **Active task** | Notifications |
| **Task status** | TODO |
| **Roadmap source** | `backend/MVP_ROADMAP.md` |
| **MVP progress** | 14 / 18 roadmap milestones completed (~78%) |

## Open Risks

1. **Real Transbank not integrated** — production WebPay credentials and SDK still required for live checkout.
2. **E2E WebPay mode** — full placeholder lifecycle E2E requires `PAYMENT_PROVIDER_MODE=webpay_placeholder` on backend (`run_melomanos.py --e2e-webpay` or `.env.local`).
3. **Pytest isolation** — `conftest.py` forces `PAYMENT_PROVIDER_MODE=simulate`; local `.env.local` must not leak into tests.
4. **Workspace path defaults** — `melomanos_paths.py` defaults to legacy `C:\melomanos_market` unless `MELOMANOS_*_DIR` env vars are set.
5. **Dual PROJECT_STATUS** — this file and `backend/PROJECT_STATUS.md` must be kept aligned after releases.

## Next Milestone

**Notifications** — implementation complete (Phases 1–4); formal roadmap close via `finish_task.py`. Next queue item: **Production Deployment**. See [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).

## Current MVP Features

- Marketplace
- Login / Auth
- Listings
- Discogs grading
- Used listing video requirement
- Favorites
- Orders
- Compra Segura / Escrow MVP
- **WebPay placeholder checkout** (sandbox + callback; simulate mode for dev default)
- Tracking
- Reviews
- Seller reputation
- Trust badges
- Digging Score
- Subscription plans
- Protected messaging
- **In-app notifications** (bell, dropdown, `/notifications`; no email/push yet)
- Seller shipping profile
- Disputes with evidence
- Dispute resolution (admin)
- Seller payout profile
- Admin panel (read-only ops dashboard)

## Current Business Model

- Free: 2 listings
- Pack: +3 listings for $990
- PRO: unlimited listings for $4.990/month

## Current Quality Gate

- Backend: `py -m pytest` — **231** tests
- Frontend: `npm run build`
- E2E: `npm run test:e2e` — **33** tests
- Full audit: `py run_audit.py`

## Next Recommended Work

### Mission layer (operational)

1. **M-002** — Profile UX audit (TYPE A) — first recommended; do not auto-start without `APPROVE_MISSION_EXECUTION`
2. Then M-003 (Profile polish) or M-011 (Listing card) / M-007 as prioritized in `NEXT_ACTION_QUEUE.md`

### Product roadmap (authoritative backlog)

1. Close Notifications milestone (`finish_task.py`) → Production deployment
2. Production deployment
3. Closed beta
4. Public launch

## AI Dev OS Document Map

| Document | Location | Role |
|----------|----------|------|
| AI_CONTEXT.md | workspace | Onboarding hub |
| STACK_CONSTRAINTS.md | workspace | Isolation, stack, Cursor/v0 rules |
| MISSION_EXECUTION_GUIDE.md | workspace | Mission pattern + approval tokens |
| NEXT_ACTION_QUEUE.md | workspace | Operational missions |
| TASKS.md | workspace | Task board |
| SPEC.md | workspace | Consolidated MVP spec |
| DESIGN.md | workspace | Flows and technical design |
| RELEASE_NOTES.md | workspace | Milestone history |
| WEBPAY_PHASE7_REPORT.md | workspace | WebPay placeholder release audit |
| MVP_ROADMAP.md | backend | Authoritative backlog |
| BUSINESS_RULES.md | backend | Authoritative business rules |
| ARCHITECTURE.md | backend | Authoritative architecture |

## Documentation Governance

Workspace docs (`AI_CONTEXT`, `TASKS`, `SPEC`, `DESIGN`, `RELEASE_NOTES`) are **indexes** — they link to authoritative backend sources; they do not override them.

**Priority on conflict:** `backend/BUSINESS_RULES.md` → `backend/ARCHITECTURE.md` → `backend/MVP_ROADMAP.md` → workspace summaries.

**Constraint pass:** 2026-06-18 — Notifications Phases 1–4 complete; roadmap advance pending `finish_task.py`.

## Source Documents

| Priority | Document | Path |
|----------|----------|------|
| 1 | Business rules | `backend/BUSINESS_RULES.md` |
| 2 | Architecture | `backend/ARCHITECTURE.md` |
| 3 | MVP roadmap | `backend/MVP_ROADMAP.md` |
| 4 | Agent rules | `backend/AGENT_RULES.md` |
| 5 | Backend project status | `backend/PROJECT_STATUS.md` |
| 6 | Quality gate | `workspace/QUALITY_GATE.md` |
| 7 | WebPay phase 7 report | `workspace/WEBPAY_PHASE7_REPORT.md` |
| 8 | WebPay implementation plan | `workspace/WEBPAY_IMPLEMENTATION_PLAN.md` |
