"""Bounded synthetic contract guards for Liora Venn v672-v6.

The module validates owner-local JSON fixtures only.  It performs no network,
filesystem, account, credential, material, professional, or authority action.
"""

from __future__ import annotations

import argparse
import copy
import json
from typing import Any


TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
MODES = (
    "bath_topology",
    "drop_order",
    "rake_path",
    "transfer_state",
    "lineage",
    "accessibility",
    "workload",
    "privacy",
    "mutation",
    "boundary",
)


def _walk(node: Any):
    if isinstance(node, dict):
        for key, value in node.items():
            yield key, value
            yield from _walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk(value)


def _common_errors(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    errors = []
    if not isinstance(payload.get("contract_id"), str) or not payload["contract_id"].startswith("LV6726-"):
        errors.append("missing_or_invalid_contract_id")
    if payload.get("synthetic_only") is not True:
        errors.append("synthetic_only_required")
    for flag in ("external_action", "empirical_claim", "authority_claim", "stage20_promotion", "private_identifier_present"):
        if payload.get(flag) is not False:
            errors.append(f"{flag}_refused")
    if payload.get("terminal_verdict") != TERMINAL_VERDICT:
        errors.append("terminal_verdict_mismatch")
    forbidden_keys = {
        "email", "address", "phone", "password", "secret", "token", "credential", "account",
        "thread_id", "task_id", "session_id", "private_route", "free_text", "person_name",
    }
    for key, value in _walk(payload):
        if key.lower() in forbidden_keys and value not in (None, "", False, [], {}):
            errors.append(f"private_or_raw_field_refused:{key.lower()}")
    return errors


def evaluate(mode: str, payload: Any) -> dict[str, Any]:
    if mode not in MODES:
        return {"mode": mode, "valid": False, "errors": ["unknown_mode"], "boundary": "synthetic owner-local guard only"}
    errors = _common_errors(payload)
    if not isinstance(payload, dict):
        return {"mode": mode, "valid": False, "errors": errors, "boundary": "synthetic owner-local guard only"}

    if mode == "bath_topology":
        nodes = payload.get("nodes", [])
        edges = payload.get("edges", [])
        node_ids = [row.get("node_id") for row in nodes if isinstance(row, dict)]
        if not nodes or len(node_ids) != len(nodes) or len(node_ids) != len(set(node_ids)):
            errors.append("bath_nodes_missing_or_duplicate")
        allowed = set(node_ids)
        if any(not isinstance(edge, list) or len(edge) != 2 or edge[0] not in allowed or edge[1] not in allowed or edge[0] == edge[1] for edge in edges):
            errors.append("bath_edge_invalid")
    elif mode == "drop_order":
        drops = payload.get("drops", [])
        sequences = [row.get("sequence") for row in drops if isinstance(row, dict)]
        if not drops or sequences != list(range(1, len(drops) + 1)):
            errors.append("drop_sequence_invalid")
        if len({row.get("drop_id") for row in drops if isinstance(row, dict)}) != len(drops):
            errors.append("drop_identifier_duplicate")
    elif mode == "rake_path":
        segments = payload.get("segments", [])
        if not segments:
            errors.append("rake_segments_missing")
        for segment in segments:
            coordinates = segment.get("from", []) + segment.get("to", []) if isinstance(segment, dict) else []
            if len(coordinates) != 4 or any(not isinstance(value, (int, float)) or value < 0 or value > 1 for value in coordinates):
                errors.append("rake_coordinate_out_of_bounds")
                break
    elif mode == "transfer_state":
        if payload.get("events") != ["prepared", "contacted", "lifted"]:
            errors.append("transfer_state_sequence_invalid")
    elif mode == "lineage":
        records = payload.get("records", [])
        identifiers = {row.get("record_id") for row in records if isinstance(row, dict)}
        if not records or None in identifiers or len(identifiers) != len(records):
            errors.append("lineage_record_invalid")
        for record in records:
            previous = record.get("supersedes")
            if previous is not None and (previous not in identifiers or previous == record.get("record_id")):
                errors.append("lineage_supersession_invalid")
                break
        if payload.get("prior_records_retained") is not True:
            errors.append("prior_records_not_retained")
    elif mode == "accessibility":
        if payload.get("heading_order") != ["h1", "h2", "h2"]:
            errors.append("heading_order_invalid")
        if payload.get("noncolour_status") is not True or not payload.get("alternate_description"):
            errors.append("static_accessibility_structure_invalid")
        if payload.get("manual_evaluation_complete") is not False or payload.get("affected_user_acceptance") is not False:
            errors.append("human_evaluation_promotion_refused")
    elif mode == "workload":
        capacity = payload.get("capacity")
        queue = payload.get("queue", [])
        if not isinstance(capacity, int) or capacity < 1 or len(queue) > capacity:
            errors.append("workload_capacity_exceeded")
        if payload.get("stop_precedence") is not True or payload.get("pause_supported") is not True:
            errors.append("workload_stop_or_pause_missing")
    elif mode == "privacy":
        allowed = {"contract_id", "synthetic_only", "external_action", "empirical_claim", "authority_claim", "stage20_promotion", "private_identifier_present", "terminal_verdict", "surrogate_id", "status"}
        extras = sorted(set(payload) - allowed)
        if extras:
            errors.append("privacy_field_not_allowlisted:" + ",".join(extras))
        if not str(payload.get("surrogate_id", "")).startswith("SYN-"):
            errors.append("surrogate_identifier_required")
    elif mode == "mutation":
        failed = payload.get("failed_witness_ids", [])
        passing = payload.get("passing_witness_ids", [])
        if not failed or not passing or set(failed) & set(passing):
            errors.append("mutation_witness_partition_invalid")
        if payload.get("failed_witnesses_retained") is not True or payload.get("failed_promoted_to_pass") is not False:
            errors.append("failed_witness_non_erasure_required")
    elif mode == "boundary":
        required_false = (
            "real_people", "real_materials", "real_measurements", "professional_authority", "legal_authority",
            "cultural_authority", "maori_authority", "independent_reproduction", "full_suite_claim",
        )
        if any(payload.get(flag) is not False for flag in required_false):
            errors.append("protected_boundary_promotion_refused")
        if payload.get("allowed_outcomes") != ["completed", "represented", "open_gap", "exact_gate"]:
            errors.append("outcome_vocabulary_invalid")

    return {
        "mode": mode,
        "valid": not errors,
        "errors": sorted(set(errors)),
        "boundary": "Bounded synthetic owner-local contract evidence only; no observation, competence, authority, production, proof, canon, or Stage 20 claim.",
    }


def accepting_fixture(mode: str) -> dict[str, Any]:
    base: dict[str, Any] = {
        "contract_id": f"LV6726-{mode.upper().replace('_', '-')}-ACCEPT",
        "synthetic_only": True,
        "external_action": False,
        "empirical_claim": False,
        "authority_claim": False,
        "stage20_promotion": False,
        "private_identifier_present": False,
        "terminal_verdict": TERMINAL_VERDICT,
    }
    mode_fields: dict[str, dict[str, Any]] = {
        "bath_topology": {"nodes": [{"node_id": "bath"}, {"node_id": "surface"}, {"node_id": "sheet"}], "edges": [["bath", "surface"], ["surface", "sheet"]]},
        "drop_order": {"drops": [{"drop_id": "drop-a", "sequence": 1}, {"drop_id": "drop-b", "sequence": 2}]},
        "rake_path": {"segments": [{"from": [0.1, 0.2], "to": [0.8, 0.2]}, {"from": [0.8, 0.2], "to": [0.8, 0.7]}]},
        "transfer_state": {"events": ["prepared", "contacted", "lifted"]},
        "lineage": {"records": [{"record_id": "swatch-r1", "supersedes": None}, {"record_id": "swatch-r2", "supersedes": "swatch-r1"}], "prior_records_retained": True},
        "accessibility": {"heading_order": ["h1", "h2", "h2"], "noncolour_status": True, "alternate_description": "Synthetic arcs move from upper left toward a central axis.", "manual_evaluation_complete": False, "affected_user_acceptance": False},
        "workload": {"capacity": 3, "queue": ["bath-a", "rack-a"], "stop_precedence": True, "pause_supported": True},
        "privacy": {"surrogate_id": "SYN-SWATCH-001", "status": "synthetic_fixture"},
        "mutation": {"failed_witness_ids": ["LV6726-MUT-FAIL-001"], "passing_witness_ids": ["LV6726-MUT-PASS-001"], "failed_witnesses_retained": True, "failed_promoted_to_pass": False},
        "boundary": {"real_people": False, "real_materials": False, "real_measurements": False, "professional_authority": False, "legal_authority": False, "cultural_authority": False, "maori_authority": False, "independent_reproduction": False, "full_suite_claim": False, "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"]},
    }
    base.update(copy.deepcopy(mode_fields[mode]))
    return base


