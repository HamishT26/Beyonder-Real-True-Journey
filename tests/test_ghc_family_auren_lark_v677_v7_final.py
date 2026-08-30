from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/auren-lark/v677-v7"
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
EVIDENCE = "3f91c32cb1acda2900ce69bedc60971353084775"
SEALED = {
    "effective_negatives": 45715,
    "effective_methods": 43030,
    "retained_failed_witnesses": 17376,
    "bounded_passing_witnesses": 26359,
    "open_gaps": 389,
    "exact_gates": 380,
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return (
        path.read_bytes()
        .replace(b"\r\n", b"\n")
        .replace(b"\r", b"\n")
    )


def test_phase_truth_has_exact_anchors_seal_and_verdict() -> None:
    truth = load(FINAL / "phase-truth.json")
    assert (
        truth["source"] == SOURCE
        and truth["x1"] == X1
        and truth["evidence"] == EVIDENCE
    )
    assert truth["exact_final"] == "COMMIT_CONTAINING_THIS_FILE"
    assert truth["lifecycle_state"] == "REPOSITORY_PREPARED_FINAL"
    assert truth["canonical_state"] == "PENDING_ONE_EXACT_FINAL_INVOCATION"
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert {key: truth[key] for key in SEALED} == SEALED
    assert (
        truth["real_world_rows"] == 0
        and truth["external_real_world_actions"] == 0
    )


def test_outcomes_use_exact_four_label_partition() -> None:
    outcomes = load(FINAL / "phase-truth.json")["outcomes"]
    assert outcomes == {
        "completed": 42,
        "represented": 12,
        "open_gap": 3,
        "exact_gate": 3,
    }
    assert sum(outcomes.values()) == 60


def test_method_flow_preserves_failures_and_closeout_witnesses() -> None:
    flow = load(FINAL / "method-flow-final.json")
    assert flow["repository_seal"] == SEALED
    assert flow["failure_nonerasure"] is True
    assert flow["recovery_never_retroactively_promotes_failure"] is True
    assert flow["precloseout_failed_witnesses"] == 3
    assert flow["precloseout_passing_witnesses"] == 3
    assert flow["closeout_failed_witnesses"] == 0
    assert flow["closeout_passing_witnesses"] == 3
    assert len(flow["precloseout_pairs"]) == 2


def test_precloseout_overlay_retains_wrapper_lock_and_projection_failures() -> None:
    overlay = load(FINAL / "precloseout-operational-overlay.json")
    assert len(overlay["pairs"]) == 3
    assert len(overlay["failures"]) == 3
    assert len(overlay["recoveries"]) == 3
    for pair in overlay["pairs"]:
        assert pair["failure"]["state"] == "retained_failure"
        assert pair["failure"]["credit"] == 0
        assert (
            pair["recovery"]["does_not_erase"]
            == pair["failure"]["method_id"]
        )
    assert overlay["semantic_change"] is False
    assert overlay["successful_x2_aggregate_replayed"] is False
    assert overlay["repository_seal"] == SEALED
    assert overlay["external_canonical_success_in_repository_seal"] is False


def test_retained_negative_categories_sum_exactly() -> None:
    register = load(FINAL / "retained-negative-register.json")
    assert (
        sum(register["categories"].values())
        == SEALED["retained_failed_witnesses"]
    )
    assert register["effective_negatives"] == SEALED["effective_negatives"]
    assert register["zero_credit"] is True
    assert register["nonerasing"] is True


def test_open_gaps_and_exact_gates_remain_open() -> None:
    gaps = load(FINAL / "open-gap-register.json")
    gates = load(FINAL / "exact-gate-register.json")
    assert gaps["total"] == 389 and len(gaps["phase_local"]) == 3
    assert gates["total"] == 380 and len(gates["phase_local"]) == 3
    assert all(row["state"] == "open_gap" for row in gaps["phase_local"])
    assert all(row["state"] == "exact_gate" for row in gates["phase_local"])


def test_complete_incomplete_checklist_keeps_terminal_actions_separate() -> None:
    checklist = load(FINAL / "complete-incomplete-checklist.json")
    assert len(checklist["complete"]) >= 12
    assert "one exact-final canonical invocation" in checklist["incomplete"]
    assert (
        "live successor registry refresh and acknowledgement"
        in checklist["incomplete"]
    )


def test_wellbeing_check_preserves_limits_and_human_control() -> None:
    value = load(FINAL / "wellbeing-workload-check.json")
    assert value["status"] == "WITHIN_DECLARED_BOUNDS"
    assert (
        value["owner_file_stop"] == 2000
        and value["document_word_stop"] == 100000
    )
    assert value["no_biological_or_consciousness_inference"] is True
    assert value["human_pause_redirect_stop_control_preserved"] is True


def test_source_ledger_has_thirteen_current_sources_as_vocabulary_only() -> None:
    ledger = load(FINAL / "source-provenance-ledger.json")
    assert len(ledger["sources"]) == 13
    assert ledger["network_rows_ingested"] == 0
    assert ledger["citations_are_observations"] is False
    assert ledger["citations_are_authority_grants"] is False
    assert ledger["professional_or_legal_instruction_claim"] is False


def test_threat_model_is_bounded_and_nonexhaustive() -> None:
    threat = load(FINAL / "threat-model.json")
    assert len(threat["threats"]) == 8
    assert len(threat["controls"]) == 8
    assert threat["residual_risk"] == "open_gap_or_exact_gate"
    assert threat["exhaustive_security"] is False


def test_bounded_security_review_has_no_findings_or_promotion() -> None:
    review = load(FINAL / "bounded-security-review.json")
    assert review["reviewed_file_count"] >= 10
    assert review["syntax_parses"] == review["reviewed_file_count"]
    assert review["findings"] == []
    assert review["medium_or_high_findings"] == 0
    assert review["exhaustive_security"] is False
    assert review["production_certification"] is False


def test_environment_verifies_twenty_five_tools_without_installation() -> None:
    env = load(FINAL / "environment-version-receipt.json")
    assert len(env["system_python_distributions"]) == 8
    assert len(env["d_drive_auxiliary_python_distributions"]) == 6
    assert len(env["node_cli_tools"]) == 11
    assert env["all_versions_present"] is True
    assert env["installations_this_phase"] == 0
    assert env["global_promoted_skills"] == []
    assert env["global_skill_promotions"] == 0
    assert env["codex_desktop_updated"] is False
    assert env["elevation_or_reboot"] is False


def test_flashcard_closeout_has_four_tiers_and_135_cards() -> None:
    cards = load(FINAL / "flashcard-closeout.json")
    assert cards["card_count"] == 135
    assert cards["section_count"] >= 10
    assert cards["tier_order"] == [
        "freed_id_anchor",
        "trinity_pillar",
        "bounded_practice",
        "task",
    ]
    assert cards["content_addressed"] is True
    assert cards["supersession_non_erasing"] is True


def test_three_bounded_practices_and_one_successor_recommendation() -> None:
    value = load(FINAL / "bounded-practices.json")
    assert len(value["practices"]) == 3
    assert (
        isinstance(value["successor_recommendation"], str)
        and value["successor_recommendation"]
    )
    assert value["real_people_objects_records_or_actions"] == 0
    assert value["employment_qualification_competence_or_authority_claim"] is False


def test_pillar_label_is_consistent_without_rewriting_x1_or_x2() -> None:
    value = load(FINAL / "pillar-label-consistency.json")
    assert value["state"] == "CONSISTENT_NO_CORRECTION_REQUIRED"
    assert value["primary_pillar"] == "Freed ID and CBR Heart"
    assert value["protected_pillars"] == ["GMUT Mind", "THOS Body"]
    assert value["affected_file_count"] == 0
    assert value["correction_commit_required"] is False


def test_baton_integrity_word_bounds_and_prepared_state() -> None:
    receipt = load(FINAL / "baton-integrity.json")
    baton = (
        FINAL
        / "handoffs/sable-rook-v677-v8-activation-candidate.md"
    )
    raw = baton.read_bytes()
    assert receipt["bytes"] == len(raw)
    assert receipt["words"] == len(raw.decode("utf-8").split())
    assert 10000 <= receipt["words"] <= 100000
    assert receipt["sha256"] == hashlib.sha256(raw).hexdigest()
    assert receipt["state"] == "PREPARED_NOT_SENT"


def test_baton_is_sanitized_unsent_and_names_exact_route() -> None:
    baton = (
        FINAL
        / "handoffs/sable-rook-v677-v8-activation-candidate.md"
    ).read_text(encoding="utf-8")
    assert "PREPARED_NOT_SENT = true" in baton
    assert "SENT_BY_AUREN_LARK = false" in baton
    assert "Sable Rook" in baton and "v677-v8" in baton
    assert "Caelen Ash" in baton and "v678-v1" in baton
    assert "NOT_READY_FOR_STAGE_20" in baton
    assert "does not prove live delivery" in baton.lower()
    assert not re.search(r"(?i)[A-Z]:[\\/]+Users[\\/]+", baton)
    assert not re.search(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        baton,
        re.I,
    )


def test_accessible_report_has_structure_and_reserved_manual_review() -> None:
    report = (FINAL / "accessible-final-report.html").read_text(
        encoding="utf-8"
    )
    for token in (
        "<html",
        'lang="en"',
        "<header",
        "<nav",
        "<main",
        "<h1",
        "<h2",
        "<table",
        "<caption>",
    ):
        assert token in report
    for token in (
        "manual",
        "keyboard",
        "browser",
        "assistive-technology",
        "Māori-language",
        "affected-user",
    ):
        assert token.lower() in report.lower()


def test_route_state_is_prepared_unsent_without_precontact() -> None:
    route = load(FINAL / "route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["prospective_successor"] == "Sable Rook"
    assert route["prospective_phase"] == "v677-v8"
    assert route["next_after_successor"] == "Caelen Ash"
    assert route["prospective_next_after_successor_phase"] == "v678-v1"
    assert route["tavian_state"] == "ON_STANDBY"
    assert route["successor_precontacted"] is False
    assert route["send_count"] == 0


def test_lifecycle_replay_requires_three_direct_commits_and_zero_merges() -> None:
    replay = load(FINAL / "lifecycle-replay.json")
    assert (
        replay["source"] == SOURCE
        and replay["x1"] == X1
        and replay["evidence"] == EVIDENCE
    )
    assert replay["expected_new_commits"] == 3
    assert replay["expected_merges"] == 0
    assert replay["strict_x1_before_x2"] is True
    assert (
        replay["predecessor_canonical_or_sealed_components_replayed"]
        is False
    )


def test_content_seal_replays_each_declared_entry() -> None:
    seal = load(FINAL / "content-seal.json")
    assert seal["status"] == "SEALED_REPOSITORY_PREPARED_FINAL"
    assert seal["entry_count"] == len(seal["entries"])
    for row in seal["entries"]:
        raw = normalized(REPO / row["path"])
        assert len(raw) == row["bytes_normalized_lf"]
        assert (
            hashlib.sha256(raw).hexdigest()
            == row["sha256_normalized_lf"]
        )


def test_final_manifests_have_exact_unique_entries_and_self_exclusions() -> None:
    for name, status in (
        (
            "final-delta-manifest.json",
            "REPOSITORY_PREPARED_FINAL_DELTA",
        ),
        (
            "final-owner-manifest.json",
            "FINAL_OWNER_FROM_ILYRA_V677_V6_SOURCE",
        ),
    ):
        manifest = load(VALIDATION / name)
        paths = [row["path"] for row in manifest["entries"]]
        assert manifest["status"] == status
        assert manifest["entry_count"] == len(paths)
        assert len(paths) == len(set(paths))
        assert len(manifest["self_exclusions"]) == 4


def test_staged_review_has_zero_confirmed_privacy_hits() -> None:
    review = load(VALIDATION / "final-staged-review.json")
    assert (
        review["status"]
        == "VALID_REPOSITORY_PREPARED_FINAL_STAGED_REVIEW"
    )
    assert review["privacy_classes"] == 5
    assert review["confirmed_privacy_hits"] == []
    assert review["out_of_scope_paths"] == []
    assert review["x1_or_x2_paths_staged"] == []
    assert (
        review["final_tests"]
        == "SCHEDULED_ONCE_INSIDE_EXACT_FINAL_CANONICAL"
    )
    assert review["precanonical_final_test_run"] is False
    assert review["full_repository_suite"] is False
    assert review["independent_reproduction"] is False


def test_final_validation_prerequisites_fail_closed() -> None:
    value = load(FINAL / "final-validation-prerequisites.json")
    assert (
        value["source"] == SOURCE
        and value["x1"] == X1
        and value["evidence"] == EVIDENCE
    )
    assert value["exclusive_owner_canonical_invocation_limit"] == 1
    assert value["full_repository_suite_authorized"] is False
    assert value["route_send_before_canonical"] is False
    assert value["one_success_no_replay"] is True


def test_family_index_roster_and_orchestration_are_phase_scoped() -> None:
    index = load(FINAL / "family-index-update.json")
    roster = load(FINAL / "roster-auth-observation.json")
    orchestration = load(FINAL / "orchestration-record.json")
    assert index["proposal_chain"] == 8210
    assert (
        index["bounded_continuity_note_without_replacing_older_history"]
        is True
    )
    assert roster["observed_edge"] == "Auren Lark -> Sable Rook"
    assert roster["prospective_phase"] == "v677-v8"
    assert roster["next_after_successor"] == "Caelen Ash"
    assert roster["state"] == "PREPARED_NOT_SENT"
    assert orchestration["strict_x1_before_x2"] is True
    assert orchestration["canonical_invocation_limit_per_exact_final"] == 1
    assert orchestration["task_created_or_forked"] is False
    assert orchestration["collaboration_subagent_spawned"] is False


def test_closeout_receipt_is_nonpromotional_and_unsent() -> None:
    value = load(FINAL / "closeout-receipt.json")
    assert value["repository_seal"] == SEALED
    assert value["canonical_state"] == "PENDING_ONE_EXACT_FINAL_INVOCATION"
    assert value["external_canonical_success_in_repository_seal"] is False
    assert value["route_state"] == "PREPARED_NOT_SENT"
    assert value["real_world_rows"] == 0
    assert value["external_actions"] == 0
