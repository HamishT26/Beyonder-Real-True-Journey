#!/usr/bin/env python3
"""Build the additive Caelen Ash v668-v6 terminal-correction overlay.

The first final remains immutable. This builder records two failed validation
invocations at zero credit and corrects only the scanner self-match accounting
needed by the separately named terminal composite.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-ash" / "v668-v6"
REL_PHASE_ROOT = "docs/caelen-ash/v668-v6"
SOURCE = "5bced658a5b3f5bd7c4d88d47057d795abe57f42"
X1 = "c5c18b81f26c8851b984e4bcb3dff1db1212fd36"
EVIDENCE = "d42953afd61753490e9c77138409e179d44974d8"
FIRST_FINAL = "4e87a72ab4f796854b7d2bee30c0143ae91887e2"
BRANCH = "codex/GHC-Family/caelen-ash-v668-v6-full-tools"
CANONICAL_RECEIPT_SHA256 = "f44ce2e540dd75d38edebf684338da1e51ce5e47862f579b2e0f4f52594a1971"
FIRST_COMPOSITE_RECEIPT_SHA256 = "a9a8da6ca8c6a3ff62a77ef0c52627818b5c31abc3488b190f470c5ebea350b4"
OLD_OWNER_MANIFEST = f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json"
CORRECTION_DELTA_MANIFEST = f"{REL_PHASE_ROOT}/validation/correction-delta-manifest.json"
CORRECTION_OWNER_MANIFEST = f"{REL_PHASE_ROOT}/validation/correction-owner-manifest.json"
BASE_COUNTS = {
    "effective_negatives": 29955,
    "methods": 16541,
    "failed_witnesses": 2256,
    "passing_witnesses": 3083,
    "open_gaps": 219,
    "exact_gates": 214,
}
CORRECTED_COUNTS = {
    "effective_negatives": 29959,
    "methods": 16545,
    "failed_witnesses": 2260,
    "passing_witnesses": 3087,
    "open_gaps": 219,
    "exact_gates": 214,
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_receipt(path: Path, expected_sha: str, expected_status: str) -> dict[str, Any]:
    data = path.read_bytes()
    actual_sha = sha256(data)
    if actual_sha != expected_sha:
        raise AssertionError({"unexpected_receipt_sha256": actual_sha})
    receipt = json.loads(data)
    if receipt.get("status") != expected_status:
        raise AssertionError({"unexpected_receipt_status": receipt.get("status")})
    if receipt.get("canonical_success_count") != 0:
        raise AssertionError("failed validation receipt must retain zero canonical-success credit")
    return receipt


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def old_blob(relative: str) -> tuple[str, bytes]:
    oid = git("rev-parse", f"{FIRST_FINAL}:{relative}")
    data = subprocess.run(
        ["git", "show", f"{FIRST_FINAL}:{relative}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    return oid, data


def exists_at_first_final(relative: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{FIRST_FINAL}:{relative}"], cwd=ROOT, capture_output=True
    ).returncode == 0


def manifest_row(path: Path) -> dict[str, Any]:
    relative = path.relative_to(ROOT).as_posix()
    if exists_at_first_final(relative):
        oid, data = old_blob(relative)
        if git("diff", "--name-only", FIRST_FINAL, "--", relative):
            raise AssertionError(f"first-final path changed during additive correction: {relative}")
        domain = "immutable_first_final_git_blob"
    else:
        data = path.read_bytes()
        oid = subprocess.run(
            ["git", "hash-object", "-w", f"--path={relative}", "--stdin"],
            cwd=ROOT,
            input=data,
            check=True,
            capture_output=True,
        ).stdout.decode("ascii").strip()
        data = subprocess.run(
            ["git", "cat-file", "blob", oid], cwd=ROOT, check=True, capture_output=True
        ).stdout
        domain = "projected_terminal_correction_git_blob"
    return {
        "path": relative,
        "git_blob_oid": oid,
        "sha256": sha256(data),
        "bytes": len(data),
        "canonical_domain": domain,
    }


def manifest_rows(paths: Iterable[Path]) -> list[dict[str, Any]]:
    return [manifest_row(path) for path in sorted(set(paths))]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-receipt", type=Path, required=True)
    parser.add_argument("--first-composite-receipt", type=Path, required=True)
    args = parser.parse_args()
    if git("rev-parse", "HEAD") != FIRST_FINAL:
        raise AssertionError("terminal correction must begin at the retained first final")
    if git("branch", "--show-current") != BRANCH:
        raise AssertionError("unexpected owner branch")
    if git("rev-parse", "HEAD^") != EVIDENCE:
        raise AssertionError("first final is not the direct child of immutable evidence")
    if git("rev-parse", f"{EVIDENCE}^") != X1 or git("rev-parse", f"{X1}^") != SOURCE:
        raise AssertionError("source x1 evidence lineage drifted")
    if git("rev-list", "--merges", f"{SOURCE}..HEAD"):
        raise AssertionError("merge found in owner lifecycle")

    canonical = read_receipt(
        args.canonical_receipt,
        CANONICAL_RECEIPT_SHA256,
        "FAILED_ONCE_ZERO_CANONICAL_SUCCESS_CREDIT",
    )
    first_composite = read_receipt(
        args.first_composite_receipt,
        FIRST_COMPOSITE_RECEIPT_SHA256,
        "DEPENDENCY_CORRECTED_COMPOSITE_FAILED_ZERO_CREDIT",
    )
    generated_at = utc_now()

    write_json("correction/privacy-self-match-correction.json", {
        "phase": "v668-v6",
        "retained_first_final": FIRST_FINAL,
        "conceptual_scanner_definitions": 2,
        "actual_raw_pattern_self_matches": 1,
        "actual_scanner_definition_self_matches": 1,
        "confirmed_payload_hits": 0,
        "matched_class": 5,
        "non_self_matching_class": 2,
        "reason": "the class-2 detector contains an escaped separator in source and therefore does not match its own source literal",
        "old_final_disposition_status": "retained_inexact_raw-candidate_count",
        "privacy_complete": False,
        "generated_at": generated_at,
    })
    write_json("correction/retained-validation-failures.json", {
        "phase": "v668-v6",
        "base_repository_seal": BASE_COUNTS,
        "corrected_repository_seal": CORRECTED_COUNTS,
        "failures": [
            {
                "id": "CA6686-N025",
                "status": "failed_zero_credit",
                "kind": "canonical_aggregate",
                "receipt_sha256": CANONICAL_RECEIPT_SHA256,
                "failure": canonical["error_summary"],
                "recovery": "document word ceiling isolated to document extensions while Python remains under AST and security review",
            },
            {
                "id": "CA6686-N026",
                "status": "failed_zero_credit",
                "kind": "isolated_git_projection_wrapper",
                "failure": "the first per-entry Git projection lost its terminal wrapper output after launch",
                "recovery": "a bounded clean-worktree projection completed without changing repository state",
            },
            {
                "id": "CA6686-N027",
                "status": "failed_zero_credit",
                "kind": "first_dependency_corrected_composite",
                "receipt_sha256": FIRST_COMPOSITE_RECEIPT_SHA256,
                "failure": first_composite["error_summary"],
                "recovery": "this additive overlay distinguishes conceptual scanner definitions from actual raw pattern self-matches",
            },
            {
                "id": "CA6686-N028",
                "status": "failed_zero_credit",
                "kind": "first_terminal_correction_staged_review",
                "failure": "eight projected document SHA values used worktree CRLF bytes while their staged Git blobs were normalized to LF",
                "recovery": "hash each filtered projected blob and then read the exact Git blob bytes before recording SHA-256 and byte length",
            },
        ],
        "canonical_invocations": 1,
        "canonical_successes": 0,
        "canonical_replayed": False,
        "first_composite_replayed": False,
        "all_failures_retained": True,
        "generated_at": generated_at,
    })
    write_json("correction/method-flow-overlay.json", {
        "phase": "v668-v6",
        "base_counts": BASE_COUNTS,
        "corrected_counts": CORRECTED_COUNTS,
        "methods": [
            {
                "method_id": "CA6686-M-N025",
                "failed_witness": "CA6686-N025",
                "passing_witness": "CA6686-P-N025",
                "failure_retained": True,
                "rule": "document ceilings apply to documents; source code receives syntax and bounded security checks",
            },
            {
                "method_id": "CA6686-M-N026",
                "failed_witness": "CA6686-N026",
                "passing_witness": "CA6686-P-N026",
                "failure_retained": True,
                "rule": "a missing wrapper receipt stays false; recovery uses a bounded clean-state projection",
            },
            {
                "method_id": "CA6686-M-N027",
                "failed_witness": "CA6686-N027",
                "passing_witness": "CA6686-P-N027",
                "failure_retained": True,
                "rule": "scanner-definition inventory and actual regex self-match count are separate predicates",
            },
            {
                "method_id": "CA6686-M-N028",
                "failed_witness": "CA6686-N028",
                "passing_witness": "CA6686-P-N028",
                "failure_retained": True,
                "rule": "manifest SHA and byte claims use the exact filtered Git blob rather than pre-filter worktree bytes",
            },
        ],
        "credit_rule": "a passing correction never rewrites its paired failed witness",
        "generated_at": generated_at,
    })
    write_json("correction/phase-truth.json", {
        "owner": "Caelen Ash",
        "phase": "v668-v6",
        "retained_first_final": FIRST_FINAL,
        "corrected_final": "SUPPLIED_AFTER_ADDITIVE_COMMIT",
        "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "outcome_counts": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "frozen_proposal_chain": 4830,
        "repository_sealed_counts": CORRECTED_COUNTS,
        "canonical_invocation_count": 1,
        "canonical_success_count": 0,
        "canonical_aggregate_replayed": False,
        "first_dependency_corrected_composite_replayed": False,
        "terminal_composite_state": "PENDING_ONE_SEPARATELY_NAMED_CORRECTED_COMPOSITE",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "generated_at": generated_at,
    })
    write_json("correction/external-validation-receipts.json", {
        "phase": "v668-v6",
        "canonical": {
            "sha256": CANONICAL_RECEIPT_SHA256,
            "status": canonical["status"],
            "canonical_success_count": 0,
        },
        "first_dependency_corrected_composite": {
            "sha256": FIRST_COMPOSITE_RECEIPT_SHA256,
            "status": first_composite["status"],
            "canonical_success_count": 0,
        },
        "raw_receipts_are_external": True,
        "private_paths_recorded": False,
        "generated_at": generated_at,
    })
    write_json("route/prepared-route-state-correction.json", {
        "owner": "Caelen Ash",
        "phase": "v668-v6",
        "state": "PREPARED_NOT_SENT",
        "successor_exact_title": "UNRESOLVED_UNTIL_CORRECTED_TERMINAL_GATE",
        "successor_contacted": False,
        "single_send_maximum": 1,
        "canonical_success_count": 0,
        "corrected_terminal_composite": "PENDING",
        "stop_on_ambiguity_or_missing_acknowledgement": True,
        "generated_at": generated_at,
    })
    write_text("correction/terminal-correction-overview.md", f"""
