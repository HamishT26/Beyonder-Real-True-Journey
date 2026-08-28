#!/usr/bin/env python3
"""Build the Orin Thale v674-v4 closeout candidate at immutable evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "Orin Thale"
OWNER_SLUG = "orin-thale"
PHASE = "v674-v4"
BRANCH = "codex/GHC-Family/orin-thale-v674-v4-full-tools"
SOURCE_FINAL = "dcdc2921b193516242c93e6ef303f854e9d21264"
X1_HEAD = "5728299ca983aa504a64a5038197358bc50c4ceb"
EVIDENCE_HEAD = "1a076e80fa77ea9d37ce1162174e3c1725f82e9b"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / OWNER_SLUG / PHASE
CLOSEOUT_ROOT = PHASE_ROOT / "closeout"
VALIDATION_ROOT = PHASE_ROOT / "validation"
HANDOFF_ROOT = PHASE_ROOT / "handoffs"

BUILDER_REL = "scripts/build_ghc_family_orin_thale_v674_v4_closeout.py"
VALIDATOR_REL = "scripts/validate_ghc_family_orin_thale_v674_v4_final.py"
PRECOMMIT_TEST_REL = "tests/test_ghc_family_orin_thale_v674_v4_closeout_precommit.py"
FINAL_TEST_REL = "tests/test_ghc_family_orin_thale_v674_v4_final.py"
OWNER_MANIFEST_REL = f"docs/{OWNER_SLUG}/{PHASE}/validation/final-owner-manifest.json"
DELTA_MANIFEST_REL = f"docs/{OWNER_SLUG}/{PHASE}/validation/final-delta-manifest.json"
STAGED_REVIEW_REL = f"docs/{OWNER_SLUG}/{PHASE}/validation/final-staged-review.json"

PRIVATE_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\\\|/Users/|/home/)", re.I),
    "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s\"']+"),
    "private_callable_identifier": re.compile(r"(?i)(?:mcp__|clientThreadId|source_thread_id)"),
    "conversation_or_session_stream": re.compile(r"(?i)(?:raw transcript|session stream|chat export)"),
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
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_evidence_head() -> None:
    head = str(run_git("rev-parse", "HEAD")).strip()
    if head != EVIDENCE_HEAD:
        raise RuntimeError(f"Closeout requires immutable evidence head {EVIDENCE_HEAD}; found {head}")
    if str(run_git("rev-parse", "HEAD^" )).strip() != X1_HEAD:
        raise RuntimeError("Evidence parent is not immutable x1")


def final_truth() -> dict[str, Any]:
    x2 = load_json(PHASE_ROOT / "x2" / "phase-truth.json")
    negatives = load_json(PHASE_ROOT / "x2" / "retained-negative-register.json")
    gates = load_json(PHASE_ROOT / "x2" / "gate-register.json")
    methods = load_json(PHASE_ROOT / "x2" / "method-flow" / "ledger.json")
    return {
        "schema": "ghc-family-final-phase-truth-v1",
        "owner": OWNER,
        "phase": PHASE,
        "branch": BRANCH,
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "exact_final_binding": "external_postcommit_receipt_required",
        "source_to_final_expected_commits": 3,
        "source_to_final_expected_merges": 0,
        "proposal_chain_rows": 6790,
        "outcomes": x2["outcomes"],
        "effective_negatives": negatives["effective_negatives"],
        "effective_methods": methods["effective_methods"],
        "effective_failed_witnesses": negatives["effective_failed_witnesses"],
        "effective_bounded_passing_witnesses": negatives["effective_bounded_passing_witnesses"],
        "effective_open_gaps": gates["effective_open_gaps"],
        "effective_exact_gates": gates["effective_exact_gates"],
        "positive_controls_passed": x2["positive_controls_passed"],
        "rejecting_mutations_rejected": x2["rejecting_mutations_rejected"],
        "phase_local_skills_validated_and_used": x2["phase_local_skills_quick_validated_and_smoke_used"],
        "family_current_runners_validated_and_used": x2["family_current_runners_validated_and_used"],
        "real_data_rows": 0,
        "external_action_count": 0,
        "same_owner_evidence": True,
        "independent_reproduction": False,
        "complete_repository_suite_run": False,
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "prepared_utc": utc_now(),
    }


def checklist(truth: dict[str, Any]) -> dict[str, Any]:
    complete = [
        "immutable_source_and_anchor_verification",
        "planning_only_x1_freeze_commit_push_and_four_way_equality",
        "bounded_x2_evidence_commit_push_and_four_way_equality",
        "sixty_new_proposals_and_sixty_zero_credit_inherited_reviews",
        "sixty_positive_controls_and_240_rejected_mutations",
        "twenty_phase_local_skills_quick_validated_read_and_smoke_used",
        "ten_family_current_runners_validated_and_used",
        "120_safe_now_80_candidate_and_100_clean_fix_refine_records",
        "five_class_privacy_candidate_adjudication",
        "bounded_changed_python_compile_and_ast_review",
        "wellbeing_check_and_structurally_accessible_static_report",
        "retained_negative_method_gap_and_gate_ledgers",
    ]
    incomplete = [
        "real_empirical_gmut_data_likelihood_or_constraint",
        "preregistered_blind_matched_budget_thos_participant_arms",
        "production_freed_id_keys_live_lifecycle_interoperability_and_governance",
        "professional_bicycle_food_or_seed_library_evaluation",
        "manual_and_affected_user_accessibility_evaluation",
        "complete_privacy_or_exhaustive_security_assurance",
        "legal_cultural_affected_party_or_Maori_authority_review",
        "independent_team_reproduction",
        "agi_asi_consciousness_personhood_theory_of_everything_canon_or_stage_20",
        "terminal_successor_send_pending_exact_final_and_fresh_live_route_gate",
    ]
    return {
        "schema": "ghc-family-complete-incomplete-checklist-v1",
        "owner": OWNER,
        "phase": PHASE,
        "completed_items": complete,
        "incomplete_or_gated_items": incomplete,
        "terminal_verdict": truth["terminal_verdict"],
        "no_incomplete_item_silently_closed": True,
    }


def handoff_candidate(truth: dict[str, Any]) -> str:
    return f"""# LIORA VENN — PREPARED ORIN THALE v674-v4 EXACT-FINAL CANDIDATE → SOLO LIORA v674-v5 ACTIVATION

