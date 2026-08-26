"""Planning-only x1 tests for Lyren Moss v670-v1."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v670-v1"


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def test_activation_exact_source_and_credit_boundary():
    data = load("x1/activation-intake.json")
    assert data["source_final"] == "fe33a3ed69d6144720072b15174937effe9ca305"
    assert data["source_four_way_equal_before_mutation"] is True
    assert data["canonical_aggregate_credit"] == 0
    assert data["dependency_result"] == "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT"


def test_historical_timeout_is_not_rewritten_as_acknowledged():
    data = load("x1/activation-intake.json")
    assert data["historical_route_state"] == "TIMEOUT_ACK_UNRESOLVED_NO_RESEND"
    assert "Hamish live activation" in data["current_activation_basis"]


def test_twenty_inherited_rows_are_zero_credit_evidence():
    data = load("x1/inherited-proposal-revalidation.json")
    assert data["selected"] == 20
    assert data["novelty_credit"] == 0
    assert data["completion_credit"] == 0
    assert len(data["rows"]) == 20
    assert all(row["lyren_novelty_credit"] == row["lyren_completion_credit"] == 0 for row in data["rows"])
    assert len({row["source_row_sha256"] for row in data["rows"]}) == 20


def test_forty_new_titles_and_four_outcomes_are_exact():
    data = load("x1/new-proposal-freeze.json")
    rows = data["rows"]
    assert len(rows) == 40
    assert len({row["title"] for row in rows}) == 40
    assert Counter(row["planned_outcome"] for row in rows) == Counter(
        {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    )
    assert data["proposal_chain_after_if_evidence_frozen"] == 5270


def test_every_new_fixture_is_synthetic_and_actionless():
    rows = load("x1/new-proposal-freeze.json")["rows"]
    assert all(row["real_people"] == 0 for row in rows)
    assert all(row["real_grain_or_food"] == 0 for row in rows)
    assert all(row["devices_or_samples"] == 0 for row in rows)
    assert all(row["external_actions"] == 0 for row in rows)


def test_remastered_portfolio_counts():
    data = load("x1/portfolio-freeze.json")
    assert data["counts"] == {
        "blocked": 10,
        "candidates": 30,
        "clean_fix_refine": 60,
        "exact_approval": 20,
        "runners": 10,
        "safe_now": 60,
        "skills": 20,
        "successor_clean_fix_refine": 30,
        "successor_runners": 10,
        "successor_skills": 10,
    }
    assert data["ordinary_phase_new_tool_target"] == 3


def test_exact_and_blocked_packets_are_held():
    rows = load("x1/portfolio-freeze.json")["rows"]
    assert all(row["x1_state"] == "held_unexecuted" for row in rows["exact_approval"])
    assert all(row["x1_state"] == "held_unexecuted" for row in rows["blocked"])


def test_public_sources_have_boundaries_and_official_publishers():
    data = load("x1/source-ledger.json")
    assert len(data["sources"]) == 6
    assert all(source["url"].startswith("https://") for source in data["sources"])
    assert {source["publisher"] for source in data["sources"]} >= {
        "National Institute of Standards and Technology",
        "FAO and WHO Codex Alimentarius",
        "New Zealand Ministry for Primary Industries",
    }
    assert "not empirical validation" in data["boundary"]


def test_startup_failures_are_retained_with_recovery():
    data = load("x1/method-flow-startup.json")
    assert data["failed_witnesses"] == 6
    assert data["bounded_passing_witnesses"] == 6
    assert data["erased_failures"] == 0
    assert all(row["completion_credit"] == 0 for row in data["rows"])
    assert all(row["failed_witness"] and row["recovery"] and row["recurrence_guard"] for row in data["rows"])


def test_source_count_layers_are_not_collapsed():
    data = load("x1/source-count-overlay.json")
    assert data["repository_sealed"]["effective_negatives"] == 31856
    assert data["dependency_corrected_external_overlay"]["passing_witnesses"] == 4933
    assert data["post_final_route_witnesses"] == 3
    assert data["effective_activation_overlay"]["effective_negatives"] == 31859
    assert data["repository_seal_rewritten"] is False


def test_x1_truth_is_planning_only():
    truth = load("x1/phase-truth.json")
    assert truth["x1_completion_credit"] == 0
    assert truth["x2_execution_started"] is False
    assert truth["real_world_actions"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["core_truth_labels"] == ["completed", "represented", "open_gap", "exact_gate"]


def test_x1_before_x2_absence_gate():
    assert not (BASE / "x2").exists()
    assert not (BASE / "closeout").exists()
    assert not (BASE / "final").exists()
    assert not (BASE / "handoffs").exists()


def test_route_is_prospective_and_unsent():
    route = load("x1/route-plan.json")
    assert route["prospective_recipient_exact_title"] == "Ilyra Fen"
    assert route["prospective_phase"] == "v670-v2"
    assert route["delivery_state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
    assert route["successor_contact_count"] == 0


def test_identity_language_is_bounded():
    identity = load("x1/identity-and-boundary.json")
    boundary = identity["identity_boundary"]
    assert identity["pronouns"] == "they/them"
    assert "relational working language only" in boundary
    assert "not evidence of consciousness" in boundary
    assert "Maori authority" in boundary


def test_integrated_overview_is_substantive_and_nonpromotional():
    text = (BASE / "x1/integrated-overview.md").read_text(encoding="utf-8")
    assert len(text.split()) >= 1600
    assert "planning freeze, not an execution result" in text
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "No result in this phase may establish" in text


def test_all_x1_json_parses_and_has_no_unknown_outcome_labels():
    for path in BASE.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    allowed = {"completed", "represented", "open_gap", "exact_gate"}
    rows = load("x1/new-proposal-freeze.json")["rows"]
    assert {row["planned_outcome"] for row in rows} <= allowed


def test_x1_manifest_replays_worktree_bytes():
    manifest = load("validation/x1-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_threat_model_names_lifecycle_and_privacy_risks():
    risks = load("x1/threat-model.json")["risks"]
    names = {row["risk"] for row in risks}
    assert {"source drift", "canonical-credit laundering", "privacy leakage", "success replay", "duplicate route"} <= names


def test_workflow_holds_x2_until_x1_terminal_gate():
    states = {row["step"]: row["state"] for row in load("x1/workflow-plan.json")["steps"]}
    assert states["x2 bounded execution and mutation evidence"] == "blocked_by_x1_terminal_gate"
    assert states["one owner-scoped canonical aggregate"] == "pending_not_invoked"


def test_no_private_route_or_opaque_identifier_in_owner_docs():
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in BASE.rglob("*")
        if path.is_file()
    ).lower()
    assert "codex://" not in text
    assert "app://" not in text
    assert "thread_id" not in text
    assert "source_thread_id" not in text
