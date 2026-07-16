# MEL-UX-001 — Frontend UX and Product Readiness Audit

**Mission type:** Read-only frontend UX and product-readiness audit
**Operational status:** **READY** — sole READY mission, per [`PROJECT_STATUS.md`](../PROJECT_STATUS.md)
**Authority:** [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) is the sole cross-repository operational-state authority.

## Execution authorization boundary

This governance package makes MEL-UX-001 persistently `READY`; it does **not** execute MEL-UX-001. Execution requires both a separate human execution authorization and a valid matching runtime lease issued after publication. Once those gates are present, executing MEL-UX-001 produces the audit report described below. The audit itself does not authorize implementation, deployment, another mission, product tests or builds, servers, screenshots, browser automation, or network access.

## Objective

Produce a bounded, evidence-based audit of the implemented frontend and its readiness against documented Melómanos product intent. The audit is read-only: it identifies prioritized findings and does not change the product.

## Required inspection scope

1. Discover and verify the frontend root without changing it.
2. Review desktop and mobile UX, navigation, information architecture, and visual consistency.
3. Review marketplace trust signals, listing discovery, and vinyl-detail flows.
4. Inspect empty, loading, error, and authenticated states where existing source or documentation permits read-only assessment.
5. Assess accessibility and responsive behavior from existing source, styles, and documentation.
6. Compare implemented UI with documented product intent, including relevant workspace product documents and authoritative backend business rules.

## Local zero-cost inspection route

Use local, read-only inspection only: repository structure, tracked source, existing documentation, existing reports, and Git status/log inspection. Do not use network access, cloud services, paid tools, APIs, or OpenAI API usage.

## Explicit prohibitions

- No code, documentation, configuration, dependency, lockfile, environment, or test changes.
- No builds, tests, development servers, Playwright execution, screenshots, or browser automation until separately authorized.
- No deployment or infrastructure, cloud, domain, database, environment, secret, or release work.
- No paid tools or APIs.

## Expected audit report

Create an audit report only after separate human execution authorization and a valid matching runtime lease are present. It must contain:

1. Evidence inventory: inspected roots, documents, routes/components, and limitations.
2. Product-intent comparison: implemented behavior versus documented intent, with citations/paths.
3. Findings grouped by navigation/IA, visual consistency, trust, discovery/detail flows, state coverage, accessibility, and responsive behavior.
4. Prioritized findings (`P0`, `P1`, `P2`) with user impact, evidence, affected surface, and a bounded recommended follow-up type.
5. Readiness assessment, unresolved questions, and explicit non-findings where evidence was insufficient.
6. A recommendation that does not authorize implementation, deployment, or any follow-up mission.

## Stop conditions

Stop and report the blocker without expanding scope if any of the following occurs:

- frontend root or required product context cannot be verified;
- required access would expose or require secrets;
- any workspace, backend, or frontend worktree is dirty and ownership/context is unclear;
- product authority is conflicting or unclear;
- the audit would require a build, test, server, screenshot, browser automation, network access, or code change.

## Completion boundary

This brief records a persistently READY audit boundary only. It does **not** execute the audit, authorize any implementation, deployment, another mission, product test/build, server, screenshot, browser automation, network activity, or reactivate Production Deployment.
