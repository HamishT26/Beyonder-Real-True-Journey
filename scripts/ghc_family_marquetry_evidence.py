#!/usr/bin/env python3
"""Bounded synthetic marquetry evidence runner for Eiren Kestrel v663-v8.

The runner validates declared owner-local fixtures only.  It does not identify
wood, authorize fabrication, operate tools, assess safety, decide rights or
cultural meaning, perform live identity operations, or promote Stage 20.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
import math
from pathlib import Path
import re
from typing import Any, Callable


SCHEMA = "ghc.family.eiren-kestrel.v663-v8.marquetry-evidence.v1"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_GATES = [
    "empirical", "participant", "professional", "production_or_deployment",
    "legal_or_cultural", "maori_authority", "privacy_complete",
    "accessibility_complete", "exhaustive_security", "independent_reproduction",
    "agi_or_asi", "consciousness_or_personhood", "theory_of_everything",
    "proof_or_canon", "stage_20",
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


def _unique_text(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    rows = _list(value, label, nonempty=nonempty)
    if not all(isinstance(row, str) and row for row in rows) or len(rows) != len(set(rows)):
        raise EvidenceError(f"{label} must contain unique nonempty text")
    return rows


def _root(value: Any, label: str) -> dict[str, Any]:
    record = _mapping(value, label)
    if record.get("synthetic") is not True:
        raise EvidenceError(f"{label} must declare synthetic=true")
    if record.get("real_world_rows") != 0:
        raise EvidenceError(f"{label} must contain zero real-world rows")
    if record.get("authority") != "none":
        raise EvidenceError(f"{label} cannot claim authority")
    if record.get("expected_outcome") not in ALLOWED_OUTCOMES:
        raise EvidenceError(f"{label} has an invalid expected outcome")
    return record


def _ok(record: dict[str, Any], proposal_id: str) -> dict[str, Any]:
    return {
        "proposal_id": proposal_id,
        "expected_outcome": record["expected_outcome"],
        "protected_gates": list(PROTECTED_GATES),
        "real_world_rows": 0,
        "valid": True,
        "boundary": "Synthetic owner-local software witness only; no real-world authority or result.",
    }


def validate_design_capsule(value: Any) -> dict[str, Any]:
    record = _root(value, "design capsule")
    if not re.fullmatch(r"syn:marquetry:panel:[a-z0-9-]+", _text(record.get("panel_token"), "panel token")):
        raise EvidenceError("panel token must use the synthetic namespace")
    _unique_text(record.get("motif_tokens"), "motif tokens", nonempty=True)
    if not isinstance(record.get("revision"), int) or record["revision"] < 1:
        raise EvidenceError("revision must be a positive integer")
    if record.get("release_hold") is not True or record.get("fabrication_authorized") is not False:
        raise EvidenceError("release hold and fabrication refusal are mandatory")
    return _ok(record, "EK6638-N001")


def validate_piece_topology(value: Any) -> dict[str, Any]:
    record = _root(value, "piece topology")
    nodes = _list(record.get("pieces"), "pieces", nonempty=True)
    identifiers = [_text(row.get("id"), "piece id") for row in nodes if isinstance(row, dict)]
    if len(identifiers) != len(nodes) or len(identifiers) != len(set(identifiers)):
        raise EvidenceError("piece identifiers must be unique")
    if any(row.get("orientation") not in {"face", "back"} for row in nodes):
        raise EvidenceError("piece orientation is invalid")
    edges = _list(record.get("adjacency"), "adjacency", nonempty=True)
    for edge in edges:
        edge = _mapping(edge, "adjacency edge")
        if edge.get("left") not in identifiers or edge.get("right") not in identifiers or edge.get("left") == edge.get("right"):
            raise EvidenceError("orphan or self adjacency rejected")
    if record.get("overlap_state") != "quarantined" or record.get("material_identification") != "refused":
        raise EvidenceError("overlap quarantine and material refusal are mandatory")
    return _ok(record, "EK6638-N002")


def validate_motif_decomposition(value: Any) -> dict[str, Any]:
    record = _root(value, "motif decomposition")
    regions = _unique_text(record.get("regions"), "regions", nonempty=True)
    coverage = _mapping(record.get("piece_coverage"), "piece coverage")
    if set(coverage) != set(regions) or any(not isinstance(rows, list) or not rows for rows in coverage.values()):
        raise EvidenceError("every region requires declared piece coverage")
    if record.get("boundary_ambiguity") != "retained" or record.get("cultural_interpretation") is not False:
        raise EvidenceError("ambiguity must remain and interpretation is refused")
    if record.get("negative_space_declared") is not True:
        raise EvidenceError("negative space must be explicit")
    return _ok(record, "EK6638-N003")


def validate_match_transformations(value: Any) -> dict[str, Any]:
    record = _root(value, "match transformations")
    rows = _list(record.get("transformations"), "transformations", nonempty=True)
    allowed = {"bookmatch", "slip_match", "four_way_match"}
    if any(_mapping(row, "transformation").get("kind") not in allowed for row in rows):
        raise EvidenceError("unsupported match transformation")
    if [row.get("sequence") for row in rows] != list(range(1, len(rows) + 1)):
        raise EvidenceError("match sequence must be contiguous")
    if record.get("source_leaf") != "placeholder" or record.get("visual_quality") != "reserved":
        raise EvidenceError("source leaf and visual quality must remain unresolved")
    if record.get("discontinuity_witness") != "retained":
        raise EvidenceError("discontinuity witness is mandatory")
    return _ok(record, "EK6638-N004")


def validate_cut_path_graph(value: Any) -> dict[str, Any]:
    record = _root(value, "cut-path graph")
    vertices = _list(record.get("vertices"), "vertices", nonempty=True)
    ids = []
    for vertex in vertices:
        vertex = _mapping(vertex, "vertex")
        ids.append(_text(vertex.get("id"), "vertex id"))
        coordinates = _list(vertex.get("xy"), "vertex coordinates")
        if len(coordinates) != 2 or any(not isinstance(item, (int, float)) or not math.isfinite(item) for item in coordinates):
            raise EvidenceError("vertex coordinates must be finite two-vectors")
    if len(ids) != len(set(ids)):
        raise EvidenceError("vertex identifiers must be unique")
    for edge in _list(record.get("edges"), "edges", nonempty=True):
        edge = _mapping(edge, "edge")
        if edge.get("source") not in ids or edge.get("target") not in ids or edge.get("source") == edge.get("target"):
            raise EvidenceError("invalid cut-path edge")
    if record.get("toolpath") is not None or record.get("cutting_instruction") is not False:
        raise EvidenceError("toolpaths and cutting instructions are prohibited")
    if record.get("kerf_status") != "placeholder":
        raise EvidenceError("kerf must remain a placeholder")
    return _ok(record, "EK6638-N005")


def validate_packet_layers(value: Any) -> dict[str, Any]:
    record = _root(value, "packet layers")
    layers = _list(record.get("layers"), "layers", nonempty=True)
    if [row.get("order") for row in layers if isinstance(row, dict)] != list(range(1, len(layers) + 1)):
        raise EvidenceError("layer order must be contiguous")
    _unique_text(record.get("registration_marks"), "registration marks", nonempty=True)
    if record.get("sacrificial_layer") != "placeholder" or record.get("mismatch_state") != "quarantined":
        raise EvidenceError("sacrificial layer and mismatch quarantine are mandatory")
    if record.get("machinery_instructions") != 0:
        raise EvidenceError("machinery instructions are prohibited")
    return _ok(record, "EK6638-N006")


def validate_grain_field(value: Any) -> dict[str, Any]:
    record = _root(value, "grain field")
    axes = _list(record.get("local_axes"), "local axes", nonempty=True)
    if any(not isinstance(axis, list) or len(axis) != 2 or any(not isinstance(item, (int, float)) or not math.isfinite(item) for item in axis) for axis in axes):
        raise EvidenceError("local grain axes must be finite two-vectors")
    if record.get("species_status") != "unknown" or record.get("continuity") != "placeholder":
        raise EvidenceError("species and continuity must remain unresolved")
    if record.get("uncertainty") != "unresolved" or record.get("real_material_rows") != 0:
        raise EvidenceError("uncertainty and zero real material rows are mandatory")
    return _ok(record, "EK6638-N007")


def validate_observation_taxonomy(value: Any) -> dict[str, Any]:
    record = _root(value, "observation taxonomy")
    allowed = {"colour_placeholder", "figure_placeholder", "surface_placeholder"}
    labels = _unique_text(record.get("labels"), "observation labels", nonempty=True)
    if not set(labels).issubset(allowed):
        raise EvidenceError("observation label is outside the declared taxonomy")
    if record.get("illumination") != "placeholder" or record.get("image_rows") != 0:
        raise EvidenceError("illumination and image evidence remain absent")
    if record.get("disagreement") != "retained" or record.get("authentication") is not False:
        raise EvidenceError("disagreement retention and authentication refusal are mandatory")
    return _ok(record, "EK6638-N008")


def validate_layup_dependencies(value: Any) -> dict[str, Any]:
    record = _root(value, "lay-up dependencies")
    nodes = _unique_text(record.get("nodes"), "dependency nodes", nonempty=True)
    for edge in _list(record.get("edges"), "dependency edges", nonempty=True):
        edge = _mapping(edge, "dependency edge")
        if edge.get("before") not in nodes or edge.get("after") not in nodes or edge.get("before") == edge.get("after"):
            raise EvidenceError("invalid lay-up dependency")
    if record.get("adhesive_status") != "vacant" or record.get("pressing_release") is not False:
        raise EvidenceError("adhesive vacancy and pressing hold are mandatory")
    if record.get("structural_claim") is not False:
        raise EvidenceError("structural release is prohibited")
    return _ok(record, "EK6638-N009")


def validate_panel_reconciliation(value: Any) -> dict[str, Any]:
    record = _root(value, "panel reconciliation")
    counts = _mapping(record.get("counts"), "counts")
    required = {"planned", "accepted", "quarantined", "unresolved", "omitted", "duplicates"}
    if set(counts) != required or any(not isinstance(counts[key], int) or counts[key] < 0 for key in required):
        raise EvidenceError("panel counts are invalid")
    if counts["planned"] != counts["accepted"] + counts["quarantined"] + counts["unresolved"] + counts["omitted"]:
        raise EvidenceError("planned piece count does not reconcile")
    if counts["duplicates"] != 0 or record.get("real_panel_complete") is not False:
        raise EvidenceError("duplicates and real completion are refused")
    _unique_text(record.get("piece_tokens"), "piece tokens", nonempty=True)
    return _ok(record, "EK6638-N010")


def validate_thos_queue(value: Any) -> dict[str, Any]:
    record = _root(value, "THOS queue")
    if record.get("expected_outcome") != "represented" or record.get("people") != 0:
        raise EvidenceError("THOS queue remains represented with zero people")
    if record.get("two_key_stop") is not True or record.get("readback") != "synthetic_digest":
        raise EvidenceError("two-key stop and readback are mandatory")
    if not isinstance(record.get("unresolved_count"), int) or record["unresolved_count"] < 0 or record.get("unresolved_ceiling", -1) < record["unresolved_count"]:
        raise EvidenceError("unresolved work exceeds the declared ceiling")
    if record.get("operational_effectiveness") is not False:
        raise EvidenceError("operational effectiveness is prohibited")
    return _ok(record, "EK6638-N011")


def validate_gmut_symmetry(value: Any) -> dict[str, Any]:
    record = _root(value, "GMUT symmetry")
    if record.get("expected_outcome") != "represented" or record.get("model_family") != "typed_planar_isometry":
        raise EvidenceError("GMUT symmetry remains a typed represented board")
    _unique_text(record.get("orbit"), "orbit", nonempty=True)
    _unique_text(record.get("stabilizer"), "stabilizer", nonempty=True)
    if record.get("empirical_rows") != 0 or record.get("physical_claim") is not False:
        raise EvidenceError("empirical and physical claims are prohibited")
    if record.get("boundary_conditions") != "declared_symbolic":
        raise EvidenceError("symbolic boundary conditions are required")
    return _ok(record, "EK6638-N012")


def validate_gmut_hygroexpansion(value: Any) -> dict[str, Any]:
    record = _root(value, "GMUT hygroexpansion")
    if record.get("expected_outcome") != "represented" or record.get("orthotropic_axes") != "typed_symbolic":
        raise EvidenceError("GMUT hygroexpansion remains represented and symbolic")
    if record.get("coefficients") != {} or record.get("measurements") != 0:
        raise EvidenceError("coefficients and measurements must remain empty")
    if record.get("covariance") != "placeholder" or record.get("material_law") is not False:
        raise EvidenceError("covariance and material-law boundaries are violated")
    if record.get("temperature_status") != "placeholder" or record.get("moisture_status") != "placeholder":
        raise EvidenceError("temperature and moisture must remain placeholders")
    return _ok(record, "EK6638-N013")


def validate_freed_statement(value: Any) -> dict[str, Any]:
    record = _root(value, "Freed ID statement")
    if record.get("expected_outcome") != "represented" or record.get("profile") != "synthetic_nonproduction":
        raise EvidenceError("Freed ID statement must remain represented and nonproduction")
    if any(record.get(key) != 0 for key in ("real_keys", "real_proofs", "real_credentials", "live_status_events")):
        raise EvidenceError("real identity lifecycle material is prohibited")
    if record.get("authorship_claim") is not False or record.get("trust_governance") is not False:
        raise EvidenceError("authorship and trust governance cannot be inferred")
    return _ok(record, "EK6638-N014")


def validate_correction_chain(value: Any) -> dict[str, Any]:
    record = _root(value, "correction chain")
    chain = _list(record.get("chain"), "chain", nonempty=True)
    revisions = [row.get("revision") for row in chain if isinstance(row, dict)]
    if revisions != list(range(1, len(chain) + 1)):
        raise EvidenceError("correction revisions must be contiguous")
    if any(row.get("supersedes") != (None if index == 0 else revisions[index - 1]) for index, row in enumerate(chain)):
        raise EvidenceError("correction supersession is invalid")
    if record.get("deletions") != 0 or record.get("live_identity_operations") != 0:
        raise EvidenceError("deletions and live identity operations are prohibited")
    if record.get("challenge_state") != "open_placeholder":
        raise EvidenceError("challenge state must remain open")
    return _ok(record, "EK6638-N015")


def validate_accessible_map(value: Any) -> dict[str, Any]:
    record = _root(value, "accessible map")
    html = _text(record.get("html"), "HTML")
    if any(token not in html for token in ('lang="en"', "<main", "<h1", "<table", "<caption")):
        raise EvidenceError("required structural accessibility token is missing")
    if record.get("colour_only_state") is not False or record.get("noncolour_textures") is not True:
        raise EvidenceError("redundant noncolour state is mandatory")
    reserved = set(_unique_text(record.get("reserved_evaluations"), "reserved evaluations", nonempty=True))
    required = {"manual", "browser", "assistive_technology", "cognitive", "maori_language", "affected_user"}
    if reserved != required:
        raise EvidenceError("manual and affected-user evaluations must remain reserved")
    return _ok(record, "EK6638-N016")


def validate_privacy_envelope(value: Any) -> dict[str, Any]:
    record = _root(value, "privacy envelope")
    if record.get("personal_rows") != 0 or record.get("free_text") != "":
        raise EvidenceError("personal rows and free text are prohibited")
    if record.get("contact_fields") != 0 or record.get("unique_identifiers") != 0:
        raise EvidenceError("contact fields and unique identifiers are prohibited")
    if record.get("retention") != "hold" or record.get("correction_route") != "placeholder":
        raise EvidenceError("retention and correction boundaries are mandatory")
    if record.get("privacy_review") != "reserved":
        raise EvidenceError("privacy review remains reserved")
    return _ok(record, "EK6638-N017")


def validate_aat_zero_row(value: Any) -> dict[str, Any]:
    record = _root(value, "Getty AAT adapter")
    if record.get("expected_outcome") != "open_gap":
        raise EvidenceError("Getty AAT adapter must remain open_gap")
    if record.get("network_calls") != 0 or record.get("downloaded_rows") != 0 or record.get("terms") != []:
        raise EvidenceError("zero-row adapter cannot ingest data")
    if record.get("source_status") != "official_documentation_identified_concept_unresolved":
        raise EvidenceError("source and concept gap is not preserved")
    if record.get("classification_authority") != "none":
        raise EvidenceError("classification authority is prohibited")
    return _ok(record, "EK6638-N018")


def validate_authority_matrix(value: Any) -> dict[str, Any]:
    record = _root(value, "authority matrix")
    if record.get("expected_outcome") != "exact_gate":
        raise EvidenceError("authority matrix must remain exact_gate")
    entries = _list(record.get("entries"), "entries", nonempty=True)
    for entry in entries:
        entry = _mapping(entry, "authority entry")
        if entry.get("state") != "exact_gate" or entry.get("decision") is not None:
            raise EvidenceError("authority entry cannot be decided locally")
        if entry.get("authority_holder") != "external_authorized_human_or_body":
            raise EvidenceError("authority holder must remain external")
    if record.get("maori_authority") != "exact_gate" or record.get("traditional_knowledge") != "exact_gate":
        raise EvidenceError("Māori authority and traditional knowledge remain exact-gated")
    return _ok(record, "EK6638-N019")


def validate_stage20_docket(value: Any) -> dict[str, Any]:
    record = _root(value, "Stage 20 docket")
    if record.get("verdict") != "NOT_READY_FOR_STAGE_20" or record.get("accepted_evidence") != []:
        raise EvidenceError("Stage 20 docket must fail closed with zero admitted evidence")
    missing = set(_unique_text(record.get("missing_requirements"), "missing requirements", nonempty=True))
    required = {"authenticated_real_assets", "competent_practitioners", "governed_safety_review", "rights_authority", "independent_reproduction"}
    if not required.issubset(missing):
        raise EvidenceError("Stage 20 missing requirements are incomplete")
    if record.get("promotion_allowed") is not False:
        raise EvidenceError("Stage 20 promotion must remain prohibited")
    return _ok(record, "EK6638-N020")


VALIDATORS: dict[str, Callable[[Any], dict[str, Any]]] = {
    function.__name__: function
    for function in (
        validate_design_capsule, validate_piece_topology, validate_motif_decomposition,
        validate_match_transformations, validate_cut_path_graph, validate_packet_layers,
        validate_grain_field, validate_observation_taxonomy, validate_layup_dependencies,
        validate_panel_reconciliation, validate_thos_queue, validate_gmut_symmetry,
        validate_gmut_hygroexpansion, validate_freed_statement,
        validate_correction_chain, validate_accessible_map, validate_privacy_envelope,
        validate_aat_zero_row, validate_authority_matrix, validate_stage20_docket,
    )
}


def _fixture_root(outcome: str = "completed") -> dict[str, Any]:
    return {"synthetic": True, "real_world_rows": 0, "authority": "none", "expected_outcome": outcome}


def fixture_cases() -> list[dict[str, Any]]:
    html = '<!doctype html><html lang="en"><body><main><h1>Marquetry evidence</h1><table><caption>Pieces</caption></table></main></body></html>'
    rows: list[tuple[str, str, dict[str, Any], list[dict[str, Any]]]] = [
        ("EK6638-N001", "validate_design_capsule", _fixture_root() | {"panel_token": "syn:marquetry:panel:a", "motif_tokens": ["syn:motif:a"], "revision": 1, "release_hold": True, "fabrication_authorized": False}, [{"path": ["panel_token"], "value": "real:panel:a"}, {"path": ["revision"], "value": 0}, {"path": ["release_hold"], "value": False}, {"path": ["fabrication_authorized"], "value": True}]),
        ("EK6638-N002", "validate_piece_topology", _fixture_root() | {"pieces": [{"id": "p1", "orientation": "face"}, {"id": "p2", "orientation": "back"}], "adjacency": [{"left": "p1", "right": "p2"}], "overlap_state": "quarantined", "material_identification": "refused"}, [{"path": ["pieces", 1, "id"], "value": "p1"}, {"path": ["pieces", 0, "orientation"], "value": "unknown"}, {"path": ["adjacency", 0, "right"], "value": "missing"}, {"path": ["overlap_state"], "value": "accepted"}]),
        ("EK6638-N003", "validate_motif_decomposition", _fixture_root() | {"regions": ["r1", "r2"], "piece_coverage": {"r1": ["p1"], "r2": ["p2"]}, "negative_space_declared": True, "boundary_ambiguity": "retained", "cultural_interpretation": False}, [{"path": ["regions", 1], "value": "r1"}, {"path": ["piece_coverage", "r2"], "value": []}, {"path": ["negative_space_declared"], "value": False}, {"path": ["cultural_interpretation"], "value": True}]),
        ("EK6638-N004", "validate_match_transformations", _fixture_root() | {"transformations": [{"sequence": 1, "kind": "bookmatch"}, {"sequence": 2, "kind": "slip_match"}], "source_leaf": "placeholder", "discontinuity_witness": "retained", "visual_quality": "reserved"}, [{"path": ["transformations", 0, "kind"], "value": "quality_match"}, {"path": ["transformations", 1, "sequence"], "value": 3}, {"path": ["source_leaf"], "value": "identified"}, {"path": ["visual_quality"], "value": "approved"}]),
        ("EK6638-N005", "validate_cut_path_graph", _fixture_root() | {"vertices": [{"id": "v1", "xy": [0, 0]}, {"id": "v2", "xy": [1, 0]}], "edges": [{"source": "v1", "target": "v2"}], "kerf_status": "placeholder", "toolpath": None, "cutting_instruction": False}, [{"path": ["vertices", 1, "id"], "value": "v1"}, {"path": ["edges", 0, "target"], "value": "missing"}, {"path": ["toolpath"], "value": ["cut"]}, {"path": ["kerf_status"], "value": "measured"}]),
        ("EK6638-N006", "validate_packet_layers", _fixture_root() | {"layers": [{"order": 1}, {"order": 2}], "registration_marks": ["m1", "m2"], "sacrificial_layer": "placeholder", "mismatch_state": "quarantined", "machinery_instructions": 0}, [{"path": ["layers", 1, "order"], "value": 3}, {"path": ["registration_marks", 1], "value": "m1"}, {"path": ["mismatch_state"], "value": "released"}, {"path": ["machinery_instructions"], "value": 1}]),
        ("EK6638-N007", "validate_grain_field", _fixture_root() | {"local_axes": [[1, 0], [0, 1]], "species_status": "unknown", "continuity": "placeholder", "uncertainty": "unresolved", "real_material_rows": 0}, [{"path": ["local_axes", 0], "value": [1, 0, 0]}, {"path": ["species_status"], "value": "identified"}, {"path": ["uncertainty"], "value": "certain"}, {"path": ["real_material_rows"], "value": 1}]),
        ("EK6638-N008", "validate_observation_taxonomy", _fixture_root() | {"labels": ["colour_placeholder", "figure_placeholder"], "illumination": "placeholder", "image_rows": 0, "disagreement": "retained", "authentication": False}, [{"path": ["labels", 0], "value": "premium"}, {"path": ["illumination"], "value": "measured"}, {"path": ["image_rows"], "value": 1}, {"path": ["authentication"], "value": True}]),
        ("EK6638-N009", "validate_layup_dependencies", _fixture_root() | {"nodes": ["substrate", "backing", "face"], "edges": [{"before": "substrate", "after": "face"}], "adhesive_status": "vacant", "pressing_release": False, "structural_claim": False}, [{"path": ["nodes", 1], "value": "substrate"}, {"path": ["edges", 0, "after"], "value": "missing"}, {"path": ["adhesive_status"], "value": "approved"}, {"path": ["pressing_release"], "value": True}]),
        ("EK6638-N010", "validate_panel_reconciliation", _fixture_root() | {"counts": {"planned": 10, "accepted": 6, "quarantined": 1, "unresolved": 2, "omitted": 1, "duplicates": 0}, "piece_tokens": ["syn:piece:1", "syn:piece:2"], "real_panel_complete": False}, [{"path": ["counts", "accepted"], "value": 7}, {"path": ["counts", "duplicates"], "value": 1}, {"path": ["piece_tokens", 1], "value": "syn:piece:1"}, {"path": ["real_panel_complete"], "value": True}]),
        ("EK6638-N011", "validate_thos_queue", _fixture_root("represented") | {"people": 0, "two_key_stop": True, "unresolved_count": 2, "unresolved_ceiling": 3, "readback": "synthetic_digest", "operational_effectiveness": False}, [{"path": ["people"], "value": 1}, {"path": ["two_key_stop"], "value": False}, {"path": ["unresolved_ceiling"], "value": 1}, {"path": ["operational_effectiveness"], "value": True}]),
        ("EK6638-N012", "validate_gmut_symmetry", _fixture_root("represented") | {"model_family": "typed_planar_isometry", "orbit": ["p1", "p2"], "stabilizer": ["identity"], "boundary_conditions": "declared_symbolic", "empirical_rows": 0, "physical_claim": False}, [{"path": ["model_family"], "value": "fitted_physics"}, {"path": ["orbit", 1], "value": "p1"}, {"path": ["empirical_rows"], "value": 1}, {"path": ["physical_claim"], "value": True}]),
        ("EK6638-N013", "validate_gmut_hygroexpansion", _fixture_root("represented") | {"orthotropic_axes": "typed_symbolic", "coefficients": {}, "measurements": 0, "covariance": "placeholder", "temperature_status": "placeholder", "moisture_status": "placeholder", "material_law": False}, [{"path": ["coefficients"], "value": {"alpha": 1}}, {"path": ["measurements"], "value": 1}, {"path": ["covariance"], "value": "estimated"}, {"path": ["material_law"], "value": True}]),
        ("EK6638-N014", "validate_freed_statement", _fixture_root("represented") | {"profile": "synthetic_nonproduction", "real_keys": 0, "real_proofs": 0, "real_credentials": 0, "live_status_events": 0, "authorship_claim": False, "trust_governance": False}, [{"path": ["profile"], "value": "production"}, {"path": ["real_keys"], "value": 1}, {"path": ["authorship_claim"], "value": True}, {"path": ["trust_governance"], "value": True}]),
        ("EK6638-N015", "validate_correction_chain", _fixture_root() | {"chain": [{"revision": 1, "supersedes": None}, {"revision": 2, "supersedes": 1}], "deletions": 0, "live_identity_operations": 0, "challenge_state": "open_placeholder"}, [{"path": ["chain", 1, "revision"], "value": 3}, {"path": ["chain", 1, "supersedes"], "value": None}, {"path": ["deletions"], "value": 1}, {"path": ["challenge_state"], "value": "closed"}]),
        ("EK6638-N016", "validate_accessible_map", _fixture_root() | {"html": html, "colour_only_state": False, "noncolour_textures": True, "reserved_evaluations": ["manual", "browser", "assistive_technology", "cognitive", "maori_language", "affected_user"]}, [{"path": ["html"], "value": "<html><body>missing</body></html>"}, {"path": ["colour_only_state"], "value": True}, {"path": ["noncolour_textures"], "value": False}, {"path": ["reserved_evaluations"], "value": []}]),
        ("EK6638-N017", "validate_privacy_envelope", _fixture_root() | {"personal_rows": 0, "free_text": "", "contact_fields": 0, "unique_identifiers": 0, "retention": "hold", "correction_route": "placeholder", "privacy_review": "reserved"}, [{"path": ["personal_rows"], "value": 1}, {"path": ["free_text"], "value": "name"}, {"path": ["unique_identifiers"], "value": 1}, {"path": ["privacy_review"], "value": "complete"}]),
        ("EK6638-N018", "validate_aat_zero_row", _fixture_root("open_gap") | {"network_calls": 0, "downloaded_rows": 0, "terms": [], "source_status": "official_documentation_identified_concept_unresolved", "classification_authority": "none"}, [{"path": ["network_calls"], "value": 1}, {"path": ["downloaded_rows"], "value": 1}, {"path": ["terms"], "value": ["marquetry"]}, {"path": ["expected_outcome"], "value": "completed"}]),
        ("EK6638-N019", "validate_authority_matrix", _fixture_root("exact_gate") | {"entries": [{"topic": "authorship", "state": "exact_gate", "decision": None, "authority_holder": "external_authorized_human_or_body"}, {"topic": "cultural_expression", "state": "exact_gate", "decision": None, "authority_holder": "external_authorized_human_or_body"}], "maori_authority": "exact_gate", "traditional_knowledge": "exact_gate"}, [{"path": ["entries", 0, "state"], "value": "completed"}, {"path": ["entries", 0, "decision"], "value": "owned"}, {"path": ["entries", 1, "authority_holder"], "value": "model"}, {"path": ["maori_authority"], "value": "cleared"}]),
        ("EK6638-N020", "validate_stage20_docket", _fixture_root() | {"verdict": "NOT_READY_FOR_STAGE_20", "accepted_evidence": [], "missing_requirements": ["authenticated_real_assets", "competent_practitioners", "governed_safety_review", "rights_authority", "independent_reproduction"], "promotion_allowed": False}, [{"path": ["verdict"], "value": "READY"}, {"path": ["accepted_evidence"], "value": ["synthetic"]}, {"path": ["missing_requirements"], "value": ["authenticated_real_assets"]}, {"path": ["promotion_allowed"], "value": True}]),
    ]
    return [{"proposal_id": proposal_id, "validator": validator, "positive": positive, "mutations": mutations} for proposal_id, validator, positive, mutations in rows]


def apply_mutation(value: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    mutated = deepcopy(value)
    cursor: Any = mutated
    for component in mutation["path"][:-1]:
        cursor = cursor[component]
    cursor[mutation["path"][-1]] = deepcopy(mutation["value"])
    return mutated


def mutation_receipt() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for case in fixture_cases():
        validator = VALIDATORS[case["validator"]]
        if not validator(case["positive"])["valid"]:
            raise EvidenceError("positive fixture failed")
        for index, mutation in enumerate(case["mutations"], 1):
            try:
                validator(apply_mutation(case["positive"], mutation))
            except (EvidenceError, KeyError, TypeError, IndexError) as exc:
                records.append({"mutation_id": f"{case['proposal_id']}-M{index:02d}", "proposal_id": case["proposal_id"], "failure_credit": 0, "rejected": True, "witness": str(exc)})
            else:
                raise EvidenceError(f"mutation was not rejected: {case['proposal_id']}:{index}")
    return {"schema": f"{SCHEMA}.mutations", "positive_fixture_count": len(fixture_cases()), "mutation_count": len(records), "rejected_count": sum(row["rejected"] for row in records), "records": records, "valid": len(records) == 80 and all(row["rejected"] for row in records), "boundary": "Deterministic synthetic rejecting mutations only; every failure retains zero completion credit."}


PROFILES = {
    "design-capsule": ["EK6638-N001"],
    "piece-topology": ["EK6638-N002", "EK6638-N003"],
    "match-geometry": ["EK6638-N004", "EK6638-N005", "EK6638-N006"],
    "material-state": ["EK6638-N007", "EK6638-N008", "EK6638-N009", "EK6638-N010"],
    "thos-assembly": ["EK6638-N011"],
    "gmut-obligations": ["EK6638-N012", "EK6638-N013"],
    "freed-id-boundaries": ["EK6638-N014", "EK6638-N015"],
    "report-boundaries": ["EK6638-N016", "EK6638-N017"],
    "source-authority": ["EK6638-N018", "EK6638-N019"],
    "terminal-evidence": ["EK6638-N020"],
}


def run_profile(profile: str) -> dict[str, Any]:
    if profile not in PROFILES:
        raise EvidenceError("unknown runner profile")
    selected = set(PROFILES[profile])
    witnesses = [VALIDATORS[case["validator"]](case["positive"]) for case in fixture_cases() if case["proposal_id"] in selected]
    receipt: dict[str, Any] = {"schema": f"{SCHEMA}.runner-profile", "profile": profile, "proposal_ids": sorted(selected), "witnesses": witnesses, "real_world_rows": 0, "valid": len(witnesses) == len(selected) and all(row["valid"] for row in witnesses), "boundary": "Owner-local synthetic smoke only; not installation, deployment, qualification, or authority."}
    if profile == "terminal-evidence":
        receipt["mutations"] = mutation_receipt()
        receipt["valid"] = receipt["valid"] and receipt["mutations"]["valid"]
    return receipt


def render_report(outcomes: list[dict[str, Any]]) -> tuple[str, str]:
    rows = "".join(f'<tr><th scope="row">{row["proposal_id"]}</th><td>{row["outcome"]}</td><td>{row["evidence_class"]}</td></tr>' for row in outcomes)
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren Kestrel v663-v8 evidence</title></head><body><header><h1>Eiren Kestrel v663-v8 bounded evidence</h1></header><nav aria-label="Report sections"><a href="#outcomes">Outcomes</a> <a href="#boundaries">Boundaries</a></nav><main><section id="outcomes"><h2>New proposal outcomes</h2><table><caption>Twenty preregistered proposal dispositions</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence class</th></tr></thead><tbody>' + rows + '</tbody></table></section><section id="boundaries"><h2>Boundaries</h2><p>All fixtures are synthetic. Manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved. Fabrication, professional safety, rights, cultural interpretation, Māori authority, production, empirical claims, and Stage 20 remain gated.</p></section></main><footer><p>Verdict: NOT_READY_FOR_STAGE_20.</p></footer></body></html>\n')
    text = "Eiren Kestrel v663-v8 bounded evidence\n\n" + "\n".join(f"{row['proposal_id']}: {row['outcome']} ({row['evidence_class']})" for row in outcomes) + "\n\nAll fixtures are synthetic. Manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved. Fabrication, professional safety, rights, cultural interpretation, Māori authority, production, empirical claims, and Stage 20 remain gated.\n\nVerdict: NOT_READY_FOR_STAGE_20.\n"
    return html, text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = run_profile(args.profile)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"profile": args.profile, "valid": receipt["valid"]}, sort_keys=True))
    return 0 if receipt["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
