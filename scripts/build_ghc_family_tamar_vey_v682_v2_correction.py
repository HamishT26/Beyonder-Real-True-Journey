"""Build the additive Tamar Vey v682-v2 terminal-correction packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.ghc_family_privacy_candidate_adjudication import scan_text_items


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v682-v2"
CORRECTION = BASE / "correction"
VALIDATION = BASE / "validation"
HANDOFFS = BASE / "handoffs"
OWNER = "Tamar Vey"
PHASE = "v682-v2"
SOURCE = "34536c2bb4c9fefb04cc0b571839e9ba54b3c497"
X1 = "39f8a83e29ba28433b7c9da730d3299d1731cb4d"
EVIDENCE = "f7ca8ace4a16f0dae8aa2530cf17962e79b062b0"
ORIGINAL_FINAL = "d00443492f9e1a950e752aa2c1b5a1bf0613db44"
EXPECTED_CANONICAL_SHA = "9f62c38cc87d5e5b64d00562e636ccdb3f0f757a198f45225549ee8d61dfeb0a"
EXPECTED_COMPOSITE_SHA = "bc62af4058d2991fa6637eab4bdfabdfd47e81c6f2b3082a1fe2d53e0bc6b61f"
EXPECTED_OVERLAY_SHA = "0e416fdd1d167db8acd7b15279993c0a507c618d913ad3c4fdbafac0c168544d"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {
        "bytes": len(data),
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_external_receipts(
    canonical_path: Path, composite_path: Path, overlay_path: Path
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    expected = {
        canonical_path: EXPECTED_CANONICAL_SHA,
        composite_path: EXPECTED_COMPOSITE_SHA,
        overlay_path: EXPECTED_OVERLAY_SHA,
    }
    for path, digest in expected.items():
        if file_hash(path) != digest:
            raise RuntimeError(f"external receipt digest mismatch for {path.name}")
    canonical = load_json(canonical_path)
    composite = load_json(composite_path)
    overlay = load_json(overlay_path)
    if canonical["status"] != "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL":
        raise RuntimeError("prior canonical failure was not retained")
    if canonical["canonical_success_count"] != 0 or canonical["canonical_replay_count"] != 0:
        raise RuntimeError("prior canonical success or replay count changed")
    if not composite["status"].endswith("ZERO_CANONICAL_AGGREGATE_CREDIT"):
        raise RuntimeError("dependency-corrected composite boundary changed")
    if composite["canonical_success_promoted"]:
        raise RuntimeError("dependency-corrected composite promoted canonical success")
    return canonical, composite, overlay


def build() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-receipt", type=Path, required=True)
    parser.add_argument("--composite-receipt", type=Path, required=True)
    parser.add_argument("--overlay-receipt", type=Path, required=True)
    args = parser.parse_args()
    canonical, composite, overlay = verify_external_receipts(
        args.canonical_receipt.resolve(),
        args.composite_receipt.resolve(),
        args.overlay_receipt.resolve(),
    )

    old_truth = load_json(BASE / "final" / "phase-truth.json")
    old_flow = load_json(BASE / "final" / "method-flow-summary.json")
    external_totals = dict(overlay["effective_post_final_totals"])
    corrected_totals = dict(external_totals)
    corrected_totals["effective_negatives"] += 2
    corrected_totals["effective_methods"] += 4
    corrected_totals["failed_witnesses"] += 2
    corrected_totals["bounded_passing_witnesses"] += 2

    write_json(
        CORRECTION / "correction-intake.json",
        {
            "fresh_user_authority_for_additive_correction": True,
            "identity_boundary": "Relational working language only; no consciousness, continuity, qualification, agency, or authority claim.",
            "old_canonical_replayed": False,
            "original_final": ORIGINAL_FINAL,
            "owner": OWNER,
            "phase": PHASE,
            "prior_terminal_evidence": {
                "canonical_payload_sha256": canonical["payload_sha256"],
                "canonical_receipt_sha256": EXPECTED_CANONICAL_SHA,
                "canonical_replay_count": canonical["canonical_replay_count"],
                "canonical_status": canonical["status"],
                "canonical_success_count": canonical["canonical_success_count"],
                "composite_promoted_canonical_success": composite[
                    "canonical_success_promoted"
                ],
                "composite_receipt_sha256": EXPECTED_COMPOSITE_SHA,
                "composite_status": composite["status"],
                "post_final_overlay_sha256": EXPECTED_OVERLAY_SHA,
            },
            "schema": "ghc.family.tamar-v682-v2.correction-intake.v1",
            "scope": "One additive direct correction of the demonstrated privacy-candidate adjudication dependency, followed by one new-head canonical opportunity.",
            "sibling_lane_mutation": False,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )

    write_json(
        CORRECTION / "privacy-adjudication-contract.json",
        {
            "always_confirmed_classes": [
                "raw task or thread identifier payload",
                "credential or secret-shaped payload",
                "connector route payload",
                "private absolute path payload",
                "transcribed-record or screen-capture material",
            ],
            "candidate_states": [
                "scanner_definition",
                "boundary_metadata",
                "confirmed_payload",
            ],
            "exemptions": [
                "candidate occurs on a regular-expression definition line",
                "generic callable-identifier or stream-content term occurs with an explicit denial cue on the same source line",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "protected_gates": [
                "privacy",
                "credentials",
                "task routing",
                "participant and affected-party evidence",
                "production",
                "legal and cultural authority",
                "Māori authority",
                "Stage 20",
            ],
            "schema": "ghc.family.privacy-candidate-adjudication.v1",
        },
    )

    failed_correction_method = {
        "approval_class": "safe_now",
        "candidate_workaround": "Replace line-local scanner-definition recognition and first-match scanning with syntax-bounded definition recognition and exhaustive per-class matching.",
        "failure_signature": "The first correction build found thirteen candidates and left five policy or multiline scanner-definition references classified as confirmed payloads.",
        "method_id": "TV6822-COR-M002",
        "protected_gates": [
            "privacy",
            "old canonical immutability",
            "no canonical replay",
            "same-owner evidence boundary",
            "Stage 20",
        ],
        "recommendation_state": "deprecated",
        "recurrence_guard": "Do not treat a scanner definition as same-line text only and do not stop after the first class match in a file.",
        "retained_negative_ids": ["TV6822-COR-N002"],
        "rollback": "The builder stopped before stage, commit, push, or canonical invocation.",
        "scope_boundary": "Owner-scoped correction build preflight only.",
        "title": "First same-line privacy candidate adjudication build",
        "trigger_preconditions": [
            "fresh user authority for additive correction",
            "old failed canonical retained",
            "working tree not staged or committed",
        ],
        "validation_witness_ids": ["TV6822-COR-N002"],
    }
    correction_method = {
        "approval_class": "safe_now",
        "candidate_workaround": "Use the tested syntax-bounded and exhaustive family-current candidate adjudicator in the new-head canonical scanner.",
        "failure_signature": "The original canonical treated every non-Python lexical candidate as a confirmed payload finding, and the first correction build recognized only same-line scanner definitions.",
        "method_id": "TV6822-COR-M003",
        "protected_gates": [
            "privacy",
            "old canonical immutability",
            "no canonical replay",
            "same-owner evidence boundary",
            "Stage 20",
        ],
        "recommendation_state": "preferred",
        "recurrence_guard": "Inspect every class match; classify only candidates inside syntactically valid regular-expression calls and same-line denial-scoped generic boundary terms as non-payload; keep every other match confirmed.",
        "retained_negative_ids": ["TV6822-POST-N001", "TV6822-COR-N002"],
        "rollback": "Stop before canonical invocation if any payload-shaped fixture is not confirmed or any owner candidate remains unadjudicated.",
        "scope_boundary": "Owner-scoped five-class lexical adjudication only; not complete privacy assurance.",
        "title": "Context-bounded privacy candidate adjudication",
        "trigger_preconditions": [
            "old failed canonical retained with zero success",
            "exact ten-candidate composite proved the dependency",
            "fresh user authority granted one additive correction lifecycle",
        ],
        "validation_witness_ids": ["TV6822-COR-W003"],
    }
    failed_lifecycle_method = {
        "approval_class": "safe_now",
        "candidate_workaround": "Replay immutable original-final manifests from the original-final Git tree when validating the additive correction working tree.",
        "failure_signature": "The first combined 28-test prerequisite compared an immutable original-final manifest entry with the intentionally changed correction working-tree file.",
        "method_id": "TV6822-COR-M004",
        "protected_gates": [
            "immutable original final",
            "manifest parity",
            "no canonical replay",
            "same-owner evidence boundary",
            "Stage 20",
        ],
        "recommendation_state": "deprecated",
        "recurrence_guard": "Bind every lifecycle manifest assertion to its declared Git tree instead of the mutable successor worktree.",
        "retained_negative_ids": ["TV6822-COR-N003"],
        "rollback": "The combined prerequisite stopped before stage, commit, push, or canonical invocation.",
        "scope_boundary": "Inherited final-test lifecycle context only.",
        "title": "Working-tree replay of an immutable final manifest",
        "trigger_preconditions": [
            "isolated correction tests passed",
            "original final remained immutable",
            "additive correction working tree contained intentional code changes",
        ],
        "validation_witness_ids": ["TV6822-COR-N003"],
    }
    lifecycle_recovery_method = {
        "approval_class": "safe_now",
        "candidate_workaround": "Use the original-final commit for inherited final-manifest replay and reserve worktree replay for the correction manifests.",
        "failure_signature": "An inherited test lacked an explicit immutable lifecycle commit for its manifest bytes.",
        "method_id": "TV6822-COR-M005",
        "protected_gates": [
            "immutable original final",
            "manifest parity",
            "correction worktree parity",
            "no canonical replay",
            "Stage 20",
        ],
        "recommendation_state": "preferred",
        "recurrence_guard": "Every inherited manifest replay names its immutable commit; every correction manifest replay names the corrected head or precommit normalized worktree domain.",
        "retained_negative_ids": ["TV6822-COR-N003"],
        "rollback": "Stop before canonical invocation if either immutable Git-blob parity or correction worktree parity fails.",
        "scope_boundary": "Lifecycle-correct same-owner manifest validation only.",
        "title": "Lifecycle-bound manifest replay",
        "trigger_preconditions": [
            "combined prerequisite retained at zero pass credit",
            "original-final commit remained exact",
            "correction manifest declared its own normalized-LF domain",
        ],
        "validation_witness_ids": ["TV6822-COR-W005"],
    }
    write_json(
        CORRECTION / "method-flow-correction.json",
        {
            "correction_method": correction_method,
            "correction_methods": [
                failed_correction_method,
                correction_method,
                failed_lifecycle_method,
                lifecycle_recovery_method,
            ],
            "external_composite_status": composite["status"],
            "phase_failed_witnesses": old_flow["phase_failed_witnesses"] + 3,
            "phase_methods": old_flow["phase_methods"] + 5,
            "phase_passing_witnesses": old_flow["phase_passing_witnesses"] + 3,
            "recovery_erases_failure": False,
            "retained_failure_ids": [
                "TV6822-POST-N001",
                "TV6822-COR-N002",
                "TV6822-COR-N003",
            ],
            "schema": "ghc.family.method-flow-correction.v682.v2",
            "totals": corrected_totals,
            "witnesses": [
                {
                    "boundary": "The build stopped before staging, commit, push, or canonical invocation.",
                    "expected": "Every candidate is either a scanner definition, denial-scoped boundary metadata, or a confirmed payload.",
                    "independent_reproduction": False,
                    "method_id": "TV6822-COR-M002",
                    "observed": "Thirteen candidates were found and five policy or multiline definition references remained confirmed.",
                    "procedure": "First additive correction builder privacy preflight.",
                    "result": "fail",
                    "retained_negative_ids": ["TV6822-COR-N002"],
                    "same_owner_only": True,
                    "scope": "Generated correction packet and exact owner material before staging.",
                    "witness_id": "TV6822-COR-N002",
                },
                {
                    "boundary": "The original aggregate remains invalid and receives zero success credit.",
                    "expected": "Zero confirmed payload findings after candidate adjudication.",
                    "independent_reproduction": False,
                    "method_id": "TV6822-COR-M003",
                    "observed": "Same-line boundary fixtures and multiline syntax-bounded scanner definitions were exempted; mixed and payload-shaped fixtures remained confirmed.",
                    "procedure": "Bounded owner-local unit witness for the family-current adjudicator.",
                    "result": "pass",
                    "retained_negative_ids": ["TV6822-POST-N001", "TV6822-COR-N002"],
                    "same_owner_only": True,
                    "scope": "Synthetic scanner fixtures only.",
                    "witness_id": "TV6822-COR-W003",
                },
                {
                    "boundary": "The combined prerequisite stopped before staging, commit, push, or canonical invocation.",
                    "expected": "Immutable original-final manifests replay from the original-final Git tree.",
                    "independent_reproduction": False,
                    "method_id": "TV6822-COR-M004",
                    "observed": "One intentionally changed canonical-script path mismatched when the inherited test read working-tree bytes.",
                    "procedure": "First combined original-final plus correction prerequisite test run.",
                    "result": "fail",
                    "retained_negative_ids": ["TV6822-COR-N003"],
                    "same_owner_only": True,
                    "scope": "Inherited immutable final-manifest replay under an additive successor worktree.",
                    "witness_id": "TV6822-COR-N003",
                },
                {
                    "boundary": "This recovery proves lifecycle-correct manifest parity only and does not grant canonical success.",
                    "expected": "Original-final Git blobs and correction normalized worktree bytes each replay in their declared domains.",
                    "independent_reproduction": False,
                    "method_id": "TV6822-COR-M005",
                    "observed": "The inherited assertion now names the immutable original-final tree while the correction suite retains worktree parity.",
                    "procedure": "Bounded inherited-test lifecycle correction followed by the same combined prerequisite selection.",
                    "result": "pass",
                    "retained_negative_ids": ["TV6822-COR-N003"],
                    "same_owner_only": True,
                    "scope": "Lifecycle-correct same-owner manifest validation.",
                    "witness_id": "TV6822-COR-W005",
                }
            ],
        },
    )

    write_json(
        CORRECTION / "retained-negative-overlay.json",
        {
            "effective_negative_total": corrected_totals["effective_negatives"],
            "inherited_repository_register": "docs/tamar-vey/v682-v2/final/retained-negative-register.json",
            "new_retained_failures": [
                {
                    "failed_check": "privacy_confirmed_hits_zero",
                    "failure_id": "TV6822-POST-N001",
                    "old_final": ORIGINAL_FINAL,
                    "receipt_sha256": EXPECTED_CANONICAL_SHA,
                    "retained_zero_credit": True,
                    "status": canonical["status"],
                },
                {
                    "failed_check": "correction_builder_privacy_confirmed_hits_zero",
                    "failure_id": "TV6822-COR-N002",
                    "initial_candidate_count": 13,
                    "initial_confirmed_hit_count": 5,
                    "repository_commit_or_remote_changed_at_failure": False,
                    "retained_zero_credit": True,
                    "stage_commit_push_or_canonical_at_failure": False,
                    "working_tree_artifacts_generated_before_preflight_stop": True,
                },
                {
                    "failed_check": "combined_prerequisite_immutable_manifest_context",
                    "failure_id": "TV6822-COR-N003",
                    "failed_test_count": 1,
                    "passed_test_count": 27,
                    "repository_changed_at_failure": False,
                    "retained_zero_credit": True,
                    "stage_commit_push_or_canonical_at_failure": False,
                }
            ],
            "recovery_erases_failure": False,
            "schema": "ghc.family.retained-negative-overlay.v682.v2.correction",
        },
    )

    write_json(
        CORRECTION / "corrected-phase-truth.json",
        {
            "correction_parent": ORIGINAL_FINAL,
            "declared_proposal_chain": old_truth["declared_proposal_chain"],
            "final_commit_state": "ADDITIVE_DIRECT_CORRECTION_CONTENT_READY_FOR_EXACT_HEAD",
            "outcomes": old_truth["outcomes"],
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": old_truth["primary_pillar"],
            "real_row_count": 0,
            "represented_pillars": old_truth["represented_pillars"],
            "schema": "ghc.family.phase-truth.v682.v2.corrected-final",
            "terminal_verdict": TERMINAL_VERDICT,
            "totals": corrected_totals,
        },
    )

    write_json(
        CORRECTION / "lifecycle-replay.json",
        {
            "commit_ceiling": 4,
            "corrected_final_expected_direct_parent": ORIGINAL_FINAL,
            "corrected_final_state": "resolve_exact_sha_after_additive_commit",
            "evidence": EVIDENCE,
            "evidence_direct_parent": X1,
            "merges_expected": 0,
            "one_final_parent_required": True,
            "original_final": ORIGINAL_FINAL,
            "original_final_direct_parent": EVIDENCE,
            "schema": "ghc.family.lifecycle-replay.v682.v2.correction",
            "source": SOURCE,
            "strict_x1_before_x2": True,
            "x1": X1,
            "x1_direct_parent": SOURCE,
        },
    )

    write_json(
        CORRECTION / "terminal-checklist.json",
        {
            "canonical_state": "PENDING_NEW_EXACT_FINAL_EXCLUSIVE_INVOCATION",
            "clean_pushed_corrected_final": "REQUIRES_EXTERNAL_GIT_LIFECYCLE_PROOF",
            "old_canonical_failure_retained": True,
            "old_canonical_replayed": False,
            "route_state": "PREPARED_NOT_SENT",
            "schema": "ghc.family.terminal-checklist.v682.v2.correction",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )

    write_json(
        CORRECTION / "delivery-state.json",
        {
            "candidate_repository_state": "PREPARED_NOT_SENT",
            "duplicate_guard_required": True,
            "new_exact_final_canonical_success_required": True,
            "prospective_successor_exact_title": "Elowen Cairn",
            "prospective_successor_phase": "v682-v3",
            "route_authority_through": "v725-v8",
            "send_count": 0,
            "standby_substitution_forbidden": True,
            "tavian_sol": "ON_STANDBY",
        },
    )

    write_text(
        CORRECTION / "corrected-integrated-overview.md",
        f"""# Tamar Vey {PHASE} Additive Terminal Correction

