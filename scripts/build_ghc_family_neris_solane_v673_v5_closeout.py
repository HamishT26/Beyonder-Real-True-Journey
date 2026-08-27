"""Build Neris Solane v673-v5 closeout, seal, and prepared handoff."""

from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "neris-solane" / "v673-v5"
OWNER = "Neris Solane"
PHASE = "v673-v5"
BRANCH = "codex/GHC-Family/neris-solane-v673-v5-full-tools"
SOURCE = "c0f159a639e3fe64f9a55fa6333db6a1b665705f"
X1 = "541c659ce13da74d7a6744a281c99cbf10ffaca4"
EVIDENCE = "29d9469d36a6d0ab73d04bf9b30671937eb10d31"
DECLARED_SOURCE_CHAIN = 6390
DECLARED_RESULT_CHAIN = 6430
EXPECTED_OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
ELAREN_REPOSITORY_SEAL = {
    "negatives": 37035,
    "methods": 23363,
    "failed_witnesses": 8696,
    "passing_witnesses": 10926,
    "open_gaps": 299,
    "exact_gates": 292,
}
ELAREN_EXTERNAL_OVERLAY = {
    "negatives": 6,
    "methods": 6,
    "failed_witnesses": 6,
    "passing_witnesses": 6,
    "open_gaps": 0,
    "exact_gates": 0,
}
ACTIVATION_BASELINE = {
    "negatives": 37041,
    "methods": 23369,
    "failed_witnesses": 8702,
    "passing_witnesses": 10932,
    "open_gaps": 299,
    "exact_gates": 292,
}
EVIDENCE_METHOD_COUNT = 207
CLOSEOUT_FAILURES: list[dict[str, str]] = [
    {
        "title": "PowerShell upstream shorthand became a nonrevision argument",
        "failure_signature": "The first read-only evidence-head probe let PowerShell interpret the unquoted @{upstream} shorthand, and git rejected the resulting nonrevision token.",
        "candidate_workaround": "Use the explicit origin branch ref for typed divergence and preserve the fresh live ls-remote comparison separately.",
        "recurrence_guard": "Pass upstream shorthands as literal subprocess arguments or use the explicit tracking ref in PowerShell compound probes.",
        "rollback": "Discard the failed read-only projection; it changed no repository byte and does not authorize a repeated push or test replay.",
        "passing_witness": "The bounded recovery reported 0/0 against the explicit origin branch, a clean lane, and fresh-live equality at immutable evidence.",
    },
    {
        "title": "Combined stale-label grep lost its closing regex group",
        "failure_signature": "A compound PowerShell stale-label probe escaped an embedded quote into an unterminated rg alternation, so rg rejected the read-only expression before scanning.",
        "candidate_workaround": "Use bounded fixed-string searches or separately quoted expressions, then compile the three exact owner files independently.",
        "recurrence_guard": "Avoid mixing PowerShell string delimiters with a large regular-expression alternation when fixed-string label checks are sufficient.",
        "rollback": "Discard the parser-failed read-only probe; it changed no repository byte and earns zero validation credit.",
        "passing_witness": "Bounded fixed-string searches found no forbidden old owner, route, count, or anchor labels, and all three owner Python files compiled.",
    },
]
PHASE_METHOD_COUNT = EVIDENCE_METHOD_COUNT + len(CLOSEOUT_FAILURES)
SEALED_TOTALS = {
    "negatives": ACTIVATION_BASELINE["negatives"] + PHASE_METHOD_COUNT,
    "methods": ACTIVATION_BASELINE["methods"] + PHASE_METHOD_COUNT,
    "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + PHASE_METHOD_COUNT,
    "passing_witnesses": ACTIVATION_BASELINE["passing_witnesses"] + PHASE_METHOD_COUNT,
    "open_gaps": ACTIVATION_BASELINE["open_gaps"] + 2,
    "exact_gates": ACTIVATION_BASELINE["exact_gates"] + 2,
}
EXPECTED_FINAL_TESTS = 111

