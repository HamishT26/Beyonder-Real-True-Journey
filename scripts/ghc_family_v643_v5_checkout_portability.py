#!/usr/bin/env python3
"""Materialize two exact historical JSON files for portable legacy tests.

The operation is semantic preserving: each target's LF-normalized SHA-256 must
match its frozen Git content before any bytes are written.  Only line endings
change, and Git-normalized content remains identical.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


TARGETS = [
    {
        "repo_path": "docs/orin-thale/v642-v6/provenance/frozen-chain-proposal-index.json",
        "normalized_sha256": "e5fa094302d36e4eea569a5ff2cebce212018afe4d17745d834e8e6818d8d6e5",
        "materialization": "lf",
        "required_raw_sha256": "e5fa094302d36e4eea569a5ff2cebce212018afe4d17745d834e8e6818d8d6e5",
    },
    {
        "repo_path": "docs/tamar-vey/v642-v7/provenance/frozen-chain-proposal-index.json",
        "normalized_sha256": "59763e85c7feb522f53a27414d6f736e3ea34185acbb7e3063468679a14d39c5",
        "materialization": "crlf",
        "required_raw_sha256": "cbab08554c0ddbafc4f77e9fbd9d89760c8a300437bd6427ef56e606604e4102",
    },
]


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def lf_normalized(payload: bytes) -> bytes:
    return payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def materialize_payload(payload: bytes, normalized_sha256: str, style: str) -> bytes:
    normalized = lf_normalized(payload)
    if sha256(normalized) != normalized_sha256:
        raise ValueError("normalized semantic hash mismatch")
    if style == "lf":
        return normalized
    if style == "crlf":
        return normalized.replace(b"\n", b"\r\n")
    raise ValueError(f"unsupported line-ending style: {style}")


def run(repo: Path, apply: bool) -> dict:
    rows = []
    for target in TARGETS:
        path = repo / target["repo_path"]
        before = path.read_bytes()
        after = materialize_payload(before, target["normalized_sha256"], target["materialization"])
        if sha256(after) != target["required_raw_sha256"]:
            raise ValueError(f"required raw hash mismatch: {target['repo_path']}")
        if apply and before != after:
            path.write_bytes(after)
        rows.append({
            "repo_path": target["repo_path"],
            "materialization": target["materialization"],
            "before_raw_sha256": sha256(before),
            "after_raw_sha256": sha256(after),
            "normalized_sha256": sha256(lf_normalized(after)),
            "semantic_hash_matched": True,
            "bytes_changed": before != after,
            "applied": apply,
        })
    return {
        "schema": "ghc.family.v643-v5.checkout-portability.v1",
        "phase": "v643-gmut-thos-v5-x1-x2",
        "target_count": len(rows),
        "apply_requested": apply,
        "rows": rows,
        "semantic_mismatch_count": 0,
        "shared_validator_changed": False,
        "git_normalized_content_changed": False,
        "valid": all(row["semantic_hash_matched"] for row in rows),
        "boundary": "This materializes exact line endings in an owned checkout after semantic-hash verification. It does not rewrite repository history or relax arbitrary hashes.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = run(args.repo.resolve(), args.apply)
    rendered = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else args.repo / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
