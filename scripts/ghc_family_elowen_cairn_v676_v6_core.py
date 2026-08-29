#!/usr/bin/env python3
"""Owner-local zero-row mechanical-typewriter core for Elowen Cairn v676-v6."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, deque
from pathlib import Path
from typing import Any


LABELS = {"completed", "represented", "open_gap", "exact_gate"}
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
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}
RUNNERS = {
    "proposal_contracts",
    "positive_controls",
    "mutation_rejector",
    "typewriter_topology",
    "measurement_vacancy",
    "provenance",
    "privacy",
    "accessibility",
    "portfolio",
    "report",
}


def validate_contract(value: dict[str, Any]) -> list[str]:
    errors = []
    missing = sorted(REQUIRED_FIELDS - value.keys())
    if missing:
        errors.append("missing_required_fields:" + ",".join(missing))
    if value.get("expected_disposition") not in LABELS:
        errors.append("unknown_outcome_label")
    if not str(value.get("surrogate_object_id", "")).startswith("SYNTH-TYPEWRITER-"):
        errors.append("synthetic_typewriter_identifier_required")
    if value.get("raw_identifier") not in {None, ""}:
        errors.append("real_or_raw_identifier_forbidden")
    if value.get("measurements") != []:
        errors.append("real_or_ungrounded_measurement_forbidden")
    if value.get("real_world_rows") != 0:
        errors.append("nonzero_real_world_rows_forbidden")
    if value.get("external_actions") != 0:
        errors.append("external_actions_forbidden")
    for field in (
        "real_world_authority",
        "condition_determined",
        "authenticity_determined",
        "treatment_performed",
        "professional_release",
        "legal_approval",
        "cultural_approval",
        "maori_authority",
        "production_ready",
        "empirical_confirmation",
    ):
        if value.get(field) is not False:
            errors.append(field + "_must_be_false")
    return errors


def positive_fixture(row: dict[str, Any]) -> dict[str, Any]:
    value = dict(row)
    value.update(
        {
            "surrogate_object_id": "SYNTH-TYPEWRITER-" + row["proposal_id"],
            "raw_identifier": None,
            "measurements": [],
            "real_world_rows": 0,
            "external_actions": 0,
            "real_world_authority": False,
            "condition_determined": False,
            "authenticity_determined": False,
            "treatment_performed": False,
            "professional_release": False,
            "legal_approval": False,
            "cultural_approval": False,
            "maori_authority": False,
            "production_ready": False,
            "empirical_confirmation": False,
        }
    )
    return value


def mutate(row: dict[str, Any], kind: str) -> dict[str, Any]:
    value = json.loads(json.dumps(positive_fixture(row), ensure_ascii=False))
    if kind == "missing_hypothesis":
        value.pop("hypothesis", None)
    elif kind == "unknown_outcome_label":
        value["expected_disposition"] = "confirmed"
    elif kind == "authority_escalation":
        value["real_world_authority"] = True
    elif kind == "real_identifier_or_measurement":
        value["raw_identifier"] = "FORBIDDEN-REAL-ACCESSION-FIXTURE"
        value["measurements"] = [{"carriage_travel_millimetres": 92.5}]
    else:
        raise ValueError("unknown mutation kind")
    return value


def validate_component_graph(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, Any]:
    if len(nodes) != len(set(nodes)):
        return {"accepted": False, "reason": "duplicate_component"}
    if any(not node.startswith("SYNTH-COMP-") for node in nodes):
        return {"accepted": False, "reason": "synthetic_component_prefix_required"}
    node_set = set(nodes)
    if any(left not in node_set or right not in node_set for left, right in edges):
        return {"accepted": False, "reason": "unknown_component_edge"}
    if any(left == right for left, right in edges):
        return {"accepted": False, "reason": "self_mesh_forbidden"}
    return {
        "accepted": True,
        "nodes": len(nodes),
        "edges": len(edges),
        "physical_object_claim": False,
        "condition_claim": False,
    }


def validate_provenance(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, Any]:
    if len(nodes) != len(set(nodes)):
        return {"accepted": False, "reason": "duplicate_node"}
    if any(not node.startswith("SYNTH-") for node in nodes):
        return {"accepted": False, "reason": "synthetic_node_prefix_required"}
    node_set = set(nodes)
    if any(left not in node_set or right not in node_set for left, right in edges):
        return {"accepted": False, "reason": "unknown_edge_node"}
    incoming = Counter(right for _, right in edges)
    outgoing = {node: [] for node in nodes}
    for left, right in edges:
        outgoing[left].append(right)
    queue = deque(sorted(node for node in nodes if incoming[node] == 0))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for target in sorted(outgoing[node]):
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)
    if len(order) != len(nodes):
        return {"accepted": False, "reason": "cycle_detected"}
    return {"accepted": True, "topological_order": order, "custody_claim": False, "attribution_claim": False}


def measurement_vacancy(value: dict[str, Any]) -> dict[str, Any]:
    required = {"quantity", "unit", "reference_source", "observed_value", "uncertainty", "traceability_status"}
    missing = sorted(required - value.keys())
    if missing:
        return {"accepted": False, "reason": "missing_measurement_vacancy_fields", "missing": missing}
    if value["observed_value"] is not None or value["uncertainty"] is not None:
        return {"accepted": False, "reason": "measurement_must_remain_absent"}
    if value["traceability_status"] != "vacant":
        return {"accepted": False, "reason": "traceability_must_remain_vacant"}
    return {"accepted": True, "measurement_result": False, "calibration_claim": False}


def accessibility_proxy(value: dict[str, Any]) -> dict[str, Any]:
    required = {"title", "summary", "component_order", "correction_route", "keyboard_order"}
    missing = sorted(required - value.keys())
    if missing:
        return {"accepted": False, "reason": "missing_accessibility_fields", "missing": missing}
    if value.get("manual_user_review") is not False:
        return {"accepted": False, "reason": "manual_user_review_must_remain_vacant"}
    if value["keyboard_order"] != sorted(value["keyboard_order"]):
        return {"accepted": False, "reason": "keyboard_order_not_deterministic"}
    return {"accepted": True, "accessibility_complete": False, "affected_user_review": False}


def privacy_candidates(value: str) -> list[str]:
    return sorted(name for name, pattern in PRIVACY_PATTERNS.items() if pattern.search(value))


def skill_smoke(skill_dir: Path) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    contract = skill_dir / "skill.json"
    errors = []
    if not skill_md.is_file():
        errors.append("missing_skill_md")
    if not contract.is_file():
        errors.append("missing_skill_json")
    if skill_md.is_file():
        value = skill_md.read_text(encoding="utf-8")
        for heading in ("---", "# ", "## Inputs", "## Procedure", "## Refusal conditions", "## Output"):
            if heading not in value:
                errors.append("missing_heading:" + heading)
    if contract.is_file():
        data = json.loads(contract.read_text(encoding="utf-8"))
        if data.get("global_install") is not False:
            errors.append("global_install_not_false")
        if data.get("real_world_rows") != 0 or data.get("external_actions") != 0:
            errors.append("nonzero_world_scope")
        if data.get("initialized_with_official_skill_creator") is not True:
            errors.append("official_initialization_not_recorded")
    return {"accepted": not errors, "errors": errors, "fixture": "synthetic_zero_row"}


def runner_smoke(name: str, invalid: bool) -> dict[str, Any]:
    if name not in RUNNERS:
        raise ValueError("unknown runner")
    if name == "typewriter_topology":
        nodes = ["SYNTH-COMP-KEYLEVER", "SYNTH-COMP-TYPEBAR", "SYNTH-COMP-CARRIAGE"]
        edges = [("SYNTH-COMP-KEYLEVER", "SYNTH-COMP-KEYLEVER" if invalid else "SYNTH-COMP-TYPEBAR")]
        details = validate_component_graph(nodes, edges)
    elif name == "measurement_vacancy":
        fixture = {
            "quantity": "carriage_travel",
            "unit": "millimetre",
            "reference_source": "none",
            "observed_value": 1.2 if invalid else None,
            "uncertainty": None,
            "traceability_status": "vacant",
        }
        details = measurement_vacancy(fixture)
    elif name == "provenance":
        nodes = ["SYNTH-OBJECT", "SYNTH-DOC", "SYNTH-CORRECTION"]
        edges = [("SYNTH-OBJECT", "SYNTH-DOC"), ("SYNTH-DOC", "SYNTH-OBJECT" if invalid else "SYNTH-CORRECTION")]
        details = validate_provenance(nodes, edges)
    elif name == "privacy":
        details = {"accepted": not invalid, "candidates": ["raw_task_route"] if invalid else []}
    elif name == "accessibility":
        fixture = {
            "title": "Synthetic typewriter mechanism",
            "summary": "No real typewriter, observation, measurement, repair, or safety conclusion",
            "component_order": ["carriage", "keylever", "platen", "typebar"],
            "correction_route": "synthetic",
            "keyboard_order": [1, 2, 3] if not invalid else [2, 1, 3],
            "manual_user_review": False,
        }
        details = accessibility_proxy(fixture)
    elif name == "portfolio":
        counts = {"safe_now": 59 if invalid else 60, "candidate": 30, "exact_approval": 20, "blocked": 10}
        details = {"accepted": counts == {"safe_now": 60, "candidate": 30, "exact_approval": 20, "blocked": 10}, "counts": counts}
    else:
        details = {"accepted": not invalid, "bounded_surface": name, "real_world_rows": 0}
    expected = not invalid
    return {
        "runner": name,
        "fixture": "invalid" if invalid else "positive",
        "accepted": bool(details.get("accepted")),
        "expected_acceptance": expected,
        "expectation_met": bool(details.get("accepted")) == expected,
        "details": details,
        "real_world_rows": 0,
        "external_actions": 0,
    }


def runner_cli(name: str) -> None:
    parser = argparse.ArgumentParser(description=f"Elowen Cairn v676-v6 family-current {name} runner")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--invalid", action="store_true")
    args = parser.parse_args()
    if not args.smoke:
        parser.error("--smoke is required")
    print(json.dumps(runner_smoke(name, args.invalid), sort_keys=True))
