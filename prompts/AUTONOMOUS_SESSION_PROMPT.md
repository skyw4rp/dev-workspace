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

## Canonical preflight (before all instructions)

Read `workspace/PROJECT_STATUS.md` first and parse its exact canonical JSON authority block. A session may operate only on its exact sole `READY` mission and explicit action classes. STOP on absent, duplicate, malformed, stale, or conflicting authority. Queue, roadmap, brief, report, token, decision, and gate output are subordinate and cannot authorize a mission, commit, or scope expansion. Gates are read-only unless a named validation command is explicitly allowed.

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
| **Max missions** | `3` | Hard stop after **N gate-completed** missions (`PASS` or `PASS_WITH_WARNINGS` only) |
| **Commits** | `disabled` | `enabled` only if user explicitly sets `Commits: enabled` in the approval message |
| **Mission types** | `A,B,C,D` | Never auto-run **TYPE F** or **TYPE H** unless user explicitly lists them in `Mission types:` |
| **Missions** | `auto` | `auto` = pick from queue per `RUN_NEXT_MISSION` rules; or explicit list e.g. `M-015,M-006` |
| **Stop on** | `FAIL,HOLD,scope-violation` | End session early; write session report |
| **Visual polish** | `no PASS` | Never mark route PASS in a session |

If the user omits parameters, use defaults.

---

## Melómanos session policy (mandatory)

| Rule | Requirement |
|------|-------------|
| **Completed mission count** | Count **only** missions whose **gate** verdict is `PASS` or `PASS_WITH_WARNINGS` toward `Max missions`. Execute-only or gate `FAIL` / `HOLD` / `STOPPED` do **not** count as completed slots. |
| **Per-mission queue sync** | After **every** gate `PASS` or `PASS_WITH_WARNINGS`, synchronize `NEXT_ACTION_QUEUE.md` for that mission **before** starting the next mission. Do **not** defer all queue updates to session end. |
| **Separate repo commits** | When `Commits: enabled`, commit **each repository separately** (frontend, workspace, backend) — one commit per repo per mission when that repo has safe files. Never batch cross-repo commits. |
| **No push in session** | **Never** push during an autonomous session — even if `SAFE_COMMIT_GATE_PROMPT.md` mentions push. Record `push_status: pending_approval` on queue rows. |
| **Mandatory stops** | **Stop** the session on any mandatory stop condition: gate `FAIL` or `HOLD` (when `Stop on` includes them), scope violation, unexpected staged files, commit failure, contradictory evidence, PASS WITH WARNINGS when session must halt (S-21), or `Max missions` reached. |
| **Consolidated session report** | At session end, produce **one** consolidated `SESSION-<YYYYMMDD-HHMM>_REPORT.md` covering all missions, commits, queue sync results, and final git state. Phase F finalizes this report; do not scatter session verdicts across multiple session files. |

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

If gate is `FAIL` or `HOLD` and `Stop on` includes it → go to **Session end** (does **not** count toward `Max missions`).

If gate is `PASS` or `PASS_WITH_WARNINGS` → mission counts as **completed** toward `Max missions`.

Do **not** implement fixes during gate review.

### D. Per-mission queue sync (mandatory)

Immediately after gate `PASS` or `PASS_WITH_WARNINGS`, update `NEXT_ACTION_QUEUE.md` for **this mission only**:

- Apply evidence fields per [`SESSION_STATE_SYNC_PROMPT.md`](SESSION_STATE_SYNC_PROMPT.md)
- `PASS` → may set `DONE`
- `PASS WITH WARNINGS` → `BLOCKED` + `human_disposition: pending`; preserve warnings
- Update summary row and **Last updated** metadata

If commits are enabled, include the queue update in the **workspace** commit for this mission (same mission batch).

### E. Commit (only if enabled)

If `Commits: enabled` **and** gate verdict is `PASS` or `PASS_WITH_WARNINGS`:

Follow `workspace/prompts/SAFE_COMMIT_GATE_PROMPT.md` for `M-XXX` — **except do not push** (Melómanos session policy).

Commit **each repository separately** when that repo has safe files from the report.

If commit fails or unexpected staged files → **STOP** session.

If `Commits: disabled` — record safe-to-commit files; do not commit.

### F. Continue

If gate-completed count < `Max missions` and no stop fired → next mission.

### G. Session closure (mandatory — finalize consolidated report)

After the last mission slot or early stop:

1. Verify per-mission queue sync is complete (repair any gap idempotently).
2. Recompute dependencies and next-mission recommendation across all session missions.
3. Finalize **one** consolidated `SESSION-<YYYYMMDD-HHMM>_REPORT.md` with pre-session / post-session queue state and closure sync result.
4. **No commit** for closure-only artifacts unless `Commits: enabled` and queue/report listed in a final workspace batch — **never push**.

If any mission ended with PASS WITH WARNINGS, session report **must** recommend `APPROVE_SESSION_CLOSURE` + `Disposition:` — not manual queue edit.

---

## Hard rules (entire session)

- Do **not** exceed **Max missions**.
- Do **not** run TYPE **F** / **H** unless explicitly allowed in session parameters.
- Do **not** commit when `Commits: disabled` (default).
- Do **not** **push** during the session — **ever** (record `push_status: pending_approval`).
- Do **not** defer `NEXT_ACTION_QUEUE.md` updates to session end — sync after each gate-completed mission.
- Do **not** count missions toward `Max missions` unless gate is `PASS` or `PASS_WITH_WARNINGS`.
- Do **not** use `git add .`.
- Do **not** stage `runs/**`, PNG/ZIP evidence, `.env`, `test-results/**`, `playwright-report/**`, `logs/**`.
- Do **not** mark Visual Polish route `PASS`.
- Do **not** weaken stop conditions from mission briefs.
- One mission at a time — finish execute → gate → queue sync → (commit per repo) before the next mission.

---

## Session report (required)

At session end, write:

`workspace/reports/missions/SESSION-<YYYYMMDD-HHMM>_REPORT.md`

Include:

| Section | Content |
|---------|---------|
| Verdict | `PASS` / `PASS_WITH_WARNINGS` / `STOPPED` / `FAIL` |
| Parameters used | Max missions, commits, types, mission list |
| Per-mission table | ID, execute verdict, gate verdict, queue synced? (Y/N), committed? (Y/N), SHAs |
| Missions skipped / not started | Reason |
| Stop condition hit | If any |
| Git status | `frontend/`, `workspace/`, `backend/` |
| Safe-to-commit backlog | Files not committed when `Commits: disabled` |
| Recommended next action | Next mission or `APPROVE_SESSION_CLOSURE` with updated params |
| **Closure sync result** | SYNCED / PARTIAL / FAILED |
| **Pre-session queue snapshot** | Summary table |
| **Post-session queue snapshot** | Summary table |
| **Missions pending human disposition** | IDs with PASS WITH WARNINGS + `human_disposition: pending` |

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
