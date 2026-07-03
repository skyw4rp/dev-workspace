# Visual Polish Screenshots — Melómanos Market

Capture directory for Visual Polish Gate evidence.  
Compare captures to: `workspace/design-references/melomanos_marketplace_reference.jpeg`

**Important:** Screenshots are visual evidence only. They do **not** constitute Daniela/Ernesto approval. Human sign-off is required per `workspace/VISUAL_POLISH_CONTROL.md`.

---

## Full-site screenshot automation

A Playwright workflow captures desktop and mobile full-page screenshots for all major routes.

| Item | Location |
|------|----------|
| Spec | `frontend/e2e/visual-polish-screenshots.spec.ts` |
| Helpers | `frontend/e2e/helpers/visual-polish-screenshots.ts` |
| Config | `frontend/playwright.visual-polish.config.ts` |
| Output | `workspace/screenshots/visual-polish/runs/<YYYY-MM-DD-HHMM>/` |
| Manifest | `workspace/screenshots/visual-polish/runs/<YYYY-MM-DD-HHMM>/manifest.json` |

The spec is **excluded** from default `npm run test:e2e` via `testIgnore` in `playwright.config.ts`.

### 1. Start Melómanos

```powershell
cd C:\melomanos\workspace
py run_melomanos.py --no-wait --kill-stale
```

Wait until backend and frontend are READY.

### 2. Run screenshot capture

```powershell
cd C:\melomanos\frontend
npm run build
npm run test:e2e:visual-polish
```

Equivalent:

```powershell
npx playwright test --config=playwright.visual-polish.config.ts
```

### 3. Find output

Latest run folder:

```
workspace/screenshots/visual-polish/runs/<timestamp>/
├── manifest.json
├── home/
├── login/
├── listing-detail/
├── sell/
├── favorites/
├── orders/
├── order-detail/          (skipped if no demo order)
├── messages/
├── notifications/
├── profile/
└── admin/                 (optional; may skip on error)
```

### Viewports

| Name | Size |
|------|------|
| Desktop | 1440 × 900 |
| Mobile | 390 × 844 |

All captures are full-page PNG screenshots.

### Auth

Uses existing Daniela demo login helper (`daniela.review@demo.melomanos.local`) via `loginDanielaViaUi`. Credentials come from `e2e/helpers/constants.ts` (env overrides supported).

### Dynamic routes

- **Listing detail:** first demo listing with cover (fallback: any listing). ID recorded in `manifest.json`.
- **Order detail:** first buying/selling order for Daniela demo user. Skipped with manifest note if none exist.

### Interactive states (when safe)

- Notifications dropdown open (navbar bell)
- Message form expanded on listing detail (authenticated)
- Admin panel after loading with `test-admin-key`

Checkout/WebPay query states are **not** captured (avoids unpredictable backend side effects).

---

## Sending screenshots to Daniela

1. Run the capture workflow above.
2. Open `manifest.json` in the latest `runs/<timestamp>/` folder — verify captures vs skips.
3. Zip or share the entire `runs/<timestamp>/` folder (or route subfolders needed).
4. Include:
   - `manifest.json`
   - route subfolders with desktop + mobile PNGs
   - note that captures reflect **current uncommitted UI** where applicable

Daniela can use these captures as input for new AI-generated visual references per page.

---

## Storing Daniela’s generated references

Place new reference images under:

```
workspace/design-references/
```

Suggested naming:

| Route | Reference filename |
|-------|-------------------|
| Home | `melomanos_home_reference.png` |
| Login | `melomanos_login_reference.png` |
| Listing detail | `melomanos_listing_detail_reference.png` |
| Sell | `melomanos_sell_reference.png` |
| … | `melomanos_<route-slug>_reference.png` |

Keep the canonical marketplace reference:

`workspace/design-references/melomanos_marketplace_reference.jpeg`

Do not overwrite approved baselines without updating `VISUAL_POLISH_STATUS.md`.

---

## Legacy single-file naming

Ad-hoc captures may still live at the folder root:

| Pattern | Example | Viewport |
|---------|---------|----------|
| `{route}-desktop-1440.png` | `home-desktop-1440.png` | Desktop ~1440px width |
| `{route}-mobile-390.png` | `home-mobile-390.png` | Mobile ~390px width |

### Route name slugs

| Route | Slug |
|-------|------|
| `/` | `home` |
| `/login` | `login` |
| `/sell` | `sell` |
| `/favorites` | `favorites` |
| `/listings/[id]` | `listing-detail` |
| `/messages` | `messages` |
| `/notifications` | `notifications` |
| `/orders` | `orders` |
| `/orders/[id]` | `order-detail` |
| `/profile` | `profile` |
| `/admin` | `admin` |

---

## Requirements

- PNG format preferred.
- Full-page or primary surface visible (no cropped CTAs).
- Capture after visual changes intended for review.
- Do not treat test PASS as visual approval — human sign-off required per `VISUAL_POLISH_CONTROL.md`.
