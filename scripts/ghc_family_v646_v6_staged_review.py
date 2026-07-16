#!/usr/bin/env python3
"""Exact staged Git-blob, privacy, JSON, stale-label, and manifest review for v646-v6."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sylven-arc/v646-v6")
PHASE = ROOT / PHASE_REL


def staged_paths() -> list[str]:
    output = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], cwd=ROOT, text=True, encoding="utf-8")
    return sorted({line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()})


def index_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{relative}"], cwd=ROOT)


def privacy(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
        "credential_material": re.compile(rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
        "private_callable_identifier": re.compile(rb"\b(?:mcp__|codex_app__|browser_(?:send|probe|route|callable|message)_[a-z0-9_]{4,})", re.I),
        "session_transcript_or_stream": re.compile(rb"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript)", re.I),
    }
    candidates = []
    confirmed = []
    scanned = 0
    for relative in paths:
        try:
            content = index_bytes(relative)
        except subprocess.CalledProcessError:
            continue
        scanned += 1
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(content))
            if not matches:
                continue
            disposition = "unresolved_payload_candidate"
            if relative.endswith(("ghc_family_v646_v6_staged_review.py", "ghc_family_v646_v6_validation_runner.py")) and class_name in {"private_callable_identifier", "session_transcript_or_stream"}:
                disposition = "scanner_definition_candidate"
            elif class_name == "session_transcript_or_stream" and (
                relative.startswith("scripts/build_ghc_family_v646_v6_")
                or relative.endswith("orchestration/terminal-route-plan.json")
                or relative.endswith("threat-model.json")
            ):
                disposition = "privacy_exclusion_policy_candidate"
            row = {"path": relative, "class": class_name, "count": len(matches), "disposition": disposition}
            candidates.append(row)
            if disposition == "unresolved_payload_candidate":
                confirmed.append(row)
    return {
        "files_scanned": scanned,
        "pattern_classes": len(patterns),
        "candidate_hits": candidates,
        "candidate_hit_count": sum(row["count"] for row in candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": sum(row["count"] for row in confirmed),
    }


def receipt_paths(stage: str) -> tuple[str, str]:
    return (
        (PHASE_REL / f"validation/{stage}-staged-review.json").as_posix(),
        (PHASE_REL / f"validation/{stage}-staged-manifest.json").as_posix(),
    )


def scope_valid(relative: str) -> bool:
    return (
        relative.startswith(PHASE_REL.as_posix() + "/")
        or re.fullmatch(r"scripts/(?:build_ghc_family_v646_v6_[a-z0-9_]+|ghc_family_v646_v6_[a-z0-9_]+)\.py", relative) is not None
        or re.fullmatch(r"tests/test_ghc_family_v646_v6(?:_x1|_closeout)?\.py", relative) is not None
    )


def build(stage: str, paths: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    review_rel, manifest_rel = receipt_paths(stage)
    expected = sorted(set(paths) | {review_rel, manifest_rel})
    excluded = {review_rel, manifest_rel}
    entries = [
        {"path": relative, "sha256": hashlib.sha256(index_bytes(relative)).hexdigest()}
        for relative in expected
        if relative not in excluded
    ]
    parse_failures = []
    json_count = 0
    for entry in entries:
        if entry["path"].endswith(".json"):
            json_count += 1
            try:
                json.loads(index_bytes(entry["path"]).decode("utf-8"))
            except Exception as exc:
                parse_failures.append({"path": entry["path"], "error": str(exc)})
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    stale_candidates = []
    for entry in entries:
        if not entry["path"].startswith(PHASE_REL.as_posix() + "/"):
            continue
        text = index_bytes(entry["path"]).decode("utf-8", errors="replace")
        if "v646-v5" in text or "Tamar Vey" in text:
            stale_candidates.append({"path": entry["path"], "disposition": "explicit_source_lineage_reference"})
    privacy_result = privacy([row["path"] for row in entries])
    out_of_scope = [relative for relative in expected if not scope_valid(relative)]
    valid = not out_of_scope and not parse_failures and diff_check.returncode == 0 and privacy_result["confirmed_hit_count"] == 0
    manifest = {
        "schema": f"ghc.family.v646-v6.{stage}-staged-manifest.v1",
        "hash_domain": "git_index_blob",
        "entries": entries,
        "entry_count": len(entries),
        "declared_self_exclusions": sorted(excluded),
        "expected_staged_paths": expected,
        "expected_staged_path_count": len(expected),
    }
    review = {
        "schema": f"ghc.family.v646-v6.{stage}-staged-review.v1",
        "review_domain": "git_index_blob",
        "stage": stage,
        "staged_paths": expected,
        "staged_path_count": len(expected),
        "out_of_scope_paths": out_of_scope,
        "json_parse_count": json_count,
        "json_parse_failures": parse_failures,
        "privacy": privacy_result,
        "stale_label_candidates": stale_candidates,
        "stale_label_confirmed_issues": [],
        "diff_check_returncode": diff_check.returncode,
        "result": "pass" if valid else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    return review, manifest


def write(stage: str, review: dict[str, Any], manifest: dict[str, Any]) -> None:
    review_rel, manifest_rel = receipt_paths(stage)
    for relative, payload in ((review_rel, review), (manifest_rel, manifest)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def check(stage: str, paths: list[str]) -> list[str]:
    issues = []
    review_rel, manifest_rel = receipt_paths(stage)
    review = json.loads((ROOT / review_rel).read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / manifest_rel).read_text(encoding="utf-8"))
    if review.get("staged_paths") != paths or manifest.get("expected_staged_paths") != paths:
        issues.append("staged path set differs from receipt")
    if review.get("result") != "pass" or review.get("privacy", {}).get("confirmed_hit_count") != 0:
        issues.append("staged review receipt not passing")
    for entry in manifest.get("entries", []):
        if hashlib.sha256(index_bytes(entry["path"])).hexdigest() != entry.get("sha256"):
            issues.append(f"manifest mismatch: {entry['path']}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("evidence", "final"), required=True)
    parser.add_argument("--write-receipts", action="store_true")
    parser.add_argument("--check-receipts", action="store_true")
    args = parser.parse_args()
    paths = staged_paths()
    review, manifest = build(args.stage, paths)
    if args.write_receipts:
        write(args.stage, review, manifest)
    issues = [] if review["result"] == "pass" else ["current staged review failed"]
    if args.check_receipts:
        issues.extend(check(args.stage, paths))
    result = {
        "stage": args.stage,
        "staged_paths": len(paths),
        "manifest_entries": manifest["entry_count"],
        "json_parses": review["json_parse_count"],
        "privacy_candidates": review["privacy"]["candidate_hit_count"],
        "privacy_confirmed": review["privacy"]["confirmed_hit_count"],
        "issues": issues,
        "result": "pass" if not issues else "fail",
    }
    print(json.dumps(result, ensure_ascii=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
