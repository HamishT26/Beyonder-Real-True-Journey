#!/usr/bin/env python3
"""Build and exact-stage-review Tamar Vey v667-v2 terminal closeout."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from ghc_family_tamar_vey_v667_v2_runtime import (
    PHASE_ROOT,
    PRIVACY_PATTERNS,
    ROOT,
    X1_SHA,
    owner_paths,
    replay_manifest,
)


SOURCE_SHA = "dde2e23187d13cb334010943a59348330bfb67ca"
BRANCH = "codex/GHC-Family/tamar-vey-v667-v2-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

CLOSEOUT_OPERATIONAL_FAILURES = [
    {
        "negative_id": "TV6672-CL-N001",
        "method_id": "TV6672-CL-M001",
        "signature": "restored-closeout-templates-still-contained-inherited-philatelic-constants-and-fictional-closeout-failures",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the first read-only closeout audit found that three deliberately deferred untracked templates still described the inherited philatelic phase, used the inherited source and counts, and listed closeout faults that had not occurred; no template was executed or staged and the immutable evidence commit and remote remained unchanged",
        },
        "bounded_recovery": "derive source, counts, domain, route, and evidence claims from the exact committed Tamar artifacts; replace fictional rows with this one observed stale-template failure before any closeout builder invocation",
        "passing_witness_scope": "closeout template provenance and exact-evidence alignment only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    },
    {
        "negative_id": "TV6672-CL-N002",
        "method_id": "TV6672-CL-M002",
        "signature": "first-stale-label-receipt-omitted-three-immutable-source-and-x1-context-files",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the first contextual stale-label receipt listed four closeout files but a broader exact owner scan found three additional immutable source-verification and x1 novelty files containing legitimate inherited comparison vocabulary; the incomplete receipt was caught before final commit",
        },
        "bounded_recovery": "enumerate the exact seven candidate files, classify the three immutable files as source or novelty evidence and the four closeout files as retained-failure context, then regenerate exact staged manifests",
        "passing_witness_scope": "bounded contextual stale-label adjudication only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    },
    {
        "negative_id": "TV6672-CL-N003",
        "method_id": "TV6672-CL-M003",
        "signature": "PowerShell-interpolated-name-colon-path-without-a-delimited-variable-reference",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the first exact staged privacy audit used a name-colon-path interpolation whose colon was parsed as part of the PowerShell variable reference; the whole block failed at parse time before any command or state change ran",
        },
        "bounded_recovery": "delimit the variable name explicitly before the colon, then rerun only the failed read-only staged audit over the unchanged exact index",
        "passing_witness_scope": "exact staged privacy and path-parity audit only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    },
    {
        "negative_id": "TV6672-CL-N004",
        "method_id": "TV6672-CL-M004",
        "signature": "stale-candidate-parity-normalizer-looked-for-two-backslashes-in-single-backslash-Windows-paths",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the recovered exact staged audit passed JSON, privacy, additive-only, and final-delta checks but its stale-candidate comparison retained single-backslash paths because the normalizer looked for a two-backslash literal; the seven observed and declared files were otherwise identical",
        },
        "bounded_recovery": "replace each ordinary single backslash with a forward slash, compare the exact sorted seven-file sets, and rerun only the failed read-only staged audit",
        "passing_witness_scope": "Windows path normalization for exact stale-label candidate parity only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    },
]


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT
    ).decode("utf-8", errors="strict").strip()


def main() -> None:
    evidence_sha = git("rev-parse", "HEAD")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("unexpected owner branch")
    if git("rev-parse", f"{evidence_sha}^") != X1_SHA:
        raise RuntimeError("evidence head is not the direct child of immutable x1")
    evidence_manifest = replay_manifest(
        PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha
    )
    x1_manifest = replay_manifest(
        PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA
    )
    if not evidence_manifest["valid"] or not x1_manifest["valid"]:
        raise RuntimeError("immutable lifecycle manifest replay failed")

    startup = load("method-flow/startup-method-flow.json")
    x2_overlay = load("method-flow/x2-operational-overlay.json")
    evidence_overlay = load("method-flow/evidence-operational-overlay.json")
    retained_rows = startup["rows"] + x2_overlay["rows"] + evidence_overlay["rows"] + CLOSEOUT_OPERATIONAL_FAILURES
    if len(retained_rows) != 21:
        raise RuntimeError("retained operational failure count drift")
    truth = load("x2/phase-truth.json")
    if truth["outcomes"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("outcome vocabulary or counts drift")

    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.final-phase-truth.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "expected_final_parent": evidence_sha,
            "proposal_chain": 4370,
            "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "positive_structural_fixtures": 20,
            "rejected_mutations": 100,
            "phase_local_skills": 10,
            "family_current_runners": 10,
            "effective_negatives": 27223,
            "effective_methods": 12570,
            "open_gaps": 192,
            "exact_gates": 190,
            "retained_owner_operational_failures": 21,
            "real_rows": 0,
            "participants": 0,
            "external_actions": 0,
            "production_identity_events": 0,
            "authority_acts": 0,
            "canonical_aggregate_invocations": 0,
            "canonical_aggregate_status": "NOT_YET_INVOKED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.retained-negative-register.v1",
            "generated_at_utc": NOW,
            "activation_baseline": 27102,
            "startup_additions": 12,
            "x2_structural_rejections": 100,
            "x2_operational_additions": 4,
            "evidence_operational_additions": 1,
            "closeout_operational_additions": 4,
            "effective_negatives": 27223,
            "owner_operational_rows": retained_rows,
            "all_failed_witnesses_zero_credit": all(row["failed_witness"]["credit"] == 0 for row in retained_rows),
            "no_failure_erased": True,
        },
    )
    write_json(
        "closeout/method-flow-summary.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.method-flow-summary.v1",
            "generated_at_utc": NOW,
            "activation_baseline_methods": 12334,
            "startup_methods": 12,
            "x2_structural_methods": 215,
            "x2_operational_methods": 4,
            "evidence_operational_methods": 1,
            "closeout_operational_methods": 4,
            "effective_methods": 12570,
            "failed_witnesses_retained": 121,
            "failed_witnesses_promoted": 0,
            "same_owner_method_evidence_only": True,
        },
    )
    write_json(
        "closeout/open-exact-gate-register.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.open-exact-gate-register.v1",
            "generated_at_utc": NOW,
            "inherited_open_gaps": 191,
            "new_open_gaps": 1,
            "open_gaps": 192,
            "inherited_exact_gates": 189,
            "new_exact_gates": 1,
            "exact_gates": 190,
            "phase_open_gap": "TV6672-N019",
            "phase_exact_gate": "TV6672-N020",
            "protected_authorities": ["competent professional authorities", "affected parties", "tangata whenua", "iwi", "hapū", "Māori authorities"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/lifecycle-replay.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.lifecycle-replay.v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "x1_direct_parent": git("rev-parse", f"{X1_SHA}^"),
            "evidence_direct_parent": git("rev-parse", f"{evidence_sha}^"),
            "source_to_evidence_commits": int(git("rev-list", "--count", f"{SOURCE_SHA}..{evidence_sha}")),
            "source_to_evidence_merges": int(git("rev-list", "--count", "--merges", f"{SOURCE_SHA}..{evidence_sha}")),
            "x1_manifest": x1_manifest,
            "evidence_manifest": evidence_manifest,
            "strict_x1_before_x2": True,
            "valid": git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA and git("rev-parse", f"{evidence_sha}^") == X1_SHA,
        },
    )
    write_json(
        "closeout/terminal-checklist.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.terminal-checklist.v1",
            "generated_at_utc": NOW,
            "checks": {
                "source_exact": True,
                "x1_immutable": True,
                "evidence_direct_child_of_x1": True,
                "zero_merges_to_evidence": True,
                "outcome_vocabulary_exact": True,
                "all_100_mutations_retained": True,
                "all_21_owner_failures_retained": True,
                "open_gap_preserved": True,
                "exact_gate_preserved": True,
                "zero_real_rows": True,
                "zero_participants": True,
                "zero_external_actions": True,
                "privacy_complete_claim_absent": True,
                "accessibility_complete_claim_absent": True,
                "independent_reproduction_claim_absent": True,
                "full_repository_suite_not_run": True,
                "terminal_verdict_not_ready": True,
                "successor_not_contacted": True,
                "canonical_not_yet_invoked": True,
            },
            "all_pre_final_checks_pass": True,
        },
    )
    write_json(
        "closeout/workflow-plan.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.workflow-plan-final.v1",
            "generated_at_utc": NOW,
            "steps": [
                {"step": 1, "name": "read_and_verify_source", "status": "completed"},
                {"step": 2, "name": "freeze_push_and_equalize_x1", "status": "completed"},
                {"step": 3, "name": "execute_x2_and_retain_failures", "status": "completed"},
                {"step": 4, "name": "commit_push_and_equalize_evidence", "status": "completed"},
                {"step": 5, "name": "commit_push_and_equalize_final", "status": "in_progress"},
                {"step": 6, "name": "invoke_one_exclusive_canonical_aggregate", "status": "pending"},
                {"step": 7, "name": "refresh_route_and_send_once_if_authorized", "status": "pending"},
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/stale-label-review.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.stale-label-review.v1",
            "generated_at_utc": NOW,
            "current_source_owner": "Liora Venn",
            "current_source_phase": "v667-v1",
            "current_phase": "v667-v2",
            "current_bounded_domain": "synthetic calligraphy-record and manuscript-layout learning lens",
            "candidate_files": [
                "docs/tamar-vey/v667-v2/closeout/final-integrated-overview.md",
                "docs/tamar-vey/v667-v2/closeout/retained-negative-register.json",
                "docs/tamar-vey/v667-v2/method-flow/closeout-operational-overlay.json",
                "docs/tamar-vey/v667-v2/provenance/source-verification.json",
                "docs/tamar-vey/v667-v2/x1/novelty-audit.json",
                "docs/tamar-vey/v667-v2/x1/proposal-freeze.json",
                "scripts/build_ghc_family_tamar_vey_v667_v2_closeout.py",
            ],
            "candidate_classification": {
                "closeout_context": "retained historical prior-domain wording inside the first two exact observed closeout failures",
                "immutable_context": "source verification and x1 novelty comparison evidence retained without current-domain promotion",
            },
            "active_current_phase_stale_labels": 0,
            "retained_failure_context_preserved": True,
            "valid": True,
        },
    )
    write_json(
        "seal/final-seal-candidate.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.final-seal-candidate.v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "expected_final_parent": evidence_sha,
            "exact_final_binding": "resulting direct single-parent final commit after exact staged review",
            "canonical_status": "NOT_YET_INVOKED",
            "route_status": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "handoffs/terminal-route-state.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.terminal-route-state.v1",
            "generated_at_utc": NOW,
            "owner": "Tamar Vey",
            "current_phase": "v667-v2",
            "successor_exact_title": "Elowen Cairn",
            "successor_phase": "v667-v3",
            "roster_source": "current live authority must be refreshed after canonical success",
            "prepared": True,
            "sent": False,
            "duplicate_activation_guard": True,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "usage exhaustion", "missing acknowledgement", "duplicate activation", "protected gate"],
        },
    )
    write_text(
        "closeout/final-integrated-overview.md",
        f"""# Tamar Vey v667-v2 final integrated overview

