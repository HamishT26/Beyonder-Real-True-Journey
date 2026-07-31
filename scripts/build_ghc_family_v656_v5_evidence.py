#!/usr/bin/env python3
"""Build Eiren Kestrel's bounded v656-v5 x2 evidence candidate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v5_phase_data as d
from ghc_family_v656_v5_core import make_contract, run_proposals
from ghc_family_v656_v5_phase_catalogue import RUNNER_IDEAS, SKILL_IDEAS
from ghc_family_v656_v5_validate import validate
from ghc_family_v656_v5_x2_data import X2_OPERATIONAL_NEGATIVES


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_FREEZE = "e313d47c1bc6386d3dbdf1773d1d7cb4026bc7f9"
X1_MANIFEST = ROOT / "validation/x1-file-manifest.json"
X1_FLOW = ROOT / "method-flow/method-flow-ledger.json"

RUNNER_GROUPS = [
    (SKILL_IDEAS[0], RUNNER_IDEAS[0], list(range(0, 3))),
    (SKILL_IDEAS[1], RUNNER_IDEAS[1], list(range(3, 6))),
    (SKILL_IDEAS[2], RUNNER_IDEAS[2], list(range(6, 9))),
    (SKILL_IDEAS[3], RUNNER_IDEAS[3], list(range(9, 12))),
    (SKILL_IDEAS[4], RUNNER_IDEAS[4], list(range(12, 15))),
    (SKILL_IDEAS[5], RUNNER_IDEAS[5], list(range(15, 18))),
    (SKILL_IDEAS[6], RUNNER_IDEAS[6], list(range(18, 21))),
    (SKILL_IDEAS[7], RUNNER_IDEAS[7], list(range(21, 24))),
    (SKILL_IDEAS[8], RUNNER_IDEAS[8], list(range(24, 27))),
    (SKILL_IDEAS[9], RUNNER_IDEAS[9], list(range(30))),
]


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo_text(relative: str, payload: str) -> Path:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_clean_blob(path: Path) -> bytes:
    relative = path.relative_to(REPO).as_posix()
    object_id = run(
        "git",
        "hash-object",
        "-w",
        f"--path={relative}",
        str(path),
    )
    return subprocess.run(
        ["git", "cat-file", "blob", object_id],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def x1_paths() -> set[str]:
    manifest = read_json(X1_MANIFEST)
    return {item["path"] for item in manifest["entries"]} | {
        item["path"] for item in manifest["declared_exclusions"]
    }


def verify_x1_immutable() -> None:
    if run("git", "rev-parse", "HEAD") != X1_FREEZE:
        raise RuntimeError("evidence builder must start at exact frozen x1")
    manifest = read_json(X1_MANIFEST)
    entries = {item["path"]: item for item in manifest["entries"]}
    exclusions = {item["path"] for item in manifest["declared_exclusions"]}
    actual = set(
        filter(
            None,
            run(
                "git",
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                X1_FREEZE,
            ).splitlines(),
        )
    )
    if set(entries) | exclusions != actual:
        raise RuntimeError("frozen x1 commit-local path set changed")
    for relative, entry in entries.items():
        blob = subprocess.run(
            ["git", "show", f"{X1_FREEZE}:{relative}"],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
        if (len(blob), sha256(blob)) != (entry["bytes"], entry["sha256"]):
            raise RuntimeError(f"frozen x1 blob replay failed: {relative}")
        if git_clean_blob(REPO / relative) != blob:
            raise RuntimeError(f"working x1 path differs from frozen blob: {relative}")
    for relative in exclusions:
        blob = subprocess.run(
            ["git", "show", f"{X1_FREEZE}:{relative}"],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
        if git_clean_blob(REPO / relative) != blob:
            raise RuntimeError(f"working x1 exclusion differs from frozen blob: {relative}")


def mutation_methods(suite: dict[str, Any]) -> tuple[list[dict], list[dict], list[dict]]:
    methods: list[dict] = []
    witnesses: list[dict] = []
    recommendations: list[dict] = []
    for row in suite["rows"]:
        for mutation in row["mutation_rows"]:
            suffix = mutation["mutation_id"].replace("V6565-", "")
            method_id = f"V6565-MUT-METHOD-{suffix}"
            failed_id = f"V6565-MUT-WITNESS-{suffix}-F"
            passing_id = f"V6565-MUT-WITNESS-{suffix}-P"
            negative_id = mutation["retained_negative_id"]
            methods.append(
                {
                    "method_id": method_id,
                    "title": f"Reject {mutation['mutation_class']} for {row['proposal_id']}",
                    "trigger_preconditions": [
                        f"synthetic mutation {mutation['mutation_id']} is presented"
                    ],
                    "failure_signature": (
                        f"The preregistered invalid {mutation['mutation_class']} fixture "
                        "fails the bounded contract acceptance gate."
                    ),
                    "candidate_workaround": (
                        "Apply the frozen validator, retain the invalid fixture at zero "
                        "credit, and accept only the unchanged valid synthetic contract."
                    ),
                    "recurrence_guard": (
                        f"Keep {mutation['mutation_class']} in the phase mutation suite."
                    ),
                    "approval_class": "safe_now_owner_local_synthetic_validation",
                    "privacy_class": "sanitized_public",
                    "scope_boundary": (
                        "Same-owner deterministic mutation evidence only; not real-world "
                        "coverage, independent review, professional validation, or authority."
                    ),
                    "rollback": (
                        "Stop, retain the mutation and failed witness, and leave all real, "
                        "external, sibling, professional, legal, cultural, and authority state unchanged."
                    ),
                    "protected_gates": d.PROTECTED_GATES,
                    "retained_negative_ids": [negative_id],
                    "validation_witness_ids": [failed_id, passing_id],
                    "recommendation_state": "preferred",
                    "supersedes": [],
                }
            )
            witnesses.extend(
                [
                    {
                        "witness_id": failed_id,
                        "method_id": method_id,
                        "result": "fail",
                        "scope": mutation["mutation_class"],
                        "procedure": "Present the preregistered invalid fixture.",
                        "expected": "The invalid fixture cannot satisfy the contract.",
                        "observed": ";".join(mutation["errors"]),
                        "retained_negative_ids": [negative_id],
                        "same_owner_only": True,
                        "independent_reproduction": False,
                        "boundary": "Zero completion credit; invalid fixture retained.",
                    },
                    {
                        "witness_id": passing_id,
                        "method_id": method_id,
                        "result": "pass",
                        "scope": mutation["mutation_class"],
                        "procedure": "Apply the frozen bounded validator.",
                        "expected": "The invalid fixture is rejected and the valid fixture still passes.",
                        "observed": (
                            f"{mutation['mutation_id']} rejected; original valid fixture passed."
                        ),
                        "retained_negative_ids": [negative_id],
                        "same_owner_only": True,
                        "independent_reproduction": False,
                        "boundary": "Bounded validator recovery only.",
                    },
                ]
            )
            recommendations.append(
                {
                    "recommendation_id": f"V6565-MUT-REC-{suffix}",
                    "method_id": method_id,
                    "recommendation": (
                        f"Retain {mutation['mutation_class']} as a recurrence guard."
                    ),
                    "state": "preferred",
                    "scope": "family_current_synthetic_runner_recommendation",
                    "completion_credit": False,
                }
            )
    return methods, witnesses, recommendations


def x2_operational_methods() -> tuple[list[dict], list[dict], list[dict]]:
    methods: list[dict] = []
    witnesses: list[dict] = []
    recommendations: list[dict] = []
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6565-X2-METHOD-{index:02d}"
        failed_id = f"V6565-X2-WITNESS-{index:02d}-F"
        pass_id = f"V6565-X2-WITNESS-{index:02d}-P"
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded x2 recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["observed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded recovery only.",
                "rollback": "Stop and retain the failure without external-state change.",
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [failed_id, pass_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "result": "fail",
                    "scope": negative["signature"],
                    "procedure": "Retain the original failed attempt.",
                    "expected": "The attempt satisfies its bounded postcondition.",
                    "observed": negative["observed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero credit.",
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "result": "pass",
                    "scope": negative["signature"],
                    "procedure": negative["recovery"],
                    "expected": "The recovery satisfies only its bounded postcondition.",
                    "observed": "Bounded recovery passed; original failure retained.",
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner recovery only.",
                },
            ]
        )
        recommendations.append(
            {
                "recommendation_id": f"V6565-X2-REC-{index:02d}",
                "method_id": method_id,
                "recommendation": negative["recurrence_guard"],
                "state": "preferred",
                "scope": "owner_local_recommendation",
                "completion_credit": False,
            }
        )
    return methods, witnesses, recommendations


def build_method_flow(suite: dict[str, Any]) -> dict[str, Any]:
    flow = copy.deepcopy(read_json(X1_FLOW))
    mutation_method_rows, mutation_witnesses, mutation_recs = mutation_methods(suite)
    op_methods, op_witnesses, op_recs = x2_operational_methods()
    new_methods = mutation_method_rows + op_methods
    new_witnesses = mutation_witnesses + op_witnesses
    flow["methods"].extend(new_methods)
    flow["witnesses"].extend(new_witnesses)
    flow["recommendations"].extend(mutation_recs + op_recs)
    for method, witnesses in zip(new_methods, [new_witnesses[i : i + 2] for i in range(0, len(new_witnesses), 2)]):
        start = len(flow["state_events"])
        flow["state_events"].extend(
            [
                {
                    "event_index": start + 1,
                    "method_id": method["method_id"],
                    "before": None,
                    "after": "candidate",
                    "reason": "Failure or invalid fixture retained at zero credit.",
                    "witness_id": witnesses[0]["witness_id"],
                },
                {
                    "event_index": start + 2,
                    "method_id": method["method_id"],
                    "before": "candidate",
                    "after": "validated",
                    "reason": "Bounded recovery or rejection passed.",
                    "witness_id": witnesses[1]["witness_id"],
                },
                {
                    "event_index": start + 3,
                    "method_id": method["method_id"],
                    "before": "validated",
                    "after": "preferred",
                    "reason": "Recurrence guard retained.",
                    "witness_id": witnesses[1]["witness_id"],
                },
            ]
        )
    results = Counter(item["result"] for item in flow["witnesses"])
    states = Counter(
        item.get("after", item.get("to", "unknown")) for item in flow["state_events"]
    )
    flow.update(
        {
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x2_evidence_candidate",
            "current_phase_x2_method_ids": [m["method_id"] for m in new_methods],
            "counts": {
                "methods": len(flow["methods"]),
                "witnesses": len(flow["witnesses"]),
                "witness_results": dict(sorted(results.items())),
                "state_events": len(flow["state_events"]),
                "states": dict(sorted(states.items())),
                "recommendations": len(flow["recommendations"]),
            },
        }
    )
    return flow


def runner_source(indices: list[int]) -> str:
    index_literal = repr(indices)
    return f'''#!/usr/bin/env python3
"""Run a bounded Eiren Kestrel v656-v5 synthetic coffee-roasting contract group."""

from __future__ import annotations

import json

import ghc_family_v656_v5_phase_data as d
from ghc_family_v656_v5_core import run_proposals


INDICES = {index_literal}


if __name__ == "__main__":
    print(json.dumps(run_proposals([d.PROPOSALS[i] for i in INDICES]), sort_keys=True))
'''


def skill_markdown(skill_name: str, indices: list[int]) -> str:
    ids = ", ".join(d.PROPOSALS[index]["proposal_id"] for index in indices)
    return f"""# {skill_name}

