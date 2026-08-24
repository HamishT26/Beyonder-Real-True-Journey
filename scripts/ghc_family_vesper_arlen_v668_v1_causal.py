"""Owner-local synthetic causal-custody primitives for Vesper v668-v1.

These functions model deterministic software fixtures only.  They do not
control a venue, production, person, device, safety process, credential, or
external service, and they confer no professional or cultural authority.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict, deque
from copy import deepcopy
from typing import Any, Iterable


class ContractError(ValueError):
    """A fail-closed synthetic contract rejection."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_event_graph(events: Iterable[dict[str, Any]]) -> list[str]:
    """Return one stable topological order or reject malformed/cyclic input."""
    rows = [deepcopy(row) for row in events]
    ids = [row.get("event_id") for row in rows]
    if any(not isinstance(event_id, str) or not event_id for event_id in ids):
        raise ContractError("every event requires a nonempty string event_id")
    if len(ids) != len(set(ids)):
        raise ContractError("duplicate event_id")
    by_id = {row["event_id"]: row for row in rows}
    incoming: dict[str, int] = {event_id: 0 for event_id in ids}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        deps = row.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(dep, str) for dep in deps):
            raise ContractError("depends_on must be a string list")
        if len(deps) != len(set(deps)):
            raise ContractError("duplicate dependency")
        for dep in deps:
            if dep not in by_id:
                raise ContractError("missing dependency")
            if dep == row["event_id"]:
                raise ContractError("self dependency")
            outgoing[dep].append(row["event_id"])
            incoming[row["event_id"]] += 1
    ready = deque(sorted(event_id for event_id, count in incoming.items() if count == 0))
    ordered: list[str] = []
    while ready:
        current = ready.popleft()
        ordered.append(current)
        for child in sorted(outgoing[current]):
            incoming[child] -= 1
            if incoming[child] == 0:
                ready.append(child)
        ready = deque(sorted(ready))
    if len(ordered) != len(rows):
        raise ContractError("causal cycle")
    return ordered


