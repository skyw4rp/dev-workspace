# Header IA Refactor C1 Report

**Date:** 2026-07-03  
**Gate:** Header Navigation Architecture — C1 (two-row header, product nav cleanup, account menu)  
**Scope:** Frontend Navbar only; no backend, no HomeHero, no Admin, no C2 presets  

---

## Verdict

**PASS WITH WARNINGS**

Implementation and validation complete. Header visual state is **IN_REVIEW** — no route or header PASS without Daniela/Ernesto approval. C2 follow-ups documented below.

---

## Files modified

### Frontend product files

| File | Change |
|------|--------|
| `frontend/src/components/Navbar.tsx` | Two-row header (utility + product), account dropdown menu, product nav reduced to 3 links, responsive single search field |

### Frontend test files

| File | Change |
|------|--------|
| `frontend/e2e/helpers/auth.ts` | `openAccountMenu`, `expectLoggedInAccountNav`; login waits on account menu |
| `frontend/e2e/helpers/demo-daniela-login.ts` | Static import; account menu assertion after Daniela login |
| `frontend/e2e/helpers/payment.ts` | Session detection via `nav-account-menu` |
| `frontend/e2e/melomanos.spec.ts` | Header IA tests (logged-out/in product nav); login opens account menu |
| `frontend/e2e/demo-daniela-login.spec.ts` | Opens account menu before orders/sell assertions |

### Workspace governance/report files

| File | Change |
|------|--------|
| `workspace/reports/visual-audit/HEADER_IA_REFACTOR_C1_REPORT.md` | This report |
| `workspace/VISUAL_POLISH_ROUTES.json` | Navbar dependency note for two-row IA (C1) |

---

## Header structure implemented

```
┌─────────────────────────────────────────────────────────────┐
│ ROW 1 — Utility (border-b subtle)                           │
│  BrandLogo │ Search (responsive grid, single input) │ Actions│
├─────────────────────────────────────────────────────────────┤
│ ROW 2 — Product (nav-product-row)                           │
│  Explorar │ Nuevos ingresos │ Comunidad                     │
└─────────────────────────────────────────────────────────────┘
```

- **Row 1:** Brand → `/`, search (`home-search`), session utilities  
- **Row 2:** Stable public marketplace links — identical for logged-out and logged-in  

---

## Logged-out behavior

- **Row 1:** Brand, search, `Iniciar sesión` (`nav-login`)  
- **Row 2:** Explorar (`nav-marketplace`), Nuevos ingresos, Comunidad  
- No inbox, orders, profile, favorites, or messages exposed  
- No “Vender vinilo” in header (login-first pattern preserved elsewhere)  

---

## Logged-in behavior

- **Row 1:** Brand, search, notification bell, messages (`nav-messages`), favorites (`nav-favorites`), account menu trigger (`nav-account-menu`)  
- **Account dropdown** (`nav-account-dropdown`): Mi perfil (`nav-profile`), Compras y ventas (`nav-orders`), Vender vinilo (`nav-sell`), Salir (`nav-logout`)  
- **Row 2:** Same public product nav as logged-out  

---

## Mobile behavior

- CSS grid places brand + actions on row 1; full-width search on row 2 (mobile), inline center column (md+)  
- Single `home-search` input (no duplicate DOM nodes)  
- Product row: 3 links with horizontal scroll — no cramped 5-link strip  
- Logged-in utilities remain accessible (icons + account chip)  
- No hamburger menu introduced  

---

## Items removed from global header

| Removed | Former target | Future home (deferred) |
|---------|---------------|------------------------|
| Sellos | `/explorar` | C2 `/explorar` chips or catalog presets |
| Artistas | `/explorar` | C2 catalog presets |
| Guía del digger | `/#guia-digger` | Home editorial (`HomeBenefitsStrip`) |
| Compras y ventas (inline) | `/orders` | Account menu (C1) |
| Vender vinilo (inline) | `/sell` | Account menu (C1) |
| Salir (inline) | logout action | Account menu (C1) |

---

## Items deferred to C2

| Item | C1 behavior | C2 target |
|------|-------------|-----------|
| Nuevos ingresos | Routes to `/explorar` (no sort/filter preset) | `/explorar?sort=newest` or equivalent when supported |
| Sellos browse | Removed from header | `/explorar` label chip or preset |
| Artistas browse | Removed from header | `/explorar` label chip or preset |
| Guía del digger | Removed from header | Home editorial anchor or dedicated content |
| Comunidad deep link | Routes to `/` | Optional `#community` anchor if added safely on Home |

---

## E2E updates

- Added `openAccountMenu()` and `expectLoggedInAccountNav()` helpers  
- Login flows open account menu before asserting `nav-orders` / `nav-sell`  
- New tests: logged-out public product nav; logged-in product nav parity  
- All preserved test ids: `home-search`, `nav-marketplace`, `nav-login`, `nav-orders`, `nav-sell`, `nav-profile`, `nav-messages`, `nav-favorites`, `nav-logout`  
- New test ids: `nav-account-menu`, `nav-account-dropdown`, `nav-product-row`  

---

## Validation results

| Check | Result |
|-------|--------|
| `npm run test:unit` | **PASS** (12/12) |
| `npm run build` | **PASS** |
| `npm run test:e2e` | **PASS** (43/43) |
| `npm run test:e2e:visual-polish` | **PASS** (1/1) |
| `py run_melomanos.py --check` | **PASS** |

---

## Screenshot run path

`workspace/screenshots/visual-polish/runs/20260703-1938/`

Manifest: `workspace/screenshots/visual-polish/runs/20260703-1938/manifest.json`  
Captures include updated two-row header on Home (logged-out/in), Login, Sell, Orders, Favorites, Messages, Profile, Listing detail, Order detail, Admin.

**Not staged.** Human review required before updating route PASS status.

---

## Product logic impact

**None.** Navigation IA and layout only. Search routing (`/` → `/explorar`, in-catalog dispatch) unchanged. No backend, business logic, or Admin changes.

---

## HomeHero protection confirmation

**Confirmed.** `HomeHero.tsx` and `HomeDiscovery.tsx` were not modified. HomeHero test assertions unchanged and passing.

---

## Admin status

**Unchanged.** Admin panel E2E passes; no Admin files modified.

---

## Git Gate Review

### Frontend files safe to commit

- `frontend/src/components/Navbar.tsx`
- `frontend/e2e/helpers/auth.ts`
- `frontend/e2e/helpers/demo-daniela-login.ts`
- `frontend/e2e/helpers/payment.ts`
- `frontend/e2e/melomanos.spec.ts`
- `frontend/e2e/demo-daniela-login.spec.ts`

### Workspace files safe to commit

- `workspace/reports/visual-audit/HEADER_IA_REFACTOR_C1_REPORT.md`
- `workspace/VISUAL_POLISH_ROUTES.json` (dependency note only)

### Files that must NOT be committed

- `workspace/screenshots/visual-polish/runs/**` (including `20260703-1938/`)
- `workspace/screenshots/visual-polish/*.png`
- `workspace/screenshots/visual-polish/*.zip`
- `frontend/test-results/**`
- Any unapproved visual evidence

### Proposed frontend commit message

```
Refactor header navigation architecture
```

### Proposed workspace commit message

```
Record header IA refactor C1
```

---

**Awaiting explicit approval before commit/push.**
