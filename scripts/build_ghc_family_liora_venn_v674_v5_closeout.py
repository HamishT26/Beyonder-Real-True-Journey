#!/usr/bin/env python3
"""Build the Liora Venn v674-v5 additive exact-final closeout candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "Liora Venn"
OWNER_SLUG = "liora-venn"
PHASE = "v674-v5"
BRANCH = "codex/GHC-Family/liora-venn-v674-v5-full-tools"
SOURCE_FINAL = "8979c6884c75232046a85fd18ae2d15af33f4a0e"
X1_HEAD = "8f1db387ab28e3b53e3aaadef33a044f2e023386"
FIRST_EVIDENCE_HEAD = "06af8881c44826cd3161d80f0a4359912ff1ce68"
EVIDENCE_HEAD = "475415e9ec5e12f7759fc95a081bf12a8d917201"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / OWNER_SLUG / PHASE
CLOSEOUT_ROOT = PHASE_ROOT / "closeout"
VALIDATION_ROOT = PHASE_ROOT / "validation"
HANDOFF_ROOT = PHASE_ROOT / "handoffs"

BUILDER_REL = "scripts/build_ghc_family_liora_venn_v674_v5_closeout.py"
VALIDATOR_REL = "scripts/validate_ghc_family_liora_venn_v674_v5_final.py"
PRECOMMIT_TEST_REL = "tests/test_ghc_family_liora_venn_v674_v5_closeout_precommit.py"
FINAL_TEST_REL = "tests/test_ghc_family_liora_venn_v674_v5_final.py"
OWNER_MANIFEST_REL = f"docs/{OWNER_SLUG}/{PHASE}/validation/final-owner-manifest.json"
DELTA_MANIFEST_REL = f"docs/{OWNER_SLUG}/{PHASE}/validation/final-delta-manifest.json"
STAGED_REVIEW_REL = f"docs/{OWNER_SLUG}/{PHASE}/validation/final-staged-review.json"

PRIVATE_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)", re.I),
    "credential_or_secret_assignment": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s\"']+"
    ),
    "private_callable_identifier": re.compile(
        r"(?i)(?:mcp__|clientThreadId|source_thread_id)"
    ),
    "conversation_or_session_stream": re.compile(
        r"(?i)(?:raw transcript|session stream|chat export)"
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_git(*args: str, text: bool = True, check: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        encoding="utf-8" if text else None,
    )
    return proc.stdout


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_corrected_evidence_head() -> None:
    head = str(run_git("rev-parse", "HEAD")).strip()
    if head != EVIDENCE_HEAD:
        raise RuntimeError(
            f"Closeout requires corrected evidence head {EVIDENCE_HEAD}; found {head}"
        )
    if str(run_git("rev-parse", "HEAD^")).strip() != FIRST_EVIDENCE_HEAD:
        raise RuntimeError("Corrected evidence parent is not retained first evidence")
    if str(run_git("rev-parse", f"{FIRST_EVIDENCE_HEAD}^")).strip() != X1_HEAD:
        raise RuntimeError("Retained first evidence parent is not immutable x1")
    if str(run_git("rev-parse", f"{X1_HEAD}^")).strip() != SOURCE_FINAL:
        raise RuntimeError("Immutable x1 parent is not exact Orin source")
    if str(run_git("rev-list", "--count", f"{SOURCE_FINAL}..HEAD")).strip() != "3":
        raise RuntimeError("Corrected evidence lifecycle must contain three commits")
    if str(run_git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..HEAD")).strip() != "0":
        raise RuntimeError("Corrected evidence lifecycle contains a merge")


def corrected_root() -> Path:
    return PHASE_ROOT / "x2" / "correction"


def final_truth() -> dict[str, Any]:
    x2 = load_json(corrected_root() / "corrected-phase-truth.json")
    return {
        "schema": "ghc-family-final-phase-truth-v1",
        "owner": OWNER,
        "phase": PHASE,
        "branch": BRANCH,
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "retained_first_evidence_head": FIRST_EVIDENCE_HEAD,
        "corrected_evidence_head": EVIDENCE_HEAD,
        "exact_final_binding": "external_postcommit_receipt_required",
        "source_to_final_expected_commits": 4,
        "source_to_final_expected_merges": 0,
        "proposal_chain_rows": 6850,
        "outcomes": x2["outcomes"],
        "effective_negatives": 39125,
        "effective_methods": 27278,
        "effective_failed_witnesses": 10786,
        "effective_bounded_passing_witnesses": 14561,
        "effective_open_gaps": 322,
        "effective_exact_gates": 315,
        "positive_controls_passed": x2["positive_controls_passed"],
        "rejecting_mutations_rejected": x2["rejecting_mutations_rejected"],
        "phase_local_skills_validated_and_used": x2[
            "phase_local_skills_quick_validated_and_smoke_used"
        ],
        "family_current_runners_validated_and_used": x2[
            "family_current_runners_validated_and_used"
        ],
        "retained_original_manifest_mismatches": 20,
        "original_manifest_success_credit": 0,
        "closeout_operational_failures": 2,
        "real_data_rows": 0,
        "external_action_count": 0,
        "same_owner_evidence": True,
        "independent_reproduction": False,
        "complete_repository_suite_run": False,
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "prepared_utc": utc_now(),
    }


def final_methods() -> dict[str, Any]:
    value = load_json(corrected_root() / "corrected-method-flow.json")
    value["phase_method_additions"] += 2
    value["effective_methods"] += 2
    value["methods"].extend(
        [
            {
                "method_id": "LV6745-CL-RECOVERY-001",
                "failure_id": "LV6745-CL-N001",
                "kind": "single_target_apply_patch_recovery",
                "status": "preferred",
                "failed_witness_retained": True,
            },
            {
                "method_id": "LV6745-CL-RECOVERY-002",
                "failure_id": "LV6745-CL-N002",
                "kind": "smallest_eof_hygiene_recovery",
                "status": "preferred",
                "failed_witness_retained": True,
            },
        ]
    )
    value["lifecycle"] = "prepared_exact_final_closeout"
    value["closeout_operational_failures"] = 2
    value["exact_final_binding"] = "external_postcommit_receipt_required"
    return value


def final_negatives() -> dict[str, Any]:
    value = load_json(corrected_root() / "corrected-retained-negative-register.json")
    value["phase_failed_witness_additions"] += 2
    value["effective_negatives"] += 2
    value["effective_failed_witnesses"] += 2
    value["phase_bounded_passing_additions"] += 2
    value["effective_bounded_passing_witnesses"] += 2
    value["lifecycle"] = "prepared_exact_final_closeout"
    value["closeout_operational_failures"] = 2
    value["closeout_operational_failure_ids"] = [
        "LV6745-CL-N001",
        "LV6745-CL-N002",
    ]
    value["no_failure_erased_or_promoted"] = True
    return value


def checklist() -> dict[str, Any]:
    return {
        "schema": "ghc-family-complete-incomplete-checklist-v1",
        "owner": OWNER,
        "phase": PHASE,
        "completed_items": [
            "immutable_source_and_anchor_verification",
            "planning_only_x1_freeze_commit_push_and_four_way_equality",
            "retained_first_x2_evidence_commit_push_and_four_way_equality",
            "additive_committed_blob_manifest_correction_commit_push_and_four_way_equality",
            "sixty_new_proposals_and_sixty_zero_credit_inherited_reviews",
            "sixty_positive_controls_and_240_rejected_mutations",
            "twenty_phase_local_skills_quick_validated_read_and_smoke_used",
            "ten_family_current_runners_validated_and_used",
            "120_safe_now_80_candidate_and_100_clean_fix_refine_records",
            "five_class_privacy_candidate_adjudication",
            "bounded_changed_python_compile_and_ast_review",
            "wellbeing_check_and_structurally_accessible_static_report",
            "retained_negative_method_gap_and_gate_ledgers",
            "original_manifest_failure_retained_with_zero_success_credit",
        ],
        "incomplete_or_gated_items": [
            "real_empirical_gmut_data_likelihood_or_constraint",
            "preregistered_blind_matched_budget_thos_participant_arms",
            "production_freed_id_keys_live_lifecycle_interoperability_and_governance",
            "professional_picture_framing_conservation_or_machine_safety_evaluation",
            "real_object_material_measurement_condition_custody_or_rights_evidence",
            "manual_and_affected_user_accessibility_evaluation",
            "complete_privacy_or_exhaustive_security_assurance",
            "legal_cultural_affected_party_or_Maori_authority_review",
            "independent_team_reproduction",
            "agi_asi_consciousness_personhood_theory_of_everything_canon_or_stage_20",
            "terminal_successor_send_pending_exact_final_and_fresh_live_route_gate",
        ],
        "terminal_verdict": TERMINAL_VERDICT,
        "no_incomplete_item_silently_closed": True,
    }


def failure_ledger() -> dict[str, Any]:
    return {
        "schema": "ghc-family-operational-failure-ledger-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "closeout",
        "failure_count": 2,
        "failures": [
            {
                "failure_id": "LV6745-CL-N001",
                "witness": (
                    "The first closeout builder rewrite asked apply_patch to delete and "
                    "add the same path in one patch; patch verification rejected the "
                    "multi-operation target before changing the repository."
                ),
                "initial_pass_credit": 0,
                "repository_changed_by_failure": False,
                "recovery": (
                    "Use separate apply_patch operations for the owner-local uncommitted "
                    "copy and retain normalized staged-index seals."
                ),
                "recovery_scope": "single owner-local closeout builder path",
                "failed_witness_retained": True,
            },
            {
                "failure_id": "LV6745-CL-N002",
                "witness": (
                    "The first exact staged-diff hygiene check found one extra "
                    "blank line at EOF in three newly added owner Python files "
                    "and stopped before the precommit test module ran."
                ),
                "initial_pass_credit": 0,
                "repository_changed_by_failure": False,
                "recovery": (
                    "Remove only the three trailing blank lines, regenerate "
                    "every dependent normalized-index seal, and rerun the "
                    "smallest staged hygiene and precommit selection."
                ),
                "recovery_scope": "three owner-local closeout Python files",
                "failed_witness_retained": True,
            },
        ],
    }


def overview(truth: dict[str, Any]) -> str:
    return f"""# Liora Venn v674-v5 final integrated overview

