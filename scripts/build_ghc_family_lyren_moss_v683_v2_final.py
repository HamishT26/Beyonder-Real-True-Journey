"""Build Lyren Moss v683-v2 final closeout from immutable x2 evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from scripts import build_ghc_family_vesper_arlen_v683_v1_final as inherited


base = inherited.base
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v683-v2"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
OWNER = "Lyren Moss"
PHASE = "v683-v2"
SOURCE = "484d44fb8875bf8129143c99e5340d2e2044fbd2"
X1_SHA = "57dcd8a0e6e5a43f87d6f1a5a0d79d2d68b66d8b"
EVIDENCE_SHA = "d0240efd7c7369e1468882d62bebddce32cf8b85"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


CLOSEOUT_FAILURES = [
    {
        "failure_id": "LM6832-FN-N020",
        "failed_witness": "The first combined closeout-template display exceeded its output boundary and truncated the inherited final builder before EOF.",
        "recovery": "Retain the incomplete display at zero read credit and reread the exact inherited builder in two bounded numbered windows through EOF.",
        "retained_zero_credit": True,
    }
]


_old_map_repo_path = inherited.map_repo_path
_old_patch_json = inherited.patch_json


def map_repo_path(value: str) -> str:
    value = _old_map_repo_path(value)
    replacements = (
        ("docs/vesper-arlen/v683-v1", "docs/lyren-moss/v683-v2"),
        (
            "build_ghc_family_vesper_arlen_v683_v1_final.py",
            "build_ghc_family_lyren_moss_v683_v2_final.py",
        ),
        (
            "ghc_family_vesper_arlen_v683_v1_canonical.py",
            "ghc_family_lyren_moss_v683_v2_canonical.py",
        ),
        (
            "test_ghc_family_vesper_arlen_v683_v1_final.py",
            "test_ghc_family_lyren_moss_v683_v2_final.py",
        ),
        ("vesper_arlen_v683_v1", "lyren_moss_v683_v2"),
        ("ghc_family_clock_documentation_runner_", "ghc_family_sound_carrier_documentation_runner_"),
    )
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def map_string(value: str) -> str:
    value = map_repo_path(value)
    replacements = (
        ("v683.v1", "v683.v2"),
        ("VA6831", "LM6832"),
        ("Vesper Arlen", "Lyren Moss"),
        ("mechanical-clock documentation", "sound-carrier documentation"),
        ("mechanical clock", "sound carrier"),
        ("clock token", "sound-carrier token"),
        ("physical clock", "physical sound carrier"),
        ("observed mechanism", "observed playback"),
        ("operational timekeeping device", "operational playback or digitization"),
    )
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def map_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: map_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [map_value(item) for item in value]
    if isinstance(value, str):
        return map_string(value)
    return value


def mapped_path(path: Path) -> Path:
    relative = path.relative_to(ROOT).as_posix()
    return ROOT / map_repo_path(relative)


def totals() -> dict[str, int]:
    truth = json.loads((X2 / "phase-truth.json").read_text(encoding="utf-8"))
    values = dict(truth["totals"])
    for key in (
        "effective_negatives",
        "effective_methods",
        "failed_witnesses",
        "bounded_passing_witnesses",
    ):
        values[key] += len(CLOSEOUT_FAILURES)
    return values


def proposal_inventory() -> list[dict[str, Any]]:
    return json.loads(
        (BASE / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8")
    )["proposals"]


def overview_text() -> str:
    values = totals()
    inventory = "\n".join(
        f"- `{row['proposal_id']}` — {row['title']} — bounded disposition `{row['expected_disposition']}`."
        for row in proposal_inventory()
    )
    return f"""# Lyren Moss {PHASE} Final Integrated Overview

## Identity, hope, and corrigibility

