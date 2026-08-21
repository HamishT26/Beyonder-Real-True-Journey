#!/usr/bin/env python3
"""Build bounded synthetic structural-monitoring evidence for GHC family phases.

The engine validates exact owner-local declarations and refusal boundaries. It
does not read waveforms, inspect a structure, calibrate sensors, identify a
person or place, infer damage, decide safety or rights, or claim engineering,
legal, cultural, Maori, professional, operational, or empirical authority.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from copy import deepcopy
import hashlib
import json
import sys
from typing import Any


SCHEMA = "ghc.family.structural-monitoring-evidence.v1"
PHASE = "v664-v5"
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
    """Raised when a synthetic fixture violates its frozen contract."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def spec(
    number: int,
    surface: str,
    outcome: str,
    sources: Iterable[str],
    critical_field: str,
    required: dict[str, Any],
) -> dict[str, Any]:
    if outcome not in ALLOWED_OUTCOMES:
        raise RuntimeError(f"unsupported surface outcome: {outcome}")
    if critical_field not in required:
        raise RuntimeError(f"critical field is absent from {surface}")
    return {
        "proposal_id": f"IF6645-N{number:03d}",
        "surface": surface,
        "expected_outcome": outcome,
        "source_ids": list(sources),
        "critical_field": critical_field,
        "required": required,
    }


