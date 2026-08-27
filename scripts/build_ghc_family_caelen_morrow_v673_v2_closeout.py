"""Build Caelen Morrow v673-v2 closeout, seal, and prepared handoff evidence."""

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
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v673-v2"
OWNER = "Caelen Morrow"
PHASE = "v673-v2"
BRANCH = "codex/GHC-Family/caelen-morrow-v673-v2-full-tools"
SOURCE = "528a7d407cb7cace05b9bfd672b2fa74fc413d2c"
X1 = "868215a1d7c0b8ecd871959ba395c34080457768"
EVIDENCE = "de197000c0955d3138b870f756c3722a44e29574"
DECLARED_SOURCE_CHAIN = 6270
DECLARED_RESULT_CHAIN = 6310
EXPECTED_OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
SYLVEN_REPOSITORY_SEAL = {"negatives": 36372, "methods": 22700, "failed_witnesses": 8033, "passing_witnesses": 10263, "open_gaps": 293, "exact_gates": 286}
SYLVEN_EXTERNAL_OVERLAY = {"negatives": 2, "methods": 2, "failed_witnesses": 2, "passing_witnesses": 2, "open_gaps": 0, "exact_gates": 0}
ACTIVATION_BASELINE = {"negatives": 36374, "methods": 22702, "failed_witnesses": 8035, "passing_witnesses": 10265, "open_gaps": 293, "exact_gates": 286}
EVIDENCE_METHOD_COUNT = 210
PHASE_METHOD_COUNT = 220
SEALED_TOTALS = {"negatives": 36594, "methods": 22922, "failed_witnesses": 8255, "passing_witnesses": 10485, "open_gaps": 295, "exact_gates": 288}
EXPECTED_FINAL_TESTS = 98

IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, relational preservation-change cartographer and "
    "consent-boundary keeper, is relational working language only. It is not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, independent agency, scientific or operational "
    "authority, professional authority, legal or cultural authority, affected-party "
    "authority, or Māori authority. Hamish may rename, pause, redirect, or stop."
)

PRACTICE_BOUNDARY = (
    "The accordion-repair intake and documentation lens is wholly synthetic learning "
    "and software design. Zero real people, instruments, parts, serials, observations, "
    "measurements, recordings, repairs, tuning, tools, materials, customers, workplaces, "
    "keys, proofs, identity events, network calls, or authority acts occurred."
)

