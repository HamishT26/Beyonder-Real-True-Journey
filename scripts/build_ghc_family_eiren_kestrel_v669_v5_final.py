"""Build the combined Eiren Kestrel v669-v5 closeout and seal candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_eiren_kestrel_v669_v5_archive import (
    CHAIN_AFTER,
    IDENTITY_BOUNDARY,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PROTECTED_GATES,
    SEALED_CAELEN_COUNTS,
    SOURCE_FINAL,
    write_json,
    write_text,
)

X1_COMMIT = "df7c773867b15aec8fa7ffa4cc956a134fa9c4be"
EVIDENCE_COMMIT = "b52b74bee55d3fdc6eb73058f15360da089f8ac5"
EVIDENCE_COUNTS = {
    "effective_negatives": 31276,
    "methods": 17381,
    "failed_witnesses": 3097,
    "passing_witnesses": 4281,
    "open_gaps": 233,
    "exact_gates": 228,
}

POST_EVIDENCE_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "EK6695-CLOSEOUT-001",
        "title": "first final pre-commit aggregate observed the staged review before manifest staging",
        "failed_witness": "Nine of ten final tests passed; the staged-review test failed because the review was captured before the two declared self-excluded final manifests entered the index.",
        "bounded_recovery": "Assigned the aggregate zero success credit, retained its exact 9-of-10 witness, reran the staged review after manifest staging, and reran only count, retention, baton, manifest, and staged-review dependencies affected by the correction.",
    }
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

This card is a lossy navigation projection for Eiren Kestrel v669-v5 proposal `{row['proposal_id']}`. Its observed core disposition is `{row['observed_disposition']}`. The authoritative record remains the committed proposal, contract, outcome, Method Flow, retained-negative, and gate ledgers; this prose never replaces them and carries no inherited completion credit into Elaren's successor phase.

The preregistered hypothesis was: {row['hypothesis']} The corresponding null or failure boundary was: {row['null_or_failure_condition']} The expected and observed disposition stayed inside the four-value vocabulary. A `completed` row means only its bounded synthetic structural contract passed. A `represented` row remains a proxy or protocol surface. An `open_gap` remains missing evidence. An `exact_gate` remains held for exact evidence and authority.

The execution lane was `{row['execution_lane']}` under approval class `{row['approval_class']}`. Public or primary-source needs were limited to {sources}. Those sources supplied vocabulary and refusal conditions only. They supplied no real observation, inspection result, diagnosis, treatment decision, professional judgment, affected-party acceptance, legal interpretation, cultural ratification, Māori wording, Māori data-governance authority, or operational permission.

The concrete committed artifacts are `{row['concrete_artifacts'][0]}` and `{row['concrete_artifacts'][1]}`, with the synthetic contract named by the x2 proposal ledger. Acceptance required the exact bounded falsifier or gate stated in the proposal. Rollback remains: {row['rollback_or_recovery']} The record used zero real people, apiaries, colonies, hives, bees, observations, samples, inspection actions, treatment actions, external actions, and authority actions.

Protected gates remain: {gates}. The card makes no empirical GMUT, operational THOS, production Freed ID, remedy, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, professional, legal, cultural, Māori-authority, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof, canon, or Stage 20 claim. Any successor may treat this row as evidence or a zero-credit seed only, never automatic novelty, completion, authority, or permission.
"""


