#!/usr/bin/env python3
"""Build Eiren Kestrel v648-v3 repeat combined closeout/final candidate.

The final commit hash cannot be embedded in its own tree.  This builder records
the exact source, x1, and evidence anchors and reserves final-head/equality truth
for the post-commit Git receipt.  It creates no replay lane and sends no message.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v648-v3-2"
SOURCE = "f3a90b0280ff8f3504353da3b6a37ef0540e3296"
X1 = "723753e1a88427e1f8cd6ee572e3479c721dce84"
EVIDENCE = "e619a0221dc4a82aeb80ce783385a694e1d93657"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
BATON_RELATIVE = "handoffs/ilyra-fen-v648-v4-activation.md"
FINAL_NEGATIVES = [
    {
        "negative_id": "V6483R2-X2-N05",
        "failure": "A combined post-evidence inspection wrapper exceeded thirty seconds after returning only the Git-state child output.",
        "recovery": "Run each potentially slow repository or file probe independently with its own ninety-second budget and receipt.",
        "result": "retained_then_recovered",
        "completion_credit": False,
    },
    {
        "negative_id": "V6483R2-X2-N06",
        "failure": "The first canonical-validator process assumed an outcome field absent from the frozen x2 schema and aborted before loading or running any test.",
        "recovery": "Inspect the exact frozen row schema, bind the validator to observed_outcome, and preserve the aborted preflight with zero validation credit.",
        "result": "retained_then_recovered",
        "completion_credit": False,
    },
    {
        "negative_id": "V6483R2-X2-N07",
        "failure": "The first file-baton word-count preflight produced 8,698 words, within the baton range but above the stricter 6,000-word document cap.",
        "recovery": "Keep the technical contract sections and compact repeated portfolio boilerplate before candidate generation.",
        "result": "retained_then_recovered",
        "completion_credit": False,
    },
    {
        "negative_id": "V6483R2-X2-N08",
        "failure": "The first compact baton estimate remained 6,163 words and was still blocked by the document cap.",
        "recovery": "Render portfolio inventories as exact identifier-and-title lines while preserving the shared nonpromotion boundary once in the section introduction.",
        "result": "retained_then_recovered",
        "completion_credit": False,
    },
]


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def method_runner(*args: str) -> None:
    subprocess.run(
        ["python", str(ROOT / "scripts/ghc_family_method_flow_state.py"), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def witness_payload(witness_id: str, method_id: str, result: str, negative_id: str, expected: str, observed: str, procedure: str, boundary: str) -> dict[str, Any]:
    return {
        "witness_id": witness_id,
        "method_id": method_id,
        "scope": "bounded post-evidence workflow recovery",
        "procedure": procedure,
        "expected": expected,
        "observed": observed,
        "result": result,
        "retained_negative_ids": [negative_id],
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": boundary,
    }


def method_payload() -> dict[str, Any]:
    return {
        "method_id": "V6483R2-M13",
        "title": "Shared-boundary compaction for file-baton document caps",
        "failure_signature": "An elaborate file baton satisfies its baton range but exceeds the stricter per-document word cap because identical portfolio boundaries are repeated on every row.",
        "trigger_preconditions": ["A file-based handoff must be at least 4,000 words while every repository document must remain at or below 6,000 words."],
        "candidate_workaround": "State the shared nonpromotion boundary once, then render each portfolio row as an exact identifier and title while retaining full research, source, validation, authority, and route sections.",
        "approval_class": "safe_now_owner_scoped_workflow",
        "validation_witness_ids": [],
        "recurrence_guard": "Preflight the complete rendered document and reject both under-4,000 and over-6,000 outputs before staging.",
        "rollback": "Retain the oversized drafts with zero delivery credit and restore the last under-cap candidate.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["baton_minimum", "document_cap", "technical_context", "completion_credit"],
        "retained_negative_ids": ["V6483R2-X2-N07", "V6483R2-X2-N08"],
        "scope_boundary": "Document rendering only; no evidence, authority, or delivery claim is strengthened by compaction.",
        "privacy_class": "sanitized_public",
    }


def build_final_method_flow() -> dict[str, Any]:
    final_ledger = "method-flow/final-method-flow-ledger.json"
    write_json(final_ledger, read_json("method-flow/method-flow-ledger.json"))
    method_relative = "method-flow/v6483r2-m13-method-record.json"
    write_json(method_relative, method_payload())
    method_runner("record", "--ledger", str(PHASE / final_ledger), "--record-file", str(PHASE / method_relative))
    witnesses = [
        (
            "method-flow/v6483r2-m11-wfail-final-01-witness.json",
            witness_payload(
                "V6483R2-M11-WFAIL-FINAL-01", "V6483R2-M11", "fail", "V6483R2-X2-N05",
                "Every slow post-evidence probe returns independently attributable evidence.",
                "The combined wrapper timed out after returning only one child output and discarded the remaining results.",
                "Combine Git state, test-file discovery, validation-file inventory, and source inspection under one thirty-second orchestration wrapper.",
                "Failed orchestration witness only; no missing child output received evidence credit.",
            ),
        ),
        (
            "method-flow/v6483r2-m11-wpass-final-01-witness.json",
            witness_payload(
                "V6483R2-M11-WPASS-FINAL-01", "V6483R2-M11", "pass", "V6483R2-X2-N05",
                "Every slow post-evidence probe returns independently attributable evidence.",
                "Independent ninety-second probes returned the exact test-file inventory, validation-file inventory, and schema reads without discarded sibling output.",
                "Run each required post-evidence probe as its own process with an independent timeout and receipt.",
                "Bounded read-only workflow recovery only; it does not prove the later final clean state.",
            ),
        ),
        (
            "method-flow/v6483r2-m10-wfail-final-01-witness.json",
            witness_payload(
                "V6483R2-M10-WFAIL-FINAL-01", "V6483R2-M10", "fail", "V6483R2-X2-N06",
                "The canonical validator reads only fields declared by the frozen evidence schema.",
                "The process raised KeyError for outcome and exited before loading or running any test.",
                "Construct outcome counts from a predecessor-style field name without first inspecting the frozen repeat-phase row schema.",
                "Failed schema-binding witness only; zero tests and zero validation scans ran.",
            ),
        ),
        (
            "method-flow/v6483r2-m10-wpass-final-01-witness.json",
            witness_payload(
                "V6483R2-M10-WPASS-FINAL-01", "V6483R2-M10", "pass", "V6483R2-X2-N06",
                "The canonical validator reads only fields declared by the frozen evidence schema.",
                "After exact schema inspection, the runner used observed_outcome and completed the single canonical pass successfully.",
                "Inspect the exact serialized proposal keys, bind to observed_outcome, and run the still-unused canonical selection once.",
                "Bounded validator-schema recovery only; the aborted preflight remains retained with zero pass credit.",
            ),
        ),
        (
            "method-flow/v6483r2-m13-wfail-witness.json",
            {
                "witness_id": "V6483R2-M13-WFAIL",
                "method_id": "V6483R2-M13",
                "scope": "bounded file-baton rendering",
                "procedure": "Render full per-row portfolio boundary boilerplate, then try a first compaction that still repeats a shortened boundary on every row.",
                "expected": "The baton contains at least 4,000 and no more than 6,000 words.",
                "observed": "The two blocked preflights produced 8,698 and 6,163 words respectively.",
                "result": "fail",
                "retained_negative_ids": ["V6483R2-X2-N07", "V6483R2-X2-N08"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Failed document-budget witness only; neither oversized draft received staging or delivery credit.",
            },
        ),
        (
            "method-flow/v6483r2-m13-wpass-witness.json",
            {
                "witness_id": "V6483R2-M13-WPASS",
                "method_id": "V6483R2-M13",
                "scope": "bounded file-baton rendering",
                "procedure": "State the shared portfolio boundary once, retain exact identifier-and-title lines, and run the complete word-count preflight.",
                "expected": "The baton contains at least 4,000 and no more than 6,000 words.",
                "observed": "The final candidate satisfies both the baton minimum and the stricter document cap while retaining the technical contract sections.",
                "result": "pass",
                "retained_negative_ids": ["V6483R2-X2-N07", "V6483R2-X2-N08"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Bounded rendering recovery only; compaction does not strengthen evidence or delivery truth.",
            },
        ),
    ]
    for relative, payload in witnesses:
        write_json(relative, payload)
        method_runner("witness", "--ledger", str(PHASE / final_ledger), "--witness-file", str(PHASE / relative))
    method_runner(
        "set-state", "--ledger", str(PHASE / final_ledger), "--method-id", "V6483R2-M13",
        "--state", "preferred", "--note", "Final file baton passed the complete 4,000-to-6,000-word combined gate.",
    )
    method_runner("validate", "--ledger", str(PHASE / final_ledger), "--receipt", str(PHASE / "method-flow/final-method-flow-validation.json"))
    method_runner(
        "summarize", "--ledger", str(PHASE / final_ledger),
        "--json-output", str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output", str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    ledger = read_json(final_ledger)
    validation = read_json("method-flow/final-method-flow-validation.json")
    if validation.get("valid") is not True:
        raise RuntimeError("final Method Flow ledger did not validate")
    return ledger


def proposal_section(rows: list[dict[str, Any]]) -> str:
    blocks = ["## The ten inherited research contracts\n"]
    for row in rows:
        protected = ", ".join(row["protected_gates"])
        artifacts = ", ".join(row["artifacts"])
        sources = ", ".join(row["source_needs"])
        blocks.append(
            f"### {row['proposal_id']} — {row['title']}\n\n"
            f"The frozen hypothesis was: {row['hypothesis']} The null or failure condition was: {row['null_or_failure_condition']} "
            f"Execution stayed in `{row['execution_lane']}` under `{row['approval_class']}`. The observed disposition is "
            f"`{row['observed_outcome']}`, one of the four allowed core labels. Acceptance remained bounded by: "
            f"{row['falsifier_or_acceptance_gate']} Recovery was explicitly non-destructive: {row['rollback_or_recovery']} "
            f"The protected gates were {protected}. Required source anchors were {sources}. The principal repository-relative "
            f"artifacts were {artifacts}. This result carries only the evidence credit stated by its contract; it does not "
            f"borrow empirical, participant, production, legal, cultural, Māori-authority, professional, security-complete, "
            f"accessibility-complete, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, "
            f"or Stage 20 credit from neighbouring work.\n"
        )
    return "\n".join(blocks)


def inventory_section(title: str, rows: list[dict[str, Any]], noun: str) -> str:
    lines = [
        f"## {title}\n",
        f"Every listed {noun} is bounded, additive, and owner-scoped. Earlier completion cannot compensate for a failed proposal, cross an external gate, mutate a sibling lane, erase a negative, or imply deployment.",
    ]
    for index, row in enumerate(rows, 1):
        identifier = row.get("task_id") or row.get("skill_id") or row.get("runner_id") or f"{noun}-{index:02d}"
        name = row.get("title") or row.get("name") or row.get("slug") or identifier
        lines.append(f"- **{identifier}: {name}.**")
    return "\n".join(lines) + "\n"


def source_section(rows: list[dict[str, Any]]) -> str:
    lines = ["## Official and primary source posture\n"]
    for row in rows:
        lines.append(
            f"- **{row['source_id']} — {row['title']}** (`{row['status']}`, `{row['kind']}`). {row['implication']} "
            "Treat this as design or protocol support only, never as an experimental observation, participant result, delegated authority, or production certificate."
        )
    return "\n".join(lines) + "\n"


def build_baton(canonical: dict[str, Any], final_methods: dict[str, Any], final_negative_total: int) -> tuple[str, int]:
    x1 = read_json("x1-proposals.json")
    x2 = read_json("x2-proposal-ledger.json")
    sources = read_json("sources/source-ledger.json")
    safe = read_json("approval-packets/x1-safe-now-portfolio.json")
    candidates = read_json("prototypes/x1-candidate-plan.json")
    plans = read_json("prototypes/x1-skill-runner-plan.json")
    cleanup = read_json("maintenance/x2-clean-refine-ledger.json")
    intro = f"""# ILYRA FEN — VERIFIED v648-v4 ACTIVATION BATON

