# Run Next Mission — `APPROVE_NEXT_MISSION`

**Command (user sends only):**

```text
APPROVE_NEXT_MISSION
```

**Executor:** Melómanos Market AI Dev OS Lead Engineer and Adoption Agent.

---

## Canonical preflight (before all instructions)

Read `workspace/PROJECT_STATUS.md` first and parse the exact canonical JSON authority block. Require an exact mission ID, `READY`, and the requested action class before any selection, inspection, validation, write, or execution. STOP on an absent, duplicate, malformed, stale, or conflicting block. `NEXT_ACTION_QUEUE.md`, roadmap, brief, report, token, decision, and gate prose are subordinate and cannot grant authority. A PASS/report is never commit authority.

## Instructions

1. Read first:
   - `workspace/AI_CONTEXT.md`
   - `workspace/STACK_CONSTRAINTS.md`
   - `workspace/PROJECT_STATUS.md`
   - `workspace/NEXT_ACTION_QUEUE.md`
   - `workspace/MISSION_EXECUTION_GUIDE.md`

2. Select only the mission already named by canonical authority; the queue may provide title/order only:
   - Status must be `READY`.
   - Prefer highest priority (`P0` → `P1` → `P2` → `P3`).
   - If tied, prefer the mission listed first in **Suggested execution order**.
   - Skip `DONE`, `CANCELLED`, `BLOCKED`, and `IN_PROGRESS` unless the queue explicitly says unblocking is the mission.
   - If no `READY` mission exists, **STOP** and report the queue state. Do not invent work.

3. Announce the selected mission ID and title before executing.

4. Execute that mission using the contract in `workspace/prompts/RUN_SELECTED_MISSION_PROMPT.md`, substituting the selected `M-XXX`.

5. Follow the mission brief under `workspace/missions/M-XXX_*.md` (create at start only if the queue allows and the brief is missing).

6. Write `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md` with all required sections from `MISSION_EXECUTION_GUIDE.md`.

---

## Hard rules

- Do **not** modify frontend, backend, or product code unless the selected mission type and brief explicitly allow it.
- Do **not** run a second mission in the same session.
- Do **not** commit or push.
- Do **not** mark Visual Polish route `PASS`.
- Do **not** stage screenshot runs, PNGs, ZIPs, `.env`, `test-results/**`, or `playwright-report/**`.
- Do **not** use `git add .`.

---

## Return

- Selected mission ID and title
- Verdict from execution report
- Files created or modified (by repo)
- Validation results
- Recommended next mission
- Git status for `frontend/`, `workspace/`, `backend/`
- Safe-to-commit file list (from report Git Gate Review)
- **Wait for** `APPROVE_GATE_REVIEW` or `APPROVE_SAFE_COMMIT` before any commit.