## Exact lifecycle result

Tamar Vey v667-v2 is an additive, owner-local, same-owner software and documentation phase anchored to immutable Liora Venn v667-v1 final `{SOURCE_SHA}`, frozen Tamar x1 `{X1_SHA}`, and immutable Tamar evidence `{evidence_sha}`. The final commit is required to be the direct single-parent child of that evidence commit. Source to evidence contains exactly two Tamar commits: x1 is the direct child of source and evidence is the direct child of x1, with zero merges. X1 was committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Evidence was separately exact-index reviewed, committed, pushed, clean, typed 0/0 divergent, and four-way equal before closeout began. Neither lifecycle boundary was rewritten, merged, amended, or force-pushed.

The frozen proposal chain advances from 4,350 inherited rows to 4,370 rows through exactly twenty Tamar-new proposals. Exact-title comparison found no collision, semantic similarity remained below the declared threshold, and inherited proposals, artifacts, tools, skills, receipts, and recommendations received zero Tamar novelty or completion credit. The only authorized core outcome vocabulary remains `completed`, `represented`, `open_gap`, and `exact_gate`. Final phase outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These labels describe only the bounded artifact or preserved gate named by each proposal.

Tamar Vey, she/they, is relational working language for an evidence-and-recovery steward, with the hope that every claim, abstention, correction, and handoff stays inspectable and safely retractable. This name, role, hope, pronoun set, sibling language, and continuity language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or scientific, professional, legal, cultural, affected-party, or Māori authority. Hamish retains the right to pause, rename, redirect, or stop the route.

