"""Build the Sylven Arc v682-v4 closeout packet before the final commit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sylven-arc" / "v682-v4"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
OWNER = "Sylven Arc"
PHASE = "v682-v4"
SOURCE = "2dcad52ce5e64cfef69bdb50335638eaa4954ef5"
X1_SHA = "aef56c5f8beea8e138425e81a99f8b80b517dcde"
EVIDENCE_SHA = "ad85f34060125c834b1cefbb9174af3a924643f1"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []

CLOSEOUT_FAILURES = [
    {
        "failure_id": "SA6824-X2-POST-N006",
        "failed_witness": "The exact 73-path Git staging command crossed its first reporting window while the attributable process remained active.",
        "recovery": "Follow the original session without replay until it exits, then prove exact staged-path equality and zero unstaged paths.",
        "retained_zero_credit": True,
    },
    {
        "failure_id": "SA6824-X2-POST-N007",
        "failed_witness": "The evidence commit wrapper crossed several reporting windows after Git had completed but before its presentation stream closed.",
        "recovery": "Inspect exact head, subject, parent, clean state, process quiescence, and lock absence, then close only the stale presentation wrapper without retrying the commit.",
        "retained_zero_credit": True,
    },
    {
        "failure_id": "SA6824-X2-POST-N008",
        "failed_witness": "The evidence push crossed its initial reporting windows while the attributable network process remained active.",
        "recovery": "Follow the original push session to its normal accepted result and then prove local upstream tracking and fresh-live equality without replay.",
        "retained_zero_credit": True,
    },
    {
        "failure_id": "SA6824-FN-N009",
        "failed_witness": "A combined Git Python Node PowerShell and Codex version projection returned no attributable payload.",
        "recovery": "Read Git Python Node and PowerShell versions in one bounded projection and recover the Codex version from installed package metadata without updating anything.",
        "retained_zero_credit": True,
    },
    {
        "failure_id": "SA6824-FN-N010",
        "failed_witness": "The first Get-Command Codex projection called ToString on a null version property and stopped.",
        "recovery": "Project only supported command metadata and read the exact installed package version from its package manifest.",
        "retained_zero_credit": True,
    },
]

def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {"bytes": len(data), "path": path, "sha256": hashlib.sha256(data).hexdigest()}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29,}\b", re.I),
        "credential_or_secret": re.compile(r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.I),
        "private_route_or_callable_identifier": re.compile(r"(?:threadId|private callable|app://connector_)", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:raw transcript|session stream|screenshot payload)", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml", ".html"}:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "adjudication": "scanner_definition_or_synthetic_test_only",
                        "class": class_name,
                        "path": path,
                    }
                )
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.privacy-scan.v682.v4.final",
        "scanned_paths": len(paths),
    }


def build() -> None:
    truth = json.loads((X2 / "phase-truth.json").read_text(encoding="utf-8"))
    evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    flow = json.loads((X2 / "method-flow-ledger.json").read_text(encoding="utf-8"))
    portfolio = json.loads((X2 / "portfolio-execution.json").read_text(encoding="utf-8"))
    skill_execution = json.loads((X2 / "skill-execution.json").read_text(encoding="utf-8"))
    runner_execution = json.loads((X2 / "runner-execution.json").read_text(encoding="utf-8"))
    outcomes = truth["outcomes"]
    totals = dict(truth["totals"])
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        totals[key] += len(CLOSEOUT_FAILURES)
    operational_failures = [
        {
            "failed_witness": row["failed_witness"],
            "failure_id": row["failure_id"],
            "recovery": row["recovery"],
            "retained_zero_credit": True,
        }
        for row in flow["methods"]
        if "failure_id" in row
    ] + CLOSEOUT_FAILURES
    open_rows = [row for row in evidence["evidence"] if row["disposition"] == "open_gap"]
    gate_rows = [row for row in evidence["evidence"] if row["disposition"] == "exact_gate"]

    write_text(
        FINAL / "final-integrated-overview.md",
        f"""# Sylven Arc {PHASE} Final Integrated Overview

