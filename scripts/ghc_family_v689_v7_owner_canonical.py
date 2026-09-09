#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical for Vesper v689-v7."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PLANNING = "ec29a1f3fa0471bf2f8d654c162846645adda1b6"
X1 = "d88dac91bed120345dad6b0371db570c37b8fed2"
X2 = "bac4894acf6a440d031cd8ebd88fc906f22e3826"
PHASE_ROOT = "docs/vesper-arlen/v689-v7"
MANIFESTS = [
    (PLANNING, f"{PHASE_ROOT}/plan/manifest.json"),
    (X1, f"{PHASE_ROOT}/x1/manifest.json"),
    (X2, f"{PHASE_ROOT}/x2/manifest.json"),
]
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
BOUNDARY = (
    "Same-owner finite synthetic software and documentation evidence under "
    "shared infrastructure only. Not independent reproduction, external audit, "
    "empirical confirmation, production certification, authority, identity "
    "evidence, Theory-of-Everything proof, or Stage 20 readiness."
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def manifest_domain(data: bytes, entry: dict[str, Any]) -> bytes:
    return data if entry.get("byte_domain") == "raw" else normalized(data)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def strict_json(data: bytes) -> Any:
    return json.loads(
        data.decode("utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"nonfinite JSON value: {value}")),
    )


def run_git(root: Path, *args: str, binary: bool = False) -> bytes | str:
    process = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
    )
    if process.returncode:
        error = process.stderr.decode("utf-8", "replace") if binary else process.stderr
        raise RuntimeError(error.strip() or f"git {' '.join(args)} failed")
    return process.stdout if binary else process.stdout.strip()


def git_blob(root: Path, commit: str, path: str) -> bytes:
    value = run_git(root, "cat-file", "blob", f"{commit}:{path}", binary=True)
    assert isinstance(value, bytes)
    return value


def tree_paths(root: Path, commit: str) -> list[str]:
    value = run_git(root, "ls-tree", "-r", "--name-only", commit)
    assert isinstance(value, str)
    return [line for line in value.splitlines() if line]


def verify_manifest_blobs(root: Path, commit: str, path: str) -> dict[str, Any]:
    manifest = strict_json(git_blob(root, commit, path))
    mismatches = []
    for entry in manifest["entries"]:
        data = manifest_domain(git_blob(root, commit, entry["path"]), entry)
        if len(data) != entry["bytes_normalized_lf"] or sha256(data) != entry["sha256_normalized_lf"]:
            mismatches.append(entry["path"])
    return {"commit": commit, "path": path, "entries": len(manifest["entries"]), "mismatches": mismatches}


def verify_manifest_checkout(root: Path, path: Path) -> dict[str, Any]:
    manifest = strict_json(path.read_bytes())
    mismatches = []
    for entry in manifest["entries"]:
        data = manifest_domain((root / entry["path"]).read_bytes(), entry)
        if len(data) != entry["bytes_normalized_lf"] or sha256(data) != entry["sha256_normalized_lf"]:
            mismatches.append(entry["path"])
    return {"path": path.relative_to(root).as_posix(), "entries": len(manifest["entries"]), "mismatches": mismatches}


def verify_content_seal_blobs(root: Path, commit: str) -> dict[str, Any]:
    path = f"{PHASE_ROOT}/final/content-seal.json"
    seal = strict_json(git_blob(root, commit, path))
    mismatches = []
    for entry in seal["targets"]:
        data = manifest_domain(git_blob(root, commit, entry["path"]), entry)
        if len(data) != entry["bytes_normalized_lf"] or sha256(data) != entry["sha256_normalized_lf"]:
            mismatches.append(entry["path"])
    return {"targets": len(seal["targets"]), "mismatches": mismatches, "self_exclusions": seal["self_exclusions"]}


def verify_content_seal_checkout(root: Path) -> dict[str, Any]:
    seal_path = root / PHASE_ROOT / "final/content-seal.json"
    seal = strict_json(seal_path.read_bytes())
    mismatches = []
    for entry in seal["targets"]:
        data = manifest_domain((root / entry["path"]).read_bytes(), entry)
        if len(data) != entry["bytes_normalized_lf"] or sha256(data) != entry["sha256_normalized_lf"]:
            mismatches.append(entry["path"])
    return {"targets": len(seal["targets"]), "mismatches": mismatches, "self_exclusions": seal["self_exclusions"]}


def privacy_scan(files: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_user_root": re.compile(rb"[A-Za-z]:\\\\Users\\\\", re.IGNORECASE),
        "private_uri": re.compile(rb"(?:plugin|app|codex)://", re.IGNORECASE),
        "delegation_markup": re.compile(rb"(?:<codex_delegation|source_thread_id)", re.IGNORECASE),
        "credential_assignment": re.compile(rb"(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.IGNORECASE),
    }
    definition_paths = {
        "scripts/ghc_family_v689_v7_plan_validate.py",
        "scripts/ghc_family_v689_v7_x1_builder.py",
        "scripts/ghc_family_v689_v7_x2_builder.py",
        "scripts/ghc_family_v689_v7_owner_canonical.py",
        "scripts/ghc_family_v689_v7_final_builder.py",
    }
    confirmed = []
    definition_candidates = []
    scanned = 0
    for path, data in files.items():
        if not path.endswith((".json", ".md", ".html", ".py", ".lock")):
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(data):
                row = {"class": label, "path": path}
                (definition_candidates if path in definition_paths else confirmed).append(row)
    return {"scanned_text_files": scanned, "classes": list(patterns), "definition_candidates": definition_candidates, "confirmed_hits": confirmed}


def security_scan(files: dict[str, bytes]) -> dict[str, Any]:
    findings = []
    parsed = 0
    for path, data in files.items():
        if not path.endswith(".py"):
            continue
        parsed += 1
        tree = ast.parse(data.decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
                findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"path": path, "line": node.lineno, "kind": "shell_true"})
    return {"python_files": parsed, "findings": findings}


def common_content_checks(files: dict[str, bytes]) -> dict[str, Any]:
    json_paths = [path for path in files if path.startswith(PHASE_ROOT) and path.endswith(".json")]
    for path in json_paths:
        strict_json(files[path])
    x1 = strict_json(files[f"{PHASE_ROOT}/x1/results.json"])
    x2 = strict_json(files[f"{PHASE_ROOT}/x2/results.json"])
    outcomes = {
        label: x1["counts"].get(label, 0) + x2["counts"].get(label, 0)
        for label in ALLOWED_OUTCOMES
    }
    expected_outcomes = {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}
    if outcomes != expected_outcomes:
        raise RuntimeError(f"outcome mismatch: {outcomes}")
    if set(outcomes) != ALLOWED_OUTCOMES:
        raise RuntimeError("unknown outcome label")
    for relative in ("x1/test-receipt.json", "x2/test-receipt.json"):
        if strict_json(files[f"{PHASE_ROOT}/{relative}"])["passed"] is not True:
            raise RuntimeError(f"failed test receipt: {relative}")
    if strict_json(files[f"{PHASE_ROOT}/x1/skill-validation.json"])["passed"] != 10:
        raise RuntimeError("x1 skill count")
    if strict_json(files[f"{PHASE_ROOT}/x2/skill-validation.json"])["passed"] != 10:
        raise RuntimeError("x2 skill count")
    if strict_json(files[f"{PHASE_ROOT}/x1/runner-smokes.json"])["passed"] != 20:
        raise RuntimeError("x1 runner smoke count")
    if strict_json(files[f"{PHASE_ROOT}/x2/runner-smokes.json"])["passed"] != 20:
        raise RuntimeError("x2 runner smoke count")
    if strict_json(files[f"{PHASE_ROOT}/x2/package-comparisons.json"])["passed"] != 30:
        raise RuntimeError("package comparison count")
    deck = strict_json(files[f"{PHASE_ROOT}/deck/deck-index.json"])
    if deck["counts"]["total"] != 208 or deck["counts"]["tier_4"] != 200:
        raise RuntimeError("deck count")
    baton = files[f"{PHASE_ROOT}/final/hand-off-baton.md"].decode("utf-8")
    baton_words = len(re.findall(r"\S+", baton))
    if not 10_000 <= baton_words <= 100_000 or "EOF VESPER ARLEN v689-v7 BATON." not in baton:
        raise RuntimeError("baton word or EOF contract")
    modules = [path for path in files if path.startswith(f"{PHASE_ROOT}/final/modules/") and path.endswith(".md")]
    if len(modules) != 13:
        raise RuntimeError("module count")
    privacy = privacy_scan(files)
    security = security_scan(files)
    if privacy["confirmed_hits"]:
        raise RuntimeError(f"privacy hits: {privacy['confirmed_hits']}")
    if security["findings"]:
        raise RuntimeError(f"security findings: {security['findings']}")
    return {"json_documents": len(json_paths), "outcomes": outcomes, "baton_words": baton_words, "modules": len(modules), "privacy": privacy, "security": security}


def checkout_files(root: Path) -> dict[str, bytes]:
    paths = []
    for relative_root in (Path(PHASE_ROOT), Path("scripts"), Path("tests")):
        base = root / relative_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.name != ".git":
                paths.append(path)
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(set(paths))}


