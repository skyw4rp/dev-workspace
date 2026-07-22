# Melómanos Market — Project Status

Living snapshot for product and quality status. Updated manually or via `py finish_task.py` after a successful release.

<!-- STATUS:LAST_QUALITY_GATE_START -->
## Last Quality Gate

- Date: 2026-06-30 23:15
- Backend tests: PASSED
- Frontend build: PASSED
- E2E tests: PASSED
- Full audit: PASSED
<!-- STATUS:LAST_QUALITY_GATE_END -->

<!-- STATUS:LATEST_RELEASE_START -->
## Latest Release

- Backend: Add production deployment backend
- Frontend: Add dispute resolution frontend
- Quality Gate: PASSED
- Date: 2026-06-30 23:15
<!-- STATUS:LATEST_RELEASE_END -->

<!-- STATUS:ROADMAP_FOCUS_START -->
## Historical Roadmap Focus (superseded)

- **Snapshot task:** Production Deployment; superseded by the deferred disposition below.
- **Last completed task:** Notifications
<!-- STATUS:ROADMAP_FOCUS_END -->

## AI Dev OS Foundation Sync

- **Sync date:** 2026-06-17
- **Audit reference:** `AI_DEV_OS_PROJECT_SCAN.md`
- **Foundation report:** `AI_DEV_OS_FOUNDATION_SYNC_REPORT.md`
- **New governance artifacts:** `AI_CONTEXT.md`, `TASKS.md`, `SPEC.md`, `DESIGN.md`, `RELEASE_NOTES.md`

## Bounded Autonomous Mission Execution (2026-07-08)

- **Guide:** `MISSION_EXECUTION_GUIDE.md`
- **Queue:** `NEXT_ACTION_QUEUE.md`
- **M-001:** DONE — `reports/missions/M-001_EXECUTION_REPORT.md`
- **Pattern:** One mission → one execution report → one gate review
- Does **not** replace Visual Polish human PASS or Quality Gate DoD

## AI Dev OS Stack + Tool Intelligence (2026-07-09)

- **Stack constraints:** `STACK_CONSTRAINTS.md`
- **Frontend:** Next.js + TypeScript + Tailwind
- **Backend:** FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Primary implementation tool:** Cursor
- **v0:** Optional UI prototype only; never backend/auth/DB/reservations/security/tests/production
- **UI mission candidates:** M-011–M-015 (listing card, explore filters, product detail, empty states, mobile nav)
- **Next recommended mission (not auto-executed):** **M-002** — Profile UX audit (TYPE A)

## Operational authority and current state

This file is the **sole cross-repository operational-state authority**. The AI Dev OS operational runtime is disabled. Its canonical authority may instead authorize one explicitly human-authorized, bounded direct Codex mission under `HUMAN_AUTHORIZED_DIRECT_CODEX`; this is not a runtime lease, simulated lease, automatic launch, or continuous autonomy. The subordinate queue in [`NEXT_ACTION_QUEUE.md`](NEXT_ACTION_QUEUE.md) records execution order but cannot authorize work independently.

**Canonical authority notice:** The machine-readable block below is the sole operational authority. All other status prose in this file is explanatory or historical and cannot authorize work.

<!-- AI_DEV_OS_OPERATIONAL_AUTHORITY_BEGIN -->
{
    "schema_version":  3,
    "authority_file":  "workspace/PROJECT_STATUS.md",
    "authority_revision":  5,
    "manual_execution_mode":  "HUMAN_AUTHORIZED_DIRECT_CODEX",
    "operational_runtime":  "DISABLED",
    "automatic_codex_launch":  "NOT_IMPLEMENTED",
    "continuous_autonomy":  "DISABLED",
    "authorized_mission":  {
                               "id":  "MEL-UX-003",
                               "status":  "READY",
                               "mode":  "HUMAN_AUTHORIZED_DIRECT_CODEX",
                               "repository":  "C:\\melomanos\\frontend"
                           },
    "blocked_missions":  [
                              {
                                  "id":  "MEL-UX-001",
                                  "status":  "BLOCKED_BY_INACTIVE_OS_RUNTIME"
                              }
                          ],
    "held_missions":  [

                      ],
    "completed_missions":  [
                               {
                                   "id":  "MEL-GOV-001-FINAL",
                                   "status":  "DONE"
                               }
                           ],
    "m021":  "HOLD",
    "os_routing_001":  "HOLD",
    "os_routing_001_disposition":  "OS_ROUTING_HOTFIX_SCOPE_EXCEEDED",
    "bounties":  "EXPERIMENTAL_HOLD",
    "production_deployment":  "DEFERRED_NOT_AUTHORIZED",
    "allowed_actions":  [
                            "repository_read",
                            "branch_create",
                            "product_code",
                            "focused_tests",
                            "lint",
                            "typecheck",
                            "build",
                            "git_inspection",
                            "status_reporting"
                        ],
    "forbidden_actions":  [
                              "server",
                              "network",
                              "cloud",
                              "secrets",
                              "database",
                              "deployment",
                              "stage",
                              "commit",
                              "push",
                              "merge",
                              "pull_request",
                              "publication",
                              "force_push",
                              "rebase",
                              "amend",
                              "reset",
                              "restore",
                              "clean",
                              "stash",
                              "tags",
                              "releases",
                              "runtime_activation",
                              "simulated_leases",
                              "paid_services",
                              "paid_apis",
                              "automatic_deployment"
                          ]
}
<!-- AI_DEV_OS_OPERATIONAL_AUTHORITY_END -->