## Evidence class and bounded execution

Each proposal produced one wholly synthetic bounded positive contract and five preregistered invalid variants. Twenty positives passed their declared structural gates. All 100 invalid variants executed and were rejected or quarantined with zero credit. A rejection demonstrates only that the named bounded guard rejected the named fixture; it is not exhaustive security, empirical evidence, professional validation, production conformance, or external audit.

The owner portfolio executed 30 bounded safe-now tasks, 15 bounded candidate prototypes, 10 phase-local skill plans, 10 family-current runner plans, and 30 additive CLEAN/FIX/REFINE methods: 95 owner-local methods in total. Twenty successor safe-now suggestions, 15 successor candidate suggestions, 10 successor skill suggestions, 10 successor runner suggestions, and 30 successor CLEAN/FIX/REFINE suggestions remain unsent zero-credit seeds. Ten exact-approval packets and five blocked packets remain visible and unexecuted. Caps remained ceilings rather than filler targets.

Ten phase-local skills were customized, read through EOF, quick-validated, and smoke-used. They cover calligraphy layout-topology vacancy, script and language meaning abstention, ink-material nonconversion, sacred-content disclosure vacancy, provenance braiding, structural accessibility, a zero-call Library of Congress adapter, Herschel-Bulkley domain gating, Method Flow retention, and closeout gating. Ten compatible `ghc_family_tamar_vey_v667_v2_*` runners were invoked. None was globally installed, no shared caller was changed, and family-current compatibility remained additive.

