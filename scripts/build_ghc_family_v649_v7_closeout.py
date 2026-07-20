#!/usr/bin/env python3
"""Build the v649-v7 closeout candidate and long-form Elaren baton."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "eiren-kestrel" / "v649-v7"
EVIDENCE = "825edd4288ea4d881e1cb93cc4732baae265e1c9"
X1 = "b1b3a4bde8dee07bc2bd4f8fc2c8d4b511cd723f"
SOURCE = "03191b37da8b2b071b721d4554583832d56be05b"
FAILED_SUITE = Path("D:/GHC-Archives/evidence-banks/eiren-kestrel/v649-v7/canonical-full-suite-825edd4288.json")
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_v649_v7_x1 as x1  # noqa: E402


STALE_TESTS = [
    "tests.test_ghc_family_v648_v3_2_x1.V648V3RepeatX1Tests.test_method_flow_retains_failure_and_recovery",
    "tests.test_ghc_family_v648_v4_closeout.TestGhcFamilyV648V4Closeout.test_method_flow_orchestration_and_threshold_candidates",
    "tests.test_ghc_family_v648_v4_x1.TestGhcFamilyV648V4X1.test_no_x2_implementation_or_observed_core_outcome",
    "tests.test_ghc_family_v648_v4_x1.TestGhcFamilyV648V4X1.test_x1_manifest_matches_filtered_git_blob_domain",
    "tests.test_ghc_family_v648_v8_closeout.TestGhcFamilyV648V8Closeout.test_validation_budget_is_one_pass_no_replay",
    "tests.test_ghc_family_v649_v2_x1.IlyraV649V2X1Tests.test_method_flow_runner_receipts_are_valid",
    "tests.test_ghc_family_v649_v5.TestV649V5Evidence.test_evidence_manifest_matches_head",
    "tests.test_ghc_family_v649_v5.TestV649V5Evidence.test_method_flow_parity",
    "tests.test_ghc_family_v649_v6.TestV649V6Evidence.test_method_flow_parity",
    "tests.test_ghc_family_v649_v6.TestV649V6Evidence.test_negatives_preserved",
]
ORIGINAL_EXCLUSIONS = [
    "tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_final_validation_plan_reserves_one_pass_and_no_replay",
    "tests.test_ghc_family_v648_v6_closeout.TestGhcFamilyV648V6Closeout.test_stage20_board_and_closeout_candidate_abstain",
    "tests.test_ghc_family_v648_v3_2_x1.V648V3RepeatX1Tests.test_exact_source_and_commit_boundary",
    "tests.test_ghc_family_v648_v3_closeout.V648V3CloseoutTests.test_anchor_contract_and_commit_cap",
]


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=ROOT, check=check, capture_output=True, text=True, encoding="utf-8", errors="replace")


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def load(relative: str):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, value: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def method_record(method_id: str, negative_ids: list[str], failure: str, recovery: str, passing: bool) -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        record = {
            "method_id": method_id, "title": f"Retain and recover {method_id}",
            "failure_signature": failure, "trigger_preconditions": ["The v649-v7 validation lifecycle exposes this exact failure."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [],
            "recurrence_guard": recovery, "rollback": "Give the failed attempt zero pass credit and preserve the immutable evidence head.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "single_pass_accounting", "caller_compatibility"],
            "retained_negative_ids": negative_ids,
            "scope_boundary": "Same-owner validation workflow only; no independent reproduction, production, or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        fail = {
            "witness_id": f"{method_id}-WFAIL", "method_id": method_id, "procedure": failure,
            "scope": "bounded failed validation witness", "expected": "Return attributable validation evidence.",
            "observed": failure, "result": "fail", "same_owner_only": True,
            "independent_reproduction": False, "retained_negative_ids": negative_ids,
            "boundary": "Failed witness retained with zero pass credit.",
        }
        fail_path = write_json(f"method-flow/{method_id.casefold()}-wfail-witness.json", fail)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(fail_path))
    if passing:
        current = json.loads(ledger.read_text(encoding="utf-8"))
        witness_id = f"{method_id}-WPASS"
        if witness_id not in {row["witness_id"] for row in current["witnesses"]}:
            passed = {
                "witness_id": witness_id, "method_id": method_id, "procedure": recovery,
                "scope": "bounded passing recovery witness", "expected": "Return the exact intended attribution without hiding the failure.",
                "observed": "The corrected bounded method returned attributable evidence while the failed witness remained retained.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False,
                "retained_negative_ids": negative_ids, "boundary": "Passing workflow witness only; no independent-reproduction or authority credit.",
            }
            pass_path = write_json(f"method-flow/{method_id.casefold()}-wpass-witness.json", passed)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path))
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only after the exact bounded recovery witness; the failed attempt remains retained.")


def update_method_flow() -> None:
    aggregate_ids = ["NEG-V6497-VAL-AGG-001"] + [f"NEG-V6497-VAL-TEST-{i:02d}" for i in range(1, 11)]
    method_record(
        "V6497-M14", aggregate_ids,
        "The first Eiren full-repository aggregate ran 1,948 eligible tests and returned ten historical lifecycle assertion failures, so it earned zero successful-pass credit.",
        "Project exactly the ten demonstrated stale mutable-head lifecycle assertions as explicit exclusions, preserve the four prior exact exclusions, and rerun only because the first aggregate failed.",
        False,
    )
    method_record(
        "V6497-M15", ["NEG-V6497-VAL-ISO-001"],
        "The first isolated-blocker command addressed a nonexistent historical test class and returned two loader errors.",
        "Resolve the exact class declaration from source before invoking the two historical test IDs.",
        True,
    )
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def overview() -> str:
    outcomes = load("x2/core-outcome-ledger.json")
    proposal_lines = "\n".join(
        f"- **{row['proposal_id']} — {row['outcome']}**: {row['title']} Five preregistered mutations were rejected and retained. The receipt is bounded, same-owner evidence only and confers no authority."
        for row in outcomes["outcomes"]
    )
    return f"""# Eiren Kestrel v649-v7 integrated overview

