#!/usr/bin/env python3
"""Build the Sylven Arc v646-v6 x2 evidence packet without closeout or seal."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v646_v6_definitions as d
from ghc_family_v646_v6_runtime import ARTIFACTS, PHASE, write_phase_artifacts


ROOT = Path(__file__).resolve().parents[1]
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"
X1_REVISION = "147aab7fd2f2805f119968dd30ab9c7996306d3a"


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


X2_NEGATIVES = [
    {
        "negative_id": "V6466-X2-N01",
        "failure": "The first source-gate run addressed the generic zero-row receipt as though its counters were top-level and stopped with a missing-key error.",
        "recovery": "Embed the surface summary in each mutation or receipt envelope and read the declared surface_summary structure.",
        "title": "Read generic evidence envelopes through their declared surface summary",
        "signature": "source gate KeyError for a zero-row counter in a generic mutation envelope",
        "trigger": ["generic evidence envelope", "surface-specific source gate", "zero-row receipt", "schema traversal"],
        "workaround": "Persist the bounded surface summary inside the receipt and make the gate traverse that explicit field.",
        "guard": "Validators must read the declared schema shape and never infer top-level placement from a filename.",
        "pass": "The repaired gate read surface_summary and passed all five zero-evidence and no-authority checks.",
    },
    {
        "negative_id": "V6466-X2-N02",
        "failure": "The repaired source gate wrote a passing UTF-8 receipt but failed while printing Māori boundary text through the Windows CP1252 console.",
        "recovery": "Keep repository receipts UTF-8 and emit console summaries with JSON ASCII escapes.",
        "title": "Separate UTF-8 evidence files from narrow Windows console summaries",
        "signature": "UnicodeEncodeError while printing Māori text to a CP1252 console",
        "trigger": ["Windows console", "CP1252", "UTF-8 repository receipt", "Māori boundary text"],
        "workaround": "Write the canonical receipt as UTF-8 and serialize only the console copy with ensure_ascii enabled.",
        "guard": "Console compatibility must not strip or alter Māori text in repository evidence.",
        "pass": "The source gate retained the UTF-8 receipt and returned a passing ASCII-escaped console summary.",
    },
    {
        "negative_id": "V6466-X2-N03",
        "failure": "The first x2 Method Flow summarize command wrote its files but exited while printing Māori boundary text through the Windows CP1252 console.",
        "recovery": "Run the unchanged family Method Flow command with Python UTF-8 mode for its console while preserving UTF-8 repository outputs.",
        "title": "Invoke the family Method Flow runner in UTF-8 console mode",
        "signature": "UnicodeEncodeError from the family Method Flow summarize console print",
        "trigger": ["family Method Flow runner", "Windows CP1252 console", "Māori boundary text", "summary command"],
        "workaround": "Set PYTHONUTF8 for the child process without changing the ledger, summary content, or repository encoding.",
        "guard": "Family runner subprocesses that can emit Māori text use UTF-8 console mode; repository files remain UTF-8.",
        "pass": "The unchanged summarize command completed in UTF-8 console mode and preserved the existing failed and passing witnesses.",
    },
    {
        "negative_id": "V6466-X2-N04",
        "failure": "The first full bounded validator passed tests, detailed, and minimal checks but the privacy scan promoted two accessibility browser-diversity field names into private-callable hits.",
        "recovery": "Keep the callable pattern class and full-file coverage but require callable-semantic browser prefixes instead of treating every browser_ field as a private identifier.",
        "title": "Distinguish browser evaluation labels from private browser callable identifiers",
        "signature": "five-class scan matched browser_diversity as a private callable identifier",
        "trigger": ["five-class privacy scan", "accessibility receipt", "browser-prefixed field", "private callable class"],
        "workaround": "Constrain the browser callable branch to send, probe, route, callable, or message semantics and retain all other pattern classes and candidates.",
        "guard": "Generic browser evaluation vocabulary is not a callable ID; any callable-semantic browser identifier remains confirmed unless explicitly dispositioned.",
        "pass": "The rerun retained the route-policy candidate, reported zero private-callable payload hits, and passed all five privacy classes.",
    },
    {
        "negative_id": "V6466-X2-N05",
        "failure": "The first exact staged evidence scan retained six candidates but treated the validation runner's three scanner-definition literals as confirmed payload hits.",
        "recovery": "Recognize both staged-review and validation-runner files as scanner definitions for callable and session pattern literals while scanning and counting the files unchanged.",
        "title": "Classify both privacy scanner implementations as scanner-definition candidates",
        "signature": "exact staged scan confirmed private-callable and session regex literals inside the validation runner",
        "trigger": ["exact staged Git-blob scan", "validation runner source", "scanner regex literals", "candidate-confirmed split"],
        "workaround": "Disposition only callable and session matches in the two known scanner implementations as scanner-definition candidates; keep all files and classes in coverage.",
        "guard": "The exception is path- and class-specific; any nondefinition match remains confirmed.",
        "pass": "The rerun scanned the same staged source files, retained all scanner-definition candidates, and reported zero confirmed privacy hits.",
    },
]


def method_call(*args: str) -> None:
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
    )


def build_x2_method_flow() -> None:
    ledger = PHASE / "method-flow/x2-method-flow-state.json"
    if not ledger.exists():
        method_call("init", "--ledger", str(ledger), "--phase", d.PHASE + "-x2", "--owner", d.OWNER)
    else:
        existing = json.loads(ledger.read_text(encoding="utf-8"))
        if existing.get("owner") != d.OWNER:
            raise RuntimeError("x2 Method Flow owner mismatch")
    for index, neg in enumerate(X2_NEGATIVES, 1):
        method_id = f"V6466-X2-M{index:02d}"
        failed_id = f"V6466-X2-M{index:02d}-W-F"
        passed_id = f"V6466-X2-M{index:02d}-W-P"
        record = f"method-flow/v6466-x2-m{index:02d}-method-record.json"
        failed = f"method-flow/v6466-x2-m{index:02d}-failed-witness.json"
        passed = f"method-flow/v6466-x2-m{index:02d}-passing-witness.json"
        write_json(
            record,
            {
                "method_id": method_id,
                "title": neg["title"],
                "failure_signature": neg["signature"],
                "trigger_preconditions": neg["trigger"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_scoped_workflow",
                "candidate_workaround": neg["workaround"],
                "validation_witness_ids": [],
                "recurrence_guard": neg["guard"],
                "rollback": "Retain the original failure and award no affected credit until the bounded recovery passes.",
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": ["privacy", "external_state", "sibling_lane", "independent_reproduction", "stage20"],
                "retained_negative_ids": [neg["negative_id"]],
                "scope_boundary": "Owner-local workflow recovery only; no scientific, professional, production, authority, or independent-reproduction credit.",
            },
        )
        write_json(
            failed,
            {
                "witness_id": failed_id,
                "method_id": method_id,
                "procedure": "Original x2 attempt retained from execution.",
                "scope": "Sylven v646-v6 x2 evidence build",
                "expected": "The bounded tool returns a complete passing result.",
                "observed": neg["failure"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [neg["negative_id"]],
                "boundary": d.TRUTH_BOUNDARY,
            },
        )
        write_json(
            passed,
            {
                "witness_id": passed_id,
                "method_id": method_id,
                "procedure": neg["workaround"],
                "scope": "Sylven v646-v6 bounded x2 recovery",
                "expected": "The recovery passes without weakening content or protected gates.",
                "observed": neg["pass"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [neg["negative_id"]],
                "boundary": d.TRUTH_BOUNDARY,
            },
        )
        current = json.loads(ledger.read_text(encoding="utf-8"))
        if not any(row.get("method_id") == method_id for row in current.get("methods", [])):
            method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / record))
        current = json.loads(ledger.read_text(encoding="utf-8"))
        for witness_id, relative in ((failed_id, failed), (passed_id, passed)):
            if not any(row.get("witness_id") == witness_id for row in current.get("witnesses", [])):
                method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / relative))
                current = json.loads(ledger.read_text(encoding="utf-8"))
        method = next(row for row in current["methods"] if row["method_id"] == method_id)
        if method.get("recommendation_state") != "preferred":
            method_call("set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Validated only for the bounded recorded trigger; failed witness retained.")
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/x2-runner-validation.json"))
    method_call("summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/x2-method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/x2-method-flow-summary.md"))


def proposal_ledger() -> dict[str, Any]:
    rows = []
    for index, proposal in enumerate(d.PROPOSALS, 1):
        key = f"{index:02d}"
        contract_rel, mutation_rel = ARTIFACTS[key]
        contract = load(contract_rel)
        mutation = load(mutation_rel)
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "outcome": contract["outcome"],
                "artifacts": [contract_rel, mutation_rel],
                "acceptance_gate_passed": contract["outcome"] == proposal["expected_disposition"],
                "mutations_executed": mutation["mutation_count"],
                "mutations_rejected": mutation["rejected_count"],
                "real_world_effect": False,
                "authority_delegated": False,
                "boundary": d.TRUTH_BOUNDARY,
            }
        )
    distribution = dict(sorted(Counter(row["outcome"] for row in rows).items()))
    return {
        "schema": "ghc.family.v646-v6.x2-proposal-ledger.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "x1_revision": X1_REVISION,
        "proposal_count": len(rows),
        "distribution": distribution,
        "proposals": rows,
        "real_data_rows": 0,
        "real_people_or_operations": 0,
        "real_keys_tokens_or_transactions": 0,
        "authority_delegated": False,
        "independent_team_reproduction": False,
        "boundary": d.TRUTH_BOUNDARY,
    }


def overview() -> str:
    return f"""# Sylven Arc v646-v6 integrated evidence overview

