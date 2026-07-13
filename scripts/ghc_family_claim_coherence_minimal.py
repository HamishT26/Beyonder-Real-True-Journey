#!/usr/bin/env python3
"""Minimal standard-library verifier for a GHC Family claim-coherence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    phase = phase.resolve()
    passed: list[str] = []
    issues: list[str] = []

    def check(value: bool, label: str) -> None:
        (passed if value else issues).append(label)

    required = [
        "x1-proposals.json",
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "provenance/frozen-chain-proposal-index.json",
        "workflow/publication-barrier-receipt.json",
        "reproduction/quarantine-recovery-receipt.json",
        "physics/identifiability-claim-boundary.json",
        "empirical/real-row-promotion-lock.json",
        "thos/real-arm-gap.json",
        "freed-id/production-assurance-boundary.json",
        "cbr/maori-data-governance-gate.json",
        "reproduction/independent-team-gap.json",
        "accessibility/manual-evaluation-reservation.json",
        "stage20/terminal-verdict.json",
        "reproduction/manifest.json",
        "reproduction/clean-snapshot-validation.json",
    ]
    for rel in required:
        check((phase / rel).is_file(), f"required:{rel}")
    if issues:
        return {
            "schema": "ghc.family.claim-coherence-minimal.v1",
            "valid": False,
            "checks_passed": len(passed),
            "checks_total": len(passed) + len(issues),
            "issues": issues,
        }

    x1 = load(phase / "x1-proposals.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    chain = load(phase / "provenance/frozen-chain-proposal-index.json")
    manifest = load(phase / "reproduction/manifest.json")
    snapshot = load(phase / "reproduction/clean-snapshot-validation.json")

    check(x1["proposal_count"] == len(x1["proposals"]) == 10, "x1-ten")
    check(x2["proposal_count"] == len(x2["proposals"]) == 10, "x2-ten")
    check(x2["disposition_counts"] == EXPECTED, "x2-distribution")
    check(truth["disposition_counts"] == EXPECTED, "truth-distribution")
    check(all(row["expected_disposition"] == row["observed_disposition"] for row in x2["proposals"]), "expected-observed")
    check(all(row["executed_as_far_as_evidence_permits"] for row in x2["proposals"]), "evidence-permitted")
    check(chain["proposal_count"] == len(chain["records"]) == 110, "chain-110")
    check(len({row["proposal_id"] for row in chain["records"]}) == 110, "chain-ids")
    check(len({row["title"] for row in chain["records"]}) == 110, "chain-titles")
    check(negatives["inherited_count"] == 96, "inherited-negatives")
    check(negatives["negative_count"] == len(negatives["negatives"]), "negative-count")
    check(negatives["negative_count"] >= 120, "negative-floor")
    check(len({row["negative_id"] for row in negatives["negatives"]}) == negatives["negative_count"], "negative-ids")
    check(negatives["all_retained"] and not negatives["erasure_permitted"], "negative-retention")
    check(gates["open_gap_count"] == 5, "open-gaps")
    check(gates["exact_gate_count"] == 6, "exact-gates")
    check(gates["silently_closed"] == 0, "no-silent-gates")
    check(truth["retained_negative_count"] == negatives["negative_count"], "truth-negative-count")
    check(truth["open_gap_count"] == 5 and truth["exact_gate_count"] == 6, "truth-gates")
    check(all(value is False for value in truth["protected_claims"].values()), "protected-false")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "terminal-not-ready")
    check("Māori authority" in truth["maori_authority_boundary"], "maori-boundary")

    summary_files = [
        "workflow/publication-barrier-receipt.json",
        "reproduction/quarantine-recovery-receipt.json",
        "physics/identifiability-claim-boundary.json",
        "empirical/real-row-promotion-lock.json",
        "accessibility/manual-evaluation-reservation.json",
        "stage20/terminal-verdict.json",
    ]
    for rel in summary_files:
        check(load(phase / rel).get("all_expected") is True, f"vectors:{rel}")
    check(load(phase / "empirical/real-row-promotion-lock.json")["real_measurement_rows"] == 0, "zero-real-rows")
    check(load(phase / "thos/real-arm-gap.json")["blind_matched_budget_real_arms"] == 0, "zero-thos-arms")
    freed = load(phase / "freed-id/production-assurance-boundary.json")
    check(freed["real_keys"] == freed["real_proofs"] == 0, "zero-real-crypto")
    check(load(phase / "cbr/maori-data-governance-gate.json")["authorized_participants_present"] == 0, "zero-authorized-participants")
    check(load(phase / "reproduction/independent-team-gap.json")["independent_team_count"] == 0, "zero-independent-team")
    check(load(phase / "accessibility/manual-evaluation-reservation.json")["complete_accessibility_conformance"] is False, "a11y-bounded")

    check(manifest["file_count"] == len(manifest["files"]), "manifest-count")
    for row in manifest["files"]:
        target = phase / row["path"]
        check(target.is_file() and digest(target) == row["normalized_sha256"], f"manifest:{row['path']}")
    if allow_pending_snapshot:
        check(snapshot["state"] in {"pending", "verified"}, "snapshot-allowed")
    else:
        check(snapshot["state"] == "verified", "snapshot-verified")
        check(snapshot["snapshot_count"] >= 2, "snapshot-count")
    check(snapshot["independent_reproduction_established"] is False, "snapshot-not-independent")

    return {
        "schema": "ghc.family.claim-coherence-minimal.v1",
        "valid": not issues,
        "checks_passed": len(passed),
        "checks_total": len(passed) + len(issues),
        "issues": issues,
        "proposal_count": 10,
        "retained_negative_count": negatives["negative_count"],
        "manifest_files": manifest["file_count"],
        "snapshot_state": snapshot["state"],
        "terminal_verdict": truth["terminal_verdict"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.phase_dir, args.allow_pending_snapshot)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
