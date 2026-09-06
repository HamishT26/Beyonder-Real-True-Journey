#!/usr/bin/env python3
"""Auren v687-v1 owner-local contract core.

The functions operate only on supplied synthetic JSON values. They do not read
private routes, mutate repositories, perform live sends, or promote evidence.
"""

from __future__ import annotations

import argparse
import copy
import io
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable

import ijson
from deepdiff import DeepDiff
from jsonpath_ng.ext import parse as parse_jsonpath


def error(reason: str) -> dict[str, str]:
    return {"error": reason}


def jsonpath_selection(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"document", "expression"}:
        return error("INVALID_SELECTION_REQUEST")
    expression = payload["expression"]
    if not isinstance(expression, str):
        return error("INVALID_EXPRESSION")
    document = copy.deepcopy(payload["document"])
    before = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    try:
        selector = parse_jsonpath(expression)
        values = [match.value for match in selector.find(document)]
    except Exception:
        return error("INVALID_EXPRESSION")
    after = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if before != after:
        return error("INPUT_MUTATED")
    return values


def stream_shape_summary(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"text"} or not isinstance(payload["text"], str):
        return error("INVALID_STREAM_REQUEST")
    raw = payload["text"].encode("utf-8")
    try:
        events = list(ijson.parse(io.BytesIO(raw)))
        value = json.loads(payload["text"])
    except Exception:
        return error("INVALID_JSON")
    starts = sum(event in {"start_map", "start_array"} for _prefix, event, _value in events)
    ends = sum(event in {"end_map", "end_array"} for _prefix, event, _value in events)
    if starts != ends:
        return error("UNBALANCED_STREAM")
    counts = {key: 0 for key in ("arrays", "booleans", "maps", "nulls", "numbers", "strings")}
    max_depth = 0

    def visit(node: object, depth: int) -> None:
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        if isinstance(node, dict):
            counts["maps"] += 1
            for item in node.values():
                visit(item, depth + 1)
        elif isinstance(node, list):
            counts["arrays"] += 1
            for item in node:
                visit(item, depth + 1)
        elif node is None:
            counts["nulls"] += 1
        elif isinstance(node, bool):
            counts["booleans"] += 1
        elif isinstance(node, (int, float)):
            counts["numbers"] += 1
        elif isinstance(node, str):
            counts["strings"] += 1
        else:
            raise TypeError(node)

    visit(value, 0)
    return {"balanced": True, "counts": counts, "max_depth": max_depth}


def _diff_paths(before: object, after: object, prefix: str = "$") -> set[str]:
    if type(before) is not type(after):
        return {prefix}
    if isinstance(before, dict):
        paths: set[str] = set()
        for key in set(before) | set(after):
            child = f"{prefix}.{key}"
            if key not in before or key not in after:
                paths.add(child)
            else:
                paths.update(_diff_paths(before[key], after[key], child))
        return paths
    if isinstance(before, list):
        paths = set()
        for index in range(max(len(before), len(after))):
            child = f"{prefix}[{index}]"
            if index >= len(before) or index >= len(after):
                paths.add(child)
            else:
                paths.update(_diff_paths(before[index], after[index], child))
        return paths
    return set() if before == after else {prefix}


def structural_delta_policy(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"after", "allowed_paths", "before"}:
        return error("INVALID_DELTA_REQUEST")
    allowed = payload["allowed_paths"]
    if not isinstance(allowed, list) or any(not isinstance(path, str) or not path.startswith("$") for path in allowed):
        return error("INVALID_ALLOWED_PATHS")
    changed = sorted(_diff_paths(payload["before"], payload["after"]))
    package_changed = bool(DeepDiff(payload["before"], payload["after"], ignore_order=False))
    if package_changed != bool(changed):
        return error("DELTA_ENGINE_DISAGREEMENT")
    forbidden = [path for path in changed if not any(path == root or path.startswith(root + ".") or path.startswith(root + "[") for root in allowed)]
    return {
        "changed_paths": changed,
        "decision": "no_change" if not changed else ("allowed_paths_only" if not forbidden else "forbidden_change"),
        "forbidden_paths": forbidden,
    }


