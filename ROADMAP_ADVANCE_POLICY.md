# Roadmap Advance Policy

> **Operational authority notice.** [`PROJECT_STATUS.md`](PROJECT_STATUS.md) is the sole cross-repository authority that can authorize an active task or READY mission. `NEXT_ACTION_QUEUE.md` and [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) are subordinate planning references. No roadmap, queue, mission brief, plan, report, checklist, or runbook — including this policy — can authorize execution by itself.

Prevents **premature auto-advance** of `MVP_ROADMAP.md` when only part of a multi-phase epic is done (e.g. WebPay Phase 1 shipped while phases 2–7 remain).

**Enforced by:** `finish_task.py` / `roadmap_advance.py` (see [README_FINISH_TASK.md](./README_FINISH_TASK.md)).

**Roadmap role:** [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) is subordinate product planning, not an active-task source or execution authority.

---

## Terminology

All task and active-task terminology in this policy is historical or subordinate roadmap terminology, not operational authorization.

| Term | Meaning | Example |
|------|---------|---------|
| **Epic** | A subordinate roadmap planning item spanning multiple deliverables or phases | Payment Provider Integration (WebPay placeholder) |
| **Phase** | An internal implementation slice inside one epic; not a separate roadmap milestone | WebPay Phase 1: shared `confirm_order_payment_held` service |
| **Task** | A single scoped unit of work (often one phase or one repo change set) | Extract payment confirm service; add checkout session migration |
| **Release** | A Quality Gate–passed commit/push via `finish_task.py` | Backend tests green → commit → push |

**Rule:** Completing a **phase** or **task** inside an epic does **not** complete the **epic**. Only the whole roadmap item may move to **Completed**.

---

## When auto-advance is allowed

This section describes historical/conditional tooling behavior only. It cannot select, promote, or authorize work; only `PROJECT_STATUS.md` can do so.

`finish_task.py` may advance **Current Active Task → Completed** and promote the next queue item **only when the entire roadmap item is complete** — not when an internal phase finishes.

| Scenario | Advance? |
|----------|----------|
| WebPay Phase 1 complete (phases 2–7 remain) | **No** |
| WebPay all 7 phases complete + DoD met | **Yes** |
| Admin Panel MVP backend + frontend complete + tests/E2E | **Yes** |
| Docs-only correction (no release) | **No** (advance runs only after successful release) |

---

## Required checklist before advancing

Before answering **Y** / typing **ADVANCE** / using `--advance-roadmap`, confirm:

1. **All planned phases** for the active epic are done (no `**Remaining:**`, no partial phase notes).
2. **Backend tests passed** (`py -m pytest` / Quality Gate).
3. **Frontend / E2E passed** when the milestone includes UI or user flows.
4. **Docs updated** (`PROJECT_STATUS.md`, design notes, API docs as applicable).
5. **Release committed and pushed** (at least one repo in the current `finish_task.py` run).
6. **No remaining tasks** listed under the active item (no open next steps, no `IN_PROGRESS` status, no unchecked `[ ]` items).

If any item is unchecked, **do not advance**. Preserve roadmap history as applicable, but only `PROJECT_STATUS.md` may authorize an active task.

---

## Tooling behavior (multi-phase safety)

When the active task section (or matching queue item) shows signals such as:

- `Phase` / `7 phases`
- `**Remaining:**`
- `**Status:** IN_PROGRESS`
- Unfinished markdown checkboxes `[ ]`

`finish_task.py` will:

1. Print a **WARNING** that auto-advance may be premature.
2. Require typing **`ADVANCE`** (not `Y` alone) on the interactive prompt.
3. Refuse `--advance-roadmap` unless **`--force-advance-roadmap`** is also passed.

Use `--force-advance-roadmap` only when you intentionally override safety (e.g. manual roadmap cleanup after verifying DoD).

---

## Manual correction

Any roadmap correction is a historical planning correction. It cannot create or restore an authorized active task without an explicit human decision in `PROJECT_STATUS.md`.

If the roadmap was advanced by mistake:

1. Correct historical planning fields in `MVP_ROADMAP.md`; do not treat **Current Active Task** or **Current Priority Queue** as operational authorization.
2. Align `backend/PROJECT_STATUS.md` and `workspace/PROJECT_STATUS.md`.
3. Do **not** rely on auto-advance until the epic is truly complete.

---

## Related documents

- [`README_FINISH_TASK.md`](./README_FINISH_TASK.md) — flags and examples
- [`backend/AI_OS_OVERVIEW.md`](../backend/AI_OS_OVERVIEW.md) — AI OS workflow
- [`backend/AGENT_RULES.md`](../backend/AGENT_RULES.md) — agent roadmap discipline
- [`PROJECT_STATUS.md`](PROJECT_STATUS.md) — sole source of truth for active-task and READY-mission authorization
- [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) — subordinate product-planning history and context
# Operational-authority override

`MVP_ROADMAP.md` is product-backlog history, not execution authority. A TODO or READY roadmap item cannot create operational READY state. Any roadmap promotion or related status write requires the exact `READY` mission and action class in the canonical JSON block in `PROJECT_STATUS.md`; otherwise STOP and preserve the backlog entry as non-operative history.