## Reconciliation binding

The canonical JSON block above is controlling and must be parsed, not interpreted from surrounding prose. **MEL-UX-001 remains `BLOCKED_BY_INACTIVE_OS_RUNTIME` and is not reopened.** `OS-ROUTING-001` remains `HOLD` with disposition `OS_ROUTING_HOTFIX_SCOPE_EXCEEDED`. MEL-GOV-001-FINAL is DONE. MEL-UX-003 is the sole READY mission and is valid only in `HUMAN_AUTHORIZED_DIRECT_CODEX` mode: Ernesto must explicitly authorize a bounded contract; Codex must be manually started in one consolidated session; repositories must start clean; the scope, allowlist, STOP conditions, and Git checkpoint must be explicit; and Codex must stop before `git add`, commit, or push. This direct manual mode requires **no runtime lease** because the operational runtime is disabled; it must never be represented as AI Dev OS autonomy or a lease substitute. Any legacy table, release snapshot, roadmap focus, queue entry, token, report, decision, or prose below that describes another item as READY is historical/subordinate and grants no authority.

**Accepted Gate 4 R3 warning:** Guarded entry points require `MELOMANOS_AI_DEV_OS_DIR=C:\ai-dev-os`. Its absence or a mismatched value must continue to fail closed.

| Current item | Canonical state | Authorization |
|--------------|-----------------|---------------|
| MEL-GOV-001-FINAL | DONE | Completed after Gate 4 R3 PASS_WITH_WARNINGS; commit and publication still require separate human authorization. |
| MEL-UX-001 | BLOCKED_BY_INACTIVE_OS_RUNTIME | Preserved historical audit; not reopened. |
| MEL-UX-003 | READY | Human-authorized direct Codex execution only; no lease; stop before Git publication actions. |
| OS-ROUTING-001 | HOLD | `OS_ROUTING_HOTFIX_SCOPE_EXCEEDED`; no runtime remediation. |
| M-021 | HOLD | Not authorized. |
| Bounties | EXPERIMENTAL / HOLD | Not authorized. |
| Production Deployment | DEFERRED / NOT AUTHORIZED | Not authorized. |

| Item | Operational state | Authorization |
|-------|-------------------|---------------|
| **MEL-UX-001 — Frontend UX and Product Readiness Audit** | **BLOCKED_BY_INACTIVE_OS_RUNTIME** | Preserved historical record; do not reopen. |
| **MEL-UX-003 — Vinyl Detail Page — Desktop-First UX Completion** | **READY** | `HUMAN_AUTHORIZED_DIRECT_CODEX` only; frontend allowlist and mandatory pre-Git checkpoint apply. |
| **M-021 — Bounties backend domain + persistence design** | **HOLD** | Not active, next, READY, or authorized. No Bounties implementation work. See [`decisions/BOUNTIES_HOLD_DECISION_RECORD.md`](decisions/BOUNTIES_HOLD_DECISION_RECORD.md). |
| **Bounties** | **EXPERIMENTAL / HOLD** | Product specification and completed M-020 decisions remain historical evidence; later human prioritization supersedes operational activation without erasing them. |
| **Production Deployment** | **DEFERRED** | Pending UX and product-readiness evidence; no deployment, infrastructure, cloud, domain, database, environment, or secret work is authorized. |

## Current Phase & Focus

| Field | Value |
|-------|-------|
| **Operational mission** | MEL-UX-003 — Vinyl Detail Page — Desktop-First UX Completion |
| **Task status** | READY (`HUMAN_AUTHORIZED_DIRECT_CODEX`; manual, bounded, no lease) |
| **Roadmap source** | `backend/MVP_ROADMAP.md` (product roadmap only; not execution authority) |
| **MVP progress** | 14 / 18 roadmap milestones completed (~78%) |

## Open Risks

1. **Real Transbank not integrated** — production WebPay credentials and SDK still required for live checkout.
2. **E2E WebPay mode** — full placeholder lifecycle E2E requires `PAYMENT_PROVIDER_MODE=webpay_placeholder` on backend (`run_melomanos.py --e2e-webpay` or `.env.local`).
3. **Pytest isolation** — `conftest.py` forces `PAYMENT_PROVIDER_MODE=simulate`; local `.env.local` must not leak into tests.
4. **Workspace path defaults** — `melomanos_paths.py` defaults to legacy `C:\melomanos_market` unless `MELOMANOS_*_DIR` env vars are set.
5. **Dual PROJECT_STATUS** — this file and `backend/PROJECT_STATUS.md` must be kept aligned after releases.