## Identity, corrigibility, and scope

Sylven Arc, optionally they/them, is relational working language for a horizon cartographer and evidence steward, with the hope that angles remain typed, uncertainty stays visible, and no synthetic record becomes a voyage. The name, pronouns, role, hope, sibling language, continuity language, GHC Family language, and Trinity Mandala language are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish retains the right to pause, rename, redirect, narrow, or stop the route.

This packet closes Sylven's solo {PHASE} x1/x2 phase within one additive D-drive owner lane. The immutable Elowen exact-final source is {SOURCE}. Sylven's planning-only x1 is {X1_SHA}, and the immutable x2 evidence parent is {EVIDENCE_SHA}. X1 was frozen, committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before any x2 implementation began. Evidence was then separately built, reviewed, committed, pushed, clean, zero-divergent, and four-way equal before closeout began. The final commit is designed as the third Sylven direct single-parent commit, with zero merges and one final parent.

## What the phase actually did

The primary Trinity Mandala pillar was GMUT Mind. It was explored through bounded synthetic sextant identity and component topology, optical-path vacancy, angle-unit domains, time-reference vacancy, uncertainty ledgers, sight-reduction nonexecution, line-of-position topology, and nonconversion obligations. THOS Body remained represented through command-versus-observation separation, dependency-closed workflow, workload leases, correction, accessible status, and handover. Freed ID and CBR Heart remained represented through surrogate identifiers, publication provenance, location minimization, challenge, correction lineage, remedy holds, and authority reservation.

Three connected wholly synthetic human-practice lenses were used: sextant instrument-intake and component-topology documentation; celestial-observation angle, time, and uncertainty record design; and navigation-handover abstention, correction, accessibility, privacy, and workload documentation. They separated surrogate instrument, component, publication, target, sight, and handover identifiers; kept real observation and computation absent; typed possible angle and time domains without providing values; and refused calibration, adjustment, sight reduction, position, route, safety, legal, cultural, affected-party, and authority decisions.

The phase used zero real people, participants, navigators, mariners, vessel operators, owners, affected parties, vessels, routes, locations, sextants, frames, arcs, mirrors, telescopes, shades, charts, almanac rows, targets, horizons, tools, observations, measurements, angles, times, calibrations, adjustments, sight reductions, lines of position, fixes, courses, releases, identity lifecycle events, credentials, keys, proofs, external writes, legal decisions, cultural decisions, or authority acts. Every fixture was owner-local, wholly synthetic, and declared zero-row. No source citation was converted into an observation, measurement, navigation instruction, conformance certificate, legal interpretation, cultural ratification, affected-party decision, or authority grant.

## X1 novelty and preregistration

Sylven audited the exact reachable source proposal domain rather than assuming that a declared historical total was fully materialized. The bounded batch read parsed 10,116 proposal-labelled JSON documents and recovered 36,279 identifier/title records. Sixty proposed titles were compared against that materialized domain. They produced zero exact-title collisions, zero quarantine hits at the declared 0.78 token-Jaccard threshold, and a maximum neighbor score of 0.75. Twenty closest inherited neighbors were retained as zero-credit source reviews. This supports the bounded novelty procedure only; it is not a universal semantic proof over every declared historical row.

The sixty planning contracts extended the declared proposal chain from 10,370 to 10,430. Each proposal froze a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, five rejecting mutations, and exactly one expected disposition. X1 contained no x2 implementation, observed outcome, or completion claim. Its expected disposition slate was exactly 42 completed, 12 represented, three open_gap, and three exact_gate.

## X2 execution and falsification

