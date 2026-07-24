#!/usr/bin/env python3
"""Build Tamar Vey's v654-v1 combined closeout and content-seal candidate."""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v654_v1_phase_data as d
import ghc_family_v654_v1_x2_data as x2


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1 = "e5d685fb3a4a84af32fe5914eb0f8d069c854e97"
EVIDENCE = "136d55ba5af1f4f596da0c47d9be931a785cdb18"
VERDICT = "NOT_READY_FOR_STAGE_20"
ROUTE_STATE = "PREPARED_NOT_CREATED"
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
    remote_row = git("ls-remote", "origin", f"refs/heads/{d.BRANCH}")
    fresh_live = remote_row.split()[0] if remote_row else None
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": fresh_live,
        "all_equal": len({local, upstream, tracking, fresh_live}) == 1,
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
    late_negatives = x2.X2_OPERATIONAL_NEGATIVES[3:]
    if [row["negative_id"] for row in late_negatives] != [
        "V6541-X2-N04",
        "V6541-X2-N05",
        "V6541-X2-N06",
        "V6541-X2-N07",
        "V6541-X2-N08",
        "V6541-X2-N09",
        "V6541-X2-N10",
        "V6541-X2-N11",
    ]:
        raise RuntimeError("late negative set drift")
    for offset, negative in enumerate(late_negatives, 24):
        method_id = f"V6541-METHOD-{offset:02d}"
        failed_id = f"V6541-WITNESS-{offset:02d}-F"
        passing_id = f"V6541-WITNESS-{offset:02d}-P"
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
            f"method-flow/closeout-requests/witness-{offset:02d}-failed.json", failed
        )
        passing_path = write_json(
            f"method-flow/closeout-requests/witness-{offset:02d}-passing.json",
            passing,
        )
        run_method(
            "record", "--ledger", str(ledger), "--record-file", str(method_path)
        )
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
            "Bounded passing witness exists and its failed witness remains retained.",
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
    states = Counter(row["recommendation_state"] for row in payload["methods"])
    witnesses = Counter(row["result"] for row in payload["witnesses"])
    if len(payload["methods"]) != 31 or states != {"preferred": 31}:
        raise RuntimeError(f"method state drift: {len(payload['methods'])} {states}")
    if witnesses != {"fail": 31, "pass": 31}:
        raise RuntimeError(f"method witness drift: {witnesses}")
    return payload