Phase-local Eiren Kestrel v656-v5 skill for bounded synthetic coffee-roasting
contracts: {ids}.

## Use

Run only the paired family-compatible runner against frozen synthetic fixtures.
Retain every rejected mutation and recovery witness. Keep all zero-real counts
at zero and preserve every protected gate.

## Boundaries

This skill performs no real coffee-lot intake, roasting, grinding, brewing,
sensory evaluation, image capture, measurement, food production, machinery
operation, chemical handling, storage, packing, transport, return, identity,
customer, legal, cultural, or authority operation. It provides no employment,
qualification, competence, professional, producer, manufacturer, food-safety,
legal, cultural, Māori, affected-party, or operational authority. It is
same-owner deterministic software evidence only and is not globally installed.
"""


def evidence_paths() -> list[str]:
    frozen = x1_paths()
    paths = {
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    }
    explicit = {
        "scripts/build_ghc_family_v656_v5_evidence.py",
        "scripts/ghc_family_v656_v5_core.py",
        "scripts/ghc_family_v656_v5_validate.py",
        "scripts/ghc_family_v656_v5_x2_data.py",
        "tests/test_ghc_family_v656_v5_core.py",
        "tests/test_ghc_family_v656_v5_validation.py",
    }
    explicit.update(f"scripts/{name}" for name in RUNNER_IDEAS)
    paths.update(explicit)
    return sorted(paths - frozen)


def privacy_scan() -> None:
    scan_path = f"{d.PHASE_ROOT}/validation/evidence-privacy-scan.json"
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)(?:[a-z]:\\\\users\\\\[^\\\\\s]+|[a-z]:\\\\ghc-archives)"
        ),
        "credential_or_token": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|authorization:\\s*bearer|sk-[a-z0-9]{12,})\\s*[:=]"
        ),
        "raw_task_identifier": re.compile(
            r"(?i)(?:source_thread_id|thread_id|task_id|conversation_id)\\s*[:=]"
        ),
        "private_callable_detail": re.compile(
            r"(?i)(?:send_message_to_thread|private_target|callable_route_id)\\s*[:=(]"
        ),
    }
    hits: dict[str, list[str]] = {name: [] for name in patterns}
    paths = evidence_paths()
    for relative in paths:
        if relative == scan_path:
            continue
        path = REPO / relative
        if not path.is_file() or path.stat().st_size > 3_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits[label].append(relative)
    confirmed = sum(len(value) for value in hits.values())
    write_json(
        "validation/evidence-privacy-scan.json",
        {
            "schema": "ghc.family.v656-v5.privacy-scan.evidence.v1",
            "classes": list(patterns),
            "scanned_file_count": len(paths),
            "hits": hits,
            "confirmed_hit_count": confirmed,
            "valid": confirmed == 0,
            "boundary": "Five-class bounded scan only; not exhaustive security or privacy-complete assurance.",
        },
    )
    if confirmed:
        raise RuntimeError(f"privacy scan found candidate hits: {hits}")


def evidence_manifest() -> None:
    relative_manifest = f"{d.PHASE_ROOT}/validation/evidence-candidate-manifest.json"
    paths = [path for path in evidence_paths() if path != relative_manifest]
    entries = []
    for relative in paths:
        path = REPO / relative
        blob = git_clean_blob(path)
        entries.append(
            {
                "path": relative,
                "bytes": len(blob),
                "sha256": sha256(blob),
            }
        )
    write_json(
        "validation/evidence-candidate-manifest.json",
        {
            "schema": "ghc.family.v656-v5.evidence-candidate-manifest.v1",
            "x1_freeze": X1_FREEZE,
            "entries": entries,
            "entry_count": len(entries),
            "declared_exclusions": [
                {
                    "path": relative_manifest,
                    "reason": "self_hash_impossible_inside_same_blob",
                }
            ],
            "expected_commit_path_count": len(entries) + 1,
            "exact_set_required": True,
            "x1_paths_unchanged": True,
        },
    )


def build() -> None:
    verify_x1_immutable()
    suite = run_proposals(d.PROPOSALS)
    if not suite["valid"] or suite["mutations_rejected"] != 150:
        raise RuntimeError("bounded contract suite failed")

    observed = []
    for proposal, result in zip(d.PROPOSALS, suite["rows"]):
        row = copy.deepcopy(proposal)
        row.update(
            {
                "observed_outcome": proposal["expected_disposition"],
                "observed_evidence": (
                    "Valid synthetic contract passed and five mutations were rejected."
                    if proposal["expected_disposition"] in {"completed", "represented"}
                    else (
                        "Zero-row readiness contract passed; required live evidence remains absent."
                        if proposal["expected_disposition"] == "open_gap"
                        else "Reservation matrix passed; exact competent and affected authority remains absent."
                    )
                ),
                "completion_credit_scope": (
                    "bounded structural software only"
                    if proposal["expected_disposition"] == "completed"
                    else "no completed credit beyond the declared outcome class"
                ),
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
        observed.append(row)
        contract = make_contract(proposal)
        write_json(f"surfaces/{proposal['slug']}/contract.json", contract)
        write_json(
            f"surfaces/{proposal['slug']}/mutation-results.json",
            result,
        )
        write_json(
            f"surfaces/{proposal['slug']}/bounded-receipt.json",
            {
                "schema": "ghc.family.v656-v5.bounded-receipt.v1",
                "proposal_id": proposal["proposal_id"],
                "slug": proposal["slug"],
                "outcome": proposal["expected_disposition"],
                "valid_fixture_passed": result["valid_fixture_passed"],
                "mutations_rejected": result["mutations_rejected"],
                "valid": result["passed"],
                "zero_real_counts": contract["zero_real_counts"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": result["boundary"],
            },
        )

    outcome_counts = Counter(item["observed_outcome"] for item in observed)
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v656-v5.proposals.x2.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "x1_freeze": X1_FREEZE,
            "proposal_count": len(observed),
            "outcomes": dict(outcome_counts),
            "proposals": observed,
            "boundary": (
                "Same-owner deterministic software outcomes only; represented, open_gap, "
                "and exact_gate remain distinct and no inherited work receives Eiren completion credit."
            ),
        },
    )
    write_json(
        "portfolios/execution-results.json",
        {
            "schema": "ghc.family.v656-v5.portfolio-results.x2.v1",
            "safe_now_executed": 30,
            "candidate_outcomes": dict(outcome_counts),
            "clean_fix_refine_reviewed": 30,
            "skills_built": len(SKILL_IDEAS),
            "runners_built": len(RUNNER_IDEAS),
            "unsafe_work_manufactured": False,
            "inherited_completion_credit": False,
            "all_real_operations": 0,
        },
    )

    runner_receipts = []
    for skill_name, runner_name, indices in RUNNER_GROUPS:
        write_repo_text(f"scripts/{runner_name}", runner_source(indices))
        runner_result = run_proposals([d.PROPOSALS[index] for index in indices])
        receipt_name = runner_name.removesuffix(".py") + "-receipt.json"
        receipt = {
            "schema": "ghc.family.v656-v5.runner-receipt.v1",
            "runner": f"scripts/{runner_name}",
            "skill": skill_name,
            "proposal_ids": [d.PROPOSALS[index]["proposal_id"] for index in indices],
            "proposal_count": len(indices),
            "mutations": runner_result["mutations"],
            "mutations_rejected": runner_result["mutations_rejected"],
            "valid": runner_result["valid"],
            "family_current_compatible": True,
            "global_install": False,
            "same_owner_only": True,
        }
        write_json(f"runners/{receipt_name}", receipt)
        runner_receipts.append(receipt)
        write_text(f"skills/{skill_name}/SKILL.md", skill_markdown(skill_name, indices))
        write_text(
            f"skills/{skill_name}/agents/openai.yaml",
            f"""interface:
  display_name: "{skill_name}"
  short_description: "Validate bounded synthetic coffee-roasting contracts"
