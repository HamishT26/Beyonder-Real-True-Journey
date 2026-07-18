#!/usr/bin/env python3
"""Exact staged-file review for Tamar Vey v648-v7 x1."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "tamar-vey" / "v648-v7" / "validation" / "x1-staged-manifest.json"
DEFAULT_RECEIPT = ROOT / "docs" / "tamar-vey" / "v648-v7" / "validation" / "x1-staged-review.json"


def git(*args: str, binary: bool = False):
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def review() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = {row["path"]: row for row in manifest["entries"]}
    expected = set(entries) | set(manifest["self_exclusions"])
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
        "scripts/build_ghc_family_v648_v7_preregistration.py",
        "scripts/ghc_family_v648_v7_x1_staged_review.py",
        "docs/tamar-vey/v648-v7/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v648-v7/validation/x1-privacy-complete-surface-preview.json",
    }
    boundary_definitions = {
        "docs/tamar-vey/v648-v7/approval-packets/inherited-exact-approvals.json",
        "scripts/ghc_family_v648_v7_definitions.py",
        "docs/tamar-vey/v648-v7/validation/x1-operational-negatives.json",
    }
    strict_secret = re.compile(r"(?i)(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"'][^\"']{6,}[\"']|bearer\s+[A-Za-z0-9._-]{12,}")
    parsed = 0
    candidates = []
    confirmed = []
    blob_mismatches = []
    checkout_byte_mismatches = []
    for relative in sorted(staged):
        blob = git("show", f":{relative}", binary=True)
        if relative in entries:
            oid = git("rev-parse", f":{relative}")
            if oid != entries[relative]["git_blob"]:
                blob_mismatches.append(relative)
            working = ROOT / relative
            if not working.is_file() or working.stat().st_size != entries[relative]["bytes"]:
                checkout_byte_mismatches.append(relative)
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
                defined = relative in scanner_definitions or (
                    pattern_class == "credential_or_secret"
                    and (relative in boundary_definitions or relative.startswith("docs/tamar-vey/v648-v7/method-flow/"))
                    and not strict_secret.search(text)
                )
                if not defined:
                    confirmed.append(row)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    if confirmed or blob_mismatches or checkout_byte_mismatches:
        raise RuntimeError("staged privacy, blob, or checkout-byte mismatch")
    return {
        "actual_staged_review": True,
        "actual_staged_path_count": len(staged),
        "actual_staged_json_parse_count": parsed,
        "actual_manifest_entry_count": len(entries),
        "actual_self_exclusion_count": len(manifest["self_exclusions"]),
        "actual_privacy_pattern_class_count": len(patterns),
        "actual_privacy_candidate_count": len(candidates),
        "actual_privacy_confirmed_hit_count": len(confirmed),
        "actual_blob_mismatch_count": len(blob_mismatches),
        "actual_checkout_byte_mismatch_count": len(checkout_byte_mismatches),
        "actual_diff_hygiene_passed": True,
        "actual_path_parity_passed": True,
        "review_boundary": "Exact Git-index blobs plus current checkout bytes; zero confirmed hits is not complete privacy assurance.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    args = parser.parse_args()
    result = review()
    receipt = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload.update(result)
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
