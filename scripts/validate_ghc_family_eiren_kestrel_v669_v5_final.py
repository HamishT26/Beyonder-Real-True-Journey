"""One-shot exact-final owner-scoped canonical validator for Eiren v669-v5."""

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

SOURCE = "0fc4f78f4da5fcaa8d990b6e81696404c9bca2f9"
X1 = "df7c773867b15aec8fa7ffa4cc956a134fa9c4be"
EVIDENCE = "b52b74bee55d3fdc6eb73058f15360da089f8ac5"
BRANCH = "codex/GHC-Family/eiren-kestrel-v669-v5-full-tools"
OWNER_PREFIX = "docs/eiren-kestrel/v669-v5/"


def command(repo: Path, *args: str, check: bool = True, binary: bool = False):
    return subprocess.run(args, cwd=repo, check=check, capture_output=True, text=not binary)


def git(repo: Path, *args: str, check: bool = True, binary: bool = False):
    return command(repo, "git", *args, check=check, binary=binary)


def blob(repo: Path, commit: str, path: str) -> bytes:
    return git(repo, "show", f"{commit}:{path}", binary=True).stdout


def replay_manifest(repo: Path, commit: str, path: str) -> dict[str, Any]:
    manifest = json.loads(blob(repo, commit, path).decode("utf-8"))
    mismatches = []
    for entry in manifest["entries"]:
        data = blob(repo, commit, entry["path"])
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    return {"path": path, "commit": commit, "declared": manifest["entry_count"], "replayed": len(manifest["entries"]), "mismatches": mismatches}


def privacy_scan(repo: Path, head: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "private_absolute_path": re.compile(r"(?i)(?:[a-z]:\\users\\|[a-z]:\\ghc-archives\\)"),
        "raw_task_or_thread_identifier": re.compile(r"\b019[0-9a-f]{5,}(?:-[0-9a-f]{4,}){2,}\b", re.IGNORECASE),
        "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"]+"),
        "transcript_or_session_stream": re.compile(r"(?i)(?:resume[_-]?value|session[_-]?stream)\s*[:=]\s*['\"][^'\"]+"),
        "private_callable_or_application_state": re.compile(r"(?i)(?:private[_-]?callable[_-]?id|private[_-]?app[_-]?state)\s*[:=]\s*['\"][^'\"]+"),
    }
    hits = []
    scanned = 0
    for path in paths:
        if not path.startswith(OWNER_PREFIX) or Path(path).suffix.lower() not in {".json", ".md", ".html", ".txt"}:
            continue
        text = blob(repo, head, path).decode("utf-8")
        scanned += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"class": class_name, "path": path, "offset": match.start()})
    return {"classes": list(patterns), "files_scanned": scanned, "candidates": hits, "confirmed_hits": len(hits)}


