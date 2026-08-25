#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Tamar v669-v1."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Tamar Vey"
PHASE = "v669-v1"
BRANCH = "codex/GHC-Family/tamar-vey-v669-v1-full-tools"
PREFIX = "docs/tamar-vey/v669-v1/"
SOURCE = "bb475c084da39512dfa0811a8520a40fd3d4c84a"
X1 = "f1a090e2396de5d76c70aa3bf7bda0a888b1249a"
EVIDENCE = "cf99dad5ec53f4af60017a829889087ed50cf752"
X1_MANIFEST = PREFIX + "validation/x1-manifest.json"
X2_MANIFEST = PREFIX + "x2/evidence/evidence-content-manifest.json"
OWNER_MANIFEST = PREFIX + "validation/final-owner-manifest.json"
DELTA_MANIFEST = PREFIX + "validation/final-delta-manifest.json"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


def run_git(*args: str, check: bool = True, binary: bool = True, timeout: int = 240) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=check, capture_output=True, text=not binary, timeout=timeout)


def git_text(*args: str) -> str:
    return run_git(*args, binary=False).stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class GitBatch:
    def __init__(self) -> None:
        self.process = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def read_exact(self, size: int) -> bytes:
        assert self.process.stdout is not None
        chunks, remaining = [], size
        while remaining:
            chunk = self.process.stdout.read(remaining)
            if not chunk:
                raise RuntimeError(f"unexpected Git batch EOF with {remaining} bytes remaining")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def blob(self, object_name: str) -> tuple[str, bytes]:
        assert self.process.stdin is not None and self.process.stdout is not None
        self.process.stdin.write((object_name + "\n").encode("utf-8"))
        self.process.stdin.flush()
        header = self.process.stdout.readline().decode("ascii").rstrip("\n")
        parts = header.split(" ")
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected Git batch header for requested owner blob: {header}")
        oid, _, size_text = parts
        payload = self.read_exact(int(size_text))
        if self.read_exact(1) != b"\n":
            raise RuntimeError("Git batch terminator mismatch")
        return oid, payload

    def close(self) -> None:
        assert self.process.stdin is not None and self.process.stderr is not None
        self.process.stdin.close()
        stderr = self.process.stderr.read().decode("utf-8", "replace")
        rc = self.process.wait()
        if rc != 0 or stderr:
            raise RuntimeError(f"Git batch close failed rc={rc}")


def commit_json(batch: GitBatch, commit: str, path: str) -> dict[str, Any]:
    _, data = batch.blob(f"{commit}:{path}")
    return json.loads(data.decode("utf-8"))


def replay_manifest(batch: GitBatch, commit: str, path: str) -> dict[str, Any]:
    manifest = commit_json(batch, commit, path)
    mismatches = []
    for row in manifest["entries"]:
        oid, data = batch.blob(f"{commit}:{row['path']}")
        if oid != row["git_blob_oid"] or len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            mismatches.append(row["path"])
    return {
        "path": path,
        "entries": len(manifest["entries"]),
        "self_exclusions": len(manifest.get("self_exclusions", [])),
        "coverage_count": manifest.get("coverage_count", len(manifest["entries"]) + len(manifest.get("self_exclusions", []))),
        "mismatch_count": len(mismatches),
        "mismatch_sample": mismatches[:10],
    }


def privacy_patterns() -> dict[str, re.Pattern[str]]:
    raw_terms = ["source" + "_thread" + "_id", "session" + "_meta.payload.id", "response" + "_item", "<" + "codex" + "_delegation"]
    return {
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:\\(?:Users|GHC-Archives)\\"),
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_route_identifier": re.compile("|".join(re.escape(term) for term in raw_terms), re.IGNORECASE),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[^\s,;}]+"),
        "email_address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    }


