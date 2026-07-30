#!/usr/bin/env python3
"""Retain and correct the failed v656-v4 aggregate launch."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v4_phase_data as d
from ghc_family_v656_v4_phase_catalogue import RUNNER_IDEAS
from build_ghc_family_v656_v4_correction import (
    batch_blobs,
    expand_text_references,
    normalize_text_references,
    tree_map,
)


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_FINAL
X1 = "1c84cf2616df4efbb13c2df89397941251e2def5"
EVIDENCE = "6f6c32a470b25ee46d16c2f8207018c701c81e02"
CLOSEOUT = "f5a8bcfc1480b4d600806b75a3c921bf3a132bb5"
CORRECTION1 = "14a04ce7607a839bcbff42d6daf59a1f1f24d2ed"
FAILED_ATTEMPT_RECEIPT_SHA256 = (
    "42ae906e32a83875aed96099db6552b77a73206fc893de1e731e29385b43f714"
)
FINAL_NEGATIVE = {
    "negative_id": "V6564-NEG-FINAL-004",
    "signature": "canonical-aggregate-test-module-discovery-failure",
    "observed": (
        "The first exact-final aggregate stopped before executing tests because "
        "script launch bound the scripts directory but not the repository root; "
        "unittest returned a _FailedTest during suite flattening."
    ),
    "recovery": (
        "Insert the exact repository root into Python's module search path before "
        "test discovery, retain the failed aggregate with zero success credit, "
        "and validate the corrected exact final."
    ),
    "recurrence_guard": (
        "When a validator is launched by repository-relative script path, bind "
        "both the repository root and scripts directory before importing tests."
    ),
    "failed_attempt_receipt_sha256": FAILED_ATTEMPT_RECEIPT_SHA256,
    "credit": 0,
    "retained": True,
}
FINAL_NEGATIVES = 14358
FINAL_METHODS = 644


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_compact_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_paths() -> list[str]:
    paths = {
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    }
    paths.update(
        {
            "scripts/build_ghc_family_v656_v4_x1.py",
            "scripts/ghc_family_v656_v4_phase_catalogue.py",
            "scripts/ghc_family_v656_v4_phase_data.py",
            "scripts/build_ghc_family_v656_v4_evidence.py",
            "scripts/ghc_family_v656_v4_core.py",
            "scripts/ghc_family_v656_v4_validate.py",
            "scripts/ghc_family_v656_v4_x2_data.py",
            "scripts/build_ghc_family_v656_v4_closeout.py",
            "scripts/ghc_family_v656_v4_final_validate.py",
            "scripts/build_ghc_family_v656_v4_correction.py",
            "scripts/build_ghc_family_v656_v4_aggregate_correction.py",
            "tests/test_ghc_family_v656_v4_x1.py",
            "tests/test_ghc_family_v656_v4_core.py",
            "tests/test_ghc_family_v656_v4_validation.py",
            "tests/test_ghc_family_v656_v4_closeout.py",
            "tests/test_ghc_family_v656_v4_correction.py",
            "tests/test_ghc_family_v656_v4_aggregate_correction.py",
        }
    )
    paths.update(f"scripts/{name}" for name in RUNNER_IDEAS)
    return sorted(paths)


def delta_paths() -> list[str]:
    paths = owner_paths()
    prior = tree_map(CORRECTION1)
    prior_paths = [path for path in paths if path in prior]
    prior_data = dict(
        zip(prior_paths, batch_blobs([prior[path] for path in prior_paths]))
    )
    return sorted(
        path
        for path in paths
        if path not in prior_data or (REPO / path).read_bytes() != prior_data[path]
    )


def append_failure(flow: dict[str, Any]) -> dict[str, Any]:
    method_id = "V6564-FINAL-METHOD-04"
    if any(item["method_id"] == method_id for item in flow["methods"]):
        return flow
    failed_id = "V6564-FINAL-WITNESS-04-F"
    passing_id = "V6564-FINAL-WITNESS-04-P"
    flow["methods"].append(
        {
            "method_id": method_id,
            "title": "Bounded recovery for aggregate test-module discovery failure",
            "trigger_preconditions": [FINAL_NEGATIVE["signature"]],
            "failure_signature": FINAL_NEGATIVE["observed"],
            "candidate_workaround": FINAL_NEGATIVE["recovery"],
            "recurrence_guard": FINAL_NEGATIVE["recurrence_guard"],
            "approval_class": "safe_now_owner_local_validator_launch_recovery",
            "privacy_class": "sanitized_public",
            "scope_boundary": (
                "Same-owner validator module-discovery recovery only; the failed "
                "aggregate receives zero success or partial credit."
            ),
            "rollback": (
                "Stop, retain the failed aggregate and external failure receipt, "
                "and leave sibling, external, professional, legal, cultural, and "
                "authority state unchanged."
            ),
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [FINAL_NEGATIVE["negative_id"]],
            "validation_witness_ids": [failed_id, passing_id],
            "recommendation_state": "preferred",
            "supersedes": [],
        }
    )
    flow["witnesses"].extend(
        [
            {
                "witness_id": failed_id,
                "method_id": method_id,
                "result": "fail",
                "scope": FINAL_NEGATIVE["signature"],
                "procedure": "Launch the exact-final validator by repository-relative script path.",
                "expected": "All selected repository test modules resolve before execution.",
                "observed": FINAL_NEGATIVE["observed"],
                "retained_negative_ids": [FINAL_NEGATIVE["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Zero aggregate success and zero partial credit.",
            },
            {
                "witness_id": passing_id,
                "method_id": method_id,
                "result": "pass",
                "scope": FINAL_NEGATIVE["signature"],
                "procedure": FINAL_NEGATIVE["recovery"],
                "expected": "The selected test loader resolves all intended repository modules.",
                "observed": (
                    "The isolated corrected selection resolved and passed 48 tests; "
                    "the full corrected-final aggregate remains pending."
                ),
                "retained_negative_ids": [FINAL_NEGATIVE["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Isolated failed-check recovery only, not aggregate success.",
            },
        ]
    )
    start = len(flow["state_events"])
    flow["state_events"].extend(
        [
            {
                "event_index": start + 1,
                "method_id": method_id,
                "before": None,
                "after": "candidate",
                "reason": "Failed aggregate retained at zero credit.",
                "witness_id": failed_id,
            },
            {
                "event_index": start + 2,
                "method_id": method_id,
                "before": "candidate",
                "after": "validated",
                "reason": "Repository-root test discovery recovery isolated and passed.",
                "witness_id": passing_id,
            },
            {
                "event_index": start + 3,
                "method_id": method_id,
                "before": "validated",
                "after": "preferred",
                "reason": "Explicit repository-root binding retained as recurrence guard.",
                "witness_id": passing_id,
            },
        ]
    )
    flow["recommendations"].append(
        {
            "recommendation_id": "V6564-FINAL-REC-04",
            "method_id": method_id,
            "recommendation": FINAL_NEGATIVE["recurrence_guard"],
            "state": "preferred",
            "scope": "family_current_validator_launch_recommendation",
            "completion_credit": False,
        }
    )
    flow["current_phase_final_method_ids"] = list(
        flow.get("current_phase_final_method_ids", [])
    ) + [method_id]
    results = Counter(item["result"] for item in flow["witnesses"])
    states = Counter(
        item.get("after", item.get("to", "unknown"))
        for item in flow["state_events"]
    )
    flow["counts"] = {
        "methods": len(flow["methods"]),
        "witnesses": len(flow["witnesses"]),
        "witness_results": dict(sorted(results.items())),
        "state_events": len(flow["state_events"]),
        "states": dict(sorted(states.items())),
        "recommendations": len(flow["recommendations"]),
    }
    flow["lifecycle"] = "aggregate_launch_corrected_final_candidate"
    return flow


def update_baton() -> int:
    path = ROOT / "handoffs/eiren-kestrel-v656-v5-activation.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        f"- Immutable Caelen combined closeout candidate: `{CLOSEOUT}`",
        (
            f"- Immutable Caelen combined closeout candidate: `{CLOSEOUT}`\n"
            f"- Immutable Caelen document-cap correction: `{CORRECTION1}`"
        ),
    )
    old = (
        "Source-to-final must contain exactly four new single-parent Caelen commits: "
        "one dedicated x1 freeze, one x2 evidence commit, one combined closeout "
        "candidate, and one lossless document-cap correction/content-seal commit. "
        "It must contain zero merges and every phase commit must have one parent; "
        "the closeout candidate must be the direct child of evidence, corrected "
        "final must be the direct child of the closeout candidate, and source, x1, "
        "evidence, and closeout candidate must be ancestral."
    )
    new = (
        "Source-to-final must contain exactly five new single-parent Caelen commits: "
        "one dedicated x1 freeze, one x2 evidence commit, one combined closeout "
        "candidate, one lossless document-cap correction, and one aggregate-launch "
        "correction/content-seal commit. It must contain zero merges and every phase "
        "commit must have one parent; the closeout candidate must be the direct child "
        "of evidence, the document-cap correction must be the direct child of the "
        "closeout candidate, aggregate-corrected final must be the direct child of "
        "the document-cap correction, and all earlier anchors must be ancestral."
    )
    if old not in text:
        raise RuntimeError("four-commit baton history paragraph not found")
    text = text.replace(old, new)
    text = text.replace("14,357", "14,358")
    text = text.replace(
        "one retained final privacy-scan candidate, and one retained manifest-audit timeout.",
        (
            "one retained final privacy-scan candidate, one retained manifest-audit "
            "timeout, one retained document-cap preflight, and one retained "
            "aggregate-launch failure."
        ),
    )
    text = text.replace("643 methods", "644 methods")
    text = text.replace("643 retained failed", "644 retained failed")
    text = text.replace("643 bounded passing", "644 bounded passing")
    marker = (
        "The bounded recoveries never erase the initial failures. Eiren must "
        "inherit the recurrence guards as recommendations rather than pretend "
        "the failed attempts did not happen."
    )
    replacement = (
        "The first canonical aggregate attempt also remains retained with zero "
        "success and zero partial credit because script-path launch omitted the "
        "repository root during unittest discovery and produced `_FailedTest` "
        "before executing tests. Its external failed-attempt receipt is bound by "
        f"SHA-256 `{FAILED_ATTEMPT_RECEIPT_SHA256}`. The isolated corrected selection "
        "resolved and passed 48 tests; that is only the failed-check recovery, not "
        "aggregate success. " + marker
    )
    if marker not in text:
        raise RuntimeError("baton recovery marker not found")
    text = text.replace(marker, replacement)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    words = len(text.split())
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"baton word count outside bounds: {words}")
    return words


def privacy_scan() -> None:
    scan_path = f"{d.PHASE_ROOT}/validation/final-privacy-scan.json"
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)(?:[a-z]:\\\\users\\\\[^\\\\\s]+|[a-z]:\\\\ghc-archives)"
        ),
        "credential_or_token": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|authorization:\s*bearer|sk-[a-z0-9]{12,})\s*[:=]"
        ),
        "raw_task_identifier": re.compile(
            r"(?i)(?:source_thread_id|thread_id|task_id|conversation_id)\s*[:=]"
        ),
        "private_callable_detail": re.compile(
            r"(?i)(?:send_message_to_thread|private_target|callable_route_id)\s*[:=(]"
        ),
    }
    hits = {label: [] for label in patterns}
    paths = owner_paths()
    for relative in paths:
        if relative == scan_path:
            continue
        try:
            text = (REPO / relative).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits[label].append(relative)
    confirmed = sum(len(items) for items in hits.values())
    write_json(
        "validation/final-privacy-scan.json",
        {
            "schema": "ghc.family.v656-v4.privacy-scan.aggregate-corrected-final.v1",
            "classes": list(patterns),
            "scanned_file_count": len(paths),
            "hits": hits,
            "confirmed_hit_count": confirmed,
            "valid": confirmed == 0,
            "boundary": "Complete owner-file five-class scan; not exhaustive security or privacy-complete assurance.",
        },
    )
    if confirmed:
        raise RuntimeError(f"privacy hits: {hits}")


def manifests() -> None:
    delta_manifest = (
        f"{d.PHASE_ROOT}/validation/aggregate-correction-staged-manifest.json"
    )
    owner_manifest = f"{d.PHASE_ROOT}/validation/final-owner-manifest.json"
    prior_tree = tree_map(CORRECTION1)
    delta = [
        path
        for path in delta_paths()
        if path not in {delta_manifest, owner_manifest}
    ]
    entries = [
        {
            "path": path,
            "status": "modified" if path in prior_tree else "added",
            "bytes": (REPO / path).stat().st_size,
            "sha256": sha256(REPO / path),
        }
        for path in delta
    ]
    write_json(
        "validation/aggregate-correction-staged-manifest.json",
        {
            "schema": "ghc.family.v656-v4.aggregate-correction-staged-manifest.v1",
            "first_correction": CORRECTION1,
            "entries": entries,
            "entry_count": len(entries),
            "declared_exclusions": [
                {"path": delta_manifest, "reason": "self_hash_impossible_inside_same_blob"},
                {
                    "path": owner_manifest,
                    "reason": "generated_after_delta_manifest_for_complete_owner_tree",
                },
            ],
            "expected_commit_path_count": len(entries) + 2,
            "zero_deletions": True,
            "history_additive": True,
            "exact_set_required": True,
        },
    )
    owner_entries = [
        {
            "path": path,
            "bytes": (REPO / path).stat().st_size,
            "sha256": sha256(REPO / path),
        }
        for path in owner_paths()
        if path != owner_manifest
    ]
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v656-v4.final-owner-manifest.aggregate-corrected.v1",
            "source": SOURCE,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "declared_exclusions": [
                {"path": owner_manifest, "reason": "self_hash_impossible_inside_same_blob"}
            ],
            "expected_owner_path_count": len(owner_entries) + 1,
            "owner_file_cap": 2000,
            "exact_set_required": True,
        },
    )


def build() -> None:
    if run("git", "rev-parse", "HEAD") != CORRECTION1:
        raise RuntimeError("aggregate correction must start at exact first correction")
    if run("git", "rev-parse", "HEAD^") != CLOSEOUT:
        raise RuntimeError("first correction is not direct child of closeout candidate")
    if run("git", "rev-list", "--count", "--merges", f"{SOURCE}..{CORRECTION1}") != "0":
        raise RuntimeError("pre-aggregate-correction history contains a merge")

    flow = expand_text_references(
        read_json("method-flow/method-flow-ledger-final.json")
    )
    flow = append_failure(flow)
    flow = normalize_text_references(flow)
    write_compact_json("method-flow/method-flow-ledger-final.json", flow)
    ledger_words = len(
        (ROOT / "method-flow/method-flow-ledger-final.json")
        .read_text(encoding="utf-8")
        .split()
    )
    if ledger_words > 100000 or flow["counts"]["methods"] != FINAL_METHODS:
        raise RuntimeError("aggregate-corrected final Method Flow invalid")
    summary = read_json("method-flow/method-flow-summary-final.json")
    summary.update(
        {
            "schema": "ghc.family.v656-v4.method-flow-summary.aggregate-corrected-final.v1",
            "counts": flow["counts"],
            "methods": FINAL_METHODS,
            "retained_failed_witnesses": FINAL_METHODS,
            "bounded_passing_witnesses": FINAL_METHODS,
            "new_final_operational_failures": 4,
            "final_ledger_words": ledger_words,
            "no_failure_erased": True,
        }
    )
    write_json("method-flow/method-flow-summary-final.json", summary)
    write_text(
        "method-flow/method-flow-summary-final.md",
        f"""# Caelen Morrow v656-v4 aggregate-corrected final Method Flow

