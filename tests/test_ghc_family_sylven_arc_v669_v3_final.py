from __future__ import annotations

import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v669-v3"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_exact_final_truth_and_four_outcome_labels():
    truth = load("closeout/phase-truth.json")
    assert truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["effective_negatives"] == 30899
    assert truth["methods"] == 17004
    assert truth["failed_witnesses"] == 2720
    assert truth["passing_witnesses"] == 3832
    assert truth["open_gaps"] == 229
    assert truth["exact_gates"] == 224
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_novelty_recovery_gap_never_becomes_universal_claim():
    truth = load("closeout/phase-truth.json")
    audit = load("x1/semantic-novelty-audit.json")
    assert truth["accessible_novelty_rows"] == 1420
    assert truth["unrecovered_declared_rows"] == 3570
    assert truth["universal_novelty_claim"] is False
    assert audit["exact_title_collisions"] == 0
    assert audit["quarantined_proposals"] == 0


def test_retained_negative_and_method_flow_accounting():
    negatives = load("closeout/retained-negative-register.json")
    methods = load("closeout/method-flow-summary.json")
    assert negatives["inherited_activation"] + negatives["owner_operational"] + negatives["rejecting_mutations"] == negatives["effective"]
    assert negatives["erased"] == 0 and negatives["completion_credit_from_failures"] == 0
    assert methods["new_owner_methods"] == 172
    assert methods["new_positive_controls"] == 36


def test_lifecycle_anchors_and_strict_separation_contract():
    replay = load("closeout/lifecycle-replay.json")
    assert replay["source"] == "9c5b88ccde33130663859a3ffcb97188fa63efd7"
    assert replay["x1"] == "a8ce92245d170fa64bc4a484a0a074a9848496de"
    assert replay["evidence"] == "d5b00198c28178c5a00e5eb9ca839e08d1194ff7"
    assert replay["expected_new_commits"] == 3
    assert replay["expected_merges"] == 0
    assert replay["strict_x1_before_x2"] is True


def test_static_report_structural_accessibility_only():
    text = (ROOT / "closeout/static-report.html").read_text(encoding="utf-8")
    for token in ['<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"']:
        assert token in text
    checklist = load("closeout/complete-incomplete-checklist.json")
    assert any("accessibility" in item for item in checklist["incomplete"])


def test_handoff_is_large_file_backed_and_prepared_not_sent():
    integrity = load("closeout/handoff-integrity.json")
    route = load("closeout/route-state-final-candidate.json")
    baton = (REPO / integrity["path"]).read_text(encoding="utf-8")
    assert integrity["words"] == len(re.findall(r"\S+", baton))
    assert 10000 <= integrity["words"] <= 100000
    assert integrity["status"] == "PREPARED_NOT_SENT"
    assert route["sent"] is False and route["acknowledged"] is False
    assert route["precontacted"] is False and route["standby_contacted"] is False
    assert route["prospective_successor"] == "Caelen Morrow"


def test_tools_are_local_smoke_used_not_globally_installed():
    skills = load("tools/skill-smoke-receipt.json")
    quick = load("tools/skill-quick-validation-receipt.json")
    runners = load("tools/runner-smoke-receipt.json")
    assert skills["count"] == quick["count"] == runners["count"] == 10
    assert all(not row["global_installation"] and row["smoke_runner_passed"] for row in skills["rows"])
    assert all(row["passed"] for row in quick["rows"])
    assert all(row["result"]["passed"] for row in runners["rows"])


def test_zero_real_world_and_external_actions():
    truth = load("closeout/phase-truth.json")
    for key in ["real_people", "real_objects", "real_measurements", "network_calls", "external_actions", "authority_actions"]:
        assert truth[key] == 0
    assert truth["full_repository_suite"] == "not_run_Eiren_only"


def test_content_seal_replays_working_bytes_before_commit():
    import hashlib

    seal = load("seal/content-seal.json")
    for item in seal["files"]:
        data = (REPO / item["path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]


def test_canonical_protocol_is_one_shot_and_not_full_suite():
    protocol = load("validation/canonical-protocol.json")
    assert protocol["exclusive_invocation_limit"] == 1
    assert protocol["historical_x1_tests"] == "already_passed_at_exact_x1_head_not_replayed"
    assert protocol["full_repository_suite"] == "not_authorized_Eiren_only"
    assert protocol["success_policy"] == "never replay complete success"


def test_boundary_language_present_in_overview_and_baton():
    overview = (ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
    baton = (ROOT / "handoffs/caelen-morrow-v669-v4-activation-candidate.md").read_text(encoding="utf-8")
    required = ["NOT_READY_FOR_STAGE_20", "Māori concepts remain under Māori authority", "no universal novelty claim", "PREPARED_NOT_SENT"]
    combined = overview + "\n" + baton
    assert all(term in combined for term in required)


def test_closeout_caps_and_no_post_evidence_failures():
    wellbeing = load("closeout/wellbeing-workload-check.json")
    failures = load("closeout/post-evidence-operational-failures.json")
    assert all(wellbeing[key] is True for key in ["within_2000_file_ceiling", "within_100000_words_per_document", "within_8_commit_ceiling"])
    assert failures["count"] == 0 and failures["rows"] == []
