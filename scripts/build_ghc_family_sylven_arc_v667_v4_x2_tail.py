#!/usr/bin/env python3
"""Compose the unwritten v667-v4 x2 tail after isolated version recovery."""

from __future__ import annotations

import sys

from build_ghc_family_sylven_arc_v667_v4_x2 import (
    INHERITED_EXACT_GATES,
    INHERITED_METHODS,
    INHERITED_NEGATIVES,
    INHERITED_OPEN_GAPS,
    NOW,
    OWNER,
    PHASE,
    SOURCE_SHA,
    X1_SHA,
    X2_OPERATIONAL_FAILURES,
    accessible_report,
    build_method_flow,
    load,
    write_json,
    write_text,
)


def compose_tail() -> None:
    outcomes_doc = load("x2/proposal-outcomes.json")
    mutations_doc = load("x2/rejecting-mutations.json")
    portfolio = load("x2/portfolio-execution.json")
    registry = load("x2/skill-runner-registry.json")
    flashcards = load("x2/flashcards/execution-receipts.json")
    deck_mutations = load("x2/flashcards/mutation-receipt.json")
    counts = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    if outcomes_doc["counts"] != counts or len(mutations_doc["mutations"]) != 100:
        raise RuntimeError("retained x2 prefix differs")
    if portfolio["executed_count"] != 95 or portfolio["held_count"] != 100:
        raise RuntimeError("retained portfolio prefix differs")
    if deck_mutations["mutation_count"] != 60 or deck_mutations["rejected_count"] != 60:
        raise RuntimeError("retained flashcard mutation prefix differs")
    if flashcards["build"]["passed"] is not True or flashcards["validate"]["passed"] is not True:
        raise RuntimeError("retained flashcard recovery differs")

    method_flow = build_method_flow(outcomes_doc["outcomes"], mutations_doc["mutations"], deck_mutations["cases"], portfolio)
    if not method_flow["valid"]:
        raise RuntimeError("updated Method Flow accounting mismatch")
    write_json("method-flow/x2-method-flow-ledger.json", method_flow)

    startup = load("method-flow/startup-method-flow.json")
    negative_rows = [
        {"negative_id": row["failure_id"], "class": "x1_owner_operational_failure", "credit": 0, "retained": True, "failure": row["failure"]}
        for row in startup["failed_witnesses"]
    ]
    negative_rows.extend(
        {"negative_id": row["failure_id"], "class": "x2_owner_operational_failure", "credit": 0, "retained": True, "failure": row["failure"]}
        for row in X2_OPERATIONAL_FAILURES
    )
    negative_rows.extend(
        {"negative_id": row["mutation_id"], "class": "proposal_rejecting_mutation", "credit": 0, "retained": True, "validator_failures": row["validator_failures"]}
        for row in mutations_doc["mutations"]
    )
    negative_rows.extend(
        {"negative_id": row["mutation_id"], "class": "flashcard_rejecting_mutation", "credit": 0, "retained": True, "issues": row["issues"]}
        for row in deck_mutations["cases"]
    )
    retained = {
        "schema": "ghc-family-retained-negative-register-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_repository_and_external_activation_count": INHERITED_NEGATIVES,
        "phase_additive_count": len(negative_rows), "effective_count": INHERITED_NEGATIVES + len(negative_rows),
        "rows": negative_rows, "failure_erased_count": 0,
    }
    if retained["phase_additive_count"] != 195 or retained["effective_count"] != 27532:
        raise RuntimeError("updated negative accounting mismatch")
    write_json("evidence/retained-negative-register.json", retained)

    evidence = load("evidence/immutable-evidence-candidate.json")
    evidence.update({
        "effective_negatives": retained["effective_count"],
        "effective_methods": method_flow["effective_method_count"],
        "validation_state": "VALID_TWO_STAGE_DEPENDENCY_CORRECTED_X2_COMPOSITE_WITH_ZERO_FAILED_AGGREGATE_CREDIT",
    })
    write_json("evidence/immutable-evidence-candidate.json", evidence)

    write_json("environment/version-receipt.json", {
        "schema": "ghc-family-version-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "action": "verify_only_no_updates_or_installs",
        "initial_grouped_probe": {
            "status": "FAILED_RETAINED_ZERO_CREDIT", "failure_id": "SA6674-X2-F004",
            "python_git_node_observations": "completed_before_failure_but_values_not_durably_materialized_and_not_replayed",
            "codex_observation": "WinError 5 Access is denied", "aggregate_credit": 0,
        },
        "versions": [
            {"label": "python", "available": True, "version": sys.version.split()[0], "source": "running_interpreter_state_not_a_replayed_subprocess", "action": "read_only_version_check"},
            {"label": "git", "available": True, "version": "observed_success_value_not_durably_materialized", "source": "retained_initial_grouped_probe", "action": "read_only_version_check"},
            {"label": "node", "available": True, "version": "observed_success_value_not_durably_materialized", "source": "retained_initial_grouped_probe", "action": "read_only_version_check"},
            {"label": "codex", "available": True, "version": "codex-cli 0.147.0", "source": "isolated codex.cmd --version recovery", "action": "read_only_version_check"},
        ],
        "codex_desktop_updated": False, "packages_installed": [], "sandbox_or_hyper_v_changed": False,
        "host_security_weakened": False, "rebooted": False,
    })
    write_json("wellbeing/x2-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "workload_state": "bounded_complete_for_two_stage_dependency_corrected_x2_evidence_candidate",
        "portfolio_execution_count": portfolio["executed_count"], "pause_and_stop_tokens_preserved": True,
        "exact_and_blocked_packets_executed": 0, "human_wellbeing_claim": False,
        "next_gate": "exact staged evidence review, commit, push and four-way equality",
    })
    write_json("validation/x2-failed-build-receipt.json", {
        "schema": "ghc-family-x2-failed-build-receipt-v1", "owner": OWNER, "phase": PHASE, "recorded_at_utc": NOW,
        "status": "FAILED_RETAINED_ZERO_CREDIT", "exit_code": 1, "successful_prefix_replayed": False,
        "failed_dependency": "flashcard compact_message successor label compatibility", "error_type": "KeyError", "error_key": "owner",
        "bounded_recovery": "owner-or-title successor label compatibility plus isolated resume from flashcard build",
    })
    write_json("validation/x2-failed-recovery-receipt.json", {
        "schema": "ghc-family-x2-failed-recovery-receipt-v1", "owner": OWNER, "phase": PHASE, "recorded_at_utc": NOW,
        "status": "FAILED_RETAINED_ZERO_CREDIT", "failure_id": "SA6674-X2-F004", "aggregate_credit": 0,
        "failed_dependency": "bare Codex executable version verification", "error": "WinError 5 Access is denied",
        "previously_successful_flashcard_and_evidence_components_replayed": False,
        "bounded_recovery": "codex.cmd --version returned codex-cli 0.147.0 once; only the unwritten receipt/report tail was resumed",
    })
    write_json("validation/x2-build-receipt.json", {
        "schema": "ghc-family-x2-build-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "contracts": 20, "proposal_mutations": 100, "flashcard_mutations": 60, "accepted_mutations": 0,
        "skills": 10, "runners": 10, "skill_smoke_passes": 10, "runner_smoke_passes": 10,
        "flashcard_commands_passed": 9, "portfolio_executions": portfolio["executed_count"],
        "method_flow_rows": method_flow["phase_method_count"], "failed_full_builder_credit": 0,
        "failed_recovery_credit": 0, "successful_prefix_replayed": False,
        "status": "VALID_TWO_STAGE_DEPENDENCY_CORRECTED_X2_COMPOSITE_WITH_ZERO_FAILED_AGGREGATE_CREDIT",
    })
    write_text("reports/accessible-report.html", accessible_report(evidence, flashcards))
    write_text("evidence/evidence-summary.md", f"""# Sylven Arc v667-v4 two-stage dependency-corrected evidence candidate

## Validation state

The complete x2 builder failed at the flashcard compact-message dependency and has zero aggregate credit. Its successful contract, mutation, skill, and runner prefix was not replayed. The first isolated recovery fixed and completed the flashcard dependency, then failed only at a bare Codex version probe; that recovery also has zero aggregate credit. `codex.cmd --version` passed once, and only this unwritten receipt/report tail was composed afterward.

## Four-label truth

Outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Verdict: `NOT_READY_FOR_STAGE_20`.

## Bounded contracts and mutations

Twenty synthetic neon-record contracts passed. One hundred preregistered proposal mutations and sixty flashcard mutations were rejected and retained at zero credit. No failure was erased.

## THOS Body

THOS Body is primary through typed record, stop, omission, topology, handover, and nonexecution contracts. No people, operators, governed real arms, outcomes, statistics, or independent review were used.

## GMUT Mind

GMUT remains a typed scalar-tensor/EFT obligation surface. Nothing here yields a force, prediction, likelihood, constraint, spectrum, colour, empirical confirmation, Theory-of-Everything proof, or canon.

## Freed ID and CBR Heart

Freed ID remains synthetic and zero-key. The modular deck contains {flashcards['build']['result']['card_count']} cards and thirteen sections, but establishes no measured cache effect, identity continuity, production credential, or trust authority.

## Bounded practice

The neon-signmaking and historic-neon documentation lens is synthetic learning/design only. No signmaking, glassworking, electrical, gas or mercury, lifting, preservation, safety, heritage, legal, cultural, affected-party, or Māori authority is claimed.

## Skills, runners, and portfolio

Ten phase-local skills and ten family-current owner runners were built and smoke-used without global installation. Ninety-five owner rows executed within structural scope; one hundred held rows remain recommendations or protected holds.

## Open and exact gates

The Smithsonian adapter remains zero-call and zero-row. Effective gaps are {INHERITED_OPEN_GAPS + 1}; effective exact gates are {INHERITED_EXACT_GATES + 1}. Māori concepts remain under Māori authority.

## Effective retention

This evidence candidate preserves {retained['effective_count']} negatives and {method_flow['effective_method_count']} methods. Same-owner evidence under shared infrastructure is not independent reproduction, external audit, complete privacy or accessibility assurance, or production certification.

## Next gate

Run the owner-local x2 module once, isolate failures if any, parse all phase JSON, stage only the evidence allowlist, verify exact Git-index manifests, commit, push, and prove fresh equality before closeout.
""")


if __name__ == "__main__":
    compose_tail()
