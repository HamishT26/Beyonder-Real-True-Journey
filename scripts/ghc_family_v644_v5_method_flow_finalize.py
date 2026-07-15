#!/usr/bin/env python3
"""Finalize v644-v5 Method Flow receipts after the lean witness is appended."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


PHASE_REL = Path("docs/eiren-kestrel/v644-v5")


def load_core(runner: Path):
    spec = importlib.util.spec_from_file_location("ghc_family_method_flow_core", runner)
    if spec is None or spec.loader is None:
        raise SystemExit("unable to load Method Flow State runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--skill-runner", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    phase = repo / PHASE_REL
    ledger_path = phase / "method-flow/method-flow-state.json"
    wrapper_path = phase / "method-flow/workaround-validation-ledger.json"
    skill_receipt_path = phase / "tooling/ghc-family-method-flow-state-skill-receipt.json"

    core = load_core(args.skill_runner.resolve())
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    validation = core.validate_ledger(ledger)
    pending = sorted(
        method["method_id"]
        for method in ledger["methods"]
        if method["recommendation_state"] not in {"preferred", "deprecated", "superseded"}
    )
    wrapper = {
        "schema": "ghc.family.v644-v5.method-flow-validation-ledger.v1",
        "phase": "v644-gmut-thos-v5-x1-x2",
        "validation": validation,
        "witnesses": ledger["witnesses"],
        "pending_methods": pending,
        "boundary": ledger["boundary"],
    }
    write_json(wrapper_path, wrapper)

    skill_receipt = json.loads(skill_receipt_path.read_text(encoding="utf-8"))
    skill_receipt["phase_ledger_validation"] = validation
    skill_receipt["pending_phase_method"] = None
    skill_receipt["all_phase_methods_preferred_or_closed"] = not pending
    write_json(skill_receipt_path, skill_receipt)

    result = {
        "valid": validation["valid"] and not pending,
        "method_count": validation["method_count"],
        "witness_count": validation["witness_count"],
        "pending_methods": pending,
        "privacy_hits": validation["privacy_hits"],
    }
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
