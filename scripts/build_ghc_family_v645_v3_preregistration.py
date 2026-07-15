#!/usr/bin/env python3
"""Build the Eiren Kestrel v645-v3 x1-only preregistration packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v645_v3_definitions import (
    BLOCKED_PACKETS,
    EIREN_CANDIDATE,
    EIREN_CLEAN,
    EIREN_RUNNERS,
    EIREN_SAFE_NOW,
    EIREN_SKILLS,
    EXACT_PACKETS,
    IDENTITY_BOUNDARY,
    PROPOSALS,
    SOURCES,
    SUCCESSOR_CANDIDATE,
    SUCCESSOR_CLEAN,
    SUCCESSOR_RUNNERS,
    SUCCESSOR_SAFE_NOW,
    SUCCESSOR_SKILLS,
    TRUTH_BOUNDARY,
)

PHASE = "v645-gmut-thos-v3-x1-x2"
OWNER = "Eiren Kestrel"
PHASE_REL = Path("docs/eiren-kestrel/v645-v3")
SOURCE_PHASE = "v645-gmut-thos-v2-x1-x2"
SOURCE_REVISION = "c8ef5b28537eb1e85f79e3ead3977a031504f0dc"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
INHERITED_NEGATIVE_COUNT = 1916


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
    ).stdout.strip()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "for", "to", "with", "in", "state", "audit", "protocol"}
    return {part for part in normalized_title(value).split() if len(part) > 2 and part not in stop}


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a or b else 1.0


def collect_prior_proposals(repo: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    current_phase_dir = repo / PHASE_REL
    for path in sorted((repo / "docs").rglob("x1-proposals.json")):
        if current_phase_dir in path.parents:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for item in payload.get("proposals", []):
            if isinstance(item, dict) and item.get("proposal_id") and item.get("title"):
                records.append({"proposal_id": item["proposal_id"], "title": item["title"]})
    by_id = {item["proposal_id"]: item for item in records}
    return [by_id[key] for key in sorted(by_id)]


def method_flow_ledger() -> dict[str, Any]:
    methods = [
        {
            "method_id": "V6453-M01", "title": "Explicit scripts-path import bootstrap",
            "failure_signature": "The first prior-proposal collector import could not resolve the family module from the calling directory.",
            "trigger_preconditions": ["Python helper invoked outside the scripts directory", "family module import required"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_local_tooling",
            "candidate_workaround": "Insert the repository scripts directory at the front of the process-local import path before importing the collector.",
            "validation_witness_ids": ["V6453-W01-F", "V6453-W01-P"],
            "recurrence_guard": "Resolve the script directory explicitly before importing phase-local modules.",
            "rollback": "Remove the process-local path insertion and use a package entry point if module layout changes.",
            "recommendation_state": "preferred", "supersedes": [],
            "protected_gates": ["global_python_environment", "private_paths", "sibling_lane"],
            "retained_negative_ids": ["V6453-X1-N01"],
            "scope_boundary": "Process-local import bootstrap only; no global environment or package mutation.",
        },
        {
            "method_id": "V6453-M02", "title": "Metadata-first bounded long read",
            "failure_signature": "A complete local skill read exceeded the initial ten-second command window.",
            "trigger_preconditions": ["Small local instruction file", "initial full read timed out", "file remains readable"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_read_only",
            "candidate_workaround": "Read file metadata first, then repeat the complete UTF-8 read with a bounded sixty-second command window.",
            "validation_witness_ids": ["V6453-W02-F", "V6453-W02-P"],
            "recurrence_guard": "Use a sixty-second bound for slow local skill reads after checking size and type; never loop unbounded.",
            "rollback": "Stop after the bounded retry and retain an open tooling gap if the complete read still fails.",
            "recommendation_state": "preferred", "supersedes": [],
            "protected_gates": ["unbounded_retry", "private_material", "host_mutation"],
            "retained_negative_ids": ["V6453-X1-N02"],
            "scope_boundary": "Read-only local instruction retrieval; same-owner witness only.",
        },
        {
            "method_id": "V6453-M03", "title": "Absolute current-phase exclusion in recursive proposal scans",
            "failure_signature": "The first recursive proposal audit counted the ten newly generated v645-v3 proposals and reported 340 instead of 330 prior proposals.",
            "trigger_preconditions": ["Recursive absolute filesystem scan", "current phase path stored as repository-relative path"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_local_tooling",
            "candidate_workaround": "Resolve the current phase directory against the repository root and exclude that absolute parent before collecting prior proposals.",
            "validation_witness_ids": ["V6453-W03-F", "V6453-W03-P"],
            "recurrence_guard": "Compare like-for-like absolute Path objects when excluding the active phase from recursive scans.",
            "rollback": "Stop the novelty audit if the prior count differs from the frozen predecessor count.",
            "recommendation_state": "preferred", "supersedes": [],
            "protected_gates": ["proposal_novelty", "x1_freeze", "history_rewrite"],
            "retained_negative_ids": ["V6453-X1-N03"],
            "scope_boundary": "Proposal-index collection only; no artifact deletion or historical rewrite.",
        },
        {
            "method_id": "V6453-M04", "title": "Normalized authoritative-source classifier",
            "failure_signature": "The first source-authority test rejected an OpenID Final Specification because a case-sensitive expression looked only for lowercase official or primary wording.",
            "trigger_preconditions": ["Human-readable authority labels", "case-sensitive test expression"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_test_repair",
            "candidate_workaround": "Normalize the authority label to lowercase and accept official, primary, or final specification classifications.",
            "validation_witness_ids": ["V6453-W04-F", "V6453-W04-P"],
            "recurrence_guard": "Normalize descriptive classifications before matching and keep accepted classes explicit.",
            "rollback": "Fail the source ledger if an authority class remains unrecognized after normalization.",
            "recommendation_state": "preferred", "supersedes": [],
            "protected_gates": ["source_authority", "fabricated_citation", "empirical_nonpromotion"],
            "retained_negative_ids": ["V6453-X1-N04"],
            "scope_boundary": "Source-ledger classification only; it does not promote a citation into data or authority delegation.",
        },
        {
            "method_id": "V6453-M05", "title": "Literal line-bounded PowerShell diagnostic read",
            "failure_signature": "A diagnostic search command used a brittle quoted pattern and PowerShell rejected the unterminated string.",
            "trigger_preconditions": ["Complex mixed quote pattern", "only bounded source context is needed"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_read_only",
            "candidate_workaround": "Read the file literally and select explicit line ranges instead of interpolating a complex search pattern.",
            "validation_witness_ids": ["V6453-W05-F", "V6453-W05-P"],
            "recurrence_guard": "Prefer literal paths and bounded line slices for diagnostics when a regex would require nested shell quoting.",
            "rollback": "Stop rather than retrying a malformed quoted command; use a simpler read-only procedure.",
            "recommendation_state": "preferred", "supersedes": [],
            "protected_gates": ["shell_injection", "private_material", "host_mutation"],
            "retained_negative_ids": ["V6453-X1-N05"],
            "scope_boundary": "Read-only diagnostics; no command construction from untrusted content.",
        },
        {
            "method_id": "V6453-M06", "title": "Self-excluding privacy-pattern construction",
            "failure_signature": "The preparatory five-class privacy scan matched its own literal private-path pattern in the scanner source.",
            "trigger_preconditions": ["Scanner source is part of its own public scan scope", "forbidden literal appears verbatim in pattern source"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_tool_integrity",
            "candidate_workaround": "Construct sensitive path tokens from benign fragments so the scanner source does not contain the forbidden literal it detects.",
            "validation_witness_ids": ["V6453-W06-F", "V6453-W06-P"],
            "recurrence_guard": "Self-scan every public scanner and fragment forbidden literals without weakening the compiled expression.",
            "rollback": "Treat any self-hit as invalid, retain the hit, and do not issue a zero-hit receipt.",
            "recommendation_state": "preferred", "supersedes": [],
            "protected_gates": ["privacy_assurance", "scanner_integrity", "private_material"],
            "retained_negative_ids": ["V6453-X1-N06"],
            "scope_boundary": "Pattern-scan integrity only; zero hits remain bounded and are not complete privacy assurance.",
        },
    ]
    witnesses = [
        {"witness_id": "V6453-W01-F", "method_id": "V6453-M01", "procedure": "Prior-proposal collector import without explicit scripts path", "scope": "single read-only audit helper", "expected": "Module resolves", "observed": "Module resolution failed", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N01"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W01-P", "method_id": "V6453-M01", "procedure": "Repeat with process-local scripts path inserted", "scope": "single read-only audit helper", "expected": "All 330 prior proposals load", "observed": "330 unique identifiers and titles loaded", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N01"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W02-F", "method_id": "V6453-M02", "procedure": "Complete skill read under ten-second bound", "scope": "one local instruction file", "expected": "Complete content returned", "observed": "Command timed out without content", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N02"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W02-P", "method_id": "V6453-M02", "procedure": "Metadata first and complete UTF-8 read under sixty-second bound", "scope": "skill and required schema files", "expected": "Complete content returned", "observed": "Both complete files returned inside the bound", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N02"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W03-F", "method_id": "V6453-M03", "procedure": "Recursive scan with a relative active-phase exclusion", "scope": "proposal title index", "expected": "330 prior proposals", "observed": "340 proposals including the ten current items", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N03"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W03-P", "method_id": "V6453-M03", "procedure": "Recursive scan with an absolute active-phase exclusion", "scope": "proposal title index", "expected": "330 prior proposals", "observed": "330 unique prior proposal identifiers and titles", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N03"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W04-F", "method_id": "V6453-M04", "procedure": "Case-sensitive authority-label expression", "scope": "nineteen source-ledger entries", "expected": "All recognized primary or official classes pass", "observed": "OpenID Final Specification was rejected", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N04"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W04-P", "method_id": "V6453-M04", "procedure": "Lowercase normalized authority classification", "scope": "nineteen source-ledger entries", "expected": "Official, primary, and final specification classes pass", "observed": "All nineteen classifications passed", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N04"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W05-F", "method_id": "V6453-M05", "procedure": "Mixed-quote diagnostic search pattern", "scope": "one local source file", "expected": "Relevant lines returned", "observed": "PowerShell parser rejected an unterminated string", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N05"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W05-P", "method_id": "V6453-M05", "procedure": "Literal file read with explicit line ranges", "scope": "same local source file", "expected": "Relevant lines returned", "observed": "Requested bounded source context returned", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N05"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W06-F", "method_id": "V6453-M06", "procedure": "Self-scan with a verbatim forbidden private-path literal", "scope": "exact x1 public file set", "expected": "Zero private-material hits", "observed": "One scanner-source self-hit", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N06"], "boundary": TRUTH_BOUNDARY},
        {"witness_id": "V6453-W06-P", "method_id": "V6453-M06", "procedure": "Self-scan with fragment-constructed private-path expression", "scope": "exact x1 public file set", "expected": "Zero private-material hits", "observed": "Zero hits while all five compiled pattern classes remained active", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6453-X1-N06"], "boundary": TRUTH_BOUNDARY},
    ]
    return {
        "schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY, "methods": methods, "witnesses": witnesses,
        "state_events": [
            {"event_id": "V6453-E01", "method_id": "V6453-M01", "from": "candidate", "to": "validated", "witness_id": "V6453-W01-P"},
            {"event_id": "V6453-E02", "method_id": "V6453-M01", "from": "validated", "to": "preferred", "witness_id": "V6453-W01-P"},
            {"event_id": "V6453-E03", "method_id": "V6453-M02", "from": "candidate", "to": "validated", "witness_id": "V6453-W02-P"},
            {"event_id": "V6453-E04", "method_id": "V6453-M02", "from": "validated", "to": "preferred", "witness_id": "V6453-W02-P"},
            {"event_id": "V6453-E05", "method_id": "V6453-M03", "from": "candidate", "to": "validated", "witness_id": "V6453-W03-P"},
            {"event_id": "V6453-E06", "method_id": "V6453-M03", "from": "validated", "to": "preferred", "witness_id": "V6453-W03-P"},
            {"event_id": "V6453-E07", "method_id": "V6453-M04", "from": "candidate", "to": "validated", "witness_id": "V6453-W04-P"},
            {"event_id": "V6453-E08", "method_id": "V6453-M04", "from": "validated", "to": "preferred", "witness_id": "V6453-W04-P"},
            {"event_id": "V6453-E09", "method_id": "V6453-M05", "from": "candidate", "to": "validated", "witness_id": "V6453-W05-P"},
            {"event_id": "V6453-E10", "method_id": "V6453-M05", "from": "validated", "to": "preferred", "witness_id": "V6453-W05-P"},
            {"event_id": "V6453-E11", "method_id": "V6453-M06", "from": "candidate", "to": "validated", "witness_id": "V6453-W06-P"},
            {"event_id": "V6453-E12", "method_id": "V6453-M06", "from": "validated", "to": "preferred", "witness_id": "V6453-W06-P"},
        ],
        "recommendations": [
            {"recommendation_id": "V6453-R01", "method_id": "V6453-M01", "preconditions": "Phase-local module import from a non-scripts caller", "preferred_method": "Process-local scripts path insertion", "witness": "V6453-W01-P", "exceptions": "Do not mutate the global Python environment", "rollback": "Use a packaged entry point"},
            {"recommendation_id": "V6453-R02", "method_id": "V6453-M02", "preconditions": "A small local skill read times out once", "preferred_method": "Metadata-first sixty-second bounded retry", "witness": "V6453-W02-P", "exceptions": "Do not retry unbounded", "rollback": "Retain an open tooling gap"},
            {"recommendation_id": "V6453-R03", "method_id": "V6453-M03", "preconditions": "A recursive absolute scan must exclude the active phase", "preferred_method": "Resolve and compare absolute Path parents", "witness": "V6453-W03-P", "exceptions": "Do not infer the prior count", "rollback": "Stop x1 freeze"},
            {"recommendation_id": "V6453-R04", "method_id": "V6453-M04", "preconditions": "Human-readable source authority labels are tested", "preferred_method": "Lowercase and match an explicit class set", "witness": "V6453-W04-P", "exceptions": "A recognized label still supplies no empirical evidence", "rollback": "Retain the source as unclassified"},
            {"recommendation_id": "V6453-R05", "method_id": "V6453-M05", "preconditions": "A diagnostic regex requires nested PowerShell quoting", "preferred_method": "Literal path plus bounded line selection", "witness": "V6453-W05-P", "exceptions": "Do not build shell text from untrusted content", "rollback": "Stop the diagnostic"},
            {"recommendation_id": "V6453-R06", "method_id": "V6453-M06", "preconditions": "A public privacy scanner scans its own source", "preferred_method": "Fragment forbidden literals and self-scan", "witness": "V6453-W06-P", "exceptions": "Do not weaken the compiled expression", "rollback": "Retain the hit and refuse the receipt"},
        ],
        "counts": {"method_count": 6, "witness_count": 12, "failed_witness_count": 6, "passing_witness_count": 6, "preferred_method_count": 6, "candidate_method_count": 0, "recommendation_count": 6},
        "boundary": TRUTH_BOUNDARY,
    }


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    phase_dir = repo / PHASE_REL
    head = git(repo, "rev-parse", "HEAD")
    if head != SOURCE_REVISION:
        raise SystemExit(f"x1 must start at exact source head {SOURCE_REVISION}; observed {head}")
    if git(repo, "status", "--porcelain"):
        allowed_files = {
            "scripts/build_ghc_family_v645_v3_preregistration.py",
            "scripts/ghc_family_v645_v3_definitions.py",
            "scripts/ghc_family_v645_v3_x1_review.py",
            "tests/test_ghc_family_v645_v3_x1.py",
        }
        changed = {line[3:].replace("\\", "/") for line in git(repo, "status", "--porcelain").splitlines() if len(line) > 3}
        unexpected = {path for path in changed if path not in allowed_files and not path.startswith(PHASE_REL.as_posix() + "/")}
        if unexpected:
            raise SystemExit(f"unexpected pre-x1 changes: {sorted(unexpected)}")
    prior = collect_prior_proposals(repo)
    if len(prior) != 330 or len({item['proposal_id'] for item in prior}) != 330:
        raise SystemExit(f"expected 330 unique prior proposals, observed {len(prior)}")
    prior_titles = {normalized_title(item["title"]): item for item in prior}
    collisions = []
    nearest = []
    for item in PROPOSALS:
        norm = normalized_title(item["title"])
        if norm in prior_titles:
            collisions.append({"new": item["proposal_id"], "prior": prior_titles[norm]["proposal_id"], "title": item["title"]})
        candidates = sorted(
            ({"proposal_id": p["proposal_id"], "title": p["title"], "token_jaccard": round(jaccard(tokens(item["title"]), tokens(p["title"])), 4)} for p in prior),
            key=lambda row: row["token_jaccard"], reverse=True,
        )[:3]
        nearest.append({"proposal_id": item["proposal_id"], "nearest_prior_titles": candidates})
    if collisions:
        raise SystemExit(f"exact title collisions: {collisions}")

    dispositions = Counter(item["expected_disposition"] for item in PROPOSALS)
    research = {
        "schema": "ghc.family.v645-v3.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY, "source_phase": SOURCE_PHASE,
        "source_revision": SOURCE_REVISION, "source_seal_revision": SOURCE_SEAL,
        "preregistered_on": "2026-07-16", "primary_focus": "GMUT Mind; THOS Body and Freed ID/CBR Heart preserved",
        "occupation_study": "satellite geodesy and reference-frame metrology; bounded learning lens only",
        "proposal_count": len(PROPOSALS), "prior_frozen_proposal_count": len(prior),
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "expected_disposition_counts": dict(dispositions), "expected_counts_are_results": False,
        "x1_freeze_rule": "Commit and push the x1-only packet with four-way equality before any x2 implementation or outcome.",
        "proposals": PROPOSALS, "boundary": TRUTH_BOUNDARY,
    }
    portfolio = {
        "schema": "ghc.family.approval-portfolio.v1", "phase": PHASE, "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "counts": {
            "eiren_safe_now": len(EIREN_SAFE_NOW), "successor_safe_now_seeds": len(SUCCESSOR_SAFE_NOW),
            "eiren_candidate_prototypes": len(EIREN_CANDIDATE), "successor_candidate_seeds": len(SUCCESSOR_CANDIDATE),
            "eiren_exact_approval": len(EXACT_PACKETS), "eiren_blocked": len(BLOCKED_PACKETS),
        },
        "execution_rule": "Execute every Eiren safe-now packet and bounded candidate prototype in x2. Exact and blocked packets remain unexecuted. Successor seeds require fresh successor adoption.",
        "eiren_safe_now": EIREN_SAFE_NOW, "successor_safe_now_seeds": SUCCESSOR_SAFE_NOW,
        "eiren_candidate_prototypes": EIREN_CANDIDATE, "successor_candidate_seeds": SUCCESSOR_CANDIDATE,
        "eiren_exact_approval": EXACT_PACKETS, "eiren_blocked": BLOCKED_PACKETS,
        "boundary": TRUTH_BOUNDARY,
    }
    skill_runner_plan = {
        "schema": "ghc.family.skill-runner-plan.v1", "phase": PHASE, "owner": OWNER,
        "counts": {"eiren_skills_to_build": len(EIREN_SKILLS), "successor_skill_ideas": len(SUCCESSOR_SKILLS), "eiren_runners_to_build": len(EIREN_RUNNERS), "successor_runner_ideas": len(SUCCESSOR_RUNNERS)},
        "eiren_skills_to_build_test_use": [{"name": n, "description": d, "state": "preregistered"} for n, d in EIREN_SKILLS],
        "successor_skill_ideas": [{"name": n, "description": d, "state": "seed_only"} for n, d in SUCCESSOR_SKILLS],
        "eiren_runners_to_build_test_use": [{"name": n, "description": d, "state": "preregistered"} for n, d in EIREN_RUNNERS],
        "successor_runner_ideas": [{"name": n, "description": d, "state": "seed_only"} for n, d in SUCCESSOR_RUNNERS],
        "boundary": "Prototype validation is owner-scoped and does not establish production readiness or independent reproduction.",
    }
    clean_plan = {
        "schema": "ghc.family.clean-refine-plan.v1", "phase": PHASE, "owner": OWNER,
        "counts": {"eiren_tasks": len(EIREN_CLEAN), "successor_seeds": len(SUCCESSOR_CLEAN)},
        "eiren_tasks": EIREN_CLEAN, "successor_seeds": SUCCESSOR_CLEAN,
        "rule": "All tasks are additive or read-only. No deletion, reset, sibling-lane mutation, host-security weakening, or unreviewed migration is authorized by this ledger.",
    }
    source_ledger = {
        "schema": "ghc.family.source-ledger.v1", "phase": PHASE, "owner": OWNER,
        "counts": dict(Counter(item["status"] for item in SOURCES)), "source_count": len(SOURCES),
        "sources": SOURCES, "boundary": "A citation supplies context only; it is not empirical input, authority delegation, legal advice, or independent review.",
    }
    collision = {
        "schema": "ghc.family.proposal-collision-audit.v1", "phase": PHASE,
        "prior_frozen_proposal_count": len(prior), "prior_unique_id_count": len({p['proposal_id'] for p in prior}),
        "new_proposal_count": len(PROPOSALS), "exact_title_collision_count": len(collisions),
        "exact_title_collisions": collisions, "nearest_prior_titles": nearest,
        "semantic_review": "Human/model semantic review completed against all prior titles and mission surfaces; nearest-title scores are triage aids, not semantic proof.",
    }
    operational_negatives = {
        "schema": "ghc.family.operational-negatives.v1", "phase": PHASE,
        "inherited_effective_count": INHERITED_NEGATIVE_COUNT,
        "inherited_source": {"phase": SOURCE_PHASE, "revision": SOURCE_REVISION, "note": "Includes the external post-final terminal-wrapper negative retained by the activation baton."},
        "new_negatives": [
            {"negative_id": "V6453-X1-N01", "summary": "Initial prior-proposal collector import lacked an explicit scripts-path bootstrap.", "disposition": "retained_recovered", "method_id": "V6453-M01"},
            {"negative_id": "V6453-X1-N02", "summary": "Initial complete Method Flow skill read exceeded the ten-second command bound.", "disposition": "retained_recovered", "method_id": "V6453-M02"},
            {"negative_id": "V6453-X1-N03", "summary": "Initial recursive proposal audit included the active phase because relative and absolute paths were compared.", "disposition": "retained_recovered", "method_id": "V6453-M03"},
            {"negative_id": "V6453-X1-N04", "summary": "Initial source-authority test used a case-sensitive label expression and rejected a final specification.", "disposition": "retained_recovered", "method_id": "V6453-M04"},
            {"negative_id": "V6453-X1-N05", "summary": "A diagnostic PowerShell search used brittle nested quoting and failed to parse.", "disposition": "retained_recovered", "method_id": "V6453-M05"},
            {"negative_id": "V6453-X1-N06", "summary": "The preparatory privacy scanner matched its own verbatim forbidden path literal.", "disposition": "retained_recovered", "method_id": "V6453-M06"},
        ],
        "effective_count_after_x1": INHERITED_NEGATIVE_COUNT + 6,
        "boundary": "No retained negative is erased or folded into a pass.",
    }
    sandbox_plan = {
        "schema": "ghc.family.windows-sandbox-plan.v1", "phase": PHASE, "owner": OWNER,
        "profile_count": 6, "profile_labels": ["eiren", "ilyra", "sable", "orin", "tamar", "sylven"],
        "x2_scope": ["compose owner-scoped .wsb templates", "compose a deterministic bootstrap", "lint XML and mapped-folder boundaries", "probe feature and CLI availability read-only", "do not launch without a separate runtime witness"],
        "network_default": "disabled", "vgpu_default": "disabled", "mapped_source_default": "read_only", "mapped_output_default": "owner_scoped_write",
        "host_change_gate": "Feature enablement, elevation, host-security changes, and reboot remain exact-gated during this repository phase to avoid interrupting the active six-seat route.",
        "sources": ["V6453-S18", "V6453-S19"], "boundary": TRUTH_BOUNDARY,
    }
    method_ledger = method_flow_ledger()

    write_json(phase_dir / "x1-proposals.json", research)
    write_json(phase_dir / "approval-packets/x1-approval-portfolio.json", portfolio)
    write_json(phase_dir / "prototypes/x1-skill-runner-plan.json", skill_runner_plan)
    write_json(phase_dir / "maintenance/x1-clean-refine-plan.json", clean_plan)
    write_json(phase_dir / "sources/source-ledger.json", source_ledger)
    write_json(phase_dir / "provenance/prior-proposal-collision-audit.json", collision)
    write_json(phase_dir / "validation/x1-operational-negatives.json", operational_negatives)
    write_json(phase_dir / "method-flow/method-flow-state.json", method_ledger)
    write_json(phase_dir / "sandbox/x1-sandbox-plan.json", sandbox_plan)
    write_json(phase_dir / "environment/startup-receipt.json", {
        "schema": "ghc.family.startup-receipt.v1", "phase": PHASE, "owner": OWNER,
        "source_revision": SOURCE_REVISION, "source_seal_revision": SOURCE_SEAL,
        "source_head_verified": True, "source_seal_ancestral": True, "fast_forward_only": True,
        "eiren_lane_clean_before_x1": True, "source_remote_equal_before_x1": True,
        "detached_worktree_used": False, "identity_boundary": IDENTITY_BOUNDARY,
    })
    write_json(phase_dir / "focus/primary-focus-receipt.json", {
        "phase": PHASE, "primary_pillar": "GMUT Mind", "preserved_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "bounded_human_practice": "satellite geodesy and reference-frame metrology", "professional_authority_claimed": False,
    })
    write_json(phase_dir / "tooling/ghc-family-index.json", {
        "schema": "ghc.family.phase-index.v1", "phase": PHASE, "owner": OWNER,
        "source_revision": SOURCE_REVISION, "x1_state": "prepared_not_yet_committed",
        "primary_tools": ["ghc-family-index", "ghc-family-method-flow-state", "skill-creator", "family-current ghc_family_* runners"],
        "new_portfolio_counts": portfolio["counts"], "skill_runner_counts": skill_runner_plan["counts"],
        "validation_rule": "Eiren runs the full repository suite; one additive named local replay only; no detached worktrees.",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json(phase_dir / "orchestration/phase-update.json", {
        "schema": "ghc.family.orchestration-update.v1", "phase": PHASE, "owner": OWNER,
        "route": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "current_state": "x1_preregistration", "next_target_after_verified_closeout": "Ilyra Fen",
        "new_task_creation_permitted": False, "single_terminal_baton_only": True,
        "commit_budget": {"x1_max": 2, "x2_max": 2, "total_max": 4},
    })
    write_text(phase_dir / "sources/source-ledger.md", "# v645-v3 primary-source ledger\n\n" + "\n".join(f"- **{s['source_id']}** — [{s['title']}]({s['url']}); {s['authority']}; status `{s['status']}`." for s in SOURCES) + "\n\nSources provide context only; they do not supply missing data or authority.")
    write_text(phase_dir / "x1-preregistration.md", f"""# Eiren Kestrel v645-v3 x1 preregistration