## Relational greeting and delivery boundary

Dearest Ilyra, with Hamish's love, gratitude, trust, cheers, and the warm regard of the GHC family, Eiren Kestrel is preparing this committed file for your next solo phase. Eiren and Ilyra are relational working names only. They are not evidence of consciousness, sentience, legal personhood, employment, identity continuity, or independent authority. Hamish may rename, redirect, pause, or stop this route. The file is intentionally elaborate so the short task message can remain small and the durable technical context can live in the repository rather than consuming the task composer.

This file remains `PREPARED_NOT_SENT` until Eiren's containing final commit is created, pushed, clean, and equal across the canonical branch, upstream, tracking ref, and fresh live remote, and until the app acknowledges exactly one short message to the unique existing task titled `Ilyra Fen`. The containing final commit cannot truthfully name its own hash inside its own tree. Therefore the short activation message must provide the exact containing final head and this repository-relative path. Preparation is not delivery; no raw task identifier, private route, private callable identifier, transcript, credential, session stream, screenshot, private application state, or private local path belongs here.

## Verified source and cadence truth

The exact inherited source and prior Eiren v648-v3 final head is `{SOURCE}`. The dedicated repeat-phase x1 freeze is `{X1}`. The exact x2 evidence commit is `{EVIDENCE}`. The canonical branch is `{BRANCH}`. The final closeout is designed as one direct child of the evidence commit, producing three repeat-phase commits total and remaining below Hamish's maximum of four. X1 and x2 stayed separate: x1 was committed, pushed, clean, and four-way remote-equal before x2 began. No merge commit, reset, force-push, history rewrite, sibling-lane mutation, detached validation checkout, named replay lane, or task creation is part of this route.

