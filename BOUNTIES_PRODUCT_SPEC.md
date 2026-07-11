# Bounties Product Specification — Melómanos Market

**Document type:** Product specification (TYPE G — not implementation-approved)  
**Mission:** M-010  
**Date:** 2026-07-10  
**Implementation status:** **NOT_APPROVED**  
**Authority:** This document defines proposed product rules. Until promoted and implemented, [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) remains authoritative for live behavior.

**Related:** [`decisions/BOUNTIES_MVP_DECISION_RECORD.md`](decisions/BOUNTIES_MVP_DECISION_RECORD.md)

---

## 1. Problem and value proposition

### User problem

Collectors often seek a **specific** vinyl pressing, edition, or condition that is **not currently listed** on Melómanos. Browsing `/explorar` and favoriting individual listings does not help when no matching listing exists. Sellers with inventory in storage may not list until they know a buyer wants the record.

### Target users

| Persona | Need |
|---------|------|
| **Buyer / collector (bounty creator)** | Signal demand for a wanted record; optionally advertise willingness to pay above typical market price |
| **Seller / digger (responder)** | Discover demand; respond with an existing or new listing |
| **Marketplace** | Increase liquidity, listing creation, and completed Compra Segura transactions |

### Why search and favorites are insufficient

| Capability | Limitation for “wanted” use case |
|------------|----------------------------------|
| **Explore / search** | Only surfaces **existing** listings |
| **Favorites** | Per-listing wishlist; no “notify when any listing matches X” in current product ([`SPEC.md`](SPEC.md) — Favorites IMPLEMENTED, no saved-search) |
| **Messaging** | Requires an existing listing thread |

### Value

| Stakeholder | Value |
|-------------|-------|
| **Buyers** | Public signal of demand; faster seller discovery; optional incentive visibility |
| **Sellers** | Qualified leads; reason to list dormant inventory |
| **Marketplace** | More listings, messages, and escrow-backed orders without new payment custody in MVP |

### Primary success condition

A buyer can publish an **active wanted request**, receive **at least one seller response** linked to a listing, and **complete purchase through existing Compra Segura** (order + escrow) without off-platform leakage.

---

## 2. Terminology

| Term | Definition |
|------|------------|
| **Bounty** | A buyer-published **wanted request** for a vinyl record, optionally including a **stated incentive** (informational in MVP). |
| **Bounty creator** | Authenticated user who owns the bounty. |
| **Wanted vinyl** | Target record metadata (artist, title, format, pressing/edition notes, condition preferences). Not a listing until a seller responds. |
| **Bounty response** (preferred) / **candidate offer** | A seller’s reply linking an **existing or newly created listing** to the bounty. One response = one listing proposal. |
| **Matched bounty** | Bounty with **≥1 active response** under buyer review (`MATCHED` or later). |
| **Accepted response** | The single response the buyer selected to pursue (`ACCEPTED`). Does not by itself move money. |
| **Fulfilled bounty** | Accepted path completed: linked **order reaches `completed`** via Compra Segura, **or** buyer marks fulfilled with audit trail (MVP may require order completion only — see open decisions). |
| **Expired bounty** | Past `expires_at` without acceptance; no longer discoverable as active. |
| **Cancelled bounty** | Creator or moderator terminated before fulfillment. |
| **Stated incentive** | Optional CLP amount the creator **declares** they are willing to pay **above or including** expected record price — **not held or guaranteed by Melómanos in MVP**. |
| **Expected record price** | Creator’s estimate of fair vinyl price (CLP), excluding Compra Segura platform fee. |
| **Reward / incentive (MVP)** | Synonym for **stated incentive** only — **not** escrowed funds. |

**Avoid:** Using “bounty” to mean both the request and the payment. Use **bounty** = request, **stated incentive** = optional declared amount, **Compra Segura payment** = actual transaction.

---

## 3. MVP scope

### Recommended MVP (Phase 1): Informational wanted board

See [`decisions/BOUNTIES_MVP_DECISION_RECORD.md`](decisions/BOUNTIES_MVP_DECISION_RECORD.md).

