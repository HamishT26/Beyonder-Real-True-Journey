#!/usr/bin/env python3
"""Build Sylven Arc v678-v6 additive correction2 after static canonical audit."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


BASE = "79c42c6158c9799344e16a9ed5fc49092422b698"
ALLOWED_TRACKED = {
    "scripts/ghc_family_sylven_arc_v678_v6_flashcards.py",
    "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py",
}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, check=False, capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def build(repo: Path) -> dict[str, Any]:
    if git(repo, "rev-parse", "HEAD") != BASE:
        raise SystemExit("correction2 must be the additive child of correction1")
    tracked = set(git(repo, "diff", "--name-only").splitlines())
    if tracked - ALLOWED_TRACKED or git(repo, "diff", "--cached", "--name-only"):
        raise SystemExit("correction2 tracked delta exceeds the flashcard import and validator contracts")
    root = repo / "docs/sylven-arc/v678-v6/correction2"
    overlay = {
        "effective_negatives": 47291, "effective_methods": 45410,
        "retained_failed_witnesses": 18952, "bounded_passing_witnesses": 29543,
        "open_gaps": 410, "exact_gates": 401,
    }
    write_json(root / "correction-truth.json", {
        "schema": "ghc-family-additive-correction-truth/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "correction1": BASE, "corrected_final": "BOUND_AT_COMMIT", "parent": BASE,
        "failed_static_audit": {
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "canonical_invoked": False,
            "privacy_confirmed_or_unresolved_candidates": 4,
            "privacy_root_cause": "two manifest scripts containing scanner definitions were absent from the exact adjudication set",
            "code_findings": 1,
            "code_root_cause": "the flashcard builder used dynamic __import__ only to reach Counter",
            "immutable_manifest_replays_passed": 3, "file_and_word_caps_passed": True,
        },
        "corrections": [
            "replace dynamic __import__ with an explicit collections.Counter import",
            "adjudicate the exact x1, correction1, and correction2 manifest scanner-definition files",
            "bind correction1 manifests to the correction1 Git tree and add correction2 manifests",
            "require five direct single-parent Sylven commits and zero merges",
        ],
        "canonical_invocation_count": 0, "canonical_success_count": 0, "canonical_replay_count": 0,
        "receipt_absent": True, "latch_absent": True, "history_rewritten": False,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "method_flow_overlay": overlay,
    })
    write_json(root / "method-flow-overlay.json", {
        "schema": "ghc-family-method-flow-overlay/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "base": {
            "effective_negatives": 47283, "effective_methods": 45392,
            "retained_failed_witnesses": 18944, "bounded_passing_witnesses": 29533,
            "open_gaps": 410, "exact_gates": 401,
        },
        "overlay": overlay, "new_failed_witnesses": 8, "new_passing_witnesses": 10, "new_methods": 18,
        "methods": [
            {"method_id": "SA6786-CORR2-N001", "status": "retained_failed_witness", "summary": "The corrected-head non-canonical static aggregate found incomplete scanner-definition adjudication and one forbidden dynamic import; canonical invocation remained zero."},
            {"method_id": "SA6786-CORR2-R001", "status": "bounded_passing_recovery", "summary": "Exact scanner-definition files were added to adjudication while payload matching remained fail-closed."},
            {"method_id": "SA6786-CORR2-R002", "status": "bounded_passing_recovery", "summary": "The flashcard builder now imports Counter explicitly and no longer uses dynamic __import__."},
            {"method_id": "SA6786-CORR2-N002", "status": "retained_failed_witness", "summary": "A read-only ripgrep inspection expression was rejected as an unclosed regular-expression group before any file inspection occurred."},
            {"method_id": "SA6786-CORR2-R003", "status": "bounded_passing_recovery", "summary": "The same bounded inspection succeeded using separately supplied literal patterns and changed no repository content."},
            {"method_id": "SA6786-CORR2-N003", "status": "retained_failed_witness", "summary": "The first correction2 manifest build failed closed because the pre-canonical state filename differed between its producer and seal target."},
            {"method_id": "SA6786-CORR2-R004", "status": "bounded_passing_recovery", "summary": "The producer now emits the single canonical-preflight-state filename required by the seal; only the failed manifest-build dependency is rerun."},
            {"method_id": "SA6786-CORR2-N004", "status": "retained_failed_witness", "summary": "The next isolated manifest build failed closed because the seal targeted a nonexistent receipt-contract document instead of the generated static-audit evidence file."},
            {"method_id": "SA6786-CORR2-R005", "status": "bounded_passing_recovery", "summary": "The seal now targets the existing static-audit-correction document; only the manifest-build dependency is rerun."},
            {"method_id": "SA6786-CORR2-N005", "status": "retained_failed_witness", "summary": "The correction2 test aggregate finished 6/8 because two assertions still encoded the earlier counts and superseded pre-canonical filename; the aggregate earns zero pass credit."},
            {"method_id": "SA6786-CORR2-R006", "status": "bounded_passing_recovery", "summary": "Only the failed Method Flow assertion is rerun against the complete retained correction2 counts."},
            {"method_id": "SA6786-CORR2-R007", "status": "bounded_passing_recovery", "summary": "Only the failed pre-canonical-state assertion is rerun against the canonical-preflight-state filename."},
            {"method_id": "SA6786-CORR2-N006", "status": "retained_failed_witness", "summary": "The first correction2 INDEX verifier crossed its display window and the wrapper exposed stdout only, losing the live session handle and final exit status; no pass is inferred."},
            {"method_id": "SA6786-CORR2-R008", "status": "bounded_passing_recovery", "summary": "After the original process ended, the exact INDEX verification is run once with session metadata retained until its final result is captured."},
            {"method_id": "SA6786-CORR2-N007", "status": "retained_failed_witness", "summary": "A correction2 regeneration attempt failed closed because the earlier correction files were still staged and the builder requires an unstaged bounded delta."},
            {"method_id": "SA6786-CORR2-R009", "status": "bounded_passing_recovery", "summary": "Only Sylven correction2 paths were unstaged without changing worktree bytes, restoring the builder precondition."},
            {"method_id": "SA6786-CORR2-N008", "status": "retained_failed_witness", "summary": "The count-only test then failed because the rejected builder had correctly left the generated Method Flow document at its previous version."},
            {"method_id": "SA6786-CORR2-R010", "status": "bounded_passing_recovery", "summary": "After successful regeneration, only that failed count assertion is rerun against the exact current overlay."},
        ],
        "failure_erasure_forbidden": True,
    })
    write_text(root / "static-audit-correction.md", f"""# Sylven Arc v678-v6 correction2 static-audit correction