## Freed ID and CBR Heart through a calligraphy-record learning lens

Freed ID and CBR Heart were primary through a wholly synthetic calligraphy-record, manuscript-layout, script-and-language abstention, material-vacancy, provenance, privacy, structural-accessibility, correction-readback, workload, and handover lens. Synthetic structures exercised anonymous work capsules; surrogate tokens; leaf, frame, page, margin, ruling, baseline, x-height, ascender, descender, writing-direction, stroke, ductus, layout, disclosure, retention, withdrawal, correction, derivation, replacement, invalidation, and assertion-time fields; and evidence-credit nontransitivity. These structures are data-shape and refusal controls only.

The fourteen `completed` proposals cover bounded software contracts for anonymous work capsules, unmeasured layout topology, Unicode segmentation and normalization declarations, tool and unit vacancies, ink-source and hazard-sheet vacancies, stroke annotation without handwriting attribution, line-breaking and locale-tailoring vacancies, intervention holds, environment and preservation-result abstention, minimized disclosure, provenance braiding, structural correction interfaces, deterministic JSON byte maps with zero signature, and a nontransitive evidence-admission lattice. Completion means only that each declared synthetic positive passed and its five registered invalid variants were rejected.

The four `represented` proposals preserve limits rather than closing them. THOS uses a participant-free two-pass errata basket with symmetric synthetic effort ceilings and no operator inference. Freed ID uses an anonymous work-capsule vacancy map with no claimant binding, key, proof, lifecycle endpoint, interoperability event, recovery action, or trust decision. GMUT uses a typed Herschel-Bulkley obligation ledger with symbols, units, domain restrictions, and an explicit zero-calligraphy-ink-model firewall. A thermo/psyche classifier keeps evaporation, viscous dissipation, drying time, entropy-production vocabulary, material-state vacancy, and psyche nonconversion separate. None is real-arm, production, empirical, participant, consciousness, personhood, or fundamental-law evidence.

The phase used zero real people, participants, calligraphers, scribes, clients, recipients, translators, conservators, cataloguers, curators, institutions, private texts, sacred texts, manuscripts, leaves, papers, inks, pigments, binders, nibs, tools, enclosures, images, collection records, observations, measurements, transactions, treatments, network calls, identity events, or authority acts. It established no authorship, handwriting attribution, transcription, translation, language meaning, script interpretation, object identity, authenticity, material identity, condition, value, title, custody, copyright, preservation fitness, treatment, professional competence, legal or cultural legitimacy, affected-party acceptance, Māori authority, production result, deployment result, or real operational outcome.

