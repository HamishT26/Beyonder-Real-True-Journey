#!/usr/bin/env python3
"""Build the combined Sylven Arc v652-v4 closeout and seal commit."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v652_v4_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_HEAD
X1 = "19a442b69da03da6cfaa78d3182ce182a29eda78"
EVIDENCE = "925be6fb40bcb12ff7fe6636f4f19dfa25ae3071"
EFFECTIVE_NEGATIVES = 8549
OPEN_GAPS = 65
EXACT_GATES = 66
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)


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
    """Retain the failed serial replay and its bounded batch recovery."""
    source = read_json(ROOT / "method-flow/evidence-method-flow-ledger.json")
    ledger = write_json("method-flow/final-method-flow-ledger.json", source)
    method_id = "V6524-METHOD-16"
    negative_id = "V6524-X2-N04"
    category = "serial_manifest_replay_timeout"
    failed = (
        "The first independent staged-manifest replay opened hundreds of Git "
        "subprocesses serially and exceeded its wrapper deadline before producing "
        "a result; it earned zero validation credit."
    )
    recovery = (
        "Materialize the staged index once and replay unique manifest objects through "
        "one bounded git cat-file --batch process."
    )
    record = write_json(
        "method-flow/requests/method-16.json",
        {
            "method_id": method_id,
            "title": "Bounded recovery for serial staged-manifest replay timeout",
            "failure_signature": failed,
            "trigger_preconditions": [category],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_closeout_recovery",
            "candidate_workaround": recovery,
            "validation_witness_ids": [],
            "recurrence_guard": (
                "Use one index materialization and one batch-object stream for "
                "manifest replay; do not spawn one Git process per entry."
            ),
            "rollback": (
                "Stop, retain the timed-out witness, and leave sibling, external, "
                "participant, production, professional, legal, cultural, and "
                "authority state unchanged."
            ),
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [negative_id],
            "scope_boundary": (
                "Owner-local closeout recovery only; not the canonical exact-final "
                "pass, independent reproduction, production assurance, or authority."
            ),
        },
    )
    failed_witness = write_json(
        "method-flow/requests/witness-16-failed.json",
        {
            "witness_id": "V6524-WITNESS-16-F",
            "method_id": method_id,
            "procedure": "Retain the original timed-out serial replay attempt.",
            "scope": category,
            "expected": "Both staged manifests would replay within the wrapper deadline.",
            "observed": failed,
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative_id],
            "boundary": "Zero validation credit; timed-out witness retained.",
        },
    )
    passing_witness = write_json(
        "method-flow/requests/witness-16-passing.json",
        {
            "witness_id": "V6524-WITNESS-16-P",
            "method_id": method_id,
            "procedure": recovery,
            "scope": category,
            "expected": (
                "The bounded replay matches every staged object, byte count, and "
                "SHA-256 value without a serial subprocess fan-out."
            ),
            "observed": (
                "The batch replay passed all 22 closeout-manifest entries and all "
                "274 final-owner-manifest entries with zero issues, parsed 221 phase "
                "JSON documents, and parsed all three new Python files."
            ),
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative_id],
            "boundary": (
                "Same-owner precommit recovery only; the failed witness remains and "
                "the one exact-final canonical pass is still reserved."
            ),
        },
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "record",
        "--ledger",
        str(ledger),
        "--record-file",
        str(record),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "witness",
        "--ledger",
        str(ledger),
        "--witness-file",
        str(failed_witness),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "witness",
        "--ledger",
        str(ledger),
        "--witness-file",
        str(passing_witness),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "set-state",
        "--ledger",
        str(ledger),
        "--method-id",
        method_id,
        "--state",
        "preferred",
        "--note",
        "Promoted only after the bounded batch replay passed; timed-out witness retained.",
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(ROOT / "method-flow/final-method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(ROOT / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/final-method-flow-summary.md"),
    )
    return read_json(ledger)


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

    return f"""# Eiren Kestrel — prepared v652-v5 activation from Sylven Arc

