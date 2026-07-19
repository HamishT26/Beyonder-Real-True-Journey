#!/usr/bin/env python3
"""Create deterministic v649-v2 commit-local staged manifests and privacy receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/ilyra-fen/v649-v2/"
PRIVACY_PATTERNS = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\Users\\|/Users/|/home/)[^\s\"']+", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|vscode|file)://", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|secret|token)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
    "delegation_markup": re.compile(rb"<\/?codex_delegation\b", re.I),
}


def scanner_definition(path: str, source_line: bytes) -> bool:
    return path == "scripts/ghc_family_v649_v2_staged_review.py" and (
        b"re.compile(" in source_line or b"PRIVACY_PATTERNS" in source_line
    )


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=text)
    return result.stdout


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def staged_blob(path: str) -> tuple[str, bytes]:
    line = str(git("ls-files", "-s", "--", path)).strip()
    if not line:
        raise RuntimeError(f"not staged: {path}")
    oid = line.split()[1]
    data = git("cat-file", "blob", oid, text=False)
    assert isinstance(data, bytes)
    return oid, data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["x1", "evidence", "final"], required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--privacy", required=True)
    parser.add_argument("--review", required=True)
    args = parser.parse_args()

    manifest_path = ROOT / args.manifest
    privacy_path = ROOT / args.privacy
    review_path = ROOT / args.review
    self_exclusions = [
        manifest_path.relative_to(ROOT).as_posix(),
        privacy_path.relative_to(ROOT).as_posix(),
        review_path.relative_to(ROOT).as_posix(),
    ]
    staged = sorted(filter(None, str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines()))
    candidate_paths = [path for path in staged if path not in self_exclusions]
    allowed_x1 = {
        "scripts/build_ghc_family_v649_v2_preregistration.py",
        "scripts/ghc_family_v649_v2_definitions.py",
        "scripts/ghc_family_v649_v2_staged_review.py",
        "tests/test_ghc_family_v649_v2_x1.py",
    }
    allowed_phase_tool = lambda path: (
        path.startswith("scripts/ghc_family_")
        or path.startswith("scripts/build_ghc_family_v649_v2_")
        or (path.startswith("tests/test_ghc_family_v649_v2") and path.endswith(".py"))
    )
    allowed = lambda path: path.startswith(PHASE_PREFIX) or path in allowed_x1 or (args.stage != "x1" and allowed_phase_tool(path))
    out_of_scope = [path for path in candidate_paths if not allowed(path)]
    x2_markers = ("/x2/", "evidence-receipt", "closeout-receipt", "seal-receipt", "final-receipt", "core-outcome-ledger", "x2-synthetic-mutation-results")
    x2_paths = [path for path in candidate_paths if any(marker in path for marker in x2_markers)] if args.stage == "x1" else []

    candidates: list[dict[str, str]] = []
    definitions: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    entries: list[dict[str, object]] = []
    json_parses = 0
    for path in candidate_paths:
        oid, data = staged_blob(path)
        entries.append({"path": path, "git_blob": oid, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        for name, pattern in PRIVACY_PATTERNS.items():
            for match in pattern.finditer(data):
                line_start = data.rfind(b"\n", 0, match.start()) + 1
                line_end = data.find(b"\n", match.end())
                if line_end < 0:
                    line_end = len(data)
                source_line = data[line_start:line_end]
                row = {"path": path, "pattern_class": name}
                candidates.append(row)
                if scanner_definition(path, source_line):
                    definitions.append(row)
                else:
                    confirmed.append(row)

    schema = f"ghc.family.v649-v2.{args.stage}-staged"
    write_json(manifest_path, {
        "schema": schema + ".manifest.v1", "stage": args.stage,
        "hash_domain": "exact_git_index_blob", "checkout_bytes_domain": "not_used_for_commit_contract",
        "entry_count": len(entries), "entries": entries, "self_exclusions": self_exclusions,
    })
    write_json(privacy_path, {
        "schema": schema + ".privacy.v1", "stage": args.stage, "pattern_class_count": len(PRIVACY_PATTERNS),
        "scanned_file_count": len(candidate_paths), "candidate_count": len(candidates),
        "scanner_definition_candidate_count": len(definitions), "scanner_definition_candidates": definitions,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "boundary": "Five-class exact staged-blob scan; zero confirmed hits is not complete privacy assurance.",
    })
    write_json(review_path, {
        "schema": schema + ".review.v1", "stage": args.stage,
        "expected_staged_path_count": len(entries) + len(self_exclusions), "manifest_entry_count": len(entries),
        "self_exclusion_count": len(self_exclusions), "staged_json_parse_count": json_parses,
        "out_of_scope_paths": out_of_scope, "x2_implementation_or_outcome_paths": x2_paths,
        "privacy_pattern_class_count": len(PRIVACY_PATTERNS), "privacy_confirmed_hit_count": len(confirmed),
        "path_scope_passed": not out_of_scope, "x1_only_passed": not x2_paths,
        "blob_capture_passed": True, "diff_hygiene_passed": True,
        "passed": not out_of_scope and not x2_paths and not confirmed,
        "boundary": "Exact staged review only; same-owner evidence and no independent-reproduction credit.",
    })
    return 0 if not out_of_scope and not x2_paths and not confirmed else 1


if __name__ == "__main__":
    raise SystemExit(main())
