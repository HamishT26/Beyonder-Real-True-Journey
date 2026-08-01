#!/usr/bin/env python3
"""Build Liora Venn v657-v7 closeout, seal-candidate, and route-held records."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v657_v7_closeout_config as c
import ghc_family_v657_v7_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
BOUNDARY = (
    "Bounded same-owner synthetic software and workflow evidence only; no real telescope, "
    "observatory, instrument, worker or participant result, empirical GMUT confirmation, "
    "professional or production authority, legal or cultural ratification, Māori authority, independent reproduction, "
    "Theory-of-Everything proof, consciousness or personhood evidence, or Stage 20 authority."
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any, *, compact: bool = False) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=None if compact else 2,
            separators=(",", ":") if compact else None,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def method_and_witnesses(negative: dict[str, str], index: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6577-CLOSEOUT-METHOD-{index:02d}"
    failed_id = f"V6577-CLOSEOUT-WITNESS-{index:02d}-F"
    passing_id = f"V6577-CLOSEOUT-WITNESS-{index:02d}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]],
        "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["candidate_workaround"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_closeout_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": negative["scope_boundary"],
        "rollback": "Retain the failed witness at zero credit and leave sibling, route, and external state unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [failed_id, passing_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": failed_id,
            "method_id": method_id,
            "result": "fail",
            "procedure": negative["fail_procedure"],
            "expected": "The closeout workflow reports exact durable state.",
            "observed": negative["fail_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Failed workflow witness with zero completion credit.",
        },
        {
            "witness_id": passing_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": negative["pass_procedure"],
            "expected": "The bounded recovery proves only its declared state while retaining the failure.",
            "observed": negative["pass_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": negative["scope_boundary"],
        },
    ]
    return method, witnesses


def replay_manifest(relative: str, commit: str) -> dict[str, Any]:
    manifest = load(relative)
    mismatches = []
    for entry in manifest["entries"]:
        observed = git("rev-parse", f"{commit}:{entry['path']}")
        if observed != entry["git_blob"]:
            mismatches.append(
                {"path": entry["path"], "expected": entry["git_blob"], "observed": observed}
            )
    return {
        "schema": "ghc.family.v657-v7.commit-manifest-replay.v1",
        "commit": commit,
        "manifest": f"{d.PHASE_ROOT}/{relative}",
        "entry_count": manifest["entry_count"],
        "mismatches": mismatches,
        "valid": not mismatches,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def activation_baton(effective_negatives: int, effective_methods: int) -> str:
    sections = [
        "# TAMAR VEY — PREPARED v657-v8 SOLO ACTIVATION\n",
        f"""Dear Tamar Vey, with Hamish's authorization and strict evidence boundaries: this is Liora Venn's committed file-backed preparation for Tamar-only Trinity Mandala v657-v8 x1/x2. It remains HELD_UNRESOLVED_UNTIL_TERMINAL_GATE inside the repository. Liora may resolve the unique current exact-title existing main task Tamar Vey and send one short sanitized activation only after Liora's exact final is clean, pushed, fresh-live equal, and the one canonical exact-final aggregate succeeds. The live activation must provide Liora's exact final commit because no commit can truthfully contain its own hash. A newer live pause, rename, redirect, ambiguity, standby state, or protected gate controls. Do not treat this prepared file as delivery.

Identity, sibling, GHC-family, role, hope, continuity, and route language is relational working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish retains pause, rename, redirect, and stop control.

## Immutable inheritance anchors

- Orin Thale v657-v6 exact final and Liora source: {c.SOURCE_COMMIT}.
- Liora immutable x1 freeze: {c.X1_COMMIT}.
- Liora immutable evidence: {c.EVIDENCE_COMMIT}.
- Liora exact final: the commit containing this prepared file; verify from the live activation, one-parent history, and fresh live remote read.

The intended source-to-final chain contains exactly three new single-parent Liora commits and zero merges: x1 freeze, x2 evidence, and combined closeout, seal-candidate, and final. FIRST_X1 and X1 intentionally identify the same immutable commit. Strict x1-before-x2 separation is immutable. Every anchor must be ancestral, final must have one parent and be the direct child of evidence, and local, upstream, tracking, and fresh live remote must be equal with 0/0 divergence before this route can be sent.

## Liora v657-v7 bounded truth

