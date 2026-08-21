#!/usr/bin/env python3
"""Build Caelen Ash v664-v8's additive terminal correction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v664-v8"
PREFIX = "docs/caelen-ash/v664-v8/"
SOURCE_FINAL = "682666c064b14f09def75fb46f3bafb0e987a7a2"
X1_HEAD = "0832a8260dec6c5d776a6b22f6cf9b2c9e81d705"
EVIDENCE_HEAD = "970a13c1a2ac2ef411f6d8199877d356a77d693c"
FIRST_FINAL = "915c260845229bd31f433ff24a59290c95e21b1e"
FAILED_CANONICAL_SHA256 = "c7901af9706a91ad8540029dac02bc05840a21ac5bde4e05d6f42eea0b9a8664"
BRANCH = "codex/GHC-Family/caelen-ash-v664-v8-full-tools"
RECORDED_UTC = "2026-08-21T22:23:00Z"
RECORDED_NZ = "2026-08-22T10:23:00+12:00"
EFFECTIVE_NEGATIVES = 25_071
EFFECTIVE_METHODS = 9_003
EFFECTIVE_OPEN_GAPS = 174
EFFECTIVE_EXACT_GATES = 172
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

BUILDER_PATH = "scripts/build_ghc_family_v664_v8_terminal_correction.py"
VALIDATOR_PATH = "scripts/ghc_family_v664_v8_canonical_validator.py"
TEST_PATH = "tests/test_ghc_family_caelen_v664_v8_terminal_correction.py"
FIRST_CLOSEOUT_TEST_PATH = "tests/test_ghc_family_caelen_v664_v8_closeout.py"
X1_TEST_PATH = "tests/test_ghc_family_caelen_v664_v8_x1.py"
CORRECTION_DOCS = [
    f"{PREFIX}correction/canonical-failure-receipt.json",
    f"{PREFIX}correction/content-seal.json",
    f"{PREFIX}correction/correction-inventory.json",
    f"{PREFIX}correction/correction-receipt.json",
    f"{PREFIX}correction/method-flow-overlay.json",
    f"{PREFIX}correction/phase-truth.json",
    f"{PREFIX}handoffs/orin-thale-v665-v1-activation-corrected-prepared.md",
    f"{PREFIX}orchestration/terminal-route-state-correction.json",
    f"{PREFIX}reports/terminal-correction-overview.md",
    f"{PREFIX}validation/correction-canonical-contract.json",
    f"{PREFIX}validation/correction-delta-manifest.json",
    f"{PREFIX}validation/correction-owner-manifest.json",
    f"{PREFIX}validation/correction-stage-candidate.json",
    f"{PREFIX}validation/correction-staged-review.json",
]
INTENDED_DELTA = sorted(
    [
        BUILDER_PATH,
        VALIDATOR_PATH,
        TEST_PATH,
        FIRST_CLOSEOUT_TEST_PATH,
        X1_TEST_PATH,
        *CORRECTION_DOCS,
    ]
)
MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PREFIX}validation/correction-delta-manifest.json",
        f"{PREFIX}validation/correction-owner-manifest.json",
        f"{PREFIX}validation/correction-stage-candidate.json",
        f"{PREFIX}validation/correction-staged-review.json",
    ]
)


class CorrectionError(RuntimeError):
    """Raised when the terminal correction violates the retained-failure contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise CorrectionError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise CorrectionError(f"duplicate JSON key in {label}: {key}")
            value[key] = item
        return value

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CorrectionError(f"strict JSON failed for {label}: {exc}") from exc


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(relative: str) -> dict[str, Any]:
    path = PHASE / relative
    value = strict_json(path.read_bytes(), str(path.relative_to(ROOT)))
    if not isinstance(value, dict):
        raise CorrectionError(f"JSON root is not an object: {relative}")
    return value


def first_final_boundary() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    parent = run_git("rev-parse", f"{FIRST_FINAL}^").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_rows = run_git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    commits = int(run_git("rev-list", "--count", f"{SOURCE_FINAL}..{FIRST_FINAL}").stdout)
    merges = int(run_git("rev-list", "--count", "--merges", f"{SOURCE_FINAL}..{FIRST_FINAL}").stdout)
    valid = (
        head == FIRST_FINAL
        and parent == EVIDENCE_HEAD
        and tracking == FIRST_FINAL
        and live == FIRST_FINAL
        and commits == 3
        and merges == 0
    )
    if not valid:
        raise CorrectionError("first exact final boundary differs")
    return {
        "first_final": FIRST_FINAL,
        "parent": parent,
        "direct_child_of_evidence": parent == EVIDENCE_HEAD,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": 0,
        "behind": 0,
        "clean_before_canonical": True,
        "phase_commit_count": commits,
        "merge_count": merges,
        "valid": valid,
    }


