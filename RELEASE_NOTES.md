# RELEASE_NOTES — Melómanos Marketplace

**Purpose:** Release **index** for auditors and agents.  
**Last synced:** 2026-06-17 (constraint pass)

> **Milestone definitions and completion criteria:** [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) — Completed  
> **Detailed changelog:** [`backend/CHANGELOG.md`](../backend/CHANGELOG.md)  
> **Do not duplicate milestone specs here.**

---

## Release Index

| # | Milestone | Date | Detail |
|---|-----------|------|--------|
| 1–12 | See roadmap Completed table | **UNKNOWN** | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) |
| 13 | Admin Panel MVP | **2026-06-05** | Below + [`backend/PROJECT_STATUS.md`](../backend/PROJECT_STATUS.md) |

**Shipped count:** 13 (per roadmap). **Pending queue:** 5 (per roadmap).

---

## Latest Documented Release — Admin Panel MVP (2026-06-05)

Source: [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) Quality Gate markers, [`backend/PROJECT_STATUS.md`](../backend/PROJECT_STATUS.md) Recently completed.

| Area | Summary |
|------|---------|
| Backend | `GET /admin/summary`, `/disputes`, `/orders`, `/users` — `x-admin-key` |
| Frontend | Read-only `/admin` |
| Tests | `test_admin_panel.py`; E2E admin panel |
| Quality Gate | 180 pytest, build, 20 E2E — PASSED |

Full notes: [`backend/PROJECT_STATUS.md`](../backend/PROJECT_STATUS.md) — Recently completed.

---

## Milestones 1–12

Listed in [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) Completed table. Historical per-milestone dates: **UNKNOWN** (not in PROJECT_STATUS). API-level history: [`backend/CHANGELOG.md`](../backend/CHANGELOG.md).

---

## Upcoming (not released)

| Milestone | Status | Spec |
|-----------|--------|------|
| Payment Provider Integration (WebPay placeholder) | READY | [`MVP_ROADMAP`](../backend/MVP_ROADMAP.md) |
| Notifications | TODO | Same |
| Production Deployment | TODO | Same |
| Closed Beta | TODO | Same |
| Public Launch | TODO | Same |

---

## How Releases Are Recorded

[`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) Rules + [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md).

---

## Source Documents

| Document | Path |
|----------|------|
| MVP roadmap (completed + queue) | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) |
| Changelog | [`backend/CHANGELOG.md`](../backend/CHANGELOG.md) |
| Backend project status | [`backend/PROJECT_STATUS.md`](../backend/PROJECT_STATUS.md) |
| Workspace project status | [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) |
| Quality gate | [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md) |
| Foundation sync report | [`workspace/AI_DEV_OS_FOUNDATION_SYNC_REPORT.md`](AI_DEV_OS_FOUNDATION_SYNC_REPORT.md) |

---

*Append a short entry here after each `finish_task.py` release; link to roadmap and PROJECT_STATUS for detail.*
