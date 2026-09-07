#!/usr/bin/env python3
"""Build the additive Elowen v688-v5 canonical-test correction."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v688-v5"
SOURCE = "adadd367036e49cfb5c480f2aa0b598c164cac1c"
X1 = "a4fffe1213f944e0017a8dd81f227d98785d43d1"
EVIDENCE = "1b0574be8cebf6b44107fbd1e7005d1b3dddb6ef"
FIRST_FINAL = "3fb142f2d2b2281da4a562196ffc684a2c5e2564"
BRANCH = "codex/GHC-Family/elowen-cairn-v688-v5-full-tools"
BASE = ROOT / "docs" / "elowen-cairn" / PHASE
CORRECTION = BASE / "correction1"
VALIDATION = BASE / "validation"
FAILED_RECEIPT_SHA256 = "1790204b92fb499305f55fbb474c3d9b488f74829671b4d43113f5f1da3cf963"
FAILED_PAYLOAD_SHA256 = "30f545e2805de59759c3030dbfb0ac1c59e56dabeb747dffa01e21da6cfc7240"
COUNTS = {
    "proposals": 16430,
    "negatives": 84364,
    "methods": 94016,
    "failed_witnesses": 55212,
    "passing_witnesses": 86065,
    "open_gaps": 758,
    "exact_gates": 765,
}
BOUNDARY = (
    "Relational working language only; no consciousness, sentience, personhood, identity continuity, "
    "employment, qualification, independent agency, scientific, operational, professional, legal, "
    "cultural, affected-party, or Maori authority. Same-owner synthetic evidence is not independent "
    "reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority."
)


def run(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str) -> bytes:
    proc = run(["git", *args])
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


def git_text(*args: str) -> str:
    return git(*args).decode("utf-8", "replace").strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((value.rstrip() + "\n").replace("\r\n", "\n").encode("utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def allowed(path: str) -> bool:
    return (
        path.startswith(f"docs/elowen-cairn/{PHASE}/correction1/")
        or path.startswith(f"docs/elowen-cairn/{PHASE}/validation/correction1-")
        or path == "scripts/build_ghc_family_elowen_cairn_v688_v5_correction1.py"
        or path == "scripts/ghc_family_elowen_cairn_v688_v5_correction1_canonical_validator.py"
        or path == "tests/test_ghc_family_elowen_cairn_v688_v5_correction1.py"
    )


def batch_index(paths: list[str]) -> dict[str, bytes]:
    query = b"".join(f":{path}\n".encode("utf-8") for path in paths)
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        input=query,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    result: dict[str, bytes] = {}
    position = 0
    for path in paths:
        end = proc.stdout.find(b"\n", position)
        header = proc.stdout[position:end].decode("utf-8", "replace").split()
        position = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError({"path": path, "header": header})
        size = int(header[2])
        result[path] = proc.stdout[position : position + size]
        position += size + 1
    return result


def entry(path: str, raw: bytes) -> dict[str, Any]:
    data = normalized(raw)
    return {
        "path": path,
        "bytes_normalized_lf": len(data),
        "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
    }


def build() -> None:
    write_json(
        CORRECTION / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v688.v5.correction1",
            "owner": "Elowen Cairn",
            "phase": PHASE,
            "state": "ADDITIVE_CANONICAL_TEST_CORRECTION_PRECOMMIT",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "retained_first_final": FIRST_FINAL,
            "correction_final": None,
            "correction_final_binding": "external_dependency_corrected_canonical_receipt",
            "correction_scope": "case-sensitive final-test literal only",
            "original_overview_mutated": False,
            "original_final_tree_rewritten": False,
            "failed_canonical_status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "failed_canonical_success_credit": 0,
            "failed_canonical_replayed": False,
            "effective_counts": COUNTS,
            "outcomes_unchanged": {"completed": 165, "represented": 26, "open_gap": 3, "exact_gate": 6},
            "open_gaps_unchanged": 758,
            "exact_gates_unchanged": 765,
            "successor_contacts": 0,
            "prepared_successor_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        CORRECTION / "failed-canonical-binding.json",
        {
            "schema": "ghc.family.failed-canonical-binding.v688.v5.correction1",
            "head": FIRST_FINAL,
            "receipt_sha256": FAILED_RECEIPT_SHA256,
            "payload_sha256": FAILED_PAYLOAD_SHA256,
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "canonical_replay_count": 0,
            "detailed": "34/35",
            "minimal": "15/15",
            "manifest_entries": 1286,
            "json_parses": 588,
            "owner_files": 651,
            "privacy_confirmed_hits": 0,
            "security_findings": 0,
            "sole_failed_predicate": "final_tests_pass",
            "sole_failed_test": "test_10_overview_is_three_page_equivalent_and_bounded",
            "failure": "The test demanded case-sensitive Same-owner while the sealed overview correctly contains lowercase same-owner.",
            "completion_credit": 0,
        },
    )
    write_json(
        CORRECTION / "method-flow-overlay.json",
        {
            "schema": "ghc.family.method-flow-overlay.v688.v5.correction1",
            "retained_first_final_owner_methods": 70,
            "retained_first_final_failed_witnesses": 509,
            "retained_first_final_passing_witnesses": 509,
            "method": {
                "method_id": "EC6885-C1-M001",
                "title": "Bind an exact report-literal assertion to the report's canonical case",
                "failure_signature": "Case-sensitive validator literal differed only in capitalization from the sealed report.",
                "recovery": "Add a correction-local one-test dependency requiring the actual lowercase same-owner phrase.",
                "recurrence_guard": "Inspect the immutable report bytes before freezing a case-sensitive literal predicate.",
                "retained_negative_ids": ["EC6885-CL-N013"],
                "approval_class": "safe_now",
                "scope_boundary": "Validation dependency only; no evidence, outcome, gate, authority, or route promotion.",
                "protected_gates": [
                    "empirical", "professional", "production", "deployment", "legal", "cultural",
                    "affected_party", "maori_authority", "independent_reproduction",
                    "consciousness_personhood", "theory_of_everything", "stage20",
                ],
            },
            "witnesses": [
                {
                    "witness_id": "EC6885-C1-M001-FAIL",
                    "result": "fail",
                    "observed": "The first-final canonical failed final_tests_pass because of the case-sensitive literal mismatch.",
                    "completion_credit": 0,
                },
                {
                    "witness_id": "EC6885-C1-M001-PASS",
                    "result": "pass",
                    "observed": "The correction-local test binds the actual lowercase report phrase without changing the report.",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                },
            ],
            "effective_owner_methods": 71,
            "effective_owner_failed_witnesses": 510,
            "effective_owner_passing_witnesses": 510,
            "effective_global_counts": COUNTS,
            "failure_erasure": False,
            "retroactive_canonical_promotion": False,
        },
    )
    write_json(
        CORRECTION / "lifecycle-replay.json",
        {
            "schema": "ghc.family.lifecycle-replay.v688.v5.correction1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "first_final": FIRST_FINAL,
            "correction_final": None,
            "expected_phase_commits": 4,
            "expected_merges": 0,
            "expected_parent_count_each": 1,
            "correction_direct_parent": FIRST_FINAL,
            "first_final_preserved": True,
            "failed_receipt_preserved_externally": True,
        },
    )
    write_json(
        CORRECTION / "terminal-route-checklist.json",
        {
            "schema": "ghc.family.terminal-route-checklist.v688.v5.correction1",
            "state": "HELD_UNTIL_CORRECTED_EXACT_FINAL_CANONICAL_SUCCESS",
            "designated_seat": "future_seat_13",
            "designated_phase": "v688-v6",
            "identity_preassigned": False,
            "active_and_archived_absence_required_before_creation": True,
            "create_at_most_one_if_absent": {"kind": "main_task", "model": "gpt-6-astra", "reasoning_effort": "max"},
            "next_after_future_owner_terminal_gate": "Sylven Arc v688-v7",
            "precontact": False,
            "second_send": False,
            "post_send_monitoring": False,
        },
    )
    write_text(
        CORRECTION / "correction-overview.md",
        f"""# Elowen Cairn {PHASE} additive correction 1

