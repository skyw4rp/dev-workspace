# Visual Polish Status — Melómanos Market

**Last updated:** 2026-07-10 (QUEUE-HYGIENE — latest run pointer + committed polish state)

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

**Home route status:** `PASS` — Daniela approved the current Home/Hero visual state after Hero V2 copy refinement and underline fix (2026-07-01). This route PASS applies to the **approved Home baseline screenshots only** (`home-hero-v2-underline-fix-*.png`). **Post–Phase 1 split (2026-07-03):** catalog/filters moved to `/explorar`; new Home captures in `runs/20260703-1759/` require Daniela/Ernesto review before updating PASS baseline. Do **not** extend Home PASS to post-split layout without human approval.

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
| `/` | P0 | **PASS** | Daniela approved Home/Hero (2026-07-01); PASS tied to approved baseline screenshots only; **post-split Home captures need review** (catalog removed) |
| `/explorar` | P0 | IN_REVIEW | Phase 1 catalog; dedicated visual-polish captures + M-012 sidebar polish committed (`9879842`); human review pending |
| `/login` | P1 | NEEDS_SCREENSHOT_VERIFICATION | |
| `/sell` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/favorites` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/listings/[id]` | P0 | IN_REVIEW | M-013 layout polish committed (`d74f34b`); human review pending |
| `/messages` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/notifications` | P2 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/orders` | P1 | NEEDS_SCREENSHOT_VERIFICATION | Auth required |
| `/orders/[id]` | P0 | IN_REVIEW | Dispute/checkout surfaces |
| `/profile` | P1 | IN_REVIEW | M-003 profile polish committed (`5857a75`); human review pending |
| `/admin` | P3 | OUT_OF_SCOPE | Legacy internal styling |

Full machine-readable inventory: `VISUAL_POLISH_ROUTES.json`

---

## Full-site screenshot coverage

| Field | Value |
|-------|--------|
| **Automation status** | `TOOLING_READY` |
| **Capture status** | `LATEST_RUN_AVAILABLE` — `runs/20260710-1411/` (frontend @ `9879842`; includes `/explorar` captures) |
| **Spec** | `frontend/e2e/visual-polish-screenshots.spec.ts` |
| **Config** | `frontend/playwright.visual-polish.config.ts` |
| **Output** | `workspace/screenshots/visual-polish/runs/<YYYY-MM-DD-HHMM>/` |
| **Manifest** | `manifest.json` per run |
| **Excluded from default E2E** | Yes (`testIgnore` in `playwright.config.ts`) |

Runbook: `workspace/screenshots/visual-polish/README.md`

**Note:** Automated screenshots are visual evidence only. They do **not** mark any route PASS and do not replace Daniela/Ernesto human approval.

---

## Known visual debt

1. **Logged-in Home screenshot** — Recommended second capture after demo login for navbar parity with reference (non-blocking; Home/Hero approved).
2. **Listing detail** — M-013 polish committed; awaiting Daniela/Ernesto human review (`IN_REVIEW`).
3. **Explore catalog** — M-012 sidebar polish + M-016 card polish committed; `/explorar?genre=` deep links do not auto-apply filters yet.
4. **Order detail / disputes** — Dispute/checkout surfaces need screenshot verification and human review.
5. **Admin route** — Legacy dark/violet internal styling (`OUT_OF_SCOPE`).
6. **Other routes** — Capture screenshots and run reference/system review per `VISUAL_POLISH_ROUTES.json`.

---

## Committed polish state (repos clean at `9879842`)

Frontend working tree is **clean**. Recent TYPE C commits on record (all **IN_REVIEW** until human PASS):

| Area | Frontend commit | Status |
|------|-----------------|--------|
| Profile | `5857a75` | IN_REVIEW |
| Listing card | `f029b83` | IN_REVIEW |
| Listing detail | `d74f34b` | IN_REVIEW |
| Explore filters sidebar | `9879842` | IN_REVIEW |

Functional smoke: **43/43 E2E**, build OK, `run_melomanos.py --check` OK. No route PASS extended beyond Home baseline.

---

## Next recommended actions

1. **Optional logged-in Home capture** — `home-desktop-1440.png` (authenticated) for navbar parity.
2. **Human review** — `/explorar`, `/listings/[id]`, `/profile` (polish committed; evidence in latest `runs/`).
3. **Order detail review** — Screenshot and approval for `/orders/[id]` dispute/checkout surfaces.
4. **Next TYPE C mission** — M-014 empty states (see `NEXT_ACTION_QUEUE.md`).
5. **Other routes** — Capture screenshots and run reference/system review per `VISUAL_POLISH_ROUTES.json`.

---

## Approval log

| Date | Route / Gate | Approver | Result | Notes |
|------|----------------|----------|--------|-------|
| 2026-07-01 | Adoption gate | AI Dev OS review | PASS WITH WARNINGS | Scaffolding versioned in workspace `main` |
| 2026-07-01 | Functional Smoke Gate | AI Dev OS review | PASS | 43/43 E2E at latest gate |
| 2026-07-01 | Home Reference Match | AI Dev OS review | PASS WITH MINOR WARNINGS | Screenshots captured; human approval pending |
| 2026-07-01 | Home `/` — Home/Hero | Daniela | **APPROVED** | Hero V2 copy + gold color emphasis; underline removed per micro-hotfix; approved screenshots: `home-hero-v2-underline-fix-*.png`. Route PASS applies to approved Home baseline only; non-Home route-specific components remain IN_REVIEW. |

---

## Related documents

- `VISUAL_POLISH_CONTROL.md` — Brand, palette, prohibited patterns, approval rules
- `VISUAL_POLISH_ROUTES.json` — Route inventory
- `workspace/screenshots/visual-polish/README.md` — Screenshot naming
