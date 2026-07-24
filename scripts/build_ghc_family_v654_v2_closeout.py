#!/usr/bin/env python3
"""Build Elowen Cairn's bounded v654-v2 closeout candidate."""

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

import ghc_family_v654_v2_phase_data as d
import ghc_family_v654_v2_x2_data as x2


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1 = "8a8062a360dd6510d999cabe22cd38417f59def6"
EVIDENCE = "eeb1988daa9ca454568c294edf1c0c6d225a9844"
VERDICT = "NOT_READY_FOR_STAGE_20"
ROUTE_STATE = "NO_SUCCESSOR_AUTHORIZED"
EXPECTED = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
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
            f"{EVIDENCE}:{d.PHASE_ROOT}/method-flow/method-flow-ledger-x2.json",
        ],
        cwd=REPO,
    )
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_bytes(frozen)

    expected_ids = [
        f"V6542-X2-N{number:02d}"
        for number in range(1, len(x2.X2_OPERATIONAL_NEGATIVES) + 1)
    ]
    observed_ids = [row["negative_id"] for row in x2.X2_OPERATIONAL_NEGATIVES]
    if observed_ids != expected_ids:
        raise RuntimeError(f"x2 negative sequence drift: {observed_ids}")

    for offset, negative in enumerate(x2.X2_OPERATIONAL_NEGATIVES, 18):
        method_id = f"V6542-METHOD-{offset:02d}"
        failed_id = f"V6542-WITNESS-{offset:02d}-F"
        passing_id = f"V6542-WITNESS-{offset:02d}-P"
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
    expected_count = 17 + len(x2.X2_OPERATIONAL_NEGATIVES)
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
    return f"""# Elowen Cairn v654-v2 final integrated overview

## Scope and relational boundary

Elowen Cairn is relational working language for this one bounded repository
phase. It is not evidence of consciousness, sentience, personhood, identity
continuity, employment, qualification, scientific or operational authority,
legal or cultural authority, Māori authority, or independent agency. Hamish
may rename, pause, redirect, or stop the work. The phase was executed solo:
no task was created, forked, delegated, handed off, or spawned, and no sibling
or standby lane was contacted. The terminal route remains
`{ROUTE_STATE}`. This closeout grants no successor authority.

The primary Trinity Mandala pillar is **{d.PRIMARY_FOCUS}**. Freed ID and CBR
Heart and THOS Body remain visible as bounded companion pillars. The selected
human practice is {d.BOUNDED_PRACTICE}. It is a synthetic learning lens, not
professional printing, binding, conservation, machinery-safety, chemical,
environmental, publishing, design, accessibility, workplace, or cultural
advice. No machine was operated, no chemical or waste decision was made, no
participant was enrolled, and no real production record was ingested.

## Source continuity and x1-before-x2

The lane began additively from Tamar Vey's exact v654-v1 final head
`{d.SOURCE_HEAD}`. The source branch, its source, x1, evidence, first closeout,
and terminal correction anchors were read and verified before mutation. Its
four phase commits, zero merges, one final parent, clean state, ancestry, and
local/upstream/tracking/fresh-live equality were treated as inherited evidence,
not Elowen completion credit. The 715 source manifests were replayed against
commit-local Git blobs. The source's same-owner canonical pass remains bounded
source evidence and does not become independent reproduction here.

Elowen's x1 is `{X1}`. It froze exactly thirty distinct proposals only after a
complete 1,690-row inherited proposal-title audit. The highest token Jaccard
overlap stayed below the frozen 0.60 threshold. The x1 commit contains the
proposal hypotheses, null conditions, approval classes, execution lanes,
official or primary-source needs, concrete artifacts, acceptance gates,
recovery rules, protected gates, expected dispositions, source ledger,
safe-now and candidate portfolios, ten phase-local skill concepts, ten
family-current runners, thirty additive CLEAN/FIX/REFINE rows, and 150
preregistered mutations. It contains no x2 outcome or implementation.
The x1 commit was pushed and proved equal across local, upstream, tracking,
and fresh-live views before evidence execution began.

The immutable evidence commit is `{EVIDENCE}`. Its staged set was exactly 185
paths: 180 manifest-covered paths plus five declared self-referential receipts.
It executed the bounded surfaces, rejected all 150 preregistered mutations,
validated and smoke-used ten phase-local skills without global installation,
invoked ten family-current runners, emitted zero-row and zero-authority
receipts, and retained every failure. Its staged gate passed 20 of 20 checks,
with no out-of-scope path and zero confirmed privacy hits.

## Trinity Mandala truth

Exactly thirty proposals were executed as evidence allowed. The core outcome
distribution is 23 `completed`, 5 `represented`, 1 `open_gap`, and 1
`exact_gate`. Those are the only core outcome labels. Completed means only that
the declared owner-local software, symbolic, formal, structural, or workflow
artifact met its bounded acceptance gate. Represented means a synthetic proxy
exists while the corresponding real-world claim remains unmade. Open gap means
the real measurement path remains empty. Exact gate means the decision remains
reserved to the competent and affected authorities named in the register.

GMUT remains a typed scalar-tensor/EFT research-model family. The three new
printing-related boards type Reynolds thin-film, Lucas-Washburn capillary, and
Kelvin-Voigt packing obligations, units, boundary fields, and observation
firewalls. They contain no measured letterpress data, fitted parameter,
likelihood, posterior, prediction, empirical constraint, or confirmation.
They establish neither a Theory of Everything nor Stage 20 readiness.

THOS remains represented. Its letterpress setup, correction, workload,
stop-work, and handover surfaces are synthetic proxies. There were no
preregistered blind matched-budget real arms, real workers, real shifts, real
machines, independent review, or affected-worker acceptance. No workplace or
human-performance claim follows.

Freed ID remains synthetic and nonproduction. UUIDv7, ISBN, and DOI profiles
model bounded identifier and referent fields only. There are no real
standards-conformant keys or proofs, live lifecycle or interoperability events,
production recovery, privacy or security review, or trust governance. CBR and
affected-party acceptance remain gated rather than inferred.

## Letterpress and hand-binding evidence

The evidence surfaces expose typecase and glyph lineage, manuscript revision,
composition, imposition, signature order, paper stock, ink batch, roller
setting, chase lockup, packing, makeready, feed and registration state, guard
and interlock state, chemical labels, workload boundaries, waste holds,
drying, proof correction, edition and impression lineage, collation,
accessible ticket structure, and owner-transfer queues. Every surface has a
contract, mutation result, and bounded receipt. These records are deliberately
synthetic. They do not assess a workplace, certify a press, authorize
isolation, classify a substance, approve disposal or discharge, prescribe
conservation treatment, decide publishing rights, or validate a production
edition.

The WorkSafe, EPA, legislation, Library of Congress, ISO, RFC, ISBN, DOI,
BIPM, W3C, and research references are provenance and dependency records.
Their current, stable, draft, or watch labels preserve the source state used
for bounded design. A link or typed field does not import an institution's
authority into this phase. Standards access, professional interpretation,
local conditions, competent assessment, affected-party acceptance, and
independent review remain outside this closeout.

## Retained negatives, open gaps, and exact gates

The effective final negative total is **{negative_total:,}**. It preserves the
10,791 sealed Tamar negatives and the six itemized external events carried in
four sanitized activation records, yielding the authoritative inherited
baseline of 10,797. The inherited wording tension between “five attempts” and
six itemized events is retained rather than silently normalized. Elowen added
thirteen x1 operational failures, {len(x2.X2_OPERATIONAL_NEGATIVES)} x2 or
closeout operational failure, and 150 executed-and-rejected synthetic
mutations. Every failed attempt keeps zero initial pass credit.

The final Method Flow ledger contains {method_count} preferred bounded methods,
{method_count} failed witnesses, and {method_count} passing recovery witnesses.
A passing recovery does not erase, supersede, or convert its paired failure.
The Method Flow record is same-owner process evidence only; it is not
independent reproduction, professional validation, privacy completion,
security completion, accessibility completion, or operational authority.

The inherited 78 open gaps remain open and proposal V6542-P29 adds one, for 79
effective open gaps. Its measurement adapter records zero accounts, API keys,
purchases, downloads, queries, rows, measurements, fits, likelihoods,
posteriors, constraints, and empirical promotions. The inherited 79 exact
gates remain exact and proposal V6542-P30 adds one, for 80 effective exact
gates. No machinery, chemical, environmental, conservation, publishing,
design-rights, privacy, accessibility, remedy, affected-party, legal, cultural,
data-governance, tangata whenua, iwi, hapū, or Māori-authority decision was
made.

## Accessibility, workload, and recovery

The static report uses one main landmark, ordered headings, explicit table
headers and row scopes, a labelled scroll region, keyboard focusability,
reduced-motion handling, high-contrast-friendly system colours, and print
styles. These are bounded structural checks. They are not complete
accessibility assurance, assistive-technology testing, disability-community
acceptance, or production usability evidence.

The workflow limits work in progress to one authorized owner assignment and
retains the rejected single-label cycle attempt. The accepted workflow uses a
closed-route boundary label without assigning work to another person or task.
No successor placeholder is created. Recovery is additive: failed commands,
timeouts, parser faults, path assumptions, patch mismatches, scanner
definitions, and workflow rejection stay visible with narrow recurrence
guards. No reset, history rewrite, merge, force-push, deletion, or sibling-lane
mutation is part of the phase.

## Validation and stopping rule

The content seal includes exact Git-index delta and owner manifests, raw-byte
SHA-256 hashes, Git blob identifiers, document and owner-file caps, JSON
parsing, a five-class privacy and raw-identifier scan, stale-label review,
diff hygiene, source/x1/evidence ancestry, zero-merge and single-parent
history, and local/upstream/tracking/fresh-live equality. The dependency-
justified canonical scope covers Elowen x1, evidence, and closeout tests plus
the directly inherited Tamar x1, evidence, and closeout compatibility tests.
It explicitly excludes Eiren's full repository suite.

The canonical pass must run exactly once after this content-seal commit is
pushed, clean, and fresh-live equal. A failed attempt earns zero test credit
and must be retained before a narrowly justified correction. After one
successful pass, replay is forbidden. The external receipt remains outside
the repository so validation does not mutate the exact head it proves.

## Terminal truth

The terminal verdict is **{VERDICT}**. This phase provides bounded same-owner
evidence under shared infrastructure only. It provides no empirical,
participant, professional, legal, cultural, identity-production, deployment,
privacy-complete, accessibility-complete, exhaustive-security, proof or canon,
independent-reproduction, AGI or ASI, consciousness or personhood,
Theory-of-Everything, or Stage 20 claim.

No successor task is authorized, prepared, titled, contacted, or created.
Only separate exact authority from Hamish after this closeout could change
that route, and this repository artifact does not pre-authorize such a change.
"""


