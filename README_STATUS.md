# Project status document

## What is `PROJECT_STATUS.md`?

A short, human-readable snapshot of Melómanos Market. It answers:

- Did the last full audit pass?
- What is already in the MVP?
- What is the business model?
- What should we build next?

It lives in the dev workspace (`C:\melomanos_workspace`; see [README_PROJECT_LAYOUT.md](./README_PROJECT_LAYOUT.md)) and is meant for **Ernesto** and **Daniela** — no need to read commits or code.

## How Daniela can use it

1. Open `C:\melomanos_workspace\PROJECT_STATUS.md` in any text editor or on GitHub.
2. Check **Last Quality Gate** — date and whether backend, frontend, E2E, and full audit passed.
3. Check **Latest Release** — what was shipped last (backend/frontend messages or “No changes”).
4. Scan **Current MVP Features** and **Next Recommended Work** for planning and demos.

The file does not contain secrets, API keys, or user data.

## How `finish_task.py` updates it

After a **successful** finish (Quality Gate passed, workflow not aborted), you may see:

```
Update PROJECT_STATUS.md? (Y/N)
```

If you answer **Y**:

- **Last Quality Gate** is replaced with the current date/time and PASSED results from the audit you just ran.
- **Latest Release** is replaced with backend/frontend lines:
  - commit message if that repo was committed and pushed
  - `No changes.` if that repo was clean or skipped

Static sections (MVP features, business model, quality gate commands, roadmap) are left unchanged.

## Manual updates

You can edit `PROJECT_STATUS.md` by hand anytime (e.g. adjust **Next Recommended Work**). Keep the HTML comment markers around **Last Quality Gate** and **Latest Release** if you want `finish_task.py` to keep updating those blocks automatically.

## Related commands

| Command | Purpose |
|---------|---------|
| `py run_audit.py` | Run Quality Gate only |
| `py finish_task.py` | Quality Gate + optional commit/push + optional status update |

See also [README_AUDIT.md](./README_AUDIT.md) and [README_FINISH_TASK.md](./README_FINISH_TASK.md).
# Operational authority

Status prose and roadmap entries are descriptive only. Before invoking this status tool, read and parse the exact canonical JSON block in `PROJECT_STATUS.md`; require the exact mission, `READY`, and the requested action class. The tool fails closed and status writes must preserve that block.
