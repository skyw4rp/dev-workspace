# TASKS — Melómanos Marketplace

**Purpose:** Workspace task board **index**.  
**Backlog master (authoritative):** [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md)  
**Last synced:** 2026-06-17 (constraint pass)

> **Do not duplicate roadmap content here.** For goals, acceptance criteria, and next steps, read [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).  
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

## IN_PROGRESS

### Payment Provider Integration (WebPay placeholder)

| Field | Value |
|-------|-------|
| **Status** | READY — [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) Current Active Task |
| **Queue line status** | TODO — documented inconsistency in roadmap |
| **Scope** | See roadmap item #1 — do not re-specify here |

**Before starting:** [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) (Compra Segura) + [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md) (Escrow Architecture).

---

## NEXT

### Notifications

Roadmap item #2 — [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) Current Priority Queue.

---

## BACKLOG

From [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) Current Priority Queue:

3. Production Deployment  
4. Closed Beta  
5. Public Launch  

**Future Ideas** (not in MVP queue until promoted): same file — Future Ideas table.

---

## Known Gaps (audit index)

Tracked in [`workspace/AI_DEV_OS_PROJECT_SCAN.md`](AI_DEV_OS_PROJECT_SCAN.md) §5–6 and [`workspace/SPEC.md`](SPEC.md). Not separate roadmap items unless promoted.

| Gap | Status |
|-----|--------|
| Register UI | MISSING — API only |
| Edit/delete listing UI | PARTIAL — backend only |
| `/releases` catalog API | DOCUMENTATION MISMATCH — see scan |
| WebPay | PLANNED — active task |
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
