# RELEASE_NOTES — Melómanos Marketplace

**Purpose:** Release **index** for auditors and agents.  
**Last synced:** 2026-06-18 (Notifications Phase 4)

> **Milestone definitions and completion criteria:** [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) — Completed  
> **Detailed changelog:** [`backend/CHANGELOG.md`](../backend/CHANGELOG.md)  
> **Do not duplicate milestone specs here.**

---

## Release Index

| # | Milestone | Date | Detail |
|---|-----------|------|--------|
| 1–12 | See roadmap Completed table | **UNKNOWN** | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) |
| 13 | Admin Panel MVP | **2026-06-05** | Below + [`backend/PROJECT_STATUS.md`](../backend/PROJECT_STATUS.md) |
| 14 | Payment Provider Integration (WebPay placeholder) | **2026-06-18** | Below + [`WEBPAY_PHASE7_REPORT.md`](WEBPAY_PHASE7_REPORT.md) |
| 15 | Notifications (in-app MVP) | **2026-06-18** (validation; roadmap advance pending) | Below + [`NOTIFICATIONS_SCOPE_REPORT.md`](NOTIFICATIONS_SCOPE_REPORT.md) |

**Shipped count:** 14 committed + Notifications ready for formal close. **Pending queue:** 4 (per roadmap).

---

## Latest Documented Release — Notifications (in-app MVP)

**Date:** 2026-06-18 (Quality Gate validation; `finish_task.py` / roadmap advance not run in Phase 4 pass)

Source: [`NOTIFICATIONS_SCOPE_REPORT.md`](NOTIFICATIONS_SCOPE_REPORT.md), [`backend/PROJECT_STATUS.md`](../backend/PROJECT_STATUS.md)

| Area | Summary |
|------|---------|
| Backend | `notifications` table; list/unread/mark-read API; event hooks (message, order, payment, ship, complete, dispute) |
| Frontend | Navbar **Alertas** bell, dropdown, `/notifications`; Spanish copy |
| Tests | 231 pytest; 33 E2E (`notifications.spec.ts`) |
| Out of scope | Email, push, mark-all-read, WebSockets |

---

## Prior Release — Payment Provider Integration (WebPay placeholder)

**Date:** 2026-06-18 (Quality Gate validation; commit/push pending)

Source: [`WEBPAY_PHASE7_REPORT.md`](WEBPAY_PHASE7_REPORT.md), [`WEBPAY_IMPLEMENTATION_PLAN.md`](WEBPAY_IMPLEMENTATION_PLAN.md)

| Area | Summary |
|------|---------|
| Backend | `PaymentProvider`, `POST /orders/{id}/checkout`, `POST /payments/webpay/callback`, placeholder sandbox, `checkout_sessions` + `payment_events` |
| Frontend | **Pay with WebPay** CTA, `?checkout=success\|cancelled`, dual-mode E2E helper |
| Tests | 215 pytest; 31 E2E (includes `webpay-lifecycle.spec.ts`) |
| Quality Gate | pytest + build + E2E — PASSED |

**Rollback:** `PAYMENT_PROVIDER_MODE=simulate` (see `backend/.env.example`).

---

## Prior Release — Admin Panel MVP (2026-06-05)

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
| Notifications | READY (roadmap advance pending) | [`NOTIFICATIONS_SCOPE_REPORT.md`](NOTIFICATIONS_SCOPE_REPORT.md) |
| Production Deployment | TODO | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) |
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