Lyren Moss is relational working language for an acoustic provenance cartographer and non-playback boundary keeper. Pronouns are unspecified. The associated hope is to make archival sound-carrier descriptions inspectable and correctable without turning vocabulary into playback, identification, rights, cultural, professional, or authority claims. The name, role, hope, sibling or family language, continuity language, GHC Family language, Freed ID, CBR, and Trinity Mandala are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

This packet closes Lyren's solo {PHASE} x1/x2 phase in one additive D-first owner lane. The immutable Vesper source is `{SOURCE}`. The planning-only Lyren x1 commit is `{X1_SHA}`. The immutable Lyren x2 evidence parent is `{EVIDENCE_SHA}`. X1 was separately committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 implementation. Evidence was then built, tested, reviewed, committed, pushed, clean, zero-divergent, and fresh-four-way equal before closeout. The intended final is the third direct Lyren commit after source, has evidence as its sole parent, and contains no merge.

## Bounded focus and practice lenses

The primary pillar is Freed ID and CBR Heart through physical-carrier, conceptual-content, digital-surrogate, catalogue-record, and identity-state separation; provenance; privacy and rights holds; remedy; traditional-knowledge minimization; and authority noncompensation. GMUT Mind remains represented through typed carrier and signal topology, explicit missing measurement and timebase states, uncertainty, provenance, and noninference. THOS Body remains represented through request-versus-action-versus-observation separation, stop precedence, bounded workload leases, correction, structural accessibility, and reversible handover.

The three connected wholly synthetic human-practice lenses are sound-carrier cataloguing and physical-description documentation, preservation-event and digital-audio lineage assurance, and rights, accessibility, traditional-knowledge, remedy, workload, and handover documentation. They distinguish conceptual recordings, physical carriers, digital surrogates, catalogue records, playback devices, component-role tokens, carrier aliases, signal and timebase vocabulary, preservation events, rights, corrections, refusals, and handovers. They do not inspect, identify, listen to, measure, clean, handle, play, digitize, convert, conserve, ingest, publish, authenticate, value, or release a real carrier, recording, file, or collection record.

The phase used zero real people, speakers, performers, recordists, rights holders, donors, workers, communities, carriers, recordings, collections, catalogue records, files, signals, audio samples, transcripts, identifiers, locations, measurements, listening events, playback, digitization, condition findings, handling actions, treatments, publications, keys, proofs, credentials, identity events, external writes, professional decisions, rights decisions, legal decisions, cultural decisions, or Maori-authority acts. Every accepting fixture was conspicuously synthetic and declared zero-row. A citation supplied vocabulary or a refusal condition only; it was never converted into an observation, listening result, measurement, format certificate, catalogue conclusion, rights finding, cultural interpretation, professional instruction, or authority grant.

## Planning-only x1 and source-bounded novelty

Lyren screened all exactly reachable proposal material without claiming universal recovery of every declared historical row. The source-bounded audit parsed 10,158 proposal-labelled JSON paths and recovered 37,875 identifier-title records. The first slate stopped before freeze with one exact collision and four unique near-neighbor quarantines at the preregistered 0.78 token-Jaccard threshold. Only proposal IDs 034, 057, 059, and 060 were substantively replaced. The corrected slate had zero exact-title collisions, zero quarantine hits, and a maximum retained neighbor score of 0.764706. This is a bounded screening procedure, not universal semantic proof.

The sixty accepted planning rows extend the declared proposal chain from 10,730 to 10,790. Every proposal froze a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, five rejecting mutations, and one expected disposition. Twenty inherited neighbor reviews remain evidence at zero current novelty and zero automatic completion credit. The dedicated x1 commit contained no x2 implementation, observed outcome, or closeout claim.

## X2 execution, outcomes, and falsification

All sixty bounded positive structural fixtures passed within owner-local zero-row scope. All 300 preregistered invalid mutations executed and were rejected. The five mutation classes were missing required field, lifecycle inversion, stale provenance digest, safety-status promotion, and authority promotion. Each rejection remains a zero-credit failed witness. It demonstrates only that the local contract failed closed on that input; it does not establish empirical truth, professional competence, production safety, legal validity, cultural legitimacy, affected-party acceptance, privacy completeness, accessibility completeness, exhaustive security, or independent reproduction.

