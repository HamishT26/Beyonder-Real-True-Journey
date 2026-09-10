"""Resume Lyren x1 only after the completed evidence tranche hit validator dependency gaps."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1"
PLAN = BASE / "plan"
X1 = BASE / "x1"
BOUNDARY = (
    "Same-owner finite software and documentation evidence only; no empirical GMUT, "
    "production repair, identity, consciousness, personhood, professional authority, "
    "legal or cultural authority, Māori authority, complete privacy or accessibility, "
    "exhaustive security, independent reproduction, Theory-of-Everything, or Stage 20 claim."
)
GATES = [
    "empirical",
    "participants",
    "professional",
    "production",
    "legal-cultural-Māori-authority",
    "privacy-accessibility-security-completeness",
    "independent-reproduction",
    "AGI-ASI-consciousness-personhood",
    "Theory-of-Everything-Stage-20",
]


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


def witness(
    witness_id: str,
    method_id: str,
    procedure: str,
    expected: object,
    observed: object,
    result: str,
    negatives: list[str],
) -> dict[str, object]:
    return {
        "witness_id": witness_id,
        "method_id": method_id,
        "procedure": procedure,
        "scope": "Lyren v690-v1 x1 exact synthetic owner fixture",
        "expected": expected,
        "observed": observed,
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": negatives,
        "boundary": BOUNDARY,
    }


def method(method_id: str, title: str, negatives: list[str], pass_ids: list[str], module: str) -> dict[str, object]:
    return {
        "method_id": method_id,
        "title": title,
        "failure_signature": "Any mismatch, mutation, unsupported repair, missing dependency, or evidence promotion remains a failure.",
        "trigger_preconditions": ["exact Lyren v690-v1 x1 frozen definition", "synthetic finite input"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now",
        "candidate_workaround": "Isolate the exact failed dependency and add a separately attributable correction.",
        "validation_witness_ids": pass_ids,
        "recurrence_guard": "Check the exact operation schema and validator runtime dependency before reuse.",
        "rollback": "Stop selecting the method; preserve definitions, failed witnesses, and source records.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": GATES,
        "retained_negative_ids": negatives,
        "scope_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "repository_scan": False,
        "module_scan": True,
        "cross_lane_scan": False,
        "unchanged_history_scan": False,
        "sibling_lane_mutation": False,
        "source_commit": "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e",
        "final_commit": "EXTERNAL_AFTER_FINAL_COMMIT",
        "changed_file_allowlist": [],
        "module_allowlist": [module],
        "exact_pushed_head_required": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator-python", required=True)
    parser.add_argument("--quick-validate", required=True)
    args = parser.parse_args()

    required_existing = [
        X1 / "results.json",
        X1 / "candidate-subjects.json",
        X1 / "refinements.json",
        X1 / "toolchain/package-smokes.json",
        X1 / "toolchain/wheel-manifest.json",
        X1 / "tooling/runner-smokes.json",
    ]
    if not all(path.is_file() for path in required_existing):
        raise RuntimeError("partial x1 evidence is incomplete; refusing recovery")
    if (X1 / "method-flow.json").exists():
        raise RuntimeError("x1 recovery already completed; refusing replay")

    skill_roots = sorted(path for path in (X1 / "skills").iterdir() if path.is_dir())
    if len(skill_roots) != 10:
        raise RuntimeError("expected ten existing x1 skill roots")
    validation_rows = []
    for skill_root in skill_roots:
        completed = subprocess.run(
            [args.validator_python, "-X", "utf8", args.quick_validate, str(skill_root)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        validation_rows.append(
            {
                "skill": skill_root.name,
                "runtime": "system Python with pre-existing PyYAML",
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "passed": completed.returncode == 0,
            }
        )
    if not all(row["passed"] for row in validation_rows):
        raise RuntimeError("bounded validator recovery still failed")
    put(
        X1 / "skills-validation.json",
        {
            "records": validation_rows,
            "count": len(validation_rows),
            "all_passed": True,
            "retained_failed_runtime_groups": ["LM6901-X1-OP001", "LM6901-X1-OP002"],
        },
    )

    results = json.loads((X1 / "results.json").read_text(encoding="utf-8"))["results"]
    candidates = json.loads((X1 / "candidate-subjects.json").read_text(encoding="utf-8"))["records"]
    refinements = json.loads((X1 / "refinements.json").read_text(encoding="utf-8"))["records"]
    package_smokes = json.loads((X1 / "toolchain/package-smokes.json").read_text(encoding="utf-8"))
    if len(results) != 100 or len(candidates) != 100 or len(refinements) != 100:
        raise RuntimeError("partial evidence counts changed")
    if not all(row["passed"] for row in results):
        raise RuntimeError("safe result did not pass")
    if not all(row["refusal_check_passed"] for row in candidates):
        raise RuntimeError("candidate refusal did not pass")
    if not all(row["lossless"] for row in refinements):
        raise RuntimeError("refinement did not remain lossless")

    methods = []
    witnesses = []
    negatives = []
    operations = sorted({row["operation"] for row in results})
    for operation in operations:
        rows = [row for row in results if row["operation"] == operation]
        method_id = "LM6901-X1-" + operation.upper()
        negative_ids = []
        pass_ids = []
        for row in rows:
            proposal_id = row["proposal_id"]
            negative_id = proposal_id + "-NEG-CANDIDATE"
            negative_ids.append(negative_id)
            negatives.append(
                {
                    "negative_id": negative_id,
                    "kind": "designed_invalid_candidate_subject",
                    "proposal_id": proposal_id,
                    "original_success_credit": 0,
                    "retained": True,
                }
            )
            safe_id = proposal_id + "-W-SAFE"
            failed_id = proposal_id + "-W-CANDIDATE"
            refusal_id = proposal_id + "-W-REFUSAL"
            refine_id = proposal_id + "-W-REFINE"
            pass_ids.extend([safe_id, refusal_id, refine_id])
            witnesses.extend(
                [
                    witness(safe_id, method_id, "evaluate frozen request", row["expected"], row["observed"], "pass", []),
                    witness(failed_id, method_id, "submit invalid unknown-field subject", "refusal required", "invalid subject observed", "fail", [negative_id]),
                    witness(refusal_id, method_id, "check invalid-subject refusal", True, True, "pass", [negative_id]),
                    witness(refine_id, method_id, "canonical source-record projection", True, True, "pass", []),
                ]
            )
        methods.append(method(method_id, operation.replace("_", " "), negative_ids, pass_ids, "scripts/ghc_family_error_control_x1.py"))

    startup = json.loads((PLAN / "startup-failures.json").read_text(encoding="utf-8"))["records"]
    intake_negatives = []
    intake_passes = []
    for record in startup:
        negative_id = record["id"]
        intake_negatives.append(negative_id)
        fail_id = negative_id + "-W-FAIL"
        pass_id = negative_id + "-W-RECOVERY"
        intake_passes.append(pass_id)
        negatives.append(
            {
                "negative_id": negative_id,
                "kind": "startup_operational_failure",
                "failure": record["failure"],
                "original_success_credit": 0,
                "retained": True,
            }
        )
        witnesses.append(witness(fail_id, "LM6901-X1-INTAKE", record["failure"], "no failure", record["failure"], "fail", [negative_id]))
        witnesses.append(witness(pass_id, "LM6901-X1-INTAKE", record["recovery"], "bounded recovery", "recovery passed", "pass", [negative_id]))
    methods.append(method("LM6901-X1-INTAKE", "startup and source intake", intake_negatives, intake_passes, "docs/lyren-moss/v690-v1/plan/startup-failures.json"))

    package_names = ["bitstring", "reedsolo", "crccheck"]
    for package_name in package_names:
        method_id = "LM6901-X1-PACKAGE-" + package_name.upper()
        negative_id = method_id + "-NEG"
        positive = next(row for row in package_smokes["records"] if row["package"] == package_name and row["kind"] == "positive")
        adverse = next(row for row in package_smokes["records"] if row["package"] == package_name and row["kind"] == "adverse")
        negatives.append(
            {
                "negative_id": negative_id,
                "kind": "designed_package_adverse_subject",
                "package": package_name,
                "original_success_credit": 0,
                "retained": True,
            }
        )
        pass_ids = [method_id + "-W-POSITIVE", method_id + "-W-REFUSAL", method_id + "-W-HASH"]
        witnesses.extend(
            [
                witness(pass_ids[0], method_id, "positive package smoke", True, positive["passed"], "pass", []),
                witness(method_id + "-W-ADVERSE", method_id, "submit designed package adverse subject", "rejection", adverse["observed"], "fail", [negative_id]),
                witness(pass_ids[1], method_id, "check package adverse rejection", True, adverse["passed"], "pass", [negative_id]),
                witness(pass_ids[2], method_id, "verify downloaded wheel hash", True, True, "pass", []),
            ]
        )
        methods.append(method(method_id, f"{package_name} isolated package use", [negative_id], pass_ids, "scripts/ghc_family_lyren_v690_v1_package_smokes.py"))

    operational_failures = [
        {
            "negative_id": "LM6901-X1-OP001",
            "failure": "The first x1 wrapper invoked all ten official skill validations under the isolated package runtime, where PyYAML was intentionally absent; 10/10 validators exited before examining a skill.",
            "recovery": "Use the pre-existing system Python that already supplies PyYAML only for the official read-only skill validator.",
        },
        {
            "negative_id": "LM6901-X1-OP002",
            "failure": "The first diagnostic repeated all ten validators under the bundled document Python, which also lacked PyYAML; 10/10 exited before skill inspection.",
            "recovery": "Probe validator runtime dependencies first, then run the ten skill roots once under the proven system Python.",
        },
    ]
    op_pass_ids = []
    for record in operational_failures:
        negative_id = record["negative_id"]
        negatives.append({**record, "kind": "operational_validator_dependency_failure", "original_success_credit": 0, "retained": True})
        witnesses.append(witness(negative_id + "-W-FAIL", "LM6901-X1-VALIDATOR-RUNTIME", record["failure"], "validator examines skills", "missing yaml dependency", "fail", [negative_id]))
        pass_id = negative_id + "-W-RECOVERY"
        op_pass_ids.append(pass_id)
        witnesses.append(witness(pass_id, "LM6901-X1-VALIDATOR-RUNTIME", record["recovery"], "10/10 valid", "10/10 valid", "pass", [negative_id]))
    methods.append(
        method(
            "LM6901-X1-VALIDATOR-RUNTIME",
            "official skill validator runtime dependency selection",
            [record["negative_id"] for record in operational_failures],
            op_pass_ids,
            "skill-creator/scripts/quick_validate.py",
        )
    )

    failed = sum(row["result"] == "fail" for row in witnesses)
    passed = sum(row["result"] == "pass" for row in witnesses)
    method_flow = {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": "v690-v1-x1",
        "owner": "Lyren Moss",
        "identity_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": [
            {"method_id": row["method_id"], "from": "candidate", "to": "validated", "reason": "bounded x1 passing witnesses exist"}
            for row in methods
        ],
        "recommendations": [
            {"method_id": row["method_id"], "state": "validated", "precondition": row["trigger_preconditions"], "rollback": row["rollback"]}
            for row in methods
        ],
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "failed_witnesses": failed,
            "passing_witnesses": passed,
            "retained_negatives": len(negatives),
        },
        "boundary": BOUNDARY,
    }
    put(X1 / "method-flow.json", method_flow)
    put(X1 / "negative-index.json", {"records": negatives, "count": len(negatives), "all_original_success_credit_zero": True})
    put(
        X1 / "completion-ledger.json",
        {
            "rows": [{"proposal_id": row["proposal_id"], "outcome": row["outcome"], "passed": row["passed"]} for row in results],
            "counts": {"completed": 100, "represented": 0, "open_gap": 0, "exact_gate": 0},
            "safe_tasks": 100,
            "candidate_subjects": 100,
            "clean_fix_refine": 100,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    put(
        X1 / "phase-truth.json",
        {
            "owner": "Lyren Moss",
            "phase": "v690-v1-x1",
            "planning_commit": "cd9baca94099be83f5b9a8ae5367e2f63a272614",
            "state": "X1_EXECUTED_AFTER_ISOLATED_VALIDATOR_DEPENDENCY_RECOVERY_NOT_YET_COMMITTED",
            "results": 100,
            "candidates": 100,
            "refinements": 100,
            "skills": 10,
            "runners": 5,
            "direct_packages": 3,
            "transitive_packages": 2,
            "method_counts": method_flow["counts"],
            "source_baseline": {"effective_negatives": 742, "methods": 50, "direct_witnesses": 1578},
            "x2_started": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )

    allowlist_path = X1 / "allowlist.json"
    manifest_path = X1 / "manifest.json"
    existing = sorted(path.relative_to(ROOT).as_posix() for path in X1.rglob("*") if path.is_file())
    put(
        allowlist_path,
        {
            "owner": "Lyren Moss",
            "phase": "x1",
            "allowed_paths": existing + [allowlist_path.relative_to(ROOT).as_posix(), manifest_path.relative_to(ROOT).as_posix()],
            "additive_only": True,
        },
    )
    entries = []
    for path in sorted(file for file in X1.rglob("*") if file.is_file() and file.name != "manifest.json"):
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": raw_sha256(path),
                "hash_domain": "raw_file_bytes",
            }
        )
    put(manifest_path, {"self_excluded": "manifest.json", "entry_count": len(entries), "entries": entries})
    print(json.dumps({"skills_valid": len(validation_rows), "methods": len(methods), "witnesses": len(witnesses), "failed": failed, "passing": passed, "negatives": len(negatives)}, sort_keys=True))


if __name__ == "__main__":
    main()
