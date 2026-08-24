from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from collections import Counter
from pathlib import Path

import pytest

from scripts.ghc_family_vesper_arlen_v668_v1_causal import (
    ContractError,
    append_compensation,
    bounded_queue,
    merkle_root,
    migrate_record,
    minimize_note,
    replay_events,
    replay_with_duplicates,
    validate_event_graph,
    validate_logical_clocks,
    validation_credit_transition,
    verify_checkpoint,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v668-v1"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def events():
    return [
        {"event_id": "a", "depends_on": [], "source": "one", "source_sequence": 1, "lamport": 1, "action": "cue", "cue": "a"},
        {"event_id": "b", "depends_on": ["a"], "source": "two", "source_sequence": 1, "lamport": 2, "action": "ack", "target": "a"},
        {"event_id": "c", "depends_on": ["b"], "source": "one", "source_sequence": 2, "lamport": 3, "action": "stop"},
    ]


def test_graph_order_is_stable():
    assert validate_event_graph(events()) == ["a", "b", "c"]


@pytest.mark.parametrize("mutator", [
    lambda rows: rows + [dict(rows[0])],
    lambda rows: [{**rows[0], "depends_on": ["missing"]}, *rows[1:]],
    lambda rows: [{**rows[0], "depends_on": ["c"]}, *rows[1:]],
    lambda rows: [{**rows[0], "event_id": ""}, *rows[1:]],
])
def test_graph_rejects_invalid(mutator):
    with pytest.raises(ContractError):
        validate_event_graph(mutator(events()))


def test_logical_clocks_pass_without_wall_clock_authority():
    result = validate_logical_clocks(events())
    assert result["state"] == "PASS_SYNTHETIC_LOGICAL_CLOCKS"
    assert result["wall_clock_authority"] is False


@pytest.mark.parametrize("index,field,value", [(2, "lamport", 2), (2, "source_sequence", 1), (0, "source", "")])
def test_logical_clocks_reject(index, field, value):
    rows = events()
    rows[index][field] = value
    with pytest.raises(ContractError):
        validate_logical_clocks(rows)


def test_merkle_checkpoint_detects_mutation():
    leaves = [{"a": 1}, {"b": 2}]
    root = merkle_root(leaves)
    assert verify_checkpoint(leaves, root)["authenticity_proof"] is False
    with pytest.raises(ContractError):
        verify_checkpoint([{"a": 1}, {"b": 3}], root)


def test_replay_is_deterministic_and_duplicates_quarantined():
    first = replay_events(events())
    second = replay_events(events())
    duplicate = replay_with_duplicates(events() + [events()[-1]])
    assert first["state_digest"] == second["state_digest"] == duplicate["state_digest"]
    assert duplicate["quarantined_duplicates"] == ["c"]


def test_compensation_retains_original():
    original = [{"event_id": "a", "action": "cue"}]
    result = append_compensation(original, "a", "synthetic")
    assert result[0] == original[0]
    assert result[-1]["erases_original"] is False
    assert len(original) == 1


def test_backpressure_keeps_stop_and_exposes_overflow():
    result = bounded_queue([{"cue_id": "r", "priority": "routine"}, {"cue_id": "s", "priority": "stop"}], 1)
    assert result["accepted"][0]["priority"] == "stop"
    assert result["overflow_visible"] is True
    assert result["live_safety_assurance"] is False


def test_schema_migration_roundtrip_preserves_unknown():
    source = {"schema_version": 1, "cue": "x", "priority": "critical", "legacy": 7}
    assert migrate_record(migrate_record(source, 2), 1) == source


@pytest.mark.parametrize("note", [{"severity": "medium", "name": "x"}, {"severity": "unknown"}, {}])
def test_note_minimization_rejects(note):
    with pytest.raises(ContractError):
        minimize_note(note)


def test_validation_credit_refuses_success_replay():
    state = validation_credit_transition("not_run", "invoke")
    state = validation_credit_transition(state, "pass")
    assert state == "successful_once"
    with pytest.raises(ContractError):
        validation_credit_transition(state, "invoke")


def test_outcomes_and_mutations_are_exact():
    outcomes = load("x2/proposals/proposal-outcomes.json")
    mutations = load("x2/proposals/negative-mutation-results.json")
    assert Counter(row["outcome"] for row in outcomes["outcomes"]) == Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    assert mutations["count"] == 100
    assert mutations["all_rejected"] and mutations["all_retained"]
    assert all(row["completion_credit"] == 0 for row in mutations["mutations"])


def test_skills_runners_and_portfolio_are_complete():
    skills = load("x2/skills/skill-catalog.json")
    runners = load("x2/runners/runner-catalog.json")
    results = load("x2/runners/runner-execution-results.json")
    portfolio = load("x2/portfolio/owner-execution.json")
    assert skills["count"] == 10
    assert runners["count"] == 10
    assert results["count"] == 10 and results["all_pass"]
    assert len(portfolio["safe_now"]) == 30 and all(row["state"] == "completed" for row in portfolio["safe_now"])
    assert len(portfolio["candidates"]) == 15 and all(row["state"] == "completed" for row in portfolio["candidates"])
    assert len(portfolio["clean_fix_refine"]) == 30
    assert all(row["state"] == "preserved_unexecuted" for row in portfolio["exact_approval_packets"])
    assert all(row["state"] == "preserved_blocked" for row in portfolio["blocked_packets"])


def test_runner_modules_are_importable_and_bounded():
    for path in sorted((PHASE / "x2" / "runners").glob("ghc_family_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        result = module.run()
        assert result["state"] == "PASS_BOUNDED_SYNTHETIC"
        assert result["external_actions"] == 0
        assert result["stage20"] is False


def test_evidence_manifest_is_exact_on_disk_and_runtime_artifact_free():
    manifest = load("validation/evidence-content-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    assert len({row["path"] for row in manifest["entries"]}) == manifest["entry_count"]
    assert not any("__pycache__" in row["path"] or row["path"].endswith(".pyc") for row in manifest["entries"])
    for row in manifest["entries"]:
        data = subprocess.run(
            ["git", "cat-file", "blob", f"9f1feed93e4b33c8fcb82f0cd818cac8a5594337:{row['path']}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_reports_preserve_accessibility_and_claim_boundaries():
    html = (PHASE / "reports" / "static-report.html").read_text(encoding="utf-8")
    assert '<html lang="en-NZ">' in html
    assert '<main>' in html and '<nav aria-label=' in html
    assert '<caption>' in html and 'scope="col"' in html and 'role="status"' in html
    assert "NOT_READY_FOR_STAGE_20" in html
    assert "complete accessibility conformance" not in html.casefold()


def test_method_flow_counts_are_additive():
    ledger = load("method-flow/method-flow-ledger.json")
    assert ledger["effective"] == {"effective_negatives": 28852, "exact_gates": 202, "failed_witnesses": 1153, "methods": 15438, "open_gaps": 205, "passing_witnesses": 1990}
    assert load("method-flow/x2-operational-method-flow.json")["failure_count"] == 2


def test_non_handoff_documents_remain_bounded():
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt"} and "handoffs" not in path.parts:
            assert len(path.read_text(encoding="utf-8").split()) <= 6000, path
