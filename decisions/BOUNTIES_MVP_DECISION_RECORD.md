# Decision Record — Bounties MVP Model (M-010 / M-020)

**ID:** DR-BOUNTIES-001  
**Mission:** M-010 (spec) · M-020 (closure)  
**Date:** 2026-07-10 (M-010) · **2026-07-10 (M-020 approved)**  
**Status:** **APPROVED** (historical product decisions preserved)
**Implementation:** **EXPERIMENTAL / HOLD** — later human prioritization supersedes operational activation; no implementation is authorized.

**Canonical spec:** [`BOUNTIES_PRODUCT_SPEC.md`](../BOUNTIES_PRODUCT_SPEC.md)  
**Approval reference:** `APPROVE_MISSION_EXECUTION` / Mission: M-020

---

## Context

Melómanos has no bounties domain in code. Compra Segura escrow applies to **listing orders** only. M-010 defined Option 2 (informational wanted board). M-020 closes eight open decisions with explicit human approval.

---

## Master decision (M-010)

Adopt **Option 2: Lightweight wanted-records board with optional stated incentive (informational only)**.

| Status | **APPROVED** (M-010 spec + M-020 confirmation) |

**Rejected alternatives:** Full escrow marketplace (defer); saved-search-only (complementary); RFO without incentive field (subset only).

---

## Closed decisions (M-020)

### DR-001 — Financial model

| Field | Value |
|-------|--------|
| **Final decision** | MVP uses **informational stated incentive only**. Melómanos does **not** reserve, collect, hold, guarantee, or transfer the incentive. Compra Segura orders remain the **only** transaction mechanism. Escrow, incentive custody, refunds, and bounty-specific commissions are **outside MVP**. |
| **Status** | **APPROVED** |
| **Rationale** | Reuses existing payment/escrow infra; avoids legal/custody scope before pilot evidence. |
| **Rejected** | B) Escrow incentive; bounty-specific checkout; platform fee on incentive |
| **Implementation consequence** | No payment fields on bounty entities beyond display CLP; no WebPay path for incentives |
| **Risks retained** | Users may misunderstand incentive as guaranteed → UI disclaimer requirement |
| **Reconsideration trigger** | Separate legal + payment provider approval for Phase 3 financial model |

---

### DR-002 — Public incentive display

| Field | Value |
|-------|--------|
| **Final decision** | Optional incentive **may be displayed publicly in CLP**. Every relevant screen must state it is **declared by the buyer** and is **not reserved or guaranteed** by Melómanos. Must **not** be presented as paid, protected, secured, or held. |
| **Status** | **APPROVED** |
| **Rationale** | Supports user concept while minimizing false escrow impression. |
| **Rejected** | Hide until response; omit incentive field entirely |
| **Implementation consequence** | Copy tokens + `data-testid` disclaimer blocks on discovery, detail, create, manage screens |
| **Risks retained** | Incentive inflation signaling without enforcement |
| **Reconsideration trigger** | Abuse metrics on misleading incentives |

---

### DR-003 — Seller responses

| Field | Value |
|-------|--------|
| **Final decision** | MVP response **requires an existing listing** owned by the responder with `status = available`. Free-form or listing-less responses **excluded**. |
| **Status** | **APPROVED** |
| **Rationale** | Ties responses to Compra Segura path; reduces fraud surface. |
| **Rejected** | B) Create-on-respond without pre-existing listing; C) Text-only response |
| **Implementation consequence** | API validates `listing_id` ownership + `available`; UI listing picker only |
| **Risks retained** | Listing sold between response and accept → handle via order failure paths |
| **Reconsideration trigger** | Pilot shows insufficient seller listing coverage |

---

### DR-004 — Self-response

| Field | Value |
|-------|--------|
| **Final decision** | Bounty creator **cannot** respond to own bounty. **Server-side enforcement required** in implementation. |
| **Status** | **APPROVED** |
| **Rationale** | Prevents collusion and reputation gaming. |
| **Rejected** | Allow self-response |
| **Implementation consequence** | `responder_id != bounty.creator_id` check on create response |
| **Risks retained** | Multi-account collusion (deferred — operational) |
| **Reconsideration trigger** | Fraud evidence |

---

### DR-005 — Fulfillment

