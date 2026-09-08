#!/usr/bin/env python3
"""Exclusive external exact-final canonical for Sylven Arc v688-v7."""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/sylven-arc/v688-v7"
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
X2 = "3c968db9391583a9e40f0eb8cc0c2f86d9997126"
FIRST_FINAL = "4e2421659eed8617cbd1fd45677b7248db2dfd11"
CORRECTION1 = "c0f79218f2d644592bd4eee0947058f0f3803b50"
BRANCH = "codex/GHC-Family/sylven-arc-v688-v7-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.PIPE).strip()


def write_external(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def batch_blobs(specs: list[str]) -> list[bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate(("\n".join(specs) + "\n").encode("utf-8"))
    if process.returncode:
        raise RuntimeError("cat_file_batch:" + error.decode("utf-8", errors="replace"))
    position = 0
    blobs = []
    for spec in specs:
        end = output.find(b"\n", position)
        if end < 0:
            raise RuntimeError("cat_file_header:" + spec)
        header = output[position:end].decode("ascii", errors="replace").split()
        position = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError("cat_file_shape:" + spec)
        size = int(header[2])
        blobs.append(output[position:position + size])
        position += size
        if output[position:position + 1] != b"\n":
            raise RuntimeError("cat_file_separator:" + spec)
        position += 1
    if position != len(output):
        raise RuntimeError("cat_file_trailing")
    return blobs


def strict(blob: bytes):
    return json.loads(blob.decode("utf-8"))


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n")


def equality(head: str) -> dict:
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", "refs/remotes/origin/" + BRANCH)
    live = git("ls-remote", "--exit-code", "origin", "refs/heads/" + BRANCH).split()[0]
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    return {"local": local, "upstream": upstream, "tracking": tracking, "fresh_live": live, "all_equal": len({local, upstream, tracking, live}) == 1 and local == head, "divergence": divergence, "clean": not bool(git("status", "--porcelain=v1"))}


def verify_manifest(head: str, path: str) -> dict:
    manifest = strict(batch_blobs([head + ":" + path])[0])
    specs = [head + ":" + item["path"] for item in manifest["entries"]]
    blobs = batch_blobs(specs) if specs else []
    failures = []
    for item, blob in zip(manifest["entries"], blobs):
        expected_bytes = item.get("bytes", item.get("bytes_normalized_lf"))
        expected_sha256 = item.get("sha256", item.get("sha256_normalized_lf"))
        if expected_bytes is None or expected_sha256 is None or len(blob) != expected_bytes or hashlib.sha256(blob).hexdigest() != expected_sha256:
            failures.append(item["path"])
    for excluded in manifest["self_exclusions"]:
        try:
            batch_blobs([head + ":" + excluded])
        except Exception:
            failures.append(excluded)
    return {"path": path, "entries": len(manifest["entries"]), "self_exclusions": len(manifest["self_exclusions"]), "failures": failures, "valid": not failures}


def scan_exact(head: str, paths: list[str]) -> dict:
    blobs = batch_blobs([head + ":" + path for path in paths])
    json_count = 0
    python_count = 0
    max_document = {"path": None, "words": 0}
    privacy_candidates = []
    security_findings = []
    definition_paths = {path for path in paths if path.endswith("_finalize.py") or path.endswith("_canonical.py") or path.startswith("tests/")}
    patterns = {
        "raw_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)") ,
        "credential_like": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_callable_identifier": re.compile(r"(?i)(?:threadId|providerTabId|sessionId)\s*[:=]"),
        "transcript_or_app_state": re.compile(r"(?i)(?:full raw transcript|private app state|session stream)"),
    }
    for path, blob in zip(paths, blobs):
        if b"\x00" in blob:
            continue
        text = blob.decode("utf-8")
        words = len(text.split())
        if words > max_document["words"]:
            max_document = {"path": path, "words": words}
        if words > 100000:
            raise RuntimeError("word_ceiling:" + path)
        for kind, pattern in patterns.items():
            if pattern.search(text):
                privacy_candidates.append({"path": path, "class": kind})
        if path.endswith(".json"):
            strict(blob)
            json_count += 1
        if path.endswith(".py"):
            tree = ast.parse(text, filename=path)
            python_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "kind": node.func.id, "line": node.lineno})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "kind": "shell_true", "line": node.lineno})
    confirmed = [item for item in privacy_candidates if item["path"] not in definition_paths and item["class"] != "transcript_or_app_state"]
    return {"owner_files": len(paths), "strict_json_count": json_count, "python_ast_count": python_count, "maximum_document": max_document, "privacy_candidates": len(privacy_candidates), "confirmed_privacy_hits": len(confirmed), "security_findings": security_findings, "valid": not confirmed and not security_findings}