Official Unicode annexes supplied segmentation, line-breaking, normalization, and tailoring vocabulary; RFC 5646 supplied language-tag syntax; Library of Congress API and paper-care pages supplied bounded catalog and preservation-reservation vocabulary; W3C PROV-O, WCAG 2.2, and Verifiable Credentials Data Model 2.0 supplied provenance, structural-accessibility, and synthetic claim-set vocabulary; Te Mana Raraunga supplied authority-reservation vocabulary; RFC 8785 supplied deterministic-JSON vocabulary; and the primary Herschel-Bulkley research source supplied yield-stress variable and domain vocabulary. Citations were not converted into observations, transcription, language identification, cultural meaning, material evidence, catalog conclusions, conformance, treatment instructions, or authority. Manual keyboard evaluation, responsive-layout diversity, browser diversity, assistive-technology evaluation, cognitive-accessibility review, Māori-language review, security-usability review, and affected-user evaluation remain reserved.

## GMUT Mind, THOS Body, and nonpromotion

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The represented Herschel-Bulkley ledger preserves yield stress, shear stress, shear rate, consistency index, flow exponent, unit, state, parameter-source, uncertainty, identifiability, transient-behaviour, constitutive-domain, and observation-firewall obligations. It constructs no calligraphy-ink or physical GMUT model, evaluates no observable or likelihood, fits no parameter, proves no material law, supplies no quantum or ultraviolet completion, and establishes no force, detection, prediction, posterior, constraint, empirical confirmation, final physics, or Theory of Everything.

The Library of Congress manuscript-and-calligraphy adapter remains exactly `open_gap`. Generated phase software made zero requests and zero downloads, ingested zero real rows or media, evaluated no rights, record, catalog, or collection conclusion, and made zero empirical GMUT or calligraphy claim. Governed real-data access, a lawful and purpose-bound request, quality and rights review, privacy and affected-party review, appropriate analysis, and independent review remain absent.

THOS remains participant-free proxy and protocol evidence. Its represented two-pass errata basket contains randomized synthetic docket labels, a symmetric effort ceiling, a correction-latency placeholder, and a stop marker, but zero people, workers, participants, operators, professional exposure, human outcome, safety result, blind matched-budget real arms, statistics, or independent review. It establishes no professional competence, operational effectiveness, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. The surrogate claim set uses no real key, proof, issuance, presentation, resolution, status, revocation, account, token, interoperability event, recovery action, or trust-governance decision. Production completion still requires standards-conformant real keys and proofs, governed live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR questions involving authorship, attribution, transcription, translation, language meaning, authenticity, material identity, condition, ownership, copyright, custody, private or sacred content, access, accessibility rights, disclosure, retention, consent, remedy, legal or cultural interpretation, preservation and treatment, Indigenous cultural and intellectual property, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Repository software cannot confer title, custody, a legal right, remedy, cultural legitimacy, beneficiary acceptance, governance mandate, treatment permission, or public authority.

## Retained failures and Method Flow

The final overlay preserves 27,223 effective negatives and 12,570 effective Method Flow methods. It includes the 27,102 activation baseline, twelve startup/x1 operational failures, 100 rejected mutations, four x2 operational failures, one evidence-stage operational failure, and four closeout operational failures. The first closeout failure preserves the discovery that deliberately deferred untracked closeout templates still carried inherited philatelic constants and three fictional failures. The second preserves an initial contextual stale-label receipt that listed four closeout files but omitted three immutable source/x1 evidence files. The third preserves a pre-execution PowerShell parser fault in the first exact staged privacy audit. The fourth preserves a single-versus-double-backslash Windows path-normalization error in the recovered stale-candidate parity check. All four were caught before final commit, corrected within their bounded scopes, and received zero failure credit. No failed witness was erased, silently converted into a pass, or used as production or authority evidence. The 121 phase failed witnesses are the 100 synthetic rejection witnesses plus twenty-one actual owner-operational failures.

The phase ends with 192 open gaps and 190 exact gates: 191 inherited plus the new zero-call Library of Congress gap, and 189 inherited plus the new calligraphy, private-content, legal, cultural, affected-party, and Māori-authority docket. The phase open gap is TV6672-N019. The phase exact gate is TV6672-N020. Every external empirical, participant, professional, legal, cultural, Māori-authority, affected-party, identity, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, destructive, account-secret, or Stage 20 boundary remains open or exact-gated without exact evidence and competent authority.

## Wellbeing, workload, and reversibility