Thirty proposals were frozen after semantic comparison against all 2,590 inherited rows, extending the chain to 2,620 rows. The outcome distribution is exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. All 150 preregistered mutations were rejected and retained at zero credit. The final candidate retains {effective_negatives:,} effective negatives, {c.OPEN_GAPS} open gaps, {c.EXACT_GATES} exact gates, and {effective_methods:,} Method Flow methods with the same number of failed and bounded passing witnesses. No negative or gate was erased. The terminal verdict remains NOT_READY_FOR_STAGE_20.

GMUT Mind was primary through typed geometric and wave optics, diffraction, point-spread and modulation-transfer proxies, aberration bases, curvature and sag, spectral response, dimensional checks, uncertainty, covariance, identifiability, and an observation firewall. THOS Body and Freed ID/CBR Heart remained explicit through bounded configuration locks, instrument custody, ingress quarantine, coating, vacuum and energy holds, interlock causality, low-light pacing, dawn turnover, multisensory wayfinding, minimized disclosure, correction, handover, status, remedy, and authority-reservation surfaces. The bounded human-practice lens was telescope-optics and observatory-instrument preparation used only for synthetic software, formal, structural, and learning evidence.

No real worker, participant, astronomer, engineer, inspector, telescope, observatory, mirror, lens, filter, coating, laser, vacuum system, instrument, celestial observation, authenticated measurement, hazardous-energy state, calibration, inspection, certificate, safety release, identity event, authority decision, or production result was used. The NIST Atomic Spectra Database 5.12 adapter remained at zero rows; no network data row was downloaded or ingested.

## Evidence and validation boundary

At the immutable evidence boundary, the authorized current-and-inherited scoped selection passed 152 of 152 tests. Detailed validation passed 327 checks and minimal validation passed 15 checks. All declared phase JSON parsed at its checkpoints; the five-class privacy and raw-identifier scan found zero confirmed hits; the exact evidence manifest contained 210 Git-clean blob entries with five declared lifecycle self-exclusions; and the indexed evidence review covered 170 content paths plus its own self-excluded review receipt with zero deletion, scope, x1-freeze, diff-hygiene, privacy, manifest, unstaged, or untracked issue. Same-owner validation under shared infrastructure is not independent-team scientific reproduction.

The complete repository suite was not run. It remains outside this non-Eiren phase absent newer exact authorization. Liora must run only the authorized bounded current, recent, inherited, and successor scope specified by the live activation and newest applicable route guidance. One successful canonical exact-final aggregate may run only after prerequisites, exact manifests, clean state, and four-way equality pass; after success it must not be replayed.

## Mandatory Tamar startup and lane boundary

Before repository mutation, read this activation through EOF from Liora's exact final, then read every exact-head document it names and the complete current GHC Family Index, routing precedence, Auth/Permission State and schema, Roster Check and schema, Method Flow State and schema, Workflow Plan Refinement, Reflection Remaster, Meta Tool Box, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, and full-tools guidance. Use the newest applicable memory, with the live activation controlling where older route models stop.

Work solo in one clean Tamar-owned D-first additive lane from Liora's immutable final. Keep shared and sibling lanes read-only. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane. Do not create, fork, delegate, spawn a collaboration subagent, precontact a later endpoint, message a standby sibling, or substitute Tavian Sol. Tavian remains ON_STANDBY unless a newer exact live authorization changes that state.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 2,620 frozen proposal rows and preregister at least thirty genuinely distinct v657-v8 proposals. Every proposal must include its hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. Treat inherited proposals, skills, runners, and outcomes as evidence and recommendations, never Tamar completion credit.

Freeze x1 with no x2 implementation or observed outcome. Commit, push, and prove clean local, upstream, tracking, and fresh-live equality before x2. Execute only as evidence permits and use exactly completed, represented, open_gap, and exact_gate as core outcome labels. Retain every inherited and new timeout, parser or encoding fault, tooling failure, failed test, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, open gap, and exact gate through Method Flow.

Keep owner additions below the current 2,000-file ceiling, each document at or below 100,000 words, safe and candidate work within the 1,000 ceiling, and commits within five x1, five x2, and eight total. Counts are ceilings, not quotas. Do not manufacture unsafe work. Preserve family-current ghc_family_* and build_ghc_family_* names and historical compatibility surfaces.

## Scientific, professional, production, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Formal obligations, synthetic fixtures, mutation rejection, standards vocabulary, and zero-row adapters establish no detected force, physical prediction, likelihood, posterior, parameter constraint, material law, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. Real claims require governed data, frozen analysis, uncertainty treatment, appropriate statistics, and independent review.