def snapshot(head: str, bank: Path, skills: Path, runners: Path) -> dict:
    checks = {}
    checks["head_exact"] = git("rev-parse", "HEAD") == head
    checks["branch_exact"] = git("branch", "--show-current") == BRANCH
    eq = equality(head)
    checks["clean"] = eq["clean"]
    checks["fresh_four_way_equal"] = eq["all_equal"]
    checks["zero_divergence"] = eq["divergence"] == [0, 0]
    checks["phase_commit_count"] = int(git("rev-list", "--count", SOURCE + ".." + head)) == 5
    checks["zero_merges"] = int(git("rev-list", "--count", "--merges", SOURCE + ".." + head)) == 0
    checks["direct_parent_chain"] = (
        git("show", "-s", "--format=%P", X1) == SOURCE
        and git("show", "-s", "--format=%P", X2) == X1
        and git("show", "-s", "--format=%P", FIRST_FINAL) == X2
        and git("show", "-s", "--format=%P", CORRECTION1) == FIRST_FINAL
        and git("show", "-s", "--format=%P", head) == CORRECTION1
    )
    changes = [line for line in git("diff", "--name-status", SOURCE, head).splitlines() if line]
    correction_changes = [line for line in git("diff", "--name-status", CORRECTION1, head).splitlines() if line]
    modified = [line.split("\t")[-1] for line in correction_changes if line.startswith("M\t")]
    checks["additive_correction_scope"] = bool(correction_changes) and all(line.startswith(("A\t", "M\t")) for line in correction_changes) and modified == ["scripts/ghc_family_sylven_arc_v688_v7_canonical.py"]
    paths = [line.split("\t")[-1] for line in changes]
    checks["owner_file_ceiling"] = len(paths) < 2000
    checks["owner_path_scope"] = all(path.startswith(BASE + "/") or re.fullmatch(r"scripts/(?:build_)?ghc_family_sylven_arc_v688_v7_[a-z0-9_]+\.py", path) or re.fullmatch(r"scripts/ghc_family_chess_[a-z0-9_]+\.py", path) or re.fullmatch(r"tests/test_ghc_family_sylven_arc_v688_v7_[a-z0-9_]+\.py", path) for path in paths)
    scan = scan_exact(head, paths)
    checks["strict_json_ast_privacy_security"] = scan["valid"] and scan["strict_json_count"] > 0 and scan["python_ast_count"] > 0
    manifests = [
        verify_manifest(X1, BASE + "/x1/x1-manifest.json"),
        verify_manifest(X2, BASE + "/x2/evidence-manifest.json"),
        verify_manifest(FIRST_FINAL, BASE + "/validation/final-delta-manifest.json"),
        verify_manifest(FIRST_FINAL, BASE + "/validation/final-owner-manifest.json"),
        verify_manifest(CORRECTION1, BASE + "/correction1/validation/correction-delta-manifest.json"),
        verify_manifest(CORRECTION1, BASE + "/correction1/validation/corrected-owner-manifest.json"),
        verify_manifest(head, BASE + "/correction2/validation/correction-delta-manifest.json"),
        verify_manifest(head, BASE + "/correction2/validation/corrected-owner-manifest.json"),
    ]
    checks["all_manifests"] = all(item["valid"] for item in manifests)
    owner_manifest = strict(batch_blobs([head + ":" + BASE + "/correction2/validation/corrected-owner-manifest.json"])[0])
    checks["final_owner_manifest_complete"] = {item["path"] for item in owner_manifest["entries"]} | set(owner_manifest["self_exclusions"]) == set(paths)
    seal = strict(batch_blobs([head + ":" + BASE + "/correction2/content-seal.json"])[0])
    seal_blobs = batch_blobs([head + ":" + item["path"] for item in seal["targets"]])
    checks["content_seal"] = all(len(blob) == item["bytes"] and hashlib.sha256(blob).hexdigest() == item["sha256"] for item, blob in zip(seal["targets"], seal_blobs))
    truth = strict(batch_blobs([head + ":" + BASE + "/correction2/phase-truth-overlay.json"])[0])
    checks["truth_counts"] = truth["effective_counts"] == {"proposals": 16830, "negatives": 85422, "methods": 94122, "failed_witnesses": 56300, "passing_witnesses": 86185, "open_gaps": 765, "exact_gates": 785}
    checks["outcomes_exact"] = truth["outcomes"] == {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10}
    checks["prepared_not_sent"] = truth["prepared_baton_state"] == "PREPARED_NOT_SENT" and truth["successor_contacts"] == 0 and truth["new_tasks_created"] == 0
    checks["not_ready_for_stage20"] = truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    baton_index = strict(batch_blobs([head + ":" + BASE + "/final/baton-index.json"])[0])
    baton_blob = batch_blobs([head + ":" + baton_index["path"]])[0]
    baton_text = baton_blob.decode("utf-8")
    checks["baton_budget_modules_hash"] = 10000 <= len(baton_text.split()) <= 100000 and len(re.findall(r"^## Module \d\d", baton_text, re.MULTILINE)) == 13 and hashlib.sha256(baton_blob).hexdigest() == baton_index["sha256"]
    route = strict(batch_blobs([head + ":" + BASE + "/final/terminal-route-checklist.json"])[0])
    checks["future_seat_self_choice"] = route["prospective_target"] == "future seat 14" and route["identity_assignment"] == "self_chosen_after_creation" and route["creation_if_absent"]["maximum"] == 1 and route["sends_or_creations_already_made"] == 0
    supplement = strict(batch_blobs([head + ":" + BASE + "/correction2/baton-supplement-index.json"])[0])
    supplement_blob = batch_blobs([head + ":" + supplement["path"]])[0]
    checks["correction_baton_supplement"] = hashlib.sha256(supplement_blob).hexdigest() == supplement["sha256"] and supplement["delivery_state"] == "PREPARED_NOT_SENT"
    promotion = strict(batch_blobs([head + ":" + BASE + "/x2/promotion-receipt.json"])[0])
    source_specs = [head + ":" + item["source"] for item in promotion["parity"]]
    source_blobs = batch_blobs(source_specs)
    promotion_failures = []
    for item, source_blob in zip(promotion["parity"], source_blobs):
        target = skills / item["target_name"] if item["target_class"] == "global Codex skill root" else runners / item["target_name"]
        if not target.is_file():
            promotion_failures.append(item["target_name"])
            continue
        target_blob = target.read_bytes()
        if hashlib.sha256(target_blob).hexdigest() != item["sha256"] or normalized(target_blob) != source_blob:
            promotion_failures.append(item["target_name"])
    checks["promotion_parity"] = not promotion_failures and promotion["overwrites"] == 0 and promotion["skill_count"] == 10 and promotion["runner_interface_count"] == 5
    plan = strict(batch_blobs([head + ":" + BASE + "/x1/tool-package-plan.json"])[0])
    artifact_failures = []
    for item in plan["packages"]:
        artifact = bank / "artifacts" / item["artifact"]
        if not artifact.is_file() or len(artifact.read_bytes()) != item["bytes"] or hashlib.sha256(artifact.read_bytes()).hexdigest() != item["sha256"]:
            artifact_failures.append(item["name"])
    checks["package_artifact_fixity"] = not artifact_failures
    package = strict(batch_blobs([head + ":" + BASE + "/x2/package-transaction.json"])[0])
    checks["package_contract"] = package["state"] == "COMPLETE" and package["direct_count"] == 3 and not package["global_python_mutated"]
    method = strict(batch_blobs([head + ":" + BASE + "/correction2/post-final-method-flow-overlay.json"])[0])
    checks["method_flow_nonerasure"] = method["combined_counts"] == {"methods": 60, "witnesses": 623, "failed_witnesses": 548, "passing_witnesses": 75, "state_events": 60, "recommendations": 60} and method["failed_witnesses_erased"] == 0
    policy = strict(batch_blobs([head + ":" + BASE + "/correction2/canonical-policy-overlay.json"])[0])
    checks["canonical_policy"] = not policy["post_success_replay"] and not policy["full_repository_suite"] and [item["expected_tests"] for item in policy["test_modules"]] == [12, 24, 20, 10, 6]
    return {"checks": checks, "equality": eq, "paths": paths, "scan": scan, "manifests": manifests, "promotion_failures": promotion_failures, "artifact_failures": artifact_failures, "policy": policy, "truth": truth}


