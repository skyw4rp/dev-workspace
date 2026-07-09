# Next Action Queue — Melómanos Market

**System:** AI Dev OS Bounded Autonomous Mission Execution  
**Pattern:** One mission → one execution report → one gate review  
**Guide:** [`MISSION_EXECUTION_GUIDE.md`](MISSION_EXECUTION_GUIDE.md)  
**Last updated:** 2026-07-08

> This queue is the **operational** execution board for Cursor missions.  
> Product backlog authority remains [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).  
> Visual PASS authority remains Visual Polish / Visual Feedback Loop (human approval).

---

## How to use

1. Pick the highest-priority mission with status `READY`.
2. Send `APPROVE_MISSION_EXECUTION` + mission ID (see guide).
3. Executor follows the brief under `workspace/missions/`.
4. Executor writes `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md`.
5. Separate gate review; commit only with `APPROVE_*_COMMIT`.

**Statuses:** `READY` | `IN_PROGRESS` | `BLOCKED` | `DONE` | `CANCELLED`

---

## Queue summary

| ID | Title | Type | Priority | Status |
|----|-------|------|----------|--------|
| M-001 | Audit Visual Polish / Visual Feedback Loop status | A | P0 | READY |
| M-002 | Profile UX audit | A | P1 | READY |
| M-003 | Profile Visual Polish Pass | C | P1 | BLOCKED |
| M-004 | Route Readiness Matrix | A | P1 | READY |
| M-005 | Listing Detail polish audit | A | P1 | READY |
| M-006 | Create Listing flow verification | D | P2 | READY |
| M-007 | Home vs Explore validation | A | P1 | READY |
| M-008 | Messaging flow audit | A | P2 | READY |
| M-009 | Favorites flow audit | A | P2 | READY |
| M-010 | Bounties product spec | G | P3 | READY |

---

## Missions

### M-001 — Audit Visual Polish / Visual Feedback Loop status

| Field | Value |
|-------|--------|
| **ID** | M-001 |
| **Title** | Audit Visual Polish / Visual Feedback Loop status |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P0 |
| **Status** | READY |
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
| **Status** | READY |
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
| **Status** | BLOCKED |
| **Scope** | Frontend visual polish for `/profile` only, within approved ivory/black/gold system; update E2E only if selectors require it |
| **Forbidden changes** | No backend; no business logic; no HomeHero; no Admin redesign; no route PASS; no commits without token |
| **Acceptance criteria** | Profile surfaces match editorial system; build + relevant E2E pass; report + screenshot run path; still IN_REVIEW pending human |
| **Verification required** | `npm run build`; targeted or full E2E as brief specifies; `test:e2e:visual-polish` if brief requires; workspace `--check` if stack needed |
| **Dependencies** | **Blocked on M-002** (audit must define scope) |
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
| **Status** | READY |
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
| **Status** | READY |
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
| **Status** | READY |
| **Scope** | Verify `/sell` create-listing flow via existing E2E/build; document gaps; **no product redesign**; code changes only if brief later upgrades and approves (default: verification only) |
| **Forbidden changes** | No backend rules; no subscription/business logic edits; no commits without token; no PASS |
| **Acceptance criteria** | Verification results table; list of failures/flakes; recommendation (fix mission vs polish mission) |
| **Verification required** | `npm run build`; relevant sell/listing E2E; note Quality Gate tier used |
| **Dependencies** | None |
| **Stop conditions** | Need business-rule change → STOP for TYPE F |
| **Brief** | `missions/M-006_CREATE_LISTING_FLOW_VERIFICATION.md` *(create at execution start if missing)* |
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
| **Status** | READY |
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
| **Status** | READY |
| **Scope** | Audit inbox/thread UX and known reply/contact-leak constraints from docs/tests; no backend changes |
| **Forbidden changes** | No messaging API/business logic; no code; no commits |
| **Acceptance criteria** | Flow findings; distinguish UX polish vs backend rule work |
| **Verification required** | Read messaging-related E2E names/docs; status routes for `/messages` |
| **Dependencies** | None |
| **Stop conditions** | Editing `messages` routers/schemas → STOP (TYPE F) |
| **Brief** | `missions/M-008_MESSAGING_FLOW_AUDIT.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-008_EXECUTION_REPORT.md` |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-008 |

---

### M-009 — Favorites flow audit

| Field | Value |
|-------|--------|
| **ID** | M-009 |
| **Title** | Favorites flow audit |
| **Mission type** | TYPE A — Review Only |
| **Priority** | P2 |
| **Status** | READY |
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
| **Status** | READY |
| **Scope** | Produce a product/UX spec for a future Bounties feature; no implementation |
| **Forbidden changes** | No frontend/backend implementation; no schema; no commits of code; docs/report only |
| **Acceptance criteria** | Spec covering problem, user flows, non-goals, open questions, suggested later mission types |
| **Verification required** | Spec completeness review only |
| **Dependencies** | None (low priority vs visual audits) |
| **Stop conditions** | Any implementation started → STOP |
| **Brief** | `missions/M-010_BOUNTIES_PRODUCT_SPEC.md` *(create at execution start if missing)* |
| **Report path** | `reports/missions/M-010_EXECUTION_REPORT.md` (or spec path named in brief) |
| **Recommended executor prompt** | `APPROVE_MISSION_EXECUTION` / Mission: M-010 — TYPE G docs only |

---

## Suggested execution order

1. **M-001** (P0) — establish visual system truth  
2. **M-004** or **M-007** — route / Home–Explore clarity  
3. **M-002** → **M-003** — Profile audit then polish  
4. **M-005** — Listing detail audit  
5. **M-006 / M-008 / M-009** — verification & flow audits  
6. **M-010** — product design when capacity allows  

---

## Notes

- Briefs for M-002+ may be created at mission start from this queue + [`MISSION_BRIEF` expectations in the guide](MISSION_EXECUTION_GUIDE.md); **M-001 brief already exists**.
- Do not weaken Visual Polish human approval gates via this queue.
- Uncommitted header search width work (if any) is **out of band** — handle via its own TYPE C mission or explicit commit approval, not by mixing into M-001.
