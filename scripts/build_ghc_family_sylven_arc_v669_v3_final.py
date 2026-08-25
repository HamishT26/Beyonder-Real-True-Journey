"""Build the Sylven Arc v669-v3 closeout and prepared successor packet."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_sylven_arc_v669_v3_archive import (
    CHAIN_AFTER,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PROTECTED_GATES,
    SOURCE_FINAL,
    write_json,
    write_text,
)


EVIDENCE_COMMIT = "d5b00198c28178c5a00e5eb9ca839e08d1194ff7"
X1_COMMIT = "a8ce92245d170fa64bc4a484a0a074a9848496de"
FINAL_COUNTS = {
    "effective_negatives": 30899,
    "methods": 17004,
    "failed_witnesses": 2720,
    "passing_witnesses": 3832,
    "open_gaps": 229,
    "exact_gates": 224,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_lf_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def proposal_rows(repo: Path) -> list[dict[str, Any]]:
    return [load_json(path) for path in sorted((repo / OWNER_ROOT / "x2/proposals").glob("*.json"))]


def final_overview() -> str:
    return """# Sylven Arc v669-v3 final integrated overview

## Executive result

Sylven Arc v669-v3 completed a bounded, same-owner, synthetic evidence phase from Elowen Cairn's immutable v669-v2 final. The lane preserves a planning-only x1 commit, a separately pushed x2 evidence commit, and this additive closeout. Forty genuinely new proposal titles were compared against the exact accessible 1,420-title corpus. The declared inherited chain had 4,990 rows, but 3,570 titles were unavailable to the inherited recovery mechanism; that limitation remains an open semantic-audit recovery gap. Consequently, the phase asserts zero exact collisions and sub-threshold token-Jaccard neighbors only within the accessible corpus and makes no universal novelty claim.

The forty core outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. A completed label means only that a declared owner-local structural or software hypothesis passed its bounded synthetic acceptance gate. A represented label means a contract or obligation board exists without the evidence needed for operational, empirical, professional, or authority promotion. The two open gaps preserve a zero-call official collection adapter and absent governed human or affected-user evaluation. The two exact gates preserve ceramics professional, safety, ownership, cultural, affected-party, and Māori authority boundaries and the separate Stage 20 evidence-and-authority boundary.

## Primary pillar and practice lens

THOS Body was primary through a wholly synthetic studio-ceramics and kiln-log documentation lens. The work modeled batch and object identities, vessel topology, state vocabularies, kiln-load and schedule relations, provenance, correction, custody, workload, hazard stops, accessibility structure, and handover. This was learning and design only. It involved zero real people, studios, kilns, vessels, fragments, materials, glazes, fuels, tools, firings, sensors, observations, measurements, hazards, professional actions, or authority acts.

GMUT Mind remained a typed scalar-tensor and effective-field-theory research-model family. The phase added only heat-flow and phase-change obligation boards with explicit units, missing values, falsification requirements, zero fitted coefficients, and analogy nonconversion. It established no likelihood, constraint, prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon.

Freed ID and CBR Heart remained synthetic and nonproduction. The zero-key ceramics envelope contains explicit issuer, holder, proof, resolution, status, revocation, recovery, governance, and affected-party vacancies. The CBR challenge ladder is only a structural representation. No live key, proof, identity lifecycle, trust decision, remedy decision, privacy-complete claim, legal interpretation, cultural interpretation, affected-party acceptance, Māori wording, Māori concept, Māori data-governance act, or Māori authority act occurred.

## Flashcard architecture

Each proposal has a four-tier Freed ID flashcard: the relational owner record, the primary and protected Trinity pillars, the bounded practice lens, and the exact task. Every card contains at least twelve named sections covering identity, phase, pillar, practice, task, hypothesis, source status, artifact, evidence, failure boundary, authority boundary, and rollback. The cards are deliberately lossy working projections. The proposal freeze, outcome ledger, Method Flow ledger, retained-negative register, and gate register remain authoritative. No card is an identity certificate or evidence of consciousness, personhood, continuity, employment, qualification, agency, or authority.