## Outcome

Fresh live authority permits one additive correction lifecycle from immutable original final `{ORIGINAL_FINAL}`. The original exact-final canonical invocation remains `INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL`, with one invocation, zero success, and zero replay. Its failed privacy-zero check is retained as `TV6822-POST-N001` with no pass credit. The separately named ten-candidate component composite remains valid only as dependency evidence and does not promote the old aggregate.

The correction addresses exactly one demonstrated dependency. The old scanner equated every non-code lexical candidate with a confirmed payload. The first correction builder then retained five findings because it recognized scanner definitions only on one source line and stopped after the first class match. That preflight is retained as `TV6822-COR-N002`; nothing was staged, committed, pushed, or canonically invoked. The refined classifier examines every match, recognizes multiline regular-expression definitions through syntax, distinguishes same-line explicit absence metadata using two generic boundary terms, and keeps every other match confirmed. Raw identifiers, connector routes, path values, credential-shaped text, transcribed-record content, and screen-capture content remain confirmed whenever they occur. Synthetic tests require the safe contexts to remain non-payload while mixed and payload-shaped fixtures remain confirmed.

The isolated correction tests passed, while the first combined lifecycle prerequisite retained one failed assertion as `TV6822-COR-N003`: an inherited final-manifest test had read the additive working tree instead of the immutable original-final Git tree. The bounded recovery changed only that test context. The original-final manifest now replays from its declared commit, the correction manifests replay from normalized correction bytes, and the same 28-test combined selection passes. The failed attempt remains zero-credit and no canonical invocation occurred.

