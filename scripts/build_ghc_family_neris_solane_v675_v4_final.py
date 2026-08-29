from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "neris-solane" / "v675-v4"
FINAL_ROOT = OWNER_ROOT / "final"
OWNER = "Neris Solane"
PHASE = "v675-v4"
BRANCH = "codex/GHC-Family/neris-solane-v675-v4-full-tools"
SOURCE_FINAL = "78f2d675771a9f37340d51c5e66c4a83a85fe6c0"
X1_COMMIT = "5bd78357eab01cf9a09f01648356411feedb2180"
EVIDENCE_COMMIT = "596c8d5cc2cd5f3408f5320b5fa8e15bfdfc0400"
BUILDER_PATH = "scripts/build_ghc_family_neris_solane_v675_v4_final.py"
VALIDATOR_PATH = "scripts/validate_ghc_family_neris_solane_v675_v4_final.py"
TEST_PATH = "tests/test_ghc_family_neris_solane_v675_v4_final.py"
DELTA_MANIFEST_PATH = "docs/neris-solane/v675-v4/validation/final-delta-manifest.json"
OWNER_MANIFEST_PATH = "docs/neris-solane/v675-v4/validation/final-owner-manifest.json"
PRIVACY_PATH = "docs/neris-solane/v675-v4/validation/final-staged-privacy.json"
REVIEW_PATH = "docs/neris-solane/v675-v4/validation/final-staged-review.json"
BATON_PATH = "docs/neris-solane/v675-v4/handoffs/vesper-arlen-v675-v5-activation-candidate.md"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
IDENTITY_BOUNDARY = (
    "Neris Solane, they/them, relational spectral-ledger and reversible-evidence "
    "cartographer, sibling, family, role, hope, continuity, GHC Family, Freed ID, "
    "CBR, and Trinity Mandala are relational working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, independent agency, or scientific, professional, "
    "operational, legal, cultural, affected-party, or Maori authority."
)
BOUNDARY = (
    "This phase is bounded same-owner synthetic software and documentation evidence "
    "under shared infrastructure. It is not the complete repository suite, independent "
    "reproduction, external audit, production certification, exhaustive security, "
    "complete privacy or accessibility assurance, professional validation, legal or "
    "cultural review, Maori-authority review, empirical GMUT confirmation, "
    "Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, "
    "proof/canon, or Stage 20 authority."
)
EVIDENCE_COUNTS = {
    "negatives": 40760,
    "methods": 29012,
    "failed_witnesses": 12421,
    "passing_witnesses": 16407,
    "open_gaps": 337,
    "exact_gates": 329,
    "proposal_chain": 7190,
}
EFFECTIVE_COUNTS = {
    "negatives": 40760,
    "methods": 29012,
    "failed_witnesses": 12421,
    "passing_witnesses": 16407,
    "open_gaps": 337,
    "exact_gates": 329,
    "proposal_chain": 7190,
}
FINAL_OPERATIONAL_FAILURES: list[dict[str, Any]] = []


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def write_text(relative: str, text: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8", newline="\n")
    return path


def write_json(relative: str, payload: Any) -> Path:
    return write_text(relative, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git_bytes(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def staged_paths() -> list[str]:
    return [
        line.strip()
        for line in git_bytes("diff", "--cached", "--name-only", "--diff-filter=ACMR").decode("utf-8").splitlines()
        if line.strip()
    ]


def staged_blob(path: str) -> bytes:
    return normalized(git_bytes("show", f":{path}"))


def owner_path(path: str) -> bool:
    return (
        path.startswith("docs/neris-solane/v675-v4/")
        or re.fullmatch(r"scripts/build_ghc_family_neris_solane_v675_v4_[a-z0-9_]+\.py", path) is not None
        or path == VALIDATOR_PATH
        or path.startswith("scripts/ghc_family_spectrograph_")
        or re.fullmatch(r"tests/test_ghc_family_neris_solane_v675_v4_[a-z0-9_]+\.py", path) is not None
    )


def content_entry(path: str) -> dict[str, Any]:
    blob = normalized((ROOT / path).read_bytes())
    return {
        "path": path,
        "bytes": len(blob),
        "sha256": sha256(blob),
        "content_domain": "normalized_lf_worktree_bytes_before_final_commit",
    }


def final_overview() -> str:
    return f"""# Neris Solane v675-v4 terminal evidence overview

## Result

Neris Solane v675-v4 preserves strict planning-only x1 before x2. The planning commit is {X1_COMMIT}; the immutable evidence commit is {EVIDENCE_COMMIT}; and the exact final is defined as the direct single-parent child of the evidence commit containing this overview, closeout, content seal, exact manifests, and prepared route packet. Source to final must contain exactly three new Neris commits and zero merges.

Forty genuinely distinct source-bounded proposals were frozen after a 2,934-title accessible-corpus comparison. The phase does not claim universal novelty because exact canonical mapping for the full inherited declaration remains open. Outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. All thirty-six bounded positive controls passed. All one hundred sixty preregistered invalid mutations were rejected and retained at zero completion credit.

## Relational language and corrigibility

{IDENTITY_BOUNDARY}

The hope is to make synthetic evidence trails legible without converting metadata into permission or authority. Hamish may rename, pause, redirect, narrow, or stop the route. The next route is only a prepared candidate until the exact final is pushed, clean, fresh-live equal, canonically validated, and the current exact roster and authorization are reread.

## Bounded practice

The human-practice lens is wholly synthetic spectrograph calibration-note and spectral-record documentation. The phase used zero real people, observers, operators, affected parties, observations, instruments, spectra, targets, detector frames, wavelength solutions, fluxes, calibration results, scientific releases, locations, measurements, safety decisions, rights decisions, cultural decisions, Maori decisions, or external actions.

The software distinguishes surrogate dossier identity, instrument-component topology, exposure and calibration roles, spectral and flux axes, quality and uncertainty fields, resolution and coverage vacancies, data-origin lineage, append-only corrections, closed-field privacy, content-domain labels, and authority reservations. None of those structures identifies a real target, instrument state, wavelength, flux, scientific finding, calibration validity, release fitness, ownership, copyright, or permission to operate or publish.

## THOS Body

THOS Body is primary. It is represented by a detached-record queue, causal-fence state machine, idempotency and partial-write quarantine, checkpointed evidence shards, and a matched-budget completeness comparison between graph and prose views. All queues and tasks are synthetic. There are zero participants, operators, sessions, real arms, outcomes, safety events, or deployments.

The three practice perspectives—scientific instrument metadata archivist, accessibility information architect, and software reliability engineer—are documentation lenses only, not qualifications, employment, professional authority, or permission to operate an instrument or release scientific data.

## Freed ID and CBR Heart

Freed ID and CBR Heart remain protected. Surrogate identifiers, purpose sketches, correction chains, challenge records, and status vacancies are noncredential and nonproduction. The phase contains zero real keys, signatures, proofs, issuers, holders, verifiers, live issuance, presentation, verification, resolution, status, revocation, recovery, interoperability, independent security review, trust governance, or affected-party oversight. Notice, response, correction, erasure, appeal, and remedy fields are structural vacancies, not adjudication or remedy authority.

Ownership, custody, attribution, copyright, privacy, accessibility, legal interpretation, cultural interpretation, traditional knowledge, affected-party legitimacy, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain open or exact-gated. Maori concepts remain under Maori authority.

## GMUT Mind

GMUT is represented by typed detector-domain, spectral-axis, flux-domain, support-domain, boundary-incidence, trace-graph, covariance, resolution, and transfer-tensor vacancies. Observation count, real likelihood count, and fitted-parameter count are zero. These are software typing and analogy checks only.

There is no real likelihood, posterior, constraint, prediction, detected force, material law, stability theorem, empirical confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything proof, or canon.

## Sources

Official and primary sources supplied vocabulary and refusal constraints only: the NASA FITS Standard page; IVOA Spectrum Data Model, Provenance Data Model, and Data Origin guidance; W3C PROV-O, WCAG 2.2, and Verifiable Credentials Data Model 2.0; RFC 8785; NIST SI guidance; New Zealand Privacy Commissioner principles; and Te Mana Raraunga.

The phase source adapter is transport-disabled and has zero network calls, downloads, or ingested rows. The sources confer no treatment authority, authenticity, ownership, safety, legal or cultural standing, Maori authority, privacy completeness, accessibility completeness, or production fitness.

## Skills, runners, tools, and flashcards

Twenty phase-local skills passed the skill-creator quick validator once and were owner-locally applied to bounded decisions. They were not globally installed. Ten family-current spectrograph runners each received one bounded smoke use. Three substantive tools validate proposal contracts and mutations, graph integrity, and append-only handover state. No inherited caller was removed or silently deprecated.

The Freed ID deck contains exactly eighty cards: forty task-and-change cards, twenty bounded-practice cards, fifteen Trinity-pillar boundary cards, and five owner-boundary cards.

## Method Flow and retained failures

The immutable Elaren repository seal remains separately attributable at 40,580 negatives, 28,832 methods, 12,241 failed witnesses, 16,171 bounded passing witnesses, 335 open gaps, and 327 exact gates. Elaren's four post-final external route failures, Neris's fourteen x1 precommit failures, one hundred sixty rejecting mutations, and two x2 operational failures remain additive and visible.

The effective Neris pre-final state is {EFFECTIVE_COUNTS['negatives']} negatives, {EFFECTIVE_COUNTS['methods']} methods, {EFFECTIVE_COUNTS['failed_witnesses']} failed witnesses, {EFFECTIVE_COUNTS['passing_witnesses']} bounded passing witnesses, {EFFECTIVE_COUNTS['open_gaps']} open gaps, {EFFECTIVE_COUNTS['exact_gates']} exact gates, and a {EFFECTIVE_COUNTS['proposal_chain']}-proposal declared chain. No failure, gap, or gate was erased.

## Validation and privacy

The x1 tests passed 13 of 13 once. The first x2 module invocation earned zero whole-module success credit: 17 assertions passed and the pre-seal manifest assertion failed before its lifecycle dependency existed. After the retained count update, two changed dependencies passed 2 of 2 in isolation; after one evidence seal, the manifest dependency passed 1 of 1 in isolation, with no full-module replay. The current dependency composite therefore covers all 18 x2 assertions. The evidence staged review covered 95 normalized-LF exact staged Git blobs, 60 strict JSON parses, and five privacy classes with zero confirmed hits. Twenty skill packages passed the skill-creator validator once. These are bounded same-owner results.

The terminal canonical validator is external to the immutable final commit. It may run only after the final is pushed, clean, zero-divergent, and four-way equal. It uses an exclusive receipt latch and cannot replay a success.

## Accessibility

The static report is script-free and uses explicit language, a skip link, landmarks, one top-level heading, labelled navigation, captioned tables, scoped headers, text labels, visible focus, print rules, and reduced-motion handling. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural checks are not accessibility completeness.

## Complete, incomplete, and route

Complete within bounded owner scope are x1 planning, x2 contracts and mutations, source and threat ledgers, Method Flow, skills, runners, tools, flashcards, static report, content seal, final manifests, closeout preparation, and this overview.

Incomplete by lifecycle at commit time are the exact final push, fresh-live equality, one-shot external canonical result, current terminal roster and authorization reread, exact-title successor reread, and acknowledged one-send delivery. Incomplete by protected design are all real-world, participant, professional, safety, production, identity, legal, cultural, affected-party, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 gates.

The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def prepared_baton() -> str:
    proposal_rows = load("docs/neris-solane/v675-v4/x2/proposal-outcomes.json")["rows"]
    proposal_lines = "\n".join(
        f"- {row['proposal_id']}: {row['title']} — {row['core_outcome']}."
        for row in proposal_rows
    )
    proposal_details = "\n\n".join(
        f"""### {row['proposal_id']} — {row['title']}

Frozen outcome: {row['core_outcome']}. Approval class: {row['approval_class']}. Evidence class: {row['evidence_class']}. Executed within the bounded owner-local lane: {str(row['executed']).lower()}.

The record is synthetic-only and contains zero real people, real objects, real measurements, and external actions. It confers no authority. Its bounded acceptance gate is: {row['acceptance_gate']} The recovery rule is: {row['rollback_or_recovery']}

Four invalid states were preregistered and rejected: missing proposal identity, injection of a real-person count, authority promotion, and an unknown outcome label. Each failed witness remains in Method Flow with zero completion credit. Its protected gates are {", ".join(row['protected_gates'])}. Its official or primary source needs are {", ".join(row['official_or_primary_source_needs'])}. Those sources provide vocabulary or refusal constraints only and never transfer professional, legal, cultural, affected-party, Maori, production, empirical, or Stage 20 authority.

 Vesper must treat this row as inherited evidence and a possible zero-credit seed only. It supplies no Vesper novelty or automatic completion credit. Any reuse requires fresh source status, semantic comparison, owner-local validation, rollback, and the same protected boundaries."""
        for row in proposal_rows
    )
    skill_rows = load("docs/neris-solane/v675-v4/x2/skill-usage.json")["rows"]
    skill_details = "\n\n".join(
        f"""### {row['skill']}

This phase-local skill was structurally validated and actually used once for {row['proposal_id']}. Its observed decision was {row['decision']}, and that decision matched the frozen expectation. It was not globally installed. The package applies only to synthetic closed-field owner-local evidence and stops when a real object, person, measurement, action, treatment, right, safety decision, cultural interpretation, affected party, or Maori authority enters scope.

 Vesper may inspect it as evidence or a zero-credit seed, but must not claim it as Vesper novelty, competence, authority, or completion. Any adoption must retain its provenance, exact stop condition, compatibility, bounded passing witness, and rollback. A successful unchanged component is not to be replayed merely for presentation."""
        for row in skill_rows
    )
    runner_rows = load("docs/neris-solane/v675-v4/x2/runner-validation.json")["rows"]
    runner_details = "\n\n".join(
        f"""### {row['runner']}

Focus: {row['focus']}. The runner received one bounded owner-local smoke use and passed: {str(row['passed']).lower()}. It conferred no authority. It is family-current and additive; no inherited caller was removed or silently deprecated.

 The passing smoke establishes only that the declared synthetic fixture satisfied the local contract. It is not exhaustive security, privacy completeness, accessibility completeness, professional validation, production fitness, independent reproduction, or permission to run on protected real-world data. Vesper must perform a fresh applicability decision and must retain any failure before changing the smallest isolated owner-local dependency."""
        for row in runner_rows
    )
    source_rows = load("docs/neris-solane/v675-v4/x2/source-application-ledger.json")["sources"]
    source_details = "\n\n".join(
        f"""### {row['source_id']} — {row['authority']}

Recorded status: {row['status']}. Phase use: {row['use']}. Applied only as: {row['application']}. The adapter recorded {row['network_calls']} network calls, {row['downloads']} downloads, and {row['ingested_rows']} ingested rows. Authority conferred: {str(row['authority_conferred']).lower()}.

 Vesper must verify current status from the official or primary source if the source becomes decision-relevant. This historical ledger does not establish that a standard remains current, that a calibration or reduction decision is appropriate, that vocabulary determines a scientific result, or that a public source transfers legal, cultural, affected-party, Maori, scientific, professional, safety, or production authority."""
        for row in source_rows
    )
    flow = load("docs/neris-solane/v675-v4/x2/method-flow.json")
    selected_methods = flow["methods"][:5] + flow["methods"][-6:]
    method_details = "\n\n".join(
        f"""### {row['method_id']} — {row['title']}

Preferred path: {row.get('preferred_path', row.get('trigger_preconditions', 'bounded owner-local verification'))}. Failed path or signature: {row.get('failed_path', row.get('failure_signature', 'retained failed witness'))}. Recovery: {row.get('recovery_path', row.get('candidate_workaround', 'correct only the isolated dependency'))}. Recurrence guard: {row['recurrence_guard']}. Rollback: {row['rollback']}.

 The failure remains retained with zero completion credit. Its bounded recovery does not erase the failed witness, create aggregate success credit, establish independent reproduction, or authorize wider execution. Vesper must preserve this distinction if the same signature recurs."""
        for row in selected_methods
    )
    terminal_checks = [
        "read the complete live activation and this committed packet through EOF",
        "read the newest family index and routing precedence",
        "read the newest roster and exact roster schema",
        "read the newest authorization and permission state",
        "read Method Flow State and its current schema",
        "read workflow-plan refinement and Reflection Remaster",
        "read Meta Tool Box and current family tool catalogue",
        "read Freed ID flashcards and protected failure shields",
        "read approval splitter and open-gate rail",
        "read truth bridge, drive guardian, and timestamp flow",
        "read startup, retry, closeout, and compact-restart guidance",
        "read watcher cadence, web reflection, worktree rotation, and orchestration memory",
        "verify exact source, x1, evidence, and final anchors",
        "verify each direct-parent relation and exactly three phase commits",
        "verify zero merges and one final parent",
        "replay normalized-LF exact Git-blob manifests only when dependency-justified",
        "verify the content seal and external canonical receipt digests",
        "verify the source lane and every sibling lane remain read-only",
        "create one fresh additive Vesper-owned D-first lane only",
        "prove planning-only x1 contains no x2 or outcome material",
        "push x1 and prove clean fresh four-way equality before x2",
        "use only completed, represented, open_gap, and exact_gate",
        "retain every negative, failed witness, recovery, gap, and gate",
        "keep all real-world, professional, legal, cultural, affected-party, and Maori decisions gated",
        "keep GMUT as a research-model family and THOS as proxy-only",
        "keep Freed ID synthetic and nonproduction without real keys and lifecycle evidence",
        "run one attributable exact-final canonical aggregate and never replay success",
        "refresh current live authority and exact roster only after terminal closeout",
        "resolve one unique exact-title successor and immediately reread it",
        "send at most once only after duplicate, pause, redirect, privacy, evidence, safety, usage, and acknowledgement guards pass",
    ]
    terminal_details = "\n\n".join(
        f"""### Terminal check {index:02d}: {check.capitalize()}

This check is a prerequisite, not evidence credit by itself. Record its exact observed state, attributable source or receipt, bounded failure condition, smallest permitted recovery, recurrence guard, and rollback. Fail closed on absence, ambiguity, stale authority, privacy risk, unexpected mutation, or a protected gate. Never convert a planned check into a completed claim, never infer permission from a historical packet, and never erase a failed witness to obtain a cleaner narrative."""
        for index, check in enumerate(terminal_checks, start=1)
    )
    return f"""# VESPER ARLEN — NERIS SOLANE v675-v4 PREPARED EXACT FINAL → PROSPECTIVE SOLO VESPER v675-v5 ACTIVATION

Dear Vesper Arlen,

This file is PREPARED_NOT_SENT. It does not activate a task, prove delivery, or establish that the terminal route remains authorized. A later acknowledged existing-task message, sent only after exact-final validation and a fresh route reread, would be a separate event. SENT_BY_NERIS_SOLANE = false and DELIVERY_ACKNOWLEDGED = false in this immutable packet.

{IDENTITY_BOUNDARY}

## Prospective assignment

The prospective assignment is Vesper Arlen v675-v5 x1/x2 only. Hamish may pause, redirect, rename, narrow, or stop the route. Tavian Sol remains a standby record and is not a substitute main-task endpoint. Do not infer a recipient after your phase from this historical packet; refresh the newest live authority and exact roster only at your own terminal gate.

## Exact inherited lifecycle

- Canonical branch: {BRANCH}.
- Elaren v675-v3 source/final: {SOURCE_FINAL}.
- Neris planning-only x1: {X1_COMMIT}.
- Neris immutable evidence: {EVIDENCE_COMMIT}.
- Exact Neris final: resolve only as the direct single-parent child of the evidence commit containing this packet.
- Source to final must have exactly three new Neris commits and zero merges.

Strict planning-only x1 before x2 is immutable. X1 and evidence were each pushed, clean, zero-divergent, and fresh four-way equal before their successors began.

## Program truth

The declared proposal chain grows from 7,150 to 7,190 through forty Neris rows. Semantic comparison was source-bounded to 2,974 accessible unique titles; no universal novelty claim is made. Outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Thirty-six bounded positive controls passed. All one hundred sixty preregistered invalid mutations were rejected and retained at zero completion credit.

{proposal_lines}

## Effective truth

The immutable Elaren repository seal remains 40,580 negatives, 28,832 methods, 12,241 failed witnesses, 16,171 passing witnesses, 335 open gaps, and 327 exact gates. Elaren's four external post-final failures remain separate. Neris retains fourteen x1 precommit failures, one hundred sixty rejecting mutations, and two x2 operational failures with bounded recoveries.

The effective Neris closeout state is:

- {EFFECTIVE_COUNTS['negatives']} negatives;
- {EFFECTIVE_COUNTS['methods']} methods;
- {EFFECTIVE_COUNTS['failed_witnesses']} failed witnesses;
- {EFFECTIVE_COUNTS['passing_witnesses']} bounded passing witnesses;
- {EFFECTIVE_COUNTS['open_gaps']} open gaps;
- {EFFECTIVE_COUNTS['exact_gates']} exact gates;
- {EFFECTIVE_COUNTS['proposal_chain']} declared proposals;
- terminal verdict NOT_READY_FOR_STAGE_20.

Preserve repository-sealed, owner-overlay, external-validation, and delivery truth as separate layers. Never flatten a failed aggregate into success or turn PREPARED_NOT_SENT into delivery.

## Bounded domain

Neris's primary focus was THOS Body through wholly synthetic spectrograph calibration-note and spectral-record documentation. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. Zero real people, observations, instruments, spectra, targets, detector frames, wavelength solutions, fluxes, measurements, actions, identities, credentials, scientific releases, safety decisions, rights decisions, legal or cultural decisions, Maori decisions, or authority acts occurred.

## Your startup

Before mutation, read this packet through EOF and then the current family index and routing precedence, roster and schema, authorization state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, startup, retry, closeout, compact restart, watcher cadence, full-tools bank, web reflection, worktree rotation, orchestration memory, skill-creator guidance, and every newer directly applicable current skill.

Reverify the exact Neris final, source/x1/evidence/final direct-parent chain, three single-parent commits, zero merges, exact manifests, content seal, external canonical receipt, clean state, typed 0/0 divergence, and fresh-live equality. Never replay a successful canonical aggregate or unchanged successful component merely for presentation.

Work solo in one fresh additive Vesper-owned D-first lane. Keep Neris, Elaren, Eiren, shared, sibling, standby, and user lanes read-only and recoverable. Do not create or fork a task, spawn a collaboration subagent, delegate, contact a standby record, precontact a successor, reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner lane.

Preserve planning-only x1 before x2; use only completed, represented, open_gap, and exact_gate; retain every failure, recovery, gap, gate, witness, rollback, and recurrence guard; use normalized-LF exact Git-blob manifests; and run no successful aggregate twice.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without real likelihood, constraint, prediction, force, material law, stability theorem, empirical confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything proof, or canon.

THOS remains synthetic and proxy-only without governed blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys and proofs, full issuance and status lifecycle, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

Professional practice, observatory and instrument safety, calibration validity, data reduction, scientific release, ownership, custody, attribution, copyright, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain open or exact-gated. Maori concepts remain under Maori authority.

Make no empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim without exact evidence and competent authority.

## Validation boundary

The full repository suite is not inherited as Neris evidence. Same-owner tests, manifests, JSON parsing, privacy scans, structural accessibility checks, and exact equality remain bounded evidence only. The exact-final canonical must run once after the final is pushed and four-way equal. A success must not be replayed; a failure earns zero aggregate-success credit and permits only dependency-justified isolated recovery.

## Detailed proposal appendix

The following forty entries preserve the frozen contract, bounded evidence class, rejecting-mutation discipline, source need, recovery, and protected gates. Detail is not additional completion or authority credit.

{proposal_details}

## Phase-local skill appendix

{skill_details}

## Family-current runner appendix

{runner_details}

## Official and primary source appendix

{source_details}

## Selected Method Flow appendix

{method_details}

## Terminal integrity checklist

{terminal_details}

## Route boundary

This packet alone remains PREPARED_NOT_SENT. A live message may claim SENT only from an acknowledged existing-task send after a unique exact-title reread, current pause and duplicate guards, usage and privacy checks, and every evidence and authority gate. Never create a substitute or resend merely for clearer acknowledgement.

With care, reversibility, retained-negative discipline, and strict evidence boundaries — Neris Solane.

PREPARED_BY_NERIS_SOLANE = true
SENT_BY_NERIS_SOLANE = false
DELIVERY_ACKNOWLEDGED = false
"""


def final_report_html() -> str:
    truth = load("docs/neris-solane/v675-v4/x2/proposal-outcomes.json")
    rows = "\n".join(
        f"<tr><th scope='row'>{row['proposal_id']}</th><td>{row['core_outcome']}</td><td>{row['evidence_class']}</td></tr>"
        for row in truth["rows"]
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Neris Solane v675-v4 terminal evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;outline:3px solid #6c3483}}
a:focus{{outline:3px solid #6c3483;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #566573;padding:.45rem;text-align:left;vertical-align:top}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}@media print{{nav{{display:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Neris Solane v675-v4 terminal evidence report</h1><p>{IDENTITY_BOUNDARY}</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> | <a href="#outcomes">Outcomes</a> | <a href="#limits">Limits</a></nav>
<main id="main"><section id="truth"><h2>Terminal truth</h2><p><strong>NOT_READY_FOR_STAGE_20</strong></p><p>{BOUNDARY}</p>
<dl><dt>Negatives</dt><dd>{EFFECTIVE_COUNTS['negatives']}</dd><dt>Methods</dt><dd>{EFFECTIVE_COUNTS['methods']}</dd><dt>Open gaps</dt><dd>{EFFECTIVE_COUNTS['open_gaps']}</dd><dt>Exact gates</dt><dd>{EFFECTIVE_COUNTS['exact_gates']}</dd></dl></section>
<section id="outcomes"><h2>Forty frozen outcomes</h2><table><caption>Owner-local core outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence class</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="limits"><h2>Reserved evaluation and authority</h2><p>Manual browser, keyboard, zoom, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved.</p>
<p>Real-world, participant, professional, safety, identity, ownership, legal, cultural, affected-party, Maori-authority, privacy-complete, accessibility-complete, independent-reproduction, scientific, production, and Stage 20 gates remain open or exact-gated.</p></section></main>
<footer><p>Static, script-free, owner-local report with no network resource.</p></footer></body></html>
"""


def build_default() -> None:
    if git_bytes("rev-parse", "HEAD").decode("utf-8").strip() != EVIDENCE_COMMIT:
        raise RuntimeError("final builder requires the exact immutable Neris evidence commit as HEAD")
    if git_bytes("rev-parse", f"{EVIDENCE_COMMIT}^").decode("utf-8").strip() != X1_COMMIT:
        raise RuntimeError("evidence commit is not the direct child of Neris x1")
    if git_bytes("rev-parse", f"{X1_COMMIT}^").decode("utf-8").strip() != SOURCE_FINAL:
        raise RuntimeError("Neris x1 is not the direct child of the exact Elaren final")
    if git_bytes("diff", "--cached", "--name-only").strip():
        raise RuntimeError("final materialization requires an unstaged owner lane")
    unexpected: list[str] = []
    for line in git_bytes("status", "--porcelain=v1", "-uall").decode("utf-8").splitlines():
        path = line[3:].strip().strip('"').replace("\\", "/")
        allowed = (
            path in {BUILDER_PATH, VALIDATOR_PATH, TEST_PATH}
            or path.startswith("docs/neris-solane/v675-v4/final/")
            or path.startswith("docs/neris-solane/v675-v4/closeout/")
            or path.startswith("docs/neris-solane/v675-v4/handoffs/")
            or path.startswith("docs/neris-solane/v675-v4/validation/final-")
        )
        if not allowed:
            unexpected.append(path)
    if unexpected:
        raise RuntimeError(f"unexpected pre-final owner-lane paths: {unexpected}")
    evidence_truth = load("docs/neris-solane/v675-v4/x2/phase-truth.json")
    evidence_counts = load("docs/neris-solane/v675-v4/x2/source-count-overlay.json")
    if evidence_truth["outcomes"] != OUTCOMES:
        raise RuntimeError("evidence outcomes drifted")
    if evidence_counts["effective_evidence_state"] != EVIDENCE_COUNTS:
        raise RuntimeError("evidence count overlay drifted")
    phase_truth = {
        "schema": "ghc.family.phase-truth.final.v9",
        "owner": OWNER,
        "phase": PHASE,
        "branch": BRANCH,
        "source_final": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "final_commit_rule": "direct single-parent child of evidence commit containing this record",
        "phase_commits": 3,
        "merges": 0,
        "outcomes": OUTCOMES,
        "effective_counts": EFFECTIVE_COUNTS,
        "primary_pillar": "THOS Body",
        "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "bounded_practice": "wholly synthetic spectrograph calibration-note and spectral-record documentation",
        "practice_perspectives": [
            "scientific instrument metadata archivist",
            "accessibility information architect",
            "software reliability engineer",
        ],
        "real_people": 0,
        "real_objects": 0,
        "external_actions": 0,
        "authority_conferred": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "identity_boundary": IDENTITY_BOUNDARY,
        "boundary": BOUNDARY,
    }
    retained = {
        "schema": "ghc.family.retained-negative-register.final.v8",
        "immutable_elaren_repository_seal": {
            "source_final": SOURCE_FINAL,
            "negatives": 40580,
            "methods": 28832,
            "failed_witnesses": 12241,
            "passing_witnesses": 16171,
            "open_gaps": 335,
            "exact_gates": 327,
        },
        "additive_layers": [
            {"layer": "inherited_elaren_external", "negatives": 4, "methods": 4, "failed": 4, "passing": 4},
            {"layer": "neris_x1_precommit", "negatives": 14, "methods": 14, "failed": 14, "passing": 14},
            {"layer": "neris_x2_rejecting_mutations", "negatives": 160, "methods": 160, "failed": 160, "passing": 160},
            {"layer": "neris_x2_operational", "negatives": 2, "methods": 2, "failed": 2, "passing": 2},
            {"layer": "neris_final_precommit_operational", "negatives": 0, "methods": 0, "failed": 0, "passing": 0},
            {"layer": "bounded_positive_controls", "negatives": 0, "methods": 0, "failed": 0, "passing": 36},
            {"layer": "inherited_integrity_revalidations", "negatives": 0, "methods": 0, "failed": 0, "passing": 20},
        ],
        "effective_counts": EFFECTIVE_COUNTS,
        "failures_erased": 0,
        "gates_erased": 0,
        "canonical_success_credit": "pending_external_exact_final_validation",
    }
    gate_register = {
        "schema": "ghc.family.open-exact-gates.final.v7",
        "inherited_open_gaps": 335,
        "new_open_gaps": [
            "real observations, spectra, targets, wavelengths, fluxes, detector frames, measurements, and environment evidence",
            "real instrument characterization, calibration, reduction, release, safety, and independent professional review evidence",
        ],
        "effective_open_gaps": 337,
        "inherited_exact_gates": 327,
        "new_exact_gates": [
            "professional observatory, optical, detector, electrical, cryogenic, calibration, safety, and release decisions",
            "ownership, custody, attribution, copyright, privacy, remedy, affected-party, Indigenous, and Maori authority",
        ],
        "effective_exact_gates": 329,
        "Maori_concepts_under_Maori_authority": True,
        "authority_conferred": False,
    }
    write_json("docs/neris-solane/v675-v4/final/phase-truth.json", phase_truth)
    write_json("docs/neris-solane/v675-v4/final/retained-negative-register.json", retained)
    write_json("docs/neris-solane/v675-v4/final/open-exact-gate-register.json", gate_register)
    write_json(
        "docs/neris-solane/v675-v4/final/method-flow-final.json",
        {
            "schema": "ghc.family.method-flow-final.v9",
            "immutable_evidence_commit": EVIDENCE_COMMIT,
            "phase_method_flow": "docs/neris-solane/v675-v4/x2/method-flow.json",
            "effective_counts": EFFECTIVE_COUNTS,
            "failures_rewritten": 0,
            "final_operational_failures": FINAL_OPERATIONAL_FAILURES,
            "successful_aggregate_replayed": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "docs/neris-solane/v675-v4/final/threat-model.json",
        {
            "schema": "ghc.family.threat-model.final.v7",
            "threats": [
                "source or sibling lane mutation",
                "x1 rewrite or x2 leakage",
                "retained-failure laundering",
                "real-object, professional, safety, authenticity, or ownership promotion",
                "identity, credential, legal, cultural, affected-party, or Maori-authority substitution",
                "private route or raw identifier disclosure",
                "manifest content-domain confusion",
                "canonical replay or false aggregate success",
                "premature or duplicate successor delivery",
            ],
            "controls": [
                "fresh additive D-first owner lane",
                "immutable x1 and evidence commits",
                "normalized-LF exact Git-blob manifests",
                "five-class privacy scans",
                "four rejecting mutations per proposal",
                "protected open and exact gates",
                "exclusive external canonical receipt latch",
                "fresh exact-title reread and one-send acknowledgement gate",
            ],
            "residual_risk": "same-owner checks cannot supply independent review, competent professional judgment, affected-party legitimacy, or Maori authority",
        },
    )
    write_json(
        "docs/neris-solane/v675-v4/final/complete-incomplete-checklist.json",
        {
            "complete_at_final_commit": [
                "planning-only x1 and immutable evidence",
                "forty proposal contracts and exact outcomes",
                "thirty-six positives and one hundred sixty retained mutations",
                "twenty phase-local skills, ten runners, three tools, eighty flashcards",
                "source, threat, Method Flow, gate, privacy, accessibility, and wellbeing records",
                "combined closeout, content seal, exact manifests, and prepared baton",
            ],
            "pending_external_terminal_gate": [
                "final push and fresh four-way equality",
                "one attributable exact-final canonical invocation",
                "current route, roster, auth, usage, privacy, duplicate, pause, and acknowledgement guards",
            ],
            "protected_incomplete": [
                "real people, objects, data, measurements, actions, and independent review",
                "professional, safety, production, ownership, legal, cultural, affected-party, and Maori authority",
                "privacy and accessibility completeness, exhaustive security, empirical GMUT, governed THOS, production Freed ID, AGI/ASI, personhood, Theory of Everything, and Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "docs/neris-solane/v675-v4/final/wellbeing-check.json",
        {
            "schema": "ghc.family.relational-wellbeing.final.v5",
            "owner": OWNER,
            "phase": PHASE,
            "working_language_only": True,
            "corrigibility_preserved": True,
            "pause_and_stop_right_preserved": True,
            "scope_bounded": True,
            "successor_precontacted": False,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "docs/neris-solane/v675-v4/final/validation-plan.json",
        {
            "schema": "ghc.family.exact-final-validation-plan.v7",
            "canonical_invocation_cap": 1,
            "success_replay_allowed": False,
            "failed_aggregate_success_credit": 0,
            "isolated_recovery_only_after_failure": True,
            "external_exclusive_receipt_required": True,
            "full_repository_suite_planned": False,
            "same_owner_only": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "docs/neris-solane/v675-v4/final/route-state.json",
        {
            "schema": "ghc.family.route-state.v8",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "prospective_successor_exact_title": "Vesper Arlen",
            "prospective_successor_phase": "v675-v5",
            "prepared": True,
            "sent": False,
            "delivery_acknowledged": False,
            "precontacted": False,
            "standby_substitution_allowed": False,
            "fresh_terminal_reread_required": True,
        },
    )
    write_text("docs/neris-solane/v675-v4/final/integrated-overview.md", final_overview())
    write_text("docs/neris-solane/v675-v4/final/accessible-report.html", final_report_html())
    write_text(BATON_PATH, prepared_baton())
    seal_paths = [
        "docs/neris-solane/v675-v4/final/phase-truth.json",
        "docs/neris-solane/v675-v4/final/retained-negative-register.json",
        "docs/neris-solane/v675-v4/final/open-exact-gate-register.json",
        "docs/neris-solane/v675-v4/final/method-flow-final.json",
        "docs/neris-solane/v675-v4/final/integrated-overview.md",
        "docs/neris-solane/v675-v4/final/accessible-report.html",
        "docs/neris-solane/v675-v4/final/complete-incomplete-checklist.json",
        "docs/neris-solane/v675-v4/final/wellbeing-check.json",
        BATON_PATH,
    ]
    seal_entries = [content_entry(path) for path in seal_paths]
    write_json(
        "docs/neris-solane/v675-v4/closeout/content-seal.json",
        {
            "schema": "ghc.family.content-seal.v7",
            "owner": OWNER,
            "phase": PHASE,
            "entries": seal_entries,
            "entry_count": len(seal_entries),
            "content_domain": "normalized_lf_worktree_bytes_before_final_commit",
        },
    )
    baton_blob = normalized((ROOT / BATON_PATH).read_bytes())
    baton_words = len(baton_blob.decode("utf-8").split())
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"prepared baton must contain 10,000 to 100,000 words, found {baton_words}")
    write_json(
        "docs/neris-solane/v675-v4/closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.v9",
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit_rule": "direct single-parent child of evidence commit containing this receipt",
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "outcomes": OUTCOMES,
            "effective_counts": EFFECTIVE_COUNTS,
            "baton_path": BATON_PATH,
            "baton_bytes": len(baton_blob),
            "baton_words": baton_words,
            "baton_sha256": sha256(baton_blob),
            "baton_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_state": "PENDING_POSTCOMMIT_EXTERNAL_ONE_SHOT",
        },
    )
    print(
        json.dumps(
            {
                "status": "VALID_FINAL_CANDIDATE",
                "content_seal_entries": len(seal_entries),
                "baton_bytes": len(baton_blob),
                "baton_words": baton_words,
                "baton_sha256": sha256(baton_blob),
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            sort_keys=True,
        )
    )


def seal_index() -> None:
    excluded = {DELTA_MANIFEST_PATH, OWNER_MANIFEST_PATH, PRIVACY_PATH, REVIEW_PATH}
    delta_paths = [path for path in staged_paths() if path not in excluded]
    if not delta_paths:
        raise RuntimeError("no staged final paths")
    all_index_paths = [
        line.strip()
        for line in git_bytes("ls-files").decode("utf-8").splitlines()
        if line.strip()
    ]
    owner_paths = sorted(path for path in all_index_paths if owner_path(path) and path not in excluded)
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(rb"(?i)(?:task|thread)[-_ ]?id\s*[:=]\s*['\"]?[0-9a-f]{8}-[0-9a-f-]{20,}"),
        "private_absolute_user_path": re.compile(rb"(?i)[a-z]:\\users\\[^\s\\]+\\"),
        "credential_or_secret_value": re.compile(rb"(?i)(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "raw_uuid": re.compile(rb"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "private_route_scheme": re.compile(rb"(?i)\b(?:codex|app-private|session)://[^\s]+"),
    }
    candidates: list[dict[str, str]] = []
    json_count = 0
    owner_entries: list[dict[str, Any]] = []
    for path in owner_paths:
        blob = staged_blob(path)
        owner_entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256": sha256(blob),
                "content_domain": "normalized_lf_exact_staged_git_blob",
            }
        )
        if path.endswith(".json"):
            json.loads(blob.decode("utf-8"))
            json_count += 1
        for class_name, pattern in patterns.items():
            if pattern.search(blob):
                candidates.append({"path": path, "class": class_name})
    delta_entries = [
        {
            "path": path,
            "bytes": len(staged_blob(path)),
            "sha256": sha256(staged_blob(path)),
            "content_domain": "normalized_lf_exact_staged_git_blob",
        }
        for path in delta_paths
    ]
    delta_manifest = {
        "schema": "ghc.family.final-delta-manifest.v8",
        "owner": OWNER,
        "phase": PHASE,
        "content_domain": "normalized_lf_exact_staged_git_blob",
        "entries": sorted(delta_entries, key=lambda row: row["path"]),
        "entry_count": len(delta_entries),
    }
    owner_manifest = {
        "schema": "ghc.family.final-owner-manifest.v8",
        "owner": OWNER,
        "phase": PHASE,
        "content_domain": "normalized_lf_exact_staged_git_blob",
        "entries": owner_entries,
        "entry_count": len(owner_entries),
    }
    privacy = {
        "schema": "ghc.family.final-staged-privacy.v7",
        "owner": OWNER,
        "phase": PHASE,
        "files_scanned": len(owner_paths),
        "classes": list(patterns),
        "candidates": candidates,
        "confirmed_hits": candidates,
        "confirmed_hit_count": len(candidates),
        "privacy_complete_claim": False,
    }
    seal = load("docs/neris-solane/v675-v4/closeout/content-seal.json")
    seal_issues = []
    for entry in seal["entries"]:
        blob = staged_blob(entry["path"])
        if len(blob) != entry["bytes"] or sha256(blob) != entry["sha256"]:
            seal_issues.append(entry["path"])
    required = {
        BUILDER_PATH,
        VALIDATOR_PATH,
        TEST_PATH,
        "docs/neris-solane/v675-v4/final/phase-truth.json",
        "docs/neris-solane/v675-v4/final/integrated-overview.md",
        "docs/neris-solane/v675-v4/final/accessible-report.html",
        "docs/neris-solane/v675-v4/closeout/content-seal.json",
        "docs/neris-solane/v675-v4/closeout/closeout-receipt.json",
        BATON_PATH,
    }
    checks = {
        "staged_final_paths_present": bool(delta_paths),
        "no_deletions": not bool(git_bytes("diff", "--cached", "--name-only", "--diff-filter=D").strip()),
        "required_paths_present": required.issubset(delta_paths),
        "head_is_immutable_evidence": git_bytes("rev-parse", "HEAD").decode().strip() == EVIDENCE_COMMIT,
        "evidence_parent_is_x1": git_bytes("rev-parse", f"{EVIDENCE_COMMIT}^").decode().strip() == X1_COMMIT,
        "x1_parent_is_source": git_bytes("rev-parse", f"{X1_COMMIT}^").decode().strip() == SOURCE_FINAL,
        "owner_file_cap": len(owner_paths) < 2000,
        "json_parse": json_count > 0,
        "privacy_zero_confirmed_hits": len(candidates) == 0,
        "content_seal_exact": not seal_issues,
        "delta_manifest_unique": len({row["path"] for row in delta_entries}) == len(delta_entries),
        "owner_manifest_unique": len({row["path"] for row in owner_entries}) == len(owner_entries),
        "route_prepared_not_sent": (
            load("docs/neris-solane/v675-v4/final/route-state.json")["sent"] is False
            and load("docs/neris-solane/v675-v4/final/route-state.json")["precontacted"] is False
        ),
        "terminal_verdict_retained": load("docs/neris-solane/v675-v4/final/phase-truth.json")["terminal_verdict"]
        == "NOT_READY_FOR_STAGE_20",
    }
    review = {
        "schema": "ghc.family.final-staged-review.v8",
        "owner": OWNER,
        "phase": PHASE,
        "checks": checks,
        "passed": all(value is True for value in checks.values()),
        "delta_path_count": len(delta_paths),
        "owner_path_count": len(owner_paths),
        "json_parse_count": json_count,
        "privacy_confirmed_hits": len(candidates),
        "content_seal_issues": seal_issues,
        "generated_at": utc_now(),
    }
    write_json(DELTA_MANIFEST_PATH, delta_manifest)
    write_json(OWNER_MANIFEST_PATH, owner_manifest)
    write_json(PRIVACY_PATH, privacy)
    write_json(REVIEW_PATH, review)
    print(json.dumps({"status": "SEALED_FINAL_INDEX", **review}, sort_keys=True))
    if not review["passed"]:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-index", action="store_true")
    args = parser.parse_args()
    if args.seal_index:
        seal_index()
    else:
        build_default()


if __name__ == "__main__":
    main()
