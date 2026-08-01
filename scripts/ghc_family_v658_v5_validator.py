#!/usr/bin/env python3
"""Detailed bounded validator for Elaren v658-v5 evidence."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v5_phase_data as d
from ghc_family_v658_v5_runtime import validate_contract


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def validate_phase() -> dict[str, Any]:
    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append(name)
        if not condition:
            errors.append(f"{name}:{detail}")

    ledger = load("x2/proposal-ledger.json")
    check("proposal_count", ledger["proposal_count"] == 30)
    check("outcome_distribution", ledger["outcome_counts"] == d.EXPECTED_DISTRIBUTION)
    check("allowed_outcomes", set(row["outcome"] for row in ledger["rows"]) == d.ALLOWED_OUTCOMES)
    check("unique_proposal_ids", len({row["proposal_id"] for row in ledger["rows"]}) == 30)
    check("unique_slugs", len({row["slug"] for row in ledger["rows"]}) == 30)

    mutation_total = 0
    for proposal in d.PROPOSALS:
        slug, pid = proposal["slug"], proposal["proposal_id"]
        contract = load(f"surfaces/{slug}/contract.json")
        mutations = load(f"surfaces/{slug}/mutation-results.json")
        receipt = load(f"surfaces/{slug}/bounded-receipt.json")
        check(f"{pid}:contract_valid", not validate_contract(contract), str(validate_contract(contract)))
        check(f"{pid}:outcome", contract["outcome"] == proposal["expected_disposition"])
        check(f"{pid}:synthetic", contract["fixture"]["synthetic_only"] is True)
        check(f"{pid}:zero_rows", contract["fixture"]["external_rows"] == 0)
        check(f"{pid}:no_network", contract["fixture"]["network_called"] is False)
        check(f"{pid}:no_authority", contract["fixture"]["authority_action_executed"] is False)
        check(f"{pid}:five_mutations", mutations["mutation_count"] == 5)
        check(f"{pid}:all_rejected", mutations["all_rejected"] is True)
        check(f"{pid}:retained_zero_credit", all(row["retained"] and row["credit"] == 0 for row in mutations["results"]))
        check(f"{pid}:receipt_valid", receipt["valid_fixture_passed"] and receipt["all_mutations_rejected"])
        mutation_total += mutations["mutation_count"]
    check("mutation_total", mutation_total == 150)

    skills = load("tooling/skill-creator-receipts.json")
    check("skill_count", skills["skill_count"] == 10)
    check("skills_valid", skills["quick_validate_passed"] == 10)
    check("skills_not_global", skills["globally_installed"] == 0)
    for name, _ in d.SKILL_SPECS:
        check(f"skill:{name}:entry", (PHASE / "skills" / name / "SKILL.md").is_file())
        check(f"skill:{name}:agent", (PHASE / "skills" / name / "agents/openai.yaml").is_file())
        check(f"skill:{name}:smoke", load(f"skills/{name}/smoke-receipt.json")["valid"] is True)

    runners = load("tooling/runner-receipts.json")
    check("runner_count", runners["runner_count"] == 10)
    check("runners_valid", runners["valid_count"] == 10)
    check("runner_surface_count", runners["surface_count"] == 30)
    check("runner_mutations", runners["rejected_mutation_count"] == 150)

    tasks = load("x2/task-execution.json")
    check("safe_tasks", tasks["counts"]["safe_now"] == 30)
    check("candidate_tasks", tasks["counts"]["candidate"] == 20)
    check("cleanup_tasks", tasks["counts"]["clean"] == 30)
    check("all_tasks_bounded", tasks["all_bounded"] is True)

    truth = load("truth/phase-truth-x2.json")
    negatives = load("truth/retained-negative-register-x2.json")
    flow = load("method-flow/method-flow-state-x2.json")
    check("truth_distribution", truth["outcome_counts"] == d.EXPECTED_DISTRIBUTION)
    check("truth_negatives", truth["effective_negatives"] == negatives["effective_count"])
    check("truth_open_gaps", truth["effective_open_gaps"] == d.SOURCE_OPEN_GAPS + 1)
    check("truth_exact_gates", truth["effective_exact_gates"] == d.SOURCE_EXACT_GATES + 1)
    check("truth_methods", truth["effective_methods"] == flow["counts"]["effective_methods"])
    check("failures_retained", flow["all_failed_witnesses_retained"] is True)
    check("no_real_data", truth["real_data_used"] is False)
    check("no_network", truth["network_called"] is False)
    check("no_authority", truth["authority_action_executed"] is False)
    check("not_ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("route_unsent", load("orchestration/route-state-x2.json")["message_sent"] is False)

    privacy = load("validation/evidence-privacy-scan.json")
    check("privacy_valid", privacy["valid"] is True)
    check("privacy_zero_hits", privacy["hit_count"] == 0)
    manifest = load("validation/evidence-content-manifest.json")
    check("manifest_cardinality", manifest["entry_count"] == len(manifest["entries"]))
    check("manifest_unique", manifest["entry_count"] == len({row["path"] for row in manifest["entries"]}))
    check("owner_file_cap", load("validation/evidence-owner-file-cap.json")["within_cap"] is True)
    check("document_cap", load("validation/evidence-document-cap.json")["all_under_limit"] is True)
    check("stale_labels", load("validation/stale-label-hygiene-x2.json")["valid"] is True)
    return {"valid": not errors, "check_count": len(checks), "checks": checks, "error_count": len(errors), "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json")
    args = parser.parse_args()
    result = validate_phase()
    if args.json:
        path = ROOT / args.json
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": result["valid"], "checks": result["check_count"], "errors": result["error_count"]}))
    if not result["valid"]:
        for error in result["errors"]:
            print(error, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
