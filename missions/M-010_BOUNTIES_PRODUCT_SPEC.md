# M-010 — Bounties Product Spec

**Mission ID:** M-010  
**Type:** TYPE G — Product Definition / Architecture Decision  
**Priority:** P3  
**Status:** IN_PROGRESS (execution authorized 2026-07-10)

---

## Title

Bounties product spec

---

## Goal

Define the smallest viable, testable **Bounties / Wanted Records** capability for Melómanos Market as documentation only — sufficient to derive future implementation missions without building the feature.

---

## Scope

- Product discovery from existing project evidence (business rules, architecture, messaging, orders, notifications).
- Requirements, business rules, state model, UX IA, trust/abuse analysis, and rollout phases.
- One canonical specification, one MVP decision record, queue synchronization, execution report.
- Proposed implementation mission decomposition (PROPOSED/BLOCKED only).

---

## Non-goals

- Frontend or backend implementation.
- Database migrations, API endpoints, or payment integration.
- WebPay, escrow extension for bounty funds, or reservation/order changes.
- Automatic activation of implementation missions.
- Visual design or route PASS approval.
- Push, tags, or history rewrite.

---

## Risk

| Risk | Level | Mitigation |
|------|-------|------------|
| Payment/legal scope creep | High | MVP excludes fund custody; explicit decision table |
| Off-platform bypass | High | Reuse protected messaging; no contact in public bounty fields |
| Order/reservation coupling | Medium | Bounty acceptance hands off to existing listing/order flow |
| Low liquidity / empty board | Medium | Premortem + phased rollout |
| Spec contradicts BUSINESS_RULES | Medium | Align with Compra Segura for transactions only |

---

## Allowed files (workspace only)

| Path | Purpose |
|------|---------|
| `missions/M-010_BOUNTIES_PRODUCT_SPEC.md` | This brief |
| `BOUNTIES_PRODUCT_SPEC.md` | Canonical product specification |
| `decisions/BOUNTIES_MVP_DECISION_RECORD.md` | MVP model decision record |
| `SPEC.md` | Index row only (pointer) |
| `NEXT_ACTION_QUEUE.md` | M-010 closure + proposed missions |
| `reports/missions/M-010_EXECUTION_REPORT.md` | Mission report |

---

## Forbidden files

- `frontend/**`, `backend/**`, `C:\ai-dev-os/**`
- Screenshots, test-results, logs, `.env`, generated artifacts
- Duplicate long-form copies of spec content in multiple files

---

## Acceptance criteria

1. Canonical spec covers problem, terminology, MVP scope, journeys, state model, business rules, trust/abuse, privacy, payment boundary, integration, conceptual data model, UX IA, metrics, rollout, open decisions.
2. Alternatives evaluated with recommendation for smallest viable option.
3. Premortem and red-team review documented.
4. Implementation status explicitly **NOT_APPROVED**.
5. Proposed follow-on missions listed as PROPOSED/BLOCKED — not READY.
6. Gate PASS or PASS WITH WARNINGS; execution report + queue sync.
7. `py run_melomanos.py --check` passes.

---

## Unresolved decisions (for human closure — not blocking spec mission)

- Whether stated **incentive amount** is displayed publicly in MVP.
- Whether sellers may respond **without** an active listing (create-on-respond vs listing-required).
- Reputation / Digging Score credit for bounty fulfillment.
- Financial incentive / escrow model (deferred post-MVP).

---

## Authoritative documents to read / update

| Document | Action |
|----------|--------|
| [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) | Read only — do not modify in this mission |
| [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md) | Read only |
| [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) | Read only |
| [`SPEC.md`](../SPEC.md) | Add Bounties index row |
| [`NOTIFICATIONS_SCOPE_REPORT.md`](../NOTIFICATIONS_SCOPE_REPORT.md) | Read — notification patterns |
| [`MISSION_EXECUTION_GUIDE.md`](../MISSION_EXECUTION_GUIDE.md) | Read — TYPE G conventions |

---

## Verification required

- Spec completeness review (self + gate).
- `py run_melomanos.py --check`.
- No broken relative links in new docs.
- No frontend/backend modifications.

---

## Stop conditions

- Any repo dirty unexpectedly.
- Brief contradicted by evidence → HOLD.
- Payment/legal decision required before MVP definition → HOLD (MVP without custody is definable).
- Application code changes needed.
- Human must choose between incompatible MVP models without a documentable default → HOLD.

---

## Canonical spec path

[`BOUNTIES_PRODUCT_SPEC.md`](../BOUNTIES_PRODUCT_SPEC.md)

---

## Report path

[`reports/missions/M-010_EXECUTION_REPORT.md`](../reports/missions/M-010_EXECUTION_REPORT.md)
# M-010 — DONE / HISTORICAL / NON-OPERATIVE

This brief preserves its original body and authorization evidence. It grants no current execution authority; only the canonical JSON block in `../PROJECT_STATUS.md` can do so.
