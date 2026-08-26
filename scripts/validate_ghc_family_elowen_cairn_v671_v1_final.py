from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import build_ghc_family_elowen_cairn_v671_v1_final as final


ROOT = final.ROOT


def run(*args: str, text: bool = True, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(list(args), cwd=ROOT, capture_output=True, text=text, env=env, check=check)


def git(*args: str, text: bool = True) -> str | bytes:
    result = run("git", *args, text=text)
    return result.stdout.strip() if text else result.stdout


def head_bytes(head: str, path: str) -> bytes:
    return git("show", f"{head}:{path}", text=False)


def head_json(head: str, path: str) -> dict[str, Any]:
    return json.loads(head_bytes(head, path).decode("utf-8"))


def owner_paths(head: str) -> list[str]:
    paths = str(git("ls-tree", "-r", "--name-only", head)).splitlines()
    return sorted(path for path in paths if final.owner_path(path))


def replay_manifest(head: str, path: str) -> list[dict[str, Any]]:
    manifest = head_json(head, path)
    failures: list[dict[str, Any]] = []
    if manifest.get("entry_count") != len(manifest.get("entries", [])):
        failures.append({"path": path, "error": "entry_count_mismatch"})
    for row in manifest.get("entries", []):
        try:
            data = head_bytes(head, row["path"])
            oid = subprocess.run(["git", "hash-object", "--stdin"], cwd=ROOT, input=data, capture_output=True, check=True).stdout.decode().strip()
            actual = {"bytes": len(data), "git_blob_oid": oid, "sha256": hashlib.sha256(data).hexdigest()}
            expected = {key: row[key] for key in actual}
            if actual != expected:
                failures.append({"path": row["path"], "expected": expected, "actual": actual})
        except Exception as error:
            failures.append({"path": row.get("path"), "error": f"{type(error).__name__}: {error}"})
    return failures


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return final.privacy_patterns()


def security_findings(path: str, data: bytes) -> list[str]:
    findings: list[str] = []
    tree = ast.parse(data.decode("utf-8"), filename=path)
    banned = {"requests", "httpx", "socket", "ctypes", "winreg"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            findings.extend(f"{path}:{node.lineno}:banned_import:{alias.name}" for alias in node.names if alias.name.split(".")[0] in banned)
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in banned:
            findings.append(f"{path}:{node.lineno}:banned_import:{node.module}")
        elif isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append(f"{path}:{node.lineno}:shell_true")
    return findings


def validate(expected_head: str) -> dict[str, Any]:
    branch = str(git("branch", "--show-current"))
    local = str(git("rev-parse", "HEAD"))
    upstream = str(git("rev-parse", "@{upstream}"))
    tracking = str(git("rev-parse", f"refs/remotes/origin/{final.BRANCH}"))
    live_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{final.BRANCH}"))
    fresh_live = live_line.split()[0] if live_line else ""
    divergence = str(git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")).split()
    clean_before = not str(git("status", "--porcelain"))
    prerequisites = {
        "branch_exact": branch == final.BRANCH,
        "clean_before": clean_before,
        "expected_head_exact": local == expected_head,
        "typed_zero_divergence_before": divergence == ["0", "0"],
        "four_way_equality_before": local == upstream == tracking == fresh_live == expected_head,
    }

    test_result: subprocess.CompletedProcess[str] | None = None
    if all(prerequisites.values()):
        environment = dict(os.environ)
        environment["PYTHONUTF8"] = "1"
        environment["ELOWEN_V671_EXPECTED_FINAL"] = expected_head
        test_result = run(
            sys.executable,
            "-X",
            "utf8",
            "-m",
            "unittest",
            "-v",
            "tests.test_ghc_family_elowen_cairn_v671_v1_final",
            text=True,
            env=environment,
            check=False,
        )
    test_output = (test_result.stdout + test_result.stderr) if test_result else ""
    match = re.search(r"Ran\s+(\d+)\s+tests?", test_output)
    tests_ran = int(match.group(1)) if match else 0
    test_return_code = test_result.returncode if test_result else -1

    paths = owner_paths(expected_head)
    json_errors: list[dict[str, str]] = []
    python_errors: list[dict[str, str]] = []
    security: list[str] = []
    privacy_candidates: list[dict[str, str]] = []
    privacy_confirmed: list[dict[str, str]] = []
    document_words: dict[str, int] = {}
    json_count = 0
    python_count = 0
    markdown_count = 0
    html_count = 0
    scanner_paths = final.SCANNER_DEFINITION_PATHS
    patterns = privacy_patterns()
    for path in paths:
        data = head_bytes(expected_head, path)
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            json_count += 1
            try:
                json.loads(data.decode("utf-8"))
            except Exception as error:
                json_errors.append({"path": path, "error": f"{type(error).__name__}: {error}"})
        if suffix == ".py":
            python_count += 1
            try:
                ast.parse(data.decode("utf-8"), filename=path)
                security.extend(security_findings(path, data))
            except Exception as error:
                python_errors.append({"path": path, "error": f"{type(error).__name__}: {error}"})
        if suffix == ".md":
            markdown_count += 1
        if suffix == ".html":
            html_count += 1
        if suffix in {".json", ".md", ".html", ".txt", ".py", ".yaml", ".yml"}:
            for label, pattern in patterns.items():
                if pattern.search(data):
                    row = {"class": label, "path": path}
                    if path in scanner_paths:
                        privacy_candidates.append(row)
                    else:
                        privacy_confirmed.append(row)
        if suffix in {".md", ".html", ".txt"}:
            document_words[path] = len(re.findall(rb"\S+", data))

    owner_manifest_path = final.FINAL_OWNER_MANIFEST
    delta_manifest_path = final.FINAL_DELTA_MANIFEST
    owner_manifest_failures = replay_manifest(expected_head, owner_manifest_path)
    delta_manifest_failures = replay_manifest(expected_head, delta_manifest_path)
    owner_manifest = head_json(expected_head, owner_manifest_path)
    delta_manifest = head_json(expected_head, delta_manifest_path)
    truth = head_json(expected_head, "docs/elowen-cairn/v671-v1/closeout/phase-truth.json")
    flow = head_json(expected_head, "docs/elowen-cairn/v671-v1/closeout/method-flow-final.json")
    flow_receipt = head_json(expected_head, "docs/elowen-cairn/v671-v1/validation/final-method-flow-validation.json")
    gaps = head_json(expected_head, "docs/elowen-cairn/v671-v1/closeout/open-exact-gate-register.json")
    route = head_json(expected_head, "docs/elowen-cairn/v671-v1/closeout/route-state-final-candidate.json")
    staged_review = head_json(expected_head, final.FINAL_STAGED_REVIEW)
    staged_privacy = head_json(expected_head, final.FINAL_STAGED_PRIVACY)
    stale = head_json(expected_head, "docs/elowen-cairn/v671-v1/validation/stale-label-review.json")
    closeout = head_json(expected_head, final.CLOSEOUT_RECEIPT)
    seal = head_json(expected_head, final.CONTENT_SEAL)
    seal_failures: list[str] = []
    for row in seal["files"]:
        data = head_bytes(expected_head, row["path"])
        oid = subprocess.run(["git", "hash-object", "--stdin"], cwd=ROOT, input=data, capture_output=True, check=True).stdout.decode().strip()
        if (len(data), oid, hashlib.sha256(data).hexdigest()) != (row["bytes"], row["git_blob_oid"], row["sha256"]):
            seal_failures.append(row["path"])
    seal_without_hash = {key: value for key, value in seal.items() if key != "payload_sha256"}
    seal_payload_exact = seal["payload_sha256"] == final.sha256(final.canonical_bytes(seal_without_hash))

    commits = str(git("rev-list", "--reverse", f"{final.SOURCE_FINAL}..{expected_head}")).splitlines()
    parents = [str(git("show", "-s", "--format=%P", commit)).split() for commit in commits]
    diff_check = run("git", "diff", "--check", f"{final.SOURCE_FINAL}..{expected_head}", text=True, check=False)
    frozen_changes = str(git("diff", "--name-only", final.FROZEN_EVIDENCE, expected_head)).splitlines()
    frozen_x1_x2_changes = [path for path in frozen_changes if path.startswith("docs/elowen-cairn/v671-v1/x1/") or path.startswith("docs/elowen-cairn/v671-v1/x2/") or path in final.x2.BUILD_PATHS]

    clean_after = not str(git("status", "--porcelain"))
    local_after = str(git("rev-parse", "HEAD"))
    upstream_after = str(git("rev-parse", "@{upstream}"))
    tracking_after = str(git("rev-parse", f"refs/remotes/origin/{final.BRANCH}"))
    live_after_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{final.BRANCH}"))
    live_after = live_after_line.split()[0] if live_after_line else ""
    divergence_after = str(git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")).split()

    detailed = {
        **prerequisites,
        "bounded_python_security": not security,
        "closeout_outcomes_exact": truth["core_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "content_seal_files": not seal_failures,
        "content_seal_payload": seal_payload_exact,
        "delta_manifest_replay": not delta_manifest_failures,
        "diff_hygiene": diff_check.returncode == 0,
        "document_ceiling": bool(document_words) and max(document_words.values()) <= final.DOCUMENT_WORD_CEILING,
        "evidence_ancestral": run("git", "merge-base", "--is-ancestor", final.FROZEN_EVIDENCE, expected_head, check=False).returncode == 0,
        "exact_final_parent": str(git("rev-parse", f"{expected_head}^")) == final.FROZEN_EVIDENCE,
        "exact_gate_count": gaps["effective_exact_gates"] == 252,
        "file_ceiling": len(paths) <= final.FILE_CEILING,
        "five_class_privacy_scan": not privacy_confirmed,
        "four_outcome_labels": set(truth["core_outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"},
        "fresh_four_way_equality_after": local_after == upstream_after == tracking_after == live_after == expected_head,
        "frozen_x1_x2_unchanged": not frozen_x1_x2_changes,
        "head_stable": local_after == local == expected_head,
        "json_parses": not json_errors and json_count >= 140,
        "method_flow_exact": flow["counts"]["methods"] == 230 and flow["counts"]["witness_results"] == {"fail": 189, "pass": 230},
        "method_flow_skill_valid": flow_receipt["valid"] and flow_receipt["issue_count"] == 0,
        "no_merges": str(git("rev-list", "--count", "--merges", f"{final.SOURCE_FINAL}..{expected_head}")) == "0",
        "one_parent_each": len(parents) == 3 and all(len(parent) == 1 for parent in parents),
        "open_gap_count": gaps["effective_open_gaps"] == 257,
        "owner_manifest_replay": not owner_manifest_failures,
        "phase_commit_count": commits == [final.FROZEN_X1, final.FROZEN_EVIDENCE, expected_head],
        "python_ast": not python_errors and python_count >= 18,
        "route_prepared_not_sent": route["delivery_state"] == "PREPARED_NOT_SENT" and not route["sent_by_elowen_cairn"],
        "seal_bound_in_closeout": closeout["content_seal_payload_sha256"] == seal["payload_sha256"],
        "source_ancestral": run("git", "merge-base", "--is-ancestor", final.SOURCE_FINAL, expected_head, check=False).returncode == 0,
        "staged_privacy_valid": staged_privacy["valid"] and staged_privacy["confirmed_hit_count"] == 0,
        "staged_review_valid": staged_review["valid"],
        "stale_label_review": stale["status"] == "PASS" and not stale["unexpected_stale_labels"],
        "static_report_present": "docs/elowen-cairn/v671-v1/closeout/static-report.html" in paths and html_count >= 1,
        "terminal_verdict": truth["terminal_verdict"] == final.TERMINAL_VERDICT,
        "tests_exact": tests_ran == 24 and test_return_code == 0,
        "truth_arithmetic": all(truth[key] == value for key, value in final.FINAL_OVERLAY.items()),
        "typed_zero_divergence_after": divergence_after == ["0", "0"],
        "working_tree_clean_after": clean_after,
        "x1_ancestral": run("git", "merge-base", "--is-ancestor", final.FROZEN_X1, expected_head, check=False).returncode == 0,
    }
    minimal = {
        "branch": detailed["branch_exact"],
        "clean": detailed["clean_before"] and detailed["working_tree_clean_after"],
        "commits": detailed["phase_commit_count"],
        "head": detailed["expected_head_exact"] and detailed["head_stable"],
        "manifests": detailed["owner_manifest_replay"] and detailed["delta_manifest_replay"],
        "merges": detailed["no_merges"],
        "parents": detailed["one_parent_each"] and detailed["exact_final_parent"],
        "privacy": detailed["five_class_privacy_scan"],
        "remote": detailed["four_way_equality_before"] and detailed["fresh_four_way_equality_after"],
        "route": detailed["route_prepared_not_sent"],
        "seal": detailed["content_seal_files"] and detailed["content_seal_payload"],
        "security": detailed["bounded_python_security"],
        "tests": detailed["tests_exact"],
        "truth": detailed["truth_arithmetic"] and detailed["terminal_verdict"],
        "zero_divergence": detailed["typed_zero_divergence_before"] and detailed["typed_zero_divergence_after"],
    }
    all_passed = all(detailed.values()) and all(minimal.values())
    receipt: dict[str, Any] = {
        "schema": "ghc.family.exact-final-owner-canonical.v1",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all_passed else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": final.OWNER,
        "phase": final.PHASE,
        "exact_final": expected_head,
        "all_passed": all_passed,
        "canonical_invocation_count": 1,
        "successful_invocation_count": 1 if all_passed else 0,
        "post_success_replay": False,
        "complete_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "tests": {"ran": tests_ran, "return_code": test_return_code, "output_sha256": hashlib.sha256(test_output.encode("utf-8")).hexdigest()},
        "detailed_checks": detailed,
        "detailed_checks_passed": sum(bool(value) for value in detailed.values()),
        "detailed_checks_total": len(detailed),
        "minimal_checks": minimal,
        "minimal_checks_passed": sum(bool(value) for value in minimal.values()),
        "minimal_checks_total": len(minimal),
        "strict_json_count": json_count,
        "markdown_count": markdown_count,
        "html_count": html_count,
        "python_ast_count": python_count,
        "owner_files_scanned": len(paths),
        "privacy_candidate_count": len(privacy_candidates),
        "privacy_confirmed_hits": privacy_confirmed,
        "python_security_findings": security,
        "manifest_entries_replayed": owner_manifest["entry_count"] + delta_manifest["entry_count"],
        "boundary": final.BOUNDARY,
        "terminal_verdict": final.TERMINAL_VERDICT,
    }
    receipt["payload_sha256"] = final.sha256(final.canonical_bytes(receipt))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--external-receipt", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        parser.error("expected head must be a full lowercase SHA-1")
    receipt_path = Path(args.external_receipt).resolve()
    if receipt_path.is_relative_to(ROOT.resolve()):
        parser.error("external receipt must remain outside the repository worktree")
    receipt = validate(args.expected_head)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    summary = {
        "status": receipt["status"],
        "all_passed": receipt["all_passed"],
        "exact_final": receipt["exact_final"],
        "tests": receipt["tests"],
        "detailed": f"{receipt['detailed_checks_passed']}/{receipt['detailed_checks_total']}",
        "minimal": f"{receipt['minimal_checks_passed']}/{receipt['minimal_checks_total']}",
        "strict_json_count": receipt["strict_json_count"],
        "owner_files_scanned": receipt["owner_files_scanned"],
        "manifest_entries_replayed": receipt["manifest_entries_replayed"],
        "privacy_candidate_count": receipt["privacy_candidate_count"],
        "privacy_confirmed_hits": len(receipt["privacy_confirmed_hits"]),
        "payload_sha256": receipt["payload_sha256"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if receipt["all_passed"] else 1)


if __name__ == "__main__":
    main()
