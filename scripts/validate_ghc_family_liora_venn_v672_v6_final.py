"""One-shot external exact-final owner-scoped validator for Liora Venn v672-v6."""

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

from scripts import build_ghc_family_liora_venn_v672_v6_final as final


ROOT = final.ROOT
OWNER_PREFIX = "docs/liora-venn/v672-v6"
TEXT_SUFFIXES = {".md", ".json", ".html", ".yaml", ".yml", ".py", ".txt"}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}").stdout


def load_blob_json(commit: str, path: str) -> Any:
    return json.loads(blob(commit, path).decode("utf-8"))


def diff_paths(base: str, tip: str) -> set[str]:
    return set(filter(None, git_text("diff", "--name-only", base, tip).splitlines()))


def verify_manifest(commit: str, manifest_path: str, actual_paths: set[str]) -> dict[str, Any]:
    manifest = load_blob_json(commit, manifest_path)
    mismatches: list[dict[str, str]] = []
    for row in manifest["entries"]:
        data = blob(commit, row["path"])
        oid = git_text("rev-parse", f"{commit}:{row['path']}")
        observed = {"git_blob_oid": oid, "bytes": len(data), "sha256": sha256(data)}
        expected = {"git_blob_oid": row["git_blob_oid"], "bytes": row["bytes"], "sha256": row["sha256"]}
        if observed != expected:
            mismatches.append({"path": row["path"], "issue": "blob_identity_mismatch"})
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    return {
        "path": manifest_path,
        "entries": manifest["entry_count"],
        "self_exclusions": len(manifest["self_exclusions"]),
        "blob_mismatches": mismatches,
        "coverage_missing": sorted(actual_paths - declared),
        "coverage_extra": sorted(declared - actual_paths),
        "valid": (
            manifest["hash_domain"] == "normalized_lf_exact_git_blob"
            and manifest["entry_count"] == len(manifest["entries"])
            and not mismatches
            and declared == actual_paths
        ),
    }


def run_owner_tests() -> dict[str, Any]:
    command = [
        sys.executable,
        "-X",
        "utf8",
        "-m",
        "unittest",
        "tests.test_ghc_family_liora_venn_v672_v6_final",
        "-v",
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=240)
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    count = int(match.group(1)) if match else 0
    return {
        "selection": ["tests.test_ghc_family_liora_venn_v672_v6_final"],
        "tests": count,
        "exit_code": result.returncode,
        "output_sha256": sha256(combined.encode("utf-8")),
        "output_tail_on_failure": combined[-3000:] if result.returncode else "",
        "valid": result.returncode == 0 and count == 30,
    }


