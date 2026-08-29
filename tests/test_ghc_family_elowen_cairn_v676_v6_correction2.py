from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "docs" / "elowen-cairn" / "v676-v6" / "correction2"
ORIGINAL_SHA = "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf"
CORRECTION1_SHA = "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f"


def load(name: str):
    return json.loads((CORRECTION / name).read_text(encoding="utf-8"))


def test_both_failed_canonical_receipts_remain_zero_credit() -> None:
    rows = load("phase-truth.json")["failed_canonical_receipts"]
    assert [row["sha256"] for row in rows] == [ORIGINAL_SHA, CORRECTION1_SHA]
    assert all(row["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" and row["success_count"] == 0 and row["replay_count"] == 0 for row in rows)


def test_correction2_method_flow_and_counts_are_exact() -> None:
    flow = load("method-flow-overlay.json")
    assert flow["current_phase_partition"] == {"methods": 660, "failed": 210, "passing": 450}
    assert flow["correction_partition"] == {"methods": 2, "failed": 1, "passing": 1}
    assert [row["truth"] for row in flow["methods"]] == [False, True]
    assert flow["current_overlay"] == {"effective_negatives": 42651, "effective_methods": 33778, "retained_failed_witnesses": 14312, "bounded_passing_witnesses": 20155, "open_gaps": 359, "exact_gates": 351}


def test_serialization_correction_is_narrow_and_reconstructs_set_comparisons() -> None:
    policy = load("validation-policy.json")
    assert policy["replay_manifest_paths_serialization_before"] == "set"
    assert policy["replay_manifest_paths_serialization_after"] == "sorted_list"
    assert policy["coverage_comparison_domain"] == "set reconstructed at comparison only"
    assert policy["owner_test_timeout_seconds"] == 900
    assert policy["prior_canonical_replay_forbidden"] is True


def test_correction2_content_seal_replays() -> None:
    seal = load("content-seal.json")
    assert len(seal["entries"]) == 4
    for row in seal["entries"]:
        raw = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert hashlib.sha256(raw).hexdigest() == row["sha256_normalized_lf"]
