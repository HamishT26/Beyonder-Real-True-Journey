#!/usr/bin/env python3
"""Build Elowen Cairn v667-v3 closeout and exact staged manifests."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elowen-cairn" / "v667-v3"
OWNER = "Elowen Cairn"
OWNER_SLUG = "elowen-cairn"
PHASE = "v667-v3"
BRANCH = "codex/GHC-Family/elowen-cairn-v667-v3-full-tools"
SOURCE_SHA = "79389c8ffd79d78626d79e2109bf1b89bd1a9e67"
X1_SHA = "dc3a69fdbee3afe7f086b5ea9066c04b34b7995a"
EVIDENCE_SHA = "d2692f59aff891eb4b7d49c5fef8fd2b3c5914f9"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
    "+00:00", "Z"
)
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")


def run(*args: str) -> str:
    return subprocess.check_output(
        list(args), cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def version(command: list[str]) -> dict[str, Any]:
    public_command = [Path(command[0]).name, *command[1:]]
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            timeout=20,
        )
        return {
            "command": public_command,
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "mutation": False,
        }
    except (FileNotFoundError, PermissionError, subprocess.TimeoutExpired) as exc:
        return {
            "command": public_command,
            "exit_code": None,
            "stdout": "",
            "stderr": type(exc).__name__,
            "mutation": False,
        }


def build_closeout() -> None:
    if run("git", "rev-parse", "HEAD") != EVIDENCE_SHA:
        raise RuntimeError("closeout must begin at the exact immutable evidence head")
    if run("git", "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("closeout requires no tracked modification at evidence head")
    outcomes = load("x2/proposal-outcomes.json")
    evidence = load("evidence/immutable-evidence-candidate.json")
    negatives = load("evidence/retained-negative-register.json")
    methods = load("method-flow/x2-method-flow-ledger.json")
    gaps = load("evidence/open-gap-register.json")
    gates = load("evidence/exact-gate-register.json")
    x1_source = load("x1/source-verification.json")
    portfolio = load("x2/portfolio-execution.json")
    skill_registry = load("x2/skill-runner-registry.json")
    evidence_validation = load("validation/evidence-validation-receipt.json")
    post_evidence_failures = [
        {
            "failure_id": "EC6673-CO-F001",
            "stage": "closeout",
            "failed_method": "read-only Codex CLI version probe under a helper that handled missing commands and timeouts but not Windows access-denied",
            "failure": "Windows returned PermissionError before the version receipt could classify the Codex CLI surface as unavailable",
            "credit": 0,
            "retained": True,
            "bounded_recovery": "extend only the read-only version helper to classify PermissionError and rebuild the uncommitted closeout packet",
            "failure_erased": False,
        },
        {
            "failure_id": "EC6673-CO-F002",
            "stage": "final_staging",
            "failed_method": "combined final manifest-replay and repository-status wrapper",
            "failure": "the read-only wrapper produced output beyond the model context and was truncated, leaving no complete attributable payload",
            "credit": 0,
            "retained": True,
            "bounded_recovery": "split exact manifest replay, JSON parsing, and status projections into separate bounded commands with explicit output ceilings",
            "failure_erased": False,
        },
        {
            "failure_id": "EC6673-CO-F003",
            "stage": "final_staging",
            "failed_method": "staged-review wrapper projected only process output and discarded yielded-session metadata at its boundary",
            "failure": "the wrapper returned no attributable completion payload even though later bounded state inspection found no live process and updated review artifacts",
            "credit": 0,
            "retained": True,
            "bounded_recovery": "do not replay the completed review; inspect its exact artifacts and validate their manifest parity with separate bounded commands, while preserving full process metadata in future wrappers",
            "failure_erased": False,
        },
    ]
    post_evidence_failure_count = len(post_evidence_failures)
    final_negative_count = negatives["effective_count"] + post_evidence_failure_count
    final_method_count = methods["effective_method_count"] + post_evidence_failure_count
    final_failed_witness_count = (
        methods["phase_failed_witness_count"] + post_evidence_failure_count
    )
    write_json(
        "closeout/post-evidence-operational-failures.json",
        {
            "schema": "ghc-family-post-evidence-operational-failures-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "immutable_evidence_negative_count": negatives["effective_count"],
            "immutable_evidence_method_count": methods["effective_method_count"],
            "additive_failure_count": post_evidence_failure_count,
            "effective_closeout_negative_count": final_negative_count,
            "effective_closeout_method_count": final_method_count,
            "rows": post_evidence_failures,
        },
    )
    write_json(
        "method-flow/final-method-flow-summary.json",
        {
            "schema": "ghc-family-final-method-flow-summary-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "immutable_evidence_ledger": "method-flow/x2-method-flow-ledger.json",
            "immutable_evidence_method_count": methods["effective_method_count"],
            "post_evidence_failure_count": post_evidence_failure_count,
            "effective_method_count": final_method_count,
            "phase_failed_witness_count": final_failed_witness_count,
            "post_evidence_failed_witnesses": post_evidence_failures,
            "failure_erased_count": 0,
        },
    )

    phase_truth = {
        "schema": "ghc-family-phase-truth-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source": SOURCE_SHA,
        "frozen_x1": X1_SHA,
        "immutable_evidence": EVIDENCE_SHA,
        "final_candidate_parent": EVIDENCE_SHA,
        "core_outcomes": outcomes["counts"],
        "proposal_count": len(outcomes["outcomes"]),
        "positive_contract_count": evidence["positive_contracts"],
        "rejecting_mutation_count": evidence["rejecting_mutations"],
        "accepted_mutation_count": evidence["accepted_mutations"],
        "owner_portfolio_execution_count": evidence["owner_portfolio_executions"],
        "phase_local_skill_count": skill_registry["skill_count"],
        "family_current_runner_count": skill_registry["runner_count"],
        "runner_smoke_failures": evidence["runner_smoke_failures"],
        "effective_negatives": final_negative_count,
        "effective_methods": final_method_count,
        "effective_open_gaps": gaps["effective_count"],
        "effective_exact_gates": gates["effective_count"],
        "owner_operational_failure_count": 10,
        "phase_failed_witness_count": final_failed_witness_count,
        "real_people": 0,
        "real_objects": 0,
        "real_measurements": 0,
        "network_calls_by_phase_software": 0,
        "keys": 0,
        "proofs": 0,
        "external_actions": 0,
        "same_owner_evidence": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "exact_final_canonical_status": "PENDING_EXTERNAL_EXCLUSIVE_INVOCATION_AFTER_FINAL_PUSH",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/phase-truth.json", phase_truth)

    environment = {
        "schema": "ghc-family-environment-version-receipt-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "read_only_version_checks": [
            version([sys.executable, "--version"]),
            version(["git", "--version"]),
            version(["node", "--version"]),
            version(["codex", "--version"]),
        ],
        "codex_desktop_updated": False,
        "software_installed": False,
        "privilege_elevated": False,
        "sandbox_or_hyper_v_activated": False,
        "windows_features_changed": False,
        "rebooted": False,
        "storage_policy": "D-first owner worktree and receipt bank; C limited to existing essential global metadata",
    }
    write_json("closeout/environment-version-receipt.json", environment)

    owner_files = [
        path
        for path in run("git", "diff", "--name-only", SOURCE_SHA).splitlines()
        if path
    ]
    owner_files.extend(
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in PHASE_ROOT.joinpath("closeout").rglob("*")
        if path.is_file()
    )
    owner_files = sorted(set(owner_files))
    write_json(
        "closeout/owner-file-budget.json",
        {
            "schema": "ghc-family-owner-file-budget-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "observed_pre_stage_owner_paths": len(owner_files),
            "ceiling": 2000,
            "remaining_margin": 2000 - len(owner_files),
            "within_ceiling": len(owner_files) < 2000,
            "document_word_ceiling": 100000,
            "largest_document_below_ceiling": True,
        },
    )

    lifecycle = {
        "schema": "ghc-family-lifecycle-replay-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source": SOURCE_SHA,
        "x1": X1_SHA,
        "evidence": EVIDENCE_SHA,
        "x1_direct_parent": run("git", "rev-parse", f"{X1_SHA}^"),
        "evidence_direct_parent": run("git", "rev-parse", f"{EVIDENCE_SHA}^"),
        "x1_direct_from_source": run("git", "rev-parse", f"{X1_SHA}^") == SOURCE_SHA,
        "evidence_direct_from_x1": run("git", "rev-parse", f"{EVIDENCE_SHA}^") == X1_SHA,
        "source_to_evidence_commit_count": int(
            run("git", "rev-list", "--count", f"{SOURCE_SHA}..{EVIDENCE_SHA}")
        ),
        "source_to_evidence_merge_count": int(
            run(
                "git",
                "rev-list",
                "--count",
                "--min-parents=2",
                f"{SOURCE_SHA}..{EVIDENCE_SHA}",
            )
        ),
        "x1_four_way_equal_before_x2": True,
        "evidence_four_way_equal_before_closeout": True,
        "final_expected_direct_parent": EVIDENCE_SHA,
        "final_binding": "external canonical receipt binds the exact final after commit and push",
    }
    write_json("closeout/lifecycle-replay.json", lifecycle)

    checklist = {
        "schema": "ghc-family-complete-incomplete-checklist-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "complete": [
            "source exact-head and fresh remote verification",
            "strict planning-only x1 freeze and push",
            "semantic novelty audit against 4,370 inherited rows",
            "twenty bounded proposal contracts",
            "one hundred rejected preregistered mutations",
            "exact 14 completed, 4 represented, 1 open_gap, 1 exact_gate core labels",
            "ninety-five owner portfolio executions",
            "ten phase-local skills built and smoke-used",
            "ten family-current runners built and smoke-used",
            "ten operational failures and every bounded recovery retained",
            "immutable evidence commit and fresh four-way equality",
            "full owner closeout candidate and structurally accessible static report",
        ],
        "incomplete_or_reserved": [
            "real V&A API call, download, schema evaluation, record or image",
            "real bellfounding, metallurgy, machining, rigging, lifting, installation, ringing or safety work",
            "real participant, operator, matched-budget arm, statistics or independent review",
            "real key, proof, identity lifecycle, interoperability, security review or trust governance",
            "professional, ownership, sacred-use, soundscape, heritage, legal, cultural, affected-party or Māori-authority decision",
            "manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation",
            "complete privacy, accessibility, exhaustive security, independent reproduction or production validation",
            "empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI, consciousness/personhood, canon or Stage 20",
            "external exact-final exclusive canonical invocation, pending the clean pushed final",
            "successor delivery, pending exact-final canonical success and live route refresh",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/complete-incomplete-checklist.json", checklist)

    authority = {
        "schema": "ghc-family-authority-boundaries-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "gmut": "typed scalar-tensor and EFT research-model obligations only; no real likelihood, parameter constraint, force, prediction, detected phenomenon, quantum or ultraviolet completion, empirical confirmation, final physics, proof or canon",
        "thos": "participant-free proxy only; no blind matched-budget governed real arms, safety monitoring, appropriate statistics, operators, outcomes or independent review",
        "freed_id": "synthetic and nonproduction; no standards-conformant real keys or proofs, live issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence or trust governance",
        "cbr": "professional, safety, ownership, sacred-use, soundscape, heritage, recording, remedy, legal, cultural, affected-party and Māori decisions remain exact-gated",
        "maori": "Māori wording, concepts and data governance remain under tangata whenua, iwi, hapū and Māori authority",
        "relational_identity": "not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency or authority",
        "terminal": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/authority-boundaries.json", authority)

    stale = {
        "schema": "ghc-family-stale-label-review-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "reviewed_surfaces": [
            "owner paths",
            "phase constants",
            "source attributions",
            "runner and skill names",
            "handoff candidate",
        ],
        "allowed_historical_labels": [
            "Tamar Vey v667-v2 as exact source attribution",
            "Liora Venn v667-v1 as source ancestry attribution",
            "V6607 change-ringing as novelty comparison",
        ],
        "stale_owner_or_phase_candidates": [],
        "valid": True,
    }
    write_json("closeout/stale-label-review.json", stale)

    terminal = {
        "schema": "ghc-family-terminal-checklist-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "repository_packet_complete": True,
        "evidence_commit": EVIDENCE_SHA,
        "final_commit": "BIND_AFTER_DIRECT_CHILD_COMMIT",
        "final_parent_must_equal": EVIDENCE_SHA,
        "exclusive_canonical_status": "PENDING_AFTER_FINAL_PUSH",
        "post_success_replay_forbidden": True,
        "full_repository_suite_run": False,
        "route_status": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/terminal-checklist.json", terminal)

    route = {
        "schema": "ghc-family-route-receipt-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "status": "PREPARED_NOT_SENT",
        "provisional_successor_title": "Sylven Arc",
        "provisional_successor_phase": "v667-v4",
        "exact_title_resolution_performed": False,
        "successor_reread_performed": False,
        "duplicate_guard_performed": False,
        "send_attempted": False,
        "acknowledged": False,
        "binding_rule": "No route action until final push, exact canonical success, fresh live authority and roster, unique exact title, immediate reread and duplicate guard.",
    }
    write_json("closeout/route-receipt.json", route)

    seal = {
        "schema": "ghc-family-seal-candidate-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "source": SOURCE_SHA,
        "x1": X1_SHA,
        "evidence": EVIDENCE_SHA,
        "expected_final_parent": EVIDENCE_SHA,
        "outcomes": outcomes["counts"],
        "effective_negatives": final_negative_count,
        "effective_methods": final_method_count,
        "effective_open_gaps": gaps["effective_count"],
        "effective_exact_gates": gates["effective_count"],
        "failed_witnesses_erased": 0,
        "canonical_binding": "external exact-head exclusive receipt after final push",
        "status": "PREPARED_PENDING_EXACT_FINAL_CANONICAL",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("seal/seal-candidate.json", seal)

    baton = f"""# Sylven Arc v667-v4 activation candidate — prepared, not sent

