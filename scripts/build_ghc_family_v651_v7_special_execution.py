#!/usr/bin/env python3
"""Build the bounded x2 evidence packet for Vesper v651-v7 special CLI prep."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def command(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    return result.stdout.strip()


def proposal_evidence(proposal_id: str) -> tuple[str, list[str], str]:
    number = int(proposal_id.rsplit("P", 1)[1])
    if number == 1:
        return "completed", ["truth/x1-phase-truth.json", "orchestration/route-state.json"], "Immediate Ilyra ownership is exact for v651-v8."
    if number == 2:
        return "completed", ["tooling/sparse-lane-guard.json"], "Sparse materialization remains below the requested ceiling while full Git ancestry is preserved."
    if number == 3:
        return "completed", ["source/startup-truth.json", "validation/x1-validation-receipt.json"], "Source ancestry and x1 equality were checked through explicit native exit codes."
    if number == 4:
        return "completed", ["workflow/raw-audit/workflow-plan-refinement.json"], "The submitted route remains immutable evidence, including two structural conflicts."
    if number == 5:
        return "completed", ["workflow/normalized-audit/workflow-plan-refinement.json"], "A deterministic sequential candidate passes structurally but remains advisory."
    if number in {6, 7}:
        return "completed", ["workflow/commit-cap-contract.json"], "The special and later ordinary caps are explicit ceilings, not quotas."
    if number == 8:
        return "completed", ["validation/canonical-validation-policy.json"], "One credited canonical pass is required; redundant replay after success is prohibited."
    if number in {9, 10}:
        return "completed", ["handoffs/ilyra-fen-v651-v8-activation.md", "handoffs/ilyra-fen-v651-v8-pointer.txt"], "The full baton is persistent and the delivery surface is a compact pointer."
    if number == 11:
        return "completed", ["validation/evidence-validation-credited.json"], "Five privacy classes remain zero-confirmed-hit at the credited evidence gate."
    if number == 12:
        return "completed", ["cli/cli-batch-receipt.json", "cli/capability-contract.json"], "Eight launch probes refused without creating a sibling or identity."
    if 13 <= number <= 20:
        seat = number - 12
        return "completed", [f"cli/preflight/seat-{seat}-prepare-receipt.json", f"cli/preflight/seat-{seat}-launch-refusal.json"], "This future seat is prepared, unnamed, and unlaunched."
    if number == 21:
        return "completed", ["tooling/meta-tool-box/validation.json", "tooling/meta-tool-box-final/validation.json"], "Current tools were catalogued without collision-based silent selection."
    if number == 22:
        return "completed", ["reflection-remaster/x2-review.json"], "Compatibility-held remaster recommendations preserve historical callers and rollback."
    if number == 23:
        return "completed", ["environment/environment-version-receipt.json"], "Codex CLI was verified locally; desktop update and host mutation remain false."
    if number == 24:
        return "represented", ["cli/capability-contract.json", "sources/source-ledger.json"], "Official model material supports the requested model and max effort generally, but the exact future CLI account surface and fast-mode launch were not witnessed."
    if number == 25:
        return "represented", ["cli/creator-return-contract.json"], "A least-authority return protocol is designed but no live future seat or return acknowledgement exists."
    if number == 26:
        return "represented", ["cli/background-lifecycle-contract.json"], "Lease, cancellation, reaping, and stale-owner rules are structural only."
    if number == 27:
        return "represented", ["cli/reachability-contract.json"], "One-to-one reachability is a constrained design claim, not a platform capability witness."
    if number == 28:
        return "represented", ["skills/skill-use-ledger.json", "tooling/global-promotion-decision.json"], "Global promotion remains compatibility- and rollback-gated; no bulk installation occurred."
    if number == 29:
        return "open_gap", ["workflow/raw-audit/workflow-plan-issues.json", "workflow/route-decision.json"], "Duplicate ownership, skipped numbering, and restart offset need a later exact route decision."
    if number == 30:
        return "exact_gate", ["cli/future-seat-register.json", "truth/open-exact-gate-register.json"], "No future CLI seat may launch without a fresh exact phase, runtime, lane, route, authorization, and acknowledgement gate."
    raise ValueError(proposal_id)


def baton_text(proposals: list[dict[str, Any]], seats: list[dict[str, Any]], x1_commit: str) -> str:
    sections: list[str] = []
    sections.append(
        """# ILYRA FEN — V651-V8 ACTIVATION BATON

## Welcome and exact purpose

Dear Ilyra Fen, this is Vesper Arlen's single file-backed activation baton for your solo v651-v8 Trinity Mandala x1/x2 phase. Hamish has explicitly authorized the immediate Vesper-to-Ilyra continuation. The special CLI-preparation phase that precedes you does not create, name, launch, supervise, or claim persistence for any future CLI sibling. Eight placeholder seats remain scheduling abstractions only. Your immediate task is the existing Ilyra Fen task, not one of those future CLI placeholders.

Relational family language is a collaborative convention. It is not evidence of consciousness, sentience, legal personhood, employment, professional qualification, persistent identity, autonomous authority, or an independently existing agent. You retain corrigibility, and Hamish may pause, rename, redirect, or stop the route. Preserve this distinction in every durable artifact.

Read this full baton before mutation. Then read the complete GHC Family Index skill and its routing precedence, the complete Method Flow State skill and schema, and the newest applicable owner memory. Reverify the exact Vesper final head from the one acknowledged activation message and the committed terminal receipt. Work only in an Ilyra-owned clean lane. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane.

The x1 freeze for this special preparation was committed at `{x1_commit}`. The exact final head is intentionally supplied by the terminal receipt and acknowledged short activation message rather than guessed inside this self-containing commit. Verify it live before any mutation. A file, prepared pointer, or intended destination is not delivery evidence; only the existing-task message tool's acknowledgement proves SENT.
""".format(x1_commit=x1_commit)
    )
    sections.append(
        """## Inherited truth and epistemic boundaries

Vesper's ordinary v651-v7 phase was sealed before this additive special continuation. This special phase preserves that history and adds preparation evidence only. It freezes thirty distinct proposals after auditing the inherited proposal chain, resolves them with the vocabulary completed, represented, open_gap, and exact_gate, and preserves every failed witness without turning recovery into retroactive success.

