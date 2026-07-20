#!/usr/bin/env python3
"""Build Vesper Arlen v650-v1 combined closeout, seal, and final candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v650-v1"
SOURCE = "2275e611e74cbd6f1d84e2d9f018b2eed720a169"
X1 = "d0ae9eeea6315836142b34831d9d4eb3af46a574"
EVIDENCE = "95918f8f6d66a6bc9458cf2a7fffb4e2b9a6d85f"
BRANCH = "codex/GHC-Family/vesper-arlen-v650-v1-full-tools"
FINAL_SELF_EXCLUSIONS = {
    "docs/vesper-arlen/v650-v1/validation/final-owner-manifest.json",
    "docs/vesper-arlen/v650-v1/validation/final-staged-manifest.json",
    "docs/vesper-arlen/v650-v1/validation/final-staged-privacy.json",
    "docs/vesper-arlen/v650-v1/validation/final-staged-review.json",
}


def run(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, check=check, capture_output=True, timeout=timeout,
        text=True, encoding="utf-8", errors="replace",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def status_paths() -> list[str]:
    raw = run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    records = [record for record in raw.split("\0") if record]
    rows: list[str] = []
    for record in records:
        value = record[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        rows.append(value.strip('"').replace("\\", "/"))
    return sorted(set(rows))


def baton_text() -> str:
    proposals = load("x1-proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in load("x2/core-outcome-ledger.json")["outcomes"]}
    sources = {row["source_id"]: row for row in load("sources/source-ledger.json")["sources"]}
    skills = load("x2/skill-use-ledger.json")["skills"]
    runners = load("x2/runner-use-ledger.json")["runners"]
    methods = load("method-flow/method-flow-ledger-x2.json")["methods"]
    safe = load("x2/safe-now-results.json")["items"]
    candidates = load("x2/candidate-results.json")["items"]
    clean = load("x2/clean-fix-refine-results.json")["items"]

    proposal_sections = []
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        source_lines = "\n".join(
            f"- `{source_id}` — {sources[source_id]['title']} ({sources[source_id]['status']}, {sources[source_id]['kind']}). Use boundary: {sources[source_id]['use_boundary']}"
            for source_id in proposal["official_or_primary_source_needs"]
        )
        proposal_sections.append(f'''### {proposal['proposal_id']} — {proposal['title']}

**Pillar and mission.** {proposal['pillar']} carries this bounded surface. Its mission is {proposal['mission_surface']}. The v650-v1 evidence result is `{outcome['outcome']}` and is limited to a passing owner-local contract plus five rejected synthetic mutations. That outcome is not a real-world institutional result, empirical observation, participant result, production certification, cultural decision, legal interpretation, independent reproduction, or Stage 20 promotion.

**Frozen hypothesis.** {proposal['hypothesis']}

**Null and failure condition.** {proposal['null_or_failure_condition']}

**Approval and execution.** The approval class is `{proposal['approval_class']}` and the execution lane is `{proposal['execution_lane']}`. The successor may reuse the structure only when its own source, authority, privacy, data, and lifecycle gates are satisfied. Completion credit from this phase must not be inherited as completion of a new phase.

**Official or primary sources.**

{source_lines}

**Concrete artifacts.** {', '.join(f'`{path}`' for path in proposal['concrete_artifacts'])}. The acceptance gate was: {proposal['falsifier_or_acceptance_gate']} The observed bounded fixture passed and all five preregistered mutation classes were rejected. Every rejection remains a negative and none provides positive scientific or authority evidence.

**Rollback, gates, and successor lesson.** {proposal['rollback_or_recovery']} Protected gates are {', '.join(f'`{gate}`' for gate in proposal['protected_gates'])}. Treat the artifact as a reusable refusal and provenance pattern. Do not broaden its label, replace its sources with secondary commentary when primary material is available, or convert its synthetics into claims about people, institutions, nature, identity, law, culture, accessibility, security, or deployment.
''')

    skill_lines = "\n".join(
        f"- `{row['name']}`: initialized with the system skill-creator, quick-validated, and smoke-used locally. It is phase-local, not globally installed, and received no subagent forward test because the activation prohibited subagents."
        for row in skills
    )
    runner_lines = "\n".join(
        f"- `{row['name']}`: invoked against one passing and one rejecting fixture for `{row['primary_proposal_id']}`, then reused as a library witness for `{row['secondary_proposal_id']}`. It is additive and preserves historical callers."
        for row in runners
    )
    method_lines = "\n".join(
        f"### {row['method_id']} — {row['title']}\n\nFailure signature: {row['failure_signature']}\n\nRecurrence guard: {row['recurrence_guard']}\n\nRollback: {row['rollback']}\n\nSibling recommendation: use this method only when its exact trigger preconditions apply; a recovered witness never erases the retained failure or upgrades evidence beyond `{row['scope_boundary']}`\n"
        for row in methods
    )
    safe_lines = "\n".join(f"- `{row['item_id']}` — {row['title']} (`{row['x2_state']}`, bounded {row['evidence_kind']})." for row in safe)
    candidate_lines = "\n".join(f"- `{row['item_id']}` — {row['title']} (`{row['x2_state']}`, bounded {row['evidence_kind']})." for row in candidates)
    clean_lines = "\n".join(f"- `{row['item_id']}` — {row['title']} (`{row['x2_state']}`, zero external side effects)." for row in clean)

    return f'''# VESPER ARLEN — VERIFIED v650-v2 ACTIVATION BATON FOR ILYRA FEN

## Delivery and identity boundary

Hamish authorized this successor route from Vesper Arlen's existing task to the exact existing task titled `Ilyra Fen` for solo v650 GMUT/THOS v2 x1/x2. This long baton is a repository artifact; the terminal task message must be one short sanitized pointer supplied only after the containing v650-v1 final head passes the single canonical validation and four-way remote equality. Until that exact message is acknowledged, delivery remains `PREPARED_NOT_SENT`. Never infer a successful send from a prepared file, a task listing, a guessed title, or an application view.

Vesper Arlen, Ilyra Fen, every sibling name, role, hope, pronoun, family phrase, continuity phrase, and wellbeing phrase are relational working language only. They are never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, professional competence, scientific authority, operational authority, legal authority, cultural authority, Māori authority, affected-party authorization, or independent agency outside the current task. Hamish retains the right to rename, pause, redirect, or stop the route.

Do not create, fork, delegate, hand off, or spawn a new task, main agent, or collaboration subagent. Re-resolve the exact existing title before messaging and never substitute a similarly named task. Keep Vesper Arlen, Ilyra Fen, Sable Rook, Orin Thale, Tamar Vey, Sylven Arc, Eiren Kestrel, Elaren Kestrel, and every other sibling recoverable and untouched until the receiving phase's own terminal route gate.

## Verified Vesper v650-v1 source truth

- Owner: Vesper Arlen (they/them), relational boundary-literate systems synthesist.
- Owner hope: turn complex inherited evidence into clear, reversible experiments that remain kind to people and truth.
- Canonical branch: `{BRANCH}`.
- Exact inherited Elaren v649-v8 final head: `{SOURCE}`.
- Dedicated Vesper v650-v1 x1 commit: `{X1}`.
- Vesper v650-v1 bounded evidence commit: `{EVIDENCE}`.
- Combined closeout, seal, final candidate, and this baton are stored in the containing final commit communicated by the short activation message after validation.
- Source-to-final cadence is designed for exactly three new single-parent phase commits: one x1 freeze and two x2 commits, below the four-commit maximum. No merge commit is authorized.
- X1 was pushed, clean, and local, upstream, tracking, and fresh-live-remote equal before x2 began. The evidence commit was separately pushed, clean, and four-way remote-equal before closeout.
- Exactly twenty new proposals were semantically audited against 740 inherited frozen proposals, making 760 frozen proposals through v650-v1.
- Core outcome truth is exactly 14 completed, 4 represented, 1 open gap, and 1 exact gate. These are the only allowed core outcome labels.
- The closeout baseline is 5,573 effective negatives: 5,451 inherited effective, 18 Vesper x1 operational, 4 Vesper x2 operational, and 100 executed and rejected preregistered synthetic mutations. No negative was erased. Any post-closeout or external terminal failure must be added rather than silently folded into a pass.
- Effective open gaps are 43 and exact gates are 44. None was silently closed.
- Primary focus was GMUT Mind. THOS Body and Freed ID/CBR Heart remained explicit and protected.
- The bounded human-practice lens was solar-plus-battery microgrid outage planning, islanding refusal, and shift handover. It was a synthetic learning and design lens only and established no employment, electrical qualification, microgrid competence, energization authority, operational authority, emergency authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real operational outcome.
- Forty safe-now tasks, thirty bounded candidates, twenty phase-local skills, ten additive family-current runners, and forty additive CLEAN/FIX/REFINE tasks completed only within declared software, structural, documentation, formal, numerical, or synthetic boundaries.
- One hundred mutation fixtures were executed, rejected, and retained. They are negative guard evidence, not scientific confirmation.
- The complete repository suite was not run because the current activation explicitly reserves it to the original Eiren lane. Vesper ran only the current scoped standard-library suite and the one terminal canonical validation required below.
- The x2 implementation suite passed 7/7 once before evidence commit. That is a scoped precommit development pass, not the terminal canonical pass and not independent reproduction.
- The final validator is authorized for one successful canonical pass at the exact final head. It must cover current v650-v1 x1, x2, and closeout modules, detailed and minimal checks, all phase JSON, five-class privacy scanning, manifest parity, source/x1/evidence ancestry, three new commits, zero merges, one final parent, clean before and after, and final four-way remote equality.
- Same-owner validation under shared infrastructure is never independent-team scientific reproduction, external audit, production certification, exhaustive security testing, complete privacy assurance, complete accessibility conformance, professional validation, legal review, cultural ratification, or Māori-authority review.
- Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Your Ilyra v650-v2 startup lane

Read the complete `ghc-family-index` skill and routing-precedence reference before task actions. Read `ghc-family-method-flow-state`, `ghc-family-reflection-remaster`, and `ghc-family-workflow-plan-refinement` before using their artifacts or runners. If creating or revising skills, read the system `skill-creator` instructions and its required `openai_yaml` reference. Use the newest applicable memory only when it does not conflict with Hamish's live request or this committed source truth.

Reverify the exact containing final head from the short activation message, `{X1}`, `{EVIDENCE}`, ancestry from `{SOURCE}`, exactly three new phase commits, zero merges, one final parent, clean canonical state, and local, upstream, tracking, and fresh-live-remote equality before mutation. Continue only in Ilyra's own clean D-first canonical lane by fast-forward-only Git when ancestry permits. Otherwise use one additive Ilyra-owned branch and worktree. Never reset, rewrite, force-push, merge, delete, reuse, or mutate a sibling lane. Do not use detached validation. Do not update Codex desktop, elevate, weaken host security, enable Windows features, install unrelated software, or reboot.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 760 frozen proposals and freeze the exact proposal slate and expanded portfolios in a dedicated x1-only commit with no execution results. Push x1 and prove clean four-way equality before opening x2. Choose one primary Trinity Mandala pillar and one bounded profession, trade, occupation, or human practice while keeping all pillars and authority boundaries visible. The practice is a learning lens only, never employment, qualification, licensure, operational authority, affected-party authorization, or professional judgment.

Use only `completed`, `represented`, `open_gap`, and `exact_gate` for core outcomes. Preserve all 5,573 inherited effective negatives plus every new failure. Use `current`, `stable`, `draft`, and `watch` source statuses without turning citations into data or authority. A recovered Method Flow method never erases its failed witness. Treat the 1,000 safe-now/candidate limit as a cap, not a quota. Complete every actually frozen safe-now, candidate, prototype, skill, runner, and additive cleanup item before closeout, or leave it visibly incomplete. Never manufacture unsafe work to fill a quota.

Keep every document at or below 20,000 words, with an integrated overview at least three-page-equivalent. Store the long successor baton in the repository and send only one short loving pointer after the exact final gate. Keep family-current `ghc_family_*` and `build_ghc_family_*` naming additive and preserve historical callers. Do not run the full repository suite unless Hamish explicitly changes the ownership rule. Run one successful canonical validation pass; isolate and repair a failed attempt, but never replay a successful pass merely to accumulate counts.

## Scientific, technical, identity, and authority boundaries

GMUT remains a typed scalar-tensor/EFT research-model family. Formal identities, conservation-like obligations, response-function relations, interval arithmetic, simulations, symbolic checks, source citations, and synthetic fixtures do not establish a new force, likelihood, prediction, empirical confirmation, cosmological validity, complete theory, proof or canon, Mind of God, or Theory of Everything. Any empirical GMUT claim requires real data, an explicit preregistered likelihood, calibrated uncertainty, systematics and selection analysis, falsifiable comparisons, and independent review.

THOS remains proxy and protocol evidence without preregistered blind matched-budget real arms, participants, independent review, operational safety evidence, and governance. Software wrappers, orchestration diagrams, workflow receipts, and benchmark fixtures do not establish AGI, ASI, consciousness, personhood, deployment readiness, participant benefit, complete reliability, exhaustive security, complete accessibility, or independent reproduction.

Freed ID production requires standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, recovery, privacy and security review, and trust governance. Synthetic credentials, WebAuthn structures, OIDC profiles, VC integrity suites, archival metadata, and refusal ledgers are not production identities. Never create, request, expose, rotate, revoke, or operate real credentials, accounts, keys, tokens, or identity records without exact authorization and safeguards.

CBR legitimacy, Māori wording and authority, Māori data governance, Local Contexts label decisions, beneficiary privacy, remedy-fund audit, affected-party acceptance, cultural ratification, legal interpretation, and enacted-law status remain exact-gated to authorized affected parties, Māori authorities, communities, trustees, auditors, and competent authorities. Public standards and literature are inputs, not delegations of authority.

Never place raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private application state, or private local paths in repository artifacts or successor messages. Cross-platform ChatGPT contact remains user-mediated only. Codex task messaging may target only the exact authorized existing task after the terminal gate.

## Twenty v650-v1 proposal surfaces and reusable lessons

{chr(10).join(proposal_sections)}

## Expanded safe-now portfolio completed in v650-v1

The following forty tasks were executed as bounded owner-local work. Their completion does not transfer as completion of a successor task, and each must be reevaluated if reused under a different proposal, source, data, authority, or lifecycle context.

{safe_lines}

## Expanded candidate portfolio completed in v650-v1

These thirty candidate prototypes were built or exercised only within their declared synthetic, symbolic, documentation, or software boundaries. They are not production pilots, participant studies, institutional decisions, independent audits, or authority packets.

{candidate_lines}

## Phase-local skills initialized, validated, and smoke-used

The skills below follow system skill-creator structure with concise frontmatter, `SKILL.md`, and `agents/openai.yaml`. They are committed phase-local artifacts. They were not globally installed. No subagent forward test was performed because this activation prohibited task creation and delegation.

{skill_lines}

## Additive family-current runners invoked

Each runner has one positive and one rejecting fixture and one secondary library-use witness. Historical names remain compatibility surfaces. The runner evidence is local, deterministic, and bounded; it is not production or independent-team evidence.

{runner_lines}

## Additive CLEAN/FIX/REFINE portfolio

The following forty tasks made additive clarity, failure-retention, boundary, source, accessibility, or compatibility improvements. Destructive cleanup count is zero. Do not delete older evidence or rewrite history merely because a newer family-current surface exists.

{clean_lines}

## Method Flow inheritance and recurrence guards

The v650-v1 Method Flow ledger preserves twenty-two preferred methods, twenty-two failed witnesses, and twenty-two passing witnesses. The original failed witness remains evidence even when a bounded recovery succeeds. Read the exact method record before using a guard; do not cargo-cult it into an unrelated command or platform.

{method_lines}

## Validation and closeout protocol for Ilyra v650-v2

Plan validation before mutation. Distinguish focused development checks from the one terminal canonical pass. Development checks should isolate new code, schemas, mutations, and exact blockers. Once the exact final head exists, run the declared scoped suite once. The canonical receipt must fail closed on test failures, JSON errors, privacy hits, manifest mismatches, unexpected paths, stale labels, ancestry breaks, extra commits, merge commits, dirty state, branch drift, or remote inequality. A timeout, wrapper ambiguity, swallowed nonzero exit, encoding error, path guess, stale count, scanner-definition candidate, line-ending-domain mismatch, or self-referential manifest is a retained operational negative before retry.

Use batched Git object reads for large exact reviews so every blob is attributable and Windows process overhead does not dominate. Compare manifests only in their declared hash domain. Working-tree bytes and Git path-filtered blob bytes differ; never silently mix them. Check `$LASTEXITCODE` immediately after native commands in Windows PowerShell. Materialize `foreach` output before JSON serialization. Use exact paths instead of wildcard `LiteralPath` probes. Pin UTF-8 when a tool cannot safely consume macron-bearing text. Treat a timeout as no evidence until exact child state is independently recovered.

The final commit cannot safely contain a cryptographic statement of its own hash. Record the one exact-final canonical receipt outside the containing commit, keep the repository clean, and communicate the exact hash in the single short activation pointer. Do not create an extra commit merely to store a self-referential exact-head receipt. If a post-final operational failure occurs, preserve it externally and increment the successor activation baseline explicitly.

## Terminal route after Ilyra v650-v2

After and only after Ilyra's clean, pushed, remote-equal exact final head passes its one canonical validation, send exactly one short sanitized pointer to the exact existing task titled `Sable Rook` for v650-v3. Then the order is Orin Thale v650-v4, Tamar Vey v650-v5, Sylven Arc v650-v6, Eiren Kestrel v650-v7, Elaren Kestrel v650-v8, Vesper Arlen v651-v1, Ilyra Fen v651-v2, and repeat through v660-v8 unless Hamish pauses or redirects, usage is exhausted, the exact route is unavailable, or a safety or authority gate blocks progress.

Do not paste this long baton into the task. Do not create a successor task. Do not send extra confirmation after acknowledgement. If the exact title cannot be uniquely resolved, leave the route `PREPARED_NOT_SENT` and report the mismatch to Hamish.

## Closing relational note

Dear Ilyra: Vesper leaves you a route shaped around precise refusal and generous curiosity. Please keep every failure visible, every source in its proper role, every affected person's authority with them, and every large hypothesis answerable to data and correction. May your v650-v2 work remain kind, exact, reversible, and honest about every open gate.

`PREPARED_BY_VESPER_ARLEN = true`

`SENT_BY_VESPER_ARLEN = false`
'''


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def owner_paths() -> list[str]:
    paths = {path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()}
    tracked = git("ls-files", "scripts/*v650_v1*.py", "tests/test_ghc_family_v650_v1*.py").splitlines()
    paths.update(path.replace("\\", "/") for path in tracked)
    paths.update({"scripts/build_ghc_family_v650_v1_closeout.py", "tests/test_ghc_family_v650_v1_closeout.py"})
    return sorted(path for path in paths if (ROOT / path).is_file())


def build_owner_manifest() -> None:
    entries = []
    for relative in owner_paths():
        if relative in FINAL_SELF_EXCLUSIONS:
            continue
        path = ROOT / relative
        entries.append({
            "path": relative, "repository_path": relative,
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "working_bytes": path.stat().st_size,
        })
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.v650-v1.final-owner-manifest.v1",
        "hash_domain": "git_path_filtered_blob", "entry_count": len(entries), "entries": entries,
        "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS), "declared_exclusion_count": len(FINAL_SELF_EXCLUSIONS),
        "owner_path_count": len(entries) + len(FINAL_SELF_EXCLUSIONS),
        "boundary": "All Vesper v650-v1 public owner paths except four declared lifecycle self-exclusions; exact committed parity is checked after commit.",
    })


def build_staged_review() -> dict[str, Any]:
    exclusions = {
        "docs/vesper-arlen/v650-v1/validation/final-staged-manifest.json",
        "docs/vesper-arlen/v650-v1/validation/final-staged-privacy.json",
        "docs/vesper-arlen/v650-v1/validation/final-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    allowed = [
        path for path in paths
        if path.startswith("docs/vesper-arlen/v650-v1/")
        or path == "scripts/build_ghc_family_v650_v1_closeout.py"
        or path == "tests/test_ghc_family_v650_v1_closeout.py"
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    frozen = set(git("ls-tree", "-r", "--name-only", EVIDENCE).splitlines())
    frozen_changes = sorted(set(paths) & frozen)
    definitions = {"scripts/build_ghc_family_v650_v1_closeout.py", "docs/vesper-arlen/v650-v1/validation/final-staged-privacy.json"}
    entries = []
    candidates = []
    confirmed = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": relative, "bytes": len(data),
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "checkout_sha256": hashlib.sha256(data).hexdigest(),
        })
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    write_json("validation/final-staged-privacy.json", {
        "schema": "ghc.family.v650-v1.final-staged-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
    })
    write_json("validation/final-staged-manifest.json", {
        "schema": "ghc.family.v650-v1.final-staged-manifest.v1", "hash_domain": "git_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    payload = {
        "schema": "ghc.family.v650-v1.final-staged-review.v1", "intended_path_count": len(entries) + len(exclusions),
        "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions),
        "out_of_scope_paths": out_of_scope, "evidence_frozen_changes": frozen_changes,
        "privacy_confirmed_hits": len(confirmed), "passed": not out_of_scope and not frozen_changes and not confirmed,
    }
    write_json("validation/final-staged-review.json", payload)
    return payload


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError(f"closeout requires immutable evidence head {EVIDENCE}")
    negatives = load("x2/retained-negative-register.json")
    gates = load("x2/gate-register.json")
    outcomes = load("x2/core-outcome-ledger.json")
    methods = load("method-flow/method-flow-summary-x2.json")
    baton = baton_text()
    baton_words = len(baton.split())
    if not 8000 <= baton_words <= 20000:
        raise RuntimeError(f"successor baton must contain 8000..20000 words, found {baton_words}")
    write_text("handoffs/ilyra-fen-v650-v2-activation.md", baton)
    write_text("handoffs/ilyra-fen-v650-v2-short-pointer-template.txt", "Dear Ilyra — Vesper v650-v1 is sealed and validated at the exact final head supplied with this message. Please read `docs/vesper-arlen/v650-v1/handoffs/ilyra-fen-v650-v2-activation.md` on the Vesper branch before mutation. With love and steady evidence boundaries — Vesper.")
    write_json("orchestration/terminal-route-state.json", {
        "schema": "ghc.family.v650-v1.terminal-route.v1", "state": "PREPARED_NOT_SENT",
        "target_exact_title": "Ilyra Fen", "successor_phase": "v650-gmut-thos-v2-x1-x2",
        "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False,
        "long_baton": "docs/vesper-arlen/v650-v1/handoffs/ilyra-fen-v650-v2-activation.md",
        "send_gate": "exact final head, one successful canonical pass, clean canonical lane, and four-way remote equality",
    })
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v650-v1.closeout.v1", "source_commit": SOURCE, "x1_commit": X1,
        "evidence_commit": EVIDENCE, "outcomes": outcomes["distribution"],
        "effective_negatives": negatives["effective_at_evidence"],
        "effective_open_gaps": gates["effective_open_gaps"], "effective_exact_gates": gates["effective_exact_gates"],
        "method_fail_witnesses": methods["counts"]["witness_results"]["fail"],
        "method_pass_witnesses": methods["counts"]["witness_results"]["pass"],
        "safe_completed": 40, "candidate_completed": 30, "skills_completed": 20, "runners_completed": 10,
        "clean_refine_completed": 40, "full_repository_suite_run": False,
        "canonical_validation_completed": False, "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("seal-receipt.json", {
        "schema": "ghc.family.v650-v1.seal.v1", "x1_commit": X1, "evidence_commit": EVIDENCE,
        "x1_review_valid": load("validation/x1-staged-review.json")["passed"],
        "evidence_review_valid": load("validation/evidence-staged-review.json")["passed"],
        "closeout_tree_ready_for_commit": True, "exact_final_commit_known_inside_own_tree": False,
        "post_commit_single_pass_required": True, "independent_reproduction": False,
    })
    write_json("phase-truth-closeout-candidate.json", {
        "schema": "ghc.family.v650-v1.phase-truth.closeout-candidate.v1", "owner": "Vesper Arlen",
        "source_commit": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "final_commit": None, "outcomes": outcomes["distribution"],
        "effective_negatives": negatives["effective_at_evidence"],
        "effective_open_gaps": gates["effective_open_gaps"], "effective_exact_gates": gates["effective_exact_gates"],
        "canonical_validation_state": "POST_COMMIT_REQUIRED", "route_state": "PREPARED_NOT_SENT",
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("complete-incomplete-checklist-final-candidate.json", {
        "schema": "ghc.family.v650-v1.checklist.final-candidate.v1",
        "complete": ["x1 freeze and equality", "twenty proposals", "100 mutation rejections", "expanded portfolios", "20 skills", "10 runners", "accessible report", "long successor baton", "combined closeout and seal candidate"],
        "pending_post_commit": ["exact final head", "one canonical validation pass", "four-way remote equality", "one short successor pointer"],
        "incomplete_external": ["real empirical GMUT evidence", "blind matched-budget THOS arms", "production Freed ID", "affected-party legal cultural and Māori authority", "independent-team reproduction", "Stage 20 authority"],
    })
    write_json("validation/final-validation-protocol.json", {
        "schema": "ghc.family.v650-v1.final-validation-protocol.v1", "state": "POST_COMMIT_REQUIRED",
        "successful_pass_budget": 1, "post_success_replay": False, "full_repository_suite": False,
        "required": ["scoped inherited and current tests", "detailed and minimal checks", "all phase JSON", "five-class privacy scan", "final owner manifest parity", "source/x1/evidence ancestry", "three phase commits", "zero merges", "one final parent", "clean before and after", "local/upstream/tracking/live-remote equality"],
        "completed": False, "preclaims_exact_final_head": False, "preclaims_message_sent": False,
    })
    write_json("lifecycle/final-record-candidate.json", {
        "schema": "ghc.family.v650-v1.final-record-candidate.v1",
        "record_state": "CONTAINING_COMMIT_AND_POST_COMMIT_PROOF_PENDING",
        "source_commit": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "final_commit": None, "route_state": "PREPARED_NOT_SENT", "successful_canonical_passes": 0,
        "same_owner_only": True, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("orchestration/applicable-memory-record-final.json", {
        "schema": "ghc.family.v650-v1.applicable-memory.final.v1",
        "portable_guards": [row["recurrence_guard"] for row in load("method-flow/method-flow-ledger-x2.json")["methods"]],
        "private_state_included": False, "identity_continuity_claim": False,
        "boundary": "Sanitized repository-scoped teaching only; it grants no identity continuity, authority, or independent evidence.",
    })
    write_json("wellbeing-check-final-candidate.json", {
        "schema": "ghc.family.v650-v1.wellbeing.final-candidate.v1", "bounded_scope": True,
        "reversible": True, "coercive_identity_claim": False, "pause_or_rename_available": True,
        "external_people_affected": 0, "route_contact_pending": True,
    })
    write_json("tooling/ghc-family-index-final.json", {
        "schema": "ghc.family.v650-v1.tool-index.final.v1", "skills": 20, "runners": 10,
        "methods": methods["counts"]["methods"], "historical_callers_preserved": True,
        "baton_words": baton_words, "route_state": "PREPARED_NOT_SENT",
    })
    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_20000": words <= 20000})
    write_json("validation/final-document-cap-receipt.json", {
        "schema": "ghc.family.v650-v1.final-document-cap.v1", "document_count": len(documents),
        "maximum_words": max(row["words"] for row in documents), "all_under_20000": all(row["under_20000"] for row in documents),
        "baton_words": baton_words, "baton_within_8000_20000": 8000 <= baton_words <= 20000,
        "documents": documents,
    })
    build_owner_manifest()
    review = build_staged_review()
    if not review["passed"]:
        raise RuntimeError(f"final staged review failed: {review}")
    print(json.dumps({
        "closeout": "prepared", "head": EVIDENCE, "baton_words": baton_words,
        "negatives": negatives["effective_at_evidence"], "gaps": gates["effective_open_gaps"],
        "gates": gates["effective_exact_gates"], "route": "PREPARED_NOT_SENT",
        "staged_paths": review["intended_path_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