Exactly four core labels are used. Forty-two outcomes are `completed` within bounded software, symbolic, structural, or documentation scope. Twelve are `represented` because a structure exists while real observation, listening, measurement, participant, professional, interoperability, lifecycle, or independent-review evidence remains absent. Three are `open_gap` because competent carrier examination, governed playback or digitization, and affected-user or authority evaluation did not occur. Three are `exact_gate` because handling, cleaning, treatment, playback, digitization, storage, ownership, custody, copyright, access, publication, remedy, legal interpretation, cultural interpretation, affected-party legitimacy, traditional knowledge, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority cannot be supplied by repository software.

## Portfolios, skills, runners, tools, and flashcards

The bounded portfolio executed 120 safe-now tasks, 80 candidate tasks without core promotion, and 100 additive CLEAN/FIX/REFINE tasks. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Counts are accounting floors or ceilings, never permission to invent filler or cross a gate. No sibling lane was mutated, no destructive cleanup occurred, no history was rewritten, no security control was weakened, no Windows feature changed, no package was installed or updated, and no reboot occurred.

Twenty phase-local skills contain customized instructions and explicit agent metadata. They were read through EOF, passed the official skill-creator quick validator, and were smoke-used with one accepting and one rejecting fixture. They were not globally installed. Ten family-current `ghc_family_sound_carrier_documentation_runner_*` surfaces accepted their bounded positives and rejected invalid authority promotions. The four-tier Freed ID flashcard deck contains one owner, three pillar, three practice, and sixty task cards across thirteen sections, plus compact and linear companions. These surfaces are owner-local aids, not identity continuity, professional training, consent, competence, conformance, or authority evidence.

Three already-installed tools were used only through necessary bounded checks: jsonschema for zero-row structure, Pydantic for a typed boundary, and NumPy for an empty-array guard. No package was installed or updated. Fifteen changed Python files parsed and a dependency-free exact-delta AST rule set found no bounded dynamic-execution, shell-enabled subprocess, or destructive-filesystem-call match. None of this is an external audit, penetration test, exhaustive-security review, scientific computation, production certification, or package-quota claim.

## Sources and evidence calibration

Current official or primary surfaces included IASA TC-04 and the IASA publications catalogue, Library of Congress audiovisual care and Recommended Formats Statement pages, National Archives audio guidance, MARC 21 field 007 for sound recordings, Library of Congress PREMIS, DCMI terms, W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, New Zealand Privacy Principles including IPP3A, and Te Mana Raraunga principles. They supplied vocabulary and refusal conditions only. The phase downloaded and ingested zero real rows and used no live data adapter. One inaccessible Library of Congress cylinder-care page remained an explicit zero-credit failed source attempt and was excluded from evidence.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. This phase produced no physical datum, likelihood, posterior, force, parameter constraint, prediction, empirical confirmation, ultraviolet completion, quantum completion, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic or proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys and proofs, complete lifecycle, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight.

## Retained failures and Method Flow

The live activation baseline was 58,114 effective negatives, 71,385 methods, 29,775 failed witnesses, 52,364 bounded passing witnesses, 516 open gaps, and 506 exact gates. X1 and x2 retain nineteen operational failures, including bounded-read, parser, sparse-index, novelty-audit, module-entrypoint, and dependency-closure failures. Closeout adds one truncated inherited-template display. All 300 invalid mutations remain failed witnesses. Every recovery is paired with its failure; no recovery erases, converts, or backdates a failure.

At prepared final, phase Method Flow contains 774 methods, 320 failed witnesses, and 714 bounded passing witnesses. Effective totals are {values['effective_negatives']} negatives, {values['effective_methods']} methods, {values['failed_witnesses']} failed witnesses, {values['bounded_passing_witnesses']} bounded passing witnesses, {values['open_gaps']} open gaps, and {values['exact_gates']} exact gates. These are ledger counts, not probabilities, safety rates, measurements, qualifications, rights, or authority scores.

