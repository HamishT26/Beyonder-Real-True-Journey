"""One-shot exact-final owner-scoped canonical validator for Neris r3."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r3-full-tools"
X1_HEAD = "705f4cda336639d2a700d2d830a975cd281c7e4b"
EVIDENCE_HEAD = "08dd119b863c7103607b8399b3a201b5cb511af9"
RECEIPT_ROOT = Path(f"{chr(68)}:{os.sep}") / "GHC-Archives" / "receipts" / "neris-solane-v667-v8-r3"
RECEIPT_PATH = RECEIPT_ROOT / "canonical-exact-final-receipt.json"
OWNER_MANIFEST = PHASE / "validation" / "final-owner-manifest.json"
DELTA_MANIFEST = PHASE / "validation" / "final-delta-manifest.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=check,
    )


def sanitize(value: str) -> str:
    value = re.sub(re.escape(str(ROOT)), "<R3_WORKTREE>", value, flags=re.I)
    value = re.sub(re.escape(str(Path.home())), "<USER_HOME>", value, flags=re.I)
    value = re.sub(r"(?<![A-Za-z])[A-Z]:[\\/]+[^\r\n'\"]*", "<ABSOLUTE_WINDOWS_PATH>", value, flags=re.I)
    return value


def owner_files() -> list[Path]:
    return sorted(
        [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts],
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def privacy_candidates(paths: list[Path]) -> list[dict[str, str]]:
    patterns = {
        "windows_absolute_path": re.compile(r"(?<![A-Za-z])[A-Z]:[\\/]+", re.I),
        "raw_thread_or_session_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?:api[_-]?key|pass" + r"word|sec" + r"ret|bearer)\s*[:=]\s*[^\s\"<]{8,}", re.I),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "private_route_or_resume_value": re.compile(r"(?:resume|session|thread)[_-]?(?:id|token)\s*[:=]\s*[^\s\"<]{8,}", re.I),
    }
    hits: list[dict[str, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"class": class_name, "path": path.relative_to(ROOT).as_posix(), "match_sha256": hashlib.sha256(match.group(0).encode()).hexdigest()})
    return hits


def manifest_replay(path: Path) -> tuple[int, bool, set[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    paths: set[str] = set()
    valid = True
    for row in payload["entries"]:
        target = ROOT / row["path"]
        paths.add(row["path"])
        valid = valid and target.is_file() and target.stat().st_size == row["bytes"] and sha256(target) == row["sha256"]
    return len(payload["entries"]), valid, paths


def run_tests() -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "tests.test_ghc_family_neris_solane_v667_v8_r3_x2",
            "tests.test_ghc_family_neris_solane_v667_v8_r3_final",
            "-v",
        ],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    combined = completed.stdout + "\n" + completed.stderr
    match = re.search(r"Ran (\d+) tests", combined)
    return {
        "returncode": completed.returncode,
        "tests_run": int(match.group(1)) if match else 0,
        "ok_marker": "OK" in combined,
        "output_sha256": hashlib.sha256(sanitize(combined).encode("utf-8")).hexdigest(),
    }


def validate(expected_head: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, observed: Any) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})
        if not condition:
            raise AssertionError(f"{name}: {observed}")

    local = git("rev-parse", "HEAD").stdout.strip()
    branch = git("branch", "--show-current").stdout.strip()
    parent = git("rev-parse", "HEAD^").stdout.strip()
    x1_line = git("rev-list", "--parents", "-n", "1", X1_HEAD).stdout.strip().split()
    evidence_parent = git("rev-parse", f"{EVIDENCE_HEAD}^").stdout.strip()
    history_lines = [line for line in git("rev-list", "--parents", "--reverse", "HEAD").stdout.splitlines() if line.strip()]
    merges = [line for line in git("rev-list", "--merges", "HEAD").stdout.splitlines() if line.strip()]
    upstream = git("rev-parse", "@{u}").stdout.strip()
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.strip()
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.strip().split()
    clean = not git("status", "--porcelain").stdout.strip()

    check("exact local head", local == expected_head, local)
    check("exact branch", branch == BRANCH, branch)
    check("final direct parent evidence", parent == EVIDENCE_HEAD, parent)
    check("evidence direct parent x1", evidence_parent == X1_HEAD, evidence_parent)
    check("x1 zero parent", x1_line == [X1_HEAD], x1_line)
    check("three commit blank-root history", len(history_lines) == 3, len(history_lines))
    check("zero merges", not merges, len(merges))
    check("upstream equality", upstream == local, upstream)
    check("tracking equality", tracking == local, tracking)
    check("fresh live equality", live == local, live)
    check("zero divergence", divergence == ["0", "0"], divergence)
    check("clean worktree", clean, clean)

    x1_count, x1_valid, _ = manifest_replay(PHASE / "validation" / "x1-content-manifest.json")
    x2_count, x2_valid, _ = manifest_replay(PHASE / "validation" / "x2-content-manifest.json")
    delta_count, delta_valid, _ = manifest_replay(DELTA_MANIFEST)
    owner_count, owner_valid, owner_paths = manifest_replay(OWNER_MANIFEST)
    current_files = owner_files()
    current_relative = {path.relative_to(ROOT).as_posix() for path in current_files}
    owner_self = OWNER_MANIFEST.relative_to(ROOT).as_posix()
    check("x1 manifest replay", x1_valid, x1_count)
    check("x2 manifest replay", x2_valid, x2_count)
    check("final delta manifest replay", delta_valid, delta_count)
    check("final owner manifest replay", owner_valid, owner_count)
    check("final owner manifest completeness", owner_paths == current_relative - {owner_self}, {"manifest": len(owner_paths), "current_minus_self": len(current_relative - {owner_self})})

    baton = PHASE / "handoffs" / "vesper-arlen-v668-v1-activation-prepared.md"
    baton_words = len(baton.read_text(encoding="utf-8").split())
    route = json.loads((PHASE / "route" / "vesper-arlen-v668-v1-prepared-route.json").read_text(encoding="utf-8"))
    outcomes = json.loads((PHASE / "x2" / "proposals" / "proposal-outcomes.json").read_text(encoding="utf-8"))
    mutations = json.loads((PHASE / "x2" / "proposals" / "negative-mutation-results.json").read_text(encoding="utf-8"))
    tools = json.loads((PHASE / "x2" / "tooling" / "thirteen-tool-transaction-receipt.json").read_text(encoding="utf-8"))
    method = json.loads((PHASE / "x2" / "method-flow" / "method-flow-ledger.json").read_text(encoding="utf-8"))
    cards = json.loads((PHASE / "x2" / "flashcards" / "four-tier-deck.json").read_text(encoding="utf-8"))
    promotion = json.loads((PHASE / "x2" / "skills" / "global-promotion-receipt.json").read_text(encoding="utf-8"))
    overlays = json.loads((PHASE / "x2" / "skills" / "core-skill-overlay-receipt.json").read_text(encoding="utf-8"))
    checklist = json.loads((PHASE / "closeout" / "terminal-checklist.json").read_text(encoding="utf-8"))
    check("baton minimum", baton_words >= 10_000, baton_words)
    check("prepared route", route["delivery_state"] == "PREPARED_NOT_SENT", route["delivery_state"])
    check("no successor precontact", not route["successor_contacted"], route["successor_contacted"])
    check("exact recipient", route["recipient_exact_title"] == "Vesper Arlen" and route["recipient_phase"] == "v668-v1", route["recipient_exact_title"])
    check("four outcomes", Counter(row["outcome_label"] for row in outcomes["outcomes"]) == Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}), outcomes["counts"])
    check("one hundred rejecting mutations", mutations["count"] == 100 and mutations["all_rejected"], mutations["count"])
    check("thirteen positive tool smokes", tools["positive_smoke_count"] == 13, tools["positive_smoke_count"])
    check("thirteen negative tool rejections", tools["negative_rejection_count"] == 13, tools["negative_rejection_count"])
    check("eleven retained tool failures", len(tools["operational_failures"]) == 11, len(tools["operational_failures"]))
    check("Method Flow exact", [method[key] for key in ("effective_negatives", "methods", "open_gaps", "exact_gates", "failed_witnesses", "passing_witnesses")] == [28733, 15319, 203, 201, 1034, 1875], method)
    check("320 flashcards", cards["count"] == 320, cards["count"])
    check("ten global skills", promotion["count"] == 10, promotion["count"])
    check("seven core overlays", overlays["count"] == 7, overlays["count"])
    check("thirty terminal checks", checklist["count"] == 30 and checklist["all_passed"], checklist["count"])
    check("terminal verdict", method["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", method["terminal_verdict"])

    json_count = 0
    for path in current_files:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
    privacy = privacy_candidates(current_files)
    security_findings = []
    python_files = [path for path in current_files if path.suffix == ".py"]
    for path in python_files:
        text = path.read_text(encoding="utf-8")
        for literal in ("shell=True", "eval" + "(", "exec" + "("):
            if literal in text:
                security_findings.append({"path": path.relative_to(ROOT).as_posix(), "rule": literal})
    check("strict JSON parses", json_count > 0, json_count)
    check("five-class privacy scan", not privacy, len(privacy))
    check("bounded Python security scan", not security_findings, len(security_findings))
    check("2,000-file guard", len(current_files) < 2000, len(current_files))

    tests = run_tests()
    check("owner-scoped tests", tests["returncode"] == 0 and tests["ok_marker"] and tests["tests_run"] == 27, tests)
    minimal_names = {
        "exact local head", "final direct parent evidence", "x1 zero parent", "zero merges",
        "fresh live equality", "zero divergence", "clean worktree", "final owner manifest replay",
        "baton minimum", "no successor precontact", "four outcomes", "five-class privacy scan",
        "owner-scoped tests", "terminal verdict", "2,000-file guard",
    }
    minimal = [row for row in checks if row["name"] in minimal_names]
    check("fifteen minimal checks", len(minimal) == 15 and all(row["passed"] for row in minimal), len(minimal))

    return {
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invoked_at": now(),
        "invocation_count": 1,
        "canonical_success_count": 1,
        "successful_replay_count": 0,
        "expected_head": expected_head,
        "branch": BRANCH,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "history_commit_count": len(history_lines),
        "merge_count": len(merges),
        "tests": tests,
        "detailed_checks": len(checks),
        "minimal_checks": len(minimal),
        "json_parses": json_count,
        "privacy_scan": {"files": len(current_files), "classes": 5, "candidates": len(privacy), "confirmed_hits": 0},
        "python_security_scan": {"files": len(python_files), "bounded_findings": len(security_findings), "exhaustive": False},
        "manifest_replay": {"x1": x1_count, "x2": x2_count, "final_delta": delta_count, "final_owner": owner_count},
        "owner_files": len(current_files),
        "baton_words": baton_words,
        "local_upstream_tracking_live_equal": True,
        "divergence": "0/0",
        "clean": True,
        "same_owner_not_independent_reproduction": True,
        "full_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "checks": checks,
    }


def write_receipt(payload: dict[str, Any]) -> None:
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    args = parser.parse_args()
    if RECEIPT_PATH.exists():
        raise SystemExit("canonical receipt already exists; replay refused")
    try:
        payload = validate(args.expected_head)
    except Exception as error:
        failure = {
            "state": "INVALID_ZERO_CANONICAL_SUCCESS_CREDIT",
            "invoked_at": now(),
            "invocation_count": 1,
            "canonical_success_count": 0,
            "successful_replay_count": 0,
            "expected_head": args.expected_head,
            "error_type": type(error).__name__,
            "error": sanitize(str(error)),
            "same_owner_recovery_not_independent_reproduction": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_receipt(failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1
    write_receipt(payload)
    print(json.dumps({key: payload[key] for key in ("state", "expected_head", "tests", "detailed_checks", "minimal_checks", "json_parses", "privacy_scan", "manifest_replay", "owner_files", "baton_words", "terminal_verdict")}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