## Scope and working identity

Sylven Arc, they/them, is a relational working name for a constraint-cartographer and falsifier-keeper. The working hope is to make unresolved boundaries legible without turning uncertainty into authority. This language does not establish consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, hydrographic competence, maritime-safety authority, place-name authority, cultural authority, Māori authority, or independent authority. Hamish may pause, rename, redirect, or stop the work.

This phase continued only the clean Sylven-owned canonical lane after a fast-forward from the verified source. The dedicated x1 freeze is {X1_REVISION}. It is a direct child of the source, contains exactly ten proposals and the 30/20/20/10/30 portfolio plans, contains no x2 execution artifact, and was pushed with exact local, upstream, tracking, and fresh-live-remote equality before x2 began. The x1 corpus audit parsed all 440 prior frozen proposals, found no exact collision, and raised the frozen chain to 450.

The primary Trinity Mandala focus is Freed ID/CBR Heart. GMUT Mind and THOS Body remain explicit. The bounded human-practice lens is hydrographic chart correction, hazard-report triage, and Notices to Mariners handover. That lens is synthetic learning and structural design only. It does not qualify this repository or its owner to receive, assess, publish, suppress, or correct a real hazard report, chart, electronic navigational chart, Notice to Mariners, place name, customary-use claim, private report, remedy request, or maritime-safety decision.

