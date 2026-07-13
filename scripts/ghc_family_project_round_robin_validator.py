#!/usr/bin/env python3
"""Validate the bounded v642-v3 project-aware round-robin packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(phase: Path, allow_pending_snapshot: bool = False, require_report: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "pass": bool(condition), "detail": detail})

    required = [
        "x1-proposals.json",
        "sources/source-ledger.json",
        "provenance/prior-proposal-collision-audit.json",
        "provenance/frozen-chain-proposal-index.json",
        "workflow/project-context-capability-register.json",
        "workflow/route-state-machine.json",
        "workflow/project-boundary-mutation-vectors.json",
        "workflow/six-seat-round-robin.json",
        "workflow/scheduler-test-vectors.json",
        "workflow/terminal-horizon-receipt.json",
        "security/permission-envelope-model.json",
        "security/least-authority-vectors.json",
        "security/effective-authority-receipt.json",
        "physics/sector-exchange-current-contract.json",
        "physics/bianchi-residual-vectors.json",
        "physics/gmut-claim-boundary.json",
        "empirical/synthetic-calibration-contract.json",
        "empirical/calibration-vectors.json",
        "empirical/calibration-claim-boundary.json",
        "thos/cluster-randomized-protocol.json",
        "thos/multiplicity-sequential-budget.json",
        "thos/cluster-mutation-vectors.json",
        "thos/real-arm-gap.json",
        "freed-id/key-status-holder-state-machine.json",
        "freed-id/revocation-race-vectors.json",
        "freed-id/production-boundary.json",
        "cbr/delegated-authority-sunset-register.json",
        "cbr/intergenerational-appeal-vectors.json",
        "cbr/authority-legitimacy-gate.json",
        "thermo-psyche/entropy-category-map.json",
        "thermo-psyche/intervention-ladder.json",
        "thermo-psyche/non-equivalence-vectors.json",
        "thermo-psyche/law-claim-boundary.json",
        "stage20/evidence-escrow-ledger.json",
        "stage20/route-evidence-separation-vectors.json",
        "stage20/independent-reproduction-reservation.json",
        "stage20/terminal-verdict.json",
        "reproduction/cross-owner-lineage-replay.json",
        "reproduction/environment-perturbation-receipt.json",
        "reproduction/independent-team-gap.json",
        "reproduction/semantic-normalization-manifest.json",
        "reproduction/manifest.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "complete-incomplete-checklist.json",
        "tooling/executed-toolchain.json",
        "validation/execution-negative-log.json",
        "wellbeing-check.md",
        "v642-v3-integrated-overview.md",
    ]
    missing = [rel for rel in required if not (phase / rel).is_file()]
    check("all required core artifacts exist", not missing, missing)
    if missing:
        issues = [row for row in checks if not row["pass"]]
        return {
            "schema": "ghc.family.project-round-robin-validation.v1",
            "valid": False,
            "check_count": len(checks),
            "pass_count": len(checks) - len(issues),
            "issue_count": len(issues),
            "issues": issues,
            "checks": checks,
        }

    x1 = load(phase / "x1-proposals.json")
    source = load(phase / "sources/source-ledger.json")
    collision = load(phase / "provenance/prior-proposal-collision-audit.json")
    chain = load(phase / "provenance/frozen-chain-proposal-index.json")
    context = load(phase / "workflow/project-context-capability-register.json")
    fsm = load(phase / "workflow/route-state-machine.json")
    project_vectors = load(phase / "workflow/project-boundary-mutation-vectors.json")
    schedule = load(phase / "workflow/six-seat-round-robin.json")
    schedule_vectors = load(phase / "workflow/scheduler-test-vectors.json")
    horizon = load(phase / "workflow/terminal-horizon-receipt.json")
    permission = load(phase / "security/permission-envelope-model.json")
    authority_vectors = load(phase / "security/least-authority-vectors.json")
    authority_receipt = load(phase / "security/effective-authority-receipt.json")
    physics = load(phase / "physics/sector-exchange-current-contract.json")
    bianchi = load(phase / "physics/bianchi-residual-vectors.json")
    gmut_boundary = load(phase / "physics/gmut-claim-boundary.json")
    calibration_contract = load(phase / "empirical/synthetic-calibration-contract.json")
    calibration = load(phase / "empirical/calibration-vectors.json")
    calibration_boundary = load(phase / "empirical/calibration-claim-boundary.json")
    thos_protocol = load(phase / "thos/cluster-randomized-protocol.json")
    multiplicity = load(phase / "thos/multiplicity-sequential-budget.json")
    thos_vectors = load(phase / "thos/cluster-mutation-vectors.json")
    thos_gap = load(phase / "thos/real-arm-gap.json")
    freed_machine = load(phase / "freed-id/key-status-holder-state-machine.json")
    freed_vectors = load(phase / "freed-id/revocation-race-vectors.json")
    freed_boundary = load(phase / "freed-id/production-boundary.json")
    sunset = load(phase / "cbr/delegated-authority-sunset-register.json")
    appeals = load(phase / "cbr/intergenerational-appeal-vectors.json")
    cbr_gate = load(phase / "cbr/authority-legitimacy-gate.json")
    entropy = load(phase / "thermo-psyche/entropy-category-map.json")
    ladder = load(phase / "thermo-psyche/intervention-ladder.json")
    entropy_vectors = load(phase / "thermo-psyche/non-equivalence-vectors.json")
    law_boundary = load(phase / "thermo-psyche/law-claim-boundary.json")
    escrow = load(phase / "stage20/evidence-escrow-ledger.json")
    stage_vectors = load(phase / "stage20/route-evidence-separation-vectors.json")
    reservation = load(phase / "stage20/independent-reproduction-reservation.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
    replay = load(phase / "reproduction/cross-owner-lineage-replay.json")
    perturb = load(phase / "reproduction/environment-perturbation-receipt.json")
    independent = load(phase / "reproduction/independent-team-gap.json")
    manifest = load(phase / "reproduction/semantic-normalization-manifest.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    tooling = load(phase / "tooling/executed-toolchain.json")
    execution_negatives = load(phase / "validation/execution-negative-log.json")

    required_fields = {
        "hypothesis",
        "null_or_failure",
        "approval_class",
        "execution_lane",
        "authoritative_source_needs",
        "deliverables",
        "test_falsifier_or_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
        "novelty_against_prior_chain",
    }
    check("x1 has exactly ten proposals", x1["proposal_count"] == len(x1["proposals"]) == 10)
    check("x1 proposal ids unique", len({row["proposal_id"] for row in x1["proposals"]}) == 10)
    check("x1 preregistration fields complete", all(required_fields <= set(row) for row in x1["proposals"]))
    check("four truth labels exact", x1["outcome_classes"] == ["completed", "represented", "open_gap", "exact_gate"])
    check("x1 expected distribution exact", Counter(row["expected_disposition"] for row in x1["proposals"]) == Counter(EXPECTED))
    check("x1 expectations are not results", x1["expected_counts_are_results"] is False)
    check("x2 has ten outcomes", x2["proposal_count"] == len(x2["proposals"]) == 10)
    check("x2 distribution exact", x2["disposition_counts"] == EXPECTED)
    check("x2 preserves expected and observed", all({"expected_disposition", "observed_disposition"} <= set(row) for row in x2["proposals"]))
    check("all proposals executed within evidence", x2["all_executed_as_far_as_evidence_permits"] and all(row["executed_as_far_as_evidence_permits"] for row in x2["proposals"]))

    check("effective source count 46", source["effective_source_count"] == source["inherited_source_count"] + source["added_source_count"] == 46)
    check("effective source status counts sum", sum(source["effective_status_counts"].values()) == 46)
    check("draft and watch remain distinct", source["effective_status_counts"]["draft"] == 3 and source["effective_status_counts"]["watch"] == 1)
    check("collision audit covers 90", collision["prior_phase_counts"]["total"] == 90)
    check("zero exact title collisions", collision["exact_title_collisions"] == 0)
    check("semantic novelty reviewed", collision["semantic_delta_review_passed"] is True)
    check("lexical score is not semantic proof", collision["method"]["lexical_score_is_semantic_proof"] is False)
    check("chain contains 100 records", chain["proposal_count"] == len(chain["records"]) == 100)
    check("chain contains v642-v3 ten", chain["version_counts"]["v642-v3"] == 10 and sum(chain["version_counts"].values()) == 100)
    check("chain titles unique", len({row["title"] for row in chain["records"]}) == 100)

    check("one active saved-project owner", len(context["active"]) == 1 and context["active"][0]["route_state"] == "ACTIVE")
    check("next existing task planned not sent", context["planned_existing"][0]["route_state"] == "PLANNED_NOT_SENT")
    check("future seats not existing", all(row["exists"] is False for row in context["future_not_existing"]))
    check("projectless lanes standby", {row["task_label"] for row in context["standby_projectless"]} == {"Elian Voss", "Nima Calder"} and all(row["route_state"] == "STANDBY" for row in context["standby_projectless"]))
    check("capabilities do not inherit", context["capability_inheritance_across_tasks"] is False)
    check("no tasks created in phase", context["task_creation_by_this_phase"] == 0)
    check("no preterminal outbound messages", context["outbound_messages_before_terminal_validation"] == 0)
    check("route states separate prepared and sent", fsm["prepared_is_sent"] is False and "SENT" in fsm["states"])
    check("artifact cannot send", fsm["repository_artifact_can_send_message"] is False)
    check("project mutations reject five", project_vectors["invalid_vectors_rejected"] == 5)
    check("zero raw task identifiers", project_vectors["raw_task_identifiers"] == 0)

    assignments = schedule["assignments"]
    check("six seats exact", len(schedule["seats"]) == 6)
    check("150 assignments exact", schedule["assignment_count"] == len(assignments) == 150)
    check("schedule starts v642-v3", assignments[0]["phase_id"] == "v642-v3" and assignments[0]["owner"] == "Eiren Kestrel")
    check("schedule ends v660-v8", assignments[-1]["phase_id"] == "v660-v8" and assignments[-1]["terminal"] is True)
    check("phase domain one through eight", all(1 <= row["phase"] <= 8 for row in assignments))
    check("no v9 permitted", schedule["v9_permitted"] is False and horizon["v9_rows"] == 0)
    check("one terminal row", horizon["terminal_rows"] == 1)
    check("post terminal not authorized", horizon["post_terminal_authorized"] is False)
    check("scheduler rejects six invalid vectors", schedule_vectors["invalid_vectors_rejected"] == 6)

    check("permissions compose by intersection", permission["composition"] == "intersection" and permission["permission_union_allowed"] is False)
    check("deny and exact gate precedence", permission["deny_precedence"] is True and permission["exact_gate_precedence"] is True)
    check("broad trust not exact authority", permission["broad_trust_satisfies_exact_gate"] is False)
    check("one bounded authority allow", authority_vectors["allowed_count"] == 1)
    check("five authority rejects", authority_vectors["rejected_count"] == 5)
    check("owned write only", authority_receipt["owned_write_allowed"] is True and authority_receipt["sibling_write_allowed"] is False)
    check("no elevation or host change", authority_receipt["elevation"] is False and authority_receipt["host_security_changed"] is False)
    check("security scope not exhaustive", authority_receipt["exhaustive_security"] is False)

    check("physics model class bounded", physics["model_class"] == "typed scalar-tensor EFT research scaffold")
    check("exchange antisymmetry required", physics["pair_exchange_antisymmetry_required"] is True)
    check("physics not empirically confirmed", physics["empirically_confirmed"] is False)
    check("Bianchi two invalid vectors rejected", bianchi["invalid_vectors_rejected"] == 2)
    check("Bianchi valid vector accepted", bianchi["vectors"][0]["accepted"] is True)
    check("Bianchi invalid vectors fail", not any(row["accepted"] for row in bianchi["vectors"][1:]))
    check("zero real likelihoods", gmut_boundary["real_measurement_rows"] == gmut_boundary["likelihoods_executed"] == 0)
    check("GMUT protected claims false", not any(gmut_boundary[key] for key in ["detected_force", "unique_prediction", "empirical_gmut_confirmation", "theory_of_everything", "proof_or_canon"]))

    check("calibration is synthetic", calibration_contract["mode"] == "deterministic_synthetic_only")
    check("calibration has zero real rows", calibration_contract["real_measurement_rows"] == 0 and calibration_contract["network_download"] is False)
    check("calibration common mode disclosed", calibration_contract["shared_generator_evaluator_common_mode_possible"] is True)
    check("calibration classifications correct", calibration["expected_classifications_correct"] is True)
    check("only balanced calibration passes", [row["passes_bounded_uniformity_fixture"] for row in calibration["vectors"]] == [True, False, False])
    check("calibration disposition represented", calibration_boundary["disposition"] == "represented")
    check("calibration has no real fit", calibration_boundary["real_measurement_rows"] == calibration_boundary["real_likelihoods"] == calibration_boundary["real_fits"] == 0)
    check("calibration not empirical confirmation", calibration_boundary["empirical_gmut_confirmation"] is False)

    check("THOS protocol only", thos_protocol["mode"] == "protocol_only")
    check("THOS cluster unit declared", thos_protocol["allocation_unit"] == "agent_session_cluster" and thos_protocol["intracluster_correlation_required"] is True)
    check("THOS zero real clusters and arms", thos_protocol["real_clusters"] == thos_protocol["real_arm_runs"] == 0)
    check("alpha spending exact", math_isclose(sum(multiplicity["alpha_spending"]), multiplicity["familywise_alpha"]))
    check("post hoc outcomes forbidden", multiplicity["post_hoc_outcomes_allowed"] is False)
    check("THOS six mutations rejected", thos_vectors["mutations_rejected"] == len(thos_vectors["vectors"]) == 6)
    check("THOS gap exact", thos_gap["state"] == "open_gap" and thos_gap["real_arm_runs"] == 0)
    check("THOS protected claims false", not any(thos_gap[key] for key in ["superiority_established", "agi", "asi", "consciousness", "personhood"]))

    check("Freed ID synthetic only", freed_machine["mode"] == "synthetic_structural_only")
    check("Freed ID revocation precedence", freed_machine["revocation_precedence"] is True)
    check("Freed ID zero crypto operations", freed_machine["real_cryptographic_operations"] == 0)
    check("Freed ID one synthetic accept", freed_vectors["synthetic_accepts"] == 1)
    check("Freed ID six synthetic rejects", freed_vectors["synthetic_rejections"] == 6)
    check("Freed ID disposition represented", freed_boundary["disposition"] == "represented")
    check("Freed ID production counts zero", all(freed_boundary[key] == 0 for key in ["real_keys", "real_proofs", "live_resolvers", "live_status_or_revocation_services", "interoperability_partners", "independent_security_reviews"]))
    check("Freed ID assurance false", freed_boundary["privacy_assurance"] is False and freed_boundary["trust_governance_established"] is False and freed_boundary["cryptographic_assurance"] is False)

    check("CBR expires to defer", sunset["default_on_expiry"] == "defer" and sunset["silent_renewal_allowed"] is False)
    check("CBR cannot appoint representative", sunset["system_may_appoint_representative"] is False)
    check("Māori authority nontransferable", sunset["maori_authority_nontransferable"] is True)
    check("all appeal vectors defer", appeals["all_defer"] is True)
    check("all remedies preserved", appeals["all_remedies_preserved"] is True)
    check("CBR exact gate", cbr_gate["state"] == "exact_gate")
    check("CBR authorities absent", not any(cbr_gate[key] for key in ["affected_party_authority_present", "future_generation_authorized_representative_present", "maori_authority_present", "cultural_ratification_present", "competent_legal_authority_present", "enacted_law"]))
    check("CBR exact Māori boundary", "Māori authority" in cbr_gate["boundary"])

    categories = {row["name"] for row in entropy["categories"]}
    check("entropy categories distinct", {"thermodynamic_entropy", "shannon_entropy", "computational_erasure_cost", "psychological_uncertainty"} <= categories)
    check("entropy automatic equivalence false", entropy["automatic_equivalence"] is False)
    check("telemetry not experience", entropy["telemetry_is_subjective_experience"] is False)
    check("intervention ladder has seven levels", len(ladder["levels"]) == 7)
    check("temporal precedence not causation", ladder["temporal_precedence_alone_proves_causation"] is False)
    check("zero real interventions", ladder["real_intervention_runs"] == 0)
    check("six invalid entropy equivalences rejected", entropy_vectors["invalid_equivalences_rejected"] == 6)
    check("thermo psyche protected claims false", not any(law_boundary[key] for key in ["fundamental_law_established", "consciousness_tensor", "consciousness", "personhood", "empirical_confirmation"]))

    check("route is not science", escrow["route_receipt_is_scientific_evidence"] is False)
    check("exact gates not scoreable", escrow["technical_score_may_override_exact_gate"] is False)
    check("stage vectors reject five", stage_vectors["invalid_vectors_rejected"] == 5)
    check("independent reservation open", reservation["state"] == "open")
    check("same-owner snapshots do not satisfy independent", reservation["same_owner_snapshots_satisfy"] is False)
    check("route success does not satisfy independent", reservation["route_success_satisfies"] is False)
    check("terminal not ready", terminal["verdict"] == "NOT_READY_FOR_STAGE_20")
    check("deployment not authorized", terminal["deployment_authorized"] is False and terminal["successor_authorized_by_artifact"] is False)

    check("96 negatives retained", negatives["negative_count"] == len(negatives["negatives"]) == 96)
    check("negative inheritance exact", negatives["inherited_count"] == 68 and negatives["new_count"] == 28)
    check("all negatives retained", negatives["all_retained"] is True and all(row["retained"] for row in negatives["negatives"]))
    check("negative erasure forbidden", negatives["erasure_permitted"] is False)
    check("eight execution failures retained", execution_negatives["negative_count"] == 8 and [row["negative_id"] for row in execution_negatives["negatives"]] == ["V6423-N21", "V6423-N22", "V6423-N23", "V6423-N24", "V6423-N25", "V6423-N26", "V6423-N27", "V6423-N28"] and all(row["preserved"] for row in execution_negatives["negatives"]))
    check("five open gaps", gates["open_gap_count"] == 5)
    check("six exact gates", gates["exact_gate_count"] == 6)
    check("no gate silently closed", gates["silently_closed"] == 0 and all(row["state"] in {"open", "deferred"} for row in gates["gates"]))
    check("phase truth distribution exact", truth["disposition_counts"] == EXPECTED)
    check("phase truth negatives exact", truth["retained_negative_count"] == 96)
    check("phase truth protected claims false", not any(truth["protected_claims"].values()))
    check("phase truth terminal exact", truth["terminal_verdict"] == terminal["verdict"] == "NOT_READY_FOR_STAGE_20")
    check("projectless lanes preserved standby", truth["projectless_lanes_on_standby"] == ["Elian Voss", "Nima Calder"])

    snapshot_verified = (
        x2["snapshot_state"] == "verified"
        and truth["same_owner_repeatability"] == "verified_bounded"
        and perturb["state"] == "verified"
        and replay["current_same_owner_snapshots"] == "verified_bounded"
    )
    check("snapshot state acceptable", snapshot_verified or allow_pending_snapshot, x2["snapshot_state"])
    check("independent team absent", reservation["independent_team_present"] is False and independent["independent_team_present"] is False and replay["independent_team_reproduction"] is False)
    check("independent gap open", truth["independent_team_gap"] == independent["state"] == "open")
    check("inherited tools unchanged by plan", tooling["inherited_tools_modified"] is False)

    mismatches = [
        rel for rel, expected in manifest["hashes"].items()
        if not (phase / rel).is_file() or digest(phase / rel) != expected
    ]
    check("manifest count matches", manifest["artifact_count"] == len(manifest["hashes"]))
    check("manifest hashes match", not mismatches, mismatches)
    aggregate = hashlib.sha256(
        "".join(f"{rel}:{manifest['hashes'][rel]}\n" for rel in sorted(manifest["hashes"])).encode("utf-8")
    ).hexdigest()
    check("manifest aggregate matches", aggregate == manifest["aggregate_sha256"])
    check("manifest has no absolute paths", manifest["absolute_paths_required"] is False)
    check("manifest independent claim false", manifest["independent_team_reproduction"] is False)

    overview = (phase / "v642-v3-integrated-overview.md").read_text(encoding="utf-8")
    word_count = len(re.findall(r"\b\w+[\w'-]*\b", overview))
    check("overview is three-page equivalent", word_count >= 1800, word_count)
    for phrase in [
        "NOT_READY_FOR_STAGE_20",
        "Māori authority",
        "zero real THOS",
        "independent scientific",
        "not a complete WCAG conformance assessment",
    ]:
        check(f"overview contains boundary: {phrase}", phrase in overview)

    report = phase / "deliverables/v642-v3-project-round-robin-report.html"
    check("report exists when required", report.is_file() or not require_report)
    if report.is_file():
        html = report.read_text(encoding="utf-8")
        for token in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
            check(f"report contains structural token {token}", token in html)
        check("report accessibility claim bounded", "not a complete WCAG conformance assessment" in html)

    issues = [row for row in checks if not row["pass"]]
    return {
        "schema": "ghc.family.project-round-robin-validation.v1",
        "valid": not issues,
        "check_count": len(checks),
        "pass_count": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "summary": {
            "proposals": 10,
            "disposition_counts": EXPECTED,
            "retained_negatives": 96,
            "open_gaps": 5,
            "exact_gates": 6,
            "schedule_assignments": 150,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "checks": checks,
    }


def math_isclose(left: float, right: float) -> bool:
    return abs(left - right) <= 1e-12


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    result = validate(phase, args.allow_pending_snapshot, args.require_report)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else phase / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
