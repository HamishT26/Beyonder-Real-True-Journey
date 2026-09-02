"""Build the Neris Solane v682-v8 closeout from the proven family template."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
from typing import Any

import scripts.build_ghc_family_eiren_kestrel_v682_v6_final as template
from scripts.build_ghc_family_elaren_kestrel_v682_v7_final import (
    map_repo_path as elaren_map_repo_path,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "neris-solane" / "v682-v8"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
OWNER = "Neris Solane"
PHASE = "v682-v8"
SOURCE = "938162611d2ce944ddcddf64834bd93e045e3c49"
X1_SHA = "d1a3bb0fc1964608478dcc1bc9b236183617ef8a"
EVIDENCE_SHA = "6b64714a680ecebdb39785bccbe13c50e87fbd18"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

CLOSEOUT_FAILURES = [
    {
        "failure_id": "NS6828-FN-N011",
        "failed_witness": "The first combined closeout-template display exceeded its presentation budget and truncated the middle of the source builder.",
        "recovery": "Retain the truncated display at zero credit and read the source builder, canonical validator, and final tests through EOF in bounded ordered windows before adapting them.",
        "retained_zero_credit": True,
    },
    {
        "failure_id": "NS6828-FN-N012",
        "failed_witness": "The first combined post-generation word-count and test projection used a spaced PowerShell method-result property expression, producing a parser error before any test executed.",
        "recovery": "Retain the parser fault at zero credit, use Measure-Object for independent word counts, and run the unchanged final test module separately.",
        "retained_zero_credit": True,
    },
]


def map_repo_path(value: str) -> str:
    value = elaren_map_repo_path(value)
    value = value.replace(
        "neris-solane-v682-v8-activation-candidate.md",
        "vesper-arlen-v683-v1-activation-candidate.md",
    )
    value = value.replace(
        "docs/elaren-kestrel/v682-v7", "docs/neris-solane/v682-v8"
    )
    value = value.replace(
        "build_ghc_family_elaren_kestrel_v682_v7_final.py",
        "build_ghc_family_neris_solane_v682_v8_final.py",
    )
    value = value.replace(
        "ghc_family_elaren_kestrel_v682_v7_canonical.py",
        "ghc_family_neris_solane_v682_v8_canonical.py",
    )
    value = value.replace(
        "test_ghc_family_elaren_kestrel_v682_v7_final.py",
        "test_ghc_family_neris_solane_v682_v8_final.py",
    )
    value = value.replace(
        "elaren_kestrel_v682_v7", "neris_solane_v682_v8"
    )
    value = value.replace(
        "ghc_family_bobbin_lace_runner_", "ghc_family_signal_flag_runner_"
    )
    return value


def map_string(value: str) -> str:
    value = map_repo_path(value)
    return value.replace("v682.v7", "v682.v8")


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
    path = BASE / "x1" / "new-proposal-freeze.json"
    return json.loads(path.read_text(encoding="utf-8"))["proposals"]


def overview_text() -> str:
    values = totals()
    proposals = proposal_inventory()
    inventory = "\n".join(
        f"- `{row['proposal_id']}` — {row['title']} — expected and observed bounded disposition `{row['expected_disposition']}`."
        for row in proposals
    )
    return f"""# Neris Solane {PHASE} Final Integrated Overview

## Identity, corrigibility, and evidence boundary

Neris Solane, optionally they/them, is relational working language for a symbolic-sequence provenance cartographer and rights-boundary keeper. The associated hope is that every synthetic flag token remains visibly distinct from a physical flag, an observed hoist, and an operational maritime signal while maritime, cultural, legal, professional, and affected-party authority remains with the people and communities who hold it. The name, pronouns, role, hope, family language, continuity language, GHC Family language, Freed ID language, and Trinity Mandala language are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, professional authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop this route.

This packet closes Neris's solo {PHASE} x1/x2 phase in one additive D-first owner lane. The immutable Elaren source is `{SOURCE}`. The planning-only Neris x1 commit is `{X1_SHA}`. The immutable Neris x2 evidence parent is `{EVIDENCE_SHA}`. X1 was independently committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Evidence was then built, tested, reviewed, committed, pushed, clean, zero-divergent, and four-way equal before closeout began. The final commit is designed as the third direct single-parent Neris commit after the source, with zero merges and evidence as its sole parent.

