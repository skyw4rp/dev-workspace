# AI_CONTEXT — Melómanos Marketplace

**Purpose:** Workspace onboarding index for humans and AI agents.  
**Last synced:** 2026-07-09 (Stack constraints + tool intelligence + UI mission candidates)  
**Root layout:** `C:\melomanos\{backend, frontend, workspace}`

> **This file is an index, not a specification.**  
> On conflict, **`backend/BUSINESS_RULES.md`**, **`backend/ARCHITECTURE.md`**, and **`backend/MVP_ROADMAP.md`** override any summary here.  
> Operational Cursor missions use **`workspace/NEXT_ACTION_QUEUE.md`** — they do not override roadmap or visual human PASS gates.  
> Stack, isolation, and tool rules: **[`STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md)**.

---

## What Melómanos Is

Chile-focused vinyl marketplace with Compra Segura (escrow), Discogs-style grading, protected messaging, and collector trust signals.

**Product and business detail:** see [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md)  
**Technical structure:** see [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md)  
**What to build next:** see [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md)

---

## Workspace Role

| Workspace doc | Role |
|---------------|------|
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | This file — start here |
| [`STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md) | Project isolation, registered stack, tool intelligence (Cursor / v0) |
| [`MISSION_EXECUTION_GUIDE.md`](MISSION_EXECUTION_GUIDE.md) | Bounded mission execution (one mission → one report → one gate) |
| [`NEXT_ACTION_QUEUE.md`](NEXT_ACTION_QUEUE.md) | Ready missions (TYPE A–H) for Cursor sessions |
| [`TASKS.md`](TASKS.md) | Task board index → roadmap |
| [`SPEC.md`](SPEC.md) | MVP coverage index → authoritative specs |
| [`DESIGN.md`](DESIGN.md) | Flow and layout index → architecture |
| [`RELEASE_NOTES.md`](RELEASE_NOTES.md) | Release index → roadmap / status |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Living snapshot |
| [`VISUAL_POLISH_CONTROL.md`](VISUAL_POLISH_CONTROL.md) | Visual polish gate (human PASS) |
| [`VISUAL_FEEDBACK_LOOP_CONTROL.md`](VISUAL_FEEDBACK_LOOP_CONTROL.md) | Screenshot evidence feedback loop |
| [`AI_DEV_OS_PROJECT_SCAN.md`](AI_DEV_OS_PROJECT_SCAN.md) | Audit scan (2026-06-17) |

---

## Current Snapshot (pointers only)

| Item | Where to read |
|------|----------------|
| Active task | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) — Current Active Task |
| Completed milestones (13) | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) — Completed |
| Quality Gate | [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md) |
| Last release | [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) — Latest Release markers |
| Registered API routers | [`backend/app/main.py`](../backend/app/main.py) |
| Frontend routes | [`frontend/src/app/`](../frontend/src/app/) |

---

## Agent Onboarding (minimal)

1. Read this file.
2. Read [`STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md) (stack + Cursor/v0 rules).
3. Read [`backend/AGENT_RULES.md`](../backend/AGENT_RULES.md).
4. Confirm active task in [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).
5. Read [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md).
6. For Cursor execution sessions: read [`MISSION_EXECUTION_GUIDE.md`](MISSION_EXECUTION_GUIDE.md) and pick one mission from [`NEXT_ACTION_QUEUE.md`](NEXT_ACTION_QUEUE.md).
7. Read the relevant section of [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) before implementing (TYPE F/H only with explicit approval).

**Path config:** [`workspace/README_PROJECT_LAYOUT.md`](README_PROJECT_LAYOUT.md) — set `MELOMANOS_*_DIR` when not using legacy defaults.

**Quality Gate commands:** [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md).

**Tool default:** Implement in **Cursor**. Do not use **v0** for backend, auth, DB, reservations, security, tests, or production integration.

---

## Registered stack (summary)

| Side | Stack |
|------|--------|
| Frontend | Next.js + TypeScript + React + Tailwind |
| Backend | FastAPI + SQLAlchemy + Alembic + PostgreSQL |
| Domains | Auth, listings, reservations/orders, messaging, payments, favorites, notifications, profile, admin |

Full constraints: [`STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md).

---

## Source Documents

### Authoritative (highest priority)

| Document | Path |
|----------|------|
| Business rules | [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) |
| Architecture | [`backend/ARCHITECTURE.md`](../backend/ARCHITECTURE.md) |
| MVP roadmap | [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md) |

### Backend governance

| Document | Path |
|----------|------|
| AI OS overview | [`backend/AI_OS_OVERVIEW.md`](../backend/AI_OS_OVERVIEW.md) |
| Agent rules | [`backend/AGENT_RULES.md`](../backend/AGENT_RULES.md) |
| Testing strategy | [`backend/TESTING_STRATEGY.md`](../backend/TESTING_STRATEGY.md) |
| Project status (backend) | [`backend/PROJECT_STATUS.md`](../backend/PROJECT_STATUS.md) |
| Changelog | [`backend/CHANGELOG.md`](../backend/CHANGELOG.md) |
| API overview | [`backend/docs/api_overview.md`](../backend/docs/api_overview.md) *(may be incomplete vs code)* |

### Workspace

| Document | Path |
|----------|------|
| Quality gate | [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md) |
| Stack constraints | [`workspace/STACK_CONSTRAINTS.md`](STACK_CONSTRAINTS.md) |
| Mission execution guide | [`workspace/MISSION_EXECUTION_GUIDE.md`](MISSION_EXECUTION_GUIDE.md) |
| Next action queue | [`workspace/NEXT_ACTION_QUEUE.md`](NEXT_ACTION_QUEUE.md) |
| Mission briefs | [`workspace/missions/`](missions/) |
| Mission reports | [`workspace/reports/missions/`](reports/missions/) |
| Project status | [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) |
| Visual polish control | [`workspace/VISUAL_POLISH_CONTROL.md`](VISUAL_POLISH_CONTROL.md) |
| Visual feedback loop | [`workspace/VISUAL_FEEDBACK_LOOP_CONTROL.md`](VISUAL_FEEDBACK_LOOP_CONTROL.md) |
| Project scan | [`workspace/AI_DEV_OS_PROJECT_SCAN.md`](AI_DEV_OS_PROJECT_SCAN.md) |
| Foundation sync report | [`workspace/AI_DEV_OS_FOUNDATION_SYNC_REPORT.md`](AI_DEV_OS_FOUNDATION_SYNC_REPORT.md) |

### Code entry points

| Area | Path |
|------|------|
| API bootstrap | [`backend/app/main.py`](../backend/app/main.py) |
| Frontend API client | [`frontend/src/lib/api.ts`](../frontend/src/lib/api.ts) |
| E2E flows | [`frontend/e2e/melomanos.spec.ts`](../frontend/e2e/melomanos.spec.ts) |

---

*Update after major milestones via `finish_task.py`. Do not duplicate content from Source Documents — link instead.*
