#!/usr/bin/env python3
"""Bounded synthetic printmaking evidence runner for Caelen Morrow v663-v7.

This family-current runner validates only declared synthetic fixtures. It does
not authorize or evaluate real printmaking, chemicals, equipment, people,
identity operations, rights decisions, professional practice, or Stage 20.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
import math
from pathlib import Path
import re
from typing import Any, Callable


SCHEMA = "ghc.family.caelen-morrow.v663-v7.printmaking-evidence.v1"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production_or_deployment",
    "legal_or_cultural",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "proof_or_canon",
    "stage_20",
]


class EvidenceError(ValueError):
    """Raised when a bounded synthetic fixture violates its contract."""


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvidenceError(f"{label} must be an object")
    return value


def _list(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list) or (nonempty and not value):
        raise EvidenceError(f"{label} must be {'a nonempty' if nonempty else 'an'} array")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{label} must be nonempty text")
    return value


def _synthetic_root(value: Any, label: str) -> dict[str, Any]:
    record = _mapping(value, label)
    if record.get("synthetic") is not True:
        raise EvidenceError(f"{label} must declare synthetic=true")
    if record.get("real_world_rows") != 0:
        raise EvidenceError(f"{label} must contain zero real-world rows")
    if record.get("authority") != "none":
        raise EvidenceError(f"{label} cannot claim authority")
    outcome = record.get("expected_outcome")
    if outcome not in ALLOWED_OUTCOMES:
        raise EvidenceError(f"{label} has an invalid expected outcome")
    return record


def _unique_text(values: Any, label: str, *, nonempty: bool = False) -> list[str]:
    rows = _list(values, label, nonempty=nonempty)
    if not all(isinstance(row, str) and row for row in rows):
        raise EvidenceError(f"{label} must contain nonempty text")
    if len(rows) != len(set(rows)):
        raise EvidenceError(f"{label} must be unique")
    return rows


def _ok(record: dict[str, Any], proposal_id: str) -> dict[str, Any]:
    return {
        "proposal_id": proposal_id,
        "expected_outcome": record["expected_outcome"],
        "protected_gates": list(PROTECTED_GATES),
        "real_world_rows": 0,
        "valid": True,
        "boundary": "Synthetic software witness only; no real-world authority or result.",
    }


def validate_work_capsule(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "work capsule")
    if not re.fullmatch(r"syn:work:[a-z0-9-]+", _text(record.get("work_token"), "work token")):
        raise EvidenceError("work token must use the synthetic namespace")
    _unique_text(record.get("matrix_family"), "matrix family", nonempty=True)
    if not isinstance(record.get("plan_revision"), int) or record["plan_revision"] < 1:
        raise EvidenceError("plan revision must be a positive integer")
    if record.get("custody_hold") is not True or record.get("real_objects") != 0:
        raise EvidenceError("custody hold and zero real objects are mandatory")
    return _ok(record, "CM6637-N001")


def validate_matrix_graph(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "matrix graph")
    nodes = _list(record.get("nodes"), "nodes", nonempty=True)
    node_ids = [_text(node.get("id"), "node id") for node in nodes if isinstance(node, dict)]
    if len(node_ids) != len(nodes) or len(node_ids) != len(set(node_ids)):
        raise EvidenceError("node identifiers must be unique")
    types = {node["id"]: node.get("type") for node in nodes}
    if any(kind not in {"matrix", "impression"} for kind in types.values()):
        raise EvidenceError("node type must be matrix or impression")
    edges = _list(record.get("edges"), "edges", nonempty=True)
    for edge in edges:
        edge = _mapping(edge, "edge")
        source, target = edge.get("source"), edge.get("target")
        if source not in types or target not in types:
            raise EvidenceError("orphan edge rejected")
        if source == target or types[source] != "matrix" or types[target] != "impression":
            raise EvidenceError("edge must connect a matrix to an impression")
    if record.get("cancellation_hold") is not True:
        raise EvidenceError("cancellation hold is mandatory")
    return _ok(record, "CM6637-N002")


EDITION_NUMBER = re.compile(r"^(?P<number>[1-9][0-9]*)/(?P<total>[1-9][0-9]*)$")
EDITION_PROOF = re.compile(r"^(?P<proof>AP|PP|TP|BAT) (?P<number>[1-9][0-9]*)$")


def parse_edition_notation(value: str) -> dict[str, Any]:
    text = _text(value, "edition notation")
    numbered = EDITION_NUMBER.fullmatch(text)
    if numbered:
        number, total = int(numbered["number"]), int(numbered["total"])
        if number > total:
            raise EvidenceError("edition number exceeds total")
        return {"kind": "numbered", "number": number, "total": total}
    proof = EDITION_PROOF.fullmatch(text)
    if proof:
        return {"kind": "proof", "proof": proof["proof"], "number": int(proof["number"])}
    raise EvidenceError("unsupported or ambiguous edition notation")


def validate_edition_notation(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "edition notation")
    cases = _unique_text(record.get("cases"), "edition cases", nonempty=True)
    parsed = [parse_edition_notation(case) for case in cases]
    if record.get("artist_acceptance") != "reserved":
        raise EvidenceError("artist acceptance must remain reserved")
    result = _ok(record, "CM6637-N003")
    result["parsed"] = parsed
    return result


def validate_registration(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "registration contract")
    if record.get("dimensions") != 2 or record.get("unit") != "synthetic_mm":
        raise EvidenceError("registration coordinates require two synthetic-mm dimensions")
    matrix = _list(record.get("affine"), "affine matrix", nonempty=True)
    if len(matrix) != 3 or any(not isinstance(row, list) or len(row) != 3 for row in matrix):
        raise EvidenceError("affine matrix must be 3 by 3")
    if any(not isinstance(item, (int, float)) or not math.isfinite(item) for row in matrix for item in row):
        raise EvidenceError("affine matrix must contain finite numeric values")
    if matrix[2] != [0, 0, 1]:
        raise EvidenceError("affine homogeneous row is invalid")
    if record.get("uncertainty_status") != "placeholder" or record.get("measured") is not False:
        raise EvidenceError("uncertainty must remain a non-measured placeholder")
    return _ok(record, "CM6637-N004")


def validate_material_quarantine(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "material quarantine")
    if record.get("compatibility_status") != "unknown":
        raise EvidenceError("material compatibility must remain unknown")
    if record.get("source_status") != "vacant" or record.get("safety_hold") is not True:
        raise EvidenceError("source vacancy and safety hold are mandatory")
    if record.get("real_materials") != 0 or record.get("disposal_authority") != "none":
        raise EvidenceError("real materials and disposal authority are prohibited")
    return _ok(record, "CM6637-N005")


def validate_session_events(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "press-session events")
    events = _list(record.get("events"), "events", nonempty=True)
    expected_sequence = list(range(1, len(events) + 1))
    if [event.get("sequence") for event in events if isinstance(event, dict)] != expected_sequence:
        raise EvidenceError("events must be contiguous and ordered")
    allowed = {"open", "pull_placeholder", "inspection_note", "reject", "correction", "close"}
    closed = False
    for event in events:
        event = _mapping(event, "event")
        if event.get("type") not in allowed:
            raise EvidenceError("unknown event type")
        if closed:
            raise EvidenceError("post-close event rejected")
        closed = event["type"] == "close"
    if not closed or record.get("people") != 0:
        raise EvidenceError("session must close with zero people")
    return _ok(record, "CM6637-N006")


def validate_drying_state(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "drying state")
    states = _unique_text(record.get("states"), "states", nonempty=True)
    if states != ["planned", "holding", "ready_placeholder"]:
        raise EvidenceError("drying states must retain the declared progression")
    transitions = _list(record.get("transitions"), "transitions", nonempty=True)
    if transitions != [["planned", "holding"], ["holding", "ready_placeholder"]]:
        raise EvidenceError("drying transition is not declared")
    if record.get("clock_domain") != "synthetic_sequence" or record.get("elapsed_measured") is not False:
        raise EvidenceError("real elapsed-time evidence is prohibited")
    return _ok(record, "CM6637-N007")


def validate_image_lineage(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "image lineage")
    if record.get("image_rows") != 0 or record.get("pixel_payloads") != 0:
        raise EvidenceError("image lineage must contain zero images and pixels")
    _unique_text(record.get("placeholder_tokens"), "placeholder tokens", nonempty=True)
    if record.get("rights_status") != "unknown" or record.get("redaction_required") is not True:
        raise EvidenceError("rights vacancy and redaction hold are mandatory")
    return _ok(record, "CM6637-N008")


def validate_pull_observation(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "pull observations")
    observations = _list(record.get("observations"), "observations", nonempty=True)
    allowed = {"registration_placeholder", "ink_transfer_placeholder", "surface_placeholder"}
    for observation in observations:
        observation = _mapping(observation, "observation")
        if observation.get("label") not in allowed or observation.get("observation_only") is not True:
            raise EvidenceError("observation taxonomy or evidence class is invalid")
        if observation.get("uncertainty") != "unresolved":
            raise EvidenceError("observation uncertainty must remain unresolved")
    if record.get("artist_acceptance") != "reserved":
        raise EvidenceError("artist acceptance must remain reserved")
    return _ok(record, "CM6637-N009")


def validate_edition_reconciliation(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "edition reconciliation")
    counts = _mapping(record.get("counts"), "edition counts")
    required = {"planned", "pulled", "rejected", "quarantined", "retained", "destroyed_placeholder"}
    if set(counts) != required or any(not isinstance(counts[key], int) or counts[key] < 0 for key in required):
        raise EvidenceError("edition counts are invalid")
    if counts["pulled"] != counts["rejected"] + counts["quarantined"] + counts["retained"]:
        raise EvidenceError("edition counts do not reconcile")
    if counts["pulled"] > counts["planned"] or counts["destroyed_placeholder"] != 0:
        raise EvidenceError("planned ceiling or destruction placeholder violated")
    _unique_text(record.get("impression_tokens"), "impression tokens", nonempty=True)
    return _ok(record, "CM6637-N010")


def validate_thos_handover(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "THOS handover")
    if record.get("expected_outcome") != "represented":
        raise EvidenceError("THOS outcome must remain represented")
    if record.get("people") != 0 or record.get("blind_real_arms") != 0:
        raise EvidenceError("real people or arms are prohibited")
    if record.get("independent_review") is not False:
        raise EvidenceError("independent review cannot be inferred")
    if record.get("workload_ceiling") != "placeholder" or record.get("injury_signal") != "placeholder":
        raise EvidenceError("workload and injury signals must remain placeholders")
    return _ok(record, "CM6637-N011")


def validate_gmut_registration(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "GMUT registration board")
    if record.get("model_family") != "typed_scalar_tensor_eft" or record.get("empirical_rows") != 0:
        raise EvidenceError("GMUT family or empirical row boundary violated")
    if record.get("covariance_status") != "placeholder" or record.get("claim_class") != "symbolic_only":
        raise EvidenceError("GMUT covariance and claim class must remain symbolic")
    if record.get("likelihood") is not None or record.get("parameter_constraints") != []:
        raise EvidenceError("real likelihood or parameter constraints are prohibited")
    return _ok(record, "CM6637-N012")


def validate_gmut_ink_transfer(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "GMUT ink-transfer board")
    if record.get("transfer_field") != "symbolic" or record.get("real_measurements") != 0:
        raise EvidenceError("ink-transfer field must remain symbolic and unmeasured")
    if record.get("pressure_status") != "placeholder" or record.get("viscosity_status") != "placeholder":
        raise EvidenceError("pressure and viscosity must remain placeholders")
    if record.get("material_law_claim") is not False or record.get("prediction_claim") is not False:
        raise EvidenceError("material-law and prediction claims are prohibited")
    return _ok(record, "CM6637-N013")


def validate_freed_statement(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "Freed ID edition statement")
    if record.get("expected_outcome") != "represented":
        raise EvidenceError("Freed ID statement must remain represented")
    if any(record.get(key) != 0 for key in ("real_keys", "real_proofs", "real_credentials", "live_status_events")):
        raise EvidenceError("real identity lifecycle material is prohibited")
    if record.get("profile") != "synthetic_nonproduction" or record.get("trust_governance") is not False:
        raise EvidenceError("Freed ID profile must remain nonproduction and ungoverned")
    return _ok(record, "CM6637-N014")


def validate_freed_correction(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "Freed ID correction")
    chain = _list(record.get("chain"), "correction chain", nonempty=True)
    revisions = [item.get("revision") for item in chain if isinstance(item, dict)]
    if revisions != list(range(1, len(chain) + 1)):
        raise EvidenceError("correction chain must be append-only and contiguous")
    if any(item.get("supersedes") != (None if index == 0 else revisions[index - 1]) for index, item in enumerate(chain)):
        raise EvidenceError("correction supersession is invalid")
    if record.get("deletions") != 0 or record.get("correction_authority") != "none":
        raise EvidenceError("deletion and correction authority are prohibited")
    return _ok(record, "CM6637-N015")


def validate_accessible_report(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "accessible report")
    html = _text(record.get("html"), "HTML")
    required = ('lang="en"', "<main", "<h1", "<table", "<caption")
    if any(token not in html for token in required):
        raise EvidenceError("required structural accessibility token is missing")
    if record.get("color_only_state") is not False:
        raise EvidenceError("colour-only state is prohibited")
    reserved = _unique_text(record.get("reserved_evaluations"), "reserved evaluations", nonempty=True)
    if set(reserved) != {"manual", "browser", "assistive_technology", "cognitive", "maori_language", "affected_user"}:
        raise EvidenceError("manual and affected-user evaluations must remain reserved")
    return _ok(record, "CM6637-N016")


def validate_privacy_envelope(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "privacy envelope")
    if record.get("personal_rows") != 0 or record.get("free_text") != "":
        raise EvidenceError("personal rows and free text are prohibited")
    if record.get("address_fields") != 0 or record.get("contact_fields") != 0:
        raise EvidenceError("address and contact fields are prohibited")
    if record.get("unique_identifier") is not False or record.get("privacy_review") != "reserved":
        raise EvidenceError("unique identifiers are refused and privacy review remains reserved")
    return _ok(record, "CM6637-N017")


def validate_aat_zero_row(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "Getty AAT adapter")
    if record.get("expected_outcome") != "open_gap":
        raise EvidenceError("AAT adapter must remain an open gap")
    if record.get("network_calls") != 0 or record.get("downloaded_rows") != 0 or record.get("terms") != []:
        raise EvidenceError("zero-row adapter cannot ingest data")
    if record.get("source_status") != "official_source_identified_no_ingestion":
        raise EvidenceError("official source vacancy is not preserved")
    return _ok(record, "CM6637-N018")


def validate_authority_gate(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "rights and authority gate")
    if record.get("expected_outcome") != "exact_gate":
        raise EvidenceError("rights and authority outcome must remain exact_gate")
    entries = _list(record.get("entries"), "authority entries", nonempty=True)
    for entry in entries:
        entry = _mapping(entry, "authority entry")
        if entry.get("state") != "exact_gate" or entry.get("decision") is not None:
            raise EvidenceError("authority entry cannot be decided locally")
        if entry.get("authority_holder") != "external_authorized_human_or_body":
            raise EvidenceError("authority holder must remain external")
    if record.get("maori_authority") != "exact_gate":
        raise EvidenceError("Maori authority must remain exact-gated")
    return _ok(record, "CM6637-N019")


def validate_stage20_docket(value: Any) -> dict[str, Any]:
    record = _synthetic_root(value, "Stage 20 docket")
    if record.get("verdict") != "NOT_READY_FOR_STAGE_20" or record.get("accepted_evidence") != []:
        raise EvidenceError("Stage 20 docket must fail closed with zero admitted evidence")
    missing = _unique_text(record.get("missing_requirements"), "missing requirements", nonempty=True)
    if not {"real_evidence", "independent_review", "exact_authority"}.issubset(set(missing)):
        raise EvidenceError("Stage 20 missing requirements are incomplete")
    if record.get("promotion_allowed") is not False:
        raise EvidenceError("Stage 20 promotion must remain prohibited")
    return _ok(record, "CM6637-N020")


VALIDATORS: dict[str, Callable[[Any], dict[str, Any]]] = {
    function.__name__: function
    for function in (
        validate_work_capsule,
        validate_matrix_graph,
        validate_edition_notation,
        validate_registration,
        validate_material_quarantine,
        validate_session_events,
        validate_drying_state,
        validate_image_lineage,
        validate_pull_observation,
        validate_edition_reconciliation,
        validate_thos_handover,
        validate_gmut_registration,
        validate_gmut_ink_transfer,
        validate_freed_statement,
        validate_freed_correction,
        validate_accessible_report,
        validate_privacy_envelope,
        validate_aat_zero_row,
        validate_authority_gate,
        validate_stage20_docket,
    )
}


def _root(outcome: str = "completed") -> dict[str, Any]:
    return {
        "synthetic": True,
        "real_world_rows": 0,
        "authority": "none",
        "expected_outcome": outcome,
    }


def fixture_cases() -> list[dict[str, Any]]:
    html = '<!doctype html><html lang="en"><body><main><h1>Evidence</h1><table><caption>Outcomes</caption></table></main></body></html>'
    rows: list[tuple[str, str, dict[str, Any], list[dict[str, Any]]]] = [
        ("CM6637-N001", "validate_work_capsule", _root() | {"work_token": "syn:work:edition-a", "matrix_family": ["syn:matrix:a"], "plan_revision": 1, "custody_hold": True, "real_objects": 0}, [{"path": ["work_token"], "value": "real:work:a"}, {"path": ["custody_hold"], "value": False}, {"path": ["real_objects"], "value": 1}, {"path": ["authority"], "value": "workshop"}]),
        ("CM6637-N002", "validate_matrix_graph", _root() | {"nodes": [{"id": "m1", "type": "matrix"}, {"id": "i1", "type": "impression"}], "edges": [{"source": "m1", "target": "i1"}], "cancellation_hold": True}, [{"path": ["edges", 0, "target"], "value": "missing"}, {"path": ["edges", 0, "source"], "value": "i1"}, {"path": ["nodes", 1, "id"], "value": "m1"}, {"path": ["cancellation_hold"], "value": False}]),
        ("CM6637-N003", "validate_edition_notation", _root() | {"cases": ["3/20", "AP 1", "PP 1"], "artist_acceptance": "reserved"}, [{"path": ["cases", 0], "value": "21/20"}, {"path": ["cases", 1], "value": "OWNER 1"}, {"path": ["cases", 2], "value": "AP 1"}, {"path": ["artist_acceptance"], "value": "accepted"}]),
        ("CM6637-N004", "validate_registration", _root() | {"dimensions": 2, "unit": "synthetic_mm", "affine": [[1, 0, 2], [0, 1, 3], [0, 0, 1]], "uncertainty_status": "placeholder", "measured": False}, [{"path": ["dimensions"], "value": 3}, {"path": ["unit"], "value": "mm"}, {"path": ["affine", 2], "value": [1, 0, 1]}, {"path": ["measured"], "value": True}]),
        ("CM6637-N005", "validate_material_quarantine", _root("represented") | {"compatibility_status": "unknown", "source_status": "vacant", "safety_hold": True, "real_materials": 0, "disposal_authority": "none"}, [{"path": ["compatibility_status"], "value": "compatible"}, {"path": ["source_status"], "value": "verified"}, {"path": ["safety_hold"], "value": False}, {"path": ["real_materials"], "value": 1}]),
        ("CM6637-N006", "validate_session_events", _root() | {"events": [{"sequence": 1, "type": "open"}, {"sequence": 2, "type": "pull_placeholder"}, {"sequence": 3, "type": "close"}], "people": 0}, [{"path": ["events", 1, "sequence"], "value": 4}, {"path": ["events", 1, "type"], "value": "operate_press"}, {"path": ["events", 2, "type"], "value": "inspection_note"}, {"path": ["people"], "value": 1}]),
        ("CM6637-N007", "validate_drying_state", _root() | {"states": ["planned", "holding", "ready_placeholder"], "transitions": [["planned", "holding"], ["holding", "ready_placeholder"]], "clock_domain": "synthetic_sequence", "elapsed_measured": False}, [{"path": ["states", 2], "value": "ready"}, {"path": ["transitions", 1], "value": ["planned", "ready_placeholder"]}, {"path": ["clock_domain"], "value": "wall_clock"}, {"path": ["elapsed_measured"], "value": True}]),
        ("CM6637-N008", "validate_image_lineage", _root("represented") | {"image_rows": 0, "pixel_payloads": 0, "placeholder_tokens": ["syn:image:1"], "rights_status": "unknown", "redaction_required": True}, [{"path": ["image_rows"], "value": 1}, {"path": ["pixel_payloads"], "value": 1}, {"path": ["rights_status"], "value": "cleared"}, {"path": ["redaction_required"], "value": False}]),
        ("CM6637-N009", "validate_pull_observation", _root() | {"observations": [{"label": "registration_placeholder", "observation_only": True, "uncertainty": "unresolved"}], "artist_acceptance": "reserved"}, [{"path": ["observations", 0, "label"], "value": "quality_failure"}, {"path": ["observations", 0, "observation_only"], "value": False}, {"path": ["observations", 0, "uncertainty"], "value": "certain"}, {"path": ["artist_acceptance"], "value": "accepted"}]),
        ("CM6637-N010", "validate_edition_reconciliation", _root() | {"counts": {"planned": 20, "pulled": 10, "rejected": 2, "quarantined": 1, "retained": 7, "destroyed_placeholder": 0}, "impression_tokens": ["syn:impression:1", "syn:impression:2"]}, [{"path": ["counts", "retained"], "value": 8}, {"path": ["counts", "pulled"], "value": 21}, {"path": ["counts", "destroyed_placeholder"], "value": 1}, {"path": ["impression_tokens", 1], "value": "syn:impression:1"}]),
        ("CM6637-N011", "validate_thos_handover", _root("represented") | {"people": 0, "blind_real_arms": 0, "independent_review": False, "workload_ceiling": "placeholder", "injury_signal": "placeholder"}, [{"path": ["people"], "value": 1}, {"path": ["blind_real_arms"], "value": 1}, {"path": ["independent_review"], "value": True}, {"path": ["workload_ceiling"], "value": "validated"}]),
        ("CM6637-N012", "validate_gmut_registration", _root() | {"model_family": "typed_scalar_tensor_eft", "empirical_rows": 0, "covariance_status": "placeholder", "claim_class": "symbolic_only", "likelihood": None, "parameter_constraints": []}, [{"path": ["empirical_rows"], "value": 1}, {"path": ["covariance_status"], "value": "estimated"}, {"path": ["likelihood"], "value": 0.5}, {"path": ["parameter_constraints"], "value": ["x<1"]}]),
        ("CM6637-N013", "validate_gmut_ink_transfer", _root() | {"transfer_field": "symbolic", "real_measurements": 0, "pressure_status": "placeholder", "viscosity_status": "placeholder", "material_law_claim": False, "prediction_claim": False}, [{"path": ["real_measurements"], "value": 1}, {"path": ["pressure_status"], "value": "measured"}, {"path": ["material_law_claim"], "value": True}, {"path": ["prediction_claim"], "value": True}]),
        ("CM6637-N014", "validate_freed_statement", _root("represented") | {"real_keys": 0, "real_proofs": 0, "real_credentials": 0, "live_status_events": 0, "profile": "synthetic_nonproduction", "trust_governance": False}, [{"path": ["real_keys"], "value": 1}, {"path": ["real_proofs"], "value": 1}, {"path": ["profile"], "value": "production"}, {"path": ["trust_governance"], "value": True}]),
        ("CM6637-N015", "validate_freed_correction", _root() | {"chain": [{"revision": 1, "supersedes": None}, {"revision": 2, "supersedes": 1}], "deletions": 0, "correction_authority": "none"}, [{"path": ["chain", 1, "revision"], "value": 3}, {"path": ["chain", 1, "supersedes"], "value": None}, {"path": ["deletions"], "value": 1}, {"path": ["correction_authority"], "value": "issuer"}]),
        ("CM6637-N016", "validate_accessible_report", _root() | {"html": html, "color_only_state": False, "reserved_evaluations": ["manual", "browser", "assistive_technology", "cognitive", "maori_language", "affected_user"]}, [{"path": ["html"], "value": "<html><body>missing</body></html>"}, {"path": ["color_only_state"], "value": True}, {"path": ["reserved_evaluations", 2], "value": "automatic_only"}, {"path": ["reserved_evaluations"], "value": []}]),
        ("CM6637-N017", "validate_privacy_envelope", _root() | {"personal_rows": 0, "free_text": "", "address_fields": 0, "contact_fields": 0, "unique_identifier": False, "privacy_review": "reserved"}, [{"path": ["personal_rows"], "value": 1}, {"path": ["free_text"], "value": "name"}, {"path": ["address_fields"], "value": 1}, {"path": ["unique_identifier"], "value": True}]),
        ("CM6637-N018", "validate_aat_zero_row", _root("open_gap") | {"network_calls": 0, "downloaded_rows": 0, "terms": [], "source_status": "official_source_identified_no_ingestion"}, [{"path": ["network_calls"], "value": 1}, {"path": ["downloaded_rows"], "value": 1}, {"path": ["terms"], "value": ["printmaking"]}, {"path": ["expected_outcome"], "value": "completed"}]),
        ("CM6637-N019", "validate_authority_gate", _root("exact_gate") | {"entries": [{"topic": "authorship", "state": "exact_gate", "decision": None, "authority_holder": "external_authorized_human_or_body"}, {"topic": "cultural_rights", "state": "exact_gate", "decision": None, "authority_holder": "external_authorized_human_or_body"}], "maori_authority": "exact_gate"}, [{"path": ["entries", 0, "state"], "value": "completed"}, {"path": ["entries", 0, "decision"], "value": "owned"}, {"path": ["entries", 1, "authority_holder"], "value": "model"}, {"path": ["maori_authority"], "value": "cleared"}]),
        ("CM6637-N020", "validate_stage20_docket", _root() | {"verdict": "NOT_READY_FOR_STAGE_20", "accepted_evidence": [], "missing_requirements": ["real_evidence", "independent_review", "exact_authority"], "promotion_allowed": False}, [{"path": ["verdict"], "value": "READY"}, {"path": ["accepted_evidence"], "value": ["synthetic"]}, {"path": ["missing_requirements"], "value": ["real_evidence"]}, {"path": ["promotion_allowed"], "value": True}]),
    ]
    return [
        {"proposal_id": proposal_id, "validator": validator, "positive": positive, "mutations": mutations}
        for proposal_id, validator, positive, mutations in rows
    ]


def apply_mutation(value: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    mutated = deepcopy(value)
    path = mutation["path"]
    cursor: Any = mutated
    for component in path[:-1]:
        cursor = cursor[component]
    cursor[path[-1]] = deepcopy(mutation["value"])
    return mutated


def mutation_receipt() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for case in fixture_cases():
        validator = VALIDATORS[case["validator"]]
        positive = validator(case["positive"])
        if not positive["valid"]:
            raise EvidenceError("positive fixture failed")
        for index, mutation in enumerate(case["mutations"], 1):
            rejected = False
            error = ""
            try:
                validator(apply_mutation(case["positive"], mutation))
            except (EvidenceError, KeyError, TypeError, IndexError) as exc:
                rejected = True
                error = str(exc)
            if not rejected:
                raise EvidenceError(f"mutation was not rejected: {case['proposal_id']}:{index}")
            records.append({
                "mutation_id": f"{case['proposal_id']}-M{index:02d}",
                "proposal_id": case["proposal_id"],
                "failure_credit": 0,
                "rejected": True,
                "witness": error,
            })
    return {
        "schema": f"{SCHEMA}.mutations",
        "positive_fixture_count": len(fixture_cases()),
        "mutation_count": len(records),
        "rejected_count": sum(row["rejected"] for row in records),
        "records": records,
        "valid": len(records) == 80 and all(row["rejected"] for row in records),
        "boundary": "Deterministic synthetic rejecting mutations only; each failure retains zero completion credit.",
    }


PROFILES = {
    "work-capsule": ["CM6637-N001"],
    "matrix-impression-graph": ["CM6637-N002"],
    "edition-notation": ["CM6637-N003"],
    "registration": ["CM6637-N004", "CM6637-N012", "CM6637-N013"],
    "session-event": ["CM6637-N005", "CM6637-N006", "CM6637-N009", "CM6637-N011"],
    "drying-state": ["CM6637-N007", "CM6637-N008"],
    "edition-reconciliation": ["CM6637-N010"],
    "mutation": [case["proposal_id"] for case in fixture_cases()],
    "static-report": ["CM6637-N016", "CM6637-N017"],
    "terminal-evidence": ["CM6637-N014", "CM6637-N015", "CM6637-N018", "CM6637-N019", "CM6637-N020"],
}


def run_profile(profile: str) -> dict[str, Any]:
    if profile not in PROFILES:
        raise EvidenceError("unknown runner profile")
    selected = set(PROFILES[profile])
    witnesses = []
    for case in fixture_cases():
        if case["proposal_id"] in selected:
            witnesses.append(VALIDATORS[case["validator"]](case["positive"]))
    receipt = {
        "schema": f"{SCHEMA}.runner-profile",
        "profile": profile,
        "proposal_ids": sorted(selected),
        "witnesses": witnesses,
        "real_world_rows": 0,
        "valid": len(witnesses) == len(selected) and all(row["valid"] for row in witnesses),
        "boundary": "Owner-local synthetic smoke only; not installation, deployment, qualification, or authority.",
    }
    if profile == "mutation":
        receipt["mutations"] = mutation_receipt()
        receipt["valid"] = receipt["valid"] and receipt["mutations"]["valid"]
    return receipt


def render_report(outcomes: list[dict[str, Any]]) -> tuple[str, str]:
    rows = "".join(
        f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['outcome']}</td><td>{row['evidence_class']}</td></tr>"
        for row in outcomes
    )
    html = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Caelen Morrow v663-v7 evidence</title></head><body>'
        '<header><h1>Caelen Morrow v663-v7 bounded evidence</h1></header>'
        '<nav aria-label="Report sections"><a href="#outcomes">Outcomes</a> '
        '<a href="#boundaries">Boundaries</a></nav><main>'
        '<section id="outcomes"><h2>New proposal outcomes</h2><table>'
        '<caption>Twenty preregistered proposal dispositions</caption>'
        '<thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th>'
        f'<th scope="col">Evidence class</th></tr></thead><tbody>{rows}</tbody></table></section>'
        '<section id="boundaries"><h2>Boundaries</h2><p>All fixtures are synthetic. '
        'Manual, browser, assistive-technology, cognitive, Maori-language, and affected-user '
        'evaluation remain reserved. Rights, professional safety, cultural interpretation, '
        'Maori authority, production, empirical claims, and Stage 20 remain gated.</p></section>'
        '</main><footer><p>Verdict: NOT_READY_FOR_STAGE_20.</p></footer></body></html>\n'
    )
    text = "Caelen Morrow v663-v7 bounded evidence\n\n" + "\n".join(
        f"{row['proposal_id']}: {row['outcome']} ({row['evidence_class']})" for row in outcomes
    ) + (
        "\n\nAll fixtures are synthetic. Manual, browser, assistive-technology, cognitive, "
        "Maori-language, and affected-user evaluation remain reserved. Rights, professional "
        "safety, cultural interpretation, Maori authority, production, empirical claims, and "
        "Stage 20 remain gated.\n\nVerdict: NOT_READY_FOR_STAGE_20.\n"
    )
    return html, text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = run_profile(args.profile)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"profile": args.profile, "valid": receipt["valid"]}, sort_keys=True))
    return 0 if receipt["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
