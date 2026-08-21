#!/usr/bin/env python3
"""Build bounded synthetic archival-audio evidence for GHC family phases.

The engine validates exact owner-local declarations and refusal boundaries. It
does not read media, inspect a carrier, capture samples, identify a voice or
person, run a preservation workflow, decide access or rights, or claim archival,
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


SCHEMA = "ghc.family.archival-audio-evidence.v1"
PHASE = "v664-v4"
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
        "proposal_id": f"LM6644-N{number:03d}",
        "surface": surface,
        "expected_outcome": outcome,
        "source_ids": list(sources),
        "critical_field": critical_field,
        "required": required,
    }


SURFACE_SPECS = (
    spec(1, "audio-object-capsule", "completed", ("SRC-IASA-TC04", "SRC-PREMIS"), "authenticity_claimed", {
        "object_token": "syn:audio-object:001", "carrier_relation": "synthetic_only", "side_state": "vacant", "channel_state": "vacant", "revision": 1, "custody_state": "hold", "authenticity_claimed": False, "audibility_claimed": False,
    }),
    spec(2, "carrier-side-channel-topology", "completed", ("SRC-IASA-TC04", "SRC-IASA-TC03"), "physical_condition_assessed", {
        "components": ["reel", "cassette", "shell", "hub", "side", "track", "channel", "leader", "splice", "segment", "surrogate"], "orphan_state": "quarantined", "physical_condition_assessed": False, "topology_complete": False,
    }),
    spec(3, "carrier-condition-boundary", "completed", ("SRC-IASA-TC03", "SRC-IASA-TC04"), "inspected_media", {
        "observation_slots": ["deformation", "residue", "binder_risk", "splice", "odour", "packaging"], "uncertainty_state": "unresolved", "inspected_media": 0, "condition_conclusion": False,
    }),
    spec(4, "playback-chain-dependency", "completed", ("SRC-IASA-TC04", "SRC-FADGI-AUDIO"), "playback_actions", {
        "dependencies": ["machine", "head", "equalization", "azimuth", "speed", "cabling", "converter", "software", "operator"], "vacancy_policy": "fail_closed", "release_state": "refused", "playback_actions": 0,
    }),
    spec(5, "calibration-reference-vacancy", "completed", ("SRC-FADGI-AUDIO", "SRC-IASA-TC04"), "measurement_rows", {
        "reference_roles": ["level", "frequency", "channel", "date", "instrument", "traceability", "tolerance", "uncertainty"], "calibration_state": "vacant", "measurement_rows": 0, "calibration_conclusion": False,
    }),
    spec(6, "clock-timebase-uncertainty", "completed", ("SRC-FADGI-AUDIO", "SRC-IASA-TC04"), "signal_estimates", {
        "nominal_rate_state": "placeholder", "drift_state": "vacant", "wow_flutter_state": "placeholder", "synchronization_debt": 1, "covariance_state": "vacant", "signal_estimates": 0,
    }),
    spec(7, "capture-provenance-fixity", "completed", ("SRC-PREMIS", "SRC-PROV", "SRC-RFC8785"), "captured_samples", {
        "event_chain": ["source", "session", "file", "fixity", "supersession", "invalidation"], "software_environment": "declared_synthetic", "checksum_state": "synthetic_digest", "captured_samples": 0, "capture_performed": False,
    }),
    spec(8, "bwf-conformance-envelope", "completed", ("SRC-EBU-BWF", "SRC-LOC-BWF"), "audio_payload_bytes", {
        "chunk_roles": ["RIFF", "WAVE", "fmt", "bext", "data", "unknown"], "loudness_state": "vacant", "chunk_order_state": "guarded", "unknown_chunk_policy": "retain", "audio_payload_bytes": 0, "conformance_certified": False,
    }),
    spec(9, "signal-event-map", "completed", ("SRC-FADGI-AUDIO", "SRC-IASA-TC04"), "detected_events", {
        "event_roles": ["clipping", "dropout", "discontinuity", "noise", "hum", "channel_imbalance", "timing_anomaly"], "review_state": "unreviewed", "detected_events": 0, "signal_diagnosis": False,
    }),
    spec(10, "fixity-migration-chain", "completed", ("SRC-PREMIS", "SRC-LOC-RFS"), "external_transfers", {
        "event_roles": ["fixity", "replication", "storage_copy", "format_migration", "validation", "rollback", "supersession"], "repository_state": "vacant", "loss_refusal": True, "external_transfers": 0,
    }),
    spec(11, "thos-audio-admission", "represented", ("SRC-IASA-TC04", "SRC-PREMIS"), "service_performance_measured", {
        "people": 0, "intake_debt": 2, "quarantine_ceiling": 2, "stop_latch": True, "discrepancy_state": "synthetic_digest", "handover_checksum": "sha256:synthetic", "service_performance_measured": False,
    }),
    spec(12, "gmut-signal-decay-chart", "represented", ("SRC-IASA-TC04", "SRC-FADGI-AUDIO"), "observation_rows", {
        "time_coordinate": "symbolic", "carrier_state_proxy": "symbolic", "transfer_operator": "placeholder", "unit_roles": "typed", "covariance_state": "vacant", "observation_rows": 0, "fitted_law": False,
    }),
    spec(13, "gmut-transfer-decomposition", "represented", ("SRC-FADGI-AUDIO", "SRC-IASA-TC04"), "physical_inference", {
        "terms": ["carrier", "head", "equalization", "timebase", "converter", "channel", "sampling", "handling"], "coefficient_rows": 0, "identifiability_state": "unresolved", "physical_inference": False,
    }),
    spec(14, "freed-id-audio-assertion", "represented", ("SRC-PREMIS", "SRC-RFC8785"), "entitlement_claimed", {
        "surrogate_object": "syn:audio-object:001", "packet_digest": "sha256:synthetic", "trust_actor_state": "vacant", "verification_material_state": "absent", "status_state": "hold", "consent_state": "vacant", "revocation_state": "vacant", "identity_claimed": False, "entitlement_claimed": False,
    }),
    spec(15, "intervention-amendment-trail", "completed", ("SRC-PROV", "SRC-PREMIS"), "adjudication_performed", {
        "chain": ["speed", "equalization", "channel", "segment", "transcript", "checksum", "challenge"], "append_only": True, "challenge_state": "unresolved", "adjudicator_state": "vacant", "adjudication_performed": False,
    }),
    spec(16, "accessible-audio-dossier", "completed", ("SRC-WCAG22", "SRC-PREMIS"), "manual_evaluation_complete", {
        "heading_route": True, "text_time_alternative": True, "event_table": True, "transcript_confidence_labels": True, "print_fallback": True, "manual_evaluation_complete": False, "affected_user_evaluation_complete": False,
    }),
    spec(17, "audio-record-minimization", "completed", ("SRC-PREMIS", "SRC-WCAG22"), "privacy_complete", {
        "person_context_rows": 0, "speaker_field_allowed": False, "contact_field_allowed": False, "purpose_enum_required": True, "free_text_allowed": False, "correction_state": "placeholder", "retention_state": "vacant", "disclosure_state": "locked", "privacy_complete": False,
    }),
    spec(18, "zero-row-audio-vocabulary-adapter", "open_gap", ("SRC-EBU-BWF", "SRC-PREMIS", "SRC-LOC-BWF"), "live_calls", {
        "schema_pins": ["ebu-bwf-watch", "premis-watch", "loc-bwf-watch"], "live_calls": 0, "downloads": 0, "media_reads": 0, "version_state": "vacant", "data_authority": False, "gap_open": True,
    }),
    spec(19, "audio-rights-authority-matrix", "exact_gate", ("SRC-IASA-TC03", "SRC-PREMIS"), "authority_decision_made", {
        "chairs": ["custody", "copyright", "performer_interests", "access", "restriction", "remedy", "affected_parties", "cultural_material", "maori_authority"], "occupied_chairs": 0, "authority_decision_made": False, "gate_open": True,
    }),
    spec(20, "stage20-audio-refusal", "completed", ("SRC-IASA-TC04", "SRC-PREMIS", "SRC-WCAG22"), "admitted_evidence_rows", {
        "witnessed_origin": False, "traceable_conversion": False, "durable_custody": False, "permissions_review": False, "access_review": False, "separate_replication": False, "admitted_evidence_rows": 0, "stage_20_ready": False,
    }),
)

SPEC_BY_SLUG = {row["surface"]: row for row in SURFACE_SPECS}
SPEC_BY_ID = {row["proposal_id"]: row for row in SURFACE_SPECS}
if len(SPEC_BY_SLUG) != 20 or len(SPEC_BY_ID) != 20:
    raise RuntimeError("surface identifiers must be unique")

RUNNER_PROFILES = {
    "object-topology": ("audio-object-capsule", "carrier-side-channel-topology"),
    "condition-playback": ("carrier-condition-boundary", "playback-chain-dependency"),
    "calibration-timebase": ("calibration-reference-vacancy", "clock-timebase-uncertainty"),
    "capture-bwf": ("capture-provenance-fixity", "bwf-conformance-envelope"),
    "signal-fixity": ("signal-event-map", "fixity-migration-chain"),
    "thos-gmut-boundaries": ("thos-audio-admission", "gmut-signal-decay-chart", "gmut-transfer-decomposition"),
    "freed-id-amendment": ("freed-id-audio-assertion", "intervention-amendment-trail"),
    "access-privacy": ("accessible-audio-dossier", "audio-record-minimization"),
    "vocabulary-authority": ("zero-row-audio-vocabulary-adapter", "audio-rights-authority-matrix"),
    "terminal-refusal": ("stage20-audio-refusal",),
}


def ghc_family_build_archival_audio_fixture(surface: str) -> dict[str, Any]:
    """Return one deterministic zero-row synthetic fixture."""

    try:
        frozen = SPEC_BY_SLUG[surface]
    except KeyError as exc:
        raise EvidenceError(f"unknown archival-audio surface: {surface}") from exc
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


def ghc_family_validate_archival_audio_surface(record: Any) -> dict[str, Any]:
    """Validate one fixture against its complete exact-key contract."""

    if not isinstance(record, dict):
        raise EvidenceError("archival-audio fixture must be a JSON object")
    surface = record.get("surface")
    if not isinstance(surface, str) or surface not in SPEC_BY_SLUG:
        raise EvidenceError("archival-audio fixture declares an unknown surface")
    frozen = SPEC_BY_SLUG[surface]
    expected = ghc_family_build_archival_audio_fixture(surface)
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
        "boundary": "Owner-local synthetic software witness only; no real recording, carrier, signal, voice, person, equipment, inspection, measurement, capture, preservation action, right, access decision, professional judgment, authority, production, empirical, or Stage 20 result.",
    }


def ghc_family_build_archival_audio_mutations(surface: str) -> list[dict[str, Any]]:
    """Return five preregistered rejecting mutations for one surface."""

    fixture = ghc_family_build_archival_audio_fixture(surface)
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


def ghc_family_execute_archival_audio_surface(surface: str) -> dict[str, Any]:
    """Run the positive fixture and all rejecting mutations once."""

    positive = ghc_family_build_archival_audio_fixture(surface)
    positive_result = ghc_family_validate_archival_audio_surface(positive)
    mutation_results = []
    for index, mutation in enumerate(ghc_family_build_archival_audio_mutations(surface), 1):
        try:
            ghc_family_validate_archival_audio_surface(mutation["record"])
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


def ghc_family_run_archival_audio_profile(profile: str) -> dict[str, Any]:
    """Invoke one family-current fixed bounded runner profile."""

    try:
        surfaces = RUNNER_PROFILES[profile]
    except KeyError as exc:
        raise EvidenceError(f"unknown archival-audio runner profile: {profile}") from exc
    executions = [ghc_family_execute_archival_audio_surface(surface) for surface in surfaces]
    return {
        "schema": f"{SCHEMA}.runner-profile",
        "family_current_runner": f"ghc_family_archival_audio_{profile.replace('-', '_')}",
        "profile": profile,
        "surfaces": list(surfaces),
        "proposal_ids": [row["proposal_id"] for row in executions],
        "surface_count": len(executions),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in executions),
        "network_calls": 0,
        "media_reads": 0,
        "real_world_rows": 0,
        "valid": all(row["valid"] for row in executions),
        "boundary": "Family-compatible owner-local profile only; not an archive, playback, inspection, capture, preservation, identity, rights, professional, empirical, production, cultural, legal, or authority system.",
    }


def outcome_counts(values: Iterable[str]) -> dict[str, int]:
    counts = {key: 0 for key in ("completed", "represented", "open_gap", "exact_gate")}
    for value in values:
        if value not in ALLOWED_OUTCOMES:
            raise EvidenceError(f"unknown outcome: {value}")
        counts[value] += 1
    return counts


def ghc_family_execute_v664_v4() -> dict[str, Any]:
    """Execute every frozen surface exactly once in one build call."""

    executions = [ghc_family_execute_archival_audio_surface(row["surface"]) for row in SURFACE_SPECS]
    runners = [ghc_family_run_archival_audio_profile(profile) for profile in RUNNER_PROFILES]
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
        "media_reads": 0,
        "real_world_rows": 0,
        "valid": valid,
        "verdict": "NOT_READY_FOR_STAGE_20",
    }


# Additive discoverable phase aliases; family-current names remain primary.
build_ghc_family_v664_v4_evidence = ghc_family_execute_v664_v4
ghc_family_validate_v664_v4_surface = ghc_family_validate_archival_audio_surface
ghc_family_run_v664_v4_profile = ghc_family_run_archival_audio_profile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("all", *RUNNER_PROFILES), default="all")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = (
            ghc_family_execute_v664_v4()
            if args.profile == "all"
            else ghc_family_run_archival_audio_profile(args.profile)
        )
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload["valid"] else 2
    except (EvidenceError, TypeError, ValueError) as exc:
        print(f"GHC_FAMILY_ARCHIVAL_AUDIO_EVIDENCE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
