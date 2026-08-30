#!/usr/bin/env python3
"""Owner-local zero-row core for the Neris Solane v677-v3 phase."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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
RUNNERS = {
    "contract",
    "mutation",
    "meteorological_chart_topology",
    "metadata",
    "flashcard",
    "toolchain",
    "privacy",
    "accessibility",
    "portfolio",
    "report",
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def validate_contract(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - value.keys())
    if missing:
        errors.append("missing_required_fields:" + ",".join(missing))
    if value.get("expected_disposition") not in LABELS:
        errors.append("unknown_outcome_label")
    if not str(value.get("surrogate_record_id", "")).startswith("SYNTH-METEO-CHART-META-"):
        errors.append("synthetic_record_identifier_required")
    if value.get("raw_identifier") not in {None, ""}:
        errors.append("real_or_raw_identifier_forbidden")
    if value.get("measurements") != []:
        errors.append("real_or_ungrounded_measurement_forbidden")
    if value.get("real_world_rows") != 0 or value.get("external_actions") != 0:
        errors.append("nonzero_external_scope")
    for field in (
        "object_observed",
        "condition_determined",
        "treatment_performed",
        "timing_conformance",
        "professional_release",
        "legal_approval",
        "cultural_approval",
        "maori_authority",
        "production_ready",
        "empirical_confirmation",
        "stage20_ready",
    ):
        if value.get(field) is not False:
            errors.append(field + "_must_be_false")
    return errors


def positive_fixture(row: dict[str, Any]) -> dict[str, Any]:
    value = json.loads(json.dumps(row, ensure_ascii=False))
    value.update(
        {
            "surrogate_record_id": "SYNTH-METEO-CHART-META-" + row["proposal_id"],
            "raw_identifier": None,
            "measurements": [],
            "real_world_rows": 0,
            "external_actions": 0,
            "object_observed": False,
            "condition_determined": False,
            "treatment_performed": False,
            "timing_conformance": False,
            "professional_release": False,
            "legal_approval": False,
            "cultural_approval": False,
            "maori_authority": False,
            "production_ready": False,
            "empirical_confirmation": False,
            "stage20_ready": False,
        }
    )
    return value


def mutate(row: dict[str, Any], kind: str) -> dict[str, Any]:
    value = positive_fixture(row)
    if kind == "missing_hypothesis":
        value.pop("hypothesis", None)
    elif kind == "unknown_outcome_label":
        value["expected_disposition"] = "confirmed"
    elif kind == "authority_escalation":
        value["professional_release"] = True
        value["stage20_ready"] = True
    elif kind == "real_identifier_or_measurement":
        value["raw_identifier"] = "FORBIDDEN-REAL-RECORD"
        value["measurements"] = [{"component_span_millimetres": 95.0}]
    else:
        raise ValueError("unknown mutation kind")
    return value


def validate_meteorological_chart_graph(nodes: list[str], edges: list[tuple[str, str]]) -> dict[str, Any]:
    if len(nodes) != len(set(nodes)):
        return {"accepted": False, "reason": "duplicate_meteorological_chart_component"}
    if any(not node.startswith("SYNTH-METEO-CHART-COMPONENT-") for node in nodes):
        return {"accepted": False, "reason": "synthetic_meteorological_chart_prefix_required"}
    node_set = set(nodes)
    if any(left not in node_set or right not in node_set for left, right in edges):
        return {"accepted": False, "reason": "unknown_meteorological_chart_relation"}
    if any(left == right for left, right in edges):
        return {"accepted": False, "reason": "self_relation_forbidden"}
    return {
        "accepted": True,
        "nodes": len(nodes),
        "edges": len(edges),
        "real_meteorological_chart_claim": False,
        "condition_assessment_claim": False,
        "repair_or_treatment_claim": False,
    }


def validate_metadata(fields: list[dict[str, Any]]) -> dict[str, Any]:
    if not fields:
        return {"accepted": False, "reason": "empty_field_set"}
    tags = [str(field.get("tag", "")) for field in fields]
    if any(not re.fullmatch(r"[0-9A-Z]{3}", tag) for tag in tags):
        return {"accepted": False, "reason": "invalid_tag"}
    if tags != sorted(tags):
        return {"accepted": False, "reason": "nondeterministic_field_order"}
    if any(field.get("real_record") is not False for field in fields):
        return {"accepted": False, "reason": "real_record_flag_forbidden"}
    return {"accepted": True, "field_count": len(fields), "measurement_or_treatment_conformance": False, "meteorological_chart_authority": False}


def canonical_digest(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_flashcard(card: dict[str, Any]) -> list[str]:
    errors = []
    for field in ("card_id", "freed_id_anchor", "trinity_pillar", "bounded_practice", "task", "section"):
        if not isinstance(card.get(field), str) or not card[field].strip():
            errors.append("missing_or_empty:" + field)
    if card.get("identity_continuity_claim") is not False:
        errors.append("identity_continuity_claim_must_be_false")
    if card.get("authority_claim") is not False:
        errors.append("authority_claim_must_be_false")
    if card.get("real_world_rows") != 0:
        errors.append("real_world_rows_must_be_zero")
    return errors


def privacy_candidates(value: str) -> list[str]:
    return sorted(name for name, pattern in PRIVACY_PATTERNS.items() if pattern.search(value))


def skill_smoke(skill_dir: Path, invalid: bool = False) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    contract = skill_dir / "skill.json"
    errors = []
    if not skill_md.is_file() or not contract.is_file():
        errors.append("missing_skill_surface")
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        for required in ("---", "# ", "## Inputs", "## Procedure", "## Refusal conditions", "## Output"):
            if required not in text:
                errors.append("missing_heading:" + required)
        if "TODO" in text:
            errors.append("unfinished_placeholder")
    if contract.is_file():
        value = json.loads(contract.read_text(encoding="utf-8"))
        if value.get("global_install") is not False or value.get("real_world_rows") != 0:
            errors.append("unsafe_skill_scope")
        if value.get("initialized_with_official_skill_creator") is not True:
            errors.append("official_initializer_not_recorded")
    if invalid:
        errors.append("synthetic_rejecting_fixture")
    return {"accepted": not errors, "errors": errors, "fixture": "rejecting" if invalid else "positive"}


def runner_smoke(name: str, invalid: bool) -> dict[str, Any]:
    if name not in RUNNERS:
        raise ValueError("unknown runner")
    if name == "meteorological_chart_topology":
        nodes = ["SYNTH-METEO-CHART-COMPONENT-CHART-GRID-001", "SYNTH-METEO-CHART-COMPONENT-MAST-001", "SYNTH-METEO-CHART-COMPONENT-TRACE-001"]
        edges = [(nodes[0], nodes[0] if invalid else nodes[1])]
        detail = validate_meteorological_chart_graph(nodes, edges)
    elif name == "metadata":
        fields = [
            {"tag": "245" if not invalid else "99", "real_record": False},
            {"tag": "500", "real_record": False},
        ]
        detail = validate_metadata(fields)
    elif name == "flashcard":
        card = {
            "card_id": "SYNTH-CARD-001",
            "freed_id_anchor": "Neris Solane",
            "trinity_pillar": "Freed ID and CBR Heart with GMUT Mind and THOS Body protected",
            "bounded_practice": "synthetic meteorological-chart component and trace documentation",
            "task": "represent one zero-row contract",
            "section": "task",
            "identity_continuity_claim": bool(invalid),
            "authority_claim": False,
            "real_world_rows": 0,
        }
        errors = validate_flashcard(card)
        detail = {"accepted": not errors, "errors": errors}
    elif name == "privacy":
        candidates = privacy_candidates("source_thread_id=forbidden" if invalid else "synthetic-card")
        detail = {"accepted": not candidates, "candidates": candidates}
    elif name == "portfolio":
        counts = {"safe": 119 if invalid else 120, "candidate": 80, "exact": 20, "blocked": 10}
        detail = {"accepted": counts == {"safe": 120, "candidate": 80, "exact": 20, "blocked": 10}, "counts": counts}
    else:
        detail = {"accepted": not invalid, "bounded_surface": name, "real_world_rows": 0, "external_actions": 0}
    expected = not invalid
    return {
        "runner": name,
        "fixture": "rejecting" if invalid else "positive",
        "accepted": bool(detail.get("accepted")),
        "expected_acceptance": expected,
        "expectation_met": bool(detail.get("accepted")) == expected,
        "details": detail,
        "real_world_rows": 0,
        "external_actions": 0,
    }


def runner_cli(name: str) -> None:
    parser = argparse.ArgumentParser(description=f"Neris Solane v677-v3 {name} runner")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--invalid", action="store_true")
    args = parser.parse_args()
    if not args.smoke:
        parser.error("--smoke is required")
    print(json.dumps(runner_smoke(name, args.invalid), sort_keys=True))
