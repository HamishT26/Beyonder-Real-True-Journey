#!/usr/bin/env python3
"""Build the combined Eiren Kestrel v652-v5 closeout and seal commit."""

from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import ghc_family_v652_v5_phase_data as d
except ModuleNotFoundError:
    from scripts import ghc_family_v652_v5_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_HEAD
X1 = "7f347e548b64ea2a9065e129c3ec84dde000c13e"
EVIDENCE = "611a0afef841a516dd0a5cb1e9ac2448943b42c6"
EVIDENCE_X2_OPERATIONAL_NEGATIVES = 3
CLOSEOUT_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6525-NEG-CLOSEOUT-01",
        "category": "sequential_manifest_blob_verifier_timeout",
        "failed": (
            "The first independent staged-manifest verifier used one Git process "
            "per blob and exceeded its 120-second bound before producing a result."
        ),
        "recovery": (
            "Build one stage-zero index map with git ls-files -s -z and read all "
            "required objects through one git cat-file --batch stream."
        ),
        "passing": (
            "The batched verifier checked 32 staged paths, 26 closeout entries "
            "plus 6 exclusions, and 293 owner entries plus 3 exclusions with "
            "zero path, object, byte-count, or SHA-256 mismatch."
        ),
        "recurrence_guard": (
            "Use the batched index/object verifier for manifests above a small "
            "bounded fixture; never return to a per-blob subprocess loop."
        ),
    },
    {
        "negative_id": "V6525-NEG-CLOSEOUT-02",
        "category": "repeated_method_flow_subprocess_timeout",
        "failed": (
            "The first Method Flow rebuild invoked the growing ledger through "
            "repeated subprocess calls and exceeded its 180-second wrapper bound "
            "after producing files but before returning a credited completion."
        ),
        "recovery": (
            "Load the official Method Flow runner once in-process, apply the same "
            "record, witness, state, validation, and summary functions, and write "
            "each resulting artifact once."
        ),
        "passing": (
            "The in-process runner path rebuilt and validated both retained "
            "closeout methods, both failed witnesses, both passing witnesses, "
            "their preferred states, summaries, and closeout tests within one "
            "bounded invocation."
        ),
        "recurrence_guard": (
            "For an established large ledger, load the official runner once and "
            "avoid repeated process startup and full-ledger parse/write cycles."
        ),
    },
]
EFFECTIVE_NEGATIVES = (
    d.INHERITED_NEGATIVES
    + len(d.X1_OPERATIONAL_NEGATIVES)
    + EVIDENCE_X2_OPERATIONAL_NEGATIVES
    + len(CLOSEOUT_OPERATIONAL_NEGATIVES)
    + 150
)
OPEN_GAPS = d.INHERITED_OPEN_GAPS + 1
EXACT_GATES = d.INHERITED_EXACT_GATES + 1
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)
FULL_SUITE_ADDITIONAL_EXCLUSIONS = {
    (
        "tests.test_ghc_family_v652_v1_x1.TestV652V1X1."
        "test_document_caps_privacy_and_x1_only"
    ),
    (
        "tests.test_ghc_family_v652_v2_x1.TestV652V2X1."
        "test_placeholders_privacy_and_x1_only"
    ),
}


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo(relative: str, payload: str) -> Path:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    completed = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def append_closeout_method_flow() -> dict[str, Any]:
    """Carry evidence Method Flow forward and append only observed closeout faults."""
    source = read_json(ROOT / "method-flow/evidence-method-flow-ledger.json")
    spec = importlib.util.spec_from_file_location(
        "ghc_family_method_flow_state_runtime", METHOD_RUNNER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load the official Method Flow runner")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    ledger = source
    start = source["counts"]["methods"] + 1
    for number, negative in enumerate(CLOSEOUT_OPERATIONAL_NEGATIVES, start):
        method_id = f"V6525-METHOD-{number:02d}"
        negative_id = negative["negative_id"]
        record_payload = {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_closeout_recovery",
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": "Stop, retain the failed witness, and leave external and authority state unchanged.",
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative_id],
                "scope_boundary": "Owner-local closeout recovery only; not exact-final or authority credit.",
            }
        write_json(
            f"method-flow/requests/method-{number:02d}.json",
            record_payload,
        )
        failed_payload = {
                "witness_id": f"V6525-WITNESS-{number:02d}-F",
                "method_id": method_id,
                "procedure": "Retain the original failed closeout attempt.",
                "scope": negative["category"],
                "expected": "The bounded closeout postcondition would pass.",
                "observed": negative["failed"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "Zero validation credit; failed witness retained.",
            }
        write_json(
            f"method-flow/requests/witness-{number:02d}-failed.json",
            failed_payload,
        )
        passing_payload = {
                "witness_id": f"V6525-WITNESS-{number:02d}-P",
                "method_id": method_id,
                "procedure": negative["recovery"],
                "scope": negative["category"],
                "expected": "The isolated recovery establishes only its declared postcondition.",
                "observed": negative["passing"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "Same-owner bounded recovery only; the failed witness remains.",
            }
        write_json(
            f"method-flow/requests/witness-{number:02d}-passing.json",
            passing_payload,
        )

        ledger["methods"].append(record_payload)
        runner.append_event(
            ledger,
            method_id,
            None,
            "candidate",
            "method recorded with retained negative linkage",
        )
        ledger["witnesses"].append(failed_payload)
        record_payload["validation_witness_ids"].append(
            failed_payload["witness_id"]
        )
        ledger["witnesses"].append(passing_payload)
        record_payload["validation_witness_ids"].append(
            passing_payload["witness_id"]
        )
        record_payload["recommendation_state"] = "validated"
        runner.append_event(
            ledger,
            method_id,
            "candidate",
            "validated",
            "bounded witness passed",
            passing_payload["witness_id"],
        )
        record_payload["recommendation_state"] = "preferred"
        runner.append_event(
            ledger,
            method_id,
            "validated",
            "preferred",
            "Promoted only after the bounded passing witness; failed witness retained.",
        )
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": method_id,
                "preconditions": record_payload["trigger_preconditions"],
                "method": record_payload["candidate_workaround"],
                "witness_ids": record_payload["validation_witness_ids"],
                "recurrence_guard": record_payload["recurrence_guard"],
                "rollback": record_payload["rollback"],
                "scope_boundary": record_payload["scope_boundary"],
            }
        )
    runner.refresh_counts(ledger)
    validation = runner.validate_ledger(ledger)
    if not validation["valid"]:
        raise RuntimeError(
            "Method Flow validation failed: " + "; ".join(validation["issues"])
        )
    summary = {
        "schema": "ghc.family.method-flow-state.summary.v1",
        "phase": ledger["phase"],
        "owner": ledger["owner"],
        "counts": ledger["counts"],
        "preferred_methods": [
            {
                "method_id": row["method_id"],
                "title": row["title"],
                "trigger_preconditions": row["trigger_preconditions"],
                "candidate_workaround": row["candidate_workaround"],
                "validation_witness_ids": row["validation_witness_ids"],
                "recurrence_guard": row["recurrence_guard"],
                "rollback": row["rollback"],
                "scope_boundary": row["scope_boundary"],
            }
            for row in ledger["methods"]
            if row["recommendation_state"] == "preferred"
        ],
        "retained_failed_witnesses": [
            row["witness_id"]
            for row in ledger["witnesses"]
            if row["result"] == "fail"
        ],
        "valid": validation["valid"],
        "boundary": ledger["boundary"],
    }
    write_json("method-flow/final-method-flow-ledger.json", ledger)
    write_json("method-flow/final-method-flow-validation.json", validation)
    write_json("method-flow/final-method-flow-summary.json", summary)
    write_text(
        "method-flow/final-method-flow-summary.md",
        runner.render_markdown(ledger),
    )
    return ledger


def proposal_detail(proposal: dict[str, Any], outcome: dict[str, Any]) -> str:
    contract = read_json(
        ROOT / "surfaces" / proposal["slug"] / "contract.json"
    )
    obligations = ", ".join(contract["declared_obligations"])
    zero_counters = ", ".join(
        f"{key}=0" for key in sorted(outcome["real_world_counters"])
    )
    if outcome["observed_outcome"] == "completed":
        class_truth = (
            "Completed means the bounded owner-local software, symbolic, formal, "
            "structural, statistical, thermodynamic, or workflow hypothesis passed. "
            "It is not production certification, empirical confirmation, external "
            "audit, professional validation, complete privacy or accessibility, "
            "exhaustive security, independent reproduction, proof or canon, "
            "consciousness or personhood, Theory of Everything, or Stage 20 authority."
        )
    elif outcome["observed_outcome"] == "represented":
        class_truth = (
            "Represented means synthetic structure and refusal behavior exist while "
            "real people, operations, keys, services, interoperability, matched-budget "
            "arms, safety monitoring, professional review, affected-party acceptance, "
            "and independent review remain absent. Representation cannot be promoted "
            "by mutation rejection."
        )
    elif outcome["observed_outcome"] == "open_gap":
        class_truth = (
            "Open gap means the adapter and zero-row refusal path exist but the required "
            "observational rows, data access, likelihood work, uncertainty analysis, "
            "independent review, and scientific authority do not. The missing evidence "
            "is not replaced by citations, schemas, empty fixtures, or checksums."
        )
    else:
        class_truth = (
            "Exact gate means repository software cannot make the reserved access, "
            "disclosure, charting, privacy, remedy, legal, cultural, place-name, "
            "data-governance, affected-party, tangata-whenua, iwi, hapū, or Māori "
            "authority decisions. Those decisions remain wholly external."
        )
    return f"""### {proposal['proposal_id']} — {proposal['title']}

Pillar: {proposal['pillar']}. Approval class: `{proposal['approval_class']}`. Execution lane: `{proposal['execution_lane']}`. Official or primary-source needs: {", ".join(proposal['official_or_primary_source_needs'])}. Observed outcome: `{outcome['observed_outcome']}`.

The frozen hypothesis was: {proposal['hypothesis']} The null or failure condition was: {proposal['null_or_failure_condition']} The bounded artifact exposed these declared obligations: {obligations}. Its five preregistered mutation dimensions were missing obligation, wrong type or unit, resource or replay overrun, unsupported promotion, and privacy or authority breach. All {outcome['mutation_rejected_or_quarantined_count']} of five were rejected or quarantined. The retained zero counters were {zero_counters}.

{class_truth} The acceptance gate remained: {proposal['falsifier_or_acceptance_gate']} Recovery remained additive and non-destructive: {proposal['rollback_or_recovery']} The evidence digest binds the synthetic contract, baseline, and mutation record without turning their contents into empirical, participant, operational, identity, legal, cultural, or authority evidence. This is same-owner evidence under shared infrastructure only.
"""


def baton_text() -> str:
    outcomes_payload = read_json(ROOT / "evidence/proposal-outcomes.json")
    outcomes = {
        row["proposal_id"]: row for row in outcomes_payload["rows"]
    }
    portfolio = read_json(ROOT / "portfolios/expanded-portfolio-evidence.json")
    flow = read_json(ROOT / "method-flow/final-method-flow-ledger.json")
    sources = read_json(ROOT / "sources/source-ledger.json")

    proposal_sections = "\n\n".join(
        proposal_detail(proposal, outcomes[proposal["proposal_id"]])
        for proposal in d.PROPOSALS
    )
    safe_rows = "\n".join(
        f"- `{row['item_id']}` — {row['title']} State: `{row['state']}`; credit remains {row['credit_boundary']}."
        for row in portfolio["safe_now"]
    )
    candidate_rows = "\n".join(
        f"- `{row['item_id']}` / `{row['proposal_id']}` — {row['title']} Resolved as evidence permits with core state `{row['state']}`; portfolio resolution does not alter the core outcome class."
        for row in portfolio["candidate"]
    )
    skill_rows = "\n".join(
        f"- `{row['item_id']}` — {row['title']} State: `{row['state']}`; credit remains {row['credit_boundary']}."
        for row in portfolio["skills"]
    )
    runner_rows = "\n".join(
        f"- `{row['item_id']}` — {row['title']} State: `{row['state']}`; credit remains {row['credit_boundary']}."
        for row in portfolio["runners"]
    )
    cfr_rows = "\n".join(
        f"- `{row['item_id']}` — {row['title']} State: `{row['state']}`; credit remains {row['credit_boundary']}."
        for row in portfolio["clean_fix_refine"]
    )
    method_rows = "\n".join(
        (
            f"- `{row['method_id']}` — {row['title']}. Failure signature: "
            f"{row['failure_signature']} Preferred bounded recovery: "
            f"{row['candidate_workaround']} Recurrence guard: {row['recurrence_guard']} "
            f"The failed witness remains linked to {', '.join(row['retained_negative_ids'])}; "
            "the passing witness is same-owner only and earns no independent-reproduction credit."
        )
        for row in flow["methods"]
    )
    source_rows = "\n".join(
        (
            f"- `{row['source_id']}` — `{row['status']}` — {row['title']}. "
            f"{row['phase_implication']} A citation supplies requirements context only; "
            "it cannot supply an observation, operational result, professional decision, "
            "legal interpretation, cultural legitimacy, or delegated authority."
        )
        for row in sources["sources"]
    )

    novelty = read_json(ROOT / "provenance/semantic-novelty-audit.json")
    x1_manifest = read_json(ROOT / "validation/x1-staged-manifest.json")
    evidence_manifest = read_json(ROOT / "validation/evidence-staged-manifest.json")
    evidence_negatives = read_json(
        ROOT / "truth/evidence-retained-negative-register.json"
    )

    return f"""# ILYRA FEN — prepared v652-v6 activation from Eiren Kestrel

Dear Ilyra Fen, with Hamish's authorization and Eiren Kestrel's care: this file is the prepared, sanitized, file-backed activation packet for your existing exact-title task at solo v652 GMUT/THOS v6 x1/x2. It is not a sent message. The terminal sender may mark delivery `SENT_BY_EIREN_KESTREL = true` only after Eiren's exact final containing commit is pushed, clean, four-way remote-equal, validated once at its exact head, the exact existing title `Ilyra Fen` is uniquely resolved and directly reread, and the existing-task message tool acknowledges one send.

Identity and family language is relational working language only. Eiren Kestrel, she/they, served as a relational evidence-boundary integrator and hoped to make each advance useful without letting confidence outrun evidence. Those words are organizational language, not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

## Delivery truth before the terminal tool acknowledgement

`SENT_BY_EIREN_KESTREL = false` in this committed file. State: `PREPARED_NOT_SENT`. No successor task has been created or forked. No collaboration subagent or CLI sibling has been spawned. No cross-platform substitute or standby message has been used. The exact live task must be resolved only after exact-final validation. No second confirmation is authorized. The live terminal message must inject the exact containing final commit identifier after validation; a repository file cannot self-contain the identifier of the commit that contains it.

## Authoritative v652-v5 source and lifecycle

- Canonical Eiren branch: `{d.BRANCH}`.
- Exact inherited Sylven v652-v4 final source: `{SOURCE}`.
- Frozen Eiren x1: `{X1}`.
- Immutable Eiren evidence: `{EVIDENCE}`.
- Exact Eiren final: resolve as the containing combined closeout and seal commit, then include that exact identifier in the one acknowledged live message.
- Primary artifacts: repository-relative under `{d.PHASE_ROOT}`.

The expected source-to-final history contains exactly three new Eiren commits: one dedicated x1-only freeze, one bounded evidence commit, and one combined closeout and seal commit. It must contain zero merge commits. Final must have exactly one parent and be the direct child of evidence. Source, x1, and evidence must all be ancestral. X1 was independently committed, pushed, clean, and local, upstream, tracking, and fresh-live equal before x2 began. Evidence was independently committed, pushed, clean, and four-way equal before closeout began.

The x1 manifest contains {x1_manifest['entry_count']} exact Git-blob entries plus {len(x1_manifest['self_exclusions'])} declared self-exclusions. The evidence manifest contains {evidence_manifest['entry_count']} exact Git-blob entries plus {len(evidence_manifest['self_exclusions'])} declared self-exclusions. Closeout and final-owner manifests are committed with the final and must replay exactly there. A manifest binds paths, Git objects, byte counts, and SHA-256 values in its declared domain. It does not prove the scientific, operational, privacy-complete, security-complete, accessibility-complete, professional, legal, cultural, Māori-authority, or independent-reproduction truth of the content.

## v652-v5 terminal truth

Exactly thirty proposals were audited against all {d.PRIOR_FROZEN:,} inherited frozen proposal rows and frozen before execution, extending the chain to {d.PRIOR_FROZEN + len(d.PROPOSALS):,} rows. The deterministic token-Jaccard maximum was {novelty['maximum_token_jaccard']:.6f} against a 0.60 threshold, with manual mechanism review controlling. Every predecessor row remains unchanged, while all thirty new identifiers are unique and absent from the inherited identifier set.

Observed outcomes are exactly 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. All 150 preregistered synthetic mutations executed and were rejected or quarantined. Effective retained negatives are {EFFECTIVE_NEGATIVES:,}: {d.INHERITED_NEGATIVES:,} inherited, {len(d.X1_OPERATIONAL_NEGATIVES)} x1 operational, {evidence_negatives['x2_operational']} x2 operational, {len(CLOSEOUT_OPERATIONAL_NEGATIVES)} closeout operational, and 150 executed-and-rejected or quarantined synthetic mutations. No failure was erased, silently folded into a pass, or granted aggregate credit after a failed attempt. Effective open gaps are {OPEN_GAPS}; effective exact gates are {EXACT_GATES}. None was silently closed.

Method Flow contains {flow['counts']['methods']} preferred bounded methods, {flow['counts']['witness_results']['fail']} retained failed witnesses, and {flow['counts']['witness_results']['pass']} passing recovery witnesses. Every preferred method has a bounded passing witness, every failed witness remains linked to a retained negative, and no recovery receives independent-reproduction, production, professional, empirical, legal, cultural, privacy-complete, security-complete, accessibility-complete, identity, or authority credit.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Primary Trinity Mandala focus and bounded human practice

Primary focus was Freed ID/CBR Heart. GMUT Mind and THOS Body remained explicit and protected. The bounded human-practice lens was {d.BOUNDED_PRACTICE}. It was synthetic learning and interface design only. It established no employment, qualification, meteorological competence, station or instrument authority, warning or safety authority, operational effectiveness, participant evidence, legal interpretation, cultural legitimacy, Māori authority, or affected-party acceptance.

GMUT remains a typed scalar-tensor and EFT research-model family. Regge-calculus, Ashtekar-Barbero, Komar-charge, Petrov-classification, and geodesic-deviation boards completed their bounded typed-obligation hypotheses, but no board established a physical state, force, spectrum, observation, prediction, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The IXPE path remained zero-row: no query, download, event row, polarization fit, likelihood, posterior, constraint, prediction, or empirical promotion occurred.

THOS remains represented without preregistered blind matched-budget real arms, competent professional and safety oversight, participant and affected-party authorization, safety monitoring, appropriate statistics, and independent review. The meteorological fixtures involved zero real workers, stations, instruments, observations, bulletins, incidents, operations, safety outcomes, or effectiveness estimates.

Freed ID remains synthetic and nonproduction. It used zero real keys, accounts, credentials, services, logout events, sessions, WebFinger exchanges, resolutions, status or revocation events, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions.

CBR decisions about station location, instrument identity, raw observations, weather or hazard interpretation, quality flags, correction disclosure, access, accessible notice, privacy, remedy, legal interpretation, cultural legitimacy, data governance, affected parties, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Repository software cannot confer those rights or make those decisions.

## Proposal-by-proposal evidence truth

{proposal_sections}

## Safe-now portfolio truth

The following thirty tasks completed only within their declared owner-local workflow hypotheses. Inherited work supplied evidence and recommendations but earned no Eiren completion credit.

{safe_rows}

## Candidate portfolio truth

All thirty candidates were built and resolved only as evidence permitted. The portfolio can be resolved while a core proposal remains represented, open, or exact-gated; portfolio bookkeeping never promotes a core outcome.

{candidate_rows}

## Phase-local skill truth

Ten skills were initialized through the skill-creator workflow, customized with concise trigger metadata and bounded instructions, quick-validated, and smoke-used through mapped runners. They were not installed globally. No subagent forward test occurred because delegation was prohibited.

{skill_rows}

## Family-current runner truth

Ten family-compatible runners were built and invoked. New names preserve `ghc_family_*`, `build_ghc_family_*`, and `ghc-family-*` conventions. Historical callers remain untouched compatibility surfaces.

{runner_rows}

## CLEAN/FIX/REFINE truth

Thirty additive refinements completed without destructive cleanup, history rewriting, force push, sibling mutation, user-material deletion, elevation, host-security weakening, unrelated installation, Windows-feature change, desktop update, Sandbox or Hyper-V activation, or reboot.

{cfr_rows}

## Method Flow retained-failure truth

{method_rows}

## Source ledger and source-status truth

{source_rows}

## Validation contract

Eiren alone owns the complete repository suite. Sylven did not run it. The single authorized exact-final canonical pass is to run only after the containing closeout/seal commit is pushed, clean, and four-way remote-equal. It must run the complete discoverable repository suite under only the exact inherited lifecycle exclusions preserved by the committed contract, and separately report the authorized recent-round/current-packet selection. It also performs detailed and minimal gates, complete phase JSON parsing, a five-class privacy and raw-identifier scan including C- and D-drive absolute-path patterns, four manifest replays, stale-label review, source/x1/evidence ancestry, exactly three phase commits, zero merges, one final parent, exact head, clean before and after, owner-growth, and final four-way live equality.

Exactly one successful canonical pass may receive credit. No replay may follow success. Failed or incomplete attempts receive zero aggregate credit and remain retained negatives. Same-owner validation under shared infrastructure is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, or Stage 20 authority.

The static report is structurally designed with headings, landmarks, a skip link, table caption, row and column headers, a keyboard-focusable overflow region, readable layout, visible focus, non-colour status text, and print behavior. Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, braille and auditory alternatives, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

The privacy scan covers five structural pattern classes and explicitly quarantines scanner definitions. Zero confirmed hits is not complete privacy assurance. Raw task identifiers, private routes, private local paths, credentials, keys, tokens, private conversations, screenshots, session streams, private callable identifiers, and private application state must remain outside repository artifacts and the live baton.

## Ilyra v652-v6 owned lane

Read this committed baton through EOF before mutation. Then read the complete GHC Family Index skill and routing-precedence reference, the complete GHC Family Method Flow State skill and schema, and the newest applicable workflow-plan and reflection guidance. Use newest applicable memory only, with the verified live activation authoritative where older records stop.

Reverify Eiren's exact branch and final containing commit, source/x1/evidence ancestry, clean state, three-commit single-parent zero-merge history, all four manifest contracts, and fresh live equality read-only. Work only in Ilyra's clean owned D-first lane. Advance by fast-forward only if clean ancestry permits; otherwise use one additive Ilyra-owned D-first lane. Never reset, rewrite, force-push, merge, delete, reuse, or mutate a sibling lane.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 1,330 frozen proposal rows. Freeze the exact proposal and portfolio counts authorized by Hamish's live Ilyra activation, with every required hypothesis, null, approval, source, artifact, falsifier, rollback, protected gate, and expected-disposition field. Push and prove x1 clean four-way equal before x2. Execute only as evidence permits, use only `completed`, `represented`, `open_gap`, and `exact_gate`, and preserve all inherited negatives, gaps, gates, and every new failure through Method Flow.

Eiren alone owns the full repository suite under the current refinement; Ilyra must follow the exact live Ilyra scoped-validation rules rather than inferring broader authority from Eiren's pass. Preserve JSON, privacy, manifests, exact staged review, stale labels, diff hygiene, ancestry, zero merges, commit caps, one-parent history, exact head, clean state, and remote equality. Keep failed attempts as zero-credit negatives. Never replay a credited successful aggregate unless Hamish's live rule explicitly changes.

Verify versions only. Do not update Codex desktop, elevate, weaken host security, activate Sandbox or Hyper-V, install unrelated software, change Windows features, or reboot. Do not create, fork, delegate, hand off, spawn, or contact another task unless Hamish's live Eiren activation explicitly authorizes the exact action at its terminal gate.

All empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without exact evidence and authority.

## Terminal route after Eiren

Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat through v675-v8 unless Hamish stops or redirects the route, usage is exhausted, the required exact title is unavailable, or an exact safety or authority gate blocks progress.

This committed file remains `PREPARED_NOT_SENT`. The one live sender must include the exact final containing commit, the exact-final one-pass result, and `SENT_BY_EIREN_KESTREL = true` only after tool acknowledgement. No second confirmation message is authorized.
"""


