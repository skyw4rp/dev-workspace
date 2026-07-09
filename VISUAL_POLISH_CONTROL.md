# Visual Polish Control — Melómanos Market

**System:** AI Dev OS Visual Polish Gate  
**Product:** Melómanos Market  
**Scope:** Visual polish and editorial consistency only — not product functionality

---

## Brand identity

| Field | Value |
|-------|--------|
| **Brand name** | Melómanos Market |
| **Direction** | Premium editorial vinyl marketplace |
| **Tone** | Music community — DJs, diggers, collectors, labels |
| **Feel** | Warm ivory editorial system; black/gold premium identity; collector culture — not generic SaaS |

---

## Approved palette

| Token | Hex | Usage |
|-------|-----|--------|
| Background | `#F7F3EA` | Page background (warm ivory) |
| Surface | `#FFFDF8` | Cards, modals, dropdowns |
| Text primary | `#0B0B0B` | Headlines, body primary |
| Text secondary | `#5E5950` | Muted metadata, labels |
| Placeholder | `#8A8479` | Input placeholders |
| Border | `#E4DED3` | Card and field borders |
| Gold accent | `#B68A2E` | Editorial accents, CTAs accent |
| Deep black | `#080808` | Approved dark editorial callouts (hero featured card, etc.) |
| Success | `#2F7D55` | Success states, badges |
| Danger | `#8A2D2D` | Error, destructive emphasis |

---

## Shared UI classes (extend, do not compete)

When polishing surfaces, prefer existing shared classes in `frontend/src/app/globals.css`:

- `btn-primary`, `btn-ghost`, `btn-danger-ghost`, `icon-btn`
- `input-field`, `label-field`
- `card-surface`, `card-surface-hover`, `dropdown-panel`
- `editorial-eyebrow`, `editorial-label`
- `badge-neutral`, `badge-gold`, `badge-success`, `badge-danger`, `badge-muted`, `badge-amber`
- `transition-ui`, `focus-ring`

---

## Prohibited legacy patterns

Do **not** reintroduce or leave dominant use of:

- Purple / violet / fuchsia gradients or accents (except documented OUT_OF_SCOPE internal routes)
- Neon gradients and heavy glow effects
- Dark SaaS dashboard panels (`#08060d`, `#0a0810`, zinc-on-black low-contrast shells)
- Generic marketplace / corporate SaaS language where editorial voice is expected
- Mixed icon families (unicode hearts, inconsistent stroke weights)
- Ad-hoc one-off button, input, badge, or card styling when shared classes exist

**Approved exception:** Intentional black/gold editorial callouts aligned with the Home reference — not purple/neon SaaS styling.

---

## Reference image

| Field | Value |
|-------|--------|
| **Canonical path** | `workspace/design-references/melomanos_marketplace_reference.jpeg` |
| **Legacy duplicate** | `workspace/design_references/` (underscore) — same asset may exist here; **do not use for gate sign-off**. Canonical path is `design-references/` (hyphen). Do not delete the duplicate unless explicitly requested. |

Screenshot captures for gate review live in:

`workspace/screenshots/visual-polish/`

See `workspace/screenshots/visual-polish/README.md` for naming conventions.

---

## Human approval gate

| Rule | Detail |
|------|--------|
| **Tests ≠ visual approval** | Passing unit, build, and E2E tests does **not** mean visual gate PASS. |
| **Human sign-off required** | Daniela / Ernesto visual approval is required before marking any route **PASS** or closing the visual gate. |
| **Screenshot evidence** | Reference-match and route PASS require screenshots in `workspace/screenshots/visual-polish/` per `VISUAL_POLISH_ROUTES.json`. |
| **Functional gate is separate** | This system governs visual polish only. Product functionality requires a separate **Functional Smoke Gate** (`py run_melomanos.py --check` or full audit). |

---

## Gate workflow (summary)

1. **Adoption** — Control, routes, status, and screenshot folder exist (this document + companions).
2. **Implementation** — Visual changes in frontend only; no backend/business-logic changes.
3. **Capture** — Desktop (1440) and mobile (390) screenshots per route.
4. **Review** — Compare to reference and palette; update `VISUAL_POLISH_STATUS.md`.
5. **Human approval** — Daniela/Ernesto sign-off.
6. **PASS** — Route or gate marked PASS only after steps 3–5.

---

## Related artifacts

| File | Purpose |
|------|---------|
| `VISUAL_POLISH_ROUTES.json` | Route inventory, priority, status, screenshot requirements |
| `VISUAL_POLISH_STATUS.md` | Living gate status, debt, next actions |
| `VISUAL_FEEDBACK_LOOP_CONTROL.md` | Capture → approve evidence workflow |
| `UX_BRAND_POLISH_IMPLEMENTATION_PLAN.md` | Historical implementation plan (not a substitute for this control file) |
| `MISSION_EXECUTION_GUIDE.md` | Bounded missions (Visual Polish work is typically TYPE C) |
| `NEXT_ACTION_QUEUE.md` | Operational mission queue — does not grant route PASS |

---

*Last updated: adoption recovery — documentation scaffolding only.*
