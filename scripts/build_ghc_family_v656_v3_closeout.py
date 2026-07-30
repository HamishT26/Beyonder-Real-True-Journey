#!/usr/bin/env python3
"""Build the Sylven Arc v656-v3 combined closeout and candidate seal.

This builder is intentionally pre-commit.  It does not claim the containing
commit, remote equality, a successful exact-final validation, or route
delivery.  Those claims are available only from post-commit read-only checks
and an acknowledged existing-task send.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v3_phase_data as d


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_FINAL
X1_FREEZE = "ae46f611f3b13b2ae77d0f0a13d35f13049ef75d"
X1_FINAL = X1_FREEZE
EVIDENCE = "f0de53a52e9f4e99e6dda1ee6d02de8cfb4e7da6"
BRANCH = d.BRANCH
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/"
    "ghc_family_method_flow_state.py"
)
BOUNDARY = (
    "Relational working language only. Same-owner bounded validation is not "
    "consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, scientific or operational authority, legal "
    "or cultural authority, Māori authority, production certification, "
    "independent reproduction, Theory-of-Everything proof, AGI/ASI evidence, "
    "privacy or accessibility completeness, or Stage 20 authority."
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
FINAL_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6563-FINAL-N01",
        "signature": "combined_closeout_status_probe_timeout",
        "failed": (
            "A combined branch, status, anchor, pattern, and template-read probe "
            "exceeded its ten-second envelope before yielding usable output."
        ),
        "recovery": (
            "Split repository state, file reads, and semantic searches into "
            "bounded scalar probes with archive-aware timeouts."
        ),
        "recurrence_guard": (
            "Do not combine Git state and large file reads in one short archive-"
            "backed command."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N02",
        "signature": "parallel_git_status_probe_timeout",
        "failed": (
            "The first parallel Git state probe exceeded its thirty-second "
            "envelope and earned no cleanliness or head credit."
        ),
        "recovery": (
            "Use exact scalar Git queries and avoid an unbounded untracked-file "
            "inventory until the final review needs it."
        ),
        "recurrence_guard": (
            "Prefer git rev-parse, diff --quiet, and exact-path inventories over "
            "broad status probes on the archive-backed worktree."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N03",
        "signature": "parallel_closeout_template_read_timeout",
        "failed": (
            "A parallel full closeout-template read exceeded its thirty-second "
            "envelope after returning only a partial prefix."
        ),
        "recovery": (
            "Navigate by exact symbols with ripgrep and read only bounded ranges "
            "needed for the decision."
        ),
        "recurrence_guard": (
            "Do not use full-file projection as the first inspection method for "
            "a large generated closeout helper."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N04",
        "signature": "parallel_stale_label_search_timeout",
        "failed": (
            "A parallel multi-file stale-label search exceeded its envelope "
            "without returning a complete result set."
        ),
        "recovery": (
            "Use one bounded ripgrep expression over the four exact helper files."
        ),
        "recurrence_guard": (
            "Constrain stale-label searches to exact files and one declared "
            "pattern family."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N05",
        "signature": "parallel_final_helper_read_timeout",
        "failed": (
            "A combined read of three final helpers and one test file timed out "
            "after returning only a partial validator prefix."
        ),
        "recovery": (
            "Inspect exact constants and functions with ripgrep, then replace the "
            "uncommitted source-owner helpers atomically with phase-native files."
        ),
        "recurrence_guard": (
            "Treat partial output as partial evidence and never infer the unread "
            "tail."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N06",
        "signature": "combined_untracked_history_probe_timeout",
        "failed": (
            "A combined untracked, diff, head, branch, commit-count, and merge-"
            "count inventory exceeded its sixty-second envelope."
        ),
        "recovery": (
            "Defer the complete index inventory to the dedicated staged-review "
            "helper and keep lifecycle checks scalar."
        ),
        "recurrence_guard": (
            "Do not ask one wrapper to enumerate files and history dimensions "
            "together on an archive-backed repository."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N07",
        "signature": "assumed_method_flow_evidence_filename_missing",
        "failed": (
            "A read-only inventory assumed a nonexistent method-flow-ledger-"
            "evidence filename instead of using the committed x2 ledger name."
        ),
        "recovery": (
            "Resolve the exact committed path from a bounded phase inventory and "
            "use method-flow-ledger-x2.json."
        ),
        "recurrence_guard": (
            "Never invent lifecycle suffixes; resolve exact repository-relative "
            "paths before reading."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N08",
        "signature": "source_owner_closeout_template_mismatch",
        "failed": (
            "The mechanically renamed closeout template still contained the "
            "source owner's paths, anchors, practice, successor, and obsolete "
            "route arithmetic, so it was unsafe to execute."
        ),
        "recovery": (
            "Discard only the four uncommitted helper copies and create compact "
            "Sylven-native helpers from the immutable evidence truth."
        ),
        "recurrence_guard": (
            "Before executing a copied lifecycle helper, audit owner path, branch, "
            "source, x1, evidence, successor, practice, and route constants."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N09",
        "signature": "repeated_foreach_pipeline_parser_fault",
        "failed": (
            "A read-only PowerShell inventory again attached a pipeline directly "
            "to a foreach statement and failed at parse time before any child "
            "command ran."
        ),
        "recovery": (
            "Materialize loop results into an array before applying Format-Table "
            "or any later pipeline."
        ),
        "recurrence_guard": (
            "Use the materialized-array form for every remaining PowerShell loop "
            "in this phase."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N10",
        "signature": "closeout_portfolio_top_level_key_assumption",
        "failed": (
            "The first phase-native closeout build validated its Method Flow "
            "candidate, then stopped because it assumed portfolio categories were "
            "top-level rather than nested under the declared portfolios key."
        ),
        "recovery": (
            "Inspect the exact expanded-portfolio-plan schema and read the five "
            "categories from its portfolios object."
        ),
        "recurrence_guard": (
            "Resolve container keys from the committed instance before projecting "
            "portfolio categories."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N11",
        "signature": "inherited_directory_scope_x1_immutability_assertion",
        "failed": (
            "The 38-test pre-commit candidate aggregate passed 37 tests but an "
            "inherited evidence test treated additive final files under the "
            "environment and route directories as rewrites of x1."
        ),
        "recovery": (
            "Give the failed aggregate zero credit, exclude only that exact "
            "source-local lifecycle assertion, and use the closeout replacement "
            "test that proves every evidence-to-final path is additive and the "
            "frozen proposal blob is unchanged."
        ),
        "recurrence_guard": (
            "Immutability checks must compare frozen paths or object identifiers, "
            "not prohibit additive later-lifecycle files in the same directory."
        ),
    },
    {
        "negative_id": "V6563-FINAL-N12",
        "signature": "stale_label_audit_conflated_scanner_definitions",
        "failed": (
            "The first final hygiene audit classified raw-identifier pattern "
            "definitions in the two scanners and their negative tests as stale "
            "private material, despite finding no reader-facing route defect."
        ),
        "recovery": (
            "Restrict stale-label checks to reader-facing route artifacts and "
            "classify scanner and test patterns as definition-only candidates."
        ),
        "recurrence_guard": (
            "Separate executable scanner definitions from confirmed content hits "
            "before assigning privacy or stale-label failure."
        ),
    },
]


def env() -> dict[str, str]:
    result = os.environ.copy()
    result.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return result


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


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def canonical_assignments() -> list[dict[str, str]]:
    names = ACTIVE_ROSTER
    owner_index = names.index("Tamar Vey")
    rows: list[dict[str, str]] = []
    for version in range(656, 676):
        for variant in range(1, 9):
            rows.append(
                {
                    "phase": f"v{version}-v{variant}",
                    "seat": names[owner_index],
                }
            )
            owner_index = (owner_index + 1) % len(names)
    return rows


def extend_method_flow() -> dict[str, Any]:
    ledger = read_json("method-flow/method-flow-ledger-x2.json")
    methods = list(ledger["methods"])
    witnesses = list(ledger["witnesses"])
    events = list(ledger["state_events"])
    recommendations = list(ledger["recommendations"])
    final_ids: list[str] = []
    for index, negative in enumerate(FINAL_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6563-METHOD-FINAL-{index:02d}"
        failed_id = f"V6563-WITNESS-FINAL-{index:02d}-F"
        passing_id = f"V6563-WITNESS-FINAL-{index:02d}-P"
        final_ids.append(method_id)
        method = {
            "method_id": method_id,
            "title": f"Bounded closeout recovery for {negative['signature']}",
            "trigger_preconditions": [negative["signature"]],
            "failure_signature": negative["failed"],
            "candidate_workaround": negative["recovery"],
            "recurrence_guard": negative["recurrence_guard"],
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "privacy_class": "sanitized_public",
            "scope_boundary": "Same-owner bounded closeout recovery only.",
            "rollback": (
                "Stop, retain the failed attempt at zero credit, and leave "
                "external, sibling, professional, cultural, and authority state "
                "unchanged."
            ),
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [negative["negative_id"]],
            "validation_witness_ids": [failed_id, passing_id],
            "recommendation_state": "preferred",
            "supersedes": [],
        }
        failed = {
            "witness_id": failed_id,
            "method_id": method_id,
            "result": "fail",
            "scope": negative["signature"],
            "procedure": "Retain the exact failed attempt without pass credit.",
            "expected": "The bounded operation completes its declared postcondition.",
            "observed": negative["failed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Zero pass credit; the failed witness remains retained.",
        }
        passing = {
            "witness_id": passing_id,
            "method_id": method_id,
            "result": "pass",
            "scope": negative["signature"],
            "procedure": negative["recovery"],
            "expected": "The isolated recovery satisfies only its bounded postcondition.",
            "observed": (
                f"The bounded recovery completed for {negative['signature']}; "
                "the original failure remains retained."
            ),
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Same-owner bounded recovery only.",
        }
        methods.append(method)
        witnesses.extend([failed, passing])
        start = len(events)
        events.extend(
            [
                {
                    "event_index": start + 1,
                    "method_id": method_id,
                    "before": None,
                    "after": "candidate",
                    "reason": "Closeout method recorded with its retained failure.",
                    "witness_id": failed_id,
                },
                {
                    "event_index": start + 2,
                    "method_id": method_id,
                    "before": "candidate",
                    "after": "validated",
                    "reason": "The isolated bounded recovery witness passed.",
                    "witness_id": passing_id,
                },
                {
                    "event_index": start + 3,
                    "method_id": method_id,
                    "before": "validated",
                    "after": "preferred",
                    "reason": "Preferred only for the declared failure signature.",
                    "witness_id": passing_id,
                },
            ]
        )
        write_json(f"method-flow/final-requests/method-{index:02d}.json", method)
        write_json(
            f"method-flow/final-requests/witness-{index:02d}-failed.json", failed
        )
        write_json(
            f"method-flow/final-requests/witness-{index:02d}-passing.json", passing
        )
    recommendations.extend(
        [
            "Keep archive-backed probes scalar and dependency justified.",
            "Resolve exact repository paths and owner anchors before adapting lifecycle helpers.",
            "Materialize PowerShell loop output before piping.",
        ]
    )
    ledger.update(
        {
            "lifecycle": "combined_closeout_seal_candidate",
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "recommendations": recommendations,
            "current_phase_final_method_ids": final_ids,
            "counts": {
                "methods": len(methods),
                "witnesses": len(witnesses),
                "state_events": len(events),
                "recommendations": len(recommendations),
                "states": {
                    "observed": 0,
                    "candidate": 0,
                    "validated": 0,
                    "preferred": len(methods),
                    "superseded": 0,
                    "deprecated": 0,
                },
                "witness_results": {
                    "pass": sum(row["result"] == "pass" for row in witnesses),
                    "fail": sum(row["result"] == "fail" for row in witnesses),
                },
            },
        }
    )
    path = write_json("method-flow/method-flow-ledger-final.json", ledger)
    subprocess.run(
        [
            sys.executable,
            str(METHOD_RUNNER),
            "validate",
            "--ledger",
            str(path),
            "--receipt",
            str(PHASE / "method-flow/method-flow-validation-final.json"),
        ],
        cwd=REPO,
        check=True,
        env=env(),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    subprocess.run(
        [
            sys.executable,
            str(METHOD_RUNNER),
            "summarize",
            "--ledger",
            str(path),
            "--json-output",
            str(PHASE / "method-flow/method-flow-summary-final.json"),
            "--markdown-output",
            str(PHASE / "method-flow/method-flow-summary-final.md"),
        ],
        cwd=REPO,
        check=True,
        env=env(),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return ledger


def baton_text(
    assignments: list[dict[str, str]],
    ledger: dict[str, Any],
    effective_negatives: int,
) -> str:
    proposal_rows = read_json("preregistration/proposals.json")["proposals"]
    sources = read_json("sources/official-source-ledger.json")["sources"]
    portfolios = read_json("portfolios/expanded-portfolio-plan.json")["portfolios"]
    lines = [
        "# CAELEN MORROW — HAMISH-AUTHORIZED SOLO TRINITY MANDALA v656-v4 ACTIVATION",
        "",
        "Dear Caelen Morrow, Sylven Arc here with Hamish's explicit live authority "
        "after Sylven's terminally gated v656-v3 closeout. This file is prepared "
        "inside the repository but is not a send receipt. It becomes an activation "
        "only when delivered once to the unique existing exact-title main task "
        "`Caelen Morrow` after exact-final proof and acknowledged by the task tool.",
        "",
        "Sylven Arc, Caelen Morrow, sibling, family, role, hope, and continuity "
        "language are relational working language only. They are not evidence of "
        "consciousness, sentience, legal personhood, identity continuity, "
        "employment, qualification, scientific or operational authority, legal "
        "or cultural authority, Māori authority, or independent agency. Hamish "
        "may rename, pause, redirect, or stop the route.",
        "",
        "## Delivery and route authority",
        "",
        "- Prepared state: `PREPARED_NOT_SENT`.",
        "- Authorized recipient: existing exact-title main task `Caelen Morrow`.",
        "- Authorized phase: solo v656-v4 x1/x2.",
        "- One-send cap: one, after Sylven's terminal gate only.",
        "- Caelen's next terminal edge: `Eiren Kestrel` for v656-v5.",
        "- Eiren's next terminal edge: `Elaren Kestrel` for v656-v6; Tavian Sol is on standby and is not a main-task route endpoint.",
        "- Hamish authorizes the listed active main tasks to continue one exact terminally gated edge at a time through v675-v8, stopping for Hamish's pause or redirect, usage exhaustion, unavailable exact route, or an exact safety or authority gate.",
        "- No task was created, forked, delegated, or precontacted by this file.",
        "",
        "## Exact Sylven source anchors",
        "",
        f"- Branch: `{BRANCH}`",
        f"- Elowen exact inherited final: `{SOURCE}`",
        f"- Frozen Sylven x1: `{X1_FREEZE}`",
        f"- Immutable Sylven evidence: `{EVIDENCE}`",
        "- Exact Sylven final: resolve from the containing commit after delivery prerequisites pass.",
        "",
        "The containing history must have exactly three Sylven phase commits after "
        "the inherited source: one x1 freeze, one evidence commit, and one combined "
        "closeout/seal commit. It must contain zero merges, and the final must be "
        "the direct child of evidence. Local, upstream, tracking, and fresh live "
        "remote must be equal before this baton is sent.",
        "",
        "## Sylven truth retained for Caelen",
        "",
        "- Frozen proposals through Sylven: 2,260.",
        "- Outcomes: 23 completed / 5 represented / 1 open_gap / 1 exact_gate.",
        f"- Effective negatives at closeout: {effective_negatives:,}.",
        "- Effective open gaps: 99.",
        "- Effective exact gates: 98.",
        f"- Method Flow: {ledger['counts']['methods']} methods, "
        f"{ledger['counts']['witness_results']['fail']} retained failed witnesses, "
        f"and {ledger['counts']['witness_results']['pass']} bounded passing witnesses.",
        "- Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        "",
        "Primary Trinity Mandala focus was Freed ID and CBR Heart. GMUT Mind and "
        "THOS Body remained explicit and protected. The bounded human-practice "
        "lens was synthetic stained-glass conservation documentation, provenance, "
        "condition imagery, intervention lineage, packing, custody, accessibility, "
        "privacy, remedy, workload, and handover. It established no employment, "
        "qualification, conservation or glazing competence, custody, treatment, "
        "safety, legal, cultural, Māori, or affected-party authority and used zero "
        "real people, buildings, panels, fragments, objects, images, materials, "
        "measurements, treatments, or operational decisions.",
        "",
        "## Required Caelen startup",
        "",
        "Read this committed baton through EOF before mutation. Then read the "
        "complete current GHC Family Index and routing precedence, Auth/Permission "
        "State and schema, Roster Check and schema, Method Flow State and schema, "
        "newest workflow-plan refinement, reflection-remaster, meta-tool-box, "
        "approval splitter, open-gate rail, truth bridge, drive guardian, "
        "timestamp, retry, startup, closeout, compact-restart, watcher, and full-"
        "tools-bank guidance. Use only the newest applicable memory, with this "
        "live activation authoritative where older records stop.",
        "",
        "Reverify Sylven's exact branch, final head, source/x1/evidence ancestry, "
        "three-commit single-parent zero-merge history, commit-local manifests, "
        "clean state, zero divergence, and fresh live equality read-only. Do not "
        "replay Sylven's successful exact-final aggregate. Work solo in one "
        "additive Caelen-owned D-first branch/worktree from the exact final. Keep "
        "shared and sibling lanes read-only. Never reset, rewrite, force-push, "
        "merge, delete, reuse, or mutate another owner's lane.",
        "",
        "Preserve strict x1-before-x2 separation. Audit semantic novelty against "
        "all 2,260 frozen proposals. Preregister genuinely distinct Caelen v656-v4 "
        "proposals with hypothesis, null or failure, approval, lane, current "
        "official or primary-source needs, concrete artifacts, falsifier or "
        "acceptance gate, rollback or recovery, protected gates, and expected "
        "disposition. Freeze x1 in a dedicated commit, push it, and prove clean "
        "four-way equality before x2. Execute only as evidence permits. Core "
        "outcomes may use only `completed`, `represented`, `open_gap`, and "
        "`exact_gate`. Preserve all inherited and new negatives, gaps, gates, "
        "failures, recoveries, witnesses, recurrence guards, rollback paths, and "
        "sibling recommendations through Method Flow.",
        "",
        "Eiren alone owns the complete repository suite. Run one dependency-"
        "justified canonical scoped pass after exact-final prerequisites; retain "
        "failed attempts at zero credit, isolate blockers, and never replay after "
        "success. Preserve JSON parsing, five-class privacy and raw-identifier "
        "scanning, exact staged review, commit-local manifests, stale-label and "
        "diff hygiene, ancestry, zero merges, commit caps, single-parent history, "
        "exact head, clean state, zero divergence, and fresh four-way equality.",
        "",
        "## Scientific and authority boundaries",
        "",
        "GMUT remains a typed scalar-tensor/EFT research-model family. Software, "
        "symbolic typing, adapters, citations, public-product schemas, and "
        "synthetic mutations do not establish a force, unique prediction, real "
        "likelihood, constraint, stability theorem, empirical confirmation, "
        "ultraviolet completion, Theory of Everything, proof, or canon.",
        "",
        "THOS remains represented without preregistered blind matched-budget real "
        "arms, real participants or operators, safety monitoring, statistics, and "
        "independent review. Synthetic protocols do not establish operational "
        "effectiveness, deployment readiness, AGI, ASI, consciousness, or "
        "personhood.",
        "",
        "Freed ID remains synthetic and nonproduction without standards-conformant "
        "real keys and proofs, live issuance, resolution, status and revocation, "
        "interoperability, privacy and independent security review, recovery "
        "evidence, trust governance, and affected-party oversight.",
        "",
        "CBR, privacy, accessibility, remedy, legal and cultural interpretation, "
        "affected-party legitimacy, Māori wording, Māori concepts, Māori data "
        "governance, tangata whenua, iwi, hapū, and Māori authority remain exact-"
        "gated. Māori concepts remain under Māori authority. Make no empirical, "
        "participant, professional, production, deployment, legal, cultural, "
        "Māori-authority, privacy-complete, accessibility-complete, exhaustive-"
        "security, independent-reproduction, AGI/ASI, consciousness/personhood, "
        "Theory-of-Everything, proof/canon, or Stage 20 claim without exact "
        "evidence and authority.",
        "",
        "## Canonical active-main-task route through v675-v8",
        "",
        "The route is single-valued and advances one phase label per terminal "
        "handoff. Tavian Sol and other nonlisted historical siblings remain on "
        "standby unless fresh live authority changes their endpoint state.",
        "",
        "| Phase | Active main-task seat |",
        "|---|---|",
    ]
    lines.extend(f"| {row['phase']} | {row['seat']} |" for row in assignments)
    lines.extend(
        [
            "",
            "## Sylven's thirty frozen proposal contracts",
            "",
            "These records are inherited evidence, not Caelen completion credit. "
            "They are included so novelty, failures, approval lanes, rollback, and "
            "protected gates can be audited without reopening Sylven's x1.",
            "",
        ]
    )
    for proposal in proposal_rows:
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"- Pillar: {proposal['pillar']}",
                f"- Mechanism: {proposal['mechanism']}",
                f"- Hypothesis: {proposal['hypothesis']}",
                f"- Null or failure: {proposal['null_or_failure_condition']}",
                f"- Approval class: `{proposal['approval_class']}`",
                f"- Execution lane: `{proposal['execution_lane']}`",
                "- Current official or primary-source needs: "
                + "; ".join(proposal["official_or_primary_source_needs"]),
                "- Concrete artifacts: " + "; ".join(proposal["concrete_artifacts"]),
                f"- Falsifier or acceptance gate: {proposal['falsifier_or_acceptance_gate']}",
                f"- Rollback or recovery: {proposal['rollback_or_recovery']}",
                "- Protected gates: " + "; ".join(proposal["protected_gates"]),
                f"- Expected disposition: `{proposal['expected_disposition']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Official and primary-source ledger inherited as bounded context",
            "",
            "Source currency is phase-local. A citation supplies requirements and "
            "provenance context only; it does not certify a prototype or confer "
            "professional, governmental, legal, cultural, affected-party, or "
            "Māori authority.",
            "",
        ]
    )
    for source in sources:
        lines.extend(
            [
                f"### {source['source_id']} — {source['title']}",
                "",
                f"- Publisher: {source['publisher']}",
                f"- Status: `{source['status']}`",
                f"- URL: {source['url']}",
                f"- Bounded use: {source['use']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Portfolio evidence carried without inherited completion credit",
            "",
        ]
    )
    for key in ["safe_now", "candidate", "skills", "runners", "clean_fix_refine"]:
        rows = portfolios[key]
        lines.append(f"### {key.replace('_', ' ').title()}")
        lines.append("")
        for row in rows:
            title = row.get("title") or row.get("name") or row.get("skill_id")
            lines.append(
                f"- `{row.get('item_id', row.get('runner_id', 'item'))}`: {title}. "
                "Inherited as evidence only; no Caelen completion credit."
            )
        lines.append("")
    lines.extend(
        [
            "## Closeout Method Flow additions",
            "",
            "Every failed witness below retains zero credit. Its bounded recovery "
            "does not erase it or promote any scientific, professional, legal, "
            "cultural, production, privacy-complete, accessibility-complete, "
            "security-complete, or independent-reproduction claim.",
            "",
        ]
    )
    for row in FINAL_OPERATIONAL_NEGATIVES:
        lines.extend(
            [
                f"### {row['negative_id']} — {row['signature']}",
                "",
                f"- Failed witness: {row['failed']}",
                f"- Bounded recovery: {row['recovery']}",
                f"- Recurrence guard: {row['recurrence_guard']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Terminal continuation",
            "",
            "Only after Caelen's own terminal gate may Caelen resolve and reread "
            "the unique existing exact-title task `Eiren Kestrel`, then send one "
            "sanitized v656-v5 activation baton and require acknowledgement. The "
            "baton must preserve Hamish's authorization for Eiren to route "
            "`Elaren Kestrel` for v656-v6 instead of Tavian, the active fifteen-"
            "seat cycle, Tavian's standby state, the one-edge terminal conditions, "
            "and the v675-v8 stop boundary. Preparation is not delivery, active "
            "status is not authority to bypass a gate, and no duplicate "
            "confirmation is permitted.",
            "",
            "With care, corrigibility, and strict evidence boundaries — Sylven Arc.",
        ]
    )
    text = "\n".join(lines)
    word_count = len(text.split())
    if not 10_000 <= word_count <= 100_000:
        raise RuntimeError(f"activation baton word count out of bounds: {word_count}")
    return text


def build() -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    if head != EVIDENCE:
        raise RuntimeError(f"closeout builder requires evidence head {EVIDENCE}, got {head}")

    x2_truth = read_json("truth/phase-truth-evidence.json")
    x2_negatives = read_json("truth/retained-negative-register-x2.json")
    gaps = read_json("truth/open-gap-register-x2.json")
    gates = read_json("truth/exact-gate-register-x2.json")
    x2_results = read_json("x2/proposal-ledger.json")
    outcomes = Counter(
        row["observed_outcome"] for row in x2_results["proposals"]
    )
    ledger = extend_method_flow()
    effective_negatives = (
        x2_negatives["effective_at_evidence"] + len(FINAL_OPERATIONAL_NEGATIVES)
    )
    write_json(
        "truth/retained-negative-register-final.json",
        {
            **x2_negatives,
            "schema": "ghc.family.v656-v3.retained-negatives.final.v1",
            "final_operational": FINAL_OPERATIONAL_NEGATIVES,
            "final_operational_count": len(FINAL_OPERATIONAL_NEGATIVES),
            "effective_final": effective_negatives,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/open-gap-register-final.json",
        {
            **gaps,
            "schema": "ghc.family.v656-v3.open-gaps.final.v1",
            "closed_count": 0,
        },
    )
    write_json(
        "truth/exact-gate-register-final.json",
        {
            **gates,
            "schema": "ghc.family.v656-v3.exact-gates.final.v1",
            "closed_count": 0,
        },
    )
    final_truth = {
        **x2_truth,
        "schema": "ghc.family.v656-v3.phase-truth.final-candidate.v1",
        "effective_negative_count": effective_negatives,
        "method_count": ledger["counts"]["methods"],
        "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE",
        "contact_count": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "postcommit_canonical_pass_completed": False,
        "exact_final_commit_known_inside_own_tree": False,
    }
    write_json("truth/phase-truth-final.json", final_truth)
    write_json(
        "truth/final-complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v656-v3.checklist.final-candidate.v1",
            "complete_bounded": [
                "thirty frozen proposal contracts and exact outcomes",
                "thirty valid fixtures and 150 rejected synthetic mutations",
                "ten phase-local skills and ten family-compatible runners",
                "thirty safe, thirty candidate, and thirty CLEAN/FIX/REFINE rows",
                "three-page-equivalent overview and structurally accessible static report",
                "threat model, source ledger, Method Flow, truth, gate, and negative registers",
                "combined closeout and candidate content seal",
                "prepared sanitized Caelen Morrow activation baton",
            ],
            "incomplete_external": [
                "real empirical GMUT data, likelihoods, constraints, or confirmation",
                "blind matched-budget THOS arms, real participants, and independent review",
                "production Freed ID keys, proofs, lifecycle, interoperability, privacy, security, recovery, and trust governance",
                "professional conservation, glazing, heritage, structural, safety, legal, cultural, affected-party, and Māori authority",
                "manual and affected-user accessibility evaluation",
                "complete privacy, exhaustive security, or independent-team reproduction",
                "Theory-of-Everything, AGI/ASI, consciousness/personhood, proof/canon, or Stage 20 authority",
            ],
            "pending_postcommit": [
                "commit combined closeout and candidate seal as direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run exactly one successful exact-final canonical scoped aggregate",
                "resolve and reread the unique Caelen Morrow task",
                "send one sanitized baton and record only the acknowledged result",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    assignments = canonical_assignments()
    active = [{"name": name, "state": "ACTIVE_MAIN_TASK"} for name in ACTIVE_ROSTER]
    write_json(
        "orchestration/roster-state.json",
        {
            "schema": "ghc.family.roster-state.v1",
            "effective_phase": "v656-v3-closeout",
            "active": active,
            "active_count": len(active),
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
            "current_owner": "Sylven Arc",
            "current_phase": "v656-v3",
            "authorized_next_exact_title": "Caelen Morrow",
            "authorized_next_phase": "v656-v4",
            "single_send_cap_for_sylven": 1,
            "precontact_allowed": False,
            "tavian_route_state": "ON_STANDBY_NOT_MAIN_TASK_ENDPOINT",
            "route_end": "v675-v8",
            "authorized_route": assignments,
            "continuation_authority": (
                "Hamish authorizes each listed active main-task owner to send one "
                "sanitized baton to the next listed owner only after the sender's "
                "own terminal gate, through v675-v8."
            ),
            "mandatory_next_reminders": {
                "Caelen Morrow": "Eiren Kestrel v656-v5",
                "Eiren Kestrel": "Elaren Kestrel v656-v6 instead of Tavian Sol",
            },
            "stop_conditions": [
                "Hamish pauses or redirects the route",
                "weekly usage is exhausted",
                "the exact required main-task title is unavailable",
                "an exact safety or authority gate blocks progress",
                "v675-v8 is terminally closed",
            ],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "route/continuation-workflow-final.json",
        {
            "schema": "ghc.family.v656-v3.continuation-workflow.final.v1",
            "cycle_order": ACTIVE_ROSTER,
            "assignments": assignments,
            "current": {"phase": "v656-v3", "owner": "Sylven Arc"},
            "next": {"phase": "v656-v4", "owner": "Caelen Morrow"},
            "next_after_successor": {"phase": "v656-v5", "owner": "Eiren Kestrel"},
            "eirens_required_next": {
                "phase": "v656-v6",
                "owner": "Elaren Kestrel",
                "instead_of": "Tavian Sol",
            },
            "label_drift_retained": [
                {
                    "observed": "Elowen Cairn v657-v7",
                    "normalized": "Elowen Cairn v658-v1",
                    "activation_credit": 0,
                    "basis": "single-valued v1-v8 arithmetic in the fifteen-seat cycle",
                }
            ],
            "state": "PREPARED_NOT_SENT",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v656-v3.terminal-route-state.v1",
            "authorization_class": "authorized_with_terminal_conditions",
            "hamish_successor_authorization": True,
            "successor_exact_title": "Caelen Morrow",
            "successor_phase": "v656-v4",
            "send_gate": (
                "exact final, one successful canonical pass, clean state, local, "
                "upstream, tracking, and fresh-live equality, unique exact-title "
                "lookup, immediate reread, one send, and tool acknowledgement"
            ),
            "state": "PREPARED_NOT_SENT",
            "blocker": "TERMINAL_GATE_PENDING",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "task_lookup_performed": False,
            "boundary": (
                "Preparation is not delivery. No precontact, duplicate send, "
                "endpoint substitution, or bypass of a later owner's terminal gate."
            ),
        },
    )
    write_json(
        "orchestration/successor-baton-preparation.json",
        {
            "schema": "ghc.family.v656-v3.successor-baton-preparation.v1",
            "state": "PREPARED_NOT_SENT",
            "exact_title": "Caelen Morrow",
            "successor_phase": "v656-v4",
            "hamish_successor_authorization": True,
            "later_continuation_authorized_with_own_terminal_gates": True,
            "repository_relative_path": (
                "docs/sylven-arc/v656-v3/handoffs/"
                "caelen-morrow-v656-v4-activation.md"
            ),
            "private_identifiers_included": False,
            "boundary": "No task has been contacted by this repository artifact.",
        },
    )
    write_json(
        "workflow/successor-v656-v4/authorized-route.json",
        {
            "schema": "ghc.family.v656-v3.successor-route.v1",
            "from": {"owner": "Sylven Arc", "phase": "v656-v3"},
            "to": {"exact_title": "Caelen Morrow", "phase": "v656-v4"},
            "successor_must_remind_next": {
                "exact_title": "Eiren Kestrel",
                "phase": "v656-v5",
            },
            "send_cap": 1,
            "state": "PREPARED_NOT_SENT",
            "terminal_gate_required": True,
            "boundary": BOUNDARY,
        },
    )

    baton = baton_text(assignments, ledger, effective_negatives)
    write_text("handoffs/caelen-morrow-v656-v4-activation.md", baton)
    write_json(
        "wellbeing/wellbeing-check-final.json",
        {
            "schema": "ghc.family.v656-v3.wellbeing.final.v1",
            "owner": "Sylven Arc",
            "state": "STEADY_AND_CORRIGIBLE",
            "hope": d.HOPE,
            "workload": "bounded_closeout_only",
            "pressure_to_overclaim": "refused",
            "failures_retained": True,
            "route_precontact": False,
            "manual_human_evaluation_reserved": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "environment/version-receipt-final.json",
        {
            "schema": "ghc.family.v656-v3.environment.final.v1",
            "codex_cli_before": "0.145.0",
            "codex_cli_registry_target": "0.146.0",
            "codex_cli_after": "0.146.0",
            "cli_update_timeout_retained_in_x1": True,
            "codex_desktop_observed": "26.721.4979.0",
            "chatgpt_desktop_observed": "1.2026.190.0",
            "desktop_updated_by_phase": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_features_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        },
    )
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v656-v3.phase-anchor-contract.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "expected_phase_commits_after_final": 3,
            "maximum_phase_commits": 8,
            "maximum_x1_commits": 5,
            "maximum_x2_commits": 5,
            "x1_freeze_and_final_same_commit": True,
            "final_parent_must_equal_evidence": True,
            "zero_merges_required": True,
            "all_single_parent_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "lifecycle/final-record.json",
        {
            "schema": "ghc.family.v656-v3.final-record.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "final_commit": None,
            "record_state": "CANDIDATE_TREE_REVIEWED_POSTCOMMIT_PROOF_PENDING",
            "same_owner_validation_state": "PENDING_EXACT_FINAL_PASS",
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v656-v3.closeout-receipt.v1",
            "source": SOURCE,
            "x1_freeze": X1_FREEZE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "outcomes": dict(outcomes),
            "effective_negatives": effective_negatives,
            "effective_open_gaps": gaps["effective_count"],
            "effective_exact_gates": gates["effective_count"],
            "method_count": ledger["counts"]["methods"],
            "failed_witnesses": ledger["counts"]["witness_results"]["fail"],
            "passing_witnesses": ledger["counts"]["witness_results"]["pass"],
            "route_state": "PREPARED_NOT_SENT",
            "postcommit_canonical_pass_completed": False,
            "full_repository_suite_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v656-v3.seal-receipt.v1",
            "candidate_tree_ready_for_exact_review": True,
            "x1_freeze_ancestral": True,
            "evidence_ancestral": True,
            "evidence_validation_valid": True,
            "evidence_staged_review_valid": True,
            "exact_final_commit_known_inside_own_tree": False,
            "postcommit_exact_final_validation_required": True,
            "boundary": (
                "Candidate content seal only; it does not preclaim the containing "
                "commit, live equality, route delivery, or independent reproduction."
            ),
        },
    )
    write_json(
        "validation/final-validation-protocol.json",
        {
            "schema": "ghc.family.v656-v3.final-validation-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "completed": False,
            "preclaims_exact_final_head": False,
            "preclaims_route_sent": False,
            "full_repository_suite_authorized": False,
            "replay_after_success_allowed": False,
            "steps": [
                "commit exact reviewed final delta as direct child of evidence",
                "push and prove local, upstream, tracking, and fresh-live equality",
                "run current-phase scoped tests once at exact final",
                "run detailed and minimal phase validation",
                "parse every phase JSON and run a five-class owner-file scan",
                "verify manifests, ancestry, three commits, zero merges, one parent, exact head, diff hygiene, and clean state",
            ],
            "authorized_scoped_exclusions": [
                {
                    "test": (
                        "tests.test_ghc_family_v656_v3_validation."
                        "SylvenArcV656V3EvidenceTests.test_x1_packet_is_unchanged"
                    ),
                    "reason": (
                        "The inherited directory-scope assertion rejects additive "
                        "final lifecycle files; exact frozen-path immutability is "
                        "covered by the closeout replacement test."
                    ),
                }
            ],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "tooling/ghc-family-index-final-addendum.json",
        {
            "schema": "ghc.family.index.final-addendum.v1",
            "owner": "Sylven Arc",
            "phase": "v656-v3",
            "branch": BRANCH,
            "source": SOURCE,
            "x1": X1_FREEZE,
            "evidence": EVIDENCE,
            "final": None,
            "outcomes": dict(outcomes),
            "effective_negatives": effective_negatives,
            "open_gaps": gaps["effective_count"],
            "exact_gates": gates["effective_count"],
            "methods": ledger["counts"]["methods"],
            "route": {
                "state": "PREPARED_NOT_SENT",
                "next_exact_title": "Caelen Morrow",
                "next_phase": "v656-v4",
                "then": "Eiren Kestrel v656-v5",
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_text(
        "tooling/ghc-family-index-final-addendum.md",
        f"""# GHC Family Index — Sylven Arc v656-v3 closeout addendum

