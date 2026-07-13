#!/usr/bin/env python3
"""Standard-library-only verifier for the bounded v642-v2 evidence crosscheck."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "pass": bool(condition), "detail": detail})

    required = [
        "x1-proposals.json",
        "sources/source-ledger.json",
        "x2-proposal-ledger.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "phase-truth.json",
        "reproduction/semantic-normalization-manifest.json",
        "reproduction/cross-owner-lineage-replay.json",
        "reproduction/independent-team-gap.json",
        "physics/canonical-equation-ast.json",
        "physics/conservation-stability-jacobian-witness.json",
        "empirical/null-baseline-readiness.json",
        "thos/real-arm-execution-gate.json",
        "freed-id/production-assurance-gate.json",
        "cbr/legal-cultural-authority-gate.json",
        "security/recovery-resource-receipt.json",
        "thermo-psyche/classification-receipt.json",
        "stage20/terminal-verdict.json",
        "validation/execution-negative-log.json",
    ]
    missing = [rel for rel in required if not (phase / rel).is_file()]
    check("required minimal artifacts present", not missing, missing)
    if missing:
        issues = [row for row in checks if not row["pass"]]
        return {
            "schema": "ghc.family.evidence-crosscheck-minimal-verifier.v1",
            "runtime": "Python standard library only",
            "valid": False,
            "check_count": len(checks),
            "pass_count": len(checks) - len(issues),
            "issue_count": len(issues),
            "issues": issues,
            "checks": checks,
        }

    x1 = load(phase / "x1-proposals.json")
    sources = load(phase / "sources/source-ledger.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    truth = load(phase / "phase-truth.json")
    manifest = load(phase / "reproduction/semantic-normalization-manifest.json")
    replay = load(phase / "reproduction/cross-owner-lineage-replay.json")
    independent = load(phase / "reproduction/independent-team-gap.json")
    ast = load(phase / "physics/canonical-equation-ast.json")
    jacobian = load(phase / "physics/conservation-stability-jacobian-witness.json")
    empirical = load(phase / "empirical/null-baseline-readiness.json")
    thos = load(phase / "thos/real-arm-execution-gate.json")
    freed = load(phase / "freed-id/production-assurance-gate.json")
    cbr = load(phase / "cbr/legal-cultural-authority-gate.json")
    security = load(phase / "security/recovery-resource-receipt.json")
    thermo = load(phase / "thermo-psyche/classification-receipt.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
    execution_negatives = load(phase / "validation/execution-negative-log.json")

    check("ten frozen proposals", x1["proposal_count"] == len(x1["proposals"]) == 10)
    check("four exact truth labels", x1["outcome_classes"] == ["completed", "represented", "open_gap", "exact_gate"])
    check("expected labels are not outcomes", x1["expected_counts_are_results"] is False)
    check("ten observed proposal outcomes", x2["proposal_count"] == len(x2["proposals"]) == 10)
    check("outcome distribution exact", x2["disposition_counts"] == EXPECTED)
    check("expected and observed fields retained", all({"expected_disposition", "observed_disposition"} <= set(row) for row in x2["proposals"]))
    check("source ledger has 38 pins", sources["source_count"] == len(sources["sources"]) == 38)
    check("source status counts preserved", Counter(row["status_class"] for row in sources["sources"]) == Counter({"current": 20, "stable": 14, "draft": 3, "watch": 1}))
    check("66 negatives retained", negatives["negative_count"] == len(negatives["negatives"]) == 66 and all(row["retained"] for row in negatives["negatives"]))
    check("negative inheritance exact", negatives["inherited_count"] == 46 and negatives["new_count"] == 20 and negatives["erasure_permitted"] is False)
    check("execution failures retained", execution_negatives["negative_count"] == 6 and all(row["preserved"] for row in execution_negatives["negatives"]))
    check("five open gaps and six exact gates", gates["open_gap_count"] == 5 and gates["exact_gate_count"] == 6)
    check("no gate silently closed", gates["silently_closed"] == 0 and all(row["state"] in {"open", "deferred"} for row in gates["gates"]))
    check("typed physics remains structural", ast["model_class"] == "typed scalar-tensor EFT research scaffold" and not any(eq["empirically_confirmed"] for eq in ast["equations"]))
    check("Jacobian does not establish empirical identifiability", jacobian["structural_observability_only"] is True and jacobian["empirical_identifiability"] is False)
    check("zero-row empirical boundary", empirical["parsed_measurement_rows"] == empirical["likelihoods_executed"] == empirical["fits_executed"] == 0 and empirical["readiness_is_fit"] is False)
    check("THOS has zero real arms", thos["real_arm_runs"] == 0 and not any(thos[key] for key in ["superiority_established", "agi", "asi", "consciousness", "personhood"]))
    check("Freed production evidence absent", all(freed[key] == 0 for key in ["real_keys", "real_proofs", "live_resolvers", "live_status_services", "interoperability_partners", "independent_security_reviews"]) and freed["cryptographic_assurance"] is False)
    check("CBR authority remains exact-gated", cbr["state"] == "exact_gate" and not any(cbr[key] for key in ["affected_party_authority_present", "maori_authority_present", "cultural_ratification_present", "competent_legal_authority_present", "enacted_law"]))
    check("security scope remains bounded", security["exhaustive_security"] is False and security["host_security_changed"] is False and security["elevation"] is False)
    check("thermo psyche claims remain false", not any(thermo[key] for key in ["fundamental_law_established", "consciousness_tensor", "consciousness", "personhood"]))
    snapshot_ok = x2["snapshot_state"] == "verified" and replay["cross_owner_internal_repeatability"] == "verified_bounded"
    check("snapshot state acceptable", snapshot_ok or allow_pending_snapshot, x2["snapshot_state"])
    check("independent-team gap remains open", independent["independent_team_present"] is False and replay["independent_team_reproduction"] is False and truth["independent_team_gap"] == "open")
    check("terminal verdict remains not ready", terminal["verdict"] == truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and terminal["deployment_authorized"] is False)
    check("all protected claims false", not any(truth["protected_claims"].values()))

    mismatches = [
        rel for rel, digest in manifest["hashes"].items()
        if not (phase / rel).is_file() or normalized_sha256(phase / rel) != digest
    ]
    check("normalized manifest hashes match", not mismatches, mismatches)
    aggregate = hashlib.sha256(
        "".join(f"{rel}:{manifest['hashes'][rel]}\n" for rel in sorted(manifest["hashes"])).encode("utf-8")
    ).hexdigest()
    check("manifest aggregate matches", aggregate == manifest["aggregate_sha256"])
    check("manifest claim is bounded", manifest["absolute_paths_required"] is False and manifest["independent_team_reproduction"] is False)

    issues = [row for row in checks if not row["pass"]]
    return {
        "schema": "ghc.family.evidence-crosscheck-minimal-verifier.v1",
        "runtime": "Python standard library only",
        "valid": not issues,
        "check_count": len(checks),
        "pass_count": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "summary": {
            "proposal_count": 10,
            "disposition_counts": EXPECTED,
            "retained_negative_count": 66,
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
