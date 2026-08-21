#!/usr/bin/env python3
"""Bounded synthetic seed-bank evidence engine for GHC family phases.

The engine validates owner-local declarations and refusal boundaries only.  It
does not access, identify, handle, store, test, regenerate, distribute, or
transfer real seed; decide stewardship, rights, benefit sharing, or traditional
knowledge; or perform any identity, professional, operational, or authority action.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import re
import sys
from typing import Any, Iterable


SCHEMA = "ghc.family.seed-bank-evidence.v1"
PHASE = "v664-v3"
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
        "proposal_id": f"VE6643-N{number:03d}",
        "surface": slug,
        "expected_outcome": outcome,
        "source_ids": list(sources),
        "critical_field": critical_field,
        "required": required,
    }


SURFACE_SPECS = (
    _spec(1, "seed-accession-capsule", "completed", ("SRC-PREMIS", "SRC-FAO-GENEBANK"), "conservation_claim", {
        "accession_token": "syn:seed-accession:001", "packet_relation": "synthetic_only", "acquisition_state": "vacant", "revision": 1, "custody_state": "hold", "authenticated": False, "conservation_claim": False,
    }),
    _spec(2, "packet-lot-topology", "completed", ("SRC-FAO-GENEBANK",), "material_condition_assessed", {
        "components": ["packet", "lot", "container", "shelf", "chamber", "duplicate", "subsample", "seal", "label", "surrogate"], "orphan_state": "quarantined", "material_condition_assessed": False, "topology_complete": False,
    }),
    _spec(3, "seed-label-register", "completed", ("SRC-PREMIS", "SRC-PROV", "SRC-GENESYS"), "attribution_claimed", {
        "layers": ["verbatim_segment", "illegible_zone", "alternative_reading", "editor_intervention", "contested_mark"], "conflict_state": "retained", "attribution_claimed": False, "real_text_rows": 0,
    }),
    _spec(4, "taxonomic-determination-graph", "completed", ("SRC-GBIF", "SRC-GENESYS"), "taxonomic_conclusion", {
        "verbatim_name": "synthetic_placeholder", "accepted_name_state": "vacant", "identifier_state": "vacant", "determination_events": 0, "uncertainty_state": "unresolved", "dispute_state": "hold", "taxonomic_conclusion": False,
    }),
    _spec(5, "cold-storage-envelope", "completed", ("SRC-FAO-GENEBANK", "SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "sensor_observation_rows", {
        "chamber_zone": "synthetic", "temperature_channel": "placeholder", "humidity_channel": "placeholder", "calibration_state": "vacant", "excursion_state": "unresolved", "uncertainty_state": "unresolved", "sensor_observation_rows": 0,
    }),
    _spec(6, "viability-sampling-plan", "completed", ("SRC-FAO-GENEBANK", "SRC-NIST-UNCERTAINTY"), "seeds_handled", {
        "lot_boundary": "synthetic", "sample_size_state": "vacant", "destructive_test_state": "hold", "replicate_state": "planned", "decision_ceiling": "no_action", "seeds_handled": 0,
    }),
    _spec(7, "germination-uncertainty-board", "completed", ("SRC-FAO-GENEBANK", "SRC-NIST-UNCERTAINTY"), "observed_seedlings", {
        "replicate_slots": 4, "categories": ["normal", "abnormal", "non_germinated", "unclassified"], "denominator_state": "vacant", "interval_state": "placeholder", "observed_seedlings": 0, "viability_estimate_present": False,
    }),
    _spec(8, "safety-duplicate-provenance", "completed", ("SRC-FAO-GENEBANK", "SRC-PREMIS", "SRC-PROV"), "physical_movements", {
        "parent_lot": "syn:seed-lot:001", "derivative_packet": "syn:seed-packet:001", "destination_state": "vacant", "transfer_state": "hold", "reconciliation_state": "unresolved", "physical_movements": 0,
    }),
    _spec(9, "moisture-unit-registry", "completed", ("SRC-FAO-GENEBANK", "SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "measurement_rows", {
        "quantities": ["fresh_mass", "dry_mass", "moisture_content"], "method_state": "vacant", "conversion_state": "guarded", "unit_state": "typed", "uncertainty_state": "unresolved", "measurement_rows": 0,
    }),
    _spec(10, "inventory-quarantine-ledger", "completed", ("SRC-FAO-GENEBANK", "SRC-PROV", "SRC-RFC8785"), "stock_asserted", {
        "state_roles": ["accession", "packet", "availability", "review", "discrepancy", "supersession", "invalidation"], "quarantine_state": "active", "stock_rows": 0, "stock_asserted": False,
    }),
    _spec(11, "thos-seed-admission-machine", "represented", ("SRC-FAO-GENEBANK", "SRC-PROV"), "operational_effectiveness", {
        "people": 0, "quarantine_pending_count": 2, "quarantine_ceiling": 2, "stop_latch": True, "discrepancy_acknowledgement": "synthetic_digest", "queue_debt": 1, "handover_checksum": "sha256:synthetic", "operational_effectiveness": False,
    }),
    _spec(12, "gmut-viability-decay-chart", "represented", ("SRC-FAO-GENEBANK", "SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"), "observation_rows", {
        "time_coordinate": "symbolic", "viability_state": "symbolic", "storage_operator": "placeholder", "unit_roles": "typed", "covariance_state": "vacant", "observation_rows": 0, "fitted_law": False,
    }),
    _spec(13, "gmut-aging-decomposition", "represented", ("SRC-FAO-GENEBANK", "SRC-NIST-UNCERTAINTY"), "physical_inference", {
        "terms": ["temperature", "moisture", "dormancy", "aging", "sampling", "handling"], "coefficient_rows": 0, "identifiability_state": "unresolved", "physical_inference": False,
    }),
    _spec(14, "freed-id-accession-assertion", "represented", ("SRC-W3C-VC20", "SRC-RFC8785", "SRC-PREMIS"), "ownership_claimed", {
        "surrogate_accession": "syn:seed-accession:001", "packet_digest": "sha256:synthetic", "claimant_state": "vacant", "proof_state": "absent", "purpose_state": "restricted", "status_state": "hold", "identity_claimed": False, "ownership_claimed": False,
    }),
    _spec(15, "seed-metadata-amendment-trail", "completed", ("SRC-W3C-VC20", "SRC-PROV", "SRC-PREMIS"), "live_governance_operation", {
        "chain": ["taxonomic_state", "storage_state", "viability_state", "reason_code", "replacement_link", "challenge"], "challenger_state": "placeholder", "resolution_state": "unresolved", "append_only": True, "live_governance_operation": False,
    }),
    _spec(16, "accessible-seed-dossier", "completed", ("SRC-WCAG22", "SRC-PROV"), "manual_evaluation_complete", {
        "heading_route": True, "definition_list_route": True, "text_storage_narrative": True, "table_fallback": True, "print_fallback": True, "manual_evaluation_complete": False, "affected_user_evaluation_complete": False,
    }),
    _spec(17, "seed-record-minimization-register", "completed", ("SRC-NZ-PRIVACY", "SRC-WCAG22"), "privacy_complete", {
        "person_context_rows": 0, "purpose_enum_required": True, "free_text_allowed": False, "contact_data_allowed": False, "correction_state": "placeholder", "retention_state": "placeholder", "disclosure_state": "locked", "privacy_complete": False,
    }),
    _spec(18, "zero-row-seed-adapter", "open_gap", ("SRC-GENESYS", "SRC-GBIF", "SRC-PREMIS"), "live_calls", {
        "schema_pins": ["genesys-api-watch", "gbif-occurrence-watch"], "live_calls": 0, "downloads": 0, "accession_rows": 0, "occurrence_rows": 0, "version_state": "vacant", "data_authority": False, "gap_open": True,
    }),
    _spec(19, "seed-stewardship-authority-matrix", "exact_gate", ("SRC-FAO-TREATY", "SRC-CBD-NAGOYA", "SRC-TE-MANA-RARAUNGA", "SRC-NZ-PRIVACY"), "authority_decision_made", {
        "chairs": ["custody", "origin", "collection_context", "traditional_knowledge", "access", "benefit_sharing", "remedy", "affected_parties", "maori_authority"], "occupied_chairs": 0, "authority_decision_made": False, "gate_open": True,
    }),
    _spec(20, "stage-20-refusal-proof", "completed", ("SRC-FAO-GENEBANK", "SRC-FAO-TREATY", "SRC-CBD-NAGOYA", "SRC-W3C-VC20", "SRC-TE-MANA-RARAUNGA"), "admitted_evidence_rows", {
        "governed_provenance": False, "validated_storage": False, "validated_assay": False, "rights_review": False, "affected_party_authority": False, "independent_reproduction": False, "admitted_evidence_rows": 0, "stage_20_ready": False,
    }),
)

SPEC_BY_SLUG = {spec["surface"]: spec for spec in SURFACE_SPECS}
SPEC_BY_ID = {spec["proposal_id"]: spec for spec in SURFACE_SPECS}
if len(SPEC_BY_SLUG) != 20 or len(SPEC_BY_ID) != 20:
    raise RuntimeError("surface identifiers must be unique")

RUNNER_PROFILES = {
    "accession-topology": ("seed-accession-capsule", "packet-lot-topology"),
    "label-taxonomy": ("seed-label-register", "taxonomic-determination-graph"),
    "storage-viability": ("cold-storage-envelope", "viability-sampling-plan"),
    "germination-duplication": ("germination-uncertainty-board", "safety-duplicate-provenance"),
    "moisture-inventory": ("moisture-unit-registry", "inventory-quarantine-ledger"),
    "thos-gmut-boundaries": ("thos-seed-admission-machine", "gmut-viability-decay-chart", "gmut-aging-decomposition"),
    "freed-id-boundaries": ("freed-id-accession-assertion", "seed-metadata-amendment-trail"),
    "access-privacy": ("accessible-seed-dossier", "seed-record-minimization-register"),
    "source-authority": ("zero-row-seed-adapter", "seed-stewardship-authority-matrix"),
    "terminal-refusal": ("stage-20-refusal-proof",),
}


def ghc_family_build_seed_bank_fixture(surface: str) -> dict[str, Any]:
    """Return the deterministic positive fixture for one declared surface."""

    try:
        spec = SPEC_BY_SLUG[surface]
    except KeyError as exc:
        raise EvidenceError(f"unknown seed-bank surface: {surface}") from exc
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


def ghc_family_validate_seed_bank_surface(record: Any) -> dict[str, Any]:
    """Validate one fixture against its exact surface contract."""

    if not isinstance(record, dict):
        raise EvidenceError("seed-bank fixture must be a JSON object")
    surface = record.get("surface")
    if not isinstance(surface, str) or surface not in SPEC_BY_SLUG:
        raise EvidenceError("seed-bank fixture declares an unknown surface")
    spec = SPEC_BY_SLUG[surface]
    expected = ghc_family_build_seed_bank_fixture(surface)
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
        "boundary": "Owner-local synthetic software witness only; no real accession, seed, packet, lot, facility, sensor, person, traditional knowledge, right, measurement, assay, transfer, benefit-sharing, authority, production, empirical, or Stage 20 result.",
    }


def ghc_family_build_seed_bank_mutations(surface: str) -> list[dict[str, Any]]:
    """Return four preregistered rejecting mutations for one surface."""

    fixture = ghc_family_build_seed_bank_fixture(surface)
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


def ghc_family_execute_seed_bank_surface(surface: str) -> dict[str, Any]:
    """Run the positive fixture and all four rejecting mutations once."""

    positive = ghc_family_build_seed_bank_fixture(surface)
    positive_result = ghc_family_validate_seed_bank_surface(positive)
    mutation_results = []
    for index, mutation in enumerate(ghc_family_build_seed_bank_mutations(surface), start=1):
        try:
            ghc_family_validate_seed_bank_surface(mutation["record"])
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


def ghc_family_run_seed_bank_profile(profile: str) -> dict[str, Any]:
    """Invoke one family-current bounded runner profile."""

    try:
        surfaces = RUNNER_PROFILES[profile]
    except KeyError as exc:
        raise EvidenceError(f"unknown seed-bank runner profile: {profile}") from exc
    executions = [ghc_family_execute_seed_bank_surface(surface) for surface in surfaces]
    return {
        "schema": f"{SCHEMA}.runner-profile",
        "family_current_runner": f"ghc_family_seed_bank_{profile.replace('-', '_')}",
        "profile": profile,
        "surfaces": list(surfaces),
        "proposal_ids": [row["proposal_id"] for row in executions],
        "surface_count": len(executions),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "network_calls": 0,
        "real_world_rows": 0,
        "valid": all(row["valid"] for row in executions),
        "boundary": "Family-compatible owner-local runner profile only; not an operational genebank, accession, seed store, assay, transfer, identity, rights, benefit-sharing, professional, empirical, production, or authority system.",
    }


def ghc_family_execute_v664_v3() -> dict[str, Any]:
    """Execute each frozen v664-v3 surface exactly once in one build call."""

    executions = [ghc_family_execute_seed_bank_surface(spec["surface"]) for spec in SURFACE_SPECS]
    outcomes = CounterLike(row["outcome"] for row in executions)
    runner_results = [ghc_family_run_seed_bank_profile(profile) for profile in RUNNER_PROFILES]
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
build_ghc_family_v664_v3_evidence = ghc_family_execute_v664_v3
ghc_family_validate_v664_v3_surface = ghc_family_validate_seed_bank_surface
ghc_family_run_v664_v3_profile = ghc_family_run_seed_bank_profile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("all", *RUNNER_PROFILES), default="all")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = (
            ghc_family_execute_v664_v3()
            if args.profile == "all"
            else ghc_family_run_seed_bank_profile(args.profile)
        )
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload["valid"] else 2
    except (EvidenceError, TypeError, ValueError) as exc:
        print(f"GHC_FAMILY_SEED_BANK_EVIDENCE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