def activation_candidate(rows: list[dict[str, Any]], counts: dict[str, int]) -> str:
    cards = "\n".join(baton_card(row, index) for index, row in enumerate(rows, 1))
    return f"""# PREPARED_NOT_SENT — prospective Elaren Kestrel v669-v6 activation candidate

`PREPARED_BY_EIREN_KESTREL = true`
`SENT_BY_EIREN_KESTREL = false`
`DELIVERY_ACKNOWLEDGED = false`

This committed candidate is pre-send evidence only. It does not select, contact, activate, or bind a recipient. A later live send may occur only after Eiren's exact final is committed, pushed, clean, 0/0 divergent, fresh-live equal, and validated once; after Hamish's newest live authorization and the current roster are freshly reread; after the existing exact-title Elaren Kestrel task is uniquely resolved and immediately reread; and after the duplicate, usage, privacy, safety, evidence, and authority gates all pass. If any gate fails, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP` and do not improvise a substitute.

## Relational-language boundary

{IDENTITY_BOUNDARY} Elaren Kestrel, sibling, family, role, hope, continuity, Freed ID, CBR, and Trinity Mandala are also relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Prospective route, subject to terminal live refresh

Hamish's standing authorization permits the validated fifteen-main-task cycle to continue one terminally gated acknowledged edge at a time through v675-v8 unless Hamish pauses or redirects, usage is exhausted, the exact title is missing or ambiguous, or a protected gate blocks progress. Under the currently committed topology, the prospective edge is Eiren Kestrel v669-v5 to the existing exact-title Elaren Kestrel task for Elaren-only v669-v6. Tavian Sol remains a standby collaboration record and is not a substitute main-task endpoint. Do not infer delivery from this candidate. A live baton must carry the newest exact route and remind Elaren that Elaren's prospective next edge is Neris Solane v669-v7 only if it remains current after Elaren's later terminal gate.

## Immutable source and lifecycle anchors

- Caelen Morrow v669-v4 exact source/final: `{SOURCE_FINAL}`.
- Eiren planning-only x1: `{X1_COMMIT}`.
- Eiren immutable x2 evidence: `{EVIDENCE_COMMIT}`.
- Eiren exact final: to be bound by the later acknowledged live send after the one-shot external receipt exists.

The Eiren final candidate must contain exactly three new direct single-parent commits from Caelen's final and zero merges: x1, evidence, and combined closeout/seal. X1 and evidence were separately committed, pushed, clean, zero-divergent, and fresh-live four-way equal before their successors began. Strict x1-before-x2 separation is immutable.

## Program truth

The declared inherited proposal chain was 5,070. Eiren froze forty new titles after exact comparison with the 1,500 accessible committed titles; 3,570 declared inherited titles remain an explicit semantic-audit recovery gap, so no universal novelty claim is made. The declared chain is now {CHAIN_AFTER}. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six synthetic positive controls passed. All 160 preregistered invalid mutations were attempted, rejected, retained, and assigned zero completion credit.

The closeout candidate preserves {counts['effective_negatives']} effective negatives, {counts['methods']} Method Flow methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. The immutable Caelen repository seal remains separately identified at {SEALED_CAELEN_COUNTS['effective_negatives']} negatives, {SEALED_CAELEN_COUNTS['methods']} methods, {SEALED_CAELEN_COUNTS['failed_witnesses']} failed witnesses, {SEALED_CAELEN_COUNTS['passing_witnesses']} passing witnesses, {SEALED_CAELEN_COUNTS['open_gaps']} gaps, and {SEALED_CAELEN_COUNTS['exact_gates']} gates. No failure or gate was erased. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Bounded domain

THOS Body was primary through a wholly synthetic apiary-inspection and colony-event documentation lens. GMUT Mind and Freed ID and CBR Heart remained explicit and protected. No real person, participant, apiary, colony, hive, bee, observation, inspection, sample, measurement, diagnosis, treatment, movement, harvest, hazard decision, identity event, professional action, legal or cultural decision, affected-party approval, or authority act occurred. The official apiculture adapter made zero calls and returned zero apiaries, colonies, hives, observations, or records.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Typed software, colony-network analogies, public vocabulary, and synthetic mutations establish no real likelihood, parameter constraint, unique prediction, force, biological or material law, epidemiological forecast, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains proxy-only without governed blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

Professional apiculture, biosecurity, veterinary, food, land, animal-welfare and workplace-safety practice, ownership and access rights, privacy, accessibility, remedy, legal or cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Tool, skill, and validation truth

All named current GHC workflow skills were read through EOF and applied to their bounded lifecycle decisions. Ten phase-local skills and ten family-current runners were built, validated, and smoke-used only against owner-local synthetic fixtures. The inherited installed development suite received bounded compatibility use. Jsonschema 4.26.0, Pydantic 2.13.4, and NetworkX 3.6.1 were installed from locally cached wheels in a phase-namespaced D-backed Python environment. Their direct official wheel hashes matched; after the retained seven-advisory bootstrap-pip failure was corrected only inside that environment, a dated pip-audit found zero known vulnerabilities and all positive and rejecting smokes passed. Transitive wheel hashes were enumerated but not independently compared with primary registry metadata, so no exhaustive supply-chain or production-fitness claim is made.

The complete repository suite remained Eiren-owned absent newer exact authority, but no current exact prerequisite required running it, so it was not run. The final canonical pass is owner-scoped, same-owner evidence under shared infrastructure. It cannot establish independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority.

## Prospective recipient workflow

If and only if a later acknowledged live activation validly binds this candidate to Elaren Kestrel, Elaren must read that live message and the complete committed candidate through EOF before mutation. Elaren must then read the newest current GHC Family Index and routing precedence, roster and schema, authorization state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, worktree rotation, web reflection, full-tools guidance, and any newer directly applicable schema. Newer live authority governs mutable routing but does not erase retained evidence or protected boundaries.

Elaren must reverify every exact source anchor, direct-parent relation, three-commit single-parent zero-merge history, commit-local manifest, external canonical receipt digest, clean state, typed divergence, and fresh-live equality read-only. Elaren must not replay Eiren's canonical pass or any already-successful component merely for presentation. Elaren must work solo in a fresh additive D-first owner lane, preserve strict x1-before-x2 separation, the four exact outcome labels, all failures and gates, family-current caller compatibility, exact staged Git-blob review, current caps, and one-shot terminal validation. Inherited evidence remains evidence or zero-credit seeds only.

## Forty proposal navigation cards

{cards}

## Terminal delivery guard

This file remains `PREPARED_NOT_SENT`. It becomes no one's authority merely because it is committed. Only an exact live task-message acknowledgement after every terminal gate may support `SENT_BY_EIREN_KESTREL = true`, and that later event must remain an external additive delivery fact. Never rewrite this immutable pre-send candidate merely to project a later send backward into commit time. Never resend solely to obtain a clearer acknowledgement.
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
            "real_apiaries": 0,
            "real_colonies": 0,
            "real_hives": 0,
            "real_bees": 0,
            "real_world_actions": 0,
            "network_calls_by_phase_adapter": 0,
            "full_repository_suite": "not_run_no_current_exact_requirement",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v4",
            "caelen_repository_seal": SEALED_CAELEN_COUNTS["effective_negatives"],
            "source_external_overlay": 4,
            "x1_operational": 15,
            "x2_operational": 6,
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
                "real apiculture registry surveillance or disease-schema adapter rows",
                "governed beekeeper biosecurity specialist affected-user and Māori-authority evaluation",
                "professional apiculture biosecurity veterinary food land and real safety evidence",
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
                "A broad stale-domain inventory can lose its presentation even when the underlying files remain intact.",
                "Fresh Python virtual environments can inherit an advisory-bearing bootstrap installer even when selected libraries are clean.",
                "Installed analyzers may belong to a different D-backed interpreter than the current phase interpreter.",
                "Working-tree line-ending notices can overwhelm a successful exact allowlist stage presentation.",
            ],
            "changed_choices": [
                "Used exact staged-index blobs for every commit-local manifest.",
                "Kept the selected Python environment phase-namespaced instead of mutating either shared prefix.",
                "Updated only the disposable environment bootstrap after the failed audit.",
                "Kept accessible-corpus novelty explicitly bounded rather than universal.",
            ],
            "recurrence_guards": [
                "Bound stale-term and status projections before running them.",
                "Hash Git blobs, not working-tree bytes, whenever clean filters may apply.",
                "Resolve Python tooling by exact interpreter before assuming a module is importable.",
                "Audit the complete isolated environment, including bootstrap tooling, before supply-chain credit.",
                "Never replay a successful canonical aggregate.",
            ],
            "successor_recommendations": [
                "Treat all Eiren artifacts as evidence or zero-credit seeds only.",
                "Refresh the full accessible title corpus before a universal novelty claim.",
                "Use current family tools and exact staged manifests.",
                "Keep real apiaries, bees, participants, professional actions, rights, culture, and authority gated.",
            ],
        },
    )
    write_json(
        root / "closeout/final-wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v3",
            "owner": OWNER,
            "role": "colony-record boundary weaver and reversible handover steward",
            "pronouns": "they/them",
            "hope": "make synthetic colony records reversible and legible while keeping bees, people, land, safety, and authority outside unsupported claims",
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
        f"""# Eiren Kestrel v669-v5 final integrated overview