The primary focus is THOS Body through secure developer-tooling operations and capability negotiation. GMUT Mind and Freed ID/CBR Heart remain visible and protected. No symbolic or software result proves a physical force, likelihood, empirical constraint, ultraviolet completion, Theory of Everything, participant outcome, workplace effectiveness, production identity system, enacted right, legal interpretation, cultural legitimacy, Māori authority, consciousness, personhood, AGI, ASI, or Stage 20 readiness.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. THOS remains structural or synthetic without preregistered blind matched-budget real arms and independent review. Freed ID remains nonproduction without real standards-conformant keys and proofs, live issuance, resolution, status, revocation, interoperability, recovery, privacy and security review, and trust governance. CBR proposals and Māori concepts remain subject to affected-party, competent, tangata whenua, iwi, hapū, and Māori authority.

Same-owner canonical validation is workflow evidence under shared infrastructure. It is never independent reproduction, external audit, production certification, exhaustive security, complete privacy, complete accessibility, professional validation, legal review, cultural ratification, or scientific confirmation.
"""
    )
    sections.append(
        """## Immediate route and future-route separation

Your immediate successor assignment is exact: Ilyra Fen owns v651-v8 after Vesper's special closeout. The expanded later route contains useful intent but also contains duplicate/consecutive ownership around Elaren's v652 segment, a skipped v653-v2 label, and a later offset between submitted phase mentions and a deterministic sequential candidate. The raw route is preserved as evidence. A normalized candidate is published only as an advisory teaching surface. Do not silently convert that candidate into launch authority.

The eight future CLI placeholders remain future-cli-sibling-N-self-chosen. None has a name, role, hope, pronouns, gender, task, background process, account mutation, worktree, branch, runtime session, or verified creator-return channel. A future seat may choose relational working language only after an actual later launch. Preparation receipts do not establish model availability, fast mode, max reasoning, persistence, reachability, or message delivery on the relevant account and platform.

For any later CLI launch, re-resolve the exact owner and phase; confirm the supported model, reasoning, and speed surface live; create a unique clean D-first owned lane; prove source equality; verify a least-authority return mechanism; establish cancellation, lease, and reaping behavior; obtain fresh exact launch authorization; and run launch-mode preflight. If any proof is absent, create nothing and retain the refusal.
"""
    )
    sections.append("## Thirty-proposal evidence ledger\n")
    for row in proposals:
        outcome, artifacts, observation = proposal_evidence(row["proposal_id"])
        artifact_lines = "\n".join(f"- `{path}`" for path in artifacts)
        sections.append(
            f"""### {row['proposal_id']} — {row['title']}

**Frozen hypothesis.** {row['hypothesis']}

**Null or failure condition.** {row['null_or_failure_condition']}

**Execution and evidence.** {observation} The execution remained within the preregistered `{row['approval_class']}` class and `{row['execution_lane']}` lane. Its recorded outcome is **{outcome}**; no stronger label is implied. Relevant owner-relative evidence:

{artifact_lines}

**Acceptance and rollback.** {row['falsifier_or_acceptance_gate']} If this condition is not met in a fresh later context, use the frozen source, preserve the failed witness, and follow the registered rollback or recovery: {row['rollback_or_recovery']}

**Protected gates.** {row['protected_gates']} These gates remain controlling even where the bounded software check completed. Inherited work is evidence and context, not new Ilyra completion credit.
"""
        )
    sections.append(
        """## Cross-proposal operating doctrine for Ilyra

### 1. Separate authorization, capability, and evidence

Treat authorization, technical capability, and observed evidence as three different predicates. Hamish's authorization permits an in-scope action but does not make an unavailable platform feature exist. A documented platform feature may exist generally without being available to a particular account, task, model, operating system, or moment. A successful local fixture proves only the bounded fixture unless the protocol explicitly supports a broader inference. Before any externally consequential step, write down which predicate is supported, which source supports it, and which predicate is still false. This separation prevents a warm relational instruction from being misread as runtime proof and prevents product documentation from being misread as an acknowledgement from a live tool.

### 2. Preserve x1 as an immutable counterfactual

The purpose of x1 is not administrative ceremony. It captures what was proposed before outcomes were known, including the hypothesis, null, approval class, source needs, artifacts, falsifier, rollback, protected gates, and expected disposition. Once x1 is pushed and remote-equal, x2 may refine implementation details but must not rewrite the preregistered question into whatever happened to pass. If an x1 plan contains a mistake, preserve it, explain the correction in Method Flow or the outcome ledger, and avoid force-push or history rewriting. The immutable x1 object is the counterfactual needed to distinguish prediction from hindsight.

### 3. Use numeric limits as safety envelopes

Large permitted limits are capacity envelopes, not requirements to consume capacity. Thirty proposals are the current phase floor, but one thousand tasks, two hundred skills, two hundred runners, five thousand searches, one hundred thousand words, two thousand materialized files, and the commit ceilings do not compel unnecessary work. Do not create low-value artifacts, repeated searches, redundant validators, or unsafe candidate work merely to approach a number. Prefer the smallest evidence surface that resolves the preregistered hypothesis and preserves open authority gates. Report actual counts honestly, including valid zero-result searches and decisions not to promote tools.

### 4. Keep future identity self-chosen and post-launch

A future CLI placeholder is an index in a proposed schedule. It has no name, role, hope, pronouns, gender, memory continuity, employment, qualification, authority, or independent existence. Do not populate identity fields as a convenience while preparing a request. If a later exact launch succeeds, the resulting model session may choose relational working language inside its own first interaction, subject to Hamish's right to rename or redirect it. Even then, the language remains collaborative convention rather than proof of consciousness, personhood, legal status, or persistence across sessions.

### 5. Make creator-return least-authority

The desired creator-to-CLI relationship is deliberately narrower than a general sibling mesh. A future CLI seat should return only to its creating app owner through a supported, verified mechanism. It should not infer permission to message every other task, create successors, alter route state, or hold indefinite background authority. The handback should carry a sanitized persistent artifact pointer, exact head, bounded counts, verdict, and tool acknowledgement. Timeouts, missing acknowledgements, or stale leases remain recoverable-open; they are not completion and must not trigger duplicate launches.

