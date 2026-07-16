# TASKS — Melómanos Marketplace

**Purpose:** Planning and task **index**; this file is **not an operational authority**.
**Operational authority:** [`PROJECT_STATUS.md`](PROJECT_STATUS.md).
**Product roadmap:** [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) (not an execution authority).
**Last reconciled:** 2026-07-15

> **Do not authorize work from this index.** For operational state, read [`PROJECT_STATUS.md`](PROJECT_STATUS.md). For product-roadmap content, read [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).
> Completion rules: [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md).

---

## COMPLETED

13 milestones per [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) — **Completed** table:

1. Marketplace Core  
2. Favorites  
3. Protected Messaging  
4. Reviews  
5. Seller Reputation  
6. Digging Score  
7. Subscription Plans  
8. Seller Shipping Profile  
9. Escrow MVP  
10. Disputes With Evidence  
11. Dispute Resolution  
12. Seller Payout Profile  
13. Admin Panel MVP  

**Last documented Quality Gate:** 2026-06-05 — see [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) markers.  
**Release detail:** [`workspace/RELEASE_NOTES.md`](RELEASE_NOTES.md).

---

## Operational reference

- **Sole READY mission:** [`MEL-UX-001 — Frontend UX and Product Readiness Audit`](missions/MEL-UX-001_FRONTEND_UX_READINESS_AUDIT.md), read-only.
- **Bounties / M-021:** EXPERIMENTAL / HOLD; no implementation work authorized.
- **Production Deployment:** DEFERRED pending UX and product-readiness evidence.

---

## BACKLOG

From [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) Current Priority Queue:

1. Production Deployment — deferred pending UX and product-readiness evidence
2. Closed Beta — not authorized
3. Public Launch — not authorized

**Future Ideas** (not in MVP queue until promoted): same file — Future Ideas table.

---

## Known Gaps (audit index)

Tracked in [`workspace/AI_DEV_OS_PROJECT_SCAN.md`](AI_DEV_OS_PROJECT_SCAN.md) §5–6 and [`workspace/SPEC.md`](SPEC.md). Not separate roadmap items unless promoted.

| Gap | Status |
|-----|--------|
| Register UI | MISSING — API only |
| Edit/delete listing UI | PARTIAL — backend only |
| `/releases` catalog API | DOCUMENTATION MISMATCH — see scan |
| WebPay | Historical placeholder implementation; no active work authorized by this index |
| Terms / privacy pages | MISSING |

---

## Source Documents

| Document | Path | Use for |
|----------|------|---------|
| MVP roadmap | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) | Tasks, goals, steps |
| Business rules | [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) | Product constraints |
| Architecture | [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md) | Technical design |
| Quality gate | [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md) | Definition of Done |
| Project status | [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) | Current focus |
| Project scan | [`workspace/AI_DEV_OS_PROJECT_SCAN.md`](AI_DEV_OS_PROJECT_SCAN.md) | Gaps and risks |
| Release notes index | [`workspace/RELEASE_NOTES.md`](RELEASE_NOTES.md) | Shipped milestones |

---

*Sync this index after each `finish_task.py` release. Update counts only; details stay in roadmap.*