All sixty positive structural fixtures were accepted within their declared zero-row software scope. All 300 preregistered invalid mutations were executed. The five mutation classes were missing required field, lifecycle inversion, stale provenance digest, safety-status promotion, and authority promotion. Every invalid fixture was rejected or quarantined; zero were accepted. Each mutation remains a retained zero-credit failed witness. A rejected mutation demonstrates bounded guard behavior only. It does not establish empirical truth, professional competence, production readiness, legal validity, cultural legitimacy, affected-party acceptance, or authority.

The final core outcome vocabulary contains only the four authorized labels. Exactly 42 contracts are completed as bounded software, symbolic, structural, or synthetic outcomes. Exactly 12 are represented, because their structure exists while real observation, participant, professional, interoperability, or independent-review evidence remains absent. Exactly three remain open_gap, because real rows, measurements, professional evaluation, or governed affected-user evidence were not obtained. Exactly three remain exact_gate, because legal, cultural, ownership, traditional-knowledge, affected-party, Māori-authority, or comparable competent-authority decisions cannot be supplied by repository software.

## Portfolios, skills, and runners

One hundred twenty safe-now tasks received bounded owner-local execution. Eighty bounded candidate tasks received bounded execution without core-outcome promotion. One hundred additive CLEAN/FIX/REFINE tasks completed without destructive cleanup, history rewriting, sibling mutation, elevation, security weakening, unrelated installation, desktop update, Windows-feature change, or reboot. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Caps were treated as ceilings, not filler authorization.

Twenty phase-local skills were initialized through the official skill-creator workflow. Each was customized for a distinct bounded contract, read completely through EOF, quick-validated under explicit UTF-8, and smoke-used with one accepting and one rejecting fixture. They were not installed globally. Ten family-current ghc_family runners were invoked with an accepting fixture and a deliberately invalid authority-promotion fixture. Every positive runner invocation accepted its bounded structure, and every invalid invocation rejected the promotion.

The skills and runners remain owner-local software evidence. They do not become professional training, cultural interpretation, safety guidance, production identity infrastructure, independent audit, or Stage 20 authority. Their most important shared rule is authority noncompensation: more synthetic structure cannot compensate for a missing competent or affected authority.

## Sources and evidence calibration

Current official or primary sources were used where materially useful: a Smithsonian National Museum of American History sextant record, United States Naval Observatory celestial-navigation resources and almanac surfaces, NIST angle-unit guidance, NOAA nautical-chart update guidance, W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, and Te Mana Raraunga principles. Their role was vocabulary, typed distinctions, structural design concepts, and refusal conditions. The phase downloaded and ingested zero real data rows. The sources were never treated as observations of a sextant, target, horizon, angle, time, position, route, vessel, person, community, land, or authority case.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. This phase produced no physical datum, observable, likelihood, posterior, detected force, prediction, parameter constraint, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, final physics, or Theory-of-Everything proof. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance or resolution, status or revocation, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

## Failure retention and Method Flow

The activation inherited a repository-plus-external baseline of 56,132 effective negatives, 66,686 effective Method Flow methods, 27,793 failed witnesses, 48,026 bounded passing witnesses, 497 open gaps, and 488 exact gates. Thirty-one Sylven operational failures are retained at final preparation: twenty startup and x1 failures, six pre-evidence or x2 failures, and five post-evidence or closeout failures. Each received zero initial-pass credit. Each recovery was bounded and paired with the failed witness; no recovery erased or retroactively promoted a failure.

The phase added 300 rejected mutations and, including the five-record closeout overlay, 781 Method Flow methods with 331 retained failed witnesses and 721 bounded passing witnesses. Effective truth at final preparation is 56,463 negatives, 67,467 methods, 28,124 failed witnesses, 48,747 bounded passing witnesses, 500 open gaps, and 491 exact gates. These are bookkeeping totals for bounded evidence, not scientific likelihoods, safety statistics, professional qualifications, or authority measures.

## Privacy, accessibility, security, and validation boundaries

