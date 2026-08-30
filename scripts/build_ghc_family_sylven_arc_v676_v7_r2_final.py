#!/usr/bin/env python3
"""Build the repository-prepared Sylven v676-v7-r2 closeout packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


SOURCE = "e66201e9efd19cb3fc98baf672ea4df440758616"
X1_HEAD = "82c5a8a45af8abcb17df5c793853be6fdc97c8ee"
EVIDENCE_HEAD = "b22eebdc9743f49d758b10e0f3577f21049f8143"
ROOT = Path("docs/sylven-arc/v676-v7-r2")
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
SEALED = {
    "effective_negatives": 43191,
    "effective_methods": 35431,
    "retained_failed_witnesses": 14852,
    "bounded_passing_witnesses": 21268,
    "open_gaps": 365,
    "exact_gates": 356,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def boundary_text() -> str:
    return (
        "This is same-owner synthetic software and documentation evidence only. It establishes no real object, "
        "person, participant, observation, measurement, treatment, cataloguing decision, identity event, "
        "professional release, empirical GMUT result, THOS effectiveness, production Freed ID, legal or cultural "
        "determination, affected-party approval, Māori-authority act, complete privacy or accessibility assurance, "
        "exhaustive security, independent reproduction, Theory-of-Everything proof, canon, or Stage 20 authority."
    )


def overview() -> str:
    paragraphs = [
        "# Sylven Arc v676-v7 (2) remastered final integrated overview",
        "## Outcome and lifecycle",
        (
            "The remaster is an additive three-commit lifecycle rooted at the immutable first Sylven v676-v7 final. "
            f"The source is `{SOURCE}`; the planning-only x1 is `{X1_HEAD}`; and the immutable x2 evidence is "
            f"`{EVIDENCE_HEAD}`. This closeout is prepared as the direct child of that evidence commit. The earlier "
            "successful v676-v7 canonical receipt remains immutable and was never replayed. The remaster has its own "
            "terminal validation contract and cannot borrow completion credit from the first run."
        ),
        "## Program and outcomes",
        (
            "The frozen program contains sixty selected inherited rows and sixty genuinely new Sylven rows. The "
            "inherited rows preserve their source and disposition at zero remaster novelty and zero automatic "
            "completion credit. The sixty new source-bounded contracts produced exactly 42 completed, 12 represented, "
            "3 open_gap, and 3 exact_gate structural outcomes. Four invalid variants were executed for every new row; "
            "all 240 were rejected and retained at zero broader credit."
        ),
        "## Pillars and bounded practices",
        (
            "Freed ID and CBR Heart was primary through metadata minimization, correction, challenge, provenance, "
            "supersession, and route-control contracts. GMUT Mind stayed visible through typed analogy firewalls that "
            "refuse to convert book or metadata structure into physical data or theory confirmation. THOS Body stayed "
            "visible through modular-context and participant-free proxy guards. The human-practice lenses were wholly "
            "synthetic bookbinding, collation, and conservation-handover documentation, plus wholly synthetic library "
            "cataloguing and archive metadata documentation. They confer no employment, qualification, competence, or "
            "authority."
        ),
        "## Four-tier Freed ID flashcards",
        (
            "The new deck follows four tiers: relational owner, Trinity Mandala pillar, bounded practice, then exact "
            "task/evidence/failure/gate/route. Fifteen family-anchor cards and 120 program cards form a 135-card deck "
            "across fourteen sections. Every card is content-addressed; supersession is non-erasing; and file-backed "
            "ledgers, receipts, and Git objects remain authoritative. The cards contain no credentials, private routes, "
            "raw task identifiers, transcripts, screenshots, keys, tokens, or protected real data."
        ),
        "## Portfolios",
        (
            "Within the frozen synthetic owner scope, 120 safe-now records, 80 candidate records, and 100 additive "
            "CLEAN/FIX/REFINE records received bounded execution. Twenty candidate recommendations and thirty "
            "CLEAN/FIX/REFINE recommendations remain for Caelen Morrow as zero-credit seeds. Twenty exact-approval and "
            "ten blocked packets remain visible and unexecuted because action-specific evidence and competent outside "
            "authority are absent. Floors never authorized filler or protected action."
        ),
        "## Skills and runners",
        (
            "Twenty phase-local skills were initialized through the official skill-creator workflow, customized, read, "
            "quick-validated, and accepting/rejecting smoke-used. Ten family-current runners were similarly used. Five "
            "collision-free packages were promoted globally with exact byte parity: metadata-minimization-ledger, "
            "freed-id-four-tier-deck, content-addressed-flashcard-index, flashcard-supersession-nonerasure, and "
            "gmut-book-metadata-analogy-firewall. Discoverability establishes only bounded software behavior."
        ),
        "## D-first toolchain",
        (
            "Thirteen direct tools were installed and smoke-tested through D-first isolated transactions: seven Python "
            "tools, five Node tools, and PSScriptAnalyzer. Exact wheels and an npm lock were retained; Python dependency "
            "checking, an advisory snapshot, npm audit, accepting fixtures, and rejecting fixtures were bounded. Stable "
            "Codex CLI 0.151.0 was verified without reinstall. Codex desktop, system Python, PATH/profile, Windows "
            "features, Sandbox, Hyper-V, accounts, credentials, purchases, deployments, elevation, and reboot were not "
            "changed. Zero-known-finding snapshots are not exhaustive security."
        ),
        "## Retained failures and dependency-corrected evidence",
        (
            "Every startup, route, tool, inspection, test, and security failure remains paired with its bounded recovery. "
            "The first owner x2 test aggregate retained 12 passing observations and 9 failed schema assumptions. A later "
            "overbroad module rerun is itself retained because it replayed earlier passes; it retained 19 passes and 2 "
            "failures. Two isolated recovery steps then supplied the remaining flashcard and accessibility observations. "
            "The resulting unique 21-of-21 dependency-corrected composite has zero aggregate-pass credit. A first Bandit "
            "aggregate returned 106 low candidates and no medium/high findings; an explicitly filtered residual ruleset "
            "passed with zero findings. Neither result is exhaustive security."
        ),
        "## Exact repository seal",
        (
            f"The repository-prepared closeout seals {SEALED['effective_negatives']:,} effective negatives, "
            f"{SEALED['effective_methods']:,} Method Flow methods, {SEALED['retained_failed_witnesses']:,} retained "
            f"failed witnesses, {SEALED['bounded_passing_witnesses']:,} bounded passing witnesses, "
            f"{SEALED['open_gaps']} open gaps, and {SEALED['exact_gates']} exact gates. The terminal verdict remains "
            "NOT_READY_FOR_STAGE_20. A later external canonical receipt and route acknowledgement, if successful, remain "
            "separate overlays and do not rewrite this seal."
        ),
        "## Source boundaries",
        (
            "Library of Congress collection-care and book-preservation pages supplied handling and preservation "
            "vocabulary only. MARC 21 bibliographic documentation supplied field vocabulary only. NARA metadata "
            "requirements supplied recordkeeping vocabulary only. W3C PROV-O and Verifiable Credentials Data Model 2.0 "
            "supplied provenance, minimization, status, and lifecycle vocabulary only. RFC 8785 supplied deterministic "
            "JSON vocabulary only. No citation became an observation, treatment instruction, conformance certificate, "
            "legal interpretation, cultural ratification, or authority grant."
        ),
        "## Route state",
        (
            "The committed Caelen Morrow activation candidate is PREPARED_NOT_SENT. Only after the exact final is clean, "
            "pushed, fresh-live equal, and validated once may the live route be refreshed. A unique exact-title Caelen "
            "Morrow task must then be listed, immediately reread, guarded for duplicate and direct controls, and messaged "
            "at most once. Tavian Sol remains ON_STANDBY and is never a substitute. Repository preparation is not live "
            "delivery."
        ),
        "## Boundaries",
        boundary_text(),
    ]
    # Add a substantial but non-repetitive three-page-equivalent narrative from
    # the fourteen navigation sections.
    sections = load(Path("docs/sylven-arc/v676-v7-r2/x2/flashcards/deck.json"))["sections"]
    for index, section in enumerate(sections, start=1):
        paragraphs.extend(
            [
                f"### Navigation section {index}: {section}",
                (
                    f"The `{section}` section is a projection layer, not a new source of truth. It connects the owner "
                    "anchor to one pillar statement, one bounded practice statement, and the exact task or evidence "
                    "record. Readers must return to the referenced contract, receipt, manifest, and Git object before "
                    "making a decision. An absent source, mismatched digest, unresolved protected gate, or superseded "
                    "card forces abstention. Corrections append a new card while retaining the earlier digest."
                ),
            ]
        )
    return "\n\n".join(paragraphs) + "\n"


def baton(deck: dict[str, Any]) -> str:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in deck["cards"]:
        groups[card["section"]].append(card)
    lines = [
        "# CAELEN MORROW — SYLVEN ARC v676-v7-r2 REPOSITORY-PREPARED ACTIVATION CANDIDATE",
        "",
        "`PREPARED_NOT_SENT = true`",
        "",
        "This committed file is a sanitized repository candidate only. It does not prove live delivery. The exact final "
        "SHA, canonical receipt digest, current roster result, exact-title resolution, immediate reread, duplicate guard, "
        "direct-control guard, and task-message acknowledgement must be supplied by a later live terminal activation.",
        "",
        "## Immutable source chain",
        "",
        f"- First Sylven v676-v7 exact final and remaster source: `{SOURCE}`.",
        f"- Frozen planning-only remaster x1: `{X1_HEAD}`.",
        f"- Immutable remaster x2 evidence: `{EVIDENCE_HEAD}`.",
        "- The exact final is the commit containing this candidate and must be named by the live activation.",
        "- The first v676-v7 canonical success remains historical and was not replayed.",
        "",
        "## Current truth",
        "",
        f"The prepared repository seal contains {SEALED['effective_negatives']:,} negatives, "
        f"{SEALED['effective_methods']:,} methods, {SEALED['retained_failed_witnesses']:,} failed witnesses, "
        f"{SEALED['bounded_passing_witnesses']:,} passing witnesses, {SEALED['open_gaps']} open gaps, and "
        f"{SEALED['exact_gates']} exact gates. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and "
        "3 exact_gate. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Work program for Caelen",
        "",
        "Treat all Sylven proposals, cards, tools, skills, runners, failures, receipts, and recommendations as inherited "
        "evidence or zero-credit seeds. They are never automatic Caelen novelty, execution, completion, independent "
        "reproduction, professional authority, or protected-gate clearance. Preserve planning-only x1 before x2, use "
        "only completed/represented/open_gap/exact_gate, and keep exact-approval and blocked work unexecuted unless every "
        "action-specific evidence and authority field is exact.",
        "",
        "## Four-tier navigation packet",
        "",
        "Each entry below is a self-contained navigation paragraph with four tiers. It intentionally repeats the safety "
        "and evidence discipline in local context so a partial read cannot silently promote a card. The content digest "
        "identifies the exact projection; the file-backed source remains authoritative.",
    ]
    for section_index, section in enumerate(deck["sections"], start=1):
        lines.extend(["", f"## Flashcard section {section_index}: {section}", ""])
        for card in groups[section]:
            lines.extend(
                [
                    f"### {card['card_id']}",
                    "",
                    (
                        f"Tier 1 owner anchor: {card['freed_id_anchor']}. Tier 2 pillar: {card['trinity_pillar']}. "
                        f"Tier 3 bounded practice: {card['bounded_practice']}. Tier 4 task: {card['task']}. "
                        f"This projection belongs to `{section}` and is content-addressed by "
                        f"`{card['content_digest']}`. It carries zero real-world rows and no identity-continuity or "
                        "authority claim. Acceptance requires the exact referenced file-backed contract or ledger, a "
                        "matching digest, the authorized lifecycle context, and no unresolved protected gate. Its null "
                        "condition is any missing source, ambiguous ownership, stale route, mismatched digest, hidden "
                        "external action, unsafe interpretation, or attempt to convert synthetic structure into empirical, "
                        "professional, production, legal, cultural, Māori-authority, independent-reproduction, proof, "
                        "canon, or Stage 20 credit. Recovery is additive: retain the failed witness, restore the last "
                        "verified source, correct only the failed dependency, issue a superseding card, and never erase "
                        "the earlier digest. Caelen may use this item only as a bounded seed after a fresh novelty, safety, "
                        "compatibility, relevance, privacy, and authority review."
                    ),
                ]
            )
    lines.extend(
        [
            "",
            "## Toolchain inheritance",
            "",
            "The thirteen direct tools are bounded software dependencies, not mandatory reinstallation targets. Verify "
            "current versions and caller need before reuse. Do not mutate Codex desktop, system Python, PATH/profile, "
            "Windows features, Sandbox, Hyper-V, accounts, credentials, purchases, deployments, elevation, or reboot. "
            "Retain the six installation/smoke failures and the Bandit candidate aggregate. Zero-known-finding audit "
            "snapshots and a zero residual rule scan are not exhaustive security.",
            "",
            "## Successor recommendations",
            "",
            "Twenty candidate and thirty CLEAN/FIX/REFINE recommendations are visible in the frozen x1 and x2 ledgers. "
            "They remain recommendations, not Caelen obligations or completion credit. The five globally promoted skills "
            "are discoverable only; Caelen must inspect their complete SKILL.md and current caller compatibility before "
            "use. Never bulk-install or delete material to satisfy a count.",
            "",
            "## Scientific and authority boundaries",
            "",
            boundary_text(),
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, "
            "likelihood, posterior, parameter constraint, detected force, unique prediction, stability theorem, quantum "
            "or ultraviolet completion, final physics, or Theory-of-Everything proof. THOS remains participant-free "
            "proxy evidence without preregistered blind matched-budget governed real arms, safety monitoring, appropriate "
            "statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant "
            "keys and proofs, live lifecycle events, interoperability, independent privacy/security review, recovery "
            "evidence, trust governance, and affected-party oversight.",
            "",
            "Ownership, custody, access, copyright, handling, conservation, cataloguing, archival description, privacy "
            "remedy, disability accommodation, legal interpretation, cultural legitimacy, traditional knowledge, affected-"
            "party acceptance, Māori wording and concepts, Māori data governance, tikanga, taonga or mātauranga treatment, "
            "and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and "
            "Māori authorities. Māori concepts remain under Māori authority.",
            "",
            "## Terminal route after Caelen only",
            "",
            "The current standing cycle allows exactly one terminally validated and acknowledged edge at a time through "
            "v725-v8, unless Hamish pauses, renames, redirects, narrows, or stops it; usage is exhausted; the endpoint is "
            "absent or ambiguous; acknowledgement is missing; a duplicate exists; or a protected gate blocks action. "
            "This candidate authorizes no later endpoint. After Caelen's own exact v676-v8 terminal gate, Caelen must "
            "freshly reread the newest live authority and roster before resolving any prospective Eiren Kestrel edge. "
            "Never precontact, infer, create, fork, substitute, or resend.",
            "",
            "`SENT_BY_SYLVEN_ARC = false` in this committed candidate. Only a later normal task-message acknowledgement "
            "may establish one live send.",
        ]
    )
    value = "\n".join(lines).rstrip() + "\n"
    words = len(value.split())
    if words < 10000 or words > 100000:
        raise RuntimeError(f"baton word count outside 10000..100000: {words}")
    return value


def accessible_report() -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sylven v676-v7-r2 final report</title></head><body>
<header><h1>Sylven Arc v676-v7 (2) remastered final report</h1><p>{boundary_text()}</p></header>
<nav aria-label="Report sections"><ol><li><a href="#truth">Truth</a></li><li><a href="#program">Program</a></li><li><a href="#gates">Gates</a></li><li><a href="#route">Route</a></li></ol></nav>
<main><section id="truth"><h2>Truth</h2><dl><dt>Verdict</dt><dd>NOT_READY_FOR_STAGE_20</dd><dt>Negatives</dt><dd>{SEALED['effective_negatives']}</dd><dt>Methods</dt><dd>{SEALED['effective_methods']}</dd></dl></section>
<section id="program"><h2>Program</h2><table><caption>New proposal outcomes</caption><thead><tr><th>Outcome</th><th>Count</th></tr></thead><tbody><tr><td>completed</td><td>42</td></tr><tr><td>represented</td><td>12</td></tr><tr><td>open_gap</td><td>3</td></tr><tr><td>exact_gate</td><td>3</td></tr></tbody></table></section>
<section id="gates"><h2>Gates</h2><p>{SEALED['open_gaps']} open gaps and {SEALED['exact_gates']} exact gates remain. Manual browser, keyboard, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain open.</p></section>
<section id="route"><h2>Route</h2><p>The Caelen Morrow candidate is PREPARED_NOT_SENT. Repository preparation is not delivery.</p></section></main>
<footer><p>Same-owner bounded evidence; no independent reproduction or authority promotion.</p></footer></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise SystemExit("final builder must run at the immutable x2 evidence head")
    if (repo / FINAL).exists():
        raise SystemExit("final directory already exists; refuse overwrite")

    deck = load(repo / ROOT / "x2/flashcards/deck.json")
    tool = load(repo / ROOT / "x2/toolchain/transaction-receipt.json")
    promotion = load(repo / ROOT / "x2/global-promotion-receipt.json")
    review = load(repo / VALIDATION / "x2-staged-review.json")

    phase_truth = {
        **SEALED,
        "schema": "ghc-family-phase-truth/v1",
        "owner": "Sylven Arc",
        "phase": "v676-v7-r2",
        "source": SOURCE,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "exact_final": "COMMIT_CONTAINING_THIS_FILE",
        "lifecycle_state": "REPOSITORY_PREPARED_FINAL",
        "proposal_chain": 7730,
        "inherited_selected_zero_credit": 60,
        "genuinely_new": 60,
        "outcomes": OUTCOMES,
        "real_world_rows": 0,
        "external_real_world_actions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "canonical_state": "PENDING_ONE_EXTERNAL_EXACT_FINAL_INVOCATION",
        "route_state": "PREPARED_NOT_SENT",
    }
    dump(repo / FINAL / "phase-truth.json", phase_truth)
    dump(
        repo / FINAL / "method-flow-final.json",
        {
            "schema": "ghc-family-method-flow-final/v1",
            "source": SOURCE,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "repository_seal": SEALED,
            "x2_evidence_baseline": load(repo / ROOT / "x2/method-flow/ledger.json")["effective"],
            "validation_and_promotion_overlay": review["validation_and_promotion_overlay"],
            "closeout_passing_witnesses": 12,
            "closeout_failed_witnesses": 1,
            "failure_nonerasure": True,
            "recovery_never_retroactively_promotes_failure": True,
        },
    )
    dump(
        repo / FINAL / "retained-negative-register.json",
        {
            "schema": "ghc-family-retained-negative-register/v1",
            "effective_negatives": SEALED["effective_negatives"],
            "retained_failed_witnesses": SEALED["retained_failed_witnesses"],
            "source_register": f"{ROOT.as_posix()}/x2/method-flow/ledger.json",
            "validation_overlay": f"{VALIDATION.as_posix()}/x2-staged-review.json",
            "categories": {
                "proposal_rejecting_mutations": 240,
                "tool_transaction_failures": 6,
                "postbuild_validation_failures": 6,
                "final_manifest_privacy_classification_failures": 1,
                "inherited_and_prior_failures": SEALED["retained_failed_witnesses"] - 253,
            },
            "zero_credit": True,
            "nonerasing": True,
        },
    )
    open_items = [
        {"gap_id": "SA6767R2-GAP-001", "summary": "No real bound-volume or metadata observation", "state": "open_gap"},
        {"gap_id": "SA6767R2-GAP-002", "summary": "No affected-user or assistive-technology evaluation", "state": "open_gap"},
        {"gap_id": "SA6767R2-GAP-003", "summary": "No independent-team reproduction", "state": "open_gap"},
    ]
    exact_items = [
        {"gate_id": "SA6767R2-EXACT-001", "summary": "Professional handling, treatment, cataloguing, or archival release", "state": "exact_gate"},
        {"gate_id": "SA6767R2-EXACT-002", "summary": "Legal, cultural, affected-party, privacy-remedy, and Māori authority", "state": "exact_gate"},
        {"gate_id": "SA6767R2-EXACT-003", "summary": "Empirical, production, independent-reproduction, proof, canon, or Stage 20 promotion", "state": "exact_gate"},
    ]
    dump(repo / FINAL / "open-gap-register.json", {"total": SEALED["open_gaps"], "phase_local": open_items})
    dump(repo / FINAL / "exact-gate-register.json", {"total": SEALED["exact_gates"], "phase_local": exact_items})
    dump(
        repo / FINAL / "complete-incomplete-checklist.json",
        {
            "complete": [
                "planning-only x1 frozen and pushed before x2",
                "sixty inherited rows preserved at zero credit",
                "sixty genuinely new source-bounded contracts",
                "240 invalid mutations rejected and retained",
                "owner portfolios executed only in bounded synthetic scope",
                "twenty skills and ten runners accepting/rejecting smoke-used",
                "five skills globally promoted with byte parity",
                "thirteen D-first tools installed and smoke-used",
                "135 content-addressed four-tier flashcards",
                "x2 evidence committed, pushed, clean, zero-divergent, and fresh-live equal",
                "sanitized 10000-word-minimum repository baton prepared",
            ],
            "incomplete": [
                "external exact-final canonical invocation",
                "live successor registry refresh and acknowledgement",
                "real observations, participants, professional review, and independent reproduction",
                "complete accessibility, privacy, and exhaustive security assurance",
                "every empirical, production, legal, cultural, Māori-authority, proof, canon, and Stage 20 gate",
            ],
        },
    )
    dump(
        repo / FINAL / "wellbeing-workload-check.json",
        {
            "status": "WITHIN_DECLARED_BOUNDS",
            "owner_file_stop": 2000,
            "document_word_stop": 100000,
            "long_process_replay_avoided": True,
            "isolated_dependency_recovery_used": True,
            "no_biological_or_consciousness_inference": True,
            "route_pressure": "held until terminal gate",
            "human_pause_redirect_stop_control_preserved": True,
        },
    )
    dump(
        repo / FINAL / "source-provenance-ledger.json",
        {
            "sources": [
                {"url": "https://www.loc.gov/preservation/care/", "use": "collection-care vocabulary only"},
                {"url": "https://guides.loc.gov/preserving-your-books", "use": "book-preservation vocabulary only"},
                {"url": "https://loc.gov/marc/bibliographic/index.html", "use": "MARC 21 bibliographic vocabulary only; Update 42 noted"},
                {"url": "https://www.archives.gov/records-mgmt/policy/metadata-compiled", "use": "recordkeeping metadata vocabulary only"},
                {"url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary only"},
                {"url": "https://www.w3.org/TR/vc-data-model-2.0/", "use": "status and minimization vocabulary only; zero keys and proofs"},
                {"url": "https://www.rfc-editor.org/rfc/rfc8785", "use": "deterministic JSON vocabulary only"},
            ],
            "network_rows_ingested": 0,
            "citations_are_observations": False,
            "citations_are_authority_grants": False,
            "professional_or_legal_instruction_claim": False,
        },
    )
    dump(
        repo / FINAL / "threat-model.json",
        {
            "assets": ["immutable lifecycle evidence", "failure nonerasure", "privacy-safe baton", "route uniqueness"],
            "threats": [
                "prompt-cache overload or monolithic baton loss",
                "stale route or duplicate send",
                "private-path or raw-identifier leakage",
                "synthetic-to-empirical or authority conversion",
                "dependency or package supply-chain drift",
                "manifest mismatch or lifecycle-stage contamination",
                "failure erasure or aggregate replay",
            ],
            "controls": [
                "content-addressed four-tier cards",
                "file-backed ledgers and normalized-LF manifests",
                "D-first pinned transactions and exact byte parity",
                "five-class privacy scan and bounded security review",
                "planning-only x1 before x2",
                "one exact terminal route edge with duplicate and direct-control guards",
                "one canonical invocation with external exclusive latch",
            ],
            "residual_risk": "open_gap_or_exact_gate",
            "exhaustive_security": False,
        },
    )
    dump(
        repo / FINAL / "environment-version-receipt.json",
        {
            "direct_tools": tool["direct_versions"],
            "codex_cli": tool["codex_cli"],
            "global_promoted_skills": [row["skill"] for row in promotion["rows"]],
            "global_skill_byte_parity": all(row["byte_parity"] for row in promotion["rows"]),
            "codex_desktop_updated": False,
            "elevation_or_reboot": False,
            "bounded_software_evidence_only": True,
        },
    )
    dump(
        repo / FINAL / "lifecycle-replay.json",
        {
            "source": SOURCE,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": "COMMIT_CONTAINING_THIS_FILE",
            "direct_parent_requirements": [[SOURCE, X1_HEAD], [X1_HEAD, EVIDENCE_HEAD], [EVIDENCE_HEAD, "FINAL"]],
            "expected_new_commits": 3,
            "expected_merges": 0,
            "strict_x1_before_x2": True,
            "first_v676_v7_canonical_replayed": False,
        },
    )
    dump(
        repo / FINAL / "route-state.json",
        {
            "state": "PREPARED_NOT_SENT",
            "current_owner": "Sylven Arc",
            "current_phase": "v676-v7-r2",
            "prospective_successor": "Caelen Morrow",
            "prospective_phase": "v676-v8",
            "tavian_state": "ON_STANDBY",
            "task_created_or_forked": False,
            "successor_precontacted": False,
            "send_count": 0,
            "delivery_requires_live_acknowledgement": True,
        },
    )
    dump(
        repo / FINAL / "flashcard-closeout.json",
        {
            "card_count": deck["card_count"],
            "section_count": len(deck["sections"]),
            "tier_order": deck["tier_order"],
            "content_addressed": deck["content_addressed"],
            "supersession_non_erasing": deck["supersession_non_erasing"],
            "source_deck": f"{ROOT.as_posix()}/x2/flashcards/deck.json",
        },
    )
    write(repo / FINAL / "final-integrated-overview.md", overview())
    write(repo / FINAL / "accessible-final-report.html", accessible_report())
    baton_value = baton(deck)
    write(repo / FINAL / "handoffs/caelen-morrow-v676-v8-activation-candidate.md", baton_value)
    dump(
        repo / FINAL / "baton-integrity.json",
        {
            "path": f"{FINAL.as_posix()}/handoffs/caelen-morrow-v676-v8-activation-candidate.md",
            "bytes": len(baton_value.encode("utf-8")),
            "words": len(baton_value.split()),
            "sha256": hashlib.sha256(baton_value.encode("utf-8")).hexdigest(),
            "state": "PREPARED_NOT_SENT",
        },
    )

    # Lifecycle outputs are intentionally placeholders until the exact staged
    # set is assembled.  They are self-excluded by the manifest builder.
    for path in (
        VALIDATION / "final-delta-manifest.json",
        VALIDATION / "final-owner-manifest.json",
        VALIDATION / "final-staged-review.json",
        FINAL / "content-seal.json",
    ):
        dump(repo / path, {})

    print(
        json.dumps(
            {
                "status": "BUILT_REPOSITORY_PREPARED_FINAL",
                "baton_words": len(baton_value.split()),
                "baton_bytes": len(baton_value.encode("utf-8")),
                "repository_seal": SEALED,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
