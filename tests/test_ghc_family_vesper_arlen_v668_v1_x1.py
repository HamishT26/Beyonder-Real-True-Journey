from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v668-v1"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def test_x1_is_planning_only() -> None:
    charter = load("x1/phase-charter.json")
    receipt = load("x1/x1-build-receipt.json")
    assert charter["x1_planning_only"] is True
    assert charter["x2_outcomes_observed"] is False
    assert receipt["x2_files_created"] == 0
    assert receipt["outcomes_observed"] is False
    frozen_paths = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "3e9bf7e7fa9ee1164b77616e09f93127d3b43fd5"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert not any(path.startswith("docs/vesper-arlen/v668-v1/x2/") for path in frozen_paths)


def test_source_and_external_overlay_are_exact() -> None:
    source = load("x1/source-intake.json")
    assert source["source_anchors"]["exact_corrected_final"] == "fa6bdcedaac48b0580f4d9581b799741cf5282e7"
    assert source["source_canonical"]["success_credit"] == 0
    assert source["source_recovery"]["not_canonical_success"] is True
    assert source["successor_visible_external_overlay"]["effective_negatives"] == 28736
    assert source["manifest_intake"]["incomplete_git_blob_replays"]["corrected_owner"] == [83, 86]
    assert len(source["manifest_intake"]["absent_ignored_artifacts"]) == 3


def test_proposal_freeze_counts_and_labels() -> None:
    frozen = load("x1/proposal-freeze.json")
    proposals = frozen["new_proposals"]
    assert len(proposals) == 20
    assert frozen["inherited_frozen_proposals"] == 4570
    assert frozen["new_frozen_total"] == 4590
    assert frozen["negative_mutation_count"] == 100
    assert Counter(row["expected_disposition"] for row in proposals) == Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    assert {row["expected_disposition"] for row in proposals} == ALLOWED
    assert len({row["title"].casefold() for row in proposals}) == 20
    assert all(row["x1_planning_only"] and row["completion_credit"] == 0 for row in proposals)
    assert all(len(row["negative_fixtures"]) == 5 for row in proposals)


def test_portfolio_floors_and_gates() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    assert len(portfolio["owner_safe_now"]) == 30
    assert len(portfolio["owner_candidates"]) == 15
    assert len(portfolio["owner_skills"]) == 10
    assert len(portfolio["owner_runners"]) == 10
    assert len(portfolio["owner_clean_fix_refine"]) == 30
    assert len(portfolio["exact_approval_packets"]) == 10
    assert len(portfolio["blocked_packets"]) == 5
    assert all(row["state"] == "preserved_unexecuted" for row in portfolio["exact_approval_packets"])
    assert all(row["state"] == "preserved_blocked" for row in portfolio["blocked_packets"])


def test_method_flow_retains_every_startup_failure() -> None:
    method = load("method-flow/startup-method-flow.json")
    assert method["startup_failure_count"] == 14
    assert len(method["startup_failures"]) == 14
    assert len({row["failure_id"] for row in method["startup_failures"]}) == 14
    assert all(row["failure_retained"] and row["credit"] == 0 for row in method["startup_failures"])
    assert method["post_startup_overlay"]["effective_negatives"] == 28750
    assert method["post_startup_overlay"]["open_gaps"] == 204


def test_manifest_is_owner_scoped_and_exact_on_disk() -> None:
    manifest = load("validation/x1-content-manifest.json")
    paths = [row["path"] for row in manifest["entries"]]
    assert len(paths) == len(set(paths)) == manifest["entry_count"]
    assert manifest["ignored_runtime_artifacts_excluded"] is True
    assert not any("__pycache__" in path or path.endswith(".pyc") for path in paths)
    assert all(path.startswith("docs/vesper-arlen/v668-v1/") or "vesper_arlen_v668_v1" in path for path in paths)
    for row in manifest["entries"]:
        data = subprocess.run(
            ["git", "cat-file", "blob", f"3e9bf7e7fa9ee1164b77616e09f93127d3b43fd5:{row['path']}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_identity_authority_and_route_are_bounded() -> None:
    identity = load("identity/relational-identity.json")
    boundary = load("x1/authorization-boundary.json")
    route = load("orchestration/roster-auth-x1.json")
    assert identity["relational_working_language_only"] is True
    assert "consciousness" in identity["not_evidence_of"]
    assert "Stage 20" in boundary["exact_gated"]
    assert route["current_owner"] == "Vesper Arlen"
    assert route["prospective_next_owner"] == "Lyren Moss"
    assert route["delivery_state"] == "NOT_ELIGIBLE_X1"
    assert len(route["roster"]) == 15


def test_documents_remain_bounded() -> None:
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt"} and "handoffs" not in path.parts:
            words = len(path.read_text(encoding="utf-8").split())
            assert words <= 6000, (path, words)
