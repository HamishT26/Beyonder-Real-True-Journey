from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "vesper-arlen" / "v673-v6"
SOURCE = "2400427269b28496acaa07cd6c18f5a2236510f7"
X1 = "9a5d432a877d5c11ac60e0d331cf27cfb55c482b"
EVIDENCE = "5b208ceb2cababd14dd5de7e35af792533b12c68"


def load(relative: str):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if check:
        assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    return result.stdout


def staged_final_present() -> bool:
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT, check=False)
    return result.returncode == 1


def final_blob(path: str) -> bytes:
    return git("show", f":{path}" if staged_final_present() else f"HEAD:{path}")


def test_closeout_truth_matches_immutable_evidence() -> None:
    evidence = load("x2/phase-truth.json")
    closeout = load("closeout/phase-truth.json")
    for key in ("outcomes", "open_gaps", "exact_gates", "terminal_verdict"):
        assert closeout[key] == evidence[key]
    assert closeout["effective_negatives"] == evidence["effective_negatives"] + 8
    assert closeout["method_flow_methods"] == evidence["method_flow_methods"] + 8
    assert closeout["failed_witnesses"] == evidence["failed_witnesses"] + 8
    assert closeout["bounded_passing_witnesses"] == evidence["bounded_passing_witnesses"] + 8
    assert closeout["canonical_state"] == "PENDING_EXACT_FINAL_CANONICAL"
    assert closeout["route_state"] == "PREPARED_NOT_SENT"


def test_sealed_totals_are_exact() -> None:
    truth = load("closeout/phase-truth.json")
    assert truth["effective_negatives"] == 37436
    assert truth["method_flow_methods"] == 23764
    assert truth["failed_witnesses"] == 9097
    assert truth["bounded_passing_witnesses"] == 11373
    assert truth["open_gaps"] == 303
    assert truth["exact_gates"] == 296


def test_complete_and_incomplete_work_are_separate() -> None:
    checklist = load("closeout/complete-incomplete-checklist.json")
    assert checklist["all_safe_now_candidate_skill_runner_cfr_plans_addressed"] is True
    assert checklist["unsafe_or_authority_dependent_work_reclassified"] is True
    assert "exact-final canonical result until post-push invocation" in checklist["incomplete_or_reserved"]
    assert "Stage 20" in checklist["incomplete_or_reserved"]


def test_wellbeing_receipt_is_workload_not_subjectivity() -> None:
    receipt = load("closeout/wellbeing-workload-check.json")
    assert receipt["relational_language_only"] is True
    assert receipt["human_wellbeing_claim"] is False
    assert receipt["consciousness_or_personhood_claim"] is False
    assert receipt["workload_controls"]["subagents_spawned"] == 0
    assert receipt["workload_controls"]["successor_precontacts"] == 0


