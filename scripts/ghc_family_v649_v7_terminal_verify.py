#!/usr/bin/env python3
"""Verify the exact final v649-v7 head without rerunning the repository suite."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "eiren-kestrel" / "v649-v7"
SOURCE = "03191b37da8b2b071b721d4554583832d56be05b"
X1 = "b1b3a4bde8dee07bc2bd4f8fc2c8d4b511cd723f"
EVIDENCE = "825edd4288ea4d881e1cb93cc4732baae265e1c9"
CLOSEOUT = "4b562d70fa930d177931160909cb5b449efc4d5f"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def manifest(commit: str, relative: str) -> tuple[int, list[str]]:
    payload = json.loads(git("show", f"{commit}:docs/eiren-kestrel/v649-v7/{relative}"))
    mismatch = []
    for row in payload["entries"]:
        if git("rev-parse", f"{commit}:{row['path']}") != row["git_blob"]:
            mismatch.append(row["path"])
    return len(payload["entries"]), mismatch


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt)
    if receipt.exists():
        raise RuntimeError("terminal receipt already exists; repeat verification is prohibited")
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_rows = git("ls-remote", "--heads", "origin", branch).splitlines()
    live = live_rows[0].split("\t")[0] if len(live_rows) == 1 else ""
    phase_json = sorted(OUT.rglob("*.json"))
    json_errors = []
    for path in phase_json:
        try: json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc: json_errors.append({"path": path.relative_to(OUT).as_posix(), "error": type(exc).__name__})
    x1_count, x1_mis = manifest(X1, "validation/x1-staged-manifest.json")
    evidence_count, evidence_mis = manifest(EVIDENCE, "validation/evidence-staged-manifest.json")
    closeout_count, closeout_mis = manifest(CLOSEOUT, "validation/closeout-staged-manifest.json")
    final_count, final_mis = manifest(head, "validation/final-staged-manifest.json")
    owner = load("validation/final-owner-manifest.json")
    owner_blob, owner_checkout = [], []
    for row in owner["entries"]:
        if git("rev-parse", f"{head}:{row['path']}") != row["git_blob"]: owner_blob.append(row["path"])
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["checkout_sha256"]: owner_checkout.append(row["path"])
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    suite = load("validation/canonical-full-suite-result.json")
    truth = load("phase-truth-final.json")
    method = load("method-flow/method-flow-summary.json")
    baton_words = len((OUT / "handoffs" / "elaren-kestrel-v649-v8-activation.md").read_text(encoding="utf-8").split())
    word_violations = []
    for path in list(OUT.rglob("*.md")) + list(OUT.rglob("*.html")) + list(OUT.rglob("*.txt")):
        count = len(path.read_text(encoding="utf-8").split())
        if count > 20000: word_violations.append({"path": path.relative_to(OUT).as_posix(), "words": count})
    detailed = {
        "expected_head": head == args.expected_head, "clean": not git("status", "--porcelain"),
        "four_way": head == upstream == tracking == live,
        "source_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=ROOT).returncode == 0,
        "x1_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=ROOT).returncode == 0,
        "evidence_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=ROOT).returncode == 0,
        "closeout_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", CLOSEOUT, head], cwd=ROOT).returncode == 0,
        "four_commits": phase_commits == 4, "zero_merges": merges == 0,
        "one_parent": len(parents) == 2, "final_parent_closeout": len(parents) == 2 and parents[1] == CLOSEOUT,
        "all_json": not json_errors, "x1_manifest": not x1_mis, "evidence_manifest": not evidence_mis,
        "closeout_manifest": not closeout_mis, "final_manifest": not final_mis,
        "owner_blob": not owner_blob, "owner_checkout": not owner_checkout, "owner_threshold": owner["within_threshold"],
        "suite": suite["successful"] and suite["tests_run"] == 1943 and suite["successful_canonical_passes"] == 1 and not suite["post_success_replay"],
        "outcomes": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "negatives": truth["effective_negatives"] == 5330, "gates": truth["open_gaps"] == 41 and truth["exact_gates"] == 42,
        "method_flow": method["counts"]["methods"] == 19 and method["counts"]["witness_results"] == {"fail": 19, "pass": 19},
        "baton_words": 8000 <= baton_words <= 20000, "word_caps": not word_violations,
        "route_unsent": load("orchestration/terminal-route-state.json")["state"] == "PREPARED_NOT_SENT",
        "stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    minimal_names = ["expected_head", "clean", "four_way", "source_ancestral", "x1_ancestral", "evidence_ancestral", "closeout_ancestral", "four_commits", "zero_merges", "one_parent", "final_parent_closeout", "all_json", "owner_blob", "owner_checkout", "suite", "stage20"]
    minimal = {name: detailed[name] for name in minimal_names}
    passed = all(detailed.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.v649-v7.terminal-validation.external.v1", "passed": passed,
        "exact_final_head": head, "branch": branch, "detailed_passed": sum(detailed.values()),
        "detailed_total": len(detailed), "detailed_checks": detailed,
        "minimal_passed": sum(minimal.values()), "minimal_total": len(minimal), "minimal_checks": minimal,
        "json_parses": len(phase_json), "json_errors": json_errors,
        "manifest_entries": {"x1": x1_count, "evidence": evidence_count, "closeout": closeout_count, "final": final_count, "owner": owner["entry_count"]},
        "manifest_mismatches": {"x1": x1_mis, "evidence": evidence_mis, "closeout": closeout_mis, "final": final_mis, "owner_blob": owner_blob, "owner_checkout": owner_checkout},
        "full_repository_suite": {"tests": 1943, "failures": 0, "errors": 0, "skipped": 0, "successful_passes": 1, "failed_attempts_before_success": 1},
        "phase_commits": phase_commits, "merges": merges, "baton_words": baton_words,
        "local_upstream_tracking_live_equal": head == upstream == tracking == live,
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": passed, "detailed": f"{sum(detailed.values())}/{len(detailed)}", "minimal": f"{sum(minimal.values())}/{len(minimal)}", "json": len(phase_json), "manifests": payload["manifest_entries"]}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
