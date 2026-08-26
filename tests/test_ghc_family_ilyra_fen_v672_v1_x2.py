"""Bounded x2 tests for Ilyra Fen v672-v1."""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from uuid import UUID

import pytest

from scripts import build_ghc_family_ilyra_fen_v672_v1_x2 as builder
from scripts.ghc_family_ilyra_v672_v1_drawing_contracts import (
    DrawingContractError,
    validate_board,
)
from scripts.ghc_family_ilyra_v672_v1_drawing_contracts import (
    positive_fixture as board_fixture,
)
from scripts.ghc_family_ilyra_v672_v1_drawing_contracts import (
    rejecting_fixtures as board_rejecting,
)
from scripts.ghc_family_ilyra_v672_v1_evidence_guard import (
    EvidenceGuardError,
    canonical_json_bytes,
    five_class_scan,
    terminal_route_guard,
    validate_proposal,
)
from scripts.ghc_family_ilyra_v672_v1_revision_tribunal import (
    RevisionTribunalError,
    validate_record,
)
from scripts.ghc_family_ilyra_v672_v1_revision_tribunal import (
    fixture as revision_fixture,
)
from scripts.ghc_family_ilyra_v672_v1_revision_tribunal import (
    rejecting_fixtures as revision_rejecting,
)

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "ilyra-fen" / "v672-v1"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def test_drawing_contract_board_accepts_bounded_positive_fixture():
    result = validate_board(board_fixture())
    assert result["accepted"] is True
    assert result["professional_result"] is False


@pytest.mark.parametrize("row", board_rejecting())
def test_drawing_contract_board_rejects_preregistered_mutations(row):
    with pytest.raises(DrawingContractError):
        validate_board(row)


@pytest.mark.parametrize("lens", ["architectural_revision", "external_reference_transmittal", "accessible_register"])
def test_revision_tribunal_accepts_each_synthetic_lens(lens):
    result = validate_record(revision_fixture(lens))
    assert result["accepted"] is True
    assert result["authority_conferred"] is False


@pytest.mark.parametrize("lens", ["architectural_revision", "external_reference_transmittal", "accessible_register"])
def test_revision_tribunal_rejects_each_lens_mutations(lens):
    for row in revision_rejecting(lens):
        with pytest.raises(RevisionTribunalError):
            validate_record(row)


def test_canonical_json_sorts_keys_and_rejects_duplicates():
    assert canonical_json_bytes('{"b":2,"a":1}') == b'{"a":1,"b":2}'
    with pytest.raises(EvidenceGuardError):
        canonical_json_bytes('{"a":1,"a":2}')


def test_canonical_json_rejects_nonfinite_values():
    with pytest.raises(EvidenceGuardError):
        canonical_json_bytes('{"value":NaN}')


def test_all_frozen_proposals_pass_structure_guard():
    rows = load("x1/new-proposal-freeze.json")["rows"]
    assert len(rows) == 40
    assert all(validate_proposal(row)["accepted"] for row in rows)


def test_proposal_guard_rejects_external_action_and_missing_gates():
    row = deepcopy(load("x1/new-proposal-freeze.json")["rows"][0])
    row["external_actions"] = 1
    with pytest.raises(EvidenceGuardError):
        validate_proposal(row)
    row["external_actions"] = 0
    row["protected_gates"] = []
    with pytest.raises(EvidenceGuardError):
        validate_proposal(row)


def test_mutation_receipt_is_exact_and_zero_credit():
    payload = load("x2/mutation-receipt.json")
    assert payload["preregistered"] == payload["executed"] == payload["rejected"] == 160
    assert payload["unexpected_accepts"] == 0
    assert payload["completion_credit"] == 0
    assert len(payload["rows"]) == 160


def test_positive_controls_are_exactly_thirty_six():
    payload = load("x2/positive-control-receipt.json")
    assert payload["planned"] == payload["executed"] == payload["passed"] == 36
    assert all(row["external_actions"] == 0 for row in payload["rows"])


def test_outcome_distribution_uses_only_four_labels():
    payload = load("x2/outcome-ledger.json")
    assert len(payload["rows"]) == 40
    assert Counter(row["observed_outcome"] for row in payload["rows"]) == Counter(builder.OUTCOMES)
    assert {row["observed_outcome"] for row in payload["rows"]} == {"completed", "represented", "open_gap", "exact_gate"}


def test_open_and_exact_rows_have_no_positive_control():
    rows = load("x2/outcome-ledger.json")["rows"]
    held = [row for row in rows if row["observed_outcome"] in {"open_gap", "exact_gate"}]
    assert len(held) == 4
    assert all(row["positive_control"] is None for row in held)