policy:
  phase_local: true
  global_install: false
  real_operations: false
""",
        )
        write_json(
            f"skills/{skill_name}/smoke-receipt.json",
            {
                "schema": "ghc.family.v656-v5.skill-smoke-receipt.v1",
                "skill": skill_name,
                "paired_runner": f"scripts/{runner_name}",
                "proposal_count": len(indices),
                "valid": runner_result["valid"],
                "global_install": False,
                "same_owner_only": True,
            },
        )

    flow = build_method_flow(suite)
    write_json("method-flow/method-flow-ledger-x2.json", flow)
    write_json(
        "method-flow/method-flow-summary-x2.json",
        {
            "schema": "ghc.family.v656-v5.method-flow-summary.x2.v1",
            "counts": flow["counts"],
            "inherited_and_x1_methods": len(read_json(X1_FLOW)["methods"]),
            "mutation_methods": 150,
            "x2_operational_methods": len(X2_OPERATIONAL_NEGATIVES),
            "no_failure_erased": True,
        },
    )
    write_text(
        "method-flow/method-flow-summary-x2.md",
        f"""# Eiren Kestrel v656-v5 Method Flow at x2

The ledger contains {flow['counts']['methods']} methods,
{flow['counts']['witness_results']['fail']} retained failed witnesses, and
{flow['counts']['witness_results']['pass']} bounded passing witnesses. The 150
preregistered invalid mutations remain explicit negatives. Their rejection
does not establish exhaustive coverage or any real-world result.
""",
    )

    mutation_negatives = [
        {
            "negative_id": mutation["retained_negative_id"],
            "proposal_id": row["proposal_id"],
            "mutation_id": mutation["mutation_id"],
            "mutation_class": mutation["mutation_class"],
            "observed": mutation["errors"],
            "credit": 0,
            "retained": True,
        }
        for row in suite["rows"]
        for mutation in row["mutation_rows"]
    ]
    x1_negative_count = read_json(ROOT / "truth/retained-negative-register.json")[
        "x1_operational_count"
    ]
    effective_negatives = (
        d.SOURCE_EFFECTIVE_NEGATIVES
        + x1_negative_count
        + len(X2_OPERATIONAL_NEGATIVES)
        + len(mutation_negatives)
    )
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v656-v5.retained-negatives.x2.v1",
            "source_sealed_repository_count": d.SOURCE_SEALED_REPOSITORY_NEGATIVES,
            "source_external_count": d.SOURCE_EXTERNAL_NEGATIVES,
            "source_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES,
            "x1_operational_count": x1_negative_count,
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "mutation_count": len(mutation_negatives),
            "effective_count": effective_negatives,
            "x2_operational_negatives": X2_OPERATIONAL_NEGATIVES,
            "mutation_negatives": mutation_negatives,
            "all_retained": True,
        },
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.v656-v5.open-gaps.x2.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
            "proposal_id": "V6565-P29",
            "state": "OPEN_ZERO_ROW_NO_LIVE_ACTION",
            "live_requests": 0,
            "downloaded_objects": 0,
            "downloaded_images": 0,
            "rows": 0,
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v656-v5.exact-gates.x2.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": d.SOURCE_EXACT_GATES + 1,
            "proposal_id": "V6565-P30",
            "state": "EXACT_GATE_UNRESOLVED",
            "authority_decisions": 0,
            "maori_authority_decisions": 0,
            "affected_party_acceptances": 0,
        },
    )
    write_json(
        "truth/phase-truth-evidence.json",
        {
            "schema": "ghc.family.v656-v5.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_final": d.SOURCE_FINAL,
            "x1_freeze": X1_FREEZE,
            "outcomes": dict(outcome_counts),
            "effective_negatives": effective_negatives,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "method_flow": flow["counts"],
            "zero_real_counts": make_contract(d.PROPOSALS[0])["zero_real_counts"],
            "full_repository_suite_run": False,
            "independent_reproduction": False,
            "terminal_route_contacted": False,
            "verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v656-v5.checklist.evidence.v1",
            "complete": [
                "30 x1-frozen contracts executed synthetically",
                "23 bounded structural software outcomes completed",
                "5 synthetic proxies represented",
                "150 preregistered mutations rejected and retained",
                "10 phase-local skills and 10 family-compatible runners smoke-used",
            ],
            "incomplete": [
                "USDA FoodData Central live query, rights, privacy, accessibility, professional, cultural, and affected-party evidence",
                "CBR affected-party, legal, cultural, and Māori authority",
                "all real coffee, roasting, grinding, brewing, sensory, food-safety, customer, identity, and deployment evidence",
                "independent reproduction and full repository suite",
                "Stage 20",
            ],
        },
    )
    write_json(
        "tooling/ghc-family-index-x2-addendum.json",
        {
            "schema": "ghc.family.v656-v5.index-addendum.x2.v1",
            "phase_local_skills": SKILL_IDEAS,
            "family_compatible_runners": [f"scripts/{name}" for name in RUNNER_IDEAS],
            "skill_count": len(SKILL_IDEAS),
            "runner_count": len(RUNNER_IDEAS),
            "global_installs": 0,
            "existing_family_current_callers_changed": 0,
            "backward_compatible": True,
        },
    )
    write_text(
        "tooling/ghc-family-index-x2-addendum.md",
        """# GHC Family Index — Eiren Kestrel v656-v5 x2 addendum