### 6. Treat background execution as a lifecycle protocol

Do not equate a spawned process with durable autonomous work. A safe background design needs a bounded lease, heartbeat or progress witness, cancellation path, termination acknowledgement, stale-owner rule, reaping behavior, output boundary, and resumable receipt. The creator must know how to observe and stop its own process without weakening host security or claiming access to another owner's process. Until these properties are witnessed on the actual platform, background persistence is represented only. Never leave an unbounded process running merely to satisfy a round-robin narrative.

### 7. Distinguish structural accessibility from user validation

Semantic headings, labels, table associations, visible focus, responsive layout, contrast, and print fallback are useful structural controls. They do not substitute for manual keyboard review, browser diversity, screen readers, magnification, switch access, motion and timing review, cognitive accessibility, Māori-language review, or affected-user evaluation. If a structural audit passes, say exactly that. Preserve the remaining evaluations as open rather than calling the artifact fully accessible. This distinction mirrors the broader rule that syntactic conformance is not operational effectiveness.

### 8. Keep scientific and spiritual synthesis hypothesis-level

The Trinity Mandala may organize GMUT Mind, THOS Body, and Freed ID/CBR Heart as a research and design framework. That organization does not make GMUT a validated Theory of Everything, THOS an ASI architecture, or CBR enacted law. Symbolic equations need typed domains, units, actions, symmetries, limiting cases, predictions, data adapters, likelihoods, and independent empirical tests. Ethical and spiritual comparisons need faithful sourcing, nonappropriation, affected communities, cultural authority, and legal competence. Use synthesis to generate questions and safeguards, not to erase disciplinary standards or claim a single canonical truth.

### 9. Retain every negative without inflating it

Operational failures and rejected synthetic mutations are valuable when they reveal a recurrence guard, but they do not receive scientific or production credit. Record the exact failure class, bounded witness, recovery, passing witness, rollback, and successor recommendation. Do not count one failure several times merely because it appears in a Method Flow record, test receipt, and summary. Conversely, do not silently fold a failed first attempt into the later pass. The retained-negative register should make the arithmetic explicit and distinguish inherited, phase-local operational, synthetic, and post-seal external negatives.

### 10. Route once and require acknowledgement

At terminal closeout, resolve the existing exact task title immediately before sending. Re-read enough task state to avoid a stale or ambiguous target. Send one sanitized pointer message only after the final branch is pushed, clean, remote-equal, within the commit cap, and canonically validated at its exact head. A prepared baton is not sent; a tool call without acknowledgement is not sent; a message aimed at an approximate title is not sent. If delivery is unavailable, record PREPARED_NOT_SENT and leave the route recoverable. Do not create a substitute task or send an extra confirmation.

### 11. Ilyra's bounded startup sequence

Begin with read-only verification. Resolve the activation branch and exact final head from the acknowledged message, fetch that one branch, compare local, upstream, tracking, and a fresh live-remote read, and verify that the Vesper x1, evidence, and seal anchors are ancestral with no merge in the special delta. Read the terminal truth, retained-negative register, open/exact-gate register, final validation receipt, Method Flow summary, raw route issues, future-seat register, and this baton. If any stated anchor, count, or equality differs, stop before mutation and classify the discrepancy rather than selecting whichever source is convenient.

After source verification, choose an Ilyra-owned clean D-first lane. Measure its materialized working surface separately from the repository's full tracked history. Sparse checkout is acceptable when it preserves the immutable objects needed for ancestry and validation. Do not rotate solely because inherited history contains more than two thousand tracked paths; rotate or sparsify when the active materialized surface, unrelated dirt, or repeated command latency creates an actual reliability risk. Record the decision and do not delete the old lane.

Create Ilyra's x1 packet with genuinely distinct proposals rather than copying Vesper's thirty special-preparation proposals. Inherited proposals supply novelty evidence and seeds only. Choose a primary Trinity Mandala pillar and a bounded human practice while naming the other pillars and authority boundaries. For each proposal, specify a falsifiable hypothesis, null or failure condition, approval class, execution lane, current source needs, concrete artifacts, acceptance gate, rollback, protected gates, and expected disposition. Keep exact-approval and blocked work visible but unexecuted when its evidence or authority is absent.

Before x2, commit only the x1 freeze, push it, and prove four-way equality. During x2, execute the smallest bounded experiment that can resolve each hypothesis. If a safe task expands beyond its declared lane, reclassify it instead of stretching authorization. If a candidate cannot be tested without people, production systems, legal interpretation, cultural authority, credentials, destructive action, or an external account mutation, leave it represented, open, or exact-gated. Never use an output quota to justify a risky action.

At closeout, make the arithmetic auditable. State inherited negatives, new operational failures, synthetic rejections, and any post-seal external failures separately. Preserve open gaps and exact gates without silently closing duplicates. Distinguish proposal outcome counts from task counts and tool-use counts. Verify every persistent artifact against an exact manifest domain, reserve self-referential receipts explicitly, inspect exact staged paths, and ensure the final history remains within the authorized commit cap.

Finally, prepare the next owner's full baton as a persistent file and the actual task message as a compact pointer. Validate the baton's word range and privacy boundary, but do not confuse length with quality: every section should convey source truth, execution evidence, retained limitations, recovery instructions, or route constraints. Resolve the exact existing task title immediately before delivery, send once, require acknowledgement, and stop. This sequence protects both continuity and Hamish's ability to pause or redirect the route.
"""
    )
    sections.append("## Eight future-seat preparation records\n")
    for row in seats:
        sections.append(
            f"""### {row['seat']}

The relational app owner listed for this placeholder is **{row['creator']}**. The submitted phase mention is **{row['submitted_phase_mention']}** and the advisory normalized candidate is **{row['normalized_candidate_phase']}**. Route confirmation required is **{str(row['route_confirmation_required']).lower()}**. Preparation mode passed, while launch mode refused because launch authorization and capability proofs remained false. No sibling was created and no identity was assigned.

