"""One-shot exact-final owner-scoped validator for Vesper Arlen v668-v1.

The command writes an external invocation state before validation.  A second
invocation with the same state path is refused, regardless of the first result.
It never labels a corrected dependency composite as canonical success.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = "docs/vesper-arlen/v668-v1"
PHASE = ROOT / PHASE_REL
BRANCH = "codex/GHC-Family/vesper-arlen-v668-v1-full-tools"
SOURCE = "fa6bdcedaac48b0580f4d9581b799741cf5282e7"
X1 = "3e9bf7e7fa9ee1164b77616e09f93127d3b43fd5"
EVIDENCE = "9f1feed93e4b33c8fcb82f0cd818cac8a5594337"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {args[0]} {result.stderr.decode('utf-8', 'replace')[:500]}")
    return result


def git_text(*args: str) -> str:
    return run(["git", *args]).stdout.decode("utf-8", "replace").strip()


class GitBatch:
    def __init__(self) -> None:
        self.process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _read_exact(self, size: int) -> bytes:
        chunks: list[bytes] = []
        remaining = size
        assert self.process.stdout is not None
        while remaining:
            piece = self.process.stdout.read(remaining)
            if not piece:
                raise RuntimeError(f"git batch ended with {remaining} bytes remaining")
            chunks.append(piece)
            remaining -= len(piece)
        return b"".join(chunks)

    def blob(self, spec: str) -> bytes:
        assert self.process.stdin is not None and self.process.stdout is not None
        self.process.stdin.write(spec.encode("utf-8") + b"\n")
        self.process.stdin.flush()
        header = self.process.stdout.readline().decode("utf-8", "replace").rstrip("\n")
        parts = header.split()
        if len(parts) >= 2 and parts[1] == "missing":
            raise KeyError(spec)
        if len(parts) < 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected git batch header: {header}")
        data = self._read_exact(int(parts[2]))
        if self._read_exact(1) != b"\n":
            raise RuntimeError("bad git batch trailer")
        return data

    def close(self) -> None:
        if self.process.stdin:
            self.process.stdin.close()
        if self.process.stdout:
            self.process.stdout.close()
        self.process.terminate()


def owner_paths(commit: str) -> list[str]:
    paths = git_text("ls-tree", "-r", "--name-only", commit).splitlines()
    return sorted(path for path in paths if path.startswith(f"{PHASE_REL}/") or ("vesper_arlen_v668_v1" in Path(path).name and (path.startswith("scripts/") or path.startswith("tests/"))))


def parse_owner_json(commit: str, paths: list[str], batch: GitBatch) -> tuple[int, list[str]]:
    failures = []
    count = 0
    for path in paths:
        if path.endswith(".json"):
            try:
                json.loads(batch.blob(f"{commit}:{path}").decode("utf-8"))
                count += 1
            except Exception as exc:
                failures.append(f"{path}: {type(exc).__name__}")
    return count, failures


def replay_manifest(commit: str, manifest_path: str, batch: GitBatch) -> dict[str, Any]:
    manifest = json.loads(batch.blob(f"{commit}:{manifest_path}").decode("utf-8"))
    failures = []
    for row in manifest["entries"]:
        try:
            data = batch.blob(f"{commit}:{row['path']}")
        except Exception as exc:
            failures.append({"path": row["path"], "error": type(exc).__name__})
            continue
        actual = hashlib.sha256(data).hexdigest()
        if actual != row["sha256"] or len(data) != row["bytes"]:
            failures.append({"path": row["path"], "expected_sha256": row["sha256"], "actual_sha256": actual, "expected_bytes": row["bytes"], "actual_bytes": len(data)})
    return {"path": manifest_path, "entries": len(manifest["entries"]), "failures": failures, "passed": len(manifest["entries"]) - len(failures)}


def privacy_scan(commit: str, paths: list[str], batch: GitBatch) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*[\"'][^\"']{4,}"),
        "raw_task_thread_session_id": re.compile(r"(?i)\b(task|thread|session|resume)[_-]?id\b\s*[:=]\s*[\"']?[A-Za-z0-9_-]{12,}"),
        "private_scheme": re.compile(r"(?i)\b(codex|app|plugin)://"),
    }
    text_suffixes = {".json", ".md", ".txt", ".py", ".html", ".css", ".js", ".mjs", ".cjs"}
    hits = []
    scanned = 0
    for path in paths:
        if Path(path).suffix.lower() not in text_suffixes:
            continue
        scanned += 1
        text = batch.blob(f"{commit}:{path}").decode("utf-8", "replace")
        for name, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path, "class": name})
    return {"files": scanned, "classes": len(patterns), "hits": hits}


def ast_security(commit: str, paths: list[str], batch: GitBatch) -> dict[str, Any]:
    findings = []
    parsed = 0
    for path in paths:
        if not path.endswith(".py"):
            continue
        source = batch.blob(f"{commit}:{path}").decode("utf-8")
        tree = ast.parse(source, filename=path)
        parsed += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name in {"eval", "exec", "rmtree"}:
                    findings.append({"path": path, "line": node.lineno, "kind": name})
                if isinstance(node.func, ast.Attribute) and node.func.attr == "system" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    findings.append({"path": path, "line": node.lineno, "kind": "os.system"})
                if name in {"run", "Popen", "call", "check_call", "check_output"} and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    findings.append({"path": path, "line": node.lineno, "kind": "shell_true"})
    return {"python_files": parsed, "findings": findings}


def check_words(commit: str, paths: list[str], batch: GitBatch) -> dict[str, Any]:
    failures = []
    baton_words = None
    for path in paths:
        if Path(path).suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        words = len(batch.blob(f"{commit}:{path}").decode("utf-8", "replace").split())
        if path.endswith("handoffs/lyren-moss-v668-v2-activation-prepared.md"):
            baton_words = words
            if not 10_000 <= words <= 100_000:
                failures.append({"path": path, "words": words, "rule": "handoff_10000_to_100000"})
        elif words > 6000:
            failures.append({"path": path, "words": words, "rule": "document_at_most_6000"})
    return {"baton_words": baton_words, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--state-file", type=Path, required=True)
    parser.add_argument("--receipt-file", type=Path, required=True)
    args = parser.parse_args()
    if args.state_file.exists() or args.receipt_file.exists():
        raise SystemExit("one-shot state or receipt already exists; replay refused")
    args.state_file.parent.mkdir(parents=True, exist_ok=True)
    invocation = {"state": "INVOKED_NOT_YET_CREDITED", "invoked_at": now(), "expected_head": args.expected_head, "canonical_success_credit": 0, "replay": False}
    args.state_file.write_text(json.dumps(invocation, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")

    batch = GitBatch()
    try:
        branch = git_text("branch", "--show-current")
        head = git_text("rev-parse", "HEAD")
        upstream = git_text("rev-parse", "@{u}")
        tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
        live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
        live = live_line.split()[0] if live_line else ""
        clean_before = not git_text("status", "--porcelain=v1")
        if branch != BRANCH or head != args.expected_head:
            raise RuntimeError("branch or exact head mismatch")
        if len({head, upstream, tracking, live}) != 1:
            raise RuntimeError("four-way equality mismatch")
        if not clean_before:
            raise RuntimeError("canonical tree not clean before validation")

        phase_commits = int(git_text("rev-list", "--count", f"{SOURCE}..{head}"))
        merges = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
        parent = git_text("show", "-s", "--format=%P", head)
        ancestry = {
            "source_to_x1": run(["git", "merge-base", "--is-ancestor", SOURCE, X1], check=False).returncode == 0,
            "x1_to_evidence": run(["git", "merge-base", "--is-ancestor", X1, EVIDENCE], check=False).returncode == 0,
            "evidence_to_final": run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], check=False).returncode == 0,
        }
        if phase_commits != 3 or merges != 0 or parent != EVIDENCE or not all(ancestry.values()):
            raise RuntimeError("lifecycle history mismatch")

        pytest_result = run([sys.executable, "-m", "pytest", "-q", "tests/test_ghc_family_vesper_arlen_v668_v1_x1.py", "tests/test_ghc_family_vesper_arlen_v668_v1_x2.py", "tests/test_ghc_family_vesper_arlen_v668_v1_final.py"])
        pytest_text = (pytest_result.stdout + pytest_result.stderr).decode("utf-8", "replace")
        match = re.search(r"(\d+) passed", pytest_text)
        if not match:
            raise RuntimeError("pytest pass count absent")
        test_count = int(match.group(1))

        paths = owner_paths(head)
        if len(paths) >= 2000:
            raise RuntimeError("owner file ceiling reached")
        json_count, json_failures = parse_owner_json(head, paths, batch)
        if json_failures:
            raise RuntimeError(f"JSON failures: {json_failures[:3]}")
        privacy = privacy_scan(head, paths, batch)
        if privacy["hits"]:
            raise RuntimeError(f"privacy hits: {privacy['hits'][:3]}")
        security = ast_security(head, paths, batch)
        if security["findings"]:
            raise RuntimeError(f"security findings: {security['findings'][:3]}")
        word_check = check_words(head, paths, batch)
        if word_check["failures"]:
            raise RuntimeError(f"word bound failures: {word_check['failures'][:3]}")

        manifests = [
            replay_manifest(X1, f"{PHASE_REL}/validation/x1-content-manifest.json", batch),
            replay_manifest(EVIDENCE, f"{PHASE_REL}/validation/evidence-content-manifest.json", batch),
            replay_manifest(head, f"{PHASE_REL}/validation/final-delta-manifest.json", batch),
            replay_manifest(head, f"{PHASE_REL}/validation/final-owner-manifest.json", batch),
        ]
        if any(row["failures"] for row in manifests):
            raise RuntimeError("manifest replay mismatch")

        outcomes = json.loads(batch.blob(f"{head}:{PHASE_REL}/x2/proposals/proposal-outcomes.json").decode("utf-8"))
        outcome_counts = Counter(row["outcome"] for row in outcomes["outcomes"])
        if set(outcome_counts) != ALLOWED or outcome_counts != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
            raise RuntimeError("outcome vocabulary or distribution mismatch")
        mutations = json.loads(batch.blob(f"{head}:{PHASE_REL}/x2/proposals/negative-mutation-results.json").decode("utf-8"))
        if mutations["count"] != 100 or not mutations["all_rejected"] or not mutations["all_retained"]:
            raise RuntimeError("mutation truth mismatch")
        html = batch.blob(f"{head}:{PHASE_REL}/reports/static-report.html").decode("utf-8")
        accessibility = all(fragment in html for fragment in ["<main>", "<nav aria-label=", "role=\"status\"", "<caption>", "scope=\"col\"", "@media print"])
        if not accessibility:
            raise RuntimeError("structural accessibility contract missing")

        detailed = [
            branch == BRANCH, head == args.expected_head, head == upstream, head == tracking, head == live, clean_before,
            phase_commits == 3, merges == 0, parent == EVIDENCE, *ancestry.values(), test_count >= 1, json_count >= 1,
            not json_failures, privacy["files"] == len(paths), not privacy["hits"], security["python_files"] >= 1, not security["findings"],
            word_check["baton_words"] is not None, not word_check["failures"], len(paths) < 2000, len(manifests) == 4,
            all(not row["failures"] for row in manifests), all(row["passed"] == row["entries"] for row in manifests),
            outcome_counts["completed"] == 14, outcome_counts["represented"] == 4, outcome_counts["open_gap"] == 1,
            outcome_counts["exact_gate"] == 1, mutations["count"] == 100, mutations["all_rejected"], mutations["all_retained"],
            accessibility, "NOT_READY_FOR_STAGE_20" in html, ("independent reproduction" in html or "independent-reproduction" in html), "complete accessibility conformance" not in html.casefold(),
        ]
        if not all(detailed):
            raise RuntimeError("detailed check false")
        minimal = [head == args.expected_head, head == live, clean_before, phase_commits == 3, merges == 0, parent == EVIDENCE, test_count > 0, not json_failures, not privacy["hits"], not security["findings"], all(not row["failures"] for row in manifests), set(outcome_counts) == ALLOWED, mutations["all_rejected"], accessibility, len(paths) < 2000]
        if not all(minimal):
            raise RuntimeError("minimal check false")

        clean_after = not git_text("status", "--porcelain=v1")
        if not clean_after:
            raise RuntimeError("canonical tree not clean after validation")
        receipt = {
            "state": "VALID_OWNER_SCOPED_CANONICAL_SUCCESS_ONCE",
            "canonical_invocation_count": 1,
            "canonical_success_count": 1,
            "canonical_replayed": False,
            "head": head,
            "branch": branch,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "phase_commits": phase_commits,
            "merges": merges,
            "parent": parent,
            "four_way_equal": True,
            "divergence": [0, 0],
            "clean_before": clean_before,
            "clean_after": clean_after,
            "tests_passed": test_count,
            "detailed_checks": {"passed": sum(detailed), "total": len(detailed)},
            "minimal_checks": {"passed": sum(minimal), "total": len(minimal)},
            "json_parses": json_count,
            "privacy": privacy,
            "security": security,
            "owner_files": len(paths),
            "manifests": manifests,
            "baton_words": word_check["baton_words"],
            "outcomes": dict(outcome_counts),
            "mutations_rejected": mutations["count"],
            "accessibility_structural": True,
            "full_repository_suite": False,
            "independent_reproduction": False,
            "external_audit": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "finished_at": now(),
        }
        payload = (json.dumps(receipt, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        args.receipt_file.parent.mkdir(parents=True, exist_ok=True)
        args.receipt_file.write_bytes(payload)
        args.state_file.write_text(json.dumps({"state": "SUCCESSFUL_ONCE_REPLAY_REFUSED", "head": head, "receipt_sha256": hashlib.sha256(payload).hexdigest(), "canonical_success_credit": 1, "replay": False}, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({**receipt, "receipt_sha256": hashlib.sha256(payload).hexdigest()}, indent=2))
        return 0
    except Exception as exc:
        args.state_file.write_text(json.dumps({"state": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT_REPLAY_REFUSED", "head": args.expected_head, "error_class": type(exc).__name__, "error": str(exc)[:1000], "canonical_success_credit": 0, "replay": False}, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({"state": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT_REPLAY_REFUSED", "error_class": type(exc).__name__, "error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    finally:
        batch.close()


if __name__ == "__main__":
    raise SystemExit(main())
