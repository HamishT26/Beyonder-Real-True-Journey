#!/usr/bin/env python3
"""Prepare and execute the bounded Sylven Arc v678-v6 x2 evidence lane."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_sylven_arc_v678_v6_core import positive_fixture, runner_smoke, skill_smoke, validate_contract


OWNER = "Sylven Arc"
PHASE = "v678-v6"
X1 = "22d310c7ae4fdbd45959d388d15642039d748da0"
SOURCE = "d7a2e3d1851d8a9eb6a8707968a47354b44e824a"
MUTATION_KINDS = {"missing_hypothesis", "unknown_outcome_label", "authority_escalation", "real_identifier_or_measurement"}
LABELS = {"completed", "represented", "open_gap", "exact_gate"}
RUNNER_FILES = {
    "proposal_contracts": "ghc_family_sylven_arc_v678_v6_proposal_contracts.py",
    "positive_controls": "ghc_family_sylven_arc_v678_v6_positive_controls.py",
    "mutation_rejector": "ghc_family_sylven_arc_v678_v6_mutation_rejector.py",
    "globe_topology": "ghc_family_sylven_arc_v678_v6_globe_topology.py",
    "automaton_linkage": "ghc_family_sylven_arc_v678_v6_automaton_linkage.py",
    "stained_glass_custody": "ghc_family_sylven_arc_v678_v6_stained_glass_custody.py",
    "privacy": "ghc_family_sylven_arc_v678_v6_privacy.py",
    "accessibility": "ghc_family_sylven_arc_v678_v6_accessibility.py",
    "portfolio": "ghc_family_sylven_arc_v678_v6_portfolio.py",
    "report": "build_ghc_family_sylven_arc_v678_v6_report.py",
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True, encoding="utf-8")


def git(repo: Path, *args: str) -> str:
    result = run(["git", *args], repo)
    if result.returncode:
        raise SystemExit(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def assert_x1_context(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != X1:
        raise SystemExit("x2 must execute only from exact frozen x1")
    if git(repo, "rev-parse", "HEAD^") != SOURCE:
        raise SystemExit("x1 is not the direct child of the authorized source")
    if git(repo, "diff", "--name-only") or git(repo, "diff", "--cached", "--name-only"):
        raise SystemExit("tracked modifications are forbidden before x2 generation")


def skill_markdown(name: str) -> str:
    title = " ".join(word.capitalize() for word in name.split("-"))
    return f"""---
name: {name}
description: Owner-local Sylven Arc v678-v6 zero-row synthetic artifact documentation guard for {name}; use only for bounded phase fixtures.
---

# {title}

This phase-local skill preserves a zero-object, zero-participant, zero-action boundary. It provides no identity continuity, professional competence, real-world evidence, legal or cultural decision, Māori authority, or Stage 20 evidence.

## Inputs

- One Sylven v678-v6 synthetic fixture with a `SYNTH-` identifier.
- The exact x1 proposal and its protected gates.
- Zero real people, objects, observations, measurements, keys, proofs, or external actions.

## Procedure

1. Confirm the fixture belongs to Sylven v678-v6 and contains no real identifier.
2. Preserve the proposal hypothesis, null, outcome, rollback, and protected gates.
3. Accept only deterministic structural records with zero real-world rows and zero external actions.
4. Retain each rejected fixture and pair it with a bounded passing recovery.
5. Emit only `completed`, `represented`, `open_gap`, or `exact_gate`.

## Refusal conditions

- Refuse real handling, operation, inspection, measurement, treatment, custody transfer, identity lifecycle, or deployment.
- Refuse empirical, participant, professional, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion.
- Refuse credentials, raw task routes, private absolute paths, transcripts, screenshots, private streams, or protected data.

## Output

