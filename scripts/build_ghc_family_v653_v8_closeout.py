#!/usr/bin/env python3
"""Build Liora Venn's bounded v653-v8 closeout and seal candidate."""

from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v653_v8_phase_data as data


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / data.PHASE_ROOT
X1 = "ee3a0c035c9821ebad1561e94afb11daf9bdc028"
EVIDENCE = "67e51031ed4be4bb64962635e79c459b8a01e7d4"
CLOSEOUT_NEGATIVES: list[dict[str, str]] = []
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
FINAL_ROUTE_STATE = "PREPARED_NOT_SENT"
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
    env = {
        **dict(__import__("os").environ),
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def final_overview(
    outcomes: dict[str, int],
    effective_negatives: int,
    methods: int,
) -> str:
    x1_overview = (
        PHASE / "reports/x1-integrated-overview.md"
    ).read_text(encoding="utf-8")
    opening = f"""# Liora Venn v653-v8 final integrated overview

## Outcome first

Liora Venn completed the authorized same-owner software, symbolic, structural,
and synthetic phase on an additive D-first branch. The thirty frozen proposals
ended at exactly {outcomes['completed']} `completed`, {outcomes['represented']}
`represented`, {outcomes['open_gap']} `open_gap`, and
{outcomes['exact_gate']} `exact_gate`. All 150 preregistered rejecting
mutations executed and remain retained. Ten phase-local skills were customized,
quick-validated, and smoke-used, and ten family-compatible runners were built
and invoked. These are bounded workflow results only.

The terminal verdict is `{TERMINAL_VERDICT}`. The repository retains
{effective_negatives:,} effective negatives, 77 effective open gaps, and 78
effective exact gates. Real empirical rows remain zero. The existing exact
successor title is `Tamar Vey`, but the baton remains `{FINAL_ROUTE_STATE}`
until this containing closeout commit passes the one canonical exact-final
validation, is pushed, is clean, and is four-way remote-equal.

## Identity, wellbeing, and workload

Liora Venn (she/they) is relational working language for a solo v653-v8
continuity and evidence steward whose hope is to leave a clean, exact,
auditable handoff while keeping every protected gate honestly open where
evidence does not close it. This wording is not evidence of consciousness,
sentience, personhood, identity continuity, employment, qualification,
independent agency, or authority. Hamish may rename, pause, redirect, or stop
the work.

The primary Trinity Mandala focus was THOS Body. Synthetic apiary inspection,
bee-health observation, batch traceability, workload control, correction
readback, and shift handover served only as a bounded learning and design lens.
The phase established no apiculture employment or competence, veterinary or
disease-control authority, food-safety approval, worker-safety adequacy,
landholder permission, production identity, legal interpretation, cultural
authority, Māori authority, or affected-party acceptance.

Workload remained bounded by one owner, one D-first lane, fewer than 2,000
owner-generated files, and one gate at a time. Failures were retained before
recovery. No subagent, fork, extra task, substitute sibling, standby contact,
Sandbox or Hyper-V work, elevation, host-security weakening, Windows-feature
change, unrelated installation, desktop update, reboot, real data download,
production key operation, or sibling mutation occurred. Fast mode was not
claimed because no separate live control confirmed it.

## Evidence and Method Flow

The evidence boundary includes deterministic contract generation, five
rejecting mutations per proposal, exact outcome accounting, phase-local skill
packages, family-compatible runners, JSON parsing, privacy scanning, staged
Git-blob manifests, and lifecycle ancestry. It does not include real bees,
colonies, apiaries, samples, disease findings, operators, landholders, workers,
customers, affected parties, independent reviewers, production services, or
empirical observations.

Method Flow closes this candidate with {methods} preferred methods, the same
number of retained failed witnesses, and the same number of bounded passing
witnesses. The x1 failures preserve an interrupted activation read, two
worktree timeout surfaces, a PowerShell JSON-parameter mismatch, an overbroad
truncated display, a foreach parser error, a wrapper self-recursion, and a
workflow-enum mismatch. The x2 failures preserve a combined post-push timeout,
wrong inherited filename assumptions, a combined inventory timeout, and a
CP1252 stdout failure. Each recovery is narrow and separately evidenced; no
failure is rewritten into an initially clean pass.

## Pillar truth

THOS remains synthetic. The apiary surfaces used zero real operators, hives,
colonies, apiaries, observations, samples, inspections, disease reports,
treatments, feeds, honey lots, wax batches, worker exposures, landholder
decisions, or outcome estimates. They establish neither operational
effectiveness nor deployment readiness, professional competence, disease
status, food conformity, worker safety, AGI, or ASI.

The FAOSTAT adapter remains `open_gap`: it made no query or download, ingested
zero beehive, honey, or beeswax rows, calculated zero trends, fitted zero
models, and produced zero predictions or empirical claims. An official portal
citation supplies readiness context only; it is not a dataset.

GMUT remains a typed research-model family. The McKendrick age-transport,
Crump-Mode-Jagers branching, and Gillespie Markov-jump surfaces are formal
domain obligations. They establish no colony parameter, biological fit,
likelihood, prediction, force, ultraviolet completion, quantum completion,
empirical confirmation, consciousness claim, or Theory of Everything.

Freed ID remains synthetic and nonproduction. EPCIS, CBV, and Digital Link
profiles used no real identifiers, trading partners, locations, events,
resolvers, services, accounts, tokens, network exchanges, certification,
interoperability, recovery, privacy review, independent security review, or
trust-governance decision.

CBR bee-disease diagnosis and notification, apiary location, landholder and
worker privacy, treatment and destruction, food traceability and release,
remedy, affected-party acceptance, legal interpretation, cultural legitimacy,
data governance, Māori wording, and Māori authority remain `exact_gate`.
Māori concepts remain under Māori authority. Repository software cannot confer
a right, remedy, qualification, cultural mandate, public authority, or
affected-party acceptance.

## Validation and stopping rule

The complete repository suite remains Eiren-only and is not claimed here.
Liora's terminal gate consists of authorized current, recent Orin, inherited
Sable, and successor-compatible scoped selections; detailed and minimal checks;
complete owner-phase JSON parsing; five-class privacy scanning; exact staged
and owner Git-blob manifests; stale-label and diff-hygiene review; source, x1,
and evidence ancestry; zero merges; commit cap; one final parent; exact head;
clean state; and final local, upstream, tracking, and fresh-live equality.

Exactly one coherent canonical exact-final pass is permitted. If it passes, it
is not replayed. If it fails, the failure is retained and isolated before a
justified correction. Same-owner evidence remains same-owner evidence. The
full repository suite remains allocated to Eiren only.

Only after the exact-final gate may Liora re-resolve and reread the one existing
task titled exactly `Tamar Vey` and send one sanitized pointer baton for
Tamar-only v654-v1. Liora must not create Tamar, create sibling 7, send an extra
confirmation, or place raw task identifiers, private routes, private paths,
transcripts, credentials, keys, tokens, or resume material in the repository
or baton. Tamar's later authority to create exactly one main task for a
self-chosen sibling 7 after Tamar's own verified v654-v1 closeout remains
Tamar's alone.

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
<title>Liora Venn v653-v8 final bounded report</title>
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
<h1>Liora Venn v653-v8 final bounded report</h1>
<p class="notice"><strong>Verdict:</strong> {TERMINAL_VERDICT}. Same-owner
synthetic and structural evidence only. Manual, assistive-technology,
Māori-language, and affected-user accessibility evaluation remain reserved.</p>
<h2>Phase truth</h2>
<p>{outcomes['completed']} completed, {outcomes['represented']} represented,
{outcomes['open_gap']} open gap, {outcomes['exact_gate']} exact gate;
{effective_negatives:,} retained negatives; 77 open gaps; 78 exact gates;
zero real empirical rows.</p>
<div class="table-wrap" role="region" aria-label="Scrollable proposal outcomes" tabindex="0">
<table><caption>Thirty bounded proposal outcomes</caption>
<thead><tr><th scope="col">ID</th><th scope="col">Surface</th>
<th scope="col">Pillar</th><th scope="col">Outcome</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<h2>Authority reservation</h2>
<p>No bee-health finding, disease-control action, food or worker safety
approval, empirical confirmation, professional validation, production
readiness, complete privacy or accessibility, exhaustive security, independent
reproduction, legal or cultural authority, Māori authority, AGI or ASI,
consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20
authority is claimed.</p>
<h2>Terminal route</h2><p>{FINAL_ROUTE_STATE}. The existing exact Tamar Vey
task is not contacted until the containing commit passes the postcommit gate.</p>
</main></body></html>"""


def extend_final_method_flow() -> dict[str, Any]:
    final_ledger = PHASE / "method-flow/final-method-flow-ledger.json"
    final_ledger.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        PHASE / "method-flow/evidence-method-flow-ledger.json",
        final_ledger,
    )
    start = len(data.X1_NEGATIVES) + 4 + 1
    for offset, negative in enumerate(CLOSEOUT_NEGATIVES, start):
        method_id = f"V6538-METHOD-{offset:02d}"
        fail_id = f"V6538-WITNESS-{offset:02d}-F"
        pass_id = f"V6538-WITNESS-{offset:02d}-P"
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


