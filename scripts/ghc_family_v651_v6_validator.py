#!/usr/bin/env python3
"""Detailed bounded validator for Elaren v651-v6 evidence and final trees."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/elaren-kestrel/v651-v6"
X1 = "b0ba19472777bc07f91c0358186b48311aa3bce3"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY = {
    "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_path": re.compile(r"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(r"(?:codex|chatgpt|file|vscode|app|thread)://", re.I),
    "delegation": re.compile(r"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential": re.compile(r"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def read(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate(output_relative: str | None = None, require_clean: bool = False) -> dict[str, Any]:
    checks: list[str] = []
    issues: list[str] = []

    def check(name: str, condition: bool) -> None:
        checks.append(name)
        if not condition:
            issues.append(name)

    packet = read("preregistration/proposals.json")
    outcomes = read("outcomes/core-outcomes.json")
    mutations = read("validation/preregistered-mutations.json")
    mutation_receipt = read("validation/mutation-execution-receipt.json")
    truth = read("truth/evidence-phase-truth.json")
    negatives = read("truth/retained-negative-register-x2.json")
    gates = read("gates/exact-open-gate-register.json")
    portfolio = read("portfolios/x2-portfolio-outcomes.json")
    skill_receipt = read("tooling/skill-build-receipt.json")
    runner_receipt = read("tooling/runner-use-receipt.json")

    check("proposal_count", len(packet["proposals"]) == 30)
    check("outcome_count", len(outcomes["outcomes"]) == 30)
    check("outcome_distribution", outcomes["outcome_counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
    check("outcome_vocabulary", set(row["truth_label"] for row in outcomes["outcomes"]) == ALLOWED)
    check("mutation_count", mutations["count"] == len(mutations["mutations"]) == 100)
    check("mutation_rejection", mutation_receipt["executed"] == mutation_receipt["rejected"] == 100 and mutation_receipt["accepted"] == 0)
    check("negative_total", negatives["effective_total"] == 7325 and negatives["failures_erased"] == 0 and negatives["x2_operational"] == 1)
    check("gate_total", (gates["effective_open_gaps"], gates["effective_exact_gates"], gates["silently_closed"]) == (57, 58, 0))
    check("portfolio_counts", portfolio["counts"] == {"safe_now_completed": 40, "candidate_resolved": 30, "skills_built_validated_used": 20, "runners_built_invoked": 10, "clean_fix_refine_completed": 40})
    check("skill_count", skill_receipt["skill_count"] == skill_receipt["quick_validated"] == skill_receipt["smoke_used"] == 20)
    check("runner_count", runner_receipt["runner_count"] == runner_receipt["invoked_count"] == 10 and runner_receipt["surface_coverage_count"] == 30)
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("no_real_evidence", all(truth[key] == 0 for key in ("real_data_rows", "participants", "real_keys_or_proofs", "authority_decisions", "production_actions")))
    check("same_owner_only", truth["same_owner_only"] and not truth["independent_reproduction"])

    source_ids = {row["source_id"] for row in read("sources/source-ledger.json")["entries"]}
    for proposal in packet["proposals"]:
        evidence = read(f"proposals/{proposal['slug']}.json")
        prefix = proposal["proposal_id"]
        check(f"{prefix}:id", evidence["proposal_id"] == proposal["proposal_id"])
        check(f"{prefix}:slug", evidence["slug"] == proposal["slug"])
        check(f"{prefix}:label", evidence["truth_label"] == proposal["expected_disposition"] in ALLOWED)
        check(f"{prefix}:valid_fixture", evidence["valid_fixture_passed"] is True)
        check(f"{prefix}:mutations", evidence["rejected_mutation_count"] in {3, 4} and len(evidence["rejecting_mutation_ids"]) == evidence["rejected_mutation_count"])
        check(f"{prefix}:source", bool(evidence["source_ids"]) and set(evidence["source_ids"]) <= source_ids)
        check(f"{prefix}:zero_real", evidence["real_data_rows"] == evidence["participant_count"] == evidence["real_keys_or_proofs"] == evidence["production_actions"] == evidence["authority_decisions"] == 0)
        check(f"{prefix}:same_owner", evidence["same_owner_only"] and not evidence["independent_reproduction"])
        check(f"{prefix}:claims_false", all(value is False for value in evidence["protected_claims"].values()))
        check(f"{prefix}:boundary", "bounded" in evidence["boundary"].casefold())

    method = read("method-flow/x2-method-flow-ledger.json")
    check("method_count", method["counts"]["methods"] == 6)
    check("method_witnesses", method["counts"]["witness_results"] == {"fail": 6, "pass": 6})
    check("method_preferred", method["counts"]["states"].get("preferred") == 6 and all(row["recommendation_state"] == "preferred" for row in method["methods"]))

    overview = (PHASE / "overview/integrated-overview.md").read_text(encoding="utf-8")
    report = (PHASE / "reports/accessible-static-report.html").read_text(encoding="utf-8")
    check("overview_words", 3000 <= len(overview.split()) <= 100000)
    for token in ('<html lang="en">', "<main>", '<nav aria-label="Report">', "<caption>", '<th scope="col">', "Manual accessibility review", "NOT_READY_FOR_STAGE_20"):
        check(f"report:{token}", token.casefold() in report.casefold())
    check("report_no_script", "<script" not in report.casefold())

    json_paths = sorted(path for path in PHASE.rglob("*.json") if output_relative is None or path.resolve() != (REPO / output_relative).resolve())
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            issues.append(f"json:{path.relative_to(PHASE).as_posix()}")
    checks.append("json_parse_complete")

    privacy_hits = []
    privacy_paths = sorted(path for path in PHASE.rglob("*") if path.is_file() and (output_relative is None or path.resolve() != (REPO / output_relative).resolve()))
    for path in privacy_paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(PHASE).as_posix(), "class": name})
    check("privacy_zero_hits", not privacy_hits)

    result = {
        "schema": "ghc.family.v651-v6.detailed-validation.v1",
        "valid": not issues,
        "check_count": len(checks),
        "issues": issues,
        "json_parse_count": len(json_paths),
        "privacy_file_count": len(privacy_paths),
        "privacy_pattern_classes": len(PRIVACY),
        "privacy_confirmed_hits": privacy_hits,
        "require_clean": require_clean,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if require_clean:
        status = subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=REPO, text=True, encoding="utf-8").strip()
        result["clean"] = not status
        if status:
            result["valid"] = False
            result["issues"].append("worktree_not_clean")
    if output_relative:
        target = REPO / output_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()
    result = validate(args.output, args.require_clean)
    print(json.dumps({key: result[key] for key in ("valid", "check_count", "json_parse_count", "privacy_file_count", "privacy_confirmed_hits")}, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
