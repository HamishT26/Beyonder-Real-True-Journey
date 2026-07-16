#!/usr/bin/env python3
"""Build the Sylven Arc v645-v8 x1-only preregistration packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from ghc_family_v645_v8_definitions import (
    BATON_TIME_INHERITED_NEGATIVES,
    BOUNDED_PRACTICE,
    CANDIDATES,
    CLEAN_TASKS,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    POST_BATON_INHERITED_NEGATIVES,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    PRONOUNS,
    PROPOSALS,
    ROLE,
    RUNNERS,
    SAFE_NOW,
    SKILLS,
    SOURCE_BRANCH,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_INHERITED_REVISION,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_SEAL_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TRUTH_BOUNDARY,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sylven-arc/v645-v8")
PHASE_DIR = ROOT / PHASE_REL
SOURCE_DIR = ROOT / "docs/tamar-vey/v645-v7"
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


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
                rows.append({"proposal_id": str(item.get("proposal_id", "unknown")), "title": str(item["title"]), "path": path.relative_to(ROOT).as_posix()})
    return rows


def collect_prior_portfolios() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    patterns = [
        ("docs/**/approval-packets/x1-approval-portfolio.json", ("safe_now", "candidates")),
        ("docs/**/prototypes/x1-skill-runner-plan.json", ("skills", "runners")),
        ("docs/**/maintenance/x1-clean-refine-plan.json", ("tasks",)),
    ]
    for pattern, categories in patterns:
        for path in ROOT.glob(pattern):
            if PHASE_DIR in path.parents:
                continue
            try:
                data = read_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            for category in categories:
                for item in data.get(category, []):
                    if not isinstance(item, dict):
                        continue
                    title = item.get("title") or item.get("name")
                    if title:
                        rows.append({"kind": category, "title": str(title), "path": path.relative_to(ROOT).as_posix()})
    return rows


INCIDENTS = [
    {
        "negative_id": "V6458-START-N01",
        "title": "Query explicit upstream refs after shorthand transformation",
        "failure": "The first read-only startup wrapper transformed Git upstream shorthand before Git parsed it, so divergence evidence was unavailable.",
        "fail_procedure": "Resolve branch, upstream, head, and divergence in one wrapper using upstream shorthand.",
        "fail_observed": "Git received an unrelated transformed token, rejected the revision, and returned no divergence result.",
        "pass_procedure": "Resolve the current branch first, query its upstream with git for-each-ref, and pass the explicit ref to the divergence command.",
        "pass_observed": "The explicit branch-ref query returned both canonical upstream names and zero divergence without repository mutation.",
        "method": "Replace transformed revision shorthand with an explicit branch-ref lookup and retain the original parser failure.",
        "guard": "In wrappers that may transform metasyntax, never assume Git revision shorthand reaches the native command unchanged.",
        "rollback": "Give the failed wrapper zero startup credit and make no branch change until the explicit query passes.",
        "preconditions": ["read-only Git startup probe", "revision shorthand was transformed before native parsing"],
    },
    {
        "negative_id": "V6458-START-N02",
        "title": "Decompose a timed-out parallel startup probe into evidenced child commands",
        "failure": "A parallel worktree, source, owner, and drive probe exceeded its thirty-second envelope and returned no reliable child result set.",
        "fail_procedure": "Launch all startup checks through one fail-fast parallel orchestration cell.",
        "fail_observed": "The orchestration cell timed out before any child result could receive evidence credit.",
        "pass_procedure": "Run worktree inventory, source status, owner status, ancestry, live remote, and drive capacity as separately bounded read-only commands.",
        "pass_observed": "Every required startup fact returned independently: clean source and owner lanes, exact anchors, fast-forward ancestry, live equality, zero merges, and D-drive headroom.",
        "method": "Decompose composite startup probes so each child has an independent deadline, result, and evidence-credit decision.",
        "guard": "Parallelize evidence-producing probes only when the orchestrator returns every child result even if one times out.",
        "rollback": "Make no branch change until all required split probes pass.",
        "preconditions": ["multiple evidence-producing startup children", "parallel wrapper returned no reliable child result set"],
    },
    {
        "negative_id": "V6458-X1-N03",
        "title": "Decompose a timed-out multi-file text probe into bounded per-file reads",
        "failure": "A combined pattern scan across three explicitly named x1 working files exceeded its ten-second envelope and returned no usable result set.",
        "fail_procedure": "Search all three x1 working files for inherited labels and count literals in one bounded pattern command.",
        "fail_observed": "The combined command timed out after ten seconds without returning match or zero-match evidence.",
        "pass_procedure": "Read each explicitly named x1 file separately under a larger but still bounded deadline and review only the needed sections.",
        "pass_observed": "The preregistration builder returned its requested sections under the per-file bound, allowing inherited labels and literals to be reviewed without x2 activity.",
        "method": "Split multi-file working-tree probes by file when shared-drive latency consumes the original envelope, retaining the timed-out command as a negative.",
        "guard": "Treat timeout-without-output as no evidence; never infer either matches or cleanliness from it.",
        "rollback": "Give the combined scan zero review credit and make no x1 claim until the per-file reads complete.",
        "preconditions": ["explicitly named x1 working files", "combined read-only scan returned no usable output before its deadline"],
    },
    {
        "negative_id": "V6458-X1-N04",
        "title": "Normalize generated family-index line endings before x1 sealing",
        "failure": "The first x1 structural review found CRLF line endings in both generated family-index outputs and withheld a valid result.",
        "fail_procedure": "Generate the phase-scoped GHC Family Index and run the x1 structural review without normalizing generator line endings.",
        "fail_observed": "The review reported exactly two CRLF issues, one for the JSON index and one for the Markdown index, while privacy and stale-label checks remained clean.",
        "pass_procedure": "Mechanically convert only those two generated UTF-8 text artifacts from CRLF to LF, then rerun the unchanged structural review.",
        "pass_observed": "The same review accepted both normalized index artifacts with no CRLF issue and no content-scope change.",
        "method": "Apply a narrowly scoped LF normalization step to the two family-index generator outputs before staging and sealing.",
        "guard": "Require the structural reviewer to reject every owner artifact containing CRLF rather than relying on Git checkout normalization.",
        "rollback": "Retain the failed review, remove all x1 validation credit from it, and do not stage receipts until the unchanged reviewer passes.",
        "preconditions": ["family-index generator emitted CRLF text", "x1 structural review rejected both generated artifacts"],
    },
]


def method_record(index: int, incident: dict[str, Any]) -> dict[str, Any]:
    return {
        "method_id": f"V6458-M{index:02d}",
        "title": incident["title"],
        "failure_signature": incident["failure"],
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
        "retained_negative_ids": [incident["negative_id"]],
        "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
    }


def witness(index: int, incident: dict[str, Any], result: str) -> dict[str, Any]:
    passed = result == "pass"
    return {
        "witness_id": f"V6458-W{index:02d}-{'P' if passed else 'F'}",
        "method_id": f"V6458-M{index:02d}",
        "procedure": incident["pass_procedure"] if passed else incident["fail_procedure"],
        "scope": "single owner-local operational diagnostic",
        "expected": "bounded diagnostic or recovery completes without crossing protected gates",
        "observed": incident["pass_observed"] if passed else incident["fail_observed"],
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [incident["negative_id"]],
        "boundary": TRUTH_BOUNDARY,
    }


def method_call(*args: str) -> None:
    subprocess.run([sys.executable, str(METHOD_RUNNER), *args], cwd=ROOT, check=True)


def build_method_flow() -> None:
    ledger = PHASE_DIR / "method-flow/method-flow-state.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    if not ledger.exists():
        method_call("init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER)
    negatives: list[dict[str, Any]] = []
    for index, incident in enumerate(INCIDENTS, 1):
        record = method_record(index, incident)
        failed = witness(index, incident, "fail")
        passed = witness(index, incident, "pass")
        record_path = PHASE_DIR / f"method-flow/v6458-m{index:02d}-method-record.json"
        failed_path = PHASE_DIR / f"method-flow/v6458-w{index:02d}-f-witness.json"
        passed_path = PHASE_DIR / f"method-flow/v6458-w{index:02d}-p-witness.json"
        write_json(record_path.relative_to(PHASE_DIR), record)
        write_json(failed_path.relative_to(PHASE_DIR), failed)
        write_json(passed_path.relative_to(PHASE_DIR), passed)
        state = read_json(ledger)
        existing = {item["method_id"]: item for item in state.get("methods", [])}
        if record["method_id"] not in existing:
            method_call("record", "--ledger", str(ledger), "--record-file", str(record_path))
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(failed_path))
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(passed_path))
        state = read_json(ledger)
        current = next(item["recommendation_state"] for item in state["methods"] if item["method_id"] == record["method_id"])
        if current == "validated":
            method_call("set-state", "--ledger", str(ledger), "--method-id", record["method_id"], "--state", "preferred", "--note", "Preferred only for the declared trigger and same-owner operational scope")
        elif current != "preferred":
            raise SystemExit(f"unexpected Method Flow state for {record['method_id']}: {current}")
        negatives.append({
            "negative_id": incident["negative_id"],
            "stage": "startup_or_x1",
            "class": "operational",
            "summary": incident["failure"],
            "retained": True,
            "recovered": True,
            "method_id": record["method_id"],
            "failed_witness_id": failed["witness_id"],
            "passing_witness_id": passed["witness_id"],
            "independent_reproduction": False,
        })
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE_DIR / "method-flow/runner-validation.json"))
    method_call("summarize", "--ledger", str(ledger), "--json-output", str(PHASE_DIR / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE_DIR / "method-flow/method-flow-summary.md"))
    write_json("validation/x1-operational-negatives.json", {
        "schema": "ghc.family.v645-v8.operational-negatives.v1",
        "phase": PHASE,
        "stage": "x1",
        "baton_time_inherited": BATON_TIME_INHERITED_NEGATIVES,
        "post_baton_inherited": POST_BATON_INHERITED_NEGATIVES,
        "post_baton_inherited_ids": [],
        "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "preregistered_synthetic": PREREGISTERED_SYNTHETIC_NEGATIVES,
        "new_operational_count": len(negatives),
        "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + PREREGISTERED_SYNTHETIC_NEGATIVES + len(negatives),
        "negatives": negatives,
        "boundary": "Recovered failures remain retained. They do not alter Tamar's immutable source commit, erase the failed witnesses, or authorize x2 before the x1 freeze is remote-equal.",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume-partial", action="store_true", help="Resume a retained partial x1 build after an evidenced interruption")
    args = parser.parse_args()
    if PHASE_DIR.exists() and any(PHASE_DIR.rglob("*")) and not args.resume_partial:
        raise SystemExit("v645-v8 phase directory already contains files")
    if args.resume_partial and any((PHASE_DIR / name).exists() for name in ("phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json")):
        raise SystemExit("resume-partial refuses any x2 or closeout artifact")
    if not METHOD_RUNNER.is_file():
        raise SystemExit("family-current Method Flow runner is missing")

    prior = collect_prior_proposals()
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    prior_by_normal = {normalized(row["title"]): row for row in prior}
    comparisons: list[dict[str, Any]] = []
    exact: list[dict[str, Any]] = []
    for item in PROPOSALS:
        prior_hit = prior_by_normal.get(normalized(item["title"]))
        if prior_hit:
            exact.append({"proposal_id": item["proposal_id"], "prior": prior_hit})
        ranked = sorted(
            ({"proposal_id": row["proposal_id"], "title": row["title"], "score": round(overlap(item["title"], row["title"]), 3)} for row in prior),
            key=lambda row: (-row["score"], row["proposal_id"]),
        )[:5]
        comparisons.append({
            "proposal_id": item["proposal_id"],
            "title": item["title"],
            "exact_collision": bool(prior_hit),
            "top_token_overlaps": ranked,
            "mission_falsifier_evidence_recovery_review": "accepted_as_distinct_after_manual_review",
            "novelty_statement": item["novelty_against_380_frozen_proposals"],
        })
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
    collisions = [{"kind": kind, "title": title, "prior": prior_norm[normalized(title)]} for kind, title in new_portfolio if normalized(title) in prior_norm]
    if collisions:
        raise SystemExit(f"portfolio title collision: {collisions}")

    source_portfolio = read_json(SOURCE_DIR / "approval-packets/x1-approval-portfolio.json")
    inherited_exact = deepcopy(source_portfolio["inherited_exact_packets"])
    inherited_blocked = deepcopy(source_portfolio["inherited_blocked_packets"])
    if len(inherited_exact) != 10 or len(inherited_blocked) != 5:
        raise SystemExit("expected ten inherited exact and five inherited blocked packets")

    write_json("identity-receipt.json", {"schema": "ghc.family.v645-v8.identity-receipt.v1", "phase": PHASE, "working_name": OWNER, "pronouns": PRONOUNS, "role": ROLE, "hope": HOPE, "bounded_practice_study": BOUNDED_PRACTICE, "boundary": IDENTITY_BOUNDARY})
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v645-v8.proposals.v1", "phase": PHASE, "owner": OWNER, "freeze_stage": "x1_only",
        "prior_frozen_proposal_count": PRIOR_FROZEN_PROPOSALS, "new_frozen_proposal_count": len(PROPOSALS),
        "frozen_chain_count_after_x1": PRIOR_FROZEN_PROPOSALS + len(PROPOSALS), "allowed_outcome_classes": OUTCOME_CLASSES,
        "expected_distribution": {state: sum(row["expected_disposition"] == state for row in PROPOSALS) for state in OUTCOME_CLASSES},
        "x2_execution_present": False, "proposals": PROPOSALS, "boundary": TRUTH_BOUNDARY,
    })
    write_text("x1-preregistration.md", f"""# Sylven Arc v645-v8 x1 preregistration