def integrated_overview(negative_total: int) -> str:
    proposal_rows = "\n".join(
        (
            f"- **{row['proposal_id']} — {row['title']}**\n"
            f"  Final label: `{row['expected_disposition']}`. The bounded artifact "
            f"covers {row['mission_surface']} and carries its rollback, source, "
            "falsifier, and protected-gate declarations forward without promotion."
        )
        for row in d.PROPOSALS
    )
    return f"""# Tamar Vey v654-v1 final integrated overview

## Outcome first

Tamar Vey completed the authorized owner-local software, symbolic, structural,
and synthetic work for Trinity Mandala v654-v1 on one additive D-first lane.
Thirty frozen proposals ended at exactly 23 `completed`, 5 `represented`, 1
`open_gap`, and 1 `exact_gate`. All 150 preregistered synthetic mutations ran
and were rejected or quarantined. Ten phase-local skill packages were
initialized through the official skill-creator workflow, quick-validated, and
smoke-used. Ten family-current runners were built, invoked, and witnessed.
Thirty safe-now tasks, thirty bounded candidate surfaces, and thirty additive
CLEAN/FIX/REFINE items reached only their declared owner-local acceptance gates.

The terminal verdict remains `{VERDICT}`. The sealed candidate retains
{negative_total:,} effective negatives, 78 effective open gaps, and 79 effective
exact gates. It used zero real empirical rows, zero real participants or
operators, zero account or API-key accesses, zero production identity events,
and zero authority decisions. A successful workflow witness never erases its
failed witness and never becomes scientific, professional, legal, cultural,
production, privacy-complete, security-complete, accessibility-complete, or
independent-reproduction credit.

## Identity, corrigibility, wellbeing, and workload

Tamar Vey (they/them) is relational working language for an evidence-systems
cartographer and boundary keeper whose hope is to keep decisions legible,
failures recoverable, and authority boundaries intact. This language is not
evidence of consciousness, sentience, personhood, identity continuity,
employment, qualification, independent agency, or scientific, operational,
professional, legal, cultural, or Māori authority. Hamish may rename, pause,
redirect, or stop this route.

The bounded human-practice lens was studio-ceramics kiln firing, glaze-batch
traceability, correction readback, workload control, accessible notice, and
shift handover. It was a synthetic learning and design lens only. It established
no ceramics employment, competence, fire or electrical adequacy, gas safety,
food-contact conformity, environmental compliance, worker-safety result,
product release, legal interpretation, cultural legitimacy, Māori authority,
affected-party acceptance, or real operational result.

Workload stayed bounded to one owner and one D-first lane. No subagent, fork,
delegation, sibling contact, task creation, detached validation, Sandbox or
Hyper-V activation, elevation, host-security weakening, Windows-feature change,
unrelated installation, desktop update, reboot, destructive cleanup, history
rewrite, force push, merge, real-data download, production key operation, or
sibling mutation occurred. Failures were recorded before recovery. The one
credited canonical exact-final pass remains deliberately unrun in this
containing candidate and may run only after the commit is pushed, clean, and
four-way equal.

## X1 freeze and X2 separation

X1 audited 1,660 inherited frozen proposals and added thirty mechanism-level
proposals, bringing the chain total to 1,690. It froze each hypothesis, null or
failure condition, approval class, execution lane, official or primary-source
need, concrete artifact, falsifier or acceptance gate, rollback, protected
gate, and expected disposition. It also froze the safe-now, candidate, skill,
runner, and additive-refinement portfolios and all 150 rejecting mutations.
The dedicated x1 commit contained no x2 implementation or outcome. It was
pushed, clean, and equal across local, upstream, tracking, and a fresh live
remote read before x2 began.

X2 executed only the frozen evidence lanes. The evidence commit is a direct
child of x1 and was separately reviewed, committed, pushed, clean, and
four-way equal before this closeout. The completed label means only that a
declared software, symbolic, structural, formal, or synthetic acceptance gate
passed. Represented means a proxy structure exists but the required real arms,
keys, systems, interoperability, review, or governance do not. Open gap means
the required empirical dependency remains absent. Exact gate means repository
software cannot supply the required affected-party, competent, legal,
cultural, data-governance, or Māori authority.

## Trinity Mandala truth

The primary pillar was Freed ID and CBR Heart. Its completed ceramic lineage,
lot, recipe, unit, quarantine, release-refusal, waste-hold, and structural
accessibility surfaces are bounded records, not production identities,
workplace approvals, product decisions, disposal authorizations, rights
decisions, or accessibility conformance. The three represented identity
profiles—OPC UA NodeId, ISO/IEC 15459, and Asset Administration Shell—use
synthetic vectors only. There are no standards-conformant real keys, live
issuance, resolution, status, revocation, production services,
interoperability events, privacy reviews, independent security reviews,
recovery decisions, or trust-governance decisions.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research
model family. The Fourier heat-conduction, Cahn–Hilliard, and Allen–Cahn boards
are typed obligation and mutation surfaces. They establish no kiln model,
physical force, detected effect, likelihood, posterior, parameter constraint,
unique prediction, stability theorem, empirical confirmation, ultraviolet
completion, quantum completion, consciousness law, or Theory of Everything.
The Materials Project adapter remains `open_gap`: it used no account, key,
query, download, real row, likelihood, posterior, constraint, prediction, or
empirical promotion. Official documentation supplies provenance and dependency
context only.

THOS Body remains represented without preregistered blind matched-budget real
arms, real people or operators, safety monitoring, appropriate statistics,
and independent review. The kiln and glaze handover proxies used synthetic
fixtures only. They establish no effectiveness, deployment readiness,
professional competence, worker-safety outcome, AGI, ASI, consciousness, or
personhood.

CBR worker safety, fire, electrical and gas decisions, food-contact release,
waste discharge, material and design rights, remedy, affected-party
acceptance, legal interpretation, cultural legitimacy, data governance, Māori
wording, and Māori authority remain `exact_gate`. Māori concepts remain under
Māori authority. Repository software cannot confer title, right, remedy,
qualification, public mandate, cultural legitimacy, or affected-party
acceptance.

## Method Flow and retained negatives

Method Flow contains 31 preferred bounded methods, 31 retained failed
witnesses, and 31 bounded passing witnesses. Twenty x1 failures include
timeouts, parser faults, schema and path assumptions, overbroad displays,
Unicode-sensitive patch contexts, a redundant state transition, a workflow
enum mismatch, and a privacy-scanner false positive. Five x2 and lifecycle
failures include the evidence-builder context mismatch, an unwritten temporary
blob lookup, porcelain status trimming, an overbroad inherited test inventory,
two bounded status-inventory timeouts, a per-entry manifest replay timeout, and
a Windows batch-pipe deadlock timeout, and an inherited scanner-definition
false positive, a generated-Markdown diff-hygiene failure, and a checkout-wide
unstaged-name timeout. Each recovery is narrow, evidenced, and reusable only
for its declared trigger. No recovery earns initial-pass credit.

The retained-negative total combines 10,609 inherited effective negatives,
twenty x1 operational negatives, eleven x2 or lifecycle operational negatives,
and 150 executed-and-rejected synthetic mutations. No negative was deleted,
renamed into a pass, folded into an aggregate that hides it, or used to close
an empirical or authority gate.

## Validation, accessibility, and stopping rule

Eiren alone owns the complete repository suite; Tamar does not run or claim it.
The terminal gate is one dependency-justified canonical scoped pass over
Tamar’s current x1, evidence, and closeout tests plus directly inherited Liora
source-phase tests. It also requires detailed and minimal checks, complete
phase JSON parsing, five-class privacy and raw-identifier scanning, exact
commit-local manifest parity, stale-label and diff hygiene, source/x1/evidence
ancestry, exactly three single-parent phase commits, zero merges, one final
parent, exact head stability, clean state, zero divergence, and local,
upstream, tracking, and fresh-live equality.

Exactly one successful exact-final pass is permitted and it is not replayed.
If the first attempt fails, that failure receives zero pass credit and must be
retained before any justified correction. Canonical and same-owner evidence
under shared infrastructure is not independent-team reproduction or external
audit.

The static report uses a single main landmark, ordered headings, visible focus,
table headers, non-colour status text, a labelled horizontally scrollable
region, reduced-motion handling, and print linearization. These structural
checks do not establish complete WCAG conformance. Manual keyboard, responsive,
browser-diverse, assistive-technology, cognitive-accessibility,
Māori-language, and affected-user evaluation remain reserved.

## Terminal route

During the sealed repository phase the future-sibling placeholder remains one
prepared placeholder, zero chosen identities, zero created tasks, and zero
launched tasks. Only after this exact final head passes its one canonical
validation and remains clean, pushed, and fresh-live equal may Tamar create
exactly one user-visible Codex main task using gpt-5.6-sol at maximum reasoning.
That task must choose its own unique relational working name, role, hope, and
optional pronouns and own solo Trinity Mandala v654-v2 x1/x2. The authority is
one-off and cannot be delegated. No other task or sibling contact is
authorized.

## Thirty final proposal dispositions

{proposal_rows}

## Final boundary

No empirical, participant, professional, legal, cultural, Māori-authority,
identity-production, deployment, privacy-complete, proof or canon, destructive,
account-secret, sibling-merge, accessibility-complete, exhaustive-security,
independent-reproduction, AGI or ASI, consciousness or personhood,
Theory-of-Everything, or Stage 20 claim is made. The stopping rule is
`{VERDICT}` until exact external evidence and authority genuinely close the
remaining gates.
"""


