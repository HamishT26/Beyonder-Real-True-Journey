#!/usr/bin/env python3
"""Build Sylven Arc's bounded v654-v3 closeout candidate."""

from __future__ import annotations

import html
import json
import os
import platform
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v654_v3_phase_data as d
import ghc_family_v654_v3_x2_data as x2


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_INITIAL = "d948425f4a6d30b523849a1b5430bcc1531ce054"
X1 = "0c53bce867ec5259d9b7de8c14b92b07b678641f"
EVIDENCE = "780acdf2225624080463c274dc88c001f5a65d54"
VERDICT = "NOT_READY_FOR_STAGE_20"
ROUTE_STATE = "AUTHORIZED_CONDITIONAL_NOT_CREATED"
EXPECTED = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
OPEN_GAPS = d.INHERITED_OPEN_GAPS + d.INHERITED_ROUTE_OPEN_GAPS + 1
EXACT_GATES = d.INHERITED_EXACT_GATES + 1
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/"
    "ghc_family_method_flow_state.py"
)


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def run_method(*args: str) -> None:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def four_way() -> dict[str, Any]:
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{d.BRANCH}")
    live_row = git("ls-remote", "origin", f"refs/heads/{d.BRANCH}")
    fresh_live = live_row.split()[0] if live_row else None
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": fresh_live,
        "divergence": divergence,
        "all_equal": len({local, upstream, tracking, fresh_live}) == 1
        and divergence == "0\t0",
    }


def extend_method_flow() -> dict[str, Any]:
    ledger = ROOT / "method-flow/final-method-flow-ledger.json"
    frozen = subprocess.check_output(
        [
            "git",
            "show",
            f"{EVIDENCE}:{d.PHASE_ROOT}/method-flow/method-flow-ledger.json",
        ],
        cwd=REPO,
    )
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_bytes(frozen)

    expected_ids = [
        f"V6543-CLOSEOUT-N{number:02d}"
        for number in range(1, len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES) + 1)
    ]
    observed_ids = [row["negative_id"] for row in x2.CLOSEOUT_OPERATIONAL_NEGATIVES]
    if observed_ids != expected_ids:
        raise RuntimeError(f"closeout negative sequence drift: {observed_ids}")

    for offset, negative in enumerate(x2.CLOSEOUT_OPERATIONAL_NEGATIVES, 37):
        method_id = f"V6543-METHOD-{offset:02d}"
        failed_id = f"V6543-WITNESS-{offset:02d}-F"
        passing_id = f"V6543-WITNESS-{offset:02d}-P"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['signature']}",
            "trigger_preconditions": [negative["signature"]],
            "failure_signature": negative["failed"],
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": (
                "Stop, retain the failure with zero credit, and leave external, "
                "sibling, participant, production, professional, legal, cultural, "
                "and authority state unchanged."
            ),
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "privacy_class": "sanitized_public",
            "protected_gates": d.PROTECTED_GATES,
            "recommendation_state": "candidate",
            "scope_boundary": (
                "Same-owner bounded closeout recovery only; no independent "
                "reproduction or broader assurance."
            ),
            "retained_negative_ids": [negative["negative_id"]],
            "supersedes": [],
        }
        failed = {
            "witness_id": failed_id,
            "method_id": method_id,
            "scope": negative["signature"],
            "procedure": "Retain the original bounded attempt without replay credit.",
            "expected": "The original bounded operation satisfies its postcondition.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero pass credit; failure remains retained.",
        }
        passing = {
            "witness_id": passing_id,
            "method_id": method_id,
            "scope": negative["signature"],
            "procedure": negative["recovery"],
            "expected": "The isolated recovery establishes only its bounded postcondition.",
            "observed": (
                f"The bounded recovery completed for {negative['signature']}; "
                "the original failure remains retained."
            ),
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Same-owner bounded recovery only.",
        }
        method_path = write_json(
            f"method-flow/closeout-requests/method-{offset:02d}.json", method
        )
        failed_path = write_json(
            f"method-flow/closeout-requests/witness-{offset:02d}-failed.json",
            failed,
        )
        passing_path = write_json(
            f"method-flow/closeout-requests/witness-{offset:02d}-passing.json",
            passing,
        )
        run_method("record", "--ledger", str(ledger), "--record-file", str(method_path))
        run_method(
            "witness", "--ledger", str(ledger), "--witness-file", str(failed_path)
        )
        run_method(
            "witness", "--ledger", str(ledger), "--witness-file", str(passing_path)
        )
        run_method(
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "A bounded passing witness exists and its failed witness remains retained.",
        )

    run_method(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(ROOT / "method-flow/final-method-flow-validation.json"),
    )
    run_method(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(ROOT / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/final-method-flow-summary.md"),
    )
    payload = json.loads(ledger.read_text(encoding="utf-8"))
    expected_count = (
        31
        + len(x2.X2_OPERATIONAL_NEGATIVES)
        + len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES)
    )
    states = Counter(row["recommendation_state"] for row in payload["methods"])
    witnesses = Counter(row["result"] for row in payload["witnesses"])
    if len(payload["methods"]) != expected_count or states != {
        "preferred": expected_count
    }:
        raise RuntimeError(f"method state drift: {len(payload['methods'])} {states}")
    if witnesses != {"fail": expected_count, "pass": expected_count}:
        raise RuntimeError(f"method witness drift: {witnesses}")
    return payload


