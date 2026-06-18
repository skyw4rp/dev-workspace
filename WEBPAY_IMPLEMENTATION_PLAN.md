# WebPay Implementation Plan — Melómanos Marketplace

**Document type:** Phased execution plan (Cursor / agent playbook)  
**Source of truth:** [`WEBPAY_INTEGRATION_DESIGN.md`](WEBPAY_INTEGRATION_DESIGN.md)  
**Active roadmap item:** Payment Provider Integration (WebPay placeholder) — [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md)  
**Policy:** Do **not** mark the full WebPay epic complete or advance `MVP_ROADMAP.md` until **all phases below are DONE**. See [`ROADMAP_ADVANCE_POLICY.md`](ROADMAP_ADVANCE_POLICY.md).

---

## Cursor instruction

```
To continue WebPay, implement the next TODO phase only.
Read WEBPAY_IMPLEMENTATION_PLAN.md and WEBPAY_INTEGRATION_DESIGN.md.
Set the target phase Status to IN_PROGRESS before coding.
When the phase completion checklist is fully satisfied, set Status to DONE.
Do not start the following phase in the same session unless explicitly asked.
```

---

## Execution rules

1. **Only one phase may be `IN_PROGRESS` at a time.**
2. **Do not start the next phase** unless the current phase is **`DONE`** (checklist complete, validation commands green).
3. **Each phase must pass its validation commands** before marking `DONE`.
4. **Do not mark the full WebPay epic complete** until all 7 phases are **`DONE`**.
5. **Do not advance `MVP_ROADMAP.md`** until all 7 phases are **`DONE`** (use `finish_task.py` only after Phase 7; multi-phase safety applies until then).
6. **Preserve escrow semantics** — post-`held` lifecycle unchanged (shipping, complete, dispute, cancel).
7. **Keep `simulate-payment` working** in `PAYMENT_PROVIDER_MODE=simulate` until Phase 7 release sign-off.
8. **Backend business logic in `app/services/payment/`**; routers stay thin.
9. On conflict with design, **design doc wins** until intentionally updated in the same release.

---

## Phase overview

| Phase | Title | Status |
|-------|-------|--------|
| **1** | Shared payment confirmation service | **DONE** |
| **2** | `checkout_sessions` and `payment_events` backend foundation | **DONE** |
| **3** | Checkout endpoint | **DONE** |
| **4** | WebPay callback / payment confirmation placeholder | **DONE** |
| **5** | Frontend checkout CTA and success handling | **DONE** |
| **6** | E2E checkout flow | **DONE** |
| **7** | Docs, business rules, release readiness | **DONE** |

---

## Phase 1 — Shared payment confirmation service

**Status:** DONE

### Goal

Extract a single escrow confirmation function used by simulate-payment (and later webhook/checkout) without changing buyer-visible behavior.

### Scope

- `confirm_order_payment_held(order, *, now=None)` service
- `PATCH /orders/{id}/simulate-payment` delegates to shared confirm
- Regression tests proving unchanged transitions

### Out of scope

- Checkout sessions, webhooks, PaymentProvider, frontend changes
- New database tables
- Real WebPay / Transbank integration

### Files affected (delivered)

| Area | Path |
|------|------|
| Service | `backend/app/services/payment/__init__.py` |
| Service | `backend/app/services/payment/confirm.py` |
| Router | `backend/app/routers/orders.py` |
| Tests | `backend/tests/test_payment_confirm.py` |
| Tests | `backend/tests/test_orders.py` (simulate regression) |

### Backend tasks (completed)

- [x] Extract `confirm_order_payment_held()` from simulate endpoint logic
- [x] Recompute amounts via `compute_escrow_amounts()`
- [x] Set `payment_status` → `held`, `status` → `pending_shipping`, timestamps
- [x] Preserve buyer auth and `payment_status == pending` guard in router
- [x] Add dedicated unit tests for confirm service

### Frontend tasks

- None (behavior unchanged)

### Tests required (completed)

- [x] `test_payment_confirm.py` — success, already-held rejection, escrow amounts
- [x] `test_orders.py` — simulate payment happy path + auth + regression cases

### Validation commands (passed at completion)

```powershell
cd C:\melomanos\backend
py -m pytest tests/test_payment_confirm.py tests/test_orders.py -q
py -m pytest -q
```

### Completion checklist

- [x] `simulate-payment` behavior unchanged (`pending` → `held`, `created` → `pending_shipping`)
- [x] Listing reservation unchanged on payment confirm
- [x] Full backend pytest suite green
- [x] No new env vars required for this phase

---

