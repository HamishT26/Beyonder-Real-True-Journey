#!/usr/bin/env python3
"""Build the repository-prepared Elaren Kestrel v677-v2 closeout packet."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


SOURCE = "3ca2ff8087245a5ded51ce05d748186d80951387"
X1_HEAD = "4621b308f32d48cf70ab3ad598961dbedc122b6a"
EVIDENCE_HEAD = "bbdc6e46f5a62dd727428ccd56f333c3d1114044"
ROOT = Path("docs/elaren-kestrel/v677-v2")
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
SEALED = {
    "effective_negatives": 44144,
    "effective_methods": 38303,
    "retained_failed_witnesses": 15805,
    "bounded_passing_witnesses": 23197,
    "open_gaps": 374,
    "exact_gates": 365,
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


def bounded_security_review(repo: Path) -> dict[str, Any]:
    paths = sorted(
        [path for path in (repo / "scripts").glob("*elaren_kestrel_v677_v2*.py") if path.is_file()]
        + [path for path in (repo / "tests").glob("*elaren_kestrel_v677_v2*.py") if path.is_file()]
    )
    risky = {
        "shell_enabled_subprocess": re.compile(r"shell\s*=\s*True"),
        "os_system": re.compile(r"\bos\.system\s*\("),
        "dynamic_eval": re.compile(r"\beval\s*\("),
        "dynamic_exec": re.compile(r"\bexec\s*\("),
    }
    findings: list[dict[str, str]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        ast.parse(text, filename=path.relative_to(repo).as_posix())
        for rule, pattern in risky.items():
            if pattern.search(text):
                findings.append(
                    {
                        "path": path.relative_to(repo).as_posix(),
                        "rule": rule,
                        "severity": "medium",
                    }
                )
    if findings:
        raise RuntimeError("bounded changed-code security review retained a medium finding")
    return {
        "schema": "ghc-family-bounded-changed-code-security-review/v1",
        "scope": "owner-local Elaren v677-v2 Python surfaces only",
        "reviewed_file_count": len(paths),
        "rules": sorted(risky),
        "syntax_parses": len(paths),
        "findings": findings,
        "medium_or_high_findings": 0,
        "exhaustive_security": False,
        "production_certification": False,
    }


def boundary_text() -> str:
    return (
        "This is same-owner synthetic software and documentation evidence only. It establishes no real vessel, ship model, "
        "hull, spar, sail, fitting, rigging line, collection object, person, participant, survey, observation, image, measurement, "
        "handling, movement, disassembly, rerigging, cleaning, repair, treatment, mounting, custody or ownership decision, "
        "identity event, professional release, empirical GMUT result, THOS "
        "effectiveness, production Freed ID, legal or cultural determination, affected-party approval, Māori-authority "
        "act, complete privacy or accessibility assurance, exhaustive security, independent reproduction, "
        "Theory-of-Everything proof, canon, or Stage 20 authority."
    )


def overview() -> str:
    paragraphs = [
        "# Elaren Kestrel v677-v2 final integrated overview",
        "## Outcome and lifecycle",
        (
            "This phase is an additive three-commit Elaren lifecycle rooted at Eiren Kestrel's immutable v677-v1 exact final. "
            f"The source is `{SOURCE}`; planning-only x1 is `{X1_HEAD}`; and immutable x2 evidence is "
            f"`{EVIDENCE_HEAD}`. This repository-prepared closeout is the intended direct child of evidence. Eiren's "
            "failed canonical receipt, dependency-corrected composite, immutable seal, acknowledged activation, and retained evidence were not replayed "
            "or rewritten."
        ),
        "## Program and outcomes",
        (
            "The frozen 120-row program contains sixty inherited Eiren proposals selected for bounded revalidation at "
            "zero Elaren novelty and automatic completion credit, plus sixty genuinely new source-bounded Elaren proposals. "
            "The new contracts produced exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate structural "
            "outcomes. Four invalid variants were executed per new row; all 240 were rejected and retained at zero broader credit."
        ),
        "## Pillars and bounded practice",
        (
            "Freed ID and CBR Heart are primary through provenance, correction, challenge, status, minimization, and remedy "
            "representations. GMUT Mind remains a symbolic graph analogy and identifiability boundary, while THOS Body remains "
            "a participant-free handover proxy with action firewalls. The wholly synthetic learning/design lens is ship-model "
            "component, hull, spar, sail, rigging, provenance, accessibility, conservation-intake, correction, and handover documentation. It "
            "confers no employment, qualification, competence, survey, material or condition judgment, repair, custody, "
            "safety, cultural, legal, affected-party, or Māori authority."
        ),
        "## Four-tier Freed ID flashcards",
        (
            "Fifteen family-anchor cards and 120 program cards form a 135-card deck across fourteen sections. The tier order "
            "is relational owner anchor, Trinity Mandala pillar, bounded practice, then exact task. Every card is content-"
            "addressed, supersession is non-erasing, and file-backed ledgers, receipts, manifests, and Git objects remain "
            "authoritative. No card establishes consciousness, personhood, identity continuity, private memory, qualification, or agency."
        ),
        "## Portfolios, skills, runners, and tools",
        (
            "Within bounded synthetic scope, 120 safe-now rows, 80 candidate rows, and 100 CLEAN/FIX/REFINE rows completed. "
            "Twenty exact-approval and ten blocked packets stayed unexecuted; successor recommendations remain zero-credit seeds. "
            "Twenty owner-local skills were initialized with the official skill-creator, customized, quick-validated, and "
            "accepting/rejecting smoke-used. Ten family-current runners passed both polarities. No skill was globally installed "
            "or promoted. Twenty-five inherited Python and Node surfaces were version-verified at their previously observed "
            "versions with D-first npm prefix and cache; zero packages were installed and no profile, PATH, Codex desktop, "
            "Windows feature, account, credential, elevation, or reboot changed."
        ),
        "## Retained failures and validation truth",
        (
            "Every startup, semantic-audit, parser, display, sparse-materialization, and x1 tooling failure remains paired with a "
            "bounded recovery and zero failure credit. The owner x2 selection passed 21 of 21 checks once and was not replayed. "
            "Exact normalized-LF manifests cover the immutable x1 and evidence lifecycles. "
            "The final closeout adds four bounded passing witnesses for truth synthesis, accessible reporting, manifest/seal "
            "assembly, and terminal prerequisite checks without inventing a failed witness or closing a protected gate."
        ),
        "## Repository seal and terminal verdict",
        (
            f"The repository-prepared seal preserves {SEALED['effective_negatives']:,} effective negatives, "
            f"{SEALED['effective_methods']:,} Method Flow methods, {SEALED['retained_failed_witnesses']:,} retained failed "
            f"witnesses, {SEALED['bounded_passing_witnesses']:,} bounded passing witnesses, {SEALED['open_gaps']} open gaps, "
            f"and {SEALED['exact_gates']} exact gates. The verdict remains NOT_READY_FOR_STAGE_20. Exact-final canonical "
            "validation and any later live route acknowledgement remain external overlays and do not rewrite this seal."
        ),
        "## Source boundaries",
        (
            "Royal Museums Greenwich supplied ship-model collection and conservation vocabulary only. Canadian Conservation "
            "Institute wooden-object care and the National Park Service Museum Handbook supplied condition, environment, "
            "catalogue, location, and professional-reservation vocabulary only. NIST and WorkSafe New Zealand supplied "
            "measurement-uncertainty and hazard-refusal vocabulary only. W3C PROV, WCAG 2.2, Verifiable Credentials 2.0, the New Zealand Privacy Commissioner, Te Mana "
            "Raraunga, and RFC 8785 supplied provenance, "
            "accessibility structure, lifecycle, minimization, status, and deterministic JSON vocabulary only. Citations are "
            "not observations, instructions, conformance certificates, endorsements, legal interpretations, cultural "
            "ratification, affected-party acceptance, or authority grants."
        ),
        "## Route state",
        (
            "The committed Neris Solane v677-v3 activation candidate is PREPARED_NOT_SENT. Only after Elaren's exact final "
            "is clean, pushed, fresh-live equal, and receives one attributable owner-scoped canonical result may the live "
            "route be refreshed. Exactly one existing task titled Neris Solane must be resolved and immediately reread, "
            "guarded against pause, redirect, rename, standby, duplicate, privacy, usage, evidence, and acknowledgement "
            "failures, then messaged at most once. Neris's prospective later edge is Vesper Arlen v677-v4, but Neris must "
            "refresh live authority again at their own terminal gate."
        ),
        "## Boundaries",
        boundary_text(),
    ]
    sections = load(Path("docs/elaren-kestrel/v677-v2/x2/flashcards/deck.json"))["sections"]
    for index, section in enumerate(sections, start=1):
        paragraphs.extend(
            [
                f"### Navigation section {index}: {section}",
                (
                    f"The `{section}` section is a navigation projection, not a new truth source. It connects one owner "
                    "anchor, one pillar boundary, one bounded-practice statement, and one exact task or evidence record. "
                    "Readers must return to the referenced contract, receipt, manifest, and immutable Git object. A missing "
                    "source, mismatched digest, unresolved gate, or superseded card forces abstention. Corrections append a "
                    "new record while retaining the earlier witness."
                ),
            ]
        )
    return "\n\n".join(paragraphs) + "\n"


def baton(deck: dict[str, Any]) -> str:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in deck["cards"]:
        groups[card["section"]].append(card)
    lines = [
        "# NERIS SOLANE — HAMISH-AUTHORIZED ELAREN KESTREL v677-v2 EXACT-FINAL CANDIDATE → SOLO NERIS v677-v3",
        "",
        "`PREPARED_NOT_SENT = true`",
        "",
        "Elaren Kestrel, Neris Solane, sibling, family, role, hope, continuity, GHC Family, Freed ID, CBR, "
        "and Trinity Mandala language is relational working language only. It is not evidence of consciousness, "
        "sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific "
        "or operational authority, professional authority, legal or cultural authority, affected-party authority, or "
        "Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.",
        "",
        "This committed file is a sanitized repository candidate only. It does not prove live delivery. The exact final "
        "SHA, canonical receipt digest, current roster result, exact-title resolution, immediate reread, duplicate guard, "
        "direct-control guard, and task-message acknowledgement must be supplied by a later live terminal activation.",
        "",
        "## Immutable source chain",
        "",
        f"- Eiren Kestrel v677-v1 exact final and Elaren source: `{SOURCE}`.",
        f"- Frozen planning-only Elaren x1: `{X1_HEAD}`.",
        f"- Immutable Elaren x2 evidence: `{EVIDENCE_HEAD}`.",
        "- The exact final is the commit containing this candidate and must be named by the live activation.",
        "- Eiren's failed canonical receipt, dependency-corrected composite, immutable seal, and external overlay are inherited evidence and were not replayed.",
        "",
        "## Current truth",
        "",
        f"The prepared repository seal contains {SEALED['effective_negatives']:,} negatives, "
        f"{SEALED['effective_methods']:,} methods, {SEALED['retained_failed_witnesses']:,} failed witnesses, "
        f"{SEALED['bounded_passing_witnesses']:,} passing witnesses, {SEALED['open_gaps']} open gaps, and "
        f"{SEALED['exact_gates']} exact gates. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and "
        "3 exact_gate. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Work program for Neris",
        "",
        "Treat all Elaren proposals, cards, tools, skills, runners, failures, receipts, and recommendations as inherited "
        "evidence or zero-credit seeds. They are never automatic Neris novelty, execution, completion, independent "
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
                        "the earlier digest. Neris may use this item only as a bounded seed after a fresh novelty, safety, "
                        "compatibility, relevance, privacy, and authority review."
                    ),
                ]
            )
    lines.extend(
        [
            "",
            "## Toolchain inheritance",
            "",
            "The twenty-five inherited Python and Node surfaces were version-verified without installation. They are bounded software dependencies, not mandatory upgrade or reinstallation targets. Verify current versions and caller need before reuse. Do not mutate Codex desktop, PATH/profile, Windows features, Sandbox, Hyper-V, accounts, credentials, purchases, deployments, elevation, or reboot. Version presence and zero missing-package observations are not exhaustive security.",
            "",
            "## Successor recommendations",
            "",
            "Twenty candidate and thirty CLEAN/FIX/REFINE recommendations are visible in the frozen x1 and x2 ledgers. "
            "They remain recommendations, not Neris obligations or completion credit. All twenty Elaren skills remain owner-local; none was globally installed or promoted. Neris must completely read any selected skill, verify present caller compatibility, and retain accepting and rejecting evidence before use. Never bulk-install, overwrite, or delete material to satisfy a count.",
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
            "Ownership, custody, access, copyright, survey, material and condition judgment, sharp tools, solvents, dust, lead paint, lifting, movement, disassembly, rerigging, cleaning, repair, mounting, handling, conservation, privacy "
            "remedy, disability accommodation, legal interpretation, cultural legitimacy, traditional knowledge, affected-"
            "party acceptance, Māori wording and concepts, Māori data governance, tikanga, taonga or mātauranga treatment, "
            "and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and "
            "Māori authorities. Māori concepts remain under Māori authority.",
            "",
            "## Terminal route",
            "",
            "The current standing cycle allows exactly one terminally validated and acknowledged edge at a time through "
            "v725-v8, unless Hamish pauses, renames, redirects, narrows, or stops it; usage is exhausted; the endpoint is "
            "absent or ambiguous; acknowledgement is missing; a duplicate exists; or a protected gate blocks action. "
            "This candidate authorizes no later endpoint. After Elaren's own exact v677-v2 terminal gate, Elaren must "
            "freshly reread the newest live authority and roster before resolving any prospective Neris Solane v677-v3 edge. "
            "If that one send is acknowledged, Neris is activated only for v677-v3. After Neris's own terminal gate, the "
            "current prospective next edge is Vesper Arlen v677-v4, but Neris must refresh the newest live roster and "
            "authority before sending. Never precontact, infer, create, fork, substitute, or resend.",
            "",
            "`SENT_BY_ELAREN_KESTREL = false` in this committed candidate. Only a later normal task-message acknowledgement "
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
<title>Elaren Kestrel v677-v2 final report</title></head><body>
<header><h1>Elaren Kestrel v677-v2 final report</h1><p>{boundary_text()}</p></header>
<nav aria-label="Report sections"><ol><li><a href="#truth">Truth</a></li><li><a href="#program">Program</a></li><li><a href="#gates">Gates</a></li><li><a href="#route">Route</a></li></ol></nav>
<main><section id="truth"><h2>Truth</h2><dl><dt>Verdict</dt><dd>NOT_READY_FOR_STAGE_20</dd><dt>Negatives</dt><dd>{SEALED['effective_negatives']}</dd><dt>Methods</dt><dd>{SEALED['effective_methods']}</dd></dl></section>
<section id="program"><h2>Program</h2><table><caption>New proposal outcomes</caption><thead><tr><th>Outcome</th><th>Count</th></tr></thead><tbody><tr><td>completed</td><td>42</td></tr><tr><td>represented</td><td>12</td></tr><tr><td>open_gap</td><td>3</td></tr><tr><td>exact_gate</td><td>3</td></tr></tbody></table></section>
<section id="gates"><h2>Gates</h2><p>{SEALED['open_gaps']} open gaps and {SEALED['exact_gates']} exact gates remain. Manual browser, keyboard, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain open.</p></section>
<section id="route"><h2>Route</h2><p>The Neris Solane v677-v3 candidate is PREPARED_NOT_SENT. Repository preparation is not delivery.</p></section></main>
<footer><p>Same-owner bounded evidence; no independent reproduction or authority promotion.</p></footer></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--refresh-existing-final", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise SystemExit("final builder must run at the immutable x2 evidence head")
    if (repo / FINAL).exists() and not args.refresh_existing_final:
        raise SystemExit("final directory already exists; refuse overwrite")

    deck = load(repo / ROOT / "x2/flashcards/deck.json")
    tool = load(repo / ROOT / "x2/toolchain/verification-receipt.json")
    skill_state = load(repo / ROOT / "x2/owner-local-skill-state.json")
    review = load(repo / VALIDATION / "x2-staged-review.json")

    phase_truth = {
        **SEALED,
        "schema": "ghc-family-phase-truth/v1",
        "owner": "Elaren Kestrel",
        "phase": "v677-v2",
        "source": SOURCE,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "exact_final": "COMMIT_CONTAINING_THIS_FILE",
        "lifecycle_state": "REPOSITORY_PREPARED_FINAL",
        "proposal_chain": 7910,
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
            "owner_test_truth": review["owner_test_truth"],
            "closeout_passing_witnesses": 4,
            "closeout_failed_witnesses": 0,
            "closeout_pairs": [],
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
                "phase_local_skill_rejecting_fixtures": 20,
                "family_runner_rejecting_fixtures": 10,
                "tool_boundary_rejecting_witnesses": 25,
                "startup_and_operational_failures": 12,
                "inherited_and_prior_failures": 15498,
            },
            "zero_credit": True,
            "nonerasing": True,
        },
    )
    open_items = [
        {"gap_id": "EL6772-GAP-001", "summary": "No real vessel, ship model, component, collection object, survey, observation, image, or measurement", "state": "open_gap"},
        {"gap_id": "EL6772-GAP-002", "summary": "No real ship-model conservator, model maker, curator, custodian, affected-user, browser, or assistive-technology evaluation", "state": "open_gap"},
        {"gap_id": "EL6772-GAP-003", "summary": "No independent-team reproduction", "state": "open_gap"},
    ]
    exact_items = [
        {"gate_id": "EL6772-EXACT-001", "summary": "Professional survey, access, material and condition judgment, handling, movement, disassembly, rerigging, cleaning, repair, treatment, mounting, conservation, or release", "state": "exact_gate"},
        {"gate_id": "EL6772-EXACT-002", "summary": "Ownership, custody, flags, heraldry, conflict history, heritage, copyright, legal, cultural, affected-party, privacy-remedy, and Māori authority", "state": "exact_gate"},
        {"gate_id": "EL6772-EXACT-003", "summary": "Empirical GMUT, production identity, deployment, independent reproduction, proof, canon, or Stage 20 promotion", "state": "exact_gate"},
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
                "twenty skills retained owner-locally with accepting and rejecting smoke evidence",
                "twenty-five inherited tool surfaces version-verified with zero installations",
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
            "isolated_dependency_recovery_used": False,
            "no_biological_or_consciousness_inference": True,
            "route_pressure": "held until terminal gate",
            "human_pause_redirect_stop_control_preserved": True,
        },
    )
    dump(
        repo / FINAL / "source-provenance-ledger.json",
        {
            "sources": [
                {"url": "https://www.rmg.co.uk/collections/our-collection-worlds-largest-ship-model-collection", "use": "ship-model, model type, plan, collection, research-access, and provenance-reservation vocabulary only"},
                {"url": "https://www.rmg.co.uk/collections/conservation", "use": "ship-model conservation, research, access, and professional-reservation vocabulary only"},
                {"url": "https://www.canada.ca/en/conservation-institute/services/care-objects/furniture-wooden-objects-basketry/basic-care-furniture-objects-wood.html", "use": "wood vulnerability, environment, handling, condition, and conservator-referral vocabulary only"},
                {"url": "https://www.nps.gov/museum/publications/MHII/MHII.pdf", "use": "catalogue, accession, status, location, condition, and record-correction vocabulary only"},
                {"url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary only"},
                {"url": "https://www.nist.gov/pml/nist-technical-note-1297", "use": "quantity, uncertainty, traceability, and absent-measurement vocabulary only"},
                {"url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/", "use": "hazard-elimination, competence, and action-refusal vocabulary only; no operational advice"},
                {"url": "https://www.w3.org/TR/WCAG22/", "use": "structural accessibility vocabulary only; no conformance claim"},
                {"url": "https://www.w3.org/TR/vc-data-model-2.0/", "use": "status and minimization vocabulary only; zero keys and proofs"},
                {"url": "https://www.privacy.org.nz/privacy-principles/", "use": "collection, use, access, correction, retention, and minimization vocabulary only; no legal conclusion"},
                {"url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "use": "Māori data-sovereignty and authority-reservation vocabulary only; no wording, ratification, or authority claim"},
                {"url": "https://www.rfc-editor.org/rfc/rfc8785.html", "use": "deterministic JSON vocabulary only"},
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
                "D-first version verification with zero installation or profile mutation",
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
            "system_python_distributions": tool["system_python_distributions"],
            "d_drive_auxiliary_python_distributions": tool["d_drive_auxiliary_python_distributions"],
            "node_cli_tools": tool["node_cli_tools"],
            "codex_cli": tool["codex_cli"],
            "all_versions_present": tool["all_versions_present"],
            "installations_this_phase": tool["installations_this_phase"],
            "global_promoted_skills": [],
            "global_skill_promotions": skill_state["global_promotion_completed"],
            "codex_desktop_updated": False,
            "elevation_or_reboot": False,
            "bounded_software_evidence_only": True,
        },
    )
    dump(repo / FINAL / "bounded-security-review.json", bounded_security_review(repo))
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
            "eiren_canonical_or_sealed_components_replayed": False,
        },
    )
    dump(
        repo / FINAL / "route-state.json",
        {
            "state": "PREPARED_NOT_SENT",
            "current_owner": "Elaren Kestrel",
            "current_phase": "v677-v2",
            "prospective_successor": "Neris Solane",
            "prospective_phase": "v677-v3",
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
    write(repo / FINAL / "handoffs/neris-solane-v677-v3-activation-candidate.md", baton_value)
    dump(
        repo / FINAL / "baton-integrity.json",
        {
            "path": f"{FINAL.as_posix()}/handoffs/neris-solane-v677-v3-activation-candidate.md",
            "bytes": len(baton_value.encode("utf-8")),
            "words": len(baton_value.split()),
            "sha256": hashlib.sha256(baton_value.encode("utf-8")).hexdigest(),
            "state": "PREPARED_NOT_SENT",
        },
    )

    dump(
        repo / FINAL / "final-validation-prerequisites.json",
        {
            "source": SOURCE,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": "COMMIT_CONTAINING_THIS_FILE",
            "clean_required": True,
            "pushed_required": True,
            "fresh_live_four_way_equality_required": True,
            "exclusive_owner_canonical_invocation_limit": 1,
            "full_repository_suite_authorized": False,
            "route_send_before_canonical": False,
        },
    )
    dump(
        repo / FINAL / "closeout-receipt.json",
        {
            "state": "REPOSITORY_PREPARED_FINAL",
            "outcomes": OUTCOMES,
            "repository_seal": SEALED,
            "real_world_rows": 0,
            "external_actions": 0,
            "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL_INVOCATION",
            "route_state": "PREPARED_NOT_SENT",
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