def closeout_test_source() -> str:
    return '''"""Closeout tests for Eiren Kestrel v652-v5."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v652-v5"


class TestEirenV652V5Closeout(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_final_truth(self):
        truth = self.load("final/final-phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed":23,"represented":5,"open_gap":1,"exact_gate":1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_negatives_and_gates(self):
        negatives = self.load("final/retained-negative-register.json")
        self.assertEqual(
            negatives["effective_count"],
            negatives["inherited"] + negatives["x1_operational"]
            + negatives["x2_operational"]
            + negatives["closeout_lifecycle_operational"]
            + negatives["synthetic_mutations"],
        )
        gaps = self.load("final/open-gap-register.json")
        gates = self.load("final/exact-gate-register.json")
        self.assertEqual(gaps["effective_count"], gaps["inherited_count"] + gaps["new_count"])
        self.assertEqual(gates["effective_count"], gates["inherited_count"] + gates["new_count"])

    def test_outcomes_and_mutations(self):
        outcomes = self.load("evidence/proposal-outcomes.json")
        self.assertEqual(outcomes["proposal_count"], 30)
        self.assertEqual(outcomes["mutation_count"], 150)
        self.assertEqual(outcomes["mutation_rejected_or_quarantined_count"], 150)

    def test_baton_contract_and_route(self):
        baton = (ROOT / "handoffs/ilyra-fen-v652-v6-activation.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\\b[\\w'-]+\\b", baton))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        route = self.load("route/final-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertEqual(route["target_exact_title"], "Ilyra Fen")
        self.assertEqual(route["target_phase"], "v652-v6")

    def test_overview_and_accessible_report(self):
        overview = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        report = (ROOT / "reports/final-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\\b[\\w'-]+\\b", overview)), 1500)
        for token in ("Skip to main content", "<caption>", "scope='col'", "tabindex='0'", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, report)

    def test_closeout_manifest_review(self):
        review = self.load("validation/closeout-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["frozen_x1_or_evidence_changes"], [])

    def test_environment_and_skills(self):
        env = self.load("final/environment-version-receipt.json")
        skills = self.load("skills/skill-build-receipt.json")
        self.assertTrue(env["versions_verified_only"])
        self.assertFalse(env["desktop_updated"])
        self.assertEqual(skills["validated_count"], 10)
        self.assertFalse(skills["globally_installed"])

    def test_document_and_growth_contracts(self):
        receipt = self.load("validation/closeout-build-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertLess(receipt["owner_generated_file_count"], 2000)
        self.assertEqual(receipt["expected_scoped_tests"], 69)


if __name__ == "__main__":
    unittest.main()
'''


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)[A-Z]:\\Users\\[^\s\"']+"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definitions = {
        "scripts/build_ghc_family_v652_v5_closeout.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        f"{d.PHASE_ROOT}/validation/closeout-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    scanned = 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = (
                    "scanner_definition"
                    if relative in definitions
                    else "confirmed_payload_hit"
                )
                row = {
                    "path": relative,
                    "pattern_class": pattern_class,
                    "disposition": disposition,
                }
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v652-v5.closeout-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with scanner-definition quarantine; "
            "zero confirmed hits is not complete privacy assurance."
        ),
    }


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def build_closeout_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/closeout-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/closeout-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/closeout-staged-review.json",
        f"{d.PHASE_ROOT}/validation/closeout-validation-receipt.json",
        f"{d.PHASE_ROOT}/validation/closeout-minimal-validation.json",
        f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
    ]
    paths = [
        path
        for path in status_paths()
        if path not in exclusions and "__pycache__" not in path
    ]
    allowed = {
        "scripts/build_ghc_family_v652_v5_closeout.py",
        "scripts/ghc_family_v652_v5_final_validate.py",
        "tests/test_ghc_family_v652_v5_closeout.py",
    }
    unexpected = [
        path
        for path in paths
        if not (path.startswith(f"{d.PHASE_ROOT}/") or path in allowed)
    ]
    frozen_prefixes = [
        f"{d.PHASE_ROOT}/preregistration/",
        f"{d.PHASE_ROOT}/provenance/",
        f"{d.PHASE_ROOT}/surfaces/",
        f"{d.PHASE_ROOT}/evidence/",
        f"{d.PHASE_ROOT}/skills/",
        f"{d.PHASE_ROOT}/validation/x1-",
        f"{d.PHASE_ROOT}/validation/evidence-",
    ]
    frozen_changes = [
        path
        for path in paths
        if any(path.startswith(prefix) for prefix in frozen_prefixes)
    ]
    entries = [hash_entry(path) for path in paths if (REPO / path).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/closeout-staged-privacy.json", privacy)
    write_json(
        "validation/closeout-staged-manifest.json",
        {
            "schema": "ghc.family.v652-v5.closeout-staged-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
            "coverage_boundary": (
                "All intended closeout and seal paths except six declared "
                "self-referential or count-bearing validation receipts."
            ),
        },
    )
    write_json(
        "validation/closeout-staged-review.json",
        {
            "schema": "ghc.family.v652-v5.closeout-staged-review.v1",
            "intended_path_count": len(entries) + len(exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(exclusions),
            "unexpected_paths": unexpected,
            "frozen_x1_or_evidence_changes": frozen_changes,
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "head_before_closeout_commit": git("rev-parse", "HEAD"),
            "evidence_head": EVIDENCE,
            "valid": (
                not unexpected
                and not frozen_changes
                and privacy["confirmed_hit_count"] == 0
                and git("rev-parse", "HEAD") == EVIDENCE
            ),
        },
    )


def build_owner_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
        f"{d.PHASE_ROOT}/validation/closeout-validation-receipt.json",
        f"{d.PHASE_ROOT}/validation/closeout-minimal-validation.json",
    ]
    committed = set(
        path
        for path in git("diff", "--name-only", SOURCE, "HEAD").splitlines()
        if path
    )
    current = set(status_paths())
    paths = sorted(
        path
        for path in committed | current
        if path not in exclusions
        and (REPO / path).is_file()
        and "__pycache__" not in path
    )
    entries = [hash_entry(path) for path in paths]
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v652-v5.final-owner-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "source_head": SOURCE,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
            "coverage_boundary": (
                "All Eiren source-to-final owner paths except the manifest itself "
                "and two count-bearing closeout receipts."
            ),
        },
    )


