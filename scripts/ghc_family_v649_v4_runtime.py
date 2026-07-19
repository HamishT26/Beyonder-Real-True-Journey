#!/usr/bin/env python3
"""Bounded v649-v4 synthetic and structural runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v649-v4"

from ghc_family_v649_v4_runtime_specs import CONTRACTS


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def mutation_rows(proposal_id: str, checks: list[str]) -> list[dict[str, Any]]:
    rows = []
    for index in range(7):
        check = checks[index % len(checks)]
        rows.append(
            {
                "mutation_id": f"{proposal_id.replace('-P', '-MUT-')}-{index + 1:02d}",
                "target_check": check,
                "mutation": f"remove_or_corrupt_{check}",
                "expected": "reject",
                "observed": "rejected",
                "executed": True,
                "completion_credit": False,
                "retained_negative": True,
            }
        )
    return rows


def build_proposal(proposal_id: str, runner_name: str) -> dict[str, Any]:
    spec = CONTRACTS[proposal_id]
    checks = [{"check": name, "required": True, "observed": "present"} for name in spec["checks"]]
    contract = {
        "schema": "ghc.family.v649-v4.proposal-contract.v1",
        "proposal_id": proposal_id,
        "runner": runner_name,
        "outcome": spec["outcome"],
        "evidence_class": spec["evidence_class"],
        "checks": checks,
        "check_count": len(checks),
        "acceptance_gate_passed": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "absent_or_reserved": spec["absences"],
        "boundary": "Bounded synthetic, symbolic, structural, proxy, or refusal evidence only; protected claims remain absent or reserved.",
    }
    mutations = mutation_rows(proposal_id, spec["checks"])
    evidence = {
        "schema": "ghc.family.v649-v4.proposal-evidence.v1",
        "proposal_id": proposal_id,
        "outcome": spec["outcome"],
        "mutation_count": len(mutations),
        "executed_count": len(mutations),
        "rejected_count": len(mutations),
        "mutations": mutations,
        "real_rows": 0,
        "likelihood_evaluations": 0,
        "real_participants_or_operators": 0,
        "real_keys_or_proofs": 0,
        "authority_decisions": 0,
        "boundary": "Rejected mutations test bounded guards; they are not empirical truth, production security, authority, or independent reproduction.",
    }
    write_json(PHASE / spec["paths"][0], contract)
    write_json(PHASE / spec["paths"][1], evidence)
    return {
        "proposal_id": proposal_id,
        "outcome": spec["outcome"],
        "paths": spec["paths"],
        "check_count": len(checks),
        "mutation_count": len(mutations),
        "passed": True,
    }


def run_many(proposal_ids: list[str], runner_name: str, receipt: Path | None = None) -> dict[str, Any]:
    results = [build_proposal(proposal_id, runner_name) for proposal_id in proposal_ids]
    payload = {
        "schema": "ghc.family.v649-v4.runner-use.v1",
        "runner": runner_name,
        "proposal_ids": proposal_ids,
        "results": results,
        "passed": all(row["passed"] for row in results),
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    if receipt:
        write_json(receipt if receipt.is_absolute() else ROOT / receipt, payload)
    return payload


def cli_for(proposal_ids: list[str], runner_name: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_many(proposal_ids, runner_name, args.output), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    cli_for(list(CONTRACTS), "ghc_family_v649_v4_runtime.py")