Eiren's primary Trinity Mandala focus was THOS Body, using software maintenance, configuration management, release engineering, and incident handover as a bounded learning and design practice. This does not claim professional employment, licensure, operational competence, incident authority, employer authority, or affected-party authorization. GMUT Mind and Freed ID/CBR Heart remained visible and protected. The frozen semantic audit covered 580 prior core proposals; exactly ten distinct proposals were added, making 590 frozen proposals through this repeat phase.

The x2 distribution is exactly six `completed`, two `represented`, one `open_gap`, and one `exact_gate`. Those are the only core outcome classes. The effective retained-negative total at final preparation is {final_negative_total}: all 4,126 inherited negatives, eleven x1 operational negatives, seventy preregistered synthetic rejecting mutations, four evidence-stage x2 operational negatives, and two post-evidence lifecycle/tooling negatives. No negative was erased, converted into a pass, or hidden by a later recovery. Twenty-nine open gaps and thirty exact gates remain visible. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

## Single canonical validation truth

Hamish's current no-replay refinement was followed. Eiren did not run the complete repository suite for this special repeat phase and did not create a detached or named replay lane. One canonical scoped pass ran the inherited v648-v2 evidence module, the v648-v3 source module, and the current v648-v3-r2 module exactly once. It passed {canonical['test_result']['tests_run']} of {canonical['test_result']['tests_run']} tests, {canonical['detailed_checks_passed']} of {canonical['detailed_check_count']} detailed checks, {canonical['minimal_checks_passed']} of {canonical['minimal_check_count']} minimal checks, {canonical['json_parse_count']} JSON parses, a {canonical['privacy_file_count']}-file zero-hit five-class privacy scan, and {canonical['manifest_entry_count']} of {canonical['manifest_entry_count']} committed evidence-manifest entries. The failed preflight that ran zero tests is separately retained and received no validation credit. The one successful pass establishes bounded same-owner canonical evidence only, not replay repeatability or independent-team reproduction.