def privacy_scan(commit: str, paths: set[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{5,}-[a-f0-9-]{12,}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\\\|C:/Users/|D:/GHC-Archives/)", re.I),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "private_callable_identifier": re.compile(r"\b(?:mcp__|codex_app__)[A-Za-z0-9_]+\b"),
        "personal_identifier": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b\+?\d[\d ()-]{8,}\d\b", re.I),
    }
    scanner_sources = {
        "scripts/build_ghc_family_liora_venn_v672_v6_final.py",
        "scripts/validate_ghc_family_liora_venn_v672_v6_final.py",
        "tests/test_ghc_family_liora_venn_v672_v6_final.py",
        "tests/test_ghc_family_liora_venn_v672_v6_x1.py",
        "tests/test_ghc_family_liora_venn_v672_v6_x2.py",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for path in sorted(paths):
        if Path(path).suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = blob(commit, path).decode("utf-8")
        except UnicodeDecodeError:
            confirmed.append({"class": "non_utf8_owner_text", "path": path, "classification": "confirmed_payload"})
            continue
        scanned += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                line_start = text.rfind("\n", 0, match.start()) + 1
                line_end = text.find("\n", match.end())
                if line_end < 0:
                    line_end = len(text)
                line = text[line_start:line_end]
                definition = path in scanner_sources and ("re.compile(" in line or path.startswith("tests/"))
                row = {
                    "class": class_name,
                    "path": path,
                    "classification": "scanner_definition_or_synthetic_test" if definition else "confirmed_payload",
                }
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    return {
        "pattern_classes": sorted(patterns),
        "scanned_text_files": scanned,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "valid": not confirmed,
        "boundary": "Bounded five-class owner-surface scan; not complete privacy assurance.",
    }


def compile_and_security_scan(commit: str, paths: set[str]) -> dict[str, Any]:
    python_paths = sorted(path for path in paths if path.endswith(".py"))
    compile_issues: list[dict[str, str]] = []
    security_findings: list[dict[str, str]] = []
    for path in python_paths:
        try:
            source = blob(commit, path).decode("utf-8")
            tree = ast.parse(source, filename=path)
            compile(source, path, "exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            compile_issues.append({"path": path, "issue": type(exc).__name__})
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                security_findings.append({"path": path, "issue": f"dynamic_{node.func.id}"})
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.value.id == "os" and node.func.attr == "system":
                    security_findings.append({"path": path, "issue": "os_system"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    security_findings.append({"path": path, "issue": "subprocess_shell_true"})
    return {
        "compiled": len(python_paths) - len(compile_issues),
        "total": len(python_paths),
        "compile_issues": compile_issues,
        "bounded_security_findings": security_findings,
        "valid": not compile_issues and not security_findings,
        "boundary": "AST and compile checks over changed Python only; not exhaustive security review.",
    }


def document_checks(commit: str, owner_paths: list[str]) -> dict[str, Any]:
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    markdown_paths = [path for path in owner_paths if path.endswith(".md")]
    html_paths = [path for path in owner_paths if path.endswith(".html")]
    json_issues: list[dict[str, str]] = []
    structure_issues: list[dict[str, str]] = []
    oversized: list[dict[str, Any]] = []
    maximum_words = 0
    for path in owner_paths:
        if Path(path).suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = blob(commit, path).decode("utf-8")
        except UnicodeDecodeError:
            structure_issues.append({"path": path, "issue": "non_utf8_text"})
            continue
        words = len(text.split())
        maximum_words = max(maximum_words, words)
        if words > 100000:
            oversized.append({"path": path, "words": words})
        if path.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError:
                json_issues.append({"path": path, "issue": "JSONDecodeError"})
        if path.endswith(".md"):
            headings = [line for line in text.splitlines() if line.startswith("#")]
            if not headings or not headings[0].startswith("# "):
                structure_issues.append({"path": path, "issue": "missing_h1"})
        if path.endswith(".html"):
            required = ('lang="en"', "<main", "<h1")
            if any(token not in text for token in required):
                structure_issues.append({"path": path, "issue": "missing_static_accessibility_structure"})
    return {
        "json": {"parsed": len(json_paths) - len(json_issues), "total": len(json_paths), "issues": json_issues},
        "markdown_documents": len(markdown_paths),
        "html_documents": len(html_paths),
        "structure_issues": structure_issues,
        "oversized_documents": oversized,
        "maximum_document_words": maximum_words,
        "valid": not json_issues and not structure_issues and not oversized,
        "boundary": "Static structure and size checks only; not affected-user accessibility evaluation.",
    }


def canonical(output: Path) -> dict[str, Any]:
    if output.exists():
        raise RuntimeError("one-shot output path already exists; replay refused")
    try:
        output.resolve().relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        raise RuntimeError("external canonical receipt must remain outside the repository")

    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    parent_fields = git_text("rev-list", "--parents", "-n", "1", head).split()
    status_before = git_text("status", "--porcelain=v1")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_rows[0] if live_rows else ""
    divergence = git_text("rev-list", "--left-right", "--count", "@{u}...HEAD").split()
    phase_commits = int(git_text("rev-list", "--count", f"{final.SOURCE_FINAL}..{head}"))
    merges = int(git_text("rev-list", "--merges", "--count", f"{final.SOURCE_FINAL}..{head}"))

    x1_paths = diff_paths(final.SOURCE_FINAL, final.X1_COMMIT)
    evidence_paths = diff_paths(final.X1_COMMIT, final.EVIDENCE_COMMIT)
    delta_paths = diff_paths(final.EVIDENCE_COMMIT, head)
    owner_paths_set = diff_paths(final.SOURCE_FINAL, head)
    owner_doc_paths = [path for path in git_text("ls-tree", "-r", "--name-only", head, OWNER_PREFIX).splitlines() if path]

    manifests = {
        "x1": verify_manifest(commit=final.X1_COMMIT, manifest_path="docs/liora-venn/v672-v6/validation/x1-manifest.json", actual_paths=x1_paths),
        "evidence": verify_manifest(commit=final.EVIDENCE_COMMIT, manifest_path="docs/liora-venn/v672-v6/validation/evidence-manifest.json", actual_paths=evidence_paths),
        "final_delta": verify_manifest(commit=head, manifest_path="docs/liora-venn/v672-v6/validation/final-delta-manifest.json", actual_paths=delta_paths),
        "final_owner": verify_manifest(commit=head, manifest_path="docs/liora-venn/v672-v6/validation/final-owner-manifest.json", actual_paths=owner_paths_set),
    }

    seal = load_blob_json(head, "docs/liora-venn/v672-v6/seal/content-seal-candidate.json")
    seal_mismatches = []
    for row in seal["targets"]:
        data = blob(head, row["path"])
        if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            seal_mismatches.append(row["path"])

    truth = load_blob_json(head, "docs/liora-venn/v672-v6/closeout/phase-truth.json")
    negatives = load_blob_json(head, "docs/liora-venn/v672-v6/closeout/retained-negative-register.json")
    gates = load_blob_json(head, "docs/liora-venn/v672-v6/closeout/gate-register.json")
    flow = load_blob_json(head, "docs/liora-venn/v672-v6/closeout/method-flow-final.json")
    lifecycle = load_blob_json(head, "docs/liora-venn/v672-v6/closeout/lifecycle-test-receipt.json")
    route = load_blob_json(head, "docs/liora-venn/v672-v6/orchestration/terminal-route-state.json")
    canonical_state = load_blob_json(head, "docs/liora-venn/v672-v6/final/canonical-invocation-state.json")
    staged_review = load_blob_json(head, "docs/liora-venn/v672-v6/validation/final-staged-review.json")
    staged_privacy = load_blob_json(head, "docs/liora-venn/v672-v6/validation/final-staged-privacy.json")
    prereceipt = load_blob_json(head, "docs/liora-venn/v672-v6/validation/final-validation-prereceipt.json")
    precommit = load_blob_json(head, "docs/liora-venn/v672-v6/validation/final-precommit-test-receipt.json")

    tests = run_owner_tests()
    privacy = privacy_scan(head, owner_paths_set)
    code = compile_and_security_scan(head, owner_paths_set)
    documents = document_checks(head, owner_doc_paths)
    counts = truth["effective_counts"]

    detailed = {
        "branch_exact": branch == final.BRANCH,
        "final_direct_child_of_evidence": parent == final.EVIDENCE_COMMIT,
        "x1_direct_child_of_source": git_text("rev-parse", f"{final.X1_COMMIT}^") == final.SOURCE_FINAL,
        "evidence_direct_child_of_x1": git_text("rev-parse", f"{final.EVIDENCE_COMMIT}^") == final.X1_COMMIT,
        "phase_commits_three": phase_commits == 3,
        "zero_merges": merges == 0,
        "one_final_parent": len(parent_fields) == 2,
        "clean_before": status_before == "",
        "typed_zero_divergence_before": divergence == ["0", "0"],
        "four_way_equal_before": head == upstream == tracking == live,
        "x1_manifest": manifests["x1"]["valid"] and manifests["x1"]["entries"] == 19 and manifests["x1"]["self_exclusions"] == 2,
        "evidence_manifest": manifests["evidence"]["valid"] and manifests["evidence"]["entries"] == 146 and manifests["evidence"]["self_exclusions"] == 2,
        "final_delta_manifest": manifests["final_delta"]["valid"] and manifests["final_delta"]["self_exclusions"] == 4,
        "final_owner_manifest": manifests["final_owner"]["valid"] and manifests["final_owner"]["self_exclusions"] == 4,
        "content_seal": seal["target_count"] == 10 == len(seal["targets"]) and not seal_mismatches,
        "owner_tests": tests["valid"],
        "documents": documents["valid"],
        "changed_python_compile_and_security": code["valid"],
        "privacy_zero_confirmed": privacy["valid"] and privacy["confirmed_hit_count"] == 0,
        "staged_review": staged_review["valid"] and not staged_review["deletions"] and not staged_review["unexpected_paths"] and not staged_review["frozen_x1_or_x2_changes"],
        "staged_privacy": staged_privacy["valid"] and staged_privacy["confirmed_hit_count"] == 0,
        "prereceipt_pending": prereceipt["final"] == "PENDING_FINAL_COMMIT" and not prereceipt["canonical_invoked"],
        "precommit_tests": precommit["valid"] and precommit["tests"] == 30 and precommit["credited_runs"] == 1 and not precommit["replayed"],
        "canonical_latch_pending_at_commit": canonical_state["state_at_commit"] == "NOT_RUN_PENDING_EXACT_FINAL_GATE" and canonical_state["attempts_at_commit"] == 0 and canonical_state["successes_at_commit"] == 0 and canonical_state["invocation_limit"] == 1 and not canonical_state["replay_after_success"],
        "outcomes_exact": truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "proposal_count": counts["declared_frozen_proposals"] == 6150,
        "effective_negatives": counts["effective_negatives"] == 35779,
        "effective_methods": counts["effective_methods"] == 22041,
        "failed_witnesses": counts["failed_witnesses"] == 7440,
        "bounded_passing_witnesses": counts["bounded_passing_witnesses"] == 9604,
        "open_gaps": counts["open_gaps"] == gates["effective_open_gaps"] == 287,
        "exact_gates": counts["exact_gates"] == gates["effective_exact_gates"] == 280,
        "negative_arithmetic": negatives["source_repository_sealed_negatives"] + negatives["liora_additive_failures"] == negatives["effective_negatives"] == 35779,
        "failed_witness_non_erasure": negatives["failed_witnesses_promoted"] == 0 and flow["failed_witness_non_erasure"],
        "closeout_failures_retained": len(flow["closeout_failures"]) == len(flow["closeout_methods"]) == len(flow["closeout_recoveries"]) == 5,
        "lifecycle_tests_not_replayed": lifecycle["x1"]["tests"] == 21 and lifecycle["x1"]["credited_runs"] == 1 and lifecycle["evidence"]["tests"] == 22 and lifecycle["evidence"]["credited_runs"] == 1,
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and not route["successor_contacted"] and route["send_count"] == 0,
        "route_exact_title": route["prospective_successor_exact_title"] == "Tamar Vey" and route["prospective_successor_phase"] == "v672-v7",
        "owner_file_ceiling": len(owner_doc_paths) < 2000,
        "document_word_ceiling": not documents["oversized_documents"],
        "full_suite_not_run": truth["full_repository_suite"] == lifecycle["full_repository_suite"] == canonical_state["full_repository_suite"] == "not_run_not_claimed",
        "same_owner_not_independent": truth["same_owner_only"] and not truth["independent_reproduction"] and not lifecycle["independent_reproduction"],
    }
    minimal_keys = [
        "branch_exact",
        "final_direct_child_of_evidence",
        "phase_commits_three",
        "zero_merges",
        "one_final_parent",
        "clean_before",
        "typed_zero_divergence_before",
        "four_way_equal_before",
        "final_delta_manifest",
        "final_owner_manifest",
        "owner_tests",
        "privacy_zero_confirmed",
        "terminal_verdict",
        "route_prepared_not_sent",
        "canonical_latch_pending_at_commit",
    ]

    status_after = git_text("status", "--porcelain=v1")
    divergence_after = git_text("rev-list", "--left-right", "--count", "@{u}...HEAD").split()
    upstream_after = git_text("rev-parse", "@{u}")
    tracking_after = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_after_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live_after = live_after_rows[0] if live_after_rows else ""
    detailed["clean_after"] = status_after == ""
    detailed["typed_zero_divergence_after"] = divergence_after == ["0", "0"]
    detailed["four_way_equal_after"] = head == upstream_after == tracking_after == live_after

    valid = all(detailed.values())
    return {
        "schema": "ghc.family.external-canonical-receipt.v3",
        "owner": final.OWNER,
        "phase": final.PHASE,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "valid": valid,
        "canonical_invocations": 1,
        "canonical_successes": 1 if valid else 0,
        "replayed": False,
        "exact_final": head,
        "parent": parent,
        "source_final": final.SOURCE_FINAL,
        "x1_commit": final.X1_COMMIT,
        "evidence_commit": final.EVIDENCE_COMMIT,
        "selected_tests": tests,
        "detailed_checks": {"passed": sum(detailed.values()), "total": len(detailed), "rows": detailed},
        "minimal_checks": {"passed": sum(detailed[key] for key in minimal_keys), "total": len(minimal_keys), "keys": minimal_keys},
        "documents": documents,
        "changed_python": code,
        "privacy": privacy,
        "manifests": manifests,
        "content_seal": {"targets": seal["target_count"], "mismatches": seal_mismatches},
        "lifecycle": {
            "phase_commits": phase_commits,
            "merge_commits": merges,
            "final_parent_count": len(parent_fields) - 1,
            "ahead_before": int(divergence[1]),
            "behind_before": int(divergence[0]),
            "ahead_after": int(divergence_after[1]),
            "behind_after": int(divergence_after[0]),
        },
        "effective_counts": counts,
        "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": final.BOUNDARY,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt = canonical(args.output)
    except Exception as exc:
        receipt = {
            "schema": "ghc.family.external-canonical-receipt.v3",
            "owner": final.OWNER,
            "phase": final.PHASE,
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "valid": False,
            "canonical_invocations": 1,
            "canonical_successes": 0,
            "replayed": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "full_repository_suite": "not_run_not_claimed",
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": final.BOUNDARY,
        }
    args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "valid": receipt["valid"], "output": args.output.name}, sort_keys=True))
    raise SystemExit(0 if receipt["valid"] else 1)


if __name__ == "__main__":
    main()
