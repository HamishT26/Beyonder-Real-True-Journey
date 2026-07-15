#!/usr/bin/env python3
"""Detailed and minimal bounded validator for Sable Rook v645-v5."""

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
SOURCE = "3e0f37ec230252776e89841f12aa31b18dc21808"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
X1 = "2e330ab76f03c05ff556c484c22851d682b0ac7b"


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def add(checks: list[dict[str, Any]], name: str, value: bool, observed: Any) -> None:
    checks.append({"check": name, "passed": bool(value), "observed": observed})


def validate(mode: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    truth = load("phase-truth.json")
    proposals = load("x2-proposal-ledger.json")
    distribution = Counter(row["outcome"] for row in proposals["proposals"])
    add(checks, "phase_directory", PHASE_DIR.is_dir(), "present")
    add(checks, "proposal_count", len(proposals["proposals"]) == 10, len(proposals["proposals"]))
    add(checks, "outcome_distribution", distribution == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(distribution))
    add(checks, "terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
    add(checks, "strict_x1_before_x2", truth["strict_x1_before_x2"], truth["strict_x1_before_x2"])
    add(checks, "primary_focus", truth["primary_focus"] == "THOS Body", truth["primary_focus"])
    add(checks, "source_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, "HEAD"], cwd=ROOT).returncode == 0, SOURCE)
    add(checks, "source_seal_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE_SEAL, "HEAD"], cwd=ROOT).returncode == 0, SOURCE_SEAL)
    add(checks, "x1_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT).returncode == 0, X1)
    merge_count = int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD"))
    add(checks, "zero_merges_since_source", merge_count == 0, merge_count)
    owner_files = [line for line in git("diff", "--name-only", f"{SOURCE}..HEAD").splitlines() if line]
    add(checks, "owner_generated_under_15000", len(owner_files) < 15000, len(owner_files))

    portfolio = load("approval-packets/x2-execution-ledger.json")
    add(checks, "safe_now_20", portfolio["counts"]["safe_now_completed"] == 20, portfolio["counts"])
    add(checks, "candidate_12", portfolio["counts"]["candidate_completed"] == 12, portfolio["counts"])
    add(checks, "exact_packets_unexecuted", portfolio["counts"]["exact_unexecuted"] == 10, portfolio["counts"])
    add(checks, "blocked_packets_unexecuted", portfolio["counts"]["blocked_unexecuted"] == 5, portfolio["counts"])
    add(checks, "predecessor_completion_credit_zero", portfolio["predecessor_completion_credit"] == 0, portfolio["predecessor_completion_credit"])
    clean = load("maintenance/x2-clean-refine-ledger.json")
    add(checks, "cleanup_20", clean["counts"]["completed"] == 20, clean["counts"])
    add(checks, "cleanup_non_destructive", clean["destructive_change_count"] == 0, clean["destructive_change_count"])
    skills = load("prototypes/skill-runner-execution-ledger.json")
    add(checks, "skills_12_used", skills["counts"]["skills_used"] == 12, skills["counts"])
    add(checks, "runners_6_used", skills["counts"]["runners_used"] == 6, skills["counts"])
    add(checks, "runner_witnesses_pass", all(row["result"] == "pass" for row in skills["runners"]), [row["result"] for row in skills["runners"]])
    retained = load("retained-negative-register.json")
    components = retained["counts"]
    expected_total = components["inherited_effective"] + components["v645_v5_x1_operational"] + components["v645_v5_x2_operational"] + components["v645_v5_synthetic"]
    add(checks, "inherited_negatives_preserved", components["inherited_effective"] == 2087, components)
    add(checks, "negative_total_sums", components["effective_total"] == expected_total, components)
    add(checks, "negative_erasure_zero", retained["negative_erasure_count"] == 0, retained["negative_erasure_count"])
    gates = load("exact-open-gate-register.json")
    add(checks, "effective_open_gaps_7", gates["effective"]["open_gaps"] == 7, gates["effective"])
    add(checks, "effective_exact_gates_8", gates["effective"]["exact_gates"] == 8, gates["effective"])
    add(checks, "gates_not_silently_closed", gates["none_silently_closed"], gates["none_silently_closed"])
    method = load("method-flow/method-flow-state-x2.json")
    add(checks, "method_count_matches_negatives", method["counts"]["methods"] == 6 + components["v645_v5_x2_operational"], method["counts"])
    add(checks, "balanced_method_witnesses", method["counts"]["witness_results"]["fail"] == method["counts"]["witness_results"]["pass"] == method["counts"]["methods"], method["counts"])

    if mode == "detailed":
        for row in proposals["proposals"]:
            for artifact in row["artifacts"]:
                add(checks, f"artifact:{row['proposal_id']}:{artifact}", (PHASE_DIR / artifact).is_file(), artifact)
        json_files = list(PHASE_DIR.rglob("*.json"))
        parsed = 0
        for path in json_files:
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        add(checks, "all_phase_json_parses", parsed == len(json_files), parsed)
        docs = list(PHASE_DIR.rglob("*.md"))
        over = [path.relative_to(PHASE_DIR).as_posix() for path in docs if len(path.read_text(encoding="utf-8").split()) > 6000]
        add(checks, "document_word_cap", not over, over)
        overview_words = len((PHASE_DIR / "v645-v5-integrated-overview.md").read_text(encoding="utf-8").split())
        add(checks, "overview_three_page_equivalent", 1500 <= overview_words <= 6000, overview_words)
        synthetic = load("validation/synthetic-mutation-negative-register.json")
        add(checks, "synthetic_negatives_70", synthetic["count"] == 70, synthetic["count"])
        add(checks, "synthetic_negatives_rejected", synthetic["all_rejected"] and synthetic["all_retained"], synthetic["count"])
        source = load("sources/source-ledger.json")
        add(checks, "source_status_vocabulary", all(row["status"] in {"current", "stable", "draft", "watch"} for row in source["sources"]), source["counts"])
        report = (PHASE_DIR / "deliverables/v645-v5-static-report.html").read_text(encoding="utf-8")
        for marker in ['<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'lang="mi"', 'Manual and affected-user evaluation remain reserved']:
            add(checks, f"report_marker:{marker}", marker in report, marker)
        for key, value in truth["protected_claims"].items():
            add(checks, f"truth_boundary:{key}", value is False, value)
        runner_receipt = load("prototypes/runner-validation-receipt.json")
        add(checks, "runner_receipt", runner_receipt["result"] == "pass" and runner_receipt["passing_witnesses"] == 6, runner_receipt)
        sandbox = load("sandbox/sandbox-readonly-audit.json")
        add(checks, "sandbox_fail_closed", not sandbox["launched"] and not sandbox["elevated"] and not sandbox["feature_changed"], sandbox)

    return {
        "schema": "ghc.family.phase-validation.v2", "phase": PHASE, "mode": mode,
        "checks": checks, "check_count": len(checks),
        "passed": sum(1 for row in checks if row["passed"]),
        "failed": [row["check"] for row in checks if not row["passed"]],
        "result": "pass" if all(row["passed"] for row in checks) else "fail",
        "same_owner_only": True, "independent_reproduction": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["detailed", "minimal"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = validate(args.mode)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mode": args.mode, "checks": payload["check_count"], "result": payload["result"]}))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