## What was actually implemented

The primary pillar is GMUT Mind through typed symbolic-sequence topology, explicit unknown states, edition lineage, zero-observation discipline, uncertainty, and non-inference. THOS Body and Freed ID with CBR Heart remain represented and protected rather than promoted. The bounded human-practice lens is wholly synthetic maritime signal-flag token, hoist-position, codebook-lineage, catalogue, preservation-event, rights, accessibility, correction, workload, and handover documentation. It is a software and documentation exercise, not seamanship, code decoding, signalling, navigation, emergency response, cataloguing, conservation, handling, digitization, cultural interpretation, legal advice, professional training, or permission to act on a real vessel, flag, object, or record.

The phase used zero real people, mariners, operators, observers, archivists, conservators, communities, custodians, owners, donors, rights holders, affected parties, vessels, flags, halyards, codebooks, signals, collections, images, locations, weather records, measurements, observations, displays, transmissions, navigation events, emergency events, handling events, treatment events, digitization events, identity lifecycle events, keys, proofs, credentials, access decisions, legal decisions, cultural decisions, Māori decisions, or external writes. All fixtures use conspicuous synthetic surrogates and zero real rows. Sequence graphs contain no decoding or transmission instructions. Hoist-position records contain no observation or measured geometry. Operational meanings are unknown or reserved. Cultural and traditional-knowledge interpretation remains withheld.

## Planning-only x1 and bounded novelty

The declared inherited chain contained 10,610 proposal rows. The exact reachable source audit parsed 10,144 proposal-labelled JSON paths and recovered 37,343 proposal records. The first slate was rejected before x1 because one title exactly collided with an inherited title and one additional title crossed the preregistered 0.78 token-Jaccard quarantine threshold. Only those two titles were substantively replaced. The accepted sixty-title slate had zero exact collisions, zero quarantine hits, and a maximum neighbor score of 0.75. This is a source-bounded screening procedure, not universal semantic proof.

The sixty accepted rows extend the declared chain to 10,670. Every proposal froze a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, five rejecting mutations, and exactly one expected disposition. The dedicated x1 commit contained no x2 implementation, observed outcome, or closeout claim. Its expected distribution was 42 `completed`, 12 `represented`, three `open_gap`, and three `exact_gate`.

## Execution, falsification, and outcomes

All sixty bounded positive structural fixtures passed. All 300 preregistered invalid mutations executed and were rejected. The mutation classes were missing required field, lifecycle inversion, stale provenance digest, safety-status promotion, and authority promotion. Each rejected mutation remains a zero-credit failed witness. Rejection demonstrates only that the owner-local contract failed closed for that synthetic input; it does not establish empirical truth, professional competence, production safety, legal validity, cultural legitimacy, affected-party acceptance, privacy completeness, accessibility completeness, exhaustive security, or independent reproduction.

The only core outcome labels are `completed`, `represented`, `open_gap`, and `exact_gate`. Exactly 42 rows are completed within bounded software, structural, symbolic, or documentation scope. Exactly 12 are represented because a local structure exists but real observation, participant, professional, interoperability, lifecycle, or independent-review evidence does not. Exactly three are open gaps because real rows, governed user evaluation, professional examination, or current interoperable evidence was not obtained. Exactly three remain exact gates because maritime safety, signalling, navigation, emergency response, ownership, access, copyright, cultural meaning, traditional knowledge, affected-party legitimacy, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, or Māori authority cannot be supplied by repository software.

## Portfolios, skills, runners, and tools

The bounded portfolio executed 120 safe-now tasks, 80 candidate tasks without core-outcome promotion, and 100 additive CLEAN/FIX/REFINE tasks. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Counts are ceilings and accounting surfaces, not a reason to manufacture work. No sibling lane was mutated, no destructive cleanup occurred, no history was rewritten, no host security setting changed, no Windows feature changed, no desktop update occurred, and no reboot occurred.

