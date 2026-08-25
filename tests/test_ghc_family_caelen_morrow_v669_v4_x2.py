"""Owner-scoped tests for Caelen Morrow v669-v4 x2 evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/caelen-morrow/v669-v4"
X1_COMMIT = "964e7a27dd73ee7d96d8b9f6136ed4bf72e1f3f7"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_exact_x1_head_and_frozen_paths() -> None:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True).stdout.strip()
    assert head == X1_COMMIT
    names = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    assert not any(path.startswith("docs/caelen-morrow/v669-v4/x1/") for path in names)
    assert "scripts/build_ghc_family_caelen_morrow_v669_v4_x1.py" not in names
    assert "scripts/ghc_family_caelen_morrow_v669_v4_archive.py" not in names


def test_exact_outcomes_positive_controls_and_mutations() -> None:
    outcomes = load("x2/outcome-ledger.json")
    assert outcomes["counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert {row["outcome"] for row in outcomes["rows"]} == {"completed", "represented", "open_gap", "exact_gate"}
    positives = load("x2/positive-controls.json")
    assert positives["count"] == 36
    assert all(row["validation"]["passed"] for row in positives["rows"])
    mutations = []
    for path in sorted((ROOT / "x2/mutations").glob("*.json")):
        mutations.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
    assert len(mutations) == 160
    assert all(row["attempted"] and not row["accepted"] and row["completion_credit"] == 0 for row in mutations)


def test_truth_counts_and_nonpromotion() -> None:
    truth = load("x2/phase-truth-evidence.json")
    assert truth["effective_negatives"] == 31088
    assert truth["methods"] == 17193
    assert truth["failed_witnesses"] == 2909
    assert truth["passing_witnesses"] == 4057
    assert truth["open_gaps"] == 231
    assert truth["exact_gates"] == 226
    assert truth["real_world_actions"] == 0
    assert truth["network_calls_by_phase_adapter"] == 0
    assert truth["shared_prefix_mutations"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_flashcards_have_four_tiers_and_ten_sections() -> None:
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


def test_portfolios_and_held_packets() -> None:
    expected = {"safe_now": 30, "candidate": 15, "skill": 10, "runner": 10, "clean_fix_refine": 30, "exact_approval": 10, "blocked": 5}
    for kind, count in expected.items():
        packet = load(f"x2/portfolio-execution/{kind}.json")
        assert packet["count"] == count
        if kind in {"exact_approval", "blocked"}:
            assert all(row["execution_state"] == "held_unexecuted" for row in packet["rows"])


def test_skills_runners_and_core_skill_uses() -> None:
    skill = load("tools/skill-smoke-receipt.json")
    runner = load("tools/runner-smoke-receipt.json")
    quick = load("tools/skill-quick-validation-receipt.json")
    core = load("tools/core-skill-use-ledger.json")
    assert skill["count"] == runner["count"] == quick["count"] == 10
    assert skill["failures"] == runner["failures"] == quick["failures"] == 0
    assert all(row["smoke_runner_passed"] and not row["global_installation"] for row in skill["rows"])
    assert all(row["returncode"] == 0 and row["result"]["passed"] for row in runner["rows"])
    assert all(row["passed"] and row["utf8_mode"] for row in quick["rows"])
    assert core["required_and_used"] >= 23
    assert all(row["status"] == "read_through_eof_and_applied" for row in core["rows"])


def test_installed_suite_and_target_three_receipts() -> None:
    suite = load("tools/installed-suite-use-receipt.json")
    tools = load("tools/isolated-toolchain-install-receipt.json")
    assert suite["count"] == 26
    assert suite["version_compatibility_failures"] == []
    assert len(tools["selected"]) == 3
    assert all(row["version_matches"] and row["integrity_matches"] for row in tools["selected"])
    assert tools["install_scripts_disabled"] is True
    assert tools["shared_npm_prefix_mutated"] is False
    assert tools["audit"]["returncode"] == 0
    assert tools["audit"]["vulnerabilities"]["total"] == 0
    assert tools["smoke"]["positive_passed"] is True
    assert tools["smoke"]["rejecting_passed"] is True
    assert tools["retained_warnings"] == ["transitive_glob_10_5_0_deprecation_warning"]


def test_method_flow_retains_x2_failures_and_mutations() -> None:
    ledger = load("method-flow/evidence-ledger.json")
    assert ledger["new_operational_failures"] == 4
    assert ledger["new_rejecting_mutations"] == 160
    assert ledger["new_method_count"] == 164
    assert ledger["new_failed_witnesses"] == 164
    assert ledger["new_bounded_recoveries"] == 164
    assert ledger["new_positive_witnesses"] == 36
    assert len(ledger["rows"]) == 164
    assert all(row["retained"] and row["completion_credit"] == 0 for row in ledger["rows"])


def test_runners_compile_without_cache_write() -> None:
    runners = sorted((REPO / "scripts").glob("ghc_family_audio_*.py"))
    assert len(runners) == 10
    for path in runners:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")


def test_evidence_manifests_replay_exact_git_blobs() -> None:
    for rel in ["validation/evidence-owner-manifest.json", "validation/evidence-delta-manifest.json"]:
        manifest = load(rel)
        assert manifest["entry_count"] == len(manifest["entries"])
        for entry in manifest["entries"]:
            staged = subprocess.run(["git", "diff", "--cached", "--name-only", "--", entry["path"]], cwd=REPO, check=True, capture_output=True, text=True).stdout.strip()
            spec = f":{entry['path']}" if staged else f"HEAD:{entry['path']}"
            data = subprocess.run(["git", "show", spec], cwd=REPO, check=True, capture_output=True).stdout
            assert len(data) == entry["bytes"]
            assert hashlib.sha256(data).hexdigest() == entry["sha256"]


def test_bounded_privacy_security_and_accessibility_receipts() -> None:
    privacy = load("validation/evidence-privacy-scan.json")
    security = load("validation/evidence-python-security-review.json")
    report = (ROOT / "x2/accessible-evidence-report.html").read_text(encoding="utf-8")
    assert len(privacy["classes"]) == 5
    assert privacy["candidate_count"] == privacy["confirmed_hits"] == 0
    assert security["finding_count"] == 0
    assert security["files_reviewed"] >= 13
    for marker in ["<main", "<nav", "<table", "<caption>", "scope=\"col\"", "focus-visible", "@media print"]:
        assert marker in report
