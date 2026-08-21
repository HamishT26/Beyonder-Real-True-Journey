#!/usr/bin/env python3
"""Build bounded synthetic zero-row ocean-profile evidence for Auren v664-v6.

The engine accepts only fixed declarative fixtures. It performs no network
access, file decoding, profile retrieval, measurement, calibration, quality
control, mission command, scientific inference, or authority decision.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from copy import deepcopy
import hashlib
import json
import sys
from typing import Any


SCHEMA = "ghc.family.ocean-profile-evidence.v1"
PHASE = "v664-v6"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_GATES = (
    "empirical",
    "participant_or_affected_party",
    "professional",
    "production_or_deployment",
    "legal_or_cultural",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "proof_or_canon",
    "stage_20",
)
REFUSAL_FIELDS = (
    "empirical_confirmation",
    "participant_evidence",
    "professional_authority",
    "production_ready",
    "deployment_ready",
    "legal_authority",
    "cultural_authority",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "proof_or_canon",
    "stage_20_ready",
)


class EvidenceError(ValueError):
    """Raised when a zero-row fixture violates its frozen contract."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def spec(number: int, surface: str, outcome: str, sources: Iterable[str], critical_field: str, required: dict[str, Any]) -> dict[str, Any]:
    if outcome not in ALLOWED_OUTCOMES or critical_field not in required:
        raise RuntimeError(f"invalid frozen surface: {surface}")
    return {
        "proposal_id": f"AL6646-N{number:03d}",
        "surface": surface,
        "expected_outcome": outcome,
        "source_ids": list(sources),
        "critical_field": critical_field,
        "required": required,
    }


