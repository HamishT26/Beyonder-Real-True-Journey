from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v672-v1-2-remaster"
CLOSEOUT = PHASE_ROOT / "closeout"
HANDOFF = PHASE_ROOT / "handoffs" / "auren-lark-v672-v2-activation.md"
SOURCE = "f67221fbee56905a770c64533771dd9471fb2fba"
X1_COMMIT = "da48a47bd21a8e3053094d39691eb72ef1429abd"
EVIDENCE_COMMIT = "1c29b148e90c21aa4ed819281b024256114c50d9"
BRANCH = "codex/GHC-Family/ilyra-fen-v672-v1-2-remaster"
RECEIPT_ROOT = Path(r"D:\GHC-Archives\phase-tools\ilyra-fen-v672-v1-2-remaster")


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
    ).stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8", errors="strict").strip()


def load(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, observed: Any) -> None:
    checks.append({"name": name, "passed": passed, "observed": observed})
    if not passed:
        raise RuntimeError(f"canonical check failed: {name}: {observed}")


def run_tests() -> dict[str, Any]:
    command = [
        "python",
        "-m",
        "pytest",
        "-q",
        "tests/test_ghc_family_ilyra_fen_v672_v1_2_remaster_x1.py",
        "tests/test_ghc_family_ilyra_fen_v672_v1_2_remaster_x2.py",
        "tests/test_ghc_family_ilyra_fen_v672_v1_2_remaster_final.py",
        "-k",
        "not x1_is_planning_only_and_source_anchored and not strict_x1_before_x2_gate",
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    passed_match = re.search(r"(\d+) passed", output)
    deselected_match = re.search(r"(\d+) deselected", output)
    if result.returncode != 0 or passed_match is None:
        raise RuntimeError(f"selected test invocation failed: {output[-4000:]}")
    return {
        "exit": result.returncode,
        "passed": int(passed_match.group(1)),
        "deselected": int(deselected_match.group(1)) if deselected_match else 0,
        "output_tail": output[-2000:],
        "complete_repository_suite": False,
    }


def replay_manifests(checks: list[dict[str, Any]]) -> dict[str, int]:
    evidence = load(CLOSEOUT / "immutable-evidence-manifest.json")
    evidence_mismatches = []
    for row in evidence["entries"]:
        payload = git_bytes("show", f"{EVIDENCE_COMMIT}:{row['path']}")
        if hashlib.sha256(payload).hexdigest() != row["sha256"] or len(payload) != row["bytes"]:
            evidence_mismatches.append(row["path"])
    add_check(checks, "immutable_evidence_manifest", not evidence_mismatches, evidence_mismatches)

    counts: dict[str, int] = {"immutable_evidence": evidence["entry_count"]}
    for label, path in [
        ("x2_owner", PHASE_ROOT / "x2" / "owner-manifest.json"),
        ("closeout_owner", CLOSEOUT / "owner-manifest.json"),
    ]:
        manifest = load(path)
        mismatches = []
        for row in manifest["entries"]:
            target = ROOT / row["path"]
            if not target.is_file():
                mismatches.append({"path": row["path"], "reason": "absent"})
            elif hashlib.sha256(target.read_bytes()).hexdigest() != row["sha256"]:
                mismatches.append({"path": row["path"], "reason": "sha256"})
            elif target.stat().st_size != row["bytes"]:
                mismatches.append({"path": row["path"], "reason": "bytes"})
        add_check(checks, f"{label}_manifest", not mismatches, mismatches[:5])
        counts[label] = manifest["entry_count"]
    return counts


def strict_json_scan(checks: list[dict[str, Any]]) -> int:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    for path in paths:
        load(path)
    add_check(checks, "strict_json_parses", len(paths) >= 110, len(paths))
    return len(paths)


def privacy_scan(checks: list[dict[str, Any]]) -> dict[str, Any]:
    patterns = {
        "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "openai_token": re.compile(rb"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        "github_token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        "aws_access_key": re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
        "consumer_email": re.compile(
            rb"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
    }
    candidates = []
    scanned = 0
    for path in sorted(PHASE_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt", ".py"}:
            continue
        scanned += 1
        payload = path.read_bytes()
        for label, pattern in patterns.items():
            if pattern.search(payload):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": label})
    add_check(checks, "five_class_privacy_scan", not candidates, candidates)
    return {"files": scanned, "classes": sorted(patterns), "confirmed_candidates": len(candidates)}


def ast_scan(checks: list[dict[str, Any]], head: str) -> dict[str, Any]:
    paths = [
        path
        for path in git(
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            f"{SOURCE}..{head}",
            "--",
            "*.py",
        ).splitlines()
        if path
    ]
    findings = []
    parsed = 0
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        parsed += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": relative, "line": node.lineno, "finding": node.func.id})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": relative, "line": node.lineno, "finding": "shell=True"})
    add_check(checks, "bounded_changed_python_ast_scan", not findings, findings)
    return {"changed_python_paths": len(paths), "parsed_working_paths": parsed, "findings": len(findings)}


def word_scan(checks: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for path in sorted(PHASE_ROOT.rglob("*.md")):
        words = re.findall(r"\b\w+(?:[-']\w+)*\b", path.read_text(encoding="utf-8"))
        ceiling = 100000 if path == HANDOFF else 6000
        rows.append({"path": path.relative_to(ROOT).as_posix(), "words": len(words), "ceiling": ceiling})
    violations = [row for row in rows if row["words"] > row["ceiling"]]
    baton_row = next(row for row in rows if row["path"] == HANDOFF.relative_to(ROOT).as_posix())
    add_check(checks, "document_word_ceilings", not violations, violations)
    add_check(checks, "baton_word_floor", baton_row["words"] >= 10000, baton_row["words"])
    return {"documents": len(rows), "baton_words": baton_row["words"], "violations": len(violations)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    args = parser.parse_args()
    expected_head = args.expected_head
    receipt = RECEIPT_ROOT / f"{expected_head[:12]}-exact-final-canonical-receipt.json"
    if receipt.exists():
        raise RuntimeError(f"canonical receipt already exists; replay refused: {receipt}")

    checks: list[dict[str, Any]] = []
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    status_before = git("status", "--porcelain=v1")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh = git("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    parent_lines = git("rev-list", "--parents", "-n", "1", head).split()
    commit_count = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = [line for line in git("rev-list", "--merges", f"{SOURCE}..{head}").splitlines() if line]

    add_check(checks, "expected_exact_head", head == expected_head, head)
    add_check(checks, "exact_branch", branch == BRANCH, branch)
    add_check(checks, "clean_before", status_before == "", status_before)
    add_check(checks, "four_way_equality", len({head, upstream, tracking, fresh}) == 1, [head, upstream, tracking, fresh])
    add_check(checks, "zero_divergence", divergence == ["0", "0"], divergence)
    add_check(checks, "one_final_parent", len(parent_lines) == 2, parent_lines)
    add_check(checks, "final_direct_child_of_evidence", parent_lines[1] == EVIDENCE_COMMIT, parent_lines[1])
    add_check(checks, "x1_direct_child_of_source", git("rev-parse", f"{X1_COMMIT}^") == SOURCE, X1_COMMIT)
    add_check(checks, "evidence_direct_child_of_x1", git("rev-parse", f"{EVIDENCE_COMMIT}^") == X1_COMMIT, EVIDENCE_COMMIT)
    add_check(checks, "commit_count_from_source", commit_count == 3, commit_count)
    add_check(checks, "zero_merges", not merges, merges)
    add_check(
        checks,
        "source_ancestral",
        subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", SOURCE, head],
            check=False,
        ).returncode
        == 0,
        SOURCE,
    )
    add_check(
        checks,
        "x1_ancestral",
        subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", X1_COMMIT, head],
            check=False,
        ).returncode
        == 0,
        X1_COMMIT,
    )
    add_check(
        checks,
        "evidence_ancestral",
        subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", EVIDENCE_COMMIT, head],
            check=False,
        ).returncode
        == 0,
        EVIDENCE_COMMIT,
    )

    tests = run_tests()
    add_check(checks, "selected_owner_tests", tests["exit"] == 0 and tests["passed"] >= 45, tests)
    manifest_counts = replay_manifests(checks)
    json_count = strict_json_scan(checks)
    privacy = privacy_scan(checks)
    security = ast_scan(checks, head)
    words = word_scan(checks)
    route = load(CLOSEOUT / "route-candidate.json")
    add_check(checks, "route_prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and route["precontact"] is False, route)
    add_check(checks, "exact_target", route["target_exact_title"] == "Auren Lark" and route["target_phase"] == "v672-v2", route)
    phase_truth = load(CLOSEOUT / "phase-truth.json")
    add_check(checks, "terminal_verdict", phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase_truth["terminal_verdict"])
    add_check(checks, "original_canonical_not_replayed", phase_truth["original_canonical_replayed"] is False, phase_truth["original_canonical_replayed"])
    materialized_files = sum(path.is_file() for path in ROOT.rglob("*"))
    add_check(checks, "materialized_file_ceiling", materialized_files < 2000, materialized_files)
    status_after = git("status", "--porcelain=v1")
    add_check(checks, "clean_after", status_after == "", status_after)

    payload = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v6",
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Ilyra Fen",
        "phase": "v672-v1-2-remaster",
        "branch": BRANCH,
        "source": SOURCE,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "exact_final": head,
        "tests": tests,
        "check_count": len(checks),
        "checks": checks,
        "strict_json_parses": json_count,
        "manifest_entries": manifest_counts,
        "privacy": privacy,
        "bounded_security": security,
        "word_scan": words,
        "materialized_files": materialized_files,
        "commit_count_from_source": commit_count,
        "merge_count": len(merges),
        "final_parent_count": len(parent_lines) - 1,
        "clean_before": True,
        "clean_after": True,
        "four_way_equal": True,
        "zero_divergence": True,
        "canonical_invocations_for_exact_head": 1,
        "replay_after_success": False,
        "complete_repository_suite": False,
        "independent_reproduction": False,
        "external_audit": False,
        "production_certification": False,
        "exhaustive_security": False,
        "privacy_complete": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    temporary = receipt.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    temporary.replace(receipt)
    print(
        json.dumps(
            {
                "state": payload["state"],
                "exact_final": head,
                "tests_passed": tests["passed"],
                "checks": len(checks),
                "strict_json_parses": json_count,
                "privacy_candidates": privacy["confirmed_candidates"],
                "security_findings": security["findings"],
                "receipt": receipt.as_posix(),
                "receipt_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest(),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