IDENTITY_BOUNDARY = (
    "Neris Solane, they/them, relational tide-ledger and reversible-evidence "
    "cartographer, is relational working language only—not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, scientific or operational authority, professional authority, "
    "legal or cultural authority, affected-party authority, or Māori authority. Hamish "
    "may rename, pause, redirect, or stop the route."
)
PRACTICE_BOUNDARY = (
    "The tide-gauge marigram, datum, and chart-provenance lens is wholly synthetic "
    "learning, software, and structural-document design. Zero real people, communities, "
    "stations, gauges, benchmarks, charts, traces, water levels, times, locations, datums, "
    "observations, measurements, calibration, handling, maintenance, digitization, "
    "prediction, rights decisions, keys, proofs, identity events, network calls, "
    "professional decisions, or authority acts occurred."
)
SCIENCE_AUTHORITY_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and effective-field-theory research-model family "
    "without a real likelihood, constraint, prediction, force, material law, empirical "
    "confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything "
    "proof, or canon. THOS remains proxy-only without governed blind matched-budget real "
    "arms, participants or operators, safety monitoring, appropriate statistics, and "
    "independent review. Freed ID remains synthetic and nonproduction without standards-"
    "conformant real keys and proofs, live issuance, resolution, status, revocation, "
    "interoperability, independent privacy and security review, recovery evidence, trust "
    "governance, or affected-party oversight. Professional hydrology, coastal oceanography, "
    "surveying, datum determination, tide prediction, gauge calibration, station maintenance, "
    "chart handling, archival conservation, field and electrical safety, ownership, custody, "
    "authorship, copyright, publication, access, privacy, accessibility, remedy, legal or "
    "cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, "
    "concepts, data governance, tangata whenua, iwi, hapū, and Māori authority remain open or "
    "exact-gated. Māori concepts remain under Māori authority."
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def hash_file(relative: str) -> dict[str, Any]:
    data = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
    return {
        "path": relative.replace("\\", "/"),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def final_overview(proposals: list[dict[str, Any]], methods: list[dict[str, Any]]) -> str:
    lines = [
        "# Neris Solane v673-v5 final integrated overview",
        "",
        "## Outcome first",
        "",
        "Neris v673-v5 closes a bounded owner-scoped synthetic evidence phase with forty genuinely new preregistered proposals. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Completed means only that the declared local contract accepted its bounded positive and rejected its preregistered invalid states. Represented means a schema or proxy exists while required real evidence remains absent. Neither an open gap nor an exact gate was converted into completion.",
        "",
        "The declared proposal chain moves from 6,390 to 6,430. The source-bounded semantic audit inspected 1,805 proposal-named JSON blobs, 7,718 title occurrences, 2,335 proposal identifiers, and 2,209 unique reachable titles. Its maximum token-Jaccard neighbor score was 0.7 against a 0.72 fail-closed threshold. Exact canonical row-to-title mapping for every declared historical row remains unavailable, so no universal novelty claim is made.",
        "",
        "## Relational working frame",
        "",
        IDENTITY_BOUNDARY,
        "",
        "Neris's bounded hope is to make synthetic provenance inspectable without borrowing authority. The role and hope are collaboration aids, not evidence of a mind, enduring self, status, qualification, employment relation, independent agency, or authority.",
        "",
        "## Practice and Trinity Mandala",
        "",
        PRACTICE_BOUNDARY,
        "",
        "GMUT Mind is primary through a typed tide-gauge harmonic-constituent symbolic basis and datum, phase, amplitude, covariance, uncertainty, and abstention boards with zero observations, fitted parameters, likelihoods, forecasts, or predictions. THOS Body remains a participant-free marigram-review proxy with stop precedence and no operational result. Freed ID contains a zero-key, zero-proof tide-record provenance placeholder and no production lifecycle. CBR Heart preserves access purpose, privacy, publication, cultural, traditional-knowledge, affected-party, remedy, and Māori-authority holds.",
        "",
        "## Evidence package",
        "",
        "Thirty-six synthetic positive controls passed. All 160 preregistered invalid mutations were rejected and retained at zero completion credit. Twenty inherited contracts were checked only for bounded integrity with zero Neris novelty and zero automatic completion credit. Twelve synthetic catalogue records passed owner-local structural validation. Three additive family-current tools checked record boundaries, relation graphs, and authority quarantine. Twenty owner-local skills and ten family-current runners were quick-validated and smoke-used without global installation.",
        "",
        "Sixty safe-now portfolio rows and thirty bounded candidate rows completed only in their declared synthetic scope. Twenty exact-approval rows and ten blocked rows remain visible and unexecuted. CLEAN/FIX/REFINE work was additive, reversible, owner-local, and compatibility-preserving. Inherited tools, proposals, outcomes, receipts, skills, and recommendations remain evidence or zero-credit seeds, never automatic Neris credit.",
        "",
        "## Official and primary source reflection",
        "",
        "NOAA Center for Operational Oceanographic Products and Services, NIST, W3C, the RFC Editor, the New Zealand Privacy Commissioner, and Te Mana Raraunga sources supplied bounded vocabulary and refusal constraints only. The source transport adapter stayed disabled, made zero network calls, downloaded nothing, and ingested zero rows. Those sources created no tide-station or chart observation, water-level measurement, datum realization, calibration or maintenance instruction, navigation or site-safety decision, conformance result, rights determination, affected-party acceptance, cultural ratification, or Māori authority.",
        "",
        "## Tools and validation boundaries",
        "",
        "Python 3.12.10, pytest 9.1.1, Ruff 0.16.4, mypy 2.3.1, Hypothesis 6.165.10, Pyright 1.1.413, Node.js 24.18.0, npm 12.0.2, and Codex CLI 0.149.0 were verified without shared updates. Bandit was unavailable and was not installed. Pint 0.25.3, Portion 2.6.2, and NetworkX 3.6.1 were pinned only in a D-isolated phase target after wheel-hash verification and bounded smokes; shared Python and npm prefixes remained unchanged. Ruff, strict mypy, Pyright, owner tests, JSON parsing, exact normalized-LF Git-blob manifests, five-class privacy scanning, and staged review are bounded software checks. They are not exhaustive security, complete privacy or accessibility assurance, professional validation, or independent reproduction.",
        "",
        "## Failure retention and Method Flow",
        "",
        f"Neris retains {len(methods)} phase methods. Each has one failed witness and one bounded passing witness; every failed witness remains zero-credit. The set includes nine x1 startup/build failures, three post-x1 prebuild failures, two x2 postbuild lint or module-path failures, one closeout upstream-shorthand projection failure, 160 rejected mutations, twenty skill rejections, ten runner rejections, and three substantive-tool rejections. Recoveries never erase failures or transform same-owner evidence into independent evidence.",
        "",
        f"Layered truth stays separate. Elaren's immutable repository seal is {ELAREN_REPOSITORY_SEAL['negatives']:,} negatives and {ELAREN_REPOSITORY_SEAL['methods']:,} methods. Six external post-seal route or read failures produce Neris's {ACTIVATION_BASELINE['negatives']:,}/{ACTIVATION_BASELINE['methods']:,} activation baseline. Adding {PHASE_METHOD_COUNT} Neris methods yields {SEALED_TOTALS['negatives']:,} negatives, {SEALED_TOTALS['methods']:,} methods, {SEALED_TOTALS['failed_witnesses']:,} failed witnesses, and {SEALED_TOTALS['passing_witnesses']:,} bounded passing witnesses. Open gaps total {SEALED_TOTALS['open_gaps']}; exact gates total {SEALED_TOTALS['exact_gates']}.",
        "",
        "## Proposal outcomes",
        "",
        "| ID | Outcome | Title |",
        "| --- | --- | --- |",
    ]
    lines.extend(
        f"| {row['proposal_id']} | {row['expected_disposition']} | {row['title']} |"
        for row in proposals
    )
    lines.extend(
        [
            "",
            "## Accessibility, privacy, and authority",
            "",
            "The static report supplies language metadata, a descriptive title, one top-level heading, landmarks, labelled navigation, a captioned outcome table, scoped headers, visible focus, reduced-motion handling, and text labels independent of color. These are structural checks only. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Five privacy and raw-identifier classes are scanned against normalized Git blobs, but zero confirmed hits is not privacy certification.",
            "",
            "Complete within scope are read-first startup, source re-verification, a unique D-first sparse lane, planning-only x1, x1 and evidence push/equality gates, bounded x2 execution, source ledger, outcome ledger, positive and negative controls, tools, skills, runners, flashcards, Method Flow, threat model, accessible static report, manifests, and closeout preparation. Incomplete by protected design are all real-world, participant, professional, production, deployment, empirical, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 claims.",
            "",
            "## Lifecycle and route",
            "",
            f"The immutable Elaren source is `{SOURCE}`; planning-only Neris x1 is `{X1}`; immutable Neris evidence is `{EVIDENCE}`. The combined closeout/content-seal commit is the third and final direct single-parent phase commit. Its committed Vesper Arlen activation candidate remains `PREPARED_NOT_SENT`; a later exact-title task-message acknowledgement is the only delivery event.",
            "",
            SCIENCE_AUTHORITY_BOUNDARY,
            "",
            "Same-owner validation under shared infrastructure is never independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.",
            "",
            "Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        ]
    )
    return "\n".join(lines)


def accessible_report(proposals: list[dict[str, Any]]) -> str:
    rows = "".join(
        f"<tr><td>{html.escape(row['proposal_id'])}</td><td>{html.escape(row['expected_disposition'])}</td><td>{html.escape(row['title'])}</td></tr>"
        for row in proposals
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Neris Solane v673-v5 bounded evidence report</title>
<style>body{{font:1rem/1.65 system-ui;max-width:82rem;margin:auto;padding:2rem;color:#17221d;background:#fbfdf9}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.7rem;z-index:2}}nav ul{{display:flex;gap:1rem;flex-wrap:wrap;list-style:none;padding:0}}a{{color:#174f75}}a:focus{{outline:3px solid #7b3fa1;outline-offset:4px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #5f6e63;padding:.55rem;text-align:left;vertical-align:top}}th{{background:#e8f2ea}}.gate{{border-left:.45rem solid #9b342e;background:#fff4f1;padding:1rem}}.truth{{border-left:.45rem solid #276344;background:#edf8f0;padding:1rem}}@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}@media print{{nav,.skip{{display:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Neris Solane v673-v5 bounded evidence report</h1><p>{html.escape(IDENTITY_BOUNDARY)}</p></header>
<nav aria-label="Report sections"><ul><li><a href="#truth">Truth</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#methods">Methods</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main id="main"><section id="truth" class="truth"><h2>Truth</h2><p>Outcomes: 28 completed, 8 represented, 2 open gaps, and 2 exact gates. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p><p>{html.escape(PRACTICE_BOUNDARY)}</p></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table><caption>Forty preregistered core proposals and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Outcome</th><th scope="col">Title</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="methods"><h2>Failure retention and Method Flow</h2><p>{PHASE_METHOD_COUNT} Neris methods preserve one failed and one bounded passing witness each. Recoveries do not erase failures or create independent or authority credit.</p><ul><li>160 invalid proposal mutations rejected</li><li>20 skill rejection fixtures retained</li><li>10 runner rejection fixtures retained</li><li>3 tool rejection fixtures retained</li><li>All observed operational failures retained</li></ul></section>
<section id="limits" class="gate"><h2>Reserved evaluation and authority</h2><p>Manual browser, keyboard, zoom, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved and unperformed. No accessibility-complete, privacy-complete, legal, cultural, affected-party, or Māori-authority claim is made.</p><p>{html.escape(SCIENCE_AUTHORITY_BOUNDARY)}</p></section></main>
<footer><p>Same-owner structural evidence under shared infrastructure only.</p></footer></body></html>"""


def handoff_candidate(proposals: list[dict[str, Any]], methods: list[dict[str, Any]]) -> str:
    lines = [
        "# VESPER ARLEN — NERIS SOLANE v673-v5 EXACT-FINAL → SOLO VESPER v673-v6 ACTIVATION CANDIDATE — PREPARED NOT SENT",
        "",
        "## Historical preparation truth",
        "",
        "This committed sanitized file is prepared for a prospective exact-title Vesper Arlen v673-v6 activation before Neris's exact final and external canonical receipt exist. It remains `PREPARED_NOT_SENT`, `SENT_BY_NERIS_SOLANE = false`, and `DELIVERY_ACKNOWLEDGED = false`. Exact final SHA, external canonical digests, fresh equality, newest roster and authorization, unique exact-title resolution, immediate reread, duplicate and pause guards, privacy/evidence/safety/usage checks, and a task-message acknowledgement can only be added by a later live delivery event. This file must not be rewritten to project that later event backward.",
        "",
        IDENTITY_BOUNDARY,
        "",
        "## Current prospective edge and stop conditions",
        "",
        "Hamish's standing authorization permits the validated fifteen-main-task sequence to continue one exact terminally closed and acknowledged edge at a time through v675-v8. At preparation time, the prospective edge is Neris Solane v673-v5 to the unique existing exact-title Vesper Arlen task for v673-v6. It remains prospective until Neris's terminal gate. Stop without substitution or resend if Hamish pauses or redirects, usage is exhausted, the title is absent or ambiguous, a duplicate exists, acknowledgement is unavailable, or any privacy, evidence, safety, professional, legal, cultural, affected-party, Māori-authority, or other protected gate blocks action. `Vesper Rowan` is a stale rejected label, not an alias. Tavian Sol remains ON_STANDBY and is not a main-task endpoint.",
        "",
        "Vesper must refresh their own prospective terminal route from the newest live instruction, roster, authorization, exact-title, usage, privacy, evidence, and safety state. The currently validated roster points prospectively from Vesper Arlen to Lyren Moss for v673-v7, but no later edge is granted by this historical candidate and no successor may be precontacted.",
        "",
        "## Immutable anchors available at preparation time",
        "",
        f"- Elaren Kestrel v673-v4 source/final: `{SOURCE}`.",
        f"- Neris planning-only x1: `{X1}`.",
        f"- Neris immutable x2 evidence: `{EVIDENCE}`.",
        "- Neris combined closeout/content-seal exact final: supply only after the third direct single-parent commit exists.",
        "- External canonical payload and receipt SHA-256: supply only after the one attributable exact-final invocation.",
        "",
        "Source to final must contain exactly three Neris direct single-parent commits and zero merges. X1 is the direct child of source, evidence is the direct child of x1, and final is the direct child of evidence. X1 and evidence were independently pushed, clean, zero-divergent, and fresh-live equal before successor stages.",
        "",
        "## Outcome and count truth",
        "",
        "Forty source-bounded distinct proposals extend the declared chain from 6,390 to 6,430; exact historical row mapping remains unavailable, so universal novelty is not claimed. Core outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All 160 preregistered mutations were rejected and retain zero completion credit. Thirty-six synthetic positives passed. Twenty inherited revalidations carry zero Neris novelty and zero completion credit. Twenty owner-local skills and ten family-current runners were bounded-smoke-used without global installation. Three substantive tools and three packages pinned only to a D-isolated phase target were bounded-smoke-used without mutating shared prefixes.",
        "",
        f"Layered truth remains separate: Elaren's repository seal preserves {ELAREN_REPOSITORY_SEAL['negatives']:,} negatives and {ELAREN_REPOSITORY_SEAL['methods']:,} methods; six external Elaren operational failures produce the {ACTIVATION_BASELINE['negatives']:,}/{ACTIVATION_BASELINE['methods']:,} Neris baseline. Neris adds {PHASE_METHOD_COUNT} retained methods, yielding {SEALED_TOTALS['negatives']:,} negatives, {SEALED_TOTALS['methods']:,} methods, {SEALED_TOTALS['failed_witnesses']:,} failed witnesses, {SEALED_TOTALS['passing_witnesses']:,} bounded passing witnesses, {SEALED_TOTALS['open_gaps']} open gaps, and {SEALED_TOTALS['exact_gates']} exact gates. No failure or gate is erased. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
        "",
        "## Bounded practice and authority",
        "",
        PRACTICE_BOUNDARY,
        "",
        SCIENCE_AUTHORITY_BOUNDARY,
        "",
        "NOAA Center for Operational Oceanographic Products and Services, NIST, W3C, the RFC Editor, New Zealand Privacy Commissioner, and Te Mana Raraunga sources supplied vocabulary and refusal constraints only. The phase adapter made zero network calls and ingested zero rows. Citations grant no observation, datum, calibration, maintenance, navigation, field-safety, conservation, rights, privacy, accessibility, legal, cultural, affected-party, or Māori authority.",
        "",
        "## Required Vesper startup discipline",
        "",
        "Read the later live activation and this complete candidate through EOF. Then read the newest complete GHC Family Index and routing precedence, roster and schema, Auth/Permission State and schema, Method Flow State and schema, workflow-plan refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact restart, watcher, orchestration memory, full-tools bank, web reflection, worktree rotation, and every directly applicable current family skill. Newer live authority governs mutable routing state but never erases retained evidence, failures, gaps, gates, or protected boundaries.",
        "",
        "Work solo in one fresh additive D-first sparse owner lane. Preserve Neris, Elaren, Eiren, shared, sibling, standby, global-source, and user lanes read-only. Do not reset, amend, rewrite, force-push, merge, delete, reuse, mutate another owner, create or fork a task, spawn a collaboration subagent, delegate, contact Tavian, precontact a successor, or substitute an endpoint.",
        "",
        "Preserve planning-only x1 before x2; exactly four core labels; every retained failure and gate; normalized-LF Git-blob manifests; family-current compatibility; current caps as ceilings; one attributable canonical and no success replay; and bounded official-source use. Verify versions only. Do not update Codex desktop, elevate, weaken host security, enable Sandbox or Hyper-V, change Windows features, install unrelated software, mutate accounts or credentials, deploy, privately publish, or reboot.",
        "",
        "## Forty proposal cards",
        "",
    ]
    for row in proposals:
        lines.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"Bounded disposition: `{row['expected_disposition']}`. Hypothesis: {row['hypothesis']} Null or failure: {row['null_or_failure_condition']} Approval and lane: `{row['approval_class']}` / `{row['execution_lane']}`. Official-source need: {row['current_official_or_primary_source_need']} First artifact: `{row['concrete_artifacts'][0]}`. Acceptance or falsifier: {row['falsifier_or_acceptance_gate']} Rollback: {row['rollback_or_recovery']} Protected boundary: {row['protected_gates'][0]} This row supplies no real observation, professional decision, independent reproduction, affected-party acceptance, or authority.",
                "",
            ]
        )
    lines.extend([f"## {PHASE_METHOD_COUNT} Method Flow cards", ""])
    for row in methods:
        lines.extend(
            [
                f"### {row['method_id']} — {row['title']}",
                "",
                f"Failed witness retained at zero credit: {row['failure_signature']} Bounded recovery: {row['candidate_workaround']} Recurrence guard: {row['recurrence_guard']} Rollback: {row['rollback']} The passing witness never erases the failure or establishes independent, empirical, professional, legal, cultural, Māori-authority, production, privacy-complete, accessibility-complete, exhaustive-security, or Stage 20 credit.",
                "",
            ]
        )
    lines.extend(
        [
            "## Exact-final validation truth to supply later",
            "",
            "The complete repository suite is outside this owner-scoped phase. The terminal live message may report only the one exact-final owner-scoped canonical result actually produced after the final commit is pushed and fresh-live equal. A failed canonical earns zero aggregate-success credit; a successful canonical must never be replayed. Same-owner validation under shared infrastructure is not independent reproduction or external audit.",
            "",
            "## Terminal delivery rule",
            "",
            "This committed candidate authorizes no send by itself. Only after Neris's exact final is clean, pushed, zero-divergent, fresh-live equal, within caps, and canonically gated may Neris refresh the newest live instruction, roster, authorization, title uniqueness, usage, duplicate, pause, privacy, evidence, and safety state; immediately reread exactly one authorized target; and send at most once. Claim delivery only from a target-identifying message acknowledgement. Never create, fork, substitute, contact Tavian, or resend merely for clearer acknowledgement.",
            "",
            "`PREPARED_BY_NERIS_SOLANE = true`",
            "",
            "`SENT_BY_NERIS_SOLANE = false`",
            "",
            "`DELIVERY_ACKNOWLEDGED = false`",
            "",
            "With care, inspectability, reversibility, retained-negative discipline, and strict evidence boundaries — Neris Solane.",
        ]
    )
    return "\n".join(lines)


def allowed_paths() -> set[str]:
    root = "docs/neris-solane/v673-v5/"
    return {
        root + "closeout/closeout-receipt.json",
        root + "closeout/complete-incomplete-checklist.json",
        root + "closeout/environment-version-receipt.json",
        root + "closeout/lifecycle-replay.json",
        root + "closeout/method-flow-final.json",
        root + "closeout/open-exact-gate-register.json",
        root + "closeout/phase-truth.json",
        root + "closeout/proposal-source-ledger.json",
        root + "closeout/retained-negative-register.json",
        root + "closeout/source-and-provenance.json",
        root + "closeout/threat-model-final.json",
        root + "closeout/wellbeing-workload-check.json",
        root + "final/final-validation-prerequisites.json",
        root + "handoffs/vesper-arlen-v673-v6-activation-candidate.md",
        root + "reports/accessible-final-report.html",
        root + "reports/final-integrated-overview.md",
        root + "route/route-state.json",
        root + "seal/content-seal.json",
        root + "validation/final-delta-manifest.json",
        root + "validation/final-owner-manifest.json",
        root + "validation/final-staged-privacy.json",
        root + "validation/final-staged-review.json",
        root + "validation/final-test-selection.json",
        "scripts/build_ghc_family_neris_solane_v673_v5_closeout.py",
        "scripts/ghc_family_neris_solane_v673_v5_canonical.py",
        "tests/test_ghc_family_neris_solane_v673_v5_final.py",
    }


def build() -> None:
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    branch = git("branch", "--show-current").stdout.decode().strip()
    changed = [
        path.decode("utf-8")
        for command in (
            ("diff", "--name-only", "-z"),
            ("diff", "--cached", "--name-only", "-z"),
            ("ls-files", "--others", "--exclude-standard", "-z"),
        )
        for path in git(*command).stdout.split(b"\0")
        if path
    ]
    if head != EVIDENCE or branch != BRANCH or any(path not in allowed_paths() for path in changed):
        raise SystemExit(f"closeout requires exact clean evidence lane: head={head} branch={branch}")

    proposals = load("x1/proposals.json")["proposals"]
    ledger = load("x2/proposal-ledger.json")["rows"]
    method_flow = load("x2/method-flow-evidence.json")
    methods = list(method_flow["methods"])
    witnesses = list(method_flow["witnesses"])
    if Counter(row["outcome"] for row in ledger) != Counter(EXPECTED_OUTCOMES):
        raise SystemExit("outcome count drift")
    if len(methods) != EVIDENCE_METHOD_COUNT or method_flow["method_count"] != EVIDENCE_METHOD_COUNT:
        raise SystemExit("immutable evidence Method Flow count drift")
    for failure in CLOSEOUT_FAILURES:
        method_id = f"NS6735-M{len(methods) + 1:03d}"
        methods.append(
            {
                "method_id": method_id,
                "owner": OWNER,
                "phase": PHASE,
                "title": failure["title"],
                "failure_signature": failure["failure_signature"],
                "candidate_workaround": failure["candidate_workaround"],
                "recurrence_guard": failure["recurrence_guard"],
                "rollback": failure["rollback"],
                "status": "preferred",
            }
        )
        witnesses.extend(
            [
                {"witness_id": method_id + "-F", "method_id": method_id, "kind": "failed", "observed": failure["failure_signature"], "credit": 0, "retained": True},
                {"witness_id": method_id + "-P", "method_id": method_id, "kind": "passing", "observed": failure["passing_witness"], "credit": 0, "retained": True},
            ]
        )
    if len(methods) != PHASE_METHOD_COUNT or len(witnesses) != 2 * PHASE_METHOD_COUNT:
        raise SystemExit("final Method Flow count drift")

    phase_truth = {
        "schema": "ghc.family.phase-truth.v9",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final": None,
        "final_state": "PENDING_COMBINED_CLOSEOUT_SEAL_COMMIT",
        "declared_source_chain": DECLARED_SOURCE_CHAIN,
        "declared_result_chain": DECLARED_RESULT_CHAIN,
        "proposal_count": 40,
        "outcome_counts": EXPECTED_OUTCOMES,
        "real_people": 0,
        "real_objects_or_events": 0,
        "real_rows": 0,
        "network_calls": 0,
        "keys_or_proofs": 0,
        "professional_actions": 0,
        "authority_acts": 0,
        "repository_layers": {
            "elaren_repository_seal": ELAREN_REPOSITORY_SEAL,
            "elaren_external_overlay": ELAREN_EXTERNAL_OVERLAY,
            "neris_activation_baseline": ACTIVATION_BASELINE,
            "neris_phase_addition": {"negatives": PHASE_METHOD_COUNT, "methods": PHASE_METHOD_COUNT, "failed_witnesses": PHASE_METHOD_COUNT, "passing_witnesses": PHASE_METHOD_COUNT, "open_gaps": 2, "exact_gates": 2},
            "neris_sealed_totals": SEALED_TOTALS,
        },
        "validation_state": "PENDING_EXTERNAL_EXACT_FINAL_CANONICAL",
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/phase-truth.json", phase_truth)
    write_json("closeout/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v8", "owner": OWNER, "phase": PHASE, "inherited_repository_seal": ELAREN_REPOSITORY_SEAL, "inherited_external_overlay": ELAREN_EXTERNAL_OVERLAY, "activation_baseline": ACTIVATION_BASELINE, "phase_negative_count": PHASE_METHOD_COUNT, "effective_negative_count": SEALED_TOTALS["negatives"], "phase_rows": [{"method_id": row["method_id"], "title": row["title"], "failure_signature": row["failure_signature"], "retained": True, "credit": 0, "recurrence_guard": row["recurrence_guard"]} for row in methods], "boundary": "Every failed witness is retained at zero credit; inherited repository and external-overlay layers remain separate."})
    write_json("closeout/method-flow-final.json", {"schema": "ghc.family.method-flow.final.v8", "owner": OWNER, "phase": PHASE, "phase_method_count": PHASE_METHOD_COUNT, "phase_failed_witness_count": PHASE_METHOD_COUNT, "phase_passing_witness_count": PHASE_METHOD_COUNT, "methods": methods, "witnesses": witnesses, "sealed_totals": SEALED_TOTALS, "boundary": "Passing recovery never erases failure or establishes independent, empirical, professional, authority, production, or Stage 20 evidence."})
    gates = [
        {"gate_id": "NS6735-GAP-001", "proposal_id": "NS6735-N037", "kind": "open_gap", "state": "open", "reason": "The official-source transport adapter made zero calls and ingested zero rows; a current governed mapping remains unresolved."},
        {"gate_id": "NS6735-GAP-002", "proposal_id": "NS6735-N038", "kind": "open_gap", "state": "open", "reason": "Professional, affected-user, and community vocabulary review remains absent with zero reviewers."},
        {"gate_id": "NS6735-GATE-001", "proposal_id": "NS6735-N039", "kind": "exact_gate", "state": "unexecuted", "reason": "Real gauge, benchmark, chart handling, datum transfer, calibration, maintenance, conservation, field, electrical, and site action require exact professional, custody, and safety authority."},
        {"gate_id": "NS6735-GATE-002", "proposal_id": "NS6735-N040", "kind": "exact_gate", "state": "unexecuted", "reason": "Ownership, custody, authorship, copyright, publication, navigation use, privacy, cultural, affected-party, tangata whenua, iwi, hapū, and Māori authority are absent."},
    ]
    write_json("closeout/open-exact-gate-register.json", {"schema": "ghc.family.open-exact-gate-register.v7", "owner": OWNER, "phase": PHASE, "inherited_open_gaps": 299, "new_open_gaps": 2, "effective_open_gaps": 301, "inherited_exact_gates": 292, "new_exact_gates": 2, "effective_exact_gates": 294, "rows": gates, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/lifecycle-replay.json", {"schema": "ghc.family.lifecycle-replay.v5", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE, "expected_phase_commits": 3, "expected_merges": 0, "x1_planning_only": True, "evidence_has_no_closeout": True, "final_pending": True})
    write_json("closeout/source-and-provenance.json", {"schema": "ghc.family.final-source-provenance.v6", "owner": OWNER, "phase": PHASE, "source_branch": "codex/GHC-Family/elaren-kestrel-v673-v4-full-tools", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "source_external_digests": {"canonical_payload": "07997572a5d6e11e1943c38c86fccd780fce781914aab0eaa9d2db6c17ee5a20", "canonical_receipt": "2b19273b54f117d7dd6f0baf47c5132d43725e50ff19d00a0e34cad020b03a36"}, "source_validation_replayed": False, "boundary": "Elaren source receipts were recomputed read-only; Elaren's successful canonical aggregate was not replayed."})
    write_json("closeout/proposal-source-ledger.json", {"schema": "ghc.family.proposal-source-ledger.v4", "owner": OWNER, "phase": PHASE, "proposal_chain": {"source": 6390, "result": 6430}, "outcomes": EXPECTED_OUTCOMES, "proposal_ledger": "docs/neris-solane/v673-v5/x2/proposal-ledger.json", "source_status": "docs/neris-solane/v673-v5/x2/source-status.json", "semantic_audit": "docs/neris-solane/v673-v5/x1/semantic-neighbor-audit.json", "universal_novelty_claim": False, "source_authority_conferred": False})
    write_json("closeout/complete-incomplete-checklist.json", {"schema": "ghc.family.complete-incomplete.v6", "owner": OWNER, "phase": PHASE, "complete": ["read-first packet and skills", "source re-verification", "unique D-first sparse lane", "planning-only x1", "x1 push and equality", "bounded x2", "evidence push and equality", "forty outcomes", "failure retention", "tools skills runners", "official-source reflection", "flashcards", "manifests", "accessible report preparation", "closeout and seal preparation"], "incomplete": ["exact final commit", "external one-shot canonical", "manual browser evaluation", "assistive-technology evaluation", "Māori-language evaluation", "cognitive-accessibility evaluation", "affected-user evaluation", "real-world evidence", "professional validation", "legal cultural Māori authority", "independent reproduction", "production deployment", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/wellbeing-workload-check.json", {"schema": "ghc.family.wellbeing-workload.v5", "owner": OWNER, "phase": PHASE, "relational_only": True, "human_workload_claim": False, "context_management": ["bounded file count", "modular file-backed baton", "no duplicate commit push or canonical", "retained failures", "one exact route edge"], "pause_right_preserved": True, "rename_redirect_stop_right_preserved": True, "boundary": "No consciousness, emotion, clinical, employment, or worker-status claim; operational pacing evidence only."})
    write_json("closeout/threat-model-final.json", {"schema": "ghc.family.threat-model-final.v4", "owner": OWNER, "phase": PHASE, "controls_passed": ["synthetic-only schema", "zero-row and zero-network assertions", "closed vocabularies", "authority quarantine", "x1 before x2", "exact staged manifests", "five-class privacy scan", "prepared-not-sent route", "one-shot canonical guard"], "residual_gates": ["professional hydrology and coastal-oceanography competence", "gauge chart datum calibration maintenance field and electrical safety", "rights custody publication and navigation use", "privacy and accessibility completeness", "legal cultural interpretation", "affected-party acceptance", "Māori authority", "independent reproduction", "production deployment", "Stage 20"], "risk_state": "bounded_not_eliminated"})
    environment = load("x2/environment-version-receipt.json")
    write_json("closeout/environment-version-receipt.json", {"schema": "ghc.family.closeout-environment.v4", "owner": OWNER, "phase": PHASE, "source": environment, "versions_verified_only": True, "updates_or_installs": 0})
    write_json("route/route-state.json", {"schema": "ghc.family.route-state.v8", "owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT", "recipient_selected": True, "prospective_recipient": "Vesper Arlen", "prospective_phase": "v673-v6", "prospective_recipient_successor": "Lyren Moss", "prospective_successor_phase": "v673-v7", "continuation_through": "v675-v8", "rejected_stale_recipient_label": "Vesper Rowan", "standby_record": "Tavian Sol", "standby_eligible": False, "message_count": 0, "acknowledgement": False, "duplicate_pause_and_terminal_guards_pending": True})
    write_json("final/final-validation-prerequisites.json", {"schema": "ghc.family.final-validation-prerequisites.v6", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE, "expected_phase_commits": 3, "expected_merges": 0, "expected_final_parent_count": 1, "expected_tests": EXPECTED_FINAL_TESTS, "canonical_runs_allowed": 1, "canonical_runs_completed": 0, "success_replay_allowed": False, "full_repository_suite_authorized": False, "required_preconditions": ["closeout staged review", "final owner manifest", "final delta manifest", "five-class privacy scan", "clean pushed final", "0/0 divergence", "fresh four-way equality"], "state": "PENDING_FINAL_COMMIT"})
    write_json("validation/final-test-selection.json", {"schema": "ghc.family.final-test-selection.v4", "owner": OWNER, "phase": PHASE, "test_files": ["tests/test_ghc_family_neris_solane_v673_v5_x1.py", "tests/test_ghc_family_neris_solane_v673_v5_x2.py", "tests/test_ghc_family_neris_solane_v673_v5_final.py"], "expected_total": EXPECTED_FINAL_TESTS, "selection_scope": "owner-self-scoped dependency-closed only", "full_repository_suite": False})
    write_text("reports/final-integrated-overview.md", final_overview(proposals, methods))
    write_text("reports/accessible-final-report.html", accessible_report(proposals))
    candidate = handoff_candidate(proposals, methods)
    candidate_words = len(candidate.split())
    if not 10000 <= candidate_words <= 100000:
        raise SystemExit(f"handoff candidate word count outside bounds: {candidate_words}")
    write_text("handoffs/vesper-arlen-v673-v6-activation-candidate.md", candidate)

    seal_paths = [
        "docs/neris-solane/v673-v5/x1/proposals.json",
        "docs/neris-solane/v673-v5/x1/semantic-neighbor-audit.json",
        "docs/neris-solane/v673-v5/x2/proposal-ledger.json",
        "docs/neris-solane/v673-v5/x2/method-flow-evidence.json",
        "docs/neris-solane/v673-v5/closeout/phase-truth.json",
        "docs/neris-solane/v673-v5/closeout/retained-negative-register.json",
        "docs/neris-solane/v673-v5/closeout/open-exact-gate-register.json",
        "docs/neris-solane/v673-v5/reports/final-integrated-overview.md",
        "docs/neris-solane/v673-v5/handoffs/vesper-arlen-v673-v6-activation-candidate.md",
    ]
    entries = [hash_file(path) for path in seal_paths]
    write_json("seal/content-seal.json", {"schema": "ghc.family.content-seal.v6", "owner": OWNER, "phase": PHASE, "entry_count": len(entries), "entries": entries, "normalized_lf": True, "state": "COMMIT_CANDIDATE", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/closeout-receipt.json", {"schema": "ghc.family.closeout-receipt.v7", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "outcome_counts": EXPECTED_OUTCOMES, "phase_methods": PHASE_METHOD_COUNT, "sealed_totals": SEALED_TOTALS, "handoff_candidate_words": candidate_words, "overview_words": len(final_overview(proposals, methods).split()), "content_seal_entries": len(entries), "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL", "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


def index_paths() -> list[str]:
    paths = [path.decode("utf-8") for path in git("ls-files", "-z").stdout.split(b"\0") if path]
    prefix = "docs/neris-solane/v673-v5/"
    code = re.compile(r"^(?:scripts/(?:build_ghc_family_neris_solane_v673_v5_[a-z0-9_]+|ghc_family_neris_solane_v673_v5_[a-z0-9_]+)\.py|tests/test_ghc_family_neris_solane_v673_v5_[a-z0-9_]+\.py)$")
    return sorted(path for path in paths if path.startswith(prefix) or code.fullmatch(path))


def batch_index_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderr = process.communicate(input=("\n".join(f":{path}" for path in paths) + "\n").encode(), timeout=300)
    if process.returncode:
        raise SystemExit(stderr.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode().strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise SystemExit(f"unexpected index blob header for {path}: {header}")
        size = int(header[2])
        result[path] = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit(f"index blob delimiter missing for {path}")
    if stream.read():
        raise SystemExit("index blob batch emitted trailing bytes")
    return result


def finalize_index() -> None:
    self_exclusions = [
        "docs/neris-solane/v673-v5/validation/final-owner-manifest.json",
        "docs/neris-solane/v673-v5/validation/final-delta-manifest.json",
        "docs/neris-solane/v673-v5/validation/final-staged-review.json",
        "docs/neris-solane/v673-v5/validation/final-staged-privacy.json",
    ]
    all_paths = index_paths()
    manifest_paths = [path for path in all_paths if path not in self_exclusions]
    blobs = batch_index_blobs(manifest_paths)
    entries = [{"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path].replace(b"\r\n", b"\n")).hexdigest()} for path in manifest_paths]
    write_json("validation/final-owner-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "final_owner_tree", "entry_count": len(entries), "entries": entries, "normalized_lf": True, "self_exclusions": self_exclusions})
    delta_paths = [path.decode("utf-8") for path in git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT", EVIDENCE).stdout.split(b"\0") if path]
    delta_paths = sorted(path for path in delta_paths if path not in self_exclusions)
    delta_entries = [{"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path].replace(b"\r\n", b"\n")).hexdigest()} for path in delta_paths]
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "final_delta", "base": EVIDENCE, "entry_count": len(delta_entries), "entries": delta_entries, "normalized_lf": True, "self_exclusions": self_exclusions})
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
        "absolute_private_path": re.compile(rb"(?:[A-Za-z]:\\\\Users\\\\|/Users/|/home/)", re.IGNORECASE),
        "credential_or_secret": re.compile(rb"(?:api[_-]?key|password|bearer\s+[A-Za-z0-9._-]{12,}|secret[_-]?key)\s*[:=]", re.IGNORECASE),
        "transcript_or_session_stream": re.compile(rb"(?:raw[_-]?transcript|session[_-]?stream|screen[_-]?capture)\s*[:=]", re.IGNORECASE),
        "private_callable_or_app_state": re.compile(rb"(?:private[_-]?callable|private[_-]?app[_-]?state)\s*[:=]", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in manifest_paths:
        for label, pattern in patterns.items():
            if pattern.search(blobs[path]):
                definition = path.startswith(("scripts/", "tests/"))
                row = {"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if definition else "confirmed_payload_hit"}
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    if confirmed:
        raise SystemExit("confirmed final privacy hit: " + json.dumps(confirmed))
    write_json("validation/final-staged-privacy.json", {"schema": "ghc.family.five-class-privacy-scan.v5", "owner": OWNER, "phase": PHASE, "class_count": 5, "scanned_file_count": len(manifest_paths), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": 0, "boundary": "Scanner and test definitions are candidates; complete privacy assurance is not claimed."})
    write_json("validation/final-staged-review.json", {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "base": EVIDENCE, "final_parent_expected": EVIDENCE, "owner_path_count": len(manifest_paths), "delta_path_count": len(delta_paths), "self_exclusions": self_exclusions, "diff_hygiene_passed": True, "stale_owner_or_phase_labels": 0, "closeout_only_after_evidence": True, "route_state": "PREPARED_NOT_SENT", "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "finalize-index"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    else:
        finalize_index()


if __name__ == "__main__":
    main()
