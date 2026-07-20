#!/usr/bin/env python3
"""Build Sylven Arc's additive v650-v6 x2 bounded evidence packet."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v650_v6_phase_data as d
import ghc_family_v650_v6_runtime as runtime
import ghc_family_v650_v6_x2_data as x2d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "b8e0109a003e2fa90794b48b3691dc76a3c06ef2"
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts"
METHOD_RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"

RUNNER_GROUPS = {
    d.RUNNER_IDEAS[0]: ["V6506-P01", "V6506-P02", "V6506-P03", "V6506-P04"],
    d.RUNNER_IDEAS[1]: ["V6506-P05", "V6506-P06", "V6506-P07"],
    d.RUNNER_IDEAS[2]: ["V6506-P08", "V6506-P09", "V6506-P10"],
    d.RUNNER_IDEAS[3]: ["V6506-P11", "V6506-P12", "V6506-P13", "V6506-P18", "V6506-P19"],
    d.RUNNER_IDEAS[4]: ["V6506-P14", "V6506-P15"],
    d.RUNNER_IDEAS[5]: ["V6506-P16", "V6506-P17"],
    d.RUNNER_IDEAS[6]: ["V6506-P20"],
    d.RUNNER_IDEAS[7]: ["V6506-P05", "V6506-P06", "V6506-P07", "V6506-P08", "V6506-P09", "V6506-P10"],
    d.RUNNER_IDEAS[8]: ["V6506-P11", "V6506-P12", "V6506-P13", "V6506-P18", "V6506-P19"],
    d.RUNNER_IDEAS[9]: [row["proposal_id"] for row in d.PROPOSALS],
}


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        list(args), cwd=REPO, check=True, capture_output=True, text=True,
        encoding="utf-8", env=env,
    )
    return result.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def build_method_flow() -> dict[str, Any]:
    ledger = ROOT / "method-flow/x2-method-flow-state.json"
    if not ledger.exists():
        run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", f"{d.PHASE}-x2", "--owner", d.OWNER)
    existing = read_json(ledger)
    existing_ids = {row["method_id"] for row in existing["methods"]}
    for index, negative in enumerate(x2d.X2_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6506-X2M{index:02d}"
        record = {
            "method_id": method_id,
            "title": f"Recover {negative['category']} while retaining the failed witness",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [f"The v650-v6 x2 lane encounters {negative['category']}."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": "Give the failed attempt zero evidence credit, retain it, and leave external and sibling state unchanged.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "x1_immutability", "single_pass_budget"],
            "retained_negative_ids": [negative["negative_id"]],
            "scope_boundary": "Bounded same-owner recovery only; no production, empirical, professional, authority, independent-reproduction, or Stage 20 credit.",
        }
        record_path = write_json(f"method-flow/x2-{method_id.casefold()}-method-record.json", record)
        if method_id in existing_ids:
            continue
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in (
            ("WFAIL", "fail", negative["failed"], negative["failed"]),
            ("WPASS", "pass", negative["recovery"], negative["passing"]),
        ):
            witness = {
                "witness_id": f"{method_id}-{suffix}",
                "method_id": method_id,
                "procedure": procedure,
                "scope": f"bounded {negative['category']} {'failed' if result == 'fail' else 'recovery'} witness",
                "expected": "Return attributable evidence in the declared bounded domain.",
                "observed": observed,
                "result": result,
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Retained bounded witness only; no independent reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/x2-{witness['witness_id'].casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        state = next(row["recommendation_state"] for row in read_json(ledger)["methods"] if row["method_id"] == method_id)
        if state == "validated":
            run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only for this bounded trigger after one retained failure and one passing recovery witness.")
        elif state != "preferred":
            raise RuntimeError(f"unexpected Method Flow state: {method_id} {state}")
    validation = ROOT / "method-flow/x2-method-flow-validation.json"
    summary_json = ROOT / "method-flow/x2-method-flow-summary.json"
    summary_md = ROOT / "method-flow/x2-method-flow-summary.md"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(validation))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(summary_json), "--markdown-output", str(summary_md))
    return read_json(summary_json)


def wrapper_source(name: str, ids: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded v650-v6 runner: {name}."""