def _valid_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and "." not in path.parts


def owner_scope_partition(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"paths"} or not isinstance(payload["paths"], list):
        return error("INVALID_SCOPE_REQUEST")
    paths = payload["paths"]
    if any(not _valid_repo_path(path) for path in paths):
        return error("INVALID_REPOSITORY_PATH")
    if len(paths) != len(set(paths)):
        return error("DUPLICATE_PATH")
    current, inherited, outside = [], [], []
    for path in sorted(paths):
        if path.startswith("docs/auren-lark/v687-v1/") or path.startswith("scripts/ghc_family_auren_lark_v687_v1") or path.startswith("tests/test_ghc_family_auren_lark_v687_v1"):
            current.append(path)
        elif path.startswith("docs/") or path.startswith("scripts/") or path.startswith("tests/"):
            inherited.append(path)
        else:
            outside.append(path)
    return {"current_owner": current, "inherited_read_only": inherited, "outside_scope": outside}


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def manifest_coverage(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"expected", "observed"}:
        return error("INVALID_MANIFEST_REQUEST")
    expected, observed = payload["expected"], payload["observed"]
    if not isinstance(expected, dict) or not isinstance(observed, dict):
        return error("INVALID_MANIFEST_MAP")
    if any(not _valid_repo_path(path) or not _is_sha256(value) for mapping in (expected, observed) for path, value in mapping.items()):
        return error("INVALID_MANIFEST_ENTRY")
    missing = sorted(set(expected) - set(observed))
    unexpected = sorted(set(observed) - set(expected))
    mismatched = sorted(path for path in set(expected) & set(observed) if expected[path] != observed[path])
    return {"mismatched": mismatched, "missing": missing, "unexpected": unexpected, "valid": not (missing or unexpected or mismatched)}


