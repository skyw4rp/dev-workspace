# Decision Record — Bounties MVP Model (M-010)

**ID:** DR-BOUNTIES-001  
**Mission:** M-010  
**Date:** 2026-07-10  
**Status:** **PROPOSED** — pending human confirmation (M-020)  
**Implementation:** **NOT_APPROVED**

**Canonical spec:** [`BOUNTIES_PRODUCT_SPEC.md`](../BOUNTIES_PRODUCT_SPEC.md)

---

## Context

Melómanos has no bounties domain in code or [`backend/BUSINESS_RULES.md`](../../backend/BUSINESS_RULES.md). Compra Segura escrow applies to **listing orders** only. Protected messaging and in-app notifications exist. The product concept describes buyers offering an incentive for hard-to-find vinyl.

---

## Decision

Adopt **Option 2: Lightweight wanted-records board with optional stated incentive (informational only)** for Phase 1 implementation.

---

## Options evaluated

| Option | Summary | Pros | Cons | Verdict |
|--------|---------|------|------|---------|
| **1. Full bounty marketplace** | Escrow stated incentive; platform matching | Strong seller motivation | Payment custody, legal, disputes, new escrow path | **Defer** |
| **2. Wanted board + informational incentive** | Public requests; optional CLP incentive display; responses link to listings; purchase via Compra Segura | Reuses orders/messaging; shippable MVP | Incentive not enforceable; possible user confusion | **Recommended MVP** |
| **3. Saved search + alerts** | Notify when listing matches criteria | Low build cost | No seller-side “seeking buyer” signal; no incentive story | **Complementary** (not substitute) |
| **4. RFO without reward** | Wanted posts only, no incentive field | Simplest | Weaker differentiation vs forums | **Subset of Option 2** (incentive optional) |

---

## Consequences

### Positive

- No new payment provider or fund-custody scope in MVP.
- Fulfillment auditable via existing order `completed` state.
- Abuse surface reduced vs holding money.

### Negative / risks

- Stated incentive may be misunderstood → require persistent UI disclaimer.
- Sellers may still negotiate off-platform → rely on messaging safety (existing).
- Buyers may publish fake bounties → rate limits + moderation.

### Neutral

- Digging Score unchanged until separate decision.
- Bounties not added to [`backend/MVP_ROADMAP.md`](../../backend/MVP_ROADMAP.md) until human promotes.

---

## Evidence

| Source | Finding |
|--------|---------|
| [`backend/BUSINESS_RULES.md`](../../backend/BUSINESS_RULES.md) § Compra Segura | Escrow on orders only; $990 platform fee |
| [`workspace/SPEC.md`](../SPEC.md) | No bounties domain; favorites/search do not cover wanted-post |
| Code search (M-010) | Zero bounty references in frontend/backend |
| [`NOTIFICATIONS_SCOPE_REPORT.md`](../NOTIFICATIONS_SCOPE_REPORT.md) | Pattern for extending notification events |

---

## Human approval required before implementation

Confirm Option 2 and open decisions in [`BOUNTIES_PRODUCT_SPEC.md` §15](../BOUNTIES_PRODUCT_SPEC.md#15-open-human-decisions) via mission **M-020**.

---

*This record does not approve building the feature.*
