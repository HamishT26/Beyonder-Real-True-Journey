#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical completion for v665-v6.

The script writes its exclusive receipt outside the repository.  It must be run
only after the exact final is committed, pushed, clean, zero-divergent, and
fresh-live equal.  A complete success must never be replayed.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/caelen-morrow/v665-v6/"
SOURCE = "cacbeb47741b9e86a6a980f85f6f9658a0837f7c"
X1 = "9be19f91371da0d2bcdd23de421fed202c5641fa"
EVIDENCE = "5904cd361cf276ce6c05b2829c581837640a564f"
BRANCH = "codex/GHC-Family/caelen-morrow-v665-v6-full-tools"
EXCLUDED_TESTS = {
    "tests.test_ghc_family_caelen_morrow_v665_v6_x1.CaelenMorrowV665V6X1Tests.test_x1_content_manifest_when_present",
    "tests.test_ghc_family_caelen_morrow_v665_v6_x2.CaelenMorrowV665V6X2Tests.test_x1_commit_is_direct_parent_basis",
    "tests.test_ghc_family_caelen_morrow_v665_v6_x2.CaelenMorrowV665V6X2Tests.test_terminal_verdict_and_no_route_artifact",
}
TEST_MODULES = [
    "tests.test_ghc_family_caelen_morrow_v665_v6_x1",
    "tests.test_ghc_family_caelen_morrow_v665_v6_x2",
    "tests.test_ghc_family_caelen_morrow_v665_v6_evidence",
    "tests.test_ghc_family_caelen_morrow_v665_v6_final",
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT)


def git_text(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def git_json(ref: str, path: str) -> dict[str, Any]:
    return json.loads(git_bytes("show", f"{ref}:{path}").decode("utf-8"))


def batch_blobs(specs: list[str]) -> list[bytes]:
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    for spec in specs:
        process.stdin.write((spec + "\n").encode("utf-8"))
    process.stdin.close()
    blobs: list[bytes] = []
    for spec in specs:
        header = process.stdout.readline().decode("utf-8").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"missing blob for {spec}")
        size = int(header[2])
        blob = process.stdout.read(size)
        if process.stdout.read(1) != b"\n":
            raise RuntimeError(f"invalid batch separator for {spec}")
        blobs.append(blob)
    if process.wait() != 0:
        raise RuntimeError("git cat-file batch failed")
    return blobs


def flatten(suite: unittest.TestSuite) -> Iterable[unittest.TestCase]:
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def run_selected_tests() -> dict[str, Any]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    loaded = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    all_tests = list(flatten(loaded))
    selected = [test for test in all_tests if test.id() not in EXCLUDED_TESTS]
    actually_excluded = {test.id() for test in all_tests if test.id() in EXCLUDED_TESTS}
    if actually_excluded != EXCLUDED_TESTS:
        raise RuntimeError("named lifecycle exclusion set did not resolve exactly")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(unittest.TestSuite(selected))
    return {
        "discovered": len(all_tests),
        "selected": len(selected),
        "excluded": len(actually_excluded),
        "excluded_ids": sorted(actually_excluded),
        "run": result.testsRun,
        "failures": [test.id() for test, _ in result.failures],
        "errors": [test.id() for test, _ in result.errors],
        "skipped": len(result.skipped),
        "passed": result.wasSuccessful() and result.testsRun == len(selected),
    }


def replay_manifest(ref: str, manifest_path: str) -> dict[str, Any]:
    manifest = git_json(ref, manifest_path)
    entries = manifest["entries"]
    blobs = batch_blobs([f"{ref}:{entry['path']}" for entry in entries])
    failures = []
    for entry, blob in zip(entries, blobs):
        if len(blob) != entry["size_bytes"] or hashlib.sha256(blob).hexdigest() != entry["sha256"]:
            failures.append(entry["path"])
    return {
        "manifest_path": manifest_path,
        "phase": manifest["phase"],
        "entries": len(entries),
        "failures": failures,
        "passed": not failures,
        "self_exclusion": manifest.get("self_exclusion"),
        "self_exclusions": manifest.get("self_exclusions", []),
        "entry_paths": [entry["path"] for entry in entries],
    }


def owner_paths(final: str) -> list[str]:
    tree = git_text("ls-tree", "-r", "--name-only", final).splitlines()
    changed = git_text("diff", "--name-only", f"{SOURCE}..{final}").splitlines()
    paths = [path for path in tree if path.startswith(PHASE_PREFIX)]
    paths += [
        path
        for path in changed
        if re.fullmatch(r"(?:scripts|tests)/[^/]*v665_v6[^/]*\.py", path)
    ]
    return sorted(set(paths))


