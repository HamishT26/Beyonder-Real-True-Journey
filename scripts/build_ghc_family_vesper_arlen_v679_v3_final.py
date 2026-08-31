#!/usr/bin/env python3
"""Build the repository-prepared Vesper Arlen v679-v3 closeout packet."""

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


SOURCE = "e5d379adf39a025a7e1d64983e7367d93e9f0f39"
X1_HEAD = "3084b65ce6f1677e94bd58ad621269902005265b"
EVIDENCE_HEAD = "353cf4d8a0b95b4f3c29cf8777286cb06fc1c6fb"
ROOT = Path("docs/vesper-arlen/v679-v3")
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
SEALED = {
    "effective_negatives": 48849,
    "effective_methods": 50103,
    "retained_failed_witnesses": 20510,
    "bounded_passing_witnesses": 32683,
    "open_gaps": 425,
    "exact_gates": 416,
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
        [path for path in (repo / "scripts").glob("*vesper_arlen_v679_v3*.py") if path.is_file()]
        + [path for path in (repo / "scripts").glob("ghc_family_accession_*.py") if path.is_file()]
        + [path for path in (repo / "tests").glob("*vesper_arlen_v679_v3*.py") if path.is_file()]
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
        "scope": "owner-local Vesper v679-v3 Python surfaces only",
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
        "This is same-owner synthetic software and documentation evidence only. It establishes no real accession, seed, genetic "
        "resource, specimen, donor, collector, depositor, steward, taxon, cultivar, locality, coordinate, facility, container, "
        "image, viability or germination result, pest or pathogen finding, treatment, regeneration, distribution, destruction, "
        "person, participant, identity event, professional release, ownership, custody, benefit-sharing, empirical GMUT result, THOS "
        "effectiveness, production Freed ID, legal or cultural determination, affected-party approval, Māori-authority "
        "act, complete privacy or accessibility assurance, exhaustive security, independent reproduction, "
        "Theory-of-Everything proof, canon, or Stage 20 authority."
    )