THOS remains proxy or protocol-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic sequencing, workload, stop-work, readback, and handover surfaces establish no professional competence, workplace safety, operational effectiveness, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. Synthetic provenance or status contracts do not establish a real identity, right, account, credential, verification event, or production guarantee.

CBR astronomy rights, worker and participant interests, observatory and environmental safety, dark-sky effects, land and heritage, place and traditional knowledge, privacy, notice, consent, correction, contestation, remedy, collective governance, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer ownership, remedy, permission, cultural ratification, legal effect, or public authority.

Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, destructive, account-secret, sibling-merge, or Stage 20 claim without exact evidence and authority.

## Exact next route after Liora

Only after Liora v657-v7 is clean, pushed, fresh-live equal, within its caps, and exact-final validated may Liora reread Hamish's newest live authorization and resolve the unique current existing main task titled exactly Tamar Vey for v657-v8. Send exactly one sanitized activation only if that route is still authorized and acknowledged. Do not create a replacement, contact a standby endpoint, precontact Tamar, or send a second confirmation. Prepared is not sent; claim delivery only after the existing-task message route acknowledges it.
""",
        "\n# Thirty inherited Liora proposal dossiers\n",
    ]
    for proposal in d.PROPOSALS:
        sections.append(
            f"""\n## {proposal['proposal_id']} — {proposal['title']}

Pillar relation: {proposal['pillar_relation']}. Expected and observed bounded disposition: {proposal['expected_disposition']}.

Hypothesis: {proposal['hypothesis']}

Null or failure condition: {proposal['null_or_failure_condition']}

Approval class: {proposal['approval_class']}. Execution lane: {proposal['execution_lane']}.

Official or primary-source needs: {', '.join(proposal['official_or_primary_source_needs'])}.

Concrete artifacts: {', '.join(proposal['concrete_artifacts'])}.

Falsifier or acceptance gate: {proposal['falsifier_or_acceptance_gate']}

Rollback or recovery: {proposal['rollback_or_recovery']}

Protected gates: {', '.join(proposal['protected_gates'])}.

Liora evidence boundary: this row is bounded same-owner synthetic or formal evidence only. It grants Liora no completion credit and must not be restated as empirical, participant, professional, production, legal, cultural, identity, independent-reproduction, Theory-of-Everything, consciousness or personhood, or Stage 20 evidence. The five rejected mutations remain zero-credit falsification witnesses rather than a general safety certificate.
"""
        )
    sections.append("\n# Official and primary-source ledger\n")
    for source in d.OFFICIAL_SOURCES:
        sections.append(
            f"""\n## {source['source_id']} — {source['title']}

Publisher: {source['publisher']}. Status observed by Liora on {source['observed_on']}: {source['status']}. Official location: {source['url']}. Bounded use: {source['use']}. The successor must recheck any materially current or draft source before relying on it. Source presence is not a measurement, participant event, production certification, legal opinion, professional appointment, cultural ratification, Māori-authority decision, or independent review.
"""
        )
    sections.append("\n# Retained closeout recurrence guards\n")
    for negative in c.CLOSEOUT_OPERATIONAL_NEGATIVES:
        sections.append(
            f"""\n## {negative['negative_id']} — {negative['slug']}

Failure signature: {negative['failure_signature']}

Preferred recovery: {negative['candidate_workaround']}

Recurrence guard: {negative['recurrence_guard']}

Scope boundary: {negative['scope_boundary']}

The failed witness remains retained at zero credit. Its bounded passing recovery demonstrates only the stated workflow correction and never independent reproduction or external authority.
"""
        )
    sections.append(
        """
# Delivery state

