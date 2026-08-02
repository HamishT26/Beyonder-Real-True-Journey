#!/usr/bin/env python3
"""Detailed same-owner validator for the Lyren v658-v8 (2) remaster."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import ghc_family_v658_v8_2_remaster_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
EVIDENCE_COMMIT = "e08a7bb24c9fc9c442374d251b985437a88ade11"


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def validate_phase() -> dict[str, Any]:
    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, predicate: bool | Callable[[], bool]) -> None:
        try:
            valid = predicate() if callable(predicate) else predicate
        except Exception as exc:  # keep the complete issue set visible
            errors.append(f"{name}: {type(exc).__name__}: {exc}")
            return
        if valid:
            checks.append(name)
        else:
            errors.append(name)

    truth = load("final/final-truth.json")
    outcomes = load("evidence/proposal-outcomes.json")
    mutations = load("evidence/mutation-register.json")
    methods = load("tooling/method-flow/validation-x2.json")
    runners = load("tooling/runner-aggregate.json")
    skills = load("tooling/skill-validation.json")
    install = load("tooling/global-skill-installation.json")
    cleanup = load("cleanup/cleanup-aggregate.json")
    prototypes = load("tooling/candidate-prototype-aggregate.json")
    scan = load("tooling/runner-smoke/ghc_family_latest_tracked_file_scan.json")
    route = load("route/prepared-route.json")
    privacy = load("validation/closeout-privacy-scan.json")
    staged = load("validation/closeout-staged-review.json")
    documents = load("validation/final-document-cap.json")
    baton = (PHASE / "handoffs/ilyra-fen-v659-v1-activation.md").read_text(encoding="utf-8")

    check("owner_and_phase", truth["owner"] == d.OWNER and truth["phase"] == d.PHASE)
    check("source_final", truth["source_final"] == d.SOURCE_FINAL)
    check("x1_freeze", truth["x1_freeze"] == d.X1_FREEZE)
    check("x2_evidence", truth["x2_evidence"] == EVIDENCE_COMMIT)
    check("frozen_chain", truth["effective_frozen"] == 2910)
    check("effective_negatives", truth["effective_negatives"] == 18078)
    check("effective_methods", truth["effective_methods"] == 4352)
    check("open_gaps", truth["effective_open_gaps"] == 121)
    check("exact_gates", truth["effective_exact_gates"] == 120)
    check("not_ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("same_owner_only", truth["same_owner_only"] is True)
    check("not_independent", truth["independent_reproduction"] is False)
    check(
        "outcome_distribution",
        truth["observed_outcomes"] == {"completed": 33, "represented": 5, "open_gap": 1, "exact_gate": 1},
    )
    check("proposal_count", outcomes["proposal_count"] == 40 and len(outcomes["outcomes"]) == 40)
    check(
        "proposal_labels",
        set(row["observed_outcome"] for row in outcomes["outcomes"]) == d.ALLOWED_OUTCOMES,
    )
    check("valid_fixtures", all(row["valid_fixture_passed"] for row in outcomes["outcomes"]))
    check("all_mutations_rejected", all(row["all_mutations_rejected"] for row in outcomes["outcomes"]))
    check("mutation_count", mutations["mutation_count"] == 200)
    check("mutations_retained", all(row["retained"] and row["credit"] == 0 for row in mutations["mutations"]))
    check("method_flow_valid", methods["valid"] is True and methods["issue_count"] == 0)
    check("method_flow_methods", methods["method_count"] == 203)
    check("method_flow_witnesses", methods["witness_count"] == 406)
    check(
        "closeout_method_flow",
        load("final/lifecycle-method-flow.json")["method_count"] == 6
        and load("final/lifecycle-method-flow.json")["witness_count"] == 12,
    )
    check("skills", skills["all_valid"] is True and skills["valid_skill_count"] == 10)
    check("runners", runners["all_built_tested_used"] is True and runners["valid_runner_count"] == 10)
    check(
        "global_install",
        install["all_valid"] is True
        and install["valid_skill_count"] == 10
        and install["existing_skill_replaced"] is False
        and install["plugin_cache_mutated"] is False
        and all(row["valid"] and row["hash_mismatch_count"] == 0 for row in install["rows"]),
    )
    check("cleanup", cleanup["count"] == 30 and cleanup["deletion_count"] == 0)
    check("prototypes", prototypes["count"] == 10 and prototypes["all_completed"] is True)
    check("latest_scan_count", scan["selected_file_count"] == 5000)
    check("latest_scan_head", scan["head"] == d.X1_FREEZE)
    check("latest_scan_files", scan["tracked_path_count"] == 64392)
    check("latest_scan_no_missing", scan["missing_path_count"] == 0)
    check("latest_scan_no_truncation", scan["truncated_file_count"] == 0)
    check("latest_scan_no_high_risk", scan["confirmed_high_risk_count"] == 0)
    check("latest_scan_bounded", scan["privacy_complete"] is False and scan["security_complete"] is False)
    check("route_prepared", route["state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")
    check("route_unsent", not route["task_lookup_performed"] and not route["message_sent"])
    check("route_ilyra", route["next_exact_title"] == "Ilyra Fen" and route["next_phase"] == "v659-v1")
    check(
        "route_auren",
        route["recipient_next_exact_title"] == "Auren Lark" and route["recipient_next_phase"] == "v659-v2",
    )
    check("tavian_standby", route["tavian_sol_state"] == "ON_STANDBY")
    check("no_bulk_route", route["bulk_or_parallel_activation_authorized"] is False)
    check("privacy_five_classes", len(privacy["classes"]) == 5)
    check("privacy_zero_hits", privacy["hit_count"] == 0 and privacy["hits"] == [])
    check("privacy_boundary", privacy["privacy_complete"] is False and privacy["security_complete"] is False)
    check("baton_word_floor", word_count(baton) >= 10000)
    check("baton_prepared", "SENT_BY_LYREN_MOSS = false" in baton)
    check("baton_ilyra", "NEXT_EXACT_TITLE = Ilyra Fen" in baton)
    check("baton_auren", "RECIPIENT_NEXT_EXACT_TITLE = Auren Lark" in baton)
    check("baton_stage20", "TERMINAL_VERDICT = NOT_READY_FOR_STAGE_20" in baton)
    check("baton_dossiers", baton.count("### ") >= 40)
    check("baton_no_private_paths", "C:\\Users\\" not in baton and "D:\\GHC-Archives\\" not in baton)
    check("baton_no_delegation_markup", "codex_delegation" not in baton)
    check("baton_no_trailing_whitespace", all(line == line.rstrip() for line in baton.splitlines()))
    check(
        "baton_no_raw_uuid",
        re.search(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", baton) is None,
    )
    check("document_cap", documents["passes"] is True and documents["activation_packet_words"] >= 10000)
    check("expected_paths", staged["valid"] is True and staged["expected_staged_path_count"] == len(staged["expected_staged_paths"]))
    check("no_expected_deletions", staged["deletions"] == [] and staged["x1_or_x2_changed_paths"] == [])

    for manifest_name in ["validation/final-delta-manifest.json", "final/final-owner-manifest.json"]:
        manifest = load(manifest_name)
        ok = manifest["entry_count"] == len(manifest["entries"])
        for row in manifest["entries"]:
            path = ROOT / row["path"]
            ok = ok and path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"]
        check(f"manifest_replay:{manifest_name}", ok)

    surface_counts = Counter(path.parent.name for path in (PHASE / "surfaces").glob("*/contract.json"))
    check("forty_surface_directories", len(surface_counts) == 40)
    check("canonical_not_run", load("validation/canonical-pass-plan.json")["state"] == "NOT_RUN_FINAL_CANDIDATE_REQUIRED")

    return {
        "schema": "ghc.family.v658-v8-2-remaster.detailed-validation.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "check_count": len(checks) + len(errors),
        "passed_count": len(checks),
        "error_count": len(errors),
        "checks": checks,
        "errors": errors,
        "valid": not errors,
        "boundary": "Same-owner repository workflow validation only; not independent reproduction or broader assurance.",
    }


if __name__ == "__main__":
    result = validate_phase()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)