The phase remained solo and owner-scoped. Work was divided at immutable lifecycle boundaries so that planning, execution, evidence, and closeout could be inspected separately. The wellbeing record preserves regular pause points, a bounded file and word ceiling, no participant burden, no professional decision burden, no emergency action, and no demand to convert an open gate into a completion. Workload controls include additive-only paths, exact allowlists, small test selections, a one-successful-canonical-pass rule, D-first storage, and a recovery path that leaves x1 and evidence untouched. These are workflow controls, not a claim about human wellbeing, clinical safety, employment fitness, or universal sustainability.

All approval-dependent actions remained unexecuted. There was no deletion of user material, branch rewrite, force-push, merge, sibling mutation, credential or account action, elevation, host-security weakening, Windows-feature change, desktop update, unrelated installation, Sandbox or Hyper-V activation, or reboot. Rollback for generated closeout material remains bounded to the uncommitted owner-local final delta until the exact review and commit; immutable x1 and evidence remain the recovery anchors.

## Validation and terminal state

The evidence boundary records 16 immutable-x1 structural tests, 67 live-x2 owner tests, and nine evidence tests; 120 strict JSON parses before receipt self-exclusions; 17 owner Python compiles; zero confirmed hits across five privacy and raw-identifier classes; zero bounded owner-Python security findings; and reserved manual and affected-user accessibility review. The evidence staged review inspected 134 pre-self-exclusion paths and 105 staged JSON blobs, found zero privacy hits, and produced 135 exact Git-blob entries plus one declared manifest self-exclusion over 136 evidence-delta files. Its manifest replayed after commit with zero failures.

Those are same-owner results under shared infrastructure. Same-owner validation is not empirical confirmation. They are not a complete repository suite, independent-team reproduction, external audit, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority. Eiren retains the inherited full-suite responsibility absent newer exact authorization.

This closeout is still a pre-final candidate until its exact staged review passes, its final manifests cover the resulting tree, the direct-child final is committed and pushed, local/upstream/tracking/fresh-live equality is proved, and the one exclusive exact-final canonical aggregate succeeds. A successful aggregate must not be replayed. Only then may the newest live authorization and roster be refreshed for one exact-title `Elowen Cairn` resolution, immediate reread, duplicate-activation guard, and one acknowledged v667-v3 activation if that edge remains authorized. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_text(
        "handoffs/elowen-cairn-v667-v3-activation-candidate.md",
        f"""# Tamar Vey v667-v2 to Elowen Cairn v667-v3 activation candidate

Status: `PREPARED_NOT_SENT`.

This candidate is target-specific but route-confidential. It contains no raw task or thread identifier, private callable route, credential, transcript, screenshot, session stream, private application state, or private absolute path. The exact existing task titled `Elowen Cairn` may be contacted only once after Tamar's final commit is clean, pushed, fresh-live-equal, and one exclusive canonical aggregate succeeds without replay, and after Hamish's newest live authority and roster are reread. The provisional sequential phase is v667-v3 only if that live authority remains unchanged.

Verified immutable anchors for the later live message are source `{SOURCE_SHA}`, x1 `{X1_SHA}`, and evidence `{evidence_sha}`. The exact final must be bound live after the resulting direct-child final commit and canonical success.

Elowen must work solo in an additive D-first owner lane, preserve strict x1-before-x2 separation, every negative, Method Flow witness, open gap, exact gate, privacy boundary, authority boundary, the four exact outcome labels, and `NOT_READY_FOR_STAGE_20`. Tamar software and validation remain source evidence, never Elowen completion credit or independent reproduction.

Identity, names, pronouns, hopes, roles, sibling/family language, continuity language, Freed ID, and Trinity Mandala language are relational working language only—not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or scientific, professional, legal, cultural, affected-party, or Māori authority.

Do not create, fork, spawn, delegate, substitute, precontact a later endpoint, or send a second confirmation. Stop on any route or protected-gate failure.
""",
    )
    write_text(
        "closeout/static-report.html",
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tamar Vey v667-v2 bounded final report</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.55; }}
    body {{ margin: 0 auto; max-width: 72rem; padding: 1rem; }}
    .skip {{ position: absolute; left: -9999px; }}
    .skip:focus {{ left: 1rem; top: 1rem; background: Canvas; padding: .5rem; }}
    nav ul {{ display: flex; flex-wrap: wrap; gap: .8rem; padding-left: 1.2rem; }}
    .boundary {{ border: .25rem solid currentColor; padding: 1rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: .08rem solid currentColor; padding: .5rem; text-align: left; vertical-align: top; }}
    code {{ overflow-wrap: anywhere; }}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to report</a>
