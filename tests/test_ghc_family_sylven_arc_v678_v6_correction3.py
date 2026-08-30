from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "docs/sylven-arc/v678-v6/correction3"
VALIDATOR = ROOT / "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py"
COMPOSITE = ROOT / "scripts/validate_ghc_family_sylven_arc_v678_v6_correction3_composite.py"
BASE = "706292a287ed36b892d97d80c9571e7a1d8b8ded"
FAILED_RECEIPT = "06e5b4d462ac51765d914e1f6e1d48d8831229dc24918daaee2eea97d63aa16e"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_01_correction3_is_additive_to_correction2():
    value = load(CORRECTION / "correction-truth.json")
    assert value["correction2"] == BASE
    assert value["parent"] == BASE
    assert value["corrected_final"] == "BOUND_AT_COMMIT"
    assert value["repair"]["history_rewritten"] is False


def test_02_failed_canonical_is_immutable_and_zero_credit():
    value = load(CORRECTION / "correction-truth.json")["failed_canonical"]
    assert value["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
    assert value["receipt_sha256"] == FAILED_RECEIPT
    assert value["invocation_count"] == 1
    assert value["success_count"] == 0
    assert value["replay_count"] == 0
    assert (value["tests_passed"], value["tests_total"]) == (40, 41)


def test_03_method_flow_preserves_canonical_and_patch_failures():
    value = load(CORRECTION / "method-flow-overlay.json")
    assert value["new_failed_witnesses"] == 2
    assert value["new_passing_witnesses"] == 1
    assert value["new_methods"] == 3
    assert value["overlay"] == {
        "effective_negatives": 47293,
        "effective_methods": 45413,
        "retained_failed_witnesses": 18954,
        "bounded_passing_witnesses": 29544,
        "open_gaps": 410,
        "exact_gates": 401,
    }


def test_04_historical_topology_tests_use_immutable_git_trees():
    first = (ROOT / "tests/test_ghc_family_sylven_arc_v678_v6_correction1.py").read_text(encoding="utf-8")
    second = (ROOT / "tests/test_ghc_family_sylven_arc_v678_v6_correction2.py").read_text(encoding="utf-8")
    assert "git_text(CORRECTION1" in first
    assert "git_text(CORRECTION2" in second
    assert "subprocess.run" in first and "subprocess.run" in second


def test_05_current_validator_binds_six_commit_correction3_topology():
    source = VALIDATOR.read_text(encoding="utf-8")
    assert 'CORRECTION2 = "706292a287ed36b892d97d80c9571e7a1d8b8ded"' in source
    assert "ghc_family_sylven_arc_v678_v6_correction3_manifest.py" in source
    assert 'topo["phase_commits"] == 6' in source
    assert '"49 passed"' in source


def test_06_composite_is_narrow_and_never_promotes_canonical_failure():
    source = COMPOSITE.read_text(encoding="utf-8")
    assert "test_05_validator_binds_first_final_and_correction_manifests" in source
    assert "test_04_validator_adjudicates_exact_manifest_definitions" in source
    assert "tests/test_ghc_family_sylven_arc_v678_v6_correction3.py" in source
    assert "ZERO_FAILED_CANONICAL_CREDIT" in source
    assert '"canonical_success": False' in source


def test_07_correction3_manifests_and_seal_are_present():
    for relative in (
        "../validation/correction3-delta-manifest.json",
        "../validation/correction3-owner-manifest.json",
        "../validation/correction3-staged-review.json",
        "correction3-content-seal.json",
    ):
        assert (CORRECTION / relative).resolve().is_file()


def test_08_route_and_authority_gates_remain_closed():
    truth = load(CORRECTION / "correction-truth.json")
    assert truth["route_state"] == "PREPARED_NOT_SENT"
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    text = (CORRECTION / "dependency-recovery-plan.md").read_text(encoding="utf-8")
    for boundary in ("independent reproduction", "Māori authority", "Stage 20 authority"):
        assert boundary in text