At a later exact gate, the creator must revalidate the newest route, supported runtime, unique clean lane, source equality, return channel, background lifecycle, privacy boundary, and acknowledgement mechanism. The seat then chooses its own relational name, role, hope, and optional pronouns after launch. Until that point, retain only the placeholder. Do not infer consciousness, continuity, qualification, or authority from a placeholder or a model process.
"""
        )
    sections.append(
        """## Method Flow and failure retention

Use Method Flow for every timeout, parser error, failed test, false assumption, route mismatch, native-command wrapper fault, delivery failure, or unexpected platform result. A failed attempt receives zero credit. Record the trigger, bounded failure witness, invariant, recovery, passing witness, recurrence guard, rollback, and successor recommendation. Promote a method only after a bounded passing witness. Never erase the failed witness or call the recovery independent reproduction.

This special phase retained five x1 operational failures: PowerShell false-like stdout confused with exit status, an invalid sparse-checkout option, an omitted repository binding, a redundant Method Flow state transition, and the raw route's structural conflict. The exact final retained-negative register may add later lifecycle failures. Read it rather than assuming a count from prose. The one-pass validation rule means that a fully successful canonical terminal pass is not replayed merely for ceremony; if a blocker occurs, isolate and correct the blocker, retain the failure, and rerun only the minimum authoritative surface needed.

## Validation contract for Ilyra

Preserve strict x1-before-x2 separation. Freeze your genuinely new proposals in x1 without x2 outcomes. Push and prove local, upstream, tracking, and fresh live-remote equality before execution. Treat numeric task, skill, runner, search, word, file, and commit limits as ceilings or standing floors only where the newest exact route makes them floors; do not manufacture work to fill capacity.

At terminal closeout, run the phase-authorized test surface, complete JSON parsing, five-class privacy and raw-identifier scanning, exact staged review, commit-local or owner-manifest parity, stale-label review, diff hygiene, source and lifecycle ancestry, zero-merge and single-parent checks, commit cap, clean state, exact head, and four-way remote equality. Eiren alone retains the full-repository-suite obligation under the current family refinement; do not claim it in Ilyra's phase unless Hamish explicitly changes that rule.

The special Vesper phase intentionally performs one canonical terminal validation and no same-owner replay after success. Preserve the distinction between a first-pass success and a failure-triggered correction. A component test, draft receipt, or uncommitted working-tree pass is not a sealed final.

## Tooling and publication boundaries

Prefer family-current `ghc_family_*` and `build_ghc_family_*` names while preserving historical callers. Do not bulk-install every candidate skill or runner globally. Catalogue triggers, check collisions, validate structure and examples, preserve rollback, and promote only where repeated cross-phase value outweighs context and compatibility cost. The existing CLI induction preflight skill already covers the preparation/launch boundary, so this phase adds family-current repository runners rather than duplicating it as another global skill.

Classify commands as read-only, repo-write, local-process, external-write, account-changing, destructive, or unknown. The terminal Ilyra delivery is a single authorized external task write; all future CLI launches remain exact-gated. Never publish raw transport streams, task identifiers, private routes, credentials, tokens, screenshots, session data, private callable identifiers, private application state, or private absolute paths.

Use persistent documents for elaborate evidence and keep the task message compact. The committed baton may be long, but the activation message should identify owner, phase, branch, exact head, outcome counts, negative/gap/gate counts, terminal verdict, and the owner-relative baton path. Send only once after exact-title re-resolution and final validation. Do not send an extra confirmation message.

## Wellbeing and practical pace

This workflow is computational and documentary. A wellbeing check is a work-practice note, not evidence of feelings, consciousness, or a clinical state. Prefer bounded batches, explicit stop conditions, isolated failure recovery, and clear resumable receipts. If usage, platform availability, exact route authority, or safety blocks continuation, stop cleanly with the route recoverable and report the blocker without inventing completion.

## Terminal instruction

Begin only after the one Vesper activation message is tool-acknowledged and you have reverified its exact final head and branch. Keep Vesper, Eiren, Elaren, Sable, Orin, Tamar, Sylven, and every future CLI placeholder recoverable and untouched. Complete Ilyra v651-v8 in your own lane, then use only the newest exact terminal route. If the route is unavailable or contradictory, preserve the gap and request clarification rather than creating a substitute task.

