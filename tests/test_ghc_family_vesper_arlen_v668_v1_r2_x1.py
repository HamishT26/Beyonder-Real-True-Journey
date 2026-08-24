from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v668-v1-r2"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def test_source_and_lifecycle_are_exact_and_planning_only() -> None:
    intake = load("x1/source-intake.json")
    truth = load("x1/phase-truth.json")
    assert intake["source_anchors"]["source_final"] == "d3fd3065a4570046335689c62af8faf636be7a86"
    assert intake["source_phase_mutated"] is False
    assert intake["source_completion_credit_to_remaster"] == 0
    assert truth["x2_implementation_present"] is False
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_proposal_chain_coverage_is_truthful() -> None:
    audit = load("x1/proposal-chain-audit.json")
    assert audit["declared_inherited_chain_count"] == 4590
    assert audit["freeze_blob_count"] >= 54
    assert audit["unique_id_count"] >= 1320
    assert audit["selected_count"] == 20
    assert audit["selected_novelty_credit"] == 0
    assert audit["compressed_title_gap_count_minimum"] > 0
    assert audit["coverage_state"].endswith("OPEN_GAP")


def test_exactly_forty_new_proposals_and_four_labels() -> None:
    freeze = load("x1/proposal-freeze.json")
    proposals = freeze["new_proposals"]
    assert len(proposals) == 40
    assert freeze["total_review_records"] == 60
    assert freeze["new_frozen_total"] == 4630
    assert freeze["negative_mutation_count"] == 160
    assert freeze["visible_title_collision_count"] == 0
    assert Counter(row["expected_disposition"] for row in proposals) == Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    assert set(freeze["allowed_outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"}
    assert all(row["x1_planning_only"] and row["x2_execution_count"] == 0 for row in proposals)
    required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
    assert all(required <= set(row) for row in proposals)


def test_expanded_portfolio_floors_and_successor_zero_credit() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    assert len(portfolio["owner_safe_now"]) == 60
    assert len(portfolio["owner_candidates"]) == 30
    assert len(portfolio["exact_approval_packets"]) == 20
    assert len(portfolio["blocked_packets"]) == 10
    assert len(portfolio["owner_skills"]) == 20
    assert len(portfolio["owner_runners"]) == 10
    assert len(portfolio["owner_clean_fix_refine"]) == 60
    successor = portfolio["successor_recommendations"]
    assert len(successor["candidates"]) == 15
    assert len(successor["skills"]) == 10
    assert len(successor["runners"]) == 10
    assert len(successor["clean_fix_refine"]) == 30
    assert successor["safe_now_recommendation_count"] == 0
    assert successor["completion_credit_to_vesper"] == 0


def test_three_practices_and_single_successor_practice() -> None:
    practices = load("x1/practice-and-pillar-freeze.json")
    assert practices["primary_pillar"] == "Freed ID and CBR Heart"
    assert practices["practice_count"] == 3
    assert len(practices["bounded_practices"]) == 3
    assert isinstance(practices["successor_practice_recommendation"], str)
    assert practices["real_people_or_collections_used"] is False


def test_thirteen_tool_pins_are_planning_only() -> None:
    plan = load("x1/toolchain-plan.json")
    assert plan["special_addition_count"] == 13
    assert len(plan["tools"]) == 13
    assert len({(row["ecosystem"], row["package"]) for row in plan["tools"]}) == 13
    assert all(row["state"] == "planned_not_installed" and row["x1_execution_count"] == 0 for row in plan["tools"])
    assert plan["D_isolated"] is True
    assert plan["npm_install_scripts_disabled"] is True


def test_route_keeps_sylven_and_does_not_consume_v668_v2() -> None:
    route = load("x1/route-auth-roster-freeze.json")
    assert len(route["cycle_order"]) == 15
    assert route["cycle_order"][13] == "Sylven Arc"
    assert route["cycle_order"][14] == "Caelen Morrow"
    assert route["current_variant"].startswith("v668-v1-r2")
    assert route["canonical_next_phase_unchanged"] == "v668-v2"
    assert route["immediate_edge_after_terminal_gate"] == {"from": "Vesper Arlen", "to": "Lyren Moss", "phase": "v668-v2"}
    assert route["precontact_permitted"] is False


def test_method_flow_retains_failed_and_passing_witnesses() -> None:
    flow = load("method-flow/startup-and-x1.json")
    assert flow["validation_scope"] == "owner_self_scoped_delta"
    assert flow["repository_wide_validation"] is False
    assert flow["cross_lane_validation"] is False
    assert flow["failure_count"] == len(flow["failures"])
    assert flow["passing_witness_count"] == flow["failure_count"]
    assert all(row["credit"] == 0 and row["passing_witness"] for row in flow["failures"])


def test_x1_manifest_matches_exact_x1_git_blobs() -> None:
    manifest = load("x1/manifest.json")
    self_path = "docs/vesper-arlen/v668-v1-r2/x1/manifest.json"
    x1_head = "be908eb829185971c10be6d100c2c85fd35871e0"
    tree = subprocess.run(
        ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", x1_head, "docs/vesper-arlen/v668-v1-r2"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    expected = {}
    for relative in sorted(path for path in tree if path != self_path):
        data = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{x1_head}:{relative}"],
            check=True,
            capture_output=True,
        ).stdout
        expected[relative] = (hashlib.sha256(data).hexdigest(), len(data))
    actual = {row["path"]: (row["sha256"], row["bytes"]) for row in manifest["entries"]}
    assert actual == expected
    assert manifest["self_exclusions"] == [self_path]


def test_every_phase_document_is_below_word_cap() -> None:
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".json", ".html"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100_000