## Phase 2 — `checkout_sessions` and `payment_events` backend foundation

**Status:** DONE

> **Phase 2 complete:** DB foundation and provider foundation implemented (migration `d7e8f9a0b1c2`, ORM models, `PaymentProvider` factory, config; 196 pytest passing).

### Goal

Add persistent checkout session and webhook idempotency storage plus PaymentProvider scaffolding — **no buyer-facing checkout flow yet**.

### Scope

- Alembic migration: `checkout_sessions`, `payment_events`
- SQLAlchemy models and Pydantic schemas
- `PaymentProvider` protocol + factory driven by `PAYMENT_PROVIDER_MODE`
- Config env vars and `.env.example` entries
- Service stubs wired but not exposed via public checkout/webhook routes yet

### Out of scope

- `POST /orders/{id}/checkout` (Phase 3)
- Webhook/callback routes (Phase 4)
- Frontend changes
- E2E changes
- Real Transbank SDK

### Files likely affected

| Area | Path |
|------|------|
| Migration | `backend/alembic/versions/*_add_checkout_sessions_and_payment_events.py` |
| Models | `backend/app/models/checkout_session.py` |
| Models | `backend/app/models/payment_event.py` |
| Models | `backend/app/models/__init__.py` |
| Schemas | `backend/app/schemas/payment.py` |
| Services | `backend/app/services/payment/provider.py` |
| Services | `backend/app/services/payment/simulate_provider.py` (skeleton) |
| Services | `backend/app/services/payment/webpay_placeholder.py` (skeleton) |
| Config | `backend/app/core/config.py` |
| Config | `backend/.env.example` |
| Tests | `backend/tests/test_checkout_models.py` (new, optional) |

### Backend tasks

- [x] Create Alembic revision per design §8.1 (`checkout_sessions`, `payment_events`)
- [x] Implement ORM models with FK, indexes, unique constraints per design §4.2
- [x] Add Pydantic schemas for checkout session and payment event payloads
- [x] Define `PaymentProvider` protocol + `get_payment_provider()` factory
- [x] Add config: `PAYMENT_PROVIDER_MODE`, `WEBPAY_CALLBACK_SECRET`, `WEBPAY_RETURN_URL_BASE`
- [x] Register models in Alembic metadata / app imports
- [x] Add minimal factory tests (mode selection: `simulate` vs `webpay_placeholder`)

### Frontend tasks

- None

### Tests required

- [x] Migration applies cleanly on SQLite (dev) and existing test DB
- [x] Model CRUD / constraint tests if added
- [x] Factory returns correct provider for each mode
- [x] Full regression: `py -m pytest` — all existing tests still pass

### Validation commands

```powershell
cd C:\melomanos\backend
py -m alembic upgrade head
py -m pytest -q
```

### Completion checklist

- [x] Tables exist with columns per design §4.2 / §8.1
- [x] `payment_events.provider_event_id` unique (idempotency ready)
- [x] `PaymentProvider` protocol and factory compile and are importable
- [x] Config documented in `.env.example`
- [x] No new HTTP routes shipped yet (or routes return 501 if stubbed)
- [x] Phase Status set to **DONE** in this file

---

## Phase 3 — Checkout endpoint

**Status:** DONE

> **Phase 3 complete:** checkout endpoint creates idempotent checkout sessions (`POST /orders/{id}/checkout`).

### Goal

Expose `POST /orders/{order_id}/checkout` for buyers to start a payment session; optionally transition order to `pending_payment`.

### Scope

- `app/services/payment/checkout.py` — create session, validate order state
- `SimulatePaymentProvider` — inline confirm or session without external URL (per mode)
- `WebPayPlaceholderProvider.create_checkout_session()` — returns placeholder URL + token
- `POST /orders/{id}/checkout` on orders router (buyer JWT)
- One active `pending` session per order (service-layer rule)
- Optional: `GET /payments/checkout-sessions/{session_id}` for buyer poll

### Out of scope

- Webhook processing / idempotent confirm from provider (Phase 4)
- Frontend redirect UX (Phase 5)
- E2E (Phase 6)
- Disabling `simulate-payment` in non-simulate modes (defer to Phase 7 if needed)

### Files likely affected

| Area | Path |
|------|------|
| Service | `backend/app/services/payment/checkout.py` |
| Service | `backend/app/services/payment/simulate_provider.py` |
| Service | `backend/app/services/payment/webpay_placeholder.py` |
| Router | `backend/app/routers/orders.py` |
| Router | `backend/app/routers/payments.py` (new, optional poll route) |
| Schemas | `backend/app/schemas/payment.py` |
| Main | `backend/app/main.py` (include payments router if created) |
| Tests | `backend/tests/test_payment_checkout.py` (new) |