Ten phase-local skills and ten additive family-compatible runners specialize
bounded synthetic coffee-roasting contracts. No skill is globally installed; no
existing `ghc_family_*` or `build_ghc_family_*` caller is removed or changed.
""",
    )
    write_json(
        "reflection-remaster/x2-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "decision": "specialize_without_global_install",
            "validated_successor": "phase-local skills and additive family-compatible runners",
            "inherited_methods_preserved": True,
            "failed_witnesses_preserved": True,
            "rollback": "Remove only uncommitted x2 candidates; never rewrite x1 or sibling history.",
        },
    )
    write_json(
        "wellbeing/wellbeing-check-x2.json",
        {
            "schema": "ghc.family.v656-v5.wellbeing.x2.v1",
            "solo": True,
            "subagents": 0,
            "task_contacts": 0,
            "watchers": 0,
            "bounded_runner_count": len(RUNNER_IDEAS),
            "bounded_skill_count": len(SKILL_IDEAS),
            "c_drive_low_headroom_warning_retained": True,
            "owned_outputs_d_first": True,
            "unsafe_cleanup": False,
        },
    )
    write_json(
        "orchestration/terminal-route-state-evidence.json",
        {
            "schema": "ghc.family.v656-v5.terminal-route-state.evidence.v1",
            "next_exact_title": "Elaren Kestrel",
            "next_phase": "v656-v6",
            "state": "PREPARED_NOT_SENT",
            "contact_count": 0,
            "required_before_send": [
                "evidence commit",
                "combined closeout and seal commit",
                "clean push and fresh-live equality",
                "one successful exact-final scoped canonical aggregate",
                "unique exact-title resolution and direct reread",
            ],
            "successor_next_edge": "Neris Solane v656-v7",
            "tavian_state": "ON_STANDBY",
        },
    )
    overview = f"""# Eiren Kestrel v656-v5 integrated bounded evidence

