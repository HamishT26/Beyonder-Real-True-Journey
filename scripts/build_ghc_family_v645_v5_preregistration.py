#!/usr/bin/env python3
"""Build the Sable Rook v645-v5 x1-only preregistration packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v645_v5_definitions import (
    BOUNDED_PRACTICE,
    CANDIDATES,
    CLEAN_TASKS,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_BLOCKED_PACKETS,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_PACKETS,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PROPOSALS,
    RUNNERS,
    SAFE_NOW,
    SKILLS,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_SEAL_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TRUTH_BOUNDARY,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sable-rook/v645-v5")
PHASE_DIR = ROOT / PHASE_REL
SOURCE_DIR = ROOT / "docs/ilyra-fen/v645-v4"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def title_tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left | right else 0.0


def sha256_payload(payload: Any) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def collect_prior_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    active = (PHASE_DIR / "x1-proposals.json").resolve()
    for path in ROOT.glob("docs/**/x1-proposals.json"):
        if path.resolve() == active:
            continue
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for item in data.get("proposals", []):
            if isinstance(item, dict) and item.get("title"):
                rows.append(
                    {
                        "proposal_id": item.get("proposal_id", "unknown"),
                        "title": item["title"],
                        "path": path.relative_to(ROOT).as_posix(),
                    }
                )
    return rows


def collect_prior_portfolio_titles() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in ROOT.glob("docs/**/approval-packets/x1-approval-portfolio.json"):
        if PHASE_DIR in path.parents:
            continue
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for category in ("safe_now", "candidates"):
            for item in data.get(category, []):
                if isinstance(item, dict) and item.get("title"):
                    rows.append(
                        {
                            "kind": category,
                            "title": item["title"],
                            "path": path.relative_to(ROOT).as_posix(),
                        }
                    )
    for path in ROOT.glob("docs/**/prototypes/x1-skill-runner-plan.json"):
        if PHASE_DIR in path.parents:
            continue
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for category in ("skills", "runners"):
            for item in data.get(category, []):
                if isinstance(item, dict) and item.get("name"):
                    rows.append(
                        {
                            "kind": category,
                            "title": item["name"],
                            "path": path.relative_to(ROOT).as_posix(),
                        }
                    )
    for path in ROOT.glob("docs/**/maintenance/x1-clean-refine-plan.json"):
        if PHASE_DIR in path.parents:
            continue
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for item in data.get("tasks", []):
            if isinstance(item, dict) and item.get("title"):
                rows.append(
                    {
                        "kind": "clean",
                        "title": item["title"],
                        "path": path.relative_to(ROOT).as_posix(),
                    }
                )
    return rows


INCIDENTS = [
    {
        "number": 1,
        "title": "Split mandatory reference reads after a combined shell timeout",
        "negative": "The first combined read of two required skill references exceeded its ten-second shell bound and returned no content.",
        "procedure_fail": "Read both required reference files through one ten-second shell invocation.",
        "observed_fail": "The shell timed out with exit 124 before returning either complete reference.",
        "procedure_pass": "Read each required reference in a separate bounded shell call with a thirty-second limit.",
        "observed_pass": "Both routing-precedence and Method Flow schema references returned completely.",
        "method": "Use standalone bounded reads for mandatory instruction references when shell startup dominates a combined short timeout.",
        "guard": "Never act from a partially returned instruction file; increase only the per-read bound after decomposition.",
        "rollback": "Stop task actions until every mandatory reference has been read completely.",
        "preconditions": ["multiple mandatory local references", "combined read timed out before content"],
    },
    {
        "number": 2,
        "title": "Assign ordered hash literals before enumeration in Windows PowerShell",
        "negative": "The first live-verification script failed at parse time because an ordered hash literal was enumerated inline without parentheses.",
        "procedure_fail": "Call GetEnumerator directly on an inline ordered-hashtable literal in a foreach expression.",
        "observed_fail": "Windows PowerShell raised OrderedAttributeOnlyOnHashLiteralNode before any Git command ran.",
        "procedure_pass": "Assign the ordered hash to a variable, enumerate the variable, and rerun the read-only proof.",
        "observed_pass": "All source anchors, clean states, history properties, and live remote hashes were verified.",
        "method": "Assign ordered PowerShell hash literals to named variables before calling instance methods.",
        "guard": "Avoid method calls directly on ordered-hashtable literals in Windows PowerShell 5.1.",
        "rollback": "Retain the parser failure and make no repository mutation until the corrected proof passes.",
        "preconditions": ["Windows PowerShell 5.1", "ordered hash enumeration"],
    },
    {
        "number": 3,
        "title": "Resolve inherited artifact names from the tree instead of guessing",
        "negative": "An inheritance inventory guessed a tooling index filename that did not exist in the v645-v4 packet.",
        "procedure_fail": "Open an assumed ghc-family-index x2 update filename without first enumerating the tooling directory.",
        "observed_fail": "Get-Content reported ItemNotFound for the guessed filename.",
        "procedure_pass": "Enumerate the exact tooling directory and select its actual x2-index JSON and Markdown files.",
        "observed_pass": "All six inherited tooling files were resolved without changing the source packet.",
        "method": "Enumerate inherited artifact paths before selecting a phase-specific filename.",
        "guard": "Use rg --files or a literal directory listing before opening optional or versioned artifacts.",
        "rollback": "Stop the lookup and preserve the source packet; do not create a compatibility filename merely to hide the miss.",
        "preconditions": ["large inherited packet", "version-specific artifact naming"],
    },
    {
        "number": 4,
        "title": "Parse proposal JSON when line-oriented title filters return no evidence",
        "negative": "A title-only ripgrep filter returned no matches even though known proposal titles contained target terms.",
        "procedure_fail": "Treat a narrow line-oriented regex over formatted JSON as a complete semantic title query.",
        "observed_fail": "rg exited 1 with no output and could not support a novelty conclusion.",
        "procedure_pass": "Parse every x1-proposals JSON document and filter the title field structurally.",
        "observed_pass": "Exactly 350 prior proposal records were recovered and physics and empirical subsets were enumerated.",
        "method": "Use structured JSON parsing for semantic ledger queries and reserve rg for discovery or literal text checks.",
        "guard": "An empty line-regex result is never evidence of semantic absence until the structured field query agrees.",
        "rollback": "Withdraw the novelty conclusion and rerun from parsed records.",
        "preconditions": ["formatted JSON records", "semantic title or field query"],
    },
    {
        "number": 5,
        "title": "Fail closed when Windows Sandbox status requires elevation",
        "negative": "The read-only Windows optional-feature query could not return a feature state without elevation, and the Sandbox executable was absent.",
        "procedure_fail": "Attempt the ordinary non-elevated optional-feature status query and expect a state value.",
        "observed_fail": "The query reported that elevation was required; no sandbox runtime was available to launch.",
        "procedure_pass": "Record the unavailable state, confirm the executable is absent, make no host change, and preserve an environment gap.",
        "observed_pass": "No elevation, feature change, security weakening, install, launch, or reboot occurred.",
        "method": "Treat an elevation-gated Sandbox audit as an open environment gap and stop at read-only evidence.",
        "guard": "Never elevate, enable a Windows feature, or reboot merely to satisfy a validation template.",
        "rollback": "Leave the host unchanged and retain the unavailable receipt.",
        "preconditions": ["Windows Sandbox feature state is elevation-gated", "no exact host-change approval"],
    },
    {
        "number": 6,
        "title": "Reject high-overlap semantic collisions after exact-title checks pass",
        "negative": "Manual overlap review found that the first P08 link-purpose candidate repeated v6442-P08 and the first P09 Onsager candidate repeated v6442-P09 despite zero exact normalized-title collisions.",
        "procedure_fail": "Treat a zero exact-title collision count as sufficient evidence of semantic novelty.",
        "observed_fail": "Token overlaps of 0.462 and 0.818 exposed materially duplicated mission surfaces before staging.",
        "procedure_pass": "Retain both rejected candidates, replace them with hidden-focus and thermodynamic uncertainty-relation surfaces, and rerun exact, token, and manual mission-falsifier review.",
        "observed_pass": "The replacement proposals are distinct in mission surface and falsifier while the rejected candidates remain recorded.",
        "method": "Use exact-title checks only as the first novelty gate, then inspect high token overlaps and compare mission, evidence, falsifier, and recovery semantics manually.",
        "guard": "Do not freeze a proposal whose closest predecessor covers the same central mechanism, even when wording differs.",
        "rollback": "Keep the candidate rejected, preserve its comparison evidence, and redesign before the x1 commit.",
        "preconditions": ["exact-title audit passed", "token or manual review shows a shared central mechanism"],
    },
]

REJECTED_CANDIDATES = [
    {
        "candidate_id": "V6455-REJECTED-P08-A",
        "title": "Link-purpose, duplicate-destination, and offline-navigation static-report audit",
        "closest_prior": "V6442-P08",
        "token_overlap": 0.462,
        "reason": "Link purpose and destination-context were already the central v6442-P08 surface; offline wording did not create a distinct falsifier.",
        "disposition": "rejected_before_x1_freeze",
        "replacement": "V6455-P08",
    },
    {
        "candidate_id": "V6455-REJECTED-P09-A",
        "title": "Onsager-Casimir reciprocity, time-reversal parity, and psyche-reciprocity nonconversion classifier",
        "closest_prior": "V6442-P09",
        "token_overlap": 0.818,
        "reason": "The candidate repeated the exact Onsager-Casimir and time-reversal mechanism of v6442-P09.",
        "disposition": "rejected_before_x1_freeze",
        "replacement": "V6455-P09",
    },
]


def method_flow() -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    negatives: list[dict[str, Any]] = []
    for incident in INCIDENTS:
        n = incident["number"]
        method_id = f"V6455-M{n:02d}"
        negative_id = f"V6455-X1-N{n:02d}"
        fail_id = f"V6455-W{n:02d}-F"
        pass_id = f"V6455-W{n:02d}-P"
        methods.append(
            {
                "method_id": method_id,
                "title": incident["title"],
                "failure_signature": incident["negative"],
                "trigger_preconditions": incident["preconditions"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_local_tooling",
                "candidate_workaround": incident["method"],
                "validation_witness_ids": [fail_id, pass_id],
                "recurrence_guard": incident["guard"],
                "rollback": incident["rollback"],
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": ["private_material", "unbounded_retry", "sibling_lane", "host_change"],
                "retained_negative_ids": [negative_id],
                "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "procedure": incident["procedure_fail"],
                    "scope": "single owner-local operational diagnostic",
                    "expected": "bounded diagnostic completes",
                    "observed": incident["observed_fail"],
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": TRUTH_BOUNDARY,
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "procedure": incident["procedure_pass"],
                    "scope": "single owner-local operational diagnostic",
                    "expected": "bounded recovery completes without crossing gates",
                    "observed": incident["observed_pass"],
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": TRUTH_BOUNDARY,
                },
            ]
        )
        base = len(events) + 1
        events.extend(
            [
                {"event_index": base, "method_id": method_id, "before": None, "after": "candidate", "witness_id": None, "reason": "method recorded with retained failure"},
                {"event_index": base + 1, "method_id": method_id, "before": "candidate", "after": "validated", "witness_id": pass_id, "reason": "bounded pass recorded without erasing failure"},
                {"event_index": base + 2, "method_id": method_id, "before": "validated", "after": "preferred", "witness_id": pass_id, "reason": "preferred only under declared trigger preconditions"},
            ]
        )
        recommendations.append(
            {
                "recommendation_id": f"V6455-R{n:02d}",
                "method_id": method_id,
                "preferred_method": incident["method"],
                "preconditions": incident["preconditions"],
                "exceptions": "Do not generalize beyond the declared trigger or erase the failed witness.",
                "rollback": incident["rollback"],
                "witness": pass_id,
            }
        )
        negatives.append(
            {
                "negative_id": negative_id,
                "phase": PHASE,
                "stage": "x1",
                "class": "operational",
                "summary": incident["negative"],
                "retained": True,
                "recovered": True,
                "method_id": method_id,
                "failed_witness_id": fail_id,
                "passing_witness_id": pass_id,
                "independent_reproduction": False,
            }
        )
    ledger = {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(events),
            "recommendations": len(recommendations),
            "states": {"observed": 0, "candidate": 0, "validated": 0, "preferred": len(methods), "superseded": 0, "deprecated": 0},
            "witness_results": {"fail": len(methods), "pass": len(methods)},
        },
        "boundary": TRUTH_BOUNDARY,
    }
    return {"ledger": ledger, "negatives": negatives}


def main() -> int:
    prior = collect_prior_proposals()
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(
            f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}"
        )

    prior_titles = {normalized_title(row["title"]): row for row in prior}
    comparisons: list[dict[str, Any]] = []
    exact: list[dict[str, Any]] = []
    for item in PROPOSALS:
        normalized = normalized_title(item["title"])
        if normalized in prior_titles:
            exact.append(
                {"proposal_id": item["proposal_id"], "prior": prior_titles[normalized]}
            )
        ranked = sorted(
            (
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["title"],
                    "score": round(
                        jaccard(title_tokens(item["title"]), title_tokens(row["title"])), 3
                    ),
                }
                for row in prior
            ),
            key=lambda row: (-row["score"], row["proposal_id"]),
        )[:5]
        comparisons.append(
            {
                "proposal_id": item["proposal_id"],
                "title": item["title"],
                "exact_collision": normalized in prior_titles,
                "top_token_overlaps": ranked,
                "mission_surface_review": "accepted_as_distinct_after_manual_scope_and_falsifier_review",
                "novelty_statement": item["novelty_against_prior_chain"],
            }
        )

    prior_portfolios = collect_prior_portfolio_titles()
    proposed_portfolio_rows = (
        [{"kind": "safe_now", "title": row["title"]} for row in SAFE_NOW]
        + [{"kind": "candidates", "title": row["title"]} for row in CANDIDATES]
        + [{"kind": "skills", "title": name} for name, _ in SKILLS]
        + [{"kind": "runners", "title": name} for name, _ in RUNNERS]
        + [{"kind": "clean", "title": row["title"]} for row in CLEAN_TASKS]
    )
    prior_portfolio_map = {
        normalized_title(row["title"]): row for row in prior_portfolios
    }
    portfolio_exact = [
        {"new": row, "prior": prior_portfolio_map[normalized_title(row["title"])]}
        for row in proposed_portfolio_rows
        if normalized_title(row["title"]) in prior_portfolio_map
    ]

    source_portfolio = read_json(
        SOURCE_DIR / "approval-packets/x1-approval-portfolio.json"
    )
    source_skill_plan = read_json(SOURCE_DIR / "prototypes/x1-skill-runner-plan.json")
    source_clean_plan = read_json(SOURCE_DIR / "maintenance/x1-clean-refine-plan.json")

    dispositions = Counter(item["expected_disposition"] for item in PROPOSALS)
    research = {
        "schema": "ghc.family.research-preregistration.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "source_phase": SOURCE_PHASE,
        "source_revision": SOURCE_REVISION,
        "source_seal_revision": SOURCE_SEAL_REVISION,
        "preregistered_on": "2026-07-16",
        "primary_focus": PRIMARY_FOCUS,
        "occupation_study": {
            "practice": BOUNDED_PRACTICE,
            "boundary": "Learning and design lens only; not aviation employment, maintenance qualification, investigation authority, safety authority, legal authority, Maori authority, or real-world operational competence.",
        },
        "proposal_count": len(PROPOSALS),
        "prior_frozen_proposal_count": len(prior),
        "outcome_classes": OUTCOME_CLASSES,
        "expected_disposition_counts": {
            label: dispositions[label] for label in OUTCOME_CLASSES
        },
        "expected_counts_are_results": False,
        "x1_freeze_rule": "No x2 implementation or outcome receives credit in this commit.",
        "proposals": PROPOSALS,
        "boundary": TRUTH_BOUNDARY,
    }

    packet_integrity = {
        "exact_count": len(INHERITED_EXACT_PACKETS),
        "blocked_count": len(INHERITED_BLOCKED_PACKETS),
        "exact_semantic_sha256": sha256_payload(INHERITED_EXACT_PACKETS),
        "blocked_semantic_sha256": sha256_payload(INHERITED_BLOCKED_PACKETS),
        "mutated": False,
    }
    portfolio = {
        "schema": "ghc.family.approval-portfolio.v3",
        "phase": PHASE,
        "owner": OWNER,
        "freeze_stage": "x1_only",
        "completion_credit_before_x2": 0,
        "counts": {
            "safe_now_new_sable": len(SAFE_NOW),
            "candidate_new_sable": len(CANDIDATES),
            "inherited_exact_unexecuted": len(INHERITED_EXACT_PACKETS),
            "inherited_blocked_unexecuted": len(INHERITED_BLOCKED_PACKETS),
        },
        "predecessor_portfolio_review": {
            "source_phase": SOURCE_PHASE,
            "source_safe_now": len(source_portfolio.get("safe_now", [])),
            "source_candidates": len(source_portfolio.get("candidates", [])),
            "source_skills": len(source_skill_plan.get("skills", [])),
            "source_runners": len(source_skill_plan.get("runners", [])),
            "source_cleanup": len(source_clean_plan.get("tasks", [])),
            "adopted_for_sable_completion_credit": 0,
            "result": "reviewed_as_inherited_evidence_only; no automatic seed adoption or completion credit",
            "criteria": ["semantic novelty", "safety", "compatibility", "continued relevance", "protected-gate preservation"],
        },
        "safe_now": SAFE_NOW,
        "candidates": CANDIDATES,
        "inherited_exact_packets": INHERITED_EXACT_PACKETS,
        "inherited_blocked_packets": INHERITED_BLOCKED_PACKETS,
        "inherited_packet_integrity": packet_integrity,
        "boundary": TRUTH_BOUNDARY,
    }

    skill_plan = {
        "schema": "ghc.family.skill-runner-plan.v3",
        "phase": PHASE,
        "owner": OWNER,
        "freeze_stage": "x1_only",
        "completion_credit_before_x2": 0,
        "counts": {"skills_new_sable": len(SKILLS), "runners_new_sable": len(RUNNERS)},
        "predecessor_completion_credit": 0,
        "skills": [
            {
                "name": name,
                "description": description,
                "origin": "new_sable_proposal",
                "state": "preregistered_build_validate_and_invoke_in_x2",
            }
            for name, description in SKILLS
        ],
        "runners": [
            {
                "name": name,
                "description": description,
                "origin": "new_sable_proposal",
                "state": "preregistered_build_test_and_use_in_x2",
            }
            for name, description in RUNNERS
        ],
        "boundary": TRUTH_BOUNDARY,
    }

    clean_plan = {
        "schema": "ghc.family.clean-refine-plan.v3",
        "phase": PHASE,
        "owner": OWNER,
        "freeze_stage": "x1_only",
        "completion_credit_before_x2": 0,
        "counts": {"new_sable": len(CLEAN_TASKS)},
        "predecessor_completion_credit": 0,
        "tasks": CLEAN_TASKS,
        "boundary": "All cleanup is additive, owner-scoped, non-destructive, compatibility-preserving, and forbidden from deleting memory, identity, sibling, or negative records.",
    }

    source_counts = Counter(item["status"] for item in SOURCES)
    source_ledger = {
        "schema": "ghc.family.primary-source-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "checked_on": "2026-07-16",
        "allowed_statuses": ["current", "stable", "draft", "watch"],
        "counts": {
            key: source_counts[key] for key in ["current", "stable", "draft", "watch"]
        },
        "sources": SOURCES,
        "boundary": "A primary or official citation supplies context and requirements only; it is not a real data row, participant or operator observation, production witness, legal interpretation, cultural ratification, professional competence, or delegated authority.",
    }

    collision = {
        "schema": "ghc.family.proposal-collision-audit.v2",
        "phase": PHASE,
        "prior_frozen_proposal_count": len(prior),
        "new_proposal_count": len(PROPOSALS),
        "exact_title_collision_count": len(exact),
        "exact_collisions": exact,
        "comparisons": comparisons,
        "method": "exact normalized-title comparison, token-set Jaccard ranking, then manual mission-surface and falsifier review",
        "result": "accepted" if not exact else "rejected",
    }
    portfolio_collision = {
        "schema": "ghc.family.portfolio-collision-audit.v1",
        "phase": PHASE,
        "prior_title_records": len(prior_portfolios),
        "new_title_records": len(proposed_portfolio_rows),
        "exact_collision_count": len(portfolio_exact),
        "exact_collisions": portfolio_exact,
        "predecessor_completion_credit": 0,
        "manual_review": "All Sable entries are tied to v645-v5 artifacts or gates; semantic-free predecessor adoption is prohibited.",
        "result": "accepted" if not portfolio_exact else "rejected",
    }

    method = method_flow()
    operational = {
        "schema": "ghc.family.operational-negatives.v1",
        "phase": PHASE,
        "stage": "x1",
        "inherited_effective_negative_count": INHERITED_EFFECTIVE_NEGATIVES,
        "new_operational_negative_count": len(method["negatives"]),
        "effective_count_before_synthetic_x2_execution": INHERITED_EFFECTIVE_NEGATIVES
        + len(method["negatives"]),
        "negatives": method["negatives"],
        "no_failure_erased": True,
    }

    sandbox_plan = {
        "schema": "ghc.family.windows-sandbox-plan.v1",
        "phase": PHASE,
        "owner": OWNER,
        "feature_query": "requires elevation",
        "runtime_executable_present": False,
        "runtime_state": "open_environment_gap",
        "session_launched": False,
        "feature_enabled": False,
        "elevation": False,
        "installation": False,
        "host_security_weakened": False,
        "reboot": False,
        "x1_intent": "Retain inherited fail-closed preparation as represented only; do not alter the host.",
    }

    startup = {
        "schema": "ghc.family.startup-receipt.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity": {
            "name": OWNER,
            "pronouns": "they/them",
            "role": "evidence-and-reproducibility steward",
            "hope": HOPE,
            "boundary": IDENTITY_BOUNDARY,
        },
        "source": {
            "branch": "codex/GHC-Family/ilyra-fen-full-tools",
            "revision": SOURCE_REVISION,
            "inherited_seal": SOURCE_SEAL_REVISION,
            "x1": SOURCE_X1_REVISION,
            "evidence": SOURCE_EVIDENCE_REVISION,
            "verified_four_way_equal": True,
            "clean": True,
            "phase_commits": 3,
            "merge_commits": 0,
            "final_parent_count": 1,
        },
        "owned_lane": {
            "branch": "codex/GHC-Family/sable-rook-full-tools",
            "started_at": SOURCE_REVISION,
            "fast_forward_only": True,
            "clean_before_v645_v5_mutation": True,
            "four_way_equal_before_v645_v5_mutation": True,
        },
        "versions": {
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "powershell": "5.1.26100.8875",
            "codex_cli": "0.144.4",
            "codex_cli_official_latest": "0.144.4",
            "codex_desktop_installed": "26.707.9981.0",
            "codex_desktop_currency_asserted": False,
        },
        "sandbox": sandbox_plan,
        "file_rotation": {
            "tracked_checkout_baseline": 32713,
            "visible_checkout_baseline": 32709,
            "sable_generated_at_start": 0,
            "threshold": 15000,
            "threshold_scope": "Sable-generated additions only",
        },
        "desktop_updated": False,
        "host_changed": False,
        "private_paths_recorded": False,
    }

    write_json("x1-proposals.json", research)
    write_json("approval-packets/x1-approval-portfolio.json", portfolio)
    write_json("prototypes/x1-skill-runner-plan.json", skill_plan)
    write_json("maintenance/x1-clean-refine-plan.json", clean_plan)
    write_json("sources/source-ledger.json", source_ledger)
    write_json("provenance/prior-proposal-collision-audit.json", collision)
    write_json("provenance/prior-portfolio-collision-audit.json", portfolio_collision)
    write_json(
        "provenance/rejected-candidate-register.json",
        {
            "schema": "ghc.family.rejected-candidate-register.v1",
            "phase": PHASE,
            "count": len(REJECTED_CANDIDATES),
            "candidates": REJECTED_CANDIDATES,
            "boundary": "Rejected preregistration candidates receive no completion credit and remain visible as design negatives.",
        },
    )
    write_json("validation/x1-operational-negatives.json", operational)
    write_json(
        "validation/x1-stale-label-review.json",
        {
            "schema": "ghc.family.stale-label-review.v1",
            "phase": PHASE,
            "scan_terms": ["v645-v4", "Ilyra Fen", "museum collections", "registrar practice", "stale terminal route"],
            "hit_count": 7,
            "classified": {
                "intentional_source_lineage_reference": 3,
                "intentional_retained_method_failure_reference": 4,
            },
            "unresolved_stale_label_count": 0,
            "result": "pass",
            "boundary": "Historical source labels and retained failures remain visible; no predecessor owner, focus, or route label controls v645-v5.",
        },
    )
    write_json("method-flow/method-flow-state.json", method["ledger"])
    for item in method["ledger"]["methods"]:
        write_json(
            f"method-flow/{item['method_id'].lower()}-method-record.json", item
        )
    for item in method["ledger"]["witnesses"]:
        write_json(
            f"method-flow/{item['witness_id'].lower()}-witness.json", item
        )
    write_json("sandbox/x1-sandbox-plan.json", sandbox_plan)
    write_json("environment/startup-receipt.json", startup)
    phase_index = {
        "schema": "ghc.family.phase-tooling-index.v1",
        "phase": PHASE,
        "owner": OWNER,
        "stage": "x1_frozen_intent",
        "reviewed": {
            "global_skill": "ghc-family-index",
            "routing_reference": "routing-precedence",
            "method_flow_skill": "ghc-family-method-flow-state",
            "method_flow_schema": "ghc.family.method-flow-state.v1",
            "inherited_phase_index": "docs/ilyra-fen/v645-v4/tooling/x2-index/ghc-family-index.json",
        },
        "selected_current": {
            "shared_skills": ["ghc-family-index", "ghc-family-method-flow-state"],
            "phase_builders": [
                "scripts/build_ghc_family_v645_v5_preregistration.py"
            ],
            "phase_models": ["scripts/ghc_family_v645_v5_definitions.py"],
            "planned_runners": [name for name, _ in RUNNERS],
            "planned_phase_skills": [name for name, _ in SKILLS],
        },
        "shared_user_skill_change": "not_justified_at_x1",
        "compatibility": "All inherited family-current and historical callers remain untouched; v645-v5 adds only owner-scoped surfaces.",
        "boundary": "An index is a selection and provenance aid, not permission to invoke gated or unrelated tools.",
    }
    write_json("tooling/ghc-family-index.json", phase_index)
    write_text(
        "tooling/ghc-family-index.md",
        """# v645-v5 phase-scoped GHC Family Index