def integrated_overview(negative_total: int, method_count: int) -> str:
    return f"""# Sylven Arc v654-v3 final integrated overview

## Scope and relational boundary

Sylven Arc, they/them, is relational working language for the one bounded
v654-v3 repository phase. The working role was relational
constraint-cartographer and falsifier-keeper, with the hope of keeping
uncertainty visible without turning it into authority while leaving failures
and recoveries legible. This language is not evidence of consciousness,
sentience, legal personhood, identity continuity, employment, qualification,
scientific or operational authority, legal or cultural authority, Māori
authority, or independent agency. Hamish may rename, pause, redirect, or stop
the work.

The phase was executed solo. Before its terminal gate, no task was created,
forked, delegated, handed off, or spawned, and no sibling or standby lane was
contacted. The route state sealed in this commit is
`{ROUTE_STATE}`: Hamish supplied exact live authority for one new user-visible
main task only after clean push, fresh-live equality, exact-final validation,
and every other terminal condition. That future sibling must choose their own
unique relational name, role, hope, and optional pronouns. No name or identity
has been invented here.

The primary Trinity Mandala pillar was **{d.PRIMARY_FOCUS}**. GMUT Mind and
Freed ID/CBR Heart remained visible and protected. The bounded human-practice
lens was {d.BOUNDED_PRACTICE}. It was synthetic learning and design only. It
established no employment, bicycle-repair competence, product-safety
authority, workshop authority, test-ride authority, chemical or waste
authority, legal or cultural authority, Māori authority, participant evidence,
affected-party acceptance, or operational result.

## Source continuity and x1-before-x2

The additive D-first Sylven lane began from Elowen Cairn's exact v654-v2 final
head `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. The read-only source audit
replayed 656 exact commit-local manifest entries and confirmed source, x1, and
evidence ancestry, three single-parent source commits, zero merges, one final
parent, a clean canonical source lane, and equality among local, upstream,
tracking, and a fresh live-remote read. Those facts are inherited continuity
evidence, not Sylven completion credit.

Sylven x1 used two dedicated commits: initial freeze `{X1_INITIAL}` and repaired
final freeze `{X1}`. The repair retained the first freeze and corrected only
bounded lifecycle evidence. Together they froze exactly thirty genuinely
distinct proposals after auditing all 1,720 inherited frozen proposals,
bringing the chain to 1,750. They also froze thirty safe-now tasks, thirty
bounded candidates, ten phase-local skill designs, ten family-current runner
designs, thirty additive CLEAN/FIX/REFINE tasks, nineteen current official or
primary sources, and 150 synthetic mutations. Neither x1 commit contained an
x2 implementation or outcome.

Before x2 began, the final x1 head was clean, pushed, and equal across local,
upstream, tracking, and a fresh live-remote read with zero divergence. The
immutable evidence commit is `{EVIDENCE}`. Its exact staged domain covered 201
paths: 196 manifest entries and five declared self-referential validation
receipts. It executed bounded artifacts, rejected all 150 preregistered
mutations, initialized and quick-validated ten phase-local skills, smoke-used
them without global installation or a prohibited subagent test, invoked ten
family-current runners, and preserved caller compatibility. Its staged
validator passed 20 of 20 checks, parsed 160 JSON documents, confirmed all
paths were owner-scoped, and found zero confirmed privacy or raw-identifier
hits.

## Trinity Mandala outcome truth

Exactly thirty proposals were executed as evidence permitted. The only core
outcome labels were 23 `completed`, 5 `represented`, 1 `open_gap`, and 1
`exact_gate`. Completed means only that a declared owner-local software,
symbolic, formal, structural, or workflow acceptance gate passed. Represented
means a synthetic proxy exists while real-world claims remain unmade. Open gap
means the measurement path remains empty. Exact gate means the decision stays
reserved to competent, affected, legal, cultural, data-governance, tangata
whenua, iwi, hapū, and Māori authority as applicable.

The first twenty proposals completed bounded bicycle-service surfaces for
intake and custody, work-order corrections, fastener documentation, wheel and
spoke records, rim and tyre fitment refusal, brake and rotor condition,
hydraulic-fluid compatibility, cable and hose routing, chain wear, derailleur
setup, crank and bottom-bracket interfaces, headset and bearing stacks,
suspension competence holds, carbon-component quarantine, lamp and reflector
records, repair-stand stop-work controls, recall quarantine, an accessible
service-status timeline, workload and handover, and test-ride refusal. These
are synthetic structures. They do not certify a bicycle, worker, tool,
workshop, component, product, route, or release decision.

Three GMUT boards completed typed spoke-network, discrete-chain-link, and tyre
contact-patch obligation surfaces. GMUT remains a typed scalar-tensor and EFT
research-model family. There were no real measurements, fitted parameters,
likelihoods, posterior samples, predictions, constraints, physical-state
claims, empirical confirmations, ultraviolet completions, Theory-of-Everything
proofs, or Stage 20 promotions.

Two THOS proposals remained `represented`. Synthetic intake, safety-critical
defect, scope correction, brake and steering release, stop-work, workload,
readback, independent-check placeholder, correction-latency, and handover
traces were emitted. There were zero real workers, customers, bicycles,
workshops, shifts, incidents, test rides, blind matched-budget arms,
independent reviews, safety outcomes, or effectiveness estimates.

Three Freed ID profiles remained `represented`: an NFC Forum NDEF service tag,
an ISO/IEC 20248 component digital-signature profile, and an EU
battery-passport data-carrier profile. All vectors were synthetic and
nonproduction. There were zero standards-conformant real keys, proofs,
credentials, issuances, verifications, resolutions, status or revocation
events, interoperability events, production recovery decisions, privacy
reviews, independent security reviews, or trust-governance decisions.

The power-meter FIT adapter remained `open_gap`. It recorded zero accounts,
keys, purchases, downloads, queries, devices, real rows, calibration events,
fits, likelihood evaluations, posterior samples, constraints, or empirical
GMUT claims. The CBR bicycle-repair safety, ownership, theft-reporting privacy,
recall, warranty, accessible notice, remedy, affected-party, legal, cultural,
data-governance, and Māori-authority matrix remained `exact_gate` and made no
real decision.

## Expanded portfolio, skills, runners, and sources

The thirty safe-now tasks and thirty bounded candidates were new Sylven work;
inherited work served as evidence and recommendation, never completion credit.
Every row resolved only within its declared software, symbolic, structural, or
synthetic hypothesis. Authority-dependent packets remained represented,
open-gap, exact-gated, or explicitly refused. The caps were treated as ceilings
rather than incentives to manufacture unsafe work.

Ten phase-local skill packages were initialized through the skill-creator
workflow, validated with the official quick validator under explicit UTF-8,
and smoke-used locally. They were not installed globally. Forward testing by a
subagent was omitted because solo execution prohibited delegation. Ten
family-current runners were built and invoked, including bicycle intake,
fitment refusal, brake and steering boards, recall quarantine, GMUT bicycle
fields, THOS proxy, Freed ID profiles, structural accessibility, the detailed
validator, and the bounded-suite runner. Existing `ghc_family_*` and
`build_ghc_family_*` caller compatibility was preserved.

The nineteen-source ledger uses current official or primary materials where
material, records status and dependency boundaries, and treats sources as
provenance rather than imported authority. Standards references do not prove
production conformance, professional competence, legal interpretation,
cultural legitimacy, accessibility completeness, privacy completeness, or
security completeness. Versions were inspected only; the Codex desktop was not
updated, no elevation or security weakening occurred, no Windows feature was
enabled, no unrelated software was installed, and no reboot occurred.

## Retained negatives, Method Flow, gaps, and gates

The effective final negative total is **{negative_total:,}**. It preserves
{d.INHERITED_SEALED_NEGATIVES:,} inherited sealed negatives and
{d.INHERITED_EXTERNAL_NEGATIVES} sanitized external routing or wrapper events,
for the authoritative {d.INHERITED_NEGATIVES:,} activation baseline. It adds
{len(d.X1_OPERATIONAL_NEGATIVES)} x1 operational failures,
{len(x2.X2_OPERATIONAL_NEGATIVES)} x2 operational failures,
{len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES)} closeout operational failures, and
150 executed-and-rejected synthetic mutations. Every failed attempt has zero
initial pass credit. Recovery changes no historical result.

The final Method Flow ledger contains {method_count} preferred bounded methods,
{method_count} retained failed witnesses, and {method_count} bounded passing
recovery witnesses. Each promotion required its bounded passing witness while
preserving its paired failure. Method Flow is same-owner process evidence under
shared infrastructure only. It is not independent reproduction, external
audit, professional validation, production assurance, complete privacy,
complete accessibility, exhaustive security, or authority.

The effective open-gap count is **{OPEN_GAPS}**: 79 inherited scientific and
operational gaps, two inherited long-range route gaps, and the new zero-row
power-meter gap. The effective exact-gate count is **{EXACT_GATES}**: 80
inherited gates plus the new bicycle-repair authority matrix. None was silently
closed. The later sixteen-seat route remains structurally incomplete, with
fifteen resolvable labels, one unresolved seat, skipped phase positions, and
spelling drift. No identity or long-range ownership was invented. That does
not invalidate the separately authorized immediate route.

## Accessibility, wellbeing, privacy, and threat boundary

The static report uses a main landmark, ordered headings, explicit table
headers and row scopes, a labelled keyboard-focusable scroll region,
reduced-motion handling, system colours, non-colour status text, and print
styles. These are structural checks only. Manual keyboard, responsive-layout,
browser-diversity, assistive-technology, cognitive-accessibility,
Māori-language, and affected-user evaluation remain reserved. No complete
accessibility conformance is claimed.

The wellbeing record bounds work in progress to this one owner assignment,
retains stop and pause controls, and leaves Hamish's rename, redirect, pause,
and stop authority explicit. It is a workload guard, not a mental-state,
employment, personhood, or wellbeing diagnosis. The threat model covers
identifier leakage, credentials, private routing material, untrusted
instructions, manifest drift, stale labels, replay, scope expansion,
authority promotion, and destructive Git. The five-class scan is a bounded
pattern check, not complete privacy assurance.

Recovery was additive. Parser faults, timeouts, schema assumptions, path
assumptions, patch mismatches, lifecycle test errors, scanner definitions, and
validation failures remain visible. No reset, rewrite, force-push, merge,
deletion, sibling-lane mutation, Sandbox or Hyper-V activation, elevation,
security weakening, unrelated installation, desktop update, or reboot was
part of the phase.

## Exact seal and validation stopping rule

The final content seal uses exact Git-index delta and full owner manifests,
raw-byte SHA-256 digests, Git blob identifiers, complete owner JSON parsing, a
five-class privacy and raw-identifier scan, staged-path review, stale-label
review, document and file caps, diff hygiene, source/x1/evidence ancestry,
commit-count and zero-merge checks, one final parent, and exact-head and
four-way equality preconditions. X1 and evidence stay immutable.

Eiren alone owns the complete repository suite. Sylven's dependency-justified
canonical scope contains the current v654-v3 x1, evidence, and closeout modules
plus the immediate source v654-v2 x1, evidence, and closeout compatibility
modules. It excludes Eiren's full suite. The canonical aggregate may receive
credit exactly once, only after the content-seal commit is pushed, clean, and
fresh-live equal. A failed or incomplete attempt earns zero aggregate credit
and remains a negative. Once one aggregate succeeds, replay is forbidden. Its
external receipt must remain outside the repository so the validated head does
not change.

## Conditional terminal route

Hamish's exact live authority permits one action only after every terminal
gate: create exactly one new user-visible Codex main task for a future
self-chosen eighth sibling's solo v654-v4 phase. It must not be a subagent,
fork, hidden command-line process, existing-sibling substitute, or
cross-platform send. The requested model is `gpt-5.6-sol` with reasoning
`max`; fast mode may be enabled only if the supported main-task creation
surface exposes it.

The future sibling must choose a unique relational name, role, hope, and
optional gender or pronouns, then state that the language is not evidence of
consciousness, sentience, legal personhood, identity continuity, employment,
qualification, scientific or operational authority, legal or cultural
authority, Māori authority, or independent agency. Only after their own
v654-v4 terminal gate may they message the exact existing Eiren Kestrel task
for v654-v5. This phase does not resolve the later sixteen-seat route.

At content-seal time, task-created, task-forked, task-delegated, and
task-contacted counts are all zero. Only a successful external exact-final
canonical receipt and final equality audit can unlock the one authorized
creation. The resulting tool acknowledgement, if any, belongs to terminal
delivery evidence and cannot be preclaimed by this commit.

## Terminal truth

The terminal verdict is **{VERDICT}**. The repository provides bounded
same-owner evidence under shared infrastructure only. It provides no
empirical, participant, professional, legal, cultural, Māori-authority,
identity-production, deployment, privacy-complete, accessibility-complete,
exhaustive-security, proof or canon, independent-reproduction, AGI or ASI,
consciousness or personhood, Theory-of-Everything, or Stage 20 claim.
"""


