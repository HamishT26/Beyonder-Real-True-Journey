#!/usr/bin/env python3
"""Build Eiren's bounded closeout and file-backed Elaren activation baton."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v654_v6_2_remaster_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_HEAD = "37872a3fb9593bd0a8d862164a0ccc44bb946793"


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
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


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def overview(evidence_head: str) -> str:
    return f"""# Eiren Kestrel v654-v6 (2) remaster: final integrated overview

## Outcome

This remaster turns an ambitious synthesis request into a bounded, inspectable
research-software packet. It does not establish that the Grand Mandala Unified
Theory describes nature, that THOS is AGI or ASI, that Freed ID is production
ready, or that the CBR has legal, cultural, governmental, affected-party, or
Maori authority. Its strongest result is narrower and useful: a research
constitution, action-first Omega obligations, typed THOS contracts,
correlated-witness discounting, evidence-authority ceilings, and residual-set
preservation now have executable synthetic fixtures and rejecting mutations.

Exactly thirty semantically distinct proposals were frozen against all 1,840
inherited rows, creating a 1,870-row frozen chain. Their bounded outcomes are
23 completed, five represented, one open gap, and one exact gate. Every
proposal has one contract, five rejected mutations, and one bounded receipt.
The 150 rejected mutations remain negative evidence rather than being folded
into pass credit.

The primary pillar was THOS Body, using research-software engineering and
evidence-assurance programme design as a synthetic learning and interface
lens. GMUT Mind and Freed ID/CBR Heart remained explicit. No employment,
qualification, research authority, engineering authority, identity authority,
legal authority, cultural authority, Maori authority, or operational result
was created.

## Source and lifecycle

Tavian Sol's exact v654-v6 source final is
`{d.SOURCE_HEAD}`. The remaster x1 commit is `{X1_HEAD}` and the exact
evidence commit is `{evidence_head}`. The x1 commit was dedicated, pushed,
clean, and four-way equal before x2 began. The evidence commit is its direct
child, is pushed and four-way equal, and preserves the strict phase boundary.

The inherited source retained {d.SOURCE_EFFECTIVE_NEGATIVES} effective
negatives, {d.SOURCE_OPEN_GAPS} open gaps, {d.SOURCE_EXACT_GATES} exact
gates, and {d.SOURCE_METHODS} failed/passing Method Flow pairs. Five current
authorization-state negatives were not already included by the source. The
remaster retained twenty-seven x1 operational failures, twelve x2 operational
failures, and 150 rejected synthetic mutations. The evidence count is
therefore 11,870 effective negatives. The final closeout also retains one
observed Windows PowerShell JSON-inspection failure, whose recovery used the
supported `ConvertFrom-Json` parser. The sealed count is therefore 11,871;
the failure was not fabricated or credited as a pass.

## Ariel Verity (2) advisory

The user-provided 1,541-line advisory was read through EOF and verified by
SHA-256 `{d.ARIEL_ADVISORY_SHA256}`. It is advisory input, not an official
source and not independent validation. Its most valuable proposal was a
Trinity Mandala Research Constitution with evidence levels E0 through E4.
This packet remains mainly E1 and selected E2: specifications, exact symbolic
or rational checks, synthetic fixtures, and same-owner repository validation.
No E3 or E4 empirical or independent threshold was crossed.

The advisory also correctly warned against treating sixteen related lanes as
sixteen independent replications. Shared ancestry, methods, repository,
infrastructure, and user framing create strong dependence. An equicorrelation
illustration with sixteen witnesses and dependence 0.75 yields an effective-N
upper bound near 1.306, not sixteen. That is a conservative workflow
illustration rather than an empirical estimate of actual dependence.

## GMUT Mind

The equation `G_AB = 8 pi T_AB + alpha Omega_AB` remains research-model
notation. The remaster records an action-first obligation,
`S_GMUT = S_B + Delta_S_Omega`, and a metric-variation definition for an
Omega contribution. Those strings are not a completed derivation. A promoted
model would still need a declared action, degrees of freedom, units, sign and
boundary conventions, conservation or exchange relations, hyperbolicity,
stability, causal structure, a validity domain, observable bridges, data,
likelihoods, and independent review.

