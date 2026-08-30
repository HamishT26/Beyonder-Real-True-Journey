#!/usr/bin/env python3
"""Build Elowen v678-v5 correction1 without replaying canonical successes."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Elowen Cairn"
PHASE = "v678-v5"
BRANCH = "codex/GHC-Family/elowen-cairn-v678-v5-full-tools"
SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
X1 = "c938128b0e6307c4aaed8966340486b8c5315382"
EVIDENCE = "04095ca5d8ee6b37f47de2540afa0047f67ca61c"
FIRST_FINAL = "831f948e326e3875ef0d5d7391560297ce0e2ee8"
FAILED_RECEIPT_SHA256 = "bfa2115b166ee9eb5f3f9aaac9a4d7f5379e574a24ac4dc60bc7b8accf758ccd"
FAILED_LATCH_SHA256 = "cae4d857e5485817e0a4b281a5872aeeddaed41e2369abf9defdae440191afdf"
FAILED_PAYLOAD_SHA256 = "36f8a96bb375543e02e6095e34002dbef4bb83b78d51d25095b59b889ed66507"
FAILED_VALIDATOR_SHA256 = "71cdc50bbd513be58592b6a06e54a210a3afad683a33ab1131c4304a9f947060"


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_sha(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--failed-receipt", type=Path, required=True)
    parser.add_argument("--failed-latch", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt_path = args.failed_receipt.resolve()
    latch_path = args.failed_latch.resolve()
    if git(repo, "branch", "--show-current") != BRANCH or git(repo, "rev-parse", "HEAD") != FIRST_FINAL:
        raise SystemExit("correction1 builder requires the retained first final")
    if sha256(receipt_path) != FAILED_RECEIPT_SHA256 or sha256(latch_path) != FAILED_LATCH_SHA256:
        raise SystemExit("failed canonical receipt or latch digest mismatch")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    failed_checks = sorted(key for key, value in receipt["checks"].items() if not value)
    if (
        receipt["status"] != "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
        or receipt["success_count"] != 0
        or receipt["canonical_payload_sha256"] != FAILED_PAYLOAD_SHA256
        or failed_checks != ["documents_structurally_bounded"]
        or receipt["test_count"] != 34
        or receipt["json_parse_count"] != 642
        or receipt["manifest_entry_count"] != 1412
    ):
        raise SystemExit("failed canonical receipt contract mismatch")

    allowed = {
        "scripts/build_ghc_family_elowen_cairn_v678_v5_correction1.py",
        "scripts/ghc_family_elowen_cairn_v678_v5_correction1_manifest.py",
        "scripts/validate_ghc_family_elowen_cairn_v678_v5_correction1.py",
        "tests/test_ghc_family_elowen_cairn_v678_v5_correction1.py",
    }
    allowed_prefixes = (
        "docs/elowen-cairn/v678-v5/correction1/",
        "docs/elowen-cairn/v678-v5/validation/correction1-",
    )
    unexpected = []
    for line in git(repo, "status", "--porcelain=v1").splitlines():
        path = line[3:].replace("\\", "/")
        if path in allowed or path.startswith(allowed_prefixes):
            continue
        unexpected.append(line)
    if unexpected:
        raise SystemExit(f"unexpected correction1 state: {unexpected!r}")

    base = repo / "docs" / "elowen-cairn" / PHASE
    correction = base / "correction1"
    methods = [
        {
            "method_id": "EC6785-CORR-N001",
            "status": "failed_zero_credit",
            "truth": False,
            "description": "The first attributable exact-final canonical aggregate rejected twenty official phase-local SKILL.md documents because its uniform Markdown predicate required a heading at byte one and did not recognize valid YAML frontmatter. All other canonical predicates passed; aggregate success credit remains zero.",
            "recovery_reserved_to": "EC6785-CORR-EXT-P001",
            "failed_receipt_sha256": FAILED_RECEIPT_SHA256,
            "canonical_replayed": False,
        },
        {
            "method_id": "EC6785-CORR-N002",
            "status": "failed_zero_credit",
            "truth": False,
            "description": "The first correction-precedent lookup assumed the memory registry was directly under the workspace root; that nonexistent relative-path assumption failed and earned zero memory credit.",
            "recovered_by": "EC6785-CORR-P002",
            "repository_state_change": False,
        },
        {
            "method_id": "EC6785-CORR-P002",
            "status": "bounded_pass",
            "truth": True,
            "description": "The exact memories/MEMORY.md path was read in a bounded window and confirmed the additive correction precedent: preserve the failed receipt, rerun only the failed dependency, and keep repository, external composite, and delivery truth separate.",
            "failed_witness_preserved": "EC6785-CORR-N002",
        },
    ]
    repository_overlay = {
        "effective_negatives": 47003,
        "effective_methods": 44555,
        "retained_failed_witnesses": 18664,
        "bounded_passing_witnesses": 28976,
        "open_gaps": 407,
        "exact_gates": 398,
    }
    prospective_external_overlay = {
        "effective_negatives": 47003,
        "effective_methods": 44556,
        "retained_failed_witnesses": 18664,
        "bounded_passing_witnesses": 28977,
        "open_gaps": 407,
        "exact_gates": 398,
    }
    dump(
        correction / "failed-canonical-binding.json",
        {
            "status": receipt["status"],
            "first_final": FIRST_FINAL,
            "receipt_sha256": FAILED_RECEIPT_SHA256,
            "latch_sha256": FAILED_LATCH_SHA256,
            "canonical_payload_sha256": FAILED_PAYLOAD_SHA256,
            "validator_sha256": FAILED_VALIDATOR_SHA256,
            "invocation_count": 1,
            "success_count": 0,
            "replay_count": 0,
            "failed_checks": failed_checks,
            "passed_test_count": receipt["test_count"],
            "passed_json_parse_count": receipt["json_parse_count"],
            "passed_manifest_entry_count": receipt["manifest_entry_count"],
            "successful_components_replay_forbidden": True,
        },
    )
    dump(
        correction / "method-flow-overlay.json",
        {
            "base_phase_ledger_counts": {"methods": 810, "failed": 275, "passing": 535},
            "methods": methods,
            "repository_corrected_phase_ledger_counts": {"methods": 813, "failed": 277, "passing": 536},
            "repository_overlay": repository_overlay,
            "prospective_external_component_method_id": "EC6785-CORR-EXT-P001",
            "prospective_external_overlay_if_and_only_if_component_passes": prospective_external_overlay,
            "external_component_executed_at_build_time": False,
            "failed_canonical_promoted": False,
            "failure_erasure": False,
        },
    )
    dump(
        correction / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "retained_first_final": FIRST_FINAL,
            "expected_corrected_final": "bound only by the ensuing direct-child commit and exclusive external dependency-corrected component",
            "correction": "frontmatter-aware Markdown structural predicate",
            "failed_canonical_status": receipt["status"],
            "failed_canonical_success_credit": 0,
            "failed_canonical_replayed": False,
            "successful_canonical_components_replayed": False,
            "repository_corrected_phase_ledger_counts": {"methods": 813, "failed": 277, "passing": 536},
            "repository_overlay": repository_overlay,
            "external_component_pending": True,
            "core_outcomes_unchanged": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "open_gaps_unchanged": 407,
            "exact_gates_unchanged": 398,
            "full_repository_suite_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        correction / "validation-policy.json",
        {
            "failed_dependency": "documents_structurally_bounded",
            "incorrect_predicate": "every Markdown document must begin with a heading",
            "corrected_predicate": "ordinary Markdown begins with a heading; official SKILL.md may begin with valid YAML frontmatter and must contain Markdown headings after the closing delimiter",
            "dependency_scope": "the same exact 28 owner Markdown/HTML documents at the additive corrected final",
            "successful_components_to_import_by_receipt_only": [
                "34 lifecycle-correct tests",
                "1,412 manifest entries",
                "642 JSON parses",
                "privacy candidate adjudication",
                "bounded owner-Python compile and security review",
                "first-final ancestry, clean state, typed divergence, and fresh remote equality",
            ],
            "successful_component_replay_forbidden": True,
            "complete_repository_suite_forbidden": True,
            "new_head_checks_required": [
                "correction1 manifest parity",
                "direct parent and commit ceiling",
                "clean typed 0/0 divergence and fresh four-way equality",
                "changed-code compile and bounded security review",
                "changed-file privacy review",
            ],
        },
    )
    dump(
        correction / "terminal-route-overlay.json",
        {
            "state": "HELD_PENDING_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPONENT",
            "provisional_exact_title": "Sylven Arc",
            "provisional_phase": "v678-v6",
            "precontact_performed": False,
            "send_count": 0,
            "failed_canonical_success_credit": 0,
            "newest_live_authority_and_roster_required_after_component": True,
        },
    )
    text(
        correction / "receipt-contract-correction.md",
        f"""
