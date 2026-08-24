#!/usr/bin/env python3
"""Pre-canonical final seal tests for Lyren Moss v668-v2."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs/lyren-moss/v668-v2"
SOURCE_FINAL = "ea14c75a4f0c543ef1bb89858e35252302924aec"
X1_HEAD = "0683eb961987fd4c7283d278e3b217647aef73f0"
EVIDENCE_HEAD = "6bb6b96b08eb26646c362967f8ed30263d348c15"
FINAL_OWNER_MANIFEST = "docs/lyren-moss/v668-v2/validation/final-owner-manifest.json"
FINAL_DELTA_MANIFEST = "docs/lyren-moss/v668-v2/validation/final-delta-manifest.json"


def read_json(relative: str) -> dict:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def git_bytes(revision: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", revision], check=True, capture_output=True
    ).stdout


def exists_in_commit(commit: str, path: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", f"{commit}:{path}"], capture_output=True
    ).returncode == 0


def immutable_final_head() -> str | None:
    head = git("rev-parse", "HEAD")
    commits = git("rev-list", "--reverse", "--ancestry-path", f"{EVIDENCE_HEAD}..{head}").splitlines()
    return commits[0] if commits else None


def canonical_bytes(path: str) -> bytes:
    final_head = immutable_final_head()
    if final_head is not None:
        return git_bytes(f"{final_head}:{path}")
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    if path in staged:
        return git_bytes(f":{path}")
    if exists_in_commit(EVIDENCE_HEAD, path):
        return git_bytes(f"{EVIDENCE_HEAD}:{path}")
    data = (ROOT / path).read_bytes()
    return data.replace(b"\r\n", b"\n") if Path(path).suffix.casefold() in {".json", ".md", ".py", ".txt"} else data


def replay_manifest(relative: str) -> int:
    manifest = read_json(relative)
    for row in manifest["entries"]:
        data = canonical_bytes(row["path"])
        assert len(data) == row["bytes"], row["path"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
    return len(manifest["entries"])


def test_exact_lifecycle_anchors() -> None:
    assert git("rev-parse", f"{X1_HEAD}^") == SOURCE_FINAL
    assert git("rev-parse", f"{EVIDENCE_HEAD}^") == X1_HEAD
    final_head = immutable_final_head()
    if final_head is not None:
        assert git("rev-parse", f"{final_head}^") == EVIDENCE_HEAD


def test_final_truth_is_exact_and_not_ready() -> None:
    truth = read_json("final/phase-truth.json")
    assert truth["allowed_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"]
    assert truth["outcome_counts"] == {
        "completed": 28,
        "exact_gate": 2,
        "open_gap": 2,
        "represented": 8,
    }
    assert truth["frozen_proposal_chain"] == 4670
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["canonical_validation_invoked"] is False
    assert truth["successor_contacted"] is False


def test_sealed_counts_are_additive() -> None:
    register = read_json("closeout/retained-negative-register.json")
    assert register["source_repository_seal"] == 29043
    assert register["inbound_route_and_lyren_operational_failures"] == 13
    assert register["owner_synthetic_mutations"] == 160
    assert register["effective_negatives_before_canonical"] == 29216
    assert register["methods_before_canonical"] == 15802
    assert register["failed_witnesses_before_canonical"] == 1517
    assert register["passing_witnesses_before_canonical"] == 2352
    assert register["open_gaps"] == 211
    assert register["exact_gates"] == 206
    assert register["all_retained"] is True


def test_method_flow_retains_thirteen_operational_ids() -> None:
    ledger = read_json("method-flow/method-flow-ledger.json")
    assert len(ledger["retained_method_ids"]) == 13
    assert ledger["successor_visible_external_and_owner_operational"] == {
        "effective_negatives": 13,
        "failed_witnesses": 13,
        "methods": 13,
        "passing_witnesses": 13,
    }
    assert ledger["all_failures_retained"] is True


def test_route_is_prepared_not_sent() -> None:
    route = read_json("closeout/route-and-roster-record.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["prospective_next_exact_title"] == "Ilyra Fen"
    assert route["prospective_next_phase"] == "v668-v3"
    assert route["successor_contacted"] is False
    assert route["tavian_state"] == "ON_STANDBY_NOT_SUBSTITUTE"
    assert route["single_send_maximum"] == 1


def test_activation_packet_is_prepared_and_sanitized() -> None:
    summary = read_json("handoffs/activation-summary.json")
    packet = (PHASE_ROOT / "handoffs/ilyra-fen-v668-v3-activation-prepared.md").read_text(encoding="utf-8")
    assert summary["prepared"] is True and summary["sent"] is False
    assert summary["baton_words"] == len(packet.split())
    assert hashlib.sha256((PHASE_ROOT / "handoffs/ilyra-fen-v668-v3-activation-prepared.md").read_bytes()).hexdigest() == summary["baton_sha256"]
    assert "PREPARED_BY_LYREN_MOSS = true" in packet
    assert "SENT_BY_LYREN_MOSS = false" in packet
    assert "supplied only in the acknowledged live activation" in packet
    for forbidden in ("<source_" + "thread_id>", "client" + "ThreadId", "C:\\Users\\", "D:\\GHC-Archives\\"):
        assert forbidden not in packet


def test_baton_retains_required_boundaries_and_successor_practice() -> None:
    packet = (PHASE_ROOT / "handoffs/ilyra-fen-v668-v3-activation-prepared.md").read_text(encoding="utf-8")
    for phrase in (
        "not evidence of consciousness",
        "NOT_READY_FOR_STAGE_20",
        "Same-owner local software validation",
        "film-scanner calibration custody",
        "one sanitized live activation",
        "Tavian Sol is on standby",
    ):
        assert phrase.casefold() in packet.casefold()


def test_final_manifests_replay_in_canonical_blob_domain() -> None:
    delta_count = replay_manifest("validation/final-delta-manifest.json")
    owner_count = replay_manifest("validation/final-owner-manifest.json")
    assert delta_count > 0
    assert owner_count > 128
    assert owner_count < 2000


def test_evidence_manifest_remains_exactly_128() -> None:
    manifest = read_json("evidence/evidence-content-manifest.json")
    assert manifest["entry_count"] == 128
    for row in manifest["entries"]:
        data = git_bytes(f"{EVIDENCE_HEAD}:{row['path']}")
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_canonical_credit_is_not_invoked_in_repository() -> None:
    credit = read_json("validation/validation-credit.json")
    assert credit["state"] == "NOT_INVOKED"
    assert credit["canonical_invocation_count"] == credit["canonical_success_count"] == 0
    assert credit["post_success_replay_allowed"] is False
    assert credit["independent_reproduction_credit"] == 0


def test_canonical_plan_is_owner_scoped_and_one_shot() -> None:
    plan = read_json("validation/canonical-plan.json")
    assert len(plan["expected_tests"]) == 3
    assert plan["manifest_replays"] == ["x1", "evidence", "final_delta", "final_owner"]
    assert plan["full_repository_suite"] is False
    assert plan["external_audit"] is False
    assert plan["independent_reproduction"] is False
    assert plan["invocation_limit"] == plan["success_limit"] == 1
    assert plan["post_success_replay"] is False


def test_final_commit_shape_when_materialized() -> None:
    final_head = immutable_final_head()
    if final_head is None:
        return
    commits = git("rev-list", "--reverse", f"{SOURCE_FINAL}..{final_head}").splitlines()
    assert commits == [X1_HEAD, EVIDENCE_HEAD, final_head]
    assert git("rev-list", "--merges", f"{SOURCE_FINAL}..{final_head}") == ""
    assert all(len(git("show", "-s", "--format=%P", commit).split()) == 1 for commit in commits)


def test_history_file_does_not_claim_self_hash() -> None:
    history = read_json("closeout/source-to-final-history.json")
    assert history["expected_final_parent"] == EVIDENCE_HEAD
    assert history["expected_new_commit_count"] == 3
    assert history["hard_commit_ceiling"] == 8
    assert history["final_hash_self_reference_possible"] is False
    assert history["final_hash_supplied_external_after_commit"] is True


def test_owner_json_files_parse() -> None:
    owner_manifest = read_json("validation/final-owner-manifest.json")
    count = 0
    for row in owner_manifest["entries"]:
        if row["path"].endswith(".json"):
            json.loads(canonical_bytes(row["path"]).decode("utf-8"))
            count += 1
    assert count >= 100


def test_materialized_files_remain_below_rotation_stop() -> None:
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    assert len(files) < 2000


def test_closeout_preserves_terminal_boundaries() -> None:
    text = (PHASE_ROOT / "final/integrated-closeout.md").read_text(encoding="utf-8")
    for phrase in (
        "NOT_READY_FOR_STAGE_20",
        "No real media",
        "No package was globally installed",
        "complete privacy",
        "independent-reproduction",
        "successor remains uncontacted",
    ):
        assert phrase.casefold() in text.casefold()
