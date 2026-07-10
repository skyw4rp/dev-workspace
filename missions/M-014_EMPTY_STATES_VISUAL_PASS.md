# M-014 — Empty States Visual Pass

**Mission ID:** M-014  
**Type:** TYPE C — Frontend Low-Risk  
**Priority:** P2  

---

## Goal

Unify editorial empty states on collector surfaces (favorites, messages, orders, explorar catalog) with ivory/black/gold system chrome and Phase 1 `/explorar` navigation.

---

## Scope

- New shared `frontend/src/components/EditorialEmptyState.tsx`
- `frontend/src/app/favorites/page.tsx`
- `frontend/src/app/messages/page.tsx` (inbox + thread placeholders)
- `frontend/src/app/orders/page.tsx`
- `frontend/src/components/catalog/CatalogExplore.tsx` (no-results state)

---

## Forbidden

- Backend / API contract changes
- Profile page tab empty states (separate surface)
- Admin empty tables
- Route PASS
- New product flows
- Commits without token

---

## Acceptance criteria

1. Shared editorial empty-state component (eyebrow, title, description, optional CTA)
2. CTAs route to `/explorar` (not `/`) where catalog exploration is intended
3. All `data-testid` values preserved
4. `npm run build` + `npm run test:e2e` (43/43) PASS
5. Execution report; routes IN_REVIEW

---

## Verification

```bash
cd frontend && npm run build && npm run test:e2e
cd workspace && py run_melomanos.py --check
```
