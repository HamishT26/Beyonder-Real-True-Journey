#!/usr/bin/env python3
"""Validate v645-v3 research, approval, skill, runner, and clean portfolios."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

EXPECTED_APPROVAL = {
    "eiren_safe_now": 15, "successor_safe_now_seeds": 15,
    "eiren_candidate_prototypes": 10, "successor_candidate_seeds": 10,
    "eiren_exact_approval": 10, "eiren_blocked": 5,
}
EXPECTED_SKILLS = {"eiren_skills_to_build": 10, "successor_skill_ideas": 10, "eiren_runners_to_build": 5, "successor_runner_ideas": 5}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def validate(phase_dir: Path) -> dict:
    research = load(phase_dir / "x1-proposals.json")
    approval = load(phase_dir / "approval-packets/x1-approval-portfolio.json")
    skills = load(phase_dir / "prototypes/x1-skill-runner-plan.json")
    clean = load(phase_dir / "maintenance/x1-clean-refine-plan.json")
    proposals = research["proposals"]
    packet_groups = [approval[key] for key in ("eiren_safe_now", "successor_safe_now_seeds", "eiren_candidate_prototypes", "successor_candidate_seeds", "eiren_exact_approval", "eiren_blocked")]
    packet_ids = [item["packet_id"] for group in packet_groups for item in group]
    checks = {
        "research_count": len(proposals) == 10,
        "research_ids_unique": len({p["proposal_id"] for p in proposals}) == 10,
        "research_distribution": Counter(p["expected_disposition"] for p in proposals) == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        "approval_counts": approval["counts"] == EXPECTED_APPROVAL,
        "packet_ids_unique": len(packet_ids) == len(set(packet_ids)),
        "skill_runner_counts": skills["counts"] == EXPECTED_SKILLS,
        "clean_counts": clean["counts"] == {"eiren_tasks": 15, "successor_seeds": 15},
        "exact_unexecuted": all(p["x2_execution"] == "do_not_execute" for p in approval["eiren_exact_approval"]),
        "blocked_unexecuted": all(p["x2_execution"] == "prohibited_without_new_evidence" for p in approval["eiren_blocked"]),
        "successor_seeds_not_executed": all("successor" in p["x2_execution"] for p in approval["successor_safe_now_seeds"] + approval["successor_candidate_seeds"]),
    }
    return {
        "schema": "ghc.family.v645-v3.portfolio-validation.v1", "valid": all(checks.values()),
        "checks": checks, "research_count": len(proposals), "packet_count": len(packet_ids),
        "boundary": "Count and structure validation does not establish task outcomes, authority, or production readiness.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    receipt = validate(args.phase_dir)
    if args.receipt:
        write(args.receipt, receipt)
    print(json.dumps(receipt, indent=2))
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