## Core evidence and falsifiers

Proposal 1 completed a durable-outbox and delivery-order tribunal. The positive fixture requires prepared, durable, dispatch-intent, and acknowledgement states in order. Seven mutations reject acknowledgement before durable recording, duplicate credit, hidden sequence gaps, unbounded poison retries, deleted dead-letter evidence, an exactly-once overclaim, and automatic replay of an external side effect. This is owner-local workflow evidence only. No message or external action was sent.

Proposal 2 completed a typed Schwinger-Dyson obligation tribunal. It records generating-functional, hierarchy, closure, retained and omitted vertex, counterterm, renormalization-condition, symmetry, unit, and EFT-domain requirements. Seven mutations reject silent closure, omitted-equals-zero reasoning, missing counterterms or renormalization conditions, incompatible symmetry assumptions, untyped domains, and promotion into quantum or empirical proof. No GMUT quantum solution, observable, force, prediction, likelihood, constraint, stability theorem, ultraviolet completion, or Theory of Everything was produced.

Proposal 3 remains open_gap. The eROSITA eRASS1 adapter records official release, catalogue, footprint, selection, calibration, contamination, completeness, covariance, nuisance, and baseline requirements. It used zero accounts, downloads, real rows, likelihood calls, posterior samples, constraints, or force claims. Official release metadata is provenance context, not an observation. A real study still requires a separately authorized and independently reviewed protocol with exact products, selection, calibration, covariance, nuisance treatment, baseline, uncertainty analysis, and claim discipline.

Proposal 4 remains represented. Synthetic hydrographic traces cover report identity, chart or ENC edition, datum, position fixing, uncertainty, hazard class, producer-reviewer separation, correction and notice state, cancellation, workload, matched budgets, blind labels, and next-watch ownership. Seven mutations reject missing datum or uncertainty, self-approval, unreviewed reactivation, missing handover ownership, real operational data, and effectiveness overclaim. There were zero real mariners, vessels, voyages, hazards, corrections, notices, participants, operational decisions, blind real arms, or effectiveness estimates.

Proposal 5 remains represented. The Freed ID DPoP profile types proof kind, public JWK, algorithm, HTTP method and target URI, issue time, unique identifier, nonce, access-token hash, key thumbprint, token type, freshness, and replay cache. Seven mutations reject type or algorithm drift, method or URI mismatch, nonce downgrade, token-hash mismatch, key mismatch or private material, and replay or production overclaim. The fixture contains zero real private keys, tokens, authorization decisions, identities, networks, wallets, issuers, verifiers, or interoperability events. TLS, implementation review, privacy and security review, recovery, and trust governance remain required for any production claim.

Proposal 6 remains exact_gate. The CBR matrix reserves hazard disclosure, reporter confidentiality, publication, chart correction, false-report response, commercial effects, customary use, sensitive locations, place-name status, data governance, remedy, legal interpretation, affected-party legitimacy, and Māori authority. It made zero case decisions. Official LINZ and New Zealand Geographic Board material establishes source context and real-world roles; it does not delegate a particular decision to this repository. Māori data and place-name questions remain under the appropriate tangata whenua, iwi, hapū, mana whenua, affected-party, Māori, cultural, and competent statutory authorities.

Proposal 7 completed a disposable JSON text-sequence tribunal. It parses RFC 7464-oriented record-separator and line-feed fixtures, retains invalid elements, rejects torn tails, and layers a phase-local ordinal and digest check that is explicitly not an RFC canonical form. The disposable fixture was removed and the canonical repository was not used as test data. Seven failures remain retained. This is not durability certification, signature assurance, canonicalization proof, or exhaustive parser security.

Proposal 8 completed a structural dragging, pointer-cancellation, and target-spacing audit. It requires a non-drag single-pointer alternative, a declared keyboard alternative, abortable or up-event activation, cancellation or undo, target-size or spacing logic, overlap review, visible instructions, and manual-evaluation reservations. Seven mutations were rejected. No browser-diversity, manual keyboard, assistive-technology, motor-access, Māori-language, cognitive-accessibility, or affected-user evaluation occurred, so complete accessibility conformance remains open.

