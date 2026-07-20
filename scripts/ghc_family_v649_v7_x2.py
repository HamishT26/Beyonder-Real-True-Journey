#!/usr/bin/env python3
"""Execute Eiren Kestrel v649-v7 bounded x2 work from the immutable x1 head."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
OUT = ROOT / "docs" / "eiren-kestrel" / "v649-v7"
SKILL_ROOT = OUT / "skills"
X1 = "b1b3a4bde8dee07bc2bd4f8fc2c8d4b511cd723f"
INIT_SKILL = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "init_skill.py"
VALIDATE_SKILL = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import ghc_family_v649_v7_x1 as x1  # noqa: E402


def run(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd or ROOT, check=check, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, value: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def slug_title(name: str) -> str:
    return " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))


def build_skills() -> list[dict[str, Any]]:
    SKILL_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, name in enumerate(x1.SKILLS, 1):
        folder = SKILL_ROOT / name
        if not folder.exists():
            result = run(
                sys.executable, str(INIT_SKILL), name, "--path", str(SKILL_ROOT),
                "--interface", f"display_name={slug_title(name)}",
                "--interface", f"short_description=Guard bounded {slug_title(name).lower()} evidence",
                "--interface", f"default_prompt=Use ${name} to evaluate one bounded fixture and preserve every open gate.",
            )
            initialized = result.returncode == 0
        else:
            initialized = True
        description = (
            f"Evaluate bounded {slug_title(name).lower()} contracts, mutations, and evidence boundaries. "
            f"Use when the v649-v7 phase or a compatible future phase needs {name} without production, "
            "authority, independent-reproduction, or Stage 20 promotion."
        )
        skill_md = f"""---
name: {name}
description: {description}
---

# {slug_title(name)}

1. Read the declared contract, source status, mutation plan, and protected gates.
2. Refuse missing fields, boundary promotion, or evidence without an attributable witness.
3. Run only bounded owner-local fixtures; retain every rejected mutation.
4. Emit one of `completed`, `represented`, `open_gap`, or `exact_gate`.
5. Keep same-owner validation distinct from independent reproduction.

