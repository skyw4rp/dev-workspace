# Home + Catalog Split Plan — Melómanos Market

**Date:** 2026-07-03  
**Author role:** Product UX architecture / frontend lead (planning only)  
**Status:** PROPOSED — no implementation in this document  
**Aligns with:** Gate B (Home UX / neuromarketing restructure), Discogs-inspired IA without literal copy

---

## Executive summary

Melómanos Home currently renders **editorial discovery and the full listings catalog on one route** (`/`). The `Marketplace` component fetches listings, shows the hero when filters are empty, then always renders `#catalogo` with top filters and a grid. This makes Home feel like a catalog page with a hero attached—not a modern marketplace landing.

**Recommendation:** Split into two routes:

| Route | Purpose |
|-------|---------|
| `/` | Discovery / editorial landing (hero, curated rails, community, CTAs) |
| `/explorar` | Full catalog browse (left sidebar filters, result count, sort, grid) |

Reuse existing API (`GET /listings`), `ListingCard`, filter mapping logic, and most home section components. **Do not copy Discogs visually**—apply warm ivory, gold accent, editorial typography, and Chilean digger tone.

---

## Current state

### Route map (today)

| Path | File | Renders |
|------|------|---------|
| `/` | `frontend/src/app/page.tsx` | `<Marketplace />` only |
| `/listings/[id]` | `frontend/src/app/listings/[id]/page.tsx` | Listing detail |
| Other | login, sell, favorites, orders, messages, profile, admin | Unaffected |

There is **no** dedicated catalog route. Catalog lives at `/#catalogo` on Home.

### `Marketplace.tsx` responsibilities (monolith)

Single client component (`frontend/src/components/Marketplace.tsx`) currently owns:

1. **Listings fetch** — `getListings(applied)` via `ListingsFilters`
2. **Filter state** — form + `buildMarketplaceApiFilters()` from `marketplace-filters.ts`
3. **Navbar search bridge** — listens to `HOME_SEARCH_EVENT`, applies search filter
4. **Hero gate** — `showHero` when no filters applied (skip/search/city/status/genre empty)
5. **Home sections** (when `showHero`):
   - `HomeHero` (featured listing from same fetch)
   - `HomeMetricsBand`
   - `HomeNewArrivals` (first items from same fetch)
   - `HomeBenefitsStrip` + `HomeCommunityCard`
6. **Catalog section** — always visible `#catalogo`:
   - Top card filter form (`data-testid="marketplace-filters"`)
   - Loading/error/empty states
   - `ListingCard` grid (limit 20, no pagination UI)

### Home component inventory

| Component | Path | Role |
|-----------|------|------|
| `HomeHero` | `components/home/HomeHero.tsx` | **Frozen** (Daniela approved) — copy, layout, title color |
| `HomeTrustRow` | `components/home/HomeTrustRow.tsx` | Trust bullets inside hero |
| `HomeMetricsBand` | `components/home/HomeMetricsBand.tsx` | Marketing stats + confidence card |
| `HomeNewArrivals` | `components/home/HomeNewArrivals.tsx` | Horizontal preview rail |
| `HomeBenefitsStrip` | `components/home/HomeBenefitsStrip.tsx` | Seller/value props |
| `HomeCommunityCard` | `components/home/HomeCommunityCard.tsx` | Dark inverse editorial CTA |
| `ListingCard` | `components/ListingCard.tsx` | Shared grid card |
| `MarketplaceStats` | `components/MarketplaceStats.tsx` | Stats row (not wired in current Marketplace) |

### Navigation & deep links (today)

| Source | Target |
|--------|--------|
| Navbar “Explorar” | `/#catalogo` (`nav-marketplace`) |
| Navbar “Sellos”, “Artistas” | `/#catalogo` |
| Navbar “Nuevos ingresos” | `/#nuevos-ingresos` (section id on HomeNewArrivals) |
| Navbar search submit | `scrollToCatalog()` + `dispatchHomeSearch(query)` |
| `HomeHero` “Explorar vinilos” | `#catalogo` |
| `HomeMetricsBand` link | `#catalogo` |
| `HomeNewArrivals` “Ver todo” | `#catalogo` |

Bridge: `frontend/src/lib/home-search.ts` — custom event + `getElementById("catalogo")`.

### API & filters (today)

**Frontend** (`ListingsFilters` in `api.ts`):

`skip`, `limit`, `search`, `city`, `genre`, `min_price`, `max_price`, `status`

**Backend** (`GET /listings`) already supports **more** than the UI exposes:

- `artist`, `genre`, `subgenre`, `city`, `min_price`, `max_price`, `min_year`, `max_year`, `status`, `search`
- `sort_by`: `created_at`, `price_clp`, `year`, `title`, `artist`
- `order`: `asc` | `desc`
- `total` in list response (for result count)

**Gap:** Frontend merges “estilo/subgénero” into `search` string (`marketplace-filters.ts`); backend has dedicated `genre` / `subgenre` params. Sort/pagination not wired in UI.

### Tests & governance

| Asset | Catalog dependency |
|-------|-------------------|
| `e2e/melomanos.spec.ts` | `homepage loads marketplace` expects `marketplace-filters` on `/` |
| `e2e/visual-polish-screenshots.spec.ts` | Captures `/` as home surface |
| `VISUAL_POLISH_ROUTES.json` | Home PASS tied to hero; dependencies include Marketplace catalog |
| `VISUAL_SCREENSHOT_AUDIT` | Gate B items: section reorder, catalog chips, community block |

### Visual / brand constraints

- Warm ivory `#F7F3EA`, surface `#FFFDF8`, gold `#B68A2E`, charcoal text
- `HomeHero` **frozen** until explicit reopen
- Admin out of scope
- Editorial, premium, electronic-vinyl community—not generic Discogs clone

---

## Proposed architecture

### Information architecture (Discogs-inspired, Melómanos-adapted)

```
┌─────────────────────────────────────────────────────────────┐
│  GLOBAL NAV: Logo | Discovery links | Search | Account        │
├─────────────────────────────────────────────────────────────┤
│  HOME (/)          │  EXPLORE (/explorar)                    │
│  ─────────────     │  ──────────────────                     │
│  Hero (frozen)     │  Page header + result count             │
│  Trust / metrics   │  ┌──────────┬─────────────────────────┐ │
│  Curated rails     │  │ Sidebar  │ Toolbar: sort + view      │ │
│  Community CTA     │  │ filters  │ ListingCard grid          │ │
│  Footer-ish blocks │  │          │ Pagination                │ │
│  NO full catalog   │  └──────────┴─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Route map (proposed)

| Route | Page file | Primary component | Purpose |
|-------|-----------|-------------------|---------|
| `/` | `app/page.tsx` | `HomeDiscovery` (new) | Editorial landing |
| `/explorar` | `app/explorar/page.tsx` (new) | `CatalogExplore` (new) | Full browse |
| `/listings/[id]` | unchanged | — | Detail |
| `/#catalogo` | — | **Redirect or alias** | `301`/client redirect → `/explorar` (preserve bookmarks) |

**Optional later:** `/explorar?search=…&genre=…&sort=price_clp&order=asc` — URL-synced filters for shareable searches (frontend-only query parsing).

### Navbar link map (proposed)

| Label | Current | Proposed |
|-------|---------|----------|
| Explorar | `/#catalogo` | `/explorar` (active when on explore) |
| Sellos | `/#catalogo` | `/explorar?label=…` or genre facet (phase 2) |
| Artistas | `/#catalogo` | `/explorar` + artist browse mode (phase 2) |
| Nuevos ingresos | `/#nuevos-ingresos` | `/` hash `#nuevos-ingresos` **or** `/explorar?sort=created_at` |
| Guía del digger | `/#guia-digger` | `/` section or `/guia` (future) |
| Header search | scroll + event on `/` | Navigate to `/explorar?q=…` (or apply if already on explore) |

`homeActive` for Explorar: pathname === `/explorar`, not `/`.

---

## Component impact map

### Reuse as-is

| Component / module | Use on |
|--------------------|--------|
| `ListingCard` | `/explorar` grid |
| `buildMarketplaceApiFilters` / extended variant | `/explorar` sidebar |
| `getListings` | Both (home curated fetch + explore) |
| `HomeHero`, `HomeTrustRow` | `/` only — **no structural change to hero block** |
| `HomeCommunityCard`, `HomeBenefitsStrip` | `/` |
| `globals.css` tokens, `input-field`, `card-surface`, badges | Both |

### Refactor / split from `Marketplace.tsx`

