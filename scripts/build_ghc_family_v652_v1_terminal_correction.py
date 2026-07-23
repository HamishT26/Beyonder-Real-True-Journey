#!/usr/bin/env python3
"""Build the additive Sable v652-v1 terminal correction after a retained final-run blocker."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v652_v1_phase_data as d
import ghc_family_v652_v1_x2_incidents as incidents


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
CLOSEOUT_HEAD = "67ea89adf25dc958c757123501cf43f62f461e2f"
GENERIC_RUNNERS = {
    "scripts/ghc_family_claim_lease_demoter.py",
    "scripts/ghc_family_cruft_pack_guard.py",
    "scripts/ghc_family_oci_referrer_tribunal.py",
    "scripts/ghc_family_gmut_covariant_boards.py",
    "scripts/ghc_family_artifact_lineage_tribunals.py",
    "scripts/ghc_family_reproducible_build_envelope.py",
    "scripts/ghc_family_court_registry_proxy.py",
    "scripts/ghc_family_identity_lifecycle_profiles.py",
    "scripts/ghc_family_stage20_multiverse_board.py",
}


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return sorted({row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3})


def is_owner_path(path: str) -> bool:
    if path.startswith(f"{d.PHASE_ROOT}/") or path in GENERIC_RUNNERS:
        return True
    if path.startswith("scripts/") and "v652_v1" in Path(path).name:
        return True
    return path.startswith("tests/") and "v652_v1" in Path(path).name


def owner_paths() -> list[str]:
    tracked = git("ls-files").splitlines()
    return sorted({path for path in tracked + status_paths() if is_owner_path(path) and (REPO / path).is_file()})


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]|(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![0-9a-f])"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v652_v1_preregistration.py",
        "scripts/build_ghc_family_v652_v1_evidence.py",
        "scripts/build_ghc_family_v652_v1_closeout.py",
        "scripts/build_ghc_family_v652_v1_terminal_correction.py",
        "scripts/ghc_family_v652_v1_evidence_validate.py",
        "scripts/ghc_family_v652_v1_closeout_validate.py",
        "scripts/ghc_family_v652_v1_correction_validate.py",
        "scripts/ghc_family_v652_v1_final_validate.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/final-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/correction-staged-privacy.json",
    }
    candidates, confirmed, scanned = [], [], 0
    for relative in paths:
        try:
            content = (REPO / relative).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {"schema": "ghc.family.v652-v1.correction-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five bounded scanner classes with exact definition quarantine; zero confirmed hits is not complete privacy assurance."}


def update_baton() -> int:
    path = ROOT / "handoffs/orin-thale-v652-v2-activation.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "The combined closeout and seal commit containing this baton cannot truthfully name its own hash;",
        "The additive terminal correction commit containing this revised baton cannot truthfully name its own hash;",
    )
    text = text.replace(
        "The Sable phase used exactly one x1 commit, one x2 evidence commit, and one combined closeout/seal commit after the source. The committed outcome distribution is exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. The effective retained-negative total is 8,018: 7,856 inherited activation negatives, six Sable x1 operational negatives, six Sable x2 or closeout operational negatives, and 150 executed and rejected synthetic mutations. The six include the immutable evidence-stage parser recurrence, four closeout-preflight wrapper failures, and one overbroad staged-validator assertion; all made no unauthorized mutation and retain zero first-pass credit.",
        "The Sable phase used exactly one x1 commit, one x2 evidence commit, one combined closeout/seal commit, and one additive terminal correction commit after the source. The committed outcome distribution is exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. The effective retained-negative total is 8,019: 7,856 inherited activation negatives, six Sable x1 operational negatives, seven Sable x2 or lifecycle operational negatives, and 150 executed and rejected synthetic mutations. The seven include the immutable evidence-stage parser recurrence, four closeout-preflight wrapper failures, one overbroad staged-validator assertion, and one failed exact-final historical-self-state selection; all made no unauthorized mutation and retain zero first-pass credit.",
    )
    text = text.replace(
        "The Sable phase used exactly one x1 commit, one x2 evidence commit, one combined closeout/seal commit, and one additive terminal correction commit after the source. The committed outcome distribution is exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. The effective retained-negative total is 8,019: 7,856 inherited activation negatives, six Sable x1 operational negatives, seven Sable x2 or lifecycle operational negatives, and 150 executed and rejected synthetic mutations. The seven include the immutable evidence-stage parser recurrence, four closeout-preflight wrapper failures, one overbroad staged-validator assertion, and one failed exact-final historical-self-state selection; all made no unauthorized mutation and retain zero first-pass credit.",
        "The Sable phase used exactly one x1 commit, one x2 evidence commit, one combined closeout/seal commit, and one additive terminal correction commit after the source. The committed outcome distribution is exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. The effective retained-negative total is 8,021: 7,856 inherited activation negatives, six Sable x1 operational negatives, nine Sable x2 or lifecycle operational negatives, and 150 executed and rejected synthetic mutations. The nine include the immutable evidence-stage parser recurrence, four closeout-preflight wrapper failures, one overbroad staged-validator assertion, one failed exact-final historical-self-state selection, one stale correction commit-count assertion, and one failed bulk-patch context match; all made no unauthorized mutation and retain zero first-pass credit.",
    )
    text = text.replace("three-commit single-parent zero-merge history", "four-commit single-parent zero-merge history")
    text = text.replace("Preserve all 8,018 inherited effective negatives", "Preserve all 8,021 inherited effective negatives")
    text = text.replace("Preserve all 8,019 inherited effective negatives", "Preserve all 8,021 inherited effective negatives")
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return len(re.findall(r"\b\w+(?:[-']\w+)*\b", text))


def build_manifests() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/correction-owner-manifest.json",
        f"{d.PHASE_ROOT}/validation/correction-delta-manifest.json",
        f"{d.PHASE_ROOT}/validation/correction-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/correction-staged-review.json",
        f"{d.PHASE_ROOT}/validation/correction-precommit-validation.json",
    ]
    for relative in exclusions:
        write_json(relative.removeprefix(f"{d.PHASE_ROOT}/"), {"state": "self_excluded_pending_refresh"})
    paths = owner_paths()
    delta = status_paths()
    entries = [hash_entry(path) for path in paths if path not in exclusions]
    delta_entries = [hash_entry(path) for path in delta if path not in exclusions and (REPO / path).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/correction-staged-privacy.json", privacy)
    write_json("validation/correction-owner-manifest.json", {"schema": "ghc.family.v652-v1.correction-owner-manifest.v1", "hash_domain": "git_path_filtered_blob", "owner_path_count": len(paths), "entry_count": len(entries), "self_exclusion_count": len(exclusions), "self_exclusions": exclusions, "entries": entries, "coverage_boundary": "All Sable v652-v1 owner paths at the correction candidate except five declared self-referential or later-written validation receipts."})
    write_json("validation/correction-delta-manifest.json", {"schema": "ghc.family.v652-v1.correction-delta-manifest.v1", "parent": CLOSEOUT_HEAD, "delta_path_count": len(delta), "entry_count": len(delta_entries), "self_exclusion_count": len(exclusions), "self_exclusions": exclusions, "entries": delta_entries, "coverage_boundary": "The exact closeout-to-correction staged surface except five declared lifecycle self-exclusions."})
    write_json("validation/correction-staged-review.json", {"schema": "ghc.family.v652-v1.correction-staged-review.v1", "expected_parent": CLOSEOUT_HEAD, "head_is_expected_parent": git("rev-parse", "HEAD") == CLOSEOUT_HEAD, "delta_path_count": len(delta), "owner_path_count": len(paths), "manifest_entries": len(entries), "delta_manifest_entries": len(delta_entries), "self_exclusions": exclusions, "privacy_confirmed_hits": privacy["confirmed_hit_count"], "failed_canonical_attempts": 1, "successful_canonical_passes": 0, "terminal_route": "PREPARED_NOT_SENT"})


def build() -> None:
    if git("rev-parse", "HEAD") != CLOSEOUT_HEAD:
        raise RuntimeError("terminal correction builder requires the exact closeout head")
    baton_words = update_baton()
    if not 10_000 <= baton_words <= 100_000:
        raise RuntimeError(f"baton word count outside 10,000..100,000: {baton_words}")
    overview = ROOT / "overview/final-integrated-overview.md"
    marker = "## Additive terminal correction"
    text = overview.read_text(encoding="utf-8")
    if marker not in text:
        text = text.rstrip() + "\n\n## Additive terminal correction\n\nThe first exact-final aggregate stopped before producing a receipt because it selected an immutable x1 self-state test against the advanced x2 tree. An isolated diagnostic retained the exact failure: six of seven x1 tests passed, while the remaining test correctly required the x1 revision to have no `surfaces/` directory. The eligible advanced-tree diagnostic then passed all fifteen x2 and closeout tests. This failure adds one retained negative, making the effective total 8,019. It does not alter the 23 completed, 5 represented, 1 open_gap, and 1 exact_gate outcomes, the sixty-two open gaps, the sixty-three exact gates, or the NOT_READY_FOR_STAGE_20 verdict. The correction uses a fourth single-parent commit within the six-commit ceiling, preserves the closeout head and manifests, and leaves one successful exact-final pass pending.\n"
        overview.write_text(text, encoding="utf-8", newline="\n")
    else:
        text = text.replace(
            "This failure adds one retained negative, making the effective total 8,019.",
            "The failed exact-final selection, stale correction commit-count assertion, and failed bulk-patch context match add three retained negatives, making the effective total 8,021. Each later passing recovery preserves its original failure with zero first-pass credit.",
        )
        text = text.replace(
            "That failed exact-final selection and the later stale correction commit-count assertion add two retained negatives, making the effective total 8,020. The correction precommit stop and its isolated six-of-seven diagnostic remain zero-credit witnesses of the same second negative; the corrected closeout selection then passed seven of seven.",
            "The failed exact-final selection, stale correction commit-count assertion, and failed bulk-patch context match add three retained negatives, making the effective total 8,021. The correction precommit stop and its isolated six-of-seven diagnostic are two zero-credit witnesses of one negative; the corrected closeout selection then passed seven of seven. The failed bulk patch changed nothing and was recovered through exact live-context edits.",
        )
        overview.write_text(text, encoding="utf-8", newline="\n")

    truth = read_json("final/phase-truth.json")
    truth.update({"effective_negatives": 8021, "negative_breakdown": {"inherited_effective": d.INHERITED_NEGATIVES, "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES), "x2_or_lifecycle_operational": len(incidents.INCIDENTS), "executed_synthetic": 150}, "phase_commit_count_candidate": 4, "closeout_head": CLOSEOUT_HEAD, "canonical_final_state": "pending_after_retained_failed_attempt"})
    write_json("final/phase-truth.json", truth)
    board = read_json("final/terminal-evidence-board.json")
    board.update({"effective_negatives": 8021, "canonical_final_state": "pending_after_retained_failed_attempt", "failed_canonical_attempts": 1, "successful_canonical_passes": 0})
    write_json("final/terminal-evidence-board.json", board)
    write_json("truth/final-retained-negative-register.json", {"schema": "ghc.family.v652-v1.retained-negatives.final.v2", "effective": 8021, "inherited_effective": d.INHERITED_NEGATIVES, "x1_operational": d.X1_OPERATIONAL_NEGATIVES, "x2_or_lifecycle_operational": incidents.INCIDENTS, "executed_synthetic": 150, "failed_canonical_attempts": 1, "no_failure_erased": True, "zero_first_pass_credit_for_failures": True})
    write_json("validation/exact-final-failed-first.json", {"schema": "ghc.family.v652-v1.exact-final.failed-first.v1", "negative_id": "V6521-X2-N07", "receipt_written": False, "successful_canonical_passes": 0, "aggregate_state": "stopped_before_receipt", "aggregate_observed": "The x1 unittest subprocess returned nonzero before x2 and closeout selections ran.", "isolated_diagnostic": {"passed": 6, "failed": 1, "failure": "test_document_caps_privacy_and_x1_only expected the x1 revision to have no surfaces directory"}, "corrected_advanced_tree_diagnostic": {"x2": "8/8", "closeout": "7/7", "total": "15/15"}, "recovery": "Bind the x1 tests to the immutable x1 revision through its exact manifest and ancestry; select only eligible x2 and closeout tests on the advanced tree.", "boundary": "Retained zero-credit same-owner failure evidence; the one successful exact-final canonical pass remains pending."})
    write_json("validation/correction-precommit-failed-first.json", {"schema": "ghc.family.v652-v1.correction-precommit.failed-first.v1", "negative_id": "V6521-X2-N08", "receipt_written": False, "canonical_final_credit": False, "aggregate_state": "stopped_before_manifest_checks", "aggregate_observed": "The closeout unittest subprocess returned nonzero.", "isolated_diagnostic": {"passed": 6, "failed": 1, "failure": "test_commit_contract expected planned_phase_total 3 while the correction contract requires 4"}, "corrected_diagnostic": {"closeout": "7/7"}, "recovery": "Update only the advanced lifecycle-count assertion; preserve the immutable closeout receipt at its exact revision.", "boundary": "Two failed witnesses of one retained zero-credit negative; the successful exact-final pass remains pending."})
    write_json("validation/correction-bulk-patch-failed.json", {"schema": "ghc.family.v652-v1.correction-bulk-patch.failed.v1", "negative_id": "V6521-X2-N09", "mutation_occurred": False, "observed": "apply_patch rejected a bulk correction edit because one expected live-source context did not match.", "recovery": "Read exact live spans and apply small path-specific patches.", "boundary": "Retained zero-credit tooling failure; no validation or scientific credit."})
    write_json("final/terminal-correction-receipt.json", {"schema": "ghc.family.v652-v1.terminal-correction.v3", "parent_closeout_head": CLOSEOUT_HEAD, "reasons": ["retained historical x1 self-state test selected at advanced head", "retained stale correction commit-count assertion", "retained failed bulk-patch context match"], "negative_ids": ["V6521-X2-N07", "V6521-X2-N08", "V6521-X2-N09"], "effective_negatives": 8021, "phase_commit_count_candidate": 4, "commit_ceiling": 6, "outcomes_unchanged": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, "gaps": 62, "gates": 63, "verdict": "NOT_READY_FOR_STAGE_20", "successful_canonical_passes": 0, "canonical_final_state": "pending_postcommit_single_pass", "route": "PREPARED_NOT_SENT"})
    write_json("final/commit-cap-contract.json", {"schema": "ghc.family.v652-v1.commit-cap.v2", "source_head": d.SOURCE_HEAD, "x1_commits": 1, "x2_evidence_commits": 1, "x2_closeout_commits": 1, "terminal_correction_commits": 1, "planned_phase_total": 4, "maximum": 6, "merge_commits_allowed": 0})
    write_json("final/source-and-ancestry-contract.json", {"schema": "ghc.family.v652-v1.ancestry-contract.v2", "source": d.SOURCE_HEAD, "x1": "0e7efd8f49dbb530d60e9d2f1b474a3de9a035c2", "evidence": "fddc360ee643b7b50f7c65395a39948cf0c0d535", "closeout": CLOSEOUT_HEAD, "final": "resolved_only_by_postcommit_validator", "expected_phase_commits": 4, "expected_merges": 0, "expected_final_parents": 1})
    write_json("final/final-receipt.json", {"schema": "ghc.family.v652-v1.final-receipt.v2", "state": "terminal_correction_candidate_complete", "exact_head": "resolved_only_by_postcommit_validator", "canonical_exact_final_state": "pending_postcommit_single_pass", "failed_canonical_attempts": 1, "successful_canonical_passes": 0, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "future_cli_seats_launched": 0, "route": "PREPARED_NOT_SENT"})
    write_json("final/seal-receipt.json", {"schema": "ghc.family.v652-v1.seal-receipt.v2", "state": "closeout_seal_preserved_with_additive_terminal_correction_candidate", "closeout_head": CLOSEOUT_HEAD, "source_head": d.SOURCE_HEAD, "x1_head": "0e7efd8f49dbb530d60e9d2f1b474a3de9a035c2", "evidence_head": "fddc360ee643b7b50f7c65395a39948cf0c0d535", "expected_phase_commits": 4, "expected_merges": 0, "expected_final_parents": 1, "commit_cap": 6, "canonical_exact_final_state": "pending_postcommit_single_pass"})

    documents = []
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", path.read_text(encoding="utf-8")))
        documents.append({"path": relative, "words": words, "baton_exception": relative == "handoffs/orin-thale-v652-v2-activation.md"})
    write_json("final/document-word-counts.json", {"schema": "ghc.family.v652-v1.document-words.v2", "documents": documents, "ordinary_cap": 100000, "baton_minimum": 10000, "baton_maximum": 100000, "valid": all((row["baton_exception"] and 10000 <= row["words"] <= 100000) or (not row["baton_exception"] and row["words"] <= 100000) for row in documents)})
    write_json("final/owner-growth-receipt.json", {"schema": "ghc.family.v652-v1.owner-growth.v2", "owner_file_count_before_correction_manifests": len(owner_paths()), "rotation_threshold": 15000, "below_threshold": len(owner_paths()) < 15000, "inherited_repository_baseline_not_used_as_trigger": True})
    build_manifests()
    privacy = read_json("validation/correction-staged-privacy.json")
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    print(json.dumps({"valid": True, "negatives": 8021, "phase_commit_candidate": 4, "baton_words": baton_words, "owner_paths": read_json("validation/correction-owner-manifest.json")["owner_path_count"], "state": "terminal_correction_candidate_not_committed"}, sort_keys=True))


if __name__ == "__main__":
    build()