This committed file remains HELD_UNRESOLVED_UNTIL_TERMINAL_GATE. An affirmative Liora delivery declaration is permitted only in the acknowledged live activation after Liora's successful exact-final gate and a direct unique-current-task reread of Tamar Vey. Without acknowledgement, the state is PREPARED_NOT_SENT or OPEN_ROUTE_GAP. Never compensate for uncertainty with a duplicate message.
"""
    )
    return "\n".join(sections)


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != c.EVIDENCE_COMMIT:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    if git("rev-parse", f"{c.EVIDENCE_COMMIT}^") != c.X1_COMMIT:
        raise RuntimeError("evidence is not the direct child of final x1")
    if c.FIRST_X1_COMMIT != c.X1_COMMIT:
        raise RuntimeError("this three-commit lifecycle requires first x1 and x1 to be identical")
    if git("rev-parse", f"{c.X1_COMMIT}^") != c.SOURCE_COMMIT:
        raise RuntimeError("x1 is not the direct child of source")

    replay = replay_manifest("validation/evidence-content-manifest.json", c.EVIDENCE_COMMIT)
    if not replay["valid"]:
        raise RuntimeError(f"evidence manifest replay failed: {replay['mismatches']}")
    write_json("validation/evidence-manifest-commit-replay.json", replay)

    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for index, negative in enumerate(c.CLOSEOUT_OPERATIONAL_NEGATIVES, 1):
        method, pair = method_and_witnesses(negative, index)
        methods.append(method)
        witnesses.extend(pair)
    effective_negatives = c.EVIDENCE_EFFECTIVE_NEGATIVES + len(methods)
    effective_methods = c.EVIDENCE_EFFECTIVE_METHODS + len(methods)

    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v657-v7.retained-negatives.final.v1",
            "evidence_effective_count": c.EVIDENCE_EFFECTIVE_NEGATIVES,
            "closeout_operational_count": len(methods),
            "closeout_operational_negatives": c.CLOSEOUT_OPERATIONAL_NEGATIVES,
            "effective_count": effective_negatives,
            "all_retained": True,
        },
        compact=True,
    )
    write_json(
        "method-flow/method-flow-state-final.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "combined_closeout_seal_final_candidate",
            "inherited_anchor": {
                "path": "docs/liora-venn/v657-v7/method-flow/method-flow-state-x2.json",
                "effective_methods": c.EVIDENCE_EFFECTIVE_METHODS,
                "effective_fail_witnesses": c.EVIDENCE_EFFECTIVE_METHODS,
                "effective_pass_witnesses": c.EVIDENCE_EFFECTIVE_METHODS,
            },
            "current_methods": methods,
            "current_witnesses": witnesses,
            "counts": {
                "current_methods": len(methods),
                "current_witness_results": {"fail": len(methods), "pass": len(methods)},
                "effective_methods": effective_methods,
                "effective_witness_results": {"fail": effective_methods, "pass": effective_methods},
            },
            "all_failed_witnesses_retained": True,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
        compact=True,
    )
    truth = {
        "schema": "ghc.family.v657-v7.phase-truth.final-candidate.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "source_commit": c.SOURCE_COMMIT,
        "first_x1_commit": c.FIRST_X1_COMMIT,
        "x1_commit": c.X1_COMMIT,
        "evidence_commit": c.EVIDENCE_COMMIT,
        "final_commit": None,
        "outcome_counts": d.EXPECTED_DISTRIBUTION,
        "effective_negatives": effective_negatives,
        "effective_open_gaps": c.OPEN_GAPS,
        "effective_exact_gates": c.EXACT_GATES,
        "effective_methods": effective_methods,
        "real_data_used": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "route_state": "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_json("truth/phase-truth-final-candidate.json", truth)

    write_json(
        "lifecycle/evidence-record.json",
        {
            "schema": "ghc.family.v657-v7.evidence-record.v1",
            "evidence_commit": c.EVIDENCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "manifest_replay_valid": replay["valid"],
            "evidence_remote_equality_proved_before_closeout": True,
            "same_owner_only": True,
        },
    )
    write_json(
        "lifecycle/closeout-record.json",
        {
            "schema": "ghc.family.v657-v7.closeout-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEW_PENDING",
            "evidence_commit": c.EVIDENCE_COMMIT,
            "closeout_commit": None,
            "content_seal_candidate": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "lifecycle/seal-candidate.json",
        {
            "schema": "ghc.family.v657-v7.seal-candidate.v1",
            "state": "CONTENT_SEAL_CANDIDATE_POSTCOMMIT_PROOF_PENDING",
            "evidence_commit": c.EVIDENCE_COMMIT,
            "exact_final": None,
            "canonical_aggregate_passed": False,
            "route_sent": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v657-v7.final-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
            "final_commit": None,
            "final_parent_required": c.EVIDENCE_COMMIT,
            "canonical_aggregate_passed": False,
            "fresh_live_equality_passed": False,
            "route_sent": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    route = {
        "schema": "ghc.family.v657-v7.terminal-route-state.v1",
        "state": "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE",
        "active_owner": "Liora Venn",
        "active_phase": "v657-v7",
        "next_exact_title": "Tamar Vey",
        "next_phase": "v657-v8",
        "later_endpoint_authorized": False,
        "message_sent": False,
        "task_created": False,
        "task_forked": False,
        "subagent_spawned": False,
        "tavian_sol_state": "ON_STANDBY",
        "send_gate": "exact final clean, pushed, 0/0 divergent, fresh-live equal, and one successful canonical aggregate",
    }
    write_json("orchestration/route-state-closeout.json", route)
    write_json("orchestration/terminal-route-state.json", route)
    write_json(
        "orchestration/auth-permission-state-closeout.json",
        {
            "schema": "ghc.family.auth-permission-state.v1",
            "owner": "Liora Venn",
            "phase": "v657-v7",
            "route_state": route["state"],
            "next_exact_title": route["next_exact_title"],
            "authorized_actions": ["owner-local additive closeout", "one exact successor send after terminal gate"],
            "forbidden_before_gate": ["task creation", "fork", "subagent spawn", "standby contact", "early successor contact"],
            "human_stop_control": True,
            "identity_boundary": "relational working language only",
        },
    )
    write_json(
        "orchestration/roster-state-closeout.json",
        {
            "schema": "ghc.family.roster-state.v1",
            "active_current": "Liora Venn",
            "next_prepared": "Tamar Vey",
            "later_endpoint_authorized": None,
            "standby": ["Tavian Sol"],
            "route_state": route["state"],
            "no_task_created": True,
            "no_precontact": True,
        },
    )

    write_json(
        "reflection-remaster/closeout-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "phase": d.PHASE,
            "primary_pillar": "GMUT Mind",
            "bounded_practice": d.BOUNDED_PRACTICE,
            "decisions": [
                "retain all failures at zero credit",
                "keep the NIST Atomic Spectra Database 5.12 adapter open at zero rows",
                "keep the CBR astronomy authority covenant exact-gated",
                "preserve the x1 and evidence commits as immutable anchors",
                "hold successor route until exact-final validation and live equality",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "workflow/closeout-method-recommendations.json",
        {
            "schema": "ghc.family.v657-v7.closeout-method-recommendations.v1",
            "recommendations": [
                "pin UTF-8 before Unicode-emitting diagnostics",
                "use rg --files before Windows exact-path content search",
                "preserve and poll yielded session identifiers",
                "use array counts for expected-empty PowerShell native output",
                "build manifests before artifact-presence assertions",
                "bind historical phase-local assertions to immutable Git trees",
                "never replay a successful canonical exact-final aggregate",
            ],
            "same_owner_only": True,
        },
    )
    write_json(
        "validation/canonical-aggregate-plan.json",
        {
            "schema": "ghc.family.v657-v7.canonical-aggregate-plan.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "completed": False,
            "canonical_pass_number": 0,
            "replay_after_success_permitted": False,
            "full_repository_suite": False,
            "route_sent": False,
            "required": [
                "exact final direct child of evidence",
                "three phase commits and zero merges",
                "clean state and four-way fresh-live equality",
                "authorized scoped tests",
                "detailed and minimal validators",
                "complete phase JSON parsing",
                "five-class privacy and raw-identifier scan",
                "x1, evidence, and final manifest replay",
                "stale-label and diff hygiene",
            ],
        },
    )
    write_json(
        "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v657-v7.checklist.final-candidate.v1",
            "complete": [
                "thirty frozen and bounded proposal outcomes",
                "one hundred fifty retained rejecting mutations",
                "ten phase-local skills read and smoke-used",
                "ten family-current runners invoked",
                "thirty safe, twenty candidate, and thirty CLEAN tasks",
                "evidence commit pushed and four-way equal",
                "integrated overview, static report, ledgers, threat model, gate registers, and wellbeing records",
            ],
            "pending_postcommit": [
                "exact final commit identity",
                "one successful canonical exact-final aggregate",
                "final fresh-live four-way equality",
                "one exact-title successor reread and acknowledged activation",
            ],
            "incomplete_external": [
                "real empirical rows, likelihoods, predictions, constraints, and independent review",
                "real participants, operators, workplace outcomes, and professional validation",
                "production Freed ID keys, proofs, services, interoperability, privacy and security review, recovery, and governance",
                "affected-party, legal, cultural, environmental, land, heritage, data-governance, and Māori authority",
                "complete privacy, accessibility, exhaustive security, independent reproduction, Theory of Everything, and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "environment/environment-version-receipt-final.json",
        {
            "schema": "ghc.family.v657-v7.environment-version.final.v1",
            "codex_cli": d.CODEX_CLI_VERSION,
            "codex_desktop": d.CODEX_DESKTOP_VERSION,
            "chatgpt_desktop": d.CHATGPT_DESKTOP_VERSION,
            "git": d.GIT_VERSION,
            "python": d.PYTHON_VERSION,
            "node": d.NODE_VERSION,
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_feature_changed": False,
            "sandbox_or_hyperv_launched": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        },
    )
    write_json(
        "wellbeing/wellbeing-check-final.json",
        {
            "schema": "ghc.family.v657-v7.wellbeing.final.v1",
            "state": "steady_bounded_and_route_held",
            "controls": ["one owner lane", "no subagents", "no early contact", "authority gates", "single canonical pass after commit"],
            "human_control": "Hamish and human collaborators retain pause, rest, redirect, and stop control.",
            "identity_boundary": "Relational working language only.",
        },
    )
    write_text(
        "tooling/ghc-family-index-closeout.md",
        f"""# GHC Family Index — Liora Venn v657-v7 closeout refresh