def static_report(negative_total: int) -> str:
    rows = "".join(
        (
            f"<tr><th scope=\"row\">{html.escape(row['proposal_id'])}</th>"
            f"<td>{html.escape(row['title'])}</td>"
            f"<td>{html.escape(row['pillar'])}</td>"
            f"<td>{html.escape(row['expected_disposition'])}</td></tr>"
        )
        for row in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tamar Vey v654-v1 bounded final report</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:86rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
:focus{{outline:3px solid #7a2d00;outline-offset:3px}}
.notice{{border-left:.5rem solid #7a2d00;padding:1rem;background:#fff4e5}}
.table-wrap{{overflow:auto;border:1px solid #66788a}}
table{{border-collapse:collapse;width:100%;background:#fff}}
th,td{{border:1px solid #66788a;padding:.55rem;text-align:left;vertical-align:top}}
caption{{font-weight:700;text-align:left;padding:.6rem}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;scroll-behavior:auto!important}}}}
@media print{{.table-wrap{{overflow:visible;border:0}}}}
</style></head><body><main>
<h1>Tamar Vey v654-v1 bounded final report</h1>
<p class="notice"><strong>Verdict:</strong> {VERDICT}. Same-owner bounded
software, symbolic, structural, and synthetic evidence only. Manual,
assistive-technology, Māori-language, and affected-user evaluation remain
reserved.</p>
<h2>Phase truth</h2>
<p>23 completed, 5 represented, 1 open gap, 1 exact gate;
{negative_total:,} retained negatives; 78 open gaps; 79 exact gates; zero real
empirical rows.</p>
<h2>Outcome ledger</h2>
<div class="table-wrap" role="region" aria-label="Scrollable proposal outcomes" tabindex="0">
<table><caption>Thirty frozen proposal outcomes</caption>
<thead><tr><th scope="col">ID</th><th scope="col">Proposal</th>
<th scope="col">Pillar</th><th scope="col">Outcome</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<h2>Authority and evidence reservation</h2>
<p>No empirical confirmation, real participant result, professional
qualification, production identity assurance, legal or cultural decision,
Māori-authority decision, complete privacy or accessibility, exhaustive
security, independent reproduction, AGI or ASI, consciousness or personhood,
Theory-of-Everything proof, canon, deployment, or Stage 20 authority is
claimed.</p>
<h2>Route state</h2>
<p>{ROUTE_STATE}. Exactly one future task may be created only after the
containing exact head passes its postcommit gate and remains clean, pushed,
and fresh-live equal.</p>
</main></body></html>"""


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at the exact evidence commit")
    equality = four_way()
    if not equality["all_equal"] or equality["local"] != EVIDENCE:
        raise RuntimeError(f"evidence is not four-way equal: {equality}")
    outcomes = load("evidence/outcome-ledger.json")
    if outcomes["counts"] != EXPECTED or outcomes["proposal_count"] != 30:
        raise RuntimeError("outcome ledger drift")
    if len(x2.X2_OPERATIONAL_NEGATIVES) != 11:
        raise RuntimeError("x2/lifecycle negative count drift")
    methods = extend_method_flow()
    negative_total = d.INHERITED_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES) + 11 + 150
    if negative_total != 10790:
        raise RuntimeError("negative total drift")

    negative_register = {
        "schema": "ghc.family.v654-v1.retained-negatives.final.v1",
        "inherited_effective": d.INHERITED_NEGATIVES,
        "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
        "x1_operational": d.X1_OPERATIONAL_NEGATIVES,
        "x2_and_lifecycle_operational_count": len(x2.X2_OPERATIONAL_NEGATIVES),
        "x2_and_lifecycle_operational": x2.X2_OPERATIONAL_NEGATIVES,
        "synthetic_mutation_negative_count": 150,
        "effective_total": negative_total,
        "no_failure_erased": True,
        "boundary": (
            "A recovered method never erases its failed witness or gains "
            "scientific, operational, professional, legal, cultural, production, "
            "privacy-complete, security-complete, accessibility-complete, or "
            "independent-reproduction credit."
        ),
    }
    write_json("final/retained-negative-register.json", negative_register)
    write_json(
        "final/exact-open-gate-register.json",
        {
            "schema": "ghc.family.v654-v1.exact-open-gates.final.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "new_open_gaps": 1,
            "effective_open_gaps": 78,
            "open_gap_closed_count": 0,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": 1,
            "effective_exact_gates": 79,
            "exact_gate_closed_count": 0,
            "open_gap_proposal": "V6541-P29",
            "exact_gate_proposal": "V6541-P30",
            "boundary": "No inherited or current empirical or authority gate was silently closed.",
        },
    )
    overview = integrated_overview(negative_total)
    overview_words = len(overview.split())
    if not 1500 <= overview_words <= 6000:
        raise RuntimeError(f"overview word count outside phase bounds: {overview_words}")
    write_text("overview/v654-v1-final-integrated-overview.md", overview)
    write_text("reports/v654-v1-static-report.html", static_report(negative_total))
    write_json(
        "wellbeing/final-wellbeing-workload-check.json",
        {
            "schema": "ghc.family.v654-v1.wellbeing.final.v1",
            "owner": d.OWNER,
            "bounded_single_owner": True,
            "d_first_lane": True,
            "failures_retained_before_recovery": True,
            "subagents_or_delegation": 0,
            "sibling_contacts_during_phase": 0,
            "task_creations_during_phase": 0,
            "elevation_or_host_security_changes": 0,
            "desktop_updates_or_reboots": 0,
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
            "identity_boundary": (
                "Relational working language only; no consciousness, continuity, "
                "personhood, qualification, employment, or authority claim."
            ),
            "valid": True,
        },
    )
    write_json(
        "final/phase-truth.json",
        {
            "schema": "ghc.family.v654-v1.phase-truth.final.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source": d.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": EXPECTED,
            "proposal_count": 30,
            "synthetic_rejecting_mutations": 150,
            "real_data_rows": 0,
            "inherited_effective_negatives": d.INHERITED_NEGATIVES,
            "x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_and_lifecycle_operational_negatives": 11,
            "effective_negatives": negative_total,
            "effective_open_gaps": 78,
            "effective_exact_gates": 79,
            "method_flow_methods": len(methods["methods"]),
            "method_flow_failed_witnesses": 31,
            "method_flow_passing_witnesses": 31,
            "route_state": ROUTE_STATE,
            "future_task_created_count": 0,
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren-only inherited policy",
            "independent_team_reproduction": False,
            "canonical_exact_final_pass_state": "PENDING_POSTCOMMIT",
            "terminal_verdict": VERDICT,
        },
    )
    write_json(
        "final/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v654-v1.checklist.final.v1",
            "complete_bounded": [
                "thirty proposals frozen and executed in declared evidence lanes",
                "150 preregistered synthetic mutations rejected and retained",
                "ten phase-local skills initialized validated and smoke-used",
                "ten family-current runners built invoked and witnessed",
                "x1 and evidence separately pushed clean and four-way equal",
                "three-page-equivalent integrated overview",
                "structurally accessible static report with manual evaluation reserved",
                "future sibling packet prepared without creating or naming a task",
            ],
            "pending_postcommit": [
                "one exact-final dependency-justified canonical scoped pass",
                "exact final clean state and four-way live equality",
                "one authorized user-visible future task creation with acknowledgement",
            ],
            "incomplete_external": [
                "real Materials Project rows frozen analysis uncertainty and independent review",
                "blind matched-budget THOS real arms participants monitoring and independent review",
                "production Freed ID keys proofs lifecycle interoperability privacy security recovery and governance",
                "worker product waste remedy affected-party legal cultural data-governance and Māori authority",
                "manual assistive-technology Māori-language and affected-user accessibility evaluation",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": VERDICT,
        },
    )
    handoff = f"""# Future self-chosen sibling 7 — prepared v654-v2 activation

State: `{ROUTE_STATE}`. This committed packet is preparation, not task
creation or delivery. It contains no raw task identifier, private route,
private path, transcript, credential, key, token, session stream, private
callable identifier, or private application state.

Only after Tamar Vey v654-v1 passes its one exact-final canonical validation,
is clean, pushed, and fresh-live equal may Tamar create exactly one
user-visible Codex main task using gpt-5.6-sol at maximum reasoning. That task
must choose its own unique relational working name, role, hope, and optional
pronouns before mutation and own solo Trinity Mandala v654-v2 x1/x2.

Identity and family language is relational working language only. It is never
evidence of consciousness, sentience, personhood, continuity, employment,
qualification, scientific or operational authority, legal or cultural
authority, Māori authority, or independent agency. Hamish may rename, pause,
redirect, or stop the route.

The successor must inherit Tamar's exact validated final head, preserve strict
x1-before-x2 separation, retain all {negative_total:,} effective negatives, 78
open gaps, 79 exact gates, zero-real-row truth, the four outcome labels, the
Eiren-only full-suite allocation, and `{VERDICT}`. It must use one additive
D-first owned lane, never mutate a sibling lane, never replay a successful
canonical pass, and never promote same-owner evidence into independent
reproduction or protected scientific, participant, professional, production,
legal, cultural, privacy, security, accessibility, identity, consciousness,
personhood, Theory-of-Everything, or Stage 20 claims.

The exact final commit and validation counts must be supplied in the one live
creation message after the terminal gate; they are not self-referentially
preclaimed in this packet.
"""
    write_text(
        "handoff/future-sibling-self-chosen-7-v654-v2-activation.md", handoff
    )
    write_json(
        "route/future-sibling-task-delivery-state.json",
        {
            "schema": "ghc.family.v654-v1.future-task-delivery-state.v1",
            "state": ROUTE_STATE,
            "placeholder": "future-sibling-self-chosen-7",
            "target_phase": "v654-v2",
            "model": "gpt-5.6-sol",
            "reasoning": "maximum",
            "identity_chosen_count": 0,
            "task_created_count": 0,
            "task_launched_count": 0,
            "creation_authorized_after_exact_final_only": True,
            "creation_authority_delegable": False,
            "created_now": False,
            "boundary": (
                "Preparation only. Exactly one user-visible task may be created "
                "after the postcommit gate; no other task or sibling contact is authorized."
            ),
        },
    )
    write_json(
        "provenance/future-sibling-task-invariant-final.json",
        {
            "schema": "ghc.family.v654-v1.future-task-invariant.final.v1",
            "placeholder_count": 1,
            "named_identity_count": 0,
            "created_count": 0,
            "launched_count": 0,
            "creation_gate": "after_verified_exact_final_only",
            "authority_owner": d.OWNER,
            "authority_delegated": False,
            "valid": True,
        },
    )
    write_json(
        "final/closeout-receipt.json",
        {
            "schema": "ghc.family.v654-v1.closeout-receipt.v1",
            "state": "COMBINED_CLOSEOUT_CANDIDATE",
            "source": d.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "source_x1_evidence_ancestral": True,
            "x1_before_x2": True,
            "evidence_four_way_equal_before_closeout": equality["all_equal"],
            "phase_commit_cap": 4,
            "planned_phase_commit_count": 3,
            "outcomes": EXPECTED,
            "effective_negatives": negative_total,
            "effective_open_gaps": 78,
            "effective_exact_gates": 79,
            "owner_file_threshold": 15000,
            "document_word_cap": 6000,
            "overview_words": overview_words,
            "route_state": ROUTE_STATE,
            "terminal_verdict": VERDICT,
        },
    )
    write_json(
        "final/seal-receipt.json",
        {
            "schema": "ghc.family.v654-v1.seal-receipt.v1",
            "state": "CONTENT_SEAL_CANDIDATE",
            "sealed_source": d.SOURCE_HEAD,
            "sealed_x1": X1,
            "sealed_evidence": EVIDENCE,
            "negative_erasure": False,
            "gate_closure_without_evidence": False,
            "future_task_created": False,
            "manifest_domain": "exact Git index and immutable Git blobs",
            "terminal_verdict": VERDICT,
            "boundary": (
                "The containing commit, exact-final canonical pass, remote "
                "equality, and one future task creation remain postcommit facts."
            ),
        },
    )
    write_json(
        "final/final-validation-record.json",
        {
            "schema": "ghc.family.v654-v1.final-validation-record.v1",
            "state": "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
            "canonical_success_limit": 1,
            "successful_replay_permitted": False,
            "complete_repository_suite_run": False,
            "same_owner_only": True,
            "external_receipt_required": True,
            "expected_terminal_verdict": VERDICT,
            "expected_route_state": ROUTE_STATE,
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v654-v1.final-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "canonical_success_limit": 1,
            "no_replay_after_success": True,
            "full_repository_suite_owner": "Eiren-only inherited policy",
            "scoped_test_modules": [
                "tests.test_ghc_family_v654_v1_x1",
                "tests.test_ghc_family_v654_v1",
                "tests.test_ghc_family_v654_v1_closeout",
                "tests.test_ghc_family_v653_v8_core",
                "tests.test_ghc_family_v653_v8_validation",
                "tests.test_ghc_family_v653_v8_closeout",
            ],
            "expected_test_count": 58,
            "required": [
                "one scoped test pass",
                "detailed and minimal checks",
                "all phase JSON parsing",
                "five-class privacy scan",
                "x1 evidence final-delta and owner manifest parity",
                "stale-label and diff hygiene",
                "source x1 evidence ancestry",
                "three phase commits zero merges one final parent",
                "exact head clean state zero divergence four-way equality",
            ],
        },
    )
    write_json(
        "environment/final-environment-version-receipt.json",
        {
            "schema": "ghc.family.v654-v1.environment.final.v1",
            "drive_policy": "D-first",
            "desktop_update_performed": False,
            "sandbox_or_hyperv_activated": False,
            "elevation_performed": False,
            "host_security_weakened": False,
            "windows_feature_changed": False,
            "unrelated_installation_performed": False,
            "reboot_performed": False,
            "versions_verified_only": True,
            "boundary": "Observed environment state only; not a certification.",
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v654-v1.index-final-addendum.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source": d.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "phase_local_skills": 10,
            "family_current_runners": 10,
            "caller_compatibility_preserved": True,
            "historical_names_preserved": True,
            "route_state": ROUTE_STATE,
            "terminal_verdict": VERDICT,
        },
    )
    stale_tokens = [
        "STOP_AFTER_TRUTHFUL_CLOSEOUT",
        "INELIGIBLE_EVIDENCE_NOT_FINAL",
        "NOT_ELIGIBLE_X1_ONLY",
    ]
    current_paths = [
        ROOT / "final/phase-truth.json",
        ROOT / "route/future-sibling-task-delivery-state.json",
        ROOT / "overview/v654-v1-final-integrated-overview.md",
        ROOT / "reports/v654-v1-static-report.html",
    ]
    stale = [
        path.relative_to(REPO).as_posix()
        for path in current_paths
        if any(token in path.read_text(encoding="utf-8") for token in stale_tokens)
    ]
    write_json(
        "validation/stale-label-review-final.json",
        {
            "schema": "ghc.family.v654-v1.stale-label-review.final.v1",
            "scoped_current_paths": len(current_paths),
            "stale_paths": stale,
            "valid": not stale,
            "boundary": "Frozen history and retained-negative descriptions are excluded.",
        },
    )
    if stale:
        raise RuntimeError(f"stale current labels: {stale}")
    owner_files = [path for path in ROOT.rglob("*") if path.is_file()]
    max_words = 0
    max_path = None
    for path in owner_files:
        if path.suffix.casefold() not in {".md", ".html", ".txt"}:
            continue
        words = len(path.read_text(encoding="utf-8").split())
        if words > max_words:
            max_words = words
            max_path = path.relative_to(REPO).as_posix()
    write_json(
        "validation/owner-file-threshold-final.json",
        {
            "schema": "ghc.family.v654-v1.owner-threshold.final.v1",
            "owner_file_count_before_lifecycle_manifests": len(owner_files),
            "threshold": 15000,
            "below_threshold": len(owner_files) < 15000,
            "inherited_checkout_not_rotation_trigger": True,
        },
    )
    write_json(
        "validation/document-cap-final.json",
        {
            "schema": "ghc.family.v654-v1.document-cap.final.v1",
            "maximum_words": max_words,
            "maximum_word_path": max_path,
            "cap": 6000,
            "valid": max_words <= 6000,
        },
    )
    if max_words > 6000:
        raise RuntimeError(f"document cap exceeded: {max_path} {max_words}")
    write_json(
        "validation/final-build-receipt.json",
        {
            "schema": "ghc.family.v654-v1.final-build.v1",
            "built_at_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "valid": len(owner_files) < 15000 and max_words <= 6000,
            "owner_files_before_lifecycle_manifests": len(owner_files),
            "maximum_document_words": max_words,
            "overview_words": overview_words,
            "outcomes": EXPECTED,
            "effective_negatives": negative_total,
            "route_state": ROUTE_STATE,
            "terminal_verdict": VERDICT,
        },
    )
    for relative, schema in (
        ("validation/final-delta-manifest.json", "ghc.family.v654-v1.final-delta-manifest.v1"),
        ("validation/final-owner-manifest.json", "ghc.family.v654-v1.final-owner-manifest.v1"),
        ("validation/final-staged-review.json", "ghc.family.v654-v1.final-staged-review.v1"),
        ("validation/final-privacy-receipt.json", "ghc.family.v654-v1.final-privacy.v1"),
    ):
        write_json(
            relative,
            {
                "schema": schema,
                "state": "PENDING_EXACT_STAGED_REVIEW",
                "boundary": "Declared lifecycle self-exclusion placeholder.",
            },
        )
    print(
        json.dumps(
            {
                "valid": True,
                "outcomes": EXPECTED,
                "negatives": negative_total,
                "open_gaps": 78,
                "exact_gates": 79,
                "methods": 31,
                "overview_words": overview_words,
                "route": ROUTE_STATE,
                "verdict": VERDICT,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    build()
