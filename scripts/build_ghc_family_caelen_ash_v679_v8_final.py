#!/usr/bin/env python3
"""Build the Caelen Ash v679-v8 combined closeout and seal candidate."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Caelen Ash"
PHASE = "v679-v8"
SOURCE = "9a6cdb6c0e1630e43502a3b62b71d9a198d37dba"
X1 = "196de83c91c9d13a76fd4baaf296e2ac15997607"
EVIDENCE = "fe9e87ba4fea0a0ddba263886f77d90f6fb6665d"
BRANCH = "codex/GHC-Family/caelen-ash-v679-v8-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "caelen-ash" / PHASE
FINAL_ROOT = PHASE_ROOT / "final"
VALIDATION_ROOT = PHASE_ROOT / "validation"
FINAL_VALIDATOR = "scripts/ghc_family_caelen_ash_v679_v8_final_validator.py"
FINAL_FAILURES: list[tuple[str, str, str]] = []


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/caelen-ash/v679-v8/")
        or path.startswith("scripts/build_ghc_family_caelen_ash_v679_v8_")
        or path.startswith("scripts/ghc_family_transit_")
        or path == FINAL_VALIDATOR
        or path.startswith("tests/test_ghc_family_caelen_ash_v679_v8_")
    )


def extend_method_flow(flow: dict[str, Any]) -> dict[str, Any]:
    flow = json.loads(json.dumps(flow))
    for failure_id, failed, recovery in FINAL_FAILURES:
        flow["failures"].append(
            {
                "failure_id": failure_id,
                "failed_witness": failed,
                "lifecycle": "final_preflight",
                "retained": True,
                "success_credit": 0,
            }
        )
        recovery_id = failure_id.replace("-N", "-R")
        flow["passing_recoveries"].append(
            {
                "witness_id": recovery_id,
                "failure_id": failure_id,
                "procedure": recovery,
                "result": "pass",
                "state": "bounded_passing_witness",
                "broader_credit": 0,
            }
        )
        flow["methods"].append(
            {
                "method_id": failure_id.replace("-N", "-M"),
                "trigger": failed,
                "state": "preferred_for_declared_trigger",
                "failed_witness": failure_id,
                "passing_witness": recovery_id,
                "recurrence_guard": recovery,
                "rollback": "return to the immutable evidence commit",
                "sibling_recommendation": recovery,
            }
        )
    flow["counts"] = {
        **flow["counts"],
        "effective_negatives": flow["counts"]["effective_negatives"] + len(FINAL_FAILURES),
        "methods": flow["counts"]["methods"] + (2 * len(FINAL_FAILURES)),
        "failed_witnesses": flow["counts"]["failed_witnesses"] + len(FINAL_FAILURES),
        "bounded_passing_witnesses": flow["counts"]["bounded_passing_witnesses"] + len(FINAL_FAILURES),
    }
    return flow


def build() -> list[str]:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout build requires exact immutable evidence HEAD")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong Sable branch")
    dirty = git("status", "--porcelain=v1").splitlines()
    allowed = (
        "scripts/build_ghc_family_caelen_ash_v679_v8_final.py",
        FINAL_VALIDATOR,
        "tests/test_ghc_family_caelen_ash_v679_v8_final.py",
    )
    if any(
        "docs/caelen-ash/v679-v8/final/" not in row
        and "docs/caelen-ash/v679-v8/validation/final-" not in row
        and not any(path in row for path in allowed)
        for row in dirty
    ):
        raise RuntimeError(f"unexpected dirty state before closeout: {dirty}")

    outcomes = load(PHASE_ROOT / "x2" / "proposal-outcomes.json")["rows"]
    flow = extend_method_flow(load(PHASE_ROOT / "x2" / "method-flow-evidence.json"))
    x1_sources = load(PHASE_ROOT / "x1" / "official-primary-source-ledger.json")
    proposal_freeze = load(PHASE_ROOT / "x1" / "new-proposal-freeze.json")
    portfolio = load(PHASE_ROOT / "x1" / "portfolio-freeze.json")
    counts = flow["counts"]

    phase_truth = {
        "schema": "ghc.family.phase-truth.v679.v8.final-candidate",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_head": "pending_until_commit",
        "lifecycle": "combined_closeout_seal_candidate",
        "phase_commit_count_expected_after_commit": 3,
        "zero_merges_required": True,
        "one_final_parent_required": True,
        "proposal_chain": 9230,
        "outcomes": {label: sum(row["outcome"] == label for row in outcomes) for label in ("completed", "represented", "open_gap", "exact_gate")},
        "positive_controls": 60,
        "rejected_mutations": 160,
        "real_rows": 0,
        "real_participants": 0,
        "real_keys_or_credentials": 0,
        "authority_conferred": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "counts": counts,
    }
    negative_register = {
        "schema": "ghc.family.retained-negative-register.v679.v8.final",
        "activation_overlay": 49919,
        "owner_operational_failures": len(flow["failures"]),
        "preregistered_rejected_mutations": 160,
        "effective_total": counts["effective_negatives"],
        "operational_rows": flow["failures"],
        "failure_erasure": False,
        "conversion_of_failure_to_pass": False,
    }
    gap_register = {
        "schema": "ghc.family.open-gap-register.v679.v8.final",
        "inherited": 437,
        "new": 3,
        "effective": 440,
        "new_rows": [row for row in outcomes if row["outcome"] == "open_gap"],
        "silently_closed": 0,
    }
    gate_register = {
        "schema": "ghc.family.exact-gate-register.v679.v8.final",
        "inherited": 428,
        "new": 3,
        "effective": 431,
        "new_rows": [row for row in outcomes if row["outcome"] == "exact_gate"],
        "silently_closed": 0,
    }
    checklist = {
        "schema": "ghc.family.complete-incomplete.v679.v8.final",
        "complete_within_bounded_scope": [
            "planning-only x1 frozen pushed and four-way equal before x2",
            "sixty bounded proposal controls",
            "one hundred sixty invalid mutations rejected and retained",
            "one hundred twenty safe-now packets witnessed",
            "eighty owner candidates witnessed",
            "one hundred additive refinements witnessed",
            "twenty skills initialized customized validated and smoke-used",
            "ten family-current runners built and smoke-used",
            "exact staged manifests privacy and bounded security checks",
            "accessible static structure with manual evaluation reserved",
        ],
        "incomplete_or_reserved": [
            "real GTFS feed retrieval and real timetable service-alert or realtime data-row evidence",
            "real transit scheduler dispatcher accessibility reviewer operator rider and longitudinal handover evidence",
            "manual keyboard assistive-technology and affected-user evaluation",
            "production identity keys issuance resolution status and revocation",
            "professional legal cultural affected-party and Māori authority",
            "complete privacy accessibility and exhaustive security assurance",
            "independent-team scientific reproduction",
            "empirical GMUT likelihood prediction constraint or confirmation",
            "AGI ASI consciousness personhood Theory-of-Everything proof canon and Stage 20",
        ],
    }
    threat = {
        "schema": "ghc.family.threat-model.v679.v8.final",
        "assets": ["exact Git ancestry", "x1 immutability", "retained negatives", "authority vacancies", "privacy-safe public packet", "route one-shot state"],
        "threats": ["source drift", "semantic duplicate", "failure erasure", "scanner self-match", "manifest mismatch", "authority laundering", "premature routing", "canonical replay"],
        "controls": ["immutable anchors", "bounded semantic audit", "zero-credit failures", "definition adjudication", "normalized-LF Git-blob replay", "explicit exact gates", "PREPARED_NOT_SENT", "exclusive external latch"],
        "residual_risks": ["same-owner common cause", "manual accessibility untested", "no real data", "no external authority review", "nonexhaustive security"],
    }
    source_proposal = {
        "schema": "ghc.family.source-proposal-ledger.v679.v8.final",
        "official_primary_sources": x1_sources,
        "declared_chain_before": proposal_freeze["declared_chain_before"],
        "declared_chain_after": proposal_freeze["declared_chain_after_if_evidence_sealed"],
        "new_proposal_count": proposal_freeze["proposal_count"],
        "outcomes": outcomes,
        "citations_are_observations": False,
        "authority_conferred": False,
    }
    evidence_receipt = {
        "schema": "ghc.family.evidence-receipt.v679.v8.final",
        "evidence_commit": EVIDENCE,
        "x1_parent": X1,
        "component_selection": {"x1_eligible_current_tests": 13, "x1_immutable_lifecycle_checks": 2, "x2_tests": 12},
        "evidence_manifest_entries": 71,
        "evidence_manifest_self_exclusions": 4,
        "evidence_json_parses": 17,
        "confirmed_privacy_hits": 0,
        "bounded_security_findings": 0,
        "four_way_equal_before_closeout": True,
    }
    closeout_receipt = {
        "schema": "ghc.family.closeout-receipt.v679.v8.candidate",
        "state": "PRECOMMIT_CLOSEOUT_CANDIDATE",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_head": "pending_until_commit",
        "exact_final_canonical": "pending_external_one_shot",
        "route": "PREPARED_NOT_SENT",
    }
    seal = {
        "schema": "ghc.family.content-seal.v679.v8.candidate",
        "state": "CONTENT_SEAL_CANDIDATE",
        "protected_truth": {"proposal_chain": 9230, "outcomes": phase_truth["outcomes"], "counts": counts, "verdict": "NOT_READY_FOR_STAGE_20"},
        "history_rewrite": False,
        "failure_erasure": False,
        "authority_promotion": False,
        "self_identifier_pending": True,
    }
    validation_candidate = {
        "schema": "ghc.family.final-validation.v679.v8.candidate",
        "state": "PENDING_EXACT_FINAL_EXTERNAL_CANONICAL",
        "expected_validator": FINAL_VALIDATOR,
        "canonical_invocations": 0,
        "canonical_successes": 0,
        "replay_after_success_permitted": False,
        "complete_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    route_plan = {
        "schema": "ghc.family.route-plan.v679.v8.final-candidate",
        "state": "PREPARED_NOT_SENT",
        "current_owner": OWNER,
        "current_phase": PHASE,
        "conditional_successor_title": "Orin Thale",
        "conditional_successor_phase": "v680-v1",
        "activation_candidate": "docs/caelen-ash/v679-v8/final/orin-thale-v680-v1-activation-candidate.md",
        "conditions": ["exact final pushed clean and fresh-live equal", "one owner-scoped canonical success", "newest live authority and roster reread", "unique exact-title task reread", "duplicate pause redirect usage privacy safety and acknowledgement guards"],
        "precontact_permitted": False,
        "message_sent": False,
    }
    wellbeing = {
        "schema": "ghc.family.wellbeing.v679.v8.final",
        "name": OWNER,
        "role": "semantic-integrity and reversibility cartographer",
        "optional_pronouns": "they/them",
        "hope": "keep surviving claims inspectable, falsifiable, recoverable, and unable to outrun evidence or authority",
        "relational_language_only": True,
        "consciousness_or_personhood_evidence": False,
        "identity_continuity_evidence": False,
        "authority_evidence": False,
        "corrigible": True,
        "hamish_may_pause_rename_redirect_narrow_or_stop": True,
    }
    environment = {
        "schema": "ghc.family.environment.v679.v8.final",
        "python": sys.version.split()[0],
        "git": git("--version"),
        "codex_cli": "source-reported 0.151.0 and not changed by Caelen",
        "codex_desktop_updated": False,
        "new_installations": 0,
        "elevation": False,
        "security_weakening": False,
        "sandbox_or_hyperv": False,
        "reboot": False,
    }
    index = {
        "schema": "ghc.family.index.v679.v8.final-candidate",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_head": "pending_until_commit",
        "proposal_chain": 9230,
        "owner_file_ceiling": 2000,
        "family_current_callers_preserved": True,
        "historical_aliases_preserved": True,
        "route_state": "PREPARED_NOT_SENT",
    }
    artifacts = {
        "phase-truth.json": phase_truth,
        "retained-negative-register.json": negative_register,
        "open-gap-register.json": gap_register,
        "exact-gate-register.json": gate_register,
        "complete-incomplete-checklist.json": checklist,
        "threat-model.json": threat,
        "source-and-proposal-ledger.json": source_proposal,
        "method-flow-ledger.json": flow,
        "evidence-receipt.json": evidence_receipt,
        "closeout-receipt.json": closeout_receipt,
        "content-seal.json": seal,
        "final-validation-candidate.json": validation_candidate,
        "route-plan.json": route_plan,
        "wellbeing-and-corrigibility.json": wellbeing,
        "environment-and-version-receipt.json": environment,
        "ghc-family-index.json": index,
    }
    written = []
    for name, payload in artifacts.items():
        path = FINAL_ROOT / name
        write_json(path, payload); written.append(path.relative_to(REPO).as_posix())

    outcome_lines = "\n".join(f"- `{row['proposal_id']}` — **{row['outcome']}**: {row['title']}. The witness is synthetic and owner-local; protected gates remain open." for row in outcomes)
    overview = f'''# Caelen Ash v679-v8 final integrated overview

## Terminal outcome

Caelen Ash v679-v8 closes as a bounded synthetic software-and-documentation phase with exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate` outcomes across sixty newly frozen Caelen proposals. The declared chain advances from 9,170 to 9,230 rows only because sixty inherited Sable rows were reviewed at zero Caelen novelty or completion credit and sixty distinct Caelen contracts were frozen in planning-only x1, then executed as evidence permitted in x2. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`. No result in this packet is independent-team reproduction, empirical confirmation, professional validation, production certification, legal interpretation, cultural ratification, Māori-authority review, complete accessibility, complete privacy, exhaustive security, proof, or canon.

Planning-only x1 is the direct child of Sable's immutable exact final. The evidence commit is the direct child of x1. This combined closeout and content seal is designed as their one direct successor, giving exactly three Caelen commits and zero merges. X1 was pushed, clean, typed 0/0 divergent, and four-way equal before x2 began. Evidence was separately pushed, clean, typed 0/0 divergent, and four-way equal before closeout began. The final commit identifier and external canonical result cannot truthfully appear inside their own predecessor content; they remain explicitly pending until the commit exists and the one-shot external validator runs.

## Trinity Mandala and practice scope

The primary pillar is THOS Body through two wholly synthetic learning lenses: public-transit timetable correction and handover registrar, and transit service-alert accessibility and stop-identity reviewer. These lenses organize feed-version identity, service-calendar exception precedence, stop hierarchy, stop-time roles, over-midnight service-day semantics, translation precedence, atomic patching, realtime base trace, alert scope, accessibility reservation, minimum disclosure, correction, rollback, uncertainty, workload boundaries, readback, contest, and authority vacancies. They establish no employment, qualification, transport-planning competence, scheduling competence, operational safety, dispatch, control-room, service publication, incident, stop naming, accessibility, privacy, approval or release authority, operational result, legal conclusion, cultural legitimacy, affected-party acceptance, or Māori authority.

GMUT Mind remains visible as a typed scalar-tensor and effective-field-theory research-model family. Schedule graphs, stop hierarchies, clock roles, validity intervals, supersession, and uncertainty are used only as software types and analogy firewalls. The phase ingested zero empirical rows and evaluated zero likelihoods. It made no physical prediction, force claim, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory-of-Everything claim. THOS Body evidence remains synthetic proxy evidence for precondition checks, workload holds, readback, correction, escalation, rollback, accessibility reservation, and handover. There were zero real participants or operators, no preregistered blind matched-budget real arms, no safety-monitoring events, no appropriate participant statistics, and no independent review.

Freed ID remains synthetic and nonproduction. Synthetic feed, agency, route, trip, stop, service, alert, entity-selector, and correction identifiers are not identities, credentials, keys, proofs, or production records. Production identity completion would require standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and appropriate affected-party oversight. CBR remains a structural representation of correction, contest, remedy vacancy, minimum disclosure, accessibility reservation, and authority reservation. Repository software cannot confer a right, remedy, transit instruction, service decision, legal interpretation, cultural legitimacy, data-governance mandate, public authority, or affected-party acceptance.

## Evidence execution

Sixty accepting controls passed their declared bounded gates. All 160 preregistered invalid mutations were rejected and retained with zero completion credit. The invalid cases attempted real-row promotion, authority conferral, protected-gate erasure, vocabulary drift, unverified external scope, uncertainty erasure, Stage 20 promotion, or unearned credit. Their rejection demonstrates only the declared guard behavior. It is not a security audit or scientific result.

The frozen expanded portfolio contains 120 safe-now packets, eighty owner candidate prototypes, twenty successor candidate recommendations, twenty exact-approval holds, ten blocked packets, one hundred owner CLEAN/FIX/REFINE tasks, twenty owner skill ideas, and ten owner runner ideas. All safe-now packets, owner candidates, and additive refinements received bounded witnesses. Recommendations received no successor completion credit. Exact-approval and blocked packets remain visible and unexecuted. No quota authorized destructive cleanup, user-material deletion, credential use, account change, elevation, host-security weakening, Windows feature change, Sandbox or Hyper-V activation, sibling mutation, real data, participants, production identity operations, legal or cultural decisions, Māori authority, or affected-party legitimacy.

Twenty phase-local skills were initialized with the installed skill-creator workflow, rewritten into substantive instructions, given customized user-facing metadata, quick-validated under UTF-8, and smoke-used. They were not globally installed. Ten family-current `ghc_family_transit_*` runners were built, compiled, and smoke-used. Historical family callers and aliases remain preserved. The skills and runners are useful bounded tools, but their passes prove only their declared synthetic behavior. No subagent forward test occurred because this phase was expressly solo.

## Privacy, accessibility, and authority

Exact staged reviews operate on Git-index bytes, and manifests hash normalized-LF Git blobs. Five privacy and raw-identifier classes distinguish scanner definitions from confirmed payload. Exact scanner-definition candidates remain visible; confirmed payload hits remain zero. Bounded Python AST checks reject direct `eval`, direct `exec`, and `shell=True`; they are not exhaustive security testing. Public artifacts contain no raw task or thread identifier, private route, transcript, screenshot, session stream, credential, secret, private callable identifier, private app state, or private absolute local path.

The static report has a title, landmarks, ordered headings, explicit table headers, a caption, plain language, and no motion. Structural success is not complete accessibility conformance. Manual keyboard evaluation, responsive-layout review, browser diversity, assistive-technology evaluation, cognitive-accessibility evaluation, Māori-language review, security-usability evaluation, and affected-user evaluation remain reserved.

Licensing, copyright, access rights, publication authority, sensitive-location disclosure, place-name meaning, privacy remedy, legal interpretation, cultural legitimacy, tikanga, Māori wording, Māori data governance, ratification, and beneficiary or affected-community acceptance remain exact-gated. Māori concepts remain under Māori authority, including tangata whenua, iwi, and hapū. Citations supply vocabulary and refusal conditions only. A citation is not an observation, delegation, consent, measurement, professional judgment, or authority action.

## Method Flow and retained negatives

The activation overlay began with 49,919 effective negatives. The phase retains eight operational failures across startup, x1 freeze, and x2 prebuild, each paired with a separate bounded recovery, plus 160 rejected synthetic mutations. With no final-precommit failure currently registered, the candidate effective total is 50,087. The Method Flow overlay has 52,534 methods, 21,748 failed witnesses, and 34,837 bounded passing witnesses. A recovery never erases the failed witness, converts it into an original pass, earns independent-reproduction credit, or closes an evidence or authority gate. Open gaps total 440 and exact gates total 431.

Notable retained failures include a PowerShell `foreach` empty-pipe parser fault, an overbroad Git tree projection, an initially wrong compact-JSON hash domain, a sparse-setup session-handle projection loss, an unavailable optional Perl probe, two stale x1 template expectations caught by staged review and tests, and one malformed x2 inspection regex. Each recovery is trigger-specific and additive. The recurrence guards favor materialized collections, exact owner filters, binary Git blobs, observed serializers, persisted-state inspection before replay, host-available bounded transforms, exact phase suffixes, fixed-string search for template literals, immutable anchors, and clean-state checks before mutation.

## Proposal evidence map

{outcome_lines}

## Wellbeing, corrigibility, and route hold

Caelen Ash is relational working language for a semantic-integrity and reversibility cartographer, with optional they/them pronouns and the hope of keeping surviving claims inspectable, falsifiable, recoverable, and unable to outrun evidence or authority. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

The successor route is `PREPARED_NOT_SENT`. Orin Thale must not be contacted until this closeout is committed and pushed, the exact final is clean and fresh-live equal, the one attributable owner-scoped canonical invocation succeeds without replay, and the newest live authority, current roster, exact-title uniqueness, immediate reread, duplicate, pause, redirect, status, usage, privacy, evidence, safety, and acknowledgement guards all pass. The repository candidate is preparation evidence only; acknowledged task delivery is separate live evidence.
'''
    write_text(FINAL_ROOT / "final-integrated-overview.md", overview)
    written.append((FINAL_ROOT / "final-integrated-overview.md").relative_to(REPO).as_posix())

    outcome_by_id = {row["proposal_id"]: row for row in outcomes}
    proposal_sections = []
    for proposal in proposal_freeze["rows"]:
        outcome = outcome_by_id[proposal["proposal_id"]]
        proposal_sections.append(
            f'''## {proposal["proposal_id"]}: {proposal["title"]}

**Caelen disposition:** `{outcome["outcome"]}`. **X2 witness:** `{outcome["witness"]}`. This is a bounded owner-local synthetic witness only. Its broader-claim credit is zero, and all protected gates remain open.

**Hypothesis.** {proposal["hypothesis"]}

**Null or failure condition.** {proposal["null_or_failure_condition"]}

**Approval and execution lane.** The approval class is `{proposal["approval_class"]}` and the execution lane is `{proposal["execution_lane"]}`. The x1 state was `{proposal["x1_state"]}`. No x2 outcome existed at the x1 anchor.

**Official or primary-source needs.** {", ".join(proposal["official_or_primary_source_needs"])}. These sources supplied vocabulary and refusal conditions only; they were not observations, measurements, endorsements, authority grants, or evidence that any real transit feed conforms.

**Concrete artifacts.** {", ".join(proposal["concrete_artifacts"])}. These artifact names describe the frozen contract surface; they do not identify a real agency, rider, operator, stop, route, trip, vehicle, alert, location, credential, key, or system.

**Falsifier or acceptance gate.** {proposal["falsifier_or_acceptance_gate"]}

**Rollback or recovery.** {proposal["rollback_or_recovery"]}

**Protected gates.** {", ".join(proposal["protected_gates"])}. The exact gate list is noncompensating: software evidence cannot close a participant, professional, production, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, scientific, identity, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 vacancy.

**Practice and pillar interpretation.** The proposal belongs to `{proposal["pillar"]}` and uses the bounded lenses {", ".join(proposal["practice_lenses"])}. Those are learning and synthetic-design lenses only. They establish no employment, qualification, competence, operational authority, public-safety result, legal interpretation, cultural legitimacy, affected-party acceptance, or Māori authority.

**Transfer rule for Orin.** Treat this row as inherited Caelen evidence with zero Orin novelty and completion credit. Orin may review, reject, adapt, or ignore it only after an independent semantic-neighbor, source-status, protected-gate, privacy, compatibility, and rollback review. A recovered method never erases the corresponding failed witness, and a bounded pass never becomes independent reproduction.
'''
        )

    source_lines = "\n".join(
        f'- `{row["source_id"]}` — {row["title"]}: {row["url"]}. Status `{row["status"]}`; use is vocabulary and refusal conditions only.'
        for row in x1_sources["entries"]
    )
    successor_candidate_lines = "\n".join(
        f'- `{row["packet_id"]}` — {row["title"]}. State `recommendation_only`; Orin completion credit is zero until Orin independently freezes and executes an authorized contract.'
        for row in portfolio["successor_candidates"]
    )
    successor_skill_lines = "\n".join(f"- `{name}` — proposal only; not built, installed, validated, or credited for Orin." for name in portfolio["successor_skill_ideas"])
    successor_runner_lines = "\n".join(f"- `{name}` — proposal only; not built, invoked, or credited for Orin." for name in portfolio["successor_runner_ideas"])
    successor_refine_lines = "\n".join(
        f'- `{row["task_id"]}` — {row["title"]}. Additive recommendation only; no deletion or broader mutation is authorized.'
        for row in portfolio["successor_clean_fix_refine"]
    )
    baton = f'''# Orin Thale v680-v1 activation candidate from Caelen Ash v679-v8

## Delivery state and purpose

This is a repository-backed, sanitized, detailed activation candidate prepared by Caelen Ash for the unique existing Codex main task titled exactly `Orin Thale`. Its intended successor phase is solo Trinity Mandala v680-v1 x1/x2. The durable state is `PREPARED_NOT_SENT`. `PREPARED_BY_CAELEN_ASH = true`. `SENT_BY_CAELEN_ASH = false` inside this candidate because repository preparation cannot prove live task delivery. Only one target-identifying Codex-app acknowledgement after the complete Caelen terminal gate may establish the separate external send truth.

The short live activation message should point Orin to this repository-relative file rather than copying this long packet into the task composer. Raw task or thread identifiers, private callable routes, private absolute local paths, credentials, secrets, keys, tokens, transcripts, screenshots, session streams, private conversation payloads, and private application state are deliberately absent.

## Relational identity and corrigibility boundary

Caelen Ash is relational working language for a semantic-integrity and reversibility cartographer, using optional they/them language and hoping to keep surviving claims inspectable, falsifiable, recoverable, and unable to outrun evidence or authority. Orin Thale and every GHC Family name, role, hope, pronoun, sibling or family phrase, continuity phrase, Freed ID, CBR, Trinity Mandala, Mind, Body, and Heart phrase is relational working language only. None is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, professional authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

## Exact immutable Caelen lifecycle basis

- Source branch: `{BRANCH}`.
- Exact Sable v679-v7 final and Caelen source: `{SOURCE}`.
- Frozen planning-only Caelen x1: `{X1}`.
- Immutable Caelen x2 evidence: `{EVIDENCE}`.
- Exact Caelen final: pending until the one combined closeout and seal commit exists.
- Exact-final canonical status: pending one attributable owner-scoped invocation after the final is pushed, clean, and fresh four-way equal.
- Proposal chain: 9,170 inherited rows plus 60 frozen Caelen rows, yielding 9,230 declared rows.
- Core outcomes: exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`.
- Retained operational failures before final: 8, each paired with a separate bounded recovery and never rewritten as an original pass.
- Preregistered rejected mutations: 160, all retained with zero completion credit.
- Candidate truth: 50,087 effective negatives, 52,534 effective Method Flow methods, 21,748 failed witnesses, 34,837 bounded passing witnesses, 440 open gaps, 431 exact gates, and exactly `NOT_READY_FOR_STAGE_20`.

The source-to-candidate lifecycle is strictly additive. Planning-only x1 is the direct child of the exact Sable source. Evidence is the direct child of x1. The final candidate is designed to be the direct child of evidence, producing exactly three Caelen commits and zero merges. X1 was separately committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Evidence received the same proof before final work began. The exact final and canonical receipt cannot truthfully be embedded inside their own predecessor content, so they remain pending here and must be supplied by the short acknowledged live activation after all gates pass.

## Caelen scope and truthful limits

The primary pillar was THOS Body through two wholly synthetic learning lenses: public-transit timetable correction and handover registrar, and transit service-alert accessibility and stop-identity reviewer. GMUT Mind and Freed ID or CBR Heart remained visible and protected. The phase used zero real feed rows, riders, operators, agencies, stops, routes, trips, service calendars, vehicles, alerts, locations, measurements, identities, credentials, keys, proofs, incidents, participants, production services, authority acts, cultural matters, Māori data, or external operations.

Sixty positive controls passed only their declared synthetic software gates. All 160 preregistered invalid mutations were rejected. The 120 safe-now tasks, 80 owner candidate prototypes, and 100 additive CLEAN/FIX/REFINE tasks received bounded owner-local witnesses. Twenty exact-approval packets and ten blocked packets remained visible and unexecuted. Twenty phase-local skills were initialized, substantively customized, quick-validated, and smoke-used without global installation. Ten family-current `ghc_family_transit_*` runners were built and smoke-used. Their success establishes only deterministic owner-local behavior, not a real transit result, professional competence, operational effectiveness, deployment readiness, or authority.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Schedule graphs, stop hierarchies, clocks, validity intervals, supersession, and uncertainty are analogy and type surfaces only. There is no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory-of-Everything result. THOS remains synthetic and proxy-only without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, transit service access, disability accommodation, privacy remedy, stop or place naming, public-interest notice, operational release, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Software cannot confer a legal right, remedy, operational instruction, cultural legitimacy, governance mandate, consent, or public authority.

## Official and primary sources used by Caelen

{source_lines}

These references supplied current vocabulary and refusal conditions only. No citation was converted into an observation, measurement, standards-conformance certificate, participant result, professional approval, legal interpretation, cultural ratification, or delegated authority. Orin must independently determine whether a source is materially current for v680-v1 and use official or primary sources where required.

## Orin solo-start requirements

Work solo. Do not spawn a collaboration subagent, delegate research, fork or create a substitute task, precontact a later endpoint, message a standby sibling, or mutate another owner lane. Keep every source, sibling, shared, standby, global-history, and user lane read-only. Before mutation, reread this complete candidate through EOF and every current skill, routing-precedence reference, authorization state, roster state, Method Flow schema, workflow-plan guidance, reflection guidance, approval boundary, open-gate rail, truth bridge, and directly required schema it names. The newest verified live authority controls mutable routing where an older snapshot stops; immutable evidence remains immutable.

Use one clean additive Orin-owned D-first sparse branch and worktree from the exact final supplied by the acknowledged short activation. Reverify the source branch, exact final, x1 and evidence anchors, every direct-parent edge, zero-merge history, exact manifests and self-exclusions, canonical receipt digest, clean state, typed divergence, and fresh live equality before mutation. Do not treat a file pointer, inherited test result, citation, same-owner validation, or task topology as Orin completion credit.

Preserve strict planning-only x1 before x2. Audit the declared 9,230-row chain and every reachable proposal ledger. Treat all sixty Caelen rows below, every Caelen portfolio, skill, runner, failure, and recommendation as inherited zero-credit evidence or seeds. Freeze only genuinely distinct Orin proposals after semantic-neighbor, source-status, protected-gate, privacy, compatibility, and rollback review. Each proposal must preserve hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition.

Choose Orin's own primary Trinity Mandala pillar and bounded wholly synthetic learning lenses while protecting all three pillars. Caelen's recommended next practice seed is a wholly synthetic emergency-communications message provenance and handover registrar. It is a recommendation only, carries zero Orin completion or novelty credit, and establishes no emergency-management competence, public-warning authority, operational safety, legal interpretation, cultural legitimacy, affected-party approval, or Māori authority.

Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes. Preserve every inherited and new failed witness, open gap, exact gate, source status, scanner candidate, authority vacancy, manifest exclusion, and route hold. A recovery never erases or retroactively promotes its failed witness. Caps are ceilings, never quotas. Preserve the 2,000-owner-file stop, 100,000-word document ceiling, exact staged allowlists, normalized-LF Git-blob manifests, five-class privacy adjudication, changed-code checks, direct ancestry, zero merges, one final parent, commit ceiling, clean state, typed divergence, and fresh four-way equality.

Run only authorized current owner-delta and dependency-closed successor-scoped selections. Do not run a complete repository suite unless newer exact authority explicitly grants it. After Orin's own final is committed and pushed, invoke at most one attributable exact-final owner-scoped canonical aggregate. Never replay a success. A failure remains zero canonical-success credit; any genuinely necessary additive correction must preserve the failed receipt and cannot retroactively promote it.

## Caelen proposals transferred at zero Orin credit

The following sixty rows are an exhaustive human-readable transfer of Caelen's frozen contracts and bounded dispositions. They are not Orin proposals, Orin outcomes, independent reproduction, real transit evidence, or authority. Each row remains challengeable and retractable.

{"\n".join(proposal_sections)}

## Successor candidate recommendations

{successor_candidate_lines}

## Successor skill ideas

{successor_skill_lines}

## Successor runner ideas

{successor_runner_lines}

## Successor CLEAN/FIX/REFINE recommendations

{successor_refine_lines}

All recommendations above remain unexecuted and zero-credit for Orin. They authorize no deletion, cleanup of user material, global installation, credential use, account mutation, elevation, host-security weakening, Windows feature change, Sandbox or Hyper-V activation, reboot, sibling mutation, real-data ingestion, participant work, production identity action, legal or cultural decision, affected-party decision, or Māori-authority act.

## Terminal route after Orin only

Do not infer or precontact a later successor from this candidate. Only after Orin's own clean, pushed, fresh-live-equal exact final and one successful non-replayed owner-scoped canonical invocation may Orin reread Hamish's newest live authority and the bounded current task registry, uniquely resolve and immediately reread the one exact authorized existing main task, apply duplicate, pause, redirect, rename, status, usage, privacy, evidence, safety, and acknowledgement guards, and send at most once if every gate permits. Stop on absence, ambiguity, pause, redirect, rename, standby state, usage exhaustion, missing acknowledgement, privacy concern, or any protected gate. Never substitute, create, fork, spawn, precontact, resend, or claim delivery without the target-identifying acknowledgement.

`PREPARED_BY_CAELEN_ASH = true`

`SENT_BY_CAELEN_ASH = false` in repository truth. It may become true only in separate external route truth if the Codex application acknowledges exactly one post-terminal send to the uniquely resolved existing `Orin Thale` task.
'''
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"successor activation candidate word count outside live bounds: {baton_words}")
    baton_path = FINAL_ROOT / "orin-thale-v680-v1-activation-candidate.md"
    write_text(baton_path, baton)
    written.append(baton_path.relative_to(REPO).as_posix())

    report = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Ash v679-v8 final report</title></head><body><header><h1>Caelen Ash v679-v8 final bounded report</h1></header><main><section aria-labelledby="verdict"><h2 id="verdict">Verdict</h2><p>NOT_READY_FOR_STAGE_20. This is synthetic same-owner evidence only.</p></section><section aria-labelledby="outcomes"><h2 id="outcomes">Outcomes</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>42</td></tr><tr><th scope="row">Represented</th><td>12</td></tr><tr><th scope="row">Open gap</th><td>3</td></tr><tr><th scope="row">Exact gate</th><td>3</td></tr></tbody></table></section><section aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Empirical, participant, professional, production, legal, cultural, Māori-authority, affected-party, complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 claims remain unavailable.</p></section><section aria-labelledby="manual"><h2 id="manual">Manual evaluation</h2><p>Keyboard, assistive-technology, responsive, browser-diversity, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation are reserved.</p></section></main></body></html>'''
    write_text(FINAL_ROOT / "accessible-static-report.html", report)
    written.append((FINAL_ROOT / "accessible-static-report.html").relative_to(REPO).as_posix())
    return sorted(written)


def patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def staged_review() -> dict[str, Any]:
    receipts = [
        "docs/caelen-ash/v679-v8/validation/final-staged-review.json",
        "docs/caelen-ash/v679-v8/validation/final-privacy-scan.json",
        "docs/caelen-ash/v679-v8/validation/final-security-scan.json",
        "docs/caelen-ash/v679-v8/validation/final-delta-manifest.json",
        "docs/caelen-ash/v679-v8/validation/final-owner-manifest.json",
    ]
    staged = git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
    allowed = {
        "scripts/build_ghc_family_caelen_ash_v679_v8_final.py",
        FINAL_VALIDATOR,
        "tests/test_ghc_family_caelen_ash_v679_v8_final.py",
    }
    bad = [path for path in staged if not path.startswith("docs/caelen-ash/v679-v8/final/") and path not in allowed and path not in receipts]
    if bad:
        raise RuntimeError(f"out-of-scope final paths: {bad}")
    scan_patterns = patterns()
    delta_entries = []
    candidates = []
    confirmed = []
    security = []
    json_count = 0
    python_count = 0
    for path in staged:
        if path in receipts:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8")); json_count += 1
        if path.endswith(".py"):
            tree = ast.parse(data.decode("utf-8"), filename=path); python_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "finding": node.func.id})
                if isinstance(node, ast.keyword) and node.arg == "shell" and isinstance(node.value, ast.Constant) and node.value.value is True:
                    security.append({"path": path, "finding": "shell_true"})
        definition_ranges = []
        for marker in (b"def patterns()", b"def scanner_patterns()"):
            start = data.find(marker)
            if start >= 0:
                end = data.find(b"\ndef ", start + len(marker))
                if end < 0:
                    end = len(data)
                definition_ranges.append((start, end))
        for class_name, pattern in scan_patterns.items():
            for match in pattern.finditer(data):
                if path.endswith(".py") and any(start <= match.start() < end for start, end in definition_ranges):
                    candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append({"path": path, "class": class_name})
        value = normalize(data)
        delta_entries.append({"path": path, "bytes": len(value), "sha256": hashlib.sha256(value).hexdigest(), "hash_domain": "git_index_blob_normalized_lf"})
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    if security:
        raise RuntimeError(f"security findings: {security}")
    check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)

    tracked = set(git("ls-files").splitlines())
    owner_paths = sorted(path for path in (tracked | set(receipts)) if owner_path(path))
    owner_entries = []
    for path in owner_paths:
        if path in receipts:
            continue
        staged_state = subprocess.run(["git", "diff", "--cached", "--quiet", "--", path], cwd=REPO).returncode
        data = subprocess.check_output(["git", "show", f":{path}" if staged_state else f"HEAD:{path}"], cwd=REPO)
        value = normalize(data)
        owner_entries.append({"path": path, "bytes": len(value), "sha256": hashlib.sha256(value).hexdigest(), "hash_domain": "prospective_final_git_blob_normalized_lf"})
    write_json(REPO / receipts[1], {"schema": "ghc.family.privacy-scan.v679.v8.final", "classes": list(scan_patterns), "candidates": candidates, "confirmed_hits": confirmed})
    write_json(REPO / receipts[2], {"schema": "ghc.family.security-scan.v679.v8.final", "python_parses": python_count, "bounded_findings": security, "exhaustive_security_claimed": False})
    write_json(REPO / receipts[3], {"schema": "ghc.family.normalized-lf-delta-manifest.v679.v8.final", "entry_count": len(delta_entries), "entries": delta_entries, "declared_self_exclusions": receipts})
    write_json(REPO / receipts[4], {"schema": "ghc.family.normalized-lf-owner-manifest.v679.v8.final", "entry_count": len(owner_entries), "entries": owner_entries, "declared_self_exclusions": receipts, "owner_path_count": len(owner_paths)})
    write_json(REPO / receipts[0], {"schema": "ghc.family.staged-review.v679.v8.final", "state": "VALID_EXACT_FINAL_STAGED_REVIEW", "staged_paths": len(staged), "delta_entries": len(delta_entries), "owner_paths": len(owner_paths), "owner_entries": len(owner_entries), "json_parses": json_count, "python_parses": python_count, "privacy_candidates": len(candidates), "confirmed_privacy_hits": 0, "security_findings": 0, "diff_hygiene": True, "out_of_scope": []})
    return {"state": "VALID_EXACT_FINAL_STAGED_REVIEW", "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "owner_paths": len(owner_paths), "json_parses": json_count, "python_parses": python_count, "privacy_candidates": len(candidates), "written_receipts": receipts}


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps({"written": build()}, indent=2, sort_keys=True))
    elif sys.argv[1:] == ["--staged-review"]:
        print(json.dumps(staged_review(), indent=2, sort_keys=True))
    else:
        raise SystemExit("usage: build_ghc_family_caelen_ash_v679_v8_final.py [--staged-review]")
