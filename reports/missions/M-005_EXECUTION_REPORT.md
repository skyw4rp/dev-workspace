# M-005 Execution Report — Listing Detail Polish Audit

**Mission:** M-005  
**Type:** TYPE A — Review Only  
**Date:** 2026-07-10  
**Executor:** Melómanos Market AI Dev OS Mission Executor  
**Frontend HEAD (observed):** `f029b83` — Polish listing card visual hierarchy  
**Workspace HEAD (observed):** `5c25072` — Record M-016 listing card polish  

---

## Verdict

**PASS_WITH_WARNINGS**

`/listings/[id]` is functionally strong (buy, favorite, message, seller trust, video, related grid) and on the ivory editorial system. Visual-polish evidence is **rich and current enough** for human review of the detail shell. UX debt is mainly **information hierarchy, Phase 1 navigation drift, and trust/CTA ordering** — not missing product capability. A bounded **TYPE C M-013** layout polish is safe next; do **not** touch buy/message/order logic.

---

## Mission scope confirmation

| Constraint | Honored |
|------------|---------|
| TYPE A review only | Yes |
| No frontend / backend / product code | Yes |
| No screenshot edits | Yes |
| No route PASS changes | Yes |
| No v0 | Yes |
| No commits / pushes | Yes |
| No M-013 implementation / no other mission | Yes |
| Only write path: this report | Yes |

---

## Context files read

| File | Role |
|------|------|
| `workspace/AI_CONTEXT.md` | Onboarding index |
| `workspace/STACK_CONSTRAINTS.md` | Stack + domain risk |
| `workspace/PROJECT_STATUS.md` | Living snapshot |
| `workspace/NEXT_ACTION_QUEUE.md` | M-005 / M-013 definitions |
| `workspace/MISSION_EXECUTION_GUIDE.md` | Mission pattern |
| `workspace/reports/missions/M-004_EXECUTION_REPORT.md` | Route matrix |
| `workspace/reports/missions/M-007_EXECUTION_REPORT.md` | Home/Explore split |
| `workspace/reports/missions/M-011_EXECUTION_REPORT.md` | Explorar capture |
| `workspace/reports/missions/M-016_EXECUTION_REPORT.md` | Listing card polish |
| `workspace/VISUAL_POLISH_CONTROL.md` | Editorial system |
| `workspace/VISUAL_POLISH_ROUTES.json` | `/listings/[id]` IN_REVIEW |
| `workspace/VISUAL_POLISH_STATUS.md` | Status snapshot |
| `workspace/VISUAL_FEEDBACK_LOOP_CONTROL.md` | Evidence loop |
| `frontend/src/app/listings/[id]/page.tsx` | Detail route |
| `frontend/src/components/ListingDetailActions.tsx` | CTAs |
| `frontend/src/components/SellerCard.tsx` | Seller trust |
| `frontend/src/components/DetailField.tsx` | Metadata rows |
| `frontend/src/components/ListingVideoSection.tsx` | Video block |
| `frontend/src/components/ListingCard.tsx` | Catalog consistency reference |
| `frontend/e2e/melomanos.spec.ts` | E2E coverage |
| `runs/20260710-1012/listing-detail/*` | Latest evidence (read-only) |

---

## Current listing detail state

**Route:** `/listings/[id]` (public, dynamic)  
**Visual status (routes JSON):** `IN_REVIEW` (P0)  
**Composition (top → bottom):**

1. Back link → `← Volver al catálogo` (`href="/"`)
2. Two-column grid: `VinylCover` hero + info column
3. Badge row (genre, subgenre, type, status)
4. **Title** (h1) → **Artist** (uppercase accent) → **Price** (4xl/5xl)
5. `DetailField` dl card (sello, género, subgénero, año, tipo, disco, funda, ciudad, estado)
6. `ListingDetailActions` (Favorito / Mensaje / Comprar + optional `MessageForm`)
7. `SellerCard` (reputation + compact Digging)
8. Collector notes section
9. `ListingVideoSection` (if video URL)
10. Related grid (`ListingCard` × up to 4) + “Ver todo →” link

**E2E:** buy creates order, favorite, message/contact-leak, Digging on seller card, cover image — strong functional coverage.

---

## Listing detail route score

**6 / 10**

| Strength | Weakness |
|----------|----------|
| Clear primary **Comprar** CTA; status-aware disabled states | Artist/title/price hierarchy inconsistent with polished `ListingCard` |
| Grading fields present (disco/funda) | Grading buried mid-metadata table, not buyer-first |
| Seller reputation + Digging visible | Trust block **below** CTAs — confidence comes late |
| Editorial ivory shell, no legacy purple | Metadata duplication (genre/status in badges + dl) |
| Rich visual-polish captures (incl. message form) | Phase 1 IA drift: back link + related link still point at Home/catalog-on-`/` |
| Related listings use shared card component | Mobile: long scroll before CTAs; expanded message pushes seller down |

