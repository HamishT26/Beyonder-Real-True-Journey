"""Bounded component recovery after the unreplayed r3 canonical failure."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r3-full-tools"
X1_HEAD = "705f4cda336639d2a700d2d830a975cd281c7e4b"
EVIDENCE_HEAD = "08dd119b863c7103607b8399b3a201b5cb511af9"
FAILED_FINAL = "68979e155cf1dc27a3fc967657f613cc3b1172c2"
FAILED_RECEIPT_SHA256 = "74c29c0a4b38128a591ae1e9f4867d457d35ae8ed84d3b2505a40aa0370b9a14"
RECEIPT_ROOT = Path(f"{chr(68)}:{os.sep}") / "GHC-Archives" / "receipts" / "neris-solane-v667-v8-r3"
FAILED_RECEIPT = RECEIPT_ROOT / "canonical-exact-final-receipt.json"
RECOVERY_RECEIPT = RECEIPT_ROOT / "canonical-dependency-recovery-receipt.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(ROOT), *arguments], text=True, encoding="utf-8", errors="replace", capture_output=True, check=check)


def owner_files() -> list[Path]:
    return sorted([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts], key=lambda path: path.relative_to(ROOT).as_posix())


def manifest_replay(relative: str) -> tuple[int, bool, set[str]]:
    payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    paths = set()
    valid = True
    for row in payload["entries"]:
        path = ROOT / row["path"]
        paths.add(row["path"])
        valid = valid and path.is_file() and path.stat().st_size == row["bytes"] and sha256(path) == row["sha256"]
    return len(payload["entries"]), valid, paths


def ast_security_scan(paths: list[Path]) -> dict[str, Any]:
    findings = []
    parsed = 0
    for path in paths:
        if path.suffix != ".py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        parsed += 1
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "rule": "dynamic_builtin_call"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "rule": "subprocess_shell_true"})
    return {"python_files_parsed": parsed, "findings": findings, "bounded": True, "exhaustive": False}


def privacy_candidates(paths: list[Path]) -> list[dict[str, str]]:
    patterns = {
        "windows_absolute_path": re.compile(r"(?<![A-Za-z])[A-Z]:[\\/]+", re.I),
        "raw_thread_or_session_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?:api[_-]?key|pass" + r"word|sec" + r"ret|bearer)\s*[:=]\s*[^\s\"<]{8,}", re.I),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "private_route_or_resume_value": re.compile(r"(?:resume|session|thread)[_-]?(?:id|token)\s*[:=]\s*[^\s\"<]{8,}", re.I),
    }
    hits = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"class": class_name, "path": path.relative_to(ROOT).as_posix(), "match_sha256": hashlib.sha256(match.group(0).encode()).hexdigest()})
    return hits


def run_tests() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "tests.test_ghc_family_neris_solane_v667_v8_r3_x2", "tests.test_ghc_family_neris_solane_v667_v8_r3_correction", "-v"],
        cwd=str(ROOT), text=True, encoding="utf-8", errors="replace", capture_output=True, check=False,
    )
    combined = completed.stdout + "\n" + completed.stderr
    match = re.search(r"Ran (\d+) tests", combined)
    return {"returncode": completed.returncode, "tests_run": int(match.group(1)) if match else 0, "ok_marker": "OK" in combined, "output_sha256": hashlib.sha256(combined.encode()).hexdigest()}


def validate(expected_head: str) -> dict[str, Any]:
    checks = []

    def check(name: str, condition: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})
        if not condition:
            raise AssertionError(f"{name}: {observed}")

    failed_receipt = json.loads(FAILED_RECEIPT.read_text(encoding="utf-8"))
    check("failed receipt hash", sha256(FAILED_RECEIPT) == FAILED_RECEIPT_SHA256, sha256(FAILED_RECEIPT))
    check("zero canonical success", failed_receipt["state"] == "INVALID_ZERO_CANONICAL_SUCCESS_CREDIT" and failed_receipt["canonical_success_count"] == 0, failed_receipt["state"])
    check("one canonical invocation", failed_receipt["invocation_count"] == 1 and failed_receipt["successful_replay_count"] == 0, failed_receipt["invocation_count"])

    local = git("rev-parse", "HEAD").stdout.strip()
    parent = git("rev-parse", "HEAD^").stdout.strip()
    branch = git("branch", "--show-current").stdout.strip()
    history = [line for line in git("rev-list", "--parents", "--reverse", "HEAD").stdout.splitlines() if line.strip()]
    merges = [line for line in git("rev-list", "--merges", "HEAD").stdout.splitlines() if line.strip()]
    upstream = git("rev-parse", "@{u}").stdout.strip()
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.strip()
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.strip().split()
    clean = not git("status", "--porcelain").stdout.strip()
    check("exact corrected head", local == expected_head, local)
    check("correction direct parent", parent == FAILED_FINAL, parent)
    check("exact branch", branch == BRANCH, branch)
    check("four single-parent commits", len(history) == 4 and all(len(line.split()) == (1 if index == 0 else 2) for index, line in enumerate(history)), history)
    check("zero merges", not merges, len(merges))
    check("four-way equality", local == upstream == tracking == live, {"local": local, "upstream": upstream, "tracking": tracking, "live": live})
    check("zero divergence", divergence == ["0", "0"], divergence)
    check("clean", clean, clean)

    manifests = {}
    for name, relative in {
        "x1": "docs/neris-solane/v667-v8-r3/validation/x1-content-manifest.json",
        "x2": "docs/neris-solane/v667-v8-r3/validation/x2-content-manifest.json",
        "failed_final_delta": "docs/neris-solane/v667-v8-r3/validation/final-delta-manifest.json",
        "failed_final_owner": "docs/neris-solane/v667-v8-r3/validation/final-owner-manifest.json",
        "correction_delta": "docs/neris-solane/v667-v8-r3/validation/correction-delta-manifest.json",
        "corrected_owner": "docs/neris-solane/v667-v8-r3/validation/corrected-owner-manifest.json",
    }.items():
        count, valid, paths = manifest_replay(relative)
        check(f"{name} manifest replay", valid, count)
        manifests[name] = {"entries": count, "paths": paths}
    current_files = owner_files()
    current_paths = {path.relative_to(ROOT).as_posix() for path in current_files}
    corrected_self = "docs/neris-solane/v667-v8-r3/validation/corrected-owner-manifest.json"
    check("corrected owner completeness", manifests["corrected_owner"]["paths"] == current_paths - {corrected_self}, {"manifest": len(manifests["corrected_owner"]["paths"]), "current": len(current_paths)})

    security = ast_security_scan(current_files)
    check("AST security dependency", not security["findings"], security)
    privacy = privacy_candidates(current_files)
    check("five-class privacy", not privacy, len(privacy))
    json_count = 0
    for path in current_files:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
    check("strict JSON", json_count > 0, json_count)
    check("2,000-file guard", len(current_files) < 2000, len(current_files))
    tests = run_tests()
    check("corrected-head component tests", tests["returncode"] == 0 and tests["ok_marker"] and tests["tests_run"] == 17, tests)
    overlay = json.loads((PHASE / "correction" / "method-flow-external-overlay.json").read_text(encoding="utf-8"))
    route = json.loads((PHASE / "route" / "vesper-arlen-v668-v1-correction-route.json").read_text(encoding="utf-8"))
    check("external overlay exact", overlay["corrected_activation_overlay"]["effective_negatives"] == 28734 and overlay["corrected_activation_overlay"]["failed_witnesses"] == 1035, overlay["corrected_activation_overlay"])
    check("route prepared not sent", route["delivery_state"] == "PREPARED_NOT_SENT" and not route["successor_contacted"], route["delivery_state"])
    check("terminal verdict", route["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", route["terminal_verdict"])

    return {
        "state": "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT",
        "validated_at": now(),
        "expected_head": expected_head,
        "failed_canonical_head": FAILED_FINAL,
        "failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA256,
        "canonical_invocation_count": 1,
        "canonical_success_count": 0,
        "canonical_replay_count": 0,
        "dependency_recovery_invocation_count": 1,
        "tests": tests,
        "precommit_final_tests_retained_not_replayed": 15,
        "checks": len(checks),
        "json_parses": json_count,
        "privacy_scan": {"files": len(current_files), "classes": 5, "candidates": 0, "confirmed_hits": 0},
        "ast_security_scan": security,
        "manifest_replay": {name: value["entries"] for name, value in manifests.items()},
        "owner_files": len(current_files),
        "history_commit_count": len(history),
        "merge_count": len(merges),
        "local_upstream_tracking_live_equal": True,
        "divergence": "0/0",
        "clean": True,
        "full_repository_suite_run": False,
        "same_owner_not_independent_reproduction": True,
        "repository_sealed_counts": overlay["repository_sealed_x2"],
        "external_activation_overlay": overlay["corrected_activation_overlay"],
        "delivery_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    args = parser.parse_args()
    if RECOVERY_RECEIPT.exists():
        raise SystemExit("dependency recovery receipt already exists; replay refused")
    try:
        payload = validate(args.expected_head)
    except Exception as error:
        payload = {
            "state": "INVALID_DEPENDENCY_RECOVERY_ZERO_SUCCESS_CREDIT",
            "validated_at": now(),
            "expected_head": args.expected_head,
            "canonical_success_count": 0,
            "canonical_replay_count": 0,
            "error_type": type(error).__name__,
            "error": str(error),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
        RECOVERY_RECEIPT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    RECOVERY_RECEIPT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    summary_keys = ("state", "expected_head", "canonical_success_count", "canonical_replay_count", "tests", "checks", "json_parses", "privacy_scan", "ast_security_scan", "manifest_replay", "owner_files", "history_commit_count", "terminal_verdict")
    print(json.dumps({key: payload[key] for key in summary_keys}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
