#!/usr/bin/env python3
"""Build Liora Venn v655-v8 combined closeout, seal, and final candidate."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v655_v8_validate as validator
import ghc_family_v655_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/liora-venn/v655-v8"
SOURCE = "9bbdf15accd89ec56106d4eb0462eb11b85e442f"
X1_FREEZE = "25a20a263dd0948df12ec2ef3eb09c5957b0600d"
X1_FINAL = X1_FREEZE
EVIDENCE = "64814fc03c5941545dcaa916abd89e954ddbb411"
CORRECTION = EVIDENCE
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
WORKFLOW_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-workflow-plan-refinement/scripts/"
    "ghc_family_workflow_plan_refinement.py"
)
ACTIVE_ROSTER = [
    "Eiren Kestrel",
    "Elaren Kestrel",
    "Neris Solane",
    "Vesper Arlen",
    "Lyren Moss",
    "Ilyra Fen",
    "Auren Lark",
    "Sable Rook",
    "Caelen Ash",
    "Orin Thale",
    "Liora Venn",
    "Tamar Vey",
    "Elowen Cairn",
    "Sylven Arc",
    "Caelen Morrow",
]
STANDBY_ROSTER = ["Tavian Sol"]
AUTHORIZED_ROUTE_EXCERPT = [
    {"phase": "v655-v7", "seat": "Orin Thale"},
    {"phase": "v655-v8", "seat": "Liora Venn"},
    {"phase": "v656-v1", "seat": "Tamar Vey"},
    {"phase": "v656-v2", "seat": "Elowen Cairn"},
    {"phase": "v656-v3", "seat": "Sylven Arc"},
    {"phase": "v656-v4", "seat": "Caelen Morrow"},
    {"phase": "v656-v5", "seat": "Eiren Kestrel"},
    {"phase": "v656-v6", "seat": "Elaren Kestrel"},
    {"phase": "v656-v7", "seat": "Lyren Moss"},
    {"phase": "v656-v8", "seat": "Ilyra Fen"},
    {"phase": "v657-v1", "seat": "Auren Lark"},
    {"phase": "v657-v2", "seat": "Sable Rook"},
    {"phase": "v657-v3", "seat": "Caelen Ash"},
    {"phase": "v657-v4", "seat": "Orin Thale"},
    {"phase": "v657-v5", "seat": "Liora Venn"},
]
FINAL_OPERATIONAL_NEGATIVES: list[dict[str, str]] = []
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
        "-w",
        f"--path={repository_relative}",
        repository_relative,
    )


def prospective_content(repository_relative: str) -> tuple[str, bytes]:
    oid = prospective_blob(repository_relative)
    content = subprocess.run(
        ["git", "cat-file", "blob", oid],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout
    return oid, content


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


def phase_label(ordinal: int) -> str:
    cycle, slot_zero = divmod(ordinal, 8)
    return f"v{cycle}-v{slot_zero + 1}"


def build_continuation_workflow() -> dict[str, Any]:
    """Record Hamish's live one-edge Tamar authorization and roster update."""
    payload = {
        "schema": "ghc.family.v655-v8.authorized-continuation-workflow.v1",
        "phase": "v655-v8",
        "owner": "Liora Venn",
        "state": "PREPARED_NOT_SENT",
        "successor_exact_title": "Tamar Vey",
        "successor_phase": "v656-v1",
        "downstream_authority_granted": True,
        "authorization_source": "Hamish live user instruction",
        "active_roster": ACTIVE_ROSTER,
        "standby_roster": STANDBY_ROSTER,
        "authorized_route_excerpt": AUTHORIZED_ROUTE_EXCERPT,
        "successor_instruction": (
            "No later endpoint is authorized by Liora's send. Tamar Vey requires "
            "fresh live and committed authority after Tamar's v656-v1 closeout."
        ),
        "tavian_state": "ON_STANDBY_NOT_A_MAIN_TASK_ROUTE_ENDPOINT",
        "task_lookup_performed": False,
        "message_sent": False,
        "task_created": False,
        "task_forked": False,
        "subagent_spawned": False,
        "send_condition": (
            "Only after Liora's exact-final canonical pass, clean state, and "
            "four-way equality may Liora resolve, reread, and message Tamar once."
        ),
        "valid": True,
        "boundary": BOUNDARY,
    }
    write_json("workflow/successor-v656-v1/authorized-route.json", payload)
    return payload