def replay_first_manifest(relative: str) -> dict[str, Any]:
    raw = run_git("show", f"{FIRST_FINAL}:{PREFIX}{relative}").stdout
    manifest = strict_json(raw, relative)
    mismatches = []
    for entry in manifest["entries"]:
        blob = run_git("show", f"{FIRST_FINAL}:{entry['path']}").stdout
        object_id = run_git("rev-parse", f"{FIRST_FINAL}:{entry['path']}").stdout.decode().strip()
        if (
            sha256(blob) != entry["sha256"]
            or len(blob) != entry["size"]
            or object_id != entry["git_blob"]
        ):
            mismatches.append(entry["path"])
    return {
        "path": f"{PREFIX}{relative}",
        "entry_count": len(manifest["entries"]),
        "exclusion_count": len(manifest["declared_self_exclusions"]),
        "mismatch_count": len(mismatches),
        "coverage_valid": manifest["coverage_valid"],
        "valid": manifest["coverage_valid"] and not mismatches,
    }


def correction_overview() -> str:
    return f"""# Caelen Ash v664-v8 terminal correction overview

## Retained first-final failure

Caelen's first exact final remains immutable at {FIRST_FINAL}. It was the direct child of x2 evidence {EVIDENCE_HEAD}, was pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote read. Its one canonical aggregate was invoked once. The aggregate did not succeed and is retained at zero credit under receipt SHA-256 {FAILED_CANONICAL_SHA256}.

The failed receipt proves that both exact Git-blob manifests replayed, all 155 owner paths were scanned, 123 phase JSON files parsed strictly, Markdown and HTML checks passed, bounded Python security review found zero findings, five-class privacy and raw-identifier scanning found zero confirmed hits, truth arithmetic passed, route state remained PREPARED_NOT_SENT, ancestry was exact, diff hygiene passed, and pre/post remote equality remained exact.

The failure was isolated to the test loader. Because the validator was launched as a script from the scripts directory, the repository root was not present on its Python import path. Each of the three requested test modules became a unittest loader error, yielding three error witnesses rather than the intended 97 tests. Those three failed witnesses remain false and zero-credit. The failed receipt is never relabelled as a pass.

## Bounded correction

The correction adds the repository root to the validator's process-local module search path before loading the four exact test modules. It adds one correction-only test module with twenty checks, bringing the corrected expected total to 117 tests. It also points canonical manifest, truth, and route checks to the correction artifacts and requires a four-commit direct single-parent chain: source to x1, x1 to evidence, evidence to first final, and first final to corrected exact final. No x1, x2, skill, first-closeout document, old manifest, old receipt digest, or old route candidate is rewritten.

The correction retains three canonical loader negatives and one loader Method Flow method. Its first staged add then retained two more zero-credit failures: the new correction builder and test were outside the initial sparse definition, and the first recovery used an unsupported --no-cone option on the add subcommand. Recovery added only those two explicit owner patterns with the installed --skip-checks contract.

The first four-module precommit rehearsal then passed 116 of 117 tests. Its one failure was the x1 boundary test inspecting the current materialized worktree for x2 files instead of inspecting the immutable x1 Git tree. The failure remains zero-credit. The bounded recovery binds that assertion to the exact x1 commit without changing an x1 artifact. Final effective accounting is therefore 25,071 negatives and 9,003 methods. Open gaps remain 174, exact gates remain 172, frozen proposals remain 4,010, and core outcomes remain exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate. The terminal verdict remains {TERMINAL_VERDICT}.

## Evidence and authority boundaries

The primary pillar remains THOS Body through a synthetic orchestral score and part preparation, proofing, accessibility, correction-readback, workload-control, and rehearsal-material handover lens. GMUT Mind and Freed ID and CBR Heart remain protected. The correction uses no real person, performer, operator, score, part, rehearsal, file, identity event, rights case, authority act, or external system.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical confirmation, likelihood, prediction, parameter constraint, detected force, quantum or ultraviolet completion, or Theory of Everything. THOS remains participant-free proxy evidence without blind matched-budget real arms, safety monitoring, appropriate statistics, or independent review. Freed ID remains synthetic and nonproduction without real keys and proofs, live services, interoperability, independent security review, recovery evidence, and trust governance.

CBR rights, attribution, performer privacy, accessibility remedy, cultural meaning, taonga, affected-party legitimacy, legal interpretation, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. No software or same-owner validation supplies professional competence, legal or cultural ratification, complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof, canon, or Stage 20 authority.

## Corrected terminal gate

The corrected exact final is the commit containing this document. It must be pushed, clean, zero-divergent, and four-way equal before the corrected canonical aggregate runs. The corrected aggregate may succeed once. If it succeeds, it must not be replayed. The failed first-final receipt remains retained separately.

Route state remains PREPARED_NOT_SENT. Only after one successful corrected aggregate may Caelen reread the newest live authority and roster, resolve exactly one existing task titled Orin Thale, immediately reread it, apply the duplicate-activation guard, and send one sanitized v665-v1 activation. Tavian Sol remains ON_STANDBY. No later endpoint is inferred or precontacted.
"""