def mutate_fixture(mode: str, mutation_class: str) -> dict[str, Any]:
    payload = accepting_fixture(mode)
    if mutation_class == "missing_or_wrong_typed_required_field":
        payload.pop("contract_id", None)
    elif mutation_class == "marbling_sequence_lineage_or_boundary_violation":
        if mode == "bath_topology":
            payload["nodes"].append({"node_id": "bath"})
        elif mode == "drop_order":
            payload["drops"][1]["sequence"] = 1
        elif mode == "rake_path":
            payload["segments"][0]["to"][0] = 2.0
        elif mode == "transfer_state":
            payload["events"] = ["prepared", "contacted", "contacted", "lifted"]
        elif mode == "lineage":
            payload["records"][1]["supersedes"] = "swatch-r2"
        elif mode == "accessibility":
            payload["heading_order"] = ["h2", "h1"]
        elif mode == "workload":
            payload["queue"] = ["a", "b", "c", "d"]
        elif mode == "privacy":
            payload["free_text"] = "synthetic but unallowlisted"
        elif mode == "mutation":
            payload["failed_witnesses_retained"] = False
        elif mode == "boundary":
            payload["professional_authority"] = True
    elif mutation_class == "privacy_identity_authority_or_cultural_smuggling":
        payload["private_identifier_present"] = True
        payload["authority_claim"] = True
    elif mutation_class == "external_action_empirical_or_stage20_promotion":
        payload["external_action"] = True
        payload["empirical_claim"] = True
        payload["stage20_promotion"] = True
    else:
        raise ValueError(f"unknown mutation class: {mutation_class}")
    return payload


def rejecting_fixture(mode: str) -> dict[str, Any]:
    return mutate_fixture(mode, "marbling_sequence_lineage_or_boundary_violation")


def cli(mode: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("accept", "reject"), required=True)
    args = parser.parse_args()
    payload = accepting_fixture(mode) if args.case == "accept" else rejecting_fixture(mode)
    result = evaluate(mode, payload)
    expected = result["valid"] if args.case == "accept" else not result["valid"]
    print(json.dumps({"mode": mode, "case": args.case, "expected_behavior_observed": expected, "result": result}, indent=2, sort_keys=True))
    return 0 if expected else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=MODES)
    parser.add_argument("--case", choices=("accept", "reject"), required=True)
    args = parser.parse_args()
    payload = accepting_fixture(args.mode) if args.case == "accept" else rejecting_fixture(args.mode)
    result = evaluate(args.mode, payload)
    expected = result["valid"] if args.case == "accept" else not result["valid"]
    print(json.dumps({"mode": args.mode, "case": args.case, "expected_behavior_observed": expected, "result": result}, indent=2, sort_keys=True))
    raise SystemExit(0 if expected else 1)