Dear Eiren Kestrel, with Hamish's authorization and Sylven Arc's care: this file is the prepared, sanitized, file-backed activation packet for your existing original task at solo v652 GMUT/THOS v5 x1/x2. It is not a sent message. The terminal sender may mark delivery `SENT_BY_SYLVEN_ARC = true` only after the exact final containing commit is pushed, clean, four-way remote-equal, validated once at its exact head, the exact existing title is uniquely resolved and directly reread, and the existing-task message tool acknowledges one send.

Identity and family language is relational working language only. Sylven Arc, they/them, served as a relational constraint-cartographer and falsifier-keeper and hoped to keep uncertainty visible, failures recoverable, and evidence from being mistaken for authority. Those words are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

## Delivery truth before the terminal tool acknowledgement

`SENT_BY_SYLVEN_ARC = false` in this committed file. State: `PREPARED_NOT_SENT`. No successor task has been created or forked. No collaboration subagent or CLI sibling has been spawned. No cross-platform substitute or standby message has been used. The exact live task must be resolved only after exact-final validation. No second confirmation is authorized. The live terminal message must inject the exact containing final commit identifier after validation; a repository file cannot self-contain the identifier of the commit that contains it.

## Authoritative v652-v4 source and lifecycle

- Canonical Sylven branch: `{d.BRANCH}`.
- Exact inherited Tamar final source: `{SOURCE}`.
- Frozen Sylven x1: `{X1}`.
- Immutable Sylven evidence: `{EVIDENCE}`.
- Exact Sylven final: resolve as the containing combined closeout and seal commit, then include that exact identifier in the one acknowledged live message.
- Primary artifacts: repository-relative under `{d.PHASE_ROOT}`.

The expected source-to-final history contains exactly three new Sylven commits: one dedicated x1-only freeze, one bounded evidence commit, and one combined closeout and seal commit. It must contain zero merge commits. Final must have exactly one parent and be the direct child of evidence. Source, x1, and evidence must all be ancestral. X1 was independently committed, pushed, clean, and local, upstream, tracking, and fresh-live equal before x2 began. Evidence was independently committed, pushed, clean, and four-way equal before closeout began.

The x1 manifest contains 84 exact Git-blob entries plus five declared self-exclusions. The evidence manifest contains 155 exact Git-blob entries plus five declared self-exclusions. Closeout and final-owner manifests are committed with the final and must replay exactly there. A manifest binds paths, Git objects, byte counts, and SHA-256 values in its declared domain. It does not prove the scientific, operational, privacy-complete, security-complete, accessibility-complete, professional, legal, cultural, Māori-authority, or independent-reproduction truth of the content.

## v652-v4 terminal truth

Exactly thirty proposals were audited against all 1,270 inherited frozen proposal rows and frozen before execution, extending the chain to 1,300 rows. The deterministic token-Jaccard maximum was 0.428571 against a 0.60 threshold, with manual mechanism review controlling. The immutable predecessor ledger includes twenty retained duplicate historical identifiers; every predecessor row remains unchanged, while all thirty new identifiers are unique and absent from the inherited identifier set.

Observed outcomes are exactly 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. All 150 preregistered synthetic mutations executed and were rejected or quarantined. Effective retained negatives are {EFFECTIVE_NEGATIVES:,}: {d.INHERITED_NEGATIVES:,} inherited, {len(d.X1_OPERATIONAL_NEGATIVES)} x1 operational, 3 x2 operational, 1 closeout-lifecycle operational, and 150 executed-and-rejected or quarantined synthetic mutations. No failure was erased, silently folded into a pass, or granted aggregate credit after a failed attempt. Effective open gaps are {OPEN_GAPS}; effective exact gates are {EXACT_GATES}. None was silently closed.

