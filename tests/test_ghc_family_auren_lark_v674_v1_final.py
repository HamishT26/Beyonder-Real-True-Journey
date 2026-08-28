from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v674-v1"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SOURCE = "3ba783297438ee89d5778065e30de737af470855"
X1_COMMIT = "763969929943d9c9bcb674999508fe33694fa357"
EVIDENCE_COMMIT = "7d0a8f09df1bf70f69369ad78e5c3da4fce85c66"
FINAL_COUNTS = {
    "effective_negatives": 38103,
    "methods": 25042,
    "failed_witnesses": 9764,
    "bounded_passing_witnesses": 12653,
    "open_gaps": 310,
    "exact_gates": 303,
}


def load(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def test_evidence_gate_and_exact_anchors() -> None:
    gate = load(FINAL / "evidence-gate.json")
    assert gate["state"] == "VALID_IMMUTABLE_X2_EVIDENCE_GATE"
    assert gate["source"] == SOURCE
    assert gate["x1_commit"] == X1_COMMIT
    assert gate["evidence_commit"] == EVIDENCE_COMMIT
    assert gate["evidence_parent"] == X1_COMMIT
    assert gate["evidence_grandparent"] == SOURCE
    assert gate["four_way_equal"] is True
    assert gate["divergence"] == {"ahead": 0, "behind": 0}
    assert gate["source_to_evidence_commits"] == 2
    assert gate["source_to_evidence_merges"] == 0


def test_phase_final_truth_and_outcomes() -> None:
    truth = load(FINAL / "phase-final.json")
    assert truth["proposal_chain"] == 6610
    assert truth["outcomes"] == {
        "completed": 42,
        "represented": 12,
        "open_gap": 3,
        "exact_gate": 3,
    }
    assert truth["effective_counts"] == FINAL_COUNTS
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["canonical_state"] == "PENDING_EXACT_FINAL_COMMIT"
    assert truth["complete_repository_suite"] is False
    assert truth["independent_reproduction"] is False
    assert truth["maori_authority"] is False


def test_failures_remain_additive_and_zero_credit() -> None:
    overlay = load(FINAL / "failure-overlay.json")
    assert overlay["x1_startup_failure_count"] == 19
    assert overlay["x2_operational_failure_count"] == 38
    assert overlay["post_evidence_closeout_failure_count"] == 3
    assert len(overlay["post_evidence_closeout_failures"]) == 3
    assert all(row["state"] == "failed_retained_zero_credit" for row in overlay["post_evidence_closeout_failures"])
    assert all(row["passing_bounded_witness"] is True for row in overlay["post_evidence_closeout_failures"])
    assert overlay["final_counts"] == FINAL_COUNTS
    assert overlay["evidence_seal_rewritten"] is False
    assert "additive" in overlay["recovery_rule"]


def test_completion_checklist_preserves_terminal_gate() -> None:
    checklist = load(FINAL / "completion-checklist.json")
    assert checklist["passed"] == len(checklist["checks"]) == 15
    assert checklist["failed"] == 0
    assert checklist["canonical_terminal_gate_pending"] is True
    assert "not_ready_for_stage_20" in checklist["checks"]


def test_activation_baton_and_route_state() -> None:
    route = load(FINAL / "route-state.json")
    path = ROOT / route["baton_path"]
    text = path.read_text(encoding="utf-8")
    word_count = len(re.findall(r"\b\w+(?:[-']\w+)*\b", text))
    assert route["target_exact_title"] == "Sable Rook"
    assert route["target_phase"] == "v674-v2"
    assert route["recipient_successor_reminder"] == "Caelen Ash v674-v3 after Sable's own exact terminal gate"
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["send_attempts"] == 0
    assert route["precontact"] is False
    assert route["terminal_gate_required"] is True
    assert route["duplicate_guard_required"] is True
    assert route["baton_words"] == word_count
    assert 10000 <= word_count <= 100000
    assert route["baton_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert "SENT_BY_AUREN_LARK remains false" in text
    assert "Auren Lark → Sable Rook → Caelen Ash" in text
    assert "v725-v8" in text
    assert "NOT_READY_FOR_STAGE_20" in text


def test_closeout_is_substantive_and_bounded() -> None:
    text = (FINAL / "closeout.md").read_text(encoding="utf-8")
    word_count = len(re.findall(r"\b\w+(?:[-']\w+)*\b", text))
    assert 500 <= word_count <= 4000
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "independent reproduction" in text
    assert "relational working language" in text


def test_final_content_seal_replays() -> None:
    seal = load(FINAL / "content-seal.json")
    assert seal["source"] == SOURCE
    assert seal["x1_commit"] == X1_COMMIT
    assert seal["evidence_commit"] == EVIDENCE_COMMIT
    assert seal["entry_count"] == len(seal["entries"])
    for row in seal["entries"]:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256_working_bytes"]


def test_final_working_manifest_replays() -> None:
    manifest = load(FINAL / "working-manifest.json")
    assert manifest["self_excluded"] is True
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256_working_bytes"]


def test_final_exact_index_manifest_replays() -> None:
    path = VALIDATION / "final-index-manifest.json"
    assert path.is_file()
    manifest = load(path)
    assert manifest["source"] == SOURCE
    assert manifest["x1_commit"] == X1_COMMIT
    assert manifest["evidence_commit"] == EVIDENCE_COMMIT
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        blob = subprocess.check_output(  # nosec B603
            ["git", "-C", str(ROOT), "cat-file", "blob", f":{row['path']}"]
        )
        blob = blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256_normalized_lf"]


def test_final_privacy_and_security_receipts() -> None:
    privacy = load(VALIDATION / "final-staged-privacy.json")
    security = load(VALIDATION / "final-bounded-security.json")
    assert len(privacy["classes"]) == 5
    assert privacy["confirmed_hits"] == []
    assert privacy["complete_privacy_assurance"] is False
    assert security["findings"] == []
    assert security["exhaustive_security_assurance"] is False


def test_final_staged_review_is_owner_only() -> None:
    review = load(VALIDATION / "final-staged-review.json")
    assert review["final_path_count"] < 2000
    assert review["source_or_sibling_mutations"] == 0
    assert review["deletions"] == 0
    assert review["state"] == "PREPARED_FOR_EXACT_FINAL_INDEX_REVIEW"
    assert all(
        path.startswith(("docs/auren-lark/v674-v1/", "scripts/", "tests/"))
        for path in review["final_paths"]
    )


def test_all_current_phase_json_is_strictly_parseable() -> None:
    paths = sorted(BASE.rglob("*.json"))
    assert len(paths) >= 110
    for path in paths:
        load(path)