| New module | Extracted from | Responsibility |
|------------|----------------|----------------|
| `HomeDiscovery.tsx` | Marketplace hero branch | Fetch **small** listing set for featured + new arrivals only; render home sections; **no catalog grid** |
| `CatalogExplore.tsx` | Marketplace `#catalogo` branch | Sidebar filters, toolbar, grid, pagination |
| `CatalogFilterSidebar.tsx` | Filter form fields | Left column; sticky on desktop |
| `CatalogResultsToolbar.tsx` | New | Result count, sort select, optional view toggle |
| `useCatalogFilters.ts` | Marketplace state | Shared hook: form, applied filters, URL sync |
| `CatalogListingGrid.tsx` | Grid + states | Loading, error, empty, cards |

### Deprecate / replace

| Item | Action |
|------|--------|
| `Marketplace.tsx` | Remove after split; or thin re-export during migration |
| `#catalogo` section id | Move to `/explorar` or keep redirect anchor on Home CTA targets |
| `HOME_SEARCH_EVENT` on Home only | Replace with router navigation to `/explorar` + query |
| `scrollToCatalog()` | Replace with `router.push('/explorar?…')` |

### Files touched (implementation estimate)

| Area | Files |
|------|-------|
| New routes | `app/explorar/page.tsx`, optional `app/explorar/layout.tsx` |
| New components | `components/catalog/*`, `components/home/HomeDiscovery.tsx` |
| Modified | `app/page.tsx`, `Navbar.tsx`, `home-search.ts`, `HomeHero.tsx` (CTA hrefs only—coordinate with frozen hero policy), `HomeMetricsBand`, `HomeNewArrivals` |
| API client | `api.ts` — extend `ListingsFilters` with `sort_by`, `order`, `artist`, `subgenre`, `min_year`, `max_year` (types only; backend exists) |
| Tests | `e2e/melomanos.spec.ts`, visual-polish spec, `marketplace-filters.test.ts` |
| Governance | `VISUAL_POLISH_ROUTES.json`, status docs |

**HomeHero note:** Daniela approved copy/layout/title color. Changing CTA `href` from `#catalogo` to `/explorar` is **navigation only**—recommend explicit micro-approval or document as allowed href update without copy/layout changes.

---

## Home section proposal (`/`)

### Keep on Home

| Section | Component | Notes |
|---------|-----------|-------|
| Hero | `HomeHero` | Frozen visual/copy; update CTA destination → `/explorar` |
| Trust row | `HomeTrustRow` | Inside hero |
| Metrics band | `HomeMetricsBand` | Marketing stats; link → `/explorar` |
| Nuevos ingresos rail | `HomeNewArrivals` | Curated horizontal gallery (6–8 items), not full catalog |
| Benefits | `HomeBenefitsStrip` | Seller/value editorial |
| Community | `HomeCommunityCard` | Approved inverse dark card |

### Remove from Home

| Piece | Current location | Move to |
|-------|------------------|---------|
| Full filter form | `#catalogo` | `/explorar` sidebar |
| Full listing grid (20+) | `#catalogo` | `/explorar` |
| “Catálogo completo” heading block | `#catalogo` | `/explorar` page header |
| `data-testid="marketplace-filters"` | Home | `/explorar` only |

### Add on Home (Gate B / Daniela brief — phased)

Align with prior audit “Gate B” items; **not all required for MVP split**:

| Section | Purpose | Priority |
|---------|---------|----------|
| “Un lugar pensado para la escena” | Community/editorial depth | P1 (Gate B) |
| Seller CTA before catalog entry | Neuromarketing | P1 |
| Quick explore chips | Genre/style entry points → `/explorar?genre=…` | P2 |
| “Explora el catálogo” editorial band | Bridge to explore route | P1 |
| Footer trust / app / community links | Discogs-style footer (Melómanos tone) | P2 |

### Home data fetching (decoupled)

- **Do not** use “no filters = show hero + full catalog” coupling.
- Home fetches: `limit: 8–12` for featured + new arrivals only (`sort_by=created_at` or curated pick).
- Explore page owns paginated full catalog fetch.

### Proposed Home vertical order (MVP split)

1. `HomeHero` + trust  
2. `HomeMetricsBand`  
3. `HomeNewArrivals` (`id="nuevos-ingresos"`)  
4. **New:** `HomeExploreEntry` — single editorial row + CTA “Explorar catálogo” → `/explorar`  
5. `HomeBenefitsStrip` + `HomeCommunityCard` (grid)  
6. Optional Gate B blocks after human approval  

---

## Explore / catalog page proposal (`/explorar`)

### Desktop layout (≥1024px)

