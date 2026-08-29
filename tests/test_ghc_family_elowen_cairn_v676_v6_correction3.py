from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "docs" / "elowen-cairn" / "v676-v6" / "correction3"
RECEIPTS = ["95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf", "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f", "1879b71dbc7fb4f5acf9dd7ca841ad927e5a32f1bc199b520dfd06d6f64af544"]


def load(name: str):
    return json.loads((CORRECTION / name).read_text(encoding="utf-8"))


def test_three_failed_receipts_remain_zero_credit() -> None:
    rows = load("phase-truth.json")["failed_canonical_receipts"]
    assert [row["sha256"] for row in rows] == RECEIPTS
    assert all(row["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" and row["success_count"] == 0 and row["replay_count"] == 0 for row in rows)


def test_correction3_method_flow_and_counts_are_exact() -> None:
    flow = load("method-flow-overlay.json")
    assert flow["current_phase_partition"] == {"methods": 662, "failed": 211, "passing": 451}
    assert flow["correction_partition"] == {"methods": 2, "failed": 1, "passing": 1}
    assert flow["current_overlay"] == {"effective_negatives": 42652, "effective_methods": 33780, "retained_failed_witnesses": 14313, "bounded_passing_witnesses": 20156, "open_gaps": 359, "exact_gates": 351}


def test_lifecycle_exclusions_are_exact_and_replaced_by_explicit_checks() -> None:
    policy = load("validation-policy.json")
    assert policy["new_corrected_head_lifecycle_exclusions"] == ["test_final_delta_and_owner_manifests_have_exact_set_and_blob_parity", "test_lifecycle_is_direct_single_parent_and_merge_free"]
    assert "correction3_owner_manifest_replay" in policy["replacement_evidence"]
    assert "six_phase_commits" in policy["replacement_evidence"]
    assert policy["prior_canonical_replay_forbidden"] is True


def test_correction3_content_seal_replays() -> None:
    seal = load("content-seal.json")
    assert len(seal["entries"]) == 4
    for row in seal["entries"]:
        raw = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert hashlib.sha256(raw).hexdigest() == row["sha256_normalized_lf"]