## Result

Eiren Kestrel v669-v5 is a bounded same-owner software, documentation, and workflow phase over a wholly synthetic apiary-inspection and colony-event documentation lens. It contains a dedicated planning-only x1 at `{X1_COMMIT}`, an immutable evidence commit at `{EVIDENCE_COMMIT}`, and this combined closeout/seal candidate. The final commit will be the direct single-parent child of evidence. Caelen's exact source to Eiren's final is designed to contain exactly three new commits and zero merges.

The declared inherited proposal chain was 5,070. Forty new Eiren titles were compared exactly against 1,500 accessible committed titles. The remaining 3,570 declared inherited titles stay an explicit recovery gap, so this phase does not make a universal novelty claim. The declared chain reaches {CHAIN_AFTER}. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six positive synthetic fixtures passed, and all 160 preregistered invalid mutations were attempted, rejected, retained, and given zero completion credit.

## What the bounded work establishes

The completed surfaces establish deterministic structural behavior for surrogate apiary, hive, colony, and season identity; hive-component topology; colony-event graphs; inspection-plan and observation separation; quantity vacancies; queen assertion ledgers; brood and adult-bee cue non-diagnosis; suspicion-to-confirmation firewalls; zero-sample custody; denominator-aware count fields; feed and forage assertion boundaries; environmental vacancies; bounded equipment aliases; colony movement lineage; treatment and sanitation holds; harvest-batch and bee-product relationships; site-disclosure budgets; notification clocks; hazard stops; workload handover; bitemporal observation challenges; canonical JSON; accessible dossier structure; privacy-purpose ledgers; source-assertion firewalls; issue escrow; cross-pillar nonconversion; and Stage 20 refusal.