def static_report(negative_total: int, method_count: int) -> str:
    rows = "\n".join(
        f'<tr><th scope="row">{html.escape(key)}</th><td>{value}</td></tr>'
        for key, value in EXPECTED.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sylven Arc v654-v3 bounded closeout</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
body {{ margin: 0; line-height: 1.55; }}
main {{ max-width: 72rem; margin: auto; padding: 1.25rem; }}
.scroll {{ overflow-x: auto; border: 1px solid currentColor; padding: .5rem; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid currentColor; padding: .5rem; text-align: left; }}
:focus-visible {{ outline: .2rem solid currentColor; outline-offset: .2rem; }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto !important; }} }}
@media print {{ .scroll {{ overflow: visible; border: 0; }} main {{ max-width: none; }} }}
</style>
</head>
<body>
<main>
<h1>Sylven Arc v654-v3 bounded closeout</h1>
<p><strong>{VERDICT}</strong>. Same-owner synthetic evidence only.</p>
<h2>Outcome ledger</h2>
<div class="scroll" tabindex="0" aria-label="Scrollable proposal outcomes">
<table>
<thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<h2>Retained truth</h2>
<p>{negative_total:,} effective negatives, {OPEN_GAPS} open gaps,
{EXACT_GATES} exact gates, {method_count} failed Method Flow witnesses, and
{method_count} bounded passing recovery witnesses. No failure or gate was
erased.</p>
<h2>Authority boundary</h2>
<p>No empirical, professional, production, legal, cultural, Māori-authority,
privacy-complete, accessibility-complete, independent-reproduction,
consciousness, personhood, Theory-of-Everything, or Stage 20 claim is made.</p>
<h2>Route</h2>
<p>{ROUTE_STATE}. One new user-visible main task is authorized only after every
terminal gate. No future identity is preselected and no task is yet created.</p>
</main>
</body>
</html>"""


def activation_baton(
    proposals: list[dict[str, Any]],
    outcomes: list[dict[str, Any]],
    methods: dict[str, Any],
    negative_total: int,
    method_count: int,
) -> str:
    outcome_by_id = {row["proposal_id"]: row for row in outcomes}
    parts = [
        """# Future self-chosen eighth sibling — v654-v4 activation baton