def scan_owner(batch: GitBatch, final: str, paths: list[str]) -> dict[str, Any]:
    patterns = privacy_patterns()
    privacy_candidates = []
    json_count = markdown_count = html_count = yaml_count = python_count = 0
    security_findings = []
    owner_mismatches, phase_mismatches, oversized = [], [], []
    maximum_words = 0
    for path in paths:
        _, data = batch.blob(f"{final}:{path}")
        suffix = Path(path).suffix.casefold()
        if suffix not in {".json", ".md", ".html", ".yaml", ".yml", ".py", ".txt"}:
            continue
        text = data.decode("utf-8")
        for line_number, line in enumerate(text.splitlines(), 1):
            for class_name, pattern in patterns.items():
                if pattern.search(line):
                    privacy_candidates.append({"class": class_name, "path": path, "line": line_number})
        if suffix == ".json":
            value = json.loads(text)
            json_count += 1
            if isinstance(value, dict) and value.get("owner", OWNER) != OWNER:
                owner_mismatches.append(path)
            if isinstance(value, dict) and value.get("phase", PHASE) != PHASE:
                phase_mismatches.append(path)
        elif suffix == ".md":
            markdown_count += 1
            if path.endswith("/SKILL.md"):
                if not text.startswith("---\n") or "\n# " not in text:
                    raise ValueError(f"invalid skill Markdown structure: {path}")
            elif not text.startswith("# "):
                raise ValueError(f"invalid Markdown heading: {path}")
        elif suffix == ".html":
            html_count += 1
            if "<html" not in text.casefold() or "<title>" not in text.casefold() or "<main" not in text.casefold():
                raise ValueError(f"invalid bounded HTML structure: {path}")
        elif suffix in {".yaml", ".yml"}:
            yaml_count += 1
            if "interface:" not in text or "display_name:" not in text or "default_prompt:" not in text:
                raise ValueError(f"invalid owner skill YAML structure: {path}")
        elif suffix == ".py":
            python_count += 1
            tree = ast.parse(text, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                    if any(name.split(".")[0] in {"requests", "socket", "urllib", "http", "ftplib"} for name in names):
                        security_findings.append({"path": path, "kind": "network_capable_import"})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "kind": "shell_enabled_subprocess"})
        if path.startswith(PREFIX) and suffix in {".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            words = len(re.findall(r"\b\w+[\w'-]*\b", text))
            maximum_words = max(maximum_words, words)
            if words > 6000:
                oversized.append({"path": path, "words": words})
    return {
        "owner_files_scanned": len(paths),
        "strict_json_count": json_count,
        "markdown_count": markdown_count,
        "html_count": html_count,
        "yaml_count": yaml_count,
        "python_ast_count": python_count,
        "privacy_classes": sorted(patterns),
        "raw_privacy_candidates": len(privacy_candidates),
        "confirmed_privacy_hits": len(privacy_candidates),
        "privacy_candidate_sample": privacy_candidates[:10],
        "security_findings": security_findings,
        "owner_label_mismatches": owner_mismatches,
        "phase_label_mismatches": phase_mismatches,
        "oversized_documents": oversized,
        "maximum_document_words": maximum_words,
    }


def run_tests() -> dict[str, Any]:
    expected = {
        "tests/test_ghc_family_tamar_vey_v669_v1_x1.py": 16,
        "tests/test_ghc_family_tamar_vey_v669_v1_x2.py": 18,
        "tests/test_ghc_family_tamar_vey_v669_v1_final.py": 15,
    }
    receipts, total = [], 0
    for path, expected_count in expected.items():
        result = subprocess.run([sys.executable, "-B", str(ROOT / path), "-v"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
        combined = result.stdout + "\n" + result.stderr
        match = re.search(r"Ran (\d+) tests", combined)
        count = int(match.group(1)) if match else -1
        if result.returncode != 0 or count != expected_count or not re.search(r"\bOK\b", combined):
            raise ValueError(f"owner test module failed or count drifted: {Path(path).name}")
        total += count
        receipts.append({"module": Path(path).name, "tests": count, "return_code": result.returncode, "status": "OK"})
    return {"modules": receipts, "tests_run": total, "expected_tests": 49, "all_passed": total == 49}


def validate(final: str) -> dict[str, Any]:
    if git_text("rev-parse", "HEAD") != final or git_text("branch", "--show-current") != BRANCH:
        raise ValueError("exact head or branch mismatch")
    status_before = run_git("status", "--porcelain", "--untracked-files=all", binary=False).stdout.splitlines()
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_lines = run_git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}", binary=False).stdout.splitlines()
    if len(live_lines) != 1:
        raise ValueError("fresh live remote did not resolve exactly one branch head")
    live = live_lines[0].split()[0]
    ancestry = {
        "x1_parent_source": git_text("rev-parse", f"{X1}^") == SOURCE,
        "evidence_parent_x1": git_text("rev-parse", f"{EVIDENCE}^") == X1,
        "final_parent_evidence": git_text("rev-parse", f"{final}^") == EVIDENCE,
        "source_ancestral": run_git("merge-base", "--is-ancestor", SOURCE, final, check=False).returncode == 0,
        "x1_ancestral": run_git("merge-base", "--is-ancestor", X1, final, check=False).returncode == 0,
        "evidence_ancestral": run_git("merge-base", "--is-ancestor", EVIDENCE, final, check=False).returncode == 0,
        "owner_commits": int(git_text("rev-list", "--count", f"{SOURCE}..{final}")),
        "merge_count": len(git_text("rev-list", "--merges", f"{SOURCE}..{final}").splitlines()) if git_text("rev-list", "--merges", f"{SOURCE}..{final}") else 0,
        "final_parent_count": len(git_text("rev-list", "--parents", "-n", "1", final).split()) - 1,
    }
    batch = GitBatch()
    try:
        manifests = {
            "x1": replay_manifest(batch, X1, X1_MANIFEST),
            "x2": replay_manifest(batch, EVIDENCE, X2_MANIFEST),
            "final_owner": replay_manifest(batch, final, OWNER_MANIFEST),
            "final_delta": replay_manifest(batch, final, DELTA_MANIFEST),
        }
        owner_manifest = commit_json(batch, final, OWNER_MANIFEST)
        owner_paths = sorted({row["path"] for row in owner_manifest["entries"]} | set(owner_manifest["self_exclusions"]))
        scan = scan_owner(batch, final, owner_paths)
        phase_truth = commit_json(batch, final, PREFIX + "closeout/phase-truth.json")
        route = commit_json(batch, final, PREFIX + "route/terminal-route-state.json")
        outcomes = commit_json(batch, EVIDENCE, PREFIX + "x2/evidence/outcome-ledger.json")
    finally:
        batch.close()
    tests = run_tests()
    status_after = run_git("status", "--porcelain", "--untracked-files=all", binary=False).stdout.splitlines()
    outcome_counts = outcomes["counts"]
    checks = {
        "exact_head": git_text("rev-parse", "HEAD") == final,
        "clean_before": len(status_before) == 0,
        "clean_after": len(status_after) == 0,
        "zero_divergence": divergence == ["0", "0"],
        "four_way_equality": final == upstream == tracking == live,
        "exact_ancestry": all(value is True for key, value in ancestry.items() if key.endswith(("source", "x1", "evidence", "ancestral"))),
        "three_owner_commits": ancestry["owner_commits"] == 3,
        "zero_merges": ancestry["merge_count"] == 0,
        "one_final_parent": ancestry["final_parent_count"] == 1,
        "all_manifest_replays": all(row["mismatch_count"] == 0 for row in manifests.values()),
        "owner_manifest_coverage": manifests["final_owner"]["coverage_count"] == manifests["final_owner"]["entries"] + 3,
        "delta_manifest_coverage": manifests["final_delta"]["coverage_count"] == manifests["final_delta"]["entries"] + 3,
        "owner_tests_49": tests["all_passed"],
        "strict_json": scan["strict_json_count"] > 0,
        "zero_confirmed_privacy_hits": scan["confirmed_privacy_hits"] == 0,
        "zero_security_findings": len(scan["security_findings"]) == 0,
        "zero_owner_label_mismatches": len(scan["owner_label_mismatches"]) == 0,
        "zero_phase_label_mismatches": len(scan["phase_label_mismatches"]) == 0,
        "document_ceiling": len(scan["oversized_documents"]) == 0,
        "file_ceiling": scan["owner_files_scanned"] < 2000,
        "four_outcome_labels": outcome_counts == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "terminal_verdict": phase_truth["terminal_verdict"] == TERMINAL_VERDICT,
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and not route["successor_contacted"],
        "full_repository_suite_not_run": "not_run" in phase_truth["full_repository_suite"],
    }
    if not all(checks.values()):
        raise ValueError("one or more exact-final canonical checks failed")
    return {
        "schema": "ghc.family.tamar-vey.v669-v1.exact-final-canonical.v1",
        "owner": OWNER,
        "phase": PHASE,
        "exact_final": final,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "status": "PASS_EXACT_FINAL_OWNER_CANONICAL_ONCE",
        "canonical_invocation_count": 1,
        "canonical_success_count": 1,
        "canonical_replay_permitted": False,
        "checks": checks,
        "tests": tests,
        "manifests": manifests,
        "scan": scan,
        "ancestry": ancestry,
        "clean_state_before": len(status_before) == 0,
        "clean_state_after": len(status_after) == 0,
        "typed_divergence": {"ahead": int(divergence[0]), "behind": int(divergence[1])},
        "four_way_equal": final == upstream == tracking == live,
        "outcomes": outcome_counts,
        "effective_negatives": phase_truth["effective_negatives"],
        "methods": phase_truth["methods"],
        "failed_witnesses": phase_truth["failed_witnesses"],
        "passing_witnesses": phase_truth["passing_witnesses"],
        "open_gaps": phase_truth["open_gaps"],
        "exact_gates": phase_truth["exact_gates"],
        "full_repository_suite": False,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "boundary": "Bounded same-owner software validation under shared infrastructure only; not external audit, independent reproduction, empirical confirmation, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, legal or cultural authority, Māori-authority review, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.expected_head)
        return_code = 0
    except Exception:
        result = {
            "schema": "ghc.family.tamar-vey.v669-v1.exact-final-canonical.v1",
            "owner": OWNER,
            "phase": PHASE,
            "exact_final": args.expected_head,
            "status": "FAIL_EXACT_FINAL_OWNER_CANONICAL_ZERO_SUCCESS_CREDIT",
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "canonical_replay_permitted": False,
            "error": "canonical validation raised before a complete passing result; inspect the attributable process locally",
            "terminal_verdict": TERMINAL_VERDICT,
        }
        return_code = 1
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt = {**result, "canonical_payload_sha256": sha256(payload)}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": receipt["status"], "tests": (receipt.get("tests") or {}).get("tests_run"), "manifest_entries": sum(row.get("entries", 0) for row in (receipt.get("manifests") or {}).values()), "confirmed_privacy_hits": (receipt.get("scan") or {}).get("confirmed_privacy_hits"), "terminal_verdict": TERMINAL_VERDICT}, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
