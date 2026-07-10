# Session State Synchronization — Closure Phase

**SOT:** AI Dev OS `execution/SESSION_CLOSURE.md` (adopted v2.2.0 candidate @ `aafe470`)  
**Template:** AI Dev OS `templates/AUTONOMOUS_SESSION_REPORT_TEMPLATE.md`  
**Project paths:** `workspace/` (not `docs/`)

Use as:

1. **Final phase** of [`prompts/AUTONOMOUS_SESSION_PROMPT.md`](AUTONOMOUS_SESSION_PROMPT.md) — mandatory.
2. **Standalone sync/recovery** — reconcile queue with reports/gates; **no** disposition implied.
3. **Human disposition** — resolve PASS WITH WARNINGS for one mission; OS mutates governance state.

### Command — sync only (no disposition)

```text
APPROVE_SESSION_CLOSURE
Session: SESSION-{YYYYMMDD-HHMM}
```

Optional: omit `Session:` to reconcile missions with reports/gates but incomplete queue sync. **Must not** change `human_disposition` from `pending` to `accepted` without `Disposition:` line.

### Command — human disposition (PASS WITH WARNINGS)

```text
APPROVE_SESSION_CLOSURE
Session: SESSION-{ID}
Mission: {MISSION_ID}
Disposition: {accepted|remediation_required|deferred|terminated}
```

Supported `Disposition:` values only: `accepted` · `remediation_required` · `deferred` · `terminated`

**Human approves. OS performs queue and handoff mutation.** Humans must not manually edit `NEXT_ACTION_QUEUE.md` or `PROJECT_STATUS.md` for disposition under normal operation.

---

## Purpose

Synchronize `workspace/NEXT_ACTION_QUEUE.md` and session report with mission execution reports and gate results **without** commit or push.

---

## Read first

- `workspace/AI_CONTEXT.md`, `workspace/STACK_CONSTRAINTS.md`
- `workspace/NEXT_ACTION_QUEUE.md`
- `workspace/PROJECT_STATUS.md`
- `workspace/MISSION_EXECUTION_GUIDE.md`
- Mission reports and gate artifacts for every mission in scope
- Existing partial `workspace/reports/missions/SESSION-*_REPORT.md` if recovering interrupted closure

---

## Hard rules

- **Do not** commit or push.
- **Do not** use `git add .`.
- **Do not** mark **DONE** without execution report + gate evidence per Gate → DONE eligibility.
- **Do not** mark **DONE** when `gate_result: PASS WITH WARNINGS` unless human sent `Disposition: accepted` in the **same** invocation.
- **Do not** set or change `human_disposition` to `accepted`, `remediation_required`, `deferred`, or `terminated` without explicit `Disposition:` line.
- **Do not** flatten **PASS WITH WARNINGS** to PASS.
- **Do not** set DONE on gate **FAIL** or **HOLD**.
- **Do not** unlock dependent missions when a dependency has `gate_result: PASS WITH WARNINGS` and `human_disposition: pending`.
- **Do not** modify product code or routes — governance files only.
- **Do not** write project state into `C:\ai-dev-os`.
- **Stop** on contradictory evidence.
- **Idempotent** — safe to re-run.

---

## Mode A — Sync / recovery (no `Disposition:`)

Follow closure algorithm in AI Dev OS `execution/SESSION_CLOSURE.md`. Reconcile evidence; set `human_disposition: pending` for PASS WITH WARNINGS; **never** imply acceptance.

### Procedure

1. **Baseline** — session ID, queue snapshot, `PROJECT_STATUS` handoff excerpt, `git status` per repo (`workspace`, `frontend`, `backend`).
2. **Gather missions** — all missions selected in session, or missions with reports not reflected in queue.
3. **Per-mission reconcile** — read brief, execution report, gate result; update queue row evidence fields; apply transition rules.
4. **Queue-level** — recompute dependencies; ensure no DONE mission remains READY; update Last updated.
5. **PROJECT_STATUS** — handoff fields only.
6. **Finalize session report** — pre-state, post-state, sync result, warnings preserved.
7. **Stop** — no commit, no push.

---

## Mode B — Human disposition (`Disposition:` required)

Run **only** when human sends `Mission:` and `Disposition:` with `APPROVE_SESSION_CLOSURE`.

Validate evidence (execution report, gate PASS WITH WARNINGS, warnings preserved, session/mission ID match). If validation fails → **STOP**; no queue mutation.

Apply disposition per AI Dev OS `SESSION_CLOSURE.md` § Human disposition. **STOP** after — no commit, no push, no next mission execution.

---

## Return

| Field | Content |
|-------|---------|
| Closure verdict | SYNCED \| PARTIAL \| FAILED |
| Session report path | |
| Missions marked DONE | |
| Missions still READY / BLOCKED | |
| Warnings preserved | |
| Next recommended mission | |
| Governance files changed | explicit list |
| Product files changed | explicit list (if any) |
| Safe-to-commit allowlist | per repo |
| Anomalies | any evidence gaps |

---

## Examples

**Standalone sync after interrupted session:**

```text
APPROVE_SESSION_CLOSURE
Session: SESSION-20260710-1721
```

**Accept warnings after S-21 stop:**

```text
APPROVE_SESSION_CLOSURE
Session: SESSION-20260710-1721
Mission: M-008
Disposition: accepted
```