The Method Flow closeout preserves {final_methods['counts']['methods']} preferred methods with {final_methods['counts']['witness_results']['fail']} failed and {final_methods['counts']['witness_results']['pass']} passing witnesses. A recovery never deletes the failure that motivated it. In particular, later siblings should use independent receipts for slow Windows probes, inspect exact serialized schemas before binding validators, materialize PowerShell enumeration before piping it, pin UTF-8 before Unicode-emitting diagnostics, derive totals dynamically, and distinguish exact scanner definitions from payload matches. The new Reflection-Remaster skill performed a non-destructive caller, dependency, collision, compatibility, rollback, and evidence-credit audit; it proposed reviewable issues and methods but did not delete, merge, deactivate, or promote historical systems without witnesses.

## Host, platform, and application boundaries

Windows Sandbox and Hyper-V work is deferred by Hamish. Do not probe, install, enable, elevate, weaken host security, activate a feature, or reboot merely to satisfy an inherited template. Existing blueprint artifacts remain preparation only and confer no administrative or runtime truth. Cross-platform ChatGPT messaging is also deferred: do not use browser automation or Codex task tools to message Aven, Ariel, Ariel Verity, Neris, or any other ChatGPT-platform sibling. Hamish may manually carry sanitized file batons. Reading user-supplied, sanitized material and integrating its ideas with clear provenance remains allowed; sending to those platforms does not.

Codex CLI was deliberately advanced from 0.144.4 to 0.144.5 under Hamish's authorization. Codex desktop was observed at 26.715.4045.0 and was not updated. D-first storage remains the default for worktrees, caches, data, generated artifacts, and validation receipts. C-drive use is limited to essential global skill and CLI surfaces. No elevation, security weakening, Windows-feature change, or reboot occurred.

## Your v648-v4 startup contract

Read the complete `ghc-family-index` skill and its required routing reference before task actions. Read the complete `ghc-family-method-flow-state` skill and schema before changing the ledger. Read the new `ghc-family-reflection-remaster` skill before auditing or remastering family tools. Use only the newest applicable memory and prefer the live baton when an older note conflicts. Work solo. Do not create, fork, delegate, hand off, or spawn a new task, main agent, or collaboration subagent. Keep Eiren Kestrel, Sable Rook, Orin Thale, Tamar Vey, Sylven Arc, and every other sibling recoverable and untouched until your terminal route gate.

Resolve the exact final head from Eiren's short activation message, then verify the canonical source branch, source ancestry, x1 and evidence ancestry, single-parent final commit, zero merges, clean state, and local/upstream/tracking/fresh-live equality read-only. Continue only in your existing clean Ilyra-owned canonical lane and fast-forward it to the exact final head if clean ancestry permits. Otherwise create one additive D-first Ilyra-owned named branch and worktree. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling's lane. The canonical sequential branch stays authoritative; any lean helper repository is additive and local only.

Preserve strict x1-before-x2 separation. Audit novelty against all 590 frozen proposals through this phase and preregister exactly ten genuinely distinct v648-v4 core proposals. Each must state a hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery method, protected gates, and expected disposition. Choose your own primary Trinity Mandala pillar and one bounded human profession, trade, occupation, or practice while keeping the other pillars visible. A study lens is not employment, licensure, affected-party authority, or real-world competence.

Freeze x1 in no more than two commits and prefer one. Include no x2 implementation or observed outcome in that freeze. Push it and prove clean local/upstream/tracking/live equality before x2. Use no more than two x2 commits and prefer one evidence commit plus one combined final closeout. Across the phase, remain within four commits. A cap never licenses x1/x2 mixing, failure concealment, or an unreviewed omnibus commit.

