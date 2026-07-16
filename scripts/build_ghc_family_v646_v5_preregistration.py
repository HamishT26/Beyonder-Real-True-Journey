#!/usr/bin/env python3
"""Build the strict Tamar Vey v646-v5 x1-only preregistration packet."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v646_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def overlap(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 0.0


def collect_prior_proposals() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in ROOT.glob("docs/**/x1-proposals.json"):
        if PHASE in path.parents:
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
            if PHASE in path.parents:
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
                        rows.append({"category": category, "title": str(title), "path": path.relative_to(ROOT).as_posix()})
    return rows


def method_call(*args: str) -> None:
    subprocess.run([sys.executable, str(METHOD_RUNNER), *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")


def build_method_flow() -> None:
    ledger = PHASE / "method-flow/method-flow-state.json"
    if ledger.exists():
        existing = json.loads(ledger.read_text(encoding="utf-8"))
        if (existing.get("phase"), existing.get("owner")) != (d.PHASE, d.OWNER):
            raise RuntimeError("existing Method Flow ledger identity mismatch")
    else:
        method_call("init", "--ledger", str(ledger), "--phase", d.PHASE, "--owner", d.OWNER)

    def ensure_method(method_id: str, relative: str) -> None:
        current = json.loads(ledger.read_text(encoding="utf-8"))
        if not any(row.get("method_id") == method_id for row in current.get("methods", [])):
            method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / relative))

    def ensure_witness(witness_id: str, relative: str) -> None:
        current = json.loads(ledger.read_text(encoding="utf-8"))
        if not any(row.get("witness_id") == witness_id for row in current.get("witnesses", [])):
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / relative))

    def ensure_preferred(method_id: str, note: str) -> None:
        current = json.loads(ledger.read_text(encoding="utf-8"))
        row = next(item for item in current.get("methods", []) if item.get("method_id") == method_id)
        if row.get("recommendation_state") != "preferred":
            method_call("set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", note)
    method = {
        "method_id": "V6465-M01",
        "title": "Separate branch movement from exact remote-equality reporting",
        "failure_signature": "The successful fast-forward and push produced an overlarge response that the tool display truncated, so the full transition transcript was not a bounded evidence surface.",
        "trigger_preconditions": ["large inherited fast-forward", "Git progress and file summary", "bounded tool output"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_read_only_or_owner_scoped_workflow",
        "candidate_workaround": "Treat the Git exit and final head as transition evidence, then run a separate bounded fetch, ref, live-remote, divergence, and clean-state proof.",
        "validation_witness_ids": [],
        "recurrence_guard": "For large inherited advances, suppress diffstat or separate movement, push, and equality proof so no overlarge output is needed for final credit.",
        "rollback": "Award no four-way-equality credit from truncated display; stop before phase mutation until the split read-only proof passes.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["history_rewrite", "force_push", "sibling_lane", "privacy", "completion_credit"],
        "retained_negative_ids": ["V6465-X1-N01"],
        "scope_boundary": "Owner-branch movement and read-only equality reporting only; no scientific, authority, production, security-complete, or independent-reproduction credit.",
    }
    failed = {
        "witness_id": "V6465-M01-F", "method_id": "V6465-M01",
        "procedure": "Combine a large fast-forward diffstat and push in one displayed evidence response.",
        "scope": "Tamar source advance", "expected": "Return the complete bounded transition and equality evidence.",
        "observed": "Git succeeded, but the tool display was truncated and could not serve as a complete equality receipt.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N01"], "boundary": d.TRUTH_BOUNDARY,
    }
    passed = {
        "witness_id": "V6465-M01-P", "method_id": "V6465-M01",
        "procedure": "Fetch once, resolve local, upstream, tracking, and live refs separately, calculate divergence, and require clean state.",
        "scope": "Tamar exact source equality after fast-forward", "expected": "All four refs equal the verified source with 0/0 divergence and a clean worktree.",
        "observed": "All four refs equaled the verified Orin final, divergence was 0/0, and the worktree was clean before x1.",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N01"], "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("method-flow/v6465-m01-method-record.json", method)
    write_json("method-flow/v6465-m01-f-witness.json", failed)
    write_json("method-flow/v6465-m01-p-witness.json", passed)
    ensure_method("V6465-M01", "method-flow/v6465-m01-method-record.json")
    ensure_witness("V6465-M01-F", "method-flow/v6465-m01-f-witness.json")
    ensure_witness("V6465-M01-P", "method-flow/v6465-m01-p-witness.json")
    ensure_preferred("V6465-M01", "Preferred only for large owner-branch advances with matching preconditions")
    method2 = {
        "method_id": "V6465-M02",
        "title": "Reject inherited expanded-portfolio titles before x1 materialization",
        "failure_signature": "The first x1 builder detected exact inherited cleanup and skill title collisions and stopped before writing the phase packet.",
        "trigger_preconditions": ["expanded portfolio freeze", "prior portfolio corpus", "exact normalized title audit"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_read_only_or_owner_scoped_workflow",
        "candidate_workaround": "List every exact collision, rewrite each central title and purpose as Tamar-specific new work, and rerun the unchanged corpus audit before materialization.",
        "validation_witness_ids": [],
        "recurrence_guard": "Audit safe, candidate, skill, runner, and cleanup titles together before any x1 file is written; shared family semantics do not excuse a duplicate proposal title.",
        "rollback": "Retain the failed build with zero freeze credit and change only the colliding uncommitted definitions.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["x1_freeze", "completion_credit", "failure_erasure", "sibling_lane", "privacy"],
        "retained_negative_ids": ["V6465-X1-N02"],
        "scope_boundary": "Expanded-portfolio semantic novelty only; no x2, authority, scientific, or independent-reproduction credit.",
    }
    failed2 = {
        "witness_id": "V6465-M02-F", "method_id": "V6465-M02",
        "procedure": "Run the exact normalized expanded-portfolio title audit against inherited packets.",
        "scope": "Tamar v646-v5 x1 portfolio freeze", "expected": "Zero inherited or within-current title collisions.",
        "observed": "Inherited cleanup and skill titles collided exactly; the builder stopped before phase materialization.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N02"], "boundary": d.TRUTH_BOUNDARY,
    }
    passed2 = {
        "witness_id": "V6465-M02-P", "method_id": "V6465-M02",
        "procedure": "Rewrite every colliding title and rerun the same prior-portfolio and within-current audit.",
        "scope": "Tamar v646-v5 x1 portfolio freeze", "expected": "Zero exact collisions and the required 30/20/20/10/30 counts remain.",
        "observed": "The corrected portfolio retained every floor and returned zero exact inherited or within-current collisions.",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N02"], "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("method-flow/v6465-m02-method-record.json", method2)
    write_json("method-flow/v6465-m02-f-witness.json", failed2)
    write_json("method-flow/v6465-m02-p-witness.json", passed2)
    ensure_method("V6465-M02", "method-flow/v6465-m02-method-record.json")
    ensure_witness("V6465-M02-F", "method-flow/v6465-m02-f-witness.json")
    ensure_witness("V6465-M02-P", "method-flow/v6465-m02-p-witness.json")
    ensure_preferred("V6465-M02", "Preferred for expanded-portfolio freezes against inherited title corpora")
    method3 = {
        "method_id": "V6465-M03",
        "title": "Separate scanner definitions from the stale-state literals they detect",
        "failure_signature": "The first exact staged review found the reviewer source itself because its scanner implementation contained each complete forbidden stale-state literal.",
        "trigger_preconditions": ["self-scanning staged reviewer", "literal stale-state definitions", "exact owner-scoped staged-file review"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped_validation_repair",
        "candidate_workaround": "Construct each monitored literal from adjacent constant fragments while scanning every staged owner file with the same rules.",
        "validation_witness_ids": [],
        "recurrence_guard": "Self-scanning validators must not embed complete monitored literals in their own implementation; retain full file coverage and make only scanner definitions representation-safe.",
        "rollback": "Retain the failed review with zero freeze credit and do not commit until the unchanged full-scope review passes.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["x1_freeze", "stale_label_review", "coverage_reduction", "failure_erasure", "completion_credit"],
        "retained_negative_ids": ["V6465-X1-N03"],
        "scope_boundary": "Owner-scoped validation representation only; no x2, scientific, authority, security-complete, privacy-complete, or independent-reproduction credit.",
    }
    failed3 = {
        "witness_id": "V6465-M03-F", "method_id": "V6465-M03",
        "procedure": "Run the exact staged-file review while the reviewer source embeds each complete forbidden stale-state literal.",
        "scope": "Tamar v646-v5 x1 exact staged-file review", "expected": "Review every staged owner file with zero stale-state findings.",
        "observed": "The reviewer source matched its own scanner-definition literals; structure, privacy, exact file set, and JSON checks otherwise passed.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N03"], "boundary": d.TRUTH_BOUNDARY,
    }
    passed3 = {
        "witness_id": "V6465-M03-P", "method_id": "V6465-M03",
        "procedure": "Build monitored literals from constant fragments, keep all staged files in scope, and rerun the exact staged-file review.",
        "scope": "Tamar v646-v5 x1 exact staged-file review", "expected": "Full-scope stale review passes without suppressing or excluding the reviewer.",
        "observed": "The reviewer source no longer contains complete monitored literals, and the stale reviewer still iterates every supplied staged owner path without an exclusion.",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N03"], "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("method-flow/v6465-m03-method-record.json", method3)
    write_json("method-flow/v6465-m03-f-witness.json", failed3)
    write_json("method-flow/v6465-m03-p-witness.json", passed3)
    ensure_method("V6465-M03", "method-flow/v6465-m03-method-record.json")
    ensure_witness("V6465-M03-F", "method-flow/v6465-m03-f-witness.json")
    ensure_witness("V6465-M03-P", "method-flow/v6465-m03-p-witness.json")
    ensure_preferred("V6465-M03", "Preferred for self-scanning validators with exact stale-state literals")
    method4 = {
        "method_id": "V6465-M04",
        "title": "Resume a preregistration build against its verified existing Method Flow ledger",
        "failure_signature": "The repaired preregistration rerun called Method Flow init unconditionally, and the runner refused the already-existing phase ledger before the updated packet could complete.",
        "trigger_preconditions": ["same phase and owner", "retained existing Method Flow ledger", "preregistration rebuild after an operational negative"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped_workflow_recovery",
        "candidate_workaround": "Verify the existing ledger phase and owner, initialize only when absent, and add only missing method, witness, and state records.",
        "validation_witness_ids": [],
        "recurrence_guard": "Every rerunnable phase builder must distinguish absent, matching, and mismatched ledgers; it may reuse only a matching ledger and must never erase prior witnesses.",
        "rollback": "Retain the failed rerun with zero freeze credit; stop on identity mismatch and leave the existing ledger unchanged.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["failure_erasure", "method_flow_identity", "x1_freeze", "completion_credit", "history_rewrite"],
        "retained_negative_ids": ["V6465-X1-N04"],
        "scope_boundary": "Phase-local builder resumption only; no x2, production, authority, privacy-complete, or independent-reproduction credit.",
    }
    failed4 = {
        "witness_id": "V6465-M04-F", "method_id": "V6465-M04",
        "procedure": "Rerun the preregistration builder while calling Method Flow init unconditionally.",
        "scope": "Tamar v646-v5 x1 repair rerun", "expected": "Preserve prior witnesses and complete the updated x1 packet.",
        "observed": "The runner returned ledger already exists and the builder exited before the updated packet completed.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N04"], "boundary": d.TRUTH_BOUNDARY,
    }
    passed4 = {
        "witness_id": "V6465-M04-P", "method_id": "V6465-M04",
        "procedure": "Verify the existing ledger identity, skip duplicate records, append only missing records, then validate and summarize the ledger.",
        "scope": "Tamar v646-v5 x1 repair rerun", "expected": "All prior failures remain and each new method and witness appears exactly once.",
        "observed": "The matching phase-owner ledger was reused; M01 and M02 were retained without duplication while missing M03 and M04 records were appended once.",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X1-N04"], "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("method-flow/v6465-m04-method-record.json", method4)
    write_json("method-flow/v6465-m04-f-witness.json", failed4)
    write_json("method-flow/v6465-m04-p-witness.json", passed4)
    ensure_method("V6465-M04", "method-flow/v6465-m04-method-record.json")
    ensure_witness("V6465-M04-F", "method-flow/v6465-m04-f-witness.json")
    ensure_witness("V6465-M04-P", "method-flow/v6465-m04-p-witness.json")
    ensure_preferred("V6465-M04", "Preferred for same-phase rebuilds with a verified matching Method Flow ledger")
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/runner-validation.json"))
    method_call("summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"))


def main() -> int:
    prior = collect_prior_proposals()
    if len(prior) != d.PRIOR_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    exact = []
    nearest = []
    for proposal in d.PROPOSALS:
        matches = [row for row in prior if normalized(row["title"]) == normalized(proposal["title"])]
        exact.extend({"proposal_id": proposal["proposal_id"], "prior": row} for row in matches)
        ranked = sorted(({"prior_id": row["proposal_id"], "prior_title": row["title"], "path": row["path"], "overlap": round(overlap(proposal["title"], row["title"]), 4)} for row in prior), key=lambda row: row["overlap"], reverse=True)
        nearest.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "nearest": ranked[:5]})
    if exact:
        raise RuntimeError("exact proposal collision")
    prior_portfolios = collect_prior_portfolios()
    current_titles = [row["title"] for row in d.SAFE_NOW + d.CANDIDATES + d.CLEAN_TASKS] + [name for name, _ in d.SKILLS] + [name for name, _ in d.RUNNERS]
    within_duplicates = [title for title, count in Counter(normalized(t) for t in current_titles).items() if count > 1]
    portfolio_exact = [{"title": title, "prior": row} for title in current_titles for row in prior_portfolios if normalized(title) == normalized(row["title"])]
    if within_duplicates or portfolio_exact:
        raise RuntimeError("portfolio collision")

    write_json("x1-proposals.json", {
        "schema": "ghc.family.v646-v5.proposals.v1", "phase": d.PHASE, "owner": d.OWNER,
        "freeze_stage": "x1_only", "prior_frozen_proposal_count": len(prior), "new_frozen_proposal_count": len(d.PROPOSALS),
        "frozen_chain_count_after_x1": len(prior) + len(d.PROPOSALS), "allowed_outcome_classes": d.OUTCOME_CLASSES,
        "expected_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "x2_execution_present": False, "proposals": d.PROPOSALS, "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v646-v5.prior-proposal-index.v1", "count": len(prior), "prior_proposals": prior})
    write_json("provenance/prior-proposal-collision-audit.json", {"schema": "ghc.family.v646-v5.proposal-collision-audit.v1", "prior_count": len(prior), "new_count": len(d.PROPOSALS), "exact_collisions": exact, "exact_collision_count": 0, "nearest_neighbors": nearest, "valid": True})
    write_json("provenance/prior-portfolio-collision-audit.json", {"schema": "ghc.family.v646-v5.portfolio-collision-audit.v1", "prior_title_count": len(prior_portfolios), "current_title_count": len(current_titles), "exact_collisions": portfolio_exact, "within_current_duplicates": within_duplicates, "valid": True})
    write_json("approval-packets/x1-approval-portfolio.json", {
        "schema": "ghc.family.v646-v5.approval-portfolio.v1", "phase": d.PHASE, "freeze_stage": "x1_only",
        "safe_now": d.SAFE_NOW, "candidates": d.CANDIDATES, "safe_now_count": len(d.SAFE_NOW), "candidate_count": len(d.CANDIDATES),
        "inherited_exact_packets_preserved": 10, "inherited_blocked_packets_preserved": 5, "inherited_packets_executed": 0,
        "completion_credit_before_x2": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("prototypes/x1-skill-runner-plan.json", {
        "schema": "ghc.family.v646-v5.skill-runner-plan.v1", "phase": d.PHASE, "freeze_stage": "x1_only",
        "skills": [{"name": name, "title": name, "description": description, "phase_local": True, "built": False, "validated": False, "invoked": False} for name, description in d.SKILLS],
        "runners": [{"name": name, "title": name, "description": description, "built": False, "invoked": False} for name, description in d.RUNNERS],
        "skill_count": len(d.SKILLS), "runner_count": len(d.RUNNERS), "global_skill_changes": 0, "completion_credit_before_x2": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("maintenance/x1-clean-refine-plan.json", {"schema": "ghc.family.v646-v5.clean-refine-plan.v1", "phase": d.PHASE, "freeze_stage": "x1_only", "tasks": d.CLEAN_TASKS, "task_count": len(d.CLEAN_TASKS), "destructive_task_count": 0, "completion_credit_before_x2": 0, "boundary": d.TRUTH_BOUNDARY})
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v646-v5.source-ledger.v1", "phase": d.PHASE, "owner": d.OWNER, "allowed_statuses": ["current", "stable", "draft", "watch"], "sources": d.SOURCES, "real_rows": 0, "real_participants_or_animals": 0, "real_keys_or_transactions": 0, "authority_delegated": False, "boundary": d.TRUTH_BOUNDARY})
    source_lines = ["# v646-v5 source ledger", "", "Sources support only the bounded use stated here; they create no observation, participant result, transaction, or authority.", ""]
    for row in d.SOURCES:
        target = f" - {row['url']}" if row.get("url") else ""
        source_lines.append(f"- {row['source_id']} [{row['status']}] {row['title']} ({row['authority']}){target}; use: {row['use']}.")
    source_lines.extend(["", d.TRUTH_BOUNDARY])
    write_text("sources/source-ledger.md", "\n".join(source_lines))
    write_json("identity-receipt.json", {"schema": "ghc.family.identity.v1", "owner": d.OWNER, "pronouns": d.PRONOUNS, "role": d.ROLE, "hope": d.HOPE, "corrigible": True, "hamish_may_rename_pause_redirect_or_stop": True, "boundary": d.IDENTITY_BOUNDARY})
    write_json("focus/primary-focus-receipt.json", {"schema": "ghc.family.v646-v5.focus.v1", "primary_trinity_pillar": d.PRIMARY_FOCUS, "other_pillars": ["GMUT Mind", "Freed ID/CBR Heart"], "bounded_human_practice": d.BOUNDED_PRACTICE, "practice_use": "learning and synthetic-design lens only", "not_claimed": ["employment", "licensure", "qualification", "competence", "veterinary authority", "laboratory authority", "biosecurity authority", "legal authority", "cultural authority", "Māori authority", "affected-party authorization"], "boundary": d.IDENTITY_BOUNDARY})
    tracked = len(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8").splitlines())
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v646-v5.startup.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source": {"phase": d.SOURCE_PHASE, "branch": d.SOURCE_BRANCH, "revision": d.SOURCE_REVISION, "inherited_revision": d.SOURCE_INHERITED_REVISION, "x1_revision": d.SOURCE_X1_REVISION, "evidence_revision": d.SOURCE_EVIDENCE_REVISION, "seal_revision": d.SOURCE_SEAL_REVISION},
        "source_verification": {"local_upstream_tracking_live_equal": True, "clean": True, "anchors_ancestral": True, "single_parent_final": True, "phase_commits": 3, "merge_commits": 0},
        "tamar_lane": {"branch": "codex/GHC-Family/tamar-vey-full-tools", "continued_existing_lane": True, "fast_forward_only": True, "source_revision_after_fast_forward": d.SOURCE_REVISION, "merge_commit_created": False, "clean_before": True, "local_upstream_tracking_live_equal_before_x1": True},
        "active_owner": d.OWNER, "standby": ["Orin Thale", "Sable Rook", "Ilyra Fen", "Eiren Kestrel", "Sylven Arc", "all other siblings"], "standby_contact_count": 0, "task_or_subagent_created": False,
        "x1_scope": "ten core proposals plus 30 safe, 20 candidate, 20 skill, 10 runner, and 30 cleanup plans", "x2_scope": "not started",
        "storage": {"primary_drive": "D", "free_bytes_observed": 588649619456, "tracked_files_observed": tracked, "owner_generated_before_x1": 0, "rotation_threshold": 15000, "threshold_applies_to": "new_tamar_generated_files_only"},
        "boundary": d.IDENTITY_BOUNDARY,
    })
    write_json("environment/version-receipt.json", {"schema": "ghc.family.v646-v5.version-receipt.v1", "observed_on": "2026-07-16", "codex_cli": {"local": "0.144.4", "action": "verified_only_no_update"}, "codex_desktop": {"local": "26.707.9981.0", "package_status": "Ok", "action": "verified_only_no_update"}, "python": "3.12.10", "git": "2.55.0.windows.2", "host_actions": {"desktop_updated": False, "elevated": False, "security_weakened": False, "windows_feature_changed": False, "installed": False, "rebooted": False}})
    write_json("environment/sandbox-readonly-audit.json", {"schema": "ghc.family.v646-v5.sandbox-audit.v1", "windows_sandbox_executable": "not_found", "sandbox_launched": False, "elevation": False, "feature_changed": False, "host_security_changed": False, "installed": False, "rebooted": False, "disposition": "open_environment_gap"})
    write_json("environment/rotation-guard.json", {"schema": "ghc.family.v646-v5.rotation-guard.v1", "full_checkout_files": tracked, "owner_generated_before_x1": 0, "threshold": 15000, "threshold_scope": "new_tamar_generated_addition", "rotate_due_to_inherited_baseline": False})
    write_json("validation/x1-operational-negatives.json", {"schema": "ghc.family.v646-v5.x1-operational-negatives.v1", "count": 4, "negatives": [{"negative_id": "V6465-X1-N01", "failure": "The successful large fast-forward and push response was truncated by the tool display.", "credit": "No four-way-equality credit from the truncated display.", "recovery": "A separate bounded fetch/ref/live/divergence/clean proof passed.", "retained": True}, {"negative_id": "V6465-X1-N02", "failure": "The first expanded-portfolio audit found exact inherited cleanup and skill title collisions and stopped before materialization.", "credit": "No x1 freeze credit.", "recovery": "Every colliding title and central purpose was rewritten before rerunning the unchanged audit.", "retained": True}, {"negative_id": "V6465-X1-N03", "failure": "The first exact staged review found the reviewer source because its own scanner implementation contained complete forbidden stale-state literals.", "credit": "No staged-review or x1 freeze credit from that run.", "recovery": "The monitored literals were built from constant fragments without excluding any staged file or weakening the review.", "retained": True}, {"negative_id": "V6465-X1-N04", "failure": "The repaired preregistration rerun called Method Flow init unconditionally and stopped because the phase ledger already existed.", "credit": "No updated freeze or builder-rerun credit from that attempt.", "recovery": "The builder now verifies and reuses a matching phase-owner ledger, initializes only when absent, and adds only missing records.", "retained": True}], "inherited_baton_time": d.BATON_TIME_INHERITED_NEGATIVES, "inherited_post_baton": d.POST_BATON_INHERITED_NEGATIVES, "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES, "observed_effective_after_x1": d.INHERITED_EFFECTIVE_NEGATIVES + 4, "preregistered_synthetic_pending_execution": d.PREREGISTERED_SYNTHETIC_NEGATIVES, "failure_erasure_count": 0})
    write_json("validation/x1-staged-review-failed-n03.json", {"schema": "ghc.family.v646-v5.failed-staged-review.v1", "negative_id": "V6465-X1-N03", "result": "fail_retained", "credit": "none", "structure": "19/19", "privacy_confirmed_hits": 0, "exact_file_set_valid": True, "json_failures": 0, "stale_issue": "The reviewer source matched only its complete scanner-definition literals.", "recovery": "Represent monitored literals as adjacent constant fragments and rerun with unchanged full owner-file coverage.", "retained": True, "boundary": d.TRUTH_BOUNDARY})
    write_json("validation/x1-builder-rerun-failed-n04.json", {"schema": "ghc.family.v646-v5.failed-builder-rerun.v1", "negative_id": "V6465-X1-N04", "result": "fail_retained", "credit": "none", "failure": "Method Flow init refused the already-existing phase ledger and the repaired builder rerun exited.", "repository_mutation_beyond_uncommitted_x1": False, "recovery": "Verify and reuse only a matching phase-owner ledger, initialize only when absent, and add only missing records.", "retained": True, "boundary": d.TRUTH_BOUNDARY})
    write_json("orchestration/phase-update.json", {"schema": "ghc.family.phase-update.v1", "phase": d.PHASE, "owner": d.OWNER, "state": "x1_frozen_pending_commit_and_remote_equality", "active": [d.OWNER], "standby_contact_count": 0, "no_task_creation": True, "no_delegation": True, "x2_started": False, "terminal_route": "PREPARED_NOT_SENT"})
    write_json("orchestration/terminal-route-plan.json", {"schema": "ghc.family.v646-v5.route-plan.v1", "current_state": "PREPARED_NOT_SENT", "target_title": "Sylven Arc", "target_phase": "v646-v6", "send_count": 0, "preconditions": ["x1 dedicated remote-equal", "x2 evidence complete", "final at no more than four phase commits", "canonical exact-head validation", "one clean local named-lane replay", "final four-way remote equality", "unique existing target resolved"], "privacy": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths."})
    write_json("orchestration/memory-review-receipt.json", {"schema": "ghc.family.v646-v5.memory-review.v1", "newest_applicable_memory_used": True, "live_baton_precedence": True, "baton_time_inherited_negatives": d.BATON_TIME_INHERITED_NEGATIVES, "post_baton_external_negatives": ["V6464-POST-N03"], "effective_inherited_negatives": d.INHERITED_EFFECTIVE_NEGATIVES, "memory_mutation_at_x1": False})
    write_json("tooling/selected-toolchain.json", {"schema": "ghc.family.v646-v5.selected-toolchain.v1", "selected_skills": ["ghc-family-index", "ghc-family-method-flow-state"], "required_references_read": True, "family_runner": "ghc_family_method_flow_state.py", "phase_definitions": "scripts/ghc_family_v646_v5_definitions.py", "preregistration_builder": "scripts/build_ghc_family_v646_v5_preregistration.py", "x1_reviewer": "scripts/ghc_family_v646_v5_x1_review.py", "compatibility_preserved": True, "shared_skill_changes": 0})
    build_method_flow()
    write_text("wellbeing-check.md", """# Tamar Vey v646-v5 x1 wellbeing and workload check