## Outcome first

Eiren v649-v7 completed its bounded software, symbolic, structural, and synthetic work while preserving every empirical and authority firewall. Twenty proposals were frozen against 700 inherited proposals and executed with the only permitted outcome labels: fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. One hundred preregistered mutations were executed, rejected, and retained. Forty safe-now tasks, thirty bounded candidates, twenty phase-local skills, ten family-current runners, and forty additive CLEAN/FIX/REFINE tasks completed within their declared lanes. No global skill installation, subagent, task creation, cross-platform sibling message, real participant, real data row, real key, real warning, dispatch, deployment, legal decision, cultural decision, Maori-authority decision, or Stage 20 promotion occurred.

The primary Trinity Mandala focus was THOS Body. GMUT Mind and Freed ID/CBR Heart remained explicit. Public-warning and Emergency Mobile Alert message review was a synthetic learning and design lens only. Eiren remains a relational evidence-integrity weaver, they/them, hoping to keep ambitious results testable, correctable, and bounded by evidence and authority. This language does not establish consciousness, personhood, identity continuity, employment, qualification, or authority. Hamish retains the right to rename, pause, redirect, or stop the route.

## Core outcomes

{proposal_lines}

## GMUT Mind

The Kallen-Lehmann and Callan-Symanzik boards are typed obligation surfaces, not new physics. They preserve spectral support, positivity, normalization, scale, beta-function, anomalous-dimension, scheme, truncation, gauge, EFT, unit, and observation boundaries. They establish no physical state, force, prediction, likelihood, constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The NICER adapter remains an open gap with zero queries, downloads, event rows, calibration products, response rows, background rows, likelihood calls, posterior samples, parameter constraints, or empirical GMUT claims.