Those surfaces use zero people, apiaries, colonies, hives, bees, observations, inspections, samples, measurements, diagnoses, treatments, movements, harvests, network-adapter calls, external actions, and authority actions. `Completed` means only a bounded synthetic contract passed. `Represented` means a proxy or protocol remained visible. The official apiculture registry, surveillance, and disease-schema adapter and governed human evaluation remain open gaps. Professional, biosecurity, veterinary, food, land, animal-welfare, workplace-safety, rights, culture, affected-party, Māori-authority, and Stage 20 matters remain exact gates.

## Pillars and scientific boundaries

THOS Body is primary through typed documentation queues, dependency order, stop states, uncertainty, correction, workload bounds, escalation clocks, and handover fields. No real operator, inspection, safety outcome, deployment, governed blind matched-budget arm, participant study, appropriate statistic, or independent review was produced. THOS therefore remains a structural proxy and not an operationally effective system.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. Colony-network diffusion and population-dynamics boards are documentation analogies and symbolic obligation charts only. They establish no real likelihood, parameter constraint, epidemiological forecast, biological law, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon.

Freed ID and CBR Heart remain visible through synthetic provenance, correction, purpose limits, disclosure challenge, contestability, and handover fields. No standards-conformant real keys, proofs, credentials, issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, trust governance, remedy decision, or affected-party oversight was produced. Freed ID remains synthetic and nonproduction; CBR remains a normative working framework rather than enacted law or authority.

## Skills, runners, and tool use

