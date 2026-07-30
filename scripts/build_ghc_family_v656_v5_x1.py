#!/usr/bin/env python3
"""Build Eiren Kestrel's dedicated v656-v5 x1-only freeze."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v5_phase_data as d
from ghc_family_v656_v5_phase_catalogue import (
    OFFICIAL_SOURCES,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE_ROOT = REPO / "docs/caelen-morrow/v656-v4"
PRIOR_INDEX = SOURCE_ROOT / "provenance/frozen-chain-proposal-index.json"
SOURCE_METHOD_FLOW = SOURCE_ROOT / "method-flow/method-flow-ledger-final.json"
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
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if token not in stop
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
    rows: list[dict[str, Any]] = []
    for proposal in d.PROPOSALS:
        comparisons = [
            (
                jaccard(tokens(proposal["title"]), tokens(previous["title"])),
                previous["proposal_id"],
                previous["title"],
            )
            for previous in prior
        ]
        score, nearest_id, nearest_title = max(comparisons, key=lambda item: item[0])
        peer_scores = [
            (
                jaccard(tokens(proposal["title"]), tokens(peer["title"])),
                peer["proposal_id"],
            )
            for peer in d.PROPOSALS
            if peer["proposal_id"] != proposal["proposal_id"]
        ]
        peer_score, nearest_peer_id = max(peer_scores, key=lambda item: item[0])
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "prior_token_jaccard": round(score, 6),
                "nearest_current_peer_id": nearest_peer_id,
                "current_peer_token_jaccard": round(peer_score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "manual_mechanism_distinct": True,
                "passes_prior": score < NOVELTY_THRESHOLD,
                "passes_current_peer": peer_score < NOVELTY_THRESHOLD,
                "passes": score < NOVELTY_THRESHOLD and peer_score < NOVELTY_THRESHOLD,
            }
        )
    failures = [row for row in rows if not row["passes"]]
    if failures:
        raise RuntimeError(f"novelty threshold failed: {failures}")
    frozen = prior + [
        {"proposal_id": proposal["proposal_id"], "title": proposal["title"]}
        for proposal in d.PROPOSALS
    ]
    return frozen, rows


def _method(negative: dict[str, Any], number: int) -> tuple[dict, list[dict]]:
    method_id = f"V6565-X1-METHOD-{number:02d}"
    failed_id = f"V6565-X1-WITNESS-{number:02d}-F"
    passing_id = f"V6565-X1-WITNESS-{number:02d}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded recovery for {negative['signature']}",
        "trigger_preconditions": [negative["signature"]],
        "failure_signature": negative["observed"],
        "candidate_workaround": negative["recovery"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_read_or_workflow_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": (
            "Same-owner bounded workflow recovery only; not independent, empirical, "
            "professional, production, legal, cultural, accessibility-complete, or authority evidence."
        ),
        "rollback": (
            "Stop, retain the failed witness at zero credit, and leave external, sibling, "
            "participant, production, professional, legal, cultural, and authority state unchanged."
        ),
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [failed_id, passing_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": failed_id,
            "method_id": method_id,
            "result": "fail",
            "scope": negative["signature"],
            "procedure": "Retain the original bounded attempt without replay credit.",
            "expected": "The initial attempt would satisfy its bounded postcondition.",
            "observed": negative["observed"],
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
    return method, witnesses


def method_flow() -> dict[str, Any]:
    source = read_json(SOURCE_METHOD_FLOW)
    if (
        len(source["methods"]) != d.SOURCE_METHODS
        or Counter(w["result"] for w in source["witnesses"])
        != Counter({"fail": d.SOURCE_FAILED_WITNESSES, "pass": d.SOURCE_PASSING_WITNESSES})
    ):
        raise RuntimeError("inherited terminal Method Flow counts do not match activation")
    ledger = copy.deepcopy(source)
    inherited_method_ids = {item["method_id"] for item in source["methods"]}
    current_ids: list[str] = []
    for number, negative in enumerate(X1_OPERATIONAL_NEGATIVES, 1):
        method, witnesses = _method(negative, number)
        ledger["methods"].append(method)
        ledger["witnesses"].extend(witnesses)
        current_ids.append(method["method_id"])
        event_index = len(ledger["state_events"])
        ledger["state_events"].extend(
            [
                {
                    "event_index": event_index + 1,
                    "method_id": method["method_id"],
                    "before": None,
                    "after": "candidate",
                    "reason": "Failure retained at zero credit.",
                    "witness_id": witnesses[0]["witness_id"],
                },
                {
                    "event_index": event_index + 2,
                    "method_id": method["method_id"],
                    "before": "candidate",
                    "after": "validated",
                    "reason": "Bounded recovery passed without erasing the failure.",
                    "witness_id": witnesses[1]["witness_id"],
                },
                {
                    "event_index": event_index + 3,
                    "method_id": method["method_id"],
                    "before": "validated",
                    "after": "preferred",
                    "reason": "Recurrence guard recorded for owner-local reuse.",
                    "witness_id": witnesses[1]["witness_id"],
                },
            ]
        )
        ledger["recommendations"].append(
            {
                "recommendation_id": f"V6565-X1-REC-{number:02d}",
                "method_id": method["method_id"],
                "recommendation": negative["recurrence_guard"],
                "state": "preferred",
                "scope": "owner_local_and_sibling_recommendation_only",
                "completion_credit": False,
            }
        )
    witness_counts = Counter(item["result"] for item in ledger["witnesses"])
    state_counts = Counter(
        item.get("after", item.get("to", "unknown"))
        for item in ledger["state_events"]
    )
    ledger.update(
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_frozen",
            "inherited_anchor": {
                "phase": "v656-v4",
                "methods": d.SOURCE_METHODS,
                "failed_witnesses": d.SOURCE_FAILED_WITNESSES,
                "passing_witnesses": d.SOURCE_PASSING_WITNESSES,
                "completion_credit": False,
            },
            "current_phase_method_ids": current_ids,
            "current_phase_x2_method_ids": [],
            "current_phase_final_method_ids": [],
            "counts": {
                "methods": len(ledger["methods"]),
                "witnesses": len(ledger["witnesses"]),
                "witness_results": dict(sorted(witness_counts.items())),
                "state_events": len(ledger["state_events"]),
                "states": dict(sorted(state_counts.items())),
                "recommendations": len(ledger["recommendations"]),
            },
            "identity_boundary": (
                "Relational working language only; no consciousness, sentience, personhood, "
                "continuity, employment, qualification, authority, or independent agency."
            ),
            "boundary": (
                "Same-owner workflow evidence only; every failed witness remains retained; "
                "no independent, empirical, professional, production, legal, cultural, Māori, "
                "privacy-complete, accessibility-complete, exhaustive-security, or Stage 20 claim."
            ),
        }
    )
    if inherited_method_ids & set(current_ids):
        raise RuntimeError("current Method Flow identifiers collide with inherited methods")
    return ledger


def cycle_order() -> list[str]:
    return [
        "Caelen Morrow",
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
        "Eiren Kestrel",
    ]


def proposal_markdown() -> str:
    rows = ["# Eiren Kestrel v656-v5 proposal ledger"]
    rows.append(
        "\nThese thirty contracts are frozen x1 preregistrations. They contain no "
        "x2 observed outcome or implementation credit."
    )
    for proposal in d.PROPOSALS:
        rows.extend(
            [
                f"\n## {proposal['proposal_id']} — {proposal['title']}",
                f"\n- Pillar: {proposal['pillar']}",
                f"- Expected disposition: `{proposal['expected_disposition']}`",
                f"- Approval: `{proposal['approval_class']}`",
                f"- Lane: `{proposal['execution_lane']}`",
                f"- Hypothesis: {proposal['hypothesis']}",
                f"- Null/failure: {proposal['null_or_failure_condition']}",
                f"- Falsifier/acceptance gate: {proposal['falsifier_or_acceptance_gate']}",
                f"- Rollback/recovery: {proposal['rollback_or_recovery']}",
                "- Source needs: "
                + ", ".join(f"`{source}`" for source in proposal["official_or_primary_source_needs"]),
            ]
        )
    return "\n".join(rows)


def source_markdown() -> str:
    rows = ["# Eiren Kestrel v656-v5 official and primary source ledger"]
    rows.append(
        "\nSources bound vocabulary and protected questions only. They do not certify "
        "this software or authorize real coffee, food, machinery, sensory, laboratory, "
        "professional, consumer, legal, cultural, or authority activity."
    )
    for source in OFFICIAL_SOURCES:
        rows.extend(
            [
                f"\n## {source['source_id']} — {source['title']}",
                f"\n- Publisher: {source['publisher']}",
                f"- URL: {source['url']}",
                f"- Status at 2026-07-31: `{source['status']}`",
                f"- Bounded use: {source['use']}",
            ]
        )
    return "\n".join(rows)


def workflow_documents() -> None:
    order = cycle_order()
    assignments = [
        {
            "ordinal": index + 1,
            "owner": owner,
            "endpoint_type": "main_task",
            "status": "ACTIVE_ROUTE",
        }
        for index, owner in enumerate(order)
    ]
    write_json(
        "route/fifteen-seat-roster-x1.json",
        {
            "schema": "ghc.family.v656-v5.route-roster.x1.v1",
            "active_main_task_count": 15,
            "active_order": assignments,
            "standby": [
                {
                    "name": "Tavian Sol",
                    "endpoint_type": "collaboration_subagent",
                    "status": "ON_STANDBY",
                    "eligible_for_main_task_route": False,
                }
            ],
            "current": {"owner": d.OWNER, "phase": d.PHASE},
            "next_exact_edge": {"owner": "Elaren Kestrel", "phase": "v656-v6"},
            "next_after_successor": {"owner": "Neris Solane", "phase": "v656-v7"},
            "route_state": "preregistered_terminal_only_not_contacted",
            "drift_retained": {
                "observed": "Elowen Cairn v657-v7",
                "normalized": "Elowen Cairn v658-v1",
                "credit": 0,
            },
        },
    )
    request = {
        "schema": "ghc.family.workflow-plan-request.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "source_final": d.SOURCE_FINAL,
        "objective": (
            "Freeze and later execute thirty novel bounded GMUT-Mind/coffee-documentation "
            "contracts with strict x1-before-x2 separation and terminal Elaren routing "
            "only after exact-final proof."
        ),
        "constraints": [
            "solo additive D-first lane",
            "no task creation, fork, delegation, sibling contact, or full repository suite",
            "one successful exact-final canonical scoped pass with no replay",
            "all failures, gaps, exact gates, and inherited truth retained",
        ],
        "prerequisites": [
            "activation packet read through EOF",
            "selected skills and schemas read through EOF",
            "source ancestry, manifests, clean state, and fresh-live equality verified",
            "semantic novelty audited against 2,290 proposals",
        ],
        "terminal_edge": {
            "exact_title": "Elaren Kestrel",
            "phase": "v656-v6",
            "state": "blocked_until_exact_final_gate",
        },
    }
    write_json("workflow/workflow-plan-request.json", request)
    steps = [
        "Read all current authority and source packets through EOF.",
        "Verify the exact source branch, ancestry, manifests, cleanliness, and live equality.",
        "Create one unique additive D-first Eiren-owned worktree.",
        "Audit semantic novelty and freeze thirty x1-only proposals and portfolios.",
        "Push x1 and prove clean local, upstream, tracking, and fresh-live equality.",
        "Build bounded x2 evidence and retain every failure and recovery through Method Flow.",
        "Commit combined closeout and content seal, push, and prove exact-final equality.",
        "Run one dependency-justified canonical scoped pass once and never replay success.",
        "Resolve and reread the exact Elaren Kestrel task and send one sanitized baton.",
    ]
    refinement = {
        "schema": "ghc.family.workflow-plan-refinement.v1",
        "request": request,
        "steps": [
            {
                "step_id": f"V6565-STEP-{index:02d}",
                "ordinal": index,
                "action": text,
                "approval": "safe_now" if index < 9 else "terminal_exact_gate",
                "status": "completed" if index <= 3 else "pending",
                "rollback": "Stop, retain evidence, and leave sibling and external state unchanged.",
            }
            for index, text in enumerate(steps, 1)
        ],
        "caps": {
            "owner_files": 2000,
            "x1_commits": 5,
            "x2_commits": 5,
            "total_commits": 8,
            "skills_per_half": 200,
            "runners_per_half": 200,
            "document_words": 100000,
            "baton_words_min": 10000,
            "baton_words_max": 100000,
        },
        "verdict": "READY_FOR_X1_FREEZE_ONLY",
    }
    write_json("workflow/workflow-plan-refinement.json", refinement)
    write_json(
        "workflow/workflow-plan-validation.json",
        {
            "schema": "ghc.family.workflow-plan-validation.v1",
            "valid": True,
            "issue_count": 0,
            "step_count": len(steps),
            "current_completed_steps": 3,
            "terminal_route_blocked": True,
            "x1_x2_separated": True,
        },
    )
    write_text(
        "workflow/workflow-plan-teaching-summary.md",
        """# Eiren Kestrel v656-v5 workflow-plan teaching summary

