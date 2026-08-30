from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/auren-lark/v677-v7"
CORRECTION = PHASE / "correction"
VALIDATION = PHASE / "validation"
SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
EVIDENCE = "3f91c32cb1acda2900ce69bedc60971353084775"
FAILED_FINAL = "4aaf45add92b18c5f8bef68ba15dd112e0f5703c"
FAILED_ATTEMPT_SHA256 = (
    "317d525189558ef52075d4e06d2f07b75efa14cda376fb4395fa3ceb183637b4"
)
FAILED_RECEIPT_SHA256 = (
    "e3dfc23b73e1bf90bdb57aecc5ca5874b662233b3bf5a10dfb0a45f8f2141857"
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def test_failed_canonical_is_retained_at_zero_credit() -> None:
    row = load(CORRECTION / "failed-canonical-receipt.json")
    assert row["head"] == FAILED_FINAL
    assert row["status"] == "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT"
    assert row["attempt_receipt_sha256"] == FAILED_ATTEMPT_SHA256
    assert row["failed_receipt_sha256"] == FAILED_RECEIPT_SHA256
    assert row["tests_passed"] == 25 and row["tests_failed"] == 1
    assert row["repository_mutation"] is False
    assert row["task_contact"] is False
    assert row["same_head_retry_permitted"] is False


def test_corrected_truth_is_additive_and_terminally_not_ready() -> None:
    truth = load(CORRECTION / "terminal-correction.json")
    assert truth["source"] == SOURCE
    assert truth["x1"] == X1
    assert truth["evidence"] == EVIDENCE
    assert truth["failed_canonical_head"] == FAILED_FINAL
    assert truth["corrected_final_head"] == "COMMIT_CONTAINING_THIS_FILE"
    assert truth["expected_phase_commits"] == 4
    assert truth["zero_merges"] is True
    assert (
        truth["effective_negatives"],
        truth["effective_methods"],
        truth["retained_failed_witnesses"],
        truth["bounded_passing_witnesses"],
    ) == (45718, 43036, 17379, 26362)
    assert (truth["open_gaps"], truth["exact_gates"]) == (389, 380)
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["route_state"] == "PREPARED_NOT_SENT"


def test_exact_four_outcome_labels_remain_unchanged() -> None:
    outcomes = load(CORRECTION / "terminal-correction.json")["outcomes"]
    assert outcomes == {
        "completed": 42,
        "represented": 12,
        "open_gap": 3,
        "exact_gate": 3,
    }
    assert sum(outcomes.values()) == 60


def test_method_flow_keeps_failure_and_recovery_distinct() -> None:
    flow = load(CORRECTION / "method-flow-correction.json")
    assert len(flow["pairs"]) == 3
    assert len(flow["failures"]) == 3
    assert len(flow["recoveries"]) == 3
    assert flow["failure"]["canonical_success_credit"] == 0
    assert flow["failure"]["retained"] is True
    assert (
        flow["recovery"]["state"]
        == "bounded_passing_dependency_preflight"
    )
    assert flow["recovery"]["old_head_replay"] is False
    assert flow["recovery"]["previously_passing_final_tests_replayed"] is False
    assert flow["pairs"][1]["failure"]["validation_credit"] == 0
    assert (
        flow["pairs"][1]["recovery"]["state"]
        == "bounded_passing_streaming_recovery"
    )
    assert flow["pairs"][2]["failure"]["validation_credit"] == 0
    assert (
        flow["pairs"][2]["recovery"]["state"]
        == "bounded_passing_exact_length_streaming_recovery"
    )
    assert flow["failure_erasure"] is False


def test_index_replay_failure_is_retained_for_streaming_recovery() -> None:
    value = load(CORRECTION / "index-replay-recovery.json")
    assert len(value["pairs"]) == 2
    assert value["failure"]["state"] == "FAILED_ZERO_VALIDATION_CREDIT"
    assert value["failure"]["retained"] is True
    assert (
        value["recovery"]["state"]
        == "bounded_passing_streaming_recovery"
    )
    assert value["recovery"]["failed_batch_replayed"] is False
    assert value["pairs"][1]["failure"]["state"] == (
        "FAILED_ZERO_VALIDATION_CREDIT"
    )
    assert value["pairs"][1]["failure"]["retained"] is True
    assert value["pairs"][1]["recovery"]["state"] == (
        "bounded_passing_exact_length_streaming_recovery"
    )
    assert (
        value["pairs"][1]["recovery"]["failed_streaming_attempt_replayed"]
        is False
    )
    assert value["repository_mutation_during_failure"] is False
    assert value["tests_run_during_failure_or_recovery"] == 0
    assert (
        value["exact_streaming_replay_state"]
        == "EXACT_LENGTH_EXTERNAL_PRECOMMIT_EVIDENCE_ONLY"
    )


def test_only_stale_pair_assertion_is_corrected() -> None:
    path = (
        REPO / "tests/test_ghc_family_auren_lark_v677_v7_final.py"
    )
    text = path.read_text(encoding="utf-8")
    assert 'assert len(flow["precloseout_pairs"]) == 3' in text
    assert 'assert len(flow["precloseout_pairs"]) == 2' not in text


def test_direct_child_correction_history_when_committed() -> None:
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", f"{FAILED_FINAL}^") == EVIDENCE
    if head != FAILED_FINAL:
        assert git("rev-parse", "HEAD^") == FAILED_FINAL
        assert int(git("rev-list", "--count", f"{SOURCE}..HEAD")) == 4
        assert git("rev-list", "--merges", f"{SOURCE}..HEAD") == ""
        for sha in (X1, EVIDENCE, FAILED_FINAL, head):
            assert (
                len(git("rev-list", "--parents", "-n", "1", sha).split())
                == 2
            )


def test_route_stays_prepared_unsent_with_exact_successor_chain() -> None:
    route = load(CORRECTION / "route-plan.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["conditional_successor_title"] == "Sable Rook"
    assert route["conditional_successor_phase"] == "v677-v8"
    assert route["next_after_successor"] == "Caelen Ash"
    assert route["conditional_next_phase"] == "v678-v1"
    assert route["old_head_replay_permitted"] is False
    assert route["message_sent"] is False
    assert route["original_baton"]["words"] == 16617


def test_validation_candidate_reserves_one_new_head_attempt() -> None:
    value = load(CORRECTION / "validation-candidate.json")
    assert value["old_head_canonical"] == "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT"
    assert value["old_head_replayed"] is False
    assert value["corrected_head"] == "COMMIT_CONTAINING_THIS_FILE"
    assert value["corrected_head_canonical_invocations"] == 0
    assert value["corrected_head_canonical_successes"] == 0
    assert value["previously_passing_final_tests_replayed"] is False
    assert value["precommit_validation_failures_retained"] == 2
    assert (
        value["streaming_index_recovery"]
        == "EXACT_LENGTH_EXTERNAL_PRECOMMIT_EVIDENCE_ONLY"
    )
    assert value["complete_repository_suite"] is False
    assert value["independent_reproduction"] is False


def test_authority_boundary_denies_every_promotional_inference() -> None:
    value = load(CORRECTION / "authority-boundary.json")
    assert value["relational_working_language_only"] is True
    for key in (
        "consciousness_or_personhood_evidence",
        "identity_continuity_evidence",
        "employment_or_qualification_evidence",
        "scientific_or_operational_authority",
        "legal_or_cultural_authority",
        "maori_authority",
        "independent_agency",
    ):
        assert value[key] is False
    assert value["human_pause_redirect_rename_stop_control"] is True


def test_correction_manifests_and_scans_are_exact_when_present() -> None:
    delta_path = VALIDATION / "correction-delta-manifest.json"
    if not delta_path.exists():
        return
    delta = load(delta_path)
    owner = load(VALIDATION / "correction-owner-manifest.json")
    privacy = load(VALIDATION / "correction-privacy-scan.json")
    security = load(VALIDATION / "correction-security-scan.json")
    review = load(VALIDATION / "correction-staged-review.json")
    assert delta["entry_count"] == review["delta_entries"]
    assert owner["entry_count"] == review["owner_entries"]
    assert owner["entry_count"] + len(owner["self_exclusions"]) == owner[
        "owner_path_count"
    ]
    assert privacy["confirmed_hits"] == []
    assert security["findings"] == []
    assert review["state"] == "VALID_EXACT_CORRECTION_STAGED_REVIEW"
    assert review["confirmed_privacy_hits"] == 0
    assert review["security_findings"] == 0
    assert review["precanonical_correction_tests_run"] is False
    assert review["retained_precommit_validation_failures"] == 2
    assert review["streaming_index_recovery_required"] is True
    assert review["exact_length_streaming_recovery_required"] is True


def test_correction_manifests_declare_unique_normalized_entries() -> None:
    for name in (
        "correction-delta-manifest.json",
        "correction-owner-manifest.json",
    ):
        manifest = load(VALIDATION / name)
        paths = [row["path"] for row in manifest["entries"]]
        assert manifest["normalized_lf"] is True
        assert manifest["entry_count"] == len(paths)
        assert len(paths) == len(set(paths))
        assert len(manifest["self_exclusions"]) == 5


def test_all_correction_json_is_strict() -> None:
    for path in CORRECTION.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def test_diff_hygiene_and_no_route_side_effect() -> None:
    result = subprocess.run(
        ["git", "diff", "--check"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    route = load(CORRECTION / "route-plan.json")
    assert route["message_sent"] is False