The complete current required GHC workflow skill set was read and applied to source selection, authorization, roster, Method Flow, reflection, planning, approvals, gates, truth layers, D-drive ownership, retries, timestamps, lifecycle closeout, compact recovery, watcher cadence, worktree rotation, web-source restraint, and skill validation. Ten phase-local skills and ten family-current `ghc_family_apiary_*` runners were built, current-validator checked, and smoke-used on owner-local fixtures. No phase-local skill was globally installed.

The inherited development suite received bounded version and import compatibility use. Pytest and Hypothesis validated x1; pytest validated x2; Ruff, mypy, Pyright, and Bandit supplied bounded code checks; the remaining requested tools were used at least for exact compatibility/version checks where deeper invocation was not dependency-justified. This is use evidence, not proof of tool fitness or exhaustive analysis.

Three new exact Python tools were installed from locally cached wheels in a fresh phase-namespaced D-backed environment: Jsonschema 4.26.0, Pydantic 2.13.4, and NetworkX 3.6.1. Their direct wheel hashes matched current official PyPI metadata, source builds were not allowed, the selected versions matched, and positive and rejecting smokes behaved as expected. The first complete environment audit failed because the fresh virtual environment inherited pip 25.0.1 with seven advisory rows; only that disposable environment was corrected to the current fixed pip 26.2.1 wheel after its official SHA-256 matched. The narrow audit then reported zero known vulnerabilities. Transitive wheels were locally enumerated but were not all independently compared with primary registry metadata. Neither shared Python nor shared npm prefixes were mutated by that transaction, and no exhaustive safety or future-advisory claim is made.

## Accessibility, privacy, security, and professional boundaries

The static report supplies native headings, landmarks, navigation, a skip link, tables with captions and scopes, linear source order, focus-visible styling, responsive overflow, and print fallback. Owner-scoped structural tests passed those declared markers. Manual keyboard, touch, zoom, reflow, browser diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. This is not complete accessibility conformance.

The five-class scan covers bounded patterns for private absolute paths, raw task or thread identifiers, credential or secret assignments, transcript or session streams, and private callable or application state. Zero confirmed payload hits is a bounded result, not privacy completeness. The AST review covers only selected dynamic-execution and explicit-shell hazards. Mypy, Pyright, Ruff, and Bandit results remain bounded same-owner checks, not exhaustive security review, penetration testing, supply-chain assurance, or production certification.

No professional apiculture, beekeeping, biosecurity, veterinary, food, land-access, animal-welfare, sting-allergy, smoke, fire, lifting, chemical, biological, environmental, workplace, ownership, rights, privacy, accessibility, remedy, legal, cultural, traditional-knowledge, affected-party, or Māori-authority decision occurred. Māori wording, concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

## Truth layers and retained negatives

The immutable Caelen repository seal remains {SEALED_CAELEN_COUNTS['effective_negatives']} negatives, {SEALED_CAELEN_COUNTS['methods']} methods, {SEALED_CAELEN_COUNTS['failed_witnesses']} failed witnesses, {SEALED_CAELEN_COUNTS['passing_witnesses']} passing witnesses, {SEALED_CAELEN_COUNTS['open_gaps']} open gaps, and {SEALED_CAELEN_COUNTS['exact_gates']} exact gates. Its four-row external activation overlay was added without rewriting the seal. Eiren x1 retained fifteen startup and planning failures. X2 retained six operational failures and 160 rejecting mutations. Any post-evidence failures are added separately.