Functional MVP quality is **good**; visual/marketplace scan quality is **moderate** — polish can improve without product redesign.

---

## Visual evidence status

| Evidence type | Exists? | Latest run | Stale? | Notes |
|---------------|---------|------------|--------|-------|
| Run logged-out desktop | Yes | `20260710-1012` | Partial | Manifest `gitSha=a9aeabb`; detail page unchanged since; related cards pre-M-016 (`f029b83`) |
| Run logged-out mobile | Yes | `20260710-1012` | Partial | Same as above |
| Run logged-in desktop/mobile | Yes | `20260710-1012` | Partial | Navbar/session surfaces captured |
| Message-form-expanded desktop/mobile | Yes | `20260710-1012` | Low | Useful for compose UX review |
| Root ad-hoc PNGs | Yes | `20260702` | Yes | `listing-detail-*.png` — not PASS evidence |
| Approved folder | No | — | N/A | `.gitkeep` only |

**Conclusion:** Evidence is **sufficient for M-013 planning and Daniela review** of the detail route. Recapture after M-013 recommended; not blocking TYPE C start.

---

## Information hierarchy assessment

| Element | Current prominence | Recommended prominence | Issue | Recommendation |
|---------|-------------------|------------------------|-------|----------------|
| Gallery/photos | High (hero left) | High | OK on desktop; mobile stacks first | Keep; optional subtle frame polish |
| Artist | Medium-low (below title, uppercase accent) | High-secondary | Inverted vs catalog cards (`editorial-label` artist → title) | Reorder: artist label → title (M-013) |
| Title | Highest (h1 3xl/4xl) | High | Competes with price | Slightly reduce or demote vs artist+price block |
| Price | Very high (4xl/5xl) | High | Oversized vs M-016 card treatment | Align scale with editorial marketplace rhythm |
| Record condition | Low (mid dl) | High for used listings | Buyer-critical signal buried | Promote near badges/price (compact grade row) |
| Sleeve condition | Low (mid dl) | High for used listings | Same | Pair with record grade above fold |
| Genre | High (badges + dl duplicate) | Medium | Triple repetition | Keep badges OR dl subset, not both |
| Label/year | Low (dl) | Low–medium | OK in secondary metadata | Collapse dl or group “Ficha técnica” |
| City/comuna | Low (dl + seller card) | Medium | Duplicated | City near price or seller header only |
| Seller | Medium (card below CTAs) | Medium-high **before** buy | Trust after action | Move compact seller summary above CTAs |
| Reserve CTA | N/A (uses Comprar → order) | — | Business flow | **Do not change** in TYPE C |
| Message CTA | Medium (ghost, equal width) | Medium | OK | Keep; polish spacing only |
| Favorite | Medium | Medium | OK | Keep |
| Description | Low (below fold) | Low–medium | OK placement | Minor typography only |
| Similar recommendations | Medium (bottom) | Medium | Link target wrong (`/?genre=`) | Point to `/explorar` filter pattern |

---

## Main UX problems

### P1 — Hierarchy & buyer scan

1. **Artist/title inversion** vs polished explore cards (M-016).  
2. **Grading not buyer-first** — VG/G grades are evaluation-critical but appear after nine dl rows.  
3. **Metadata noise** — genre, subgenre, and status appear in badges and again in the dl.

### P1 — Trust & CTA order

4. **Seller reputation below Comprar** — buyer commits before seeing full trust stack (reputation + Digging).  
5. **Mobile scroll depth** — metadata table + CTAs + seller + notes + video + related = very long page.

### P2 — Catalog consistency / Phase 1 IA

6. **Back link** `← Volver al catálogo` → `/` (catalog lives on `/explorar` since Phase 1; profile already fixed to Explorar).  
7. **Related “Ver todo →”** links to `/?genre=` instead of `/explorar`.  
8. **Related cards** now use M-016 polish while detail header/dl still uses older visual language — rhythm mismatch.

### P2 — Density

9. **SellerCard** stacks `SellerReputationPanel` + compact `DiggingScorePanel` — dense on mobile.  
10. **Three equal ghost/primary CTAs** — Comprar is rightmost on desktop (good) but not visually isolated enough on mobile stack.

### Out of scope (do not fix in TYPE C without TYPE F)

- Order creation / reservation rules (`createOrderFromListing`)  
- Message contact-leak rules  
- WebPay/checkout (order detail route)  
- Digging/reputation API semantics  

---

## Obvious fixes that do not require Daniela

