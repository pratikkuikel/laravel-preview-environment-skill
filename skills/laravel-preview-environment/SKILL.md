---
name: laravel-preview-environment
description: Create isolated temporary HTTPS preview environments for Laravel branches and pull requests using GitHub Actions, MySQL, Vite and Cloudflare tunnels.
---

# Laravel Preview Environment

## Purpose

Launch a disposable preview environment for a Laravel branch or pull request without touching production or the source branch.

## Workflow

1. Inspect the repository
- Detect Laravel version.
- Detect required PHP version from composer.lock.
- Detect database requirements.
- Detect frontend build tooling.

2. Create an isolated preview environment
- Use a temporary branch/workflow.
- Never modify the reviewed branch.
- Use disposable credentials and databases.

3. Provision runtime
- Install Composer dependencies.
- Install Node dependencies.
- Use the correct PHP version.
- Prefer MySQL for MySQL-based Laravel projects.

4. Configure Laravel
- Generate application key.
- Disable debug tooling.
- Configure safe preview mail/queue/cache settings.
- Run migrations and seeders.

5. Build frontend

```bash
npm ci
npm run build
```

Verify production assets exist before publishing.

6. Expose HTTPS preview

Use Cloudflare Quick Tunnel or equivalent temporary HTTPS tunnel.

7. Verify before handoff

Required checks:

- Application boots.
- Database migrations pass.
- Seed data works.
- Vite assets exist.
- Filament assets load.
- No mixed-content HTTP URLs.
- Debugbar is disabled.

## Laravel HTTPS rules

Temporary tunnels terminate HTTPS before Laravel receives the request. Always verify:

- APP_URL
- ASSET_URL
- trusted proxy handling
- forwarded HTTPS headers

Do not hand over a preview URL until browser assets load correctly.

## Security

Never expose:

- production database
- production secrets
- production API keys
- real customer data

Use disposable environments only.

## Output

Provide:

- Preview URL
- Login credentials if created
- Source commit/branch
- Verification results
- Lifetime limitations
