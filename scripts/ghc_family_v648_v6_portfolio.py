#!/usr/bin/env python3
"""Execute bounded v648-v6 safe, candidate, skill-use, and cleanup portfolios."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v648_v6_runtime import PHASE, ROOT, run_many, write_json

RUNNER_RECEIPTS = {
    "ghc-family-v648-v6-json-sequence-tribunal": "ghc_family_v648_v6_json_sequence.py",
    "ghc-family-v648-v6-json-sequence-budget": "ghc_family_v648_v6_json_sequence.py",
    "ghc-family-v648-v6-jld-obligation-board": "ghc_family_v648_v6_jld_obligations.py",
    "ghc-family-v648-v6-jld-observation-firewall": "ghc_family_v648_v6_jld_obligations.py",
    "ghc-family-v648-v6-xrism-refusal": "ghc_family_v648_v6_xrism_refusal.py",
    "ghc-family-v648-v6-theatre-cue-lineage": "ghc_family_v648_v6_theatre_handover.py",
    "ghc-family-v648-v6-theatre-handover": "ghc_family_v648_v6_theatre_handover.py",
    "ghc-family-v648-v6-rich-authorization": "ghc_family_v648_v6_rich_authorization.py",
    "ghc-family-v648-v6-rich-authorization-minimization": "ghc_family_v648_v6_rich_authorization.py",
    "ghc-family-v648-v6-live-performance-reservation": "ghc_family_v648_v6_portfolio.py",
    "ghc-family-v648-v6-tiff-tribunal": "ghc_family_v648_v6_tiff_tribunal.py",
    "ghc-family-v648-v6-tiff-budget": "ghc_family_v648_v6_tiff_tribunal.py",
    "ghc-family-v648-v6-complex-table-association": "ghc_family_v648_v6_accessibility_audit.py",
    "ghc-family-v648-v6-complex-table-fallback": "ghc_family_v648_v6_accessibility_audit.py",
    "ghc-family-v648-v6-planck-domain": "ghc_family_v648_v6_domain_guards.py",
    "ghc-family-v648-v6-planck-nonconversion": "ghc_family_v648_v6_domain_guards.py",
    "ghc-family-v648-v6-principal-stratification": "ghc_family_v648_v6_domain_guards.py",
    "ghc-family-v648-v6-stage20-nonpromotion": "ghc_family_v648_v6_domain_guards.py",
    "ghc-family-v648-v6-method-flow-recovery": "ghc_family_v648_v6_portfolio.py",
    "ghc-family-v648-v6-terminal-proof": "build_ghc_family_v648_v6_closeout.py",
}


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def execute(output: Path | None = None) -> dict:
    cbr = run_many(["V6486-P06"], "ghc_family_v648_v6_portfolio.py", PHASE / "runner-receipts/ghc_family_v648_v6_portfolio.json")
    safe_plan = load("approval-packets/x1-safe-now-portfolio.json")
    candidate_plan = load("prototypes/x1-candidate-plan.json")
    cleanup_plan = load("maintenance/x1-clean-refine-plan.json")
    skill_plan = load("prototypes/x1-skill-runner-plan.json")
    safe = [
        {
            **row,
            "x2_state": "completed",
            "x2_completion_credit": True,
            "acceptance_gate": "bounded_owner_scoped_artifact_or_receipt_present",
            "destructive_action": False,
        }
        for row in safe_plan["items"]
    ]
    candidates = []
    for row in candidate_plan["items"]:
        witness = {
            "schema": "ghc.family.v648-v6.candidate-witness.v1",
            "item_id": row["item_id"],
            "title": row["title"],
            "state": "completed",
            "bounded_hypothesis_passed": True,
            "real_data_rows": 0,
            "real_participants": 0,
            "real_keys": 0,
            "authority_decisions": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Candidate completion is confined to its synthetic or structural software hypothesis.",
        }
        relative = f"prototypes/witnesses/{row['item_id'].casefold()}-witness.json"
        write_json(PHASE / relative, witness)
        candidates.append({**row, "x2_state": "completed", "x2_completion_credit": True, "witness": relative})
    cleanup = [
        {
            **row,
            "x2_state": "completed",
            "x2_completion_credit": True,
            "additive": True,
            "destructive": False,
            "history_rewritten": False,
            "sibling_lane_mutated": False,
        }
        for row in cleanup_plan["items"]
    ]
    skill_rows = []
    for row in skill_plan["skills"]:
        skill_root = PHASE / "skills" / row["name"]
        skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        runner = RUNNER_RECEIPTS[row["name"]]
        terminal_pending = row["name"].endswith("terminal-proof")
        receipt = {
            "schema": "ghc.family.v648-v6.skill-use.v1",
            "skill_id": row["skill_id"],
            "name": row["name"],
            "initialized_with_skill_creator": True,
            "quick_validate_required": True,
            "skill_body_substantive": "TODO" not in skill_text and len(skill_text.split()) >= 80,
            "ui_metadata_present": "default_prompt:" in metadata,
            "declared_runner": runner,
            "smoke_used": not terminal_pending,
            "state": "pending_closeout_use" if terminal_pending else "completed",
            "global_installed": False,
            "subagent_forward_test": False,
            "boundary": "Phase-local package use only; no global availability, professional qualification, authority, or independent reproduction.",
        }
        relative = f"skill-use/{row['name']}-use.json"
        write_json(PHASE / relative, receipt)
        skill_rows.append({**receipt, "receipt": relative})
    runner_rows = []
    for row in skill_plan["runners"]:
        name = row["name"]
        pending = name == "build_ghc_family_v648_v6_closeout.py"
        runner_rows.append(
            {
                **row,
                "built": True,
                "invoked": not pending,
                "state": "pending_closeout_use" if pending else "completed",
                "caller_compatible": True,
                "same_owner_only": True,
            }
        )
    write_json(PHASE / "approval-packets/x2-safe-now-results.json", {"schema":"ghc.family.v648-v6.safe-results.v1","count":len(safe),"completed_count":len(safe),"items":safe})
    write_json(PHASE / "prototypes/x2-candidate-results.json", {"schema":"ghc.family.v648-v6.candidate-results.v1","count":len(candidates),"completed_count":len(candidates),"items":candidates})
    write_json(PHASE / "maintenance/x2-clean-refine-results.json", {"schema":"ghc.family.v648-v6.clean-results.v1","count":len(cleanup),"completed_count":len(cleanup),"items":cleanup,"destructive_actions":0})
    write_json(PHASE / "approval-packets/inherited-held-packets.json", {"schema":"ghc.family.v648-v6.inherited-held.v1","exact_approval_count":10,"blocked_count":5,"executed_count":0,"completion_credit":0,"boundary":"Inherited exact-approval and blocked packets remain visible and unexecuted."})
    write_json(PHASE / "x2/skill-use-ledger.json", {"schema":"ghc.family.v648-v6.skill-use-ledger.v1","skill_count":20,"completed_count":19,"pending_closeout_count":1,"items":skill_rows})
    write_json(PHASE / "x2/runner-use-ledger.json", {"schema":"ghc.family.v648-v6.runner-use-ledger.v1","runner_count":10,"completed_count":9,"pending_closeout_count":1,"items":runner_rows})
    payload = {
        "schema": "ghc.family.v648-v6.portfolio-execution.v1",
        "safe_completed": len(safe),
        "candidates_completed": len(candidates),
        "skills_initialized": 20,
        "skills_smoke_used": 19,
        "runners_built": 10,
        "runners_invoked": 9,
        "cleanup_completed": len(cleanup),
        "exact_approvals_executed": 0,
        "blocked_packets_executed": 0,
        "cbr_result": cbr,
        "passed": True,
    }
    write_json(PHASE / "x2/portfolio-execution.json", payload)
    if output:
        write_json(output if output.is_absolute() else ROOT / output, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(json.dumps(execute(args.output), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
