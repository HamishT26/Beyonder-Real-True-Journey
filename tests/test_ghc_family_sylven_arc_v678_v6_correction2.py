from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "docs/sylven-arc/v678-v6/correction2"
FLASHCARDS = ROOT / "scripts/ghc_family_sylven_arc_v678_v6_flashcards.py"
VALIDATOR = ROOT / "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py"
BASE = "79c42c6158c9799344e16a9ed5fc49092422b698"
CORRECTION2 = "706292a287ed36b892d97d80c9571e7a1d8b8ded"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(ref: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout


def test_01_correction2_is_additive_to_correction1():
    value = load(CORRECTION / "correction-truth.json")
    assert value["correction1"] == BASE
    assert value["parent"] == BASE
    assert value["corrected_final"] == "BOUND_AT_COMMIT"
    assert value["history_rewritten"] is False


def test_02_failed_static_audit_is_retained_without_canonical_credit():
    value = load(CORRECTION / "correction-truth.json")
    audit = value["failed_static_audit"]
    assert audit["status"] == "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT"
    assert audit["canonical_invoked"] is False
    assert audit["privacy_confirmed_or_unresolved_candidates"] == 4
    assert audit["code_findings"] == 1
    assert audit["immutable_manifest_replays_passed"] == 3


def test_03_explicit_counter_import_replaces_dynamic_import():
    source = FLASHCARDS.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module == "collections"]
    assert any(any(alias.name == "Counter" for alias in node.names) for node in imports)
    assert '__import__("collections")' not in source
    assert "Counter(card[\"outcome\"] for card in cards)" in source


def test_04_validator_adjudicates_exact_manifest_definitions():
    source = git_text(CORRECTION2, "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py")
    for name in (
        "ghc_family_sylven_arc_v678_v6_x1_manifest.py",
        "ghc_family_sylven_arc_v678_v6_correction1_manifest.py",
        "ghc_family_sylven_arc_v678_v6_correction2_manifest.py",
    ):
        assert name in source
    assert 'topo["phase_commits"] == 5' in source


def test_05_method_flow_preserves_all_correction2_failures_and_recoveries():
    value = load(CORRECTION / "method-flow-overlay.json")
    assert value["new_failed_witnesses"] == 8
    assert value["new_passing_witnesses"] == 10
    assert value["new_methods"] == 18
    assert value["overlay"] == {
        "effective_negatives": 47291, "effective_methods": 45410,
        "retained_failed_witnesses": 18952, "bounded_passing_witnesses": 29543,
        "open_gaps": 410, "exact_gates": 401,
    }


def test_06_no_canonical_receipt_or_latch_was_spent():
    value = load(CORRECTION / "canonical-preflight-state.json")
    assert value["canonical_invocation_count"] == 0
    assert value["receipt_absent"] is True
    assert value["latch_absent"] is True
    assert value["route_state"] == "PREPARED_NOT_SENT"


def test_07_correction2_manifests_and_seal_exist():
    for relative in (
        "../validation/correction2-delta-manifest.json",
        "../validation/correction2-owner-manifest.json",
        "../validation/correction2-staged-review.json",
        "correction2-content-seal.json",
    ):
        assert (CORRECTION / relative).resolve().is_file()


def test_08_correction2_preserves_authority_and_stage20_holds():
    value = load(CORRECTION / "correction-truth.json")
    assert value["route_state"] == "PREPARED_NOT_SENT"
    assert value["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    text = (CORRECTION / "static-audit-correction.md").read_text(encoding="utf-8")
    assert "Māori-authority" in text
    assert "No canonical aggregate, receipt, or latch" in text
