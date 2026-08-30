from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "docs/sylven-arc/v678-v6/correction1"
VALIDATOR = ROOT / "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py"
FIRST_FINAL = "ea27f954b8636f167c83b964c0ba5ad15301ea1e"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_01_correction_is_additive_to_exact_first_final():
    value = load(CORRECTION / "correction-truth.json")
    assert value["first_final"] == FIRST_FINAL
    assert value["parent"] == FIRST_FINAL
    assert value["corrected_final"] == "BOUND_AT_COMMIT"
    assert value["first_final_history_rewritten"] is False


def test_02_no_canonical_or_latch_was_spent_before_correction():
    value = load(CORRECTION / "canonical-preflight-state.json")
    assert value["canonical_invocation_count"] == 0
    assert value["canonical_success_count"] == 0
    assert value["canonical_replay_count"] == 0
    assert value["receipt_absent"] is True
    assert value["latch_absent"] is True


def test_03_method_flow_preserves_failure_and_recovery_separately():
    value = load(CORRECTION / "method-flow-overlay.json")
    assert value["new_failed_witnesses"] == 1
    assert value["new_passing_witnesses"] == 1
    assert value["new_methods"] == 2
    assert value["failure_erasure_forbidden"] is True
    assert value["overlay"] == {
        "effective_negatives": 47283, "effective_methods": 45392,
        "retained_failed_witnesses": 18944, "bounded_passing_witnesses": 29533,
        "open_gaps": 410, "exact_gates": 401,
    }


def test_04_validator_forbids_dynamic_execution_but_allows_compile_only_check():
    source = VALIDATOR.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assignments = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)]
    forbidden = None
    for node in assignments:
        if any(isinstance(target, ast.Name) and target.id == "forbidden_calls" for target in node.targets):
            forbidden = ast.literal_eval(node.value)
            break
    assert forbidden == {"eval", "exec", "__import__"}
    assert 'compile(source, path, "exec")' in source


def test_05_validator_binds_first_final_and_correction_manifests():
    source = VALIDATOR.read_text(encoding="utf-8")
    assert 'FIRST_FINAL = "ea27f954b8636f167c83b964c0ba5ad15301ea1e"' in source
    assert "ghc_family_sylven_arc_v678_v6_final_manifest.py" in source
    assert "ghc_family_sylven_arc_v678_v6_correction1_manifest.py" in source
    assert 'topo["phase_commits"] == 4' in source


def test_06_correction_preserves_route_and_stage20_holds():
    value = load(CORRECTION / "correction-truth.json")
    assert value["route_state"] == "PREPARED_NOT_SENT"
    assert value["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    text = (CORRECTION / "receipt-contract-correction.md").read_text(encoding="utf-8")
    assert "Māori-authority" in text
    assert "No canonical command was invoked" in text


def test_07_correction_manifests_and_seal_are_present():
    for relative in (
        "../validation/correction1-delta-manifest.json",
        "../validation/correction1-owner-manifest.json",
        "../validation/correction1-staged-review.json",
        "correction1-content-seal.json",
    ):
        assert (CORRECTION / relative).resolve().is_file()


def test_08_correction_json_parses_and_remains_bounded():
    paths = list(CORRECTION.glob("*.json"))
    assert len(paths) >= 4
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))
    for path in CORRECTION.glob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100000
