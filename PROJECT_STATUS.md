# Melómanos Market — Project Status

Living snapshot for product and quality status. Updated manually or via `py finish_task.py` after a successful release.

<!-- STATUS:LAST_QUALITY_GATE_START -->
## Last Quality Gate

- Date: 2026-06-17 22:47
- Backend tests: PASSED
- Frontend build: PASSED
- E2E tests: PASSED
- Full audit: PASSED
<!-- STATUS:LAST_QUALITY_GATE_END -->

<!-- STATUS:LATEST_RELEASE_START -->
## Latest Release

- Backend: Update AI Operating System documentation
- Frontend: Add payment provider integration (webpay placeholder) frontend
- Quality Gate: PASSED
- Date: 2026-06-17 22:47
<!-- STATUS:LATEST_RELEASE_END -->

<!-- STATUS:ROADMAP_FOCUS_START -->
## Roadmap Focus

- **Current Active Task:** Payment Provider Integration (WebPay placeholder)
- **Status:** IN_PROGRESS — Phases 1–7 implementation **DONE**; milestone pending commit/push and explicit roadmap advance
- **Next in queue:** Notifications
<!-- STATUS:ROADMAP_FOCUS_END -->

## AI Dev OS Foundation Sync

- **Sync date:** 2026-06-17
- **Audit reference:** `AI_DEV_OS_PROJECT_SCAN.md`
- **Foundation report:** `AI_DEV_OS_FOUNDATION_SYNC_REPORT.md`
- **New governance artifacts:** `AI_CONTEXT.md`, `TASKS.md`, `SPEC.md`, `DESIGN.md`, `RELEASE_NOTES.md`

## Current Phase & Focus

| Field | Value |
|-------|-------|
| **Phase** | Implementation (WebPay placeholder complete; release pending) |
| **Active task** | Payment Provider Integration (WebPay placeholder) |
| **Task status** | IN_PROGRESS (awaiting commit/push) |
| **Roadmap source** | `backend/MVP_ROADMAP.md` |
| **MVP progress** | 13 / 18 roadmap milestones completed (~72%); WebPay #14 ready after release |

## Open Risks

1. **Real Transbank not integrated** — production WebPay credentials and SDK still required for live checkout.
2. **E2E WebPay mode** — full placeholder lifecycle E2E requires `PAYMENT_PROVIDER_MODE=webpay_placeholder` on backend (`run_melomanos.py --e2e-webpay` or `.env.local`).
3. **Pytest isolation** — `conftest.py` forces `PAYMENT_PROVIDER_MODE=simulate`; local `.env.local` must not leak into tests.
4. **Workspace path defaults** — `melomanos_paths.py` defaults to legacy `C:\melomanos_market` unless `MELOMANOS_*_DIR` env vars are set.
5. **Dual PROJECT_STATUS** — this file and `backend/PROJECT_STATUS.md` must be kept aligned after releases.

## Next Milestone

**Payment Provider Integration (WebPay placeholder)** — implementation complete. Run `finish_task.py`, commit/push all three repos, then explicit roadmap advance. **Notifications** is next in queue.

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

- Backend: `py -m pytest` — **215** tests
- Frontend: `npm run build`
- E2E: `npm run test:e2e` — **31** tests
- Full audit: `py run_audit.py`

## Next Recommended Work

1. `finish_task.py` release (backend, frontend, workspace)
2. Explicit roadmap advance (Payment Provider → Completed)
3. Notifications (in-app + optional email)
4. Production deployment
5. Closed beta / public launch

## AI Dev OS Document Map

| Document | Location | Role |
|----------|----------|------|
| AI_CONTEXT.md | workspace | Onboarding hub |
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

**Constraint pass:** 2026-06-18 — WebPay Phase 7 docs aligned with implementation.

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