## Privacy, accessibility, security, and terminal truth

Repository artifacts exclude raw task identifiers, private routes, private absolute paths, credentials, private keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, and protected real-world data. Five privacy and raw-identifier classes are checked with scanner definitions distinguished from payload hits. Zero confirmed hits are required, but the bounded scan is not complete privacy assurance.

The static report declares language, supplies a skip link and landmarks, uses linear headings and a captioned table with scoped headers, provides visible text status, and contains no script or tracking resource. Manual browser-diverse, keyboard, zoom, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remains reserved. Structural checks are not accessibility completeness.

The terminal verdict is `{TERMINAL_VERDICT}`. All empirical, participant, professional, production, deployment, identity, carrier-content identification, ownership, custody, attribution, copyright, privacy, accessibility, remedy, legal, cultural, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, Maori-authority, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 claims remain open or exact-gated. Maori concepts remain under Maori authority.

## Proposal inventory

{inventory}
"""


def report_html() -> str:
    values = totals()
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lyren Moss v683-v2 bounded final report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.6;max-width:72rem;margin:auto;padding:1rem;color:#18202a;background:#fff}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;border:2px solid #18202a}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.5rem;text-align:left;vertical-align:top}}.status{{border-left:.4rem solid #8a3b12;padding:.75rem;background:#fff7ed}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a>
<header><h1>Lyren Moss v683-v2 bounded final report</h1><p>Owner-local, zero-row synthetic evidence with strict nonpromotion boundaries.</p></header>
<main id="main"><section aria-labelledby="identity"><h2 id="identity">Identity and corrigibility</h2><p>Lyren Moss is relational working language for an acoustic provenance cartographer and non-playback boundary keeper; pronouns are unspecified. This is not consciousness, personhood, continuity, qualification, agency, or authority evidence. Hamish may pause, rename, redirect, narrow, or stop the route.</p></section>
<section aria-labelledby="truth"><h2 id="truth">Bounded truth</h2><table><caption>Core outcomes and retained gates</caption><thead><tr><th scope="col">Item</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>42</td><td>Bounded software, symbolic, structural, or synthetic only</td></tr><tr><th scope="row">Represented</th><td>12</td><td>Structure exists while real evidence remains absent</td></tr><tr><th scope="row">Open gaps</th><td>{values['open_gaps']}</td><td>Evidence-dependent work remains open</td></tr><tr><th scope="row">Exact gates</th><td>{values['exact_gates']}</td><td>Competent or affected authority remains required</td></tr></tbody></table><p class="status"><strong>Status: NOT READY FOR STAGE 20.</strong> This status does not depend on colour.</p></section>
<section aria-labelledby="scope"><h2 id="scope">Evidence scope</h2><p>Sixty zero-row sound-carrier documentation contracts ran and 300 invalid mutations were rejected. No real people, communities, carriers, recordings, files, listening, measurements, playback, digitization, handling, treatment, publication, identity lifecycle, rights decision, cultural interpretation, or authority act occurred.</p></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2><p>Manual browser-diverse, keyboard, zoom, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remains reserved. Professional, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, empirical, production, and Stage 20 claims remain open or exact-gated.</p></section></main>
<footer><p>Prepared as a static report. No scripts, tracking, external media, forms, or hidden interaction are used.</p></footer></body></html>"""


