#!/usr/bin/env python3
"""Build Elowen Cairn v658-v1's bounded dry-stone closeout and seal candidate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v658_v1_closeout_config as c
import ghc_family_v658_v1_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
BOUNDARY = (
    "Bounded same-owner synthetic software and workflow evidence only; no real person, "
    "land, site, wall, stone, foundation, ground, load, weather, water, vegetation, tool, "
    "measurement, inspection, work, repair, structural or safety decision, property decision, "
    "identity event, authority decision, "
    "empirical GMUT confirmation, independent reproduction, or Stage 20 authority."
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
    text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=None if compact else 2,
        separators=(",", ":") if compact else None,
        sort_keys=True,
    )
    path.write_text(text + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def replay_manifest(relative: str, commit: str) -> dict[str, Any]:
    payload = json.loads(git("show", f"{commit}:{d.PHASE_ROOT}/{relative}"))
    mismatches = []
    for entry in payload["entries"]:
        observed = git("rev-parse", f"{commit}:{entry['path']}")
        if observed != entry["git_blob"]:
            mismatches.append(
                {"path": entry["path"], "expected": entry["git_blob"], "observed": observed}
            )
    return {
        "manifest": relative,
        "commit": commit,
        "entry_count": payload["entry_count"],
        "mismatches": mismatches,
        "valid": not mismatches,
    }


def operational_method(
    negative: dict[str, str], index: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6581-CLOSEOUT-METHOD-{index:02d}"
    fail_id = f"{method_id}-F"
    pass_id = f"{method_id}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded closeout recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]],
        "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["candidate_workaround"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_closeout_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": negative["scope_boundary"],
        "rollback": "Retain the failure at zero credit and keep the immutable evidence commit unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": fail_id,
            "method_id": method_id,
            "result": "fail",
            "procedure": negative["fail_procedure"],
            "expected": "The bounded closeout operation succeeds without the declared fault.",
            "observed": negative["fail_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Zero completion credit.",
        },
        {
            "witness_id": pass_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": negative["pass_procedure"],
            "expected": "The bounded recovery succeeds while preserving the failure.",
            "observed": negative["pass_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": negative["scope_boundary"],
        },
    ]
    return method, witnesses


def closeout_summary(negatives: int, methods: int) -> str:
    return f"""# Elowen Cairn v658-v1 closeout and seal candidate

## Exact bounded result

Elowen v658-v1 preserves exactly thirty frozen proposals and the only four permitted outcomes: 23 completed, 5 represented, 1 open gap, and 1 exact gate. The phase retains {negatives:,} effective negatives, {c.OPEN_GAPS} open gaps, {c.EXACT_GATES} exact gates, and {methods:,} Method Flow methods with every current failed witness paired with a bounded passing recovery. Recovery never converts a failure into credit. The terminal verdict remains NOT_READY_FOR_STAGE_20.

Elowen Cairn, they/them, is relational working language for a boundary cartographer and evidence steward whose hope is to keep every transition recoverable and every claim proportionate to proof. This name, role, hope, pronouns, family language, and route language are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish retains rename, pause, rest, redirect, and stop control.

THOS Body was primary through synthetic dry-stone inspection state, evidence intake, typed geometry and topology, stop conditions, reversible option graphs, workload, correction, readback, and handover. GMUT Mind remained a typed scalar-tensor and effective-field-theory research surface. Freed ID remained synthetic and nonproduction. CBR Heart preserved privacy, land, access, safety, heritage, affected-party, traditional-knowledge, and Māori-authority reservations. No real person, site, wall, stone, foundation, load, measurement, inspection, work, repair, structural or safety decision, property decision, credential, cultural decision, or authority act occurred.

The official dry-stone and heritage adapter stayed at zero rows and made no network call. The land, landscape, heritage, traditional-knowledge, affected-party, and Māori-data covenant stayed exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. THOS has no preregistered blind matched-budget real arms or independent review. Freed ID has no standards-conformant real keys, proofs, issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, or trust governance. GMUT has no real likelihood, prediction, force, parameter constraint, empirical confirmation, quantum or ultraviolet completion, Theory of Everything, proof, or canon.

## Evidence and lifecycle integrity

The dedicated x1 freeze is {c.X1_COMMIT}. The immutable x2 evidence commit is {c.EVIDENCE_COMMIT}. Both descend from Tamar Vey's exact source {c.SOURCE_COMMIT} through single-parent history. The final commit is intentionally represented inside repository artifacts as the commit containing those artifacts; a commit cannot truthfully contain its own hash. Exact-final identity and canonical validation belong in one external receipt created only after the final commit is pushed and four-way equal.