## Execution and rejection evidence

Thirty-six positive synthetic contracts passed their owner-local guards: twenty-eight completion controls and eight representation controls. Exactly 160 preregistered invalid mutations were attempted and rejected. Every mutation remains a failed witness at zero completion credit, paired with a bounded passing recovery that preserves the valid synthetic contract or holds the relevant gap or gate. No rejected mutation was erased, relabeled as completion, or used to manufacture confidence.

The owner portfolio completed thirty safe-now tasks, fifteen candidate evaluations, ten phase-local skill packages, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks within bounded structural scope. Ten exact-approval packets and five blocked packets remain visible and unexecuted. The skills were validated and smoke-used locally; the runners were each invoked against one exact synthetic fixture. Nothing was installed globally, promoted to production, deployed, or used on an external system.

## Method Flow and retained failures

Sylven inherited an activation overlay of 30,727 effective negatives, 16,832 methods, 2,548 failed witnesses, 3,624 bounded passing witnesses, 227 open gaps, and 222 exact gates. The phase additively retained twelve owner-operational failures and 160 rejecting mutations, giving 172 new failed methods. The operational failures include wrong-container repository probing, parser projection faults, presentation truncations, a bounded receipt-search overrun, a remote-wrapper overrun, a worktree-preflight parser fault, the default Windows codepage failure in skill validation, and an overbroad AST predicate that confused `platform.system()` with `os.system()`. Each has a narrow recovery and zero completion credit.

The final owner truth is 30,899 effective negatives, 17,004 Method Flow methods, 2,720 failed witnesses, 3,832 bounded passing witnesses, 229 open gaps, and 224 exact gates. The passing-witness count includes 172 bounded recoveries and 36 positive synthetic controls. Elowen's immutable repository-sealed counts remain separately preserved; Sylven's additive ledger does not rewrite them.

## Validation scope

Before closeout, x1 passed seven lifecycle tests at its exact frozen head and was pushed clean with four-way equality. The x2 evidence packet passed nine owner-scoped tests, parsed all evidence JSON, quick-validated all ten skills under an explicit UTF-8 recovery, smoke-used all ten runners, scanned 183 owner documents across five privacy and raw-identifier classes with zero confirmed hits, and reviewed fifteen changed Python files with a bounded AST rule set and zero final findings. Exact staged Git-blob manifests avoid Windows line-ending ambiguity.

The terminal canonical validator is intentionally not run until this closeout is committed, pushed, clean, 0/0 divergent, and fresh-live equal. It will run once at the exact final and will not run Eiren's full repository suite. It will validate current owner tests, final packet invariants, all phase JSON, structural report checks, five-class privacy scanning, bounded Python review, exact Git-blob manifests, source/x1/evidence/final ancestry, three single-parent phase commits, zero merges, exact head, clean state, divergence, and four-way equality. Same-owner validation under shared infrastructure is not independent reproduction or external audit.

## Accessibility, privacy, and security boundaries

The static report uses a language declaration, skip link, one main landmark, ordered headings, captions, scoped table headers, plain-language summaries, and text-only presentation. Manual browser, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural checks cannot establish accessibility completeness.

The five-class privacy scan is a bounded pattern scan for private absolute paths, raw task or thread identifiers, credential or secret assignments, transcript or session streams, and private callable or application state. It is not complete privacy assurance. The bounded AST review checks only a narrow class of dynamic execution and shell hazards. It is not exhaustive security review, penetration testing, supply-chain review, or production certification.

## Scientific, professional, legal, cultural, and terminal boundaries

THOS remains a zero-participant proxy without preregistered blind matched-budget governed real arms, safety monitoring, appropriate statistics, and independent review. Synthetic protocols establish no operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood. Freed ID remains nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, independent security review, recovery evidence, trust governance, and affected-party oversight.