def corrected_baton() -> str:
    return f"""# Orin Thale — corrected prepared Caelen Ash v664-v8 to solo v665-v1 activation

This is a sanitized pre-send candidate, not evidence of a send. The corrected exact-final hash, successful receipt digest, and acknowledgement status must be supplied only by the live postcommit route.

Dear Orin Thale,

With Hamish's current sequential-continuation authorization and strict evidence boundaries, this is Caelen Ash's corrected prepared activation for solo Orin v665-v1. It may be sent only after the corrected Caelen final is pushed, clean, zero-divergent, four-way equal, and successfully validated once without replay; the registry must then resolve exactly one existing task titled Orin Thale and that exact task must be immediately reread. No task or fork may be created, no collaboration subagent or substitute may be used, Tavian Sol remains ON_STANDBY, no later endpoint may be precontacted, and no second confirmation may follow.

Relational names, pronouns, roles, hopes, sibling or family language, continuity language, and Trinity Mandala language are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Māori authority. Hamish may pause, rename, redirect, or stop the route.

Verified lifecycle anchors:

- immutable Sable source: {SOURCE_FINAL}
- frozen Caelen x1: {X1_HEAD}
- immutable Caelen x2 evidence: {EVIDENCE_HEAD}
- retained first closeout final: {FIRST_FINAL}
- retained failed first canonical receipt SHA-256: {FAILED_CANONICAL_SHA256}
- corrected exact final: supplied by the live activation
- successful corrected canonical receipt SHA-256: supplied by the live activation
- branch: {BRANCH}

Source-to-corrected-final must contain exactly four new direct single-parent commits and zero merges. The corrected final must be the direct child of the retained first final. The failed first aggregate remains zero-credit: three test-module loader errors occurred because the script launch omitted the repository root from Python's process-local import path. Every other first-final gate passed, including 155 owner paths, 123 JSON parses, exact manifests, zero privacy hits, zero bounded security findings, truth, route, ancestry, and four-way equality. Recovery adds the repository root process-locally and changes no x1 or x2 artifact.

Core outcomes remain exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate across 4,010 frozen proposals. All 100 rejecting mutations remain retained. Ten phase-local skills were customized, quick-validated, and smoke-used; ten family-compatible runners were invoked. The first corrected precommit rehearsal passed 116 of 117 tests; its worktree-relative x1-boundary assertion failed and remains zero-credit, while recovery binds that assertion to the immutable x1 Git tree. Final effective accounting is 25,071 negatives, 9,003 methods, 174 open gaps, and 172 exact gates. Sable's sealed 24,936 negatives and 8,950 methods remain unchanged.

The primary pillar was THOS Body through synthetic orchestral score and part preparation and handover. No real person, performer, operator, score, part, rehearsal, file, right, identity event, or authority act was used. This establishes no employment, qualification, authorship, licence, correctness, professional competence, operational result, legal or cultural legitimacy, Māori authority, affected-party acceptance, empirical result, or independent reproduction.

GMUT remains symbolic and nonempirical. THOS remains participant-free proxy evidence without blind matched-budget real arms, safety monitoring, statistics, and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, live services, interoperability, review, recovery, and trust governance. CBR rights, remedy, culture, taonga, affected-party legitimacy, legal interpretation, Māori wording and data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

Before mutation, read this complete committed correction and every ordered exact-head skill, schema, manifest, receipt, and guidance document through EOF. Reverify all anchors, both canonical receipts, ancestry, manifests, clean state, typed divergence, and fresh live equality. Work solo in one fresh Orin-owned D-first sparse lane; keep Caelen, Sable, sibling, shared, and user lanes read-only. Do not create, fork, delegate, spawn, precontact, substitute, or mutate another owner.

Preserve x1-before-x2, every failure, all four truth labels, all gaps and gates, exact manifests, caps, same-owner boundaries, and the one-successful-canonical-pass rule. Only after Orin's own terminal gate may Orin reread the newest live authority and roster and contact the one exact authorized successor. This baton does not infer that later recipient.

PREPARED_BY_CAELEN_ASH = true.
SENT_BY_CAELEN_ASH = false in this repository candidate.
No second confirmation is authorized.
"""