| Fix | Type | Risk |
|-----|------|------|
| Back link → `/explorar` + copy “Volver a Explorar” | IA / presentational | LOW |
| Related link → `/explorar` with genre query | IA / presentational | LOW |
| Artist → title hierarchy aligned with ListingCard | Presentational | LOW |
| Compact grade row under price (Disco · Cover) | Presentational | LOW |
| Collapse/group dl; remove duplicate genre/status rows | Presentational | LOW |
| Move seller name + trust summary above CTA row | Layout | LOW–MEDIUM |
| Price type scale reduction | Presentational | LOW |
| SellerCard / DetailField spacing and editorial labels | Presentational | LOW |
| Recapture visual-polish after M-013 | TYPE D evidence | LOW |

---

## Items that require Daniela or human product decision

1. **Human visual PASS** for `/listings/[id]` — route remains IN_REVIEW.  
2. **Buy vs trust ordering** — moving seller above Comprar is recommended but is a marketplace UX judgment.  
3. **Whether Comprar should be sticky on mobile** — product/UX call (optional; higher scope).  
4. **Message-first vs buy-first emphasis** — current parity across three buttons; Daniela may want Comprar dominant on mobile only.  
5. **Related section cardinality** — four cards on mobile adds length; keep or reduce?  
6. **Video section prominence** for used listings — required by rules but visual weight is a judgment call.

---

## Recommended next mission

**M-013 — Product detail page layout (TYPE C)**

**Why exactly one:** M-005 confirms issues are **layout/hierarchy/IA**, not missing features or business-rule gaps. Evidence exists. M-013 is already queued and blocked on M-005 — this audit unblocks it. Do **not** run another TYPE A first. Do **not** do TYPE D only — capture is adequate; recapture comes **after** M-013.

### M-013 brief (proposed)

| Field | Value |
|-------|--------|
| **Goal** | Bounded listing detail layout polish: hierarchy, grading prominence, trust/CTA order, Phase 1 back/related links — without changing buy/message/favorite behavior |
| **Allowed scope** | `listings/[id]/page.tsx`, `DetailField.tsx`, `ListingDetailActions.tsx` (classes/layout only), `SellerCard.tsx` (density/chrome only), `ListingVideoSection.tsx` (spacing/copy chrome only) |
| **Forbidden scope** | `createOrderFromListing`, message rules, auth, API, backend, Navbar, HomeHero, Explore grid/filters, route PASS, pricing/reservation logic |
| **Likely files** | `page.tsx`, `DetailField.tsx`, `ListingDetailActions.tsx`, `SellerCard.tsx` (optional `ListingVideoSection.tsx`) |
| **Acceptance criteria** | Detail hierarchy matches M-016 card language; grading visible near price; seller trust before or integrated with CTAs; back/related links use `/explorar`; build + E2E pass; new visual-polish run path; IN_REVIEW pending human |
| **Validation required** | `npm run build`; `npm run test:e2e`; `npm run test:e2e:visual-polish`; `py run_melomanos.py --check` |
| **Screenshot recapture** | **Yes** — after implementation, new run under `runs/<ts>/listing-detail/` |
| **Stop conditions** | Any handler/API change; escrow/message rule edits; marking PASS; scope expands to full listing detail product redesign |

---

## Risks

| Risk | Severity | Notes |
|------|----------|-------|
| TYPE C touching `ListingDetailActions` handlers | P0 | Layout/classes only |
| Stale evidence after M-016 related cards | P2 | Recapture post-M-013 |
| Seller/Digging API loading states changed accidentally | P1 | Avoid logic edits in SellerCard |
| Daniela rejects trust-above-CTA reorder | P2 | Reversible layout |
| Queue still shows M-005 READY / M-013 BLOCKED | P2 | TYPE B hygiene after commit |

---

## Stop conditions encountered

None.

Consciously **did not**:

- Implement layout polish  
- Mark route PASS  
- Edit screenshots or code  
- Start M-013  
- Commit or push  

---

## Files created or modified

| Path | Action |
|------|--------|
| `workspace/reports/missions/M-005_EXECUTION_REPORT.md` | **Created** (this file) |

No other files modified.

---

## Validation

| Check | Result |
|-------|--------|
| Frontend unchanged | **Yes** — clean at `f029b83` |
| Backend unchanged | **Yes** — clean |
| Screenshots unchanged | **Yes** — read-only inspection |
| No route marked PASS | **Yes** |
| Workspace report created | **Yes** |
| Git status only M-005 report uncommitted | **Expected:** `?? reports/missions/M-005_EXECUTION_REPORT.md` |

---

## Gate Review recommendation

**Safe to commit** this report only, after explicit `APPROVE_WORKSPACE_COMMIT`.

**Proposed message:** `Record M-005 listing detail polish audit`

**Must NOT commit:** frontend, backend, `screenshots/**` runs/PNGs, artifacts.

**Do not commit. Do not push.** Wait for explicit approval.

---

*End of M-005 execution report.*