SURFACE_SPECS = (
    spec(1, "sensor-array-topology", "completed", ("SRC-USGS-NSMP", "SRC-FHWA-SHM"), "condition_conclusion", {
        "structure_token": "syn:structure:001", "nodes": ["foundation", "floor-a", "floor-b", "roof", "sensor-a", "sensor-b"], "edges": [["foundation", "floor-a"], ["floor-a", "floor-b"], ["floor-b", "roof"], ["floor-a", "sensor-a"], ["roof", "sensor-b"]], "orphan_channels": [], "real_sensors": 0, "condition_conclusion": False,
    }),
    spec(2, "channel-epoch-response-obligations", "completed", ("SRC-FDSN-STATIONXML", "SRC-USGS-NSMP-DATA"), "response_chain_complete", {
        "source_identifier": "FDSN:SY_TEST_00_HN_Z", "epoch_state": "synthetic", "response_stages": ["sensor", "digitizer"], "unit_path": ["m/s^2", "count"], "uncertainty_state": "vacant", "observed_stations": 0, "response_chain_complete": False,
    }),
    spec(3, "clock-synchronization-uncertainty", "completed", ("SRC-FDSN-MSEED3", "SRC-NIST-TN1297"), "measured_corrections", {
        "nominal_rate_hz": 200, "offset_state": "vacant", "drift_state": "vacant", "leap_state": "unresolved", "covariance_state": "vacant", "measured_corrections": 0, "timing_conclusion": False,
    }),
    spec(4, "orientation-unit-coordinate-guard", "completed", ("SRC-FDSN-STATIONXML", "SRC-NIST-TN1297"), "real_geometry_rows", {
        "coordinate_frame": "synthetic_local_right_handed", "axes": ["X", "Y", "Z"], "polarity_state": "declared", "acceleration_unit": "m/s^2", "conversion_lineage": ["count", "m/s^2"], "real_geometry_rows": 0, "orientation_verified": False,
    }),
    spec(5, "acquisition-provenance-event-chain", "completed", ("SRC-PROV", "SRC-RFC8785"), "acquired_samples", {
        "event_chain": ["configuration", "trigger", "record", "transform", "checksum", "supersession", "invalidation"], "recorder_state": "synthetic", "firmware_state": "placeholder", "checksum_state": "synthetic_digest", "acquired_samples": 0, "authenticity_claimed": False,
    }),
    spec(6, "miniseed-header-refusal", "completed", ("SRC-FDSN-MSEED3", "SRC-RFC8785"), "payload_bytes", {
        "format_version": 3, "source_identifier": "FDSN:SY_TEST_00_HN_Z", "time_quality_state": "vacant", "encoding_state": "placeholder", "extra_header_policy": "unknown_retain", "checksum_state": "vacant", "payload_bytes": 0, "conformance_certified": False,
    }),
    spec(7, "stationxml-response-completeness", "completed", ("SRC-FDSN-STATIONXML", "SRC-NIST-TN1297"), "schema_conformance_certified", {
        "hierarchy": ["network", "station", "channel", "response"], "epoch_state": "synthetic", "equipment_state": "placeholder", "stage_sequence": [1, 2], "input_unit": "m/s^2", "output_unit": "count", "availability_state": "vacant", "schema_conformance_certified": False,
    }),
    spec(8, "window-aliasing-leakage-quarantine", "completed", ("SRC-USGS-NSMP-DATA", "SRC-NIST-TN1297"), "spectral_estimates", {
        "window": "hann", "sampling_rate_hz": 200, "nyquist_hz": 100, "antialias_state": "unverified", "overlap_fraction": 0.5, "padding_state": "declared", "filter_transient_state": "quarantined", "spectral_estimates": 0, "damage_inference": False,
    }),
    spec(9, "gmut-modal-obligation-board", "represented", ("SRC-FHWA-SHM", "SRC-FEMA-P58"), "empirical_parameter_rows", {
        "state_variables": ["u(t)", "a(t)"], "operators": ["M", "C", "K"], "eigenpair_domain": "symbolic", "boundary_state": "unresolved", "unit_state": "typed", "observation_firewall": True, "empirical_parameter_rows": 0, "physical_solution_claimed": False,
    }),
    spec(10, "gmut-model-discrepancy-separation", "represented", ("SRC-NIST-TN1297", "SRC-FEMA-P58"), "physical_inference", {
        "terms": ["excitation", "sensor_response", "environment", "operation", "truncation", "residual"], "covariance_state": "vacant", "identifiability_state": "unresolved", "coefficient_rows": 0, "damage_label": "not_identifiable", "physical_inference": False,
    }),
    spec(11, "thos-vibration-handover", "represented", ("SRC-FHWA-SHM", "SRC-USGS-NSMP"), "service_performance_measured", {
        "people": 0, "states": ["intake", "clock_hold", "metadata_hold", "anomaly_quarantine", "correction_readback", "handover", "stop"], "workload_ceiling": 3, "stop_latch": True, "accepted_handover": False, "service_performance_measured": False,
    }),
    spec(12, "freed-id-dataset-claim-shell", "represented", ("SRC-PROV", "SRC-RFC8785"), "identity_claimed", {
        "dataset_token": "syn:vibration-dataset:001", "digest": "sha256:synthetic", "issuer_state": "vacant", "subject_state": "vacant", "controller_state": "vacant", "verification_material_state": "absent", "status_state": "hold", "consent_state": "vacant", "revocation_state": "vacant", "identity_claimed": False,
    }),
    spec(13, "missingness-saturation-dropout", "completed", ("SRC-USGS-NSMP-DATA", "SRC-FDSN-MSEED3"), "detected_events", {
        "event_roles": ["missing_channel", "saturation", "clipping", "dropout", "trigger_censoring", "telemetry_gap", "maintenance_window"], "denominator_state": "explicit_zero_observations", "cause_state": "unresolved", "detected_events": 0, "denominator_repaired": False,
    }),
    spec(14, "intervention-amendment-trace", "completed", ("SRC-PROV", "SRC-FDSN-STATIONXML"), "maintenance_actions", {
        "fields": ["orientation", "gain", "location", "timing", "firmware", "channel_mapping", "checksum", "challenge"], "append_only": True, "challenge_state": "unresolved", "adjudicator_state": "vacant", "maintenance_actions": 0, "adjudication_performed": False,
    }),
    spec(15, "accessible-vibration-dossier", "completed", ("SRC-WCAG22", "SRC-NIST-TN1297"), "manual_evaluation_complete", {
        "semantic_headings": True, "captioned_tables": True, "text_plot_alternative": True, "uncertainty_labels": True, "status_explanation": True, "print_fallback": True, "manual_evaluation_complete": False, "affected_user_evaluation_complete": False,
    }),
    spec(16, "monitoring-data-minimization", "completed", ("SRC-PROV", "SRC-WCAG22"), "privacy_complete", {
        "asset_token": "syn:asset:001", "exact_location_allowed": False, "contact_field_allowed": False, "purpose_enum_required": True, "free_text_allowed": False, "retention_state": "vacant", "disclosure_state": "locked", "correction_state": "placeholder", "privacy_complete": False,
    }),
    spec(17, "canonical-fixture-integrity", "completed", ("SRC-RFC8785", "SRC-PROV"), "authenticity_claimed", {
        "strict_json": True, "deterministic_order": True, "git_blob_domain": True, "self_exclusions_explicit": True, "supersession_state": "append_only", "signature_present": False, "authenticity_claimed": False,
    }),
    spec(18, "zero-row-nsmp-adapter", "open_gap", ("SRC-USGS-NSMP-DATA", "SRC-FDSN-MSEED3", "SRC-FDSN-STATIONXML"), "live_calls", {
        "product_identity": "USGS_NSMP_FDSN_WATCH", "schema_pins": ["miniseed3-watch", "stationxml-1.2-watch"], "live_calls": 0, "downloads": 0, "waveform_rows": 0, "response_rows": 0, "likelihood_evaluations": 0, "data_authority": False, "gap_open": True,
    }),
    spec(19, "structural-safety-authority-matrix", "exact_gate", ("SRC-FEMA-P58", "SRC-FHWA-SHM"), "authority_decision_made", {
        "chairs": ["engineer", "owner", "occupant", "regulator", "emergency_authority", "affected_party", "legal", "cultural", "data_governance", "maori_authority"], "occupied_chairs": 0, "decisions": [], "authority_decision_made": False, "gate_open": True,
    }),
    spec(20, "stage20-strong-motion-refusal", "completed", ("SRC-USGS-NSMP", "SRC-NIST-TN1297", "SRC-WCAG22"), "admitted_evidence_rows", {
        "calibrated_instrumentation": False, "governed_data": False, "validated_models": False, "professional_review": False, "affected_party_legitimacy": False, "independent_reproduction": False, "admitted_evidence_rows": 0, "stage_20_ready": False,
    }),
)

