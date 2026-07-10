# Run Selected Mission — `APPROVE_MISSION_EXECUTION`

**Command (user sends):**

```text
APPROVE_MISSION_EXECUTION
Mission: M-XXX
```

Replace `M-XXX` with the mission ID (e.g. `M-002`, `M-012`).

**Executor:** Melómanos Market AI Dev OS Lead Engineer and Adoption Agent.

---

## Instructions

1. Read first:
   - `workspace/AI_CONTEXT.md`
   - `workspace/STACK_CONSTRAINTS.md`
   - `workspace/PROJECT_STATUS.md`
   - `workspace/NEXT_ACTION_QUEUE.md`
   - `workspace/MISSION_EXECUTION_GUIDE.md`
   - `workspace/reports/missions/` (prior related reports if useful)
   - Mission entry for `M-XXX` in `NEXT_ACTION_QUEUE.md`

2. Open the mission brief:
   - `workspace/missions/M-XXX_*.md`
   - If missing and the queue says “create at execution start if missing”, create it from the queue entry only. Otherwise **STOP** and report.

3. Confirm mission type (`A`–`H`), scope, forbidden changes, acceptance criteria, verification, dependencies, and stop conditions from the brief and queue.

4. Execute **only** mission `M-XXX` within bounds. Prefer the smallest correct change set.

5. Write `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md` including at minimum:
   - Verdict (`PASS` / `PASS_WITH_WARNINGS` / `FAIL` / `STOPPED`)
   - Mission scope confirmation table
   - What was inspected or changed
   - Validation results
   - Warnings / stop conditions hit (if any)
   - Recommended next mission
   - Git status (`frontend/`, `workspace/`, `backend/`)
   - **Git Gate Review** — files safe / not safe to commit; proposed commit message(s)

---

## Hard rules

- Do **not** start another mission ID in the same session.
- Do **not** expand scope beyond the brief (no “while here” polish, fixes, or refactors).
- Do **not** modify frontend or backend unless the mission type and brief allow it.
- Do **not** modify screenshots, approved baselines, or route PASS status unless the brief explicitly allows it (default: never).
- Do **not** use v0 unless the mission brief explicitly allows it for TYPE C visual work.
- Do **not** commit or push.
- Do **not** stage `workspace/screenshots/visual-polish/runs/**`, unapproved PNG/ZIP evidence, `.env`, `test-results/**`, `playwright-report/**`, or `logs/**`.
- Do **not** use `git add .`.

---

## Type reminders

| Type | Default code changes |
|------|----------------------|
| **A** | Review only — reports/docs in scope only |
| **B** | Workspace docs / governance only |
| **C** | Frontend low-risk visual polish only |
| **D** | Tests / capture / verification tooling |
| **E** | Backend low-risk (no BUSINESS_RULES) |
| **F** / **H** | Requires explicit approval; read `backend/BUSINESS_RULES.md` first |
| **G** | Product design / specs only — no implementation |

When uncertain, choose the more conservative type and **STOP**.

---

## Return

- Short summary and verdict
- Files created / updated (by repo)
- Validation results
- Recommended next mission
- Git status for all three repos
- Safe-to-commit files from Git Gate Review
- **Wait for** `APPROVE_GATE_REVIEW` or `APPROVE_SAFE_COMMIT` before any commit.