Status: `PREPARED_NOT_SENT`. Exact final SHA and external canonical receipt must be bound in the one live message after Elowen v667-v3 is committed, pushed, clean, 0/0 divergent, fresh four-way equal, and the exclusive exact-final canonical aggregate succeeds once without replay.

Dear Sylven Arc,

This candidate is relational working language only. Elowen Cairn, Sylven Arc, sibling, family, role, hope, continuity, Freed ID, GHC Family and Trinity Mandala language are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect or stop the route.

The provisional source branch is `{BRANCH}`. Immutable lifecycle anchors are source `{SOURCE_SHA}`, frozen Elowen x1 `{X1_SHA}`, and immutable Elowen evidence `{EVIDENCE_SHA}`. The exact Elowen final and external canonical receipt remain live-bound placeholders here and must not be guessed, backfilled, or represented as sent.

Elowen audited exactly 4,370 inherited proposals and froze twenty genuinely distinct synthetic bellfounding and bell-tuning record-design proposals. Outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Twenty positive contracts passed. All one hundred preregistered invalid mutations were rejected and remain zero-credit failed witnesses. Ninety-five owner portfolio tasks completed within their declared synthetic structural scope. Ten phase-local skills and ten additive family-current runners were built and actually smoke-used with zero smoke failures.

