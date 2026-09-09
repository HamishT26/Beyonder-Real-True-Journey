from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ghc_family_preservation_x2 as core


def proposals():
    document = json.loads((ROOT / "docs/vesper-arlen/v689-v7/plan/new-proposals.json").read_text(encoding="utf-8"))
    return [row for row in document["proposals"] if row["session"] == "x2"]


def test_all_frozen_x2_contracts_and_refusals():
    rows = proposals()
    assert len(rows) == 100
    for row in rows:
        request = copy.deepcopy(row["request"])
        assert core.evaluate(request) == row["expected"]
        assert request == row["request"]
        candidate = copy.deepcopy(row["candidate_request"])
        assert core.evaluate(candidate) == row["candidate_expected"]
        assert candidate == row["candidate_request"]


@pytest.mark.parametrize(
    "payload_request,code",
    [
        ({"op": "digest_match", "payload": {"data_hex": "00", "declared_sha256": "A" * 64}, "synthetic": True}, "E_ENCODING"),
        ({"op": "deterministic_json", "payload": {"record": {"value": 1.5}}, "synthetic": True}, "E_TYPE"),
        ({"op": "merkle_root", "payload": {"leaves_hex": []}, "synthetic": True}, "E_TYPE"),
        ({"op": "xor_parity", "payload": {"shards_hex": ["00", "0001"]}, "synthetic": True}, "E_SHAPE"),
        ({"op": "claim_reservation", "payload": {"execute": True, "requested_scope": "stage20", "synthetic_evidence": True}, "synthetic": True}, "E_AUTHORITY"),
        ({"op": "sha256_digest", "payload": {"data_hex": "00"}, "synthetic": False}, "E_SYNTHETIC"),
    ],
)
def test_adverse_contracts(payload_request, code):
    assert core.evaluate(payload_request) == {"error": code, "ok": False, "value": None}


def test_merkle_side_conflict_is_rejected():
    row = next(item for item in proposals() if item["operation"] == "merkle_verify")
    request = copy.deepcopy(row["request"])
    request["payload"]["proof"][0]["side"] = "left" if request["payload"]["proof"][0]["side"] == "right" else "right"
    assert core.evaluate(request)["error"] == "E_PROOF"
