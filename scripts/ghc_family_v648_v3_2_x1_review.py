#!/usr/bin/env python3
"""Validate the Eiren Kestrel v648-v3 repeat x1-only packet."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v648-v3-2"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
ALLOWED_SOURCE_STATUS = {"current", "stable", "draft", "watch"}
RAW_UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I)
PRIVATE_PATH = re.compile(r"(?:[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b|/(?:Users|home)/)", re.I)
PRIVATE_ROUTE = re.compile(r"\b(?:thread|app|plugin)://", re.I)
SECRET = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[opusr]_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)\b")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def review() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, observed: Any) -> None:
        checks.append({"name": name, "pass": bool(condition), "observed": observed})

    proposals = load("x1-proposals.json")
    collision = load("provenance/proposal-collision-audit.json")
    sources = load("sources/source-ledger.json")
    safe = load("approval-packets/x1-safe-now-portfolio.json")
    candidates = load("prototypes/x1-candidate-plan.json")
    skill_runner = load("prototypes/x1-skill-runner-plan.json")
    cleanup = load("maintenance/x1-clean-refine-plan.json")
    negatives = load("retained-negative-register.json")
    operational = load("validation/x1-operational-negatives.json")
    phase_truth = load("phase-truth.json")
    route = load("orchestration/terminal-route-plan.json")
    method = load("method-flow/method-flow-ledger.json")
    method_validation = load("method-flow/method-flow-validation.json")
    versions = load("environment/version-receipt.json")
    deferred = load("environment/deferred-host-features.json")
    validation_plan = load("validation/single-pass-validation-plan.json")
    commit_plan = load("validation/commit-plan.json")
    baton = load("validation/file-baton-contract.json")

    proposal_rows = proposals["proposals"]
    required = {
        "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "source_needs",
        "artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition",
    }
    check("exactly_ten_distinct_proposals", len(proposal_rows) == 10 and len({row["title"].casefold() for row in proposal_rows}) == 10, len(proposal_rows))
    check("complete_preregistration_fields", all(required.issubset(row) for row in proposal_rows), sorted(required))
    check("frozen_chain_580_to_590", proposals["prior_frozen_proposal_count"] == 580 and proposals["frozen_chain_count_after_x1"] == 590, [proposals["prior_frozen_proposal_count"], proposals["frozen_chain_count_after_x1"]])
    dispositions = Counter(row["expected_disposition"] for row in proposal_rows)
    check("expected_distribution_6_2_1_1", dispositions == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(dispositions))
    check("exact_outcome_vocabulary", set(dispositions) == ALLOWED_OUTCOMES, sorted(dispositions))
    check("x1_has_no_observed_outcomes", all(row["observed_outcome"] is None and row["x2_execution_state"] == "not_started" for row in proposal_rows), proposals["x2_execution_present"])
    check("collision_gate_unchanged_and_clean", collision["threshold"] == 0.5 and collision["all_below_threshold"] is True and len(collision["audits"]) == 10, collision["threshold"])
    check("source_statuses_and_count", len(sources["sources"]) == 19 and set(sources["status_counts"]) == ALLOWED_SOURCE_STATUS, sources["status_counts"])
    check("safe_now_portfolio_15", safe["count"] == 15 and len(safe["tasks"]) == 15, safe["count"])
    check("candidate_portfolio_20", candidates["count"] == 20 and len(candidates["tasks"]) == 20, candidates["count"])
    check("skill_portfolio_20", skill_runner["skill_count"] == 20 and len(skill_runner["skills"]) == 20, skill_runner["skill_count"])
    check("runner_portfolio_10", skill_runner["runner_count"] == 10 and len(skill_runner["runners"]) == 10, skill_runner["runner_count"])
    check("cleanup_portfolio_30", cleanup["count"] == 30 and len(cleanup["tasks"]) == 30 and not cleanup["destructive_tasks"], cleanup["count"])
    check("portfolio_work_is_unexecuted", all(not row["x2_completion_credit"] for row in safe["tasks"] + candidates["tasks"] + cleanup["tasks"]), "no x2 credit")
    check("eleven_x1_negatives_retained", operational["count"] == 11 and operational["all_retained"] is True and len(operational["negatives"]) == 11, operational["count"])
    check("negative_arithmetic", negatives["inherited_effective_negatives"] == 4126 and negatives["x1_operational_negatives"] == 11 and negatives["effective_total_if_all_synthetic_execute"] == 4207, negatives)
    counts = method["counts"]
    check("method_flow_nine_preferred", counts["methods"] == 9 and counts["states"]["preferred"] == 9 and counts["states"]["candidate"] == 0, counts["states"])
    check("method_flow_fail_pass_parity", counts["witness_results"] == {"fail": 9, "pass": 9}, counts["witness_results"])
    check("method_flow_schema_valid", method_validation["valid"] is True and not method_validation["privacy_hits"], method_validation["issue_count"])
    check("phase_truth_x1_only", phase_truth["x2_started"] is False and phase_truth["outcomes_observed"] is False and phase_truth["state"] == "X1_FREEZE_CANDIDATE", phase_truth["state"])
    check("truth_boundaries_zero", (phase_truth["real_data_rows"], phase_truth["real_people_or_operations"], phase_truth["real_keys_or_tokens"], phase_truth["authority_decisions"]) == (0, 0, 0, 0), "0/0/0/0")
    check("terminal_not_ready", phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase_truth["terminal_verdict"])
    check("route_prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and route["message_sent"] is False and route["task_created"] is False and route["task_forked"] is False and route["subagent_spawned"] is False, route["state"])
    check("route_uses_file_baton", route["message_mode"] == "short_existing_task_file_pointer" and route["baton_file_required"] is True, route["message_mode"])
    check("file_baton_contract", baton["baton_word_minimum"] == 4000 and baton["baton_word_cap"] == 10000 and baton["document_word_cap"] == 6000, [baton["baton_word_minimum"], baton["baton_word_cap"]])
    check("single_pass_no_replay", validation_plan["canonical_validation_runs"] == 1 and validation_plan["named_replays"] == 0 and validation_plan["detached_replays"] == 0 and validation_plan["same_owner_repeatability_claim"] is False, validation_plan)
    check("commit_cap", commit_plan == {"phase_commits_max": 4, "preferred_phase_commits": 3, "x1_commits_max": 2, "x1_x2_mixing_allowed": False, "x2_commits_max": 2}, commit_plan)
    check("sandbox_and_hyperv_deferred", deferred["probe_run"] is False and deferred["windows_sandbox"] == "deferred_by_user" and deferred["hyper_v_nexus"] == "deferred_by_user" and deferred["feature_changed"] is False, deferred)
    check("cli_only_updated", versions["codex_cli_after"] == "0.144.5" and versions["desktop_updated"] is False and versions["elevation_used"] is False, versions)

    parse_errors = []
    json_files = sorted(PHASE.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_errors.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    check("all_json_parses", not parse_errors, len(json_files))

    privacy_hits = []
    word_cap_violations = []
    patterns = {"raw_uuid": RAW_UUID, "private_path": PRIVATE_PATH, "private_route": PRIVATE_ROUTE, "credential": SECRET}
    for path in sorted(PHASE.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        for name, pattern in patterns.items():
            if pattern.search(text):
                privacy_hits.append({"path": relative, "class": name})
        if path.suffix.lower() in {".md", ".html", ".txt"}:
            words = len(re.findall(r"\b\w+\b", text, re.UNICODE))
            if words > 6000:
                word_cap_violations.append({"path": relative, "words": words})
    check("privacy_scan_zero", not privacy_hits, privacy_hits)
    check("documents_under_6000", not word_cap_violations, word_cap_violations)

    forbidden = []
    for path in PHASE.rglob("*"):
        if path.is_file() and (path.name.startswith("x2-") or path.name in {"evidence-receipt.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"}):
            forbidden.append(path.relative_to(PHASE).as_posix())
    check("no_x2_or_closeout_artifacts", not forbidden, forbidden)

    valid = all(row["pass"] for row in checks)
    return {
        "schema": "ghc.family.v648-v3-r2.x1-review.v1",
        "valid": valid,
        "checks_total": len(checks),
        "checks_passed": sum(row["pass"] for row in checks),
        "json_files_parsed": len(json_files),
        "privacy_hits": privacy_hits,
        "word_cap_violations": word_cap_violations,
        "checks": checks,
        "boundary": "X1 review proves preregistration structure and separation only; it grants no x2, empirical, authority, production, accessibility-complete, replay, or independent-reproduction credit.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=PHASE / "validation/x1-review.json")
    args = parser.parse_args()
    result = review()
    write(args.receipt, result)
    print(json.dumps({"valid": result["valid"], "checks": result["checks_total"], "json": result["json_files_parsed"]}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