```
┌──────────────────────────────────────────────────────────────┐
│  Explorar vinilos          [breadcrumb optional]              │
│  Pressings electrónicos…                                      │
├──────────────┬───────────────────────────────────────────────┤
│  FILTROS     │  142 resultados    Ordenar: [Más recientes ▾] │
│  (sticky)    │  ─────────────────────────────────────────────  │
│              │  ┌─────┐ ┌─────┐ ┌─────┐                      │
│  Búsqueda    │  │Card │ │Card │ │Card │                      │
│  Ciudad      │  └─────┘ └─────┘ └─────┘                      │
│  Género      │  … pagination …                               │
│  Estilo      │                                               │
│  Precio      │                                               │
│  Año         │                                               │
│  Estado      │                                               │
│  [Buscar]    │                                               │
│  [Limpiar]   │                                               │
└──────────────┴───────────────────────────────────────────────┘
```

- **Sidebar width:** ~260–300px fixed; `card-surface` or flat ivory panel with `border-border`
- **Main:** `flex-1 min-w-0`; grid `sm:2 lg:3` columns (reuse current gaps from scale polish)
- **Sticky sidebar:** `lg:sticky lg:top-[header-height]`

### Toolbar

| Control | Behavior |
|---------|----------|
| Result count | `data.total` from API — “{n} vinilos” |
| Sort | Select: Más recientes (`created_at desc`), Precio ↑↓, Año, Artista, Título — maps to existing API |
| View (optional P2) | Grid / compact list — grid only for MVP |
| Active filter chips | Removable pills above grid (mobile-friendly summary) |

### Mobile layout (<1024px)

| Pattern | Behavior |
|---------|----------|
| Filters | **Sheet/drawer** or full-screen modal — “Filtros (3)” button in toolbar |
| Search | Can remain in navbar (navigate to `/explorar?q=`) **plus** in filter sheet |
| Grid | 1–2 columns |
| Sort | Dropdown in toolbar row |
| No horizontal overflow | `min-w-0`, drawer instead of sidebar column |

### Filter redesign (Melómanos, not Discogs)

| Discogs pattern | Melómanos adaptation |
|-----------------|----------------------|
| Dense gray sidebar | Warm ivory surface, gold focus rings, editorial labels |
| Many faceted checkboxes | Start with existing fields; add facets incrementally |
| Generic sans | Existing Geist + `editorial-label` / `label-field` |
| Dark chrome | Light `card-surface` sidebar, `border-border` dividers |
| Applied filter bar | Gold-accent chips on ivory (`badge-gold` / muted variants) |

**MVP filter fields** (map to API):

- Búsqueda → `search`
- Ciudad → `city`
- Género → `genre` (use API param, stop merging into search)
- Estilo / subgénero → `subgenre` or `search` fallback
- Precio min/max → `min_price`, `max_price`
- Año min/max → `min_year`, `max_year` (backend ready; UI new)
- Estado → `status` (Disponible / Reservado / Vendido labels)

### Pagination

- Backend supports `skip` + `limit` + `total`
- Add “Cargar más” or numbered pages on `/explorar` (frontend only)
- Home rail does **not** paginate

---

## Can `Marketplace` be reused on `/explorar`?

**Partially — not as a single component.**

| Piece | Reusable? |
|-------|-----------|
| Filter form fields + `buildMarketplaceApiFilters` | Yes — extract to sidebar |
| `getListings` + state machine | Yes — extract to `useCatalogFilters` |
| Listing grid + cards | Yes — verbatim |
| Hero + `showHero` gate | **No** on `/explorar` |
| Monolithic `Marketplace` | **Split required** |

**Recommended:** Create `CatalogExplore` from catalog half of `Marketplace`; create `HomeDiscovery` from hero half. Share hook + filter builder; do not duplicate API calls logic.

---

## Implementation phases

### Phase 0 — Planning & approval (this document)

- [ ] Product/Daniela sign-off on IA split
- [ ] Confirm HomeHero CTA href change allowed
- [ ] Update `VISUAL_POLISH_ROUTES.json` with `/explorar`

### Phase 1 — Route skeleton (small PR)

- Add `app/explorar/page.tsx` with extracted catalog UI (move grid + filters)
- Slim `app/page.tsx` to home sections only (no grid)
- Feature parity: same filters, same 20 listings, top form → sidebar layout can wait one commit

**Validation:** build, E2E homepage test updated, manual `/` and `/explorar`

### Phase 2 — Navigation & search wiring

- Navbar links → `/explorar`
- `home-search.ts` → `router.push('/explorar?search=…')`
- Home CTAs → `/explorar`
- Optional: redirect `/#catalogo` → `/explorar` on Home mount

