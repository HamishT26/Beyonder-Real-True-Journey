#!/usr/bin/env python3
"""One-shot ancestry-aware complete unittest aggregate for the Neris remaster."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import unittest
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH = "codex/GHC-Family/neris-solane-v662-v3-2-remaster"
PHASE_ROOT = "docs/neris-solane/v662-v3-2-remaster"
FINAL_VALIDATION = f"{PHASE_ROOT}/validation/final-validation.json"
FINAL_PRIVACY = f"{PHASE_ROOT}/validation/final-privacy-scan.json"
FINAL_OWNER_MANIFEST = f"{PHASE_ROOT}/validation/final-owner-manifest.json"
FINAL_DELTA_MANIFEST = f"{PHASE_ROOT}/validation/final-delta-manifest.json"
FINAL_ROUTE = f"{PHASE_ROOT}/routing/route-state-final.json"
FINAL_TRUTH = f"{PHASE_ROOT}/truth/final-truth.json"
TEST_PATTERN = "test*.py"
BRANCH_PATTERN = re.compile(r"codex/GHC-Family/[A-Za-z0-9._/-]+")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def git(*args: str, cwd: Path = ROOT, check: bool = True, timeout: int = 600) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, timeout=timeout)
    if check and completed.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed with {completed.returncode}: {completed.stderr[-1000:].decode('utf-8', 'replace')}")
    return completed


def git_text(*args: str, cwd: Path = ROOT, check: bool = True, timeout: int = 600) -> str:
    return git(*args, cwd=cwd, check=check, timeout=timeout).stdout.decode("utf-8", "replace").strip()


def git_blob(revision: str, relative: str) -> bytes:
    return git("show", f"{revision}:{relative}").stdout


def committed_json(revision: str, relative: str) -> dict[str, Any]:
    return json.loads(git_blob(revision, relative).decode("utf-8"))


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def current_inventory() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), pattern=TEST_PATTERN)
    tests = list(flatten(suite))
    test_ids = [test.id() for test in tests]
    if loader.errors:
        raise RuntimeError({"loader_errors": loader.errors})
    if len(test_ids) != len(set(test_ids)):
        raise RuntimeError("duplicate current unittest identifiers")
    by_module: dict[str, list[str]] = defaultdict(list)
    module_paths: dict[str, str] = {}
    for test in tests:
        module = test.__class__.__module__
        by_module[module].append(test.id())
        loaded = sys.modules.get(module)
        if loaded is None or not getattr(loaded, "__file__", None):
            raise RuntimeError(f"cannot resolve module file for {module}")
        module_paths[module] = Path(loaded.__file__).resolve().relative_to(ROOT).as_posix()
    ordered_ids = sorted(test_ids)
    return {
        "test_count": len(test_ids),
        "unique_test_count": len(set(test_ids)),
        "module_count": len(by_module),
        "selection_sha256": sha256("\n".join(ordered_ids).encode("utf-8")),
        "by_module": {module: sorted(ids) for module, ids in sorted(by_module.items())},
        "module_paths": module_paths,
        "loader_errors": [],
        "duplicate_ids": 0,
    }


def definition_commits(expected_head: str, inventory: dict[str, Any]) -> list[dict[str, Any]]:
    test_paths = set(inventory["module_paths"].values())
    history = git_text("log", expected_head, "--format=@@%H", "--name-only", "--", "tests")
    anchors: dict[str, str] = {}
    current = ""
    for line in history.splitlines():
        if line.startswith("@@"):
            current = line[2:]
        elif line in test_paths and line not in anchors:
            anchors[line] = current
    if set(anchors) != test_paths:
        raise RuntimeError({"unmapped_test_paths": sorted(test_paths - set(anchors))})
    rows = []
    for module, ids in sorted(inventory["by_module"].items()):
        path = inventory["module_paths"][module]
        anchor = anchors[path]
        final_blob = git_blob(expected_head, path)
        anchor_blob = git_blob(anchor, path)
        if final_blob != anchor_blob:
            raise RuntimeError(f"definition blob mismatch for {path}")
        hints = sorted(set(BRANCH_PATTERN.findall(final_blob.decode("utf-8", "replace"))))
        if len(hints) > 1:
            raise RuntimeError({"ambiguous_branch_hints": path, "hints": hints})
        rows.append(
            {
                "module": module,
                "path": path,
                "definition_commit": anchor,
                "blob_sha256": sha256(final_blob),
                "test_id_count": len(ids),
                "test_id_sha256": sha256("\n".join(ids).encode("utf-8")),
                "branch_hint": hints[0] if hints else None,
            }
        )
    return rows


def replay_manifest(revision: str, relative: str) -> dict[str, Any]:
    manifest = committed_json(revision, relative)
    mismatches = []
    for entry in manifest["entries"]:
        payload = git_blob(revision, entry["path"])
        if len(payload) != entry["bytes"] or sha256(payload) != entry["sha256"]:
            mismatches.append(entry["path"])
    return {"path": relative, "entries": manifest["entry_count"], "mismatches": mismatches, "valid": not mismatches}


def repository_clean() -> dict[str, Any]:
    tracked = git("diff-index", "--quiet", "HEAD", "--", check=False, timeout=900).returncode == 0
    untracked = [row for row in git_text("ls-files", "--others", "--exclude-standard", timeout=900).splitlines() if row]
    return {"tracked_clean": tracked, "untracked_count": len(untracked), "clean": tracked and not untracked}


def remote_equality(expected_head: str) -> dict[str, Any]:
    local = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": int(divergence[0]),
        "behind": int(divergence[1]),
        "valid": local == upstream == tracking == live == expected_head and divergence == ["0", "0"],
    }


def json_parse(revision: str) -> dict[str, Any]:
    paths = [row for row in git_text("ls-tree", "-r", "--name-only", revision, "--", PHASE_ROOT).splitlines() if row.endswith(".json")]
    failures = []
    for path in paths:
        try:
            json.loads(git_blob(revision, path).decode("utf-8"))
        except Exception as error:  # pragma: no cover - diagnostic path
            failures.append({"path": path, "error": type(error).__name__})
    return {"count": len(paths), "parsed": len(paths) - len(failures), "failures": failures, "valid": not failures}


def preflight(expected_head: str, receipt_dir: Path, scratch_root: Path) -> dict[str, Any]:
    inventory = current_inventory()
    rows = definition_commits(expected_head, inventory)
    equality = remote_equality(expected_head)
    clean = repository_clean()
    final_validation = committed_json(expected_head, FINAL_VALIDATION)
    privacy = committed_json(expected_head, FINAL_PRIVACY)
    route = committed_json(expected_head, FINAL_ROUTE)
    truth = committed_json(expected_head, FINAL_TRUTH)
    owner_manifest = replay_manifest(expected_head, FINAL_OWNER_MANIFEST)
    delta_manifest = replay_manifest(expected_head, FINAL_DELTA_MANIFEST)
    invocation_marker = receipt_dir / "canonical-invocation-marker.json"
    success_latch = receipt_dir / "canonical-success-latch.json"
    checks = {
        "exact_head": git_text("rev-parse", "HEAD") == expected_head,
        "exact_branch": git_text("branch", "--show-current") == BRANCH,
        "clean_state": clean["clean"],
        "four_way_remote_equality": equality["valid"],
        "loader_errors_zero": not inventory["loader_errors"],
        "duplicate_test_ids_zero": inventory["duplicate_ids"] == 0,
        "all_modules_mapped": len(rows) == inventory["module_count"],
        "all_definition_blobs_equal": all(row["blob_sha256"] for row in rows),
        "owner_manifest_replays": owner_manifest["valid"],
        "delta_manifest_replays": delta_manifest["valid"],
        "final_validation_valid": final_validation["valid"],
        "privacy_zero": privacy["confirmed_hit_count"] == 0,
        "privacy_not_complete": privacy["privacy_complete"] is False,
        "route_not_sent": route["message_attempted"] is False and route["sent"] is False,
        "not_ready_for_stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "scratch_root_absent": not scratch_root.exists(),
        "invocation_marker_absent": not invocation_marker.exists(),
        "success_latch_absent": not success_latch.exists(),
    }
    anchor_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        anchor_counts[row["definition_commit"]] += 1
    return {
        "schema": "ghc.family.v662-v3-2-remaster.canonical-preflight.v1",
        "expected_head": expected_head,
        "recorded_at_utc": utc_now(),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "valid": all(checks.values()),
        "inventory": {key: inventory[key] for key in ("test_count", "unique_test_count", "module_count", "selection_sha256", "loader_errors", "duplicate_ids")},
        "definition_anchors": len(anchor_counts),
        "largest_anchor_group": max(anchor_counts.values()),
        "module_ledger": rows,
        "remote_equality": equality,
        "clean_state": clean,
        "owner_manifest": owner_manifest,
        "delta_manifest": delta_manifest,
        "json": json_parse(expected_head),
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Read-only exact-final inventory and structural preflight only; no test body ran and no complete-suite success is claimed.",
    }


def bounded_process(command: list[str], cwd: Path, timeout: int) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONUTF8"] = "1"
    flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environment, creationflags=flags)
    timed_out = False
    try:
        output, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], check=False, capture_output=True)
        output, _ = process.communicate()
    return {
        "returncode": process.returncode,
        "timed_out": timed_out,
        "duration_seconds": round(time.monotonic() - started, 3),
        "output_sha256": sha256(output),
        "output": output,
    }


def worker_run(worker_id: int, groups: list[tuple[str, list[dict[str, Any]]]], scratch_root: Path, module_timeout: int) -> dict[str, Any]:
    worker = scratch_root / f"worker-{worker_id:02d}"
    clone = bounded_process(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(worker)], scratch_root, 1200)
    if clone["returncode"] != 0 or clone["timed_out"]:
        return {"worker": worker_id, "clone_valid": False, "modules": [], "failures": [{"kind": "clone_failure", "output_sha256": clone["output_sha256"]}]}
    module_results = []
    failures = []
    for group_index, (anchor, rows) in enumerate(groups, 1):
        hints = sorted({row["branch_hint"] for row in rows if row["branch_hint"]})
        if len(hints) > 1:
            failures.append({"kind": "branch_hint_ambiguity", "anchor": anchor, "count": len(hints)})
            continue
        switch_command = ["git", "switch", "-C", hints[0], anchor] if hints else ["git", "switch", "--detach", anchor]
        switched = bounded_process(switch_command, worker, 1200)
        if switched["returncode"] != 0 or switched["timed_out"]:
            failures.append({"kind": "anchor_switch_failure", "anchor": anchor, "output_sha256": switched["output_sha256"]})
            continue
        for row in rows:
            result = bounded_process(
                [sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", "tests", "-p", Path(row["path"]).name, "-v"],
                worker,
                module_timeout,
            )
            text = result.pop("output").decode("utf-8", "replace")
            count_match = re.search(r"Ran\s+(\d+)\s+tests?", text)
            observed_count = int(count_match.group(1)) if count_match else None
            valid = result["returncode"] == 0 and not result["timed_out"] and observed_count == row["test_id_count"]
            receipt = {
                "module": row["module"],
                "path": row["path"],
                "definition_commit": anchor,
                "test_id_count": row["test_id_count"],
                "observed_test_count": observed_count,
                "returncode": result["returncode"],
                "timed_out": result["timed_out"],
                "duration_seconds": result["duration_seconds"],
                "output_sha256": result["output_sha256"],
                "raw_output_retained": False,
                "valid": valid,
            }
            module_results.append(receipt)
            if not valid:
                failures.append({"kind": "module_failure", **receipt})
        if group_index % 10 == 0 or group_index == len(groups):
            print(json.dumps({"progress": True, "worker": worker_id, "anchor_groups_done": group_index, "anchor_groups_total": len(groups), "modules_done": len(module_results), "failures": len(failures)}, sort_keys=True), flush=True)
    dirty = git_text("status", "--porcelain=v1", cwd=worker, check=False, timeout=900).splitlines()
    return {
        "worker": worker_id,
        "clone_valid": True,
        "anchor_groups": len(groups),
        "modules": module_results,
        "failures": failures,
        "final_dirty_path_count": len(dirty),
        "valid": not failures and not dirty,
    }


def partition_rows(expected_head: str, rows: list[dict[str, Any]], workers: int) -> list[list[tuple[str, list[dict[str, Any]]]]]:
    order = git_text("rev-list", "--reverse", "--topo-order", expected_head).splitlines()
    positions = {commit: index for index, commit in enumerate(order)}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["definition_commit"]].append(row)
    groups = sorted(grouped.items(), key=lambda item: positions[item[0]])
    partitions: list[list[tuple[str, list[dict[str, Any]]]]] = [[] for _ in range(workers)]
    loads = [0] * workers
    for anchor, group_rows in groups:
        target = min(range(workers), key=lambda index: loads[index])
        partitions[target].append((anchor, sorted(group_rows, key=lambda row: row["path"])))
        loads[target] += 10 + sum(row["test_id_count"] for row in group_rows)
    for partition in partitions:
        partition.sort(key=lambda item: positions[item[0]])
    return partitions


def write_receipt(path: Path, value: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    path.write_bytes(payload)
    return sha256(payload)


def canonical(expected_head: str, receipt_dir: Path, scratch_root: Path, workers: int, module_timeout: int) -> dict[str, Any]:
    receipt_dir.mkdir(parents=True, exist_ok=True)
    marker = receipt_dir / "canonical-invocation-marker.json"
    latch = receipt_dir / "canonical-success-latch.json"
    if marker.exists() or latch.exists():
        raise RuntimeError("canonical invocation or success latch already exists; replay refused")
    pre = preflight(expected_head, receipt_dir, scratch_root)
    if not pre["valid"] or not pre["json"]["valid"]:
        failure = {"schema": "ghc.family.v662-v3-2-remaster.canonical-failure.v1", "state": "PRE_FLIGHT_FAILED_ZERO_CREDIT", "preflight": pre, "valid": False, "recorded_at_utc": utc_now()}
        write_receipt(receipt_dir / "canonical-failure.json", failure)
        return failure
    write_receipt(marker, {"schema": "ghc.family.canonical-invocation-marker.v1", "expected_head": expected_head, "invoked_at_utc": utc_now(), "attempt": 1, "success_replay_forbidden": True})
    scratch_root.mkdir(parents=True, exist_ok=False)
    rows = pre["module_ledger"]
    partitions = partition_rows(expected_head, rows, workers)
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(worker_run, index + 1, partition, scratch_root, module_timeout) for index, partition in enumerate(partitions)]
        worker_results = [future.result() for future in futures]
    modules = [row for worker in worker_results for row in worker.get("modules", [])]
    failures = [row for worker in worker_results for row in worker.get("failures", [])]
    observed_tests = sum(row["observed_test_count"] or 0 for row in modules)
    component_checks = {
        "all_workers_valid": all(worker.get("valid") for worker in worker_results),
        "module_count_exact": len(modules) == pre["inventory"]["module_count"],
        "test_count_exact": observed_tests == pre["inventory"]["test_count"],
        "all_modules_valid": all(row["valid"] for row in modules),
        "failures_zero": not failures,
        "json_valid": pre["json"]["valid"],
        "owner_manifest_valid": pre["owner_manifest"]["valid"],
        "delta_manifest_valid": pre["delta_manifest"]["valid"],
        "remote_equality_valid": pre["remote_equality"]["valid"],
        "complete_current_inventory_mapped_once": pre["inventory"]["duplicate_ids"] == 0 and len(rows) == pre["inventory"]["module_count"],
    }
    valid = all(component_checks.values())
    receipt = {
        "schema": "ghc.family.v662-v3-2-remaster.exact-final-canonical-receipt.v1",
        "expected_head": expected_head,
        "invocation_count": 1,
        "successful_invocation_count": 1 if valid else 0,
        "post_success_replay": False,
        "recorded_at_utc": utc_now(),
        "duration_seconds": round(time.monotonic() - started, 3),
        "inventory": pre["inventory"],
        "definition_anchors": pre["definition_anchors"],
        "workers": workers,
        "module_timeout_seconds": module_timeout,
        "modules_run": len(modules),
        "tests_run": observed_tests,
        "module_failures": failures,
        "module_results": modules,
        "component_checks": component_checks,
        "passed": sum(component_checks.values()),
        "total": len(component_checks),
        "valid": valid,
        "raw_test_transcripts_retained": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "privacy_complete": False,
        "accessibility_complete": False,
        "exhaustive_security": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One same-owner complete current unittest inventory executed at immutable definition commits under shared local infrastructure; not external audit, independent reproduction, empirical confirmation, professional or production validation, complete privacy or accessibility assurance, exhaustive security, authority, personhood evidence, Theory-of-Everything proof, or Stage 20 authority.",
    }
    name = "canonical-success.json" if valid else "canonical-failure.json"
    receipt_sha = write_receipt(receipt_dir / name, receipt)
    if valid:
        write_receipt(latch, {"schema": "ghc.family.canonical-success-latch.v1", "expected_head": expected_head, "receipt_sha256": receipt_sha, "successful_invocations": 1, "replay_refused": True, "latched_at_utc": utc_now()})
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("preflight", "canonical"), required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-dir", type=Path, required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--module-timeout", type=int, default=300)
    args = parser.parse_args()
    if args.mode == "preflight":
        result = preflight(args.expected_head, args.receipt_dir.resolve(), args.scratch_root.resolve())
        args.receipt_dir.mkdir(parents=True, exist_ok=True)
        write_receipt(args.receipt_dir / "canonical-preflight.json", result)
    else:
        result = canonical(args.expected_head, args.receipt_dir.resolve(), args.scratch_root.resolve(), args.workers, args.module_timeout)
    print(json.dumps({"mode": args.mode, "valid": result["valid"], "tests": result.get("tests_run", result.get("inventory", {}).get("test_count")), "modules": result.get("modules_run", result.get("inventory", {}).get("module_count")), "passed": result.get("passed"), "total": result.get("total")}, sort_keys=True), flush=True)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
