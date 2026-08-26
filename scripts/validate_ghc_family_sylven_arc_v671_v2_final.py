"""One-shot exact-final owner-scoped canonical validator for Sylven Arc v671-v2."""

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


OWNER = "Sylven Arc"
PHASE = "v671-v2"
SOURCE = "ebbd2ea41873c12287d94b0ec2b64dc22a87c07d"
X1 = "26c88fefc685b48965a1418d07204cc91f6580a0"
EVIDENCE = "140714b7a4e25814de333752a8627055384195ab"
OWNER_PREFIX = "docs/sylven-arc/v671-v2/"
BRANCH = "codex/GHC-Family/sylven-arc-v671-v2-full-tools"
BOUNDARY = "Same-owner exact-final validation under shared infrastructure is not independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Maori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority."


def proc(repo: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, env=env)


def text(repo: Path, *args: str) -> str:
    result = proc(repo, *args)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8", errors="replace").strip()


def blob(repo: Path, commit: str, path: str) -> bytes:
    result = proc(repo, "git", "show", f"{commit}:{path}")
    if result.returncode:
        raise RuntimeError(f"missing blob {commit}:{path}")
    return result.stdout


def load_blob_json(repo: Path, commit: str, path: str) -> Any:
    return json.loads(blob(repo, commit, path).decode("utf-8"))


def check_manifest(repo: Path, commit: str, manifest_path: str) -> dict[str, Any]:
    manifest = load_blob_json(repo, commit, manifest_path)
    mismatches = []
    for entry in manifest["entries"]:
        data = blob(repo, commit, entry["path"])
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    return {"path": manifest_path, "entries": len(manifest["entries"]), "mismatches": mismatches, "valid": not mismatches and manifest["entry_count"] == len(manifest["entries"])}


