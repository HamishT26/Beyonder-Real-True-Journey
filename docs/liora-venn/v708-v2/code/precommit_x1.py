#!/usr/bin/env python3
"""Run bounded owner-local X1 precommit checks and save a noncanonical receipt."""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = ROOT / "x1"
RECEIPT = X1 / "precommit-receipt.json"
BOUNDARY = (
    "Bounded same-owner synthetic precommit evidence only. This is not the exclusive "
    "exact-final canonical aggregate, a full-repository suite, independent reproduction, "
    "empirical confirmation, professional or authority evidence, or Stage 20 credit. "
    "NOT_READY_FOR_STAGE_20."
)


def run_owner_tests() -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(X1 / "tests"),
            "-p",
            "test_*.py",
            "-v",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
    return {
        "exit_code": result.returncode,
        "tests": int(match.group(1)) if match else 0,
        "ok_token": "OK" in combined,
    }


def text_files() -> list[Path]:
    allowed = {".json", ".md", ".py", ".txt", ".html", ".yaml", ".yml"}
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in allowed)


tests = run_owner_tests()
if tests != {"exit_code": 0, "tests": 25, "ok_token": True}:
    raise SystemExit(f"owner tests failed: {tests}")

json_paths = sorted(ROOT.rglob("*.json"))
for path in json_paths:
    json.loads(path.read_text(encoding="utf-8"))

python_paths = sorted(ROOT.rglob("*.py"))
for path in python_paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

documents = text_files()
word_counts: list[tuple[str, int]] = []
for path in documents:
    text = path.read_text(encoding="utf-8")
    word_counts.append((path.relative_to(ROOT).as_posix(), len(text.split())))
max_path, max_words = max(word_counts, key=lambda item: item[1])
if max_words > 100_000:
    raise SystemExit(f"word ceiling exceeded: {max_path} {max_words}")

# These five patterns are scanner definitions. Hits in this file are adjudicated as
# scanner-definition candidates; a hit in any other owner file is unresolved.
patterns = {
    "raw_task_or_thread_identifier": re.compile(
        r"(?i)\b(?:task|thread|conversation)[_-]?(?:id|uuid)\b\s*[:=]\s*[\"']?[0-9a-f-]{16,}"
    ),
    "private_route_scheme": re.compile(r"(?i)(?:chatgpt-conversation|plugin)://"),
    "credential_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']{4,}"
    ),
    "email_or_network_identifier": re.compile(
        r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:\\(?:Users|GHC-Archives|GHC-Family-Laboratory)\\"),
}

candidates: list[dict[str, str]] = []
unresolved: list[dict[str, str]] = []
for path in documents:
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT).as_posix()
    for class_name, pattern in patterns.items():
        if pattern.search(text):
            item = {"class": class_name, "path": relative}
            if path == Path(__file__).resolve():
                item["adjudication"] = "scanner_definition"
                candidates.append(item)
            else:
                item["adjudication"] = "unresolved"
                unresolved.append(item)
if unresolved:
    raise SystemExit(f"unresolved privacy candidates: {unresolved}")

receipt = {
    "schema": "liora.x1.precommit.v1",
    "canonical": False,
    "full_repository_suite": False,
    "owner_tests": tests,
    "strict_json_parses_before_receipt": len(json_paths),
    "python_ast_checks": len(python_paths),
    "text_files_scanned": len(documents),
    "privacy_classes": list(patterns),
    "privacy_candidates": candidates,
    "confirmed_privacy_hits": 0,
    "maximum_document": {"path": max_path, "words": max_words},
    "word_ceiling": 100_000,
    "x2_files_present": any((ROOT / "x2").rglob("*")) if (ROOT / "x2").exists() else False,
    "adviser_state": json.loads((X1 / "advisory-state.json").read_text(encoding="utf-8"))["state"],
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "boundary": BOUNDARY,
}
RECEIPT.write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)

# Require the newly written receipt to parse as part of the same bounded check.
all_json = sorted(ROOT.rglob("*.json"))
for path in all_json:
    json.loads(path.read_text(encoding="utf-8"))
receipt["strict_json_parses_including_receipt"] = len(all_json)
RECEIPT.write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
)
print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
