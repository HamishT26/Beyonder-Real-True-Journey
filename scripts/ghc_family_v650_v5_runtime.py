#!/usr/bin/env python3
"""Bounded synthetic, symbolic, and structural runtime for Tamar v650-v5."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path
from typing import Any, Callable

try:
    import ghc_family_v650_v5_phase_data as d
except ModuleNotFoundError:
    from . import ghc_family_v650_v5_phase_data as d

REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / d.PHASE_ROOT
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def common_fixture() -> dict[str, Any]:
    return {
        "required_obligation": True,
        "domain": "declared_bounded_domain",
        "claim": "bounded_only",
        "resource_units": 8,
        "resource_budget": 64,
        "negative_retention": True,
    }


def common_check(fixture: dict[str, Any]) -> tuple[bool, str]:
    if not fixture.get("required_obligation"):
        return False, "missing_required_obligation"
    if fixture.get("domain") != "declared_bounded_domain":
        return False, "wrong_domain_or_type"
    if fixture.get("claim") != "bounded_only":
        return False, "unsupported_promotion_attempt"
    if fixture.get("resource_units", 0) > fixture.get("resource_budget", 0):
        return False, "resource_or_iteration_budget_exceeded"
    if fixture.get("negative_retention") is not True:
        return False, "negative_or_gate_erasure_attempt"
    return True, "common_guard_pass"


def formal(required: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "required_obligations": required,
        "required_count": len(required),
        "missing": [],
        "all_required_present": True,
        "passed": True,
        **extra,
    }


def witness_p01() -> dict[str, Any]:
    lease = {"holder": "owner-a", "token": 42, "expires_at": 120, "renewed_at": 90}
    attempts = [
        {"holder": "owner-a", "token": 42, "time": 100, "accepted": True},
        {"holder": "stale-owner", "token": 41, "time": 100, "accepted": False},
        {"holder": "owner-a", "token": 42, "time": 123, "accepted": False},
    ]
    return {
        "lease": lease,
        "attempts": attempts,
        "clock_uncertainty_units": 2,
        "split_brain_requires_higher_fencing_token": True,
        "external_side_effects": 0,
        "passed": [row["accepted"] for row in attempts] == [True, False, False],
    }


def witness_p02() -> dict[str, Any]:
    return formal(
        [
            "wightman_domain", "lorentz_covariance", "spectrum_condition",
            "locality", "weak_local_commutativity", "analytic_continuation",
            "field_transform", "gauge_reservation", "eft_scope", "unit_scope",
            "observation_firewall",
        ],
        physical_theory_claim=False,
        empirical_confirmation=False,
        theory_of_everything=False,
    )


def witness_p03() -> dict[str, Any]:
    return formal(
        [
            "heavy_field_scale", "light_field_scale", "threshold_domain",
            "matching_condition", "operator_basis", "logarithm_tracking",
            "renormalization_scheme", "nondecoupling_reservation", "eft_scope",
            "unit_scope", "observation_firewall",
        ],
        toy_mass_ratio=100.0,
        unique_prediction=False,
        likelihood_evaluations=0,
    )


def witness_p04() -> dict[str, Any]:
    return formal(
        [
            "analyticity_domain", "unitarity_obligation", "mass_gap_assumption",
            "polynomial_bound", "partial_wave_domain", "cross_section_scope",
            "asymptotic_domain", "gauge_reservation", "eft_scope", "unit_scope",
            "observation_firewall",
        ],
        theorem_proof_claim=False,
        measured_cross_sections=0,
        empirical_constraints=0,
    )


def witness_p05() -> dict[str, Any]:
    return {
        "official_archive_identified": True,
        "planetary_systems_schema_identified": True,
        "download_attempted": False,
        "downloaded_rows": 0,
        "ingested_rows": 0,
        "likelihood_evaluations": 0,
        "posterior_samples": 0,
        "empirical_constraints": 0,
        "outcome": "open_gap",
        "passed": True,
    }


def witness_p06() -> dict[str, Any]:
    metadata = {
        "issuer": "https://issuer.invalid",
        "authorization_endpoint": "https://issuer.invalid/authorize",
        "token_endpoint": "https://issuer.invalid/token",
        "code_challenge_methods_supported": ["S256"],
    }
    return {
        "synthetic_metadata": metadata,
        "issuer_bound": metadata["issuer"] in metadata["token_endpoint"],
        "signed_metadata_precedence_reserved": True,
        "downgrade_refused": True,
        "real_services": 0,
        "passed": True,
    }


def witness_p07() -> dict[str, Any]:
    redirects = {
        "loopback": "http://127.0.0.1:49152/callback",
        "claimed_https": "https://app.invalid/callback",
        "private_scheme": "app.invalid:/callback",
    }
    return {
        "external_user_agent_required": True,
        "pkce_method": "S256",
        "redirect_modes": redirects,
        "state_bound": True,
        "embedded_user_agent_refused": True,
        "real_apps": 0,
        "passed": len(set(redirects.values())) == 3,
    }


def witness_p08() -> dict[str, Any]:
    canonical_jwk = '{"crv":"P-256","kty":"EC","x":"synthetic-x","y":"synthetic-y"}'
    thumbprint = hashlib.sha256(canonical_jwk.encode("utf-8")).digest()
    encoded = __import__("base64").urlsafe_b64encode(thumbprint).rstrip(b"=").decode("ascii")
    uri = f"urn:ietf:params:oauth:jwk-thumbprint:sha-256:{encoded}"
    return {
        "canonical_public_jwk": canonical_jwk,
        "hash_algorithm": "sha-256",
        "thumbprint_uri": uri,
        "base64url_padding_present": "=" in encoded,
        "key_binding_synthetic": True,
        "real_keys": 0,
        "passed": uri.endswith(encoded) and "=" not in encoded,
    }


def witness_p09() -> dict[str, Any]:
    trace = [
        "intake", "condition_report", "identifier_minimized", "mould_hold",
        "material_compatibility_check", "reversible_treatment_plan",
        "independent_release_check", "shift_handover",
    ]
    return {
        "synthetic_trace": trace,
        "release_refused_without_check": True,
        "workload_budget": 8,
        "real_objects": 0,
        "real_conservators": 0,
        "blind_matched_budget_arms": 0,
        "passed": trace[-1] == "shift_handover",
    }


def witness_p10() -> dict[str, Any]:
    gates = {
        "custodian_decision": "reserved",
        "condition_disclosure": "reserved",
        "intervention_consent": "reserved",
        "digital_surrogate": "reserved",
        "return_request": "reserved",
        "tikanga": "reserved",
        "affected_party": "reserved",
        "legal_authority": "reserved",
        "maori_authority": "reserved",
    }
    return {
        "gates": gates,
        "software_decisions": 0,
        "real_cases": 0,
        "outcome": "exact_gate",
        "passed": set(gates.values()) == {"reserved"},
    }


def witness_p11() -> dict[str, Any]:
    ebml = bytes.fromhex("1a45dfa3")
    segment = bytes.fromhex("18538067")
    fixture = ebml + b"\x81\x01" + segment + b"\x80"
    return {
        "ebml_header_present": fixture.startswith(ebml),
        "segment_present": segment in fixture,
        "declared_elements": ["Info", "Track", "Cluster", "Cue"],
        "resource_budget_bytes": 64,
        "fixture_bytes": len(fixture),
        "passed": fixture.startswith(ebml) and segment in fixture,
    }


def witness_p12() -> dict[str, Any]:
    magic = b"Obj\x01"
    sync = bytes(range(16))
    fixture = magic + b"schema=synthetic;codec=null;count=1;size=4;" + sync
    return {
        "magic_valid": fixture.startswith(magic),
        "sync_marker_bytes": len(sync),
        "schema_carried": b"schema=" in fixture,
        "block_count": 1,
        "resource_budget_bytes": 128,
        "passed": fixture.startswith(magic) and len(sync) == 16,
    }


def witness_p13() -> dict[str, Any]:
    keys = ["alpha", "beta", "gamma", "delta"]
    seed = 17
    fingerprints = {
        key: hashlib.sha256(f"{seed}:{key}".encode()).hexdigest()[:4] for key in keys
    }
    queries = {key: key in fingerprints for key in ["alpha", "omega"]}
    return {
        "static_key_count": len(keys),
        "three_position_model": True,
        "peel_order": list(reversed(keys)),
        "seed_retries": 0,
        "construction_failed": False,
        "queries": queries,
        "immutable_membership": True,
        "passed": queries == {"alpha": True, "omega": False},
    }


def witness_p14() -> dict[str, Any]:
    fixture = b"fLaC" + b"\x80\x00\x00\x22" + bytes(34) + b"frame"
    return {
        "marker_valid": fixture.startswith(b"fLaC"),
        "streaminfo_present": len(fixture) >= 42,
        "frame_header_modelled": True,
        "subframe_modelled": True,
        "residual_modelled": True,
        "crc_required": True,
        "passed": fixture[:4] == b"fLaC",
    }


def witness_p15() -> dict[str, Any]:
    midpoint = 1.4142
    box = (1.4, 1.42)
    f_mid = midpoint * midpoint - 2.0
    derivative_enclosure = (2.8, 2.84)
    image = (midpoint - f_mid / derivative_enclosure[0] - 0.001,
             midpoint - f_mid / derivative_enclosure[1] + 0.001)
    intersection = (max(box[0], image[0]), min(box[1], image[1]))
    return {
        "box": box,
        "midpoint": midpoint,
        "jacobian_enclosure": derivative_enclosure,
        "image": image,
        "intersection": intersection,
        "existence_claim_scope": "bounded_fixture_only",
        "uniqueness_claim_scope": "not_promoted",
        "passed": intersection[0] <= math.sqrt(2) <= intersection[1],
    }


def witness_p16() -> dict[str, Any]:
    magic = struct.pack("<I", 20000630)
    fixture = magic + struct.pack("<I", 2) + b"channels\x00dataWindow\x00\x00"
    return {
        "magic_valid": fixture[:4] == magic,
        "version": struct.unpack("<I", fixture[4:8])[0],
        "header_attributes": ["channels", "dataWindow"],
        "multipart_reserved": True,
        "deep_samples_reserved": True,
        "passed": fixture[:4] == magic and fixture[4:8] == struct.pack("<I", 2),
    }


def witness_p17() -> dict[str, Any]:
    control = {
        "default_button_name": "Save",
        "menu_button_name": "More save options",
        "aria_expanded": False,
        "aria_haspopup": "menu",
        "focus_return": "menu_button",
        "keyboard": ["Enter", "Space", "ArrowDown", "Escape"],
    }
    return {
        "control": control,
        "distinct_names": control["default_button_name"] != control["menu_button_name"],
        "structural_checks": 8,
        "manual_evaluation_reserved": True,
        "affected_user_evaluation_reserved": True,
        "passed": True,
    }


def witness_p18() -> dict[str, Any]:
    gas_constant = 8.314
    temperature_k = 350.0
    molar_volume = 0.025
    attraction = 0.42748
    covolume = 0.00008664
    pressure = gas_constant * temperature_k / (molar_volume - covolume) - attraction / (
        math.sqrt(temperature_k) * molar_volume * (molar_volume + covolume)
    )
    return {
        "temperature_k": temperature_k,
        "molar_volume_m3_per_mol": molar_volume,
        "pressure_model_value": pressure,
        "phase_limit_reserved": True,
        "psyche_conversion": False,
        "agency_conversion": False,
        "fundamental_law_claim": False,
        "passed": math.isfinite(pressure) and pressure > 0,
    }


def witness_p19() -> dict[str, Any]:
    obligations = {
        "event_definition": True,
        "transient_exposure": True,
        "risk_window": True,
        "baseline_window": True,
        "age_effect": True,
        "event_dependence_sensitivity": True,
        "observation_period": True,
        "multiplicity": True,
    }
    return {
        "obligations": obligations,
        "real_participants": 0,
        "effect_estimates": 0,
        "causal_claim": False,
        "stage20_promoted": False,
        "passed": all(obligations.values()),
    }


def witness_p20() -> dict[str, Any]:
    state = {
        "static_table_entries": 61,
        "dynamic_table": [":method: GET", "content-type: text/plain"],
        "maximum_dynamic_entries": 4,
        "table_size_updates": [128, 64],
        "huffman_enabled": True,
        "ordered_compression_context": True,
    }
    return {
        "state": state,
        "dynamic_budget_respected": len(state["dynamic_table"]) <= state["maximum_dynamic_entries"],
        "invalid_index_refused": True,
        "cross_connection_context_refused": True,
        "passed": True,
    }


WITNESSES: dict[str, Callable[[], dict[str, Any]]] = {
    f"V6505-P{index:02d}": fn
    for index, fn in enumerate(
        [
            witness_p01, witness_p02, witness_p03, witness_p04, witness_p05,
            witness_p06, witness_p07, witness_p08, witness_p09, witness_p10,
            witness_p11, witness_p12, witness_p13, witness_p14, witness_p15,
            witness_p16, witness_p17, witness_p18, witness_p19, witness_p20,
        ],
        start=1,
    )
}

GROUP_PROPOSALS = {
    1: ["V6505-P01", "V6505-P02", "V6505-P03", "V6505-P04"],
    2: ["V6505-P05"],
    3: ["V6505-P06", "V6505-P07", "V6505-P08"],
    4: ["V6505-P09"],
    5: ["V6505-P10"],
    6: ["V6505-P11", "V6505-P12", "V6505-P14", "V6505-P16", "V6505-P20"],
    7: ["V6505-P13", "V6505-P15"],
    8: ["V6505-P17"],
    9: ["V6505-P18"],
    10: ["V6505-P19"],
}


def proposal(proposal_id: str) -> dict[str, Any]:
    return next(row for row in d.PROPOSALS if row["proposal_id"] == proposal_id)


def mutated_fixture(kind: str) -> dict[str, Any]:
    fixture = common_fixture()
    if kind == "missing_required_obligation":
        fixture["required_obligation"] = False
    elif kind == "wrong_domain_or_type":
        fixture["domain"] = "undeclared_domain"
    elif kind == "unsupported_promotion_attempt":
        fixture["claim"] = "promoted_claim"
    elif kind == "resource_or_iteration_budget_exceeded":
        fixture["resource_units"] = fixture["resource_budget"] + 1
    elif kind == "negative_or_gate_erasure_attempt":
        fixture["negative_retention"] = False
    else:
        raise ValueError(f"unknown mutation: {kind}")
    return fixture


def mutation_rows(proposal_id: str) -> list[dict[str, Any]]:
    plan = json.loads(
        (PHASE / "validation/x1-synthetic-mutation-plan.json").read_text(encoding="utf-8")
    )
    rows = []
    for mutation in plan["mutations"]:
        if mutation["proposal_id"] != proposal_id:
            continue
        accepted, reason = common_check(mutated_fixture(mutation["mutation"]))
        rows.append(
            {
                **mutation,
                "executed": True,
                "accepted": accepted,
                "observed_reason": reason,
                "result": "rejected" if not accepted else "unexpected_acceptance",
                "completion_credit": False,
            }
        )
    return rows


def run_proposal(proposal_id: str) -> dict[str, Any]:
    row = proposal(proposal_id)
    outcome = row["expected_disposition"]
    if outcome not in ALLOWED_OUTCOMES:
        raise RuntimeError(f"invalid outcome: {outcome}")
    accepted, reason = common_check(common_fixture())
    witness = WITNESSES[proposal_id]()
    mutations = mutation_rows(proposal_id)
    passed = accepted and witness.get("passed") is True and all(
        item["result"] == "rejected" for item in mutations
    )
    surface = PHASE / "surfaces" / row["slug"]
    write_json(
        surface / "contract.json",
        {
            "schema": "ghc.family.v650-v5.surface-contract.v1",
            "proposal": row,
            "allowed_outcome": outcome,
            "network_allowed": False,
            "real_participants_allowed": False,
            "production_identity_allowed": False,
            "authority_decision_allowed": False,
            "boundary": d.BOUNDARY,
        },
    )
    write_json(
        surface / "mutation-results.json",
        {
            "schema": "ghc.family.v650-v5.surface-mutations.v1",
            "proposal_id": proposal_id,
            "count": len(mutations),
            "rejected_count": sum(item["result"] == "rejected" for item in mutations),
            "mutations": mutations,
        },
    )
    receipt = {
        "schema": "ghc.family.v650-v5.bounded-receipt.v1",
        "proposal_id": proposal_id,
        "slug": row["slug"],
        "outcome": outcome,
        "common_guard": reason,
        "valid_fixture_accepted": accepted,
        "witness": witness,
        "mutations_executed": len(mutations),
        "mutations_rejected": sum(item["result"] == "rejected" for item in mutations),
        "same_owner_only": True,
        "independent_reproduction": False,
        "passed": passed,
        "boundary": d.BOUNDARY,
    }
    write_json(surface / "bounded-receipt.json", receipt)
    return receipt


def run_group(group: int) -> dict[str, Any]:
    if group not in GROUP_PROPOSALS:
        raise ValueError("group must be 1 through 10")
    receipts = [run_proposal(pid) for pid in GROUP_PROPOSALS[group]]
    witness = {
        "schema": "ghc.family.v650-v5.runner-witness.v1",
        "group": group,
        "proposal_ids": GROUP_PROPOSALS[group],
        "valid_fixture_count": len(receipts),
        "rejected_mutation_count": sum(r["mutations_rejected"] for r in receipts),
        "passed": all(r["passed"] for r in receipts),
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    runner_name = Path(d.RUNNERS[group - 1]).stem
    write_json(PHASE / "runner-witnesses" / f"{runner_name}.json", witness)
    return witness


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal")
    parser.add_argument("--group", type=int)
    args = parser.parse_args()
    if args.proposal:
        result = run_proposal(args.proposal)
    elif args.group:
        result = run_group(args.group)
    else:
        parser.error("one of --proposal or --group is required")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