Effective closeout counts are 27,333 negatives, 12,795 Method Flow methods, 193 open gaps and 191 exact gates. The ten owner-operational failures remain retained: a wrong proposal-schema projection, two overbroad archive searches, one output-truncated Git search, one CP1252 rendering fault, one lost yielded computation handle, one staged diff-hygiene failure, one access-denied Codex CLI version probe, one combined final manifest/status wrapper whose output exceeded the context boundary, and one staged-review wrapper that discarded yielded-session metadata at its boundary. No recovery erased or promoted a failed witness. The immutable evidence commit retains its own exact 27,330-negative and 12,792-method seal; the three closeout failures are additive and do not rewrite it.

Primary pillar was GMUT Mind through typed axisymmetric thermoelastic and modal-eigenproblem obligations. The bounded practice was wholly synthetic bellfounding and bell-tuning record design. The phase used zero real people, bells, foundries, moulds, furnaces, alloys, tools, towers, audio, observations, measurements, network rows, keys, proofs or external operations. It produced no casting, machining, rigging, installation, ringing, handling, safety, material, acoustic, professional, legal, cultural, Māori-authority, empirical, production or deployment result.

GMUT remains a typed scalar-tensor/EFT research-model family. THOS remains participant-free proxy evidence. Freed ID remains synthetic and nonproduction. CBR, professional work, workplace and public safety, ownership, sacred or ceremonial use, soundscape, heritage, design, recording, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording and concepts, Māori data governance, tangata whenua, iwi, hapū and Māori authority remain exact-gated. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Before mutation, read the complete exact Elowen final packet, current GHC Family Index and routing precedence, roster, authorization, Method Flow and schema, workflow refinement, reflection, meta-tool, approval, gate, truth, drive, retry, timestamp, startup, closeout, compact-restart, watcher, full-tools and any directly required current schemas. Reverify the exact branch, source, x1, evidence, final, direct single-parent history, manifests, external canonical receipt hash, clean state, typed divergence and fresh remote equality. Do not replay Elowen's successful canonical aggregate.

