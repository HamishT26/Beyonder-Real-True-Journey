from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v673-v8"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "c1818f0c09737c69a1870ef6bf8ed7fc339cb727"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_bytes(spec: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", spec], cwd=ROOT)


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_exact_source_head_and_branch() -> None:
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == SOURCE
    assert subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip() == "codex/GHC-Family/ilyra-fen-v673-v8-full-tools"


def test_x1_is_planning_only_and_x2_absent() -> None:
    assert X1.is_dir()
    assert not (BASE / "x2").exists()
    assert not any("x2" in path.relative_to(BASE).parts for path in X1.rglob("*"))


def test_proposal_freeze_and_allowed_labels() -> None:
    payload = load(X1 / "proposals.json")
    rows = payload["proposals"]
    assert payload["declared_chain_before"] == 6510
    assert payload["declared_chain_after"] == 6550
    assert len(rows) == 40
    assert len({row["title"] for row in rows}) == 40
    assert {row["planned_disposition"] for row in rows} == {"completed", "represented", "open_gap", "exact_gate"}
    assert all(row["x1_state"] == "frozen_not_executed" for row in rows)


def test_planned_outcome_distribution() -> None:
    payload = load(X1 / "portfolio-freeze.json")
    assert payload["planned_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert payload["x2_outcomes_claimed"] is False


def test_inherited_revalidations_zero_credit() -> None:
    payload = load(X1 / "inherited-revalidations.json")
    assert payload["count"] == 20 == len(payload["rows"])
    assert all(row["ilyra_novelty_credit"] == 0 and row["ilyra_completion_credit"] == 0 for row in payload["rows"])


def test_semantic_audit_preserves_universal_gap() -> None:
    payload = load(X1 / "semantic-neighbor-audit.json")
    assert payload["accessible_predecessor_titles"] == 40
    assert payload["unmapped_declared_inherited_rows"] == 6470
    assert payload["universal_novelty_claimed"] is False
    assert payload["max_predecessor_jaccard"] < payload["quarantine_threshold"]
    assert payload["max_within_slate_jaccard"] < payload["quarantine_threshold"]


def test_approval_packet_counts_and_holds() -> None:
    payload = load(X1 / "approval-split.json")
    assert len(payload["safe_now"]) == 60
    assert len(payload["candidates"]) == 30
    assert len(payload["exact_approval"]) == 20
    assert len(payload["blocked"]) == 10
    assert all(row["state"] == "held_exact_approval_required" for row in payload["exact_approval"])
    assert all(row["state"] == "blocked_unexecuted" for row in payload["blocked"])


def test_skill_runner_and_successor_floors() -> None:
    payload = load(X1 / "skill-runner-plan.json")
    assert len(payload["owner_skills"]) == 20
    assert len(payload["owner_runners"]) == 10
    assert len(payload["successor"]["skills"]) == 10
    assert len(payload["successor"]["runners"]) == 10
    assert len(payload["successor"]["clean_fix_refine"]) == 30
    assert payload["successor"]["execution_credit"] == 0


def test_clean_fix_refine_floor() -> None:
    payload = load(X1 / "clean-fix-refine-plan.json")
    assert len(payload["owner_reviews"]) == 60
    assert all(row["deletion"] is False for row in payload["owner_reviews"])


def test_practice_lenses_are_synthetic() -> None:
    payload = load(X1 / "practice-lens-screen.json")
    assert len(payload["lenses"]) == 3
    assert payload["real_objects_or_people"] == 0
    assert "loom pattern-chain" in payload["practice"]


def test_startup_failures_retained() -> None:
    payload = load(X1 / "method-flow-startup.json")
    assert payload["startup_failure_count"] == 14 == len(payload["methods"])
    assert payload["failures_erased"] == 0
    assert all(row["credit"] == 0 and row["state"] == "preferred" for row in payload["methods"])
    assert len({row["failure_signature"] for row in payload["methods"]}) == 14


def test_source_truth_and_activation_overlay_are_separate() -> None:
    payload = load(X1 / "source-and-provenance.json")
    assert payload["source_final"] == SOURCE
    assert payload["source_repository_counts"]["negatives"] == 37613
    assert payload["activation_overlay"]["negatives"] == 37616
    assert payload["source_manifest_entries_reverified"] == 225
    assert payload["source_validation_inherited_without_replay"] is True


def test_route_is_prospective_and_unsent() -> None:
    payload = load(X1 / "route-plan.json")
    assert payload["prospective_exact_title"] == "Auren Lark"
    assert payload["prospective_phase"] == "v674-v1"
    assert payload["precontact_performed"] is False
    assert payload["send_attempts"] == 0
    assert payload["tavian_state"] == "ON_STANDBY"


def test_privacy_receipt_has_five_classes_and_zero_hits() -> None:
    payload = load(VALIDATION / "x1-staged-privacy.json")
    assert len(payload["classes"]) == 5
    assert len(payload["candidates"]) == 1
    assert len(payload["reviewed_false_positives"]) == 1
    assert payload["confirmed_hits"] == []
    assert payload["complete_privacy_assurance"] is False


def test_staged_review_excludes_x2_and_deletions() -> None:
    payload = load(VALIDATION / "x1-staged-review.json")
    assert payload["x2_paths"] == 0
    assert payload["deletions"] == 0
    assert payload["source_or_sibling_mutations"] == 0


def test_phase_boundary_language() -> None:
    text = (X1 / "phase-boundaries.md").read_text(encoding="utf-8")
    assert "relational working language only" in text
    assert "NOT_READY" not in text
    assert "independent reproduction" in text
    assert "Maori-authority" in text


def test_integrated_overview_has_ten_sections_and_terminal_verdict() -> None:
    text = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
    assert text.count("\n## ") == 11
    assert "NOT_READY_FOR_STAGE_20" in text
    assert len(text.split()) >= 700


def test_exact_index_manifest_replays() -> None:
    payload = load(VALIDATION / "x1-manifest.json")
    assert payload["source_final"] == SOURCE
    assert payload["entry_count"] == len(payload["entries"])
    assert payload["entry_count"] >= 20
    assert payload["self_exclusions"] == ["docs/ilyra-fen/v673-v8/validation/x1-manifest.json"]
    for entry in payload["entries"]:
        blob = normalized(git_bytes(f":{entry['path']}"))
        assert len(blob) == entry["bytes"]
        assert hashlib.sha256(blob).hexdigest() == entry["sha256_normalized_lf"]


def test_only_owner_x1_paths_are_staged() -> None:
    paths = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).splitlines()
    assert paths
    assert not any("/x2/" in path for path in paths)
    assert all(
        path.startswith("docs/ilyra-fen/v673-v8/")
        or path in {"scripts/build_ghc_family_ilyra_fen_v673_v8_x1.py", "tests/test_ghc_family_ilyra_fen_v673_v8_x1.py"}
        for path in paths
    )