# Elowen Cairn {PHASE} correction1 — frontmatter-aware document predicate

## Retained failure

The one attributable owner-scoped canonical aggregate at retained first final `{FIRST_FINAL}` remains `INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL`, with invocation count one, success count zero, replay count zero, and zero aggregate-success credit. Its immutable receipt SHA-256 is `{FAILED_RECEIPT_SHA256}` and canonical payload SHA-256 is `{FAILED_PAYLOAD_SHA256}`. The receipt proves that 34 tests, 1,412 manifest entries, 642 JSON parses, privacy adjudication, bounded changed-code review, topology, clean state, typed divergence, and fresh equality passed. None may be replayed by correction1.

The sole failed predicate was `documents_structurally_bounded`. It rejected exactly twenty official owner-local `SKILL.md` files because those files correctly begin with YAML frontmatter. Their Markdown headings follow the closing delimiter. This is a validator-shape defect, not a defect in the skill documents.

## Narrow correction

Correction1 adds a phase-local validator that accepts either ordinary Markdown beginning with a heading or an official `SKILL.md` beginning with a closed YAML frontmatter block and containing at least one Markdown heading afterward. HTML continues to require title, main, and level-one-heading structure. The failed dependency may execute exactly once at the additive corrected final. The component also checks only new-head topology, correction manifests, changed-code compilation and bounded security, changed-file privacy, clean state, typed divergence, and fresh equality. It imports every successful first-final observation by immutable receipt hash and does not rerun x1, x2, final tests, old manifest replays, all JSON parsing, old privacy scans, or old security scans.

