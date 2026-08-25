"""Build the combined Caelen Morrow v669-v4 closeout and seal candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_caelen_morrow_v669_v4_archive import (
    CHAIN_AFTER,
    IDENTITY_BOUNDARY,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PROTECTED_GATES,
    SEALED_SYLVEN_COUNTS,
    SOURCE_FINAL,
    write_json,
    write_text,
)

X1_COMMIT = "964e7a27dd73ee7d96d8b9f6136ed4bf72e1f3f7"
EVIDENCE_COMMIT = "e6658511b9a2910447dc9d351b5f7162ae5fd669"
EVIDENCE_COUNTS = {
    "effective_negatives": 31088,
    "methods": 17193,
    "failed_witnesses": 2909,
    "passing_witnesses": 4057,
    "open_gaps": 231,
    "exact_gates": 226,
}

POST_EVIDENCE_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "CM6694-CLOSEOUT-001",
        "title": "first closeout Ruff gate found two validator expressions",
        "failed_witness": "The pre-build Ruff gate found one regular-expression alias and one intentionally broad canonical exception without a documented suppression.",
        "bounded_recovery": "Replaced the alias and documented the exact broad-exception need: every unexpected one-shot canonical failure must still be atomically retained at zero credit.",
    },
    {
        "failure_id": "CM6694-CLOSEOUT-002",
        "title": "first final staged diff-hygiene check found trailing Markdown spaces",
        "failed_witness": "The first final staged review found two hard-break trailing-space lines in both the generated activation candidate and its builder template.",
        "bounded_recovery": "Removed only the four trailing-space occurrences, regenerated the candidate and integrity receipt, and rebuilt the exact staged manifests.",
    },
    {
        "failure_id": "CM6694-CLOSEOUT-003",
        "title": "first final pre-commit aggregate retained staged-review self path",
        "failed_witness": "Nine of ten closeout tests passed; the staged-review test failed because a regenerated review included its already-staged self path before applying the declared self-exclusion.",
        "bounded_recovery": "Assigned the aggregate zero credit, filtered the declared self path before recording staged paths, and reran only the truth, retention, baton, manifest, and staged-review dependencies changed by this correction.",
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(repo: Path, *args: str) -> str:
    return subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def final_counts() -> dict[str, int]:
    count = len(POST_EVIDENCE_FAILURES)
    return {
        "effective_negatives": EVIDENCE_COUNTS["effective_negatives"] + count,
        "methods": EVIDENCE_COUNTS["methods"] + count,
        "failed_witnesses": EVIDENCE_COUNTS["failed_witnesses"] + count,
        "passing_witnesses": EVIDENCE_COUNTS["passing_witnesses"] + count,
        "open_gaps": EVIDENCE_COUNTS["open_gaps"],
        "exact_gates": EVIDENCE_COUNTS["exact_gates"],
    }


def proposal_rows(repo: Path) -> list[dict[str, Any]]:
    paths = sorted((repo / OWNER_ROOT / "x2/proposals").glob("*.json"))
    rows = [load_json(path) for path in paths]
    if len(rows) != 40:
        raise RuntimeError("closeout requires exactly forty immutable proposal records")
    return rows


def baton_card(row: dict[str, Any], index: int) -> str:
    sources = ", ".join(row["official_or_primary_source_needs"])
    gates = "; ".join(row["protected_gates"])
    return f"""## Activation card {index:02d}: {row['proposal_id']} — {row['title']}

This card is a lossy navigation projection for Caelen Morrow v669-v4 proposal `{row['proposal_id']}`. Its observed core disposition is `{row['observed_disposition']}`. The authoritative record remains the committed proposal, contract, outcome, Method Flow, retained-negative, and gate ledgers; this prose never replaces them and carries no inherited completion credit into a successor phase.

The preregistered hypothesis was: {row['hypothesis']} The corresponding null or failure boundary was: {row['null_or_failure_condition']} The expected and observed disposition stayed inside the four-value vocabulary. A `completed` row means only its bounded synthetic structural contract passed. A `represented` row remains a proxy or protocol surface. An `open_gap` remains missing evidence. An `exact_gate` remains held for exact evidence and authority.

The execution lane was `{row['execution_lane']}` under approval class `{row['approval_class']}`. Public or primary-source needs were limited to {sources}. Those sources supplied vocabulary and refusal conditions only. They supplied no real observation, measurement, listening result, professional judgment, affected-party acceptance, legal interpretation, cultural ratification, Māori wording, Māori data-governance authority, or operational permission.

