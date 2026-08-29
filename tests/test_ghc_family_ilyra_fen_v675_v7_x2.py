from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v675-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "7c60b4452d3b98a4bcdc9362eea35a4c07f4fe29"
X1_COMMIT = "88cc5a56ff27f9b3861d6f19963d1c0d1739bf58"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_x1_gate_was_exact_before_x2() -> None:
    gate = load(X2 / "x1-terminal-gate.json")
    assert gate["head"] == gate["local"] == gate["upstream"] == gate["tracking"] == gate["fresh_live_remote"] == X1_COMMIT
    assert gate["parent"] == SOURCE and gate["all_equal"] and gate["clean_before_x2_mutation"]
    assert gate["current_delta_authorized"] is True
    assert gate["ahead"] == gate["behind"] == 0
    assert git("rev-parse", "HEAD") == X1_COMMIT


def test_proposal_contracts_and_exact_distribution() -> None:
    paths = sorted((X2 / "proposal-contracts").glob("*.json"))
    rows = [load(path) for path in paths]
    assert len(rows) == 40
    assert Counter(row["outcome"] for row in rows) == Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    assert {row["outcome"] for row in rows} == ALLOWED
    assert sum(row["completion_credit"] for row in rows) == 28
    assert all(row["synthetic_only"] and not row["real_world_action"] for row in rows)


