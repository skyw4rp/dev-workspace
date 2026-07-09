# Visual Feedback Loop Control — Melómanos Market

**System:** AI Dev OS Visual Feedback Loop (VISUAL_FEEDBACK_LOOP)  
**Product:** Melómanos Market  
**Scope:** Visual QA workflow, evidence, and human approval — not product functionality

---

## Purpose

Instantiate the closed-loop visual QA workflow for Melómanos Market:

**Capture → Analyze → Plan → Implement → Validate → Re-capture → Package → Approve → Record**

This document governs how screenshot evidence, AI visual audits, repair gates, and human sign-off interact. It extends (does not replace) the Visual Polish Gate artifacts.

---

## Brand identity

| Field | Value |
|-------|--------|
| **Brand name** | Melómanos Market |
| **Direction** | Premium editorial vinyl marketplace |
| **Tone** | Electronic-vinyl community — DJs, diggers, collectors, labels |
| **Feel** | Warm ivory editorial; black/charcoal typography; sober gold/champagne accents; curated, niche, premium |

### Visual identity constraints

**Use:** warm ivory / off-white backgrounds, black/charcoal primary text, muted warm gray secondary text, gold editorial accents, intentional deep-black inverse callouts (`#080808`).

**Avoid:** purple, violet, fuchsia, neon, rave/festival styling, dark SaaS dashboard shells, startup UI patterns, heavy glow, dominant gradients outside approved inverse editorial cards.

---

## Approved design tokens

| Token | Hex | Usage |
|-------|-----|--------|
| Background | `#F7F3EA` | Page background (warm ivory) |
| Surface | `#FFFDF8` | Cards, modals, dropdowns |
| Text primary | `#0B0B0B` | Headlines, body primary |
| Text secondary | `#5E5950` | Muted metadata, labels |
| Placeholder | `#8A8479` | Input placeholders |
| Border | `#E4DED3` | Card and field borders |
| Gold accent | `#B68A2E` | Editorial accents, CTAs accent |
| Deep black | `#080808` | Approved dark editorial callouts only |
| Success | `#2F7D55` | Success states, Disponible badges |
| Danger | `#8A2D2D` | Error, destructive emphasis |

Shared UI classes live in `frontend/src/app/globals.css` — prefer extending these over ad-hoc styling during repair gates.

---

## Artifact paths

| Artifact | Path |
|----------|------|
| **Route manifest** | `workspace/VISUAL_POLISH_ROUTES.json` |
| **Visual status (living)** | `workspace/VISUAL_POLISH_STATUS.md` |
| **Visual polish control** | `workspace/VISUAL_POLISH_CONTROL.md` |
| **Feedback loop control (this file)** | `workspace/VISUAL_FEEDBACK_LOOP_CONTROL.md` |
| **Screenshot runs (generated)** | `workspace/screenshots/visual-polish/runs/` |
| **Approved screenshot evidence** | `workspace/screenshots/visual-polish/approved/` |
| **Design references (canonical)** | `workspace/design-references/` |
| **Route design references** | `workspace/design-references/routes/` |
| **Visual audit reports** | `workspace/reports/visual-audit/` |
| **Screenshot runbook** | `workspace/screenshots/visual-polish/README.md` |

### Canonical reference image

`workspace/design-references/melomanos_marketplace_reference.jpeg`

Route-specific references (when Daniela provides them) go under `workspace/design-references/routes/` using the naming pattern in the screenshot README.

---

## Feedback loop stages

| Stage | Owner | Output |
|-------|-------|--------|
| **1. Capture** | Automation or human | PNG screenshots in `runs/<YYYY-MM-DD-HHMM>/` + `manifest.json` |
| **2. Analyze** | AI visual audit + human | Drift classification per route/surface; findings in `reports/visual-audit/` |
| **3. Plan** | AI + human | Scoped repair gate (e.g. Gate A color, Gate B Home UX); no scope creep |
| **4. Implement** | Frontend only | Visual changes per gate constraints; no backend/business-logic changes unless explicitly scoped |
| **5. Validate** | CI + smoke | `npm run test:unit`, `npm run build`, `npm run test:e2e`, `py run_melomanos.py --check` |
| **6. Re-capture** | Automation | New run folder under `runs/` reflecting post-fix UI |
| **7. Package** | AI or human | Curated subset for review (route folders, manifest, optional zip) |
| **8. Approve** | Daniela / Ernesto | Explicit human sign-off; never inferred from tests or AI audit |
| **9. Record** | Workspace governance | Update `VISUAL_POLISH_STATUS.md`, approval log, copy approved evidence to `approved/` if committing |

