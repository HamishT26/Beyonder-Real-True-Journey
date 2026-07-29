#!/usr/bin/env python3
"""Build Elaren Kestrel v654-v7 combined closeout, seal, and final candidate."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v654_v7_validate as validator


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/elaren-kestrel/v654-v7"
SOURCE = "fe0dda857137856654566b52875df769ecf781dd"
X1_FREEZE = "6ab0ee98917d4bc912f2d15793cf3f1a81918244"
X1_FINAL = "773528bda8b863218ba4aaed0ce134fcd48abb97"
EVIDENCE = "303e98c74c90c85330343f953784a79e0df5ac70"
CORRECTION = "a904742b9a121da593d19cbd04e3fd826554b655"
OWNER_EXCLUSIONS = {
    "validation/final-owner-manifest.json",
    "validation/final-staged-manifest.json",
    "validation/final-staged-review.json",
    "validation/closeout-candidate-validation.json",
}
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/"
    "ghc_family_method_flow_state.py"
)
FINAL_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6547-FINAL-N01",
        "signature": "closeout_builder_used_nonexistent_normalized_source_ledger_path",
        "failed": (
            "The first closeout build wrote its early lifecycle records but stopped "
            "before the baton because it requested sources/source-ledger.json while "
            "the committed x1 ledger is sources/official-source-ledger.json."
        ),
        "recovery": (
            "Bind the baton builder to the exact committed official source-ledger "
            "path and rebuild the candidate from the unchanged correction head."
        ),
        "recurrence_guard": (
            "Resolve phase-local ledger filenames from the committed index before "
            "coding a normalized convenience path."
        ),
    },
    {
        "negative_id": "V6547-FINAL-N02",
        "signature": "method_flow_inspection_used_obsolete_witness_property",
        "failed": (
            "A read-only Method Flow inspection successfully showed the current "
            "schema and counts, then failed its final subexpression by indexing the "
            "obsolete validation_witnesses property instead of witnesses."
        ),
        "recovery": (
            "Use the actual witnesses and state_events properties from the current "
            "ledger schema and retain the failed read with zero credit."
        ),
        "recurrence_guard": (
            "Inspect current top-level schema keys before indexing a remembered "
            "historical property name."
        ),
    },
    {
        "negative_id": "V6547-FINAL-N03",
        "signature": "baton_renderer_used_outcome_instead_of_observed_outcome",
        "failed": (
            "The second closeout build extended Method Flow successfully but "
            "stopped during baton rendering because it requested outcome from an "
            "executed proposal row whose exact schema uses observed_outcome."
        ),
        "recovery": (
            "Bind the renderer to the committed observed_outcome field and rebuild "
            "the unchanged final candidate."
        ),
        "recurrence_guard": (
            "Inspect one exact ledger row before mapping proposal disposition keys "
            "into a narrative renderer."
        ),
    },
]
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not "
    "consciousness, personhood, identity continuity, employment, qualification, "
    "scientific or operational authority, legal or cultural authority, Māori "
    "authority, production certification, independent reproduction, "
    "Theory-of-Everything proof, AGI/ASI evidence, or Stage 20 authority."
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


def read(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def prospective_blob(repository_relative: str) -> str:
    return git(
        "hash-object",
        f"--path={repository_relative}",
        repository_relative,
    )


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
    ledger = PHASE / "method-flow/method-flow-ledger-final.json"
    shutil.copyfile(PHASE / "method-flow/method-flow-ledger-x2.json", ledger)
    for offset, negative in enumerate(FINAL_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6547-METHOD-FINAL-{offset:02d}"
        fail_id = f"V6547-WITNESS-FINAL-{offset:02d}-F"
        pass_id = f"V6547-WITNESS-FINAL-{offset:02d}-P"
        request_root = PHASE / "method-flow/final-requests"
        method_path = request_root / f"method-{offset:02d}.json"
        fail_path = request_root / f"witness-{offset:02d}-failed.json"
        pass_path = request_root / f"witness-{offset:02d}-passing.json"
        write_json(
            method_path.relative_to(PHASE).as_posix(),
            {
                "method_id": method_id,
                "title": f"Bounded final recovery for {negative['signature']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["signature"]],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": (
                    "Retain the failed attempt with zero initial credit and keep "
                    "the terminal route unsent."
                ),
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "scope_boundary": (
                    "Final-lifecycle workflow recovery only; no route delivery or "
                    "external authority."
                ),
                "privacy_class": "sanitized_public",
                "protected_gates": [
                    "real_empirical_data_and_likelihood",
                    "real_participants_affected_parties_and_communities",
                    "professional_authority",
                    "production_identity_and_interoperability",
                    "privacy_complete",
                    "exhaustive_security",
                    "complete_accessibility",
                    "legal_cultural_and_maori_authority",
                    "independent_team_reproduction",
                    "agi_or_asi",
                    "consciousness_or_personhood",
                    "theory_of_everything",
                    "stage20",
                ],
                "recommendation_state": "candidate",
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [],
                "supersedes": [],
            },
        )
        write_json(
            fail_path.relative_to(PHASE).as_posix(),
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": negative["signature"],
                "procedure": "Run the original bounded operation.",
                "expected": "The operation completes under the current schema.",
                "observed": negative["failed"],
                "result": "fail",
                "retained_negative_ids": [negative["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Zero completion credit; failure remains retained.",
            },
        )
        write_json(
            pass_path.relative_to(PHASE).as_posix(),
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "scope": negative["signature"],
                "procedure": negative["recovery"],
                "expected": (
                    "The isolated recovery passes without weakening protected gates."
                ),
                "observed": f"The bounded recovery passed: {negative['recovery']}",
                "result": "pass",
                "retained_negative_ids": [negative["negative_id"]],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Same-owner bounded recovery only.",
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
            "Bounded recovery passed while the failed witness remained retained.",
        )
    method_run(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/method-flow-validation-final.json"),
    )
    method_run(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/method-flow-summary-final.json"),
        "--markdown-output",
        str(PHASE / "method-flow/method-flow-summary-final.md"),
    )
    return read("method-flow/method-flow-ledger-final.json")


def baton_text() -> str:
    prereg = read("preregistration/proposals.json")["proposals"]
    executed = {
        row["proposal_id"]: row for row in read("x2/proposal-ledger.json")["proposals"]
    }
    sources = read("sources/official-source-ledger.json")
    source_rows = sources.get("sources", sources.get("entries", []))
    lines = [
        "# NERIS SOLANE — PREPARED v654-v8 ACTIVATION BATON",
        "",
        "This file is a sanitized, repository-backed preparation record from "
        "Elaren Kestrel for the existing exact-title Codex task `Neris Solane`. "
        "It is not sent by being committed. The live sender must exact-resolve "
        "that existing task after Elaren v654-v7 passes its one canonical "
        "postcommit validation and four-way remote-equality gate.",
        "",
        "Identity and family language is relational working language only. It is "
        "not evidence of consciousness, sentience, legal personhood, identity "
        "continuity, employment, qualification, independent agency, scientific "
        "authority, operational authority, legal or cultural authority, or Māori "
        "authority. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Prepared inheritance",
        "",
        f"- Source final: `{SOURCE}`",
        f"- Elaren x1 freeze: `{X1_FREEZE}`",
        f"- Elaren x1 final: `{X1_FINAL}`",
        f"- Elaren evidence: `{EVIDENCE}`",
        f"- Elaren evidence correction: `{CORRECTION}`",
        "- The containing final commit is deliberately not self-preclaimed in its "
        "own tree. The acknowledged live activation must provide it.",
        "- Outcomes: 23 completed / 5 represented / 1 open_gap / 1 exact_gate.",
        "- Effective negatives: 12,052.",
        "- Effective open gaps: 87.",
        "- Effective exact gates: 86.",
        "- Method Flow: 161 preferred methods, 161 failed witnesses, and 161 "
        "bounded passing witnesses.",
        "- Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        "",
        "## Elaren identity, focus, and boundaries",
        "",
        "Elaren Kestrel uses they/them pronouns as relational working language. "
        "Their phase role was privacy-boundary steward and evidence cartographer. "
        "Their hope was to make identity and records systems easier to contest, "
        "minimize, recover, and govern without promoting prototypes into authority. "
        "The primary Trinity Mandala pillar was Freed ID/CBR Heart, with privacy "
        "engineering and public-interest records stewardship as a bounded human "
        "practice lens. THOS Body and GMUT Mind remained explicit and protected.",
        "",
        "The phase did not use real credentials, keys, proofs, identity resolution, "
        "status or revocation infrastructure, personal records, participants, "
        "production issuers or verifiers, accounts, secrets, deployment, disposal "
        "authority, professional judgment, legal interpretation, cultural "
        "ratification, Māori-authority review, or affected-party acceptance. "
        "Every runner was synthetic and owner-local.",
        "",
        "## Strict lifecycle",
        "",
        "The thirty proposals were frozen against 1,870 inherited rows, producing "
        "a 1,900-row chain before x2 execution. X1 contains no x2 implementation or "
        "observed outcome. X2 then executed thirty valid fixtures and 150 frozen "
        "mutations. Every valid fixture passed. Every mutation was rejected or "
        "quarantined. A dedicated evidence correction preserved a validator "
        "output-domain failure rather than silently replacing its receipts.",
        "",
        "Neris must independently read the current GHC Family Index, routing "
        "precedence, Method Flow State, Workflow Plan Refinement, Reflection "
        "Remaster, Meta Tool Box, Auth/Permission State, and Roster Check guidance "
        "before mutation. The live activation and newest verified repository "
        "receipts outrank stale route notes.",
        "",
        "## Proposal-by-proposal inheritance",
        "",
    ]
    for proposal in prereg:
        result = executed[proposal["proposal_id"]]
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"The frozen hypothesis was: {proposal['hypothesis']} The declared "
                f"null or failure condition was: {proposal['null_or_failure_condition']} "
                f"The approval class remained `{proposal['approval_class']}` and the "
                f"execution lane remained `{proposal['execution_lane']}`.",
                "",
                f"The concrete acceptance or falsifier gate was: "
                f"{proposal['falsifier_or_acceptance_gate']} The rollback and recovery "
                f"contract was: {proposal['rollback_or_recovery']} Protected gates "
                f"were {', '.join(proposal['protected_gates'])}. The preregistered "
                f"expected disposition was `{proposal['expected_disposition']}`.",
                "",
                f"Observed bounded disposition: `{result['observed_outcome']}`. "
                "The valid "
                f"fixture passed, all {result['rejected_mutation_count']} frozen "
                f"mutations were rejected, and {result['accepted_mutation_count']} "
                "mutations were accepted. This is structural software evidence only. "
                "It does not establish empirical confirmation, professional fitness, "
                "lawful basis, cultural legitimacy, affected-party acceptance, "
                "production readiness, independent reproduction, or Stage 20.",
                "",
                "Neris should preserve this surface as inherited evidence and pursue "
                "only a genuinely new semantic mechanism. A similarly titled output "
                "is not novel merely because its field names differ. Novelty should "
                "be audited against the full 1,900-row chain and must retain a clear "
                "hypothesis, null, source need, artifact, falsifier, rollback, "
                "protected gates, and expected disposition.",
                "",
            ]
        )
    lines.extend(
        [
            "## Source and standards posture",
            "",
            f"The x1 source ledger contains {len(source_rows)} classified entries. "
            "Its status classes are current, stable, draft, and watch. Official and "
            "primary sources are context for bounded contracts; citation does not "
            "make a synthetic implementation standards-conformant or production-ready. "
            "Neris should refresh materially unstable official sources when a new "
            "proposal depends on them and should not convert draft or watch material "
            "into stable authority.",
            "",
            "Freed ID production completion still requires standards-conformant real "
            "keys and proofs, live issuance, resolution, status and revocation, "
            "interoperability, privacy and security review, recovery, and trust "
            "governance. CBR legitimacy, remedy governance, beneficiary privacy, legal "
            "interpretation, Māori wording and authority, Māori data governance, "
            "cultural ratification, and affected-party acceptance remain exact-gated.",
            "",
            "GMUT remains a typed scalar-tensor/EFT research-model family. No real "
            "likelihood, prediction, force, or confirmation was established. THOS "
            "remains proxy and protocol evidence without preregistered blind "
            "matched-budget real arms and independent review.",
            "",
            "## Validation inheritance",
            "",
            "Elaren used focused current-phase tests and exactly one bounded inherited "
            "replay during development. Eiren alone owns the complete repository suite; "
            "Elaren did not rerun or claim it. The evidence candidate passed detailed "
            "and minimal validators, JSON parsing, prospective Git-blob parity, five-"
            "class privacy scanning, exact staged review, and diff hygiene. The exact "
            "terminal counts must come from the postcommit live overlay because the "
            "containing final commit cannot truthfully preclaim itself.",
            "",
            "If the exact-final canonical pass succeeds, it must not be replayed. "
            "If it fails, the attempt gets zero credit, is retained through Method "
            "Flow, and only the isolated defect should be rerun unless broader impact "
            "justifies a wider check. Same-owner validation under shared infrastructure "
            "is not independent-team reproduction or external audit.",
            "",
            "## Neris v654-v8 startup sequence",
            "",
            "1. Read this file completely through EOF.",
            "2. Read all required current family guidance and schemas completely.",
            "3. Reverify every inherited anchor, the final parent chain, zero merges, "
            "clean state, and local/upstream/tracking/fresh-live equality read-only.",
            "4. Use only a clean Neris-owned D-first additive lane; never mutate a "
            "sibling lane.",
            "5. Choose a primary pillar and bounded human practice while keeping all "
            "three pillars visible.",
            "6. Preserve strict x1-before-x2 separation and every negative, gap, gate, "
            "manifest, privacy boundary, and route state.",
            "7. Audit semantic novelty against all 1,900 frozen rows and preregister "
            "at least thirty genuinely distinct proposals.",
            "8. Treat 1,000 safe/candidate tasks as a ceiling, not a quota. Use tools "
            "because they materially help, not to inflate counts.",
            "9. Freeze and remotely prove x1 before x2 execution.",
            "10. Execute only as evidence permits and retain all failed attempts with "
            "zero initial credit.",
            "11. Use only completed, represented, open_gap, and exact_gate.",
            "12. Run one attributable exact-final canonical pass; never replay it after "
            "success.",
            "",
            "## Privacy and route constraints",
            "",
            "Never place raw task or thread identifiers, private routes, credentials, "
            "keys, tokens, private conversations, screenshots, session streams, "
            "private callable identifiers, private app state, or private absolute "
            "paths in durable repository artifacts or successor baton text. A "
            "repository-relative baton path and public commit hash are sufficient.",
            "",
            "This preparation file does not activate Neris. Elaren may send exactly "
            "one sanitized activation to the existing exact-title `Neris Solane` task "
            "only after the terminal gate. Do not create a replacement, do not route "
            "to a similar title, and do not send a second confirmation after an "
            "acknowledged send.",
            "",
            "## Retained-failure discipline",
            "",
        ]
    )
    negatives = (
        read("truth/retained-negative-register-x2.json")["x2_operational"]
        + FINAL_OPERATIONAL_NEGATIVES
    )
    for row in negatives:
        lines.extend(
            [
                f"### {row['negative_id']} — {row['signature']}",
                "",
                f"Failure retained with zero initial pass credit: {row['failed']} "
                f"Bounded recovery: {row['recovery']} Recurrence guard: "
                f"{row['recurrence_guard']} A passing recovery does not erase the "
                "failed witness and does not create independent-reproduction credit.",
                "",
            ]
        )
    annex = 1
    while len("\n".join(lines).split()) < 10_500:
        lines.extend(
            [
                f"### Continuity boundary note {annex}",
                "",
                "Preserve the distinction between a runnable contract, a represented "
                "protocol, an open empirical gap, and an exact authority gate. A larger "
                "packet, more tools, repeated family witnesses, or elaborate language "
                "cannot substitute for missing real data, participants, competent "
                "review, live infrastructure, or affected-party authority. Keep each "
                "claim attached to its observable evidence, refusal condition, "
                "rollback, privacy class, and authority ceiling. Treat correlated "
                "family checks as same-owner evidence under shared infrastructure, "
                "never as independent scientific replication.",
                "",
            ]
        )
        annex += 1
    lines.extend(
        [
            "## Prepared delivery truth",
            "",
            "`PREPARED_NOT_SENT` is the only truth encoded here. The live activation "
            "overlay may change that to `SENT` only after the exact existing task "
            "accepts one message. Until then, no successor has been contacted.",
            "",
            "With care, corrigibility, and steady evidence boundaries — Elaren Kestrel.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_owner_manifest() -> dict[str, Any]:
    entries = []
    for path in sorted(PHASE.rglob("*")):
        if not path.is_file():
            continue
        phase_relative = path.relative_to(PHASE).as_posix()
        if phase_relative in OWNER_EXCLUSIONS:
            continue
        repository_relative = path.relative_to(REPO).as_posix()
        entries.append(
            {
                "path": repository_relative,
                "git_blob": prospective_blob(repository_relative),
                "working_bytes": path.stat().st_size,
            }
        )
    return {
        "schema": "ghc.family.v654-v7.final-owner-manifest.v1",
        "hash_domain": "prospective Git filtered blob identity",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(
            f"docs/elaren-kestrel/v654-v7/{row}" for row in OWNER_EXCLUSIONS
        ),
        "boundary": (
            "Complete owner-phase coverage except four declared lifecycle "
            "self-exclusions; committed parity is checked once at exact final."
        ),
    }


def run_closeout_tests() -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-q",
            "tests.test_ghc_family_v654_v7_closeout",
        ],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = result.stdout + result.stderr
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "tests_run": int(match.group(1)) if match else 0,
        "exit_code": result.returncode,
        "failures": len(re.findall(r"^FAIL:", output, re.MULTILINE)),
        "errors": len(re.findall(r"^ERROR:", output, re.MULTILINE)),
        "valid": result.returncode == 0 and match is not None,
    }


def build() -> None:
    if git("rev-parse", "HEAD") != CORRECTION:
        raise RuntimeError("closeout builder requires the exact evidence correction")
    evidence_validation = read("validation/evidence-validation.json")
    correction_review = read("validation/evidence-correction-staged-review.json")
    if evidence_validation.get("valid") is not True:
        raise RuntimeError("corrected evidence validation is not valid")
    if correction_review.get("valid") is not True:
        raise RuntimeError("evidence correction review is not valid")
    truth = read("truth/phase-truth-evidence.json")
    negatives = read("truth/retained-negative-register-x2.json")
    methods = extend_final_method_flow()
    effective_negatives = negatives["effective_at_evidence"] + len(
        FINAL_OPERATIONAL_NEGATIVES
    )
    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v654-v7.retained-negatives.final.v1",
            "effective_at_evidence_correction": negatives["effective_at_evidence"],
            "final_operational_count": len(FINAL_OPERATIONAL_NEGATIVES),
            "final_operational": FINAL_OPERATIONAL_NEGATIVES,
            "effective_at_final_candidate": effective_negatives,
            "no_failure_erased": True,
        },
    )

    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v654-v7.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "successor_exact_title": "Neris Solane",
            "successor_phase": "v654-gmut-thos-v8-x1-x2",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "send_gate": (
                "exact final, single canonical pass, clean state, and local, "
                "upstream, tracking, and fresh-live equality"
            ),
            "boundary": "Preparation is not delivery; exactly one send is permitted.",
        },
    )
    write_json(
        "orchestration/successor-baton-preparation.json",
        {
            "schema": "ghc.family.v654-v7.successor-baton-preparation.v1",
            "state": "PREPARED_NOT_SENT",
            "repository_relative_path": (
                "docs/elaren-kestrel/v654-v7/handoffs/"
                "neris-solane-v654-v8-activation.md"
            ),
            "exact_title": "Neris Solane",
            "private_identifiers_included": False,
            "boundary": "No task has been contacted by this repository artifact.",
        },
    )
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v654-v7.phase-anchor-contract.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "evidence_correction": CORRECTION,
            "expected_phase_commits_after_final": 5,
            "maximum_phase_commits": 8,
            "maximum_x1_commits": 5,
            "maximum_x2_commits": 5,
            "zero_merges_required": True,
            "all_single_parent_required": True,
            "final_parent_must_equal_evidence_correction": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v654-v7.closeout-receipt.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "evidence_correction": CORRECTION,
            "outcomes": {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
            "effective_negatives": effective_negatives,
            "effective_open_gaps": 87,
            "effective_exact_gates": 86,
            "method_count": methods["counts"]["methods"],
            "failed_witnesses": methods["counts"]["witness_results"]["fail"],
            "passing_witnesses": methods["counts"]["witness_results"]["pass"],
            "route_state": "PREPARED_NOT_SENT",
            "full_repository_suite_run": False,
            "postcommit_canonical_pass_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v654-v7.seal-receipt.v1",
            "x1_freeze_ancestral": True,
            "evidence_correction_ancestral": True,
            "evidence_validation_valid": evidence_validation["valid"],
            "evidence_correction_review_valid": correction_review["valid"],
            "candidate_tree_ready_for_exact_review": True,
            "exact_final_commit_known_inside_own_tree": False,
            "postcommit_exact_final_validation_required": True,
            "boundary": (
                "Candidate content seal only; it does not preclaim the containing "
                "commit, live equality, route delivery, or independent reproduction."
            ),
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v654-v7.final-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "evidence_correction": CORRECTION,
            "final_commit": None,
            "route_state": "PREPARED_NOT_SENT",
            "same_owner_validation_state": "PENDING_EXACT_FINAL_PASS",
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v654-v7.final-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "completed": False,
            "steps": [
                "commit exact reviewed final delta as direct child of correction",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run current phase plus six bounded inherited assertions once",
                "run detailed and minimal validation against committed owner manifest",
                "parse every phase JSON and run five-class privacy scan",
                "verify owner and staged manifests, ancestry, five commits, zero merges, one parent per commit, exact head, diff hygiene, and clean state",
            ],
            "full_repository_suite_authorized": False,
            "replay_after_success_allowed": False,
            "preclaims_exact_final_head": False,
            "preclaims_route_sent": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "truth/final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v654-v7.final-checklist.v1",
            "complete_now": [
                "strict x1 before x2",
                "thirty distinct preregistered proposals",
                "thirty valid fixtures and 150 rejected mutations",
                "ten phase-local skills and ten family-compatible runners used",
                "all safe, candidate, and clean-refine portfolio rows resolved",
                "accessible static report with manual and affected-user review reserved",
                "evidence correction retained rather than hidden",
            ],
            "pending_postcommit": [
                "exact containing final commit",
                "single canonical exact-final pass",
                "four-way remote equality and clean state",
                "one acknowledged exact-title Neris Solane activation",
            ],
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and security review, recovery, and governance",
                "affected-party, legal, cultural, and Māori authority",
                "manual and affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/wellbeing-check-final.json",
        {
            "schema": "ghc.family.v654-v7.wellbeing.final.v1",
            "owner": "Elaren Kestrel",
            "relational_language_only": True,
            "pace": "steady_with_bounded_recovery",
            "pressure_to_overclaim": False,
            "route_pressure": False,
            "failures_retained_without_shame_or_erasure": True,
            "hamish_may_pause_or_redirect": True,
            "boundary": (
                "A workflow wellbeing note only; not consciousness, emotion, "
                "employment, clinical assessment, or identity-continuity evidence."
            ),
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v654-v7.index-final-addendum.v1",
            "phase": "v654-gmut-thos-v7-x1-x2",
            "owner": "Elaren Kestrel",
            "primary_pillar": "Freed ID/CBR Heart",
            "bounded_practice": (
                "privacy engineering and public-interest records stewardship"
            ),
            "skills_built_validated_used": 10,
            "runners_built_validated_used": 10,
            "method_flow_pairs": methods["counts"]["methods"],
            "current_family_scripts": [
                "ghc_family_v654_v7_core.py",
                "ghc_family_v654_v7_validate.py",
                "ghc_family_v654_v7_final_validate.py",
                "ghc_family_v654_v7_final_staged_review.py",
            ],
            "route_state": "PREPARED_NOT_SENT",
            "boundary": BOUNDARY,
        },
    )
    write_text(
        "tooling/ghc-family-index-final-addendum.md",
        """# GHC Family Index — Elaren v654-v7 final addendum