def privacy_patterns() -> dict[str, re.Pattern[str]]:
    return {
        "raw_task_or_thread_identifier": re.compile(
            "(" + "source_" + "thread_id|" + "thread" + "Id|" + "task" + "Id)", re.I
        ),
        "private_absolute_path": re.compile(r"[A-Z]:\\(?:Users|GHC-Archives)\\", re.I),
        "credential_or_token_value": re.compile(
            r"(Bearer\s+[A-Za-z0-9._~-]+|api[_-]?key\s*[:=]\s*[\"']?[A-Za-z0-9])",
            re.I,
        ),
        "session_identifier_value": re.compile(
            r"session[_ -]?(?:id|stream)\s*[:=]\s*[\"']?[A-Za-z0-9]", re.I
        ),
        "private_callable_identifier_value": re.compile(
            r"(?:callable|tool)[_ -]?id\s*[:=]\s*[\"']?[A-Za-z0-9]", re.I
        ),
    }


def security_findings(path: str, text: str) -> list[dict[str, Any]]:
    findings = []
    tree = ast.parse(text, filename=path)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        else:
            name = ""
        if name in {"eval", "exec", "system", "popen"}:
            findings.append({"path": path, "line": node.lineno, "class": name})
        if name in {"run", "Popen", "call", "check_call", "check_output"}:
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "class": "subprocess_shell_true"})
    return findings


