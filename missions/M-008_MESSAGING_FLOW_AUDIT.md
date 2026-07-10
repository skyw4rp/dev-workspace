# M-008 — Messaging Flow Audit

**Mission ID:** M-008  
**Type:** TYPE A — Review Only  
**Priority:** P2  
**Route:** `/messages`, listing message form

---

## Goal

Audit inbox/thread UX and known reply/contact-leak constraints. Distinguish UX polish vs backend rule work.

---

## Scope

- Read `/messages` page UX
- Read messaging E2E coverage
- Read backend `message_safety` references (read-only)
- Recommend TYPE C polish if warranted

---

## Forbidden

- Code changes
- Backend API / business logic
- Route PASS
- Commits

---

## Acceptance criteria

Flow findings ranked; UX vs TYPE F distinction; recommended next mission.