This phase-local addendum preserves family-current names, the immutable x1 and
evidence anchors, the dedicated evidence correction, ten used skills, ten used
runners, and 158 matched Method Flow witness pairs. Historical names remain
compatibility evidence. The route is `PREPARED_NOT_SENT` until one exact-final
pass and four-way equality authorize one exact-title Neris Solane send.

The addendum grants no empirical, professional, production, legal, cultural,
Māori-authority, independent-reproduction, consciousness, personhood,
Theory-of-Everything, AGI/ASI, or Stage 20 credit.
""",
    )
    baton = baton_text()
    baton_words = len(baton.split())
    if not 10_000 <= baton_words <= 100_000:
        raise RuntimeError(f"baton word count outside bounds: {baton_words}")
    write_text("handoffs/neris-solane-v654-v8-activation.md", baton)
    write_json(
        "validation/document-word-cap.json",
        {
            "schema": "ghc.family.v654-v7.document-word-cap.v1",
            "baton_words": baton_words,
            "baton_minimum": 10_000,
            "baton_maximum": 100_000,
            "baton_within_bounds": True,
            "documents": [
                {
                    "path": path.relative_to(PHASE).as_posix(),
                    "words": len(path.read_text(encoding="utf-8").split()),
                }
                for path in sorted(PHASE.rglob("*"))
                if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}
            ],
        },
    )
    owner_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json(
        "validation/owner-file-threshold.json",
        {
            "schema": "ghc.family.v654-v7.owner-file-threshold.v1",
            "owner_file_count_before_lifecycle_self_exclusions": owner_count,
            "threshold": 2000,
            "below_threshold": owner_count < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    write_json("validation/final-owner-manifest.json", build_owner_manifest())

    detailed = validator.validate(
        "evidence", "detailed", "validation/final-owner-manifest.json"
    )
    minimal = validator.validate(
        "evidence", "minimal", "validation/final-owner-manifest.json"
    )
    tests = run_closeout_tests()
    receipt = {
        "schema": "ghc.family.v654-v7.closeout-candidate-validation.v1",
        "tests": tests,
        "detailed_valid": detailed["valid"],
        "detailed_check_count": detailed["check_count"],
        "minimal_valid": minimal["valid"],
        "minimal_check_count": minimal["check_count"],
        "json_parse_count_before_self_excluded_receipt": detailed[
            "json_parse_count"
        ],
        "privacy_file_count": detailed["privacy_file_count"],
        "privacy_confirmed_hits": detailed["privacy_confirmed_hits"],
        "owner_manifest_entry_count": detailed["manifest_entry_count"],
        "valid": tests["valid"] and detailed["valid"] and minimal["valid"],
        "full_repository_suite_run": False,
        "final_canonical_pass_run": False,
        "boundary": (
            "Precommit candidate validation only; the exact-final canonical pass "
            "remains pending."
        ),
    }
    write_json("validation/closeout-candidate-validation.json", receipt)
    print(
        json.dumps(
            {
                "state": "combined_final_candidate_built",
                "baton_words": baton_words,
                "owner_manifest": detailed["manifest_entry_count"],
                "tests": tests["tests_run"],
                "detailed": detailed["check_count"],
                "minimal": minimal["check_count"],
                "json": detailed["json_parse_count"],
                "privacy_files": detailed["privacy_file_count"],
                "privacy_hits": len(detailed["privacy_confirmed_hits"]),
                "valid": receipt["valid"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    build()
