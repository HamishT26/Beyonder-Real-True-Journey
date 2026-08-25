from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v669-v3"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_exact_outcomes_positive_controls_and_mutations():
    outcomes = load("x2/outcome-ledger.json")
    assert outcomes["counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert set(row["outcome"] for row in outcomes["rows"]) == {"completed", "represented", "open_gap", "exact_gate"}
    positives = load("x2/positive-controls.json")
    assert positives["count"] == 36
    assert all(row["validation"]["passed"] for row in positives["rows"])
    mutations = []
    for path in sorted((ROOT / "x2/mutations").glob("*.json")):
        mutations.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
    assert len(mutations) == 160
    assert all(row["attempted"] and not row["accepted"] and row["completion_credit"] == 0 for row in mutations)


def test_truth_counts_and_nonpromotion():
    truth = load("x2/phase-truth-evidence.json")
    assert truth["effective_negatives"] == 30899
    assert truth["methods"] == 17004
    assert truth["failed_witnesses"] == 2720
    assert truth["passing_witnesses"] == 3832
    assert truth["open_gaps"] == 229
    assert truth["exact_gates"] == 224
    assert truth["real_world_actions"] == 0
    assert truth["network_calls"] == 0
    assert truth["global_installations"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_flashcards_have_four_tiers_and_ten_sections():
    deck = load("x2/flashcard-deck.json")
    assert deck["card_count"] == 40
    cards = list((ROOT / "x2/cards").glob("*.json"))
    assert len(cards) == 40
    for path in cards:
        card = json.loads(path.read_text(encoding="utf-8"))
        assert len(card["tiers"]) == 4
        assert len(card["sections"]) >= 10
        assert card["authoritative"] is False
        assert card["lossy_projection"] is True


def test_portfolios_and_held_packets():
    expected = {"safe_now": 30, "candidate": 15, "skill": 10, "runner": 10, "clean_fix_refine": 30, "exact_approval": 10, "blocked": 5}
    for kind, count in expected.items():
        packet = load(f"x2/portfolio-execution/{kind}.json")
        assert packet["count"] == count
        if kind in {"exact_approval", "blocked"}:
            assert all(row["execution_state"] == "held_unexecuted" for row in packet["rows"])


def test_ten_phase_local_skills_and_runners_smoke_used():
    skill_receipt = load("tools/skill-smoke-receipt.json")
    runner_receipt = load("tools/runner-smoke-receipt.json")
    quick_receipt = load("tools/skill-quick-validation-receipt.json")
    assert skill_receipt["count"] == 10 and skill_receipt["failures"] == 0
    assert runner_receipt["count"] == 10 and runner_receipt["failures"] == 0
    assert all(row["smoke_runner_passed"] and not row["global_installation"] for row in skill_receipt["rows"])
    assert all(row["returncode"] == 0 and row["result"]["passed"] for row in runner_receipt["rows"])
    assert quick_receipt["count"] == 10 and quick_receipt["failures"] == 0
    assert all(row["passed"] and row["utf8_mode"] for row in quick_receipt["rows"])


def test_method_flow_retains_all_new_failures():
    ledger = load("method-flow/evidence-ledger.json")
    assert ledger["new_method_count"] == 172
    assert ledger["new_failed_witnesses"] == 172
    assert ledger["new_bounded_recoveries"] == 172
    assert ledger["new_positive_witnesses"] == 36
    assert len(ledger["rows"]) == 172
    assert all(row["retained"] and row["completion_credit"] == 0 for row in ledger["rows"])


def test_runner_scripts_compile_and_use_family_current_prefix():
    runners = sorted((REPO / "scripts").glob("ghc_family_ceramics_*.py"))
    assert len(runners) == 10
    proc = subprocess.run(["python", "-m", "py_compile", *map(str, runners)], cwd=REPO, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr


def test_evidence_manifests_replay_working_tree_bytes():
    import hashlib

    for rel in ["validation/evidence-owner-manifest.json", "validation/evidence-delta-manifest.json"]:
        manifest = load(rel)
        assert manifest["entry_count"] == len(manifest["entries"])
        for entry in manifest["entries"]:
            data = (REPO / entry["path"]).read_bytes()
            assert len(data) == entry["bytes"]
            assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_bounded_privacy_and_security_receipts():
    privacy = load("validation/evidence-privacy-scan.json")
    security = load("validation/evidence-python-security-review.json")
    assert len(privacy["classes"]) == 5
    assert privacy["candidate_count"] == 0
    assert privacy["confirmed_hits"] == 0
    assert security["finding_count"] == 0
    assert security["files_reviewed"] >= 14