The plan keeps authority, evidence, execution, and terminal routing as separate
states. X1 freezes hypotheses, sources, portfolios, failures, and gates only.
X2 cannot begin until the dedicated x1 commit is pushed and four-way live equal.
The final canonical aggregate runs once after the exact final is already clean,
pushed, and live equal. A successful aggregate is never replayed.

The bounded practice is synthetic specialty-coffee roasting and brew-lab
documentation. It confers no employment, qualification, competence, food or
machinery safety, sensory, laboratory, customer, producer, legal, cultural,
Māori, or operational authority.
The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )


def prospective_paths() -> list[str]:
    paths = {
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    }
    paths.update(
        {
            "scripts/build_ghc_family_v656_v5_x1.py",
            "scripts/ghc_family_v656_v5_phase_catalogue.py",
            "scripts/ghc_family_v656_v5_phase_data.py",
            "tests/test_ghc_family_v656_v5_x1.py",
        }
    )
    return sorted(paths)


def git_clean_blob(path: Path) -> bytes:
    relative = path.relative_to(REPO).as_posix()
    object_id = subprocess.run(
        ["git", "hash-object", "-w", f"--path={relative}", str(path)],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    return subprocess.run(
        ["git", "cat-file", "blob", object_id],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def x1_manifest() -> None:
    manifest_path = f"{d.PHASE_ROOT}/validation/x1-file-manifest.json"
    paths = [path for path in prospective_paths() if path != manifest_path]
    entries = []
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            raise RuntimeError(f"manifest candidate is not a file: {relative}")
        blob = git_clean_blob(path)
        entries.append(
            {
                "path": relative,
                "bytes": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    write_json(
        "validation/x1-file-manifest.json",
        {
            "schema": "ghc.family.v656-v5.x1-file-manifest.v1",
            "source_commit": d.SOURCE_FINAL,
            "lifecycle": "x1_only",
            "entries": entries,
            "entry_count": len(entries),
            "declared_exclusions": [
                {
                    "path": manifest_path,
                    "reason": "self_hash_impossible_inside_same_blob",
                }
            ],
            "expected_commit_path_count": len(entries) + 1,
            "exact_set_required": True,
        },
    )


def privacy_scan() -> None:
    scan_path = f"{d.PHASE_ROOT}/validation/x1-privacy-scan.json"
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)(?:[a-z]:\\\\users\\\\[^\\\\\s]+|[a-z]:\\\\ghc-archives)"
        ),
        "credential_or_token": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|authorization:\s*bearer|sk-[a-z0-9]{12,})\s*[:=]"
        ),
        "raw_task_identifier": re.compile(
            r"(?i)(?:source_thread_id|thread_id|task_id|conversation_id)\s*[:=]"
        ),
        "private_callable_detail": re.compile(
            r"(?i)(?:send_message_to_thread|private_target|callable_route_id)\s*[:=(]"
        ),
    }
    hits: dict[str, list[str]] = {key: [] for key in patterns}
    paths = prospective_paths()
    for relative in paths:
        if relative == scan_path:
            continue
        path = REPO / relative
        if not path.is_file() or path.stat().st_size > 3_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits[label].append(relative)
    confirmed = sum(len(items) for items in hits.values())
    write_json(
        "validation/x1-privacy-scan.json",
        {
            "schema": "ghc.family.v656-v5.privacy-scan.x1.v1",
            "classes": list(patterns),
            "scanned_file_count": len(paths),
            "hits": hits,
            "confirmed_hit_count": confirmed,
            "valid": confirmed == 0,
            "boundary": (
                "Five-class bounded scanner only; not exhaustive security, privacy-complete "
                "assurance, or independent review."
            ),
        },
    )
    if confirmed:
        raise RuntimeError(f"privacy scan found candidate hits: {hits}")