**Validation:** E2E, visual-polish capture for new route

### Phase 3 — Explore UX (Discogs-inspired layout)

- Left sidebar filters (desktop)
- Mobile filter drawer
- Result count + sort toolbar
- Extend `ListingsFilters` + `buildMarketplaceApiFilters` for `sort_by` / `order`

**Validation:** filter unit tests, explore E2E, screenshots

### Phase 4 — URL-synced filters (optional)

- `useSearchParams` on `/explorar`
- Shareable URLs, navbar search prefill from query

### Phase 5 — Home Gate B editorial (separate gate)

- Daniela blocks: community depth, chips, section reorder
- **Do not** mix with Phase 1–3 unless approved
- Re-capture Home PASS baselines

### Phase 6 — Governance & cleanup

- Remove `Marketplace.tsx` monolith
- Update workspace reports, visual audit route table
- Deprecate `HOME_SEARCH_EVENT` if fully replaced

---

## Validation plan

| Layer | Checks |
|-------|--------|
| Unit | `marketplace-filters.test.ts` extended for sort/genre split |
| Build | `npm run build` |
| E2E | Update `homepage loads marketplace` → hero-only assertions on `/`; add `explorar loads catalog` with `marketplace-filters` |
| Visual polish | Add `/explorar` to `visual-polish-screenshots.spec.ts` manifest |
| Smoke | `py run_melomanos.py --check` |
| Manual | Logged-in/out header at 1440 + 390; filter drawer mobile |
| Governance | `VISUAL_POLISH_STATUS.md` — Home PASS scope shrinks to discovery-only |

---

## Risks and mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **E2E `marketplace-filters` on `/`** | High | Update test in same PR as split; split CI gate |
| **Broken `/#catalogo` bookmarks** | Medium | Client redirect on Home; keep temporary `id="catalogo"` anchor or document breaking change |
| **Navbar search behavior change** | Medium | If not on `/explorar`, navigate with query; if on explore, apply filter in place |
| **Duplicated fetch logic** | Medium | Single `useCatalogFilters` hook shared |
| **HomeHero frozen policy** | Medium | Only change `href` targets; no copy/layout; get Daniela ack |
| **SEO** | Low–Medium | Add `/explorar` title + meta description; Home stays primary brand landing |
| **Visual regression** | Medium | New screenshot route; re-approve Home without catalog |
| **Mobile header crowding** | Low | Explore page doesn’t add header items |
| **Backend change assumed** | Low | Sort/year/artist params **already exist** — frontend wiring only |
| **Gate B scope creep** | High | Keep MVP split separate from Daniela neuromarketing blocks |
| **Sellos/Artistas nav stubs** | Low | Phase 2: link to `/explorar` with query; Phase 4: real facets |
| **Pagination absent today** | Medium | Users see 20 items; add pagination in Phase 3 |
| **Filter semantics change** | Medium | Document genre vs search merge change; update tests |

---

## Final recommendation

**Proceed with the Home / Catalog split** as the primary Gate B structural change:

1. **`/` = discovery landing** — hero (frozen), metrics, new arrivals rail, benefits, community; **no full catalog**.
2. **`/explorar` = marketplace browse** — sidebar filters, result count, sort, grid, pagination.
3. **Refactor `Marketplace.tsx`** into `HomeDiscovery` + `CatalogExplore` with a shared filter hook; **reuse** `ListingCard` and existing API.
4. **Wire navigation** globally to `/explorar`; replace hash + custom-event search bridge with router + query params.
5. **Implement in 3–4 small PRs** (skeleton → nav → explore layout → URL sync); keep Daniela editorial sections for a follow-up Gate B PR.
6. **Do not copy Discogs** visually—use Melómanos ivory/gold editorial system for sidebar and toolbar.

This aligns with Discogs’ **mental model** (Home ≠ Explore) while preserving Melómanos’ approved hero, community card, and warm marketplace identity.

---

## Related artifacts

| Document | Relevance |
|----------|-----------|
| `workspace/reports/visual-audit/VISUAL_SCREENSHOT_AUDIT_20260703-1208.md` | Gate B deferred items |
| `workspace/VISUAL_FEEDBACK_LOOP_CONTROL.md` | Gate B definition |
| `workspace/VISUAL_POLISH_ROUTES.json` | Route inventory update needed |
| `workspace/reports/visual-polish/UI_SCALE_POLISH_REPORT.md` | Card/grid scale tokens for explore |

---

*Planning document only. No files were modified in the frontend or backend repositories.*
