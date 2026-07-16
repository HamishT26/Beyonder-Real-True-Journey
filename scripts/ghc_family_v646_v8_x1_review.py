#!/usr/bin/env python3
"""Validate Ilyra Fen v646-v8 x1 and emit exact staged-blob receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"
PHASE_REL = Path("docs/ilyra-fen/v646-v8")
SOURCE = "bb3a661e70f1cf9b92e5293b2f5292393bd9a60f"
ALLOWED_SCRIPTS = {
    "scripts/build_ghc_family_v646_v8_preregistration.py",
    "scripts/ghc_family_v646_v8_definitions.py",
    "scripts/ghc_family_v646_v8_x1_review.py",
}
REQUIRED_PROPOSAL_FIELDS = {
    "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure", "approval_class",
    "execution_lane", "current_primary_or_official_source_needs", "concrete_artifacts",
    "test_falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
    "expected_disposition", "novelty_against_460_frozen_proposals",
}
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_uri": re.compile(r"(?i)(?:codex|app)" + r"://"),
    "delegation_markup": re.compile(r"<" + r"codex_delegation", re.I),
    "private_local_path": re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret)\s*[:=]\s*[\"'][^\"']+[\"']"),
}


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    cp = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=not binary, encoding=None if binary else "utf-8")
    if check and cp.returncode:
        raise RuntimeError((cp.stderr if not binary else cp.stderr.decode("utf-8", "replace")).strip())
    return cp.stdout


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def add(checks: list[dict[str, Any]], name: str, passed: bool, detail: Any = None) -> None:
    row = {"check": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)


def structural_checks() -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    issues: list[str] = []
    proposals = load("x1-proposals.json")
    rows = proposals["proposals"]
    add(checks, "source_exact", str(git("rev-parse", "HEAD")).strip() == SOURCE)
    add(checks, "proposal_count_10", len(rows) == 10)
    add(checks, "prior_count_460", proposals["prior_frozen_proposal_count"] == 460)
    add(checks, "frozen_after_470", proposals["frozen_chain_count_after_x1"] == 470)
    add(checks, "x1_only", proposals["x2_execution_present"] is False)
    add(checks, "proposal_fields", all(REQUIRED_PROPOSAL_FIELDS.issubset(row) for row in rows))
    outcomes = [row["expected_disposition"] for row in rows]
    add(checks, "outcome_vocabulary", set(outcomes) == {"completed", "represented", "open_gap", "exact_gate"})
    add(checks, "expected_distribution", {key: outcomes.count(key) for key in set(outcomes)} == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    collision = load("provenance/proposal-collision-audit.json")
    add(checks, "no_exact_title_collision", collision["exact_collision_count"] == 0)
    add(checks, "collision_rows_10", len(collision["rows"]) == 10)
    source = load("sources/source-ledger.json")
    add(checks, "source_count_18", len(source["sources"]) == 18)
    add(checks, "source_status_vocab", set(source["status_counts"]).issubset({"current", "stable", "draft", "watch"}))
    add(checks, "zero_real_evidence", all(source[key] == 0 for key in ("real_data_rows_ingested", "likelihood_evaluations", "real_participants", "real_keys_or_proofs", "real_aircraft_or_maintenance_actions")))
    add(checks, "safe_30", load("approval-packets/x1-approval-portfolio.json")["count"] == 30)
    add(checks, "candidate_20", load("prototypes/x1-candidate-plan.json")["count"] == 20)
    skill_plan = load("prototypes/x1-skill-runner-plan.json")
    add(checks, "skills_20", skill_plan["skill_count"] == 20)
    add(checks, "runners_10", skill_plan["runner_count"] == 10)
    add(checks, "cleanup_30", load("maintenance/x1-clean-refine-plan.json")["count"] == 30)
    protected = load("approval-packets/x1-protected-packet-register.json")
    add(checks, "protected_10_5_unexecuted", protected["exact_count"] == 10 and protected["blocked_count"] == 5 and protected["execution_credit"] == 0)
    add(checks, "synthetic_70_unexecuted", load("validation/x1-synthetic-mutation-plan.json")["count"] == 70 and load("validation/x1-synthetic-mutation-plan.json")["x2_execution_present"] is False)
    negatives = load("retained-negative-register.json")
    add(checks, "x1_negatives_6", negatives["x1_operational"] == 6)
    add(checks, "effective_negatives_3071", negatives["effective_total_at_x1"] == 3071)
    method = load("method-flow/method-flow-summary.json")
    add(checks, "method_flow_6_11", method["counts"]["methods"] == 6 and method["counts"]["witnesses"] == 11)
    add(checks, "method_failures_6_passes_5", method["counts"]["witness_results"] == {"fail": 6, "pass": 5})
    add(checks, "method_terminal_states", method["counts"]["states"]["candidate"] == 0 and method["counts"]["states"]["observed"] == 0)
    gates = load("x1-gate-carry-forward.json")
    add(checks, "gates_16_17", gates["inherited_open_gaps"] == 16 and gates["inherited_exact_gates"] == 17 and gates["closed_without_exact_evidence"] == 0)
    route = load("orchestration/terminal-route-plan.json")
    add(checks, "route_prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0)
    forbidden_paths = [p.relative_to(PHASE).as_posix() for p in PHASE.rglob("*") if p.is_file() and (p.name.startswith("x2-") or p.name in {"evidence-receipt.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"})]
    add(checks, "no_x2_or_closeout_paths", not forbidden_paths, forbidden_paths)
    for row in checks:
        if not row["passed"]:
            issues.append(row["check"])
    return checks, issues


def scan_blobs(blobs: dict[str, bytes]) -> tuple[int, list[dict[str, Any]], list[str]]:
    json_count = 0
    hits: list[dict[str, Any]] = []
    json_issues: list[str] = []
    for path, blob in blobs.items():
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if path.endswith(".json"):
            try:
                json.loads(text)
                json_count += 1
            except json.JSONDecodeError as exc:
                json_issues.append(f"{path}:{exc.lineno}:{exc.colno}")
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                hits.append({"path": path, "class": kind, "match_sha256": hashlib.sha256(match.group(0).encode("utf-8")).hexdigest()})
    return json_count, hits, json_issues


def worktree_blobs() -> dict[str, bytes]:
    paths = [p for p in PHASE.rglob("*") if p.is_file()]
    scripts = [ROOT / path for path in sorted(ALLOWED_SCRIPTS)]
    return {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in paths + scripts}


def staged_blobs() -> dict[str, bytes]:
    paths = [p for p in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if p]
    return {path: git("show", f":{path}", binary=True) for path in paths}


def review(mode: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
    checks, issues = structural_checks()
    blobs = staged_blobs() if mode == "staged" else worktree_blobs()
    json_count, hits, json_issues = scan_blobs(blobs)
    issues.extend(f"json:{item}" for item in json_issues)
    issues.extend(f"privacy:{row['class']}:{row['path']}" for row in hits)
    paths = sorted(blobs)
    if mode == "staged":
        unexpected = [path for path in paths if not (path.startswith(PHASE_REL.as_posix() + "/") or path in ALLOWED_SCRIPTS)]
        if unexpected:
            issues.extend(f"unexpected:{path}" for path in unexpected)
        manifest_rel = (PHASE_REL / "validation/x1-staged-manifest.json").as_posix()
        entries = [{"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()} for path, blob in sorted(blobs.items()) if path != manifest_rel]
        manifest = {
            "schema": "ghc.family.v646-v8.x1-staged-manifest.v1", "phase": "v646-gmut-thos-v8-x1-x2",
            "hash_domain": "exact staged Git-index blobs excluding this self-referential manifest",
            "entry_count": len(entries), "entries": entries,
            "boundary": "Exact staged-blob parity is bounded same-owner workflow evidence only.",
        }
    else:
        manifest = None
    payload = {
        "schema": f"ghc.family.v646-v8.x1-{mode}-review.v1", "mode": mode,
        "file_count": len(paths), "paths": paths, "structural_check_count": len(checks),
        "checks": checks, "json_parse_count": json_count, "json_issues": json_issues,
        "privacy_pattern_classes": sorted(PATTERNS), "privacy_confirmed_hit_count": len(hits),
        "privacy_confirmed_hits": hits, "issues": issues, "valid": not issues,
        "boundary": "This is bounded same-owner x1 workflow evidence, not complete privacy, exhaustive security, authority, production, accessibility, or independent reproduction.",
    }
    return payload, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("worktree", "staged"), default="worktree")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload, manifest = review(args.mode)
    if args.write:
        target = PHASE / "validation"
        target.mkdir(parents=True, exist_ok=True)
        (target / f"x1-{args.mode}-review.json").write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        if manifest is not None:
            (target / "x1-staged-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"mode": args.mode, "files": payload["file_count"], "checks": payload["structural_check_count"], "json": payload["json_parse_count"], "privacy_hits": payload["privacy_confirmed_hit_count"], "issues": len(payload["issues"]), "valid": payload["valid"]}, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
