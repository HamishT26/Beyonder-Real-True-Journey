"""Exact Git-tree replacements for phase-local lifecycle tests at the final head."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = "docs/vesper-arlen/v669-v8"
X1_COMMIT = "6cf75a062b9248359599f29ad88ba39ec733f576"
EVIDENCE_COMMIT = "375b43adfcc4e4a911ea26218806af79d70db58f"


def git_lines(*args: str) -> list[str]:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()


def test_x1_git_tree_is_planning_only() -> None:
    paths = git_lines("ls-tree", "-r", "--name-only", X1_COMMIT, OWNER_ROOT)
    forbidden = ("/x2/", "/closeout/", "/seal/", "/final/", "/handoffs/")
    assert paths
    assert not [path for path in paths if any(token in path for token in forbidden)]


def test_evidence_git_tree_has_no_closeout_and_preserves_x1() -> None:
    paths = git_lines("ls-tree", "-r", "--name-only", EVIDENCE_COMMIT, OWNER_ROOT)
    forbidden = ("/closeout/", "/seal/", "/final/", "/handoffs/")
    x1_delta = git_lines("diff", "--name-only", X1_COMMIT, EVIDENCE_COMMIT, "--", f"{OWNER_ROOT}/x1")
    assert paths
    assert not [path for path in paths if any(token in path for token in forbidden)]
    assert not x1_delta
