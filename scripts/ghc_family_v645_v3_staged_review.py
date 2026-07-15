#!/usr/bin/env python3
"""Review every substantive staged v645-v3 blob before an Eiren commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


PHASE_ROOT = "docs/eiren-kestrel/v645-v3/"
X1_COMMIT = "abb576e6de2666dd2dc792f6dd189722424ff0c2"
X1_SET = PHASE_ROOT + "validation/x1-exact-file-set.json"
X1_MUTABLE = {
    PHASE_ROOT + "method-flow/method-flow-state.json",
    "tests/test_ghc_family_v645_v3_x1.py",
}
EXACT_TOOLS = {
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
    "tests/test_ghc_family_v645_v3.py",
    "tests/test_ghc_family_v645_v3_x1.py",
}


def git(repo: Path, *args: str, check: bool = True) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=check).stdout


def load_blob(repo: Path, spec: str) -> Any:
    return json.loads(git(repo, "show", spec).decode("utf-8"))


def run(repo: Path, self_path: str) -> dict[str, Any]:
    repo = repo.resolve()
    names = [value.decode("utf-8") for value in git(repo, "diff", "--cached", "--name-only", "-z").split(b"\0") if value]
    names = [name for name in names if name != self_path]
    statuses: dict[str, str] = {}
    for line in git(repo, "diff", "--cached", "--name-status").decode("utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            statuses[parts[-1]] = parts[0]

    x1_files = set(load_blob(repo, f"{X1_COMMIT}:{X1_SET}")["files"])
    frozen = x1_files - X1_MUTABLE
    frozen_diff = [value.decode("utf-8") for value in git(repo, "diff", "--name-only", "-z", X1_COMMIT, "--", *sorted(frozen)).split(b"\0") if value]
    delegation = "codex" + "_delegation"
    route = "source" + "_thread_id"
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "delegation_markup": re.compile(rf"<(?:{delegation}|{route})>", re.I),
        "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_uri": re.compile(r"\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
    }
    rows: list[dict[str, Any]] = []
    json_issues: list[str] = []
    privacy_hits: list[dict[str, str]] = []
    for name in names:
        blob = git(repo, "show", f":{name}")
        text = blob.decode("utf-8", errors="replace")
        if name.endswith(".json"):
            try:
                json.loads(text)
            except Exception as exc:  # pragma: no cover - diagnostic receipt
                json_issues.append(f"{name}:{type(exc).__name__}")
        for label, pattern in patterns.items():
            if pattern.search(text):
                privacy_hits.append({"path": name, "pattern_class": label})
        rows.append({
            "path": name,
            "status": statuses.get(name),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "bytes": len(blob),
            "allowed_scope": name.startswith(PHASE_ROOT) or name in EXACT_TOOLS,
            "x1_frozen": name in frozen,
            "x1_append_only_or_test_compatibility": name in X1_MUTABLE,
        })
    diff = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--check"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    issues: list[str] = []
    if not rows:
        issues.append("no substantive staged files")
    if any(not row["allowed_scope"] for row in rows):
        issues.append("out-of-scope staged path")
    if any("D" in (row["status"] or "") for row in rows):
        issues.append("staged deletion")
    if any(row["x1_frozen"] for row in rows) or frozen_diff:
        issues.append("frozen x1 content changed")
    if json_issues:
        issues.append("staged JSON parse issue")
    if privacy_hits:
        issues.append("staged privacy scan hit")
    if diff.returncode:
        issues.append("git diff --cached --check failed")
    return {
        "schema": "ghc.family.v645-v3.staged-review.v1",
        "self_receipt_excluded": self_path,
        "reviewed_file_count": len(rows),
        "expected_staged_file_count_with_receipt": len(rows) + 1,
        "files": rows,
        "frozen_x1_diff_paths": frozen_diff,
        "json_files_parsed": sum(row["path"].endswith(".json") for row in rows),
        "json_issues": json_issues,
        "privacy": {"pattern_classes": sorted(patterns), "hits": privacy_hits, "valid": not privacy_hits},
        "diff_check_returncode": diff.returncode,
        "diff_check_output": diff.stdout,
        "issues": issues,
        "valid": not issues,
        "boundary": "Exact staged-blob review is bounded change-control evidence, not semantic, scientific, legal, cultural, accessibility, security, or authority review.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    self_path = output.resolve().relative_to(repo).as_posix()
    result = run(repo, self_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("valid", "reviewed_file_count", "expected_staged_file_count_with_receipt", "issues")}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
