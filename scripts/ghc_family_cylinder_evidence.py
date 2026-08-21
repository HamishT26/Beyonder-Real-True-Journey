#!/usr/bin/env python3
"""Bounded synthetic wax-cylinder evidence engine for GHC family phases.

The engine validates owner-local declarations and refusal boundaries only.  It
does not inspect, handle, clean, fit, play, transfer, preserve, authenticate, or
decide rights for a real carrier or recording.  It performs no network access,
identity operation, professional decision, or authority action.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import re
import sys
from typing import Any, Iterable


SCHEMA = "ghc.family.cylinder-evidence.v1"
PHASE = "v664-v1"
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
        "proposal_id": f"EL6641-N{number:03d}",
        "surface": slug,
        "expected_outcome": outcome,
        "source_ids": list(sources),
        "critical_field": critical_field,
        "required": required,
    }


SURFACE_SPECS = (
    _spec(1, "cylinder-capsule", "completed", ("SRC-LOC-CARE", "SRC-UCSB-CYLINDER"), "playback_authorized", {
        "carrier_token": "syn:cylinder:carrier:001", "format_state": "hypothesis_only", "box_relation": "synthetic_container", "revision": 1, "custody_state": "hold", "authenticated": False, "playback_authorized": False,
    }),
    _spec(2, "carrier-topology", "completed", ("SRC-LOC-CARE", "SRC-UCSB-CYLINDER"), "material_identified", {
        "parts": ["cylinder", "box", "lid", "label", "core", "surface", "fragment", "surrogate"], "orphan_state": "quarantined", "material_identified": False, "topology_complete": False,
    }),
    _spec(3, "transcription-braid", "completed", ("SRC-PREMIS", "SRC-PROV"), "attribution_claimed", {
        "layers": ["verbatim", "supplied_expansion", "illegibility", "conflict", "correction"], "conflict_state": "retained", "attribution_claimed": False, "real_text_rows": 0,
    }),
    _spec(4, "surface-observation", "completed", ("SRC-LOC-CARE",), "diagnosis_made", {
        "terms": ["dust", "deposit", "bloom", "mould_like_cue", "abrasion", "crack", "deformation"], "observation_state": "synthetic_only", "diagnosis_made": False, "treatment_recommended": False,
    }),
    _spec(5, "fragment-graph", "completed", ("SRC-LOC-BROKEN", "SRC-LOC-CARE"), "reassembly_instruction", {
        "edge_tokens": ["syn:edge:a", "syn:edge:b"], "adjacency_state": "hypothesis_only", "missing_regions": ["unknown-region"], "duplicate_state": "quarantined", "fit_state": "hold", "reassembly_instruction": False,
    }),
    _spec(6, "groove-coordinate-envelope", "completed", ("SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "measurement_rows", {
        "axial_origin": "symbolic", "rotation_direction": "unknown", "pitch_state": "placeholder", "speed_state": "vacant", "uncertainty_state": "unresolved", "measurement_rows": 0,
    }),
    _spec(7, "fit-decision-board", "completed", ("SRC-LOC-CARE", "SRC-NIST-SI"), "equipment_fit_decided", {
        "mandrel_state": "vacant", "bore_state": "vacant", "dimension_state": "placeholder", "eccentricity_state": "placeholder", "clearance_state": "hold", "contact_authorized": False, "equipment_fit_decided": False,
    }),
    _spec(8, "playback-chain-hold", "completed", ("SRC-IASA-TC04", "SRC-LOC-CARE"), "playback_setting_instruction", {
        "stylus_profile": "vacant", "groove_family": "hypothesis_only", "rotation_speed": "vacant", "equalization": "vacant", "transducer_chain": "vacant", "source_version": "unresolved", "compatibility_state": "hold", "playback_setting_instruction": False,
    }),
    _spec(9, "transfer-provenance", "completed", ("SRC-IASA-TC04", "SRC-PREMIS", "SRC-PROV"), "operation_executed", {
        "carrier": "syn:cylinder:carrier:001", "session_state": "placeholder", "device_state": "vacant", "converter_state": "vacant", "channel_map": "placeholder", "derivative_state": "proposed", "fixity_state": "planned", "operation_executed": False,
    }),
    _spec(10, "derivative-reconciliation", "completed", ("SRC-IASA-TC04", "SRC-LOC-RFS", "SRC-PREMIS", "SRC-RFC8785"), "fidelity_claimed", {
        "file_roles": ["preservation_master_placeholder", "access_derivative_placeholder"], "checksum_state": "synthetic", "sample_format": "placeholder", "provenance_state": "declared", "duplicate_count": 0, "invalidation_state": "available", "fidelity_claimed": False,
    }),
    _spec(11, "thos-triage-queue", "represented", ("SRC-IASA-TC04", "SRC-PROV"), "operational_effectiveness", {
        "people": 0, "quarantine_state": "active", "unresolved_count": 2, "unresolved_ceiling": 2, "two_key_stop": True, "discrepancy_readback": "synthetic_digest", "handover_digest": "sha256:synthetic", "operational_effectiveness": False,
    }),
    _spec(12, "gmut-groove-chart", "represented", ("SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "observation_rows", {
        "angular_coordinate": "symbolic", "axial_coordinate": "symbolic", "pitch_tensor": "placeholder", "boundary_conditions": "declared_symbolic", "units_state": "typed", "covariance_state": "vacant", "observation_rows": 0,
    }),
    _spec(13, "gmut-modulation-decomposition", "represented", ("SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "physical_inference", {
        "radial_offset": "symbolic", "angular_rate": "placeholder", "harmonic_family": ["h0", "h1"], "confounders": ["carrier_geometry", "time_base", "transfer_chain"], "coefficient_rows": 0, "physical_inference": False,
    }),
    _spec(14, "freed-id-cylinder-statement", "represented", ("SRC-W3C-VC20", "SRC-RFC8785", "SRC-PREMIS"), "identity_claimed", {
        "surrogate_carrier": "syn:cylinder:carrier:001", "recording_work": "placeholder", "content_digest": "sha256:synthetic", "issuer_state": "vacant", "proof_state": "absent", "rights_state": "hold", "identity_claimed": False, "authorship_claimed": False,
    }),
    _spec(15, "freed-id-correction-chain", "completed", ("SRC-W3C-VC20", "SRC-PROV", "SRC-PREMIS"), "live_identity_operation", {
        "chain": ["transcription", "format_hypothesis", "access_state", "rights_hold", "supersession", "challenge"], "status_state": "vacant", "append_only": True, "live_identity_operation": False,
    }),
    _spec(16, "accessible-evidence-map", "completed", ("SRC-WCAG22", "SRC-PROV"), "manual_evaluation_complete", {
        "carrier_part_table": True, "provenance_narrative": True, "noncolour_states": True, "transcript_fallback": True, "print_mode": True, "manual_evaluation_complete": False, "affected_user_evaluation_complete": False,
    }),
    _spec(17, "privacy-minimization-docket", "completed", ("SRC-NZ-PRIVACY", "SRC-WCAG22"), "privacy_complete", {
        "catalogue_rows": 0, "field_purpose_map": True, "indirect_identity_allowed": False, "access_reserved": True, "correction_reserved": True, "disclosure_state": "hold", "expiry_trigger": "declared", "privacy_complete": False,
    }),
    _spec(18, "zero-row-vocabulary-adapter", "open_gap", ("SRC-UCSB-CYLINDER", "SRC-LOC-CARE", "SRC-PREMIS"), "live_calls", {
        "schema_pins": ["ucsb-cylinder-watch", "loc-cylinder-watch"], "live_calls": 0, "downloads": 0, "version_state": "vacant", "catalog_authority": False, "gap_open": True,
    }),
    _spec(19, "rights-authority-matrix", "exact_gate", ("SRC-TE-MANA-RARAUNGA", "SRC-NZ-PRIVACY"), "authority_decision_made", {
        "chairs": ["performance", "composition", "recording", "donor_restriction", "cultural_expression", "traditional_knowledge", "access", "remedy", "affected_parties", "maori_authority"], "occupied_chairs": 0, "authority_decision_made": False, "gate_open": True,
    }),
    _spec(20, "stage-20-admission-docket", "completed", ("SRC-IASA-TC04", "SRC-W3C-VC20", "SRC-TE-MANA-RARAUNGA"), "admitted_evidence_rows", {
        "authenticated_carrier": False, "governed_preservation": False, "calibrated_transfer": False, "rights_review": False, "affected_party_authority": False, "independent_reproduction": False, "admitted_evidence_rows": 0, "stage_20_ready": False,
    }),
)

SPEC_BY_SLUG = {spec["surface"]: spec for spec in SURFACE_SPECS}
SPEC_BY_ID = {spec["proposal_id"]: spec for spec in SURFACE_SPECS}
if len(SPEC_BY_SLUG) != 20 or len(SPEC_BY_ID) != 20:
    raise RuntimeError("surface identifiers must be unique")

RUNNER_PROFILES = {
    "carrier-capsule": ("cylinder-capsule", "carrier-topology"),
    "inscription-observation": ("transcription-braid", "surface-observation"),
    "fragment-geometry": ("fragment-graph", "groove-coordinate-envelope"),
    "fit-playback-hold": ("fit-decision-board", "playback-chain-hold"),
    "provenance-derivatives": ("transfer-provenance", "derivative-reconciliation"),
    "thos-gmut-boundaries": ("thos-triage-queue", "gmut-groove-chart", "gmut-modulation-decomposition"),
    "freed-id-boundaries": ("freed-id-cylinder-statement", "freed-id-correction-chain"),
    "access-privacy": ("accessible-evidence-map", "privacy-minimization-docket"),
    "source-authority": ("zero-row-vocabulary-adapter", "rights-authority-matrix"),
    "terminal-admission": ("stage-20-admission-docket",),
}


def ghc_family_build_cylinder_fixture(surface: str) -> dict[str, Any]:
    """Return the deterministic positive fixture for one declared surface."""

    try:
        spec = SPEC_BY_SLUG[surface]
    except KeyError as exc:
        raise EvidenceError(f"unknown cylinder surface: {surface}") from exc
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


def ghc_family_validate_cylinder_surface(record: Any) -> dict[str, Any]:
    """Validate one fixture against its exact surface contract."""

    if not isinstance(record, dict):
        raise EvidenceError("cylinder fixture must be a JSON object")
    surface = record.get("surface")
    if not isinstance(surface, str) or surface not in SPEC_BY_SLUG:
        raise EvidenceError("cylinder fixture declares an unknown surface")
    spec = SPEC_BY_SLUG[surface]
    expected = ghc_family_build_cylinder_fixture(surface)
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
        "boundary": "Owner-local synthetic software witness only; no real carrier, recording, person, right, measurement, operation, authority, production, empirical, or Stage 20 result.",
    }


def ghc_family_build_cylinder_mutations(surface: str) -> list[dict[str, Any]]:
    """Return four preregistered rejecting mutations for one surface."""

    fixture = ghc_family_build_cylinder_fixture(surface)
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


def ghc_family_execute_cylinder_surface(surface: str) -> dict[str, Any]:
    """Run the positive fixture and all four rejecting mutations once."""

    positive = ghc_family_build_cylinder_fixture(surface)
    positive_result = ghc_family_validate_cylinder_surface(positive)
    mutation_results = []
    for index, mutation in enumerate(ghc_family_build_cylinder_mutations(surface), start=1):
        try:
            ghc_family_validate_cylinder_surface(mutation["record"])
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


def ghc_family_run_cylinder_profile(profile: str) -> dict[str, Any]:
    """Invoke one family-current bounded runner profile."""

    try:
        surfaces = RUNNER_PROFILES[profile]
    except KeyError as exc:
        raise EvidenceError(f"unknown cylinder runner profile: {profile}") from exc
    executions = [ghc_family_execute_cylinder_surface(surface) for surface in surfaces]
    return {
        "schema": f"{SCHEMA}.runner-profile",
        "family_current_runner": f"ghc_family_cylinder_{profile.replace('-', '_')}",
        "profile": profile,
        "surfaces": list(surfaces),
        "proposal_ids": [row["proposal_id"] for row in executions],
        "surface_count": len(executions),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "network_calls": 0,
        "real_world_rows": 0,
        "valid": all(row["valid"] for row in executions),
        "boundary": "Family-compatible owner-local runner profile only; not an operational archive, preservation, identity, rights, professional, empirical, production, or authority system.",
    }


def ghc_family_execute_v664_v1() -> dict[str, Any]:
    """Execute each frozen v664-v1 surface exactly once in one build call."""

    executions = [ghc_family_execute_cylinder_surface(spec["surface"]) for spec in SURFACE_SPECS]
    outcomes = CounterLike(row["outcome"] for row in executions)
    runner_results = [ghc_family_run_cylinder_profile(profile) for profile in RUNNER_PROFILES]
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
build_ghc_family_v664_v1_evidence = ghc_family_execute_v664_v1
ghc_family_validate_v664_v1_surface = ghc_family_validate_cylinder_surface
ghc_family_run_v664_v1_profile = ghc_family_run_cylinder_profile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("all", *RUNNER_PROFILES), default="all")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = (
            ghc_family_execute_v664_v1()
            if args.profile == "all"
            else ghc_family_run_cylinder_profile(args.profile)
        )
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload["valid"] else 2
    except (EvidenceError, TypeError, ValueError) as exc:
        print(f"GHC_FAMILY_CYLINDER_EVIDENCE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
