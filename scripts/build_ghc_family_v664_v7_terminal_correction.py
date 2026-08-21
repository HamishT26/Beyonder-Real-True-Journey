#!/usr/bin/env python3
"""Build and exact-review the additive Sable Rook v664-v7 terminal correction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_closeout as closeout  # noqa: E402


PREFIX = closeout.PREFIX
SOURCE = closeout.SOURCE
X1 = closeout.X1
EVIDENCE = closeout.EVIDENCE
BASE_FINAL = "32f4c9f572059f655e8c8c69ca9fbe603de62946"
BRANCH = closeout.BRANCH
VERDICT = closeout.VERDICT
BUILDER = "scripts/build_ghc_family_v664_v7_terminal_correction.py"
CANONICAL = "scripts/ghc_family_v664_v7_canonical_validator_v2.py"
TEST = "tests/test_ghc_family_sable_v664_v7_terminal_correction.py"
FAILED_CANONICAL_SHA256 = "3a36101ce75282fdd870defb25e6bc8bf990d329689467e17a3a958f959446af"
SCANNER_DEFINITION_DIGESTS = {
    "33e7b9c64bc6953375c7a8bc30d96dba57f474347278e324105aa29d80c1b9f1",
    "d469e413f8bdab9ccf5b3108935403fa3269515b4e66ef76a5561ac3f5be350d",
}
CORRECTION_OWNER_MANIFEST = f"{PREFIX}validation/correction-owner-manifest.json"
CORRECTION_DELTA_MANIFEST = f"{PREFIX}validation/correction-delta-manifest.json"
CORRECTION_CANDIDATE = f"{PREFIX}validation/correction-stage-candidate.json"
CORRECTION_REVIEW = f"{PREFIX}validation/correction-staged-review.json"
CORRECTION_EXCLUSIONS = sorted(
    [CORRECTION_OWNER_MANIFEST, CORRECTION_DELTA_MANIFEST, CORRECTION_CANDIDATE, CORRECTION_REVIEW]
)
GENERATED_RELATIVE = [
    "correction/canonical-failure-receipt.json",
    "correction/content-seal.json",
    "correction/correction-inventory.json",
    "correction/correction-receipt.json",
    "correction/method-flow-overlay.json",
    "correction/phase-truth.json",
    "orchestration/terminal-route-state-correction.json",
    "reports/terminal-correction-overview.md",
    "validation/correction-canonical-contract.json",
    "validation/correction-delta-manifest.json",
    "validation/correction-owner-manifest.json",
    "validation/correction-stage-candidate.json",
    "validation/correction-staged-review.json",
]
CORRECTION_PATHS = sorted(
    [BUILDER, CANONICAL, TEST, *[f"{PREFIX}{relative}" for relative in GENERATED_RELATIVE]]
)


class CorrectionError(RuntimeError):
    """Raised when the additive terminal correction cannot be verified."""


def corrected_scan(path: str, raw: bytes) -> list[dict[str, str]]:
    rows = closeout.scan(path, raw)
    for row in rows:
        if (
            path == closeout.evidence.EVIDENCE_BUILDER
            and row["class"] == "private_route_or_callable"
            and row["excerpt_sha256"] in SCANNER_DEFINITION_DIGESTS
        ):
            row["disposition"] = "scanner_definition"
            row["adjudication"] = "exact digest matches immutable evidence-stage scanner-definition receipt"
    return rows


def write_json(relative: str, value: Any) -> str:
    return closeout.write_json(relative, value)


def write_text(relative: str, value: str) -> str:
    return closeout.write_text(relative, value)


def working_paths() -> list[str]:
    return sorted(
        set(
            closeout.zpaths("diff", "--name-only", "-z")
            + closeout.zpaths("diff", "--cached", "--name-only", "-z")
            + closeout.zpaths("ls-files", "--others", "--exclude-standard", "-z")
        )
    )


def staged_paths() -> list[str]:
    return closeout.zpaths("diff", "--cached", "--name-only", "-z")


def base_owner_paths() -> list[str]:
    return closeout.zpaths("diff", "--name-only", "-z", f"{SOURCE}..{BASE_FINAL}")


def build_documents() -> dict[str, Any]:
    if closeout.git_text("rev-parse", "HEAD") != BASE_FINAL:
        raise CorrectionError("terminal correction requires the exact failed-canonical final")
    current = working_paths()
    unexpected = sorted(set(current) - set(CORRECTION_PATHS))
    if unexpected:
        raise CorrectionError(f"unexpected paths before correction build: {unexpected}")

    failure = {
        "schema": "ghc.family.sable.v664-v7.failed-canonical-receipt.v1",
        "base_final": BASE_FINAL,
        "external_receipt_sha256": FAILED_CANONICAL_SHA256,
        "valid": False,
        "tests": 35,
        "checks": 27,
        "passed_checks": 26,
        "strict_json": 142,
        "owner_paths": 185,
        "confirmed_privacy_candidates": 2,
        "candidate_paths": [closeout.evidence.EVIDENCE_BUILDER],
        "candidate_classes": ["private_route_or_callable"],
        "candidate_excerpt_sha256": sorted(SCANNER_DEFINITION_DIGESTS),
        "completion_credit": 0,
        "repository_mutation_during_validation": False,
        "send_performed": False,
        "disposition": "retained_failed_canonical_zero_credit",
    }
    write_json("correction/canonical-failure-receipt.json", failure)

    canonical_method = {
        "method_id": "SR6647-M024",
        "negative_id": "SR6647-CANONICAL-NEG001",
        "trigger": "whole-owner-scanner-definition-adjudication",
        "state": "candidate",
        "failed_witness": "The first and only canonical invocation at the base final passed 26 of 27 checks but classified two immutable evidence-scanner regex literals as confirmed privacy candidates.",
        "failed_witness_credit": "zero",
        "passing_witness": "Adjudicate only the two exact excerpt digests already recorded as scanner definitions by the immutable evidence staged review, then rebuild exact correction manifests before a new-final canonical attempt.",
        "promotion_rule": "Preferred only after the corrected exact-final canonical aggregate passes once.",
        "recurrence_guard": "Carry scanner-definition adjudications by exact path, class, and digest across whole-owner scans.",
        "rollback": "Preserve the invalid external receipt and base final; add one correction commit without reset, amend, rewrite, force push, or deletion.",
        "sibling_recommendation": "Treat scanner source literals as candidates requiring exact prior-receipt adjudication, never blanket suppression.",
    }
    sparse_method = {
        "method_id": "SR6647-M025",
        "negative_id": "SR6647-CORRECTION-NEG002",
        "trigger": "terminal-correction-sparse-staging-coverage",
        "state": "preferred",
        "failed_witness": "The first exact correction staging attempt staged fifteen intended paths but refused the new correction builder because that one owner path was outside the inherited sparse specification.",
        "failed_witness_credit": "zero",
        "passing_witness": "Add only the exact correction-builder path to the sparse specification and restage all sixteen paths from the immutable correction inventory.",
        "promotion_rule": "Preferred for an exact owner path after the bounded sparse addition and complete staged allowlist pass.",
        "recurrence_guard": "Compare every additive lifecycle builder against the sparse pattern set before its first stage attempt.",
        "rollback": "Do not unstage the fifteen valid owner paths; add only the refused builder path and rerun exact staged review.",
        "sibling_recommendation": "Preflight additive terminal-correction builders against sparse definitions before staging.",
    }
    failures = [canonical_method, sparse_method]
    method_flow = {
        "schema": "ghc.family.sable.v664-v7.terminal-correction-method-flow.v1",
        "base_effective_negatives": 24934,
        "base_effective_methods": 8948,
        "new_failed_witness_count": 2,
        "new_passing_witness_count": 1,
        "effective_negatives": 24936,
        "effective_methods": 8950,
        "failures": failures,
        "failure_erasure_count": 0,
        "valid": True,
    }
    write_json("correction/method-flow-overlay.json", method_flow)

    truth = {
        "schema": "ghc.family.sable.v664-v7.terminal-correction-phase-truth.v1",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "base_final": BASE_FINAL,
        "corrected_final": "assigned_only_after_containing_commit_exists",
        "phase_commit_count_candidate": 4,
        "zero_merge_candidate": True,
        "final_single_parent_candidate": True,
        "frozen_proposal_count": 3990,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": 24936,
        "effective_methods": 8950,
        "effective_open_gaps": 173,
        "effective_exact_gates": 171,
        "failed_canonical_receipts": 1,
        "successful_canonical_receipts": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("correction/phase-truth.json", truth)

    route = {
        "schema": "ghc.family.sable.v664-v7.terminal-route-state.correction.v1",
        "state": "PREPARED_NOT_SENT",
        "successor_title": None,
        "successor_phase": None,
        "send_count": 0,
        "task_created": False,
        "task_forked": False,
        "precontact_performed": False,
        "valid": True,
    }
    write_json("orchestration/terminal-route-state-correction.json", route)

    receipt = {
        "schema": "ghc.family.sable.v664-v7.terminal-correction-receipt.v1",
        "base_final": BASE_FINAL,
        "correction_final": "assigned_after_commit",
        "failed_canonical_sha256": FAILED_CANONICAL_SHA256,
        "corrected_scanner_definition_digests": sorted(SCANNER_DEFINITION_DIGESTS),
        "canonical_v2": "pending_one_exact-final_invocation",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("correction/correction-receipt.json", receipt)

    seal = {
        "schema": "ghc.family.sable.v664-v7.terminal-correction-content-seal.v1",
        "immutable_base_final": BASE_FINAL,
        "invalid_canonical_receipt_preserved": True,
        "invalid_receipt_sha256": FAILED_CANONICAL_SHA256,
        "adjudication_scope": "two exact immutable evidence-scanner definition digests only",
        "history_rewritten": False,
        "failed_witness_erased": False,
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("correction/content-seal.json", seal)

    contract = {
        "schema": "ghc.family.sable.v664-v7.corrected-canonical-contract.v1",
        "script": CANONICAL,
        "base_failed_receipt_sha256": FAILED_CANONICAL_SHA256,
        "required_tests": [
            "tests.test_ghc_family_sable_v664_v7_x1",
            "tests.test_ghc_family_sable_v664_v7_x2",
            "tests.test_ghc_family_sable_v664_v7_closeout",
            "tests.test_ghc_family_sable_v664_v7_terminal_correction",
        ],
        "whole_owner_privacy_scan": True,
        "exact_scanner_definition_allowlist": sorted(SCANNER_DEFINITION_DIGESTS),
        "one_successful_invocation": True,
        "post_success_replay": False,
        "full_repository_suite": False,
        "valid": True,
    }
    write_json("validation/correction-canonical-contract.json", contract)

    overview = f"""# Sable Rook v664-v7 terminal correction