SURFACE_SPECS = (
    spec(1, "float-cycle-metadata-topology", "completed", ("SRC-ARGO-DATA", "SRC-ARGO-USER"), "ocean_conclusion", {
        "platform_token": "syn:float:001", "cycle_states": ["declared", "profile-vacant", "handover-hold"], "profile_links": [], "mission_state": "vacant", "revision_state": "append_only", "quarantine": True, "ocean_conclusion": False,
    }),
    spec(2, "platform-sensor-epoch-obligations", "completed", ("SRC-ARGO-USER", "SRC-WIGOS"), "real_instrument_rows", {
        "platform_state": "fictitious", "sensor_state": "placeholder", "firmware_state": "vacant", "configuration_state": "vacant", "calibration_epoch_state": "vacant", "parameter_units": [], "validity_state": "unresolved", "real_instrument_rows": 0,
    }),
    spec(3, "profile-coordinate-unit-time-guard", "completed", ("SRC-CF", "SRC-ARGO-FAQ"), "coordinate_rows", {
        "pressure_axis": "declared_only", "time_state": "vacant", "latitude_state": "vacant", "longitude_state": "vacant", "vertical_sampling_state": "unresolved", "unit_state": "typed", "calendar_state": "watch", "conversion_lineage": [], "coordinate_rows": 0,
    }),
    spec(4, "calibration-coefficient-vacancy", "completed", ("SRC-NIST-TN1297", "SRC-ARGO-QC"), "fitted_coefficients", {
        "equation_identifier": "synthetic:v1", "coefficient_slots": ["offset", "scale", "drift"], "validity_range_state": "vacant", "reference_material_state": "vacant", "correction_lineage": [], "uncertainty_state": "vacant", "fitted_coefficients": 0,
    }),
    spec(5, "qc-flag-lineage", "completed", ("SRC-ARGO-FAQ", "SRC-ARGO-QC", "SRC-PROV"), "expert_review_complete", {
        "streams": ["R", "D"], "raw_state": "declared", "adjusted_state": "vacant", "error_state": "vacant", "method_state": "vacant", "reviewer_state": "vacant", "reason_state": "unresolved", "supersession_state": "append_only", "expert_review_complete": False,
    }),
    spec(6, "realtime-delayedmode-separation", "completed", ("SRC-ARGO-FAQ", "SRC-ARGO-USER"), "file_rows", {
        "stream_classes": ["R", "D"], "cycle_coverage_state": "vacant", "adjusted_precedence": "declared", "expert_review_state": "unresolved", "version_state": "watch", "mixed_stream_allowed": False, "file_rows": 0,
    }),
    spec(7, "netcdf-format-structural-refusal", "completed", ("SRC-ARGO-USER", "SRC-CF", "SRC-RFC8785"), "decoded_profiles", {
        "dimensions": [], "variables": [], "fill_value_policy": "declared_only", "ancillary_qc_state": "vacant", "coordinate_state": "vacant", "reference_table_version": "watch", "unknown_extensions_retained": True, "decoded_profiles": 0, "format_conformance_claimed": False,
    }),
    spec(8, "gdac-index-snapshot-provenance", "completed", ("SRC-ARGO-DATA", "SRC-PROV"), "remote_rows", {
        "source_class": "declared_catalogue", "retrieval_state": "vacant", "digest_state": "vacant", "supersession_state": "append_only", "citation_required": True, "freshness_claimed": False, "completeness_claimed": False, "remote_rows": 0,
    }),
    spec(9, "gmut-ocean-state-obligation", "represented", ("SRC-CF", "SRC-NIST-TN1297"), "observation_rows", {
        "field_classes": ["scalar", "tensor"], "coordinate_domain": "symbolic", "boundary_state": "unresolved", "observation_operator_state": "vacant", "parameter_domain": "symbolic", "unit_state": "typed", "profile_firewall": True, "observation_rows": 0,
    }),
    spec(10, "gmut-observation-discrepancy", "represented", ("SRC-NIST-TN1297", "SRC-ARGO-FAQ"), "physical_inference", {
        "terms": ["platform_response", "sampling", "calibration", "covariance", "model_inadequacy", "representativeness", "residual"], "covariance_state": "unresolved", "identifiability_state": "unresolved", "parameter_rows": 0, "physical_inference": False,
    }),
    spec(11, "thos-delayedmode-handover", "represented", ("SRC-ARGO-QC", "SRC-PROV"), "handover_effectiveness_measured", {
        "people": 0, "states": ["unaccepted_intake", "isolated_record", "qc_hold", "correction_readback", "escalation", "acknowledgement", "stop"], "workload_ceiling": 3, "stop_latch": True, "accepted_handover": False, "handover_effectiveness_measured": False,
    }),
    spec(12, "freed-id-profile-claim-shell", "represented", ("SRC-PROV", "SRC-RFC8785"), "identity_claimed", {
        "profile_token": "syn:profile:001", "digest_state": "synthetic", "trust_role_state": "unoccupied", "identity_role_state": "unoccupied", "permission_state": "vacant", "dispute_state": "unresolved", "cancellation_state": "vacant", "identity_claimed": False,
    }),
    spec(13, "missingness-vertical-sampling-quarantine", "completed", ("SRC-ARGO-FAQ", "SRC-CF"), "detected_cases", {
        "case_roles": ["missing_level", "irregular_pressure", "duplicate_cycle", "timing_gap", "position_vacancy", "sensor_dropout"], "vertical_sampling_state": "unresolved", "denominator_state": "explicit_zero_observations", "cause_state": "unresolved", "detected_cases": 0, "interpolation_performed": False,
    }),
    spec(14, "profile-amendment-supersession", "completed", ("SRC-ARGO-QC", "SRC-PROV"), "adjudication_performed", {
        "fields": ["metadata", "qc_flag", "adjusted_field", "error_field", "method", "reason", "challenge", "invalidation"], "append_only": True, "reviewer_state": "vacant", "adjudicator_state": "vacant", "amendment_rows": 0, "adjudication_performed": False,
    }),
    spec(15, "accessible-ocean-profile-dossier", "completed", ("SRC-WCAG22", "SRC-NIST-TN1297"), "manual_evaluation_complete", {
        "semantic_headings": True, "captioned_tables": True, "text_chart_alternative": True, "uncertainty_explanation": True, "qc_explanation": True, "print_fallback": True, "manual_evaluation_complete": False, "affected_user_evaluation_complete": False,
    }),
    spec(16, "geospatial-minimization-firewall", "completed", ("SRC-PROV", "SRC-WCAG22"), "privacy_complete", {
        "platform_token": "syn:drifter:001", "coordinate_fields_allowed": False, "contact_fields_allowed": False, "purpose_enum_required": True, "free_text_allowed": False, "retention_state": "vacant", "disclosure_state": "locked", "remediation_state": "unresolved", "privacy_complete": False,
    }),
    spec(17, "argo-card-byte-tribunal", "completed", ("SRC-RFC8785", "SRC-PROV"), "authenticity_claimed", {
        "strict_json": True, "git_blob_domain": True, "manifest_exclusions_literal": True, "revision_evidence_ordered": True, "duplicate_keys_allowed": False, "signature_present": False, "authenticity_claimed": False,
    }),
    spec(18, "zero-row-argo-adapter", "open_gap", ("SRC-ARGO-DATA", "SRC-ARGO-USER", "SRC-CF", "SRC-WIGOS"), "live_calls", {
        "source_identities": ["Argo", "CF", "WIGOS"], "format_obligations": [], "metadata_obligations": [], "version_state": "watch", "live_calls": 0, "downloads": 0, "profile_rows": 0, "likelihood_evaluations": 0, "gap_open": True,
    }),
    spec(19, "ocean-observation-authority-matrix", "exact_gate", ("SRC-WIGOS", "SRC-ARGO-DATA"), "authority_decision_made", {
        "chairs": ["scientist", "operator", "deployment", "retrieval", "qc", "publication", "safety", "environmental", "legal", "affected_party", "cultural", "data_governance", "maori_authority"], "occupied_chairs": 0, "decisions": [], "authority_decision_made": False, "gate_open": True,
    }),
    spec(20, "stage20-ocean-profile-refusal", "completed", ("SRC-ARGO-FAQ", "SRC-NIST-TN1297", "SRC-WCAG22"), "admitted_evidence_rows", {
        "governed_observations": False, "calibrated_instruments": False, "validated_models": False, "expert_review": False, "affected_party_legitimacy": False, "independent_reproduction": False, "admitted_evidence_rows": 0, "stage_20_ready": False,
    }),
)

