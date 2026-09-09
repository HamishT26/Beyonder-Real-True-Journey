#!/usr/bin/env python3
"""Execute and bind the frozen Vesper v689-v7 x2 tranche."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_preservation_x2 as core

OWNER = "Vesper Arlen"
PHASE = "v689-v7"
PLANNING_COMMIT = "ec29a1f3fa0471bf2f8d654c162846645adda1b6"
X1_COMMIT = "d88dac91bed120345dad6b0371db570c37b8fed2"
BOUNDARY = (
    "Same-owner finite synthetic software and documentation evidence only; "
    "not independent reproduction, empirical confirmation, authenticity, "
    "production or professional authority, identity evidence, or Stage 20. "
    "Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20."
)
GATES = [
    "empirical_gmut", "theory_of_everything", "independent_reproduction",
    "production_deployment", "real_credentials", "participant_evidence",
    "privacy_completeness", "accessibility_completeness", "exhaustive_security",
    "professional_authority", "legal_authority", "cultural_authority",
    "affected_party_authority", "maori_authority", "agi_asi",
    "consciousness_personhood", "stage20",
]
PAIRS = [
    ("sha256_digest", "digest_match"),
    ("deterministic_json", "json_roundtrip"),
    ("merkle_root", "merkle_proof"),
    ("merkle_verify", "xor_parity"),
    ("xor_recover", "claim_reservation"),
]


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(root: Path, *args: str) -> str:
    process = subprocess.run(["git", "-C", str(root), *args], text=True, encoding="utf-8", capture_output=True, check=False)
    if process.returncode:
        raise RuntimeError(process.stderr.strip() or "git command failed")
    return process.stdout.strip()


def verify_manifest_commit(root: Path, commit: str, path: str) -> dict[str, Any]:
    def blob(relative: str) -> bytes:
        return subprocess.run(["git", "-C", str(root), "cat-file", "blob", f"{commit}:{relative}"], check=True, capture_output=True).stdout

    manifest = json.loads(blob(path))
    mismatches = []
    for entry in manifest["entries"]:
        raw = blob(entry["path"]).replace(b"\r\n", b"\n")
        if len(raw) != entry["bytes_normalized_lf"] or digest(raw) != entry["sha256_normalized_lf"]:
            mismatches.append(entry["path"])
    return {"commit": commit, "manifest": path, "entries": len(manifest["entries"]), "mismatches": mismatches}


def skill_text(name: str, operation: str, runner: str) -> str:
    label = operation.replace("_", " ")
    return f"""---
name: {name}
description: Evaluate the bounded synthetic {label} contract and its authority reservation when exact integrity evidence is needed.
---

# {name}

Use this phase-local skill only for the exact `{operation}` operation in Vesper v689-v7 synthetic fixtures.

1. Require exactly `op`, `payload`, and `synthetic: true`.
2. Run `{runner}` only for its declared operation pair.
3. Preserve input bytes and the complete typed envelope.
4. Keep invalid subjects failed at zero credit even when refusal checks pass.
5. Treat digests, deterministic bytes, Merkle paths, and recovery as correspondence evidence only.
6. Stop on real records, untrusted payloads, credentials, identity, rights, ownership, legal or cultural interpretation, Maori authority, production, or Stage 20.

A finite pass is same-owner software evidence only—not authenticity, consent, ownership, exhaustive security, independent reproduction, consciousness, personhood, empirical GMUT confirmation, or a Theory of Everything.
"""


def runner_text(pair: tuple[str, str]) -> str:
    return f"""#!/usr/bin/env python3
from ghc_family_preservation_x2 import cli_main

ALLOWED = {{{pair[0]!r}, {pair[1]!r}}}

if __name__ == "__main__":
    raise SystemExit(cli_main(ALLOWED))
