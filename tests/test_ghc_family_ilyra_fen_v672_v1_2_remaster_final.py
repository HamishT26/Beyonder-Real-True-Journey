from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v672-v1-2-remaster"
X2 = PHASE_ROOT / "x2"
CLOSEOUT = PHASE_ROOT / "closeout"
HANDOFF = PHASE_ROOT / "handoffs" / "auren-lark-v672-v2-activation.md"
SOURCE = "f67221fbee56905a770c64533771dd9471fb2fba"
X1_COMMIT = "da48a47bd21a8e3053094d39691eb72ef1429abd"
EVIDENCE_COMMIT = "1c29b148e90c21aa4ed819281b024256114c50d9"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
    ).stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def test_terminal_candidate_anchors_and_truth() -> None:
    truth = load(CLOSEOUT / "phase-truth.json")
    assert truth["source"] == SOURCE
    assert truth["x1_commit"] == X1_COMMIT
    assert truth["evidence_commit"] == EVIDENCE_COMMIT
    assert truth["planned_final_parent"] == EVIDENCE_COMMIT
    assert truth["proposal_chain"] == 5950
    assert truth["commits_from_source_if_finalized"] == 3
    assert truth["merge_count_if_finalized"] == 0
    assert truth["final_parent_count"] == 1
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["route_state"] == "PREPARED_NOT_SENT"


def test_exact_outcome_labels_and_counts() -> None:
    ledger = load(X2 / "proposals" / "outcome-ledger.json")
    counts = Counter(row["observed_disposition"] for row in ledger["rows"])
    assert set(counts) == ALLOWED_OUTCOMES
    assert counts == Counter(completed=28, represented=8, open_gap=2, exact_gate=2)
    assert load(CLOSEOUT / "phase-truth.json")["outcomes"] == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }


def test_immutable_evidence_manifest_replays_git_blobs() -> None:
    manifest = load(CLOSEOUT / "immutable-evidence-manifest.json")
    assert manifest["evidence_commit"] == EVIDENCE_COMMIT
    assert manifest["entry_count"] == 138
    for row in manifest["entries"]:
        payload = git_bytes("show", f"{EVIDENCE_COMMIT}:{row['path']}")
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["path"]
        assert len(payload) == row["bytes"], row["path"]
        assert git("rev-parse", f"{EVIDENCE_COMMIT}:{row['path']}") == row["git_blob"], row["path"]


def test_evidence_gate_was_four_way_equal() -> None:
    gate = load(CLOSEOUT / "evidence-gate.json")
    assert gate["state"] == "VALID_IMMUTABLE_EVIDENCE_GATE"
    assert gate["evidence_commit"] == EVIDENCE_COMMIT
    assert gate["evidence_parent"] == X1_COMMIT
    assert gate["four_way_equal"] is True
    assert gate["zero_divergence"] is True
    assert len({gate["local"], gate["upstream"], gate["tracking"], gate["fresh_live_remote"]}) == 1


def test_method_flow_closeout_preserves_exact_counts() -> None:
    flow = load(CLOSEOUT / "method-flow-closeout.json")
    sealed = {
        "effective_negatives": 35196,
        "effective_methods": 21827,
        "effective_failed_witnesses": 7017,
        "effective_passing_witnesses": 9118,
        "open_gaps": 276,
        "exact_gates": 270,
    }
    effective = {
        **sealed,
        "effective_negatives": 35197,
        "effective_methods": 21828,
        "effective_failed_witnesses": 7018,
        "effective_passing_witnesses": 9119,
    }
    assert flow["sealed_at_evidence"] == sealed
    assert flow["effective_counts"] == effective
    assert flow["operational_failures"] == 29
    assert flow["invalid_mutations"] == 160
    assert flow["failures_erased"] == 0
    assert flow["recoveries_relabelled_as_original_success"] == 0
    assert len(flow["post_evidence_failures"]) == 1
    assert flow["post_evidence_failures"][0]["method_id"] == "MF-CLOSEOUT-001"
    assert flow["post_evidence_failures"][0]["failure_credit"] == 0


def test_package_and_tool_summary_separates_failed_audit() -> None:
    summary = load(CLOSEOUT / "package-and-tool-summary.json")
    assert summary["direct_packages"] == 13
    assert summary["python_direct"] == 8
    assert summary["python_transitive"] == 2
    assert summary["node_direct"] == 5
    assert summary["local_skills"] == 20
    assert summary["local_runners"] == 10
    assert summary["global_promotions"] == 5
    assert summary["global_composites"] == 1
    assert summary["original_python_audit_success"] is False
    assert summary["dependency_corrected_python_audit_success"] is True
    assert summary["successful_audits_replayed"] is False