### Backend tasks

- [x] Implement `create_checkout_session(order, return_url, cancel_url)` in checkout service
- [x] Validate: caller is buyer, `payment_status == pending`, order payable state
- [x] Persist `checkout_sessions` row (`pending`, amounts, idempotency_key)
- [x] Order status remains `created` (no payment confirm in Phase 3)
- [x] Implement `POST /orders/{id}/checkout` returning `checkout_url`, `session_id`, `expires_at`
- [x] `simulate` mode: return placeholder checkout URL
- [x] `webpay_placeholder` mode: return internal sandbox URL with session token

### Frontend tasks

- None (API-only phase)

### Tests required

- [x] Buyer can create checkout — 200, session persisted
- [x] Seller / other user — 403
- [x] Wrong `payment_status` — 400
- [x] Amounts match `compute_escrow_amounts()`
- [x] Second checkout while session pending — returns same session (200)
- [x] Regression: Phase 1 simulate tests still pass

### Validation commands

```powershell
cd C:\melomanos\backend
py -m pytest tests/test_payment_checkout.py tests/test_payment_confirm.py tests/test_orders.py -q
py -m pytest -q
```

### Completion checklist

- [x] Checkout endpoint documented in OpenAPI / schemas
- [x] Session rows auditable in DB
- [x] Both provider modes create sessions correctly
- [x] No webhook confirm path required yet for tests in this phase
- [x] Phase Status set to **DONE** in this file

---

## Phase 4 — WebPay callback / payment confirmation placeholder

**Status:** DONE

> **Phase 4 complete:** WebPay callback/webhook confirms payment idempotently via `confirm_order_payment_held()`.

### Goal

Process provider callbacks idempotently and confirm payment into escrow via shared `confirm_order_payment_held()`.

### Scope

- `POST /payments/webpay/callback` with shared-secret / HMAC verification
- Idempotency via `payment_events` table
- Map `payment.approved` → `confirm_order_payment_held()`; `payment.failed` → session failed
- `GET /payments/webpay/placeholder/{session_id}` — dev sandbox page that posts callback
- Optional `GET /payments/webpay/return` redirect helper
- Refactor `simulate-payment` to call shared confirm (if not already) and respect mode flags

### Out of scope

- Frontend checkout button (Phase 5)
- E2E (Phase 6)
- Real Transbank production API
- Provider-side refund API on disputes

### Files likely affected

| Area | Path |
|------|------|
| Service | `backend/app/services/payment/webpay_placeholder.py` |
| Service | `backend/app/services/payment/confirm.py` (reuse only) |
| Service | `backend/app/services/payment/checkout.py` |
| Router | `backend/app/routers/payments.py` |
| Schemas | `backend/app/schemas/payment.py` |
| Router | `backend/app/routers/orders.py` (simulate mode guard) |
| Tests | `backend/tests/test_payment_webhook.py` (new) |
| Tests | `backend/tests/test_payment_checkout.py` (extend) |

### Backend tasks

- [x] Implement webhook parser + `verify_webhook()` on placeholder provider
- [x] `POST /payments/webpay/callback` — auth, idempotency, transactional confirm
- [x] Duplicate `provider_event_id` → 200 OK, no double state change
- [x] Approved event: session `completed`, order `held` + `pending_shipping`
- [x] Failed event: session `failed`, order remains payable
- [x] Placeholder sandbox page route for manual / test completion
- [x] Wire `simulate-payment` through confirm service; 410 when `webpay_placeholder` mode

### Frontend tasks

- None

### Tests required

- [x] Webhook approve → single `held` transition
- [x] Same event twice → idempotent (still one transition)
- [x] Invalid secret → 401/403
- [x] Failed payment → order still `pending`, session `failed`
- [x] Full order lifecycle via checkout + webhook (backend-only)
- [x] All existing `test_orders.py` simulate tests pass in `simulate` mode

### Validation commands

```powershell
cd C:\melomanos\backend
py -m pytest tests/test_payment_webhook.py tests/test_payment_checkout.py tests/test_payment_confirm.py tests/test_orders.py -q
py -m pytest -q
```

### Completion checklist

- [x] Webhook is source of truth for payment confirmation (design §15)
- [x] `confirm_order_payment_held()` is the only path to `held`
- [x] Idempotency table prevents double-spend (design risk R1)
- [x] Placeholder sandbox completable without frontend
- [x] Phase Status set to **DONE** in this file

---

## Phase 5 — Frontend checkout CTA and success handling