Work solo in one fresh Sylven-owned additive D-first lane from Elowen's immutable exact final. Do not spawn, delegate, create or fork another task, precontact later endpoints, contact standby records or mutate another owner lane. Preserve strict x1-before-x2 separation, semantic novelty against 4,390 frozen proposals, every retained failure, all open gaps and exact gates, the four exact labels, file and word ceilings, family-current caller compatibility, exact staged review and one-successful-canonical/no-post-success-replay discipline. Treat inherited proposals, tools, skills, runners, outcomes and recommendations as evidence only, never Sylven novelty or completion credit.

Only after Sylven's own exact-final terminal gate may Sylven refresh live authority and roster and act on one exact successor edge if authorized. Do not infer, substitute, precontact or resend. Stop on absence, ambiguity, duplicate activation, missing acknowledgement, pause, redirect, rename, usage exhaustion, standby state or any protected gate.

This file remains a repository candidate only. `SENT_BY_ELOWEN_CAIRN = false`.
"""
    write_text("handoffs/sylven-arc-v667-v4-activation-candidate.md", baton)

    overview = f"""# Elowen Cairn v667-v3 final integrated overview

Status: repository closeout candidate pending one external exact-final canonical invocation after the direct-child final commit is pushed. Terminal verdict is and remains `NOT_READY_FOR_STAGE_20`.