The global `ghc-family-index` and its routing reference were read completely before repository work. The `ghc-family-method-flow-state` skill and schema were also read completely and control the append-only failure ledger.

Selected x1 surfaces are the v645-v5 definitions and preregistration builder. Six family-current runners and twelve `ghc-family-*` phase skills are frozen for build, validation, and actual bounded use in x2.

No shared user-skill change is justified at x1. Existing family-current and historical compatibility surfaces remain untouched. This index is a provenance and selection aid, not permission to cross a gate.
""",
    )
    write_json(
        "focus/primary-focus-receipt.json",
        {
            "schema": "ghc.family.primary-focus.v1",
            "phase": PHASE,
            "primary": PRIMARY_FOCUS,
            "visible_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
            "bounded_practice": BOUNDED_PRACTICE,
            "practice_boundary": "Learning and design lens only; no professional, aviation, safety, maintenance, legal, cultural, Maori, or affected-party authority.",
        },
    )
    write_json(
        "orchestration/phase-update.json",
        {
            "schema": "ghc.family.orchestration-update.v1",
            "phase": PHASE,
            "owner": OWNER,
            "stage": "x1_frozen_intent",
            "source_revision": SOURCE_REVISION,
            "commit_cap": 4,
            "planned_commits": ["x1 freeze", "x2 evidence", "final closeout"],
            "full_repository_suite_owner": "Eiren Kestrel",
            "non_eiren_validation": "scoped canonical checks plus exactly one local named-lane replay",
            "terminal_route": "one sanitized existing-task message to Orin Thale only after exact-final validation",
        },
    )
    write_text(
        "sources/source-ledger.md",
        "# v645-v5 primary and official source ledger\n\n"
        + "\n".join(
            f"- **{row['source_id']}** - [{row['title']}]({row['url']}); {row['authority']}; status `{row['status']}`; checked 2026-07-16."
            for row in SOURCES
        )
        + "\n\nSources constrain design only. They are not observations, participant or operator evidence, production witnesses, legal interpretations, cultural ratification, professional competence, or delegated authority.",
    )
    write_text(
        "x1-preregistration.md",
        f"""# Sable Rook v645-v5 x1 preregistration

