#!/usr/bin/env python3
"""Review the exact staged owner blobs for Sylven v645-v8."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/sylven-arc/v645-v8/"
SELF_PATHS = {
    f"{PHASE_PREFIX}validation/evidence-staged-review.json",
    f"{PHASE_PREFIX}validation/evidence-staged-manifest.json",
}
PATTERNS = {
    "raw_uuid_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_route_or_callable": re.compile("(?:source_" + "thread_id|client" + "ThreadId|app" + "://|codex" + "://|private_" + "callable_id)", re.I),
    "credential_or_secret_material": re.compile("(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE " + "KEY|api[_-]?" + "key\\s*[:=]|authorization:\\s*bearer\\s+[A-Za-z0-9._~-]{12,})", re.I),
    "private_absolute_local_path": re.compile("(?:[A-Za-z]:\\\\" + "Users\\\\[^\\\\\\s]+\\\\|D:\\\\GHC-" + "Archives\\\\)", re.I),
    "private_session_artifact": re.compile("(?:session[_ -]?" + "stream[_ -]?(?:path|id)|transcript[_ -]?(?:path|id)|screenshot[_ -]?(?:path|id))", re.I),
}


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def write(relative: str, payload: dict) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", default="evidence", choices=["evidence", "closeout"])
    args = parser.parse_args()
    names = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    statuses = [row.split("\t", 1) for row in git("diff", "--cached", "--name-status", "--diff-filter=ACMR").splitlines() if row]
    owner = sorted(path for path in names if path.startswith(PHASE_PREFIX) or re.fullmatch(r"(?:scripts|tests)/[^/]*v645_v8[^/]*\.py", path))
    entries = []
    candidates = []
    confirmed = []
    json_failures = []
    for path in owner:
        if path in SELF_PATHS:
            continue
        data = git("show", f":{path}", binary=True)
        entries.append({"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            confirmed.append({"path": path, "pattern_class": "invalid_utf8"})
            continue
        if path.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError:
                json_failures.append(path)
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                line = text.splitlines()[line_number - 1]
                scanner_definition = path == "scripts/ghc_family_v645_v8_x1_review.py" and label in line and "re.compile" in line
                row = {"path": path, "pattern_class": label, "line": line_number, "context": "scanner_definition" if scanner_definition else "content"}
                candidates.append(row)
                if not scanner_definition:
                    confirmed.append(row)
    unexpected = sorted(set(names) - set(owner))
    non_additive = [path for status, path in statuses if status != "A"]
    manifest_path = f"{PHASE_PREFIX}validation/{args.stage}-staged-manifest.json"
    review_path = f"{PHASE_PREFIX}validation/{args.stage}-staged-review.json"
    manifest = {"schema": f"ghc.family.v645-v8.{args.stage}-staged-manifest.v1", "stage": args.stage, "domain": "exact staged Git blobs", "entry_count": len(entries), "entries": entries, "self_excluded": sorted(SELF_PATHS), "valid": True}
    review = {
        "schema": f"ghc.family.v645-v8.{args.stage}-staged-review.v1",
        "stage": args.stage,
        "staged_file_count": len(names),
        "owner_staged_file_count": len(owner),
        "manifest_entry_count": len(entries),
        "unexpected_paths": unexpected,
        "non_additive_paths": non_additive,
        "json_failures": json_failures,
        "privacy_pattern_classes": sorted(PATTERNS),
        "privacy_candidate_count": len(candidates),
        "privacy_candidates": candidates,
        "privacy_confirmed_hit_count": len(confirmed),
        "privacy_confirmed_hits": confirmed,
        "x1_tracked_paths_modified": non_additive,
        "valid": not unexpected and not non_additive and not json_failures and not confirmed,
        "boundary": "Exact staged review is not privacy-complete, security-complete, or independent reproduction.",
    }
    write(manifest_path, manifest)
    write(review_path, review)
    print(json.dumps({"stage": args.stage, "files": len(names), "entries": len(entries), "candidates": len(candidates), "confirmed": len(confirmed), "valid": review["valid"]}, ensure_ascii=False))
    return 0 if review["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
