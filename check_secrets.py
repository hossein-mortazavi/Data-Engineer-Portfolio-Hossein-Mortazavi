#!/usr/bin/env python3
"""Lightweight, offline scan for committed secrets.

This is a safety net, not a replacement for a dedicated scanner: it catches the most
common accidental leaks (private keys, cloud access keys, hard-coded passwords/tokens).
Placeholders such as ``change-me`` or ``${VAR}`` are ignored. Exit status is 1 on a hit.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", ".terraform", "__pycache__"}
SKIP_FILES = {"scripts/check_secrets.py", "package-lock.json"}
PLACEHOLDER_HINTS = ("change", "example", "your", "<", "${", "xxx", "placeholder", "dummy", "***")

PATTERNS: dict[str, re.Pattern[str]] = {
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "AWS access key id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Azure storage account key": re.compile(r"AccountKey=[A-Za-z0-9+/]{40,}={0,2}"),
    "hard-coded credential": re.compile(
        r"(?i)\b(password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]([^'\"\s]{8,})['\"]"
    ),
}


def is_placeholder(text: str) -> bool:
    lowered = text.lower()
    return any(hint in lowered for hint in PLACEHOLDER_HINTS)


def scan_file(path: Path) -> list[tuple[int, str]]:
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(content.splitlines(), start=1):
        for label, pattern in PATTERNS.items():
            match = pattern.search(line)
            if not match:
                continue
            if label == "hard-coded credential" and is_placeholder(match.group(2)):
                continue
            hits.append((line_no, label))
    return hits


def main() -> int:
    findings = 0
    scanned = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or SKIP_DIRS.intersection(path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES:
            continue
        scanned += 1
        for line_no, label in scan_file(path):
            print(f"{rel}:{line_no}: possible {label}")
            findings += 1
    print(f"Scanned {scanned} files; {findings} possible secret(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