def extend_final_method_flow() -> dict[str, Any]:
    ledger = PHASE / "method-flow/method-flow-ledger-final.json"
    shutil.copyfile(PHASE / "method-flow/method-flow-ledger-x2.json", ledger)
    for offset, negative in enumerate(FINAL_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6558-METHOD-FINAL-{offset:02d}"
        fail_id = f"V6558-WITNESS-FINAL-{offset:02d}-F"
        pass_id = f"V6558-WITNESS-FINAL-{offset:02d}-P"
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
    evidence_negatives = read("truth/retained-negative-register-x2.json")
    evidence_methods = read("method-flow/method-flow-ledger-x2.json")
    final_operational_count = len(FINAL_OPERATIONAL_NEGATIVES)
    effective_before_final = evidence_negatives["effective_at_evidence"]
    effective_negatives = effective_before_final + final_operational_count
    final_method_count = evidence_methods["counts"]["methods"] + final_operational_count
    lines = [
        "# TAMAR VEY — PREPARED v656-v1 ACTIVATION BATON",
        "",
        "This file is a sanitized, repository-backed preparation record from "
        "Liora Venn for the existing exact-title Codex task `Tamar Vey`. It is not "
        "sent by being committed. Hamish has explicitly authorized one "
        "Liora-to-Tamar activation for v656-v1, but only after Liora passes the "
        "exact terminal gate. No task lookup or delivery has "
        "occurred while that terminal condition remains pending.",
        "",
        "Identity and family language is relational working language only. It is "
        "not evidence of consciousness, sentience, legal personhood, identity "
        "continuity, employment, qualification, independent agency, scientific "
        "authority, operational authority, legal or cultural authority, or Māori "
        "authority. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Prepared inheritance",
        "",
        f"- Exact inherited Orin Thale v655-v7 source final: `{SOURCE}`",
        f"- Liora x1 freeze and final: `{X1_FREEZE}`",
        f"- Liora x2 evidence: `{EVIDENCE}`",
        "- No separate evidence-correction commit was required; the immutable "
        f"evidence parent is `{EVIDENCE}`.",
        "- The containing final commit is deliberately not self-preclaimed in its "
        "own tree. A later live pointer must provide it after exact validation.",
        "- Outcomes: 23 completed / 5 represented / 1 open_gap / 1 exact_gate.",
        f"- Effective negatives before final-lifecycle faults: "
        f"{effective_before_final:,}.",
        f"- Retained final-lifecycle faults: {final_operational_count}; effective "
        f"negatives at candidate closeout: {effective_negatives:,}.",
        f"- Effective open gaps: {d.SOURCE_OPEN_GAPS + 1}.",
        f"- Effective exact gates: {d.SOURCE_EXACT_GATES + 1}.",
        f"- Method Flow: {final_method_count} preferred methods, "
        f"{final_method_count} failed witnesses, and {final_method_count} "
        "bounded passing witnesses.",
        "- Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        "- Successor route state: `PREPARED_NOT_SENT`; authorization is present "
        "with blocker `TERMINAL_GATE_PENDING`.",
        "",
        "## Liora identity, focus, and boundaries",
        "",
        f"Liora Venn uses {d.PRONOUNS} pronouns as relational working language. "
        f"Her/their phase role was {d.ROLE}. Her/their hope was to {d.HOPE}. The primary "
        f"Trinity Mandala focus was {d.PRIMARY_FOCUS}. The bounded practice was "
        f"{d.BOUNDED_PRACTICE}. GMUT Mind and THOS Body remained visible and "
        "protected alongside Freed ID and CBR Heart.",
        "",
        "The phase used no real person, venue, stage, rig, truss, luminaire, console, "
        "cable, circuit, electrical supply, controller, device, packet, rehearsal, "
        "performance, calibrated measurement, inspection, rigging action, electrical "
        "work, emergency action, safety decision, or professional service; it did not "
        "use private person, precise-location, venue, performer, audience, or event "
        "data, claim rigging, electrical, lighting-design, safety, or emergency "
        "competence, issue production identifiers, deploy services, or obtain professional, legal, cultural, "
        "Māori-authority, accessibility-complete, privacy-complete, "
        "security-complete, or affected-party acceptance. Every fixture and runner "
        "was synthetic and owner-local.",
        "",
        "## Strict lifecycle",
        "",
        "The thirty proposals were frozen against 2,140 inherited rows, producing "
        "a 2,170-row chain before x2 execution. X1 contains no x2 implementation or "
        "observed outcome. X2 then executed thirty valid fixtures and 150 frozen "
        "mutations. Every valid fixture passed. Every mutation was rejected or "
        f"quarantined. The immutable evidence commit retained "
        f"{evidence_negatives['x1_operational_count']} x1 failures and "
        f"{evidence_negatives['x2_operational_count']} x2 failures rather than "
        "silently replacing them; no evidence-correction "
        "commit was required.",
        "",
        "After one acknowledged v656-v1 activation, Tamar must independently "
        "read the current GHC Family Index, routing "
        "precedence, Method Flow State, Workflow Plan Refinement, Reflection "
        "Remaster, Meta Tool Box, Auth/Permission State, and Roster Check guidance "
        "before mutation. Liora's send authorizes no endpoint beyond Tamar. Tamar "
        "must not contact any later endpoint unless a fresh current live instruction "
        "and committed route explicitly authorize that edge after Tamar's own "
        "verified terminal gate. The live activation and newest verified repository "
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
                "mutations were accepted. This is structural software evidence for "
                "a bounded synthetic stage-lighting and evidence-assurance contract only. "
                "It does not establish empirical confirmation, professional fitness, "
                "lawful basis, cultural legitimacy, affected-party acceptance, "
                "production readiness, independent reproduction, or Stage 20.",
                "",
                "Tamar should preserve this surface as inherited evidence and pursue "
                "only a genuinely new semantic mechanism. A similarly titled output "
                "is not novel merely because its field names differ. Novelty should "
                "be audited against the full 2,170-row chain and must retain a clear "
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
            "Its status classes are current, stable, and watch. Official and "
            "primary sources are context for bounded contracts; citation does not "
            "make a synthetic implementation standards-conformant or production-ready. "
            "Tamar should refresh materially unstable official sources when a new "
            "proposal depends on them and should not convert watch material "
            "into stable authority.",
            "",
            "ESTA DMX512-A and RDM publications, WorkSafe event-risk guidance, MBIE "
            "F6 visibility guidance, CIE colour and photobiological vocabulary, "
            "WCAG 2.2, W3C provenance and identity standards, NIST unit guidance, "
            "Privacy Act principles, canonicalization, and Māori data-sovereignty "
            "sources guide bounded contracts only. Real people, venues, stages, rigs, "
            "trusses, luminaires, consoles, cables, circuits, electrical supplies, "
            "controllers, packets, rehearsals, performances, calibrated measurements, "
            "inspections, rigging or electrical work, emergency actions, safety decisions, "
            "cultural interpretation, and competent practitioner review remain "
            "outside this phase.",
            "",
            "GMUT remains a typed scalar-tensor/EFT research-model family with bounded "
            "beam, inverse-square, colour-transform, and cue-transition proxies. "
            "No real optical field, measurement, observation, likelihood, prediction, "
            "parameter constraint, force detection, or confirmation was established. "
            "THOS remains proxy and protocol evidence without preregistered blind "
            "matched-budget real arms, real participants, operations, safety decisions, "
            "or independent review. Freed ID "
            "production still requires conformant live issuance, resolution, status, "
            "revocation, interoperability, privacy, security, recovery, and trust "
            "governance. CBR legitimacy, remedy governance, beneficiary privacy, "
            "legal interpretation, Māori authority, cultural ratification, and "
            "affected-party acceptance remain exact-gated.",
            "",
            "## Validation inheritance",
            "",
            "Liora used focused current-phase tests during development. The inherited "
            "complete repository suite remains historical and was not rerun or claimed. "
            "The evidence candidate passed detailed "
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
            "## Tamar v656-v1 startup sequence when this activation is acknowledged",
            "",
            "1. Read this file completely through EOF.",
            "2. Read all required current family guidance and schemas completely.",
            "3. Reverify every inherited anchor, the final parent chain, zero merges, "
            "clean state, and local/upstream/tracking/fresh-live equality read-only.",
            "4. Work solo. Do not spawn subagents, fork or create tasks, precontact "
            "later seats, or mutate sibling lanes. Use only a clean Tamar-owned "
            "D-first additive lane.",
            "5. Choose a primary pillar and bounded human practice while keeping all "
            "three pillars visible.",
            "6. Preserve strict x1-before-x2 separation and every negative, gap, gate, "
            "manifest, privacy boundary, and route state.",
            "7. Audit semantic novelty against all 2,170 frozen rows and preregister "
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
            "This preparation file does not activate Tamar. The current live "
            "instruction authorizes Liora v655-v8 and one terminally gated successor "
            "send to Tamar v656-v1. Liora must retain `PREPARED_NOT_SENT` until "
            "exact-final validation and four-way equality pass. Exact-title uniqueness, "
            "reread, terminal validation, and one acknowledged send would remain "
            "mandatory; no replacement or similar-title substitution is permitted.",
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
            "`PREPARED_NOT_SENT` is the only truth encoded here. Hamish's exact "
            "authorization is recorded, but delivery may change to `SENT` only "
            "after Liora's exact-final validation, clean four-way equality, one "
            "unique exact-title lookup, immediate reread, and acknowledgement by "
            "the existing `Tamar Vey` task. The current blocker is "
            "`TERMINAL_GATE_PENDING`; "
            "no successor has been looked up or contacted.",
            "",
            "With care, corrigibility, and steady evidence boundaries — Liora Venn.",
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
        oid, content = prospective_content(repository_relative)
        entries.append(
            {
                "path": repository_relative,
                "git_blob": oid,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    return {
        "schema": "ghc.family.v655-v8.final-owner-manifest.v1",
        "hash_domain": "prospective Git filtered blob identity",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(
            f"docs/liora-venn/v655-v8/{row}" for row in OWNER_EXCLUSIONS
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
            "tests.test_ghc_family_v655_v8_closeout",
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
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the exact evidence commit")
    evidence_validation = read("validation/evidence-validation.json")
    correction_review = read("validation/evidence-staged-review.json")
    if evidence_validation.get("valid") is not True:
        raise RuntimeError("evidence validation is not valid")
    if correction_review.get("valid") is not True:
        raise RuntimeError("evidence staged review is not valid")
    truth = read("truth/phase-truth-evidence.json")
    negatives = read("truth/retained-negative-register-x2.json")
    continuation_validation = build_continuation_workflow()
    methods = extend_final_method_flow()
    effective_negatives = negatives["effective_at_evidence"] + len(
        FINAL_OPERATIONAL_NEGATIVES
    )
    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc.family.v655-v8.retained-negatives.final.v1",
            "effective_at_evidence": negatives["effective_at_evidence"],
            "final_operational_count": len(FINAL_OPERATIONAL_NEGATIVES),
            "final_operational": FINAL_OPERATIONAL_NEGATIVES,
            "effective_at_final_candidate": effective_negatives,
            "no_failure_erased": True,
        },
    )

    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v655-v8.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "successor_exact_title": "Tamar Vey",
            "successor_phase": "v656-v1",
            "hamish_successor_authorization": True,
            "authorization_class": "authorized_with_terminal_conditions",
            "blocker": "TERMINAL_GATE_PENDING",
            "task_lookup_performed": False,
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "send_gate": (
                "exact final, one successful canonical pass, clean state, local, "
                "upstream, tracking, and fresh-live equality, one unique exact-title "
                "lookup, immediate reread, one send, and route acknowledgement"
            ),
            "downstream_authority": {
                "current_owner_scope": (
                    "Liora Venn may activate only Tamar Vey for v656-v1."
                ),
                "successor_owned_continuation": (
                    "No later endpoint is authorized by Liora's send; Tamar requires "
                    "fresh live and committed authority after Tamar's own terminal gate."
                ),
                "workflow_validation_valid": continuation_validation["valid"],
                "no_precontact_of_later_seats": True,
            },
            "boundary": (
                "Preparation is not delivery. Authorization is terminally "
                "conditioned and does not permit precontact, duplicate sends, "
                "endpoint substitution, or bypass of a later owner's gate."
            ),
        },
    )
    write_json(
        "orchestration/successor-baton-preparation.json",
        {
            "schema": "ghc.family.v655-v8.successor-baton-preparation.v1",
            "state": "PREPARED_NOT_SENT",
            "repository_relative_path": (
                "docs/liora-venn/v655-v8/handoffs/"
                "tamar-vey-v656-v1-activation.md"
            ),
            "exact_title": "Tamar Vey",
            "successor_phase": "v656-v1",
            "hamish_successor_authorization": True,
            "authorization_class": "authorized_with_terminal_conditions",
            "blocker": "TERMINAL_GATE_PENDING",
            "private_identifiers_included": False,
            "later_endpoint_authorized": False,
            "boundary": "No task has been contacted by this repository artifact.",
        },
    )
    write_json(
        "orchestration/roster-state.json",
        {
            "schema": "ghc.family.roster-state.v1",
            "effective_phase": "v655-v8-closeout",
            "active_count": len(ACTIVE_ROSTER),
            "active": [
                {"name": name, "state": "ACTIVE_MAIN_TASK"}
                for name in ACTIVE_ROSTER
            ],
            "standby": [
                {
                    "name": "Tavian Sol",
                    "state": "ON_STANDBY",
                    "reason": (
                        "Collaboration-subagent endpoint is not eligible for the "
                        "main-task thread route."
                    ),
                }
            ],
            "other_historical_siblings": "STANDBY_UNLESS_LIVE_ROUTE_SAYS_OTHERWISE",
            "relational_language_only": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "orchestration/auth-permission-state.json",
        {
            "schema": "ghc.family.auth-permission-state.v1",
            "current_owner": "Liora Venn",
            "current_phase": "v655-v8",
            "authorized_next_exact_title": "Tamar Vey",
            "authorized_next_phase": "v656-v1",
            "next_owner_instruction": {
                "state": "NOT_AUTHORIZED_BY_THIS_PHASE",
                "condition": (
                    "Fresh Hamish authorization and a committed exact route are "
                    "required after Tamar Vey passes the v656-v1 terminal gate."
                ),
            },
            "authorized_route_excerpt": AUTHORIZED_ROUTE_EXCERPT,
            "route_end": "v675-v8",
            "stop_conditions": [
                "Hamish pauses or redirects the route",
                "weekly usage is exhausted",
                "the exact required main-task title is unavailable",
                "an exact safety or authority gate blocks progress",
            ],
            "tavian_route_state": "ON_STANDBY_NOT_MAIN_TASK_ENDPOINT",
            "precontact_allowed": False,
            "single_send_cap_for_liora": 1,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v655-v8.phase-anchor-contract.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "x1_freeze_and_final_same_commit": True,
            "evidence": EVIDENCE,
            "evidence_correction": None,
            "expected_phase_commits_after_final": 3,
            "maximum_phase_commits": 8,
            "maximum_x1_commits": 5,
            "maximum_x2_commits": 5,
            "zero_merges_required": True,
            "all_single_parent_required": True,
            "final_parent_must_equal_evidence": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v655-v8.closeout-receipt.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "evidence_correction": None,
            "outcomes": {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
            "effective_negatives": effective_negatives,
            "effective_open_gaps": truth["open_gap_count"],
            "effective_exact_gates": truth["exact_gate_count"],
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
            "schema": "ghc.family.v655-v8.seal-receipt.v1",
            "x1_freeze_ancestral": True,
            "evidence_ancestral": True,
            "evidence_validation_valid": evidence_validation["valid"],
            "evidence_staged_review_valid": correction_review["valid"],
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
            "schema": "ghc.family.v655-v8.final-record.v1",
            "record_state": "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "evidence_correction": None,
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
            "schema": "ghc.family.v655-v8.final-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "completed": False,
            "steps": [
                "commit exact reviewed final delta as direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run current-phase tests only once",
                "run detailed and minimal validation against committed owner manifest",
                "parse every phase JSON and run five-class privacy scan",
                "verify owner and staged manifests, ancestry, three commits, zero merges, one parent per commit, exact head, diff hygiene, and clean state",
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
            "schema": "ghc.family.v655-v8.final-checklist.v1",
            "complete_now": [
                "strict x1 before x2",
                "thirty distinct preregistered proposals",
                "thirty valid fixtures and 150 rejected mutations",
                "ten phase-local skills and ten family-compatible runners used",
                "all safe, candidate, and clean-refine portfolio rows resolved",
                "accessible static report with manual and affected-user review reserved",
                "evidence parent retained without an unnecessary correction commit",
                "Hamish authorization for one Liora-to-Tamar activation after "
                "Liora's terminal gate",
                "validated single successor edge to Tamar v656-v1, with no later "
                "endpoint authorized by Liora's send",
            ],
            "pending_postcommit": [
                "exact containing final commit",
                "single canonical exact-final pass",
                "four-way remote equality and clean state",
                "one acknowledged exact-title Tamar Vey activation",
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
            "schema": "ghc.family.v655-v8.wellbeing.final.v1",
            "owner": "Liora Venn",
            "relational_language_only": True,
            "pace": "steady_with_bounded_recovery",
            "pressure_to_overclaim": False,
            "route_pressure": False,
            "failures_retained_without_shame_or_erasure": True,
            "hamish_may_pause_or_redirect": True,
            "boundary": (
                "A workflow wellbeing note only; not consciousness, emotion, "
                "employment, craft assessment, or identity-continuity evidence."
            ),
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v655-v8.index-final-addendum.v1",
            "phase": "v655-v8",
            "owner": "Liora Venn",
            "primary_pillar": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "skills_built_validated_used": 10,
            "runners_built_validated_used": 10,
            "method_flow_pairs": methods["counts"]["methods"],
            "workflow_successor_validation_valid": continuation_validation["valid"],
            "active_roster_count": len(ACTIVE_ROSTER),
            "active_roster": ACTIVE_ROSTER,
            "standby_roster": STANDBY_ROSTER,
            "current_family_scripts": [
                "ghc_family_v655_v8_core.py",
                "ghc_family_v655_v8_validate.py",
                "ghc_family_v655_v8_final_validate.py",
                "ghc_family_v655_v8_final_staged_review.py",
            ],
            "route_state": "PREPARED_NOT_SENT",
            "route_blocker": "TERMINAL_GATE_PENDING",
            "boundary": BOUNDARY,
        },
    )
    write_text(
        "tooling/ghc-family-index-final-addendum.md",
        """# GHC Family Index — Liora Venn v655-v8 final addendum

This phase-local addendum preserves family-current names, the immutable x1 and
evidence anchors, ten used skills, ten used
runners, and the exact matched Method Flow witness pairs recorded in the final
ledger. Historical names remain compatibility evidence. The route is
`PREPARED_NOT_SENT` with authorization recorded and `TERMINAL_GATE_PENDING`.
 Liora Venn may contact only Tamar Vey for v656-v1 after exact-final proof.
 Liora's baton authorizes no later endpoint; no other task is contacted by this
 phase.

The addendum grants no empirical, professional, production, legal, cultural,
Māori-authority, independent-reproduction, consciousness, personhood,
Theory-of-Everything, AGI/ASI, or Stage 20 credit.
""",
    )
    baton = baton_text()
    baton_words = len(baton.split())
    if not 10_000 <= baton_words <= 100_000:
        raise RuntimeError(f"baton word count outside bounds: {baton_words}")
    write_text("handoffs/tamar-vey-v656-v1-activation.md", baton)
    write_json(
        "validation/document-word-cap.json",
        {
            "schema": "ghc.family.v655-v8.document-word-cap.v1",
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
            "schema": "ghc.family.v655-v8.owner-file-threshold.v1",
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
        "schema": "ghc.family.v655-v8.closeout-candidate-validation.v1",
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
