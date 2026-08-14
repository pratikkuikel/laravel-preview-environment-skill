# Laravel Preview Environment Skill

A cross-agent skill for launching disposable Laravel preview environments.

Supports Codex, Claude, ChatGPT Skills, and other agent workflows.

## Features

- GitHub Actions based previews
- MySQL disposable database
- Composer/PHP version detection
- Vite production builds
- Filament verification
- HTTPS tunnel previews
- APP_URL / ASSET_URL handling
- Mixed content checks
- Safe temporary credentials

## Import into ChatGPT

Download:

```
releases/laravel-preview-environment-skill.zip
```

Import the ZIP file as a ChatGPT Skill.

The package contains:

```
skills/
└── laravel-preview-environment/
    └── SKILL.md
```

## Example prompts

```
Preview this Laravel PR and give me a temporary admin URL.
```

```
Run this branch in an isolated Laravel preview environment.
```

## What the skill does

1. Inspects the Laravel project.
2. Detects PHP, Composer, database, and frontend requirements.
3. Creates an isolated preview environment.
4. Runs migrations and seeders.
5. Builds frontend assets.
6. Exposes the app through HTTPS.
7. Verifies assets and browser compatibility before handoff.

## Safety

Never expose:

- production databases
- production secrets
- customer data
- payment credentials

Use disposable preview infrastructure only.

## Compatible projects

Works especially well with:

- Laravel
- FilamentPHP
- Livewire
- Vite
- MySQL