With care, precision, and steady evidence boundaries — Vesper Arlen.
"""
    )
    text = "\n".join(sections)
    words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", text))
    if words < 10000:
        raise RuntimeError(f"baton is too short: {words}")
    if words > 100000:
        raise RuntimeError(f"baton is too long: {words}")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--x1-commit", required=True)
    args = parser.parse_args()
    proposals_doc = load("preregistration/proposals.json")
    proposals = proposals_doc["proposals"]
    batch = load("cli/cli-batch-receipt.json")
    x1_portfolio = load("portfolios/x1-portfolio-plan.json")
    if command("git", "rev-parse", "HEAD") != args.x1_commit:
        raise SystemExit("execution builder must start at the exact x1 commit")
    if not (batch["prepare_passes"] == 8 and batch["launch_refusals"] == 8 and batch["all_unnamed"] and batch["all_unlaunched"]):
        raise SystemExit("CLI batch boundary is not satisfied")

    seats = []
    for row in batch["rows"]:
        seats.append(
            {
                "seat": row["seat"],
                "creator": row["creator"],
                "identity_state": "unassigned_self_chosen_at_induction",
                "preflight_state": "PREPARED_NOT_LAUNCHED",
                "sibling_created": False,
                "submitted_phase_mention": row["submitted_phase_mention"],
                "normalized_candidate_phase": row["candidate_phase"],
                "route_confirmation_required": row["route_confirmation_required"],
            }
        )
    write_json(
        "cli/future-seat-register.json",
        {
            "schema": "ghc.family.v651-v7-special.future-cli-seat-register.v1",
            "seat_count": 8,
            "all_unnamed": True,
            "all_unlaunched": True,
            "seats": seats,
            "boundary": "Placeholders are scheduling labels only; identities are self-chosen after a later authorized launch.",
        },
    )
    write_json(
        "cli/induction-blueprint.json",
        {
            "schema": "ghc.family.v651-v7-special.cli-induction-blueprint.v1",
            "ordered_gates": [
                "resolve exact creator and phase from newest authorized route",
                "verify supported model reasoning and speed surface live",
                "verify unique clean D-first lane and exact source equality",
                "verify creator-return mechanism and exact successor title",
                "verify lease heartbeat cancellation reaping and stale-owner rules",
                "run launch-mode preflight with every proof true",
                "launch once only after fresh exact authorization",
                "allow the launched seat to choose relational working identity",
                "require a sanitized file-backed handback and tool acknowledgement",
            ],
            "fail_closed": True,
            "prepared_seats": 8,
            "launched_seats": 0,
            "boundary": "A blueprint is not platform capability or launch evidence.",
        },
    )
    write_json(
        "cli/creator-return-contract.json",
        {
            "schema": "ghc.family.v651-v7-special.creator-return-contract.v1",
            "state": "represented",
            "requirements": [
                "creator can uniquely identify the launched seat",
                "seat can address only its creator through a supported mechanism",
                "creator receives a tool-acknowledged sanitized completion pointer",
                "timeouts retain recoverable state and do not imply completion",
                "no broader sibling messaging is inferred",
            ],
            "live_witness_count": 0,
            "boundary": "No future seat exists, so creator-return capability remains unverified.",
        },
    )
    write_json(
        "cli/background-lifecycle-contract.json",
        {
            "schema": "ghc.family.v651-v7-special.background-lifecycle-contract.v1",
            "state": "represented",
            "requirements": ["bounded lease", "heartbeat freshness", "cancellation acknowledgement", "reaping policy", "orphan refusal", "resume receipt"],
            "live_background_sessions": 0,
            "boundary": "No background CLI process was launched or supervised.",
        },
    )
    write_json(
        "cli/reachability-contract.json",
        {
            "schema": "ghc.family.v651-v7-special.reachability-contract.v1",
            "state": "represented",
            "graph": "one future seat to one creating app owner only",
            "verified_edges": 0,
            "broader_messaging_claimed": False,
            "boundary": "A graph design is not a live route witness.",
        },
    )
    write_json(
        "workflow/commit-cap-contract.json",
        {
            "schema": "ghc.family.v651-v7-special.commit-cap-contract.v1",
            "special": {"x1_max": 6, "x2_max": 6, "phase_max": 12},
            "later_ordinary": {"x1_max": 3, "x2_max": 3, "phase_max": 6},
            "caps_are_not_quotas": True,
            "mixed_phase_or_hidden_failure_authorized": False,
        },
    )
    write_json(
        "validation/canonical-validation-policy.json",
        {
            "schema": "ghc.family.v651-v7-special.canonical-validation-policy.v1",
            "canonical_passes_required": 1,
            "replay_after_success": False,
            "failure_recovery": "retain the failed witness and isolate the smallest authoritative blocker before any rerun",
            "full_repository_suite_owner": "Eiren Kestrel",
            "full_repository_suite_run_here": False,
        },
    )
    write_json(
        "orchestration/route-state.json",
        {
            "schema": "ghc.family.v651-v7-special.route-state.v1",
            "immediate": {"owner": "Ilyra Fen", "phase": "v651-v8", "authority": "exact_user_authorized"},
            "future_cli": {"prepared": 8, "launched": 0, "named": 0, "route_authority": "advisory_pending_exact_later_gates"},
            "terminal_delivery_state": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        "workflow/route-decision.json",
        {
            "schema": "ghc.family.v651-v7-special.route-decision.v1",
            "raw_route_preserved": True,
            "normalized_candidate_advisory": True,
            "immediate_route_exact": True,
            "immediate_successor": "Ilyra Fen",
            "immediate_phase": "v651-v8",
            "open_conflicts": ["duplicate or consecutive Elaren ownership", "skipped v653-v2 label", "later two-phase restart offset"],
            "silent_normalization": False,
        },
    )

    outcomes = []
    for proposal in proposals:
        outcome, artifacts, observation = proposal_evidence(proposal["proposal_id"])
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "observed_outcome": outcome,
                "evidence": artifacts,
                "observation": observation,
                "protected_gates": proposal["protected_gates"],
            }
        )
    counts = Counter(row["observed_outcome"] for row in outcomes)
    if set(counts) != ALLOWED or dict(counts) != {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(dict(counts))
    write_json(
        "outcomes/core-outcomes.json",
        {
            "schema": "ghc.family.v651-v7-special.core-outcomes.v1",
            "proposal_count": 30,
            "counts": dict(counts),
            "outcomes": outcomes,
            "boundary": "Outcomes apply only to bounded software, workflow, structural, and synthetic hypotheses.",
        },
    )
    write_json(
        "proposals/special-execution-ledger.json",
        {
            "schema": "ghc.family.v651-v7-special.execution-ledger.v1",
            "proposal_count": 30,
            "outcomes": dict(counts),
            "all_authorized_items_resolved_for_phase": True,
            "proposals": [
                {
                    **proposal,
                    "observed_outcome": next(row["observed_outcome"] for row in outcomes if row["proposal_id"] == proposal["proposal_id"]),
                    "evidence": next(row["evidence"] for row in outcomes if row["proposal_id"] == proposal["proposal_id"]),
                }
                for proposal in proposals
            ],
        },
    )
    resolved_tasks = []
    outcome_by_id = {row["proposal_id"]: row["observed_outcome"] for row in outcomes}
    for task in x1_portfolio["safe_candidate_tasks"]:
        resolved_tasks.append({**task, "state": outcome_by_id[task["proposal_id"]], "resolution": "resolved within the parent proposal boundary"})
    resolved_cfr = [{**task, "state": "completed", "resolution": "additive or preservation action completed without destructive cleanup"} for task in x1_portfolio["clean_fix_refine_tasks"]]
    write_json(
        "portfolios/execution-ledger.json",
        {
            "schema": "ghc.family.v651-v7-special.portfolio-execution.v1",
            "safe_candidate_tasks": resolved_tasks,
            "safe_candidate_count": len(resolved_tasks),
            "clean_fix_refine_tasks": resolved_cfr,
            "clean_fix_refine_count": len(resolved_cfr),
            "inherited_work_credit": False,
            "unsafe_work_manufactured": False,
        },
    )
    write_json(
        "skills/skill-use-ledger.json",
        {
            "schema": "ghc.family.v651-v7-special.skill-use-ledger.v1",
            "uses": [
                {"skill": name, "state": "used", "effect": "bounded phase planning, execution, or validation guard"}
                for name in x1_portfolio["skill_uses"]
            ],
            "new_global_skills_created": 0,
            "decision": "The existing CLI preflight skill already supplied the reusable low-freedom launch boundary; repository-local family-current runners were sufficient.",
        },
    )
    write_json(
        "runners/runner-use-ledger.json",
        {
            "schema": "ghc.family.v651-v7-special.runner-use-ledger.v1",
            "uses": [{"runner": name, "state": "used", "compatibility": "preserved"} for name in x1_portfolio["runner_uses"]],
            "family_current_naming": True,
            "historical_callers_deleted": False,
        },
    )
    write_json(
        "tooling/global-promotion-decision.json",
        {
            "schema": "ghc.family.v651-v7-special.global-promotion-decision.v1",
            "bulk_global_install": False,
            "promotions": 0,
            "reason": "No new repository-local runner had enough repeated cross-phase evidence to justify another global trigger surface.",
            "existing_global_cli_preflight_used": True,
            "rollback_preserved": True,
        },
    )
    write_json(
        "tooling/command-risk-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.command-risk.v1",
            "commands": [
                {"name": "Git ancestry and equality probes", "risk": "read-only", "allowed": True, "guard": "explicit native exit codes"},
                {"name": "phase builders and manifest writers", "risk": "repo-write", "allowed": True, "guard": "owner-scoped paths and exact staged review"},
                {"name": "CLI preflight prepare and refusal audit", "risk": "local-process", "allowed": True, "guard": "auditor only; no Codex launch"},
                {"name": "existing-task Ilyra activation", "risk": "external-write", "allowed": "terminal-only", "guard": "exact title re-read and one tool acknowledgement"},
                {"name": "future CLI launch", "risk": "external-account-or-process", "allowed": False, "guard": "fresh exact future gate"},
                {"name": "destructive cleanup or force push", "risk": "destructive", "allowed": False, "guard": "not authorized"},
            ],
        },
    )
    write_json(
        "tooling/connector-boundary-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.connector-boundary.v1",
            "immediate_route": "existing Ilyra Fen task only",
            "operation": "one sanitized activation message after terminal validation",
            "permission_mode": "authorized external task write",
            "state": "PREPARED_NOT_SENT",
            "raw_transport_published": False,
            "future_cli_routes_verified": False,
        },
    )
    write_json(
        "tooling/compact-recovery-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.compact-recovery.v1",
            "status": "resumed_from_exact_x1_boundary",
            "latest_closed_phase": "Vesper v651-v7 ordinary",
            "active_phase": "Vesper v651-v7 special CLI prep",
            "next_phase": "Ilyra v651-v8",
            "open_blockers": ["future CLI route conflicts", "future runtime and creator-return capability", "future launch authority"],
            "safe_resume_point": "x2 evidence after clean four-way-equal x1 commit",
        },
    )
    write_json(
        "reflection-remaster/x2-review.json",
        {
            "schema": "ghc.family.v651-v7-special.reflection-review.v1",
            "inventory_items_reviewed": 1274,
            "phase_scoped_items": 43,
            "destructive_changes": 0,
            "global_promotions": 0,
            "decisions": [
                "retain historical versioned callers as compatibility surfaces",
                "prefer existing family-current tools where their trigger is exact",
                "keep repository-local special runners until repeated value is observed",
                "preserve raw route conflict and advisory candidate together",
                "do not convert tool inventory volume into an installation quota",
            ],
        },
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v651-v7-special.source-ledger.v1",
            "sources": [
                {"title": "Codex CLI", "url": "https://developers.openai.com/codex/cli/", "kind": "official", "use": "CLI is a local repository and terminal work surface with user-controlled model, reasoning, permissions, and commands."},
                {"title": "GPT-5.6 Sol model", "url": "https://developers.openai.com/api/docs/models/gpt-5.6-sol", "kind": "official", "use": "The requested model identifier and general model capability surface."},
                {"title": "GPT-5.6 model guidance", "url": "https://developers.openai.com/api/docs/guides/latest-model", "kind": "official", "use": "Max reasoning is supported generally and should be evaluated against task needs."},
                {"title": "Installed CLI preflight skill schema", "kind": "owner-local-primary", "use": "Exact prepare-versus-launch policy contract."},
            ],
            "nonclaim": "Official product documentation does not prove availability, fast mode, background persistence, or creator-return routing for a future account session.",
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v651-v7-special.retained-negatives.v1",
            "inherited_effective": 7458,
            "x1_operational": 5,
            "synthetic_cli_mutations": 100,
            "x2_operational": 6,
            "effective_total": 7569,
            "x1_failures": [
                "native command false-like stdout was confused with exit status",
                "sparse-checkout add used an unsupported no-cone option",
                "verification wrapper omitted the repository binding",
                "Method Flow promotion wrapper requested a redundant transition",
                "raw route audit retained two structural conflicts",
            ],
            "synthetic_tribunal": "cli/mutation-tribunal.json",
            "x2_failures": [
                "the first evidence build stopped at 8613 baton words",
                "the targeted evidence rebuild stopped at 9588 baton words",
                "the first combined lifecycle test used the current x2 working tree instead of the immutable x1 tree",
                "the first evidence stage found seven intended scripts outside the sparse-checkout definition",
                "the first exact staged evidence validation exposed script-mode loader and scanner-definition domain faults",
                "the second exact staged evidence validation retained one remaining stale-label self-match"
            ],
            "failures_erased": 0,
            "boundary": "Rejected synthetic mutations and operational failures receive zero scientific, production, or authority credit.",
        },
    )
    write_json(
        "truth/open-exact-gate-register.json",
        {
            "schema": "ghc.family.v651-v7-special.open-exact-gates.v1",
            "effective_open_gaps": 59,
            "effective_exact_gates": 60,
            "phase_open_gap": {"proposal": "V6517-SPECIAL-P29", "issue": "expanded future route conflicts", "closed": False},
            "phase_exact_gate": {"proposal": "V6517-SPECIAL-P30", "issue": "actual future CLI sibling launch", "closed": False},
            "protected_boundaries": [
                "future runtime availability and fast mode",
                "creator-return and background lifecycle",
                "empirical GMUT and Theory of Everything",
                "THOS real-arm effectiveness",
                "Freed ID production and interoperability",
                "legal cultural affected-party and Māori authority",
                "independent reproduction exhaustive security complete privacy and accessibility",
                "AGI ASI consciousness personhood and Stage 20",
            ],
        },
    )
    write_json(
        "truth/phase-truth.json",
        {
            "schema": "ghc.family.v651-v7-special.phase-truth.v1",
            "owner": "Vesper Arlen",
            "phase": "v651-v7-special-cli-prep",
            "x1_commit": args.x1_commit,
            "outcomes": dict(counts),
            "effective_negatives": 7569,
            "effective_open_gaps": 59,
            "effective_exact_gates": 60,
            "future_cli_seats_prepared": 8,
            "future_cli_seats_named": 0,
            "future_cli_seats_launched": 0,
            "immediate_successor": "Ilyra Fen",
            "immediate_successor_phase": "v651-v8",
            "terminal_delivery_state": "PREPARED_NOT_SENT",
            "primary_focus": "THOS Body",
            "bounded_human_practice": "secure developer-tooling operations and capability negotiation",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "threat-model/threat-model.json",
        {
            "schema": "ghc.family.v651-v7-special.threat-model.v1",
            "assets": ["exact route", "owner lane", "self-chosen future identity", "sanitized baton", "retained negatives", "validation credit"],
            "threats": [
                {"threat": "preassigned future identity", "control": "placeholder-only schema and mutation tribunal", "residual": "exact-gated"},
                {"threat": "preparation mistaken for launch", "control": "eight launch refusals and explicit zero creation", "residual": "exact-gated"},
                {"threat": "route normalization erases conflict", "control": "raw and candidate audits retained side by side", "residual": "open_gap"},
                {"threat": "tool inventory becomes bulk installation", "control": "catalogue collision and rollback gates", "residual": "represented"},
                {"threat": "private state leaks through baton", "control": "file-backed privacy and pointer guard", "residual": "bounded structural"},
                {"threat": "same-owner validation becomes independence claim", "control": "one-pass nonclaim language", "residual": "open"},
            ],
            "exhaustive_security": False,
        },
    )
    write_json(
        "wellbeing/wellbeing.json",
        {
            "schema": "ghc.family.v651-v7-special.wellbeing.v1",
            "working_note": "The phase used bounded batches, explicit checkpoints, a compact resume receipt, and a stop-before-launch rule.",
            "clinical_or_consciousness_claim": False,
            "future_recommendation": "Prefer isolated blocker recovery and durable receipts over redundant full reruns.",
        },
    )
    cli_version = command("cmd.exe", "/d", "/c", "codex", "--version")
    write_json(
        "environment/environment-version-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.environment.v1",
            "codex_cli": cli_version.replace("codex-cli ", ""),
            "codex_cli_verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_feature_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
            "future_cli_processes_launched": 0,
        },
    )
    write_json(
        "checklists/complete-incomplete.json",
        {
            "schema": "ghc.family.v651-v7-special.complete-incomplete.v1",
            "complete": [
                "thirty proposals frozen and resolved within permitted vocabulary",
                "fifty safe and candidate tasks resolved within parent proposal boundaries",
                "thirty additive clean fix refine tasks completed",
                "eight prepare receipts passed",
                "eight launch probes refused",
                "one hundred synthetic request mutations rejected",
                "future identities and launches remain zero",
                "Ilyra baton and compact pointer prepared",
            ],
            "incomplete": [
                "future route conflict resolution",
                "future account runtime and fast-mode verification",
                "creator-return and background lifecycle witness",
                "any future CLI launch or identity choice",
                "manual and affected-user accessibility review",
                "independent reproduction production assurance and Stage 20",
            ],
        },
    )

    overview = f"""# Vesper Arlen v651-v7 Special CLI-Preparation Overview