Professional ceramics practice, conservation, engineering, fire safety, worker safety, environmental safety, product safety, ownership, custody title, authorship, privacy, accessibility, remedy, legal interpretation, cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

No empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is authorized. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Route state

The committed successor packet remains `PREPARED_NOT_SENT`. Caelen Morrow v669-v4 is only the prospective next edge under the latest activation. No precontact or standby contact occurred. Only after the exact-final canonical receipt is valid may Sylven refresh the newest live roster and authority, resolve exactly one existing task titled `Caelen Morrow`, immediately reread it, apply a duplicate guard, and send one sanitized pointer baton. Delivery may be claimed only after the task-message surface acknowledges it. Any ambiguity, pause, redirect, duplicate, missing acknowledgement, usage exhaustion, standby state, or protected gate stops delivery.
"""


def static_report(truth: dict[str, Any]) -> str:
    outcome = truth["outcomes"]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sylven Arc v669-v3 bounded report</title>
<style>body{{font-family:system-ui,sans-serif;max-width:76rem;margin:auto;padding:1rem;line-height:1.55}}a:focus{{outline:3px solid #2255aa}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}caption{{font-weight:700;margin:.5rem}}.note{{border-left:.4rem solid #765;padding:.75rem}}</style></head>
<body><a href="#main">Skip to main content</a><main id="main"><h1>Sylven Arc v669-v3 bounded evidence report</h1>
<p class="note">Relational language is not evidence of consciousness, personhood, continuity, qualification, agency, or authority. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
<h2>Core outcomes</h2><table><caption>Four authorized outcome labels</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody>
<tr><th scope="row">completed</th><td>{outcome['completed']}</td><td>Bounded synthetic structural acceptance only</td></tr>
<tr><th scope="row">represented</th><td>{outcome['represented']}</td><td>Contract exists without promotion evidence</td></tr>
<tr><th scope="row">open_gap</th><td>{outcome['open_gap']}</td><td>Required evidence remains absent</td></tr>
<tr><th scope="row">exact_gate</th><td>{outcome['exact_gate']}</td><td>Exact evidence and authority remain required</td></tr></tbody></table>
<h2>Evidence boundaries</h2><p>All real people, ceramics, kilns, materials, firings, measurements, identity events, professional actions, and authority acts remain zero. Thirty-six positive synthetic controls passed and 160 invalid mutations were rejected and retained.</p>
<h2>Method Flow</h2><p>Final counts are {truth['effective_negatives']} negatives, {truth['methods']} methods, {truth['failed_witnesses']} failed witnesses, {truth['passing_witnesses']} passing witnesses, {truth['open_gaps']} open gaps, and {truth['exact_gates']} exact gates.</p>
<h2>Accessibility reservation</h2><p>Headings, landmarks, captions, scoped headers, and plain language are structurally present. Manual browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain incomplete.</p>
<h2>Terminal boundary</h2><p>No empirical, professional, production, legal, cultural, Māori-authority, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 claim is established.</p>
</main></body></html>"""