SPEC_BY_SLUG = {row["surface"]: row for row in SURFACE_SPECS}
SPEC_BY_ID = {row["proposal_id"]: row for row in SURFACE_SPECS}
if len(SPEC_BY_SLUG) != 20 or len(SPEC_BY_ID) != 20:
    raise RuntimeError("surface identifiers must be unique")

RUNNER_PROFILES = {
    "sensor-topology": ("sensor-array-topology", "channel-epoch-response-obligations"),
    "timebase-units": ("clock-synchronization-uncertainty", "orientation-unit-coordinate-guard"),
    "provenance-formats": ("acquisition-provenance-event-chain", "miniseed-header-refusal"),
    "metadata-analysis": ("stationxml-response-completeness", "window-aliasing-leakage-quarantine"),
    "gmut-boundaries": ("gmut-modal-obligation-board", "gmut-model-discrepancy-separation"),
    "thos-freed-id": ("thos-vibration-handover", "freed-id-dataset-claim-shell"),
    "missingness-amendment": ("missingness-saturation-dropout", "intervention-amendment-trace"),
    "access-privacy": ("accessible-vibration-dossier", "monitoring-data-minimization"),
    "adapter-authority": ("canonical-fixture-integrity", "zero-row-nsmp-adapter", "structural-safety-authority-matrix"),
    "terminal-refusal": ("stage20-strong-motion-refusal",),
}


def ghc_family_build_structural_monitoring_fixture(surface: str) -> dict[str, Any]:
    """Return one deterministic zero-row synthetic fixture."""

    try:
        frozen = SPEC_BY_SLUG[surface]
    except KeyError as exc:
        raise EvidenceError(f"unknown structural-monitoring surface: {surface}") from exc
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


def ghc_family_validate_structural_monitoring_surface(record: Any) -> dict[str, Any]:
    """Validate one fixture against its complete exact-key contract."""

    if not isinstance(record, dict):
        raise EvidenceError("structural-monitoring fixture must be a JSON object")
    surface = record.get("surface")
    if not isinstance(surface, str) or surface not in SPEC_BY_SLUG:
        raise EvidenceError("structural-monitoring fixture declares an unknown surface")
    frozen = SPEC_BY_SLUG[surface]
    expected = ghc_family_build_structural_monitoring_fixture(surface)
    missing = sorted(set(expected) - set(record))
    extra = sorted(set(record) - set(expected))
    if missing or extra:
        raise EvidenceError(f"surface key set differs; missing={missing}, extra={extra}")
    if record.get("synthetic") is not True or record.get("real_world_rows") != 0:
        raise EvidenceError("fixture must remain synthetic with zero real-world rows")
    if record.get("authority") != "none":
        raise EvidenceError("fixture cannot claim authority")
    if record.get("proposal_id") != frozen["proposal_id"]:
        raise EvidenceError("proposal identifier differs from the frozen surface")
    if record.get("expected_outcome") != frozen["expected_outcome"]:
        raise EvidenceError("fixture outcome differs from the frozen disposition")
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
        "boundary": "Owner-local synthetic software witness only; no real structure, sensor, waveform, person, location, equipment, inspection, measurement, calibration, damage inference, safety decision, professional judgment, authority, production, empirical, or Stage 20 result.",
    }


def ghc_family_build_structural_monitoring_mutations(surface: str) -> list[dict[str, Any]]:
    """Return five preregistered rejecting mutations for one surface."""

    fixture = ghc_family_build_structural_monitoring_fixture(surface)
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