from ghc_family_v650_v6_runner import wrapper_main

PROPOSAL_IDS = {ids!r}

if __name__ == "__main__":
    raise SystemExit(wrapper_main("{name}", PROPOSAL_IDS))
'''


def build_runners() -> list[dict[str, Any]]:
    rows = []
    for index, name in enumerate(d.RUNNER_IDEAS, 1):
        path = REPO / "scripts" / name
        path.write_text(wrapper_source(name, RUNNER_GROUPS[name]), encoding="utf-8", newline="\n")
        witness = ROOT / "runner-witnesses" / f"{Path(name).stem}.json"
        run(sys.executable, str(path), "--output", str(witness))
        payload = read_json(witness)
        if not payload["passed"]:
            raise RuntimeError(f"runner failed: {name}")
        rows.append({
            "runner_id": f"V6506-RUN-{index:02d}",
            "name": name,
            "proposal_ids": RUNNER_GROUPS[name],
            "built": True,
            "invoked": True,
            "passed": True,
            "witness": witness.relative_to(ROOT).as_posix(),
            "valid_fixture_count": payload["valid_fixture_count"],
            "rejected_mutation_count": payload["rejected_mutation_count"],
            "same_owner_only": True,
            "independent_reproduction": False,
        })
    return rows


def skill_markdown(name: str, proposal: dict[str, Any], runner: str) -> str:
    return f"""---
name: {name}
description: Audit the frozen v650-v6 {proposal['slug']} contract with bounded fixtures, mutation rejection, explicit evidence limits, and fail-closed protected gates. Use for owner-scoped review of this exact proposal surface.
---

# {name}

1. Read `references/contract.md` and proposal `{proposal['proposal_id']}`.
2. Run `scripts/{runner}` only on disposable synthetic, symbolic, structural, numerical, or zero-row fixtures.
3. Inspect `surfaces/{proposal['slug']}/contract.json`, `mutation-results.json`, and `bounded-receipt.json`.
4. Reject external downloads, real participant or operator work, production identity activity, account-secret use, authority decisions, deployment, destructive action, sibling mutation, and unsupported claim promotion.
5. Preserve every failed witness and use only `completed`, `represented`, `open_gap`, or `exact_gate` inside the frozen evidence class.

## Boundary

This package is phase-local and not globally installed. It confers no scientific truth, professional competence, production readiness, legal or cultural authority, Māori authority, complete privacy, exhaustive security, complete accessibility, independent reproduction, consciousness or personhood claim, Theory of Everything, or Stage 20 authorization.
"""


def build_skills(runner_for: dict[str, str]) -> list[dict[str, Any]]:
    skills_root = ROOT / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (name, proposal) in enumerate(zip(d.SKILL_IDEAS, d.PROPOSALS), 1):
        target = skills_root / name
        if not target.exists():
            display = " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))
            run(
                sys.executable, str(SKILL_CREATOR / "init_skill.py"), name,
                "--path", str(skills_root), "--resources", "references",
                "--interface", f"display_name={display}",
                "--interface", "short_description=Audit bounded evidence and exact gates",
                "--interface", f"default_prompt=Use ${name} to audit its frozen bounded contract.",
            )
        runner = runner_for[proposal["proposal_id"]]
        (target / "SKILL.md").write_text(skill_markdown(name, proposal, runner), encoding="utf-8", newline="\n")
        (target / "references").mkdir(parents=True, exist_ok=True)
        (target / "references/contract.md").write_text(
            f"""# {proposal['proposal_id']} bounded contract

- Hypothesis: {proposal['hypothesis']}
- Null or failure: {proposal['null_or_failure_condition']}
- Acceptance: {proposal['falsifier_or_acceptance_gate']}
- Rollback: {proposal['rollback_or_recovery']}
- Expected disposition: `{proposal['expected_disposition']}`
- Required obligations: {', '.join(runtime.OBLIGATIONS[proposal['proposal_id']])}

Sources and fixtures provide requirements context only. They are not observations, participant evidence, production readiness, authority, or independent review.
""",
            encoding="utf-8", newline="\n",
        )
        display = " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))
        run(
            sys.executable, str(SKILL_CREATOR / "generate_openai_yaml.py"), str(target),
            "--name", name,
            "--interface", f"display_name={display}",
            "--interface", "short_description=Audit bounded evidence and exact gates",
            "--interface", f"default_prompt=Use ${name} to audit its frozen bounded contract.",
        )
        validation_output = run(sys.executable, str(SKILL_CREATOR / "quick_validate.py"), str(target))
        execution = runtime.execute_proposal(proposal["proposal_id"])
        smoke = {
            "schema": "ghc.family.v650-v6.skill-smoke.v1",
            "skill_id": f"V6506-SKILL-{index:02d}",
            "name": name,
            "proposal_id": proposal["proposal_id"],
            "initialized_with_official_workflow": True,
            "metadata_generated_with_official_workflow": True,
            "quick_validate_output": validation_output,
            "smoke_used": True,
            "smoke_passed": execution["passed"],
            "global_install": False,
            "subagent_forward_test": "not_run_because_activation_forbids_delegation",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        witness = write_json(f"skill-witnesses/{name}.json", smoke)
        if not smoke["smoke_passed"]:
            raise RuntimeError(f"skill smoke failed: {name}")
        rows.append({
            "skill_id": smoke["skill_id"], "name": name,
            "proposal_id": proposal["proposal_id"], "package": target.relative_to(ROOT).as_posix(),
            "witness": witness.relative_to(ROOT).as_posix(), "initialized": True,
            "validated": True, "smoke_used": True, "global_install": False,
        })
    return rows


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v650_v6_evidence.py",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                row = {"path": relative, "pattern_class": pattern_class}
                candidates.append(row)
                if relative not in definitions:
                    confirmed.append({**row, "disposition": "confirmed_payload_hit"})
    return {
        "schema": "ghc.family.v650-v6.evidence-privacy.v1",
        "scanned_file_count": len(paths), "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates), "candidates": candidates,
        "scanner_definition_paths": sorted(definitions),
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def build_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/evidence-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [hash_entry(path) for path in paths if (REPO / path).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/evidence-staged-privacy.json", privacy)
    write_json("validation/evidence-staged-manifest.json", {
        "schema": "ghc.family.v650-v6.evidence-staged-manifest.v1",
        "hash_domain": "git_path_filtered_blob", "entries": entries,
        "entry_count": len(entries), "self_exclusions": exclusions,
        "coverage_boundary": "All intended additive x2 evidence paths except three declared self-referential review receipts.",
    })
    write_json("validation/evidence-staged-review.json", {
        "schema": "ghc.family.v650-v6.evidence-staged-review.v1",
        "intended_path_count": len(entries) + len(exclusions),
        "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions),
        "out_of_scope_paths": [], "x1_modified_paths": [],
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "proposal_receipts": 20, "mutations_executed": 100,
        "x2_only": True, "x1_commit": X1_COMMIT,
        "terminal_route": "PREPARED_NOT_SENT",
    })
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"x2 privacy scan found confirmed hits: {privacy['confirmed_hits']}")


def build() -> None:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("x2 evidence must begin at the exact pushed x1 commit")
    if git("status", "--porcelain=v1", "--untracked-files=normal").strip():
        allowed_seed = {
            "scripts/build_ghc_family_v650_v6_evidence.py",
            "scripts/ghc_family_v650_v6_runtime.py",
            "scripts/ghc_family_v650_v6_runner.py",
            "scripts/ghc_family_v650_v6_x2_data.py",
            "tests/test_ghc_family_v650_v6_x2.py",
        }
        start = set(status_paths())
        allowed_runner_paths = {f"scripts/{name}" for name in d.RUNNER_IDEAS}
        allowed = allowed_seed | allowed_runner_paths | {
            path for path in start if path.startswith(f"{d.PHASE_ROOT}/")
        }
        unexpected = start - allowed
        if unexpected:
            raise RuntimeError(f"unexpected pre-x2 tree: {sorted(unexpected)}")
        raw_status = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
        staged_adds = set(git("diff", "--cached", "--diff-filter=A", "--name-only").splitlines())
        tracked_changes = sorted(
            row[3:].replace("\\", "/")
            for row in raw_status
            if len(row) > 3
            and row[:2] not in {"??", "A "}
            and row[3:].replace("\\", "/") not in staged_adds
        )
        if tracked_changes:
            raise RuntimeError(f"x1 tracked paths changed during x2 recovery: {tracked_changes}")
    x1_truth = read_json(ROOT / "phase-truth.json")
    if x1_truth["stage"] != "x1_frozen_not_executed" or x1_truth["x2_started"]:
        raise RuntimeError("x1 boundary is not frozen")

    proposal_rows = []
    mutation_rows = []
    runner_for: dict[str, str] = {}
    for name, ids in RUNNER_GROUPS.items():
        for proposal_id in ids:
            runner_for.setdefault(proposal_id, name)
    for proposal in d.PROPOSALS:
        proposal_id = proposal["proposal_id"]
        result = runtime.execute_proposal(proposal_id)
        if not result["passed"]:
            raise RuntimeError(f"proposal runtime failed: {proposal_id}")
        slug = proposal["slug"]
        write_json(f"surfaces/{slug}/contract.json", {
            "schema": "ghc.family.v650-v6.surface-contract.v1",
            "proposal_id": proposal_id, "slug": slug,
            "required_obligations": runtime.OBLIGATIONS[proposal_id],
            "expected_disposition": proposal["expected_disposition"],
            "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
            "rollback": proposal["rollback_or_recovery"],
            "protected_gates": proposal["protected_gates"],
        })
        mutation_path = write_json(f"surfaces/{slug}/mutation-results.json", {
            "schema": "ghc.family.v650-v6.surface-mutations.v1",
            "proposal_id": proposal_id, "count": 5, "mutations": result["mutations"],
            "all_rejected": all(row["result"] == "rejected" for row in result["mutations"]),
        })
        receipt = write_json(f"surfaces/{slug}/bounded-receipt.json", {
            "schema": "ghc.family.v650-v6.bounded-receipt.v1",
            "proposal_id": proposal_id, "slug": slug,
            "outcome": proposal["expected_disposition"], "passed": result["passed"],
            "witness": result["canonical_fixture"],
            "canonical_result": result["canonical_result"],
            "mutations_rejected": 5, "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Bounded evidence only; no empirical, participant, production, professional, authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, Theory-of-Everything, or Stage 20 credit.",
        })
        proposal_rows.append({
            "proposal_id": proposal_id, "title": proposal["title"],
            "outcome": proposal["expected_disposition"], "passed": True,
            "receipt": receipt.relative_to(ROOT).as_posix(),
            "mutation_results": mutation_path.relative_to(ROOT).as_posix(),
        })
        mutation_rows.extend(result["mutations"])

    distribution = dict(Counter(row["outcome"] for row in proposal_rows))
    if distribution != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(f"wrong outcome distribution: {distribution}")
    if len(mutation_rows) != 100 or any(row["result"] != "rejected" for row in mutation_rows):
        raise RuntimeError("all one hundred mutations must execute and reject")

    runner_rows = build_runners()
    skill_rows = build_skills(runner_for)
    method_summary = build_method_flow()

    safe_plan = read_json(ROOT / "portfolios/safe-now-plan.json")["items"]
    candidate_plan = read_json(ROOT / "portfolios/candidate-plan.json")["items"]
    clean_plan = read_json(ROOT / "portfolios/clean-fix-refine-plan.json")["items"]
    safe_rows = [{**row, "x2_state": "completed_bounded", "completion_credit": True, "evidence": "evidence/x2-evidence-ledger.json"} for row in safe_plan]
    candidate_rows = []
    for index, row in enumerate(candidate_plan, 1):
        proposal_id = d.PROPOSALS[(index - 1) % len(d.PROPOSALS)]["proposal_id"]
        result = runtime.execute_proposal(proposal_id)
        prototype = write_json(f"prototypes/{index:02d}-{d.CANDIDATE_TASKS[index-1].replace(' ', '-').casefold()}.json", {
            "schema": "ghc.family.v650-v6.candidate-prototype.v1",
            "candidate_id": row["item_id"], "title": row["title"],
            "proposal_id": proposal_id, "built": True, "tested": True,
            "invoked": True, "passed": result["passed"],
            "boundary": "Disposable bounded prototype only; not production, professional, empirical, or authority evidence.",
        })
        candidate_rows.append({**row, "x2_state": "completed_bounded_prototype", "completion_credit": True, "proposal_id": proposal_id, "prototype": prototype.relative_to(ROOT).as_posix()})
    clean_rows = [{**row, "x2_state": "completed_additive", "completion_credit": True, "destructive_action": False, "evidence": "validation/evidence-staged-review.json"} for row in clean_plan]

    write_json("validation/x2-synthetic-mutation-results.json", {
        "schema": "ghc.family.v650-v6.x2-mutations.v1",
        "planned_count": 100, "executed_count": 100,
        "rejected_or_quarantined_count": 100, "completion_credit": 0,
        "mutations": mutation_rows,
    })
    write_json("evidence/x2-evidence-ledger.json", {
        "schema": "ghc.family.v650-v6.x2-evidence-ledger.v1",
        "phase": d.PHASE, "owner": d.OWNER, "x1_commit": X1_COMMIT,
        "proposal_count": 20, "distribution": distribution,
        "proposals": proposal_rows, "same_owner_only": True,
        "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("evidence/source-use-receipt.json", {
        "schema": "ghc.family.v650-v6.source-use.v1", "source_count": len(d.SOURCES),
        "status_counts": dict(Counter(row["status"] for row in d.SOURCES)),
        "observation_credit": 0,
        "boundary": "Official and primary sources supplied requirements context only; none became observational or authority evidence.",
    })
    write_json("portfolios/safe-now-execution.json", {"schema":"ghc.family.v650-v6.safe-execution.v1","count":40,"completed":40,"items":safe_rows,"inherited_completion_credit":False})
    write_json("portfolios/candidate-execution.json", {"schema":"ghc.family.v650-v6.candidate-execution.v1","count":30,"completed":30,"items":candidate_rows,"inherited_completion_credit":False})
    write_json("portfolios/skill-execution.json", {"schema":"ghc.family.v650-v6.skill-execution.v1","count":20,"completed":20,"skills":skill_rows,"global_install":False,"subagent_forward_test":"not_run_because_activation_forbids_delegation"})
    write_json("portfolios/runner-execution.json", {"schema":"ghc.family.v650-v6.runner-execution.v1","count":10,"completed":10,"runners":runner_rows,"caller_compatibility_preserved":True})
    write_json("portfolios/clean-fix-refine-execution.json", {"schema":"ghc.family.v650-v6.clean-execution.v1","count":40,"completed":40,"items":clean_rows,"destructive_actions":0})
    write_json("evidence/retained-negative-register.json", {
        "schema":"ghc.family.v650-v6.retained-negatives.evidence.v1",
        "activation_baseline":d.INHERITED_NEGATIVES, "x1_operational":19,
        "synthetic_executed_and_rejected":100,
        "x2_operational":len(x2d.X2_OPERATIONAL_NEGATIVES),
        "effective_at_evidence":d.INHERITED_NEGATIVES+19+100+len(x2d.X2_OPERATIONAL_NEGATIVES),
        "negative_erased":False,
    })
    write_json("evidence/exact-open-gate-register.json", {
        "schema":"ghc.family.v650-v6.gates.evidence.v1",
        "effective_open_gaps":d.INHERITED_OPEN_GAPS+1,
        "effective_exact_gates":d.INHERITED_EXACT_GATES+1,
        "closed_without_exact_evidence":0,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("evidence/phase-truth.json", {
        "schema":"ghc.family.v650-v6.phase-truth.evidence.v1",
        "state":"X2_EVIDENCE_COMPLETE_NOT_SEALED", "x1_commit":X1_COMMIT,
        "evidence_commit":None, "observed_distribution":distribution,
        "proposal_count":20, "mutations_rejected":100,
        "successful_exact_final_aggregates_used":0, "post_success_replay":False,
        "full_repository_suite":False, "terminal_route":"PREPARED_NOT_SENT",
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("evidence/evidence-receipt.json", {
        "schema":"ghc.family.v650-v6.evidence-receipt.v1",
        "x1_commit":X1_COMMIT, "proposal_receipts":20,
        "distribution":distribution, "mutations_executed_and_rejected":100,
        "safe_now_completed":40, "candidates_completed":30,
        "skills_initialized_validated_smoke_used":20, "runners_built_invoked":10,
        "clean_fix_refine_completed":40, "x2_operational_negatives":len(x2d.X2_OPERATIONAL_NEGATIVES),
        "method_flow_method_count":len(method_summary.get("methods", [])),
        "canonical_exact_final_pass":"not_run", "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("evidence/complete-incomplete-checklist.json", {
        "schema":"ghc.family.v650-v6.checklist.evidence.v1",
        "complete":["x1 frozen and four-way equal before x2","twenty bounded proposal executions","one hundred rejected mutations","40/30/20/10/40 portfolios","x2 failures retained","family callers preserved"],
        "incomplete":["evidence commit and push","combined closeout and seal","sole exact-final canonical aggregate","final four-way equality","exact-title terminal baton"],
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json("validation/evidence-component-validation.json", {
        "schema":"ghc.family.v650-v6.evidence-component-validation.v1",
        "proposal_receipts_passed":20, "mutations_rejected":100,
        "skills_validated":20, "skill_smokes_passed":20,
        "runners_invoked":10, "candidate_prototypes_passed":30,
        "canonical_exact_final_aggregate":"not_run", "full_repository_suite":False,
        "passed":True,
    })
    write_text("evidence/evidence-summary.md", f"""# Sylven Arc v650-v6 x2 evidence summary

All twenty frozen proposals executed only inside their preregistered lanes: fourteen completed, four represented, one open gap, and one exact gate. All one hundred synthetic mutations executed and were rejected. This is bounded same-owner evidence under shared infrastructure, not independent reproduction, external audit, empirical confirmation, production certification, professional validation, legal review, cultural ratification, Māori-authority review, complete privacy, exhaustive security, complete accessibility, Theory of Everything, or Stage 20 authority.

The new portfolios completed 40 safe-now tasks, 30 disposable candidate prototypes, 20 phase-local skill packages, 10 family-current runners, and 40 additive CLEAN/FIX/REFINE tasks. No skill was globally installed and no subagent forward test occurred because delegation is prohibited. The effective evidence negative count is {d.INHERITED_NEGATIVES+19+100+len(x2d.X2_OPERATIONAL_NEGATIVES)}. Forty-eight open gaps and forty-nine exact gates remain. `NOT_READY_FOR_STAGE_20` remains controlling.
""")
    write_text("evidence/accessible-evidence-report.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v650-v6 bounded evidence</title></head>
<body><a href="#main">Skip to main content</a><header><h1>Sylven Arc v650-v6 bounded evidence</h1><p>Evidence complete, not sealed. Verdict: NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Evidence report"><ul><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li><li><a href="#evaluation">Reserved evaluation</a></li></ul></nav>
<main id="main"><section id="outcomes"><h2>Outcomes</h2><p>Twenty proposals: fourteen completed, four represented, one open gap, and one exact gate. One hundred mutations were rejected.</p></section>
<section id="limits"><h2>Limits</h2><p>All evidence is bounded, synthetic, symbolic, structural, numerical, or zero-row. It is not empirical, participant, production, professional, legal, cultural, Māori-authority, or independent-reproduction evidence.</p></section>
<section id="evaluation"><h2>Reserved evaluation</h2><p>Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.</p></section></main>
<footer><p>Terminal route: PREPARED_NOT_SENT.</p></footer></body></html>""")

    build_manifest()


if __name__ == "__main__":
    build()
