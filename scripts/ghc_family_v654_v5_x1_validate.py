#!/usr/bin/env python3
"""Validate Eiren Kestrel v654-v5 x1 without running x2 or the final canonical pass."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v654-v5"
ALLOWED_STATUSES = {"current", "stable", "draft", "watch"}
EXPECTED_COUNTS = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
EXPECTED_NEGATIVES = 11330


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=REPO, text=True, encoding="utf-8").strip()


def write(relative: str, payload: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate(require_staged: bool) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed})

    proposals = load("preregistration/proposals.json")
    sources = load("sources/source-ledger.json")
    novelty = load("provenance/semantic-novelty-audit.json")
    index = load("provenance/frozen-chain-proposal-index.json")
    portfolios = load("portfolios/expanded-portfolio-plan.json")
    mutations = load("validation/preregistered-mutation-plan.json")
    negatives = load("truth/retained-negative-register.json")
    truth = load("truth/x1-phase-truth.json")
    route = load("route/terminal-route-state.json")
    successor = load("provenance/successor-authority-invariant.json")
    workflow = load("workflow/workflow-plan-refinement.json")
    method = load("method-flow/method-flow-ledger.json")
    summary = load("method-flow/method-flow-summary.json")
    privacy = load("validation/x1-staged-privacy.json")
    manifest = load("validation/x1-staged-manifest.json")

    rows = proposals["proposals"]
    check("proposal_count", proposals["proposal_count"] == len(rows) == 30, len(rows))
    counts = dict(Counter(row["expected_disposition"] for row in rows))
    check("planned_distribution", counts == EXPECTED_COUNTS, counts)
    required = {
        "hypothesis",
        "null_or_failure_condition",
        "approval_class",
        "execution_lane",
        "official_or_primary_source_needs",
        "concrete_artifacts",
        "falsifier_or_acceptance_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
    }
    check("proposal_fields", all(required <= set(row) for row in rows), len(rows))
    check("x1_no_observed_outcomes", proposals["x1_only"] and not proposals["observed_outcomes_present"] and all("observed_outcome" not in row for row in rows), proposals["observed_outcomes_present"])
    source_ids = {row["source_id"] for row in sources["sources"]}
    referenced = {source_id for row in rows for source_id in row["official_or_primary_source_needs"]}
    check("source_statuses", set(sources["status_counts"]) <= ALLOWED_STATUSES and all(row["status"] in ALLOWED_STATUSES for row in sources["sources"]), sources["status_counts"])
    check("source_references_resolve", referenced <= source_ids, sorted(referenced - source_ids))
    check("source_count", sources["source_count"] == len(sources["sources"]) == 14, sources["source_count"])
    check("frozen_index", (index["prior_count"], index["new_count"], index["count"]) == (1780, 30, 1810), [index["prior_count"], index["new_count"], index["count"]])
    check("semantic_novelty", novelty["valid"] and len(novelty["rows"]) == 30 and max(row["token_jaccard"] for row in novelty["rows"]) < 0.60, max(row["token_jaccard"] for row in novelty["rows"]))
    check("portfolio_counts", portfolios["counts"] == {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30}, portfolios["counts"])
    check("portfolio_unexecuted", all(not row["completion_credit"] for group in portfolios["portfolios"].values() for row in group), "all_false")
    check("mutations_frozen", mutations["count"] == 150 and mutations["x1_execution_count"] == 0 and all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"]), mutations["count"])
    check("negative_retention", (negatives["inherited_effective"], negatives["x1_operational_count"], negatives["effective_after_x1"]) == (11322, 8, EXPECTED_NEGATIVES) and negatives["no_failure_erased"], [negatives["inherited_effective"], negatives["x1_operational_count"], negatives["effective_after_x1"]])
    method_states = Counter(row["recommendation_state"] for row in method["methods"])
    witness_results = Counter(row["result"] for row in method["witnesses"])
    check("method_flow", len(method["methods"]) == 67 and method_states == {"preferred": 67} and witness_results == {"fail": 67, "pass": 67}, {"methods": len(method["methods"]), "states": dict(method_states), "witnesses": dict(witness_results)})
    check("method_summary", summary["valid"] and summary["counts"]["methods"] == 67, summary["counts"])
    check("workflow", workflow["valid"] and not workflow["requires_user_confirmation"], {"valid": workflow["valid"], "requires_user_confirmation": workflow["requires_user_confirmation"]})
    check("truth_boundary", truth["lifecycle"] == "x1_frozen_not_executed" and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and truth["real_row_count"] == 0, truth["lifecycle"])
    check("successor_hold", route["state"] == "ACTIVE_CURRENT_PHASE_SUCCESSOR_CONTACT_PROHIBITED" and route["create_count"] == 0 and route["contact_count"] == 0 and successor["created_count"] == 0 and successor["forked_count"] == 0 and successor["delegated_count"] == 0 and successor["contacted_count"] == 0 and successor["terminal_gate_required"], route["state"])

    json_paths = sorted(ROOT.rglob("*.json"))
    parse_failures = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_failures.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    check("json_parse", not parse_failures, {"count": len(json_paths), "failures": parse_failures})

    check("privacy", privacy["confirmed_hit_count"] == 0, privacy["confirmed_hit_count"])
    manifest_mismatches = []
    for row in manifest["entries"]:
        path = REPO / row["path"]
        if not path.is_file():
            manifest_mismatches.append({"path": row["path"], "reason": "missing"})
            continue
        oid = run("git", "hash-object", f"--path={row['path']}", row["path"])
        if oid != row["git_blob"]:
            manifest_mismatches.append({"path": row["path"], "reason": "blob", "expected": row["git_blob"], "observed": oid})
    check("manifest_replay", manifest["entry_count"] == len(manifest["entries"]) and not manifest_mismatches, {"entries": len(manifest["entries"]), "mismatches": manifest_mismatches})

    staged_paths: list[str] = []
    out_of_scope: list[str] = []
    if require_staged:
        staged_paths = sorted(run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines())
        allowed_exact = {
            "scripts/ghc_family_v654_v5_phase_data.py",
            "scripts/build_ghc_family_v654_v5_method_flow.py",
            "scripts/build_ghc_family_v654_v5_preregistration.py",
            "scripts/ghc_family_v654_v5_x1_validate.py",
            "tests/test_ghc_family_v654_v5_x1.py",
        }
        out_of_scope = [
            path for path in staged_paths
            if not path.startswith("docs/eiren-kestrel/v654-v5/") and path not in allowed_exact
        ]
        check("exact_staged_scope", bool(staged_paths) and not out_of_scope, {"count": len(staged_paths), "out_of_scope": out_of_scope})
        check("staged_x1_only", not any("/surfaces/" in path or "/evidence/" in path or "/final/" in path for path in staged_paths), "no_x2_paths")

    passed = sum(row["passed"] for row in checks)
    receipt = {
        "schema": "ghc.family.v654-v5.x1-validation.v1",
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "valid": passed == len(checks),
        "json_parse_count": len(json_paths),
        "privacy_confirmed_hit_count": privacy["confirmed_hit_count"],
        "manifest_entry_count": manifest["entry_count"],
        "require_staged": require_staged,
        "staged_path_count": len(staged_paths),
        "out_of_scope_staged_paths": out_of_scope,
        "full_repository_suite_run": False,
        "final_canonical_pass_run": False,
        "boundary": "X1-only same-owner validation; not x2, final canonical validation, independent reproduction, production assurance, complete privacy or accessibility, authority, or Stage 20 readiness.",
    }
    write("validation/x1-validation-receipt.json", receipt)
    write(
        "validation/x1-minimal-validation.json",
        {
            "schema": "ghc.family.v654-v5.x1-minimal-validation.v1",
            "checks": [
                {"name": "proposal_count", "passed": proposals["proposal_count"] == 30},
                {"name": "mutations_unexecuted", "passed": mutations["x1_execution_count"] == 0},
                {"name": "privacy_zero", "passed": privacy["confirmed_hit_count"] == 0},
                {"name": "successor_not_created_or_contacted", "passed": successor["created_count"] == 0 and successor["contacted_count"] == 0},
                {"name": "terminal_verdict", "passed": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"},
            ],
            "valid": receipt["valid"],
            "boundary": receipt["boundary"],
        },
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-staged", action="store_true")
    args = parser.parse_args()
    receipt = validate(args.require_staged)
    print(json.dumps({"passed": receipt["passed"], "total": receipt["total"], "valid": receipt["valid"]}, sort_keys=True))
    raise SystemExit(0 if receipt["valid"] else 1)


if __name__ == "__main__":
    main()
