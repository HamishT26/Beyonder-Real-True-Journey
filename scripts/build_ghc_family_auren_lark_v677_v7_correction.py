#!/usr/bin/env python3
"""Build and review the additive Auren v677-v7 terminal correction."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
EVIDENCE = "3f91c32cb1acda2900ce69bedc60971353084775"
FAILED_FINAL = "4aaf45add92b18c5f8bef68ba15dd112e0f5703c"
BRANCH = "codex/GHC-Family/auren-lark-v677-v7-full-tools"
FAILED_ATTEMPT_SHA256 = (
    "317d525189558ef52075d4e06d2f07b75efa14cda376fb4395fa3ceb183637b4"
)
FAILED_RECEIPT_SHA256 = (
    "e3dfc23b73e1bf90bdb57aecc5ca5874b662233b3bf5a10dfb0a45f8f2141857"
)

REPO = Path(__file__).resolve().parents[1]
PHASE_REL = "docs/auren-lark/v677-v7"
PHASE = REPO / PHASE_REL
CORRECTION = PHASE / "correction"
VALIDATION = PHASE / "validation"
CODE_PATHS = {
    "scripts/build_ghc_family_auren_lark_v677_v7_correction.py",
    "scripts/ghc_family_auren_lark_v677_v7_canonical.py",
    "tests/test_ghc_family_auren_lark_v677_v7_correction.py",
    "tests/test_ghc_family_auren_lark_v677_v7_final.py",
}
RECEIPT_PATHS = {
    f"{PHASE_REL}/validation/correction-delta-manifest.json",
    f"{PHASE_REL}/validation/correction-owner-manifest.json",
    f"{PHASE_REL}/validation/correction-privacy-scan.json",
    f"{PHASE_REL}/validation/correction-security-scan.json",
    f"{PHASE_REL}/validation/correction-staged-review.json",
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str, text: bool = True):
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=text,
        encoding="utf-8" if text else None,
    )


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def manifest_entry(path: str, data: bytes) -> dict[str, Any]:
    value = normalized(data)
    return {
        "path": path,
        "bytes_normalized_lf": len(value),
        "sha256_normalized_lf": hashlib.sha256(value).hexdigest(),
    }


def index_blob(path: str) -> bytes:
    return git("show", f":{path}", text=False)


def failed_final_blob(path: str) -> bytes:
    return git("show", f"{FAILED_FINAL}:{path}", text=False)


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{PHASE_REL}/")
        or (
            path.startswith("scripts/")
            and "auren_lark_v677_v7" in path
            and path.endswith(".py")
        )
        or (
            path.startswith("tests/")
            and "auren_lark_v677_v7" in path
            and path.endswith(".py")
        )
    )


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "private_absolute_path": re.compile(
            rb"(?i)[A-Z]:[\\/]+Users[\\/]+"
        ),
        "raw_task_identifier": re.compile(
            rb"(?i)(source_thread_id|clientThreadId)"
        ),
        "credential_or_secret": re.compile(
            rb"(?i)(-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,})"
        ),
        "uuid_like_private_identifier": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_session_material": re.compile(
            rb"(?i)(private app state|session stream|raw transcript payload|screenshot payload)"
        ),
    }


def build() -> list[str]:
    if git("rev-parse", "HEAD").strip() != FAILED_FINAL:
        raise RuntimeError(
            "correction build requires the exact failed-canonical final"
        )
    if git("branch", "--show-current").strip() != BRANCH:
        raise RuntimeError("wrong branch")
    observed = {
        row[3:].strip().replace("\\", "/")
        for row in git("status", "--porcelain=v1").splitlines()
        if row
    }
    if CORRECTION.exists():
        expected_status_paths = (
            CODE_PATHS
            | {
                path.relative_to(REPO).as_posix()
                for path in CORRECTION.rglob("*")
                if path.is_file()
            }
            | RECEIPT_PATHS
        )
    else:
        expected_status_paths = CODE_PATHS
    if observed != expected_status_paths:
        raise RuntimeError(
            "unexpected pre-correction paths: "
            + json.dumps(
                {
                    "missing": sorted(expected_status_paths - observed),
                    "extra": sorted(observed - expected_status_paths),
                },
                sort_keys=True,
            )
        )

    failure = {
        "failure_id": "AUR6777-CANON-N001",
        "failed_head": FAILED_FINAL,
        "lifecycle": "external_exact_final_canonical",
        "state": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
        "summary": "The sole canonical invocation at the three-commit final ran 26 owner-final tests; 25 passed and one stale assertion expected two precloseout pairs after the retained third pair had been added.",
        "tests_passed_with_bounded_component_credit": 25,
        "tests_failed": 1,
        "canonical_success_credit": 0,
        "retained": True,
    }
    recovery = {
        "witness_id": "AUR6777-CANON-P001",
        "failure_id": failure["failure_id"],
        "state": "bounded_passing_dependency_preflight",
        "procedure": "Change only the stale pair-count assertion from two to three, bind historical manifests to the failed final, and validate a new direct-child correction without retrying the failed head.",
        "old_head_replay": False,
        "previously_passing_final_tests_replayed": False,
        "broader_credit": 0,
    }
    validation_failure = {
        "failure_id": "AUR6777-CORR-N001",
        "lifecycle": "precommit_correction_index_replay",
        "state": "FAILED_ZERO_VALIDATION_CREDIT",
        "summary": "The first external correction-index replay wrote every cat-file request before consuming output, allowing the input and output pipes to fill and deadlock. The exact read-only process was interrupted; no repository state changed.",
        "validation_credit": 0,
        "retained": True,
    }
    validation_recovery = {
        "witness_id": "AUR6777-CORR-P001",
        "failure_id": validation_failure["failure_id"],
        "state": "bounded_passing_streaming_recovery",
        "procedure": "Stream one cat-file request and consume its complete framed response before sending the next request, then replay the exact correction manifests without running tests.",
        "failed_batch_replayed": False,
        "precanonical_tests_run": False,
        "broader_credit": 0,
    }
    framing_failure = {
        "failure_id": "AUR6777-CORR-N002",
        "lifecycle": "precommit_correction_streaming_index_replay",
        "state": "FAILED_ZERO_VALIDATION_CREDIT",
        "summary": "The first one-request/one-response recovery assumed one pipe read would return the complete declared blob length. The pipe returned a partial chunk on the first object, producing a framing failure before any hash claim.",
        "validation_credit": 0,
        "retained": True,
    }
    framing_recovery = {
        "witness_id": "AUR6777-CORR-P002",
        "failure_id": framing_failure["failure_id"],
        "state": "bounded_passing_exact_length_streaming_recovery",
        "procedure": "Retain request-response ordering and read each declared blob through a bounded loop until the exact byte length is received before consuming the framing newline.",
        "failed_streaming_attempt_replayed": False,
        "precanonical_tests_run": False,
        "broader_credit": 0,
    }
    pairs = [
        {"failure": failure, "recovery": recovery},
        {
            "failure": validation_failure,
            "recovery": validation_recovery,
        },
        {
            "failure": framing_failure,
            "recovery": framing_recovery,
        },
    ]
    truth = {
        "schema": "ghc-family-terminal-correction/v1",
        "owner": "Auren Lark",
        "phase": "v677-v7",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "failed_canonical_head": FAILED_FINAL,
        "corrected_final_head": "COMMIT_CONTAINING_THIS_FILE",
        "expected_phase_commits": 4,
        "zero_merges": True,
        "outcomes": {
            "completed": 42,
            "represented": 12,
            "open_gap": 3,
            "exact_gate": 3,
        },
        "declared_proposal_chain": 8210,
        "effective_negatives": 45718,
        "effective_methods": 43036,
        "retained_failed_witnesses": 17379,
        "bounded_passing_witnesses": 26362,
        "open_gaps": 389,
        "exact_gates": 380,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "canonical_attempts_before_correction": 1,
        "canonical_successes_before_correction": 0,
        "new_head_canonical": "PENDING_EXTERNAL_ONE_SHOT",
    }
    original_integrity = json.loads(
        failed_final_blob(
            f"{PHASE_REL}/final/baton-integrity.json"
        ).decode("utf-8")
    )
    artifacts: dict[str, Any] = {
        "terminal-correction.json": truth,
        "failed-canonical-receipt.json": {
            "schema": "ghc-family-failed-canonical-receipt/v1",
            "head": FAILED_FINAL,
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "attempt_receipt_sha256": FAILED_ATTEMPT_SHA256,
            "failed_receipt_sha256": FAILED_RECEIPT_SHA256,
            "tests_passed": 25,
            "tests_failed": 1,
            "repository_mutation": False,
            "task_contact": False,
            "same_head_retry_permitted": False,
        },
        "method-flow-correction.json": {
            "schema": "ghc-family-method-flow-correction/v1",
            "failure": failure,
            "recovery": recovery,
            "pairs": pairs,
            "failures": [row["failure"] for row in pairs],
            "recoveries": [row["recovery"] for row in pairs],
            "effective_counts": {
                key: truth[key]
                for key in (
                    "effective_negatives",
                    "effective_methods",
                    "retained_failed_witnesses",
                    "bounded_passing_witnesses",
                    "open_gaps",
                    "exact_gates",
                )
            },
            "failure_erasure": False,
        },
        "index-replay-recovery.json": {
            "schema": "ghc-family-correction-index-replay-recovery/v1",
            "failure": validation_failure,
            "recovery": validation_recovery,
            "pairs": [
                {
                    "failure": validation_failure,
                    "recovery": validation_recovery,
                },
                {
                    "failure": framing_failure,
                    "recovery": framing_recovery,
                },
            ],
            "repository_mutation_during_failure": False,
            "tests_run_during_failure_or_recovery": 0,
            "exact_streaming_replay_state": "EXACT_LENGTH_EXTERNAL_PRECOMMIT_EVIDENCE_ONLY",
        },
        "route-plan.json": {
            "schema": "ghc-family-route-plan-correction/v1",
            "state": "PREPARED_NOT_SENT",
            "conditional_successor_title": "Sable Rook",
            "conditional_successor_phase": "v677-v8",
            "next_after_successor": "Caelen Ash",
            "conditional_next_phase": "v678-v1",
            "old_head_replay_permitted": False,
            "message_sent": False,
            "original_baton": original_integrity,
        },
        "validation-candidate.json": {
            "schema": "ghc-family-corrected-final-validation-candidate/v1",
            "old_head_canonical": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "old_head_replayed": False,
            "corrected_head": "COMMIT_CONTAINING_THIS_FILE",
            "corrected_head_canonical_invocations": 0,
            "corrected_head_canonical_successes": 0,
            "previously_passing_final_tests_replayed": False,
            "precommit_validation_failures_retained": 2,
            "streaming_index_recovery": "EXACT_LENGTH_EXTERNAL_PRECOMMIT_EVIDENCE_ONLY",
            "complete_repository_suite": False,
            "independent_reproduction": False,
        },
        "authority-boundary.json": {
            "schema": "ghc-family-correction-authority-boundary/v1",
            "relational_working_language_only": True,
            "consciousness_or_personhood_evidence": False,
            "identity_continuity_evidence": False,
            "employment_or_qualification_evidence": False,
            "scientific_or_operational_authority": False,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
            "independent_agency": False,
            "human_pause_redirect_rename_stop_control": True,
        },
    }
    written: list[str] = []
    for name, payload in artifacts.items():
        path = CORRECTION / name
        write_json(path, payload)
        written.append(path.relative_to(REPO).as_posix())

    overview = """# Auren Lark v677-v7 additive terminal correction