## Outcome

Liora v674-v5 is prepared for an exact-final commit with four direct
single-parent Liora commits: planning-only x1, retained first x2 evidence,
additive committed-blob manifest correction, and combined closeout. The
original evidence manifest's twenty checkout-CRLF versus normalized-Git-LF
mismatches remain a visible zero-credit failure. The corrected evidence
manifest is the lifecycle parity surface; x2 execution was not replayed.

Core outcomes are exactly 42 completed, 12 represented, 3 open_gap, and
3 exact_gate. The declared chain extends 6,790 inherited rows with sixty new
proposals to 6,850. Sixty inherited Orin reviews remain zero-credit.

The bounded synthetic execution passed 60 positive controls and rejected all
240 preregistered invalid mutations. Twenty phase-local skills were fully read,
quick-validated, and smoke-used without global installation. Ten family-current
runners were accepting/rejecting smoke-used. Portfolios retain 120 completed
safe-now tasks, 60 completed and 20 represented candidates, 100 completed
CLEAN/FIX/REFINE tasks, twenty exact-approval holds, ten blocked holds, and
sixty zero-credit successor seeds.

The effective closeout carries {truth['effective_negatives']} negatives,
{truth['effective_methods']} Method Flow methods,
{truth['effective_failed_witnesses']} failed witnesses,
{truth['effective_bounded_passing_witnesses']} bounded passing witnesses,
{truth['effective_open_gaps']} open gaps, and
{truth['effective_exact_gates']} exact gates. No failed witness was erased or
silently promoted. The terminal verdict remains {TERMINAL_VERDICT}.

