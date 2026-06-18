# Notifications Scope Report — Melómanos Marketplace

**Document type:** Pre-implementation scope audit  
**Date:** 2026-06-18  
**Active milestone:** Notifications (`backend/MVP_ROADMAP.md` — Current Priority Queue #1)  
**Status:** Planning only — **no code changes in this document**

**Authority stack:** `BUSINESS_RULES.md` → `ARCHITECTURE.md` → `MVP_ROADMAP.md` → this report

---

## 1. Current roadmap definition of Notifications

### Source: `backend/MVP_ROADMAP.md` (queue #1 + Current Active Task)

| Area | Roadmap text |
|------|----------------|
| **Business goal** | Buyers and sellers get timely updates on **messages, orders, shipping, and disputes**. |
| **Technical goal** | **In-app notification store** + **optional email hooks** for key events. |
| **Backend** | `notifications` table; `GET /users/me/notifications`, `PATCH .../read`; **emit on order/dispute/message events**. |
| **Frontend** | **Notification bell + list + mark read**. |
| **Tests** | Backend: create on event, list, read state. E2E: **new message creates visible notification**. |
| **Dependencies** | Marketplace Core, Orders, Messaging |
| **Complexity** | Medium |
| **Status** | TODO |

### Explicitly required (milestone DoD)

1. Persistent **in-app** notifications per user.
2. **List** endpoint for the authenticated user.
3. **Mark as read** (single or bulk — roadmap says `PATCH .../read`).
4. **Event emission** wired into existing flows (at minimum message, order, dispute domains per roadmap).
5. **Frontend bell** with list UI and read interaction.
6. **Backend pytest** proving create-on-event, list, read state.
7. **One E2E** proving a new message produces a visible notification.
8. Quality Gate + commit + push + `PROJECT_STATUS.md` update (per roadmap Rules).

### Implied (not spelled out in roadmap)

- **Recipient-only access** — notifications are private to `user_id` (consistent with messages, disputes, profile).
- **Spanish-friendly copy** for notification titles/bodies (product uses Spanish for safety and order UX).
- **Deep links** — tapping a notification should navigate to the relevant resource (`/messages`, `/orders/{id}`, dispute section).
- **Unread count** — required for a useful bell (implied by “mark read” + bell pattern; messages already show unread in navbar).
- **Idempotent or de-duplicated creation** — avoid spam on retries (especially payment webhook).
- **Service-layer hooks** — `ARCHITECTURE.md` requires business logic in `app/services/`, not fat routers.
- **Alembic migration** + model registration in `app/models/__init__.py`.
- **Navbar integration** — natural home for bell (existing `Navbar.tsx` already polls message unread).

### Out of scope (per roadmap / architecture)

| Item | Rationale |
|------|-----------|
| **Real email delivery** (SMTP/SendGrid) in MVP | Roadmap says “optional email hooks” — not required for milestone completion unless explicitly promoted. |
| **Push notifications** (mobile/web push) | Not mentioned; post-MVP. |
| **SMS / WhatsApp** | Off-platform contact is discouraged by messaging safety rules. |
| **Admin notification inbox** | Admin panel is read-only ops; no roadmap requirement to notify admins in-app. |
| **Notification preferences / opt-out matrix** | Not in roadmap; defer unless needed for beta. |
| **Real-time WebSockets** | Polling on navigation + manual refresh is sufficient for MVP. |
| **Digest / batching emails** | Post-MVP. |
| **Notifications for favorites, Digging Score, subscriptions** | Roadmap scopes messages, orders, shipping, disputes only. |

### Related context (not Notifications-specific)

- **Closed Beta** lists Notifications as **recommended** dependency (`MVP_ROADMAP.md` #3).
- **`ARCHITECTURE.md`** lists Notifications as “Planned — In-app + email”.
- **`BUSINESS_RULES.md`** does not yet define notification rules (gap to close in Phase 4 docs).
- **Existing message unread** in `Navbar.tsx` uses `getConversations()` + `totalUnreadCount()` — separate from this milestone unless unified by design decision.

---

## 2. Recommended MVP scope

### Must have for MVP (ship milestone)

| # | Capability |
|---|------------|
| M1 | `notifications` table + Alembic migration |
| M2 | `NotificationService.create_for_user()` (or equivalent) called from **message sent** hook |
| M3 | Order lifecycle hooks: **payment held** (seller), **shipped** (buyer), **completed** (seller) |
| M4 | Dispute hooks: **dispute opened** (counterparty), **dispute resolved** (both participants) |
| M5 | `GET /users/me/notifications` — paginated list, newest first |
| M6 | `GET /users/me/notifications/unread-count` (or unread in list meta) |
| M7 | `PATCH /users/me/notifications/{id}/read` + `PATCH /users/me/notifications/read-all` |
| M8 | Frontend **notification bell** in navbar with unread badge |
| M9 | Dropdown or `/notifications` page listing items with mark-read |
| M10 | Backend tests: create, list, auth, mark read, unread count |
| M11 | E2E: send listing message → receiver sees notification (roadmap-mandated) |

### Should have if simple (still MVP-friendly)

| # | Capability | Notes |
|---|------------|-------|
| S1 | **Order created** notify seller | One line in `POST /orders/from-listing` — high value, low effort |
| S2 | **Review received** notify seller | Hook in `POST /reviews` after completed order check |
| S3 | `entity_type` + `entity_id` on notification row | Clean deep linking without parsing body text |
| S4 | `data-testid` on bell, list, unread badge | Matches existing E2E conventions |
| S5 | Mark read when user opens linked order/message | UX polish; optional auto-read on navigate |
| S6 | Stub `send_notification_email()` no-op or log-only | Satisfies “optional email hooks” without SMTP |

### Future / post-MVP

| # | Capability |
|---|------------|
| F1 | Real email provider integration |
| F2 | Per-user notification preferences |
| F3 | WebSocket / SSE live updates |
| F4 | Admin alerts (new dispute in queue) |
| F5 | Payment **pending** reminder for buyer (nudge before timeout) |
| F6 | Merge message unread + notification unread into single “inbox” UX |
| F7 | Notification retention / archival job (90-day cleanup) |

---

## 3. Event triggers

Recommended MVP mapping (who gets notified, when). **Actor** = user who performed the action; **recipient** = notification target.

| Event | Emit in MVP? | Recipient | Suggested `type` | Deep link |
|-------|----------------|-----------|------------------|-----------|
| **New message** | **Required** (E2E) | `message.receiver_id` | `message.received` | `/messages` or listing thread |
| **Order created** | Should have (S1) | Seller (`order.seller_id`) | `order.created` | `/orders/{id}` |
| **Payment held** | **Must have** | Seller | `order.payment_held` | `/orders/{id}` |
| **Order shipped** | **Must have** | Buyer | `order.shipped` | `/orders/{id}` |
| **Order completed** | **Must have** | Seller | `order.completed` | `/orders/{id}` |
| **Dispute opened** | **Must have** | Non-opener participant | `dispute.opened` | `/orders/{id}` (dispute section) |
| **Dispute status changed** | **Must have** (resolve + under_review) | Both participants | `dispute.status_changed` | `/orders/{id}` |
| **Review received** | Should have (S2) | Seller (`review.seller_id` or via listing) | `review.received` | `/listings/{id}` or seller profile |
| **Admin dispute resolution** | Optional MVP | Buyer + seller on resolve | `dispute.resolved` | `/orders/{id}` |
| **Admin-related (summary)** | **Out of scope** | — | — | Admin uses `/admin` dashboard today |
| **Order cancelled** | Future | Counterparty | `order.cancelled` | `/orders/{id}` |
| **Payment pending** (buyer nudge) | Future | Buyer | `order.payment_pending` | `/orders/{id}` |
| **Checkout failed** | Future | Buyer | `order.payment_failed` | `/orders/{id}` |

### Hook placement (implementation hint)

| Event | Suggested hook location |
|-------|-------------------------|
| Message | `messages.py` `create_message` after successful commit |
| Order created | `orders.py` `create_order_from_listing` |
| Payment held | `confirm_order_payment_held()` in `payment/confirm.py` (single path for simulate + webhook) |
| Shipped | `orders.py` `update_order_shipping` |
| Completed | `orders.py` `complete_order` |
| Dispute opened | `dispute.py` `open_order_dispute` |
| Dispute under review / resolved | `dispute.py` `mark_dispute_under_review`, `resolve_dispute_for_*` |
| Review | `reviews.py` `create_review` |

### De-duplication rules

- Do **not** notify the actor (e.g. seller does not get “you shipped” unless product wants self-confirmation — default **no**).
- WebPay webhook idempotency: only create `payment_held` notification when `payment_status` transitions `pending` → `held`.
- One dispute-opened notification per dispute id.

---

## 4. Backend design proposal

### Model: `notifications`

| Field | Type | Notes |
|-------|------|-------|
| `id` | PK int | |
| `user_id` | FK → `users.id` | Recipient only |
| `type` | string(64) | e.g. `message.received`, `order.shipped` |
| `title` | string(255) | Short Spanish headline |
| `body` | text nullable | Optional detail |
| `entity_type` | string(32) nullable | `order`, `message`, `dispute`, `listing`, `review` |
| `entity_id` | int nullable | For deep links |
| `read_at` | datetime nullable | Null = unread |
| `created_at` | datetime | UTC, indexed with `user_id` |

**Indexes:** `(user_id, created_at DESC)`, `(user_id, read_at)` for unread queries.

**No** `deleted_at` in MVP — keep table append-only; optional cleanup later.

### Pydantic schemas

- `NotificationRead` — API response
- `NotificationListResponse` — `{ items: NotificationRead[], unread_count: int }` or separate count endpoint
- `NotificationMarkRead` — optional body for bulk ids

### API endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/users/me/notifications` | List for current user; query `?skip=&limit=&unread_only=` |
| `GET` | `/users/me/notifications/unread-count` | Fast badge poll |
| `PATCH` | `/users/me/notifications/{id}/read` | Mark one read (403 if not owner) |
| `PATCH` | `/users/me/notifications/read-all` | Mark all read for current user |

Register under `app/routers/users.py` or new `app/routers/notifications.py` with prefix `/users/me/notifications` (match roadmap wording).

### Service layer: `app/services/notification.py`

```text
create_notification(db, *, user_id, type, title, body=None, entity_type=None, entity_id=None) -> Notification
mark_notification_read(db, *, notification_id, user_id) -> Notification
mark_all_read(db, *, user_id) -> int
list_notifications(db, *, user_id, skip, limit, unread_only) -> tuple[list, int unread_count]
notify_order_event(db, order, *, event_type, recipient_user_id)  # optional helper
```

Keep routers thin: auth → service → schema.

### Auth rules

- All endpoints require `get_current_user`.
- Users may only list/read/update notifications where `notification.user_id == current_user.id`.
- Return **404** (not 403) for other users’ notification ids to avoid leaking existence.

### Read / unread behavior

- **Unread:** `read_at IS NULL`.
- **Mark read:** set `read_at = now()`; idempotent if already read.
- **Unread count:** `COUNT(*) WHERE user_id = ? AND read_at IS NULL`.
- **No** automatic expiry in MVP.

### Email hooks (optional / stub)

```text
# app/services/notification_email.py (stub)
def maybe_send_email(notification: Notification, user: User) -> None:
    pass  # log at debug in dev
```

Call after `create_notification` behind `NOTIFICATION_EMAIL_ENABLED=false` config.

---

## 5. Frontend design proposal

### Placement

- Add **NotificationBell** beside existing **MessagesLink** in `Navbar.tsx`.
- Keep **message unread** separate in MVP (avoid breaking existing `totalUnreadCount` behavior).

### Components

| Component | Responsibility |
|-----------|----------------|
| `NotificationBell.tsx` | Icon, unread badge, toggles dropdown |
| `NotificationDropdown.tsx` | Last N items, “Mark all read”, link to full page |
| `app/notifications/page.tsx` | Full list (optional but recommended for mobile) |

### Data flow

- `getNotifications()`, `getUnreadNotificationCount()`, `markNotificationRead()`, `markAllNotificationsRead()` in `lib/api.ts`.
- Poll unread count on: login, pathname change, after mark-read (mirror messages pattern).
- Optional custom event `NOTIFICATIONS_UPDATED_EVENT` (parallel to `MESSAGES_UPDATED_EVENT`).

### UX details

| Element | Behavior |
|---------|----------|
| **Bell** | Visible when logged in; `data-testid="notification-bell"` |
| **Badge** | Show count if unread > 0; cap display `9+` |
| **List item** | Title, relative time, unread dot; click → navigate + mark read |
| **Empty state** | “No notifications yet” / “Sin notificaciones” |
| **Mark all read** | Button in dropdown + full page |

### Copy language

- Spanish primary for titles (align with order/dispute UI).
- English acceptable for dev/E2E assertions if consistent with mixed navbar (“Orders”, “Messages”).

---

## 6. Testing plan

### Backend tests (`tests/test_notifications.py`)

| Test | Asserts |
|------|---------|
| `test_create_notification_on_message` | POST message → receiver has 1 unread |
| `test_list_notifications_auth` | Only own notifications returned |
| `test_mark_read` | `read_at` set; unread count decreases |
| `test_mark_read_wrong_user` | 404 |
| `test_mark_all_read` | All user notifications read |
| `test_payment_held_notifies_seller` | After simulate-payment / confirm |
| `test_shipping_notifies_buyer` | After PATCH shipping |
| `test_dispute_open_notifies_counterparty` | Buyer opens → seller notified |

Target: **8–12** new pytest cases; full suite must stay green (baseline **215**).

### Frontend E2E (`e2e/notifications.spec.ts` or extend `melomanos.spec.ts`)

| Test | Asserts |
|------|---------|
| **Roadmap-required** | Buyer sends allowed message → seller sees notification bell/count or list entry |
| Optional | Seller ships order → buyer notification |
| Optional | Mark all read clears badge |

Use stable `data-testid` selectors.

### Regression risks

| Risk | Mitigation |
|------|------------|
| Double notifications on webhook retry | Hook only on state transition in `confirm_order_payment_held` |
| Breaking message unread badge | Do not replace MessagesLink logic in Phase 3 |
| Transaction ordering | Create notification in same DB transaction as domain event when possible |
| E2E flakiness | Wait for API poll after message send; use unique listing stamp |
| Performance on list | Paginate default `limit=20` |

### Quality Gate (milestone completion)

```powershell
cd backend && py -m pytest -q
cd frontend && npm run build && npm run test:e2e
```

---

## 7. Implementation phases

Break into four phases (similar to WebPay plan). **One phase IN_PROGRESS at a time.**

### Phase 1 — Backend foundation

- Alembic migration `notifications` table
- SQLAlchemy model + schemas
- `app/services/notification.py` CRUD + unread count
- Router: list, unread-count, mark read, mark all read
- Pytest: list/auth/read (no event hooks yet)

**Validation:** `py -m pytest tests/test_notifications.py -q`

### Phase 2 — Event creation hooks

- Wire hooks: message, payment held, shipped, completed, dispute opened/resolved
- Optional: order created, review received
- Pytest: integration per event type
- Stub email hook (no-op)

**Validation:** `py -m pytest -q` (full suite)

### Phase 3 — Frontend UI

- API client methods
- `NotificationBell` + dropdown (+ optional `/notifications` page)
- Navbar integration + unread polling
- `data-testid` attributes

**Validation:** `npm run build`; manual smoke

### Phase 4 — E2E + docs / release

- E2E: message → visible notification (roadmap requirement)
- Update `BUSINESS_RULES.md`, `ARCHITECTURE.md`, `TESTING_STRATEGY.md` baselines
- `PROJECT_STATUS.md`, `RELEASE_NOTES.md`, milestone → Completed via `finish_task.py`

**Validation:** full Quality Gate + `finish_task.py --advance-roadmap`

---

## 8. Risks and decisions needed

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| D1 | **Bell vs extend Messages link** | Separate bell vs unified inbox | **Separate bell** for MVP; messages keep own unread |
| D2 | **Dropdown vs page only** | Dropdown only vs `/notifications` page | **Both** — dropdown for quick view, page for mobile/history |
| D3 | **Spanish vs bilingual copy** | ES only vs EN | **Spanish** titles; match order/dispute pages |
| D4 | **Notify on order created** | Yes / no | **Yes** (seller) — simple, high value |
| D5 | **Notify buyer on payment held** | Yes / no | **No** by default — buyer initiated payment; seller needs action |
| D6 | **Dispute under_review** | Notify participants? | **Yes** — status change is material |
| D7 | **Admin resolution** | Separate admin notification? | **No** — notify buyer/seller only with `dispute.resolved` |
| D8 | **Email in MVP** | Stub vs skip | **Stub** (`NOTIFICATION_EMAIL_ENABLED=false`) |
| D9 | **Auto-read on navigate** | On click vs manual only | **Mark read on click** in Phase 3 if trivial |
| D10 | **BUSINESS_RULES update** | Phase 4 vs now | **Phase 4** with implementation |
| D11 | **Pagination default** | 20 vs 50 | **20** |

### Technical risks

- Hook sprawl across routers — centralize types in `notification.py` constants.
- `confirm_order_payment_held` is the correct single hook for payment (simulate + WebPay).
- Closed Beta may expect notifications live — coordinate before beta milestone.

---

## Summary

Notifications MVP is **well-bounded** in the roadmap: in-app store, list/read API, hooks on core marketplace events, bell UI, one message E2E. Email is optional. Admin push is out of scope. Existing message unread in the navbar should remain separate unless product chooses unification.

**Recommended next implementation phase:** **Phase 1 — Backend foundation** (table, service, read API, auth tests) before wiring event hooks or frontend.

---

## References

| Document | Path |
|----------|------|
| MVP roadmap | `backend/MVP_ROADMAP.md` |
| Backend status | `backend/PROJECT_STATUS.md` |
| Workspace status | `workspace/PROJECT_STATUS.md` |
| Business rules | `backend/BUSINESS_RULES.md` |
| Architecture | `backend/ARCHITECTURE.md` |
| Testing strategy | `backend/TESTING_STRATEGY.md` |
| Navbar (existing unread) | `frontend/src/components/Navbar.tsx` |
| Messages router | `backend/app/routers/messages.py` |
| Payment confirm hook | `backend/app/services/payment/confirm.py` |

---

*Report only — no code, roadmap status, or milestone advance performed.*
