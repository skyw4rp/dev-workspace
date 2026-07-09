# M-001 — Audit Visual Polish / Visual Feedback Loop status

| Field | Value |
|-------|--------|
| **Mission ID** | M-001 |
| **Title** | Audit Visual Polish / Visual Feedback Loop status |
| **Mission type** | **TYPE A — Review Only** |
| **Priority** | P0 |
| **Status** | READY |
| **Product** | Melómanos Market |
| **Pattern** | One mission → one execution report → one gate review |

---

## Goal

Audit the current Visual Polish Gate and Visual Feedback Loop adoption state. Produce a clear snapshot of route readiness, evidence strategy, and open visual debt. Recommend the **safest next TYPE C** (frontend low-risk polish) mission — without implementing anything.

---

## Scope (allowed)

Read-only inspection of:

- `workspace/VISUAL_POLISH_CONTROL.md`
- `workspace/VISUAL_POLISH_ROUTES.json`
- `workspace/VISUAL_POLISH_STATUS.md`
- `workspace/VISUAL_FEEDBACK_LOOP_CONTROL.md`
- `workspace/screenshots/visual-polish/` (README + folder structure; list runs — do not edit images)
- `workspace/reports/visual-audit/`
- Related visual-polish reports under `workspace/reports/visual-polish/` and UX split reports under `workspace/reports/ux/` if needed for context
- `workspace/MISSION_EXECUTION_GUIDE.md` and `workspace/NEXT_ACTION_QUEUE.md` (for recommendation alignment)

Optional: `git status` in `workspace/`, `frontend/`, `backend/` to confirm no unexpected product drift (report only).

Write:

- `workspace/reports/missions/M-001_EXECUTION_REPORT.md`

---

## Forbidden changes

- No frontend component or CSS changes
- No backend code or schema changes
- No business logic, auth, reservation, messaging, payment, listing, order, or WebPay changes
- No screenshot create/edit/delete
- No staging of `runs/**` or unapproved evidence
- No marking any route or gate **PASS**
- No commits / pushes
- No starting M-002+ implementation in this mission
- Do not replace or rewrite Visual Polish / Feedback Loop control docs (read only; suggest follow-ups in the report if gaps exist)

---

## Acceptance criteria

1. Execution report exists at `workspace/reports/missions/M-001_EXECUTION_REPORT.md`.
2. Report includes current Visual Polish gate summary (Home approval, adoption status).
3. Report includes route status snapshot (from JSON/status) with P0/P1 highlights.
4. Report describes screenshot evidence strategy (runs vs approved baselines).
5. Report lists open visual debt / IN_REVIEW / NEEDS_SCREENSHOT_VERIFICATION items.
6. Report recommends **one** safest next TYPE C mission (or explicitly recommends another TYPE A first) with rationale.
7. Report includes Git Gate Review: docs touched this mission (if any beyond the report), and files that must NOT be committed.
8. Verdict is `PASS`, `PASS WITH WARNINGS`, or `FAIL` / `STOPPED` with reasons.

---

## Verification required

| Check | Required |
|-------|----------|
| Read control + routes + status + feedback loop docs | Yes |
| Inspect screenshot folder strategy (README / runs listing) | Yes |
| Skim recent visual-audit reports | Yes |
| Product code changes | Must remain **no** |
| `npm` / pytest / E2E | Not required for TYPE A |
| Commit | Forbidden |

---

## Dependencies

None. This is the recommended first mission.

---

## Stop conditions

Stop immediately and write the report if:

- Completing the audit would require editing product code
- Human asks mid-mission to “just polish Profile” → do not; recommend M-002/M-003
- Critical control files are missing → `PASS WITH WARNINGS` or `STOPPED` with gap list
- Pressure to mark routes PASS → refuse; document

---

## Continue conditions

Continue only while:

- Work remains read-only (+ writing the execution report)
- No second mission is started
- No files outside the allowed write path are modified

---

## Output template (execution report)

Use at least:

```markdown
## M-001 Execution Report

### Verdict
### Visual Polish / Feedback Loop snapshot
### Route readiness highlights
### Evidence strategy
### Open debt
### Recommended next mission
### Validation results
| Check | Result |
### Git Gate Review
### Remaining risks or warnings
```

---

## Executor prompt

Copy into the next Cursor session:

```text
APPROVE_MISSION_EXECUTION
Mission: M-001

Act as Melómanos Market AI Dev OS Mission Executor.

Read:
- workspace/MISSION_EXECUTION_GUIDE.md
- workspace/NEXT_ACTION_QUEUE.md
- workspace/missions/M-001_AUDIT_VISUAL_POLISH_FEEDBACK_LOOP.md

Execute M-001 only (TYPE A — Review Only).

Inspect Visual Polish and Visual Feedback Loop artifacts listed in the brief.
Write workspace/reports/missions/M-001_EXECUTION_REPORT.md.

Do NOT modify frontend or backend code.
Do NOT modify screenshots.
Do NOT mark any route PASS.
Do NOT commit.
Do NOT push.
Do NOT start another mission.

Return the execution report summary and the recommended next mission.
```

---

## Gate review prompt (after report)

```text
GATE_REVIEW for M-001

Read workspace/missions/M-001_AUDIT_VISUAL_POLISH_FEEDBACK_LOOP.md
and workspace/reports/missions/M-001_EXECUTION_REPORT.md.

Confirm TYPE A scope compliance.
List files safe to commit (workspace report/docs only).
List files that must NOT be committed.
Propose workspace commit message if applicable.

Do not implement. Do not commit unless APPROVE_WORKSPACE_COMMIT is provided with exact paths.
```

---

*Brief created 2026-07-08 as part of bounded mission adoption. Docs-only.*
