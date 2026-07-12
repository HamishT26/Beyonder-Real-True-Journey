#!/usr/bin/env python3
"""Scan a public GHC phase for common private-material and raw-ID patterns."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "windows_absolute_path": re.compile(r"\b[A-Za-z]:\\"),
    "raw_uuid_task_or_thread_id": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "chatgpt_conversation_url": re.compile(r"https://chatgpt\.com/c/", re.IGNORECASE),
    "openai_style_secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "github_token": re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private_key_block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"\bBearer\s+[A-Za-z0-9._~-]{20,}", re.IGNORECASE),
}


def scan_phase(repo: Path, phase: Path, excluded: set[Path]) -> dict:
    hits = []
    scanned = 0
    allowed_suffixes = {".json", ".md", ".html", ".tex", ".txt"}
    for path in sorted(phase.rglob("*")):
        resolved = path.resolve()
        if not path.is_file() or path.suffix.lower() not in allowed_suffixes or resolved in excluded:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern_name, pattern in PATTERNS.items():
            if pattern.search(text):
                hits.append(
                    {
                        "file": resolved.relative_to(repo).as_posix(),
                        "pattern": pattern_name,
                    }
                )
    return {
        "schema": "ghc.family.phase-privacy-scan.v1",
        "scope": phase.resolve().relative_to(repo).as_posix(),
        "scanned_file_count": scanned,
        "pattern_classes": sorted(PATTERNS),
        "hit_count": len(hits),
        "hits": hits,
        "valid": not hits and scanned > 0,
        "boundary": (
            "pattern scan for public artifacts; semantic secrets, novel encodings, and "
            "untracked private state still require human review"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir.is_absolute() else repo / args.phase_dir
    excluded = {args.output.resolve()} if args.output else set()
    report = scan_phase(repo, phase, excluded)
    encoded = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
