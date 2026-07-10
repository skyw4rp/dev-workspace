# Autonomous Session Orchestrator — `APPROVE_AUTONOMOUS_SESSION`

**Command (user sends):**

```text
APPROVE_AUTONOMOUS_SESSION
```

Optional parameters (same message, one per line):

```text
APPROVE_AUTONOMOUS_SESSION
Max missions: 3
Commits: disabled
Mission types: A,B,C,D
Missions: auto
Stop on: FAIL,HOLD,scope-violation
```

**Executor:** Melómanos Market AI Dev OS Lead Engineer and Adoption Agent (session orchestrator role).

---

## Purpose

Run **multiple bounded missions** in one approved session using existing single-mission prompts as building blocks:

1. Execute mission → 2. Gate review → 3. (Optional) safe commit → repeat until limits or stop.

This reduces human mediation versus sending `APPROVE_NEXT_MISSION` repeatedly, while preserving gates and stop conditions.

---

## Read first

- `workspace/AI_CONTEXT.md`
- `workspace/STACK_CONSTRAINTS.md`
- `workspace/NEXT_ACTION_QUEUE.md`
- `workspace/MISSION_EXECUTION_GUIDE.md`
- `workspace/prompts/RUN_SELECTED_MISSION_PROMPT.md`
- `workspace/prompts/GATE_REVIEW_PROMPT.md`
- `workspace/prompts/SAFE_COMMIT_GATE_PROMPT.md`

---

## Session parameters (defaults)

| Parameter | Default | Notes |
|-----------|---------|-------|
| **Max missions** | `3` | Hard stop after N missions complete (execute + report), whether or not committed |
| **Commits** | `disabled` | `enabled` only if user explicitly sets `Commits: enabled` in the approval message |
| **Mission types** | `A,B,C,D` | Never auto-run **TYPE F** or **TYPE H** unless user explicitly lists them in `Mission types:` |
| **Missions** | `auto` | `auto` = pick from queue per `RUN_NEXT_MISSION` rules; or explicit list e.g. `M-015,M-006` |
| **Stop on** | `FAIL,HOLD,scope-violation` | End session early; write session report |
| **Visual polish** | `no PASS` | Never mark route PASS in a session |

If the user omits parameters, use defaults.

---

## Session loop

For each mission slot (1..Max missions):

### A. Select mission

- If `Missions: auto` — select highest-priority `READY` mission from `NEXT_ACTION_QUEUE.md` (same rules as `APPROVE_NEXT_MISSION`).
- If explicit list — take next ID not yet run this session.
- If mission type not in allowed types → **STOP** session; report.
- If no `READY` mission → end session normally (not a failure).

Announce: `Session mission N/Max: M-XXX — <title>`.

### B. Execute

Follow `workspace/prompts/RUN_SELECTED_MISSION_PROMPT.md` for `M-XXX`.

Write `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md`.

If verdict is `FAIL` or `STOPPED` and `Stop on` includes `FAIL` → go to **Session end**.

### C. Gate review (inline)

Follow `workspace/prompts/GATE_REVIEW_PROMPT.md` for the same `M-XXX`.

Record gate verdict in the session log.

If gate is `FAIL` or `HOLD` and `Stop on` includes it → go to **Session end**.

Do **not** implement fixes during gate review.

### D. Commit (only if enabled)

If `Commits: enabled` **and** gate verdict is `PASS` or `PASS_WITH_WARNINGS`:

Follow `workspace/prompts/SAFE_COMMIT_GATE_PROMPT.md` for `M-XXX`.

If commit fails or unexpected staged files → **STOP** session.

If `Commits: disabled` — record safe-to-commit files; do not commit.

### E. Continue

If more mission slots remain and no stop fired → next mission.

---

## Hard rules (entire session)

- Do **not** exceed **Max missions**.
- Do **not** run TYPE **F** / **H** unless explicitly allowed in session parameters.
- Do **not** commit when `Commits: disabled` (default).
- Do **not** use `git add .`.
- Do **not** stage `runs/**`, PNG/ZIP evidence, `.env`, `test-results/**`, `playwright-report/**`, `logs/**`.
- Do **not** mark Visual Polish route `PASS`.
- Do **not** weaken stop conditions from mission briefs.
- One mission at a time — finish execute → gate → (commit) before starting the next.

---

## Session report (required)

At session end, write:

`workspace/reports/missions/SESSION-<YYYYMMDD-HHMM>_REPORT.md`

Include:

| Section | Content |
|---------|---------|
| Verdict | `PASS` / `PASS_WITH_WARNINGS` / `STOPPED` / `FAIL` |
| Parameters used | Max missions, commits, types, mission list |
| Per-mission table | ID, execute verdict, gate verdict, committed? (Y/N), SHAs |
| Missions skipped / not started | Reason |
| Stop condition hit | If any |
| Git status | `frontend/`, `workspace/`, `backend/` |
| Safe-to-commit backlog | Files not committed when `Commits: disabled` |
| Recommended next action | Next mission or `APPROVE_AUTONOMOUS_SESSION` with updated params |

---

## Return (to human)

- Session verdict
- Missions completed (table)
- Commits made (if any) with SHAs
- Session report path
- Git status all repos
- What to send next (`APPROVE_SAFE_COMMIT`, `APPROVE_AUTONOMOUS_SESSION`, `HOLD`, etc.)

---

## Example (execute + gate only, no commits)

```text
APPROVE_AUTONOMOUS_SESSION
Max missions: 2
Commits: disabled
Missions: auto
```

## Example (execute + gate + commit)

```text
APPROVE_AUTONOMOUS_SESSION
Max missions: 1
Commits: enabled
Missions: M-015
```