The closeout candidate therefore preserves {counts['effective_negatives']} effective negatives, {counts['methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. No failed witness, warning, gap, or gate was erased or silently converted. Inherited evidence and recommendations remain zero-credit evidence or seeds, never automatic Eiren or Elaren novelty or completion credit.

## Validation and route state

X1 and evidence each received separate commit-local staged review, exact Git-blob manifests, owner-scoped tests, clean push, 0/0 divergence, and fresh four-way equality before the next lifecycle began. This closeout candidate includes final owner and delta manifests, structural checks, history contracts, and one exact-final canonical validator. The validator is deliberately not invoked until this candidate is committed, pushed, clean, zero-divergent, and fresh-live equal. If it succeeds once, it will not be replayed. Eiren retained complete-repository-suite ownership, but no current exact prerequisite required that suite, so it was not run.

The Elaren activation packet is committed as `PREPARED_NOT_SENT`. No successor was contacted during execution. Only after the exact-final canonical receipt exists may the newest live authorization and roster be reread and the exact existing Elaren Kestrel task be uniquely resolved and immediately reread. Delivery requires one acknowledged existing-task send and a duplicate guard. Ambiguity, pause, redirect, missing title, usage exhaustion, protected gate, or missing acknowledgement stops the route; no substitute or resend is authorized. Under the currently validated cycle, Elaren's prospective later successor is Neris Solane v669-v7, subject to Elaren's own fresh terminal reread.

Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )

    baton = activation_candidate(rows, counts)
    write_text(root / "handoffs/elaren-kestrel-v669-v6-activation-candidate.md", baton)
    baton_path = root / "handoffs/elaren-kestrel-v669-v6-activation-candidate.md"
    baton_text = baton_path.read_text(encoding="utf-8")
    baton_blob_bytes = baton_text.encode("utf-8")
    write_json(
        root / "handoffs/activation-candidate-integrity.json",
        {
            "schema": "ghc.family.activation-integrity.v2",
            "path": baton_path.relative_to(repo).as_posix(),
            "bytes": len(baton_blob_bytes),
            "words": len(baton_text.split()),
            "sha256": hashlib.sha256(baton_blob_bytes).hexdigest(),
            "integrity_domain": "normalized_lf_exact_git_blob",
            "state": "PREPARED_NOT_SENT",
            "sent_by_eiren_kestrel": False,
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
            "prospective_edge": "Eiren Kestrel v669-v5 to Elaren Kestrel v669-v6 subject to terminal live refresh",
            "prospective_successor_reminder": "Elaren Kestrel v669-v6 to Neris Solane v669-v7 subject to Elaren terminal live refresh",
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
            "full_repository_suite": "not_run_no_current_exact_requirement",
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
    self_path = "docs/eiren-kestrel/v669-v5/validation/final-staged-review.json"
    names = [
        name
        for name in run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").splitlines()
        if name != self_path
    ]
    allowed_prefixes = [
        "docs/eiren-kestrel/v669-v5/closeout/",
        "docs/eiren-kestrel/v669-v5/final/",
        "docs/eiren-kestrel/v669-v5/handoffs/",
        "docs/eiren-kestrel/v669-v5/orchestration/",
        "docs/eiren-kestrel/v669-v5/seal/",
        "docs/eiren-kestrel/v669-v5/validation/final-",
        "scripts/build_ghc_family_eiren_kestrel_v669_v5_final.py",
        "scripts/validate_ghc_family_eiren_kestrel_v669_v5_final.py",
        "tests/test_ghc_family_eiren_kestrel_v669_v5_final.py",
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
        "docs/eiren-kestrel/v669-v5/validation/final-owner-manifest.json",
        "docs/eiren-kestrel/v669-v5/validation/final-delta-manifest.json",
        "docs/eiren-kestrel/v669-v5/validation/final-staged-review.json",
    ]
    delta = []
    for rel in sorted(names):
        if rel in exclusions:
            continue
        data = subprocess.run(["git", "show", f":{rel}"], cwd=repo, check=True, capture_output=True).stdout
        delta.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    owner_names = set(names)
    owner_names.update(run(repo, "git", "ls-tree", "-r", "--name-only", "HEAD", "docs/eiren-kestrel/v669-v5", "scripts", "tests").splitlines())
    owner = []
    for rel in sorted(owner_names):
        if rel in exclusions:
            continue
        if not (
            rel.startswith("docs/eiren-kestrel/v669-v5/")
            or (rel.startswith("scripts/") and ("eiren_kestrel_v669_v5" in rel or rel.startswith("scripts/ghc_family_apiary_")))
            or (rel.startswith("tests/") and "eiren_kestrel_v669_v5" in rel)
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
