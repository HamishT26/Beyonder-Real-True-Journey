"""One-shot exact-final owner-scoped validator for Caelen Morrow v671-v3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_PREFIX = "docs/caelen-morrow/v671-v3/"
SOURCE = "33b7c2d6b9f79f931ff98c478f136dab823c4d69"
X1 = "2551c126776ea0538354a32b90414f31f5cec4b3"
EVIDENCE = "46c41e84871edd72544ddad16f038902ec2386f5"
BRANCH = "codex/GHC-Family/caelen-morrow-v671-v3-full-tools"
RESULT = "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"


def executable(name: str) -> str:
    resolved = shutil.which(name)
    if resolved is None:
        raise RuntimeError(f"required executable unavailable: {name}")
    return resolved


def run(
    command: list[str], timeout: int = 180, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    command = [executable(command[0]), *command[1:]]
    return subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git failed")
    return result.stdout.strip()


def blob(path: str) -> bytes:
    result = subprocess.run(
        [executable("git"), "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        timeout=180,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.replace(b"\r\n", b"\n")


def load_blob_json(path: str) -> Any:
    return json.loads(blob(path).decode("utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_replay(path: str) -> dict[str, Any]:
    manifest = load_blob_json(path)
    failures = []
    for entry in manifest["entries"]:
        data = blob(entry["path"])
        if len(data) != entry["bytes"]:
            failures.append({"path": entry["path"], "kind": "bytes"})
        if sha256(data) != entry["sha256"]:
            failures.append({"path": entry["path"], "kind": "sha256"})
    return {
        "path": path,
        "declared": manifest["entry_count"],
        "observed": len(manifest["entries"]),
        "failures": failures,
        "valid": manifest["entry_count"] == len(manifest["entries"])
        and not failures,
    }


def owner_and_phase_paths() -> tuple[list[str], list[str]]:
    all_paths = [
        row for row in git("ls-tree", "-r", "--name-only", "HEAD").splitlines() if row
    ]
    owner = [path for path in all_paths if path.startswith(OWNER_PREFIX)]
    python = [
        path
        for path in all_paths
        if (
            path.startswith("scripts/")
            and (
                "caelen_morrow_v671_v3" in path
                or path.startswith("scripts/ghc_family_letterpress_")
                or path
                in {
                    "scripts/ghc_family_imposition_position_graph.py",
                    "scripts/ghc_family_typecase_relation_guard.py",
                }
            )
        )
        or (
            path.startswith("tests/")
            and "caelen_morrow_v671_v3" in path
            and path.endswith(".py")
        )
    ]
    return sorted(owner), sorted(python)


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I
        ),
        "private_route_or_callable": re.compile(
            rb"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I
        ),
        "credential_assignment": re.compile(
            rb"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
            re.I,
        ),
        "transcript_or_session_stream": re.compile(
            rb"\b(?:session_stream|private_transcript|private_conversation_dump)\b",
            re.I,
        ),
    }
    definitions = {
        "scripts/build_ghc_family_caelen_morrow_v671_v3_x1.py",
        "scripts/build_ghc_family_caelen_morrow_v671_v3_x2.py",
        "scripts/build_ghc_family_caelen_morrow_v671_v3_final.py",
        "scripts/validate_ghc_family_caelen_morrow_v671_v3_final.py",
        "tests/test_ghc_family_caelen_morrow_v671_v3_x1.py",
        "tests/test_ghc_family_caelen_morrow_v671_v3_x2.py",
        "tests/test_ghc_family_caelen_morrow_v671_v3_final.py",
    }
    candidates = []
    scanned = 0
    for path in paths:
        if Path(path).suffix.lower() not in {
            ".json",
            ".md",
            ".html",
            ".txt",
            ".py",
            ".mjs",
            ".yaml",
        }:
            continue
        data = blob(path)
        if b"\x00" in data:
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(data):
                candidates.append(
                    {
                        "path": path,
                        "pattern_class": label,
                        "disposition": (
                            "scanner_definition_or_unit_test"
                            if path in definitions
                            else "confirmed_payload_hit"
                        ),
                    }
                )
    confirmed = [
        row for row in candidates if row["disposition"] == "confirmed_payload_hit"
    ]
    return {
        "files_scanned": scanned,
        "pattern_classes": sorted(patterns),
        "candidates": candidates,
        "candidate_count": len(candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "valid": not confirmed,
        "boundary": "A bounded five-class scan is not complete privacy assurance.",
    }


def python_review(paths: list[str]) -> dict[str, Any]:
    compile_failures = []
    security_findings = []
    for path in paths:
        text = blob(path).decode("utf-8")
        try:
            tree = ast.parse(text, filename=path)
            compile(text, path, "exec")
        except SyntaxError as exc:
            compile_failures.append({"path": path, "issue": str(exc)})
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                security_findings.append(
                    {"path": path, "line": node.lineno, "kind": node.func.id}
                )
            for keyword in node.keywords:
                if (
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ):
                    security_findings.append(
                        {"path": path, "line": node.lineno, "kind": "shell_true"}
                    )
    return {
        "python_files": len(paths),
        "compile_failures": compile_failures,
        "security_findings": security_findings,
        "valid": not compile_failures and not security_findings,
        "boundary": "A bounded AST review is not exhaustive security assurance.",
    }


def parent_count(commit: str) -> int:
    return len(git("show", "-s", "--format=%P", commit).split())


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


def validate(expected_final: str, receipt_path: Path) -> None:
    if receipt_path.exists() or receipt_path.with_suffix(receipt_path.suffix + ".tmp").exists():
        raise SystemExit("canonical receipt or temporary already exists; refusing replay")

    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    fresh_live = live_line.split("\t", 1)[0] if live_line else ""
    divergence_parts = git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    clean_before = not bool(git("status", "--porcelain"))

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GHC_CAELEN_V671_V3_EXPECTED_FINAL"] = expected_final
    test = run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_ghc_family_caelen_morrow_v671_v3_final",
            "-v",
        ],
        timeout=300,
        env=env,
    )
    test_match = re.search(r"Ran (\d+) tests?", test.stderr + test.stdout)
    tests_run = int(test_match.group(1)) if test_match else 0

    owner_paths, python_paths = owner_and_phase_paths()
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    markdown_paths = [path for path in owner_paths if path.endswith(".md")]
    json_failures = []
    for path in json_paths:
        try:
            json.loads(blob(path).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_failures.append({"path": path, "issue": type(exc).__name__})
    markdown_failures = []
    for path in markdown_paths:
        try:
            blob(path).decode("utf-8")
        except UnicodeDecodeError:
            markdown_failures.append(path)

    privacy = privacy_scan(sorted(set(owner_paths + python_paths)))
    python = python_review(python_paths)
    manifests = [
        manifest_replay(
            "docs/caelen-morrow/v671-v3/validation/x1-manifest.json"
        ),
        manifest_replay(
            "docs/caelen-morrow/v671-v3/validation/evidence-manifest.json"
        ),
        manifest_replay(
            "docs/caelen-morrow/v671-v3/validation/final-delta-manifest.json"
        ),
        manifest_replay(
            "docs/caelen-morrow/v671-v3/validation/final-owner-manifest.json"
        ),
    ]

    truth = load_blob_json("docs/caelen-morrow/v671-v3/closeout/phase-truth.json")
    route = load_blob_json(
        "docs/caelen-morrow/v671-v3/orchestration/route-state-final-candidate.json"
    )
    seal = load_blob_json("docs/caelen-morrow/v671-v3/seal/content-seal.json")
    final_delta = git("diff", "--name-only", f"{EVIDENCE}..HEAD").splitlines()
    forbidden_delta = [
        path
        for path in final_delta
        if path.startswith(
            (
                "docs/caelen-morrow/v671-v3/x1/",
                "docs/caelen-morrow/v671-v3/x2/",
                "docs/caelen-morrow/v671-v3/method-flow/",
                "docs/caelen-morrow/v671-v3/skills/",
                "docs/caelen-morrow/v671-v3/tools/",
            )
        )
        or path.endswith("_v671_v3_x1.py")
        or path.endswith("_v671_v3_x2.py")
        or "ghc_family_letterpress_" in path
        or path.endswith("ghc_family_caelen_morrow_v671_v3_letterpress.py")
    ]
    word_cap_failures = []
    for path in owner_paths:
        if Path(path).suffix.lower() in {".json", ".md", ".html", ".txt", ".py"}:
            try:
                words = len(blob(path).decode("utf-8").split())
            except UnicodeDecodeError:
                continue
            if words > 100000:
                word_cap_failures.append({"path": path, "words": words})

    detailed = {
        "expected_head": local == expected_final,
        "branch": git("branch", "--show-current") == BRANCH,
        "source_ancestor": run(["git", "merge-base", "--is-ancestor", SOURCE, "HEAD"]).returncode == 0,
        "x1_ancestor": run(["git", "merge-base", "--is-ancestor", X1, "HEAD"]).returncode == 0,
        "evidence_ancestor": run(["git", "merge-base", "--is-ancestor", EVIDENCE, "HEAD"]).returncode == 0,
        "x1_direct_parent": git("rev-parse", f"{X1}^") == SOURCE,
        "evidence_direct_parent": git("rev-parse", f"{EVIDENCE}^") == X1,
        "final_direct_parent": git("rev-parse", "HEAD^") == EVIDENCE,
        "three_phase_commits": int(git("rev-list", "--count", f"{SOURCE}..HEAD")) == 3,
        "zero_merges": int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")) == 0,
        "source_parent_count": parent_count(SOURCE) >= 1,
        "x1_parent_count": parent_count(X1) == 1,
        "evidence_parent_count": parent_count(EVIDENCE) == 1,
        "final_parent_count": parent_count(expected_final) == 1,
        "local_upstream_equal": local == upstream,
        "local_tracking_equal": local == tracking,
        "local_fresh_live_equal": local == fresh_live,
        "zero_divergence": divergence_parts == ["0", "0"],
        "clean_before": clean_before,
        "tests_twenty": tests_run == 20,
        "tests_passed": test.returncode == 0,
        "json_parses": not json_failures,
        "markdown_decodes": not markdown_failures,
        "privacy_zero_confirmed": privacy["confirmed_hit_count"] == 0,
        "python_compile_and_review": python["valid"],
        "all_manifests_replay": all(row["valid"] for row in manifests),
        "final_delta_additive": not forbidden_delta,
        "owner_file_cap": len(owner_paths) <= 2000,
        "document_word_caps": not word_cap_failures,
        "outcomes": truth["outcomes"]
        == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "counts": (
            truth["effective_negatives"],
            truth["effective_methods"],
            truth["failed_witnesses"],
            truth["passing_witnesses"],
            truth["open_gaps"],
            truth["exact_gates"],
        )
        == (33905, 20222, 5726, 7333, 261, 256),
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["delivery_state"] == "PREPARED_NOT_SENT"
        and route["successor_contact_count"] == 0,
        "handoff_integrity": (
            len(
                blob(
                    "docs/caelen-morrow/v671-v3/handoffs/eiren-kestrel-v671-v4-activation-candidate.md"
                )
            )
            == seal["handoff_candidate_bytes_normalized_lf"]
            and sha256(
                blob(
                    "docs/caelen-morrow/v671-v3/handoffs/eiren-kestrel-v671-v4-activation-candidate.md"
                )
            )
            == seal["handoff_candidate_sha256_normalized_lf"]
        ),
    }
    minimal_names = [
        "expected_head",
        "branch",
        "final_direct_parent",
        "three_phase_commits",
        "zero_merges",
        "final_parent_count",
        "local_upstream_equal",
        "local_tracking_equal",
        "local_fresh_live_equal",
        "zero_divergence",
        "clean_before",
        "tests_passed",
        "all_manifests_replay",
        "terminal_verdict",
        "route_prepared_not_sent",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    valid = all(detailed.values()) and all(minimal.values())
    clean_after = not bool(git("status", "--porcelain"))
    valid = valid and clean_after

    payload = {
        "schema": "ghc.family.exact-final-canonical-receipt.v7",
        "result": RESULT if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Caelen Morrow",
        "phase": "v671-v3",
        "exact_final": expected_final,
        "branch": BRANCH,
        "invocation_count": 1,
        "replayed": False,
        "tests": {
            "command": "python -m unittest owner-final-tests",
            "run": tests_run,
            "passed": tests_run if test.returncode == 0 else 0,
            "failed_or_error": 0 if test.returncode == 0 else 1,
            "returncode": test.returncode,
        },
        "detailed_checks": {
            "passed": sum(detailed.values()),
            "total": len(detailed),
            "rows": detailed,
        },
        "minimal_checks": {
            "passed": sum(minimal.values()),
            "total": len(minimal),
            "rows": minimal,
        },
        "json_documents": len(json_paths),
        "json_failures": json_failures,
        "markdown_documents": len(markdown_paths),
        "markdown_failures": markdown_failures,
        "owner_files": len(owner_paths),
        "privacy_scan": privacy,
        "python_review": python,
        "manifest_replays": manifests,
        "manifest_entries_total": sum(row["declared"] for row in manifests),
        "final_delta_paths": len(final_delta),
        "forbidden_final_delta_paths": forbidden_delta,
        "word_cap_failures": word_cap_failures,
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": fresh_live,
        "typed_divergence": {
            "ahead": int(divergence_parts[0]) if len(divergence_parts) == 2 else None,
            "behind": int(divergence_parts[1]) if len(divergence_parts) == 2 else None,
        },
        "clean_before": clean_before,
        "clean_after": clean_after,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "boundary": (
            "This is bounded same-owner owner-scoped validation under shared "
            "infrastructure, not independent reproduction, external audit, "
            "production certification, exhaustive security, complete privacy "
            "or accessibility assurance, professional validation, legal review, "
            "cultural ratification, Maori-authority review, empirical GMUT "
            "confirmation, Theory-of-Everything proof, AGI or ASI evidence, "
            "consciousness or personhood evidence, proof, canon, or Stage 20 authority."
        ),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    canonical_bytes = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    receipt = {
        "payload_sha256": sha256(canonical_bytes),
        "payload": payload,
    }
    atomic_write(receipt_path, receipt)
    if not valid:
        raise SystemExit(json.dumps(receipt, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    validate(args.expected_final, args.receipt)


if __name__ == "__main__":
    main()
