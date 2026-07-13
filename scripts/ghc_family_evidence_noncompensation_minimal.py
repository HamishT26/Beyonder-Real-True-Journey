#!/usr/bin/env python3
"""Standard-library-only minimal verifier for bounded v642-v5 evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
VECTOR_PATHS = [
    "provenance/assertion-granularity-vectors.json",
    "physics/constraint-propagation-vectors.json",
    "empirical/prior-data-conflict-vectors.json",
    "thos/inter-rater-mutation-vectors.json",
    "freed-id/redirect-metadata-leak-vectors.json",
    "cbr/minority-report-vectors.json",
    "security/recovery-mutation-vectors.json",
    "reproduction/clock-locale-order-vectors.json",
    "thermo-psyche/analogy-admissibility-vectors.json",
    "stage20/score-laundering-vectors.json",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "pass": bool(condition), "detail": detail})

    required = [
        "x1-proposals.json",
        "provenance/frozen-chain-proposal-index.json",
        "sources/source-ledger.json",
        "x2-proposal-ledger.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "phase-truth.json",
        "reproduction/manifest.json",
        "reproduction/clean-snapshot-validation.json",
        "physics/well-posedness-claim-boundary.json",
        "empirical/zero-row-inference-lock.json",
        "thos/real-rater-arm-gap.json",
        "freed-id/production-resolution-boundary.json",
        "cbr/dissent-recusal-authority-gate.json",
        "reproduction/hermeticity-gap.json",
        "thermo-psyche/category-barrier.json",
        "stage20/terminal-verdict.json",
        "validation/execution-negative-log.json",
        *VECTOR_PATHS,
    ]
    missing = [rel for rel in required if not (phase / rel).is_file()]
    check("required minimal artifacts present", not missing, missing)
    if missing:
        issues = [row for row in checks if not row["pass"]]
        return {
            "schema": "ghc.family.evidence-noncompensation-minimal-verifier.v1",
            "runtime": "Python standard library only",
            "valid": False,
            "check_count": len(checks),
            "pass_count": len(checks) - len(issues),
            "issue_count": len(issues),
            "issues": issues,
            "checks": checks,
        }

    x1 = load(phase / "x1-proposals.json")
    chain = load(phase / "provenance/frozen-chain-proposal-index.json")
    sources = load(phase / "sources/source-ledger.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    truth = load(phase / "phase-truth.json")
    manifest = load(phase / "reproduction/manifest.json")
    snapshot = load(phase / "reproduction/clean-snapshot-validation.json")
    physics = load(phase / "physics/well-posedness-claim-boundary.json")
    empirical = load(phase / "empirical/zero-row-inference-lock.json")
    thos = load(phase / "thos/real-rater-arm-gap.json")
    freed = load(phase / "freed-id/production-resolution-boundary.json")
    cbr = load(phase / "cbr/dissent-recusal-authority-gate.json")
    hermetic = load(phase / "reproduction/hermeticity-gap.json")
    category = load(phase / "thermo-psyche/category-barrier.json")
    terminal = load(phase / "stage20/terminal-verdict.json")

    check("ten frozen proposals", x1["proposal_count"] == len(x1["proposals"]) == 10)
    check("110 predecessors audited", x1["prior_frozen_proposal_count"] == 110)
    check("120 proposal chain unique", chain["proposal_count"] == len(chain["records"]) == 120 and len({r["title"] for r in chain["records"]}) == 120)
    check("four exact outcome labels", set(x1["outcome_classes"]) == set(EXPECTED))
    check("expected labels are not observations", x1["expected_counts_are_results"] is False)
    check("62 effective sources", sources["effective_source_count"] == 62 and sum(sources["effective_status_counts"].values()) == 62)
    check("source states remain visible", set(sources["effective_status_counts"]) == {"current", "stable", "draft", "watch"})
    check("ten x2 outcomes", x2["proposal_count"] == len(x2["proposals"]) == 10)
    check("outcome distribution exact", x2["disposition_counts"] == EXPECTED)
    check("every proposal executed to evidence boundary", x2["all_executed_as_far_as_evidence_permits"] is True)

    vector_negatives: list[str] = []
    for rel in VECTOR_PATHS:
        rows = load(phase / rel)["vectors"]
        check(f"three vectors and expected results: {rel}", len(rows) == 3 and all(row["matches_expected"] for row in rows))
        ids = [row["negative_id"] for row in rows if "negative_id" in row]
        check(f"two retained negative vectors: {rel}", len(ids) == 2)
        vector_negatives.extend(ids)
    check("twenty distinct vector negatives", len(vector_negatives) == len(set(vector_negatives)) == 20)

    negative_ids = [row["negative_id"] for row in negatives["negatives"]]
    check("120 inherited negatives retained", negatives["inherited_count"] == 120 and negative_ids[:120] == [row["negative_id"] for row in negatives["negatives"][:120]])
    check("at least 25 local negatives retained", negatives["new_count"] >= 25 and negatives["negative_count"] >= 145)
    check("negative register exact and unique", negatives["negative_count"] == len(negative_ids) == len(set(negative_ids)))
    check("retention invariant", negatives["all_retained"] is True and negatives["erasure_permitted"] is False and all(row["retained"] for row in negatives["negatives"]))
    check("x1 and vector negatives present", all(f"V6425-X1-N{n:02d}" in negative_ids for n in range(1, 6)) and all(f"V6425-N{n:02d}" in negative_ids for n in range(1, 21)))

    check("five open gaps and six exact gates", gates["open_gap_count"] == 5 and gates["exact_gate_count"] == 6)
    check("no gate silently closed", gates["silently_closed"] == 0 and Counter(row["gate_class"] for row in gates["gates"]) == {"open_gap": 5, "exact_gate": 6})
    check("all gates remain open or deferred", all(row["state"] in {"open", "deferred"} for row in gates["gates"]))

    check("GMUT promotion remains false", not any(physics[key] for key in ["gmut_well_posedness_established", "empirical_confirmation", "detected_force", "unique_prediction", "theory_of_everything", "proof_or_canon"]))
    check("empirical adapter has zero rows and fits", empirical["real_measurement_rows"] == empirical["likelihood_executions"] == empirical["fits"] == 0 and empirical["promotion_allowed"] is False)
    check("THOS real evidence remains absent", thos["real_raters"] == thos["blind_matched_budget_real_arms"] == thos["independent_reviews"] == 0 and not any(thos[key] for key in ["real_thos_superiority", "agi", "asi", "consciousness", "personhood"]))
    check("Freed ID production evidence remains absent", sum(freed[key] for key in ["real_keys", "real_proofs", "live_resolvers_or_status_services", "interoperability_partners", "independent_security_reviews", "independent_privacy_reviews", "trust_governance_authorities"]) == 0 and freed["production_assurance"] is False)
    check("CBR and Maori authority remain exact-gated", cbr["technical_artifact_can_grant_maori_authority"] is False and cbr["authorized_participants_present"] == 0)
    check("independent team gap remains open", hermetic["independent_team_count"] == 0 and hermetic["independent_reproduction_established"] is False)
    check("thermo-psyche claims remain false", not any(category[key] for key in ["fundamental_thermo_psyche_law", "consciousness", "personhood", "empirical_confirmation"]))
    check("terminal decision is noncompensatory defer", terminal["decision"] == "defer" and terminal["verdict"] == "NOT_READY_FOR_STAGE_20" and terminal["weighted_compensation_used"] is False)
    check("all protected claims false", all(value is False for value in truth["protected_claims"].values()))
    check("route and final verdict fail closed", truth["route_state"] == "NO_SUCCESSOR_AUTHORIZED" and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")

    records = manifest["files"]
    mismatches = [row["path"] for row in records if not (phase / row["path"]).is_file() or digest(phase / row["path"]) != row["normalized_sha256"]]
    check("manifest paths unique", manifest["file_count"] == len(records) == len({row["path"] for row in records}))
    check("normalized manifest hashes match", not mismatches, mismatches)
    check("manifest claim is bounded", manifest["same_owner_repeatability_only"] is True and manifest["independent_reproduction_established"] is False)

    snapshot_ok = snapshot["state"] == "verified" and snapshot["snapshot_count"] >= 2 and snapshot["hash_mismatches"] == 0 and x2["snapshot_state"] == "verified"
    check("snapshot state acceptable", snapshot_ok or (allow_pending_snapshot and snapshot["state"] in {"pending", "verified"}), snapshot["state"])
    check("snapshot is not independent reproduction", snapshot["independent_reproduction_established"] is False)

    issues = [row for row in checks if not row["pass"]]
    return {
        "schema": "ghc.family.evidence-noncompensation-minimal-verifier.v1",
        "runtime": "Python standard library only",
        "valid": not issues,
        "check_count": len(checks),
        "pass_count": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "summary": {
            "proposal_count": 10,
            "disposition_counts": EXPECTED,
            "retained_negative_count": negatives["negative_count"],
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "checks": checks,
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    report = verify(phase, args.allow_pending_snapshot)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else phase / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    raise SystemExit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()
