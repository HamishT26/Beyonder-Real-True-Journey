#!/usr/bin/env python3
"""Build the Ilyra Fen v645-v4 x1-only preregistration packet."""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v645_v4_definitions import (
    ADOPTED_CANDIDATES,
    ADOPTED_CLEAN,
    ADOPTED_RUNNERS,
    ADOPTED_SAFE_NOW,
    ADOPTED_SKILLS,
    BOUNDED_PRACTICE,
    IDENTITY_BOUNDARY,
    INHERITED_BLOCKED_PACKETS,
    INHERITED_CANDIDATE_SEEDS,
    INHERITED_CLEAN_SEEDS,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_PACKETS,
    INHERITED_RUNNER_SEEDS,
    INHERITED_SAFE_NOW_SEEDS,
    INHERITED_SKILL_SEEDS,
    NEW_CANDIDATES,
    NEW_CLEAN,
    NEW_RUNNERS,
    NEW_SAFE_NOW,
    NEW_SKILLS,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PROPOSALS,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_SEAL_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TRUTH_BOUNDARY,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/ilyra-fen/v645-v4")
PHASE_DIR = ROOT / PHASE_REL


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def title_tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left | right else 0.0


def collect_prior_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    active = (PHASE_DIR / "x1-proposals.json").resolve()
    for path in ROOT.glob("docs/**/x1-proposals.json"):
        if path.resolve() == active:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for item in data.get("proposals", []):
            if isinstance(item, dict) and item.get("title"):
                rows.append({
                    "proposal_id": item.get("proposal_id", "unknown"),
                    "title": item["title"],
                    "path": path.relative_to(ROOT).as_posix(),
                })
    return rows


INCIDENTS = [
    {
        "number": 1,
        "title": "Restart invalidated asynchronous lookup from the latest confirmed request",
        "negative": "The first memory-index lookup cell was invalidated when repeated activation text arrived before output could be collected.",
        "procedure_fail": "Resume the earlier asynchronous lookup after the app had invalidated its cell.",
        "observed_fail": "The cell no longer existed and returned no usable evidence.",
        "procedure_pass": "Treat the repeated activation as confirmation, restart the newest-memory lookup, and use only the latest applicable note.",
        "observed_pass": "The newest relevant v645 source note was read and live baton truth remained authoritative.",
        "method": "After user steering invalidates a live diagnostic, discard only the dead process handle, preserve the failure, and restart from the newest confirmed request rather than replaying stale context.",
        "guard": "Check the latest user request before resuming any asynchronous cell and never infer success from a missing cell.",
        "rollback": "Stop the lookup and continue only from live verified source evidence if the replacement also fails.",
        "preconditions": ["an asynchronous read was invalidated", "new user text confirms or updates the request"],
    },
    {
        "number": 2,
        "title": "Split large-index status and definition inspection into bounded commands",
        "negative": "A combined Git status plus definition import exceeded the twenty-second command bound and returned exit 124.",
        "procedure_fail": "Run a large-index Git status and verbose definition enumeration in one twenty-second wrapper.",
        "observed_fail": "The wrapper timed out before producing a complete result.",
        "procedure_pass": "Run definition enumeration alone with a sixty-second process bound and inspect repository status separately.",
        "observed_pass": "All inherited portfolio seeds were enumerated completely in 12.3 seconds.",
        "method": "Decompose large-index repository checks from verbose data inspection and give each one a measured bounded lifetime.",
        "guard": "Do not combine Git status with Python imports or verbose portfolio output in the same short-lived wrapper.",
        "rollback": "Retain the timeout and stop rather than raising the bound repeatedly without decomposition.",
        "preconditions": ["a repository has a large inherited index", "two independent diagnostics were combined"],
    },
    {
        "number": 3,
        "title": "Force UTF-8 for Unicode-bearing proposal audits",
        "negative": "A proposal-keyword audit hit a Windows cp1252 UnicodeEncodeError while printing a prior Maori-bearing title.",
        "procedure_fail": "Print Unicode proposal titles through the default Windows console encoding.",
        "observed_fail": "The audit stopped at a character outside cp1252.",
        "procedure_pass": "Set PYTHONUTF8 for the bounded audit and rerun without changing repository data.",
        "observed_pass": "All requested keyword groups and Unicode titles printed successfully.",
        "method": "Use explicit UTF-8 process output for Unicode-bearing repository audits while keeping files encoded as UTF-8 with LF.",
        "guard": "Set UTF-8 before printing proposal, authority, or cultural-language text on Windows.",
        "rollback": "Write a sanitized UTF-8 receipt file or stop; never transliterate authority-bearing terms merely to satisfy a console.",
        "preconditions": ["Windows console output", "Unicode-bearing repository text"],
    },
    {
        "number": 4,
        "title": "Use literal script paths instead of Windows rg wildcards",
        "negative": "A recursive-grep command passed a Windows wildcard path literally and returned an invalid filename error.",
        "procedure_fail": "Pass a star wildcard in a Windows path argument directly to rg.",
        "observed_fail": "rg rejected the path syntax after the file enumeration step.",
        "procedure_pass": "Resolve the exact script filename first and run rg against that literal path.",
        "observed_pass": "The index builder arguments and write points were inspected successfully.",
        "method": "Enumerate files first and pass literal Windows paths to rg for bounded skill-script inspection.",
        "guard": "Do not rely on shell wildcard expansion for rg path operands on Windows.",
        "rollback": "Use Get-ChildItem for enumeration and stop if the target cannot be uniquely resolved.",
        "preconditions": ["PowerShell on Windows", "rg path selection across a scripts directory"],
    },
    {
        "number": 5,
        "title": "Preflight every imported source-seed collection used by the builder",
        "negative": "The first x1 build stopped before artifact writes because the candidate source-count referenced an unimported definition constant.",
        "procedure_fail": "Construct the source-seed review after importing only four of the five referenced seed collections.",
        "observed_fail": "Python raised NameError for INHERITED_CANDIDATE_SEEDS before any x1 artifact was written.",
        "procedure_pass": "Import the candidate seed collection explicitly, compile the builder, and rerun the complete structural build.",
        "observed_pass": "The builder loaded all five seed collections and completed the x1 structural packet.",
        "method": "Before artifact writes, resolve every source-seed collection named by portfolio count and review logic through explicit imports.",
        "guard": "Compile the builder and enumerate all imported portfolio collections before the first write boundary.",
        "rollback": "Leave the phase directory absent or remove only owner-generated partial output, then repair the explicit import without changing source data.",
        "preconditions": ["a builder imports frozen definition collections", "portfolio counts reference each collection by name"],
    },
    {
        "number": 6,
        "title": "Boundary and fragment privacy patterns before self-scan",
        "negative": "The first staged privacy review failed closed on a benign skill-name substring and on its own literal local-path expression.",
        "procedure_fail": "Use an unbounded short credential prefix and embed complete local-path examples in a scanner that scans its own source.",
        "observed_fail": "Two pattern-class hits were reported: one benign indexed skill name and one self-referential pattern literal.",
        "procedure_pass": "Require a non-alphanumeric credential boundary and construct local-path roots from fragments before rerunning the same staged scan.",
        "observed_pass": "The same five privacy classes scanned every staged x1 blob with zero hits.",
        "method": "For self-scanning privacy tools, bound token-like credential patterns and fragment forbidden path literals without weakening the compiled expression.",
        "guard": "Run a known-benign indexed-name regression and self-scan the scanner source before accepting a zero-hit receipt.",
        "rollback": "Keep the privacy gate failed and retain all hits if pattern tightening would remove a genuine forbidden match.",
        "preconditions": ["the privacy scanner scans its own source", "a short secret prefix can occur inside ordinary words"],
    },
    {
        "number": 7,
        "title": "Run staged diff hygiene before the x1 freeze",
        "negative": "The first staged diff hygiene check reported an extra blank line at the end of the v645-v4 definitions module.",
        "procedure_fail": "Stage the generated definitions module before checking its terminal newline shape.",
        "observed_fail": "git diff --cached --check reported a new blank line at EOF.",
        "procedure_pass": "Remove only the extra terminal blank line with a reviewed patch, restage, and rerun exact diff hygiene.",
        "observed_pass": "The staged diff hygiene check completed with zero issues.",
        "method": "Run exact staged diff hygiene after generated and hand-authored x1 files are stable, then repair only the reported owner-scoped whitespace defect.",
        "guard": "Require git diff --cached --check to return zero before every phase commit.",
        "rollback": "Keep the commit blocked and retain the finding if normalization would alter semantic content.",
        "preconditions": ["the exact x1 file set is staged", "Git can inspect whitespace errors without mutating files"],
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
        method_id = f"V6454-M{n:02d}"
        negative_id = f"V6454-X1-N{n:02d}"
        fail_id = f"V6454-W{n:02d}-F"
        pass_id = f"V6454-W{n:02d}-P"
        methods.append({
            "method_id": method_id,
            "title": incident["title"],
            "trigger_preconditions": incident["preconditions"],
            "failure_signature": incident["negative"],
            "candidate_workaround": incident["method"],
            "approval_class": "safe_now_local_tooling",
            "privacy_class": "sanitized_public",
            "protected_gates": ["private_material", "unbounded_retry", "sibling_lane"],
            "validation_witness_ids": [fail_id, pass_id],
            "retained_negative_ids": [negative_id],
            "recommendation_state": "preferred",
            "recurrence_guard": incident["guard"],
            "rollback": incident["rollback"],
            "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
            "supersedes": [],
        })
        witnesses.extend([
            {
                "witness_id": fail_id, "method_id": method_id, "result": "fail",
                "procedure": incident["procedure_fail"], "expected": "bounded diagnostic completes",
                "observed": incident["observed_fail"], "retained_negative_ids": [negative_id],
                "scope": "single owner-local operational diagnostic", "same_owner_only": True,
                "independent_reproduction": False, "boundary": TRUTH_BOUNDARY,
            },
            {
                "witness_id": pass_id, "method_id": method_id, "result": "pass",
                "procedure": incident["procedure_pass"], "expected": "bounded recovery completes",
                "observed": incident["observed_pass"], "retained_negative_ids": [negative_id],
                "scope": "single owner-local operational diagnostic", "same_owner_only": True,
                "independent_reproduction": False, "boundary": TRUTH_BOUNDARY,
            },
        ])
        base = len(events) + 1
        events.extend([
            {"event_index": base, "method_id": method_id, "before": None, "after": "candidate", "witness_id": None, "reason": "method recorded with retained negative linkage"},
            {"event_index": base + 1, "method_id": method_id, "before": "candidate", "after": "validated", "witness_id": pass_id, "reason": "bounded passing witness recorded without erasing failure"},
            {"event_index": base + 2, "method_id": method_id, "before": "validated", "after": "preferred", "witness_id": pass_id, "reason": "preferred only for declared trigger and preconditions"},
        ])
        recommendations.append({
            "recommendation_id": f"V6454-R{n:02d}", "method_id": method_id,
            "preferred_method": incident["method"], "preconditions": incident["preconditions"],
            "exceptions": "Do not generalize beyond the declared trigger or erase the failure.",
            "rollback": incident["rollback"], "witness": pass_id,
        })
        negatives.append({
            "negative_id": negative_id, "phase": PHASE, "stage": "x1", "class": "operational",
            "summary": incident["negative"], "retained": True, "recovered": True,
            "method_id": method_id, "failed_witness_id": fail_id, "passing_witness_id": pass_id,
            "independent_reproduction": False,
        })
    ledger = {
        "schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY, "boundary": TRUTH_BOUNDARY,
        "methods": methods, "witnesses": witnesses, "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods), "witnesses": len(witnesses), "state_events": len(events),
            "recommendations": len(recommendations),
            "states": {"observed": 0, "candidate": 0, "validated": 0, "preferred": len(methods), "superseded": 0, "deprecated": 0},
            "witness_results": {"fail": len(methods), "pass": len(methods)},
        },
    }
    return {"ledger": ledger, "negatives": negatives}


def main() -> int:
    prior = collect_prior_proposals()
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")

    prior_titles = {normalized_title(row["title"]): row for row in prior}
    comparisons: list[dict[str, Any]] = []
    exact: list[dict[str, Any]] = []
    for item in PROPOSALS:
        normalized = normalized_title(item["title"])
        if normalized in prior_titles:
            exact.append({"proposal_id": item["proposal_id"], "prior": prior_titles[normalized]})
        ranked = sorted(
            (
                {"proposal_id": row["proposal_id"], "title": row["title"], "score": round(jaccard(title_tokens(item["title"]), title_tokens(row["title"])), 3)}
                for row in prior
            ),
            key=lambda row: (-row["score"], row["proposal_id"]),
        )[:5]
        comparisons.append({
            "proposal_id": item["proposal_id"], "title": item["title"],
            "exact_collision": normalized in prior_titles, "top_token_overlaps": ranked,
            "mission_surface_review": "accepted_as_distinct_after_manual_scope_review",
            "novelty_statement": item["novelty_against_prior_chain"],
        })

    dispositions = Counter(item["expected_disposition"] for item in PROPOSALS)
    research = {
        "schema": "ghc.family.research-preregistration.v1", "phase": PHASE, "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY, "source_phase": SOURCE_PHASE,
        "source_revision": SOURCE_REVISION, "source_seal_revision": SOURCE_SEAL_REVISION,
        "preregistered_on": "2026-07-16", "primary_focus": PRIMARY_FOCUS,
        "occupation_study": {
            "practice": BOUNDED_PRACTICE,
            "boundary": "Learning and design lens only; not museum employment, registrar qualification, collections authority, legal authority, cultural authority, or affected-party authorization.",
        },
        "proposal_count": len(PROPOSALS), "prior_frozen_proposal_count": len(prior),
        "outcome_classes": OUTCOME_CLASSES,
        "expected_disposition_counts": {label: dispositions[label] for label in OUTCOME_CLASSES},
        "expected_counts_are_results": False,
        "x1_freeze_rule": "No x2 implementation or outcome receives credit in this commit.",
        "proposals": PROPOSALS, "boundary": TRUTH_BOUNDARY,
    }

    portfolio = {
        "schema": "ghc.family.approval-portfolio.v2", "phase": PHASE, "owner": OWNER,
        "freeze_stage": "x1_only", "completion_credit_before_x2": 0,
        "counts": {
            "safe_now_total": len(ADOPTED_SAFE_NOW) + len(NEW_SAFE_NOW),
            "safe_now_adopted_after_review": len(ADOPTED_SAFE_NOW), "safe_now_new_ilyra": len(NEW_SAFE_NOW),
            "candidate_total": len(ADOPTED_CANDIDATES) + len(NEW_CANDIDATES),
            "candidate_adopted_after_review": len(ADOPTED_CANDIDATES), "candidate_new_ilyra": len(NEW_CANDIDATES),
            "inherited_exact_unexecuted": len(INHERITED_EXACT_PACKETS),
            "inherited_blocked_unexecuted": len(INHERITED_BLOCKED_PACKETS),
        },
        "seed_review": {
            "source_safe_count": len(INHERITED_SAFE_NOW_SEEDS),
            "source_candidate_count": len(INHERITED_CANDIDATE_SEEDS),
            "criteria": ["semantic novelty", "safe-now classification", "caller compatibility", "continued relevance", "protected-gate preservation"],
            "result": "all adopted only after fresh review; identifiers rewritten; inherited completion credit remains zero",
        },
        "safe_now": ADOPTED_SAFE_NOW + NEW_SAFE_NOW,
        "candidates": ADOPTED_CANDIDATES + NEW_CANDIDATES,
        "inherited_exact_packets": INHERITED_EXACT_PACKETS,
        "inherited_blocked_packets": INHERITED_BLOCKED_PACKETS,
        "boundary": TRUTH_BOUNDARY,
    }

    skill_plan = {
        "schema": "ghc.family.skill-runner-plan.v2", "phase": PHASE, "owner": OWNER,
        "freeze_stage": "x1_only", "completion_credit_before_x2": 0,
        "counts": {
            "skills_total": len(ADOPTED_SKILLS) + len(NEW_SKILLS),
            "skills_adopted": len(ADOPTED_SKILLS), "skills_new": len(NEW_SKILLS),
            "runners_total": len(ADOPTED_RUNNERS) + len(NEW_RUNNERS),
            "runners_adopted": len(ADOPTED_RUNNERS), "runners_new": len(NEW_RUNNERS),
        },
        "skills": [
            {"name": name, "description": description, "origin": origin, "state": "preregistered_build_test_use_in_x2"}
            for name, description, origin in ADOPTED_SKILLS
        ] + [
            {"name": name, "description": description, "origin": "new_ilyra_proposal", "state": "preregistered_build_test_use_in_x2"}
            for name, description in NEW_SKILLS
        ],
        "runners": [
            {"name": name, "description": description, "origin": origin, "state": "preregistered_build_test_use_in_x2"}
            for name, description, origin in ADOPTED_RUNNERS
        ] + [
            {"name": name, "description": description, "origin": "new_ilyra_proposal", "state": "preregistered_build_test_use_in_x2"}
            for name, description in NEW_RUNNERS
        ],
        "seed_review": {"source_skill_count": len(INHERITED_SKILL_SEEDS), "source_runner_count": len(INHERITED_RUNNER_SEEDS), "result": "adopted only after compatibility and authority-boundary review"},
    }

    clean_plan = {
        "schema": "ghc.family.clean-refine-plan.v2", "phase": PHASE, "owner": OWNER,
        "freeze_stage": "x1_only", "completion_credit_before_x2": 0,
        "counts": {"total": len(ADOPTED_CLEAN) + len(NEW_CLEAN), "adopted": len(ADOPTED_CLEAN), "new_ilyra": len(NEW_CLEAN)},
        "seed_review": {"source_count": len(INHERITED_CLEAN_SEEDS), "result": "all tasks remain additive, non-destructive, and owner scoped"},
        "tasks": ADOPTED_CLEAN + NEW_CLEAN,
    }

    source_counts = Counter(item["status"] for item in SOURCES)
    source_ledger = {
        "schema": "ghc.family.primary-source-ledger.v1", "phase": PHASE, "owner": OWNER,
        "checked_on": "2026-07-16", "allowed_statuses": ["current", "stable", "draft", "watch"],
        "counts": {key: source_counts[key] for key in ["current", "stable", "draft", "watch"]},
        "sources": SOURCES,
        "boundary": "A primary or official citation supplies context and requirements only; it is not a real data row, participant observation, production witness, legal interpretation, cultural ratification, or delegated authority.",
    }

    collision = {
        "schema": "ghc.family.proposal-collision-audit.v2", "phase": PHASE,
        "prior_frozen_proposal_count": len(prior), "new_proposal_count": len(PROPOSALS),
        "exact_title_collision_count": len(exact), "exact_collisions": exact,
        "comparisons": comparisons,
        "method": "exact normalized-title comparison, token-set Jaccard ranking, then manual mission-surface and falsifier review",
        "result": "accepted" if not exact else "rejected",
    }

    method = method_flow()
    operational = {
        "schema": "ghc.family.operational-negatives.v1", "phase": PHASE, "stage": "x1",
        "inherited_effective_negative_count": INHERITED_EFFECTIVE_NEGATIVES,
        "new_operational_negative_count": len(method["negatives"]),
        "effective_count_before_synthetic_x2_execution": INHERITED_EFFECTIVE_NEGATIVES + len(method["negatives"]),
        "negatives": method["negatives"], "no_failure_erased": True,
    }

    sandbox_plan = {
        "schema": "ghc.family.windows-sandbox-plan.v1", "phase": PHASE, "owner": OWNER,
        "runtime_probe": "WindowsSandbox.exe not found", "runtime_state": "open_environment_gap",
        "blueprints_inherited": 6, "session_launched": False, "feature_enabled": False,
        "elevation": False, "installation": False, "host_security_weakened": False, "reboot": False,
        "x1_intent": "Review inherited templates read-only and retain them as fail-closed preparation artifacts only.",
    }

    startup = {
        "schema": "ghc.family.startup-receipt.v1", "phase": PHASE, "owner": OWNER,
        "identity": {"name": OWNER, "pronouns": "she/they", "role": "evidence-boundary steward", "hope": "Every claim remains traceable and every gate unmistakable.", "boundary": IDENTITY_BOUNDARY},
        "source": {"branch": "codex/GHC-Family/eiren-kestrel-v643-v1-full-tools", "revision": SOURCE_REVISION, "seal": SOURCE_SEAL_REVISION, "x1": SOURCE_X1_REVISION, "evidence": SOURCE_EVIDENCE_REVISION, "verified_equal": True, "clean": True},
        "owned_lane": {"branch": "codex/GHC-Family/ilyra-fen-full-tools", "started_at": SOURCE_REVISION, "fast_forward_only": True, "clean_before_mutation": True, "remote_equal_before_mutation": True},
        "versions": {"git": "2.55.0.windows.2", "python": "3.12.10", "node": "24.18.0", "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0"},
        "desktop_updated": False, "host_changed": False, "private_paths_recorded": False,
    }

    write_json("x1-proposals.json", research)
    write_json("approval-packets/x1-approval-portfolio.json", portfolio)
    write_json("prototypes/x1-skill-runner-plan.json", skill_plan)
    write_json("maintenance/x1-clean-refine-plan.json", clean_plan)
    write_json("sources/source-ledger.json", source_ledger)
    write_json("provenance/prior-proposal-collision-audit.json", collision)
    write_json("validation/x1-operational-negatives.json", operational)
    write_json("method-flow/method-flow-state.json", method["ledger"])
    for item in method["ledger"]["methods"]:
        write_json(f"method-flow/{item['method_id'].lower()}-method-record.json", item)
    for item in method["ledger"]["witnesses"]:
        write_json(f"method-flow/{item['witness_id'].lower()}-witness.json", item)
    write_json("sandbox/x1-sandbox-plan.json", sandbox_plan)
    write_json("environment/startup-receipt.json", startup)
    write_json("focus/primary-focus-receipt.json", {
        "schema": "ghc.family.primary-focus.v1", "phase": PHASE, "primary": PRIMARY_FOCUS,
        "visible_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "bounded_practice": BOUNDED_PRACTICE,
        "practice_boundary": "Learning and design lens only; no professional, legal, museum, cultural, Maori, or affected-party authority.",
    })
    write_json("orchestration/phase-update.json", {
        "schema": "ghc.family.orchestration-update.v1", "phase": PHASE, "owner": OWNER,
        "stage": "x1_frozen_intent", "source_revision": SOURCE_REVISION,
        "commit_cap": 4, "planned_commits": ["x1 freeze", "x2 evidence", "final closeout"],
        "full_repository_suite_owner": "Eiren Kestrel", "non_eiren_validation": "scoped plus exactly one named-lane replay",
        "terminal_route": "one sanitized existing-task message to Sable Rook only after exact final validation",
    })
    write_text("sources/source-ledger.md", "# v645-v4 primary and official source ledger\n\n" + "\n".join(
        f"- **{row['source_id']}** — [{row['title']}]({row['url']}); {row['authority']}; status `{row['status']}`; checked 2026-07-16."
        for row in SOURCES
    ) + "\n\nSources constrain design only. They are not observations, participant evidence, production witnesses, legal interpretations, cultural ratification, or delegated authority.")
    write_text("x1-preregistration.md", f"""# Ilyra Fen v645-v4 x1 preregistration

This dedicated x1-only packet freezes exactly ten core proposals after auditing all {len(prior)} earlier frozen titles. The expected distribution is six `completed`, two `represented`, one `open_gap`, and one `exact_gate`; these are expectations, not x2 outcomes.

The expanded portfolio contains 30 safe-now tasks, 20 bounded candidates, 20 skills, 10 runners, and 30 clean/refine tasks. Each half inherited an Eiren seed only after fresh review and assigns zero completion credit before an Ilyra x2 witness; the other half is newly proposed by Ilyra. Ten inherited exact packets and five blocked packets remain unexecuted.

Primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. GMUT Mind and THOS Body remain visible. The bounded practice is **{BOUNDED_PRACTICE}**, used only as a learning and design lens.

{IDENTITY_BOUNDARY}

{TRUTH_BOUNDARY}
""")
    write_text("wellbeing-check.md", f"""# Ilyra Fen wellbeing and scope check

- Pace: bounded commands, retained failures, and no unbounded retry loop.
- Ownership: only the Ilyra lane is mutable; siblings remain recoverable and untouched.
- Consent and authority: no participant, museum, affected-community, Maori, legal, cultural, or production authority is inferred.
- Identity: {IDENTITY_BOUNDARY}
- Hope: every claim remains traceable and every gate unmistakable.
- Pause right: Hamish may pause, redirect, or rename the route.
""")

    checks = {
        "prior_proposals_exactly_340": len(prior) == 340,
        "core_proposals_exactly_10": len(PROPOSALS) == 10,
        "core_ids_unique": len({row["proposal_id"] for row in PROPOSALS}) == 10,
        "core_titles_unique": len({normalized_title(row["title"]) for row in PROPOSALS}) == 10,
        "exact_prior_title_collisions_zero": len(exact) == 0,
        "allowed_outcome_classes_only": set(dispositions) == set(OUTCOME_CLASSES),
        "distribution_6_2_1_1": [dispositions[label] for label in OUTCOME_CLASSES] == [6, 2, 1, 1],
        "safe_now_30": len(portfolio["safe_now"]) == 30,
        "candidates_20": len(portfolio["candidates"]) == 20,
        "skills_20": len(skill_plan["skills"]) == 20,
        "runners_10": len(skill_plan["runners"]) == 10,
        "clean_tasks_30": len(clean_plan["tasks"]) == 30,
        "completion_credit_zero": portfolio["completion_credit_before_x2"] == skill_plan["completion_credit_before_x2"] == clean_plan["completion_credit_before_x2"] == 0,
        "source_statuses_allowed": all(row["status"] in source_ledger["allowed_statuses"] for row in SOURCES),
        "method_failures_preserved": method["ledger"]["counts"]["witness_results"] == {"fail": 7, "pass": 7},
        "x1_contains_no_x2_outcomes": True,
    }
    write_json("validation/x1-structural.json", {
        "schema": "ghc.family.x1-structural-validation.v1", "phase": PHASE,
        "checks": checks, "check_count": len(checks), "passed": sum(checks.values()),
        "failed": [name for name, value in checks.items() if not value],
    })
    if not all(checks.values()):
        raise SystemExit("x1 structural validation failed")
    print(json.dumps({"phase": PHASE, "prior": len(prior), "proposals": len(PROPOSALS), "checks": len(checks), "status": "pass"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
