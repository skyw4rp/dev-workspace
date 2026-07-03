# UI Scale Polish Report — Melómanos Market

**Date:** 2026-07-03  
**Scope:** Frontend visual scale pass (marketplace-grade legibility)  
**Reference benchmark:** Discogs/Reverb-style header, search, cards, and controls  
**Verdict:** **PASS**

---

## Summary

Applied a token-driven UI scale polish across shared design system classes and high-traffic marketplace surfaces. The header, search bar, navigation actions, product cards, buttons, inputs, badges, and listing detail metadata are larger and more legible at desktop distance while preserving the warm ivory / black / gold Melómanos identity.

No backend, API, routing, or business logic changes were made.

---

## Files changed

| File | Changes |
|------|---------|
| `frontend/src/app/globals.css` | Added UI scale CSS variables; bumped buttons, inputs, search, badges, labels, editorial tokens |
| `frontend/src/components/icons/index.ts` | `ICON_SIZE_MD` 18→20px; `ICON_SIZE_NAV` 20→22px |
| `frontend/src/components/Navbar.tsx` | Taller header padding; larger nav text (15px token); wider/taller search; larger profile avatar & icons |
| `frontend/src/components/BrandLogo.tsx` | Slightly larger mark and wordmark |
| `frontend/src/components/ListingCard.tsx` | Larger artist/title/price hierarchy; standard button sizes; more card padding/gaps |
| `frontend/src/components/ListingDetailActions.tsx` | Removed `text-xs` button overrides; larger action buttons & error text |
| `frontend/src/components/DetailField.tsx` | Larger listing detail field labels and values |
| `frontend/src/components/Marketplace.tsx` | Larger catalog heading; filter form spacing; wider card grid gaps |
| `frontend/src/components/NotificationBell.tsx` | Matches `icon-btn` scale (40px); larger bell icon & badge text |

**Not modified:** `HomeHero.tsx`, `admin/page.tsx`, backend, workspace governance (except this report).

---

## Design tokens added (`globals.css`)

| Token | Value | Use |
|-------|-------|-----|
| `--text-nav` | 15px (0.9375rem) | Nav links, buttons, inputs, search |
| `--text-body` | 16px | Body reference |
| `--text-body-sm` | 14px | Secondary UI copy |
| `--text-caption` | 13px | Labels, eyebrows, metadata |
| `--text-badge` | 11px | Status/meta badges (was 10px) |
| `--control-height` | 44px (2.75rem) | Buttons, inputs, search |
| `--icon-nav` | 20px | Nav icon reference |
| `--icon-btn-size` | 40px | Icon button hit area |

Shared classes updated: `btn-*`, `icon-btn`, `input-field`, `input-search`, `label-field`, `badge-*`, `editorial-label`, `editorial-eyebrow`.

---

## Before/after observations

### Header / Navbar (compare `runs/20260703-1529` → `runs/20260703-1545`)

| Element | Before | After |
|---------|--------|-------|
| Center nav text | 13px | 15px (`--text-nav`) |
| Action links (“Vender vinilo”, etc.) | 11–13px mixed | 15px consistent |
| Search input | ~36px tall, 13px text, narrow | 44px min-height, 15px text, wider (up to 380px) |
| Search icon | 16px | 20px |
| Icon buttons (messages, favorites, bell) | 36×36px, 18px icons | 40×40px, 22px icons |
| Profile avatar | 36px | 40px |
| Mobile nav strip | 12px (`text-xs`) | 14px (`--text-body-sm`) |
| ⌘ K shortcut pill | Removed (prior microfix) | — |

### Product cards

| Element | Before | After |
|---------|--------|-------|
| Artist line | 12px uppercase | 14px semibold uppercase |
| Title | 16px | 18px / 20px (sm) |
| City | 14px | 15px |
| Price | 24–30px | 28px / 30px |
| Card actions | `text-xs` shrunk buttons | Full `btn-primary` / `btn-ghost` (44px) |
| Grid gap | 24px | 28–32px |

### Forms & catalog

| Element | Before | After |
|---------|--------|-------|
| Inputs / buttons (global) | 40px min-height, 14px text | 44px, 15px text |
| Filter form | Compact padding | `p-5 sm:p-7`, larger headings |
| Badges | 10px, tight padding | 11px, `px-2.5 py-1` |

### Listing detail

- `DetailField` labels 10px → 13px; values 14px → 15px
- Action row buttons use standard control height (no `text-xs` override)

---

## Validation commands run

```powershell
cd C:\melomanos\frontend
npm run build                    # PASS
npm run test:e2e:visual-polish   # PASS — 28 captures

cd C:\melomanos\workspace
py run_melomanos.py --no-wait --kill-stale   # stack ready for capture
```

**Note:** Full `npm run test:e2e` not re-run in this pass; build + visual-polish capture passed. Prior Gate A run: 37/37 E2E (one intermittent dispute/WebPay flake observed in header microfix session).

---

## Screenshots captured

| Run | Path | Notes |
|-----|------|-------|
| **After (this pass)** | `workspace/screenshots/visual-polish/runs/20260703-1545/` | 28 captures, post scale polish |
| Before reference | `workspace/screenshots/visual-polish/runs/20260703-1529/` | Pre-scale; includes header microfix baseline |

Compare especially: `home/logged-in-desktop-1440.png`, `listing-detail/logged-in-desktop-1440.png`, `login/login-desktop-1440.png`.

Screenshots are gitignored under `runs/` — not committed.

---

## Product logic unchanged confirmation

- No changes to `frontend/src/lib/api.ts`, auth, orders, payments, messages, or routes
- Navbar `href`s, search submit behavior, and session logic unchanged
- ListingCard favorite/buy flows unchanged
- `Marketplace.tsx` filter API mapping unchanged (visual/spacing only)

---

## Warnings & follow-up

1. **HomeHero frozen** — Hero section typography not scaled; may feel slightly smaller relative to new header/catalog. Address in Gate B if desired.
2. **Profile / orders / sell pages** — Benefit from global tokens but no page-specific pass; profile dense areas may still use local `text-xs` overrides.
3. **Home interior components** (`HomeMetricsBand`, `HomeNewArrivals`) — Not scaled in this pass.
4. **Commit bundling** — `Navbar.tsx` includes both header microfix (⌘ K removal, nav typography) and scale polish; recommend single commit: `Refine header search and navigation typography` or split if preferred.
5. **Human visual approval** — Screenshots are evidence only; Daniela/Ernesto sign-off still required per Visual Feedback Loop.

---

## Suggested commit message

```
Improve marketplace UI scale and legibility
```

Or combine with pending header microfix:

```
Refine header search and navigation typography
```

---

*Frontend visual-only pass. No backend files modified.*