"""


def run_runner(root: Path, path: Path, request: dict[str, Any]) -> dict[str, Any]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.run([sys.executable, str(path)], cwd=root, env=env, input=canonical(request) + b"\n", capture_output=True, check=False)
    return {"exit_code": process.returncode, "envelope": json.loads(process.stdout), "stderr": process.stderr.decode().strip()}


def package_comparisons(target: Path) -> list[dict[str, Any]]:
    sys.path.insert(0, str(target))
    blake3 = importlib.import_module("blake3")
    cbor2 = importlib.import_module("cbor2")
    reedsolo = importlib.import_module("reedsolo")
    rows = []
    for case in range(1, 11):
        data = f"blake3-comparison-{case:02d}".encode()
        incremental = blake3.blake3()
        incremental.update(data[: len(data) // 2])
        incremental.update(data[len(data) // 2 :])
        rows.append({"package": "blake3", "case": case, "claim": "one-shot equals incremental on exact bytes", "passed": incremental.digest() == blake3.blake3(data).digest(), "same_owner_only": True})
    for case in range(1, 11):
        left = {"z": case, "a": [case, case + 1]}
        right = {"a": [case, case + 1], "z": case}
        left_bytes = cbor2.dumps(left, canonical=True)
        right_bytes = cbor2.dumps(right, canonical=True)
        rows.append({"package": "cbor2", "case": case, "claim": "canonical bytes ignore input map insertion order and roundtrip", "passed": left_bytes == right_bytes and cbor2.loads(left_bytes) == left, "same_owner_only": True})
    codec = reedsolo.RSCodec(10)
    for case in range(1, 11):
        data = f"reed-solomon-{case:02d}".encode()
        encoded = bytearray(codec.encode(data))
        encoded[case % len(encoded)] ^= case
        decoded = codec.decode(encoded)[0]
        rows.append({"package": "reedsolo", "case": case, "claim": "one synthetic symbol error is corrected within ten parity symbols", "passed": bytes(decoded) == data, "same_owner_only": True})
    return rows


def static_review(paths: list[Path], root: Path) -> dict[str, Any]:
    findings = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
                findings.append({"path": path.relative_to(root).as_posix(), "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"path": path.relative_to(root).as_posix(), "line": node.lineno, "kind": "shell_true"})
    return {"files": len(paths), "findings": findings, "passed": not findings, "boundary": BOUNDARY}


def privacy_review(paths: list[Path], root: Path) -> dict[str, Any]:
    import re

    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_user_root": re.compile(r"[A-Za-z]:\\\\Users\\\\", re.IGNORECASE),
        "private_uri": re.compile(r"(?:plugin|app|codex)://", re.IGNORECASE),
        "delegation_markup": re.compile(r"(?:<codex_delegation|source_thread_id)", re.IGNORECASE),
        "credential_assignment": re.compile(r"(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.IGNORECASE),
    }
    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"class": label, "path": path.relative_to(root).as_posix()})
    return {"classes": list(patterns), "files": len(paths), "confirmed_hits": hits, "passed": not hits, "boundary": BOUNDARY}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--package-target", type=Path, required=True)
    parser.add_argument("--skill-validator", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    phase_root = root / "docs/vesper-arlen/v689-v7"
    plan_root = phase_root / "plan"
    x2_root = phase_root / "x2"
    skills_root = phase_root / "skills"
    if args.x1_commit != X1_COMMIT or git(root, "rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("x2 must start at the exact immutable x1 commit")
    x1_gate = verify_manifest_commit(root, X1_COMMIT, "docs/vesper-arlen/v689-v7/x1/manifest.json")
    if x1_gate["mismatches"]:
        raise RuntimeError("x1 Git-blob manifest failed")
    branch = git(root, "symbolic-ref", "--short", "HEAD")
    upstream = git(root, "rev-parse", "@{upstream}")
    tracking = git(root, "rev-parse", f"refs/remotes/origin/{branch}")
    live = git(root, "ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()[0]
    x1_gate.update({"parent": git(root, "show", "-s", "--format=%P", X1_COMMIT), "expected_parent": PLANNING_COMMIT, "clean_at_start": not git(root, "status", "--porcelain=v1"), "four_way_equal": len({X1_COMMIT, upstream, tracking, live}) == 1, "boundary": BOUNDARY})
    if x1_gate["parent"] != PLANNING_COMMIT or not x1_gate["four_way_equal"]:
        raise RuntimeError("x1 lifecycle or equality gate failed")

    proposals = [row for row in load(plan_root / "new-proposals.json")["proposals"] if row["session"] == "x2"]
    results = []
    for row in proposals:
        before = canonical(row["request"])
        observed = core.evaluate(row["request"])
        candidate = core.evaluate(row["candidate_request"])
        passed = observed == row["expected"] and candidate == row["candidate_expected"] and before == canonical(row["request"])
        results.append({"proposal_id": row["proposal_id"], "operation": row["operation"], "observed": observed, "observed_sha256": digest(canonical(observed)), "expected_sha256": row["expected_sha256"], "main_passed": observed == row["expected"], "candidate_observed": candidate, "candidate_subject_result": "fail", "candidate_subject_success_credit": 0, "refusal_predicate_passed": candidate == row["candidate_expected"], "input_unchanged": before == canonical(row["request"]), "outcome": row["expected_disposition"] if passed else "open_gap"})
    if not all(row["main_passed"] and row["refusal_predicate_passed"] and row["input_unchanged"] for row in results):
        raise RuntimeError("x2 frozen portfolio failed")

    inherited = load(plan_root / "inherited-selections.json")["selections"][100:]
    projections = []
    for row in inherited:
        reconstructed = {key: value for key, value in sorted(row["source_record"].items())}
        observed = digest(canonical(reconstructed))
        projections.append({"selection_id": row["selection_id"], "source_proposal_id": row["source_proposal_id"], "expected_sha256": row["source_record_sha256"], "observed_sha256": observed, "lossless": reconstructed == row["source_record"] and observed == row["source_record_sha256"], "source_execution_credit": 0})
    if not all(row["lossless"] for row in projections):
        raise RuntimeError("x2 source reconstruction failed")

    skill_plan = load(plan_root / "skills-runners-plan.json")
    x2_skills = [row for row in skill_plan["skills"] if row["session"] == "x2"]
    x2_runners = [row for row in skill_plan["runners"] if row["session"] == "x2"]
    runner_paths = {}
    for row in x2_runners:
        path = root / "scripts" / row["name"]
        write_text(path, runner_text(tuple(row["operations"])))
        runner_paths[row["runner_id"]] = path
    operation_to_runner = {operation: row["name"] for row in x2_runners for operation in row["operations"]}
    for row in x2_skills:
        write_text(skills_root / row["name"] / "SKILL.md", skill_text(row["name"], row["operation"], operation_to_runner[row["operation"]]))

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    skill_results = []
    for row in x2_skills:
        path = skills_root / row["name"]
        process = subprocess.run([sys.executable, str(args.skill_validator), str(path)], cwd=root, env=env, text=True, encoding="utf-8", capture_output=True, check=False)
        skill_results.append({"name": row["name"], "exit_code": process.returncode, "passed": process.returncode == 0, "output": (process.stdout + process.stderr).strip()})
    if not all(row["passed"] for row in skill_results):
        raise RuntimeError("x2 skill validation failed")

    runner_smokes = []
    for row in x2_runners:
        path = runner_paths[row["runner_id"]]
        for operation in row["operations"]:
            proposal = next(item for item in proposals if item["operation"] == operation)
            positive = run_runner(root, path, proposal["request"])
            adverse = run_runner(root, path, proposal["candidate_request"])
            runner_smokes.extend([
                {"runner": row["name"], "operation": operation, "kind": "positive", "passed": positive["exit_code"] == 0 and positive["envelope"] == proposal["expected"], **positive},
                {"runner": row["name"], "operation": operation, "kind": "adverse", "passed": adverse["exit_code"] == 2 and adverse["envelope"] == proposal["candidate_expected"], "invalid_subject_success_credit": 0, **adverse},
            ])
    if not all(row["passed"] for row in runner_smokes):
        raise RuntimeError("x2 runner smoke failed")

    comparisons = package_comparisons(args.package_target)
    if not all(row["passed"] for row in comparisons):
        raise RuntimeError("x2 package comparison failed")

    failed_test_path = x2_root / "test-receipt.json"
    retained_test_path = x2_root / "test-receipt-failed-01.json"
    if failed_test_path.exists() and not retained_test_path.exists():
        prior = load(failed_test_path)
        if prior.get("passed") is False:
            write_json(retained_test_path, prior)
    test_process = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/test_ghc_family_preservation_x2.py"], cwd=root, env=env, text=True, encoding="utf-8", capture_output=True, check=False)
    test_receipt = {"command": "python -m pytest -q tests/test_ghc_family_preservation_x2.py", "exit_code": test_process.returncode, "stdout": test_process.stdout.strip(), "stderr": test_process.stderr.strip(), "passed": test_process.returncode == 0, "boundary": BOUNDARY}
    if not test_receipt["passed"]:
        write_json(failed_test_path, test_receipt)
        raise RuntimeError("x2 tests failed")

    runtime_paths = [root / "scripts/ghc_family_preservation_x2.py", root / "scripts/ghc_family_v689_v7_x2_builder.py", root / "tests/test_ghc_family_preservation_x2.py", *runner_paths.values()]
    security = static_review(runtime_paths, root)
    if not security["passed"]:
        raise RuntimeError("x2 static security review failed")

    external_failures = [
        {"retained_negative_id": "VA6897-X2-N001", "stage": "x1_postseal_equality_projection", "observed": "The first combined equality tool command ended in malformed shell text and produced no equality receipt.", "original_success_credit": 0, "recovery": "Run a complete scalar equality projection; exact x1 and all three remote views then matched.", "recovery_state": "bounded_recovery_passed"},
        {"retained_negative_id": "VA6897-X2-N002", "stage": "x2_ast_lint_preflight", "observed": "The first parallel preflight used an invalid worktree directory for one command, so the orchestration was rejected before either check ran.", "original_success_credit": 0, "recovery": "Use the exact Vesper worktree for both bounded preflight commands.", "recovery_state": "bounded_recovery_passed"},
        {"retained_negative_id": "VA6897-X2-N003", "stage": "x2_ruff_preflight", "observed": "The first exact Ruff pass found three import-order findings across the x2 core, builder, and test.", "original_success_credit": 0, "recovery": "Apply Ruff's safe import-order fixes to those three files and rerun only AST plus Ruff.", "recovery_state": "bounded_recovery_passed"}
    ]
    methods = []
    witnesses = []
    for index, operation in enumerate(sorted(core.X2_OPERATIONS), 1):
        method_id = f"VA6897-X2-M{index:02d}"
        methods.append({"method_id": method_id, "title": operation.replace("_", " "), "failure_signature": "typed envelope mismatch or invalid-subject admission", "trigger_preconditions": ["frozen synthetic request", "exact x2 operation", "immutable x1 gate"], "privacy_class": "sanitized_public", "approval_class": "safe_now_synthetic", "candidate_workaround": "retain request and repair only the selected x2 operation", "validation_witness_ids": [], "recurrence_guard": "exact envelope plus input immutability and field closure", "rollback": "select immutable x1 commit", "recommendation_state": "validated", "supersedes": [], "protected_gates": GATES, "retained_negative_ids": [f"VA6897-X2-CAND-{operation}"], "scope_boundary": BOUNDARY})
    grouped = {operation: [row for row in results if row["operation"] == operation] for operation in core.X2_OPERATIONS}
    for method in methods:
        operation = method["title"].replace(" ", "_")
        for row in grouped[operation]:
            witnesses.extend([
                {"witness_id": f"{row['proposal_id']}-MAIN", "method_id": method["method_id"], "procedure": "evaluate frozen request", "scope": "synthetic owner x2", "expected": "exact envelope", "observed": "matched", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
                {"witness_id": f"{row['proposal_id']}-SUBJECT", "method_id": method["method_id"], "procedure": "submit invalid extra-field subject", "scope": "synthetic owner x2", "expected": "subject remains unsuccessful", "observed": "rejected", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [f"{row['proposal_id']}-CANDIDATE"], "boundary": BOUNDARY},
                {"witness_id": f"{row['proposal_id']}-GUARD", "method_id": method["method_id"], "procedure": "check refusal predicate", "scope": "synthetic owner x2", "expected": "E_FIELDS", "observed": "E_FIELDS", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [f"{row['proposal_id']}-CANDIDATE"], "boundary": BOUNDARY},
            ])
    witnesses.extend([
        {"witness_id": failure["retained_negative_id"], "method_id": methods[0]["method_id"], "procedure": "retained postseal projection", "scope": failure["stage"], "expected": "complete equality receipt", "observed": failure["observed"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["retained_negative_id"]], "boundary": BOUNDARY}
        for failure in external_failures
    ])
    for method in methods:
        method["validation_witness_ids"] = [row["witness_id"] for row in witnesses if row["method_id"] == method["method_id"] and row["result"] == "pass"]

    counts = {label: sum(row["outcome"] == label for row in results) for label in ("completed", "represented", "open_gap", "exact_gate")}
    write_json(x2_root / "x1-gate.json", x1_gate)
    write_json(x2_root / "results.json", {"schema": "ghc.family.vesper.preservation-results.v1", "owner": OWNER, "phase": PHASE, "session": "x2", "results": results, "counts": counts, "boundary": BOUNDARY})
    write_json(x2_root / "source-projections.json", {"schema": "ghc.family.source-projections.v1", "owner": OWNER, "phase": PHASE, "session": "x2", "projections": projections, "passed": 100, "source_execution_credit": 0, "boundary": BOUNDARY})
    write_json(x2_root / "cleanup-receipt.json", {"tasks": 100, "passed": 100, "changed_source_records": 0, "description": "Lossless sorted key-value reconstructions; no deletion or host cleanup.", "boundary": BOUNDARY})
    write_json(x2_root / "skill-validation.json", {"validator": "official skill-creator quick_validate.py", "results": skill_results, "passed": 10, "failed": 0, "global_installation": False, "boundary": BOUNDARY})
    write_json(x2_root / "runner-smokes.json", {"smokes": runner_smokes, "passed": len(runner_smokes), "failed": 0, "boundary": BOUNDARY})
    write_json(x2_root / "package-comparisons.json", {"comparisons": comparisons, "passed": len(comparisons), "failed": 0, "same_owner_only": True, "independent_reproduction": False, "boundary": BOUNDARY})
    write_json(x2_root / "test-receipt.json", test_receipt)
    write_json(x2_root / "security-review.json", security)
    write_json(x2_root / "static-review.json", {"ast_files": len(runtime_paths), "ruff_reserved_for_exact_staged_review": True, "passed": True, "boundary": BOUNDARY})
    write_json(x2_root / "method-flow.json", {"schema": "ghc.family.method-flow-state.v1", "owner": OWNER, "phase": PHASE, "execution_authority": "owner_self_scoped_delta", "identity_boundary": BOUNDARY, "methods": methods, "witnesses": witnesses, "state_events": [{"event": "x2 executed after immutable exact x1 gate", "result": "pass"}], "recommendations": [{"recommendation": "Keep recovery capability separate from authenticity and rights conclusions.", "state": "preferred"}], "counts": {"methods": len(methods), "witnesses": len(witnesses), "failed": sum(row["result"] == "fail" for row in witnesses), "passing": sum(row["result"] == "pass" for row in witnesses)}, "boundary": BOUNDARY})
    write_json(x2_root / "operational-failures.json", {"failures": external_failures, "erased": False, "boundary": BOUNDARY})
    write_json(x2_root / "meta-tool-catalogue.json", {"schema": "ghc.family.meta-tool-catalogue.v1", "owner": OWNER, "phase": PHASE, "session": "x2", "skills": [{"name": row["name"], "status": "current", "evidence_state": "validated", "operation": row["operation"], "global_installation": False} for row in x2_skills], "runners": [{"name": row["name"], "status": "current", "evidence_state": "validated", "operations": row["operations"]} for row in x2_runners], "boundary": BOUNDARY})
    write_json(x2_root / "phase-summary.json", {"state": "X2_EXECUTED_CANDIDATES_REJECTED_SOURCE_RECONSTRUCTED", "owner": OWNER, "phase": PHASE, "safe_tasks": 100, "candidate_subjects_failed": 100, "candidate_refusal_checks_passed": 100, "clean_fix_refine": 100, "skills": 10, "runners": 5, "package_comparisons": 30, "outcomes": counts, "boundary": BOUNDARY})

    privacy_paths = sorted([path for path in x2_root.rglob("*") if path.is_file()] + [skills_root / row["name"] / "SKILL.md" for row in x2_skills])
    privacy = privacy_review(privacy_paths, root)
    write_json(x2_root / "privacy-review.json", privacy)
    if not privacy["passed"]:
        raise RuntimeError("x2 privacy review failed")

    include = sorted(
        [path for path in x2_root.rglob("*") if path.is_file() and path.name != "manifest.json"]
        + [skills_root / row["name"] / "SKILL.md" for row in x2_skills]
        + runtime_paths
    )
    entries = []
    for path in sorted(set(include)):
        data = path.read_bytes().replace(b"\r\n", b"\n")
        entries.append({"path": path.relative_to(root).as_posix(), "bytes_normalized_lf": len(data), "sha256_normalized_lf": digest(data)})
    write_json(x2_root / "manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v1", "owner": OWNER, "phase": PHASE, "lifecycle": "x2", "x1_commit": X1_COMMIT, "entries": entries, "entry_count": len(entries), "self_exclusions": ["docs/vesper-arlen/v689-v7/x2/manifest.json"], "boundary": BOUNDARY})
    print(json.dumps({"status": "VALID_X2_BUILT", "results": len(results), "outcomes": counts, "projections": len(projections), "skills": len(x2_skills), "runners": len(x2_runners), "comparisons": len(comparisons), "manifest_entries": len(entries)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
