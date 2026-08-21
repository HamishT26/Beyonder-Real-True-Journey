#!/usr/bin/env python3
"""Shared zero-document runner core for Caelen Ash v664-v8."""

from __future__ import annotations

import argparse
import json


CAPABILITIES = {
    "score_source_provenance": "completed",
    "rehearsal_topology_guard": "completed",
    "transposition_vacancy": "completed",
    "page_turn_reservation": "completed",
    "musicxml_smufl_zero_document": "represented",
    "gmut_score_time_firewall": "represented",
    "thos_material_handover": "represented",
    "freed_id_edition_vacancy": "represented",
    "music_rights_authority_matrix": "exact_gate",
    "stage20_score_nonpromotion": "completed",
}
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def evaluate(capability: str) -> dict:
    if capability not in CAPABILITIES:
        raise ValueError(f"unknown capability: {capability}")
    disposition = CAPABILITIES[capability]
    receipt = {
        "schema": "ghc.family.caelen.v664-v8.runner-receipt.v1",
        "capability": capability,
        "input_kind": "synthetic_zero_document",
        "real_record_count": 0,
        "real_person_count": 0,
        "score_file_count": 0,
        "rehearsal_observation_count": 0,
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
        print(f"{capability}: {receipt['disposition']} (synthetic zero-document)")
    return 0