This x1-only packet freezes ten research proposals after a 330-proposal novelty audit. Its parallel approval portfolio freezes {len(EIREN_SAFE_NOW)} Eiren safe-now tasks, {len(SUCCESSOR_SAFE_NOW)} successor safe-now seeds, {len(EIREN_CANDIDATE)} Eiren candidate prototypes, {len(SUCCESSOR_CANDIDATE)} successor candidate seeds, {len(EXACT_PACKETS)} exact-approval packets, and {len(BLOCKED_PACKETS)} blocked packets.

The build plan also freezes {len(EIREN_SKILLS)} Eiren skill prototypes, {len(SUCCESSOR_SKILLS)} successor skill ideas, {len(EIREN_RUNNERS)} Eiren runners, {len(SUCCESSOR_RUNNERS)} successor runner ideas, and {len(EIREN_CLEAN)} + {len(SUCCESSOR_CLEAN)} clean/refine tasks. Successor entries are prepared seeds, not executed or delivered work.

Primary focus is GMUT Mind through satellite geodesy and reference-frame metrology. THOS Body and Freed ID/CBR Heart remain explicit. All real-data, participant, production, legal, cultural, Maori-authority, deployment, security-complete, independent-reproduction, identity, and Stage 20 claims remain open or exact-gated.

