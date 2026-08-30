#!/usr/bin/env python3
"""Build the additive Sylven Arc v678-v6 canonical-validator correction1 packet."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


FIRST_FINAL = "ea27f954b8636f167c83b964c0ba5ad15301ea1e"


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
    if git(repo, "rev-parse", "HEAD") != FIRST_FINAL:
        raise SystemExit("correction1 must be the additive child of the immutable first final")
    tracked = set(git(repo, "diff", "--name-only").splitlines())
    if tracked - {"scripts/validate_ghc_family_sylven_arc_v678_v6_final.py"} or git(repo, "diff", "--cached", "--name-only"):
        raise SystemExit("only the correction-scoped validator edit may differ from the immutable first final")
    root = repo / "docs/sylven-arc/v678-v6/correction1"
    overlay = {
        "effective_negatives": 47283, "effective_methods": 45392,
        "retained_failed_witnesses": 18944, "bounded_passing_witnesses": 29533,
        "open_gaps": 410, "exact_gates": 401,
    }
    write_json(root / "correction-truth.json", {
        "schema": "ghc-family-additive-correction-truth/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "first_final": FIRST_FINAL, "corrected_final": "BOUND_AT_COMMIT", "parent": FIRST_FINAL,
        "reason": "pre-canonical static audit found that the validator's bounded AST checker would reject its own safe compile-only syntax check",
        "failed_canonical_invocation_created": False, "canonical_latch_created": False, "canonical_receipt_created": False,
        "correction": [
            "remove compile from the forbidden dynamic-call names while retaining eval, exec, and __import__ refusals",
            "bind immutable first-final manifests at the first-final Git tree",
            "add correction1 delta and corrected-owner manifests",
            "require four direct single-parent Sylven commits and zero merges",
        ],
        "first_final_history_rewritten": False, "source_evidence_replayed": False,
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "method_flow_overlay": overlay,
    })
    write_json(root / "method-flow-overlay.json", {
        "schema": "ghc-family-method-flow-overlay/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "base": {
            "effective_negatives": 47282, "effective_methods": 45390,
            "retained_failed_witnesses": 18943, "bounded_passing_witnesses": 29532,
            "open_gaps": 410, "exact_gates": 401,
        },
        "overlay": overlay, "new_failed_witnesses": 1, "new_passing_witnesses": 1, "new_methods": 2,
        "methods": [
            {"method_id": "SA6786-CORR1-N001", "status": "retained_failed_witness", "summary": "Pre-canonical audit showed the validator would flag its own safe compile-only check; no canonical invocation or latch occurred."},
            {"method_id": "SA6786-CORR1-R001", "status": "bounded_passing_recovery", "summary": "The direct-child correction retained dynamic eval, exec, and import refusals while allowing the explicit compile-only syntax check and adding lifecycle-correct correction manifests."},
        ],
        "failure_erasure_forbidden": True,
    })
    write_json(root / "canonical-preflight-state.json", {
        "schema": "ghc-family-canonical-preflight-state/v1", "owner": "Sylven Arc", "phase": "v678-v6",
        "first_final_preflight": "PASS_BEFORE_STATIC_SELF-AUDIT", "static_self_audit": "FAILED_CLOSED_BEFORE_CANONICAL",
        "canonical_invocation_count": 0, "canonical_success_count": 0, "canonical_replay_count": 0,
        "receipt_absent": True, "latch_absent": True, "correction_required": True,
    })
    write_text(root / "receipt-contract-correction.md", f"""# Sylven Arc v678-v6 correction1 receipt-contract correction

The immutable first final `{FIRST_FINAL}` remains preserved. Its repository packet was internally consistent, pushed, clean, fresh-live equal, and its latch preflight passed. Before invoking the exclusive canonical aggregate, a static audit found that the validator classified the Python built-in `compile` as a forbidden dynamic call while also using `compile(source, path, "exec")` only to syntax-check exact committed owner source. This would have made the canonical fail on its own validator rather than on unsafe owner code.

No canonical command was invoked. No receipt or latch was created. Correction1 removes only `compile` from that forbidden-name set; `eval`, `exec`, and `__import__` remain forbidden. The checker still parses every changed owner Python file, compiles exact source without executing it, and rejects destructive `rmtree` or `unlink` calls. The correction also binds the historical first-final manifests to the first-final tree and gives the corrected head its own delta, owner, and content-seal contracts.

The corrected final must be the direct child of the immutable first final. Source to corrected final must contain four direct single-parent Sylven commits, zero merges, and one corrected-final parent. The repository remains `PREPARED_NOT_SENT`, the terminal verdict remains `NOT_READY_FOR_STAGE_20`, and all scientific, empirical, professional, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, consciousness, personhood, Theory-of-Everything, proof, canon, and Stage 20 boundaries remain unchanged.
""")
    return {"status": "CORRECTION1_BUILT_PREPARED_NOT_SENT", "first_final": FIRST_FINAL, "overlay": overlay}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(build(args.repo.resolve()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
