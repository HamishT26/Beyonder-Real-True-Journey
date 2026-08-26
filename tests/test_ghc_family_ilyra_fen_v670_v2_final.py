"""Closeout and seal tests for Ilyra Fen v670-v2."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from scripts import build_ghc_family_ilyra_fen_v670_v2_final as builder
from scripts import validate_ghc_family_ilyra_fen_v670_v2_final as validator
from scripts.ghc_family_ilyra_v670_v2_evidence_guard import five_class_scan

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "ilyra-fen" / "v670-v2"


def load(relative: str):
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def index_or_head(path: str) -> bytes:
    staged = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=False, capture_output=True)
    return staged.stdout if staged.returncode == 0 else git_bytes("show", f"HEAD:{path}")


def test_exact_final_constants_and_evidence_parent_contract():
    assert builder.SOURCE == validator.SOURCE == "1b25a3e888464698a650cd515f4afae0841100c1"
    assert builder.X1 == validator.X1 == "7283038addb45c27f60a69394f7f12bf22dcb759"
    assert builder.EVIDENCE == validator.EVIDENCE == "8d91a3b40ea17752ceb64d87c541bbb24f6c3b83"
    assert builder.BRANCH == validator.BRANCH


def test_phase_truth_has_exact_counts_outcomes_and_verdict():
    truth = load("closeout/phase-truth.json")
    assert truth["effective_negatives"] == 32237
    assert truth["effective_methods"] == 18345
    assert truth["effective_failed_witnesses"] == 4058
    assert truth["effective_passing_witnesses"] == 5350
    assert truth["open_gaps"] == 243
    assert truth["exact_gates"] == 238
    assert truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["external_actions"] == 0


def test_method_flow_retains_five_post_evidence_failures_at_zero_credit():
    flow = load("closeout/method-flow-final.json")
    assert flow["post_evidence_count"] == 5
    assert len(flow["post_evidence_rows"]) == 5
    assert all(row["completion_credit"] == 0 for row in flow["post_evidence_rows"])
    assert flow["no_failure_erased"] is True


def test_negative_and_gate_registers_preserve_layers():
    negatives = load("closeout/retained-negative-register.json")
    gates = load("closeout/exact-open-gate-register.json")
    assert negatives["source_repository_seal"] == 32057
    assert negatives["evidence_overlay"] == 32232
    assert negatives["post_evidence_operational"] == 5
    assert negatives["effective"] == 32237
    assert negatives["erased"] == 0
    assert gates["effective_open_gaps"] == 243
    assert gates["effective_exact_gates"] == 238
    assert gates["all_remain_visible"] is True


def test_final_proposal_ledger_uses_only_four_labels():
    ledger = load("closeout/proposal-ledger-final.json")
    assert ledger["chain"] == 5310
    assert ledger["new_rows"] == len(ledger["rows"]) == 40
    assert Counter(row["outcome"] for row in ledger["rows"]) == Counter(builder.OUTCOMES)
    assert {row["outcome"] for row in ledger["rows"]} == {"completed", "represented", "open_gap", "exact_gate"}
    assert ledger["universal_novelty_claim"] is False


def test_integrated_overview_is_three_page_equivalent_and_bounded():
    words = len((OWNER_ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8").split())
    assert 1600 <= words <= 100000


def test_accessible_final_report_has_structural_features_and_reservations():
    text = (OWNER_ROOT / "closeout/accessible-final-report.html").read_text(encoding="utf-8")
    for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', "scope='row'", 'role="status"', '@media print'):
        assert token in text
    assert "affected-user evaluation remain reserved" in text


def test_wellbeing_is_relational_corrigible_and_non_authoritative():
    payload = load("closeout/final-wellbeing-check.json")
    assert payload["relational_working_language_only"] is True
    assert payload["no_consciousness_personhood_continuity_employment_qualification_agency_or_authority_claim"] is True
    assert payload["corrigible"] is True
    assert payload["hamish_may_rename_pause_redirect_or_stop"] is True


def test_source_ledger_is_vocabulary_only_with_zero_empirical_rows():
    payload = load("closeout/source-evidence-ledger.json")
    assert len(payload["official_or_primary_sources"]) == 5
    assert payload["empirical_rows_downloaded"] == 0
    assert payload["source_validation_claim"] is False


def test_activation_candidate_is_prepared_not_sent_and_git_blob_ready():
    path = OWNER_ROOT / "handoffs/auren-lark-v670-v3-activation-candidate.md"
    text = path.read_text(encoding="utf-8")
    integrity = load("handoffs/activation-candidate-integrity.json")
    data = path.read_bytes()
    assert 10000 <= len(text.split()) <= 100000
    assert integrity["state"] == "PREPARED_NOT_SENT"
    assert integrity["sent_by_ilyra_fen"] is False
    assert integrity["bytes"] == len(data)
    assert integrity["words"] == len(text.split())
    assert integrity["sha256"] == hashlib.sha256(data).hexdigest()
    assert "SENT_BY_ILYRA_FEN = false" in text


def test_route_state_has_zero_contact_and_no_resend():
    route = load("orchestration/route-state-final-candidate.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["prospective_exact_title"] == "Auren Lark"
    assert route["prospective_phase"] == "v670-v3"
    assert route["successor_contacted"] is False
    assert route["standby_contacted"] is False
    assert route["resend_allowed"] is False


def test_canonical_state_is_not_run_at_commit_and_one_shot_only():
    state = load("final/canonical-invocation-state.json")
    prerequisites = load("final/final-validation-prerequisites.json")
    assert state["state_at_commit"] == "NOT_RUN_PENDING_EXACT_FINAL_GATE"
    assert state["attempts_at_commit"] == state["successes_at_commit"] == 0
    assert prerequisites["one_shot"] is True
    assert prerequisites["replay_after_success"] is False
    assert prerequisites["full_repository_suite"] == "not_run_not_claimed"


def test_every_owner_json_parses_and_every_document_is_below_cap():
    json_paths = sorted(OWNER_ROOT.rglob("*.json"))
    assert len(json_paths) >= 150
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    for path in OWNER_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".tex"}:
            assert len(path.read_text(encoding="utf-8").split()) <= 100000


def test_owner_documents_have_zero_confirmed_five_class_hits():
    hits = []
    for path in OWNER_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".tex"}:
            result = five_class_scan(path.read_text(encoding="utf-8"))
            if result["confirmed_hits"]:
                hits.append({"path": path.relative_to(ROOT).as_posix(), "classes": result["confirmed_hits"]})
    assert hits == []


def test_final_manifests_replay_index_or_head_blobs_exactly():
    for relative in ("validation/final-delta-manifest.json", "validation/final-owner-manifest.json"):
        manifest = load(relative)
        assert manifest["entry_count"] == len(manifest["entries"])
        for row in manifest["entries"]:
            data = index_or_head(row["path"])
            assert row["bytes"] == len(data)
            assert row["sha256"] == hashlib.sha256(data).hexdigest()


def test_final_manifest_coverage_matches_delta_and_owner_surface():
    delta = load("validation/final-delta-manifest.json")
    owner = load("validation/final-owner-manifest.json")
    staged = set(git_text("diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").splitlines())
    expected_delta = staged or set(git_text("diff", "--name-only", builder.EVIDENCE, "HEAD").splitlines())
    committed_owner = set(git_text("ls-tree", "-r", "--name-only", "HEAD", builder.OWNER_PREFIX).splitlines())
    expected_owner = committed_owner | {path for path in staged if path.startswith(builder.OWNER_PREFIX)}
    assert {row["path"] for row in delta["entries"]} | set(delta["self_exclusions"]) == expected_delta
    assert {row["path"] for row in owner["entries"]} | set(owner["self_exclusions"]) == expected_owner


def test_final_staged_review_is_exact_and_freezes_x1_evidence():
    review = load("validation/final-staged-review.json")
    assert review["valid"] is True
    assert review["disallowed_paths"] == []
    assert review["frozen_x1_or_evidence_paths"] == []


def test_x1_and_evidence_paths_are_unchanged_after_evidence_commit():
    changed = git_text(
        "diff",
        "--name-only",
        builder.EVIDENCE,
        "--",
        "docs/ilyra-fen/v670-v2/x1",
        "docs/ilyra-fen/v670-v2/x2",
        "scripts/build_ghc_family_ilyra_fen_v670_v2_x1.py",
        "scripts/build_ghc_family_ilyra_fen_v670_v2_x2.py",
        "scripts/ghc_family_ilyra_v670_v2_constraint_board.py",
        "scripts/ghc_family_ilyra_v670_v2_custody_tribunal.py",
        "scripts/ghc_family_ilyra_v670_v2_evidence_guard.py",
        "tests/test_ghc_family_ilyra_fen_v670_v2_x1.py",
        "tests/test_ghc_family_ilyra_fen_v670_v2_x2.py",
    )
    assert changed == ""


def test_materialized_file_count_stays_below_rotation_guard():
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    assert len(files) < 2000


def test_final_builder_and_validator_are_fail_closed_on_scope():
    assert builder.final_counts()["effective_negatives"] == 32237
    assert validator.BATON_PATH.endswith("auren-lark-v670-v3-activation-candidate.md")
    assert validator.ALLOWED_OUTCOMES == {"completed", "represented", "open_gap", "exact_gate"}
