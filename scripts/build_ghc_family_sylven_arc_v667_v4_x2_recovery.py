#!/usr/bin/env python3
"""Resume Sylven v667-v4 only after the retained flashcard-build failure.

This recovery never replays the already successful contract, mutation, skill,
or owner-runner components of the failed x2 builder. It retries only the fixed
flashcard build dependency, runs later dependencies once, and composes the
dependency-corrected evidence candidate with zero aggregate credit.
"""

from __future__ import annotations

import json
import subprocess
import sys

from build_ghc_family_sylven_arc_v667_v4_x2 import (
    INHERITED_EXACT_GATES,
    INHERITED_METHODS,
    INHERITED_NEGATIVES,
    INHERITED_OPEN_GAPS,
    NOW,
    OWNER,
    OWNER_SLUG,
    PHASE,
    PHASE_ROOT,
    ROOT,
    RUNNER_FILES,
    SKILL_SPECS,
    SOURCE_SHA,
    X1_SHA,
    X2_OPERATIONAL_FAILURES,
    accessible_report,
    build_method_flow,
    execute_portfolios,
    git,
    load,
    run_json,
    version_row,
    write_json,
    write_text,
)
from ghc_family_sylven_arc_v667_v4_core import validate_contract


def verify_retained_prefix() -> tuple[list[dict], list[dict], dict, list[dict], list[dict]]:
    if git("rev-parse", "HEAD") != X1_SHA:
        raise RuntimeError("recovery requires the unchanged immutable x1 head")
    outcomes_doc = load("x2/proposal-outcomes.json")
    mutations_doc = load("x2/rejecting-mutations.json")
    registry = load("x2/skill-runner-registry.json")
    outcomes = outcomes_doc["outcomes"]
    mutations = mutations_doc["mutations"]
    if outcomes_doc["counts"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("retained outcome prefix differs")
    if len(outcomes) != 20 or len(mutations) != 100 or any(row["accepted"] for row in mutations):
        raise RuntimeError("retained contract or mutation prefix differs")
    for outcome in outcomes:
        contract = load(f"x2/proposals/{outcome['proposal_id'].casefold()}/contract.json")
        if validate_contract(contract):
            raise RuntimeError(f"retained positive contract differs: {outcome['proposal_id']}")
    runner_smokes = [load(f"x2/runner-smoke/{kind}.json") for kind in RUNNER_FILES]
    skill_smokes = [load(f"x2/skill-smoke/{name}.json") for name, _, _ in SKILL_SPECS]
    if registry["skill_count"] != 10 or registry["runner_count"] != 10:
        raise RuntimeError("retained skill-runner registry differs")
    if not all(row["passed"] for row in runner_smokes + skill_smokes):
        raise RuntimeError("retained skill or runner smoke differs")
    return outcomes, mutations, registry, runner_smokes, skill_smokes


def recover() -> None:
    outcomes, all_mutations, registry, runner_smokes, skill_smokes = verify_retained_prefix()
    counts = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    flashcard = ROOT / "scripts" / "ghc_family_freed_id_flashcards.py"
    base = [sys.executable, str(flashcard)]
    phase_root_rel = f"docs/{OWNER_SLUG}/{PHASE}"
    deck_rel = f"{phase_root_rel}/deck"
    flashcard_receipts: dict[str, dict] = {
        "prebuild_smoke": {"schema": "ghc.family.freed-id-flashcards.v1.smoke", "valid": True, "card_count": 233, "section_count": 13, "new_core_outcomes": counts, "executed_once_before_build": True, "replayed": False},
        "failed_build": {
            "status": "FAILED_RETAINED_ZERO_CREDIT",
            "exit_code": 1,
            "failed_dependency": "compact_message successor label compatibility",
            "error_type": "KeyError",
            "error_key": "owner",
            "successful_prefix_replayed": False,
            "credit": 0,
        },
    }
    flashcard_receipts["build"] = run_json(base + ["build", "--repo", str(ROOT), "--phase-root", phase_root_rel, "--output-dir", deck_rel, "--x1", X1_SHA])
    for command in ("validate", "manifest", "graph", "privacy", "render-html", "diff", "compact-message", "mutations"):
        flashcard_receipts[command.replace("-", "_")] = run_json(base + [command, "--repo", str(ROOT), "--deck-dir", deck_rel])
    for command in ("build", "validate", "manifest", "graph", "privacy", "render_html", "diff", "compact_message", "mutations"):
        if flashcard_receipts[command].get("passed") is not True:
            raise RuntimeError(f"recovered flashcard dependency failed: {command}")
    deck_mutation_result = flashcard_receipts["mutations"]["result"]
    if deck_mutation_result["mutation_count"] != 60 or deck_mutation_result["rejected_count"] != 60:
        raise RuntimeError("flashcard mutation count mismatch")
    write_json("x2/flashcards/execution-receipts.json", flashcard_receipts)
    write_json("x2/flashcards/mutation-receipt.json", deck_mutation_result)

    portfolio_execution = execute_portfolios(load("x1/portfolio-freeze.json"))
    if portfolio_execution["executed_count"] != 95 or portfolio_execution["held_count"] != 100:
        raise RuntimeError("portfolio execution partition mismatch")
    write_json("x2/portfolio-execution.json", portfolio_execution)

    method_flow = build_method_flow(outcomes, all_mutations, deck_mutation_result["cases"], portfolio_execution)
    if not method_flow["valid"]:
        raise RuntimeError("Method Flow accounting mismatch")
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
        for row in all_mutations
    )
    negative_rows.extend(
        {"negative_id": row["mutation_id"], "class": "flashcard_rejecting_mutation", "credit": 0, "retained": True, "issues": row["issues"]}
        for row in deck_mutation_result["cases"]
    )
    retained = {
        "schema": "ghc-family-retained-negative-register-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_repository_and_external_activation_count": INHERITED_NEGATIVES,
        "phase_additive_count": len(negative_rows), "effective_count": INHERITED_NEGATIVES + len(negative_rows),
        "rows": negative_rows, "failure_erased_count": 0,
    }
    if retained["phase_additive_count"] != 195 or retained["effective_count"] != 27532:
        raise RuntimeError("negative accounting mismatch")
    write_json("evidence/retained-negative-register.json", retained)
    write_json("evidence/open-gap-register.json", {
        "schema": "ghc-family-open-gap-register-v5", "inherited_count": INHERITED_OPEN_GAPS, "new_count": 1, "effective_count": INHERITED_OPEN_GAPS + 1,
        "new_rows": [{"proposal_id": "SA6674-N019", "gap": "Smithsonian transport, schema materialization, rights review, provenance evaluation and collection assessment remain absent", "network_calls": 0, "rows": 0, "media": 0}],
    })
    write_json("evidence/exact-gate-register.json", {
        "schema": "ghc-family-exact-gate-register-v5", "inherited_count": INHERITED_EXACT_GATES, "new_count": 1, "effective_count": INHERITED_EXACT_GATES + 1,
        "new_rows": [{"proposal_id": "SA6674-N020", "gate": "neon labour, flame, gas and mercury, high voltage, lifting, public safety, ownership, advertising, heritage, accessibility, light pollution, privacy, remedy, legal, cultural, affected-party and Māori authority", "executed": False}],
    })
    evidence = {
        "schema": "ghc-family-immutable-evidence-candidate-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "source_head": SOURCE_SHA, "frozen_x1": X1_SHA, "proposal_outcomes": counts,
        "positive_contracts": len(outcomes), "proposal_rejecting_mutations": len(all_mutations), "flashcard_rejecting_mutations": deck_mutation_result["mutation_count"], "accepted_mutations": 0,
        "owner_portfolio_executions": portfolio_execution["executed_count"], "held_portfolio_rows": portfolio_execution["held_count"],
        "phase_local_skills_built_and_smoke_used": registry["skill_smoke_passes"], "family_current_runners_built_and_smoke_used": registry["runner_smoke_passes"], "global_install_count": 0,
        "flashcard_cards": flashcard_receipts["build"]["result"]["card_count"], "flashcard_sections": flashcard_receipts["build"]["result"]["section_count"],
        "real_people": 0, "real_objects": 0, "real_measurements": 0, "network_calls": 0, "keys": 0, "proofs": 0, "external_actions": 0,
        "effective_negatives": retained["effective_count"], "effective_methods": method_flow["effective_method_count"],
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "validation_state": "VALID_DEPENDENCY_CORRECTED_X2_COMPOSITE_WITH_ZERO_FAILED_BUILDER_CREDIT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "same_owner_only": True,
    }
    write_json("evidence/immutable-evidence-candidate.json", evidence)
    write_json("environment/version-receipt.json", {
        "schema": "ghc-family-version-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "action": "verify_only_no_updates_or_installs",
        "versions": [version_row("python", [sys.executable, "--version"]), version_row("git", ["git", "--version"]), version_row("node", ["node", "--version"]), version_row("codex", ["codex", "--version"])],
        "codex_desktop_updated": False, "packages_installed": [], "sandbox_or_hyper_v_changed": False, "host_security_weakened": False, "rebooted": False,
    })
    write_json("wellbeing/x2-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "workload_state": "bounded_complete_for_dependency_corrected_x2_evidence_candidate", "portfolio_execution_count": portfolio_execution["executed_count"],
        "pause_and_stop_tokens_preserved": True, "exact_and_blocked_packets_executed": 0, "human_wellbeing_claim": False,
        "next_gate": "exact staged evidence review, commit, push and four-way equality",
    })
    write_json("validation/x2-failed-build-receipt.json", {
        "schema": "ghc-family-x2-failed-build-receipt-v1", "owner": OWNER, "phase": PHASE, "recorded_at_utc": NOW,
        "status": "FAILED_RETAINED_ZERO_CREDIT", "exit_code": 1, "successful_prefix_replayed": False,
        "failed_dependency": "flashcard compact_message successor label compatibility", "error_type": "KeyError", "error_key": "owner",
        "bounded_recovery": "owner-or-title successor label compatibility plus isolated resume from flashcard build",
    })
    write_json("validation/x2-build-receipt.json", {
        "schema": "ghc-family-x2-build-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "contracts": 20, "proposal_mutations": 100, "flashcard_mutations": 60, "accepted_mutations": 0,
        "skills": 10, "runners": 10, "skill_smoke_passes": 10, "runner_smoke_passes": 10, "flashcard_commands_passed": 9,
        "portfolio_executions": portfolio_execution["executed_count"], "method_flow_rows": method_flow["phase_method_count"],
        "failed_full_builder_credit": 0, "successful_prefix_replayed": False,
        "status": "VALID_DEPENDENCY_CORRECTED_X2_COMPOSITE_WITH_ZERO_FAILED_BUILDER_CREDIT",
    })
    write_text("reports/accessible-report.html", accessible_report(evidence, flashcard_receipts))
    write_text("evidence/evidence-summary.md", f"""# Sylven Arc v667-v4 dependency-corrected evidence candidate

## Validation state

The first x2 builder failed at the flashcard compact-message dependency and has zero aggregate credit. Twenty contracts, one hundred proposal mutations, ten skills, and ten runners had already completed; none was replayed. Only the corrected flashcard build was resumed, followed by its not-yet-run downstream checks.

## Four-label truth

Outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Verdict: `NOT_READY_FOR_STAGE_20`.

## Bounded contracts

Twenty synthetic neon-record contracts passed with zero people, objects, measurements, network rows, keys, proofs, external actions, or authority acts.

## Retained mutations

One hundred preregistered proposal mutations and sixty flashcard mutations were rejected and retained at zero credit. No failure was erased.

## THOS Body

THOS Body is primary through typed record, stop, omission, topology, handover, and nonexecution contracts. There are no participants, operators, governed real arms, outcomes, statistics, or independent review.

## GMUT Mind

GMUT remains a typed scalar-tensor/EFT obligation surface. Nothing here produces a force, spectrum, colour, prediction, likelihood, constraint, empirical confirmation, Theory-of-Everything proof, or canon.

## Freed ID and CBR Heart

Freed ID remains a zero-key synthetic component genealogy. The modular deck has {flashcard_receipts['build']['result']['card_count']} cards and thirteen sections. It measures neither cache effect nor identity continuity. CBR authority categories remain gated.

## Skills, runners, and portfolio

Ten phase-local skills and ten family-current owner runners were built and smoke-used without global installation. Ninety-five owner rows executed within bounded structural scope; one hundred held rows remain recommendations or protected holds.

## Open and exact gates

The Smithsonian adapter remains zero-call and zero-row. Professional, safety, heritage, legal, cultural, affected-party, Māori wording, Māori concepts, Māori data governance, and Māori authority remain open or exact-gated.

## Effective retention

This evidence candidate preserves {retained['effective_count']} negatives, {method_flow['effective_method_count']} methods, {INHERITED_OPEN_GAPS + 1} open gaps, and {INHERITED_EXACT_GATES + 1} exact gates. Same-owner evidence is not independent reproduction or external audit.

## Next gate

Run exact owner-local tests, parse every phase JSON file, stage the evidence allowlist, inspect Git-index manifests and privacy classes, commit, push, and prove fresh remote equality before closeout.
""")


if __name__ == "__main__":
    recover()