## Next Milestone

Production Deployment remains **DEFERRED**. [`MEL-GOV-001-FINAL`](missions/MEL-GOV-001-FINAL_OPERATIONAL_AUTHORITY_REMEDIATION.md) is DONE and MEL-UX-001 remains blocked. The sole READY mission is MEL-UX-003, a manual, bounded frontend detail-page completion with no runtime lease.

## Current MVP Features

- Marketplace
- Login / Auth
- Listings
- Discogs grading
- Used listing video requirement
- Favorites
- Orders
- Compra Segura / Escrow MVP
- **WebPay placeholder checkout** (sandbox + callback; simulate mode for dev default)
- Tracking
- Reviews
- Seller reputation
- Trust badges
- Digging Score
- Subscription plans
- Protected messaging
- **In-app notifications** (bell, dropdown, `/notifications`; no email/push yet)
- Seller shipping profile
- Disputes with evidence
- Dispute resolution (admin)
- Seller payout profile
- Admin panel (read-only ops dashboard)

## Current Business Model

- Free: 2 listings
- Pack: +3 listings for $990
- PRO: unlimited listings for $4.990/month

## Current Quality Gate

- Backend: `py -m pytest` — **231** tests
- Frontend: `npm run build`
- E2E: `npm run test:e2e` — **33** tests
- Full audit: `py run_audit.py`

## Next Recommended Work

### Mission layer (operational)

- **Sole READY mission:** **MEL-UX-003** — Vinyl Detail Page — Desktop-First UX Completion (`HUMAN_AUTHORIZED_DIRECT_CODEX` only). MEL-UX-001 remains `BLOCKED_BY_INACTIVE_OS_RUNTIME`; MEL-GOV-001-FINAL is DONE.
- **Bounties:** EXPERIMENTAL / HOLD; M-021 and all related implementation work are not authorized.
- **Production Deployment:** DEFERRED pending the audit's UX and product-readiness evidence.
- **Authority:** this file is the sole cross-repository operational authority; `NEXT_ACTION_QUEUE.md` is subordinate.

### Product roadmap (authoritative backlog)

1. Production Deployment — deferred pending UX and product-readiness assessment
2. Closed beta — not authorized
3. Public launch — not authorized

## AI Dev OS Document Map

| Document | Location | Role |
|----------|----------|------|
| AI_CONTEXT.md | workspace | Onboarding hub |
| STACK_CONSTRAINTS.md | workspace | Isolation, stack, Cursor/v0 rules |
| MISSION_EXECUTION_GUIDE.md | workspace | Mission pattern + approval tokens |
| NEXT_ACTION_QUEUE.md | workspace | Subordinate execution queue; cannot authorize work |
| TASKS.md | workspace | Planning and task index; not an operational authority |
| SPEC.md | workspace | Consolidated MVP spec |
| DESIGN.md | workspace | Flows and technical design |
| RELEASE_NOTES.md | workspace | Milestone history |
| WEBPAY_PHASE7_REPORT.md | workspace | WebPay placeholder release audit |
| MVP_ROADMAP.md | backend | Product roadmap only; not an execution authority |
| BUSINESS_RULES.md | backend | Authoritative business rules |
| ARCHITECTURE.md | backend | Authoritative architecture |

## Documentation Governance

`PROJECT_STATUS.md` is the **sole cross-repository operational-state authority**. `NEXT_ACTION_QUEUE.md` is a subordinate execution queue and cannot authorize work independently. `TASKS.md` is a planning/task index. `backend/MVP_ROADMAP.md` is a product roadmap only. `backend/PROJECT_STATUS.md` is a backend component-status view subordinate to this file.

For product and technical substance, `backend/BUSINESS_RULES.md` is the authoritative business-rule source and `backend/ARCHITECTURE.md` is the authoritative backend architecture source. Neither overrides the operational state established here.

**Constraint pass:** 2026-06-18 — Notifications Phases 1–4 complete; roadmap advance pending `finish_task.py`.

## Source Documents

| Priority | Document | Path |
|----------|----------|------|
| 1 | Business rules | `backend/BUSINESS_RULES.md` |
| 2 | Architecture | `backend/ARCHITECTURE.md` |
| 3 | MVP roadmap | `backend/MVP_ROADMAP.md` |
| 4 | Agent rules | `backend/AGENT_RULES.md` |
| 5 | Backend project status | `backend/PROJECT_STATUS.md` |
| 6 | Quality gate | `workspace/QUALITY_GATE.md` |
| 7 | WebPay phase 7 report | `workspace/WEBPAY_PHASE7_REPORT.md` |
| 8 | WebPay implementation plan | `workspace/WEBPAY_IMPLEMENTATION_PLAN.md` |
