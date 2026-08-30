from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "elowen-cairn" / "v678-v5"
CORRECTION = BASE / "correction1"
FIRST_FINAL = "831f948e326e3875ef0d5d7391560297ce0e2ee8"
FAILED_RECEIPT_SHA256 = "bfa2115b166ee9eb5f3f9aaac9a4d7f5379e574a24ac4dc60bc7b8accf758ccd"
FAILED_PAYLOAD_SHA256 = "36f8a96bb375543e02e6095e34002dbef4bb83b78d51d25095b59b889ed66507"


def load(name: str):
    return json.loads((CORRECTION / name).read_text(encoding="utf-8"))


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_failed_canonical_is_bound_and_never_promoted() -> None:
    binding = load("failed-canonical-binding.json")
    assert binding["first_final"] == FIRST_FINAL
    assert binding["receipt_sha256"] == FAILED_RECEIPT_SHA256
    assert binding["canonical_payload_sha256"] == FAILED_PAYLOAD_SHA256
    assert binding["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
    assert binding["invocation_count"] == 1
    assert binding["success_count"] == 0
    assert binding["replay_count"] == 0
    assert binding["failed_checks"] == ["documents_structurally_bounded"]
    assert binding["passed_test_count"] == 34
    assert binding["passed_json_parse_count"] == 642
    assert binding["passed_manifest_entry_count"] == 1412
    assert binding["successful_components_replay_forbidden"] is True


def test_correction_truth_method_flow_and_policy_are_narrow() -> None:
    truth = load("phase-truth.json")
    overlay = load("method-flow-overlay.json")
    policy = load("validation-policy.json")
    assert truth["retained_first_final"] == FIRST_FINAL
    assert truth["failed_canonical_success_credit"] == 0
    assert truth["failed_canonical_replayed"] is False
    assert truth["successful_canonical_components_replayed"] is False
    assert truth["repository_corrected_phase_ledger_counts"] == {"methods": 813, "failed": 277, "passing": 536}
    assert truth["repository_overlay"] == {
        "effective_negatives": 47003,
        "effective_methods": 44555,
        "retained_failed_witnesses": 18664,
        "bounded_passing_witnesses": 28976,
        "open_gaps": 407,
        "exact_gates": 398,
    }
    assert truth["core_outcomes_unchanged"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert overlay["failed_canonical_promoted"] is False
    assert overlay["failure_erasure"] is False
    assert len(overlay["methods"]) == 3
    assert sum(row["truth"] is False for row in overlay["methods"]) == 2
    assert sum(row["truth"] is True for row in overlay["methods"]) == 1
    assert policy["failed_dependency"] == "documents_structurally_bounded"
    assert policy["successful_component_replay_forbidden"] is True
    assert policy["complete_repository_suite_forbidden"] is True


def test_correction_seal_and_route_overlay_are_prepared_not_sent() -> None:
    seal = load("content-seal.json")
    assert len(seal["entries"]) == 7
    for row in seal["entries"]:
        path = REPO / row["path"]
        assert hashlib.sha256(normalized(path.read_bytes())).hexdigest() == row["sha256_normalized_lf"]
    route = load("terminal-route-overlay.json")
    assert route["state"] == "HELD_PENDING_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPONENT"
    assert route["provisional_exact_title"] == "Sylven Arc"
    assert route["provisional_phase"] == "v678-v6"
    assert route["precontact_performed"] is False
    assert route["send_count"] == 0
    baton = (CORRECTION / "sylven-arc-v678-v6-activation-candidate-corrected1.md").read_text(encoding="utf-8")
    assert "PREPARED NOT SENT" in baton
    assert "SENT_BY_ELOWEN_CAIRN = false" in baton
    assert "Sylven Arc" in baton and "v678-v6" in baton
