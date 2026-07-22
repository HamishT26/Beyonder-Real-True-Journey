#!/usr/bin/env python3
"""Validate closeout content before the final staged manifests are built."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    checks = []
    issues = []

    def check(label: str, condition: bool) -> None:
        checks.append({"check": label, "passed": bool(condition)})
        if not condition:
            issues.append(label)

    closeout = load("closeout/closeout-receipt.json")
    seal = load("seal/seal-receipt.json")
    final = load("final/final-record.json")
    contract = load("final/final-validation-contract.json")
    route = load("route/terminal-route-receipt.json")
    truth = load("truth/phase-truth.json")
    evidence = load("validation/evidence-validation-receipt.json")
    baton = (PHASE / "handoffs/sable-rook-v652-v1-activation.md").read_text(encoding="utf-8")
    words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
    check("anchors", closeout["source_head"] == "68f7e9b7fc454746c02b8a85987e10b87a0725c3" and closeout["x1_commit"] == "580a3f0155c589866fd7f4aacd88790419cd147a" and closeout["evidence_commit"] == "0b382d660837536e12672e28cc68f6208e2b0069")
    check("truth_distribution", closeout["outcomes"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
    check("truth_counts", (closeout["effective_negatives"], closeout["effective_open_gaps"], closeout["effective_exact_gates"]) == (7855, 61, 62))
    check("evidence_valid", evidence["valid"])
    check("baton_budget", 10_000 <= words <= 100_000)
    check("future_cli_zero", final["future_cli"] == {"prepared": 8, "named": 0, "launched": 0})
    check("route_held", route["recipient_exact_title"] == "Sable Rook" and route["successor_phase"] == "v652-v1" and route["send_state"] == "PREPARED_NOT_SENT")
    check("no_replay", seal["one_canonical_pass"] and not seal["replay_after_success"] and not contract["replay_after_success"])
    check("scope_rule", contract["full_repository_suite_owner"] == "Eiren Kestrel only under the current refinement" and not contract["full_repository_suite_planned"])
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and final["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    payload = {
        "schema": "ghc.family.v651-v8-special.closeout-validation.v1",
        "checks": len(checks),
        "check_rows": checks,
        "issues": issues,
        "baton_words": words,
        "valid": not issues,
        "boundary": "Precommit closeout content validation only; the exact-final canonical run occurs once after the final commit is pushed.",
    }
    output = ROOT / args.receipt
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": not issues, "checks": len(checks), "issues": issues, "baton_words": words}))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
