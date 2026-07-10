# Mission Execution Guide — Melómanos Market

**System:** AI Dev OS Bounded Autonomous Mission Execution Layer (Melómanos adoption)  
**Product:** Melómanos Market  
**Pattern:** **One mission → one execution report → one gate review**

This guide adapts the base AI Dev OS bounded autonomy layer to Melómanos without replacing Visual Polish, Visual Feedback Loop, Quality Gate, or roadmap authority.

---

## Purpose

Reduce human mediation (copying long prompts between ChatGPT and Cursor) by:

1. Queuing **bounded missions** with explicit type, scope, and stop conditions.
2. Letting an executor run **one mission** to completion (or stop).
3. Writing **one execution report**.
4. Running a **separate gate review** before any commit.

Humans approve with short tokens instead of rewriting full prompts each time.

---

## Artifact layout

| Artifact | Path |
|----------|------|
| Next Action Queue | `workspace/NEXT_ACTION_QUEUE.md` |
| Stack constraints / tools | `workspace/STACK_CONSTRAINTS.md` |
| Mission briefs | `workspace/missions/M-XXX_*.md` |
| Mission execution reports | `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md` |
| Reusable prompt interfaces | `workspace/prompts/*.md` |
| Session reports | `workspace/reports/missions/SESSION-<YYYYMMDD-HHMM>_REPORT.md` |
| This guide | `workspace/MISSION_EXECUTION_GUIDE.md` |
| Visual Polish control | `workspace/VISUAL_POLISH_CONTROL.md` |
| Visual Feedback Loop | `workspace/VISUAL_FEEDBACK_LOOP_CONTROL.md` |
| Quality Gate | `workspace/QUALITY_GATE.md` |

Do **not** put mission briefs under `frontend/` or `backend/`.

---

## Mission type taxonomy (TYPE A–H)

Use the **most conservative** type when uncertain.

| Type | Name | Typical Melómanos use | Default commit policy |
|------|------|----------------------|------------------------|
| **A** | Review Only | Audits, status reads, route readiness, UX diagnosis | No code changes; docs/reports only if in scope |
| **B** | Docs / Governance | Queue updates, control docs, reports | Workspace docs only |
| **C** | Frontend Low-Risk | Visual polish, layout microfixes, shared CSS, E2E selector updates for IA | Frontend only; no business logic |
| **D** | Frontend Verification | E2E / visual-polish capture / build validation | Tests or capture only; prefer no product edits |
| **E** | Backend Low-Risk | Non-rule helpers, logging, test fixtures (rare) | Backend only; **no** BUSINESS_RULES changes |
| **F** | Backend / Business Logic | Auth, escrow, messaging, payment, listings, orders, WebPay | Explicit approval required |
| **G** | Product Design | Specs, IA plans, bounties product brief | Docs only; **no** implementation |
| **H** | Cross-cutting / High Risk | Multi-repo features, migrations, production deploy | Explicit multi-token approval |

### Melómanos mapping rules

- **Visual Polish** work → **TYPE C** (unless it becomes product redesign → **G** first).
- **Visual Feedback Loop** audits / evidence review → **TYPE A**.
- **Product / UX redesign / specs** → **TYPE G** until implementation is explicitly approved.
- **Backend / business rules** → **TYPE F** or **H**; never self-start from a TYPE A/C queue item.
- If unsure between implementation and review → choose **TYPE A**.

### Tool intelligence (summary)

