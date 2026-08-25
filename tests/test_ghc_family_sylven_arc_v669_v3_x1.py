from __future__ import annotations

import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from ghc_family_sylven_arc_v669_v3_archive import (  # noqa: E402
    ACCESSIBLE_WITH_ELOWEN,
    CHAIN_AFTER,
    OWNER_ROOT,
    PROTECTED_GATES,
    SOURCE_CHAIN_DECLARED,
)


def load(rel: str):
    return json.loads((REPO / OWNER_ROOT / rel).read_text(encoding="utf-8"))


def proposal_rows():
    freeze = load("x1/proposal-freeze.json")
    rows = []
    for rel in freeze["shards"]:
        rows.extend(json.loads((REPO / rel).read_text(encoding="utf-8"))["rows"])
    return rows


def test_exactly_forty_complete_contracts():
    rows = proposal_rows()
    assert len(rows) == 40
    required = {
        "proposal_id",
        "title",
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
    assert all(required <= row.keys() for row in rows)
    assert all(len(row["negative_fixtures"]) == 4 for row in rows)


def test_novelty_is_bounded_and_gap_is_visible():
    audit = load("x1/semantic-novelty-audit.json")
    assert audit["declared_inherited_frozen_proposals"] == SOURCE_CHAIN_DECLARED
    assert audit["accessible_comparison_rows"] == ACCESSIBLE_WITH_ELOWEN
    assert audit["unrecovered_declared_rows"] == 3570
    assert audit["unavailable_history_is_open_gap"] is True
    assert audit["universal_novelty_claim"] is False
    assert audit["exact_title_collisions"] == 0
    assert audit["quarantined_proposals"] == 0


def test_planned_outcomes_and_chain():
    freeze = load("x1/proposal-freeze.json")
    rows = proposal_rows()
    assert freeze["proposal_chain_after"] == CHAIN_AFTER
    assert freeze["expected_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    counts = {label: sum(row["expected_disposition"] == label for row in rows) for label in freeze["expected_outcomes"]}
    assert counts == freeze["expected_outcomes"]
    assert all(row["observed_disposition"] is None for row in rows)


def test_portfolio_floors_and_held_packets():
    freeze = load("x1/portfolio-freeze.json")
    assert freeze["counts"] == {
        "safe_now": 30,
        "candidate": 15,
        "skill": 10,
        "runner": 10,
        "clean_fix_refine": 30,
        "exact_approval": 10,
        "blocked": 5,
    }
    assert all(row["execution_state"] == "held_unexecuted" for row in freeze["rows"]["exact_approval"] + freeze["rows"]["blocked"])


def test_protected_gates_and_zero_x1_credit():
    rows = proposal_rows()
    assert all(row["protected_gates"] == PROTECTED_GATES for row in rows)
    assert all(row["x1_completion_credit"] == 0 for row in rows)
    phase = load("x1/phase-truth.json")
    assert phase["observed_outcomes"] is None
    assert phase["canonical_validation"] == "not_run_x1"
    assert phase["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_x1_manifest_replays_working_tree_bytes():
    manifest = load("validation/x1-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    for entry in manifest["entries"]:
        data = (REPO / entry["path"]).read_bytes()
        import hashlib

        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_x1_paths_have_no_x2_or_outcome_artifacts():
    owner_files = [path.relative_to(REPO).as_posix() for path in (REPO / OWNER_ROOT).rglob("*") if path.is_file()]
    assert not any("/x2/" in path or "/closeout/" in path or "/seal/" in path for path in owner_files)
    assert not any("observed_disposition\"" in path for path in owner_files)
