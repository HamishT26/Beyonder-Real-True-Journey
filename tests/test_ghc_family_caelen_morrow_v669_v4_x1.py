"""Planning-only lifecycle tests for Caelen Morrow v669-v4 x1."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_caelen_morrow_v669_v4_archive import (
    CHAIN_AFTER,
    OWNER_ROOT,
    PROTECTED_GATES,
    SOURCE_FINAL,
    SOURCE_RECOVERED,
    STARTUP_EFFECTIVE_BASELINE,
    STARTUP_FAILURE_COUNT,
    TOOL_CANDIDATES,
    inherited_title_corpus,
    jaccard,
    normalize_title,
    proposal_rows,
)

ROOT = REPO / OWNER_ROOT


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_exact_source_head_and_planning_only_tree() -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()
    assert head == SOURCE_FINAL
    assert not (ROOT / "x2").exists()
    assert not (ROOT / "closeout").exists()
    assert not (ROOT / "seal").exists()


def test_accessible_corpus_and_proposals_are_bounded() -> None:
    corpus, sources = inherited_title_corpus(REPO)
    assert len(corpus) == SOURCE_RECOVERED == 1460
    assert sources
    rows = proposal_rows(corpus)
    assert len(rows) == 40
    assert not any(row["visible_title_collision"] for row in rows)
    assert not any(row["semantic_neighbor_quarantined"] for row in rows)
    assert {row["expected_disposition"] for row in rows} == {
        "completed",
        "represented",
        "open_gap",
        "exact_gate",
    }
    assert all(row["observed_disposition"] is None for row in rows)
    assert all(row["x1_completion_credit"] == 0 for row in rows)
    assert all(row["protected_gates"] == PROTECTED_GATES for row in rows)


@given(st.text(max_size=100))
@settings(max_examples=40, deadline=None)
def test_normalization_is_idempotent(value: str) -> None:
    assert normalize_title(normalize_title(value)) == normalize_title(value)


@given(st.text(max_size=60), st.text(max_size=60))
@settings(max_examples=40, deadline=None)
def test_jaccard_is_symmetric_and_bounded(left: str, right: str) -> None:
    score = jaccard(left, right)
    assert 0.0 <= score <= 1.0
    assert score == pytest.approx(jaccard(right, left))


def test_freeze_counts_and_outcomes() -> None:
    freeze = load("x1/proposal-freeze.json")
    assert freeze["proposal_chain_before"] == 5030
    assert freeze["proposal_chain_after"] == CHAIN_AFTER == 5070
    assert freeze["proposal_count"] == 40
    assert freeze["mutation_count"] == 160
    assert freeze["expected_outcomes"] == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }
    assert freeze["strict_x1_only"] is True


def test_startup_failures_and_recoveries_are_retained() -> None:
    overlay = load("x1/startup-operational-failures.json")
    assert overlay["failure_count"] == STARTUP_FAILURE_COUNT == 24
    assert overlay["bounded_recovery_witness_count"] == 24
    assert overlay["effective_startup_baseline"] == STARTUP_EFFECTIVE_BASELINE
    assert len(overlay["rows"]) == 24
    assert all(row["completion_credit"] == 0 for row in overlay["rows"])
    assert all(row["failed_witness_retained"] for row in overlay["rows"])


def test_tool_candidates_are_planning_only() -> None:
    freeze = load("x1/tool-candidate-freeze.json")
    assert freeze["target_count"] == 3
    assert freeze["installation_state"] == "not_started_x1"
    assert freeze["selected"] == TOOL_CANDIDATES
    assert {row["name"] for row in freeze["selected"]} == {
        "htmlhint",
        "remark-cli",
        "remark-preset-lint-recommended",
    }


def test_route_and_phase_truth_do_not_claim_delivery_or_outcomes() -> None:
    route = load("x1/route-state.json")
    truth = load("x1/phase-truth.json")
    assert route["prospective_successor"] == "Eiren Kestrel"
    assert route["prospective_phase"] == "v669-v5"
    assert route["sent"] is False
    assert route["precontacted"] is False
    assert route["standby_contacted"] is False
    assert truth["lifecycle"] == "x1_planning_only"
    assert truth["observed_outcomes"] is None
    assert truth["tool_installations"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_manifest_matches_current_x1_git_blobs() -> None:
    manifest = load("validation/x1-manifest.json")
    declared = {entry["path"]: entry for entry in manifest["entries"]}
    assert manifest["entry_count"] == len(declared)
    assert manifest["domain"] == "x1_exact_staged_git_blobs_before_commit"
    assert all(not path.startswith("docs/caelen-morrow/v669-v4/x2/") for path in declared)
    for rel, entry in declared.items():
        data = subprocess.run(
            ["git", "show", f":{rel}"], cwd=REPO, check=True, capture_output=True
        ).stdout
        import hashlib

        assert entry["bytes"] == len(data)
        assert entry["sha256"] == hashlib.sha256(data).hexdigest()


def test_x1_has_no_private_absolute_path_or_raw_uuid() -> None:
    windows_user = r"(?i)(?:[A-Z]:" + r"\\Users\\"
    unix_users = r"|/home/|/Users/)"
    private_path = re.compile(windows_user + unix_users)
    raw_uuid = re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")
    hits: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if private_path.search(text) or raw_uuid.search(text):
            hits.append(path.relative_to(REPO).as_posix())
    assert hits == []
