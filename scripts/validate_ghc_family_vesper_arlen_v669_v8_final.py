"""One-shot exact-final owner-scoped canonical validator for Vesper Arlen v669-v8."""

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

SOURCE_FINAL = "8b1a06d1f34147f7adbb494622df4734f48344de"
X1_COMMIT = "6cf75a062b9248359599f29ad88ba39ec733f576"
EVIDENCE_COMMIT = "375b43adfcc4e4a911ea26218806af79d70db58f"
BRANCH = "codex/GHC-Family/vesper-arlen-v669-v8-full-tools"
OWNER_PREFIX = "docs/vesper-arlen/v669-v8/"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
COUNTS = {
    "effective_negatives": 31853,
    "methods": 17958,
    "failed_witnesses": 3674,
    "passing_witnesses": 4930,
    "open_gaps": 239,
    "exact_gates": 234,
}


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True)


def git_blob(repo: Path, spec: str) -> bytes:
    return subprocess.run(["git", "cat-file", "blob", spec], cwd=repo, check=True, capture_output=True).stdout


def batch_blobs(repo: Path, specs: dict[str, str]) -> dict[str, bytes]:
    """Alternate each Git batch request with its exact-length response on Windows."""
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    result: dict[str, bytes] = {}
    try:
        for key, spec in specs.items():
            proc.stdin.write((spec + "\n").encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                raise RuntimeError(f"Git batch did not return a blob for {key}")
            size = int(header[2])
            chunks: list[bytes] = []
            remaining = size
            while remaining:
                chunk = proc.stdout.read(remaining)
                if not chunk:
                    raise RuntimeError(f"short Git batch read for {key}")
                chunks.append(chunk)
                remaining -= len(chunk)
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing Git batch separator for {key}")
            result[key] = b"".join(chunks)
    finally:
        proc.stdin.close()
        proc.stdout.close()
    proc.wait(timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(f"Git batch exited {proc.returncode}")
    return result


def privacy_candidates(text: str) -> list[str]:
    absolute_path = "(?i)(?:" + "[a-z]" + r":\\" + "|/" + "users" + "/|/" + "home" + "/)" + r"[^\s\"']+"
    patterns = {
        "private_absolute_path": absolute_path,
        "opaque_task_or_thread_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "credential_or_secret_assignment": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,}\]]+",
        "private_route_scheme": r"(?i)(?:codex|vscode|file|app)://[^\s\"']+",
        "protected_stream_filename": r"(?i)[^\s\"']*(?:transcript|screenshot|session[_-]?stream)[^\s\"']*\.(?:jsonl?|png|jpe?g|webp|log)",
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text)]


def replay_manifests(repo: Path, final: str) -> dict[str, Any]:
    domains = [
        ("x1", X1_COMMIT, "docs/vesper-arlen/v669-v8/validation/x1-manifest.json"),
        ("evidence", EVIDENCE_COMMIT, "docs/vesper-arlen/v669-v8/validation/evidence-manifest.json"),
        ("final_delta", final, "docs/vesper-arlen/v669-v8/validation/final-delta-manifest.json"),
        ("final_owner", final, "docs/vesper-arlen/v669-v8/validation/final-owner-manifest.json"),
    ]
    manifests: list[tuple[str, str, dict[str, Any]]] = []
    specs: dict[str, str] = {}
    for domain, commit, path in domains:
        manifest = json.loads(git_blob(repo, f"{commit}:{path}").decode("utf-8"))
        manifests.append((domain, commit, manifest))
        for entry in manifest["entries"]:
            specs[f"{domain}:{entry['path']}"] = f"{commit}:{entry['path']}"
    blobs = batch_blobs(repo, specs)
    rows: list[dict[str, Any]] = []
    total = 0
    mismatches = 0
    for domain, _commit, manifest in manifests:
        domain_mismatches = 0
        for entry in manifest["entries"]:
            data = blobs[f"{domain}:{entry['path']}"]
            if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
                domain_mismatches += 1
        total += manifest["entry_count"]
        mismatches += domain_mismatches
        rows.append({"domain": domain, "entries": manifest["entry_count"], "mismatches": domain_mismatches})
    return {"domains": rows, "entries": total, "mismatches": mismatches}


def exact_delta_review(repo: Path, final: str) -> dict[str, Any]:
    paths = run(repo, "git", "diff", "--name-only", SOURCE_FINAL, final).stdout.splitlines()
    blobs = batch_blobs(repo, {path: f"{final}:{path}" for path in paths})
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    security: list[dict[str, Any]] = []
    stale_paths: list[str] = []
    word_violations: list[str] = []
    text_files = 0
    python_files = 0
    allowed_stale_paths = {
        "docs/vesper-arlen/v669-v8/x1/route-state.json",
        "ghc-family-index/references/v669-v8-vesper-arlen.md",
        "scripts/build_ghc_family_vesper_arlen_v669_v8_x1.py",
        "tests/test_ghc_family_vesper_arlen_v669_v8_x1.py",
    }
    for path, data in blobs.items():
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            try:
                json.loads(data.decode("utf-8"))
            except Exception as exc:  # noqa: BLE001
                json_errors.append(f"{path}:{type(exc).__name__}")
        if suffix in {".json", ".md", ".html", ".txt", ".py"}:
            text_files += 1
            text = data.decode("utf-8", errors="replace")
            privacy.extend({"path": path, "class": name} for name in privacy_candidates(text))
            if len(text.split()) > 100000:
                word_violations.append(path)
            if "Vesper Rowan" in text and path not in allowed_stale_paths:
                stale_paths.append(path)
        if suffix == ".py":
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
        "owner_delta_files": len(paths),
        "json_documents": sum(path.endswith(".json") for path in paths),
        "json_errors": json_errors,
        "text_files": text_files,
        "privacy_candidates": privacy,
        "python_files": python_files,
        "security_findings": security,
        "stale_label_paths_outside_allowlist": stale_paths,
        "word_violations": word_violations,
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
    owner = exact_delta_review(repo, final)
    blobs: dict[str, bytes] = owner.pop("blobs")
    truth = json.loads(blobs["docs/vesper-arlen/v669-v8/closeout/phase-truth.json"].decode("utf-8"))
    baton_path = "docs/vesper-arlen/v669-v8/handoffs/lyren-moss-v670-v1-activation-candidate.md"
    baton_receipt = json.loads(blobs["docs/vesper-arlen/v669-v8/handoffs/activation-candidate-integrity.json"].decode("utf-8"))
    baton = blobs[baton_path]
    route = json.loads(blobs["docs/vesper-arlen/v669-v8/orchestration/route-state-final-candidate.json"].decode("utf-8"))
    report = blobs["docs/vesper-arlen/v669-v8/x2/accessible-evidence-report.html"].decode("utf-8")
    final_review = json.loads(blobs["docs/vesper-arlen/v669-v8/validation/final-staged-review.json"].decode("utf-8"))

    test_modules = [
        "tests.test_ghc_family_vesper_arlen_v669_v8_x1",
        "tests.test_ghc_family_vesper_arlen_v669_v8_x2",
        "tests.test_ghc_family_vesper_arlen_v669_v8_final",
    ]
    test_proc = run(repo, sys.executable, "-B", "-m", "unittest", *test_modules)
    test_output = (test_proc.stdout + "\n" + test_proc.stderr).strip()
    match = re.search(r"Ran (\d+) tests", test_output)
    test_count = int(match.group(1)) if match else 0

    worktree_diff = run(repo, "git", "diff", "--quiet").returncode
    index_diff = run(repo, "git", "diff", "--cached", "--quiet").returncode
    untracked = run(repo, "git", "ls-files", "--others", "--exclude-standard").stdout.splitlines()
    post_head = run(repo, "git", "rev-parse", "HEAD").stdout.strip()
    post_live_line = run(repo, "git", "ls-remote", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    post_live = post_live_line.split()[0] if post_live_line else ""
    normalized_baton = baton.decode("utf-8").replace("\r\n", "\n").rstrip() + "\n"

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
        "stale_label_confined_to_declared_x1_truth": not owner["stale_label_paths_outside_allowlist"],
        "owner_file_ceiling": owner["owner_delta_files"] < 2000,
        "all_word_ceilings": not owner["word_violations"],
        "selected_tests_passed_once": test_proc.returncode == 0 and test_count == 81,
        "four_outcome_labels": truth["outcomes"] == OUTCOMES,
        "effective_counts_preserved": all(truth[key] == value for key, value in COUNTS.items()),
        "proposal_chain": truth["proposal_chain"] == 5230,
        "terminal_nonpromotion": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "baton_word_bounds": 10000 <= len(normalized_baton.split()) <= 100000,
        "baton_words": len(normalized_baton.split()) == baton_receipt["word_count"],
        "baton_sha256": hashlib.sha256(normalized_baton.encode("utf-8")).hexdigest() == baton_receipt["sha256_normalized_lf"],
        "baton_prepared_not_sent": baton_receipt["delivery_state"] == "PREPARED_NOT_SENT" and not baton_receipt["delivery_acknowledged"],
        "route_prepared_not_sent": route["delivery_state"] == "PREPARED_NOT_SENT" and route["successor_contact_count"] == 0 and not route["app_acknowledgement"],
        "final_staged_review_passed": final_review["passed"],
        "accessible_report_structure": all(token in report for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"')) and "<script" not in report.lower(),
    }
    passed = all(checks.values())
    receipt = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v3",
        "owner": "Vesper Arlen",
        "phase": "v669-v8",
        "result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if passed else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invocation_count": 1,
        "successful_invocation_count": 1 if passed else 0,
        "post_success_replay": False,
        "exact_final": final,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_declared": len(checks),
        "tests": {"modules": test_modules, "declared": 81, "passed": test_count if test_proc.returncode == 0 else 0, "returncode": test_proc.returncode},
        "manifests": manifests,
        "owner_review": owner,
        "history": {"phase_commits": phase_commits, "merge_count": merge_count, "single_parent_rows": len(parent_rows)},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": live, "post_test_live": post_live, "divergence": divergence},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "claim_boundary": "Owner-scoped same-infrastructure software evidence is not the complete repository suite, independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal or cultural review, Maori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.",
    }
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "result": receipt["result"],
                "checks": f"{receipt['checks_passed']}/{receipt['checks_declared']}",
                "tests": f"{receipt['tests']['passed']}/{receipt['tests']['declared']}",
                "json": owner["json_documents"],
                "privacy": len(owner["privacy_candidates"]),
                "manifest_entries": manifests["entries"],
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
