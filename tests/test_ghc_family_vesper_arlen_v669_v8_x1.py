"""Planning-only tests for Vesper Arlen v669-v8 x1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_vesper_arlen_v669_v8_sourdough import (
    CANDIDATE_TITLES,
    CHAIN_AFTER,
    OWNER_ROOT,
    PRACTICES,
    PROPOSAL_SPECS,
    PROTECTED_GATES,
    REFINE_TITLES,
    RUNNER_TITLES,
    SAFE_TITLES,
    SKILL_TITLES,
    SOURCE_CHAIN_DECLARED,
    SOURCE_RECOVERED,
    SUCCESSOR_REFINE,
    SUCCESSOR_RUNNERS,
    SUCCESSOR_SKILLS,
    TOOL_CANDIDATES,
    inherited_revalidations,
    inherited_title_corpus,
    proposal_rows,
)

X1 = ROOT / OWNER_ROOT / "x1"
VALIDATION = ROOT / OWNER_ROOT / "validation"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def all_new_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted((X1 / "proposal-freeze-shards").glob("*.json")):
        rows.extend(read_json(path)["rows"])
    return rows


def test_exact_accessible_corpus_and_revalidations() -> None:
    corpus, sources = inherited_title_corpus(ROOT)
    assert len(corpus) == SOURCE_RECOVERED == 1620
    assert len({row["proposal_id"] for row in corpus}) == 1620
    assert len(sources) >= 1
    selected = inherited_revalidations(corpus)
    assert len(selected) == 20
    assert all(row["completion_credit"] == row["current_novelty_credit"] == 0 for row in selected)


def test_new_proposal_contracts_are_distinct_and_unquarantined() -> None:
    corpus, _ = inherited_title_corpus(ROOT)
    rows = proposal_rows(corpus)
    assert len(rows) == len(PROPOSAL_SPECS) == 40
    assert len({row["proposal_id"] for row in rows}) == 40
    assert len({row["title"].lower() for row in rows}) == 40
    assert not [row for row in rows if row["visible_title_collision"]]
    assert not [row for row in rows if row["semantic_neighbor_quarantined"]]


def test_expected_truth_distribution_and_labels() -> None:
    rows = all_new_rows()
    counts = {label: sum(row["expected_disposition"] == label for row in rows) for label in ("completed", "represented", "open_gap", "exact_gate")}
    assert counts == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert not ({row["expected_disposition"] for row in rows} - set(counts))


def test_each_new_proposal_has_required_x1_fields() -> None:
    for row in all_new_rows():
        assert row["hypothesis"]
        assert row["null_or_failure_condition"]
        assert row["approval_class"]
        assert row["execution_lane"]
        assert row["official_or_primary_source_needs"]
        assert len(row["concrete_artifacts"]) == 2
        assert row["falsifier_or_acceptance_gate"]
        assert row["rollback_or_recovery"]
        assert row["protected_gates"] == PROTECTED_GATES
        assert row["observed_disposition"] is None
        assert row["x1_completion_credit"] == 0


def test_exactly_four_rejecting_mutations_per_new_proposal() -> None:
    rows = all_new_rows()
    mutations = [mutation for row in rows for mutation in row["negative_fixtures"]]
    assert len(mutations) == 160
    assert len({row["mutation_id"] for row in mutations}) == 160
    assert all(row["expected"] == "reject" for row in mutations)


def test_proposal_freeze_has_sixty_total_rows_and_chain_math() -> None:
    packet = read_json(X1 / "proposal-freeze.json")
    assert packet["rows_total"] == 60
    assert packet["new_proposal_count"] == 40
    assert len(packet["inherited_revalidations"]) == 20
    assert packet["proposal_chain_before"] == SOURCE_CHAIN_DECLARED == 5190
    assert packet["proposal_chain_after"] == CHAIN_AFTER == 5230
    assert packet["strict_x1_only"] is True


def test_novelty_audit_retains_unrecovered_gap() -> None:
    audit = read_json(X1 / "semantic-novelty-audit.json")
    assert audit["accessible_comparison_rows"] == 1620
    assert audit["unrecovered_declared_rows"] == 3570
    assert audit["unavailable_history_is_open_gap"] is True
    assert audit["universal_novelty_claim"] is False
    assert audit["exact_title_collisions"] == []
    assert audit["quarantined_proposals"] == []


def test_owner_portfolio_floors() -> None:
    packet = read_json(X1 / "portfolio-freeze.json")
    assert packet["counts"] == {
        "blocked": 10,
        "candidate": 30,
        "clean_fix_refine": 60,
        "exact_approval": 20,
        "runner": 10,
        "safe_now": 60,
        "skill": 20,
    }
    assert len(SAFE_TITLES) == 60
    assert len(CANDIDATE_TITLES) == 30
    assert len(REFINE_TITLES) == 60
    assert len(SKILL_TITLES) == 20
    assert len(RUNNER_TITLES) == 10


def test_exact_and_blocked_packets_remain_unexecuted() -> None:
    rows = read_json(X1 / "portfolio-freeze.json")["rows"]
    assert all(item["execution_state"] == "held_unexecuted" and item["completion_credit"] == 0 for item in rows["exact_approval"])
    assert all(item["execution_state"] == "held_unexecuted" and item["completion_credit"] == 0 for item in rows["blocked"])


def test_successor_recommendation_floors_and_one_practice() -> None:
    packet = read_json(X1 / "successor-recommendations-freeze.json")
    assert packet["counts"] == {"clean_fix_refine": 30, "runner": 10, "skill": 10}
    assert len(SUCCESSOR_SKILLS) == len(SUCCESSOR_RUNNERS) == 10
    assert len(SUCCESSOR_REFINE) == 30
    assert packet["practice_recommendation"]["practice"] == "grain-milling quality documentation"
    assert packet["route_binding"] == "recommendations_only_no_contact_until_exact_terminal_gate"


def test_three_practice_lenses_are_bounded() -> None:
    assert len(PRACTICES) == 3
    assert {row["practice"] for row in PRACTICES} == {
        "baker and process handover",
        "food-microbiology laboratory technician",
        "HACCP-style process reviewer",
    }
    assert all("no " in row["boundary"].lower() for row in PRACTICES)


def test_three_tool_candidates_are_planning_only_and_pinned() -> None:
    packet = read_json(X1 / "tool-candidate-freeze.json")
    assert packet["installation_state"] == "planned_not_installed_in_x1"
    assert [row["name"] for row in TOOL_CANDIDATES] == ["pint", "transitions", "portion"]
    assert all(len(row["wheel_sha256"]) == 64 for row in TOOL_CANDIDATES)
    assert all(row["declared_dependencies"] for row in TOOL_CANDIDATES)
    assert packet["target_count"] == 3


def test_startup_failures_are_retained_with_paired_witnesses() -> None:
    packet = read_json(X1 / "startup-operational-failures.json")
    assert packet["failure_count"] == len(packet["rows"])
    assert packet["failure_count"] >= 10
    assert all(row["approval_credit"] == 0 for row in packet["rows"])
    assert all(row["failed_witness"] and row["passing_bounded_witness"] and row["preferred_method"] for row in packet["rows"])


def test_x1_truth_is_planning_only() -> None:
    truth = read_json(X1 / "phase-truth.json")
    assert truth["x2_execution_started"] is False
    assert truth["x1_completion_credit"] == 0
    assert truth["real_world_actions"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["core_truth_labels"] == ["completed", "represented", "open_gap", "exact_gate"]


def test_route_is_prepared_not_sent_and_title_corrected() -> None:
    route = read_json(X1 / "route-state.json")
    assert route["delivery_state"] == "PREPARED_NOT_SENT"
    assert route["delivery_acknowledged"] is False
    assert route["successor_contact_count"] == 0
    assert route["stale_rejected_label"] == "Vesper Rowan"
    assert "Lyren Moss" in route["prospective_next_edge"]


def test_workflow_caps_and_one_success_rule() -> None:
    plan = read_json(X1 / "workflow-plan-freeze.json")
    assert plan["strict_x1_before_x2"] is True
    assert plan["commit_ceiling"] == {"x1": 5, "x2": 5, "total": 8}
    assert plan["file_ceiling"] == 2000
    assert any("one exact-final" in gate for gate in plan["gates"])


def test_source_ledger_is_zero_data_and_current_source_exact() -> None:
    ledger = read_json(X1 / "source-ledger.json")
    assert ledger["immutable_source"]["exact_final"] == "8b1a06d1f34147f7adbb494622df4734f48344de"
    assert ledger["immutable_source"]["direct_parent_chain"] is True
    assert ledger["immutable_source"]["zero_merges"] is True
    assert all(row["data_rows_ingested"] == 0 for row in ledger["sources"])


def test_x1_validation_receipt_passes() -> None:
    receipt = read_json(VALIDATION / "x1-validation-receipt.json")
    assert receipt["passed"] is True
    assert receipt["strict_planning_only"] is True
    assert receipt["checks"]["privacy_candidates"] == []
    assert receipt["checks"]["x2_paths"] == 0


def test_no_x2_closeout_seal_final_or_handoff_materialized() -> None:
    root = ROOT / OWNER_ROOT
    forbidden = [root / "x2", root / "closeout", root / "seal", root / "final", root / "handoffs"]
    assert not [path for path in forbidden if path.exists()]


def test_all_x1_json_documents_parse() -> None:
    paths = sorted((ROOT / OWNER_ROOT).rglob("*.json"))
    assert len(paths) >= 15
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_every_document_remains_below_word_ceiling() -> None:
    for path in (ROOT / OWNER_ROOT).rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".json", ".html"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100000


@pytest.mark.parametrize("gate", PROTECTED_GATES)
def test_protected_gate_names_remain_explicit(gate: str) -> None:
    assert gate
    assert (
        "claim" in gate
        or "authority" in gate
        or "real_" in gate
        or "safety" in gate
        or "identity" in gate
        or "production" in gate
        or "live_" in gate
        or "ownership" in gate
        or "cultural" in gate
        or "legitimacy" in gate
    )
