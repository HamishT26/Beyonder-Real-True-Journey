#!/usr/bin/env python3
"""Validate the Eiren v648-v3 final candidate without rerunning tests or replay."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v648-v3"
OUTPUT = PHASE / "validation/final-precommit-gate.json"
SOURCE = "227a764b2bfad7a601bf45dcbacc1e37ffa5bb62"
X1 = "bd21b594451226294528f4f72f138bdada6cb3af"
EVIDENCE = "240aacba289cbc58280693395733da7b6450faa4"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def main() -> int:
    suite = load("validation/full-repository-suite.json")
    closeout = load("closeout-receipt.json")
    truth = load("phase-truth.json")
    route = load("orchestration/terminal-route-state.json")
    preparation = load("orchestration/successor-baton-preparation.json")
    protocol = load("validation/final-validation-protocol.json")
    replay = load("reproduction/same-owner-replay-plan.json")
    lifecycle = load("validation/lifecycle-operational-negatives.json")

    checks: dict[str, bool] = {
        "full_suite_owner": suite["owner"] == "Eiren Kestrel",
        "full_suite_canonical": suite["canonical"] is True and suite["suite_execution_count"] == 2 and suite["canonical_successful_execution_count"] == 1,
        "full_suite_passed": suite["successful"] is True and suite["failures"] == 0 and suite["errors"] == 0,
        "full_suite_bound_to_evidence_head": suite["evidence_head"] == EVIDENCE,
        "closeout_suite_parity": closeout["full_repository_suite_run"] is True and closeout["full_repository_suite_tests"] == suite["tests_run"],
        "no_replay": suite["replay_executed"] is False and closeout["replay_executed"] is False and replay["named_lane_count"] == 0,
        "zero_repeatability_credit": closeout["repeatability_credit"] == 0 and replay["repeatability_credit"] == 0,
        "no_independent_reproduction_claim": closeout["independent_reproduction"] is False and suite["independent_reproduction"] is False,
        "terminal_abstention": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and closeout["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "counts": closeout["effective_negatives"] == 4115 + lifecycle["count"] and (closeout["effective_open_gaps"], closeout["effective_exact_gates"]) == (28, 29),
        "route_prepared_unsent": route["state"] == "PREPARED_NOT_SENT" and route["message_sent"] is False,
        "successor_exact": (preparation["target_existing_task_title"], preparation["target_phase"]) == ("Ilyra Fen", "v648-gmut-thos-v4-x1-x2"),
        "postcommit_proof_not_preclaimed": protocol["completed"] is False and protocol["preclaims_exact_final_head"] is False,
        "replay_protocol_empty": protocol["named_replay_requirements"] == [],
        "commit_cap_precommit": int(git("rev-list", "--count", f"{SOURCE}..HEAD")) == 2,
        "no_merges": git("rev-list", "--count", "--merges", f"{SOURCE}..HEAD") == "0",
        "anchors": all(git("merge-base", "--is-ancestor", anchor, "HEAD") == "" for anchor in (SOURCE, X1, EVIDENCE)),
    }

    json_files = sorted(PHASE.rglob("*.json"))
    json_errors = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - retained in receipt on failure
            json_errors.append({"path": path.relative_to(PHASE).as_posix(), "error": type(exc).__name__})
    checks["all_existing_json_parse"] = not json_errors

    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+"),
        "delegation_markup": re.compile("<codex_" + "delegation", re.IGNORECASE),
        "private_uri": re.compile("(?:codex|app)" + r"://", re.IGNORECASE),
    }
    privacy_hits = []
    for path in sorted(item for item in PHASE.rglob("*") if item.is_file()):
        text = path.read_text(encoding="utf-8", errors="replace")
        for kind, pattern in patterns.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(PHASE).as_posix(), "class": kind})
    checks["five_class_privacy_clean"] = not privacy_hits

    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.suffix.lower() not in {".md", ".html"}:
            continue
        words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8", errors="replace")))
        documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words})
    checks["document_cap"] = bool(documents) and all(row["words"] <= 6000 for row in documents)

    valid = all(checks.values())
    payload = {
        "schema": "ghc.family.v648-v3.final-precommit-gate.v1",
        "valid": valid,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "json_files_parsed": len(json_files),
        "json_errors": json_errors,
        "privacy_pattern_classes": sorted(patterns),
        "privacy_hits": privacy_hits,
        "documents_checked": len(documents),
        "tests_rerun_by_this_gate": 0,
        "replay_executed": False,
        "repeatability_credit": 0,
        "boundary": "Precommit structural gate only; exact final-head, clean-state, live-remote equality, unique task resolution, and baton acknowledgement remain postcommit.",
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": valid, "checks": f"{payload['checks_passed']}/{payload['checks_total']}", "json": len(json_files), "privacy_hits": len(privacy_hits)}))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