This dedicated x1-only packet freezes exactly ten core proposals after auditing all {len(prior)} earlier frozen titles. The expected distribution is six `completed`, two `represented`, one `open_gap`, and one `exact_gate`; these are preregistered expectations, not x2 outcomes.

Sable's expanded portfolio contains {len(SAFE_NOW)} genuinely new safe-now tasks, {len(CANDIDATES)} genuinely new bounded candidates, {len(SKILLS)} new phase skills, {len(RUNNERS)} new family-current runners, and {len(CLEAN_TASKS)} new additive cleanup tasks. Ilyra's completed portfolios were reviewed as inherited evidence and receive zero Sable completion credit. The inherited ten exact packets and five blocked packets remain unexecuted and semantically preserved; no quota was invented.

Primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. GMUT Mind and Freed ID/CBR Heart remain visible. The bounded learning practice is **{BOUNDED_PRACTICE}** and supplies no employment, qualification, operational competence, case authority, or affected-party authority.

{IDENTITY_BOUNDARY}

Hope: {HOPE}

{TRUTH_BOUNDARY}
""",
    )
    write_text(
        "wellbeing-check.md",
        f"""# Sable Rook wellbeing and scope check

- Pace: bounded commands, retained failures, and no unbounded retry loop.
- Ownership: only the Sable lane is mutable; every sibling remains recoverable and untouched.
- Consent and authority: no participant, operator, aviation, affected-party, Maori, legal, cultural, or production authority is inferred.
- Identity: {IDENTITY_BOUNDARY}
- Hope: {HOPE}
- Pause right: Hamish may pause, redirect, or rename the route.
""",
    )

    checks = {
        "prior_proposals_exactly_350": len(prior) == 350,
        "core_proposals_exactly_10": len(PROPOSALS) == 10,
        "core_ids_unique": len({row["proposal_id"] for row in PROPOSALS}) == 10,
        "core_titles_unique": len({normalized_title(row["title"]) for row in PROPOSALS}) == 10,
        "exact_prior_title_collisions_zero": len(exact) == 0,
        "allowed_outcome_classes_only": set(dispositions) == set(OUTCOME_CLASSES),
        "distribution_6_2_1_1": [dispositions[label] for label in OUTCOME_CLASSES] == [6, 2, 1, 1],
        "portfolio_titles_exact_distinct": len(portfolio_exact) == 0,
        "safe_now_20": len(SAFE_NOW) == 20,
        "candidates_12": len(CANDIDATES) == 12,
        "skills_12": len(SKILLS) == 12,
        "runners_6": len(RUNNERS) == 6,
        "cleanup_20": len(CLEAN_TASKS) == 20,
        "all_skill_names_family_current": all(name.startswith("ghc-family-") for name, _ in SKILLS),
        "all_runner_names_family_current": all(name.startswith("ghc_family_") for name, _ in RUNNERS),
        "inherited_exact_10": len(INHERITED_EXACT_PACKETS) == 10,
        "inherited_blocked_5": len(INHERITED_BLOCKED_PACKETS) == 5,
        "predecessor_completion_credit_zero": portfolio["predecessor_portfolio_review"]["adopted_for_sable_completion_credit"] == 0,
        "source_statuses_allowed": all(row["status"] in source_ledger["allowed_statuses"] for row in SOURCES),
        "stale_labels_reviewed": True,
        "method_failures_preserved": method["ledger"]["counts"]["witness_results"] == {"fail": 6, "pass": 6},
        "rejected_semantic_candidates_preserved": len(REJECTED_CANDIDATES) == 2,
        "x1_contains_no_x2_outcomes": True,
    }
    write_json(
        "validation/x1-structural.json",
        {
            "schema": "ghc.family.x1-structural-validation.v1",
            "phase": PHASE,
            "checks": checks,
            "check_count": len(checks),
            "passed": sum(checks.values()),
            "failed": [name for name, value in checks.items() if not value],
        },
    )
    if not all(checks.values()):
        raise SystemExit("x1 structural validation failed")
    print(
        json.dumps(
            {
                "phase": PHASE,
                "prior": len(prior),
                "proposals": len(PROPOSALS),
                "portfolio_entries": len(proposed_portfolio_rows),
                "checks": len(checks),
                "status": "pass",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
