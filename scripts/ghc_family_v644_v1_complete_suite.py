#!/usr/bin/env python3
"""Run the complete repository suite with exact checkout-byte restoration.

The inherited portability helper materializes two historical JSON fixtures
using their frozen LF-normalized hashes. This wrapper snapshots the original
raw bytes, applies that bounded materialization, runs unittest discovery, and
restores the original bytes in a ``finally`` block. A passing suite is counted
only when every original raw byte sequence is restored exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_portability_helper(repo: Path):
    path = repo / "scripts/ghc_family_v643_v5_checkout_portability.py"
    spec = importlib.util.spec_from_file_location("ghc_family_checkout_portability_runtime", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run(repo: Path) -> tuple[dict[str, Any], str]:
    repo = repo.resolve()
    helper = load_portability_helper(repo)
    targets = [repo / row["repo_path"] for row in helper.TARGETS]
    before = {path: path.read_bytes() for path in targets}
    suite_output = ""
    suite_returncode = 1
    adapter_receipt: dict[str, Any] = {}
    try:
        adapter_receipt = helper.run(repo, apply=True)
        suite = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        suite_output = suite.stdout
        suite_returncode = suite.returncode
    finally:
        for path, payload in before.items():
            path.write_bytes(payload)

    restoration = [
        {
            "repo_path": path.relative_to(repo).as_posix(),
            "before_raw_sha256": sha256(payload),
            "restored_raw_sha256": sha256(path.read_bytes()),
            "restored_exactly": path.read_bytes() == payload,
        }
        for path, payload in before.items()
    ]
    match = re.search(r"Ran\s+(\d+)\s+tests?", suite_output)
    test_count = int(match.group(1)) if match else 0
    passed = suite_returncode == 0 and all(row["restored_exactly"] for row in restoration)
    receipt = {
        "schema": "ghc.family.v644-v1.complete-suite.v1",
        "phase": "v644-gmut-thos-v1-x1-x2",
        "adapter": "scripts/ghc_family_v643_v5_checkout_portability.py",
        "adapter_valid": adapter_receipt.get("valid") is True,
        "semantic_mismatch_count": adapter_receipt.get("semantic_mismatch_count"),
        "test_count": test_count,
        "tests_passed": test_count if suite_returncode == 0 else None,
        "suite_returncode": suite_returncode,
        "raw_byte_restoration": restoration,
        "all_original_bytes_restored": all(row["restored_exactly"] for row in restoration),
        "valid": passed,
        "boundary": (
            "The adapter changes only bounded checkout materialization after frozen semantic-hash checks and "
            "restores exact original bytes. It does not relax arbitrary hashes or rewrite repository history."
        ),
    }
    return receipt, suite_output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt, suite_output = run(repo)
    if suite_output:
        print(suite_output, end="" if suite_output.endswith("\n") else "\n")
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else repo / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({key: receipt[key] for key in ("valid", "test_count", "suite_returncode", "all_original_bytes_restored")}, ensure_ascii=False))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
