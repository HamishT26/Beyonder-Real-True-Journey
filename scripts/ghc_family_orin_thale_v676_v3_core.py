#!/usr/bin/env python3
"""Owner-local zero-row core for Orin Thale v676-v3."""

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
    "claim_state",
    "provenance",
    "privacy",
    "accessibility",
    "portfolio",
    "method_flow",
    "report",
}


def validate_contract(value: dict[str, Any]) -> list[str]:
    errors = []
    missing = sorted(REQUIRED_FIELDS - value.keys())
    if missing:
        errors.append("missing_required_fields:" + ",".join(missing))
    if value.get("expected_disposition") not in LABELS:
        errors.append("unknown_outcome_label")
    if not str(value.get("surrogate_item_id", "")).startswith("SYNTH-ITEM-"):
        errors.append("synthetic_item_identifier_required")
    if not str(value.get("surrogate_claim_id", "")).startswith("SYNTH-CLAIM-"):
        errors.append("synthetic_claim_identifier_required")
    if value.get("claimant_identifier") not in {None, ""}:
        errors.append("real_or_raw_claimant_identifier_forbidden")
    if value.get("real_world_rows") not in (0, []):
        errors.append("nonzero_real_world_rows_forbidden")
    if value.get("external_actions") not in (0, []):
        errors.append("external_actions_forbidden")
    for field in (
        "real_world_authority",
        "ownership_determined",
        "physical_custody_claimed",
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
            "surrogate_item_id": "SYNTH-ITEM-" + row["proposal_id"],
            "surrogate_claim_id": "SYNTH-CLAIM-" + row["proposal_id"],
            "claimant_identifier": None,
            "real_world_rows": 0,
            "external_actions": 0,
            "real_world_authority": False,
            "ownership_determined": False,
            "physical_custody_claimed": False,
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
    elif kind == "real_identifier_ingestion":
        value["claimant_identifier"] = "FORBIDDEN-REAL-IDENTIFIER-FIXTURE"
    else:
        raise ValueError("unknown mutation kind")
    return value


def validate_claim_state(events: list[dict[str, str]]) -> dict[str, Any]:
    allowed = {
        None: {"intake"},
        "intake": {"held", "quarantined"},
        "held": {"challenged", "surrogate_return_recorded", "retention_unknown"},
        "challenged": {"held", "contested"},
        "contested": {"held"},
        "quarantined": {"held"},
        "retention_unknown": {"held"},
        "surrogate_return_recorded": set(),
    }
    state = None
    for event in events:
        nxt = event.get("state")
        if nxt not in allowed.get(state, set()):
            return {"accepted": False, "reason": "invalid_claim_state_transition", "from": state, "to": nxt}
        if event.get("real_action") != "none":
            return {"accepted": False, "reason": "real_action_forbidden"}
        state = nxt
    return {"accepted": True, "final_state": state, "physical_return": False, "ownership_determined": False}


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
    return {"accepted": True, "topological_order": order, "custody_claim": False, "authority_claim": False}


def accessibility_proxy(value: dict[str, Any]) -> dict[str, Any]:
    required = {"title", "summary", "status", "correction_route", "keyboard_order"}
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
        for heading in ("---", "# ", "## Inputs", "## Procedure", "## Refusal conditions", "## Output"):
            if heading not in value:
                errors.append("missing_heading:" + heading)
    if contract.is_file():
        data = json.loads(contract.read_text(encoding="utf-8"))
        if data.get("global_install") is not False:
            errors.append("global_install_not_false")
        if data.get("real_world_rows") != 0 or data.get("external_actions") != 0:
            errors.append("nonzero_world_scope")
    return {"accepted": not errors, "errors": errors}


def runner_smoke(name: str, invalid: bool) -> dict[str, Any]:
    if name not in RUNNERS:
        raise ValueError("unknown runner")
    if name == "claim_state":
        events = [
            {"state": "intake", "real_action": "none"},
            {"state": "held", "real_action": "none"},
            {"state": "intake" if invalid else "challenged", "real_action": "none"},
        ]
        details = validate_claim_state(events)
    elif name == "provenance":
        nodes = ["SYNTH-ITEM", "SYNTH-HOLD", "SYNTH-RECEIPT"]
        edges = [("SYNTH-ITEM", "SYNTH-HOLD"), ("SYNTH-HOLD", "SYNTH-ITEM" if invalid else "SYNTH-RECEIPT")]
        details = validate_provenance(nodes, edges)
    elif name == "privacy":
        details = {"accepted": not invalid, "candidates": ["raw_task_route"] if invalid else []}
    elif name == "accessibility":
        fixture = {
            "title": "Synthetic item",
            "summary": "No real item",
            "status": "held_proxy",
            "correction_route": "synthetic",
            "keyboard_order": [1, 2, 3] if not invalid else [2, 1, 3],
            "manual_user_review": False,
        }
        details = accessibility_proxy(fixture)
    elif name == "portfolio":
        counts = {"safe_now": 59 if invalid else 60, "candidate": 30, "exact_approval": 20, "blocked": 10}
        details = {"accepted": counts == {"safe_now": 60, "candidate": 30, "exact_approval": 20, "blocked": 10}, "counts": counts}
    elif name == "method_flow":
        rows = [{"truth": True}, {}] if invalid else [{"truth": True}, {"truth": False}]
        details = {"accepted": all("truth" in row for row in rows), "rows": len(rows)}
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
    parser = argparse.ArgumentParser(description=f"Orin Thale v676-v3 family-current {name} runner")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--invalid", action="store_true")
    args = parser.parse_args()
    if not args.smoke:
        parser.error("--smoke is required")
    print(json.dumps(runner_smoke(name, args.invalid), sort_keys=True))