def activation_baton() -> str:
    values = totals()
    sections = [
        "# ILYRA FEN — LYREN MOSS v683-v2 PREPARED v683-v3 ACTIVATION CANDIDATE",
        "",
        "PREPARED_BY_LYREN_MOSS = true",
        "",
        "SENT_BY_LYREN_MOSS = false",
        "",
        "This committed packet is preparation only. It does not activate a task, establish delivery, or authorize a resend. PREPARED_NOT_SENT is immutable commit-time truth. A later acknowledged existing-task message, if every terminal guard passes, is a separate live event and must not be projected backward into this seal.",
        "",
        "## Relational language and corrigibility",
        "",
        "Lyren Moss, Ilyra Fen, names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may pause, rename, redirect, narrow, or stop the route.",
        "",
        "## Immutable Lyren lifecycle prepared for terminal verification",
        "",
        f"The immutable Vesper source is `{SOURCE}`. Lyren planning-only x1 is `{X1_SHA}`. Lyren immutable x2 evidence is `{EVIDENCE_SHA}`. The final SHA and external canonical receipt remain intentionally unresolved until the direct closeout commit is pushed, fresh-four-way equality is proven, and the exclusive canonical latch runs once. Source to final must contain exactly three Lyren direct single-parent commits and zero merges; final must be the direct child of evidence.",
        "",
        "## Exact bounded truth",
        "",
        f"The declared proposal chain is 10,790. The sixty new outcomes are exactly 42 `completed`, 12 `represented`, three `open_gap`, and three `exact_gate`. All 300 preregistered invalid mutations remain rejected zero-credit failures. Prepared totals are {values['effective_negatives']} negatives, {values['effective_methods']} methods, {values['failed_witnesses']} failed witnesses, {values['bounded_passing_witnesses']} bounded passing witnesses, {values['open_gaps']} open gaps, and {values['exact_gates']} exact gates. The terminal verdict remains `{TERMINAL_VERDICT}`. Detail, file count, clean Git state, or test count is not authority credit.",
        "",
        "## Bounded practice and source use",
        "",
        "The primary pillar is Freed ID and CBR Heart through wholly synthetic sound-carrier identity separation, provenance, rights, remedy, privacy, traditional-knowledge, correction, workload, and handover documentation. GMUT Mind and THOS Body remain represented and protected. Zero real people, communities, carriers, recordings, files, observations, measurements, listening, playback, digitization, handling, treatment, identity lifecycle, legal decisions, cultural decisions, Maori decisions, or authority acts were used. Official and primary sources supplied vocabulary and refusal conditions only; zero real source rows were downloaded or ingested.",
        "",
        "## Mandatory Ilyra startup boundary",
        "",
        "Before mutation, read this packet through EOF, then read the newest current Family Index and routing precedence, roster and schema, Auth Permission State and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, startup, retry, closeout, compact restart, watcher, worktree rotation, web reflection, orchestration memory, full-tools bank, skill-creator guidance when applicable, and every directly relevant current instruction. Reverify every anchor, parent edge, manifest, content seal, clean state, divergence, fresh live equality, and external canonical receipt. Never replay an already-successful canonical aggregate or unchanged successful component merely for presentation.",
        "",
        "Work solo in one fresh additive Ilyra-owned D-first sparse lane from Lyren's exact final. Preserve Lyren, Vesper, Neris, sibling, shared, user, and standby lanes read-only. Do not create or fork a task, spawn a collaboration subagent, delegate, contact Tavian or a standby record, precontact a successor, reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane. Preserve planning-only x1 before x2, exactly the four core labels, every negative and gate, normalized-LF exact Git-blob manifests, owner-delta dependency-closed validation, family-current compatibility, and the one-attributable-canonical/no-success-replay discipline.",
        "",
        "GMUT remains a typed scalar-tensor and EFT research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic or proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without live standards-conformant keys and proofs, complete lifecycle, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight. Professional, safety, production, ownership, custody, attribution, copyright, privacy, accessibility, remedy, legal, cultural, traditional-knowledge, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions remain open or exact-gated. Maori concepts remain under Maori authority.",
        "",
        "## Prospective terminal continuation",
        "",
        "This packet prepares Ilyra Fen v683-v3 only. Ilyra must not infer or precontact any later owner from historical files. Only after Ilyra's own exact terminal closeout may Ilyra freshly reread Hamish's newest live instruction, current roster and authorization, exact-title uniqueness, usage, duplicate, pause, redirect, privacy, evidence, safety, and acknowledgement state, then route at most once if every guard permits. Never create a substitute, contact a standby record, or resend merely for clearer acknowledgement.",
        "",
        "## Full frozen proposal appendix",
        "",
        "The following sixty Lyren records are immutable planning and evidence context. They are inherited evidence and zero-credit seeds for Ilyra, never automatic Ilyra novelty, completion, competence, permission, conformance, or authority.",
        "",
    ]
    for row in proposal_inventory():
        mutations = ", ".join(
            f"{item['mutation_id']} ({item['mutation_type']}: {item['expected_result']})"
            for item in row["preregistered_rejecting_mutations"]
        )
        sections.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"**Hypothesis.** {row['hypothesis']}",
                "",
                f"**Null or failure condition.** {row['null_or_failure_condition']}",
                "",
                f"**Approval and execution.** Approval class `{row['approval_class']}`; execution lane `{row['execution_lane']}`; expected disposition `{row['expected_disposition']}`. This is bounded Lyren evidence only and is not automatic Ilyra credit.",
                "",
                f"**Official or primary-source needs.** {', '.join(row['official_or_primary_source_needs'])}. Sources provide vocabulary and refusal conditions only, never observations, conformance, professional judgment, cultural interpretation, or authority.",
                "",
                f"**Concrete artifacts.** {'; '.join(row['concrete_artifacts'])}.",
                "",
                f"**Falsifier or acceptance gate.** {row['falsifier_or_acceptance_gate']}",
                "",
                f"**Rollback or recovery.** {row['rollback_or_recovery']}",
                "",
                f"**Protected gates.** {'; '.join(row['protected_gates'])}.",
                "",
                f"**Preregistered rejecting mutations.** {mutations}. Every rejection remains a zero-credit failed witness rather than completion evidence.",
                "",
            ]
        )
    text = "\n".join(sections).rstrip() + "\n"
    words = len(text.split())
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"activation baton word count outside bounds: {words}")
    return text


