#!/usr/bin/env python3
"""Validate Orin Thale v652-v2 x1 without executing x2 work."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"
SOURCE = "f168bcb798715d61d8b0a9ec2c6646a7af09ce29"
OUT = ROOT / "validation/x1-validation-receipt.json"
MINIMAL = ROOT / "validation/x1-minimal-validation.json"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env).stdout.strip()


def write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    checks = []

    def check(name: str, condition: bool, observed) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})

    source_files = [
        REPO / "scripts/ghc_family_v652_v2_phase_data.py",
        REPO / "scripts/build_ghc_family_v652_v2_preregistration.py",
        REPO / "scripts/ghc_family_v652_v2_x1_validate.py",
        REPO / "tests/test_ghc_family_v652_v2_x1.py",
    ]
    syntax_issues = []
    for path in source_files:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - receipt path
            syntax_issues.append({"path": path.relative_to(REPO).as_posix(), "error": str(exc)})
    check("python_source_syntax", not syntax_issues, syntax_issues)

    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    suite = subprocess.run([sys.executable, "-m", "unittest", "tests.test_ghc_family_v652_v2_x1", "-v"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", env=env)
    check("x1_unit_tests", suite.returncode == 0 and "Ran 6 tests" in suite.stderr and "OK" in suite.stderr, {"exit_code": suite.returncode, "expected": 6})

    json_paths = sorted(ROOT.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append({"path": path.relative_to(REPO).as_posix(), "error": str(exc)})
    check("complete_phase_json_parse", not json_issues, {"parsed": len(json_paths), "issues": json_issues})

    proposals = load("preregistration/proposals.json")
    check("exact_proposal_count", proposals["proposal_count"] == 30, proposals["proposal_count"])
    check("expected_dispositions", proposals["expected_disposition_counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, proposals["expected_disposition_counts"])
    check("x1_has_no_observed_outcomes", proposals["x1_only"] and not proposals["observed_outcomes_present"] and all("observed_outcome" not in row for row in proposals["proposals"]), proposals["observed_outcomes_present"])

    index = load("provenance/frozen-chain-proposal-index.json")
    audit = load("provenance/semantic-novelty-audit.json")
    check("frozen_chain_1240", (index["prior_count"], index["new_count"], index["count"]) == (1210, 30, 1240), {key: index[key] for key in ("prior_count", "new_count", "count")})
    check("novelty_and_manual_review", audit["valid"] and audit["manual_mechanism_review_count"] == 30 and max(row["token_jaccard"] for row in audit["rows"]) < 0.60, max(row["token_jaccard"] for row in audit["rows"]))

    portfolios = load("portfolios/expanded-portfolio-plan.json")
    check("portfolio_floors", portfolios["counts"] == {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30}, portfolios["counts"])
    mutations = load("validation/preregistered-mutation-plan.json")
    check("mutations_frozen_unexecuted", mutations["count"] == 150 and all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"]), mutations["count"])

    negatives = load("truth/retained-negative-register.json")
    check("retained_negative_count", (negatives["inherited_effective"], negatives["x1_operational_count"], negatives["effective_after_x1"]) == (8022, 15, 8037), {key: negatives[key] for key in ("inherited_effective", "x1_operational_count", "effective_after_x1")})
    method = load("method-flow/method-flow-validation.json")
    check("method_flow_valid", method["valid"] and method["method_count"] >= 13 and method["witness_count"] >= 13, {key: method[key] for key in ("valid", "method_count", "witness_count")})

    workflow = load("workflow/workflow-plan-refinement.json")
    check("workflow_plan_valid", workflow["valid"] and not workflow["requires_user_confirmation"], {"valid": workflow["valid"], "requires_user_confirmation": workflow["requires_user_confirmation"]})
    placeholder = load("provenance/future-cli-placeholder-invariant.json")
    check("future_cli_placeholders_unlaunched", (placeholder["prepared_placeholder_count"], placeholder["named_count"], placeholder["created_count"], placeholder["launched_count"]) == (8, 0, 0, 0), {key: placeholder[key] for key in ("prepared_placeholder_count", "named_count", "created_count", "launched_count")})

    privacy = load("validation/x1-staged-privacy.json")
    check("privacy_scan_zero_confirmed", privacy["confirmed_hit_count"] == 0 and len(privacy["pattern_classes"]) == 5, {"scanned": privacy["scanned_file_count"], "confirmed": privacy["confirmed_hit_count"]})

    manifest = load("validation/x1-staged-manifest.json")
    entries = {row["path"]: row for row in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    status_rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    status = {row[3:].replace("\\", "/") for row in status_rows if len(row) > 3 and "__pycache__" not in row}
    expected_paths = status - exclusions
    check("manifest_path_set", set(entries) == expected_paths, {"entries": len(entries), "expected": len(expected_paths), "missing": sorted(expected_paths - set(entries)), "extra": sorted(set(entries) - expected_paths)})
    mismatches = []
    for relative, row in entries.items():
        oid = git("hash-object", f"--path={relative}", relative)
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        if oid != row["git_blob"] or len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            mismatches.append(relative)
    check("manifest_blob_parity", not mismatches, {"checked": len(entries), "mismatches": mismatches})

    anchor = load("provenance/source-anchor-ledger.json")
    check("source_anchor_contract", anchor["source_head"] == SOURCE and anchor["history"] == {"final_parent_count": 1, "phase_commits": 4, "single_parent": True, "zero_merges": True} and anchor["source_manifests"]["mismatches"] == 0, anchor["source_head"])
    check("no_x2_surface", not (ROOT / "surfaces").exists(), str((ROOT / "surfaces").exists()))

    overview_words = len((ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8").split())
    check("overview_three_page_equivalent", overview_words >= 1300, overview_words)
    route = load("route/terminal-route-state.json")
    check("route_held", route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and route["create_or_fork_count"] == 0, route["state"])
    truth = load("truth/x1-phase-truth.json")
    check("terminal_truth", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and truth["observed_outcome_count"] == 0 and not truth["independent_reproduction_claimed"], truth)

    passed = sum(row["passed"] for row in checks)
    receipt = {
        "schema": "ghc.family.v652-v2.x1-validation.v1",
        "phase": "v652-v2",
        "owner": "Orin Thale",
        "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "valid": passed == len(checks),
        "unit_test_summary": {"passed": 6, "total": 6, "exit_code": suite.returncode},
        "json_parse_count": len(json_paths),
        "boundary": "X1 preregistration validation only; not x2, final canonical validation, independent reproduction, production certification, empirical confirmation, legal or cultural authority, complete privacy or accessibility, or Stage 20 authority.",
    }
    write(OUT, receipt)
    minimal_names = ["exact_proposal_count", "frozen_chain_1240", "x1_has_no_observed_outcomes", "manifest_blob_parity", "privacy_scan_zero_confirmed", "route_held", "terminal_truth"]
    minimal_rows = [row for row in checks if row["name"] in minimal_names]
    write(MINIMAL, {"schema": "ghc.family.v652-v2.x1-minimal-validation.v1", "checks": minimal_rows, "passed": sum(row["passed"] for row in minimal_rows), "total": len(minimal_rows), "valid": all(row["passed"] for row in minimal_rows), "boundary": receipt["boundary"]})
    print(json.dumps({"passed": passed, "total": len(checks), "unit_tests": 6, "json": len(json_paths), "valid": receipt["valid"]}, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
