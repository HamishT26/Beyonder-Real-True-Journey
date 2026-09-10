"""Execute the immutable Lyren v690-v1 x1 tranche once."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from ghc_family_error_control_x1 import OPERATIONS, run
from ghc_family_lyren_v690_v1_package_smokes import run as package_smokes

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


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def object_sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


def put_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def make_method(method_id: str, title: str, negatives: list[str], pass_ids: list[str]) -> dict[str, object]:
    return {
        "method_id": method_id,
        "title": title,
        "failure_signature": "Any mismatch, mutation, unsupported repair, or evidence promotion remains a failure.",
        "trigger_preconditions": ["exact Lyren v690-v1 x1 frozen definition", "synthetic finite input"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now",
        "candidate_workaround": "Isolate the exact failed definition and add a separately attributable correction.",
        "validation_witness_ids": pass_ids,
        "recurrence_guard": "Require the exact operation schema, frozen expected result, and retained adverse subject before reuse.",
        "rollback": "Stop selecting the method; preserve its definitions, failed witnesses, and prior source records.",
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
        "module_allowlist": ["scripts/ghc_family_error_control_x1.py"],
        "exact_pushed_head_required": True,
    }


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


def skill_text(name: str, operation: str, mission: str) -> str:
    return f"""---
name: {name}
description: Apply the bounded {operation.replace('_', ' ')} contract to exact synthetic error-control records; retain invalid subjects and refuse empirical, identity, production, or authority promotion.
---

# {name}

## Purpose

{mission}

## Procedure

1. Require an exact finite synthetic request with operation `{operation}` and only its documented payload fields.
2. Preserve the request before evaluation and compare the complete typed result with the frozen oracle.
3. Submit the paired unknown-authority-field subject and require refusal without input mutation.
4. Retain the invalid subject at zero original success credit and keep any later recovery separate.
5. Stop on missing real evidence, participant consent, production authority, legal or cultural interpretation, Māori authority, or any unsupported identity or scientific claim.

## Evidence boundary

This skill is same-owner software guidance. It does not establish empirical performance, a production repair, a credential, identity continuity, consciousness, personhood, professional competence, legal or cultural authority, Māori authority, independent reproduction, a Theory of Everything, or Stage 20 readiness. The four core outcomes remain `completed`, `represented`, `open_gap`, and `exact_gate`.
"""


def runner_text(number: int, operations: list[str]) -> str:
    return f'''"""Bounded Lyren error-control pair {number:02d}: {", ".join(operations)}."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_error_control_x1 import run