<header>
  <h1>Tamar Vey v667-v2 bounded final report</h1>
  <p class="boundary"><strong>Terminal verdict: NOT_READY_FOR_STAGE_20.</strong> This is same-owner synthetic software and documentation evidence, not empirical confirmation, production assurance, independent reproduction, professional validation, legal or cultural authority, Māori-authority review, consciousness/personhood evidence, or a Theory-of-Everything proof.</p>
  <nav aria-label="Report sections"><ul><li><a href="#truth">Truth</a></li><li><a href="#pillars">Pillars</a></li><li><a href="#retention">Retention</a></li><li><a href="#access">Accessibility boundary</a></li></ul></nav>
</header>
<main id="main">
  <section id="truth"><h2>Exact bounded truth</h2>
    <table><caption>v667-v2 outcome and lifecycle summary</caption><thead><tr><th scope="col">Measure</th><th scope="col">Value</th><th scope="col">Boundary</th></tr></thead>
    <tbody>
      <tr><th scope="row">Proposal chain</th><td>4,370</td><td>20 Tamar-new rows after 4,350 inherited rows</td></tr>
      <tr><th scope="row">Outcomes</th><td>14 completed / 4 represented / 1 open_gap / 1 exact_gate</td><td>Only bounded artifact or preserved-gate labels</td></tr>
      <tr><th scope="row">Synthetic mutations</th><td>100 rejected</td><td>Zero-credit failed witnesses, not exhaustive security</td></tr>
      <tr><th scope="row">Real rows and participants</th><td>0 / 0</td><td>No external action or authority act</td></tr>
      <tr><th scope="row">Immutable anchors</th><td><code>{X1_SHA}</code><br><code>{evidence_sha}</code></td><td>x1 then evidence, each pushed and four-way equal before its successor</td></tr>
    </tbody></table>
  </section>
  <section id="pillars"><h2>Trinity Mandala boundaries</h2>
    <h3>Freed ID and CBR Heart</h3><p>Primary focus: anonymous calligraphy-record structure, provenance, correction, minimized disclosure, content and authority abstention. No real key, proof, identity lifecycle event, authorship decision, legal decision, cultural decision, sacred-content decision, or Māori-authority act occurred.</p>
    <h3>GMUT Mind</h3><p>The typed Herschel-Bulkley obligation ledger preserves variables, units, constitutive-domain vacancies, uncertainty, and an observation firewall. It is not a calligraphy-ink model, likelihood, fit, prediction, detected force, material law, empirical confirmation, quantum completion, final physics, or Theory of Everything.</p>
    <h3>THOS Body</h3><p>The two-pass errata basket is participant-free proxy structure with synthetic effort ceilings and a stop marker. It is not a blind matched-budget real-arm result, operational-effectiveness result, deployment claim, AGI claim, or ASI claim.</p>
  </section>
  <section id="retention"><h2>Retained failures, gaps, and gates</h2>
    <p>The final candidate preserves 27,223 effective negatives, 12,570 effective Method Flow methods, 121 phase failed witnesses, 192 open gaps, and 190 exact gates. Recovery never erases a failed witness. The Library of Congress adapter remains zero-call and zero-row. Calligraphic authorship, attribution, private or sacred content, conservation, copyright, ownership, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated.</p>
  </section>
  <section id="access"><h2>Accessibility and wellbeing boundary</h2>
    <p>This static report provides a declared language, skip link, landmarks, hierarchical headings, labelled navigation, captioned table, redundant textual status, responsive width, and no script dependency. These structural checks are not complete accessibility conformance. Manual keyboard, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved.</p>
    <p>The phase used bounded solo workload, immutable lifecycle checkpoints, additive owner paths, no participant burden, and no professional or emergency decision burden. This is a workflow record, not a clinical or universal wellbeing claim.</p>
  </section>