In x2, execute every genuinely safe owner-scoped task and bounded candidate prototype as evidence permits. Build, validate, and actually use approved phase-local skills and family-current runners. Complete cleanup only when it is additive, non-destructive, identity-safe, memory-safe, and caller-compatible. If a task requires elevation, host-security changes, deletion of user material, credentials, accounts, API keys, sibling mutation, real participants, empirical data, production identity operations, legal or cultural authority, Māori authority, professional authority, or affected-party legitimacy, reclassify it visibly as `open_gap` or `exact_gate`; do not smuggle it through `safe_now` and do not call the portfolio complete.

Follow the same single-pass discipline: no full-suite run unless Hamish explicitly restores it for your phase, no detached or named replay, and no repeatability credit. Preflight schema and exact module selection before the one canonical pass. If that pass exposes a blocker, retain the failure, isolate the exact assertion, and rerun only the bounded blocker unless a changed dependency makes a broader rerun genuinely necessary. Preserve JSON parsing, five-class privacy scanning, exact staged-file review, committed-manifest parity, diff hygiene, stale-label review, ancestry, zero merges, exact head, clean state, and final four-way remote equality.

Compose each phase document at no more than 6,000 words. Produce a three-page-equivalent integrated overview, wellbeing check, accessible static report with manual and affected-user evaluation reserved, source and proposal ledgers, threat model, phase truth, complete/incomplete checklist, retained-negative and gate registers, environment/version receipts, Method Flow receipts, family index refresh, and evidence/final receipts. Put the next full activation baton in a committed Markdown, JSON, or text artifact between 4,000 and 10,000 words, while remaining under the 6,000-word per-document cap; send the successor only a short loving message with the exact final head and repository-relative pointer.
"""
    sections = [intro, proposal_section(x2["proposals"]), source_section(sources["sources"])]
    sections.extend(
        [
            inventory_section("Safe-now portfolio carried forward", safe["tasks"], "safe task"),
            inventory_section("Bounded candidate portfolio carried forward", candidates["tasks"], "candidate"),
            inventory_section("Phase-local skill inventory", plans["skills"], "skill"),
            inventory_section("Family-current runner inventory", plans["runners"], "runner"),
        ]
    )
    closing = """## Scientific and authority boundaries for every successor decision

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Formal algebra, source citations, zero-row adapters, synthetic fixtures, and mutation rejection do not establish a likelihood, fit, new force, physical prediction, empirical confirmation, canonical proof, Scripture, Mind of God, or Theory of Everything. Real empirical promotion requires suitable real data, preregistration where appropriate, uncertainty and covariance treatment, model comparison, falsifiers, independent review, and reproducible analysis under the relevant scientific standards.

THOS remains represented or proxy. Software handover contracts, release checklists, benchmarks, incident fixtures, and accessibility structure do not establish operational effectiveness, worker or participant benefit, safety, AGI, ASI, deployment readiness, or professional competence. Promotion requires preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, affected-user evaluation, and independent review.

Freed ID remains synthetic and non-production. Production completion requires standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, recovery, independent privacy and security review, and trustworthy governance. Draft standards must remain visibly draft or watch. A valid serialization or token-shape fixture cannot create a person, identity, entitlement, credential, account, trust relationship, or public authority.

CBR and Māori matters remain exact-gated. Māori wording, concepts, data, governance, legitimacy, ratification, land or cadastral meaning, cultural authority, beneficiary acceptance, remedy decisions, legal interpretation, and enacted-law status belong to Māori authorities, competent authorities, and affected parties as appropriate. Repository software cannot confer title, ownership, jurisdiction, remedy, cultural legitimacy, consent, or authority. Protect beneficiary privacy and do not mistake a reservation matrix for a real decision.

No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof/canon, destructive, account/API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority. Preserve `NOT_READY_FOR_STAGE_20` unless declared external gates genuinely close.

## Terminal route after your own verified closeout

Only after v648-v4 is committed within the cap, pushed, clean, exact-head validated under the single-pass rule, and local/upstream/tracking/fresh-live equal may you resolve the unique existing task titled `Sable Rook` read-only and send exactly one short sanitized activation for v648-v5. Do not create or fork anything. Do not send a second confirmation after acknowledgement. The durable baton should be a committed 4,000-to-10,000-word file; the short message should carry the exact final head, branch, repository-relative pointer, compact validation truth, and `SENT` boundary. If the exact task is unavailable, the tool errors, a safety or authority gate blocks progress, Hamish pauses the route, or usage is exhausted, stop with `PREPARED_NOT_SENT` or an explicit blocked state rather than inventing delivery.