Proposal 9 completed a typed Gibbs phase-rule classifier. It keeps component, phase, equilibrium, reactive-constraint, fixed-intensive-variable, and nonnegative degree-of-freedom assumptions explicit. Seven mutations reject missing counts or equilibrium, hidden constraints, an incorrect constrained count, negative freedom, and conversion into human choice, autonomy, identity, justice, psyche, or consciousness claims. It is a thermodynamic formal surface only and contains zero participant evidence.

Proposal 10 completed a structural Stage 20 decision-curve nonpromotion board. A synthetic abstract event table exercises threshold probability, true and false positives, a net-benefit calculation, treat-all and treat-none baselines, and explicit absence of prevalence transport or value authority. Seven mutations reject universalized thresholds, unsupported transport, missing calibration or population, hidden harms, missing baselines, missing uncertainty or authority, and Stage 20 promotion. No real decision, person, clinical recommendation, policy preference, or governed value judgment was made.

## Portfolios, Method Flow, and retained negatives

The phase executed 30 new safe-now tasks, 20 bounded candidate prototypes, 20 phase-local skill builds, 10 family-current runner builds, and 30 additive CLEAN/FIX/REFINE tasks. Completion means only that the declared owner-local structural or synthetic hypothesis and evidence link exist. It supplies no inherited-work completion credit and cannot compensate for missing empirical, professional, participant, legal, cultural, privacy, security, accessibility, or independent evidence.

All 70 preregistered synthetic negative mutations executed and were rejected. The activation baseline of 2,884 inherited effective negatives remains preserved. Ten x1 operational failures and {len(X2_NEGATIVES)} x2 operational failures are added, making {d.INHERITED_EFFECTIVE_NEGATIVES + 10 + d.PREREGISTERED_SYNTHETIC_NEGATIVES + len(X2_NEGATIVES)} effective negatives at this evidence point. Recovery did not erase any failure. X1 Method Flow retains ten failed and ten passing witnesses; the x2 companion ledger retains {len(X2_NEGATIVES)} failed and {len(X2_NEGATIVES)} passing witnesses. Preferred status applies only to each recorded bounded trigger.

The inherited 14 open gaps and 15 exact gates remain open. The eROSITA study adds one open gap and the navigation-chart authority matrix adds one exact gate, producing 15 effective open gaps and 16 effective exact gates. None was silently closed. The phase remains NOT_READY_FOR_STAGE_20.

## Validation and next gate

This evidence packet is designed for current-phase tests, eligible recent-round and successor-scoped tests, detailed and minimal validators, complete JSON parsing, five-class privacy and raw-identifier scanning, exact staged-file review, manifest parity, stale-label review, diff hygiene, ancestry, zero merges, commit-cap, single-parent history, exact head, clean state, and four-way remote equality. Eiren alone owns the complete repository suite; Sylven does not run it.

After an additive evidence commit, a combined closeout and seal commit may be prepared if every bounded check passes. The exact final head must then pass canonical validation and exactly one clean local-only named replay. Canonical plus named replay is same-owner repeatability under shared infrastructure only, never independent-team scientific reproduction. The Eiren route remains PREPARED_NOT_SENT until all final gates pass and one existing-task message is acknowledged.

