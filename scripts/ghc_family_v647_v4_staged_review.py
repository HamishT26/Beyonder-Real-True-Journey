#!/usr/bin/env python3
"""Exact staged Git-blob review and lifecycle manifest builder for Sylven v647-v4."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sylven-arc/v647-v4")
PHASE = ROOT / PHASE_REL
RUNNERS = {
    "ghc_family_atomic_publish_tribunal.py", "ghc_family_two_pi_obligations.py", "ghc_family_planck_pr4_zero_row.py",
    "ghc_family_wastewater_handover.py", "ghc_family_oauth_jar_profile.py", "ghc_family_wastewater_authority.py",
    "ghc_family_tar_pax_tribunal.py", "ghc_family_tabs_audit.py", "ghc_family_second_law_statements.py",
    "ghc_family_target_trial_board.py",
}


def staged_paths() -> list[str]:
    output = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], cwd=ROOT, text=True, encoding="utf-8")
    return sorted({line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()})


def blob(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{relative}"], cwd=ROOT)


def receipt_paths(lifecycle: str) -> tuple[str, str, str]:
    base = (PHASE_REL / "validation").as_posix()
    return (f"{base}/{lifecycle}-staged-review.json", f"{base}/{lifecycle}-staged-privacy.json", f"{base}/{lifecycle}-staged-manifest.json")


def scope_valid(relative: str) -> bool:
    if relative.startswith(PHASE_REL.as_posix() + "/"):
        return True
    if re.fullmatch(r"scripts/(?:build_ghc_family_v647_v4_[a-z0-9_]+|ghc_family_v647_v4_[a-z0-9_]+)\.py", relative):
        return True
    if relative.startswith("scripts/") and relative.split("/")[-1] in RUNNERS:
        return True
    return re.fullmatch(r"tests/test_ghc_family_v647_v4(?:_[a-z0-9_]+)?\.py", relative) is not None


def privacy(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
        "credential_material": re.compile(rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
        "private_callable_identifier": re.compile(rb"\b(?:mcp__|codex_app__|browser_(?:send|probe|route|callable|message)_[a-z0-9_]{4,})", re.I),
        "private_conversational_record": re.compile(rb"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript|private conversational record)", re.I),
    }
    candidates, confirmed = [], []
    for relative in paths:
        content = blob(relative)
        for name, pattern in patterns.items():
            matches = list(pattern.finditer(content))
            if not matches:
                continue
            disposition = "unresolved_payload_candidate"
            if relative.endswith(("ghc_family_v647_v4_staged_review.py", "ghc_family_v647_v4_validation_runner.py")) and name in {"private_callable_identifier", "private_conversational_record"}:
                disposition = "scanner_definition_candidate"
            elif name == "private_conversational_record" and relative.startswith(PHASE_REL.as_posix() + "/"):
                disposition = "privacy_exclusion_policy_candidate"
            row = {"path": relative, "pattern_class": name, "count": len(matches), "disposition": disposition}
            candidates.append(row)
            if disposition == "unresolved_payload_candidate":
                confirmed.append(row)
    return {"pattern_classes": sorted(patterns), "candidates": candidates, "candidate_hit_count": sum(r["count"] for r in candidates), "confirmed": confirmed, "confirmed_hit_count": sum(r["count"] for r in confirmed)}


def build(lifecycle: str, paths: list[str]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    review_rel, privacy_rel, manifest_rel = receipt_paths(lifecycle)
    expected = sorted(set(paths) | {review_rel, privacy_rel, manifest_rel})
    excluded = {review_rel, privacy_rel, manifest_rel}
    entries = [{"path": p, "bytes": len(blob(p)), "sha256": hashlib.sha256(blob(p)).hexdigest()} for p in expected if p not in excluded]
    json_count, parse_failures = 0, []
    for entry in entries:
        if entry["path"].endswith(".json"):
            json_count += 1
            try:
                json.loads(blob(entry["path"]).decode("utf-8"))
            except Exception as exc:
                parse_failures.append({"path": entry["path"], "error": str(exc)})
    privacy_result = privacy([row["path"] for row in entries])
    diff = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    out_of_scope = [p for p in expected if not scope_valid(p)]
    x1_forbidden = []
    if lifecycle == "x1":
        for entry in entries:
            if entry["path"].startswith(PHASE_REL.as_posix() + "/") and any(token in entry["path"] for token in ("x2-proposal-ledger", "evidence-receipt", "closeout-receipt", "seal-receipt", "final-receipt")):
                x1_forbidden.append(entry["path"])
    valid = not out_of_scope and not parse_failures and not x1_forbidden and diff.returncode == 0 and privacy_result["confirmed_hit_count"] == 0
    review = {
        "schema": f"ghc.family.v647-v4.{lifecycle}-staged-review.v1", "lifecycle": lifecycle,
        "staged_paths": expected, "staged_path_count": len(expected), "out_of_scope_paths": out_of_scope,
        "x1_forbidden_paths": x1_forbidden, "json_parse_count": json_count, "json_parse_failures": parse_failures,
        "diff_check_returncode": diff.returncode, "diff_check_output": diff.stdout + diff.stderr,
        "result": "pass" if valid else "fail", "boundary": "Exact staged Git-blob review only; no broader assurance.",
    }
    privacy_receipt = {"schema": f"ghc.family.v647-v4.{lifecycle}-staged-privacy.v1", "files_scanned": len(entries), **privacy_result, "result": "pass" if privacy_result["confirmed_hit_count"] == 0 else "fail"}
    manifest = {"schema": f"ghc.family.v647-v4.{lifecycle}-staged-manifest.v1", "lifecycle": lifecycle, "hash_domain": "sha256 of exact Git-index blob bytes", "entries": entries, "entry_count": len(entries), "self_exclusions": sorted(excluded)}
    return review, privacy_receipt, manifest


def write(lifecycle: str, review: dict[str, Any], privacy_receipt: dict[str, Any], manifest: dict[str, Any]) -> None:
    for relative, payload in zip(receipt_paths(lifecycle), (review, privacy_receipt, manifest)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def check(lifecycle: str, paths: list[str]) -> list[str]:
    issues = []
    review_rel, privacy_rel, manifest_rel = receipt_paths(lifecycle)
    review = json.loads((ROOT / review_rel).read_text(encoding="utf-8"))
    privacy_receipt = json.loads((ROOT / privacy_rel).read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / manifest_rel).read_text(encoding="utf-8"))
    if review.get("staged_paths") != paths:
        issues.append("staged path set differs from review receipt")
    if review.get("result") != "pass" or privacy_receipt.get("result") != "pass":
        issues.append("review or privacy receipt is not passing")
    for entry in manifest.get("entries", []):
        content = blob(entry["path"])
        if len(content) != entry["bytes"] or hashlib.sha256(content).hexdigest() != entry["sha256"]:
            issues.append(f"manifest mismatch: {entry['path']}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lifecycle", choices=("x1", "evidence", "final"), required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    paths = staged_paths()
    review, privacy_receipt, manifest = build(args.lifecycle, paths)
    if args.write:
        write(args.lifecycle, review, privacy_receipt, manifest)
    current_expected = sorted(set(paths) | set(receipt_paths(args.lifecycle)))
    issues = [] if review["result"] == "pass" else ["current staged review failed"]
    if args.check:
        issues.extend(check(args.lifecycle, current_expected))
    result = {"lifecycle": args.lifecycle, "staged_paths": len(paths), "manifest_entries": manifest["entry_count"], "json_parses": review["json_parse_count"], "privacy_candidates": privacy_receipt["candidate_hit_count"], "privacy_confirmed": privacy_receipt["confirmed_hit_count"], "issues": issues, "result": "pass" if not issues else "fail"}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
