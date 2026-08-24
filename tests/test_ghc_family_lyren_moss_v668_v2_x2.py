#!/usr/bin/env python3
"""Bounded x2 evidence tests for Lyren Moss v668-v2."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_lyren_moss_v668_v2_archive import (  # noqa: E402
    ALLOWED_OUTCOMES,
    PHASE_ROOT,
    PROTECTED_GATES,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_FINAL,
)
from ghc_family_lyren_moss_v668_v2_controls import (  # noqa: E402
    ContractError,
    container_codec_board,
    rational_timebase,
    route_transition,
    validation_credit_transition,
)


X1_HEAD = "0683eb961987fd4c7283d278e3b217647aef73f0"


def read_json(relative: str) -> dict:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True).stdout


def immutable_evidence_head() -> str | None:
    head = git("rev-parse", "HEAD")
    commits = git("rev-list", "--reverse", "--ancestry-path", f"{X1_HEAD}..{head}").splitlines()
    return commits[0] if commits else None


def test_immutable_x1_is_direct_child_and_x2_free() -> None:
    assert git("rev-parse", f"{X1_HEAD}^") == SOURCE_FINAL
    paths = set(git("ls-tree", "-r", "--name-only", X1_HEAD).splitlines())
    assert not any(path.startswith("docs/lyren-moss/v668-v2/x2/") for path in paths)
    assert "scripts/ghc_family_lyren_moss_v668_v2_controls.py" not in paths


def test_exact_outcome_counts_and_labels() -> None:
    packet = read_json("x2/proposals/proposal-outcomes.json")
    assert packet["count"] == 40
    assert packet["outcome_counts"] == {
        "completed": 28,
        "exact_gate": 2,
        "open_gap": 2,
        "represented": 8,
    }
    assert set(packet["outcome_counts"]) == set(ALLOWED_OUTCOMES)
    assert Counter(row["outcome"] for row in packet["outcomes"]) == Counter(packet["outcome_counts"])


def test_completed_receipts_are_bounded_and_synthetic() -> None:
    rows = read_json("x2/proposals/proposal-outcomes.json")["outcomes"]
    completed = [row for row in rows if row["outcome"] == "completed"]
    assert len(completed) == 28
    assert all(row["bounded_completion_credit"] == 1 for row in completed)
    assert all(row["external_actions"] == 0 and row["real_people"] == 0 and row["real_rows"] == 0 for row in completed)
    assert all(row["professional_or_authority_credit"] == 0 for row in completed)
    assert all(row["independent_reproduction_credit"] == 0 and row["stage20_credit"] == 0 for row in completed)


def test_represented_gap_and_gate_credit_remains_zero() -> None:
    rows = read_json("x2/proposals/proposal-outcomes.json")["outcomes"]
    noncompleted = [row for row in rows if row["outcome"] != "completed"]
    assert len(noncompleted) == 12
    assert all(row["bounded_completion_credit"] == 0 for row in noncompleted)
    assert sum(row["execution_count"] for row in noncompleted if row["outcome"] == "represented") == 8
    assert sum(row["execution_count"] for row in noncompleted if row["outcome"] in {"open_gap", "exact_gate"}) == 0


def test_one_hundred_sixty_mutations_are_rejected_and_retained() -> None:
    packet = read_json("x2/proposals/negative-mutation-results.json")
    assert packet["count"] == packet["rejected"] == 160
    assert packet["accepted"] == 0
    assert packet["failure_credit"] == 0
    assert packet["failed_witnesses_retained"] == 160
    assert packet["bounded_passing_rejection_witnesses"] == 160
    assert all(not row["accepted"] and row["failed_witness_retained"] for row in packet["mutations"])


def test_proposal_and_card_materialization_is_exact() -> None:
    proposal_files = list((PHASE_ROOT / "x2/proposals").glob("lm6682-n*.json"))
    card_files = list((PHASE_ROOT / "x2/cards").glob("lm6682-n*.json"))
    assert len(proposal_files) == 40
    assert len(card_files) == 40
    assert len({read_json(f"x2/cards/{path.name}")["card_id"] for path in card_files}) == 40


def test_flashcard_graph_has_four_tiers_and_required_categories() -> None:
    deck = read_json("x2/cards/deck-index.json")
    assert deck["card_count"] == 40
    assert len(deck["tier_order"]) == 4
    for row in deck["cards"]:
        assert len(row["address"]) == 4
        assert row["address"][0] == "Lyren Moss"
        assert row["outcome"] in ALLOWED_OUTCOMES
    assert deck["identity_continuity_or_personhood_evidence"] is False


def test_control_registry_covers_twenty_eight_completed_controls() -> None:
    packet = read_json("x2/evidence/control-receipts.json")
    assert packet["completed_control_count"] == 28
    assert packet["control_count"] == 28
    assert len(packet["controls"]) == 28
    assert packet["external_actions"] == packet["real_rows"] == 0


def test_exact_rational_and_container_boundaries() -> None:
    assert rational_timebase(24000, 1001)["denominator"] == 1001
    with pytest.raises(ContractError):
        rational_timebase(23.976, 1)  # type: ignore[arg-type]
    assert container_codec_board("Matroska", ["FFV1", "PCM"], 1)["unknown_elements_preserved"] == 1
    with pytest.raises(ContractError):
        container_codec_board("FFV1", ["FFV1"], 0)


def test_route_and_validation_state_machines_refuse_replay() -> None:
    route = route_transition("prepared_not_sent", "terminal_gate_passed")
    route = route_transition(route, "exact_title_unique")
    assert route == "ready_to_send"
    with pytest.raises(ContractError):
        route_transition(route, "exact_title_unique")
    credit = validation_credit_transition("not_invoked", "invoke")
    credit = validation_credit_transition(credit, "pass")
    assert credit == "successful_once_no_replay"
    with pytest.raises(ContractError):
        validation_credit_transition(credit, "invoke")


def test_source_and_practice_receipts_reserve_authority() -> None:
    source = read_json("x2/evidence/source-use-receipt.json")
    practice = read_json("x2/evidence/pillar-practice-receipt.json")
    assert source["source_count"] == 7
    assert source["webvtt_work_in_progress_status_retained"] is True
    assert source["real_conformance_assessments"] == source["professional_format_selections"] == 0
    assert practice["primary_pillar"] == "THOS Body"
    assert practice["practice_count"] == practice["synthetic_fixtures"] == 3
    assert practice["professional_or_operational_authority"] is False


def test_fixture_boundary_has_zero_real_rows_and_actions() -> None:
    boundary = read_json("x2/evidence/fixture-boundary.json")
    assert boundary["synthetic_only"] is True
    for key, value in boundary.items():
        if key.startswith("real_") or key == "external_archival_actions":
            assert value == 0


def test_accessibility_is_structural_not_complete() -> None:
    evidence = read_json("x2/evidence/accessibility-structure.json")
    assert evidence["native_table"] and evidence["caption"] and evidence["scoped_headers"]
    assert evidence["manual_evaluation"] is False
    assert evidence["affected_user_evaluation"] is False
    assert evidence["complete_accessibility_claim"] is False


def test_portfolio_counts_and_exact_packets_remain_unexecuted() -> None:
    owner = read_json("x2/portfolio/owner-execution.json")
    assert owner["counts"] == {
        "owner_safe_now": 60,
        "owner_candidates": 30,
        "owner_skills": 20,
        "owner_runners": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine": 30,
        "exact_approval_packets": 20,
        "blocked_packets": 10,
    }
    assert all(row["x2_execution_count"] == 0 for row in owner["exact_approval_packets"])
    assert all(row["completion_credit"] == 0 for row in owner["blocked_packets"])
    assert owner["destructive_cleanup_actions"] == owner["global_overwrites"] == 0


def test_twenty_skills_are_phase_local_and_complete() -> None:
    paths = sorted((PHASE_ROOT / "x2/skills").glob("*/SKILL.md"))
    assert len(paths) == len(SKILL_NAMES) == 20
    assert {path.parent.name for path in paths} == set(SKILL_NAMES)
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for heading in ("## Purpose", "## Trigger", "## Inputs", "## Procedure", "## Outputs", "## Failure shields", "## Evidence and identity boundary", "## Rollback and validation"):
            assert heading in text
        assert "not globally installed" in text


def test_ten_runners_have_one_self_test_receipt() -> None:
    packet = read_json("x2/runners/runner-receipts.json")
    assert packet["count"] == len(RUNNER_NAMES) == 10
    assert packet["all_built_tested_used_once"] is True
    assert packet["global_install_count"] == 0
    for receipt in packet["receipts"]:
        assert receipt["build_count"] == receipt["test_count"] == receipt["use_count"] == 1
        assert receipt["receipt"]["state"] == "PASS_PHASE_LOCAL_RUNNER_SELF_TEST"
        assert receipt["receipt"]["external_actions"] == 0
        path = ROOT / receipt["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["sha256"]


def test_successor_recommendations_have_zero_owner_credit_and_no_contact() -> None:
    successor = read_json("x2/portfolio/successor-recommendations.json")
    assert successor["recipient"] == "Ilyra Fen"
    assert successor["phase"] == "v668-v3"
    assert successor["contacted"] is False
    assert successor["owner_completion_credit"] == 0
    assert all(row["completion_credit"] == 0 for row in successor["clean_fix_refine"])


def test_method_flow_counts_are_additive_and_terminal() -> None:
    method = read_json("method-flow/x2-operational-method-flow.json")
    assert method["owner_synthetic_mutations"] == {
        "effective_negatives": 160,
        "failed_witnesses": 160,
        "methods": 160,
        "passing_witnesses": 160,
    }
    assert method["effective_after_x2_before_closeout"] == {
        "effective_negatives": 29211,
        "methods": 15797,
        "failed_witnesses": 1512,
        "passing_witnesses": 2347,
        "open_gaps": 211,
        "exact_gates": 206,
    }
    assert method["all_failures_retained"] is True
    assert method["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_route_remains_prepared_not_sent() -> None:
    route = read_json("x2/route/prepared-route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_contacted"] is False
    assert route["terminal_gate_passed"] is False
    assert route["single_send_maximum"] == 1


def test_evidence_manifest_replays_in_worktree_or_git_blob_domain() -> None:
    manifest = read_json("evidence/evidence-content-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    evidence_head = immutable_evidence_head()
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    for row in manifest["entries"]:
        if evidence_head is not None:
            data = git_bytes("show", f"{evidence_head}:{row['path']}")
        elif row["path"] in staged:
            data = git_bytes("show", f":{row['path']}")
        else:
            data = (ROOT / row["path"]).read_bytes()
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_materialized_and_owner_file_count_is_below_rotation_stop() -> None:
    owner_files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    assert len(owner_files) < 2000


def test_report_preserves_terminal_and_protected_gates() -> None:
    report = (PHASE_ROOT / "x2/evidence-report.md").read_text(encoding="utf-8")
    assert "NOT_READY_FOR_STAGE_20" in report
    assert "globally installed" in report
    assert "No real media payload" in report
    for gate in PROTECTED_GATES:
        assert gate in report
