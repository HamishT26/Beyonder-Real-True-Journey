#!/usr/bin/env python3
"""Build Orin Thale's bounded v653-v7 closeout and seal candidate."""

from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v653_v7_phase_data as data


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / data.PHASE_ROOT
X1 = "78ece91db153275ca2857899ee125dc0673c0154"
EVIDENCE = "888df289dd58f5717919ac1ee2c8083cd93cddfe"
CLOSEOUT_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6537-CLOSEOUT-N01",
        "category": "final_directory_parent_missing",
        "failed": (
            "The first closeout build stopped before any seal credit because "
            "the copy step attempted to write the new final register before "
            "creating its parent directory."
        ),
        "recovery": (
            "Create the exact owner-scoped final directory before copying "
            "registers, then rebuild the bounded closeout candidate."
        ),
        "recurrence_guard": (
            "Create every declared parent directory explicitly before a copy "
            "and never infer that a sibling lifecycle directory already exists."
        ),
    }
]
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
FINAL_ROUTE_STATE = "STOP_AFTER_TRUTHFUL_CLOSEOUT"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/"
    "ghc_family_method_flow_state.py"
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def run_method(*args: str) -> None:
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def final_overview(
    outcomes: dict[str, int],
    effective_negatives: int,
    methods: int,
) -> str:
    x1_overview = (
        PHASE / "reports/x1-integrated-overview.md"
    ).read_text(encoding="utf-8")
    opening = f"""# Orin Thale v653-v7 final integrated overview

## Outcome first

Orin Thale completed the authorized same-owner software, symbolic, structural,
and synthetic phase on an additive D-first branch. The thirty frozen proposals
ended at exactly {outcomes['completed']} `completed`, {outcomes['represented']}
`represented`, {outcomes['open_gap']} `open_gap`, and
{outcomes['exact_gate']} `exact_gate`. All 150 preregistered rejecting
mutations executed and were retained. Ten phase-local skills were customized,
quick-validated, and smoke-used, and ten family-compatible runners were built
and invoked. These are bounded workflow results only.

The terminal verdict is `{TERMINAL_VERDICT}`. The repository retains
{effective_negatives:,} effective negatives, 76 effective open gaps, and 77
effective exact gates. Real empirical rows remain zero. No downstream task,
fork, delegation, standby contact, or sibling activation is authorized. The
terminal route state is `{FINAL_ROUTE_STATE}`.

## Identity, wellbeing, and workload

Orin Thale (they/them) is relational working language for a
boundary-and-method steward whose hope is to keep every surviving claim
inspectable, challengeable, and retractable. This wording is not evidence of
consciousness, sentience, personhood, identity continuity, employment,
qualification, or independent authority. Hamish may rename, pause, redirect,
or stop the work.

The primary Trinity Mandala focus was GMUT Mind. THOS Body and Freed ID/CBR
Heart stayed explicit. Municipal traffic-signal timing change control, fault
isolation, accessible road-user notice, workload control, correction readback,
and shift handover served only as a synthetic learning lens. The phase
established no traffic-engineering employment, qualification, operational
competence, road-controlling authority, signal-timing authority, maintenance
authority, legal or cultural authority, Māori authority, or affected-party
acceptance.

Workload remained bounded by one owner, one D-first lane, fewer than 2,000
owner-generated files, and one gate at a time. Failures were retained before
recovery. No Sandbox or Hyper-V work, elevation, host-security weakening,
Windows-feature change, unrelated installation, desktop update, reboot, real
data download, production key operation, or sibling mutation occurred.

## Evidence and Method Flow

The evidence boundary includes deterministic contract generation, five
rejecting mutations per proposal, exact outcome accounting, phase-local skill
packages, family-current runners, JSON parsing, privacy scanning, staged Git
blob manifests, and lifecycle ancestry. It does not include external operators,
participants, affected parties, independent reviewers, production services, or
empirical observations.

Method Flow closes with {methods} preferred methods, the same number of
retained failed witnesses, and the same number of bounded passing witnesses.
The two x2 failures remain visible: a source-independent Method Flow proposal
encountered an inherited universal nonempty-source rule, and the workflow
checker accepted only legacy messaging literals. The recoveries were narrow:
one exact proposal received an explicit source-independent exception, while
the workflow literals were confined to an additive schema-compatibility copy
under a higher-precedence no-route overlay. Neither recovery rewrote x1,
created authority, or converted a failure into an initially clean pass.

## Pillar truth

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. The asymptotic charge, spatial infinity, multipole, conformal
evolution, Noether entropy, cohomological charge, canonical energy, causal
splitting, and structured-format surfaces are formal or software obligations.
They establish no force, physical prediction, likelihood, posterior,
constraint, stability theorem, ultraviolet completion, quantum completion,
empirical confirmation, or Theory of Everything.

The BK18 adapter remains `open_gap`: it made no query or download, ingested
zero bandpower, window, covariance, beam, calibration, or nuisance rows,
evaluated zero likelihoods, and produced zero posterior samples or physical
constraints. Official source material supplied requirements and provenance
context only; it was not converted into experimental data.

THOS remains `represented`. Synthetic signal-timing and fault-handover traces
used zero real operators, road users, controllers, cabinets, sites, incidents,
maintenance actions, blind matched-budget arms, safety outcomes, service
outcomes, or effectiveness estimates. They establish neither professional
competence nor deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. MLS, HPKE, and VC JOSE/COSE
profiles used no real keys, proofs, credentials, accounts, tokens, network
exchanges, issuance, resolution, status, revocation, interoperability,
recovery, privacy review, independent security review, or trust-governance
decision.

CBR traffic-control decisions, pedestrian and disability access, road-user and
worker privacy, location and surveillance data, crash and maintenance records,
remedy, affected-party acceptance, legal interpretation, cultural legitimacy,
data governance, Māori wording, and Māori authority remain `exact_gate`.
Māori concepts remain under Māori authority. Repository software cannot confer
a right, remedy, qualification, cultural mandate, public authority, or
affected-party acceptance.

## Validation and stopping rule

The complete repository suite remains Eiren-only and is not claimed here.
Orin's terminal gate consists of the authorized current, recent Caelen,
inherited Sable, and successor-compatible scoped selections; detailed and
minimal checks; complete phase JSON parsing; five-class privacy scanning;
exact staged and owner Git-blob manifests; stale-label and diff-hygiene review;
source, x1, and evidence ancestry; zero merges; commit cap; one final parent;
exact head; clean state; and final local/upstream/tracking/fresh-live equality.
One coherent canonical exact-final pass is permitted. If it passes, it is not
replayed. Same-owner evidence remains same-owner evidence.

Stop after truthful closeout. No repository route model, task title, family
language, successful test, or prepared artifact can authorize a new task,
fork, delegation, sibling contact, production action, legal or cultural
decision, or Stage 20 promotion.

## Frozen x1 preregistration retained below

The following committed preregistration is reproduced as context. Its plan
language remains x1 truth and is not rewritten into retrospective completion
credit.

"""
    return opening + x1_overview