Correction1 `{BASE}` remains immutable. A non-canonical static audit replayed the evidence, first-final, and correction1 manifests successfully and confirmed all file and word caps. It then failed closed for two independent reasons: the validator had not yet listed the x1 and correction1 manifest scripts as scanner-definition sources, and the flashcard builder used `__import__("collections")` solely to access `Counter`.

No canonical aggregate, receipt, or latch was invoked or created. Correction2 adds exact-file scanner adjudication for the manifest implementations and replaces dynamic import with `from collections import Counter`. Payload matches remain failures, and `eval`, `exec`, and `__import__` remain forbidden call sites in owner code. The validator now binds correction1 to its immutable tree and gives correction2 its own delta, corrected-owner, and content-seal layer.

A later read-only ripgrep inspection expression was rejected as an unclosed group before inspecting any file. The bounded recovery supplied each search pattern separately and succeeded without changing repository content. Both the failed method and its recovery remain explicit in Method Flow.

The first correction2 manifest build also failed closed because its seal expected `canonical-preflight-state.json` while the builder emitted `precanonical-state.json`. The producer now emits the exact seal-target name, and only that failed manifest-build dependency is rerun.

The next isolated manifest build failed closed on a second filename mismatch: the seal targeted a nonexistent receipt-contract document rather than the generated `static-audit-correction.md`. The seal now binds the actual static-audit evidence file.

The first correction2 test aggregate then completed 6/8. Its two stale assertions expected the earlier counts and the superseded `precanonical-state.json` filename. The aggregate remains zero-credit; only those two failed methods are rerun after the exact expectations are corrected.

The first correction2 INDEX verifier then crossed its display window while still running, and its stdout-only wrapper discarded the live session handle. The process was allowed to finish, but no status was inferred. A corrected wrapper retains session metadata and captures one complete rerun against the changed final staged target.

A subsequent regeneration attempt failed closed because the earlier correction delta remained staged. Only the Sylven-owned correction2 paths were unstaged, preserving every worktree byte. The count-only test run immediately after the rejected builder also failed against the correctly unchanged generated file; after regeneration, only that failed assertion is rerun.

The corrected final must be the direct child of correction1. Source to corrected final must contain exactly five direct single-parent Sylven commits and zero merges. The route remains `PREPARED_NOT_SENT`; scientific, empirical, participant, professional, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, consciousness, personhood, Theory-of-Everything, proof, canon, and Stage 20 gates remain unchanged.
""")
    write_json(root / "canonical-preflight-state.json", {
        "schema": "ghc-family-precanonical-state/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "canonical_invocation_count": 0, "receipt_absent": True, "latch_absent": True,
        "previous_static_audit": "FAILED_CLOSED", "correction2_prepared": True,
        "route_state": "PREPARED_NOT_SENT",
    })
    return {"status": "CORRECTION2_BUILT_PREPARED_NOT_SENT", "base": BASE, "overlay": overlay}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(build(args.repo.resolve()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