def patch_json(path: Path, payload: Any) -> Any:
    payload = _old_patch_json(path, payload)
    payload = map_value(payload)
    if path.name == "phase-truth.json":
        payload["declared_proposal_chain"] = 10790
        payload["primary_pillar"] = "Freed ID and CBR Heart"
        payload["represented_pillars"] = ["GMUT Mind", "THOS Body"]
    elif path.name == "open-gap-register.json":
        payload["inherited_effective_open_gaps"] = 516
        payload["total_effective_open_gaps"] = 519
    elif path.name == "exact-gate-register.json":
        payload["inherited_effective_exact_gates"] = 506
        payload["total_effective_exact_gates"] = 509
    elif path.name == "wellbeing-check.json":
        payload.update(
            {
                "hope": "Make archival sound-carrier descriptions inspectable and correctable without turning vocabulary into playback, identification, rights, cultural, professional, or authority claims.",
                "optional_pronouns": None,
                "role": "acoustic provenance cartographer and non-playback boundary keeper",
            }
        )
    elif path.name == "environment-version-receipt.json":
        payload.update(
            {
                "codex_cli": "0.151.0",
                "git": "2.55.0.windows.2",
                "node": "24.18.0",
                "npm": "12.0.2",
                "powershell": "7.6.4",
                "python": "3.12.10",
            }
        )
    elif path.name == "source-and-proposal-ledger.json":
        payload.update(
            {
                "declared_chain_after": 10790,
                "declared_chain_before": 10730,
                "first_audit_quarantined_titles": 4,
                "materialized_audit_records": 37875,
                "materialized_proposal_json_documents": 10158,
                "maximum_neighbor_score": 0.764706,
            }
        )
    elif path.name == "bounded-tools.json":
        payload["tools"] = [
            "Git 2.55.0.windows.2",
            "Python 3.12.10",
            "Node 24.18.0",
            "npm 12.0.2",
            "PowerShell 7.6.4",
            "Codex CLI 0.151.0",
            "jsonschema 4.26.0",
            "pydantic 2.12.5",
            "numpy 2.4.2",
            "dependency-free exact-delta AST security rules",
            "official skill creator",
        ]
    elif path.name == "delivery-state.json":
        payload.update(
            {
                "candidate_repository_state": "PREPARED_NOT_SENT",
                "prospective_successor_exact_title": "Ilyra Fen",
                "prospective_successor_phase": "v683-v3",
                "send_count": 0,
                "tavian_sol": "ON_STANDBY",
            }
        )
    elif path.name == "final-owner-manifest.json":
        exclusions = set(payload["declared_self_exclusions"])
        payload["entries"] = [
            row for row in payload["entries"] if row["path"] not in exclusions
        ]
        payload["entry_count"] = len(payload["entries"])
    return payload