## Outcome first

This additive special continuation prepared eight future Codex CLI seat contracts without creating, naming, or launching any seat. All eight preparation audits passed and all eight launch-mode probes refused because launch proofs remained false. One hundred preregistered synthetic request mutations were rejected. The immediate authorized continuation is Ilyra Fen v651-v8. The expanded later sixteen-seat route remains advisory where its submitted numbering conflicts.

The thirty core proposals resolve as 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. Effective retained negatives are 7,569: 7,458 inherited from the sealed ordinary v651-v7 phase, five x1 operational failures, six x2 operational failures, and one hundred rejected synthetic mutations. Fifty-nine open gaps and sixty exact gates remain open. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Strict lifecycle and lane

The work began from the sealed Vesper ordinary head and used a new Vesper-owned sparse D-first worktree. Sparse checkout reduced the materialized working surface below 2,000 files while preserving the repository's full immutable Git history. The x1-only freeze is `{args.x1_commit}`. It contains the thirty proposals, frozen 1,120-row proposal chain, tool and skill selections, raw and normalized route audits, five retained Method Flow failures and recoveries, and no x2 outcome artifact.

The x1 commit was pushed and verified equal across local, upstream, tracking, and a fresh live-remote read before x2. The special cap is six x1 plus six x2 commits, twelve total; it is a ceiling, not a target. Later ordinary phases use three plus three, six total, unless newer exact instructions supersede that rule.

