from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Elaren Kestrel"
PHASE = "v671-v5"
OWNER_PREFIX = "docs/elaren-kestrel/v671-v5"
EXPECTED_COUNTS = {
    "effective_negatives": 34280,
    "effective_methods": 20823,
    "failed_witnesses": 6101,
    "bounded_passing_witnesses": 7970,
    "open_gaps": 265,
    "exact_gates": 260,
}
EXPECTED_OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def run(repo: Path, *args: str, check: bool = True, timeout: int = 300) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, check=False, timeout=timeout)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result


def git_text(repo: Path, *args: str) -> str:
    return run(repo, *args).stdout.decode("utf-8").strip()


def git_blob(repo: Path, commit: str, path: str) -> bytes:
    return run(repo, "show", f"{commit}:{path}").stdout


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def normalized_lf(blob: bytes) -> bytes:
    return blob.replace(bytes([13, 10]), bytes([10]))


def parse_json_blob(repo: Path, commit: str, path: str) -> Any:
    return json.loads(git_blob(repo, commit, path).decode("utf-8"))


def verify_manifest(repo: Path, commit: str, path: str) -> dict[str, Any]:
    payload = parse_json_blob(repo, commit, path)
    issues = []
    for row in payload["entries"]:
        raw = git_blob(repo, commit, row["path"])
        normalized = normalized_lf(raw)
        if len(normalized) != row["bytes"]:
            issues.append({"path": row["path"], "issue": "bytes"})
        if sha256(normalized) != row["sha256"]:
            issues.append({"path": row["path"], "issue": "normalized_sha256"})
        if sha256(raw) != row["git_blob_sha256"]:
            issues.append({"path": row["path"], "issue": "git_blob_sha256"})
    if len(payload["entries"]) != payload["entry_count"]:
        issues.append({"path": path, "issue": "entry_count"})
    return {"path": path, "entries": payload["entry_count"], "issues": issues, "result": "VALID" if not issues else "INVALID"}


def privacy_scan(repo: Path, commit: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "opaque_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"[A-Za-z]:\\(?:Users|GHC-Archives)\\", re.I),
        "credential_or_token": re.compile(r"\b(?:sk|ghp|github_pat)-?[A-Za-z0-9_]{16,}\b"),
        "private_delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.I),
        "private_session_stream": re.compile(r"\b(?:session_stream|private_app_state)\s*[:=]", re.I),
    }
    hits = []
    scanned = 0
    extensions = {".md", ".json", ".html", ".py", ".txt", ".yaml", ".yml", ".toml"}
    for path in paths:
        if Path(path).suffix.lower() not in extensions:
            continue
        text = git_blob(repo, commit, path).decode("utf-8")
        scanned += 1
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"path": path, "class": label, "match_sha256": sha256(match.group(0).encode("utf-8"))})
    return {"files": scanned, "classes": len(patterns), "candidates": len(hits), "confirmed_hits": len(hits), "hits": hits}


def security_scan(repo: Path, commit: str, paths: list[str]) -> dict[str, Any]:
    findings = []
    checked = 0
    for path in paths:
        if not path.endswith(".py"):
            continue
        checked += 1
        text = git_blob(repo, commit, path).decode("utf-8")
        try:
            tree = ast.parse(text, filename=path)
        except SyntaxError as exc:
            findings.append({"path": path, "issue": f"syntax:{exc.msg}"})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "issue": node.func.id})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path, "issue": "shell_true"})
    return {"python_files": checked, "finding_count": len(findings), "findings": findings}


def selected_tests(repo: Path, receipt_dir: Path) -> dict[str, Any]:
    modules = [
        "tests.test_ghc_family_elaren_kestrel_v671_v5_x1",
        "tests.test_ghc_family_elaren_kestrel_v671_v5_x2",
        "tests.test_ghc_family_elaren_kestrel_v671_v5_final",
    ]
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPYCACHEPREFIX"] = str(receipt_dir / "pycache")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "unittest", "-v", *modules],
        cwd=repo, capture_output=True, check=False, timeout=600, env=env,
    )
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"Ran\s+(\d+)\s+tests?", output)
    count = int(match.group(1)) if match else 0
    return {
        "modules": modules, "returncode": result.returncode, "tests": count,
        "output_sha256": sha256(output.encode("utf-8")),
        "result": "VALID" if result.returncode == 0 and count == 57 else "INVALID",
    }


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    temp.replace(path)


