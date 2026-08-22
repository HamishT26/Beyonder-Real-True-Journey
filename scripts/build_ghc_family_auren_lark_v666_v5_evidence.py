#!/usr/bin/env python3
"""Build Auren Lark v666-v5 evidence receipts and exact staged manifest."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_auren_lark_v666_v5_runtime import (
    PHASE_ROOT,
    ROOT,
    X1_SHA,
    changed_python_files,
    load_json,
    replay_manifest,
    read_exact,
    scan_privacy,
    scan_python_security,
    text_files,
    write_json,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
SOURCE_SHA = "e4548a5447996f09087644a4a03e77dea8045ee4"


def write(relative: str, value: Any) -> None:
    write_json(PHASE_ROOT / relative, value)


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def run_x2_tests() -> dict[str, Any]:
    command = [
        sys.executable,
        "-X",
        "utf8",
        "-m",
        "unittest",
        "-q",
        "tests.test_ghc_family_auren_lark_v666_v5_x2",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )
    combined = (completed.stdout + "\n" + completed.stderr).strip()
    match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
    observed = int(match.group(1)) if match else 0
    return {
        "schema": "ghc.family.auren-lark.v666-v5.evidence-test-receipt.v1",
        "generated_at_utc": NOW,
        "command": "python -X utf8 -m unittest -q tests.test_ghc_family_auren_lark_v666_v5_x2",
        "returncode": completed.returncode,
        "observed_test_count": observed,
        "expected_test_count": 66,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "immutable_x1_covered_by": [
            "20-entry exact Git-blob manifest replay at the x1 commit",
            "zero x2, evidence, closeout, seal, final, or handoff paths in the x1 tree",
        ],
        "declared_lifecycle_exclusion": "the frozen x1 filesystem-absence assertion is not run against the later x2 materialized worktree; it passed during x1 and is replaced here by stronger exact-tree and manifest checks without modifying x1",
        "canonical_aggregate": False,
        "valid": completed.returncode == 0 and observed == 66,
    }


def build() -> None:
    truth = load_json(PHASE_ROOT / "x2" / "phase-truth.json")
    ledger = load_json(PHASE_ROOT / "x2" / "proposal-ledger.json")
    flow = load_json(PHASE_ROOT / "method-flow" / "x2-method-flow.json")
    overlay = load_json(PHASE_ROOT / "method-flow" / "x2-operational-overlay.json")
    gates = load_json(PHASE_ROOT / "x2" / "open-gate-register.json")
    portfolio = load_json(PHASE_ROOT / "x2" / "portfolio-execution.json")
    skills = load_json(PHASE_ROOT / "x2" / "skill-catalog.json")
    runners = load_json(PHASE_ROOT / "x2" / "runner-catalog.json")
    deck = load_json(PHASE_ROOT / "deck" / "model-validation.json")
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    privacy = scan_privacy(text_files())
    security = scan_python_security(changed_python_files())
    tests = run_x2_tests()
    if not all((x1_replay["valid"], privacy["valid"], security["valid"], tests["valid"])):
        raise RuntimeError(
            json.dumps(
                {
                    "x1_replay": x1_replay,
                    "privacy": privacy,
                    "security": security,
                    "tests": tests,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    write("evidence/evidence-test-receipt.json", tests)
    write(
        "evidence/evidence-test-recovery-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.evidence-test-recovery-receipt.v1",
            "generated_at_utc": NOW,
            "failed_invocation": "immutable x1 and materialized x2 modules were first combined in the later x2 worktree",
            "failed_observed_tests": 77,
            "failed_observed_failures": 1,
            "failed_aggregate_credit": 0,
            "failure_retained_as": "AL6665-OPS-N002",
            "repository_state_changed": False,
            "recovery": "leave x1 immutable, replay its exact manifest and tree boundaries, then run the 66 x2 tests in the x2 lifecycle domain",
            "recovery_observed_tests": tests["observed_test_count"],
            "recovery_observed_failures": 0,
            "recovery_valid": tests["valid"],
            "canonical_aggregate": False,
            "claim_boundary": "dependency- and lifecycle-corrected evidence test receipt only; not a clean first aggregate, terminal canonical validation, or independent reproduction",
        },
    )
    write(
        "evidence/privacy-scan-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.privacy-scan-receipt.v1",
            "generated_at_utc": NOW,
            **privacy,
        },
    )
    write(
        "evidence/security-scan-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.security-scan-receipt.v1",
            "generated_at_utc": NOW,
            **security,
        },
    )
    write(
        "evidence/x1-immutability-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.evidence-x1-immutability-receipt.v1",
            "generated_at_utc": NOW,
            "x1_sha": X1_SHA,
            "manifest_replay": x1_replay,
            "source_receipt": "docs/auren-lark/v666-v5/x2/x1-immutability-receipt.json",
            "x1_modified": False,
            "valid": x1_replay["valid"],
        },
    )
    write(
        "evidence/evidence-summary.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.evidence-summary.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "proposal_chain_total": 4270,
            "outcomes": ledger["outcome_counts"],
            "contracts": 20,
            "positive_structural_fixtures": 20,
            "rejected_negative_mutations": 100,
            "core_x2_method_count": flow["new_method_count"],
            "operational_failure_count": overlay["new_negative_count"],
            "effective_negatives": overlay["effective_negatives"],
            "effective_methods": overlay["effective_methods"],
            "open_gaps": gates["effective_open_gap_count"],
            "exact_gates": gates["effective_exact_gate_count"],
            "skills_built_tested_used": skills["skill_count"],
            "runners_smoke_passed": runners["runner_count"],
            "deck_cards": deck["card_count"],
            "x2_tests_passed": tests["observed_test_count"],
            "five_class_privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "bounded_python_security_findings": security["finding_count"],
            "real_data_rows": 0,
            "participant_count": 0,
            "network_calls_by_generated_phase_software": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_validation_is_independent_reproduction": False,
        },
    )
    write(
        "evidence/authority-and-evidence-gaps.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.authority-and-evidence-gaps.v1",
            "generated_at_utc": NOW,
            "open_gap_count": gates["effective_open_gap_count"],
            "exact_gate_count": gates["effective_exact_gate_count"],
            "new_open_gaps": gates["new_open_gaps"],
            "new_exact_gates": gates["new_exact_gates"],
            "protected_domains": [
                "empirical and participant evidence",
                "professional perfumery, chemistry, toxicology, occupational-safety, manufacturing, quality, labeling, and regulatory authority",
                "production, deployment, product, and market-release readiness",
                "privacy-complete, accessibility-complete, exhaustive-security, standards-conformance, and independent reproduction",
                "legal, cultural, affected-party, trade-secret, and Māori authority",
                "AGI, ASI, consciousness, personhood, identity continuity, Theory-of-Everything, proof, canon, and Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "evidence/portfolio-evidence-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.portfolio-evidence-receipt.v1",
            "generated_at_utc": NOW,
            "owner_method_count": portfolio["method_count"],
            "successor_recommendation_count": portfolio["recommendation_count"],
            "protected_items_executed": portfolio["protected_items_executed"],
            "external_actions": portfolio["external_actions"],
            "valid": portfolio["method_count"] == 95
            and portfolio["protected_items_executed"] == 0
            and portfolio["external_actions"] == 0,
        },
    )
    write(
        "evidence/flashcard-evidence-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.flashcard-evidence-receipt.v1",
            "generated_at_utc": NOW,
            "card_count": deck["card_count"],
            "tier_counts": deck["tier_counts"],
            "core_outcomes": deck["core_outcomes"],
            "missing_parents": deck["missing_parents"],
            "model_valid": deck["valid"],
            "implicit_completion": False,
            "successor_contacted": False,
            "claim_boundary": deck["claim_boundary"],
        },
    )
    write(
        "evidence/meta-toolbox-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.meta-toolbox-receipt.v1",
            "generated_at_utc": NOW,
            "skills": {"count": skills["skill_count"], "all_built_tested_used_bounded": skills["all_built_tested_used_bounded"]},
            "runners": {"count": runners["runner_count"], "all_smoke_passed": runners["all_smoke_passed"]},
            "closeout_runner_probe_only": True,
            "canonical_runner_probe_only": True,
            "terminal_work_invoked": False,
            "claim_boundary": "owner-local phase tooling only; no professional, production, external, independent, personhood, or Stage 20 authority",
        },
    )
    write(
        "evidence/reflection-remaster-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.reflection-remaster-receipt.v1",
            "generated_at_utc": NOW,
            "decisions": [
                {"decision": "choose a fragrance-formulation provenance lens", "because": "zero inherited perfume proposals and only one unrelated fragrance row made the practice distinct while supporting strong safety and authority abstention", "counterfactual": "reusing a recent or crowded practice domain would weaken novelty", "reversible": True},
                {"decision": "preserve the mixed-lifecycle x1 failure", "because": "the failure was real and x1 immutability forbids weakening its assertion", "counterfactual": "editing x1 after freeze would destroy the lifecycle boundary", "reversible": False},
                {"decision": "keep all source use vocabulary-only", "because": "current source review cannot confer safety, legal, regulatory, professional, or release authority", "counterfactual": "claim promotion would cross exact gates", "reversible": True},
            ],
            "unresolved": [
                "external current-row ingestion and mapping governance",
                "participant and professional validation",
                "legal, cultural, affected-party, trade-secret, and Māori authority",
                "independent reproduction and Stage 20 evidence",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "evidence/method-flow-recommendations.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.method-flow-recommendations.v1",
            "generated_at_utc": NOW,
            "recommendations": [
                "bind every test to the lifecycle tree whose invariant it asserts",
                "inspect exact state before retrying any ambiguous wrapper",
                "use one patch update operation per target file",
                "retain every rejecting mutation and operational fault at zero credit",
                "never convert source vocabulary into safety, compliance, or authority",
                "keep x1 immutable and replay manifests through exact Git blobs",
                "keep successor recommendations at zero current novelty and completion credit",
                "run terminal canonical validation once only after exact final and four-way equality",
                "refresh live authority and roster before any successor resolution",
                "preserve NOT_READY_FOR_STAGE_20 until exact protected evidence and authority exist",
            ],
            "recommendation_count": 10,
            "completion_credit": 0,
        },
    )
    write(
        "evidence/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.evidence-checklist.v1",
            "generated_at_utc": NOW,
            "completed": [
                "immutable x1 replay and zero-later-path checks",
                "twenty contracts and positive fixtures",
                "one hundred rejecting synthetic mutations",
                "exact 14 completed, 4 represented, 1 open_gap, and 1 exact_gate ledger",
                "ninety-five bounded portfolio methods",
                "ten phase-local skills read, tested, and used bounded",
                "ten family-current runners smoke checked with terminal interfaces probe-only",
                "twenty-five-card flashcard deck and static report",
                "five-class privacy and bounded changed-Python security scans",
                "sixty-six x2 tests with exact lifecycle exclusion recorded",
            ],
            "incomplete": [
                "evidence staged review, manifest, commit, push, and equality",
                "closeout and final manifests",
                "exact final push and fresh-live equality",
                "one attributable canonical aggregate",
                "fresh terminal authority and roster reread",
                "any permitted exact-title successor delivery",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write(
        "seal/evidence-seal.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.evidence-seal.v1",
            "owner": "Auren Lark",
            "phase": "v666-v5",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "ledger_canonical_sha256": canonical_sha256(ledger),
            "method_flow_canonical_sha256": canonical_sha256(flow),
            "operational_overlay_canonical_sha256": canonical_sha256(overlay),
            "gate_register_canonical_sha256": canonical_sha256(gates),
            "evidence_summary_canonical_sha256": canonical_sha256(
                {
                    "proposal_chain_total": truth["proposal_chain_total"],
                    "outcomes": truth["outcomes"],
                    "effective_negatives": truth["effective_negatives_with_operational_overlay"],
                    "effective_methods": truth["effective_methods_with_operational_overlay"],
                    "open_gaps": truth["open_gaps"],
                    "exact_gates": truth["exact_gates"],
                    "terminal_verdict": truth["terminal_verdict"],
                }
            ),
            "x1_manifest_replay_valid": x1_replay["valid"],
            "privacy_scan_valid": privacy["valid"],
            "security_scan_valid": security["valid"],
            "x2_tests_valid": tests["valid"],
            "evidence_manifest_state": "awaiting_exact_staged_review",
            "canonical_aggregate_invoked": False,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "claim_boundary": "content-state evidence seal only; not a terminal canonical receipt, independent reproduction, professional or legal approval, cultural or Māori authority, or Stage 20 authority",
        },
    )
    write(
        "evidence/evidence-build-receipt.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.evidence-build-receipt.v1",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_auren_lark_v666_v5_evidence.py",
            "x2_tests": tests["observed_test_count"],
            "x1_manifest_entries": x1_replay["entry_count"],
            "privacy_scanned_files": privacy["scanned_file_count"],
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "python_files_scanned": security["scanned_python_count"],
            "security_findings": security["finding_count"],
            "canonical_aggregate_invoked": False,
            "successor_contacted": False,
            "status": "EVIDENCE_CONTENT_BUILT_AWAITING_EXACT_STAGED_REVIEW",
        },
    )
    print(
        json.dumps(
            {
                "x2_tests": tests["observed_test_count"],
                "x1_manifest_entries": x1_replay["entry_count"],
                "privacy_files": privacy["scanned_file_count"],
                "privacy_hits": privacy["confirmed_hit_count"],
                "python_files": security["scanned_python_count"],
                "security_findings": security["finding_count"],
                "valid": True,
            },
            sort_keys=True,
        )
    )


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]
    ).decode("utf-8")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def staged_index_map() -> dict[str, tuple[str, str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "--stage", "-z"]
    )
    result: dict[str, tuple[str, str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, encoded_path = record.split(b"\t", 1)
        mode, oid, stage = metadata.decode("ascii").split()
        result[encoded_path.decode("utf-8").replace("\\", "/")] = (mode, oid, stage)
    return result


def batch_index_blobs(
    paths: list[str], index: dict[str, tuple[str, str, str]]
) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("git cat-file pipes unavailable")
        for path in paths:
            if path not in index:
                raise RuntimeError(f"staged path missing from index map: {path}")
            _mode, oid, stage = index[path]
            if stage != "0":
                raise RuntimeError(f"unexpected index stage {stage}: {path}")
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[0] != oid or header[1] != "blob":
                raise RuntimeError(f"invalid cat-file header for {path}")
            blob = read_exact(process.stdout, int(header[2]))
            if read_exact(process.stdout, 1) != b"\n":
                raise RuntimeError(f"missing cat-file terminator for {path}")
            result[path] = blob
    finally:
        if process.stdin is not None:
            process.stdin.close()
        return_code = process.wait(timeout=30)
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
        if return_code:
            raise RuntimeError(f"git cat-file --batch failed: {stderr[:240]}")
    return result


def build_staged_review() -> None:
    review_path = "docs/auren-lark/v666-v5/validation/evidence-staged-review.json"
    manifest_path = "docs/auren-lark/v666-v5/validation/evidence-content-manifest.json"
    rows = [
        (status, path)
        for status, path in staged_rows()
        if path not in {review_path, manifest_path}
    ]
    if not rows:
        raise RuntimeError("no staged evidence content")
    paths = [path for _, path in rows]
    invalid = [
        path
        for path in paths
        if not path.startswith("docs/auren-lark/v666-v5/")
        and not re.fullmatch(r"scripts/(?:build_)?ghc_family_auren_lark_v666_v5_[a-z0-9_]+\.py", path)
        and not re.fullmatch(r"tests/test_ghc_family_auren_lark_v666_v5_(?:x2|evidence)\.py", path)
    ]
    premature = [
        path
        for path in paths
        if any(
            path.startswith(f"docs/auren-lark/v666-v5/{part}/")
            for part in ("closeout", "final", "handoffs")
        )
    ]
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'
        ),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(
            r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"
        ),
        "session_identifier_value": re.compile(
            r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'
        ),
        "private_callable_identifier_value": re.compile(
            r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'
        ),
    }
    parsed_json = 0
    maximum_words = 0
    maximum_path = ""
    privacy_candidates = []
    security_findings = []
    index = staged_index_map()
    blobs = batch_index_blobs(paths, index)
    for path in paths:
        blob = blobs[path]
        text_value = blob.decode("utf-8")
        if "\r" in text_value:
            raise RuntimeError(f"non-LF staged text: {path}")
        word_count = len(re.findall(r"\S+", text_value))
        if word_count > maximum_words:
            maximum_words, maximum_path = word_count, path
        if path.endswith(".json"):
            json.loads(text_value)
            parsed_json += 1
        for class_name, pattern in privacy_patterns.items():
            if pattern.search(text_value):
                privacy_candidates.append({"path": path, "class": class_name})
        if path.endswith(".py"):
            tree = ast.parse(text_value, filename=path)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                if name in {"eval", "exec"}:
                    security_findings.append({"path": path, "line": node.lineno, "class": f"dynamic_{name}"})
                if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "line": node.lineno, "class": "shell_true"})
    truth = json.loads(blobs["docs/auren-lark/v666-v5/x2/phase-truth.json"])
    overlay = json.loads(blobs["docs/auren-lark/v666-v5/method-flow/x2-operational-overlay.json"])
    deck = json.loads(blobs["docs/auren-lark/v666-v5/deck/model-validation.json"])
    tooling = json.loads(blobs["docs/auren-lark/v666-v5/x2/tooling-smoke-receipt.json"])
    x1_tree_paths = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", X1_SHA]
    ).decode("utf-8").splitlines()
    x1_owner_count = sum(
        path.startswith("docs/auren-lark/v666-v5/")
        or path
        in {
            "scripts/build_ghc_family_auren_lark_v666_v5_x1.py",
            "tests/test_ghc_family_auren_lark_v666_v5_x1.py",
        }
        for path in x1_tree_paths
    )
    owner_tree_count = x1_owner_count + len(paths) + 2
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": maximum_words <= 100000,
        "expected_14_4_1_1": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not privacy_candidates,
        "bounded_changed_python_security_zero_findings": not security_findings,
        "owner_allowlist": not invalid,
        "owner_file_cap": owner_tree_count <= 2000,
        "premature_lifecycle_paths_absent": not premature,
        "proposal_chain_4270": truth["proposal_chain_total"] == 4270,
        "retained_operational_failures_8": overlay["new_negative_count"] == 8 and len(overlay["rows"]) == 8,
        "skills_and_runners_10_of_10": tooling["skill_passed_count"] == 10 and tooling["passed_count"] == 10,
        "deck_model_valid": deck["valid"],
        "terminal_not_ready": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.auren-lark.v666-v5.evidence-staged-review.v1",
        "owner": "Auren Lark",
        "phase": "v666-v5",
        "lifecycle": "evidence",
        "generated_at_utc": NOW,
        "reviewed_from": "git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "owner_tree_count_after_commit": owner_tree_count,
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(privacy_patterns),
        "privacy_candidates": len(privacy_candidates),
        "privacy_confirmed_hits": len(privacy_candidates),
        "privacy_candidate_rows": privacy_candidates,
        "changed_python_security_findings": security_findings,
        "checks": checks,
        "self_exclusions": [review_path, manifest_path],
        "claim_boundary": "exact staged same-owner evidence review only; not exhaustive security, privacy, accessibility, chemical safety, standards conformance, or independent reproduction",
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write("validation/evidence-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])
    entries = []
    manifest_rows = [(status, path) for status, path in staged_rows() if path != manifest_path]
    manifest_paths = [path for _status, path in manifest_rows]
    manifest_index = staged_index_map()
    manifest_blobs = batch_index_blobs(manifest_paths, manifest_index)
    for status, path in manifest_rows:
        mode, oid, stage = manifest_index[path]
        if stage != "0":
            raise RuntimeError(f"unexpected index stage for {path}")
        blob = manifest_blobs[path]
        entries.append(
            {
                "path": path,
                "git_mode": mode,
                "git_blob_oid": oid,
                "sha256": hashlib.sha256(blob).hexdigest(),
                "size_bytes": len(blob),
            }
        )
    write(
        "validation/evidence-content-manifest.json",
        {
            "schema": "ghc.family.auren-lark.v666-v5.content-manifest.v1",
            "owner": "Auren Lark",
            "phase": "evidence",
            "phase_label": "v666-v5",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "hash_source": "actual_git_index_blobs",
            "entries": entries,
            "entry_count": len(entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _ in rows),
            "self_exclusion": manifest_path,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", manifest_path])
    print(
        json.dumps(
            {
                "reviewed": len(paths),
                "manifest_entries": len(entries),
                "owner_tree_count_after_commit": owner_tree_count,
                "valid": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    else:
        raise SystemExit(
            "usage: build_ghc_family_auren_lark_v666_v5_evidence.py [--staged-review]"
        )