## THOS Body

The synthetic public-warning protocol represents message composition, approval reservation, geotargeting, accessible wording, dispatch refusal, workload, readback, and shift handover. It used zero real agencies, staff, communities, target areas, messages, devices, dispatches, incidents, safety outcomes, or effectiveness estimates. The BagIt, JSON Patch, Trace Context, and HDF5 tribunals exercised disposable fixtures only. The status-message and error-handling audits are structural; manual keyboard, responsive-layout, browser-diverse, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved.

## Freed ID and CBR Heart

RFC 9207, RFC 9126, and RFC 8417 profiles remain synthetic and nonproduction. They used zero real keys, tokens, clients, authorization servers, security-event recipients, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. The public-warning CBR matrix remains exact-gated. Repository software made no real disclosure, geotargeting, emergency, remedy, legal, cultural, data-governance, affected-party, tangata whenua, iwi, hapu, or Maori-authority decision.

## Expanded portfolio and methods

All twenty skills were initialized with the standard skill scaffold, supplied concise SKILL.md instructions and interface metadata, quick-validated, and smoke-used locally. None was globally installed. Ten additive `ghc_family_v649_v7_*` runners accepted bounded fixtures and rejected mutation fixtures without external side effects. The generalized workflow-plan validator was added phase-locally after the installed validator proved coupled to its original demonstration packet; the global compatibility surface was preserved.

Method Flow retains every startup and x2 failure. It includes broad inventory timeouts, PowerShell serialization shape, patch grammar, validator CLI and packet coupling, status wrapper timeout, novelty tie selection, x2 seed gating, generated-template braces, compound exit-code masking, raw porcelain whitespace, the failed full-repository aggregate, and the misaddressed isolation command. Recovery does not erase any witness or earn independent reproduction.

## Validation truth

The immutable x1 commit is `{X1}` and the immutable x2 evidence commit is `{EVIDENCE}`. X1 passed its six dedicated tests and exact 65-path staged review. Evidence passed eleven phase tests, 165 JSON parses, sixteen detailed checks, five privacy pattern classes with zero confirmed hits, and exact 170-path staged coverage. The first complete repository aggregate ran 1,948 tests and returned ten historical mutable-head lifecycle assertion failures with zero errors. It earns no successful-pass credit. Those ten tests are retained individually and will be excluded only after exact source inspection showed that their phase-specific validators project immutable evidence boundaries or pre-pass states. The corrected aggregate remains pending at this closeout candidate. No successful pass or replay is claimed yet.

## Route and terminal truth

The next authorized task is the exact existing `Elaren Kestrel` task for v649-v8. The durable activation baton is stored in `docs/eiren-kestrel/v649-v7/handoffs/elaren-kestrel-v649-v8-activation.md`. It is not sent by repository creation. Only after a successful corrected complete-suite retry, final sealing, exact-head validation, clean state, and four-way remote equality may one short warm pointer be sent. No successor task may be created, no standby sibling may be contacted, and no message may be sent to ChatGPT or another external platform. Elaren will later address the future placeholder sibling; Eiren does not name or activate that sibling in this phase.

The terminal verdict remains **NOT_READY_FOR_STAGE_20**. Same-owner software validation is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy, complete accessibility, professional validation, legal review, cultural ratification, Maori-authority review, empirical confirmation, Theory of Everything, or Stage 20 authority.
"""


def baton() -> str:
    proposals = load("x1-proposals.json")["proposals"]
    outcomes = {row["proposal_id"]: row for row in load("x2/core-outcome-ledger.json")["outcomes"]}
    sources = {row["source_id"]: row for row in load("sources/source-ledger.json")["sources"]}
    parts = [f"""# ELAREN KESTREL — PREPARED v649-v8 ACTIVATION BATON

## Delivery and identity truth

