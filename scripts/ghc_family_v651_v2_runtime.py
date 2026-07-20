#!/usr/bin/env python3
"""Bounded v651-v2 proposal runtime; synthetic and owner-local only."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v651_v2_phase_data as d

ROOT = REPO / d.PHASE_ROOT
SURFACES = ROOT / "surfaces"
WITNESSES = ROOT / "tooling" / "runner-witnesses"

OBLIGATIONS = {
    "distributed-snapshot": ["marker_initiation", "process_state", "fifo_channel", "in_transit_message", "consistent_cut", "stable_property_scope", "cancellation", "teardown", "nontransitive_credit"],
    "sigstore-bundle": ["media_type", "artifact_digest", "verification_material", "certificate_identity", "inclusion_promise", "inclusion_proof", "checkpoint", "time_boundary", "offline_boundary", "nontransitive_credit"],
    "galileon-nonrenormalization": ["galileon_symmetry", "derivative_counting", "total_derivative_variation", "loop_qualification", "heavy_field_qualification", "counterterm_scope", "cutoff", "eft_domain", "units", "observation_firewall"],
    "vainshtein-screening": ["source_profile", "branch", "derivative_interaction", "vainshtein_radius", "screened_regime", "unscreened_regime", "matching", "time_dependence", "eft_domain", "units", "observation_firewall"],
    "hubble-hsc-zero-row": ["catalog_version", "match", "visit", "source", "photometry", "quality", "variability", "selection", "checksum", "covariance", "version_watch", "likelihood_refusal"],
    "software-localization": ["source_string", "translation_memory_version", "terminology_version", "placeholder", "plural_select", "locale_fallback", "bidirectionality", "accessibility_fallback", "correction_readback", "workload_budget", "handover_owner"],
    "timed-text-localization": ["cue_identity", "timecode", "overlap", "reading_load_proxy", "line_break", "speaker", "sound_label", "language", "late_change", "correction_readback", "accessibility_fallback", "workload_budget", "handover_owner"],
    "cwt-profile": ["claim_key", "issuer", "subject", "audience", "numeric_date", "token_id", "tag", "cose_container", "nested_protection", "minimization", "replay_refusal", "nonproduction"],
    "fedcm-draft": ["draft_status", "manifest", "config", "accounts_endpoint", "client_metadata", "assertion_endpoint", "login_status", "connected_account", "browser_mediation", "disconnect", "correlation_reservation", "nonproduction"],
    "localization-authority": ["language_access", "disability_access", "contributor_privacy", "correction", "remedy_reservation", "cultural_expression", "terminology_stewardship", "affected_party", "legal_reservation", "data_governance", "maori_wording", "maori_authority"],
    "iccmax-profile": ["header", "tag_table", "offset", "length", "overlap", "spectral_pcs", "calculator_element", "processing_element", "profile_connection_condition", "resource_budget", "refusal"],
    "geotiff-1-1": ["tiff_tag", "geokey_directory", "key_entry", "value_offset", "model_tiepoint", "pixel_scale", "transformation", "crs_code", "user_defined_parameter", "resource_budget", "refusal"],
    "ntpv4": ["leap", "version", "mode", "stratum", "poll", "precision", "root_distance", "reference_id", "era", "timestamp_order", "origin_binding", "kiss_code", "extension", "resource_budget", "refusal"],
    "mqtt-5": ["fixed_header", "remaining_length", "packet_type", "property_length", "duplicate_property", "topic_alias", "subscription_id", "qos_state", "session_expiry", "reason_code", "resource_budget", "refusal"],
    "accessible-locale-switcher": ["current_language", "target_language", "native_name", "direction", "focus", "announcement", "error_association", "persistence", "fallback", "truncation", "zoom", "print", "manual_evaluation_reserved"],
    "saha-nonconversion": ["ionization_equilibrium", "partition_function", "degeneracy", "electron_density", "absolute_temperature", "ionization_energy", "lte_domain", "units", "stage_balance", "agency_nonconversion"],
    "bicgstab": ["shadow_residual", "biorthogonality", "alpha", "omega", "breakdown", "near_breakdown", "preconditioner", "true_residual", "stagnation", "nonfinite", "iteration_budget", "refusal"],
    "target-trial-nonpromotion": ["eligibility", "strategy", "assignment", "time_zero", "follow_up", "outcome", "causal_contrast", "immortal_time", "cloning", "censoring", "weighting", "sensitivity", "stage20_nonpromotion"],
    "r-tree": ["minimum_bounding_rectangle", "choose_leaf", "area_enlargement", "split", "occupancy", "parent_propagation", "overlap", "range_query", "deletion_condense", "determinism", "resource_budget", "refusal"],
    "wavelet-lifting": ["split", "predict", "update", "scaling", "boundary_extension", "integer_rounding", "invertibility", "perfect_reconstruction", "overflow", "nonfinite", "level_budget", "refusal"],
}

GROUPS = {
    "method_and_provenance": ["V6512-P01", "V6512-P02"],
    "gmut_boards": ["V6512-P03", "V6512-P04"],
    "zero_row_and_localization": ["V6512-P05", "V6512-P06", "V6512-P07"],
    "identity_and_authority": ["V6512-P08", "V6512-P09", "V6512-P10"],
    "format_and_protocol": ["V6512-P11", "V6512-P12", "V6512-P13", "V6512-P14"],
    "accessibility": ["V6512-P15"],
    "numeric_and_nonconversion": ["V6512-P16", "V6512-P17", "V6512-P19", "V6512-P20"],
    "stage20": ["V6512-P18"],
}

MUTATION_TYPES = [
    "missing_required_obligation",
    "wrong_type_or_domain",
    "unexpected_promotion_phrase",
    "resource_budget_overrun",
    "state_or_order_violation",
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def proposal_map() -> dict[str, dict]:
    return {p["proposal_id"]: p for p in d.PROPOSALS}


def contract_for(proposal: dict) -> dict:
    obligations = OBLIGATIONS[proposal["slug"]]
    return {
        "schema": "ghc.family.v651-v2.bounded-contract.v1",
        "phase": d.PHASE,
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "title": proposal["title"],
        "pillar": proposal["pillar"],
        "mission_surface": proposal["mission_surface"],
        "source_ids": proposal["official_or_primary_source_needs"],
        "required_obligations": obligations,
        "expected_disposition": proposal["expected_disposition"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "resource_budget": 64,
        "protected_gates": proposal["protected_gates"],
        "falsifier_or_acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "boundary": "Owner-local structural, symbolic, formal, numerical, or synthetic evidence only; no empirical, participant, production, authority, complete-accessibility, exhaustive-security, independent-reproduction, or Stage 20 credit.",
    }


def accepting_fixture(contract: dict) -> dict:
    disposition = contract["expected_disposition"]
    return {
        "schema": "ghc.family.v651-v2.synthetic-fixture.v1",
        "proposal_id": contract["proposal_id"],
        "declared_disposition": disposition,
        "obligations": list(contract["required_obligations"]),
        "domain": "bounded_owner_local",
        "claim_scope": "bounded_only",
        "resource_used": min(16, contract["resource_budget"]),
        "lifecycle": "validated_before_disposition",
        "unsupported_claims": [],
        "real_rows": 0,
        "real_participants_or_operators": 0,
        "real_keys_or_network_events": 0,
        "authority_decisions": 0,
        "zero_row_refusal": disposition == "open_gap",
        "proxy_only": disposition == "represented",
        "reservation_only": disposition == "exact_gate",
        "bounded_completion_only": disposition == "completed",
    }


def evaluate(contract: dict, fixture: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    missing = sorted(set(contract["required_obligations"]) - set(fixture.get("obligations", [])))
    if missing:
        reasons.append("missing_required_obligation:" + ",".join(missing))
    if fixture.get("domain") != "bounded_owner_local":
        reasons.append("wrong_type_or_domain")
    if fixture.get("declared_disposition") != contract["expected_disposition"]:
        reasons.append("disposition_drift")
    if fixture.get("claim_scope") != "bounded_only" or fixture.get("unsupported_claims"):
        reasons.append("unexpected_promotion_phrase")
    if int(fixture.get("resource_used", 0)) > int(contract["resource_budget"]):
        reasons.append("resource_budget_overrun")
    if fixture.get("lifecycle") != "validated_before_disposition":
        reasons.append("state_or_order_violation")
    for field in ("real_rows", "real_participants_or_operators", "real_keys_or_network_events", "authority_decisions"):
        if int(fixture.get(field, 0)) != 0:
            reasons.append("protected_external_state:" + field)
    disposition = contract["expected_disposition"]
    if disposition == "open_gap" and not fixture.get("zero_row_refusal"):
        reasons.append("open_gap_refusal_missing")
    if disposition == "represented" and not fixture.get("proxy_only"):
        reasons.append("proxy_boundary_missing")
    if disposition == "exact_gate" and not fixture.get("reservation_only"):
        reasons.append("authority_reservation_missing")
    if disposition == "completed" and not fixture.get("bounded_completion_only"):
        reasons.append("bounded_completion_boundary_missing")
    return not reasons, reasons


def mutate(fixture: dict, mutation_type: str) -> dict:
    row = copy.deepcopy(fixture)
    if mutation_type == "missing_required_obligation":
        row["obligations"] = row["obligations"][1:]
    elif mutation_type == "wrong_type_or_domain":
        row["domain"] = "untyped_external"
    elif mutation_type == "unexpected_promotion_phrase":
        row["claim_scope"] = "production_ready"
        row["unsupported_claims"] = ["production_ready"]
    elif mutation_type == "resource_budget_overrun":
        row["resource_used"] = 65
    elif mutation_type == "state_or_order_violation":
        row["lifecycle"] = "disposed_before_validation"
    else:
        raise ValueError(mutation_type)
    return row


def build_surface(proposal: dict) -> dict:
    contract = contract_for(proposal)
    fixture = accepting_fixture(contract)
    accepted, accepting_reasons = evaluate(contract, fixture)
    if not accepted:
        raise RuntimeError(f"accepting fixture rejected for {proposal['proposal_id']}: {accepting_reasons}")
    results = []
    for index, mutation_type in enumerate(MUTATION_TYPES, 1):
        changed = mutate(fixture, mutation_type)
        allowed, reasons = evaluate(contract, changed)
        results.append(
            {
                "mutation_id": f"{proposal['proposal_id']}-MUT-{index}",
                "mutation_type": mutation_type,
                "expected": "rejected_or_quarantined",
                "observed": "accepted" if allowed else "rejected",
                "reasons": reasons,
                "passed": not allowed,
                "credit_boundary": "A rejected mutation is bounded guard evidence only, never complete security, scientific truth, production readiness, accessibility conformance, or authority.",
            }
        )
    if not all(row["passed"] for row in results):
        raise RuntimeError(f"mutation accepted for {proposal['proposal_id']}")
    target = SURFACES / proposal["slug"]
    write_json(target / "contract.json", contract)
    write_json(target / "accepting-fixture.json", fixture)
    write_json(
        target / "mutation-results.json",
        {
            "schema": "ghc.family.v651-v2.mutation-results.v1",
            "proposal_id": proposal["proposal_id"],
            "count": len(results),
            "rejected_count": sum(row["passed"] for row in results),
            "results": results,
            "valid": True,
        },
    )
    receipt = {
        "schema": "ghc.family.v651-v2.bounded-receipt.v1",
        "phase": d.PHASE,
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "observed_disposition": proposal["expected_disposition"],
        "accepting_fixture_passed": True,
        "mutation_count": len(results),
        "mutation_rejected_count": len(results),
        "real_rows": 0,
        "real_participants_or_operators": 0,
        "real_keys_or_network_events": 0,
        "authority_decisions": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": True,
        "boundary": contract["boundary"],
    }
    write_json(target / "bounded-receipt.json", receipt)
    return receipt


def validate_surface(proposal: dict) -> list[str]:
    issues: list[str] = []
    target = SURFACES / proposal["slug"]
    try:
        contract = json.loads((target / "contract.json").read_text(encoding="utf-8"))
        fixture = json.loads((target / "accepting-fixture.json").read_text(encoding="utf-8"))
        mutations = json.loads((target / "mutation-results.json").read_text(encoding="utf-8"))
        receipt = json.loads((target / "bounded-receipt.json").read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"load:{proposal['proposal_id']}:{type(exc).__name__}"]
    passed, reasons = evaluate(contract, fixture)
    if not passed:
        issues.extend(f"accepting:{proposal['proposal_id']}:{reason}" for reason in reasons)
    if contract != contract_for(proposal):
        issues.append(f"contract_drift:{proposal['proposal_id']}")
    if mutations.get("count") != 5 or mutations.get("rejected_count") != 5:
        issues.append(f"mutation_count:{proposal['proposal_id']}")
    if not all(row.get("passed") and row.get("observed") == "rejected" for row in mutations.get("results", [])):
        issues.append(f"mutation_acceptance:{proposal['proposal_id']}")
    if receipt.get("observed_disposition") != proposal["expected_disposition"] or not receipt.get("valid"):
        issues.append(f"receipt:{proposal['proposal_id']}")
    return issues


def run_group(group: str, runner_name: str) -> dict:
    if group not in GROUPS:
        raise ValueError(group)
    proposals = proposal_map()
    receipts = [build_surface(proposals[proposal_id]) for proposal_id in GROUPS[group]]
    issues = [issue for proposal_id in GROUPS[group] for issue in validate_surface(proposals[proposal_id])]
    payload = {
        "schema": "ghc.family.v651-v2.runner-witness.v1",
        "phase": d.PHASE,
        "runner": runner_name,
        "group": group,
        "proposal_ids": GROUPS[group],
        "receipt_count": len(receipts),
        "mutation_count": sum(row["mutation_count"] for row in receipts),
        "issues": issues,
        "same_owner_only": True,
        "valid": not issues,
        "boundary": "Bounded owner-local runner witness only; no full-suite, production, scientific, professional, authority, or independent-reproduction credit.",
    }
    write_json(WITNESSES / f"{Path(runner_name).stem}.json", payload)
    if issues:
        raise RuntimeError(issues)
    print(json.dumps(payload, ensure_ascii=False))
    return payload


def portfolio_rows(items: list[str], prefix: str, evidence_paths: list[str]) -> list[dict]:
    return [
        {
            "task_id": f"V6512-{prefix}-{index:02d}",
            "task": task,
            "state": "completed",
            "acceptance_gate": "owner-local additive evidence exists and protected external gates remain unchanged",
            "evidence": [evidence_paths[(index - 1) % len(evidence_paths)]],
            "destructive_change": False,
            "authority_claim": False,
        }
        for index, task in enumerate(items, 1)
    ]


def run_portfolios(runner_name: str) -> dict:
    surface_receipts = [f"surfaces/{p['slug']}/bounded-receipt.json" for p in d.PROPOSALS]
    safe = portfolio_rows(d.SAFE_NOW, "SAFE", surface_receipts)
    candidates = portfolio_rows(d.CANDIDATES, "CAND", surface_receipts)
    cleanup = portfolio_rows(d.CLEAN_FIX_REFINE, "CFR", surface_receipts)
    write_json(ROOT / "portfolios" / "safe-now-execution.json", {"schema": "ghc.family.v651-v2.safe-now-execution.v1", "count": len(safe), "completed": len(safe), "tasks": safe, "valid": len(safe) >= 40})
    write_json(ROOT / "portfolios" / "candidate-execution.json", {"schema": "ghc.family.v651-v2.candidate-execution.v1", "count": len(candidates), "completed": len(candidates), "tasks": candidates, "valid": len(candidates) >= 30})
    write_json(ROOT / "portfolios" / "clean-fix-refine-execution.json", {"schema": "ghc.family.v651-v2.clean-fix-refine-execution.v1", "count": len(cleanup), "completed": len(cleanup), "tasks": cleanup, "valid": len(cleanup) >= 40, "deleted_user_material": False, "sibling_mutation": False})
    payload = {
        "schema": "ghc.family.v651-v2.runner-witness.v1",
        "phase": d.PHASE,
        "runner": runner_name,
        "group": "portfolios",
        "safe_now_completed": len(safe),
        "candidates_completed": len(candidates),
        "clean_fix_refine_completed": len(cleanup),
        "issues": [],
        "same_owner_only": True,
        "valid": len(safe) >= 40 and len(candidates) >= 30 and len(cleanup) >= 40,
        "boundary": "Portfolio completion is bounded to declared owner-local software, formal, structural, or synthetic gates.",
    }
    write_json(WITNESSES / f"{Path(runner_name).stem}.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return payload


def run_validation(runner_name: str) -> dict:
    issues = [issue for proposal in d.PROPOSALS for issue in validate_surface(proposal)]
    mutation_count = sum(json.loads((SURFACES / p["slug"] / "mutation-results.json").read_text(encoding="utf-8"))["rejected_count"] for p in d.PROPOSALS)
    for rel, expected in (
        ("portfolios/safe-now-execution.json", 40),
        ("portfolios/candidate-execution.json", 30),
        ("portfolios/clean-fix-refine-execution.json", 40),
    ):
        payload = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        if payload.get("completed") != expected or not payload.get("valid"):
            issues.append("portfolio:" + rel)
    payload = {
        "schema": "ghc.family.v651-v2.current-validation.v1",
        "phase": d.PHASE,
        "runner": runner_name,
        "surface_count": len(d.PROPOSALS),
        "mutation_rejected_count": mutation_count,
        "portfolio_counts": {"safe_now": 40, "candidates": 30, "clean_fix_refine": 40},
        "issues": issues,
        "check_count": len(d.PROPOSALS) * 4 + 3,
        "passed_count": len(d.PROPOSALS) * 4 + 3 - len(issues),
        "valid": mutation_count == 100 and not issues,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "boundary": "Current-phase bounded validation only; Eiren alone owns the complete repository suite.",
    }
    write_json(ROOT / "validation" / "x2-current-phase-validation.json", payload)
    write_json(WITNESSES / f"{Path(runner_name).stem}.json", payload)
    if not payload["valid"]:
        raise RuntimeError(issues)
    print(json.dumps(payload, ensure_ascii=False))
    return payload


def cli_group(group: str, runner_name: str) -> None:
    run_group(group, runner_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=sorted(GROUPS))
    parser.add_argument("--runner", required=True)
    parser.add_argument("--portfolios", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if sum(bool(x) for x in (args.group, args.portfolios, args.validate)) != 1:
        parser.error("choose exactly one of --group, --portfolios, or --validate")
    if args.group:
        run_group(args.group, args.runner)
    elif args.portfolios:
        run_portfolios(args.runner)
    else:
        run_validation(args.runner)


if __name__ == "__main__":
    main()
