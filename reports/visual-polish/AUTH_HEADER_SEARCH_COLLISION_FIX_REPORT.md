# Authenticated Header Search Collision Fix Report

**Date:** 2026-07-03  
**Scope:** Desktop logged-in header layout regression  
**Verdict:** **PASS**

---

## Summary

Fixed the authenticated desktop header regression where the search input collapsed into a small circular pill when logged in. The root cause was `flex-1` + `min-w-0` on the search form combined with many `shrink-0` action elements — flexbox shrank the search below usable width, and `rounded-full` made it look like an icon button.

The search now lives in a dedicated flex child with **`min-w-[240px] lg:min-w-[260px]`** and **`flex-1`**, so it cannot collapse. Secondary chrome was tightened: truncated profile name, role label deferred to `2xl`, tighter nav padding at `lg`, and compact action link padding.

Logged-out header remains correct. Mobile nav strip pattern unchanged (search hidden below `md`).

---

## Root cause

| Factor | Effect |
|--------|--------|
| `NavbarSearch` used `min-w-0 flex-1` | Search was allowed to shrink to ~44px when actions competed for space |
| `input-search` uses `rounded-full` | At tiny width, the field rendered as a circle (magnifying glass only) |
| Logged-in cluster is wide | Vender vinilo + Compras y ventas + 3 icon buttons + profile chip + Salir (2xl) |
| All actions use `shrink-0` | Flex shrink was absorbed entirely by the search |

Logged-out state had only “Iniciar sesión”, so search kept ample width and looked fine.

---

## Files changed

| File | Repo | Change |
|------|------|--------|
| `frontend/src/components/Navbar.tsx` | `C:\melomanos\frontend` | Search wrapper min-width, profile constraints, responsive action/nav spacing |

**Not modified:** backend, auth logic, search dispatch, routes, `globals.css`.

---

## Layout fix (technical)

### Search wrapper (new)

```tsx
<div className="hidden min-w-[240px] flex-1 md:block lg:min-w-[260px]">
  <NavbarSearch />
</div>
```

`NavbarSearch` form is `w-full` only — flex growth/min-width owned by wrapper.

### Profile chip

- `shrink-0` + `max-w-[10rem]` (xl/2xl steps)
- Name truncated: `max-w-[5.5rem]` → `xl:max-w-[6.5rem]` → `2xl:max-w-[8rem]`
- “Coleccionista” label + chevron: `2xl` only

### Action links

- Remain `xl:inline-block` (required for E2E at 1440px viewport)
- Slightly tighter padding: `px-2.5` at xl, `px-3` at 2xl

### Nav links

- `lg:px-2 xl:px-3` to recover horizontal budget on medium desktop

---

## Before/after observations

Compare runs:

| State | Before (broken) | After (fixed) |
|-------|-----------------|---------------|
| Run folder | `runs/20260703-1630/` | `runs/20260703-1635/` |

### Logged-out desktop (`home/logged-out-desktop-1440.png`)

- **Before:** Wide search between nav and “Iniciar sesión” — good
- **After:** Unchanged — search still expands, placeholder readable

### Logged-in desktop (`home/logged-in-desktop-1440.png`)

- **Before:** Search collapsed to small circular magnifying-glass pill
- **After:** Full-width search field between nav and actions; placeholder visible; profile shows truncated name; icons + text actions accessible

### Logged-in mobile (`home/logged-in-mobile-390.png`)

- **Before/after:** Search hidden (`md` breakpoint); horizontal nav strip below header — no regression

---

## Validation commands run

```powershell
cd C:\melomanos\frontend
npm run build                    # PASS
npm run test:e2e:visual-polish   # PASS — 28 captures (after restoring xl action links)
```

**Note:** First visual-polish run failed because action links were temporarily `2xl:inline-block` while E2E login helper expects `nav-orders` visible at 1440px (`xl`). Restored to `xl:inline-block`; search min-width fix retained.

---

## Screenshots captured

**Latest run:** `workspace/screenshots/visual-polish/runs/20260703-1635/`

- Manifest: `workspace/screenshots/visual-polish/runs/20260703-1635/manifest.json`
- Key files: `home/logged-in-desktop-1440.png`, `home/logged-out-desktop-1440.png`, `home/logged-in-mobile-390.png`
- Gitignored — not committed

---

## Product logic unchanged confirmation

- `dispatchHomeSearch` / `scrollToCatalog` unchanged
- All `href`s, `data-testid`s, auth/session logic unchanged
- No backend or API changes

---

## Warnings & follow-ups

1. **Commit from frontend repo:** `cd C:\melomanos\frontend` — not `workspace`.
2. **1536px+ (2xl):** “Coleccionista” subtitle and chevron appear; full profile width at widest breakpoints.
3. **Very tight lg (1024–1279):** If overflow appears on real devices, consider hiding one nav label or deferring “Vender vinilo” text to `2xl` with an icon alternative.
4. **Bundle commits:** `Navbar.tsx` may include prior scale polish + search width changes — review full `git diff` before commit.

---

## Suggested commit message

```
Fix logged-in header search collapse on desktop
```

---

*Frontend layout-only fix.*