**Status:** DONE

> **Phase 5 complete:** frontend checkout flow connected to backend checkout sessions.

### Goal

Replace/supplement simulate button with checkout redirect flow and return-url handling on order detail.

### Scope

- API client: `createCheckoutSession(orderId)`
- `lib/payments.ts` — mode helpers, return URL builder
- Order detail: **Pagar con WebPay** CTA, loading state, simulate fallback in dev
- Handle `?checkout=success|cancelled` query on return
- Conditional UI: simulate vs `webpay_placeholder` (via env or `GET /payments/config`)
- Retain or extend `data-testid` for E2E

### Out of scope

- Full E2E spec updates (Phase 6)
- Roadmap / BUSINESS_RULES doc updates (Phase 7)
- Real Transbank redirect

### Files likely affected

| Area | Path |
|------|------|
| Page | `frontend/src/app/orders/[id]/page.tsx` |
| Component | `frontend/src/components/OrderEscrowCard.tsx` |
| Component | `frontend/src/components/OrderPaymentCard.tsx` (new, optional) |
| API | `frontend/src/lib/api.ts` |
| Helpers | `frontend/src/lib/payments.ts` (new) |
| Helpers | `frontend/src/lib/orders.ts` (`orderNeedsPayment`, `pending_payment`) |
| List | `frontend/src/app/orders/page.tsx` (optional badge) |

### Backend tasks

- [ ] Optional: `GET /payments/config` exposing `PAYMENT_PROVIDER_MODE` to frontend (deferred; frontend uses `NEXT_PUBLIC_PAYMENT_PROVIDER_MODE` + localStorage override for E2E)

### Frontend tasks

- [x] Add `createCheckoutSession()` to `api.ts`
- [x] Build return/cancel URLs pointing to `/orders/{id}?checkout=...`
- [x] On CTA click: POST checkout → redirect to `checkout_url`
- [x] On return success: refresh order, show success message
- [x] On return cancelled: show retry message
- [x] Show **Confirmar pago** when mode is `simulate`; **Pay with WebPay** when placeholder
- [x] `data-testid="order-checkout-webpay"` and `order-checkout-notice`

### Tests required

- [x] `npm run build` — types compile
- [x] `npm run test:e2e` — WebPay checkout CTA, redirect, return messages, error handling (8 new tests)
- [x] Existing simulate-path E2E regression (20 legacy + 8 new = 28 total)

### Validation commands

```powershell
cd C:\melomanos\frontend
npm run build
npm run test:e2e
```

### Completion checklist

- [x] Buyer sees correct CTA per payment mode
- [x] Redirect flow reaches backend checkout sandbox URL
- [x] Return URL shows success/cancelled messages and refreshes order on success
- [x] Simulate mode still works for local dev
- [x] Phase Status set to **DONE** in this file

---

## Phase 6 — E2E checkout flow

**Status:** DONE

> **Phase 6 complete:** full placeholder WebPay lifecycle validated end-to-end.

### Goal

Automated Playwright coverage for placeholder checkout: buyer pays → order reaches `pending_shipping`.

### Scope

- E2E helper to complete placeholder checkout (sandbox route or test webhook helper)
- Update `melomanos.spec.ts` payment flows
- `data-testid="order-checkout-webpay"` (or retain `order-confirm-payment` for simulate branch)
- CI runs with `PAYMENT_PROVIDER_MODE=webpay_placeholder` (or documented dual-mode strategy)

### Out of scope

- Production WebPay credentials
- Notifications milestone
- Roadmap completion

### Files likely affected

| Area | Path |
|------|------|
| E2E spec | `frontend/e2e/melomanos.spec.ts` |
| E2E helpers | `frontend/e2e/helpers/order.ts` |
| Config | `frontend/playwright.config.ts` (if env needed) |
| Workspace | `workspace/run_audit.py` / audit docs (if env wiring needed) |

### Backend tasks

- [x] Ensure placeholder sandbox + webhook stable under E2E timing
- [x] Document test env vars (`workspace/e2e-webpay.env`, `run_melomanos.py --e2e-webpay`)
- [x] Extend `test_payment_webhook.py` lifecycle + `payment_event` assertions

### Frontend tasks

- [x] Add checkout E2E test: buy → checkout → assert `pending_shipping`
- [x] Seller shipping form unlocks after payment
- [x] Cancelled checkout → buyer can retry
- [x] Keep simulate-path regression via `confirmOrderPaymentForE2e` dual-mode helper

### Tests required

- [x] E2E: buyer checkout placeholder → `pending_shipping`
- [x] E2E: seller sees shipping form after payment
- [x] E2E: cancelled checkout retry
- [x] E2E: full lifecycle through review (`webpay-lifecycle.spec.ts`)
- [x] Backend pytest: checkout session + payment_event + complete order

### Validation commands

```powershell
cd C:\melomanos\backend
py -m pytest -q

cd C:\melomanos\frontend
npm run build
npm run test:e2e
```

Start backend for Phase 6 E2E:

```powershell
cd C:\melomanos\workspace
py run_melomanos.py --kill-stale --e2e-webpay --no-wait
```

### Completion checklist

- [x] E2E payment flow green locally (31/31)
- [x] No flakiness from external redirect (same-host placeholder)
- [x] Existing non-payment E2E tests still pass (dual-mode payment helper)
- [x] Phase Status set to **DONE** in this file

---

## Phase 7 — Docs, business rules, release readiness

**Status:** DONE

> **Phase 7 complete:** governance docs aligned, Quality Gate validated, `WEBPAY_PHASE7_REPORT.md` published. Roadmap advance pending commit/push.

### Goal

Align governance docs with implemented gateway placeholder, run full Quality Gate release, and prepare roadmap completion (without advancing until this phase is DONE).

### Scope

- Update `BUSINESS_RULES.md` — Compra Segura gateway in scope for placeholder
- Update `ARCHITECTURE.md` — payment module, escrow diagram, new routes
- Update `TESTING_STRATEGY.md` / quality baselines if test counts changed
- Update `MVP_ROADMAP.md` progress notes (all phases DONE — still **IN_PROGRESS** until release)
- Update `workspace/RELEASE_NOTES.md`, `PROJECT_STATUS.md` (backend + workspace)
- `backend/.env.example` final review
- Release via `finish_task.py` (all three repos)

### Out of scope

- Real Transbank production integration
- Notifications milestone
- Automatic provider refunds on dispute

### Files likely affected

| Area | Path |
|------|------|
| Docs | `backend/BUSINESS_RULES.md` |
| Docs | `backend/ARCHITECTURE.md` |
| Docs | `backend/MVP_ROADMAP.md` |
| Docs | `backend/PROJECT_STATUS.md` |
| Docs | `backend/TESTING_STRATEGY.md` |
| Docs | `workspace/PROJECT_STATUS.md` |
| Docs | `workspace/RELEASE_NOTES.md` |
| Docs | `workspace/TASKS.md` |
| Design | `workspace/WEBPAY_INTEGRATION_DESIGN.md` (status note only) |
| Plan | `workspace/WEBPAY_IMPLEMENTATION_PLAN.md` (all phases DONE) |

### Backend tasks

- [x] Final review: feature flag matrix (design §10.4)
- [x] Confirm rollback path: `PAYMENT_PROVIDER_MODE=simulate`

### Frontend tasks

- [x] README / env notes if payment mode exposed to devs

### Tests required

- [x] Full Quality Gate pass (design §9.4)
- [x] Test count baseline updated in docs (215 pytest, 31 E2E)

### Validation commands

```powershell
cd C:\melomanos\backend
py -m pytest -q

cd C:\melomanos\frontend
npm run build
npm run test:e2e
```

### Completion checklist

- [x] All 7 phases marked **DONE** in this file
- [x] `BUSINESS_RULES.md` no longer contradicts placeholder gateway
- [x] `ARCHITECTURE.md` documents payment module and webhook flow
- [x] Quality Gate PASS recorded in `PROJECT_STATUS.md`
- [ ] Release committed/pushed (backend, frontend, workspace) — **pending user `finish_task.py`**
- [ ] Roadmap **Remaining** / phase notes cleared; epic ready for advance per policy — **not auto-advanced**
- [x] Phase Status set to **DONE** in this file

---

## Cross-phase reference

### Central confirm function (Phase 1 — reuse in Phases 4+)

```
confirm_order_payment_held(order):
  assert payment_status == pending
  compute_escrow_amounts(...)
  payment_status = held
  status = pending_shipping
  payment_confirmed_at = funds_held_at = now()
```

### Environment modes (design §3.3)

| Mode | Buyer experience |
|------|------------------|
| `simulate` | Confirmar pago (legacy) |
| `webpay_placeholder` | Redirect to sandbox → webhook confirm |

### Authority stack

1. [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md)
2. [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md)
3. [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md)
4. [`WEBPAY_INTEGRATION_DESIGN.md`](WEBPAY_INTEGRATION_DESIGN.md)
5. This plan

---

*Last updated: Phase 7 DONE — all WebPay phases complete; roadmap advance pending commit/push.*