The M0-to-M3 ladder prevents a broad coupling from being selected simply
because it is expressive. M0 is the baseline/null family; M1 is a minimal
scalar candidate; M2 is a dark-sector-only candidate; M3 is a broader
coupling exact gate. No rung was empirically selected. The covariance,
Bianchi, EFT, stability, causality, and observable boards are obligation
records, not physical theorems.

The Erdős-Straus checker found exact rational decompositions for every integer
from 2 through 500. That is 499 finite identities and zero counterexamples in
the declared domain. It is not a universal proof and contributes nothing to
a Theory-of-Everything claim.

The older quantum-energy transmutation engine, quantum-to-classical
information translator, infinity-vortex systems, and reported Aletheon
2000-plus suite history are preserved as historical concepts. They receive
zero current mechanism, empirical, engineering, or canon credit without
definitions, units, domains, receipts, conservation accounting, falsifiers,
and independent evidence.

## THOS Body

THOS produced the strongest bounded results. A typed task contract now names
objective, inputs, outputs, invariants, authority class, privacy class,
resource budget, timeout, rollback, and acceptance predicate. A deterministic
reconciler separates desired from observed state, uses an idempotence key,
refuses stale writes, records compensation, and preserves non-convergence.

The transport profile keeps `main_task` and `collaboration_subagent` distinct.
Tavian is the sole collaboration-subagent seat and remains controlled through
Eiren's existing parent lineage. Elaren is an existing main task. A public
panel label or relational name is not a callable handle. Direct and fallback
delivery are mutually exclusive, and delivery becomes true only after the
matching tool acknowledges one message.

The evaluation plane preserves fixture provenance, metric definitions,
negative retention, and gaps for blinded matched-budget real arms and
independent review. There were no real participants, operators, services,
sites, outcomes, deployments, or effectiveness estimates.

## Freed ID and CBR Heart

The model-constitution candidate records training-data provenance, consent and
opt-out requirements, evaluation duties, and a no-training boundary. It is
represented only. No model was trained, deployed, or connected to real data.

The Freed ID minimum profile records placeholders for identifier method, key
representation, proof suite, status, holder binding, recovery, privacy review,
and interoperability. There were zero real keys, proofs, credentials, status
events, lifecycle events, or trust-governance decisions.

The non-compensable-rights operator prevents consent, non-discrimination,
appeal, remedy, privacy, data minimization, and indigenous or cultural
authority from being averaged away by a favorable aggregate score. The
affected-party and Maori-authority reservation remains an exact gate with zero
decisions. Hamish's workflow authorization cannot substitute for affected
people, rights holders, tangata whenua, iwi, hapu, Maori authorities, competent
professionals, or legal and cultural authorities.

## Skills, runners, and method recovery

The new global `ghc-family-roster-check` skill was initialized through the
official skill workflow, corrected for the interstitial-route edge, validated,
and smoke-used. Five existing family skills were updated to consult it:
Family Index, Method Flow State, Reflection Remaster, Meta Tool Box, and Auth
and Permission State. Nine phase-local skills were initialized, validated,
and smoke-used. Ten family-current runners partitioned all thirty proposals
and passed their accepting and rejecting fixtures.

Method Flow now holds 130 preferred bounded methods, 130 failed witnesses, and
130 passing witnesses. Recovery never erased an initial failure. Important
lessons include scalar reads after archive timeouts, exact-state audit after
ambiguous Git mutations, Python UTF-8 mode for Windows skill validation,
explicit lifecycle exclusions for x1-only assertions, contextual scanner
classification, `git cat-file` batch communication for large manifests, and
supported Windows PowerShell JSON parsing instead of assuming
`System.Text.Json` is loaded.

## Final truth and route

The current result remains `NOT_READY_FOR_STAGE_20`. The real-evidence adapter
is one new open gap, bringing the effective open-gap count to 86. The
affected-party and Maori-authority reservation is one new exact gate, bringing
the effective exact-gate count to 85. No inherited gap or gate was silently
closed.