def canonical_checks(final: str) -> dict[str, Any]:
    detail: dict[str, bool] = {}
    evidence: dict[str, Any] = {}

    def check(name: str, condition: bool, value: Any = None) -> None:
        detail[name] = bool(condition)
        if value is not None:
            evidence[name] = value

    local = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    clean_before = git_text("status", "--porcelain=v1") == ""
    check("exact_final_head", local == final, local)
    check("exact_branch", branch == BRANCH, branch)
    check("upstream_equal", upstream == final, upstream)
    check("tracking_equal", tracking == final, tracking)
    check("fresh_live_equal", live == final, live)
    check("four_way_equal", len({local, upstream, tracking, live}) == 1)
    check("zero_divergence", divergence == ["0", "0"], divergence)
    check("clean_before", clean_before)

    check("final_parent_evidence", git_text("rev-parse", "HEAD^") == EVIDENCE)
    check("evidence_parent_x1", git_text("rev-parse", f"{EVIDENCE}^") == X1)
    check("x1_parent_source", git_text("rev-parse", f"{X1}^") == SOURCE)
    commit_count = int(git_text("rev-list", "--count", f"{SOURCE}..{final}"))
    merges = git_text("rev-list", "--merges", f"{SOURCE}..{final}").splitlines()
    check("exact_three_phase_commits", commit_count == 3, commit_count)
    check("zero_merges", not merges, len(merges))
    for label, commit in (("x1", X1), ("evidence", EVIDENCE), ("final", final)):
        parents = git_text("show", "-s", "--format=%P", commit).split()
        check(f"{label}_one_parent", len(parents) == 1, len(parents))

    final_statuses = git_text("diff", "--name-status", f"{EVIDENCE}..{final}").splitlines()
    check("final_delta_nonempty", bool(final_statuses), len(final_statuses))
    check("final_delta_additive_only", all(row.startswith("A\t") for row in final_statuses))
    source_statuses = git_text("diff", "--name-status", f"{SOURCE}..{final}").splitlines()
    check("source_to_final_zero_deletions", not any(row.startswith("D\t") for row in source_statuses))
    check("phase_commit_cap", commit_count <= 8)

    manifests = [
        replay_manifest(X1, PHASE_PREFIX + "validation/x1-content-manifest.json"),
        replay_manifest(EVIDENCE, PHASE_PREFIX + "validation/evidence-content-manifest.json"),
        replay_manifest(final, PHASE_PREFIX + "validation/final-delta-manifest.json"),
        replay_manifest(final, PHASE_PREFIX + "validation/final-owner-manifest.json"),
    ]
    for row in manifests:
        check("manifest_" + row["phase"] + "_replay", row["passed"], row["entries"])
    check("x1_manifest_entries_18", manifests[0]["entries"] == 18)
    check("evidence_manifest_entries_115", manifests[1]["entries"] == 115)

    paths = owner_paths(final)
    blobs = batch_blobs([f"{final}:{path}" for path in paths])
    blob_map = dict(zip(paths, blobs))
    check("owner_file_cap", len(paths) <= 2000, len(paths))

    json_failures = []
    json_count = 0
    privacy_hits = []
    python_count = 0
    compile_failures = []
    security = []
    word_cap_failures = []
    max_words = 0
    max_word_path = ""
    crlf_paths = []
    patterns = privacy_patterns()
    for path, blob in blob_map.items():
        if b"\r\n" in blob:
            crlf_paths.append(path)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            privacy_hits.append({"class": "non_utf8_owner_file", "path": path})
            continue
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(text)
            except Exception as exc:
                json_failures.append({"path": path, "error": type(exc).__name__})
        if path.endswith(".py"):
            python_count += 1
            try:
                compile(text, path, "exec")
                security.extend(security_findings(path, text))
            except Exception as exc:
                compile_failures.append({"path": path, "error": type(exc).__name__})
        words = len(re.findall(r"\S+", text))
        if words > max_words:
            max_words, max_word_path = words, path
        if words > 100_000:
            word_cap_failures.append(path)
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                privacy_hits.append({"class": class_name, "path": path})
    check("all_owner_json_parse", not json_failures, json_count)
    check("owner_python_compile", not compile_failures, python_count)
    check("bounded_python_security_zero", not security, len(security))
    check("five_class_privacy_zero", not privacy_hits, len(privacy_hits))
    check("utf8_lf_owner_blobs", not crlf_paths, len(crlf_paths))
    check("document_word_caps", not word_cap_failures, {"max": max_words, "path": max_word_path})

    report = blob_map[PHASE_PREFIX + "reports/static-report.html"].decode("utf-8").casefold()
    html_markers = ("<html lang=\"en-nz\"", "skip-link", "<main", "<h1", "<caption", "prefers-reduced-motion")
    check("static_report_structure", all(marker in report for marker in html_markers))
    check("static_report_no_script_or_form", "<script" not in report and "<form" not in report)
    check("manual_accessibility_reserved", all(term in report for term in ("screen-reader", "refreshable-braille-display", "affected-user")))

    truth = json.loads(blob_map[PHASE_PREFIX + "closeout/phase-truth.json"])
    negative = json.loads(blob_map[PHASE_PREFIX + "closeout/retained-negative-register.json"])
    flow = json.loads(blob_map[PHASE_PREFIX + "closeout/method-flow-final.json"])
    gates = json.loads(blob_map[PHASE_PREFIX + "closeout/exact-open-gate-register.json"])
    route = json.loads(blob_map[PHASE_PREFIX + "orchestration/route-state-final-candidate.json"])
    seal = json.loads(blob_map[PHASE_PREFIX + "seal/seal-candidate.json"])
    freeze = json.loads(blob_map[PHASE_PREFIX + "x1/proposal-freeze.json"])
    ledger = json.loads(blob_map[PHASE_PREFIX + "x2/proposal-ledger.json"])
    portfolio = json.loads(blob_map[PHASE_PREFIX + "x2/portfolio-execution.json"])
    prerequisites = json.loads(blob_map[PHASE_PREFIX + "final/final-validation-prerequisites.json"])
    check("frozen_total_4130", truth["new_frozen_total"] == 4130)
    check("outcomes_14_4_1_1", truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    check("proposal_ledger_matches_truth", ledger["outcome_counts"] == truth["outcomes"])
    check("twenty_new_proposals", len(freeze["new_proposals"]) == 20)
    check("hundred_mutations_rejected", ledger["rejected_mutation_count"] == 100 and ledger["accepted_mutation_count"] == 0)
    check("effective_negatives_25797", negative["effective_total"] == 25797)
    check("effective_methods_9769", flow["effective_total"] == 9769)
    check("effective_open_gaps_180", gates["effective_open_gaps"] == 180)
    check("effective_exact_gates_178", gates["effective_exact_gates"] == 178)
    check("no_failure_erased", negative["no_failure_erased"] and flow["no_failure_erased"])
    check("twenty_five_failures_retained", len(negative["startup_and_operational_failure_ids"]) == 25)
    check("terminal_not_ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and seal["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("zero_real_rows", truth["real_rows"] == 0)
    check("zero_participants", truth["participants"] == 0)
    check("zero_phase_network_calls", truth["network_calls_by_phase_software"] == 0)
    check("zero_external_actions", truth["external_actions"] == 0)
    check("route_prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and not route["sent_by_caelen_morrow"])
    check("zero_route_contacts", route["successor_contact_count"] == route["standby_contact_count"] == route["task_creation_count"] == 0)
    check("prospective_eiren_only", route["prospective_recipient_title"] == "Eiren Kestrel")
    baton_path = route["prepared_baton"]
    baton_blob = blob_map[baton_path]
    baton_words = len(re.findall(r"\S+", baton_blob.decode("utf-8")))
    check("baton_word_cap", 10_000 <= baton_words <= 100_000, baton_words)
    check("baton_hash", hashlib.sha256(baton_blob).hexdigest() == route["prepared_baton_sha256"])
    check("exact_approval_unexecuted", all(row["x2_status"] == "unexecuted_exact_gate" for row in portfolio["exact_approval_packets"]))
    check("blocked_unexecuted", all(row["x2_status"] == "unexecuted_blocked" for row in portfolio["blocked_packets"]))
    check("no_global_installations", portfolio["global_installations"] == 0)
    check("three_named_test_exclusions", {row["test_id"] for row in prerequisites["excluded_evidence_lifecycle_tests"]} == EXCLUDED_TESTS)
    check("test_exclusion_zero_credit", prerequisites["exclusion_credit"] == 0)
    check("full_repository_suite_false", prerequisites["full_repository_suite"] is False)
    check("one_shot_required", prerequisites["one_shot_external_receipt_required"] and prerequisites["never_replay_complete_success"])

    final_review = json.loads(blob_map[PHASE_PREFIX + "validation/final-staged-review.json"])
    check("final_staged_review_valid", final_review["valid"] and all(final_review["checks"].values()))
    check("final_review_zero_privacy_hits", final_review["privacy_confirmed_hits"] == 0)
    check("canonical_not_invoked_in_commit", not final_review["canonical_aggregate_invoked"] and not truth["canonical_completion_invoked"])

    final_delta_paths = set(git_text("diff", "--name-only", f"{EVIDENCE}..{final}").splitlines())
    delta_manifest = manifests[2]
    expected_delta_manifest_paths = final_delta_paths - {PHASE_PREFIX + "validation/final-delta-manifest.json"}
    check("final_delta_manifest_coverage", set(delta_manifest["entry_paths"]) == expected_delta_manifest_paths)
    owner_manifest = manifests[3]
    owner_exclusions = set(owner_manifest["self_exclusions"])
    check("final_owner_manifest_coverage", set(owner_manifest["entry_paths"]) == set(paths) - owner_exclusions)

    tests = run_selected_tests()
    check("selected_owner_tests_pass", tests["passed"], {key: tests[key] for key in ("discovered", "selected", "excluded", "run", "failures", "errors", "skipped")})

    fresh_live_after = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    clean_after = git_text("status", "--porcelain=v1") == ""
    check("fresh_live_equal_after", fresh_live_after == final, fresh_live_after)
    check("clean_after", clean_after)

    minimal = {
        "head_branch": detail["exact_final_head"] and detail["exact_branch"],
        "four_way_equality": detail["four_way_equal"] and detail["zero_divergence"] and detail["fresh_live_equal_after"],
        "clean_state": detail["clean_before"] and detail["clean_after"],
        "ancestry": detail["final_parent_evidence"] and detail["evidence_parent_x1"] and detail["x1_parent_source"],
        "history_shape": detail["exact_three_phase_commits"] and detail["zero_merges"] and detail["x1_one_parent"] and detail["evidence_one_parent"] and detail["final_one_parent"],
        "manifests": all(row["passed"] for row in manifests) and detail["final_delta_manifest_coverage"] and detail["final_owner_manifest_coverage"],
        "tests": detail["selected_owner_tests_pass"],
        "json": detail["all_owner_json_parse"],
        "python": detail["owner_python_compile"] and detail["bounded_python_security_zero"],
        "privacy": detail["five_class_privacy_zero"],
        "accessibility_structure": detail["static_report_structure"] and detail["manual_accessibility_reserved"],
        "truth_counts": detail["outcomes_14_4_1_1"] and detail["effective_negatives_25797"] and detail["effective_methods_9769"] and detail["effective_open_gaps_180"] and detail["effective_exact_gates_178"],
        "boundaries": detail["zero_real_rows"] and detail["zero_participants"] and detail["zero_external_actions"] and detail["terminal_not_ready"],
        "route": detail["route_prepared_not_sent"] and detail["zero_route_contacts"] and detail["prospective_eiren_only"],
        "caps": detail["owner_file_cap"] and detail["document_word_caps"] and detail["phase_commit_cap"] and detail["baton_word_cap"],
    }
    if len(minimal) != 15:
        raise RuntimeError("minimal check count is not 15")
    passed = all(detail.values()) and all(minimal.values())
    return {
        "passed": passed,
        "detailed": detail,
        "detailed_evidence": evidence,
        "detailed_count": len(detail),
        "detailed_passed": sum(detail.values()),
        "minimal": minimal,
        "minimal_count": len(minimal),
        "minimal_passed": sum(minimal.values()),
        "tests": tests,
        "manifests": [{key: row[key] for key in ("manifest_path", "phase", "entries", "failures", "passed")} for row in manifests],
        "owner_file_count": len(paths),
        "owner_json_count": json_count,
        "changed_python_count": python_count,
        "privacy_scan_file_count": len(paths),
        "privacy_scan_classes": list(patterns),
        "privacy_confirmed_hits": len(privacy_hits),
        "bounded_security_findings": len(security),
        "maximum_document_words": max_words,
        "maximum_document_path": max_word_path,
        "full_repository_suite_run": False,
        "same_owner": True,
        "independent_reproduction": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt-dir", required=True)
    args = parser.parse_args()
    expected_final = args.expected_final.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", expected_final):
        parser.error("--expected-final must be a full lowercase SHA-1")
    receipt_dir = Path(args.receipt_dir)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    stem = f"caelen-morrow-v665-v6-{expected_final}"
    lock_path = receipt_dir / f"{stem}.lock.json"
    receipt_path = receipt_dir / f"{stem}.canonical-receipt.json"
    try:
        descriptor = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        print(json.dumps({"status": "REFUSED_EXISTING_EXCLUSIVE_GUARD", "expected_final": expected_final}, sort_keys=True))
        return 3
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
        json.dump({"status": "STARTED", "expected_final": expected_final, "started_at_utc": now()}, handle, sort_keys=True)
        handle.write("\n")
    started = now()
    try:
        checks = canonical_checks(expected_final)
        status = "PASS" if checks["passed"] else "FAIL"
        payload = {
            "schema": "ghc.family.caelen-morrow.v665-v6.external-canonical-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "status": status,
            "started_at_utc": started,
            "finished_at_utc": now(),
            "exact_final": expected_final,
            "branch": BRANCH,
            "source_sha": SOURCE,
            "x1_sha": X1,
            "evidence_sha": EVIDENCE,
            "canonical_invocation_count": 1,
            "replay": False,
            "aggregate_success_credit": 1 if status == "PASS" else 0,
            "checks": checks,
            "claim_boundary": "bounded same-owner owner-delta validation under shared infrastructure only; not a full repository suite, independent reproduction, external audit, production certification, exhaustive security, privacy or accessibility completeness, professional validation, legal or cultural review, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, or Stage 20 authority",
        }
    except Exception as exc:
        payload = {
            "schema": "ghc.family.caelen-morrow.v665-v6.external-canonical-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "status": "ERROR",
            "started_at_utc": started,
            "finished_at_utc": now(),
            "exact_final": expected_final,
            "canonical_invocation_count": 1,
            "replay": False,
            "aggregate_success_credit": 0,
            "error_class": type(exc).__name__,
            "error_message": str(exc)[:500],
        }
    payload_sha = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    receipt = {"payload_sha256": payload_sha, "payload": payload}
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    lock_path.write_text(
        json.dumps(
            {
                "status": payload["status"],
                "expected_final": expected_final,
                "receipt_filename": receipt_path.name,
                "payload_sha256": payload_sha,
                "finished_at_utc": payload["finished_at_utc"],
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    output = {
        "status": payload["status"],
        "expected_final": expected_final,
        "receipt_filename": receipt_path.name,
        "payload_sha256": payload_sha,
        "canonical_invocation_count": 1,
        "aggregate_success_credit": payload["aggregate_success_credit"],
    }
    if payload["status"] == "PASS":
        output.update(
            {
                "tests": payload["checks"]["tests"]["run"],
                "detailed": payload["checks"]["detailed_count"],
                "minimal": payload["checks"]["minimal_count"],
                "json": payload["checks"]["owner_json_count"],
                "privacy_files": payload["checks"]["privacy_scan_file_count"],
                "manifest_entries": sum(row["entries"] for row in payload["checks"]["manifests"]),
            }
        )
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