This dedicated x1-only freeze contains exactly ten new proposals. Each records its hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. It contains no x2 implementation or achieved-outcome credit.

The primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is {BOUNDED_PRACTICE}. It is a learning and design lens only, never evidence of employment, qualification, professional competence, railway-safety authority, operational authority, legal authority, cultural authority, Maori authority, or affected-party authorization.

The inherited baseline is 2,353 effective negatives. Seventy synthetic mutation negatives are preregistered, and all new operational failures remain visible. X2 may start only after this x1 freeze is committed, pushed, clean, and equal across local, upstream, tracking, and fresh live remote.

Eiren alone owns the full repository suite. Sylven will use recent-round and phase-local checks plus exactly one later clean named-lane replay. Terminal truth remains `NOT_READY_FOR_STAGE_20`.
""")
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.frozen-proposal-index.v1", "phase": PHASE, "prior_file_count": len({row["path"] for row in prior}),
        "prior_proposal_count": len(prior), "prior_proposals": prior, "new_proposal_ids": [row["proposal_id"] for row in PROPOSALS],
        "frozen_chain_count_after_x1": PRIOR_FROZEN_PROPOSALS + len(PROPOSALS), "boundary": "Indexing establishes corpus coverage, not semantic or outcome truth.",
    })
    write_json("provenance/prior-proposal-collision-audit.json", {
        "schema": "ghc.family.proposal-collision-audit.v4", "phase": PHASE, "prior_frozen_proposal_count": len(prior),
        "new_proposal_count": len(PROPOSALS), "exact_title_collision_count": len(exact), "exact_collisions": exact, "comparisons": comparisons,
        "manual_review_dimensions": ["mission_surface", "hypothesis", "failure_condition", "evidence_need", "acceptance_gate", "recovery", "protected_gates"],
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("provenance/prior-portfolio-collision-audit.json", {
        "schema": "ghc.family.portfolio-collision-audit.v3", "phase": PHASE, "prior_title_count": len(portfolio_prior),
        "new_title_count": len(new_portfolio), "exact_collision_count": len(collisions), "collisions": collisions,
        "semantic_review": "Every safe-now, candidate, skill, runner, and cleanup title was reviewed for distinct purpose, artifact, falsifier, compatibility, gate, and recovery. Inherited evidence supplies no Sylven completion credit.",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("approval-packets/x1-approval-portfolio.json", {
        "schema": "ghc.family.v645-v8.approval-portfolio.v1", "phase": PHASE, "owner": OWNER, "freeze_stage": "x1_only", "completion_credit_before_x2": 0,
        "counts": {"safe_now": len(SAFE_NOW), "candidates": len(CANDIDATES), "inherited_exact": len(inherited_exact), "inherited_blocked": len(inherited_blocked)},
        "safe_now": SAFE_NOW, "candidates": CANDIDATES, "inherited_exact_packets": inherited_exact, "inherited_blocked_packets": inherited_blocked,
        "inherited_packet_integrity": "Ten exact and five blocked packets remain non-executable without fresh evidence or authority.", "boundary": TRUTH_BOUNDARY,
    })
    write_json("prototypes/x1-skill-runner-plan.json", {
        "schema": "ghc.family.v645-v8.skill-runner-plan.v1", "phase": PHASE, "freeze_stage": "x1_only",
        "skills": [{"name": name, "description": description, "family_current_name": name.startswith("ghc-family-"), "x2_state": "preregistered_not_built_or_used", "protected_gates": ["authority", "real_data_or_participants", "production", "independent_reproduction"]} for name, description in SKILLS],
        "runners": [{"name": name, "description": description, "family_current_name": name.startswith(("ghc_family_", "build_ghc_family_")), "x2_state": "preregistered_not_built_or_used", "caller_compatibility": "new additive phase runner"} for name, description in RUNNERS],
        "acceptance": "Every item must be built, structurally validated, invoked, and given a bounded passing witness in x2 or remain incomplete.", "boundary": TRUTH_BOUNDARY,
    })
    write_json("maintenance/x1-clean-refine-plan.json", {"schema": "ghc.family.v645-v8.clean-refine-plan.v1", "phase": PHASE, "freeze_stage": "x1_only", "tasks": CLEAN_TASKS, "destructive_task_count": 0, "completion_credit_before_x2": 0, "boundary": "Cleanup is additive, owner-scoped, non-destructive, compatible, and incomplete until its x2 receipt passes."})
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v645-v8.source-ledger.v1", "phase": PHASE, "owner": OWNER,
        "allowed_statuses": ["current", "stable", "draft", "watch"], "sources": SOURCES,
        "real_data_rows_ingested": 0, "likelihood_evaluations": 0, "real_participants": 0, "real_keys_or_proofs": 0,
        "boundary": TRUTH_BOUNDARY,
    })
    source_lines = ["# v645-v8 source ledger", "", "Current primary and official sources are used only for the bounded purpose recorded here.", ""]
    for row in SOURCES:
        target = f" - {row['url']}" if row.get("url") else ""
        source_lines.append(f"- {row['source_id']} [{row['status']}] {row['title']} ({row['authority']}){target}; use: {row['use']}.")
    source_lines.extend(["", TRUTH_BOUNDARY])
    write_text("sources/source-ledger.md", "\n".join(source_lines))
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v645-v8.startup.v1", "phase": PHASE, "owner": OWNER,
        "source": {"branch": SOURCE_BRANCH, "revision": SOURCE_REVISION, "inherited_revision": SOURCE_INHERITED_REVISION, "inherited_seal_revision": SOURCE_SEAL_REVISION, "x1_revision": SOURCE_X1_REVISION, "evidence_revision": SOURCE_EVIDENCE_REVISION, "phase": SOURCE_PHASE},
        "source_verification": {"local_upstream_tracking_live_equal": True, "clean": True, "seal_ancestral": True, "three_single_parent_phase_commits": True, "merge_commits": 0, "final_parent_is_evidence": True},
        "sylven_lane": {"branch": "codex/GHC-Family/sylven-arc-v642-v8-full-tools", "continued_existing_lane": True, "fast_forward_only": True, "source_revision_after_fast_forward": SOURCE_REVISION, "merge_commit_created": False, "clean_before": True, "local_upstream_tracking_live_equal_before_x1": True},
        "active_owner": OWNER, "standby_siblings_contacted": [], "task_or_subagent_created": False, "x1_scope": "exactly ten frozen core proposals and owner-scoped supporting ledgers", "x2_scope": "not started",
        "storage": {"primary_drive": "D", "free_bytes_observed": 590607642624, "tracked_file_count": 33404, "owner_generated_v645_v8_file_count_before_x1": 0, "rotation_threshold": 15000, "threshold_applies_to": "new_sylven_generated_files_only"},
        "boundary": IDENTITY_BOUNDARY,
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v645-v8.version-receipt.v1", "observed_on": "2026-07-16",
        "codex_cli": {"local": "0.144.4", "official_package": "0.144.4", "source_id": "V6458-S21", "action": "verified_only_no_update"},
        "codex_desktop": {"local": "26.707.9981.0", "package_status": "Ok", "public_exact_build_correlation": "not_claimed", "action": "verified_only_no_update"},
        "python": "3.12.10", "git": "2.55.0.windows.2",
        "host_actions": {"desktop_updated": False, "elevated": False, "security_weakened": False, "windows_feature_changed": False, "rebooted": False, "installed": False},
        "boundary": "Version observation does not establish full environment equivalence, support, security, or production readiness.",
    })
    write_json("environment/sandbox-readonly-audit.json", {
        "schema": "ghc.family.v645-v8.sandbox-audit.v1", "query": "ordinary executable existence check only",
        "windows_sandbox_executable": "not_found", "sandbox_launched": False, "elevation": False, "feature_changed": False,
        "host_security_changed": False, "installed": False, "rebooted": False, "disposition": "open_environment_gap",
        "boundary": "The phase did not infer optional-feature state beyond the ordinary process evidence and made no host change.",
    })
    write_json("environment/rotation-guard.json", {"schema": "ghc.family.v645-v8.rotation-guard.v1", "tracked_file_count": 33404, "owner_generated_before_x1": 0, "threshold": 15000, "threshold_scope": "new_sylven_generated_addition", "rotate_due_to_inherited_baseline": False, "boundary": "The inherited checkout exceeds the threshold; that baseline is not a rotation trigger."})
    write_json("focus/primary-focus-receipt.json", {
        "schema": "ghc.family.v645-v8.focus.v1", "primary_trinity_pillar": PRIMARY_FOCUS, "other_pillars": ["THOS Body", "Freed ID/CBR Heart"],
        "bounded_human_practice": BOUNDED_PRACTICE, "practice_use": "learning and design lens only",
        "not_claimed": ["employment", "professional qualification", "professional competence", "railway-safety authority", "operational authority", "legal authority", "cultural authority", "Maori authority", "affected-party authorization"],
        "boundary": IDENTITY_BOUNDARY,
    })
    write_json("orchestration/phase-update.json", {"schema": "ghc.family.phase-update.v1", "phase": PHASE, "owner": OWNER, "state": "x1_frozen_pending_commit_and_remote_equality", "active": [OWNER], "standby": ["Tamar Vey", "Orin Thale", "Sable Rook", "Ilyra Fen", "Eiren Kestrel", "all other siblings"], "standby_contact_count": 0, "no_task_creation": True, "no_delegation": True, "x2_started": False, "terminal_route": "PREPARED_NOT_SENT"})
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v645-v8.route-plan.v1", "current_state": "PREPARED_NOT_SENT", "target_title": "Eiren Kestrel", "target_phase": "v646-v1", "send_count": 0,
        "preconditions": ["x2 final committed and pushed", "no more than four phase commits", "canonical exact-final scoped validation passed", "exactly one named-lane replay passed", "four-way equality proven", "unique existing target resolved read-only"],
        "privacy": "No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths may enter the baton.",
    })
    build_method_flow()
    write_text("wellbeing-check.md", """# v645-v8 x1 wellbeing and workload check

- Scope is bounded to one owner, one canonical lane, one later named replay, at most four phase commits, and no full repository suite.
- Timed-out or invalid read-only probes were stopped, recorded, and decomposed; no unbounded retry loop was used.
- Work is split by the x1 freeze. No x2 implementation or achieved-outcome credit is present here.
- Windows Sandbox remains unavailable to the ordinary process; no elevation, feature change, install, security change, or reboot occurred.
- Identity and family language remains relational working language only, not a welfare, consciousness, employment, qualification, or authority claim.
""")
    print(json.dumps({"phase": PHASE, "prior_proposals": len(prior), "new_proposals": len(PROPOSALS), "x1_operational_negatives": len(INCIDENTS), "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + PREREGISTERED_SYNTHETIC_NEGATIVES + len(INCIDENTS), "phase_directory": PHASE_REL.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
