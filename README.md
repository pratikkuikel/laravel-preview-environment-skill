# Laravel Preview Environment Skill

Create disposable HTTPS previews for Laravel branches and pull requests without touching staging or production. The skill inspects the application, adapts a bounded GitHub Actions workflow, provisions synthetic data, builds frontend assets, launches a temporary Cloudflare Quick Tunnel, and verifies the public result before handoff.

The canonical cross-agent skill is `skills/laravel-preview-environment/SKILL.md`. It includes a project inspector, a workflow validator, a safe GitHub Actions starting point, and a detailed preview runbook.

## Agent support

- Codex and ChatGPT: import `laravel-preview-environment-skill.zip`, install the repository as a plugin, or copy `skills/laravel-preview-environment` into `~/.codex/skills/`.
- Claude Code: run `claude --plugin-dir .`, or use the checked-in `.claude/skills/` adapter.
- Gemini CLI: run `gemini extensions link .`; `gemini-extension.json` loads `GEMINI.md`, which imports the canonical skill.
- Other agents: point the agent to `AGENTS.md` or directly to the canonical `SKILL.md`.

## Importable package

Download [`laravel-preview-environment-skill.zip`](https://github.com/pratikkuikel/laravel-preview-environment-skill/releases/download/latest/laravel-preview-environment-skill.zip) and import it as a ChatGPT or Codex skill. Every push to `main` rebuilds and validates this rolling release. The archive contains only the Codex plugin manifest, this README, and the canonical skill with its bundled resources.

## Direct user-level installation

From the repository root:

```bash
mkdir -p ~/.agents/skills ~/.claude/skills
cp -a skills/laravel-preview-environment ~/.agents/skills/
cp -a skills/laravel-preview-environment ~/.claude/skills/
```

## Example prompts

```text
Preview this Laravel PR and give me a temporary verified admin URL.
```

```text
Inspect this Laravel repository and add a safe manual preview workflow.
```

## Important limitation

Cloudflare Quick Tunnel URLs are public, temporary, have no uptime guarantee, and last only while the workflow remains running. Use only disposable credentials and synthetic data. Use a named tunnel protected by Cloudflare Access when the preview must be private.

## Validate a customized workflow

```bash
python3 skills/laravel-preview-environment/scripts/inspect_laravel_project.py /path/to/laravel-project
python3 skills/laravel-preview-environment/scripts/validate_preview_workflow.py /path/to/preview.yml
```
