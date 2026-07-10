# M-018 — Autonomous Session Orchestrator

**Mission ID:** M-018  
**Type:** TYPE B — Workflow / Governance  
**Priority:** P1  
**Command:** `APPROVE_AUTONOMOUS_SESSION`

---

## Goal

Add a bounded multi-mission session orchestrator so one human approval can run several missions (execute → gate review → optional safe commit) under explicit limits and stop conditions.

---

## Scope

- `workspace/prompts/AUTONOMOUS_SESSION_PROMPT.md`
- `workspace/MISSION_EXECUTION_GUIDE.md` — session command + artifact
- `workspace/NEXT_ACTION_QUEUE.md` — M-018 entry DONE

---

## Forbidden

- Frontend / backend / product code
- Screenshots
- Business logic
- Commits during M-018 execution
- Route PASS

---

## Acceptance criteria

1. `APPROVE_AUTONOMOUS_SESSION` prompt with defaults and optional parameters
2. Session loop composes existing single-mission prompts
3. Session report convention documented
4. Mission guide updated
5. M-018 execution report

---

## Verification

Docs inspection; git status shows only expected workspace paths.
