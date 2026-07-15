#!/usr/bin/env python3
"""Detailed or minimal bounded validator for the v645-v4 packet."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/ilyra-fen/v645-v4"
PHASE = "v645-gmut-thos-v4-x1-x2"
SOURCE = "3bff59204cee9a7f031b032262d45360cc310c8a"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
X1 = "a0c2cdfac1fee23c2f5318a148f80198d251efc6"


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
    add(checks, "independent_reproduction_open", truth["independent_team_reproduction"] is False, truth["independent_team_reproduction"])
    add(checks, "source_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, "HEAD"], cwd=ROOT).returncode == 0, SOURCE)
    add(checks, "source_seal_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE_SEAL, "HEAD"], cwd=ROOT).returncode == 0, SOURCE_SEAL)
    add(checks, "x1_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT).returncode == 0, X1)
    add(checks, "zero_merges_since_source", int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")) == 0, git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD"))
    add(checks, "owner_generated_under_15000", len(git("diff", "--name-only", f"{SOURCE}..HEAD").splitlines()) < 15000, len(git("diff", "--name-only", f"{SOURCE}..HEAD").splitlines()))

    portfolio = load("approval-packets/x2-execution-ledger.json")
    add(checks, "safe_now_30", portfolio["counts"]["safe_now_completed"] == 30, portfolio["counts"]["safe_now_completed"])
    add(checks, "candidate_20", portfolio["counts"]["candidate_completed"] == 20, portfolio["counts"]["candidate_completed"])
    add(checks, "exact_packets_unexecuted", portfolio["counts"]["exact_unexecuted"] == 10, portfolio["counts"]["exact_unexecuted"])
    add(checks, "blocked_packets_unexecuted", portfolio["counts"]["blocked_unexecuted"] == 5, portfolio["counts"]["blocked_unexecuted"])
    clean = load("maintenance/x2-clean-refine-ledger.json")
    add(checks, "cleanup_30", clean["counts"]["completed"] == 30, clean["counts"]["completed"])
    add(checks, "cleanup_non_destructive", clean["destructive_change_count"] == 0, clean["destructive_change_count"])
    skills = load("prototypes/skill-runner-execution-ledger.json")
    add(checks, "skills_20_used", skills["counts"]["skills_used"] == 20, skills["counts"]["skills_used"])
    add(checks, "runners_10_used", skills["counts"]["runners_used"] == 10, skills["counts"]["runners_used"])
    add(checks, "runner_witnesses_pass", all(row["bounded_test"] == "pass" for row in skills["runners"]), [row["bounded_test"] for row in skills["runners"]])
    retained = load("retained-negative-register.json")
    add(checks, "inherited_negatives_preserved", retained["counts"]["inherited_effective"] == 2003, retained["counts"]["inherited_effective"])
    add(checks, "effective_negatives_2087", retained["counts"]["effective_total"] == 2087, retained["counts"]["effective_total"])
    add(checks, "negative_erasure_zero", retained["negative_erasure_count"] == 0, retained["negative_erasure_count"])
    gates = load("exact-open-gate-register.json")
    add(checks, "effective_open_gaps_6", gates["effective"]["open_gaps"] == 6, gates["effective"]["open_gaps"])
    add(checks, "effective_exact_gates_7", gates["effective"]["exact_gates"] == 7, gates["effective"]["exact_gates"])
    add(checks, "gates_not_silently_closed", gates["none_silently_closed"], gates["none_silently_closed"])
    method = load("method-flow/method-flow-state.json")
    add(checks, "method_count_14", method["counts"]["methods"] == 14, method["counts"]["methods"])
    add(checks, "balanced_method_witnesses", method["counts"]["witness_results"] == {"fail": 14, "pass": 14}, method["counts"]["witness_results"])

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
        overview_words = len((PHASE_DIR / "v645-v4-integrated-overview.md").read_text(encoding="utf-8").split())
        add(checks, "overview_three_page_equivalent", 1500 <= overview_words <= 6000, overview_words)
        synthetic = load("validation/synthetic-mutation-negative-register.json")
        add(checks, "synthetic_negatives_70", synthetic["count"] == 70, synthetic["count"])
        add(checks, "synthetic_negatives_rejected", synthetic["all_rejected"], synthetic["all_rejected"])
        source = load("sources/source-ledger.json")
        add(checks, "source_status_vocabulary", all(row["status"] in {"current", "stable", "draft", "watch"} for row in source["sources"]), source["counts"])
        report = (PHASE_DIR / "deliverables/v645-v4-static-report.html").read_text(encoding="utf-8")
        for marker in ['<html lang="en">', 'href="#main"', '<main id="main">', '<caption>', 'lang="mi"', 'Manual and affected-user evaluation remain reserved']:
            add(checks, f"report_marker:{marker}", marker in report, marker)
        for key in ["empirical_gmut_confirmation", "thos_effectiveness", "freed_id_production_completion", "cbr_or_maori_authority", "complete_accessibility", "exhaustive_security", "agi_or_asi", "consciousness_or_personhood", "theory_of_everything"]:
            add(checks, f"truth_boundary:{key}", truth[key] is False, truth[key])

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
