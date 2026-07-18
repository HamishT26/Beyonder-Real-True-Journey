#!/usr/bin/env python3
"""Verify the immutable Eiren v649-v1 final head and write an external receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v649-v1"
PREFIX = "docs/eiren-kestrel/v649-v1/"
SOURCE = "1e916c0c6378a6f665c144aabbf8d25d6fdc8670"
X1 = "3a9f2ec098ee3844fa1933dcc9396302851ed5d1"
EVIDENCE = "060f57634b1660ee61b360168ee65337c10d4a76"
PRIVACY = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\Users\\|/Users/|/home/)[^\s\"']+", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|vscode|file)://", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|secret|token)\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
    "delegation_markup": re.compile(rb"<\/?codex_delegation\b", re.I),
}


def git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=text).stdout


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def manifest_parity(commit: str, relative: str) -> tuple[int, list[str]]:
    payload = json.loads(str(git("show", f"{commit}:{PREFIX}{relative}")))
    mismatches = []
    for row in payload["entries"]:
        observed = str(git("rev-parse", f"{commit}:{row['path']}")).strip()
        if observed != row["git_blob"]:
            mismatches.append(row["path"])
    return len(payload["entries"]), mismatches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--suite-receipt", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    output = Path(args.receipt)
    if output.exists():
        raise RuntimeError("terminal receipt already exists; repeat verification is prohibited")
    suite = json.loads(Path(args.suite_receipt).read_text(encoding="utf-8"))
    head = str(git("rev-parse", "HEAD")).strip()
    branch = str(git("branch", "--show-current")).strip()
    upstream = str(git("rev-parse", "@{u}")).strip()
    tracking = str(git("rev-parse", f"refs/remotes/origin/{branch}")).strip()
    live_lines = str(git("ls-remote", "--heads", "origin", branch)).splitlines()
    live = live_lines[0].split("\t")[0] if len(live_lines) == 1 else ""
    parent_line = str(git("rev-list", "--parents", "-n", "1", head)).strip().split()
    phase_files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    json_files = [path for path in phase_files if path.suffix.lower() == ".json"]
    json_errors = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_errors.append({"path": path.relative_to(PHASE).as_posix(), "error": type(exc).__name__})

    public_files = list(phase_files)
    public_files.extend(sorted((ROOT / "scripts").glob("*v649_v1*.py")))
    public_files.extend(sorted((ROOT / "tests").glob("test_ghc_family_v649_v1*.py")))
    public_files = sorted(set(public_files))
    candidates = []
    definitions = []
    confirmed = []
    for path in public_files:
        data = path.read_bytes()
        relative = path.relative_to(ROOT).as_posix()
        for name, pattern in PRIVACY.items():
            for match in pattern.finditer(data):
                start = data.rfind(b"\n", 0, match.start()) + 1
                end = data.find(b"\n", match.end())
                if end < 0:
                    end = len(data)
                line = data[start:end]
                row = {"path": relative, "pattern_class": name}
                candidates.append(row)
                if relative.startswith("scripts/") and b"re.compile(" in line:
                    definitions.append(row)
                else:
                    confirmed.append(row)

    x1_count, x1_mismatch = manifest_parity(X1, "validation/x1-staged-manifest.json")
    evidence_count, evidence_mismatch = manifest_parity(EVIDENCE, "validation/evidence-staged-manifest.json")
    final_count, final_mismatch = manifest_parity(head, "validation/final-staged-manifest.json")
    final_manifest = load("validation/final-staged-manifest.json")
    final_changed = set(filter(None, str(git("diff-tree", "--no-commit-id", "--name-only", "-r", head)).splitlines()))
    final_covered = {row["path"] for row in final_manifest["entries"]} | set(final_manifest["self_exclusions"])

    owner = load("validation/final-owner-manifest.json")
    owner_blob_mismatch = []
    owner_checkout_mismatch = []
    for row in owner["entries"]:
        observed = str(git("rev-parse", f"{head}:{row['path']}")).strip()
        if observed != row["git_blob"]:
            owner_blob_mismatch.append(row["path"])
        checkout = (ROOT / row["path"]).read_bytes()
        if hashlib.sha256(checkout).hexdigest() != row["checkout_sha256"]:
            owner_checkout_mismatch.append(row["path"])

    stale_targets = [
        PHASE / "integrated-overview.md", PHASE / "accessible-report.html",
        PHASE / "wellbeing-check.md", PHASE / "closeout-receipt.json",
        PHASE / "seal-receipt.json", PHASE / "final-receipt.json",
        PHASE / "handoffs/ilyra-fen-v649-v2-activation.md",
        ROOT / "scripts/build_ghc_family_v649_v1_closeout.py",
        ROOT / "tests/test_ghc_family_v649_v1_closeout.py",
    ]
    stale_terms = ("MIGHTEE", "drinking-water treatment", "PCAPNG", "Haag-Ruelle", "resource-indicator profile")
    stale_hits = []
    for path in stale_targets:
        text = path.read_text(encoding="utf-8")
        for term in stale_terms:
            if term in text:
                stale_hits.append({"path": path.relative_to(ROOT).as_posix(), "term": term})

    word_violations = []
    for path in phase_files:
        if path.suffix.lower() in {".md", ".html", ".txt"}:
            count = len(path.read_text(encoding="utf-8").split())
            if count > 6000:
                word_violations.append({"path": path.relative_to(PHASE).as_posix(), "words": count})

    diff_check = subprocess.run(["git", "diff", "--check", f"{SOURCE}..{head}"], cwd=ROOT, capture_output=True).returncode == 0
    anchors = {anchor: subprocess.run(["git", "merge-base", "--is-ancestor", anchor, head], cwd=ROOT).returncode == 0 for anchor in (SOURCE, X1, EVIDENCE)}
    phase_commits = int(str(git("rev-list", "--count", f"{SOURCE}..{head}")).strip())
    merges = int(str(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}")).strip())
    clean = not str(git("status", "--porcelain")).strip()
    four_way = head == upstream == tracking == live
    suite_ok = suite.get("successful") is True and suite.get("exact_head") == head and suite.get("canonical_successful_passes") == 1 and suite.get("replay_runs") == 0
    method_summary = load("method-flow/method-flow-summary.json")
    phase_truth = load("phase-truth-final-candidate.json")
    detailed = {
        "suite_success": suite_ok,
        "exact_head": head == args.expected_head,
        "clean": clean,
        "four_way": four_way,
        "divergence_zero": str(git("rev-list", "--left-right", "--count", "HEAD...@{u}")).strip().replace("\t", " ") == "0 0",
        "source_ancestral": anchors[SOURCE], "x1_ancestral": anchors[X1], "evidence_ancestral": anchors[EVIDENCE],
        "three_phase_commits": phase_commits == 3, "zero_merges": merges == 0,
        "one_parent": len(parent_line) == 2, "final_parent_evidence": len(parent_line) == 2 and parent_line[1] == EVIDENCE,
        "all_json": not json_errors, "privacy_zero_confirmed": not confirmed,
        "x1_manifest": not x1_mismatch, "evidence_manifest": not evidence_mismatch,
        "final_manifest": not final_mismatch, "final_changed_covered": final_changed == final_covered,
        "owner_blob_manifest": not owner_blob_mismatch, "owner_checkout_manifest": not owner_checkout_mismatch,
        "owner_threshold": owner["within_threshold"], "word_caps": not word_violations,
        "stale_labels": not stale_hits, "diff_hygiene": diff_check,
        "outcomes": phase_truth["outcomes"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "negative_total": phase_truth["effective_negatives"] == 4742,
        "open_gaps": phase_truth["effective_open_gaps"] == 35,
        "exact_gates": phase_truth["effective_exact_gates"] == 36,
        "method_failures": method_summary["counts"]["witness_results"] == {"fail": 7, "pass": 7},
        "no_replay": load("reproduction/no-replay-plan.json")["named_lane_count"] == 0,
        "route_unsent_in_repo": load("orchestration/terminal-route-state.json")["state"] == "PREPARED_NOT_SENT",
        "stage20_abstains": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    minimal_names = [
        "suite_success", "exact_head", "clean", "four_way", "source_ancestral",
        "x1_ancestral", "evidence_ancestral", "three_phase_commits", "zero_merges",
        "one_parent", "final_parent_evidence", "all_json", "privacy_zero_confirmed",
        "x1_manifest", "evidence_manifest", "final_manifest", "owner_blob_manifest",
        "owner_checkout_manifest", "diff_hygiene", "stage20_abstains",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    passed = all(detailed.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.v649-v1.terminal-validation.external.v1",
        "passed": passed, "exact_final_head": head, "branch": branch,
        "full_repository_suite": {key: suite[key] for key in ("tests_run", "failures", "errors", "skipped", "successful", "tests_excluded", "module_file_count")},
        "detailed_passed": sum(detailed.values()), "detailed_total": len(detailed),
        "detailed_checks": detailed, "minimal_passed": sum(minimal.values()),
        "minimal_total": len(minimal), "minimal_checks": minimal,
        "json_parses": len(json_files), "json_errors": json_errors,
        "privacy_scanned_files": len(public_files), "privacy_pattern_classes": len(PRIVACY),
        "privacy_candidates": len(candidates), "privacy_scanner_definition_candidates": len(definitions),
        "privacy_confirmed_hits": confirmed,
        "manifest_entries": {"x1": x1_count, "evidence": evidence_count, "final": final_count, "owner": owner["entry_count"]},
        "manifest_mismatches": {"x1": x1_mismatch, "evidence": evidence_mismatch, "final": final_mismatch, "owner_blob": owner_blob_mismatch, "owner_checkout": owner_checkout_mismatch},
        "stale_label_hits": stale_hits, "word_cap_violations": word_violations,
        "phase_commits": phase_commits, "merges": merges, "final_parent": parent_line[1] if len(parent_line) == 2 else None,
        "local_upstream_tracking_live_equal": four_way, "clean_before_after": clean,
        "canonical_successful_passes": 1 if suite_ok else 0, "replay_runs": 0,
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Exact-final same-owner validation under shared infrastructure; not independent reproduction, external audit, production certification, exhaustive security, complete privacy, complete accessibility, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"passed": passed, "tests": suite.get("tests_run"), "detailed": f"{sum(detailed.values())}/{len(detailed)}", "minimal": f"{sum(minimal.values())}/{len(minimal)}", "json": len(json_files), "privacy_files": len(public_files)}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