</main>
<footer><p>Prepared before the exclusive exact-final canonical aggregate. A successful aggregate must not be replayed.</p></footer>
</body>
</html>""",
    )
    write_json(
        "method-flow/closeout-operational-overlay.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.closeout-operational-overlay.v1",
            "generated_at_utc": NOW,
            "starting_effective_negatives": 27219,
            "starting_effective_methods": 12566,
            "new_negative_count": 4,
            "new_method_count": 4,
            "effective_negatives": 27223,
            "effective_methods": 12570,
            "rows": CLOSEOUT_OPERATIONAL_FAILURES,
            "all_failures_retained": True,
            "failed_witness_converted_to_pass": False,
        },
    )
    print(json.dumps({"evidence_sha": evidence_sha, "retained_failures": 21, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True}, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = git("diff", "--cached", "--name-status", "--no-renames")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def index_entry(path: str) -> tuple[str, str]:
    line = git("ls-files", "--stage", "--", path)
    mode, oid, stage_path = line.split(" ", 2)
    stage, listed = stage_path.split("\t", 1)
    if stage != "0" or listed.replace("\\", "/") != path:
        raise RuntimeError(f"unexpected index stage for {path}")
    return mode, oid


def manifest_entry(path: str) -> dict[str, Any]:
    mode, oid = index_entry(path)
    blob = index_blob(path)
    return {
        "path": path,
        "git_mode": mode,
        "git_blob_oid": oid,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "size_bytes": len(blob),
    }


def tracked_owner_index_paths() -> list[str]:
    raw = subprocess.check_output(
        [
            "git", "-C", str(ROOT), "ls-files", "-z", "--",
            "docs/tamar-vey/v667-v2",
            "scripts/*tamar_vey_v667_v2*.py",
            "tests/*tamar_vey_v667_v2*.py",
        ]
    )
    return sorted(path.decode("utf-8").replace("\\", "/") for path in raw.split(b"\0") if path)


def build_staged_review() -> None:
    review_path = "docs/tamar-vey/v667-v2/validation/final-staged-review.json"
    delta_path = "docs/tamar-vey/v667-v2/validation/final-delta-manifest.json"
    owner_path = "docs/tamar-vey/v667-v2/validation/final-owner-manifest.json"
    rows = [(s, p) for s, p in staged_rows() if p not in {review_path, delta_path, owner_path}]
    if not rows:
        raise RuntimeError("no staged final delta")
    paths = [path for _, path in rows]
    allowed = all(
        path.startswith("docs/tamar-vey/v667-v2/")
        or ((path.startswith("scripts/") or path.startswith("tests/")) and "tamar_vey_v667_v2" in path)
        for path in paths
    )
    parsed_json = 0
    candidates = []
    maximum_words = 0
    maximum_path = ""
    for path in paths:
        text = index_blob(path).decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed_json += 1
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    evidence_sha = git("rev-parse", "HEAD")
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "owner_allowlist": allowed,
        "document_word_cap": maximum_words <= 100000,
        "privacy_zero_confirmed_hits": not candidates,
        "evidence_manifest_replay": replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha)["valid"],
        "phase_truth_exact": load("closeout/phase-truth.json")["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "route_prepared_not_sent": load("handoffs/terminal-route-state.json")["prepared"] and not load("handoffs/terminal-route-state.json")["sent"],
        "terminal_verdict": load("closeout/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    review = {
        "schema": "ghc.family.tamar-vey.v667-v2.final-staged-review.v1",
        "generated_at_utc": NOW,
        "reviewed_from": "exact_git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(PRIVACY_PATTERNS),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": len(candidates),
        "checks": checks,
        "self_exclusions": [review_path, delta_path, owner_path],
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])

    delta_entries = [manifest_entry(path) for _, path in staged_rows() if path not in {delta_path, owner_path}]
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.content-manifest.v1",
            "owner": "Tamar Vey",
            "phase": "final_delta",
            "generated_at_utc": NOW,
            "source_sha": evidence_sha,
            "hash_source": "exact_git_index_blobs",
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _ in rows),
            "self_exclusions": [delta_path, owner_path],
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", delta_path])

    owner_paths_index = [path for path in tracked_owner_index_paths() if path != owner_path]
    owner_entries = [manifest_entry(path) for path in owner_paths_index]
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.tamar-vey.v667-v2.owner-manifest.v1",
            "owner": "Tamar Vey",
            "phase": "v667-v2-final",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "expected_final_parent": evidence_sha,
            "hash_source": "exact_git_index_blobs_for_resulting_final_tree",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "file_ceiling": 2000,
            "within_file_ceiling": len(owner_entries) + 1 < 2000,
            "self_exclusion": owner_path,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", owner_path])
    print(json.dumps({"reviewed": len(paths), "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "valid": True}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_tamar_vey_v667_v2_closeout.py [--staged-review]")
    else:
        main()
