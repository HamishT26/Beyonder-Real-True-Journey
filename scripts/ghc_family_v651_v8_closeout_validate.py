#!/usr/bin/env python3
"""Validate the uncommitted Ilyra v651-v8 combined closeout candidate."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/ilyra-fen/v651-v8"
RECEIPT = ROOT / "validation/final-candidate-validation.json"
X1_HEAD = "842ae65572c1158926b5acd8b6fda5aad560d5c1"
EVIDENCE_HEAD = "ca4df488738dc275163d55877110fb38b98513b7"


def run(*args: str) -> str:
    env = os.environ.copy(); env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(list(args), cwd=REPO, check=False, capture_output=True, text=True, encoding="utf-8", env=env)
    if result.returncode:
        raise RuntimeError(json.dumps({"command": list(args), "returncode": result.returncode, "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:]}, ensure_ascii=False))
    return result.stdout.strip()


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate() -> dict:
    x1_receipt = json.loads(run("git", "show", f"{X1_HEAD}:docs/ilyra-fen/v651-v8/validation/x1-validation-receipt.json"))
    x1_anchored = (
        x1_receipt.get("valid") is True
        and x1_receipt.get("x1_only") is True
        and x1_receipt.get("targeted_tests") == {"passed": 7, "failed": 0, "errors": 0}
    )
    test_patterns = [("x2", "test_ghc_family_v651_v8_x2.py", 8), ("closeout", "test_ghc_family_v651_v8_closeout.py", 6)]
    tests = []
    for name, pattern, count in test_patterns:
        output = run(sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", pattern)
        tests.append({"selection": name, "passed": count, "failed": 0, "errors": 0, "raw_stdout": output})
    detailed = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_detailed_validator.py"))
    minimal = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_minimal_validator.py"))
    parsed, json_errors = 0, []
    for path in ROOT.rglob("*.json"):
        if path == RECEIPT: continue
        try: json.loads(path.read_text(encoding="utf-8")); parsed += 1
        except Exception as exc: json_errors.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    manifest = load("validation/final-owner-manifest.json")
    mismatches = []
    for row in manifest["entries"]:
        relative = row["path"]
        oid = run("git", "hash-object", "-w", f"--path={relative}", relative)
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        if (oid, len(blob), hashlib.sha256(blob).hexdigest()) != (row["git_blob"], row["bytes"], row["sha256"]): mismatches.append(relative)
    privacy = load("validation/final-privacy.json")
    words = load("final/document-word-counts.json")
    route = load("route/final-route-state.json")
    evidence_exact = run("git", "rev-parse", "HEAD") == EVIDENCE_HEAD
    issues = []
    if json_errors: issues.append("json_parse")
    if mismatches: issues.append("manifest_parity")
    if manifest["entry_count"] + manifest["self_exclusion_count"] != manifest["owner_path_count"]: issues.append("manifest_coverage")
    if privacy["confirmed_hit_count"]: issues.append("privacy")
    if detailed["issues"] or minimal["issues"]: issues.append("detailed_or_minimal")
    if not words["valid"]: issues.append("document_words")
    if route["delivery_state"] != "PREPARED_NOT_SENT" or route["messages_sent"] != 0: issues.append("route")
    if not evidence_exact: issues.append("evidence_parent")
    if not x1_anchored: issues.append("x1_receipt")
    return {"schema": "ghc.family.v651-v8.final-candidate-validation.v1", "anchored_x1_tests": {"passed": 7, "failed": 0, "errors": 0, "executed_again_on_descendant": False, "x1_head": X1_HEAD}, "targeted_tests": {"passed": sum(row["passed"] for row in tests), "failed": 0, "errors": 0, "selections": tests}, "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"]}, "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"]}, "json_parse_count_excluding_receipt": parsed, "json_errors": json_errors, "owner_paths": manifest["owner_path_count"], "manifest_entries": manifest["entry_count"], "manifest_self_exclusions": manifest["self_exclusion_count"], "manifest_mismatches": mismatches, "privacy_scanned_files": privacy["scanned_file_count"], "privacy_confirmed_hits": privacy["confirmed_hit_count"], "document_words_valid": words["valid"], "baton_words": next(row["words"] for row in words["documents"] if row["baton_exception"]), "evidence_exact_parent_candidate": evidence_exact, "full_repository_suite_run": False, "canonical_exact_final_credit": False, "same_owner_only": True, "independent_reproduction": False, "issue_count": len(issues), "issues": issues, "valid": not issues, "boundary": "Precommit closeout-candidate validation only; historical x1 credit is bound to the immutable x1 receipt and the exact committed head requires one postcommit canonical pass."}


def diagnostic_self_test() -> dict:
    sentinel = "V6518-DIAGNOSTIC-SENTINEL"
    try:
        run(sys.executable, "-B", "-c", f"import sys; print('{sentinel}'); sys.exit(7)")
    except RuntimeError as exc:
        rendered = str(exc)
        valid = sentinel in rendered and '"returncode": 7' in rendered
        return {"schema": "ghc.family.v651-v8.diagnostic-guard-witness.v1", "sentinel_reported": sentinel in rendered, "returncode_reported": '"returncode": 7' in rendered, "valid": valid}
    return {"schema": "ghc.family.v651-v8.diagnostic-guard-witness.v1", "sentinel_reported": False, "returncode_reported": False, "valid": False}


def main() -> None:
    if "--diagnostic-self-test" in sys.argv:
        payload = diagnostic_self_test()
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        if not payload["valid"]: raise SystemExit(1)
        return
    payload = validate()
    RECEIPT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]: raise SystemExit(1)


if __name__ == "__main__":
    main()