def validate_logical_clocks(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [deepcopy(row) for row in events]
    order = validate_event_graph(rows)
    by_id = {row["event_id"]: row for row in rows}
    last_by_source: dict[str, int] = {}
    for event_id in order:
        row = by_id[event_id]
        source = row.get("source")
        sequence = row.get("source_sequence")
        lamport = row.get("lamport")
        if not isinstance(source, str) or not source:
            raise ContractError("source required")
        if not isinstance(sequence, int) or sequence < 0:
            raise ContractError("nonnegative source_sequence required")
        if not isinstance(lamport, int) or lamport < 0:
            raise ContractError("nonnegative lamport required")
        if source in last_by_source and sequence <= last_by_source[source]:
            raise ContractError("decreasing or repeated source_sequence")
        last_by_source[source] = sequence
        for dep in row.get("depends_on", []):
            if by_id[dep].get("lamport", -1) >= lamport:
                raise ContractError("dependency lamport must be smaller")
    return {"state": "PASS_SYNTHETIC_LOGICAL_CLOCKS", "order": order, "wall_clock_authority": False}


def merkle_root(leaves: Iterable[Any]) -> str:
    nodes = [hashlib.sha256(canonical_bytes(leaf)).digest() for leaf in leaves]
    if not nodes:
        return hashlib.sha256(b"").hexdigest()
    while len(nodes) > 1:
        if len(nodes) % 2:
            nodes.append(nodes[-1])
        nodes = [hashlib.sha256(nodes[index] + nodes[index + 1]).digest() for index in range(0, len(nodes), 2)]
    return nodes[0].hex()


def verify_checkpoint(leaves: Iterable[Any], expected_root: str) -> dict[str, Any]:
    actual = merkle_root(leaves)
    if actual != expected_root:
        raise ContractError("checkpoint root mismatch")
    return {"state": "PASS_SYNTHETIC_CHECKPOINT", "root": actual, "authenticity_proof": False, "identity_proof": False}


def replay_events(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [deepcopy(row) for row in events]
    order = validate_event_graph(rows)
    by_id = {row["event_id"]: row for row in rows}
    seen: set[str] = set()
    state = {"active": [], "stopped": False, "acknowledged": []}
    quarantined: list[str] = []
    for event_id in order:
        if event_id in seen:
            quarantined.append(event_id)
            continue
        seen.add(event_id)
        row = by_id[event_id]
        action = row.get("action")
        if action == "cue":
            if not state["stopped"]:
                state["active"].append(row.get("cue", event_id))
        elif action == "ack":
            state["acknowledged"].append(row.get("target"))
        elif action == "stop":
            state["stopped"] = True
        elif action == "noop":
            pass
        else:
            raise ContractError("unknown synthetic action")
    state["active"] = sorted(set(state["active"]))
    state["acknowledged"] = sorted(set(state["acknowledged"]))
    return {"state": state, "quarantined_duplicates": quarantined, "event_order": order, "state_digest": digest(state)}


def replay_with_duplicates(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [deepcopy(row) for row in events]
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    duplicates: list[str] = []
    for row in rows:
        event_id = row.get("event_id")
        if event_id in seen:
            duplicates.append(str(event_id))
            continue
        seen.add(str(event_id))
        unique.append(row)
    receipt = replay_events(unique)
    receipt["quarantined_duplicates"] = duplicates
    return receipt


def append_compensation(journal: list[dict[str, Any]], target_id: str, reason: str) -> list[dict[str, Any]]:
    if not target_id or not any(row.get("event_id") == target_id for row in journal):
        raise ContractError("compensation target absent")
    if not reason or len(reason) > 160:
        raise ContractError("bounded compensation reason required")
    result = deepcopy(journal)
    result.append(
        {
            "event_id": f"compensate-{len(result) + 1:03d}",
            "action": "compensate",
            "target": target_id,
            "reason": reason,
            "erases_original": False,
            "external_rollback_complete": False,
        }
    )
    return result


def bounded_queue(items: Iterable[dict[str, Any]], capacity: int) -> dict[str, Any]:
    if not isinstance(capacity, int) or capacity < 1:
        raise ContractError("positive capacity required")
    rows = [deepcopy(row) for row in items]
    for row in rows:
        if row.get("priority") not in {"stop", "critical", "routine"}:
            raise ContractError("unknown priority")
    ranked = sorted(rows, key=lambda row: ({"stop": 0, "critical": 1, "routine": 2}[row["priority"]], str(row.get("cue_id", ""))))
    accepted = ranked[:capacity]
    rejected = ranked[capacity:]
    if any(row["priority"] == "stop" for row in rejected):
        raise ContractError("stop cue cannot be displaced")
    return {"accepted": accepted, "rejected": rejected, "overflow_visible": bool(rejected), "live_safety_assurance": False}


TRANSITIONS = {
    "draft": {"ready", "cancelled"},
    "ready": {"called", "held", "cancelled"},
    "held": {"ready", "cancelled"},
    "called": {"acknowledged", "stopped"},
    "acknowledged": {"complete", "stopped"},
    "stopped": {"cancelled"},
    "complete": set(),
    "cancelled": set(),
}


def apply_transition(current: str, requested: str, readback: str) -> dict[str, Any]:
    if current not in TRANSITIONS or requested not in TRANSITIONS:
        raise ContractError("unknown state")
    if requested not in TRANSITIONS[current]:
        raise ContractError("illegal transition")
    if not isinstance(readback, str) or not readback.strip():
        raise ContractError("readback required")
    return {"from": current, "to": requested, "readback": readback.strip(), "operator_understanding_proven": False}


def migrate_record(record: dict[str, Any], target_version: int) -> dict[str, Any]:
    row = deepcopy(record)
    version = row.get("schema_version")
    if version not in {1, 2} or target_version not in {1, 2}:
        raise ContractError("unsupported schema version")
    if version == target_version:
        return row
    if version == 1 and target_version == 2:
        if "cue" not in row:
            raise ContractError("v1 cue required")
        known = {"schema_version", "cue", "priority"}
        extras = {key: value for key, value in row.items() if key not in known}
        return {"schema_version": 2, "cue_name": row["cue"], "priority": row.get("priority", "routine"), "preserved_unknown": extras}
    if version == 2 and target_version == 1:
        if "cue_name" not in row:
            raise ContractError("v2 cue_name required")
        result = {"schema_version": 1, "cue": row["cue_name"], "priority": row.get("priority", "routine")}
        unknown = row.get("preserved_unknown", {})
        if not isinstance(unknown, dict):
            raise ContractError("preserved_unknown must be an object")
        result.update(unknown)
        return result
    raise ContractError("unreachable migration")


def append_correction(entries: list[dict[str, Any]], correction: dict[str, Any]) -> list[dict[str, Any]]:
    result = deepcopy(entries)
    prior_digest = digest(result[-1]) if result else hashlib.sha256(b"").hexdigest()
    allowed = {"record_id", "reason_code", "tombstone", "replacement_digest"}
    if set(correction) - allowed:
        raise ContractError("unapproved correction field")
    if not correction.get("record_id") or not correction.get("reason_code"):
        raise ContractError("record and reason required")
    row = {**correction, "prior_digest": prior_digest, "raw_private_payload": False, "legal_erasure_complete": False}
    result.append(row)
    return result


def minimize_note(note: dict[str, Any]) -> dict[str, Any]:
    allowed = {"category", "severity", "action_required", "retention_class"}
    prohibited = set(note) - allowed
    if prohibited:
        raise ContractError("prohibited note fields")
    if note.get("severity") not in {"low", "medium", "high"}:
        raise ContractError("typed severity required")
    return {key: note[key] for key in sorted(note)}


def validation_credit_transition(state: str, event: str) -> str:
    table = {
        ("not_run", "invoke"): "invoked",
        ("invoked", "fail"): "failed_zero_credit",
        ("invoked", "pass"): "successful_once",
        ("failed_zero_credit", "dependency_correction"): "dependency_corrected_noncanonical",
    }
    if (state, event) not in table:
        raise ContractError("validation credit transition refused")
    return table[(state, event)]
