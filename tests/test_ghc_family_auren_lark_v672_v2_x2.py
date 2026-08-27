from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "auren-lark" / "v672-v2"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
VALIDATION = PHASE / "validation"
X1_HEAD = "821a40be02af8db39524dc862aeaadf32e1543c3"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_x1_is_immutable_and_x2_gate_is_exact() -> None:
    changed = subprocess.check_output(
        ["git", "-C", str(ROOT), "diff", "--name-only", X1_HEAD], text=True
    ).splitlines()
    frozen_exact = {
        "scripts/build_ghc_family_auren_lark_v672_v2_x1.py",
        "scripts/build_ghc_family_auren_lark_v672_v2_staged_review.py",
        "tests/test_ghc_family_auren_lark_v672_v2_x1.py",
    }
    assert not [
        path
        for path in changed
        if path.startswith("docs/auren-lark/v672-v2/x1/") or path in frozen_exact
    ]
    gate = load(X2 / "lifecycle" / "x1-gate.json")
    assert gate["state"] == "VALID_STRICT_X1_GATE"
    assert gate["x1_commit"] == X1_HEAD
    assert gate["x1_parent"] == "40db1e418c1251e12d77f832c0890869b990dba5"
    assert gate["four_way_equal"] is True
    assert gate["zero_divergence"] is True


def test_outcomes_have_only_four_labels_and_exact_counts() -> None:
    ledger = load(X2 / "proposals" / "outcome-ledger.json")
    rows = ledger["rows"]
    assert len(rows) == 40
    outcomes = Counter(row["outcome"] for row in rows)
    assert set(outcomes) == ALLOWED
    assert outcomes == Counter(
        {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    )
    assert ledger["inherited_completion_credit"] == 0


def test_skill_and_runner_portfolios_are_exact() -> None:
    skill_registry = load(X2 / "tools" / "skill-registry.json")
    runner_registry = load(X2 / "tools" / "runner-registry.json")
    assert skill_registry["skill_count"] == 20
    assert runner_registry["runner_count"] == 10
    assert len({row["name"] for row in skill_registry["skills"]}) == 20
    assert len({row["surface"] for row in runner_registry["runners"]}) == 10
    for row in skill_registry["skills"]:
        path = X2 / "tools" / "skills" / row["name"] / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\nname: ")
        assert "NOT_READY_FOR_STAGE_20" in text
        assert "same-owner software evidence only" in text
    for row in runner_registry["runners"]:
        assert (ROOT / row["path"]).is_file()


def test_fixture_ledger_has_ten_accepting_and_fifty_rejecting() -> None:
    ledger = load(X2 / "fixtures" / "fixture-ledger.json")
    assert ledger["real_records"] == 0
    assert ledger["accepting"] == 10
    assert ledger["rejecting"] == 50
    assert len(ledger["rows"]) == 60
    assert Counter(row["expected"] for row in ledger["rows"]) == Counter(
        {"accept": 10, "reject": 50}
    )
    for row in ledger["rows"]:
        fixture = load(ROOT / row["path"])
        assert fixture["surface"] == row["surface"]
        assert fixture["expected"] == row["expected"]


def test_runner_smoke_succeeded_once_without_broader_claim() -> None:
    receipt = load(X2 / "validation" / "runner-smoke-receipt.json")
    assert receipt["state"] == "VALID_X2_OWNER_SCOPED_RUNNER_SMOKE"
    assert receipt["invocations"] == 1
    assert receipt["successful_invocations"] == 1
    assert receipt["runner_count"] == 10
    assert receipt["checks"] == 60
    assert receipt["accepting_passed"] == receipt["accepting_total"] == 10
    assert receipt["rejecting_refused"] == receipt["rejecting_total"] == 50
    assert receipt["mismatch_count"] == 0
    assert receipt["complete_repository_suite"] is False
    assert receipt["independent_reproduction"] is False
    equivalence = load(X2 / "validation" / "post-smoke-ruff-ast-equivalence.json")
    assert equivalence["state"] == "VALID_ISOLATED_POST_SMOKE_AST_EQUIVALENCE"
    assert equivalence["runner_count"] == equivalence["ast_equal_count"] == 10
    assert all(row["ast_equal"] for row in equivalence["rows"])
    assert equivalence["runner_smoke_replayed"] is False
    assert equivalence["broader_credit"] == 0


def test_method_flow_and_effective_counts_preserve_failures() -> None:
    flow = load(X2 / "method-flow" / "ledger.json")
    truth = load(X2 / "phase-truth.json")
    assert flow["x1_startup_failures_retained"] == 12
    assert len(flow["x2_operational_failures"]) == 3
    assert len(flow["expected_rejections"]) == 50
    assert flow["failures_erased"] == 0
    assert flow["recoveries_relabelled_as_original_success"] == 0
    expected = {
        "effective_negatives": 35266,
        "effective_methods": 21897,
        "effective_failed_witnesses": 7087,
        "effective_passing_witnesses": 9184,
        "open_gaps": 279,
        "exact_gates": 272,
    }
    assert flow["effective_counts"] == expected
    assert truth["effective_counts"] == expected
    assert truth["state"] == "X2_EVIDENCE_BUILT_NOT_YET_IMMUTABLE"
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_owner_manifest_matches_working_tree_exact_bytes() -> None:
    manifest = load(X2 / "owner-manifest.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        data = (ROOT / row["path"]).read_bytes()
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_x2_text_has_no_confirmed_five_class_privacy_hit() -> None:
    patterns = [
        re.compile(rb"A" + rb"KIA[0-9A-Z]{16}"),
        re.compile(rb"gh" + rb"p_[A-Za-z0-9]{20,}"),
        re.compile(rb"BEGIN [A-Z ]*PRIVATE" + rb" KEY"),
        re.compile(rb"\b019[a-f0-9]{5}-[a-f0-9-]{20,}\b"),
        re.compile(rb"(?i)(password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    ]
    candidates = []
    for path in X2.rglob("*"):
        if not path.is_file():
            continue
        data = path.read_bytes()
        for pattern in patterns:
            if pattern.search(data):
                candidates.append(path)
    assert candidates == []


def test_route_is_not_sent_and_evidence_review_is_valid_when_present() -> None:
    route = load(X2 / "route" / "sable-candidate.json")
    assert route["state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
    assert route["precontacted"] is False
    assert route["send_count"] == 0
    review_path = VALIDATION / "evidence-staged-review.json"
    if review_path.exists():
        review = load(review_path)
        assert review["valid"] is True
        assert review["deletions"] == []
        assert review["out_of_scope"] == []
        assert review["frozen_x1_mutations"] == []
        assert review["confirmed_privacy_candidates"] == []
        assert review["bounded_changed_python_security_findings"] == []
        assert review["owner_manifest_mismatches"] == []


def test_overview_is_substantive_and_boundary_complete() -> None:
    overview = (X2 / "integrated-overview.md").read_text(encoding="utf-8")
    assert len(re.findall(r"\S+", overview)) >= 700
    assert "NOT_READY_FOR_STAGE_20" in overview
    assert "wholly synthetic" in overview
    assert "Māori authority" in overview
