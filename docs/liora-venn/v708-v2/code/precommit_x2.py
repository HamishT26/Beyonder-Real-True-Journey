#!/usr/bin/env python3
"""Run bounded owner-local X2 precommit checks and save a noncanonical receipt."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "x1"
X2 = ROOT / "x2"
RECEIPT = X2 / "precommit-receipt.json"
X1_HEAD = "efd43f08eb4bfb66830c5c4da1274c3c643d5d7b"
BOUNDARY = (
    "Bounded same-owner synthetic X2 precommit evidence only. This is not the exclusive "
    "exact-final canonical aggregate, a full-repository suite, independent reproduction, "
    "empirical confirmation, professional or authority evidence, or Stage 20 credit. "
    "NOT_READY_FOR_STAGE_20."
)


def run_owner_tests() -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(X2 / "tests"), "-p", "test_*.py", "-v"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
    return {"exit_code": result.returncode, "tests": int(match.group(1)) if match else 0, "ok_token": "OK" in combined}


tests = run_owner_tests()
if tests != {"exit_code": 0, "tests": 60, "ok_token": True}:
    raise SystemExit(f"owner tests failed: {tests}")

# ROOT is docs/liora-venn/v708-v2, so parents[2] is the repository root.
repo = ROOT.parents[2]
x1_diff = subprocess.run(
    ["git", "diff", "--name-only", X1_HEAD, "--", "docs/liora-venn/v708-v2/x1"],
    cwd=repo,
    text=True,
    capture_output=True,
    encoding="utf-8",
    check=False,
)
if x1_diff.returncode or x1_diff.stdout.strip():
    raise SystemExit(f"immutable X1 changed: {x1_diff.stdout} {x1_diff.stderr}")

json_paths = sorted(ROOT.rglob("*.json"))
for path in json_paths:
    json.loads(path.read_text(encoding="utf-8"))

python_paths = sorted(ROOT.rglob("*.py"))
for path in python_paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

allowed = {".json", ".md", ".py", ".txt", ".html", ".yaml", ".yml"}
documents = sorted(path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in allowed)
word_counts = [(path.relative_to(ROOT).as_posix(), len(path.read_text(encoding="utf-8").split())) for path in documents]
max_path, max_words = max(word_counts, key=lambda item: item[1])
if max_words > 100_000:
    raise SystemExit(f"word ceiling exceeded: {max_path} {max_words}")

patterns = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)\b(?:task|thread|conversation)[_-]?(?:id|uuid)\b\s*[:=]\s*[\"']?[0-9a-f-]{16,}"),
    "private_route_scheme": re.compile(r"(?i)(?:chatgpt-conversation|plugin)://"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']{4,}"),
    "email_or_network_identifier": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|GHC-Archives|GHC-Family-Laboratory)[\\/]"),
}
candidates = []
unresolved = []
for path in documents:
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT).as_posix()
    for class_name, pattern in patterns.items():
        if pattern.search(text):
            record = {"class": class_name, "path": relative}
            if path == Path(__file__).resolve():
                record["adjudication"] = "scanner_definition"
                candidates.append(record)
            elif class_name == "private_absolute_path" and relative in {
                "code/build_x1.py",
                "code/build_x2.py",
            }:
                record["adjudication"] = "synthetic_manual_hook_cwd_fixture_no_user_identifier"
                candidates.append(record)
            else:
                record["adjudication"] = "unresolved"
                unresolved.append(record)
if unresolved:
    raise SystemExit(f"unresolved privacy candidates: {unresolved}")

outcomes = json.loads((X2 / "outcome-ledger.json").read_text(encoding="utf-8"))["counts"]
if outcomes != {"completed": 16, "represented": 1, "open_gap": 2, "exact_gate": 1}:
    raise SystemExit(f"unexpected outcomes: {outcomes}")
flow = json.loads((X2 / "method-flow.json").read_text(encoding="utf-8"))
if flow["counts"]["states"]["candidate"] != 0:
    raise SystemExit("candidate Method Flow methods remain")
if flow.get("witnesses_embedded") is not False or not flow.get("witness_shards"):
    raise SystemExit("X2 Method Flow witness shards missing")
sharded_witnesses = []
for record in sorted(flow["witness_shards"], key=lambda item: item["shard"]):
    path = ROOT / record["path"]
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != record["sha256"]:
        raise SystemExit(f"Method Flow shard hash mismatch: {record['path']}")
    shard = json.loads(raw)
    if shard["count"] != record["count"] or len(shard["witnesses"]) != record["count"]:
        raise SystemExit(f"Method Flow shard count mismatch: {record['path']}")
    sharded_witnesses.extend(shard["witnesses"])
shard_ids = [item["witness_id"] for item in sharded_witnesses]
if len(shard_ids) != len(set(shard_ids)) or len(shard_ids) != flow["counts"]["witnesses"]:
    raise SystemExit("Method Flow witness shard identity/count mismatch")
if {
    "pass": sum(item["result"] == "pass" for item in sharded_witnesses),
    "fail": sum(item["result"] == "fail" for item in sharded_witnesses),
} != flow["counts"]["witness_results"]:
    raise SystemExit("Method Flow witness result totals mismatch")
known_ids = set(shard_ids)
for item in flow["methods"]:
    if not set(item["validation_witness_ids"]) <= known_ids:
        raise SystemExit(f"Method Flow backlink mismatch: {item['method_id']}")
lab = json.loads((X2 / "laboratory" / "receipt.json").read_text(encoding="utf-8"))
if (lab["model_invocations"], lab["successes"], lab["replays"]) != (15, 15, 0):
    raise SystemExit("unexpected X2 model receipt")
teren = json.loads((X2 / "results" / "teren-five-task-execution.json").read_text(encoding="utf-8"))
if teren["task_count"] != 5 or any(not item["mutant_rejected"] for item in teren["tasks"]):
    raise SystemExit("unexpected Teren five-task receipt")

receipt = {
    "schema": "liora.x2.precommit.v1",
    "canonical": False,
    "full_repository_suite": False,
    "immutable_x1_head": X1_HEAD,
    "immutable_x1_diff_paths": 0,
    "owner_tests": tests,
    "strict_json_parses_before_receipt": len(json_paths),
    "python_ast_checks": len(python_paths),
    "text_files_scanned": len(documents),
    "privacy_classes": list(patterns),
    "privacy_candidates": candidates,
    "confirmed_privacy_hits": 0,
    "maximum_document": {"path": max_path, "words": max_words},
    "word_ceiling": 100_000,
    "laboratory_models": 15,
    "laboratory_replays": 0,
    "teren_advisory_tasks": 5,
    "teren_mutants_rejected": 5,
    "method_flow": flow["counts"],
    "method_flow_witness_shards": len(flow["witness_shards"]),
    "method_flow_shard_ids_unique": True,
    "method_flow_backlinks_complete": True,
    "outcomes": outcomes,
    "adviser_state": json.loads((X2 / "advisory-state.json").read_text(encoding="utf-8"))["state"],
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "boundary": BOUNDARY,
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
all_json = sorted(ROOT.rglob("*.json"))
for path in all_json:
    json.loads(path.read_text(encoding="utf-8"))
receipt["strict_json_parses_including_receipt"] = len(all_json)
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
