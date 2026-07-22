#!/usr/bin/env python3
"""Run the one credited exact-final Eiren v651-v5 (2) canonical aggregate."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/eiren-kestrel/v651-v5-2-remaster"
SOURCE = "2bb6aa2d5e8003c4cb522f798d59e7b7f123742c"
X1 = "d9e8cbf0063639aa0a6fb54c54a96683c587ce7e"
EVIDENCE = "c67ce592463450ccf9aee7d460210cddb467c5ca"
CLOSEOUT = "7758ed116115462d3814af784a234418861b3d45"
VALIDATION_FAILURE = "73365f50f096ef90d957f3a092fe83160acc9a89"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools"
PATTERNS = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def git(*args: str, binary: bool = False) -> str | bytes:
    proc = subprocess.run(["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def load_at(commit: str, path: str):
    return json.loads(git("show", f"{commit}:{path}"))


def tree_map(commit: str, prefix: str) -> dict[str, str]:
    raw = git("ls-tree", "-r", "-z", commit, "--", prefix, binary=True)
    result = {}
    for record in raw.split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            _mode, kind, oid = meta.decode("ascii").split()
            if kind == "blob":
                result[path.decode("utf-8")] = oid
    return result


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(oid + "\n" for oid in unique).encode("ascii"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    stream = io.BytesIO(proc.stdout)
    result = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode("ascii").split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected batch header: {header}")
        size = int(header[2])
        result[expected] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch terminator")
    return result


def manifest_check(commit: str, path: str, expected_paths: set[str]) -> dict:
    manifest = load_at(commit, path)
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    tree = tree_map(commit, "") if False else None
    blobs = batch_blobs([row["git_blob"] for row in manifest["entries"]])
    issues = []
    if declared != expected_paths:
        issues.append({"issue": "path_set", "missing": sorted(expected_paths - declared), "extra": sorted(declared - expected_paths)})
    for row in manifest["entries"]:
        observed_oid = git("rev-parse", f"{commit}:{row['path']}")
        data = blobs[row["git_blob"]]
        if observed_oid != row["git_blob"]:
            issues.append({"issue": "blob", "path": row["path"]})
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            issues.append({"issue": "content", "path": row["path"]})
    return {"path": path, "entries": len(manifest["entries"]), "self_exclusions": len(manifest["self_exclusions"]), "issues": issues, "valid": not issues}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists():
        raise SystemExit("refusing to overwrite an existing validation attempt")
    try:
        output.relative_to(REPO.resolve())
        raise SystemExit("validation output must remain outside the repository")
    except ValueError:
        pass
    output.parent.mkdir(parents=True, exist_ok=True)

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    clean_before = not bool(git("status", "--porcelain=v1"))
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    selection_policy = load_at(head, f"{PHASE_ROOT}/validation/final-selection-policy.json")
    prior_policy = load_at(head, "docs/eiren-kestrel/v651-v5/validation/final-selection-policy.json")
    exclusions = set(prior_policy["exact_lifecycle_exclusions"])

    prior_path = REPO / "scripts/ghc_family_v651_v5_final_validate.py"
    spec = importlib.util.spec_from_file_location("v651_v5_prior_validator", prior_path)
    prior = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(prior)
    selection, tests = prior.run_full_suite(exclusions)
    selection["current_exact_final_attempts"] = 2
    selection["failed_exact_final_attempts_retained"] = 1
    selection["credited_exact_final_passes"] = 1

    source_to_x1 = set(filter(None, git("diff", "--name-only", f"{SOURCE}..{X1}").splitlines()))
    x1_to_evidence = set(filter(None, git("diff", "--name-only", f"{X1}..{EVIDENCE}").splitlines()))
    evidence_to_final = set(filter(None, git("diff", "--name-only", f"{EVIDENCE}..{head}").splitlines()))
    owner_tree = set(tree_map(head, PHASE_ROOT))
    manifests = [
        manifest_check(X1, f"{PHASE_ROOT}/validation/x1-staged-manifest.json", source_to_x1),
        manifest_check(EVIDENCE, f"{PHASE_ROOT}/validation/evidence-staged-manifest.json", x1_to_evidence),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-delta-manifest.json", evidence_to_final),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-owner-manifest.json", owner_tree),
    ]

    owner_map = tree_map(head, PHASE_ROOT)
    owner_blobs = batch_blobs(list(owner_map.values()))
    json_count, json_issues, privacy_hits, word_issues = 0, [], [], []
    for path, oid in owner_map.items():
        data = owner_blobs[oid]
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
                json_count += 1
            except Exception as exc:
                json_issues.append({"path": path, "error": type(exc).__name__})
        code_domain = "/skills/" in path or path.endswith(".py")
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                if not code_domain:
                    privacy_hits.append({"path": path, "class": class_name, "offset": match.start()})
        if path.endswith((".md", ".html")):
            words = len(re.findall(r"\b[\w'-]+\b", data.decode("utf-8")))
            if words > 100000:
                word_issues.append({"path": path, "words": words})

    truth = load_at(head, f"{PHASE_ROOT}/final/phase-truth.json")
    negatives = load_at(head, f"{PHASE_ROOT}/final/retained-negative-register.json")
    gates = load_at(head, f"{PHASE_ROOT}/final/gate-register.json")
    methods = load_at(head, f"{PHASE_ROOT}/method-flow/method-flow-summary.json")
    route = load_at(head, f"{PHASE_ROOT}/orchestration/final-orchestration.json")
    caps = load_at(head, f"{PHASE_ROOT}/validation/final-document-cap-receipt.json")
    threshold = load_at(head, f"{PHASE_ROOT}/validation/final-owner-file-threshold.json")
    review = load_at(head, f"{PHASE_ROOT}/validation/final-staged-review.json")
    baton = git("show", f"{head}:{PHASE_ROOT}/handoffs/elaren-kestrel-v651-v6-activation.md")
    overview = git("show", f"{head}:{PHASE_ROOT}/overview/final-integrated-overview.md")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    baton_words = len(re.findall(r"\b[\w'-]+\b", baton))
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview))

    detailed = {
        "branch": branch == BRANCH,
        "clean_before": clean_before,
        "four_way_equality": head == upstream == tracking == live,
        "source_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=REPO).returncode == 0,
        "x1_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=REPO).returncode == 0,
        "evidence_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=REPO).returncode == 0,
        "closeout_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", CLOSEOUT, head], cwd=REPO).returncode == 0,
        "validation_failure_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", VALIDATION_FAILURE, head], cwd=REPO).returncode == 0,
        "five_commits_within_cap": phase_commits == 5 and phase_commits <= 6,
        "zero_merges": merges == 0,
        "one_final_parent": len(parents) == 2 and parents[1] == VALIDATION_FAILURE,
        "outcomes": truth["outcome_counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "negatives": negatives["effective"] == 7219 and negatives["no_failure_erased"],
        "gaps": gates["effective_open_gaps"] == 56 and gates["silently_closed"] == 0,
        "gates": gates["effective_exact_gates"] == 57 and gates["silently_closed"] == 0,
        "methods": methods["counts"]["methods"] == 19 and methods["counts"]["witness_results"] == {"fail": 25, "pass": 20} and methods["counts"]["states"]["preferred"] == 19,
        "x1_manifest": manifests[0]["valid"],
        "evidence_manifest": manifests[1]["valid"],
        "final_delta_manifest": manifests[2]["valid"],
        "final_owner_manifest": manifests[3]["valid"],
        "json": not json_issues,
        "privacy": not privacy_hits,
        "documents": not word_issues and 10000 <= baton_words <= 100000 and overview_words >= 1500 and caps["valid"],
        "owner_threshold": threshold["within_threshold"] and threshold["owner_generated_files_at_final_commit"] < 2000,
        "route": route["target_exact_title"] == "Elaren Kestrel" and route["target_phase"] == "v651-v6" and route["send_count"] == 0,
        "no_cli_sibling": truth["cli_siblings_spawned"] == 0,
        "full_suite": selection["canonical_successful_passes"] == 1 and selection["current_exact_final_attempts"] == 2 and selection["failed_exact_final_attempts_retained"] == 1 and tests["failures"] == 0 and tests["errors"] == 0,
        "exact_exclusions": len(exclusions) == selection_policy["exact_lifecycle_exclusion_count"] == 33,
        "no_replay": not truth["post_success_replay_run"],
        "stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "staged_review": review["valid"] and not review["unexpected_paths"],
    }
    minimal_names = ["clean_before", "four_way_equality", "source_ancestral", "x1_ancestral", "evidence_ancestral", "closeout_ancestral", "validation_failure_ancestral", "five_commits_within_cap", "zero_merges", "one_final_parent", "final_delta_manifest", "final_owner_manifest", "full_suite", "stage20"]
    minimal = {name: detailed[name] for name in minimal_names}
    clean_after = not bool(git("status", "--porcelain=v1"))
    issues = [name for name, value in detailed.items() if not value]
    if not clean_after:
        issues.append("clean_after")
    valid = not issues
    receipt = {
        "schema": "ghc.family.v651-v5-2.exact-final-validation.v1", "phase": "v651-v5-2-remaster", "owner": "Eiren Kestrel", "exact_head": head, "branch": branch,
        "selection": selection, "tests": tests,
        "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "json": {"parsed": json_count, "issues": json_issues},
        "privacy": {"files_scanned": len(owner_map), "pattern_classes": sorted(PATTERNS), "confirmed_hits": privacy_hits, "zero_confirmed_hits": not privacy_hits},
        "manifests": manifests,
        "documents": {"baton_words": baton_words, "overview_words": overview_words, "issues": word_issues},
        "history": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "closeout": CLOSEOUT, "validation_failure": VALIDATION_FAILURE, "final": head, "phase_commits": phase_commits, "commit_cap": 6, "merges": merges, "final_parent_count": len(parents) - 1},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "live": live, "all_equal": head == upstream == tracking == live},
        "clean_before": clean_before, "clean_after": clean_after, "full_repository_suite_run": True, "post_success_replay_run": False, "same_owner_only": True, "independent_reproduction": False,
        "issues": issues, "valid": valid, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": "One Eiren-owned exact-final complete-repository aggregate with the inherited exact lifecycle exclusion set. Same-owner validation is not independent-team reproduction or external audit.",
    }
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"head": head, "tests": f"{tests['passed']}/{tests['total']}", "detailed": f"{receipt['detailed']['passed']}/{receipt['detailed']['total']}", "minimal": f"{receipt['minimal']['passed']}/{receipt['minimal']['total']}", "json": json_count, "privacy_files": len(owner_map), "manifest_entries": sum(row["entries"] for row in manifests), "clean_before": clean_before, "clean_after": clean_after, "all_equal": receipt["equality"]["all_equal"], "valid": valid}))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