def materialize(commit: str, paths: list[str], target: Path) -> int:
    target.mkdir(parents=True, exist_ok=False)
    blobs = batch_blobs([commit + ":" + path for path in paths])
    for path, blob in zip(paths, blobs):
        destination = target / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(blob)
    return len(paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head", required=True)
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--skills", type=Path, required=True)
    parser.add_argument("--runners", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    if re.fullmatch(r"[0-9a-f]{40}", args.head) is None:
        raise SystemExit("exact_head_required")
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:" or bank.is_relative_to(ROOT):
        raise SystemExit("external_D_first_bank_required")
    canonical_dir = bank / "canonical"
    marker = canonical_dir / "invocation.json"
    receipt = canonical_dir / "exact-final-owner-scoped-canonical.json"
    preflight = canonical_dir / "preflight.json"
    if args.preflight:
        if marker.exists() or receipt.exists() or preflight.exists():
            raise SystemExit("canonical_preflight_replay_refused")
        state = snapshot(args.head, bank, args.skills.resolve(), args.runners.resolve())
        result = {"schema": "ghc.family.exact-final-canonical-preflight.v1", "owner": "Sylven Arc", "phase": "v688-v7", "head": args.head, "checks": state["checks"], "check_count": len(state["checks"]), "passed_check_count": sum(state["checks"].values()), "valid": all(state["checks"].values()), "canonical_invoked": False, "owner_files": len(state["paths"]), "scan": state["scan"], "manifests": state["manifests"]}
        write_external(preflight, result)
        print(json.dumps({"preflight": True, "valid": result["valid"], "checks": result["check_count"], "failed": [key for key, value in result["checks"].items() if not value]}, sort_keys=True))
        return 0 if result["valid"] else 1
    if marker.exists() or receipt.exists():
        raise SystemExit("canonical_replay_refused")
    saved_preflight = strict(preflight.read_bytes())
    if saved_preflight["head"] != args.head or saved_preflight["valid"] is not True:
        raise SystemExit("matching_valid_preflight_required")
    write_external(marker, {"schema": "ghc.family.canonical-invocation.v1", "owner": "Sylven Arc", "phase": "v688-v7", "head": args.head, "invocation_count": 1, "replay_count": 0, "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat()})
    checks = {}
    state = {}
    tests = []
    error = None
    try:
        state = snapshot(args.head, bank, args.skills.resolve(), args.runners.resolve())
        checks.update(state["checks"])
        if not all(checks.values()):
            raise RuntimeError("exact_final_preconditions_changed")
        for entry in state["policy"]["test_modules"]:
            commit = args.head if entry["definition"] == "exact_final" else entry["definition"]
            manifest = strict(batch_blobs([commit + ":" + entry["manifest"]])[0])
            paths = [item["path"] for item in manifest["entries"]] + manifest["self_exclusions"]
            view = canonical_dir / ("definition-" + entry["stage"])
            count_files = materialize(commit, paths, view)
            process = subprocess.run([sys.executable, "-B", "-X", "utf8", str(view / entry["module"])], cwd=view, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            (canonical_dir / (entry["stage"] + "-tests.stdout.txt")).write_bytes(process.stdout)
            (canonical_dir / (entry["stage"] + "-tests.stderr.txt")).write_bytes(process.stderr)
            match = re.search(r"Ran (\d+) tests?", process.stderr.decode("utf-8", errors="replace"))
            count = int(match.group(1)) if match else 0
            passed = process.returncode == 0 and count == entry["expected_tests"]
            tests.append({"stage": entry["stage"], "definition": commit, "module": entry["module"], "expected_tests": entry["expected_tests"], "tests": count, "returncode": process.returncode, "passed": passed, "materialized_files": count_files, "definition_sha256": hashlib.sha256((view / entry["module"]).read_bytes()).hexdigest()})
            print(json.dumps({"canonical_stage": entry["stage"], "tests": count, "passed": passed}), flush=True)
        checks["all_lifecycle_tests"] = len(tests) == 3 and all(item["passed"] for item in tests)
        after = equality(args.head)
        checks["head_stable_after"] = git("rev-parse", "HEAD") == args.head
        checks["clean_after"] = after["clean"]
        checks["fresh_four_way_equal_after"] = after["all_equal"]
        checks["zero_divergence_after"] = after["divergence"] == [0, 0]
    except Exception as exc:
        error = {"class": type(exc).__name__, "scope": "exact owner canonical; detailed private diagnostics retained externally"}
        checks["canonical_exception_absent"] = False
        after = None
    valid = all(checks.values()) and len(tests) == 3 and all(item["passed"] for item in tests)
    result = {
        "schema": "ghc.family.exact-corrected-final-owner-scoped-canonical.sylven-arc.v688-v7",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "head": args.head,
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": X2,
        "first_final": FIRST_FINAL,
        "correction1": CORRECTION1,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "canonical_invocation_count": 1,
        "canonical_success_count": int(valid),
        "canonical_replay_count": 0,
        "checks": checks,
        "check_count": len(checks),
        "passed_check_count": sum(checks.values()),
        "test_modules": tests,
        "test_count": sum(item["tests"] for item in tests),
        "owner_files": len(state.get("paths", [])),
        "scan": state.get("scan"),
        "manifests": state.get("manifests"),
        "equality_after": after,
        "error": error,
        "completed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "same_owner_shared_infrastructure": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "successor_contacts": 0,
        "prepared_baton_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_external(receipt, result)
    print(json.dumps({"status": result["status"], "checks": result["check_count"], "passed_checks": result["passed_check_count"], "tests": result["test_count"], "owner_files": result["owner_files"], "replays": 0}, sort_keys=True), flush=True)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
