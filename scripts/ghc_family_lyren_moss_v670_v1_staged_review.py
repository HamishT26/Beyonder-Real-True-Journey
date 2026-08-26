"""Create exact staged-review receipts for Lyren Moss v670-v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, check=False, capture_output=True)


def staged_blob(path: str) -> bytes:
    proc = run("git", "cat-file", "blob", f":{path}")
    if proc.returncode:
        raise RuntimeError(f"missing staged blob: {path}")
    return proc.stdout


def allowed(path: str, stage: str) -> bool:
    common = (
        path.startswith(("docs/lyren-moss/v670-v1/", "scripts/ghc_family_grain_milling_", "scripts/build_ghc_family_lyren_moss_v670_v1_", "scripts/validate_ghc_family_lyren_moss_v670_v1_", "tests/test_ghc_family_lyren_moss_v670_v1_")) or path == "ghc-family-index/references/v670-v1-lyren-moss.md" or path == "scripts/ghc_family_lyren_moss_v670_v1_staged_review.py"
    )
    if not common:
        return False
    if stage == "x1":
        return not any(
            token in path
            for token in (
                "/x2/",
                "/closeout/",
                "/final/",
                "/handoffs/",
                "_x2.py",
                "_final.py",
            )
        )
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["x1", "evidence", "final"], required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    staged_names = run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT").stdout.decode().splitlines()
    disallowed = [path for path in staged_names if not allowed(path, args.stage)]
    diff_check = run("git", "diff", "--cached", "--check")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    mismatches = []
    for entry in manifest["entries"]:
        data = staged_blob(entry["path"])
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != entry["bytes"] or digest != entry["sha256"]:
            mismatches.append(entry["path"])

    receipt = {
        "schema": "ghc.family.staged-review.v3",
        "owner": "Lyren Moss",
        "phase": "v670-v1",
        "stage": args.stage,
        "staged_entries": len(staged_names),
        "disallowed_paths": disallowed,
        "diff_check_returncode": diff_check.returncode,
        "diff_check_output": (diff_check.stdout + diff_check.stderr).decode(errors="replace"),
        "manifest_entries": manifest["entry_count"],
        "manifest_mismatches": mismatches,
        "passed": not disallowed and diff_check.returncode == 0 and not mismatches,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"stage": args.stage, "passed": receipt["passed"], "staged": len(staged_names), "manifest": manifest["entry_count"]}, sort_keys=True))
    raise SystemExit(0 if receipt["passed"] else 1)


if __name__ == "__main__":
    main()