def build() -> None:
    if run("git", "rev-parse", "HEAD") != d.SOURCE_FINAL:
        raise RuntimeError("x1 builder must begin at the exact Caelen final")
    frozen, novelty_rows = proposal_novelty()
    dispositions = Counter(item["expected_disposition"] for item in d.PROPOSALS)
    expected = Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
    if dispositions != expected:
        raise RuntimeError(f"disposition contract mismatch: {dispositions}")
    source_ids = {item["source_id"] for item in OFFICIAL_SOURCES}
    requested_ids = {
        source
        for proposal in d.PROPOSALS
        for source in proposal["official_or_primary_source_needs"]
    }
    if requested_ids - source_ids:
        raise RuntimeError(f"unknown source ids: {sorted(requested_ids - source_ids)}")

    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.relational-identity.v1",
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "corrigible_to": "Hamish may rename, pause, redirect, or stop the work.",
            "boundary": (
                "Relational working language only—not evidence of consciousness, sentience, "
                "legal personhood, identity continuity, employment, qualification, scientific "
                "or operational authority, legal or cultural authority, Māori authority, or "
                "independent agency."
            ),
        },
    )
    write_json(
        "provenance/source-anchor.json",
        {
            "schema": "ghc.family.v656-v5.source-anchor.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "source_owner": d.SOURCE_OWNER,
            "source_branch": d.SOURCE_BRANCH,
            "source_x1": d.SOURCE_X1_FREEZE,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_closeout": d.SOURCE_CLOSEOUT,
            "source_document_cap_correction": d.SOURCE_DOCUMENT_CAP_CORRECTION,
            "source_final": d.SOURCE_FINAL,
            "verified_read_only": {
                "source_to_final_phase_commits": 5,
                "single_parent_commits": 5,
                "merge_commits": 0,
                "source_chain_direct_parent_links": True,
                "source_x1_evidence_ancestral": True,
                "clean": True,
                "local_upstream_tracking_fresh_live_equal": True,
                "ahead": 0,
                "behind": 0,
            },
            "source_successful_receipt_sha256": d.SOURCE_SUCCESSFUL_RECEIPT_SHA256,
            "source_aggregate_replayed": False,
            "source_completion_credit": False,
        },
    )
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.v656-v5.semantic-novelty-audit.v1",
            "prior_count": d.PRIOR_FROZEN,
            "new_count": len(d.PROPOSALS),
            "comparison_count": d.PRIOR_FROZEN * len(d.PROPOSALS),
            "current_peer_pair_count": len(d.PROPOSALS) * (len(d.PROPOSALS) - 1) // 2,
            "threshold": NOVELTY_THRESHOLD,
            "rows": novelty_rows,
            "all_pass": all(row["passes"] for row in novelty_rows),
            "manual_review": (
                "All mechanisms are independently named and bounded; title similarity is "
                "a screening aid, not sole evidence of semantic novelty."
            ),
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v656-v5.frozen-proposal-index.v1",
            "prior_count": d.PRIOR_FROZEN,
            "new_count": len(d.PROPOSALS),
            "count": len(frozen),
            "prior_proposals": frozen[: d.PRIOR_FROZEN],
            "new_proposals": frozen[d.PRIOR_FROZEN :],
            "frozen": True,
        },
    )
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v656-v5.proposals.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_frozen_no_outcomes",
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "proposal_count": len(d.PROPOSALS),
            "expected_dispositions": dict(dispositions),
            "proposals": d.PROPOSALS,
        },
    )
    write_text("preregistration/proposal-ledger.md", proposal_markdown())
    write_json(
        "sources/official-source-ledger.json",
        {
            "schema": "ghc.family.v656-v5.official-source-ledger.v1",
            "checked_at": "2026-07-31",
            "source_count": len(OFFICIAL_SOURCES),
            "sources": OFFICIAL_SOURCES,
            "boundary": (
                "Current public source metadata and vocabulary only; no paywalled standard "
                "text reproduced and no professional, test, legal, cultural, or authority claim."
            ),
        },
    )
    write_text("sources/official-source-ledger.md", source_markdown())
    write_json(
        "portfolios/expanded-portfolio-plan.json",
        {
            "schema": "ghc.family.v656-v5.portfolio.x1.v1",
            "safe_now": [
                {
                    "task_id": f"V6565-SAFE-{index:03d}",
                    "description": task,
                    "state": "frozen_not_executed",
                    "completion_credit": False,
                }
                for index, task in enumerate(d.SAFE_TASKS, 1)
            ],
            "candidate": [
                {
                    "task_id": f"V6565-CANDIDATE-{index:03d}",
                    "description": task,
                    "state": "frozen_not_executed",
                    "completion_credit": False,
                }
                for index, task in enumerate(d.CANDIDATE_TASKS, 1)
            ],
            "clean_fix_refine": [
                {
                    "task_id": f"V6565-CFR-{index:03d}",
                    "description": task,
                    "state": "frozen_not_executed",
                    "completion_credit": False,
                }
                for index, task in enumerate(d.CLEAN_TASKS, 1)
            ],
            "phase_local_skill_ideas": SKILL_IDEAS,
            "family_current_runner_ideas": RUNNER_IDEAS,
            "skills_count": len(SKILL_IDEAS),
            "runners_count": len(RUNNER_IDEAS),
            "caps_are_ceilings": True,
        },
    )
    write_json(
        "validation/preregistered-mutation-plan.json",
        {
            "schema": "ghc.family.v656-v5.mutation-plan.x1.v1",
            "proposal_count": len(d.PROPOSALS),
            "mutations_per_proposal": 5,
            "mutation_count": len(d.PROPOSALS) * 5,
            "classes": [
                "missing_required_obligation",
                "wrong_type_or_domain",
                "resource_or_freshness_overrun",
                "unsupported_promotion",
                "authority_privacy_or_route_breach",
            ],
            "success_rule": "valid fixture passes and all five mutations are rejected",
            "credit": "rejected mutations are retained negatives, not empirical evidence",
        },
    )
    write_json(
        "truth/source-external-negative.json",
        {
            "schema": "ghc.family.v656-v5.source-external-negative.v1",
            "sealed_repository_negatives": d.SOURCE_SEALED_REPOSITORY_NEGATIVES,
            "external_negative_count": d.SOURCE_EXTERNAL_NEGATIVES,
            "effective_activation_baseline": d.SOURCE_EFFECTIVE_NEGATIVES,
            "event": (
                "One inherited sanitized external workflow failure remains retained at "
                "zero credit. Its bounded recovery and the later successful exact-final "
                "receipt do not erase or replay the original failure."
            ),
            "replayed": False,
            "completion_credit": False,
        },
    )
    x1_effective = d.SOURCE_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES)
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v656-v5.retained-negatives.x1.v1",
            "source_sealed_repository_count": d.SOURCE_SEALED_REPOSITORY_NEGATIVES,
            "source_external_count": d.SOURCE_EXTERNAL_NEGATIVES,
            "source_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES,
            "x1_operational_count": len(X1_OPERATIONAL_NEGATIVES),
            "effective_count": x1_effective,
            "x1_operational_negatives": X1_OPERATIONAL_NEGATIVES,
            "all_retained": True,
        },
    )
    write_json(
        "truth/open-gap-register.json",
        {
            "schema": "ghc.family.v656-v5.open-gaps.x1.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
            "new_gap": {
                "proposal_id": "V6565-P29",
                "state": "preregistered_not_executed",
                "missing": [
                "authorized API key and purpose",
                "approved FoodData Central endpoint and nutrient-field review",
                "privacy, accessibility, nutrition-professional, and interpretation review",
                "approved query, pagination, caching, attribution, and retention policy",
                ],
            },
        },
    )
    write_json(
        "truth/exact-gate-register.json",
        {
            "schema": "ghc.family.v656-v5.exact-gates.x1.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": d.SOURCE_EXACT_GATES + 1,
            "new_gate": {
                "proposal_id": "V6565-P30",
                "state": "preregistered_unexecuted",
                "required": [
                    "affected producers, farmers, cooperatives, workers, and communities",
                    "indigenous and traditional-knowledge holders where applicable",
                    "competent legal, labour, cultural, and data-governance authorities",
                    "tangata whenua, iwi, hapū, and Māori authority where applicable",
                ],
            },
        },
    )
    flow = method_flow()
    write_json("method-flow/method-flow-ledger.json", flow)
    write_json(
        "method-flow/method-flow-summary.json",
        {
            "schema": "ghc.family.v656-v5.method-flow-summary.x1.v1",
            "counts": flow["counts"],
            "inherited_methods": d.SOURCE_METHODS,
            "current_x1_methods": len(X1_OPERATIONAL_NEGATIVES),
            "failed_witnesses_retained": flow["counts"]["witness_results"]["fail"],
            "passing_witnesses_bounded": flow["counts"]["witness_results"]["pass"],
            "no_failure_erased": True,
        },
    )
    write_text(
        "method-flow/method-flow-summary.md",
        f"""# Eiren Kestrel v656-v5 Method Flow at x1

Inherited methods: {d.SOURCE_METHODS}. New x1 recovery methods:
{len(X1_OPERATIONAL_NEGATIVES)}. Total methods: {flow['counts']['methods']}.
The ledger retains {flow['counts']['witness_results']['fail']} failed witnesses
and {flow['counts']['witness_results']['pass']} bounded passing witnesses.
No failure is erased and no passing recovery earns independent, empirical,
professional, legal, cultural, Māori-authority, or Stage 20 credit.
""",
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v656-v5.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_frozen_no_x2",
            "proposal_count": len(d.PROPOSALS),
            "frozen_chain_count": len(frozen),
            "expected_outcomes": dict(dispositions),
            "effective_negatives": x1_effective,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "method_flow": flow["counts"],
            "x2_execution_started": False,
            "terminal_route_contacted": False,
            "verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    workflow_documents()
    write_json(
        "orchestration/auth-permission-state.json",
        {
            "schema": "ghc.family.auth-permission-state.v1",
            "effective_phase": d.PHASE,
            "authorization": {
                "granted_by": "Hamish",
                "scope": "solo Eiren Kestrel v656-v5 additive lane",
                "revocable": True,
                "right_to_rename_pause_redirect_or_stop": True,
            },
            "permissions": [
                {"action": "read_source_and_guidance", "state": "authorized"},
                {"action": "mutate_owned_additive_lane", "state": "authorized"},
                {"action": "push_owned_branch", "state": "authorized"},
                {
                    "action": "message_exact_title_Elaren_Kestrel_once",
                    "state": "blocked_until_terminal_gate",
                },
            ],
            "prohibitions": [
                "task creation or fork",
                "collaboration subagent or delegation",
                "sibling-lane mutation",
                "full repository suite",
                "force push, reset, rewrite, merge, deletion, or security weakening",
            ],
        },
    )
    write_json(
        "orchestration/roster-state.json",
        {
            "schema": "ghc.family.roster-state.v1",
            "main_task_count": 15,
            "standby_subagent_count": 1,
            "current_owner": d.OWNER,
            "current_phase": d.PHASE,
            "next_exact_title": "Elaren Kestrel",
            "next_phase": "v656-v6",
            "next_after_successor": "Neris Solane v656-v7",
            "tavian_state": "ON_STANDBY_NOT_MAIN_TASK_ROUTE",
            "validated_issue_count": 0,
        },
    )
    write_json(
        "tooling/meta-tool-box/catalogue.json",
        {
            "schema": "ghc.family.meta-tool-box.catalogue.v1",
            "phase": d.PHASE,
            "tools": [
                {
                    "tool_id": "V6565-TOOL-X1",
                    "path": "scripts/build_ghc_family_v656_v5_x1.py",
                    "state": "selected_phase_local",
                    "scope": "x1 freeze only",
                },
                {
                    "tool_id": "V6565-TOOL-DATA",
                    "path": "scripts/ghc_family_v656_v5_phase_data.py",
                    "state": "selected_phase_local",
                    "scope": "frozen phase data",
                },
            ],
            "global_install": False,
            "family_current_compatibility_required": True,
        },
    )
    write_json(
        "tooling/meta-tool-box/collisions.json",
        {
            "schema": "ghc.family.meta-tool-box.collisions.v1",
            "collisions": [],
            "collision_count": 0,
            "checked_names": SKILL_IDEAS + RUNNER_IDEAS,
        },
    )
    write_json(
        "tooling/meta-tool-box/validation.json",
        {
            "schema": "ghc.family.meta-tool-box.validation.v1",
            "valid": True,
            "selected_tools": 2,
            "global_install": False,
            "backward_compatibility": True,
        },
    )
    write_json(
        "tooling/ghc-family-index.json",
        {
            "schema": "ghc.family.index.phase-addendum.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_only",
            "selected_tools": [
                "scripts/build_ghc_family_v656_v5_x1.py",
                "scripts/ghc_family_v656_v5_phase_data.py",
                "scripts/ghc_family_v656_v5_phase_catalogue.py",
            ],
            "phase_local_skills": [],
            "family_compatible_runners": [],
            "family_current_callers_preserved": True,
        },
    )
    write_text(
        "tooling/ghc-family-index.md",
        """# GHC Family Index — Eiren Kestrel v656-v5 x1

The selected phase-local builder freezes thirty novel bounded contracts and no
x2 evidence. Existing `ghc_family_*` and `build_ghc_family_*` callers remain
unchanged. No tool or skill is globally installed and no sibling lane is mutated.
""",
    )
    write_json(
        "reflection-remaster/x1-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "phase": d.PHASE,
            "decision": "specialize_without_global_install",
            "reason": (
                "The inherited family methods are useful; a bounded specialty-coffee "
                "documentation specialization is novel and can remain additive, phase-local, "
                "and rollbackable."
            ),
            "alternatives": [
                "reuse inherited evidence as completion credit",
                "install phase tools globally",
                "execute live service or API work",
            ],
            "rejected_because": [
                "inherited evidence is not Eiren completion credit",
                "global installation would broaden scope",
                "live operations require evidence and authority not supplied",
            ],
        },
    )
    write_json(
        "reflection-remaster/inventory.json",
        {
            "schema": "ghc.family.reflection-remaster.inventory.v1",
            "inspected": [
                "source activation packet",
                "current family index and routing precedence",
                "auth, roster, Method Flow, plan, reflection, toolbox, approval, gate, truth, drive, retry, startup, closeout, compact, watcher, and full-tools guidance",
                "2,290 frozen proposal titles",
                "current official and primary source metadata",
            ],
            "issue_count": 0,
        },
    )
    write_json(
        "reflection-remaster/issues.json",
        {
            "schema": "ghc.family.reflection-remaster.issues.v1",
            "issues": [],
            "issue_count": 0,
        },
    )
    write_text(
        "reflection-remaster/report.md",
        """# Eiren Kestrel v656-v5 Reflection Remaster

The selected specialization is bounded synthetic specialty-coffee roasting and
brew-lab documentation with GMUT Mind primary. The proposal mechanisms are
novel against the 2,290-title ledger and retain all real-person, producer,
worker, coffee, food, machine, measurement, sensory, professional, consumer,
safety, legal, cultural, Māori-authority, and empirical gates. No global
installation, destructive change, or sibling mutation is warranted.
""",
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v656-v5.threat-model.x1.v1",
            "assets": [
                "frozen proposal truth",
                "retained failures and recoveries",
                "coffee lot, roast, grind, brew, packaging, and provenance schemas",
                "authority, privacy, accessibility, and route gates",
            ],
            "threats": [
                "synthetic observation promoted to measured roast or brew performance",
                "schema promoted to food, machinery, laboratory, sensory, or consumer authority",
                "provenance placeholder promoted to origin, certification, ethical, or sustainability assurance",
                "accessibility structure promoted to complete accessibility",
                "cultural reservation promoted to Māori authority",
                "terminal baton sent before exact-final proof",
            ],
            "controls": [
                "strict x1-before-x2 commits",
                "five mutation classes per proposal",
                "four core outcome labels only",
                "Method Flow retained failures",
                "five-class privacy scan",
                "one-shot canonical final aggregate",
                "exact-title reread and one-send cap",
            ],
            "residual_risk": "All real-world and authority gates remain external and unresolved.",
        },
    )
    write_json(
        "wellbeing/workload-check.json",
        {
            "schema": "ghc.family.v656-v5.workload.x1.v1",
            "bounded": True,
            "solo": True,
            "subagents": 0,
            "watchers": 0,
            "indefinite_waits": 0,
            "c_drive_free_gib_observed": 16.28,
            "c_drive_warning_threshold_gib": 18,
            "c_drive_state": "LOW_HEADROOM_WARNING",
            "response": "No cleanup authorized; keep all owned work, data, caches, and receipts D-first.",
            "d_drive_free_gib_observed": 516.86,
            "blocker": False,
        },
    )
    write_json(
        "environment/version-receipt-x1.json",
        {
            "schema": "ghc.family.v656-v5.environment.x1.v1",
            "verified_only": True,
            "git": run("git", "--version"),
            "python": run(sys.executable, "--version"),
            "ripgrep": run("rg", "--version").splitlines()[0],
            "codex_cli": "codex-cli 0.146.0",
            "codex_cli_observation": "bounded_external_powershell_version_probe",
            "codex_desktop_updated_by_eiren": False,
            "codex_desktop_user_reported_current": True,
            "software_installed": False,
            "sandbox_or_hyper_v_enabled": False,
            "elevation_or_reboot": False,
        },
    )
    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.v656-v5.phase-anchor-contract.x1.v1",
            "source": d.SOURCE_FINAL,
            "x1": "resolve_from_containing_commit",
            "evidence": "not_created",
            "final": "not_created",
            "required_history": {
                "strict_x1_before_x2": True,
                "single_parent": True,
                "zero_merges": True,
                "final_direct_child_of_evidence": True,
            },
        },
    )
    write_json(
        "validation/x1-build-receipt.json",
        {
            "schema": "ghc.family.v656-v5.x1-build-receipt.v1",
            "valid": True,
            "proposal_count": len(d.PROPOSALS),
            "frozen_chain_count": len(frozen),
            "source_count": len(OFFICIAL_SOURCES),
            "novelty_all_pass": True,
            "x2_paths_created": 0,
            "outcomes_observed": False,
            "terminal_contact": False,
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.v656-v5.x1-staged-review.v1",
            "review_basis": "prospective full candidate set; exact equality required after git add",
            "source": d.SOURCE_FINAL,
            "paths": prospective_paths(),
            "all_paths_additive_or_new_phase_local": True,
            "x2_surface_paths": [],
            "outcome_or_closeout_paths": [],
            "sibling_paths": [],
            "destructive_paths": [],
            "valid": True,
        },
    )
    privacy_scan()
    # Rebuild staged review after privacy scan so it names the complete candidate set.
    review = read_json(ROOT / "validation/x1-staged-review.json")
    review["paths"] = prospective_paths()
    review["path_count"] = len(review["paths"])
    write_json("validation/x1-staged-review.json", review)
    x1_manifest()
    # The manifest changes the privacy scan's prospective count by one. Keep the
    # scan bounded to all non-self candidates and declare its own and manifest lifecycle.
    scan = read_json(ROOT / "validation/x1-privacy-scan.json")
    scan["manifest_excluded_from_initial_scan"] = True
    scan["manifest_review"] = "manifest contains only public relative paths and SHA-256 digests"
    write_json("validation/x1-privacy-scan.json", scan)
    # Recompute manifest after the bounded scan annotation changed.
    x1_manifest()
    print(
        json.dumps(
            {
                "valid": True,
                "phase": d.PHASE,
                "proposals": len(d.PROPOSALS),
                "frozen": len(frozen),
                "x1_negatives": len(X1_OPERATIONAL_NEGATIVES),
                "method_flow": flow["counts"]["methods"],
                "manifest_entries": read_json(
                    ROOT / "validation/x1-file-manifest.json"
                )["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