def commit_files(root: Path, commit: str) -> dict[str, bytes]:
    paths = [path for path in tree_paths(root, commit) if path.startswith((PHASE_ROOT + "/", "scripts/", "tests/"))]
    return {path: git_blob(root, commit, path) for path in paths}


def preflight(root: Path) -> dict[str, Any]:
    files = checkout_files(root)
    common = common_content_checks(files)
    manifest = verify_manifest_checkout(root, root / PHASE_ROOT / "final/manifest.json")
    seal = verify_content_seal_checkout(root)
    if manifest["mismatches"] or seal["mismatches"]:
        raise RuntimeError("preflight manifest or content-seal mismatch")
    return {"status": "VALID_PREFLIGHT_NO_CANONICAL_CREDIT", "manifest": manifest, "content_seal": seal, **common, "boundary": BOUNDARY}


def canonical(root: Path, expected_final: str, branch: str) -> dict[str, Any]:
    head = run_git(root, "rev-parse", "HEAD")
    assert isinstance(head, str)
    if head != expected_final:
        raise RuntimeError("HEAD does not match expected final")
    current_branch = run_git(root, "symbolic-ref", "--short", "HEAD")
    if current_branch != branch:
        raise RuntimeError("branch mismatch")
    if run_git(root, "status", "--porcelain=v1"):
        raise RuntimeError("worktree is not clean")
    history_value = run_git(root, "rev-list", "--reverse", expected_final)
    assert isinstance(history_value, str)
    history = history_value.splitlines()
    if len(history) != 4 or history[:3] != [PLANNING, X1, X2] or history[3] != expected_final:
        raise RuntimeError(f"unexpected blank-root history: {history}")
    if run_git(root, "rev-list", "--count", "--merges", expected_final) != "0":
        raise RuntimeError("merge commit present")
    if run_git(root, "show", "-s", "--format=%P", PLANNING) != "":
        raise RuntimeError("planning commit is not root")
    upstream = run_git(root, "rev-parse", "@{upstream}")
    tracking = run_git(root, "rev-parse", f"refs/remotes/origin/{branch}")
    live_value = run_git(root, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    assert isinstance(live_value, str)
    live = live_value.split()[0]
    if len({head, upstream, tracking, live}) != 1:
        raise RuntimeError("four-way equality failed")
    manifests = [verify_manifest_blobs(root, commit, path) for commit, path in [*MANIFESTS, (expected_final, f"{PHASE_ROOT}/final/manifest.json")]]
    if any(row["mismatches"] for row in manifests):
        raise RuntimeError("manifest mismatch")
    seal = verify_content_seal_blobs(root, expected_final)
    if seal["mismatches"]:
        raise RuntimeError("content seal mismatch")
    files = commit_files(root, expected_final)
    common = common_content_checks(files)
    tracked = len(tree_paths(root, expected_final))
    if tracked >= 2_000:
        raise RuntimeError("owner file ceiling exceeded")
    return {
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "expected_final": expected_final,
        "branch": branch,
        "history": history,
        "commits": 4,
        "merges": 0,
        "clean": True,
        "divergence": "0/0",
        "four_way_equal": True,
        "tracked_files": tracked,
        "manifests": manifests,
        "manifest_entries": sum(row["entries"] for row in manifests),
        "content_seal": seal,
        **common,
        "invocations": 1,
        "successes": 1,
        "replays": 0,
        "complete_repository_suite": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }


def write_exclusive(path: Path, value: dict[str, Any]) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--expected-final")
    parser.add_argument("--branch")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--latch", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    if args.preflight:
        print(json.dumps(preflight(root), sort_keys=True))
        return 0
    if not all((args.expected_final, args.branch, args.receipt, args.latch)):
        parser.error("canonical mode requires expected final, branch, receipt, and latch")
    assert args.receipt is not None and args.latch is not None
    marker = {
        "schema": "ghc.family.canonical-invocation-latch.v1",
        "owner": "Vesper Arlen",
        "phase": "v689-v7",
        "expected_final": args.expected_final,
        "invoked_at_utc": datetime.now(timezone.utc).isoformat(),
        "state": "INVOKED_ONCE_NO_REPLAY",
    }
    write_exclusive(args.latch, marker)
    try:
        payload = canonical(root, args.expected_final, args.branch)
    except (OSError, ValueError, RuntimeError, AssertionError, subprocess.SubprocessError) as exc:
        payload = {
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "expected_final": args.expected_final,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "invocations": 1,
            "successes": 0,
            "replays": 0,
            "boundary": BOUNDARY,
        }
        write_exclusive(args.receipt, payload)
        print(json.dumps(payload, sort_keys=True))
        return 2
    write_exclusive(args.receipt, payload)
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
