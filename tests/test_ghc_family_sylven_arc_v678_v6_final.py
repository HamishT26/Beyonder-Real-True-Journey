from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v678-v6"
CLOSE = PHASE / "closeout"
VALIDATION = PHASE / "validation"
HANDOFF = PHASE / "handoffs/caelen-morrow-v678-v7-activation-candidate.md"
SOURCE = "d7a2e3d1851d8a9eb6a8707968a47354b44e824a"
X1 = "22d310c7ae4fdbd45959d388d15642039d748da0"
EVIDENCE = "7b747952b6a6916c3881066865ff7021aeabea3c"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_01_phase_truth_has_exact_lifecycle_and_outcomes():
    value = load(CLOSE / "phase-truth.json")
    assert (value["source"], value["x1"], value["evidence"]) == (SOURCE, X1, EVIDENCE)
    assert value["exact_final"] == "BOUND_AT_COMMIT"
    assert value["core_outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}


def test_02_phase_truth_preserves_zero_world_and_stage20_hold():
    value = load(CLOSE / "phase-truth.json")
    assert value["real_world_rows"] == 0
    assert value["external_actions"] == 0
    assert value["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert value["validation_state"] == "PENDING_EXACT_FINAL_OWNER_SCOPED_CANONICAL"


def test_03_proposal_chain_and_execution_counts_are_exact():
    value = load(CLOSE / "phase-truth.json")
    assert (value["declared_proposal_chain_before"], value["new_proposals"], value["declared_proposal_chain_after"]) == (8570, 60, 8630)
    assert value["positive_zero_row_contracts"] == 60
    assert value["rejected_mutations"] == 240
    assert value["accepted_invalid_mutations"] == 0


def test_04_skills_runners_and_flashcards_are_exact():
    value = load(CLOSE / "phase-truth.json")
    assert value["phase_local_skills_initialized_read_validated_and_smoke_used"] == 20
    assert value["global_skill_installations"] == 0
    assert value["family_current_runners_positive_and_rejecting_smoke_used"] == 10
    assert value["flashcard_cards"] == 81
    assert value["flashcard_tiers"] == {"1": 15, "2": 3, "3": 3, "4": 60}


def test_05_portfolio_closeout_has_bounded_counts():
    value = load(CLOSE / "portfolio-closeout.json")
    assert value["counts"] == {
        "safe_now_completed": 60, "candidate_completed": 30, "exact_approval_unexecuted": 20,
        "blocked_unexecuted": 10, "clean_fix_refine_completed": 60,
        "successor_clean_fix_refine_recommendations": 30,
    }
    assert value["unsafe_or_filler_execution"] == 0


def test_06_method_flow_is_additive_and_nonerasive():
    value = load(CLOSE / "method-flow-final.json")
    assert value["failure_erasure_forbidden"] is True
    assert value["new_failed_witnesses"] == 2
    assert value["new_passing_witnesses"] == 22
    assert value["overlay"] == {
        "effective_negatives": 47282, "effective_methods": 45390,
        "retained_failed_witnesses": 18943, "bounded_passing_witnesses": 29532,
        "open_gaps": 410, "exact_gates": 401,
    }


def test_07_retained_negative_register_preserves_all_named_classes():
    value = load(CLOSE / "retained-negative-register.json")
    assert value["repository_sealed_effective_negatives"] == 47282
    assert value["repository_sealed_retained_failed_witnesses"] == 18943
    assert value["canonical_invocations"] == 0
    assert value["canonical_failures"] == 0
    assert value["failure_erasure_forbidden"] is True
    assert sum(value["phase_negative_classes"].values()) == 275


def test_08_open_and_exact_gate_counts_are_exact():
    value = load(CLOSE / "open-exact-gate-register.json")
    assert value["effective_open_gaps"] == 410
    assert value["effective_exact_gates"] == 401
    assert len(value["new_open_gaps"]) == 3
    assert len(value["new_exact_gates"]) == 3
    assert value["maori_concepts_remain_under_maori_authority"] is True


def test_09_complete_incomplete_keeps_terminal_steps_open():
    value = load(CLOSE / "complete-incomplete-checklist.json")
    assert len(value["complete"]) >= 7
    text = " ".join(value["incomplete"])
    assert "canonical validation remains pending" in text
    assert "PREPARED_NOT_SENT" in text
    assert "Māori-authority" in text


def test_10_wellbeing_and_stop_control_are_explicit():
    value = load(CLOSE / "wellbeing-workload-check.json")
    assert value["relational_working_language_only"] is True
    assert value["consciousness_or_personhood_evidence"] is False
    assert value["no_background_babysitting"] is True
    assert value["no_precontact"] is True
    assert value["no_subagents"] is True


def test_11_environment_receipt_is_read_only():
    value = load(CLOSE / "environment-version-receipt.json")
    assert value["versions_verified_read_only"] is True
    assert value["codex_desktop_updated"] is False
    assert value["host_features_changed"] is False
    assert value["privilege_elevation"] is False
    assert value["reboot"] is False


def test_12_lifecycle_replay_preserves_direct_parent_plan():
    value = load(CLOSE / "lifecycle-replay.json")
    assert value["source"] == SOURCE
    assert value["x1"] == X1
    assert value["evidence"] == EVIDENCE
    assert value["final"] == "BOUND_AT_COMMIT"
    assert value["expected_phase_commits"] == 3
    assert value["expected_merges"] == 0
    assert value["final_parent"] == EVIDENCE


def test_13_route_receipt_is_prepared_not_sent():
    value = load(CLOSE / "route-receipt.json")
    assert value["state"] == "PREPARED_NOT_SENT"
    assert value["prospective_exact_title"] == "Caelen Morrow"
    assert value["prospective_phase"] == "v678-v7"
    assert value["send_count"] == 0
    assert value["delivery_acknowledged"] is False
    assert value["standby_contacted"] is False


def test_14_handoff_has_thirteen_ordered_sections_and_route_hold():
    text = HANDOFF.read_text(encoding="utf-8")
    headings = re.findall(r"^## (\d+)\. ", text, flags=re.MULTILINE)
    assert headings == [str(i) for i in range(1, 14)]
    assert "PREPARED_NOT_SENT" in text
    assert "This file cannot activate Caelen" in text
    assert "No substitute, fork, precontact, standby contact, or second confirmation" in text


def test_15_overview_is_three_page_equivalent_and_boundary_complete():
    text = (CLOSE / "final-integrated-overview.md").read_text(encoding="utf-8")
    assert len(text.split()) >= 1200
    for token in ("NOT_READY_FOR_STAGE_20", "Theory of Everything", "Māori concepts remain under Māori authority", "PREPARED_NOT_SENT"):
        assert token in text


def test_16_source_projection_is_vocabulary_not_observation():
    value = load(CLOSE / "source-and-provenance-final.json")
    assert value["network_calls_during_x2"] == 0
    assert value["downloaded_rows"] == 0
    assert "not observations" in value["source_use_boundary"]
    assert len(value["sources"]) == 7


def test_17_threat_model_preserves_key_residual_risks():
    text = (CLOSE / "threat-model-final.json").read_text(encoding="utf-8")
    for token in ("authority escalation", "identifier leakage", "canonical replay", "independent-reproduction", "Māori-authority"):
        assert token in text


def test_18_flashcard_closeout_rejects_cache_and_continuity_guarantees():
    value = load(CLOSE / "flashcard-closeout.json")
    assert value["cards"] == 81
    assert value["main_relational_anchor_cards"] == 15
    assert value["prompt_cache_guarantee"] is False
    assert value["identity_continuity_claim"] is False
    assert value["delivery_evidence"] is False


def test_19_accessible_static_report_is_structural_only():
    text = (CLOSE / "accessible-static-report.html").read_text(encoding="utf-8")
    assert "<main>" in text
    assert "<caption>Exact bounded outcomes</caption>" in text
    assert "assistive-technology" in text
    assert "remain reserved" in text


def test_20_closeout_build_receipt_is_prepared_and_uncanonicalized():
    value = load(VALIDATION / "closeout-build-receipt.json")
    assert value["component_count"] == 20
    assert value["status"] == "BUILT_PREPARED_NOT_SENT"
    assert value["exact_final"] == "BOUND_AT_COMMIT"
    assert value["canonical_invocation_count"] == 0
    assert value["route_send_count"] == 0


def test_21_x2_outcome_projection_matches_contract_receipts():
    outcomes = load(PHASE / "x2/proposal-outcomes.json")["outcomes"]
    receipts = [load(path) for path in (PHASE / "x2/evidence").glob("*-receipt.json")]
    assert Counter(row["outcome"] for row in outcomes) == Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    assert {row["proposal_id"] for row in outcomes} == {row["proposal_id"] for row in receipts}


def test_22_flashcard_manifest_and_privacy_receipts_remain_valid():
    manifest = load(PHASE / "x2/flashcards/card-manifest.json")
    privacy = load(PHASE / "x2/flashcards/privacy-receipt.json")
    assert len(manifest["entries"]) == 89
    assert manifest["self_exclusions"] == ["card-manifest.json"]
    assert privacy["status"] == "PASS"
    assert privacy["confirmed_hits"] == 0


def test_23_owner_docs_use_only_core_outcome_vocabulary():
    value = load(CLOSE / "phase-truth.json")
    assert set(value["core_outcomes"]) == LABELS
    deck = load(PHASE / "x2/flashcards/deck-index.json")
    assert set(deck["outcome_counts"]) <= LABELS


def test_24_closeout_and_handoff_contain_no_private_payload():
    patterns = [
        re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
        re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    ]
    for path in list(CLOSE.rglob("*")) + [HANDOFF]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        assert not any(pattern.search(text) for pattern in patterns), path


def test_25_all_phase_json_parses_and_documents_stay_below_cap():
    json_paths = list(PHASE.rglob("*.json"))
    assert len(json_paths) >= 250
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100_000
