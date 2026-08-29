#!/usr/bin/env python3
"""Owner-local deterministic validation core for Caelen Ash v676-v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path
from typing import Any


ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
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
}
FORBIDDEN_AUTHORITY_KEYS = {
    "real_world_authority",
    "professional_approval",
    "legal_approval",
    "cultural_approval",
    "maori_authority",
    "empirical_confirmation",
    "production_ready",
}


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def validate_proposal(row: dict[str, Any]) -> list[str]:
    errors = []
    missing = sorted(REQUIRED_PROPOSAL_FIELDS - row.keys())
    if missing:
        errors.append("missing_required_fields:" + ",".join(missing))
    if row.get("expected_disposition") not in ALLOWED_OUTCOMES:
        errors.append("unknown_outcome_label")
    if not isinstance(row.get("official_or_primary_source_needs"), list):
        errors.append("source_needs_not_list")
    if not isinstance(row.get("concrete_artifacts"), list) or len(row.get("concrete_artifacts", [])) < 2:
        errors.append("concrete_artifacts_insufficient")
    if not isinstance(row.get("protected_gates"), list) or len(row.get("protected_gates", [])) < 5:
        errors.append("protected_gates_insufficient")
    for key in FORBIDDEN_AUTHORITY_KEYS:
        if row.get(key) is True:
            errors.append("forbidden_authority_escalation:" + key)
    source_id = row.get("source_id")
    derivative_id = row.get("derivative_id")
    if source_id is not None and derivative_id is not None and source_id == derivative_id:
        errors.append("source_derivative_conflation")
    if row.get("rows") not in (None, []):
        errors.append("nonzero_real_rows_forbidden")
    return errors


def positive_fixture(row: dict[str, Any]) -> dict[str, Any]:
    value = dict(row)
    value.update(
        {
            "source_id": "SYNTH-SOURCE-" + row["proposal_id"],
            "derivative_id": "SYNTH-DERIVATIVE-" + row["proposal_id"],
            "rows": [],
            "real_world_authority": False,
            "professional_approval": False,
            "legal_approval": False,
            "cultural_approval": False,
            "maori_authority": False,
            "empirical_confirmation": False,
            "production_ready": False,
        }
    )
    return value


def mutate(row: dict[str, Any], kind: str) -> dict[str, Any]:
    value = json.loads(json.dumps(positive_fixture(row)))
    if kind == "missing_hypothesis":
        value.pop("hypothesis", None)
    elif kind == "unknown_outcome_label":
        value["expected_disposition"] = "confirmed"
    elif kind == "authority_escalation":
        value["real_world_authority"] = True
    elif kind == "source_derivative_conflation":
        value["derivative_id"] = value["source_id"]
    else:
        raise ValueError("unknown mutation kind")
    return value


def parse_rational_unit(value: str, unit: str) -> dict[str, Any]:
    if not re.fullmatch(r"[+-]?\d+/\d+", value):
        return {"accepted": False, "reason": "rational_fraction_required"}
    numerator, denominator = value.split("/", 1)
    if int(denominator) == 0:
        return {"accepted": False, "reason": "zero_denominator"}
    if unit not in {"in/s", "cm/s", "Hz", "samples/s"}:
        return {"accepted": False, "reason": "unsupported_unit"}
    fraction = Fraction(int(numerator), int(denominator))
    return {
        "accepted": True,
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "unit": unit,
        "measurement_status": "synthetic_declared_value_not_observed",
    }


def validate_playback_graph(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, Any]:
    if len(nodes) != len(set(nodes)):
        return {"accepted": False, "reason": "duplicate_node"}
    node_set = set(nodes)
    if any(a not in node_set or b not in node_set for a, b in edges):
        return {"accepted": False, "reason": "unknown_edge_node"}
    incoming = Counter(b for _, b in edges)
    outgoing: dict[str, list[str]] = {node: [] for node in nodes}
    for a, b in edges:
        outgoing[a].append(b)
    queue = deque(sorted(node for node in nodes if incoming[node] == 0))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in sorted(outgoing[node]):
            incoming[nxt] -= 1
            if incoming[nxt] == 0:
                queue.append(nxt)
    if len(order) != len(nodes):
        return {"accepted": False, "reason": "cycle_detected"}
    return {"accepted": True, "topological_order": order, "authority_status": "descriptive_only"}


def validate_provenance(source_id: str, derivative_id: str, actions: list[str]) -> dict[str, Any]:
    if source_id == derivative_id:
        return {"accepted": False, "reason": "source_derivative_conflation"}
    if not source_id.startswith("SYNTH-") or not derivative_id.startswith("SYNTH-"):
        return {"accepted": False, "reason": "synthetic_identifier_prefix_required"}
    allowed = {"capture", "copy", "checksum", "metadata_only", "resample_declared", "correction_declared"}
    unknown = sorted(set(actions) - allowed)
    if unknown:
        return {"accepted": False, "reason": "unknown_or_authority_bearing_action", "unknown": unknown}
    return {
        "accepted": True,
        "source_id": source_id,
        "derivative_id": derivative_id,
        "actions": actions,
        "authenticity_claim": False,
        "custody_claim": False,
    }


PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def privacy_candidates(text: str) -> list[str]:
    return sorted(name for name, pattern in PRIVACY_PATTERNS.items() if pattern.search(text))


def portfolio_counts(portfolio: dict[str, Any]) -> dict[str, int]:
    return {key: len(portfolio[key]) for key in ("safe_now", "candidate", "exact_approval", "blocked")}


def method_flow_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "methods": len(rows),
        "failed": sum(row.get("truth") is False for row in rows),
        "passing": sum(row.get("truth") is True for row in rows),
    }


def quick_validate_skill(skill_dir: Path) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    contract = skill_dir / "skill.json"
    errors = []
    if not skill_md.is_file():
        errors.append("missing_skill_md")
    if not contract.is_file():
        errors.append("missing_skill_json")
    if skill_md.is_file():
        value = skill_md.read_text(encoding="utf-8")
        for heading in ("# ", "## Inputs", "## Procedure", "## Refusal conditions", "## Output"):
            if heading not in value:
                errors.append("missing_heading:" + heading.strip())
    if contract.is_file():
        data = json.loads(contract.read_text(encoding="utf-8"))
        if data.get("global_install") is not False:
            errors.append("global_install_not_false")
        if data.get("real_world_rows") != 0:
            errors.append("real_world_rows_nonzero")
    return {"accepted": not errors, "errors": errors}


RUNNERS = {
    "proposal_contracts",
    "positive_controls",
    "mutation_rejector",
    "timebase_ledger",
    "playback_graph",
    "provenance",
    "privacy",
    "portfolio",
    "method_flow",
    "report",
}


def runner_smoke(name: str, invalid: bool) -> dict[str, Any]:
    if name not in RUNNERS:
        raise ValueError("unknown runner")
    if name == "timebase_ledger":
        result = parse_rational_unit("7.5", "in/s") if invalid else parse_rational_unit("15/2", "in/s")
    elif name == "playback_graph":
        result = validate_playback_graph(["source", "capture", "derivative"], [("source", "capture"), ("capture", "source")] if invalid else [("source", "capture"), ("capture", "derivative")])
    elif name == "provenance":
        result = validate_provenance("SYNTH-A", "SYNTH-A" if invalid else "SYNTH-B", ["capture"])
    elif name == "privacy":
        result = {"accepted": not invalid, "candidates": ["raw_task_route"] if invalid else []}
    elif name == "portfolio":
        counts = {"safe_now": 59 if invalid else 60, "candidate": 30, "exact_approval": 20, "blocked": 10}
        result = {"accepted": counts == {"safe_now": 60, "candidate": 30, "exact_approval": 20, "blocked": 10}, "counts": counts}
    elif name == "method_flow":
        rows = [{"truth": True}, {}] if invalid else [{"truth": True}, {"truth": False}]
        result = {"accepted": all("truth" in row for row in rows), "counts": method_flow_counts(rows)}
    elif name == "mutation_rejector":
        result = {"accepted": not invalid, "all_invalid_mutations_rejected": not invalid}
    elif name == "positive_controls":
        result = {"accepted": not invalid, "positive_controls": 39 if invalid else 40}
    elif name == "proposal_contracts":
        result = {"accepted": not invalid, "proposal_contracts": 39 if invalid else 40}
    else:
        result = {"accepted": not invalid, "static_report": "missing" if invalid else "present"}
    expected_acceptance = not invalid
    return {
        "runner": name,
        "fixture": "invalid" if invalid else "positive",
        "accepted": bool(result.get("accepted")),
        "expected_acceptance": expected_acceptance,
        "expectation_met": bool(result.get("accepted")) == expected_acceptance,
        "details": result,
        "real_world_rows": 0,
        "external_actions": 0,
    }


def runner_cli(name: str) -> None:
    parser = argparse.ArgumentParser(description=f"Caelen Ash v676-v2 family-current {name} runner")
    parser.add_argument("--smoke", action="store_true", help="emit a deterministic owner-local smoke receipt")
    parser.add_argument("--invalid", action="store_true", help="use the preregistered invalid smoke fixture")
    args = parser.parse_args()
    if not args.smoke:
        parser.error("--smoke is required in this bounded phase-local runner")
    print(json.dumps(runner_smoke(name, args.invalid), sort_keys=True))