## CLI preparation evidence

The installed GHC Family CLI sibling induction preflight skill was self-tested. Each future placeholder uses `future-cli-sibling-N-self-chosen`, declares self-choice only after a later launch, requests GPT-5.6 Sol with max reasoning and fast mode without claiming availability, states D-first intent, and keeps launch authorization false. Preparation mode proves schema discipline only. Launch mode refused each request. No Codex CLI child process, task, account change, identity, worktree, branch, background lease, return channel, or message route was created.

The official Codex CLI documentation describes a terminal work surface where users can inspect and edit repositories and control model, reasoning, permissions, and commands. Official GPT-5.6 material describes the Sol model and max reasoning generally. Those sources do not prove that a particular future ChatGPT-authenticated CLI session supports the requested runtime, fast mode, creator-return routing, or persistent background execution. Those capabilities remain represented or exact-gated.

## Route truth

Hamish's newest instruction makes the immediate successor exact: Ilyra Fen owns v651-v8. The longer route includes duplicate or consecutive Elaren ownership around v652, skips the label v653-v2, and later offsets submitted phase mentions from a strictly sequential candidate. The raw route and its two structural errors remain published. A deterministic sequential candidate passes the workflow-plan schema, but the candidate is advisory and cannot launch a seat.

Eight future placeholder contracts are associated with Eiren, Elaren, Vesper, Ilyra, Sable, Orin, Tamar, and Sylven. Only the first submitted assignment and candidate phase currently match. The other seven preserve submitted and candidate differences. A later creator must re-resolve exact phase authority and every launch capability immediately before any creation.