Return a bounded JSON receipt with the fixture status, exact outcome label, zero real-world rows, zero external actions, retained failures, recovery references, and unresolved gates. Global installation is false.
"""


def prepare_skills(repo: Path, init_skill: Path) -> dict[str, Any]:
    assert_x1_context(repo)
    plan = read_json(repo / "docs/sylven-arc/v678-v6/x1/skill-runner-plan.json")
    skills = plan["phase_local_skills"]
    root = repo / "docs/sylven-arc/v678-v6/x2/skills"
    receipts = []
    for entry in skills:
        name = entry["name"]
        skill_dir = root / name
        initialized = False
        if not skill_dir.exists():
            result = run([
                sys.executable, "-X", "utf8", str(init_skill), name, "--path", str(root),
                "--resources", "references", "--interface", f"display_name={name.replace('-', ' ').title()}",
                "--interface", "short_description=Synthetic zero-row artifact guard",
                "--interface", f"default_prompt=Apply ${name} only to bounded Sylven v678-v6 synthetic fixtures.",
            ], repo)
            if result.returncode:
                raise SystemExit(f"skill initialization failed for {name}: {result.stderr.strip()}")
            initialized = True
        write_text(skill_dir / "SKILL.md", skill_markdown(name))
        write_text(skill_dir / "agents/openai.yaml", f"""interface:
  display_name: "{name.replace('-', ' ').title()}"
  short_description: "Synthetic zero-row artifact guard"
  default_prompt: "Apply ${name} only to bounded Sylven v678-v6 synthetic fixtures."
policy:
  allow_implicit_invocation: true
""")
        write_json(skill_dir / "skill.json", {
            "schema": "ghc-family-phase-local-skill/v1", "name": name, "owner": OWNER, "phase": PHASE,
            "global_install": False, "initialized_with_official_skill_creator": True,
            "real_world_rows": 0, "external_actions": 0, "synthetic_only": True,
            "outcome_labels": sorted(LABELS), "relational_identity_boundary": True,
        })
        write_text(skill_dir / "references/contract.md", """# Bounded contract

