#!/usr/bin/env python3
"""Build the Orin Thale v645-v6 x1-only preregistration packet."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from ghc_family_v645_v6_definitions import (
    BOUNDED_PRACTICE,
    CANDIDATES,
    CLEAN_TASKS,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    PRONOUNS,
    PROPOSALS,
    ROLE,
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
PHASE_REL = Path("docs/orin-thale/v645-v6")
PHASE_DIR = ROOT / PHASE_REL
SOURCE_DIR = ROOT / "docs/sable-rook/v645-v5"


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


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def overlap(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 0.0


def collect_prior_proposals() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
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
                        "proposal_id": str(item.get("proposal_id", "unknown")),
                        "title": str(item["title"]),
                        "path": path.relative_to(ROOT).as_posix(),
                    }
                )
    return rows


def collect_prior_portfolios() -> list[dict[str, str]]:
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
                            "title": str(item["title"]),
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
                label = item.get("name") if isinstance(item, dict) else None
                if label:
                    rows.append(
                        {
                            "kind": category,
                            "title": str(label),
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
                        "title": str(item["title"]),
                        "path": path.relative_to(ROOT).as_posix(),
                    }
                )
    return rows


INCIDENTS = [
    {
        "number": 1,
        "title": "Split broad Git startup probes after an evidence-free timeout",
        "negative": "The first combined worktree, status, head, and branch probe exceeded its bounded shell time and returned no evidence.",
        "fail_procedure": "Run worktree enumeration and status plus head and branch reads in one bounded command.",
        "fail_observed": "The wrapper timed out before returning any Git evidence.",
        "pass_procedure": "Run rev-parse, branch, status, ancestry, and remote equality as small separately timed read-only probes.",
        "pass_observed": "The source and Orin lane were proven clean, exact, and fast-forward compatible before mutation.",
        "method": "Decompose startup Git proof into small read-only probes and capture each native result separately.",
        "guard": "Do not retry a broad timed-out wrapper or infer any result from its silence.",
        "rollback": "Make no repository mutation until the decomposed proof passes.",
        "preconditions": ["large linked-worktree repository", "combined read-only Git probe returned no evidence"],
        "side_effect_budget": ["read_only_git_metadata", "no_ref_change", "no_worktree_change"],
    },
    {
        "number": 2,
        "title": "Remove unsupported ConvertFrom-Json parameters before structured audit",
        "negative": "A Windows PowerShell structured JSON inspection used an unsupported Depth parameter and produced no parsed evidence.",
        "fail_procedure": "Invoke ConvertFrom-Json with the newer Depth parameter on Windows PowerShell 5.1.",
        "fail_observed": "PowerShell rejected the parameter before parsing either JSON document.",
        "pass_procedure": "Use ConvertFrom-Json without Depth and bound only ConvertTo-Json output depth.",
        "pass_observed": "The collision audit and proposal ledger parsed successfully without changing source artifacts.",
        "method": "Keep Windows PowerShell 5.1 JSON input parsing parameter-free and apply depth only when rendering output.",
        "guard": "Check cmdlet version-specific parameters before using them in evidence probes.",
        "rollback": "Withdraw the parse conclusion and rerun the exact read-only inspection.",
        "preconditions": ["Windows PowerShell 5.1", "structured JSON inspection"],
        "side_effect_budget": ["read_only_json", "no_artifact_change"],
    },
    {
        "number": 3,
        "title": "Fail closed when Windows Sandbox state is elevation-gated",
        "negative": "The ordinary optional-feature query required elevation and the Windows Sandbox executable was absent.",
        "fail_procedure": "Run the non-elevated read-only Windows optional-feature query and expect an available state.",
        "fail_observed": "The query reported an elevation requirement; no Sandbox executable was available.",
        "pass_procedure": "Record the unavailable state, confirm no executable, make no host change, and preserve the environment gap.",
        "pass_observed": "No elevation, feature change, install, host-security weakening, Sandbox launch, or reboot occurred.",
        "method": "Treat elevation-gated Sandbox status as an open environment gap and stop at read-only evidence.",
        "guard": "Never elevate, enable a feature, weaken security, or reboot to satisfy a validation template.",
        "rollback": "Leave the host unchanged and retain the unavailable receipt.",
        "preconditions": ["Sandbox status requires elevation", "no exact host-change authorization"],
        "side_effect_budget": ["read_only_host_query", "no_elevation", "no_feature_change", "no_reboot"],
    },
    {
        "number": 4,
        "title": "Reject predecessor portfolio collisions before materialization",
        "negative": "The first x1 build attempt found fourteen cleanup titles that exactly repeated predecessor portfolio tasks and stopped before writing the phase packet.",
        "fail_procedure": "Reuse generic predecessor cleanup titles while claiming a genuinely new Orin cleanup portfolio.",
        "fail_observed": "The portfolio collision gate listed fourteen exact title collisions and exited before artifact materialization.",
        "pass_procedure": "Replace every collided task with an Orin-specific purpose and acceptance surface, then rerun the full predecessor title audit.",
        "pass_observed": "The corrected safe-now, candidate, skill, runner, and cleanup portfolios have zero exact predecessor title collisions.",
        "method": "Run portfolio collision detection before phase materialization and redesign every exact collision instead of waiving it.",
        "guard": "Generic maintenance obligations still require a distinct owner-scoped purpose, artifact, acceptance gate, or evidence surface.",
        "rollback": "Leave the phase directory absent, preserve the failed comparison, and redesign before the x1 freeze.",
        "preconditions": ["successor portfolio design", "predecessor title corpus available"],
        "side_effect_budget": ["read_only_predecessor_scan", "no_phase_artifact_write", "no_history_change"],
    },
    {
        "number": 5,
        "title": "Use a dependency-free scoped test entrypoint when pytest is absent",
        "negative": "The selected Python runtime had no pytest module, so the first scoped test invocation ran zero tests and received no evidence credit.",
        "fail_procedure": "Invoke the v645-v6 x1 file through python -m pytest in the selected runtime.",
        "fail_observed": "The runtime reported that pytest was absent; zero tests ran and zero evidence credit was assigned.",
        "pass_procedure": "Invoke the deterministic dependency-free direct entrypoint in the v645-v6 x1 test file.",
        "pass_observed": "All ten phase-local x1 tests ran and passed with no dependency or environment change.",
        "method": "Keep the assertions and add a deterministic dependency-free direct entrypoint that discovers and invokes only the phase-local test functions.",
        "guard": "Check the intended test runtime and preserve zero-test dependency failures before switching runners.",
        "rollback": "Do not count the failed invocation; retain the test source and run only the bounded phase entrypoint.",
        "preconditions": ["phase-local pure-Python assertions", "pytest module absent from selected runtime"],
        "side_effect_budget": ["phase_test_file_only", "no_package_install", "no_environment_update"],
    },
    {
        "number": 6,
        "title": "Normalize family-index checkout text after preserving encoding drift",
        "negative": "The family-index builder emitted phase-local text with CRLF checkout bytes and a visibly mojibake Markdown dash.",
        "fail_procedure": "Run the x1 structural byte and encoding scan over the first family-index output.",
        "fail_observed": "Both files contained CRLF checkout bytes and the Markdown heading displayed a mojibake dash.",
        "pass_procedure": "Normalize canonical index blobs into the two owner-scoped files and rerun UTF-8, CRLF, and visible-heading checks.",
        "pass_observed": "Both files passed UTF-8 and LF-only checks, the heading rendered correctly, and no family tool was semantically promoted.",
        "method": "Normalize only the owner phase index outputs from canonical Git index blobs after recording the original encoding drift.",
        "guard": "Inspect generated text bytes and visible headings before staging family-index output on Windows.",
        "rollback": "Restore the phase-local generated files and retain the encoding negative if normalization changes semantics.",
        "preconditions": ["Windows family-index generation", "owner-scoped phase output", "UTF-8 LF cleanup obligation"],
        "side_effect_budget": ["two_owner_phase_files", "no_shared_skill_change", "no_tool_selection_change"],
    },
]


def method_record(incident: dict[str, Any]) -> dict[str, Any]:
    n = incident["number"]
    return {
        "method_id": f"V6456-M{n:02d}",
        "title": incident["title"],
        "failure_signature": incident["negative"],
        "trigger_preconditions": incident["preconditions"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_local_tooling",
        "candidate_workaround": incident["method"],
        "validation_witness_ids": [],
        "recurrence_guard": incident["guard"],
        "rollback": incident["rollback"],
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["private_material", "destructive_action", "sibling_lane", "host_change"],
        "retained_negative_ids": [f"V6456-X1-N{n:02d}"],
        "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
        "side_effect_budget": incident["side_effect_budget"],
        "rollback_witness_required": True,
    }


def witness(incident: dict[str, Any], result: str) -> dict[str, Any]:
    n = incident["number"]
    passed = result == "pass"
    return {
        "witness_id": f"V6456-W{n:02d}-{'P' if passed else 'F'}",
        "method_id": f"V6456-M{n:02d}",
        "procedure": incident["pass_procedure"] if passed else incident["fail_procedure"],
        "scope": "single owner-local operational diagnostic",
        "expected": "bounded diagnostic or recovery completes without crossing gates",
        "observed": incident["pass_observed"] if passed else incident["fail_observed"],
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [f"V6456-X1-N{n:02d}"],
        "boundary": TRUTH_BOUNDARY,
    }


def main() -> int:
    if PHASE_DIR.exists() and any(PHASE_DIR.rglob("*")):
        raise SystemExit("v645-v6 phase directory already contains files")

    prior = collect_prior_proposals()
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    prior_by_normal = {normalized(row["title"]): row for row in prior}
    comparisons: list[dict[str, Any]] = []
    exact: list[dict[str, Any]] = []
    for item in PROPOSALS:
        if normalized(item["title"]) in prior_by_normal:
            exact.append({"proposal_id": item["proposal_id"], "prior": prior_by_normal[normalized(item["title"])]})
        ranked = sorted(
            (
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["title"],
                    "score": round(overlap(item["title"], row["title"]), 3),
                }
                for row in prior
            ),
            key=lambda row: (-row["score"], row["proposal_id"]),
        )[:5]
        comparisons.append(
            {
                "proposal_id": item["proposal_id"],
                "title": item["title"],
                "exact_collision": False,
                "top_token_overlaps": ranked,
                "mission_falsifier_evidence_recovery_review": "accepted_as_distinct_after_manual_review",
                "novelty_statement": item["novelty_against_360_frozen_proposals"],
            }
        )
    if exact:
        raise SystemExit(f"proposal title collision: {exact}")

    portfolio_prior = collect_prior_portfolios()
    new_portfolio = [
        *[("safe_now", item["title"]) for item in SAFE_NOW],
        *[("candidates", item["title"]) for item in CANDIDATES],
        *[("skills", item[0]) for item in SKILLS],
        *[("runners", item[0]) for item in RUNNERS],
        *[("clean", item["title"]) for item in CLEAN_TASKS],
    ]
    prior_norm = {normalized(item["title"]): item for item in portfolio_prior}
    portfolio_collisions = [
        {"kind": kind, "title": title, "prior": prior_norm[normalized(title)]}
        for kind, title in new_portfolio
        if normalized(title) in prior_norm
    ]
    if portfolio_collisions:
        raise SystemExit(f"portfolio title collision: {portfolio_collisions}")

    source_portfolio = read_json(SOURCE_DIR / "approval-packets/x1-approval-portfolio.json")
    inherited_exact = deepcopy(source_portfolio["inherited_exact_packets"])
    inherited_blocked = deepcopy(source_portfolio["inherited_blocked_packets"])
    if len(inherited_exact) != 10 or len(inherited_blocked) != 5:
        raise SystemExit("expected ten inherited exact and five inherited blocked packets")

    write_json(
        "identity-receipt.json",
        {
            "schema": "ghc.family.v645-v6.identity-receipt.v1",
            "phase": PHASE,
            "working_name": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
            "bounded_practice_study": BOUNDED_PRACTICE,
            "boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "x1-proposals.json",
        {
            "schema": "ghc.family.v645-v6.proposals.v1",
            "phase": PHASE,
            "owner": OWNER,
            "freeze_stage": "x1_only",
            "prior_frozen_proposal_count": PRIOR_FROZEN_PROPOSALS,
            "new_frozen_proposal_count": len(PROPOSALS),
            "frozen_chain_count_after_x1": PRIOR_FROZEN_PROPOSALS + len(PROPOSALS),
            "allowed_outcome_classes": OUTCOME_CLASSES,
            "x2_execution_present": False,
            "proposals": PROPOSALS,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_text(
        "x1-preregistration.md",
        """# Orin Thale v645-v6 x1 preregistration

