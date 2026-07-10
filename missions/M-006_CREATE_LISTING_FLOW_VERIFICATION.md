# M-006 — Create Listing Flow Verification

**Mission ID:** M-006  
**Type:** TYPE D — Frontend Verification  
**Priority:** P2  
**Route:** `/sell`

---

## Goal

Verify `/sell` create-listing flow via existing E2E/build. Document gaps. **Verification only** — no product redesign.

---

## Scope

- Run `npm run build`
- Run sell-related E2E in `e2e/melomanos.spec.ts`
- Run `py run_melomanos.py --check`
- Document results; no code changes

---

## Forbidden

- Backend / business rule changes
- Product redesign
- Route PASS
- Commits

---

## Acceptance criteria

Verification results table; failures/flakes listed; recommendation for follow-up mission.

---

## Verification

```bash
cd frontend && npm run build
npx playwright test e2e/melomanos.spec.ts -g "sell|used listing"
cd workspace && py run_melomanos.py --check
```
