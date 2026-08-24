from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v668-v1"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def test_final_truth_and_counts():
    truth = load("closeout/phase-truth.json")
    assert truth["source_final"] == "fa6bdcedaac48b0580f4d9581b799741cf5282e7"
    assert truth["x1_head"] == "3e9bf7e7fa9ee1164b77616e09f93127d3b43fd5"
    assert truth["evidence_head"] == "9f1feed93e4b33c8fcb82f0cd818cac8a5594337"
    assert truth["outcomes"] == {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4}
    assert truth["effective"] == {"effective_negatives": 28855, "exact_gates": 202, "failed_witnesses": 1156, "methods": 15441, "open_gaps": 205, "passing_witnesses": 1993}
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_baton_is_bounded_and_hash_locked():
    metadata = load("handoffs/lyren-moss-v668-v2-activation-metadata.json")
    path = ROOT / metadata["path"]
    data = path.read_bytes()
    assert 10_000 <= len(path.read_text(encoding="utf-8").split()) <= 100_000
    assert metadata["words"] == len(path.read_text(encoding="utf-8").split())
    assert hashlib.sha256(data).hexdigest() == metadata["sha256"]
    assert metadata["state"] == "PREPARED_NOT_SENT"
    assert "DELIVERY_STATE: SENT_ONCE_ACKNOWLEDGED" not in path.read_text(encoding="utf-8")


def test_route_is_prepared_not_sent_and_exact():
    route = load("orchestration/route-state-final-candidate.json")
    assert route["sender"] == "Vesper Arlen"
    assert route["recipient"] == "Lyren Moss"
    assert route["recipient_phase"] == "v668-v2"
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["substitute"] is None


def test_closeout_preserves_every_gate_and_failure():
    negatives = load("closeout/retained-negative-register.json")
    gates = load("closeout/exact-open-gate-register.json")
    assert negatives["effective_negatives"] == 28855
    assert negatives["erased_failures"] == 0
    assert negatives["source_manifest_closure_defect_retained"] == 1
    assert gates["open_gaps"] == 205 and gates["exact_gates"] == 202
    assert gates["silently_closed"] == 0


def test_final_manifests_are_exact_on_disk_and_closed():
    for name in ["validation/final-delta-manifest.json", "validation/final-owner-manifest.json"]:
        manifest = load(name)
        assert manifest["entry_count"] == len(manifest["entries"])
        assert len({row["path"] for row in manifest["entries"]}) == manifest["entry_count"]
        assert not any("__pycache__" in row["path"] or row["path"].endswith(".pyc") for row in manifest["entries"])
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            assert len(data) == row["bytes"]
            assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_final_packet_artifacts_exist():
    required = [
        "closeout/final-summary.md", "closeout/phase-truth.json", "closeout/complete-incomplete-checklist.json",
        "closeout/retained-negative-register.json", "closeout/exact-open-gate-register.json", "closeout/wellbeing-check.json",
        "closeout/source-and-provenance-record.json", "reports/integrated-evidence-overview.md", "reports/static-report.html",
        "tooling/ghc-family-index-final.json", "tooling/method-flow-final.json", "tooling/meta-tool-box-final.json",
        "tooling/roster-check-final.json", "tooling/auth-permission-final.json", "seal/content-seal-candidate.json",
        "final/final-validation-prerequisites.json", "method-flow/final-operational-overlay.json", "handoffs/lyren-moss-v668-v2-activation-prepared.md",
    ]
    assert all((PHASE / path).is_file() for path in required)


def test_only_four_core_outcomes_exist():
    outcomes = load("x2/proposals/proposal-outcomes.json")["outcomes"]
    assert Counter(row["outcome"] for row in outcomes) == Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    assert {row["outcome"] for row in outcomes} == {"completed", "represented", "open_gap", "exact_gate"}


def test_non_handoff_documents_remain_under_word_cap():
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt"} and "handoffs" not in path.parts:
            assert len(path.read_text(encoding="utf-8").split()) <= 6000, path
