#!/usr/bin/env python3
"""Validate a persistent baton and its compact sanitized delivery pointer."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file|vscode)://"),
    "delegation_markup": re.compile(r"(?i)<\s*codex_delegation\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret)\s*[:=]\s*[^\s,}\]]+"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baton", type=Path)
    parser.add_argument("pointer", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    baton = args.baton.read_text(encoding="utf-8")
    pointer = args.pointer.read_text(encoding="utf-8")
    baton_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
    pointer_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", pointer))
    hits = []
    for label, pattern in PATTERNS.items():
        for surface, text in (("baton", baton), ("pointer", pointer)):
            if pattern.search(text):
                hits.append({"surface": surface, "class": label})
    checks = {
        "baton_word_range": 10000 <= baton_words <= 100000,
        "pointer_compact": pointer_words <= 350,
        "pointer_names_ilyra": "Ilyra Fen" in pointer,
        "pointer_names_v651_v8": "v651-v8" in pointer,
        "no_private_hits": not hits,
    }
    payload = {
        "schema": "ghc.family.baton-pointer-guard.receipt.v1",
        "valid": all(checks.values()),
        "checks": checks,
        "baton_words": baton_words,
        "pointer_words": pointer_words,
        "privacy_hits": hits,
        "boundary": "A valid file and pointer are PREPARED_NOT_SENT until the existing-task message tool acknowledges one delivery.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": payload["valid"], "baton_words": baton_words, "pointer_words": pointer_words, "hits": len(hits)}))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