{d.TRUTH_BOUNDARY}
"""


def static_report() -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v646-v6 bounded evidence report</title><style>body{{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:1.5rem;line-height:1.55}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #777;padding:.5rem;text-align:left;vertical-align:top}}th{{background:#eee;color:#111}}.hold{{border-left:.4rem solid #8b0000;padding-left:1rem}}a:focus{{outline:3px solid #005fcc;outline-offset:2px}}@media print{{body{{max-width:none}}}}</style></head><body><a href="#main">Skip to evidence</a><header><h1>Sylven Arc v646-v6 bounded evidence report</h1><p>Static structural report. Manual keyboard, pointer, browser, responsive-layout, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved.</p></header><main id="main"><section aria-labelledby="verdict"><h2 id="verdict">Verdict</h2><p class="hold"><strong>NOT_READY_FOR_STAGE_20.</strong> Six completed structural or synthetic surfaces, two represented proxies, one open gap, and one exact gate do not establish empirical confirmation or authority.</p></section><section aria-labelledby="outcomes"><h2 id="outcomes">Core outcomes</h2><table><caption>Permitted outcome vocabulary and bounded meaning</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody><tr><th scope="row">P01</th><td>completed</td><td>Owner-local durable-outbox workflow only.</td></tr><tr><th scope="row">P02</th><td>completed</td><td>Typed Schwinger-Dyson obligations; no physical result.</td></tr><tr><th scope="row">P03</th><td>open_gap</td><td>Zero eROSITA rows, likelihoods, or constraints.</td></tr><tr><th scope="row">P04</th><td>represented</td><td>Synthetic hydrographic handover; no operations.</td></tr><tr><th scope="row">P05</th><td>represented</td><td>Synthetic DPoP vectors; no real keys or tokens.</td></tr><tr><th scope="row">P06</th><td>exact_gate</td><td>Publication, place-name, legal, affected-party, and Māori authority reserved.</td></tr><tr><th scope="row">P07</th><td>completed</td><td>Disposable JSON-sequence fixture only.</td></tr><tr><th scope="row">P08</th><td>completed</td><td>Structural pointer audit; manual evaluation reserved.</td></tr><tr><th scope="row">P09</th><td>completed</td><td>Thermodynamic formal classifier; no psyche conversion.</td></tr><tr><th scope="row">P10</th><td>completed</td><td>Synthetic decision-curve refusal; Stage 20 held.</td></tr></tbody></table></section><section aria-labelledby="negative"><h2 id="negative">Negative and gate truth</h2><ul><li>{d.INHERITED_EFFECTIVE_NEGATIVES + 10 + d.PREREGISTERED_SYNTHETIC_NEGATIVES + len(X2_NEGATIVES)} effective negatives at evidence stage.</li><li>15 effective open gaps.</li><li>16 effective exact gates.</li><li>70 of 70 preregistered synthetic mutations rejected and retained.</li><li>No full repository suite; Eiren alone owns it.</li></ul></section><section aria-labelledby="boundaries"><h2 id="boundaries">Reserved boundaries</h2><p>{d.TRUTH_BOUNDARY}</p></section></main><footer><p>Owner-scoped static artifact. Same-owner checks are not independent reproduction.</p></footer></body></html>"""