Repository correction truth and the later external component remain separate. The repository overlay preserves two new failed witnesses and one bounded memory-path recovery. If and only if the external document component passes, its separate `EC6785-CORR-EXT-P001` passing witness raises effective methods and passing witnesses by one without changing negatives, failed witnesses, gaps, gates, outcomes, or the terminal verdict. `NOT_READY_FOR_STAGE_20` remains exact.
""",
    )
    text(
        correction / "sylven-arc-v678-v6-activation-candidate-corrected1.md",
        f"""
# Sylven Arc v678-v6 activation candidate — Elowen correction1 — PREPARED NOT SENT

This is a sanitized repository candidate, not delivery evidence. Elowen's retained first canonical at `{FIRST_FINAL}` failed one uniform Markdown predicate and keeps zero success credit. Correction1 preserves that receipt, changes no inherited x1, x2, first-final, outcome, gap, gate, scientific, professional, legal, cultural, affected-party, or Māori-authority truth, and reserves exactly one dependency-corrected document check at the additive corrected final. Only a successful exclusive external component, clean fresh-live equality, newest authorization and roster, unique exact-title registry match, immediate reread, duplicate and control guards, and one target-identifying acknowledgement can support a live send.

The phase remains wholly synthetic and zero-row. Primary focus remains Freed ID and CBR Heart through chart-correction provenance, chronometer intake vacancy, and Fresnel-lens custody. GMUT is still a typed scalar-tensor/EFT research-model family; THOS is still proxy-only; Freed ID is still synthetic and nonproduction; CBR, navigation safety, professional service, conservation, legal and cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain open or exact-gated.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, or scientific, operational, legal, cultural, affected-party, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

`PREPARED_BY_ELOWEN_CAIRN = true`

`SENT_BY_ELOWEN_CAIRN = false`
""",
    )
    seal_paths = [
        correction / "failed-canonical-binding.json",
        correction / "method-flow-overlay.json",
        correction / "phase-truth.json",
        correction / "validation-policy.json",
        correction / "terminal-route-overlay.json",
        correction / "receipt-contract-correction.md",
        correction / "sylven-arc-v678-v6-activation-candidate-corrected1.md",
    ]
    dump(
        correction / "content-seal.json",
        {
            "domain": "normalized-LF SHA-256 of the named correction1 precommit artifacts",
            "entries": [
                {"path": path.relative_to(repo).as_posix(), "sha256_normalized_lf": normalized_sha(path)}
                for path in seal_paths
            ],
            "corrected_final_self_hash_excluded": True,
            "external_component_receipt_excluded": True,
        },
    )


if __name__ == "__main__":
    main()