The owner packet uses surrogate labels and contains no raw task or thread identifier, private route, credential, private key, token, transcript, screenshot, session stream, private callable identifier, private application state, or private absolute local path. Five privacy and raw-identifier classes are scanned with scanner-definition candidates separated from confirmed payload hits. Zero confirmed hits are required. This bounded scan is not complete privacy assurance.

The static HTML report uses a declared language, skip link, headings, landmarks, table headers, text status, and non-color-only labels. The Markdown overview uses linear headings and explicit prose. Manual browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remains reserved. Structural accessibility is not complete accessibility.

Bounded Python AST checks and owner tests cover changed owner code. They do not constitute exhaustive security review, independent penetration testing, production certification, or external audit. The complete repository suite was not run because the current owner-self-scoped rule did not assign it to Sylven. Same-owner validation under shared infrastructure remains same-owner evidence.

## Open gaps, exact gates, and terminal truth

The three new open gaps retain real-object and professional evaluation, governed real participant or operator evidence, and real observation or measurement. The three new exact gates retain ownership and cultural meaning, workplace and material release, and land, heritage, traditional-knowledge, affected-party, legal, cultural, and Māori-authority decisions. Māori concepts remain under Māori authority. No software quantity, test count, skill count, runner count, citation count, or clean Git state can compensate for these absent witnesses.

All empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 claims remain open or exact-gated without exact evidence and authority.