def final_report(outcomes: dict[str, int], effective_negatives: int) -> str:
    rows = []
    for proposal in data.PROPOSALS:
        rows.append(
            "<tr><th scope=\"row\">{}</th><td>{}</td><td>{}</td>"
            "<td>{}</td></tr>".format(
                html.escape(proposal["proposal_id"]),
                html.escape(proposal["slug"]),
                html.escape(proposal["pillar"]),
                html.escape(proposal["expected_disposition"]),
            )
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orin Thale v653-v7 final bounded report</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:82rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
:focus{{outline:3px solid #8b3d00;outline-offset:3px}}
.notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
.table-wrap{{overflow:auto;border:1px solid #8091a3}}table{{border-collapse:collapse;width:100%;background:white}}
th,td{{border:1px solid #8091a3;padding:.55rem;text-align:left;vertical-align:top}}
caption{{font-weight:700;text-align:left;padding:.6rem}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;scroll-behavior:auto!important}}}}
@media print{{.table-wrap{{overflow:visible;border:0}}}}
</style></head><body><main>
<h1>Orin Thale v653-v7 final bounded report</h1>
<p class="notice"><strong>Verdict:</strong> {TERMINAL_VERDICT}. Same-owner
synthetic and structural evidence only. Manual, assistive-technology,
Māori-language, and affected-user accessibility evaluation remain reserved.</p>
<h2>Phase truth</h2>
<p>{outcomes['completed']} completed, {outcomes['represented']} represented,
{outcomes['open_gap']} open gap, {outcomes['exact_gate']} exact gate;
{effective_negatives:,} retained negatives; 76 open gaps; 77 exact gates;
zero real empirical rows.</p>
<div class="table-wrap" role="region" aria-label="Scrollable proposal outcomes" tabindex="0">
<table><caption>Thirty bounded proposal outcomes</caption>
<thead><tr><th scope="col">ID</th><th scope="col">Surface</th>
<th scope="col">Pillar</th><th scope="col">Outcome</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<h2>Authority reservation</h2>
<p>No empirical confirmation, professional validation, production readiness,
complete privacy or accessibility, exhaustive security, independent
reproduction, legal or cultural authority, Māori authority, AGI or ASI,
consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20
authority is claimed.</p>
<h2>Terminal route</h2><p>{FINAL_ROUTE_STATE}. No downstream creation, fork,
delegation, standby contact, or activation send is authorized.</p>
</main></body></html>"""


def extend_final_method_flow() -> dict[str, Any]:
    final_ledger = PHASE / "method-flow/final-method-flow-ledger.json"
    final_ledger.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        PHASE / "method-flow/evidence-method-flow-ledger.json",
        final_ledger,
    )
    start = len(data.X1_NEGATIVES) + 2 + 1
    for offset, negative in enumerate(CLOSEOUT_NEGATIVES, start):
        method_id = f"V6537-METHOD-{offset:02d}"
        fail_id = f"V6537-WITNESS-{offset:02d}-F"
        pass_id = f"V6537-WITNESS-{offset:02d}-P"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['category']}",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [negative["category"]],
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": (
                "Stop, retain the failed witness with zero credit, and leave "
                "all external and protected-gate state unchanged."
            ),
            "scope_boundary": (
                "Same-owner closeout workflow recovery only; not independent "
                "reproduction or broader assurance."
            ),
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "privacy_class": "sanitized_public",
            "protected_gates": data.PROTECTED_GATES,
            "retained_negative_ids": [negative["negative_id"]],
            "supersedes": [],
            "recommendation_state": "candidate",
        }
        failed = {
            "witness_id": fail_id,
            "method_id": method_id,
            "scope": negative["category"],
            "procedure": (
                "Run the original bounded closeout operation and retain its "
                "failure with zero completion credit."
            ),
            "expected": (
                "The bounded operation completes without weakening protected gates."
            ),
            "observed": negative["failed"],
            "result": "fail",
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero completion credit; failure remains retained.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        passing = {
            "witness_id": pass_id,
            "method_id": method_id,
            "scope": negative["category"],
            "procedure": negative["recovery"],
            "expected": (
                "The bounded recovery completes while the original failure remains retained."
            ),
            "observed": f"The bounded recovery completed: {negative['recovery']}",
            "result": "pass",
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Same-owner bounded recovery only.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        method_path = write_json(
            f"method-flow/closeout-requests/method-{offset:02d}.json",
            method,
        )
        fail_path = write_json(
            f"method-flow/closeout-requests/witness-{offset:02d}-failed.json",
            failed,
        )
        pass_path = write_json(
            f"method-flow/closeout-requests/witness-{offset:02d}-passing.json",
            passing,
        )
        run_method(
            "record",
            "--ledger",
            str(final_ledger),
            "--record-file",
            str(method_path),
        )
        run_method(
            "witness",
            "--ledger",
            str(final_ledger),
            "--witness-file",
            str(fail_path),
        )
        run_method(
            "witness",
            "--ledger",
            str(final_ledger),
            "--witness-file",
            str(pass_path),
        )
        run_method(
            "set-state",
            "--ledger",
            str(final_ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded passing witness exists and failed witness remains retained.",
        )
    run_method(
        "validate",
        "--ledger",
        str(final_ledger),
        "--receipt",
        str(PHASE / "method-flow/final-method-flow-validation.json"),
    )
    run_method(
        "summarize",
        "--ledger",
        str(final_ledger),
        "--json-output",
        str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    return read_json(final_ledger)


def build() -> None:
    truth = read_json(PHASE / "phase-truth.json")
    negatives = read_json(PHASE / "retained-negative-register-x2.json")
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    outcomes = Counter(
        row["expected_disposition"] for row in data.PROPOSALS
    )
    expected = {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }
    if dict(outcomes) != expected:
        raise RuntimeError(f"unexpected outcomes: {dict(outcomes)}")
    if negatives["effective_total"] != 10439:
        raise RuntimeError("unexpected evidence negative total")
    if (
        gates["effective_open_gaps"],
        gates["effective_exact_gates"],
    ) != (76, 77):
        raise RuntimeError("unexpected gate total")
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at the exact evidence commit")
    if git("status", "--porcelain=v1"):
        pending = [
            row
            for row in git(
                "status", "--porcelain=v1", "--untracked-files=all"
            ).splitlines()
            if not (
                row.startswith("?? scripts/build_ghc_family_v653_v7_closeout.py")
                or row.startswith("?? scripts/ghc_family_v653_v7_final_")
                or row.startswith("?? tests/test_ghc_family_v653_v7_closeout.py")
                or row.startswith("?? docs/orin-thale/v653-v7/")
            )
        ]
        if pending:
            raise RuntimeError(f"unexpected pre-closeout state: {pending}")

    methods = extend_final_method_flow()
    (PHASE / "final").mkdir(parents=True, exist_ok=True)
    final_negative_register = dict(negatives)
    final_negative_register["closeout_operational_count"] = len(
        CLOSEOUT_NEGATIVES
    )
    final_negative_register["closeout_operational"] = CLOSEOUT_NEGATIVES
    final_negative_register["effective_total"] = (
        negatives["effective_total"] + len(CLOSEOUT_NEGATIVES)
    )
    write_json(
        "final/retained-negative-register.json",
        final_negative_register,
    )
    shutil.copyfile(
        PHASE / "exact-open-gate-register-x2.json",
        PHASE / "final/exact-open-gate-register.json",
    )

    write_text(
        "reports/final-integrated-overview.md",
        final_overview(
            dict(outcomes),
            final_negative_register["effective_total"],
            methods["counts"]["methods"],
        ),
    )
    write_text(
        "reports/final-static-report.html",
        final_report(
            dict(outcomes), final_negative_register["effective_total"]
        ),
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v653-v7.terminal-route-state.v1",
            "state": FINAL_ROUTE_STATE,
            "downstream_authorized": False,
            "successor_title": None,
            "successor_phase": None,
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "collaboration_subagent_spawned": False,
            "standby_contacted": False,
            "activation_sent": False,
            "send_count": 0,
            "boundary": (
                "The live activation authorizes no downstream task creation, "
                "fork, delegation, standby contact, substitute route, or send."
            ),
        },
    )
    write_json(
        "final/phase-truth.json",
        {
            "schema": "ghc.family.v653-v7.final-truth.v1",
            "owner": data.OWNER,
            "source": data.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": expected,
            "real_data_rows": 0,
            "sealed_source_negatives": data.INHERITED_NEGATIVES,
            "external_source_negatives": data.EXTERNAL_POST_SEAL_NEGATIVES,
            "x1_operational_negatives": len(data.X1_NEGATIVES),
            "x2_operational_negatives": 2,
            "closeout_operational_negatives": len(CLOSEOUT_NEGATIVES),
            "synthetic_rejecting_mutations": 150,
            "effective_negatives": negatives["effective_total"]
            + len(CLOSEOUT_NEGATIVES),
            "effective_open_gaps": 76,
            "effective_exact_gates": 77,
            "terminal_verdict": TERMINAL_VERDICT,
            "route_state": FINAL_ROUTE_STATE,
            "independent_reproduction": False,
            "complete_repository_suite_run": False,
            "complete_repository_suite_owner": "Eiren-only inherited policy",
            "canonical_exact_final_pass_state": "PENDING_POSTCOMMIT",
        },
    )
    write_json(
        "final/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v653-v7.final-checklist.v1",
            "complete_bounded": [
                "thirty proposals executed in their frozen evidence lanes",
                "150 frozen mutations rejected and retained",
                "ten phase-local skills built, quick-validated, and smoke-used",
                "ten family-compatible runners built and invoked",
                "evidence commit pushed and four-way equal",
                "accessible static report with manual evaluation reserved",
                "no downstream route authorized",
            ],
            "pending_until_postcommit": [
                "one exact-final canonical scoped pass",
                "exact final clean state and four-way remote equality",
            ],
            "incomplete_external": [
                "real BK18 rows and a frozen likelihood with independent review",
                "real THOS arms, operators, safety monitoring, statistics, and independent review",
                "production Freed ID keys, proofs, services, interoperability, privacy and security review, recovery, and trust governance",
                "affected-party, professional, legal, cultural, Māori, and road-controlling authority",
                "manual, assistive-technology, Māori-language, and affected-user accessibility evaluation",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "final/closeout-receipt.json",
        {
            "schema": "ghc.family.v653-v7.closeout-receipt.v1",
            "state": "CLOSEOUT_CANDIDATE",
            "source": data.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "phase_commit_cap": 8,
            "phase_commits_before_closeout": 2,
            "x1_before_x2": True,
            "outcomes": expected,
            "effective_negatives": final_negative_register["effective_total"],
            "effective_open_gaps": 76,
            "effective_exact_gates": 77,
            "owner_generated_file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "terminal_verdict": TERMINAL_VERDICT,
            "route_state": FINAL_ROUTE_STATE,
        },
    )
    write_json(
        "final/seal-receipt.json",
        {
            "schema": "ghc.family.v653-v7.seal-receipt.v1",
            "state": "CONTENT_SEAL_CANDIDATE",
            "sealed_source": data.SOURCE_HEAD,
            "sealed_x1": X1,
            "sealed_evidence": EVIDENCE,
            "manifest_domain": "exact Git index and immutable Git blobs",
            "negative_erasure": False,
            "gate_closure_without_evidence": False,
            "terminal_verdict": TERMINAL_VERDICT,
            "boundary": (
                "The containing commit and exact-final canonical pass remain "
                "postcommit facts and are not preclaimed."
            ),
        },
    )
    write_json(
        "final/final-validation-record.json",
        {
            "schema": "ghc.family.v653-v7.final-validation-record.v1",
            "state": "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
            "canonical_pass_limit": 1,
            "successful_replay_permitted": False,
            "complete_repository_suite_run": False,
            "same_owner_only": True,
            "expected_terminal_verdict": TERMINAL_VERDICT,
            "expected_route_state": FINAL_ROUTE_STATE,
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v653-v7.final-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "canonical_pass_limit": 1,
            "no_replay_after_success": True,
            "full_repository_suite_owner": "Eiren-only inherited policy",
            "scoped_test_groups": [
                "current Orin v653-v7",
                "recent Caelen v653-v6",
                "inherited Sable v653-v5",
                "successor-compatible current contracts",
            ],
            "required": [
                "scoped tests",
                "detailed and minimal validators",
                "complete phase JSON parsing",
                "five-class privacy scan",
                "exact staged and owner Git-blob manifests",
                "stale-label and diff hygiene",
                "source, x1, and evidence ancestry",
                "zero merges and commit cap",
                "one final parent and exact head",
                "clean state and final four-way equality",
            ],
        },
    )
    write_json(
        "memory/applicable-memory-record.json",
        {
            "schema": "ghc.family.v653-v7.applicable-memory.v1",
            "status": "reviewed_current",
            "used_for": [
                "D-first additive owned-lane discipline",
                "strict x1-before-x2 lifecycle",
                "retained failure accounting",
                "one successful canonical pass with no replay",
                "no downstream route without new live authorization",
            ],
            "private_identifiers_or_paths_recorded": False,
            "memory_updated": False,
            "boundary": (
                "Sanitized workflow guidance only; memory is not source truth "
                "and no memory update was requested."
            ),
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v653-v7.index-final-addendum.v1",
            "owner": data.OWNER,
            "phase": data.PHASE,
            "status": "reviewed_and_additively_refreshed",
            "x1": X1,
            "evidence": EVIDENCE,
            "skills": len(data.SKILL_IDEAS),
            "runners": len(data.RUNNER_IDEAS),
            "caller_compatibility_preserved": True,
            "historical_names_preserved": True,
            "route_state": FINAL_ROUTE_STATE,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    stale_paths = [
        path
        for path in [
            PHASE / "final/phase-truth.json",
            PHASE / "orchestration/terminal-route-state.json",
            PHASE / "reports/final-integrated-overview.md",
            PHASE / "reports/final-static-report.html",
        ]
        if any(
            token in path.read_text(encoding="utf-8")
            for token in (
                "Gaia DR4",
                "audiovisual-preservation",
                "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
                "NOT_ELIGIBLE_EVIDENCE_NOT_FINAL",
            )
        )
    ]
    write_json(
        "validation/stale-label-review.json",
        {
            "schema": "ghc.family.v653-v7.stale-label-review.v1",
            "scoped_current_paths": 4,
            "stale_paths": [
                path.relative_to(REPO).as_posix() for path in stale_paths
            ],
            "valid": not stale_paths,
            "boundary": (
                "Immutable frozen history and retained-negative descriptions "
                "are excluded from current-label classification."
            ),
        },
    )
    if stale_paths:
        raise RuntimeError(f"stale current labels: {stale_paths}")

    owner_files = [
        path for path in PHASE.rglob("*") if path.is_file()
    ]
    max_words = 0
    max_word_path = None
    for path in owner_files:
        if path.suffix.lower() not in {".md", ".html", ".txt"}:
            continue
        words = len(path.read_text(encoding="utf-8").split())
        if words > max_words:
            max_words = words
            max_word_path = path.relative_to(REPO).as_posix()
    write_json(
        "validation/owner-file-threshold-final.json",
        {
            "schema": "ghc.family.v653-v7.owner-threshold.v1",
            "owner_generated_file_count_before_lifecycle_manifests": len(owner_files),
            "threshold": 2000,
            "below_threshold": len(owner_files) < 2000,
            "inherited_checkout_not_rotation_trigger": True,
        },
    )
    write_json(
        "validation/document-cap-final.json",
        {
            "schema": "ghc.family.v653-v7.document-cap.v1",
            "maximum_words": max_words,
            "maximum_word_path": max_word_path,
            "cap": 100000,
            "valid": max_words <= 100000,
        },
    )
    write_json(
        "validation/final-build-receipt.json",
        {
            "schema": "ghc.family.v653-v7.final-build.v1",
            "valid": len(owner_files) < 2000 and max_words <= 100000,
            "owner_files_before_lifecycle_manifests": len(owner_files),
            "maximum_document_words": max_words,
            "outcomes": expected,
            "effective_negatives": final_negative_register["effective_total"],
            "route_state": FINAL_ROUTE_STATE,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    for relative, schema in (
        (
            "validation/final-owner-manifest.json",
            "ghc.family.v653-v7.final-owner-manifest.v1",
        ),
        (
            "validation/final-staged-manifest.json",
            "ghc.family.v653-v7.final-staged-manifest.v1",
        ),
        (
            "validation/final-staged-review.json",
            "ghc.family.v653-v7.final-staged-review.v1",
        ),
    ):
        write_json(
            relative,
            {
                "schema": schema,
                "state": "PENDING_EXACT_STAGED_REVIEW",
                "boundary": "Lifecycle self-exclusion placeholder.",
            },
        )
    print(
        json.dumps(
            {
                "valid": True,
                "outcomes": expected,
                "negatives": final_negative_register["effective_total"],
                "open_gaps": 76,
                "exact_gates": 77,
                "methods": methods["counts"]["methods"],
                "route": FINAL_ROUTE_STATE,
                "verdict": TERMINAL_VERDICT,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