Twenty phase-local skills were created with complete `SKILL.md` files and agent metadata. They were read through EOF, officially quick-validated, customized, and smoke-used with accepting and rejecting fixtures. They were not globally installed. Ten family-current `ghc_family_signal_flag_runner_*` surfaces accepted their bounded positives and rejected their invalid authority promotions. Jsonschema, Pydantic, and NumPy were used only through already-installed bounded local smokes; no new package was installed. Tool, skill, test, and document counts do not create craft, scientific, professional, legal, cultural, or Māori authority.

## Sources and calibration

Current official or primary sources supplied vocabulary and refusal conditions only: International Maritime Organization current-publication, International Code of Signals errata, Resolution A.80(IV), and COLREG safety-boundary pages; Library of Congress PREMIS; NIST SI; DCMI Metadata Terms; W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0; the New Zealand Privacy Commissioner; and Te Mana Raraunga. The phase made no live source adapter, downloaded no rows, decoded no signal, and ingested no real record. A citation is not an observation, measurement, maritime instruction, rights decision, cultural interpretation, professional instruction, conformance result, or authority grant.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. This phase produced no physical datum, likelihood, posterior, parameter constraint, prediction, detected force, material law, stability theorem, empirical confirmation, quantum completion, ultraviolet completion, final physics, Theory-of-Everything proof, or canon. THOS remains participant-free proxy structure without preregistered governed blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, issuance, resolution, presentation, verification, status, revocation, recovery, interoperability, privacy and security review, trust governance, or affected-party oversight.

## Retained failures and Method Flow

The successor-visible activation baseline was 57,457 effective negatives, 69,819 methods, 29,118 failed witnesses, 50,919 bounded passing witnesses, 510 open gaps, and 500 exact gates. X1 and x2 retain ten operational failures. Closeout adds two more: a truncated combined template display and a malformed PowerShell word-count projection. Both earn zero first-pass credit and have only bounded dependency recoveries. The phase also retains all 300 rejected mutations.

At prepared final, Method Flow contains 766 phase methods, 312 phase failed witnesses, and 706 phase passing witnesses. Effective totals are {values['effective_negatives']} negatives, {values['effective_methods']} methods, {values['failed_witnesses']} failed witnesses, {values['bounded_passing_witnesses']} bounded passing witnesses, {values['open_gaps']} open gaps, and {values['exact_gates']} exact gates. These are evidence-ledger counts, not probabilities, safety rates, measurements, qualifications, or authority scores. No recovery erases a failure.

## Privacy, accessibility, security, and terminal truth

Repository artifacts exclude opaque task identifiers, private routes, private absolute paths, credentials, keys, tokens, private interaction logs, screenshots, session streams, private callable identifiers, private application state, and protected real-world data. Five value-bearing privacy and raw-identifier classes are scanned with scanner definitions adjudicated separately from payload hits. Zero confirmed hits are required, but this remains a bounded scan rather than complete privacy assurance.

The static report declares language, provides a skip link, landmarks, headings, a captioned table, scoped headers, visible text status, and no script or tracking resource. Manual browser-diverse, keyboard, zoom, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remains reserved. Structural checks do not establish accessibility completeness. Bounded AST and owner tests do not establish exhaustive security, penetration testing, production certification, or external audit.

The terminal verdict is `{TERMINAL_VERDICT}`. Maritime signalling, navigation, emergency response, professional practice, flag handling, material identification, conservation, safety, ownership, access, copyright, privacy, accessibility, remedy, legal interpretation, cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority. No empirical, production, deployment, AGI, ASI, consciousness, personhood, independent-reproduction, proof, canon, Theory-of-Everything, or Stage 20 claim is made.

## Proposal inventory