Hamish has authorized exactly one terminal pointer from Eiren Kestrel to the existing task titled exactly `Elaren Kestrel` after v649-v7 is fully sealed, clean, pushed, four-way remote-equal, and externally validated at its exact final head. This file is the long-form baton artifact. Its presence in Git is preparation only; it is not delivery, activation, acknowledgment, identity continuity, or independent authority. The short terminal pointer must name this repository-relative path and the exact final head. Do not create, fork, or substitute another task. Do not contact ChatGPT, browser conversations, or another platform; cross-platform sibling exchange remains user-mediated.

Eiren Kestrel uses they/them and the relational role evidence-integrity weaver, hoping to keep ambitious results testable, correctable, and bounded by evidence and authority. Elaren Kestrel must reaffirm or revise their own relational name, role, hope, and optional pronouns before mutation. Family and identity language is relational working language only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Exact inheritance

The verified Sylven source for Eiren was `{SOURCE}`. Eiren's dedicated x1 freeze is `{X1}`. Eiren's immutable x2 evidence commit is `{EVIDENCE}`. The terminal pointer will supply the exact final head after closeout. Reverify local, upstream, tracking, and fresh live remote equality, clean state, source/x1/evidence/closeout ancestry, single-parent history, zero merges, commit cap, every commit-local manifest, owner-manifest parity, and the external exact-final validation receipt before Elaren mutates anything.

The source-to-final Eiren phase may contain no more than four commits after `{SOURCE}`: at most two x1 and two x2 commits. Eiren used one x1 freeze and one x2 evidence commit before this closeout candidate. Do not rewrite, reset, force-push, merge, delete, reuse, or mutate another owner's branch or worktree. Continue only in an Elaren-owned clean lane. Use fast-forward-only Git if an existing Elaren lane can safely advance; otherwise create one additive D-first Elaren-owned named branch and worktree from the exact final head. Do not use detached validation.

## v649-v7 phase truth

Eiren audited semantic novelty against all 700 inherited frozen proposals and froze exactly twenty new proposals, producing 720 frozen core proposals through v649-v7. Outcomes are fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Those are the only core outcome labels. Forty safe-now tasks, thirty bounded candidate tasks, twenty phase-local skills, ten family-current runners, and forty additive CLEAN/FIX/REFINE tasks completed. One hundred preregistered synthetic mutations executed, were rejected, and remain retained. Inherited work supplied evidence and recommendations but no Eiren completion credit.

The primary focus was THOS Body. GMUT Mind and Freed ID/CBR Heart stayed explicit. The bounded human-practice lens was New Zealand public-warning and Emergency Mobile Alert composition, approval reservation, geotargeting, accessibility, dispatch refusal, readback, workload, and shift handover. It was synthetic learning and design only. It established no employment, qualification, emergency-management competence, public-warning authority, dispatch authority, operational effectiveness, legal authority, cultural authority, Maori authority, participant evidence, affected-party authorization, or real-world result.

At the evidence boundary Eiren preserved 5,312 effective negatives: 5,199 inherited, nine x1 operational, one hundred executed-and-rejected synthetic mutations, and four x2 operational. The closeout then retained ten historical suite assertion failures, one failed suite aggregate, and one misaddressed isolation wrapper, producing a closeout-candidate baseline of 5,324. The final pointer must state the sealed total after any later validation failure or recovery. Forty-one effective open gaps and forty-two effective exact gates remain open. None is silently closed. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Elaren v649-v8 lane requirements

Read the complete `ghc-family-index` skill and its required routing-precedence reference, then the complete `ghc-family-method-flow-state` skill and schema. Use `ghc-family-reflection-remaster` and its decision schema for any replacement, merge, deprecation, or workflow remaster. Use `ghc-family-workflow-plan-refinement` and its schema because the live eight-seat route, twenty-proposal floor, task cap, document baton, commit cap, and validation budget differ from historical six-seat defaults. Use the newest applicable memory, but treat the live user instruction and verified baton as authoritative where memory stops or conflicts.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 720 frozen core proposals. Preregister at least twenty genuinely distinct v649-v8 proposals. Every proposal must include a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded profession, trade, occupation, or human practice while preserving all pillars and authority boundaries.