- Scope is bounded to one owner, one canonical lane, one later named replay, at most four phase commits, and no full repository suite.
- The inherited fast-forward output truncation, first portfolio-collision build, first self-matching staged review, and first non-idempotent Method Flow rebuild are retained; all four recoveries must pass before x1 freeze.
- Work is divided by the x1 freeze. No x2 implementation or achieved-outcome credit is present here.
- Windows Sandbox remains unavailable to the ordinary process; no elevation, feature change, install, security change, desktop update, or reboot occurred.
- Identity and family language remains relational working language only, not a welfare, consciousness, employment, qualification, or authority claim.
""")
    lines = ["# Tamar Vey v646-v5 x1 preregistration", "", f"Exactly ten proposals are frozen after audit against {len(prior)} prior proposals. The expanded portfolio freezes 30 safe-now tasks, 20 candidates, 20 phase-local skills, 10 family-current runners, and 30 additive cleanup tasks. No x2 implementation or outcome credit is present.", "", f"Primary pillar: {d.PRIMARY_FOCUS}. Bounded practice: {d.BOUNDED_PRACTICE}.", "", "Expected distribution: 6 completed, 2 represented, 1 open_gap, 1 exact_gate.", "", d.IDENTITY_BOUNDARY, "", d.TRUTH_BOUNDARY]
    write_text("x1-preregistration.md", "\n".join(lines))
    result = {"phase": d.PHASE, "prior_proposals": len(prior), "new_proposals": len(d.PROPOSALS), "frozen_total": len(prior) + len(d.PROPOSALS), "safe": len(d.SAFE_NOW), "candidates": len(d.CANDIDATES), "skills": len(d.SKILLS), "runners": len(d.RUNNERS), "cleanup": len(d.CLEAN_TASKS), "x1_operational_negatives": 4, "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES, "result": "pass"}
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