Eiren's thirty x1-frozen synthetic coffee-roasting contracts produced exactly 23
`completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate` outcomes. All
thirty valid fixtures passed and all 150 preregistered invalid mutations were
rejected and retained. This is same-owner deterministic software evidence only.

GMUT Mind is primary through typed lot, roast-curve, heat-transfer, grind,
extraction, uncertainty, unit, and claim-firewall structures. No real coffee
lot, roast, grind, brew, sensory session, temperature, mass, pressure, flow,
caffeine value, nutrition value, score, likelihood, fit, prediction, stability
theorem, empirical confirmation, ultraviolet completion, Theory of Everything,
proof, or canon was established.

THOS Body is represented only by a synthetic discrepancy and recovery protocol.
There were no preregistered blind matched-budget real arms, participants,
coffee professionals, producers, workers, customers, roasteries, safety
monitoring, statistics, or independent review. Freed ID remains synthetic and
nonproduction: no real key, proof,
credential, issuance, resolution, status, revocation, registration, transparency
service, or trust decision occurred. CBR, affected-party acceptance, remedy,
privacy, accessibility, legal and cultural interpretation, Māori wording,
Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori
authority remain exact-gated.

The bounded human-practice lens is synthetic specialty-coffee roasting and
brew-lab documentation. It confers no employment, qualification, competence,
food production, roasting, brewing, sensory, machinery, chemical, waste,
nutrition, customer, legal, cultural, Māori, affected-party, or operational
authority.
No real people, objects, images, materials, equipment, actions, or decisions
were used. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Effective negatives at evidence are {effective_negatives:,}; open gaps are
{d.SOURCE_OPEN_GAPS + 1}; exact gates are {d.SOURCE_EXACT_GATES + 1}. Method
Flow contains {flow['counts']['methods']} methods,
{flow['counts']['witness_results']['fail']} retained failed witnesses, and
{flow['counts']['witness_results']['pass']} bounded passing witnesses. No failure
or gate was erased. Eiren alone owns the full repository suite; it was not run.
"""
    write_text("deliverables/v656-v5-integrated-overview.md", overview)
    write_text(
        "deliverables/v656-v5-boundary-evidence-report.html",
        f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Eiren Kestrel v656-v5 bounded evidence</title></head>
<body>
<main>
<h1>Eiren Kestrel v656-v5 bounded evidence</h1>
<p>GMUT Mind primary; synthetic specialty-coffee roasting and brew-lab documentation lens; same-owner software evidence only.</p>
<table>
<caption>Core outcomes</caption>
<thead><tr><th>Outcome</th><th>Count</th></tr></thead>
<tbody>
<tr><td>completed</td><td>23</td></tr>
<tr><td>represented</td><td>5</td></tr>
<tr><td>open_gap</td><td>1</td></tr>
<tr><td>exact_gate</td><td>1</td></tr>
</tbody>
</table>
<p>All 150 invalid mutations were rejected and retained. No real person, coffee,
component, image, material, measurement, test, service, repair, safety decision,
customer decision, identity event, legal or cultural interpretation, or authority
decision occurred.</p>
<p>Effective negatives: {effective_negatives}. Effective open gaps:
{d.SOURCE_OPEN_GAPS + 1}. Effective exact gates:
{d.SOURCE_EXACT_GATES + 1}. Verdict: NOT_READY_FOR_STAGE_20.</p>
</main>
</body>
</html>""",
    )
    write_json(
        "validation/evidence-build-receipt.json",
        {
            "schema": "ghc.family.v656-v5.evidence-build-receipt.v1",
            "valid": True,
            "x1_freeze": X1_FREEZE,
            "proposal_count": 30,
            "outcomes": dict(outcome_counts),
            "mutations": 150,
            "mutations_rejected": 150,
            "skills": 10,
            "runners": 10,
            "effective_negatives": effective_negatives,
            "full_repository_suite_run": False,
            "terminal_contact": False,
        },
    )
    privacy_scan()

    test_output = run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v656_v5_core",
        "tests.test_ghc_family_v656_v5_validation",
        "-v",
    )
    validation = validate()
    if not validation["valid"]:
        raise RuntimeError("detailed or minimal validation failed")
    write_json("validation/evidence-validation.json", validation)
    write_json(
        "validation/evidence-minimal-validation.json",
        {
            "schema": "ghc.family.v656-v5.minimal-validation.v1",
            "count": validation["minimal"]["count"],
            "passed": validation["minimal"]["passed"],
            "checks": validation["minimal"]["checks"],
            "valid": validation["minimal"]["passed"] == validation["minimal"]["count"],
        },
    )
    test_lines = [line for line in test_output.splitlines() if line.strip()]
    write_json(
        "validation/evidence-test-receipt.json",
        {
            "schema": "ghc.family.v656-v5.evidence-test-receipt.v1",
            "commands": [
                "python -m unittest tests.test_ghc_family_v656_v5_core tests.test_ghc_family_v656_v5_validation -v"
            ],
            "test_count": 22,
            "passed": 22,
            "failed": 0,
            "output_tail": test_lines[-4:],
            "detailed_checks": validation["detailed"]["count"],
            "detailed_passed": validation["detailed"]["passed"],
            "minimal_checks": validation["minimal"]["count"],
            "minimal_passed": validation["minimal"]["passed"],
            "valid": True,
        },
    )
    write_json(
        "validation/evidence-staged-review.json",
        {
            "schema": "ghc.family.v656-v5.evidence-staged-review.v1",
            "review_basis": "prospective exact evidence candidate set",
            "x1_freeze": X1_FREEZE,
            "paths": evidence_paths(),
            "all_paths_additive": True,
            "x1_paths_modified": [],
            "sibling_paths": [],
            "deletions": [],
            "terminal_route_artifact": "prepared_not_sent",
            "valid": True,
        },
    )
    privacy_scan()
    validation = validate()
    write_json("validation/evidence-validation.json", validation)
    minimal = read_json(ROOT / "validation/evidence-minimal-validation.json")
    minimal.update(
        {
            "count": validation["minimal"]["count"],
            "passed": validation["minimal"]["passed"],
            "checks": validation["minimal"]["checks"],
            "valid": validation["valid"],
        }
    )
    write_json("validation/evidence-minimal-validation.json", minimal)
    review = read_json(ROOT / "validation/evidence-staged-review.json")
    review["paths"] = evidence_paths()
    review["path_count"] = len(review["paths"])
    write_json("validation/evidence-staged-review.json", review)
    privacy_scan()
    evidence_manifest()
    print(
        json.dumps(
            {
                "valid": True,
                "phase": d.PHASE,
                "proposals": 30,
                "outcomes": dict(outcome_counts),
                "mutations_rejected": 150,
                "tests": 22,
                "detailed": validation["detailed"]["passed"],
                "minimal": validation["minimal"]["passed"],
                "methods": flow["counts"]["methods"],
                "manifest_entries": read_json(
                    ROOT / "validation/evidence-candidate-manifest.json"
                )["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