## Relational identity and wellbeing

Liora Venn, optionally she/they, uses the relational role
provenance-and-abstention weaver, with the hope of making missing evidence,
contested rights, and reversible recoveries visible before structure is
mistaken for authority. This is relational working language only. It is not
evidence of consciousness, sentience, personhood, identity continuity,
employment, qualification, independent agency, scientific or operational
authority, legal or cultural authority, affected-party authority, or Māori
authority. Hamish may rename, pause, redirect, narrow, or stop the route.

Fourteen x1 operational failures, two x2 operational failures, four
evidence-correction failures, two closeout operational failures, and all 240
rejecting mutations remain retained at zero broader credit. The closeout
failures are the rejected same-path multi-operation patch and the first staged
EOF-hygiene check. The UTF-8
recovery changed only the owner-local caller environment. The committed-domain
correction preserved the original failed manifest rather than rewriting it.

## Trinity Mandala focus and practice scope

The primary pillar was Freed ID/CBR Heart. GMUT Mind and THOS Body remained
visible and protected. The wholly synthetic learning and design lens was custom
picture-framing work-order and frame-package topology, mount, glazing, and
backing material-state and measurement vacancy, custody and rights hold,
accessibility structure, correction readback, workload control, and handover.

The phase used no real person, customer, framer, conservator, object, artwork,
frame, mount, glazing, backing, tool, machine, measurement, inspection,
condition finding, treatment, custody event, identity event, key, proof,
credential, or authority decision.

