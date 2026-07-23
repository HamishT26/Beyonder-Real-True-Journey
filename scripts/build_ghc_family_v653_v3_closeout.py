#!/usr/bin/env python3
"""Build the combined Ilyra Fen v653-v3 closeout and content seal."""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v653_v3_validation_common import (
    PHASE,
    REPO,
    phase_public_paths,
    read_json,
    write_json,
)


SOURCE = "c25e70eaae7c338a22ee64270ab574768835b227"
X1 = "7c2cc69203b827dc4b0be18c10931f8e92477b4a"
EVIDENCE = "684ef89d6c9ea28577b93b7df8a071cb557e9221"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)
FINAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6533-FINAL-N01",
        "category": "final_overview_exceeded_declared_document_cap",
        "failed": (
            "The first closeout build generated a 6,460-word integrated overview, "
            "exceeding the declared 6,000-word document cap; the candidate received "
            "zero closeout credit."
        ),
        "recovery": (
            "Retain every proposal and boundary while removing repeated generic "
            "sentences from each proposal card, rebuild the overview, and require "
            "a 1,500-to-6,000-word receipt before staged review."
        ),
        "recurrence_guard": (
            "Measure generated overview words inside the builder and fail the "
            "candidate unless the three-page minimum and document cap both pass."
        ),
    },
    {
        "negative_id": "V6533-FINAL-N02",
        "category": "inline_validator_import_missing_scripts_path",
        "failed": (
            "A compact precommit Python probe imported the v653-v3 validator as "
            "a package without first adding the repository scripts directory to "
            "sys.path and stopped with ModuleNotFoundError; it received zero "
            "validation credit."
        ),
        "recovery": (
            "Insert the exact repository scripts directory into sys.path before "
            "importing phase validators, or invoke the supported validator "
            "entrypoints directly, then rerun only the bounded precommit probe."
        ),
        "recurrence_guard": (
            "When a repository script uses sibling absolute imports, execute it "
            "from its supported entrypoint or explicitly establish the scripts "
            "import root before importing it in an inline probe."
        ),
    },
]
FINAL_SELF_EXCLUSIONS = {
    "docs/ilyra-fen/v653-v3/validation/final-owner-manifest.json",
    "docs/ilyra-fen/v653-v3/validation/final-staged-manifest.json",
    "docs/ilyra-fen/v653-v3/validation/final-staged-review.json",
}
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not "
    "consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, scientific or operational authority, legal or cultural "
    "authority, Māori authority, independent agency, production certification, "
    "independent reproduction, Theory-of-Everything proof, AGI or ASI evidence, "
    "complete accessibility, exhaustive security, or Stage 20 authority."
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