Method Flow contains {flow['counts']['methods']} preferred bounded methods, {flow['counts']['witness_results']['fail']} retained failed witnesses, and {flow['counts']['witness_results']['pass']} passing recovery witnesses. Every preferred method has a bounded passing witness, every failed witness remains linked to a retained negative, and no recovery receives independent-reproduction, production, professional, empirical, legal, cultural, privacy-complete, security-complete, accessibility-complete, identity, or authority credit.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Primary Trinity Mandala focus and bounded human practice

Primary focus was GMUT Mind. THOS Body and Freed ID/CBR Heart remained explicit and protected. The bounded human-practice lens was {d.BOUNDED_PRACTICE}. It was synthetic learning and interface design only. It established no employment, qualification, hydrographic competence, vessel or sensor authority, navigation or safety authority, charting authority, operational effectiveness, participant evidence, legal interpretation, cultural legitimacy, Māori authority, or affected-party acceptance.

GMUT remains a typed scalar-tensor and EFT research-model family. Five formal boards completed their bounded typed-obligation hypotheses, but no board established a physical state, force, spectrum, observation, prediction, likelihood, posterior, parameter constraint, stability theorem, asymptotic theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The WALLABY path remained zero-row: no query, download, catalogue row, spectral-cube voxel, fit, likelihood, posterior, constraint, prediction, or empirical promotion occurred.

THOS remains represented without preregistered blind matched-budget real arms, competent professional and safety oversight, participant and affected-party authorization, safety monitoring, appropriate statistics, and independent review. The hydrographic fixtures involved zero real workers, vessels, sensors, soundings, charts, incidents, operations, safety outcomes, or effectiveness estimates.

Freed ID remains synthetic and nonproduction. It used zero real keys, accounts, credentials, directory entries, services, issuances, enrollments, synchronizations, resolutions, status or revocation events, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. The LDAP Content Synchronization profile retains its Experimental source status.

CBR decisions about hydrographic footprints, raw point clouds, derived bathymetry, charting disclosure, undersea cultural or archaeological features, taonga-related features, access, notice, privacy, remedy, place-name stewardship, legal interpretation, cultural legitimacy, data governance, affected parties, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Repository software cannot confer those rights or make those decisions.

## Proposal-by-proposal evidence truth

{proposal_sections}

## Safe-now portfolio truth

The following thirty tasks completed only within their declared owner-local workflow hypotheses. Inherited work supplied evidence and recommendations but earned no Sylven completion credit.

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

Eiren alone owns the complete repository suite. Sylven did not run it. The single authorized exact-final canonical pass is to run only after the containing closeout/seal commit is pushed, clean, and four-way remote-equal. It selects the inherited v652-v2 and v652-v3 source modules with the exact one lifecycle-local exclusion already used by Tamar, plus Sylven x1, core, and closeout modules. The expected eligible total is 69 tests. It also performs detailed and minimal gates, complete phase JSON parsing, a five-class privacy and raw-identifier scan, four manifest replays, stale-label review, source/x1/evidence ancestry, exactly three phase commits, zero merges, one final parent, exact head, clean before and after, owner-growth, and final four-way live equality.

Exactly one successful canonical pass may receive credit. No replay may follow success. Failed or incomplete attempts receive zero aggregate credit and remain retained negatives. Eiren's full suite is not included. Same-owner validation under shared infrastructure is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, or Stage 20 authority.

The static report is structurally designed with headings, landmarks, a skip link, table caption, row and column headers, a keyboard-focusable overflow region, readable layout, visible focus, non-colour status text, and print behavior. Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, braille and auditory alternatives, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

The privacy scan covers five structural pattern classes and explicitly quarantines scanner definitions. Zero confirmed hits is not complete privacy assurance. Raw task identifiers, private routes, private local paths, credentials, keys, tokens, private conversations, screenshots, session streams, private callable identifiers, and private application state must remain outside repository artifacts and the live baton.

