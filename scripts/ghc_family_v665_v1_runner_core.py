#!/usr/bin/env python3
"""Shared zero-row and zero-object runner core for Orin Thale v665-v1."""

from __future__ import annotations

import argparse
import json


CAPABILITIES = {
    "variational_bicomplex_boundary": "completed",
    "jet_atlas_quarantine": "completed",
    "contact_degree_guard": "completed",
    "euler_boundary_lineage": "completed",
    "millinery_topology_vacancy": "completed",
    "millinery_material_state": "completed",
    "thos_bench_handover": "represented",
    "freed_id_work_envelope": "represented",
    "millinery_rights_authority": "exact_gate",
    "stage20_model_nonpromotion": "completed",
}
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def evaluate(capability: str) -> dict:
    if capability not in CAPABILITIES:
        raise ValueError(f"unknown capability: {capability}")
    disposition = CAPABILITIES[capability]
    receipt = {
        "schema": "ghc.family.orin.v665-v1.runner-receipt.v1",
        "capability": capability,
        "input_kind": "synthetic_zero_row_or_object",
        "real_record_count": 0,
        "real_person_count": 0,
        "real_object_or_material_count": 0,
        "empirical_row_count": 0,
        "participant_or_operator_observation_count": 0,
        "authority_decision_count": 0,
        "protected_gates_preserved": True,
        "disposition": disposition,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": disposition in ALLOWED,
    }
    return receipt


def main_for(capability: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    receipt = evaluate(capability)
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    else:
        print(f"{capability}: {receipt['disposition']} (synthetic zero-row or object)")
    return 0