The first exact-final canonical invocation at `{BASE_FINAL}` remains an invalid, zero-credit witness. It passed 35 scoped tests and 26 of 27 checks but failed the whole-owner five-class scan because two regex literals in the immutable evidence scanner were not carried forward as scanner-definition adjudications. Their exact excerpt digests match the immutable evidence staged-review receipt; no payload, private route, credential, raw identifier, transcript, or private local path was found.

This additive correction does not rewrite x1, evidence, the base final, or its failed external receipt. It changes only the terminal scanner contract and lifecycle evidence needed to carry the two exact path/class/digest adjudications. A later exact staging attempt also retained one sparse-path refusal before the correction builder was added explicitly. Working truth is now 24,936 retained negatives and 8,950 Method Flow methods, with 173 open gaps, 171 exact gates, outcomes 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`, and `{VERDICT}`.

The canonical v2 aggregate may run only after this correction commit is pushed, clean, typed 0/0 divergent, and fresh-live equal. A successful run must not be replayed. The route remains `PREPARED_NOT_SENT`; no successor is named or contacted by this correction.
"""
    write_text("reports/terminal-correction-overview.md", overview)

    inventory = {
        "schema": "ghc.family.sable.v664-v7.terminal-correction-inventory.v1",
        "path_count": len(CORRECTION_PATHS),
        "paths": CORRECTION_PATHS,
        "within_2000_file_guard": len(CORRECTION_PATHS) < 2000,
        "valid": True,
    }
    write_json("correction/correction-inventory.json", inventory)

    for relative, schema in [
        ("validation/correction-owner-manifest.json", "ghc.family.sable.v664-v7.correction-owner-manifest.pending.v1"),
        ("validation/correction-delta-manifest.json", "ghc.family.sable.v664-v7.correction-delta-manifest.pending.v1"),
        ("validation/correction-stage-candidate.json", "ghc.family.sable.v664-v7.correction-stage-candidate.pending.v1"),
        ("validation/correction-staged-review.json", "ghc.family.sable.v664-v7.correction-staged-review.pending.v1"),
    ]:
        write_json(relative, {"schema": schema, "pending_exact_staged_review": True})

    actual = working_paths()
    if actual != CORRECTION_PATHS:
        raise CorrectionError(f"correction inventory differs: expected={CORRECTION_PATHS} actual={actual}")
    return {
        "valid": True,
        "correction_paths": len(CORRECTION_PATHS),
        "negatives": 24936,
        "methods": 8950,
        "failed_canonical_receipts": 1,
        "terminal_verdict": VERDICT,
    }


def record(path: str, staged: set[str]) -> dict[str, Any]:
    if path in staged:
        raw = closeout.index_blob(path)
        oid = closeout.index_oid(path)
    else:
        raw = closeout.commit_blob(BASE_FINAL, path)
        oid = closeout.commit_oid(BASE_FINAL, path)
    return {
        "path": path,
        "mode": "100644",
        "object_type": "blob",
        "git_blob": oid,
        "sha256": closeout.sha256(raw),
        "size": len(raw),
        "hash_domain": "exact Git blob",
    }


def write_staged_review() -> dict[str, Any]:
    if closeout.git_text("rev-parse", "HEAD") != BASE_FINAL:
        raise CorrectionError("correction staged review requires immutable base final")
    actual = staged_paths()
    if actual != CORRECTION_PATHS:
        raise CorrectionError("correction staged paths differ from inventory")
    overwritten = [path for path in actual if closeout.run_git("cat-file", "-e", f"{BASE_FINAL}:{path}", check=False).returncode == 0]
    if overwritten:
        raise CorrectionError(f"correction overwrites base-final paths: {overwritten}")
    json_count = 0
    python_count = 0
    candidates: list[dict[str, str]] = []
    for path in actual:
        raw = closeout.index_blob(path)
        if path.endswith(".json"):
            closeout.strict_json(raw, path)
            json_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        if Path(path).suffix.lower() in closeout.TEXT_SUFFIXES:
            candidates.extend(corrected_scan(path, raw))
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_issue"]
    if confirmed:
        raise CorrectionError(f"confirmed correction privacy findings: {confirmed}")
    diff = closeout.run_git("diff", "--cached", "--check", check=False)
    if diff.returncode:
        raise CorrectionError((diff.stdout + diff.stderr).decode("utf-8", "replace"))

    staged = set(actual)
    owner_paths = sorted(set(base_owner_paths()) | staged)
    owner_entries = [record(path, staged) for path in owner_paths if path not in CORRECTION_EXCLUSIONS]
    delta_entries = [record(path, staged) for path in actual if path not in CORRECTION_EXCLUSIONS]
    owner = {
        "schema": "ghc.family.sable.v664-v7.correction-owner-manifest.v1",
        "source": SOURCE,
        "base_final": BASE_FINAL,
        "intended_path_count": len(owner_paths),
        "entry_count": len(owner_entries),
        "declared_self_exclusion_count": len(CORRECTION_EXCLUSIONS),
        "declared_self_exclusions": CORRECTION_EXCLUSIONS,
        "entries": owner_entries,
        "coverage_valid": len(owner_entries) + len(CORRECTION_EXCLUSIONS) == len(owner_paths),
    }
    delta = {
        "schema": "ghc.family.sable.v664-v7.correction-delta-manifest.v1",
        "base_final": BASE_FINAL,
        "intended_path_count": len(actual),
        "entry_count": len(delta_entries),
        "declared_self_exclusion_count": len(CORRECTION_EXCLUSIONS),
        "declared_self_exclusions": CORRECTION_EXCLUSIONS,
        "entries": delta_entries,
        "coverage_valid": len(delta_entries) + len(CORRECTION_EXCLUSIONS) == len(actual),
    }
    review = {
        "schema": "ghc.family.sable.v664-v7.correction-staged-review.v1",
        "staged_path_count": len(actual),
        "immutable_base_overwrites": overwritten,
        "strict_json_count": json_count,
        "python_compile_count": python_count,
        "scanner_candidate_count": len(candidates),
        "scanner_definition_count": sum(row["disposition"] == "scanner_definition" for row in candidates),
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
        "scanner_candidates": candidates,
        "diff_hygiene_issues": 0,
        "valid": not overwritten and not confirmed,
    }
    candidate = {
        "schema": "ghc.family.sable.v664-v7.correction-stage-candidate.v1",
        "branch": BRANCH,
        "base_final": BASE_FINAL,
        "corrected_final": "assigned_after_commit",
        "failed_canonical_sha256": FAILED_CANONICAL_SHA256,
        "canonical_v2": "pending_one_exact-final_invocation",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": VERDICT,
        "valid": owner["coverage_valid"] and delta["coverage_valid"] and review["valid"],
    }
    write_json("validation/correction-owner-manifest.json", owner)
    write_json("validation/correction-delta-manifest.json", delta)
    write_json("validation/correction-staged-review.json", review)
    write_json("validation/correction-stage-candidate.json", candidate)
    return {
        "valid": candidate["valid"],
        "staged_paths": len(actual),
        "owner_entries": len(owner_entries),
        "owner_exclusions": len(CORRECTION_EXCLUSIONS),
        "delta_entries": len(delta_entries),
        "delta_exclusions": len(CORRECTION_EXCLUSIONS),
        "strict_json": json_count,
        "python_compiles": python_count,
        "privacy_confirmed_hits": len(confirmed),
    }


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != CORRECTION_PATHS:
        raise CorrectionError("correction staged allowlist changed")
    owner = closeout.strict_json(closeout.index_blob(CORRECTION_OWNER_MANIFEST), CORRECTION_OWNER_MANIFEST)
    delta = closeout.strict_json(closeout.index_blob(CORRECTION_DELTA_MANIFEST), CORRECTION_DELTA_MANIFEST)
    review = closeout.strict_json(closeout.index_blob(CORRECTION_REVIEW), CORRECTION_REVIEW)
    candidate = closeout.strict_json(closeout.index_blob(CORRECTION_CANDIDATE), CORRECTION_CANDIDATE)
    staged = set(actual)
    expected_owner = sorted(set(base_owner_paths()) | staged)
    owner_covered = sorted([row["path"] for row in owner["entries"]] + owner["declared_self_exclusions"])
    delta_covered = sorted([row["path"] for row in delta["entries"]] + delta["declared_self_exclusions"])
    if owner_covered != expected_owner or delta_covered != actual:
        raise CorrectionError("correction manifest coverage mismatch")
    for manifest in (owner, delta):
        for row in manifest["entries"]:
            if row["path"] in staged:
                raw = closeout.index_blob(row["path"])
                oid = closeout.index_oid(row["path"])
            else:
                raw = closeout.commit_blob(BASE_FINAL, row["path"])
                oid = closeout.commit_oid(BASE_FINAL, row["path"])
            if oid != row["git_blob"] or closeout.sha256(raw) != row["sha256"] or len(raw) != row["size"]:
                raise CorrectionError(f"correction manifest mismatch: {row['path']}")
    if not (owner["coverage_valid"] and delta["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise CorrectionError("one correction receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "owner_entries": owner["entry_count"],
        "owner_exclusions": owner["declared_self_exclusion_count"],
        "delta_entries": delta["entry_count"],
        "delta_exclusions": delta["declared_self_exclusion_count"],
        "strict_json": review["strict_json_count"],
        "python_compiles": review["python_compile_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
    elif args.write_staged_review:
        result = write_staged_review()
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
