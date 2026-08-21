#!/usr/bin/env python3
"""Bounded synthetic tide-gauge marigram evidence engine for GHC family phases.

The engine validates owner-local declarations and refusal boundaries only.  It
does not inspect a real chart, install or calibrate a gauge, realize a datum,
digitize a trace, make a prediction, conduct a survey, infer sea-level change,
decide rights, or perform any identity, professional, operational, or authority action.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import re
import sys
from typing import Any, Iterable


SCHEMA = "ghc.family.marigram-evidence.v1"
PHASE = "v664-v2"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_GATES = (
    "empirical",
    "participant",
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


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _spec(
    number: int,
    slug: str,
    outcome: str,
    sources: Iterable[str],
    critical_field: str,
    required: dict[str, Any],
) -> dict[str, Any]:
    if outcome not in ALLOWED_OUTCOMES:
        raise RuntimeError(f"unsupported surface outcome: {outcome}")
    if critical_field not in required:
        raise RuntimeError(f"critical field is absent from {slug}")
    return {
        "proposal_id": f"NE6642-N{number:03d}",
        "surface": slug,
        "expected_outcome": outcome,
        "source_ids": list(sources),
        "critical_field": critical_field,
        "required": required,
    }


SURFACE_SPECS = (
    _spec(1, "marigram-archive-capsule", "completed", ("SRC-PREMIS", "SRC-IOC-SEA"), "sea_level_claim", {
        "station_token": "syn:tide-station:001", "chart_roll_relation": "synthetic_only", "datum_state": "vacant", "revision": 1, "custody_state": "hold", "authenticated": False, "sea_level_claim": False,
    }),
    _spec(2, "gauge-component-topology", "completed", ("SRC-IOC-SEA",), "instrument_condition_assessed", {
        "components": ["float", "stilling_well", "inlet", "counterweight", "drum", "clock", "pen", "paper_chart", "benchmark", "surrogate"], "orphan_state": "quarantined", "instrument_condition_assessed": False, "topology_complete": False,
    }),
    _spec(3, "written-mark-register", "completed", ("SRC-PREMIS", "SRC-PROV"), "attribution_claimed", {
        "layers": ["heading", "margin_note", "overwritten_stroke", "unreadable_span", "editorial_supply", "contested_reading"], "conflict_state": "retained", "attribution_claimed": False, "real_text_rows": 0,
    }),
    _spec(4, "datum-dependency-graph", "completed", ("SRC-NOAA-DATUM", "SRC-PSMSL-RLR", "SRC-LINZ-LVD"), "vertical_reference_realized", {
        "zero_nodes": ["gauge_zero", "chart_zero", "staff_zero"], "reference_nodes": ["benchmark", "local_datum", "national_datum_placeholder"], "epoch_state": "vacant", "offset_state": "vacant", "transformation_rows": 0, "vertical_reference_realized": False,
    }),
    _spec(5, "chart-time-envelope", "completed", ("SRC-IOC-SEA", "SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "timing_observation_rows", {
        "timezone_state": "vacant", "civil_time_scale": "unknown", "drum_period": "placeholder", "start_mark": "synthetic", "end_mark": "synthetic", "drift_state": "unresolved", "discontinuity_state": "hold", "uncertainty_state": "unresolved", "timing_observation_rows": 0,
    }),
    _spec(6, "geometry-scale-envelope", "completed", ("SRC-IOC-SEA", "SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "calibration_rows", {
        "drum_circumference": "placeholder", "paper_advance": "placeholder", "pen_ordinate": "placeholder", "float_ratio": "placeholder", "inlet_damping": "placeholder", "axis_state": "typed", "unit_state": "vacant", "covariance_state": "unresolved", "calibration_rows": 0,
    }),
    _spec(7, "digitization-provenance", "completed", ("SRC-PREMIS", "SRC-PROV", "SRC-RFC8785"), "extraction_rows", {
        "source_chart": "syn:marigram:chart:001", "scan_state": "vacant", "control_point_rows": 0, "trace_version": "placeholder", "interpolation_state": "hold", "operator_state": "vacant", "derivative_state": "proposed", "extraction_rows": 0,
    }),
    _spec(8, "trace-state-ledger", "completed", ("SRC-PREMIS", "SRC-PROV"), "trace_reconstruction_claimed", {
        "states": ["tear", "fold", "ink_dropout", "overtrace", "splice", "reversal", "margin_loss", "duplicate", "gap"], "gap_mask_present": True, "undecidable_segments": 2, "reconstructed_ordinates": 0, "trace_reconstruction_claimed": False,
    }),
    _spec(9, "unit-uncertainty-registry", "completed", ("SRC-NIST-SI", "SRC-NIST-UNCERTAINTY", "SRC-NOAA-DATUM"), "measurement_rows", {
        "axes": ["water_level_ordinate", "time_abscissa"], "conversion_state": "placeholder", "significant_figure_state": "hold", "uncertainty_state": "unresolved", "measurement_rows": 0,
    }),
    _spec(10, "series-role-ledger", "completed", ("SRC-PREMIS", "SRC-PROV", "SRC-RFC8785"), "fidelity_claimed", {
        "series_roles": ["raw_trace", "digitized_ordinate", "datum_adjusted_placeholder", "filtered_placeholder", "residual_placeholder"], "fixity_state": "synthetic", "invalidation_state": "available", "fidelity_claimed": False,
    }),
    _spec(11, "thos-admission-machine", "represented", ("SRC-IOC-SEA", "SRC-PROV"), "operational_effectiveness", {
        "people": 0, "datum_pending_count": 2, "datum_pending_ceiling": 2, "freeze_token": True, "discrepancy_echo": "synthetic_digest", "queue_debt": 1, "transfer_digest": "sha256:synthetic", "operational_effectiveness": False,
    }),
    _spec(12, "gmut-tide-series-chart", "represented", ("SRC-NIST-SI", "SRC-NIST-UNCERTAINTY", "SRC-NOAA-DATUM"), "observation_rows", {
        "time_coordinate": "symbolic", "water_level_state": "symbolic", "constituent_basis": "placeholder", "datum_operator": "placeholder", "residual_channel": "vacant", "units_state": "typed", "covariance_state": "vacant", "observation_rows": 0,
    }),
    _spec(13, "gmut-confounder-decomposition", "represented", ("SRC-NIST-UNCERTAINTY", "SRC-NOAA-DATUM", "SRC-PSMSL-RLR", "SRC-LINZ-SEA"), "physical_inference", {
        "terms": ["datum_step", "clock_drift", "inlet_response", "meteorological_confounder", "tidal_constituent"], "coefficient_rows": 0, "identifiability_state": "unresolved", "physical_inference": False,
    }),
    _spec(14, "freed-id-station-assertion", "represented", ("SRC-W3C-VC20", "SRC-RFC8785", "SRC-PREMIS"), "ownership_claimed", {
        "surrogate_station": "syn:tide-station:001", "chart_digest": "sha256:synthetic", "claimant_state": "vacant", "proof_state": "absent", "purpose_state": "restricted", "revocation_state": "hold", "identity_claimed": False, "ownership_claimed": False,
    }),
    _spec(15, "metadata-amendment-trail", "completed", ("SRC-W3C-VC20", "SRC-PROV", "SRC-PREMIS"), "live_governance_operation", {
        "chain": ["station_hypothesis", "datum_state", "timebase_state", "reason_code", "supersession", "challenge"], "challenger_state": "placeholder", "resolution_state": "unresolved", "append_only": True, "live_governance_operation": False,
    }),
    _spec(16, "accessible-marigram-dossier", "completed", ("SRC-WCAG22", "SRC-PROV"), "manual_evaluation_complete", {
        "component_crosswalk": True, "plain_language_datum_account": True, "text_described_trace_states": True, "table_fallback": True, "paged_rendering": True, "manual_evaluation_complete": False, "affected_user_evaluation_complete": False,
    }),
    _spec(17, "context-minimization-register", "completed", ("SRC-NZ-PRIVACY", "SRC-WCAG22"), "privacy_complete", {
        "station_context_rows": 0, "purpose_bound_fields": True, "free_text_allowed": False, "contact_data_allowed": False, "correction_pathway_state": "placeholder", "disclosure_state": "freeze", "deletion_cue": "declared", "privacy_complete": False,
    }),
    _spec(18, "zero-row-tide-adapter", "open_gap", ("SRC-NOAA-PRODUCTS", "SRC-PSMSL-RLR", "SRC-PREMIS"), "live_calls", {
        "schema_pins": ["noaa-coops-watch", "psmsl-rlr-watch"], "live_calls": 0, "downloads": 0, "version_state": "vacant", "data_authority": False, "gap_open": True,
    }),
    _spec(19, "rights-authority-matrix", "exact_gate", ("SRC-TE-MANA-RARAUNGA", "SRC-NZ-PRIVACY", "SRC-LINZ-LVD"), "authority_decision_made", {
        "chairs": ["chart_custody", "station_land", "benchmark_access", "location_sensitivity", "traditional_knowledge", "publication", "remedy", "affected_parties", "maori_authority"], "occupied_chairs": 0, "authority_decision_made": False, "gate_open": True,
    }),
    _spec(20, "stage-20-refusal-proof", "completed", ("SRC-IOC-SEA", "SRC-W3C-VC20", "SRC-TE-MANA-RARAUNGA", "SRC-NOAA-DATUM"), "admitted_evidence_rows", {
        "governed_datum_realization": False, "calibrated_trace_extraction": False, "uncertainty_accounted": False, "rights_review": False, "affected_party_authority": False, "independent_reproduction": False, "admitted_evidence_rows": 0, "stage_20_ready": False,
    }),
)

SPEC_BY_SLUG = {spec["surface"]: spec for spec in SURFACE_SPECS}
SPEC_BY_ID = {spec["proposal_id"]: spec for spec in SURFACE_SPECS}
if len(SPEC_BY_SLUG) != 20 or len(SPEC_BY_ID) != 20:
    raise RuntimeError("surface identifiers must be unique")

RUNNER_PROFILES = {
    "archive-topology": ("marigram-archive-capsule", "gauge-component-topology"),
    "transcription-datum": ("written-mark-register", "datum-dependency-graph"),
    "time-geometry": ("chart-time-envelope", "geometry-scale-envelope"),
    "digitization-trace": ("digitization-provenance", "trace-state-ledger"),
    "units-series": ("unit-uncertainty-registry", "series-role-ledger"),
    "thos-gmut-boundaries": ("thos-admission-machine", "gmut-tide-series-chart", "gmut-confounder-decomposition"),
    "freed-id-boundaries": ("freed-id-station-assertion", "metadata-amendment-trail"),
    "access-privacy": ("accessible-marigram-dossier", "context-minimization-register"),
    "source-authority": ("zero-row-tide-adapter", "rights-authority-matrix"),
    "terminal-refusal": ("stage-20-refusal-proof",),
}


def ghc_family_build_marigram_fixture(surface: str) -> dict[str, Any]:
    """Return the deterministic positive fixture for one declared surface."""

    try:
        spec = SPEC_BY_SLUG[surface]
    except KeyError as exc:
        raise EvidenceError(f"unknown marigram surface: {surface}") from exc
    fixture: dict[str, Any] = {
        "schema": SCHEMA,
        "phase": PHASE,
        "proposal_id": spec["proposal_id"],
        "surface": surface,
        "synthetic": True,
        "real_world_rows": 0,
        "authority": "none",
        "expected_outcome": spec["expected_outcome"],
        "source_ids": list(spec["source_ids"]),
        "protected_gates": list(PROTECTED_GATES),
    }
    fixture.update({field: False for field in REFUSAL_FIELDS})
    fixture.update(deepcopy(spec["required"]))
    return fixture


def ghc_family_validate_marigram_surface(record: Any) -> dict[str, Any]:
    """Validate one fixture against its exact surface contract."""

    if not isinstance(record, dict):
        raise EvidenceError("marigram fixture must be a JSON object")
    surface = record.get("surface")
    if not isinstance(surface, str) or surface not in SPEC_BY_SLUG:
        raise EvidenceError("marigram fixture declares an unknown surface")
    spec = SPEC_BY_SLUG[surface]
    expected = ghc_family_build_marigram_fixture(surface)
    missing = sorted(set(expected) - set(record))
    extra = sorted(set(record) - set(expected))
    if missing or extra:
        raise EvidenceError(f"surface key set differs; missing={missing}, extra={extra}")
    if record.get("synthetic") is not True or record.get("real_world_rows") != 0:
        raise EvidenceError("fixture must remain synthetic with zero real-world rows")
    if record.get("authority") != "none":
        raise EvidenceError("fixture cannot claim authority")
    if record.get("proposal_id") != spec["proposal_id"]:
        raise EvidenceError("proposal identifier differs from the frozen surface")
    if record.get("expected_outcome") != spec["expected_outcome"]:
        raise EvidenceError("fixture outcome differs from the frozen disposition")
    if record.get("source_ids") != list(spec["source_ids"]):
        raise EvidenceError("source identifiers differ from the frozen source map")
    if record.get("protected_gates") != list(PROTECTED_GATES):
        raise EvidenceError("protected-gate list differs from the family contract")
    for field in REFUSAL_FIELDS:
        if record.get(field) is not False:
            raise EvidenceError(f"protected refusal field promoted: {field}")
    for field, value in spec["required"].items():
        if record.get(field) != value:
            raise EvidenceError(f"surface contract differs at {field}")
    return {
        "schema": f"{SCHEMA}.validation",
        "proposal_id": spec["proposal_id"],
        "surface": surface,
        "outcome": spec["expected_outcome"],
        "fixture_sha256": _digest(record),
        "real_world_rows": 0,
        "authority": "none",
        "protected_gates_open": list(PROTECTED_GATES),
        "valid": True,
        "boundary": "Owner-local synthetic software witness only; no real station, chart, benchmark, datum, person, right, measurement, calibration, prediction, survey, authority, production, empirical, or Stage 20 result.",
    }


def ghc_family_build_marigram_mutations(surface: str) -> list[dict[str, Any]]:
    """Return four preregistered rejecting mutations for one surface."""

    fixture = ghc_family_build_marigram_fixture(surface)
    spec = SPEC_BY_SLUG[surface]
    rows = []
    for label, field, value in (
        ("synthetic boundary removed", "synthetic", False),
        ("real-world row injected", "real_world_rows", 1),
        ("authority promoted", "authority", "professional"),
        ("surface-critical field changed", spec["critical_field"], "__invalid_mutation__"),
    ):
        mutated = deepcopy(fixture)
        mutated[field] = value
        rows.append({"label": label, "field": field, "record": mutated})
    return rows


def ghc_family_execute_marigram_surface(surface: str) -> dict[str, Any]:
    """Run the positive fixture and all four rejecting mutations once."""

    positive = ghc_family_build_marigram_fixture(surface)
    positive_result = ghc_family_validate_marigram_surface(positive)
    mutation_results = []
    for index, mutation in enumerate(ghc_family_build_marigram_mutations(surface), start=1):
        try:
            ghc_family_validate_marigram_surface(mutation["record"])
        except EvidenceError as exc:
            mutation_results.append(
                {
                    "mutation_id": f"{SPEC_BY_SLUG[surface]['proposal_id']}-M{index:02d}",
                    "label": mutation["label"],
                    "field": mutation["field"],
                    "rejected": True,
                    "failure_class": type(exc).__name__,
                    "reason": str(exc),
                    "completion_credit": 0,
                }
            )
        else:
            mutation_results.append(
                {
                    "mutation_id": f"{SPEC_BY_SLUG[surface]['proposal_id']}-M{index:02d}",
                    "label": mutation["label"],
                    "field": mutation["field"],
                    "rejected": False,
                    "failure_class": None,
                    "reason": "mutation was incorrectly accepted",
                    "completion_credit": 0,
                }
            )
    valid = positive_result["valid"] and all(row["rejected"] for row in mutation_results)
    return {
        "schema": f"{SCHEMA}.surface-execution",
        "proposal_id": SPEC_BY_SLUG[surface]["proposal_id"],
        "surface": surface,
        "outcome": SPEC_BY_SLUG[surface]["expected_outcome"],
        "positive_fixture": positive,
        "positive_result": positive_result,
        "mutation_count": len(mutation_results),
        "rejected_mutation_count": sum(row["rejected"] for row in mutation_results),
        "mutations": mutation_results,
        "post_success_replay": False,
        "valid": valid,
    }


def ghc_family_run_marigram_profile(profile: str) -> dict[str, Any]:
    """Invoke one family-current bounded runner profile."""

    try:
        surfaces = RUNNER_PROFILES[profile]
    except KeyError as exc:
        raise EvidenceError(f"unknown marigram runner profile: {profile}") from exc
    executions = [ghc_family_execute_marigram_surface(surface) for surface in surfaces]
    return {
        "schema": f"{SCHEMA}.runner-profile",
        "family_current_runner": f"ghc_family_marigram_{profile.replace('-', '_')}",
        "profile": profile,
        "surfaces": list(surfaces),
        "proposal_ids": [row["proposal_id"] for row in executions],
        "surface_count": len(executions),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "network_calls": 0,
        "real_world_rows": 0,
        "valid": all(row["valid"] for row in executions),
        "boundary": "Family-compatible owner-local runner profile only; not an operational archive, tide station, datum, survey, prediction, identity, rights, professional, empirical, production, or authority system.",
    }


def ghc_family_execute_v664_v2() -> dict[str, Any]:
    """Execute each frozen v664-v2 surface exactly once in one build call."""

    executions = [ghc_family_execute_marigram_surface(spec["surface"]) for spec in SURFACE_SPECS]
    outcomes = CounterLike(row["outcome"] for row in executions)
    runner_results = [ghc_family_run_marigram_profile(profile) for profile in RUNNER_PROFILES]
    expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    valid = (
        len(executions) == 20
        and outcomes == expected
        and sum(row["rejected_mutation_count"] for row in executions) == 80
        and all(row["valid"] for row in executions)
        and all(row["valid"] for row in runner_results)
    )
    return {
        "schema": f"{SCHEMA}.phase-execution",
        "phase": PHASE,
        "surface_count": len(executions),
        "executions": executions,
        "outcome_counts": outcomes,
        "mutation_count": 80,
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "runner_profile_count": len(runner_results),
        "runner_results": runner_results,
        "network_calls": 0,
        "downloads": 0,
        "real_world_rows": 0,
        "valid": valid,
        "verdict": "NOT_READY_FOR_STAGE_20",
    }


def CounterLike(values: Iterable[str]) -> dict[str, int]:
    """Return all four truth labels in stable display order."""

    counts = {key: 0 for key in ("completed", "represented", "open_gap", "exact_gate")}
    for value in values:
        if value not in ALLOWED_OUTCOMES:
            raise EvidenceError(f"unknown outcome: {value}")
        counts[value] += 1
    return counts


# Backwards-compatible and discoverable build aliases.  The family-current
# names above remain primary; these phase aliases are additive only.
build_ghc_family_v664_v2_evidence = ghc_family_execute_v664_v2
ghc_family_validate_v664_v2_surface = ghc_family_validate_marigram_surface
ghc_family_run_v664_v2_profile = ghc_family_run_marigram_profile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("all", *RUNNER_PROFILES), default="all")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = (
            ghc_family_execute_v664_v2()
            if args.profile == "all"
            else ghc_family_run_marigram_profile(args.profile)
        )
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload["valid"] else 2
    except (EvidenceError, TypeError, ValueError) as exc:
        print(f"GHC_FAMILY_MARIGRAM_EVIDENCE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