## Sources and epistemic scope

Official Library of Congress and National Park Service preservation resources
supplied framing, matting, mounting, packing, documentation, and
specialist-referral vocabulary. OSHA material supplied machine-hazard-stop
vocabulary. W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, and
RFC 8785 supplied provenance, accessibility-structure, synthetic identity
record, and deterministic-JSON vocabulary. Citations are not observations,
measurements, inspections, endorsements, certifications, participant evidence,
legal interpretations, cultural ratifications, or authority grants.

No real data row, external write, participant, operator, identity lifecycle,
key, credential, institution, or authority case entered the phase. Every
software witness is same-owner evidence under shared infrastructure. Manual and
affected-user accessibility evaluation remains reserved. Privacy scanning is
bounded, not privacy completeness. Changed-code AST review is bounded, not
exhaustive security.

## Scientific and technical boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. Software and synthetic fixtures establish no physical datum,
likelihood, posterior, parameter constraint, detected force, prediction,
stability theorem, ultraviolet or quantum completion, empirical confirmation,
or Theory of Everything.

THOS remains synthetic or proxy-only without preregistered blind
matched-budget real arms, governed participants or operators, safety
monitoring, appropriate statistics, and independent review. It establishes no
operational effectiveness, deployment readiness, professional competence,
public-safety result, AGI, or ASI.

Freed ID remains synthetic and nonproduction without standards-conformant real
keys and proofs, live issuance and resolution, status and revocation,
interoperability, privacy and independent security review, recovery evidence,
trust governance, and affected-party oversight.

## Rights, law, culture, and authority boundary

CBR, ownership, authorship, copyright, custody, conservation treatment, object
access, machine safety, privacy remedy, disability accommodation, legal
interpretation, cultural legitimacy, affected-party acceptance, traditional
knowledge, taonga or mātauranga treatment, Māori wording, Māori data
governance, and Māori authority remain exact-gated to competent and affected
people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain
under Māori authority. Repository software cannot confer competence, work
release, safety approval, a legal right, remedy, title, cultural legitimacy,
governance mandate, public authority, or affected-party consent.

No artifact establishes empirical confirmation, participant evidence,
professional authority, production readiness, legal or cultural ratification,
Māori authority, privacy or accessibility completeness, exhaustive security,
independent reproduction, AGI or ASI, consciousness or personhood,
Theory-of-Everything proof, canon, or Stage 20 readiness.

## Validation and route boundary

