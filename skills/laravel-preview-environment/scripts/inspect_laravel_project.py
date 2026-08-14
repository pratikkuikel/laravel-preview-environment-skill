#!/usr/bin/env python3
"""Inspect a Laravel repository using only Python's standard library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"Cannot read valid JSON from {path}: {error}") from error
    if not isinstance(value, dict):
        raise SystemExit(f"Expected a JSON object in {path}")
    return value


def env_value(path: Path, key: str) -> str | None:
    if not path.is_file():
        return None
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        found_key, value = line.split("=", 1)
        if found_key.strip() == key:
            return value.strip().strip("'\"") or None
    return None


def package_manager(root: Path) -> tuple[str | None, str | None]:
    candidates = (
        ("pnpm", "pnpm-lock.yaml"),
        ("yarn", "yarn.lock"),
        ("npm", "package-lock.json"),
        ("bun", "bun.lockb"),
        ("bun", "bun.lock"),
    )
    matches = [(manager, lock) for manager, lock in candidates if (root / lock).is_file()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        return "ambiguous", ", ".join(lock for _, lock in matches)
    return None, None


def inspect(root: Path) -> dict[str, Any]:
    composer = load_json(root / "composer.json")
    package = load_json(root / "package.json")
    require = composer.get("require") if isinstance(composer.get("require"), dict) else {}
    require_dev = composer.get("require-dev") if isinstance(composer.get("require-dev"), dict) else {}
    scripts = package.get("scripts") if isinstance(package.get("scripts"), dict) else {}
    manager, lock_file = package_manager(root)
    all_php_packages = {**require, **require_dev}
    env_example = root / ".env.example"

    js_packages: dict[str, Any] = {}
    for section in ("dependencies", "devDependencies"):
        values = package.get(section)
        if isinstance(values, dict):
            js_packages.update(values)

    markers = {
        "filament": any(name.startswith("filament/") for name in all_php_packages),
        "livewire": "livewire/livewire" in all_php_packages,
        "inertia": "inertiajs/inertia-laravel" in all_php_packages,
        "octane": "laravel/octane" in all_php_packages,
        "reverb": "laravel/reverb" in all_php_packages,
        "horizon": "laravel/horizon" in all_php_packages,
        "telescope": "laravel/telescope" in all_php_packages,
        "vite": any(name in js_packages for name in ("vite", "laravel-vite-plugin")),
    }

    return {
        "root": str(root),
        "is_laravel": "laravel/framework" in require and (root / "artisan").is_file(),
        "laravel_constraint": require.get("laravel/framework"),
        "php_constraint": require.get("php"),
        "composer_lock": (root / "composer.lock").is_file(),
        "php_extensions": sorted(name.removeprefix("ext-") for name in require if name.startswith("ext-")),
        "package_manager": manager,
        "frontend_lock": lock_file,
        "node_constraint": package.get("engines", {}).get("node")
        if isinstance(package.get("engines"), dict)
        else None,
        "build_script": scripts.get("build"),
        "database_connection": env_value(env_example, "DB_CONNECTION"),
        "queue_connection": env_value(env_example, "QUEUE_CONNECTION"),
        "cache_store": env_value(env_example, "CACHE_STORE") or env_value(env_example, "CACHE_DRIVER"),
        "session_driver": env_value(env_example, "SESSION_DRIVER"),
        "features": markers,
        "paths": {
            "env_example": env_example.is_file(),
            "migrations": (root / "database/migrations").is_dir(),
            "seeders": (root / "database/seeders").is_dir(),
            "routes": sorted(path.name for path in (root / "routes").glob("*.php"))
            if (root / "routes").is_dir()
            else [],
            "github_workflows": sorted(path.name for path in (root / ".github/workflows").glob("*.y*ml"))
            if (root / ".github/workflows").is_dir()
            else [],
        },
        "review_required": [
            "Verify the resolved PHP and Node versions against lock files and CI.",
            "Inspect migrations and runtime configuration before selecting database services.",
            "Inspect seeders and outbound integrations before running or exposing the app.",
            "Identify the requested health route and feature journey before adapting a workflow.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", help="Laravel repository root")
    args = parser.parse_args()
    root = Path(args.repository).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    report = inspect(root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["is_laravel"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
