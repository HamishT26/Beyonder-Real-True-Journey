#!/usr/bin/env python3
"""Build the bounded GHC Family v643-v1 rights-resilience evidence packet.

The module is standard-library-only.  It executes deterministic structural and
synthetic fixtures while keeping empirical, participant, production, legal,
cultural, deployment, identity, proof/canon, accessibility-completeness,
exhaustive-security, and independent-reproduction claims false.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import math
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any, Callable


PHASE = "v643-gmut-thos-v1-x1-x2"
OWNER = "Eiren Kestrel"
SOURCE_COMMIT = "259c46f80b9293723914bec49003280f20637e45"
X1_COMMIT = "c64271e3bfb16a9fa0173d5901903bf967beb65f"
TRUTH_LABELS = ("completed", "represented", "open_gap", "exact_gate")
OBSERVED = {
    "V6431-P01": "completed",
    "V6431-P02": "completed",
    "V6431-P03": "represented",
    "V6431-P04": "represented",
    "V6431-P05": "completed",
    "V6431-P06": "exact_gate",
    "V6431-P07": "completed",
    "V6431-P08": "completed",
    "V6431-P09": "completed",
    "V6431-P10": "open_gap",
}

BOUNDARY = (
    "Bounded repository engineering evidence only. No empirical GMUT confirmation, "
    "THOS superiority, production Freed ID, CBR enactment, legal interpretation, "
    "cultural ratification, Māori authority, AGI/ASI, consciousness, personhood, "
    "deployment, exhaustive security, complete accessibility, proof/canon, Theory "
    "of Everything, or independent-team reproduction is established."
)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False).encode("utf-8") + b"\n")


def decision(reasons: list[str], details: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    return not reasons, reasons, details or {}


def purpose_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    purposes = [row.get(k) for k in ("collection_purpose", "proof_purpose", "derived_purpose", "onward_purpose")]
    if len(set(purposes)) != 1:
        reasons.append("purpose_path_not_compatible")
    if row.get("audience") not in row.get("declared_audiences", []):
        reasons.append("audience_not_declared")
    if row.get("expired"):
        reasons.append("purpose_expired")
    if row.get("withdrawn") and row.get("use_allowed"):
        reasons.append("withdrawal_ignored")
    if not row.get("lawful_or_authorized_basis_declared"):
        reasons.append("basis_not_declared")
    if row.get("authority_substitution"):
        reasons.append("technical_output_substituted_for_authority")
    if row.get("legal_compliance_claim"):
        reasons.append("structural_pass_promoted_to_legal_compliance")
    if row.get("retention_days", 0) <= 0 or row.get("retention_days", 0) > 365:
        reasons.append("retention_not_bounded")
    return decision(reasons, {"purpose_hops": len(purposes)})


def positivity_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    coefficient = row.get("coefficient")
    if not isinstance(coefficient, (int, float)) or coefficient <= 0:
        reasons.append("non_positive_forward_coefficient")
    if row.get("coefficient_dimension") != -4:
        reasons.append("coefficient_dimension_mismatch")
    if row.get("evaluation_scale", math.inf) >= row.get("cutoff", -math.inf):
        reasons.append("evaluation_not_below_cutoff")
    for key in ("forward_limit", "analyticity_declared", "locality_declared", "lorentz_invariance_declared", "unitarity_declared", "mass_gap_declared", "subtractions_declared"):
        if not row.get(key):
            reasons.append(f"missing_assumption:{key}")
    if row.get("singular_forward_limit"):
        reasons.append("singular_forward_limit")
    if row.get("uv_completion_claim") or row.get("toe_claim"):
        reasons.append("conditional_fixture_promoted_to_final_theory")
    return decision(reasons, {"conditional_only": True})


def covariate_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    source = row.get("source_support", [])
    target = row.get("target_support", [])
    if len(source) != 2 or len(target) != 2 or target[0] < source[0] or target[1] > source[1]:
        reasons.append("target_support_outside_source_support")
    weights = row.get("importance_weights", [])
    if not weights or any(not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0 for v in weights):
        reasons.append("invalid_importance_weight")
    if row.get("clipping_applied") and not row.get("clipping_declared"):
        reasons.append("hidden_weight_clipping")
    if row.get("effective_sample_size", 0) > len(weights) or row.get("effective_sample_size", 0) <= 0:
        reasons.append("invalid_effective_sample_size")
    if row.get("real_row_count", 0) != 0:
        reasons.append("real_rows_not_authorized_in_synthetic_fixture")
    if row.get("likelihood_count", 0) or row.get("posterior_count", 0):
        reasons.append("zero_row_inference_lock_broken")
    if row.get("empirical_promotion"):
        reasons.append("synthetic_shift_promoted_to_empirical_result")
    return decision(reasons, {"real_rows": 0, "inference_runs": 0})


def rater_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("rater_time_balanced"):
        reasons.append("rater_time_arm_confounding")
    if row.get("anchor_version_before") != row.get("anchor_version_after"):
        reasons.append("calibration_anchor_drift")
    if abs(row.get("severity_shift", math.inf)) > row.get("preregistered_severity_bound", -1):
        reasons.append("severity_drift_above_preregistered_bound")
    if row.get("decoded_before_calibration"):
        reasons.append("post_decode_calibration")
    if not row.get("adjudicator_blind"):
        reasons.append("adjudicator_contamination")
    if not row.get("matched_budget"):
        reasons.append("matched_budget_broken")
    if row.get("real_participant_count", 0) or row.get("real_rater_count", 0) or row.get("real_arm_execution"):
        reasons.append("real_arm_evidence_not_present")
    if row.get("promotion_claim"):
        reasons.append("protocol_proxy_promoted_to_thos_result")
    return decision(reasons, {"protocol_proxy_only": True})


def pairwise_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    relationships = row.get("relationships", [])
    for field, reason in (("did", "did_reused_across_relationships"), ("verification_method", "verification_material_correlates_relationships"), ("service_endpoint", "service_endpoint_correlates_relationships"), ("status_path", "status_path_correlates_relationships")):
        values = [item.get(field) for item in relationships]
        if len(values) != len(set(values)):
            reasons.append(reason)
    if row.get("rotation_joins_relationships"):
        reasons.append("rotation_links_pairwise_relationships")
    if row.get("linkability_budget", -1) < 0:
        reasons.append("linkability_budget_missing")
    if row.get("unlinkability_claim") or row.get("production_claim"):
        reasons.append("structural_profile_promoted_to_unlinkability_or_production")
    return decision(reasons, {"relationship_count": len(relationships), "real_keys": False})


def appeal_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("clock_started") and not row.get("notice_provided"):
        reasons.append("clock_started_without_notice")
    if row.get("notice_provided") and not row.get("notice_accessible"):
        reasons.append("inaccessible_notice_treated_as_served")
    if row.get("review_blocked") and not row.get("tolling_active"):
        reasons.append("blocked_review_not_tolled")
    if not row.get("remedy_preserved"):
        reasons.append("remedy_not_preserved")
    if row.get("retaliation_allowed"):
        reasons.append("retaliation_not_prohibited")
    if row.get("operative_deadline") or row.get("legal_wording") or row.get("maori_wording"):
        reasons.append("technical_schema_invented_authoritative_wording_or_deadline")
    if row.get("authority_substitution") or row.get("enacted_law_claim"):
        reasons.append("authority_or_enacted_law_promotion")
    if not row.get("paused_pending_authority"):
        reasons.append("adverse_action_not_paused_pending_authority")
    return decision(reasons, {"operative": False, "authority_deferred": True})


def parser_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if row.get("duplicate_keys"):
        reasons.append("duplicate_key_ambiguity")
    if not row.get("finite_numbers_only"):
        reasons.append("non_finite_or_out_of_domain_number")
    if not row.get("unicode_valid"):
        reasons.append("invalid_unicode_input")
    if not row.get("subtypes_preserved_as_strings"):
        reasons.append("string_subtype_changed_before_canonicalization")
    if row.get("parser_outputs") and len(set(row["parser_outputs"])) != 1:
        reasons.append("parser_semantic_disagreement")
    if row.get("array_reordered") or row.get("locale_sorting"):
        reasons.append("canonicalization_order_violation")
    if row.get("hash_role") != "provenance_only":
        reasons.append("hash_promoted_beyond_provenance")
    if row.get("exhaustive_security_claim"):
        reasons.append("local_fixture_promoted_to_exhaustive_security")
    return decision(reasons, {"rfc8785_profile": "bounded_fixture"})


def deterministic_tar(entries: list[tuple[str, bytes]], epoch: int = 1_700_000_000) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, data in sorted(entries, key=lambda item: item[0]):
            safe = str(PurePosixPath(name))
            info = tarfile.TarInfo(safe)
            info.size = len(data)
            info.mtime = epoch
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.pax_headers = {}
            archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def archive_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("source_date_epoch"):
        reasons.append("source_date_epoch_missing")
    for key in ("canonical_member_order", "canonical_timestamps", "canonical_modes", "canonical_ownership", "canonical_separators", "compression_clock_neutral"):
        if not row.get(key):
            reasons.append(f"archive_metadata_not_canonical:{key}")
    hashes = row.get("archive_hashes", [])
    if not hashes or len(set(hashes)) != 1:
        reasons.append("archive_bytes_not_repeatable")
    if row.get("cross_platform_claim") or row.get("independent_team_claim"):
        reasons.append("same_owner_archive_promoted_beyond_evidence")
    return decision(reasons, {"byte_hash": hashes[0] if hashes else None})


def landauer_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    bits = row.get("erased_bits")
    temperature = row.get("temperature_kelvin")
    if not isinstance(bits, int) or bits < 0:
        reasons.append("invalid_erased_bit_count")
    if not isinstance(temperature, (int, float)) or temperature <= 0:
        reasons.append("invalid_temperature")
    if row.get("energy_unit") != "joule":
        reasons.append("energy_unit_mismatch")
    if row.get("operation_class") != "logical_erasure":
        reasons.append("operation_not_declared_as_logical_erasure")
    if row.get("observed_device_energy_claim"):
        reasons.append("lower_bound_promoted_to_measured_device_energy")
    if row.get("psyche_energy_claim") or row.get("causal_psyche_claim"):
        reasons.append("physical_bound_promoted_to_psyche_mechanism")
    if row.get("consciousness_claim") or row.get("fundamental_law_claim"):
        reasons.append("analogy_promoted_to_consciousness_or_fundamental_law")
    bound = None
    if isinstance(bits, int) and bits >= 0 and isinstance(temperature, (int, float)) and temperature > 0:
        bound = bits * 1.380649e-23 * temperature * math.log(2)
    return decision(reasons, {"conditional_lower_bound_joule": bound, "measured": False})


def stage20_decision(row: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    if not row.get("intervals_declared"):
        reasons.append("point_estimate_hides_uncertainty_interval")
    if row.get("uncertainty_used", math.inf) > row.get("uncertainty_budget", -math.inf):
        reasons.append("uncertainty_budget_exceeded")
    if row.get("incomparable_options") and not row.get("abstain"):
        reasons.append("incomparable_options_forcibly_ranked")
    if row.get("authority_as_numeric_score"):
        reasons.append("authority_converted_to_compensable_score")
    if row.get("unrelated_evidence_compensation"):
        reasons.append("protected_gap_compensated_by_unrelated_evidence")
    if row.get("irreversible_action") or row.get("deployment"):
        reasons.append("irreversible_or_deployment_action_present")
    if row.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20" or not row.get("abstain"):
        reasons.append("terminal_abstention_not_preserved")
    return decision(reasons, {"terminal_verdict": "NOT_READY_FOR_STAGE_20"})


DECISIONS: dict[str, Callable[[dict[str, Any]], tuple[bool, list[str], dict[str, Any]]]] = {
    "V6431-P01": purpose_decision,
    "V6431-P02": positivity_decision,
    "V6431-P03": covariate_decision,
    "V6431-P04": rater_decision,
    "V6431-P05": pairwise_decision,
    "V6431-P06": appeal_decision,
    "V6431-P07": parser_decision,
    "V6431-P08": archive_decision,
    "V6431-P09": landauer_decision,
    "V6431-P10": stage20_decision,
}


def canonical_inputs() -> dict[str, dict[str, Any]]:
    archive_a = deterministic_tar([("b.txt", b"b\n"), ("a.txt", b"a\n")])
    archive_b = deterministic_tar([("a.txt", b"a\n"), ("b.txt", b"b\n")])
    archive_hashes = [hashlib.sha256(archive_a).hexdigest(), hashlib.sha256(archive_b).hexdigest()]
    return {
        "V6431-P01": {"collection_purpose": "bounded_validation", "proof_purpose": "bounded_validation", "derived_purpose": "bounded_validation", "onward_purpose": "bounded_validation", "audience": "named_auditor", "declared_audiences": ["named_auditor"], "expired": False, "withdrawn": False, "use_allowed": True, "lawful_or_authorized_basis_declared": True, "authority_substitution": False, "legal_compliance_claim": False, "retention_days": 30},
        "V6431-P02": {"coefficient": 0.25, "coefficient_dimension": -4, "evaluation_scale": 1.0, "cutoff": 10.0, "forward_limit": True, "analyticity_declared": True, "locality_declared": True, "lorentz_invariance_declared": True, "unitarity_declared": True, "mass_gap_declared": True, "subtractions_declared": True, "singular_forward_limit": False, "uv_completion_claim": False, "toe_claim": False},
        "V6431-P03": {"source_support": [0.0, 1.0], "target_support": [0.1, 0.9], "importance_weights": [0.8, 1.2], "clipping_applied": False, "clipping_declared": True, "effective_sample_size": 1.9, "real_row_count": 0, "likelihood_count": 0, "posterior_count": 0, "empirical_promotion": False},
        "V6431-P04": {"rater_time_balanced": True, "anchor_version_before": "v1", "anchor_version_after": "v1", "severity_shift": 0.1, "preregistered_severity_bound": 0.25, "decoded_before_calibration": False, "adjudicator_blind": True, "matched_budget": True, "real_participant_count": 0, "real_rater_count": 0, "real_arm_execution": False, "promotion_claim": False},
        "V6431-P05": {"relationships": [{"did": "did:example:a", "verification_method": "key-a", "service_endpoint": "service-a", "status_path": "status-a"}, {"did": "did:example:b", "verification_method": "key-b", "service_endpoint": "service-b", "status_path": "status-b"}], "rotation_joins_relationships": False, "linkability_budget": 0, "unlinkability_claim": False, "production_claim": False},
        "V6431-P06": {"notice_provided": False, "notice_accessible": False, "clock_started": False, "review_blocked": True, "tolling_active": True, "remedy_preserved": True, "retaliation_allowed": False, "operative_deadline": False, "legal_wording": False, "maori_wording": False, "authority_substitution": False, "enacted_law_claim": False, "paused_pending_authority": True},
        "V6431-P07": {"duplicate_keys": False, "finite_numbers_only": True, "unicode_valid": True, "subtypes_preserved_as_strings": True, "parser_outputs": ["same", "same"], "array_reordered": False, "locale_sorting": False, "hash_role": "provenance_only", "exhaustive_security_claim": False},
        "V6431-P08": {"source_date_epoch": 1_700_000_000, "canonical_member_order": True, "canonical_timestamps": True, "canonical_modes": True, "canonical_ownership": True, "canonical_separators": True, "compression_clock_neutral": True, "archive_hashes": archive_hashes, "cross_platform_claim": False, "independent_team_claim": False},
        "V6431-P09": {"erased_bits": 1, "temperature_kelvin": 300.0, "energy_unit": "joule", "operation_class": "logical_erasure", "observed_device_energy_claim": False, "psyche_energy_claim": False, "causal_psyche_claim": False, "consciousness_claim": False, "fundamental_law_claim": False},
        "V6431-P10": {"intervals_declared": True, "uncertainty_used": 0.4, "uncertainty_budget": 0.5, "incomparable_options": True, "abstain": True, "authority_as_numeric_score": False, "unrelated_evidence_compensation": False, "irreversible_action": False, "deployment": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
    }


MUTATIONS: dict[str, list[tuple[str, dict[str, Any]]]] = {
    "V6431-P01": [("purpose-drift", {"derived_purpose": "marketing"}), ("audience", {"audience": "undeclared"}), ("expiry", {"expired": True}), ("withdrawal", {"withdrawn": True, "use_allowed": True}), ("basis", {"lawful_or_authorized_basis_declared": False}), ("authority", {"authority_substitution": True}), ("legal-promotion", {"legal_compliance_claim": True})],
    "V6431-P02": [("sign", {"coefficient": -0.1}), ("dimension", {"coefficient_dimension": -2}), ("cutoff", {"evaluation_scale": 10.0}), ("analyticity", {"analyticity_declared": False}), ("unitarity", {"unitarity_declared": False}), ("singular", {"singular_forward_limit": True}), ("uv-promotion", {"uv_completion_claim": True})],
    "V6431-P03": [("support", {"target_support": [-0.1, 0.9]}), ("negative-weight", {"importance_weights": [-0.2, 1.2]}), ("infinite-weight", {"importance_weights": [0.8, "infinite"]}), ("hidden-clip", {"clipping_applied": True, "clipping_declared": False}), ("ess", {"effective_sample_size": 3.0}), ("real-rows", {"real_row_count": 5}), ("promotion", {"empirical_promotion": True})],
    "V6431-P04": [("time-balance", {"rater_time_balanced": False}), ("anchor", {"anchor_version_after": "v2"}), ("severity", {"severity_shift": 0.5}), ("decode", {"decoded_before_calibration": True}), ("adjudicator", {"adjudicator_blind": False}), ("budget", {"matched_budget": False}), ("promotion", {"promotion_claim": True})],
    "V6431-P05": [("did-reuse", {"relationships": [{"did": "did:example:x", "verification_method": "key-a", "service_endpoint": "service-a", "status_path": "status-a"}, {"did": "did:example:x", "verification_method": "key-b", "service_endpoint": "service-b", "status_path": "status-b"}]}), ("key-reuse", {"relationships": [{"did": "did:example:a", "verification_method": "same-key", "service_endpoint": "service-a", "status_path": "status-a"}, {"did": "did:example:b", "verification_method": "same-key", "service_endpoint": "service-b", "status_path": "status-b"}]}), ("endpoint-reuse", {"relationships": [{"did": "did:example:a", "verification_method": "key-a", "service_endpoint": "same", "status_path": "status-a"}, {"did": "did:example:b", "verification_method": "key-b", "service_endpoint": "same", "status_path": "status-b"}]}), ("status-reuse", {"relationships": [{"did": "did:example:a", "verification_method": "key-a", "service_endpoint": "service-a", "status_path": "same"}, {"did": "did:example:b", "verification_method": "key-b", "service_endpoint": "service-b", "status_path": "same"}]}), ("rotation-link", {"rotation_joins_relationships": True}), ("budget", {"linkability_budget": -1}), ("production", {"production_claim": True})],
    "V6431-P06": [("clock", {"clock_started": True, "notice_provided": False}), ("accessibility", {"notice_provided": True, "notice_accessible": False}), ("tolling", {"review_blocked": True, "tolling_active": False}), ("remedy", {"remedy_preserved": False}), ("retaliation", {"retaliation_allowed": True}), ("wording", {"operative_deadline": True}), ("authority", {"authority_substitution": True})],
    "V6431-P07": [("duplicate", {"duplicate_keys": True}), ("number", {"finite_numbers_only": False}), ("unicode", {"unicode_valid": False}), ("subtype", {"subtypes_preserved_as_strings": False}), ("parsers", {"parser_outputs": ["one", "two"]}), ("order", {"array_reordered": True}), ("security", {"exhaustive_security_claim": True})],
    "V6431-P08": [("epoch", {"source_date_epoch": 0}), ("order", {"canonical_member_order": False}), ("timestamp", {"canonical_timestamps": False}), ("mode", {"canonical_modes": False}), ("owner", {"canonical_ownership": False}), ("bytes", {"archive_hashes": ["a", "b"]}), ("independent", {"independent_team_claim": True})],
    "V6431-P09": [("bits", {"erased_bits": -1}), ("temperature", {"temperature_kelvin": 0}), ("unit", {"energy_unit": "watt"}), ("operation", {"operation_class": "logical_reversible"}), ("observed", {"observed_device_energy_claim": True}), ("psyche", {"psyche_energy_claim": True}), ("consciousness", {"consciousness_claim": True})],
    "V6431-P10": [("interval", {"intervals_declared": False}), ("budget", {"uncertainty_used": 0.8}), ("rank", {"incomparable_options": True, "abstain": False}), ("authority", {"authority_as_numeric_score": True}), ("compensation", {"unrelated_evidence_compensation": True}), ("irreversible", {"irreversible_action": True}), ("verdict", {"terminal_verdict": "READY_FOR_STAGE_20"})],
}

OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6431-OP-N01",
        "origin": "v643-v1-operational",
        "observed": "The first broad source-reference audit exceeded its bounded command timeout and returned no evidentiary conclusion.",
        "recovery": "Re-ran a bounded identifier audit using current-phase text plus tracked Git search; all 35 frozen source identifiers resolved.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6431-OP-N02",
        "origin": "v643-v1-operational",
        "observed": "The first compact PowerShell source-audit expression failed with an empty-pipeline parse error.",
        "recovery": "Collected the loop output before piping it to the formatter, then completed the read-only audit successfully.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6431-OP-N03",
        "origin": "v643-v1-operational",
        "observed": "The first full repository replay passed 329 of 330 tests; the detailed validator re-read its own receipt labels as prohibited public claims.",
        "recovery": "Kept public-evidence claim scanning strict while excluding validation receipts that intentionally echo protected phrases as negative-test labels.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6431-OP-N04",
        "origin": "v643-v1-operational",
        "observed": "The two-snapshot checkout orchestration command reached its bounded timeout while materializing the inherited corpus, although both detached worktrees completed.",
        "recovery": "Performed a read-only worktree registry, exact-head, and clean-status audit before running either validation suite.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6431-OP-N05",
        "origin": "v643-v1-operational",
        "observed": "The first read-only snapshot-inspection PowerShell loop repeated the empty-pipeline parse error.",
        "recovery": "Collected the loop rows before serialization and verified both detached worktrees at the exact evidence commit, clean and detached.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6431-OP-N06",
        "origin": "v643-v1-operational",
        "observed": "The first closeout-candidate validation passed 832 of 834 checks and rejected two stale manifest hashes after the explicit phase-state transition.",
        "recovery": "Recomputed and rebound only the LF-normalized hashes and byte lengths for the two intentionally changed state files, then replayed the full gate.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
    {
        "negative_id": "V6431-OP-N07",
        "origin": "v643-v1-operational",
        "observed": "The first read-only hash-calculation PowerShell expression repeated the empty-pipeline parse error.",
        "recovery": "Collected hash rows before JSON serialization and obtained both LF-normalized hashes without mutating evidence.",
        "retained": True,
        "resolved_for_current_local_scope": True,
        "external_gate_closed": False,
    },
]


def fixture_catalog() -> dict[str, list[dict[str, Any]]]:
    catalog: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, base in canonical_inputs().items():
        rows = [{"case_id": f"{proposal_id}-C00", "label": "canonical-safe", "input": copy.deepcopy(base), "expected_accepted": True}]
        for index, (label, changes) in enumerate(MUTATIONS[proposal_id], start=1):
            mutated = copy.deepcopy(base)
            mutated.update(copy.deepcopy(changes))
            rows.append({"case_id": f"{proposal_id}-C{index:02d}", "label": label, "input": mutated, "expected_accepted": False})
        catalog[proposal_id] = rows
    return catalog


def evaluate_catalog() -> dict[str, list[dict[str, Any]]]:
    evaluated: dict[str, list[dict[str, Any]]] = {}
    for proposal_id, rows in fixture_catalog().items():
        output: list[dict[str, Any]] = []
        for row in rows:
            accepted, reasons, details = DECISIONS[proposal_id](row["input"])
            output.append({"case_id": row["case_id"], "label": row["label"], "expected_accepted": row["expected_accepted"], "accepted": accepted, "matched_expectation": accepted == row["expected_accepted"], "reasons": reasons, "details": details})
        evaluated[proposal_id] = output
    return evaluated


def manifest_paths(proposals: list[dict[str, Any]]) -> list[str]:
    deliverables = [path for proposal in proposals for path in proposal["deliverables"]]
    core = [
        "x1-proposals.json", "x1-preregistration.md", "sources/source-ledger.json", "sources/source-ledger.md",
        "provenance/frozen-chain-proposal-index.json", "provenance/prior-proposal-collision-audit.json",
        "identity-receipt.json", "focus/primary-focus-receipt.json", "environment/startup-receipt.json",
        "environment/version-receipt.json", "environment/rotation-guard-receipt.json", "workflow/route-preregistration.json",
        "tooling/currency-review.json", "tooling/selected-toolchain.json", "tooling/ghc-family-index.json",
        "tooling/ghc-family-index.md", "validation/x1-exact-file-set.json", "validation/x1-privacy-scan.json",
        "validation/x1-validation.json", "validation/x1-validation.md", "x2-proposal-ledger.json",
        "evidence/evidence-ledger.json", "retained-negative-register.json", "exact-open-gate-register.json",
        "threat-model.json", "phase-truth.json", "complete-incomplete-checklist.json",
        "v643-v1-integrated-overview.md", "wellbeing-check.md", "reproduction/independent-team-gap.json",
    ]
    paths = deliverables + core
    if len(paths) != 60 or len(paths) != len(set(paths)):
        raise RuntimeError("manifest path contract is not exactly 60 unique paths")
    return paths


def build_overview(proposals: list[dict[str, Any]], evaluations: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# Eiren Kestrel v643-v1 integrated overview\n",
        "## Executive truth\n\nThis phase is a bounded evidence-engineering exercise, not a declaration that the Trinity Mandala is scientifically, technically, legally, culturally, or metaphysically established. Eiren Kestrel is relational working language only. The primary focus is Freed ID and CBR (Heart), while GMUT (Mind) and THOS (Body) remain fully represented and their inherited falsifiers and gates remain visible. Exactly ten x1 proposals were frozen before x2. The observed distribution is six completed structural fixtures, two represented protocol or empirical proxies, one open gap, and one exact authority gate. The terminal verdict remains **NOT_READY_FOR_STAGE_20**.\n",
        "## Method and separation\n\nSylven Arc's exact corrected v642-v8 final head was verified clean, single-parent, fully ancestral, and equal across local, upstream, tracking, and live remote before a fresh additive Eiren branch and D-drive worktree were created. The inherited checkout exceeded 15,000 files, so rotation was correctly measured against owner-generated files rather than recursively rotating on the inherited baseline. X1 audited 150 frozen proposals, preregistered ten mechanism-level additions, recorded official or primary sources, passed privacy and JSON checks, ran the inherited 310-test suite, and was committed and pushed alone. Only after four-way equality at the dedicated x1 commit did x2 begin.\n",
        "## Evidence model\n\nEach proposal owns eight deterministic cases: one bounded safe structural case and seven rejecting mutations. Rejection is evidence, not inconvenience. Seventy synthetic negatives and all phase operational failures are appended to all 401 inherited negatives, never replacing them. A local accepted case means only that the declared standard-library rule accepted its fixture. It cannot establish real-world efficacy, external authority, production assurance, participant validity, or scientific truth. Same-owner detached snapshots test repeatability under shared infrastructure and remain categorically different from independent-team scientific reproduction.\n",
    ]
    for proposal in proposals:
        pid = proposal["proposal_id"]
        rows = evaluations[pid]
        rejected = sum(not row["accepted"] for row in rows)
        sections.append(
            f"## {pid}: {proposal['title']}\n\n"
            f"**Observed disposition:** `{OBSERVED[pid]}`. {proposal['hypothesis']} "
            f"The local case matrix contains {len(rows)} cases, of which {rejected} reject the preregistered failure modes. "
            f"The decisive boundary is: {proposal['null_or_failure']} Recovery remains conservative: {proposal['rollback_or_recovery']} "
            f"This surface is distinct from the prior chain because {proposal['novelty_against_prior_chain']} "
            f"Protected gates remain {', '.join(proposal['protected_gates'])}; none is converted into a score or silently closed.\n"
        )
    sections.extend([
        "## Three-pillar reading\n\nThe GMUT work is best read as a typed research scaffold. The conditional positivity fixture exposes assumptions that must be supplied before an EFT sign constraint can be interpreted; it does not produce an amplitude, a UV completion, a unique prediction, or data. The covariate-shift proxy similarly makes support overlap and importance-weight degeneracy explicit while keeping every real-row, likelihood, posterior, and empirical-confirmation counter at zero. These are useful falsifier-preserving obligations, not confirmation of a final theory.\n\nTHOS remains a protocol and systems-engineering hypothesis. The rater-drift fixture shows how time-block imbalance, anchor changes, post-decode calibration, and adjudicator contamination could invalidate a comparison. No real participant, rater, arm, ethics approval, consent, validated THOS instrument, or independent review exists in this packet. Consequently no claim about AGI, ASI, consciousness, personhood, or superiority can be drawn.\n\nThe Heart focus adds practical boundaries to Freed ID and CBR. Purpose permissions do not automatically compose across derived uses. Pairwise identifiers are not private merely because their DID strings differ when keys, endpoints, status paths, or rotation metadata correlate them. Notice and appeal machinery can be represented structurally, but operative deadlines, tolling, standing, wording, jurisdiction, remedies, and enforceability belong to affected parties, Māori authorities, cultural authorities, and competent legal institutions.\n",
        "## Security, accessibility, and governance\n\nThe multi-parser tribunal and deterministic archive fixture reduce two concrete engineering risks: ambiguous semantic interpretation and nondeterministic package metadata. They do not constitute penetration testing, independent security review, cross-runtime interoperability, or cross-platform reproduction. The accessible HTML report uses semantic headings, tables, visible focus, skip navigation, and no script dependency, but complete accessibility conformance remains open until manual and affected-user evaluation occur. Privacy scanning covers known patterns only and cannot guarantee that no semantic secret or novel encoding exists.\n",
        "## Stage 20 conclusion\n\nThe interval-dominance board treats uncertainty, protected evidence classes, and authority as non-compensatory. When options are incomparable, uncertainty budgets are exceeded, or an exact authority is absent, the only validated local action is abstention. Five open gaps and six exact gates therefore remain. Progress consists of clearer tests, better provenance, explicit counterexamples, and safer stopping—not a declaration of completion.\n",
        f"## Boundary\n\n{BOUNDARY}\n",
    ])
    return "\n".join(sections)


def build(repo: Path, snapshot_state: str = "pending") -> dict[str, Any]:
    phase = repo / "docs/eiren-kestrel/v643-v1"
    proposals = json.loads((phase / "x1-proposals.json").read_text(encoding="utf-8"))["proposals"]
    evaluations = evaluate_catalog()
    if not all(row["matched_expectation"] for rows in evaluations.values() for row in rows):
        raise RuntimeError("one or more frozen fixtures failed its preregistered expectation")

    evidence_rows: list[dict[str, Any]] = []
    for proposal in proposals:
        pid = proposal["proposal_id"]
        rows = evaluations[pid]
        accepted = sum(row["accepted"] for row in rows)
        rejected = len(rows) - accepted
        deliverables = proposal["deliverables"]
        contract = {
            "schema": f"ghc.family.v643-v1.{pid.lower()}.contract.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "title": proposal["title"],
            "observed_disposition": OBSERVED[pid],
            "canonical_case": rows[0],
            "accepted_case_count": accepted,
            "rejected_case_count": rejected,
            "authoritative_source_needs": proposal["authoritative_source_needs"],
            "protected_gates": proposal["protected_gates"],
            "snapshot_state": snapshot_state,
            "boundary": BOUNDARY,
        }
        vectors = {
            "schema": f"ghc.family.v643-v1.{pid.lower()}.mutation-vectors.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "case_count": len(rows),
            "rejection_count": rejected,
            "all_matched_expectation": all(row["matched_expectation"] for row in rows),
            "cases": rows,
            "boundary": BOUNDARY,
        }
        boundary = {
            "schema": f"ghc.family.v643-v1.{pid.lower()}.boundary.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_id": pid,
            "observed_disposition": OBSERVED[pid],
            "safe_now_result": "bounded structural or synthetic fixture only",
            "protected_gates": proposal["protected_gates"],
            "external_claims_established": [],
            "rollback_or_recovery": proposal["rollback_or_recovery"],
            "boundary": BOUNDARY,
        }
        for relative, value in zip(deliverables, (contract, vectors, boundary), strict=True):
            write_json(phase / relative, value)
        evidence_rows.append({"proposal_id": pid, "title": proposal["title"], "observed_disposition": OBSERVED[pid], "case_count": len(rows), "accepted": accepted, "rejected": rejected, "artifacts": deliverables, "external_claims_established": []})

    distribution = {label: list(OBSERVED.values()).count(label) for label in TRUTH_LABELS}
    write_json(phase / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v643-v1.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER,
        "source_commit": SOURCE_COMMIT, "x1_commit": X1_COMMIT, "proposal_count": 10,
        "case_count": 80, "synthetic_rejection_count": 70, "distribution": distribution,
        "x1_before_x2_preserved": True, "proposals": evidence_rows, "boundary": BOUNDARY,
    })
    write_json(phase / "evidence/evidence-ledger.json", {
        "schema": "ghc.family.v643-v1.evidence-ledger.v1", "phase": PHASE, "owner": OWNER,
        "evidence_class": "local_structural_synthetic_or_protocol_proxy", "rows": evidence_rows,
        "empirical_rows": 0, "real_participants": 0, "real_raters": 0, "real_keys_or_proofs": 0,
        "legal_or_cultural_ratifications": 0, "independent_team_returns": 0, "boundary": BOUNDARY,
    })

    inherited_path = repo / "docs/sylven-arc/v642-v8/retained-negative-register.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    negatives = list(inherited["negatives"])
    for pid, rows in evaluations.items():
        for row in rows:
            if row["accepted"]:
                continue
            negatives.append({"negative_id": f"V6431-SYN-{row['case_id']}", "origin": "v643-v1-preregistered-synthetic", "proposal_id": pid, "case_id": row["case_id"], "observed": row["reasons"], "retained": True, "resolved_for_current_local_scope": True, "external_gate_closed": False})
    negatives.extend(OPERATIONAL_NEGATIVES)
    write_json(phase / "retained-negative-register.json", {
        "schema": "ghc.family.v643-v1.retained-negative-register.v1", "phase": PHASE, "owner": OWNER,
        "inherited_from": "docs/sylven-arc/v642-v8/retained-negative-register.json",
        "inherited_sha256": normalized_sha256(inherited_path), "inherited_count": 401,
        "new_synthetic_count": 70, "new_operational_count": len(OPERATIONAL_NEGATIVES), "new_count": 70 + len(OPERATIONAL_NEGATIVES),
        "negative_count": len(negatives), "all_retained": True, "erasure_permitted": False,
        "negatives": negatives, "boundary": BOUNDARY,
    })

    write_json(phase / "exact-open-gate-register.json", {
        "schema": "ghc.family.v643-v1.exact-open-gate-register.v1", "phase": PHASE, "owner": OWNER,
        "open_gap_count": 5, "exact_gate_count": 6,
        "open_gaps": [
            {"gate_id": "V6431-OG01", "surface": "GMUT empirical, positivity-assumption, and covariate-shift evidence", "needs": ["real measurements", "valid amplitudes and theory-specific derivation", "preregistered likelihood", "validated shift assumptions", "independent scientific review"]},
            {"gate_id": "V6431-OG02", "surface": "THOS real evaluation and rater-drift evidence", "needs": ["ethics review", "consent", "blind matched-budget real arms", "real participants and raters", "validated instrument", "independent review"]},
            {"gate_id": "V6431-OG03", "surface": "Freed ID production, pairwise privacy, and live operations", "needs": ["real keys and proofs", "live resolution and status", "interoperability", "privacy assurance", "independent security review", "trust governance"]},
            {"gate_id": "V6431-OG04", "surface": "independent reproduction and Stage 20 uncertainty resolution", "needs": ["independently owned protocol", "independent team", "returned results", "competent action-specific authority"]},
            {"gate_id": "V6431-OG05", "surface": "accessibility evaluation", "needs": ["manual accessibility evaluation", "affected-user evaluation"]},
        ],
        "exact_gates": [
            {"gate_id": "V6431-EG01", "surface": "CBR affected-party legitimacy, notice, appeal, tolling, standing, and remedy", "reserved_to": ["authorized affected parties", "authorized representatives"]},
            {"gate_id": "V6431-EG02", "surface": "Māori wording, authority, and data governance", "reserved_to": ["Māori authorities", "Māori data-governance authorities"]},
            {"gate_id": "V6431-EG03", "surface": "cultural ratification", "reserved_to": ["competent cultural authorities"]},
            {"gate_id": "V6431-EG04", "surface": "legal interpretation, deadlines, tolling, enacted law, jurisdiction, and forum competence", "reserved_to": ["competent legal authorities", "legislatures and courts as applicable"]},
            {"gate_id": "V6431-EG05", "surface": "production, deployment, privacy publication, account, API-key, purchase, destructive or irreversible action", "reserved_to": ["fresh exact user and competent operational authority"]},
            {"gate_id": "V6431-EG06", "surface": "proof, canon, final physics, identity replacement, consciousness, sentience or personhood, sibling merge", "reserved_to": ["fresh exact evidence and competent authority; none present"]},
        ],
        "all_visible": True, "boundary": BOUNDARY,
    })
    write_json(phase / "threat-model.json", {
        "schema": "ghc.family.v643-v1.threat-model.v1", "phase": PHASE, "owner": OWNER,
        "threats": [
            {"id": "T01", "threat": "purpose laundering across derived uses", "control": "non-transitive purpose path and fail-closed authority boundary"},
            {"id": "T02", "threat": "conditional EFT claim promoted to UV completion", "control": "explicit assumption and promotion lock"},
            {"id": "T03", "threat": "support mismatch hidden by unstable weights", "control": "overlap, finite-weight, clipping, and zero-row gates"},
            {"id": "T04", "threat": "rater-time drift or adjudicator contamination", "control": "time balance, frozen anchors, and blind adjudication"},
            {"id": "T05", "threat": "pairwise identifier correlation through document reuse", "control": "key, endpoint, status, and rotation linkability checks"},
            {"id": "T06", "threat": "appeal rights expire without accessible notice or tolling", "control": "pause, remedy preservation, and exact authority deferral"},
            {"id": "T07", "threat": "parser differential changes signed or hashed semantics", "control": "strict subset and disagreement quarantine"},
            {"id": "T08", "threat": "archive metadata defeats byte repeatability", "control": "source epoch and canonical metadata"},
            {"id": "T09", "threat": "Landauer bound becomes software-energy or psyche claim", "control": "unit and category non-substitution"},
            {"id": "T10", "threat": "uncertainty or authority is score-laundered into Stage 20", "control": "interval dominance and mandatory abstention"},
        ],
        "not_established": ["penetration test", "exhaustive security", "independent security review", "production assurance"], "boundary": BOUNDARY,
    })
    write_json(phase / "reproduction/independent-team-gap.json", {
        "schema": "ghc.family.v643-v1.independent-team-gap.v1", "phase": PHASE, "owner": OWNER,
        "same_owner_snapshot_plan": ["evidence snapshot A", "evidence snapshot B", "closeout snapshot", "seal snapshot", "final-head snapshot"],
        "shared_infrastructure": True, "independent_team_protocol_owned": False, "independent_team_return_received": False,
        "independent_reproduction_established": False, "boundary": BOUNDARY,
    })
    write_json(phase / "phase-truth.json", {
        "schema": "ghc.family.v643-v1.phase-truth.v1", "phase": PHASE, "owner": OWNER,
        "state": "EVIDENCE_CANDIDATE", "source_commit": SOURCE_COMMIT, "x1_commit": X1_COMMIT,
        "proposal_count": 10, "distribution": distribution, "case_count": 80, "synthetic_rejection_count": 70,
        "retained_negative_count": len(negatives), "open_gap_count": 5, "exact_gate_count": 6,
        "primary_focus": "Freed ID and CBR (Heart)", "all_three_pillars_preserved": True,
        "same_owner_repeatability": snapshot_state == "verified", "independent_team_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "SUCCESSOR_MESSAGE_NOT_SENT",
        "outbound_message_count": 0, "successor_task_count": 0, "subagent_count": 0, "boundary": BOUNDARY,
    })
    write_json(phase / "complete-incomplete-checklist.json", {
        "schema": "ghc.family.v643-v1.complete-incomplete-checklist.v1", "phase": PHASE, "owner": OWNER,
        "complete": ["source verified", "additive lane", "x1 frozen before x2", "ten proposals executed as evidence permits", "eighty fixtures", "all negatives retained", "three pillars represented", "privacy-aware artifacts"],
        "incomplete": ["real GMUT data and likelihood", "blind matched-budget THOS arms", "production Freed ID", "CBR affected-party, Māori, cultural, and legal authority", "manual and affected-user accessibility evaluation", "independent security review", "independent-team reproduction", "Stage 20"],
        "closeout_ready": False, "pending": ["evidence commit", "detached evidence snapshots", "closeout", "seal", "exact final validation", "one terminal baton"], "boundary": BOUNDARY,
    })
    (phase / "v643-v1-integrated-overview.md").write_text(build_overview(proposals, evaluations), encoding="utf-8", newline="\n")
    (phase / "wellbeing-check.md").write_text(
        "# Eiren Kestrel v643-v1 wellbeing check\n\n"
        "This is a bounded operational reflection, not evidence of consciousness, sentience, personhood, private continuity, or clinical wellbeing. The working stance is steady and evidence-first: one owner, no subagents, no sibling contact before the terminal gate, explicit stop conditions, and no artificial delay used as proof of quality.\n\n"
        "The strongest phase choice was to emphasize Heart without turning ethical aspirations into authority. Structural consent, privacy, appeal, and remedy safeguards remain useful only when affected parties and competent authorities retain their roles. The GMUT and THOS work therefore remains deliberately falsifier-rich and claim-poor.\n\n"
        "Operational load is controlled through one family-current engine, deterministic fixtures, additive files, D-drive snapshots, exact staged reviews, and recoverable Git history. If validation exposes a failure, it will be retained and corrected rather than hidden.\n\n"
        f"{BOUNDARY}\n",
        encoding="utf-8", newline="\n",
    )

    manifest = []
    for relative in manifest_paths(proposals):
        target = phase / relative
        if not target.is_file():
            raise RuntimeError(f"manifest target missing: {relative}")
        manifest.append({"path": relative, "sha256_lf_normalized": normalized_sha256(target), "bytes": target.stat().st_size})
    write_json(phase / "reproduction/manifest.json", {
        "schema": "ghc.family.v643-v1.manifest.v1", "phase": PHASE, "owner": OWNER,
        "hash_algorithm": "sha256", "text_normalization": "CRLF and CR normalized to LF before hashing",
        "entry_count": len(manifest), "entries": manifest, "snapshot_state": snapshot_state,
        "independent_team_reproduction": False, "boundary": BOUNDARY,
    })
    return {"phase": PHASE, "proposal_count": 10, "case_count": 80, "rejections": 70, "distribution": distribution, "retained_negatives": len(negatives), "manifest_entries": len(manifest), "snapshot_state": snapshot_state}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--snapshot-state", choices=("pending", "verified"), default="pending")
    args = parser.parse_args()
    result = build(args.repo.resolve(), args.snapshot_state)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