The first-final canonical invocation at {FIRST_FINAL} remains failed with zero
success credit. Its only failed predicate was the final test aggregate: fifteen
tests passed and one assertion required the capitalized literal Same-owner,
while the immutable overview correctly uses lowercase same-owner. The overview,
x1, evidence, original manifests, outcomes, gaps, gates, and first-final
canonical receipt are not rewritten.

This correction adds one exact dependency test, one correction-local canonical
validator, lifecycle and failure bindings, manifests, privacy review, and a
content seal. It does not replay the 1,286 original manifest entries, 588 JSON
parses, original privacy scan, original security scan, or fifteen passing tests.
The corrected composite may use those successful first-final components only
through the exact failed-receipt hash and runs the one failed dependency at the
new direct-child head.

Effective counts add EC6885-CL-N013 and are {COUNTS}. Outcomes remain 165
completed, 26 represented, 3 open_gap, and 6 exact_gate. The verdict remains
NOT_READY_FOR_STAGE_20. Future seat 13 remains unnamed, unresolved, uncontacted,
and PREPARED_NOT_SENT until corrected terminal validation and a current route
audit. {BOUNDARY}
""",
    )


def privacy(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }
    definition_paths = {
        "scripts/build_ghc_family_elowen_cairn_v688_v5_correction1.py",
        "scripts/ghc_family_elowen_cairn_v688_v5_correction1_canonical_validator.py",
    }
    candidates = []
    confirmed = []
    for path in paths:
        if Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(blobs[path]))
            if not matches:
                continue
            row = {
                "path": path,
                "class": class_name,
                "match_count": len(matches),
                "adjudication": "scanner_definition_not_payload" if path in definition_paths else "confirmed_payload_hit",
            }
            candidates.append(row)
            if row["adjudication"] == "confirmed_payload_hit":
                confirmed.append(row)
    return {
        "schema": "ghc.family.five-class-privacy.v688.v5.correction1",
        "scanned_path_count": len(paths),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "valid": not confirmed,
    }


def finalize() -> None:
    exclusions = [
        f"docs/elowen-cairn/{PHASE}/validation/correction1-delta-manifest.json",
        f"docs/elowen-cairn/{PHASE}/validation/correction1-owner-manifest.json",
        f"docs/elowen-cairn/{PHASE}/validation/correction1-privacy.json",
        f"docs/elowen-cairn/{PHASE}/validation/correction1-staged-review.json",
        f"docs/elowen-cairn/{PHASE}/correction1/content-seal.json",
    ]
    staged = sorted(line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line)
    material = [path for path in staged if path not in exclusions]
    blobs = batch_index(material)
    unexpected = [path for path in staged if not allowed(path)]
    manifest = {
        "schema": "ghc.family.normalized-lf-manifest.v688.v5.correction1",
        "anchor": "PENDING_CORRECTION1_COMMIT",
        "source": FIRST_FINAL,
        "byte_domain": "normalized_lf_git_index_blob",
        "declared_self_exclusions": exclusions,
        "entry_count": len(material),
        "entries": [entry(path, blobs[path]) for path in material],
    }
    write_json(VALIDATION / "correction1-delta-manifest.json", manifest)
    write_json(VALIDATION / "correction1-owner-manifest.json", {**manifest, "schema": "ghc.family.normalized-lf-owner-manifest.v688.v5.correction1"})
    write_json(VALIDATION / "correction1-privacy.json", privacy(material, blobs))
    write_json(
        VALIDATION / "correction1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v688.v5.correction1",
            "source": FIRST_FINAL,
            "expected_path_count": len(material) + len(exclusions),
            "expected_paths": sorted(material + exclusions),
            "unexpected_paths": unexpected,
            "deletions": [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=D").splitlines() if line],
            "prior_lifecycle_mutations": [path for path in staged if not allowed(path)],
        },
    )
    targets = [
        f"docs/elowen-cairn/{PHASE}/correction1/phase-truth.json",
        f"docs/elowen-cairn/{PHASE}/correction1/failed-canonical-binding.json",
        f"docs/elowen-cairn/{PHASE}/correction1/method-flow-overlay.json",
        f"docs/elowen-cairn/{PHASE}/correction1/lifecycle-replay.json",
        f"docs/elowen-cairn/{PHASE}/correction1/terminal-route-checklist.json",
        f"docs/elowen-cairn/{PHASE}/correction1/correction-overview.md",
    ]
    write_json(
        CORRECTION / "content-seal.json",
        {
            "schema": "ghc.family.content-seal.v688.v5.correction1",
            "byte_domain": "normalized_lf_git_index_blob",
            "target_count": len(targets),
            "targets": [entry(path, blobs[path]) for path in targets],
            "failed_canonical_preserved": True,
            "prepared_successor_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    if args.finalize_validation:
        finalize()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
