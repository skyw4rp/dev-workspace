# M-019 — Messages Back Link Remediation (PROPOSED)

**Mission ID:** M-019  
**Type:** TYPE C — Frontend Low-Risk  
**Priority:** P2  
**Status:** APPROVED — executable via `APPROVE_MISSION_EXECUTION` (2026-07-10)  
**Origin:** M-008 F1 — `human_disposition: remediation_required` (SESSION-20260710-1721)

---

## Goal

Correct the `/messages` page persistent back link so `← Volver al catálogo` navigates to `/explorar` instead of `/`, aligning with Phase 1 Home vs Explore catalog split.

---

## Scope

- `frontend/src/app/messages/page.tsx` — back link `href` and label only (match Phase 1 pattern used on profile/listing detail where applicable)
- E2E assertion update **only if** an existing test asserts the old `/` destination for this link

---

## Forbidden

- Messaging API, routers, or business logic (TYPE F)
- Contact-leak / reply behavior changes
- Mobile header / Navbar (M-015 scope)
- Route PASS
- Backend changes
- Commits without token

---

## Acceptance criteria

1. On `/messages`, the back link labeled `← Volver al catálogo` (or approved Phase 1 copy) resolves to `/explorar`
2. No regression to inbox, thread, or reply E2E (`messages page loads`, `messages reply from inbox thread`)
3. `npm run build` PASS
4. Targeted messaging E2E PASS
5. Execution report references M-008 F1 remediation
6. Routes remain IN_REVIEW — no visual PASS

---

## Verification plan

| Check | Command / action |
|-------|------------------|
| Build | `npm run build` (frontend) |
| Messaging E2E | `npm run test:e2e` — messaging-related specs |
| Manual | Load `/messages`; confirm back link target is `/explorar` |
| Workspace | `py run_melomanos.py --check` if stack validation needed |

---

## Expected repositories affected

| Repo | Change |
|------|--------|
| `frontend/` | `src/app/messages/page.tsx`; optional E2E selector/href assertion |
| `workspace/` | Execution report only (post-execution) |
| `backend/` | None |

---

## Dependencies

- M-008 disposition `remediation_required` recorded (met at proposal time)
- No dependency on M-015 — distinct surface (messages page back link vs mobile header)

---

## Stop conditions

- Fix requires messaging API or anti-leak rule change → STOP (TYPE F)
- Scope expands to full messages UX redesign → STOP; open TYPE G
- Test failures outside href/copy → STOP and report

---

## Relationship to M-008

Completing M-019 successfully does **not** auto-close M-008. After remediation, human may re-run disposition or gate review per mission guide.
