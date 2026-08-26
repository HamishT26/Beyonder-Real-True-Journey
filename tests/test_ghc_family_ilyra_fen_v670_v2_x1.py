"""Planning-only tests for Ilyra Fen v670-v2 x1."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_ilyra_fen_v670_v2_x1 as builder

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "ilyra-fen" / "v670-v2"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def test_exact_owner_phase_source_and_branch_constants():
    assert builder.OWNER == "Ilyra Fen"
    assert builder.PHASE == "v670-v2"
    assert builder.SOURCE_FINAL == "1b25a3e888464698a650cd515f4afae0841100c1"
    assert builder.BRANCH == "codex/GHC-Family/ilyra-fen-v670-v2-full-tools"


def test_forty_new_proposals_are_unique_and_four_label_only():
    rows = load("x1/new-proposal-freeze.json")["rows"]
    assert len(rows) == 40
    assert len({row["title"] for row in rows}) == 40
    assert Counter(row["planned_outcome"] for row in rows) == Counter(builder.OUTCOMES)
    assert {row["planned_outcome"] for row in rows} == set(builder.CORE_LABELS)


def test_each_new_proposal_has_full_preregistration_contract():
    required = {
        "hypothesis",
        "null_or_failure_condition",
        "approval_class",
        "execution_lane",
        "official_or_primary_source_needs",
        "concrete_artifacts",
        "falsifier_or_acceptance_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
    }
    for row in load("x1/new-proposal-freeze.json")["rows"]:
        assert required <= row.keys()
        assert row["expected_disposition"] == row["planned_outcome"]
        assert row["real_people"] == 0
        assert row["external_actions"] == 0


def test_twenty_inherited_rows_have_zero_ilyra_credit():
    payload = load("x1/inherited-proposal-revalidation.json")
    assert payload["selected"] == 20
    assert payload["novelty_credit"] == 0
    assert payload["completion_credit"] == 0
    assert len(payload["rows"]) == 20
    assert all(row["ilyra_novelty_credit"] == 0 for row in payload["rows"])
    assert all(row["ilyra_completion_credit"] == 0 for row in payload["rows"])


def test_proposal_chain_and_semantic_gap_remain_explicit():
    freeze = load("x1/new-proposal-freeze.json")
    audit = load("x1/semantic-neighbor-audit.json")
    assert freeze["proposal_chain_before"] == 5270
    assert freeze["proposal_chain_after_if_evidence_frozen"] == 5310
    assert audit["inherited_semantic_recovery_gap"] == 3570
    assert audit["collisions"] == 0
    assert audit["universal_novelty_claim"] is False


def test_portfolio_matches_current_overlay_exactly():
    counts = load("x1/portfolio-freeze.json")["counts"]
    assert counts == {
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


def test_three_practice_lenses_and_one_successor_lens_are_frozen():
    payload = load("x1/portfolio-freeze.json")
    assert len(payload["bounded_practice_lenses"]) == 3
    assert payload["successor_practice_recommendation"] == "synthetic seed-bank cold-storage excursion correction and handover"
    assert payload["ordinary_phase_new_tool_target"] == 3


def test_primary_pillar_and_protected_pillars_are_explicit():
    truth = load("x1/phase-truth.json")
    assert truth["primary_pillar"] == "GMUT Mind"
    assert truth["protected_pillars"] == ["THOS Body", "Freed ID and CBR Heart"]
    assert truth["x2_execution_started"] is False
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_source_verification_is_exact_and_commit_local():
    source = load("x1/activation-intake.json")["source_verification"]
    assert source["all_equal"] is True
    assert source["parent_chain"]["exact"] is True
    assert source["phase_commits"] == 3
    assert source["merge_commits"] == 0
    assert source["commit_local_manifest_entries_replayed"] == 372
    assert source["commit_local_manifest_mismatches"] == 0


def test_external_receipt_path_is_not_invented():
    receipt = load("x1/activation-intake.json")["source_verification"]["external_canonical_receipt"]
    assert receipt["path_supplied"] is False
    assert receipt["rehash_state"].startswith("not_rehashed")


def test_startup_failures_are_retained_at_zero_credit():
    payload = load("x1/method-flow-startup.json")
    assert payload["failed_witnesses"] == 9
    assert payload["bounded_passing_witnesses"] == 9
    assert payload["erased_failures"] == 0
    assert all(row["completion_credit"] == 0 for row in payload["rows"])
    assert all(row["failed_witness"] and row["recovery"] for row in payload["rows"])


def test_source_seal_and_successor_overlay_are_separate():
    payload = load("x1/source-count-overlay.json")
    assert payload["repository_sealed"]["effective_negatives"] == 32057
    assert payload["successor_activation_overlay"]["effective_negatives"] == 32066
    assert payload["successor_activation_overlay"]["repository_seal_rewritten"] is False


def test_route_is_prepared_not_sent_and_auren_only():
    route = load("x1/route-plan.json")
    assert route["prospective_recipient_exact_title"] == "Auren Lark"
    assert route["prospective_phase"] == "v670-v3"
    assert route["delivery_state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
    assert route["successor_contact_count"] == 0
    assert route["standby_contact_count"] == 0


def test_sources_are_official_or_primary_and_bounded():
    payload = load("x1/source-ledger.json")
    urls = {row["url"] for row in payload["sources"]}
    assert "https://fits.gsfc.nasa.gov/fits_standard.html" in urls
    assert "https://www.epa.gov/quality/sample-and-evidence-management" in urls
    assert "https://gtfs.org/documentation/schedule/reference/" in urls
    assert "not observations" in payload["boundary"]


def test_identity_language_is_relational_only():
    payload = load("x1/identity-and-boundary.json")
    boundary = payload["identity_boundary"].lower()
    assert "relational working language only" in boundary
    assert "not evidence of consciousness" in boundary
    assert "maori authority" in boundary


def test_overview_is_three_page_equivalent_and_below_cap():
    words = (OWNER_ROOT / "x1" / "integrated-overview.md").read_text(encoding="utf-8").split()
    assert len(words) >= 1200
    assert len(words) <= 100000


def test_every_phase_document_is_below_word_cap():
    for path in OWNER_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".html"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100000, path


def test_no_x2_or_closeout_material_exists_in_x1():
    assert not (OWNER_ROOT / "x2").exists()
    assert not (OWNER_ROOT / "closeout").exists()
    assert not (OWNER_ROOT / "final").exists()


def test_materialized_file_count_stays_below_rotation_guard():
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    assert len(files) < 2000


def test_x1_text_contains_no_raw_task_identifier_shape():
    uuid = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE)
    for path in (OWNER_ROOT / "x1").rglob("*"):
        if path.is_file():
            assert not uuid.search(path.read_text(encoding="utf-8")), path


def test_build_receipt_is_planning_only():
    receipt = load("x1/build-receipt.json")
    assert receipt["x2_materialized"] is False
    assert receipt["external_actions"] == 0
    assert receipt["new_rows"] == 40
    assert receipt["inherited_rows"] == 20