def test_handoff_meets_word_and_hash_contract() -> None:
    integrity = load(CLOSEOUT / "handoff-integrity.json")
    payload = HANDOFF.read_bytes()
    words = re.findall(r"\b\w+(?:[-']\w+)*\b", payload.decode("utf-8"))
    assert 10000 <= len(words) <= 100000
    assert len(words) == integrity["words"]
    assert hashlib.sha256(payload).hexdigest() == integrity["sha256"]
    assert integrity["delivery_state"] == "PREPARED_NOT_SENT"
    assert integrity["target_exact_title"] == "Auren Lark"


def test_handoff_delivery_and_next_edge_markers() -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    assert "PREPARED_BY_ILYRA_FEN = true" in text
    assert "SENT_BY_ILYRA_FEN = false" in text
    assert "TARGET_EXACT_TITLE = Auren Lark" in text
    assert "TARGET_PHASE = v672-v2" in text
    assert "Sable Rook for v672-v3" in text
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "relational working language only" in text


def test_route_candidate_is_unsent_and_guarded() -> None:
    route = load(CLOSEOUT / "route-candidate.json")
    assert route["target_exact_title"] == "Auren Lark"
    assert route["target_phase"] == "v672-v2"
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["precontact"] is False
    assert route["send_ceiling"] == 1
    assert len(route["required_guards"]) >= 7
    assert route["next_after_target"].startswith("Sable Rook for v672-v3")


def test_terminal_checklist_keeps_route_work_remaining() -> None:
    checklist = load(CLOSEOUT / "terminal-checklist.json")
    assert all(checklist["checks"].values())
    assert len(checklist["remaining_before_route"]) == 5
    assert "one owner-scoped canonical pass" in checklist["remaining_before_route"][2]


def test_validation_scope_is_owner_scoped() -> None:
    scope = load(CLOSEOUT / "validation-scope.json")
    assert scope["run_after_clean_pushed_final_only"] is True
    assert scope["canonical_success_ceiling"] == 1
    assert scope["replay_after_success"] is False
    assert scope["complete_repository_suite"] is False
    assert scope["independent_reproduction"] is False
    assert len(scope["checks"]) == 10


def test_closeout_manifest_replays_working_bytes() -> None:
    manifest = load(CLOSEOUT / "owner-manifest.json")
    assert manifest["self_excluded"] is True
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]
        assert path.stat().st_size == row["bytes"], row["path"]


def test_all_phase_json_is_strictly_parseable() -> None:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(paths) >= 110
    for path in paths:
        load(path)


def test_document_word_ceilings() -> None:
    for path in sorted(PHASE_ROOT.rglob("*.md")):
        words = re.findall(r"\b\w+(?:[-']\w+)*\b", path.read_text(encoding="utf-8"))
        ceiling = 100000 if path == HANDOFF else 6000
        assert len(words) <= ceiling, (path, len(words))


def test_five_class_privacy_scan_has_no_confirmed_candidate() -> None:
    patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "openai_token": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
        "consumer_email": re.compile(
            r"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
    }
    candidates = []
    for path in sorted(PHASE_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append((path.relative_to(ROOT).as_posix(), label))
    assert candidates == []


def test_bounded_changed_python_ast_scan() -> None:
    paths = [
        path
        for path in (ROOT / "scripts").glob("*v672_v1_2*.py")
        if path.is_file()
    ]
    paths.extend(
        path
        for path in (ROOT / "tests").glob("*v672_v1_2*.py")
        if path.is_file()
    )
    findings = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append((path.name, node.lineno, node.func.id))
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append((path.name, node.lineno, "shell=True"))
    assert findings == []


def test_history_anchors_and_commit_ceiling() -> None:
    assert git("rev-parse", f"{X1_COMMIT}^") == SOURCE
    assert git("rev-parse", f"{EVIDENCE_COMMIT}^") == X1_COMMIT
    assert git("merge-base", "--is-ancestor", EVIDENCE_COMMIT, "HEAD") == ""
    count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    assert 2 <= count <= 3
    merges = git("rev-list", "--merges", f"{SOURCE}..HEAD")
    assert merges == ""


def test_original_canonical_is_never_promoted_or_replayed() -> None:
    truth = load(CLOSEOUT / "phase-truth.json")
    x2_truth = load(X2 / "phase-truth.json")
    assert truth["original_canonical_replayed"] is False
    assert x2_truth["original_canonical_replayed"] is False
    report = (CLOSEOUT / "terminal-report.md").read_text(encoding="utf-8")
    assert "original Python audit failed and remains zero-credit" in report
    assert "original v672-v1 canonical aggregate was not replayed" in report


def test_materialized_lane_remains_below_rotation_guard() -> None:
    assert sum(path.is_file() for path in ROOT.rglob("*")) < 2000
