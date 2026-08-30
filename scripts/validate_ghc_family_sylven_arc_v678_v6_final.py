#!/usr/bin/env python3
"""Exclusive owner-scoped exact-final validator for Sylven Arc v678-v6."""

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


BRANCH = "codex/GHC-Family/sylven-arc-v678-v6-full-tools"
SOURCE = "d7a2e3d1851d8a9eb6a8707968a47354b44e824a"
X1 = "22d310c7ae4fdbd45959d388d15642039d748da0"
EVIDENCE = "7b747952b6a6916c3881066865ff7021aeabea3c"
FIRST_FINAL = "ea27f954b8636f167c83b964c0ba5ad15301ea1e"
FINAL_TEST = "tests/test_ghc_family_sylven_arc_v678_v6_final.py"
CORRECTION_TEST = "tests/test_ghc_family_sylven_arc_v678_v6_correction1.py"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}
PRIVACY = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(terminal transcript|session stream|screenshot payload)"),
}


def run(repo: Path, args: list[str], timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, timeout=timeout)


def git(repo: Path, *args: str) -> str:
    result = run(repo, ["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip() or "git command failed")
    return result.stdout.decode("utf-8").strip()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def atomic_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(canonical_bytes(value))
    os.replace(temporary, path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref_blob(repo: Path, ref: str, path: str) -> bytes:
    result = run(repo, ["git", "show", f"{ref}:{path}"])
    if result.returncode:
        raise RuntimeError(f"missing Git blob {path}")
    return result.stdout


def is_owner(path: str) -> bool:
    return (
        path.startswith("docs/sylven-arc/v678-v6/")
        or (path.startswith("scripts/") and "sylven_arc_v678_v6" in path)
        or (path.startswith("tests/") and "sylven_arc_v678_v6" in path)
    )


def equality(repo: Path, expected: str) -> dict[str, Any]:
    branch = git(repo, "branch", "--show-current")
    local = git(repo, "rev-parse", "HEAD")
    upstream = git(repo, "rev-parse", "@{upstream}")
    tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_output = git(repo, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_output.split()[0] if live_output else ""
    divergence = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    return {
        "branch": branch, "local": local, "upstream": upstream, "tracking": tracking, "fresh_live": live,
        "expected_head": expected, "all_equal": local == upstream == tracking == live == expected,
        "divergence": [int(value) for value in divergence], "clean": not bool(git(repo, "status", "--porcelain")),
    }


def topology(repo: Path, final: str) -> dict[str, Any]:
    commits = git(repo, "rev-list", "--count", f"{SOURCE}..{final}")
    merges = git(repo, "rev-list", "--merges", "--count", f"{SOURCE}..{final}")
    parents = git(repo, "show", "-s", "--format=%P", final).split()
    first_final_parent = git(repo, "rev-parse", f"{FIRST_FINAL}^")
    return {
        "source_is_x1_parent": git(repo, "rev-parse", f"{X1}^") == SOURCE,
        "x1_is_evidence_parent": git(repo, "rev-parse", f"{EVIDENCE}^") == X1,
        "evidence_is_first_final_parent": first_final_parent == EVIDENCE,
        "first_final_is_corrected_final_parent": len(parents) == 1 and parents[0] == FIRST_FINAL,
        "phase_commits": int(commits), "merges": int(merges), "final_parent_count": len(parents),
        "source_ancestor": run(repo, ["git", "merge-base", "--is-ancestor", SOURCE, final]).returncode == 0,
    }


def manifest_check(repo: Path, final: str) -> dict[str, Any]:
    checks = {}
    commands = [
        ("evidence", [sys.executable, "-X", "utf8", "scripts/ghc_family_sylven_arc_v678_v6_evidence_manifest.py", "verify", "--repo", ".", "--ref", EVIDENCE]),
        ("first_final", [sys.executable, "-X", "utf8", "scripts/ghc_family_sylven_arc_v678_v6_final_manifest.py", "verify", "--repo", ".", "--ref", FIRST_FINAL]),
        ("correction1", [sys.executable, "-X", "utf8", "scripts/ghc_family_sylven_arc_v678_v6_correction1_manifest.py", "verify", "--repo", ".", "--ref", final]),
    ]
    for name, command in commands:
        result = run(repo, command, timeout=240)
        checks[name] = {
            "passed": result.returncode == 0,
            "result": json.loads(result.stdout.decode("utf-8")) if result.returncode == 0 else None,
            "error": result.stderr.decode("utf-8", errors="replace")[:500] if result.returncode else "",
        }
    return checks


def parse_json(repo: Path, final: str, owner_paths: list[str]) -> dict[str, Any]:
    failures = []
    count = 0
    for path in owner_paths:
        if not path.endswith(".json"):
            continue
        count += 1
        try:
            json.loads(ref_blob(repo, final, path).decode("utf-8"))
        except Exception as exc:
            failures.append({"path": path, "error": type(exc).__name__})
    return {"count": count, "failures": failures, "passed": not failures}


def privacy_check(repo: Path, final: str, owner_paths: list[str]) -> dict[str, Any]:
    candidates = []
    confirmed = []
    definition_or_metadata = {
        "scripts/ghc_family_sylven_arc_v678_v6_core.py",
        "scripts/ghc_family_sylven_arc_v678_v6_flashcards.py",
        "scripts/ghc_family_sylven_arc_v678_v6_evidence_manifest.py",
        "scripts/ghc_family_sylven_arc_v678_v6_final_manifest.py",
        "scripts/validate_ghc_family_sylven_arc_v678_v6_final.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_x1.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_x2.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_final.py",
        "docs/sylven-arc/v678-v6/validation/evidence-staged-review.json",
        "docs/sylven-arc/v678-v6/validation/final-manifest-preflight-recovery.json",
        "docs/sylven-arc/v678-v6/validation/final-staged-review.json",
    }
    scanned = 0
    for path in owner_paths:
        if Path(path).suffix.lower() not in {".json", ".md", ".html", ".py", ".yaml", ".yml", ".txt"}:
            continue
        scanned += 1
        value = ref_blob(repo, final, path).decode("utf-8")
        for kind, pattern in PRIVACY.items():
            if not pattern.search(value):
                continue
            item = {"path": path, "class": kind}
            if path in definition_or_metadata:
                item["adjudication"] = "scanner_definition_or_adjudication_metadata"
                candidates.append(item)
            else:
                item["adjudication"] = "confirmed_or_unresolved_payload"
                confirmed.append(item)
    return {"classes": sorted(PRIVACY), "scanned_files": scanned, "candidates": candidates, "confirmed": confirmed, "passed": not confirmed}


def code_check(repo: Path, final: str) -> dict[str, Any]:
    paths = [path for path in git(repo, "diff", "--name-only", SOURCE, final).splitlines() if path.endswith(".py") and is_owner(path)]
    findings = []
    forbidden_calls = {"eval", "exec", "__import__"}
    for path in paths:
        source = ref_blob(repo, final, path).decode("utf-8")
        try:
            tree = ast.parse(source, filename=path)
            compile(source, path, "exec")
        except Exception as exc:
            findings.append({"path": path, "kind": type(exc).__name__})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                findings.append({"path": path, "kind": f"forbidden_dynamic_call:{node.func.id}"})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"rmtree", "unlink"}:
                findings.append({"path": path, "kind": f"destructive_call:{node.func.attr}"})
    return {"files": len(paths), "findings": findings, "passed": not findings}


def word_and_file_caps(repo: Path, final: str, owner_paths: list[str]) -> dict[str, Any]:
    maximum = 0
    maximum_path = ""
    for path in owner_paths:
        if Path(path).suffix.lower() not in {".md", ".html", ".txt"}:
            continue
        words = len(ref_blob(repo, final, path).decode("utf-8").split())
        if words > maximum:
            maximum = words
            maximum_path = path
    materialized = sum(path.is_file() for path in repo.rglob("*"))
    return {
        "owner_files": len(owner_paths), "materialized_files": materialized,
        "maximum_document_words": maximum, "maximum_document_path": maximum_path,
        "owner_file_cap_passed": len(owner_paths) < 2000, "materialized_file_cap_passed": materialized < 2000,
        "word_cap_passed": maximum <= 100000,
    }


def preflight(repo: Path, expected: str, receipt: Path, latch: Path) -> dict[str, Any]:
    eq = equality(repo, expected)
    topo = topology(repo, expected)
    result = {
        "status": "PASS" if (
            eq["branch"] == BRANCH and eq["all_equal"] and eq["divergence"] == [0, 0] and eq["clean"]
            and topo["source_is_x1_parent"] and topo["x1_is_evidence_parent"] and topo["evidence_is_first_final_parent"]
            and topo["first_final_is_corrected_final_parent"]
            and topo["phase_commits"] == 4 and topo["merges"] == 0 and topo["final_parent_count"] == 1
            and not receipt.exists() and not latch.exists()
        ) else "FAIL",
        "expected_head": expected, "equality": eq, "topology": topo,
        "receipt_absent": not receipt.exists(), "latch_absent": not latch.exists(),
    }
    if result["status"] != "PASS":
        raise SystemExit(json.dumps(result, sort_keys=True))
    return result


def canonical_validate(repo: Path, expected: str, receipt: Path, latch: Path) -> dict[str, Any]:
    pre = preflight(repo, expected, receipt, latch)
    latch.parent.mkdir(parents=True, exist_ok=True)
    with latch.open("x", encoding="utf-8") as handle:
        json.dump({"schema": "ghc-family-canonical-latch/v1", "phase": "v678-v6", "head": expected, "state": "RUNNING", "invocation_count": 1, "success_count": 0, "replay_count": 0}, handle, sort_keys=True)
        handle.write("\n")
    try:
        owner_paths = [path for path in git(repo, "ls-tree", "-r", "--name-only", expected).splitlines() if is_owner(path)]
        tests = run(repo, [sys.executable, "-X", "utf8", "-m", "pytest", "-q", FINAL_TEST, CORRECTION_TEST], timeout=300)
        tests_passed = tests.returncode == 0
        manifests = manifest_check(repo, expected)
        parsed = parse_json(repo, expected, owner_paths)
        privacy = privacy_check(repo, expected, owner_paths)
        code = code_check(repo, expected)
        caps = word_and_file_caps(repo, expected, owner_paths)
        topo = topology(repo, expected)
        eq_after = equality(repo, expected)
        truth = json.loads(ref_blob(repo, expected, "docs/sylven-arc/v678-v6/closeout/phase-truth.json").decode("utf-8"))
        route = json.loads(ref_blob(repo, expected, "docs/sylven-arc/v678-v6/closeout/route-receipt.json").decode("utf-8"))
        detailed = {
            "tests_exact": tests_passed,
            "test_count_exact": tests_passed and "33 passed" in tests.stdout.decode("utf-8", errors="replace"),
            "json_parse": parsed["passed"],
            "json_count_nonzero": parsed["count"] > 250,
            "privacy_five_classes": len(privacy["classes"]) == 5,
            "privacy_zero_confirmed": privacy["passed"],
            "code_compile_ast": code["passed"],
            "code_count_nonzero": code["files"] >= 10,
            "evidence_manifest": manifests["evidence"]["passed"],
            "first_final_manifest": manifests["first_final"]["passed"],
            "correction1_manifest": manifests["correction1"]["passed"],
            "source_parent_x1": topo["source_is_x1_parent"],
            "x1_parent_evidence": topo["x1_is_evidence_parent"],
            "evidence_parent_first_final": topo["evidence_is_first_final_parent"],
            "first_final_parent_corrected_final": topo["first_final_is_corrected_final_parent"],
            "four_commits": topo["phase_commits"] == 4,
            "zero_merges": topo["merges"] == 0,
            "one_final_parent": topo["final_parent_count"] == 1,
            "source_ancestor": topo["source_ancestor"],
            "branch_exact": eq_after["branch"] == BRANCH,
            "head_exact": eq_after["local"] == expected,
            "local_upstream_equal": eq_after["local"] == eq_after["upstream"],
            "local_tracking_equal": eq_after["local"] == eq_after["tracking"],
            "fresh_live_equal": eq_after["local"] == eq_after["fresh_live"],
            "typed_zero_divergence": eq_after["divergence"] == [0, 0],
            "clean_after": eq_after["clean"],
            "owner_file_cap": caps["owner_file_cap_passed"],
            "materialized_file_cap": caps["materialized_file_cap_passed"],
            "word_cap": caps["word_cap_passed"],
            "outcome_labels": set(truth["core_outcomes"]) == LABELS,
            "outcome_counts": truth["core_outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "zero_world_rows": truth["real_world_rows"] == 0,
            "zero_external_actions": truth["external_actions"] == 0,
            "stage20_hold": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
            "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT",
            "route_send_zero": route["send_count"] == 0,
            "canonical_was_pending": truth["validation_state"] == "PENDING_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        }
        minimal = {
            "preflight_passed": pre["status"] == "PASS", "tests": tests_passed,
            "manifests": all(value["passed"] for value in manifests.values()), "json": parsed["passed"],
            "privacy": privacy["passed"], "code": code["passed"], "topology": topo["phase_commits"] == 4 and topo["merges"] == 0,
            "clean": eq_after["clean"], "divergence": eq_after["divergence"] == [0, 0], "four_way": eq_after["all_equal"],
            "file_cap": caps["owner_file_cap_passed"] and caps["materialized_file_cap_passed"], "word_cap": caps["word_cap_passed"],
            "labels": set(truth["core_outcomes"]) == LABELS, "stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
            "route_hold": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0,
        }
        valid = all(detailed.values()) and all(minimal.values())
        payload = {
            "schema": "ghc-family-owner-scoped-canonical-receipt/v1", "owner": "Sylven Arc", "phase": "v678-v6",
            "head": expected, "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "invocation_count": 1, "success_count": 1 if valid else 0, "replay_count": 0,
            "tests": {"passed": 33 if tests_passed else 0, "total": 33, "output_tail": tests.stdout.decode("utf-8", errors="replace")[-500:]},
            "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
            "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
            "json": parsed, "privacy": privacy, "code": code, "manifests": manifests, "topology": topo,
            "caps": caps, "equality_before": pre["equality"], "equality_after": eq_after,
            "full_repository_suite_run": False, "independent_reproduction": False,
            "empirical_confirmation": False, "professional_authority": False, "production_certification": False,
            "privacy_complete": False, "accessibility_complete": False, "maori_authority": False, "stage20_authority": False,
        }
        payload_digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
        receipt_value = {"payload": payload, "payload_sha256": payload_digest}
        atomic_write(receipt, receipt_value)
        atomic_write(latch, {
            "schema": "ghc-family-canonical-latch/v1", "phase": "v678-v6", "head": expected,
            "state": "SUCCEEDED" if valid else "FAILED", "invocation_count": 1,
            "success_count": 1 if valid else 0, "replay_count": 0,
            "receipt_sha256": sha256(receipt), "payload_sha256": payload_digest,
        })
        if not valid:
            raise SystemExit(json.dumps({"status": payload["status"], "receipt_sha256": sha256(receipt)}, sort_keys=True))
        return {"status": payload["status"], "receipt_sha256": sha256(receipt), "latch_sha256": sha256(latch), "payload_sha256": payload_digest, "tests": "33/33", "detailed": f"{sum(detailed.values())}/{len(detailed)}", "minimal": f"{sum(minimal.values())}/{len(minimal)}", "json": parsed["count"], "privacy_confirmed": len(privacy["confirmed"]), "owner_files": len(owner_paths)}
    except Exception as exc:
        if not receipt.exists():
            atomic_write(receipt, {"schema": "ghc-family-owner-scoped-canonical-receipt/v1", "owner": "Sylven Arc", "phase": "v678-v6", "head": expected, "status": "INVALID_EXCEPTION", "error_type": type(exc).__name__, "invocation_count": 1, "success_count": 0, "replay_count": 0})
        atomic_write(latch, {"schema": "ghc-family-canonical-latch/v1", "phase": "v678-v6", "head": expected, "state": "FAILED", "invocation_count": 1, "success_count": 0, "replay_count": 0, "receipt_sha256": sha256(receipt)})
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preflight", "canonical"))
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--latch", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.command == "preflight":
        result = preflight(repo, args.expected_head, args.receipt.resolve(), args.latch.resolve())
    else:
        result = canonical_validate(repo, args.expected_head, args.receipt.resolve(), args.latch.resolve())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
