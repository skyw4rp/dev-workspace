# Melómanos Market — Project Status

Living snapshot for product and quality status. Updated manually or via `py finish_task.py` after a successful release.

<!-- STATUS:LAST_QUALITY_GATE_START -->
## Last Quality Gate

- Date: 2026-06-17 18:28
- Backend tests: PASSED
- Frontend build: PASSED
- E2E tests: PASSED
- Full audit: PASSED
<!-- STATUS:LAST_QUALITY_GATE_END -->

<!-- STATUS:LATEST_RELEASE_START -->
## Latest Release

- Backend: No changes.
- Frontend: No changes.
- Quality Gate: PASSED
- Date: 2026-06-17 18:28
<!-- STATUS:LATEST_RELEASE_END -->

<!-- STATUS:ROADMAP_FOCUS_START -->
## Roadmap Focus

- **Current Active Task:** Payment Provider Integration (WebPay placeholder)
- **Status:** IN_PROGRESS (Phase 1 complete — shared payment confirmation service)
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
| **Phase** | Implementation |
| **Active task** | Payment Provider Integration (WebPay placeholder) |
| **Task status** | IN_PROGRESS (Phase 1 complete) |
| **Roadmap source** | `backend/MVP_ROADMAP.md` |
| **MVP progress** | 13 / 18 roadmap milestones completed (~72%) |

## Open Risks

1. **WebPay not implemented** — payments remain simulate-only; blocks production checkout.
2. **Workspace path defaults** — `melomanos_paths.py` defaults to legacy `C:\melomanos_market` unless `MELOMANOS_*_DIR` env vars are set.
3. **Documentation drift** — `/releases` catalog documented in backend README/CHANGELOG but not registered in `app/main.py`.
4. **Dual PROJECT_STATUS** — this file and `backend/PROJECT_STATUS.md` must be kept aligned after releases.
5. **Quality Gate staleness** — last PASS documented 2026-06-05; current test status **UNKNOWN** until re-run.

## Next Milestone

**Payment Provider Integration (WebPay placeholder)** — Phase 1 complete (`confirm_order_payment_held`). Remaining: checkout, webhook, frontend, E2E. **Notifications** is next after WebPay ships.

## Current MVP Features

- Marketplace
- Login / Auth
- Listings
- Discogs grading
- Used listing video requirement
- Favorites
- Orders
- Compra Segura / Escrow MVP
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

- Backend: `py -m pytest`
- Frontend: `npm run build`
- E2E: `npm run test:e2e`
- Full audit: `py run_audit.py`

## Next Recommended Work

- Payment provider integration (WebPay placeholder)
- Notifications (in-app + optional email)
- Production deployment
- Closed beta
- Public launch

## AI Dev OS Document Map

| Document | Location | Role |
|----------|----------|------|
| AI_CONTEXT.md | workspace | Onboarding hub |
| TASKS.md | workspace | Task board |
| SPEC.md | workspace | Consolidated MVP spec |
| DESIGN.md | workspace | Flows and technical design |
| RELEASE_NOTES.md | workspace | Milestone history |
| MVP_ROADMAP.md | backend | Authoritative backlog |
| BUSINESS_RULES.md | backend | Authoritative business rules |
| ARCHITECTURE.md | backend | Authoritative architecture |

## Documentation Governance

Workspace docs (`AI_CONTEXT`, `TASKS`, `SPEC`, `DESIGN`, `RELEASE_NOTES`) are **indexes** — they link to authoritative backend sources; they do not override them.

**Priority on conflict:** `backend/BUSINESS_RULES.md` → `backend/ARCHITECTURE.md` → `backend/MVP_ROADMAP.md` → workspace summaries.

**Constraint pass:** 2026-06-17 — workspace foundation docs refactored to prefer references over duplicated content.

## Source Documents

| Priority | Document | Path |
|----------|----------|------|
| 1 | Business rules | `backend/BUSINESS_RULES.md` |
| 2 | Architecture | `backend/ARCHITECTURE.md` |
| 3 | MVP roadmap | `backend/MVP_ROADMAP.md` |
| 4 | Agent rules | `backend/AGENT_RULES.md` |
| 5 | Backend project status | `backend/PROJECT_STATUS.md` |
| 6 | Quality gate | `workspace/QUALITY_GATE.md` |
| 7 | Project scan | `workspace/AI_DEV_OS_PROJECT_SCAN.md` |
| 8 | Foundation sync report | `workspace/AI_DEV_OS_FOUNDATION_SYNC_REPORT.md` |