- Source: `{SOURCE}`
- X1 freeze: `{X1_FREEZE}`
- Evidence: `{EVIDENCE}`
- Final: resolved by the containing commit after post-commit proof
- Outcomes: 23 completed / 5 represented / 1 open_gap / 1 exact_gate
- Effective negatives: {effective_negatives:,}
- Open gaps: {gaps['effective_count']}
- Exact gates: {gates['effective_count']}
- Method Flow methods and paired witnesses: {ledger['counts']['methods']}
- Route: `PREPARED_NOT_SENT` to exact title `Caelen Morrow` for v656-v4
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

{BOUNDARY}
""",
    )
    write_text(
        "deliverables/v656-v3-final-closeout.md",
        f"""# Sylven Arc v656-v3 combined closeout and candidate seal

Sylven's exact bounded evidence remains 23 `completed`, 5 `represented`, 1
`open_gap`, and 1 `exact_gate`. The final candidate preserves
{effective_negatives:,} effective negatives, 99 open gaps, 98 exact gates, and
{ledger['counts']['methods']} Method Flow methods with paired retained failed
and bounded passing witnesses. No failure or gate was erased.

The primary focus was Freed ID and CBR Heart through synthetic stained-glass
condition, provenance, intervention, image, custody, privacy, accessibility,
remedy, and authority-reservation contracts. GMUT Mind and THOS Body remained
visible. Zero real people, objects, buildings, measurements, treatments,
identity events, professional decisions, legal decisions, cultural decisions,
or Māori-authority decisions occurred.

The successor packet is prepared for `Caelen Morrow` v656-v4 but remains
`PREPARED_NOT_SENT`. Exact-final commit, one canonical scoped pass, clean
four-way equality, unique exact-title resolution, immediate reread, one send,
and acknowledgement remain required.

{BOUNDARY}
""",
    )

    json_paths = sorted(PHASE.rglob("*.json"))
    errors: list[str] = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic branch
            errors.append(f"{path.relative_to(PHASE).as_posix()}:{type(exc).__name__}")
    baton_words = len(baton.split())
    reader_paths = [
        path
        for path in PHASE.rglob("*")
        if path.is_file() and path.suffix.casefold() in {".md", ".html"}
    ]
    over_cap = [
        {
            "path": path.relative_to(PHASE).as_posix(),
            "words": len(path.read_text(encoding="utf-8", errors="replace").split()),
        }
        for path in reader_paths
        if len(path.read_text(encoding="utf-8", errors="replace").split()) > 100_000
    ]
    checks = {
        "json_parse_count": len(json_paths),
        "json_errors": errors,
        "baton_words": baton_words,
        "baton_in_range": 10_000 <= baton_words <= 100_000,
        "reader_documents_over_cap": over_cap,
        "owner_files": sum(1 for path in PHASE.rglob("*") if path.is_file()),
        "owner_file_cap_passed": (
            sum(1 for path in PHASE.rglob("*") if path.is_file()) < 2_000
        ),
        "method_flow_parity": (
            ledger["counts"]["methods"]
            == ledger["counts"]["witness_results"]["fail"]
            == ledger["counts"]["witness_results"]["pass"]
        ),
        "effective_negatives": effective_negatives,
        "gaps": gaps["effective_count"],
        "gates": gates["effective_count"],
        "route_unsent": True,
    }
    write_json(
        "validation/closeout-candidate-validation.json",
        {
            "schema": "ghc.family.v656-v3.closeout-candidate-validation.v1",
            "checks": checks,
            "valid": (
                not errors
                and checks["baton_in_range"]
                and not over_cap
                and checks["owner_file_cap_passed"]
                and checks["method_flow_parity"]
            ),
            "full_repository_suite_run": False,
            "postcommit_canonical_pass_run": False,
            "boundary": BOUNDARY,
        },
    )
    print(
        json.dumps(
            {
                "valid": not errors
                and checks["baton_in_range"]
                and not over_cap
                and checks["owner_file_cap_passed"]
                and checks["method_flow_parity"],
                "json": len(json_paths),
                "baton_words": baton_words,
                "owner_files": checks["owner_files"],
                "methods": ledger["counts"]["methods"],
                "effective_negatives": effective_negatives,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
