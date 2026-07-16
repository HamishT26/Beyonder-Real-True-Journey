#!/usr/bin/env python3
"""Shared implementations for the four phase-specific v646-v3 runners."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from ghc_family_v646_v3_runtime import RUNNERS as CORE_SURFACES, run as run_core


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v646-v3"
BOUNDARY = "Bounded same-owner structural evidence only; no empirical, authority, production, exhaustive-assurance, independent-reproduction, or Stage 20 credit."


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def core_runner() -> dict[str, Any]:
    scratch = ROOT / ".ghc-family-runtime-v646-v3" / "core-runner"
    rows = {name: run_core(name, scratch) for name in CORE_SURFACES}
    return {
        "runner": "v646-v3-core-runner", "checks": sum(row.get("checks", 0) for row in rows.values()),
        "passed": len(rows) == 10 and all(row.get("passed") for row in rows.values()),
        "core_count": len(rows), "results": rows, "boundary": BOUNDARY,
    }


def portfolio_runner() -> dict[str, Any]:
    safe = load("approval-packets/x2-safe-now-execution.json")
    candidates = load("prototypes/x2-candidate-execution.json")
    cleanup = load("maintenance/x2-clean-refine-ledger.json")
    protected = load("approval-packets/x2-protected-packet-register.json")
    checks = [
        len(safe.get("tasks", [])) == safe.get("completed") == 30,
        all(row.get("state") == "completed" for row in safe.get("tasks", [])),
        len(candidates.get("tasks", [])) == candidates.get("completed") == 20,
        all(row.get("state") == "completed" for row in candidates.get("tasks", [])),
        len(cleanup.get("tasks", [])) == cleanup.get("completed") == 30,
        all(row.get("state") == "completed" for row in cleanup.get("tasks", [])),
        protected.get("inherited_exact_count") == 10 and protected.get("inherited_blocked_count") == 5,
        protected.get("executed") == protected.get("relabelled_safe_now") == 0,
    ]
    return {"runner": "v646-v3-portfolio-runner", "checks": len(checks), "passed": all(checks), "safe": 30, "candidates": 20, "cleanup": 30, "boundary": BOUNDARY}


def skill_runner() -> dict[str, Any]:
    receipt = load("prototypes/skill-build-receipt.json")
    checks = [
        receipt.get("skill_count") == 20, receipt.get("validated_count") == 20,
        receipt.get("smoke_use_pass_count") == 20, receipt.get("newly_initialized_count") == 20,
        receipt.get("compatible_reused_count") == 0, receipt.get("valid") is True,
    ]
    return {"runner": "v646-v3-skill-runner", "checks": len(checks), "passed": all(checks), "skill_count": receipt.get("skill_count"), "validated": receipt.get("validated_count"), "smoke_used": receipt.get("smoke_use_pass_count"), "boundary": BOUNDARY}


def validation_runner() -> dict[str, Any]:
    from ghc_family_v646_v3_validator import validate
    return validate(mode="minimal", revision=None, require_clean=False)


TOOLS: dict[str, Callable[[], dict[str, Any]]] = {
    "core": core_runner, "portfolio": portfolio_runner, "skill": skill_runner, "validation": validation_runner,
}


def main_for(name: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = TOOLS[name]()
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if payload.get("passed") or payload.get("valid") else 1