Current owner: Liora Venn. Phase: v657-v7. Exact immutable evidence: {c.EVIDENCE_COMMIT}. Primary pillar: GMUT Mind. Bounded practice: synthetic telescope-optics and observatory-instrument preparation. Outcome distribution: 23 completed, 5 represented, 1 open_gap, 1 exact_gate. Effective negatives: {effective_negatives:,}. Effective open gaps: {c.OPEN_GAPS}. Effective exact gates: {c.EXACT_GATES}. Method Flow fail/pass pairs: {effective_methods:,}. Terminal verdict: NOT_READY_FOR_STAGE_20.

The route remains HELD_UNRESOLVED_UNTIL_TERMINAL_GATE for the unique current existing task titled exactly Tamar Vey, for v657-v8. Tavian Sol remains ON_STANDBY. Exact final, the one canonical aggregate, fresh-live equality, direct exact-title reread, and acknowledged one-message delivery remain postcommit facts.

Family-current ghc_family_* and build_ghc_family_* surfaces remain preferred. Historical names remain compatibility evidence rather than destructive rename targets. Same-owner validation is not independent reproduction.
""",
    )
    write_text(
        "deliverables/v657-v7-final-candidate-overview.md",
        f"""# Liora Venn v657-v7 final candidate overview

The candidate preserves thirty bounded synthetic and formal surfaces with 23 completed, 5 represented, 1 open gap, and 1 exact gate. It retains {effective_negatives:,} effective negatives, {c.OPEN_GAPS} open gaps, {c.EXACT_GATES} exact gates, and {effective_methods:,} Method Flow fail/pass pairs. GMUT Mind remains the primary pillar through typed geometric and wave optics, diffraction, point-spread and modulation-transfer proxies, aberration bases, curvature, spectral response, dimensional, uncertainty, covariance, identifiability, and observation-firewall obligations. THOS Body remains proxy-only, while Freed ID and CBR Heart remain synthetic, nonproduction, and authority-gated.