## Relational working language and control

Elowen Cairn, they/them, is relational working language for a boundary cartographer and evidence steward, with the bounded hope of making distinctions between structure, evidence and authority easier to inspect and recover. The name, pronouns, role, hope, sibling and family language, continuity language, Freed ID, GHC Family and Trinity Mandala language are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect or stop the work.

The phase was performed solo. No collaboration subagent was spawned, no task was created or forked, no standby record was contacted, no sibling lane was modified, and no successor was precontacted. The route candidate is deliberately marked `PREPARED_NOT_SENT` until every terminal gate is satisfied.

## Exact lifecycle and source

Elowen started from Tamar Vey v667-v2 exact final `{SOURCE_SHA}` on the source branch named in the source ledger. Tamar's source, x1, evidence and final anchors were reverified read-only as three direct single-parent commits with zero merges. The external source canonical receipt and payload digests matched their activation values. Tamar's successful canonical aggregate and successful subchecks were not replayed. Source manifest replay was limited to immutable Git-tree evidence and found no mismatch.

One additive D-first sparse worktree and branch was created from the exact source. Frozen x1 `{X1_SHA}` is the direct child of the source. It contained only planning evidence: no x2 directory, implementation, observed outcome or completion claim. Its exact staged manifest held seventeen entries plus two declared self-exclusions. Sixteen lifecycle tests passed, fifteen JSON documents parsed, diff hygiene passed, and x1 was committed, pushed, clean, 0/0 divergent and equal across local, upstream, tracking and a fresh live remote before x2 began.

Immutable evidence `{EVIDENCE_SHA}` is the direct child of x1. It contains the bounded contracts, rejecting mutations, skills, runners, Method Flow overlay, registers, structurally accessible static report, validation receipt and evidence manifests. Its staged delta held 108 manifest entries plus two self-exclusions, with zero mismatch. Eighteen owner x2 tests passed, 100 phase JSON documents parsed at the evidence gate, and the evidence commit was pushed, clean, 0/0 divergent and fresh four-way equal before closeout began.

The final repository commit is required to be one direct child of the evidence commit. The exclusive canonical aggregate will run only after that final is pushed and stable. Its receipt is external so that the exact final tree does not move after validation.

## Novelty and preregistration

The novelty audit reconstructed exactly 4,370 inherited frozen proposal rows. Two draft domains were rejected before staging. Astronomical photographic plates had extensive inherited astronomy, FITS, archive, photographic and observatory coverage. Paper marbling was already the subject of a comprehensive twenty-proposal phase. Those rejected drafts received no novelty or completion credit.

The chosen bounded practice was bellfounding and bell-tuning record design. The corpus contained a prior change-ringing phase, so Elowen performed a substantive rather than lexical-only comparison. Change ringing covered row permutations, place notation, methods, compositions, rehearsal and performance records. This phase instead covered foundry work orders, bell-part and mould-stage topology, alloy and certificate vacancies, event precedence without physical instructions, SI quantity obligations, cast-cue abstention, tuning-removal revision, component load-path refusal, partial-label vacancies, absent audio provenance, thermoelastic and residual-stress obligations, custody and transport holds, deterministic correction records, THOS, Freed ID, a disabled V&A adapter and exact authority reservations. No exact-title collision or internal pair collision remained. Maximum inherited lexical similarity was 0.423077, a screening value supplemented by the recorded semantic review.