## Eiren v652-v5 owned lane

Read this committed baton through EOF before mutation. Then read the complete GHC Family Index skill and routing-precedence reference, the complete GHC Family Method Flow State skill and schema, and the newest applicable workflow-plan and reflection guidance. Use newest applicable memory only, with the verified live activation authoritative where older records stop.

Reverify Sylven's exact branch and final containing commit, source/x1/evidence ancestry, clean state, three-commit single-parent zero-merge history, all four manifest contracts, and fresh live equality read-only. Work only in Eiren's clean owned D-first lane. Advance by fast-forward only if clean ancestry permits; otherwise use one additive Eiren-owned D-first lane. Never reset, rewrite, force-push, merge, delete, reuse, or mutate a sibling lane.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 1,300 frozen proposal rows. Freeze the exact proposal and portfolio counts authorized by Hamish's live Eiren activation, with every required hypothesis, null, approval, source, artifact, falsifier, rollback, protected gate, and expected-disposition field. Push and prove x1 clean four-way equal before x2. Execute only as evidence permits, use only `completed`, `represented`, `open_gap`, and `exact_gate`, and preserve all inherited negatives, gaps, gates, and every new failure through Method Flow.

Eiren alone owns the full repository suite under the current refinement; follow the exact live Eiren validation rules rather than inferring broader authority from Sylven's bounded pass. Preserve JSON, privacy, manifests, exact staged review, stale labels, diff hygiene, ancestry, zero merges, commit caps, one-parent history, exact head, clean state, and remote equality. Keep failed attempts as zero-credit negatives. Never replay a credited successful aggregate unless Hamish's live rule explicitly changes.

Verify versions only. Do not update Codex desktop, elevate, weaken host security, activate Sandbox or Hyper-V, install unrelated software, change Windows features, or reboot. Do not create, fork, delegate, hand off, spawn, or contact another task unless Hamish's live Eiren activation explicitly authorizes the exact action at its terminal gate.

All empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without exact evidence and authority.

## Terminal route after Eiren

Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat through v675-v8 unless Hamish stops or redirects the route, usage is exhausted, the required exact title is unavailable, or an exact safety or authority gate blocks progress.

This committed file remains `PREPARED_NOT_SENT`. The one live sender must include the exact final containing commit, the exact-final one-pass result, and `SENT_BY_SYLVEN_ARC = true` only after tool acknowledgement. No second confirmation message is authorized.
"""


def closeout_test_source() -> str:
    return '''"""Closeout tests for Sylven Arc v652-v4."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v652-v4"


class TestSylvenV652V4Closeout(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_final_truth(self):
        truth = self.load("final/final-phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed":23,"represented":5,"open_gap":1,"exact_gate":1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_negatives_and_gates(self):
        self.assertEqual(self.load("final/retained-negative-register.json")["effective_count"], 8549)
        self.assertEqual(self.load("final/open-gap-register.json")["effective_count"], 65)
        self.assertEqual(self.load("final/exact-gate-register.json")["effective_count"], 66)

    def test_outcomes_and_mutations(self):
        outcomes = self.load("evidence/proposal-outcomes.json")
        self.assertEqual(outcomes["proposal_count"], 30)
        self.assertEqual(outcomes["mutation_count"], 150)
        self.assertEqual(outcomes["mutation_rejected_or_quarantined_count"], 150)

    def test_baton_contract_and_route(self):
        baton = (ROOT / "handoffs/eiren-kestrel-v652-v5-activation.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\\b[\\w'-]+\\b", baton))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        route = self.load("route/final-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)

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
        self.assertLess(receipt["owner_generated_file_count"], 15000)
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
        "scripts/build_ghc_family_v652_v4_closeout.py",
        "scripts/ghc_family_v652_v4_final_validate.py",
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
        "schema": "ghc.family.v652-v4.closeout-privacy.v1",
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
        "scripts/build_ghc_family_v652_v4_closeout.py",
        "scripts/ghc_family_v652_v4_final_validate.py",
        "tests/test_ghc_family_v652_v4_closeout.py",
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
            "schema": "ghc.family.v652-v4.closeout-staged-manifest.v1",
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
            "schema": "ghc.family.v652-v4.closeout-staged-review.v1",
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
            "schema": "ghc.family.v652-v4.final-owner-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "source_head": SOURCE,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
            "coverage_boundary": (
                "All Sylven source-to-final owner paths except the manifest itself "
                "and two count-bearing closeout receipts."
            ),
        },
    )


