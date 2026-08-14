---
name: laravel-preview-environment
description: Create isolated, temporary HTTPS preview environments for Laravel branches and pull requests. Use when previewing a Laravel, Filament, Livewire, Inertia, or Vite change; adding or repairing a GitHub Actions preview workflow; exposing a disposable local or CI runtime through a Cloudflare tunnel; or verifying preview boot, migrations, assets, HTTPS, authentication, and teardown before sharing a URL.
---

# Laravel Preview Environment

Launch a bounded preview from an exact branch or commit without modifying it. Keep production systems outside the preview boundary.

Resolve every bundled resource path relative to this `SKILL.md`, regardless of the current working directory.

## Workflow

1. Establish scope. Record the repository, exact ref and resolved SHA, required preview route, expected user journey, lifetime, and whether a public URL is acceptable. Treat a Quick Tunnel as public internet exposure.
2. Create a separate read-only inspection checkout at the resolved SHA, without switching or modifying the user's current checkout. Run `scripts/inspect_laravel_project.py <inspection-checkout>` and verify its findings against `composer.json`, lock files, `.env.example`, migrations, build scripts, route definitions, and CI configuration. Detect runtime and extensions; never default blindly to the newest PHP or Node release.
3. Read [references/preview-runbook.md](references/preview-runbook.md) completely. Select local or CI execution, the database engine required by the application, safe synthetic seed strategy, and public Quick Tunnel or access-controlled named tunnel.
4. Create the preview outside the reviewed checkout, or add a workflow in a separate authorized change. Prove the runtime checkout still matches the resolved SHA. Keep the source branch and production services immutable.
5. Copy `assets/github-actions-preview.yml` only for a compatible GitHub-hosted Ubuntu, MySQL, Composer, and Node/Vite application. Adapt every project-specific command and validate it with `scripts/validate_preview_workflow.py <workflow>`.
6. Provision only disposable services. Build from lock files, generate a fresh application key, use log/sync/file drivers, block outbound side effects, migrate an empty preview database, and seed synthetic accounts only when the seeder has been inspected.
7. Boot locally and pass an origin health check before starting the tunnel. After receiving the HTTPS URL, set `APP_URL` and `ASSET_URL`, clear cached configuration, and restart the server so generated URLs use the public origin.
8. Complete the verification gate in the runbook. Inspect the actual page and network behavior when browser tooling is available; a successful process exit or HTTP status alone is insufficient.
9. Hand off the exact URL, route, synthetic credentials, SHA, verification evidence, known limitations, expiry time, stop mechanism, and explicit warning against entering real data.
10. Stop or cancel the preview at expiry. Confirm the runner, tunnel, server, database, artifacts containing credentials, and any named tunnel or DNS records are gone.

## Decision gates

- Pause before exposure when the data is not demonstrably synthetic, the seeder may call external systems, the application cannot suppress email/queue/payment/webhook side effects, or the user has not authorized a public URL.
- Use a named tunnel protected by access control when confidentiality matters. Quick Tunnels provide a random hostname, not authentication.
- Match MySQL/PostgreSQL/Redis/search/storage services to the migrations and runtime. SQLite is acceptable only when the application already supports it and parity is not material to the requested review.
- Treat migrations, frontend builds, browser assets, Livewire/Inertia interactions, login, and the requested feature journey as separate checks.

## Completion contract

Deliver a preview only when the exact SHA is proven, the verification gate passes, exposure is bounded, and teardown is defined. Otherwise report the failed gate and retain logs without presenting the preview as ready.

## Bundled resources

- `assets/github-actions-preview.yml`: adaptable, bounded GitHub Actions starting point.
- `references/preview-runbook.md`: runtime, security, verification, handoff, and teardown requirements.
- `scripts/inspect_laravel_project.py`: dependency-free project capability report.
- `scripts/validate_preview_workflow.py`: dependency-free static guardrail check for a customized workflow.
