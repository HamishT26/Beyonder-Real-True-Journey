from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v673-v8"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SOURCE = "c1818f0c09737c69a1870ef6bf8ed7fc339cb727"
X1_COMMIT = "b567a67858066e6c23f3abb82828f5185d7ab65e"
EVIDENCE_COMMIT = "ca26e19e01d117055130da6201ac001311fd41d2"


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
    assert gate["four_way_equal"] is True
    assert gate["source_to_evidence_commits"] == 2
    assert gate["source_to_evidence_merges"] == 0


def test_phase_final_truth_and_outcomes() -> None:
    truth = load(FINAL / "phase-final.json")
    assert truth["proposal_chain"] == 6550
    assert truth["outcomes"] == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }
    assert truth["effective_counts"] == {
        "effective_negatives": 37803,
        "effective_methods": 24230,
        "effective_failed_witnesses": 9464,
        "effective_passing_witnesses": 11841,
        "open_gaps": 307,
        "exact_gates": 300,
    }
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["complete_repository_suite"] is False
    assert truth["independent_reproduction"] is False


def test_post_evidence_failures_are_additive() -> None:
    overlay = load(FINAL / "failure-overlay.json")
    assert overlay["post_evidence_failure_count"] == 4
    assert overlay["repository_seal_rewritten"] is False
    assert all(row["state"] == "failed_retained_zero_credit" for row in overlay["post_evidence_failures"])
    assert all(row["passing_bounded_witness"] is True for row in overlay["post_evidence_failures"])


def test_completion_checklist_preserves_terminal_gate() -> None:
    checklist = load(FINAL / "completion-checklist.json")
    assert checklist["passed"] == 12
    assert checklist["failed"] == 0
    assert checklist["canonical_terminal_gate_pending"] is True


def test_activation_candidate_and_route_state() -> None:
    route = load(FINAL / "route-state.json")
    path = ROOT / route["baton_path"]
    text = path.read_text(encoding="utf-8")
    words = re.findall(r"\b\w+(?:[-']\w+)*\b", text)
    assert route["target_exact_title"] == "Auren Lark"
    assert route["target_phase"] == "v674-v1"
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["send_attempts"] == 0
    assert route["precontact"] is False
    assert route["terminal_gate_required"] is True
    assert route["baton_words"] == len(words)
    assert route["baton_words"] >= 1000
    assert route["baton_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert "SENT_BY_ILYRA_FEN remains false" in text


def test_closeout_is_substantive_and_bounded() -> None:
    text = (FINAL / "closeout.md").read_text(encoding="utf-8")
    words = re.findall(r"\b\w+(?:[-']\w+)*\b", text)
    assert 350 <= len(words) <= 3000
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "independent reproduction" in text


def test_final_content_seal_replays() -> None:
    seal = load(FINAL / "content-seal.json")
    assert seal["source"] == SOURCE
    assert seal["x1_commit"] == X1_COMMIT
    assert seal["evidence_commit"] == EVIDENCE_COMMIT
    assert seal["self_excluded"] is True
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
        blob = subprocess.check_output(
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


def test_all_current_phase_json_is_strictly_parseable() -> None:
    paths = sorted(BASE.rglob("*.json"))
    assert len(paths) >= 100
    for path in paths:
        load(path)