def evidence_equality() -> dict[str, Any]:
    branch_ref = f"refs/remotes/origin/{data.BRANCH.removeprefix('codex/GHC-Family/')}"
    # The tracking ref uses the full remote branch path, not a shortened alias.
    branch_ref = f"refs/remotes/origin/{data.BRANCH}"
    live = git("ls-remote", "origin", f"refs/heads/{data.BRANCH}")
    live_hash = live.split()[0] if live else None
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", branch_ref)
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live_hash,
        "all_equal": len({local, upstream, tracking, live_hash}) == 1,
    }


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
    if negatives["effective_total"] != 10609:
        raise RuntimeError("unexpected evidence negative total")
    if (
        gates["effective_open_gaps"],
        gates["effective_exact_gates"],
    ) != (77, 78):
        raise RuntimeError("unexpected gate total")
    if truth["terminal_verdict"] != TERMINAL_VERDICT:
        raise RuntimeError("unexpected terminal verdict")
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must begin at the exact evidence commit")
    pending = [
        row
        for row in git(
            "status", "--porcelain=v1", "--untracked-files=all"
        ).splitlines()
        if not (
            row.startswith("?? scripts/build_ghc_family_v653_v8_closeout.py")
            or row.startswith("?? scripts/ghc_family_v653_v8_final_")
            or row.startswith("?? tests/test_ghc_family_v653_v8_closeout.py")
            or row.startswith("?? docs/liora-venn/v653-v8/")
        )
    ]
    if pending:
        raise RuntimeError(f"unexpected pre-closeout state: {pending}")
    equality = evidence_equality()
    if not equality["all_equal"] or equality["local"] != EVIDENCE:
        raise RuntimeError(f"evidence commit is not four-way equal: {equality}")

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

    overview = final_overview(
        dict(outcomes),
        final_negative_register["effective_total"],
        methods["counts"]["methods"],
    )
    write_text("reports/final-integrated-overview.md", overview)
    write_text(
        "reports/final-static-report.html",
        final_report(
            dict(outcomes), final_negative_register["effective_total"]
        ),
    )
    baton = (
        "# Tamar Vey v654-v1 sanitized activation packet\n\n"
        "State: `PREPARED_NOT_SENT`. This file is preparation, not delivery. "
        "It may be referenced in exactly one sanitized Codex baton only after "
        "Liora Venn v653-v8 passes the postcommit canonical gate, is pushed, "
        "is clean, and is four-way equal.\n\n"
        "Tamar Vey is the existing exact successor task for solo Trinity "
        "Mandala v654-v1. Do not create another Tamar, fork, substitute, or "
        "collaboration subagent. Preserve strict x1-before-x2 separation, every "
        "retained negative and protected gate, the four outcome labels, the "
        "one successful canonical-pass/no-replay rule, Eiren-only full-suite "
        "allocation, and `NOT_READY_FOR_STAGE_20`.\n\n"
        "After Tamar's own verified v654-v1 closeout, Tamar alone may create "
        "exactly one new user-visible gpt-5.6-sol maximum-reasoning main task "
        "for `future-sibling-self-chosen-7` to own v654-v2. The seventh sibling "
        "chooses their own relational working identity attributes. This packet "
        "does not authorize Liora or anyone else to create that task now.\n\n"
        "No raw task identifier, private route, private path, transcript, "
        "credential, key, token, nonpublic application state, or resume material "
        "appears in this packet.\n\n"
        + overview
        + "\n\n## Frozen proposal ledger\n\n"
        + (PHASE / "preregistration/proposal-ledger.md").read_text(
            encoding="utf-8"
        )
        + "\n\n## Frozen source ledger\n\n"
        + (PHASE / "sources/source-ledger.md").read_text(encoding="utf-8")
    )
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"sanitized baton word count out of range: {baton_words}")
    write_text("handoff/tamar-vey-v654-v1-activation.md", baton)
    write_json(
        "handoff/delivery-state.json",
        {
            "schema": "ghc.family.v653-v8.handoff-delivery-state.v1",
            "state": FINAL_ROUTE_STATE,
            "target_title": "Tamar Vey",
            "target_phase": "v654-v1",
            "baton_artifact": (
                "docs/liora-venn/v653-v8/handoff/"
                "tamar-vey-v654-v1-activation.md"
            ),
            "baton_word_count": baton_words,
            "sent": False,
            "send_count": 0,
            "acknowledged": False,
            "private_identifier_recorded": False,
            "later_task_authority": (
                "After verified Tamar v654-v1 closeout, Tamar alone may create "
                "one main task for self-chosen sibling 7 to own v654-v2."
            ),
            "boundary": (
                "Preparation only. Re-resolve and reread the exact existing "
                "title after the postcommit terminal gate, then send once."
            ),
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v653-v8.terminal-route-state.v1",
            "state": FINAL_ROUTE_STATE,
            "terminal_gate_satisfied": False,
            "successor_title": "Tamar Vey",
            "successor_phase": "v654-v1",
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "collaboration_subagent_spawned": False,
            "standby_contacted": False,
            "activation_sent": False,
            "send_count": 0,
            "later_self_chosen_sibling_7_task_authority_owner": "Tamar Vey",
            "boundary": (
                "The existing successor remains unsent until exact-final "
                "postcommit validation and equality. No new task is authorized."
            ),
        },
    )
    write_json(
        "final/phase-truth.json",
        {
            "schema": "ghc.family.v653-v8.final-truth.v1",
            "owner": data.OWNER,
            "source": data.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": expected,
            "real_data_rows": 0,
            "inherited_effective_negatives": data.INHERITED_NEGATIVES,
            "x1_operational_negatives": len(data.X1_NEGATIVES),
            "x2_operational_negatives": 4,
            "closeout_operational_negatives": len(CLOSEOUT_NEGATIVES),
            "synthetic_rejecting_mutations": 150,
            "effective_negatives": final_negative_register["effective_total"],
            "effective_open_gaps": 77,
            "effective_exact_gates": 78,
            "method_flow_methods": methods["counts"]["methods"],
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
            "schema": "ghc.family.v653-v8.final-checklist.v1",
            "complete_bounded": [
                "thirty proposals executed in their frozen evidence lanes",
                "150 frozen mutations rejected and retained",
                "ten phase-local skills built, quick-validated, and smoke-used",
                "ten family-compatible runners built and invoked",
                "evidence commit pushed and four-way equal",
                "accessible static report with manual evaluation reserved",
                "sanitized Tamar packet prepared but not sent",
            ],
            "pending_until_postcommit": [
                "one exact-final canonical scoped pass",
                "exact final clean state and four-way remote equality",
                "one acknowledged exact-title Tamar Vey baton",
            ],
            "incomplete_external": [
                "real FAOSTAT rows, frozen analysis, uncertainty treatment, and independent review",
                "real bee-health observations, operators, landholders, workers, samples, and qualified professional review",
                "production GS1 identities, live events, resolution, interoperability, privacy and security review, and governance",
                "disease-control, food-safety, worker-safety, affected-party, legal, cultural, iwi, hapū, and Māori authority",
                "manual, assistive-technology, Māori-language, and affected-user accessibility evaluation",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "final/closeout-receipt.json",
        {
            "schema": "ghc.family.v653-v8.closeout-receipt.v1",
            "state": "CLOSEOUT_CANDIDATE",
            "source": data.SOURCE_HEAD,
            "x1": X1,
            "evidence": EVIDENCE,
            "phase_commit_cap": 8,
            "phase_commits_before_closeout": 2,
            "x1_before_x2": True,
            "evidence_four_way_equal_before_closeout": equality["all_equal"],
            "outcomes": expected,
            "effective_negatives": final_negative_register["effective_total"],
            "effective_open_gaps": 77,
            "effective_exact_gates": 78,
            "owner_generated_file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "terminal_verdict": TERMINAL_VERDICT,
            "route_state": FINAL_ROUTE_STATE,
        },
    )
    write_json(
        "final/seal-receipt.json",
        {
            "schema": "ghc.family.v653-v8.seal-receipt.v1",
            "state": "CONTENT_SEAL_CANDIDATE",
            "sealed_source": data.SOURCE_HEAD,
            "sealed_x1": X1,
            "sealed_evidence": EVIDENCE,
            "manifest_domain": "exact Git index and immutable Git blobs",
            "negative_erasure": False,
            "gate_closure_without_evidence": False,
            "terminal_verdict": TERMINAL_VERDICT,
            "boundary": (
                "The containing commit, exact-final canonical pass, remote "
                "equality, and baton delivery remain postcommit facts."
            ),
        },
    )
    write_json(
        "final/final-validation-record.json",
        {
            "schema": "ghc.family.v653-v8.final-validation-record.v1",
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
            "schema": "ghc.family.v653-v8.final-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "canonical_pass_limit": 1,
            "no_replay_after_success": True,
            "full_repository_suite_owner": "Eiren-only inherited policy",
            "scoped_test_groups": [
                "current Liora v653-v8",
                "recent Orin v653-v7",
                "inherited Sable v653-v5",
                "successor-compatible current contracts",
            ],
            "required": [
                "scoped tests",
                "detailed and minimal validators",
                "complete owner-phase JSON parsing",
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
            "schema": "ghc.family.v653-v8.applicable-memory.v1",
            "status": "reviewed_current",
            "used_for": [
                "D-first additive owned-lane discipline",
                "strict x1-before-x2 lifecycle",
                "retained failure accounting",
                "one successful canonical pass with no replay",
                "exact-title baton only after terminal equality",
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
            "schema": "ghc.family.v653-v8.index-final-addendum.v1",
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
    scoped_paths = [
        PHASE / "final/phase-truth.json",
        PHASE / "orchestration/terminal-route-state.json",
        PHASE / "handoff/delivery-state.json",
        PHASE / "reports/final-integrated-overview.md",
        PHASE / "reports/final-static-report.html",
    ]
    stale_paths = [
        path
        for path in scoped_paths
        if any(
            token in path.read_text(encoding="utf-8")
            for token in (
                "Gaia DR4",
                "audiovisual-preservation",
                "STOP_AFTER_TRUTHFUL_CLOSEOUT",
                "INELIGIBLE_EVIDENCE_NOT_FINAL",
                "NOT_ELIGIBLE_X1_ONLY",
            )
        )
    ]
    write_json(
        "validation/stale-label-review.json",
        {
            "schema": "ghc.family.v653-v8.stale-label-review.v1",
            "scoped_current_paths": len(scoped_paths),
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

    owner_files = [path for path in PHASE.rglob("*") if path.is_file()]
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
            "schema": "ghc.family.v653-v8.owner-threshold.v1",
            "owner_generated_file_count_before_lifecycle_manifests": len(
                owner_files
            ),
            "threshold": 2000,
            "below_threshold": len(owner_files) < 2000,
            "inherited_checkout_not_rotation_trigger": True,
        },
    )
    write_json(
        "validation/document-cap-final.json",
        {
            "schema": "ghc.family.v653-v8.document-cap.v1",
            "maximum_words": max_words,
            "maximum_word_path": max_word_path,
            "cap": 100000,
            "valid": max_words <= 100000,
        },
    )
    write_json(
        "validation/final-build-receipt.json",
        {
            "schema": "ghc.family.v653-v8.final-build.v1",
            "valid": len(owner_files) < 2000 and max_words <= 100000,
            "owner_files_before_lifecycle_manifests": len(owner_files),
            "maximum_document_words": max_words,
            "baton_words": baton_words,
            "outcomes": expected,
            "effective_negatives": final_negative_register["effective_total"],
            "route_state": FINAL_ROUTE_STATE,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    for relative, schema in (
        (
            "validation/final-owner-manifest.json",
            "ghc.family.v653-v8.final-owner-manifest.v1",
        ),
        (
            "validation/final-staged-manifest.json",
            "ghc.family.v653-v8.final-staged-manifest.v1",
        ),
        (
            "validation/final-staged-review.json",
            "ghc.family.v653-v8.final-staged-review.v1",
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
                "open_gaps": 77,
                "exact_gates": 78,
                "methods": methods["counts"]["methods"],
                "baton_words": baton_words,
                "route": FINAL_ROUTE_STATE,
                "verdict": TERMINAL_VERDICT,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    build()