Full rules: [`STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md).

- **Cursor** = primary tool for all real repo changes.
- **v0** = optional UI prototype for compatible TYPE C visual missions only.
- **Never** use v0 for backend, auth, database, reservations, security, tests, or production integration.
- v0 may propose UI; **Cursor integrates**; Melómanos git repos remain source of truth.

---

## How to run a mission

### 1. Pick one mission from the queue

Open `workspace/NEXT_ACTION_QUEUE.md`. Select a mission with status `READY` (or `BLOCKED` only if unblocking is the mission itself).

### 2. Confirm approval

Require an explicit human token:

```text
APPROVE_MISSION_EXECUTION
Mission: M-XXX
```

Without this token, do **not** execute product or code work. Docs-only TYPE A/B may proceed when the user explicitly asks to run that mission ID.

### 3. Read the brief

Open `workspace/missions/M-XXX_*.md`. Treat the brief as the contract:

- scope
- forbidden changes
- acceptance criteria
- verification required
- stop conditions

### 4. Execute within bounds

- Do only what the brief allows.
- Prefer the smallest change set.
- Do not start a second mission in the same session unless the human explicitly queues it after gate review.

### 5. Write the execution report

Create or update:

`workspace/reports/missions/M-XXX_EXECUTION_REPORT.md`

Minimum sections:

- Verdict (`PASS` / `PASS WITH WARNINGS` / `FAIL` / `STOPPED`)
- What was inspected or changed
- Validation results
- Recommended next mission
- Git Gate Review (files safe / not safe to commit)
- Stop conditions hit (if any)

### 6. Stop for gate review

Do **not** commit or push unless a separate commit approval token is given.

---

## Continue conditions

The executor **may continue** within the same mission when:

- Work remains inside the brief scope.
- No stop condition has fired.
- Validation steps listed in the brief are still runnable.
- Changes stay in the allowed repos/files.
- The mission has not yet produced its final report.

---

## Stop conditions

The executor **must stop** and write a report when any of these occur:

| Condition | Action |
|-----------|--------|
| Scope would expand into another mission | STOP; recommend next mission ID |
| Forbidden path touched (backend rules, HomeHero when forbidden, Admin redesign, etc.) | STOP |
| Business logic / auth / payment / messaging / escrow change needed | STOP; reclassify as TYPE F/H |
| Visual route PASS requested without human approval | STOP; do not mark PASS |
| Tests fail and fix is out of scope | STOP with FAIL |
| Ambiguous product decision requires Daniela/Ernesto | STOP; ask |
| Commit requested without approval token | STOP; provide Git Gate Review only |
| Screenshot evidence would be staged without approval | STOP; leave runs unstaged |

---

## Gate review (separate step)

After the execution report exists, run a **gate review** (same or new session) that only:

1. Reads the mission brief + execution report.
2. Confirms scope compliance.
3. Lists files safe / not safe to commit.
4. Proposes commit message(s).
5. Waits for an approval token.

Gate review must **not** continue implementation.

---

## Approval tokens

| Token | Meaning |
|-------|---------|
| `APPROVE_NEXT_MISSION` | Run highest-priority `READY` mission from queue — see [`prompts/RUN_NEXT_MISSION_PROMPT.md`](prompts/RUN_NEXT_MISSION_PROMPT.md) |
| `APPROVE_MISSION_EXECUTION` + `Mission: M-XXX` | Run the named mission per its brief — see [`prompts/RUN_SELECTED_MISSION_PROMPT.md`](prompts/RUN_SELECTED_MISSION_PROMPT.md) |
| `APPROVE_GATE_REVIEW` + `Mission: M-XXX` | Review-only gate on brief + execution report — see [`prompts/GATE_REVIEW_PROMPT.md`](prompts/GATE_REVIEW_PROMPT.md) |
| `APPROVE_SAFE_COMMIT` + `Mission: M-XXX` | Inspect diffs, validate, stage/commit/push per report safe list — see [`prompts/SAFE_COMMIT_GATE_PROMPT.md`](prompts/SAFE_COMMIT_GATE_PROMPT.md) |
| `APPROVE_AUTONOMOUS_SESSION` | Multi-mission session (execute → gate → optional commit → **mandatory closure**) — see [`prompts/AUTONOMOUS_SESSION_PROMPT.md`](prompts/AUTONOMOUS_SESSION_PROMPT.md) |
| `APPROVE_SESSION_CLOSURE` + `Session: SESSION-*` | Standalone queue sync / recovery after autonomous session — **no** disposition — see [`prompts/SESSION_STATE_SYNC_PROMPT.md`](prompts/SESSION_STATE_SYNC_PROMPT.md) |
| `APPROVE_SESSION_CLOSURE` + `Session:` + `Mission:` + `Disposition:` | Resolve PASS WITH WARNINGS for one mission — OS mutates queue; human does not edit disposition manually |
| `APPROVE_FRONTEND_COMMIT` | Stage/commit/push listed frontend files only (explicit path list) |
| `APPROVE_BACKEND_COMMIT` | Stage/commit/push listed backend files only |
| `APPROVE_WORKSPACE_COMMIT` | Stage/commit/push listed workspace files only |
| `HOLD` | Pause; do not commit; do not continue |
| `REJECT` | Reject outcome; do not commit; may require rework mission |

Commit approvals must list **exact file paths**. Use file-by-file staging. Never `git add .`.

---

## Commits

- Default: **do not commit**.
- One mission may produce changes in at most the repos allowed by its type.
- Prefer separate commits per repo (frontend / backend / workspace).
- Never stage:
  - `workspace/screenshots/visual-polish/runs/**`
  - unapproved `*.png` / `*.zip` evidence
  - `.env` / secrets
  - `test-results/**`, `playwright-report/**`, `logs/**`
- Visual route `PASS` is never granted by commit alone — human visual approval required per Visual Polish Control.

---

## Preventing scope mixing

| Anti-pattern | Correct pattern |
|--------------|-----------------|
| “While here, also polish Profile and fix messaging” | One mission only |
| Mixing TYPE G spec with TYPE C implementation | Spec mission first; implement later |
| Marking routes PASS after a polish pass | Leave IN_REVIEW; wait for Daniela/Ernesto |
| Backend “small fix” inside a frontend polish mission | STOP; open TYPE F mission |
| Committing screenshots with code | Separate evidence policy; usually do not commit runs |

---

## Integration with existing Melómanos systems

| System | Relationship |
|--------|--------------|
| **Visual Polish** | Still authoritative for palette, route status, human PASS |
| **Visual Feedback Loop** | Still authoritative for Capture → Approve evidence workflow |
| **Quality Gate** | Still required for functional DoD (`QUALITY_GATE.md`) |
| **MVP Roadmap** | Still authoritative for product backlog (`backend/MVP_ROADMAP.md`) |
| **Mission Queue** | Operational execution layer for bounded Cursor sessions |

Missions **orchestrate** work; they do not override business rules or visual human gates.

---

## Short Command Interface

Melómanos-local prompt files under `workspace/prompts/` let you send **short tokens** instead of pasting long executor prompts. The agent reads the matching prompt file and follows it.

| You send | Prompt file | Outcome |
|----------|-------------|---------|
| `APPROVE_NEXT_MISSION` | [`prompts/RUN_NEXT_MISSION_PROMPT.md`](prompts/RUN_NEXT_MISSION_PROMPT.md) | Picks highest-priority `READY` mission, executes, writes report |
| `APPROVE_MISSION_EXECUTION` + `Mission: M-XXX` | [`prompts/RUN_SELECTED_MISSION_PROMPT.md`](prompts/RUN_SELECTED_MISSION_PROMPT.md) | Executes named mission, writes report |
| `APPROVE_GATE_REVIEW` + `Mission: M-XXX` | [`prompts/GATE_REVIEW_PROMPT.md`](prompts/GATE_REVIEW_PROMPT.md) | Review-only; lists safe files; no implementation |
| `APPROVE_SAFE_COMMIT` + `Mission: M-XXX` | [`prompts/SAFE_COMMIT_GATE_PROMPT.md`](prompts/SAFE_COMMIT_GATE_PROMPT.md) | Inspects diffs, validates, commits per report safe list |
| `APPROVE_AUTONOMOUS_SESSION` | [`prompts/AUTONOMOUS_SESSION_PROMPT.md`](prompts/AUTONOMOUS_SESSION_PROMPT.md) | Multi-mission session under limits (default: no commits) |
| `APPROVE_SESSION_CLOSURE` + `Session: SESSION-*` | [`prompts/SESSION_STATE_SYNC_PROMPT.md`](prompts/SESSION_STATE_SYNC_PROMPT.md) | Mandatory finalization / recovery — sync queue with reports; no commit |

Repo-specific commit tokens (`APPROVE_FRONTEND_COMMIT`, `APPROVE_WORKSPACE_COMMIT`, `APPROVE_BACKEND_COMMIT`) remain available when you need an explicit path list instead of the report-driven safe-commit gate.

### Autonomous session (multi-mission)

One approval can run several bounded missions in sequence. Default: **execute + gate review only** (`Commits: disabled`). Enable commits only with explicit `Commits: enabled` in the same message.

```text
APPROVE_AUTONOMOUS_SESSION
Max missions: 3
Commits: disabled
Mission types: A,B,C,D
Missions: auto
```

Session output: per-mission reports plus **one** consolidated `SESSION-<YYYYMMDD-HHMM>_REPORT.md`.

**Melómanos session policy:** Count only gate `PASS` / `PASS_WITH_WARNINGS` toward max missions; sync queue after each completed mission; commit each repo separately; never push in-session; stop on mandatory stop conditions.

**Mandatory closure:** Every autonomous session **must** end with session state synchronization (Phase G in `AUTONOMOUS_SESSION_PROMPT.md` or standalone `APPROVE_SESSION_CLOSURE`). A session is **not complete** until the queue reflects execution reports and gate results.

**PASS WITH WARNINGS (S-21):** Closure **must not** auto-mark DONE. Set `BLOCKED` (or `IN_PROGRESS`) with `human_disposition: pending`. Human resolves via `APPROVE_SESSION_CLOSURE` + `Disposition:` — not manual queue edits.

### Autonomous session closure (mandatory)

After the last mission slot (or early stop):

1. Run [`prompts/SESSION_STATE_SYNC_PROMPT.md`](prompts/SESSION_STATE_SYNC_PROMPT.md) (Mode A — no `Disposition:` unless human sends it).
2. Update queue evidence fields (`execution_report`, `gate_result`, `completed_in_session`, `human_disposition`, etc.).
3. Finalize `SESSION-*_REPORT.md` with pre-session / post-session queue state.
4. **No commit. No push.**

### Examples

```text
APPROVE_NEXT_MISSION
```

```text
APPROVE_MISSION_EXECUTION
Mission: M-012
```

```text
APPROVE_GATE_REVIEW
Mission: M-013
```

```text
APPROVE_SAFE_COMMIT
Mission: M-013
```

```text
APPROVE_AUTONOMOUS_SESSION
Max missions: 2
Commits: disabled
```

Default after any mission run: **do not commit** until `APPROVE_GATE_REVIEW` and/or `APPROVE_SAFE_COMMIT` (or a repo-specific `APPROVE_*_COMMIT` with exact paths).

---

## How this reduces human mediation

| Before | After |
|--------|-------|
| Human pastes long custom prompts each turn | Human sends short mission ID + approval token |
| Scope drifts across ChatGPT ↔ Cursor | Brief + stop conditions bound the session |
| Mixed polish + product + commit in one go | One mission → one report → one gate → optional commit |
| Unclear next step | `NEXT_ACTION_QUEUE.md` holds READY missions |

---

*Adoption date: 2026-07-08. Docs-only; does not replace Visual Polish or Visual Feedback Loop.*