| In scope (MVP) | Out of scope (MVP) |
|----------------|-------------------|
| Create / edit / cancel bounty (authenticated) | Escrow or custody of incentive funds |
| Public discovery of **active** bounties | Automatic payout of stated incentive |
| Seller **response** linked to listing ID | Bounty-specific WebPay checkout |
| Buyer accept / reject responses | Platform fee on incentive amount |
| Handoff to **existing** listing message + order flow | Saved-search / alert engine (separate feature) |
| Expiration + basic moderation suspend | Digging Score changes from bounty activity |
| In-app notifications (new response, accepted, expired) | Email/push for bounty events |
| Protected messaging for negotiation | Counterfeit grading disputes beyond existing order/dispute |
| Rate limits + duplicate detection | Mobile app |
| Audit events (status history) | Public creator email/phone |

### Financial semantics (MVP)

| Concept | MVP behavior |
|---------|--------------|
| **Informational bounty** | Default — no money held |
| **Buyer-declared incentive** | Optional display field; **not enforceable** by platform in MVP |
| **Reserved / collected funds** | **Not in MVP** |
| **Seller payment** | Only via existing **Compra Segura** on linked listing order |
| **Marketplace fee** | Existing **$990 CLP** Compra Segura fee on orders — **not** applied to stated incentive unless separately approved |

Melómanos **does not** hold or transfer bounty incentive money in MVP. Stated incentive is **marketing signal only**.

---

## 4. User journeys

### 4.1 Buyer creates bounty

1. Authenticated user opens **Crear bounty** (`/bounties/new`).
2. Enters wanted vinyl metadata (required: artist, title; optional: label, year, pressing, min grades, notes, Discogs release ID if known).
3. Optionally sets **expected record price** and **stated incentive** (CLP).
4. Sets expiration (default 30 days; max 90 — policy TBD).
5. Submits → bounty `ACTIVE` (or `DRAFT` if draft flow included).
6. **Empty state:** validation errors inline; subscription limits N/A for bounties in MVP.

**Failure:** Unauthenticated → redirect `/login`. Rate limit → Spanish error.

### 4.2 Buyer edits or cancels

- **Edit:** Allowed while `ACTIVE` and **no accepted response**; edits logged in status history.
- **Cancel:** Creator may cancel while not `FULFILLED`; active responses marked withdrawn; responders notified.

### 4.3 Discover active bounties

- **Browse** `/bounties` — filter/sort by recency, incentive (optional), genre tags if added later.
- **Detail** `/bounties/[id]` — public wanted metadata; creator shown as **display name + trust signals** (no contact).
- **Empty state:** “No hay bounties activos” + CTA to create.

### 4.4 Seller responds

1. Authenticated seller views bounty detail → **Responder**.
2. **Preferred MVP:** Select **existing active listing** (`status = available`) OR **create new listing** (redirect `/sell` with bounty context prefilled).
3. Response includes optional message (opens protected messaging thread on linked listing **or** bounty-scoped thread — see integration).
4. Buyer notified via in-app notification.

**Failure paths:** Listing not owned by seller; listing sold/reserved; duplicate response same listing; bounty expired mid-flow.

### 4.5 Buyer evaluates responses

- Inbox on bounty detail or **Mis bounties** → list responses with listing preview, price, seller reputation.
- **Accept** one response → bounty `ACCEPTED`; other pending responses auto-rejected or withdrawn.
- **Reject** individual responses while staying `MATCHED`.

### 4.6 Acceptance → fulfillment

1. Accepted response deep-links to **listing detail** → buyer uses normal **Compra Segura** reserve/checkout.
2. Bounty remains `ACCEPTED` until linked order `completed` → auto `FULFILLED`.
3. If order cancelled before payment held → bounty returns to `MATCHED` or `ACTIVE` (policy: return to `MATCHED` if other responses exist).

**Dispute path:** Existing order dispute flow; bounty status unchanged except optional flag `fulfillment_disputed` for ops.

