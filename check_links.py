#!/usr/bin/env python3
"""Verify that relative links in Markdown files point to files or directories that exist.

External links (http/https/mailto) and pure in-page anchors are ignored: this check
must work offline and deterministically. Links inside fenced code blocks are skipped.
Exit status is 1 if any broken link is found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]]*\]\(([^)\s]+)\)")
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", ".pytest_cache", ".ruff_cache"}
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:")


def markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if not SKIP_DIRS.intersection(p.parts))


def broken_links(md_file: Path) -> list[tuple[int, str]]:
    problems: list[tuple[int, str]] = []
    in_fence = False
    for line_no, line in enumerate(md_file.read_text(encoding="utf-8").splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LINK_RE.finditer(line):
            target = match.group(1) or match.group(2)
            if target.startswith(EXTERNAL_PREFIXES) or target.startswith("#"):
                continue
            path_part = unquote(target.split("#", 1)[0])
            if not path_part:
                continue
            resolved = (md_file.parent / path_part).resolve()
            if not resolved.exists():
                problems.append((line_no, target))
    return problems


def main() -> int:
    failures = 0
    files = markdown_files(ROOT)
    for md_file in files:
        for line_no, target in broken_links(md_file):
            print(f"{md_file.relative_to(ROOT)}:{line_no}: broken link -> {target}")
            failures += 1
    print(f"Checked {len(files)} Markdown files; {failures} broken link(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
