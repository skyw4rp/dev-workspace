# Visual Polish Status — Melómanos Market

**Last updated:** Home/Hero human approval recorded (Daniela)

---

## Gate summary

| Field | Value |
|-------|--------|
| **Current visual gate** | `HOME_APPROVED` |
| **Adoption status** | `COMPLETE` |
| **Visual Polish Adoption Gate** | `PASS WITH WARNINGS` |
| **Functional Smoke Gate** | `PASS` |
| **Reference image status** | `PRESENT` |
| **Canonical reference path** | `workspace/design-references/melomanos_marketplace_reference.jpeg` |
| **Screenshot baseline status** | `PRESENT` |
| **Home Reference Match Review** | `PASS WITH MINOR WARNINGS` |
| **Human approval status** | `APPROVED` for Home/Hero (Daniela) |

---

## Home screenshot baseline

| Capture | Path | Viewport |
|---------|------|----------|
| Desktop (approved) | `workspace/screenshots/visual-polish/home-hero-v2-underline-fix-desktop-1440.png` | 1440×900 (full page) |
| Mobile (approved) | `workspace/screenshots/visual-polish/home-hero-v2-underline-fix-mobile-390.png` | 390×844 (full page) |
| Desktop (Hero V2) | `workspace/screenshots/visual-polish/home-hero-v2-desktop-1440.png` | 1440×900 (full page) |
| Mobile (Hero V2) | `workspace/screenshots/visual-polish/home-hero-v2-mobile-390.png` | 390×844 (full page) |
| Desktop (initial baseline) | `workspace/screenshots/visual-polish/home-desktop-1440.png` | 1440×900 (full page) |
| Mobile (initial baseline) | `workspace/screenshots/visual-polish/home-mobile-390.png` | 390×844 (full page) |

Compared against: `workspace/design-references/melomanos_marketplace_reference.jpeg`

**Home route status:** `PASS` — Daniela approved the current Home/Hero visual state after Hero V2 copy refinement and underline fix (2026-07-01). This route PASS applies to the approved Home baseline screenshots only; non-Home route-specific components in shared or uncommitted files remain `IN_REVIEW`.

---

## Home Reference Match — minor warnings

1. **Logged-out navbar** — Screenshot captured unauthenticated (“Iniciar sesión”); reference shows logged-in Daniela profile, message icon, and notification badge. Environmental difference; logged-in Home screenshot recommended for parity.
2. **Confidence card density** — MM stamp + copy + link fit in compact `lg:h-28` band; slightly denser than reference.
3. **Hero micro-rhythm** — Improved vs prior builds; not pixel-perfect vs reference (minor air between trust row and metrics).
4. **New arrivals content** — Live API listings vs reference static mock cards (acceptable).

No P0 blockers identified. No legacy purple/neon/dark-dashboard on Home capture. Daniela approved with these minor warnings acknowledged.

---

## Route status snapshot

| Route | Priority | Status | Notes |
|-------|----------|--------|-------|
| `/` | P0 | **PASS** | Daniela approved Home/Hero (2026-07-01); PASS tied to approved baseline screenshots; non-Home components IN_REVIEW |
| `/login` | P1 | NEEDS_SCREENSHOT_VERIFICATION | |
| `/sell` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/favorites` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/listings/[id]` | P0 | IN_REVIEW | Uncommitted polish reported |
| `/messages` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/notifications` | P2 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/orders` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/orders/[id]` | P0 | IN_REVIEW | Dispute/checkout surfaces |
| `/profile` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/admin` | P3 | OUT_OF_SCOPE | Legacy internal styling |

Full machine-readable inventory: `VISUAL_POLISH_ROUTES.json`

---

## Known visual debt