The sole canonical invocation at the three-commit exact final failed after 25 owner-final tests passed and one stale assertion expected two precloseout pairs even though the final correctly retained three. The failed attempt and receipt remain external, immutable, and zero-credit. That exact final will not be retried.

This additive correction changes one test assertion from two to three, adds correction manifests and receipts, and updates the canonical validator to bind the historical final manifests and content seal to the failed final while validating the new correction delta at a direct-child head. The prior 25 passing final tests are retained as bounded component evidence and are not replayed. The corrected canonical may run only the previously failed final test plus the correction-local test file once. A first read-only batch replay deadlocked because it wrote every object request before consuming output. That exact process was interrupted with no repository mutation and zero validation credit. The first streaming recovery then assumed one pipe read would return the complete declared blob length and failed framing on a partial first read, also with zero credit and no repository mutation. The retained exact-length recovery streams one request at a time and loops until every declared byte is consumed before reading the delimiter.

Corrected repository truth is 45,718 effective negatives, 43,036 methods, 17,379 retained failed witnesses, 26,362 bounded passing witnesses, 389 open gaps, 380 exact gates, and NOT_READY_FOR_STAGE_20. X1, evidence, and the failed-canonical final remain immutable ancestors. The correction establishes no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim.

The Sable route remains PREPARED_NOT_SENT until a one-shot canonical invocation at the corrected head succeeds and every fresh live route guard passes.
"""
    path = CORRECTION / "terminal-correction-overview.md"
    write_text(path, overview)
    written.append(path.relative_to(REPO).as_posix())

    note = f"""# Sable Rook v677-v8 activation correction note — prepared not sent

