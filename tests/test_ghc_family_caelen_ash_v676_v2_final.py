from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "caelen-ash" / "v676-v2"
FINAL = BASE / "final"
EVIDENCE = "bc7f321d66c094422ddc69275d811eb8ec917f3b"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def normalized_sha(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def test_final_candidate_is_built_only_from_immutable_evidence() -> None:
    assert git("branch", "--show-current") == BRANCH
    head = git("rev-parse", "HEAD")
    if head == EVIDENCE:
        assert git("status", "--porcelain=v1")
    else:
        assert git("rev-parse", "HEAD^") == EVIDENCE


def test_final_truth_preserves_exact_anchors_chain_and_outcomes() -> None:
    data = load(FINAL / "phase-truth.json")
    assert data["source"] == "939312172819669aad250cf034d8a6a7efe3df5b"
    assert data["x1"] == "39daa2da64125b839714efa8b7488d8ed9ed364b"
    assert data["evidence"] == EVIDENCE
    assert data["proposal_chain"] == 7470
    assert data["core_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert data["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_method_flow_preserves_exact_phase_arithmetic() -> None:
    data = load(FINAL / "method-flow-ledger.json")
    assert data["phase_ledger_counts"] == {"methods": 449, "failed": 181, "passing": 268}
    assert len(data["methods"]) == 449
    assert data["current_overlay"] == {
        "effective_negatives": 41843,
        "effective_methods": 31203,
        "retained_failed_witnesses": 13504,
        "bounded_passing_witnesses": 18388,
        "open_gaps": 351,
        "exact_gates": 343,
    }
    ids = {row["method_id"] for row in data["methods"]}
    for row in data["methods"]:
        if row["truth"] is False:
            assert row["recovered_by"] in ids


def test_retained_negative_register_contains_every_phase_false_witness() -> None:
    data = load(FINAL / "retained-negative-register.json")
    assert data["activation_effective_negatives"] == 41662
    assert data["new_caelen_effective_negatives"] == 181
    assert data["current_effective_negatives"] == 41843
    assert data["phase_failed_witness_count"] == 181
    assert len(data["phase_failed_witnesses"]) == 181
    assert data["failed_witnesses_converted_to_pass"] == 0
    assert all(row["truth"] is False for row in data["phase_failed_witnesses"])


def test_source_and_proposal_ledger_has_forty_new_rows_and_four_labels_only() -> None:
    data = load(FINAL / "source-and-proposal-ledger.json")
    assert data["declared_chain_before"] == 7430
    assert data["declared_chain_after"] == 7470
    assert len(data["proposals"]) == 40
    assert len(data["outcomes"]) == 40
    assert set(row["outcome"] for row in data["outcomes"]) == LABELS
    assert len(data["official_primary_sources"]) == 7
    assert data["reachable_novelty_audit"]["universal_novelty_proof_claimed"] is False


def test_content_seal_replays_every_named_normalized_lf_hash() -> None:
    data = load(BASE / "closeout" / "content-seal.json")
    assert len(data["entries"]) == 8
    for row in data["entries"]:
        assert normalized_sha(REPO / row["path"]) == row["sha256_normalized_lf"]
    assert data["final_commit_self_hash_excluded"] is True
    assert data["canonical_receipt_external"] is True


def test_complete_incomplete_ledger_keeps_open_and_exact_gated_work_visible() -> None:
    data = load(FINAL / "complete-incomplete-ledger.json")
    assert len(data["complete_bounded"]) >= 7
    assert len(data["represented_only"]) >= 2
    assert len(data["open"]) == 2
    assert len(data["exact_gated"]) == 2
    assert data["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_portfolio_truth_does_not_execute_exact_or_blocked_packets() -> None:
    data = load(FINAL / "portfolio-truth.json")
    assert data["safe_now_completed"] == 60
    assert data["candidate_completed_bounded"] == 30
    assert data["exact_approval_unexecuted"] == 20
    assert data["blocked_unexecuted"] == 10
    assert data["owner_clean_fix_refine_completed"] == 60
    assert data["successor_clean_fix_refine_recommendations_zero_credit"] == 30
    assert data["core_outcome_counts_unchanged_by_portfolio_status"] is True


def test_post_evidence_failure_and_recovery_remain_separate() -> None:
    data = load(FINAL / "post-evidence-overlay.json")
    assert data["failed_witness"]["truth"] is False
    assert data["bounded_recovery"]["truth"] is True
    assert data["bounded_recovery"]["failed_witness_preserved"] == data["failed_witness"]["method_id"]
    assert data["repository_seal_rewritten"] is False
    assert data["evidence_commit_mutated"] is False


def test_final_truth_has_zero_real_rows_participants_and_authority_actions() -> None:
    data = load(FINAL / "phase-truth.json")
    assert data["real_world_rows"] == 0
    assert data["participants"] == 0
    assert data["real_carriers_or_recordings"] == 0
    assert data["production_identity_events"] == 0
    assert data["authority_actions"] == 0
    assert data["full_repository_suite_run"] is False
    assert data["independent_reproduction_claimed"] is False


def test_static_final_report_is_text_first_and_reserves_manual_evaluation() -> None:
    value = (FINAL / "accessible-report.html").read_text(encoding="utf-8")
    assert "<caption>Core outcomes</caption>" in value
    assert "NOT_READY_FOR_STAGE_20" in value
    assert "Manual keyboard, screen-reader" in value
    assert "<script" not in value.lower()


def test_route_remains_prepared_not_sent_and_target_neutral() -> None:
    hold = load(BASE / "handoffs" / "terminal-route-hold.json")
    baton = (BASE / "handoffs" / "successor-activation-candidate.md").read_text(encoding="utf-8")
    assert hold["state"] == "PREPARED_NOT_SENT"
    assert hold["successor_inferred"] is False
    assert hold["recipient_named"] is False
    assert hold["precontact_performed"] is False
    assert hold["send_count"] == 0
    assert "SENT_BY_CAELEN_ASH = false" in baton


def test_validation_candidate_enforces_one_canonical_and_no_full_suite() -> None:
    data = load(BASE / "validation" / "final-validation-candidate.json")
    assert data["source"] == "939312172819669aad250cf034d8a6a7efe3df5b"
    assert data["x1"] == "39daa2da64125b839714efa8b7488d8ed9ed364b"
    assert data["evidence"] == EVIDENCE
    assert data["expected_phase_commits"] == 3
    assert data["expected_merges"] == 0
    assert data["canonical_invocation_limit"] == 1
    assert data["canonical_success_replay_forbidden"] is True
    assert data["full_repository_suite"] is False


def test_no_canonical_receipt_or_latch_is_stored_in_repository() -> None:
    names = [path.name.lower() for path in BASE.rglob("*") if path.is_file()]
    assert "canonical-receipt.json" not in names
    assert "canonical-invocation-latch.json" not in names


def test_final_stage_does_not_modify_immutable_x1_or_x2_paths() -> None:
    if git("rev-parse", "HEAD") == EVIDENCE:
        changed = [line for line in git("status", "--porcelain=v1", "-uall").splitlines() if line]
        paths = [line[3:].replace("\\", "/") for line in changed]
        assert not [path for path in paths if "/x1/" in f"/{path}/" or "/x2/" in f"/{path}/"]


def test_owner_material_remains_below_file_and_document_caps() -> None:
    files = [path for path in BASE.rglob("*") if path.is_file()]
    assert len(files) < 2000
    for path in files:
        if path.suffix.lower() in {".md", ".html"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100_000


def test_all_owner_json_parses_strictly() -> None:
    paths = list(BASE.rglob("*.json"))
    assert len(paths) >= 145
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_final_packet_has_no_private_absolute_path_raw_route_or_secret_assignment() -> None:
    patterns = [
        re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
        re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    ]
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        value = path.read_text(encoding="utf-8")
        for pattern in patterns:
            assert pattern.search(value) is None, f"{pattern.pattern} in {path.relative_to(REPO)}"
