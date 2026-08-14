# Laravel Preview Environment Skill

A reusable AI agent skill for creating isolated, temporary Laravel preview environments for branches and pull requests.

The goal is simple:

> Preview any Laravel application in a real running environment before merging, without touching staging or production.

This skill creates a disposable preview stack with:

- GitHub Actions runner
- PHP version detected from the project requirements
- Composer dependencies
- MySQL database
- Laravel migrations and seeders
- Vite production assets
- Cloudflare HTTPS tunnel
- Filament/admin panel verification
- Mixed-content and asset loading checks

## Why this exists

Laravel teams often need to answer:

- "Can I see this PR running?"
- "Can I review this Filament panel before merging?"
- "Does this branch actually boot from a clean environment?"
- "Can QA test this feature without deploying it?"

A temporary preview environment solves this without maintaining expensive staging infrastructure for every branch.

## What it does

The skill workflow:

1. Creates an isolated preview branch/environment.
2. Installs project dependencies using the existing lock files.
3. Detects and uses the required PHP runtime.
4. Starts a disposable MySQL database.
5. Runs Laravel migrations and seeders.
6. Builds frontend assets using Vite.
7. Starts Laravel locally.
8. Creates a temporary HTTPS URL using Cloudflare Tunnel.
9. Configures Laravel for the external HTTPS hostname.
10. Verifies CSS, JavaScript, images, and admin panels load correctly.
11. Provides a temporary login and preview URL.

## Supported use cases

Works well for:

- Laravel applications
- Laravel + Filament admin panels
- Laravel + Livewire applications
- Laravel + Vite frontend builds
- Pull request reviews
- Internal QA previews
- Client demos

## Important safety rules

This skill intentionally uses disposable infrastructure.

It should never:

- use production databases
- expose production credentials
- copy production `.env` files
- send real emails
- run production payment integrations
- expose debug mode publicly

Preview environments should use:

```env
APP_DEBUG=false
DEBUGBAR_ENABLED=false
MAIL_MAILER=log
QUEUE_CONNECTION=sync
```

## Common problems handled

### Mixed content errors

A common issue with temporary HTTPS tunnels is Laravel generating:

```
http://preview-url/css/app.css
```

inside an HTTPS page.

The skill handles this by configuring:

```env
APP_URL=https://preview-url
ASSET_URL=https://preview-url
```

and clearing Laravel caches after the tunnel hostname is known.

### SQLite migration failures

Many Laravel projects are designed for MySQL.

This skill prefers using MySQL instead of forcing migrations to support SQLite.

### Composer PHP version mismatches

The PHP runtime is selected based on the project's requirements instead of blindly using the runner default.

## Example usage

Ask your AI agent:

```
Preview this Laravel PR and give me an admin URL.
```

or:

```
Run the staging branch in a temporary preview environment.
```

The agent should return:

- preview URL
- login credentials
- source branch/commit
- verification results
- expiration information

## Limitations

This is intended for temporary previews, not production hosting.

Typical GitHub Actions + Cloudflare Quick Tunnel previews last only while the runner is alive.

For permanent staging environments use:

- dedicated VPS
- managed preview platforms
- Kubernetes environments
- Laravel Forge/Ploi/etc.

## Installation

Upload this skill to your AI agent's skill directory or use it through a compatible Skills system.

Repository:

https://github.com/pratikkuikel/laravel-preview-environment-skill

## License

MIT License