### 4.7 Expiration

- Cron/job sets `EXPIRED` at `expires_at`; hidden from public discovery; creator notified; responses archived read-only.

### 4.8 Notifications and messaging touchpoints

| Event | Notification (proposed) | Messaging |
|-------|-------------------------|-----------|
| New response | Creator | Optional intro via listing thread |
| Response accepted | Responder | Encourage Compra Segura checkout |
| Response rejected | Responder | None required |
| Bounty expired | Creator + pending responders | Threads read-only |
| Bounty cancelled | Responders | — |

All message bodies subject to [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) Protected Messaging Rules.

---

## 5. State model

### States

| State | Meaning | Terminal? |
|-------|---------|-----------|
| `DRAFT` | Not published (optional MVP) | No |
| `ACTIVE` | Discoverable; accepting responses | No |
| `MATCHED` | ≥1 pending response; none accepted | No |
| `ACCEPTED` | One response selected; checkout expected | No |
| `FULFILLED` | Linked order completed (or manual confirm if approved) | **Yes** |
| `EXPIRED` | Past expiration without fulfillment | **Yes** |
| `CANCELLED` | Creator/mod cancelled | **Yes** |
| `SUSPENDED` | Moderation hold | No → may become `CANCELLED` |

### Transition table (summary)

| From | To | Actor | Preconditions | Effects |
|------|-----|-------|---------------|---------|
| `DRAFT` | `ACTIVE` | Creator | Valid fields | Visible in discovery |
| `ACTIVE` | `MATCHED` | System | First response submitted | Notify creator |
| `MATCHED` | `ACCEPTED` | Creator | One response selected | Reject/withdraw others; notify responder |
| `ACCEPTED` | `FULFILLED` | System | Linked order `completed` | Audit; optional metrics |
| `ACCEPTED` | `MATCHED` | System | Order cancelled pre-payment | Re-open other responses if any |
| `*` (non-terminal) | `CANCELLED` | Creator / Admin | Not `FULFILLED` | Withdraw responses |
| `ACTIVE`/`MATCHED` | `EXPIRED` | System | `now > expires_at` | Delist |
| `*` | `SUSPENDED` | Admin | Abuse report / policy | Hide from discovery |

**Reservation/order coupling:** Accepting a response **must not** auto-call `POST /orders/from-listing/{id}`. Buyer explicitly starts purchase. Listing reservation rules unchanged ([`DESIGN.md`](DESIGN.md)).

**Reversibility:** `ACCEPTED` → `MATCHED` only before payment held. `FULFILLED`, `EXPIRED`, `CANCELLED` are terminal.

---

## 6. Business rules

### Creation

- **Who:** Authenticated users with verified account (same as messaging).
- **Required fields:** Artist, title (Spanish/UTF-8); at least one distinguishing attribute (year, label, pressing, or free-text “detalles”).
- **Optional:** Discogs release ID (numeric, validated format); expected record price CLP; stated incentive CLP; min record/cover grade (Discogs enum); expiration date.
- **Limits (proposed):** Max 5 active bounties per user; max 1 active bounty per normalized `(artist, title, pressing_key)` per creator; global rate limit 10 creates/day/user.

### Pricing and currency

- All amounts **CLP integers** (consistent with listings/orders).
- **Stated incentive** ≥ 0; if > 0, must be ≥ minimum display threshold (e.g. $1.000 CLP) to reduce noise.
- Display: “Incentivo declarado (informativo)” — not a payment promise.

### Responses

- **Who:** Authenticated sellers (any plan).
- **Listing required:** Response must reference `listing_id` where seller is owner and listing `available` (recommended — see open decision on create-on-respond).
- **Multiple responses:** Allowed from different sellers; one response per seller per bounty; one listing per response.
- **Without listing:** Deferred — increases fraud risk.

### Acceptance and cancellation

- Only creator accepts; only one accepted response at a time.
- Creator cannot cancel after buyer (creator) has initiated payment on linked order without admin path.
- Seller may withdraw own pending response anytime before acceptance.

