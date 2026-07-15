#!/usr/bin/env python3
"""Build an exact staged-blob or committed-blob v645-v3 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOTS = [
    "docs/eiren-kestrel/v645-v3",
    "scripts/build_ghc_family_v645_v3_preregistration.py",
    "scripts/ghc_family_v645_v3_definitions.py",
    "scripts/ghc_family_v645_v3_x1_review.py",
    "scripts/build_ghc_family_v645_v3_evidence.py",
    "scripts/ghc_family_anytime_evidence_board.py",
    "scripts/ghc_family_deferred_issuance_state_machine.py",
    "scripts/ghc_family_eft_quotient_validator.py",
    "scripts/ghc_family_git_acceleration_lab.py",
    "scripts/ghc_family_sandbox_blueprint_linter.py",
    "scripts/ghc_family_v645_v3_portfolio_validator.py",
    "scripts/ghc_family_v645_v3_staged_review.py",
    "scripts/ghc_family_v645_v3_manifest.py",
    "scripts/ghc_family_v645_v3_validator.py",
    "tests/test_ghc_family_v645_v3_x1.py",
    "tests/test_ghc_family_v645_v3.py",
]


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit")
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    output_rel = output.resolve().relative_to(repo).as_posix()
    excluded = set(args.exclude) | {output_rel}
    if args.commit:
        raw = git(repo, "ls-tree", "-r", "--name-only", "-z", args.commit, "--", *ROOTS)
    else:
        raw = git(repo, "ls-files", "-z", "--", *ROOTS)
    paths = sorted(value.decode("utf-8") for value in raw.split(b"\0") if value and value.decode("utf-8") not in excluded)
    entries = []
    for path in paths:
        blob = git(repo, "show", f"{args.commit}:{path}" if args.commit else f":{path}")
        entries.append({"path": path, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})
    payload = {
        "schema": "ghc.family.v645-v3.exact-blob-manifest.v1",
        "target": args.commit or "INDEX",
        "target_kind": "commit" if args.commit else "staged_index",
        "hash_domain": "exact Git blob bytes",
        "roots": ROOTS,
        "excluded_receipts": sorted(excluded),
        "entry_count": len(entries),
        "entries": entries,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False,
        "boundary": "The explicit self-referential exclusions permit exact change detection; this is not a signature or independent reproduction.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"target": payload["target"], "entries": payload["entry_count"], "output": output_rel}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