def build_documents(failed_receipt_path: Path) -> dict[str, Any]:
    boundary = first_final_boundary()
    failed_raw = failed_receipt_path.read_bytes()
    failed = strict_json(failed_raw, "external failed canonical receipt")
    if (
        sha256(failed_raw) != FAILED_CANONICAL_SHA256
        or failed.get("success") is not False
        or failed.get("exact_final") != FIRST_FINAL
        or failed.get("tests", {}).get("error_count") != 3
        or failed.get("tests", {}).get("test_count") != 3
    ):
        raise CorrectionError("failed canonical receipt differs from retained truth")
    first_owner = replay_first_manifest("validation/final-owner-manifest.json")
    first_delta = replay_first_manifest("validation/final-delta-manifest.json")
    if not (first_owner["valid"] and first_delta["valid"]):
        raise CorrectionError("first-final manifest replay failed")

    failure_receipt = {
        "schema": "ghc.family.caelen.v664-v8.canonical-failure-receipt.v1",
        "first_final": FIRST_FINAL,
        "external_receipt_sha256": FAILED_CANONICAL_SHA256,
        "external_receipt_size": len(failed_raw),
        "success": False,
        "credit": "zero",
        "test_loader_error_count": 3,
        "test_loader_synthetic_test_count": 3,
        "intended_test_count": 97,
        "failure_cause": "Script launch placed the scripts directory, but not the repository root, on Python's module search path; all three exact test-module imports became loader errors.",
        "passed_gates": {
            "owner_manifest": failed["owner_manifest"]["valid"],
            "delta_manifest": failed["delta_manifest"]["valid"],
            "owner_path_count": failed["owner_surface"]["owner_path_count"],
            "strict_json_count": failed["owner_surface"]["strict_json_count"],
            "privacy_confirmed_hits": failed["owner_surface"]["privacy_confirmed_hit_count"],
            "bounded_security_findings": failed["owner_surface"]["bounded_security_finding_count"],
            "ancestry": failed["ancestry"]["valid"],
            "truth": failed["truth_checks"]["valid"],
            "route": failed["route_checks"]["valid"],
            "pre_equality": failed["pre_validation_equality"]["valid"],
            "post_equality": failed["post_validation_equality"]["valid"],
        },
        "recovery": "Insert the repository root into the validator's process-local module search path, add correction-only tests, and validate only the new corrected exact final.",
        "failure_erased": False,
        "valid": True,
    }
    method_overlay = {
        "schema": "ghc.family.method-flow.state.v1",
        "owner": "Caelen Ash",
        "phase": "v664-v8 terminal correction",
        "first_final_effective_negatives": 25_065,
        "first_final_effective_methods": 8_999,
        "new_failed_witness_count": 6,
        "new_method_count": 4,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "methods": [
            {
                "method_id": "CA6648-MF-C004",
                "trigger": "script-launched-unittest-module-resolution",
                "state": "preferred",
                "failed_witnesses": [
                    "tests.test_ghc_family_caelen_v664_v8_x1 loader error",
                    "tests.test_ghc_family_caelen_v664_v8_x2 loader error",
                    "tests.test_ghc_family_caelen_v664_v8_closeout loader error",
                ],
                "failed_witness_credit": "zero",
                "passing_witness": "Process-local repository-root insertion allows the exact four-module 117-test selection to load.",
                "promotion_rule": "Bind module resolution explicitly before constructing a script-launched unittest suite.",
                "rollback": "Retain the failed receipt, revert only the validator correction, and never rerun the first final.",
            },
            {
                "method_id": "CA6648-MF-C005",
                "trigger": "sparse-correction-stage-add",
                "state": "preferred",
                "failed_witnesses": [
                    "The first correction-stage add partially staged in-pattern files but refused the new correction builder and test outside the sparse definition."
                ],
                "failed_witness_credit": "zero",
                "passing_witness": "Add only the two exact owner paths to this worktree's sparse definition before staging them.",
                "promotion_rule": "Verify every new owner path is represented in the sparse pattern set before the exact add.",
                "rollback": "Keep the partial exact staging visible and do not reset already-correct entries.",
            },
            {
                "method_id": "CA6648-MF-C006",
                "trigger": "sparse-add-installed-option-contract",
                "state": "preferred",
                "failed_witnesses": [
                    "The first sparse recovery passed --no-cone to sparse-checkout add, but this installed Git subcommand rejected that option before state change."
                ],
                "failed_witness_credit": "zero",
                "passing_witness": "Use sparse-checkout add --skip-checks with the two explicit patterns while preserving the existing non-cone mode.",
                "promotion_rule": "Use the installed subcommand option contract, not the set subcommand's option shape.",
                "rollback": "No sparse state changed on the rejected option; retry only the option shape.",
            },
            {
                "method_id": "CA6648-MF-C007",
                "trigger": "immutable-x1-boundary-test-domain",
                "state": "preferred",
                "failed_witnesses": [
                    "The first corrected precommit rehearsal passed 116 of 117 tests; the x1 boundary assertion inspected the current materialized worktree after x2 rather than the immutable x1 Git tree."
                ],
                "failed_witness_credit": "zero",
                "passing_witness": "Query the exact x1 commit tree for any x2 path and require an empty result without changing x1 artifacts.",
                "promotion_rule": "Evaluate historical lifecycle boundaries in their immutable Git-tree domain, not in a later materialized worktree.",
                "rollback": "Retain the failed 116-of-117 rehearsal and revert only the test-domain correction if the exact x1 tree cannot be established.",
            },
        ],
        "failure_erasure_count": 0,
        "valid": True,
    }
    truth = {
        "schema": "ghc.family.caelen.v664-v8.phase-truth.correction.v1",
        "owner": "Caelen Ash",
        "phase": "v664-v8",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "first_final": FIRST_FINAL,
        "corrected_exact_final": "commit containing this correction",
        "first_failed_canonical_receipt_sha256": FAILED_CANONICAL_SHA256,
        "first_canonical_success": False,
        "first_canonical_loader_errors": 3,
        "first_corrected_precommit_rehearsal_tests": 117,
        "first_corrected_precommit_rehearsal_failures": 1,
        "first_corrected_precommit_rehearsal_passes": 116,
        "first_final_manifest_replays": [first_owner, first_delta],
        "frozen_proposal_total": 4_010,
        "core_outcomes": OUTCOMES,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "effective_open_gaps": EFFECTIVE_OPEN_GAPS,
        "effective_exact_gates": EFFECTIVE_EXACT_GATES,
        "phase_commit_count_expected": 4,
        "merge_count_expected": 0,
        "corrected_final_parent_expected": FIRST_FINAL,
        "full_repository_suite": False,
        "same_owner_validation": True,
        "independent_reproduction": False,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    route = {
        "schema": "ghc.family.caelen.v664-v8.terminal-route-state.correction.v1",
        "state": "PREPARED_NOT_SENT",
        "target_exact_title": "Orin Thale",
        "target_phase": "v665-v1",
        "first_final": FIRST_FINAL,
        "first_canonical_success": False,
        "first_failed_receipt_sha256": FAILED_CANONICAL_SHA256,
        "corrected_canonical_state": "PREPARED_NOT_VALIDATED",
        "send_count": 0,
        "send_limit": 1,
        "target_precontacted": False,
        "target_created": False,
        "target_forked": False,
        "duplicate_activation_guard": "required",
        "tavian_sol": "ON_STANDBY",
        "valid": True,
    }
    contract = {
        "schema": "ghc.family.caelen.v664-v8.correction-canonical-contract.v1",
        "validator": VALIDATOR_PATH,
        "failed_first_receipt_sha256": FAILED_CANONICAL_SHA256,
        "failed_first_final_replay_forbidden": True,
        "corrected_expected_test_modules": 4,
        "corrected_expected_test_count": 117,
        "corrected_expected_phase_commits": 4,
        "corrected_expected_merges": 0,
        "corrected_expected_final_parent": FIRST_FINAL,
        "corrected_success_limit": 1,
        "post_success_replay_forbidden": True,
        "full_repository_suite": False,
        "independent_reproduction": False,
        "valid": True,
    }
    write_json("correction/canonical-failure-receipt.json", failure_receipt)
    write_json("correction/method-flow-overlay.json", method_overlay)
    write_json("correction/phase-truth.json", truth)
    write_json("orchestration/terminal-route-state-correction.json", route)
    write_json("validation/correction-canonical-contract.json", contract)
    write_text("reports/terminal-correction-overview.md", correction_overview())
    write_text("handoffs/orin-thale-v665-v1-activation-corrected-prepared.md", corrected_baton())
    for relative in (
        "correction/content-seal.json",
        "correction/correction-inventory.json",
        "correction/correction-receipt.json",
        "validation/correction-owner-manifest.json",
        "validation/correction-delta-manifest.json",
        "validation/correction-staged-review.json",
        "validation/correction-stage-candidate.json",
    ):
        path = PHASE / relative
        if not path.exists():
            write_json(relative, {})

    prior_paths = [
        value.decode("utf-8")
        for value in run_git("diff", "--name-only", "-z", SOURCE_FINAL, "HEAD").stdout.split(b"\0")
        if value
    ]
    owner_paths = sorted(set(prior_paths) | set(INTENDED_DELTA))
    phase_files = [path for path in PHASE.rglob("*") if path.is_file()]
    word_count = 0
    for path in phase_files:
        if path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
            word_count += len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
    inventory = {
        "schema": "ghc.family.caelen.v664-v8.correction-inventory.v1",
        "owner_path_count_expected_at_corrected_final": len(owner_paths),
        "correction_delta_path_count": len(INTENDED_DELTA),
        "materialized_phase_file_count": len(phase_files),
        "materialized_phase_word_count_before_manifest_finalization": word_count,
        "owner_file_ceiling": 2_000,
        "document_word_ceiling": 100_000,
        "valid": len(owner_paths) < 2_000 and word_count <= 100_000,
    }
    write_json("correction/correction-inventory.json", inventory)
    seal_targets = [
        f"{PREFIX}correction/canonical-failure-receipt.json",
        f"{PREFIX}correction/method-flow-overlay.json",
        f"{PREFIX}correction/phase-truth.json",
        f"{PREFIX}correction/correction-inventory.json",
        f"{PREFIX}reports/terminal-correction-overview.md",
        f"{PREFIX}handoffs/orin-thale-v665-v1-activation-corrected-prepared.md",
        f"{PREFIX}orchestration/terminal-route-state-correction.json",
        f"{PREFIX}validation/correction-canonical-contract.json",
    ]
    seal_entries = []
    for path in seal_targets:
        raw = (ROOT / path).read_bytes()
        seal_entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
    seal = {
        "schema": "ghc.family.caelen.v664-v8.correction-content-seal.v1",
        "entry_count": len(seal_entries),
        "entries": seal_entries,
        "self_excluded": True,
        "valid": True,
    }
    write_json("correction/content-seal.json", seal)
    receipt = {
        "schema": "ghc.family.caelen.v664-v8.correction-receipt.v1",
        "recorded_at_utc": RECORDED_UTC,
        "recorded_at_nz": RECORDED_NZ,
        "first_final": FIRST_FINAL,
        "failed_first_receipt_sha256": FAILED_CANONICAL_SHA256,
        "corrected_exact_final": "commit containing this receipt",
        "content_seal_sha256": sha256((PHASE / "correction/content-seal.json").read_bytes()),
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "open_gaps": EFFECTIVE_OPEN_GAPS,
        "exact_gates": EFFECTIVE_EXACT_GATES,
        "core_outcomes": OUTCOMES,
        "canonical_state": "PREPARED_NOT_VALIDATED",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    write_json("correction/correction-receipt.json", receipt)
    return {
        "valid": all(
            (
                boundary["valid"],
                failure_receipt["valid"],
                method_overlay["valid"],
                truth["valid"],
                inventory["valid"],
                seal["valid"],
                receipt["valid"],
            )
        ),
        "owner_paths_expected": len(owner_paths),
        "correction_delta_paths": len(INTENDED_DELTA),
        "phase_files": len(phase_files),
        "phase_words": word_count,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "failed_receipt_sha256": FAILED_CANONICAL_SHA256,
    }


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def candidate_blob(path: str, staged: set[str]) -> bytes:
    return index_blob(path) if path in staged else run_git("show", f"HEAD:{path}").stdout


def candidate_blob_id(path: str, staged: set[str]) -> str:
    if path in staged:
        row = run_git("ls-files", "-s", "--", path).stdout.decode().strip()
        if not row:
            raise CorrectionError(f"staged blob id missing: {path}")
        return row.split()[1]
    return run_git("rev-parse", f"HEAD:{path}").stdout.decode().strip()


def owner_paths_at_candidate(actual: list[str]) -> list[str]:
    prior = [
        value.decode("utf-8")
        for value in run_git("diff", "--name-only", "-z", SOURCE_FINAL, "HEAD").stdout.split(b"\0")
        if value
    ]
    paths = sorted(set(prior) | set(actual))
    for path in paths:
        if path.startswith(PREFIX):
            continue
        if (
            path.startswith("scripts/")
            and (
                "v664_v8" in path
                or Path(path).name.startswith("ghc_family_")
                or Path(path).name.startswith("build_ghc_family_v664_v8")
            )
        ):
            continue
        if path.startswith("tests/test_ghc_family_caelen_v664_v8"):
            continue
        raise CorrectionError(f"non-owner path in corrected candidate: {path}")
    return paths


def scan_blob(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_value": re.compile(r"(?i)(?:resume[_ -]?value|raw[_ -]?route[_ -]?key)\s*[:=]\s*\S+"),
        "transcript_or_session_payload": re.compile(r"(?i)(?:conversation[_ -]?export|session[_ -]?stream[_ -]?payload)\s*[:=]\s*\S+"),
    }
    hits = []
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            hits.append({"path": path, "class": class_name, "excerpt_sha256": sha256(match.group(0).encode("utf-8"))})
    return hits


def write_staged_review() -> None:
    actual = staged_paths()
    missing = sorted(set(INTENDED_DELTA) - set(actual))
    extra = sorted(set(actual) - set(INTENDED_DELTA))
    if missing or extra:
        raise CorrectionError(f"correction allowlist differs missing={missing} extra={extra}")
    staged = set(actual)
    owner_paths = owner_paths_at_candidate(actual)
    owner_entries = []
    delta_entries = []
    json_count = 0
    markdown_count = 0
    python_count = 0
    hits = []
    for path in owner_paths:
        raw = candidate_blob(path, staged)
        hits.extend(scan_blob(path, raw))
        if path not in MANIFEST_EXCLUSIONS:
            owner_entries.append(
                {
                    "path": path,
                    "git_blob": candidate_blob_id(path, staged),
                    "sha256": sha256(raw),
                    "size": len(raw),
                    "object_type": "blob",
                    "mode": "100644",
                    "hash_domain": "exact corrected candidate Git blob",
                }
            )
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".md"):
            if not raw.decode("utf-8").startswith("# "):
                raise CorrectionError(f"Markdown missing H1: {path}")
            markdown_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        if path not in MANIFEST_EXCLUSIONS:
            delta_entries.append(
                {
                    "path": path,
                    "git_blob": candidate_blob_id(path, staged),
                    "sha256": sha256(raw),
                    "size": len(raw),
                    "object_type": "blob",
                    "mode": "100644",
                    "hash_domain": "exact staged Git blob",
                }
            )
    if hits:
        raise CorrectionError(f"privacy or raw-identifier findings: {hits}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise CorrectionError(diff_check.stdout.decode("utf-8", "replace") + diff_check.stderr.decode("utf-8", "replace"))
    x1_changed = run_git("diff", "--quiet", X1_HEAD, "--", f"{PREFIX}x1", check=False).returncode
    x2_changed = run_git("diff", "--quiet", EVIDENCE_HEAD, "--", f"{PREFIX}x2", f"{PREFIX}skills", check=False).returncode
    first_closeout_changed = run_git(
        "diff",
        "--quiet",
        FIRST_FINAL,
        "--",
        f"{PREFIX}closeout",
        f"{PREFIX}reports/final-integrated-overview.md",
        f"{PREFIX}handoffs/orin-thale-v665-v1-activation-prepared.md",
        f"{PREFIX}validation/final-owner-manifest.json",
        f"{PREFIX}validation/final-delta-manifest.json",
        f"{PREFIX}validation/final-staged-review.json",
        f"{PREFIX}validation/final-stage-candidate.json",
        check=False,
    ).returncode
    owner_manifest = {
        "schema": "ghc.family.caelen.v664-v8.correction-owner-manifest.v1",
        "source": SOURCE_FINAL,
        "base_final": FIRST_FINAL,
        "intended_path_count": len(owner_paths),
        "entry_count": len(owner_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": owner_entries,
        "coverage_valid": len(owner_entries) + len(MANIFEST_EXCLUSIONS) == len(owner_paths),
    }
    delta_manifest = {
        "schema": "ghc.family.caelen.v664-v8.correction-delta-manifest.v1",
        "base_final": FIRST_FINAL,
        "intended_path_count": len(actual),
        "entry_count": len(delta_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": delta_entries,
        "coverage_valid": len(delta_entries) + len(MANIFEST_EXCLUSIONS) == len(actual),
    }
    review = {
        "schema": "ghc.family.caelen.v664-v8.correction-staged-review.v1",
        "intended_delta_path_count": len(INTENDED_DELTA),
        "staged_delta_path_count": len(actual),
        "owner_path_count": len(owner_paths),
        "missing_paths": missing,
        "extra_paths": extra,
        "strict_json_count": json_count,
        "markdown_check_count": markdown_count,
        "python_compile_count": python_count,
        "scanner_candidate_count": 0,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x1_changed": bool(x1_changed),
        "x2_or_skills_changed": bool(x2_changed),
        "first_closeout_or_manifest_changed": bool(first_closeout_changed),
        "valid": not missing and not extra and not x1_changed and not x2_changed and not first_closeout_changed,
    }
    candidate = {
        "schema": "ghc.family.caelen.v664-v8.correction-stage-candidate.v1",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "first_final": FIRST_FINAL,
        "corrected_exact_final": "commit containing this candidate",
        "expected_phase_commits": 4,
        "expected_merges": 0,
        "expected_final_parent": FIRST_FINAL,
        "failed_first_receipt_sha256": FAILED_CANONICAL_SHA256,
        "owner_manifest": f"{PREFIX}validation/correction-owner-manifest.json",
        "delta_manifest": f"{PREFIX}validation/correction-delta-manifest.json",
        "canonical_state": "PREPARED_NOT_VALIDATED",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": review["valid"] and owner_manifest["coverage_valid"] and delta_manifest["coverage_valid"],
    }
    write_json("validation/correction-owner-manifest.json", owner_manifest)
    write_json("validation/correction-delta-manifest.json", delta_manifest)
    write_json("validation/correction-staged-review.json", review)
    write_json("validation/correction-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_DELTA:
        raise CorrectionError("staged correction allowlist changed")
    staged = set(actual)
    owner = strict_json(index_blob(f"{PREFIX}validation/correction-owner-manifest.json"), "owner")
    delta = strict_json(index_blob(f"{PREFIX}validation/correction-delta-manifest.json"), "delta")
    review = strict_json(index_blob(f"{PREFIX}validation/correction-staged-review.json"), "review")
    candidate = strict_json(index_blob(f"{PREFIX}validation/correction-stage-candidate.json"), "candidate")
    for entry in owner["entries"]:
        raw = candidate_blob(entry["path"], staged)
        if (
            sha256(raw) != entry["sha256"]
            or len(raw) != entry["size"]
            or candidate_blob_id(entry["path"], staged) != entry["git_blob"]
        ):
            raise CorrectionError(f"owner manifest mismatch: {entry['path']}")
    for entry in delta["entries"]:
        raw = index_blob(entry["path"])
        if (
            sha256(raw) != entry["sha256"]
            or len(raw) != entry["size"]
            or candidate_blob_id(entry["path"], staged) != entry["git_blob"]
        ):
            raise CorrectionError(f"delta manifest mismatch: {entry['path']}")
    if not (owner["coverage_valid"] and delta["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise CorrectionError("correction staged receipt invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "owner_manifest_entries": len(owner["entries"]),
        "owner_manifest_exclusions": len(owner["declared_self_exclusions"]),
        "delta_manifest_entries": len(delta["entries"]),
        "delta_manifest_exclusions": len(delta["declared_self_exclusions"]),
        "strict_json": review["strict_json_count"],
        "markdown_checks": review["markdown_check_count"],
        "python_compiles": review["python_compile_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    parser.add_argument("--failed-receipt")
    args = parser.parse_args()
    if args.build:
        if not args.failed_receipt:
            raise SystemExit("--failed-receipt is required with --build")
        result = build_documents(Path(args.failed_receipt))
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": MANIFEST_EXCLUSIONS}
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