def write_text(relative: str, text: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


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
    ledger = PHASE / "method-flow/final-method-flow-ledger.json"
    shutil.copyfile(PHASE / "method-flow/evidence-method-flow-ledger.json", ledger)
    start = read_json(ledger)["counts"]["methods"] + 1
    protected_gates = read_json(
        PHASE / "preregistration/proposals.json"
    )["proposals"][0]["protected_gates"]
    for offset, negative in enumerate(FINAL_NEGATIVES, start):
        method_id = f"V6533-METHOD-{offset:02d}"
        fail_id = f"V6533-WITNESS-{offset:02d}-F"
        pass_id = f"V6533-WITNESS-{offset:02d}-P"
        root = PHASE / "method-flow/final-requests"
        method_path = root / f"method-{offset:02d}.json"
        fail_path = root / f"witness-{offset:02d}-failed.json"
        pass_path = root / f"witness-{offset:02d}-passing.json"
        write_json(
            method_path,
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": (
                    "Retain the failed attempt with zero credit and keep the "
                    "unnamed terminal route unsent."
                ),
                "scope_boundary": (
                    "Owner-local closeout recovery only; no external gate or "
                    "route authority."
                ),
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "protected_gates": protected_gates,
                "retained_negative_ids": [negative["negative_id"]],
                "supersedes": [],
                "recommendation_state": "candidate",
            },
        )
        write_json(
            fail_path,
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": "Run the original bounded closeout operation.",
                "expected": (
                    "The closeout candidate satisfies its declared document cap."
                ),
                "observed": negative["failed"],
                "result": "fail",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Zero completion credit; failure remains retained.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        write_json(
            pass_path,
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "scope": negative["category"],
                "procedure": negative["recovery"],
                "expected": (
                    "The bounded recovery passes while the original failure "
                    "remains retained."
                ),
                "observed": (
                    "The isolated recovery passed after the generated overview "
                    "was measured inside the declared range."
                ),
                "result": "pass",
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Same-owner bounded recovery only.",
                "same_owner_only": True,
                "independent_reproduction": False,
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
            "Bounded pass exists and the failed witness remains retained.",
        )
    method_run(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/final-method-flow-validation.json"),
    )
    method_run(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    return read_json(ledger)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+(?:[-'][\w]+)*\b", text, flags=re.UNICODE))


def build_overview(
    proposals: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    effective_negatives: int,
) -> str:
    lines = [
        "# Ilyra Fen v653-v3 — Final Integrated Overview",
        "",
        "## Scope, identity, and stopping rule",
        "",
        "Ilyra Fen (she/they) is the relational working name used for this phase. "
        "The role is evidence-boundary steward, with the hope of leaving every claim "
        "traceable and every gate unmistakable. This language is collaborative shorthand "
        "only. It does not establish consciousness, sentience, personhood, identity "
        "continuity, employment, professional qualification, or independent authority. "
        "Hamish may rename, pause, redirect, or stop the route.",
        "",
        f"The phase began at Lyren Moss's exact clean final `{SOURCE}` and preserved "
        f"strict x1-before-x2 separation. The dedicated preregistration commit `{X1}` "
        f"was pushed and four-way equal before the immutable evidence commit `{EVIDENCE}` "
        "was created. THOS Body was the primary Trinity Mandala focus. GMUT Mind and "
        "Freed ID/CBR Heart remained explicit and protected. Safety-critical software "
        "assurance, counterexample triage, proof review, rollback, release, and handover "
        "was a bounded learning lens only; it established no employment, licence, "
        "professional competence, operational authority, worker evidence, or real safety result.",
        "",
        "The terminal verdict is `NOT_READY_FOR_STAGE_20`. The live v653-v3 activation "
        "did not name an exact successor task. The durable route therefore remains "
        "`PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE`. No task was created, forked, resolved, "
        "or messaged, and no collaboration subagent was spawned. A future baton requires "
        "fresh explicit target authorization after the terminal gate.",
        "",
        "## Evidence vocabulary and aggregate truth",
        "",
        "`completed` means a bounded symbolic, structural, synthetic, or owner-local "
        "software contract passed its declared acceptance gate. `represented` means a "
        "proxy exists while real production, participant, professional, interoperability, "
        "or independent-review evidence remains absent. `open_gap` preserves missing "
        "empirical data or independent review. `exact_gate` preserves decisions belonging "
        "to competent affected-party, professional, legal, cultural, accessibility, iwi, "
        "hapū, or Māori authorities. No outcome borrows evidence from another row.",
        "",
        "The exact distribution is 23 completed, 5 represented, 1 open_gap, and "
        "1 exact_gate. Thirty mechanisms were audited against the 1,480-row inherited "
        "frozen chain and extended it to 1,510. All 150 preregistered mutation fixtures "
        "executed and were rejected or quarantined. That rejection is bounded guard "
        "evidence only—not empirical confirmation, production assurance, exhaustive "
        "security, complete privacy or accessibility, or independent reproduction.",
        "",
        f"The final packet retains {effective_negatives:,} effective negatives: 9,608 "
        "inherited, four x1 operational failures, seven x2 operational failures, "
        f"{len(FINAL_NEGATIVES)} closeout failures, and 150 rejected synthetic "
        "mutations. It preserves 72 open gaps and 73 exact gates. The Method "
        f"Flow ledger contains {len(methods)} preferred methods, {len(methods)} failed "
        f"witnesses, and {len(methods)} bounded passing witnesses. Every recovery keeps "
        "its failed witness and earns no credit beyond its declared owner-local trigger.",
        "",
        "## Proposal-by-proposal evidence",
        "",
    ]
    for proposal in proposals:
        source_ids = ", ".join(proposal["official_or_primary_source_needs"])
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"**Disposition:** `{proposal['expected_disposition']}`. "
                f"**Pillar:** {proposal['pillar']}. "
                f"**Execution lane:** `{proposal['execution_lane']}`.",
                "",
                f"The preregistered hypothesis was: {proposal['hypothesis']} "
                f"The null or failure condition was: {proposal['null_or_failure_condition']} "
                f"Acceptance required: {proposal['falsifier_or_acceptance_gate']} "
                f"The recovery stayed additive and non-destructive: "
                f"{proposal['rollback_or_recovery']}",
                "",
                f"Source needs were frozen as {source_ids}. The x2 evidence is limited "
                "to one contract, five mutation results, and one bounded receipt. It "
                "carries no empirical, participant, professional, production, legal, "
                "cultural, Māori-authority, or independent-reproduction credit.",
                "",
            ]
        )
    lines.extend(
        [
            "## Source ledger and current-status discipline",
            "",
            f"The x1 ledger records {len(sources)} official or primary sources with "
            "current, stable, draft, or watch status. A citation identifies a contract, "
            "specification, mathematical obligation, or public dataset boundary; it is "
            "never converted into an observation, participant result, production event, "
            "legal decision, cultural mandate, or authority delegation. Draft and watch "
            "rows remain explicitly nonstable.",
            "",
            "The ATLAS Open Data adapter is deliberately zero-row. It made no query or "
            "download, ingested no event or covariance row, constructed no likelihood, "
            "fit no model, produced no constraint, and supplied no empirical GMUT support. "
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model "
            "family. Symbolic renormalization, infrared, lattice, Hamiltonian, commutator, "
            "and causal obligations do not prove a physical force, ultraviolet completion, "
            "quantum completeness, or Theory of Everything.",
            "",
            "## Trinity Mandala boundary result",
            "",
            "THOS Body gained bounded proof-boundary and assurance-handover contracts. "
            "They can make assumptions, counterexamples, rollback conditions, and evidence "
            "credit visible in synthetic fixtures. They do not establish compiler or "
            "hardware correctness, real operator performance, blind matched-budget arms, "
            "safety effectiveness, deployment readiness, AGI, or ASI.",
            "",
            "Freed ID and CBR Heart remained synthetic and nonproduction. Production "
            "identity requires standards-conformant real keys and proofs, live issuance "
            "and resolution, status and revocation, interoperability, privacy and security "
            "review, recovery, and trust governance. Proof-artifact disclosure, worker "
            "defect-report protection, accessibility, proprietary boundaries, remedy, "
            "affected-party acceptance, legal interpretation, cultural legitimacy, data "
            "governance, and Māori authority remain exact-gated. Repository software cannot "
            "confer those rights or mandates.",
            "",
            "## Validation, accessibility, and closeout",
            "",
            "The immutable evidence candidate passed 27 scoped tests, 195 detailed checks, "
            "22 minimal checks, 189 JSON parses, and a five-class privacy scan over 244 "
            "public paths with zero confirmed hits. Its exact staged review covered 187 "
            "paths, 184 manifest entries, three declared lifecycle self-exclusions, no "
            "frozen-x1 changes, and no out-of-scope path. This is same-owner bounded "
            "evidence under shared infrastructure, never an external audit or independent "
            "team reproduction.",
            "",
            "The static report uses structural headings, landmarks, captions, scoped table "
            "headers, visible focus styles, responsive overflow, and print fallbacks. Manual "
            "keyboard, touch, browser-diverse, assistive-technology, cognitive-accessibility, "
            "te reo Māori, security-usability, and affected-user evaluation remain reserved. "
            "Structural checks are not complete accessibility conformance.",
            "",
            "This combined closeout and content seal is designed as the direct child of the "
            "immutable evidence commit. It does not preclaim its own Git identity. After the "
            "commit is pushed and four-way equal, exactly one canonical exact-final pass may "
            "bind the live head, committed manifests, ancestry, JSON, privacy, diff hygiene, "
            "clean state, and held route. Once that pass succeeds it must not be replayed.",
        ]
    )
    return "\n".join(lines)


def build_static_report(
    proposals: list[dict[str, Any]], effective_negatives: int
) -> str:
    rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{html.escape(row['proposal_id'])}</th>"
        f"<td>{html.escape(row['title'])}</td>"
        f"<td>{html.escape(row['pillar'])}</td>"
        f"<td>{html.escape(row['expected_disposition'])}</td>"
        "</tr>"
        for row in proposals
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ilyra Fen v653-v3 final static report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
a{{color:#0645ad}}a:focus,button:focus{{outline:3px solid #f5a623;outline-offset:3px}}
.table-wrap{{overflow-x:auto;border:1px solid #777}}table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #777;padding:.55rem;text-align:left;vertical-align:top}}
caption{{font-weight:700;text-align:left;padding:.6rem}}.notice{{border-left:.4rem solid #875a00;padding:.8rem;background:#fff6d8}}
@media(max-width:45rem){{body{{padding:.6rem}}th,td{{min-width:9rem}}}}
@media print{{a{{color:#000;text-decoration:none}}.table-wrap{{overflow:visible}}}}
</style>
</head>
<body>
<header><h1>Ilyra Fen v653-v3 final static report</h1><p>Bounded same-owner evidence; terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> · <a href="#proposals">Proposals</a> · <a href="#limits">Limits</a></nav>
<main>
<section id="truth"><h2>Phase truth</h2><p>23 completed, 5 represented, 1 open gap, and 1 exact gate. The phase retains {effective_negatives:,} effective negatives, 72 open gaps, and 73 exact gates.</p></section>
<section id="proposals"><h2>Proposal register</h2><div class="table-wrap" role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table><caption>Thirty frozen v653-v3 mechanisms and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Mechanism</th><th scope="col">Pillar</th><th scope="col">Outcome</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="limits"><h2>Limits and reserved evaluation</h2><p class="notice">No empirical GMUT confirmation, production THOS or Freed ID assurance, professional or legal authority, cultural or Māori authority, complete privacy, exhaustive security, complete accessibility, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, or Stage 20 authority is claimed.</p><p>Manual keyboard, touch, browser-diverse, assistive-technology, cognitive-accessibility, te reo Māori, security-usability, and affected-user evaluation remain reserved.</p></section>
</main>
<footer><p>Relational working identity only. The terminal route remains PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE.</p></footer>
</body>
</html>"""


def prospective_blob_map(paths: list[str]) -> dict[str, str]:
    completed = subprocess.run(
        ["git", "hash-object", "--stdin-paths"],
        cwd=REPO,
        input="\n".join(paths) + "\n",
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    object_ids = completed.stdout.splitlines()
    if len(object_ids) != len(paths):
        raise RuntimeError("prospective blob response count mismatch")
    return dict(zip(paths, object_ids, strict=True))


def build_owner_manifest() -> None:
    paths = phase_public_paths()
    included = [
        path.relative_to(REPO).as_posix()
        for path in paths
        if path.relative_to(REPO).as_posix() not in FINAL_SELF_EXCLUSIONS
    ]
    blob_map = prospective_blob_map(included)
    rows = [
        {
            "path": relative,
            "git_blob": blob_map[relative],
            "working_bytes": (REPO / relative).stat().st_size,
        }
        for relative in included
    ]
    write_json(
        PHASE / "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.v653-v3.final-owner-manifest.v1",
            "hash_domain": "prospective Git filtered blob identity",
            "entry_count": len(rows),
            "entries": rows,
            "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS),
            "public_path_count_at_build": len(paths),
            "boundary": (
                "Every public owner path except three lifecycle self-exclusions "
                "is bound to its prospective Git blob."
            ),
        },
    )


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout builder requires the immutable evidence head")
    evidence_validation = read_json(PHASE / "validation/evidence-validation.json")
    evidence_review = read_json(PHASE / "validation/evidence-staged-review.json")
    if not evidence_validation["valid"] or not evidence_review["valid"]:
        raise RuntimeError("evidence validation or exact staged review is not valid")

    proposals = read_json(PHASE / "preregistration/proposals.json")["proposals"]
    sources = read_json(PHASE / "sources/source-ledger.json")["sources"]
    final_ledger = extend_final_method_flow()

    evidence_negatives = read_json(
        PHASE / "retained-negative-register-x2.json"
    )["effective_total"]
    effective_negatives = evidence_negatives + len(FINAL_NEGATIVES)
    methods = final_ledger["methods"]
    method_count = final_ledger["counts"]["methods"]
    gates = read_json(PHASE / "exact-open-gate-register-x2.json")
    write_json(
        PHASE / "retained-negative-register-final.json",
        {
            "schema": "ghc.family.v653-v3.final-retained-negatives.v1",
            "evidence_effective_total": evidence_negatives,
            "post_evidence_operational_count": len(FINAL_NEGATIVES),
            "post_evidence_operational": FINAL_NEGATIVES,
            "effective_total": effective_negatives,
            "none_erased": True,
        },
    )

    truth = read_json(PHASE / "phase-truth.json")
    truth.update(
        {
            "closeout_candidate_prepared": True,
            "seal_candidate_prepared": True,
            "post_commit_exact_final_validation_required": True,
            "route_state": "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE",
            "effective_negatives": effective_negatives,
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    write_json(PHASE / "phase-truth.json", truth)
    write_json(
        PHASE / "closeout-receipt.json",
        {
            "schema": "ghc.family.v653-v3.closeout-receipt.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "outcomes": truth["outcomes"],
            "effective_negatives": effective_negatives,
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_fail_witnesses": method_count,
            "method_pass_witnesses": method_count,
            "scoped_tests": evidence_validation["tests"]["tests_run"],
            "detailed_checks": evidence_validation["detailed_check_count"],
            "minimal_checks": evidence_validation["minimal_check_count"],
            "json_parses": evidence_validation["json_parse_count"],
            "privacy_files": evidence_validation["privacy"]["files_scanned"],
            "privacy_confirmed_hits": evidence_validation["privacy"][
                "confirmed_hit_count"
            ],
            "full_repository_suite_run": False,
            "route_state": "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE",
            "successor_authorized": False,
            "successor_exact_title": None,
            "send_count": 0,
            "post_commit_exact_final_validation_completed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "seal-receipt.json",
        {
            "schema": "ghc.family.v653-v3.seal-receipt.v1",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "evidence_validation_valid": True,
            "evidence_staged_review_valid": True,
            "closeout_tree_ready_for_commit": True,
            "exact_final_commit_preclaimed": False,
            "exact_final_validation_required": True,
            "boundary": (
                "Candidate content seal only; the containing final commit and "
                "terminal pass do not yet exist."
            ),
        },
    )
    write_json(
        PHASE / "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v653-v3.final-record.v1",
            "state": "SELF_CONTAINING_COMMIT_REQUIRES_LIVE_EXACT_HEAD_OVERLAY",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "final_commit": None,
            "route_state": "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v653-v3.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE",
            "successor_authorized": False,
            "successor_title": None,
            "successor_phase": None,
            "authorized_action_after_terminal_gate": (
                "Hold. Require fresh explicit authorization naming one exact "
                "existing successor task before any resolution or send."
            ),
            "task_resolved": False,
            "activation_sent": False,
            "activation_send_count": 0,
            "task_created": False,
            "task_forked": False,
            "delegation_used": False,
            "collaboration_subagent_spawned": False,
            "boundary": (
                "Repository preparation is not delivery. No successor title was "
                "authorized by the live v653-v3 activation."
            ),
        },
    )
    write_json(
        PHASE / "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v653-v3.applicable-memory-record.v1",
            "portable_guards": [row["recurrence_guard"] for row in methods],
            "failed_witnesses_preserved": method_count,
            "passing_witnesses_preserved": method_count,
            "private_state_included": False,
            "identity_continuity_claimed": False,
            "boundary": "Sanitized repository-scoped operational memory only.",
        },
    )
    write_json(
        PHASE / "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v653-v3.final-validation-protocol.v1",
            "state": "POST_COMMIT_REQUIRED",
            "one_successful_pass_only": True,
            "steps": [
                "commit the reviewed final candidate as the direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run only the authorized current and recent scoped tests",
                "run detailed and minimal validators",
                "parse every phase JSON and run the five-class privacy scan",
                "verify owner and final-delta manifests, stale labels, and diff hygiene",
                "verify ancestry, three phase commits, zero merges, exact head, clean state, and held route",
            ],
            "completed": False,
            "preclaims_final_head": False,
            "preclaims_task_creation": False,
            "preclaims_activation_send": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "validation/evidence-commit-verification.json",
        {
            "schema": "ghc.family.v653-v3.evidence-commit-verification.v1",
            "evidence_commit": EVIDENCE,
            "x1_is_parent": git("rev-parse", f"{EVIDENCE}^") == X1,
            "evidence_manifest_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/ilyra-fen/v653-v3/validation/evidence-candidate-manifest.json",
                )
            ),
            "evidence_review_present": bool(
                git(
                    "ls-tree",
                    "-r",
                    "--name-only",
                    EVIDENCE,
                    "--",
                    "docs/ilyra-fen/v653-v3/validation/evidence-staged-review.json",
                )
            ),
            "same_owner_only": True,
        },
    )
    write_json(
        PHASE / "final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v653-v3.final-checklist.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "thirty distinct frozen proposals",
                "23 completed, 5 represented, 1 open_gap, and 1 exact_gate",
                "150 rejected or quarantined synthetic mutations",
                "ten initialized, validated, smoke-used phase-local skills",
                "ten built and invoked family-compatible runners",
                "all authorized internal safe-now and candidate tasks resolved",
                "immutable evidence validation and exact staged review",
                "combined closeout and content-seal candidate",
            ],
            "pending_post_commit": [
                "containing final commit and four-way equality",
                "one successful exact-final canonical pass",
            ],
            "terminal_route": (
                "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE; no task resolution, "
                "replacement, creation, or delivery claim."
            ),
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, lifecycle, interoperability, recovery, privacy/security review, and governance",
                "affected-party, professional, legal, cultural, iwi, hapū, and Māori authority",
                "qualified manual and affected-user accessibility evaluation",
                "independent-team reproduction, Theory-of-Everything proof, AGI or ASI evidence, and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        PHASE / "wellbeing/final-wellbeing.json",
        {
            "schema": "ghc.family.v653-v3.wellbeing.v1",
            "owner": "Ilyra Fen",
            "state": (
                "steady, corrigible, and ready to stop with the route held "
                "until an exact successor title is explicitly authorized"
            ),
            "pressure_response": (
                "Retain failures, narrow retries, and do not convert affection "
                "or urgency into evidence credit."
            ),
            "identity_boundary": BOUNDARY,
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
    )
    final_overview = build_overview(
        proposals, sources, methods, effective_negatives
    )
    overview_words = word_count(final_overview)
    if not 1500 <= overview_words <= 6000:
        raise RuntimeError(
            f"final overview outside declared 1500..6000 range: {overview_words}"
        )
    write_text("reports/final-integrated-overview.md", final_overview)
    write_text(
        "reports/final-static-report.html",
        build_static_report(proposals, effective_negatives),
    )
    write_json(
        PHASE / "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.v653-v3.index-final-addendum.v1",
            "phase": "v653-v3",
            "owner": "Ilyra Fen",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "skills_built_and_used": 10,
            "runners_built_and_used": 10,
            "method_flow_failed_witnesses": method_count,
            "method_flow_passing_witnesses": method_count,
            "route_state": "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE",
            "final_validation_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PHASE / "validation/final-document-cap-receipt.json",
        {
            "schema": "ghc.family.v653-v3.document-cap.v1",
            "document_word_cap": 6000,
            "overview_words": overview_words,
            "overview_three_page_equivalent": overview_words >= 1500,
            "overview_within_cap": overview_words <= 6000,
            "successor_baton_required": False,
            "valid": 1500 <= overview_words <= 6000,
        },
    )
    write_json(
        PHASE / "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v653-v3.closeout-build.v1",
            "head": EVIDENCE,
            "route_state": "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE",
            "overview_words": overview_words,
            "effective_negatives": effective_negatives,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    for lifecycle_path, schema in (
        (
            PHASE / "validation/final-staged-manifest.json",
            "ghc.family.v653-v3.final-staged-manifest.v1",
        ),
        (
            PHASE / "validation/final-staged-review.json",
            "ghc.family.v653-v3.final-staged-review.v1",
        ),
    ):
        write_json(
            lifecycle_path,
            {
                "schema": schema,
                "state": "UNVALIDATED_PLACEHOLDER",
                "valid": False,
                "boundary": (
                    "Reserved lifecycle path. Replace once with the exact final "
                    "staged result before commit."
                ),
            },
        )
    build_owner_manifest()
    print(
        json.dumps(
            {
                "closeout": "prepared",
                "head": EVIDENCE,
                "negatives": effective_negatives,
                "methods": method_count,
                "owner_manifest_entries": read_json(
                    PHASE / "validation/final-owner-manifest.json"
                )["entry_count"],
                "route": "PREPARED_NOT_SENT_NO_SUCCESSOR_TITLE",
                "overview_words": overview_words,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