---

## Drift taxonomy

Classify every finding with exactly one primary label:

| Label | Definition |
|-------|------------|
| **ON_SYSTEM** | Matches approved palette, typography, and editorial patterns |
| **MINOR_DRIFT** | Small spacing, rhythm, or density differences; non-blocking |
| **MAJOR_DRIFT** | Wrong palette branch, legacy styling dominant, or reference mismatch on primary surface |
| **LEGACY_STYLE_PRESENT** | Violet/purple/fuchsia, dark SaaS shell, neon, or prohibited patterns still visible |
| **OUT_OF_SCOPE** | Surface explicitly deferred (e.g. `/admin`); document but do not block customer-facing gates |
| **NEEDS_HUMAN_REVIEW** | Ambiguous, subjective, or approval-bound (e.g. copy tone, hero treatment) |

---

## Severity model

| Severity | Meaning | Approval impact |
|----------|---------|-----------------|
| **P0** | Blocks route PASS or gate closure | Must fix before human approval |
| **P1** | Should fix before design review sign-off | Fix in current gate unless explicitly deferred |
| **P2** | Cosmetic deferral OK | May ship with documented minor warnings |
| **OUT_OF_SCOPE** | Not evaluated for customer-facing PASS | Document in audit; not blocking |

Examples:

- P0: Legacy violet reputation panel on public listing detail
- P1: Navbar search using hardcoded hex instead of token
- P2: Hero micro-rhythm slightly tighter than reference
- OUT_OF_SCOPE: Admin violet dashboard styling

---

## Repair gate model

Repairs are scoped **gates**, not ad-hoc drive-by fixes.

| Gate | Scope | Protected |
|------|-------|-----------|
| **Gate A** | Full-site corporate color standardization | HomeHero frozen; no Home IA restructure |
| **Gate B** | Home UX / neuromarketing restructure (Daniela prompt) | HomeHero copy/layout/title color frozen unless explicitly reopened |
| **Route gates** | Single-route polish (listing detail, order detail, etc.) | Routes marked PASS in status doc |
| **Admin gate** | Internal admin restyle | Requires explicit authorization; default OUT_OF_SCOPE |

Gate rules:

1. One gate per implementation pass; document scope in audit report before coding.
2. No backend, API, auth, payment, order, or message logic changes in visual gates.
3. No route changes unless the gate explicitly includes IA work (Gate B only).
4. Re-capture after implement + validate before requesting human approval.

---

## Screenshot package rules

### Generated runs (`runs/`)

- Created by `npm run test:e2e:visual-polish` or manual capture per README.
- Folder pattern: `workspace/screenshots/visual-polish/runs/<YYYY-MM-DD-HHMM>/`
- Each run includes `manifest.json` (routes, viewports, dynamic IDs, skips, errors).
- **Not committed by default** — listed in `.gitignore`.
- Screenshots are **evidence**, not approval.

### Approved evidence (`approved/`)

- Curated PNGs copied here **only after explicit human approval** for a route or gate.
- May be committed as permanent approval record when Ernesto/Daniela authorize.
- Naming: `{route-slug}-{state}-desktop-1440.png`, `{route-slug}-{state}-mobile-390.png`, or gate-specific names documented in status.

### Packaging for review

When sending to Daniela/Ernesto:

1. Latest `runs/<timestamp>/` folder (or selected route subfolders).
2. `manifest.json` from that run.
3. Reference image path and any route-specific references from `design-references/routes/`.
4. Short audit summary with drift taxonomy + severity per route.

Optional: zip entire run folder (e.g. `melomanos-visual-review-<timestamp>.zip`) — zip files are not committed unless explicitly requested.

---

## Human approval rules

| Rule | Detail |
|------|--------|
| **Tests ≠ visual approval** | Passing unit, build, and E2E does not mark any route PASS. |
| **AI audit ≠ human approval** | AI screenshot analysis informs planning; Daniela/Ernesto sign-off is required for PASS. |
| **Explicit approval only** | Record approver, date, and evidence paths in `VISUAL_POLISH_STATUS.md` approval log. |
| **Route PASS is evidence-bound** | PASS applies to named screenshot baselines, not “latest code generally.” |
| **Protected blocks** | HomeHero approved block remains frozen unless explicitly reopened in writing. |

Approvers: Daniela (design), Ernesto (engineering/product gate).

---

## Evidence retention rules