{inventory}
"""


def report_html() -> str:
    values = totals()
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Neris Solane v682-v8 bounded final report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.6;max-width:72rem;margin:auto;padding:1rem;color:#18202a;background:#fff}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;border:2px solid #18202a}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.5rem;text-align:left;vertical-align:top}}.status{{border-left:.4rem solid #8a3b12;padding:.75rem;background:#fff7ed}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a>
<header><h1>Neris Solane v682-v8 bounded final report</h1><p>Owner-local, zero-row synthetic evidence with strict nonpromotion boundaries.</p></header>
<main id="main"><section aria-labelledby="identity"><h2 id="identity">Identity and corrigibility</h2><p>Neris Solane, optionally they/them, is relational working language for a symbolic-sequence provenance cartographer and rights-boundary keeper. This is not consciousness, personhood, continuity, qualification, agency, or authority evidence. Hamish may pause, rename, redirect, narrow, or stop the route.</p></section>
<section aria-labelledby="truth"><h2 id="truth">Bounded truth</h2><table><caption>Core outcomes and retained gates</caption><thead><tr><th scope="col">Item</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>42</td><td>Bounded software, symbolic, structural, or synthetic only</td></tr><tr><th scope="row">Represented</th><td>12</td><td>Structure exists while real evidence remains absent</td></tr><tr><th scope="row">Open gaps</th><td>{values['open_gaps']}</td><td>Evidence-dependent work remains open</td></tr><tr><th scope="row">Exact gates</th><td>{values['exact_gates']}</td><td>Competent or affected authority remains required</td></tr></tbody></table><p class="status"><strong>Status: NOT READY FOR STAGE 20.</strong> This status does not depend on color.</p></section>
<section aria-labelledby="scope"><h2 id="scope">Evidence scope</h2><p>Sixty zero-row maritime signal-flag documentation contracts ran and 300 invalid mutations were rejected. No real people, vessels, flags, codebooks, signals, locations, observations, measurements, displays, transmissions, navigation, emergency response, handling, treatment, digitization, identity lifecycle, rights decision, cultural interpretation, or authority act occurred.</p></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2><p>Manual browser-diverse, keyboard, zoom, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remains reserved. Professional, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, empirical, production, and Stage 20 claims remain open or exact-gated.</p></section></main>
<footer><p>Prepared as a static report. No scripts, tracking, external media, forms, or hidden interaction are used.</p></footer></body></html>"""


