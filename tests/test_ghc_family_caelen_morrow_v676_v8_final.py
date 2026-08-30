from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/caelen-morrow/v676-v8"
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
SOURCE = "56075d91265e71ce9165670db78ef455c29d5e2f"
X1 = "5d7e2cea2c77b8a79a6e0e1d72aa349d9c6fbc2b"
EVIDENCE = "81a216207416f6cc10d18b7927818a36ca3e897d"
SEALED = {
    "effective_negatives": 43513,
    "effective_methods": 36411,
    "retained_failed_witnesses": 15174,
    "bounded_passing_witnesses": 21928,
    "open_gaps": 368,
    "exact_gates": 359,
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_final_phase_truth_has_exact_anchors_and_verdict() -> None:
    truth = load(FINAL / "phase-truth.json")
    assert truth["source"] == SOURCE
    assert truth["x1"] == X1
    assert truth["evidence"] == EVIDENCE
    assert truth["exact_final"] == "COMMIT_CONTAINING_THIS_FILE"
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["canonical_state"] == "PENDING_ONE_EXTERNAL_EXACT_FINAL_INVOCATION"
    assert truth["route_state"] == "PREPARED_NOT_SENT"


def test_repository_seal_is_exact_and_nonpromotional() -> None:
    truth = load(FINAL / "phase-truth.json")
    for key, value in SEALED.items():
        assert truth[key] == value
    assert truth["real_world_rows"] == 0
    assert truth["external_real_world_actions"] == 0


def test_outcome_partition_uses_only_four_labels() -> None:
    outcomes = load(FINAL / "phase-truth.json")["outcomes"]
    assert outcomes == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    assert sum(outcomes.values()) == 60


def test_method_flow_preserves_failure_nonerasure() -> None:
    flow = load(FINAL / "method-flow-final.json")
    assert flow["repository_seal"] == SEALED
    assert flow["failure_nonerasure"] is True
    assert flow["recovery_never_retroactively_promotes_failure"] is True
    assert flow["closeout_failed_witnesses"] == 4
    assert flow["closeout_passing_witnesses"] == 4
    assert flow["closeout_pairs"][0]["failure_id"] == "CM6768-FINAL-N001"
    assert flow["closeout_pairs"][0]["failure_credit"] == 0
    assert flow["closeout_pairs"][1]["failure_id"] == "CM6768-FINAL-N002"
    assert flow["closeout_pairs"][1]["failure_credit"] == 0
    assert flow["closeout_pairs"][2]["failure_id"] == "CM6768-FINAL-N003"
    assert flow["closeout_pairs"][2]["failure_credit"] == 0
    assert flow["closeout_pairs"][3]["failure_id"] == "CM6768-FINAL-N004"
    assert flow["closeout_pairs"][3]["failure_credit"] == 0


def test_retained_negative_register_matches_seal() -> None:
    register = load(FINAL / "retained-negative-register.json")
    assert register["effective_negatives"] == SEALED["effective_negatives"]
    assert register["retained_failed_witnesses"] == SEALED["retained_failed_witnesses"]
    assert register["zero_credit"] is True
    assert register["nonerasing"] is True


def test_open_and_exact_gate_totals_remain_open() -> None:
    gaps = load(FINAL / "open-gap-register.json")
    gates = load(FINAL / "exact-gate-register.json")
    assert gaps["total"] == 368 and len(gaps["phase_local"]) == 3
    assert gates["total"] == 359 and len(gates["phase_local"]) == 3
    assert all(row["state"] == "open_gap" for row in gaps["phase_local"])
    assert all(row["state"] == "exact_gate" for row in gates["phase_local"])


def test_complete_incomplete_checklist_keeps_terminal_work_separate() -> None:
    checklist = load(FINAL / "complete-incomplete-checklist.json")
    assert len(checklist["complete"]) >= 10
    assert "external exact-final canonical invocation" in checklist["incomplete"]
    assert "live successor registry refresh and acknowledgement" in checklist["incomplete"]


def test_wellbeing_and_workload_receipt_preserves_human_control() -> None:
    value = load(FINAL / "wellbeing-workload-check.json")
    assert value["status"] == "WITHIN_DECLARED_BOUNDS"
    assert value["owner_file_stop"] == 2000
    assert value["document_word_stop"] == 100000
    assert value["no_biological_or_consciousness_inference"] is True
    assert value["human_pause_redirect_stop_control_preserved"] is True


def test_source_ledger_uses_citations_as_vocabulary_only() -> None:
    ledger = load(FINAL / "source-provenance-ledger.json")
    assert len(ledger["sources"]) == 8
    assert ledger["network_rows_ingested"] == 0
    assert ledger["citations_are_observations"] is False
    assert ledger["citations_are_authority_grants"] is False
    assert ledger["professional_or_legal_instruction_claim"] is False


def test_threat_model_retains_residual_risk_and_nonexhaustive_security() -> None:
    threat = load(FINAL / "threat-model.json")
    assert len(threat["threats"]) >= 7
    assert len(threat["controls"]) >= 7
    assert threat["residual_risk"] == "open_gap_or_exact_gate"
    assert threat["exhaustive_security"] is False


def test_environment_receipt_verifies_twenty_five_tools_without_installation() -> None:
    env = load(FINAL / "environment-version-receipt.json")
    assert len(env["system_python_distributions"]) == 8
    assert len(env["d_drive_auxiliary_python_distributions"]) == 6
    assert len(env["node_cli_tools"]) == 11
    assert env["all_versions_present"] is True
    assert env["installations_this_phase"] == 0
    assert env["global_promoted_skills"] == []
    assert env["global_skill_promotions"] == 0
    assert isinstance(env["codex_cli"], str) and env["codex_cli"]
    assert env["codex_desktop_updated"] is False
    assert env["elevation_or_reboot"] is False


def test_flashcard_closeout_has_four_tiers_and_135_cards() -> None:
    cards = load(FINAL / "flashcard-closeout.json")
    assert cards["card_count"] == 135
    assert cards["section_count"] == 14
    assert cards["tier_order"] == ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"]
    assert cards["content_addressed"] is True
    assert cards["supersession_non_erasing"] is True


def test_baton_integrity_replays_and_word_bounds_hold() -> None:
    receipt = load(FINAL / "baton-integrity.json")
    baton = FINAL / "handoffs/eiren-kestrel-v677-v1-activation-candidate.md"
    raw = baton.read_bytes()
    assert receipt["bytes"] == len(raw)
    assert receipt["words"] == len(raw.decode("utf-8").split())
    assert 10000 <= receipt["words"] <= 100000
    assert receipt["sha256"] == hashlib.sha256(raw).hexdigest()
    assert receipt["state"] == "PREPARED_NOT_SENT"


def test_baton_is_sanitized_prepared_state_not_delivery() -> None:
    baton = (FINAL / "handoffs/eiren-kestrel-v677-v1-activation-candidate.md").read_text(encoding="utf-8")
    assert "PREPARED_NOT_SENT = true" in baton
    assert "SENT_BY_CAELEN_MORROW = false" in baton
    assert "does not prove live delivery" in baton.lower()
    assert "NOT_READY_FOR_STAGE_20" in baton
    assert not re.search(r"(?i)[A-Z]:[\\/]+Users[\\/]+", baton)
    assert not re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", baton, re.I)


def test_accessible_report_has_landmarks_table_caption_and_reserved_reviews() -> None:
    report = (FINAL / "accessible-final-report.html").read_text(encoding="utf-8")
    for token in ("<html", 'lang="en"', "<header", "<nav", "<main", "<h1", "<h2", "<table", "<caption>"):
        assert token in report
    for token in ("manual", "browser", "keyboard", "assistive-technology", "Māori-language", "affected-user"):
        assert token.lower() in report.lower()


def test_route_state_is_unsent_and_tavian_is_standby() -> None:
    route = load(FINAL / "route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["prospective_successor"] == "Eiren Kestrel"
    assert route["prospective_phase"] == "v677-v1"
    assert route["tavian_state"] == "ON_STANDBY"
    assert route["successor_precontacted"] is False
    assert route["send_count"] == 0


def test_lifecycle_replay_requires_three_direct_commits_and_zero_merges() -> None:
    replay = load(FINAL / "lifecycle-replay.json")
    assert replay["source"] == SOURCE
    assert replay["x1"] == X1
    assert replay["evidence"] == EVIDENCE
    assert replay["expected_new_commits"] == 3
    assert replay["expected_merges"] == 0
    assert replay["strict_x1_before_x2"] is True
    assert replay["sylven_failed_canonical_or_corrected_composite_replayed"] is False


def test_content_seal_replays_every_declared_entry() -> None:
    seal = load(FINAL / "content-seal.json")
    assert seal["status"] == "SEALED_REPOSITORY_PREPARED_FINAL"
    assert seal["entry_count"] == len(seal["entries"])
    for row in seal["entries"]:
        path = REPO / row["path"]
        assert hashlib.sha256(normalized(path)).hexdigest() == row["sha256_normalized_lf"]


def test_final_manifests_have_no_duplicate_paths() -> None:
    for name in ("final-delta-manifest.json", "final-owner-manifest.json"):
        manifest = load(VALIDATION / name)
        paths = [row["path"] for row in manifest["entries"]]
        assert manifest["entry_count"] == len(paths)
        assert len(paths) == len(set(paths))


def test_final_artifacts_have_no_private_path_or_raw_task_identifier_payload() -> None:
    forbidden = [
        re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)(source_thread_id|clientThreadId)"),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    ]
    hits = []
    for path in sorted(FINAL.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
            text = path.read_text(encoding="utf-8")
            if any(pattern.search(text) for pattern in forbidden):
                hits.append(path.relative_to(REPO).as_posix())
    assert hits == []


def test_final_validation_prerequisites_fail_closed_before_external_canonical() -> None:
    value = load(FINAL / "final-validation-prerequisites.json")
    assert value["source"] == SOURCE
    assert value["x1"] == X1
    assert value["evidence"] == EVIDENCE
    assert value["exclusive_owner_canonical_invocation_limit"] == 1
    assert value["full_repository_suite_authorized"] is False
    assert value["route_send_before_canonical"] is False


def test_closeout_receipt_preserves_prepared_not_sent_state() -> None:
    value = load(FINAL / "closeout-receipt.json")
    assert value["repository_seal"] == SEALED
    assert value["canonical_state"] == "PENDING_EXTERNAL_EXACT_FINAL_INVOCATION"
    assert value["route_state"] == "PREPARED_NOT_SENT"
    assert value["real_world_rows"] == 0
    assert value["external_actions"] == 0