def main() -> int:
    write_phase_artifacts()
    for command in (
        [sys.executable, str(ROOT / "scripts/ghc_family_v646_v6_portfolio_runner.py")],
        [sys.executable, str(ROOT / "scripts/ghc_family_v646_v6_skill_runner.py")],
        [sys.executable, str(ROOT / "scripts/ghc_family_v646_v6_source_gate.py")],
    ):
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")
    build_x2_method_flow()
    ledger = proposal_ledger()
    write_json("x2-proposal-ledger.json", ledger)
    write_json(
        "validation/x2-operational-negatives.json",
        {
            "schema": "ghc.family.v646-v6.x2-operational-negatives.v1",
            "count": len(X2_NEGATIVES),
            "negatives": [{"negative_id": row["negative_id"], "failure": row["failure"], "recovery": row["recovery"], "retained": True} for row in X2_NEGATIVES],
            "failure_erasure_count": 0,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    effective_total = d.INHERITED_EFFECTIVE_NEGATIVES + 10 + d.PREREGISTERED_SYNTHETIC_NEGATIVES + len(X2_NEGATIVES)
    write_json(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v646-v6.retained-negatives.v1",
            "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES,
            "x1_operational": 10,
            "preregistered_synthetic_executed_and_rejected": d.PREREGISTERED_SYNTHETIC_NEGATIVES,
            "x2_operational": len(X2_NEGATIVES),
            "effective_total": effective_total,
            "no_negative_erased": True,
            "failure_erasure_count": 0,
            "same_owner_only": True,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v646-v6.gates.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "new_open_gaps": [{"proposal_id": "V6466-P03", "title": d.PROPOSALS[2]["title"], "state": "open"}],
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": [{"proposal_id": "V6466-P06", "title": d.PROPOSALS[5]["title"], "state": "exact_gate"}],
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "silently_closed": 0,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v646-v6.threat-model.v1",
            "assets": ["x1 freeze", "retained negatives", "source status", "zero-row lock", "synthetic-only fixtures", "authority reservations", "remote equality"],
            "threats": [
                {"threat": "x1_x2_phase_mix", "control": "dedicated remote-equal x1 commit and content seal", "residual": "watch"},
                {"threat": "source_to_observation_conversion", "control": "zero-row and citation-observation firewall", "residual": "open_gap"},
                {"threat": "hydrographic_or_place_name_authority_substitution", "control": "exact-gate matrix and zero real cases", "residual": "exact_gate"},
                {"threat": "real_key_or_token_leakage", "control": "synthetic values and five-class scan", "residual": "independent privacy and security review open"},
                {"threat": "invalid_json_sequence_smuggling", "control": "failed-element retention and torn-tail refusal", "residual": "not exhaustive security"},
                {"threat": "accessibility_overclaim", "control": "structural-only labels and manual reservations", "residual": "manual and affected-user review open"},
                {"threat": "stage20_metric_or_value_laundering", "control": "threshold-authority and nonpromotion board", "residual": "stage20 held"},
                {"threat": "private_material_in_public_artifacts", "control": "five-class full-file scan with candidates separated from confirmed hits", "residual": "complete privacy assurance open"},
            ],
            "exhaustive_security_claimed": False,
            "privacy_complete_claimed": False,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    runner_names = [name for name, _ in d.RUNNERS]
    invoked = {
        "ghc_family_v646_v6_runtime.py",
        "ghc_family_v646_v6_core_runner.py",
        "ghc_family_v646_v6_portfolio_runner.py",
        "ghc_family_v646_v6_skill_runner.py",
        "ghc_family_v646_v6_outbox_tribunal.py",
        "ghc_family_v646_v6_json_sequence_tribunal.py",
        "ghc_family_v646_v6_source_gate.py",
    }
    runner_rows = [
        {"name": name, "path": f"scripts/{name}", "built": (ROOT / "scripts" / name).is_file(), "invoked_before_evidence": name in invoked, "family_current_name": name.startswith("ghc_family_")}
        for name in runner_names
    ]
    write_json(
        "prototypes/runner-build-use-receipt.json",
        {
            "schema": "ghc.family.v646-v6.runner-build-use.v1",
            "runners": runner_rows,
            "runner_count": len(runner_rows),
            "built_count": sum(row["built"] for row in runner_rows),
            "invoked_before_evidence_count": sum(row["invoked_before_evidence"] for row in runner_rows),
            "compatibility_preserved": True,
            "result": "pass" if len(runner_rows) == 10 and all(row["built"] and row["family_current_name"] for row in runner_rows) else "fail",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    owner_files = [path for path in PHASE.rglob("*") if path.is_file()]
    write_json(
        "environment/x2-environment-receipt.json",
        {
            "schema": "ghc.family.v646-v6.x2-environment.v1",
            "owner_generated_files_at_evidence": len(owner_files),
            "rotation_threshold": 15000,
            "rotation_required": len(owner_files) >= 15000,
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "codex_cli": "0.144.4 verified only",
            "codex_desktop": "26.707.9981.0 verified only",
            "sandbox_available": False,
            "desktop_updated": False,
            "elevated": False,
            "security_weakened": False,
            "windows_feature_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        },
    )
    write_json(
        "evidence/phase-truth.json",
        {
            "schema": "ghc.family.v646-v6.evidence-phase-truth.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_revision": d.SOURCE_REVISION,
            "x1_revision": X1_REVISION,
            "state": "x2_evidence_complete_pending_closeout_and_seal",
            "proposal_distribution": ledger["distribution"],
            "effective_negatives": effective_total,
            "effective_open_gaps": 15,
            "effective_exact_gates": 16,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "full_repository_suite_run": False,
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v646-v6.checklist.v1",
            "complete": [
                "skill and schema startup",
                "source and live-remote gate",
                "dedicated x1 remote-equal freeze",
                "440-proposal novelty audit",
                "ten proposal execution within evidence bounds",
                "70 synthetic negative rejections",
                "30 safe, 20 candidate, 20 skill, 10 runner, and 30 cleanup portfolio execution",
                "source-use refusal gate",
                "threat model and accessible static evidence report",
            ],
            "incomplete": [
                "combined closeout and seal commit",
                "canonical exact-final scoped validation",
                "one clean local-only named replay",
                "final four-way remote equality",
                "one acknowledged Eiren v646-v7 baton",
                "real eROSITA data and independent review",
                "real THOS arms and professional review",
                "production Freed ID",
                "CBR, legal, affected-party, cultural, place-name, and Māori authority",
                "manual and affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20 readiness",
            ],
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "orchestration/x2-update.json",
        {
            "schema": "ghc.family.v646-v6.x2-update.v1",
            "state": "evidence_complete_pending_closeout",
            "x1_revision": X1_REVISION,
            "route": "PREPARED_NOT_SENT",
            "send_count": 0,
            "standby_contact_count": 0,
            "task_creation_count": 0,
            "delegation_count": 0,
        },
    )
    write_text("v646-v6-integrated-overview.md", overview())
    write_text("deliverables/v646-v6-evidence-report.html", static_report())
    write_text(
        "deliverables/v646-v6-x2-wellbeing.md",
        f"""# Sylven Arc v646-v6 x2 wellbeing and workload check

- The phase stayed solo, owner-scoped, additive, and within three planned phase commits.
- {len(X2_NEGATIVES)} x2 tooling failures remain retained with passing bounded recoveries; no failure was erased.
- No real people, operations, rows, keys, tokens, publications, decisions, or authority were used.
- Eiren's complete repository suite was not run.
- Windows Sandbox remains unavailable; no elevation, feature change, install, security weakening, desktop update, or reboot occurred.
- Identity language remains relational only and does not establish welfare, consciousness, employment, qualification, or authority.
""",
    )
    evidence_files = [path for path in PHASE.rglob("*") if path.is_file() and "validation/evidence-build-manifest.json" not in path.as_posix()]
    write_json(
        "validation/evidence-build-manifest.json",
        {
            "schema": "ghc.family.v646-v6.evidence-build-manifest.v1",
            "hash_domain": "working_tree_bytes_before_staging",
            "entries": [
                {"path": path.relative_to(PHASE).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                for path in sorted(evidence_files)
            ],
            "entry_count": len(evidence_files),
            "self_excluded": True,
        },
    )
    write_json(
        "evidence-receipt.json",
        {
            "schema": "ghc.family.v646-v6.evidence-receipt.v1",
            "state": "evidence_complete_pending_commit",
            "x1_revision": X1_REVISION,
            "core_surfaces": 10,
            "distribution": ledger["distribution"],
            "synthetic_negatives_executed": 70,
            "synthetic_negatives_rejected": 70,
            "effective_negatives": effective_total,
            "effective_open_gaps": 15,
            "effective_exact_gates": 16,
            "full_repository_suite_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    result = {
        "proposals": ledger["proposal_count"],
        "distribution": ledger["distribution"],
        "synthetic_negatives": 70,
        "effective_negatives": effective_total,
        "open_gaps": 15,
        "exact_gates": 16,
        "x2_operational_negatives": len(X2_NEGATIVES),
        "result": "pass",
    }
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
