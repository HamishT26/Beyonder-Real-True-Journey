"""One-shot exact-final owner-scoped validator for Neris Solane v671-v6."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SOURCE_FINAL = "0b81e278af69a6ee0b994eb78c3dd6166c7087b6"
X1_COMMIT = "e79dab91f6dd76bc84556756e3ad657a0150ce9d"
EVIDENCE_COMMIT = "041ea6824d438db774b5af9efff6cf6d59eafa51"
BRANCH = "codex/GHC-Family/neris-solane-v671-v6-full-tools"
OWNER_PREFIX = "docs/neris-solane/v671-v6/"
BATON_PATH = OWNER_PREFIX + "handoffs/vesper-arlen-v671-v7-activation-candidate.md"


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True)


def git_blob(repo: Path, spec: str) -> bytes:
    return subprocess.run(["git", "cat-file", "blob", spec], cwd=repo, check=True, capture_output=True).stdout


def batch_blobs(repo: Path, specs: dict[str, str]) -> dict[str, bytes]:
    """Alternate Git batch requests and exact-length responses on Windows."""
    proc = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert proc.stdin is not None and proc.stdout is not None
    result: dict[str, bytes] = {}
    for key, spec in specs.items():
        proc.stdin.write((spec + "\n").encode("utf-8"))
        proc.stdin.flush()
        header = proc.stdout.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"Git batch did not return a blob for {key}")
        remaining = int(header[2])
        chunks: list[bytes] = []
        while remaining:
            chunk = proc.stdout.read(remaining)
            if not chunk:
                raise RuntimeError(f"short Git batch read for {key}")
            chunks.append(chunk)
            remaining -= len(chunk)
        if proc.stdout.read(1) != b"\n":
            raise RuntimeError(f"missing Git batch separator for {key}")
        result[key] = b"".join(chunks)
    proc.stdin.close()
    proc.stdout.close()
    proc.wait(timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(f"Git batch exited {proc.returncode}")
    return result


def owner_path(path: str) -> bool:
    return (
        path.startswith(OWNER_PREFIX)
        or (path.startswith("scripts/") and ("neris_solane_v671_v6" in path or path.startswith("scripts/ghc_family_pantograph_")))
        or (path.startswith("tests/") and "neris_solane_v671_v6" in path)
    )


def privacy_candidates(text: str) -> list[str]:
    absolute_path = "(?i)(?:" + "[a-z]" + r":\\" + "|/" + "users" + "/|/" + "home" + "/)" + r"[^\s\"']+"
    patterns = {
        "private_absolute_path": absolute_path,
        "raw_task_or_thread_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "credential_or_secret_assignment": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,}\]]+",
        "transcript_screenshot_or_session_stream": r"(?i)(?:private[_-]?transcript|screenshot[_-]?path|session[_-]?stream)\s*[:=]\s*[^\s,}\]]+",
        "private_callable_or_application_state": r"(?i)(?:private[_-]?callable[_-]?id|private[_-]?app[_-]?state)\s*[:=]\s*[^\s,}\]]+",
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text)]


def replay_manifests(repo: Path, final: str) -> dict[str, Any]:
    domains = [
        ("x1", X1_COMMIT, OWNER_PREFIX + "validation/x1-manifest.json"),
        ("evidence_delta", EVIDENCE_COMMIT, OWNER_PREFIX + "validation/evidence-delta-manifest.json"),
        ("evidence_owner", EVIDENCE_COMMIT, OWNER_PREFIX + "validation/evidence-owner-manifest.json"),
        ("final_delta", final, OWNER_PREFIX + "validation/final-delta-manifest.json"),
        ("final_owner", final, OWNER_PREFIX + "validation/final-owner-manifest.json"),
    ]
    manifests: list[tuple[str, dict[str, Any]]] = []
    specs: dict[str, str] = {}
    for domain, commit, path in domains:
        manifest = json.loads(git_blob(repo, f"{commit}:{path}").decode("utf-8"))
        manifests.append((domain, manifest))
        for entry in manifest["entries"]:
            specs[f"{domain}:{entry['path']}"] = f"{commit}:{entry['path']}"
    blobs = batch_blobs(repo, specs)
    rows: list[dict[str, Any]] = []
    total = 0
    mismatches = 0
    for domain, manifest in manifests:
        domain_mismatches = 0
        for entry in manifest["entries"]:
            data = blobs[f"{domain}:{entry['path']}"]
            if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
                domain_mismatches += 1
        total += manifest["entry_count"]
        mismatches += domain_mismatches
        rows.append({"domain": domain, "entries": manifest["entry_count"], "mismatches": domain_mismatches})
    return {"domains": rows, "entries": total, "mismatches": mismatches}


def exact_owner_review(repo: Path, final: str) -> dict[str, Any]:
    paths = run(repo, "git", "ls-tree", "-r", "--name-only", final, OWNER_PREFIX.rstrip("/"), "scripts", "tests").stdout.splitlines()
    paths = [path for path in paths if owner_path(path)]
    blobs = batch_blobs(repo, {path: f"{final}:{path}" for path in paths})
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    security: list[dict[str, Any]] = []
    text_files = 0
    python_files = 0
    for path, data in blobs.items():
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
            except Exception as exc:  # noqa: BLE001
                json_errors.append(f"{path}:{type(exc).__name__}")
        if Path(path).suffix.lower() in {".json", ".md", ".html", ".txt", ".py"}:
            text_files += 1
            text = data.decode("utf-8", errors="replace")
            privacy.extend({"path": path, "class": name} for name in privacy_candidates(text))
        if path.endswith(".py"):
            python_files += 1
            tree = ast.parse(data.decode("utf-8"), filename=path)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "line": node.lineno, "kind": node.func.id})
                if isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                    security.append({"path": path, "line": node.lineno, "kind": "system_call"})
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        security.append({"path": path, "line": node.lineno, "kind": "shell_true"})
    return {
        "owner_files": len(paths),
        "json_documents": sum(path.endswith(".json") for path in paths),
        "json_errors": json_errors,
        "text_files": text_files,
        "privacy_candidates": privacy,
        "python_files": python_files,
        "security_findings": security,
        "blobs": blobs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit("canonical output already exists; one-shot validator refuses replay")
    output.parent.mkdir(parents=True, exist_ok=True)
    final = args.expected_final

    head = run(repo, "git", "rev-parse", "HEAD").stdout.strip()
    upstream = run(repo, "git", "rev-parse", "@{u}").stdout.strip()
    tracking = run(repo, "git", "rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.strip()
    live_line = run(repo, "git", "ls-remote", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    live = live_line.split()[0] if live_line else ""
    divergence = run(repo, "git", "rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.strip().split()
    phase_commits = run(repo, "git", "rev-list", "--reverse", f"{SOURCE_FINAL}..{final}").stdout.splitlines()
    merge_count = int(run(repo, "git", "rev-list", "--count", "--merges", f"{SOURCE_FINAL}..{final}").stdout.strip())
    parent_rows = [run(repo, "git", "rev-list", "--parents", "-n", "1", commit).stdout.strip().split() for commit in phase_commits]

    manifests = replay_manifests(repo, final)
    owner = exact_owner_review(repo, final)
    blobs: dict[str, bytes] = owner.pop("blobs")
    truth = json.loads(blobs[OWNER_PREFIX + "closeout/phase-truth-final.json"].decode("utf-8"))
    composite = json.loads(blobs[OWNER_PREFIX + "validation/x2-test-composite-receipt.json"].decode("utf-8"))
    baton_receipt = json.loads(blobs[OWNER_PREFIX + "handoffs/vesper-arlen-v671-v7-activation-candidate-receipt.json"].decode("utf-8"))
    baton = blobs[BATON_PATH]
    route = json.loads(blobs[OWNER_PREFIX + "route/route-state.json"].decode("utf-8"))
    report = blobs[OWNER_PREFIX + "x2/accessible-evidence-report.html"].decode("utf-8")

    test_proc = run(repo, sys.executable, "-B", "-m", "unittest", "tests.test_ghc_family_neris_solane_v671_v6_final")
    test_output = (test_proc.stdout + "\n" + test_proc.stderr).strip()
    match = re.search(r"Ran (\d+) tests", test_output)
    test_count = int(match.group(1)) if match else 0

    worktree_diff = run(repo, "git", "diff", "--quiet").returncode
    index_diff = run(repo, "git", "diff", "--cached", "--quiet").returncode
    untracked = run(repo, "git", "ls-files", "--others", "--exclude-standard").stdout.splitlines()
    post_head = run(repo, "git", "rev-parse", "HEAD").stdout.strip()
    post_live_line = run(repo, "git", "ls-remote", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    post_live = post_live_line.split()[0] if post_live_line else ""

    checks = {
        "expected_head": head == final == post_head,
        "local_upstream_equal": head == upstream,
        "local_tracking_equal": head == tracking,
        "local_fresh_live_equal": head == live == post_live,
        "zero_divergence": divergence == ["0", "0"],
        "clean_worktree": worktree_diff == 0,
        "clean_index": index_diff == 0,
        "zero_untracked": not untracked,
        "three_phase_commits": phase_commits == [X1_COMMIT, EVIDENCE_COMMIT, final],
        "zero_merges": merge_count == 0,
        "single_parent_phase_history": len(parent_rows) == 3 and all(len(row) == 2 for row in parent_rows),
        "x1_direct_source_child": parent_rows[0][1] == SOURCE_FINAL,
        "evidence_direct_x1_child": parent_rows[1][1] == X1_COMMIT,
        "final_direct_evidence_child": parent_rows[2][1] == EVIDENCE_COMMIT,
        "all_manifest_replays": manifests["mismatches"] == 0,
        "all_json_parses": not owner["json_errors"],
        "zero_privacy_candidates": not owner["privacy_candidates"],
        "zero_bounded_python_findings": not owner["security_findings"],
        "owner_file_ceiling": owner["owner_files"] < 2000,
        "final_tests_passed_once": test_proc.returncode == 0 and test_count == 18,
        "x2_suite_preserved": composite["collection_only"]["collected_tests"] == 22 and composite["owner_suite"]["passed_tests"] == 22,
        "x2_success_not_replayed": composite["owner_suite"]["successful_replay"] is False,
        "target_changed_two_test_refresh": composite["target_changed_refresh"]["passed_tests"] == 2 and not composite["target_changed_refresh"]["unchanged_successful_components_replayed"],
        "not_complete_repository_suite": composite["complete_repository_suite"] is False,
        "four_outcome_labels": truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "effective_counts_preserved": all(truth[key] == value for key, value in {"effective_negatives": 34458, "methods": 21001, "failed_witnesses": 6279, "passing_witnesses": 8184, "open_gaps": 267, "exact_gates": 262}.items()),
        "terminal_nonpromotion": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "baton_bytes": len(baton) == baton_receipt["bytes"],
        "baton_words": len(baton.decode("utf-8").split()) == baton_receipt["whitespace_words"] and baton_receipt["whitespace_words"] >= 10000,
        "baton_sha256": hashlib.sha256(baton).hexdigest() == baton_receipt["sha256"],
        "baton_prepared_not_sent": baton_receipt["prepared_not_sent"] and not baton_receipt["sent_by_neris_solane"] and not baton_receipt["delivery_acknowledged"],
        "baton_exact_title": baton_receipt["recipient_exact_title"] == "Vesper Arlen" and baton_receipt["stale_rejected_labels"] == ["Vesper Rowan"],
        "route_prepared_no_substitution": route["state"] == "PREPARED_NOT_SENT" and route["recipient_exact_title"] == "Vesper Arlen" and not route["substitution_permitted"] and not route["sent_by_neris_solane"] and not route["delivery_acknowledged"],
        "accessible_report_structure": all(token in report for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"')) and "<script" not in report.lower(),
    }
    passed = all(checks.values())
    receipt = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v4",
        "owner": "Neris Solane",
        "phase": "v671-v6",
        "result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if passed else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invocation_count": 1,
        "successful_invocation_count": 1 if passed else 0,
        "post_success_replay": False,
        "exact_final": final,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_declared": len(checks),
        "tests": {"module": "tests.test_ghc_family_neris_solane_v671_v6_final", "declared": 18, "passed": test_count if test_proc.returncode == 0 else 0, "returncode": test_proc.returncode},
        "manifests": manifests,
        "owner_review": owner,
        "history": {"phase_commits": phase_commits, "merge_count": merge_count, "single_parent_rows": len(parent_rows)},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": live, "post_test_live": post_live, "divergence": divergence},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "claim_boundary": "Owner-scoped same-infrastructure software evidence is not the complete repository suite, independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal or cultural review, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.",
    }
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"result": receipt["result"], "checks": f"{receipt['checks_passed']}/{receipt['checks_declared']}", "tests": f"{receipt['tests']['passed']}/{receipt['tests']['declared']}", "json": owner["json_documents"], "privacy": len(owner["privacy_candidates"]), "manifest_entries": manifests["entries"]}, sort_keys=True))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