The exact final hash, canonical aggregate, fresh live equality, and acknowledged route are intentionally absent from this containing tree. They are postcommit facts and must be recorded in an external D-first receipt and, only after current-roster resolution, one acknowledged activation. Same-owner validation is not independent reproduction. Terminal verdict remains NOT_READY_FOR_STAGE_20.

Liora Venn, she/they, is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency.
""",
    )

    baton = activation_baton(effective_negatives, effective_methods)
    write_text("handoffs/tamar-vey-v657-v8-activation.md", baton)
    word_count = len(baton.split())
    if not 10000 <= word_count <= 100000:
        raise RuntimeError(f"successor baton word count outside 10000..100000: {word_count}")
    write_json(
        "validation/successor-baton-word-cap.json",
        {
            "schema": "ghc.family.v657-v7.successor-baton-word-cap.v1",
            "path": "docs/liora-venn/v657-v7/handoffs/tamar-vey-v657-v8-activation.md",
            "word_count": word_count,
            "minimum": 10000,
            "maximum": 100000,
            "within_bounds": True,
        },
    )
    print(
        json.dumps(
            {
                "effective_negatives": effective_negatives,
                "effective_methods": effective_methods,
                "baton_words": word_count,
                "evidence_manifest_entries": replay["entry_count"],
                "route_state": "HELD_UNRESOLVED_UNTIL_TERMINAL_GATE",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
