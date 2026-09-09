from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ghc_family_preservation_x1 as core


def proposals():
    document = json.loads((ROOT / "docs/vesper-arlen/v689-v7/plan/new-proposals.json").read_text(encoding="utf-8"))
    return [row for row in document["proposals"] if row["session"] == "x1"]


def test_all_frozen_x1_contracts_and_refusals():
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
        ({"op": "unsigned_varint_decode", "payload": {"encoded_hex": "8000"}, "synthetic": True}, "E_ENCODING"),
        ({"op": "fixed_chunk_ranges", "payload": {"length": 4096, "width": 1}, "synthetic": True}, "E_BOUNDS"),
        ({"op": "base32_decode", "payload": {"encoded": "mzxw6"}, "synthetic": True}, "E_ENCODING"),
        ({"op": "crc32_verify", "payload": {"data_hex": "00", "declared_crc32": "ABCDEF00"}, "synthetic": True}, "E_ENCODING"),
        ({"op": "zigzag_encode", "payload": {"value": True}, "synthetic": True}, "E_TYPE"),
        ({"op": "base32_encode", "payload": {"data_hex": "00"}, "synthetic": False}, "E_SYNTHETIC"),
    ],
)
def test_adverse_contracts(payload_request, code):
    assert core.evaluate(payload_request) == {"error": code, "ok": False, "value": None}


def test_duplicate_json_key_is_rejected():
    with pytest.raises(core.ContractError) as exc:
        core.loads_strict('{"op":"a","op":"b"}')
    assert exc.value.code == "E_JSON_DUPLICATE"
