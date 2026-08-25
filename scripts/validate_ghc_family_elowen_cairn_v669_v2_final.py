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

from ghc_family_elowen_cairn_v669_v2_archive import (
    BRANCH,
    DOCUMENT_WORD_CEILING,
    FILE_CEILING,
    FINAL_OVERLAY,
    FROZEN_EVIDENCE,
    FROZEN_X1,
    OWNER,
    PHASE,
    REL_PHASE_ROOT,
    ROOT,
    SOURCE_FINAL,
    SOURCE_START,
    TERMINAL_VERDICT,
    canonical_json_bytes,
    sha256_bytes,
    utc_now,
)


OWNER_MANIFEST = (REL_PHASE_ROOT / "validation/final-owner-manifest.json").as_posix()
DELTA_MANIFEST = (REL_PHASE_ROOT / "validation/final-delta-manifest.json").as_posix()
CONTENT_SEAL = (REL_PHASE_ROOT / "seal/content-seal.json").as_posix()


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
    selected = []
    for path in paths:
        if path.startswith("docs/elowen-cairn/v669-v2/"):
            selected.append(path)
        elif path.startswith("scripts/ghc_family_lutherie_"):
            selected.append(path)
        elif "elowen_cairn_v669_v2" in path and (path.startswith("scripts/") or path.startswith("tests/")):
            selected.append(path)
    return sorted(selected)