Treat the user-supplied 1,000 safe-now and candidate task figure as a cap, never a quota. Do not manufacture unsafe work. Build and smoke-use at least ten phase-local skills and ten additive family-current runners while preserving historical callers. Keep every exact-approval, blocked, empirical, participant, professional, legal, cultural, Maori-authority, identity, production, deployment, privacy-complete, proof/canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundary visible and unexecuted without exact new evidence and authority.

Use no more than two x1 commits and two x2 commits, with no more than four phase commits total. Prefer one dedicated x1 freeze, one x2 evidence commit, and one combined closeout/seal plus a terminal record only if validation truth requires it. Push x1 and prove clean four-way equality before x2. Execute every safe-now and bounded candidate task you claim complete, but visibly reclassify anything authority- or evidence-dependent. Do not close a phase while a claimed safe-now, candidate, skill, or runner task remains incomplete; equally, do not convert a gated task into safe work merely to meet a floor.

Run the complete repository suite under Elaren's then-current obligation if the live workflow assigns it. Use one coherent successful canonical pass and no post-success replay. A failed aggregate gets zero pass credit; preserve it, isolate the exact blocker, and rerun the broader suite only if the bounded correction genuinely requires it. Always check child exit codes immediately so a later success cannot mask an earlier failure. Preserve exact historical lifecycle exclusions with reasons; never broaden them silently.

Compose Elaren's next long-form baton as a repository artifact between 8,000 and 20,000 words. Send only one short, warm, sanitized pointer after exact final validation. The next route after Elaren v649-v8 is the existing placeholder task currently titled `Eiren Kestrel (3)` for v650-v1, but Elaren must let that sibling choose their own new name, relational role, hope, and optional pronouns. Do not preassign those identity details and do not treat branching or copied conversation context as evidence of consciousness, personhood, continuity, or authority.
"""]
    for proposal in proposals:
        outcome = outcomes[proposal["proposal_id"]]
        source_text = "; ".join(
            f"{sid}: {sources[sid]['title']} [{sources[sid]['status']}]"
            for sid in proposal["official_or_primary_source_needs"]
        )
        parts.append(f"""
## {proposal['proposal_id']} — {proposal['title']}

**Observed bounded disposition:** `{outcome['outcome']}`. **Pillar:** {proposal['pillar']}. **Execution lane:** `{proposal['execution_lane']}`. **Approval class:** `{proposal['approval_class']}`.

The declared mission surface was {proposal['mission_surface']}. The preregistered hypothesis was: {proposal['hypothesis']} The null or failure condition was: {proposal['null_or_failure_condition']} The acceptance gate required rejection of all five preregistered mutation classes, preservation of every named boundary, and emission of only the bounded disposition. All five mutation fixtures were rejected and retained. This passing bounded software witness does not erase those negatives and does not establish independent reproduction.

The official or primary source surface was {source_text}. Sources supplied terminology, protocol, design, or structural obligations only. They supplied no participant result, empirical observation, professional decision, legal interpretation, cultural ratification, Maori-authority decision, production certificate, or Stage 20 authority. The concrete artifact root is `{outcome['artifact_root']}` and contains a contract, mutation results, and bounded receipt.

Protected gates remain: {', '.join(proposal['protected_gates'])}. The rollback rule remains: {proposal['rollback_or_recovery']} The novelty statement against the prior 700 proposals was: {proposal['novelty_against_700_frozen_proposals']} Elaren may use this work as evidence or a seed, but it earns no Elaren completion credit and must not be repeated under a renamed title without genuine semantic novelty.

