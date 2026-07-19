#!/usr/bin/env python3
"""Detailed and minimal bounded validators for Ilyra Fen v649-v2."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v649-v2"
X1_COMMIT = "d20d13d2e17adbf35d0088fb38c66fab470a460f"
SOURCE_COMMIT = "26e61bc8161d29a229c362c9a6aefedbbd8b49f5"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"(?:[A-Z]:\\Users\\|/Users/|/home/)[^\s\"']+", re.I),
    "private_uri": re.compile(r"(?:codex|chatgpt|vscode|file)://", re.I),
    "credential_assignment": re.compile(r"(?:api[_-]?key|password|secret|token)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
    "delegation_markup": re.compile(r"<\/?codex_delegation\b", re.I),
}


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def add(checks: list[dict[str, Any]], name: str, passed: bool, detail: str = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def phase_scan() -> tuple[int, int, list[dict[str, str]], int, list[str]]:
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    hits: list[dict[str, str]] = []
    json_count = 0
    json_errors: list[str] = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
                json_count += 1
            except Exception as exc:  # pragma: no cover - receipt path
                json_errors.append(f"{relative}:{type(exc).__name__}")
        if path.suffix.lower() not in {".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern_class, pattern in PRIVACY.items():
            if pattern.search(text):
                hits.append({"path": relative, "pattern_class": pattern_class})
    return len(files), json_count, hits, len(PRIVACY), json_errors


def build_checks(mode: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    proposals = load("x2-proposal-ledger.json")
    mutations = load("validation/x2-synthetic-mutation-results.json")
    safe = load("portfolios/safe-now-ledger.json")
    candidates = load("portfolios/candidate-ledger.json")
    skills = load("portfolios/skill-ledger.json")
    runners = load("portfolios/runner-ledger.json")
    cleanup = load("maintenance/clean-fix-refine-ledger.json")
    negatives = load("retained-negative-register-final.json") if (PHASE / "retained-negative-register-final.json").is_file() else load("retained-negative-register-x2.json")
    gates = load("exact-open-gate-register-x2.json")
    truth = load("phase-truth-final.json") if (PHASE / "phase-truth-final.json").is_file() else load("phase-truth-x2.json")
    method = load("method-flow/method-flow-ledger.json")
    source = load("sources/source-ledger.json")
    phase_files, json_count, privacy_hits, privacy_classes, json_errors = phase_scan()

    add(checks, "phase_directory", PHASE.is_dir())
    add(checks, "ten_core_proposals", len(proposals["proposals"]) == 10)
    add(checks, "outcome_distribution", proposals["outcome_distribution"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    add(checks, "outcome_vocabulary", set(x["observed_outcome"] for x in proposals["proposals"]) == ALLOWED_OUTCOMES)
    add(checks, "seventy_mutations", mutations["count"] == 70)
    add(checks, "all_mutations_rejected", mutations["rejected"] == 70 and mutations["accepted"] == 0)
    add(checks, "safe_now_thirty", safe["count"] == safe["completed"] == 30)
    add(checks, "candidates_twenty", candidates["count"] == candidates["built_tested_invoked"] == 20)
    add(checks, "skills_twenty", skills["count"] == skills["initialized_customized_smoke_used"] == 20)
    add(checks, "runners_ten", runners["count"] == runners["accept_and_reject_witnessed"] == 10)
    add(checks, "cleanup_thirty", cleanup["count"] == cleanup["completed"] == 30)
    expected_negatives = negatives["inherited_effective"] + negatives["new_x1_operational"] + negatives["new_x2_operational"] + negatives["preregistered_synthetic_executed_and_rejected"] + negatives.get("post_evidence_operational", 0)
    add(checks, "negatives_preserved", negatives["current_effective"] == expected_negatives and negatives["no_negative_erased"])
    add(checks, "open_gaps_preserved", gates["effective_open_gaps"] == 36 and gates["none_silently_closed"])
    add(checks, "exact_gates_preserved", gates["effective_exact_gates"] == 37 and gates["none_silently_closed"])
    add(checks, "terminal_abstention", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    add(checks, "same_owner_only", truth["same_owner_only"] and not truth["independent_reproduction"])
    method_states = method["counts"]["states"]
    add(checks, "method_flow_preferred", method_states["preferred"] + method_states["candidate"] == method["counts"]["methods"] and method_states["candidate"] <= 1)
    add(checks, "method_failures_retained", method["counts"]["witness_results"]["fail"] >= 9)
    add(checks, "method_recoveries_witnessed", method["counts"]["witness_results"]["pass"] >= 9)
    add(checks, "source_status_vocabulary", all(x["status"] in {"current", "stable", "draft", "watch"} for x in source["sources"]))

    if mode == "detailed":
        add(checks, "complete_json_parse", not json_errors, ",".join(json_errors))
        add(checks, "five_privacy_classes", privacy_classes == 5)
        add(checks, "privacy_zero_confirmed", not privacy_hits, json.dumps(privacy_hits, ensure_ascii=False))
        add(checks, "owner_file_threshold", phase_files < 15000, str(phase_files))
        documents = [path for path in PHASE.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html"}]
        word_counts = {path.relative_to(ROOT).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in documents}
        add(checks, "document_word_cap", all(count <= 6000 for count in word_counts.values()), json.dumps({k: v for k, v in word_counts.items() if v > 6000}))
        add(checks, "skill_todos_absent", all("TODO" not in (PHASE / "skills" / row["name"] / "SKILL.md").read_text(encoding="utf-8") for row in skills["skills"]))
        add(checks, "skill_metadata_present", all((PHASE / "skills" / row["name"] / "agents" / "openai.yaml").stat().st_size > 0 for row in skills["skills"]))
        add(checks, "runner_names_family_current", all(row["runner"].startswith("ghc_family_") for row in runners["runners"]))
        add(checks, "runner_accept_witnesses", all(row["accepting_returncode"] == 0 for row in runners["runners"]))
        add(checks, "runner_reject_witnesses", all(row["rejecting_returncode"] == 2 for row in runners["runners"]))
        add(checks, "real_and_authority_counts_zero", all(all(v == 0 for v in row["real_or_authority_gate_counts"].values()) for row in proposals["proposals"]))
        add(checks, "exact_approvals_unexecuted", load("approval-packets/inherited-exact-approvals.json")["unexecuted"])
        add(checks, "blocked_packets_unexecuted", load("approval-packets/inherited-blocked-packets.json")["unexecuted"])
        add(checks, "x1_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", X1_COMMIT, "HEAD"], cwd=ROOT).returncode == 0)
        add(checks, "source_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE_COMMIT, "HEAD"], cwd=ROOT).returncode == 0)
        x1_manifest = load("validation/x1-staged-manifest.json")
        add(checks, "x1_manifest_cardinality", x1_manifest["entry_count"] == 48)
        add(checks, "identity_boundary_present", "relational working language" in truth["identity_boundary"].casefold())
        add(checks, "primary_focus", truth["primary_focus"] == "THOS Body")
        add(checks, "bounded_practice", "transfusion" in truth["bounded_practice"])
        if (PHASE / "deliverables" / "v649-v2-static-report.html").is_file():
            add(checks, "static_report_present", (PHASE / "deliverables" / "v649-v2-static-report.html").stat().st_size > 0)
            add(checks, "integrated_overview_present", (PHASE / "deliverables" / "v649-v2-final-integrated-overview.md").stat().st_size > 0)
            add(checks, "manual_accessibility_reserved", "Manual and affected-user evaluation remains reserved" in (PHASE / "deliverables" / "v649-v2-static-report.html").read_text(encoding="utf-8"))
            add(checks, "terminal_route_held", load("orchestration/terminal-route-final.json")["state"] == "PREPARED_NOT_SENT")

    meta = {
        "phase_file_count": phase_files,
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_pattern_class_count": privacy_classes,
        "privacy_confirmed_hit_count": len(privacy_hits),
        "privacy_confirmed_hits": privacy_hits,
    }
    return checks, meta


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["detailed", "minimal"], required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    checks, meta = build_checks(args.mode)
    issues = [row for row in checks if not row["passed"]]
    payload = {
        "schema": f"ghc.family.v649-v2.validation.{args.mode}.v1",
        "mode": args.mode,
        "check_count": len(checks),
        "passed_count": len(checks) - len(issues),
        "issue_count": len(issues),
        "issues": issues,
        "checks": checks,
        "valid": not issues,
        **meta,
        "boundary": "Bounded same-owner repository validation only; not independent reproduction or broader assurance.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mode": args.mode, "checks": len(checks), "issues": len(issues), "json": meta["json_parse_count"], "files": meta["phase_file_count"], "privacy_hits": meta["privacy_confirmed_hit_count"]}, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