The concrete committed artifacts are `{row['concrete_artifacts'][0]}` and `{row['concrete_artifacts'][1]}`, with the synthetic contract named by the x2 proposal ledger. Acceptance required the exact bounded falsifier or gate stated in the proposal. Rollback remains: {row['rollback_or_recovery']} The record used zero real people, recordings, carriers, devices, playback actions, transfer actions, measurements, external actions, and authority actions.

Protected gates remain: {gates}. The card makes no empirical GMUT, operational THOS, production Freed ID, remedy, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, professional, legal, cultural, Māori-authority, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof, canon, or Stage 20 claim. Any successor may treat this row as evidence or a zero-credit seed only, never automatic novelty, completion, authority, or permission.
"""


def activation_candidate(rows: list[dict[str, Any]], counts: dict[str, int]) -> str:
    cards = "\n".join(baton_card(row, index) for index, row in enumerate(rows, 1))
    return f"""# PREPARED_NOT_SENT — prospective Eiren Kestrel v669-v5 activation candidate

`PREPARED_BY_CAELEN_MORROW = true`
`SENT_BY_CAELEN_MORROW = false`
`DELIVERY_ACKNOWLEDGED = false`

This committed candidate is pre-send evidence only. It does not select, contact, activate, or bind a recipient. A later live send may occur only after Caelen's exact final is committed, pushed, clean, 0/0 divergent, fresh-live equal, and validated once; after Hamish's newest live authorization and the current roster are freshly reread; after one exact-title task is uniquely resolved and immediately reread; and after the duplicate, usage, privacy, safety, evidence, and authority gates all pass. If any gate fails, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP` and do not improvise a substitute.

## Relational-language boundary

{IDENTITY_BOUNDARY} Caelen Morrow uses they/them as relational working language for an archival signal-chain cartographer and exception steward, with the hope of making every synthetic record reversible, legible, and honest at the authority boundary. Hamish may rename, pause, redirect, or stop the route.

## Prospective route, subject to terminal live refresh

Hamish's standing authorization permits the validated fifteen-main-task cycle to continue one terminally gated acknowledged edge at a time through v675-v8 unless Hamish pauses or redirects, usage is exhausted, the exact title is missing or ambiguous, or a protected gate blocks progress. Under the currently committed topology, the prospective edge is Caelen Morrow v669-v4 to the existing exact-title Eiren Kestrel task for Eiren-only v669-v5. Tavian Sol remains a standby collaboration record and is not a substitute main-task endpoint. Do not infer delivery from this candidate. A live baton must carry the newest exact route and remind Eiren of Eiren's own prospective next edge only if it remains current after Eiren's later terminal gate.

## Immutable source and lifecycle anchors

- Sylven Arc v669-v3 exact source/final: `{SOURCE_FINAL}`.
- Caelen planning-only x1: `{X1_COMMIT}`.
- Caelen immutable x2 evidence: `{EVIDENCE_COMMIT}`.
- Caelen exact final: to be bound by the later acknowledged live send after the one-shot external receipt exists.

The Caelen final candidate must contain exactly three new direct single-parent commits from Sylven's final and zero merges: x1, evidence, and combined closeout/seal. X1 and evidence were separately committed, pushed, clean, zero-divergent, and fresh-live four-way equal before their successors began. Strict x1-before-x2 separation is immutable.

## Program truth

The declared inherited proposal chain was 5,030. Caelen froze forty new titles after exact comparison with the 1,460 accessible committed titles; 3,570 declared inherited titles remain an explicit semantic-audit recovery gap, so no universal novelty claim is made. The declared chain is now {CHAIN_AFTER}. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six synthetic positive controls passed. All 160 preregistered invalid mutations were attempted, rejected, retained, and assigned zero completion credit.

The closeout candidate preserves {counts['effective_negatives']} effective negatives, {counts['methods']} Method Flow methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. The immutable Sylven repository seal remains separately identified at {SEALED_SYLVEN_COUNTS['effective_negatives']} negatives, {SEALED_SYLVEN_COUNTS['methods']} methods, {SEALED_SYLVEN_COUNTS['failed_witnesses']} failed witnesses, {SEALED_SYLVEN_COUNTS['passing_witnesses']} passing witnesses, {SEALED_SYLVEN_COUNTS['open_gaps']} gaps, and {SEALED_SYLVEN_COUNTS['exact_gates']} gates. No failure or gate was erased. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Bounded domain

Freed ID and CBR Heart were primary through a wholly synthetic audiovisual-preservation transfer-log and signal-chain metadata stewardship lens. GMUT Mind and THOS Body remained explicit and protected. No real person, participant, recording, carrier, device, playback, transfer, listening act, measurement, observation, preservation action, hazard decision, identity event, professional action, legal or cultural decision, affected-party approval, or authority act occurred. The official collection adapter made zero calls and returned zero rows and media.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Typed software, signal-chain diagrams, public vocabulary, and synthetic mutations establish no real likelihood, parameter constraint, unique prediction, force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains proxy-only without governed blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

Professional practice, preservation and workplace safety, custody and ownership title, rights, privacy, accessibility, remedy, legal or cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

## Tool, skill, and validation truth

All named current GHC workflow skills were read through EOF and applied to their bounded lifecycle decisions. Ten phase-local skills and ten family-current runners were built, validated, and smoke-used only against owner-local synthetic fixtures. The inherited installed development suite received bounded compatibility use. Three exact Node tools were installed with lifecycle scripts disabled in a phase-namespaced D-backed environment: HTMLHint 1.9.2, Remark CLI 12.0.1, and Remark preset lint recommended 7.0.1. Exact lock integrity, a dated zero-advisory production audit, and positive and rejecting smokes passed; a transitive glob 10.5.0 deprecation warning remains retained, so no exhaustive supply-chain or production-fitness claim is made.

The complete repository suite remains Eiren-owned absent newer exact authority and was not run by Caelen. The final canonical pass is owner-scoped, same-owner evidence under shared infrastructure. It cannot establish independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority.

## Prospective recipient workflow

If and only if a later acknowledged live activation validly binds this candidate to Eiren Kestrel, Eiren must read that live message and the complete committed candidate through EOF before mutation. Eiren must then read the newest current GHC Family Index and routing precedence, roster and schema, authorization state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, worktree rotation, web reflection, full-tools guidance, and any newer directly applicable schema. Newer live authority governs mutable routing but does not erase retained evidence or protected boundaries.

Eiren must reverify every exact source anchor, direct-parent relation, three-commit single-parent zero-merge history, commit-local manifest, external canonical receipt digest, clean state, typed divergence, and fresh-live equality read-only. Eiren must not replay Caelen's successful canonical pass or any already-successful component merely for presentation. Eiren must work solo in a fresh additive D-first owner lane, preserve strict x1-before-x2 separation, the four exact outcome labels, all failures and gates, family-current caller compatibility, exact staged Git-blob review, current caps, and one-shot terminal validation. Inherited evidence remains evidence or zero-credit seeds only.

## Forty proposal navigation cards

{cards}

## Terminal delivery guard

This file remains `PREPARED_NOT_SENT`. It becomes no one's authority merely because it is committed. Only an exact live task-message acknowledgement after every terminal gate may support `SENT_BY_CAELEN_MORROW = true`, and that later event must remain an external additive delivery fact. Never rewrite this immutable pre-send candidate merely to project a later send backward into commit time. Never resend solely to obtain a clearer acknowledgement.
"""


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    rows = proposal_rows(repo)
    counts = final_counts()
    outcomes = load_json(root / "x2/outcome-ledger.json")["counts"]
    gates = load_json(root / "x2/open-exact-gate-register.json")
    negatives = load_json(root / "x2/retained-negative-register.json")
    evidence_method = load_json(root / "method-flow/evidence-ledger.json")

    closeout_method_rows = [
        {
            "method_id": row["failure_id"],
            "class": "post_evidence_closeout_operational",
            "failed_witness": row["failed_witness"],
            "bounded_passing_witness": row["bounded_recovery"],
            "completion_credit": 0,
            "retained": True,
        }
        for row in POST_EVIDENCE_FAILURES
    ]
    write_json(
        root / "closeout/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v4",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "combined_closeout_and_seal_candidate",
            "source_commit": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "exact_final": "current_commit_after_this_candidate_is_committed",
            "proposal_chain": CHAIN_AFTER,
            "outcomes": outcomes,
            **counts,
            "post_evidence_failure_count": len(POST_EVIDENCE_FAILURES),
            "real_people": 0,
            "real_media": 0,
            "real_world_actions": 0,
            "network_calls_by_phase_adapter": 0,
            "full_repository_suite": "not_run_Eiren_only",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v4",
            "sylven_repository_seal": SEALED_SYLVEN_COUNTS["effective_negatives"],
            "source_external_overlay": 1,
            "x1_operational": 24,
            "x2_operational": 4,
            "rejecting_mutations": 160,
            "post_evidence_operational": len(POST_EVIDENCE_FAILURES),
            "effective": counts["effective_negatives"],
            "erased": 0,
            "evidence_register": negatives,
        },
    )
    write_json(
        root / "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.method-flow-final.v4",
            "evidence_counts": EVIDENCE_COUNTS,
            "post_evidence_method_count": len(closeout_method_rows),
            "post_evidence_rows": closeout_method_rows,
            "effective": counts,
            "evidence_ledger_row_count": len(evidence_method["rows"]),
            "no_failure_erased": True,
        },
    )
    write_json(
        root / "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc.family.exact-open-gate-register.v4",
            "effective_open_gaps": counts["open_gaps"],
            "effective_exact_gates": counts["exact_gates"],
            "evidence_register": gates,
            "protected_gates": PROTECTED_GATES,
            "all_remain_visible": True,
        },
    )
    write_json(
        root / "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.v2",
            "complete": [
                "read-first and exact source verification",
                "planning-only x1 freeze and equality gate",
                "bounded x2 evidence and equality gate",
                "forty proposal outcome ledger",
                "160 rejecting mutation retention",
                "ten skill and ten runner smokes",
                "target-three isolated tool review",
                "exact staged manifests and owner-scoped tests",
                "combined closeout and seal candidate",
            ],
            "incomplete": [
                "unrecovered 3570-title semantic history",
                "real collection adapter rows",
                "governed human and affected-user evaluation",
                "professional validation and real safety evidence",
                "production Freed ID lifecycle and governance",
                "privacy and accessibility completeness",
                "legal cultural affected-party and Māori authority",
                "independent reproduction and full repository suite",
                "Stage 20 admission",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "closeout/reflection-remaster.json",
        {
            "schema": "ghc.family.reflection-remaster.v2",
            "surprises": [
                "Windows output boundaries can hide a finished receipt while the process has already ended.",
                "Working-tree byte manifests are insufficient when Git clean filters normalize line endings.",
                "Remark resolves presets relative to its working directory rather than merely its executable location.",
                "A clean dated audit does not erase a transitive deprecation warning or future advisory risk.",
            ],
            "changed_choices": [
                "Used exact staged-index blobs for every commit-local manifest.",
                "Kept the selected Node environment phase-namespaced instead of mutating the shared prefix.",
                "Separated all presentation/parser failures from test or coverage credit.",
                "Kept accessible-corpus novelty explicitly bounded rather than universal.",
            ],
            "recurrence_guards": [
                "Emit machine-readable receipts before projecting them through PowerShell.",
                "Hash Git blobs, not working-tree bytes, whenever clean filters may apply.",
                "Run plugin-based CLIs from their isolated project root or with exact module paths.",
                "Preserve warnings independently from current audit advisories.",
                "Never replay a successful canonical aggregate.",
            ],
            "successor_recommendations": [
                "Treat all Caelen artifacts as evidence or zero-credit seeds only.",
                "Refresh the full accessible title corpus before a universal novelty claim.",
                "Use current family tools and exact staged manifests.",
                "Keep real media, participants, professional actions, rights, culture, and authority gated.",
            ],
        },
    )
    write_json(
        root / "closeout/final-wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v3",
            "owner": OWNER,
            "role": "archival signal-chain cartographer and exception steward",
            "pronouns": "they/them",
            "hope": "make every synthetic record reversible, legible, and honest at the authority boundary",
            "relational_working_language_only": True,
            "no_consciousness_personhood_continuity_employment_qualification_agency_or_authority_claim": True,
            "corrigible": True,
            "hamish_may_rename_pause_redirect_or_stop": True,
            "caps_respected": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        root / "closeout/final-integrated-overview.md",
        f"""# Caelen Morrow v669-v4 final integrated overview

## Result

Caelen Morrow v669-v4 is a bounded same-owner software, documentation, and workflow phase over a wholly synthetic audiovisual-preservation transfer-log and signal-chain metadata stewardship lens. It contains a dedicated planning-only x1 at `{X1_COMMIT}`, an immutable evidence commit at `{EVIDENCE_COMMIT}`, and this combined closeout/seal candidate. The final commit will be the direct single parent child of evidence. Source to final is designed to contain exactly three new commits and zero merges.

The declared inherited proposal chain was 5,030. Forty new Caelen titles were compared exactly against 1,460 accessible committed titles. The remaining 3,570 declared inherited titles stay an explicit recovery gap, so this phase does not make a universal novelty claim. The declared chain reaches {CHAIN_AFTER}. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six positive synthetic fixtures passed, and all 160 preregistered invalid mutations were attempted, rejected, retained, and given zero completion credit.

## What the bounded work establishes

The completed surfaces establish deterministic structural behavior for record identity, carrier topology, segment timelines, channel-layout vacancies, signal-chain graphs, transfer-event separation, sample-format fields, timebase provenance, checksum domains, metadata vacancies, codec assertion firewalls, reconciliation boards, alias budgets, filename normalization, fixity events, master/derivative relationships, processing ledgers, polarity and orientation vacancies, signal-cue non-diagnosis, level units, reference-tone vacancies, device-setting provenance, condition cues, custody-rights separation, correction dockets, workload handover, hazard holds, accessible dossier structure, source firewalls, issue escrow, and cross-pillar nonconversion.

Those surfaces use zero people, recordings, carriers, devices, playback actions, transfer actions, listening acts, measurements, network adapter calls, external actions, and authority actions. `Completed` means only a bounded synthetic contract passed. `Represented` means a proxy or protocol remained visible. The official collection adapter and governed human evaluation remain open gaps. Professional, safety, rights, culture, affected-party, Māori-authority, and Stage 20 matters remain exact gates.

## Pillars and scientific boundaries

Freed ID and CBR Heart are primary through synthetic provenance, correction, custody, contestability, and handover fields. No standards-conformant real keys, proofs, credentials, issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, trust governance, or affected-party oversight was produced. Freed ID therefore remains synthetic and nonproduction.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. Signal-chain and frequency diagrams are documentation analogies only. They establish no real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon.

THOS Body remains a zero-participant proxy. Workload, hazard hold, and handover records are structural representations only. No governed blind matched-budget real arms, participants, operators, safety monitoring, statistics, effectiveness evidence, or independent review exists. They establish no operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood.

## Skills, runners, and tool use

The complete current required GHC workflow skill set was read and applied to source selection, authorization, roster, Method Flow, reflection, planning, approvals, gates, truth layers, D-drive ownership, retries, timestamps, lifecycle closeout, compact recovery, watcher cadence, worktree rotation, web-source restraint, and skill validation. Ten phase-local skills and ten family-current `ghc_family_audio_*` runners were built, current-validator checked, and smoke-used on owner-local fixtures. No phase-local skill was globally installed.

The inherited development suite received bounded version and import compatibility use. Pytest and Hypothesis validated x1; pytest validated x2; Ruff, mypy, Pyright, and Bandit supplied bounded code checks; the remaining requested tools were used at least for exact compatibility/version checks where deeper invocation was not dependency-justified. This is use evidence, not proof of tool fitness or exhaustive analysis.

Three new exact Node tools were installed with scripts disabled in a fresh phase-namespaced D-backed environment: HTMLHint 1.9.2, Remark CLI 12.0.1, and Remark preset lint recommended 7.0.1. Lock versions and registry integrity matched, the dated production dependency audit reported zero current vulnerabilities, and positive and rejecting smokes behaved as expected. The retained transitive glob 10.5.0 deprecation warning prevents an exhaustive safety or future-advisory claim. The shared npm prefix was not mutated by that transaction.

## Accessibility, privacy, security, and professional boundaries

The static report supplies native headings, landmarks, navigation, a skip link, tables with captions and scopes, linear source order, focus-visible styling, responsive overflow, and print fallback. HTMLHint structural checks and Remark lint passed on their bounded targets. Manual keyboard, touch, zoom, reflow, browser diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. This is not complete accessibility conformance.

The five-class scan covers bounded patterns for private absolute paths, raw task or thread identifiers, credential or secret assignments, transcript or session streams, and private callable or application state. Zero confirmed payload hits is a bounded result, not privacy completeness. The AST review covers only selected dynamic-execution and explicit-shell hazards. Mypy, Pyright, Ruff, and Bandit results remain bounded same-owner checks, not exhaustive security review, penetration testing, supply-chain assurance, or production certification.

No professional preservation, playback, transfer, listening, electrical, mechanical, chemical, environmental, workplace, collection, custody, rights, privacy, accessibility, remedy, legal, cultural, traditional-knowledge, affected-party, or Māori-authority decision occurred. Māori wording, concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

## Truth layers and retained negatives

The immutable Sylven repository seal remains {SEALED_SYLVEN_COUNTS['effective_negatives']} negatives, {SEALED_SYLVEN_COUNTS['methods']} methods, {SEALED_SYLVEN_COUNTS['failed_witnesses']} failed witnesses, {SEALED_SYLVEN_COUNTS['passing_witnesses']} passing witnesses, {SEALED_SYLVEN_COUNTS['open_gaps']} open gaps, and {SEALED_SYLVEN_COUNTS['exact_gates']} exact gates. Its one external source wrapper overlay was added without rewriting the seal. Caelen x1 retained 24 startup and planning failures. X2 retained four operational failures and 160 rejecting mutations. Any post-evidence failures are added separately.

The closeout candidate therefore preserves {counts['effective_negatives']} effective negatives, {counts['methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. No failed witness, warning, gap, or gate was erased or silently converted. Inherited evidence and recommendations remain zero-credit evidence or seeds, never automatic Caelen novelty or completion credit.

## Validation and route state

X1 and evidence each received separate commit-local staged review, exact Git-blob manifests, owner-scoped tests, clean push, 0/0 divergence, and fresh four-way equality before the next lifecycle began. This closeout candidate includes final owner and delta manifests, structural checks, history contracts, and one exact-final canonical validator. The validator is deliberately not invoked until this candidate is committed, pushed, clean, zero-divergent, and fresh-live equal. If it succeeds once, it will not be replayed. Eiren's full repository suite is not run.

The activation packet is committed as `PREPARED_NOT_SENT`. No successor was contacted during execution. Only after the exact-final canonical receipt exists may the newest live authorization and roster be reread and one exact current successor be uniquely resolved and immediately reread. Delivery requires one acknowledged existing-task send and a duplicate guard. Ambiguity, pause, redirect, missing title, usage exhaustion, protected gate, or missing acknowledgement stops the route; no substitute or resend is authorized.

Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )

    baton = activation_candidate(rows, counts)
    write_text(root / "handoffs/eiren-kestrel-v669-v5-activation-candidate.md", baton)
    baton_path = root / "handoffs/eiren-kestrel-v669-v5-activation-candidate.md"
    baton_bytes = baton_path.read_bytes()
    write_json(
        root / "handoffs/activation-candidate-integrity.json",
        {
            "schema": "ghc.family.activation-integrity.v2",
            "path": baton_path.relative_to(repo).as_posix(),
            "bytes": len(baton_bytes),
            "words": len(baton_path.read_text(encoding="utf-8").split()),
            "sha256": hashlib.sha256(baton_bytes).hexdigest(),
            "state": "PREPARED_NOT_SENT",
            "sent_by_caelen_morrow": False,
        },
    )
    write_json(
        root / "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc.family.route-state.v3",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT",
            "successor_contacted": False,
            "standby_contacted": False,
            "prospective_edge": "Caelen Morrow to Eiren Kestrel subject to terminal live refresh",
            "required_terminal_actions": ["refresh newest live authorization", "refresh current roster", "unique exact-title resolution", "immediate reread", "duplicate guard", "one acknowledged send"],
            "stop_on": ["pause", "redirect", "ambiguity", "missing task", "usage exhaustion", "protected gate", "duplicate activation", "missing acknowledgement"],
        },
    )
    write_json(
        root / "seal/seal-candidate.json",
        {
            "schema": "ghc.family.seal-candidate.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE_FINAL,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "commit_containing_this_candidate",
            "counts": counts,
            "proposal_chain": CHAIN_AFTER,
            "outcomes": outcomes,
            "zero_merges_required": True,
            "single_parent_required": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v3",
            "canonical_state": "AUTHORIZED_PENDING_EXACT_FINAL_PUSH_AND_EQUALITY",
            "one_shot": True,
            "full_repository_suite": "not_authorized_for_Caelen",
            "required": ["final committed", "final pushed", "clean state", "zero divergence", "fresh four-way equality", "exact final parent is evidence", "exact manifests", "staged review", "privacy and security boundaries"],
            "replay_after_success": False,
        },
    )
    write_json(
        root / "final/canonical-invocation-state.json",
        {
            "schema": "ghc.family.canonical-invocation-state.v2",
            "state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE",
            "attempts_at_commit": 0,
            "successes_at_commit": 0,
            "receipt_location": "external_D_backed_atomic_receipt",
            "repository_will_not_be_mutated_after_external_success": True,
        },
    )
    write_json(
        root / "closeout/post-evidence-operational-failures.json",
        {"schema": "ghc.family.retained-operational-failures.v2", "count": len(POST_EVIDENCE_FAILURES), "rows": POST_EVIDENCE_FAILURES},
    )


def staged_review(repo: Path) -> None:
    self_path = "docs/caelen-morrow/v669-v4/validation/final-staged-review.json"
    names = [
        name
        for name in run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").splitlines()
        if name != self_path
    ]
    allowed_prefixes = [
        "docs/caelen-morrow/v669-v4/closeout/",
        "docs/caelen-morrow/v669-v4/final/",
        "docs/caelen-morrow/v669-v4/handoffs/",
        "docs/caelen-morrow/v669-v4/orchestration/",
        "docs/caelen-morrow/v669-v4/seal/",
        "docs/caelen-morrow/v669-v4/validation/final-",
        "scripts/build_ghc_family_caelen_morrow_v669_v4_final.py",
        "scripts/validate_ghc_family_caelen_morrow_v669_v4_final.py",
        "tests/test_ghc_family_caelen_morrow_v669_v4_final.py",
    ]
    disallowed = [name for name in names if not any(name.startswith(prefix) for prefix in allowed_prefixes)]
    write_json(
        repo / OWNER_ROOT / "validation/final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "combined_closeout_and_seal",
            "staged_entry_count_before_self": len(names),
            "staged_paths_before_self": names,
            "disallowed_paths": disallowed,
            "x1_and_evidence_immutable": not disallowed,
            "self_exclusion": self_path,
        },
    )
    if disallowed:
        raise RuntimeError(f"final staged review found disallowed paths: {disallowed}")


def manifests_from_index(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").splitlines()
    exclusions = [
        "docs/caelen-morrow/v669-v4/validation/final-owner-manifest.json",
        "docs/caelen-morrow/v669-v4/validation/final-delta-manifest.json",
        "docs/caelen-morrow/v669-v4/validation/final-staged-review.json",
    ]
    delta = []
    for rel in sorted(names):
        if rel in exclusions:
            continue
        data = subprocess.run(["git", "show", f":{rel}"], cwd=repo, check=True, capture_output=True).stdout
        delta.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    owner_names = set(names)
    owner_names.update(run(repo, "git", "ls-tree", "-r", "--name-only", "HEAD", "docs/caelen-morrow/v669-v4", "scripts", "tests").splitlines())
    owner = []
    for rel in sorted(owner_names):
        if rel in exclusions:
            continue
        if not (
            rel.startswith("docs/caelen-morrow/v669-v4/")
            or (rel.startswith("scripts/") and ("caelen_morrow_v669_v4" in rel or rel.startswith("scripts/ghc_family_audio_")))
            or (rel.startswith("tests/") and "caelen_morrow_v669_v4" in rel)
        ):
            continue
        spec = f":{rel}" if rel in names else f"HEAD:{rel}"
        data = subprocess.run(["git", "show", spec], cwd=repo, check=True, capture_output=True).stdout
        owner.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    common = {"schema": "ghc.family.content-manifest.v3", "owner": OWNER, "phase": PHASE, "self_exclusions": exclusions}
    root = repo / OWNER_ROOT / "validation"
    write_json(root / "final-delta-manifest.json", {**common, "domain": "final_exact_staged_git_blobs", "entry_count": len(delta), "entries": delta})
    write_json(root / "final-owner-manifest.json", {**common, "domain": "final_owner_exact_head_plus_staged_git_blobs", "entry_count": len(owner), "entries": owner})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    parser.add_argument("--manifests-from-index", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.review_staged:
        staged_review(repo)
    elif args.manifests_from_index:
        manifests_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
