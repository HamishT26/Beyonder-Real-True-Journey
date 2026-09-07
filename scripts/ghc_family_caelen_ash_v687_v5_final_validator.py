#!/usr/bin/env python3
"""Prepare and review Caelen Ash v687-v5 final owner-scoped validation evidence."""

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
SOURCE = "5a71b1b7866171aa4ee16664ab7fc434bb6f5593"
X1 = "a3e882fc450322186c71ab430be501f3cb3648a0"
EVIDENCE = "e2de3422d62572b7d1e8fbfa8e84c8a4f9fded72"
BRANCH = "codex/GHC-Family/caelen-ash-v687-v5-full-tools"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, text=True, encoding="utf-8", errors="strict", capture_output=True)


def batch_git_objects(specifications: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            raise SystemExit("missing git cat-file separator")
    process.stdin.close()
    error = process.stderr.read() if process.stderr is not None else b""
    code = process.wait()
    if code:
        raise SystemExit("git cat-file failed: " + error.decode("utf-8", errors="replace"))
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


def is_owner(relative: str) -> bool:
    return relative.startswith("docs/caelen-ash/v687-v5/") or bool(re.fullmatch(r"(?:scripts|tests)/[^/]*caelen_ash_v687_v5[^/]*\.py", relative))


def status_names() -> list[str]:
    values = []
    for args in [("diff", "--name-only", "--diff-filter=ACMR"), ("diff", "--cached", "--name-only", "--diff-filter=ACMR"), ("ls-files", "--others", "--exclude-standard")]:
        values.extend(line for line in git(*args).stdout.splitlines() if line)
    return sorted(set(values))


def delta_files() -> list[Path]:
    return [ROOT / relative for relative in status_names() if (ROOT / relative).is_file()]


def owner_files() -> list[Path]:
    names = [line for line in git("ls-files").stdout.splitlines() if line]
    names.extend(line for line in git("ls-files", "--others", "--exclude-standard").stdout.splitlines() if line)
    return [ROOT / relative for relative in sorted(set(names)) if is_owner(relative) and (ROOT / relative).is_file()]


def privacy(paths: list[Path]) -> dict:
    patterns = {
        "raw_task_identifier": re.compile(r"(?i)(?:thread|task)[_-]?id\s*[:=]\s*[0-9a-f]{8}"),
        "private_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+"),
        "secret_assignment": re.compile(r"(?i)(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s\"']{8,}"),
        "private_callable_route": re.compile(r"(?i)(?:mcp__codex_app__|providerTabId|clientThreadId)"),
        "private_application_state": re.compile(r"(?i)(?:session[_-]?stream|private app state|raw transcript)"),
    }
    definitions = {
        "scripts/ghc_family_caelen_ash_v687_v5_x1_validator.py",
        "scripts/ghc_family_caelen_ash_v687_v5_x2_validator.py",
        "scripts/ghc_family_caelen_ash_v687_v5_final_validator.py",
        "scripts/ghc_family_caelen_ash_v687_v5_canonical.py",
    }
    boundary_files = {
        "scripts/build_ghc_family_caelen_ash_v687_v5_final.py",
        "docs/caelen-ash/v687-v5/handoffs/future-sibling-09-v687-v6-induction-baton.md",
        "docs/caelen-ash/v687-v5/handoffs/compact-induction-candidate.md",
    }
    candidates, confirmed, scanned = [], [], 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".html", ".txt", ".py", ".lock"}:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        for kind, pattern in patterns.items():
            for match in pattern.finditer(text):
                if relative in definitions:
                    disposition = "scanner_definition_not_payload"
                elif relative in boundary_files and kind == "private_application_state":
                    disposition = "boundary_vocabulary_not_payload"
                else:
                    disposition = "confirmed_payload_hit"
                item = {"path": relative, "line": text.count("\n", 0, match.start()) + 1, "kind": kind, "disposition": disposition}
                candidates.append(item)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(item)
    return {"classes": list(patterns), "files_scanned": scanned, "candidates": candidates, "confirmed": confirmed, "confirmed_count": len(confirmed), "complete_privacy": False}


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


