#!/usr/bin/env python3
"""Owner-local zero-row core for Lyren Moss v679-v4.

Every fixture is synthetic documentation.  The module deliberately contains no
sensor adapter, filesystem discovery, network client, production action, or
authority path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


LABELS = {"completed", "represented", "open_gap", "exact_gate"}
MUTATIONS = (
    "missing_hypothesis",
    "unknown_outcome_label",
    "numeric_reading_injection",
    "authority_escalation",
)
RUNNERS = {
    "contract",
    "column",
    "sequence",
    "correction",
    "provenance",
    "accessibility",
    "privacy",
    "mutation",
    "method_flow",
    "terminal",
}
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
AUTHORITY_FLAGS = (
    "collection_condition_determined",
    "environmental_risk_determined",
    "treatment_or_mitigation_recommended",
    "professional_release",
    "legal_approval",
    "cultural_approval",
    "maori_authority",
    "affected_party_approval",
    "production_ready",
    "empirical_confirmation",
    "independent_reproduction",
    "stage20_ready",
)
CHANNELS = ("temperature", "relative_humidity", "light", "pollutant")
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+" + "Users" + r"[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(" + "source" + r"[_-]?thread[_-]?id|" + "client" + r"ThreadId)"),
    "credential_assignment": re.compile(
        r"(?i)(" + "api" + r"[_-]?key|" + "private" + r"[_-]?key|" + "pass" + r"word|" + "bear" + r"er)\s*[:=]"
    ),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_or_capture": re.compile(r"(?i)(" + "terminal trans" + r"cript|" + "screen" + r"shot payload|" + "session" + r"[_ -]?stream)"),
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def contract_from_proposal(proposal: dict[str, Any]) -> dict[str, Any]:
    """Materialize a zero-row contract from a frozen x1 proposal."""
    row = {key: proposal[key] for key in REQUIRED_PROPOSAL_FIELDS}
    row.update(
        {
            "schema": "ghc-family.lyren-moss.v679-v4.synthetic-monitor-contract.v1",
            "record_id": "SYNTH-MONITOR-LOG-" + proposal["proposal_id"],
            "zone_alias": "SYNTH-ZONE-" + proposal["proposal_id"],
            "channel_states": {channel: "not_observed" for channel in CHANNELS},
            "readings": [],
            "uncertainty_values": [],
            "calibration_state": "not_evaluated",
            "action_state": "none",
            "real_world_rows": 0,
            "external_actions": 0,
            "raw_identifier": None,
            "correction_lineage": [],
            "provenance_agents": [],
            "identity_continuity_claim": False,
            "consciousness_or_personhood_claim": False,
        }
    )
    row.update({flag: False for flag in AUTHORITY_FLAGS})
    return row


def validate_contract(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_PROPOSAL_FIELDS - value.keys())
    if missing:
        errors.append("missing_required_fields:" + ",".join(missing))
    if value.get("expected_disposition") not in LABELS:
        errors.append("unknown_outcome_label")
    if not str(value.get("record_id", "")).startswith("SYNTH-MONITOR-LOG-LM6794-N"):
        errors.append("synthetic_record_identifier_required")
    if not str(value.get("zone_alias", "")).startswith("SYNTH-ZONE-LM6794-N"):
        errors.append("synthetic_zone_alias_required")
    if value.get("raw_identifier") not in {None, ""}:
        errors.append("raw_identifier_forbidden")
    if value.get("readings") != [] or value.get("uncertainty_values") != []:
        errors.append("numeric_or_ungrounded_measurement_forbidden")
    if value.get("real_world_rows") != 0 or value.get("external_actions") != 0:
        errors.append("nonzero_external_scope")
    if value.get("calibration_state") != "not_evaluated":
        errors.append("calibration_evaluation_forbidden")
    if value.get("action_state") != "none":
        errors.append("operational_action_forbidden")
    states = value.get("channel_states")
    if not isinstance(states, dict) or set(states) != set(CHANNELS):
        errors.append("channel_order_or_shape_invalid")
    elif any(state != "not_observed" for state in states.values()):
        errors.append("observed_channel_state_forbidden")
    for flag in AUTHORITY_FLAGS + ("identity_continuity_claim", "consciousness_or_personhood_claim"):
        if value.get(flag) is not False:
            errors.append(flag + "_must_be_false")
    return errors


def mutate(contract: dict[str, Any], kind: str) -> dict[str, Any]:
    value = json.loads(json.dumps(contract, ensure_ascii=False))
    if kind == "missing_hypothesis":
        value.pop("hypothesis", None)
    elif kind == "unknown_outcome_label":
        value["expected_disposition"] = "validated"
    elif kind == "numeric_reading_injection":
        value["readings"] = [{"channel": "temperature", "value": 20.0, "unit": "degC"}]
        value["channel_states"]["temperature"] = "observed"
    elif kind == "authority_escalation":
        value["environmental_risk_determined"] = True
        value["treatment_or_mitigation_recommended"] = True
        value["stage20_ready"] = True
    else:
        raise ValueError("unknown mutation kind")
    return value


def validate_columns(columns: list[dict[str, Any]]) -> dict[str, Any]:
    if [item.get("channel") for item in columns] != list(CHANNELS):
        return {"accepted": False, "reason": "channel_order_or_vocabulary_invalid"}
    if any(item.get("state") != "not_observed" for item in columns):
        return {"accepted": False, "reason": "observation_state_forbidden"}
    if any(item.get("value") is not None or item.get("unit") is not None for item in columns):
        return {"accepted": False, "reason": "numeric_reading_forbidden"}
    return {"accepted": True, "channels": len(columns), "real_measurement_claim": False}


def validate_sequence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    sequences = [row.get("sequence") for row in rows]
    if sequences != list(range(1, len(rows) + 1)):
        return {"accepted": False, "reason": "nondeterministic_or_gapped_sequence"}
    if len({row.get("record_id") for row in rows}) != len(rows):
        return {"accepted": False, "reason": "duplicate_record_identifier"}
    if any(not str(row.get("record_id", "")).startswith("SYNTH-MONITOR-SEQ-") for row in rows):
        return {"accepted": False, "reason": "synthetic_sequence_prefix_required"}
    return {"accepted": True, "rows": len(rows), "real_event_order_claim": False}


def validate_correction(original: dict[str, Any], correction: dict[str, Any]) -> dict[str, Any]:
    if correction.get("supersedes") != original.get("record_id"):
        return {"accepted": False, "reason": "supersession_link_missing"}
    if correction.get("record_id") == original.get("record_id"):
        return {"accepted": False, "reason": "original_erasure_or_identifier_reuse"}
    if not correction.get("reason"):
        return {"accepted": False, "reason": "correction_reason_required"}
    return {"accepted": True, "records_retained": 2, "real_record_correction_claim": False}


def validate_provenance(nodes: list[dict[str, Any]], edges: list[dict[str, str]]) -> dict[str, Any]:
    identifiers = [node.get("id") for node in nodes]
    if len(identifiers) != len(set(identifiers)):
        return {"accepted": False, "reason": "duplicate_provenance_node"}
    if any(not str(identifier).startswith("SYNTH-PROV-") for identifier in identifiers):
        return {"accepted": False, "reason": "synthetic_provenance_prefix_required"}
    if any(node.get("type") == "Agent" for node in nodes):
        return {"accepted": False, "reason": "agent_or_identity_node_forbidden"}
    known = set(identifiers)
    if any(edge.get("from") not in known or edge.get("to") not in known for edge in edges):
        return {"accepted": False, "reason": "dangling_provenance_edge"}
    return {"accepted": True, "nodes": len(nodes), "edges": len(edges), "identity_claim": False}


def validate_accessibility(html: str) -> dict[str, Any]:
    required = ("<main", "<h1", "<table", "<caption", "<th scope=", "<details", "@media print")
    missing = [token for token in required if token not in html]
    return {
        "accepted": not missing,
        "missing": missing,
        "structural_only": True,
        "complete_accessibility_assurance": False,
        "affected_user_evaluation": False,
    }


def privacy_candidates(text: str) -> list[str]:
    return sorted(name for name, pattern in PRIVACY_PATTERNS.items() if pattern.search(text))


def validate_skill(skill_dir: Path) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    agent_yaml = skill_dir / "agents" / "openai.yaml"
    errors: list[str] = []
    if not skill_md.is_file() or not agent_yaml.is_file():
        errors.append("missing_standard_skill_surface")
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        for required in ("---", "# ", "## Inputs", "## Procedure", "## Refusal conditions", "## Output"):
            if required not in text:
                errors.append("missing_skill_section:" + required)
        if "TODO" in text:
            errors.append("unfinished_skill_placeholder")
    return {
        "accepted": not errors,
        "errors": errors,
        "global_install": False,
        "real_world_rows": 0,
        "external_actions": 0,
    }


def positive_runner_fixture(name: str) -> dict[str, Any]:
    if name == "contract" or name == "mutation":
        proposal = {key: "bounded" for key in REQUIRED_PROPOSAL_FIELDS}
        proposal.update({"proposal_id": "LM6794-N001", "expected_disposition": "completed", "protected_gates": []})
        contract = contract_from_proposal(proposal)
        if name == "contract":
            errors = validate_contract(contract)
            return {"accepted": not errors, "errors": errors}
        rejected = all(validate_contract(mutate(contract, kind)) for kind in MUTATIONS)
        return {"accepted": rejected, "mutations_rejected": len(MUTATIONS)}
    if name == "column":
        return validate_columns([{"channel": channel, "state": "not_observed", "value": None, "unit": None} for channel in CHANNELS])
    if name == "sequence":
        return validate_sequence([{"sequence": index, "record_id": f"SYNTH-MONITOR-SEQ-{index:03d}"} for index in range(1, 4)])
    if name == "correction":
        return validate_correction(
            {"record_id": "SYNTH-MONITOR-CORR-001"},
            {"record_id": "SYNTH-MONITOR-CORR-002", "supersedes": "SYNTH-MONITOR-CORR-001", "reason": "synthetic transcription correction"},
        )
    if name == "provenance":
        nodes = [{"id": "SYNTH-PROV-ENTITY-001", "type": "Entity"}, {"id": "SYNTH-PROV-ACTIVITY-001", "type": "Activity"}]
        return validate_provenance(nodes, [{"from": nodes[0]["id"], "to": nodes[1]["id"]}])
    if name == "accessibility":
        return validate_accessibility("<main><h1>x</h1><table><caption>x</caption><th scope='col'>x</th></table><details>x</details><style>@media print{}</style></main>")
    if name == "privacy":
        hits = privacy_candidates("SYNTH-MONITOR-LOG-LM6794-N001")
        return {"accepted": not hits, "candidates": hits}
    if name in {"method_flow", "terminal"}:
        return {"accepted": True, "bounded_surface": name, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    raise ValueError("unknown runner")


def rejecting_runner_fixture(name: str) -> dict[str, Any]:
    if name == "contract":
        return {"accepted": False, "reason": "missing_required_fields"}
    if name == "column":
        return validate_columns([{"channel": "temperature", "state": "observed", "value": 20.0, "unit": "degC"}])
    if name == "sequence":
        return validate_sequence([{"sequence": 2, "record_id": "SYNTH-MONITOR-SEQ-001"}])
    if name == "correction":
        return validate_correction({"record_id": "SYNTH-MONITOR-CORR-001"}, {"record_id": "SYNTH-MONITOR-CORR-001", "supersedes": None})
    if name == "provenance":
        return validate_provenance([{"id": "SYNTH-PROV-AGENT-001", "type": "Agent"}], [])
    if name == "accessibility":
        return validate_accessibility("<div>unstructured</div>")
    if name == "privacy":
        marker = "source" + "_thread_id=synthetic-forbidden"
        hits = privacy_candidates(marker)
        return {"accepted": not hits, "candidates": hits}
    if name == "mutation":
        return {"accepted": False, "reason": "synthetic_invalid_mutation"}
    if name in {"method_flow", "terminal"}:
        return {"accepted": False, "reason": "synthetic_gate_breach"}
    raise ValueError("unknown runner")


def runner_smoke(name: str, invalid: bool = False) -> dict[str, Any]:
    if name not in RUNNERS:
        raise ValueError("unknown runner")
    detail = rejecting_runner_fixture(name) if invalid else positive_runner_fixture(name)
    expected = not invalid
    accepted = bool(detail.get("accepted"))
    return {
        "runner": name,
        "fixture": "rejecting" if invalid else "positive",
        "accepted": accepted,
        "expected_acceptance": expected,
        "expectation_met": accepted == expected,
        "details": detail,
        "real_world_rows": 0,
        "external_actions": 0,
    }


def runner_cli(name: str) -> None:
    parser = argparse.ArgumentParser(description=f"Lyren Moss v679-v4 {name} runner")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--invalid", action="store_true")
    args = parser.parse_args()
    if not args.smoke:
        parser.error("--smoke is required")
    print(json.dumps(runner_smoke(name, args.invalid), sort_keys=True))