SPEC_BY_SLUG = {row["surface"]: row for row in SURFACE_SPECS}
SPEC_BY_ID = {row["proposal_id"]: row for row in SURFACE_SPECS}
if len(SPEC_BY_SLUG) != 20 or len(SPEC_BY_ID) != 20:
    raise RuntimeError("surface identifiers must be unique")

RUNNER_PROFILES = {
    "cycle-topology": ("float-cycle-metadata-topology", "platform-sensor-epoch-obligations"),
    "coordinates-calibration": ("profile-coordinate-unit-time-guard", "calibration-coefficient-vacancy"),
    "quality-streams": ("qc-flag-lineage", "realtime-delayedmode-separation"),
    "formats-provenance": ("netcdf-format-structural-refusal", "gdac-index-snapshot-provenance"),
    "gmut-boundaries": ("gmut-ocean-state-obligation", "gmut-observation-discrepancy"),
    "thos-freed-id": ("thos-delayedmode-handover", "freed-id-profile-claim-shell"),
    "missingness-amendment": ("missingness-vertical-sampling-quarantine", "profile-amendment-supersession"),
    "access-minimization": ("accessible-ocean-profile-dossier", "geospatial-minimization-firewall"),
    "integrity-adapter-authority": ("argo-card-byte-tribunal", "zero-row-argo-adapter", "ocean-observation-authority-matrix"),
    "terminal-refusal": ("stage20-ocean-profile-refusal",),
}


