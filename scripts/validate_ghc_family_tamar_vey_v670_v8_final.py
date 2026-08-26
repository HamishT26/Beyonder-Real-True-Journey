"""One-shot exact-final owner-scoped canonical validator for Tamar v670-v8."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "tamar-vey" / "v670-v8"
OWNER = "Tamar Vey"
PHASE = "v670-v8"
BRANCH = "codex/GHC-Family/tamar-vey-v670-v8-full-tools"
SOURCE_FINAL = "65142e05e70b507d7f15247c4154d8d6013ca046"
X1_COMMIT = "0654a2bb72fd2a121ff3e7b05652e5b38005ec14"
EVIDENCE_COMMIT = "62cd89e3bfbd6d20ecf39894a65a500070c2f808"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
COUNTS = {
    "effective_negatives": 33318,
    "effective_methods": 19594,
    "failed_witnesses": 5139,
    "bounded_passing_witnesses": 6633,
    "open_gaps": 255,
    "exact_gates": 250,
}
RUNNER_PATHS = {
    "scripts/ghc_family_calculator_asset_identity.py",
    "scripts/ghc_family_calculator_stepped_drum_topology.py",
    "scripts/ghc_family_calculator_pinwheel_vacancy.py",
    "scripts/ghc_family_calculator_operation_trace.py",
    "scripts/ghc_family_calculator_carry_nonconversion.py",
    "scripts/ghc_family_calculator_energization_abstention.py",
    "scripts/ghc_family_calculator_privacy_quarantine.py",
    "scripts/ghc_family_calculator_accessible_status.py",
    "scripts/ghc_family_calculator_correction_readback.py",
    "scripts/ghc_family_calculator_workload_handover.py",
}
BOUNDARY = (
    "Bounded owner-local software evidence under shared infrastructure only; not a full-repository "
    "suite, independent reproduction, external audit, empirical validation, professional "
    "certification, production readiness, legal or cultural ratification, Māori-authority review, "
    "complete privacy or accessibility assurance, exhaustive security, proof, canon, or Stage 20 authority."
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_receipt(path: Path, payload: dict[str, Any], *, exclusive: bool = False) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if exclusive:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    else:
        path.write_text(text, encoding="utf-8", newline="\n")


def tree_objects(commit: str) -> dict[str, tuple[str, str]]:
    rows = git_text("ls-tree", "-r", commit).splitlines()
    result: dict[str, tuple[str, str]] = {}
    for row in rows:
        left, path = row.split("\t", 1)
        mode, _kind, object_id = left.split()
        result[path] = (mode, object_id)
    return result


def batch_blobs(object_ids: list[str]) -> list[bytes | None]:
    if not object_ids:
        return []
    payload = b"".join(object_id.encode("ascii") + b"\n" for object_id in object_ids)
    result = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=ROOT, input=payload, capture_output=True, check=True
    )
    stream = result.stdout
    offset = 0
    blobs: list[bytes | None] = []
    for _object_id in object_ids:
        end = stream.find(b"\n", offset)
        if end < 0:
            raise ValueError("truncated git cat-file batch header")
        header = stream[offset:end]
        offset = end + 1
        if header.endswith(b" missing"):
            blobs.append(None)
            continue
        size = int(header.rsplit(b" ", 1)[1])
        blob = stream[offset : offset + size]
        offset += size
        if stream[offset : offset + 1] != b"\n":
            raise ValueError("truncated git cat-file batch separator")
        offset += 1
        blobs.append(blob)
    return blobs


def replay_manifest(head: str, relative: str) -> dict[str, Any]:
    manifest = load(f"validation/{relative}")
    objects = tree_objects(head)
    missing = [row["path"] for row in manifest["entries"] if row["path"] not in objects]
    blobs = (
        batch_blobs([objects[row["path"]][1] for row in manifest["entries"]])
        if not missing
        else []
    )
    mismatches = []
    if not missing:
        for row, blob in zip(manifest["entries"], blobs, strict=True):
            if (
                blob is None
                or len(blob) != row["bytes"]
                or hashlib.sha256(blob).hexdigest() != row["sha256"]
                or ("mode" in row and objects[row["path"]][0] != row["mode"])
            ):
                mismatches.append(row["path"])
    return {
        "valid": not missing and not mismatches,
        "entries": manifest["entry_count"],
        "self_exclusions": manifest["self_exclusions"],
        "missing": missing,
        "mismatches": mismatches,
        "paths": [row["path"] for row in manifest["entries"]],
    }


def is_owner_path(path: str) -> bool:
    if path.startswith("docs/tamar-vey/v670-v8/") or path in RUNNER_PATHS:
        return True
    return bool(
        re.fullmatch(
            r"(?:scripts|tests)/(?:build_|validate_|test_)?ghc_family_tamar_(?:vey_)?v670_v8_.+\.py",
            path,
        )
    )


def current_equality() -> dict[str, Any]:
    local = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    divergence = [
        int(value)
        for value in git_text(
            "rev-list", "--left-right", "--count", "HEAD...@{upstream}"
        ).split()
    ]
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": local == upstream == tracking == live,
        "ahead": divergence[0],
        "behind": divergence[1],
    }


def check(name: str, passed: bool, observed: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "observed": observed}


def canonical_payload() -> dict[str, Any]:
    started = now_utc()
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    before_equality = current_equality()
    clean_before = git_text("status", "--porcelain=v1") == ""
    parent = git_text("rev-parse", "HEAD^")
    parent_count = len(git_text("rev-list", "--parents", "-n", "1", "HEAD").split()) - 1
    commit_count = int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..HEAD"))
    merge_count = int(git_text("rev-list", "--count", "--merges", f"{SOURCE_FINAL}..HEAD"))
    x1_parent = git_text("rev-parse", f"{X1_COMMIT}^")
    evidence_parent = git_text("rev-parse", f"{EVIDENCE_COMMIT}^")

    test_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_ghc_family_tamar_vey_v670_v8_final",
            "-v",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
    )
    test_output = test_result.stdout + test_result.stderr
    test_match = re.search(r"Ran\s+(\d+)\s+tests", test_output)
    test_count = int(test_match.group(1)) if test_match else 0

    json_paths = sorted(OWNER_ROOT.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append(
                {"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__}
            )

    x1_manifest = replay_manifest(head, "x1-manifest.json")
    evidence_manifest = replay_manifest(head, "evidence-manifest.json")
    delta_manifest = replay_manifest(head, "final-delta-manifest.json")
    owner_manifest = replay_manifest(head, "final-owner-manifest.json")
    changed_delta = set(git_text("diff", "--name-only", f"{EVIDENCE_COMMIT}..HEAD").splitlines())
    expected_delta = set(delta_manifest["paths"]) | set(delta_manifest["self_exclusions"])
    changed_owner = {
        path
        for path in git_text("diff", "--name-only", f"{SOURCE_FINAL}..HEAD").splitlines()
        if is_owner_path(path)
    }
    expected_owner = set(owner_manifest["paths"]) | set(owner_manifest["self_exclusions"])

    phase = load("closeout/phase-truth.json")
    route = load("orchestration/route-state-final-candidate.json")
    canonical_state = load("final/canonical-invocation-state.json")
    staged_review = load("validation/final-staged-review.json")
    privacy_receipt = load("validation/final-staged-privacy.json")
    validation_receipt = load("validation/final-validation-receipt.json")
    method_receipt = load("validation/final-method-flow-validation.json")
    precommit_receipt = load("validation/final-precommit-test-receipt.json")
    skill_summary = load("closeout/skill-runner-tool-summary.json")
    mutation_receipt = load("x2/mutation-receipt.json")
    exact_blocked = load("x2/exact-and-blocked-register.json")

    detailed = [
        check("exact_branch", branch == BRANCH, branch),
        check("final_parent_is_evidence", parent == EVIDENCE_COMMIT, parent),
        check("x1_parent_is_source", x1_parent == SOURCE_FINAL, x1_parent),
        check("evidence_parent_is_x1", evidence_parent == X1_COMMIT, evidence_parent),
        check("source_is_ancestor", git("merge-base", "--is-ancestor", SOURCE_FINAL, head, check=False).returncode == 0, SOURCE_FINAL),
        check("x1_is_ancestor", git("merge-base", "--is-ancestor", X1_COMMIT, head, check=False).returncode == 0, X1_COMMIT),
        check("evidence_is_ancestor", git("merge-base", "--is-ancestor", EVIDENCE_COMMIT, head, check=False).returncode == 0, EVIDENCE_COMMIT),
        check("three_phase_commits", commit_count == 3, commit_count),
        check("zero_merges", merge_count == 0, merge_count),
        check("one_final_parent", parent_count == 1, parent_count),
        check("clean_before", clean_before, clean_before),
        check("zero_divergence_before", before_equality["ahead"] == 0 and before_equality["behind"] == 0, {"ahead": before_equality["ahead"], "behind": before_equality["behind"]}),
        check("four_way_equal_before", before_equality["four_way_equal"], before_equality),
        check("x1_manifest_replay", x1_manifest["valid"], {"entries": x1_manifest["entries"], "missing": len(x1_manifest["missing"]), "mismatches": len(x1_manifest["mismatches"])}),
        check("evidence_manifest_replay", evidence_manifest["valid"], {"entries": evidence_manifest["entries"], "missing": len(evidence_manifest["missing"]), "mismatches": len(evidence_manifest["mismatches"])}),
        check("final_delta_manifest_replay", delta_manifest["valid"], {"entries": delta_manifest["entries"], "missing": len(delta_manifest["missing"]), "mismatches": len(delta_manifest["mismatches"])}),
        check("final_owner_manifest_replay", owner_manifest["valid"], {"entries": owner_manifest["entries"], "missing": len(owner_manifest["missing"]), "mismatches": len(owner_manifest["mismatches"])}),
        check("final_delta_coverage", changed_delta == expected_delta, {"changed": len(changed_delta), "expected": len(expected_delta)}),
        check("final_owner_coverage", changed_owner == expected_owner, {"changed": len(changed_owner), "expected": len(expected_owner)}),
        check("staged_review_valid", staged_review["valid"] and not staged_review["out_of_scope"] and not staged_review["frozen_x1_or_evidence_mutations"], staged_review["valid"]),
        check("privacy_receipt_valid", privacy_receipt["valid"] and privacy_receipt["confirmed_hit_count"] == 0, privacy_receipt["confirmed_hit_count"]),
        check("validation_receipt_valid", validation_receipt["valid"] and validation_receipt["stale_label_review_valid"] and not validation_receipt["json_issues"] and not validation_receipt["python_compile_issues"] and not validation_receipt["stale_label_unexpected"], validation_receipt["valid"]),
        check("method_receipt_valid", method_receipt["valid"] and method_receipt["issue_count"] == 0, method_receipt["issue_count"]),
        check("precommit_receipt_valid", precommit_receipt["valid"] and precommit_receipt["tests"] == 25, {"valid": precommit_receipt["valid"], "tests": precommit_receipt["tests"]}),
        check("phase_outcomes_exact", phase["outcomes"] == OUTCOMES, phase["outcomes"]),
        check("phase_counts_exact", all(phase[key] == value for key, value in COUNTS.items()), {key: phase[key] for key in COUNTS}),
        check("gap_gate_totals_exact", phase["open_gaps"] == 255 and phase["exact_gates"] == 250, {"open_gaps": phase["open_gaps"], "exact_gates": phase["exact_gates"]}),
        check("terminal_verdict_exact", phase["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase["terminal_verdict"]),
        check("route_prepared_not_sent", route["delivery_state"] == "PREPARED_NOT_SENT" and route["successor_contact_count"] == 0, route["delivery_state"]),
        check("canonical_state_precommit", canonical_state["state"] == "NOT_INVOKED_PRECOMMIT" and canonical_state["invocation_count"] == 0, canonical_state),
    ]

    changed_text = [
        path
        for path in sorted(changed_owner)
        if Path(path).suffix.lower() in {".py", ".json", ".md", ".html", ".txt", ".yaml"}
    ]
    objects = tree_objects(head)
    text_blobs = batch_blobs([objects[path][1] for path in changed_text])
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "transcript_or_session_stream": re.compile(r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I),
    }
    scanner_surfaces = {path for path in changed_text if path.startswith(("scripts/", "tests/"))}
    privacy_candidates = []
    for path, blob in zip(changed_text, text_blobs, strict=True):
        if blob is None:
            privacy_candidates.append({"path": path, "class": "missing_blob", "disposition": "confirmed_payload_hit"})
            continue
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            privacy_candidates.append({"path": path, "class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        for label, pattern in privacy_patterns.items():
            if pattern.search(text):
                privacy_candidates.append({"path": path, "class": label, "disposition": "scanner_definition_or_unit_test" if path in scanner_surfaces else "confirmed_payload_hit"})
    confirmed_privacy = [row for row in privacy_candidates if row["disposition"] == "confirmed_payload_hit"]

    changed_python = [path for path in sorted(changed_owner) if path.endswith(".py")]
    security_findings = []
    for path in changed_python:
        blob = batch_blobs([objects[path][1]])[0]
        try:
            source = blob.decode("utf-8") if blob is not None else ""
            compile(source, path, "exec")
            ast.parse(source, filename=path)
        except (UnicodeDecodeError, SyntaxError) as exc:
            security_findings.append({"path": path, "issue": type(exc).__name__})

    docs = [
        path
        for path in OWNER_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
    ]
    max_words = max((len(path.read_text(encoding="utf-8").split()) for path in docs), default=0)
    materialized = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])

    after_equality = current_equality()
    clean_after = git_text("status", "--porcelain=v1") == ""
    minimal = [
        check("final_tests_25", test_result.returncode == 0 and test_count == 25, {"tests": test_count, "exit": test_result.returncode}),
        check("strict_json", not json_issues, {"documents": len(json_paths), "issues": len(json_issues)}),
        check("five_class_privacy", not confirmed_privacy, {"scanned": len(changed_text), "candidates": len(privacy_candidates), "confirmed": len(confirmed_privacy)}),
        check("bounded_python_security", not security_findings, {"files": len(changed_python), "findings": len(security_findings)}),
        check("file_cap", materialized < 2000, materialized),
        check("word_cap", max_words < 100000, max_words),
        check("twenty_skills", skill_summary["skills"]["smoke_used"] == 20, skill_summary["skills"]),
        check("ten_runners", skill_summary["runners"]["passed"] == 10, skill_summary["runners"]),
        check("three_tools", skill_summary["tools"]["built"] == 3, skill_summary["tools"]),
        check("mutations_160", mutation_receipt["executed"] == 160 and mutation_receipt["rejected"] == 160, {"executed": mutation_receipt["executed"], "rejected": mutation_receipt["rejected"]}),
        check("exact_blocked_unexecuted", exact_blocked["executed"] == 0, exact_blocked["executed"]),
        check("full_suite_not_run", phase["full_repository_suite"] == "not_run_not_claimed", phase["full_repository_suite"]),
        check("not_independent_reproduction", phase["same_owner_independent_reproduction"] is False, phase["same_owner_independent_reproduction"]),
        check("clean_after", clean_after, clean_after),
        check("four_way_after", after_equality["four_way_equal"] and after_equality["ahead"] == 0 and after_equality["behind"] == 0, after_equality),
    ]

    detailed_passed = sum(row["passed"] for row in detailed)
    minimal_passed = sum(row["passed"] for row in minimal)
    valid = detailed_passed == 30 and minimal_passed == 15
    core = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v2",
        "owner": OWNER,
        "phase": PHASE,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "started_at_utc": started,
        "completed_at_utc": now_utc(),
        "invocation_count": 1,
        "success_count": 1 if valid else 0,
        "replay_count": 0,
        "branch": branch,
        "exact_final": head,
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "tests": {"passed": test_count if test_result.returncode == 0 else 0, "total": 25, "exit_code": test_result.returncode, "output_sha256": hashlib.sha256(test_output.encode("utf-8")).hexdigest()},
        "detailed_checks": {"passed": detailed_passed, "total": 30, "rows": detailed},
        "minimal_checks": {"passed": minimal_passed, "total": 15, "rows": minimal},
        "json_documents": len(json_paths),
        "json_issues": json_issues,
        "privacy": {"scanned_text_files": len(changed_text), "pattern_classes": sorted(privacy_patterns), "candidates": privacy_candidates, "confirmed_hits": confirmed_privacy},
        "security": {"changed_python_files": len(changed_python), "findings": security_findings},
        "manifests": {"x1": x1_manifest["entries"], "evidence": evidence_manifest["entries"], "final_delta": delta_manifest["entries"], "final_owner": owner_manifest["entries"]},
        "lifecycle": {"phase_commits": commit_count, "merges": merge_count, "final_parents": parent_count, "clean_before": clean_before, "clean_after": clean_after, "before_equality": before_equality, "after_equality": after_equality},
        "caps": {"materialized_files": materialized, "file_guard": 2000, "max_document_words": max_words, "word_guard": 100000},
        "outcomes": OUTCOMES,
        "counts": COUNTS,
        "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    core["canonical_payload_sha256"] = hashlib.sha256(
        json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return core


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt).resolve()
    if receipt.suffix.lower() != ".json":
        raise SystemExit("canonical receipt must be an exact JSON path")
    if receipt.is_relative_to(ROOT.resolve()):
        raise SystemExit("canonical receipt must remain external to the repository")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    running = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v2",
        "owner": OWNER,
        "phase": PHASE,
        "status": "INVOKED_RUNNING_NO_REPLAY",
        "started_at_utc": now_utc(),
        "invocation_count": 1,
        "success_count": 0,
        "replay_count": 0,
        "boundary": BOUNDARY,
    }
    try:
        write_receipt(receipt, running, exclusive=True)
    except FileExistsError as exc:
        raise SystemExit("canonical receipt already exists; replay prohibited") from exc
    try:
        payload = canonical_payload()
    except Exception as exc:
        invalid = {
            **running,
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "completed_at_utc": now_utc(),
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        write_receipt(receipt, invalid)
        raise
    write_receipt(receipt, payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "exact_final": payload["exact_final"],
                "tests": payload["tests"],
                "detailed": payload["detailed_checks"]["passed"],
                "minimal": payload["minimal_checks"]["passed"],
                "json_documents": payload["json_documents"],
                "privacy_confirmed_hits": len(payload["privacy"]["confirmed_hits"]),
                "security_findings": len(payload["security"]["findings"]),
                "canonical_payload_sha256": payload["canonical_payload_sha256"],
            },
            sort_keys=True,
        )
    )
    if payload["status"] != "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
