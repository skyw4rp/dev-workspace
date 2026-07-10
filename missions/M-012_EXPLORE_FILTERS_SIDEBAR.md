# M-012 — Explore Filters / Sidebar Improvement

**Mission ID:** M-012  
**Type:** TYPE C — Frontend Low-Risk  
**Priority:** P1  
**Route:** `/explorar`

---

## Goal

Improve visual hierarchy and readability of the Explore catalog filter chrome without changing filter semantics or query behavior.

---

## Scope

- `frontend/src/components/catalog/CatalogExplore.tsx` — layout, Tailwind classes, copy labels only
- Optional: `frontend/src/app/explorar/page.tsx` — page shell spacing only if needed

---

## Forbidden

- Backend, API, auth, orders, payments, messaging, reservations
- `lib/marketplace-filters.ts` query contract changes
- `useCatalogListings` behavior changes
- Header C2 presets (Sellos / Artistas modes)
- Home restructure, Navbar, ListingCard, Admin
- Route PASS
- v0 integration
- Commits without token

---

## Acceptance criteria

1. Desktop: filters in a sticky sidebar; results grid beside it
2. Mobile: filters remain visible on load (`data-testid="marketplace-filters"`)
3. Editorial ivory/black/gold system consistent with M-016 cards / M-013 detail
4. `npm run build` PASS
5. `npm run test:e2e` PASS (43/43)
6. `npm run test:e2e:visual-polish` PASS
7. `py run_melomanos.py --check` PASS
8. Execution report + screenshot run path; route IN_REVIEW

---

## Verification

```bash
cd frontend && npm run build && npm run test:e2e && npm run test:e2e:visual-polish
cd workspace && py run_melomanos.py --check
```

---

## Stop conditions

- Sort/query contract change required → STOP
- Sellos/Artistas preset IA needed → STOP (TYPE G / C2)
- Business-rule or API change → STOP (TYPE F)