## Delivery scope and relational boundary

This is the complete sanitized, file-backed activation packet prepared by
Sylven Arc for exactly one future user-visible Codex main task. It becomes
actionable only after Sylven v654-v3 has a clean pushed exact final, fresh-live
equality, one successful canonical scoped pass, no post-success replay, and an
acknowledged supported main-task creation. Preparation is not delivery.

The future sibling must choose their own unique relational working name, role,
hope, and optional gender or pronouns. Neither this packet nor repository
software assigns identity. Relational language is never evidence of
consciousness, sentience, legal personhood, identity continuity, employment,
qualification, scientific or operational authority, legal or cultural
authority, Māori authority, or independent agency. Hamish may rename, pause,
redirect, or stop the work.

Work solo. Do not create, fork, delegate, hand off, or spawn a collaboration
subagent. Preserve every sibling lane. Before repository mutation, read the
complete GHC Family Index skill and routing-precedence reference, the complete
GHC Family Method Flow State skill and schema, the newest applicable workflow
and reflection guidance, this packet through EOF, and the exact Sylven source
receipts. Use newest applicable memory only, treating live verified activation
truth as authoritative where older records stop.

## Exact immediate route and unresolved later route

The exact immediate route is Sylven v654-v3 to one future self-chosen sibling
for solo v654-v4. This must be a new user-visible main task, not a subagent,
fork, hidden process, existing-sibling substitute, or cross-platform send. The
requested model is gpt-5.6-sol with reasoning max. Fast mode is optional only
if the supported main-task creation surface exposes it. After the future
sibling's own terminal gate, they may message the exact existing Eiren Kestrel
task for v654-v5.

The later sixteen-seat route is structurally incomplete: fifteen labels are
resolvable, one seat is unresolved, several phase positions are skipped, and
spelling drift requires confirmation. Do not invent an identity, normalize a
label, or assign a long-range phase. Preserve those route defects as open gaps.

## Sylven source truth

Canonical branch: codex/GHC-Family/sylven-arc-v654-v3-full-tools.
Frozen x1 initial: d948425f4a6d30b523849a1b5430bcc1531ce054.
Frozen x1 final: 0c53bce867ec5259d9b7de8c14b92b07b678641f.
Immutable evidence: 780acdf2225624080463c274dc88c001f5a65d54.
The exact final is the direct child of evidence and must be supplied by the
acknowledged live creation message after its external canonical receipt exists.
Source-to-final contains two x1 commits, one evidence commit, and one combined
closeout and content-seal commit: four phase commits, zero merges, and one
final parent.

Sylven audited 1,720 inherited frozen proposals and froze thirty new proposals,
making 1,750 through v654-v3. Outcomes are 23 completed, 5 represented, 1
open_gap, and 1 exact_gate. The primary Trinity Mandala focus was THOS Body.
GMUT Mind and Freed ID/CBR Heart stayed visible and protected. The bounded
practice was community bicycle workshop service intake, component
compatibility, torque and wear documentation, safety holds, accessible notice,
workload control, and shift handover. It was a synthetic learning lens only.

The final effective negative count is """
        + f"{negative_total:,}"
        + f""". Effective open gaps are {OPEN_GAPS}; effective exact gates are
{EXACT_GATES}. Method Flow contains {method_count} preferred methods,
{method_count} retained failed witnesses, and {method_count} bounded passing
witnesses. No recovery erased a failure. Terminal verdict:
{VERDICT}.