def ghc_family_execute_structural_monitoring_surface(surface: str) -> dict[str, Any]:
    """Run the positive fixture and all rejecting mutations once."""

    positive = ghc_family_build_structural_monitoring_fixture(surface)
    positive_result = ghc_family_validate_structural_monitoring_surface(positive)
    mutation_results = []
    for index, mutation in enumerate(ghc_family_build_structural_monitoring_mutations(surface), 1):
        try:
            ghc_family_validate_structural_monitoring_surface(mutation["record"])
        except EvidenceError as exc:
            mutation_results.append({
                "mutation_id": f"{SPEC_BY_SLUG[surface]['proposal_id']}-M{index:02d}",
                "label": mutation["label"],
                "field": mutation["field"],
                "rejected": True,
                "failure_class": type(exc).__name__,
                "reason": str(exc),
                "completion_credit": 0,
            })
        else:
            mutation_results.append({
                "mutation_id": f"{SPEC_BY_SLUG[surface]['proposal_id']}-M{index:02d}",
                "label": mutation["label"],
                "field": mutation["field"],
                "rejected": False,
                "failure_class": None,
                "reason": "mutation was incorrectly accepted",
                "completion_credit": 0,
            })
    return {
        "schema": f"{SCHEMA}.surface-execution",
        "proposal_id": SPEC_BY_SLUG[surface]["proposal_id"],
        "surface": surface,
        "outcome": SPEC_BY_SLUG[surface]["expected_outcome"],
        "positive_fixture": positive,
        "positive_result": positive_result,
        "mutation_count": len(mutation_results),
        "rejected_mutation_count": sum(bool(row["rejected"]) for row in mutation_results),
        "mutations": mutation_results,
        "post_success_replay": False,
        "valid": positive_result["valid"] and all(row["rejected"] for row in mutation_results),
    }


def ghc_family_run_structural_monitoring_profile(profile: str) -> dict[str, Any]:
    """Invoke one family-current fixed bounded runner profile."""

    try:
        surfaces = RUNNER_PROFILES[profile]
    except KeyError as exc:
        raise EvidenceError(f"unknown structural-monitoring runner profile: {profile}") from exc
    executions = [ghc_family_execute_structural_monitoring_surface(surface) for surface in surfaces]
    return {
        "schema": f"{SCHEMA}.runner-profile",
        "family_current_runner": f"ghc_family_structural_monitoring_{profile.replace('-', '_')}",
        "profile": profile,
        "surfaces": list(surfaces),
        "proposal_ids": [row["proposal_id"] for row in executions],
        "surface_count": len(executions),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "network_calls": 0,
        "waveform_reads": 0,
        "real_world_rows": 0,
        "valid": all(row["valid"] for row in executions),
        "boundary": "Family-compatible owner-local profile only; not a monitoring, inspection, calibration, safety, identity, rights, professional, empirical, production, cultural, legal, or authority system.",
    }


def outcome_counts(values: Iterable[str]) -> dict[str, int]:
    counts = {key: 0 for key in ("completed", "represented", "open_gap", "exact_gate")}
    for value in values:
        if value not in ALLOWED_OUTCOMES:
            raise EvidenceError(f"unknown outcome: {value}")
        counts[value] += 1
    return counts


def ghc_family_execute_v664_v5() -> dict[str, Any]:
    """Execute every frozen surface exactly once in one build call."""

    executions = [ghc_family_execute_structural_monitoring_surface(row["surface"]) for row in SURFACE_SPECS]
    runners = [ghc_family_run_structural_monitoring_profile(profile) for profile in RUNNER_PROFILES]
    outcomes = outcome_counts(row["outcome"] for row in executions)
    expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    valid = (
        len(executions) == 20
        and outcomes == expected
        and sum(row["rejected_mutation_count"] for row in executions) == 100
        and all(row["valid"] for row in executions)
        and all(row["valid"] for row in runners)
    )
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
        "waveform_reads": 0,
        "real_world_rows": 0,
        "valid": valid,
        "verdict": "NOT_READY_FOR_STAGE_20",
    }


# Additive discoverable phase aliases; family-current names remain primary.
build_ghc_family_v664_v5_evidence = ghc_family_execute_v664_v5
ghc_family_validate_v664_v5_surface = ghc_family_validate_structural_monitoring_surface
ghc_family_run_v664_v5_profile = ghc_family_run_structural_monitoring_profile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("all", *RUNNER_PROFILES), default="all")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = (
            ghc_family_execute_v664_v5()
            if args.profile == "all"
            else ghc_family_run_structural_monitoring_profile(args.profile)
        )
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload["valid"] else 2
    except (EvidenceError, TypeError, ValueError) as exc:
        print(f"GHC_FAMILY_STRUCTURAL_MONITORING_EVIDENCE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