| Field | Value |
|-------|--------|
| **Final decision** | Bounty becomes **FULFILLED** only when linked Compra Segura order reaches canonical **`completed`** state. Accepting a response **does not** fulfill. Accepting **does not** auto-reserve listing unless a **future explicitly approved** design defines atomic accept+reserve. |
| **Status** | **APPROVED** |
| **Rationale** | Auditable fulfillment; avoids reservation/order coupling bugs. |
| **Rejected** | Manual buyer confirm without order; auto-reserve on accept |
| **Implementation consequence** | Order completion webhook/job transitions bounty; accept is non-terminal pre-checkout |
| **Risks retained** | Buyer accepts then never purchases → seller effort unrewarded (operational) |
| **Reconsideration trigger** | Pilot fulfillment rate below threshold |

---

### DR-006 — Digging Score

| Field | Value |
|-------|--------|
| **Final decision** | Bounty create/respond/accept/cancel/expire/fulfill has **no Digging Score effect** in MVP. Reputation integration **deferred**. |
| **Status** | **APPROVED** |
| **Rationale** | Aligns with BUSINESS_RULES — score from platform orders/activity; avoids gaming. |
| **Rejected** | +N points for bounty fulfillment |
| **Implementation consequence** | No hooks in `digging_score` service for bounty events |
| **Risks retained** | None material for MVP |
| **Reconsideration trigger** | Post-pilot product review |

---

### DR-007 — Active bounty limit

| Field | Value |
|-------|--------|
| **Final decision** | Max **5 ACTIVE-equivalent** bounties per user (`ACTIVE`, `MATCHED`, `ACCEPTED` count toward limit; `DRAFT` and terminal states per M-010 state model). Backend must enforce **atomically** on create/activate. |
| **Status** | **APPROVED** |
| **Rationale** | Balances utility vs spam. |
| **Rejected** | Limits of 3 or 10 |
| **Implementation consequence** | Transactional count check; 409 on exceed |
| **Risks retained** | Power users may hit cap |
| **Reconsideration trigger** | Pilot usage data |

---

### DR-008 — Roadmap and rollout

| Field | Value |
|-------|--------|
| **Final decision** | **Closed pilot** first. Not promoted to general MVP scope until pilot evidence reviewed. Implementation may use controlled exposure; **public rollout requires separate gate**. |
| **Status** | **APPROVED** |
| **Rationale** | Marketplace maturity; avoids roadmap distraction from deployment/WebPay priorities. |
| **Rejected** | Immediate MVP_ROADMAP promotion; open public launch day one |
| **Implementation consequence** | Feature flag / allowlist; no MVP_ROADMAP promotion in M-020 |
| **Risks retained** | Low liquidity in pilot cohort |
| **Reconsideration trigger** | Pilot metrics review + explicit promotion approval |

---

## Public terminology (M-020)

| Context | Term |
|---------|------|
| **Internal / technical** | `Bounty`, `BountyResponse`, API routes |
| **Primary customer-facing** | **Vinilos buscados** |
| **Supporting copy** | “Busco este vinilo”; “Incentivo ofrecido” |
| **Forbidden customer-facing** | Wording implying guaranteed payment, escrowed reward, secured/held funds |

---

## Implementation authorization boundary

| Scope | Status |
|-------|--------|
| Bounded backend domain design (M-021) | **HOLD** — not READY, active, next, or authorized |
| API, UI, notifications, E2E (M-022–M-027) | **HOLD** — no implementation work authorized |
| Payment custody / incentive escrow | **NOT_APPROVED** |
| Digging Score integration | **NOT_APPROVED** (deferred) |
| General public rollout | **NOT_APPROVED** — closed pilot only |

---

## Evidence

| Source | Finding |
|--------|---------|
| M-010 spec | Option 2 recommended; eight open decisions in §15 |
| M-020 human authorization | All eight decisions explicitly approved |
| [`backend/BUSINESS_RULES.md`](../../backend/BUSINESS_RULES.md) | Compra Segura on orders; Digging Score from platform activity |

---

*These approved product decisions remain historical evidence. The later human prioritization decision supersedes operational activation without erasing them: Bounties and M-021 are on HOLD until a new explicit human decision; see [`BOUNTIES_HOLD_DECISION_RECORD.md`](BOUNTIES_HOLD_DECISION_RECORD.md).*