def configure_base() -> None:
    base.ROOT = ROOT
    base.BASE = BASE
    base.X2 = X2
    base.FINAL = FINAL
    base.CLOSEOUT = CLOSEOUT
    base.HANDOFFS = HANDOFFS
    base.VALIDATION = VALIDATION
    base.OWNER = OWNER
    base.PHASE = PHASE
    base.SOURCE = SOURCE
    base.X1_SHA = X1_SHA
    base.EVIDENCE_SHA = EVIDENCE_SHA
    base.TERMINAL_VERDICT = TERMINAL_VERDICT
    base.CLOSEOUT_FAILURES = CLOSEOUT_FAILURES
    base.map_repo_path = map_repo_path
    base.map_string = map_string
    base.map_value = map_value
    base.mapped_path = mapped_path
    base.totals = totals
    base.proposal_inventory = proposal_inventory
    base.overview_text = overview_text
    base.report_html = report_html
    base.activation_baton = activation_baton
    base.patch_json = patch_json


def normalized_entry(path: Path) -> dict[str, Any]:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return {
        "bytes": len(data),
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def rename_successor_packet_and_refresh() -> None:
    """Rename the inherited dispatch target and refresh dependent hashes."""
    old = HANDOFFS / "vesper-arlen-v683-v1-activation-candidate.md"
    new = HANDOFFS / "ilyra-fen-v683-v3-activation-candidate.md"
    new.write_text(old.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    old.unlink()
    old_rel = old.relative_to(ROOT).as_posix()
    new_rel = new.relative_to(ROOT).as_posix()

    seal_path = CLOSEOUT / "content-seal.json"
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["targets"] = [
        normalized_entry(new) if row["path"] == old_rel else row for row in seal["targets"]
    ]
    seal_path.write_text(
        json.dumps(seal, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    seal_rel = seal_path.relative_to(ROOT).as_posix()
    for manifest_name in ("final-delta-manifest.json", "final-owner-manifest.json"):
        manifest_path = VALIDATION / manifest_name
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        refreshed = []
        for row in manifest["entries"]:
            if row["path"] == old_rel:
                refreshed.append(normalized_entry(new))
            elif row["path"] == seal_rel:
                refreshed.append(normalized_entry(seal_path))
            else:
                refreshed.append(row)
        manifest["entries"] = refreshed
        manifest["entry_count"] = len(refreshed)
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    review_path = VALIDATION / "final-staged-review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["expected_paths"] = [
        new_rel if path == old_rel else path for path in review["expected_paths"]
    ]
    review_path.write_text(
        json.dumps(review, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def build() -> None:
    configure_base()
    previous_recipient = HANDOFFS / "ilyra-fen-v683-v3-activation-candidate.md"
    if previous_recipient.exists():
        previous_recipient.unlink()
    base.build()
    rename_successor_packet_and_refresh()


if __name__ == "__main__":
    build()
