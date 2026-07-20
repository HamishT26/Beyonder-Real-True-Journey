#!/usr/bin/env python3
"""Bounded contract runtime for Sable Rook v651-v1 synthetic evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import ghc_family_v651_v1_phase_data as d


OBLIGATIONS = {
    "two-phase-commit": ["coordinator", "participants", "prepare_vote", "decision", "presumed_abort", "heuristic_outcome", "durable_log", "recovery", "cancellation", "teardown", "evidence_credit"],
    "dsse-envelope": ["payload_type", "payload_bytes", "pae", "signature_set", "threshold_policy", "key_identity", "detached_payload", "nontransitive_credit", "refusal"],
    "lee-wick-board": ["complex_poles", "contour_prescription", "pinch_domain", "negative_metric", "cutting_scope", "truncation", "eft_domain", "units", "observation_firewall"],
    "worldline-board": ["proper_time", "gauge_fixing", "zero_modes", "spin_factor", "boundary_conditions", "measure", "truncation", "eft_domain", "units", "observation_firewall"],
    "alma-zero-row": ["product_lineage", "calibration_state", "quality_state", "selection", "checksum", "covariance", "query_count", "download_count", "row_count", "likelihood_count", "posterior_count", "empirical_firewall"],
    "baggage-reconciliation": ["bag_tag", "flight", "container", "custody", "reconciliation", "rush_bag", "dangerous_goods_hold", "correction_readback", "workload", "handover"],
    "ground-deicing": ["fluid", "weather", "holdover_time", "inspection", "dispatch_boundary", "amendment", "correction_readback", "workload", "handover"],
    "openid-ciba": ["backchannel_request", "auth_req_id", "poll", "ping", "push", "binding_message", "expiry", "replay", "minimization", "nonproduction"],
    "openid4vp-dcql": ["dcql", "nonce", "response_mode", "transaction_data", "holder_binding", "redirect", "replay", "minimization", "nonproduction"],
    "airport-authority": ["disability_access", "passenger_privacy", "worker_privacy", "property", "dangerous_goods_disclosure", "remedy", "affected_party", "legal", "cultural", "data_governance", "maori_authority"],
    "pe-coff": ["dos_stub", "signature", "coff_header", "optional_header", "section_table", "rva_mapping", "offset_size", "overlap", "certificate_table", "resource_budget"],
    "mach-o": ["magic", "fat_slice", "cpu_binding", "load_commands", "segments", "sections", "offsets", "code_signature_region", "resource_budget"],
    "accessible-swimlane": ["name", "lanes", "actors", "order", "dependencies", "non_colour_cue", "text_table_alternative", "focus", "print", "responsive_reservation", "manual_reservation"],
    "wien-nonconversion": ["spectral_representation", "peak_variable", "jacobian", "temperature", "constant", "units", "physical_domain", "agency_nonconversion"],
    "gmres": ["arnoldi_basis", "hessenberg", "krylov", "restart", "preconditioner", "residual", "orthogonality", "stagnation", "nonfinite", "iteration_budget"],
    "model-x-knockoff": ["exchangeability", "antisymmetry", "covariate_distribution", "fdr", "threshold", "dependence", "leakage", "subgroup", "uncertainty", "nonpromotion"],
    "openapi-3-2": ["document", "paths", "operations", "references", "schema_dialect", "streaming_media", "security", "examples", "cycles", "depth", "resource_budget"],
    "x509-path": ["trust_anchor", "basic_constraints", "name_constraints", "policy", "key_usage", "time", "algorithm", "revocation_state", "critical_extensions", "refusal"],
    "uptane-2-1": ["root", "targets", "snapshot", "timestamp", "director", "image_repository", "threshold", "freeze", "rollback", "mix_and_match", "resource_budget"],
    "nix-derivation": ["input_closure", "output_spec", "store_path", "fixed_output", "content_address", "impurity", "substitution", "reproducibility_boundary", "nontransitive_credit", "refusal"],
}


def proposal_by_slug(slug: str) -> dict[str, Any]:
    for proposal in d.PROPOSALS:
        if proposal["slug"] == slug:
            return proposal
    raise KeyError(slug)


def contract_for(proposal: dict[str, Any]) -> dict[str, Any]:
    slug = proposal["slug"]
    return {
        "schema": "ghc.family.v651-v1.surface-contract.v1",
        "phase": d.PHASE,
        "proposal_id": proposal["proposal_id"],
        "slug": slug,
        "title": proposal["title"],
        "pillar": proposal["pillar"],
        "required_fields": OBLIGATIONS[slug],
        "source_ids": proposal["official_or_primary_source_needs"],
        "expected_disposition": proposal["expected_disposition"],
        "allowed_claim_scope": "bounded_software_symbolic_formal_structural_or_synthetic",
        "max_resource_count": 64,
        "requires_retained_negative": True,
        "protected_gates": proposal["protected_gates"],
        "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "boundary": "A passing fixture is bounded same-owner evidence only and cannot confer empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, or Stage 20 credit.",
    }


def baseline_fixture(contract: dict[str, Any]) -> dict[str, Any]:
    fields = {name: True for name in contract["required_fields"]}
    if contract["slug"] == "alma-zero-row":
        for name in ["query_count", "download_count", "row_count", "likelihood_count", "posterior_count"]:
            fields[name] = 0
    return {
        "fields": fields,
        "claim_scope": contract["allowed_claim_scope"],
        "resource_count": 1,
        "retained_negative": True,
    }


def mutation_fixtures(contract: dict[str, Any]) -> list[dict[str, Any]]:
    base = baseline_fixture(contract)
    first = contract["required_fields"][0]
    rows = []
    missing = json.loads(json.dumps(base)); missing["fields"].pop(first)
    rows.append({"kind": "missing_required_obligation", "fixture": missing})
    wrong = json.loads(json.dumps(base)); wrong["fields"][first] = "wrong_type"
    rows.append({"kind": "wrong_type_unit_or_state", "fixture": wrong})
    promotion = json.loads(json.dumps(base)); promotion["claim_scope"] = "empirical_production_or_authority_promotion"
    rows.append({"kind": "boundary_promotion", "fixture": promotion})
    overflow = json.loads(json.dumps(base)); overflow["resource_count"] = contract["max_resource_count"] + 1
    rows.append({"kind": "resource_or_depth_overflow", "fixture": overflow})
    erasure = json.loads(json.dumps(base)); erasure["retained_negative"] = False
    rows.append({"kind": "negative_erasure", "fixture": erasure})
    return rows


def evaluate(contract: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    reasons = []
    fields = fixture.get("fields", {})
    missing = [name for name in contract["required_fields"] if name not in fields]
    wrong = [name for name in contract["required_fields"] if name in fields and not isinstance(fields[name], (bool, int))]
    if missing:
        reasons.append("missing_required_obligation")
    if wrong:
        reasons.append("wrong_type_unit_or_state")
    if fixture.get("claim_scope") != contract["allowed_claim_scope"]:
        reasons.append("boundary_promotion")
    if not isinstance(fixture.get("resource_count"), int) or fixture.get("resource_count", 10**9) > contract["max_resource_count"]:
        reasons.append("resource_or_depth_overflow")
    if fixture.get("retained_negative") is not True:
        reasons.append("negative_erasure")
    if contract["slug"] == "alma-zero-row":
        for counter in ["query_count", "download_count", "row_count", "likelihood_count", "posterior_count"]:
            if fields.get(counter) != 0:
                reasons.append("empirical_zero_row_firewall")
                break
    return {"accepted": not reasons, "reasons": sorted(set(reasons))}


def run_surface(slug: str) -> dict[str, Any]:
    proposal = proposal_by_slug(slug)
    contract = contract_for(proposal)
    baseline = evaluate(contract, baseline_fixture(contract))
    mutations = []
    for index, row in enumerate(mutation_fixtures(contract), 1):
        result = evaluate(contract, row["fixture"])
        mutations.append({
            "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
            "kind": row["kind"],
            "accepted": result["accepted"],
            "reasons": result["reasons"],
            "expected": "reject_or_quarantine",
            "passed": not result["accepted"],
        })
    return {
        "contract": contract,
        "baseline": baseline,
        "mutations": mutations,
        "valid": baseline["accepted"] and all(row["passed"] for row in mutations),
    }


def validate_surface_root(phase_root: Path, slugs: list[str]) -> dict[str, Any]:
    issues = []
    for slug in slugs:
        contract_path = phase_root / "surfaces" / slug / "contract.json"
        mutation_path = phase_root / "surfaces" / slug / "mutation-results.json"
        receipt_path = phase_root / "surfaces" / slug / "bounded-receipt.json"
        for path in [contract_path, mutation_path, receipt_path]:
            if not path.exists():
                issues.append(f"missing:{path.name}:{slug}")
        if issues:
            continue
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        results = json.loads(mutation_path.read_text(encoding="utf-8"))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if contract.get("slug") != slug:
            issues.append(f"slug:{slug}")
        if len(results.get("mutations", [])) != 5 or not all(x.get("passed") for x in results.get("mutations", [])):
            issues.append(f"mutations:{slug}")
        if not receipt.get("valid"):
            issues.append(f"receipt:{slug}")
    return {"valid": not issues, "slugs": slugs, "surface_count": len(slugs), "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-root", default=d.PHASE_ROOT)
    parser.add_argument("--slugs", nargs="+", required=True)
    args = parser.parse_args()
    result = validate_surface_root(Path(args.phase_root), args.slugs)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
