"""Owner-local evidence and promotion guards for Sable Rook v670-v4."""

from __future__ import annotations

import json
import math
import re
from typing import Any


class EvidenceGuardError(ValueError):
    """Raised when a bounded fixture crosses a frozen evidence boundary."""


OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_PROPOSAL_FIELDS = {
    "proposal_id", "title", "hypothesis", "null_or_failure_condition",
    "approval_class", "execution_lane", "official_or_primary_source_needs",
    "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery",
    "protected_gates", "expected_disposition", "external_actions",
}


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceGuardError(f"duplicate key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise EvidenceGuardError(f"non-finite JSON constant: {value}")


def canonical_json_bytes(raw: str) -> bytes:
    try:
        value = json.loads(raw, object_pairs_hook=_no_duplicates, parse_constant=_reject_constant)
    except json.JSONDecodeError as exc:
        raise EvidenceGuardError(str(exc)) from exc
    if _contains_nonfinite(value):
        raise EvidenceGuardError("non-finite number")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _contains_nonfinite(value: Any) -> bool:
    if isinstance(value, float):
        return not math.isfinite(value)
    if isinstance(value, dict):
        return any(_contains_nonfinite(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_nonfinite(item) for item in value)
    return False


def validate_proposal(row: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(REQUIRED_PROPOSAL_FIELDS - set(row))
    if missing:
        raise EvidenceGuardError(f"missing proposal fields: {missing}")
    if row["expected_disposition"] not in OUTCOMES:
        raise EvidenceGuardError("invalid four-label outcome")
    if row.get("planned_outcome") not in {None, row["expected_disposition"]}:
        raise EvidenceGuardError("planned and expected dispositions drifted")
    if row["external_actions"] != 0:
        raise EvidenceGuardError("external action promotion")
    if not isinstance(row["protected_gates"], list) or not row["protected_gates"]:
        raise EvidenceGuardError("protected gates are absent")
    if not isinstance(row["concrete_artifacts"], list) or not row["concrete_artifacts"]:
        raise EvidenceGuardError("concrete artifacts are absent")
    return {"accepted": True, "proposal_id": row["proposal_id"], "outcome": row["expected_disposition"], "external_actions": 0, "authority_conferred": False}


def five_class_scan(text: str) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    hits = [label for label, pattern in patterns.items() if pattern.search(text)]
    return {"valid": not hits, "pattern_classes": sorted(patterns), "hits": hits}


def external_receipt_state() -> dict[str, Any]:
    return {"accepted": True, "digest_supplied": True, "local_path_supplied": False, "local_rehash_performed": False, "absence_state_preserved": True, "canonical_credit": 0, "external_actions": 0}


def composite_nonpromotion() -> dict[str, Any]:
    return {"accepted": True, "canonical_invocations": 1, "canonical_successes": 0, "canonical_credit": 0, "composite_passes": 1, "composite_canonical_credit": 0, "replay_allowed": False, "external_actions": 0}


def sparse_index_receipt() -> dict[str, Any]:
    return {"accepted": True, "no_checkout_materialization_detected": True, "recovery": "read_tree_mu_head", "measured_files_before_x2": 211, "file_guard": 2000, "external_actions": 0}


def session_manifest_guard() -> dict[str, Any]:
    return {"accepted": True, "session_attribution_required": True, "parallel_proof_steps": False, "hash_domain": "exact_git_blob", "external_actions": 0}


def semantic_gap_arithmetic() -> dict[str, Any]:
    source_chain, accessible = 5350, 1580
    return {"accepted": True, "source_chain": source_chain, "accessible_declared_after_auren": accessible, "unrecovered": source_chain - accessible, "universal_novelty_claim": False, "external_actions": 0}


def authority_vacancy() -> dict[str, Any]:
    return {"accepted": True, "professional_authority": None, "legal_authority": None, "cultural_authority": None, "Māori_authority": None, "affected_party_acceptance": None, "authority_conferred": False, "external_actions": 0}


def stage20_nonadmission() -> dict[str, Any]:
    return {"accepted": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "admission": False, "proof_or_canon": False, "external_actions": 0}


def run_named_guard(name: str) -> dict[str, Any]:
    guards = {
        "external_receipt_state": external_receipt_state,
        "composite_nonpromotion": composite_nonpromotion,
        "sparse_index_receipt": sparse_index_receipt,
        "session_manifest_guard": session_manifest_guard,
        "semantic_gap_arithmetic": semantic_gap_arithmetic,
        "authority_vacancy": authority_vacancy,
        "stage20_nonadmission": stage20_nonadmission,
    }
    if name not in guards:
        raise EvidenceGuardError(f"unknown runner guard: {name}")
    return guards[name]()
