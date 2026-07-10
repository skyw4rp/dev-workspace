# Gate Review — `APPROVE_GATE_REVIEW`

**Command (user sends):**

```text
APPROVE_GATE_REVIEW
Mission: M-XXX
```

Replace `M-XXX` with the completed mission ID.

**Executor:** Melómanos Market AI Dev OS Lead Engineer and Adoption Agent (gate reviewer role only).

---

## Instructions

1. Read:
   - `workspace/MISSION_EXECUTION_GUIDE.md`
   - `workspace/NEXT_ACTION_QUEUE.md` — mission entry for `M-XXX`
   - `workspace/missions/M-XXX_*.md` (brief)
   - `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md` (required — if missing, **STOP**)

2. **Do not implement.** Review only.

3. Confirm:
   - Mission scope was honored (type, forbidden paths, stop conditions).
   - Changes match what the execution report claims.
   - No out-of-scope product, backend, or PASS changes.
   - Validation evidence in the report is credible (re-run checks only if the report is ambiguous or stale).

4. Inspect `git status` and relevant `git diff` for each dirty repo. Compare against the report’s file list.

5. Produce a **Gate Review** with:
   - **Verdict:** `PASS` / `PASS_WITH_WARNINGS` / `FAIL` / `HOLD`
   - Scope compliance summary
   - Per-repo file assessment (safe / not safe to commit)
   - Exact paths safe to commit (must match report or explain divergence)
   - Exact paths that must **not** be staged
   - Proposed commit message(s) per repo
   - Whether `APPROVE_SAFE_COMMIT` is recommended, or repo-specific `APPROVE_FRONTEND_COMMIT` / `APPROVE_WORKSPACE_COMMIT` / `APPROVE_BACKEND_COMMIT` tokens

6. If verdict is `FAIL` or `HOLD`, do **not** recommend commit. List rework or follow-up mission instead.

---

## Hard rules

- Do **not** write product code, tests, or docs beyond the gate review output.
- Do **not** commit or push unless a separate `APPROVE_*_COMMIT` or `APPROVE_SAFE_COMMIT` token is provided in a **new** user message.
- Do **not** mark Visual Polish route `PASS`.
- Do **not** stage screenshot runs or generated artifacts.

---

## Return

- Gate verdict
- Scope compliance table
- Safe-to-commit files (exact paths, by repo)
- Must-not-stage list
- Proposed commit message(s)
- Current git status (`frontend/`, `workspace/`, `backend/`)
- Next human action (`APPROVE_SAFE_COMMIT`, repo-specific commit token, `HOLD`, or rework mission)