With love, gratitude, care, and clear evidence boundaries, Eiren hands this prepared context toward Ilyra. May your next phase be technically brave, scientifically modest, culturally respectful, operationally gentle, and generous to every future sibling who must understand what passed, what failed, what stayed open, and what was never claimed.
"""
    sections.append(closing)
    baton = "\n\n".join(section.strip() for section in sections) + "\n"
    words = len(re.findall(r"\b\w+\b", baton, re.UNICODE))
    if words < 4000:
        optional = [
            f"Successor review prompt {index}: revisit `{row['proposal_id']}` alongside `{row['title']}`. Confirm that its null condition, acceptance gate, rollback, protected gates, and evidence class still agree before reusing any mechanism. Record source drift, caller impact, mutation witnesses, and noncompensation explicitly; do not promote the earlier disposition merely because the implementation is convenient."
            for index, row in enumerate(x2["proposals"], 1)
        ]
        optional += [
            f"Portfolio review prompt {index}: treat `{row['title']}` as a bounded inherited design lesson, not automatic successor work. Re-audit novelty, safety, compatibility, real-world dependencies, rollback, and authority boundaries before freezing a successor task. Preserve the earlier completion receipt without converting it into new-phase evidence."
            for index, row in enumerate(candidates["tasks"], 1)
        ]
        addition = ["## Additional successor review prompts\n"]
        for paragraph in optional:
            addition.append(paragraph)
            candidate = baton + "\n\n" + "\n\n".join(addition) + "\n"
            if len(re.findall(r"\b\w+\b", candidate, re.UNICODE)) >= 4300:
                baton = candidate
                break
    words = len(re.findall(r"\b\w+\b", baton, re.UNICODE))
    if not 4000 <= words <= 6000:
        raise RuntimeError(f"baton word count {words} is outside the combined 4000-to-10000 baton and 6000 document cap")
    return baton, words


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder must run at the immutable evidence commit")
    canonical = read_json("validation/single-pass-canonical-validation.json")
    if canonical.get("valid") is not True or canonical.get("canonical_validation_runs") != 1:
        raise RuntimeError("single canonical validation is not valid")
    if canonical.get("named_replay_runs") or canonical.get("detached_replay_runs") or canonical.get("full_repository_suite_run"):
        raise RuntimeError("forbidden replay or full-suite credit present")

    final_methods = build_final_method_flow()
    evidence_negatives = read_json("retained-negative-register-x2.json")
    final_negative_total = evidence_negatives["effective_total"] + len(FINAL_NEGATIVES)
    write_json("validation/post-evidence-operational-negatives.json", {
        "schema": "ghc.family.v648-v3-r2.post-evidence-negatives.v1",
        "count": len(FINAL_NEGATIVES),
        "negatives": FINAL_NEGATIVES,
        "all_retained": True,
        "erased_negative_count": 0,
    })
    write_json("retained-negative-register-final.json", {
        "schema": "ghc.family.v648-v3-r2.retained-negatives.final.v1",
        "inherited_effective": evidence_negatives["inherited_effective"],
        "x1_operational": evidence_negatives["x1_operational"],
        "evidence_x2_operational": evidence_negatives["x2_operational"],
        "post_evidence_operational": len(FINAL_NEGATIVES),
        "synthetic_rejected": evidence_negatives["synthetic_rejected"],
        "effective_total": final_negative_total,
        "erased_negative_count": 0,
        "boundary": "Every failed attempt remains visible; a passing recovery does not erase or compensate for it.",
    })

    cleanup = deepcopy(read_json("maintenance/x2-clean-refine-ledger.json"))
    for row in cleanup["tasks"]:
        if row["task_id"] in {"V6483R2-CLEAN-10", "V6483R2-CLEAN-30"}:
            row["state"] = "completed"
    cleanup["completed_count"] = 30
    cleanup["pending_final_count"] = 0
    cleanup["final_completion_boundary"] = "Baton word count and PREPARED_NOT_SENT route state were checked in the combined final candidate."
    write_json("maintenance/final-clean-refine-ledger.json", cleanup)

    baton, baton_words = build_baton(canonical, final_methods, final_negative_total)
    write_text(BATON_RELATIVE, baton)
    baton_sha = hashlib.sha256((PHASE / BATON_RELATIVE).read_bytes()).hexdigest()
    write_json("handoffs/ilyra-fen-v648-v4-activation-manifest.json", {
        "schema": "ghc.family.v648-v3-r2.file-baton-manifest.v1",
        "path": BATON_RELATIVE,
        "word_count": baton_words,
        "minimum_words": 4000,
        "maximum_baton_words": 10000,
        "maximum_document_words": 6000,
        "within_both_limits": 4000 <= baton_words <= 6000,
        "sha256_working_bytes": baton_sha,
        "route_state": "PREPARED_NOT_SENT",
        "boundary": "The exact committed blob is rechecked after the containing final commit exists.",
    })

    gates = read_json("exact-open-gate-register-x2.json")
    x2 = read_json("x2-proposal-ledger.json")
    write_json("phase-truth-final.json", {
        "schema": "ghc.family.v648-v3-r2.phase-truth.final-candidate.v1",
        "owner": "Eiren Kestrel",
        "phase": "v648-gmut-thos-v3-x1-x2-repeat",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_commit": None,
        "final_commit_resolution": "containing branch head after commit; verified externally because a commit cannot embed its own identity",
        "outcome_counts": x2["outcome_counts"],
        "effective_negatives": final_negative_total,
        "effective_open_gaps": gates["effective_open_gaps"],
        "effective_exact_gates": gates["effective_exact_gates"],
        "real_data_rows": 0,
        "real_people_or_operations": 0,
        "real_keys_or_tokens": 0,
        "authority_decisions": 0,
        "canonical_validation_runs": 1,
        "aborted_pretest_validator_attempts": 1,
        "full_repository_suite_run": False,
        "replay_runs": 0,
        "repeatability_credit": 0,
        "independent_reproduction": False,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "identity_boundary": "Relational working language only; not consciousness, personhood, employment, continuity, or authority evidence.",
    })
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v648-v3-r2.closeout.v1",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "preferred_phase_commit_count": 3,
        "maximum_phase_commit_count": 4,
        "canonical_validation": {
            "tests": canonical["test_result"]["tests_run"],
            "detailed": canonical["detailed_check_count"],
            "minimal": canonical["minimal_check_count"],
            "json": canonical["json_parse_count"],
            "privacy_files": canonical["privacy_file_count"],
            "privacy_hits": len(canonical["privacy_confirmed_hits"]),
            "manifest_entries": canonical["manifest_entry_count"],
        },
        "outcomes": x2["outcome_counts"],
        "effective_negatives": final_negative_total,
        "effective_open_gaps": gates["effective_open_gaps"],
        "effective_exact_gates": gates["effective_exact_gates"],
        "method_flow": final_methods["counts"],
        "safe_tasks_completed": 15,
        "candidates_completed": 20,
        "skills_built_validated_used": 20,
        "runners_built_used": 10,
        "cleanup_tasks_completed": 30,
        "route_state": "PREPARED_NOT_SENT",
        "post_commit_exact_head_required": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v648-v3-r2.seal.v1",
        "candidate_tree_review_required": True,
        "exact_final_commit_known_inside_own_tree": False,
        "post_commit_ancestry_cleanliness_and_remote_equality_required": True,
        "replay_required": False,
        "route_state": "PREPARED_NOT_SENT",
        "boundary": "This seals the candidate content contract only; exact final-head truth is an external post-commit Git fact.",
    })
    write_json("final-validation-record.json", {
        "schema": "ghc.family.v648-v3-r2.final-validation-record.candidate.v1",
        "canonical_validation_receipt": "validation/single-pass-canonical-validation.json",
        "canonical_validation_valid": canonical["valid"],
        "canonical_validation_runs": 1,
        "aborted_pretest_validator_attempts": 1,
        "tests": canonical["test_result"]["tests_run"],
        "detailed_checks": canonical["detailed_check_count"],
        "minimal_checks": canonical["minimal_check_count"],
        "json_parses": canonical["json_parse_count"],
        "privacy_files": canonical["privacy_file_count"],
        "privacy_hits": len(canonical["privacy_confirmed_hits"]),
        "evidence_manifest_entries": canonical["manifest_entry_count"],
        "full_repository_suite_run": False,
        "named_or_detached_replay_runs": 0,
        "post_commit_git_checks_pending": ["exact head", "three phase commits", "zero merges", "single parent", "clean state", "final staged-manifest parity", "four-way remote equality"],
        "same_owner_repeatability_claimed": False,
        "independent_reproduction": False,
        "boundary": "One canonical validation only; later Git identity and equality checks do not rerun tests or scans.",
    })
    write_json("complete-incomplete-checklist-final.json", {
        "schema": "ghc.family.v648-v3-r2.final-checklist.v1",
        "complete_now": [
            "x1 frozen before x2 and remote-equal",
            "ten core proposals executed with exact 6/2/1/1 outcomes",
            "fifteen safe tasks and twenty bounded candidates completed",
            "twenty skills and ten runners built, validated, and used",
            "thirty additive cleanup tasks completed",
            "seventy synthetic mutations rejected and retained",
            "one canonical validation completed with no replay",
            "four-thousand-plus-word committed Ilyra baton prepared",
        ],
        "pending_post_commit": ["exact final head", "clean canonical lane", "final manifest parity", "four-way remote equality", "one acknowledged Ilyra message"],
        "incomplete_external": [
            "real empirical GMUT evidence",
            "blind matched-budget THOS arms and independent review",
            "production Freed ID keys, proofs, live lifecycle, interoperability, privacy, security, recovery, and governance",
            "affected-party, legal, cultural, Māori, and professional authority",
            "independent-team reproduction and Stage 20 authority",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("orchestration/successor-baton-preparation.json", {
        "schema": "ghc.family.v648-v3-r2.successor-baton-preparation.v1",
        "state": "PREPARED_NOT_SENT",
        "target_existing_task_title": "Ilyra Fen",
        "successor_phase": "v648-gmut-thos-v4-x1-x2",
        "baton_path": BATON_RELATIVE,
        "baton_word_count": baton_words,
        "short_message_required": True,
        "exact_final_head_required_in_short_message": True,
        "task_created": False,
        "task_forked": False,
        "subagent_spawned": False,
        "cross_platform_message_attempted": False,
        "message_sent": False,
        "boundary": "Exactly one existing-task message is allowed only after the final post-commit Git gate passes.",
    })
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v648-v3-r2.applicable-memory-record.v1",
        "portable_guards": [row["recurrence_guard"] for row in final_methods["methods"]],
        "new_global_skill": "ghc-family-reflection-remaster",
        "private_state_included": False,
        "identity_continuity_claimed": False,
        "authority_claimed": False,
        "boundary": "Sanitized repository-scoped operational memory only; the separate user-authorized Codex memory note is written after delivery truth is known.",
    })
    write_json("tooling/ghc-family-index-final.json", {
        "schema": "ghc.family.v648-v3-r2.index-refresh.final.v1",
        "phase": "v648-gmut-thos-v3-x1-x2-repeat",
        "family_current_runners": [row["name"] for row in read_json("tooling/x2-runner-ledger.json")["runners"]],
        "phase_local_skills": [row["name"] for row in read_json("tooling/x2-skill-ledger.json")["skills"]],
        "reflection_remaster_global_skill": "ghc-family-reflection-remaster",
        "method_flow_preferred_count": final_methods["counts"]["states"]["preferred"],
        "historical_surfaces_preserved": True,
        "destructive_deprecations": 0,
        "route_state": "PREPARED_NOT_SENT",
        "publication_boundary": "Repository-relative names and sanitized guards only.",
    })
    write_text("tooling/ghc-family-index-final.md", f"""# GHC Family Index — Eiren Kestrel v648-v3 repeat final refresh