This is the dedicated x1-only freeze for exactly ten core proposals. It records hypotheses, failure conditions, approval classes, execution lanes, current primary or official source needs, artifacts, acceptance gates, recovery, protected gates, and expected dispositions. It contains no x2 implementation, outcome credit, or claim that an expected disposition has been achieved.

The primary Trinity Mandala focus is **GMUT Mind**. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is maritime bridge-resource management and near-miss review. It is a learning and design lens only, never evidence of employment, licensure, competence, maritime authority, investigation authority, legal authority, cultural authority, Māori authority, or affected-party authorization.

The inherited 2,172 effective negatives include the repository-preserved v645-v5 total and four sanitized post-final operational negatives. Seventy synthetic mutation negatives are preregistered. Every new operational failure must remain visible. X2 may start only after this freeze is committed, pushed, clean, and proven equal across local, upstream, tracking, and fresh live remote.

Terminal truth remains `NOT_READY_FOR_STAGE_20`.""",
    )
    write_json(
        "provenance/prior-proposal-collision-audit.json",
        {
            "schema": "ghc.family.proposal-collision-audit.v3",
            "phase": PHASE,
            "prior_frozen_proposal_count": len(prior),
            "new_proposal_count": len(PROPOSALS),
            "exact_title_collision_count": len(exact),
            "exact_collisions": exact,
            "comparisons": comparisons,
            "manual_review_dimensions": ["mission_surface", "hypothesis", "failure_condition", "evidence_need", "acceptance_gate", "recovery", "protected_gates"],
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "provenance/prior-portfolio-collision-audit.json",
        {
            "schema": "ghc.family.portfolio-collision-audit.v2",
            "phase": PHASE,
            "prior_title_count": len(portfolio_prior),
            "new_title_count": len(new_portfolio),
            "exact_collision_count": len(portfolio_collisions),
            "collisions": portfolio_collisions,
            "semantic_review": "Every new safe-now, candidate, skill, runner, and cleanup title was reviewed for purpose, artifact, falsifier, compatibility, gate, and recovery distinctness; inherited evidence supplies no Orin completion credit.",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "provenance/rejected-candidate-register.json",
        {
            "schema": "ghc.family.v645-v6.rejected-candidates.v1",
            "phase": PHASE,
            "candidates": [
                {
                    "candidate_id": "V6456-REJECTED-P06-A",
                    "title": "CBR maritime-casualty VDR custody, seafarer protection, remedy, and Maori-authority reservation matrix",
                    "closest_prior": "V6455-P06",
                    "token_overlap": 0.529,
                    "reason": "The first candidate repeated the predecessor's occurrence-custody, reporter-protection, remedy, and authority structure too closely.",
                    "disposition": "rejected_before_x1_freeze",
                    "replacement": "V6456-P06",
                }
            ],
            "boundary": "Rejected candidates receive no proposal or completion credit and remain retained novelty evidence.",
        },
    )
    write_json(
        "approval-packets/x1-approval-portfolio.json",
        {
            "schema": "ghc.family.v645-v6.approval-portfolio.v1",
            "phase": PHASE,
            "owner": OWNER,
            "freeze_stage": "x1_only",
            "completion_credit_before_x2": 0,
            "counts": {"safe_now": len(SAFE_NOW), "candidates": len(CANDIDATES), "inherited_exact": len(inherited_exact), "inherited_blocked": len(inherited_blocked)},
            "predecessor_portfolio_review": "Sable portfolios are inherited evidence only. Orin designed new purpose, artifact, witness, and recovery surfaces after novelty, safety, compatibility, relevance, and gate review.",
            "safe_now": SAFE_NOW,
            "candidates": CANDIDATES,
            "inherited_exact_packets": inherited_exact,
            "inherited_blocked_packets": inherited_blocked,
            "inherited_packet_integrity": "Ten exact and five blocked packets are carried forward unchanged in meaning and remain non-executable without fresh evidence or authority.",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "prototypes/x1-skill-runner-plan.json",
        {
            "schema": "ghc.family.v645-v6.skill-runner-plan.v1",
            "phase": PHASE,
            "freeze_stage": "x1_only",
            "skills": [
                {"name": name, "description": description, "family_current_name": name.startswith("ghc-family-"), "x2_state": "preregistered_not_built_or_used", "protected_gates": ["authority", "real_data_or_participants", "production", "independent_reproduction"]}
                for name, description in SKILLS
            ],
            "runners": [
                {"name": name, "description": description, "family_current_name": name.startswith("ghc_family_") or name.startswith("build_ghc_family_"), "x2_state": "preregistered_not_built_or_used", "caller_compatibility": "new additive phase runner"}
                for name, description in RUNNERS
            ],
            "acceptance": "Every item must be built, structurally validated, actually invoked, and given a bounded passing witness in x2 or remain incomplete.",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write_json(
        "maintenance/x1-clean-refine-plan.json",
        {
            "schema": "ghc.family.v645-v6.clean-refine-plan.v1",
            "phase": PHASE,
            "freeze_stage": "x1_only",
            "tasks": CLEAN_TASKS,
            "destructive_task_count": 0,
            "completion_credit_before_x2": 0,
            "boundary": "Cleanup is additive, owner-scoped, non-destructive, compatible, and incomplete until its x2 receipt passes.",
        },
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v645-v6.source-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "allowed_statuses": ["current", "stable", "draft", "watch"],
            "sources": SOURCES,
            "real_data_rows_ingested": 0,
            "likelihood_evaluations": 0,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    source_lines = ["# v645-v6 source ledger", "", "Current primary and official sources are used only for the bounded purpose recorded here.", ""]
    for row in SOURCES:
        target = f" — {row['url']}" if row.get("url") else ""
        source_lines.append(f"- {row['source_id']} [{row['status']}] {row['title']} ({row['authority']}){target}; use: {row['use']}.")
    source_lines.extend(["", TRUTH_BOUNDARY])
    write_text("sources/source-ledger.md", "\n".join(source_lines))
    write_json(
        "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v645-v6.startup.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source": {"branch": "codex/GHC-Family/sable-rook-full-tools", "revision": SOURCE_REVISION, "seal_revision": SOURCE_SEAL_REVISION, "x1_revision": SOURCE_X1_REVISION, "evidence_revision": SOURCE_EVIDENCE_REVISION, "phase": SOURCE_PHASE},
            "source_verification": {"local_upstream_tracking_live_equal": True, "clean": True, "seal_ancestral": True, "three_single_parent_phase_commits": True, "merge_commits": 0, "final_parent_is_evidence": True},
            "orin_lane": {"branch": "codex/GHC-Family/orin-thale-v642-v6-full-tools", "continued_existing_lane": True, "fast_forward_only": True, "source_revision_after_fast_forward": SOURCE_REVISION, "merge_commit_created": False, "clean_before": True},
            "active_owner": OWNER,
            "standby_siblings_contacted": [],
            "x1_scope": "exactly ten core proposals plus new safe-now, candidate, skill, runner, and cleanup portfolios",
            "x2_scope": "not started",
            "storage": {"primary_drive": "D", "free_bytes_observed": 591383392256, "full_checkout_file_count": 33069, "tracked_file_count": 32940, "owner_generated_v645_v6_file_count_before_x1": 0, "rotation_threshold": 15000, "threshold_applies_to": "new_orin_generated_files_only"},
            "boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "environment/version-receipt.json",
        {
            "schema": "ghc.family.v645-v6.version-receipt.v1",
            "observed_on": "2026-07-16",
            "codex_cli": {"local": "0.144.4", "official_release": "0.144.4", "source_id": "S22", "action": "verified_only_no_update"},
            "codex_desktop": {"local": "26.707.9981.0", "package_status": "Ok", "public_exact_build_correlation": "not_claimed", "action": "verified_only_no_update"},
            "python": "3.12.10",
            "git": "2.55.0.windows.2",
            "host_actions": {"desktop_updated": False, "elevated": False, "security_weakened": False, "windows_feature_changed": False, "rebooted": False},
            "boundary": "Version observation does not prove full environment equivalence, security, support, or production readiness.",
        },
    )
    write_json(
        "environment/sandbox-readonly-audit.json",
        {
            "schema": "ghc.family.v645-v6.sandbox-audit.v1",
            "query": "ordinary read-only optional-feature status plus executable lookup",
            "feature_query": "unavailable_without_elevation",
            "executable": "not_found",
            "sandbox_launched": False,
            "elevation": False,
            "feature_changed": False,
            "host_security_changed": False,
            "installed": False,
            "rebooted": False,
            "retained_negative_id": "V6456-X1-N03",
            "disposition": "open_environment_gap",
        },
    )
    write_json(
        "environment/rotation-guard.json",
        {
            "schema": "ghc.family.v645-v6.rotation-guard.v1",
            "full_checkout_file_count": 33069,
            "tracked_file_count": 32940,
            "owner_generated_before_x1": 0,
            "threshold": 15000,
            "threshold_scope": "new_orin_generated_addition",
            "rotate_due_to_inherited_baseline": False,
            "boundary": "The inherited full checkout exceeds 15,000 files; that baseline is not a rotation trigger.",
        },
    )
    write_json(
        "focus/primary-focus-receipt.json",
        {
            "schema": "ghc.family.v645-v6.focus.v1",
            "primary_trinity_pillar": PRIMARY_FOCUS,
            "other_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "bounded_human_practice": BOUNDED_PRACTICE,
            "practice_use": "learning and design lens only",
            "not_claimed": ["employment", "licensure", "professional competence", "maritime authority", "investigation authority", "legal authority", "cultural authority", "Maori authority", "affected-party authorization"],
            "boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "orchestration/phase-update.json",
        {
            "schema": "ghc.family.phase-update.v1",
            "phase": PHASE,
            "owner": OWNER,
            "state": "x1_frozen_pending_commit_and_remote_equality",
            "active": [OWNER],
            "standby": ["Sable Rook", "Ilyra Fen", "Eiren Kestrel", "Tamar Vey", "Sylven Arc", "all other siblings"],
            "no_task_creation": True,
            "no_delegation": True,
            "x2_started": False,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        "orchestration/terminal-route-plan.json",
        {
            "schema": "ghc.family.v645-v6.route-plan.v1",
            "current_state": "PREPARED_NOT_SENT",
            "target_title": "Tamar Vey",
            "target_phase": "v645-v7",
            "send_count": 0,
            "preconditions": ["x2 closeout committed and pushed", "commit cap satisfied", "canonical exact-final scoped validation passed", "one named-lane replay passed", "four-way equality proven", "exact existing target resolved read-only"],
            "privacy": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths may enter the baton.",
        },
    )
    negatives = []
    for incident in INCIDENTS:
        n = incident["number"]
        record = method_record(incident)
        failed = witness(incident, "fail")
        passed = witness(incident, "pass")
        write_json(f"method-flow/v6456-m{n:02d}-method-record.json", record)
        write_json(f"method-flow/v6456-w{n:02d}-f-witness.json", failed)
        write_json(f"method-flow/v6456-w{n:02d}-p-witness.json", passed)
        negatives.append(
            {
                "negative_id": f"V6456-X1-N{n:02d}",
                "stage": "x1",
                "class": "operational",
                "summary": incident["negative"],
                "retained": True,
                "recovered": True,
                "method_id": record["method_id"],
                "failed_witness_id": failed["witness_id"],
                "passing_witness_id": passed["witness_id"],
                "side_effect_budget": incident["side_effect_budget"],
                "independent_reproduction": False,
            }
        )
    write_json(
        "validation/x1-operational-negatives.json",
        {
            "schema": "ghc.family.v645-v6.operational-negatives.v1",
            "phase": PHASE,
            "stage": "x1",
            "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
            "preregistered_synthetic": PREREGISTERED_SYNTHETIC_NEGATIVES,
            "new_operational_count": len(negatives),
            "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + PREREGISTERED_SYNTHETIC_NEGATIVES + len(negatives),
            "negatives": negatives,
            "boundary": "Counts preserve failures; recovered does not mean erased or converted to independent evidence.",
        },
    )
    write_text(
        "wellbeing-check.md",
        """# v645-v6 x1 wellbeing and workload check

- Scope is bounded to one owner, one canonical lane, one later named replay, at most four phase commits, and no full repository suite.
- The first broad Git probe was stopped at its bound and decomposed; no unbounded retry loop was used.
- The workload is split by the x1 freeze. No x2 evidence or outcome credit is present here.
- Windows Sandbox remains unavailable without elevation; no host change was attempted.
- Identity and family language remains relational working language only, not a welfare, consciousness, employment, or authority claim.
""",
    )
    print(json.dumps({"phase": PHASE, "prior_proposals": len(prior), "new_proposals": len(PROPOSALS), "x1_operational_negatives": len(negatives), "phase_directory": PHASE_REL.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
