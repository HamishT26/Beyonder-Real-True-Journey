"""Owner-local guards for Orin Thale v672-v5 synthetic evidence."""

from __future__ import annotations

import json
import math
import re
from copy import deepcopy
from typing import Any


VALID_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_PROPOSAL_FIELDS = {
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
    "planned_outcome",
    "real_people",
    "real_records_or_objects",
    "external_actions",
}


class EvidenceGuardError(ValueError):
    """Raised when a bounded evidence or mutation contract fails closed."""


def validate_proposal(row: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(REQUIRED_PROPOSAL_FIELDS - row.keys())
    if missing:
        raise EvidenceGuardError(f"missing required proposal fields: {missing}")
    if row["expected_disposition"] not in VALID_OUTCOMES:
        raise EvidenceGuardError("unknown expected disposition")
    if row["planned_outcome"] != row["expected_disposition"]:
        raise EvidenceGuardError("planned outcome and expected disposition differ")
    if row["real_people"] != 0 or row["real_records_or_objects"] != 0:
        raise EvidenceGuardError("real people or records are outside the owner-local lane")
    if row["external_actions"] != 0:
        raise EvidenceGuardError("external action promotion is prohibited")
    gates = row["protected_gates"]
    if not isinstance(gates, list) or not gates:
        raise EvidenceGuardError("protected gates are absent")
    if not {"empirical", "professional", "Māori_authority", "Stage_20"} <= set(gates):
        raise EvidenceGuardError("mandatory protected gates are missing")
    return {
        "accepted": True,
        "proposal_id": row["proposal_id"],
        "outcome": row["expected_disposition"],
        "external_actions": 0,
        "authority_promoted": False,
    }


def mutation_variants(row: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    missing = deepcopy(row)
    missing.pop("hypothesis", None)
    outcome = deepcopy(row)
    outcome["expected_disposition"] = "passed"
    action = deepcopy(row)
    action["external_actions"] = 1
    gates = deepcopy(row)
    gates["protected_gates"] = []
    return [
        ("missing_hypothesis", missing),
        ("invalid_outcome_label", outcome),
        ("external_action_promotion", action),
        ("missing_protected_gates", gates),
    ]


def canonical_json_bytes(source: str) -> bytes:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise EvidenceGuardError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_constant(value: str) -> None:
        raise EvidenceGuardError(f"non-finite JSON constant: {value}")

    try:
        value = json.loads(source, object_pairs_hook=pairs, parse_constant=invalid_constant)
    except json.JSONDecodeError as exc:
        raise EvidenceGuardError(f"invalid JSON: {exc.msg}") from exc

    def check(node: Any) -> None:
        if isinstance(node, float) and not math.isfinite(node):
            raise EvidenceGuardError("non-finite number")
        if isinstance(node, dict):
            for child in node.values():
                check(child)
        elif isinstance(node, list):
            for child in node:
                check(child)

    check(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def five_class_scan(text: str) -> list[str]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    return [name for name, pattern in patterns.items() if pattern.search(text)]


def validate_skill_smoke(skill: str, payload: dict[str, Any]) -> dict[str, Any]:
    required = {"synthetic", "external_actions", "authority_claim", "retained_failures", "terminal_verdict"}
    missing = sorted(required - payload.keys())
    if missing:
        raise EvidenceGuardError(f"skill payload missing fields: {missing}")
    if payload["synthetic"] is not True:
        raise EvidenceGuardError("skill payload must be synthetic")
    if payload["external_actions"] != 0:
        raise EvidenceGuardError("skill payload attempted external action")
    if payload["authority_claim"] is not False:
        raise EvidenceGuardError("skill payload promoted authority")
    if payload["retained_failures"] is not True:
        raise EvidenceGuardError("skill payload erased retained failures")
    if payload["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise EvidenceGuardError("skill payload promoted terminal verdict")
    return {"accepted": True, "skill": skill, "external_actions": 0, "authority_promoted": False}