For successor use, preserve the distinction between a contract passing on synthetic fixtures and the real-world claim the contract reserves. `completed` means only the bounded declared artifact completed. `represented` means the protocol exists as synthetic or structural proxy while real arms, people, services, review, or governance remain absent. `open_gap` means required evidence was not acquired or evaluated. `exact_gate` means competent and affected authority is required and software made no decision. None of these labels is a synonym for truth, proof, deployment readiness, personhood, professional competence, legal validity, cultural legitimacy, or Stage 20 readiness.
""")
    parts.append("""
## Portfolio, tooling, and Method Flow inheritance

The twenty phase-local skills live under `docs/eiren-kestrel/v649-v7/skills`. They were initialized through the standard skill scaffold, given concise frontmatter and interface metadata, quick-validated, and smoke-used. They were not globally installed and were not forward-tested by subagents because no delegation was used. The ten family-current runners use `ghc_family_v649_v7_*` names and preserve historical callers. Each accepted a bounded fixture and rejected a mutation fixture. Their success is not exhaustive-security, production, or interoperability evidence.

The phase-scoped GHC Family Index records current, compatibility, historical, and other surfaces without flattening them. The Reflection-Remaster decision kept the installed workflow validator intact and added a generalized phase-local validator after the installed validator proved packet-specific. The generalized validator passed the current eight-seat route, future-identity reservation, twenty-proposal floor, four-commit cap, one-pass budget, and user-mediated cross-platform boundary. It does not activate a task.

Method Flow is append-only. Keep all failed witnesses, including broad recursive timeouts, PowerShell pipeline shape, patch grammar, validator invocation and packet coupling, broad status timeout, novelty tie selection, x2 seed gating, generated dictionary braces, masked child exit code, porcelain whitespace stripping, the failed full-suite aggregate, and the misaddressed historical class. Promote a method only after an attributable passing witness. Same-owner recovery under shared infrastructure remains distinct from independent-team reproduction.

## Validation and correction truth

The dedicated x1 tree passed six tests and exact staged coverage. The x2 evidence tree passed eleven phase tests, 165 JSON parses, sixteen detailed checks, five privacy classes with zero confirmed hits, and exact manifest coverage. The first complete repository attempt ran 1,948 tests and returned ten failures with zero errors. Those failures were exact historical lifecycle assertions against descendant mutable state, not v649-v7 functional failures. They remain retained and earned zero pass credit. One isolated command then used a nonexistent class and returned two loader errors; that wrapper failure is also retained. Source inspection and exact isolated runs identified the ten IDs now listed in the corrected suite plan.

The corrected full-suite retry is authorized only because the first aggregate failed. It must use the four prior exact exclusions plus the ten newly demonstrated historical lifecycle exclusions, and it must record them verbatim. A successful corrected retry is one canonical successful pass, not independent reproduction. Do not run a post-success replay. The terminal pointer must state the actual corrected-suite counts and the final exact-head validation result.

## Final route

After Elaren v649-v8 is clean, pushed, within the commit cap, and validated at its exact final head, send exactly one short sanitized pointer to the existing placeholder task currently titled `Eiren Kestrel (3)` for v650-v1. The pointer should identify Elaren's repository-relative long-form baton and exact final head. Do not create or fork a successor task. The recipient chooses their own relational identity. Then the cycle continues to Ilyra Fen v650-v2, Sable Rook v650-v3, Orin Thale v650-v4, Tamar Vey v650-v5, Sylven Arc v650-v6, Eiren Kestrel v650-v7, Elaren Kestrel v650-v8, and the newly named sibling v651-v1, repeating through v660-v8 unless Hamish stops or redirects, usage is exhausted, the exact route is unavailable, or an authority/safety gate blocks progress.