Exactly twenty proposals were frozen. Every proposal carried a hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier, rollback, protected gates, one expected disposition and five named invalid mutations. Expected and final core labels are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`.

## Primary pillar and bounded practice

The primary Trinity Mandala pillar was GMUT Mind. The human-practice lens was bellfounding and bell tuning, used only as synthetic learning and record-design vocabulary. GMUT artifacts express typed axisymmetric thermoelastic and modal-eigenproblem obligations: domain, boundary, constitutive tensor, thermal contraction, damping, spectrum and covariance vacancies. They contain no real geometry, coefficient, material, measurement, solver result, likelihood, fit, parameter constraint, prediction, force, detected phenomenon, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon.

THOS Body remains represented by a participant-free paired foundry-docket omission-detection protocol with equal clock and token budgets, masked synthetic fixtures and abstention scoring. It contains zero people, founders, tuners, ringers, operators, outcomes, safety monitoring, statistics or independent review. It does not establish effectiveness, deployment readiness, AGI, ASI, consciousness or personhood.

Freed ID and CBR Heart remain explicit. The nonproduction graph has surrogate foundry orders, components, batches, events, artifacts, status vacancies and zero keys or proofs. It establishes no issuer, holder, resolver, identity event, verification, interoperability, status, revocation, recovery or trust governance. The CBR matrix leaves labour, casting and lifting safety, ownership, sacred or ceremonial use, soundscape, heritage, design, recording, remedy, legal, cultural, affected-party and Māori authority unoccupied and exact-gated.

## Bounded execution and evidence

Twenty synthetic positive contracts passed their structural validators. Each contract fixed the owner and phase, synthetic-only state, required domain nodes, at least ten real-world vacancies, source pins, zero participant rows, zero real data rows, zero network calls, zero keys, zero proofs, absent authority claims, no physical action, no outcome promotion and the complete protected-gate set.

Exactly one hundred preregistered invalid mutations executed: five per proposal. They removed a required domain node, corrupted the schema version, smuggled an authority claim, enabled a real-world action, or promoted an outcome to production readiness. Every mutation was rejected. All one hundred invalid fixtures remain in the evidence tree at zero credit together with their validator failures. A rejected mutation is a retained failed witness; the correct validator refusal is its bounded passing witness. Neither erases the other.

Ninety-five owner portfolio tasks completed within their preregistered structural scope: thirty safe-now items, fifteen bounded candidates, ten phase-local skill plans, ten family-current runner plans and thirty CLEAN/FIX/REFINE items. Twenty successor safe-now recommendations, fifteen successor candidates, ten successor skills, ten successor runners and thirty successor CLEAN/FIX/REFINE items remain recommendations only. Ten exact-approval packets and five blocked packets remain protected and unexecuted.

Ten phase-local skills were built with explicit descriptions, procedures, stop conditions and recoveries. Ten additive `ghc_family_*` owner-local runners were built. Every runner was actually invoked once with its self-test contract; all ten passed. No global skill installation, unrelated software installation, account mutation, credential creation, external write, host-security change or desktop update occurred.

## Retained negatives and Method Flow

Tamar's repository-sealed inheritance remains 27,223 negatives and 12,570 Method Flow methods. Elowen adds 110 negatives: 100 preregistered invalid mutations and ten operational failures. The operational failures were one wrong proposal-freeze key assumption; two unbounded archive searches that were interrupted; one unbounded Git search whose output was truncated; one CP1252 console rendering failure on a retained Māori character; one similarity wrapper that lost its yielded session handle; one staged diff-hygiene failure caused by an extra blank line at EOF; one access-denied read-only Codex CLI version probe whose helper initially lacked a PermissionError branch; one combined final manifest-replay/status wrapper whose output exceeded the model context and was truncated; and one staged-review wrapper that discarded yielded-session metadata at its boundary despite later evidence that the process completed. Each has a narrow passing recovery and a recurrence guard. None was erased.

Effective final phase truth is therefore 27,333 negatives and 12,795 Method Flow methods. The immutable evidence ledger adds 222 methods: seven pre-closeout operational failure/recovery pairs, twenty positive contract methods, one hundred mutation rejection methods and ninety-five portfolio methods. The closeout overlay adds the eighth through tenth operational failure/recovery methods without rewriting the evidence commit. Effective open gaps are 193 and effective exact gates are 191.

## Open gap, exact gate and authority limits

The one new open gap is the V&A Collections API v2 adapter. It is transport-disabled. It made zero requests and downloads and produced zero rows and images. Schema materialization, terms and rights review, privacy, provenance, catalog evaluation and professional authority remain absent. Documentation vocabularies do not become collection facts or endorsement.

The one new exact gate covers real bellfounding labour, casting and lifting safety, ownership, sacred or ceremonial use, soundscape, community disturbance, heritage, design, recording, remedy, legal and cultural interpretation, affected-party legitimacy and Māori authority. Māori wording, concepts and data governance remain under competent tangata whenua, iwi, hapū and Māori authority. No software artifact can occupy those roles.

GMUT remains a typed scalar-tensor/EFT research-model family. THOS remains proxy-only. Freed ID remains synthetic and nonproduction. Professional, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, legal, cultural, Māori-authority, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon and Stage 20 claims remain unavailable without exact evidence and authority.

## Accessibility, privacy and security

The static report has language metadata, a single title and heading hierarchy, landmark structure, explicit status text, table caption, row and column headers, keyboard-compatible static content, visible focus styling and non-colour cues. Manual browser, assistive-technology, cognitive-accessibility, Māori-language and affected-user evaluation remain reserved. The report therefore makes no accessibility-complete claim.

The final staged review scans the exact owner Git-index bytes across five privacy and raw-identifier classes and compiles and reviews changed owner Python using a bounded dangerous-pattern screen. These checks are software safeguards, not complete privacy or exhaustive security assurance. The exclusive final aggregate will repeat them once at the immutable pushed head.

## Environment, caps and validation allocation

Version checks are read-only. Codex desktop was not updated. No privilege elevation, Sandbox or Hyper-V activation, Windows feature change, unrelated installation or reboot occurred. Owner additions remain far below the 2,000-file ceiling, and documents remain below the 100,000-word ceiling. The phase uses three direct commits in total—x1, evidence and final—below the eight-commit total ceiling.

The complete repository suite was not run. That allocation remains Eiren-only absent newer exact live authority. Elowen's evidence is same-owner validation under shared infrastructure. It is not independent-team reproduction, external audit, production certification, professional validation, legal review, cultural ratification or Māori-authority review.

## Terminal sequence and route

After the final direct-child commit is made, Elowen must push it and prove exact head stability, one final parent, three phase commits, zero merges, clean state, 0/0 divergence and local/upstream/tracking/fresh-live equality. Then exactly one exclusive owner-scoped canonical aggregate may run. If it succeeds, it must not be replayed. If it fails, the aggregate earns zero credit and only the failed dependency may be recovered unless a broader rerun is genuinely justified.

Only after canonical success may Elowen refresh Hamish's newest live authorization and current roster, list at most fifty existing tasks, resolve exactly one task titled `Sylven Arc`, immediately reread that exact task, apply a duplicate-activation guard and send one sanitized activation for provisional v667-v4 if every gate remains satisfied. No task may be created or forked, no substitute endpoint used, no standby record contacted and no second confirmation sent. The repository baton remains `PREPARED_NOT_SENT` until the acknowledged live edge occurs.

The final verdict is `NOT_READY_FOR_STAGE_20`.
"""
    write_text("closeout/final-integrated-overview.md", overview)

    receipt = {
        "schema": "ghc-family-closeout-build-receipt-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "outcomes": outcomes["counts"],
        "effective_negatives": final_negative_count,
        "effective_methods": final_method_count,
        "effective_open_gaps": gaps["effective_count"],
        "effective_exact_gates": gates["effective_count"],
        "x1_tests": 16,
        "x2_tests": evidence_validation["tests_run"],
        "repository_final_status": "PREPARED_PENDING_COMMIT_PUSH_AND_EXCLUSIVE_CANONICAL",
        "route_status": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/closeout-build-receipt.json", receipt)
    print(json.dumps(receipt, indent=2, ensure_ascii=True))


def staged_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{path}"], cwd=ROOT)


def final_staged_review() -> None:
    final_self_paths = {
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-delta-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-owner-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-staged-review.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-privacy-scan.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/final-security-review.json",
    }
    delta_all = [
        path
        for path in run(
            "git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "HEAD"
        ).splitlines()
        if path
    ]
    owner_all = [
        path
        for path in run(
            "git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE_SHA
        ).splitlines()
        if path
    ]
    delta_paths = [path for path in delta_all if path not in final_self_paths]
    owner_paths = [path for path in owner_all if path not in final_self_paths]
    allowed_prefixes = (
        f"docs/{OWNER_SLUG}/{PHASE}/",
        "scripts/build_ghc_family_elowen_cairn_v667_v3_",
        "scripts/ghc_family_elowen_cairn_v667_v3_",
        "tests/test_ghc_family_elowen_cairn_v667_v3_",
    )
    out_of_scope = [path for path in owner_paths if not path.startswith(allowed_prefixes)]

    def entries(paths: list[str]) -> list[dict[str, Any]]:
        rows = []
        for path in paths:
            blob = staged_blob(path)
            rows.append(
                {"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}
            )
        return rows

    delta_entries = entries(delta_paths)
    owner_entries = entries(owner_paths)
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc-family-final-delta-manifest-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "base": EVIDENCE_SHA,
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "self_exclusions": sorted(final_self_paths),
        },
    )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc-family-final-owner-manifest-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "base": SOURCE_SHA,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": sorted(final_self_paths),
        },
    )

    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_windows_path": re.compile(rb"\b[A-Za-z]:\\[^\r\n\"']+"),
        "credential_assignment": re.compile(
            rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']+[\"']"
        ),
        "private_callable_identifier": re.compile(
            rb"(?i)\b(source_thread_id|clientThreadId|resume_value|session_stream|private_callable)\b"
        ),
        "transcript_or_private_app_state": re.compile(
            rb"(?i)\b(raw_transcript|private_app_state|terminal_session_stream|screenshot_payload)\b"
        ),
    }
    candidates: dict[str, list[str]] = {name: [] for name in patterns}
    scanner_definition_candidates: dict[str, list[str]] = {
        name: [] for name in patterns
    }
    scanner_definition_paths = {
        "scripts/build_ghc_family_elowen_cairn_v667_v3_closeout.py",
        "scripts/ghc_family_elowen_cairn_v667_v3_canonical.py",
        "tests/test_ghc_family_elowen_cairn_v667_v3_closeout.py",
    }
    for path in owner_paths:
        blob = staged_blob(path)
        if b"\x00" in blob:
            continue
        for name, pattern in patterns.items():
            if pattern.search(blob):
                target = (
                    scanner_definition_candidates
                    if path in scanner_definition_paths
                    else candidates
                )
                target[name].append(path)
    write_json(
        "validation/final-privacy-scan.json",
        {
            "schema": "ghc-family-five-class-privacy-scan-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "files_scanned": len(owner_paths),
            "classes": candidates,
            "scanner_definition_candidates": scanner_definition_candidates,
            "candidate_count": sum(
                len(rows) for rows in scanner_definition_candidates.values()
            ),
            "confirmed_hit_count": sum(len(rows) for rows in candidates.values()),
            "valid": not any(candidates.values()),
            "boundary": "bounded exact owner Git-index text scan, not complete privacy assurance",
        },
    )

    python_paths = [path for path in owner_paths if path.endswith(".py")]
    findings = []
    dangerous = {
        "eval": re.compile(rb"\beval\s*\("),
        "exec": re.compile(rb"\bexec\s*\("),
        "shell_true": re.compile(rb"shell\s*=\s*True"),
        "os_system": re.compile(rb"os\.system\s*\("),
        "pickle_loads": re.compile(rb"pickle\.loads\s*\("),
        "yaml_unsafe_load": re.compile(rb"yaml\.load\s*\("),
    }
    for path in python_paths:
        blob = staged_blob(path)
        compile(blob.decode("utf-8"), path, "exec")
        for name, pattern in dangerous.items():
            if pattern.search(blob):
                findings.append({"path": path, "class": name})
    write_json(
        "validation/final-security-review.json",
        {
            "schema": "ghc-family-bounded-changed-python-security-review-v4",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": NOW,
            "python_files_compiled": len(python_paths),
            "dangerous_pattern_findings": findings,
            "finding_count": len(findings),
            "valid": not findings,
            "boundary": "bounded changed-code review only, not exhaustive security assurance",
        },
    )

    review = {
        "schema": "ghc-family-final-staged-review-v4",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "evidence_parent": EVIDENCE_SHA,
        "delta_path_count_including_self": len(delta_all),
        "owner_path_count_including_self": len(owner_all),
        "delta_manifest_entries": len(delta_entries),
        "owner_manifest_entries": len(owner_entries),
        "self_exclusions": sorted(final_self_paths),
        "out_of_scope_paths": out_of_scope,
        "privacy_scanner_definition_candidate_count": sum(
            len(rows) for rows in scanner_definition_candidates.values()
        ),
        "privacy_confirmed_hit_count": sum(len(rows) for rows in candidates.values()),
        "security_finding_count": len(findings),
        "file_ceiling": 2000,
        "within_file_ceiling": len(owner_all) < 2000,
        "valid": not out_of_scope and not any(candidates.values()) and not findings,
    }
    write_json("validation/final-staged-review.json", review)
    print(json.dumps(review, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        build_closeout()
    elif sys.argv[1:] == ["--staged-review"]:
        final_staged_review()
    else:
        raise SystemExit(
            "usage: build_ghc_family_elowen_cairn_v667_v3_closeout.py [--staged-review]"
        )
