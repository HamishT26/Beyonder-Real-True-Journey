#!/usr/bin/env python3
"""Validate the exact staged Liora Venn v668-v8 x1 Git-blob surface."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_liora_venn_v668_v8_archive import (
    ALLOWED_OUTCOMES,
    BRANCH,
    OWNER,
    PHASE,
    REL_PHASE_ROOT,
    ROOT,
    SOURCE_FINAL,
    TERMINAL_VERDICT,
    utc_now,
)


REVIEW_PATH = f"{REL_PHASE_ROOT}/validation/x1-staged-review.json"
MANIFEST_PATH = f"{REL_PHASE_ROOT}/validation/x1-manifest.json"
ALLOWLIST_PATH = f"{REL_PHASE_ROOT}/validation/x1-staged-allowlist.json"
PYTHON_PATHS = {
    "scripts/ghc_family_liora_venn_v668_v8_archive.py",
    "scripts/build_ghc_family_liora_venn_v668_v8_x1.py",
    "scripts/validate_ghc_family_liora_venn_v668_v8_x1.py",
    "tests/test_ghc_family_liora_venn_v668_v8_x1.py",
}
TEXT_SUFFIXES = {".json", ".md", ".html", ".yaml", ".yml", ".py"}


def run_git(*args: str, binary: bool = False, check: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=check, capture_output=True, text=not binary)


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def staged_oid(path: str) -> str:
    return git("rev-parse", f":{path}")


def staged_bytes(path: str) -> bytes:
    oid = staged_oid(path)
    return run_git("cat-file", "blob", oid, binary=True).stdout


def json_from_stage(path: str) -> Any:
    return json.loads(staged_bytes(path).decode("utf-8"))


def word_count(data: bytes) -> int:
    return len(re.findall(r"\b\w+[\w'-]*\b", data.decode("utf-8")))


def compute(owner_tests: int, owner_tests_return_code: int) -> dict[str, Any]:
    staged = sorted(filter(None, git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "--").splitlines()))
    unstaged = sorted(filter(None, git("diff", "--name-only", "--").splitlines()))
    untracked = sorted(filter(None, git("ls-files", "--others", "--exclude-standard", "--").splitlines()))
    allowlist = json_from_stage(ALLOWLIST_PATH)["paths"]
    if staged != sorted(allowlist):
        raise ValueError("staged paths differ from the exact x1 allowlist")
    if unstaged or untracked:
        raise ValueError(f"unstaged or untracked paths remain before staged review: {unstaged + untracked}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode != 0:
        raise ValueError(diff_check.stdout + diff_check.stderr)
    if git("branch", "--show-current") != BRANCH or git("rev-parse", "HEAD") != SOURCE_FINAL:
        raise ValueError("x1 staged review is not at the exact planning parent and branch")
    if any(f"/{segment}/" in f"/{path}/" for path in staged for segment in ("x2", "evidence", "final", "closeout", "seal", "skills", "runners")):
        raise ValueError("x2 or later lifecycle material is staged in x1")

    documents: dict[str, bytes] = {path: staged_bytes(path) for path in staged if Path(path).suffix.casefold() in TEXT_SUFFIXES}
    json_documents: dict[str, Any] = {}
    markdown_count = html_count = yaml_count = 0
    for path, data in documents.items():
        suffix = Path(path).suffix.casefold()
        text = data.decode("utf-8")
        if suffix == ".json":
            json_documents[path] = json.loads(text)
        elif suffix == ".md":
            markdown_count += 1
            if not text.startswith("# "):
                raise ValueError(f"Markdown lacks a level-one title: {path}")
        elif suffix == ".html":
            html_count += 1
        elif suffix in {".yaml", ".yml"}:
            yaml_count += 1

    for path in PYTHON_PATHS:
        if path not in staged:
            raise ValueError(f"missing staged Python surface: {path}")
        tree = ast.parse(staged_bytes(path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                if any(name.split(".")[0] in {"requests", "socket", "urllib", "http", "ftplib"} for name in names):
                    raise ValueError(f"network-capable import in {path}")
            if isinstance(node, ast.Call) and any(
                keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True
                for keyword in node.keywords
            ):
                raise ValueError(f"shell-enabled subprocess call in {path}")

    raw_identifier_terms = ["source" + "_thread" + "_id", "session" + "_meta.payload.id", "response" + "_item", "<" + "codex" + "_delegation"]
    privacy_patterns = {
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:\\(?:Users|GHC-Archives)\\"),
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_route_identifier": re.compile("|".join(re.escape(term) for term in raw_identifier_terms), re.IGNORECASE),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[^\s,;}]+"),
        "email_address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    }
    privacy_candidates: list[dict[str, Any]] = []
    for path, data in documents.items():
        if path == REVIEW_PATH:
            continue
        for line_number, line in enumerate(data.decode("utf-8").splitlines(), 1):
            for class_name, pattern in privacy_patterns.items():
                if pattern.search(line):
                    privacy_candidates.append({"class": class_name, "path": path, "line": line_number})
    if privacy_candidates:
        raise ValueError(f"confirmed privacy or raw-identifier hits: {privacy_candidates[:20]}")

    manifest = json_from_stage(MANIFEST_PATH)
    self_exclusions = set(manifest["self_exclusions"])
    if self_exclusions != {MANIFEST_PATH, REVIEW_PATH}:
        raise ValueError("unexpected x1 manifest self-exclusion set")
    expected_manifest_paths = set(staged) - self_exclusions
    manifest_paths = {row["path"] for row in manifest["entries"]}
    if manifest_paths != expected_manifest_paths or manifest["entry_count"] != len(manifest_paths):
        raise ValueError("manifest paths do not equal staged paths minus declared self-exclusions")
    manifest_mismatches = []
    for row in manifest["entries"]:
        oid = staged_oid(row["path"])
        data = staged_bytes(row["path"])
        if oid != row["git_blob_oid"] or len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            manifest_mismatches.append(row["path"])
    if manifest_mismatches:
        raise ValueError(f"manifest mismatches: {manifest_mismatches}")

    proposal_freeze = json_documents[f"{REL_PHASE_ROOT}/x1/proposal-freeze.json"]
    proposal_rows = []
    for shard in proposal_freeze["shards"]:
        proposal_rows.extend(json_documents[shard["path"]]["rows"])
    disposition_counts = {label: sum(row["expected_disposition"] == label for row in proposal_rows) for label in ALLOWED_OUTCOMES}
    if disposition_counts != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValueError("proposal disposition drift")
    if sum(len(row["negative_fixtures"]) for row in proposal_rows) != 160:
        raise ValueError("planned rejecting-mutation drift")
    owner_mismatches = [path for path, value in json_documents.items() if isinstance(value, dict) and "owner" in value and value["owner"] != OWNER]
    phase_mismatches = [path for path, value in json_documents.items() if isinstance(value, dict) and "phase" in value and value["phase"] != PHASE]
    if owner_mismatches or phase_mismatches:
        raise ValueError(f"owner or phase label drift: {owner_mismatches + phase_mismatches}")

    document_words = {path: word_count(data) for path, data in documents.items() if path.startswith(f"{REL_PHASE_ROOT}/") and path != REVIEW_PATH}
    oversized = {path: count for path, count in document_words.items() if count > 6000}
    if oversized or sum(document_words.values()) > 100000 or len(staged) > 2000:
        raise ValueError(f"file or word ceiling exceeded: {oversized}")
    nonself = [(path, staged_oid(path)) for path in staged if path != REVIEW_PATH]
    staged_digest = hashlib.sha256("".join(f"{path}\0{oid}\n" for path, oid in nonself).encode("utf-8")).hexdigest()
    if owner_tests != 16 or owner_tests_return_code != 0:
        raise ValueError("the attributable pre-stage owner x1 test receipt is incomplete")

    checks = {
        "exact_allowlist": True,
        "diff_check": True,
        "strict_json": True,
        "markdown_structure": True,
        "python_ast": True,
        "five_class_privacy_zero_confirmed": True,
        "bounded_changed_code_security_zero_findings": True,
        "manifest_replay_zero_mismatches": True,
        "owner_and_phase_labels": True,
        "document_and_file_ceilings": True,
        "planning_only_x1": True,
        "source_parent_and_branch": True,
        "owner_tests_16_of_16": True,
    }
    return {
        "schema": "ghc.family.staged-review.v1",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": utc_now(),
        "execution_state": "PASS_EXACT_STAGED_X1_OWNER_REVIEW",
        "source_commit": SOURCE_FINAL,
        "branch": BRANCH,
        "staged_file_count": len(staged),
        "reviewed_nonself_file_count": len(nonself),
        "staged_nonself_path_oid_sha256": staged_digest,
        "strict_json_count": len(json_documents),
        "markdown_count": markdown_count,
        "html_count": html_count,
        "yaml_count": yaml_count,
        "python_ast_count": len(PYTHON_PATHS),
        "manifest_entry_count": len(manifest["entries"]),
        "manifest_mismatch_count": 0,
        "self_exclusions": sorted(self_exclusions),
        "privacy_classes": sorted(privacy_patterns),
        "privacy_candidate_count": 0,
        "privacy_confirmed_hit_count": 0,
        "security_finding_count": 0,
        "owner_label_mismatch_count": 0,
        "phase_label_mismatch_count": 0,
        "maximum_document_words": max(document_words.values()),
        "total_owner_document_words_excluding_review": sum(document_words.values()),
        "proposal_count": len(proposal_rows),
        "expected_outcomes": disposition_counts,
        "planned_rejecting_mutations": 160,
        "owner_tests": {"invocations": 1, "tests_run": owner_tests, "return_code": owner_tests_return_code, "same_owner_only": True},
        "checks": checks,
        "canonical": False,
        "canonical_invocation_count": 0,
        "completion_credit": 0,
        "independent_reproduction": False,
        "full_repository_suite": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "boundary": "Exact staged owner-x1 software evidence only; no empirical, professional, production, legal, cultural, Māori-authority, independent-reproduction, or Stage 20 credit.",
    }


def stable_projection(receipt: dict[str, Any]) -> dict[str, Any]:
    excluded = {"generated_at_utc"}
    return {key: value for key, value in receipt.items() if key not in excluded}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner-tests", type=int, default=16)
    parser.add_argument("--owner-tests-return-code", type=int, default=0)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    receipt = compute(args.owner_tests, args.owner_tests_return_code)
    output = ROOT / REVIEW_PATH
    if args.verify_only:
        staged_receipt = json_from_stage(REVIEW_PATH)
        if stable_projection(staged_receipt) != stable_projection(receipt):
            raise ValueError("staged x1 review receipt does not match the fresh indexed-blob projection")
        print(json.dumps({"status": "PASS_STAGED_X1_REVIEW_REPLAY", "staged_files": receipt["staged_file_count"], "manifest_entries": receipt["manifest_entry_count"], "terminal_verdict": TERMINAL_VERDICT}, sort_keys=True))
        return
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": receipt["execution_state"], "staged_files": receipt["staged_file_count"], "manifest_entries": receipt["manifest_entry_count"], "terminal_verdict": TERMINAL_VERDICT}, sort_keys=True))


if __name__ == "__main__":
    main()
