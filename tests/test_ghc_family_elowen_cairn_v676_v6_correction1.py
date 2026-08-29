from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v676-v6"
CORRECTION = BASE / "correction1"
FAILED_SHA = "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf"


def load(name: str):
    return json.loads((CORRECTION / name).read_text(encoding="utf-8"))


def test_failed_canonical_is_immutable_zero_credit_and_not_replayed() -> None:
    truth = load("phase-truth.json")
    assert truth["failed_canonical_receipt_sha256"] == FAILED_SHA
    assert truth["failed_canonical_status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
    assert (truth["failed_canonical_invocation_count"], truth["failed_canonical_success_count"], truth["failed_canonical_replay_count"]) == (1, 0, 0)
    assert truth["original_final_rewritten"] is False
    assert truth["failed_receipt_rewritten"] is False


def test_correction_method_flow_and_overlay_are_exact() -> None:
    flow = load("method-flow-overlay.json")
    assert flow["current_phase_partition"] == {"methods": 658, "failed": 209, "passing": 449}
    assert flow["correction_partition"] == {"methods": 4, "failed": 2, "passing": 2}
    assert [row["truth"] for row in flow["methods"]] == [False, True, False, True]
    assert flow["methods"][1]["failed_witness_preserved"] == flow["methods"][0]["method_id"]
    assert flow["current_overlay"] == {
        "effective_negatives": 42650,
        "effective_methods": 33776,
        "retained_failed_witnesses": 14311,
        "bounded_passing_witnesses": 20154,
        "open_gaps": 359,
        "exact_gates": 351,
    }


def test_timeout_correction_is_narrow_and_original_replay_forbidden() -> None:
    policy = load("validation-policy.json")
    assert policy["original_owner_test_timeout_seconds"] == 300
    assert policy["corrected_owner_test_timeout_seconds"] == 900
    assert policy["original_canonical_success_credit"] == 0
    assert policy["original_canonical_replay_forbidden"] is True
    assert policy["complete_repository_suite_authorized"] is False


def test_correction_content_seal_replays() -> None:
    seal = load("content-seal.json")
    assert len(seal["entries"]) == 4
    for row in seal["entries"]:
        raw = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert hashlib.sha256(raw).hexdigest() == row["sha256_normalized_lf"]
