# Phase 1.1 E2E + Governance Alignment

**Date:** 2026-07-03  
**Frontend base:** 148986a (+ uncommitted test/governance changes)  
**Workspace base:** 45ad85c (+ uncommitted governance changes)

## Verdict

**PASS WITH WARNINGS**

- Phase 1 IA E2E alignment: complete (40/41 passing)
- WebPay/Favorites flakes: resolved in test helpers
- Messages inbox reply: regression test added; exposes **REAL_PRODUCT_BUG** (missing `POST /messages/reply`)
- Governance: `/explorar` represented; Home catalog dependency removed from manifest

## Known open item

| Test | Classification | Notes |
|------|----------------|-------|
| `messages reply from inbox thread` | **REAL_PRODUCT_BUG** | Frontend calls `POST /messages/reply`; backend router has no reply handler (404 `Not Found`). Prior weak assertion matched unsent textarea text (false positive). Strengthened test now fails correctly. |

**Recommended follow-up (out of Phase 1.1 scope):** add bounded backend `POST /messages/reply` or route inbox replies through existing `POST /messages` with explicit `receiver_id`.
