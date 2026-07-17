#!/usr/bin/env python3
"""Review the staged Ilyra v647-v6 x1-only surface and emit Git-blob evidence."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"
MANIFEST = "docs/ilyra-fen/v647-v6/validation/x1-staged-manifest.json"
REVIEW = "docs/ilyra-fen/v647-v6/validation/x1-staged-review.json"
SELF_EXCLUSIONS = {MANIFEST, REVIEW}


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=text)
    return result.stdout


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def staged_paths() -> list[str]:
    return sorted(line for line in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line)


def index_blob(path: str) -> str:
    line = str(git("ls-files", "-s", "--", path)).strip()
    if not line:
        raise RuntimeError(f"missing staged index entry: {path}")
    return line.split()[1]


def staged_bytes(path: str) -> bytes:
    return bytes(git("show", f":{path}", text=False))


def main() -> None:
    paths = staged_paths()
    allowed_scripts = {
        "scripts/ghc_family_v647_v6_definitions.py",
        "scripts/build_ghc_family_v647_v6_preregistration.py",
        "scripts/ghc_family_v647_v6_x1_review.py",
    }
    allowed_tests = {"tests/test_ghc_family_v647_v6_x1.py"}
    out_of_scope = [
        path for path in paths
        if not path.startswith("docs/ilyra-fen/v647-v6/") and path not in allowed_scripts and path not in allowed_tests
    ]
    forbidden_path_tokens = ("x2-proposal-ledger", "x2-portfolio-execution", "x2-candidate-execution", "evidence-receipt", "closeout-receipt", "seal-receipt", "final-receipt")
    forbidden_paths = [path for path in paths if any(token in path for token in forbidden_path_tokens)]
    content_paths = [path for path in paths if path not in SELF_EXCLUSIONS]
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_uri": re.compile(rb"\b(?:app|plugin)://", re.I),
        "delegation_markup": re.compile(rb"<(?:codex_delegation|source_thread_id)>", re.I),
        "credential_assignment": re.compile(rb"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
    }
    privacy_hits = []
    x2_credit_hits = []
    entries = []
    for path in content_paths:
        data = staged_bytes(path)
        for label, pattern in patterns.items():
            if pattern.search(data):
                privacy_hits.append({"path": path, "pattern_class": label})
        forbidden_credit_needles = [
            b'"x2_completion_' + b'credit": true',
            b'"x2_execution_' + b'present": true',
        ]
        if any(needle in data for needle in forbidden_credit_needles):
            x2_credit_hits.append(path)
        entries.append({"path": path, "git_blob": index_blob(path), "bytes": len(data)})
    manifest = {
        "schema": "ghc.family.v647-v6.x1-staged-manifest.v1",
        "hash_domain": "Git index blob identity",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "boundary": "This manifest seals the staged x1 plan surface only; it contains no x2 outcome credit.",
    }
    review = {
        "schema": "ghc.family.v647-v6.x1-staged-review.v1",
        "staged_count": len(paths),
        "content_entry_count": len(entries),
        "out_of_scope_paths": out_of_scope,
        "forbidden_x2_paths": forbidden_paths,
        "x2_execution_credit_hits": x2_credit_hits,
        "privacy_pattern_classes": sorted(patterns),
        "privacy_hits": privacy_hits,
        "privacy_confirmed_hit_count": len(privacy_hits),
        "x1_only": not out_of_scope and not forbidden_paths and not x2_credit_hits and not privacy_hits,
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "boundary": "Staged review proves only x1 surface integrity and privacy-pattern absence within the staged paths.",
    }
    write_json(ROOT / MANIFEST, manifest)
    write_json(ROOT / REVIEW, review)
    print(json.dumps({"staged": len(paths), "entries": len(entries), "issues": len(out_of_scope) + len(forbidden_paths) + len(x2_credit_hits) + len(privacy_hits), "x1_only": review["x1_only"]}))
    if not review["x1_only"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
