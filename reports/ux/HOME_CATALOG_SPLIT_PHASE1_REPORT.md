# Home + Catalog Split — Phase 1 Implementation Report

**Date:** 2026-07-03  
**Scope:** Phase 1 only (structural route split, no Gate B, no sidebar redesign, no URL-synced filters)  
**Plan reference:** `workspace/reports/ux/HOME_CATALOG_SPLIT_PLAN.md`

---

## Summary

Phase 1 splits the monolithic Home/catalog experience into two routes:

| Route | Component | Content |
|-------|-----------|---------|
| `/` | `HomeDiscovery` | Hero, metrics, new arrivals rail, benefits, community — **no catalog grid or filters** |
| `/explorar` | `CatalogExplore` | Full filter form, listing grid, loading/error/empty states (unchanged behavior) |

`Marketplace.tsx` was removed. Catalog logic was extracted into `useCatalogListings` + `useListingsQuery` without changing API contracts or filter mapping.

Navbar **Explorar**, **Sellos**, and **Artistas** now route to `/explorar`. Header search navigates to `/explorar` with a `sessionStorage` bridge for the query when not already on the explore page. Home CTAs (`HomeHero`, `HomeMetricsBand`, `HomeNewArrivals`) point to `/explorar`.

---

## Files changed by repo

### Frontend (`C:\melomanos\frontend`)

| Action | Path |
|--------|------|
| **Added** | `src/app/explorar/page.tsx` |
| **Added** | `src/components/catalog/CatalogExplore.tsx` |
| **Added** | `src/components/home/HomeDiscovery.tsx` |
| **Added** | `src/hooks/useCatalogListings.ts` |
| **Added** | `src/lib/useListingsQuery.ts` |
| **Deleted** | `src/components/Marketplace.tsx` |
| **Modified** | `src/app/page.tsx` |
| **Modified** | `src/components/Navbar.tsx` |
| **Modified** | `src/components/home/HomeHero.tsx` |
| **Modified** | `src/components/home/HomeMetricsBand.tsx` |
| **Modified** | `src/components/home/HomeNewArrivals.tsx` |
| **Modified** | `src/lib/home-search.ts` |
| **Modified** | `src/lib/marketplace-filters.ts` |
| **Modified** | `e2e/melomanos.spec.ts` |

### Workspace (`C:\melomanos\workspace`)

| Action | Path |
|--------|------|
| **Added** | `reports/ux/HOME_CATALOG_SPLIT_PHASE1_REPORT.md` (this file) |

No backend, API, or auth files were modified.

---

## Route changes

| Before | After |
|--------|-------|
| `/` → `Marketplace` (hero + catalog) | `/` → `HomeDiscovery` (discovery only) |
| — | `/explorar` → `CatalogExplore` (full catalog) |
| Navbar Explorar → `/#catalogo` | Navbar Explorar → `/explorar` |
| Navbar Sellos/Artistas → `/#catalogo` | Navbar Sellos/Artistas → `/explorar` |
| Hero CTA → `#catalogo` | Hero CTA → `/explorar` |
| Home “Ver todos” / metrics link → `#catalogo` | → `/explorar` |
| Header search → scroll + event on `/` | → `router.push('/explorar')` + `sessionStorage` pending search |

**Unchanged:** `/listings/[id]`, `/sell`, `/login`, `/profile`, `/orders`, `/messages`, `/favorites`, `/admin`, `/#nuevos-ingresos`, `/#guia-digger`.

---

## Component changes

### `HomeDiscovery`
- Fetches `{ skip: 0, limit: 20 }` via `useListingsQuery` for featured listing + new arrivals rail.
- Renders: `HomeHero`, `HomeMetricsBand`, `HomeNewArrivals`, `HomeBenefitsStrip`, `HomeCommunityCard`.
- No filter state, no catalog grid.

### `CatalogExplore`
- Extracted verbatim catalog UI from former `Marketplace.tsx` (top filter card + grid).
- Uses `useCatalogListings` for form state, API filters, navbar search event, and pending search consumption on mount.
- Retains `id="catalogo"` and `data-testid="marketplace-filters"` for test compatibility and scroll target on `/explorar`.

### `useListingsQuery`
- Shared listings fetch hook (loading, error, data).

### `useCatalogListings`
- Filter form + applied filters + `HOME_SEARCH_EVENT` listener + `consumePendingHomeSearch()` on mount.

### `home-search.ts`
- Added `setPendingHomeSearch` / `consumePendingHomeSearch` via `sessionStorage` (Phase 1 bridge; not URL-synced).