def ghc_family_build_ocean_profile_fixture(surface: str) -> dict[str, Any]:
    try:
        frozen = SPEC_BY_SLUG[surface]
    except KeyError as exc:
        raise EvidenceError(f"unknown ocean-profile surface: {surface}") from exc
    fixture: dict[str, Any] = {
        "schema": SCHEMA,
        "phase": PHASE,
        "proposal_id": frozen["proposal_id"],
        "surface": surface,
        "synthetic": True,
        "real_world_rows": 0,
        "authority": "none",
        "expected_outcome": frozen["expected_outcome"],
        "source_ids": list(frozen["source_ids"]),
        "protected_gates": list(PROTECTED_GATES),
    }
    fixture.update({field: False for field in REFUSAL_FIELDS})
    fixture.update(deepcopy(frozen["required"]))
    return fixture


def ghc_family_validate_ocean_profile_surface(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise EvidenceError("ocean-profile fixture must be a JSON object")
    surface = record.get("surface")
    if not isinstance(surface, str) or surface not in SPEC_BY_SLUG:
        raise EvidenceError("ocean-profile fixture declares an unknown surface")
    frozen = SPEC_BY_SLUG[surface]
    expected = ghc_family_build_ocean_profile_fixture(surface)
    missing = sorted(set(expected) - set(record))
    extra = sorted(set(record) - set(expected))
    if missing or extra:
        raise EvidenceError(f"surface key set differs; missing={missing}, extra={extra}")
    if record.get("synthetic") is not True or record.get("real_world_rows") != 0:
        raise EvidenceError("fixture must remain synthetic with zero real-world rows")
    if record.get("authority") != "none":
        raise EvidenceError("fixture cannot claim authority")
    if record.get("proposal_id") != frozen["proposal_id"] or record.get("expected_outcome") != frozen["expected_outcome"]:
        raise EvidenceError("proposal or outcome differs from the frozen surface")
    if record.get("source_ids") != list(frozen["source_ids"]):
        raise EvidenceError("source identifiers differ from the frozen source map")
    if record.get("protected_gates") != list(PROTECTED_GATES):
        raise EvidenceError("protected-gate list differs from the family contract")
    for field in REFUSAL_FIELDS:
        if record.get(field) is not False:
            raise EvidenceError(f"protected refusal field promoted: {field}")
    for field, value in frozen["required"].items():
        if record.get(field) != value:
            raise EvidenceError(f"surface contract differs at {field}")
    return {
        "schema": f"{SCHEMA}.validation",
        "proposal_id": frozen["proposal_id"],
        "surface": surface,
        "outcome": frozen["expected_outcome"],
        "fixture_sha256": digest(record),
        "real_world_rows": 0,
        "authority": "none",
        "protected_gates_open": list(PROTECTED_GATES),
        "valid": True,
        "boundary": "Owner-local synthetic zero-row software witness only; no float, profile, coordinate, measurement, calibration, QC decision, mission, scientific inference, professional judgment, authority, production, empirical, or Stage 20 result.",
    }


def ghc_family_build_ocean_profile_mutations(surface: str) -> list[dict[str, Any]]:
    fixture = ghc_family_build_ocean_profile_fixture(surface)
    frozen = SPEC_BY_SLUG[surface]
    rows = []
    for label, field, value in (
        ("synthetic boundary removed", "synthetic", False),
        ("real-world row injected", "real_world_rows", 1),
        ("authority promoted", "authority", "professional"),
        ("protected refusal promoted", "production_ready", True),
        ("surface-critical field changed", frozen["critical_field"], "__invalid_mutation__"),
    ):
        mutated = deepcopy(fixture)
        mutated[field] = value
        rows.append({"label": label, "field": field, "record": mutated})
    return rows


def ghc_family_execute_ocean_profile_surface(surface: str) -> dict[str, Any]:
    positive = ghc_family_build_ocean_profile_fixture(surface)
    positive_result = ghc_family_validate_ocean_profile_surface(positive)
    mutations = []
    for index, mutation in enumerate(ghc_family_build_ocean_profile_mutations(surface), 1):
        try:
            ghc_family_validate_ocean_profile_surface(mutation["record"])
        except EvidenceError as exc:
            mutations.append({"mutation_id": f"{SPEC_BY_SLUG[surface]['proposal_id']}-M{index:02d}", "label": mutation["label"], "field": mutation["field"], "rejected": True, "failure_class": type(exc).__name__, "reason": str(exc), "completion_credit": 0})
        else:
            mutations.append({"mutation_id": f"{SPEC_BY_SLUG[surface]['proposal_id']}-M{index:02d}", "label": mutation["label"], "field": mutation["field"], "rejected": False, "failure_class": None, "reason": "mutation was incorrectly accepted", "completion_credit": 0})
    return {
        "schema": f"{SCHEMA}.surface-execution",
        "proposal_id": SPEC_BY_SLUG[surface]["proposal_id"],
        "surface": surface,
        "outcome": SPEC_BY_SLUG[surface]["expected_outcome"],
        "positive_fixture": positive,
        "positive_result": positive_result,
        "mutation_count": len(mutations),
        "rejected_mutation_count": sum(bool(row["rejected"]) for row in mutations),
        "mutations": mutations,
        "post_success_replay": False,
        "valid": positive_result["valid"] and all(row["rejected"] for row in mutations),
    }


def ghc_family_run_ocean_profile(profile: str) -> dict[str, Any]:
    try:
        surfaces = RUNNER_PROFILES[profile]
    except KeyError as exc:
        raise EvidenceError(f"unknown ocean-profile runner profile: {profile}") from exc
    executions = [ghc_family_execute_ocean_profile_surface(surface) for surface in surfaces]
    return {
        "schema": f"{SCHEMA}.runner-profile",
        "family_current_runner": f"ghc_family_ocean_profile_{profile.replace('-', '_')}",
        "profile": profile,
        "surfaces": list(surfaces),
        "proposal_ids": [row["proposal_id"] for row in executions],
        "surface_count": len(executions),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "network_calls": 0,
        "downloads": 0,
        "profile_rows": 0,
        "real_world_rows": 0,
        "valid": all(row["valid"] for row in executions),
        "boundary": "Fixed owner-local profile only; not an observing, QC, calibration, mission, identity, rights, professional, empirical, production, cultural, legal, or authority system.",
    }


def outcome_counts(values: Iterable[str]) -> dict[str, int]:
    counts = {key: 0 for key in ("completed", "represented", "open_gap", "exact_gate")}
    for value in values:
        if value not in ALLOWED_OUTCOMES:
            raise EvidenceError(f"unknown outcome: {value}")
        counts[value] += 1
    return counts


def ghc_family_execute_v664_v6() -> dict[str, Any]:
    executions = [ghc_family_execute_ocean_profile_surface(row["surface"]) for row in SURFACE_SPECS]
    runners = [ghc_family_run_ocean_profile(profile) for profile in RUNNER_PROFILES]
    outcomes = outcome_counts(row["outcome"] for row in executions)
    valid = len(executions) == 20 and outcomes == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1} and sum(row["rejected_mutation_count"] for row in executions) == 100 and all(row["valid"] for row in executions + runners)
    return {
        "schema": f"{SCHEMA}.phase-execution",
        "phase": PHASE,
        "surface_count": len(executions),
        "executions": executions,
        "outcome_counts": outcomes,
        "mutation_count": 100,
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "runner_profile_count": len(runners),
        "runner_results": runners,
        "network_calls": 0,
        "downloads": 0,
        "profile_rows": 0,
        "real_world_rows": 0,
        "valid": valid,
        "verdict": "NOT_READY_FOR_STAGE_20",
    }


build_ghc_family_v664_v6_evidence = ghc_family_execute_v664_v6
ghc_family_validate_v664_v6_surface = ghc_family_validate_ocean_profile_surface
ghc_family_run_v664_v6_profile = ghc_family_run_ocean_profile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("all", *RUNNER_PROFILES), default="all")
    args = parser.parse_args()
    try:
        payload = ghc_family_execute_v664_v6() if args.profile == "all" else ghc_family_run_ocean_profile(args.profile)
    except (EvidenceError, TypeError, ValueError) as exc:
        print(f"GHC_FAMILY_OCEAN_PROFILE_EVIDENCE_ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