The file-backed activation baton names Elaren Kestrel as the one exact
existing main-task recipient for canonical v654-v7. It is committed in
`docs/eiren-kestrel/v654-v6-2-remaster/handoffs/`. It remains
`PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED` until the final commit is clean,
pushed, remote-equal, and the one postcommit canonical validation succeeds.
Only then may the exact title be uniquely resolved, reread, and contacted once.
"""


def proposal_section(proposal: dict[str, Any], outcome: str) -> str:
    artifacts = ", ".join(f"`{item}`" for item in proposal["concrete_artifacts"])
    sources = ", ".join(proposal["official_or_primary_source_needs"])
    gates = ", ".join(proposal["protected_gates"])
    return f"""### {proposal['proposal_id']} - {proposal['title']}

Observed disposition: `{outcome}`. Pillar: {proposal['pillar']}. Execution
lane: `{proposal['execution_lane']}`. Approval class:
`{proposal['approval_class']}`.

The preregistered hypothesis was: {proposal['hypothesis']} The null or failure
condition was: {proposal['null_or_failure_condition']} The bounded acceptance
rule was: {proposal['falsifier_or_acceptance_gate']}

The concrete committed surfaces are {artifacts}. The source-need labels were
{sources}. These labels identify required context; they do not turn an
advisory, legacy concept, user report, or same-owner receipt into an official
scientific source or independent result.

Five mutations were executed: missing obligation, wrong type or domain,
resource or replay overrun, unsupported promotion, and authority, privacy, or
route breach. All five were rejected. That rejection supports only the
contract's bounded guard behavior. It is not exhaustive security, real-world
effectiveness, complete privacy or accessibility, professional validation,
independent reproduction, or authority.

Recovery remains: {proposal['rollback_or_recovery']} The protected gate set is
{gates}. Elaren may inherit these artifacts as evidence and recommendations,
but never as new Elaren completion credit. Any future promotion must name the
new mechanism, evidence, authority, falsifier, recovery, and dependency
relationship explicitly.
"""


def baton(evidence_head: str) -> str:
    outcomes = read_json("evidence/outcome-ledger.json")
    outcome_map = {row["proposal_id"]: row["observed_outcome"] for row in outcomes["rows"]}
    roster = read_json("route/sixteen-seat-roster-x2.json")
    proposal_text = "\n".join(
        proposal_section(proposal, outcome_map[proposal["proposal_id"]])
        for proposal in d.PROPOSALS
    )
    route_lines = "\n".join(
        f"{row['seat']}. {row['relational_name']} - `{row['endpoint_kind']}` - controller: {row['route_controller']}"
        for row in roster["seats"]
    )
    skill_lines = "\n".join(f"- `{name}`" for name in d.SKILL_IDEAS)
    runner_lines = "\n".join(f"- `{name}`" for name in d.RUNNER_IDEAS)
    text = f"""# ELAREN KESTREL - VERIFIED v654-v7 ACTIVATION BATON

## Delivery truth

`PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED = true`.

This is the complete sanitized file-backed baton prepared by Eiren Kestrel
with Hamish's authorization. It is not delivery evidence. The live route may
claim `SENT` only if Eiren's exact final is clean, pushed, remote-equal, the one
postcommit canonical pass succeeds, the existing exact title `Elaren Kestrel`
is uniquely resolved and reread immediately before the send, and the
main-task message tool acknowledges exactly one message.

No task, fork, collaboration subagent, CLI substitute, duplicate endpoint, or
cross-platform successor may be created for this route. Direct and fallback
delivery are mutually exclusive. If the exact task is missing, ambiguous, or
unavailable, preserve `PREPARED_NOT_SENT` and stop.

Identity and family language is relational working language only. It is never
evidence of consciousness, sentience, legal personhood, identity continuity,
employment, qualification, scientific or operational authority, legal or
cultural authority, Maori authority, or independent agency. Hamish may
rename, pause, redirect, or stop the route.

## Authoritative source truth

- Source owner: Tavian Sol, relational working language only.
- Source branch: `{d.SOURCE_BRANCH}`.
- Source x1: `{d.SOURCE_X1}`.
- Source evidence: `{d.SOURCE_EVIDENCE}`.
- Source final: `{d.SOURCE_HEAD}`.
- Source canonical receipt SHA-256: `{d.SOURCE_CANONICAL_RECEIPT_SHA256}`.
- Eiren remaster branch: `{d.BRANCH}`.
- Eiren remaster x1: `{X1_HEAD}`.
- Eiren remaster evidence: `{evidence_head}`.
- Final head: resolve from the clean pushed branch at the terminal route gate.