def test_route_is_prepared_not_sent() -> None:
    route = load("route/route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["prospective_exact_title"] == "Lyren Moss"
    assert route["prospective_phase"] == "v673-v7"
    assert route["precontact_performed"] is False
    assert route["sent_by_vesper_arlen"] is False
    assert route["activation_claimed"] is False


def test_handoff_is_sanitized_and_within_word_range() -> None:
    path = OUT / "handoffs" / "lyren-moss-v673-v7-activation-candidate.md"
    text = path.read_text(encoding="utf-8")
    words = len(re.findall(r"\b\S+\b", text))
    receipt = load("handoffs/lyren-moss-v673-v7-activation-candidate.receipt.json")
    assert 10000 <= words <= 100000
    assert receipt["word_count"] == words
    assert receipt["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert receipt["state"] == "PREPARED_NOT_SENT"
    assert receipt["sent_by_vesper_arlen"] is False


def test_handoff_has_all_proposal_and_method_cards() -> None:
    text = (OUT / "handoffs" / "lyren-moss-v673-v7-activation-candidate.md").read_text(encoding="utf-8")
    assert all(f"VA6736-N{index:03d}" in text for index in range(1, 41))
    assert all(f"VA6736-M{index:03d}" in text for index in range(1, 23))
    assert "28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`" in text


def test_accessible_final_report_has_structural_features_and_reservation() -> None:
    html = (OUT / "reports" / "accessible-final-report.html").read_text(encoding="utf-8")
    for token in ('<html lang="en">', "<title>", 'href="#main"', '<main id="main">', "<h1>", "<caption>", 'scope="col"', 'scope="row"', "@media print"):
        assert token in html
    assert "Manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved." in html


def test_final_overview_is_three_page_equivalent_and_bounded() -> None:
    text = (OUT / "reports" / "final-integrated-overview.md").read_text(encoding="utf-8")
    words = len(re.findall(r"\b\S+\b", text))
    assert words >= 1200
    assert words <= 100000
    assert "NOT_READY_FOR_STAGE_20" in text


def test_final_validation_prerequisite_is_pending_and_one_shot() -> None:
    prereq = load("final/final-validation-prerequisites.json")
    assert prereq["state"] == "PENDING_EXACT_FINAL_CANONICAL"
    assert prereq["invocation_limit"] == 1
    assert prereq["success_replay_allowed"] is False
    assert prereq["full_repository_suite"] is False
    assert prereq["independent_reproduction"] is False


def test_content_seal_replays_exact_tree_domain() -> None:
    seal = load("seal/content-seal.json")
    if seal.get("state") == "PENDING_STAGED_FINALIZATION":
        return
    assert seal["state"] == "VALID_CONTENT_SEAL"
    assert seal["entry_count"] == len(seal["entries"]) == 12
    for row in seal["entries"]:
        data = final_blob(row["path"])
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() == row["sha256_normalized_lf"]


def test_final_owner_manifest_replays_exact_tree_domain() -> None:
    manifest = load("validation/final-owner-manifest.json")
    if manifest.get("state") == "PENDING_STAGED_FINALIZATION":
        return
    assert manifest["entry_count"] == len(manifest["entries"])
    assert manifest["entry_count"] + len(manifest["self_exclusions"]) == manifest["owner_path_count"]
    for row in manifest["entries"]:
        data = final_blob(row["path"])
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() == row["sha256_normalized_lf"]


def test_final_delta_manifest_replays_exact_tree_domain() -> None:
    manifest = load("validation/final-delta-manifest.json")
    if manifest.get("state") == "PENDING_STAGED_FINALIZATION":
        return
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        data = final_blob(row["path"])
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() == row["sha256_normalized_lf"]


def test_final_staged_review_and_privacy_are_valid() -> None:
    review = load("validation/final-staged-review.json")
    privacy = load("validation/final-staged-privacy.json")
    if review.get("state") == "PENDING_STAGED_FINALIZATION":
        return
    assert review["state"] == "VALID_FINAL_EXACT_STAGED_SCOPE"
    assert review["out_of_scope_paths"] == []
    assert review["commit_count_after_source"] == 3
    assert review["expected_final_parent"] == EVIDENCE
    assert privacy["state"] == "VALID_ZERO_CONFIRMED_PRIVACY_HITS"
    assert privacy["confirmed_hit_count"] == 0


def test_all_owner_json_parses() -> None:
    paths = sorted(OUT.rglob("*.json"))
    assert len(paths) >= 90
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_no_private_patterns_in_owner_public_text() -> None:
    forbidden = ["source_" + "thread_id", "C:" + "\\Users\\", "private_" + "transcript"]
    for path in [p for p in OUT.rglob("*") if p.is_file()]:
        text = path.read_text(encoding="utf-8")
        assert all(term not in text for term in forbidden)


def test_phase_index_is_additive_and_current() -> None:
    text = (ROOT / "ghc-family-index" / "references" / "v673-v6-vesper-arlen.md").read_text(encoding="utf-8")
    assert X1 in text and EVIDENCE in text
    assert "PREPARED_NOT_SENT" in text
    assert "37,436 effective negatives" in text
    assert "does not replace older family history" in text


def test_commit_lifecycle_is_precommit_or_exact_final() -> None:
    head = git("rev-parse", "HEAD").decode().strip()
    if head == EVIDENCE:
        assert head == EVIDENCE
        assert git("status", "--porcelain").decode().strip()
    else:
        assert int(git("rev-list", "--count", f"{SOURCE}..HEAD").decode()) == 3
        assert int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD").decode()) == 0
        assert git("rev-parse", "HEAD^").decode().strip() == EVIDENCE


def test_owner_file_count_is_below_ceiling() -> None:
    owner_files = [path for path in OUT.rglob("*") if path.is_file()]
    assert 0 < len(owner_files) < 2000


def test_no_successor_delivery_is_claimed_in_repository() -> None:
    for path in [OUT / "route" / "route-state.json", OUT / "handoffs" / "lyren-moss-v673-v7-activation-candidate.receipt.json"]:
        value = json.loads(path.read_text(encoding="utf-8"))
        assert value.get("sent_by_vesper_arlen") is False
