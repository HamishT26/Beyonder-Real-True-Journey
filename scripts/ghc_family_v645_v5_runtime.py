#!/usr/bin/env python3
"""Bounded runtime shared by the Sable Rook v645-v5 family runners."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/sable-rook/v645-v5"
PHASE = "v645-gmut-thos-v5-x1-x2"

RUNNER_PROFILES = {
    "ghc_family_v645_v5_portfolio_runner.py": "portfolio",
    "ghc_family_v645_v5_core_runner.py": "core",
    "ghc_family_v645_v5_skill_runner.py": "skill",
    "ghc_family_v645_v5_boundary_runner.py": "boundary",
    "ghc_family_v645_v5_method_flow_runner.py": "method_flow",
    "ghc_family_v645_v5_validation_runner.py": "validation",
}


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def check(name: str, passed: bool, observed: Any) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "observed": observed}


def evaluate(runner_name: str) -> dict[str, Any]:
    profile = RUNNER_PROFILES[runner_name]
    checks: list[dict[str, Any]] = []

    if profile == "portfolio":
        ledger = load("approval-packets/x2-execution-ledger.json")
        counts = ledger["counts"]
        checks += [
            check("safe_now_completed", counts["safe_now_completed"] == 20, counts),
            check("candidate_completed", counts["candidate_completed"] == 12, counts),
            check("exact_unexecuted", counts["exact_unexecuted"] == 10, counts),
            check("blocked_unexecuted", counts["blocked_unexecuted"] == 5, counts),
            check(
                "owner_witnesses_pass",
                all(row["result"] == "pass" for row in ledger["owner_witnesses"]),
                len(ledger["owner_witnesses"]),
            ),
            check("predecessor_credit_zero", ledger["predecessor_completion_credit"] == 0, ledger["predecessor_completion_credit"]),
        ]

    elif profile == "core":
        ledger = load("x2-proposal-ledger.json")
        distribution = Counter(row["outcome"] for row in ledger["proposals"])
        missing = [
            artifact
            for row in ledger["proposals"]
            for artifact in row["artifacts"]
            if not (PHASE_DIR / artifact).is_file()
        ]
        checks += [
            check("proposal_count", len(ledger["proposals"]) == 10, len(ledger["proposals"])),
            check("distribution", distribution == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(distribution)),
            check("all_artifacts_present", not missing, missing),
            check("terminal_fail_closed", ledger["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", ledger["terminal_verdict"]),
        ]

    elif profile == "skill":
        plan = load("prototypes/skill-runner-execution-ledger.json")
        malformed = []
        for row in plan["skills"]:
            text = (PHASE_DIR / row["skill_path"]).read_text(encoding="utf-8")
            required = ["# Trigger scope", "# Required inputs", "# Procedure", "# Protected gates", "# Recovery"]
            if not all(marker in text for marker in required):
                malformed.append(row["skill_name"])
        checks += [
            check("skills_built", len(plan["skills"]) == 12, len(plan["skills"])),
            check("skills_invoked", all(row["invoked"] and row["result"] == "pass" for row in plan["skills"]), len(plan["skills"])),
            check("skill_instructions_complete", not malformed, malformed),
            check("runners_registered", len(plan["runners"]) == 6, len(plan["runners"])),
        ]

    elif profile == "boundary":
        desi = load("gmut/desi-bao-zero-row-receipt.json")
        thos = load("thos/learning-decay-proxy-vectors.json")
        freed = load("freed-id/verifier-attestation-profile.json")
        cbr = load("cbr/aviation-occurrence-reservation.json")
        synthetic = load("validation/synthetic-mutation-negative-register.json")
        report = (PHASE_DIR / "deliverables/v645-v5-static-report.html").read_text(encoding="utf-8")
        checks += [
            check("desi_zero_rows", desi["real_rows_ingested"] == 0 and desi["likelihood_evaluations"] == 0, desi),
            check("thos_zero_real_arms", thos["real_participants"] == 0 and thos["real_operators"] == 0, thos),
            check("freed_id_nonproduction", freed["details"]["real_keys"] == 0 and freed["details"]["live_services"] == 0, freed["details"]),
            check("cbr_authority_reserved", all(value == "unresolved_exact_gate" for value in cbr["details"]["authority_status"].values()), cbr["details"]["authority_status"]),
            check("synthetic_rejections", synthetic["count"] == 70 and synthetic["all_rejected"], synthetic["count"]),
            check("report_structure", all(marker in report for marker in ['<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'Manual and affected-user evaluation remain reserved']), "required markers"),
        ]

    elif profile == "method_flow":
        state = load("method-flow/method-flow-state-x2.json")
        fail_ids = {w["witness_id"] for w in state["witnesses"] if w["result"] == "fail"}
        pass_ids = {w["witness_id"] for w in state["witnesses"] if w["result"] == "pass"}
        malformed = [
            row["method_id"]
            for row in state["methods"]
            if not ({row["validation_witness_ids"][0]} <= fail_ids and {row["validation_witness_ids"][1]} <= pass_ids)
        ]
        checks += [
            check("append_only_methods", state["counts"]["methods"] >= 11, state["counts"]),
            check("failures_retained", state["counts"]["witness_results"]["fail"] == state["counts"]["methods"], state["counts"]),
            check("passes_bounded", state["counts"]["witness_results"]["pass"] == state["counts"]["methods"], state["counts"]),
            check("method_pairs_valid", not malformed, malformed),
        ]

    elif profile == "validation":
        truth = load("phase-truth.json")
        retained = load("retained-negative-register.json")
        gates = load("exact-open-gate-register.json")
        owner_files = git("diff", "--name-only", "3e0f37ec230252776e89841f12aa31b18dc21808..HEAD").splitlines()
        checks += [
            check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"]),
            check("all_claim_gates_false", all(value is False for value in truth["protected_claims"].values()), truth["protected_claims"]),
            check("negative_erasure_zero", retained["negative_erasure_count"] == 0, retained["negative_erasure_count"]),
            check("gates_preserved", gates["none_silently_closed"] and gates["effective"]["open_gaps"] == 7 and gates["effective"]["exact_gates"] == 8, gates["effective"]),
            check("owner_files_under_15000", len(owner_files) < 15000, len(owner_files)),
        ]

    result = "pass" if all(row["passed"] for row in checks) else "fail"
    return {
        "schema": "ghc.family.runner-witness.v1",
        "phase": PHASE,
        "runner": runner_name,
        "profile": profile,
        "checks": checks,
        "check_count": len(checks),
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded software and synthetic behavior only; protected empirical, participant, production, authority, security-complete, accessibility-complete, and Stage 20 gates remain open.",
    }


def cli(runner_name: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = evaluate(Path(runner_name).name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runner": payload["runner"], "checks": payload["check_count"], "result": payload["result"]}))
    return 0 if payload["result"] == "pass" else 1