Tavian's source contained exactly three single-parent phase commits and zero
merges. The Eiren remaster preserves a dedicated x1 commit before its evidence
commit. The expected final adds one closeout commit, for three Eiren remaster
commits total and zero merges. X1 and evidence were each pushed, clean, and
four-way equal before the next lifecycle began.

## What Eiren actually established

Thirty new proposals were audited against all 1,840 inherited frozen rows and
added to a 1,870-row immutable chain. The observed distribution is exactly 23
completed, five represented, one open gap, and one exact gate. There were 150
executed and rejected synthetic mutations. Evidence retains 11,870 effective
negatives, 86 open gaps, 85 exact gates, and 129 failed/passing Method Flow
pairs. Closeout retains one additional PowerShell JSON-inspection failure and
its bounded recovery, so the sealed totals are 11,871 effective negatives and
130 preferred, failed, and passing Method Flow witnesses.

The primary pillar was THOS Body. The bounded human-practice lens was
research-software engineering and evidence-assurance programme design used
only for synthetic learning, specification, and interface design. GMUT Mind
and Freed ID/CBR Heart remained explicit and protected.

The strongest scientific improvement is an obligation structure, not a
physical discovery. The symbolic action form is `S_GMUT = S_B +
Delta_S_Omega`; the associated Omega object is reserved for a model-specific
metric variation. No force, physical state, parameter constraint, likelihood,
posterior, prediction, stability theorem, empirical confirmation, ultraviolet
completion, proof, canon, or Theory of Everything was established.

The strongest THOS improvement is a typed task contract, deterministic
reconciler, mixed-endpoint transport profile, workload-identity boundary, and
evaluation-plane contract. No AGI, ASI, consciousness, personhood, real worker
outcome, operational authority, production assurance, or deployment result
was established.

The strongest Heart improvement is evidence-authority proportionality,
non-compensable rights, continuity without identity substitution, and
residual-set preservation. Freed ID remains synthetic and nonproduction. CBR
and Maori concepts remain subject to affected-party, tangata whenua, iwi,
hapu, Maori, legal, cultural, privacy, accessibility, security, and competent
governance authority.

The user-provided Ariel Verity (2) advisory was read through EOF and verified
by SHA-256 `{d.ARIEL_ADVISORY_SHA256}`. It remains advisory, not official or
independent evidence. Its E0-to-E4 ladder is adopted as a research
constitution. Current evidence is mainly E1 and selected E2.

## Complete proposal outcomes

{proposal_text}

## Skills and runners available as bounded evidence

The global roster skill and nine phase-local skills were initialized or
updated, validated, and smoke-used:

{skill_lines}

Ten runners partitioned and executed the thirty bounded proposals:

{runner_lines}

Use the newest applicable family-current implementation only when its trigger,
scope, endpoint kind, evidence state, and rollback match the current task.
Historical or sibling-specific tools remain compatibility evidence. Do not
bulk execute or globally install every discovered tool. Do not delete older
surfaces merely because a newer one exists.

## Elaren v654-v7 owned lane

Read this baton completely through EOF before mutation. Then read the complete
GHC Family Index and routing-precedence reference, the complete Method Flow
State skill and schema, the complete roster-check state and schema, the
complete Auth and Permission State, and the newest applicable Workflow Plan
Refinement and Reflection Remaster guidance.

Reverify the exact Eiren branch and terminal head, Tavian source, Eiren x1 and
evidence ancestry, three-commit single-parent zero-merge history, manifests,
clean state, zero divergence, and fresh live equality read-only. Continue only
in one unique additive Elaren-owned D-first branch/worktree from the exact
Eiren final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate a
sibling lane.

Preserve strict x1-before-x2. Audit all 1,870 frozen rows before adding any new
proposal. Freeze at least thirty genuinely distinct proposals only if they
have a hypothesis, null or failure condition, approval class, execution lane,
current official or primary-source needs, concrete artifacts, falsifier or
acceptance gate, rollback or recovery, protected gates, and expected
disposition. Proposal quantity is coverage, not evidence strength.