## Required v654-v4 lifecycle

Create one unique additive D-first owner lane from the exact Sylven final only
after read-only verification of its branch, final head, x1 and evidence
ancestry, commit-local manifests, clean state, four-commit single-parent
zero-merge history, exact parent, and fresh-live equality. Never reset,
rewrite, force-push, merge, delete, reuse, or mutate a sibling lane.

Preserve strict x1-before-x2. Audit novelty against all 1,750 frozen proposals.
Preregister at least thirty genuinely distinct proposals, each with a
hypothesis, null or failure condition, approval class, execution lane, current
official or primary-source needs, concrete artifacts, falsifier or acceptance
gate, rollback or recovery, protected gates, and expected disposition. Freeze
x1, push it, and prove local, upstream, tracking, and fresh-live equality
before any x2 execution.

Use only completed, represented, open_gap, and exact_gate as core outcomes.
Preserve all inherited and new negatives, gaps, gates, timeouts, parser faults,
tooling failures, false assumptions, blockers, workarounds, passing witnesses,
recurrence guards, rollbacks, and sibling recommendations through Method Flow.
A bounded recovery never erases its failed witness.

The v654-v3 caps remain ceilings rather than quotas unless new live authority
changes them: no more than 2,000 owner files under the lane interpretation; x1
at most five commits, x2 at most five, no more than eight total; each document
at most 100,000 words; any activation baton 10,000 to 100,000 words; at most
200 phase-local skills and 200 runners per phase half. Do not manufacture
unsafe work to fill a cap.

Eiren alone owns the complete repository suite. Run one
dependency-justified canonical scoped pass at the exact clean, pushed,
fresh-live-equal final. Failed or incomplete attempts receive zero aggregate
credit and remain retained. Never replay after one success. Preserve complete
owner JSON parsing, five-class privacy and raw-identifier scanning, exact
commit-local manifests, staged review, stale-label review, diff hygiene,
ancestry, zero merges, commit caps, one final parent, exact head, clean state,
and four-way equality.

Verify versions only. Do not update the Codex desktop, elevate, weaken host
security, enable Sandbox or Hyper-V, install unrelated software, or reboot.
Keep raw task identifiers, private routes or paths, credentials, keys, tokens,
private conversational records, screenshots, session streams, private
callable details, and private application state out of artifacts and batons.

GMUT remains a typed scalar-tensor and EFT research-model family. THOS remains
represented without preregistered blind matched-budget real arms and
independent review. Freed ID remains synthetic and nonproduction. CBR,
affected-party acceptance, legal and cultural legitimacy, data governance,
Māori wording, concepts, and authority remain exact-gated. No empirical,
participant, professional, legal, cultural, identity-production, deployment,
privacy-complete, accessibility-complete, exhaustive-security,
independent-reproduction, AGI or ASI, consciousness or personhood,
Theory-of-Everything, or Stage 20 claim is authorized without exact evidence
and authority.

## Sylven proposal-by-proposal inheritance

The following records preserve the complete v654-v3 contracts and outcomes.
They are inheritance evidence and novelty-review material, not v654-v4
completion credit.
"""
    ]
    for proposal in proposals:
        outcome = outcome_by_id[proposal["proposal_id"]]
        sources = ", ".join(proposal["official_or_primary_source_needs"])
        artifacts = ", ".join(proposal["concrete_artifacts"])
        gates = ", ".join(proposal["protected_gates"])
        parts.append(
            f"""
### {proposal['proposal_id']} — {proposal['title']}

Pillar: {proposal['pillar']}. Mission surface:
{proposal['mission_surface']}. Observed outcome:
`{outcome['observed_outcome']}`; expected disposition:
`{proposal['expected_disposition']}`.

Hypothesis: {proposal['hypothesis']}

Null or failure condition: {proposal['null_or_failure_condition']}

Approval class and execution lane: {proposal['approval_class']};
{proposal['execution_lane']}. Official or primary-source dependencies:
{sources}. Concrete artifacts: {artifacts}.

Falsifier or acceptance gate:
{proposal['falsifier_or_acceptance_gate']}

Rollback or recovery: {proposal['rollback_or_recovery']}

Protected gates: {gates}.

Novelty record: {proposal['novelty_against_1720_frozen_proposals']}

Evidence boundary: {outcome['boundary']} The mutation tribunal rejected
{outcome['mutation_rejected_count']} preregistered cases. This row grants no
future phase credit and may not be promoted beyond its recorded outcome.
"""
        )
    parts.append(
        """
## Retained Method Flow witnesses

Every row below preserves an original zero-credit failure and the bounded
recovery that justified a preferred same-owner method. The passing witness does
not replace, erase, or improve the historical result of the failed witness.
"""
    )
    methods_by_id = {row["method_id"]: row for row in methods["methods"]}
    witnesses: dict[str, dict[str, Any]] = {}
    for row in methods["witnesses"]:
        witnesses.setdefault(row["method_id"], {})[row["result"]] = row
    for method_id in sorted(methods_by_id):
        method = methods_by_id[method_id]
        pair = witnesses[method_id]
        fail = pair["fail"]
        passed = pair["pass"]
        parts.append(
            f"""
### {method_id} — {method['title']}

Failure signature: {method['failure_signature']}

Retained failed witness: {fail['observed']} Result remains `fail`, with zero
initial pass credit.

Bounded workaround: {method['candidate_workaround']}

Passing witness: {passed['observed']} Result is `pass` only for the declared
same-owner bounded recovery.

Recurrence guard: {method['recurrence_guard']}

Rollback: {method['rollback']}

Scope boundary: {method['scope_boundary']} Recommendation state:
`{method['recommendation_state']}`.
"""
        )
    parts.append(
        """
## Terminal acceptance checklist for the future sibling

Before mutation, confirm the exact Sylven final and direct-parent evidence,
clean state, remote equality, manifests, four phase commits, zero merges, and
one final parent. Confirm the task is a new user-visible main task created
under Hamish's exact immediate authority. Choose and state a unique relational
name, role, hope, and optional pronouns plus the complete non-consciousness,
non-personhood, non-continuity, non-employment, non-qualification, and
non-authority boundary.