def _parse_instant(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("not text")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("offset required")
    return parsed.astimezone(timezone.utc)


def evidence_expiry_state(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"as_of", "expires_at", "observed_at"}:
        return error("INVALID_EXPIRY_REQUEST")
    try:
        observed = _parse_instant(payload["observed_at"])
        as_of = _parse_instant(payload["as_of"])
        expires = None if payload["expires_at"] is None else _parse_instant(payload["expires_at"])
    except (TypeError, ValueError):
        return error("INVALID_INSTANT")
    if as_of < observed:
        state = "not_yet_effective"
    elif expires is None:
        state = "unknown_expiry"
    elif expires < observed:
        return error("INVALID_EXPIRY_ORDER")
    elif as_of <= expires:
        state = "fresh"
    else:
        state = "expired"
    return {"state": state, "world_verified": False}


def failure_recovery_pair(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"failure", "recovery"}:
        return error("INVALID_PAIR_REQUEST")
    failure, recovery = payload["failure"], payload["recovery"]
    if not isinstance(failure, dict) or not isinstance(recovery, dict) or set(failure) != {"criterion", "id", "passed"} or set(recovery) != {"corrects", "criterion", "id", "passed"}:
        return error("INVALID_PAIR_SHAPE")
    values = (failure["id"], recovery["id"], recovery["corrects"], failure["criterion"], recovery["criterion"])
    if any(not isinstance(value, str) or not value for value in values) or type(failure["passed"]) is not bool or type(recovery["passed"]) is not bool:
        return error("INVALID_PAIR_FIELD")
    valid = failure["passed"] is False and recovery["passed"] is True and failure["id"] != recovery["id"] and recovery["corrects"] == failure["id"] and recovery["criterion"] == failure["criterion"]
    return {"failure_retained": True, "original_success_credit": 0, "valid_recovery_pair": valid}


def dependency_closure(payload: object) -> object:
    if not isinstance(payload, dict) or set(payload) != {"nodes"} or not isinstance(payload["nodes"], dict):
        return error("INVALID_DEPENDENCY_REQUEST")
    nodes = payload["nodes"]
    if any(not isinstance(name, str) or not name or not isinstance(reqs, list) or any(not isinstance(req, str) or not req for req in reqs) for name, reqs in nodes.items()):
        return error("INVALID_DEPENDENCY_NODE")
    missing = sorted({req for reqs in nodes.values() for req in reqs if req not in nodes})
    if missing:
        return {"missing": missing, "order": [], "state": "missing_dependency"}
    incoming = {name: set(reqs) for name, reqs in nodes.items()}
    order: list[str] = []
    while incoming:
        ready = sorted(name for name, reqs in incoming.items() if not reqs)
        if not ready:
            return {"missing": [], "order": [], "state": "cycle"}
        for name in ready:
            order.append(name)
            del incoming[name]
        for reqs in incoming.values():
            reqs.difference_update(ready)
    return {"missing": [], "order": order, "state": "closed"}


def route_attempt_lattice(payload: object) -> object:
    required = {"acknowledgement", "reread", "replacement_created", "resend_count", "resolution_count", "send_count"}
    if not isinstance(payload, dict) or set(payload) != required:
        return error("INVALID_ROUTE_REQUEST")
    if any(type(payload[key]) is not int or payload[key] < 0 for key in ("resolution_count", "send_count", "resend_count")) or type(payload["reread"]) is not bool or type(payload["replacement_created"]) is not bool:
        return error("INVALID_ROUTE_FIELD")
    if payload["acknowledgement"] not in {"none", "acknowledged", "opaque", "rejected", "unavailable"}:
        return error("INVALID_ACKNOWLEDGEMENT")
    if payload["replacement_created"] or payload["resend_count"]:
        return error("PROHIBITED_ROUTE_MUTATION")
    if payload["resolution_count"] == 0:
        return {"state": "OPEN_ROUTE_GAP"}
    if payload["resolution_count"] > 1:
        return {"state": "AMBIGUOUS_ROUTE"}
    if not payload["reread"]:
        return {"state": "PREPARED_NOT_SENT_REREAD_REQUIRED"}
    if payload["send_count"] == 0:
        return {"state": "ELIGIBLE_FOR_ONE_SEND"}
    if payload["send_count"] != 1:
        return error("INVALID_SEND_COUNT")
    states = {
        "acknowledged": "SENT_ONCE_ACKNOWLEDGED",
        "opaque": "SENT_ONCE_TOOL_ACCEPTED_OPAQUE_NO_RESEND",
        "rejected": "PREPARED_NOT_SENT_REJECTED",
        "unavailable": "PREPARED_NOT_SENT_ROUTE_UNAVAILABLE",
        "none": "PREPARED_NOT_SENT_ACKNOWLEDGEMENT_MISSING",
    }
    return {"state": states[payload["acknowledgement"]]}


def terminal_handoff_readiness(payload: object) -> object:
    guards = [
        "sealed", "pushed", "clean", "fresh_equal", "validated", "current_authority",
        "unique_recipient", "recipient_reread", "not_previously_sent", "usage_available",
        "privacy_clear", "safety_clear",
    ]
    if not isinstance(payload, dict) or set(payload) != set(guards) or any(type(payload[key]) is not bool for key in guards):
        return error("INVALID_TERMINAL_GUARDS")
    missing = [key for key in guards if not payload[key]]
    return {"decision": "eligible_for_one_send" if not missing else "held", "missing": missing, "send_performed": False}


OPERATIONS: dict[str, Callable[[object], object]] = {
    "jsonpath_selection": jsonpath_selection,
    "stream_shape_summary": stream_shape_summary,
    "structural_delta_policy": structural_delta_policy,
    "owner_scope_partition": owner_scope_partition,
    "manifest_coverage": manifest_coverage,
    "evidence_expiry_state": evidence_expiry_state,
    "failure_recovery_pair": failure_recovery_pair,
    "dependency_closure": dependency_closure,
    "route_attempt_lattice": route_attempt_lattice,
    "terminal_handoff_readiness": terminal_handoff_readiness,
}


def execute(operation: str, payload: object) -> object:
    handler = OPERATIONS.get(operation)
    if handler is None:
        return error("UNKNOWN_OPERATION")
    return handler(copy.deepcopy(payload))


def typed_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(typed_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def cli(allowed: set[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", choices=sorted(allowed), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = execute(args.operation, payload)
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0
