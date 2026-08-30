#!/usr/bin/env python3
"""Build the additive Sylven Arc v678-v6 correction3 recovery packet."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


BASE = "706292a287ed36b892d97d80c9571e7a1d8b8ded"
FAILED_CANONICAL_SHA256 = "06e5b4d462ac51765d914e1f6e1d48d8831229dc24918daaee2eea97d63aa16e"
FAILED_CANONICAL_PAYLOAD_SHA256 = "67ac13794ac47b127adc998ee4389570063620f0c4a63cb75ca3608c782bb8ee"
ALLOWED_TRACKED = {
    "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py",
    "tests/test_ghc_family_sylven_arc_v678_v6_correction1.py",
    "tests/test_ghc_family_sylven_arc_v678_v6_correction2.py",
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
        raise SystemExit("correction3 must be the additive child of correction2")
    tracked = set(git(repo, "diff", "--name-only").splitlines())
    if tracked - ALLOWED_TRACKED or git(repo, "diff", "--cached", "--name-only"):
        raise SystemExit("correction3 tracked delta exceeds the exact failed-dependency repair")
    root = repo / "docs/sylven-arc/v678-v6/correction3"
    overlay = {
        "effective_negatives": 47293,
        "effective_methods": 45413,
        "retained_failed_witnesses": 18954,
        "bounded_passing_witnesses": 29544,
        "open_gaps": 410,
        "exact_gates": 401,
    }
    write_json(root / "correction-truth.json", {
        "schema": "ghc-family-additive-correction-truth/v1",
        "owner": "Sylven Arc",
        "phase": "v678-v6",
        "correction2": BASE,
        "corrected_final": "BOUND_AT_COMMIT",
        "parent": BASE,
        "failed_canonical": {
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "receipt_sha256": FAILED_CANONICAL_SHA256,
            "payload_sha256": FAILED_CANONICAL_PAYLOAD_SHA256,
            "invocation_count": 1,
            "success_count": 0,
            "replay_count": 0,
            "tests_passed": 40,
            "tests_total": 41,
            "failed_dependency": "correction1 immutable-lifecycle topology assertion",
        },
        "repair": {
            "scope": "bind correction1 and correction2 topology assertions to their exact immutable Git trees",
            "successful_canonical_components_replayed": False,
            "full_repository_suite_run": False,
            "history_rewritten": False,
        },
        "composite_state": "PENDING_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "method_flow_overlay": overlay,
    })
    write_json(root / "method-flow-overlay.json", {
        "schema": "ghc-family-method-flow-overlay/v1",
        "owner": "Sylven Arc",
        "phase": "v678-v6",
        "base": {
            "effective_negatives": 47291,
            "effective_methods": 45410,
            "retained_failed_witnesses": 18952,
            "bounded_passing_witnesses": 29543,
            "open_gaps": 410,
            "exact_gates": 401,
        },
        "overlay": overlay,
        "new_failed_witnesses": 2,
        "new_passing_witnesses": 1,
        "new_methods": 3,
        "methods": [
            {"method_id": "SA6786-CORR3-N001", "status": "retained_failed_witness", "summary": "The sole exact-final canonical aggregate completed 40/41 tests and remains invalid with zero canonical-success credit; it is never replayed."},
            {"method_id": "SA6786-CORR3-N002", "status": "retained_failed_witness", "summary": "The first multi-hunk validator patch was atomically rejected because one live manifest-command line differed from the expected context."},
            {"method_id": "SA6786-CORR3-R001", "status": "bounded_passing_recovery", "summary": "Live bounded sections were reread and the same correction was applied as exact-context hunks without partial history mutation."},
        ],
        "failure_erasure_forbidden": True,
    })
    write_json(root / "composite-preflight-state.json", {
        "schema": "ghc-family-dependency-corrected-composite-preflight/v1",
        "owner": "Sylven Arc",
        "phase": "v678-v6",
        "failed_canonical_receipt_sha256": FAILED_CANONICAL_SHA256,
        "failed_canonical_latch_state": "FAILED",
        "canonical_replay_count": 0,
        "composite_receipt_absent_at_build": True,
        "composite_latch_absent_at_build": True,
        "route_state": "PREPARED_NOT_SENT",
    })
    write_text(root / "dependency-recovery-plan.md", f"""# Sylven Arc v678-v6 dependency-corrected recovery

Correction2 `{BASE}` remains immutable. The single attributable canonical aggregate is retained as invalid at zero canonical-success credit under receipt SHA-256 `{FAILED_CANONICAL_SHA256}`. It completed 40 passing test observations and one failed historical topology assertion; every non-test component passed. The canonical aggregate and its successful components are not replayed.

Correction3 binds correction1 and correction2 topology assertions to the exact immutable Git trees they describe. The dependency-corrected composite may run only the failed correction1 test, the one correction2 topology test affected by the new current validator, and the new correction3 tests. Exact-head manifests, JSON, privacy, bounded code, caps, topology, clean state, typed divergence, and fresh-live equality are target-dependent and must be reevaluated for the additive corrected head.

The result, if valid, is named `VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_FAILED_CANONICAL_CREDIT`. It never becomes canonical success, independent reproduction, empirical or participant evidence, professional or production authority, complete privacy or accessibility assurance, legal or cultural ratification, Māori authority, Theory-of-Everything proof, canon, or Stage 20 authority. The route remains `PREPARED_NOT_SENT` until the separate guarded live-delivery gate.
""")
    return {"status": "CORRECTION3_BUILT_PREPARED_NOT_SENT", "base": BASE, "overlay": overlay}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(build(args.repo.resolve()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