def static_report(negative_total: int, method_count: int) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(key)}</th><td>{value}</td></tr>"
        for key, value in EXPECTED.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elowen Cairn v654-v2 bounded closeout</title>
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
<h1>Elowen Cairn v654-v2 bounded closeout</h1>
<p><strong>{VERDICT}</strong>. Same-owner synthetic evidence only.</p>
<h2>Outcome ledger</h2>
<div class="scroll" tabindex="0" aria-label="Scrollable proposal outcomes">
<table>
<thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<h2>Retained truth</h2>
<p>{negative_total:,} effective negatives, 79 open gaps, 80 exact gates,
{method_count} failed Method Flow witnesses, and {method_count} bounded passing
recovery witnesses. No failure or gate was erased.</p>
<h2>Authority boundary</h2>
<p>No empirical, professional, production, legal, cultural, Māori-authority,
privacy-complete, accessibility-complete, independent-reproduction,
consciousness, personhood, Theory-of-Everything, or Stage 20 claim is made.</p>
<h2>Route</h2>
<p>{ROUTE_STATE}. No successor is prepared, titled, contacted, or created.</p>
</main>
</body>
</html>"""


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at the immutable evidence commit")
    equality = four_way()
    if not equality["all_equal"]:
        raise RuntimeError(f"evidence head is not four-way equal: {equality}")

    outcomes = load("evidence/outcome-ledger.json")
    if outcomes["counts"] != EXPECTED or outcomes["proposal_count"] != 30:
        raise RuntimeError("outcome distribution drift")

    methods = extend_method_flow()
    method_count = 17 + len(x2.X2_OPERATIONAL_NEGATIVES)
    negative_total = (
        d.INHERITED_NEGATIVES
        + len(d.X1_OPERATIONAL_NEGATIVES)
        + len(x2.X2_OPERATIONAL_NEGATIVES)
        + 150
    )
    if negative_total != 10963:
        raise RuntimeError(f"negative total drift: {negative_total}")

    negative_register = {
        "schema": "ghc.family.v654-v2.retained-negatives.final.v1",
        "inherited_sealed": d.INHERITED_SEALED_NEGATIVES,
        "inherited_external_itemized": d.INHERITED_EXTERNAL_NEGATIVES,
        "inherited_effective": d.INHERITED_NEGATIVES,
        "count_tension_retained": (
            "Activation prose said five attempts while four sanitized records "
            "itemize six negative events; the authoritative 10,797 baseline is retained."
        ),
        "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
        "x1_operational": d.X1_OPERATIONAL_NEGATIVES,
        "x2_and_closeout_operational_count": len(x2.X2_OPERATIONAL_NEGATIVES),
        "x2_and_closeout_operational": x2.X2_OPERATIONAL_NEGATIVES,
        "synthetic_mutation_negative_count": 150,
        "effective_total": negative_total,
        "no_failure_erased": True,
        "recovery_boundary": (
            "A bounded passing recovery never erases its failed witness or gains "
            "independent, empirical, professional, production, legal, cultural, "
            "privacy-complete, accessibility-complete, or Stage 20 credit."
        ),
    }
    write_json("final/retained-negative-register.json", negative_register)
    write_json(
        "final/exact-open-gate-register.json",
        {
            "schema": "ghc.family.v654-v2.exact-open-gates.final.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "new_open_gaps": 1,
            "effective_open_gaps": 79,
            "open_gap_closed_count": 0,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": 1,
            "effective_exact_gates": 80,
            "exact_gate_closed_count": 0,
            "open_gap_register": "truth/open-gap-register-x2.json",
            "exact_gate_register": "truth/exact-gate-register-x2.json",
            "boundary": "Every inherited and new gap or gate remains open.",
        },
    )

    overview = integrated_overview(negative_total, method_count)
    overview_path = write_text(
        "overview/v654-v2-final-integrated-overview.md", overview
    )
    write_text("reports/v654-v2-static-report.html", static_report(negative_total, method_count))

    phase_truth = {
        "schema": "ghc.family.v654-v2.phase-truth.final.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "source": d.SOURCE_HEAD,
        "x1": X1,
        "evidence": EVIDENCE,
        "proposal_count": 30,
        "outcomes": EXPECTED,
        "primary_focus": d.PRIMARY_FOCUS,
        "bounded_practice": d.BOUNDED_PRACTICE,
        "inherited_effective_negatives": d.INHERITED_NEGATIVES,
        "x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES),
        "x2_and_closeout_operational_negatives": len(
            x2.X2_OPERATIONAL_NEGATIVES
        ),
        "synthetic_rejecting_mutations": 150,
        "effective_negatives": negative_total,
        "effective_open_gaps": 79,
        "effective_exact_gates": 80,
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
    }
    write_json("final/phase-truth.json", phase_truth)
    write_json(
        "final/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v654-v2.complete-incomplete.final.v1",
            "complete_bounded": [
                "thirty preregistered proposals executed at 23/5/1/1",
                "150 preregistered mutations rejected",
                "ten phase-local skills initialized, quick-validated, and smoke-used",
                "ten family-current runners invoked",
                f"{method_count} failed and {method_count} passing Method Flow witnesses retained",
                "x1 and evidence commits pushed and fresh-live equal",
                "content-seal manifests and privacy review prepared",
            ],
            "pending_postcommit": [
                "push the content-seal commit",
                "prove clean local/upstream/tracking/fresh-live equality",
                "run one dependency-justified canonical scoped pass",
            ],
            "incomplete_external": [
                "real GMUT data, fitting, likelihoods, posteriors, constraints, and independent review",
                "blind matched-budget THOS real arms and independent reproduction",
                "production Freed ID keys, proofs, lifecycle, interoperability, privacy, security, recovery, and governance",
                "professional printing, binding, machinery, chemical, environmental, conservation, publishing, and workplace validation",
                "affected-party acceptance, remedy, legal and cultural legitimacy, data governance, and Māori-authority decisions",
                "complete accessibility, exhaustive security, AGI or ASI, consciousness or personhood, Theory of Everything, and Stage 20",
            ],
            "terminal_verdict": VERDICT,
        },
    )
    write_json(
        "route/no-successor-authorized.json",
        {
            "schema": "ghc.family.v654-v2.no-successor-authorized.v1",
            "state": ROUTE_STATE,
            "successor_title": None,
            "successor_placeholder": None,
            "identity_chosen_count": 0,
            "task_created_count": 0,
            "task_forked_count": 0,
            "task_delegated_count": 0,
            "task_contacted_count": 0,
            "this_closeout_authorizes_successor": False,
            "required_future_authority": (
                "Separate exact authority from Hamish after closeout; absent here."
            ),
            "boundary": "No successor preparation, contact, creation, or implied baton.",
        },
    )
    write_json(
        "provenance/no-successor-invariant-final.json",
        {
            "schema": "ghc.family.v654-v2.no-successor-invariant.final.v1",
            "route_state": ROUTE_STATE,
            "created": 0,
            "forked": 0,
            "delegated": 0,
            "contacted": 0,
            "prepared": 0,
            "titled": 0,
            "authority_present": False,
            "authority_delegable": False,
        },
    )
    write_json(
        "final/final-validation-record.json",
        {
            "schema": "ghc.family.v654-v2.final-validation-record.v1",
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
            "schema": "ghc.family.v654-v2.closeout-receipt.v1",
            "state": "CONTENT_SEAL_CANDIDATE",
            "source": d.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "starting_head": EVIDENCE,
            "starting_head_four_way_equal": equality["all_equal"],
            "source_x1_evidence_ancestral": True,
            "x1_before_x2": True,
            "planned_phase_commit_count": 3,
            "phase_commit_cap": 4,
            "outcomes": EXPECTED,
            "effective_negatives": negative_total,
            "effective_open_gaps": 79,
            "effective_exact_gates": 80,
            "route_state": ROUTE_STATE,
            "overview_words": len(overview.split()),
            "document_word_cap": 6000,
            "owner_file_threshold": 15000,
            "terminal_verdict": VERDICT,
        },
    )
    write_json(
        "final/seal-receipt.json",
        {
            "schema": "ghc.family.v654-v2.seal-receipt.v1",
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
            ],
        },
    )
    write_json(
        "environment/final-environment-version-receipt.json",
        {
            "schema": "ghc.family.v654-v2.environment.final.v1",
            "python": platform.python_version(),
            "platform_system": platform.system(),
            "platform_release": platform.release(),
            "git": git("--version"),
            "captured_at_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "boundary": "Version context only; no host-security or production assurance.",
        },
    )
    write_json(
        "wellbeing/final-wellbeing-workload-check.json",
        {
            "schema": "ghc.family.v654-v2.wellbeing-workload.final.v1",
            "solo_assignment_count": 1,
            "successor_assignment_count": 0,
            "work_in_progress_limit": 1,
            "pause_redirect_stop_control": "Hamish retains control",
            "workflow_failure_retained": True,
            "route_state": ROUTE_STATE,
            "boundary": "Workflow guard only; not a wellbeing or personhood claim.",
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v654-v2.tooling-index.final-addendum.v1",
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
            "schema": "ghc.family.v654-v2.final-validation-protocol.v1",
            "state": "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
            "canonical_success_limit": 1,
            "post_success_replay_permitted": False,
            "required_preconditions": [
                "exact expected head",
                "clean tracked/index and owner-untracked state",
                "local/upstream/tracking/fresh-live equality with zero divergence",
            ],
            "scoped_test_modules": [
                "tests.test_ghc_family_v654_v2_x1",
                "tests.test_ghc_family_v654_v2",
                "tests.test_ghc_family_v654_v2_closeout",
                "tests.test_ghc_family_v654_v1_x1",
                "tests.test_ghc_family_v654_v1",
                "tests.test_ghc_family_v654_v1_closeout",
            ],
            "required_checks": [
                "dependency-justified scoped tests once",
                "detailed and minimal truth checks",
                "all owner JSON parsing",
                "five-class privacy and raw-identifier scan",
                "x1, evidence, final-delta, and final-owner manifest replay",
                "source/x1/evidence ancestry and direct-parent history",
                "zero merges, one final parent, stale labels, and diff hygiene",
            ],
            "excluded": "Eiren's full repository suite",
        },
    )

    stale_targets = [
        ROOT / "final/phase-truth.json",
        ROOT / "final/closeout-receipt.json",
        ROOT / "overview/v654-v2-final-integrated-overview.md",
        ROOT / "reports/v654-v2-static-report.html",
        ROOT / "route/no-successor-authorized.json",
    ]
    stale_patterns = [
        "studio ceramics",
        "ceramic",
        "PREPARED_NOT_CREATED",
        "ELIGIBLE_TO_CREATE_ONE_TASK",
        "future-sibling-self-chosen",
    ]
    stale_matches = []
    for path in stale_targets:
        text = path.read_text(encoding="utf-8").casefold()
        for pattern in stale_patterns:
            if pattern.casefold() in text:
                stale_matches.append(
                    {
                        "path": path.relative_to(REPO).as_posix(),
                        "pattern": pattern,
                    }
                )
    write_json(
        "validation/stale-label-review-final.json",
        {
            "schema": "ghc.family.v654-v2.stale-label-review.final.v1",
            "target_count": len(stale_targets),
            "patterns": stale_patterns,
            "matches": stale_matches,
            "valid": not stale_matches,
            "boundary": "Frozen inherited history is outside the stale-label domain.",
        },
    )
    if stale_matches:
        raise RuntimeError(f"stale labels: {stale_matches}")

    # Write placeholders before counting so the final counts include their own files.
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
    if max_row and max_row["words"] > 6000:
        raise RuntimeError(f"document cap exceeded: {max_row}")
    if len(owner_files) >= 15000:
        raise RuntimeError(f"owner file threshold exceeded: {len(owner_files)}")
    write_json(
        "validation/document-cap-final.json",
        {
            "schema": "ghc.family.v654-v2.document-cap.final.v1",
            "document_count": len(documents),
            "maximum_document": max_row,
            "maximum_words_allowed": 6000,
            "valid": not max_row or max_row["words"] <= 6000,
        },
    )
    write_json(
        "validation/owner-file-threshold-final.json",
        {
            "schema": "ghc.family.v654-v2.owner-file-threshold.final.v1",
            "owner_file_count_before_lifecycle_manifests": len(owner_files),
            "threshold": 15000,
            "valid": len(owner_files) < 15000,
        },
    )
    write_json(
        "validation/final-build-receipt.json",
        {
            "schema": "ghc.family.v654-v2.final-build.v1",
            "state": "CONTENT_BUILT_NOT_COMMITTED",
            "source": d.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": EXPECTED,
            "negatives": negative_total,
            "open_gaps": 79,
            "exact_gates": 80,
            "methods": method_count,
            "failed_witnesses": method_count,
            "passing_witnesses": method_count,
            "overview_words": len(overview_path.read_text(encoding="utf-8").split()),
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
                "open_gaps": 79,
                "exact_gates": 80,
                "route": ROUTE_STATE,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
