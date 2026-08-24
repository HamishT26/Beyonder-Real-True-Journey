from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v668-v6"
SOURCE = "5bced658a5b3f5bd7c4d88d47057d795abe57f42"
X1 = "c5c18b81f26c8851b984e4bcb3dff1db1212fd36"
EVIDENCE = "d42953afd61753490e9c77138409e179d44974d8"
FIRST_FINAL = "4e87a72ab4f796854b7d2bee30c0143ae91887e2"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def test_first_final_and_immutable_anchors_are_retained() -> None:
    assert git("rev-parse", FIRST_FINAL) == FIRST_FINAL
    assert git("rev-parse", f"{FIRST_FINAL}^") == EVIDENCE
    assert git("rev-parse", f"{EVIDENCE}^") == X1
    assert git("rev-parse", f"{X1}^") == SOURCE
    assert git("rev-list", "--merges", f"{SOURCE}..{FIRST_FINAL}") == ""


def test_privacy_self_match_correction_is_exact() -> None:
    correction = load("correction/privacy-self-match-correction.json")
    assert correction["conceptual_scanner_definitions"] == 2
    assert correction["actual_raw_pattern_self_matches"] == 1
    assert correction["actual_scanner_definition_self_matches"] == 1
    assert correction["confirmed_payload_hits"] == 0
    assert correction["privacy_complete"] is False
    test_source = subprocess.run(
        ["git", "show", f"{FIRST_FINAL}:tests/test_ghc_family_caelen_ash_v668_v6_x2.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    class_two = re.compile((b"source_" + b"thread_id" + rb"\s*[:=]"), re.I)
    class_five = re.compile((b"response" + b"_item"), re.I)
    assert class_two.search(test_source) is None
    assert class_five.search(test_source) is not None


def test_failed_validation_invocations_keep_zero_credit() -> None:
    retained = load("correction/retained-validation-failures.json")
    assert [row["id"] for row in retained["failures"]] == ["CA6686-N025", "CA6686-N026", "CA6686-N027", "CA6686-N028"]
    assert all(row["status"] == "failed_zero_credit" for row in retained["failures"])
    assert retained["canonical_invocations"] == 1
    assert retained["canonical_successes"] == 0
    assert retained["canonical_replayed"] is False
    assert retained["first_composite_replayed"] is False


def test_corrected_truth_preserves_labels_counts_and_terminal_boundary() -> None:
    truth = load("correction/phase-truth.json")
    assert truth["allowed_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"]
    assert truth["outcome_counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["frozen_proposal_chain"] == 4830
    assert truth["repository_sealed_counts"] == {
        "effective_negatives": 29959,
        "methods": 16545,
        "failed_witnesses": 2260,
        "passing_witnesses": 3087,
        "open_gaps": 219,
        "exact_gates": 214,
    }
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_method_flow_overlay_retains_each_failure_and_recovery() -> None:
    overlay = load("correction/method-flow-overlay.json")
    assert len(overlay["methods"]) == 4
    assert all(row["failure_retained"] is True for row in overlay["methods"])
    assert len({row["failed_witness"] for row in overlay["methods"]}) == 4
    assert len({row["passing_witness"] for row in overlay["methods"]}) == 4


def test_corrected_route_remains_prepared_and_unsent() -> None:
    route = load("route/prepared-route-state-correction.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_contacted"] is False
    assert route["single_send_maximum"] == 1
    assert route["canonical_success_count"] == 0
    assert route["corrected_terminal_composite"] == "PENDING"


def test_correction_manifests_are_bounded_and_self_exclusions_are_explicit() -> None:
    delta = load("validation/correction-delta-manifest.json")
    owner = load("validation/correction-owner-manifest.json")
    assert delta["expected_parent"] == FIRST_FINAL
    assert delta["entry_count"] == len(delta["entries"]) == 10
    assert owner["entry_count"] == len(owner["entries"])
    assert owner["entry_count"] < 2000
    assert len({row["path"] for row in owner["entries"]}) == owner["entry_count"]
    assert owner["self_exclusions"] == ["docs/caelen-ash/v668-v6/validation/correction-owner-manifest.json"]


def test_correction_documents_are_bounded_and_claim_care_is_visible() -> None:
    paths = [
        PHASE / "correction" / "terminal-correction-overview.md",
        PHASE / "handoffs" / "successor-terminal-correction-basis.md",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert 120 <= len(text.split()) <= 6000
        assert "NOT_READY_FOR_STAGE_20" in text
        assert "zero" in text.lower()