def canonical_sha(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    expected = args.expected_final
    receipt = args.receipt
    if receipt.exists():
        raise SystemExit("canonical receipt already exists; replay refused")

    detailed: list[dict[str, Any]] = []
    minimal: list[dict[str, Any]] = []

    def detail(name: str, passed: bool, observed: Any = None) -> None:
        detailed.append({"name": name, "passed": bool(passed), "observed": observed})

    def mini(name: str, passed: bool) -> None:
        minimal.append({"name": name, "passed": bool(passed)})

    head = text(repo, "git", "rev-parse", "HEAD")
    parent = text(repo, "git", "rev-parse", f"{expected}^")
    x1_parent = text(repo, "git", "rev-parse", f"{X1}^")
    evidence_parent = text(repo, "git", "rev-parse", f"{EVIDENCE}^")
    phase_commits = int(text(repo, "git", "rev-list", "--count", f"{SOURCE}..{expected}"))
    merges = [row for row in text(repo, "git", "rev-list", "--merges", f"{SOURCE}..{expected}").splitlines() if row]
    status_before = text(repo, "git", "status", "--porcelain")
    upstream = text(repo, "git", "rev-parse", "@{u}")
    tracking = text(repo, "git", "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_tokens = text(repo, "git", "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    divergence_tokens = text(repo, "git", "rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    divergence = [int(value) for value in divergence_tokens]

    detail("exact_head", head == expected, head)
    detail("x1_direct_parent", x1_parent == SOURCE, x1_parent)
    detail("evidence_direct_parent", evidence_parent == X1, evidence_parent)
    detail("final_direct_parent", parent == EVIDENCE, parent)
    detail("three_phase_commits", phase_commits == 3, phase_commits)
    detail("zero_merges", not merges, len(merges))
    detail("one_final_parent", len(text(repo, "git", "rev-list", "--parents", "-n", "1", expected).split()) == 2)
    detail("clean_before", status_before == "", status_before)
    detail("zero_divergence", divergence == [0, 0], divergence)
    detail("four_way_equality", head == upstream == tracking == live, {"local": head, "upstream": upstream, "tracking": tracking, "live": live})

    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["GHC_EXPECTED_FINAL"] = expected
    tests = proc(repo, "python", "-X", "utf8", "-m", "pytest", "-q", "tests/test_ghc_family_sylven_arc_v671_v2_final.py", env=env)
    test_stdout = tests.stdout.decode("utf-8", errors="replace")
    test_stderr = tests.stderr.decode("utf-8", errors="replace")
    match = re.search(r"(\d+) passed", test_stdout)
    passed_tests = int(match.group(1)) if match else 0
    tests_exact = tests.returncode == 0 and passed_tests == 24
    detail("owner_tests_exact", tests_exact, {"returncode": tests.returncode, "passed": passed_tests})

    paths = [row for row in text(repo, "git", "ls-tree", "-r", "--name-only", expected, "--", OWNER_PREFIX).splitlines() if row]
    json_paths = [path for path in paths if path.endswith(".json")]
    json_issues = []
    for path in json_paths:
        try:
            json.loads(blob(repo, expected, path).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path, "issue": type(exc).__name__})
    detail("all_phase_json_parses", not json_issues, {"count": len(json_paths), "issues": json_issues})

    manifest_results = [
        check_manifest(repo, X1, f"{OWNER_PREFIX}validation/x1-manifest.json"),
        check_manifest(repo, EVIDENCE, f"{OWNER_PREFIX}validation/evidence-manifest.json"),
        check_manifest(repo, expected, f"{OWNER_PREFIX}validation/final-owner-manifest.json"),
        check_manifest(repo, expected, f"{OWNER_PREFIX}validation/final-delta-manifest.json"),
    ]
    detail("all_manifests_replay", all(row["valid"] for row in manifest_results), manifest_results)

    phase_tree = [row for row in text(repo, "git", "ls-tree", "-r", "--name-only", expected, "--", "scripts", "tests").splitlines() if row]
    runner_names = {
        "ghc_family_coating_safety_abstention.py", "ghc_family_letter_layout_relations.py", "ghc_family_paint_layer_vacancy.py",
        "ghc_family_signboard_topology.py", "ghc_family_signwork_accessible_status.py", "ghc_family_signwork_correction_readback.py",
        "ghc_family_signwork_measurement_vacancy.py", "ghc_family_signwork_privacy_quarantine.py", "ghc_family_signwork_project_identity.py",
        "ghc_family_signwork_workload_handover.py",
    }
    python_paths = sorted({path for path in phase_tree if "sylven_arc_v671_v2" in path or Path(path).name in runner_names})
    compile_issues = []
    security_findings = []
    for path in python_paths:
        source = blob(repo, expected, path).decode("utf-8")
        try:
            tree = ast.parse(source, filename=path)
        except SyntaxError as exc:
            compile_issues.append({"path": path, "issue": str(exc)})
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                security_findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
            if isinstance(node.func, ast.Attribute) and node.func.attr == "system" and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                security_findings.append({"path": path, "line": node.lineno, "kind": "os.system"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    security_findings.append({"path": path, "line": node.lineno, "kind": "shell_true"})
    detail("changed_python_compiles", not compile_issues, {"count": len(python_paths), "issues": compile_issues})
    detail("bounded_python_security", not security_findings, {"count": len(python_paths), "findings": security_findings})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    scan_paths = sorted(set(paths + python_paths))
    definition_paths = {path for path in python_paths if path.startswith("scripts/build_") or path.startswith("scripts/validate_") or path.startswith("tests/test_")}
    candidates = []
    scanned_text = 0
    for path in scan_paths:
        if Path(path).suffix.lower() not in {".json", ".md", ".html", ".txt", ".py"}:
            continue
        source = blob(repo, expected, path).decode("utf-8")
        scanned_text += 1
        for label, pattern in patterns.items():
            if pattern.search(source):
                candidates.append({"path": path, "class": label, "disposition": "scanner_definition_or_unit_test" if path in definition_paths else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    detail("five_class_privacy_scan", not confirmed, {"files": scanned_text, "candidates": len(candidates), "confirmed": confirmed})

    truth = load_blob_json(repo, expected, f"{OWNER_PREFIX}closeout/phase-truth.json")
    method = load_blob_json(repo, expected, f"{OWNER_PREFIX}closeout/method-flow-final.json")
    gates = load_blob_json(repo, expected, f"{OWNER_PREFIX}closeout/open-exact-gate-register.json")
    review = load_blob_json(repo, expected, f"{OWNER_PREFIX}validation/final-staged-review.json")
    staged_privacy = load_blob_json(repo, expected, f"{OWNER_PREFIX}validation/final-staged-privacy.json")
    stale = load_blob_json(repo, expected, f"{OWNER_PREFIX}validation/stale-label-review.json")
    seal = load_blob_json(repo, expected, f"{OWNER_PREFIX}seal/content-seal.json")
    checklist = load_blob_json(repo, expected, f"{OWNER_PREFIX}closeout/complete-incomplete-checklist.json")
    route = load_blob_json(repo, expected, f"{OWNER_PREFIX}orchestration/route-state.json")
    prerequisites = load_blob_json(repo, expected, f"{OWNER_PREFIX}final/final-validation-prerequisites.json")

    detail("outcomes_exact", truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}, truth["outcomes"])
    detail("proposal_chain_exact", truth["proposal_chain"] == 5630, truth["proposal_chain"])
    detail("terminal_counts_exact", [truth[key] for key in ("effective_negatives", "methods", "failed_witnesses", "passing_witnesses", "open_gaps", "exact_gates")] == [33707, 20024, 5528, 7099, 259, 254])
    detail("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
    detail("method_flow_retention", method["row_count"] == 182 and method["all_failures_retained"] and method["all_recoveries_paired"])
    detail("gates_exact", gates["effective_open_gaps"] == 259 and gates["effective_exact_gates"] == 254)
    detail("staged_review_valid", review["valid"] and not review["immutable_x1_x2_mutations"] and not review["out_of_scope"])
    detail("staged_privacy_valid", staged_privacy["valid"] and staged_privacy["confirmed_hit_count"] == 0)
    detail("stale_labels_valid", stale["valid"] and not stale["stale_labels_found"])
    detail("content_seal_valid", canonical_sha(seal["canonical_payload"]) == seal["canonical_payload_sha256"])
    detail("complete_incomplete_visible", len(checklist["complete"]) >= 8 and len(checklist["incomplete"]) >= 8)
    detail("route_prepared_not_sent", route["delivery_state"] == "PREPARED_NOT_SENT" and route["successor_contact_count"] == 0 and route["task_creation_count"] == 0 and not route["sent_by_sylven_arc"])
    detail("canonical_prerequisite_budget", prerequisites["canonical_invocation_budget"] == 1 and prerequisites["canonical_invocations"] == 0 and not prerequisites["post_success_replay"])

    owner_files = len(paths)
    materialized = len([path for path in repo.rglob("*") if path.is_file() and ".git" not in path.parts])
    word_violations = []
    for path in paths:
        if Path(path).suffix.lower() in {".md", ".txt"}:
            words = len(blob(repo, expected, path).decode("utf-8").split())
            if words > 100000:
                word_violations.append({"path": path, "words": words})
    detail("owner_file_ceiling", owner_files < 2000, owner_files)
    detail("materialized_file_ceiling", materialized < 2000, materialized)
    detail("document_word_ceiling", not word_violations, word_violations)
    detail("full_suite_not_run", True, "owner_scoped_only")

    mini("tests", tests_exact)
    mini("json", not json_issues)
    mini("privacy", not confirmed)
    mini("security", not security_findings)
    mini("manifests", all(row["valid"] for row in manifest_results))
    mini("ancestry", x1_parent == SOURCE and evidence_parent == X1 and parent == EVIDENCE)
    mini("commits", phase_commits == 3 and not merges)
    mini("head", head == expected)
    mini("clean", status_before == "")
    mini("divergence", divergence == [0, 0])
    mini("remote_equality", head == upstream == tracking == live)
    mini("truth", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    mini("gates", gates["effective_open_gaps"] == 259 and gates["effective_exact_gates"] == 254)
    mini("route", route["delivery_state"] == "PREPARED_NOT_SENT")
    mini("caps", owner_files < 2000 and materialized < 2000 and not word_violations)

    status_after = text(repo, "git", "status", "--porcelain")
    detail("clean_after", status_after == "", status_after)
    all_valid = tests_exact and all(row["passed"] for row in detailed) and all(row["passed"] for row in minimal)
    payload = {
        "schema": "ghc.family.exact-final-owner-canonical.v5",
        "owner": OWNER,
        "phase": PHASE,
        "exact_final": expected,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all_valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "valid": all_valid,
        "invocation_count": 1,
        "replayed": False,
        "full_repository_suite": False,
        "tests": {"returncode": tests.returncode, "passed": passed_tests, "expected": 24, "stdout_sha256": hashlib.sha256(tests.stdout).hexdigest(), "stderr_sha256": hashlib.sha256(tests.stderr).hexdigest(), "exact": tests_exact},
        "detailed": {"passed": sum(row["passed"] for row in detailed), "total": len(detailed), "rows": detailed},
        "minimal": {"passed": sum(row["passed"] for row in minimal), "total": len(minimal), "rows": minimal},
        "json_documents": len(json_paths),
        "privacy": {"files": scanned_text, "candidate_count": len(candidates), "confirmed_hit_count": len(confirmed)},
        "python": {"files": len(python_paths), "compile_issues": compile_issues, "security_findings": security_findings},
        "manifests": manifest_results,
        "history": {"phase_commits": phase_commits, "merges": len(merges), "final_parents": 1},
        "git": {"clean_before": status_before == "", "clean_after": status_after == "", "divergence": divergence, "four_way_equal": head == upstream == tracking == live},
        "boundary": BOUNDARY,
    }
    payload["canonical_payload_sha256"] = canonical_sha(payload)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    temporary = receipt.with_suffix(receipt.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(receipt)
    print(json.dumps({"result": payload["result"], "tests": f"{passed_tests}/24", "detailed": f"{payload['detailed']['passed']}/{payload['detailed']['total']}", "minimal": f"{payload['minimal']['passed']}/{payload['minimal']['total']}", "json": len(json_paths), "privacy_confirmed": len(confirmed), "python_findings": len(security_findings), "receipt": str(receipt)}, sort_keys=True))
    raise SystemExit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
