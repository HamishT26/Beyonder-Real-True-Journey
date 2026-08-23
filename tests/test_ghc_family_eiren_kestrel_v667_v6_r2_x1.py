from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "eiren-kestrel" / "v667-v6-r2"
BUILDER_PATH = ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_r2_x1.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("eiren_v667_v6_r2_x1", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def test_builder_self_validation_passes() -> None:
    receipt = load_builder().validate_tree()
    assert receipt["status"] == "PASS"
    assert receipt["x2_paths"] == 0
    assert receipt["overview_words"] >= 900


def test_phase_charter_binds_exact_source_and_boundary() -> None:
    charter = load("x1/phase-charter.json")
    assert charter["source_final"] == "1a754e02bfc705d738285c4a6cf9ce1c948a8580"
    assert charter["source_x1"] == "38aa1b783fd016134b46607894d16e56e5ccac99"
    assert charter["source_evidence"] == "8d7ff4b6938b783d23e4ce880ffed8d5fd7f9e59"
    assert charter["source_parent"] == "af68b8bdf317317fb349388f905d73862a9ea1b8"
    assert charter["x1_planning_only"] is True
    assert charter["outcomes_observed"] is False
    assert charter["x2_implementation_count"] == 0
    assert charter["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_source_validation_truth_preserves_canonical_and_unsent_route_overlay() -> None:
    source = load("x1/source-verification.json")
    assert source["canonical_invocation"]["invoked"] == 1
    assert source["canonical_invocation"]["succeeded"] == 1
    assert source["canonical_invocation"]["credit"] == 1
    assert source["canonical_invocation"]["replayed"] is False
    assert source["post_final_route_overlay"]["attempt_count"] == 3
    assert source["post_final_route_overlay"]["send_attempted"] is False
    assert source["post_final_route_overlay"]["acknowledged"] is False
    assert source["manifests_replayed"]["total"] == 844
    assert source["manifests_replayed"]["mismatches"] == 0


def test_novelty_audit_covers_all_4470_rows() -> None:
    novelty = load("x1/novelty-audit.json")
    assert novelty["valid"] is True
    assert novelty["corpus_row_count"] == 4470
    assert novelty["new_proposal_count"] == 20
    assert novelty["new_frozen_total"] == 4490
    assert novelty["exact_title_collisions"] == []
    assert novelty["pair_collisions_at_or_above_threshold"] == []
    assert novelty["domain_review"]["domain_term_match_count"] == 0
    assert novelty["maximum_inherited_similarity"] < 0.6
    assert len(novelty["nearest_inherited_matches"]) == 20


def test_program_freezes_twenty_new_and_twenty_zero_credit_inherited() -> None:
    freeze = load("x1/proposal-freeze.json")
    assert len(freeze["new_proposals"]) == 20
    assert len(freeze["selected_inherited"]) == 20
    assert len({row["proposal_id"] for row in freeze["new_proposals"]}) == 20
    assert Counter(row["expected_disposition"] for row in freeze["new_proposals"]) == Counter(
        {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    )
    assert all(row["outcomes_observed"] is False for row in freeze["new_proposals"])
    assert all(row["x2_implementation_count"] == 0 for row in freeze["new_proposals"])
    assert all(len(row["preregistered_mutations"]) == 5 for row in freeze["new_proposals"])
    assert all(row["eiren_novelty_credit"] == 0 for row in freeze["selected_inherited"])
    assert all(row["eiren_completion_credit"] == 0 for row in freeze["selected_inherited"])
    assert all(row["automatic_completion_credit"] == 0 for row in freeze["selected_inherited"])


def test_only_four_core_outcomes_are_used() -> None:
    freeze = load("x1/proposal-freeze.json")
    assert freeze["allowed_core_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"]
    assert set(row["expected_disposition"] for row in freeze["new_proposals"]) <= set(freeze["allowed_core_outcomes"])


def test_each_new_proposal_has_required_fields_and_zero_real_rows() -> None:
    freeze = load("x1/proposal-freeze.json")
    required = {
        "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
        "execution_lane", "current_official_or_primary_source_needs", "concrete_artifacts",
        "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
        "expected_disposition", "distinctive_invariant",
    }
    for row in freeze["new_proposals"]:
        assert required <= set(row)
        assert row["real_data_rows_planned"] == 0
        assert row["participant_count_planned"] == 0
        assert row["network_calls_planned"] == 0
        assert row["protected_gates"]


def test_portfolio_counts_and_zero_outcomes() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    expected = {
        "owner_safe_now": 30,
        "successor_safe_now_recommendations": 20,
        "owner_candidates": 15,
        "successor_candidate_recommendations": 15,
        "owner_skill_ideas": 10,
        "successor_skill_recommendations": 10,
        "owner_runner_ideas": 10,
        "successor_runner_recommendations": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine_recommendations": 30,
        "exact_approval_packets": 10,
        "blocked_packets": 5,
    }
    assert {key: len(portfolio[key]) for key in expected} == expected
    assert portfolio["outcomes_observed"] is False
    assert portfolio["x2_implementation_count"] == 0
    assert all(row["outcomes_observed"] is False for key in expected for row in portfolio[key])


def test_exact_and_blocked_packets_remain_unexecuted() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    assert all(row["x1_status"] == "planned_not_executed" for row in portfolio["exact_approval_packets"])
    assert all(row["x1_status"] == "planned_not_executed" for row in portfolio["blocked_packets"])
    assert all(row["expected_disposition"] == "exact_gate" for row in portfolio["exact_approval_packets"])
    assert all(row["expected_disposition"] == "exact_gate" for row in portfolio["blocked_packets"])


def test_thirteen_tools_are_planned_but_not_downloaded_installed_or_used() -> None:
    tools = load("x1/toolchain-install-plan.json")
    assert tools["new_tool_program_target"] == 13
    assert len(tools["new_tools"]) == 13
    assert {row["tool"] for row in tools["new_tools"]} == {
        "validate-pyproject", "pyproject-fmt", "deptry", "vulture", "radon", "xenon",
        "codespell", "yamllint", "toml-sort", "pip-licenses", "cyclonedx-bom",
        "check-manifest", "twine",
    }
    assert tools["x1_download_count"] == 0
    assert tools["x1_install_count"] == 0
    assert tools["x1_smoke_count"] == 0
    assert all(len(row["sha256"]) == 64 for row in tools["new_tools"])
    assert all(row["x1_status"] == "planned_not_downloaded_not_installed_not_used" for row in tools["new_tools"])


def test_all_mandatory_skills_were_read_and_used_before_mutation() -> None:
    adoption = load("x1/mandatory-skill-adoption.json")
    assert adoption["required_count"] == 21
    assert len(adoption["skills"]) == 21
    assert all(row["entrypoint_read_through_eof"] for row in adoption["skills"])
    assert all(row["required_references_read_through_eof"] for row in adoption["skills"])
    assert all(row["used_before_mutation"] for row in adoption["skills"])


def test_route_is_current_owner_only_and_unsent() -> None:
    route = load("x1/auth-roster-receipt.json")
    assert route["current_owner"] == "Eiren Kestrel"
    assert route["current_phase"] == "v667-v6-r2"
    assert route["prospective_terminal_successor"] == "Elaren Kestrel v667-v7"
    assert route["successor_contact_authorized_during_execution"] is False
    assert route["standby_contacted"] is False
    assert route["task_created_or_forked"] is False
    assert route["subagent_spawned"] is False


def test_x1_contains_no_later_lifecycle_directory() -> None:
    for name in ("x2", "evidence", "closeout", "seal", "route"):
        assert not (PHASE_ROOT / name).exists()


def test_content_manifest_replays_exact_working_tree_bytes() -> None:
    manifest = load("validation/x1-content-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        data = (ROOT / row["path"]).read_bytes()
        import hashlib

        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_overview_is_three_page_equivalent_and_preserves_boundaries() -> None:
    text = (PHASE_ROOT / "x1/x1-overview.md").read_text(encoding="utf-8")
    assert len(text.split()) >= 900
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "downloads and installs nothing" in text
    assert "no successor" in text.casefold()
    assert "Māori authority remain with Māori authority" in text


def test_every_phase_json_document_parses() -> None:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(paths) >= 17
    for path in paths:
        assert isinstance(json.loads(path.read_text(encoding="utf-8")), dict)
