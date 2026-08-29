"""One-shot exact-final owner-scoped canonical validator for Eiren Kestrel v675-v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v675-v2"
OWNER = "Eiren Kestrel"
PHASE = "v675-v2"
SOURCE_FINAL = "394482bea39831b87a72aefe10a39340543070c7"
X1_COMMIT = "c8d2d107235db9a1e3a42b2d9843596a6f5c1890"
EVIDENCE_COMMIT = "f3bb95c68182c8f7ae1d469ea97443245ce9735b"
BRANCH = "codex/GHC-Family/eiren-kestrel-v675-v2-full-tools"
TEST_PATH = "tests/test_ghc_family_eiren_kestrel_v675_v2_final.py"
X1_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/x1-manifest.json"
EVIDENCE_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/evidence-manifest.json"
DELTA_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/final-delta-manifest.json"
OWNER_MANIFEST = "docs/eiren-kestrel/v675-v2/validation/final-owner-manifest.json"
BOUNDARY = (
    "Same-owner local software and documentation validation is not independent reproduction, external audit, "
    "production certification, exhaustive security, complete privacy or accessibility assurance, professional "
    "validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, "
    "Theory-of-Everything proof, AGI/ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority."
)


def resolve_git_executable() -> str:
    candidate = shutil.which("git")
    if candidate is None:
        raise RuntimeError("git executable is required")
    return candidate


GIT_EXE = resolve_git_executable()


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(  # nosec B603
        [GIT_EXE, *args], cwd=ROOT, check=check, capture_output=True
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def commit_blob(commit: str, path: str) -> bytes:
    return normalized(git("show", f"{commit}:{path}").stdout)


def commit_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(commit_blob(commit, path).decode("utf-8"))


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def check(name: str, passed: bool, observed: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "observed": observed}


def write_receipt(path: Path, payload: dict[str, Any], *, exclusive: bool = False) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    except Exception:
        if exclusive and path.exists():
            path.unlink()
        raise


def replay_manifest(commit: str, relative: str) -> dict[str, Any]:
    payload = commit_json(commit, relative)
    issues = []
    for entry in payload["entries"]:
        path = entry["path"]
        try:
            blob = commit_blob(commit, path)
            mode = git_text("ls-tree", commit, "--", path).split()[0]
        except (subprocess.CalledProcessError, IndexError) as exc:
            issues.append({"path": path, "issue": f"missing:{exc}"})
            continue
        if len(blob) != entry["bytes"]:
            issues.append({"path": path, "issue": "length_mismatch"})
        if sha256(blob) != entry["sha256"]:
            issues.append({"path": path, "issue": "sha256_mismatch"})
        if mode != entry["mode"]:
            issues.append({"path": path, "issue": "mode_mismatch"})
    return {
        "path": relative,
        "entries": payload["entry_count"],
        "self_exclusions": payload["self_exclusions"],
        "issues": issues,
        "valid": not issues and payload["entry_count"] == len(payload["entries"]),
    }


RUNNER_NAMES = {
    "ghc_family_tinsmith_work_identity.py",
    "ghc_family_pattern_piece_relations.py",
    "ghc_family_seam_taxonomy_guard.py",
    "ghc_family_form_geometry_vacancy.py",
    "ghc_family_tin_condition_cue.py",
    "ghc_family_tinsmith_correction_chain.py",
    "ghc_family_tin_privacy_minimizer.py",
    "ghc_family_thos_seam_quarantine.py",
    "ghc_family_freed_id_tinsmith_envelope.py",
    "ghc_family_cbr_tinsmith_response.py",
}


def is_owner_path(path: str) -> bool:
    if path.startswith("docs/eiren-kestrel/v675-v2/"):
        return True
    if path.startswith("scripts/") and (
        "eiren_kestrel_v675_v2" in path or Path(path).name in RUNNER_NAMES
    ):
        return True
    return path.startswith("tests/test_ghc_family_eiren_kestrel_v675_v2_")


def current_equality() -> dict[str, Any]:
    local = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}")
    clean = not git_text("status", "--porcelain=v1")
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "divergence": divergence,
        "clean": clean,
        "four_way_equal": local == upstream == tracking == live,
    }


def run_tests() -> dict[str, Any]:
    result = subprocess.run(  # nosec B603
        [
            sys.executable,
            "-m",
            "pytest",
            TEST_PATH,
            "-q",
            "--disable-warnings",
            "--maxfail=1",
        ],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    output = normalized(result.stdout + result.stderr)
    match = re.search(rb"(\d+) passed", output)
    passed = int(match.group(1)) if match else 0
    return {
        "exit_code": result.returncode,
        "passed": passed,
        "expected": 25,
        "output_sha256": sha256(output),
        "output_tail": output.decode("utf-8", errors="replace").splitlines()[-12:],
        "valid": result.returncode == 0 and passed == 25,
    }


def privacy_scan(head: str, owner_paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "private_absolute_path": re.compile(r"\b[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "credential_assignment": re.compile(
            r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{12,}",
            re.IGNORECASE,
        ),
        "transcript_or_session_stream": re.compile(
            r"^\s*(?:user|assistant|developer|system)\s*:", re.IGNORECASE | re.MULTILINE
        ),
        "private_callable_identifier": re.compile(r"\bmcp__[a-z0-9_]+\b", re.IGNORECASE),
    }
    suffixes = {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}
    scanned = 0
    candidates = []
    confirmed = []
    decode_issues = []
    for path in owner_paths:
        if Path(path).suffix.lower() not in suffixes:
            continue
        scanned += 1
        blob = commit_blob(head, path)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            decode_issues.append(path)
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                row = {
                    "path": path,
                    "line": text.count("\n", 0, match.start()) + 1,
                    "class": class_name,
                }
                if path.startswith(("scripts/", "tests/")):
                    row["classification"] = "scanner_definition_or_rejecting_fixture"
                    candidates.append(row)
                else:
                    confirmed.append(row)
    return {
        "classes": len(patterns),
        "scanned": scanned,
        "candidates": candidates,
        "confirmed": confirmed,
        "decode_issues": decode_issues,
        "valid": not confirmed and not decode_issues,
    }


def canonical_payload() -> dict[str, Any]:
    equality_before = current_equality()
    head = equality_before["local"]
    phase_commits = git_text("rev-list", "--reverse", f"{SOURCE_FINAL}..{head}").splitlines()
    merge_commits = git_text("rev-list", "--merges", f"{SOURCE_FINAL}..{head}").splitlines()
    parent_counts = [len(git_text("show", "-s", "--format=%P", commit).split()) for commit in phase_commits]
    tree_paths = git_text("ls-tree", "-r", "--name-only", head).splitlines()
    owner_paths = sorted(path for path in tree_paths if is_owner_path(path))
    x1_manifest = replay_manifest(X1_COMMIT, X1_MANIFEST)
    evidence_manifest = replay_manifest(EVIDENCE_COMMIT, EVIDENCE_MANIFEST)
    delta_manifest = replay_manifest(head, DELTA_MANIFEST)
    owner_manifest = replay_manifest(head, OWNER_MANIFEST)
    owner_manifest_payload = commit_json(head, OWNER_MANIFEST)
    owner_expected = {entry["path"] for entry in owner_manifest_payload["entries"]} | set(
        owner_manifest_payload["self_exclusions"]
    )
    privacy = privacy_scan(head, owner_paths)
    json_issues: list[dict[str, Any]] = []
    json_count = 0
    word_issues: list[dict[str, Any]] = []
    text_suffixes = {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}
    for path in owner_paths:
        blob = commit_blob(head, path)
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(blob.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": path, "issue": str(exc)})
        if Path(path).suffix.lower() in text_suffixes:
            try:
                words = len(blob.decode("utf-8").split())
            except UnicodeDecodeError as exc:
                word_issues.append({"path": path, "issue": str(exc)})
                continue
            if words > 100000:
                word_issues.append({"path": path, "words": words})
    changed_python = [
        path
        for path in git_text("diff", "--name-only", SOURCE_FINAL, head, "--", "*.py").splitlines()
        if path
    ]
    compile_issues: list[dict[str, Any]] = []
    for path in changed_python:
        try:
            compile(commit_blob(head, path).decode("utf-8"), path, "exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            compile_issues.append({"path": path, "issue": str(exc)})
    tests = run_tests()
    phase_truth = commit_json(head, "docs/eiren-kestrel/v675-v2/closeout/phase-truth.json")
    method_flow = commit_json(head, "docs/eiren-kestrel/v675-v2/closeout/method-flow-final.json")
    method_witnesses = commit_json(
        head, "docs/eiren-kestrel/v675-v2/closeout/method-flow-witnesses-final.json"
    )
    negatives = commit_json(head, "docs/eiren-kestrel/v675-v2/closeout/retained-negative-register.json")
    gates = commit_json(head, "docs/eiren-kestrel/v675-v2/closeout/exact-open-gate-register.json")
    review = commit_json(head, "docs/eiren-kestrel/v675-v2/validation/final-staged-review.json")
    validation = commit_json(head, "docs/eiren-kestrel/v675-v2/validation/final-validation-receipt.json")
    precommit = commit_json(
        head, "docs/eiren-kestrel/v675-v2/validation/final-precommit-test-receipt.json"
    )
    canonical_state = commit_json(head, "docs/eiren-kestrel/v675-v2/final/canonical-invocation-state.json")
    route = commit_json(head, "docs/eiren-kestrel/v675-v2/orchestration/route-state-final-candidate.json")
    seal = commit_json(head, "docs/eiren-kestrel/v675-v2/seal/content-seal.json")
    seal_issues = []
    for entry in seal["entries"]:
        path = f"docs/eiren-kestrel/v675-v2/{entry['path']}"
        blob = commit_blob(head, path)
        if len(blob) != entry["bytes"] or sha256(blob) != entry["sha256"]:
            seal_issues.append(path)
    outcomes = phase_truth["outcomes"]
    effective = phase_truth["effective_counts"]
    detailed = [
        check("tests_25", tests["valid"], tests),
        check("json_parse", not json_issues, {"parsed": json_count, "issues": json_issues}),
        check("word_ceiling", not word_issues, word_issues),
        check("owner_file_ceiling", len(owner_paths) <= 2000, len(owner_paths)),
        check("privacy_five_classes", privacy["classes"] == 5, privacy["classes"]),
        check("privacy_zero_confirmed", privacy["valid"], len(privacy["confirmed"])),
        check("python_compile", not compile_issues, compile_issues),
        check("x1_manifest", x1_manifest["valid"], x1_manifest),
        check("evidence_manifest", evidence_manifest["valid"], evidence_manifest),
        check("delta_manifest", delta_manifest["valid"], delta_manifest),
        check("owner_manifest", owner_manifest["valid"], owner_manifest),
        check("owner_manifest_coverage", owner_expected == set(owner_paths), len(owner_expected)),
        check("source_ancestral", git("merge-base", "--is-ancestor", SOURCE_FINAL, head, check=False).returncode == 0, SOURCE_FINAL),
        check("x1_ancestral", git("merge-base", "--is-ancestor", X1_COMMIT, head, check=False).returncode == 0, X1_COMMIT),
        check("evidence_ancestral", git("merge-base", "--is-ancestor", EVIDENCE_COMMIT, head, check=False).returncode == 0, EVIDENCE_COMMIT),
        check("three_phase_commits", len(phase_commits) == 3, phase_commits),
        check("zero_merges", not merge_commits, merge_commits),
        check("single_parent_commits", parent_counts == [1, 1, 1], parent_counts),
        check("final_direct_child_evidence", git_text("rev-parse", f"{head}^") == EVIDENCE_COMMIT, git_text("rev-parse", f"{head}^")),
        check("clean_before", equality_before["clean"], equality_before),
        check("zero_divergence_before", equality_before["divergence"] == "0\t0", equality_before["divergence"]),
        check("four_way_before", equality_before["four_way_equal"], equality_before),
        check("outcomes", outcomes == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, outcomes),
        check("method_counts", len(method_flow["methods"]) == 220 and method_witnesses["row_count"] == 440, method_flow["counts"]),
        check("retained_negatives", negatives["row_count"] == 220 and negatives["failures_rewritten_as_pass"] == 0, negatives["row_count"]),
        check("effective_counts", effective["effective_negatives"] == 40407 and effective["effective_methods"] == 28659, effective),
        check("gates", gates["effective_open_gaps"] == 333 and gates["effective_exact_gates"] == 325, {"gaps": gates["effective_open_gaps"], "gates": gates["effective_exact_gates"]}),
        check("review", review["valid"] and not review["issues"], review["issues"]),
        check("validation", validation["valid"], validation),
        check("precommit", precommit["valid"] and precommit["tests"] == 25, precommit),
        check("canonical_uninvoked", canonical_state["state"] == "NOT_INVOKED_PRECOMMIT" and canonical_state["invocation_count"] == 0, canonical_state),
        check(
            "route_prepared_not_sent",
            route["state"] == "PREPARED_NOT_SENT"
            and not route["sent"]
            and route["prospective_successor_title"] == "Elaren Kestrel"
            and route["prospective_successor_phase"] == "v675-v3"
            and route["successor_after_successor_title"] == "Neris Solane"
            and route["successor_after_successor_phase"] == "v675-v4",
            route,
        ),
        check("seal", not seal_issues and seal["entry_count"] == len(seal["entries"]), seal_issues),
        check("terminal_verdict", phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase_truth["terminal_verdict"]),
    ]
    minimal = [
        check("exact_head", head == equality_before["fresh_live"], head),
        check("clean", equality_before["clean"], equality_before["clean"]),
        check("zero_divergence", equality_before["divergence"] == "0\t0", equality_before["divergence"]),
        check("four_way_equal", equality_before["four_way_equal"], equality_before),
        check("final_parent", git_text("rev-parse", f"{head}^") == EVIDENCE_COMMIT, EVIDENCE_COMMIT),
        check("three_commits", len(phase_commits) == 3, len(phase_commits)),
        check("zero_merges", not merge_commits, len(merge_commits)),
        check("single_parents", parent_counts == [1, 1, 1], parent_counts),
        check("tests", tests["valid"], tests["passed"]),
        check("json", not json_issues, json_count),
        check("privacy", privacy["valid"], privacy["scanned"]),
        check("manifests", all(row["valid"] for row in [x1_manifest, evidence_manifest, delta_manifest, owner_manifest]), [x1_manifest["entries"], evidence_manifest["entries"], delta_manifest["entries"], owner_manifest["entries"]]),
        check("caps", len(owner_paths) <= 2000 and not word_issues, len(owner_paths)),
        check("not_stage20", phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase_truth["terminal_verdict"]),
        check("not_delivered", route["state"] == "PREPARED_NOT_SENT", route["state"]),
    ]
    all_valid = all(row["passed"] for row in detailed + minimal)
    equality_after = current_equality()
    all_valid = all_valid and equality_after["clean"] and equality_after["four_way_equal"]
    core = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all_valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "exact_final": head,
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "invocation_count": 1,
        "success_count": 1 if all_valid else 0,
        "replay_count": 0,
        "tests": tests,
        "detailed_checks": {"passed": sum(row["passed"] for row in detailed), "total": len(detailed), "rows": detailed},
        "minimal_checks": {"passed": sum(row["passed"] for row in minimal), "total": len(minimal), "rows": minimal},
        "owner_json_parsed": json_count,
        "owner_files": len(owner_paths),
        "privacy": privacy,
        "changed_python_files": len(changed_python),
        "python_compile_issues": compile_issues,
        "manifests": {
            "x1": x1_manifest,
            "evidence": evidence_manifest,
            "final_delta": delta_manifest,
            "final_owner": owner_manifest,
        },
        "history": {
            "phase_commits": phase_commits,
            "merges": merge_commits,
            "parent_counts": parent_counts,
            "final_parent": git_text("rev-parse", f"{head}^"),
        },
        "equality_before": equality_before,
        "equality_after": equality_after,
        "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    payload_digest = sha256(
        json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    core["canonical_payload_sha256"] = payload_digest
    return core


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt).resolve()
    if receipt.suffix.lower() != ".json":
        raise SystemExit("canonical receipt must be an exact JSON path")
    if receipt.is_relative_to(ROOT.resolve()):
        raise SystemExit("canonical receipt must remain external to repository")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    running = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "status": "RUNNING_EXCLUSIVE_LATCH",
        "invocation_count": 1,
        "success_count": 0,
        "replay_count": 0,
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
            "status": "INVALID_CANONICAL_EXCEPTION",
            "exception_type": type(exc).__name__,
            "exception": str(exc),
        }
        write_receipt(receipt, invalid)
        raise
    write_receipt(receipt, payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "exact_final": payload["exact_final"],
                "tests": payload["tests"]["passed"],
                "detailed": payload["detailed_checks"]["passed"],
                "minimal": payload["minimal_checks"]["passed"],
                "owner_json": payload["owner_json_parsed"],
                "owner_files": payload["owner_files"],
                "canonical_payload_sha256": payload["canonical_payload_sha256"],
            },
            sort_keys=True,
        )
    )
    if payload["status"] != "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