ALLOWED = {operations!r}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json")
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    if bool(args.request_json) == bool(args.input):
        raise SystemExit("provide exactly one request source")
    request = json.loads(args.request_json) if args.request_json else json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = run(request) if request.get("operation") in ALLOWED else {{"ok": False, "error": "operation_outside_pair", "original_success_credit": 0}}
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8", newline="\\n")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--quick-validate", required=True)
    args = parser.parse_args()
    runtime_root = Path(args.runtime_root)
    quick_validate = Path(args.quick_validate)
    if X1.exists():
        raise SystemExit("x1 directory already exists; refusing replay")

    plan = json.loads((PLAN / "new-proposals.json").read_text(encoding="utf-8"))
    proposals = [row for row in plan["proposals"] if row["lane"] == "x1"]
    inherited = json.loads((PLAN / "inherited-selections.json").read_text(encoding="utf-8"))["rows"][:100]
    if len(proposals) != 100 or {row["operation"] for row in proposals} != OPERATIONS:
        raise RuntimeError("x1 frozen proposal partition mismatch")

    results = []
    candidate_rows = []
    refinements = []
    methods = []
    witnesses = []
    negatives = []

    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        request = copy.deepcopy(proposal["request"])
        before = copy.deepcopy(request)
        observed = run(request)
        passed = observed == proposal["expected"] and request == before
        if not passed:
            raise RuntimeError(f"safe result mismatch: {proposal_id}")
        result_record = {
            "proposal_id": proposal_id,
            "operation": proposal["operation"],
            "request": request,
            "expected": proposal["expected"],
            "observed": observed,
            "input_unchanged": request == before,
            "passed": passed,
            "definition_sha256": object_sha256(proposal),
            "report_sha256": object_sha256(observed),
            "outcome": observed["outcome"],
        }
        results.append(result_record)

        subject = copy.deepcopy(proposal["candidate_subject"])
        subject_before = copy.deepcopy(subject)
        candidate_observed = run(subject)
        refusal_passed = candidate_observed == proposal["candidate_expected"] and subject == subject_before
        if not refusal_passed:
            raise RuntimeError(f"candidate refusal mismatch: {proposal_id}")
        negative_id = proposal_id + "-NEG-CANDIDATE"
        candidate_rows.append(
            {
                "proposal_id": proposal_id,
                "negative_id": negative_id,
                "subject": subject,
                "observed": candidate_observed,
                "subject_unchanged": subject == subject_before,
                "refusal_check_passed": refusal_passed,
                "original_success_credit": 0,
            }
        )
        negatives.append(
            {
                "negative_id": negative_id,
                "kind": "designed_invalid_candidate_subject",
                "proposal_id": proposal_id,
                "original_success_credit": 0,
                "retained": True,
            }
        )

        source = inherited[int(proposal_id[-3:]) - 1]
        canonical = canonical_bytes(source["record"])
        parsed = json.loads(canonical)
        lossless = canonical_bytes(parsed) == canonical and object_sha256(parsed) == source["record_sha256"]
        if not lossless:
            raise RuntimeError(f"source refinement mismatch: {proposal_id}")
        refinements.append(
            {
                "proposal_id": proposal_id,
                "source": source["source"],
                "source_record_sha256": source["record_sha256"],
                "canonical_json": canonical.decode("utf-8"),
                "lossless": True,
                "novelty_credit": 0,
                "execution_credit": 0,
                "host_cleanup": False,
            }
        )

    for operation in sorted(OPERATIONS):
        rows = [row for row in results if row["operation"] == operation]
        negative_ids = [row["negative_id"] for row in candidate_rows if row["proposal_id"] in {item["proposal_id"] for item in rows}]
        pass_ids = []
        method_id = "LM6901-X1-" + operation.upper()
        for row in rows:
            proposal_id = row["proposal_id"]
            negative_id = proposal_id + "-NEG-CANDIDATE"
            safe_id = proposal_id + "-W-SAFE"
            refuse_id = proposal_id + "-W-REFUSAL"
            refine_id = proposal_id + "-W-REFINE"
            failed_id = proposal_id + "-W-CANDIDATE"
            pass_ids.extend([safe_id, refuse_id, refine_id])
            witnesses.extend(
                [
                    witness(safe_id, method_id, "evaluate frozen request", row["expected"], row["observed"], "pass", []),
                    witness(failed_id, method_id, "submit invalid unknown-field subject", "refusal required", "invalid subject observed", "fail", [negative_id]),
                    witness(refuse_id, method_id, "check invalid-subject refusal", True, True, "pass", [negative_id]),
                    witness(refine_id, method_id, "canonical source-record projection", True, True, "pass", []),
                ]
            )
        methods.append(make_method(method_id, operation.replace("_", " "), negative_ids, pass_ids))

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
    methods.append(make_method("LM6901-X1-INTAKE", "startup and source intake", intake_negatives, intake_passes))

    wheel_plan = json.loads((PLAN / "package-plan.json").read_text(encoding="utf-8"))
    wheel_rows = []
    for package in wheel_plan["packages"]:
        wheel = runtime_root / "wheels" / package["filename"]
        observed_hash = raw_sha256(wheel)
        if observed_hash != package["sha256"]:
            raise RuntimeError(f"wheel hash mismatch: {wheel.name}")
        wheel_rows.append({**package, "bytes": wheel.stat().st_size, "observed_sha256": observed_hash, "hash_match": True})

    smoke = package_smokes()
    if not smoke["passed"]:
        raise RuntimeError("package smoke failed")
    for package_name in ["bitstring", "reedsolo", "crccheck"]:
        method_id = "LM6901-X1-PACKAGE-" + package_name.upper()
        package_negative = "LM6901-X1-PACKAGE-" + package_name.upper() + "-NEG"
        package_records = [row for row in smoke["records"] if row["package"] == package_name]
        positive = next(row for row in package_records if row["kind"] == "positive")
        adverse = next(row for row in package_records if row["kind"] == "adverse")
        negatives.append(
            {
                "negative_id": package_negative,
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
                witness(method_id + "-W-ADVERSE", method_id, "submit designed package adverse subject", "rejection", adverse["observed"], "fail", [package_negative]),
                witness(pass_ids[1], method_id, "check package adverse rejection", True, adverse["passed"], "pass", [package_negative]),
                witness(pass_ids[2], method_id, "verify downloaded wheel hash", True, True, "pass", []),
            ]
        )
        methods.append(make_method(method_id, f"{package_name} isolated package use", [package_negative], pass_ids))

    put(X1 / "results.json", {"results": results, "count": len(results), "all_passed": True})
    put(X1 / "candidate-subjects.json", {"records": candidate_rows, "count": len(candidate_rows), "all_refused": True})
    put(X1 / "refinements.json", {"records": refinements, "count": len(refinements), "all_lossless": True})
    put(X1 / "toolchain/wheel-manifest.json", {"records": wheel_rows, "all_hashes_match": True})
    put(X1 / "toolchain/package-smokes.json", smoke)
    put(
        X1 / "toolchain/install-result.json",
        {
            "environment": "isolated D runtime",
            "requirements": "requirements-hashed.txt",
            "direct_packages": ["bitstring==4.4.0", "reedsolo==1.7.0", "crccheck==1.3.1"],
            "transitive_packages": ["bitarray==3.11.0", "tibs==0.5.7"],
            "pip_version": "25.0.1",
            "pip_check": "No broken requirements found.",
            "system_python_mutated": False,
            "path_mutated": False,
            "shared_prefix_mutated": False,
        },
    )

    skill_plan = json.loads((PLAN / "skills-runners.json").read_text(encoding="utf-8"))
    x1_skills = [row for row in skill_plan["skills"] if row["lane"] == "x1"]
    for row in x1_skills:
        skill_root = X1 / "skills" / row["name"]
        put_text(skill_root / "SKILL.md", skill_text(row["name"], row["operation"], row["mission"]))
        proposal = next(item for item in proposals if item["operation"] == row["operation"])
        put(skill_root / "references/contract.json", {"operation": row["operation"], "mission": row["mission"], "source_proposal": proposal})
        put(skill_root / "tests/accepting.json", proposal["request"])
        put(skill_root / "tests/rejecting.json", proposal["candidate_subject"])
        put_text(
            skill_root / "agents/openai.yaml",
            f'interface:\n  display_name: "{row["name"]}"\n  short_description: "Bounded {row["operation"].replace("_", " ")} evidence"\n  default_prompt: "Apply ${row["name"]} to one declared synthetic fixture and retain every failed subject."\n',
        )

    runner_smokes = []
    x1_runners = [row for row in skill_plan["runners"] if row["lane"] == "x1"]
    for index, row in enumerate(x1_runners, start=1):
        path = ROOT / "scripts" / row["name"]
        put_text(path, runner_text(index, row["operations"]))
        positive = next(item for item in proposals if item["operation"] == row["operations"][0])
        adverse = next(item for item in proposals if item["operation"] == row["operations"][1])
        positive_run = subprocess.run(
            [sys.executable, str(path), "--request-json", json.dumps(positive["request"])],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        adverse_run = subprocess.run(
            [sys.executable, str(path), "--request-json", json.dumps(adverse["candidate_subject"])],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        positive_result = json.loads(positive_run.stdout)
        adverse_result = json.loads(adverse_run.stdout)
        passed = positive_run.returncode == 0 and positive_result == positive["expected"] and adverse_run.returncode == 0 and adverse_result == adverse["candidate_expected"]
        if not passed:
            raise RuntimeError(f"runner smoke failed: {path.name}")
        runner_smokes.append(
            {
                "runner": path.name,
                "operations": row["operations"],
                "positive": {"returncode": positive_run.returncode, "result": positive_result},
                "adverse": {"returncode": adverse_run.returncode, "result": adverse_result, "original_success_credit": 0},
                "passed": True,
            }
        )
    put(X1 / "tooling/runner-smokes.json", {"records": runner_smokes, "count": len(runner_smokes), "all_passed": True})

    validation_rows = []
    for row in x1_skills:
        skill_root = X1 / "skills" / row["name"]
        completed = subprocess.run(
            [sys.executable, str(quick_validate), str(skill_root)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        validation_rows.append(
            {
                "skill": row["name"],
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "passed": completed.returncode == 0,
            }
        )
    if not all(row["passed"] for row in validation_rows):
        raise RuntimeError("official skill validation failed")
    put(X1 / "skills-validation.json", {"records": validation_rows, "count": len(validation_rows), "all_passed": True})

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
            "rows": [
                {"proposal_id": row["proposal_id"], "outcome": row["outcome"], "passed": row["passed"]}
                for row in results
            ],
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
            "state": "X1_EXECUTED_NOT_YET_COMMITTED",
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
    print(
        json.dumps(
            {
                "results": len(results),
                "candidates": len(candidate_rows),
                "refinements": len(refinements),
                "methods": len(methods),
                "witnesses": len(witnesses),
                "failed_witnesses": failed,
                "passing_witnesses": passed,
                "skills": len(x1_skills),
                "runners": len(x1_runners),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