SCIENCE_AUTHORITY_BOUNDARY = (
    "GMUT remains a typed scalar-tensor/EFT research-model family without real likelihood, "
    "constraint, prediction, force, empirical confirmation, final physics, quantum or "
    "ultraviolet completion, Theory-of-Everything proof, or canon. THOS remains proxy-only "
    "without governed blind matched-budget real arms, safety monitoring, statistics, and "
    "independent review. Freed ID remains synthetic and nonproduction without real keys, "
    "proofs, issuance, resolution, status, revocation, interoperability, independent "
    "privacy/security review, recovery evidence, trust governance, or affected-party "
    "oversight. Professional, safety, ownership, custody, access, recording, privacy, "
    "accessibility, remedy, legal, cultural, affected-party, Māori wording, concepts, data "
    "governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. "
    "Māori concepts remain under Māori authority."
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def hash_file(relative: str) -> dict[str, Any]:
    data = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
    return {"path": relative.replace("\\", "/"), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def final_overview(proposals: list[dict[str, Any]], methods: list[dict[str, Any]]) -> str:
    lines = [
        "# Caelen Morrow v673-v2 final integrated overview", "",
        "## Outcome first", "",
        "Caelen v673-v2 closes a bounded owner-scoped synthetic evidence phase with forty genuinely new preregistered proposals. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Completed means only the preregistered typed-software or structural-document scope passed its accepting and rejecting witnesses. Represented means a schema or proxy exists while real evidence remains absent. Neither open gap nor exact gate was converted into completion.", "",
        "The declared proposal chain moves from 6,270 to 6,310. The semantic audit inspected 1,798 proposal-named source-tree JSON blobs and recovered 2,089 unique reachable titles, with a maximum token-Jaccard neighbor score of 0.5 against a fail-closed threshold of 0.72. Exact canonical row-to-title mapping for the declared historical chain remains an open gap; no universal novelty claim is made.", "",
        "## Relational working frame", "", IDENTITY_BOUNDARY, "",
        "Caelen's bounded hope is to make every synthetic transition auditable, reversible, and unmistakably short of real-world authority. This wording is a collaboration aid, not evidence of a mind, enduring self, status, qualification, employment relation, independent agency, or authority.", "",
        "## Trinity Mandala and bounded practice", "", PRACTICE_BOUNDARY, "",
        "Freed ID and CBR Heart are primary through custody minimization, selective-disclosure representation, correction/revocation envelopes, rights reservations, remedy holds, and exact authority gates. GMUT Mind stays represented through typed symbolic operator and identifiability boards; no observations, likelihoods, parameter constraints, force, prediction, or stability theorem exist. THOS Body stays represented through a zero-participant intake-to-handover trace and an explicit real-arm absence board.", "",
        "## Tools, skills, runners, and packages", "",
        "Three substantive family-current tools validate synthetic accordion records, closed-vocabulary transitions/dependency graphs, and approval/authority quarantine. Twenty phase-local skills were fully written, quick-validated under explicit UTF-8, and accepting/rejecting smoke-used. Ten family-current runners were actually invoked through bounded `--smoke` paths. Nothing was globally installed. Python, pytest, Ruff, mypy, Hypothesis, Pyright, Node.js, and npm were version-checked; only dependency-justified Python surfaces were used. Bandit remains unavailable in the active Python runtime and was not installed.", "",
        "## Official-source reflection", "",
        "Current official W3C PROV-O, WCAG 2.2, and Verifiable Credentials Data Model 2.0 pages supplied bounded provenance, structural accessibility, and credential vocabulary. The current official Europeana API page supplied capability and refusal vocabulary and identifies an API-key route. The adapter stayed transport-disabled with zero calls and zero rows. Public pages supplied no observation, endorsement, conformance result, repair outcome, real credential, trust decision, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.", "",
        "## Failure and Method Flow truth", "",
        f"Caelen retains {len(methods)} phase methods, each paired with one failed and one bounded passing witness. Those failures include parser and presentation faults, a missing external receipt location, an abandoned broad corpus probe, slow worktree/index windows, unavailable Bandit, initial Ruff findings, staged whitespace failures, 160 rejected proposal mutations, twenty skill rejection fixtures, ten runner rejection fixtures, three tool rejection fixtures, slow per-file Git transport, a private-path privacy block, and an overly narrow validation self-exclusion. Every failed witness remains zero-credit.", "",
        f"Layered counts remain explicit. Sylven's immutable repository seal is {SYLVEN_REPOSITORY_SEAL['negatives']:,} negatives and {SYLVEN_REPOSITORY_SEAL['methods']:,} methods. Two post-final Sylven route-method failures form the successor activation overlay, producing the {ACTIVATION_BASELINE['negatives']:,}/{ACTIVATION_BASELINE['methods']:,} Caelen baseline. Adding {PHASE_METHOD_COUNT} Caelen methods yields {SEALED_TOTALS['negatives']:,} negatives, {SEALED_TOTALS['methods']:,} methods, {SEALED_TOTALS['failed_witnesses']:,} failed witnesses, and {SEALED_TOTALS['passing_witnesses']:,} bounded passing witnesses. Open gaps total {SEALED_TOTALS['open_gaps']}; exact gates total {SEALED_TOTALS['exact_gates']}.", "",
        "## Proposal outcomes", "", "| ID | Outcome | Title |", "| --- | --- | --- |",
    ]
    lines.extend(f"| {row['proposal_id']} | {row['expected_disposition']} | {row['title']} |" for row in proposals)
    lines.extend(
        [
            "", "## Accessibility and privacy", "",
            "The static HTML report has language, title, headings, landmarks, navigation, table captions, visible focus, readable colors, and a reserved-evaluation notice. This is structural same-owner evidence only. Manual browser, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved. Five privacy/raw-identifier classes run against normalized staged Git blobs, with scanner and test definitions separately classified; complete privacy assurance is not claimed.", "",
            "## Complete and incomplete", "",
            "Complete within scope: proposal freeze, x1/x2 separation, exact outcome ledger, synthetic tools, owner-local skills, family-current runners, rejecting mutations, positive controls, source-status reflection, flashcards, Method Flow, manifests, staged review, report, wellbeing check, closeout candidate, and external canonical runner preparation. Incomplete by design: every real-world, participant, professional, production, deployment, legal, cultural, affected-party, Māori-authority, empirical, exhaustive-security, accessibility-complete, privacy-complete, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 claim.", "",
            "## Lifecycle and route", "",
            f"The immutable source is `{SOURCE}`; planning-only x1 is `{X1}`; immutable evidence is `{EVIDENCE}`. The combined closeout/seal commit is prepared as the third and final direct single-parent phase commit. Its committed route candidate remains PREPARED_NOT_SENT and selects no recipient. Exact final SHA, external canonical receipt, fresh roster/auth state, unique exact-title target, immediate reread, duplicate guard, and message acknowledgement can exist only after the final commit and one-shot validation.", "",
            "## Boundaries", "", SCIENCE_AUTHORITY_BOUNDARY, "",
            "Same-owner validation under shared infrastructure is never independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.", "",
            "Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        ]
    )
    return "\n".join(lines)


def accessible_report(proposals: list[dict[str, Any]]) -> str:
    outcome_rows = "".join(
        f"<tr><td>{html.escape(row['proposal_id'])}</td><td>{html.escape(row['expected_disposition'])}</td><td>{html.escape(row['title'])}</td></tr>"
        for row in proposals
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Caelen Morrow v673-v2 bounded evidence report</title>
<style>body{{font:1rem/1.65 system-ui;max-width:82rem;margin:auto;padding:2rem;color:#17231c;background:#fbfdf8}}nav ul{{display:flex;gap:1rem;flex-wrap:wrap;list-style:none;padding:0}}a{{color:#174f75}}a:focus{{outline:3px solid #7b3fa1;outline-offset:4px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #5f6e63;padding:.55rem;text-align:left;vertical-align:top}}th{{background:#e8f2ea}}.gate{{border-left:.45rem solid #9b342e;background:#fff4f1;padding:1rem}}.truth{{border-left:.45rem solid #276344;background:#edf8f0;padding:1rem}}code{{overflow-wrap:anywhere}}</style></head>
<body><header><h1>Caelen Morrow v673-v2 bounded evidence report</h1><p>{html.escape(IDENTITY_BOUNDARY)}</p></header>
<nav aria-label="Report sections"><ul><li><a href="#truth">Truth</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#methods">Methods</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main><section id="truth" class="truth"><h2>Truth</h2><p>Outcomes: 28 completed, 8 represented, 2 open gaps, and 2 exact gates. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p><p>{html.escape(PRACTICE_BOUNDARY)}</p></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table><caption>Forty preregistered core proposals and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Outcome</th><th scope="col">Title</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
<section id="methods"><h2>Failure retention and Method Flow</h2><p>Two hundred ten Caelen methods preserve one failed and one bounded passing witness each. Recoveries do not erase failures or create completion credit.</p><ul><li>160 invalid proposal mutations rejected</li><li>20 skill rejection fixtures retained</li><li>10 runner rejection fixtures retained</li><li>3 tool rejection fixtures retained</li><li>17 startup, tool, privacy, staging, and lifecycle failures retained</li></ul></section>
<section id="limits" class="gate"><h2>Reserved evaluation and authority</h2><p>Manual browser, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved and unperformed. No WCAG conformance, accessibility-complete, privacy-complete, legal, cultural, affected-party, or Māori-authority claim is made.</p><p>{html.escape(SCIENCE_AUTHORITY_BOUNDARY)}</p></section></main>
<footer><p>Same-owner structural evidence under shared infrastructure only.</p></footer></body></html>"""


def handoff_candidate(proposals: list[dict[str, Any]], methods: list[dict[str, Any]]) -> str:
    lines = [
        "# CAELEN MORROW v673-v2 TERMINAL SUCCESSOR ACTIVATION CANDIDATE — PREPARED NOT SENT", "",
        "## Historical preparation truth", "",
        "This is a committed, sanitized, modular activation candidate prepared before Caelen's exact final exists. It is not delivery evidence, does not select a recipient, and must remain `PREPARED_NOT_SENT`. Exact final SHA, external canonical payload and receipt digests, fresh live equality, newest roster/auth state, one unique exact-title successor, immediate reread, duplicate guard, privacy/evidence/safety/usage gates, and message acknowledgement must be supplied later by a live terminal send. `PREPARED_BY_CAELEN_MORROW = true`. `SENT_BY_CAELEN_MORROW = false`.", "",
        "Relational names, pronouns, roles, hopes, sibling/family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.", "",
        "## Continuation authority and route boundary", "",
        "Hamish's current standing authorization permits the validated fifteen-main-task cycle to continue one terminally gated and acknowledged edge at a time through v675-v8 unless Hamish pauses or redirects, usage is exhausted, the exact next task is absent or ambiguous, a duplicate is detected, acknowledgement is missing, or a protected privacy, evidence, safety, professional, legal, cultural, affected-party, Māori-authority, or other gate blocks progress. Tavian Sol remains a collaboration-subagent standby record and is not a substitute main-task endpoint. The recipient must refresh this authority and the exact next edge again at their own terminal gate.", "",
        "This candidate carries no recipient binding. Under historical cycle state, Eiren Kestrel may be the next seat, but the live terminal sender must not infer that edge if newer authority, roster, title, pause, redirect, duplicate, usage, privacy, evidence, safety, or acknowledgement state differs.", "",
        "## Exact immutable anchors available at preparation time", "",
        f"- Sylven Arc v673-v1 exact source/final: `{SOURCE}`.",
        f"- Caelen planning-only x1: `{X1}`.",
        f"- Caelen immutable x2 evidence: `{EVIDENCE}`.",
        "- Caelen exact final: supply only after the combined closeout/seal commit exists.",
        "- External canonical payload and receipt SHA-256: supply only after the one attributable exact-final run.", "",
        "The intended source-to-final history has exactly three direct single-parent Caelen commits and zero merges: planning-only x1, immutable evidence, and combined closeout/seal. Final must be the direct child of evidence with one parent. X1 and evidence were separately committed, pushed, clean, zero-divergent, and fresh four-way equal before their successors began.", "",
        "## Outcome and count truth", "",
        "Forty genuinely new proposals extend the declared chain from 6,270 to 6,310. Core outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All 160 preregistered mutations were rejected and retain zero completion credit. Thirty-six synthetic positive controls passed. Twenty skills and ten runners were owner-locally validated/smoke-used without global installation; three substantive tools passed accepting and rejecting fixtures.", "",
        f"Layered truth is immutable: Sylven's repository seal preserves {SYLVEN_REPOSITORY_SEAL['negatives']:,} negatives and {SYLVEN_REPOSITORY_SEAL['methods']:,} methods. Two external Sylven route-method failures produce Caelen's {ACTIVATION_BASELINE['negatives']:,}/{ACTIVATION_BASELINE['methods']:,} baseline. Caelen adds {PHASE_METHOD_COUNT} retained methods. The prepared closeout therefore preserves {SEALED_TOTALS['negatives']:,} effective negatives, {SEALED_TOTALS['methods']:,} methods, {SEALED_TOTALS['failed_witnesses']:,} failed witnesses, {SEALED_TOTALS['passing_witnesses']:,} bounded passing witnesses, {SEALED_TOTALS['open_gaps']} open gaps, and {SEALED_TOTALS['exact_gates']} exact gates. No failure or gate is erased. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.", "",
        "## Bounded domain", "", IDENTITY_BOUNDARY, "", PRACTICE_BOUNDARY, "", SCIENCE_AUTHORITY_BOUNDARY, "",
        "Current W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, and Europeana API pages supplied vocabulary and refusal constraints only. The collection adapter made zero calls and ingested zero rows. Citations establish no observation, endorsement, repair result, conformance, identity credential, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.", "",
        "## Required next-owner startup discipline", "",
        "Read this candidate through EOF, then reread the newest live activation, exact final owner packet, complete current GHC Family Index and routing precedence, roster/schema, authorization/schema, Method Flow State/schema, workflow-plan refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, D-drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, full-tools bank, web reflection, worktree rotation, and skill-creator guidance where applicable. Newer live authority governs mutable route state but never erases evidence, failures, gaps, gates, or protected boundaries.", "",
        "Work solo in a new additive D-first sparse owner lane. Keep Caelen, Sylven, siblings, shared, standby, global-source, and user lanes read-only and recoverable. Do not reset, amend, rewrite, force-push, merge, delete, reuse, mutate another owner, create/fork a task, spawn a collaboration subagent, delegate research, contact Tavian, precontact a successor, or use a substitute route.", "",
        "Preserve planning-only x1 before x2; four exact core labels; every retained failure and gate; normalized Git-blob manifests; family-current `ghc_family_*` and `build_ghc_family_*` compatibility; owner-file/word/commit ceilings; exact staged review; one attributable canonical/no-success-replay discipline; and current official or primary sources only where materially needed. Verify versions only. Do not update Codex desktop, install unrelated software, elevate, weaken host security, enable Sandbox/Hyper-V, change Windows features, mutate accounts/credentials, or reboot.", "",
        "## Forty proposal cards", "",
    ]
    for row in proposals:
        lines.extend(
            [
                f"### {row['proposal_id']} — {row['title']}", "",
                f"Expected/final bounded disposition: `{row['expected_disposition']}`. Hypothesis: {row['hypothesis']} Null or failure: {row['null_or_failure_condition']} Approval/lane: `{row['approval_class']}` / `{row['execution_lane']}`. Official-source need: {row['current_official_or_primary_source_need']} Artifact: `{row['concrete_artifacts'][0]}`. Falsifier or gate: {row['falsifier_or_acceptance_gate']} Rollback: {row['rollback_or_recovery']} Protected boundary: {row['protected_gates'][0]} This row carries no inherited completion credit, real-world observation, professional decision, affected-party acceptance, independent reproduction, or authority.", "",
            ]
        )
    lines.extend(["## Two hundred ten Method Flow cards", ""])
    for row in methods:
        lines.extend(
            [
                f"### {row['method_id']} — {row['title']}", "",
                f"Failed witness retained at zero credit: {row['failure_signature']} Bounded recovery: {row['candidate_workaround']} Recurrence guard: {row['recurrence_guard']} Rollback: {row['rollback']} The passing witness never erases the failure and establishes no independent, empirical, professional, legal, cultural, Māori-authority, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, or Stage 20 credit.", "",
            ]
        )
    lines.extend(
        [
            "## Exact-final validation truth to supply later", "",
            "The complete repository suite remains outside Caelen's owner scope. The terminal sender may report only the one owner-scoped exact-final canonical result actually produced after the final commit is pushed and fresh-live equal. A failed canonical earns zero canonical-success credit. A successful canonical must never be replayed. Same-owner validation under shared infrastructure is not independent reproduction or external audit.", "",
            "## Terminal delivery rule", "",
            "This committed candidate authorizes no send by itself. Only after Caelen's own exact final is clean, pushed, zero-divergent, fresh four-way equal, within caps, and canonically validated may Caelen refresh the newest live roster/auth state, require one unique authorized exact-title successor, immediately reread it, apply pause/redirect/rename/duplicate/standby/usage/privacy/evidence/safety/acknowledgement guards, and send at most once. Claim delivery only from a target-identifying task-message acknowledgement. Never create, fork, substitute, contact Tavian, or resend merely for clearer acknowledgement.", "",
            "`PREPARED_BY_CAELEN_MORROW = true`", "", "`SENT_BY_CAELEN_MORROW = false`", "",
            "With care, inspectability, reversibility, retained-negative discipline, and strict evidence boundaries — Caelen Morrow.",
        ]
    )
    return "\n".join(lines)


def build() -> None:
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    branch = git("branch", "--show-current").stdout.decode().strip()
    unstaged = [path.decode("utf-8") for path in git("diff", "--name-only", "-z").stdout.split(b"\0") if path]
    staged = [path.decode("utf-8") for path in git("diff", "--cached", "--name-only", "-z").stdout.split(b"\0") if path]
    untracked = [path.decode("utf-8") for path in git("ls-files", "--others", "--exclude-standard", "-z").stdout.split(b"\0") if path]
    allowed = {
        "docs/caelen-morrow/v673-v2/closeout/closeout-receipt.json",
        "docs/caelen-morrow/v673-v2/closeout/complete-incomplete-checklist.json",
        "docs/caelen-morrow/v673-v2/closeout/lifecycle-replay.json",
        "docs/caelen-morrow/v673-v2/closeout/method-flow-final.json",
        "docs/caelen-morrow/v673-v2/closeout/open-exact-gate-register.json",
        "docs/caelen-morrow/v673-v2/closeout/phase-truth.json",
        "docs/caelen-morrow/v673-v2/closeout/retained-negative-register.json",
        "docs/caelen-morrow/v673-v2/closeout/source-and-provenance.json",
        "docs/caelen-morrow/v673-v2/closeout/threat-model-final.json",
        "docs/caelen-morrow/v673-v2/closeout/wellbeing-workload-check.json",
        "docs/caelen-morrow/v673-v2/final/final-validation-prerequisites.json",
        "docs/caelen-morrow/v673-v2/handoffs/post-gate-successor-activation-candidate.md",
        "docs/caelen-morrow/v673-v2/reports/accessible-final-report.html",
        "docs/caelen-morrow/v673-v2/reports/final-integrated-overview.md",
        "docs/caelen-morrow/v673-v2/route/route-state.json",
        "docs/caelen-morrow/v673-v2/seal/content-seal.json",
        "docs/caelen-morrow/v673-v2/validation/final-test-selection.json",
        "docs/caelen-morrow/v673-v2/validation/final-owner-manifest.json",
        "docs/caelen-morrow/v673-v2/validation/final-delta-manifest.json",
        "docs/caelen-morrow/v673-v2/validation/final-staged-review.json",
        "docs/caelen-morrow/v673-v2/validation/final-staged-privacy.json",
        "scripts/build_ghc_family_caelen_morrow_v673_v2_closeout.py",
        "scripts/ghc_family_caelen_morrow_v673_v2_canonical.py",
        "tests/test_ghc_family_caelen_morrow_v673_v2_final.py",
    }
    changed = staged + unstaged + untracked
    if head != EVIDENCE or branch != BRANCH or any(path not in allowed for path in changed):
        raise SystemExit(f"closeout requires clean exact evidence on exact branch: head={head} branch={branch}")

    proposals = load("x1/proposals.json")["proposals"]
    ledger = load("x2/proposal-ledger.json")["rows"]
    method_flow = load("x2/method-flow-evidence.json")
    methods = list(method_flow["methods"])
    witnesses = list(method_flow["witnesses"])
    if Counter(row["outcome"] for row in ledger) != Counter(EXPECTED_OUTCOMES):
        raise SystemExit("outcome count drift")
    if len(methods) != EVIDENCE_METHOD_COUNT or method_flow["failed_witness_count"] != EVIDENCE_METHOD_COUNT:
        raise SystemExit("immutable evidence Method Flow count drift")
    post_evidence_methods = [
        {
            "method_id": "CM6732-M211",
            "owner": OWNER,
            "phase": PHASE,
            "title": "Bare Ruff command was absent from the closeout PowerShell path",
            "failure_signature": "The first closeout lint invocation used the bare ruff command and PowerShell reported that no matching executable, function, script, or cmdlet was available on PATH.",
            "candidate_workaround": "Use the already verified Python module entry point with python -m ruff instead of changing PATH or installing another package.",
            "recurrence_guard": "Probe the bounded module entry point for Python tools before relying on a global executable shim, and retain a missing-shim result at zero credit.",
            "rollback": "Make no environment mutation; return to the immutable evidence commit if the module entry point is unavailable.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M212",
            "owner": OWNER,
            "phase": PHASE,
            "title": "First explicit-module closeout lint found five mechanical findings",
            "failure_signature": "The first python -m ruff closeout lint found three import-order findings and two long-form regular-expression flag findings across the three new closeout files.",
            "candidate_workaround": "Apply only Ruff's five declared safe mechanical fixes, then rerun the identical explicit-module selection.",
            "recurrence_guard": "Run the exact explicit-module lint selection before closeout generation and retain the original diagnostic receipt when mechanical fixes are required.",
            "rollback": "Restore the three untracked closeout files from their pre-fix Git-independent hashes if the bounded mechanical rewrite changes semantics.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M213",
            "owner": OWNER,
            "phase": PHASE,
            "title": "Pytest collection crossed its first reporting window",
            "failure_signature": "The first exact 98-test collection process continued beyond the 30-second tool reporting window, so that wrapper returned no collection receipt.",
            "candidate_workaround": "Do not relaunch; audit the exact original process to completion and recover the declared count from the unchanged test definitions plus the already sealed 73-test x1/x2 selection.",
            "recurrence_guard": "Treat a reporting-window expiry as inconclusive, inspect the original process before any rerun, and use a nonexecuting static count when the output channel is unavailable.",
            "rollback": "Leave repository bytes unchanged and retain zero aggregate credit for the wrapper without a receipt.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M214",
            "owner": OWNER,
            "phase": PHASE,
            "title": "First static test-count projection used an invalid foreach pipeline",
            "failure_signature": "PowerShell rejected the first static test-count command because the foreach expression was piped directly, creating an empty-pipe parser error before any count was emitted.",
            "candidate_workaround": "Materialize the foreach rows in a task-local scalar array and pipe that array to JSON conversion.",
            "recurrence_guard": "Materialize PowerShell foreach output before piping it whenever a structured projection follows the loop.",
            "rollback": "Discard the failed read-only command result; no repository or environment state changed.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M215",
            "owner": OWNER,
            "phase": PHASE,
            "title": "First closeout rebuild rejected its own generated files",
            "failure_signature": "After new retained failures changed the derived counts, the first closeout rebuild stopped because its exact-evidence guard allowed only the three source files and rejected the builder's own existing generated outputs.",
            "candidate_workaround": "Extend the guard with only the exact declared builder-output paths while preserving rejection of every unrelated tracked or untracked path.",
            "recurrence_guard": "Declare both bootstrap inputs and deterministic builder outputs in a closed startup allowlist before any evidence-derived rebuild is needed.",
            "rollback": "Keep all generated files uncommitted and return to the immutable evidence parent if any unrelated path appears.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M216",
            "owner": OWNER,
            "phase": PHASE,
            "title": "Untracked-path display attempted an invalid string-to-byte conversion",
            "failure_signature": "A read-only PowerShell display wrapper passed a native command string containing NUL separators to UTF8.GetString, which expected bytes and raised a conversion error before the following plain listing succeeded.",
            "candidate_workaround": "Use the native newline listing directly for presentation and reserve byte decoding for subprocess APIs that return byte arrays.",
            "recurrence_guard": "Do not wrap PowerShell native-command string output in Encoding.GetString; choose either native text output or an actual byte-oriented process API.",
            "rollback": "Discard the failed display projection; repository and environment state were unchanged.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M217",
            "owner": OWNER,
            "phase": PHASE,
            "title": "First exact index finalizer output channel lost its running-session handle",
            "failure_signature": "The exact index finalizer crossed the first 30-second tool window and the wrapper printed only its empty output, discarding the returned running-session handle even though the original process later completed successfully.",
            "candidate_workaround": "Audit the original process and its four atomic outputs, retain the presentation fault, then preserve the session handle on any dependency-justified rerun after count-bearing inputs change.",
            "recurrence_guard": "When a bounded command may yield, always surface both output and session identifier before deciding whether any rerun is needed.",
            "rollback": "Do not replay merely for presentation; accept only atomic files from the original process and rerun solely when an input dependency changes.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M218",
            "owner": OWNER,
            "phase": PHASE,
            "title": "Python-module Pyright entry point was unavailable",
            "failure_signature": "After mypy passed the three closeout files, python -m pyright failed before analysis because the Python environment contains no pyright module.",
            "candidate_workaround": "Use the already verified npm-installed Pyright CLI from the D-drive global prefix without installing or updating anything.",
            "recurrence_guard": "Distinguish Python-module and npm-CLI entry points during version probes and invoke the installed provider explicitly.",
            "rollback": "Make no package or PATH mutation; retain the module-entry failure at zero credit.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M219",
            "owner": OWNER,
            "phase": PHASE,
            "title": "First npm Pyright cold-start wrapper lost its session handle",
            "failure_signature": "The first npm Pyright analysis crossed a 30-second cold-start reporting window and the wrapper failed to surface its returned session handle, leaving the result inconclusive.",
            "candidate_workaround": "Audit the exact original Node process to exit, then rerun only the inconclusive Pyright check with the running-session result preserved.",
            "recurrence_guard": "Preserve session identifiers for Node-based static analyzers whose first startup can exceed the initial reporting window.",
            "rollback": "Award zero credit to the inconclusive wrapper and do not rerun mypy or any already successful dependency.",
            "status": "preferred",
        },
        {
            "method_id": "CM6732-M220",
            "owner": OWNER,
            "phase": PHASE,
            "title": "Cap audit wrapper outlived its final optional diff-stat presentation",
            "failure_signature": "The cap and stale-label audit emitted all required scalar results, but its appended optional git diff stat extended past the 30-second wrapper window and the session handle was not surfaced.",
            "candidate_workaround": "Retain the scalar cap and stale-label receipt, audit the original process to exit, and omit the nonessential duplicate diff-stat presentation.",
            "recurrence_guard": "Keep required scalar audits separate from potentially slow human-readable diff summaries and preserve any yielded session handle.",
            "rollback": "Do not replay the successful scalar audit; discard only the missing optional presentation.",
            "status": "preferred",
        },
    ]
    post_evidence_witnesses = [
        {"witness_id": "CM6732-M211-F", "method_id": "CM6732-M211", "kind": "failed", "observed": "PowerShell rejected the bare ruff command before lint execution because no matching command was available on PATH.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M211-P", "method_id": "CM6732-M211", "kind": "passing", "observed": "python -m ruff --version resolved the already installed Ruff 0.16.4 module without installing or changing any package.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M212-F", "method_id": "CM6732-M212", "kind": "failed", "observed": "The first explicit-module lint returned five safe-fixable findings: three import-order and two regular-expression flag aliases.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M212-P", "method_id": "CM6732-M212", "kind": "passing", "observed": "The identical explicit-module closeout lint passes after only the five declared Ruff mechanical fixes.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M213-F", "method_id": "CM6732-M213", "kind": "failed", "observed": "The first exact collection wrapper crossed its 30-second reporting window and returned no test-count receipt while the original Python process remained active.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M213-P", "method_id": "CM6732-M213", "kind": "passing", "observed": "The original process was audited to a later exited state without relaunch, and static definitions confirm 20 x1 functions, the sealed 53-case x2 selection, and 25 final functions for 98 total tests.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M214-F", "method_id": "CM6732-M214", "kind": "failed", "observed": "PowerShell rejected the direct foreach-to-pipeline expression with an empty-pipe parser error before producing a count.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M214-P", "method_id": "CM6732-M214", "kind": "passing", "observed": "The corrected scalar-array projection emitted 20 x1, 34 x2, and 25 final test functions while identifying the single x2 parametrization that expands the sealed x1/x2 selection to 73 cases.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M215-F", "method_id": "CM6732-M215", "kind": "failed", "observed": "The first count-adjusted closeout rebuild stopped before writing because the startup guard rejected its own prior generated outputs as unexpected untracked files.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M215-P", "method_id": "CM6732-M215", "kind": "passing", "observed": "The corrected closed allowlist accepts only the exact seventeen deterministic builder outputs and three source files while continuing to reject unrelated paths.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M216-F", "method_id": "CM6732-M216", "kind": "failed", "observed": "UTF8.GetString rejected PowerShell's already-decoded NUL-separated native-command string because it was not a byte array.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M216-P", "method_id": "CM6732-M216", "kind": "passing", "observed": "The immediately following native newline listing emitted the exact twenty untracked paths without conversion or repository mutation.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M217-F", "method_id": "CM6732-M217", "kind": "failed", "observed": "The first exact index finalizer wrapper crossed its reporting window and discarded the live session handle, returning no direct completion receipt.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M217-P", "method_id": "CM6732-M217", "kind": "passing", "observed": "The original process was audited to exit and its four atomic outputs parsed: 139 owner entries, 20 delta entries, a staged review, and zero confirmed five-class privacy hits.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M218-F", "method_id": "CM6732-M218", "kind": "failed", "observed": "python -m pyright returned No module named pyright after the paired mypy selection had passed.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M218-P", "method_id": "CM6732-M218", "kind": "passing", "observed": "The existing D-prefix npm CLI resolved as Pyright 1.1.413 without install, update, or environment mutation.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M219-F", "method_id": "CM6732-M219", "kind": "failed", "observed": "The first npm Pyright cold-start wrapper exceeded 30 seconds and lost its session handle, so its analysis result remained inconclusive at zero credit.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M219-P", "method_id": "CM6732-M219", "kind": "passing", "observed": "The isolated same-file Pyright recovery completed with 0 errors, 0 warnings, and 0 informations; no successful mypy or other component was replayed.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M220-F", "method_id": "CM6732-M220", "kind": "failed", "observed": "The cap/stale-label wrapper crossed its reporting window only while producing an optional diff-stat summary and did not surface a session handle.", "credit": 0, "retained": True},
        {"witness_id": "CM6732-M220-P", "method_id": "CM6732-M220", "kind": "passing", "observed": "The already-emitted scalar receipt proves 143 final owner files, a 24,589-word maximum document, zero stale-label matches, 24 staged paths, and zero untracked paths; the original process was later absent.", "credit": 0, "retained": True},
    ]
    methods.extend(post_evidence_methods)
    witnesses.extend(post_evidence_witnesses)
    if len(methods) != PHASE_METHOD_COUNT or len(witnesses) != 2 * PHASE_METHOD_COUNT:
        raise SystemExit("final Method Flow count drift")

    phase_truth = {
        "schema": "ghc.family.phase-truth.v9", "owner": OWNER, "phase": PHASE,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "final": None, "final_state": "PENDING_COMBINED_CLOSEOUT_SEAL_COMMIT",
        "declared_source_chain": DECLARED_SOURCE_CHAIN, "declared_result_chain": DECLARED_RESULT_CHAIN,
        "proposal_count": 40, "outcome_counts": EXPECTED_OUTCOMES,
        "real_people": 0, "real_instruments": 0, "real_rows": 0, "network_calls": 0,
        "keys_or_proofs": 0, "professional_actions": 0, "authority_acts": 0,
        "repository_layers": {"sylven_repository_seal": SYLVEN_REPOSITORY_SEAL, "sylven_external_overlay": SYLVEN_EXTERNAL_OVERLAY, "caelen_activation_baseline": ACTIVATION_BASELINE, "caelen_phase_addition": {"negatives": PHASE_METHOD_COUNT, "methods": PHASE_METHOD_COUNT, "failed_witnesses": PHASE_METHOD_COUNT, "passing_witnesses": PHASE_METHOD_COUNT, "open_gaps": 2, "exact_gates": 2}, "caelen_sealed_totals": SEALED_TOTALS},
        "validation_state": "PENDING_EXTERNAL_EXACT_FINAL_CANONICAL",
        "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/phase-truth.json", phase_truth)
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v8", "owner": OWNER, "phase": PHASE,
            "inherited_repository_seal": SYLVEN_REPOSITORY_SEAL, "inherited_external_overlay": SYLVEN_EXTERNAL_OVERLAY,
            "activation_baseline": ACTIVATION_BASELINE, "phase_negative_count": PHASE_METHOD_COUNT,
            "effective_negative_count": SEALED_TOTALS["negatives"],
            "phase_rows": [{"method_id": row["method_id"], "title": row["title"], "failure_signature": row["failure_signature"], "retained": True, "credit": 0, "recurrence_guard": row["recurrence_guard"]} for row in methods],
            "boundary": "Every current failed witness is retained at zero credit; inherited counts remain layered and are not silently rewritten.",
        },
    )
    write_json(
        "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.method-flow.final.v8", "owner": OWNER, "phase": PHASE,
            "phase_method_count": PHASE_METHOD_COUNT, "phase_failed_witness_count": PHASE_METHOD_COUNT,
            "phase_passing_witness_count": PHASE_METHOD_COUNT, "methods": methods,
            "witnesses": witnesses, "sealed_totals": SEALED_TOTALS,
            "boundary": "Passing recovery never erases failure or establishes independent, professional, empirical, authority, production, or Stage 20 evidence.",
        },
    )
    gate_rows = [
        {"gate_id": "CM6732-GAP-001", "proposal_id": "CM6732-N037", "kind": "open_gap", "state": "open", "reason": "Transport-disabled public collection adapter made zero calls and ingested zero rows."},
        {"gate_id": "CM6732-GAP-002", "proposal_id": "CM6732-N038", "kind": "open_gap", "state": "open", "reason": "Current official accordion-source capability and real governed evidence remain absent."},
        {"gate_id": "CM6732-GATE-001", "proposal_id": "CM6732-N031", "kind": "exact_gate", "state": "unexecuted", "reason": "Remedy and affected-party acceptance require exact authority and evidence."},
        {"gate_id": "CM6732-GATE-002", "proposal_id": "CM6732-N032", "kind": "exact_gate", "state": "unexecuted", "reason": "Legal, cultural, tangata whenua, iwi, hapū, and Māori authority are absent."},
    ]
    write_json("closeout/open-exact-gate-register.json", {"schema": "ghc.family.open-exact-gate-register.v7", "owner": OWNER, "phase": PHASE, "inherited_open_gaps": 293, "new_open_gaps": 2, "effective_open_gaps": 295, "inherited_exact_gates": 286, "new_exact_gates": 2, "effective_exact_gates": 288, "rows": gate_rows, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/lifecycle-replay.json", {"schema": "ghc.family.lifecycle-replay.v5", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE, "expected_phase_commits": 3, "expected_merges": 0, "x1_planning_only": True, "evidence_has_no_closeout": True, "final_pending": True})
    write_json("closeout/source-and-provenance.json", {"schema": "ghc.family.final-source-provenance.v6", "owner": OWNER, "phase": PHASE, "source_branch": "codex/GHC-Family/sylven-arc-v673-v1-full-tools", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "source_external_digests": {"canonical_payload": "7efb155e26c4fc44aa6243fc71ef2dd8efd3d5ef0032e44e37c67c0db3bde7dd", "canonical_receipt": "59087cd1e6164784f04f5f1690798a75db56d6449caaa96a7fc748c15292c7df", "operational_overlay": "28dc8618c45c5e4e2286568b0c48363041bfad0f5bc119440396584c2f92c62a"}, "external_digest_file_location_materialized": False, "source_validation_replayed": False, "boundary": "Live supplied digests retained; no missing receipt path invented."})
    write_json("closeout/complete-incomplete-checklist.json", {"schema": "ghc.family.complete-incomplete.v6", "owner": OWNER, "phase": PHASE, "complete": ["read-first packet and skills", "source re-verification", "unique D-first sparse lane", "planning-only x1", "x1 push and fresh equality", "bounded x2", "evidence push and fresh equality", "forty outcome ledger", "failure retention", "skills/runners/tools", "official-source reflection", "flashcards", "manifests", "accessible static report preparation", "closeout and seal preparation"], "incomplete": ["exact final commit", "external one-shot canonical", "manual browser evaluation", "assistive-technology evaluation", "Māori-language evaluation", "cognitive-accessibility evaluation", "affected-user evaluation", "real-world evidence", "professional validation", "legal/cultural/Māori authority", "independent reproduction", "production/deployment", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/wellbeing-workload-check.json", {"schema": "ghc.family.wellbeing-workload.v5", "owner": OWNER, "phase": PHASE, "relational_only": True, "human_workload_claim": False, "context_management": ["bounded file count", "modular handoff sections", "single-process waits", "no duplicate commit/push/canonical", "retained failures"], "pause_right_preserved": True, "rename_redirect_stop_right_preserved": True, "boundary": "No consciousness, emotion, clinical, employment, or worker-status claim; operational pacing evidence only."})
    write_json("closeout/threat-model-final.json", {"schema": "ghc.family.threat-model-final.v4", "owner": OWNER, "phase": PHASE, "controls_passed": ["synthetic-only schema", "zero-row and zero-network assertions", "closed vocabularies", "authority quarantine", "x1-before-x2", "exact staged manifests", "five-class privacy scan", "prepared-not-sent route", "one-shot canonical guard"], "residual_gates": ["professional competence", "safety", "rights and custody", "privacy/accessibility completeness", "legal/cultural interpretation", "affected-party acceptance", "Māori authority", "independent reproduction", "production/deployment", "Stage 20"], "risk_state": "bounded_not_eliminated"})
    write_json("route/route-state.json", {"schema": "ghc.family.route-state.v8", "owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT", "recipient_selected": False, "recipient": None, "historical_cycle_hint": "Eiren Kestrel; must be freshly revalidated and not inferred", "continuation_through": "v675-v8", "standby_record": "Tavian Sol", "standby_eligible": False, "message_count": 0, "acknowledgement": False, "duplicate_guard_pending": True, "terminal_gate_pending": True})
    write_json("final/final-validation-prerequisites.json", {"schema": "ghc.family.final-validation-prerequisites.v6", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE, "expected_phase_commits": 3, "expected_merges": 0, "expected_final_parent_count": 1, "expected_tests": EXPECTED_FINAL_TESTS, "canonical_runs_allowed": 1, "canonical_runs_completed": 0, "success_replay_allowed": False, "full_repository_suite_authorized": False, "required_preconditions": ["closeout staged review", "final owner manifest", "final delta manifest", "five-class privacy scan", "clean pushed final", "0/0 divergence", "fresh four-way equality"], "state": "PENDING_FINAL_COMMIT"})
    write_json("validation/final-test-selection.json", {"schema": "ghc.family.final-test-selection.v4", "owner": OWNER, "phase": PHASE, "test_files": ["tests/test_ghc_family_caelen_morrow_v673_v2_x1.py", "tests/test_ghc_family_caelen_morrow_v673_v2_x2.py", "tests/test_ghc_family_caelen_morrow_v673_v2_final.py"], "expected_total": EXPECTED_FINAL_TESTS, "lifecycle_git_tree_checks": 4, "selection_scope": "owner-self-scoped dependency-closed only", "full_repository_suite": False})
    write_text("reports/final-integrated-overview.md", final_overview(proposals, methods))
    write_text("reports/accessible-final-report.html", accessible_report(proposals))
    candidate = handoff_candidate(proposals, methods)
    candidate_words = len(candidate.split())
    if not 10000 <= candidate_words <= 100000:
        raise SystemExit(f"handoff candidate word count outside ceiling/floor: {candidate_words}")
    write_text("handoffs/post-gate-successor-activation-candidate.md", candidate)

    seal_paths = [
        "docs/caelen-morrow/v673-v2/x1/proposals.json",
        "docs/caelen-morrow/v673-v2/x1/semantic-neighbor-audit.json",
        "docs/caelen-morrow/v673-v2/x2/proposal-ledger.json",
        "docs/caelen-morrow/v673-v2/x2/method-flow-evidence.json",
        "docs/caelen-morrow/v673-v2/closeout/phase-truth.json",
        "docs/caelen-morrow/v673-v2/closeout/retained-negative-register.json",
        "docs/caelen-morrow/v673-v2/closeout/open-exact-gate-register.json",
        "docs/caelen-morrow/v673-v2/reports/final-integrated-overview.md",
        "docs/caelen-morrow/v673-v2/handoffs/post-gate-successor-activation-candidate.md",
    ]
    seal_entries = [hash_file(path) for path in seal_paths]
    write_json("seal/content-seal.json", {"schema": "ghc.family.content-seal.v6", "owner": OWNER, "phase": PHASE, "entry_count": len(seal_entries), "entries": seal_entries, "normalized_lf": True, "state": "COMMIT_CANDIDATE", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/closeout-receipt.json", {"schema": "ghc.family.closeout-receipt.v7", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "outcome_counts": EXPECTED_OUTCOMES, "phase_methods": PHASE_METHOD_COUNT, "sealed_totals": SEALED_TOTALS, "handoff_candidate_words": candidate_words, "content_seal_entries": len(seal_entries), "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL", "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


def index_paths() -> list[str]:
    paths = [path.decode("utf-8") for path in git("ls-files", "-z").stdout.split(b"\0") if path]
    owner_prefix = "docs/caelen-morrow/v673-v2/"
    code_pattern = re.compile(r"^(?:scripts/(?:build_ghc_family_caelen_morrow_v673_v2_[a-z0-9_]+|ghc_family_caelen_morrow_v673_v2_[a-z0-9_]+)\.py|tests/test_ghc_family_caelen_morrow_v673_v2_[a-z0-9_]+\.py)$")
    return sorted(path for path in paths if path.startswith(owner_prefix) or code_pattern.fullmatch(path))


def batch_index_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderr = process.communicate(input=("\n".join(f":{path}" for path in paths) + "\n").encode("utf-8"), timeout=300)
    if process.returncode:
        raise SystemExit(stderr.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("utf-8", errors="strict").strip().split()
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
        "docs/caelen-morrow/v673-v2/validation/final-owner-manifest.json",
        "docs/caelen-morrow/v673-v2/validation/final-delta-manifest.json",
        "docs/caelen-morrow/v673-v2/validation/final-staged-review.json",
        "docs/caelen-morrow/v673-v2/validation/final-staged-privacy.json",
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
    write_json("validation/final-staged-privacy.json", {"schema": "ghc.family.five-class-privacy-scan.v5", "owner": OWNER, "phase": PHASE, "class_count": 5, "scanned_file_count": len(manifest_paths), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": 0, "boundary": "Scanner/test definitions are candidates; every other match fails closed. Complete privacy assurance is not claimed."})
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