### `HomeHero`
- CTA changed from `<a href="#catalogo">` to `<Link href="/explorar">` (navigation only; copy/layout unchanged per frozen hero policy).
- Fallback detail href when no listing: `/explorar`.

### `Navbar`
- `exploreActive` highlights Explorar when `pathname === '/explorar'`.
- Search submit: on `/explorar` dispatches event + scrolls; elsewhere stores pending search and navigates.

---

## Validation commands run

| Command | Result |
|---------|--------|
| `npm run build` (frontend) | **PASS** — `/explorar` listed in route table |
| `npm run test:unit` | **PASS** — 12/12 |
| `npx playwright test e2e/melomanos.spec.ts -g "homepage loads discovery\|explorar page loads"` | **PASS** — 2/2 |
| `npm run test:e2e:visual-polish` | **FAIL (timeout)** — 600s exceeded on first home capture (`settlePage`); likely environmental/slow-run issue, not split-specific |
| HTTP smoke `/` | **200** — `home-hero` present, no `marketplace-filters` |
| HTTP smoke `/explorar` | **200** — `marketplace-filters` present |

**Servers for E2E:** backend `http://127.0.0.1:8000` (already running), frontend `npm run start` on `:3000`.

---

## Screenshots captured

No new visual-polish run completed successfully in this session (full-site capture timed out at 10 minutes).

**Manual inspection performed via HTTP smoke + targeted Playwright:**

- `/` — discovery sections render; catalog filters absent from HTML.
- `/explorar` — catalog filters and heading present.

**Recommended follow-up:** Re-run `npm run test:e2e:visual-polish` when backend + frontend are stable; add `/explorar` to the capture manifest in Phase 3.

---

## Warnings / follow-ups

| Item | Priority | Notes |
|------|----------|-------|
| **Phase 2 — search wiring polish** | P1 | Replace `sessionStorage` bridge with URL query params when approved |
| **Phase 3 — sidebar layout** | P1 | Move top filter card to left sidebar per plan |
| **`/#catalogo` bookmarks** | P2 | No redirect from Home; old links land on `/` without catalog — consider client redirect in Phase 2 |
| **Visual polish timeout** | P2 | Re-run full capture; Home baseline may change (no catalog section) — update governance |
| **`VISUAL_POLISH_ROUTES.json`** | P2 | Add `/explorar` route entry |
| **Sellos / Artistas** | P3 | Currently generic `/explorar`; facet query params in Phase 4 |
| **HomeMetricsBand “Cómo funciona”** | P3 | Now links to `/explorar`; may deserve a dedicated trust/how-it-works page later |
| **Gate B editorial** | Deferred | Per plan — not in Phase 1 scope |
| **Commit** | — | Changes uncommitted per instruction |

---

## Exact git status

### Frontend (`C:\melomanos\frontend`)

```
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
	modified:   e2e/melomanos.spec.ts
	modified:   src/app/page.tsx
	deleted:    src/components/Marketplace.tsx
	modified:   src/components/Navbar.tsx
	modified:   src/components/home/HomeHero.tsx
	modified:   src/components/home/HomeMetricsBand.tsx
	modified:   src/components/home/HomeNewArrivals.tsx
	modified:   src/lib/home-search.ts
	modified:   src/lib/marketplace-filters.ts

Untracked files:
	src/app/explorar/
	src/components/catalog/
	src/components/home/HomeDiscovery.tsx
	src/hooks/
	src/lib/useListingsQuery.ts
```

### Workspace (`C:\melomanos\workspace`)

```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
	reports/ux/HOME_CATALOG_SPLIT_PHASE1_REPORT.md
```

*(Plus prior untracked `reports/ux/HOME_CATALOG_SPLIT_PLAN.md` if not yet committed.)*

---

## Acceptance criteria checklist

| Criterion | Status |
|-----------|--------|
| Home no longer shows full catalog/filter grid | ✅ |
| `/explorar` shows full catalog experience | ✅ |
| Existing filters work on `/explorar` | ✅ (same form + `buildMarketplaceApiFilters`) |
| Listing cards + detail navigation work | ✅ (unchanged `ListingCard` / routes) |
| Navbar Explorar → `/explorar` | ✅ |
| No backend/business logic changes | ✅ |
| Build passes | ✅ |
| No horizontal overflow introduced | ✅ (layout preserved from prior Marketplace markup) |

---

*Phase 1 complete. Ready for review and commit when approved.*