def security_review(repo: Path, head: str, paths: list[str]) -> dict[str, Any]:
    py_paths = [path for path in paths if path.endswith(".py") and ("eiren_kestrel_v669_v5" in path or path.startswith("scripts/ghc_family_apiary_"))]
    findings = []
    for path in py_paths:
        tree = ast.parse(blob(repo, head, path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            if isinstance(node.func, ast.Attribute) and node.func.attr == "system" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                findings.append({"path": path, "line": node.lineno, "kind": "os.system"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "kind": "shell_true"})
    return {"files_reviewed": len(py_paths), "finding_count": len(findings), "findings": findings}


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    receipt = Path(os.environ["EK6695_CANONICAL_RECEIPT"])
    if receipt.exists():
        raise SystemExit("canonical receipt already exists; replay refused")
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    try:
        head = git(repo, "rev-parse", "HEAD").stdout.strip()
        clean_before = git(repo, "status", "--porcelain=v1").stdout == ""
        parent = git(repo, "rev-parse", "HEAD^").stdout.strip()
        check("final direct parent is evidence", parent == EVIDENCE, parent)
        check("x1 direct parent is source", git(repo, "rev-parse", f"{X1}^").stdout.strip() == SOURCE)
        check("evidence direct parent is x1", git(repo, "rev-parse", f"{EVIDENCE}^").stdout.strip() == X1)
        commits = git(repo, "rev-list", "--reverse", f"{SOURCE}..{head}").stdout.splitlines()
        merges = git(repo, "rev-list", "--merges", f"{SOURCE}..{head}").stdout.splitlines()
        parent_counts = [len(git(repo, "rev-list", "--parents", "-n", "1", commit).stdout.split()) - 1 for commit in commits]
        check("exactly three phase commits", len(commits) == 3, commits)
        check("zero phase merges", not merges, merges)
        check("one parent per phase commit", parent_counts == [1, 1, 1], parent_counts)
        check("exact lifecycle order", commits == [X1, EVIDENCE, head], commits)
        check("clean before canonical", clean_before)

        paths = git(repo, "ls-tree", "-r", "--name-only", head).stdout.splitlines()
        owner_paths = [path for path in paths if path.startswith(OWNER_PREFIX)]
        changed = git(repo, "diff", "--name-only", SOURCE, head).stdout.splitlines()
        disallowed = [path for path in changed if not (path.startswith(OWNER_PREFIX) or (path.startswith("scripts/") and ("eiren_kestrel_v669_v5" in path or path.startswith("scripts/ghc_family_apiary_"))) or (path.startswith("tests/") and "eiren_kestrel_v669_v5" in path))]
        check("owner scope only", not disallowed, disallowed)
        check("owner file ceiling", len(owner_paths) <= 2000, len(owner_paths))

        json_failures = []
        markdown_failures = []
        max_words = 0
        max_word_path = None
        for path in owner_paths:
            suffix = Path(path).suffix.lower()
            if suffix not in {".json", ".md", ".html", ".txt"}:
                continue
            data = blob(repo, head, path)
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                markdown_failures.append(path)
                continue
            words = len(text.split())
            if words > max_words:
                max_words, max_word_path = words, path
            if suffix == ".json":
                try:
                    json.loads(text)
                except json.JSONDecodeError:
                    json_failures.append(path)
        check("all owner JSON parses", not json_failures, {"parsed": sum(path.endswith('.json') for path in owner_paths), "failures": json_failures})
        check("all owner text UTF-8", not markdown_failures, markdown_failures)
        check("document word ceiling", max_words <= 100000, {"max_words": max_words, "path": max_word_path})

        manifests = [
            replay_manifest(repo, X1, "docs/eiren-kestrel/v669-v5/validation/x1-manifest.json"),
            replay_manifest(repo, EVIDENCE, "docs/eiren-kestrel/v669-v5/validation/evidence-delta-manifest.json"),
            replay_manifest(repo, EVIDENCE, "docs/eiren-kestrel/v669-v5/validation/evidence-owner-manifest.json"),
            replay_manifest(repo, head, "docs/eiren-kestrel/v669-v5/validation/final-delta-manifest.json"),
            replay_manifest(repo, head, "docs/eiren-kestrel/v669-v5/validation/final-owner-manifest.json"),
        ]
        check("all commit-local manifests replay", all(not item["mismatches"] for item in manifests), manifests)

        privacy = privacy_scan(repo, head, owner_paths)
        security = security_review(repo, head, paths)
        check("five-class privacy scan", privacy["confirmed_hits"] == 0, privacy)
        check("bounded Python security review", security["finding_count"] == 0, security)

        baton_integrity = json.loads(blob(repo, head, OWNER_PREFIX + "handoffs/activation-candidate-integrity.json"))
        baton_data = blob(repo, head, baton_integrity["path"])
        check("baton exact integrity", len(baton_data) == baton_integrity["bytes"] and hashlib.sha256(baton_data).hexdigest() == baton_integrity["sha256"])
        check("baton word bounds", 10000 <= baton_integrity["words"] <= 100000, baton_integrity["words"])
        route = json.loads(blob(repo, head, OWNER_PREFIX + "orchestration/route-state-final-candidate.json"))
        check("route prepared not sent", route["state"] == "PREPARED_NOT_SENT" and not route["successor_contacted"] and not route["standby_contacted"], route)

        x2_nodeids = [
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_exact_outcomes_positive_controls_and_mutations",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_truth_counts_and_nonpromotion",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_flashcards_have_four_tiers_and_ten_sections",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_portfolios_and_held_packets",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_skills_runners_and_core_skill_uses",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_installed_suite_and_target_three_receipts",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_method_flow_retains_x2_failures_and_mutations",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_runners_compile_without_cache_write",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_evidence_manifests_replay_exact_git_blobs",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x2.py::test_bounded_privacy_security_and_accessibility_receipts",
        ]
        final_module = "tests/test_ghc_family_eiren_kestrel_v669_v5_final.py"
        pytest = command(repo, sys.executable, "-m", "pytest", "-q", *x2_nodeids, final_module, "-p", "no:cacheprovider", check=False)
        check("owner-scoped pytest", pytest.returncode == 0, {"selected_x2": len(x2_nodeids), "final_module": final_module, "stdout_tail": pytest.stdout[-1200:], "stderr_tail": pytest.stderr[-1200:]})

        final_review = json.loads(blob(repo, head, OWNER_PREFIX + "validation/final-staged-review.json"))
        check("final staged review exact allowlist", final_review["disallowed_paths"] == [] and final_review["x1_and_evidence_immutable"] is True, final_review)
        stale_patterns = [
            re.compile(r"audiovisual-preservation", re.IGNORECASE),
            re.compile(r"ghc_family_audio_", re.IGNORECASE),
            re.compile(r"Eiren Kestrel v669-v5 to (?:the existing exact-title )?Eiren Kestrel", re.IGNORECASE),
        ]
        stale = [
            path
            for path in owner_paths
            if any(pattern.search(blob(repo, head, path).decode("utf-8", errors="ignore")) for pattern in stale_patterns)
        ]
        check("no stale domain or self-route labels", not stale, stale)

        fetch = git(repo, "fetch", "--no-tags", "origin", f"refs/heads/{BRANCH}", check=False)
        check("fresh live fetch", fetch.returncode == 0, fetch.stderr)
        local = git(repo, "rev-parse", "HEAD").stdout.strip()
        upstream = git(repo, "rev-parse", "@{u}").stdout.strip()
        tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.strip()
        live = git(repo, "rev-parse", "FETCH_HEAD").stdout.strip()
        divergence = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.split()
        check("fresh four-way equality", local == upstream == tracking == live, {"local": local, "upstream": upstream, "tracking": tracking, "fresh_live": live})
        check("zero divergence", divergence == ["0", "0"], divergence)
        clean_after = git(repo, "status", "--porcelain=v1").stdout == ""
        check("clean after canonical", clean_after)
        check("exact head stable", local == head, {"initial": head, "final": local})

        passed = all(item["passed"] for item in checks)
        payload = {
            "schema": "ghc.family.exact-final-canonical-receipt.v3",
            "owner": "Eiren Kestrel",
            "phase": "v669-v5",
            "result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if passed else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
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
            "full_repository_suite": "not_run_no_current_exact_requirement",
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        atomic_write(receipt, payload)
        print(json.dumps({key: payload[key] for key in ["result", "success", "exact_head", "check_count", "passed_checks", "manifest_entries", "json_documents", "privacy_files"]}, sort_keys=True))
        return 0 if passed else 1
    except Exception as exc:  # noqa: BLE001 - an unexpected one-shot failure must still produce its atomic receipt
        payload = {
            "schema": "ghc.family.exact-final-canonical-receipt.v3",
            "owner": "Eiren Kestrel",
            "phase": "v669-v5",
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
        print(json.dumps({"result": payload["result"], "success": False, "exception_type": payload["exception_type"]}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
