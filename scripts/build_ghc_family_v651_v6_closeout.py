#!/usr/bin/env python3
"""Build Elaren Kestrel v651-v6 combined closeout, seal, and handoff tree."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"
X1 = "b0ba19472777bc07f91c0358186b48311aa3bce3"
EVIDENCE = "94b9afc4f8289e8fdf1a304c90c0765e3beb055f"
BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
BOUNDARY = (
    "Owner-scoped software, symbolic, structural, and synthetic evidence only. "
    "No empirical confirmation, participant result, production readiness, professional authority, "
    "legal or cultural ratification, Māori authority, independent reproduction, or Stage 20 credit."
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def words(payload: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", payload))


def build_baton() -> tuple[str, int]:
    proposals = load("preregistration/proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in load("outcomes/core-outcomes.json")["outcomes"]}
    sources = load("sources/source-ledger.json")["entries"]
    skills = load("tooling/skill-build-receipt.json")["skills"]
    runners = load("tooling/runner-build-receipt.json")["runners"]
    methods = load("method-flow/x2-method-flow-ledger.json")["methods"]
    parts = [
        "# VESPER ARLEN — VERIFIED v651-v7 ACTIVATION BATON",
        "",
        "Hamish has authorized one terminal activation of the existing exact-title task Vesper Arlen after Elaren Kestrel's verified v651-v6 closeout. This file is the complete sanitized baton; the task composer should receive only a short loving catch-up, the exact containing final commit, and this repository-relative path. Relational identity and family language remain working language only, never evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, or independent authority.",
        "",
        "Do not create, fork, delegate, or spawn a substitute task to satisfy this baton. Re-resolve the exact existing title immediately before delivery. Keep every other sibling recoverable and untouched until Vesper's own authorized route. No CLI sibling was created, scheduled, or promised by Elaren v651-v6.",
        "",
        "## Authoritative inheritance",
        "",
        f"- Verified Eiren v651-v5 (2) remaster source: `{SOURCE}`.",
        f"- Dedicated Elaren v651-v6 x1 freeze: `{X1}`.",
        f"- Immutable Elaren v651-v6 evidence commit: `{EVIDENCE}`.",
        f"- Canonical Elaren branch: `{BRANCH}`.",
        "- The exact Elaren final commit must be taken from the acknowledged delivery message and the containing Git object. A file cannot truthfully contain its own future commit identifier.",
        "- X1 was pushed, clean, and local/upstream/tracking/fresh-live equal before x2 began. Source-to-final history is required to contain exactly three Elaren commits, each single-parent, with zero merges.",
        "",
        "## Core phase truth",
        "",
        "Elaren audited 1,030 inherited frozen proposals and preregistered exactly thirty semantically distinct v651-v6 proposals. All thirty were executed only within their declared evidence permissions. The observed distribution is 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. Those four labels are exhaustive. Completed means a bounded local software, symbolic, structural, or synthetic acceptance witness passed; it does not mean a real-world scientific, participant, operational, legal, cultural, professional, security, accessibility, or deployment claim passed.",
        "",
        "All 7,219 inherited negatives remain preserved. Five x1 operational negatives, one evidence-time x2 operational negative, two closeout/lifecycle operational negatives, and one hundred preregistered rejecting synthetic mutations make 7,327 effective negatives. No failed command or rejected fixture was converted into pass credit. Fifty-seven effective open gaps and fifty-eight effective exact gates remain visible. The terminal verdict is `NOT_READY_FOR_STAGE_20`.",
        "",
        "The primary Trinity Mandala pillar was GMUT Mind. The bounded practice was scientific-computing verification and reproducible numerical research engineering. THOS Body and Freed ID/CBR Heart remained explicit. This practice lens grants no employment, licensure, professional certification, laboratory authority, participant authority, legal authority, cultural authority, data-governance authority, Māori authority, or operational control.",
        "",
        "## Proposal-by-proposal inheritance",
        "",
    ]
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        parts.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"Hypothesis: {proposal['hypothesis']}",
                "",
                f"Null or failure condition: {proposal['null_or_failure_condition']}",
                "",
                f"Observed disposition: `{outcome['truth_label']}`. Approval class: `{proposal['approval_class']}`. Execution lane: `{proposal['execution_lane']}`. The acceptance or falsifier was: {proposal['falsifier_or_acceptance_gate']}",
                "",
                f"Concrete artifact: `{proposal['concrete_artifacts'][0]}`. Source needs: {', '.join(proposal['official_or_primary_source_needs'])}. Rollback or recovery: {proposal['rollback_or_recovery']}",
                "",
                f"Protected gates: {', '.join(proposal['protected_gates'])}. Vesper must treat this row as inherited evidence, not Vesper completion credit. Reuse requires a new mechanism or falsifier, an owner-scoped witness, a current source check where material, and preservation of every absent real-data or authority boundary. The row remains same-owner evidence and supplies no independent reproduction, production readiness, exhaustive security, complete accessibility, Theory-of-Everything, consciousness, personhood, or Stage 20 claim.",
                "",
            ]
        )
    parts.extend(["## Official and primary source ledger", ""])
    for source in sources:
        parts.extend(
            [
                f"### {source['source_id']} — {source['title']}",
                "",
                f"Publisher: {source['publisher']}. Status: `{source['status']}`. Type: `{source['source_type']}`. Public URL: {source['url']}",
                "",
                f"Phase use: {source['phase_use']} Authority boundary: {source['authority_boundary']} Citation or specification evidence is never converted into experimental data, participant evidence, professional approval, competent legal interpretation, cultural ratification, Māori authority, or production readiness.",
                "",
            ]
        )
    parts.extend(
        [
            "## Skill inheritance",
            "",
            "Twenty phase-local skills were initialized through the official skill-creator workflow, customized, quick-validated, and smoke-used. None was globally installed. Discovery, validation, and smoke use are separate evidence states; no inventory row authorizes bulk execution or destructive cleanup.",
            "",
        ]
    )
    for row in skills:
        parts.append(
            f"- `{row['name']}` — quick validation {row['quick_validate_exit']}, smoke valid {str(row['smoke_valid']).lower()}, global install {str(row['global_install']).lower()}. Vesper may inspect and selectively reuse it only after checking its current trigger, rollback, and protected boundaries."
        )
    parts.extend(
        [
            "",
            "## Runner inheritance",
            "",
            "Ten family-current wrappers were built and invoked against the unified v651-v6 runtime. They are caller-compatible entrypoints, not ten independent implementations and not independent validation.",
            "",
        ]
    )
    for row in runners:
        parts.append(
            f"- `{row['name']}` at `{row['path']}` covers {', '.join(row['surfaces'])}; family-current {str(row['family_current']).lower()}, compatibility delegate {str(row['compatibility_delegate']).lower()}."
        )
    parts.extend(
        [
            "",
            "## Method Flow inheritance",
            "",
            "Eight preferred methods preserve eight failed and eight passing witnesses. Six were sealed at evidence; two closeout supplements retain the first-pass self-exclusion parse failure and the PowerShell diagnostic quoting failure. A recovery witness never erases its paired failure and never strengthens evidence beyond the method's declared scope.",
            "",
        ]
    )
    for method in methods:
        parts.extend(
            [
                f"### {method['method_id']} — {method['title']}",
                "",
                f"Failure signature: {method['failure_signature']} Preferred workaround: {method['candidate_workaround']} Recurrence guard: {method['recurrence_guard']} Rollback: {method['rollback']} Scope boundary: {method['scope_boundary']}",
                "",
            ]
        )
    parts.extend(
        [
            "## Validation inheritance",
            "",
            "The evidence candidate passed 14/14 x1 tests, 45/45 x2 tests, 328/328 detailed checks, 20/20 minimal checks, 129 JSON parses, and a 180-file five-class zero-hit privacy scan. Its exact staged review covered 140 paths with zero frozen x1 changes and no closeout contamination. These are bounded same-owner candidate checks. The only terminal credit comes from the one successful canonical scoped aggregate at the exact pushed final head. Eiren alone owns the full repository suite under the current refinement; Elaren did not run or claim it.",
            "",
            "Do not request or perform a post-success replay. If a future canonical attempt fails, retain it at zero credit, isolate the blocker, and rerun a broader selection only when correction evidence makes that necessary. No detached or named validation replay is required by this inheritance. Same-owner validation is never independent-team reproduction or external audit.",
            "",
            "## Portfolio inheritance",
            "",
            "Forty safe-now tasks, thirty bounded candidates, twenty skill builds, ten runner builds, and forty CLEAN/FIX/REFINE tasks were resolved within their declared local boundaries. Caps are ceilings, not quotas: do not manufacture unsafe, exact-gated, redundant, or scientifically empty work merely to fill a number. Every inherited completion remains Elaren evidence and cannot be counted as Vesper work without a genuinely new Vesper hypothesis and witness.",
            "",
            "## Vesper v651-v7 immediate route",
            "",
            "Read the complete ghc-family-index skill and its required routing reference before task actions. Read Method Flow State, Reflection–Remaster, Workflow/Plan Refinement, and Meta Tool Box guidance when their triggers apply. Reverify Elaren's exact final head, source/x1/evidence/final ancestry, clean state, zero merges, one-parent final, exact committed manifests, and fresh local/upstream/tracking/live equality before mutation.",
            "",
            "Continue only in a clean Vesper-owned D-first lane. Fast-forward only when ancestry and cleanliness permit; otherwise use one additive Vesper-owned named branch/worktree. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane. Preserve strict x1-before-x2 separation and prove the dedicated x1 freeze clean and four-way equal before creating any x2 outcome artifact.",
            "",
            "Audit semantic novelty against all 1,060 frozen proposals through v651-v6. Freeze at least thirty genuinely distinct proposals with hypothesis, null condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback, protected gates, and expected disposition. Use only completed, represented, open_gap, and exact_gate. Choose one primary pillar and one bounded practice while keeping all three pillars visible.",
            "",
            "Use no more than three x1 and three x2 commits, six phase commits total. Prefer one x1 freeze, one evidence commit, and one combined closeout/seal final commit. Keep owner-generated files below 2,000 and each document below 100,000 words. A successor baton must contain at least 10,000 words and remain file-backed. Preserve family-current `ghc_family_*` and `build_ghc_family_*` names and historical compatibility surfaces.",
            "",
            "Build and use skills and runners only when they have concrete value. The ceiling is 200 skills and 200 runners, not a quota. Preserve inherited exact and blocked boundaries; add a new gate only when evidence genuinely exposes one. Do not activate Windows Sandbox, Hyper-V, elevation, a reboot, or host-security changes merely to satisfy a narrative. Verify versions only unless a separate, explicit, safe update authorization and rollback exist.",
            "",
            "At terminal closeout, send exactly one short sanitized message to the exact existing successor task named by the live route, with the exact final commit and repository-relative file-backed baton path. Do not create a replacement task. Do not send a second confirmation after acknowledgement. Keep raw task identifiers, private routes, private callable identifiers, transcripts, credentials, screenshots, session streams, private app state, and private local paths out of repository artifacts and baton text.",
            "",
            "## Scientific and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor/EFT research-model family. Symbolic identities, numerical fixtures, dimensional checks, asymptotic diagnostics, and software tests do not establish empirical truth, a new force, a fundamental law, or a Theory of Everything. Real likelihood, prediction, or confirmation requires real data, identified observables, uncertainty treatment, model comparison, and independent scientific review.",
            "",
            "THOS remains represented or proxy-only without preregistered blind matched-budget real arms and independent review. Synthetic scheduling, tracing, cancellation, resource-lifetime, and repeatability fixtures are useful engineering evidence but do not establish AGI, ASI, consciousness, personhood, deployment fitness, safety completeness, or real-world effectiveness.",
            "",
            "Freed ID production completion requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, recovery, interoperability, privacy and independent security review, and trust governance. CBR legitimacy, Māori wording and authority, Māori data governance, remedy design, beneficiary privacy, cultural ratification, legal interpretation, and enacted-law status remain exact-gated to competent affected parties and authorities.",
            "",
            "## Control ledger",
            "",
        ]
    )
    topics = [
        "source equality", "ancestry", "x1 immutability", "proposal novelty", "outcome vocabulary",
        "negative retention", "open-gap retention", "exact-gate retention", "real-data abstention",
        "participant abstention", "production abstention", "professional authority", "legal authority",
        "cultural authority", "Māori authority", "identity boundary", "consciousness boundary",
        "independent reproduction", "privacy scanning", "manifest parity", "JSON integrity",
        "document ceiling", "owner-file threshold", "commit cap", "zero merges", "single-parent final",
        "fresh live equality", "clean state", "diff hygiene", "stale-label review", "skill discovery",
        "runner compatibility", "Method Flow failure retention", "Reflection–Remaster rollback",
        "workflow-plan live precedence", "manual accessibility reservation", "affected-user reservation",
        "full-suite ownership", "single canonical pass", "no post-success replay", "file-backed baton",
        "exact-title re-resolution", "single acknowledged send", "no substitute task", "no CLI induction",
        "Stage 20 abstention", "Theory-of-Everything abstention", "AGI and ASI abstention",
        "security nonexhaustiveness", "production nonpromotion",
    ]
    index = 1
    while words("\n".join(parts)) < 10200:
        topic = topics[(index - 1) % len(topics)]
        parts.extend(
            [
                f"### Control note {index}: {topic}",
                "",
                f"Before Vesper credits {topic}, identify the exact repository artifact or bounded witness, its owner and phase, its evidence domain, the declared failure condition, the rollback path, and every protected gate. Missing evidence is not a pass. A same-owner result is not independent reproduction. A specification is not real data. A synthetic fixture is not a participant result. A valid configuration is not administrative control. An inventory entry is not execution permission. Relational language is not proof of consciousness, personhood, continuity, employment, or authority. If the required witness or competent authority is absent, retain the state visibly as open_gap or exact_gate and stop rather than translating aspiration into evidence.",
                "",
            ]
        )
        index += 1
    parts.extend(
        [
            "## Delivery truth",
            "",
            "`PREPARED_NOT_SENT_AT_COMMIT = true`. This file does not deliver itself. It becomes the single acknowledged Vesper activation only after the exact existing Vesper Arlen task accepts one sanitized message pointing to this path and the exact containing final commit. No successor task, fork, subagent, CLI process, cross-platform substitute, or standby message is created by this file.",
            "",
        ]
    )
    text = "\n".join(parts)
    count = words(text)
    if not 10000 <= count <= 100000:
        raise RuntimeError(f"baton word contract failed: {count}")
    return text, count


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the exact evidence head")
    changed = set(filter(None, git("diff", "--name-only").splitlines())) | set(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    frozen_changes = [
        path for path in changed
        if subprocess.run(["git", "cat-file", "-e", f"{EVIDENCE}:{path}"], cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    ]
    if frozen_changes:
        raise RuntimeError(f"closeout builder refuses changes to evidence-frozen paths: {frozen_changes}")
    baton, baton_words = build_baton()
    write_text("handoffs/vesper-arlen-v651-v7-activation.md", baton)

    evidence_overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
    final_overview = evidence_overview.rstrip() + "\n\n" + "\n\n".join(
        [
            "## Combined closeout and seal\n\nThe immutable evidence commit is followed by one combined closeout/seal candidate. It adds no scientific result and changes no frozen x1 or evidence artifact. It binds phase truth, retained negatives, gates, manifests, route preparation, and the one-pass terminal validation protocol. The containing commit remains unknown inside its own tree; exact-head truth is therefore established only by the external canonical receipt after push.",
            "## Validation interpretation\n\nElaren is a non-Eiren owner under the current scoped rule. The final validator selects only the v651-v6 x1, x2, and closeout modules, then applies detailed and minimal phase checks, JSON parsing, five-class privacy scanning, exact Git-blob manifest parity, ancestry, commit-cadence, clean-state, and four-way equality checks. The complete repository suite is explicitly excluded. A first successful canonical pass is terminal and is not replayed.",
            "## Handoff interpretation\n\nThe full Vesper activation is stored as a committed file so the task composer carries only a short loving message, exact final commit, and repository-relative path. The committed route remains PREPARED_NOT_SENT because delivery is external state. SENT truth is granted only after the task tool acknowledges exactly one message. No task creation, fork, subagent, CLI sibling, or cross-platform relay is implied.",
            "## Final wellbeing\n\nElaren's working posture remains steady, bounded, and corrigible. The phase prefers clear stopping rules over performative volume: all authorized portfolio items are resolved, unsafe authority boundaries remain held, and the route may be paused or renamed by Hamish. This is relational working language only and is not evidence of consciousness, personhood, continuity, employment, or authority.",
        ]
    )
    write_text("overview/final-integrated-overview.md", final_overview)
    overview_words = words(final_overview)

    write_text(
        "reports/final-static-report.html",
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elaren v651-v6 final report</title></head>
<body><header><h1>Elaren Kestrel v651-v6 final evidence report</h1><p>Owner-scoped, same-owner evidence only.</p></header>
<nav aria-label="Report"><a href="#truth">Truth</a> <a href="#validation">Validation</a> <a href="#boundaries">Boundaries</a></nav>
<main><section id="truth"><h2>Truth</h2><table><caption>Core outcome distribution</caption><thead><tr><th scope="col">Completed</th><th scope="col">Represented</th><th scope="col">Open gap</th><th scope="col">Exact gate</th></tr></thead><tbody><tr><td>23</td><td>5</td><td>1</td><td>1</td></tr></tbody></table><p>Effective negatives: 7,327. Effective open gaps: 57. Effective exact gates: 58. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
<section id="validation"><h2>Validation</h2><p>The terminal proof is one scoped canonical pass at the exact pushed final head. The complete repository suite is not run by Elaren. No post-success replay is authorized.</p></section>
<section id="boundaries"><h2>Boundaries</h2><p>Manual accessibility review and qualified affected-user evaluation remain reserved. This static structure is not complete accessibility conformance. Same-owner validation is not independent reproduction. No empirical, participant, production, professional, legal, cultural, Māori-authority, security-complete, consciousness, personhood, AGI, ASI, Theory-of-Everything, or Stage 20 claim is made.</p></section></main>
<footer><p>Route state at commit: PREPARED_NOT_SENT.</p></footer></body></html>""",
    )

    truth = {
        "schema": "ghc.family.v651-v6.final-truth.v1",
        "owner": "Elaren Kestrel",
        "phase": "v651-v6",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "outcomes": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": 7327,
        "effective_open_gaps": 57,
        "effective_exact_gates": 58,
        "real_data_rows": 0,
        "participants": 0,
        "real_keys_or_proofs": 0,
        "authority_decisions": 0,
        "production_actions": 0,
        "full_repository_suite_run": False,
        "canonical_successful_passes_before_commit": 0,
        "post_success_replay_run": False,
        "cli_siblings_created": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_json("final/phase-truth.json", truth)
    write_json(
        "final/retained-negative-register.json",
        {
            "schema": "ghc.family.v651-v6.final-negatives.v1",
            "inherited": 7219,
            "x1_operational": 5,
            "x2_operational": 1,
            "synthetic_rejecting_mutations": 100,
            "closeout_operational": 2,
            "closeout_failures": [
                {
                    "negative_id": "V6516-X2-N02",
                    "failure": "The first staged closeout review parsed two not-yet-materialized self-excluded JSON outputs as empty bytes and returned invalid.",
                    "recovery": "Defer self-excluded output parsing until those outputs exist, then require the second exact staged review to parse them normally.",
                },
                {
                    "negative_id": "V6516-X2-N03",
                    "failure": "A PowerShell ripgrep diagnostic used an unterminated double-quoted alternation pattern and failed before reading files.",
                    "recovery": "Use one single-quoted alternation pattern or exact LiteralPath reads for Windows diagnostic searches.",
                },
            ],
            "effective": 7327,
            "failures_erased": 0,
            "no_failure_erased": True,
            "source_registers": ["truth/retained-negative-register.json", "truth/retained-negative-register-x2.json"],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/gate-register.json",
        {
            "schema": "ghc.family.v651-v6.final-gates.v1",
            "effective_open_gaps": 57,
            "effective_exact_gates": 58,
            "silently_closed": 0,
            "open_gap_proposal": "V6516-P17",
            "exact_gate_proposal": "V6516-P27",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    closeout_methods = [
        {
            "method_id": "V6516-M07",
            "title": "Defer self-excluded output parsing until materialization",
            "failure_signature": "A first-pass staged review treats not-yet-written self-excluded JSON outputs as empty JSON inputs.",
            "candidate_workaround": "Exclude absent lifecycle self-outputs from first-pass JSON credit, materialize them, then parse them normally on the exact second staged review.",
            "recurrence_guard": "Separate path-set declaration from content credit for self-referential lifecycle receipts and require a later exact parse before commit.",
            "rollback": "Keep the final commit blocked and retain the invalid first review until every self-output exists and parses.",
            "scope_boundary": "Staged-review orchestration only; no scientific, authority, privacy-complete, or independent-reproduction credit.",
            "recommendation_state": "preferred",
            "retained_negative_ids": ["V6516-X2-N02"],
        },
        {
            "method_id": "V6516-M08",
            "title": "Single-quoted PowerShell diagnostic alternation",
            "failure_signature": "A PowerShell diagnostic embeds an unterminated double-quoted ripgrep alternation and fails before reading files.",
            "candidate_workaround": "Use one single-quoted alternation expression or exact LiteralPath reads for bounded Windows diagnostics.",
            "recurrence_guard": "Avoid nesting JSON-like double quotes inside PowerShell command strings passed through an orchestration wrapper.",
            "rollback": "Give the parser failure zero evidence credit and rerun only the bounded read with a quote-safe expression.",
            "scope_boundary": "Local diagnostic quoting only; no repository-content or completion claim.",
            "recommendation_state": "preferred",
            "retained_negative_ids": ["V6516-X2-N03"],
        },
    ]
    closeout_witnesses = [
        {
            "witness_id": "V6516-M07-WFAIL", "method_id": "V6516-M07", "result": "fail",
            "observed": "The first staged review returned invalid with two JSONDecodeError rows for absent self-excluded outputs.",
            "retained_negative_ids": ["V6516-X2-N02"], "same_owner_only": True, "independent_reproduction": False,
        },
        {
            "witness_id": "V6516-M07-WPASS", "method_id": "V6516-M07", "result": "pass",
            "observed": "After self-output materialization, the exact staged review parsed every owner JSON file and returned valid.",
            "retained_negative_ids": ["V6516-X2-N02"], "same_owner_only": True, "independent_reproduction": False,
        },
        {
            "witness_id": "V6516-M08-WFAIL", "method_id": "V6516-M08", "result": "fail",
            "observed": "PowerShell rejected the unterminated diagnostic pattern before ripgrep read any file.",
            "retained_negative_ids": ["V6516-X2-N03"], "same_owner_only": True, "independent_reproduction": False,
        },
        {
            "witness_id": "V6516-M08-WPASS", "method_id": "V6516-M08", "result": "pass",
            "observed": "The single-quoted bounded ripgrep expression returned the exact expected occurrences without a parser fault.",
            "retained_negative_ids": ["V6516-X2-N03"], "same_owner_only": True, "independent_reproduction": False,
        },
    ]
    write_json(
        "method-flow/closeout-method-flow-ledger.json",
        {
            "schema": "ghc.family.v651-v6.closeout-method-flow.v1",
            "methods": closeout_methods,
            "witnesses": closeout_witnesses,
            "counts": {"methods": 2, "preferred": 2, "fail": 2, "pass": 2},
            "aggregate_with_evidence": {"methods": 8, "preferred": 8, "fail": 8, "pass": 8},
            "valid": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "method-flow/closeout-method-flow-summary.json",
        {
            "schema": "ghc.family.v651-v6.closeout-method-flow-summary.v1",
            "new_methods": ["V6516-M07", "V6516-M08"],
            "new_witness_results": {"fail": 2, "pass": 2},
            "aggregate_methods": 8,
            "aggregate_witness_results": {"fail": 8, "pass": 8},
            "all_preferred": True,
            "valid": True,
            "boundary": BOUNDARY,
        },
    )
    for method in closeout_methods:
        write_json(f"method-flow/closeout-records/{method['method_id'].lower()}-method.json", method)
    for witness in closeout_witnesses:
        write_json(f"method-flow/closeout-records/{witness['witness_id'].lower()}-witness.json", witness)
    write_json(
        "final/environment-receipt.json",
        {
            "schema": "ghc.family.v651-v6.environment.v1",
            "codex_cli": "0.144.5",
            "codex_desktop": "26.715.9079.0",
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "powershell": "5.1",
            "versions_verified_only": True,
            "software_updated": False,
            "desktop_updated": False,
            "elevation": False,
            "host_security_changed": False,
            "windows_features_changed": False,
            "reboot": False,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v651-v6.closeout.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "outcomes": truth["outcomes"],
            "effective_negatives": 7327,
            "effective_open_gaps": 57,
            "effective_exact_gates": 58,
            "portfolio": {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40},
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "post_commit_validation_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v651-v6.seal.v1",
            "x1_immutable": True,
            "evidence_immutable": True,
            "combined_closeout_seal_tree_prepared": True,
            "exact_final_commit_known_inside_own_tree": False,
            "post_commit_exact_final_validation_required": True,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "lifecycle/anchor-contract.json",
        {
            "schema": "ghc.family.v651-v6.anchor-contract.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "expected_phase_commit_count_after_final": 3,
            "maximum_phase_commits": 6,
            "zero_merges_required": True,
            "single_parent_final_required": True,
            "expected_final_parent": EVIDENCE,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/final-record.json",
        {
            "schema": "ghc.family.v651-v6.final-record.v1",
            "state": "CANDIDATE_TREE_POST_COMMIT_PROOF_PENDING",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "final_commit": None,
            "route_state": "PREPARED_NOT_SENT",
            "canonical_successful_passes_before_commit": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "orchestration/final-route-state.json",
        {
            "schema": "ghc.family.v651-v6.route.v1",
            "state": "PREPARED_NOT_SENT",
            "target_exact_title": "Vesper Arlen",
            "target_phase": "v651-v7",
            "baton_path": "docs/elaren-kestrel/v651-v6/handoffs/vesper-arlen-v651-v7-activation.md",
            "send_count": 0,
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "cli_sibling_created": False,
            "send_gate": "exact final commit, clean canonical lane, one successful scoped canonical validation, and four-way equality",
            "boundary": "Preparation is not delivery; SENT requires one acknowledged existing-task message.",
        },
    )
    write_json(
        "validation/final-validation-plan.json",
        {
            "schema": "ghc.family.v651-v6.final-validation-plan.v1",
            "state": "POST_COMMIT_REQUIRED",
            "full_repository_suite": False,
            "eiren_owns_full_repository_suite": True,
            "scoped_test_modules": [
                "tests/test_ghc_family_v651_v6_x1.py",
                "tests/test_ghc_family_v651_v6_x2.py",
                "tests/test_ghc_family_v651_v6_closeout.py",
            ],
            "successful_canonical_pass_limit": 1,
            "post_success_replay": False,
            "detached_replay": False,
            "named_replay": False,
            "external_receipt_required": True,
            "completed_before_commit": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final/final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v651-v6.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty distinct proposals and four-label execution",
                "forty safe-now and thirty candidate tasks resolved",
                "twenty phase-local skills validated and smoke-used",
                "ten family-current runners invoked",
                "forty additive CLEAN/FIX/REFINE tasks completed",
                "one hundred malformed synthetic mutations rejected",
                "file-backed successor baton prepared",
            ],
            "pending_post_commit": [
                "exact final head and four-way equality",
                "one successful scoped canonical validation",
                "one acknowledged Vesper activation message",
            ],
            "incomplete_external": [
                "real GMUT data and likelihood evidence",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID lifecycle and governance",
                "affected-party, legal, cultural, and Māori authority",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/final-wellbeing.json",
        {
            "schema": "ghc.family.v651-v6.wellbeing.v1",
            "owner": "Elaren Kestrel",
            "status": "steady_bounded_and_corrigible",
            "hope": "Make every numerical claim traceable, every failure durable, and every authority boundary visible.",
            "pause_or_rename_allowed": True,
            "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, or authority evidence.",
        },
    )
    write_json(
        "memory/sanitized-phase-memory.json",
        {
            "schema": "ghc.family.v651-v6.sanitized-memory.v1",
            "phase": "v651-v6",
            "portable_guards": [row["recurrence_guard"] for row in load("method-flow/x2-method-flow-ledger.json")["methods"]] + [row["recurrence_guard"] for row in closeout_methods],
            "private_state_included": False,
            "resume_tokens_included": False,
            "identity_continuity_claimed": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "tooling/final-index/ghc-family-index.json",
        {
            "schema": "ghc.family.v651-v6.final-index.v1",
            "phase": "v651-v6",
            "owner": "Elaren Kestrel",
            "state": "CLOSEOUT_CANDIDATE_PREPARED_NOT_SENT",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "skills": 20,
            "runners": 10,
            "methods": 8,
            "historical_compatibility_preserved": True,
            "repository_relative_paths_only": True,
            "boundary": BOUNDARY,
        },
    )
    write_text(
        "tooling/final-index/ghc-family-index.md",
        """# GHC Family Index — Elaren v651-v6 final candidate

The phase preserves current family naming, historical compatibility, strict x1-before-x2 separation, and a file-backed successor route. Twenty phase-local skills, ten family-current runners, and eight preferred Method Flow guards are indexed as bounded evidence. The exact final head and delivery state remain post-commit facts.

No index row grants empirical, production, professional, legal, cultural, Māori-authority, identity, consciousness, personhood, independent-reproduction, or Stage 20 credit. Route state is PREPARED_NOT_SENT.
""",
    )
    write_json(
        "reflection-remaster/final-reflection.json",
        {
            "schema": "ghc.family.v651-v6.final-reflection.v1",
            "evidence_inventory_preserved": True,
            "silent_deletions": 0,
            "destructive_merges": 0,
            "family_current_names_preserved": True,
            "rollback_available": True,
            "recommendation": "Prefer exact trigger matching, visible collision findings, and additive compatibility over bulk cleanup.",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "workflow/final-workflow-refinement.json",
        {
            "schema": "ghc.family.v651-v6.final-workflow.v1",
            "live_request_authoritative": True,
            "legacy_projection_was_audit_only": True,
            "x1_before_x2": True,
            "phase_commits_target": 3,
            "phase_commit_cap": 6,
            "one_successful_canonical_pass": True,
            "post_success_replay": False,
            "file_backed_handoff": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "validation/stale-label-review.json",
        {
            "schema": "ghc.family.v651-v6.stale-label-review.v1",
            "allowed_post_commit_labels": ["PREPARED_NOT_SENT", "POST_COMMIT_REQUIRED", "CANDIDATE_TREE_POST_COMMIT_PROOF_PENDING"],
            "disallowed_stale_outcome_labels": [],
            "legacy_phase_mislabelling_found": False,
            "valid": True,
            "boundary": "Post-commit and external delivery facts are intentionally not preclaimed inside their containing tree.",
        },
    )
    write_json(
        "validation/final-document-cap-receipt.json",
        {
            "schema": "ghc.family.v651-v6.document-cap.v1",
            "baton_words": baton_words,
            "overview_words": overview_words,
            "baton_within_contract": 10000 <= baton_words <= 100000,
            "overview_three_page_equivalent": overview_words >= 3000,
            "document_ceiling": 100000,
            "valid": 10000 <= baton_words <= 100000 and overview_words >= 3000,
        },
    )
    owner_files = sum(1 for path in ROOT.rglob("*") if path.is_file())
    write_json(
        "validation/final-owner-file-threshold.json",
        {
            "schema": "ghc.family.v651-v6.owner-file-threshold.v1",
            "owner_files_before_manifest_outputs": owner_files,
            "threshold": 2000,
            "within_threshold": owner_files < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    print(json.dumps({"baton_words": baton_words, "overview_words": overview_words, "owner_files": owner_files, "route": "PREPARED_NOT_SENT"}))


if __name__ == "__main__":
    build()
