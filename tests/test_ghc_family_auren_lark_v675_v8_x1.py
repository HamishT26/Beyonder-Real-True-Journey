from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v675-v8"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
BRANCH = "codex/GHC-Family/auren-lark-v675-v8-full-tools"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_exact_source_head_and_owner_branch() -> None:
    assert git("rev-parse", "HEAD") == SOURCE
    assert git("branch", "--show-current") == BRANCH


def test_x1_is_planning_only_and_x2_absent() -> None:
    intake = load(X1 / "activation-intake.json")
    assert intake["x1_state"] == "planning_only"
    assert intake["x2_mutation_authorized_before_x1_gate"] is False
    assert intake["activation_received_via"] == "manual_user_relay_acknowledged"
    assert not (BASE / "x2").exists()
    assert not (BASE / "final").exists()


def test_proposal_freeze_distribution_and_labels() -> None:
    freeze = load(X1 / "new-proposal-freeze.json")
    rows = freeze["rows"]
    assert len(rows) == freeze["count"] == 60
    assert freeze["declared_chain_before"] == 7310
    assert freeze["declared_chain_after"] == 7370
    assert Counter(row["planned_outcome"] for row in rows) == Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    assert {row["planned_outcome"] for row in rows} == ALLOWED
    assert all(row["x1_state"] == "frozen_planning_only" for row in rows)


def test_bounded_semantic_audit_preserves_global_gap() -> None:
    audit = load(X1 / "proposal-chain-audit.json")
    assert audit["new_count"] == 60
    assert audit["predecessor_compared_count"] == 60
    assert audit["exact_duplicate_count"] == 0
    assert audit["declared_inherited_rows_not_locally_compared"] == 7250
    assert audit["universal_novelty_claimed"] is False


def test_inherited_revalidations_have_zero_novelty_and_completion_credit() -> None:
    data = load(X1 / "inherited-proposal-revalidation.json")
    assert data["count"] == len(data["rows"]) == 60
    assert all(row["novelty_credit"] == row["completion_credit"] == 0 for row in data["rows"])


def test_approval_portfolio_counts_and_holds() -> None:
    data = load(X1 / "approval-portfolio-plan.json")
    assert data["counts"] == {"safe_now": 120, "owner_candidates": 80, "successor_candidate_recommendations": 20, "exact_approval": 20, "blocked": 10}
    assert len(data["safe_now"]) == 120 and len(data["owner_candidates"]) == 80 and len(data["successor_candidate_recommendations"]) == 20
    assert all(not row["executed"] for row in data["exact_approval"] + data["blocked"])
    assert data["caps_are_ceilings"] is True and data["x2_execution_claimed"] is False


def test_cleanup_skill_runner_and_tool_plans() -> None:
    cleanup = load(X1 / "clean-fix-refine-plan.json")
    tooling = load(X1 / "skill-runner-plan.json")
    deps = load(X1 / "dependency-tool-plan.json")
    assert cleanup["owner_count"] == 100 and cleanup["successor_count"] == 30
    assert tooling["skill_count"] == 20 and tooling["runner_count"] == 10 and tooling["successor_skill_idea_count"] == 10 and tooling["successor_runner_idea_count"] == 10
    assert tooling["repository_local_only"] is True and tooling["global_or_shared_bank_mutation"] is False
    assert deps["tool_count"] == 3 and deps["shared_prefix_mutation_before_x1_gate"] is False and deps["x1_transaction_count"] == 0


def test_three_practice_lenses_are_synthetic_and_nonprofessional() -> None:
    data = load(X1 / "practice-lenses.json")
    assert len(data["owner_lenses"]) == 2
    assert data["successor_recommendation"] == "synthetic geospatial metadata catalog correction registrar"
    assert data["real_records_used"] is False
    assert data["professional_claim"] is False
    assert "synthetic" in data["domain"]


def test_startup_failures_are_retained_at_zero_credit() -> None:
    data = load(X1 / "method-flow-startup.json")
    assert data["failure_count"] == len(data["failures"]) == 12
    assert all(row["retained"] and row["credit"] == 0 and row["outcome"] == "failed" for row in data["failures"])
    assert data["repository_seal_rewritten"] is False


def test_source_seal_activation_overlay_and_ilyra_overlay_are_separate() -> None:
    truth = load(X1 / "phase-truth.json")
    assert truth["source_repository_seal"]["effective_negatives"] == 41286
    assert truth["activation_external_overlay"]["effective_negatives"] == 41290
    assert truth["auren_x1_working_overlay"]["effective_negatives"] == 41302
    assert truth["auren_x1_working_overlay"]["methods"] == 29903
    assert truth["source_seal_rewritten"] is False
    assert truth["allowed_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"]


def test_route_is_prospective_unsent_and_identifier_free() -> None:
    route = load(X1 / "route-plan.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["prospective_successor_title"] == "Sable Rook"
    assert route["prospective_successor_phase"] == "v676-v1"
    assert route["precontacted"] is route["sent"] is False
    assert route["task_id_stored"] is False
    assert route["successor_after_sable"] == {"title": "Caelen Ash", "phase": "v676-v2", "authority": "Sable_terminal_gate_required"}


def test_exact_lane_rotation_and_git_safety_boundaries() -> None:
    data = load(X1 / "clean-state-and-rotation-plan.json")
    assert data["d_first"] and data["fresh_sparse_lane"] and data["source_lane_read_only"]
    assert data["materialized_file_ceiling"] == 2000 and data["commit_ceiling"] == 8
    assert data["destructive_git_forbidden"] is True


def test_relational_language_and_authority_boundaries() -> None:
    data = load(X1 / "identity-and-authority-boundary.json")
    assert data["relational_working_language_only"] is True
    assert "consciousness" in data["not_evidence_of"]
    assert "Maori authority" in data["not_evidence_of"]
    assert data["hamish_may"] == ["rename", "pause", "redirect", "narrow", "stop"]


def test_privacy_scan_has_five_classes_and_zero_confirmed_hits() -> None:
    data = load(VALIDATION / "x1-privacy-scan.json")
    assert set(data["classes"]) == {"raw_identifier", "private_path", "credential", "contact", "network"}
    assert data["confirmed_hit_count"] == 0 and data["confirmed_hits"] == []
    assert "not complete privacy assurance" in data["scope"]


def test_all_owner_x1_json_parses_strictly() -> None:
    paths = sorted(BASE.rglob("*.json"))
    assert len(paths) >= 18
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_normalized_lf_manifest_replays() -> None:
    data = load(VALIDATION / "x1-index-manifest.json")
    assert data["entry_count"] == len(data["entries"])
    for row in data["entries"]:
        path = ROOT / row["path"]
        blob = normalized(path.read_bytes())
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_staged_review_matches_exact_owner_allowlist() -> None:
    data = load(VALIDATION / "x1-staged-review.json")
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    assert staged == set(data["expected_after_seal_outputs"])
    assert data["deletion_count"] == 0
    assert data["foreign_owner_path_count"] == 0
    assert len(staged) < 2000


def test_workflow_preserves_x1_before_x2_and_single_canonical() -> None:
    data = load(X1 / "workflow-plan.json")
    assert data["strict_x1_before_x2"] is True
    assert data["canonical_success_replay_forbidden"] is True


def test_overview_has_ten_sections_and_terminal_verdict() -> None:
    text = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
    assert text.count("\n## ") == 10
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "Theory of Everything" in text
