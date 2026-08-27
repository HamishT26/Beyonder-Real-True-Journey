from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "auren-lark" / "v672-v2"
CLOSEOUT = PHASE / "closeout"
VALIDATION = PHASE / "validation"
EVIDENCE = "e735ac99202e9ad69252ed39ce9eb41d684bf671"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_x1_and_x2_are_unchanged_after_evidence() -> None:
    changed = subprocess.check_output(
        ["git", "-C", str(ROOT), "diff", "--name-only", EVIDENCE], text=True
    ).splitlines()
    frozen_prefixes = (
        "docs/auren-lark/v672-v2/x1/",
        "docs/auren-lark/v672-v2/x2/",
    )
    frozen_exact = {
        "scripts/build_ghc_family_auren_lark_v672_v2_x1.py",
        "scripts/build_ghc_family_auren_lark_v672_v2_staged_review.py",
        "scripts/build_ghc_family_auren_lark_v672_v2_x2.py",
        "scripts/build_ghc_family_auren_lark_v672_v2_evidence_staged_review.py",
        "scripts/validate_ghc_family_auren_lark_v672_v2_x2.py",
        "tests/test_ghc_family_auren_lark_v672_v2_x1.py",
        "tests/test_ghc_family_auren_lark_v672_v2_x2.py",
    }
    assert not [
        path for path in changed if path.startswith(frozen_prefixes) or path in frozen_exact
    ]


def test_closeout_truth_preserves_counts_labels_and_verdict() -> None:
    truth = load(CLOSEOUT / "phase-truth.json")
    assert truth["state"] == "TERMINAL_CANDIDATE_PREPARED_NOT_COMMITTED"
    assert truth["route_state"] == "PREPARED_NOT_SENT"
    assert truth["planned_final_parent"] == EVIDENCE
    assert truth["commits_from_source_if_finalized"] == 3
    assert truth["merge_count_if_finalized"] == 0
    assert set(truth["outcomes"]) == ALLOWED
    assert truth["outcomes"] == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }
    assert truth["effective_counts"] == {
        "effective_negatives": 35268,
        "effective_methods": 21899,
        "effective_failed_witnesses": 7089,
        "effective_passing_witnesses": 9186,
        "open_gaps": 279,
        "exact_gates": 272,
    }
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_evidence_gate_and_manifest_replay_exact_git_blobs() -> None:
    gate = load(CLOSEOUT / "evidence-gate.json")
    assert gate["state"] == "VALID_IMMUTABLE_EVIDENCE_GATE"
    assert gate["evidence_commit"] == EVIDENCE
    assert gate["evidence_parent"] == "821a40be02af8db39524dc862aeaadf32e1543c3"
    assert gate["four_way_equal"] is True
    manifest = load(CLOSEOUT / "immutable-evidence-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"]) == 112
    for row in manifest["entries"]:
        blob_id = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", f"{EVIDENCE}:{row['path']}"],
            text=True,
        ).strip()
        blob = subprocess.check_output(["git", "-C", str(ROOT), "cat-file", "blob", blob_id])
        assert blob_id == row["git_blob"]
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_closeout_owner_manifest_matches_working_bytes() -> None:
    manifest = load(CLOSEOUT / "owner-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        data = (ROOT / row["path"]).read_bytes()
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_baton_integrity_word_bounds_and_privacy() -> None:
    integrity = load(CLOSEOUT / "handoff-integrity.json")
    baton_path = ROOT / integrity["path"]
    data = baton_path.read_bytes()
    text = data.decode("utf-8")
    words = len(re.findall(r"\S+", text))
    assert hashlib.sha256(data).hexdigest() == integrity["sha256"]
    assert words == integrity["words"]
    assert integrity["minimum_words"] <= words <= integrity["maximum_words"]
    assert integrity["target_exact_title"] == "Sable Rook"
    assert integrity["delivery_state"] == "PREPARED_NOT_SENT"
    patterns = [
        re.compile(r"\b019[a-f0-9]{5}-[a-f0-9-]{20,}\b"),
        re.compile(r"A" + r"KIA[0-9A-Z]{16}"),
        re.compile(r"gh" + r"p_[A-Za-z0-9]{20,}"),
        re.compile(r"BEGIN [A-Z ]*PRIVATE" + r" KEY"),
    ]
    assert not [pattern.pattern for pattern in patterns if pattern.search(text)]
    assert "SENT_BY_AUREN_LARK = false" in text
    assert "NOT_READY_FOR_STAGE_20" in text


def test_method_flow_retains_every_failure_and_no_replay() -> None:
    flow = load(CLOSEOUT / "method-flow-closeout.json")
    assert flow["x1_operational_failures"] == 12
    assert flow["x2_operational_failures"] == 3
    assert flow["invalid_mutations"] == 50
    assert [row["failure_id"] for row in flow["closeout_operational_failures"]] == [
        "AL6722-CLOSEOUT-001",
        "AL6722-CLOSEOUT-002",
    ]
    assert flow["failures_erased"] == 0
    assert flow["recoveries_relabelled_as_original_success"] == 0
    assert flow["runner_smoke_replayed"] is False


def test_validation_scope_and_terminal_checklist_are_exact() -> None:
    scope = load(CLOSEOUT / "validation-scope.json")
    checklist = load(CLOSEOUT / "terminal-checklist.json")
    assert scope["run_after_clean_pushed_final_only"] is True
    assert scope["canonical_success_ceiling"] == 1
    assert scope["replay_after_success"] is False
    assert scope["complete_repository_suite"] is False
    assert scope["independent_reproduction"] is False
    assert all(checklist["checks"].values())
    assert len(checklist["remaining_before_route"]) == 5


def test_route_remains_prepared_not_sent() -> None:
    route = load(CLOSEOUT / "route-candidate.json")
    assert route["target_exact_title"] == "Sable Rook"
    assert route["target_phase"] == "v672-v3"
    assert route["delivery_state"] == "PREPARED_NOT_SENT"
    assert route["send_count"] == 0
    assert route["precontacted"] is False
    assert route["task_created"] is False
    assert route["fork_created"] is False
    assert route["subagent_spawned"] is False


def test_final_staged_review_is_valid_when_present() -> None:
    path = VALIDATION / "final-staged-review.json"
    if not path.exists():
        return
    review = load(path)
    assert review["valid"] is True
    assert review["deletions"] == []
    assert review["out_of_scope"] == []
    assert review["frozen_x1_x2_mutations"] == []
    assert review["confirmed_privacy_candidates"] == []
    assert review["bounded_changed_python_security_findings"] == []
    assert review["immutable_evidence_mismatches"] == []
    assert review["closeout_manifest_mismatches"] == []
    assert review["baton_valid"] is True


def test_canonical_validator_and_terminal_report_are_present() -> None:
    validator = ROOT / "scripts" / "validate_ghc_family_auren_lark_v672_v2_final.py"
    report = (CLOSEOUT / "terminal-report.md").read_text(encoding="utf-8")
    assert validator.is_file()
    assert "NOT_READY_FOR_STAGE_20" in report
    assert "60/60" in report
    assert "not replayed" in report
