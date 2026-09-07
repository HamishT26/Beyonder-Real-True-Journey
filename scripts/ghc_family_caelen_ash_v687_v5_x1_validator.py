#!/usr/bin/env python3
"""Build and review Caelen Ash v687-v5 planning-only validation evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-ash" / "v687-v5"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE = "5a71b1b7866171aa4ee16664ab7fc434bb6f5593"
BRANCH = "codex/GHC-Family/caelen-ash-v687-v5-full-tools"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True
    )


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n"
    )


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(path: Path) -> str:
    return hashlib.sha256(normalized(path)).hexdigest()


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def x1_files() -> list[Path]:
    paths = [path for path in X1.rglob("*") if path.is_file()]
    paths.extend(
        ROOT / rel for rel in [
            "scripts/build_ghc_family_caelen_ash_v687_v5_x1.py",
            "scripts/ghc_family_caelen_ash_v687_v5_plan_cases.py",
            "scripts/ghc_family_caelen_ash_v687_v5_x1_validator.py",
            "tests/test_ghc_family_caelen_ash_v687_v5_x1.py",
        ]
    )
    paths.extend(path for path in VALIDATION.glob("x1-*.json") if path.is_file())
    return sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())


def privacy(paths: list[Path]) -> dict:
    patterns = {
        "raw_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    definition = "scripts/ghc_family_caelen_ash_v687_v5_x1_validator.py"
    candidates = []
    confirmed = []
    scanned = 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".txt", ".yaml", ".yml"}:
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for kind, pattern in patterns.items():
            for match in pattern.finditer(text):
                item = {
                    "path": rel,
                    "line": text.count("\n", 0, match.start()) + 1,
                    "kind": kind,
                    "disposition": "scanner_definition_not_payload" if rel == definition else "confirmed_payload_hit",
                }
                candidates.append(item)
                if rel != definition:
                    confirmed.append(item)
    return {
        "classes": list(patterns), "files_scanned": scanned,
        "candidates": candidates, "confirmed": confirmed,
        "confirmed_count": len(confirmed), "complete_privacy": False,
    }


def security(paths: list[Path]) -> dict:
    findings = []
    python_files = [path for path in paths if path.suffix == ".py"]
    for path in python_files:
        rel = path.relative_to(ROOT).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": rel, "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                findings.append({"path": rel, "line": node.lineno, "kind": "system_call"})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": rel, "line": node.lineno, "kind": "shell_true"})
    return {"python_files": len(python_files), "findings": findings, "exhaustive_security": False}


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise SystemExit("x1 validation build requires the exact Teryn final source head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected Caelen branch")
    if git("diff", "--name-only").stdout.strip():
        raise SystemExit("tracked source drift before x1 validation")

    rows = load(X1 / "new-proposals.json")["proposals"]
    inherited = load(X1 / "inherited-review.json")["rows"]
    scores = []
    for row in rows:
        left = tokens(row["title"])
        nearest = max(
            ((len(left & tokens(old["title"])) / len(left | tokens(old["title"])), old["source_id"])
             for old in inherited),
            default=(0.0, None),
        )
        scores.append({"proposal_id": row["id"], "nearest_source_id": nearest[1], "token_jaccard": round(nearest[0], 6)})
    write(
        VALIDATION / "x1-refinement-check.json",
        {
            "new_rows": len(rows), "inherited_rows": len(inherited),
            "exact_title_collisions": len({r["title"] for r in rows}) != len(rows),
            "maximum_token_jaccard": max(x["token_jaccard"] for x in scores),
            "high_similarity_threshold": 0.78,
            "high_similarity_rows": [x for x in scores if x["token_jaccard"] >= 0.78],
            "declared_family_chain": 14630,
            "global_novelty_claim": False,
            "boundary": "Direct semantic-neighbor review covers the 200 inherited source contracts; it is not a universal novelty proof over every historical row.",
        },
    )

    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_ghc_family_caelen_ash_v687_v5_x1", "-v"],
        cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True
    )
    write(
        VALIDATION / "x1-tests.json",
        {"selected": 9, "passed": 9 if tests.returncode == 0 else 0, "returncode": tests.returncode, "success": tests.returncode == 0},
    )
    current = x1_files()
    write(VALIDATION / "x1-privacy.json", privacy(current))
    write(VALIDATION / "x1-security.json", security(current))
    write(
        VALIDATION / "x1-staged-review.json",
        {
            "state": "PREPARED_NOT_STAGED", "staged_count": 0,
            "manifest_entry_count": 0, "manifest_mismatches": [],
            "missing_paths": [], "out_of_scope_paths": [],
            "inherited_paths_changed": [], "diff_hygiene": "PENDING_STAGING",
        },
    )
    exclusions = {
        "docs/caelen-ash/v687-v5/validation/x1-manifest.json",
        "docs/caelen-ash/v687-v5/validation/x1-staged-review.json",
    }
    entries = [
        {"path": path.relative_to(ROOT).as_posix(), "bytes_normalized_lf": len(normalized(path)), "sha256_normalized_lf": digest(path)}
        for path in x1_files() if path.relative_to(ROOT).as_posix() not in exclusions
    ]
    write(
        VALIDATION / "x1-manifest.json",
        {"schema": "ghc.family.caelen-manifest.v1", "byte_domain": "normalized_lf_git_blob", "entries": entries, "self_exclusions": sorted(exclusions)},
    )
    review = load(VALIDATION / "x1-staged-review.json")
    review["manifest_entry_count"] = len(entries)
    write(VALIDATION / "x1-staged-review.json", review)


def review_staged() -> None:
    manifest = load(VALIDATION / "x1-manifest.json")
    expected = {item["path"]: item["sha256_normalized_lf"] for item in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    wanted = set(expected) | exclusions
    mismatches = []
    for rel, expected_hash in sorted(expected.items()):
        data = subprocess.run(["git", "show", f":{rel}"], cwd=ROOT, check=False, capture_output=True).stdout
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected_hash:
            mismatches.append({"path": rel, "expected": expected_hash, "actual": actual})
    diff = git("diff", "--cached", "--check", check=False)
    missing = sorted(wanted - set(staged))
    out_of_scope = sorted(set(staged) - wanted)
    inherited = [rel for rel in staged if not (rel.startswith("docs/caelen-ash/v687-v5/") or "caelen_ash_v687_v5" in rel)]
    passed = not mismatches and not missing and not out_of_scope and not inherited and diff.returncode == 0
    write(
        VALIDATION / "x1-staged-review.json",
        {
            "state": "PASS" if passed else "FAIL", "staged_count": len(staged),
            "manifest_entry_count": len(expected), "self_exclusions": sorted(exclusions),
            "exact_staged_allowlist": staged, "manifest_mismatches": mismatches,
            "missing_paths": missing, "out_of_scope_paths": out_of_scope,
            "inherited_paths_changed": inherited,
            "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff.stdout + diff.stderr,
        },
    )
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