Read the original 16,617-word prepared baton at {original_integrity['path']} and this correction note together. The original baton SHA-256 is {original_integrity['sha256']}. The three-commit Auren final {FAILED_FINAL} received one zero-credit failed canonical attempt because a test assertion expected two retained precloseout pairs instead of the exact three. That head is immutable and will not be retried.

The corrected final is the direct child containing this note. Corrected repository truth is 45,718 negatives, 43,036 methods, 17,379 retained failures, 26,362 bounded passes, 389 open gaps, 380 exact gates, a declared 8,210-proposal chain, and NOT_READY_FOR_STAGE_20. The route remains PREPARED_NOT_SENT until the corrected head has one successful owner-scoped canonical pass and fresh task-registry guards pass.

Sable must work solo in a Sable-owned D-first lane, preserve planning-only x1 before x2, keep every source and sibling lane read-only, retain every failure, gap, gate, manifest, privacy boundary, and authority reservation, and never treat same-owner validation as independent reproduction. After Sable's own terminal gate, the prospective next exact-title task is Caelen Ash for v678-v1, subject to a fresh live authority and roster check; this is not permission to precontact Caelen.

Names, roles, hopes, pronouns, sibling and family language, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala remain relational working language only. They are never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.

PREPARED_BY_AUREN_LARK = true
SENT_BY_AUREN_LARK = false
"""
    path = CORRECTION / "handoffs/sable-rook-v677-v8-correction-note.md"
    write_text(path, note)
    written.append(path.relative_to(REPO).as_posix())
    return sorted(written)


def staged_review() -> dict[str, Any]:
    if git("rev-parse", "HEAD").strip() != FAILED_FINAL:
        raise RuntimeError(
            "correction staged review requires the failed final as HEAD"
        )
    staged = {
        row
        for row in git(
            "diff", "--cached", "--name-only", "--diff-filter=ACMR"
        ).splitlines()
        if row
    }
    correction_paths = {
        path.relative_to(REPO).as_posix()
        for path in CORRECTION.rglob("*")
        if path.is_file()
    }
    expected = correction_paths | CODE_PATHS
    if staged != expected:
        raise RuntimeError(
            "unexpected initial correction stage: "
            + json.dumps(
                {
                    "missing": sorted(expected - staged),
                    "extra": sorted(staged - expected),
                },
                sort_keys=True,
            )
        )
    if any("/x1/" in path or "/x2/" in path for path in staged):
        raise RuntimeError("correction stage mixed x1 or x2 paths")

    delta_data = {path: index_blob(path) for path in sorted(staged)}
    json_count = 0
    python_count = 0
    security_findings: list[dict[str, Any]] = []
    for path, data in delta_data.items():
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_count += 1
        if path.endswith(".py"):
            tree = ast.parse(data.decode("utf-8"), filename=path)
            python_count += 1
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in {"eval", "exec"}
                ):
                    security_findings.append(
                        {
                            "path": path,
                            "line": node.lineno,
                            "kind": node.func.id,
                        }
                    )
                if isinstance(node, ast.Call):
                    for keyword in node.keywords:
                        if (
                            keyword.arg == "shell"
                            and isinstance(keyword.value, ast.Constant)
                            and keyword.value.value is True
                        ):
                            security_findings.append(
                                {
                                    "path": path,
                                    "line": node.lineno,
                                    "kind": "shell_true",
                                }
                            )
    if security_findings:
        raise RuntimeError(
            f"bounded correction security findings: {security_findings}"
        )

    failed_paths = {
        row
        for row in git(
            "ls-tree", "-r", "--name-only", FAILED_FINAL
        ).splitlines()
        if row
    }
    owner_paths = sorted(
        path
        for path in failed_paths | staged | RECEIPT_PATHS
        if owner_path(path)
    )
    owner_data: dict[str, bytes] = {}
    for path in owner_paths:
        if path in RECEIPT_PATHS:
            continue
        owner_data[path] = (
            delta_data[path] if path in delta_data else failed_final_blob(path)
        )
    if len(owner_paths) >= 2000:
        raise RuntimeError("owner file ceiling reached")

    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    patterns = privacy_patterns()
    for path, data in sorted(owner_data.items()):
        if Path(path).suffix.lower() not in {
            ".json",
            ".md",
            ".txt",
            ".html",
            ".py",
            ".yaml",
            ".yml",
        }:
            continue
        for category, pattern in patterns.items():
            if pattern.search(data):
                scanner_definition = path.startswith(("scripts/", "tests/"))
                row = {
                    "path": path,
                    "category": category,
                    "scanner_definition": scanner_definition,
                }
                candidates.append(row)
                if not scanner_definition:
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError(f"confirmed correction privacy hits: {confirmed}")

    oversized = []
    for path, data in owner_data.items():
        if Path(path).suffix.lower() in {".md", ".txt", ".html"}:
            words = len(data.decode("utf-8").split())
            if words > 100000:
                oversized.append({"path": path, "words": words})
    if oversized:
        raise RuntimeError(f"document word ceiling exceeded: {oversized}")

    check = subprocess.run(
        ["git", "diff", "--cached", "--check"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)

    delta_manifest = {
        "schema": "ghc-family-exact-git-blob-manifest/v1",
        "status": "CORRECTION_DELTA_FROM_FAILED_CANONICAL_FINAL",
        "source": FAILED_FINAL,
        "entry_count": len(staged),
        "entries": [
            manifest_entry(path, delta_data[path]) for path in sorted(staged)
        ],
        "self_exclusions": sorted(RECEIPT_PATHS),
        "normalized_lf": True,
    }
    owner_manifest = {
        "schema": "ghc-family-exact-git-blob-manifest/v1",
        "status": "CORRECTED_OWNER_FROM_ILYRA_V677_V6_SOURCE",
        "source": SOURCE,
        "failed_final": FAILED_FINAL,
        "owner_path_count": len(owner_paths),
        "entry_count": len(owner_data),
        "entries": [
            manifest_entry(path, owner_data[path])
            for path in sorted(owner_data)
        ],
        "self_exclusions": sorted(RECEIPT_PATHS),
        "normalized_lf": True,
    }
    write_json(
        VALIDATION / "correction-delta-manifest.json", delta_manifest
    )
    write_json(
        VALIDATION / "correction-owner-manifest.json", owner_manifest
    )
    write_json(
        VALIDATION / "correction-privacy-scan.json",
        {
            "schema": "ghc-family-correction-privacy-scan/v1",
            "privacy_classes": sorted(patterns),
            "owner_paths_scanned": len(owner_data),
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "complete_privacy_assurance": False,
        },
    )
    write_json(
        VALIDATION / "correction-security-scan.json",
        {
            "schema": "ghc-family-correction-security-scan/v1",
            "changed_python_parses": python_count,
            "findings": security_findings,
            "exhaustive_security": False,
        },
    )
    review = {
        "schema": "ghc-family-correction-staged-review/v1",
        "state": "VALID_EXACT_CORRECTION_STAGED_REVIEW",
        "initial_staged_paths": len(staged),
        "expected_final_staged_paths": len(staged) + len(RECEIPT_PATHS),
        "delta_entries": len(staged),
        "owner_paths": len(owner_paths),
        "owner_entries": len(owner_data),
        "json_parses": json_count,
        "python_parses": python_count,
        "privacy_candidates": len(candidates),
        "confirmed_privacy_hits": 0,
        "security_findings": 0,
        "diff_hygiene": True,
        "x1_or_x2_paths_staged": 0,
        "precanonical_correction_tests_run": False,
        "previously_passing_final_tests_replayed": False,
        "retained_precommit_validation_failures": 2,
        "streaming_index_recovery_required": True,
        "exact_length_streaming_recovery_required": True,
    }
    write_json(VALIDATION / "correction-staged-review.json", review)
    return review


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            json.dumps(
                {"status": "BUILT_TERMINAL_CORRECTION", "written": build()},
                indent=2,
                sort_keys=True,
            )
        )
    elif sys.argv[1:] == ["--staged-review"]:
        print(json.dumps(staged_review(), indent=2, sort_keys=True))
    else:
        raise SystemExit(
            "usage: build_ghc_family_auren_lark_v677_v7_correction.py [--staged-review]"
        )
