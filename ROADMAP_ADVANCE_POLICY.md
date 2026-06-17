# Roadmap Advance Policy

Prevents **premature auto-advance** of `MVP_ROADMAP.md` when only part of a multi-phase epic is done (e.g. WebPay Phase 1 shipped while phases 2–7 remain).

**Enforced by:** `finish_task.py` / `roadmap_advance.py` (see [README_FINISH_TASK.md](./README_FINISH_TASK.md)).

**Authoritative roadmap:** [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).

---

## Terminology

| Term | Meaning | Example |
|------|---------|---------|
| **Epic** | A roadmap queue item / active task spanning multiple deliverables or phases | Payment Provider Integration (WebPay placeholder) |
| **Phase** | An internal implementation slice inside one epic; not a separate roadmap milestone | WebPay Phase 1: shared `confirm_order_payment_held` service |
| **Task** | A single scoped unit of work (often one phase or one repo change set) | Extract payment confirm service; add checkout session migration |
| **Release** | A Quality Gate–passed commit/push via `finish_task.py` | Backend tests green → commit → push |

**Rule:** Completing a **phase** or **task** inside an epic does **not** complete the **epic**. Only the whole roadmap item may move to **Completed**.

---

## When auto-advance is allowed

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

If any item is unchecked, **do not advance**. Update the roadmap body to reflect progress and keep the same **Current Active Task**.

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

If the roadmap was advanced by mistake:

1. Restore **Current Active Task** and **Current Priority Queue** in `MVP_ROADMAP.md`.
2. Align `backend/PROJECT_STATUS.md` and `workspace/PROJECT_STATUS.md`.
3. Do **not** rely on auto-advance until the epic is truly complete.

---

## Related documents

- [`README_FINISH_TASK.md`](./README_FINISH_TASK.md) — flags and examples
- [`backend/AI_OS_OVERVIEW.md`](../backend/AI_OS_OVERVIEW.md) — AI OS workflow
- [`backend/AGENT_RULES.md`](../backend/AGENT_RULES.md) — agent roadmap discipline
- [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) — source of truth for active task