def test_outcomes_extend_chain_without_promoting_gaps_or_gates() -> None:
    freeze = load(X1 / "new-proposal-freeze.json")
    outcomes = load(X2 / "proposal-outcomes.json")
    assert freeze["declared_chain_after"] == 7310
    assert outcomes["distribution"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert outcomes["allowed_labels"] == ["completed", "represented", "open_gap", "exact_gate"]


def test_all_160_invalid_mutations_are_rejected_and_retained() -> None:
    rows = []
    for path in sorted((X2 / "invalid-mutations").glob("*.json")):
        rows.extend(load(path)["rows"])
    assert len(rows) == 160
    assert len({row["kind"] for row in rows}) == 16
    assert all(row["expected"] == "reject" and row["observed"] == "rejected" for row in rows)
    assert all(row["retained"] and row["credit"] == 0 for row in rows)


def test_forty_positive_controls_pass_boundedly() -> None:
    data = load(X2 / "positive-controls.json")
    assert data["count"] == len(data["rows"]) == 40
    assert all(row["passed"] and row["observed"] == "accepted_bounded_synthetic" for row in data["rows"])


def test_d_isolated_tools_have_exact_official_hashes_and_smoke_use() -> None:
    data = load(X2 / "tool-receipt.json")
    assert data["direct_tool_count"] == 3 and data["dependency_count"] == 2
    assert data["all_official_hashes_match"] is True
    assert all(row["actual_sha256"] == row["sha256"] for row in data["files"])
    assert data["smoke"]["pyyaml"] == "6.0.3"
    assert data["smoke"]["jsonpath_selected"] == ["datum"]
    assert data["smoke"]["deepdiff_nonempty"] is True
    assert data["shared_python_or_npm_prefix_mutated"] is False


def test_synthetic_practice_reconciles_and_quarantines_without_overwrite() -> None:
    data = load(X2 / "practice" / "reconciliation-output.json")
    assert data["reconciled_count"] == 2 and data["quarantined_count"] == 2
    assert data["source_overwrite_count"] == 0 and data["authority_promotions"] == 0
    assert data["selected_canonical_terms"] == ["datum_reference", "benchmark_reference", "unknown_quarantined", "unknown_quarantined"]
    boundary = load(X2 / "practice" / "boundary.json")
    assert boundary["real_people"] == boundary["real_places"] == boundary["real_records"] == boundary["real_measurements"] == 0
    assert boundary["external_actions"] == boundary["authority_decisions"] == 0


def test_phase_local_skills_and_runners_built_tested_and_used() -> None:
    receipt = load(X2 / "skill-runner-use-receipt.json")
    assert receipt["skill_count"] == 20 and receipt["runner_count"] == 10
    assert receipt["runner_self_tests_passed"] == 10
    assert receipt["repository_local_only"] and not receipt["global_installation"] and not receipt["shared_bank_mutation"]
    skills = list((X2 / "skills").glob("*/SKILL.md"))
    runners = list((X2 / "runners").glob("*.py"))
    assert len(skills) == 20 and len(runners) == 10
    for runner in runners:
        ast.parse(runner.read_text(encoding="utf-8"))


def test_approval_and_cleanup_portfolios_have_exact_dispositions() -> None:
    data = load(X2 / "portfolio-execution.json")
    assert data["counts"] == {"safe_now_completed": 60, "candidates_evaluated": 30, "exact_held": 20, "blocked_held": 10, "clean_fix_refine_completed": 60, "successor_recommendations": 30}
    assert data["exact_or_blocked_executed"] is False
    assert all(not row["executed"] for row in data["exact_approval"] + data["blocked"])
    assert data["caps_are_ceilings"] is True


def test_method_flow_retains_failures_and_exact_effective_counts() -> None:
    data = load(X2 / "method-flow.json")
    assert data["additive_methods"] == len(data["rows"]) == 466
    assert data["additive_failed_witnesses"] == 169
    assert data["additive_passing_witnesses"] == 297
    truth = data["effective_truth"]
    assert truth == {"effective_negatives": 41286, "methods": 29875, "failed_witnesses": 12947, "bounded_passing_witnesses": 17154, "open_gaps": 343, "exact_gates": 335, "declared_proposals": 7310, "verdict": "NOT_READY_FOR_STAGE_20"}
    failed = [row for row in data["rows"] if row["state"] == "failed"]
    assert all(row["credit"] == 0 for row in failed)


def test_open_gaps_and_exact_gates_remain_protected() -> None:
    gaps = load(X2 / "open-gap-register.json")
    gates = load(X2 / "exact-gate-register.json")
    assert gaps["new_count"] == 2 and gaps["effective_open_gaps"] == 343
    assert gates["new_count"] == 2 and gates["effective_exact_gates"] == 335
    assert all(row["state"] == "open_gap" for row in gaps["rows"])
    assert all(row["state"] == "exact_gate" for row in gates["rows"])


def test_route_remains_prepared_not_sent() -> None:
    route = load(X2 / "route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_title"] == "Auren Lark" and route["successor_phase"] == "v675-v8"
    assert route["precontacted"] is route["sent"] is False
    assert route["task_identifier_stored"] is False


def test_four_tier_flashcards_are_projection_only() -> None:
    data = load(X2 / "flashcards.json")
    assert len(data["tiers"]) == 4 and len(data["cards"]) == 40
    assert data["identity_or_memory_evidence"] is False
    assert all(row["projection_only"] for row in data["cards"])


def test_all_phase_json_parses_strictly() -> None:
    paths = sorted(BASE.rglob("*.json"))
    assert len(paths) >= 90
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_privacy_scan_has_zero_confirmed_five_class_hits() -> None:
    data = load(VALIDATION / "x2-privacy-scan.json")
    assert set(data["classes"]) == {"raw_identifier", "private_path", "credential", "contact", "network"}
    assert data["confirmed_hit_count"] == 0 and data["confirmed_hits"] == []
    assert "not complete privacy assurance" in data["scope"]


def test_bounded_python_security_scan_has_zero_findings() -> None:
    data = load(VALIDATION / "x2-security-scan.json")
    assert data["checked_python_files"] >= 14
    assert data["finding_count"] == 0 and data["findings"] == []
    assert "not exhaustive security" in data["scope"]


def test_evidence_manifest_replays_normalized_lf() -> None:
    data = load(VALIDATION / "x2-evidence-manifest.json")
    assert data["entry_count"] == len(data["entries"])
    for row in data["entries"]:
        blob = normalized((ROOT / row["path"]).read_bytes())
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_full_owner_manifest_replays_normalized_lf() -> None:
    data = load(VALIDATION / "x2-owner-manifest.json")
    assert data["entry_count"] == len(data["entries"])
    for row in data["entries"]:
        blob = normalized((ROOT / row["path"]).read_bytes())
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_staged_review_is_exact_owner_delta_with_no_deletions() -> None:
    data = load(VALIDATION / "x2-staged-review.json")
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    assert staged == set(data["expected_after_seal_outputs"])
    assert data["deletion_count"] == 0 and data["foreign_owner_path_count"] == 0
    assert len(staged) < 2000


def test_materialized_owner_scope_is_below_rotation_guard() -> None:
    files = [path for path in ROOT.rglob("*") if path.is_file() and path.name != ".git"]
    assert len(files) < 2000


def test_overview_preserves_all_terminal_boundaries() -> None:
    text = (X2 / "integrated-overview.md").read_text(encoding="utf-8")
    assert text.count("\n## ") == 10
    for phrase in ["NOT_READY_FOR_STAGE_20", "complete repository suite", "independent reproduction", "Theory-of-Everything", "relational working language only"]:
        assert phrase in text