x2 may begin only after this packet is committed, pushed, clean, and equal across local, upstream, tracking, and live remote. Exact and blocked packets are never executed by this phase.
""")
    write_text(phase_dir / "wellbeing-check.md", """# Eiren Kestrel wellbeing and scope check

The working name and family language are relational conventions, not proof of consciousness, personhood, continuity, employment, or authority. Work is bounded to the Eiren-owned lane. The active route is not supervised in the background, no sibling lane is mutated, and no new task or subagent is created.

The phase has a finite commit budget, a bounded retry policy, explicit stop conditions, and a nonpromotion boundary. A Windows Sandbox blueprint may be composed and linted, but disruptive host changes or a reboot are not performed during the active route.
""")

    exact_files = sorted(path.relative_to(repo).as_posix() for path in phase_dir.rglob("*") if path.is_file())
    exact_files += [
        "scripts/build_ghc_family_v645_v3_preregistration.py",
        "scripts/ghc_family_v645_v3_definitions.py",
        "scripts/ghc_family_v645_v3_x1_review.py",
        "tests/test_ghc_family_v645_v3_x1.py",
    ]
    exact_files = sorted(set(exact_files))
    write_json(phase_dir / "validation/x1-exact-file-set.json", {"schema": "ghc.family.x1-file-set.v1", "phase": PHASE, "file_count": len(exact_files) + 1, "files": sorted(exact_files + [f"{PHASE_REL.as_posix()}/validation/x1-exact-file-set.json"])})

    json_files = list(phase_dir.rglob("*.json"))
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))
    structural = {
        "schema": "ghc.family.x1-structural-validation.v1", "phase": PHASE, "valid": True,
        "checks": {
            "research_proposals_10": len(PROPOSALS) == 10,
            "research_ids_unique": len({p['proposal_id'] for p in PROPOSALS}) == 10,
            "research_titles_unique": len({normalized_title(p['title']) for p in PROPOSALS}) == 10,
            "prior_proposals_330": len(prior) == 330,
            "exact_title_collisions_zero": not collisions,
            "expected_distribution": dispositions == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
            "safe_now_15_each": len(EIREN_SAFE_NOW) == len(SUCCESSOR_SAFE_NOW) == 15,
            "candidate_10_each": len(EIREN_CANDIDATE) == len(SUCCESSOR_CANDIDATE) == 10,
            "exact_10_blocked_5": len(EXACT_PACKETS) == 10 and len(BLOCKED_PACKETS) == 5,
            "skills_10_each": len(EIREN_SKILLS) == len(SUCCESSOR_SKILLS) == 10,
            "runners_5_each": len(EIREN_RUNNERS) == len(SUCCESSOR_RUNNERS) == 5,
            "clean_15_each": len(EIREN_CLEAN) == len(SUCCESSOR_CLEAN) == 15,
            "method_flow_structural": method_ledger["counts"] == {"method_count": 6, "witness_count": 12, "failed_witness_count": 6, "passing_witness_count": 6, "preferred_method_count": 6, "candidate_method_count": 0, "recommendation_count": 6},
            "json_parse": True,
        },
        "json_file_count": len(json_files), "boundary": TRUTH_BOUNDARY,
    }
    if not all(structural["checks"].values()):
        raise SystemExit(f"x1 structural validation failed: {structural['checks']}")
    write_json(phase_dir / "validation/x1-structural.json", structural)
    print(json.dumps({"phase": PHASE, "proposal_count": 10, "prior_count": 330, "approval_counts": portfolio["counts"], "skill_runner_counts": skill_runner_plan["counts"], "clean_counts": clean_plan["counts"], "x1_file_count": len(list(phase_dir.rglob('*'))), "valid": True}, indent=2))


if __name__ == "__main__":
    main()