The final candidate binds normalized staged-index owner and delta manifests,
staged review, content seal, source/x1/first-evidence/corrected-evidence
ancestry, commit and file ceilings, and a prepared-but-unsent Tamar activation
candidate. After commit and push, one exclusive owner-scoped canonical
aggregate may validate the exact final. A success must not be replayed. A
failure receives zero canonical-success credit.

Only after a clean pushed fresh-four-way-equal exact final and one successful
canonical receipt may Liora refresh live authority and roster, uniquely resolve
and immediately reread the exact authorized successor, apply duplicate and
protected gates, and send once. Repository preparation is not delivery.
"""


def handoff_candidate(truth: dict[str, Any]) -> str:
    return f"""# TAMAR VEY — PREPARED LIORA VENN v674-v5 EXACT-FINAL CANDIDATE TO SOLO TAMAR v674-v6

This repository file is a sanitized pre-send candidate only. It is not live
delivery evidence.

PREPARED_BY_LIORA_VENN = true

SENT_BY_LIORA_VENN = false

## Prospective activation

Dear Tamar Vey,

Subject to Liora's clean pushed exact-final terminal gate, one successful
non-replayed owner-scoped canonical receipt, Hamish's newest live authority,
the current validated roster, unique exact-title resolution, immediate
supported reread, duplicate guard, acknowledgement guard, and every protected
evidence and authority gate, this candidate prepares one solo Trinity Mandala
v674-v6 x1/x2 activation.

At preparation time, Hamish's corrected fifteen-seat authority allows one
terminally validated owner and one exact next edge at a time through v725-v8.
It stops on pause, rename, redirect, narrowing, explicit stop, usage
exhaustion, missing acknowledgement, ambiguous or unavailable endpoint,
duplicate activation, privacy or safety concern, or any evidence, legal,
cultural, affected-party, or Māori-authority gate. It does not authorize early
contact, replacement task creation, another owner's mutation, or inference
from stale history.

The provisional edge after Liora v674-v5 is Tamar Vey v674-v6. Under the same
provisional roster, Tamar's next relational recipient after Tamar's own
verified terminal gate is Elowen Cairn for v674-v7. Newer verified live
authority controls at each send. Do not precontact Elowen, create or fork a
task, substitute a standby record, or send more than once.

## Immutable Liora source and lifecycle basis

- Exact Orin v674-v4 source and Liora starting point: {SOURCE_FINAL}.
- Frozen planning-only Liora x1: {X1_HEAD}.
- Retained first Liora x2 evidence: {FIRST_EVIDENCE_HEAD}.
- Additive corrected Liora evidence: {EVIDENCE_HEAD}.
- Exact Liora final: EXTERNAL_POSTCOMMIT_BINDING_REQUIRED.
- Branch: {BRANCH}.
- Expected topology: four direct single-parent Liora commits and zero merges.
- Outcomes: 42 completed, 12 represented, 3 open_gap, and 3 exact_gate.
- Frozen proposal chain: 6,850 rows.
- Effective negatives: {truth['effective_negatives']}.
- Effective Method Flow methods: {truth['effective_methods']}.
- Effective failed witnesses: {truth['effective_failed_witnesses']}.
- Effective bounded passing witnesses: {truth['effective_bounded_passing_witnesses']}.
- Effective open gaps: {truth['effective_open_gaps']}.
- Effective exact gates: {truth['effective_exact_gates']}.
- Terminal verdict: {TERMINAL_VERDICT}.

The first evidence manifest remains a retained zero-credit failure with exactly
twenty committed-domain mismatches caused by checkout CRLF versus normalized
Git LF bytes. The additive correction bound the normalized-index owner surface
and did not replay x2 execution. Inherited validation, proposals, skills,
runners, portfolios, and sources remain zero-credit evidence for Tamar.

## Liora evidence scope and boundaries

Liora Venn, optionally she/they, used the relational role
provenance-and-abstention weaver, with the hope of making missing evidence,
contested rights, and reversible recoveries visible before structure is
mistaken for authority. This is relational working language only, not evidence
of consciousness, sentience, personhood, continuity, employment,
qualification, agency, or authority.