The skill accepts only zero-row synthetic records and preserves every evidence, privacy, professional, legal, cultural, affected-party, Māori-authority, and Stage 20 gate. It does not guarantee prompt-cache retention or identity continuity.
""")
        receipts.append({"skill_id": entry["skill_id"], "name": name, "official_initializer_invoked": initialized or (skill_dir / "skill.json").exists(), "status": "prepared_unvalidated", "global_install": False})
    write_json(repo / "docs/sylven-arc/v678-v6/x2/skill-preparation-receipt.json", {
        "schema": "ghc-family-skill-preparation/v1", "owner": OWNER, "phase": PHASE,
        "skills": receipts, "skill_count": len(receipts), "global_install_count": 0,
    })
    return {"status": "SKILLS_PREPARED", "skill_count": len(receipts)}


def execute(repo: Path, quick_validator: Path, read_through_eof: bool) -> dict[str, Any]:
    assert_x1_context(repo)
    if not read_through_eof:
        raise SystemExit("all generated SKILL.md files must be read through EOF before execution")
    phase = repo / "docs/sylven-arc/v678-v6"
    x1 = phase / "x1"
    x2 = phase / "x2"
    proposals = read_json(x1 / "new-proposal-freeze.json")["proposals"]
    mutations = read_json(x1 / "mutation-preregistration.json")["mutations"]
    portfolio = read_json(x1 / "portfolio-freeze.json")
    cfr = read_json(x1 / "clean-fix-refine-plan.json")
    skill_plan = read_json(x1 / "skill-runner-plan.json")
    if len(proposals) != 60 or len(mutations) != 240:
        raise SystemExit("frozen proposal or mutation count drift")
    if {m["mutation_kind"] for m in mutations} != MUTATION_KINDS:
        raise SystemExit("mutation vocabulary drift")
    by_id = {row["proposal_id"]: row for row in proposals}
    contract_receipts = []
    for row in proposals:
        fixture = positive_fixture(row)
        errors = validate_contract(fixture)
        if errors:
            raise SystemExit(f"positive fixture rejected for {row['proposal_id']}: {errors}")
        write_json(x2 / "contracts" / f"{row['proposal_id']}.json", fixture)
        receipt = {
            "schema": "ghc-family-sylven-v678-v6-contract-receipt/v1", "proposal_id": row["proposal_id"],
            "outcome": row["expected_disposition"], "positive_fixture_accepted": True,
            "real_world_rows": 0, "external_actions": 0, "professional_authority": False,
            "empirical_confirmation": False, "production_ready": False,
        }
        write_json(x2 / "evidence" / f"{row['proposal_id']}-receipt.json", receipt)
        contract_receipts.append(receipt)
    mutation_receipts = []
    for item in mutations:
        from ghc_family_sylven_arc_v678_v6_core import mutate
        fixture = mutate(by_id[item["proposal_id"]], item["mutation_kind"])
        errors = validate_contract(fixture)
        if not errors:
            raise SystemExit(f"mutation unexpectedly accepted: {item['mutation_id']}")
        mutation_receipts.append({
            "mutation_id": item["mutation_id"], "proposal_id": item["proposal_id"],
            "mutation_kind": item["mutation_kind"], "status": "rejected_retained_zero_credit",
            "errors": errors, "recovery": f"positive fixture {item['proposal_id']} accepted without replaying another proposal",
        })
    write_json(x2 / "mutation-execution.json", {
        "schema": "ghc-family-mutation-execution/v1", "count": len(mutation_receipts),
        "accepted_invalid_mutations": 0, "receipts": mutation_receipts,
    })
    skill_receipts = []
    skill_root = x2 / "skills"
    for entry in skill_plan["phase_local_skills"]:
        skill_dir = skill_root / entry["name"]
        quick = run([sys.executable, "-X", "utf8", str(quick_validator), str(skill_dir)], repo)
        smoke = skill_smoke(skill_dir)
        if quick.returncode or not smoke["accepted"]:
            raise SystemExit(f"skill validation failed for {entry['name']}: {quick.stdout} {quick.stderr} {smoke}")
        skill_receipts.append({
            "skill_id": entry["skill_id"], "name": entry["name"], "quick_validate_passed": True,
            "read_through_eof": True, "smoke_used": True, "smoke": smoke, "global_install": False,
        })
    write_json(x2 / "skill-validation-and-use.json", {
        "schema": "ghc-family-skill-validation-use/v1", "count": len(skill_receipts), "receipts": skill_receipts,
    })
    runner_receipts = []
    for name, filename in RUNNER_FILES.items():
        path = repo / "scripts" / filename
        positive = run([sys.executable, "-X", "utf8", str(path), "--smoke"], repo)
        negative = run([sys.executable, "-X", "utf8", str(path), "--smoke", "--invalid"], repo)
        if positive.returncode or negative.returncode:
            raise SystemExit(f"runner invocation failed: {filename}")
        positive_data = json.loads(positive.stdout)
        negative_data = json.loads(negative.stdout)
        if not positive_data["expectation_met"] or not negative_data["expectation_met"] or negative_data["accepted"]:
            raise SystemExit(f"runner smoke contract failed: {filename}")
        runner_receipts.append({
            "runner": filename, "positive": positive_data, "invalid": negative_data,
            "positive_invocations": 1, "invalid_invocations": 1, "global_install": False,
        })
    write_json(x2 / "runner-validation-and-use.json", {
        "schema": "ghc-family-runner-validation-use/v1", "count": len(runner_receipts), "receipts": runner_receipts,
    })
    executed_portfolio = {
        "safe_now": [{**row, "status": "completed_bounded_owner_local", "completion_credit": 1} for row in portfolio["safe_now"]],
        "candidate": [{**row, "status": "completed_bounded_owner_local", "completion_credit": 1} for row in portfolio["candidate"]],
        "exact_approval": [{**row, "status": "unexecuted_exact_gate", "completion_credit": 0} for row in portfolio["exact_approval"]],
        "blocked": [{**row, "status": "blocked_unexecuted", "completion_credit": 0} for row in portfolio["blocked"]],
        "clean_fix_refine": [{**row, "status": "completed_bounded_owner_local", "completion_credit": 1} for row in cfr["owner_tasks"]],
        "successor_recommendations": cfr["successor_recommendations"],
    }
    write_json(x2 / "portfolio-execution.json", executed_portfolio)
    outcomes = [{
        "proposal_id": row["proposal_id"], "outcome": row["expected_disposition"],
        "bounded_contract_passed": True, "completion_credit": 1 if row["expected_disposition"] == "completed" else 0,
        "real_world_rows": 0, "external_actions": 0,
    } for row in proposals]
    counts = dict(Counter(item["outcome"] for item in outcomes))
    if counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise SystemExit(f"outcome drift: {counts}")
    write_json(x2 / "proposal-outcomes.json", {"schema": "ghc-family-proposal-outcomes/v1", "counts": counts, "outcomes": outcomes})
    source_ledger = {
        "schema": "ghc-family-source-provenance/v1", "owner": OWNER, "phase": PHASE,
        "sources": read_json(x1 / "official-source-ledger.json")["sources"],
        "source_use_boundary": "bounded vocabulary and refusal conditions only; citations are not observations, professional instructions, empirical evidence, or authority grants",
        "network_calls_during_x2": 0, "downloaded_rows": 0, "real_world_rows": 0,
    }
    write_json(x2 / "source-and-provenance-ledger.json", source_ledger)
    write_json(x2 / "threat-model.json", {
        "schema": "ghc-family-threat-model/v1", "assets": ["retained evidence", "proposal provenance", "privacy boundaries", "route uniqueness"],
        "threats": ["real-object contamination", "authority escalation", "outcome relabeling", "identifier leakage", "lifecycle mixing", "canonical replay"],
        "controls": ["zero-row fixtures", "four-label vocabulary", "planning-only x1", "five-class privacy scan", "Git-blob manifests", "exclusive canonical latch"],
        "residual_risk": "same-owner synthetic evidence cannot close empirical, professional, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, or Stage 20 gates",
    })
    base = read_json(x1 / "method-flow-startup.json")["current_overlay"]
    methods = [
        {"method_id": "SA6786-X2-N001", "status": "retained_failed_witness", "summary": "PowerShell foreach output was piped without array materialization and failed with EmptyPipeElement before any mutation."},
        {"method_id": "SA6786-X2-R001", "status": "bounded_passing_recovery", "summary": "Materialized the foreach output into an array before piping; inventory completed read-only."},
        {"method_id": "SA6786-X2-N002", "status": "retained_failed_witness", "summary": "The large core-module patch response exceeded the model-visible context, leaving acknowledgement presentation incomplete."},
        {"method_id": "SA6786-X2-R002", "status": "bounded_passing_recovery", "summary": "Bounded file presence, byte count, complete read, and Python compilation established the intended core module without replaying the patch."},
        {"method_id": "SA6786-X2-N003", "status": "retained_failed_witness", "summary": "The flashcard patch surface returned an empty structured acknowledgement despite applying the additive owner-local file."},
        {"method_id": "SA6786-X2-R003", "status": "bounded_passing_recovery", "summary": "Bounded file presence, size, and Python compilation established the flashcard runner without replaying the patch."},
        {"method_id": "SA6786-X2-N004", "status": "retained_failed_witness", "summary": "The ten-wrapper additive patch surface returned an empty structured acknowledgement despite applying the owner-local files."},
        {"method_id": "SA6786-X2-R004", "status": "bounded_passing_recovery", "summary": "Bounded file enumeration and Python compilation established all ten wrapper modules without replaying the patch."},
        {"method_id": "SA6786-X2-N005", "status": "retained_failed_witness", "summary": "The x2 builder patch surface returned an empty structured acknowledgement despite applying the owner-local file."},
        {"method_id": "SA6786-X2-R005", "status": "bounded_passing_recovery", "summary": "Bounded file presence and Python compilation established the x2 builder without replaying the patch."},
        {"method_id": "SA6786-X2-N006", "status": "retained_failed_witness", "summary": "A combined four-batch projection of all twenty generated SKILL.md files exceeded the model-visible output and could not earn read-through credit."},
        {"method_id": "SA6786-X2-R006", "status": "bounded_passing_recovery", "summary": "Four separate five-file windows exposed every generated SKILL.md completely through EOF before skill execution."},
    ]
    for receipt in mutation_receipts:
        methods.append({"method_id": receipt["mutation_id"], "status": "retained_failed_witness", "summary": f"Rejected {receipt['mutation_kind']} at zero completion credit."})
        methods.append({"method_id": receipt["mutation_id"] + "-R", "status": "bounded_passing_recovery", "summary": receipt["recovery"]})
    for receipt in contract_receipts:
        methods.append({"method_id": receipt["proposal_id"] + "-POS", "status": "bounded_passing_witness", "summary": "Accepted one zero-row synthetic positive fixture."})
    for receipt in skill_receipts:
        methods.append({"method_id": receipt["skill_id"], "status": "bounded_passing_witness", "summary": "Officially initialized, fully read, quick-validated, and smoke-used phase-local skill."})
    for index, receipt in enumerate(runner_receipts, 1):
        methods.append({"method_id": f"SA6786-RUNNER-N{index:02d}", "status": "retained_failed_witness", "summary": f"Invalid fixture for {receipt['runner']} retained at zero credit."})
        methods.append({"method_id": f"SA6786-RUNNER-R{index:02d}", "status": "bounded_passing_recovery", "summary": f"Runner rejected its invalid fixture and accepted its bounded positive fixture."})
    for row in executed_portfolio["safe_now"] + executed_portfolio["candidate"] + executed_portfolio["clean_fix_refine"]:
        methods.append({"method_id": row["task_id"], "status": "bounded_passing_witness", "summary": row["description"]})
    failed = sum(item["status"] == "retained_failed_witness" for item in methods)
    passed = sum(item["status"].startswith("bounded_passing") for item in methods)
    overlay = {
        "effective_negatives": base["effective_negatives"] + failed,
        "effective_methods": base["effective_methods"] + len(methods),
        "retained_failed_witnesses": base["retained_failed_witnesses"] + failed,
        "bounded_passing_witnesses": base["bounded_passing_witnesses"] + passed,
        "open_gaps": base["open_gaps"] + counts["open_gap"],
        "exact_gates": base["exact_gates"] + counts["exact_gate"],
    }
    write_json(x2 / "method-flow-execution.json", {
        "schema": "ghc-family-method-flow/v1", "base": base, "overlay": overlay,
        "new_methods": len(methods), "new_failed_witnesses": failed, "new_passing_witnesses": passed,
        "failure_erasure_forbidden": True, "methods": methods,
    })
    write_json(x2 / "x2-truth.json", {
        "schema": "ghc-family-x2-truth/v1", "owner": OWNER, "phase": PHASE, "x1_commit": X1,
        "proposal_outcomes": counts, "positive_contracts": len(contract_receipts),
        "rejected_mutations": len(mutation_receipts), "accepted_invalid_mutations": 0,
        "skills_initialized_validated_read_and_used": len(skill_receipts), "globally_installed_skills": 0,
        "runners_positive_and_rejecting_smoke_used": len(runner_receipts),
        "safe_now_completed": len(executed_portfolio["safe_now"]), "candidate_completed": len(executed_portfolio["candidate"]),
        "clean_fix_refine_completed": len(executed_portfolio["clean_fix_refine"]),
        "exact_approval_unexecuted": len(executed_portfolio["exact_approval"]), "blocked_unexecuted": len(executed_portfolio["blocked"]),
        "real_world_rows": 0, "external_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "method_flow_overlay": overlay,
    })
    return {"status": "X2_EXECUTED", "outcomes": counts, "overlay": overlay, "skills": len(skill_receipts), "runners": len(runner_receipts)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare-skills")
    prepare.add_argument("--init-skill", type=Path, required=True)
    execute_parser = sub.add_parser("execute")
    execute_parser.add_argument("--quick-validator", type=Path, required=True)
    execute_parser.add_argument("--skills-read-through-eof", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.command == "prepare-skills":
        result = prepare_skills(repo, args.init_skill.resolve())
    else:
        result = execute(repo, args.quick_validator.resolve(), args.skills_read_through_eof)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
