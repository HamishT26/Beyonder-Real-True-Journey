#!/usr/bin/env python3
"""Build the combined Lyren Moss v653-v2 closeout and content seal."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v653_v2_validation_common import (
    PHASE,
    REPO,
    phase_public_paths,
    read_json,
    write_json,
)


SOURCE = "97989717f8447ef2fa09a37a92c76617dea30874"
X1 = "90cc4cff205fef8b7fe0fb1218083e9ced14f146"
EVIDENCE = "6728c0e6d2a5b16a56f08b80e60fdbfe36818427"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)
FINAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6532-FINAL-N01",
        "category": "powershell_foreach_direct_pipe_parser_error",
        "failed": (
            "A bounded closeout inspection placed a pipeline directly after a "
            "PowerShell foreach block and failed with 'An empty pipe element is not allowed.'"
        ),
        "recovery": (
            "Materialize foreach results in an owner-local array, then pipe that array "
            "to the bounded formatter; the corrected closeout inspection completed."
        ),
        "recurrence_guard": (
            "Materialize PowerShell foreach output before piping it, especially in "
            "single-line bounded probes."
        ),
    },
    {
        "negative_id": "V6532-FINAL-N02",
        "category": "retained_negative_register_filename_assumption",
        "failed": (
            "A combined read-only probe guessed a nonexistent x1 retained-negative "
            "register filename and ended with a file-not-found result."
        ),
        "recovery": (
            "Discover retained-negative files with rg --files before reading them; "
            "the bounded discovery confirmed the existing x2 and final register paths."
        ),
        "recurrence_guard": (
            "Use exact rg --files discovery before reading lifecycle filenames that "
            "have not already been confirmed."
        ),
    },
    {
        "negative_id": "V6532-FINAL-N03",
        "category": "stale_closeout_test_expectation_after_retained_negatives",
        "failed": (
            "The first scoped closeout test after adding retained final negatives "
            "failed because its expected negative and Method Flow totals were stale."
        ),
        "recovery": (
            "Update the scoped closeout assertions to the frozen terminal totals after "
            "recording this failure, rebuild once, and rerun the bounded test."
        ),
        "recurrence_guard": (
            "Freeze retained-negative and Method Flow totals before the final scoped "
            "closeout test and keep count assertions synchronized with that freeze."
        ),
    },
]
FINAL_SELF_EXCLUSIONS = {
    "docs/lyren-moss/v653-v2/validation/final-owner-manifest.json",
    "docs/lyren-moss/v653-v2/validation/final-staged-manifest.json",
    "docs/lyren-moss/v653-v2/validation/final-staged-review.json",
}
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, scientific "
    "or operational authority, legal or cultural authority, Māori authority, independent agency, "
    "production certification, independent reproduction, Theory-of-Everything proof, AGI/ASI "
    "evidence, or Stage 20 authority."
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def method_run(*args: str) -> None:
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


def extend_final_method_flow() -> dict[str, Any]:
    ledger = PHASE / "method-flow/final-method-flow-ledger.json"
    shutil.copyfile(PHASE / "method-flow/evidence-method-flow-ledger.json", ledger)
    start = read_json(ledger)["counts"]["methods"] + 1
    for offset, negative in enumerate(FINAL_NEGATIVES, start):
        method_id = f"V6532-METHOD-{offset:02d}"
        fail_id = f"V6532-WITNESS-{offset:02d}-F"
        pass_id = f"V6532-WITNESS-{offset:02d}-P"
        root = PHASE / "method-flow/final-requests"
        method_path = root / f"method-{offset:02d}.json"
        fail_path = root / f"witness-{offset:02d}-failed.json"
        pass_path = root / f"witness-{offset:02d}-passing.json"
        write_json(
            method_path,
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": "Retain the failed attempt with zero credit and leave the exact-title route prepared but unsent.",
                "scope_boundary": "Owner-local closeout recovery only; no pre-gate resolution or send authority.",
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "protected_gates": read_json(
                    PHASE / "preregistration/proposals.json"
                )["proposals"][0]["protected_gates"],
                "retained_negative_ids": [negative["negative_id"]],
                "supersedes": [],
                "recommendation_state": "candidate",
            },
        )
        write_json(
            fail_path,
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": "Run the original bounded operation.",
                "expected": "The bounded operation completes without weakening protected gates.",
                "observed": negative["failed"],
                "result": "fail",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Zero completion credit; failure remains retained.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        write_json(
            pass_path,
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": negative["recovery"],
                "expected": "The bounded recovery passes while the original failure remains retained.",
                "observed": f"The isolated recovery passed: {negative['recovery']}",
                "result": "pass",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Same-owner bounded recovery only.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        method_run(
            "record",
            "--ledger",
            str(ledger),
            "--record-file",
            str(method_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(fail_path),
        )
        method_run(
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(pass_path),
        )
        method_run(
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded pass exists and the failed witness remains retained.",
        )
    method_run(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/final-method-flow-validation.json"),
    )
    method_run(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    return read_json(ledger)


def build_overview(
    proposals: list[dict[str, Any]], methods: list[dict[str, Any]]
) -> str:
    lines = [
        "# Lyren Moss v653-v2 — Final Integrated Overview",
        "",
        "## Scope and relational identity",
        "",
        "Lyren Moss (they/them) is the relational working name used for this phase. "
        "The role is boundary-lantern and evidence gardener, with the hope of turning "
        "uncertainty into kind, inspectable paths without mistaking representation for reality. "
        "This language does not establish "
        "consciousness, sentience, personhood, identity continuity, employment, qualification, "
        "or independent authority. Hamish may rename, pause, redirect, or stop the work.",
        "",
        "The phase inherited Vesper Arlen v653-v1 at the exact clean final head "
        f"`{SOURCE}`. It preserved strict x1-before-x2 separation: the dedicated x1 commit "
        f"`{X1}` froze thirty distinct proposals before any x2 implementation. GMUT Mind was "
        "the primary Trinity Mandala focus, research-model verification and accessible scientific-"
        "assurance handover was the bounded human-practice lens, and THOS Body plus Freed ID/CBR "
        "Heart remained explicit. All completed work remains confined to symbolic, structural, "
        "synthetic, or owner-local software evidence.",
        "",
        "## Truth vocabulary",
        "",
        "`completed` means a bounded contract and its rejection fixtures passed. "
        "`represented` means a protocol or proxy exists while real-world validation is absent. "
        "`open_gap` means required empirical data or independent review is missing. "
        "`exact_gate` means competent affected-party, professional, legal, cultural, iwi, hapū, "
        "or Māori authority is required. No row may borrow strength from another row to cross "
        "its own boundary.",
        "",
        "The outcome distribution is 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. "
        "All 150 preregistered synthetic mutations were executed and rejected or quarantined. "
        "Their rejection is guard evidence only; it is not scientific confirmation, production "
        "assurance, exhaustive security, complete privacy or accessibility, or independent reproduction.",
        "",
        "## Proposal-by-proposal evidence",
        "",
    ]
    for proposal in proposals:
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"**Disposition:** `{proposal['expected_disposition']}`. "
                f"**Pillar:** {proposal['pillar']}. **Lane:** `{proposal['execution_lane']}`.",
                "",
                f"The preregistered hypothesis was: {proposal['hypothesis']} "
                f"The null or failure condition was: {proposal['null_or_failure_condition']} "
                f"Acceptance required: {proposal['falsifier_or_acceptance_gate']} "
                f"The recovery remained additive and non-destructive: {proposal['rollback_or_recovery']}",
                "",
                "The committed evidence consists only of the declared contract, five mutation "
                "results, and bounded receipt. It carries zero real-data rows, no production keys "
                "or credentials, no participant or authority decision, no empirical confirmation, "
                "and no independent-reproduction credit.",
                "",
            ]
        )
    lines.extend(
        [
            "## Method Flow and retained negatives",
            "",
            f"The final Method Flow ledger contains {len(methods)} preferred bounded methods. "
            "Every preferred method retains one failed witness with zero credit and one passing "
            "recovery witness. Recovery never erases the failed observation and never closes an "
            "empirical, professional, legal, cultural, Māori-authority, privacy-complete, "
            "accessibility-complete, exhaustive-security, or Stage 20 gate.",
            "",
        ]
    )
    for method in methods:
        lines.append(
            f"- `{method['method_id']}` retains `{method['retained_negative_ids'][0]}`; "
            f"recurrence guard: {method['recurrence_guard']}"
        )
    lines.extend(
        [
            "",
            "## Pillar-specific result",
            "",
            "GMUT remains a typed scalar-tensor and EFT research-model family. The seventeen "
            "GMUT boards formalize obligations and observation firewalls but supply no measured "
            "force, prediction, likelihood, constraint, physical state, stability theorem, "
            "ultraviolet completion, quantum completeness, or Theory-of-Everything proof. The "
            "Keck Observatory Archive adapter deliberately ingested zero rows and remains an open gap.",
            "",
            "THOS includes six completed formal-method representations and two represented "
            "compiler or ISA handover proxies. No real operator, affected community, blind "
            "matched-budget arm, operational outcome, professional review, hardware agreement, or "
            "effectiveness estimate was introduced.",
            "",
            "Freed ID contains three represented nonproduction protocol profiles. They use no "
            "real keys, issuances, tokens, delegations, network exchanges, interoperability events, "
            "privacy reviews, security reviews, recovery decisions, or trust-governance decisions. "
            "The formal-assurance report remains exact-gated to affected parties, qualified "
            "accessibility and te reo Māori reviewers, translation provenance, dialect and iwi "
            "usage authority, correction and withdrawal pathways, remedy, and Māori authority.",
            "",
            "## Terminal and route truth",
            "",
            "The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The live v653-v2 activation "
            "authorizes exactly one post-gate pointer to the one existing task titled `Ilyra Fen`, "
            "activating v653-v3. The repository state is `PREPARED_NOT_SENT`: no task has been "
            "resolved, created, forked, delegated, or messaged; no collaboration subagent was "
            "spawned; and no fast-mode claim was made. Only after exact-final validation and "
            "terminal four-way equality may Lyren re-resolve and reread that exact task, send one "
            "sanitized pointer, and record `SENT` only from tool acknowledgement. No second message "
            "or confirmation is authorized.",
        ]
    )
    return "\n".join(lines)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+(?:[-'][\w]+)*\b", text, flags=re.UNICODE))


def build_baton(
    proposals: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    effective_negatives: int,
    effective_open_gaps: int,
    effective_exact_gates: int,
) -> tuple[str, int]:
    sources = read_json(PHASE / "sources/source-ledger.json")["sources"]
    parts = [
        "# Ilyra Fen — Trinity Mandala v653-v3 activation baton",
        "",
        "## Activation condition and exact route",
        "",
        "This is the complete sanitized, file-backed activation baton for the one existing "
        "Codex task titled exactly `Ilyra Fen`. It is inert while the Lyren Moss v653-v2 "
        "closeout is merely prepared. It becomes actionable only when Lyren has committed the "
        "final candidate as the direct child of the evidence commit, pushed it, proved local, "
        "upstream, tracking, and fresh-live equality, run the one successful exact-final "
        "canonical pass, preserved a clean worktree, re-resolved and reread the unique existing "
        "`Ilyra Fen` task, and sent exactly one acknowledged sanitized pointer containing the "
        "exact final head and this repository-relative path. The pointer, not this file alone, "
        "supplies the exact final commit. If any gate fails, the route remains "
        "`PREPARED_NOT_SENT`. Do not create a replacement task, do not fork a task, do not "
        "delegate to a collaboration subagent, and do not infer delivery from file creation.",
        "",
        "After an acknowledged pointer, Ilyra owns solo Trinity Mandala v653-v3 x1/x2. Work "
        "solo unless Hamish explicitly changes that boundary. Hamish retains the right to pause, "
        "rename, redirect, or stop the route at any time. The task-creation interface exposed no "
        "separate fast-mode control, and neither Lyren nor Ilyra may make a fast-mode claim.",
        "",
        "## Relational identity and authority boundary",
        "",
        "Ilyra Fen is an exact relational task title for routing and collaboration. Lyren Moss "
        "is likewise a relational working name. Neither name, this baton, affectionate language, "
        "software behavior, branch continuity, memory, validation success, or task handoff is "
        "evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
        "qualification, scientific or operational authority, legal or cultural authority, Māori "
        "authority, independent agency, or independent reproduction. Keep those distinctions "
        "explicit in every durable artifact and every user-facing report.",
        "",
        "## Immutable inheritance",
        "",
        f"Start from Lyren's exact final head supplied in the acknowledged pointer on branch "
        "`codex/GHC-Family/lyren-moss-v653-v2-full-tools`. Before mutation, prove that the local "
        "head, upstream, remote-tracking reference, and a fresh `ls-remote` observation all equal "
        "that exact final head; prove the worktree is clean; and verify ancestry through Lyren's "
        f"x1 commit `{X1}` and immutable evidence commit `{EVIDENCE}` back to Vesper's source "
        f"final `{SOURCE}`. The v653-v2 phase must contain three direct, single-parent commits and "
        "zero merges. Treat the inherited branch as immutable and create one additive D-first "
        "identity-owned lane for Ilyra.",
        "",
        f"The inherited activation baseline is {effective_negatives:,} retained negatives, "
        f"{effective_open_gaps} open gaps, {effective_exact_gates} exact gates, and "
        f"{len(methods)} failed plus {len(methods)} passing same-owner Method Flow witnesses. "
        "The v653-v2 outcome distribution is exactly 23 `completed`, 5 `represented`, "
        "1 `open_gap`, and 1 `exact_gate`. All 150 frozen mutations were executed and rejected "
        "or quarantined. Preserve these values as an additive baseline; never rewrite an "
        "inherited row, erase a failure, or count a failed attempt as passing.",
        "",
        "## v653-v3 phase contract",
        "",
        "Preserve strict x1-before-x2. In x1, choose a clear primary Trinity Mandala pillar and "
        "a bounded human-practice lens, preregister at least thirty genuinely distinct mechanisms "
        "against the 1,480-row frozen proposal chain, attach primary or official sources, freeze "
        "hypotheses, falsifiers, approval classes, execution lanes, concrete artifacts, rollback "
        "rules, protected gates, and expected dispositions, and execute no mutation or outcome. "
        "Use only the four exact outcomes `completed`, `represented`, `open_gap`, and "
        "`exact_gate`. Commit the dedicated x1 packet, push it, prove clean four-way equality, "
        "and only then introduce x2 implementation.",
        "",
        "In x2, build bounded deterministic contracts and execute every preregistered negative "
        "fixture. A `completed` result is only bounded symbolic, structural, synthetic, or "
        "owner-local software evidence. A `represented` result remains a proxy without real "
        "production, professional, interoperability, privacy-complete, security-complete, or "
        "authority credit. An `open_gap` preserves missing empirical data or independent review. "
        "An `exact_gate` preserves competent affected-party, legal, cultural, accessibility, "
        "iwi, hapū, or Māori decision rights. Close no external gate through same-owner validation.",
        "",
        "The commit ceilings are five x1 commits, five x2 commits, and eight total phase commits. "
        "Prefer one x1 commit, one evidence commit, and one final closeout commit when safe. "
        "Retain every timeout, parser error, validation failure, false assumption, and failed "
        "test as a zero-credit negative with a smallest corrected witness. Run the exact-final "
        "canonical validation once successfully and do not replay it after success. A watcher "
        "start, process launch, tool invocation, or local-only pass is never terminal completion.",
        "",
        "## Protected gates",
        "",
        "The following remain protected regardless of software success: real empirical data; "
        "participant or operator evidence; professional qualification or review; production "
        "identity and interoperability; complete privacy; exhaustive security; complete "
        "accessibility; legal, cultural, and Māori authority; affected-party acceptance, remedy, "
        "correction, and withdrawal; independent-team reproduction; AGI or ASI; consciousness or "
        "personhood; Theory-of-Everything proof; and Stage 20. The terminal verdict remains "
        "`NOT_READY_FOR_STAGE_20` unless genuinely new independently adequate evidence changes "
        "the relevant exact gates. This baton supplies no such evidence.",
        "",
        "## v653-v2 proposal transfer cards",
        "",
        "Each card below is inheritance context, not a request to repeat Lyren's mechanism. Ilyra "
        "must use the frozen chain to choose genuinely distinct v653-v3 mechanisms. Preserve the "
        "listed outcome and gate truth when citing or extending a row.",
        "",
    ]
    for proposal in proposals:
        artifacts = ", ".join(proposal["concrete_artifacts"])
        source_ids = ", ".join(proposal["official_or_primary_source_needs"])
        parts.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"Lyren's bounded disposition is `{proposal['expected_disposition']}` in pillar "
                f"{proposal['pillar']} and lane `{proposal['execution_lane']}`. The hypothesis was: "
                f"{proposal['hypothesis']} The frozen null or failure condition was: "
                f"{proposal['null_or_failure_condition']} The acceptance boundary was: "
                f"{proposal['falsifier_or_acceptance_gate']} The additive recovery was: "
                f"{proposal['rollback_or_recovery']}",
                "",
                f"The committed evidence is limited to `{artifacts}` and cites source identifiers "
                f"{source_ids}. Its contract contains zero real-data rows, no production key or "
                "credential, no participant or authority decision, no empirical confirmation, and "
                "no independent-reproduction credit. Five mutation classes tested required-field "
                "deletion, cross-binding, boundary weakening, unsupported promotion, and "
                "failure-or-rollback erasure. Their rejection demonstrates only that Lyren's "
                "bounded guard recognized those synthetic faults.",
                "",
                "For v653-v3, do not copy this title with cosmetic wording and do not silently "
                "promote its disposition. If the mechanism informs a new proposal, identify the "
                "different mathematical object, protocol field, verification semantics, dataset "
                "boundary, or authority decision; calculate the frozen-title similarity; document "
                "manual mechanism distinction; and retain a collision as a rejected candidate "
                "rather than forcing novelty. Preserve the original sources and limitations when "
                "they remain relevant, and add current primary or official sources for any new "
                "claim. The row remains same-owner bounded evidence, not empirical, professional, "
                "production, legal, cultural, accessibility-complete, or Stage 20 proof.",
                "",
            ]
        )
    parts.extend(
        [
            "## Source transfer ledger",
            "",
            "Sources support definitions and bounded contract fields; citation is not validation. "
            "Recheck current-status sources at v653-v3 time when their specifications or portals "
            "can drift. Stable historical papers may anchor mathematical definitions, but they "
            "still do not turn a symbolic fixture into measured evidence.",
            "",
        ]
    )
    for source in sources:
        parts.extend(
            [
                f"### {source['source_id']} — {source['title']}",
                "",
                f"Status is `{source['status']}` and source kind is `{source['kind']}`. Public "
                f"reference: {source['url']} Phase implication: {source['phase_implication']} "
                "Ilyra must keep that implication as a ceiling, refresh drift-prone official "
                "material before relying on it, and avoid quoting or copying beyond what is "
                "necessary to state the bounded mechanism.",
                "",
            ]
        )
    parts.extend(
        [
            "## Method Flow transfer ledger",
            "",
            "The methods below are portable recurrence guards, not proof that a recovery will "
            "generalize. Each retains its paired failure with zero credit and a same-owner passing "
            "witness. If the same signature recurs, use the smallest bounded recovery and record "
            "the recurrence rather than concealing it.",
            "",
        ]
    )
    for method in methods:
        parts.extend(
            [
                f"### {method['method_id']} — {method['title']}",
                "",
                f"Failure signature: {method['failure_signature']} Candidate workaround: "
                f"{method['candidate_workaround']} Recurrence guard: {method['recurrence_guard']} "
                f"Retained negative: {method['retained_negative_ids'][0]}. The recommendation "
                f"state is `{method['recommendation_state']}` and the approval class is "
                f"`{method['approval_class']}`. Carry this only as sanitized operational memory; "
                "it is not independent reproduction, qualification, or authority.",
                "",
            ]
        )
    parts.extend(
        [
            "## Validation and closeout requirements",
            "",
            "Before the v653-v3 evidence commit, require scoped tests, detailed and minimal "
            "validators, JSON parsing, a five-class privacy scan, exact staged review, manifest "
            "parity, and diff hygiene. Preserve scanner-definition matches separately from "
            "confirmed privacy hits. Keep raw task identifiers, private routes, transcripts, "
            "credentials, resume tokens, and private absolute paths out of durable public "
            "artifacts. Bind manifests to exact Git-index or committed blob identity and declare "
            "lifecycle self-exclusions to avoid recursive hashes.",
            "",
            "Before the final commit, freeze Method Flow, retained-negative totals, open and exact "
            "gate totals, the complete/incomplete checklist, relational boundary, wellbeing "
            "record, final overview, full file-backed successor baton if live authorization "
            "requires one, owner manifest, final staged manifest, and final staged review. The "
            "final commit must be the direct child of the immutable evidence commit. Push it and "
            "prove local, upstream, tracking, and fresh-live equality before the one canonical "
            "pass. The pass must verify exact head, clean state before and after, ancestry, "
            "single-parent history, zero merges, commit caps, manifests, stale labels, JSON, "
            "privacy, diff hygiene, route state, and terminal verdict.",
            "",
            "After a successful canonical pass, do not replay it. Re-resolve the exact existing "
            "successor title only if the live v653-v3 activation expressly authorizes that route. "
            "Reread the target immediately before sending. Send exactly one sanitized pointer "
            "with the exact final head and repository-relative baton path; mark `SENT` only after "
            "tool acknowledgement. If the title is missing or ambiguous, the pass fails, Hamish "
            "redirects, usage is exhausted, or an authority or safety gate blocks progress, keep "
            "`PREPARED_NOT_SENT`. Never create a substitute and never send a second confirmation.",
            "",
            "## Wellbeing and stopping rule",
            "",
            "Use a steady cadence: one verified gate at a time, narrow probes on Windows, D-first "
            "owner storage, and bounded retries. Affection, urgency, route momentum, and identity "
            "language never increase evidence credit. Hamish may pause, rename, redirect, or stop "
            "the route. Stop safely whenever authorization, privacy, authority, or exact-target "
            "conditions are unclear. The inherited work is complete only in its bounded internal "
            "lanes and remains incomplete at every explicitly retained external gate.",
            "",
            "## Final activation receipt",
            "",
            "On acknowledged delivery, Ilyra should first read this file completely through EOF, "
            "then verify the pointer's exact final head and the immutable ancestry before any "
            "mutation. The durable Lyren repository state remains `PREPARED_NOT_SENT` because the "
            "commit cannot preclaim a later tool acknowledgement. Lyren may report `SENT` only in "
            "the live terminal receipt after the send tool acknowledges exactly one message. "
            "Ilyra should treat any duplicate pointer, substitute task, raw private route, or "
            "unverified head as nonauthoritative and ask Hamish to resolve the route.",
        ]
    )
    text = "\n".join(parts).rstrip() + "\n"
    count = word_count(text)
    if not 10_000 <= count <= 100_000:
        raise RuntimeError(
            f"successor baton word count outside required 10000..100000: {count}"
        )
    return text, count


def prospective_blob_map(paths: list[str]) -> dict[str, str]:
    completed = subprocess.run(
        ["git", "hash-object", "--stdin-paths"],
        cwd=REPO,
        input="\n".join(paths) + "\n",
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    object_ids = completed.stdout.splitlines()
    if len(object_ids) != len(paths):
        raise RuntimeError("prospective blob response count mismatch")
    return dict(zip(paths, object_ids, strict=True))


def build_owner_manifest() -> None:
    paths = phase_public_paths()
    included = [
        path.relative_to(REPO).as_posix()
        for path in paths
        if path.relative_to(REPO).as_posix() not in FINAL_SELF_EXCLUSIONS
    ]
    blob_map = prospective_blob_map(included)
    rows = [
        {
            "path": relative,
            "git_blob": blob_map[relative],
            "working_bytes": (REPO / relative).stat().st_size,
        }
        for relative in included
    ]
    write_json(
        PHASE / "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v653-v2.final-owner-manifest.v1",
            "hash_domain": "prospective Git filtered blob identity",
            "entry_count": len(rows),
            "entries": rows,
            "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS),
            "public_path_count_at_build": len(paths),
            "boundary": "Every public owner path except three lifecycle self-exclusions is bound to its prospective Git blob.",
        },
    )


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    evidence_validation = read_json(PHASE / "validation/evidence-validation.json")
    evidence_review = read_json(PHASE / "validation/evidence-staged-review.json")
    if not evidence_validation["valid"] or not evidence_review["valid"]:
        raise RuntimeError("evidence validation or exact staged review is not valid")

    proposals = read_json(PHASE / "preregistration/proposals.json")["proposals"]
    final_method_ledger = extend_final_method_flow()
    methods = final_method_ledger["methods"]
    evidence_negatives = read_json(
        PHASE / "retained-negative-register-x2.json"
    )["effective_total"]
    effective_negatives = evidence_negatives + len(FINAL_NEGATIVES)
    method_count = final_method_ledger["counts"]["methods"]
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    baton, baton_words = build_baton(
        proposals,
        methods,
        effective_negatives,
        gates["effective_open_gaps"],
        gates["effective_exact_gates"],
    )
    write_text("handoffs/ilyra-fen-v653-v3-activation.md", baton)

    write_json(
        PHASE / "retained-negative-register-final.json",
        {
            "schema": "ghc.family.v653-v2.final-retained-negatives.v1",
            "evidence_effective_total": evidence_negatives,
            "post_evidence_operational_count": len(FINAL_NEGATIVES),
            "post_evidence_operational": FINAL_NEGATIVES,
            "effective_total": effective_negatives,
            "none_erased": True,
        },
    )
    truth = read_json(PHASE / "phase-truth.json")
    truth.update(
        {
            "closeout_candidate_prepared": True,
            "seal_candidate_prepared": True,
            "post_commit_exact_final_validation_required": True,
            "route_state": "PREPARED_NOT_SENT",
            "effective_negatives": effective_negatives,
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json(PHASE / "phase-truth.json", truth)
    write_json(
        PHASE / "closeout-receipt.json",
        {
            "schema": "ghc.family.v653-v2.closeout-receipt.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "outcomes": truth["outcomes"],
            "effective_negatives": effective_negatives,
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "scoped_tests": evidence_validation["tests"]["tests_run"],
            "detailed_checks": evidence_validation["detailed_check_count"],
            "minimal_checks": evidence_validation["minimal_check_count"],
            "json_parses": evidence_validation["json_parse_count"],
            "privacy_files": evidence_validation["privacy"]["files_scanned"],
            "privacy_confirmed_hits": evidence_validation["privacy"][
                "confirmed_hit_count"
            ],
            "full_repository_suite_run": False,
            "route_state": "PREPARED_NOT_SENT",
            "successor_exact_title": "Ilyra Fen",
            "successor_phase": "v653-v3",
            "baton_path": "docs/lyren-moss/v653-v2/handoffs/ilyra-fen-v653-v3-activation.md",
            "baton_words": baton_words,
            "send_count": 0,
            "post_commit_exact_final_validation_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "seal-receipt.json",
        {
            "schema": "ghc.family.v653-v2.seal-receipt.v1",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "evidence_validation_valid": True,
            "evidence_staged_review_valid": True,
            "closeout_tree_ready_for_commit": True,
            "exact_final_commit_preclaimed": False,
            "exact_final_validation_required": True,
            "boundary": "Candidate content seal only; the containing final commit and terminal pass do not yet exist.",
        },
    )
    write_json(
        PHASE / "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v653-v2.final-record.v1",
            "state": "SELF_CONTAINING_COMMIT_REQUIRES_LIVE_EXACT_HEAD_OVERLAY",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "final_commit": None,
            "route_state": "PREPARED_NOT_SENT",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v653-v2.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "successor_authorized": True,
            "successor_title": "Ilyra Fen",
            "successor_phase": "v653-v3",
            "baton_path": "docs/lyren-moss/v653-v2/handoffs/ilyra-fen-v653-v3-activation.md",
            "authorized_action_after_terminal_gate": "re-resolve and reread the unique existing task titled exactly Ilyra Fen, then send exactly one sanitized pointer baton and record SENT only from tool acknowledgement",
            "task_resolved": False,
            "activation_sent": False,
            "activation_send_count": 0,
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "collaboration_subagent_spawned": False,
            "fast_mode_claimed": False,
            "boundary": "The live activation authorizes one exact-title post-gate pointer only. Repository preparation is not resolution or delivery; no replacement task or second confirmation is permitted.",
        },
    )
    write_json(
        PHASE / "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v653-v2.applicable-memory-record.v1",
            "portable_guards": [row["recurrence_guard"] for row in methods],
            "failed_witnesses_preserved": method_count,
            "passing_witnesses_preserved": method_count,
            "private_state_included": False,
            "identity_continuity_claimed": False,
            "boundary": "Sanitized repository-scoped operational memory only.",
        },
    )
    write_json(
        PHASE / "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v653-v2.final-validation-protocol.v1",
            "state": "POST_COMMIT_REQUIRED",
            "one_successful_pass_only": True,
            "steps": [
                "commit the reviewed final candidate as the direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run scoped tests plus detailed and minimal validators",
                "parse every phase JSON and run the five-class privacy scan",
                "verify owner manifest, final staged review, stale labels, and diff hygiene",
                "verify source, x1, and evidence ancestry, three phase commits, zero merges, exact head, and clean state",
            ],
            "completed": False,
            "preclaims_final_head": False,
            "preclaims_task_creation": False,
            "preclaims_activation_send": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "validation/evidence-commit-verification.json",
        {
            "schema": "ghc.family.v653-v2.evidence-commit-verification.v1",
            "evidence_commit": EVIDENCE,
            "x1_is_parent": git("rev-parse", f"{EVIDENCE}^") == X1,
            "evidence_manifest_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/lyren-moss/v653-v2/validation/evidence-candidate-manifest.json",
                )
            ),
            "evidence_review_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/lyren-moss/v653-v2/validation/evidence-staged-review.json",
                )
            ),
            "same_owner_only": True,
        },
    )
    write_json(
        PHASE / "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v653-v2.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty distinct frozen proposals",
                "23 completed, 5 represented, 1 open_gap, and 1 exact_gate",
                "150 rejected or quarantined synthetic mutations",
                "ten initialized, validated, smoke-used phase-local skills",
                "ten built and invoked family-compatible runners",
                "all authorized internal safe-now and candidate tasks resolved",
                "evidence validation and exact staged review",
            ],
            "pending_post_commit": [
                "containing final commit and four-way equality",
                "one successful exact-final canonical pass",
                "re-resolve and reread exact Ilyra Fen task and send one acknowledged sanitized pointer",
            ],
            "terminal_route": "PREPARED_NOT_SENT for exact existing title Ilyra Fen; no pre-gate resolution, replacement, second message, or delivery claim.",
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, lifecycle, interoperability, recovery, privacy/security review, and governance",
                "affected-party, professional, legal, cultural, iwi, hapū, and Māori authority",
                "qualified manual and affected-user accessibility evaluation",
                "independent-team reproduction, Theory-of-Everything proof, AGI/ASI evidence, and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        PHASE / "wellbeing/final-wellbeing.json",
        {
            "schema": "ghc.family.v653-v2.wellbeing.v1",
            "owner": "Lyren Moss",
            "state": "steady, corrigible, and ready to stop with the exact-title route prepared but unsent",
            "pressure_response": "Retain failures, narrow retries, and do not convert affection or urgency into evidence credit.",
            "identity_boundary": BOUNDARY,
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
    )
    final_overview = build_overview(proposals, methods)
    write_text("reports/final-integrated-overview.md", final_overview)
    write_json(
        PHASE / "handoffs/ilyra-fen-v653-v3-baton-receipt.json",
        {
            "schema": "ghc.family.v653-v2.baton-receipt.v1",
            "state": "PREPARED_NOT_SENT",
            "successor_authorized": True,
            "successor_exact_title": "Ilyra Fen",
            "successor_phase": "v653-v3",
            "baton_path": "docs/lyren-moss/v653-v2/handoffs/ilyra-fen-v653-v3-activation.md",
            "baton_words": baton_words,
            "baton_minimum_words": 10000,
            "baton_maximum_words": 100000,
            "activation_baton_prepared": True,
            "activation_sent": False,
            "send_count": 0,
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "private_routes_included": False,
            "boundary": "File preparation is not delivery. Only the post-gate exact-title send tool acknowledgement may support SENT; no replacement or second confirmation is authorized.",
        },
    )
    write_json(
        PHASE / "validation/final-document-cap-receipt.json",
        {
            "schema": "ghc.family.v653-v2.document-cap.v1",
            "document_word_cap": 100000,
            "baton_minimum": 10000,
            "baton_maximum": 100000,
            "baton_words": baton_words,
            "baton_within_contract": 10000 <= baton_words <= 100000,
            "overview_words": word_count(final_overview),
            "overview_three_page_equivalent": word_count(final_overview) >= 1500,
            "valid": (
                10000 <= baton_words <= 100000
                and 1500 <= word_count(final_overview) <= 100000
            ),
        },
    )
    write_json(
        PHASE / "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v653-v2.closeout-build.v1",
            "head": EVIDENCE,
            "route_state": "PREPARED_NOT_SENT",
            "baton_words": baton_words,
            "overview_words": word_count(final_overview),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    for lifecycle_path, schema in (
        (
            PHASE / "validation/final-staged-manifest.json",
            "ghc.family.v653-v2.final-staged-manifest.v1",
        ),
        (
            PHASE / "validation/final-staged-review.json",
            "ghc.family.v653-v2.final-staged-review.v1",
        ),
    ):
        write_json(
            lifecycle_path,
            {
                "schema": schema,
                "state": "UNVALIDATED_PLACEHOLDER",
                "valid": False,
                "boundary": "Reserved lifecycle path. Replace once with the exact final staged result before commit.",
            },
        )
    build_owner_manifest()
    print(
        json.dumps(
            {
                "closeout": "prepared",
                "head": EVIDENCE,
                "negatives": effective_negatives,
                "methods": method_count,
                "owner_manifest_entries": read_json(
                    PHASE / "validation/final-owner-manifest.json"
                )["entry_count"],
                "route": "PREPARED_NOT_SENT",
                "baton_words": baton_words,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