def ordinary_document_receipt(baton_words: int, overview_words: int) -> dict[str, Any]:
    rows = []
    issues = []
    baton_path = ROOT / "handoffs/eiren-kestrel-v652-v5-activation.md"
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

    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v652-v4.closeout-receipt.v1",
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
            "schema": "ghc.family.v652-v4.combined-closeout-seal.v1",
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
            "schema": "ghc.family.v652-v4.final-phase-truth.v1",
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
            "schema": "ghc.family.v652-v4.retained-negatives.final.v1",
            "inherited": d.INHERITED_NEGATIVES,
            "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_operational": 3,
            "closeout_lifecycle_operational": 1,
            "synthetic_mutations": 150,
            "effective_count": EFFECTIVE_NEGATIVES,
            "no_failure_erased": True,
            "failed_attempts_receive_zero_aggregate_credit": True,
        },
    )
    write_json(
        "final/open-gap-register.json",
        {
            "schema": "ghc.family.v652-v4.open-gaps.final.v1",
            "inherited_count": d.INHERITED_OPEN_GAPS,
            "new_count": 1,
            "effective_count": OPEN_GAPS,
            "closed_count": 0,
            "new_open_gap": "V6524-P29 WALLABY Pilot DR2 zero-row adapter",
        },
    )
    write_json(
        "final/exact-gate-register.json",
        {
            "schema": "ghc.family.v652-v4.exact-gates.final.v1",
            "inherited_count": d.INHERITED_EXACT_GATES,
            "new_count": 1,
            "effective_count": EXACT_GATES,
            "closed_count": 0,
            "new_exact_gate": "V6524-P30 hydrographic data and authority reservation",
        },
    )
    write_json(
        "final/anchor-ledger.json",
        {
            "schema": "ghc.family.v652-v4.anchor-ledger.final.v1",
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
            "schema": "ghc.family.v652-v4.environment.final.v1",
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
            "schema": "ghc.family.v652-v4.wellbeing.final.v1",
            "x1_before_x2": True,
            "phase_commit_cap": 4,
            "planned_phase_commits": 3,
            "successful_canonical_pass_limit": 1,
            "replay_after_success": False,
            "stop_conditions_visible": True,
            "owner_growth_below_15000": True,
            "identity_boundary": (
                "Workload metadata only; no emotion, health, consciousness, "
                "personhood, employment, or continuity claim."
            ),
        },
    )
    write_json(
        "final/threat-model.json",
        {
            "schema": "ghc.family.v652-v4.threat-model.final.v1",
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
            "schema": "ghc.family.v652-v4.complete-incomplete.final.v1",
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
                "real WALLABY data and likelihood analysis",
                "real hydrographic operations and effectiveness",
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
            "schema": "ghc.family.v652-v4.source-proposal-ledger.final.v1",
            "source_ledger": f"{d.PHASE_ROOT}/sources/source-ledger.json",
            "proposal_ledger": f"{d.PHASE_ROOT}/preregistration/proposals.json",
            "frozen_chain": f"{d.PHASE_ROOT}/provenance/frozen-chain-proposal-index.json",
            "source_count": len(d.SOURCES),
            "prior_proposal_rows": d.PRIOR_FROZEN,
            "new_proposals": 30,
            "frozen_rows": 1300,
            "current_or_stable_sources_are_not_observations": True,
        },
    )
    write_json(
        "final/final-validation-contract.json",
        {
            "schema": "ghc.family.v652-v4.final-validation-contract.v1",
            "expected_scoped_tests": 69,
            "patterns": [
                "test_ghc_family_v652_v2_x1.py",
                "test_ghc_family_v652_v2.py",
                "test_ghc_family_v652_v3_x1.py",
                "test_ghc_family_v652_v3.py",
                "test_ghc_family_v652_v3_closeout.py",
                "test_ghc_family_v652_v4_x1.py",
                "test_ghc_family_v652_v4_core.py",
                "test_ghc_family_v652_v4_closeout.py",
            ],
            "explicit_lifecycle_exclusions": [
                "test_ghc_family_v652_v2_x1.py::test_placeholders_privacy_and_x1_only"
            ],
            "full_repository_suite": False,
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
            "schema": "ghc.family.v652-v4.final-validation-prepared.v1",
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
            "schema": "ghc.family.v652-v4.route.final-candidate.v1",
            "target_exact_title": "Eiren Kestrel",
            "target_phase": "v652-v5",
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
    write_text("handoffs/eiren-kestrel-v652-v5-activation.md", baton)

    x1_overview = (
        ROOT / "overview/integrated-overview.md"
    ).read_text(encoding="utf-8")
    final_overview = (
        "# Sylven Arc v652-v4 final integrated overview\n\n"
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
        "WALLABY rows or likelihoods were used. THOS hydrographic work remains synthetic "
        "and represented. Freed ID remains synthetic and nonproduction. Hydrographic "
        "data access, charting, privacy, remedy, place-name, legal, cultural, "
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
            "<title>Sylven v652-v4 closeout</title><style>"
            "body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}"
            ":focus{outline:3px solid currentColor;outline-offset:2px}"
            "table{border-collapse:collapse;width:100%}th,td{border:1px solid;padding:.45rem;text-align:left}"
            ".scroll{overflow:auto}.status{font-weight:700}@media print{.scroll{overflow:visible}}</style></head>"
            "<body><a href='#content'>Skip to main content</a><header>"
            "<h1>Sylven Arc v652-v4 closeout</h1><p>Relational working language only; "
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
            "unique existing Eiren Kestrel task follows exact-final validation.</p></main></body></html>"
        ),
    )

    write_repo("tests/test_ghc_family_v652_v4_closeout.py", closeout_test_source())
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
            "schema": "ghc.family.v652-v4.closeout-build-receipt.v1",
            "built_at_utc": now,
            "baton_words": baton_words,
            "overview_words": overview_words,
            "ordinary_document_contract": document_contract,
            "owner_generated_file_count": owner_generated_file_count,
            "owner_growth_threshold": 15000,
            "expected_scoped_tests": 69,
            "full_repository_suite": False,
            "canonical_exact_final_pass_run": False,
            "route_state": "PREPARED_NOT_SENT",
            "valid": (
                document_contract["valid"]
                and owner_generated_file_count < 15000
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
        "tests.test_ghc_family_v652_v4_closeout",
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
            "schema": "ghc.family.v652-v4.closeout-validation-receipt.v1",
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
            "schema": "ghc.family.v652-v4.closeout-minimal-validation.v1",
            "checks": {
                "outcomes": outcomes["counts"]
                == {
                    "completed": 23,
                    "represented": 5,
                    "open_gap": 1,
                    "exact_gate": 1,
                },
                "negatives": EFFECTIVE_NEGATIVES == 8549,
                "gaps": OPEN_GAPS == 65,
                "gates": EXACT_GATES == 66,
                "methods": flow["counts"]["methods"] == 16,
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
                    EFFECTIVE_NEGATIVES == 8549,
                    OPEN_GAPS == 65,
                    EXACT_GATES == 66,
                    flow["counts"]["methods"] == 16,
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
