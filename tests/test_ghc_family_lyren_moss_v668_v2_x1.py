#!/usr/bin/env python3
"""Planning-only x1 contract tests for Lyren Moss v668-v2."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_lyren_moss_v668_v2_archive import (  # noqa: E402
    ALLOWED_OUTCOMES,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE_ROOT,
    PROTECTED_GATES,
    SOURCE_FINAL,
    SOURCE_REPOSITORY_SEAL,
    sha256_bytes,
)


def read_json(relative: str) -> dict:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], check=True, capture_output=True
    ).stdout


def immutable_x1_head() -> str | None:
    head = git("rev-parse", "HEAD")
    if head == SOURCE_FINAL:
        return None
    commits = git("rev-list", "--reverse", "--ancestry-path", f"{SOURCE_FINAL}..{head}").splitlines()
    return commits[0] if commits else None


def test_exact_owner_and_phase() -> None:
    truth = read_json("x1/phase-truth.json")
    assert truth["owner"] == OWNER == "Lyren Moss"
    assert truth["phase"] == "v668-v2"
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_source_anchor_exists_and_is_ancestor_or_current() -> None:
    assert git("rev-parse", f"{SOURCE_FINAL}^{{commit}}") == SOURCE_FINAL
    head = git("rev-parse", "HEAD")
    if head != SOURCE_FINAL:
        subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", SOURCE_FINAL, head], check=True
        )


def test_source_seal_is_not_rewritten_by_overlay() -> None:
    intake = read_json("x1/source-intake.json")
    assert intake["source_repository_seal"] == SOURCE_REPOSITORY_SEAL
    overlay = intake["planning_overlay_after_retained_startup_failure"]
    assert overlay["effective_negatives"] == 29049
    assert overlay["methods"] == 15635
    assert overlay["failed_witnesses"] == 1350
    assert overlay["passing_witnesses"] == 2185


def test_visible_chain_audit_preserves_compressed_title_gap() -> None:
    audit = read_json("x1/proposal-chain-audit.json")
    assert audit["declared_inherited_chain_count"] == INHERITED_FROZEN_PROPOSALS == 4630
    assert audit["selected_count"] == 20
    assert audit["selected_novelty_credit"] == 0
    assert audit["selected_completion_credit"] == 0
    assert audit["freeze_blob_count"] > 0
    assert audit["unique_id_count"] >= 20
    assert audit["coverage_state"].endswith("OPEN_GAP")


def test_forty_distinct_proposals_and_exact_outcomes() -> None:
    freeze = read_json("x1/proposal-freeze.json")
    rows = freeze["new_proposals"]
    assert len(rows) == 40
    assert len({row["proposal_id"] for row in rows}) == 40
    assert len({row["normalized_title"] for row in rows}) == 40
    assert sum(row["visible_title_collision"] for row in rows) == 0
    assert Counter(row["expected_disposition"] for row in rows) == Counter(
        {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    )
    assert freeze["new_frozen_total"] == 4670


def test_mutations_are_preregistered_and_unexecuted() -> None:
    rows = read_json("x1/proposal-freeze.json")["new_proposals"]
    mutations = [mutation for row in rows for mutation in row["negative_fixtures"]]
    assert len(mutations) == 160
    assert all(mutation["state"] == "preregistered_not_executed" for mutation in mutations)
    assert all(mutation["credit"] == 0 for mutation in mutations)


def test_four_outcomes_only() -> None:
    truth = read_json("x1/phase-truth.json")
    assert tuple(truth["allowed_outcomes"]) == ALLOWED_OUTCOMES
    assert set(truth["expected_outcomes"]) == set(ALLOWED_OUTCOMES)
    assert truth["observed_outcomes"] is False


def test_pillar_and_practices_are_bounded() -> None:
    practice = read_json("x1/practice-and-pillar-freeze.json")
    assert practice["primary_pillar"] == "THOS Body"
    assert len(practice["practices"]) == 3
    assert practice["synthetic_only"] is True
    assert practice["real_people"] == 0
    assert practice["professional_or_operational_authority"] is False


def test_source_ledger_is_primary_or_official_and_bounded() -> None:
    ledger = read_json("x1/source-ledger.json")
    assert ledger["source_count"] == 7
    assert ledger["primary_or_official_only"] is True
    assert ledger["professional_selection_or_conformance_claim"] is False
    assert any("Candidate Recommendation" in row["authority"] for row in ledger["sources"])


def test_portfolio_counts_and_unexecuted_exact_packets() -> None:
    portfolio = read_json("x1/portfolio-freeze.json")
    assert portfolio["counts"] == {
        "owner_safe_now": 60,
        "owner_candidates": 30,
        "owner_skills": 20,
        "owner_runners": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine": 30,
        "exact_approval_packets": 20,
        "blocked_packets": 10,
    }
    assert all(row["completion_credit"] == 0 for row in portfolio["exact_approval_packets"])
    assert all(row["x2_execution_count"] == 0 for row in portfolio["blocked_packets"])


def test_route_is_prepared_not_contacted() -> None:
    route = read_json("x1/route-auth-roster-freeze.json")
    assert route["current_seat"] == {"owner": "Lyren Moss", "phase": "v668-v2"}
    assert route["prospective_next"] == {"exact_title": "Ilyra Fen", "phase": "v668-v3", "contacted": False}
    assert route["single_send_maximum"] == 1
    assert route["standby_not_substitute"] == ["Tavian Sol"]


def test_retained_failures_are_not_erased() -> None:
    method = read_json("method-flow/startup-and-x1.json")
    assert len(method["lyren_failures"]) == 5
    assert all(row["retained"] for row in method["lyren_failures"])
    assert all(row["failure_credit"] == 0 for row in method["lyren_failures"])
    assert method["correction_erases_failure"] is False


def test_immutable_x1_tree_has_no_x2_or_controls() -> None:
    x1_head = immutable_x1_head()
    if x1_head is None:
        assert not (PHASE_ROOT / "x2").exists()
        assert not (ROOT / "scripts/ghc_family_lyren_moss_v668_v2_controls.py").exists()
        return
    paths = set(git("ls-tree", "-r", "--name-only", x1_head).splitlines())
    assert not any(path.startswith(f"{PHASE_ROOT.relative_to(ROOT).as_posix()}/x2/") for path in paths)
    assert "scripts/ghc_family_lyren_moss_v668_v2_controls.py" not in paths
    assert git("rev-parse", f"{x1_head}^") == SOURCE_FINAL


def test_x1_manifest_replays_in_correct_domain() -> None:
    manifest = read_json("x1/manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    assert manifest["x2_entries"] == []
    x1_head = immutable_x1_head()
    for row in manifest["entries"]:
        data = (ROOT / row["path"]).read_bytes() if x1_head is None else git_bytes("show", f"{x1_head}:{row['path']}")
        assert len(data) == row["bytes"]
        assert sha256_bytes(data) == row["sha256"]


def test_overview_retains_protected_boundaries() -> None:
    overview = (PHASE_ROOT / "x1/integrated-overview.md").read_text(encoding="utf-8")
    for phrase in ("not evidence of consciousness", "same-owner local software validation", "NOT_READY_FOR_STAGE_20", "x1 tree contains only declarations"):
        assert phrase.casefold() in overview.casefold()
    for gate in PROTECTED_GATES:
        assert gate in overview