### Duplicates

- Multiple users may bounty the same record — allowed (market signal).
- Same creator duplicate active bounty — blocked via normalized key.

### Fulfillment evidence

- **Primary:** Order ID linked to accepted response reaches `completed`.
- **Manual buyer confirm:** Deferred (abuse risk).

### Moderation

- Admin may `SUSPEND` or `CANCEL` for fake/spam/abuse.
- Public fields scanned for contact patterns (same categories as messaging where applicable).
- Retention: terminal bounties retained 12 months for audit (proposed); PII per existing user deletion policy.

### Audit trail

- `BountyStatusHistory`: `from_status`, `to_status`, `actor_id`, `reason`, `timestamp`, optional `metadata_json`.

---

## 7. Trust, abuse, and adversarial review

| Risk | Likelihood | Impact | MVP mitigation | Deferred | Detection |
|------|------------|--------|----------------|----------|-----------|
| Fake bounties (no intent to buy) | Medium | Medium | Rate limits; min field quality; report button | Reputation penalty | Report queue; creator accept→order conversion rate |
| Fake responses / wrong listing | Medium | High | Listing must be `available` + owned; buyer inspects listing | Response verification photos | Buyer reject; admin suspend |
| Price manipulation (inflated incentive) | Low | Low | Label as informational only | Escrowed incentive | Display disclaimer |
| Bait-and-switch after accept | Medium | High | Purchase via Compra Segura + disputes | — | Order/dispute evidence |
| Off-platform contact | High | High | Protected messaging; no contact in bounty text filters | — | `message_safety` patterns |
| Contact in bounty description | Medium | High | Server-side filter on create/edit | ML moderation | Block + 400 |
| Spam duplicate bounties | Medium | Low | Per-user caps; normalized dedup | Captcha | Rate limit metrics |
| Harassment in responses | Low | Medium | Report; suspend; existing messaging blocks | — | User reports |
| Collusion (fake fulfill) | Low | High | Fulfillment = order completed only | — | Order graph audit |
| Buyer cancels after seller effort | Medium | Medium | No penalty MVP; messaging preserves good faith | Cancellation policy + reputation | — |
| Counterfeit / grading disputes | Medium | Medium | Existing dispute on order | — | Order dispute |
| Stolen listing images | Low | Medium | Report listing; existing moderation | Image hash | Admin |
| Account farming | Low | Medium | Auth required; rate limits | Device fingerprint | Anomaly metrics |
| Reputation gaming | Low | Low | **No** Digging Score change in MVP | Defined bounty rules | — |

---

## 8. Privacy and security

### Public vs private

| Field | Visibility |
|-------|------------|
| Wanted metadata, grades, notes (sanitized) | Public when `ACTIVE`/`MATCHED`/`ACCEPTED` |
| Stated incentive, expected price | Public (with disclaimer) |
| Creator user ID | Internal; public display name + avatar only |
| Response message preview | Creator only until accept; then participants |
| Linked order IDs | Creator + accepted responder only |
| Email, phone, address | **Never** on bounty surfaces |

### Authorization

- CRUD bounty: creator only (except admin).
- Submit response: any authenticated seller; not creator on own bounty (prevent self-dealing) — **recommended rule**.
- Accept/reject response: creator only.
- View suspended bounty: admin + creator.

### Messaging

- Reuse listing-scoped threads where possible ([`routers/messages.py`](../backend/app/routers/messages.py)).
- Contact-data filtering unchanged.

### Rate limits

- Create bounty: 10/day/user.
- Response: 20/day/user.
- Report: 5/day/user.

---

## 9. Payments and legal boundary

### Established product facts

