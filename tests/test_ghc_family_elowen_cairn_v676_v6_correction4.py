from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "docs" / "elowen-cairn" / "v676-v6" / "correction4"
VALIDATOR = ROOT / "scripts" / "validate_ghc_family_elowen_cairn_v676_v6_final.py"
RECEIPTS = [
    "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf",
    "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f",
    "1879b71dbc7fb4f5acf9dd7ca841ad927e5a32f1bc199b520dfd06d6f64af544",
]


def load(name: str):
    return json.loads((CORRECTION / name).read_text(encoding="utf-8"))


def test_three_failed_canonical_receipts_remain_zero_credit() -> None:
    rows = load("phase-truth.json")["failed_canonical_receipts"]
    assert [row["sha256"] for row in rows] == RECEIPTS
    assert all(
        row["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
        and row["success_count"] == 0
        and row["replay_count"] == 0
        for row in rows
    )


def test_correction4_method_flow_counts_and_pairs_are_exact() -> None:
    flow = load("method-flow-overlay.json")
    assert flow["base_phase_partition"] == {"methods": 662, "failed": 211, "passing": 451}
    assert flow["correction_partition"] == {"methods": 24, "failed": 12, "passing": 12}
    assert flow["current_phase_partition"] == {"methods": 686, "failed": 223, "passing": 463}
    assert flow["current_overlay"] == {
        "effective_negatives": 42664,
        "effective_methods": 33804,
        "retained_failed_witnesses": 14325,
        "bounded_passing_witnesses": 20168,
        "open_gaps": 359,
        "exact_gates": 351,
    }
    negatives = [row for row in flow["methods"] if row["truth"] is False]
    positives = [row for row in flow["methods"] if row["truth"] is True]
    assert len(negatives) == len(positives) == 12


def test_validator_receipt_contract_is_exact() -> None:
    source = VALIDATOR.read_text(encoding="utf-8")
    lines = source.splitlines()
    detailed_start = lines.index("    detailed = [")
    detailed_end = next(
        index
        for index in range(detailed_start + 1, len(lines))
        if lines[index].startswith("    objects = tree_objects")
    )
    minimal_start = lines.index("    minimal = [")
    minimal_end = next(
        index
        for index in range(minimal_start + 1, len(lines))
        if lines[index].startswith("    detailed_passed =")
    )
    assert sum(line.startswith("        check(") for line in lines[detailed_start:detailed_end]) == 48
    assert sum(line.startswith("        check(") for line in lines[minimal_start:minimal_end]) == 15
    assert 'detailed_passed == 48 and minimal_passed == 15' in source
    assert '"detailed_checks": {"passed": detailed_passed, "total": 48' in source
    assert '"tests": {"passed": test_count' in source and '"total": 48' in source


def test_correction4_content_seal_replays() -> None:
    seal = load("content-seal.json")
    assert len(seal["entries"]) == 4
    for row in seal["entries"]:
        raw = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert hashlib.sha256(raw).hexdigest() == row["sha256_normalized_lf"]
