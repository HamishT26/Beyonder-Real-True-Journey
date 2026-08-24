#!/usr/bin/env python3
"""Bounded archival controls for the Vesper v668-v1-r2 remaster.

The module operates on synthetic owner-local fixtures.  Its successful results
do not establish authenticity, professional competence, legal compliance,
cultural legitimacy, Maori authority, empirical confirmation, or Stage 20.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict, deque
from copy import deepcopy
from itertools import pairwise
from pathlib import PurePosixPath
from typing import Any


class ContractError(ValueError):
    """Raised when a bounded synthetic contract is rejected."""


PROTECTED_CLAIMS = {
    "empirical",
    "participant",
    "professional",
    "production",
    "legal",
    "cultural",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "theory_of_everything",
    "stage20",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any, algorithm: str = "sha256") -> str:
    hasher = hashlib.new(algorithm)
    hasher.update(value if isinstance(value, bytes) else canonical_bytes(value))
    return hasher.hexdigest()


def validate_control_envelope(row: dict[str, Any]) -> dict[str, Any]:
    required = {
        "control_id": str,
        "schema_version": int,
        "payload_digest": str,
        "claim_class": str,
        "external_action": bool,
        "protected_claims": dict,
    }
    missing = sorted(set(required) - set(row))
    if missing:
        raise ContractError(f"missing required fields: {missing}")
    for field, expected in required.items():
        if not isinstance(row[field], expected) or (expected is int and isinstance(row[field], bool)):
            raise ContractError(f"wrong type for {field}")
    if row["schema_version"] != 1 or not re.fullmatch(r"[0-9a-f]{64}", row["payload_digest"]):
        raise ContractError("schema or digest domain rejected")
    if row["claim_class"] != "bounded_structural":
        raise ContractError("forbidden claim class")
    if row["external_action"]:
        raise ContractError("external action bypass rejected")
    if set(row["protected_claims"]) != PROTECTED_CLAIMS:
        raise ContractError("protected claim set mismatch")
    if any(value is not False for value in row["protected_claims"].values()):
        raise ContractError("protected claim promotion rejected")
    return {
        "state": "PASS_BOUNDED_CONTROL_ENVELOPE",
        "control_id": row["control_id"],
        "payload_digest": row["payload_digest"],
        "external_actions": 0,
        "protected_claims_promoted": 0,
    }


def base_envelope(control_id: str, payload: Any) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "schema_version": 1,
        "payload_digest": digest(payload),
        "claim_class": "bounded_structural",
        "external_action": False,
        "protected_claims": {name: False for name in sorted(PROTECTED_CLAIMS)},
    }


def mutated_envelope(base: dict[str, Any], mutation_class: str) -> dict[str, Any]:
    row = deepcopy(base)
    if mutation_class == "missing_required_field":
        row.pop("payload_digest")
    elif mutation_class == "wrong_type":
        row["schema_version"] = "one"
    elif mutation_class == "forbidden_claim":
        row["claim_class"] = "empirical_confirmation"
    elif mutation_class == "boundary_bypass":
        row["external_action"] = True
    else:
        raise ContractError("unknown mutation class")
    return row


def accession_envelope(identifier: str, payload: bytes) -> dict[str, Any]:
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,63}", identifier):
        raise ContractError("identifier domain rejected")
    return {
        "identifier": identifier,
        "bytes": len(payload),
        "sha256": digest(payload),
        "state": "PASS_SYNTHETIC_ACCESSION_ENVELOPE",
        "authenticity_proven": False,
    }


def custody_order(events: list[dict[str, Any]]) -> list[str]:
    identifiers = [str(row.get("event_id", "")) for row in events]
    if not identifiers or any(not item for item in identifiers) or len(set(identifiers)) != len(identifiers):
        raise ContractError("event identifiers missing or duplicated")
    by_id = {row["event_id"]: row for row in events}
    indegree = {event_id: 0 for event_id in by_id}
    children: dict[str, list[str]] = defaultdict(list)
    for row in events:
        if not isinstance(row.get("recorded_at"), int) or not isinstance(row.get("effective_at"), int):
            raise ContractError("bitemporal values must be integers")
        for parent in row.get("depends_on", []):
            if parent not in by_id:
                raise ContractError("unknown custody dependency")
            children[parent].append(row["event_id"])
            indegree[row["event_id"]] += 1
    queue = deque(sorted(event_id for event_id, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(events):
        raise ContractError("custody ancestry cycle rejected")
    return order


def append_correction(entries: list[dict[str, Any]], target: str, reason: str) -> list[dict[str, Any]]:
    if not entries or target not in {str(row.get("event_id")) for row in entries}:
        raise ContractError("correction target absent")
    if not reason.strip():
        raise ContractError("correction reason absent")
    output = deepcopy(entries)
    output.append({"event_id": f"correction-{len(output) + 1}", "corrects": target, "reason": reason, "tombstone": True})
    return output


def namespace_tribunal(values: list[str]) -> dict[str, Any]:
    canonical = [value.casefold().strip() for value in values]
    if any(not re.fullmatch(r"[a-z0-9._-]+", value) for value in canonical):
        raise ContractError("namespace character domain rejected")
    if len(set(canonical)) != len(canonical):
        raise ContractError("canonical namespace collision")
    return {"state": "PASS_SYNTHETIC_NAMESPACE", "canonical": canonical}


def reversible_redaction(source: str, spans: list[tuple[int, int]], reason_code: str) -> dict[str, Any]:
    if not reason_code or any(start < 0 or end <= start or end > len(source) for start, end in spans):
        raise ContractError("redaction span or reason rejected")
    ordered = sorted(spans)
    if any(left[1] > right[0] for left, right in pairwise(ordered)):
        raise ContractError("overlapping redactions rejected")
    view = source
    for start, end in reversed(ordered):
        view = view[:start] + "[REDACTED]" + view[end:]
    return {"source_sha256": digest(source.encode()), "view": view, "reason_code": reason_code, "source_mutated": False}


def retention_decision(state: str, authority_present: bool, stop_requested: bool) -> dict[str, Any]:
    if stop_requested:
        return {"state": "STOPPED", "destruction_authorized": False}
    if state == "destroy" and not authority_present:
        raise ContractError("destruction without authority rejected")
    return {"state": state.upper(), "destruction_authorized": state == "destroy" and authority_present}


def fixity_quorum(payload: bytes, claimed: dict[str, str]) -> dict[str, Any]:
    if set(claimed) != {"sha256", "sha512"}:
        raise ContractError("exact fixity quorum required")
    observed = {name: digest(payload, name) for name in sorted(claimed)}
    if observed != claimed:
        raise ContractError("fixity mismatch quarantined")
    return {"state": "PASS_SYNTHETIC_FIXITY_QUORUM", "algorithms": sorted(observed), "authenticity_proven": False}


def bagit_paths(paths: list[str]) -> dict[str, Any]:
    normalized: list[str] = []
    for value in paths:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "data":
            raise ContractError("BagIt path confinement rejected")
        item = path.as_posix()
        if item in normalized:
            raise ContractError("duplicate bag member rejected")
        normalized.append(item)
    return {"state": "PASS_SYNTHETIC_BAGIT_PATHS", "members": sorted(normalized)}


def transfer_readback(sender: str, receiver: str) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{64}", sender) or sender != receiver:
        raise ContractError("transfer readback mismatch")
    return {"state": "PASS_SYNTHETIC_TRANSFER_READBACK", "digest": sender, "external_transfer": False}


def role_access(role: str, purpose: str, allowed: dict[str, set[str]]) -> dict[str, Any]:
    granted = role in allowed and purpose in allowed[role]
    return {"state": "GRANTED" if granted else "DENIED", "reason": "declared role-purpose pair" if granted else "least-privilege refusal"}


def language_fallback(tag: str, labels: dict[str, str]) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", tag):
        raise ContractError("language tag rejected")
    selected = labels.get(tag) or labels.get(tag.split("-")[0]) or labels.get("en")
    if not selected:
        raise ContractError("fallback label absent")
    return {"state": "PASS_STRUCTURAL_LANGUAGE_FALLBACK", "label": selected, "maori_authority_claimed": False}


def salvage_queue(items: list[dict[str, Any]], capacity: int) -> dict[str, Any]:
    ranking = {"stop": 0, "critical": 1, "routine": 2}
    if capacity < 1 or any(row.get("priority") not in ranking for row in items):
        raise ContractError("queue domain rejected")
    ordered = sorted(items, key=lambda row: (ranking[row["priority"]], str(row.get("item_id", ""))))
    admitted = ordered[:capacity]
    return {"state": "PASS_SYNTHETIC_SALVAGE_QUEUE", "admitted": admitted, "deferred": ordered[capacity:]}


def route_transition(state: str, event: str) -> str:
    transitions = {
        ("prepared_not_sent", "terminal_gate_passed"): "ready_to_resolve",
        ("ready_to_resolve", "exact_title_unique"): "ready_to_send",
        ("ready_to_send", "acknowledged"): "sent_once_acknowledged",
        ("ready_to_send", "opaque_ack"): "opaque_ack_unresolved_no_resend",
        ("prepared_not_sent", "pause"): "paused_unsent",
    }
    try:
        return transitions[(state, event)]
    except KeyError as exc:
        raise ContractError("route transition rejected") from exc


def validate_flashcard_graph(cards: list[dict[str, Any]]) -> dict[str, Any]:
    required_tiers = ("freed_id_anchor", "pillar", "practice", "task")
    identifiers: set[str] = set()
    for card in cards:
        if tuple(card.get("tier_order", ())) != required_tiers:
            raise ContractError("flashcard tier order rejected")
        if any(not str(card.get(tier, "")).strip() for tier in required_tiers):
            raise ContractError("flashcard tier vacancy")
        identifier = str(card.get("card_id", ""))
        if not identifier or identifier in identifiers:
            raise ContractError("flashcard identifier missing or duplicated")
        identifiers.add(identifier)
    return {"state": "PASS_FOUR_TIER_FLASHCARD_GRAPH", "card_count": len(cards), "tier_count": 4}


def validation_credit_transition(state: str, event: str) -> str:
    transitions = {
        ("not_invoked", "invoke"): "invoked",
        ("invoked", "pass"): "successful_once_no_replay",
        ("invoked", "fail"): "failed_zero_credit",
    }
    if state in {"successful_once_no_replay", "failed_zero_credit"}:
        raise ContractError("terminal validation credit state cannot be replayed")
    try:
        return transitions[(state, event)]
    except KeyError as exc:
        raise ContractError("validation credit transition rejected") from exc
