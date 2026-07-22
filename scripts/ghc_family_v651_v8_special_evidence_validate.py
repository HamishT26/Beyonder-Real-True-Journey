#!/usr/bin/env python3
"""Validate the bounded Ilyra v651-v8 SPECIAL x2 evidence candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/ilyra-fen/v651-v8-special-cli-prep")
PHASE = ROOT / PHASE_REL
SOURCE = "68f7e9b7fc454746c02b8a85987e10b87a0725c3"
X1 = "580a3f0155c589866fd7f4aacd88790419cd147a"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_local_path": re.compile(r"(?i)(?:[a-z]:\\users\\|/users/|/home/)[^\s\"'<>]+"),
    "delegation_markup": re.compile(r"(?i)<\s*/?\s*codex_delegation\b"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file)://[^\s\"'<>]+"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s,;}]+"),
}


def git(*args: str, binary: bool = False):
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True, text=not binary, encoding=None if binary else "utf-8"
    ).stdout


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

    proposals = load("preregistration/proposals.json")
    proposal_chain = load("provenance/frozen-chain-proposal-index.json")
    outcomes = load("x2/core-outcome-ledger.json")
    placeholders = load("cli/future-seat-placeholders.json")
    cli = load("cli/cli-batch-receipt.json")
    plan = load("portfolios/x1-portfolio-plan.json")
    safe = load("x2/safe-now-execution-ledger.json")
    candidates = load("x2/candidate-execution-ledger.json")
    skills = load("skills/skill-use-ledger.json")
    runners = load("runners/runner-use-ledger.json")
    cleanup = load("maintenance/clean-fix-refine-ledger.json")
    truth = load("truth/phase-truth.json")
    negatives = load("truth/retained-negative-register.json")
    gates = load("truth/open-exact-gate-register.json")
    method = load("method-flow/method-flow-ledger.json")
    method_validation = load("method-flow/method-flow-validation-x2.json")
    meta = load("tooling/meta-tool-box-x2/meta-tool-catalogue.json")
    meta_validation = load("tooling/meta-tool-box-x2/validation.json")
    baton_budget = load("handoffs/baton-word-budget.json")

    check("proposal_count_30", len(proposals["proposals"]) == 30)
    check("proposal_chain_1180", proposal_chain.get("count") == 1180 and proposal_chain.get("new_count") == 30)
    check("outcome_count_30", len(outcomes["rows"]) == 30)
    check("outcome_distribution", outcomes["distribution"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
    check("outcome_labels", {row["outcome"] for row in outcomes["rows"]} <= ALLOWED)
    check("frozen_dispositions_match", all(a["expected_disposition"] == b["outcome"] for a, b in zip(proposals["proposals"], outcomes["rows"], strict=True)))
    check("placeholders_eight", len(placeholders["placeholders"]) == 8)
    check("placeholders_unnamed", placeholders["named_cli_siblings"] == 0 and all(row["name"] is None and row["role"] is None and row["hope"] is None for row in placeholders["placeholders"]))
    check("placeholders_unlaunched", placeholders["launched_cli_siblings"] == 0 and cli["all_unlaunched"])
    check("prepare_and_refuse", cli["prepare_passes"] == 8 and cli["launch_refusals"] == 8)
    check("mutations_rejected", cli["synthetic_mutations_rejected"] == 100)
    check("safe_now_40", len(plan["safe_now_tasks"]) == 40 and safe["count"] == 40 and all(row["state"] == "completed" for row in safe["rows"]))
    check("candidates_30", len(plan["candidate_tasks"]) == 30 and candidates["count"] == 30 and all(row["state"] == "completed" for row in candidates["rows"]))
    check("skills_20", len(plan["skill_ideas"]) == 20 and skills["validated"] == 20 and skills["smoke_used"] == 20 and skills["global_promotions"] == 0)
    check("runners_12", len(plan["runner_ideas"]) == 12 and runners["accept_passes"] == 12 and runners["reject_passes"] == 12)
    check("cleanup_40", len(plan["clean_fix_refine_tasks"]) == 40 and cleanup["count"] == 40 and cleanup["destructive_actions"] == 0)
    check("phase_truth_counts", truth["effective_negatives"] == 7855 and truth["effective_open_gaps"] == 61 and truth["effective_exact_gates"] == 62)
    check("negative_arithmetic", negatives["effective_total"] == negatives["inherited_ordinary"] + negatives["x1_operational"] + negatives["post_x1_lifecycle_operational"] + negatives["x2_operational"] + negatives["synthetic_cli_mutations"])
    check("gate_counts", gates["effective_open_gaps"] == 61 and gates["effective_exact_gates"] == 62)
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("route_held", truth["immediate_successor"] == "Sable Rook" and truth["immediate_successor_phase"] == "v652-v1" and truth["terminal_delivery_state"] == "PREPARED_NOT_SENT")
    check("method_flow", method["counts"]["methods"] == 8 and method["counts"]["witness_results"] == {"fail": 10, "pass": 8} and method_validation["valid"])
    check("meta_catalogue", meta["card_count"] == 20 and meta_validation["valid"])
    check("baton_budget", baton_budget["valid"] and 10_000 <= baton_budget["words"] <= 100_000)
    check("primary_focus", truth["primary_focus"] == "THOS Body")

    git("merge-base", "--is-ancestor", SOURCE, X1)
    check("source_ancestral_to_x1", True)
    check("x1_parent_source", git("rev-parse", f"{X1}^").strip() == SOURCE)
    x1_manifest = json.loads(git("show", f"{X1}:{PHASE_REL.as_posix()}/validation/x1-index-manifest.json"))
    manifest_issues = []
    for row in x1_manifest["entries"]:
        data = git("show", f"{X1}:{row['path']}", binary=True)
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            manifest_issues.append(row["path"])
    check("x1_blob_manifest", not manifest_issues)
    x1_paths = git("ls-tree", "-r", "--name-only", X1, PHASE_REL.as_posix()).splitlines()
    check("x1_has_no_x2", not any(any(marker in path.lower() for marker in ("/x2-", "/evidence/", "/closeout/", "/seal/", "/final/")) for path in x1_paths))

    json_issues = []
    privacy_hits = []
    overlong = []
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                json_issues.append(f"{rel}:{exc.lineno}")
        if path.suffix.lower() in {".md", ".txt"}:
            words = len(re.findall(r"\b\w+[\w'-]*\b", text, flags=re.UNICODE))
            if words > 100_000:
                overlong.append({"path": rel, "words": words})
        if path.suffix.lower() in {".json", ".md", ".txt", ".html"}:
            for name, pattern in PRIVACY.items():
                if pattern.search(text):
                    privacy_hits.append({"path": rel, "class": name})
    check("json_parse", not json_issues)
    check("privacy_zero", not privacy_hits)
    check("document_cap", not overlong)
    check("owner_files_under_2000", len(files) < 2_000)
    materialized = len([path for path in ROOT.rglob("*") if path.is_file()])
    check("materialized_under_2000", materialized < 2_000)

    payload = {
        "schema": "ghc.family.v651-v8-special.evidence-validation.v1",
        "phase": "v651-v8-special-cli-prep",
        "checks": len(checks),
        "check_rows": checks,
        "issues": issues,
        "json_documents": len(list(PHASE.rglob("*.json"))),
        "public_files_scanned": len(files),
        "privacy_pattern_classes": sorted(PRIVACY),
        "confirmed_privacy_hits": privacy_hits,
        "owner_files": len(files),
        "materialized_files": materialized,
        "x1_manifest_entries": len(x1_manifest["entries"]),
        "valid": not issues,
        "boundary": "Bounded same-owner evidence under shared infrastructure; not full-suite, independent reproduction, production certification, complete privacy or accessibility, scientific confirmation, authority, or Stage 20 evidence.",
    }
    output = ROOT / args.receipt
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": not issues, "checks": len(checks), "issues": issues, "json": payload["json_documents"], "files": len(files)}))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