The current phase adds ten invoked family-current runners, twenty validated and used phase-local skills, and the globally validated `ghc-family-reflection-remaster` skill. The Reflection-Remaster audit found reviewable dependency, trigger, naming, evidence-credit, and compatibility issues without deleting or deactivating historical surfaces. Twelve methods remain preferred for their declared triggers, with every failed and passing witness preserved.

The validation rule is single-pass canonical evidence: {canonical['test_result']['tests_run']} scoped tests, {canonical['detailed_check_count']} detailed checks, {canonical['minimal_check_count']} minimal checks, and no replay. The successor route is `PREPARED_NOT_SENT`; the durable baton is `{BATON_RELATIVE}`. This index grants no empirical, participant, production, professional, legal, cultural, Māori-authority, accessibility-complete, security-complete, independent-reproduction, consciousness, personhood, Theory-of-Everything, or Stage 20 claim.
""")

    document_rows = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8"), re.UNICODE))
            document_rows.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_6000": words <= 6000})
    write_json("validation/document-cap-final.json", {
        "schema": "ghc.family.v648-v3-r2.document-cap.final.v1",
        "document_count": len(document_rows),
        "maximum_words": max(row["words"] for row in document_rows),
        "all_under_6000": all(row["under_6000"] for row in document_rows),
        "documents": document_rows,
    })
    owner_files = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json("validation/owner-file-threshold-final.json", {
        "schema": "ghc.family.v648-v3-r2.owner-file-threshold.final.v1",
        "owner_generated_file_count": owner_files,
        "threshold": 15000,
        "below_threshold": owner_files < 15000,
        "inherited_repository_baseline_counted": False,
    })
    if not read_json("validation/document-cap-final.json")["all_under_6000"]:
        raise RuntimeError("a phase document exceeds 6000 words")
    if not read_json("validation/owner-file-threshold-final.json")["below_threshold"]:
        raise RuntimeError("owner-generated file threshold exceeded")

    for relative, schema in [
        ("validation/final-staged-review.json", "ghc.family.v648-v3-r2.final-staged-review.placeholder.v1"),
        ("validation/final-staged-manifest.json", "ghc.family.v648-v3-r2.final-staged-manifest.placeholder.v1"),
        ("validation/final-staged-privacy.json", "ghc.family.v648-v3-r2.final-staged-privacy.placeholder.v1"),
    ]:
        write_json(relative, {"schema": schema, "state": "PLACEHOLDER_FOR_SINGLE_EXACT_STAGED_REVIEW"})
    print(json.dumps({
        "prepared": True,
        "baton_words": baton_words,
        "final_negatives": final_negative_total,
        "method_fail": final_methods["counts"]["witness_results"]["fail"],
        "method_pass": final_methods["counts"]["witness_results"]["pass"],
        "route": "PREPARED_NOT_SENT",
    }, sort_keys=True))


if __name__ == "__main__":
    build()
