#!/usr/bin/env python3
"""Check a customized Laravel preview workflow for required static guardrails."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_PATTERNS = {
    "manual workflow_dispatch trigger": r"(?m)^\s*workflow_dispatch\s*:",
    "read-only repository permission": r"(?ms)^permissions:\s*\n\s*contents:\s*read\s*$",
    "bounded job timeout": r"(?m)^\s*timeout-minutes\s*:\s*\d+\s*$",
    "concurrency cancellation": r"(?ms)^concurrency:.*?cancel-in-progress:\s*true",
    "immutable requested checkout": r"(?ms)uses:\s*actions/checkout@.*?ref:\s*\$\{\{\s*inputs\.ref\s*\}\}",
    "checkout credentials disabled": r"persist-credentials:\s*false",
    "debug disabled": r"APP_DEBUG:\s*[\"']?false",
    "safe mail driver": r"MAIL_MAILER:\s*log",
    "safe queue driver": r"QUEUE_CONNECTION:\s*sync",
    "fresh application key": r"php artisan key:generate",
    "forced disposable migration": r"php artisan migrate:fresh --force",
    "local origin health check": r"curl[^\n]+127\.0\.0\.1",
    "temporary Cloudflare tunnel": r"cloudflared tunnel --url",
    "HTTPS origin update": r"ASSET_URL.*PREVIEW_URL|PREVIEW_URL.*ASSET_URL",
    "public HTTPS verification": r"(?s)curl.{0,300}PREVIEW_URL",
    "mixed-content check": r"[Mm]ixed-content|http://",
    "bounded keepalive": r"sleep[^\n]+LIFETIME_MINUTES",
    "unconditional cleanup": r"(?s)if:\s*\$\{\{\s*always\(\)\s*\}\}.{0,500}rm -f \.env",
}

FORBIDDEN_PATTERNS = {
    "automatic pull_request execution": r"(?m)^\s*pull_request(?:_target)?\s*:",
    "write-all permission": r"(?m)^\s*permissions\s*:\s*write-all\s*$",
    "production environment": r"APP_ENV:\s*[\"']?production",
    "enabled debug mode": r"APP_DEBUG:\s*[\"']?true",
    "production database hint": r"(?i)(DB_DATABASE|database)\s*[:=]\s*[\"']?production\b",
    "unbounded latest cloudflared download": r"cloudflared/releases/latest/download",
    "ignored Composer platform requirements": r"composer install[^\n]*--ignore-platform-req",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", help="Customized GitHub Actions YAML file")
    args = parser.parse_args()
    path = Path(args.workflow).expanduser().resolve()
    if not path.is_file():
        parser.error(f"not a file: {path}")
    text = path.read_text(encoding="utf-8", errors="replace")

    errors: list[str] = []
    for label, pattern in REQUIRED_PATTERNS.items():
        if not re.search(pattern, text):
            errors.append(f"missing: {label}")
    for label, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, text):
            errors.append(f"unsafe: {label}")

    if errors:
        print(f"FAIL: {path}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {path}")
    print(f"Checked {len(REQUIRED_PATTERNS)} required and {len(FORBIDDEN_PATTERNS)} forbidden patterns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
