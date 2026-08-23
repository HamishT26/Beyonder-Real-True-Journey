from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "eiren-kestrel" / "v667-v6-r2"
BUILDER_PATH = ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_r2_final.py"
SOURCE_FINAL = "1a754e02bfc705d738285c4a6cf9ce1c948a8580"
X1_HEAD = "0ff9e3058d4df62d30035b7d9f5d5ce0939f10a2"
EVIDENCE_HEAD = "942eda86e745da93ece372d89870e052361b039c"


def load_builder():
    spec = importlib.util.spec_from_file_location("eiren_v667_v6_r2_final", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8")


def test_final_builder_self_validation_passes() -> None:
    receipt = load_builder().validate_tree()
    assert receipt["status"] == "PASS"
    assert receipt["overview_words"] >= 900
    assert receipt["baton_words"] >= 10_000
    assert receipt["x1_manifest_entries"] == 20
    assert receipt["evidence_manifest_entries"] == 389
    assert receipt["final_delta_entries"] >= 15
    assert receipt["final_owner_entries"] >= 400
    assert receipt["staged_status"] == "PASS"


def test_exact_history_is_three_single_parent_commits_with_zero_merges() -> None:
    head = git_text("rev-parse", "HEAD").strip()
    commits = [line for line in git_text("rev-list", "--reverse", f"{SOURCE_FINAL}..{head}").splitlines() if line]
    assert commits == [X1_HEAD, EVIDENCE_HEAD, head]
    assert git_text("rev-list", "--merges", f"{SOURCE_FINAL}..{head}").strip() == ""
    for commit in commits:
        parents = git_text("show", "-s", "--format=%P", commit).strip().split()
        assert len(parents) == 1
    assert git_text("rev-parse", "HEAD^").strip() == EVIDENCE_HEAD


def test_integrated_truth_preserves_sealed_and_external_counts() -> None:
    truth = load("truth/phase-truth.json")
    assert truth["repository_evidence_sealed_counts"] == {
        "failed_witnesses": 450,
        "methods": 14172,
        "negatives": 28166,
        "passing_witnesses": 741,
    }
    overlay = len(load_builder().POST_EVIDENCE_FAILURES)
    assert truth["post_evidence_external_overlay_counts"] == {
        "failed_witnesses": overlay,
        "methods": overlay,
        "negatives": overlay,
        "passing_witnesses": overlay,
    }
    assert (truth["effective_negatives"], truth["effective_methods"]) == (28166 + overlay, 14172 + overlay)
    assert (truth["effective_open_gaps"], truth["effective_exact_gates"]) == (198, 196)
    assert (truth["effective_failed_witnesses"], truth["effective_passing_witnesses"]) == (450 + overlay, 741 + overlay)
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_proposal_and_outcome_truth_remains_exact() -> None:
    truth = load("truth/source-proposal-x1-x2-truth.json")
    assert truth["source_inherited_proposal_count"] == 4470
    assert truth["new_proposal_count"] == 20
    assert truth["selected_inherited_revalidation_count"] == 20
    assert truth["effective_frozen_proposal_count"] == 4490
    assert truth["new_outcomes"] == {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4}
    assert truth["selected_inherited_eiren_novelty_credit"] == 0
    assert truth["selected_inherited_eiren_completion_credit"] == 0
    assert truth["rejecting_mutations"] == 100


def test_post_evidence_failures_are_retained_without_rewriting_evidence() -> None:
    overlay = load("truth/post-evidence-operational-overlay.json")
    methods = load("method-flow/method-flow-state-final.json")
    expected = len(load_builder().POST_EVIDENCE_FAILURES)
    assert overlay["row_count"] == expected
    assert overlay["rows"][0]["failure_id"] == "EK6676R2-POSTEVIDENCE-F001"
    assert overlay["rows"][0]["repository_bytes_changed_by_failure"] == 0
    assert overlay["repository_evidence_rewritten"] is False
    assert methods["evidence_sealed_effective_methods"] == 14172
    assert methods["post_evidence_external_method_additions"] == expected
    assert methods["effective_methods_for_successor"] == 14172 + expected
    assert methods["phase_method_count"] == 246 + expected


def test_all_four_manifests_replay_exact_committed_bytes() -> None:
    for relative, commit in (
        ("validation/immutable-x1-manifest.json", X1_HEAD),
        ("validation/immutable-evidence-manifest.json", EVIDENCE_HEAD),
        ("validation/final-delta-manifest.json", "HEAD"),
        ("validation/final-owner-manifest.json", "HEAD"),
    ):
        manifest = load(relative)
        assert manifest["entry_count"] == len(manifest["entries"])
        for row in manifest["entries"]:
            data = git_bytes("show", f"{commit}:{row['path']}")
            assert len(data) == row["bytes"]
            assert hashlib.sha256(data).hexdigest() == row["sha256"]


def test_staged_review_is_additive_and_private_material_clean() -> None:
    review = load("validation/final-staged-review.json")
    assert review["status"] == "PASS"
    assert review["staged_path_count"] == review["additive_path_count"]
    assert review["non_additive_paths"] == []
    assert review["diff_check"] == "PASS"
    assert review["privacy_class_count"] == 5
    assert review["privacy_candidate_count"] == 0
    assert review["privacy_confirmed_hit_count"] == 0
    assert review["immutable_x1_or_evidence_changes"] == 0


def test_overview_and_baton_preserve_route_and_authority_boundaries() -> None:
    overview = (PHASE_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
    baton = (PHASE_ROOT / "handoffs" / "elaren-kestrel-v667-v7-activation-prepared.md").read_text(encoding="utf-8")
    assert len(overview.split()) >= 900
    assert len(baton.split()) >= 10_000
    assert "NOT_READY_FOR_STAGE_20" in overview and "NOT_READY_FOR_STAGE_20" in baton
    assert "PREPARED_NOT_SENT" in baton
    assert "SENT_BY_EIREN_KESTREL = false at commit time" in baton
    assert "Māori concepts remain under Māori authority" in overview
    assert "Māori concepts remain under Māori authority" in baton


def test_route_is_prepared_unsent_and_standby_untouched() -> None:
    route = load("route/route-state.json")
    assert route["current_assignment"] == "Eiren Kestrel v667-v6-r2"
    assert route["prospective_successor"] == "Elaren Kestrel v667-v7"
    assert route["successor_contacted_during_execution"] is False
    assert route["task_created_or_forked"] is False
    assert route["collaboration_subagent_spawned"] is False
    assert route["standby_contacted"] is False
    assert route["substitute_endpoint_used"] is False
    assert route["delivery_state"] == "PREPARED_NOT_SENT"
    assert route["sent_by_eiren_kestrel"] is False


def test_tool_receipt_has_thirteen_tools_and_no_aggregate_inflation() -> None:
    receipt = load("x2/tooling/thirteen-tool-transaction-receipt.json")
    environment = load("environment/version-receipt.json")
    assert receipt["top_level_program_count"] == 13
    assert receipt["initial_smoke_aggregate"]["passed"] == 12
    assert receipt["initial_smoke_aggregate"]["failed"] == 1
    assert receipt["initial_smoke_aggregate"]["aggregate_success_credit"] == 0
    assert receipt["isolated_dependency_recovery"]["passed"] is True
    assert receipt["isolated_dependency_recovery"]["passing_components_replayed"] == 0
    assert receipt["post_install_audit"]["known_vulnerabilities"] == 0
    assert receipt["post_install_audit"]["replayed"] is False
    assert environment["new_phase_tool_count"] == 13
    assert environment["d_first_isolated"] is True
    assert environment["codex_desktop_updated"] is False
    assert environment["exhaustive_security_claim"] is False


def test_accessibility_structure_and_manual_reservations_remain() -> None:
    reservation = load("report/accessibility-reservation.json")
    assert reservation["automated_structure_present"] is True
    assert reservation["noncolour_states"] is True
    assert reservation["manual_browser_evaluation"] == "reserved"
    assert reservation["screen_reader_evaluation"] == "reserved"
    assert reservation["cognitive_accessibility_evaluation"] == "reserved"
    assert reservation["affected_user_evaluation"] == "reserved"
    assert reservation["Māori_language_evaluation"] == "reserved_under_Māori_authority"
    assert reservation["accessibility_complete"] is False


def test_exact_final_canonical_was_not_invoked_precommit() -> None:
    plan = load("validation/final-validation-plan.json")
    closeout = load("closeout/closeout-receipt.json")
    seal = load("seal/seal-candidate.json")
    assert plan["invocation_target"] == 1
    assert plan["precommit_invocations"] == 0
    assert plan["state"] == "NOT_INVOKED_PRECOMMIT"
    assert closeout["canonical_invocation_count"] == 0
    assert closeout["canonical_success_count"] == 0
    assert closeout["canonical_replayed"] is False
    assert seal["canonical_state"] == "NOT_INVOKED_PRECOMMIT"


def test_every_phase_json_document_parses() -> None:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(paths) >= 380
    for path in paths:
        assert isinstance(json.loads(path.read_text(encoding="utf-8")), dict)