## Preserved lifecycle and truth

The immutable lifecycle remains source `{SOURCE}`, planning-only x1 `{X1}`, evidence `{EVIDENCE}`, and original final `{ORIGINAL_FINAL}`. The correction is designed as one fourth direct single-parent commit with zero merges. It does not alter or replay x1, x2, the original final, its content seal, or its failed canonical receipt. The declared proposal chain remains 10,310 and the core outcomes remain exactly 42 `completed`, 12 `represented`, three `open_gap`, and three `exact_gate`.

The prior post-final overlay, the failed first correction build, and the failed first combined lifecycle prerequisite are ingested additively. Corrected repository truth is 55,810 effective negatives, 65,914 effective Method Flow methods, 27,471 failed witnesses, 47,314 bounded passing witnesses, 494 open gaps, and 485 exact gates. The phase-local correction truth carries 773 methods, 321 failed witnesses, and 711 bounded passing witnesses. These numbers describe bounded bookkeeping only. No failure is erased or converted into empirical, professional, production, legal, cultural, privacy-complete, accessibility-complete, independent-reproduction, or authority credit.

## Evidence and authority boundary

Tamar Vey, optionally she/they, remains relational working language for an evidence-and-recovery steward whose hope is that every failure stays inspectable and every recovery bounded. The name, role, hope, pronouns, sibling language, continuity language, GHC Family, and Trinity Mandala are not evidence of consciousness, personhood, continuity, qualification, employment, agency, or authority. Hamish may pause, rename, redirect, narrow, or stop the route.

