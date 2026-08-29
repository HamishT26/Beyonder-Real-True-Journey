from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v675-v8"
FINAL = BASE / "final"
VALIDATION = BASE / "validation"
SOURCE = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
X1_COMMIT = "e839cf0159f43d62cc34086c75fc934970765239"
EVIDENCE_COMMIT = "557f54729be94db41e927adcb43da6699e6d5bb1"
BRANCH = "codex/GHC-Family/auren-lark-v675-v8-full-tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def current_delta() -> set[str]:
    head = git("rev-parse", "HEAD")
    if head == EVIDENCE_COMMIT:
        return set(git("diff", "--cached", "--name-only").splitlines())
    assert git("rev-parse", "HEAD^") == EVIDENCE_COMMIT
    return set(git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines())


def test_evidence_terminal_gate_and_exact_ancestry() -> None:
    gate = load(FINAL / "evidence-terminal-gate.json")
    assert gate["head"] == gate["local"] == gate["upstream"] == gate["tracking"] == gate["fresh_live_remote"] == EVIDENCE_COMMIT
    assert gate["parent"] == X1_COMMIT and gate["grandparent"] == SOURCE
    assert gate["all_equal"] and gate["ahead"] == gate["behind"] == 0
    assert gate["evidence_manifest_replay"]["mismatches"] == []
    assert gate["owner_manifest_replay"]["mismatches"] == []


def test_final_truth_and_exact_outcomes() -> None:
    data = load(FINAL / "phase-truth.json")
    assert data["truth"] == {"effective_negatives": 41471, "methods": 30602, "failed_witnesses": 13132, "bounded_passing_witnesses": 17699, "open_gaps": 346, "exact_gates": 338, "declared_proposals": 7370, "verdict": "NOT_READY_FOR_STAGE_20"}
    assert data["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    assert data["source_seal_rewritten"] is False
    summary = load(FINAL / "outcome-summary.json")
    assert Counter(row["outcome"] for row in summary["rows"]) == Counter(data["outcomes"])


def test_retained_failures_remain_zero_credit() -> None:
    data = load(BASE / "closeout" / "retained-negative-register.json")
    assert data["phase_failed_witness_count"] == len(data["rows"]) == 181
    assert data["all_zero_credit"] is True
    assert data["effective_failed_witnesses"] == 13132
    assert any(row["reference"] == "AL6758-OP-019" for row in data["rows"])
    assert any(row["reference"] == "AL6758-OP-020" for row in data["rows"])
    assert any(row["reference"] == "AL6758-OP-021" for row in data["rows"])


def test_completion_checklist_preserves_incomplete_terminal_gates() -> None:
    data = load(BASE / "closeout" / "complete-incomplete-checklist.json")
    assert "independent reproduction" in data["incomplete_or_gated"]
    assert "full repository suite" in data["incomplete_or_gated"]
    assert "Stage 20" in data["incomplete_or_gated"]
    assert data["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_source_to_final_history_plan_is_direct_and_merge_free() -> None:
    data = load(BASE / "closeout" / "source-to-final-history-plan.json")
    assert data["source"] == SOURCE and data["x1"] == X1_COMMIT and data["evidence"] == EVIDENCE_COMMIT
    assert data["required_source_to_final_commits"] == 3
    assert data["required_merge_count"] == 0 and data["required_final_parent"] == EVIDENCE_COMMIT


def test_activation_candidate_is_long_sanitized_and_prepared_not_sent() -> None:
    path = BASE / "handoffs" / "sable-rook-v676-v1-activation-candidate.md"
    text = path.read_text(encoding="utf-8")
    route = load(BASE / "route" / "prepared-route-state.json")
    assert len(text.split()) >= 10000
    assert len(text.split()) < 100000
    assert route["candidate_words"] == len(text.split())
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_title"] == "Sable Rook" and route["successor_phase"] == "v676-v1"
    assert route["successor_after_current_title"] == "Caelen Ash" and route["successor_after_current_phase"] == "v676-v2"
    assert route["precontacted"] is route["sent"] is False
    assert route["task_identifier_stored"] is False
    assert "PREPARED_BY_AUREN_LARK = true" in text
    assert "SENT_BY_AUREN_LARK = false" in text
    assert "Do not precontact Caelen Ash" in text


def test_content_seal_replays_normalized_lf() -> None:
    data = load(BASE / "seal" / "content-seal.json")
    assert data["entry_count"] == len(data["entries"])
    for row in data["entries"]:
        blob = normalized((ROOT / row["path"]).read_bytes())
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_final_delta_manifest_replays() -> None:
    data = load(VALIDATION / "final-delta-manifest.json")
    for row in data["entries"]:
        blob = normalized((ROOT / row["path"]).read_bytes())
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_final_owner_manifest_replays() -> None:
    data = load(VALIDATION / "final-owner-manifest.json")
    assert data["entry_count"] == len(data["entries"])
    for row in data["entries"]:
        blob = normalized((ROOT / row["path"]).read_bytes())
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_final_privacy_and_bounded_security_scans() -> None:
    privacy = load(VALIDATION / "final-privacy-scan.json")
    security = load(VALIDATION / "final-security-scan.json")
    assert privacy["confirmed_hit_count"] == 0 and privacy["confirmed_hits"] == []
    assert set(privacy["classes"]) == {"raw_identifier", "private_path", "credential", "contact", "network"}
    assert security["finding_count"] == 0 and security["findings"] == []
    assert security["checked_python_files"] >= 17


def test_final_delta_review_is_exact_with_no_deletions() -> None:
    review = load(VALIDATION / "final-staged-review.json")
    assert current_delta() == set(review["expected_after_seal_outputs"])
    assert review["deletion_count"] == 0 and review["foreign_owner_path_count"] == 0


def test_all_current_phase_json_parses_strictly() -> None:
    paths = sorted(BASE.rglob("*.json"))
    assert len(paths) >= 140
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_materialized_scope_and_commit_ceiling() -> None:
    files = [path for path in ROOT.rglob("*") if path.is_file() and path.name != ".git"]
    assert len(files) < 2000
    assert int(git("rev-list", "--count", f"{SOURCE}..HEAD")) <= 3
    assert len(git("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()) == 0


def test_validation_credit_is_bounded_same_owner_only() -> None:
    data = load(VALIDATION / "validation-credit.json")
    assert data["owner_scoped_same_infrastructure"] is True
    assert not any(data[key] for key in ["independent_reproduction", "external_audit", "production_certification", "complete_privacy_or_accessibility", "exhaustive_security", "stage20_evidence"])


def test_integrated_overview_has_ten_sections_and_terminal_boundaries() -> None:
    text = (FINAL / "integrated-overview.md").read_text(encoding="utf-8")
    assert text.count("\n## ") == 10
    for phrase in ["NOT_READY_FOR_STAGE_20", "complete repository suite", "independent reproduction", "Theory-of-Everything", "relational working language only"]:
        assert phrase in text


def test_canonical_plan_is_one_shot_and_not_full_repo() -> None:
    data = load(VALIDATION / "canonical-plan.json")
    assert data["invocation_limit"] == data["success_limit"] == 1
    assert data["post_success_replay"] is False
    assert data["full_repository_suite"] is False and data["independent_reproduction"] is False
