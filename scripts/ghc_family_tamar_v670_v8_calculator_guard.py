"""Fail-closed structural guards for Tamar Vey v670-v8 synthetic evidence."""

from __future__ import annotations

import json
import math
import re
from typing import Any


class EvidenceGuardError(ValueError):
    """Raised when a bounded evidence contract crosses its frozen boundary."""


ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
ALLOWED_APPROVAL_CLASSES = {"safe_now", "bounded_candidate", "open_gap", "exact_gate"}
ALLOWED_LANES = {"owner_local_symbolic_or_synthetic_x2", "held_without_real_world_execution"}
REQUIRED_FIELDS = {
    "proposal_id",
    "title",
    "hypothesis",
    "null_or_failure_condition",
    "approval_class",
    "execution_lane",
    "official_or_primary_source_needs",
    "concrete_artifacts",
    "falsifier_or_acceptance_gate",
    "rollback_or_recovery",
    "protected_gates",
    "expected_disposition",
    "external_actions",
}


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceGuardError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise EvidenceGuardError(f"non-finite JSON value: {value}")


def canonical_json_bytes(payload: str | dict[str, Any] | list[Any]) -> bytes:
    """Return deterministic UTF-8 JSON after rejecting duplicates and non-finite values."""

    value = (
        json.loads(payload, object_pairs_hook=_pairs_no_duplicates, parse_constant=_reject_constant)
        if isinstance(payload, str)
        else payload
    )

    def check(item: Any) -> None:
        if isinstance(item, float) and not math.isfinite(item):
            raise EvidenceGuardError("non-finite JSON value")
        if isinstance(item, dict):
            for child in item.values():
                check(child)
        elif isinstance(item, list):
            for child in item:
                check(child)

    check(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def validate_proposal(row: dict[str, Any]) -> dict[str, Any]:
    """Validate only the frozen structural contract, never a real calculator or decision."""

    missing = sorted(REQUIRED_FIELDS - set(row))
    if missing:
        raise EvidenceGuardError(f"missing fields: {missing}")
    if row["expected_disposition"] not in ALLOWED_OUTCOMES:
        raise EvidenceGuardError("invalid outcome label")
    if row["approval_class"] not in ALLOWED_APPROVAL_CLASSES:
        raise EvidenceGuardError("invalid approval class")
    if row["execution_lane"] not in ALLOWED_LANES:
        raise EvidenceGuardError("invalid execution lane")
    if row["external_actions"] != 0:
        raise EvidenceGuardError("external action promotion rejected")
    if not isinstance(row["protected_gates"], list) or not row["protected_gates"]:
        raise EvidenceGuardError("protected gates are required")
    if not isinstance(row["concrete_artifacts"], list) or not row["concrete_artifacts"]:
        raise EvidenceGuardError("concrete artifacts are required")
    held = row["expected_disposition"] in {"open_gap", "exact_gate"}
    if held != (row["execution_lane"] == "held_without_real_world_execution"):
        raise EvidenceGuardError("held outcome and execution lane disagree")
    return {
        "accepted": True,
        "proposal_id": row["proposal_id"],
        "outcome": row["expected_disposition"],
        "external_actions": 0,
        "authority_conferred": False,
        "real_observation": False,
    }


def five_class_scan(text: str) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I
        ),
        "private_route_or_callable": re.compile(
            r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I
        ),
        "credential_assignment": re.compile(
            r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
            re.I,
        ),
        "transcript_or_session_stream": re.compile(
            r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I
        ),
    }
    hits = [name for name, pattern in patterns.items() if pattern.search(text)]
    return {"valid": not hits, "pattern_classes": sorted(patterns), "hits": hits}


def run_named_guard(name: str) -> dict[str, Any]:
    rows = {
        "calculator_identity_vacancy": {
            "accepted": True,
            "object_identity_established": False,
            "external_actions": 0,
        },
        "measurement_vacancy": {
            "accepted": True,
            "real_measurements": 0,
            "professional_interpretation": False,
            "external_actions": 0,
        },
        "authority_vacancy": {
            "accepted": True,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
            "external_actions": 0,
        },
        "privacy_vacancy": {
            "accepted": True,
            "real_personal_data": 0,
            "privacy_completeness_claimed": False,
            "external_actions": 0,
        },
        "gmuthos_nonpromotion": {
            "accepted": True,
            "empirical_gmut_evidence": False,
            "real_thos_participants": 0,
            "external_actions": 0,
        },
        "stage20_nonadmission": {
            "accepted": True,
            "admission": False,
            "external_actions": 0,
        },
    }
    try:
        return rows[name]
    except KeyError as exc:
        raise EvidenceGuardError(f"unknown guard: {name}") from exc