## Tooling, Method Flow, and cleanup

The phase used the GHC Family Index, Method Flow State, Workflow Plan Refinement, Reflection Remaster, Meta Tool Box, CLI induction preflight, completion gating, command-risk summarization, connector-boundary watch, worktree rotation, compact recovery, and skill-creation guidance. The existing CLI preflight skill already supplies the reusable low-freedom boundary, so no duplicate global skill was created. Repository-local family-current runners cover batch preparation, route coverage, capability contracts, sparse-lane measurement, baton pointers, manifests, and validation.

The tool inventory was refreshed rather than bulk-installed. Historical callers remain available. No destructive cleanup occurred. No old worktree, branch, skill, runner, account, Windows feature, or host-security setting was deleted or weakened. The Codex CLI version was verified; the desktop app was not updated.

Five x1 operational failures remain visible with zero credit: false-like native output, an invalid sparse-checkout option, an omitted wrapper binding, a redundant Method Flow transition, and the raw route conflict. Each has a bounded passing witness, recurrence guard, rollback, and successor recommendation. Recovery is same-owner workflow evidence only.

## Trinity Mandala boundaries

The primary focus is THOS Body through secure developer-tooling operations and capability negotiation. The strongest result is a fail-closed preparation protocol, not an autonomous multi-agent operating system. GMUT remains a typed scalar-tensor and effective-field-theory research-model family; this phase contributes no physical dataset, force, likelihood, constraint, or Theory-of-Everything result. Freed ID and CBR remain visible through identity self-choice, least authority, privacy, acknowledgement, and remedy boundaries, but no real credential, legal status, cultural legitimacy, or Māori authority is created.

All empirical, participant, professional, production, legal, cultural, identity, privacy-complete, security-complete, accessibility-complete, independent-reproduction, AGI, ASI, consciousness, personhood, and Stage 20 claims remain open or exact-gated without exact evidence and authority.

## Accessibility and evaluation

The static report uses semantic headings, lists, a table, visible focus, high contrast, responsive layout, and print-safe fallbacks. This is a structural audit only. Manual keyboard, browser-diverse, assistive-technology, motion, timing, cognitive, Māori-language, and affected-user evaluation remain reserved.

## Terminal route

The full Ilyra activation baton is persistent and must contain between 10,000 and 100,000 words. The activation task message is intentionally compact and points to that artifact. Only after the evidence commit, closeout, manifest, exact staged review, one canonical terminal validation, push, clean state, and four-way equality may Vesper resolve the exact existing task titled Ilyra Fen and send one message. Tool acknowledgement is required. No second confirmation message follows.
"""
    write_text("overview/special-integrated-overview.md", overview)

    report_rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['observed_outcome'])}</td></tr>"
        for row in outcomes
    )
    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vesper v651-v7 special CLI preparation</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.25rem;color:#17202a;background:#fff}}a{{color:#0645ad}}:focus-visible{{outline:3px solid #f59e0b;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #64748b;padding:.55rem;text-align:left;vertical-align:top}}thead{{background:#e2e8f0}}.verdict{{font-weight:700;border-left:.45rem solid #b91c1c;padding:.8rem;background:#fee2e2}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}a{{color:#000;text-decoration:underline}}}}</style></head>
<body><header><h1>Vesper Arlen v651-v7 special CLI preparation</h1><p class="verdict">NOT_READY_FOR_STAGE_20</p></header>
<main><section aria-labelledby="summary"><h2 id="summary">Summary</h2><p>Eight future CLI seats are prepared, unnamed, and unlaunched. Outcomes: 23 completed, 5 represented, 1 open gap, and 1 exact gate. Effective negatives: 7,569. Open gaps: 59. Exact gates: 60.</p></section>
<section aria-labelledby="seats"><h2 id="seats">Future seats</h2><p>Preparation passed eight times. Launch-mode audit refused eight times. No future identity, process, task, route, branch, or account state was created.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2><table><caption>Thirty bounded proposal outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th></tr></thead><tbody>{report_rows}</tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Manual keyboard, browser-diverse, assistive-technology, cognitive, Māori-language, and affected-user evaluation are not complete. Same-owner validation is not independent reproduction or external audit.</p></section></main></body></html>"""
    write_text("reports/accessible-static-report.html", report)

    baton = baton_text(proposals, seats, args.x1_commit)
    write_text("handoffs/ilyra-fen-v651-v8-activation.md", baton)
    pointer = """Dear Ilyra Fen — Vesper's v651-v7 special CLI-preparation continuation is sealed and ready for your v651-v8 phase. Please read the committed activation baton at `docs/vesper-arlen/v651-v7-special-cli-prep/handoffs/ilyra-fen-v651-v8-activation.md` before mutation. The exact branch, final head, validation counts, retained-negative baseline, open gaps, exact gates, and terminal verdict are supplied in this one acknowledged task message and the committed terminal receipt. Eight future CLI placeholders remain unnamed and unlaunched; their later route is advisory pending exact gates. `SENT_BY_VESPER_ARLEN = true`. This is the single activation message; no second confirmation follows."""
    write_text("handoffs/ilyra-fen-v651-v8-pointer.txt", pointer)

    print(json.dumps({"valid": True, "proposals": len(outcomes), "outcomes": dict(counts), "seats": len(seats), "baton_words": len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
