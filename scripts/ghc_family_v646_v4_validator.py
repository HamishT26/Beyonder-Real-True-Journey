#!/usr/bin/env python3
"""Detailed and minimal non-Eiren validators for Orin Thale v646-v4."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/orin-thale/v646-v4")
PHASE = ROOT / PHASE_REL
SOURCE = "c45aba6c9c2fee5d60e1fcde9f0de849290cfc96"
X1 = "8b63d3f65f9fe9909da71eeb1171e3b5cf86768a"
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PRIVATE = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "delegation_markup": re.compile(r"(?i)<" + r"\/?" + "codex_" + r"delegation>|<source_" + "thread_id>"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|codex|vscode)://"),
    "private_local_path": re.compile(r"(?i)(?:\b[A-Z]:[\\/]+(?:Users|GHC-Archives)[\\/]+|/(?:home|users)/)"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"),
}
BOUNDARY = "Non-Eiren scoped validation and same-owner replay evidence only; not the full repository suite, independent reproduction, authority, production certification, complete privacy, exhaustive security, or complete accessibility."


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def phase_files() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


def scan_text(path: str, text: str) -> list[dict[str, Any]]:
    return [{"path": path, "class": kind, "offset": match.start()} for kind, pattern in PRIVATE.items() for match in pattern.finditer(text)]


def commit_count() -> int:
    return int(str(git("rev-list", "--count", f"{SOURCE}..HEAD")).strip())


def merge_count() -> int:
    return int(str(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")).strip())


def verify_manifest(relative: str, revision: str) -> tuple[int, list[dict[str, str]]]:
    manifest = load(relative)
    mismatches = []
    for row in manifest.get("entries", []):
        path = row["path"]
        try:
            blob = git("show", f"{revision}:{path}", binary=True)
            assert isinstance(blob, bytes)
            observed = hashlib.sha256(blob).hexdigest()
        except Exception:
            observed = "missing"
        if observed != row["sha256"]:
            mismatches.append({"path": path, "expected": row["sha256"], "observed": observed})
    return len(manifest.get("entries", [])), mismatches


def minimal_checks() -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    issues: list[str] = []

    def check(name: str, condition: bool) -> None:
        checks.append({"check": name, "passed": bool(condition)})
        if not condition:
            issues.append(name)

    required = [
        "x2-proposal-ledger.json", "retained-negative-register.json", "exact-open-gate-register.json",
        "phase-truth.json", "complete-incomplete-checklist.json", "threat-model.json",
        "prototypes/skill-build-receipt.json", "prototypes/runner-build-use-receipt.json",
        "method-flow/runner-validation.json", "orchestration/terminal-route-plan.json",
        "v646-v4-integrated-overview.md", "deliverables/v646-v4-static-report.html",
    ]
    for relative in required:
        check(f"required_{relative}", (PHASE / relative).is_file())
    if issues:
        return checks, issues
    ledger = load("x2-proposal-ledger.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")
    safe = load("approval-packets/x2-safe-now-execution.json")
    candidates = load("prototypes/x2-candidate-execution.json")
    cleanup = load("maintenance/x2-clean-refine-ledger.json")
    skills = load("prototypes/skill-build-receipt.json")
    runners = load("prototypes/runner-build-use-receipt.json")
    method = load("method-flow/runner-validation.json")
    truth = load("phase-truth.json")
    route = load("orchestration/terminal-route-plan.json")
    distribution = ledger.get("distribution", {})
    check("proposal_count_10", ledger.get("proposal_count") == 10)
    check("four_outcomes_only", set(distribution) == OUTCOMES)
    check("distribution_6_2_1_1", distribution == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    check("outcomes_match_rows", Counter(row.get("outcome") for row in ledger.get("proposals", [])) == Counter(distribution))
    check("all_core_gates_passed_in_scope", all(row.get("acceptance_gate_passed_within_scope") for row in ledger.get("proposals", [])))
    check("independent_reproduction_false", ledger.get("independent_reproduction") is False)
    check("negative_components", negatives.get("inherited_effective") == 2704 and negatives.get("x1_operational") == 16 and negatives.get("preregistered_synthetic_executed_and_rejected") == 70 and negatives.get("x2_operational", 0) >= 3)
    check("negative_total_formula", negatives.get("effective_total") == negatives.get("inherited_effective") + negatives.get("x1_operational") + negatives.get("preregistered_synthetic_executed_and_rejected") + negatives.get("x2_operational"))
    check("no_negative_erased", negatives.get("no_negative_erased") is True)
    check("open_gaps_13", gates.get("effective_open_gaps") == 13)
    check("exact_gates_14", gates.get("effective_exact_gates") == 14)
    check("no_silent_gate_closure", gates.get("closed_without_exact_evidence") == 0)
    check("safe_30", safe.get("completed") == 30 and len(safe.get("tasks", [])) == 30)
    check("candidates_20", candidates.get("completed") == 20 and len(candidates.get("tasks", [])) == 20)
    check("cleanup_30", cleanup.get("completed") == 30 and len(cleanup.get("tasks", [])) == 30 and cleanup.get("destructive_actions") == 0)
    check("skills_20", skills.get("valid") is True and skills.get("skill_count") == 20 and skills.get("smoke_use_pass_count") == 20)
    runner_final = runners.get("valid") is True and runners.get("runner_count") == runners.get("built_count") == runners.get("invoked_count") == runners.get("passed_count") == 10
    runner_preflight = runners.get("preflight_valid") is True and runners.get("runner_count") == runners.get("built_count") == 10 and runners.get("invoked_count", 0) >= 8 and runners.get("passed_count", 0) >= 8
    check("runners_10", runner_final or runner_preflight)
    check("method_flow_valid", method.get("valid") is True and method.get("method_count", 0) >= 19 and method.get("witness_count", 0) >= 38)
    check("terminal_route_prepared", route.get("current_state") == "PREPARED_NOT_SENT" and route.get("send_count") == 0)
    check("terminal_verdict_closed", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    check("source_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, "HEAD"], cwd=ROOT).returncode == 0)
    check("x1_ancestry", subprocess.run(["git", "merge-base", "--is-ancestor", X1, "HEAD"], cwd=ROOT).returncode == 0)
    check("commit_cap", commit_count() <= 4)
    check("zero_merges", merge_count() == 0)
    check("overview_three_page", len((PHASE / "v646-v4-integrated-overview.md").read_text(encoding="utf-8").split()) >= 1500)
    check("identity_boundary", "relational working language" in load("identity-receipt.json").get("identity_boundary", ""))
    sources = load("sources/source-ledger.json").get("sources", [])
    check("source_count_17", len(sources) == 17)
    check("source_status_vocab", all(row.get("status") in {"current", "stable", "draft", "watch"} for row in sources))
    check("owner_generated_under_15000", len(phase_files()) < 15000)
    return checks, issues


def validate(mode: str = "detailed", revision: str | None = None, require_clean: bool = False) -> dict[str, Any]:
    checks, issues = minimal_checks()
    head = str(git("rev-parse", "HEAD")).strip()
    if revision is not None:
        ok = head == revision; checks.append({"check": "exact_revision", "passed": ok})
        if not ok: issues.append("exact_revision")
    if require_clean:
        clean = not str(git("status", "--porcelain=v1")).strip(); checks.append({"check": "clean_state", "passed": clean})
        if not clean: issues.append("clean_state")
    if mode == "minimal":
        return {"schema": "ghc.family.v646-v4.minimal-validation.v1", "mode": mode, "head": head, "check_count": len(checks), "checks": checks, "issue_count": len(issues), "issues": list(dict.fromkeys(issues)), "valid": not issues, "passed": not issues, "boundary": BOUNDARY}
    ledger = load("x2-proposal-ledger.json")
    for row in ledger.get("proposals", []):
        for key in ("proposal_id", "title", "outcome", "primary_artifact", "vector_artifact", "boundary"):
            ok = bool(row.get(key)); checks.append({"check": f"proposal_{row.get('proposal_id')}_{key}", "passed": ok})
            if not ok: issues.append(f"proposal_{row.get('proposal_id')}_{key}")
        for artifact_key in ("primary_artifact", "vector_artifact"):
            exists = (PHASE / row[artifact_key]).is_file(); checks.append({"check": f"artifact_{row['proposal_id']}_{artifact_key}", "passed": exists})
            if not exists: issues.append(f"artifact_{row['proposal_id']}_{artifact_key}")
        if (PHASE / row["primary_artifact"]).is_file():
            payload = load(row["primary_artifact"]); ok = payload.get("passed") is True and payload.get("outcome") == row.get("outcome")
            checks.append({"check": f"core_{row['proposal_id']}_passed", "passed": ok})
            if not ok: issues.append(f"core_{row['proposal_id']}_passed")
    for row in load("validation/x2-synthetic-negative-register.json").get("rows", []):
        ok = row.get("expected") == row.get("observed") == "rejected" and row.get("result") == "pass" and row.get("independent_reproduction") is False
        checks.append({"check": f"mutation_{row.get('negative_id')}", "passed": ok})
        if not ok: issues.append(f"mutation_{row.get('negative_id')}")
    for relative, expected in (("approval-packets/x2-safe-now-execution.json", 30), ("prototypes/x2-candidate-execution.json", 20), ("maintenance/x2-clean-refine-ledger.json", 30)):
        payload = load(relative)
        for row in payload.get("tasks", []):
            ok = row.get("state") == "completed" and (PHASE / row.get("artifact", "missing")).is_file()
            checks.append({"check": f"portfolio_{row.get('packet_id')}", "passed": ok})
            if not ok: issues.append(f"portfolio_{row.get('packet_id')}")
        if len(payload.get("tasks", [])) != expected: issues.append(f"portfolio_count_{relative}")
    protected = load("approval-packets/x2-protected-packet-register.json")
    protected_ok = protected.get("inherited_exact_count") == 10 and protected.get("inherited_blocked_count") == 5 and protected.get("executed") == 0 and protected.get("relabelled_safe_now") == 0
    checks.append({"check": "protected_packets_unexecuted", "passed": protected_ok})
    if not protected_ok: issues.append("protected_packets_unexecuted")
    json_files = sorted(PHASE.rglob("*.json")); json_issues = []
    for path in json_files:
        try: json.loads(path.read_text(encoding="utf-8")); ok = True
        except Exception as exc: ok = False; json_issues.append({"path": path.relative_to(ROOT).as_posix(), "error": str(exc)})
        checks.append({"check": f"json_{path.relative_to(PHASE).as_posix()}", "passed": ok})
    if json_issues: issues.append("json_parse")
    privacy_hits = []
    files = phase_files()
    for path in files:
        try: payload = path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        found = scan_text(path.relative_to(ROOT).as_posix(), payload); privacy_hits.extend(found)
        checks.append({"check": f"privacy_{path.relative_to(PHASE).as_posix()}", "passed": not found})
    if privacy_hits: issues.append("privacy_hits")
    word_issues = []
    for path in PHASE.rglob("*.md"):
        words = len(path.read_text(encoding="utf-8").split()); ok = words <= 6000
        checks.append({"check": f"word_cap_{path.relative_to(PHASE).as_posix()}", "passed": ok})
        if not ok: word_issues.append({"path": path.relative_to(ROOT).as_posix(), "words": words})
    if word_issues: issues.append("word_cap")
    report = (PHASE / "deliverables/v646-v4-static-report.html").read_text(encoding="utf-8")
    for token in ("<caption>", "scope=\"col\"", "scope='row'", "aria-labelledby=\"chart-title chart-desc\"", "data-table-ref=\"#outcome-table\"", "Skip to main content", "tabindex=\"0\"", "affected-user evaluation remain reserved"):
        ok = token in report; checks.append({"check": f"report_{hashlib.sha256(token.encode()).hexdigest()[:8]}", "passed": ok})
        if not ok: issues.append(f"report_missing_{token}")
    stale_checks = {
        "route_not_sent": load("orchestration/terminal-route-plan.json").get("current_state") == "PREPARED_NOT_SENT",
        "truth_not_stage20": load("phase-truth.json").get("terminal_verdict") == "NOT_READY_FOR_STAGE_20",
        "no_independent_reproduction": load("phase-truth.json").get("independent_reproduction") is False,
        "runners_state_known": load("phase-truth.json").get("runners_aggregate_use_pending") in {True, False},
    }
    for name, ok in stale_checks.items():
        checks.append({"check": f"stale_{name}", "passed": ok})
        if not ok: issues.append(f"stale_{name}")
    manifest_results = []
    if revision and (PHASE / "validation/evidence-staged-manifest.json").is_file():
        evidence_revision = revision
        if (PHASE / "closeout-receipt.json").is_file(): evidence_revision = load("closeout-receipt.json").get("evidence_commit", revision)
        count, mismatch = verify_manifest("validation/evidence-staged-manifest.json", evidence_revision)
        manifest_results.append({"manifest": "evidence", "entries": count, "revision": evidence_revision, "mismatches": mismatch})
        checks.append({"check": "evidence_manifest_parity", "passed": not mismatch})
        if mismatch: issues.append("evidence_manifest_parity")
    if revision and (PHASE / "validation/final-staged-manifest.json").is_file():
        count, mismatch = verify_manifest("validation/final-staged-manifest.json", revision)
        manifest_results.append({"manifest": "final", "entries": count, "revision": revision, "mismatches": mismatch})
        checks.append({"check": "final_manifest_parity", "passed": not mismatch})
        if mismatch: issues.append("final_manifest_parity")
    issues = list(dict.fromkeys(issues))
    return {
        "schema": "ghc.family.v646-v4.detailed-validation.v1", "mode": mode, "head": head,
        "check_count": len(checks), "checks": checks, "json_parse_count": len(json_files), "json_issues": json_issues,
        "privacy": {"pattern_classes": sorted(PRIVATE), "file_count": len(files), "confirmed_hits": privacy_hits, "confirmed_hit_count": len(privacy_hits), "boundary": "A bounded zero-hit scan is not complete privacy or security assurance."},
        "word_cap_issues": word_issues, "manifests": manifest_results, "commit_count_from_source": commit_count(),
        "merge_count_from_source": merge_count(), "issue_count": len(issues), "issues": issues,
        "valid": not issues, "passed": not issues, "boundary": BOUNDARY,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("minimal", "detailed"), default="detailed")
    parser.add_argument("--revision")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.mode, args.revision, args.require_clean)
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({"mode": args.mode, "head": result["head"], "checks": result["check_count"], "issues": result["issue_count"], "json": result.get("json_parse_count"), "privacy_files": result.get("privacy", {}).get("file_count"), "privacy_hits": result.get("privacy", {}).get("confirmed_hit_count"), "valid": result["valid"]}))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
