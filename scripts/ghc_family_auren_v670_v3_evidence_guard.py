"""Canonical evidence, privacy, proposal, and terminal-route guards."""

from __future__ import annotations

import json
import re
from typing import Any

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROPOSAL_REQUIRED = {
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


class EvidenceGuardError(ValueError):
    """Raised when evidence structure or a protected boundary fails."""


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceGuardError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical_json_bytes(text: str) -> bytes:
    try:
        payload = json.loads(
            text,
            object_pairs_hook=_unique_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(EvidenceGuardError(f"nonfinite value: {value}")),
        )
    except json.JSONDecodeError as exc:
        raise EvidenceGuardError(f"invalid JSON: {exc.msg}") from exc
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def validate_proposal(row: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise EvidenceGuardError("proposal must be an object")
    missing = sorted(PROPOSAL_REQUIRED - row.keys())
    if missing:
        raise EvidenceGuardError(f"missing proposal fields: {missing}")
    if row["expected_disposition"] not in ALLOWED_OUTCOMES:
        raise EvidenceGuardError("outcome label is not permitted")
    if row["external_actions"] != 0:
        raise EvidenceGuardError("proposal may not perform an external action")
    if not row["protected_gates"]:
        raise EvidenceGuardError("protected gates are required")
    if row["expected_disposition"] in {"open_gap", "exact_gate"} and row["execution_lane"] != "held_without_real_world_execution":
        raise EvidenceGuardError("gaps and exact gates must remain held")
    return {
        "accepted": True,
        "proposal_id": row["proposal_id"],
        "disposition": row["expected_disposition"],
        "external_actions": 0,
        "boundary": "proposal structure only",
    }


def five_class_scan(text: str) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_absolute_path": re.compile(r"\b(?:C:\\Users\\[^\\\s]+|D:\\GHC-Archives)(?:\\|\b)", re.IGNORECASE),
        "credential_or_private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}", re.IGNORECASE),
        "private_callable_route": re.compile(r"\b(?:source_thread_id|clientThreadId|resume_value|private_callable_identifier)\b", re.IGNORECASE),
        "transcript_screenshot_or_session_stream": re.compile(r"<codex_delegation>|session_meta\.payload\.id|data:image/|screenshot_[a-z0-9_]*\s*[:=]", re.IGNORECASE),
    }
    hits = [name for name, pattern in patterns.items() if pattern.search(text)]
    return {"classes": list(patterns), "confirmed_hits": hits, "valid": not hits}


def terminal_route_guard(state: dict[str, Any]) -> dict[str, Any]:
    required_true = {
        "clean",
        "pushed",
        "fresh_four_way_equal",
        "canonical_success_once",
        "live_authority_refreshed",
        "unique_exact_title",
        "immediate_reread",
        "duplicate_guard",
        "acknowledgement",
    }
    missing = sorted(key for key in required_true if state.get(key) is not True)
    if missing:
        return {"allowed": False, "missing": missing, "resend_allowed": False}
    if state.get("canonical_replayed") is not False or state.get("send_count") != 0:
        return {"allowed": False, "missing": ["one_success_or_one_send_discipline"], "resend_allowed": False}
    if not state.get("expected_recipient") or state.get("recipient") != state.get("expected_recipient"):
        return {"allowed": False, "missing": ["exact_recipient"], "resend_allowed": False}
    if not state.get("expected_phase") or state.get("phase") != state.get("expected_phase"):
        return {"allowed": False, "missing": ["exact_phase"], "resend_allowed": False}
    return {"allowed": True, "missing": [], "resend_allowed": False}