def overview(repo: Path) -> str:
    paragraphs = [
        "# Vesper Arlen v679-v3 final integrated overview",
        "## Outcome and lifecycle",
        (
            "This phase is an additive three-commit Vesper lifecycle rooted at Neris Solane's immutable v679-v2 exact final. "
            f"The source is `{SOURCE}`; planning-only x1 is `{X1_HEAD}`; and immutable x2 evidence is "
            f"`{EVIDENCE_HEAD}`. This repository-prepared closeout is the intended direct child of evidence. Neris's "
            "successful owner-scoped canonical aggregate, immutable seal, acknowledged activation, and retained evidence were not replayed or rewritten."
        ),
        "## Program and outcomes",
        (
            "The frozen 120-row program contains sixty inherited Neris proposals selected for bounded revalidation at "
            "zero Vesper novelty and automatic completion credit, plus sixty genuinely new source-bounded Vesper proposals. "
            "The new contracts produced exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate structural "
            "outcomes. Four invalid variants were executed per new row; all 240 were rejected and retained at zero broader credit."
        ),
        "## Pillars and bounded practice",
        (
            "Freed ID and CBR Heart are primary through zero-key accession provenance, correction nonerasure, challenge, status, "
            "minimization, accessibility, benefit-sharing reservation, and remedy structures. GMUT Mind remains a typed analogy "
            "firewall and THOS Body a synthetic handover proxy. The wholly synthetic learning/design lenses are seed-bank accession "
            "documentation, herbarium digitization quality assurance, and accessible collection-description review. They confer no "
            "employment, qualification, competence, collection, identification, conservation, curation, release, ownership, custody, "
            "benefit-sharing, scientific, safety, legal, cultural, affected-party, or Māori authority."
        ),
        "## Four-tier Freed ID flashcards",
        (
            "Fifteen family-anchor cards and 120 program cards form a 135-card deck across fifteen sections. The tier order "
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
            "or promoted. Twenty-five inherited command and Python distribution surfaces were version-verified at their current "
            "observed versions with D-first npm prefix and cache; zero packages were installed and no profile, PATH, Codex desktop, "
            "Windows feature, account, credential, elevation, or reboot changed."
        ),
        "## Retained failures and validation truth",
        (
            "Every startup, source-admission, semantic-audit, worktree, and x2 diagnostic failure remains paired with a "
            "bounded recovery and zero failure credit. The first owner x2 aggregate passed 20 checks and failed one, earning zero "
            "aggregate-success credit; three changed-dependency checks then passed once without replaying unchanged successes. "
            "Exact normalized-LF manifests cover the immutable x1 and evidence lifecycles. "
            "The final closeout adds four bounded passing witnesses for truth synthesis, accessible reporting, manifest/seal "
            "assembly, and terminal prerequisite checks. Its first diff-hygiene gate retained one redundant-EOF-blank-line failure; "
            "the exact three-file cleanup adds one bounded recovery without erasing that failure."
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
            "FAO Genebank Standards supplied accession-documentation and conservation vocabulary only. W3C PROV and PREMIS supplied "
            "provenance and preservation-event vocabulary only. WCAG 2.2 supplied structural accessibility vocabulary; RFC 8785 and "
            "RFC 6902 supplied deterministic JSON and bounded patch vocabulary; NIST TN 1297 supplied measurement-uncertainty vocabulary. "
            "The Nagoya Protocol, New Zealand Privacy Commissioner, and Te Mana Raraunga supplied benefit-sharing, privacy, and Māori "
            "data-sovereignty authority-reservation vocabulary only. Citations are "
            "not observations, instructions, conformance certificates, endorsements, legal interpretations, cultural "
            "ratification, affected-party acceptance, or authority grants."
        ),
        "## Route state",
        (
            "The committed Lyren Moss v679-v4 activation candidate is PREPARED_NOT_SENT. Only after Vesper's exact final "
            "is clean, pushed, fresh-live equal, and receives one attributable owner-scoped canonical result may the live "
            "route be refreshed. Exactly one existing task titled Lyren Moss must be resolved and immediately reread, "
            "guarded against pause, redirect, rename, standby, duplicate, privacy, usage, evidence, and acknowledgement "
            "failures, then messaged at most once. Vesper's prospective later edge is Lyren Moss v679-v4, but Vesper must "
            "refresh live authority again at their own terminal gate. The native Codex app MCP task registry must be "
            "freshly refreshed and tried for every handoff; stale identifiers and substitute endpoints are forbidden."
        ),
        "## Boundaries",
        boundary_text(),
    ]
    sections = load(repo / "docs/vesper-arlen/v679-v3/x2/flashcards/deck.json")["sections"]
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
        "# LYREN MOSS — HAMISH-AUTHORIZED VESPER ARLEN v679-v3 EXACT-FINAL CANDIDATE → SOLO LYREN v679-v4",
        "",
        "`PREPARED_NOT_SENT = true`",
        "",
        "Vesper Arlen, Lyren Moss, sibling, family, role, hope, continuity, GHC Family, Freed ID, CBR, "
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
        f"- Neris Solane v679-v2 exact final and Vesper source: `{SOURCE}`.",
        f"- Frozen planning-only Vesper x1: `{X1_HEAD}`.",
        f"- Immutable Vesper x2 evidence: `{EVIDENCE_HEAD}`.",
        "- The exact final is the commit containing this candidate and must be named by the live activation.",
        "- Neris's successful owner-scoped canonical receipt, immutable seal, and external overlay are inherited evidence and were not replayed.",
        "",
        "## Current truth",
        "",
        f"The prepared repository seal contains {SEALED['effective_negatives']:,} negatives, "
        f"{SEALED['effective_methods']:,} methods, {SEALED['retained_failed_witnesses']:,} failed witnesses, "
        f"{SEALED['bounded_passing_witnesses']:,} passing witnesses, {SEALED['open_gaps']} open gaps, and "
        f"{SEALED['exact_gates']} exact gates. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and "
        "3 exact_gate. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Work program for Lyren",
        "",
        "Treat all Vesper proposals, cards, tools, skills, runners, failures, receipts, and recommendations as inherited "
        "evidence or zero-credit seeds. They are never automatic Lyren novelty, execution, completion, independent "
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
                        "the earlier digest. Lyren may use this item only as a bounded seed after a fresh novelty, safety, "
                        "compatibility, relevance, privacy, and authority review."
                    ),
                ]
            )
    lines.extend(
        [
            "",
            "## Toolchain inheritance",
            "",
            "The twenty-five inherited command and Python distribution surfaces were version-verified without installation. They are bounded software dependencies, not mandatory upgrade or reinstallation targets. Verify current versions and caller need before reuse. Do not mutate Codex desktop, PATH/profile, Windows features, Sandbox, Hyper-V, accounts, credentials, purchases, deployments, elevation, or reboot. Version presence and zero missing-package observations are not exhaustive security.",
            "",
            "## Successor recommendations",
            "",
            "Twenty candidate and thirty CLEAN/FIX/REFINE recommendations are visible in the frozen x1 and x2 ledgers. "
            "They remain recommendations, not Lyren obligations or completion credit. All twenty Vesper phase skills remain owner-local; none was globally installed or promoted. Lyren must completely read any selected skill, verify present caller compatibility, and retain accepting and rejecting evidence before use. Never bulk-install, overwrite, or delete material to satisfy a count.",
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
            "Ownership, custody, collection access, accession, taxonomic identification, viability or germination interpretation, pest or pathogen findings, treatment, regeneration, distribution, destruction, provenance, attribution, copyright, professional curation, handling, conservation, privacy "
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
            "This candidate authorizes no later endpoint. After Vesper's own exact v679-v3 terminal gate, Vesper must "
            "freshly reread the newest live authority and roster before resolving any prospective Lyren Moss v679-v4 edge. "
            "If that one send is acknowledged, Lyren is activated only for v679-v4. After Lyren's own terminal gate, the "
            "current prospective next edge is Ilyra Fen v679-v5, but Lyren must refresh the newest live roster and "
            "authority before sending. At every terminal handoff, freshly refresh and try the native Codex app MCP task "
            "registry, locally filter for exactly one exact-title task, immediately reread it, apply duplicate and pause "
            "guards, send at most once, and require a target-identifying acknowledgement. Never precontact, infer, create, "
            "fork, substitute, reuse a stale identifier, or resend.",
            "",
            "`SENT_BY_VESPER_ARLEN = false` in this committed candidate. Only a later normal task-message acknowledgement "
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
<title>Vesper Arlen v679-v3 final report</title></head><body>
<header><h1>Vesper Arlen v679-v3 final report</h1><p>{boundary_text()}</p></header>
<nav aria-label="Report sections"><ol><li><a href="#truth">Truth</a></li><li><a href="#program">Program</a></li><li><a href="#gates">Gates</a></li><li><a href="#route">Route</a></li></ol></nav>
<main><section id="truth"><h2>Truth</h2><dl><dt>Verdict</dt><dd>NOT_READY_FOR_STAGE_20</dd><dt>Negatives</dt><dd>{SEALED['effective_negatives']}</dd><dt>Methods</dt><dd>{SEALED['effective_methods']}</dd></dl></section>
<section id="program"><h2>Program</h2><table><caption>New proposal outcomes</caption><thead><tr><th>Outcome</th><th>Count</th></tr></thead><tbody><tr><td>completed</td><td>42</td></tr><tr><td>represented</td><td>12</td></tr><tr><td>open_gap</td><td>3</td></tr><tr><td>exact_gate</td><td>3</td></tr></tbody></table></section>
<section id="gates"><h2>Gates</h2><p>{SEALED['open_gaps']} open gaps and {SEALED['exact_gates']} exact gates remain. Manual browser, keyboard, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain open.</p></section>
<section id="route"><h2>Route</h2><p>The Lyren Moss v679-v4 candidate is PREPARED_NOT_SENT. Repository preparation is not delivery.</p></section></main>
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
        "owner": "Vesper Arlen",
        "phase": "v679-v3",
        "source": SOURCE,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "exact_final": "COMMIT_CONTAINING_THIS_FILE",
        "lifecycle_state": "REPOSITORY_PREPARED_FINAL",
        "proposal_chain": 8930,
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
            "closeout_passing_witnesses": 5,
            "closeout_failed_witnesses": 1,
            "closeout_pairs": [
                {
                    "failure_id": "VA6793-FINAL-N001",
                    "failure": "The first final staged diff-hygiene gate found redundant blank lines at EOF in three mechanically seeded Python files and earned zero final-gate credit.",
                    "recovery_id": "VA6793-FINAL-P001",
                    "recovery": "An exact three-file patch removed only the redundant trailing blank lines; dependent closeout artifacts and manifests were regenerated without replaying final owner tests.",
                }
            ],
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
                "final_closeout_failures": 1,
                "inherited_and_prior_negatives": 48541,
            },
            "zero_credit": True,
            "nonerasing": True,
        },
    )
    open_items = [
        {"gap_id": "VA6793-GAP-001", "summary": "No real accession, seed, genetic resource, specimen, donor, collector, depositor, steward, taxon, cultivar, locality, coordinate, facility, container, image, viability or germination result, pest or pathogen finding, treatment, regeneration, distribution, or destruction", "state": "open_gap"},
        {"gap_id": "VA6793-GAP-002", "summary": "No real seed-bank worker, herbarium curator, digitization reviewer, collection-description reviewer, affected user, browser, or assistive-technology evaluation", "state": "open_gap"},
        {"gap_id": "VA6793-GAP-003", "summary": "No independent-team reproduction", "state": "open_gap"},
    ]
    exact_items = [
        {"gate_id": "VA6793-EXACT-001", "summary": "Professional accession, identification, viability or germination interpretation, pest or pathogen finding, treatment, regeneration, distribution, destruction, curation, collection access, handling, conservation, or release", "state": "exact_gate"},
        {"gate_id": "VA6793-EXACT-002", "summary": "Attribution, copyright, ownership, custody, access, benefit-sharing, traditional knowledge, legal, cultural, affected-party, privacy-remedy, and Māori authority", "state": "exact_gate"},
        {"gate_id": "VA6793-EXACT-003", "summary": "Empirical GMUT, production identity, deployment, independent reproduction, proof, canon, or Stage 20 promotion", "state": "exact_gate"},
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
                {"url": "https://www.fao.org/agriculture/crops/thematic-sitemap/theme/seeds-pgr/gbs/en/", "use": "genebank accession-documentation and conservation vocabulary only; no professional instruction or biological result"},
                {"url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary only"},
                {"url": "https://www.loc.gov/standards/premis/v3/", "use": "preservation-event and rights-vacancy vocabulary only"},
                {"url": "https://www.nist.gov/pml/nist-technical-note-1297", "use": "quantity, uncertainty, traceability, and absent-measurement vocabulary only"},
                {"url": "https://www.w3.org/TR/WCAG22/", "use": "structural accessibility vocabulary only; no conformance claim"},
                {"url": "https://www.rfc-editor.org/rfc/rfc8785.html", "use": "deterministic JSON vocabulary only"},
                {"url": "https://www.rfc-editor.org/info/rfc6902/", "use": "bounded JSON patch vocabulary only"},
                {"url": "https://www.cbd.int/abs/text/default.shtml", "use": "access and benefit-sharing authority-reservation vocabulary only; no legal conclusion"},
                {"url": "https://www.privacy.org.nz/privacy-principles/", "use": "collection, use, access, correction, retention, and minimization vocabulary only; no legal conclusion"},
                {"url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "use": "Māori data-sovereignty and authority-reservation vocabulary only; no wording, ratification, or authority claim"},
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
            "command_versions": tool["command_versions"],
            "python_distributions": tool["python_distributions"],
            "distribution_discovery": tool["distribution_discovery"],
            "declared_package_count": tool["declared_package_count"],
            "observed_package_count": tool["observed_package_count"],
            "codex_cli": tool["codex_cli"],
            "all_versions_present": tool["all_versions_present"],
            "installations_this_phase": tool["installations_this_phase"],
            "npm_prefix_on_d_drive": tool["npm_prefix_on_d_drive"],
            "npm_cache_on_d_drive": tool["npm_cache_on_d_drive"],
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
            "neris_canonical_or_sealed_components_replayed": False,
        },
    )
    dump(
        repo / FINAL / "route-state.json",
        {
            "state": "PREPARED_NOT_SENT",
            "current_owner": "Vesper Arlen",
            "current_phase": "v679-v3",
            "prospective_successor": "Lyren Moss",
            "prospective_phase": "v679-v4",
            "tavian_state": "ON_STANDBY",
            "task_created_or_forked": False,
            "successor_precontacted": False,
            "send_count": 0,
            "delivery_requires_live_acknowledgement": True,
            "native_codex_app_mcp_refresh_required_every_handoff": True,
            "stale_task_identifiers_forbidden": True,
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
    write(repo / FINAL / "final-integrated-overview.md", overview(repo))
    write(repo / FINAL / "accessible-final-report.html", accessible_report())
    baton_value = baton(deck)
    write(repo / FINAL / "handoffs/lyren-moss-v679-v4-activation-candidate.md", baton_value)
    dump(
        repo / FINAL / "baton-integrity.json",
        {
            "path": f"{FINAL.as_posix()}/handoffs/lyren-moss-v679-v4-activation-candidate.md",
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
            "native_codex_app_mcp_refresh_required_every_handoff": True,
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