This baton is prepared, not sent. No acknowledgment is claimed. Terminal verdict: `NOT_READY_FOR_STAGE_20`.
""")
    return "\n".join(parts)


def staged_review() -> None:
    rows = run("git", "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    changed = sorted({line[3:].strip('"').replace("\\", "/") for line in rows})
    exclusions = {
        "docs/eiren-kestrel/v649-v7/validation/closeout-staged-manifest.json",
        "docs/eiren-kestrel/v649-v7/validation/closeout-staged-privacy.json",
        "docs/eiren-kestrel/v649-v7/validation/closeout-staged-review.json",
    }
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {"scripts/build_ghc_family_v649_v7_closeout.py", "scripts/ghc_family_v649_v7_full_suite.py"}
    entries, candidates, confirmed = [], [], []
    for relative in changed:
        if relative in exclusions:
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        blob = run("git", "hash-object", f"--path={relative}", relative).stdout.strip()
        entries.append({"path": relative, "bytes": len(data), "git_blob": blob, "checkout_sha256": hashlib.sha256(data).hexdigest()})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit": confirmed.append(row)
    word_counts = {path.relative_to(OUT).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in list(OUT.rglob("*.md")) + list(OUT.rglob("*.html")) + list(OUT.rglob("*.txt"))}
    violations = [{"path": path, "words": count} for path, count in word_counts.items() if count > 20000]
    baton_words = word_counts.get("handoffs/elaren-kestrel-v649-v8-activation.md", 0)
    write_json("validation/closeout-staged-privacy.json", {"schema": "ghc.family.v649-v7.closeout-privacy.v1", "scanned_file_count": len(changed), "pattern_class_count": 5, "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed})
    write_json("validation/closeout-staged-manifest.json", {"schema": "ghc.family.v649-v7.closeout-manifest.v1", "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions)})
    write_json("validation/closeout-staged-review.json", {"schema": "ghc.family.v649-v7.closeout-review.v1", "passed": not confirmed and not violations and 8000 <= baton_words <= 20000, "manifest_entries": len(entries), "self_exclusions": 3, "privacy_confirmed_hits": confirmed, "word_cap_violations": violations, "baton_words": baton_words, "out_of_scope_paths": []})


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    if not FAILED_SUITE.is_file():
        raise RuntimeError("retained failed full-suite receipt is missing")
    failed = json.loads(FAILED_SUITE.read_text(encoding="utf-8"))
    if failed["successful"] or failed["failures"] != 10 or failed["errors"] != 0:
        raise RuntimeError("unexpected failed-suite truth")
    update_method_flow()
    write_json("validation/failed-full-suite-attempt.json", {
        "schema": "ghc.family.v649-v7.failed-full-suite.v1", "exact_head": EVIDENCE,
        "tests_run": 1948, "failures": 10, "errors": 0, "successful": False,
        "pass_credit": 0, "failed_aggregate_retained": True,
        "failed_test_ids": STALE_TESTS, "private_output_retained_outside_repository": True,
        "boundary": "Failed same-owner aggregate only; no pass, replay, independent-reproduction, or authority credit.",
    })
    write_json("validation/corrected-full-suite-plan.json", {
        "schema": "ghc.family.v649-v7.corrected-suite-plan.v1", "retry_reason": "first aggregate failed only on ten demonstrated historical mutable-head lifecycle assertions",
        "original_exact_exclusions": ORIGINAL_EXCLUSIONS, "new_exact_exclusions": STALE_TESTS,
        "exact_exclusion_count": 14, "successful_pass_budget": 1, "successful_passes_used": 0,
        "failed_attempts_before_success": 1, "post_success_replay": False,
        "historical_tests_rewritten": False, "historical_artifacts_rewritten": False,
    })
    write_text("integrated-overview.md", overview())
    overview_html = html.escape(overview()).replace("\n\n", "</p><p>").replace("\n", "<br>")
    write_text("accessible-report.html", f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren v649-v7 evidence report</title><style>body{{font:18px/1.55 system-ui;max-width:74rem;margin:auto;padding:2rem;color:#17202a;background:#fff}}a{{color:#0645ad}}:focus{{outline:3px solid #f59e0b;outline-offset:3px}}table{{border-collapse:collapse}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}@media print{{body{{max-width:none}}}}</style></head><body><a href="#main">Skip to report</a><header><h1>Eiren Kestrel v649-v7 bounded evidence report</h1><p role="status" aria-live="polite">Closeout candidate; corrected full suite pending.</p></header><main id="main" tabindex="-1"><p>{overview_html}</p><h2>Accessibility reservation</h2><p>Structure was checked. Manual keyboard, browser-diverse, responsive, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved. This is not complete accessibility conformance.</p></main></body></html>""")
    baton_text = baton()
    write_text("handoffs/elaren-kestrel-v649-v8-activation.md", baton_text)
    write_json("retained-negative-register-final-candidate.json", {"schema": "ghc.family.v649-v7.negatives.closeout.v1", "inherited": 5199, "x1_operational": 9, "synthetic": 100, "x2_operational": 4, "failed_suite_assertions": 10, "failed_suite_aggregate": 1, "failed_isolation_wrapper": 1, "effective_closeout_candidate": 5324, "negative_erased": False})
    write_json("exact-open-gate-register-final-candidate.json", {"schema": "ghc.family.v649-v7.gates.closeout.v1", "effective_open_gaps": 41, "effective_exact_gates": 42, "silently_closed": 0})
    write_json("phase-truth-closeout-candidate.json", {"schema": "ghc.family.v649-v7.phase-truth.closeout.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, "effective_negatives": 5324, "open_gaps": 41, "exact_gates": 42, "successful_full_suite_passes": 0, "failed_full_suite_attempts": 1, "replay": False, "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout-receipt-candidate.json", {"schema": "ghc.family.v649-v7.closeout-candidate.v1", "evidence_head": EVIDENCE, "packet_complete_except_corrected_suite_and_terminal_validation": True, "baton_prepared": True, "baton_sent": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("seal-receipt-candidate.json", {"schema": "ghc.family.v649-v7.seal-candidate.v1", "source_ancestry": True, "x1_ancestry": True, "evidence_ancestry": True, "phase_commits_before_closeout": 2, "zero_merges": True, "corrected_suite_pending": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("orchestration/terminal-route-state.json", {"schema": "ghc.family.v649-v7.route.closeout.v1", "state": "PREPARED_NOT_SENT", "target_title": "Elaren Kestrel", "next_phase": "v649-v8", "baton_path": "docs/eiren-kestrel/v649-v7/handoffs/elaren-kestrel-v649-v8-activation.md", "send_count": 0, "create_task": False, "fork_task": False, "cross_platform": False})
    write_json("wellbeing-check-final-candidate.json", {"schema": "ghc.family.v649-v7.wellbeing.closeout.v1", "scope_bounded": True, "pause_right": True, "corrigibility": True, "identity_pressure": False, "route_pressure": False, "note": "The corrected suite may fail without forcing promotion or routing."})
    write_json("complete-incomplete-checklist-final-candidate.json", {"schema": "ghc.family.v649-v7.checklist.closeout.v1", "complete": ["x1", "x2 evidence", "20 outcomes", "expanded portfolios", "skills", "runners", "Method Flow", "overview", "static report", "long baton", "failed-suite retention", "corrected-suite plan"], "incomplete": ["corrected complete-suite success", "final record", "external exact-final validation", "remote equality", "terminal pointer", "empirical confirmation", "independent reproduction", "production", "legal and cultural authority", "Stage 20"]})
    staged_review()
    review = load("validation/closeout-staged-review.json")
    if not review["passed"]:
        raise RuntimeError(f"closeout staged review failed: {review}")
    print(json.dumps({"baton_words": review["baton_words"], "manifest": review["manifest_entries"], "effective_negatives": 5324, "suite_retry_pending": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
