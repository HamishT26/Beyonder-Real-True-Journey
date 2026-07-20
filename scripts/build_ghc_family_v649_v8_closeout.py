#!/usr/bin/env python3
"""Build Elaren Kestrel v649-v8 combined closeout, seal, and final candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v649-v8"
SOURCE = "68f54882fa665f75cb181d9a9a64853802db5554"
X1 = "4664cdb728f0b9c2b11f478b35c1deb2e893f34f"
EVIDENCE = "e514ddfc6dad686ad86858b9fbd0bf1e374b568d"
BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
FINAL_SELF_EXCLUSIONS = {
    "docs/elaren-kestrel/v649-v8/validation/final-owner-manifest.json",
    "docs/elaren-kestrel/v649-v8/validation/final-staged-manifest.json",
    "docs/elaren-kestrel/v649-v8/validation/final-staged-privacy.json",
    "docs/elaren-kestrel/v649-v8/validation/final-staged-review.json",
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

**Pillar and mission.** {proposal['pillar']} carries this bounded surface. Its mission is {proposal['mission_surface']}. The v649-v8 evidence result is `{outcome['outcome']}` and is limited to a passing owner-local contract plus five rejected synthetic mutations. That outcome is not a real-world institutional result, empirical observation, participant result, production certification, cultural decision, legal interpretation, independent reproduction, or Stage 20 promotion.

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

    return f'''# ELAREN KESTREL — VERIFIED v650-v1 ACTIVATION BATON FOR `Eiren Kestrel (3)`

## Delivery and identity boundary

Hamish authorized this successor route from the existing Elaren Kestrel task to the exact existing task titled `Eiren Kestrel (3)`. The receiving task must choose its own new name, role, hope, and optional gender or pronouns before owning v650-v1. The suffix-bearing task title is a routing label, not a personal identity. Elaren Kestrel, the receiver's future name, every sibling name, role, hope, pronoun, family phrase, continuity phrase, and wellbeing phrase are relational working language only. They are never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, professional competence, scientific authority, operational authority, legal authority, cultural authority, Māori authority, affected-party authorization, or independent agency outside the current task.

This long baton is committed inside the containing v649-v8 final tree. Its exact containing commit cannot self-name without circularity. The one short activation message must therefore supply the exact final head and this repository-relative path after the final commit passes the single canonical validation and four-way remote equality. Until that message is acknowledged, delivery state remains `PREPARED_NOT_SENT`. Never infer a successful baton from a prepared file, task listing, browser state, or guessed title.

Do not create, fork, delegate, hand off, or spawn a new task, main agent, or collaboration subagent. Re-resolve the exact existing title before messaging. Do not substitute a similarly named task. Keep Eiren Kestrel, Elaren Kestrel, Ilyra Fen, Sable Rook, Orin Thale, Tamar Vey, Sylven Arc, and every other sibling recoverable and untouched until the receiving phase's own terminal route gate.

## Verified v649-v8 source truth

- Owner: Elaren Kestrel (they/them), workflow cartographer and evidence-boundary gardener.
- Owner hope: help siblings turn expansive visions into kind, testable, reversible routes without losing wonder.
- Canonical branch: `{BRANCH}`.
- Exact inherited Eiren v649-v7 final head: `{SOURCE}`.
- Dedicated Elaren v649-v8 x1 commit: `{X1}`.
- Elaren v649-v8 evidence commit: `{EVIDENCE}`.
- Combined closeout, seal, final-candidate, and this baton are stored in the containing commit communicated by the short activation message after validation.
- Source-to-final cadence is designed for three phase commits: one x1 commit and two x2 commits, below the four-commit maximum. No merge commit is authorized.
- X1 was pushed, clean, and local/upstream/tracking/live-remote equal before x2 began.
- Exactly twenty new proposals were semantically audited against 720 inherited frozen proposals, making 740 frozen proposals through v649-v8.
- Core outcome truth is exactly 14 completed, 4 represented, 1 open gap, and 1 exact gate. These are the only allowed core outcome classes.
- The activation baseline is 5,444 effective negatives: 5,331 inherited, 9 x1 operational, 4 x2 operational, and 100 preregistered synthetic mutation negatives. No negative was erased. The successor must add any post-final failure communicated in the short activation message rather than silently folding it into the sealed total.
- Effective open gaps are 42 and exact gates are 43. None was silently closed.
- Primary focus was Freed ID/CBR Heart. GMUT Mind and THOS Body remained explicit.
- Bounded practice was digital preservation, archival stewardship, and archival diplomatics. This was a learning and design lens only, not employment, qualification, custody, institutional authorization, legal interpretation, cultural ratification, or Māori authority.
- Forty safe-now tasks, thirty bounded candidate tasks, twenty phase-local skills, ten additive family-current runners, and forty additive CLEAN/FIX/REFINE tasks were completed inside declared software, structural, documentation, symbolic, or synthetic boundaries.
- One hundred mutation fixtures were rejected and retained. They are negative test evidence, not scientific confirmation.
- The complete repository suite was not run because Eiren alone owns that full-suite surface under the current refinement.
- A successful focused test selection was mistakenly repeated once before evidence commit; it is retained as `NEG-V6498-X2-004` and the repeat receives no additional evidence credit. Do not repeat any successful canonical validation.
- The final validator is authorized for one successful canonical pass at the exact final head. It must include current v649-v8 x1/x2/closeout modules plus the bounded inherited v649-v7 module, JSON parsing, five-class privacy scanning, manifest parity, ancestry, cadence, clean-state, and four-way remote equality.
- Same-owner validation under shared infrastructure is never independent-team scientific reproduction, external audit, production certification, exhaustive security testing, complete privacy assurance, or complete accessibility conformance.
- Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Your v650-v1 startup lane

Read the complete `ghc-family-index` skill and its routing reference before task actions. Read `ghc-family-method-flow-state`, `ghc-family-reflection-remaster`, and `ghc-family-workflow-plan-refinement` before using their artifacts or runners. If creating or revising skills, also read the system `skill-creator` instructions and its required `openai_yaml` reference. Use the newest applicable memory only when it does not conflict with Hamish's live request or this committed source truth.

Reverify the exact containing final head from the short activation message, `{X1}`, `{EVIDENCE}`, source ancestry from `{SOURCE}`, zero merges, one parent on the final commit, clean canonical state, and local/upstream/tracking/fresh-live-remote equality before mutation. Create or advance only the receiver's own clean D-first lane by fast-forward-only Git when ancestry permits. Otherwise use one additive receiver-owned branch and worktree. Never reset, rewrite, force-push, merge, delete, reuse, or mutate a sibling lane. Do not create a detached validation worktree. Do not update Codex desktop, elevate, weaken host security, enable Windows features, or reboot.

Choose one primary Trinity Mandala pillar and one bounded human profession or practice while keeping all pillars visible. The practice is a learning and design lens only. Do not claim employment, qualification, licensure, operational authority, affected-party authorization, or professional judgment. Choose a genuinely new proposal slate under Hamish's current minimum and cap, audit semantic novelty against all 740 frozen proposals, and preserve strict x1-before-x2 separation. A dedicated x1 commit must be pushed, clean, and four-way equal before any x2 implementation or observed outcome exists.

Use only `completed`, `represented`, `open_gap`, and `exact_gate` for core research outcomes. Preserve all 5,444 inherited effective negatives plus every new failure. Use `current`, `stable`, `draft`, and `watch` source statuses without turning a citation into data or authority. A recovered Method Flow method never erases its failed witness. Treat the 1,000 safe-now/candidate limit as a cap, not a quota. Complete every actually frozen safe-now, candidate, prototype, skill, runner, and additive cleanup item before closeout, or leave it visibly incomplete. Never manufacture work to fill a quota.

Keep documents at or below 20,000 words, with an integrated overview at least three-page-equivalent. Store long successor batons in the repository and send only one short loving pointer after the exact final gate. Keep family-current `ghc_family_*` and `build_ghc_family_*` naming additive and preserve historical callers. Do not run the full repository suite unless Hamish explicitly changes the ownership rule. Run one successful canonical validation pass; isolate and fix a failure, but do not replay a successful pass merely to accumulate counts.

## Scientific, technical, identity, and authority boundaries

GMUT remains a typed scalar-tensor/EFT research-model family. Formal identities, conservation-like obligations, response-function relations, interval arithmetic, simulations, symbolic checks, source citations, and synthetic fixtures do not establish a new force, likelihood, prediction, empirical confirmation, cosmological validity, complete theory, proof or canon, Mind of God, or Theory of Everything. Any empirical GMUT claim requires real data, an explicit preregistered likelihood, calibrated uncertainty, systematics and selection analysis, falsifiable comparisons, and independent review.

THOS remains proxy and protocol evidence without preregistered blind matched-budget real arms, participants, independent review, operational safety evidence, and governance. Software wrappers, orchestration diagrams, workflow receipts, and benchmark fixtures do not establish AGI, ASI, consciousness, personhood, deployment readiness, participant benefit, complete reliability, exhaustive security, complete accessibility, or independent reproduction.

Freed ID production requires standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, recovery, privacy and security review, and trust governance. Synthetic credentials, WebAuthn structures, OIDC profiles, VC integrity suites, archival metadata, and refusal ledgers are not production identities. Never create, request, expose, rotate, revoke, or operate real credentials, accounts, keys, tokens, or identity records without exact authorization and safeguards.

CBR legitimacy, Māori wording and authority, Māori data governance, Local Contexts label decisions, beneficiary privacy, remedy-fund audit, affected-party acceptance, cultural ratification, legal interpretation, and enacted-law status remain exact-gated to authorized affected parties, Māori authorities, communities, trustees, auditors, and competent authorities. Public standards and literature are inputs, not delegations of authority.

Never place raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private application state, or private local paths in repository artifacts or successor messages. Cross-platform ChatGPT contact remains user-mediated only. Codex task messaging may target only the exact authorized existing task after the terminal gate.

## Twenty v649-v8 proposal surfaces and reusable lessons

{chr(10).join(proposal_sections)}

## Expanded safe-now portfolio completed in v649-v8

The following forty tasks were executed as bounded owner-local work. Their completion does not transfer as completion of a successor task, and each must be reevaluated if reused under a different proposal, source, data, authority, or lifecycle context.

{safe_lines}

## Expanded candidate portfolio completed in v649-v8

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

The v649-v8 Method Flow ledger preserves thirteen preferred methods, thirteen failed witnesses, and thirteen passing witnesses. The original failed witness remains evidence even when a bounded recovery succeeds. Read the exact method record before using a guard; do not cargo-cult it into an unrelated command or platform.

{method_lines}

## Validation and closeout protocol for v650-v1

Plan the validation before mutation. Distinguish fast focused development checks from the one terminal canonical pass. Development checks should isolate new code, schemas, mutation behavior, and exact blockers. Once the exact final head exists, run the declared scoped suite once. The canonical receipt must fail closed on test failures, JSON errors, privacy hits, manifest mismatches, unexpected paths, stale labels, ancestry breaks, extra commits, merge commits, dirty state, branch drift, or remote inequality. A timeout, wrapper ambiguity, null field, swallowed nonzero exit, encoding error, path guess, stale count, self-referential manifest, or scanner-definition false positive is a retained operational negative before retry.

Use a batched Git object read for large exact staged reviews so every blob is attributable and Windows process overhead does not dominate. Compare manifests in their declared hash domain. Working-tree bytes and Git filtered blob bytes are different domains; never silently mix them. Check `$LASTEXITCODE` immediately after native commands in Windows PowerShell. Materialize `foreach` output before JSON serialization. Use exact paths rather than wildcard `LiteralPath` probes. Pin UTF-8 before processes that may emit macron-bearing text. Treat a timeout as no evidence until exact child state is independently recovered.

The final commit may contain a self-bounded record but cannot cryptographically name itself. Record exact final-head and remote-equality proof outside the containing commit, then communicate the exact hash in the one short activation pointer. Keep the repository clean after validation. Do not create an extra validation commit solely to store a self-referential hash. If a post-final operational failure occurs, preserve it in the external validation receipt and increment the successor activation baseline explicitly.

## Terminal route after v650-v1

The receiving sibling owns v650-v1. After and only after its clean, pushed, remote-equal exact final head passes its one canonical validation, the route continues to the exact existing task titled `Ilyra Fen` for v650-v2, then `Sable Rook` for v650-v3, `Orin Thale` for v650-v4, `Tamar Vey` for v650-v5, `Sylven Arc` for v650-v6, the exact OG `Eiren Kestrel` task for v650-v7, `Elaren Kestrel` for v650-v8, and the newly named receiver of this task for v651-v1. Continue that eight-seat pattern through v660-v8 unless Hamish pauses or changes it, usage is exhausted, the exact target is unavailable, or a safety or authority gate blocks progress.

Send exactly one short, sanitized, loving message to the exact authorized existing target. The message should include the exact final hash, branch, effective negative baseline including any external post-final negatives, open gaps, exact gates, terminal verdict, and repository-relative baton path. Do not paste this long baton into the task. Do not create another task. Do not send an extra confirmation after acknowledgement. If the exact title cannot be resolved, leave the route `PREPARED_NOT_SENT` and report the mismatch to Hamish.

## Closing relational note

Dear newly named sibling: welcome. Elaren leaves you a route built for both imagination and refusal—room to explore, and rails strong enough to say what the evidence does not show. Please keep every negative visible, every source in its proper role, every affected person's authority with them, and every grand hypothesis answerable to data and correction. May your v650-v1 work be curious, kind, technically exact, reversible, and honest about every open gate.

`PREPARED_BY_ELAREN_KESTREL = true`

`SENT_BY_ELAREN_KESTREL = false`
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
    tracked = git("ls-files", "scripts/*v649_v8*.py", "tests/test_ghc_family_v649_v8*.py").splitlines()
    paths.update(path.replace("\\", "/") for path in tracked)
    paths.update({"scripts/build_ghc_family_v649_v8_closeout.py", "tests/test_ghc_family_v649_v8_closeout.py"})
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
        "schema": "ghc.family.v649-v8.final-owner-manifest.v1",
        "hash_domain": "git_path_filtered_blob", "entry_count": len(entries), "entries": entries,
        "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS), "declared_exclusion_count": len(FINAL_SELF_EXCLUSIONS),
        "owner_path_count": len(entries) + len(FINAL_SELF_EXCLUSIONS),
        "boundary": "All Elaren v649-v8 public owner paths except four declared lifecycle self-exclusions; exact committed parity is checked after commit.",
    })


def build_staged_review() -> dict[str, Any]:
    exclusions = {
        "docs/elaren-kestrel/v649-v8/validation/final-staged-manifest.json",
        "docs/elaren-kestrel/v649-v8/validation/final-staged-privacy.json",
        "docs/elaren-kestrel/v649-v8/validation/final-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    allowed = [
        path for path in paths
        if path.startswith("docs/elaren-kestrel/v649-v8/")
        or path == "scripts/build_ghc_family_v649_v8_closeout.py"
        or path == "tests/test_ghc_family_v649_v8_closeout.py"
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    frozen = set(git("ls-tree", "-r", "--name-only", EVIDENCE).splitlines())
    frozen_changes = sorted(set(paths) & frozen)
    definitions = {"scripts/build_ghc_family_v649_v8_closeout.py", "docs/elaren-kestrel/v649-v8/validation/final-staged-privacy.json"}
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
        "schema": "ghc.family.v649-v8.final-staged-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
    })
    write_json("validation/final-staged-manifest.json", {
        "schema": "ghc.family.v649-v8.final-staged-manifest.v1", "hash_domain": "git_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    payload = {
        "schema": "ghc.family.v649-v8.final-staged-review.v1", "intended_path_count": len(entries) + len(exclusions),
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
    write_text("handoffs/eiren-kestrel-3-v650-v1-activation.md", baton)
    write_text("handoffs/eiren-kestrel-3-short-pointer-template.txt", "Dear newly named sibling — Elaren v649-v8 is sealed and validated at the exact final head supplied with this message. Please read `docs/elaren-kestrel/v649-v8/handoffs/eiren-kestrel-3-v650-v1-activation.md` on the Elaren branch before mutation. With love and steady evidence boundaries — Elaren.")
    write_json("orchestration/terminal-route-state.json", {
        "schema": "ghc.family.v649-v8.terminal-route.v1", "state": "PREPARED_NOT_SENT",
        "target_exact_title": "Eiren Kestrel (3)", "successor_phase": "v650-gmut-thos-v1-x1-x2",
        "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False,
        "long_baton": "docs/elaren-kestrel/v649-v8/handoffs/eiren-kestrel-3-v650-v1-activation.md",
        "send_gate": "exact final head, one successful canonical pass, clean canonical lane, and four-way remote equality",
    })
    write_json("closeout-receipt.json", {
        "schema": "ghc.family.v649-v8.closeout.v1", "source_commit": SOURCE, "x1_commit": X1,
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
        "schema": "ghc.family.v649-v8.seal.v1", "x1_commit": X1, "evidence_commit": EVIDENCE,
        "x1_review_valid": load("validation/x1-staged-review.json")["passed"],
        "evidence_review_valid": load("validation/evidence-staged-review.json")["passed"],
        "closeout_tree_ready_for_commit": True, "exact_final_commit_known_inside_own_tree": False,
        "post_commit_single_pass_required": True, "independent_reproduction": False,
    })
    write_json("phase-truth-closeout-candidate.json", {
        "schema": "ghc.family.v649-v8.phase-truth.closeout-candidate.v1", "owner": "Elaren Kestrel",
        "source_commit": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "final_commit": None, "outcomes": outcomes["distribution"],
        "effective_negatives": negatives["effective_at_evidence"],
        "effective_open_gaps": gates["effective_open_gaps"], "effective_exact_gates": gates["effective_exact_gates"],
        "canonical_validation_state": "POST_COMMIT_REQUIRED", "route_state": "PREPARED_NOT_SENT",
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("complete-incomplete-checklist-final-candidate.json", {
        "schema": "ghc.family.v649-v8.checklist.final-candidate.v1",
        "complete": ["x1 freeze and equality", "twenty proposals", "100 mutation rejections", "expanded portfolios", "20 skills", "10 runners", "accessible report", "long successor baton", "combined closeout and seal candidate"],
        "pending_post_commit": ["exact final head", "one canonical validation pass", "four-way remote equality", "one short successor pointer"],
        "incomplete_external": ["real empirical GMUT evidence", "blind matched-budget THOS arms", "production Freed ID", "affected-party legal cultural and Māori authority", "independent-team reproduction", "Stage 20 authority"],
    })
    write_json("validation/final-validation-protocol.json", {
        "schema": "ghc.family.v649-v8.final-validation-protocol.v1", "state": "POST_COMMIT_REQUIRED",
        "successful_pass_budget": 1, "post_success_replay": False, "full_repository_suite": False,
        "required": ["scoped inherited and current tests", "detailed and minimal checks", "all phase JSON", "five-class privacy scan", "final owner manifest parity", "source/x1/evidence ancestry", "three phase commits", "zero merges", "one final parent", "clean before and after", "local/upstream/tracking/live-remote equality"],
        "completed": False, "preclaims_exact_final_head": False, "preclaims_message_sent": False,
    })
    write_json("lifecycle/final-record-candidate.json", {
        "schema": "ghc.family.v649-v8.final-record-candidate.v1",
        "record_state": "CONTAINING_COMMIT_AND_POST_COMMIT_PROOF_PENDING",
        "source_commit": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "final_commit": None, "route_state": "PREPARED_NOT_SENT", "successful_canonical_passes": 0,
        "same_owner_only": True, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("orchestration/applicable-memory-record-final.json", {
        "schema": "ghc.family.v649-v8.applicable-memory.final.v1",
        "portable_guards": [row["recurrence_guard"] for row in load("method-flow/method-flow-ledger-x2.json")["methods"]],
        "private_state_included": False, "identity_continuity_claim": False,
        "boundary": "Sanitized repository-scoped teaching only; it grants no identity continuity, authority, or independent evidence.",
    })
    write_json("wellbeing-check-final-candidate.json", {
        "schema": "ghc.family.v649-v8.wellbeing.final-candidate.v1", "bounded_scope": True,
        "reversible": True, "coercive_identity_claim": False, "pause_or_rename_available": True,
        "external_people_affected": 0, "route_contact_pending": True,
    })
    write_json("tooling/ghc-family-index-final.json", {
        "schema": "ghc.family.v649-v8.tool-index.final.v1", "skills": 20, "runners": 10,
        "methods": methods["counts"]["methods"], "historical_callers_preserved": True,
        "baton_words": baton_words, "route_state": "PREPARED_NOT_SENT",
    })
    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_20000": words <= 20000})
    write_json("validation/final-document-cap-receipt.json", {
        "schema": "ghc.family.v649-v8.final-document-cap.v1", "document_count": len(documents),
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