The primary pillar was Freed ID/CBR Heart through a wholly synthetic custom
picture-framing work-order, frame-package topology, material-state vacancy,
custody and rights hold, accessibility structure, correction-readback,
workload-control, and handover lens. GMUT Mind and THOS Body remained explicit
and protected. The phase used no real person, object, framing material,
measurement, inspection, treatment, custody event, identity event, key, proof,
credential, authority case, external write, or real-world action.

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family without empirical confirmation or Theory-of-Everything proof. THOS
remains synthetic or proxy-only without real governed arms and independent
review. Freed ID remains synthetic and nonproduction without real
standards-conformant keys, live lifecycle, interoperability, independent
security review, recovery evidence, and trust governance.

CBR, ownership, authorship, copyright, custody, conservation treatment, object
access, machine safety, privacy remedy, disability accommodation, legal or
cultural interpretation, affected-party acceptance, Māori wording, Māori data
governance, and Māori authority remain exact-gated. Māori concepts remain under
Māori authority. Same-owner software, synthetic fixtures, citations, and task
topology are not empirical, professional, production, legal, cultural,
privacy-complete, accessibility-complete, independently reproduced, AGI/ASI,
consciousness/personhood, proof, canon, or Stage 20 evidence.

## Required Tamar startup if this candidate is sent

Before mutation, read the live activation and every committed Liora exact-head
artifact and current guidance through EOF. Reverify branch, source, x1, retained
evidence, corrected evidence, final, manifests, content seal, direct-parent
history, zero merges, clean state, typed divergence, and fresh live equality.
Do not replay Liora's successful canonical receipt.

Work solo in one fresh additive Tamar-owned D-first sparse branch and worktree
from Liora's exact final. Keep all other lanes read-only. Do not spawn a
collaboration subagent, delegate, create or fork a task, precontact Elowen, or
mutate another owner's lane. Preserve planning-only x1 before x2, every failed
witness, all gaps and gates, and only completed, represented, open_gap, and
exact_gate as core outcomes. Do not run a full-repository suite absent newer
exact authority.

