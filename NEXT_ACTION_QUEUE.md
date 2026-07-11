# Next Action Queue — Melómanos Market

**System:** AI Dev OS Bounded Autonomous Mission Execution  
**Pattern:** One mission → one execution report → one gate review  
**Guide:** [`MISSION_EXECUTION_GUIDE.md`](MISSION_EXECUTION_GUIDE.md)  
**Last updated:** 2026-07-10 (M-010 Bounties product spec — TYPE G closure)  
**Stack / tools:** [`STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md)

> This queue is the **operational** execution board for Cursor missions.  
> Product backlog authority remains [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).  
> Visual PASS authority remains Visual Polish / Visual Feedback Loop (human approval).  
> **Cursor** is the primary implementation tool. **v0** is optional UI prototype only — see stack constraints.

---

## How to use

1. Pick the highest-priority mission with status `READY`, or send `APPROVE_NEXT_MISSION` (see [`prompts/RUN_NEXT_MISSION_PROMPT.md`](prompts/RUN_NEXT_MISSION_PROMPT.md)).
2. Or send `APPROVE_MISSION_EXECUTION` + mission ID (see [`prompts/RUN_SELECTED_MISSION_PROMPT.md`](prompts/RUN_SELECTED_MISSION_PROMPT.md)).
3. Executor follows the brief under `workspace/missions/`.
4. Executor writes `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md`.
5. Gate review with `APPROVE_GATE_REVIEW` + mission ID; commit with `APPROVE_SAFE_COMMIT` or repo-specific `APPROVE_*_COMMIT`.
6. After autonomous sessions, run `APPROVE_SESSION_CLOSURE` + `Session: SESSION-*` to sync queue (see [`prompts/SESSION_STATE_SYNC_PROMPT.md`](prompts/SESSION_STATE_SYNC_PROMPT.md)).

**Statuses:** `READY` | `IN_PROGRESS` | `BLOCKED` | `DONE` | `CANCELLED`

**Evidence fields (per mission detail — not separate statuses):** `execution_report`, `gate_result`, `gate_review`, `completion_evidence`, `commit_sha`, `push_status`, `completed_in_session`, `human_disposition`, optional `claimed_by` / `active_session_id`. **DONE** requires `gate_result: PASS`, or `PASS WITH WARNINGS` only after `human_disposition: accepted` via `APPROVE_SESSION_CLOSURE` + `Disposition:`.

---

## Queue summary

| ID | Title | Type | Priority | Status |
|----|-------|------|----------|--------|
| M-001 | Audit Visual Polish / Visual Feedback Loop status | A | P0 | DONE |
| M-002 | Profile UX audit | A | P1 | DONE |
| M-003 | Profile Visual Polish Pass | C | P1 | DONE |
| M-004 | Route Readiness Matrix | A | P1 | DONE |
| M-005 | Listing Detail polish audit | A | P1 | DONE |
| M-006 | Create Listing flow verification | D | P2 | DONE |
| M-007 | Home vs Explore validation | A | P1 | DONE |
| M-008 | Messaging flow audit | A | P2 | DONE |
| M-009 | Favorites flow audit | A | P2 | DONE |
| M-010 | Bounties product spec | G | P3 | DONE |
| M-011 | Add /explorar visual-polish screenshot capture | D | P1 | DONE |
| M-012 | Explore filters/sidebar improvement | C | P1 | DONE |
| M-013 | Product detail page layout | C | P1 | DONE |
| M-014 | Empty states visual pass | C | P2 | DONE |
| M-015 | Mobile navigation polish | C | P2 | DONE |
| M-016 | Listing card visual improvement | C | P1 | DONE |
| M-017 | Adopt reusable mission runner prompts | B | P1 | DONE |
| M-018 | Autonomous session orchestrator | B | P1 | DONE |
| M-019 | Messages back link remediation | C | P2 | DONE |

---

## Missions

### M-001 — Audit Visual Polish / Visual Feedback Loop status

| Field | Value |
|-------|--------|
| **ID** | M-001 |
| **Title** | Audit Visual Polish / Visual Feedback Loop status |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P0 |
| **Status** | DONE (2026-07-08) — report [`reports/missions/M-001_EXECUTION_REPORT.md`](reports/missions/M-001_EXECUTION_REPORT.md) |
| **Scope** | Read Visual Polish + Visual Feedback Loop control docs, route JSON, status, screenshot strategy, visual-audit reports; produce execution report recommending safest next TYPE C mission |
| **Forbidden changes** | No frontend/backend code; no business logic; no screenshot edits; no route PASS changes; no commits |
| **Acceptance criteria** | Execution report exists; current gate/route snapshot summarized; safest next TYPE C mission identified with rationale; risks/warnings listed |
| **Verification required** | Docs inspection only; optional `git status` on workspace/frontend/backend to confirm no product drift |
| **Dependencies** | None |
| **Stop conditions** | Any urge to implement polish or mark PASS → STOP; missing critical control docs → STOP WITH WARNINGS and report |
| **Brief** | [`missions/M-001_AUDIT_VISUAL_POLISH_FEEDBACK_LOOP.md`](missions/M-001_AUDIT_VISUAL_POLISH_FEEDBACK_LOOP.md) |
| **Report path** | `reports/missions/M-001_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | See brief § Executor prompt |

---

### M-002 — Profile UX audit

| Field | Value |
|-------|--------|
| **ID** | M-002 |
| **Title** | Profile UX audit |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P1 |
| **Status** | DONE (2026-07-09) — report [`reports/missions/M-002_EXECUTION_REPORT.md`](reports/missions/M-002_EXECUTION_REPORT.md) |
| **Scope** | Review `/profile` UX against brand system and existing screenshots/reports; list defects and polish opportunities; no implementation |
| **Forbidden changes** | No code; no PASS; no commits; no backend |
| **Acceptance criteria** | Report with findings ranked P0–P2; recommended follow-up mission (likely M-003) |
| **Verification required** | Read profile-related visual status/routes; inspect latest screenshot runs if present (read-only) |
| **Dependencies** | Prefer M-001 done (not hard-blocked) |
| **Stop conditions** | Implementation requested mid-audit → STOP and open TYPE C mission |
| **Brief** | `missions/M-002_PROFILE_UX_AUDIT.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-002_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-002 — TYPE A Profile UX audit only |

---

### M-003 — Profile Visual Polish Pass

| Field | Value |
|-------|--------|
| **ID** | M-003 |
| **Title** | Profile Visual Polish Pass |
| **Mission type** | TYPE C — Frontend Low-Risk |
| **Priority** | P1 |
| **Status** | DONE (2026-07-09) — report [`reports/missions/M-003_EXECUTION_REPORT.md`](reports/missions/M-003_EXECUTION_REPORT.md); frontend `5857a75` |
| **Scope** | Frontend visual polish for `/profile` only, within approved ivory/black/gold system; update E2E only if selectors require it |
| **Forbidden changes** | No backend; no business logic; no HomeHero; no Admin redesign; no route PASS; no commits without token |
| **Acceptance criteria** | Profile surfaces match editorial system; build + relevant E2E pass; report + screenshot run path; still IN_REVIEW pending human |
| **Verification required** | `npm run build`; targeted or full E2E as brief specifies; `test:e2e:visual-polish` if brief requires; workspace `--check` if stack needed |
| **Dependencies** | M-002 DONE (met) |
| **Stop conditions** | Scope expands beyond Profile; product redesign needed → STOP for TYPE G |
| **Brief** | `missions/M-003_PROFILE_VISUAL_POLISH_PASS.md` *(create after M-002)* |
| **Report path** | `reports/missions/M-003_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | Only after M-002 DONE + `APPROVE_MISSION_EXECUTION` for M-003 |

---

### M-004 — Route Readiness Matrix

| Field | Value |
|-------|--------|
| **ID** | M-004 |
| **Title** | Route Readiness Matrix |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P1 |
| **Status** | DONE (2026-07-09) — report [`reports/missions/M-004_EXECUTION_REPORT.md`](reports/missions/M-004_EXECUTION_REPORT.md) |
| **Scope** | Build a readiness matrix from `VISUAL_POLISH_ROUTES.json` + status + latest runs; classify each route (evidence, auth, risk, next action) |
| **Forbidden changes** | No code; no PASS flips; no screenshot mutation; no commits |
| **Acceptance criteria** | Matrix table in execution report; recommended ordered polish queue |
| **Verification required** | Read-only inspection of routes JSON, status, screenshot README |
| **Dependencies** | Prefer M-001 |
| **Stop conditions** | Temptation to mark PASS → STOP |
| **Brief** | `missions/M-004_ROUTE_READINESS_MATRIX.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-004_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-004 |

---

### M-005 — Listing Detail polish audit

| Field | Value |
|-------|--------|
| **ID** | M-005 |
| **Title** | Listing Detail polish audit |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P1 |
| **Status** | DONE (2026-07-10) — report [`reports/missions/M-005_EXECUTION_REPORT.md`](reports/missions/M-005_EXECUTION_REPORT.md) |
| **Scope** | Audit `/listings/[id]` visual/UX debt (IN_REVIEW historically); list safe TYPE C follow-ups |
| **Forbidden changes** | No code; no pricing/order/message logic changes; no PASS; no commits |
| **Acceptance criteria** | Ranked findings; explicit out-of-scope business items called out |
| **Verification required** | Routes/status/reports + read-only screenshots |
| **Dependencies** | None (prefer M-001) |
| **Stop conditions** | Fixing buy/message flows → STOP (wrong type) |
| **Brief** | `missions/M-005_LISTING_DETAIL_POLISH_AUDIT.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-005_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-005 |

---

### M-006 — Create Listing flow verification

| Field | Value |
|-------|--------|
| **ID** | M-006 |
| **Title** | Create Listing flow verification |
| **Mission type** | TYPE D — Frontend Verification |
| **Priority** | P2 |
| **Status** | DONE (2026-07-10) |
| **execution_report** | [`reports/missions/M-006_EXECUTION_REPORT.md`](reports/missions/M-006_EXECUTION_REPORT.md) |
| **gate_result** | PASS |
| **gate_review** | Inline in execution report § Verdict |
| **completion_evidence** | build PASS; sell E2E 6/6 PASS; workspace `--check` PASS |
| **commit_sha** | — |
| **push_status** | not_requested |
| **completed_in_session** | SESSION-20260710-1721 |
| **human_disposition** | — |
| **Scope** | Verify `/sell` create-listing flow via existing E2E/build; document gaps; **no product redesign**; code changes only if brief later upgrades and approves (default: verification only) |
| **Forbidden changes** | No backend rules; no subscription/business logic edits; no commits without token; no PASS |
| **Acceptance criteria** | Verification results table; list of failures/flakes; recommendation (fix mission vs polish mission) |
| **Verification required** | `npm run build`; relevant sell/listing E2E; note Quality Gate tier used |
| **Dependencies** | None |
| **Stop conditions** | Need business-rule change → STOP for TYPE F |
| **Brief** | [`missions/M-006_CREATE_LISTING_FLOW_VERIFICATION.md`](missions/M-006_CREATE_LISTING_FLOW_VERIFICATION.md) |
| **Report path** | `reports/missions/M-006_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-006 — verification only |

---

### M-007 — Home vs Explore validation

| Field | Value |
|-------|--------|
| **ID** | M-007 |
| **Title** | Home vs Explore validation |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P1 |
| **Status** | DONE (2026-07-09) — report [`reports/missions/M-007_EXECUTION_REPORT.md`](reports/missions/M-007_EXECUTION_REPORT.md) |
| **Scope** | Validate Phase 1 Home discovery vs `/explorar` catalog split against governance reports; confirm header IA C1 alignment; recommend TYPE C only if concrete low-risk UI debt found |
| **Forbidden changes** | No HomeHero edits; no catalog preset C2; no code unless mission reclassified; no PASS; no commits |
| **Acceptance criteria** | Split integrity checklist; open visual debts; next mission recommendation |
| **Verification required** | Read Phase 1 / header IA reports; optional read-only screenshot compare |
| **Dependencies** | Prefer M-001 |
| **Stop conditions** | Implementing C2 presets or Home restructure → STOP |
| **Brief** | `missions/M-007_HOME_VS_EXPLORE_VALIDATION.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-007_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-007 |

---

### M-008 — Messaging flow audit

| Field | Value |
|-------|--------|
| **ID** | M-008 |
| **Title** | Messaging flow audit |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P2 |
| **Status** | DONE (2026-07-10) — re-audit closure after M-019 remediation |
| **execution_report** | [`reports/missions/M-008_EXECUTION_REPORT.md`](reports/missions/M-008_EXECUTION_REPORT.md) |
| **reaudit_report** | [`reports/missions/M-008_REAUDIT_REPORT.md`](reports/missions/M-008_REAUDIT_REPORT.md) |
| **gate_result** | PASS WITH WARNINGS |
| **gate_review** | Original: execution report § Verdict; closure: re-audit report § Gate result |
| **completion_evidence** | F1 remediated (M-019); messaging E2E 3/3; contact-leak PASS; build + unit PASS |
| **commit_sha** | workspace pending — post re-audit commit |
| **push_status** | pending_approval |
| **completed_in_session** | SESSION-20260710-1721; closed M-008-REAUDIT 2026-07-10 |
| **human_disposition** | accepted_after_remediation |
| **disposition_recorded** | 2026-07-10 — M-008-REAUDIT after M-019 @ frontend `e8b8564` |
| **remediation_mission** | M-019 — DONE; frontend `e8b8564de09ed81d4c1f02839aae34f14e05169d` |
| **Scope** | Audit inbox/thread UX and known reply/contact-leak constraints from docs/tests; no backend changes |
| **Forbidden changes** | No messaging API/business logic; no code; no commits |
| **Acceptance criteria** | Flow findings; distinguish UX polish vs backend rule work |
| **Verification required** | Read messaging-related E2E names/docs; status routes for `/messages` |
| **Dependencies** | None |
| **Stop conditions** | Editing `messages` routers/schemas → STOP (TYPE F) |
| **Brief** | [`missions/M-008_MESSAGING_FLOW_AUDIT.md`](missions/M-008_MESSAGING_FLOW_AUDIT.md) |
| **Report path** | `reports/missions/M-008_EXECUTION_REPORT.md` |
| **Notes** | **F1 closed** via M-019. **Non-blocking warnings preserved:** F2 mobile thread density; F3 trust copy density; F4 route IN_REVIEW (human visual gate). `gate_result` not flattened to PASS. |
| **Recommended executor prompt** | Completed — M-008 closed after re-audit |

---

### M-009 — Favorites flow audit

| Field | Value |
|-------|--------|
| **ID** | M-009 |
| **Title** | Favorites flow audit |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P2 |
| **Status** | DONE (2026-07-10) |
| **execution_report** | [`reports/missions/M-009_EXECUTION_REPORT.md`](reports/missions/M-009_EXECUTION_REPORT.md) |
| **gate_result** | PASS |
| **gate_review** | Inline in execution report |
| **completion_evidence** | Flow audit; M-014 empty state; E2E favorites flow |
| **commit_sha** | workspace `07329d5` |
| **push_status** | pending_approval |
| **completed_in_session** | SESSION-20260710-1811 |
| **human_disposition** | — |
| **Scope** | Audit `/favorites` UX/visual readiness; recommend TYPE C polish if warranted |
| **Forbidden changes** | No code; no PASS; no commits |
| **Acceptance criteria** | Findings + recommended next mission |
| **Verification required** | Routes/status + read-only screenshots |
| **Dependencies** | None |
| **Stop conditions** | Implementing favorites API changes → STOP |
| **Brief** | `missions/M-009_FAVORITES_FLOW_AUDIT.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-009_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-009 |

---

### M-010 — Bounties product spec

| Field | Value |
|-------|--------|
| **ID** | M-010 |
| **Title** | Bounties product spec |
| **Mission type** | TYPE G — Product Design only |
| **Priority** | P3 |
| **Status** | DONE (2026-07-10) — specification complete; **implementation NOT_APPROVED** |
| **execution_report** | [`reports/missions/M-010_EXECUTION_REPORT.md`](reports/missions/M-010_EXECUTION_REPORT.md) |
| **gate_result** | PASS WITH WARNINGS |
| **gate_review** | Inline in execution report § Gate result |
| **completion_evidence** | [`BOUNTIES_PRODUCT_SPEC.md`](BOUNTIES_PRODUCT_SPEC.md); [`decisions/BOUNTIES_MVP_DECISION_RECORD.md`](decisions/BOUNTIES_MVP_DECISION_RECORD.md); SPEC index row |
| **commit_sha** | pending — post M-010 commit |
| **push_status** | pending_approval |
| **completed_in_session** | M-010-20260710 |
| **implementation_status** | **NOT_APPROVED** |
| **human_disposition** | — |
| **Scope** | Product/UX spec for future Bounties (wanted records + optional informational incentive); no implementation |
| **Forbidden changes** | No frontend/backend implementation; no schema; no code |
| **Acceptance criteria** | Spec: problem, flows, non-goals, open questions, proposed later missions — **met** |
| **Verification required** | Spec completeness; `py run_melomanos.py --check` — **met** |
| **Dependencies** | None |
| **Brief** | [`missions/M-010_BOUNTIES_PRODUCT_SPEC.md`](missions/M-010_BOUNTIES_PRODUCT_SPEC.md) |
| **Canonical spec** | [`BOUNTIES_PRODUCT_SPEC.md`](BOUNTIES_PRODUCT_SPEC.md) |
| **Decision record** | [`decisions/BOUNTIES_MVP_DECISION_RECORD.md`](decisions/BOUNTIES_MVP_DECISION_RECORD.md) |
| **Notes** | **W1–W4** non-blocking: human decisions (M-020); roadmap/BUSINESS_RULES updates deferred to implementation. MVP = informational wanted board; no fund custody. |
| **Recommended executor prompt** | Completed — see proposed batch below |

---

### M-011 — Add /explorar visual-polish screenshot capture

| Field | Value |
|-------|--------|
| **ID** | M-011 |
| **Title** | Add /explorar visual-polish screenshot capture |
| **Mission type** | TYPE D — Test / Tooling / Verification |
| **Priority** | P1 |
| **Status** | DONE (2026-07-09) — report [`reports/missions/M-011_EXECUTION_REPORT.md`](reports/missions/M-011_EXECUTION_REPORT.md) |
| **Scope** | Visual-polish screenshot tooling only — add `/explorar` desktop + mobile logged-out captures to `frontend/e2e/visual-polish-screenshots.spec.ts`; preserve existing captures |
| **Forbidden changes** | No product UI; no backend; no business logic; no route PASS; no staging screenshot runs; no commits without token |
| **Acceptance criteria** | `/explorar` desktop + mobile visual-polish evidence generated (`runs/<ts>/explorar/`); build + E2E + `test:e2e:visual-polish` pass |
| **Verification required** | `npm run build`; `npm run test:e2e`; `npm run test:e2e:visual-polish`; `py run_melomanos.py --check` |
| **Dependencies** | M-007 recommended first (met); executed per approved brief after M-007 TYPE D recommendation |
| **Stop conditions** | Explore layout polish → STOP (TYPE C); marking PASS → STOP |
| **Brief** | M-007 recommendation + `APPROVE_MISSION_EXECUTION` prompt (2026-07-09) |
| **Report path** | `reports/missions/M-011_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | Completed — governance note: queue originally listed Listing Card as M-011; see M-016 |

---

### M-012 — Explore filters/sidebar improvement

| Field | Value |
|-------|--------|
| **ID** | M-012 |
| **Title** | Explore filters/sidebar improvement |
| **Mission type** | TYPE C — Frontend Low-Risk |
| **Priority** | P1 |
| **Status** | DONE (2026-07-10) — report [`reports/missions/M-012_EXECUTION_REPORT.md`](reports/missions/M-012_EXECUTION_REPORT.md); frontend `9879842` |
| **Scope** | Visual/layout polish of `/explorar` filter form / sidebar chrome only; keep filter query behavior intact |
| **Forbidden changes** | No new catalog presets (Header C2); no backend filter semantics; no Home restructure; no PASS; no commits without token |
| **Tooling** | **Cursor** primary. Optional **v0** for sidebar layout sketch only; Cursor integrates |
| **Acceptance criteria** | Filters readable on desktop/mobile; build + E2E; evidence run; IN_REVIEW |
| **Verification required** | `npm run build`; E2E covering explorar/filters; visual-polish if required |
| **Dependencies** | Prefer M-007 (Home vs Explore validation) before large IA claims; not hard-blocked for chrome-only polish |
| **Stop conditions** | Changing sort/query contracts or adding Sellos/Artistas modes → STOP (C2 / TYPE G) |
| **Brief** | [`missions/M-012_EXPLORE_FILTERS_SIDEBAR.md`](missions/M-012_EXPLORE_FILTERS_SIDEBAR.md) |
| **Report path** | `reports/missions/M-012_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-012 |

---

### M-013 — Product detail page layout

| Field | Value |
|-------|--------|
| **ID** | M-013 |
| **Title** | Product detail page layout |
| **Mission type** | TYPE C — Frontend Low-Risk |
| **Priority** | P1 |
| **Status** | DONE (2026-07-10) — report [`reports/missions/M-013_EXECUTION_REPORT.md`](reports/missions/M-013_EXECUTION_REPORT.md); frontend `d74f34b` |
| **Scope** | Layout/visual polish for `/listings/[id]` within design system after audit defines file scope |
| **Forbidden changes** | No buy/message/order business logic; no backend; no PASS; no commits without token |
| **Tooling** | **Cursor** primary. Optional **v0** layout sketch only after M-005; Cursor integrates |
| **Acceptance criteria** | Detail layout editorial; build + E2E; evidence; IN_REVIEW |
| **Verification required** | `npm run build`; listing-related E2E; visual-polish |
| **Dependencies** | M-005 DONE (met) |
| **Stop conditions** | Touching escrow/message rules → STOP (TYPE F) |
| **Brief** | `missions/M-013_PRODUCT_DETAIL_LAYOUT.md` *(create after M-005)* |
| **Report path** | `reports/missions/M-013_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | Only after M-005 DONE + `APPROVE_MISSION_EXECUTION` for M-013 |

---

### M-014 — Empty states visual pass

| Field | Value |
|-------|--------|
| **ID** | M-014 |
| **Title** | Empty states visual pass |
| **Mission type** | TYPE C — Frontend Low-Risk |
| **Priority** | P2 |
| **Status** | DONE (2026-07-10) — report [`reports/missions/M-014_EXECUTION_REPORT.md`](reports/missions/M-014_EXECUTION_REPORT.md); frontend `065c0e8` |
| **Scope** | Editorial empty states for favorites, messages, orders, and/or explorar-as-scoped in brief — copy + layout only |
| **Forbidden changes** | No API empty-contract changes; no backend; no PASS; no commits without token |
| **Tooling** | **Cursor** primary. Optional **v0** for empty-state composition; Cursor integrates |
| **Acceptance criteria** | Empty states on-system; build + relevant E2E; evidence if capturable |
| **Verification required** | `npm run build`; targeted E2E |
| **Dependencies** | None |
| **Stop conditions** | Inventing new product flows → STOP (TYPE G) |
| **Brief** | [`missions/M-014_EMPTY_STATES_VISUAL_PASS.md`](missions/M-014_EMPTY_STATES_VISUAL_PASS.md) |
| **Report path** | `reports/missions/M-014_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-014 |

---

### M-015 — Mobile navigation polish

| Field | Value |
|-------|--------|
| **ID** | M-015 |
| **Title** | Mobile navigation polish |
| **Mission type** | TYPE C — Frontend Low-Risk |
| **Priority** | P2 |
| **Status** | DONE (2026-07-10) |
| **execution_report** | [`reports/missions/M-015_EXECUTION_REPORT.md`](reports/missions/M-015_EXECUTION_REPORT.md) |
| **gate_result** | PASS |
| **gate_review** | Inline in execution report |
| **completion_evidence** | build PASS; E2E 44/44 PASS; mobile header test added |
| **commit_sha** | frontend `b1a9bf8`; workspace `eb59457` |
| **push_status** | pending_approval |
| **completed_in_session** | SESSION-20260710-1811 |
| **human_disposition** | — |
| **Scope** | Mobile utility/product header behavior within Header IA C1 (spacing, search row, product links) — no IA redesign |
| **Forbidden changes** | No C2 presets; no hamburger redesign unless brief explicitly allows; no backend; no PASS; no commits without token |
| **Tooling** | **Cursor** only (Navbar is production-integrated; avoid v0 full-header rewrite) |
| **Acceptance criteria** | Mobile header usable; E2E header tests pass; evidence mobile captures; IN_REVIEW |
| **Verification required** | `npm run build`; `npm run test:e2e`; visual-polish mobile |
| **Dependencies** | Header C1 + search-width already committed |
| **Stop conditions** | Reopening full Header IA / Home restructure → STOP |
| **Brief** | `missions/M-015_MOBILE_NAVIGATION_POLISH.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-015_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-015 |

---

### M-016 — Listing card visual improvement

| Field | Value |
|-------|--------|
| **ID** | M-016 |
| **Title** | Listing card visual improvement |
| **Mission type** | TYPE C — Frontend Low-Risk |
| **Priority** | P1 |
| **Status** | DONE (2026-07-10) — report [`reports/missions/M-016_EXECUTION_REPORT.md`](reports/missions/M-016_EXECUTION_REPORT.md); frontend `f029b83` |
| **Scope** | Visual polish of `ListingCard` (and shared cover/badge chrome only) within ivory/black/gold system; preserve test ids and buy/favorite behavior |
| **Forbidden changes** | No backend; no pricing/reservation logic; no HomeHero; no route PASS; no commits without token |
| **Tooling** | **Cursor** primary. Optional **v0** sketch only if brief allows; Cursor integrates; repo is source of truth |
| **Acceptance criteria** | Cards match editorial system on `/explorar` (and any shared grid); build + E2E pass; screenshot run path; IN_REVIEW pending human |
| **Verification required** | `npm run build`; `npm run test:e2e`; visual-polish capture if brief requires |
| **Dependencies** | M-011 DONE (explorar capture evidence). Prefer M-001 DONE (met) |
| **Stop conditions** | Business-rule or API change needed → STOP (TYPE F); scope expands to full Explore IA → STOP |
| **Brief** | `missions/M-016_LISTING_CARD_VISUAL_IMPROVEMENT.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-016_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-016 — TYPE C ListingCard only |
| **Notes** | Former queue entry M-011 (Listing Card); renumbered after M-011 executed as explorar capture TYPE D |

---

### M-017 — Adopt reusable mission runner prompts

| Field | Value |
|-------|--------|
| **ID** | M-017 |
| **Title** | Adopt reusable mission runner prompts |
| **Mission type** | TYPE B — Docs / Governance |
| **Priority** | P1 |
| **Status** | DONE (2026-07-10) — report [`reports/missions/M-017_EXECUTION_REPORT.md`](reports/missions/M-017_EXECUTION_REPORT.md) |
| **Scope** | Add `workspace/prompts/` short-command interfaces; update mission guide and queue references |
| **Forbidden changes** | No frontend/backend/product code; no screenshots; no commits during execution |
| **Acceptance criteria** | Four prompt files; Short Command Interface in guide; M-017 report; queue updated |
| **Verification required** | Docs inspection; git status shows only expected workspace paths |
| **Dependencies** | Mission execution layer adopted (M-001 guide + queue) |
| **Stop conditions** | Any product code change → STOP |
| **Brief** | User `APPROVE_MISSION_EXECUTION` prompt (2026-07-10) |
| **Report path** | `reports/missions/M-017_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-017 — completed |

---

### M-019 — Messages back link remediation (PROPOSED)

| Field | Value |
|-------|--------|
| **ID** | M-019 |
| **Title** | Messages back link remediation |
| **Mission type** | TYPE C — Frontend Low-Risk |
| **Priority** | P2 |
| **Status** | DONE (2026-07-10) |
| **execution_report** | [`reports/missions/M-019_EXECUTION_REPORT.md`](reports/missions/M-019_EXECUTION_REPORT.md) |
| **gate_result** | PASS |
| **gate_review** | Inline in execution report § Gate review |
| **completion_evidence** | Back link `/explorar`; messaging E2E 2/2; build + unit PASS |
| **commit_sha** | frontend `e8b8564`; workspace `15db36e` |
| **push_status** | pending_approval |
| **completed_in_session** | ACTION-M-019-20260710 |
| **human_disposition** | — |
| **human_activation** | 2026-07-10 — explicit `APPROVE_MISSION_EXECUTION` |
| **m008_remediation** | F1 resolved — M-008 eligible for re-audit; **not** auto-DONE |
| **Scope** | Fix `/messages` back link destination `/` → `/explorar` in `frontend/src/app/messages/page.tsx`; E2E update only if href asserted |
| **Forbidden changes** | Messaging API/business logic; mobile header (M-015); backend; route PASS; commits without token |
| **Acceptance criteria** | Back link → `/explorar`; messaging E2E pass; build pass; execution report |
| **Verification required** | `npm run build`; targeted messaging E2E |
| **Dependencies** | M-008 `human_disposition: remediation_required` (origin) |
| **Stop conditions** | TYPE F scope; full messages redesign → STOP |
| **Brief** | [`missions/M-019_MESSAGES_BACK_LINK_REMEDIATION.md`](missions/M-019_MESSAGES_BACK_LINK_REMEDIATION.md) |
| **Report path** | `reports/missions/M-019_EXECUTION_REPORT.md` |
| **Notes** | M-008 F1 remediated. M-008 remains BLOCKED pending re-audit / disposition — do not auto-DONE. |
| **Recommended executor prompt** | Completed — see M-019 report |

---

### M-018 — Autonomous session orchestrator

| Field | Value |
|-------|--------|
| **ID** | M-018 |
| **Title** | Autonomous session orchestrator |
| **Mission type** | TYPE B — Docs / Governance |
| **Priority** | P1 |
| **Status** | DONE (2026-07-10) — report [`reports/missions/M-018_EXECUTION_REPORT.md`](reports/missions/M-018_EXECUTION_REPORT.md) |
| **Scope** | Add `APPROVE_AUTONOMOUS_SESSION` multi-mission orchestrator prompt; update mission guide and queue |
| **Forbidden changes** | No frontend/backend/product code; no commits during execution |
| **Acceptance criteria** | `AUTONOMOUS_SESSION_PROMPT.md`; session report convention; guide + queue updated |
| **Verification required** | Docs inspection; git status shows only workspace docs |
| **Dependencies** | M-017 reusable prompts (met) |
| **Stop conditions** | Any product code change → STOP |
| **Brief** | [`missions/M-018_AUTONOMOUS_SESSION_ORCHESTRATOR.md`](missions/M-018_AUTONOMOUS_SESSION_ORCHESTRATOR.md) |
| **Report path** | `reports/missions/M-018_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_AUTONOMOUS_SESSION` — see [`prompts/AUTONOMOUS_SESSION_PROMPT.md`](prompts/AUTONOMOUS_SESSION_PROMPT.md) |

---

## Suggested execution order

**Queue exhausted for READY missions.** All M-001–M-019 and M-010 are DONE.

**Completed (recent):** **M-010** Bounties product spec (2026-07-10).

**Primary next human action:** Review [`BOUNTIES_PRODUCT_SPEC.md`](BOUNTIES_PRODUCT_SPEC.md) → `APPROVE_MISSION_EXECUTION` / Mission: **M-020** (decision closure) when ready — or promote implementation batch after decisions locked.

**READY missions:** **zero**. **READY A/B/C/D:** zero. **BLOCKED:** none.

---

## Proposed missions (post M-010 — not READY)

Implementation **NOT_APPROVED**. Activate only with explicit per-mission approval.

| ID | Title | Type | Priority | Status |
|----|-------|------|----------|--------|
| M-020 | Bounties human decision closure | G | P2 | PROPOSED |
| M-021 | Bounties backend domain + persistence design | F | P2 | PROPOSED |
| M-022 | Bounties API contracts | F | P2 | PROPOSED |
| M-023 | Bounties discovery + detail UI | C/H | P2 | PROPOSED |
| M-024 | Create / manage bounties UI | C/H | P2 | PROPOSED |
| M-025 | Seller response flow | C/H | P2 | PROPOSED |
| M-026 | Bounties notifications + messaging hooks | F | P2 | PROPOSED |
| M-027 | Bounties E2E + abuse controls | D/F | P2 | PROPOSED |

**Suggested order:** M-020 → M-021 → M-022 → parallel UI (M-023–M-025) → M-026 → M-027.

Or run a bounded batch: `APPROVE_AUTONOMOUS_SESSION` with `Max missions:` and `Commits: disabled|enabled`.

---

## Notes

- Reusable prompts: [`workspace/prompts/`](prompts/) — includes `APPROVE_AUTONOMOUS_SESSION` for multi-mission sessions
- Briefs for M-002+ may be created at mission start from this queue + [`MISSION_EXECUTION_GUIDE.md`](MISSION_EXECUTION_GUIDE.md); **M-001 brief + report exist**.
- Do not weaken Visual Polish human approval gates via this queue.
- Header search-width microfix is **committed** (`frontend` `d09225b`); do not reopen as dirty work.
- UI candidates M-012, M-013, M-014, M-015, M-016 follow [`STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md) tool rules.
- **M-011 governance (2026-07-09):** M-011 executed as explorar visual-polish capture (TYPE D, DONE). Former Listing Card mission renumbered to **M-016**.
- **SESSION-20260710-1721 (2026-07-10):** M-008 disposition `remediation_required` (2026-07-10). M-019 proposed for messages back link `/` → `/explorar`. M-015 does **not** cover this defect (header-only scope).
