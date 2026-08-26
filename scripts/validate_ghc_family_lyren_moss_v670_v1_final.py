"""One-shot exact-final owner-scoped canonical validator for Lyren v670-v1."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SOURCE = "fe33a3ed69d6144720072b15174937effe9ca305"
X1 = "128f52cee0acc532a114b05242d356cb7a59596c"
EVIDENCE = "4538663ed1e526931056b104fbd86c27629aa223"
BRANCH = "codex/GHC-Family/lyren-moss-v670-v1-full-tools"
OWNER_PREFIX = "docs/lyren-moss/v670-v1/"
EXPECTED_COUNTS = {
    "effective_negatives": 32057,
    "methods": 18162,
    "failed_witnesses": 3878,
    "passing_witnesses": 5131,
    "open_gaps": 241,
    "exact_gates": 236,
}


def command(
    repo: Path,
    *args: str,
    check: bool = True,
    binary: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        args,
        cwd=repo,
        check=check,
        capture_output=True,
        text=not binary,
        env=env,
    )


def git(
    repo: Path, *args: str, check: bool = True, binary: bool = False
) -> subprocess.CompletedProcess[Any]:
    return command(repo, "git", *args, check=check, binary=binary)


def blob(repo: Path, commit: str, path: str) -> bytes:
    return git(repo, "show", f"{commit}:{path}", binary=True).stdout


def replay_manifest(repo: Path, commit: str, path: str) -> dict[str, Any]:
    manifest = json.loads(blob(repo, commit, path).decode("utf-8"))
    mismatches = []
    for entry in manifest["entries"]:
        data = blob(repo, commit, entry["path"])
        if (
            len(data) != entry["bytes"]
            or hashlib.sha256(data).hexdigest() != entry["sha256"]
        ):
            mismatches.append(entry["path"])
    return {
        "path": path,
        "commit": commit,
        "declared": manifest["entry_count"],
        "replayed": len(manifest["entries"]),
        "mismatches": mismatches,
    }


def privacy_scan(repo: Path, head: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "private_absolute_path": re.compile(r"(?i)(?:[a-z]:\\users\\|[a-z]:\\ghc-archives\\)"),
        "raw_task_or_thread_identifier": re.compile(
            r"\b019[0-9a-f]{5,}(?:-[0-9a-f]{4,}){2,}\b", re.IGNORECASE
        ),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"]+"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(?:resume[_-]?value|session[_-]?stream)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_callable_or_application_state": re.compile(
            r"(?i)(?:private[_-]?callable[_-]?id|private[_-]?app[_-]?state)\s*[:=]\s*['\"][^'\"]+"
        ),
    }
    candidates = []
    scanned = 0
    for path in paths:
        if not path.startswith(OWNER_PREFIX):
            continue
        if Path(path).suffix.lower() not in {".json", ".md", ".html", ".txt"}:
            continue
        text = blob(repo, head, path).decode("utf-8")
        scanned += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append(
                    {"class": class_name, "path": path, "offset": match.start()}
                )
    return {
        "classes": list(patterns),
        "files_scanned": scanned,
        "candidates": candidates,
        "confirmed_hits": len(candidates),
    }


def security_review(repo: Path, head: str, paths: list[str]) -> dict[str, Any]:
    python_paths = [
        path
        for path in paths
        if path.endswith(".py")
        and (
            "lyren_moss_v670_v1" in path
            or path.startswith("scripts/ghc_family_grain_milling_")
        )
    ]
    findings = []
    for path in python_paths:
        tree = ast.parse(blob(repo, head, path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append(
                    {"path": path, "line": node.lineno, "kind": node.func.id}
                )
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "system"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
            ):
                findings.append(
                    {"path": path, "line": node.lineno, "kind": "os.system"}
                )
            for keyword in node.keywords:
                if (
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ):
                    findings.append(
                        {"path": path, "line": node.lineno, "kind": "shell_true"}
                    )
    return {
        "files_reviewed": len(python_paths),
        "finding_count": len(findings),
        "findings": findings,
    }


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    receipt_text = os.environ.get("LM6701_CANONICAL_RECEIPT")
    if not receipt_text:
        raise SystemExit("LM6701_CANONICAL_RECEIPT is required")
    receipt = Path(receipt_text)
    if receipt.exists():
        raise SystemExit("canonical receipt already exists; replay refused")
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    try:
        head = git(repo, "rev-parse", "HEAD").stdout.strip()
        branch = git(repo, "branch", "--show-current").stdout.strip()
        clean_before = git(repo, "status", "--porcelain=v1").stdout == ""
        parent = git(repo, "rev-parse", "HEAD^").stdout.strip()
        check("exact branch", branch == BRANCH, branch)
        check("final direct parent is evidence", parent == EVIDENCE, parent)
        check(
            "x1 direct parent is source",
            git(repo, "rev-parse", f"{X1}^").stdout.strip() == SOURCE,
        )
        check(
            "evidence direct parent is x1",
            git(repo, "rev-parse", f"{EVIDENCE}^").stdout.strip() == X1,
        )
        commits = git(repo, "rev-list", "--reverse", f"{SOURCE}..{head}").stdout.splitlines()
        merges = git(repo, "rev-list", "--merges", f"{SOURCE}..{head}").stdout.splitlines()
        parent_counts = [
            len(
                git(repo, "rev-list", "--parents", "-n", "1", commit).stdout.split()
            )
            - 1
            for commit in commits
        ]
        check("exactly three phase commits", len(commits) == 3, commits)
        check("zero phase merges", not merges, merges)
        check("one parent per phase commit", parent_counts == [1, 1, 1], parent_counts)
        check("exact lifecycle order", commits == [X1, EVIDENCE, head], commits)
        check("clean before canonical", clean_before)

        paths = git(repo, "ls-tree", "-r", "--name-only", head).stdout.splitlines()
        owner_paths = [path for path in paths if path.startswith(OWNER_PREFIX)]
        changed = git(repo, "diff", "--name-only", SOURCE, head).stdout.splitlines()
        disallowed = [
            path
            for path in changed
            if not (
                path.startswith(OWNER_PREFIX)
                or path == "ghc-family-index/references/v670-v1-lyren-moss.md"
                or (
                    path.startswith("scripts/")
                    and (
                        "lyren_moss_v670_v1" in path
                        or path.startswith("scripts/ghc_family_grain_milling_")
                    )
                )
                or (path.startswith("tests/") and "lyren_moss_v670_v1" in path)
            )
        ]
        check("owner scope only", not disallowed, disallowed)
        check("owner file ceiling", len(owner_paths) <= 2000, len(owner_paths))

        json_failures = []
        utf8_failures = []
        max_words = 0
        max_word_path = None
        for path in owner_paths:
            if Path(path).suffix.lower() not in {".json", ".md", ".html", ".txt"}:
                continue
            data = blob(repo, head, path)
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                utf8_failures.append(path)
                continue
            words = len(text.split())
            if words > max_words:
                max_words = words
                max_word_path = path
            if path.endswith(".json"):
                try:
                    json.loads(text)
                except json.JSONDecodeError:
                    json_failures.append(path)
        check(
            "all owner JSON parses",
            not json_failures,
            {
                "parsed": sum(path.endswith(".json") for path in owner_paths),
                "failures": json_failures,
            },
        )
        check("all owner text UTF-8", not utf8_failures, utf8_failures)
        check(
            "document word ceiling",
            max_words <= 100000,
            {"max_words": max_words, "path": max_word_path},
        )

        manifests = [
            replay_manifest(
                repo,
                X1,
                OWNER_PREFIX + "validation/x1-manifest.json",
            ),
            replay_manifest(
                repo,
                EVIDENCE,
                OWNER_PREFIX + "validation/evidence-manifest.json",
            ),
            replay_manifest(
                repo,
                head,
                OWNER_PREFIX + "validation/final-delta-manifest.json",
            ),
            replay_manifest(
                repo,
                head,
                OWNER_PREFIX + "validation/final-owner-manifest.json",
            ),
        ]
        check(
            "all commit-local manifests replay",
            all(not item["mismatches"] for item in manifests),
            manifests,
        )

        privacy = privacy_scan(repo, head, owner_paths)
        security = security_review(repo, head, paths)
        check("five-class privacy scan", privacy["confirmed_hits"] == 0, privacy)
        check(
            "bounded Python security review",
            security["finding_count"] == 0,
            security,
        )

        integrity = json.loads(
            blob(
                repo,
                head,
                OWNER_PREFIX + "handoffs/activation-candidate-integrity.json",
            ).decode("utf-8")
        )
        baton_data = blob(repo, head, integrity["path"])
        check(
            "baton exact integrity",
            len(baton_data) == integrity["bytes"]
            and hashlib.sha256(baton_data).hexdigest() == integrity["sha256"],
        )
        check("baton word bounds", 10000 <= integrity["words"] <= 100000, integrity["words"])
        check(
            "baton prepared not sent",
            integrity["state"] == "PREPARED_NOT_SENT"
            and integrity["sent_by_lyren_moss"] is False,
            integrity,
        )
        route = json.loads(
            blob(
                repo,
                head,
                OWNER_PREFIX + "orchestration/route-state-final-candidate.json",
            ).decode("utf-8")
        )
        check(
            "route prepared not sent",
            route["state"] == "PREPARED_NOT_SENT"
            and route["successor_contacted"] is False
            and route["standby_contacted"] is False,
            route,
        )
        truth = json.loads(
            blob(repo, head, OWNER_PREFIX + "closeout/phase-truth.json").decode("utf-8")
        )
        check(
            "final counts exact",
            all(truth[key] == value for key, value in EXPECTED_COUNTS.items()),
            {key: truth[key] for key in EXPECTED_COUNTS},
        )
        check(
            "four outcome labels exact",
            truth["outcomes"]
            == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            truth["outcomes"],
        )
        check(
            "terminal verdict protected",
            truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        )

        phase_python = [
            path
            for path in paths
            if path.endswith(".py")
            and (
                "lyren_moss_v670_v1" in path
                or path.startswith("scripts/ghc_family_grain_milling_")
            )
        ]
        run_env = dict(os.environ)
        run_env["PYTHONDONTWRITEBYTECODE"] = "1"
        ruff = command(
            repo,
            sys.executable,
            "-B",
            "-m",
            "ruff",
            "check",
            *phase_python,
            check=False,
            env=run_env,
        )
        check(
            "owner Python Ruff",
            ruff.returncode == 0,
            {"files": len(phase_python), "stdout": ruff.stdout[-1200:], "stderr": ruff.stderr[-1200:]},
        )
        pytest = command(
            repo,
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "tests/test_ghc_family_lyren_moss_v670_v1_x1.py",
            "tests/test_ghc_family_lyren_moss_v670_v1_x2.py",
            "tests/test_ghc_family_lyren_moss_v670_v1_final.py",
            "-k",
            "not test_x1_before_x2_absence_gate and not test_no_final_closeout_or_handoff_exists_at_evidence_stage",
            "-p",
            "no:cacheprovider",
            check=False,
            env=run_env,
        )
        check(
            "owner-scoped pytest",
            pytest.returncode == 0,
            {"stdout_tail": pytest.stdout[-1600:], "stderr_tail": pytest.stderr[-1600:]},
        )

        staged_review = json.loads(
            blob(
                repo,
                head,
                OWNER_PREFIX + "validation/final-staged-review.json",
            ).decode("utf-8")
        )
        check(
            "final staged review exact allowlist",
            staged_review["disallowed_paths"] == []
            and staged_review["x1_and_evidence_immutable"] is True,
            staged_review,
        )

        fetch = git(
            repo,
            "fetch",
            "--no-tags",
            "origin",
            f"refs/heads/{BRANCH}",
            check=False,
        )
        check("fresh live fetch", fetch.returncode == 0, fetch.stderr)
        local = git(repo, "rev-parse", "HEAD").stdout.strip()
        upstream = git(repo, "rev-parse", "@{u}").stdout.strip()
        tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.strip()
        live = git(repo, "rev-parse", "FETCH_HEAD").stdout.strip()
        divergence = git(
            repo, "rev-list", "--left-right", "--count", "HEAD...@{u}"
        ).stdout.split()
        check(
            "fresh four-way equality",
            local == upstream == tracking == live,
            {
                "local": local,
                "upstream": upstream,
                "tracking": tracking,
                "fresh_live": live,
            },
        )
        check("zero divergence", divergence == ["0", "0"], divergence)
        clean_after = git(repo, "status", "--porcelain=v1").stdout == ""
        check("clean after canonical", clean_after)
        check("exact head stable", local == head, {"initial": head, "final": local})

        passed = all(item["passed"] for item in checks)
        payload = {
            "schema": "ghc.family.exact-final-canonical-receipt.v4",
            "owner": "Lyren Moss",
            "phase": "v670-v1",
            "result": (
                "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
                if passed
                else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
            ),
            "success": passed,
            "attempt": 1,
            "replayed": False,
            "exact_head": head,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "check_count": len(checks),
            "passed_checks": sum(item["passed"] for item in checks),
            "failed_checks": [item for item in checks if not item["passed"]],
            "checks": checks,
            "manifest_entries": sum(item["declared"] for item in manifests),
            "json_documents": sum(path.endswith(".json") for path in owner_paths),
            "privacy_files": privacy["files_scanned"],
            "privacy_confirmed_hits": privacy["confirmed_hits"],
            "python_files_reviewed": security["files_reviewed"],
            "full_repository_suite": "not_run_not_claimed",
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        atomic_write(receipt, payload)
        print(
            json.dumps(
                {
                    key: payload[key]
                    for key in [
                        "result",
                        "success",
                        "exact_head",
                        "check_count",
                        "passed_checks",
                        "manifest_entries",
                        "json_documents",
                        "privacy_files",
                    ]
                },
                sort_keys=True,
            )
        )
        return 0 if passed else 1
    except Exception as exc:  # noqa: BLE001 - one-shot failure still receives an atomic receipt
        payload = {
            "schema": "ghc.family.exact-final-canonical-receipt.v4",
            "owner": "Lyren Moss",
            "phase": "v670-v1",
            "result": "CANONICAL_EXCEPTION_ZERO_SUCCESS_CREDIT",
            "success": False,
            "attempt": 1,
            "replayed": False,
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "checks": checks,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        atomic_write(receipt, payload)
        print(
            json.dumps(
                {
                    "result": payload["result"],
                    "success": False,
                    "exception_type": payload["exception_type"],
                },
                sort_keys=True,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
