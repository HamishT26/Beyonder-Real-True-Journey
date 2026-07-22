#!/usr/bin/env python3
"""Run the one credited exact-final canonical validation without mutating the repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/ilyra-fen/v651-v8-special-cli-prep")
PHASE = ROOT / PHASE_REL
SOURCE = "68f7e9b7fc454746c02b8a85987e10b87a0725c3"
X1 = "580a3f0155c589866fd7f4aacd88790419cd147a"
EVIDENCE = "0b382d660837536e12672e28cc68f6208e2b0069"
BRANCH = "codex/GHC-Family/ilyra-fen-v651-v8-special-cli-prep"
PRIVACY = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_local_path": re.compile(r"(?i)(?:[a-z]:\\users\\|/users/|/home/)[^\s\"'<>]+"),
    "delegation_markup": re.compile(r"(?i)<\s*/?\s*codex_delegation\b"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file)://[^\s\"'<>]+"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s,;}]+"),
}


def run(args: list[str], *, binary: bool = False, check: bool = True):
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
        timeout=180,
        check=check,
    )


def git(*args: str, binary: bool = False):
    return run(["git", *args], binary=binary).stdout


def verify_manifest(relative: str) -> tuple[int, list[str], list[str]]:
    payload = json.loads((PHASE / relative).read_text(encoding="utf-8"))
    issues = []
    for row in payload["entries"]:
        data = git("show", f"HEAD:{row['path']}", binary=True)
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            issues.append(row["path"])
    exclusions = payload.get("self_exclusions", payload.get("declared_exclusions", []))
    return len(payload["entries"]), exclusions, issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    checks = []
    issues = []

    def check(label: str, condition: bool, detail=None) -> None:
        checks.append({"check": label, "passed": bool(condition), "detail": detail})
        if not condition:
            issues.append(label)

    status_before = git("status", "--porcelain=v1", "--untracked-files=all")
    head = git("rev-parse", "HEAD").strip()
    check("clean_before", status_before == "", status_before)
    check("exact_head", head == args.expected_head, head)
    check("branch", git("branch", "--show-current").strip() == BRANCH)
    for label, ancestor in (("source", SOURCE), ("x1", X1), ("evidence", EVIDENCE)):
        result = run(["git", "merge-base", "--is-ancestor", ancestor, "HEAD"], check=False)
        check(f"{label}_ancestry", result.returncode == 0)
    commits = git("rev-list", "--count", f"{SOURCE}..HEAD").strip()
    merges = git("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()
    parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
    check("three_phase_commits", commits == "3", commits)
    check("zero_merges", not merges, len(merges))
    check("one_final_parent", len(parents) == 2, len(parents) - 1)

    x2_tests = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_ghc_family_v651_v8_special_x2.py", "-v"], check=False)
    closeout_tests = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_ghc_family_v651_v8_special_closeout.py", "-v"], check=False)
    x2_count = len(re.findall(r"^test_", x2_tests.stderr, flags=re.MULTILINE))
    closeout_count = len(re.findall(r"^test_", closeout_tests.stderr, flags=re.MULTILINE))
    check("x2_tests", x2_tests.returncode == 0 and x2_count == 21, {"count": x2_count, "exit": x2_tests.returncode})
    check("closeout_tests", closeout_tests.returncode == 0 and closeout_count == 8, {"count": closeout_count, "exit": closeout_tests.returncode})

    evidence_receipt = Path(args.receipt).with_name("evidence-recheck.json")
    detailed = run([sys.executable, "scripts/ghc_family_v651_v8_special_evidence_validate.py", "--receipt", str(evidence_receipt)], check=False)
    detailed_payload = json.loads(evidence_receipt.read_text(encoding="utf-8")) if evidence_receipt.exists() else {}
    check("detailed_checks", detailed.returncode == 0 and detailed_payload.get("checks") == 34 and detailed_payload.get("valid") is True, {"checks": detailed_payload.get("checks"), "exit": detailed.returncode})

    json_issues = []
    privacy_hits = []
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        raw = git("show", f"HEAD:{relative}", binary=True)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                json_issues.append(f"{relative}:{exc.lineno}")
        if path.suffix.lower() in {".json", ".md", ".txt", ".html"}:
            for name, pattern in PRIVACY.items():
                if pattern.search(text):
                    privacy_hits.append({"path": relative, "class": name})
    check("json_parse", not json_issues, {"documents": len(list(PHASE.rglob('*.json'))), "issues": json_issues})
    check("privacy_zero", not privacy_hits, {"files": len(files), "classes": len(PRIVACY), "hits": privacy_hits})
    check("owner_file_threshold", len(files) < 2_000, len(files))

    owner_entries, owner_exclusions, owner_issues = verify_manifest("validation/final-owner-manifest.json")
    delta_entries, delta_exclusions, delta_issues = verify_manifest("validation/final-delta-manifest.json")
    x1_manifest = json.loads(git("show", f"{X1}:{PHASE_REL.as_posix()}/validation/x1-index-manifest.json"))
    x1_issues = []
    for row in x1_manifest["entries"]:
        data = git("show", f"{X1}:{row['path']}", binary=True)
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            x1_issues.append(row["path"])
    evidence_manifest = json.loads(git("show", f"{EVIDENCE}:{PHASE_REL.as_posix()}/validation/evidence-index-manifest.json"))
    evidence_issues = []
    for row in evidence_manifest["entries"]:
        data = git("show", f"{EVIDENCE}:{row['path']}", binary=True)
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            evidence_issues.append(row["path"])
    phase_paths = set(git("ls-tree", "-r", "--name-only", "HEAD", PHASE_REL.as_posix()).splitlines())
    owner_manifest = json.loads((PHASE / "validation/final-owner-manifest.json").read_text(encoding="utf-8"))
    owner_covered = {row["path"] for row in owner_manifest["entries"]} | set(owner_exclusions)
    check("owner_manifest", not owner_issues and owner_covered == phase_paths, {"entries": owner_entries, "exclusions": len(owner_exclusions), "mismatches": owner_issues, "coverage_delta": len(owner_covered ^ phase_paths)})
    check("delta_manifest", not delta_issues, {"entries": delta_entries, "exclusions": len(delta_exclusions), "mismatches": delta_issues})
    check("x1_manifest", not x1_issues, {"entries": len(x1_manifest["entries"]), "mismatches": x1_issues})
    check("evidence_manifest", not evidence_issues, {"entries": len(evidence_manifest["entries"]), "mismatches": evidence_issues})

    diff_check = run(["git", "diff", "--check", f"{SOURCE}..HEAD"], check=False)
    check("diff_hygiene", diff_check.returncode == 0 and not diff_check.stdout, diff_check.stdout)
    local = head
    upstream = git("rev-parse", "@{u}").strip()
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
    live_text = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").strip()
    live = live_text.split("\t", 1)[0] if live_text else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").strip()
    check("four_way_equality", local == upstream == tracking == live and divergence.replace("\t", " ") == "0 0", {"local": local, "upstream": upstream, "tracking": tracking, "live": live, "divergence": divergence})
    check("commit_cap", int(commits) <= 12, commits)
    truth = json.loads((PHASE / "truth/phase-truth.json").read_text(encoding="utf-8"))
    check("truth", truth["effective_negatives"] == 7855 and truth["effective_open_gaps"] == 61 and truth["effective_exact_gates"] == 62 and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("future_cli_zero", truth["future_cli_seats_named"] == 0 and truth["future_cli_seats_launched"] == 0)
    check("route_held_before_ack", truth["terminal_delivery_state"] == "PREPARED_NOT_SENT")
    status_after = git("status", "--porcelain=v1", "--untracked-files=all")
    check("clean_after", status_after == "", status_after)

    payload = {
        "schema": "ghc.family.v651-v8-special.terminal-validation.v1",
        "phase": "v651-v8-special-cli-prep",
        "exact_head": head,
        "checks": len(checks),
        "check_rows": checks,
        "issues": issues,
        "scoped_tests": {"x2": x2_count, "closeout": closeout_count, "total": x2_count + closeout_count},
        "detailed_checks": detailed_payload.get("checks"),
        "json_documents": len(list(PHASE.rglob("*.json"))),
        "public_files_scanned": len(files),
        "privacy_classes": len(PRIVACY),
        "confirmed_privacy_hits": privacy_hits,
        "owner_manifest_entries": owner_entries,
        "owner_manifest_exclusions": owner_exclusions,
        "delta_manifest_entries": delta_entries,
        "delta_manifest_exclusions": delta_exclusions,
        "phase_commits": int(commits),
        "merge_commits": len(merges),
        "final_parents": len(parents) - 1,
        "four_way_equal": local == upstream == tracking == live,
        "valid": not issues,
        "same_owner_only": True,
        "independent_reproduction": False,
        "replay_after_success": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One credited bounded exact-final canonical validation under shared infrastructure; not full-suite, independent reproduction, external audit, production certification, scientific confirmation, professional authority, legal or cultural authority, complete privacy or accessibility, exhaustive security, consciousness/personhood, or Stage 20 evidence.",
    }
    receipt = Path(args.receipt)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": not issues, "checks": len(checks), "issues": issues, "tests": x2_count + closeout_count, "detailed": detailed_payload.get("checks"), "json": payload["json_documents"], "files": len(files), "owner_manifest": owner_entries, "delta_manifest": delta_entries}))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