def replay_manifest(anchor: str, manifest_path: Path) -> dict:
    manifest = strict_load(manifest_path)
    specifications = [anchor + ":" + entry["path"] for entry in manifest["entries"]]
    objects = batch_git_objects(specifications)
    mismatches = []
    for entry in manifest["entries"]:
        specification = anchor + ":" + entry["path"]
        actual = hashlib.sha256(normalized_bytes(objects[specification])).hexdigest()
        expected = entry["sha256_normalized_lf"]
        if actual != expected:
            mismatches.append({"path": entry["path"], "expected": expected, "actual": actual})
    return {"anchor": anchor, "entries": len(manifest["entries"]), "self_exclusions": manifest["self_exclusions"], "mismatches": mismatches, "passed": not mismatches}


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != EVIDENCE:
        raise SystemExit("final validation preparation requires immutable x2 evidence head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected owner branch")
    if git("diff", "--name-only", X1, "--", "docs/caelen-ash/v687-v5/x1", "scripts/build_ghc_family_caelen_ash_v687_v5_x1.py", "scripts/ghc_family_caelen_ash_v687_v5_plan_cases.py", "scripts/ghc_family_caelen_ash_v687_v5_x1_validator.py", "tests/test_ghc_family_caelen_ash_v687_v5_x1.py").stdout.strip():
        raise SystemExit("x1 drift detected")

    x1 = replay_manifest(X1, VALIDATION / "x1-manifest.json")
    x2 = replay_manifest(EVIDENCE, VALIDATION / "x2-manifest.json")
    write(VALIDATION / "final-immutable-replay.json", {"x1": x1, "x2": x2, "mismatch_count": len(x1["mismatches"]) + len(x2["mismatches"])})
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_ghc_family_caelen_ash_v687_v5_x2", "tests.test_ghc_family_caelen_ash_v687_v5_final", "-v"],
        cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True,
    )
    write(VALIDATION / "final-tests.json", {"selected": 20, "passed": 20 if tests.returncode == 0 else 0, "returncode": tests.returncode, "success": tests.returncode == 0})

    current_owner = owner_files()
    json_failures = []
    json_paths = [path for path in current_owner if path.suffix == ".json"]
    for path in json_paths:
        try:
            strict_load(path)
        except Exception as exc:
            json_failures.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    write(VALIDATION / "final-json-preflight.json", {"documents": len(json_paths), "failures": json_failures, "duplicate_key_refusal": True, "nonfinite_refusal": True, "passed": not json_failures})
    current_owner = owner_files()
    write(VALIDATION / "final-privacy.json", privacy(current_owner))
    write(VALIDATION / "final-security.json", security(delta_files()))
    write(VALIDATION / "final-staged-review.json", {"state": "PREPARED_NOT_STAGED", "staged_count": 0, "delta_manifest_entries": 0, "owner_manifest_entries": 0, "manifest_mismatches": [], "missing_paths": [], "out_of_scope_paths": [], "diff_hygiene": "PENDING_STAGING"})

    delta_exclusions = {
        "docs/caelen-ash/v687-v5/validation/final-delta-manifest.json",
        "docs/caelen-ash/v687-v5/validation/final-owner-manifest.json",
        "docs/caelen-ash/v687-v5/validation/final-staged-review.json",
    }
    delta_entries = [{"path": path.relative_to(ROOT).as_posix(), "bytes_normalized_lf": len(normalized(path)), "sha256_normalized_lf": digest(path)} for path in delta_files() if path.relative_to(ROOT).as_posix() not in delta_exclusions]
    write(VALIDATION / "final-delta-manifest.json", {"schema": "ghc.family.caelen-final-delta-manifest.v1", "parent": EVIDENCE, "byte_domain": "normalized_lf_git_blob", "entries": delta_entries, "self_exclusions": sorted(delta_exclusions)})

    owner_exclusions = {
        "docs/caelen-ash/v687-v5/validation/final-owner-manifest.json",
        "docs/caelen-ash/v687-v5/validation/final-staged-review.json",
    }
    owner_entries = [{"path": path.relative_to(ROOT).as_posix(), "bytes_normalized_lf": len(normalized(path)), "sha256_normalized_lf": digest(path)} for path in owner_files() if path.relative_to(ROOT).as_posix() not in owner_exclusions]
    write(VALIDATION / "final-owner-manifest.json", {"schema": "ghc.family.caelen-final-owner-manifest.v1", "source": SOURCE, "byte_domain": "normalized_lf_git_blob", "entries": owner_entries, "self_exclusions": sorted(owner_exclusions)})
    review = strict_load(VALIDATION / "final-staged-review.json")
    review["delta_manifest_entries"] = len(delta_entries)
    review["owner_manifest_entries"] = len(owner_entries)
    write(VALIDATION / "final-staged-review.json", review)

    privacy_receipt = strict_load(VALIDATION / "final-privacy.json")
    security_receipt = strict_load(VALIDATION / "final-security.json")
    if x1["mismatches"] or x2["mismatches"] or tests.returncode or json_failures or privacy_receipt["confirmed_count"] or security_receipt["findings"]:
        raise SystemExit("final validation preparation failed")


def review_staged() -> None:
    delta_manifest = strict_load(VALIDATION / "final-delta-manifest.json")
    owner_manifest = strict_load(VALIDATION / "final-owner-manifest.json")
    delta_expected = {entry["path"]: entry["sha256_normalized_lf"] for entry in delta_manifest["entries"]}
    owner_expected = {entry["path"]: entry["sha256_normalized_lf"] for entry in owner_manifest["entries"]}
    exclusions = set(delta_manifest["self_exclusions"])
    staged = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    specifications = [":" + relative for relative in sorted(owner_expected)]
    objects = batch_git_objects(specifications)
    mismatches = []
    for relative, expected in sorted(owner_expected.items()):
        actual = hashlib.sha256(normalized_bytes(objects[":" + relative])).hexdigest()
        if actual != expected:
            mismatches.append({"path": relative, "expected": expected, "actual": actual})
    wanted = set(delta_expected) | exclusions
    missing = sorted(wanted - set(staged))
    out_of_scope = sorted(set(staged) - wanted)
    diff = git("diff", "--cached", "--check", check=False)
    passed = not mismatches and not missing and not out_of_scope and diff.returncode == 0
    write(
        VALIDATION / "final-staged-review.json",
        {
            "state": "PASS" if passed else "FAIL",
            "staged_count": len(staged),
            "delta_manifest_entries": len(delta_expected),
            "delta_self_exclusions": sorted(exclusions),
            "owner_manifest_entries": len(owner_expected),
            "owner_self_exclusions": owner_manifest["self_exclusions"],
            "manifest_mismatches": mismatches,
            "missing_paths": missing,
            "out_of_scope_paths": out_of_scope,
            "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff.stdout + diff.stderr,
        },
    )
    if not passed:
        raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    review_staged() if args.review_staged else build()


if __name__ == "__main__":
    main()