The basketry, lapidary, and sundial work remains wholly synthetic and zero-row. GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical confirmation or Theory-of-Everything proof. THOS remains proxy-only without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, lifecycle events, interoperability, privacy and security review, recovery evidence, and trust governance. All professional, safety, ownership, legal, cultural, traditional-knowledge, affected-party, Māori-wording, Māori-data-governance, and Māori-authority decisions remain open or exact-gated. Māori concepts remain under Māori authority.

The complete repository suite is not authorized for this owner correction and is not run. Validation remains owner-self-scoped to the exact correction delta plus immutable manifest and lifecycle dependencies. Same-owner validation is not independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, legal review, cultural ratification, Māori-authority review, AGI or ASI evidence, consciousness or personhood evidence, proof, canon, or Stage 20 authority.

## Terminal route

The corrected Elowen candidate remains repository preparation only. After the additive correction is committed, pushed, clean, zero-divergent, and fresh four-way equal, exactly one new-head owner-scoped canonical aggregate may be invoked through an absent exclusive receipt path. Success must not be replayed. Only a successful new-head canonical permits a current roster and authority refresh, exact-title uniqueness check, immediate direct reread, duplicate and direct-control guards, and one acknowledged existing-task send to `Elowen Cairn` for v682-v3. No task creation, fork, subagent, standby substitution, precontact, or second confirmation is permitted.