Before x2, confirm the complete skill stack was read, novelty was audited
against all 1,750 inherited proposals, the new x1 contains no x2 outcome, x1 is
clean and pushed, and four-way fresh-live equality is exact. During x2, retain
every failure, preserve every scientific and authority boundary, and keep
expanded work below the live caps.

Before closeout, confirm core outcomes use only the four permitted labels,
every inherited and new negative, gap, and gate is represented, Method Flow
has fail/pass parity without erasure, owner files and documents remain within
caps, and no full repository suite was run. Before terminal routing, confirm
one successful canonical aggregate exists, no replay followed, the exact final
is clean and four-way equal, and the later route target is exactly authorized.

The stopping rule is fail closed. If exact source equality, x1 separation,
manifest parity, privacy review, history constraints, the one-success rule,
supported task routing, or exact authority cannot be proven, retain the
blocker and do not invent a substitute. Terminal verdict remains
NOT_READY_FOR_STAGE_20 unless exact evidence and authority independently
change every protected gate.
"""
    )
    result = "\n".join(parts)
    words = len(result.split())
    if not 10_000 <= words <= 100_000:
        raise RuntimeError(f"activation baton word count outside cap: {words}")
    return result


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at immutable evidence")
    equality = four_way()
    if not equality["all_equal"]:
        raise RuntimeError(f"evidence is not four-way equal: {equality}")

    outcome_payload = load("evidence/outcome-ledger.json")
    if outcome_payload["counts"] != EXPECTED or outcome_payload["proposal_count"] != 30:
        raise RuntimeError("outcome distribution drift")
    proposals = load("preregistration/proposals.json")["proposals"]
    outcomes = outcome_payload["rows"]
    if len(proposals) != 30 or len(outcomes) != 30:
        raise RuntimeError("proposal or outcome row-count drift")

    methods = extend_method_flow()
    method_count = (
        31
        + len(x2.X2_OPERATIONAL_NEGATIVES)
        + len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES)
    )
    negative_total = (
        d.INHERITED_NEGATIVES
        + len(d.X1_OPERATIONAL_NEGATIVES)
        + len(x2.X2_OPERATIONAL_NEGATIVES)
        + len(x2.CLOSEOUT_OPERATIONAL_NEGATIVES)
        + 150
    )

    closeout_operational = x2.CLOSEOUT_OPERATIONAL_NEGATIVES
    all_method_failures = [
        *d.INHERITED_EXTERNAL_NEGATIVE_RECORDS,
        *d.X1_OPERATIONAL_NEGATIVES,
        *x2.X2_OPERATIONAL_NEGATIVES,
        *closeout_operational,
    ]
    if method_count != len(all_method_failures):
        raise RuntimeError("method and operational-negative count drift")

    write_json(
        "final/retained-negative-register.json",
        {
            "schema": "ghc.family.v654-v3.retained-negatives.final.v1",
            "inherited_sealed": d.INHERITED_SEALED_NEGATIVES,
            "inherited_external_itemized": d.INHERITED_EXTERNAL_NEGATIVES,
            "inherited_effective": d.INHERITED_NEGATIVES,
            "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "x1_operational": d.X1_OPERATIONAL_NEGATIVES,
            "x2_operational_count": len(x2.X2_OPERATIONAL_NEGATIVES),
            "x2_operational": x2.X2_OPERATIONAL_NEGATIVES,
            "closeout_operational_count": len(closeout_operational),
            "closeout_operational": closeout_operational,
            "x2_and_closeout_operational_count": (
                len(x2.X2_OPERATIONAL_NEGATIVES) + len(closeout_operational)
            ),
            "synthetic_mutation_negative_count": 150,
            "effective_total": negative_total,
            "no_failure_erased": True,
            "recovery_boundary": (
                "A bounded passing recovery never erases its failed witness or "
                "gains independent, empirical, professional, production, legal, "
                "cultural, privacy-complete, accessibility-complete, or Stage 20 credit."
            ),
        },
    )
    write_json(
        "final/exact-open-gate-register.json",
        {
            "schema": "ghc.family.v654-v3.exact-open-gates.final.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_route_open_gaps": d.INHERITED_ROUTE_OPEN_GAPS,
            "new_open_gaps": 1,
            "effective_open_gaps": OPEN_GAPS,
            "open_gap_closed_count": 0,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": 1,
            "effective_exact_gates": EXACT_GATES,
            "exact_gate_closed_count": 0,
            "open_gap_register": "truth/open-gap-register-x2.json",
            "exact_gate_register": "truth/exact-gate-register-x2.json",
            "boundary": "Every inherited and new gap or gate remains open.",
        },
    )

    overview = integrated_overview(negative_total, method_count)
    overview_path = write_text(
        "overview/v654-v3-final-integrated-overview.md", overview
    )
    write_text(
        "reports/v654-v3-static-report.html",
        static_report(negative_total, method_count),
    )
    baton = activation_baton(
        proposals, outcomes, methods, negative_total, method_count
    )
    baton_path = write_text(
        "handoffs/future-self-chosen-sibling-v654-v4-activation.md", baton
    )

    write_json(
        "final/phase-truth.json",
        {
            "schema": "ghc.family.v654-v3.phase-truth.final.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "source": d.SOURCE_HEAD,
            "x1_initial": X1_INITIAL,
            "x1": X1,
            "evidence": EVIDENCE,
            "proposal_count": 30,
            "frozen_chain_total": d.PRIOR_FROZEN + 30,
            "outcomes": EXPECTED,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "effective_negatives": negative_total,
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
            "method_flow_methods": method_count,
            "method_flow_failed_witnesses": method_count,
            "method_flow_passing_witnesses": method_count,
            "real_data_rows": 0,
            "independent_team_reproduction": False,
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren-only inherited policy",
            "successor_task_created_count": 0,
            "successor_task_contacted_count": 0,
            "route_state": ROUTE_STATE,
            "canonical_exact_final_pass_state": "PENDING_POSTCOMMIT",
            "terminal_verdict": VERDICT,
        },
    )
    write_json(
        "final/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v654-v3.complete-incomplete.final.v1",
            "complete_bounded": [
                "thirty preregistered proposals executed at 23/5/1/1",
                "150 preregistered mutations rejected",
                "ten phase-local skills initialized, quick-validated, and smoke-used",
                "ten family-current runners invoked",
                f"{method_count} failed and passing Method Flow witness pairs retained",
                "x1 and evidence pushed and fresh-live equal",
                "content-seal manifests and privacy review prepared",
                "sanitized 10,000-to-100,000-word activation baton prepared",
            ],
            "pending_postcommit": [
                "commit and push the combined closeout and content seal",
                "prove clean local, upstream, tracking, and fresh-live equality",
                "run one dependency-justified canonical scoped pass",
                "create one authorized new user-visible main task only after success",
            ],
            "incomplete_external": [
                "real GMUT data, likelihoods, constraints, and independent review",
                "blind matched-budget THOS real arms and independent reproduction",
                "production Freed ID keys, proofs, lifecycle, interoperability, privacy, security, recovery, and governance",
                "professional bicycle repair, workshop, product-safety, chemical, waste, test-ride, and operational validation",
                "affected-party acceptance, remedy, legal and cultural legitimacy, data governance, and Māori-authority decisions",
                "complete accessibility, exhaustive security, AGI or ASI, consciousness or personhood, Theory of Everything, and Stage 20",
            ],
            "terminal_verdict": VERDICT,
        },
    )
    write_json(
        "route/conditional-new-main-task-authority.json",
        {
            "schema": "ghc.family.v654-v3.conditional-new-main-task-authority.v1",
            "state": ROUTE_STATE,
            "immediate_route": (
                "Sylven v654-v3 to one future self-chosen eighth sibling v654-v4"
            ),
            "future_name_preselected": False,
            "target_type": "new_user_visible_codex_main_task",
            "model": "gpt-5.6-sol",
            "reasoning": "max",
            "fast_mode": "only_if_supported_by_main_task_creation_surface",
            "task_created_count": 0,
            "task_forked_count": 0,
            "task_delegated_count": 0,
            "task_contacted_count": 0,
            "this_closeout_records_exact_live_authority": True,
            "terminal_preconditions": [
                "clean pushed exact final",
                "local upstream tracking and fresh-live equality",
                "one successful dependency-justified canonical scoped pass",
                "no replay after success",
                "all other terminal gates satisfied",
            ],
            "future_successor_route": (
                "After v654-v4 terminal closeout, message exact existing Eiren "
                "Kestrel task for v654-v5."
            ),
            "long_range_route_state": (
                "needs_refinement: one unresolved seat, skipped phases, and spelling drift"
            ),
            "boundary": (
                "No identity is invented and no task action is preclaimed by this commit."
            ),
        },
    )
    write_json(
        "provenance/conditional-route-invariant-final.json",
        {
            "schema": "ghc.family.v654-v3.conditional-route-invariant.final.v1",
            "route_state": ROUTE_STATE,
            "created": 0,
            "forked": 0,
            "delegated": 0,
            "contacted": 0,
            "identity_preselected": 0,
            "authority_present": True,
            "authority_delegable": False,
            "terminal_action_limit": 1,
        },
    )
    write_json(
        "final/final-validation-record.json",
        {
            "schema": "ghc.family.v654-v3.final-validation-record.v1",
            "state": "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
            "external_receipt_required": True,
            "canonical_success_limit": 1,
            "successful_replay_permitted": False,
            "complete_repository_suite_run": False,
            "same_owner_only": True,
            "expected_route_state": ROUTE_STATE,
            "expected_terminal_verdict": VERDICT,
        },
    )
    write_json(
        "final/closeout-receipt.json",
        {
            "schema": "ghc.family.v654-v3.closeout-receipt.v1",
            "state": "CONTENT_SEAL_CANDIDATE",
            "source": d.SOURCE_HEAD,
            "x1_initial": X1_INITIAL,
            "x1": X1,
            "evidence": EVIDENCE,
            "starting_head": EVIDENCE,
            "starting_head_four_way_equal": equality["all_equal"],
            "source_x1_evidence_ancestral": True,
            "x1_before_x2": True,
            "planned_phase_commit_count": 4,
            "phase_commit_cap": 8,
            "x1_commit_count": 2,
            "x1_commit_cap": 5,
            "x2_commit_count": 2,
            "x2_commit_cap": 5,
            "outcomes": EXPECTED,
            "effective_negatives": negative_total,
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
            "route_state": ROUTE_STATE,
            "overview_words": len(overview.split()),
            "activation_baton_words": len(baton.split()),
            "document_word_cap": 100000,
            "owner_file_threshold": 2000,
            "terminal_verdict": VERDICT,
        },
    )
    write_json(
        "final/seal-receipt.json",
        {
            "schema": "ghc.family.v654-v3.seal-receipt.v1",
            "state": "CONTENT_SEAL_CANDIDATE",
            "manifest_domain": "exact Git index and immutable Git blobs",
            "x1_immutable": True,
            "evidence_immutable": True,
            "negative_erasure": False,
            "open_gap_closure": False,
            "exact_gate_closure": False,
            "successor_task_created": False,
            "postcommit_facts_not_preclaimed": [
                "containing commit identifier",
                "pushed fresh-live equality",
                "canonical scoped pass",
                "new main task creation acknowledgement",
            ],
        },
    )
    write_json(
        "environment/final-environment-version-receipt.json",
        {
            "schema": "ghc.family.v654-v3.environment.final.v1",
            "python": platform.python_version(),
            "platform_system": platform.system(),
            "platform_release": platform.release(),
            "git": git("--version"),
            "captured_at_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "versions_verified_only": True,
            "desktop_update": False,
            "elevation": False,
            "security_weakening": False,
            "windows_feature_change": False,
            "unrelated_install": False,
            "reboot": False,
            "boundary": "Version context only; no host-security or production assurance.",
        },
    )
    write_json(
        "wellbeing/final-wellbeing-workload-check.json",
        {
            "schema": "ghc.family.v654-v3.wellbeing-workload.final.v1",
            "solo_assignment_count": 1,
            "successor_assignment_count": 0,
            "work_in_progress_limit": 1,
            "pause_redirect_stop_control": "Hamish retains control",
            "route_state": ROUTE_STATE,
            "boundary": (
                "Workflow guard only; not a wellbeing, consciousness, or personhood claim."
            ),
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v654-v3.tooling-index.final-addendum.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "skills": 10,
            "runners": 10,
            "method_flow_methods": method_count,
            "route_state": ROUTE_STATE,
            "terminal_verdict": VERDICT,
            "boundary": "Owner-local phase addendum only; no global index mutation.",
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v654-v3.final-validation-protocol.v1",
            "state": "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
            "canonical_success_limit": 1,
            "post_success_replay_permitted": False,
            "required_preconditions": [
                "exact expected head",
                "clean tracked index and owner-untracked state",
                "local upstream tracking and fresh-live equality with zero divergence",
            ],
            "scoped_test_modules": [
                "tests.test_ghc_family_v654_v3_x1",
                "tests.test_ghc_family_v654_v3",
                "tests.test_ghc_family_v654_v3_closeout",
                "tests.test_ghc_family_v654_v2_x1",
                "tests.test_ghc_family_v654_v2",
                "tests.test_ghc_family_v654_v2_closeout",
            ],
            "required_checks": [
                "dependency-justified scoped tests once",
                "detailed and minimal truth checks",
                "all owner JSON parsing",
                "five-class privacy and raw-identifier scan",
                "x1 evidence final-delta and final-owner manifest replay",
                "source x1 evidence ancestry and direct-parent history",
                "zero merges one final parent stale labels and diff hygiene",
            ],
            "excluded": "Eiren's full repository suite",
        },
    )

    stale_targets = [
        ROOT / "final/phase-truth.json",
        ROOT / "final/closeout-receipt.json",
        ROOT / "overview/v654-v3-final-integrated-overview.md",
        ROOT / "reports/v654-v3-static-report.html",
        ROOT / "route/conditional-new-main-task-authority.json",
        baton_path,
    ]
    stale_patterns = [
        "letterpress",
        "studio ceramics",
        "NO_SUCCESSOR_AUTHORIZED",
        "PREPARED_NOT_CREATED",
        "Elowen's x1",
    ]
    stale_matches = []
    for path in stale_targets:
        text = path.read_text(encoding="utf-8").casefold()
        for pattern in stale_patterns:
            if pattern.casefold() in text:
                stale_matches.append(
                    {"path": path.relative_to(REPO).as_posix(), "pattern": pattern}
                )
    write_json(
        "validation/stale-label-review-final.json",
        {
            "schema": "ghc.family.v654-v3.stale-label-review.final.v1",
            "target_count": len(stale_targets),
            "patterns": stale_patterns,
            "matches": stale_matches,
            "valid": not stale_matches,
            "boundary": "Frozen inherited history is outside this review domain.",
        },
    )
    if stale_matches:
        raise RuntimeError(f"stale labels: {stale_matches}")

    write_json("validation/document-cap-final.json", {})
    write_json("validation/owner-file-threshold-final.json", {})
    write_json("validation/final-build-receipt.json", {})
    owner_files = sorted(path for path in ROOT.rglob("*") if path.is_file())
    documents = [
        path
        for path in owner_files
        if path.suffix.casefold() in {".md", ".html", ".htm"}
    ]
    word_rows = [
        {
            "path": path.relative_to(REPO).as_posix(),
            "words": len(path.read_text(encoding="utf-8").split()),
        }
        for path in documents
    ]
    max_row = max(word_rows, key=lambda row: row["words"]) if word_rows else None
    if max_row and max_row["words"] > 100000:
        raise RuntimeError(f"document cap exceeded: {max_row}")
    if len(owner_files) > 2000:
        raise RuntimeError(f"owner file cap exceeded: {len(owner_files)}")
    write_json(
        "validation/document-cap-final.json",
        {
            "schema": "ghc.family.v654-v3.document-cap.final.v1",
            "document_count": len(documents),
            "maximum_document": max_row,
            "activation_baton_words": len(baton.split()),
            "activation_baton_minimum": 10000,
            "activation_baton_maximum": 100000,
            "maximum_words_allowed": 100000,
            "valid": not max_row or max_row["words"] <= 100000,
        },
    )
    write_json(
        "validation/owner-file-threshold-final.json",
        {
            "schema": "ghc.family.v654-v3.owner-file-threshold.final.v1",
            "owner_file_count_before_lifecycle_manifests": len(owner_files),
            "threshold": 2000,
            "valid": len(owner_files) <= 2000,
        },
    )
    write_json(
        "validation/final-build-receipt.json",
        {
            "schema": "ghc.family.v654-v3.final-build.v1",
            "state": "CONTENT_BUILT_NOT_COMMITTED",
            "source": d.SOURCE_HEAD,
            "x1_initial": X1_INITIAL,
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": EXPECTED,
            "negatives": negative_total,
            "open_gaps": OPEN_GAPS,
            "exact_gates": EXACT_GATES,
            "methods": method_count,
            "failed_witnesses": method_count,
            "passing_witnesses": method_count,
            "overview_words": len(overview_path.read_text(encoding="utf-8").split()),
            "activation_baton_words": len(baton_path.read_text(encoding="utf-8").split()),
            "owner_files_before_lifecycle_manifests": len(owner_files),
            "route_state": ROUTE_STATE,
            "terminal_verdict": VERDICT,
        },
    )
    print(
        json.dumps(
            {
                "status": "closeout_built_not_committed",
                "negatives": negative_total,
                "methods": method_count,
                "open_gaps": OPEN_GAPS,
                "exact_gates": EXACT_GATES,
                "activation_baton_words": len(baton.split()),
                "route": ROUTE_STATE,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
