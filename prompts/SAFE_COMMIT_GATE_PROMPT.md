# Safe Commit Gate — `APPROVE_SAFE_COMMIT`

**Command (user sends):**

```text
APPROVE_SAFE_COMMIT
Mission: M-XXX
```

Replace `M-XXX` with the mission ID whose execution report authorizes commits.

**Executor:** Melómanos Market AI Dev OS Lead Engineer and Adoption Agent (commit gate role).

---

## Instructions

1. Read:
   - `workspace/MISSION_EXECUTION_GUIDE.md`
   - `workspace/reports/missions/M-XXX_EXECUTION_REPORT.md` — **Git Gate Review** section (required)
   - Optional: output from a prior `APPROVE_GATE_REVIEW` for the same mission

2. If the execution report is missing or Git Gate Review lists no safe files, **STOP** and report.

3. **Before staging**, inspect every listed file:
   - `git diff -- <path>` per file (or `git diff --cached` if already staged)
   - Confirm changes match mission scope (type, forbidden paths, no surprise logic)
   - If any file fails inspection, **STOP** — do not stage or commit

4. Run validations required by the execution report **before** committing (e.g. `npm run build`, `npm run test:e2e`, `npm run test:e2e:visual-polish`, `py run_melomanos.py --check`, `py -m pytest`). Skip only what the report explicitly marks N/A.

5. Stage **file-by-file only** — never `git add .`:
   - Frontend files → `C:\melomanos\frontend`
   - Workspace files → `C:\melomanos\workspace`
   - Backend files → `C:\melomanos\backend`
   - One repo at a time; verify `git status` after each staging batch

6. If any unexpected file appears staged, **STOP**, unstage, and report.

7. Commit per repo using the message(s) from the execution report (or gate review). Prefer **separate commits** per repo.

8. Push each repo after its commit succeeds.

---

## Must NOT stage

- `workspace/screenshots/visual-polish/runs/**`
- `workspace/screenshots/visual-polish/*.png` (unless report explicitly lists an approved baseline promotion — rare)
- `workspace/screenshots/visual-polish/*.zip`
- `frontend/test-results/**`
- `frontend/playwright-report/**`
- `test-results/**`
- `logs/**`
- Any `.env` or secrets file
- Any path not listed in the execution report Git Gate Review safe list

---

## Hard rules

- Do **not** commit files outside the safe list.
- Do **not** amend commits unless user rules allow and hooks require it.
- Do **not** update git config.
- Do **not** force-push.
- Do **not** mark Visual Polish route `PASS` via commit.

---

## Return

- Per-repo commit SHA(s)
- Commit message(s) used
- Validation results (re-run summary)
- `git status` for `frontend/`, `workspace/`, `backend/`
- Confirmation that no forbidden artifacts were staged