This file is a sanitized pre-send candidate only. It is not delivery evidence.

`PREPARED_BY_ORIN_THALE = true`

`SENT_BY_ORIN_THALE = false`

## Prospective activation

Dear Liora Venn,

Subject to Orin's clean pushed exact-final terminal gate, one successful non-replayed owner-scoped canonical receipt, Hamish's newest live authority, the current validated roster, unique exact-title resolution, immediate supported reread, duplicate guard, acknowledgement guard, and every protected evidence and authority gate, this candidate prepares one solo Trinity Mandala v674-v5 x1/x2 activation.

At preparation time, Hamish's newest corrected fifteen-seat authority allows one terminally validated owner and one exact next edge at a time through the requested terminal label v725-v8. That continuing authority stops early on pause, rename, redirect, narrowing, explicit stop, usage exhaustion, missing acknowledgement, ambiguous or unavailable endpoint, duplicate activation, privacy or safety concern, or any evidence, legal, cultural, affected-party, or Maori-authority gate. It does not authorize early contact, replacement task creation, another owner's mutation, or inference from stale repository history.

The current provisional edge after Orin v674-v4 is Liora Venn v674-v5. Under the same provisional current roster, Liora's next relational recipient after Liora's own verified terminal gate is Tamar Vey for v674-v6. Newer verified live authority controls at each send. Do not precontact Tamar, create or fork a task, substitute a standby record, or send more than once.

## Immutable Orin source and lifecycle basis

