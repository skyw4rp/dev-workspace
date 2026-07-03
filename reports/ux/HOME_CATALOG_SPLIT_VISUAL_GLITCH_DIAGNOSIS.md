# Home + Catalog Split — Visual Glitch Diagnosis

**Date:** 2026-07-03  
**Last updated:** 2026-07-03 (Home visual stability — screenshot-confirmed)  
**Scope:** Home `/` only — no backend changes  
**Related:** Phase 1 split (`HOME_CATALOG_SPLIT_PHASE1_REPORT.md`)

---

## Summary

Home visual instability had **three layers**:

| Layer | Root cause | Fix |
|-------|------------|-----|
| **A** | Infinite `/listings` refetch loop | `useListingsQuery` filter stabilization |
| **B** | `HomeNewArrivals` deferred mount (494px CLS) | Reserved rail + stable placeholder cards |
| **C** | Post-load visual swaps (screenshot evidence) | Static hero card; initials-only rail covers; logo focus |

**Layer C (this pass)** matches captured screenshots:

1. **HomeHero** — featured card text jumped when API `featuredListing` replaced static placeholders (~300ms after load). **Not** auto-rotation (no interval/autoplay exists).
2. **HomeNewArrivals** — gray pulse skeletons → cards; then `VinylCover` attempted API images → **initials placeholder → blank `<img>` area** while loading/failing.
3. **BrandLogo** — browser programmatic focus on `/` navigation showed default `:focus` outline (no `outline-none` / `focus-visible` guard).

---

## Exact root cause (screenshot-aligned)

### 1. HomeHero featured card swap — **confirmed**

```tsx
// Before: HomeDiscovery passed API listing into HomeHero
const featuredListing = data?.items.find(...) ?? data?.items[0];
<HomeHero featuredListing={featuredListing} />
```

When `useListingsQuery` resolved, artist/title/city/price changed from frozen defaults to API values without user interaction.

- **Auto-rotate?** **No** — `slideIndex` is decorative only; no `setInterval`, no carousel autoplay.
- **Hydration mismatch?** **No** — console clean.

**Fix:** HomeHero uses **static frozen copy only** (`HERO_FEATURED` constant). No API wiring on Home.

### 2. HomeNewArrivals cover state swap — **confirmed**

Two transitions caused the “initials → blank” effect:

| Step | UI | Cause |
|------|-----|-------|
| t0 | Gray pulse skeleton blocks | `showSkeleton` empty state (no initials) |
| t1 | Cards with initials | `VinylCover` placeholder when `coverImageUrl` null |
| t2 | Blank square | `coverImageUrl` set → `<img>` renders before paint / broken URL empty area |

**Refetch/re-render loop?** **No** after Layer A fix — single API call; `loading` not toggled again after data set.

**Fix:**

- Replace gray skeletons with **same card component** + `RAIL_PLACEHOLDER_LISTINGS` (initials covers).
- Home rail **never passes `coverImageUrl`** — stable initials placeholder style (explorar/catalog unchanged).

### 3. Header/logo focus outline — **confirmed**

`BrandLogo` `<Link>` had no `outline-none` / `focus-visible` styling. Next.js navigation can focus the first header link → visible outline without user keyboard interaction.

**Fix:** `outline-none focus:outline-none focus-visible:ring-…` on logo link (keyboard focus preserved).

---

## Investigation checklist

| Question | Answer |
|----------|--------|
| HomeHero auto-rotating too quickly? | **No** — no autoplay |
| HomeNewArrivals refetching after mount? | **No** — one fetch |
| ListingCard placeholders switching fallbacks? | **Yes on Home rail** — skeleton → initials → blank img; fixed by initials-only rail |
| Loading toggled again after render? | **No** |
| Interval / carousel / hydration? | **No** — API-driven prop updates + cover URL swap + focus |

---

## Files changed

### Frontend (`C:\melomanos\frontend`)

| File | Change |
|------|--------|
| `src/lib/useListingsQuery.ts` | Stabilize filters (`useMemo` + serialized key) |
| `src/components/home/HomeDiscovery.tsx` | Remove `featuredListing` prop; static hero |
| `src/components/home/HomeHero.tsx` | Static `HERO_FEATURED` copy; remove API prop |
| `src/components/home/HomeNewArrivals.tsx` | Placeholder rail cards; no cover URLs on Home; no gray skeleton |
| `src/components/BrandLogo.tsx` | Suppress spurious `:focus` outline; keep `focus-visible` ring |

*(Phase 1 split files remain uncommitted.)*

### Workspace

| File | Change |
|------|--------|
| `reports/ux/HOME_CATALOG_SPLIT_VISUAL_GLITCH_DIAGNOSIS.md` | This report |

---

## Validation

| Command | Result |
|---------|--------|
| `npm run build` | **PASS** |
| `npm run test:unit` | **PASS** (12/12) |
| Split E2E (`homepage loads discovery`, `explorar page loads`) | **PASS** (2/2) |
| Listings API calls on `/` | **1** (no loop) |
| Hydration warnings | **None** |

**Manual / screenshot re-check:** After fresh `npm run build` + restart `next start` on port 3000:

- Hero featured card text should stay **Priku / Romanian Minimal EP** on load.
- New arrivals covers should stay **initials style** (no blank img flash).
- Logo should not show outline unless keyboard Tab focus.

---

## Visual-polish timeout (reference)

Original timeout was caused by Layer A refetch loop blocking `networkidle`. With Layer A fixed, `settlePage` completes in &lt;500ms on `/`. Re-run visual-polish after server restart to refresh Home baselines.

---

## Is commit safe now?

**Yes — recommended to commit as one frontend changeset** (Phase 1 split + all Home stability fixes):

1. Phase 1 route split (`/`, `/explorar`)
2. `useListingsQuery` loop fix
3. Home layout stability (rail placeholders, static hero, logo focus, initials-only rail covers)

**Do not commit** until Daniela re-screenshots Home PASS if governance requires visual sign-off.

Suggested message:

```
Split Home catalog to /explorar and stabilize Home load visuals

Move catalog to /explorar, fix listings refetch loop, reserve new-arrivals
layout, keep hero and rail covers visually stable on load, and suppress
logo focus outline on navigation.
```

---

## Residual notes (acceptable)

- When API data arrives, new-arrivals **text** (title/artist/price) updates once — cards keep same initials cover style; no blank image flash.
- Logged-in navbar may still briefly revalidate session on route change (separate from this pass; not screenshot focus).

---

## Exact git status

### Frontend

```
On branch master
Changes not staged + untracked: Phase 1 split + glitch fixes
(modified: HomeHero, HomeNewArrivals, HomeDiscovery, BrandLogo, Navbar, …)
(untracked: explorar/, catalog/, hooks/, useListingsQuery.ts)
```

### Workspace

```
Untracked: reports/ux/HOME_CATALOG_SPLIT_*.md
```

---

*Do not commit unless explicitly requested.*
