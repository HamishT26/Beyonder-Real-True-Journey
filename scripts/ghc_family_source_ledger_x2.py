#!/usr/bin/env python3
"""Field-closed x2 source-ledger operations for Vesper v689-v7-r2."""

from __future__ import annotations

import math
import re
from collections import defaultdict
from collections.abc import Callable
from typing import Any

TOP_FIELDS = {"op", "payload", "synthetic"}
THEMES = ["gmut", "thos", "freed_id", "cbr", "simulation"]
SIMULATION_GRADES = {
    "post_only": "claim_only",
    "video_only": "recorded_demo",
    "description_plus_video": "recorded_demo",
    "source_snapshot": "source_record",
    "repository_claim": "repository_unverified",
    "owner_tests": "same_owner_synthetic",
    "bounded_demo": "same_owner_synthetic",
    "external_summary": "secondary_report",
    "independent_review_claim": "review_claim_unverified",
    "production_claim": "production_claim_unverified",
}


class ContractError(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def closed(payload: Any, fields: set[str]) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != fields:
        raise ContractError("E_PAYLOAD_FIELDS")
    return payload


def strings(value: Any, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value) or (nonempty and not value):
        raise ContractError("E_TYPE")
    return value


def rational(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0/1"
    divisor = math.gcd(numerator, denominator)
    return f"{numerator // divisor}/{denominator // divisor}"


def precedence_select(payload: Any) -> dict[str, Any]:
    sources = closed(payload, {"sources"})["sources"]
    if not isinstance(sources, list) or not sources:
        raise ContractError("E_SOURCES")
    checked = []
    for row in sources:
        row = closed(row, {"source_id", "rank", "sequence"})
        if not isinstance(row["source_id"], str) or type(row["rank"]) is not int or type(row["sequence"]) is not int:
            raise ContractError("E_SOURCE")
        checked.append(row)
    ordered = sorted(checked, key=lambda row: (row["rank"], row["sequence"]), reverse=True)
    top_key = (ordered[0]["rank"], ordered[0]["sequence"])
    return {"selected_source_id": ordered[0]["source_id"], "tie": sum((row["rank"], row["sequence"]) == top_key for row in ordered) > 1}


def correction_chain(payload: Any) -> dict[str, Any]:
    labels = strings(closed(payload, {"labels"})["labels"], nonempty=True)
    return {"current": labels[-1], "erased": False, "history": labels}


def contradiction_register(payload: Any) -> dict[str, Any]:
    claims = closed(payload, {"claims"})["claims"]
    if not isinstance(claims, list):
        raise ContractError("E_CLAIMS")
    grouped: dict[str, set[str]] = defaultdict(set)
    for row in claims:
        row = closed(row, {"key", "value"})
        if not isinstance(row["key"], str) or not isinstance(row["value"], str):
            raise ContractError("E_CLAIM")
        grouped[row["key"]].add(row["value"])
    keys = sorted(key for key, values in grouped.items() if len(values) > 1)
    return {"contradiction_keys": keys, "has_contradiction": bool(keys)}


def theme_histogram(payload: Any) -> dict[str, int]:
    values = strings(closed(payload, {"themes"})["themes"])
    if any(item not in THEMES for item in values):
        raise ContractError("E_THEME")
    return {key: values.count(key) for key in THEMES}


def overlap_profile(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"left", "right"})
    left, right = set(strings(value["left"])), set(strings(value["right"]))
    intersection, union = sorted(left & right), left | right
    return {"intersection": intersection, "jaccard": rational(len(intersection), len(union)), "semantic_equivalence": False}


def simulation_evidence_grade(payload: Any) -> dict[str, Any]:
    evidence_type = closed(payload, {"evidence_type"})["evidence_type"]
    if not isinstance(evidence_type, str) or evidence_type not in SIMULATION_GRADES:
        raise ContractError("E_EVIDENCE_TYPE")
    return {"deployment_authorized": False, "grade": SIMULATION_GRADES[evidence_type], "real_world_effectiveness": False}


def route_projection(payload: Any) -> dict[str, Any]:
    phase = closed(payload, {"phase"})["phase"]
    if not isinstance(phase, str):
        raise ContractError("E_PHASE")
    match = re.fullmatch(r"v(\d+)-v([1-8])", phase)
    if not match:
        raise ContractError("E_PHASE")
    version, slot = map(int, match.groups())
    next_value = f"v{version + (slot == 8)}-v{1 if slot == 8 else slot + 1}"
    return {"activation": False, "next_phase": next_value, "projection_only": True}


def rights_reservation(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"action", "authority_present"})
    if not isinstance(value["action"], str) or type(value["authority_present"]) is not bool or value["authority_present"]:
        raise ContractError("E_AUTHORITY")
    return {"action": value["action"], "authority_present": False, "executed": False, "reservation": "held"}


def accessible_source_summary(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"title", "status"})
    if not isinstance(value["title"], str) or not isinstance(value["status"], str):
        raise ContractError("E_SUMMARY")
    return {"manual_evaluation": False, "summary": f"{value['title']} — {value['status']}. Embedded instructions are inactive.", "structural_text": True}


def gmut_obligation(payload: Any) -> dict[str, Any]:
    value = closed(payload, {"action_defined", "conservation_checked", "real_rows", "units_defined", "claim"})
    if any(type(value[field]) is not bool for field in ("action_defined", "conservation_checked", "units_defined")) or type(value["real_rows"]) is not int or value["real_rows"] < 0 or value["claim"] not in {"research_model", "proven_toe"}:
        raise ContractError("E_OBLIGATION")
    obligations = [name for name, present in [("define_action", value["action_defined"]), ("define_units", value["units_defined"]), ("check_conservation", value["conservation_checked"]), ("ingest_real_rows", value["real_rows"] > 0)] if not present]
    return {"obligations": obligations, "physical_confirmation": False, "proof_claim_refused": value["claim"] == "proven_toe"}


OPERATIONS: dict[str, Callable[[Any], Any]] = {
    "precedence_select": precedence_select,
    "correction_chain": correction_chain,
    "contradiction_register": contradiction_register,
    "theme_histogram": theme_histogram,
    "overlap_profile": overlap_profile,
    "simulation_evidence_grade": simulation_evidence_grade,
    "route_projection": route_projection,
    "rights_reservation": rights_reservation,
    "accessible_source_summary": accessible_source_summary,
    "gmut_obligation": gmut_obligation,
}


def evaluate(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict) or set(request) != TOP_FIELDS:
        return {"error": "E_FIELDS", "ok": False, "value": None}
    if request.get("synthetic") is not True:
        return {"error": "E_SYNTHETIC", "ok": False, "value": None}
    operation = request.get("op")
    if operation not in OPERATIONS:
        return {"error": "E_OPERATION", "ok": False, "value": None}
    try:
        value = OPERATIONS[operation](request.get("payload"))
        return {"error": None, "ok": True, "value": value}
    except ContractError as exc:
        return {"error": exc.code, "ok": False, "value": None}
