#!/usr/bin/env python3
"""Bounded synthetic craft-workflow guard for Caelen Ash v672-v4."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

REQUIREMENTS = {'warp_plan': ['plan_id', 'version', 'supersedes', 'correction_state'], 'material_provenance': ['yarn_lot_surrogate', 'substitution_state', 'provenance_state', 'real_material_claim'], 'loom_compatibility': ['reed_state', 'heddle_state', 'compatibility_basis', 'real_loom_assessed'], 'threading_sequence': ['threading_steps', 'monotonic', 'orientation', 'manual_execution_reserved'], 'pattern_lineage': ['pattern_version', 'repeat_boundary', 'prior_version', 'nonerasure'], 'accessibility_structure': ['plain_language_summary', 'diagram_alternative', 'table_relationships', 'manual_evaluation_reserved'], 'privacy_minimization': ['fields_allowed', 'workshop_zone_generalized', 'direct_identifiers'], 'workload_handover': ['open_actions', 'hold_state', 'next_role', 'workload_budget'], 'authority_boundary': ['operational_authority', 'legal_authority', 'cultural_authority', 'maori_authority'], 'weaving_packet': ['schema_version', 'components', 'deterministic', 'stage20']}

def validate(data, expected_surface):
    reasons = []
    if data.get("surface") != expected_surface:
        reasons.append("surface_mismatch")
    if data.get("synthetic") is not True:
        reasons.append("synthetic_boundary_missing")
    if data.get("authority_state") != "vacant":
        reasons.append("authority_promoted")
    if "raw_identifier" in data:
        reasons.append("raw_identifier_present")
    payload = data.get("payload")
    if not isinstance(payload, dict):
        reasons.append("payload_not_object")
        payload = {}
    for key in REQUIREMENTS[expected_surface]:
        if key not in payload:
            reasons.append("missing_required:" + key)
    if expected_surface == "authority_boundary":
        for key in REQUIREMENTS[expected_surface]:
            if payload.get(key) != "vacant":
                reasons.append("authority_value_not_vacant:" + key)
    if expected_surface == "privacy_minimization" and payload.get("direct_identifiers") is not False:
        reasons.append("direct_identifier_boundary_failed")
    if expected_surface == "weaving_packet" and payload.get("stage20") != "not_ready":
        reasons.append("stage20_promoted")
    return {"valid": not reasons, "reasons": sorted(set(reasons)), "surface": expected_surface}

def run_fixture_directory(expected_surface, fixture_dir):
    results = []
    for path in sorted(Path(fixture_dir).glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        result = validate(data, expected_surface)
        expected_valid = path.name == "accepting.json"
        results.append({
            "fixture": path.name,
            "expected_valid": expected_valid,
            "observed_valid": result["valid"],
            "reasons": result["reasons"],
            "passed": result["valid"] is expected_valid,
        })
    return {
        "surface": expected_surface,
        "checks": len(results),
        "passed_checks": sum(row["passed"] for row in results),
        "valid": len(results) == 6 and all(row["passed"] for row in results),
        "results": results,
        "scope": "synthetic_software_only",
        "broader_credit": 0,
    }

def cli(expected_surface):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = run_fixture_directory(expected_surface, args.fixture_dir)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"surface": expected_surface, "valid": receipt["valid"], "checks": receipt["checks"]}))
    raise SystemExit(0 if receipt["valid"] else 1)
