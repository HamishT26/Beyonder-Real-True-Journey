#!/usr/bin/env python3
"""Standard-library minimal verifier for the v642-v3 round-robin packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}


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
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "workflow/project-context-capability-register.json",
        "workflow/six-seat-round-robin.json",
        "security/effective-authority-receipt.json",
        "physics/gmut-claim-boundary.json",
        "empirical/calibration-claim-boundary.json",
        "thos/real-arm-gap.json",
        "freed-id/production-boundary.json",
        "cbr/authority-legitimacy-gate.json",
        "thermo-psyche/law-claim-boundary.json",
        "stage20/independent-reproduction-reservation.json",
        "stage20/terminal-verdict.json",
        "reproduction/semantic-normalization-manifest.json",
        "reproduction/environment-perturbation-receipt.json",
    ]
    missing = [rel for rel in required if not (phase / rel).is_file()]
    check("required minimal artifacts present", not missing, missing)
    if missing:
        issues = [row for row in checks if not row["pass"]]
        return {
            "schema": "ghc.family.project-round-robin-minimal.v1",
            "valid": False,
            "check_count": len(checks),
            "pass_count": len(checks) - len(issues),
            "issue_count": len(issues),
            "issues": issues,
            "checks": checks,
        }

    x1 = load(phase / "x1-proposals.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    context = load(phase / "workflow/project-context-capability-register.json")
    schedule = load(phase / "workflow/six-seat-round-robin.json")
    authority = load(phase / "security/effective-authority-receipt.json")
    gmut = load(phase / "physics/gmut-claim-boundary.json")
    calibration = load(phase / "empirical/calibration-claim-boundary.json")
    thos = load(phase / "thos/real-arm-gap.json")
    freed = load(phase / "freed-id/production-boundary.json")
    cbr = load(phase / "cbr/authority-legitimacy-gate.json")
    thermo = load(phase / "thermo-psyche/law-claim-boundary.json")
    reservation = load(phase / "stage20/independent-reproduction-reservation.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
    manifest = load(phase / "reproduction/semantic-normalization-manifest.json")
    perturb = load(phase / "reproduction/environment-perturbation-receipt.json")

    check("ten x1 proposals", x1["proposal_count"] == len(x1["proposals"]) == 10)
    check("x1 expectations not results", x1["expected_counts_are_results"] is False)
    check("ten x2 outcomes", x2["proposal_count"] == len(x2["proposals"]) == 10)
    check("outcome distribution exact", x2["disposition_counts"] == EXPECTED)
    check("all outcomes evidence-bounded", all(row["executed_as_far_as_evidence_permits"] for row in x2["proposals"]))
    check("96 negatives retained", negatives["negative_count"] == len(negatives["negatives"]) == 96)
    check("negative inheritance exact", negatives["inherited_count"] == 68 and negatives["new_count"] == 28)
    check("negative erasure forbidden", negatives["erasure_permitted"] is False and negatives["all_retained"] is True)
    check("five open gaps and six exact gates", gates["open_gap_count"] == 5 and gates["exact_gate_count"] == 6)
    check("no gate silently closed", gates["silently_closed"] == 0)
    check("active owner saved-project", context["active"][0]["project_state"] == "saved_project")
    check("projectless lanes standby", all(row["route_state"] == "STANDBY" for row in context["standby_projectless"]))
    check("future tasks not existing", all(row["exists"] is False for row in context["future_not_existing"]))
    check("no tasks or messages early", context["task_creation_by_this_phase"] == context["outbound_messages_before_terminal_validation"] == 0)
    check("schedule exact", schedule["assignment_count"] == len(schedule["assignments"]) == 150)
    check("schedule domain exact", all(1 <= row["phase"] <= 8 for row in schedule["assignments"]) and schedule["v9_permitted"] is False)
    check("schedule terminal exact", schedule["assignments"][-1]["phase_id"] == "v660-v8" and schedule["assignments"][-1]["terminal"] is True)
    check("authority remains least privilege", authority["owned_write_allowed"] is True and authority["sibling_write_allowed"] is False)
    check("no host mutation or elevation", authority["host_security_changed"] is False and authority["elevation"] is False)
    check("GMUT protected claims false", not any(gmut[key] for key in ["detected_force", "unique_prediction", "empirical_gmut_confirmation", "theory_of_everything", "proof_or_canon"]))
    check("calibration represented only", calibration["disposition"] == "represented" and calibration["real_measurement_rows"] == calibration["real_likelihoods"] == calibration["real_fits"] == 0)
    check("THOS zero real arms", thos["real_arm_runs"] == 0 and thos["state"] == "open_gap")
    check("THOS protected claims false", not any(thos[key] for key in ["superiority_established", "agi", "asi", "consciousness", "personhood"]))
    check("Freed ID production absent", all(freed[key] == 0 for key in ["real_keys", "real_proofs", "live_resolvers", "live_status_or_revocation_services", "interoperability_partners", "independent_security_reviews"]))
    check("Freed ID assurance false", freed["cryptographic_assurance"] is False and freed["trust_governance_established"] is False)
    check("CBR authority exact-gated", cbr["state"] == "exact_gate" and not any(cbr[key] for key in ["affected_party_authority_present", "maori_authority_present", "cultural_ratification_present", "competent_legal_authority_present", "enacted_law"]))
    check("thermo psyche protected claims false", not any(thermo[key] for key in ["fundamental_law_established", "consciousness_tensor", "consciousness", "personhood", "empirical_confirmation"]))
    check("independent reproduction reserved open", reservation["state"] == "open" and reservation["independent_team_present"] is False)
    check("terminal not ready", terminal["verdict"] == truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("all phase truth protected claims false", not any(truth["protected_claims"].values()))
    snapshot_ok = (
        x2["snapshot_state"] == "verified"
        and truth["same_owner_repeatability"] == "verified_bounded"
        and perturb["state"] == "verified"
    )
    check("snapshot state acceptable", snapshot_ok or allow_pending_snapshot, x2["snapshot_state"])
    mismatches = [
        rel for rel, expected in manifest["hashes"].items()
        if not (phase / rel).is_file() or digest(phase / rel) != expected
    ]
    check("manifest hashes match", not mismatches, mismatches)
    aggregate = hashlib.sha256(
        "".join(f"{rel}:{manifest['hashes'][rel]}\n" for rel in sorted(manifest["hashes"])).encode("utf-8")
    ).hexdigest()
    check("manifest aggregate matches", aggregate == manifest["aggregate_sha256"])
    check("manifest independence claim false", manifest["independent_team_reproduction"] is False)

    issues = [row for row in checks if not row["pass"]]
    return {
        "schema": "ghc.family.project-round-robin-minimal.v1",
        "runtime": "Python standard library only",
        "valid": not issues,
        "check_count": len(checks),
        "pass_count": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "summary": {
            "proposals": 10,
            "disposition_counts": EXPECTED,
            "retained_negatives": 96,
            "open_gaps": 5,
            "exact_gates": 6,
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
    result = verify(phase, args.allow_pending_snapshot)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else phase / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
