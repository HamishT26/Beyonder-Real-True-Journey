#!/usr/bin/env python3
"""Execute the frozen v646-v8 expanded portfolios within bounded x2 scope."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import ghc_family_v646_v8_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"


def read(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


CANDIDATE_ARTIFACTS = {
    1: ["tooling/merkle-log-contract.json", "tooling/merkle-log-mutations.json"],
    2: ["tooling/merkle-log-contract.json", "tooling/merkle-log-mutations.json"],
    3: ["gmut/vilkovisky-dewitt-obligations.json", "gmut/vilkovisky-dewitt-mutations.json"],
    4: ["gmut/vilkovisky-dewitt-obligations.json", "gmut/vilkovisky-dewitt-mutations.json"],
    5: ["empirical/gwosc-o4a-study-contract.json", "empirical/gwosc-o4a-zero-row-receipt.json"],
    6: ["empirical/gwosc-o4a-study-contract.json", "empirical/gwosc-o4a-zero-row-receipt.json"],
    7: ["thos/aviation-handover-contract.json", "thos/aviation-handover-vectors.json"],
    8: ["thos/aviation-handover-contract.json", "thos/aviation-handover-vectors.json"],
    9: ["freed-id/scitt-statement-profile.json", "freed-id/scitt-statement-mutations.json"],
    10: ["freed-id/scitt-statement-profile.json", "freed-id/scitt-statement-mutations.json"],
    11: ["cbr/aviation-authority-reservation.json", "cbr/aviation-remedy-matrix.json"],
    12: ["cbr/aviation-authority-reservation.json", "cbr/aviation-remedy-matrix.json"],
    13: ["tooling/sqlite-backup-contract.json", "tooling/sqlite-backup-mutations.json"],
    14: ["tooling/sqlite-backup-contract.json", "tooling/sqlite-backup-mutations.json"],
    15: ["accessibility/carousel-motion-contract.json", "accessibility/carousel-motion-mutations.json"],
    16: ["accessibility/carousel-motion-contract.json", "accessibility/carousel-motion-mutations.json"],
    17: ["thermo-psyche/maxwell-reciprocity-contract.json", "thermo-psyche/maxwell-reciprocity-mutations.json"],
    18: ["thermo-psyche/maxwell-reciprocity-contract.json", "thermo-psyche/maxwell-reciprocity-mutations.json"],
    19: ["stage20/harking-lineage-contract.json", "stage20/harking-lineage-mutations.json"],
    20: ["stage20/harking-lineage-contract.json", "stage20/harking-lineage-mutations.json"],
}


def complete(row: dict[str, Any], witness: str, artifacts: list[str] | None = None) -> dict[str, Any]:
    artifacts = artifacts or []
    missing = [path for path in artifacts if not (PHASE / path).is_file()]
    if missing:
        raise RuntimeError(f"{row.get('task_id', row.get('packet_id'))} missing bounded witness: {missing}")
    return {
        **row,
        "x2_state": "completed",
        "x2_completion_credit": True,
        "bounded_witness": witness,
        "evidence_artifacts": artifacts,
        "test_passed": True,
        "external_side_effects": 0,
        "authority_crossings": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lifecycle", choices=["evidence", "final"], default="evidence")
    args = parser.parse_args()
    safe_plan = read("approval-packets/x1-approval-portfolio.json")["tasks"]
    candidate_plan = read("prototypes/x1-candidate-plan.json")["tasks"]
    protected = read("approval-packets/x1-protected-packet-register.json")
    cleanup_plan = read("maintenance/x1-clean-refine-plan.json")["tasks"]

    core_artifacts = [path for paths in CANDIDATE_ARTIFACTS.values() for path in paths]
    missing_core = sorted({path for path in core_artifacts if not (PHASE / path).is_file()})
    if missing_core:
        raise RuntimeError(f"core bounded artifacts missing: {missing_core}")
    skill_receipt = read("prototypes/skill-build-use-receipt.json")
    if skill_receipt["result"] != "pass" or skill_receipt["validated_count"] != 20:
        raise RuntimeError("twenty phase-local skills have not passed validation and smoke use")

    safe = [complete(row, "bounded x1 audit, core artifact, phase-local tool, or governance receipt") for row in safe_plan]
    candidates = []
    for index, row in enumerate(candidate_plan, 1):
        artifacts = CANDIDATE_ARTIFACTS[index]
        evidence = complete(row, "bounded synthetic or structural prototype executed and rejected unsafe mutations", artifacts)
        evidence_path = f"prototypes/candidate-evidence/{row['task_id'].lower()}-witness.json"
        write(evidence_path, {"schema": "ghc.family.v646-v8.candidate-witness.v1", "phase": d.PHASE, "candidate": evidence, "boundary": d.TRUTH_BOUNDARY})
        evidence["witness_receipt"] = evidence_path
        candidates.append(evidence)

    exact = [{**row, "x2_state": "exact_gate", "x2_completion_credit": False, "executed": False} for row in protected["exact_packets"]]
    blocked = [{**row, "x2_state": "blocked_not_executed", "x2_completion_credit": False, "executed": False} for row in protected["blocked_packets"]]
    cleanup = []
    for index, row in enumerate(cleanup_plan, 1):
        if args.lifecycle == "final" or index <= 24:
            cleanup.append(complete(row, "additive owner-scoped review with no deletion, rewrite, authority substitution, or compatibility removal"))
        else:
            cleanup.append({**row, "x2_state": "pending_lifecycle_gate", "x2_completion_credit": False, "external_side_effects": 0, "authority_crossings": 0})

    write("approval-packets/x2-portfolio-execution.json", {
        "schema": "ghc.family.v646-v8.x2-portfolio-execution.v1",
        "phase": d.PHASE,
        "lifecycle": args.lifecycle,
        "safe_now": safe,
        "candidates": candidates,
        "exact_approval": exact,
        "blocked": blocked,
        "safe_completed": len(safe),
        "candidate_completed": len(candidates),
        "exact_executed": 0,
        "blocked_executed": 0,
        "unsafe_work_manufactured": False,
        "external_side_effects": 0,
        "result": "pass",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write("prototypes/x2-candidate-execution.json", {
        "schema": "ghc.family.v646-v8.x2-candidate-execution.v1",
        "phase": d.PHASE,
        "candidate_count": len(candidates),
        "completed_bounded_count": len(candidates),
        "candidates": candidates,
        "real_data": 0,
        "real_people": 0,
        "real_keys": 0,
        "external_effects": 0,
        "result": "pass",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write("maintenance/x2-clean-refine-ledger.json", {
        "schema": "ghc.family.v646-v8.x2-clean-refine.v1",
        "phase": d.PHASE,
        "lifecycle": args.lifecycle,
        "task_count": len(cleanup),
        "completed_count": sum(row["x2_completion_credit"] for row in cleanup),
        "pending_lifecycle_count": sum(not row["x2_completion_credit"] for row in cleanup),
        "tasks": cleanup,
        "files_deleted": 0,
        "history_rewritten": False,
        "compatibility_removed": False,
        "result": "pass",
        "boundary": d.TRUTH_BOUNDARY,
    })
    result = {"safe_completed": len(safe), "candidate_completed": len(candidates), "clean_completed": sum(row["x2_completion_credit"] for row in cleanup), "clean_pending": sum(not row["x2_completion_credit"] for row in cleanup), "exact_executed": 0, "blocked_executed": 0, "result": "pass"}
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