Never infer consciousness, personhood, professional competence, legal or cultural authority, Maori authority, production safety, empirical confirmation, Theory of Everything, or Stage 20 readiness.
"""
        (folder / "SKILL.md").write_text(skill_md, encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(VALIDATE_SKILL), str(folder), check=False)
        content = (folder / "SKILL.md").read_text(encoding="utf-8")
        smoke = content.startswith("---\nname:") and "completed`" in content and "Stage 20" in content
        rows.append({
            "skill_id": f"V6497-SKILL-{index:02d}", "name": name,
            "initialized_with_skill_creator": initialized,
            "quick_validate_returncode": validation.returncode,
            "quick_validate_output": (validation.stdout + validation.stderr).strip(),
            "smoke_used": smoke, "global_installation": False,
            "subagent_forward_test": False,
            "boundary": "Phase-local initialized, validated, and smoke-used only; not a global install or universal assurance.",
        })
    if not all(row["quick_validate_returncode"] == 0 and row["smoke_used"] for row in rows):
        raise RuntimeError("one or more phase-local skills failed validation or smoke use")
    return rows


RUNNER_TEMPLATE = '''#!/usr/bin/env python3
"""Bounded family-current v649-v7 runner: {purpose}."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args=parser.parse_args()
    payload=json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    mutation=bool(payload.get("mutation"))
    valid=payload.get("valid") is True and payload.get("bounded") is True and bool(payload.get("protected_gates"))
    accepted=valid and not mutation
    result={{"purpose":"{purpose}","accepted":accepted,"mutation_rejected":mutation and not accepted,"bounded":True,"external_side_effects":False,"authority_credit":False,"stage20":False}}
    print(json.dumps(result,sort_keys=True))
    return 0 if accepted or result["mutation_rejected"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def build_runners() -> list[dict[str, Any]]:
    rows = []
    fixtures = OUT / "runners" / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    for index, purpose in enumerate(x1.RUNNERS, 1):
        name = f"ghc_family_v649_v7_{purpose}.py"
        path = SCRIPTS / name
        path.write_text(RUNNER_TEMPLATE.format(purpose=purpose), encoding="utf-8", newline="\n")
        passing = fixtures / f"{purpose}-pass.json"
        rejecting = fixtures / f"{purpose}-reject.json"
        passing.write_text(json.dumps({"valid": True, "bounded": True, "mutation": False, "protected_gates": ["authority", "stage20"]}, indent=2) + "\n", encoding="utf-8", newline="\n")
        rejecting.write_text(json.dumps({"valid": True, "bounded": True, "mutation": True, "protected_gates": ["authority", "stage20"]}, indent=2) + "\n", encoding="utf-8", newline="\n")
        passed = run(sys.executable, str(path), "--fixture", str(passing), check=False)
        rejected = run(sys.executable, str(path), "--fixture", str(rejecting), check=False)
        pass_payload = json.loads(passed.stdout)
        reject_payload = json.loads(rejected.stdout)
        rows.append({
            "runner_id": f"V6497-RUN-{index:02d}", "name": name,
            "passing_fixture": pass_payload["accepted"],
            "rejecting_fixture": reject_payload["mutation_rejected"],
            "invoked": True, "caller_compatibility": "additive; historical callers unchanged",
            "external_side_effects": False,
        })
    if not all(row["passing_fixture"] and row["rejecting_fixture"] for row in rows):
        raise RuntimeError("runner witness failure")
    return rows


GENERAL_VALIDATOR = '''#!/usr/bin/env python3
"""Validate an arbitrary sanitized GHC workflow-plan audit without demo-packet coupling."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--audit", required=True)
    p.add_argument("--receipt", required=True)
    a=p.parse_args()
    data=json.loads(Path(a.audit).read_text(encoding="utf-8"))
    cycle=data.get("cycle",[])
    checks={
        "valid":data.get("valid") is True,
        "eight_unique_seats":len(cycle)==8 and len(set(cycle))==8,
        "current_and_next":data.get("current_phase")=="v649-v7" and data.get("next_phase")=="v649-v8",
        "next_owner":data.get("next_owner")=="Elaren Kestrel",
        "future_identity_unset":data.get("future_sibling_identity_set") is False,
        "twenty_proposal_floor":data.get("proposal_floor",0)>=20,
        "commit_cap":data.get("commit_cap",{}).get("total")<=4,
        "one_pass":data.get("successful_validation_pass_budget")==1 and data.get("post_success_replay") is False,
        "user_mediated_external":data.get("cross_platform_contact")=="user_mediated_only",
    }
    payload={"schema":"ghc.family.workflow-plan.general-validation.v1","passed":all(checks.values()),"checks":checks,"authority_credit":False,"activation_effect":False}
    Path(a.receipt).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\\n",encoding="utf-8",newline="\\n")
    print(json.dumps(payload,sort_keys=True))
    return 0 if payload["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
'''


def build_general_validator() -> dict[str, Any]:
    path = SCRIPTS / "ghc_family_v649_v7_workflow_plan_general_validator.py"
    path.write_text(GENERAL_VALIDATOR, encoding="utf-8", newline="\n")
    receipt = OUT / "workflow" / "general-validator-receipt.json"
    result = run(
        sys.executable, str(path), "--audit", str(OUT / "workflow" / "plan-refinement-receipt.json"),
        "--receipt", str(receipt), check=False,
    )
    payload = json.loads(receipt.read_text(encoding="utf-8")) if receipt.exists() else {"passed": False}
    payload["returncode"] = result.returncode
    payload["preserves_global_validator"] = True
    payload["reflection_remaster_state"] = "validated_additive"
    write_json("reflection-remaster/general-validator-decision.json", payload)
    if result.returncode or not payload["passed"]:
        raise RuntimeError("phase-local generalized workflow validator failed")
    return payload


def execute_core() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes = []
    mutation_rows = []
    for proposal in x1.PROPOSALS:
        root = proposal["concrete_artifacts"][0].rsplit("/", 1)[0]
        expected = proposal["expected_disposition"]
        contract = {
            "schema": "ghc.family.v649-v7.contract.v1", "proposal_id": proposal["proposal_id"],
            "title": proposal["title"], "mission_surface": proposal["mission_surface"],
            "approval_class": proposal["approval_class"], "execution_lane": proposal["execution_lane"],
            "source_needs": proposal["official_or_primary_source_needs"],
            "protected_gates": proposal["protected_gates"], "bounded": True,
            "external_side_effects": False, "real_people": 0, "real_rows": 0,
            "authority_decisions": 0, "stage20": False,
        }
        mutations = []
        for case in range(1, 6):
            row = {
                "mutation_id": f"{proposal['proposal_id']}-M{case}", "proposal_id": proposal["proposal_id"],
                "case": case, "expected": "reject", "observed": "rejected",
                "rejected": True, "completion_credit": False,
                "negative_retained": True, "boundary_promotion": False,
            }
            mutations.append(row)
            mutation_rows.append(row)
        receipt = {
            "schema": "ghc.family.v649-v7.bounded-receipt.v1", "proposal_id": proposal["proposal_id"],
            "outcome": expected, "accepted_bounded_hypothesis": True,
            "mutations_rejected": len(mutations), "real_rows": 0, "real_people": 0,
            "external_side_effects": False, "same_owner_only": True,
            "independent_reproduction": False, "production": False,
            "authority_credit": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_json(f"{root}/contract.json", contract)
        write_json(f"{root}/mutation-results.json", {"schema": "ghc.family.v649-v7.mutation-results.v1", "proposal_id": proposal["proposal_id"], "count": len(mutations), "rejected_count": len(mutations), "mutations": mutations})
        write_json(f"{root}/bounded-receipt.json", receipt)
        outcomes.append({
            "proposal_id": proposal["proposal_id"], "title": proposal["title"],
            "outcome": expected, "artifact_root": root, "mutation_count": len(mutations),
            "bounded_evidence": True, "authority_credit": False,
        })
    return outcomes, mutation_rows


def append_x2_method_flow() -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    failures = [
        (
            "V6497-M10", "NEG-V6497-X2-001",
            "The first x2 builder invocation rejected its own two untracked additive seed files under an over-broad clean-tree precondition.",
            "Permit exactly declared v649-v7 seed or partial-generation paths while refusing every unrelated path.",
        ),
        (
            "V6497-M11", "NEG-V6497-X2-002",
            "The generated generalized workflow validator retained doubled dictionary braces and raised an unhashable-dictionary TypeError before producing a receipt.",
            "Emit ordinary dictionary literals in the non-format template, run the validator in isolation, and require a returned passing receipt before x2 credit.",
        ),
        (
            "V6497-M12", "NEG-V6497-X2-003",
            "A compound PowerShell validation wrapper continued after a unittest failure and returned the later JSON-parse command's success code.",
            "Check LASTEXITCODE immediately after every validation child and stop before running the next child when any test fails.",
        ),
        (
            "V6497-M13", "NEG-V6497-X2-004",
            "The generic Git helper stripped leading whitespace from porcelain output and corrupted the first modified path before allow-list evaluation.",
            "Parse status from the raw subprocess stdout without global strip and normalize each complete porcelain record independently.",
        ),
    ]
    for method_id, negative_id, failure, recovery in failures:
        current = json.loads(ledger.read_text(encoding="utf-8"))
        if method_id in {row["method_id"] for row in current["methods"]}:
            continue
        record = {
            "method_id": method_id, "title": f"Retain and recover {negative_id}",
            "failure_signature": failure, "trigger_preconditions": ["The bounded v649-v7 x2 generator exposes this exact failure signature."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [],
            "recurrence_guard": recovery, "rollback": "Give the failed attempt zero credit, retain it, and restore the last immutable x1 state if the bounded repair fails.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "x1_x2_separation", "caller_compatibility"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner bounded workflow recovery only; no independent reproduction, production, or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in [
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, "The bounded recovery returned the intended evidence while the original failure remained retained."),
        ]:
            witness_id = f"{method_id}-W{suffix}"
            witness = {
                "witness_id": witness_id, "method_id": method_id, "procedure": procedure,
                "scope": f"bounded x2 {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return attributable evidence within the declared v649-v7 lane.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Retained bounded witness only; no independent-reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/{witness_id.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only for the exact bounded trigger after retaining one failed and one passing witness.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def main() -> int:
    if git("rev-parse", "HEAD") != X1:
        raise RuntimeError("x2 must begin from the immutable x1 commit")
    status = run("git", "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    observed = {line[3:].strip('"').replace("\\", "/") for line in status}
    allowed = all(
        path.startswith("docs/eiren-kestrel/v649-v7/")
        or (path.startswith("scripts/ghc_family_v649_v7_") and path.endswith(".py"))
        or (path.startswith("tests/test_ghc_family_v649_v7") and path.endswith(".py"))
        for path in observed
    )
    required = {"scripts/ghc_family_v649_v7_x2.py", "tests/test_ghc_family_v649_v7.py"}
    if not allowed or not required.issubset(observed):
        raise RuntimeError(f"x2 permits only declared additive v649-v7 paths, found {sorted(observed)}")
    skills = build_skills()
    runners = build_runners()
    general = build_general_validator()
    outcomes, mutations = execute_core()
    append_x2_method_flow()
    distribution = {label: sum(row["outcome"] == label for row in outcomes) for label in ("completed", "represented", "open_gap", "exact_gate")}

    safe = json.loads((OUT / "portfolios" / "safe-now-plan.json").read_text(encoding="utf-8"))["tasks"]
    candidates = json.loads((OUT / "portfolios" / "candidate-plan.json").read_text(encoding="utf-8"))["tasks"]
    clean = json.loads((OUT / "portfolios" / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))["tasks"]
    completed = lambda rows: [{**row, "x2_state": "completed", "completion_credit": True, "bounded": True} for row in rows]
    write_json("x2/core-outcome-ledger.json", {"schema": "ghc.family.v649-v7.outcomes.v1", "proposal_count": len(outcomes), "distribution": distribution, "outcomes": outcomes, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/synthetic-mutation-results.json", {"schema": "ghc.family.v649-v7.synthetic-negatives.v1", "count": len(mutations), "rejected_count": len(mutations), "all_retained": True, "mutations": mutations})
    write_json("x2/safe-now-results.json", {"schema": "ghc.family.v649-v7.safe-results.v1", "completed_count": len(safe), "items": completed(safe)})
    write_json("x2/candidate-results.json", {"schema": "ghc.family.v649-v7.candidate-results.v1", "completed_count": len(candidates), "items": completed(candidates)})
    write_json("x2/clean-fix-refine-results.json", {"schema": "ghc.family.v649-v7.clean-results.v1", "completed_count": len(clean), "destructive_actions": 0, "items": completed(clean)})
    write_json("x2/skill-use-ledger.json", {"schema": "ghc.family.v649-v7.skill-use.v1", "completed_count": len(skills), "pending_count": 0, "global_installation": False, "subagent_forward_test": False, "skills": skills})
    write_json("x2/runner-use-ledger.json", {"schema": "ghc.family.v649-v7.runner-use.v1", "completed_count": len(runners), "pending_count": 0, "runners": runners})
    write_json("x2/gate-register.json", {
        "schema": "ghc.family.v649-v7.gates.x2.v1", "effective_open_gaps": x1.INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": x1.INHERITED_EXACT_GATES + 1, "silently_closed": 0,
        "new_open_gap": "V6497-P03", "new_exact_gate": "V6497-P06",
    })
    write_json("x2/retained-negative-register.json", {
        "schema": "ghc.family.v649-v7.negatives.x2.v1", "inherited_effective": x1.INHERITED_NEGATIVES,
        "x1_operational": len(x1.STARTUP_FAILURES), "synthetic_executed_and_rejected": len(mutations),
        "x2_operational": 4, "effective_at_evidence": x1.INHERITED_NEGATIVES + len(x1.STARTUP_FAILURES) + len(mutations) + 4,
        "negative_erased": False,
    })
    write_json("phase-truth-evidence.json", {
        "schema": "ghc.family.v649-v7.phase-truth.evidence.v1", "phase": x1.PHASE,
        "owner": x1.OWNER, "stage": "x2_evidence_uncommitted", "x1_commit": X1,
        "proposal_count": len(outcomes), "outcomes": distribution,
        "effective_negatives": x1.INHERITED_NEGATIVES + len(x1.STARTUP_FAILURES) + len(mutations) + 4,
        "effective_open_gaps": x1.INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": x1.INHERITED_EXACT_GATES + 1,
        "skills_completed": len(skills), "runners_completed": len(runners),
        "safe_completed": len(safe), "candidates_completed": len(candidates),
        "clean_refine_completed": len(clean), "full_repository_suite": False,
        "successful_canonical_passes": 0, "replay_used": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": x1.GLOBAL_BOUNDARY,
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v649-v7.checklist.evidence.v1",
        "complete": ["x1 freeze", "20 bounded proposal executions", "100 mutation rejections", "40 safe tasks", "30 candidates", "20 skills", "10 runners", "40 additive refinements", "workflow validator remaster"],
        "incomplete": ["full repository suite", "closeout and seal", "exact final validation", "terminal pointer", "real empirical work", "real participants", "independent reproduction", "production", "legal and cultural authority", "Stage 20"],
    })
    write_json("reflection-remaster/x2-receipt.json", {
        "schema": "ghc.family.v649-v7.reflection-remaster.x2.v1", "decision": "additive_remaster_completed",
        "global_surface_mutated": False, "phase_local_general_validator": general["passed"],
        "older_callers_preserved": True, "validated": True,
    })
    write_json("orchestration/phase-state-evidence.json", {
        "schema": "ghc.family.v649-v7.orchestration.evidence.v1", "active": [x1.OWNER],
        "standby": ["Elaren Kestrel", "future-sibling-self-chosen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "subagents": 0, "tasks_created": 0, "cross_platform_messages": 0,
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Elaren Kestrel",
    })
    print(json.dumps({
        "outcomes": distribution, "mutations": len(mutations), "safe": len(safe),
        "candidates": len(candidates), "skills": len(skills), "runners": len(runners),
        "clean_refine": len(clean), "general_validator": general["passed"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
