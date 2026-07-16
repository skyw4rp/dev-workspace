# Decision Record — Bounties Operational Hold

**ID:** DR-BOUNTIES-002
**Date:** 2026-07-15
**Status:** **SUBORDINATE DECISION EVIDENCE**
**Operational authority reference:** [`PROJECT_STATUS.md`](../PROJECT_STATUS.md)

## Decision

Bounties is **EXPERIMENTAL / HOLD** until a new explicit human decision. M-021 is **HOLD** and is not READY, active, next, or authorized for implementation.

No Bounties backend, persistence, schema, migration, API, UI, test, dependency, or operational work is authorized. This includes all proposed Bounties follow-on work (M-022–M-027).

## Relationship to existing evidence

This later prioritization decision supersedes the prior operational activation of M-021. It does **not** erase, amend, or invalidate the historical M-010 specification, the completed M-020 decision closure, or commit `189e960` (“Approve Bounties MVP product decisions”).

The preserved product history remains available in [`BOUNTIES_PRODUCT_SPEC.md`](../BOUNTIES_PRODUCT_SPEC.md) and [`BOUNTIES_MVP_DECISION_RECORD.md`](BOUNTIES_MVP_DECISION_RECORD.md). Any future reconsideration must use that evidence and receive a new explicit human decision before implementation can be authorized.

## Consequences

| Item | Disposition |
|------|-------------|
| Bounties product specification | Historical product evidence retained |
| M-020 decisions | Historical approved decisions retained |
| M-021 | HOLD; no execution authorization |
| M-022–M-027 | HOLD; no execution authorization |
| Production roadmap promotion | Not authorized |

*This record is subordinate decision evidence; it does not govern operational disposition or modify the substantive business-rule or architecture authorities.*
# Subordinate decision evidence

This record is subordinate evidence only. Its HOLD effect exists only because the canonical JSON authority block in `../PROJECT_STATUS.md` adopts the Bounties HOLD state; this record cannot independently authorize, hold, release, or execute work.