The final ledger preserves {FINAL_METHODS} methods, {FINAL_METHODS} retained
failed witnesses, and {FINAL_METHODS} bounded passing witnesses. The failed
aggregate launch is retained with zero success and zero partial credit. The
isolated repository-root discovery recovery passed 48 selected tests but is not
aggregate success. The compact lossless final ledger contains {ledger_words}
physical words. No failure, gap, or exact gate is erased.
""",
    )
    negatives = read_json("truth/retained-negative-register-final.json")
    items = list(negatives["final_operational_negatives"])
    if not any(item["negative_id"] == FINAL_NEGATIVE["negative_id"] for item in items):
        items.append(FINAL_NEGATIVE)
    negatives.update(
        {
            "schema": "ghc.family.v656-v4.retained-negatives.aggregate-corrected-final.v1",
            "final_operational_count": len(items),
            "final_operational_negatives": items,
            "effective_count": FINAL_NEGATIVES,
            "all_retained": True,
        }
    )
    write_json("truth/retained-negative-register-final.json", negatives)
    truth = read_json("truth/phase-truth-final.json")
    truth.update(
        {
            "schema": "ghc.family.v656-v4.phase-truth.aggregate-corrected-final.v1",
            "first_correction": CORRECTION1,
            "final": "resolve_from_containing_commit",
            "phase_commit_count": 5,
            "effective_negatives": FINAL_NEGATIVES,
            "method_flow": flow["counts"],
            "canonical_failed_attempts": 1,
            "canonical_successes": 0,
            "terminal_route_contacted": False,
            "terminal_route_state": "PREPARED_NOT_SENT",
            "verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json("truth/phase-truth-final.json", truth)
    baton_words = update_baton()
    successor = read_json("orchestration/successor-baton-preparation.json")
    successor.update(
        {
            "word_count": baton_words,
            "first_correction": CORRECTION1,
            "aggregate_corrected_final": "resolve_from_containing_commit",
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
        }
    )
    write_json("orchestration/successor-baton-preparation.json", successor)
    route = read_json("orchestration/terminal-route-state.json")
    route.update(
        {
            "first_correction": CORRECTION1,
            "corrected_phase_commit_count": 5,
            "canonical_failed_attempts": 1,
            "canonical_successes": 0,
            "state": "PREPARED_NOT_SENT",
            "contact_count": 0,
        }
    )
    write_json("orchestration/terminal-route-state.json", route)
    final_record = read_json("lifecycle/final-record.json")
    final_record.update(
        {
            "schema": "ghc.family.v656-v4.final-record.aggregate-corrected.v1",
            "first_correction": CORRECTION1,
            "final": "resolve_from_containing_commit",
            "expected_phase_commits": 5,
            "first_correction_direct_child_of_closeout": True,
            "aggregate_corrected_final_direct_child_of_first_correction": True,
            "content_seal_in_correction_commit": False,
            "content_seal_in_aggregate_correction_commit": True,
        }
    )
    write_json("lifecycle/final-record.json", final_record)
    write_json(
        "lifecycle/aggregate-correction-record.json",
        {
            "schema": "ghc.family.v656-v4.aggregate-correction-record.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "closeout_candidate": CLOSEOUT,
            "first_correction": CORRECTION1,
            "aggregate_corrected_final": "resolve_from_containing_commit",
            "retained_failure": FINAL_NEGATIVE,
            "aggregate_success_credit": False,
            "isolated_recovery_tests": 48,
            "history_rewritten": False,
            "force_push": False,
            "deletions": 0,
            "commit_cap": {"used": 5, "ceiling": 8},
        },
    )
    closeout = read_json("closeout/closeout-receipt.json")
    closeout.update(
        {
            "schema": "ghc.family.v656-v4.closeout-receipt.aggregate-corrected.v1",
            "effective_negatives": FINAL_NEGATIVES,
            "methods": FINAL_METHODS,
            "failed_witnesses": FINAL_METHODS,
            "passing_witnesses": FINAL_METHODS,
            "first_correction": CORRECTION1,
            "aggregate_corrected_final": "resolve_from_containing_commit",
            "canonical_failed_attempts": 1,
            "canonical_successes": 0,
            "state": "AGGREGATE_CORRECTED_CANDIDATE_REQUIRES_EXACT_FINAL_GATE",
        }
    )
    write_json("closeout/closeout-receipt.json", closeout)
    seal = read_json("seal/seal-receipt.json")
    seal.update(
        {
            "schema": "ghc.family.v656-v4.seal-receipt.aggregate-corrected.v1",
            "content_seal": "aggregate_launch_correction_commit",
            "first_correction": CORRECTION1,
            "terminal_message_sent": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json("seal/seal-receipt.json", seal)
    protocol = read_json("validation/final-validation-protocol.json")
    protocol.update(
        {
            "schema": "ghc.family.v656-v4.final-validation-protocol.aggregate-corrected.v1",
            "phase_commits": 5,
            "first_correction": CORRECTION1,
            "failed_aggregate_attempts": 1,
            "successful_aggregate_attempts": 0,
            "selected_test_modules": [
                "tests.test_ghc_family_v656_v4_x1 minus two lifecycle-local working-head assertions",
                "tests.test_ghc_family_v656_v4_core",
                "tests.test_ghc_family_v656_v4_validation",
                "tests.test_ghc_family_v656_v4_closeout",
                "tests.test_ghc_family_v656_v4_correction",
                "tests.test_ghc_family_v656_v4_aggregate_correction",
            ],
            "manifest_replays": [
                "x1",
                "evidence",
                "closeout delta",
                "document-cap correction delta",
                "aggregate-launch correction delta",
                "corrected owner",
            ],
            "validator_launch_guard": "repository root inserted before unittest discovery",
        }
    )
    write_json("validation/final-validation-protocol.json", protocol)
    checklist = read_json("truth/final-complete-incomplete-checklist.json")
    checklist["complete"].append(
        "failed aggregate retained and repository-root test discovery corrected"
    )
    write_json("truth/final-complete-incomplete-checklist.json", checklist)
    wellbeing = read_json("wellbeing/wellbeing-check-final.json")
    wellbeing.update(
        {
            "commits_planned": 5,
            "baton_word_count": baton_words,
            "failed_aggregate_attempts_retained": 1,
        }
    )
    write_json("wellbeing/wellbeing-check-final.json", wellbeing)
    index = read_json("tooling/ghc-family-index-final-addendum.json")
    index.update(
        {
            "schema": "ghc.family.v656-v4.index-addendum.aggregate-corrected-final.v1",
            "aggregate_correction_builder": "scripts/build_ghc_family_v656_v4_aggregate_correction.py",
            "first_correction": CORRECTION1,
            "route_state": "PREPARED_NOT_SENT",
        }
    )
    write_json("tooling/ghc-family-index-final-addendum.json", index)
    write_text(
        "tooling/ghc-family-index-final-addendum.md",
        """# GHC Family Index — Caelen Morrow v656-v4 aggregate-corrected final