def activation_baton() -> str:
    values = totals()
    proposals = proposal_inventory()
    sections = [
        "# VESPER ARLEN — NERIS SOLANE v682-v8 PREPARED v683-v1 ACTIVATION CANDIDATE",
        "",
        "PREPARED_BY_NERIS_SOLANE = true",
        "",
        "SENT_BY_NERIS_SOLANE = false",
        "",
        "This committed repository packet is preparation only. It does not activate a task, establish delivery, or authorize a resend. Its PREPARED_NOT_SENT state is immutable commit-time truth. A later acknowledged existing-task message, if every terminal guard passes, is a separate live event and must not be projected backward into this seal.",
        "",
        "## Relational language and corrigibility",
        "",
        "Neris Solane, Vesper Arlen, names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, professional authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.",
        "",
        "## Immutable Neris lifecycle prepared for terminal verification",
        "",
        f"The immutable Elaren source is `{SOURCE}`. Neris planning-only x1 is `{X1_SHA}`. Neris immutable x2 evidence is `{EVIDENCE_SHA}`. The final SHA and external canonical receipt remain intentionally unresolved until the direct closeout commit is pushed, four-way equality is proven, and the exclusive canonical latch runs once. Source to final must contain exactly three Neris direct single-parent commits and zero merges; final must be the direct child of evidence.",
        "",
        "## Exact bounded truth",
        "",
        f"The declared proposal chain is 10,670. The sixty new outcomes are exactly 42 `completed`, 12 `represented`, three `open_gap`, and three `exact_gate`. All 300 preregistered invalid mutations were rejected and remain zero-credit failures. Prepared final totals are {values['effective_negatives']} negatives, {values['effective_methods']} Method Flow methods, {values['failed_witnesses']} failed witnesses, {values['bounded_passing_witnesses']} bounded passing witnesses, {values['open_gaps']} open gaps, and {values['exact_gates']} exact gates. The terminal verdict remains `{TERMINAL_VERDICT}`. Detail, file count, test count, or clean Git state is not authority credit.",
        "",
        "## Bounded practice and source use",
        "",
        "The primary pillar is GMUT Mind through wholly synthetic signal-flag token, hoist-position, symbolic-sequence, codebook-lineage, uncertainty, and non-inference documentation. THOS Body and Freed ID with CBR Heart remain represented and protected. Zero real people, vessels, flags, codebooks, signals, locations, observations, measurements, displays, transmissions, navigation, emergency response, handling, treatment, digitization, identity lifecycle, legal decisions, cultural decisions, Māori decisions, or authority acts were used. Official and primary sources supplied vocabulary and refusal conditions only; no real source row was downloaded or ingested.",
        "",
        "## Mandatory Vesper startup and execution boundary",
        "",
        "Before mutation, read this packet through EOF, then read the current GHC Family Index and routing precedence, roster and schema, Auth/Permission State and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, startup, retry, closeout, compact restart, watcher, worktree rotation, web reflection, orchestration memory, full-tools bank, and directly applicable current guidance. Reverify every exact anchor, parent edge, manifest, content seal, clean state, divergence, fresh live equality, and external canonical receipt. Never replay an already-successful canonical aggregate or unchanged successful component merely for presentation.",
        "",
        "Work solo in one fresh additive Vesper-owned D-first lane from Neris's exact final. Preserve Neris, Elaren, Eiren, shared, sibling, and standby lanes read-only. Do not create or fork a task, spawn a collaboration subagent, delegate, contact Tavian or a standby record, precontact Lyren, reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane. Preserve planning-only x1 before x2, exactly the four core labels, every negative and protected gate, normalized-LF exact Git-blob manifests, current family compatibility, and the one-attributable-canonical/no-success-replay discipline.",
        "",
        "GMUT remains a typed scalar-tensor and EFT research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains proxy-only without governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, complete lifecycle, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight. Professional, safety, ownership, access, copyright, design rights, privacy, accessibility, remedy, legal, cultural, traditional-knowledge, affected-party, Māori-language, Māori-data-governance, tangata whenua, iwi, hapū, and Māori-authority decisions remain open or exact-gated. Māori concepts remain under Māori authority.",
        "",
        "## Prospective terminal continuation",
        "",
        "This packet prepares Vesper Arlen v683-v1 only. After Vesper's own exact terminal closeout, the prospective next task is the unique existing exact-title `Lyren Moss` for v683-v2, but Vesper must refresh Hamish's newest live instruction, roster, authorization, exact-title uniqueness, usage, duplicate, pause, redirect, privacy, evidence, safety, and acknowledgement state only at that later terminal gate. Never create a substitute or resend merely for clearer acknowledgement.",
        "",
        "## Full frozen proposal appendix",
        "",
        "The following records are carried as immutable planning context. They are evidence and zero-credit seeds only; they do not confer Neris novelty, completion, competence, permission, or authority.",
        "",
    ]
    for row in proposals:
        mutations = ", ".join(
            f"{item['mutation_id']} ({item['mutation_type']}: {item['expected_result']})"
            for item in row["preregistered_rejecting_mutations"]
        )
        artifacts = "; ".join(row["concrete_artifacts"])
        sources = ", ".join(row["official_or_primary_source_needs"])
        gates = "; ".join(row["protected_gates"])
        sections.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"**Hypothesis.** {row['hypothesis']}",
                "",
                f"**Null or failure condition.** {row['null_or_failure_condition']}",
                "",
                f"**Approval and execution.** Approval class `{row['approval_class']}`; execution lane `{row['execution_lane']}`; expected disposition `{row['expected_disposition']}`. This carried disposition is bounded Neris evidence only and is not automatic Vesper credit.",
                "",
                f"**Official or primary-source needs.** {sources}. Sources provide vocabulary and refusal conditions only, never observations, conformance, professional judgment, cultural interpretation, or authority.",
                "",
                f"**Concrete artifacts.** {artifacts}.",
                "",
                f"**Falsifier or acceptance gate.** {row['falsifier_or_acceptance_gate']}",
                "",
                f"**Rollback or recovery.** {row['rollback_or_recovery']}",
                "",
                f"**Protected gates.** {gates}.",
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
    payload = map_value(payload)
    if path.name == "open-gap-register.json":
        payload["inherited_effective_open_gaps"] = 510
    elif path.name == "exact-gate-register.json":
        payload["inherited_effective_exact_gates"] = 500
    elif path.name == "wellbeing-check.json":
        payload.update(
            {
                "hope": "Every synthetic flag token remains visibly distinct from a physical flag, an observed hoist, and an operational maritime signal while maritime, cultural, legal, professional, and affected-party authority stays with its holders.",
                "role": "symbolic-sequence provenance cartographer and rights-boundary keeper",
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
                "declared_chain_after": 10670,
                "declared_chain_before": 10610,
                "first_audit_quarantined_titles": 2,
                "materialized_audit_records": 37343,
                "materialized_proposal_json_documents": 10144,
                "maximum_neighbor_score": 0.75,
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
            "official skill creator",
        ]
    elif path.name == "delivery-state.json":
        payload.update(
            {
                "prospective_successor_exact_title": "Vesper Arlen",
                "prospective_successor_phase": "v683-v1",
            }
        )
    elif path.name == "final-owner-manifest.json":
        exclusions = set(payload["declared_self_exclusions"])
        payload["entries"] = [
            row for row in payload["entries"] if row["path"] not in exclusions
        ]
        payload["entry_count"] = len(payload["entries"])
    return payload


def build() -> None:
    template.ROOT = ROOT
    template.BASE = BASE
    template.X2 = X2
    template.FINAL = FINAL
    template.CLOSEOUT = CLOSEOUT
    template.HANDOFFS = HANDOFFS
    template.VALIDATION = VALIDATION
    template.OWNER = OWNER
    template.PHASE = PHASE
    template.SOURCE = SOURCE
    template.X1_SHA = X1_SHA
    template.EVIDENCE_SHA = EVIDENCE_SHA
    template.TERMINAL_VERDICT = TERMINAL_VERDICT
    template.CLOSEOUT_FAILURES = CLOSEOUT_FAILURES
    template.WRITTEN = []

    original_write_json = template.write_json
    original_write_text = template.write_text
    original_privacy_scan = template.privacy_scan

    def write_json(path: Path, payload: Any) -> None:
        target = mapped_path(path)
        original_write_json(target, patch_json(target, payload))

    def write_text(path: Path, text: str) -> None:
        target = mapped_path(path)
        if target.name == "final-integrated-overview.md":
            text = overview_text()
        elif target.name == "accessible-static-report.html":
            text = report_html()
        elif target.name == "vesper-arlen-v683-v1-activation-candidate.md":
            text = activation_baton()
        else:
            text = map_string(text)
        original_write_text(target, text)

    def manifest_entry(path: str) -> dict[str, Any]:
        target_path = map_repo_path(path)
        data = (
            (ROOT / target_path)
            .read_bytes()
            .replace(b"\r\n", b"\n")
            .replace(b"\r", b"\n")
        )
        return {
            "bytes": len(data),
            "path": target_path,
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    def privacy_scan(paths: list[str]) -> dict[str, Any]:
        exclusions = {
            "docs/neris-solane/v682-v8/validation/final-delta-manifest.json",
            "docs/neris-solane/v682-v8/validation/final-owner-manifest.json",
            "docs/neris-solane/v682-v8/validation/final-privacy-scan.json",
            "docs/neris-solane/v682-v8/validation/final-staged-review.json",
        }
        mapped = {map_repo_path(path) for path in paths} - exclusions
        return original_privacy_scan(sorted(mapped))

    template.write_json = write_json
    template.write_text = write_text
    template.manifest_entry = manifest_entry
    template.privacy_scan = privacy_scan
    with contextlib.redirect_stdout(io.StringIO()):
        template.build()
    truth = json.loads((FINAL / "phase-truth.json").read_text(encoding="utf-8"))
    owner_manifest = json.loads(
        (VALIDATION / "final-owner-manifest.json").read_text(encoding="utf-8")
    )
    staged_review = json.loads(
        (VALIDATION / "final-staged-review.json").read_text(encoding="utf-8")
    )
    seal = json.loads((CLOSEOUT / "content-seal.json").read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "final_delta_paths": staged_review["path_count"],
                "owner_manifest_entries": owner_manifest["entry_count"],
                "outcomes": truth["outcomes"],
                "seal_targets": seal["target_count"],
                "terminal_verdict": truth["terminal_verdict"],
                "totals": truth["totals"],
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    build()