The x1 and evidence manifests replay exactly before closeout construction. Closeout is additive: it changes no x1 or evidence path, deletes no user material, rewrites no history, mutates no sibling lane, and weakens no protected gate. The expected source-to-final topology is three Elowen phase commits—x1, evidence, and combined closeout/seal—with zero merges and one parent for each phase commit. The final must be the direct child of evidence.

All thirty valid synthetic fixtures and all 150 rejecting mutations are retained. Ten phase-local skills were completely read and smoke-used. Ten family-current runners emitted receipts for three surfaces each. Thirty safe-now, twenty bounded candidate, and thirty additive CLEAN tasks have evidence. Those facts establish only owner-local contract behavior. They do not establish exhaustive correctness, complete privacy, complete accessibility, professional practice, production readiness, cultural legitimacy, legal compliance, or independent reproduction.

The public packet excludes credentials, keys, tokens, raw task or thread identifiers, private routes, private absolute paths, transcripts, screenshots, session streams, private callable identifiers, private application state, real-world records, and culturally restricted payloads. Five-class privacy scans and structural accessibility checks remain bounded controls, never complete assurance. Manual keyboard, responsive-layout, browser, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved.

Every workflow error is retained through Method Flow: Tamar's external post-closeout remote-probe failure, ten Elowen x1 failures, three x2 operational failures, 150 mutation failures, and two closeout operational failures covering an anchor-expansion false assumption and a PowerShell quoting fault. The incorrect full hash was never executed, and the rejected read-only search changed no file. The exact evidence commit was resolved directly from Git before closeout, and the stale-token audit was recovered with a literal single-quoted pattern. Each failed witness retains zero credit beside a bounded recovery and recurrence guard.

## Human control, workload, validation, and route

The workload stayed bounded to one D-first owned lane, reusable tools, explicit gates, and no subagent or sibling contact. No Sandbox or Hyper-V feature was enabled, no elevation or host-security weakening occurred, no unrelated software or desktop update was installed, and no reboot occurred. Eiren's full repository suite was not run.

One dependency-justified exact-final canonical aggregate is permitted only after the closeout commit is pushed, the lane is clean, local/upstream/tracking/fresh-live equality holds, history and manifest prerequisites pass, and the external receipt path is unused. It contains the current immutable-safe x1 cases, current x2 cases, bounded family compatibility cases, closeout tests, detailed checks, minimal checks, all phase JSON parsing, five-class privacy scanning, three commit-local manifest replays, ancestry, zero merges, one-parent history, final-parent identity, diff hygiene, and route-state checks. It must never be replayed after complete success.