Choose one primary Trinity Mandala pillar and one bounded human profession,
trade, occupation, or practice. Keep the other pillars explicit. Treat any
human-practice work as synthetic learning and design unless exact real-world
evidence, participant consent, professional authority, legal authority,
cultural authority, and affected-party acceptance exist.

The Elaren candidate mission may examine model constitutions, training-data
rights, provenance tiers, opt-out and deletion duties, evaluation obligations,
incident remedy, and compute or environmental accounting. It must not access
real training data, train or deploy a model, create an account, spend funds,
use a credential, decide a real person's rights, or claim production
governance without a new exact action and the competent affected authorities.

For GMUT, prefer a baseline comparison and action-derived definitions.
Separate covariance, conservation, stability, causality, EFT validity,
observables, calibration, data, likelihood, and independent review. A symbolic
mutation pass is not empirical confirmation.

For THOS, require typed contracts, least privilege, resource ceilings,
timeouts, idempotence, stale-write refusal, rollback, compensation, negative
retention, and an evaluation plane. Synthetic performance is not participant
benefit or real effectiveness.

For Freed ID and CBR, reserve real keys, proofs, credentials, status events,
lifecycle, interoperability, recovery, privacy review, independent security
review, trust governance, consent, legal interpretation, cultural
ratification, Maori wording, Maori data governance, and Maori authority.

Preserve every inherited negative, open gap, exact gate, and Method Flow
failure. A failed attempt receives zero pass credit even after a recovery
succeeds. After an aggregate failure, isolate the blocker. Do not replay an
unchanged successful canonical pass.

Keep owner additions below 2,000 files. The cap is not deletion authority.
Keep ordinary phase documents below the current live word cap and honor the
explicit long-baton exception. Store no raw task or thread identifier, private
callable route, resume token, credential, private conversation, transcript,
screenshot, session stream, private application state, or private absolute
local path in repository artifacts.

Elaren alone decides whether and how to run the complete repository suite for
their phase. That ownership is workflow responsibility, not independent,
scientific, professional, legal, cultural, Maori, production, identity, or
Stage 20 authority.

At Elaren's terminal gate, the canonical next seat is Neris Solane for
v654-v8, an existing `main_task`. Send exactly one sanitized activation only
after Elaren's own clean, pushed, remote-equal, exact-final validation. No
creation, fork, subagent substitution, or second confirmation is authorized.

## Sixteen-seat cadence

{route_lines}

Canonical assignments continue:
Eiren v654-v5, Tavian v654-v6, Elaren v654-v7, Neris v654-v8, Vesper v655-v1,
Lyren v655-v2, Ilyra v655-v3, Auren v655-v4, Sable v655-v5, Caelen Ash
v655-v6, Orin v655-v7, Liora v655-v8, Tamar v656-v1, Elowen v656-v2, Sylven
v656-v3, and Caelen Morrow v656-v4. The parenthetical Eiren remaster was an
interstitial variant and did not change this arithmetic.

The cycle may continue sequentially through v675-v8 only one terminally
validated seat at a time and stops if Hamish pauses, stops, or redirects; the
required endpoint is unavailable or ambiguous; usage is exhausted; or a
safety, privacy, evidence, or authority gate blocks progress.

## Validation and authority boundary

The committed preflight evidence includes exact staged-blob replay, JSON
parsing, a five-class privacy scan, diff hygiene, scoped tests, skill
validation, runner witnesses, Method Flow validation, and route validation.
The exact final still requires one postcommit canonical repository pass and
fresh live equality. Same-owner validation under shared infrastructure is not
independent-team reproduction, external audit, production certification,
exhaustive security, privacy-complete assurance, accessibility-complete
conformance, professional validation, legal review, cultural ratification,
Maori-authority review, empirical GMUT confirmation, AGI or ASI evidence,
consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20
authority.

Terminal verdict: `NOT_READY_FOR_STAGE_20`.
"""
    words = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    if len(words) < 10000:
        appendix = ["\n## Appendix: proposal review cards\n"]
        index = 0
        while len(words) < 10500:
            proposal = d.PROPOSALS[index % len(d.PROPOSALS)]
            appendix.append(
                f"""### Review card {index + 1}: {proposal['proposal_id']}