# Caelen Ash v668-v6 additive terminal correction

The retained first final `{FIRST_FINAL}` remains immutable. Its sole canonical aggregate failed once because a document word ceiling was applied to Python source. That aggregate has zero canonical-success credit and was never replayed. The first separately named dependency-corrected composite also failed once because it expected two raw privacy-pattern self-matches while the exact Git blobs contain one. It likewise has zero credit and was never replayed.

This correction does not erase either failure. It distinguishes two conceptual scanner definitions from one actual raw self-match. The one raw match is a scanner-definition literal in the x2 test source; there are zero confirmed payload hits. The class-2 detector does not match its own escaped source representation. This is bounded owner-scope evidence, not complete privacy assurance.

Repository truth after retaining the four post-seal failures is {CORRECTED_COUNTS['effective_negatives']:,} effective negatives, {CORRECTED_COUNTS['methods']:,} methods, {CORRECTED_COUNTS['failed_witnesses']:,} failed witnesses, {CORRECTED_COUNTS['passing_witnesses']:,} bounded passing witnesses, {CORRECTED_COUNTS['open_gaps']} open gaps, and {CORRECTED_COUNTS['exact_gates']} exact gates. Core outcomes remain exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. The proposal chain remains 4,830 and the verdict remains `NOT_READY_FOR_STAGE_20`.

No empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim is created. A separately named corrected terminal composite may validate the additive corrected head once; it may not replay or promote the failed canonical aggregate or the failed first composite.

Generated at {generated_at}.
""")
    write_text("handoffs/successor-terminal-correction-basis.md", f"""
# Caelen Ash v668-v6 corrected terminal handoff basis — prepared, not sent

This sanitized basis supports at most one later live activation after the additive corrected head is committed, pushed, clean, fresh-live equal, and passes one separately named corrected terminal composite. It does not name or infer a successor. The current live roster, authorization state, bounded task registry, and exact target must be refreshed after that gate.

Immutable anchors are source `{SOURCE}`, x1 `{X1}`, evidence `{EVIDENCE}`, and retained first final `{FIRST_FINAL}`. The corrected final is supplied only in the acknowledged live activation. Source-to-corrected-final must contain four direct single-parent commits and zero merges.

The canonical receipt `{CANONICAL_RECEIPT_SHA256}` records one failed canonical invocation and zero successes. The first composite receipt `{FIRST_COMPOSITE_RECEIPT_SHA256}` records one failed separately named composite and zero credit. Neither invocation may be replayed or relabelled. The corrected terminal composite is a distinct bounded recovery and cannot award canonical-success credit.

Outcomes remain 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`; the corrected repository seal is {CORRECTED_COUNTS['effective_negatives']:,} negatives, {CORRECTED_COUNTS['methods']:,} methods, {CORRECTED_COUNTS['failed_witnesses']:,} failed witnesses, {CORRECTED_COUNTS['passing_witnesses']:,} bounded passing witnesses, {CORRECTED_COUNTS['open_gaps']} gaps, and {CORRECTED_COUNTS['exact_gates']} gates. The verdict remains `NOT_READY_FOR_STAGE_20`.

Names, pronouns, role, hope, sibling or family language, continuity language, Freed ID, CBR, and Trinity Mandala language are relational working language only. They establish no consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Maori authority.

PREPARED_BY_CAELEN_ASH = true
SENT_BY_CAELEN_ASH = false

Generated at {generated_at}.
""")

    new_relatives = [
        f"{REL_PHASE_ROOT}/correction/privacy-self-match-correction.json",
        f"{REL_PHASE_ROOT}/correction/retained-validation-failures.json",
        f"{REL_PHASE_ROOT}/correction/method-flow-overlay.json",
        f"{REL_PHASE_ROOT}/correction/phase-truth.json",
        f"{REL_PHASE_ROOT}/correction/external-validation-receipts.json",
        f"{REL_PHASE_ROOT}/correction/terminal-correction-overview.md",
        f"{REL_PHASE_ROOT}/route/prepared-route-state-correction.json",
        f"{REL_PHASE_ROOT}/handoffs/successor-terminal-correction-basis.md",
        "scripts/build_ghc_family_caelen_ash_v668_v6_terminal_correction.py",
        "tests/test_ghc_family_caelen_ash_v668_v6_correction.py",
    ]
    new_paths = [ROOT / relative for relative in new_relatives]
    missing = [path.relative_to(ROOT).as_posix() for path in new_paths if not path.is_file()]
    if missing:
        raise AssertionError({"missing_correction_paths": missing})
    delta_rows = manifest_rows(new_paths)
    delta_path = write_json("validation/correction-delta-manifest.json", {
        "phase": "v668-v6",
        "expected_parent": FIRST_FINAL,
        "scope": "exact additive terminal-correction content excluding both correction manifests",
        "entry_count": len(delta_rows),
        "entries": delta_rows,
        "self_exclusions": [CORRECTION_DELTA_MANIFEST, CORRECTION_OWNER_MANIFEST],
        "generated_at": generated_at,
    })

    old_owner = json.loads((ROOT / OLD_OWNER_MANIFEST).read_text(encoding="utf-8"))
    owner_relatives = {row["path"] for row in old_owner["entries"]}
    owner_relatives.add(OLD_OWNER_MANIFEST)
    owner_relatives.update(new_relatives)
    owner_relatives.add(delta_path.relative_to(ROOT).as_posix())
    owner_relatives.discard(CORRECTION_OWNER_MANIFEST)
    owner_rows = manifest_rows(ROOT / relative for relative in owner_relatives)
    write_json("validation/correction-owner-manifest.json", {
        "phase": "v668-v6",
        "source": SOURCE,
        "frozen_x1": X1,
        "evidence": EVIDENCE,
        "retained_first_final": FIRST_FINAL,
        "scope": "complete corrected Caelen owner packet excluding this self-referential correction manifest",
        "entry_count": len(owner_rows),
        "entries": owner_rows,
        "self_exclusions": [CORRECTION_OWNER_MANIFEST],
        "owner_file_ceiling": 2000,
        "generated_at": generated_at,
    })
    print(json.dumps({
        "state": "ADDITIVE_TERMINAL_CORRECTION_BUILT",
        "correction_delta_entries": len(delta_rows),
        "correction_owner_entries": len(owner_rows),
        "corrected_counts": CORRECTED_COUNTS,
        "canonical_success_count": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