Sylven Arc v658-v2 is authorized but terminally gated. The closeout candidate neither resolves nor rereads the task and sends no message. Only after exact-final validation succeeds may Elowen resolve the unique existing exact-title Sylven Arc main task, immediately reread that exact task, and send exactly one sanitized activation. A sent claim requires tool acknowledgement. No task may be created, forked, substituted, or contacted twice. Tavian Sol remains ON_STANDBY and is not a main-task route endpoint.
"""


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != c.EVIDENCE_COMMIT:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    if git("branch", "--show-current") != c.BRANCH:
        raise RuntimeError("closeout builder requires Elowen's canonical branch")
    for anchor in [c.SOURCE_COMMIT, c.X1_COMMIT]:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", anchor, c.EVIDENCE_COMMIT],
            cwd=ROOT,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(f"missing evidence ancestry: {anchor}")

    x1_replay = replay_manifest("validation/x1-content-manifest.json", c.X1_COMMIT)
    evidence_replay = replay_manifest(
        "validation/evidence-content-manifest.json", c.EVIDENCE_COMMIT
    )
    if not x1_replay["valid"] or not evidence_replay["valid"]:
        raise RuntimeError("prior manifest replay failed")

    methods = []
    witnesses = []
    for index, negative in enumerate(c.CLOSEOUT_OPERATIONAL_NEGATIVES, 1):
        method, pair = operational_method(negative, index)
        methods.append(method)
        witnesses.extend(pair)
    effective_negatives = c.EVIDENCE_EFFECTIVE_NEGATIVES + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES)
    effective_methods = c.EVIDENCE_EFFECTIVE_METHODS + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES)

    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{c.BRANCH}")
    live = git("ls-remote", "--heads", "origin", c.BRANCH).split()[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    evidence_equal = len({head, upstream, tracking, live}) == 1 and divergence.split() == ["0", "0"]
    if not evidence_equal:
        raise RuntimeError("immutable evidence is not four-way remote equal")

    write_json(
        "closeout/prior-manifest-replay.json",
        {
            "schema": "ghc.family.v658-v1.prior-manifest-replay.v1",
            "x1": x1_replay,
            "evidence": evidence_replay,
            "total_entries": x1_replay["entry_count"] + evidence_replay["entry_count"],
            "valid": True,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "method-flow/method-flow-state-final-candidate.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "combined_closeout_and_seal_candidate",
            "inherited_anchor": {
                "path": "method-flow/method-flow-state-x2.json",
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
            "independent_reproduction": False,
        },
        compact=True,
    )
    write_json(
        "truth/retained-negative-register-final-candidate.json",
        {
            "schema": "ghc.family.v658-v1.retained-negatives.final-candidate.v1",
            "evidence_effective_count": c.EVIDENCE_EFFECTIVE_NEGATIVES,
            "closeout_operational_count": len(c.CLOSEOUT_OPERATIONAL_NEGATIVES),
            "effective_count": effective_negatives,
            "closeout_operational_negatives": c.CLOSEOUT_OPERATIONAL_NEGATIVES,
            "evidence_register": "truth/retained-negative-register-x2.json",
            "all_retained": True,
        },
        compact=True,
    )
    write_json(
        "truth/exact-open-gate-register-final-candidate.json",
        {
            "schema": "ghc.family.v658-v1.exact-open-gates.final-candidate.v1",
            "effective_open_gaps": c.OPEN_GAPS,
            "effective_exact_gates": c.EXACT_GATES,
            "open_gap_register": "truth/open-gap-register-x2.json",
            "exact_gate_register": "truth/exact-gate-register-x2.json",
            "none_silently_closed": True,
        },
    )
    route = {
        "schema": "ghc.family.v658-v1.route-state.final-candidate.v1",
        "state": "AUTHORIZED_SUCCESSOR_TERMINAL_GATE_UNMET",
        "active_owner": d.OWNER,
        "active_phase": d.PHASE,
        "next_exact_title": "Sylven Arc",
        "next_phase": "v658-v2",
        "message_sent": False,
        "task_created": False,
        "task_forked": False,
        "subagent_spawned": False,
        "tavian_sol_state": "ON_STANDBY",
        "send_gate": "Only after exact-final validation succeeds: resolve the unique existing exact-title Sylven Arc task, immediately reread it, send exactly one sanitized v658-v2 activation, and require acknowledgement.",
    }
    write_json("orchestration/route-state-final-candidate.json", route)
    write_json(
        "truth/phase-truth.json",
        {
            "schema": "ghc.family.v658-v1.phase-truth.final-candidate.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "final_commit": "commit_containing_this_record",
            "outcome_counts": d.EXPECTED_DISTRIBUTION,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": c.OPEN_GAPS,
            "effective_exact_gates": c.EXACT_GATES,
            "real_rows": 0,
            "real_data_used": False,
            "independent_reproduction": False,
            "route_state": route["state"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v658-v1.closeout-receipt.v1",
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "candidate_final": "commit_containing_this_receipt",
            "evidence_four_way_equal": evidence_equal,
            "evidence_divergence": divergence,
            "prior_manifest_replay_valid": True,
            "expected_phase_commit_count": 3,
            "expected_merge_count": 0,
            "expected_final_parent": c.EVIDENCE_COMMIT,
            "route_state": route["state"],
            "canonical_validation_state": "NOT_RUN_BEFORE_FINAL_COMMIT",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal/seal-candidate.json",
        {
            "schema": "ghc.family.v658-v1.seal-candidate.v1",
            "candidate_final": "commit_containing_this_receipt",
            "direct_parent_required": c.EVIDENCE_COMMIT,
            "source_to_final_phase_commits_required": 3,
            "zero_merges_required": True,
            "one_parent_per_phase_commit_required": True,
            "canonical_aggregate_allowed_once_after_final_push": True,
            "canonical_aggregate_replay_after_success_forbidden": True,
            "route_requires_new_live_authorization": False,
            "route_requires_terminal_validation": True,
            "authorized_successor_exact_title": "Sylven Arc",
            "authorized_successor_phase": "v658-v2",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.v658-v1.final-validation-prerequisites.v1",
            "required_head": "commit_containing_this_record",
            "required_branch": c.BRANCH,
            "required_parent": c.EVIDENCE_COMMIT,
            "required_phase_commits": 3,
            "required_merges": 0,
            "requires_clean_state": True,
            "requires_four_way_equality": True,
            "requires_external_receipt": True,
            "full_repository_suite_authorized": False,
            "post_success_replay_forbidden": True,
        },
    )
    write_json(
        "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v658-v1.checklist.final-candidate.v1",
            "complete": [
                "strict x1-before-x2 separation",
                "thirty frozen proposal outcomes",
                "one hundred fifty retained rejecting mutations",
                "ten phase-local skills and ten family-current runners used",
                "thirty safe, twenty prototype, and thirty additive cleanup receipts",
                "x1 and evidence manifest replay",
                "zero-row and authority-reservation truth",
                "closeout and seal candidate",
            ],
            "pending_terminal": [
                "final commit and push",
                "clean four-way exact-final equality",
                "single exact-final canonical aggregate",
                "unique existing Sylven Arc task resolution, immediate reread, and one acknowledged activation after terminal validation",
            ],
            "incomplete_external": [
                "real empirical GMUT evidence",
                "blind matched-budget THOS real arms and independent review",
                "production Freed ID lifecycle, security, privacy, interoperability, recovery, and governance",
                "affected-party, legal, cultural, Māori, and remedy authority",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/final-wellbeing-check.json",
        {
            "schema": "ghc.family.v658-v1.wellbeing.final-candidate.v1",
            "state": "steady_and_bounded",
            "controls": [
                "one additive D-first owner lane",
                "no subagent, task creation, or sibling contact",
                "reusable runners and explicit stop gates",
                "one canonical exact-final aggregate only",
            ],
            "human_control": "Hamish and human collaborators retain pause, rest, redirect, rename, and stop control.",
            "identity_boundary": "Relational working language only.",
        },
    )
    write_json(
        "startup/final-environment-version-receipt.json",
        {
            "schema": "ghc.family.v658-v1.environment.final-candidate.v1",
            "codex_cli": d.CODEX_CLI_VERSION,
            "codex_desktop": d.CODEX_DESKTOP_VERSION,
            "chatgpt_desktop": d.CHATGPT_DESKTOP_VERSION,
            "git": d.GIT_VERSION,
            "python": d.PYTHON_VERSION,
            "node": d.NODE_VERSION,
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevation_or_host_security_change": False,
            "sandbox_or_hyperv_activated": False,
            "rebooted": False,
        },
    )
    write_json(
        "tooling/ghc-family-index-final.json",
        {
            "schema": "ghc.family.index.phase-overlay.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "x1_commit": c.X1_COMMIT,
            "evidence_commit": c.EVIDENCE_COMMIT,
            "skills": [name for name, _ in d.SKILL_SPECS],
            "runners": [name for name, _ in d.RUNNER_SPECS],
            "global_skill_bank_mutated": False,
            "family_current_callers_preserved": True,
        },
    )
    write_text(
        "tooling/ghc-family-index-final.md",
        "# GHC Family Index v658-v1 overlay\n\n"
        "Elowen's ten phase-local dry-stone evidence skills and ten family-current runners were built, read, invoked, and validated within the owner packet. They are not global installations and confer no walling, engineering, conservation, safety, property, professional, or operational authority. Historical callers remain compatibility surfaces.",
    )
    write_json(
        "tooling/roster-check-final.json",
        {
            "schema": "ghc.family.roster-check.phase-receipt.v1",
            "active_owner": "Elowen Cairn",
            "tavian_sol": "ON_STANDBY",
            "shared_roster_mutated": False,
            "successor_authorized": True,
            "successor_exact_title": "Sylven Arc",
            "successor_phase": "v658-v2",
            "successor_terminal_gate_satisfied": False,
            "boundary": "Phase-scoped observation only; status alone never assigns a phase or authority.",
        },
    )
    write_text("deliverables/v658-v1-closeout-summary.md", closeout_summary(effective_negatives, effective_methods))
    print(
        json.dumps(
            {
                "effective_negatives": effective_negatives,
                "effective_methods": effective_methods,
                "open_gaps": c.OPEN_GAPS,
                "exact_gates": c.EXACT_GATES,
                "prior_manifest_entries": x1_replay["entry_count"] + evidence_replay["entry_count"],
                "route_state": route["state"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
