from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v673-v2"
SOURCE = "528a7d407cb7cace05b9bfd672b2fa74fc413d2c"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def test_exact_proposal_count_and_labels() -> None:
    payload = load("x1/proposals.json")
    assert payload["proposal_count"] == 40
    assert Counter(row["expected_disposition"] for row in payload["proposals"]) == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }


def test_every_required_proposal_field_is_present() -> None:
    required = {
        "proposal_id", "title", "hypothesis", "null_or_failure_condition",
        "approval_class", "execution_lane", "current_official_or_primary_source_need",
        "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery",
        "protected_gates", "expected_disposition",
    }
    for row in load("x1/proposals.json")["proposals"]:
        assert required <= set(row)
        assert all(row[key] for key in required)


def test_proposal_ids_and_titles_are_unique() -> None:
    rows = load("x1/proposals.json")["proposals"]
    assert len({row["proposal_id"] for row in rows}) == 40
    assert len({row["title"] for row in rows}) == 40


def test_x1_has_no_observed_outcome() -> None:
    payload = load("x1/proposals.json")
    assert payload["outcomes_observed"] is False
    assert all(row["outcome_observed"] is False for row in payload["proposals"])


def test_semantic_audit_is_bounded_and_collision_free() -> None:
    payload = load("x1/semantic-neighbor-audit.json")
    assert payload["collisions"] == 0
    assert payload["max_jaccard"] < payload["threshold"] == 0.72
    assert payload["universal_novelty_claim"] is False
    assert payload["exact_source_tree_corpus"]["malformed_or_missing_blobs"] == 0


def test_declared_chain_extends_by_forty() -> None:
    payload = load("x1/semantic-neighbor-audit.json")
    assert payload["declared_source_chain"] == 6270
    assert payload["declared_result_chain"] == 6310


def test_primary_and_protected_pillars_are_visible() -> None:
    for row in load("x1/proposals.json")["proposals"]:
        assert row["primary_pillar"] == "Freed ID and CBR Heart"
        assert row["protected_pillars"] == ["GMUT Mind", "THOS Body"]


def test_identity_and_practice_boundaries_are_explicit() -> None:
    text = (OWNER_ROOT / "x1" / "phase-boundaries.md").read_text(encoding="utf-8")
    for phrase in ["relational working language only", "no real people", "no employment", "NOT_READY_FOR_STAGE_20"]:
        assert phrase in text


def test_exact_approval_and_blocked_rows_are_unexecuted() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    assert all(row["state"] == "unexecuted_exact_approval" for row in portfolio["exact_approval"])
    assert all(row["state"] == "blocked_unexecuted" for row in portfolio["blocked"])


def test_portfolio_counts_are_exact() -> None:
    counts = load("x1/portfolio-freeze.json")["counts"]
    assert counts == {"safe_now": 60, "candidate": 30, "exact_approval": 20, "blocked": 10, "clean_fix_refine": 60, "skills": 20, "runners": 10, "tools": 3}


def test_startup_method_flow_retains_failure_and_recovery_pairs() -> None:
    flow = load("x1/method-flow-startup.json")
    assert flow["method_count"] == 9
    assert flow["failed_witness_count"] == 9
    assert flow["passing_witness_count"] == 9
    assert len(flow["witnesses"]) == 18
    assert all(row["retained"] for row in flow["witnesses"])


def test_source_provenance_preserves_external_location_gap() -> None:
    source = load("x1/source-and-provenance.json")
    assert source["source_final"] == SOURCE
    assert source["external_receipt_file_location_materialized"] is False
    assert source["source_validation_replayed"] is False


def test_open_gate_plan_preserves_inherited_baseline() -> None:
    gate = load("x1/open-gate-plan.json")
    assert gate["inherited_activation_baseline"]["negatives"] == 36374
    assert gate["inherited_activation_baseline"]["methods"] == 22702
    assert len(gate["planned_new_open_gaps"]) == 2
    assert len(gate["planned_new_exact_gates"]) == 2


def test_toolchain_plan_does_not_install_or_hide_gap() -> None:
    tools = load("x1/selected-toolchain-plan.json")
    assert tools["installation_authorized_or_performed"] is False
    assert "Bandit in active Python 3.12" in tools["unavailable_retained"]


def test_flashcards_are_navigation_only() -> None:
    cards = load("x1/flashcard-plan.json")
    assert cards["planned_card_count"] == 60
    assert cards["cache_or_cognition_claim"] is False
    assert cards["identity_continuity_claim"] is False


def test_threat_model_keeps_ten_explicit_threats() -> None:
    threat = load("x1/threat-model.json")
    assert len(threat["threats"]) == 10
    assert all(row["control"] for row in threat["threats"])


def test_approval_split_matches_proposals() -> None:
    split = load("x1/approval-split.json")
    assert len(split["safe_now"]) == 28
    assert len(split["candidate"]) == 10
    assert len(split["exact_approval"]) == 2
    assert split["exact_approval_executed"] == 0


def test_build_receipt_is_planning_only() -> None:
    receipt = load("x1/build-receipt.json")
    assert receipt["x2_paths_created"] is False
    assert receipt["network_calls"] == 0
    assert receipt["real_rows"] == 0
    assert receipt["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_manifest_replays_normalized_git_blobs_when_present() -> None:
    path = OWNER_ROOT / "validation" / "x1-manifest.json"
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        blob = subprocess.run(["git", "show", f":{row['path']}"], cwd=ROOT, capture_output=True, check=True).stdout
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == row["sha256"]


def test_validation_receipt_is_not_canonical() -> None:
    path = OWNER_ROOT / "validation" / "x1-validation-receipt.json"
    if not path.exists():
        return
    receipt = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["valid"] is True
    assert receipt["canonical_aggregate"] is False
    assert receipt["planning_only"] is True
