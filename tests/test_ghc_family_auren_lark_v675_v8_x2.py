from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v675-v8"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
X1_COMMIT = "e839cf0159f43d62cc34086c75fc934970765239"
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
    assert len(rows) == 60
    assert Counter(row["outcome"] for row in rows) == Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    assert {row["outcome"] for row in rows} == ALLOWED
    assert sum(row["completion_credit"] for row in rows) == 42
    assert all(row["synthetic_only"] and not row["real_world_action"] for row in rows)


def test_outcomes_extend_chain_without_promoting_gaps_or_gates() -> None:
    freeze = load(X1 / "new-proposal-freeze.json")
    outcomes = load(X2 / "proposal-outcomes.json")
    assert freeze["declared_chain_after"] == 7370
    assert outcomes["distribution"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    assert outcomes["allowed_labels"] == ["completed", "represented", "open_gap", "exact_gate"]


def test_sixty_inherited_rows_remain_zero_credit() -> None:
    data = load(X2 / "inherited-revalidation-results.json")
    assert data["count"] == len(data["rows"]) == 60
    assert data["novelty_credit"] == data["completion_credit"] == 0
    assert all(row["novelty_credit"] == row["completion_credit"] == 0 for row in data["rows"])


def test_all_160_invalid_mutations_are_rejected_and_retained() -> None:
    rows = []
    for path in sorted((X2 / "invalid-mutations").glob("*.json")):
        rows.extend(load(path)["rows"])
    assert len(rows) == 160
    assert len({row["kind"] for row in rows}) == 16
    assert all(row["expected"] == "reject" and row["observed"] == "rejected" for row in rows)
    assert all(row["retained"] and row["credit"] == 0 for row in rows)


def test_sixty_positive_controls_pass_boundedly() -> None:
    data = load(X2 / "positive-controls.json")
    assert data["count"] == len(data["rows"]) == 60
    assert all(row["passed"] and row["observed"] == "accepted_bounded_synthetic" for row in data["rows"])


def test_d_first_tools_have_exact_official_hashes_and_smoke_use() -> None:
    data = load(X2 / "tool-receipt.json")
    assert data["direct_transaction_count"] == 3 and data["dependency_count"] == 3
    assert data["all_official_python_hashes_match"] is True
    assert len(data["python_files"]) == 5
    assert all(row["actual_sha256"] == row["sha256"] for row in data["python_files"])
    assert data["smoke"] == {"deepdiff_nonempty": True, "jsonpatch_state": "bounded"}
    assert data["codex"]["installed_version"] == "0.151.0"
    assert data["codex"]["command_output"] == "codex-cli 0.151.0"
    assert data["codex"]["official_integrity_match"] is True
    assert data["codex"]["previous_version"] == "0.150.1"


def test_synthetic_practice_applies_patch_and_exact_rollback() -> None:
    data = load(X2 / "practice" / "drift-and-rollback-receipt.json")
    assert data["forward_operation_count"] == 4
    assert data["rollback_exact"] is True and data["baseline_preserved"] is True
    assert data["real_deployment"] is False and data["external_action"] is False
    assert data["authority_promotions"] == 0
    package = load(X2 / "practice" / "preservation-package-audit.json")
    assert package["entry_count"] == len(package["rows"]) == 3
    assert package["complete_package_claimed"] is package["legal_review_claimed"] is False
    boundary = load(X2 / "practice" / "boundary.json")
    for key in ["real_people", "real_organizations", "real_repositories", "real_services", "real_incidents", "real_deployments", "external_actions", "authority_decisions"]:
        assert boundary[key] == 0


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
    assert data["counts"] == {
        "safe_now_completed": 120, "owner_candidates_evaluated": 80,
        "successor_candidate_recommendations": 20, "exact_held": 20, "blocked_held": 10,
        "clean_fix_refine_completed": 100, "successor_clean_fix_refine": 30,
        "successor_skill_ideas": 10, "successor_runner_ideas": 10,
    }
    assert data["exact_or_blocked_executed"] is False and data["successor_rows_executed"] is False
    assert all(not row["executed"] for row in data["exact_approval"] + data["blocked"])
    assert all(not row["executed"] for row in data["successor_candidate_recommendations"])
    assert data["caps_are_ceilings"] is True


def test_method_flow_retains_failures_and_exact_effective_counts() -> None:
    data = load(X2 / "method-flow.json")
    assert data["additive_methods"] == len(data["rows"]) == 717
    assert data["additive_failed_witnesses"] == 178
    assert data["additive_passing_witnesses"] == 539
    truth = data["effective_truth"]
    assert truth == {"effective_negatives": 41468, "methods": 30596, "failed_witnesses": 13129, "bounded_passing_witnesses": 17696, "open_gaps": 346, "exact_gates": 338, "declared_proposals": 7370, "verdict": "NOT_READY_FOR_STAGE_20"}
    failed = [row for row in data["rows"] if row["state"] == "failed"]
    assert all(row["credit"] == 0 for row in failed)
    x2_failures = load(X2 / "x2-operational-failures.json")
    assert x2_failures["count"] == len(x2_failures["rows"]) == 6
    assert all(row["retained"] and row["credit"] == 0 for row in x2_failures["rows"])


def test_open_gaps_and_exact_gates_remain_protected() -> None:
    gaps = load(X2 / "open-gap-register.json")
    gates = load(X2 / "exact-gate-register.json")
    assert gaps["new_count"] == 3 and gaps["effective_open_gaps"] == 346
    assert gates["new_count"] == 3 and gates["effective_exact_gates"] == 338
    assert all(row["state"] == "open_gap" for row in gaps["rows"])
    assert all(row["state"] == "exact_gate" for row in gates["rows"])


def test_route_remains_prepared_not_sent() -> None:
    route = load(X2 / "route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_title"] == "Sable Rook" and route["successor_phase"] == "v676-v1"
    assert route["successor_after_sable"] == {"title": "Caelen Ash", "phase": "v676-v2", "requires": "Sable exact terminal gate"}
    assert route["precontacted"] is route["sent"] is False
    assert route["task_identifier_stored"] is False


def test_four_tier_flashcards_are_projection_only() -> None:
    data = load(X2 / "flashcards.json")
    assert len(data["tiers"]) == 4 and len(data["cards"]) == 60
    assert len(data["sections"]) >= 10
    assert data["identity_or_memory_evidence"] is False
    assert all(row["projection_only"] for row in data["cards"])


def test_all_phase_json_parses_strictly() -> None:
    paths = sorted(BASE.rglob("*.json"))
    assert len(paths) >= 110
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
    assert data["owner_manifest_excluded_to_avoid_cycle"].endswith("x2-owner-manifest.json")
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
