from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "docs" / "auren-lark" / "v672-v2" / "x1"
VALIDATION = ROOT / "docs" / "auren-lark" / "v672-v2" / "validation"
SOURCE = "40db1e418c1251e12d77f832c0890869b990dba5"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(name: str) -> dict:
    return json.loads((X1 / name).read_text(encoding="utf-8"))


def test_x1_is_planning_only_and_exact_source() -> None:
    truth = load("phase-truth.json")
    assert truth["state"] == "X1_PLANNING_ONLY"
    assert truth["x2_executed"] is False
    assert truth["source"] == SOURCE
    assert truth["proposal_chain_source"] == 5950
    assert truth["proposal_chain_if_x2_evidence_frozen"] == 5990
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert not (X1.parent / "x2").exists()


def test_proposal_freeze_has_exact_four_label_distribution() -> None:
    freeze = load("new-proposal-freeze.json")
    rows = freeze["proposals"]
    assert len(rows) == 40
    assert len({row["proposal_id"] for row in rows}) == 40
    outcomes = Counter(row["expected_outcome"] for row in rows)
    assert set(outcomes) == ALLOWED
    assert outcomes == Counter(
        {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    )
    assert all(row["x1_state"] == "planning_only_not_completion_credit" for row in rows)
    assert freeze["inherited_completion_credit"] == 0
    assert freeze["universal_novelty_claimed"] is False


def test_source_ledger_preserves_external_receipt_gap_and_official_limits() -> None:
    ledger = load("source-ledger.json")
    assert ledger["source_final"] == SOURCE
    assert ledger["source_canonical_replay_prohibited"] is True
    assert ledger["source_canonical_payload_state"].startswith("external_reference_only")
    assert ledger["external_receipt_payload_availability_gap"]["state"] == "open_gap"
    assert [source["status"] for source in ledger["official_sources"]] == [
        "current_stable_final",
        "current_stable_recommendation",
    ]
    assert ledger["official_sources"][0]["url"].startswith("https://csrc.nist.gov/")
    assert ledger["official_sources"][1]["url"].startswith("https://www.w3.org/")


def test_startup_failures_are_retained_and_counts_are_additive() -> None:
    flow = load("method-flow-startup.json")
    failures = flow["failed_witnesses"]
    assert len(failures) == 12
    assert len({row["failure_id"] for row in failures}) == 12
    assert all(row["state"] == "failed_retained_zero_credit_recovered" for row in failures)
    assert flow["source_baseline"]["effective_negatives"] == 35201
    assert flow["activation_overlay"]["effective_negatives"] == 35213
    assert flow["activation_overlay"]["effective_methods"] == 21844
    assert flow["activation_overlay"]["open_gaps"] == 277


def test_identity_and_route_boundaries_are_explicit() -> None:
    identity = load("identity-and-boundary.json")
    assert identity["working_language_only"] is True
    required = {
        "consciousness",
        "sentience",
        "legal_personhood",
        "identity_continuity",
        "employment",
        "professional_qualification",
        "scientific_authority",
        "operational_authority",
        "legal_authority",
        "cultural_authority",
        "maori_authority",
        "independent_agency",
    }
    assert set(identity["not_evidence_of"]) == required
    route = load("route-plan.json")
    assert route["state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
    assert route["next_exact_title"] == "Sable Rook"
    assert route["precontacted"] is False
    assert route["send_count"] == 0


def test_x1_manifest_matches_exact_utf8_bytes() -> None:
    receipt = load("build-receipt.json")
    assert receipt["state"] == "X1_PLANNING_ONLY"
    assert receipt["manifest_entries"] == len(receipt["manifest"])
    for row in receipt["manifest"]:
        path = ROOT / row["path"]
        data = path.read_bytes()
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_overview_is_substantive_and_keeps_stage20_closed() -> None:
    overview = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
    assert len(re.findall(r"\S+", overview)) >= 700
    assert "NOT_READY_FOR_STAGE_20" in overview
    assert "planning-only" in overview
    assert "independent reproduction" in overview


def test_x1_staged_review_is_valid_when_present() -> None:
    path = VALIDATION / "x1-staged-review.json"
    if not path.exists():
        return
    review = json.loads(path.read_text(encoding="utf-8"))
    assert review["valid"] is True
    assert review["lifecycle"] == "X1_PLANNING_ONLY"
    assert review["deletions"] == []
    assert review["out_of_scope"] == []
    assert review["x2_paths"] == []
    assert review["confirmed_privacy_candidates"] == []
    assert review["working_index_mismatches"] == []
