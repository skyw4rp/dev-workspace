# Stack Constraints — Melómanos Market

**System:** AI Dev OS Project Isolation + Stack Constraints (Melómanos adoption)  
**Product:** Melómanos Market  
**Last updated:** 2026-07-09  
**Authority:** This file constrains tool choice and mission classification. It does **not** override [`backend/BUSINESS_RULES.md`](../backend/BUSINESS_RULES.md).

---

## Project isolation

| Field | Value |
|-------|--------|
| **Root** | `C:\melomanos\` |
| **Repos** | Three separate git repos: `frontend/`, `backend/`, `workspace/` |
| **Workspace role** | Governance, missions, Visual Polish, reports, ops scripts — not application runtime |
| **Source of truth** | Code in `frontend/` + `backend/`; business rules in backend docs |

Do not treat Melómanos as a monorepo for commits. Use file-by-file staging per repo. Never `git add .` across the tree.

---

## Registered stack

### Frontend

| Layer | Technology |
|-------|------------|
| Framework | **Next.js** (App Router) + **TypeScript** |
| UI | **React** + **Tailwind CSS** |
| Shared styles | `frontend/src/app/globals.css` (editorial tokens, shared button/input/card classes) |
| E2E | Playwright (`npm run test:e2e`, `npm run test:e2e:visual-polish`) |
| Unit | Vitest (`npm run test:unit`) |

### Backend

| Layer | Technology |
|-------|------------|
| API | **FastAPI** |
| ORM | **SQLAlchemy** |
| Migrations | **Alembic** |
| Database | **PostgreSQL** (local + production target) |
| Tests | pytest |

### Product domains (existing — high sensitivity)

Treat these as **in-repo product domains**, not greenfield:

| Domain | Notes |
|--------|--------|
| **Auth / session** | Login, tokens, protected routes |
| **Listings** | Catalog, sell flow, grading, covers, video rules |
| **Reservations / orders** | Compra Segura, escrow, shipping, disputes |
| **Messaging** | Protected inbox, contact-leak rules, replies |
| **Payments** | WebPay placeholder / simulate modes |
| **Favorites / notifications / profile** | Collector surfaces |
| **Admin** | Internal; visual polish default OUT_OF_SCOPE |

Changes that touch domain **rules** are TYPE F/H — not TYPE C polish.

---

## Evidence-grounded tool intelligence

| Tool | Role for Melómanos |
|------|---------------------|
| **Cursor** | **Primary implementation tool** for all real repo changes (frontend, backend, workspace docs, tests, integration) |
| **v0** | **Optional** UI prototyping only for compatible **frontend visual** missions |
| **ChatGPT / planning** | Specs, mission briefs, gate review — not a substitute for Cursor commits |
| **Playwright / pytest** | Verification evidence — not visual PASS |

### v0 rules (hard)

**Allowed (optional):**

- Early visual exploration for TYPE C UI surfaces (cards, filters chrome, empty states, layout sketches)
- Producing **proposals** that a human or Cursor then integrates into the real Next.js + Tailwind codebase

**Forbidden:**

- Backend, FastAPI, SQLAlchemy, Alembic, PostgreSQL
- Auth, security, reservations/orders, messaging rules, payments
- Tests as the only “integration”
- Production wiring, env secrets, deploy
- Treating v0 output as the product source of truth

**Integration rule:** v0 may propose UI → **Cursor must integrate** into `frontend/` → Melómanos repo remains source of truth → Visual Polish human PASS still required for route PASS.

---

## Model routing (Melómanos practical map)

| Work | Prefer |
|------|--------|
| TYPE A/B audits, governance, reports | Fast/cheap reasoning OK; accuracy over flair |
| TYPE C visual polish in existing design system | Implementation-capable model in **Cursor** |
| TYPE F/H business logic | Strongest available + explicit `APPROVE_MISSION_EXECUTION`; read BUSINESS_RULES first |
| TYPE G product design | Spec-focused; no code |
| UI prototype exploration | Optional v0 **only** if mission brief allows; then Cursor |

Do not route backend or domain-rule work to UI generators.

---

## Vision / North Star (product)

Melómanos Market is a **premium editorial vinyl marketplace** for the electronic-vinyl community (DJs, diggers, collectors, labels):

- Warm ivory / off-white, black/charcoal, sober gold
- Curated, niche, collector culture — **not** generic SaaS, rave, or Discogs visual copy
- Compra Segura and protected messaging are product pillars

Visual system authority: [`VISUAL_POLISH_CONTROL.md`](VISUAL_POLISH_CONTROL.md), [`VISUAL_FEEDBACK_LOOP_CONTROL.md`](VISUAL_FEEDBACK_LOOP_CONTROL.md).

---

## Application factory note

Melómanos is an **existing production-bound product**, not a blank Application Factory scaffold. New OS factory templates must **adapt to** this stack and domains — do not regenerate the app from a generic template.

---

## EES / evidence expectations

| Evidence | Use |
|----------|-----|
| Mission execution reports | `reports/missions/` |
| Visual audit reports | `reports/visual-audit/` |
| Screenshot runs | `screenshots/visual-polish/runs/` (gitignored; not PASS) |
| Approved baselines | Root approved PNGs / future `approved/` |
| Quality Gate | [`QUALITY_GATE.md`](QUALITY_GATE.md) |

Missions should cite evidence paths. Do not invent PASS from green tests alone.

---

## README / docs hygiene

- Prefer **indexes that link** over duplicating BUSINESS_RULES / roadmap content
- Keep `AI_CONTEXT.md` short; put stack/tool rules here
- Mission queue is operational; roadmap remains product backlog authority
- Do not commit `runs/`, secrets, or `test-results/`

---

## Related

| Doc | Role |
|-----|------|
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | Onboarding index |
| [`MISSION_EXECUTION_GUIDE.md`](MISSION_EXECUTION_GUIDE.md) | Mission pattern + tokens |
| [`NEXT_ACTION_QUEUE.md`](NEXT_ACTION_QUEUE.md) | Ready missions |
| [`QUALITY_GATE.md`](QUALITY_GATE.md) | Functional DoD |
# Canonical authority boundary

`PROJECT_STATUS.md` is read first for every execution, technical command, validation, or session. Parse its exact JSON authority block and require an exact `READY` mission plus the requested action class. If the block is absent, duplicated, malformed, stale, or conflicts with prose, STOP. Tokens, queues, roadmaps, briefs, reports, decisions, and gate PASS results are intent or evidence, never authority. A gate is read-only unless the canonical block explicitly permits its validation command.
