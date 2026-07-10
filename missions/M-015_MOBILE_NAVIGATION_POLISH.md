# M-015 — Mobile Navigation Polish

**Mission ID:** M-015  
**Type:** TYPE C — Frontend Low-Risk  
**Priority:** P2  

---

## Goal

Improve mobile utility and product header usability within Header IA C1 — spacing, touch targets, and product-link row scroll behavior. No IA redesign.

---

## Scope

- `frontend/src/components/Navbar.tsx` only
  - Mobile utility row spacing (logo, search, icon cluster)
  - Product nav row horizontal scroll with snap and touch-friendly link targets
  - Preserve all `data-testid` values and product link behavior

---

## Forbidden

- Header IA C2 presets / hamburger redesign
- HomeHero / Home restructure
- `/messages` back link (M-019)
- Backend changes
- Route PASS
- Commits without session authorization

---

## Acceptance criteria

1. Product nav links meet min touch height on mobile
2. Product row scrolls cleanly on narrow viewports without layout break
3. Existing header E2E tests pass at desktop viewport
4. `npm run build` + full E2E PASS
5. Execution report; routes IN_REVIEW

---

## Verification

- `npm run build`
- `npm run test:e2e`