def test_three_tools_have_accepting_and_rejecting_evidence():
    payload = load("x2/tool-evidence.json")
    assert len(payload["tools"]) == 3
    assert payload["evidence"]["drawing_contracts"]["rejecting"] == 5
    assert payload["evidence"]["revision_tribunal"]["rejecting"] == 12
    assert payload["evidence"]["evidence_guard"]["duplicate_rejected"] is True
    assert payload["external_actions"] == 0


def test_owner_portfolio_completed_and_approval_work_held():
    payload = load("x2/portfolio-outcome.json")
    assert payload["counts"]["safe_now"] == 60
    assert payload["counts"]["candidates"] == 30
    assert payload["counts"]["skills"] == 20
    assert payload["counts"]["runners"] == 10
    assert payload["counts"]["clean_fix_refine"] == 60
    assert payload["exact_and_blocked_executed"] == 0


def test_skill_and_runner_packages_are_built_validated_smoke_used_and_local():
    payload = load("x2/skill-runner-evidence.json")
    assert len(payload["skills"]) == 20
    assert len(payload["runners"]) == 10
    assert payload["quick_validation_failures"] == 0
    assert payload["runner_smoke_failures"] == 0
    assert payload["global_installations"] == 0
    assert all(row["quick_validate_exit"] == 0 for row in payload["skills"])
    assert all(row["accepting_exit"] == 0 and row["rejecting_exit"] == 1 for row in payload["runners"])


def test_clean_fix_refine_is_additive_only():
    payload = load("x2/clean-fix-refine-evidence.json")
    assert len(payload["completed"]) == 60
    assert len(payload["successor_recommendations"]) == 30
    assert payload["destructive_cleanup"] == 0


def test_exact_and_blocked_packets_remain_unexecuted():
    payload = load("x2/exact-and-blocked-register.json")
    assert len(payload["exact_approval"]) == 20
    assert len(payload["blocked"]) == 10
    assert payload["executed"] == 0


def test_method_flow_retains_all_failures_and_counts_overlay():
    payload = load("x2/method-flow-evidence.json")
    assert len(payload["startup_rows"]) == 16
    assert len(payload["x2_operational_rows"]) == 9
    assert len(payload["mutation_rows"]) == 160
    assert payload["effective_negatives"] == 35001
    assert payload["effective_methods"] == 21547
    assert payload["effective_failed_witnesses"] == 6822
    assert payload["effective_passing_witnesses"] == 8838
    assert payload["erased_failures"] == 0


def test_phase_truth_preserves_gaps_gates_and_terminal_verdict():
    truth = load("x2/phase-truth-evidence.json")
    assert truth["proposal_chain"] == 5910
    assert truth["open_gaps"] == 273
    assert truth["exact_gates"] == 268
    assert truth["real_world_actions"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_accessible_report_has_structural_features_and_reservations():
    text = (OWNER_ROOT / "x2" / "accessible-evidence-report.html").read_text(encoding="utf-8")
    for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', "scope='row'", 'role="status"', '@media print'):
        assert token in text
    assert "affected-user evaluation remain reserved" in text


def test_five_class_guard_accepts_safe_text_and_rejects_uuid():
    assert five_class_scan("bounded synthetic fixture only")["valid"] is True
    synthetic_uuid = str(UUID(hex="12345678123441238123123456789abc"))
    assert five_class_scan(synthetic_uuid)["valid"] is False


def test_scanner_self_reference_candidate_is_retained_and_disposed():
    payload = load("x2/privacy-candidate-disposition.json")
    assert payload["candidate_classes"] == ["private_callable_route", "transcript_screenshot_or_session_stream"]
    assert payload["disposition"] == "scanner_pattern_definition_nonpayload"
    assert payload["confirmed_payload_hits"] == 0
    assert payload["privacy_complete"] is False


def test_terminal_route_guard_is_fail_closed():
    assert terminal_route_guard({"recipient": "Auren Lark", "phase": "v672-v2"})["allowed"] is False


def test_x1_paths_are_unmodified_in_worktree():
    changed = builder.git_text("diff", "--name-only", builder.X1_COMMIT, "--", "docs/ilyra-fen/v672-v1/x1", "scripts/build_ghc_family_ilyra_fen_v672_v1_x1.py", "tests/test_ghc_family_ilyra_fen_v672_v1_x1.py")
    assert changed == ""


def test_all_x2_json_parses_and_docs_below_cap():
    json_paths = sorted((OWNER_ROOT / "x2").rglob("*.json"))
    assert len(json_paths) >= 130
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    for path in (OWNER_ROOT / "x2").rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100000


def test_materialized_file_guard_remains_below_two_thousand():
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    assert len(files) < 2000


def test_environment_receipt_has_no_install_update_or_real_download():
    payload = load("x2/environment-receipt.json")
    assert payload["desktop_updated_by_phase"] is False
    assert payload["elevation"] is False
    assert payload["host_security_changes"] is False
    assert payload["unrelated_installation"] is False
    assert payload["reboot"] is False
    assert payload["real_data_downloads"] == 0
