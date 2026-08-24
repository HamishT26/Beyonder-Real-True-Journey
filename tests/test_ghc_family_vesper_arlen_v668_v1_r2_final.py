from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v668-v1-r2"
SOURCE = "d3fd3065a4570046335689c62af8faf636be7a86"
X1 = "be908eb829185971c10be6d100c2c85fd35871e0"
EVIDENCE = "813b4bd702c85476cc87791790d1e1cd27e4b5ff"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def test_closeout_anchors_and_expected_history_are_exact():
    record = load("final/final-record.json")
    assert record["source_final"] == SOURCE
    assert record["x1_head"] == X1
    assert record["evidence_head"] == EVIDENCE
    assert subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{EVIDENCE}^"], check=True, capture_output=True, text=True).stdout.strip() == X1
    assert subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{X1}^"], check=True, capture_output=True, text=True).stdout.strip() == SOURCE


def test_baton_is_sanitized_and_within_required_word_range():
    summary = load("handoffs/activation-summary.json")
    path = ROOT / summary["baton_path"]
    text = path.read_text(encoding="utf-8")
    assert 10_000 <= len(text.split()) <= 100_000
    assert summary["baton_words"] == len(text.split())
    assert summary["baton_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    forbidden = [
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        r"\b[A-Za-z]:[\\/](?!/)",
        r"(?i)\bsource_thread_id\b",
        r"(?i)\bcodex_delegation\b",
        r"(?i)\bprivate_callable_identifier\b",
    ]
    assert all(re.search(pattern, text) is None for pattern in forbidden)


def test_baton_reminds_lyren_of_ilyra_and_never_claims_delivery_early():
    summary = load("handoffs/activation-summary.json")
    route = load("closeout/route-and-roster-record.json")
    assert summary["recipient"] == "Lyren Moss" and summary["phase"] == "v668-v2"
    assert summary["next_after_lyren"] == {"recipient": "Ilyra Fen", "phase": "v668-v3"}
    assert summary["sent"] is False and route["successor_contacted"] is False
    assert route["cycle_count"] == 15 and "Sylven Arc" in route["cycle"]


def test_closeout_counts_preserve_all_negatives_gaps_and_gates():
    negatives = load("closeout/retained-negative-register.json")
    gaps = load("closeout/open-gap-register.json")
    gates = load("closeout/exact-gate-register.json")
    assert negatives["effective_negatives_before_canonical"] == 29042
    assert negatives["all_retained"] and negatives["original_tool_audit_rewritten"] is False
    assert gaps["effective_open_gaps"] == 209 and gaps["closed_without_evidence"] == 0
    assert gates["effective_exact_gates"] == 204 and gates["closed_without_authority"] == 0


def test_content_seal_matches_manifests_and_baton():
    seal = load("seal/content-seal.json")
    owner = PHASE / "validation" / "final-owner-manifest.json"
    delta = PHASE / "validation" / "final-delta-manifest.json"
    baton = PHASE / "handoffs" / "lyren-moss-v668-v2-activation.md"
    assert seal["owner_manifest_sha256"] == hashlib.sha256(owner.read_bytes()).hexdigest()
    assert seal["delta_manifest_sha256"] == hashlib.sha256(delta.read_bytes()).hexdigest()
    assert seal["baton_sha256"] == hashlib.sha256(baton.read_bytes()).hexdigest()
    assert seal["canonical_validation_invoked"] is False and seal["successor_contacted"] is False


def test_outcomes_use_only_four_labels_and_exact_distribution():
    outcomes = load("x2/proposals/proposal-outcomes.json")
    assert outcomes["outcome_counts"] == {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8}
    assert set(outcomes["outcome_counts"]) == {"completed", "represented", "open_gap", "exact_gate"}


def test_final_remains_not_ready_and_canonical_pending():
    record = load("final/final-record.json")
    assert record["state"] == "CONTENT_SEALED_CANONICAL_PENDING"
    assert record["canonical_invocation_count"] == 0
    assert record["canonical_success_credit"] == 0
    assert record["post_success_replay"] is False
    assert record["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