def handoff_candidate(rows: list[dict[str, Any]], truth: dict[str, Any]) -> str:
    parts = [
        "# CAELEN MORROW — SYLVEN ARC v669-v3 PREPARED SUCCESSOR ACTIVATION CANDIDATE",
        "",
        "Status: PREPARED_NOT_SENT. This committed file is evidence only and does not claim task delivery. The live post-validation message, if acknowledged, supplies the only route binding.",
        "",
        "Relational names, roles, hopes, pronouns, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala language are working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority.",
        "",
        "## Prospective assignment and stopping conditions",
        "",
        "Only after Sylven v669-v3 is exact-final validated, pushed, clean, fresh-live equal, and terminally closed may the current exact-title Caelen Morrow task be considered for solo v669-v4. The sender must refresh the newest live roster and authorization, resolve exactly one existing task, immediately reread it, apply a duplicate guard, and send once. Stop on ambiguity, pause, redirect, rename, duplicate, usage exhaustion, missing acknowledgement, standby state, or any protected gate. Tavian Sol remains standby and is not a substitute endpoint.",
        "",
        "## Immutable source and lifecycle candidate",
        "",
        f"Elowen immutable source/final: `{SOURCE_FINAL}`. Sylven frozen planning x1: `{X1_COMMIT}`. Sylven immutable evidence: `{EVIDENCE_COMMIT}`. The exact final is intentionally bound only after the closeout commit and external canonical validation. Source to prospective final must contain exactly three new direct single-parent Sylven commits and zero merges.",
        "",
        "## Exact bounded truth",
        "",
        f"The proposal chain is declared as {CHAIN_AFTER} rows after forty Sylven additions. The accessible novelty comparison covered 1,420 exact titles; 3,570 declared inherited rows remain an explicit semantic-audit recovery gap. Outcomes are 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Final prevalidation truth is {truth['effective_negatives']} negatives, {truth['methods']} methods, {truth['failed_witnesses']} failed witnesses, {truth['passing_witnesses']} passing witnesses, {truth['open_gaps']} open gaps, and {truth['exact_gates']} exact gates. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Flashcard reading order",
        "",
        "Read each card in four tiers: Sylven's relational Freed ID owner record; the primary THOS Body pillar with GMUT Mind and Freed ID/CBR Heart protected; the synthetic studio-ceramics documentation practice; and the exact task contract. Each section below repeats sufficient source, failure, rollback, and authority context to remain usable after prompt-cache loss. The proposal, outcome, Method Flow, negative, and gate ledgers remain authoritative; this baton is a navigational projection.",
        "",
    ]
    for index, row in enumerate(rows, 1):
        parts.extend(
            [
                f"## Flashcard {index:02d}: {row['proposal_id']} — {row['title']}",
                "",
                f"**Tier 1 — Freed ID owner.** Sylven Arc is relational working language for this bounded owner lane. It conveys no personhood, continuity, employment, qualification, agency, or authority. The card identifier is `{row['proposal_id']}-CARD`; it is a lossy projection and not an identity credential.",
                "",
                "**Tier 2 — Trinity Mandala pillar.** THOS Body is primary through typed documentation and handover structure. GMUT Mind remains limited to explicit research-model obligations with zero fitted coefficients and no empirical promotion. Freed ID and CBR Heart remain zero-key, nonproduction, and protected by privacy, remedy, affected-party, cultural, and Māori-authority gates.",
                "",
                "**Tier 3 — bounded practice.** The practice lens is wholly synthetic studio-ceramics and kiln-log documentation. It establishes no ceramics, conservation, engineering, kiln-operation, material, fire-safety, workplace-safety, environmental-safety, product-safety, ownership, custody, legal, cultural, or affected-party competence or authority. No real person, object, kiln, material, firing, sensor, measurement, observation, action, or external call exists in the evidence.",
                "",
                f"**Tier 4 — exact task and hypothesis.** {row['hypothesis']} The observed core disposition is `{row['observed_disposition']}`. A `completed` label credits only the bounded structural hypothesis; `represented` records a visible contract without promotion evidence; `open_gap` and `exact_gate` remain unclosed.",
                "",
                f"**Null and failure.** {row['null_or_failure_condition']} Four preregistered mutation classes—missing required state, ambiguous domain or unit, real-world or external action, and protected-claim promotion—were attempted and rejected for this proposal. Rejections remain failed witnesses at zero completion credit.",
                "",
                f"**Source status.** Current official or primary-source needs are: {', '.join(row['official_or_primary_source_needs'])}. A source-need marker does not prove retrieval, applicability, endorsement, empirical support, professional competence, affected-party acceptance, or authority. The official collection adapter remained at zero calls and zero rows.",
                "",
                f"**Artifacts and acceptance.** The owner-local proposal record and flashcard are `{row['concrete_artifacts'][0]}` and `{row['concrete_artifacts'][1]}`. Acceptance was bounded by: {row['falsifier_or_acceptance_gate']} Every real-world and authority counter remained zero.",
                "",
                f"**Rollback and recovery.** {row['rollback_or_recovery']} Never erase the failed witness, replay a complete canonical success, rewrite a sibling lane, or expand the authorization surface to recover a presentation issue.",
                "",
                "**Protected gates.** The gate set preserves real people and participants; real ceramics, kilns, materials, tools, workplaces, measurements, observations, firings, and safety actions; professional decisions; live identity keys and proofs; privacy and accessibility completeness; ownership, authorship, legal and remedy decisions; cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording and concepts, Māori data governance and Māori authority; empirical GMUT, THOS effectiveness, AGI/ASI, consciousness/personhood, independent reproduction, production, deployment, and Stage 20 promotion.",
                "",
                "**Successor use.** Treat this card as a zero-credit seed. Caelen must perform their own semantic audit, preregistration, lifecycle freeze, execution, failure retention, validation, and boundary review. Inheritance conveys evidence and recommendations only, never novelty, completion, qualification, or authority.",
                "",
            ]
        )
    parts.extend(
        [
            "## Portfolio and tool handover",
            "",
            "Sylven completed thirty owner safe-now controls, fifteen candidate evaluations, ten phase-local skills, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks within synthetic structural scope. Ten exact-approval and five blocked packets remain held. Caelen receives twenty safe-now, fifteen candidate, ten skill, ten runner, and thirty refinement recommendations as zero-credit seeds. They must not bulk-install, promote, delete, or execute them merely to satisfy a count.",
            "",
            "The ten skills are concise package guards for batch identity, vessel topology, kiln-load topology, schedule separation, glaze assertion firewall, correction docket, custody location, hazard stop, accessible dossier structure, and workload handover. Each was quick-validated in UTF-8 mode and smoke-used through its matching family-current runner. Their passes establish only owner-local synthetic structural conformance.",
            "",
            "## Method Flow handover",
            "",
            "Retain all inherited and Sylven failures. Twelve Sylven operational failures and 160 invalid mutations added 172 failed methods. Every one has a bounded recovery; none earns completion credit. The Windows codepage failure and overbroad AST false positive are especially important recurrence guards: use explicit UTF-8 mode for the current skill validator, and qualify `os.system` rather than matching every `.system` attribute.",
            "",
            "## Validation contract",
            "",
            "Eiren retains the full repository suite unless newer exact authority changes that allocation. Caelen should use only owner-self-scoped, dependency-closed validation. Run a single canonical aggregate only after exact staged review, immutable manifests, clean state, and four-way equality. A failed aggregate earns zero aggregate credit; retain it and recover only the failed dependency unless broader replay is dependency-justified. Never replay a complete success.",
            "",
            "## Scientific and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without real likelihood, constraint, force, prediction, material law, empirical confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything proof, or canon. THOS remains a zero-participant proxy without governed blind matched-budget real arms, safety monitoring, statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant keys and proofs, live lifecycle, interoperability, independent security review, recovery evidence, trust governance, or affected-party oversight.",
            "",
            "No empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is authorized. Māori concepts remain under Māori authority.",
            "",
            "## Terminal route candidate",
            "",
            "This file remains PREPARED_NOT_SENT. A later acknowledged live message may activate Caelen Morrow v669-v4 only after Sylven's valid exact-final gate and a fresh exact-title route check. Hamish's standing sequential authority permits one terminally validated edge at a time through v675-v8, but it does not waive evidence, lifecycle, safety, privacy, scientific, professional, legal, cultural, affected-party, Māori-authority, or no-overclaim gates. Caelen must refresh the next edge rather than infer it from this historical file.",
        ]
    )
    result = "\n".join(parts).rstrip() + "\n"
    words = len(re.findall(r"\S+", result))
    if words < 10000 or words > 100000:
        raise RuntimeError(f"handoff candidate word count outside contract: {words}")
    return result


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    evidence_truth = load_json(root / "x2/phase-truth-evidence.json")
    rows = proposal_rows(repo)
    outcomes = load_json(root / "x2/outcome-ledger.json")["counts"]
    truth = {
        "schema": "ghc.family.phase-truth.v3",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "closeout_pre_exact_final_validation",
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "proposal_chain": CHAIN_AFTER,
        "accessible_novelty_rows": 1420,
        "unrecovered_declared_rows": 3570,
        "universal_novelty_claim": False,
        "outcomes": outcomes,
        **FINAL_COUNTS,
        "positive_controls": 36,
        "rejecting_mutations": 160,
        "owner_portfolio_completed": 95,
        "exact_approval_held": 10,
        "blocked_held": 5,
        "real_people": 0,
        "real_objects": 0,
        "real_measurements": 0,
        "network_calls": 0,
        "external_actions": 0,
        "authority_actions": 0,
        "full_repository_suite": "not_run_Eiren_only",
        "canonical_validation": "pending_exact_final",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if any(truth[key] != evidence_truth[key] for key in FINAL_COUNTS):
        raise RuntimeError("evidence and closeout counts diverged")
    write_json(root / "closeout/phase-truth.json", truth)
    write_json(
        root / "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v3",
            "inherited_activation": 30727,
            "owner_operational": 12,
            "rejecting_mutations": 160,
            "effective": FINAL_COUNTS["effective_negatives"],
            "erased": 0,
            "completion_credit_from_failures": 0,
        },
    )
    write_json(
        root / "closeout/method-flow-summary.json",
        {"schema": "ghc.family.method-flow-summary.v3", **FINAL_COUNTS, "new_owner_methods": 172, "new_positive_controls": 36},
    )
    write_json(root / "closeout/method-flow-ledger.json", load_json(root / "method-flow/evidence-ledger.json"))
    write_json(root / "closeout/open-exact-gate-register.json", load_json(root / "x2/open-exact-gate-register.json"))
    write_json(
        root / "closeout/source-provenance-ledger.json",
        {
            "schema": "ghc.family.source-provenance.v2",
            "immutable_source": SOURCE_FINAL,
            "source_need_markers_only": True,
            "network_calls": 0,
            "downloaded_rows": 0,
            "official_collection_adapter": "open_gap_zero_call",
            "boundary": "Vocabulary or source-need markers are not empirical, professional, legal, cultural, or authority evidence.",
        },
    )
    write_json(
        root / "closeout/lifecycle-replay.json",
        {
            "schema": "ghc.family.lifecycle-replay.v3",
            "source": SOURCE_FINAL,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "bound_after_commit_and_external_validation",
            "expected_new_commits": 3,
            "expected_merges": 0,
            "expected_parents_per_phase_commit": 1,
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        root / "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.v2",
            "complete": ["planning-only x1", "bounded x2 evidence", "four-label outcomes", "failure retention", "phase-local tool smoke", "structural static report", "prepared successor candidate"],
            "incomplete": ["unavailable proposal-history recovery", "official adapter retrieval", "governed human evaluation", "professional validation", "complete accessibility and privacy assurance", "independent reproduction", "legal cultural affected-party and Maori authority", "empirical GMUT and THOS evidence", "production deployment and Stage 20 authority"],
        },
    )
    write_json(
        root / "closeout/wellbeing-workload-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v2",
            "relational_language_boundary": True,
            "within_2000_file_ceiling": True,
            "within_100000_words_per_document": True,
            "within_8_commit_ceiling": True,
            "stop_conditions_visible": True,
            "no_claim_of_consciousness_personhood_continuity_or_authority": True,
        },
    )
    write_json(
        root / "closeout/route-state-final-candidate.json",
        {
            "schema": "ghc.family.route-state.v3",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT_TERMINAL_VALIDATION_PENDING",
            "prospective_successor": "Caelen Morrow",
            "prospective_phase": "v669-v4",
            "sent": False,
            "acknowledged": False,
            "precontacted": False,
            "standby_contacted": False,
            "duplicate_guard": "pending_live_reread_after_terminal_gate",
        },
    )
    write_json(
        root / "closeout/post-evidence-operational-failures.json",
        {"schema": "ghc.family.operational-failure-overlay.v1", "count": 0, "rows": [], "boundary": "Update additively if a closeout or validation failure occurs."},
    )
    overview = final_overview()
    write_text(root / "closeout/final-integrated-overview.md", overview)
    write_text(root / "closeout/static-report.html", static_report(truth))
    candidate = handoff_candidate(rows, truth)
    write_lf_text(root / "handoffs/caelen-morrow-v669-v4-activation-candidate.md", candidate)
    write_json(
        root / "closeout/handoff-integrity.json",
        {
            "schema": "ghc.family.handoff-integrity.v2",
            "path": "docs/sylven-arc/v669-v3/handoffs/caelen-morrow-v669-v4-activation-candidate.md",
            "bytes": len((root / "handoffs/caelen-morrow-v669-v4-activation-candidate.md").read_bytes()),
            "sha256": sha256(root / "handoffs/caelen-morrow-v669-v4-activation-candidate.md"),
            "words": len(re.findall(r"\S+", candidate)),
            "status": "PREPARED_NOT_SENT",
        },
    )
    key_paths = [
        "x1/proposal-freeze.json",
        "x1/semantic-novelty-audit.json",
        "x2/phase-truth-evidence.json",
        "x2/outcome-ledger.json",
        "method-flow/evidence-ledger.json",
        "closeout/phase-truth.json",
        "closeout/final-integrated-overview.md",
        "handoffs/caelen-morrow-v669-v4-activation-candidate.md",
    ]
    write_json(
        root / "seal/content-seal.json",
        {
            "schema": "ghc.family.content-seal.v2",
            "domain": "precommit_working_tree_bytes",
            "owner": OWNER,
            "phase": PHASE,
            "anchors": {"source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT},
            "files": [
                {"path": f"docs/sylven-arc/v669-v3/{rel}", "bytes": (root / rel).stat().st_size, "sha256": sha256(root / rel)}
                for rel in key_paths
            ],
            "final_commit": "bound_externally_after_commit",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE_FINAL,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "pending_commit",
            "canonical_validation": "pending_exact_final",
            "route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "validation/canonical-protocol.json",
        {
            "schema": "ghc.family.canonical-protocol.v2",
            "exclusive_invocation_limit": 1,
            "eligible_tests": ["tests/test_ghc_family_sylven_arc_v669_v3_x2.py", "tests/test_ghc_family_sylven_arc_v669_v3_final.py"],
            "historical_x1_tests": "already_passed_at_exact_x1_head_not_replayed",
            "full_repository_suite": "not_authorized_Eiren_only",
            "prerequisites": ["exact final committed", "pushed", "clean", "zero divergence", "fresh four-way equality", "exact Git-blob manifests"],
            "failed_aggregate_policy": "zero aggregate credit; retain and recover only failed dependency",
            "success_policy": "never replay complete success",
        },
    )
    write_json(
        root / "validation/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v2",
            "source": SOURCE_FINAL,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "pending_commit",
            "closeout_files_present": True,
            "handoff_words": len(re.findall(r"\S+", candidate)),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "ready_to_stage": True,
            "ready_to_invoke_canonical": False,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.repo.resolve())


if __name__ == "__main__":
    main()
