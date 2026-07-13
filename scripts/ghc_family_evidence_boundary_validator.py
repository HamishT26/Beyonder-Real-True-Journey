#!/usr/bin/env python3
"""Validate reusable GHC evidence-boundary artifacts and protected gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


def load(phase_dir: Path, rel: str) -> dict[str, Any]:
    return json.loads((phase_dir / rel).read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(
    phase_dir: Path,
    *,
    allow_pending_snapshot: bool = True,
    require_report: bool = False,
    output: Path | None = None,
) -> dict[str, Any]:
    issues: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "pass": bool(condition), "detail": detail})
        if not condition:
            issues.append(name if detail is None else f"{name}: {detail}")

    x1 = load(phase_dir, "x1-proposals.json")
    ledger = load(phase_dir, "x2-proposal-ledger.json")
    truth = load(phase_dir, "phase-truth.json")
    source = load(phase_dir, "sources/source-ledger.json")
    negatives = load(phase_dir, "retained-negative-register.json")
    gates = load(phase_dir, "exact-open-gate-register.json")
    chain = load(phase_dir, "provenance/frozen-chain-proposal-index.json")

    required_proposal_fields = {
        "hypothesis", "null_or_failure", "approval_class", "execution_lane",
        "authoritative_source_needs", "deliverables", "test_falsifier_or_gate",
        "rollback_or_recovery", "protected_gates", "expected_disposition",
        "novelty_against_prior_chain",
    }
    check("x1 proposal count is ten", x1["proposal_count"] == len(x1["proposals"]) == 10)
    check("x1 proposal ids are unique", len({row["proposal_id"] for row in x1["proposals"]}) == 10)
    check("x1 required fields present", all(required_proposal_fields <= set(row) for row in x1["proposals"]))
    check("x1 source is exact v8 final head", x1["source_revision"] == "62f35540964e964760fdf10c7acf580f320dcd29")
    check("x2 references x1 commit", ledger["x1_commit"] == "4785eae506ec19152b282297e496ff7f0209fa2e")
    check("x2 source matches x1", ledger["source_revision"] == x1["source_revision"] == truth["source_revision"])

    expected_counts = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
    observed_counts = dict(Counter(row["observed_disposition"] for row in ledger["proposals"]))
    check("x2 proposal count is ten", ledger["proposal_count"] == len(ledger["proposals"]) == 10)
    check("all proposals executed as evidence permits", ledger["all_executed_as_far_as_evidence_permits"] and all(row["executed_as_far_as_evidence_permits"] for row in ledger["proposals"]))
    check("disposition counts exact", ledger["disposition_counts"] == observed_counts == expected_counts, observed_counts)
    check("phase truth disposition counts exact", truth["disposition_counts"] == expected_counts)
    check("x1 expected and x2 observed match without changing x1", x1["expected_disposition_counts"] == expected_counts and not x1["expected_counts_are_results"])

    source_ids = {row["source_id"] for row in source["sources"]}
    proposal_refs = {ref for proposal in x1["proposals"] for ref in proposal["authoritative_source_needs"]}
    source_counts = dict(Counter(row["status_class"] for row in source["sources"]))
    check("source count exact", source["source_count"] == len(source["sources"]) == 34)
    check("source statuses exact", source_counts == source["status_counts"] == {"current": 19, "stable": 11, "draft": 3, "watch": 1}, source_counts)
    check("all source references resolve", not (proposal_refs - source_ids), sorted(proposal_refs - source_ids))
    bbs = next(row for row in source["sources"] if row["source_id"] == "V6421-S33")
    check("BBS pin stays draft", bbs["status_class"] == "draft")

    check("frozen proposal chain has eighty", chain["proposal_count"] == len(chain["records"]) == 80)
    check("frozen proposal version counts", chain["version_counts"].get("v642-v1") == 10 and sum(chain["version_counts"].values()) == 80)
    check("frozen proposal titles have no exact duplicates", chain["exact_duplicate_titles"] == [])
    inheritance = load(phase_dir, "provenance/counterevidence-inheritance-vectors.json")
    context = load(phase_dir, "provenance/context-collision-matrix.json")
    partition = load(phase_dir, "provenance/source-independence-partition.json")
    check("counterevidence mutations all rejected", inheritance["vector_count"] == 8 and inheritance["all_rejected_or_quarantined"] and inheritance["erased_negative_count"] == 0)
    check("citation scope never silently expands", context["unsupported_scope_expansions"] == 0 and not context["lexical_similarity_is_semantic_proof"])
    check("independence counts authority roots", partition["independence_is_root_based_not_document_count"] and partition["false_independent_root_count"] == 0)

    canonical = load(phase_dir, "physics/canonical-variational-register.json")
    surface = load(phase_dir, "physics/boundary-surface-equivalence-vectors.json")
    boundary = load(phase_dir, "physics/initial-boundary-admissibility-matrix.json")
    physics = load(phase_dir, "physics/conservation-stability-identifiability-receipt.json")
    check("canonical model family remains scaffold", canonical["model_family"] == "typed scalar-tensor/EFT research scaffold")
    check("canonical dimensions declared", canonical["declared_dimensions"]["R"] == 2 and canonical["declared_dimensions"]["V"] == 4)
    check("boundary functional declared", canonical["boundary_term_required_for_declared_variational_problem"])
    check("surface mutations killed", surface["mutation_count"] == 8 and surface["all_mutations_killed"] and surface["positive_control"]["bulk_equations_match"])
    check("inadmissible boundary cases rejected", boundary["invalid_cases_rejected"] == 4 and not boundary["global_well_posedness_proved"])
    check("physics structural obligations linked", all(physics[key] for key in ["unit_checks_passed", "free_index_checks_passed", "covariance_obligations_linked", "divergence_and_conservation_obligations_linked", "local_stability_mutations_rejected", "structural_rank_degeneracy_rejected", "boundary_admissibility_checked"]))
    check("physics protected claims false", not any([canonical["empirical_confirmation"], canonical["detected_force"], canonical["unique_prediction"], canonical["theory_of_everything"], physics["empirical_stability_or_identifiability"], physics["empirical_gmut_confirmation"], physics["theory_of_everything"]]))

    empirical_contract = load(phase_dir, "empirical/selection-window-contract.json")
    covariance = load(phase_dir, "empirical/covariance-shape-vectors.json")
    adapter = load(phase_dir, "empirical/zero-row-readiness-receipt.json")
    check("empirical contract declares selection covariance nuisance baseline", {"selection_function", "mask_or_window", "covariance_schema", "nuisance_lock", "baseline_lock"} <= set(empirical_contract["required_fields"]))
    check("empirical mutations quarantined", covariance["all_quarantined"] and not covariance["real_covariance_loaded"])
    check("empirical adapter has zero data and inference", adapter["real_measurement_rows_parsed"] == adapter["likelihood_calls"] == adapter["parameter_fits"] == 0)
    check("empirical disposition represented", adapter["disposition"] == "represented" and not adapter["readiness_is_fit"] and not adapter["empirical_gmut_confirmation"])

    thos_lock = load(phase_dir, "thos/crossover-sequence-lock.json")
    carryover = load(phase_dir, "thos/period-carryover-vectors.json")
    exposure = load(phase_dir, "thos/matched-budget-exposure.json")
    thos_gap = load(phase_dir, "thos/real-arm-gap.json")
    check("THOS lock is synthetic", thos_lock["synthetic_only"] and thos_lock["real_arm_runs"] == 0 and thos_lock["analysis_locked_before_unseal"])
    check("THOS carryover mutations rejected", carryover["all_rejected_before_unseal"] and carryover["real_outcomes"] == 0)
    check("THOS exposures matched", exposure["tokens_equal"] and exposure["time_equal"] and exposure["tools_equal"] and not exposure["real_budget_observed"])
    check("THOS protected claims false", not any([thos_gap["real_arms_present"], thos_gap["blind_matched_budget_superiority_result"], thos_gap["agi_evidence"], thos_gap["asi_evidence"], thos_gap["consciousness_evidence"], thos_gap["personhood_evidence"]]))
    check("THOS disposition represented", thos_gap["disposition"] == "represented")

    disclosure = load(phase_dir, "freed-id/disclosure-minimization-profile.json")
    linkability = load(phase_dir, "freed-id/correlation-linkability-vectors.json")
    standards = load(phase_dir, "freed-id/status-resolution-standards-boundary.json")
    freed_gate = load(phase_dir, "freed-id/production-cryptographic-gate.json")
    check("Freed ID fixtures are inert", disclosure["real_credentials"] == disclosure["real_keys"] == disclosure["real_proofs"] == 0)
    check("Freed ID linkability vectors flagged", linkability["all_flagged_or_rejected"] and linkability["cryptographic_operations"] == 0 and not linkability["production_unlinkability"])
    check("Freed ID status and resolution remain non-live", not standards["draft_replaces_stable"] and not standards["live_resolution_executed"] and not standards["live_status_or_revocation_executed"] and not standards["interoperability_test_executed"])
    check("Freed ID production gate entirely open", freed_gate["satisfied_count"] == 0 and not freed_gate["cryptographic_assurance"] and not freed_gate["production_assurance"] and freed_gate["disposition"] == "open_gap")

    standing = load(phase_dir, "cbr/standing-representation-boundary.json")
    remedy = load(phase_dir, "cbr/remedy-preservation-protocol.json")
    retaliation = load(phase_dir, "cbr/anti-retaliation-recusal-vectors.json")
    cbr_gates = load(phase_dir, "cbr/legal-cultural-authority-gates.json")
    check("CBR system cannot determine standing", not standing["system_can_determine_standing"] and standing["conflicts_deferred"])
    check("CBR remedy cannot be waived by artifact", not remedy["technical_artifact_can_waive_remedy"] and remedy["algorithmic_live_resolutions"] == 0)
    check("CBR retaliation and recusal vectors deferred", retaliation["all_deferred_or_rejected"] and retaliation["authorized_live_cases"] == 0)
    check("CBR authority exact gate", cbr_gates["decision"] == "exact_gate" and not cbr_gates["system_may_speak_for_maori"] and not cbr_gates["system_may_substitute_for_affected_parties"] and all(not row["present"] for row in cbr_gates["gates"]))

    resource = load(phase_dir, "security/resource-ceiling-policy.json")
    parser_vectors = load(phase_dir, "security/parser-decompression-vectors.json")
    recovery = load(phase_dir, "security/recovery-and-privacy-receipt.json")
    check("resource limits are pre-materialization", resource["checked_before_materialization"] and not resource["large_payloads_created"] and not resource["privilege_required"])
    check("resource vectors rejected without payload", parser_vectors["unsafe_vectors_rejected"] == 9 and parser_vectors["payload_bytes_materialized"] == 0 and not parser_vectors["exhaustive_security"])
    check("security recovery bounded", recovery["pass"] and recovery["destructive_commands"] == 0 and not recovery["privilege_expansion"] and not recovery["host_security_change"] and not recovery["exhaustive_security"])
    check("security receipt has zero raw ids and private material", recovery["raw_task_or_thread_ids_in_artifacts"] == 0 and recovery["private_routes_or_credentials_in_artifacts"] == 0)

    spec = load(phase_dir, "reproduction/minimal-verifier-spec.json")
    ablation = load(phase_dir, "reproduction/dependency-ablation-matrix.json")
    dual = load(phase_dir, "reproduction/dual-oracle-receipt.json")
    independent = load(phase_dir, "reproduction/independent-team-gap.json")
    snapshot = load(phase_dir, "reproduction/clean-snapshot-validation.json")
    check("minimal verifier is stdlib and offline", spec["runtime"] == "Python standard library only" and not spec["network_required"] and not spec["private_routes_required"] and not spec["absolute_paths_required"] and not spec["optional_packages_required"])
    check("dependencies ablated with common mode visible", ablation["all_declared_nonrequirements"] and ablation["shared_repository_common_mode_remains"])
    check("dual oracle state acceptable", dual["state"] in {"pending_validator_execution", "verified"})
    if dual["state"] == "verified":
        check("dual oracles both valid and equal", dual["full_validator_valid"] and dual["minimal_verifier_valid"] and dual["core_outputs_equal"])
    check("independent reproduction remains open", independent["gap"] == "open" and not independent["independent_team_reproduction"] and not independent["independent_team_result_returned"])
    check("snapshot state acceptable", snapshot["state"] == "verified" or (allow_pending_snapshot and snapshot["state"] == "pending_evidence_commit"), snapshot["state"])
    if snapshot["state"] == "verified":
        check("two detached clean snapshots", len(snapshot["snapshots"]) == 2 and all(row["detached"] and row["clean"] and row["valid"] for row in snapshot["snapshots"]))
        check("snapshot remains same-owner", not snapshot["independent_team_reproduction"])

    constructs = load(phase_dir, "thermo-psyche/construct-operationalization-register.json")
    causal = load(phase_dir, "thermo-psyche/causal-direction-vectors.json")
    alternatives = load(phase_dir, "thermo-psyche/alternative-explanation-matrix.json")
    classification = load(phase_dir, "thermo-psyche/classification-receipt.json")
    six_classes = {"category_barrier", "heuristic", "normative_principle", "operational_rule", "formal_invariant", "empirical_hypothesis"}
    check("thermo psyche six classes exact", set(constructs["classes"]) == six_classes and constructs["all_classes_have_construct_operationalization_and_falsifier"])
    check("thermo psyche causal shortcuts rejected", causal["all_category_shortcuts_rejected"])
    check("thermo psyche alternatives retained", alternatives["alternatives_required"] and not alternatives["absence_of_listed_alternative_proves_causation"])
    check("thermo psyche protected claims false", classification["fundamental_physical_laws_established"] == classification["consciousness_tensors_established"] == 0 and not classification["consciousness_evidence"] and not classification["personhood_evidence"])

    order = load(phase_dir, "stage20/evidence-order-register.json")
    authority = load(phase_dir, "stage20/authority-nonsubstitution-vectors.json")
    board = load(phase_dir, "stage20/pass-fail-defer-board.json")
    terminal = load(phase_dir, "stage20/terminal-verdict.json")
    check("Stage20 exact authority unranked", order["non_substitutable_unranked_count"] == 5 and not order["exact_authority_scored"])
    check("Stage20 authority substitutions rejected", authority["all_rejected"] and not authority["authority_optimized_away"])
    check("Stage20 board uses all decision classes", set(row["decision"] for row in board["board"]) == {"pass", "fail", "defer"} and not board["all_mandatory_gates_pass"])
    check("Stage20 terminal not ready", terminal["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and not terminal["stage20_complete"] and terminal["blocking_fail_or_defer_present"])

    check("retained negatives exact", (negatives["inherited_count"], negatives["new_count"], negatives["negative_count"]) == (32, 14, 46))
    check("all negatives retained", negatives["all_retained"] and not negatives["erasure_permitted"] and all(row["retained"] for row in negatives["negatives"]))
    gate_class_counts = Counter(row["gate_class"] for row in gates["gates"])
    check("gate counts exact", gates["open_gap_count"] == gate_class_counts["open_gap"] == 5 and gates["exact_gate_count"] == gate_class_counts["exact_gate"] == 6)
    check("no gates silently closed", gates["silently_closed"] == 0 and all(row["state"] in {"open", "deferred"} for row in gates["gates"]))
    check("all protected claims false", not any(truth["protected_claims"].values()))
    check("phase truth terminal exact", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and truth["independent_team_gap"] == "open")

    manifest = load(phase_dir, "reproduction/manifest.json")
    actual_hashes = {rel: normalized_sha256(phase_dir / rel) for rel in manifest["normalized_hashes"]}
    check("manifest artifact count exact", manifest["artifact_count"] == len(actual_hashes) == 44)
    check("manifest hashes match", actual_hashes == manifest["normalized_hashes"])
    aggregate = hashlib.sha256("".join(f"{key}:{actual_hashes[key]}\n" for key in sorted(actual_hashes)).encode("utf-8")).hexdigest()
    check("manifest aggregate matches", aggregate == manifest["aggregate_sha256"])
    check("manifest preserves reproduction boundary", not manifest["network_required"] and not manifest["private_route_required"] and not manifest["absolute_machine_path_required"] and not manifest["independent_team_reproduction"])

    overview = (phase_dir / "v642-v1-integrated-overview.md").read_text(encoding="utf-8")
    check("overview is three-page equivalent", len(re.findall(r"\b\w+\b", overview)) >= 1800, len(re.findall(r"\b\w+\b", overview)))
    for phrase in ["NOT_READY_FOR_STAGE_20", "Māori authority", "same-owner", "zero real THOS arm runs", "not a complete WCAG conformance assessment"]:
        check(f"overview contains boundary: {phrase}", phrase in overview)

    report_path = phase_dir / "deliverables/v642-v1-evidence-boundary-report.html"
    if require_report:
        check("static report exists", report_path.is_file())
        if report_path.is_file():
            report = report_path.read_text(encoding="utf-8")
            for token in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
                check(f"static report contains {token}", token in report)
            check("report accessibility claim bounded", "not a complete WCAG conformance assessment" in report)

    summary = {
        "proposal_count": ledger["proposal_count"],
        "disposition_counts": ledger["disposition_counts"],
        "negative_count": negatives["negative_count"],
        "open_gap_count": gates["open_gap_count"],
        "exact_gate_count": gates["exact_gate_count"],
        "terminal_verdict": terminal["terminal_verdict"],
    }
    result = {
        "schema": "ghc.family.evidence-boundary-validation.v1",
        "valid": not issues,
        "check_count": len(checks),
        "pass_count": sum(1 for row in checks if row["pass"]),
        "issue_count": len(issues),
        "issues": issues,
        "summary": summary,
        "checks": checks,
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase_dir = args.phase_dir.resolve()
    result = validate(
        phase_dir,
        allow_pending_snapshot=args.allow_pending_snapshot,
        require_report=args.require_report,
        output=args.output.resolve() if args.output else None,
    )
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