def validate(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    final = args.final
    branch = args.branch
    run(repo, "fetch", "origin", branch, "--quiet", timeout=300)
    head = git_text(repo, "rev-parse", "HEAD")
    upstream = git_text(repo, "rev-parse", "@{upstream}")
    tracking = git_text(repo, "rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git_text(repo, "ls-remote", "origin", f"refs/heads/{branch}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    status = git_text(repo, "status", "--porcelain=v1", "--untracked-files=all")
    owner_paths = [path for path in git_text(repo, "ls-tree", "-r", "--name-only", final, OWNER_PREFIX).splitlines() if path]
    added_paths = [path for path in git_text(repo, "diff", "--name-only", args.source, final).splitlines() if path]
    phase_commits = int(git_text(repo, "rev-list", "--count", f"{args.source}..{final}"))
    merges = int(git_text(repo, "rev-list", "--merges", "--count", f"{args.source}..{final}"))
    parent_rows = [git_text(repo, "rev-list", "--parents", "-n", "1", commit).split() for commit in (args.x1, args.evidence, final)]

    test_result = selected_tests(repo, args.receipt_dir)
    json_issues = []
    json_count = 0
    markdown_count = 0
    html_count = 0
    for path in owner_paths:
        raw = git_blob(repo, final, path)
        raw.decode("utf-8")
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError as exc:
                json_issues.append({"path": path, "issue": str(exc)})
        elif path.endswith(".md"):
            markdown_count += 1
        elif path.endswith(".html"):
            html_count += 1

    privacy = privacy_scan(repo, final, [*owner_paths, *[path for path in added_paths if path.endswith(".py")]])
    security = security_scan(repo, final, [path for path in added_paths if path.endswith(".py")])
    manifests = [
        verify_manifest(repo, args.x1, f"{OWNER_PREFIX}/validation/x1-manifest.json"),
        verify_manifest(repo, args.evidence, f"{OWNER_PREFIX}/validation/evidence-manifest.json"),
        verify_manifest(repo, final, f"{OWNER_PREFIX}/validation/final-delta-manifest.json"),
        verify_manifest(repo, final, f"{OWNER_PREFIX}/validation/final-owner-manifest.json"),
    ]
    phase_truth = parse_json_blob(repo, final, f"{OWNER_PREFIX}/closeout/phase-truth.json")
    route = parse_json_blob(repo, final, f"{OWNER_PREFIX}/orchestration/route-state-final-candidate.json")
    seal = parse_json_blob(repo, final, f"{OWNER_PREFIX}/seal/content-seal.json")
    baton = git_blob(repo, final, route["baton_path"])
    seal_issues = []
    for row in seal["entries"]:
        raw = git_blob(repo, final, row["path"])
        if len(raw) != row["bytes"] or sha256(raw) != row["sha256"]:
            seal_issues.append(row["path"])

    detailed = {
        "head_exact": head == final,
        "branch_exact": git_text(repo, "branch", "--show-current") == branch,
        "x1_parent_source": parent_rows[0] == [args.x1, args.source],
        "evidence_parent_x1": parent_rows[1] == [args.evidence, args.x1],
        "final_parent_evidence": parent_rows[2] == [final, args.evidence],
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merges == 0,
        "single_parent_each": all(len(row) == 2 for row in parent_rows),
        "clean": status == "",
        "divergence_zero": divergence == ["0", "0"],
        "upstream_equal": upstream == final,
        "tracking_equal": tracking == final,
        "live_equal": live == final,
        "selected_tests_57": test_result["result"] == "VALID",
        "json_all_parse": not json_issues,
        "owner_json_present": json_count > 0,
        "markdown_present": markdown_count > 0,
        "html_present": html_count > 0,
        "privacy_zero": privacy["confirmed_hits"] == 0,
        "security_zero": security["finding_count"] == 0,
        "x1_manifest": manifests[0]["result"] == "VALID",
        "evidence_manifest": manifests[1]["result"] == "VALID",
        "final_delta_manifest": manifests[2]["result"] == "VALID",
        "final_owner_manifest": manifests[3]["result"] == "VALID",
        "phase_counts": phase_truth["counts"] == EXPECTED_COUNTS,
        "phase_outcomes": phase_truth["outcomes"] == EXPECTED_OUTCOMES,
        "verdict_held": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared": route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0,
        "baton_words": 10000 <= route["baton_words"] <= 100000,
        "baton_bytes": len(baton) == route["baton_bytes"],
        "baton_sha256": sha256(baton) == route["baton_sha256"],
        "content_seal": not seal_issues,
        "owner_file_cap": len(owner_paths) < 2000,
        "added_file_cap": len(added_paths) < 2000,
    }
    minimal = {
        "exact_head": detailed["head_exact"], "exact_parent": detailed["final_parent_evidence"],
        "history": detailed["three_phase_commits"] and detailed["zero_merges"],
        "clean": detailed["clean"], "remote_equal": detailed["upstream_equal"] and detailed["tracking_equal"] and detailed["live_equal"],
        "tests": detailed["selected_tests_57"], "json": detailed["json_all_parse"],
        "privacy": detailed["privacy_zero"], "security": detailed["security_zero"],
        "manifests": all(row["result"] == "VALID" for row in manifests),
        "phase_truth": detailed["phase_counts"] and detailed["phase_outcomes"],
        "seal": detailed["content_seal"], "baton": detailed["baton_words"] and detailed["baton_sha256"],
        "route_held": detailed["route_prepared"], "verdict": detailed["verdict_held"],
    }
    result = "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all(detailed.values()) and all(minimal.values()) else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
    return {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v7",
        "owner": OWNER, "phase": PHASE, "result": result,
        "invocation_count": 1, "successful_invocation_count": 1 if result.startswith("VALID") else 0,
        "post_success_replay": False, "source": args.source, "x1": args.x1,
        "evidence": args.evidence, "final": final, "branch": branch,
        "tests": test_result, "detailed": detailed,
        "detailed_checks": len(detailed), "detailed_passed": sum(detailed.values()),
        "minimal": minimal, "minimal_checks": len(minimal), "minimal_passed": sum(minimal.values()),
        "json_documents": json_count, "json_issues": json_issues,
        "markdown_documents": markdown_count, "html_documents": html_count,
        "privacy": privacy, "security": security, "manifests": manifests,
        "owner_files": len(owner_paths), "added_paths": len(added_paths),
        "seal_issues": seal_issues, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Same-owner local software evidence only; not the complete repository suite, independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal or cultural review, Maori authority, empirical confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--x1", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--final", required=True)
    parser.add_argument("--receipt-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.receipt_dir = args.receipt_dir.resolve()
    marker = args.receipt_dir / "elaren-kestrel-v671-v5-canonical-invocation.json"
    payload_path = args.receipt_dir / "elaren-kestrel-v671-v5-canonical-payload.json"
    receipt_path = args.receipt_dir / "elaren-kestrel-v671-v5-canonical-receipt.json"
    if marker.exists():
        raise SystemExit("canonical invocation marker already exists; replay refused")
    atomic_json(marker, {"owner": OWNER, "phase": PHASE, "state": "INVOKED_ONCE_RUNNING", "final": args.final})
    try:
        payload = validate(args)
    except Exception as exc:
        payload = {
            "schema": "ghc.family.exact-final-owner-scoped-canonical.v7",
            "owner": OWNER, "phase": PHASE,
            "result": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "invocation_count": 1, "successful_invocation_count": 0,
            "post_success_replay": False, "final": args.final,
            "error_type": type(exc).__name__, "error": str(exc),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    payload_bytes = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    atomic_json(payload_path, payload)
    receipt = {
        "schema": "ghc.family.exact-final-canonical-receipt.v7",
        "owner": OWNER, "phase": PHASE, "result": payload["result"],
        "final": args.final, "payload_sha256": sha256(payload_bytes),
        "invocation_count": 1, "successful_invocation_count": payload.get("successful_invocation_count", 0),
        "post_success_replay": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    atomic_json(receipt_path, receipt)
    atomic_json(marker, {"owner": OWNER, "phase": PHASE, "state": payload["result"], "final": args.final, "receipt_sha256": sha256(receipt_path.read_bytes())})
    print(json.dumps({"result": payload["result"], "payload_sha256": receipt["payload_sha256"], "receipt_sha256": sha256(receipt_path.read_bytes()), "detailed": f"{payload.get('detailed_passed', 0)}/{payload.get('detailed_checks', 0)}", "minimal": f"{payload.get('minimal_passed', 0)}/{payload.get('minimal_checks', 0)}", "tests": payload.get("tests", {}).get("tests", 0)}, sort_keys=True))
    if not payload["result"].startswith("VALID"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
