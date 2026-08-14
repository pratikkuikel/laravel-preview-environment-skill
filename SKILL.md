---
name: laravel-preview-environment
description: Create isolated temporary HTTPS preview environments for Laravel branches and pull requests using GitHub Actions, MySQL, Vite, and Cloudflare tunnels.
---

# Laravel Preview Environment Skill

## Purpose

Create a disposable preview environment for a Laravel branch or pull request so developers can inspect real application behavior without deploying to staging or production.

Useful for:

- Reviewing Laravel pull requests visually
- Testing Filament admin panels
- Sharing unfinished features with stakeholders
- QA before merging
- Previewing feature branches

## Workflow

### 1. Inspect the project

Before creating the preview:

- Detect Laravel version
- Detect PHP requirement from Composer lock
- Inspect `.env.example`
- Detect database requirements
- Detect frontend build system
- Identify admin routes and seed requirements

Never guess the runtime version.

## 2. Create isolated preview infrastructure

The preview must:

- Use a temporary branch
- Never modify the source branch
- Never use production credentials
- Use disposable databases
- Use synthetic data only

Recommended stack:

- GitHub Actions runner
- PHP matching Composer requirements
- MySQL service for MySQL Laravel applications
- Node + Vite build
- Cloudflare Quick Tunnel HTTPS URL

## 3. Laravel setup

Example environment:

```env
APP_ENV=production
APP_DEBUG=false
DEBUGBAR_ENABLED=false

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_DATABASE=preview
DB_USERNAME=root
DB_PASSWORD=root

QUEUE_CONNECTION=sync
CACHE_STORE=file
SESSION_DRIVER=file
MAIL_MAILER=log
```

Generate a fresh key:

```bash
php artisan key:generate
php artisan optimize:clear
```

## 4. Dependencies

Install exactly from lock files:

```bash
composer install --no-interaction --prefer-dist --optimize-autoloader
npm ci
npm run build
```

For Laravel Vite applications verify:

```bash
test -f public/build/manifest.json
```

## 5. Database

Prefer MySQL when the project uses MySQL migrations.

Run:

```bash
php artisan migrate:fresh --seed --force
```

Do not switch to SQLite just for convenience if migrations depend on MySQL behavior.

## 6. Start Laravel

Boot locally first:

```bash
php artisan serve --host=0.0.0.0 --port=8000
```

Verify the application responds before exposing it publicly.

## 7. HTTPS preview tunnel

Expose the local application:

```bash
cloudflared tunnel --url http://127.0.0.1:8000 --no-autoupdate
```

Capture the generated HTTPS URL.

## 8. Fix Laravel HTTPS asset generation

After the tunnel URL exists, configure:

```env
APP_URL=https://preview-url.trycloudflare.com
ASSET_URL=https://preview-url.trycloudflare.com
```

Then:

```bash
php artisan optimize:clear
```

Restart Laravel after changing URL configuration.

## 9. Prevent mixed content issues

Before sharing the URL verify:

- Filament CSS loads
- Filament JS loads
- Vite assets load
- Images load
- Livewire works
- Debugbar is disabled

If assets still generate HTTP URLs, check trusted proxy handling and forwarded HTTPS headers.

Common cause:

Cloudflare receives HTTPS but Laravel sees HTTP internally.

## 10. Final verification checklist

Do not hand off a preview until:

- [ ] Correct branch/SHA is running
- [ ] Composer installation succeeds
- [ ] Correct PHP version is used
- [ ] Database starts successfully
- [ ] Migrations pass
- [ ] Seeders pass
- [ ] Frontend build passes
- [ ] Laravel boots
- [ ] HTTPS tunnel works
- [ ] APP_URL uses HTTPS
- [ ] ASSET_URL uses HTTPS
- [ ] No mixed-content URLs exist
- [ ] CSS and JS load correctly
- [ ] Temporary credentials work

## Security rules

Never:

- expose production databases
- copy production `.env`
- enable debug publicly
- send real emails
- run production queues
- expose API keys
- use customer data

Use disposable preview credentials and synthetic data.

## Lifetime

GitHub Actions runners are temporary.

A preview created this way is suitable for:

- code review
- QA
- demonstrations
- stakeholder approval

It is not a replacement for staging or production hosting.

## Example handoff

```
Laravel preview is live.

URL: https://example.trycloudflare.com/controlpanel

Login:
Email: preview@example.com
Password: temporary-password

Verified:
- Laravel boot
- Database migration
- Seed data
- Vite build
- HTTPS assets
- No mixed content

Source: branch @ commit SHA

Temporary environment. Do not enter production data.
```
