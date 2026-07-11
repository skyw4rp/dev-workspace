# SPEC — Melómanos Marketplace MVP

**Purpose:** MVP **coverage index** — what is implemented vs planned, with pointers to authoritative specs.  
**Last synced:** 2026-06-17 (constraint pass)

> **This file does not define requirements.**  
> **Authoritative:** [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md), [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md), [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).

**Status legend:** `IMPLEMENTED` | `PARTIAL` | `PLANNED` | `UNKNOWN`

---

## Domain Index

| Domain | Status | Business rules | Architecture | Code |
|--------|--------|----------------|--------------|------|
| Auth | IMPLEMENTED (UI register: PARTIAL) | [BUSINESS_RULES](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Auth](../backend/ARCHITECTURE.md) | [`routers/auth.py`](../backend/app/routers/auth.py), [`/login`](../frontend/src/app/login/page.tsx) |
| Listings | IMPLEMENTED (edit/delete UI: PARTIAL) | [BUSINESS_RULES § Marketplace](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Listings](../backend/ARCHITECTURE.md) | [`routers/listings.py`](../backend/app/routers/listings.py), [`/sell`](../frontend/src/app/sell/page.tsx) |
| Favorites | IMPLEMENTED | — | [ARCHITECTURE § Favorites](../backend/ARCHITECTURE.md) | [`routers/favorites.py`](../backend/app/routers/favorites.py) |
| Messaging | IMPLEMENTED | [BUSINESS_RULES § Protected Messaging](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Messages](../backend/ARCHITECTURE.md) | [`routers/messages.py`](../backend/app/routers/messages.py), [`message_safety.py`](../backend/app/services/message_safety.py) |
| Reservations | IMPLEMENTED | [BUSINESS_RULES § Marketplace](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Listings](../backend/ARCHITECTURE.md) | [`listings.py` reserve](../backend/app/routers/listings.py), [`orders.py` from-listing](../backend/app/routers/orders.py) |
| Orders / Escrow | IMPLEMENTED | [BUSINESS_RULES § Compra Segura](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Orders, Escrow](../backend/ARCHITECTURE.md) | [`routers/orders.py`](../backend/app/routers/orders.py), [`escrow.py`](../backend/app/services/escrow.py) |
| Reviews | IMPLEMENTED | [BUSINESS_RULES](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Reviews](../backend/ARCHITECTURE.md) | [`routers/reviews.py`](../backend/app/routers/reviews.py), [`orders/[id]`](../frontend/src/app/orders/[id]/page.tsx) |
| Disputes | IMPLEMENTED | [BUSINESS_RULES](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Disputes](../backend/ARCHITECTURE.md) | [`routers/disputes.py`](../backend/app/routers/disputes.py) |
| Admin | IMPLEMENTED (panel read-only) | — | [ARCHITECTURE](../backend/ARCHITECTURE.md) | [`routers/admin.py`](../backend/app/routers/admin.py), [`/admin`](../frontend/src/app/admin/page.tsx) |
| Payments (WebPay) | PLANNED | [BUSINESS_RULES § Compra Segura](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Escrow](../backend/ARCHITECTURE.md) | [`MVP_ROADMAP` item #1](../backend/MVP_ROADMAP.md) |
| Notifications | PLANNED | — | — | [`MVP_ROADMAP` item #2](../backend/MVP_ROADMAP.md) |
| Subscriptions | IMPLEMENTED | [BUSINESS_RULES § Subscription](../backend/BUSINESS_RULES.md) | [ARCHITECTURE § Subscriptions](../backend/ARCHITECTURE.md) | [`subscription.py`](../backend/app/services/subscription.py) |
| Reputation / Digging Score | IMPLEMENTED | [BUSINESS_RULES](../backend/BUSINESS_RULES.md) | [ARCHITECTURE](../backend/ARCHITECTURE.md) | [`users.py`](../backend/app/routers/users.py) |
| Shipping / Payout profiles | IMPLEMENTED (payout UI: UNKNOWN) | [BUSINESS_RULES](../backend/BUSINESS_RULES.md) | [ARCHITECTURE](../backend/ARCHITECTURE.md) | [`users.py`](../backend/app/routers/users.py) |
| **Bounties / Wanted records** | **PLANNED** | [BOUNTIES_PRODUCT_SPEC](BOUNTIES_PRODUCT_SPEC.md) · [DR-BOUNTIES-001](decisions/BOUNTIES_MVP_DECISION_RECORD.md) | — | Decisions **APPROVED** M-020; bounded implementation M-021+; **closed pilot** |
| Catalog `/releases` | UNKNOWN | — | README/CHANGELOG only | Not in [`main.py`](../backend/app/main.py) |

---

## Coverage Gaps (index only)

| Gap | Status | Detail in |
|-----|--------|-----------|
| Registration UI | PARTIAL | [`AI_DEV_OS_PROJECT_SCAN.md`](AI_DEV_OS_PROJECT_SCAN.md) |
| Edit/delete listing UI | PARTIAL | Same |
| Product photo upload | PARTIAL | Same |
| Legal pages | MISSING | [`MVP_ROADMAP` Public Launch](../backend/MVP_ROADMAP.md) |
| Production API URL config | MISSING | [`MVP_ROADMAP` Production Deployment](../backend/MVP_ROADMAP.md) |

---

## Quality Gate

Definition of Done: [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md).  
Last documented PASS: [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) — 2026-06-05. Current run: **UNKNOWN**.

---

## Source Documents

| Priority | Document | Path |
|----------|----------|------|
| 1 | Business rules | [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) |
| 2 | Architecture | [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md) |
| 3 | MVP roadmap | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) |
| 4 | API overview | [`backend/docs/api_overview.md`](../backend/docs/api_overview.md) |
| 5 | Live routes | [`backend/app/main.py`](../backend/app/main.py) |
| 6 | Project scan | [`workspace/AI_DEV_OS_PROJECT_SCAN.md`](AI_DEV_OS_PROJECT_SCAN.md) |
| 7 | Testing strategy | [`backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md) |
| 8 | Quality gate | [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md) |

---

*Add rows when domains change; do not copy rule text from Source Documents.*
