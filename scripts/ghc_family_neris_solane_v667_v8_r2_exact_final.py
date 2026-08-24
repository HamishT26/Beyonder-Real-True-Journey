#!/usr/bin/env python3
"""Run the Neris Solane v667-v8-r2 exact-final owner-scoped aggregate once."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OWNER = "Neris Solane"
PHASE = "v667-v8-r2"
BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r2-full-tools"
SOURCE = "0db6ed4837c09868a27782e9309c7bea5c943d44"
X1 = "fb83958e7a591645e2731873f00bd1c5af6df2ee"
EVIDENCE = "2873b788991008deb555200e8fd086f88417c190"
PHASE_ROOT = "docs/neris-solane/v667-v8-r2"
FINAL_TEST = "tests/test_ghc_family_neris_solane_v667_v8_r2_final.py"
DEFAULT_RECEIPT_ROOT = Path(ROOT.anchor) / "GHC-Archives" / "phase-temp" / "neris-solane-v667-v8-r2" / "canonical"
RECEIPT_ROOT = Path(os.environ.get("GHC_FAMILY_CANONICAL_BANK", str(DEFAULT_RECEIPT_ROOT)))
LOCK = RECEIPT_ROOT / "canonical-lock.json"
RECEIPT = RECEIPT_ROOT / "exact-final-canonical-receipt.json"
TOKEN = "D_FIRST_NERIS_V667_V8_R2_CANONICAL_RECEIPT"


def run(argv: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(["git", "-C", str(ROOT), *args], check=check)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{PHASE_ROOT}/")
        or path.startswith("scripts/ghc_family_neris_solane_v667_v8_r2_")
        or path in {
            "scripts/build_ghc_family_neris_solane_v667_v8_r2_x1.py",
            "scripts/build_ghc_family_neris_solane_v667_v8_r2_x2.py",
            "scripts/build_ghc_family_neris_solane_v667_v8_r2_final.py",
            "tests/test_ghc_family_neris_solane_v667_v8_r2_x1.py",
            "tests/test_ghc_family_neris_solane_v667_v8_r2_x2.py",
            FINAL_TEST,
        }
    )


def read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"partial Git blob with {remaining} bytes outstanding")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def git_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    """Alternate one request with one exact-length response on Windows."""
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None or proc.stderr is None:
        raise RuntimeError("Git batch pipes unavailable")
    blobs: dict[str, bytes] = {}
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="strict").rstrip("\n")
            fields = header.split()
            if len(fields) != 3 or fields[1] != "blob":
                raise RuntimeError(f"unexpected Git batch header for {path}: {header}")
            data = read_exact(proc.stdout, int(fields[2]))
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing Git batch delimiter for {path}")
            blobs[path] = data
        proc.stdin.close()
        stderr = proc.stderr.read()
        if proc.wait(timeout=60) != 0:
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=60)
        if proc.stdin is not None and not proc.stdin.closed:
            proc.stdin.close()
        if proc.stdout is not None and not proc.stdout.closed:
            proc.stdout.close()
        if proc.stderr is not None and not proc.stderr.closed:
            proc.stderr.close()
    return blobs


def write_external(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def acquire_one_shot_lock() -> None:
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    if RECEIPT.exists():
        raise FileExistsError("canonical receipt already exists")
    payload = json.dumps(
        {
            "state": "STARTED",
            "invocation_count": 1,
            "successful_invocation_count": 0,
            "replayed": False,
            "receipt_token": TOKEN,
        },
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    descriptor = os.open(LOCK, flags)
    try:
        os.write(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def replay_manifest(commit: str, manifest: dict[str, Any]) -> int:
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("manifest entry count mismatch")
    paths = [row["path"] for row in manifest["entries"]]
    blobs = git_blobs(commit, paths)
    for row in manifest["entries"]:
        data = blobs[row["path"]]
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            raise AssertionError(f"manifest replay mismatch: {row['path']}")
    return len(paths)


def privacy_scan(blobs: dict[str, bytes]) -> tuple[int, list[dict[str, str]]]:
    unix_users = b"/" + b"Users" + b"/"
    unix_home = b"/" + b"home" + b"/"
    route_key = rb"(?:source_" + b"thread_id" + rb"|private_" + b"callable_identifier" + rb")"
    interaction_key = rb"(?:session[_-]?" + b"stream" + rb"|private[_-]?" + b"transcript" + rb"|private[_-]?" + b"conversation" + rb")"
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\Users\\[^\\\s]+|" + re.escape(unix_users) + rb"[^/\s]+|" + re.escape(unix_home) + rb"[^/\s]+)"),
        "private_route_or_callable": re.compile(rb"(?:thread|codex|chat)://|" + route_key + rb"\s*[:=]", re.I),
        "credential_value": re.compile(rb"(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}", re.I),
        "private_interaction_payload": re.compile(interaction_key + rb"\s*[:=]\s*['\"]?[^\s,}\]]+", re.I),
    }
    candidates = [
        {"path": path, "class": name}
        for path, data in blobs.items()
        for name, pattern in patterns.items()
        if pattern.search(data)
    ]
    return len(patterns), candidates


def security_scan(blobs: dict[str, bytes]) -> tuple[int, list[dict[str, str]]]:
    patterns = {
        "dynamic_eval": re.compile((r"(?<![A-Za-z0-9_])e" + "val" + r"\s*\(").encode("ascii")),
        "dynamic_exec": re.compile((r"(?<![A-Za-z0-9_])ex" + "ec" + r"\s*\(").encode("ascii")),
        "shell_true": re.compile(("shell" + r"\s*=\s*" + "True").encode("ascii")),
        "os_system": re.compile(("os" + r"\s*\.\s*" + "system" + r"\s*\(").encode("ascii")),
        "pickle_loads": re.compile(("pickle" + r"\s*\.\s*" + "loads" + r"\s*\(").encode("ascii")),
        "unsafe_yaml_load": re.compile(("yaml" + r"\s*\.\s*" + "load" + r"\s*\(").encode("ascii")),
    }
    python_blobs = {path: data for path, data in blobs.items() if path.endswith(".py")}
    findings = [
        {"path": path, "class": name}
        for path, data in python_blobs.items()
        for name, pattern in patterns.items()
        if pattern.search(data)
    ]
    return len(python_blobs), findings


def stale_label_scan(blobs: dict[str, bytes]) -> list[dict[str, str]]:
    stale_tokens = [
        ("Neris " + "Solane " + "v667-v7").encode("utf-8"),
        ("Neris-" + "only " + "v667 v7").encode("utf-8"),
        ("Elaren " + "Kestrel " + "v667-v8").encode("utf-8"),
        ("Elaren-" + "only " + "v667 v8").encode("utf-8"),
    ]
    return [
        {"path": path, "token_sha256": digest(token)}
        for path, data in blobs.items()
        for token in stale_tokens
        if token in data
    ]


def validate(expected_final: str) -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD").strip()
    branch = git_text("branch", "--show-current").strip()
    parent = git_text("rev-parse", "HEAD^").strip()
    commits = [line for line in git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines() if line]
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines() if line]
    parent_counts = [len(git_text("show", "-s", "--format=%P", commit).strip().split()) for commit in commits]
    expected_chain = [X1, EVIDENCE, head]
    if expected_final != head or branch != BRANCH or parent != EVIDENCE:
        raise AssertionError("exact final, branch, or direct parent prerequisite failed")
    if commits != expected_chain or merges or parent_counts != [1, 1, 1]:
        raise AssertionError("source-to-final history prerequisite failed")

    test_result = run([sys.executable, "-B", FINAL_TEST], check=False)
    test_output = (test_result.stdout + b"\n" + test_result.stderr).decode("utf-8", errors="replace")
    ran = re.search(r"Ran\s+(\d+)\s+tests?", test_output)
    selected_tests = int(ran.group(1)) if ran else 0
    if test_result.returncode or selected_tests != 21:
        raise AssertionError(f"final-only tests failed or count drifted: return={test_result.returncode}, selected={selected_tests}")

    owner_paths = [path for path in git_text("ls-tree", "-r", "--name-only", head).splitlines() if path and owner_path(path)]
    if not owner_paths or len(owner_paths) >= 2000:
        raise AssertionError(f"owner file ceiling failed: {len(owner_paths)}")
    blobs = git_blobs(head, owner_paths)
    json_count = 0
    markdown_count = 0
    python_count = 0
    for path, data in blobs.items():
        text = data.decode("utf-8", errors="strict")
        if path.endswith(".json"):
            json.loads(text)
            json_count += 1
        elif path.endswith(".md"):
            if not text.lstrip().startswith("#"):
                raise AssertionError(f"Markdown structure failed: {path}")
            markdown_count += 1
        elif path.endswith(".py"):
            compile(text, path, "exec")
            python_count += 1

    privacy_class_count, privacy_candidates = privacy_scan(blobs)
    if privacy_candidates:
        raise AssertionError(f"privacy candidates: {privacy_candidates[:20]}")
    security_python_count, security_findings = security_scan(blobs)
    if security_findings:
        raise AssertionError(f"bounded Python security findings: {security_findings[:20]}")
    stale_findings = stale_label_scan(blobs)
    if stale_findings:
        raise AssertionError(f"stale owner/phase labels: {stale_findings[:20]}")

    manifest_names = (
        "immutable-x1-manifest",
        "immutable-evidence-manifest",
        "final-delta-manifest",
        "final-owner-manifest",
    )
    manifests = {
        name: json.loads(blobs[f"{PHASE_ROOT}/validation/{name}.json"].decode("utf-8"))
        for name in manifest_names
    }
    manifest_counts = {
        "immutable-x1-manifest": replay_manifest(X1, manifests["immutable-x1-manifest"]),
        "immutable-evidence-manifest": replay_manifest(EVIDENCE, manifests["immutable-evidence-manifest"]),
        "final-delta-manifest": replay_manifest(head, manifests["final-delta-manifest"]),
        "final-owner-manifest": replay_manifest(head, manifests["final-owner-manifest"]),
    }
    if manifest_counts["immutable-x1-manifest"] != 23 or manifest_counts["immutable-evidence-manifest"] != 476:
        raise AssertionError(f"immutable lifecycle manifest count drift: {manifest_counts}")

    closeout = json.loads(blobs[f"{PHASE_ROOT}/closeout/combined-closeout.json"].decode("utf-8"))
    flow = json.loads(blobs[f"{PHASE_ROOT}/closeout/method-flow-state-final.json"].decode("utf-8"))
    route = json.loads(blobs[f"{PHASE_ROOT}/route/terminal-route-state.json"].decode("utf-8"))
    seal = json.loads(blobs[f"{PHASE_ROOT}/seal/seal-candidate.json"].decode("utf-8"))
    outcomes = json.loads(blobs[f"{PHASE_ROOT}/x2/proposal-outcomes.json"].decode("utf-8"))
    tool_receipt = json.loads(blobs[f"{PHASE_ROOT}/x2/tooling/thirteen-tool-transaction-receipt.json"].decode("utf-8"))
    baton = blobs[f"{PHASE_ROOT}/handoffs/vesper-arlen-v668-v1-activation-prepared-not-sent.md"]
    baton_words = len(baton.decode("utf-8").split())

    expected_outcomes = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    expected_evidence = {"effective_negatives": 28580, "methods": 14991, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 864, "passing_witnesses": 1576}
    expected_overlay = {"effective_negatives": 28584, "methods": 14995, "open_gaps": 202, "exact_gates": 200, "failed_witnesses": 868, "passing_witnesses": 1580}
    detailed_checks = {
        "exact_expected_final": expected_final == head,
        "exact_branch": branch == BRANCH,
        "direct_final_parent": parent == EVIDENCE,
        "exact_three_commit_chain": commits == expected_chain,
        "zero_merges": len(merges) == 0,
        "one_parent_each": parent_counts == [1, 1, 1],
        "twenty_one_final_tests": selected_tests == 21,
        "owner_file_ceiling": len(owner_paths) < 2000,
        "strict_json_parse": json_count > 0,
        "five_privacy_classes": privacy_class_count == 5,
        "zero_privacy_candidates": not privacy_candidates,
        "bounded_python_scan": security_python_count == python_count,
        "zero_security_findings": not security_findings,
        "zero_stale_labels": not stale_findings,
        "x1_manifest_23": manifest_counts["immutable-x1-manifest"] == 23,
        "evidence_manifest_476": manifest_counts["immutable-evidence-manifest"] == 476,
        "final_delta_manifest_13": manifest_counts["final-delta-manifest"] == 13,
        "final_owner_manifest_520": manifest_counts["final-owner-manifest"] == 520,
        "proposal_chain_4550": closeout["proposal_chain"] == {"inherited": 4530, "new": 20, "final_frozen_total": 4550},
        "four_outcomes_exact": closeout["outcomes"] == expected_outcomes == outcomes["counts"],
        "one_hundred_rejections": closeout["rejecting_mutations"] == 100,
        "twenty_zero_credit_revalidations": closeout["selected_inherited_revalidations"] == 20,
        "thirteen_tool_transaction": tool_receipt["status"] == "PASS" and tool_receipt["direct_tool_count"] == 13,
        "tool_smokes_exact": tool_receipt["positive_smoke_count"] == 13 and tool_receipt["negative_rejection_count"] == 13,
        "evidence_counts_exact": flow["evidence_sealed"] == expected_evidence,
        "route_overlay_exact": flow["effective_for_later_authorized_route"] == expected_overlay,
        "final_failures_retained": [row["failure_id"] for row in flow["final_closeout_operational_overlay"]["failures_at_commit_time"]] == ["NS6678R2-FINAL-N001", "NS6678R2-FINAL-N002", "NS6678R2-FINAL-N003", "NS6678R2-FINAL-N004"],
        "route_name_clear": route["name_conflict"] is False,
        "route_user_redirect": route["state"] == "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery_user_redirect": route["delivery"] == "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "no_successor_contact": route["successor_contacted"] is False,
        "no_substitution": route["substituted"] is False,
        "no_task_creation": route["created"] is False,
        "standby_untouched": route["Tavian_state"] == "ON_STANDBY" and route["Tavian_contacted"] is False,
        "commit_truth_zero_invocations": seal["canonical_invocation_count"] == 0,
        "commit_truth_zero_successes": seal["canonical_success_count"] == 0,
        "no_post_success_replay": seal["post_success_replay"] is False,
        "baton_minimum_words": baton_words >= 10000,
        "baton_maximum_words": baton_words <= 100000,
        "terminal_not_ready": closeout["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    failed_detailed = [name for name, passed in detailed_checks.items() if not passed]
    if failed_detailed:
        raise AssertionError(f"detailed checks failed: {failed_detailed}")

    dirty = git_text("status", "--porcelain=v1", "--untracked-files=all").strip()
    upstream = git_text("rev-parse", "@{upstream}").strip()
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}").strip()
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").strip().split()
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").strip()
    live = live_line.split()[0] if live_line else ""
    minimal_checks = {
        "head_is_expected": head == expected_final,
        "branch_is_expected": branch == BRANCH,
        "final_parent_is_evidence": parent == EVIDENCE,
        "history_is_linear": commits == expected_chain and not merges and parent_counts == [1, 1, 1],
        "final_tests_pass": test_result.returncode == 0 and selected_tests == 21,
        "manifests_replay": sum(manifest_counts.values()) > 0,
        "owner_scope_under_ceiling": 0 < len(owner_paths) < 2000,
        "privacy_clean": not privacy_candidates,
        "bounded_security_clean": not security_findings,
        "stale_labels_clean": not stale_findings,
        "route_stopped": route["state"] == "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2" and not route["successor_contacted"],
        "verdict_not_ready": closeout["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "clean_state": dirty == "",
        "zero_divergence": divergence == ["0", "0"],
        "fresh_four_way_equality": head == upstream == tracking == live,
    }
    failed_minimal = [name for name, passed in minimal_checks.items() if not passed]
    if failed_minimal:
        raise AssertionError(f"minimal checks failed: {failed_minimal}")

    return {
        "schema": "ghc-family-exact-final-canonical-receipt-v8",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "PASS",
        "validation_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invocation_count": 1,
        "successful_invocation_count": 1,
        "replayed": False,
        "head": head,
        "branch": branch,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_parent": parent,
        "phase_commit_count": len(commits),
        "merge_count": len(merges),
        "parent_counts": parent_counts,
        "final_only_tests_selected": selected_tests,
        "final_only_tests_failed": 0,
        "detailed_check_count": len(detailed_checks),
        "detailed_check_failures": 0,
        "minimal_check_count": len(minimal_checks),
        "minimal_check_failures": 0,
        "owner_file_count": len(owner_paths),
        "json_document_count": json_count,
        "markdown_document_count": markdown_count,
        "python_compile_count": python_count,
        "privacy_class_count": privacy_class_count,
        "privacy_scanned_file_count": len(owner_paths),
        "privacy_candidate_count": 0,
        "privacy_confirmed_hit_count": 0,
        "security_python_file_count": security_python_count,
        "bounded_security_finding_count": 0,
        "stale_label_finding_count": 0,
        "manifest_entry_counts": manifest_counts,
        "manifest_replay_total": sum(manifest_counts.values()),
        "baton_bytes": len(baton),
        "baton_words": baton_words,
        "baton_sha256": digest(baton),
        "clean_state": True,
        "divergence": {"ahead": 0, "behind": 0},
        "four_way_equality": True,
        "refs": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_remote": live},
        "route_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "successor_contacted": False,
        "already_successful_components_replayed": [],
        "scope": "bounded same-owner exact-final Neris source-to-final delta under shared infrastructure only",
        "not_claimed": [
            "complete repository suite", "independent reproduction", "external audit", "production certification",
            "exhaustive security", "privacy completeness", "accessibility completeness", "participant evidence",
            "professional validation", "legal or cultural review", "Maori-authority review", "empirical GMUT confirmation",
            "Theory-of-Everything proof", "AGI or ASI", "consciousness or personhood", "Stage 20 authority",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_final):
        print(json.dumps({"status": "INVALID_EXPECTED_FINAL"}, sort_keys=True))
        return 2
    try:
        acquire_one_shot_lock()
    except FileExistsError:
        print(json.dumps({"status": "REFUSED_DUPLICATE_INVOCATION", "receipt_token": TOKEN}, sort_keys=True))
        return 2
    try:
        receipt = validate(args.expected_final)
    except Exception as exc:
        failure = {
            "schema": "ghc-family-exact-final-canonical-receipt-v8",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "FAIL",
            "validation_state": "FAILED_ZERO_AGGREGATE_SUCCESS_CREDIT",
            "invocation_count": 1,
            "successful_invocation_count": 0,
            "replayed": False,
            "expected_final": args.expected_final,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "aggregate_success_credit": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_external(RECEIPT, failure)
        receipt_sha = digest(RECEIPT.read_bytes())
        write_external(LOCK, {"state": "FAILED", "invocation_count": 1, "successful_invocation_count": 0, "replayed": False, "receipt_sha256": receipt_sha, "receipt_token": TOKEN})
        print(json.dumps({"status": "FAIL", "receipt_sha256": receipt_sha, "receipt_token": TOKEN}, sort_keys=True))
        return 1
    write_external(RECEIPT, receipt)
    receipt_sha = digest(RECEIPT.read_bytes())
    write_external(LOCK, {"state": "PASS", "invocation_count": 1, "successful_invocation_count": 1, "replayed": False, "receipt_sha256": receipt_sha, "receipt_token": TOKEN})
    print(json.dumps({"status": "PASS", "receipt_sha256": receipt_sha, "receipt_token": TOKEN}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