1. **Logged-in Home screenshot** — Recommended second capture after demo login for navbar parity with reference (non-blocking; Home/Hero approved).
2. **Listing detail** — Active/uncommitted visual polish changes in frontend; not human-approved.
3. **Order detail / disputes** — Uncommitted polish on dispute section; WebPay UI needs screenshot verification.
4. **Admin route** — Legacy dark/violet internal styling (`OUT_OF_SCOPE`).
5. **Other routes** — No screenshot baseline beyond Home.

---

## Uncommitted product UI changes (record only)

**14 modified frontend files** — mixed approval scope. Daniela approved the current Home/Hero visual state; route `/` PASS is tied to the approved Home baseline screenshots. Non-Home route-specific components remain `IN_REVIEW`:

| File | Scope | Status |
|------|-------|--------|
| `src/components/home/HomeHero.tsx` | Home/Hero | **APPROVED** (Daniela, 2026-07-01) |
| `src/components/home/HomeMetricsBand.tsx` | Home | **APPROVED** (Daniela, 2026-07-01) |
| `src/app/listings/[id]/page.tsx` | Listing detail | IN_REVIEW |
| `src/components/DetailField.tsx` | Listing detail | IN_REVIEW |
| `src/components/DiggingScorePanel.tsx` | Shared / listing | IN_REVIEW |
| `src/components/ListingDetailActions.tsx` | Listing detail | IN_REVIEW |
| `src/components/ListingVideoSection.tsx` | Listing detail | IN_REVIEW |
| `src/components/Marketplace.tsx` | Home catalog + marketplace | IN_REVIEW |
| `src/components/MessageForm.tsx` | Messages / listing | IN_REVIEW |
| `src/components/OrderDisputeSection.tsx` | Order detail | IN_REVIEW |
| `src/components/SellerCard.tsx` | Listing detail | IN_REVIEW |
| `src/components/SellerReputationPanel.tsx` | Listing detail | IN_REVIEW |
| `src/components/TrustBadgePills.tsx` | Shared | IN_REVIEW |
| `src/components/VinylCover.tsx` | Listing detail | IN_REVIEW |

Functional Smoke Gate **PASS** with these changes present (37/37 E2E, build OK, `run_melomanos.py --check` OK). Home/Hero visual acceptance recorded; frontend commit of non-Home files remains blocked pending separate route approval.

---

## Next recommended actions

1. **Optional logged-in Home capture** — `home-desktop-1440.png` (authenticated) for navbar parity.
2. **Listing detail review** — Screenshot, reference match, and human approval for `/listings/[id]`.
3. **Order detail review** — Screenshot and approval for `/orders/[id]` dispute/checkout surfaces.
4. **Frontend commit** — Home/Hero-approved files may be committed when Ernesto scopes the commit; other route files await separate approval.
5. **Other routes** — Capture screenshots and run reference/system review per `VISUAL_POLISH_ROUTES.json`.

---

## Approval log

| Date | Route / Gate | Approver | Result | Notes |
|------|----------------|----------|--------|-------|
| 2026-07-01 | Adoption gate | AI Dev OS review | PASS WITH WARNINGS | Scaffolding versioned in workspace `main` |
| 2026-07-01 | Functional Smoke Gate | AI Dev OS review | PASS | 37/37 E2E with uncommitted UI |
| 2026-07-01 | Home Reference Match | AI Dev OS review | PASS WITH MINOR WARNINGS | Screenshots captured; human approval pending |
| 2026-07-01 | Home `/` — Home/Hero | Daniela | **APPROVED** | Hero V2 copy + gold color emphasis; underline removed per micro-hotfix; approved screenshots: `home-hero-v2-underline-fix-*.png`. Route PASS applies to approved Home baseline only; non-Home route-specific components remain IN_REVIEW. |

---

## Related documents

- `VISUAL_POLISH_CONTROL.md` — Brand, palette, prohibited patterns, approval rules
- `VISUAL_POLISH_ROUTES.json` — Route inventory
- `workspace/screenshots/visual-polish/README.md` — Screenshot naming
