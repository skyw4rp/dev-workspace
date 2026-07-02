# Visual Polish Screenshots — Melómanos Market

Capture directory for Visual Polish Gate evidence.  
Compare captures to: `workspace/design-references/melomanos_marketplace_reference.jpeg`

## Naming convention

| Pattern | Example | Viewport |
|---------|---------|----------|
| `{route}-desktop-1440.png` | `home-desktop-1440.png` | Desktop ~1440px width |
| `{route}-mobile-390.png` | `home-mobile-390.png` | Mobile ~390px width |

### Route name slugs

Use lowercase kebab-case derived from the route:

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

## Requirements

- PNG format preferred.
- Full-page or primary surface visible (no cropped CTAs).
- Capture after visual changes intended for review.
- Do not treat test PASS as visual approval — human sign-off required per `VISUAL_POLISH_CONTROL.md`.

## Subfolders (optional)

Organize by route if volume grows, e.g. `home/home-desktop-1440.png`.
