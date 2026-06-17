# AI_CONTEXT — Melómanos Marketplace

**Purpose:** Workspace onboarding index for humans and AI agents.  
**Last synced:** 2026-06-17 (Foundation Sync, constraint pass)  
**Root layout:** `C:\melomanos\{backend, frontend, workspace}`

> **This file is an index, not a specification.**  
> On conflict, **`backend/BUSINESS_RULES.md`**, **`backend/ARCHITECTURE.md`**, and **`backend/MVP_ROADMAP.md`** override any summary here.

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
| [`TASKS.md`](TASKS.md) | Task board index → roadmap |
| [`SPEC.md`](SPEC.md) | MVP coverage index → authoritative specs |
| [`DESIGN.md`](DESIGN.md) | Flow and layout index → architecture |
| [`RELEASE_NOTES.md`](RELEASE_NOTES.md) | Release index → roadmap / status |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Living snapshot |
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
2. Read [`backend/AGENT_RULES.md`](../backend/AGENT_RULES.md).
3. Confirm active task in [`backend/MVP_ROADMAP.md`](../backend/MVP_ROADMAP.md).
4. Read [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md).
5. Read the relevant section of [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md) before implementing.

**Path config:** [`workspace/README_PROJECT_LAYOUT.md`](README_PROJECT_LAYOUT.md) — set `MELOMANOS_*_DIR` when not using legacy defaults.

**Quality Gate commands:** [`workspace/QUALITY_GATE.md`](QUALITY_GATE.md).

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
| Project status | [`workspace/PROJECT_STATUS.md`](PROJECT_STATUS.md) |
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
