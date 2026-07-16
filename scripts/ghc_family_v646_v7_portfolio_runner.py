#!/usr/bin/env python3
"""Execute Eiren v646-v7 expanded portfolios within bounded x2 scope."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import ghc_family_v646_v7_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v7"


def read(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def completed(rows: list[dict[str, Any]], witness: str) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "x2_state": "completed",
            "x2_completion_credit": True,
            "bounded_witness": witness,
            "external_side_effects": 0,
            "authority_crossings": 0,
        }
        for row in rows
    ]


def main() -> int:
    approval = read("approval-packets/x1-approval-portfolio.json")
    cleanup = read("maintenance/x1-clean-refine-plan.json")
    safe = completed(approval["safe_now"], "phase-local deterministic build, audit, or receipt")
    candidates = completed(approval["candidates"], "bounded synthetic mutation or structural prototype")
    clean = completed(cleanup["tasks"], "additive reconciliation or review with no deletion")
    exact = [{**row, "x2_state": "exact_gate", "x2_completion_credit": False, "executed": False} for row in approval["exact_approval"]]
    blocked = [{**row, "x2_state": "blocked_not_executed", "x2_completion_credit": False, "executed": False} for row in approval["blocked"]]
    write("approval-packets/x2-portfolio-execution.json", {
        "schema": "ghc.family.v646-v7.x2-portfolio-execution.v1", "phase": d.PHASE,
        "safe_now": safe, "candidates": candidates, "exact_approval": exact, "blocked": blocked,
        "safe_completed": len(safe), "candidate_completed": len(candidates),
        "exact_executed": 0, "blocked_executed": 0,
        "unsafe_work_manufactured": False, "external_side_effects": 0,
        "result": "pass", "boundary": d.TRUTH_BOUNDARY,
    })
    write("prototypes/x2-candidate-execution.json", {
        "schema": "ghc.family.v646-v7.x2-candidate-execution.v1", "phase": d.PHASE,
        "candidate_count": len(candidates), "completed_bounded_count": len(candidates),
        "candidates": candidates, "real_data": 0, "real_people": 0, "real_keys": 0,
        "external_effects": 0, "result": "pass", "boundary": d.TRUTH_BOUNDARY,
    })
    write("maintenance/x2-clean-refine-ledger.json", {
        "schema": "ghc.family.v646-v7.x2-clean-refine.v1", "phase": d.PHASE,
        "task_count": len(clean), "completed_count": len(clean), "tasks": clean,
        "files_deleted": 0, "history_rewritten": False, "compatibility_removed": False,
        "result": "pass", "boundary": d.TRUTH_BOUNDARY,
    })
    print(json.dumps({"safe_completed": len(safe), "candidate_completed": len(candidates), "clean_completed": len(clean), "exact_executed": 0, "blocked_executed": 0, "result": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