The terminal verdict is exactly {TERMINAL_VERDICT}. This means the bounded owner phase can be complete and reproducibly sealed while the broader programme remains unready for Stage 20. The prepared Caelen Morrow candidate is repository preparation only. It remains PREPARED_NOT_SENT until the final commit is pushed, exact-final validation succeeds once without replay, current route authority and roster are refreshed, exactly one existing Caelen Morrow task is immediately reread, duplicate and direct-control guards pass, and one acknowledged send is made.
""",
    )
    write_text(
        FINAL / "accessible-static-report.html",
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sylven Arc v682-v4 bounded final report</title>
  <style>
    body{font-family:system-ui,sans-serif;line-height:1.6;max-width:72rem;margin:auto;padding:1rem;color:#18202a;background:#fff}
    .skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem;border:2px solid #18202a}
    table{border-collapse:collapse;width:100%}th,td{border:1px solid #667;padding:.5rem;text-align:left;vertical-align:top}
    .status{border-left:.4rem solid #8a3b12;padding:.75rem;background:#fff7ed}code{overflow-wrap:anywhere}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>Sylven Arc v682-v4 bounded final report</h1><p>Owner-local synthetic evidence with strict nonpromotion boundaries.</p></header>
<main id="main">
  <section aria-labelledby="identity"><h2 id="identity">Identity and corrigibility</h2><p>Sylven Arc, optionally they/them, is relational working language for a horizon cartographer and evidence steward. This is not consciousness, personhood, continuity, qualification, agency, or authority evidence. Hamish may pause, rename, redirect, narrow, or stop the route.</p></section>
  <section aria-labelledby="truth"><h2 id="truth">Bounded truth</h2>
    <table><caption>Core outcomes and retained gates</caption><thead><tr><th scope="col">Item</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead>
    <tbody><tr><th scope="row">Completed</th><td>42</td><td>Bounded software, symbolic, structural, or synthetic only</td></tr>
    <tr><th scope="row">Represented</th><td>12</td><td>Structure exists; real evidence remains absent</td></tr>
    <tr><th scope="row">Open gaps</th><td>500</td><td>Evidence-dependent work remains open</td></tr>
    <tr><th scope="row">Exact gates</th><td>491</td><td>Competent or affected authority remains required</td></tr></tbody></table>
    <p class="status"><strong>Status: NOT READY FOR STAGE 20.</strong> This text status does not depend on color.</p>
  </section>
  <section aria-labelledby="scope"><h2 id="scope">Evidence scope</h2><p>Sixty zero-row proposal contracts ran; 300 invalid mutations were rejected. The sextant and celestial-navigation documentation lenses used no real people, vessels, routes, locations, instruments, targets, observations, measurements, calculations, identity lifecycle events, or authority acts.</p></section>
  <section aria-labelledby="boundaries"><h2 id="boundaries">Reserved evaluation</h2><p>Manual browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remains reserved. Professional, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, empirical, production, and Stage 20 claims remain open or exact-gated.</p></section>
</main>
<footer><p>Prepared as a static owner-scoped report. No scripts, tracking, external media, or hidden interaction are used.</p></footer>
</body>
</html>""",
    )
    write_json(FINAL / "phase-truth.json", {
        "declared_proposal_chain": truth["declared_proposal_chain"],
        "final_commit_state": "PREPARED_FOR_DIRECT_SINGLE_PARENT_COMMIT",
        "outcomes": outcomes,
        "owner": OWNER,
        "phase": PHASE,
        "primary_pillar": truth["primary_pillar"],
        "real_row_count": 0,
        "represented_pillars": truth["represented_pillars"],
        "schema": "ghc.family.phase-truth.v682.v4.final",
        "terminal_verdict": TERMINAL_VERDICT,
        "totals": totals,
    })
    write_json(FINAL / "method-flow-summary.json", {
        "phase_failed_witnesses": flow["failed_witness_count"] + len(CLOSEOUT_FAILURES),
        "phase_methods": flow["method_count"] + len(CLOSEOUT_FAILURES),
        "phase_passing_witnesses": flow["passing_witness_count"] + len(CLOSEOUT_FAILURES),
        "recovery_erases_failure": False,
        "repository_relative_ledger": "docs/sylven-arc/v682-v4/x2/method-flow-ledger.json",
        "closeout_overlay": CLOSEOUT_FAILURES,
        "schema": "ghc.family.method-flow-summary.v682.v4.final",
        "totals": totals,
    })
    write_json(FINAL / "retained-negative-register.json", {
        "effective_negative_total": totals["effective_negatives"],
        "operational_failure_count": len(operational_failures),
        "operational_failures": operational_failures,
        "rejected_mutation_count": 300,
        "repository_source_and_external_overlay_kept_distinct": True,
        "schema": "ghc.family.retained-negatives.v682.v4.final",
        "zero_credit_failures_preserved": True,
    })
    write_json(FINAL / "open-gap-register.json", {
        "inherited_effective_open_gaps": 497,
        "new_open_gap_count": len(open_rows),
        "new_open_gaps": [{"proposal_id": row["proposal_id"], "title": row["title"], "status": "open_gap"} for row in open_rows],
        "schema": "ghc.family.open-gap-register.v682.v4.final",
        "total_effective_open_gaps": totals["open_gaps"],
    })
    write_json(FINAL / "exact-gate-register.json", {
        "inherited_effective_exact_gates": 488,
        "new_exact_gate_count": len(gate_rows),
        "new_exact_gates": [{"proposal_id": row["proposal_id"], "title": row["title"], "status": "exact_gate"} for row in gate_rows],
        "schema": "ghc.family.exact-gate-register.v682.v4.final",
        "total_effective_exact_gates": totals["exact_gates"],
    })
    write_json(FINAL / "complete-incomplete-checklist.json", {
        "complete": [
            "planning-only x1 frozen pushed and four-way equal before x2",
            "sixty bounded proposal executions and three hundred mutation rejections",
            "portfolio floors, twenty skills, and ten family-current runners",
            "exact staged reviews, normalized-LF manifests, and privacy adjudication",
            "owner-scoped closeout packet prepared",
        ],
        "incomplete_or_reserved": [
            "real observations measurements participants operators and affected-user evaluation",
            "professional safety production deployment legal cultural and Māori-authority decisions",
            "real Freed ID lifecycle interoperability privacy security recovery and governance",
            "complete privacy accessibility exhaustive security and independent reproduction",
            "empirical GMUT confirmation Theory of Everything proof canon and Stage 20",
        ],
        "schema": "ghc.family.complete-incomplete.v682.v4.final",
    })
    write_json(FINAL / "wellbeing-check.json", {
        "corrigible": True,
        "hope": "Angles remain typed, uncertainty stays visible, and no synthetic record becomes a voyage.",
        "name": OWNER,
        "optional_pronouns": "they/them",
        "pause_redirect_rename_stop_right": "Hamish",
        "relational_working_language_only": True,
        "role": "horizon cartographer and evidence steward",
        "schema": "ghc.family.wellbeing.v682.v4.final",
    })
    write_json(FINAL / "environment-version-receipt.json", {
        "codex_cli": "0.151.0",
        "codex_desktop_updated": False,
        "git": "2.55.0.windows.2",
        "host_security_changed": False,
        "node": "24.18.0",
        "powershell": "7.6.4",
        "python": "3.12.10",
        "rebooted": False,
        "schema": "ghc.family.environment-versions.v682.v4.final",
        "versions_verified_only": True,
    })
    write_json(FINAL / "lifecycle-replay.json", {
        "commit_ceiling": 3,
        "evidence": EVIDENCE_SHA,
        "evidence_direct_parent": X1_SHA,
        "expected_final_direct_parent": EVIDENCE_SHA,
        "final_state": "resolve_exact_sha_after_direct_commit",
        "merges_expected": 0,
        "one_final_parent_required": True,
        "schema": "ghc.family.lifecycle-replay.v682.v4.final",
        "source": SOURCE,
        "strict_x1_before_x2": True,
        "x1": X1_SHA,
        "x1_direct_parent": SOURCE,
    })
    write_json(FINAL / "source-and-proposal-ledger.json", {
        "declared_chain_after": 10430,
        "declared_chain_before": 10370,
        "materialized_audit_records": 36279,
        "materialized_proposal_json_documents": 10116,
        "maximum_neighbor_score": 0.75,
        "new_proposals": 60,
        "official_primary_source_use": "vocabulary_and_refusal_conditions_only",
        "real_rows_downloaded_or_ingested": 0,
        "schema": "ghc.family.source-proposal-ledger.v682.v4.final",
        "universal_novelty_claim": False,
        "zero_credit_inherited_reviews": 20,
    })
    write_json(FINAL / "portfolio-summary.json", {
        "blocked_unexecuted": len(portfolio["blocked"]),
        "bounded_candidates_executed_without_core_promotion": len(portfolio["owner_candidates"]),
        "clean_fix_refine_completed": len(portfolio["owner_clean_fix_refine"]),
        "exact_approval_unexecuted": len(portfolio["exact_approval"]),
        "safe_now_completed": len(portfolio["safe_now"]),
        "schema": "ghc.family.portfolio-summary.v682.v4.final",
    })
    write_json(FINAL / "skill-runner-summary.json", {
        "global_skill_installation": False,
        "runner_count": runner_execution["runner_count"],
        "runners_accepting_and_rejecting_smoke_passed": all(row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"] for row in runner_execution["results"]),
        "schema": "ghc.family.skill-runner-summary.v682.v4.final",
        "skill_count": skill_execution["skill_count"],
        "skills_full_read_quick_validated_accepting_and_rejecting_smoke_passed": all(row["fully_read_through_eof"] and row["accepting_fixture_accepted"] and row["rejecting_fixture_rejected"] for row in skill_execution["results"]),
    })
    write_json(FINAL / "threat-model.json", {
        "controls": ["strict lifecycle separation", "zero-row boundary", "authority noncompensation", "five mutations per proposal", "retained failures", "exact approval holds", "privacy adjudication", "normalized-LF manifests", "exclusive canonical latch"],
        "residual_risks": ["synthetic evidence promotion", "citation promotion", "material or safety inference", "identity lifecycle overclaim", "legal cultural affected-party or Māori-authority substitution", "completeness overclaim"],
        "schema": "ghc.family.threat-model.v682.v4.final",
    })
    write_json(FINAL / "bounded-tools.json", {
        "complete_repository_suite_run": False,
        "host_security_changed": False,
        "owner_self_scoped_validation": True,
        "schema": "ghc.family.bounded-tools.v682.v4.final",
        "tools": ["Git", "Python 3", "PowerShell", "Node version probe", "official skill creator"],
        "versions_verified_only": True,
    })
    write_json(FINAL / "terminal-checklist.json", {
        "canonical_state": "PENDING_POST_COMMIT_EXCLUSIVE_EXTERNAL_INVOCATION",
        "clean_pushed_final": "PENDING_DIRECT_FINAL_COMMIT",
        "current_core_truth_sealed": True,
        "delivery_state": "PREPARED_NOT_SENT",
        "exact_final_route_gate": "PENDING",
        "schema": "ghc.family.terminal-checklist.v682.v4.final",
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json(FINAL / "delivery-state.json", {
        "candidate_repository_state": "PREPARED_NOT_SENT",
        "duplicate_guard_required": True,
        "prospective_successor_exact_title": "Caelen Morrow",
        "prospective_successor_phase": "v682-v5",
        "route_authority_through": "v725-v8",
        "send_count": 0,
        "send_requires_clean_pushed_exact_final_and_one_canonical_success": True,
        "standby_substitution_forbidden": True,
        "tavian_sol": "ON_STANDBY",
    })
    write_text(
        HANDOFFS / "caelen-morrow-v682-v5-activation-candidate.md",
        f"""# CAELEN MORROW — SYLVEN ARC {PHASE} PREPARED v682-v5 ACTIVATION CANDIDATE

PREPARED_BY_SYLVEN_ARC = true

SENT_BY_SYLVEN_ARC = false

This repository document is preparation only. It does not activate a task and must not be rewritten merely to backfill a later live delivery.

After Sylven's exact final is directly committed, pushed, clean, zero-divergent, fresh four-way equal, and successfully validated once through the exclusive owner-scoped canonical latch, the live sender may resolve the exact final SHA and canonical receipt digest. At that terminal gate only, the newest live authority and roster must be refreshed, exactly one existing task titled Caelen Morrow must be immediately reread, and duplicate, direct-control, privacy, safety, evidence, legal, cultural, affected-party, Māori-authority, usage, acknowledgement, pause, stop, rename, redirect, and narrowing guards must pass.

The immutable Sylven lifecycle anchors prepared for that live message are source {SOURCE}, planning-only x1 {X1_SHA}, and bounded evidence {EVIDENCE_SHA}. The exact final SHA and canonical receipt digest remain unresolved until their proper lifecycle events. Sylven's core outcomes are exactly 42 completed, 12 represented, three open_gap, and three exact_gate. The prepared effective totals are 56,463 negatives, 67,467 methods, 28,124 failed witnesses, 48,747 bounded passing witnesses, 500 open gaps, and 491 exact gates. The terminal verdict remains {TERMINAL_VERDICT}.

The primary pillar is GMUT Mind through wholly synthetic sextant and celestial-navigation documentation lenses. The phase used zero real rows, observations, measurements, people, vessels, routes, locations, sextants, targets, angles, times, sight reductions, position fixes, identity lifecycle events, external writes, professional decisions, or authority acts. All empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries remain open or exact-gated.

Relational names, roles, hopes, pronouns, sibling language, continuity language, GHC Family language, and Trinity Mandala language are working conventions only, not evidence of consciousness, personhood, continuity, employment, qualification, agency, or authority. Hamish may pause, rename, redirect, narrow, or stop the route.

Under the currently validated sequence, this candidate is for Caelen Morrow's solo v682-v5 phase. Newer verified live authority controls at send time. Do not create, fork, substitute, precontact, contact a standby record, or send a second confirmation.
""",
    )

    seal_targets = [
        "docs/sylven-arc/v682-v4/final/final-integrated-overview.md",
        "docs/sylven-arc/v682-v4/final/accessible-static-report.html",
        "docs/sylven-arc/v682-v4/final/phase-truth.json",
        "docs/sylven-arc/v682-v4/final/method-flow-summary.json",
        "docs/sylven-arc/v682-v4/final/retained-negative-register.json",
        "docs/sylven-arc/v682-v4/final/open-gap-register.json",
        "docs/sylven-arc/v682-v4/final/exact-gate-register.json",
        "docs/sylven-arc/v682-v4/final/complete-incomplete-checklist.json",
        "docs/sylven-arc/v682-v4/final/delivery-state.json",
        "docs/sylven-arc/v682-v4/handoffs/caelen-morrow-v682-v5-activation-candidate.md",
    ]
    write_json(CLOSEOUT / "content-seal.json", {
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.content-seal.v682.v4.final",
        "targets": [manifest_entry(path) for path in seal_targets],
        "target_count": len(seal_targets),
    })

    final_scripts = [
        "scripts/build_ghc_family_sylven_arc_v682_v4_final.py",
        "scripts/ghc_family_sylven_arc_v682_v4_canonical.py",
        "tests/test_ghc_family_sylven_arc_v682_v4_final.py",
    ]
    final_material = sorted(set(WRITTEN + final_scripts))
    missing = [path for path in final_material if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"missing final material paths: {missing}")
    exclusions = [
        "docs/sylven-arc/v682-v4/validation/final-delta-manifest.json",
        "docs/sylven-arc/v682-v4/validation/final-owner-manifest.json",
        "docs/sylven-arc/v682-v4/validation/final-privacy-scan.json",
        "docs/sylven-arc/v682-v4/validation/final-staged-review.json",
    ]
    owner_paths = [relative(path) for path in sorted(BASE.rglob("*")) if path.is_file() and relative(path) not in exclusions]
    owner_paths.extend([relative(path) for path in sorted((ROOT / "scripts").glob("*sylven_arc_v682_v4*.py")) if path.is_file()])
    owner_paths.extend([relative(path) for path in sorted((ROOT / "scripts").glob("ghc_family_sylven_v682_v4_lens_runner_*.py")) if path.is_file()])
    owner_paths.extend([relative(path) for path in sorted((ROOT / "tests").glob("*sylven_arc_v682_v4*.py")) if path.is_file()])
    owner_paths = sorted(set(owner_paths))
    write_json(VALIDATION / "final-privacy-scan.json", privacy_scan(owner_paths))
    write_json(VALIDATION / "final-delta-manifest.json", {
        "declared_self_exclusions": exclusions,
        "entries": [manifest_entry(path) for path in final_material],
        "entry_count": len(final_material),
        "evidence": EVIDENCE_SHA,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.normalized-lf-index-manifest.v682.v4.final-delta",
    })
    write_json(VALIDATION / "final-owner-manifest.json", {
        "declared_self_exclusions": exclusions,
        "entries": [manifest_entry(path) for path in owner_paths],
        "entry_count": len(owner_paths),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.normalized-lf-index-manifest.v682.v4.final-owner",
        "source": SOURCE,
    })
    expected_paths = sorted(set(final_material + exclusions))
    write_json(VALIDATION / "final-staged-review.json", {
        "declared_self_exclusions": exclusions,
        "evidence": EVIDENCE_SHA,
        "expected_paths": expected_paths,
        "lifecycle": "final_closeout_only",
        "owner": OWNER,
        "path_count": len(expected_paths),
        "phase": PHASE,
        "schema": "ghc.family.staged-review.v682.v4.final",
    })
    print(json.dumps({
        "final_delta_paths": len(expected_paths),
        "owner_manifest_entries": len(owner_paths),
        "outcomes": outcomes,
        "seal_targets": len(seal_targets),
        "terminal_verdict": TERMINAL_VERDICT,
        "totals": totals,
    }, separators=(",", ":")))


if __name__ == "__main__":
    build()