def replay_manifest(head: str, manifest_path: str) -> list[dict[str, Any]]:
    manifest = head_json(head, manifest_path)
    failures: list[dict[str, Any]] = []
    if manifest.get("entry_count") != len(manifest.get("entries", [])):
        failures.append({"path": manifest_path, "error": "entry_count_mismatch"})
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
    return {
        "raw_identifier": re.compile(rb"\b019[0-9a-f]{5}-[0-9a-f-]{20,}\b", re.I),
        "credential_assignment": re.compile(rb"(?i)(?:password|secret|api[_-]?key|bearer|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
        "private_route": re.compile(rb"(?i)(?:task|thread|session|resume)[_-]?id\s*[:=]\s*['\"][^'\"]+"),
        "private_absolute_path": re.compile(rb"[A-Za-z]:\\(?:Users|GHC-Archives)\\"),
        "private_app_state": re.compile(rb"(?i)(?:private_callable|session_stream|application_state)\s*[:=]\s*['\"][^'\"]+"),
    }


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
    tracking = str(git("rev-parse", f"refs/remotes/origin/{BRANCH}"))
    live_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"))
    fresh_live = live_line.split()[0] if live_line else ""
    divergence = str(git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")).split()
    clean_before = not str(git("status", "--porcelain"))

    prerequisites = {
        "branch_exact": branch == BRANCH,
        "clean_before": clean_before,
        "expected_head_exact": local == expected_head,
        "four_way_equality_before": local == upstream == tracking == fresh_live == expected_head,
        "typed_zero_divergence_before": divergence == ["0", "0"],
    }
    test_result: subprocess.CompletedProcess[str] | None = None
    if all(prerequisites.values()):
        test_env = dict(os.environ)
        test_env["ELOWEN_EXPECTED_FINAL"] = expected_head
        test_result = run(
            sys.executable,
            "-X",
            "utf8",
            "-m",
            "unittest",
            "-v",
            "tests.test_ghc_family_elowen_cairn_v669_v2_final",
            text=True,
            env=test_env,
            check=False,
        )
    test_output = (test_result.stdout + test_result.stderr) if test_result else ""
    tests_ran_match = re.search(r"Ran\s+(\d+)\s+tests?", test_output)
    tests_ran = int(tests_ran_match.group(1)) if tests_ran_match else 0
    test_return_code = test_result.returncode if test_result else -1

    paths = owner_paths(expected_head)
    json_errors: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    python_errors: list[dict[str, str]] = []
    security: list[str] = []
    document_words: dict[str, int] = {}
    json_count = 0
    python_count = 0
    markdown_count = 0
    html_count = 0
    patterns = privacy_patterns()
    text_suffixes = {".json", ".md", ".html", ".txt", ".py", ".yaml", ".yml"}
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
        if suffix in text_suffixes:
            for class_name, pattern in patterns.items():
                if pattern.search(data):
                    privacy_hits.append({"class": class_name, "path": path})
        if suffix in {".md", ".html", ".txt"}:
            document_words[path] = len(re.findall(rb"\S+", data))

    owner_manifest_failures = replay_manifest(expected_head, OWNER_MANIFEST)
    delta_manifest_failures = replay_manifest(expected_head, DELTA_MANIFEST)
    truth = head_json(expected_head, (REL_PHASE_ROOT / "closeout/phase-truth.json").as_posix())
    method_flow = head_json(expected_head, (REL_PHASE_ROOT / "closeout/method-flow-ledger.json").as_posix())
    gaps = head_json(expected_head, (REL_PHASE_ROOT / "closeout/open-exact-gate-register.json").as_posix())
    route = head_json(expected_head, (REL_PHASE_ROOT / "closeout/route-state-final-candidate.json").as_posix())
    seal = head_json(expected_head, CONTENT_SEAL)
    seal_failures = []
    for row in seal["files"]:
        data = head_bytes(expected_head, row["path"])
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            seal_failures.append(row["path"])
    seal_payload = {key: value for key, value in seal.items() if key != "payload_sha256"}
    seal_payload_exact = seal["payload_sha256"] == sha256_bytes(canonical_json_bytes(seal_payload))

    commits = str(git("rev-list", "--reverse", f"{SOURCE_FINAL}..{expected_head}")).splitlines()
    parents = [str(git("show", "-s", "--format=%P", commit)).split() for commit in commits]
    diff_check = run("git", "diff", "--check", f"{SOURCE_FINAL}..{expected_head}", text=True, check=False)
    clean_after = not str(git("status", "--porcelain"))
    local_after = str(git("rev-parse", "HEAD"))
    upstream_after = str(git("rev-parse", "@{upstream}"))
    tracking_after = str(git("rev-parse", f"refs/remotes/origin/{BRANCH}"))
    live_after_line = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"))
    live_after = live_after_line.split()[0] if live_after_line else ""

    detailed = {
        **prerequisites,
        "bounded_python_security": not security,
        "closeout_outcomes_exact": truth["core_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "content_seal_files": not seal_failures,
        "content_seal_payload": seal_payload_exact,
        "delta_manifest_replay": not delta_manifest_failures,
        "diff_hygiene": diff_check.returncode == 0,
        "document_ceiling": bool(document_words) and max(document_words.values()) <= DOCUMENT_WORD_CEILING,
        "exact_final_parent": str(git("rev-parse", f"{expected_head}^")) == FROZEN_EVIDENCE,
        "exact_gate_count": gaps["effective_exact_gates"] == 222,
        "file_ceiling": len(paths) <= FILE_CEILING,
        "five_class_privacy_scan": not privacy_hits,
        "four_outcome_labels": set(truth["core_outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"},
        "fresh_four_way_equality_after": local_after == upstream_after == tracking_after == live_after == expected_head,
        "head_stable": local_after == local == expected_head,
        "json_parses": not json_errors and json_count >= 120,
        "method_count": truth["methods"] == 16826 and len(method_flow["methods"]) == 196,
        "no_merges": str(git("rev-list", "--count", "--merges", f"{SOURCE_FINAL}..{expected_head}")) == "0",
        "one_parent_each": len(parents) == 3 and all(len(parent) == 1 for parent in parents),
        "open_gap_count": gaps["effective_open_gaps"] == 227,
        "owner_manifest_replay": not owner_manifest_failures,
        "phase_commit_count": commits == [FROZEN_X1, FROZEN_EVIDENCE, expected_head],
        "python_ast": not python_errors and python_count >= 18,
        "route_prepared_not_sent": route["delivery_state"] == "PREPARED_NOT_SENT" and not route["sent_by_elowen_cairn"],
        "static_report_present": (REL_PHASE_ROOT / "closeout/static-report.html").as_posix() in paths and html_count >= 1,
        "terminal_verdict": truth["terminal_verdict"] == TERMINAL_VERDICT,
        "tests_exact": tests_ran == 20 and test_return_code == 0,
        "truth_arithmetic": all(truth[key] == value for key, value in FINAL_OVERLAY.items()),
        "working_tree_clean_after": clean_after,
        "x1_ancestral": run("git", "merge-base", "--is-ancestor", FROZEN_X1, expected_head, text=True, check=False).returncode == 0,
        "evidence_ancestral": run("git", "merge-base", "--is-ancestor", FROZEN_EVIDENCE, expected_head, text=True, check=False).returncode == 0,
        "source_ancestral": run("git", "merge-base", "--is-ancestor", SOURCE_START, expected_head, text=True, check=False).returncode == 0,
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
        "zero_divergence": detailed["typed_zero_divergence_before"],
    }
    all_passed = all(detailed.values()) and all(minimal.values())
    receipt = {
        "all_passed": all_passed,
        "boundary": "One exact-final same-owner canonical aggregate under shared infrastructure; not a full repository suite, independent reproduction, external audit, production certification, professional validation, legal or cultural authority, Māori authority, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.",
        "canonical_invocation_count": 1,
        "complete_repository_suite": False,
        "detailed_checks": detailed,
        "detailed_checks_passed": sum(bool(value) for value in detailed.values()),
        "detailed_checks_total": len(detailed),
        "exact_final": expected_head,
        "generated_at_utc": utc_now(),
        "manifest_entries_replayed": head_json(expected_head, OWNER_MANIFEST)["entry_count"] + head_json(expected_head, DELTA_MANIFEST)["entry_count"],
        "minimal_checks": minimal,
        "minimal_checks_passed": sum(bool(value) for value in minimal.values()),
        "minimal_checks_total": len(minimal),
        "owner": OWNER,
        "owner_files_scanned": len(paths),
        "phase": PHASE,
        "post_success_replay": False,
        "privacy_confirmed_hits": len(privacy_hits),
        "python_ast_count": python_count,
        "python_security_findings": security,
        "schema": "ghc.family.exact-final-canonical.v3",
        "strict_json_count": json_count,
        "successful_invocation_count": 1 if all_passed else 0,
        "tests": {"return_code": test_return_code, "ran": tests_ran},
        "terminal_verdict": TERMINAL_VERDICT,
    }
    receipt["payload_sha256"] = sha256_bytes(canonical_json_bytes(receipt))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--external-receipt", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        parser.error("expected head must be a full lowercase SHA-1")
    receipt = validate(args.expected_head)
    path = Path(args.external_receipt)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "all_passed": receipt["all_passed"],
        "detailed": f"{receipt['detailed_checks_passed']}/{receipt['detailed_checks_total']}",
        "exact_final": receipt["exact_final"],
        "minimal": f"{receipt['minimal_checks_passed']}/{receipt['minimal_checks_total']}",
        "owner_files_scanned": receipt["owner_files_scanned"],
        "payload_sha256": receipt["payload_sha256"],
        "strict_json_count": receipt["strict_json_count"],
        "tests": receipt["tests"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if receipt["all_passed"] else 1)


if __name__ == "__main__":
    main()