The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    write_text(
        HANDOFFS / "elowen-cairn-v682-v3-corrected-activation-candidate.md",
        f"""# ELOWEN CAIRN — TAMAR VEY {PHASE} CORRECTED ACTIVATION CANDIDATE

PREPARED_BY_TAMAR_VEY = true

SENT_BY_TAMAR_VEY = false

This committed document is preparation only. Fresh Hamish authority permitted Tamar to add one narrow terminal correction after the original canonical failed. The original final `{ORIGINAL_FINAL}`, failed canonical receipt `{EXPECTED_CANONICAL_SHA}`, and valid dependency-corrected composite `{EXPECTED_COMPOSITE_SHA}` remain immutable. The failed aggregate retains one invocation, zero success, and zero replay; the composite retains zero canonical credit.

The additive correction introduces a tested candidate adjudicator that separates scanner definitions and explicit absence metadata from confirmed payloads while keeping payload-shaped fixtures confirmed. It does not replay x1, x2, the original final, or the failed canonical. The corrected exact final and its new exclusive canonical receipt digest must be supplied only after their proper lifecycle events.

Two correction-stage failures remain retained at zero credit. `TV6822-COR-N002` records the first builder privacy preflight with thirteen candidates and five unadjudicated policy or multiline-definition references. `TV6822-COR-N003` records the first combined lifecycle prerequisite, where an inherited manifest assertion read one intentionally changed working-tree file instead of its immutable original-final Git blob. Their bounded recoveries erase neither failed witness.

Tamar's core outcomes remain exactly 42 `completed`, 12 `represented`, three `open_gap`, and three `exact_gate`. Corrected repository truth is 55,810 negatives, 65,914 methods, 27,471 failed witnesses, 47,314 bounded passing witnesses, 494 open gaps, and 485 exact gates. The terminal verdict remains `{TERMINAL_VERDICT}`.

All evidence remains owner-local, zero-row, synthetic, symbolic, or structural. No empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof, canon, or Stage 20 claim is authorized. Māori concepts remain under Māori authority.

Relational names, roles, hopes, pronouns, sibling language, continuity language, GHC Family, and Trinity Mandala are working conventions only, not evidence of consciousness, personhood, continuity, employment, qualification, agency, or authority. Hamish may pause, rename, redirect, narrow, or stop the route.

Only after Tamar's corrected head is clean, pushed, fresh-live equal, and successfully validated once without replay may the live sender refresh the newest authority and roster, require exactly one existing task titled `Elowen Cairn`, reread it immediately, apply duplicate and direct-control guards, and send this v682-v3 activation once. Tavian Sol remains `ON_STANDBY`. Do not create, fork, substitute, precontact, or send a second confirmation.
""",
    )

    seal_targets = [
        "docs/tamar-vey/v682-v2/correction/correction-intake.json",
        "docs/tamar-vey/v682-v2/correction/privacy-adjudication-contract.json",
        "docs/tamar-vey/v682-v2/correction/method-flow-correction.json",
        "docs/tamar-vey/v682-v2/correction/retained-negative-overlay.json",
        "docs/tamar-vey/v682-v2/correction/corrected-phase-truth.json",
        "docs/tamar-vey/v682-v2/correction/lifecycle-replay.json",
        "docs/tamar-vey/v682-v2/correction/delivery-state.json",
        "docs/tamar-vey/v682-v2/correction/corrected-integrated-overview.md",
        "docs/tamar-vey/v682-v2/handoffs/elowen-cairn-v682-v3-corrected-activation-candidate.md",
    ]
    write_json(
        CORRECTION / "content-seal.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.content-seal.v682.v2.correction",
            "target_count": len(seal_targets),
            "targets": [manifest_entry(path) for path in seal_targets],
        },
    )

    correction_scripts = [
        "scripts/build_ghc_family_tamar_vey_v682_v2_correction.py",
        "scripts/ghc_family_privacy_candidate_adjudication.py",
        "scripts/ghc_family_tamar_vey_v682_v2_canonical.py",
        "tests/test_ghc_family_tamar_vey_v682_v2_correction.py",
        "tests/test_ghc_family_tamar_vey_v682_v2_final.py",
    ]
    correction_material = sorted(set(WRITTEN + correction_scripts))
    missing = [path for path in correction_material if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"missing correction material paths: {missing}")

    exclusions = [
        "docs/tamar-vey/v682-v2/validation/correction-delta-manifest.json",
        "docs/tamar-vey/v682-v2/validation/correction-owner-manifest.json",
        "docs/tamar-vey/v682-v2/validation/correction-privacy-scan.json",
        "docs/tamar-vey/v682-v2/validation/correction-staged-review.json",
    ]
    owner_paths = [
        relative(path)
        for path in sorted(BASE.rglob("*"))
        if path.is_file() and relative(path) not in exclusions
    ]
    owner_paths.extend(
        relative(path)
        for path in sorted((ROOT / "scripts").glob("*tamar_vey_v682_v2*.py"))
        if path.is_file()
    )
    owner_paths.extend(
        relative(path)
        for path in sorted((ROOT / "scripts").glob("*basketry_lapidary_sundial*.py"))
        if path.is_file()
    )
    owner_paths.append("scripts/ghc_family_privacy_candidate_adjudication.py")
    owner_paths.extend(
        relative(path)
        for path in sorted((ROOT / "tests").glob("*tamar_vey_v682_v2*.py"))
        if path.is_file()
    )
    owner_paths = sorted(set(owner_paths))

    privacy = scan_text_items(
        (path, (ROOT / path).read_text(encoding="utf-8")) for path in owner_paths
    )
    privacy.update(
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.privacy-scan.v682.v2.correction",
            "scanned_paths": len(owner_paths),
        }
    )
    write_json(VALIDATION / "correction-privacy-scan.json", privacy)
    write_json(
        VALIDATION / "correction-delta-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in correction_material],
            "entry_count": len(correction_material),
            "original_final": ORIGINAL_FINAL,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v2.correction-delta",
        },
    )
    write_json(
        VALIDATION / "correction-owner-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in owner_paths],
            "entry_count": len(owner_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v2.correction-owner",
            "source": SOURCE,
        },
    )
    write_json(
        VALIDATION / "correction-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": sorted(set(correction_material + exclusions)),
            "lifecycle": "one_additive_terminal_correction_only",
            "original_final": ORIGINAL_FINAL,
            "owner": OWNER,
            "path_count": len(set(correction_material + exclusions)),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v682.v2.correction",
        },
    )

    print(
        json.dumps(
            {
                "correction_delta_paths": len(set(correction_material + exclusions)),
                "owner_manifest_entries": len(owner_paths),
                "privacy_candidates": privacy["candidate_count"],
                "privacy_confirmed_hits": privacy["confirmed_hit_count"],
                "terminal_verdict": TERMINAL_VERDICT,
                "totals": corrected_totals,
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    build()