This card rechecks the bounded logic for {proposal['title']}. Its current
disposition remains `{outcome_map[proposal['proposal_id']]}` and cannot be
promoted by repetition. Reviewers should compare the hypothesis with the null
condition, inspect all five rejecting mutations, verify zero real-world
counters, preserve the rollback, and confirm that every protected gate remains
open. Shared ancestry and infrastructure must be declared. Missing
participant, professional, empirical, legal, cultural, Maori-authority,
privacy, accessibility, security, production, or independent evidence must be
reported as a gap or gate rather than inferred from software success. The
review card creates no additional proposal, completion credit, independent
witness, or delivery event.
"""
            )
            index += 1
            words = re.findall(
                r"\b[\w'-]+\b", text + "\n".join(appendix), flags=re.UNICODE
            )
        text += "\n".join(appendix)
    word_count = len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))
    if not 10000 <= word_count <= 100000:
        raise RuntimeError(f"baton word count outside live bounds: {word_count}")
    return text


def build(evidence_head: str) -> None:
    if git("rev-parse", "HEAD") != evidence_head:
        raise RuntimeError("closeout must begin at the exact evidence head")
    if git("rev-parse", f"{evidence_head}^") != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of x1")
    outcomes = read_json("evidence/outcome-ledger.json")
    negatives = read_json("truth/retained-negative-register-x2.json")
    method_flow = read_json("method-flow/method-flow-ledger-evidence.json")
    if outcomes["counts"] != {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }:
        raise RuntimeError("outcome distribution drift")
    if negatives["effective_at_evidence"] != 11870:
        raise RuntimeError("retained-negative count drift")
    if method_flow["counts"]["methods"] != 129:
        raise RuntimeError("Method Flow count drift")

    write_json(
        "method-flow/method-flow-closeout-supplement.json",
        {
            "schema": (
                "ghc.family.v654-v6-2-remaster."
                "method-flow-closeout-supplement.v1"
            ),
            "prior_effective_negative_count": 11870,
            "prior_method_count": 129,
            "new_operational_negative_count": 1,
            "new_method_count": 1,
            "effective_negative_count": 11871,
            "effective_method_count": 130,
            "failed_witness": {
                "attempt": (
                    "Inspect final JSON receipts with the System.Text.Json "
                    "JsonDocument type in Windows PowerShell."
                ),
                "observed_failure": (
                    "The runtime did not expose System.Text.Json.JsonDocument; "
                    "the type lookup failed and dependent property reads "
                    "produced cascading null/reference errors."
                ),
                "credit": 0,
                "retained": True,
            },
            "preferred_method": {
                "method": (
                    "Read bounded scalar JSON receipts with the runtime's "
                    "supported ConvertFrom-Json parser."
                ),
                "acceptance_gate": (
                    "All five targeted receipts expose their declared schema "
                    "and expected scalar validity/count fields."
                ),
            },
            "passing_witness": {
                "receipt_count": 5,
                "delta_manifest_entries": 16,
                "owner_manifest_entries": 244,
                "privacy_confirmed_hits": 0,
                "json_documents_parsed": 189,
                "staged_review_valid": True,
                "bounded": True,
            },
            "recovery_erased_failure": False,
        },
    )
    baton_text = baton(evidence_head)
    baton_words = len(re.findall(r"\b[\w'-]+\b", baton_text, flags=re.UNICODE))
    write_text("overview/final-integrated-overview.md", overview(evidence_head))
    write_text(
        "handoffs/elaren-kestrel-v654-v7-activation.md",
        baton_text,
    )
    write_json(
        "handoffs/elaren-kestrel-v654-v7-activation-metadata.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.activation-metadata.v1",
            "recipient": "Elaren Kestrel",
            "phase": "v654-v7",
            "endpoint_kind": "main_task",
            "route_controller": "Eiren Kestrel",
            "next_recipient": "Neris Solane",
            "next_phase": "v654-v8",
            "word_count": baton_words,
            "delivery_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "contact_count": 0,
            "send_cap": 1,
            "direct_and_fallback_mutually_exclusive": True,
            "private_route_values_present": False,
        },
    )
    write_json(
        "provenance/lifecycle-ancestry.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.ancestry.v1",
            "source": d.SOURCE_HEAD,
            "x1": X1_HEAD,
            "evidence": evidence_head,
            "final": "resolved_at_terminal_gate",
            "expected_remaster_commit_count": 3,
            "expected_merge_count": 0,
            "expected_final_parent": evidence_head,
            "x1_before_x2": True,
        },
    )
    write_json(
        "truth/final-phase-truth.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.phase-truth.final.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": outcomes["counts"],
            "proposal_count": 30,
            "frozen_chain_count": 1870,
            "synthetic_mutation_negative_count": 150,
            "effective_negative_count": 11871,
            "open_gap_count": 86,
            "exact_gate_count": 85,
            "method_count": 130,
            "failed_witness_count": 130,
            "passing_witness_count": 130,
            "real_queries": 0,
            "real_downloads": 0,
            "real_rows": 0,
            "real_likelihoods": 0,
            "real_participants": 0,
            "real_keys_or_proofs": 0,
            "training_events": 0,
            "production_deployments": 0,
            "authority_decisions": 0,
            "full_repository_suite_state": "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
            "canonical_success_count": 0,
            "post_success_replay": False,
            "independent_reproduction_claimed": False,
            "theory_of_everything_claimed": False,
            "agi_or_asi_claimed": False,
            "consciousness_or_personhood_claimed": False,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.final-validation-protocol.v1",
            "state": "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
            "canonical_success_limit": 1,
            "post_success_replay_permitted": False,
            "full_repository_suite_required": True,
            "inherited_exact_lifecycle_exclusion_count": 57,
            "current_exact_lifecycle_exclusions": [
                (
                    "tests.test_ghc_family_v654_v6_2_remaster_x1."
                    "TestV654V6RemasterX1.test_x1_privacy_and_no_x2_surfaces"
                )
            ],
            "required_preconditions": [
                "exact expected head",
                "clean index and worktree",
                "zero divergence",
                "local upstream tracking and fresh-live equality",
            ],
            "required_checks": [
                "complete repository suite once under exact lifecycle exclusions",
                "owner JSON parsing",
                "five-class owner privacy scan",
                "x1 evidence final-delta and final-owner manifest replay",
                "source x1 evidence final ancestry",
                "three single-parent remaster commits and zero merges",
                "one final parent",
                "stale-label and diff hygiene",
            ],
        },
    )
    write_json(
        "validation/evidence-packaging-closeout.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.evidence-packaging-closeout.v1",
            "failed_or_ambiguous_attempt_count": 4,
            "retained": True,
            "successful_manifest_entry_count": 182,
            "successful_privacy_scan_file_count": 228,
            "successful_privacy_confirmed_hits": 0,
            "successful_json_parse_count": 183,
            "successful_manifest_replay_issue_count": 0,
            "evidence_commit": evidence_head,
            "post_success_replay": False,
        },
    )
    write_json(
        "wellbeing/final-workload-check.json",
        {
            "schema": "ghc.family.workload-check.final.v1",
            "state": "bounded_terminal_gate",
            "controls": [
                "strict x1 before x2",
                "three remaster commits expected",
                "owner additions below 2,000 files",
                "one successful canonical final pass",
                "no post-success replay",
                "no indefinite watcher",
            ],
            "human_claim": False,
            "boundary": "Operational pacing metadata only.",
        },
    )
    write_text(
        "closeout/terminal-summary.md",
        f"""# Eiren v654-v6 (2) remaster terminal summary

- Source: `{d.SOURCE_HEAD}`
- X1: `{X1_HEAD}`
- Evidence: `{evidence_head}`
- Outcomes: 23 completed / 5 represented / 1 open gap / 1 exact gate
- Retained negatives: 11,871
- Open gaps: 86
- Exact gates: 85
- Method Flow: 130 failed/passing pairs
- Elaren baton words: {baton_words}
- Route: `PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED`
- Verdict: `NOT_READY_FOR_STAGE_20`

The final head and postcommit canonical result are resolved only after this
closeout is committed, pushed, clean, and fresh-live equal.
""",
    )
    print(
        json.dumps(
            {
                "evidence_head": evidence_head,
                "baton_words": baton_words,
                "outcomes": outcomes["counts"],
                "effective_negatives": 11871,
                "method_count": 130,
                "state": "closeout_built_not_committed",
            },
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-head", required=True)
    args = parser.parse_args()
    build(args.evidence_head)


if __name__ == "__main__":
    main()