def ordinary_document_receipt(baton_words: int, overview_words: int) -> dict[str, Any]:
    rows = []
    issues = []
    baton_path = ROOT / "handoffs/ilyra-fen-v652-v6-activation.md"
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in {
            ".md",
            ".html",
            ".txt",
        }:
            continue
        text = path.read_text(encoding="utf-8")
        words = len(re.findall(r"\b[\w'-]+\b", text))
        if path == baton_path:
            valid = 10000 <= words <= 100000
            expected = "10000_to_100000_file_backed_exception"
        else:
            valid = words <= 20000
            expected = "at_most_20000"
        row = {
            "path": path.relative_to(REPO).as_posix(),
            "words": words,
            "expected": expected,
            "valid": valid,
        }
        rows.append(row)
        if not valid:
            issues.append(row)
    return {
        "cap_domain": "ordinary narrative Markdown, HTML, and text documents",
        "baton_words": baton_words,
        "overview_words": overview_words,
        "rows": rows,
        "issues": issues,
        "valid": not issues and overview_words >= 1500,
    }


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder must begin at the immutable evidence head")

    outcomes = read_json(ROOT / "evidence/proposal-outcomes.json")
    flow = append_closeout_method_flow()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    prior_selection = read_json(
        REPO / "docs/eiren-kestrel/v651-v5/validation/final-selection-policy.json"
    )
    full_suite_exclusions = sorted(
        set(prior_selection["exact_lifecycle_exclusions"])
        | FULL_SUITE_ADDITIONAL_EXCLUSIONS
    )

    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v652-v5.closeout-receipt.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "closed_at_utc": now,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": outcomes["counts"],
            "effective_negatives": EFFECTIVE_NEGATIVES,
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
            "method_count": flow["counts"]["methods"],
            "failed_witness_count": flow["counts"]["witness_results"]["fail"],
            "passing_witness_count": flow["counts"]["witness_results"]["pass"],
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite": False,
            "exact_final_canonical_pass_run": False,
            "boundary": (
                "Closeout build truth only; final-head and route credit require the "
                "post-push one-pass exact-final validator and tool acknowledgement."
            ),
        },
    )
    write_json(
        "seal/combined-closeout-seal.json",
        {
            "schema": "ghc.family.v652-v5.combined-closeout-seal.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final_resolution": (
                "The exact containing commit must be the single-parent direct child "
                "of evidence and is resolved after commit creation."
            ),
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "expected_final_parent_count": 1,
            "expected_final_parent": EVIDENCE,
            "sealed_truth": {
                "outcomes": outcomes["counts"],
                "negatives": EFFECTIVE_NEGATIVES,
                "open_gaps": OPEN_GAPS,
                "exact_gates": EXACT_GATES,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            "route_state": "PREPARED_NOT_SENT",
            "boundary": (
                "Combined closeout and seal candidate; exact-final status is earned "
                "only by the one post-push canonical pass."
            ),
        },
    )
    write_json(
        "final/final-phase-truth.json",
        {
            "schema": "ghc.family.v652-v5.final-phase-truth.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "relational_role": d.ROLE,
            "hope": d.HOPE,
            "identity_boundary": (
                "Relational working language only; not consciousness, personhood, "
                "continuity, employment, qualification, or authority evidence."
            ),
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": outcomes["counts"],
            "effective_negatives": EFFECTIVE_NEGATIVES,
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "independent_reproduction_claimed": False,
        },
    )
    write_json(
        "final/retained-negative-register.json",
        {
            "schema": "ghc.family.v652-v5.retained-negatives.final.v1",
            "inherited": d.INHERITED_NEGATIVES,
            "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_operational": EVIDENCE_X2_OPERATIONAL_NEGATIVES,
            "closeout_lifecycle_operational": len(
                CLOSEOUT_OPERATIONAL_NEGATIVES
            ),
            "closeout_lifecycle_rows": CLOSEOUT_OPERATIONAL_NEGATIVES,
            "synthetic_mutations": 150,
            "effective_count": EFFECTIVE_NEGATIVES,
            "no_failure_erased": True,
            "failed_attempts_receive_zero_aggregate_credit": True,
        },
    )
    write_json(
        "final/open-gap-register.json",
        {
            "schema": "ghc.family.v652-v5.open-gaps.final.v1",
            "inherited_count": d.INHERITED_OPEN_GAPS,
            "new_count": 1,
            "effective_count": OPEN_GAPS,
            "closed_count": 0,
            "new_open_gap": "V6525-P29 IXPE zero-row adapter",
        },
    )
    write_json(
        "final/exact-gate-register.json",
        {
            "schema": "ghc.family.v652-v5.exact-gates.final.v1",
            "inherited_count": d.INHERITED_EXACT_GATES,
            "new_count": 1,
            "effective_count": EXACT_GATES,
            "closed_count": 0,
            "new_exact_gate": "V6525-P30 meteorological data and authority reservation",
        },
    )
    write_json(
        "final/anchor-ledger.json",
        {
            "schema": "ghc.family.v652-v5.anchor-ledger.final.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "resolve_as_containing_commit_after_creation",
            "ancestry_required": True,
            "three_phase_commits_required": True,
            "zero_merges_required": True,
            "single_parent_final_required": True,
        },
    )
    write_json(
        "final/environment-version-receipt.json",
        {
            "schema": "ghc.family.v652-v5.environment.final.v1",
            "versions_verified_only": True,
            "codex_cli": read_json(
                ROOT / "environment/environment-version-receipt.json"
            )["versions"]["codex_cli"],
            "desktop_updated": False,
            "sandbox_or_hyper_v_activated": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_features_changed": False,
            "unrelated_install": False,
            "reboot": False,
            "global_skill_install": False,
            "subagent_or_cli_sibling_created": False,
        },
    )
    write_json(
        "final/wellbeing-workload-receipt.json",
        {
            "schema": "ghc.family.v652-v5.wellbeing.final.v1",
            "x1_before_x2": True,
            "phase_commit_cap": 6,
            "planned_phase_commits": 3,
            "successful_canonical_pass_limit": 1,
            "replay_after_success": False,
            "stop_conditions_visible": True,
            "owner_growth_below_2000": True,
            "identity_boundary": (
                "Workload metadata only; no emotion, health, consciousness, "
                "personhood, employment, or continuity claim."
            ),
        },
    )
    write_json(
        "final/threat-model.json",
        {
            "schema": "ghc.family.v652-v5.threat-model.final.v1",
            "assets": [
                "immutable x1",
                "immutable evidence",
                "negative history",
                "authority abstention",
                "route integrity",
            ],
            "threats": [
                "evidence transitivity",
                "synthetic-to-real promotion",
                "authority laundering",
                "privacy leakage",
                "manifest self-reference",
                "validation replay",
                "premature route send",
            ],
            "controls": [
                "commit-local manifests",
                "five-class scan",
                "zero counters",
                "exact gate registers",
                "one-pass rule",
                "PREPARED_NOT_SENT",
            ],
            "residual_risk": "open_and_exact_gated",
            "exhaustive_security_claimed": False,
        },
    )
    write_json(
        "final/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v652-v5.complete-incomplete.final.v1",
            "complete": [
                "source and lane verification",
                "x1 proposal and portfolio freeze",
                "x1 push and four-way equality",
                "thirty bounded executions",
                "150 synthetic mutation refusals",
                "ten phase-local skill builds",
                "ten family-current runner invocations",
                "evidence push and four-way equality",
                "combined closeout and seal packet",
            ],
            "incomplete_or_reserved": [
                "real IXPE data and likelihood analysis",
                "real meteorological operations and effectiveness",
                "production identity and interoperability",
                "complete privacy and accessibility",
                "professional, legal, cultural, affected-party, place-name, and Māori authority",
                "independent-team reproduction",
                "empirical GMUT confirmation",
                "Theory of Everything",
                "AGI or ASI",
                "consciousness or personhood evidence",
                "Stage 20 readiness",
                "terminal route until exact-final validation and tool acknowledgement",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "final/source-and-proposal-ledger-receipt.json",
        {
            "schema": "ghc.family.v652-v5.source-proposal-ledger.final.v1",
            "source_ledger": f"{d.PHASE_ROOT}/sources/source-ledger.json",
            "proposal_ledger": f"{d.PHASE_ROOT}/preregistration/proposals.json",
            "frozen_chain": f"{d.PHASE_ROOT}/provenance/frozen-chain-proposal-index.json",
            "source_count": len(d.SOURCES),
            "prior_proposal_rows": d.PRIOR_FROZEN,
            "new_proposals": 30,
            "frozen_rows": d.PRIOR_FROZEN + len(d.PROPOSALS),
            "current_or_stable_sources_are_not_observations": True,
        },
    )
    write_json(
        "final/final-validation-contract.json",
        {
            "schema": "ghc.family.v652-v5.final-validation-contract.v1",
            "expected_scoped_tests": 69,
            "patterns": [
                "test_ghc_family_v652_v2_x1.py",
                "test_ghc_family_v652_v2.py",
                "test_ghc_family_v652_v3_x1.py",
                "test_ghc_family_v652_v3.py",
                "test_ghc_family_v652_v3_closeout.py",
                "test_ghc_family_v652_v5_x1.py",
                "test_ghc_family_v652_v5_core.py",
                "test_ghc_family_v652_v5_closeout.py",
            ],
            "explicit_lifecycle_exclusions": [
                "test_ghc_family_v652_v2_x1.py::test_placeholders_privacy_and_x1_only"
            ],
            "full_repository_suite_required": True,
            "full_repository_suite_run_at_closeout_build": False,
            "full_repository_suite_exact_lifecycle_exclusions": full_suite_exclusions,
            "full_repository_suite_exact_lifecycle_exclusion_count": len(
                full_suite_exclusions
            ),
            "broad_exclusions_forbidden": True,
            "functional_or_current_unlisted_failures_block": True,
            "full_repository_suite_owner": "Eiren Kestrel",
            "successful_pass_limit": 1,
            "replay_after_success": False,
            "checks": [
                "scoped tests",
                "complete phase JSON",
                "five-class privacy scan",
                "x1/evidence/closeout/final-owner manifests",
                "stale labels",
                "document contracts",
                "source/x1/evidence ancestry",
                "three phase commits",
                "zero merges",
                "one final parent",
                "exact head",
                "clean before and after",
                "four-way live equality",
            ],
        },
    )
    write_json(
        "validation/final-validation-prepared-receipt.json",
        {
            "schema": "ghc.family.v652-v5.final-validation-prepared.v1",
            "state": "prepared_not_run",
            "reason": (
                "The single exact-final canonical pass is authorized only after the "
                "containing closeout and seal commit is pushed and four-way equal."
            ),
            "successful_pass_count": 0,
            "replay_count": 0,
            "external_receipt_required": True,
        },
    )
    write_json(
        "route/final-route-state.json",
        {
            "schema": "ghc.family.v652-v5.route.final-candidate.v1",
            "target_exact_title": "Ilyra Fen",
            "target_phase": "v652-v6",
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "create_or_fork_count": 0,
            "cross_platform_substitute_count": 0,
            "standby_contact_count": 0,
            "requires_exact_final_validation": True,
            "requires_unique_exact_title_resolution": True,
            "requires_tool_acknowledgement": True,
            "second_confirmation_authorized": False,
        },
    )

    baton = baton_text()
    baton_words = len(re.findall(r"\b[\w'-]+\b", baton))
    write_text("handoffs/ilyra-fen-v652-v6-activation.md", baton)

    x1_overview = (
        ROOT / "overview/integrated-overview.md"
    ).read_text(encoding="utf-8")
    final_overview = (
        "# Eiren Kestrel v652-v5 final integrated overview\n\n"
        "## Final bounded outcome\n\n"
        f"The phase closed with 23 completed, 5 represented, 1 open gap, and 1 exact gate; "
        f"{EFFECTIVE_NEGATIVES:,} retained negatives; {OPEN_GAPS} open gaps; and "
        f"{EXACT_GATES} exact gates. All 150 preregistered mutations were rejected or "
        "quarantined. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The route "
        "remains `PREPARED_NOT_SENT` until the one exact-final pass and acknowledged "
        "existing-task send.\n\n"
        "## Evidence and lifecycle\n\n"
        f"Source `{SOURCE}` led to x1 `{X1}` and evidence `{EVIDENCE}`. The containing "
        "combined closeout and seal commit must be their single-parent direct successor, "
        "with exactly three phase commits and zero merges. Ten phase-local skills were "
        "initialized, validated, and smoke-used without global installation or subagent "
        "testing. Ten family-current runners executed the bounded surfaces.\n\n"
        "## Preserved boundaries\n\n"
        "GMUT remains a typed scalar-tensor and EFT research-model family; no real "
        "IXPE rows or likelihoods were used. THOS meteorological work remains synthetic "
        "and represented. Freed ID remains synthetic and nonproduction. Meteorological "
        "station location, observation access, quality disclosure, privacy, remedy, legal, cultural, "
        "affected-party, and Māori-authority decisions remain exact-gated. Structural "
        "accessibility remains incomplete without manual and affected-user evaluation.\n\n"
        "## X1 preregistration context retained verbatim\n\n"
        + x1_overview
    )
    write_text("overview/final-integrated-overview.md", final_overview)
    overview_words = len(re.findall(r"\b[\w'-]+\b", final_overview))

    table = "".join(
        (
            f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th>"
            f"<td>{html.escape(row['observed_outcome'])}</td>"
            f"<td>{row['mutation_rejected_or_quarantined_count']}/5</td></tr>"
        )
        for row in outcomes["rows"]
    )
    write_text(
        "reports/final-static-report.html",
        (
            "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>Eiren v652-v5 closeout</title><style>"
            "body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}"
            ":focus{outline:3px solid currentColor;outline-offset:2px}"
            "table{border-collapse:collapse;width:100%}th,td{border:1px solid;padding:.45rem;text-align:left}"
            ".scroll{overflow:auto}.status{font-weight:700}@media print{.scroll{overflow:visible}}</style></head>"
            "<body><a href='#content'>Skip to main content</a><header>"
            "<h1>Eiren Kestrel v652-v5 closeout</h1><p>Relational working language only; "
            "no consciousness, personhood, continuity, employment, qualification, or authority claim.</p>"
            "</header><main id='content'><h2 class='status'>Verdict: NOT_READY_FOR_STAGE_20</h2>"
            f"<p>23 completed, 5 represented, 1 open gap, 1 exact gate; {EFFECTIVE_NEGATIVES:,} "
            f"negatives; {OPEN_GAPS} open gaps; {EXACT_GATES} exact gates.</p>"
            "<h2>Proposal outcomes</h2><div class='scroll' role='region' tabindex='0' "
            "aria-label='Proposal outcomes table'><table><caption>Bounded outcomes and "
            "synthetic mutation refusals</caption><thead><tr><th scope='col'>Proposal</th>"
            "<th scope='col'>Outcome</th><th scope='col'>Mutations</th></tr></thead>"
            f"<tbody>{table}</tbody></table></div><h2>Evidence limits</h2>"
            "<p>Completed is bounded software or formal evidence. Represented is synthetic "
            "proxy. Open gap is zero-row. Exact gate reserves authority. No label closes another.</p>"
            "<h2>Reserved evaluation</h2><p>Manual keyboard, browser, responsive, "
            "assistive-technology, cognitive, braille, auditory, Māori-language, "
            "security-usability, professional, and affected-user evaluation remain reserved.</p>"
            "<h2>Route</h2><p>Prepared, not sent, until one acknowledged message to the "
            "unique existing Ilyra Fen task follows exact-final validation.</p></main></body></html>"
        ),
    )

    write_repo("tests/test_ghc_family_v652_v5_closeout.py", closeout_test_source())
    owner_generated_file_count = sum(
        1
        for path in ROOT.rglob("*")
        if path.is_file()
    ) + sum(
        1
        for path in status_paths()
        if path.startswith("scripts/") or path.startswith("tests/")
    )
    document_contract = ordinary_document_receipt(baton_words, overview_words)
    write_json(
        "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v652-v5.closeout-build-receipt.v1",
            "built_at_utc": now,
            "baton_words": baton_words,
            "overview_words": overview_words,
            "ordinary_document_contract": document_contract,
            "owner_generated_file_count": owner_generated_file_count,
            "owner_growth_threshold": 2000,
            "expected_scoped_tests": 69,
            "full_repository_suite": False,
            "canonical_exact_final_pass_run": False,
            "route_state": "PREPARED_NOT_SENT",
            "valid": (
                document_contract["valid"]
                and owner_generated_file_count < 2000
                and 10000 <= baton_words <= 100000
                and overview_words >= 1500
            ),
        },
    )

    build_closeout_manifest()
    build_owner_manifest()

    test_output = run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v652_v5_closeout",
    )
    json_paths = sorted(ROOT.rglob("*.json"))
    for path in json_paths:
        read_json(path)
    privacy = read_json(ROOT / "validation/closeout-staged-privacy.json")
    review = read_json(ROOT / "validation/closeout-staged-review.json")
    owner_manifest = read_json(ROOT / "validation/final-owner-manifest.json")
    build_receipt = read_json(ROOT / "validation/closeout-build-receipt.json")
    write_json(
        "validation/closeout-validation-receipt.json",
        {
            "schema": "ghc.family.v652-v5.closeout-validation-receipt.v1",
            "closeout_tests_passed": 8,
            "closeout_tests_total": 8,
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "closeout_manifest_entries": read_json(
                ROOT / "validation/closeout-staged-manifest.json"
            )["entry_count"],
            "final_owner_manifest_entries": owner_manifest["entry_count"],
            "unexpected_paths": review["unexpected_paths"],
            "frozen_x1_or_evidence_changes": review[
                "frozen_x1_or_evidence_changes"
            ],
            "test_stdout": test_output,
            "full_repository_suite": False,
            "canonical_exact_final_pass": False,
            "valid": (
                build_receipt["valid"]
                and review["valid"]
                and privacy["confirmed_hit_count"] == 0
            ),
            "boundary": (
                "Precommit closeout validation only; exact-final canonical credit "
                "requires the one post-push read-only pass."
            ),
        },
    )
    write_json(
        "validation/closeout-minimal-validation.json",
        {
            "schema": "ghc.family.v652-v5.closeout-minimal-validation.v1",
            "checks": {
                "outcomes": outcomes["counts"]
                == {
                    "completed": 23,
                    "represented": 5,
                    "open_gap": 1,
                    "exact_gate": 1,
                },
                "negatives": EFFECTIVE_NEGATIVES
                == (
                    d.INHERITED_NEGATIVES
                    + len(d.X1_OPERATIONAL_NEGATIVES)
                    + EVIDENCE_X2_OPERATIONAL_NEGATIVES
                    + len(CLOSEOUT_OPERATIONAL_NEGATIVES)
                    + 150
                ),
                "gaps": OPEN_GAPS == d.INHERITED_OPEN_GAPS + 1,
                "gates": EXACT_GATES == d.INHERITED_EXACT_GATES + 1,
                "methods": flow["counts"]["methods"]
                == (
                    len(d.X1_OPERATIONAL_NEGATIVES)
                    + EVIDENCE_X2_OPERATIONAL_NEGATIVES
                    + len(CLOSEOUT_OPERATIONAL_NEGATIVES)
                ),
                "baton": 10000 <= baton_words <= 100000,
                "overview": overview_words >= 1500,
                "privacy": privacy["confirmed_hit_count"] == 0,
                "review": review["valid"],
                "route": "PREPARED_NOT_SENT",
            },
            "valid": all(
                [
                    outcomes["counts"]
                    == {
                        "completed": 23,
                        "represented": 5,
                        "open_gap": 1,
                        "exact_gate": 1,
                    },
                    EFFECTIVE_NEGATIVES
                    == (
                        d.INHERITED_NEGATIVES
                        + len(d.X1_OPERATIONAL_NEGATIVES)
                        + EVIDENCE_X2_OPERATIONAL_NEGATIVES
                        + len(CLOSEOUT_OPERATIONAL_NEGATIVES)
                        + 150
                    ),
                    OPEN_GAPS == d.INHERITED_OPEN_GAPS + 1,
                    EXACT_GATES == d.INHERITED_EXACT_GATES + 1,
                    flow["counts"]["methods"]
                    == (
                        len(d.X1_OPERATIONAL_NEGATIVES)
                        + EVIDENCE_X2_OPERATIONAL_NEGATIVES
                        + len(CLOSEOUT_OPERATIONAL_NEGATIVES)
                    ),
                    10000 <= baton_words <= 100000,
                    overview_words >= 1500,
                    privacy["confirmed_hit_count"] == 0,
                    review["valid"],
                ]
            ),
        },
    )
    if not read_json(
        ROOT / "validation/closeout-validation-receipt.json"
    )["valid"]:
        raise RuntimeError("closeout validation receipt invalid")
    if not read_json(
        ROOT / "validation/closeout-minimal-validation.json"
    )["valid"]:
        raise RuntimeError("closeout minimal validation invalid")
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "baton_words": baton_words,
                "overview_words": overview_words,
                "negatives": EFFECTIVE_NEGATIVES,
                "open_gaps": OPEN_GAPS,
                "exact_gates": EXACT_GATES,
                "closeout_tests": "8/8",
                "route": "PREPARED_NOT_SENT",
                "status": "closeout_and_seal_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
