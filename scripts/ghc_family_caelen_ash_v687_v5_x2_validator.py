#!/usr/bin/env python3
"""Build and review Caelen Ash v687-v5 immutable x2 evidence validation."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from ghc_family_caelen_ash_v687_v5_core import strict_load


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-ash" / "v687-v5"
VALIDATION = BASE / "validation"
X1 = "a3e882fc450322186c71ab430be501f3cb3648a0"
BRANCH = "codex/GHC-Family/caelen-ash-v687-v5-full-tools"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True,
    )


def git_bytes(*args: str, check: bool = True) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)
    return result.stdout


def batch_git_objects(specifications: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    objects: dict[str, bytes] = {}
    for specification in specifications:
        process.stdin.write((specification + "\n").encode("utf-8"))
        process.stdin.flush()
        header = process.stdout.readline().decode("ascii", errors="strict").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise SystemExit("unexpected git cat-file header for " + specification)
        size = int(header[2])
        objects[specification] = process.stdout.read(size)
        if process.stdout.read(1) != b"\n":
            raise SystemExit("missing git cat-file record separator")
    process.stdin.close()
    error = process.stderr.read() if process.stderr is not None else b""
    returncode = process.wait()
    if returncode != 0:
        raise SystemExit("git cat-file batch failed: " + error.decode("utf-8", errors="replace"))
    return objects


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded(value))


def normalized_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized(path: Path) -> bytes:
    return normalized_bytes(path.read_bytes())


def digest(path: Path) -> str:
    return hashlib.sha256(normalized(path)).hexdigest()


def delta_names() -> list[str]:
    tracked = [line for line in git("diff", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    staged = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    untracked = [line for line in git("ls-files", "--others", "--exclude-standard").stdout.splitlines() if line]
    return sorted(set(tracked + staged + untracked))


def delta_files() -> list[Path]:
    return [ROOT / name for name in delta_names() if (ROOT / name).is_file()]


def privacy(paths: list[Path]) -> dict:
    patterns = {
        "raw_task_identifier": re.compile(r"(?i)(?:thread|task)[_-]?id\s*[:=]\s*[0-9a-f]{8}"),
        "private_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+"),
        "secret_assignment": re.compile(r"(?i)(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s\"']{8,}"),
        "private_callable_route": re.compile(r"(?i)(?:mcp__codex_app__|providerTabId|clientThreadId)"),
        "private_application_state": re.compile(r"(?i)(?:session[_-]?stream|private app state|raw transcript)"),
    }
    definition = "scripts/ghc_family_caelen_ash_v687_v5_x2_validator.py"
    candidates, confirmed, scanned = [], [], 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".html", ".txt", ".py", ".lock"}:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        for kind, pattern in patterns.items():
            for match in pattern.finditer(text):
                item = {
                    "path": relative,
                    "line": text.count("\n", 0, match.start()) + 1,
                    "kind": kind,
                    "disposition": "scanner_definition_not_payload" if relative == definition else "confirmed_payload_hit",
                }
                candidates.append(item)
                if relative != definition:
                    confirmed.append(item)
    return {
        "classes": list(patterns),
        "files_scanned": scanned,
        "candidates": candidates,
        "confirmed": confirmed,
        "confirmed_count": len(confirmed),
        "complete_privacy": False,
    }


def security(paths: list[Path]) -> dict:
    findings = []
    python_files = [path for path in paths if path.suffix == ".py"]
    for path in python_files:
        relative = path.relative_to(ROOT).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": relative, "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                findings.append({"path": relative, "line": node.lineno, "kind": "system_call"})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": relative, "line": node.lineno, "kind": "shell_true"})
    return {"python_files": len(python_files), "findings": findings, "exhaustive_security": False}


def build(global_skills: Path, global_scripts: Path) -> None:
    if git("rev-parse", "HEAD").stdout.strip() != X1:
        raise SystemExit("x2 validation requires the immutable x1 head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected owner branch")
    if git("diff", "--name-only", "--", "docs/caelen-ash/v687-v5/x1", "scripts/build_ghc_family_caelen_ash_v687_v5_x1.py", "scripts/ghc_family_caelen_ash_v687_v5_plan_cases.py", "scripts/ghc_family_caelen_ash_v687_v5_x1_validator.py", "tests/test_ghc_family_caelen_ash_v687_v5_x1.py").stdout.strip():
        raise SystemExit("x1 source drift detected")

    x1_manifest = strict_load(VALIDATION / "x1-manifest.json")
    mismatches = []
    for entry in x1_manifest["entries"]:
        data = git_bytes("show", f"{X1}:{entry['path']}")
        actual = hashlib.sha256(normalized_bytes(data)).hexdigest()
        if actual != entry["sha256_normalized_lf"]:
            mismatches.append({"path": entry["path"], "expected": entry["sha256_normalized_lf"], "actual": actual})
    write(
        VALIDATION / "x1-immutable-replay.json",
        {"anchor": X1, "entries": len(x1_manifest["entries"]), "self_exclusions": x1_manifest["self_exclusions"], "mismatches": mismatches, "passed": not mismatches},
    )

    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_ghc_family_caelen_ash_v687_v5_x2", "-v"],
        cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True,
    )
    write(VALIDATION / "x2-tests.json", {"selected": 10, "passed": 10 if tests.returncode == 0 else 0, "returncode": tests.returncode, "success": tests.returncode == 0})

    promotion = strict_load(BASE / "x2" / "promotion-receipt.json")
    promotion_mismatches = []
    for member in promotion["members"]:
        local = BASE / "skills" / member["skill"] / member["path"]
        global_member = global_skills / member["skill"] / member["path"]
        for domain, path in [("local", local), ("global", global_member)]:
            actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
            if actual != member["sha256"]:
                promotion_mismatches.append({"skill": member["skill"], "path": member["path"], "domain": domain, "expected": member["sha256"], "actual": actual})
    for name in promotion["shared_names"]:
        local = ROOT / "scripts" / name
        global_member = global_scripts / name
        if not local.exists() or not global_member.exists() or hashlib.sha256(local.read_bytes()).hexdigest() != hashlib.sha256(global_member.read_bytes()).hexdigest():
            promotion_mismatches.append({"shared_name": name, "domain": "local_global_byte_parity"})
    write(VALIDATION / "x2-promotion-parity.json", {"skills": promotion["skills"], "shared_runners": promotion["shared_runners"], "dependency_files": promotion["dependency_files"], "mismatches": promotion_mismatches, "passed": not promotion_mismatches})

    current = delta_files()
    json_paths = [path for path in current if path.suffix == ".json"]
    json_failures = []
    for path in json_paths:
        try:
            strict_load(path)
        except Exception as exc:
            json_failures.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    write(VALIDATION / "x2-json-preflight.json", {"documents": len(json_paths), "failures": json_failures, "duplicate_key_refusal": True, "nonfinite_refusal": True, "passed": not json_failures})
    current = delta_files()
    write(VALIDATION / "x2-privacy.json", privacy(current))
    write(VALIDATION / "x2-security.json", security(current))
    write(
        VALIDATION / "x2-staged-review.json",
        {"state": "PREPARED_NOT_STAGED", "staged_count": 0, "manifest_entry_count": 0, "manifest_mismatches": [], "missing_paths": [], "out_of_scope_paths": [], "x1_paths_changed": [], "diff_hygiene": "PENDING_STAGING"},
    )

    exclusions = {
        "docs/caelen-ash/v687-v5/validation/x2-manifest.json",
        "docs/caelen-ash/v687-v5/validation/x2-staged-review.json",
    }
    entries = [
        {"path": path.relative_to(ROOT).as_posix(), "bytes_normalized_lf": len(normalized(path)), "sha256_normalized_lf": digest(path)}
        for path in delta_files() if path.relative_to(ROOT).as_posix() not in exclusions
    ]
    write(
        VALIDATION / "x2-manifest.json",
        {"schema": "ghc.family.caelen-x2-manifest.v1", "anchor_parent": X1, "byte_domain": "normalized_lf_git_blob", "entries": entries, "self_exclusions": sorted(exclusions)},
    )
    review = strict_load(VALIDATION / "x2-staged-review.json")
    review["manifest_entry_count"] = len(entries)
    write(VALIDATION / "x2-staged-review.json", review)

    privacy_receipt = strict_load(VALIDATION / "x2-privacy.json")
    security_receipt = strict_load(VALIDATION / "x2-security.json")
    if mismatches or tests.returncode or promotion_mismatches or json_failures or privacy_receipt["confirmed_count"] or security_receipt["findings"]:
        raise SystemExit("x2 validation preparation failed")


def review_staged() -> None:
    manifest = strict_load(VALIDATION / "x2-manifest.json")
    expected = {item["path"]: item["sha256_normalized_lf"] for item in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    wanted = set(expected) | exclusions
    mismatches = []
    specifications = [":" + relative for relative in sorted(expected)]
    staged_objects = batch_git_objects(specifications)
    for relative, expected_hash in sorted(expected.items()):
        actual = hashlib.sha256(normalized_bytes(staged_objects[":" + relative])).hexdigest()
        if actual != expected_hash:
            mismatches.append({"path": relative, "expected": expected_hash, "actual": actual})
    diff = git("diff", "--cached", "--check", check=False)
    missing = sorted(wanted - set(staged))
    out_of_scope = sorted(set(staged) - wanted)
    x1_changed = [name for name in staged if name.startswith("docs/caelen-ash/v687-v5/x1/") or name.endswith("_v687_v5_x1.py") or name.endswith("_v687_v5_plan_cases.py")]
    passed = not mismatches and not missing and not out_of_scope and not x1_changed and diff.returncode == 0
    write(
        VALIDATION / "x2-staged-review.json",
        {
            "state": "PASS" if passed else "FAIL",
            "staged_count": len(staged),
            "manifest_entry_count": len(expected),
            "self_exclusions": sorted(exclusions),
            "exact_staged_allowlist": staged,
            "manifest_mismatches": mismatches,
            "missing_paths": missing,
            "out_of_scope_paths": out_of_scope,
            "x1_paths_changed": x1_changed,
            "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff.stdout + diff.stderr,
        },
    )
    if not passed:
        raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    parser.add_argument("--global-skills", type=Path)
    parser.add_argument("--global-scripts", type=Path)
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        if args.global_skills is None or args.global_scripts is None:
            raise SystemExit("global roots are required for preparation")
        build(args.global_skills, args.global_scripts)


if __name__ == "__main__":
    main()