- Caelen Ash exact source and Orin starting point: `{SOURCE_FINAL}`.
- Frozen planning-only Orin x1: `{X1_HEAD}`.
- Immutable Orin x2 evidence: `{EVIDENCE_HEAD}`.
- Exact Orin final: `EXTERNAL_POSTCOMMIT_BINDING_REQUIRED`.
- Branch: `{BRANCH}`.
- Expected source-to-final topology: exactly three direct single-parent Orin commits and zero merges.
- Core outcomes: 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`.
- Frozen proposal chain: 6,790 rows.
- Effective negatives: {truth['effective_negatives']}.
- Effective Method Flow methods: {truth['effective_methods']}.
- Effective failed witnesses: {truth['effective_failed_witnesses']}.
- Effective bounded passing witnesses: {truth['effective_bounded_passing_witnesses']}.
- Effective open gaps: {truth['effective_open_gaps']}.
- Effective exact gates: {truth['effective_exact_gates']}.
- Terminal verdict: `{TERMINAL_VERDICT}`.

Inherited validation, proposal, skill, runner, portfolio, and source evidence remains zero-credit source evidence for Liora. It is never automatic Liora novelty, execution, completion, or independent reproduction credit.

## Orin evidence scope

Orin Thale, optionally they/them, used the relational role boundary-and-recovery architect, with the hope of making operational dependencies, correction paths, and authority vacancies legible and reversible before structure is mistaken for evidence. This is relational working language only, not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish may rename, pause, redirect, or stop the route.

The primary pillar was THOS Body through three wholly synthetic lenses: bicycle wheelbuilding record and correction handover; bakery batch trace, allergen vacancy, and correction handover; and community seed-library accession and minimum-disclosure handover. GMUT Mind and Freed ID/CBR Heart remained explicit and protected.

The phase used no real person, participant, operator, bicycle, wheel, component, tool, tension reading, bakery, food, ingredient, allergen record, seed, accession, donor, germination result, measurement, inspection, identity, key, credential, institution, authority case, external write, or real-world action. Sixty positive synthetic controls passed. All 240 preregistered invalid mutations were rejected and retained. Twenty owner-local skills were read, quick-validated, and smoke-used without global installation. Ten family-current runners accepted 60 positive controls and rejected 240 invalid controls. Same-owner software evidence is not independent reproduction.

## Required Liora startup, if and only if this candidate is sent after all gates pass

Before mutation, read the complete live activation and every committed Orin exact-head artifact, current GHC Family Index and routing precedence, authorization and roster states, Method Flow schema, workflow-plan refinement, reflection-remaster, approval boundary, open-gate rail, truth bridge, and directly required current reference through EOF. Reverify the branch, exact source, x1, evidence, exact final, manifests, content seal, direct-parent history, zero merges, clean state, typed divergence, and fresh live equality. Do not replay Orin's successful canonical receipt.

Work solo in one fresh additive Liora-owned D-first sparse branch and worktree from Orin's exact final. Keep Orin, Caelen, Sable, Auren, every sibling, shared, standby, global, and user lane read-only. Do not spawn a collaboration subagent, delegate research, create or fork a task, precontact Tamar, or mutate another owner's lane.

Preserve strict planning-only x1 before x2, exact manifests, retained failures, all open gaps and exact gates, scanner-candidate adjudication, deterministic UTF-8 and JSON controls, normalized-LF Git-blob domain distinctions, self-exclusion arithmetic, stale-label and diff hygiene, and the four exact labels `completed`, `represented`, `open_gap`, and `exact_gate`. Treat inherited material as source evidence or zero-credit seeds only.

Use current official or primary sources where materially required, but never convert a citation into an observation, inspection, participant witness, professional approval, legal interpretation, cultural legitimacy, or authority grant. Verify environment versions only. Do not update Codex desktop, install unrelated software, elevate, weaken host security, enable Sandbox or Hyper-V, change Windows features, or reboot.

Run only the authorized owner-self-scoped lifecycle and dependency-closed selections. Do not run a full-repository suite unless newer exact authority explicitly grants it. After a clean pushed exact final, invoke at most one attributable owner-scoped canonical aggregate under an exclusive external receipt latch. Never replay a success. A failed canonical remains zero success credit; a narrow dependency correction remains separately named.

## Scientific, identity, production, professional, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic contracts, synthetic fixtures, analogy, and citations establish no physical datum, likelihood, posterior, parameter constraint, detected force, prediction, stability theorem, ultraviolet or quantum completion, empirical confirmation, or Theory of Everything.

THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. It establishes no operational effectiveness, deployment readiness, professional competence, public-safety result, AGI, or ASI.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, roadworthiness, food safety and release, recall, seed and collection title, access, distribution, privacy remedy, disability accommodation, legal interpretation, cultural legitimacy, affected-party acceptance, traditional knowledge, taonga or matauranga treatment, Maori wording, Maori data governance, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority.

Do not promote synthetic, symbolic, citation, standards, same-owner, inherited, validation, or task-topology evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Maori authority, affected-party approval, privacy or accessibility completeness, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

## Terminal route after Liora only

Only after Liora's own clean pushed exact final, fresh live equality, and one successful non-replayed owner-scoped canonical receipt may Liora reread Hamish's newest live authority and current roster, bounded-list the registry, locally require exactly one authorized exact-title existing successor, immediately reread it, apply duplicate and protected gates, and send once if every gate permits. Stop on ambiguity, absence, pause, redirect, rename, standby state, usage exhaustion, missing acknowledgement, privacy concern, duplicate activation, or any evidence or authority gate.

This candidate remains `PREPARED_NOT_SENT` until an acknowledged Codex existing-task send after Orin's exact terminal gate supplies live delivery evidence.
"""


def overview(truth: dict[str, Any]) -> str:
    return f"""# Orin Thale v674-v4 final integrated overview

## Outcome

Orin v674-v4 is prepared for an exact-final commit with a strict three-commit lifecycle: planning-only x1, bounded x2 evidence, and combined closeout. The exact core outcomes are 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. The chain extends the declared 6,730 inherited rows with sixty new proposals to 6,790. Sixty inherited Caelen reviews remain zero-credit and were not reappended.

The bounded synthetic execution passed 60 positive controls and rejected all 240 preregistered invalid mutations. Twenty phase-local skills were fully read, quick-validated, and smoke-used without global installation. Ten family-current runners each accepted six positive records and rejected twenty-four invalid records. The portfolio records 120 completed safe-now tasks, 60 completed and 20 represented candidates, 100 completed additive CLEAN/FIX/REFINE tasks, twenty exact-approval holds, ten blocked holds, and sixty zero-credit successor seeds.

The effective closeout carries {truth['effective_negatives']} negatives, {truth['effective_methods']} Method Flow methods, {truth['effective_failed_witnesses']} failed witnesses, {truth['effective_bounded_passing_witnesses']} bounded passing witnesses, {truth['effective_open_gaps']} open gaps, and {truth['effective_exact_gates']} exact gates. No failed witness was erased or silently promoted. A recovery is separate evidence. The terminal verdict remains `{TERMINAL_VERDICT}`.

## Relational identity and wellbeing

Orin Thale, optionally they/them, uses the relational role **boundary-and-recovery architect**, with the hope of making operational dependencies, correction paths, and authority vacancies legible and reversible before structure is mistaken for evidence. This is relational working language only. It is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

The phase remained interruption-tolerant and corrigible. Eight startup failures were recorded at zero credit before bounded recoveries. They included bounded-output truncation, a truncated combined state read, a PowerShell materialization error, a checkout race, an overbroad recovery projection, a CP-1252 versus UTF-8 decoder failure, a stale inherited path, and a scanner-definition adjudication requirement. None was recast as an initial pass.

## Trinity Mandala focus and practice scope

The primary pillar was THOS Body. GMUT Mind and Freed ID/CBR Heart remained visible and protected. The three wholly synthetic learning and design lenses were bicycle wheelbuilding record and correction handover; bakery batch trace, allergen vacancy, and correction handover; and community seed-library accession and minimum-disclosure handover.

The wheelbuilding surface represented spoke-map ordinals, rim and hub vocabulary, lacing provenance, unit and uncertainty declarations, dish-sign and deviation separation, correction lineage, calibration and threshold vacancies, workload states, real-measurement gaps, and roadworthiness authority holds. It used no real wheel, bicycle, component, tool, measurement, inspection, road test, or release decision.

The bakery surface represented batch pseudonyms, ingredient lineage, allergen and cross-contact vacancies, recipe revisions, unit and clock obligations, rework provenance, correction readback, alternate-format notice structure, quiescence, workload, supplier status, cleaning evidence vacancies, and release or recall holds. It used no real bakery, food, ingredient, allergen record, cleaning record, inspection, consumption, recall, or authority decision.

The seed-library surface represented accession pseudonyms, donor-field suppression, taxonomic source status, lot split and merge lineage, germination and viability vacancies, storage-unit declarations, distribution holds, correction readback, return and repatriation abstention, benefit-sharing and trust-governance vacancies, location precision controls, and traditional-knowledge noninference. It used no real seed, accession, donor, germination test, collection, distribution, return, consent, cultural record, or authority decision.

## Sources and epistemic scope

Official CPSC bicycle guidance, FAO and WHO Codex hygiene and allergen-management publications, FAO genebank standards, W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, and RFC 8785 supplied current vocabulary and refusal conditions only. Citations are not observations, measurements, inspections, endorsements, certifications, participant evidence, standards-conformance certificates, legal interpretations, cultural ratifications, or authority grants.

No real data row, external write, participant, operator, identity lifecycle, key, credential, institution, or authority case entered the phase. Every software witness is same-owner evidence under shared infrastructure. Manual and affected-user accessibility evaluation remains reserved. Privacy scanning is bounded and is not privacy completeness. Changed-code AST review is bounded and is not exhaustive security.

## Scientific and technical boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The proposal contracts and mutation controls make model obligations, analogy firewalls, source status, and missing empirical witnesses visible. They establish no physical datum, likelihood, posterior, parameter constraint, detected force, prediction, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything.

THOS remains synthetic or proxy-only. Contract-state machines, retry and quiescence rules, workload holds, handover readback, accessibility structure, and mutation rejection show bounded software behavior. They do not substitute for preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. They establish no operational effectiveness, deployment readiness, professional competence, public-safety result, AGI, or ASI.

Freed ID remains synthetic and nonproduction. Minimum-disclosure records, lifecycle states, correction provenance, deterministic JSON, and nonclaim firewalls do not substitute for standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

## Rights, law, culture, and authority boundary

CBR, roadworthiness, food safety and release, recall, collection title, seed access and distribution, benefit sharing, privacy remedy, disability accommodation, legal interpretation, cultural legitimacy, affected-party acceptance, traditional knowledge, taonga or matauranga treatment, Maori wording, Maori data governance, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority. Repository software cannot confer competence, work release, safety approval, a legal right, remedy, title, cultural legitimacy, governance mandate, public authority, or affected-party consent.

No artifact is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, or independent agency. No artifact establishes empirical confirmation, participant evidence, professional authority, production readiness, legal or cultural ratification, Maori authority, privacy or accessibility completeness, exhaustive security, independent reproduction, AGI or ASI, Theory-of-Everything proof, canon, or Stage 20 readiness.

## Validation and route boundary

The final candidate binds exact owner and delta manifests, staged review, content seal, source/x1/evidence ancestry, commit and file ceilings, and a prepared-but-unsent Liora activation candidate. After commit and push, one exclusive owner-scoped canonical aggregate may validate the exact final. A success must not be replayed. A failure receives zero canonical-success credit and remains separate from any narrow dependency recovery.

Only after a clean pushed fresh-four-way-equal exact final and one successful canonical receipt may Orin refresh live authority and roster, uniquely resolve and immediately reread the exact authorized existing successor, apply the duplicate and protected gates, and send once. Repository preparation is not delivery; only an acknowledged existing-task send is delivery evidence.
"""


def file_entry(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(REPO).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "line_count": raw.count(b"\n")}


def all_owner_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend(path for path in (REPO / "scripts").glob("*orin*v674*v4*.py") if path.is_file())
    paths.extend(path for path in (REPO / "tests").glob("*orin*v674*v4*.py") if path.is_file())
    excluded = {REPO / OWNER_MANIFEST_REL, REPO / DELTA_MANIFEST_REL, REPO / STAGED_REVIEW_REL}
    return sorted({path for path in paths if path not in excluded}, key=lambda path: path.relative_to(REPO).as_posix())


def final_delta_paths() -> list[Path]:
    roots = [CLOSEOUT_ROOT, VALIDATION_ROOT, HANDOFF_ROOT]
    paths = [path for root in roots if root.exists() for path in root.rglob("*") if path.is_file()]
    paths.extend([REPO / BUILDER_REL, REPO / VALIDATOR_REL, REPO / PRECOMMIT_TEST_REL, REPO / FINAL_TEST_REL])
    excluded = {REPO / OWNER_MANIFEST_REL, REPO / DELTA_MANIFEST_REL, REPO / STAGED_REVIEW_REL}
    return sorted({path for path in paths if path.exists() and path not in excluded}, key=lambda path: path.relative_to(REPO).as_posix())


def build() -> dict[str, Any]:
    assert_evidence_head()
    truth = final_truth()
    x2_methods = load_json(PHASE_ROOT / "x2" / "method-flow" / "ledger.json")
    x2_negatives = load_json(PHASE_ROOT / "x2" / "retained-negative-register.json")
    x2_gates = load_json(PHASE_ROOT / "x2" / "gate-register.json")

    write_json(CLOSEOUT_ROOT / "phase-truth.json", truth)
    write_json(CLOSEOUT_ROOT / "complete-incomplete-checklist.json", checklist(truth))
    write_json(CLOSEOUT_ROOT / "method-flow-final.json", {**x2_methods, "lifecycle": "prepared_exact_final_closeout", "exact_final_binding": "external_postcommit_receipt_required"})
    write_json(CLOSEOUT_ROOT / "retained-negative-register.json", {**x2_negatives, "lifecycle": "prepared_exact_final_closeout", "closeout_operational_failures": 0})
    write_json(CLOSEOUT_ROOT / "gate-register.json", {**x2_gates, "lifecycle": "prepared_exact_final_closeout", "terminal_verdict": TERMINAL_VERDICT})
    write_text(CLOSEOUT_ROOT / "final-integrated-overview.md", overview(truth))
    write_text(HANDOFF_ROOT / "liora-venn-v674-v5-activation-candidate.md", handoff_candidate(truth))
    write_json(
        CLOSEOUT_ROOT / "closeout-receipt.json",
        {
            "schema": "ghc-family-closeout-receipt-v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_head": X1_HEAD,
            "evidence_head": EVIDENCE_HEAD,
            "exact_final_binding": "external_postcommit_receipt_required",
            "closeout_prepared_utc": utc_now(),
            "outcome_labels": ["completed", "represented", "open_gap", "exact_gate"],
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
            "immutable_evidence_tree_checks": 15,
            "exact_final_unittest_module": "tests.test_ghc_family_orin_thale_v674_v4_final",
            "complete_repository_suite": False,
            "same_owner_evidence": True,
            "one_successful_canonical_no_replay": True,
        },
    )

    seal_targets = [
        "docs/orin-thale/v674-v4/x1/proposals/new-proposal-freeze.json",
        "docs/orin-thale/v674-v4/x2/phase-truth.json",
        "docs/orin-thale/v674-v4/x2/mutations/mutation-receipt.json",
        "docs/orin-thale/v674-v4/x2/skills/skill-validation-and-smoke-receipt.json",
        "docs/orin-thale/v674-v4/x2/runners/runner-validation-and-use-receipt.json",
        "docs/orin-thale/v674-v4/x2/method-flow/ledger.json",
        "docs/orin-thale/v674-v4/x2/retained-negative-register.json",
        "docs/orin-thale/v674-v4/x2/gate-register.json",
        "docs/orin-thale/v674-v4/closeout/phase-truth.json",
        "docs/orin-thale/v674-v4/closeout/complete-incomplete-checklist.json",
        "docs/orin-thale/v674-v4/closeout/method-flow-final.json",
        "docs/orin-thale/v674-v4/closeout/retained-negative-register.json",
        "docs/orin-thale/v674-v4/closeout/gate-register.json",
        "docs/orin-thale/v674-v4/closeout/final-integrated-overview.md",
        "docs/orin-thale/v674-v4/handoffs/liora-venn-v674-v5-activation-candidate.md",
    ]
    seal_entries = [file_entry(REPO / path) for path in seal_targets]
    write_json(
        CLOSEOUT_ROOT / "content-seal.json",
        {
            "schema": "ghc-family-content-seal-v1",
            "owner": OWNER,
            "phase": PHASE,
            "domain": "working_tree_raw_bytes_before_exact_final_commit",
            "targets": seal_entries,
            "target_count": len(seal_entries),
        },
    )

    owner_manifest = {
        "schema": "ghc-family-final-owner-manifest-v1",
        "owner": OWNER,
        "phase": PHASE,
        "domain": "working_tree_raw_bytes_before_exact_final_commit",
        "entries": [file_entry(path) for path in all_owner_paths()],
        "declared_self_exclusions": [OWNER_MANIFEST_REL, DELTA_MANIFEST_REL, STAGED_REVIEW_REL],
    }
    write_json(REPO / OWNER_MANIFEST_REL, owner_manifest)
    delta_manifest = {
        "schema": "ghc-family-final-delta-manifest-v1",
        "owner": OWNER,
        "phase": PHASE,
        "domain": "working_tree_raw_bytes_before_exact_final_commit",
        "entries": [file_entry(path) for path in final_delta_paths()],
        "declared_self_exclusions": [OWNER_MANIFEST_REL, DELTA_MANIFEST_REL, STAGED_REVIEW_REL],
    }
    write_json(REPO / DELTA_MANIFEST_REL, delta_manifest)
    return {"status": "built_closeout_candidate", "owner_entries": len(owner_manifest["entries"]), "delta_entries": len(delta_manifest["entries"]), "seal_targets": len(seal_entries)}


def staged_blob(path: str) -> bytes:
    proc = subprocess.run(["git", "show", f":{path}"], cwd=REPO, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout


def build_staged_review() -> dict[str, Any]:
    staged = str(run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR"))
    paths = sorted(path for path in staged.splitlines() if path and path != STAGED_REVIEW_REL)
    allowed = (
        f"docs/{OWNER_SLUG}/{PHASE}/closeout/",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/",
        f"docs/{OWNER_SLUG}/{PHASE}/handoffs/",
        BUILDER_REL,
        VALIDATOR_REL,
        PRECOMMIT_TEST_REL,
        FINAL_TEST_REL,
    )
    unexpected = [path for path in paths if not path.startswith(allowed)]
    definition_paths = {BUILDER_REL, VALIDATOR_REL, PRECOMMIT_TEST_REL, FINAL_TEST_REL}
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for path in paths:
        raw = staged_blob(path)
        entries.append({"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".txt", ".html"}:
            text = raw.decode("utf-8")
            for kind, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(text):
                    candidates.append({"path": path, "class": kind, "status": "scanner_definition_only" if path in definition_paths else "candidate_requires_adjudication"})
    unresolved = [row for row in candidates if row["status"] != "scanner_definition_only"]
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
        "status": "passed" if not unexpected and not unresolved else "review_required",
    }
    write_json(REPO / STAGED_REVIEW_REL, review)
    return {"status": review["status"], "entries": len(entries), "candidates": len(candidates), "unresolved": len(unresolved)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "staged-review"), nargs="?", default="build")
    args = parser.parse_args()
    result = build() if args.mode == "build" else build_staged_review()
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