The immutable document-cap correction remains evidence. A fifth single-parent
commit retains the failed aggregate launch and binds the repository root before
unittest discovery. The failed attempt has zero success and zero partial credit.
No successful aggregate has yet run. Existing family-current callers remain
unchanged, and the Eiren Kestrel route remains `PREPARED_NOT_SENT`.
""",
    )
    write_text(
        "deliverables/v656-v4-final-closeout.md",
        f"""# Caelen Morrow v656-v4 aggregate-corrected final closeout

The bounded outcomes remain 23 `completed`, 5 `represented`, 1 `open_gap`, and
1 `exact_gate`. Effective negatives are {FINAL_NEGATIVES:,}; open gaps are 100;
exact gates are 99. Method Flow retains {FINAL_METHODS} methods,
{FINAL_METHODS} failed witnesses, and {FINAL_METHODS} bounded passing witnesses.

The first canonical aggregate attempt at `{CORRECTION1}` stopped before test
execution because repository-root test discovery was not bound. It receives
zero success and zero partial credit and is retained by external receipt
SHA-256 `{FAILED_ATTEMPT_RECEIPT_SHA256}`. The isolated corrected selection
passed 48 tests; that is recovery evidence only.

The {baton_words:,}-word sanitized Eiren Kestrel v656-v5 baton remains
`PREPARED_NOT_SENT`. It may be sent exactly once only after the aggregate-
corrected final is clean, pushed, fresh-live equal, and its one canonical scoped
aggregate succeeds. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_json(
        "validation/aggregate-correction-build-receipt.json",
        {
            "schema": "ghc.family.v656-v4.aggregate-correction-build-receipt.v1",
            "valid": True,
            "first_correction": CORRECTION1,
            "aggregate_corrected_final": "resolve_from_containing_commit",
            "retained_failure": FINAL_NEGATIVE,
            "failed_attempt_receipt_sha256": FAILED_ATTEMPT_RECEIPT_SHA256,
            "isolated_recovery_tests": 48,
            "aggregate_success_credit": False,
            "effective_negatives": FINAL_NEGATIVES,
            "methods": FINAL_METHODS,
            "baton_words": baton_words,
            "history_rewritten": False,
            "deletions": 0,
            "terminal_contact": False,
        },
    )
    write_json(
        "validation/aggregate-correction-staged-review.json",
        {
            "schema": "ghc.family.v656-v4.aggregate-correction-staged-review.v1",
            "first_correction": CORRECTION1,
            "paths": delta_paths(),
            "path_count": len(delta_paths()),
            "deletions": [],
            "history_additive": True,
            "failure_retained": True,
            "terminal_route_state": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    privacy_scan()
    review = read_json("validation/aggregate-correction-staged-review.json")
    review["paths"] = delta_paths()
    review["path_count"] = len(review["paths"])
    write_json("validation/aggregate-correction-staged-review.json", review)
    privacy_scan()
    over_cap = []
    for path in owner_paths():
        try:
            text = (REPO / path).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        words = len(text.split())
        if words > 100000:
            over_cap.append({"path": path, "words": words})
    if over_cap:
        raise RuntimeError(f"document cap failure: {over_cap}")
    manifests()
    if read_json("validation/final-owner-manifest.json")[
        "expected_owner_path_count"
    ] > 2000:
        raise RuntimeError("owner file cap exceeded")
    print(
        json.dumps(
            {
                "valid": True,
                "phase": d.PHASE,
                "first_correction": CORRECTION1,
                "effective_negatives": FINAL_NEGATIVES,
                "methods": FINAL_METHODS,
                "baton_words": baton_words,
                "aggregate_delta_entries": read_json(
                    "validation/aggregate-correction-staged-manifest.json"
                )["entry_count"],
                "owner_manifest_entries": read_json(
                    "validation/final-owner-manifest.json"
                )["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
