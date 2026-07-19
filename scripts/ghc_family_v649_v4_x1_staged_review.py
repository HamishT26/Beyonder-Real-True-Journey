#!/usr/bin/env python3
"""Exact staged-file review for Orin Thale v649-v4 x1."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "orin-thale" / "v649-v4" / "validation" / "x1-staged-manifest.json"
DEFAULT_RECEIPT = ROOT / "docs" / "orin-thale" / "v649-v4" / "validation" / "x1-staged-review.json"


def git(*args: str, binary: bool = False):
    completed = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return completed.stdout if binary else completed.stdout.decode("utf-8").strip()


def review() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    staged = set(filter(None, git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    if staged != expected:
        raise RuntimeError(f"staged path mismatch missing={sorted(expected-staged)} unexpected={sorted(staged-expected)}")
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    scanner_definitions = {
        "scripts/build_ghc_family_v649_v4_preregistration.py",
        "scripts/ghc_family_v649_v4_x1_staged_review.py",
        "docs/orin-thale/v649-v4/validation/x1-staged-privacy.json",
    }
    parsed = 0
    candidates = []
    confirmed = []
    for relative in sorted(staged):
        blob = git("show", f":{relative}", binary=True)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if relative.endswith(".json"):
            json.loads(text)
            parsed += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                row = {"path": relative, "pattern_class": pattern_class}
                candidates.append(row)
                if relative not in scanner_definitions:
                    confirmed.append(row)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    return {
        "actual_staged_review": True,
        "actual_staged_path_count": len(staged),
        "actual_staged_json_parse_count": parsed,
        "actual_manifest_entry_count": len(manifest["entries"]),
        "actual_self_exclusion_count": len(manifest["self_exclusions"]),
        "actual_privacy_pattern_class_count": len(patterns),
        "actual_privacy_candidate_count": len(candidates),
        "actual_privacy_confirmed_hit_count": len(confirmed),
        "actual_diff_hygiene_passed": True,
        "actual_path_parity_passed": True,
        "review_boundary": "Exact Git-index blobs only; zero confirmed hits is not complete privacy assurance.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = review()
    if args.receipt:
        receipt = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        payload.update(result)
        receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