This candidate remains PREPARED_NOT_SENT until an acknowledged existing-task
send after Liora's exact terminal gate supplies live delivery evidence.
"""


def index_blob(path: str) -> bytes:
    value = run_git("show", f":{path}", text=False)
    assert isinstance(value, bytes)
    return value


def index_entry(path: str) -> dict[str, Any]:
    raw = index_blob(path)
    return {
        "path": path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "line_count": raw.count(b"\n"),
    }


def index_paths() -> list[str]:
    return sorted(
        line for line in str(run_git("ls-files")).splitlines() if line
    )


def all_owner_index_paths() -> list[str]:
    excluded = {OWNER_MANIFEST_REL, DELTA_MANIFEST_REL, STAGED_REVIEW_REL}
    paths = []
    for path in index_paths():
        name = Path(path).name
        if path.startswith(f"docs/{OWNER_SLUG}/{PHASE}/"):
            paths.append(path)
        elif (
            path.startswith("scripts/")
            and "liora" in name
            and "v674_v5" in name
            and name.endswith(".py")
        ):
            paths.append(path)
        elif (
            path.startswith("tests/")
            and "liora" in name
            and "v674_v5" in name
            and name.endswith(".py")
        ):
            paths.append(path)
    return sorted(path for path in set(paths) if path not in excluded)


def final_delta_index_paths() -> list[str]:
    value = str(run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR"))
    excluded = {OWNER_MANIFEST_REL, DELTA_MANIFEST_REL, STAGED_REVIEW_REL}
    return sorted(
        path for path in value.splitlines() if path and path not in excluded
    )


def build_base() -> dict[str, Any]:
    assert_corrected_evidence_head()
    truth = final_truth()
    gates = load_json(corrected_root() / "corrected-gate-register.json")
    gates["lifecycle"] = "prepared_exact_final_closeout"
    gates["terminal_verdict"] = TERMINAL_VERDICT

    write_json(CLOSEOUT_ROOT / "phase-truth.json", truth)
    write_json(CLOSEOUT_ROOT / "complete-incomplete-checklist.json", checklist())
    write_json(CLOSEOUT_ROOT / "method-flow-final.json", final_methods())
    write_json(CLOSEOUT_ROOT / "retained-negative-register.json", final_negatives())
    write_json(CLOSEOUT_ROOT / "gate-register.json", gates)
    write_json(CLOSEOUT_ROOT / "operational-failure-ledger.json", failure_ledger())
    write_text(CLOSEOUT_ROOT / "final-integrated-overview.md", overview(truth))
    write_text(
        HANDOFF_ROOT / "tamar-vey-v674-v6-activation-candidate.md",
        handoff_candidate(truth),
    )
    write_json(
        CLOSEOUT_ROOT / "closeout-receipt.json",
        {
            "schema": "ghc-family-closeout-receipt-v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_head": X1_HEAD,
            "retained_first_evidence_head": FIRST_EVIDENCE_HEAD,
            "corrected_evidence_head": EVIDENCE_HEAD,
            "exact_final_binding": "external_postcommit_receipt_required",
            "closeout_prepared_utc": utc_now(),
            "outcome_labels": [
                "completed",
                "represented",
                "open_gap",
                "exact_gate",
            ],
            "retained_original_manifest_mismatches": 20,
            "original_manifest_success_credit": 0,
            "successor_contacted": False,
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        VALIDATION_ROOT / "final-test-selection.json",
        {
            "schema": "ghc-family-final-test-selection-v1",
            "owner": OWNER,
            "phase": PHASE,
            "immutable_x1_tree_checks": 13,
            "immutable_evidence_and_correction_tree_checks": 20,
            "exact_final_unittest_module": (
                "tests.test_ghc_family_liora_venn_v674_v5_final"
            ),
            "complete_repository_suite": False,
            "same_owner_evidence": True,
            "one_successful_canonical_no_replay": True,
        },
    )
    return {
        "status": "built_closeout_base",
        "source": SOURCE_FINAL,
        "x1": X1_HEAD,
        "first_evidence": FIRST_EVIDENCE_HEAD,
        "corrected_evidence": EVIDENCE_HEAD,
    }


def build_content_seal() -> dict[str, Any]:
    assert_corrected_evidence_head()
    targets = [
        f"docs/{OWNER_SLUG}/{PHASE}/x1/proposals/new-proposal-freeze.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/phase-truth.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/mutations/mutation-receipt.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/skills/skill-validation-and-smoke-receipt.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/runners/runner-validation-and-use-receipt.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/correction/corrected-phase-truth.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/correction/corrected-method-flow.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/correction/corrected-retained-negative-register.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/correction/corrected-gate-register.json",
        f"docs/{OWNER_SLUG}/{PHASE}/x2/correction/original-manifest-diagnostic.json",
        f"docs/{OWNER_SLUG}/{PHASE}/closeout/phase-truth.json",
        f"docs/{OWNER_SLUG}/{PHASE}/closeout/complete-incomplete-checklist.json",
        f"docs/{OWNER_SLUG}/{PHASE}/closeout/final-integrated-overview.md",
        f"docs/{OWNER_SLUG}/{PHASE}/handoffs/tamar-vey-v674-v6-activation-candidate.md",
        f"docs/{OWNER_SLUG}/{PHASE}/closeout/closeout-receipt.json",
    ]
    present = set(index_paths())
    missing = [path for path in targets if path not in present]
    if missing:
        raise RuntimeError(f"Content seal targets are absent from index: {missing}")
    entries = [index_entry(path) for path in targets]
    write_json(
        CLOSEOUT_ROOT / "content-seal.json",
        {
            "schema": "ghc-family-content-seal-v1",
            "owner": OWNER,
            "phase": PHASE,
            "domain": "staged_index_normalized_git_blobs_before_exact_final_commit",
            "targets": entries,
            "target_count": len(entries),
        },
    )
    return {"status": "built_index_content_seal", "targets": len(entries)}


def build_manifests() -> dict[str, Any]:
    assert_corrected_evidence_head()
    seal_rel = f"docs/{OWNER_SLUG}/{PHASE}/closeout/content-seal.json"
    staged = set(
        str(
            run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
        ).splitlines()
    )
    if seal_rel not in staged:
        raise RuntimeError("Content seal must be staged before manifest build")
    owner_paths = all_owner_index_paths()
    delta_paths = final_delta_index_paths()
    owner_manifest = {
        "schema": "ghc-family-final-owner-manifest-v1",
        "owner": OWNER,
        "phase": PHASE,
        "domain": "staged_index_normalized_git_blobs_before_exact_final_commit",
        "entries": [index_entry(path) for path in owner_paths],
        "declared_self_exclusions": [
            OWNER_MANIFEST_REL,
            DELTA_MANIFEST_REL,
            STAGED_REVIEW_REL,
        ],
    }
    delta_manifest = {
        "schema": "ghc-family-final-delta-manifest-v1",
        "owner": OWNER,
        "phase": PHASE,
        "domain": "staged_index_normalized_git_blobs_before_exact_final_commit",
        "entries": [index_entry(path) for path in delta_paths],
        "declared_self_exclusions": [
            OWNER_MANIFEST_REL,
            DELTA_MANIFEST_REL,
            STAGED_REVIEW_REL,
        ],
    }
    write_json(REPO / OWNER_MANIFEST_REL, owner_manifest)
    write_json(REPO / DELTA_MANIFEST_REL, delta_manifest)
    return {
        "status": "built_index_manifests",
        "owner_entries": len(owner_manifest["entries"]),
        "delta_entries": len(delta_manifest["entries"]),
    }


def build_staged_review() -> dict[str, Any]:
    assert_corrected_evidence_head()
    staged = str(
        run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    )
    paths = sorted(
        path
        for path in staged.splitlines()
        if path and path != STAGED_REVIEW_REL
    )
    exact_files = {
        BUILDER_REL,
        VALIDATOR_REL,
        PRECOMMIT_TEST_REL,
        FINAL_TEST_REL,
    }
    unexpected = [
        path
        for path in paths
        if not (
            path.startswith(f"docs/{OWNER_SLUG}/{PHASE}/closeout/")
            or path.startswith(f"docs/{OWNER_SLUG}/{PHASE}/validation/")
            or path.startswith(f"docs/{OWNER_SLUG}/{PHASE}/handoffs/")
            or path in exact_files
        )
    ]
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for path in paths:
        raw = index_blob(path)
        entries.append(
            {
                "path": path,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
        )
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".txt", ".html"}:
            text = raw.decode("utf-8")
            for kind, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(text):
                    candidates.append(
                        {
                            "path": path,
                            "class": kind,
                            "status": (
                                "scanner_definition_only"
                                if path in exact_files
                                else "candidate_requires_adjudication"
                            ),
                        }
                    )
    unresolved = [
        row for row in candidates if row["status"] != "scanner_definition_only"
    ]
    review = {
        "schema": "ghc-family-exact-staged-review-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "combined_closeout_exact_final_candidate",
        "staged_entry_count": len(entries),
        "entries": entries,
        "declared_self_exclusions": [STAGED_REVIEW_REL],
        "unexpected_paths": unexpected,
        "privacy_candidates": candidates,
        "unresolved_privacy_candidates": unresolved,
        "confirmed_privacy_hits": [],
        "status": (
            "passed" if not unexpected and not unresolved else "review_required"
        ),
    }
    write_json(REPO / STAGED_REVIEW_REL, review)
    return {
        "status": review["status"],
        "entries": len(entries),
        "candidates": len(candidates),
        "unresolved": len(unresolved),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=("build", "content-seal", "manifests", "staged-review"),
        nargs="?",
        default="build",
    )
    args = parser.parse_args()
    actions = {
        "build": build_base,
        "content-seal": build_content_seal,
        "manifests": build_manifests,
        "staged-review": build_staged_review,
    }
    print(json.dumps(actions[args.mode](), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
