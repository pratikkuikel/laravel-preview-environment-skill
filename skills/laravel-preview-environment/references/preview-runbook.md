# Laravel preview runbook

Use this runbook as the operational contract for every preview. Adapt commands to the repository; preserve the gates.

## 1. Scope and isolation

Record before provisioning:

- repository and exact branch, pull request, tag, or SHA;
- route and user journey to demonstrate;
- local machine, sandbox, self-hosted runner, or GitHub-hosted runner;
- expected lifetime and the person who can stop it;
- public anonymous URL or access-controlled URL;
- synthetic accounts and fixtures needed for the journey.

Use a separate clone, worktree, container, sandbox, or ephemeral runner for both inspection and execution. Check out the resolved SHA directly and record `git rev-parse HEAD` before reading project files; a clean current checkout may still be on the wrong branch. Do not commit generated preview configuration to the reviewed branch unless the user explicitly asked to add a reusable workflow.

## 2. Project inspection

Run the bundled inspector, then verify its evidence. Inspect at least:

- `composer.json` and `composer.lock` for PHP, Laravel, extension, and script requirements;
- JS lock files and `package.json` for the package manager, Node constraints, and build script;
- `.env.example`, `config/database.php`, migrations, and CI for database, Redis, search, object storage, and queue dependencies;
- application boot code, trusted-proxy configuration, route files, panel providers, and auth guards;
- seeders and factories for real addresses, production identifiers, outbound calls, or copied data;
- scheduled jobs, queue workers, webhooks, payment clients, analytics, error reporting, and mail transports.

Choose the runtime from repository evidence. Install dependencies from lock files. Add only extensions and services the application requires.

## 3. Safe preview configuration

Use a fresh `APP_KEY` and an empty disposable database. Prefer these preview defaults unless the application requires another safe local driver:

```env
APP_ENV=preview
APP_DEBUG=false
LOG_CHANNEL=stderr
MAIL_MAILER=log
QUEUE_CONNECTION=sync
CACHE_STORE=file
SESSION_DRIVER=file
TELESCOPE_ENABLED=false
DEBUGBAR_ENABLED=false
HORIZON_PREFIX=preview_
```

Also replace or disable SMS, payment, webhook, cloud-storage, search, analytics, exception-reporting, OAuth, and third-party credentials. An unset credential is safer than a production secret, but verify that boot does not require it. Never copy `.env`, database dumps, uploaded files, or caches from production.

Review the seeder before running it. Use synthetic, visibly temporary accounts. A migration passing does not authorize seeding. Use `migrate:fresh --force` only against a database whose disposable identity has been proven from the active runtime configuration.

## 4. Execution choices

### Local or sandbox preview

Prefer this when the user already has an isolated execution environment and can keep its process alive. Start the origin on a loopback or sandbox port, verify it locally, then start the tunnel in a second long-lived process. Preserve process identifiers so teardown is deterministic.

### GitHub Actions preview

Use the bundled asset as a starting point only when the repository is compatible with GitHub-hosted Ubuntu, MySQL, Composer, and a Node build. The workflow is manual, read-only, concurrency-bounded, and time-bounded. It must remain running for the URL to remain live.

Adapt:

- PHP and Node versions;
- PHP extensions and database service;
- package-manager install and build commands;
- migration and reviewed synthetic seeder commands;
- health route and requested feature route;
- storage linking, Filament assets, Octane, Reverb, workers, or other required processes.

Keep `permissions: contents: read`. Do not accept arbitrary shell commands as workflow inputs. Do not use pull-request secrets or execute untrusted fork code with privileged tokens.

## 5. HTTPS and proxy behavior

Cloudflare Quick Tunnels are development-only public URLs. They have no uptime guarantee, limit concurrent in-flight requests, and do not support Server-Sent Events. The URL changes when the tunnel process restarts and disappears when it stops. Quick Tunnels are unsuitable for private data and features that require SSE.

Boot the origin first. Start the tunnel and capture the emitted `https://*.trycloudflare.com` URL. Then set both `APP_URL` and `ASSET_URL` to that URL, clear configuration caches, and restart the Laravel server.

When Laravel still emits HTTP URLs behind TLS termination, inspect forwarded headers and configure trusted proxies for the isolated preview. Make the smallest preview-only change possible. Do not weaken production proxy trust globally just to make a temporary preview work.

For a confidential or stable preview, use a named Cloudflare Tunnel with Cloudflare Access or another authenticated preview provider. Treat tunnel tokens as secrets and remove any created tunnel, hostname, access policy, and DNS record during teardown.

## 6. Verification gate

Collect evidence for every applicable gate:

1. **Identity:** checked-out SHA equals the requested SHA; the preview shows a build identifier when feasible.
2. **Install:** Composer and frontend installs came from lock files without ignored platform requirements.
3. **Database:** the active runtime points to the disposable database; migrations pass; seed counts and synthetic credentials are known.
4. **Origin:** the local health route responds before tunneling; logs contain no boot exception.
5. **HTTPS:** the public route responds over HTTPS after configuration restart; generated canonical, asset, redirect, and form URLs use HTTPS.
6. **Assets:** built manifests exist; CSS, JS, fonts, and images return successful responses with correct content types; the browser reports no mixed content.
7. **Framework:** Livewire, Inertia, Filament, CSRF, sessions, login, logout, uploads, and websockets/SSE are tested when relevant. Quick Tunnel's SSE limitation must be disclosed.
8. **Feature:** perform the requested user journey with synthetic data and verify its persisted result.
9. **Safety:** debug pages are off; outbound email, queues, schedules, webhooks, payments, telemetry, and production integrations are blocked or redirected.
10. **Lifetime:** the stop mechanism and automatic expiry are proven.

Use a real browser when available for visual and network checks. If browser access is unavailable, state that limitation and do not claim browser, mixed-content, or interaction verification from `curl` alone.

## 7. Handoff

Provide:

- public URL and exact starting route;
- source branch or pull request and resolved SHA;
- synthetic credentials, shared through an appropriate private channel when needed;
- checks passed and checks not run;
- known limitations, including public access and Quick Tunnel constraints;
- creation time, expiry time, and exact stop/cancel mechanism;
- warning: temporary preview; do not enter real or sensitive data.

## 8. Teardown

Cancel the job or stop the tunnel, application server, queue workers, websocket servers, and schedulers. Use an unconditional cleanup/finally step in CI. Remove disposable databases, containers, temporary files containing credentials, uploaded synthetic files, named tunnels, DNS records, and access policies created for the preview. Confirm the old URL no longer serves the application. Preserve only sanitized logs needed for debugging.

## Primary references

- Cloudflare Quick Tunnels: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/
- Laravel trusted proxies: https://laravel.com/docs/requests#configuring-trusted-proxies
- GitHub Actions service containers: https://docs.github.com/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers
