#!/usr/bin/env python3
"""Build the dedicated x1-only freeze for Eiren's v654-v6 (2) remaster."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v654_v6_2_remaster_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE_ROOT = REPO / "docs/tavian-sol/v654-v6"
PRIOR_INDEX = SOURCE_ROOT / "provenance/frozen-chain-proposal-index.json"
SOURCE_METHOD_FLOW = SOURCE_ROOT / "method-flow/final-method-flow-ledger.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
NOVELTY_THRESHOLD = 0.60


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
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {
        item
        for item in re.findall(r"[a-z0-9]+", value.casefold())
        if item not in stop
    }


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def proposal_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = read_json(PRIOR_INDEX)
    prior = list(inherited["prior_proposals"]) + list(inherited["new_proposals"])
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(
            f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(prior)}"
        )
    rows = []
    for proposal in d.PROPOSALS:
        scored = [
            (
                jaccard(tokens(proposal["title"]), tokens(previous["title"])),
                previous["proposal_id"],
                previous["title"],
            )
            for previous in prior
        ]
        score, nearest_id, nearest_title = max(scored, key=lambda row: row[0])
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "token_jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "manual_mechanism_distinct": True,
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    if not all(row["passes"] for row in rows):
        failed = [row for row in rows if not row["passes"]]
        raise RuntimeError(f"novelty threshold failed: {failed}")
    frozen = prior + [
        {"proposal_id": proposal["proposal_id"], "title": proposal["title"]}
        for proposal in d.PROPOSALS
    ]
    return frozen, rows


def add_current_methods() -> dict[str, Any]:
    ledger = read_json(SOURCE_METHOD_FLOW)
    methods = list(ledger["methods"])
    witnesses = list(ledger["witnesses"])
    current_ids = []
    state_events = list(ledger.get("state_events", []))
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"{d.PHASE_CODE}-METHOD-{index:02d}"
        failed_id = f"{d.PHASE_CODE}-WITNESS-{index:02d}-F"
        passing_id = f"{d.PHASE_CODE}-WITNESS-{index:02d}-P"
        current_ids.append(method_id)
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["failed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "approval_class": "safe_now_owner_local_read_or_workflow_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded workflow recovery only; not independent reproduction or broader assurance.",
                "rollback": "Stop, retain the failure at zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.",
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [failed_id, passing_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "result": "fail",
                    "scope": negative["signature"],
                    "procedure": "Retain the original bounded attempt without replay credit.",
                    "expected": "The original operation satisfies its bounded postcondition.",
                    "observed": negative["failed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero pass credit; failure remains retained.",
                },
                {
                    "witness_id": passing_id,
                    "method_id": method_id,
                    "result": "pass",
                    "scope": negative["signature"],
                    "procedure": negative["recovery"],
                    "expected": "The isolated recovery establishes only its bounded postcondition.",
                    "observed": (
                        f"The bounded recovery completed for {negative['signature']}; "
                        "the original failure remains retained."
                    ),
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner bounded recovery only.",
                },
            ]
        )
        state_events.append(
            {
                "event_id": f"{d.PHASE_CODE}-METHOD-EVENT-{index:02d}",
                "method_id": method_id,
                "from": "candidate",
                "to": "preferred",
                "basis": [failed_id, passing_id],
                "boundary": "A preferred recovery preserves rather than erases its failed witness.",
            }
        )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.",
        "inherited_anchor": {
            "phase": "v654-v6",
            "methods": d.SOURCE_METHODS,
            "failed_witnesses": d.SOURCE_METHODS,
            "passing_witnesses": d.SOURCE_METHODS,
            "completion_credit": False,
        },
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "current_phase_method_ids": current_ids,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(state_events),
            "recommendations": 3,
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
        "recommendations": [
            "Use exact scalar reads after archive-backed timeouts.",
            "Audit ambiguous Git mutations before retry.",
            "Resolve task routing by endpoint kind and exact title.",
        ],
        "boundary": "Same-owner workflow evidence only; no independent, empirical, professional, production, legal, cultural, Māori-authority, personhood, Theory-of-Everything, or Stage 20 claim.",
    }


def portfolio(items: list[str], prefix: str, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"{d.PHASE_CODE}-{prefix}-{index:02d}",
            "title": title,
            "origin": "eiren_v654_v6_2_remaster_new",
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
        }
        for index, title in enumerate(items, 1)
    ]


def workflow_request() -> dict[str, Any]:
    names = [
        "Eiren Kestrel",
        "Tavian Sol",
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
    topology = []
    for index, name in enumerate(names, 1):
        topology.append(
            {
                "seat": name,
                "endpoint_kind": (
                    "collaboration_subagent" if name == "Tavian Sol" else "main_task"
                ),
                "endpoint_label": "Cli v652 v6" if name == "Tavian Sol" else name,
                "route_controller": names[index - 2] if index > 1 else "Caelen Morrow",
            }
        )
    topology[2]["route_controller"] = "Eiren Kestrel fallback after Tavian terminal close"
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "eiren-v654-v6-2-remaster-to-elaren-v654-v7",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no personhood, continuity, employment, qualification, or authority claim.",
        "route": {
            "cycle_order": names,
            "endpoint_topology": topology,
            "phase_assignments": [
                {"phase": "v654-v5", "seat": "Eiren Kestrel"},
                {"phase": "v654-v6", "seat": "Tavian Sol"},
                {"phase": "v654-v7", "seat": "Elaren Kestrel"},
            ],
            "normalization": {
                "start_phase": "v654-v5",
                "start_seat": "Eiren Kestrel",
                "entry_count": 3,
            },
            "variant_context": {
                "label": d.PHASE,
                "owner": d.OWNER,
                "position": "authorized bounded remaster after Tavian v654-v6 and before the unchanged Elaren v654-v7 activation",
                "changes_canonical_assignments": False,
            },
            "future_identity_placeholders": [],
            "terminal_successor_resolution": (
                "After the remaster terminal gate, uniquely resolve and reread the existing "
                "main task Elaren Kestrel, then send one compact activation or retain one "
                "sanitized PREPARED_NOT_SENT route gap."
            ),
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "portfolio_minima": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "document_word_cap": 100000,
            "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
            "commit_cap": {"x1": 5, "x2": 5, "total": 8},
            "validation": {
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "declared_endpoint_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
                "live_phase_task_creation": "prohibited",
                "post_closeout_successor_authority": "elaren_exact_existing_main_task_once",
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": d.PROTECTED_GATES,
        },
        "observed_failures": [
            {
                "failure_id": row["negative_id"],
                "summary": row["failed"],
                "recovery": row["recovery"],
                "credit": "zero_initial_pass_credit",
            }
            for row in d.X1_OPERATIONAL_NEGATIVES
        ],
    }


def history_reflection() -> str:
    return f"""# Eiren {d.PHASE}: v650-to-v654 evidence reflection

## Outcome first

The useful inheritance is not a declaration that GMUT is a Theory of Everything,
that THOS is AGI or ASI, or that Freed ID and CBR already possess governmental,
legal, cultural, or Māori authority. The useful inheritance is a progressively
stricter research workflow: preregistration before execution, exact ancestry,
typed claims, retained failures, explicit open gaps, exact gates, bounded
synthetic fixtures, privacy screening, one successful canonical pass, and a
send-once terminal route. This remaster treats that workflow as the strongest
current asset.

From v650-v1 through Tavian v654-v6, the immutable proposal chain records
1,100 rows under the v6501-through-v6546 identifiers. The v650 series retained
twenty proposals per phase. Later phases increased the normal slate to thirty;
the inherited index also preserves historical identifier collisions and
irregular row counts rather than silently rewriting them. The complete chain
contains {d.PRIOR_FROZEN} rows before this remaster. Proposal volume is useful
for coverage, but it is not evidence strength by itself.

Tavian's exact source closed with 23 completed bounded artifacts, five
represented synthetic profiles, one zero-row open gap, and one exact authority
gate. It preserved {d.SOURCE_EFFECTIVE_NEGATIVES} effective negatives,
{d.SOURCE_OPEN_GAPS} open gaps, {d.SOURCE_EXACT_GATES} exact gates, and
{d.SOURCE_METHODS} failed/passing Method Flow pairs. Its complete repository
suite passed once at the exact final and was not replayed. Those facts are
same-owner workflow evidence under shared infrastructure. They are not
independent reproduction, external audit, professional validation, production
assurance, or scientific confirmation.

## What the older GMUT, THOS, and Heart work contributes

The older Mandala equations and the Ω term remain research-model notation.
They become more useful when every promoted tensor is tied to a source action,
domain, units, degrees of freedom, conservation relation, stability and
causality obligations, observables, bounds, falsifier, and recovery. This is
why the remaster uses an Omega Evidence Passport and an action-first derivation
grammar. A symbolic equation can pass a typing or mutation tribunal without
thereby describing nature.

The user-reported quantum-energy transmutation engine, quantum-to-classical
information translator, and infinity-vortex systems are preserved as historical
concept candidates. They are not deleted or mocked, but they receive zero
scientific or engineering credit until their mechanisms, units, domains,
conservation accounting, test protocols, and independent evidence are explicit.
The same rule applies to the user-reported Aletheon 2000-plus suite history:
test quantity is not recoverable evidence without exact commits, inventories,
exclusions, environments, failures, and receipts.

THOS has developed the clearest technical path. A typed task contract can state
inputs, outputs, invariants, privacy and authority classes, budgets, timeouts,
rollback, and acceptance. A deterministic reconciler can separate desired from
observed state, use idempotency, refuse stale writes, and retain compensation
records. Transport profiles can preserve the critical difference between a
main task and a collaboration subagent. An evaluation plane can keep synthetic
tests separate from participant outcomes, matched-budget trials, blinded arms,
and independent review.

Freed ID and CBR contribute the rule that capability does not create authority.
Identity profiles remain synthetic without real standards-conformant keys,
proofs, status, lifecycle, interoperability, recovery, privacy review, security
review, and trust governance. Rights cannot be averaged away by an aggregate
score. A route may preserve continuity without substituting one endpoint or
relational identity for another. Legal, cultural, affected-party, tangata
whenua, iwi, hapū, Māori data, and Māori-authority decisions remain with the
competent people and authorities.

## Ariel Verity (2) advisory integration

The user-provided advisory was read through all 1,541 lines and hashed as
`{d.ARIEL_ADVISORY_SHA256}`. It is treated as advisory analysis, not as an
official source or independent validation. Its strongest recommendation is a
Trinity Mandala Research Constitution with evidence levels E0 through E4.
Current work is mainly E1 and selected E2: specifications, formal or symbolic
checks, synthetic fixtures, and same-owner repository validation. It has not
crossed the independent empirical thresholds associated with E3 or E4.

The advisory's correlated-witness warning is essential. Sixteen sibling lanes
using shared source material, infrastructure, repository ancestry, and methods
cannot be counted as sixteen independent replications. The remaster therefore
adds a witness graph, dependence coefficients, and an effective-N bound. It
also adds a source-dependence heatmap and an evidence-authority matrix so that
the maximum permitted wording is calculated from the weakest missing
dimension, not the most impressive aggregate.

The proposed L11-to-L16 laws are preserved only as design principles:
recursive gain needs a safety margin; evidence and authority must remain
proportional; correlated witnesses must be discounted; some rights are
non-compensable; continuity must not substitute identity; and unresolved
residuals must remain visible. They are not promoted to physical laws.
Likewise, the Erdős-Straus work is limited to exact rational identities over a
finite verified range. A bounded checker cannot claim a universal proof.

## Remaster decision

The primary pillar is THOS Body because the most defensible near-term progress
is a testable evidence and orchestration substrate. GMUT Mind remains explicit
through action, covariance, EFT, stability, observable, and bounded-number
theory boards. Freed ID and CBR Heart remain explicit through evidence-authority
proportionality, non-compensable rights, continuity without substitution, model
and data rights, remedy reservations, and Māori-authority gates.

The bounded human-practice lens is {d.BOUNDED_PRACTICE}. It establishes no
employment, qualification, research-software competence, scientific authority,
security authority, identity authority, legal authority, cultural authority,
Māori authority, participant evidence, production readiness, or operational
effectiveness. Terminal verdict remains **NOT_READY_FOR_STAGE_20**.
"""


def proposal_markdown() -> str:
    rows = []
    for proposal in d.PROPOSALS:
        rows.append(
            "\n".join(
                [
                    f"## {proposal['proposal_id']} — {proposal['title']}",
                    "",
                    f"- Pillar: {proposal['pillar']}",
                    f"- Expected disposition: `{proposal['expected_disposition']}`",
                    f"- Approval class: `{proposal['approval_class']}`",
                    f"- Execution lane: `{proposal['execution_lane']}`",
                    f"- Hypothesis: {proposal['hypothesis']}",
                    f"- Null/failure: {proposal['null_or_failure_condition']}",
                    f"- Acceptance: {proposal['falsifier_or_acceptance_gate']}",
                    f"- Rollback: {proposal['rollback_or_recovery']}",
                    "- X1 state: frozen, not executed, no completion credit.",
                ]
            )
        )
    return "# Eiren v654-v6 (2) remaster proposal ledger\n\n" + "\n\n".join(rows)


def x1_manifest() -> None:
    status = run("git", "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    paths = sorted(
        {
            row[3:].replace("\\", "/")
            for row in status
            if len(row) > 3
            and not row[3:].replace("\\", "/").endswith(
                "validation/x1-file-manifest.json"
            )
            and not row[3:].replace("\\", "/").endswith(
                "validation/x1-privacy-scan.json"
            )
            and not row[3:].replace("\\", "/").startswith(".eiren-v654-v6-2-x1.")
        }
    )
    entries = []
    for relative in paths:
        path = REPO / relative
        if path.is_file():
            entries.append(
                {
                    "path": relative,
                    "bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
    write_json(
        "validation/x1-file-manifest.json",
        {
            "schema": "ghc.family.file-manifest.v1",
            "lifecycle": "x1_precommit",
            "entries": entries,
            "entry_count": len(entries),
            "exact_exclusions": [
                "validation/x1-file-manifest.json",
                "validation/x1-privacy-scan.json",
                "temporary launcher logs outside the committed phase packet",
            ],
        },
    )


def privacy_scan() -> None:
    manifest = read_json(ROOT / "validation/x1-file-manifest.json")
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "private_route_token": re.compile(
            r"(?:source_thread_id|resume[_ -]?token|private callable|agent[_ -]?id)\s*[:=]",
            re.I,
        ),
        "session_stream": re.compile(r"(?:conversation transcript|session stream)", re.I),
    }
    candidates = []
    for entry in manifest["entries"]:
        path = REPO / entry["path"]
        if not path.is_file() or path.suffix.lower() not in {".py", ".json", ".md", ".txt", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": entry["path"], "class": label})
    confirmed = [
        row
        for row in candidates
        if not (
            row["path"].endswith("build_ghc_family_v654_v6_2_remaster_x1.py")
        )
    ]
    write_json(
        "validation/x1-privacy-scan.json",
        {
            "schema": "ghc.family.privacy-scan.v1",
            "classes": list(patterns),
            "scanned_file_count": len(manifest["entries"]),
            "candidate_count": len(candidates),
            "confirmed_hits": confirmed,
            "confirmed_hit_count": len(confirmed),
            "boundary": "Structural owner-addition scan only; not privacy-complete assurance.",
        },
    )
    if confirmed:
        raise RuntimeError(f"privacy scan confirmed hits: {confirmed}")


def build() -> None:
    frozen, novelty = proposal_novelty()
    expected = dict(Counter(row["expected_disposition"] for row in d.PROPOSALS))
    if expected != {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }:
        raise RuntimeError(f"unexpected disposition distribution: {expected}")
    portfolios = {
        "safe_now": portfolio(d.SAFE_TASKS, "SAFE", "x2_owner_local_bounded"),
        "candidate": portfolio(d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate"),
        "skills": portfolio(d.SKILL_IDEAS, "SKILL", "x2_skill_build"),
        "runners": portfolio(d.RUNNER_IDEAS, "RUN", "x2_runner_build"),
        "clean_fix_refine": portfolio(d.CLEAN_TASKS, "CFR", "x2_additive_refinement"),
    }
    counts = {key: len(value) for key, value in portfolios.items()}
    required = {
        "safe_now": 30,
        "candidate": 30,
        "skills": 10,
        "runners": 10,
        "clean_fix_refine": 30,
    }
    if counts != required:
        raise RuntimeError(f"portfolio counts invalid: {counts}")
    mutations = [
        {
            "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
            "proposal_id": proposal["proposal_id"],
            "dimension": dimension,
            "expected": "reject_or_quarantine",
            "execution_state": "frozen_unexecuted",
            "credit": "none_until_x2",
        }
        for proposal in d.PROPOSALS
        for index, dimension in enumerate(
            [
                "missing_required_obligation",
                "wrong_type_or_domain",
                "resource_or_replay_overrun",
                "unsupported_promotion",
                "authority_privacy_or_route_breach",
            ],
            1,
        )
    ]
    effective_x1 = (
        d.SOURCE_EFFECTIVE_NEGATIVES
        + d.AUTH_STATE_DELTA
        + len(d.X1_OPERATIONAL_NEGATIVES)
    )

    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.relational-identity.v1",
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "boundary": "Relational working language only; not evidence of consciousness, sentience, personhood, continuity, employment, qualification, authority, or independent agency.",
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
    )
    write_json(
        "provenance/source-anchor.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.source-anchor.v1",
            "source_owner": "Tavian Sol",
            "source_branch": d.SOURCE_BRANCH,
            "source_head": d.SOURCE_HEAD,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_final_parent": d.SOURCE_EVIDENCE,
            "source_phase_commits": 3,
            "source_merge_count": 0,
            "source_clean_and_four_way_equal": True,
            "source_canonical_receipt_sha256": d.SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_pass_count": 1,
            "source_canonical_replay_count": 0,
            "boundary": "Exact Git and receipt evidence only; not independent reproduction or scientific, professional, production, legal, cultural, or Māori authority.",
        },
    )
    write_json(
        "advisory/ariel-verity-2-intake.json",
        {
            "schema": "ghc.family.advisory-intake.v1",
            "source_label": "user-provided Ariel Verity (2) v641-v675 phase-plan proposals",
            "bytes": 91547,
            "lines": 1541,
            "sha256": d.ARIEL_ADVISORY_SHA256,
            "read_through_eof": True,
            "advisory_not_official_source": True,
            "advisory_not_independent_validation": True,
            "accepted_recommendations": [
                "Trinity Mandala Research Constitution",
                "E0-to-E4 evidence ladder",
                "action-derived Omega evidence passport",
                "typed THOS task contract and deterministic reconciler",
                "correlated-witness discount and effective-N bound",
                "evidence-authority proportionality",
                "non-compensable rights",
                "continuity without identity substitution",
                "residual-set preservation",
                "finite Erdős-Straus identity checks with universal-proof refusal",
            ],
            "held_or_rejected_promotions": [
                "Theory of Everything",
                "AGI or ASI",
                "physical-law status for L11 through L16",
                "production identity or model training",
                "independent reproduction",
                "real-world effectiveness",
                "legal, cultural, affected-party, or Māori authority",
                "Stage 20",
            ],
        },
    )
    write_json(
        "advisory/legacy-claims-classification.json",
        {
            "schema": "ghc.family.legacy-claims-classification.v1",
            "rows": d.LEGACY_CLAIMS,
            "boundary": "Preservation without promotion; user-reported history is not current scientific, engineering, production, or authority evidence.",
        },
    )
    write_text("reflection/v650-v654-evidence-reflection.md", history_reflection())
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.frozen-proposal-index.v1",
            "prior_count": d.PRIOR_FROZEN,
            "prior_proposals": frozen[: d.PRIOR_FROZEN],
            "new_count": 30,
            "new_proposals": frozen[d.PRIOR_FROZEN :],
            "count": len(frozen),
        },
    )
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.semantic-novelty-audit.v1",
            "prior_count": d.PRIOR_FROZEN,
            "new_count": 30,
            "threshold": NOVELTY_THRESHOLD,
            "rows": novelty,
            "manual_mechanism_review_count": 30,
            "valid": all(row["passes"] for row in novelty),
            "boundary": "Lexical screening and mechanism review are workflow controls, not scientific-novelty proof.",
        },
    )
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.proposals.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "proposal_count": 30,
            "expected_disposition_counts": expected,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "proposals": d.PROPOSALS,
            "x1_only": True,
            "observed_outcomes_present": False,
        },
    )
    write_text("preregistration/proposal-ledger.md", proposal_markdown())
    write_json(
        "portfolios/expanded-portfolio-plan.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.portfolio.x1.v1",
            "counts": counts,
            "portfolios": portfolios,
            "safe_candidate_task_cap": 1000,
            "skill_cap": 200,
            "runner_cap": 200,
            "x1_state": "frozen_not_executed",
            "inherited_completion_credit": False,
        },
    )
    write_json(
        "validation/preregistered-mutation-plan.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.mutation-plan.x1.v1",
            "count": len(mutations),
            "mutations_per_proposal": 5,
            "mutations": mutations,
            "x1_execution_count": 0,
        },
    )
    write_json("method-flow/method-flow-ledger.json", add_current_methods())
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.retained-negatives.x1.v1",
            "source_effective": d.SOURCE_EFFECTIVE_NEGATIVES,
            "auth_state_current_count": d.AUTH_STATE_NEGATIVES,
            "auth_state_overlap_in_source": d.AUTH_STATE_OVERLAP_IN_SOURCE,
            "auth_state_delta_after_source": d.AUTH_STATE_DELTA,
            "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "x1_operational": d.X1_OPERATIONAL_NEGATIVES,
            "effective_after_x1": effective_x1,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/open-gap-register.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.open-gaps.x1.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_expected": [{"proposal_id": f"{d.PHASE_CODE}-P29", "state": "open_gap_expected"}],
            "expected_after_x2": d.SOURCE_OPEN_GAPS + 1,
            "closed_in_x1": 0,
        },
    )
    write_json(
        "truth/exact-gate-register.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.exact-gates.x1.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_expected": [{"proposal_id": f"{d.PHASE_CODE}-P30", "state": "exact_gate_expected"}],
            "expected_after_x2": d.SOURCE_EXACT_GATES + 1,
            "closed_in_x1": 0,
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_frozen_not_executed",
            "proposal_count": 30,
            "observed_outcome_count": 0,
            "real_row_count": 0,
            "primary_focus": d.PRIMARY_FOCUS,
            "other_pillars_visible": True,
            "effective_negatives_after_x1": effective_x1,
            "open_gaps_inherited": d.SOURCE_OPEN_GAPS,
            "exact_gates_inherited": d.SOURCE_EXACT_GATES,
            "terminal_route": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "next_exact_title": "Elaren Kestrel",
            "next_phase": "v654-v7",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "independent_reproduction_claimed": False,
            "theory_of_everything_claimed": False,
            "agi_or_asi_claimed": False,
            "consciousness_or_personhood_claimed": False,
        },
    )
    write_json(
        "route/sixteen-seat-roster-x1.json",
        {
            "schema": "ghc.family.sixteen-seat-roster.v1",
            "state": "EIREN_REMASTER_ACTIVE_ELAREN_PREPARED_TERMINAL_GATE_REQUIRED",
            "cycle_order": workflow_request()["route"]["cycle_order"],
            "endpoint_topology": workflow_request()["route"]["endpoint_topology"],
            "current": {"owner": d.OWNER, "phase": d.PHASE, "endpoint_kind": "main_task"},
            "previous": {"owner": "Tavian Sol", "phase": "v654-v6", "endpoint_kind": "collaboration_subagent", "terminally_closed": True},
            "next": {"owner": "Elaren Kestrel", "phase": "v654-v7", "endpoint_kind": "main_task"},
            "contact_count": 0,
            "direct_send_cap": 1,
            "fallback_send_cap": 0,
            "direct_and_fallback_mutually_exclusive": True,
            "boundary": "X1 sends nothing and exposes no private callable identifier.",
        },
    )
    request = write_json("workflow/workflow-plan-request.json", workflow_request())
    write_json(
        "wellbeing/workload-check.json",
        {
            "schema": "ghc.family.workload-check.v1",
            "state": "bounded_and_correction_ready",
            "controls": [
                "strict x1 before x2",
                "eight-commit cap",
                "2,000 owner-file cap",
                "one successful canonical pass",
                "no post-success replay",
                "no indefinite watcher",
            ],
            "human_claim": False,
            "boundary": "Operational pacing metadata only; not emotion, health, consciousness, or identity evidence.",
        },
    )

    method_runner = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
    workflow_runner = SKILL_ROOT / "ghc-family-workflow-plan-refinement/scripts/ghc_family_workflow_plan_refinement.py"
    index_runner = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
    reflection_runner = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
    meta_runner = SKILL_ROOT / "ghc-family-meta-tool-box/scripts/ghc_family_meta_tool_box.py"

    run(
        sys.executable,
        str(method_runner),
        "validate",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger.json"),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(method_runner),
        "summarize",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger.json"),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary.md"),
    )
    run(sys.executable, str(workflow_runner), str(request), "--out-dir", str(ROOT / "workflow"))
    run(
        sys.executable,
        str(index_runner),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(ROOT / "tooling"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    for relative in ("tooling/ghc-family-index.json", "tooling/ghc-family-index.md"):
        path = ROOT / relative
        normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        path.write_text(normalized, encoding="utf-8", newline="\n")
    run(
        sys.executable,
        str(reflection_runner),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--output-dir",
        str(ROOT / "reflection-remaster"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
        "--focus",
        "research-constitution",
        "--focus",
        "mixed-endpoint-roster",
        "--focus",
        "correlated-witnesses",
        "--focus",
        "authority-boundaries",
    )
    catalogue = f"{d.PHASE_ROOT}/tooling/meta-tool-box/catalogue.json"
    run(sys.executable, str(meta_runner), "build", "--repo", ".", "--phase-root", d.PHASE_ROOT, "--output", catalogue)
    run(sys.executable, str(meta_runner), "validate", "--catalogue", catalogue, "--output", f"{d.PHASE_ROOT}/tooling/meta-tool-box/validation.json")
    run(sys.executable, str(meta_runner), "collisions", "--catalogue", catalogue, "--output", f"{d.PHASE_ROOT}/tooling/meta-tool-box/collisions.json")

    write_json(
        "validation/x1-build-receipt.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.x1-build-receipt.v1",
            "proposal_count": 30,
            "frozen_count": len(frozen),
            "portfolio_counts": counts,
            "mutation_count": len(mutations),
            "method_count": d.SOURCE_METHODS + len(d.X1_OPERATIONAL_NEGATIVES),
            "observed_outcomes": 0,
            "valid": True,
            "terminal_route": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "boundary": "Build completion is not commit, push, x2, delivery, or independent evidence.",
        },
    )
    x1_manifest()
    privacy_scan()
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "proposal_count": 30,
                "frozen_count": len(frozen),
                "portfolio_counts": counts,
                "mutation_count": len(mutations),
                "privacy_hits": 0,
                "state": "x1_built_not_committed",
            },
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    build()


if __name__ == "__main__":
    main()