| Location | Retention | Git |
|----------|-----------|-----|
| `runs/` | Keep locally for comparison; rotate old runs as needed | **Ignored** |
| Root-level ad-hoc PNGs in `visual-polish/` | Historical baselines (e.g. Home hero approved) | May be tracked when approved |
| `approved/` | Permanent human-approved evidence | **May commit** when explicitly selected |
| `reports/visual-audit/` | Audit and adoption reports | **Commit** governance reports |
| `design-references/` | Canonical and route references | Commit reference assets |

Do not delete governance evidence or overwrite approved baselines without updating status docs.

---

## AI screenshot audit rules

When performing an AI visual audit on a screenshot run:

1. Read `manifest.json` first — note skips, dynamic IDs, auth state per capture.
2. Compare each **in-scope** route to canonical reference and approved tokens.
3. Classify findings using drift taxonomy + severity.
4. Distinguish **APPROVED_INVERSE_EDITORIAL** dark cards (`#080808`) from **LEGACY_STYLE_PRESENT** violet/SaaS drift.
5. Mark `/admin` captures as **OUT_OF_SCOPE** unless gate explicitly includes admin.
6. Do not mark routes PASS in `VISUAL_POLISH_STATUS.md` — recommend status only.
7. Write audit output to `workspace/reports/visual-audit/<report-name>.md`.
8. Recommend next gate (e.g. Gate A, Gate B, route-specific) with file scope.

---

## Route-by-route approval rules

Route inventory and priorities: `VISUAL_POLISH_ROUTES.json`.  
Living status: `VISUAL_POLISH_STATUS.md`.

| Route | Priority | Default scope | Notes |
|-------|----------|---------------|-------|
| `/` | P0 | Customer-facing | **PASS** recorded for approved Home/Hero baselines only; HomeHero frozen |
| `/listings/[id]` | P0 | Customer-facing | Requires post-gate re-capture + human approval |
| `/orders/[id]` | P0 | Customer-facing | Dispute/checkout surfaces; separate state captures when testable |
| `/login`, `/sell`, `/favorites`, `/orders`, `/messages`, `/profile` | P1 | Customer-facing | NEEDS_SCREENSHOT_VERIFICATION until audit + approval |
| `/notifications` | P2 | Customer-facing | Page + bell dropdown are separate surfaces |
| `/admin` | P3 | **OUT_OF_SCOPE** | Legacy internal styling; capture optional for evidence only |

Per-route PASS checklist:

- [ ] Desktop (1440×900) and mobile (390×844) captures present
- [ ] AI audit: no P0 drift on primary surface
- [ ] Functional smoke PASS with changes
- [ ] Daniela or Ernesto explicit approval recorded
- [ ] Approved screenshots copied to `approved/` if committing evidence
- [ ] `VISUAL_POLISH_STATUS.md` and `VISUAL_POLISH_ROUTES.json` updated

---

## Capture automation

| Item | Value |
|------|--------|
| Command | `cd frontend && npm run test:e2e:visual-polish` |
| Prerequisite | `py run_melomanos.py --no-wait --kill-stale` (stack READY) |
| Spec | `frontend/e2e/visual-polish-screenshots.spec.ts` |
| Config | `frontend/playwright.visual-polish.config.ts` |
| Excluded from default E2E | Yes (`testIgnore` in `playwright.config.ts`) |

---

## Prohibited legacy patterns

Same as `VISUAL_POLISH_CONTROL.md` — do not reintroduce:

- Purple / violet / fuchsia gradients or dominant accents (customer-facing)
- Neon gradients and heavy glow
- Dark SaaS dashboard panels on public routes
- Generic marketplace / corporate SaaS voice where editorial is expected

**Approved exception:** Intentional `#080808` black/gold inverse editorial callouts (Home featured card, community card, cover placeholders) — not legacy drift.

---

## Related documents

| File | Purpose |
|------|---------|
| `VISUAL_POLISH_CONTROL.md` | Brand, palette, prohibited patterns, polish gate summary |
| `VISUAL_POLISH_ROUTES.json` | Machine-readable route inventory |
| `VISUAL_POLISH_STATUS.md` | Living gate status, debt, approval log |
| `screenshots/visual-polish/README.md` | Capture runbook |
| `reports/visual-audit/VISUAL_FEEDBACK_LOOP_ADOPTION_REPORT.md` | Adoption record for this capability |
| `MISSION_EXECUTION_GUIDE.md` | Bounded missions — Feedback Loop audits are typically TYPE A |
| `NEXT_ACTION_QUEUE.md` | Operational mission queue (starts with M-001) |

---

*Adopted: Visual Feedback Loop capability — workspace governance only.*