- Compra Segura holds **order** funds after payment confirmation ([`BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md)).
- Platform fee **$990 CLP** per order on listing transactions.
- Real WebPay production **not** integrated until explicitly approved.

### MVP legal boundary

| Topic | MVP stance |
|-------|------------|
| Incentive custody | **None** — stated incentive is non-binding expression |
| Tax / consumer law (Chile) | **Requires external validation** before any fund-holding model |
| Refunds on stated incentive | N/A in MVP |
| Platform commission on incentive | **Not in MVP** |

### Future models (NOT_APPROVED)

| Phase | Description | Approval required |
|-------|-------------|-------------------|
| Phase 3a | Optional **escrow-like** incentive hold separate from listing price | Legal + payment provider + TYPE F/H |
| Phase 3b | Platform fee on bounty feature | Business + legal |

**No legal conclusions** in this document.

---

## 10. Integration with existing product

| Domain | Reuse | New work |
|--------|-------|----------|
| **Auth** | JWT sessions | Bounty ownership checks |
| **Listings** | Response links to listing; `/sell` prefill | Bounty context param |
| **Favorites** | Complementary (not replaced) | — |
| **Messaging** | Listing threads + safety filters | Optional bounty system messages |
| **Notifications** | Extend event types | `bounty.response`, `bounty.accepted`, etc. |
| **Orders / reservations** | Post-acceptance purchase only | Store `accepted_order_id` on bounty |
| **Trust / reputation** | Display seller badges on responses | No score change MVP |
| **Digging Score** | No change MVP | Future rule if approved |
| **Search / Explore** | Separate discovery route `/bounties` | Optional cross-link |
| **Profile** | “Mis bounties” tab | Profile stats |
| **Admin** | Suspend/cancel | Admin bounty list |

**Conflict avoidance:** Bounty acceptance does **not** change listing status until standard order flow runs.

---

## 11. Conceptual data and API model

*Conceptual only — no migrations or endpoints in M-010.*

### Entities

```
User 1──* Bounty
Bounty 1──* BountyResponse *──1 Listing
Bounty 1──* BountyStatusHistory
BountyResponse 0──1 Order (after acceptance checkout)
User 1──* BountyResponse (as responder)
```

### Bounty (conceptual fields)

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | PK |
| `creator_id` | FK User | |
| `status` | enum | State model §5 |
| `artist`, `title` | string | Required |
| `label`, `year`, `pressing_notes` | optional | |
| `discogs_release_id` | optional int | |
| `min_record_grade`, `min_cover_grade` | optional enum | Discogs grades |
| `details_text` | text | Filtered |
| `expected_price_clp` | optional int | |
| `stated_incentive_clp` | optional int | Informational MVP |
| `expires_at` | timestamp | |
| `accepted_response_id` | optional FK | |
| `fulfilled_order_id` | optional FK | |
| `created_at`, `updated_at` | timestamps | |

### BountyResponse

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | |
| `bounty_id`, `responder_id`, `listing_id` | FKs | |
| `status` | enum | `pending`, `accepted`, `rejected`, `withdrawn` |
| `message` | optional text | Safety-filtered |
| `created_at` | timestamp | |

### Concurrency

- Accept response: **atomic** — single transaction; lock bounty row; verify still `MATCHED`/`ACTIVE`.
- Expire job: idempotent status transition.

### Conceptual API surface (future)

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/bounties` | List active (public) |
| POST | `/bounties` | Create |
| GET/PATCH/DELETE | `/bounties/{id}` | Detail / edit / cancel |
| GET | `/bounties/mine` | Creator list |
| POST | `/bounties/{id}/responses` | Submit response |
| PATCH | `/bounties/{id}/responses/{rid}` | Accept / reject |
| GET | `/users/me/bounties` | Alias for mine |

---

## 12. UX information architecture

| Screen | Route (proposed) | Entry points |
|--------|------------------|--------------|
| Discovery | `/bounties` | Nav link (Phase 2 UI); Explore cross-promo |
| Detail | `/bounties/[id]` | Discovery, notifications |
| Create | `/bounties/new` | CTA on discovery, profile |
| Manage | `/bounties/mine` or profile tab | Profile, creator notifications |
| Respond | Modal on detail | Detail CTA |
| Messaging handoff | `/listings/[id]` + `/messages` | After accept |

**Navigation:** Phase 1 back-link pattern (`← Volver a Explorar` or parent context) per existing IA ([M-019 remediation](../reports/missions/M-019_EXECUTION_REPORT.md)).

**Visual design:** NOT_APPROVED — subject to Visual Polish human gate when implemented.

---

## 13. Metrics

| Metric | Definition | Operational use |
|--------|------------|-----------------|
| Active bounties | Count `ACTIVE` + `MATCHED` + `ACCEPTED` | Liquidity |
| Response rate | Bounties with ≥1 response / active created | Demand quality |
| Time to first response | Median hours | Seller engagement |
| Match rate | `MATCHED` or higher / created | — |
| Acceptance rate | `ACCEPTED` or higher / with responses | Buyer seriousness |
| Fulfillment rate | `FULFILLED` / `ACCEPTED` | Core success |
| Cancellation rate | `CANCELLED` / created | Abuse/UX signal |
| Expiration rate | `EXPIRED` / created | Stale demand |
| Abuse report rate | Reports / active bounties | Trust |
| Order conversion | Orders from accepted responses / `ACCEPTED` | Revenue linkage |

---

## 14. Rollout strategy

| Phase | Deliverable | Approval |
|-------|-------------|----------|
| **0** | M-010 spec + human decision closure (M-020) | This document |
| **1** | Informational bounties: backend domain + API + basic UI | TYPE F/H per mission |
| **2** | Notifications, discovery polish, E2E, abuse reports | TYPE C/F |
| **3** | Optional financial incentive / escrow | Separate legal + product gate |

Align with [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) promotion process — **not** in current MVP queue until promoted.

---

## 15. Open human decisions

| Decision | Options | Recommendation | Evidence | Human approval required |
|----------|---------|----------------|----------|-------------------------|
| MVP financial model | A) Informational only B) Escrow incentive | **A** | No custody infra; Compra Segura covers transactions | **Yes** — confirm A |
| Public display of stated incentive | A) Always show if set B) Hide until response C) Never in MVP | **A** with disclaimer | User concept mentions incentive | Yes |
| Seller response without listing | A) Listing required B) Create-on-respond C) Text-only response | **A** (listing required) | Listing ties to Compra Segura | Yes |
| Self-response (creator responds to own bounty) | A) Block B) Allow | **A) Block** | Collusion risk | Yes |
| Fulfillment definition | A) Order completed only B) Manual buyer confirm | **A** | Auditable | Yes |
| Digging Score for bounty fulfill | A) None MVP B) +N points | **A** | BUSINESS_RULES score from orders | Yes |
| Active bounty limit per user | 3 / 5 / 10 | **5** | Balance spam vs utility | Yes |
| Promote to MVP_ROADMAP | Now / After beta / Defer | **After closed beta** | Roadmap focus: deployment, WebPay | Yes |

---

## Alternatives considered

See §3 and [`decisions/BOUNTIES_MVP_DECISION_RECORD.md`](decisions/BOUNTIES_MVP_DECISION_RECORD.md).

1. **Full bounty marketplace** — escrow incentive + matching engine — **rejected for MVP** (legal/payment complexity).
2. **Lightweight wanted board + optional stated incentive** — **recommended**.
3. **Saved search + notifications** — lower cost; does not surface seller-seeking-buyer — **complementary future mission**.
4. **Request-for-offer without financial reward** — subset of option 2 (incentive optional).

---

## Premortem (6-month failure scenarios)

| Failure mode | Likely cause | Prevention |
|--------------|--------------|------------|
| Ghost town | Too few bounties | Seed with collectors; profile CTAs |
| Unanswered bounties | Low seller awareness | Notifications + Explore promo |
| Incentive confusion | Users think money is held | Persistent “informativo” copy |
| Off-platform deals | Sellers bypass fee | Messaging safety + checkout CTA |
| Ops overload | Disputes on wrong records | Fulfillment = order only |
| Feature bloat | Built escrow too early | Phase gating |

---

*End of Bounties Product Specification.*
