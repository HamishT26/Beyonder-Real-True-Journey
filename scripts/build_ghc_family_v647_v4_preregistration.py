#!/usr/bin/env python3
"""Build the Sylven Arc v647-v4 x1-only preregistration packet."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v647_v4_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sylven-arc/v647-v4")
PHASE = ROOT / PHASE_REL
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def frozen_chain() -> list[dict[str, str]]:
    prior = load("docs/tamar-vey/v647-v3/provenance/frozen-chain-proposal-index.json")["prior_proposals"]
    tamar = load("docs/tamar-vey/v647-v3/x1-proposals.json")["proposals"]
    rows = [{"path": row["path"], "proposal_id": row["proposal_id"], "title": row["title"]} for row in prior]
    rows.extend(
        {"path": "docs/tamar-vey/v647-v3/x1-proposals.json", "proposal_id": row["proposal_id"], "title": row["title"]}
        for row in tamar
    )
    if len(rows) != d.PRIOR_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN_PROPOSALS} frozen proposals, found {len(rows)}")
    if len({row["proposal_id"] for row in rows}) != len(rows):
        raise RuntimeError("prior proposal identifiers are not unique")
    return rows


def collision_audit(prior: list[dict[str, str]]) -> dict[str, Any]:
    audits = []
    prior_titles = {row["title"].casefold() for row in prior}
    for proposal in d.PROPOSALS:
        mine = tokens(proposal["title"])
        scored = []
        for row in prior:
            theirs = tokens(row["title"])
            score = len(mine & theirs) / len(mine | theirs)
            scored.append({"proposal_id": row["proposal_id"], "title": row["title"], "jaccard": round(score, 6)})
        scored.sort(key=lambda row: (-row["jaccard"], row["proposal_id"]))
        audits.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "exact_title_collision": proposal["title"].casefold() in prior_titles,
                "nearest_neighbors": scored[:5],
                "maximum_jaccard": scored[0]["jaccard"],
                "semantic_distinction": proposal["novelty_against_prior_frozen_proposals"],
                "novelty_gate_passed": proposal["title"].casefold() not in prior_titles and scored[0]["jaccard"] < 0.5,
            }
        )
    return {
        "schema": "ghc.family.v647-v4.proposal-collision-audit.v1",
        "prior_count": len(prior),
        "candidate_count": len(audits),
        "method": "exact case-folded title comparison plus token-set Jaccard nearest-neighbor review and explicit semantic distinction",
        "threshold": "no exact collision and maximum Jaccard below 0.5",
        "audits": audits,
        "passed": sum(row["novelty_gate_passed"] for row in audits),
        "valid": all(row["novelty_gate_passed"] for row in audits),
        "boundary": d.TRUTH_BOUNDARY,
    }


def method_call(*args: str) -> None:
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
    )


def build_method_flow() -> None:
    ledger = PHASE / "method-flow/method-flow-state.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    if not ledger.exists():
        method_call("init", "--ledger", str(ledger), "--phase", d.PHASE + "-x1", "--owner", d.OWNER)
    for spec in d.METHOD_SPECS:
        suffix = spec["method_id"].split("-")[-1].lower()
        record_rel = f"method-flow/v6474-{suffix}-method-record.json"
        failed_rel = f"method-flow/v6474-{suffix}-failed-witness.json"
        passed_rel = f"method-flow/v6474-{suffix}-passing-witness.json"
        write_json(
            record_rel,
            {
                "method_id": spec["method_id"], "title": spec["title"], "failure_signature": spec["failure_signature"],
                "trigger_preconditions": spec["trigger_preconditions"], "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_scoped_workflow", "candidate_workaround": spec["candidate_workaround"],
                "validation_witness_ids": [], "recurrence_guard": spec["recurrence_guard"], "rollback": spec["rollback"],
                "recommendation_state": "candidate", "supersedes": [], "protected_gates": spec["protected_gates"],
                "retained_negative_ids": spec["retained_negative_ids"],
                "scope_boundary": "Owner-local x1 startup recovery only; no scientific, professional, production, authority, or independent-reproduction credit.",
            },
        )
        write_json(
            failed_rel,
            {
                "witness_id": spec["method_id"] + "-W-F", "method_id": spec["method_id"],
                "procedure": "Original read-only startup attempt retained from execution.", "scope": "Sylven v647-v4 source verification",
                "expected": "The bounded structured diagnostic returns a complete result.", "observed": spec["failed_observed"],
                "result": "fail", "same_owner_only": True, "independent_reproduction": False,
                "retained_negative_ids": spec["retained_negative_ids"], "boundary": d.TRUTH_BOUNDARY,
            },
        )
        write_json(
            passed_rel,
            {
                "witness_id": spec["method_id"] + "-W-P", "method_id": spec["method_id"],
                "procedure": spec["candidate_workaround"], "scope": "Sylven v647-v4 bounded startup recovery",
                "expected": "The recovery passes without weakening protected gates.", "observed": spec["pass_observed"],
                "result": "pass", "same_owner_only": True, "independent_reproduction": False,
                "retained_negative_ids": spec["retained_negative_ids"], "boundary": d.TRUTH_BOUNDARY,
            },
        )
        current = json.loads(ledger.read_text(encoding="utf-8"))
        if not any(row.get("method_id") == spec["method_id"] for row in current.get("methods", [])):
            method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / record_rel))
        current = json.loads(ledger.read_text(encoding="utf-8"))
        for relative, witness_id in ((failed_rel, spec["method_id"] + "-W-F"), (passed_rel, spec["method_id"] + "-W-P")):
            if not any(row.get("witness_id") == witness_id for row in current.get("witnesses", [])):
                method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / relative))
                current = json.loads(ledger.read_text(encoding="utf-8"))
        method = next(row for row in current["methods"] if row["method_id"] == spec["method_id"])
        if method.get("recommendation_state") != "preferred":
            method_call("set-state", "--ledger", str(ledger), "--method-id", spec["method_id"], "--state", "preferred", "--note", "Validated only for the declared startup trigger; failed witness retained.")
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/runner-validation.json"))
    method_call("summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"))


def main() -> int:
    PHASE.mkdir(parents=True, exist_ok=True)
    prior = frozen_chain()
    collision = collision_audit(prior)
    if not collision["valid"]:
        raise RuntimeError("semantic novelty gate failed")
    distribution = {name: sum(p["expected_disposition"] == name for p in d.PROPOSALS) for name in d.OUTCOME_CLASSES}
    write_json("identity-receipt.json", {"schema": "ghc.family.v647-v4.identity.v1", "owner": d.OWNER, "pronouns": d.PRONOUNS, "role": d.ROLE, "hope": d.HOPE, "corrigible_by_hamish": True, "boundary": d.IDENTITY_BOUNDARY})
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v647-v4.prior-proposal-index.v1", "count": len(prior), "prior_proposals": prior})
    write_json("provenance/proposal-collision-audit.json", collision)
    write_json(
        "x1-proposals.json",
        {
            "schema": "ghc.family.v647-v4.x1-proposals.v1", "phase": d.PHASE, "owner": d.OWNER,
            "source_phase": d.SOURCE_PHASE, "source_revision": d.SOURCE_REVISION,
            "prior_frozen_proposal_count": len(prior), "new_frozen_proposal_count": len(d.PROPOSALS),
            "frozen_chain_count_after_x1": len(prior) + len(d.PROPOSALS), "outcome_classes": d.OUTCOME_CLASSES,
            "expected_distribution": distribution, "expected_counts_are_results": False, "x2_execution_present": False,
            "x1_freeze_rule": "No x2 implementation, mutation execution, outcome, or completion credit exists in this packet.",
            "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE,
            "identity_boundary": d.IDENTITY_BOUNDARY, "boundary": d.TRUTH_BOUNDARY, "proposals": d.PROPOSALS,
        },
    )
    lines = ["# Sylven Arc v647-v4 x1 preregistration", "", d.IDENTITY_BOUNDARY, "", f"Primary focus: **{d.PRIMARY_FOCUS}**.", f"Bounded practice: **{d.BOUNDED_PRACTICE}**.", "", "Exactly ten proposals are frozen below. Expected dispositions are hypotheses, not results. X2 execution is absent.", ""]
    for p in d.PROPOSALS:
        lines.extend([
            f"## {p['proposal_id']} — {p['title']}", "", f"- Hypothesis: {p['hypothesis']}",
            f"- Null/failure: {p['null_or_failure']}", f"- Approval class: `{p['approval_class']}`",
            f"- Execution lane: `{p['execution_lane']}`", f"- Official or primary sources: {', '.join(p['current_primary_or_official_source_needs'])}",
            f"- Concrete artifacts: {', '.join(p['concrete_artifacts'])}", f"- Falsifier/acceptance gate: {p['test_falsifier_or_acceptance_gate']}",
            f"- Rollback/recovery: {p['rollback_or_recovery']}", f"- Protected gates: {', '.join(p['protected_gates'])}",
            f"- Expected disposition: `{p['expected_disposition']}`", f"- Novelty: {p['novelty_against_prior_frozen_proposals']}", "",
        ])
    write_text("x1-preregistration.md", "\n".join(lines))
    sources = [
        {"source_id": sid, "status": status, "authority_class": authority, "title": title, "url": url, "use": use, "accessed_utc": "2026-07-16T20:00:00Z", "observation_credit": False, "authority_delegated": False}
        for sid, status, authority, title, url, use in d.SOURCES
    ]
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v647-v4.source-ledger.v1", "allowed_statuses": ["current", "stable", "draft", "watch"], "sources": sources, "source_count": len(sources), "boundary": d.TRUTH_BOUNDARY})
    write_text("sources/source-ledger.md", "# v647-v4 source ledger\n\n" + "\n".join(f"- **{s['source_id']}** `{s['status']}` — [{s['title']}]({s['url']}): {s['use']}" for s in sources) + "\n\nSources supply requirements and provenance only; they are not observations, legal advice, cultural ratification, or delegated authority.")
    safe = [{"packet_id": f"V6474-X1-SAFE-{i:02d}", "title": title, "approval_class": "safe_now_owner_scoped", "planned_execution": "x2", "completion_credit": False} for i, title in enumerate(d.SAFE_TASK_TITLES, 1)]
    candidates = [{"packet_id": f"V6474-X1-CAND-{i:02d}", "title": title, "approval_class": "bounded_candidate", "planned_execution": "x2_if_falsifier_available", "completion_credit": False} for i, title in enumerate(d.CANDIDATE_TITLES, 1)]
    exact = [{"packet_id": f"V6474-X1-EXACT-{i:02d}", "title": title, "approval_class": "exact_approval_or_external_evidence_required", "planned_execution": "none", "completion_credit": False} for i, title in enumerate(d.EXACT_PACKET_TITLES, 1)]
    blocked = [{"packet_id": f"V6474-X1-BLOCK-{i:02d}", "title": title, "approval_class": "blocked", "planned_execution": "none", "completion_credit": False} for i, title in enumerate(d.BLOCKED_PACKET_TITLES, 1)]
    write_json("approval-packets/x1-approval-portfolio.json", {"schema": "ghc.family.v647-v4.x1-portfolio.v1", "safe_now_count": len(safe), "candidate_count": len(candidates), "exact_count": len(exact), "blocked_count": len(blocked), "safe_now": safe, "candidates": candidates, "exact": exact, "blocked": blocked, "x2_execution_present": False, "boundary": d.TRUTH_BOUNDARY})
    skills = [{"skill_id": f"V6474-X1-SKILL-{i:02d}", "name": name, "purpose": purpose, "build_state": "planned_for_x2", "global_install": False, "completion_credit": False} for i, (name, purpose) in enumerate(d.SKILL_SPECS, 1)]
    runners = [{"runner_id": f"V6474-X1-RUN-{i:02d}", "name": name, "family_current_name": name.startswith("ghc_family_"), "build_state": "planned_for_x2", "completion_credit": False} for i, name in enumerate(d.RUNNER_TITLES, 1)]
    write_json("prototypes/x1-skill-runner-plan.json", {"schema": "ghc.family.v647-v4.x1-skill-runner-plan.v1", "skill_count": len(skills), "runner_count": len(runners), "skills": skills, "runners": runners, "x2_implementation_present": False, "boundary": d.TRUTH_BOUNDARY})
    cleanup = [{"task_id": f"V6474-X1-CLEAN-{i:02d}", "title": title, "class": ["CLEAN", "FIX", "REFINE"][(i - 1) % 3], "execution_state": "planned_for_x2", "completion_credit": False} for i, title in enumerate(d.CLEAN_TASK_TITLES, 1)]
    write_json("maintenance/x1-clean-refine-plan.json", {"schema": "ghc.family.v647-v4.x1-clean-refine-plan.v1", "count": len(cleanup), "tasks": cleanup, "x2_execution_present": False, "boundary": d.TRUTH_BOUNDARY})
    mutations = [{"negative_id": f"V6474-P{i:02d}-SYN-{j:02d}", "proposal_id": f"V6474-P{i:02d}", "mutation_index": j, "execution_state": "preregistered_not_executed", "expected_result": "reject", "accepted": None, "retained": True} for i in range(1, 11) for j in range(1, 8)]
    write_json("validation/x1-synthetic-mutation-plan.json", {"schema": "ghc.family.v647-v4.x1-synthetic-plan.v1", "count": len(mutations), "executed": 0, "rejected": 0, "mutations": mutations, "boundary": d.TRUTH_BOUNDARY})
    write_json("validation/x1-operational-negatives.json", {"schema": "ghc.family.v647-v4.x1-negatives.v1", "count": len(d.X1_NEGATIVES), "negatives": d.X1_NEGATIVES, "failure_erasure_count": 0})
    write_json("retained-negative-register.json", {"schema": "ghc.family.v647-v4.retained-negatives.v1", "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES, "x1_operational": len(d.X1_NEGATIVES), "preregistered_synthetic_planned_not_effective": d.PREREGISTERED_SYNTHETIC_NEGATIVES, "effective_total": d.INHERITED_EFFECTIVE_NEGATIVES + len(d.X1_NEGATIVES), "no_negative_erased": True, "failure_erasure_count": 0, "same_owner_only": True, "boundary": d.TRUTH_BOUNDARY})
    write_json("exact-open-gate-register.json", {"schema": "ghc.family.v647-v4.gates.v1", "inherited_open_gaps": d.INHERITED_OPEN_GAPS, "inherited_exact_gates": d.INHERITED_EXACT_GATES, "preregistered_open_gap_additions": 1, "preregistered_exact_gate_additions": 1, "current_effective_open_gaps": d.INHERITED_OPEN_GAPS, "current_effective_exact_gates": d.INHERITED_EXACT_GATES, "expected_after_x2_open_gaps": d.INHERITED_OPEN_GAPS + 1, "expected_after_x2_exact_gates": d.INHERITED_EXACT_GATES + 1, "silently_closed": 0, "boundary": d.TRUTH_BOUNDARY})
    write_json("x1-gate-carry-forward.json", {"schema": "ghc.family.v647-v4.x1-gate-carry-forward.v1", "protected_gate_count": len({gate for p in d.PROPOSALS for gate in p["protected_gates"]}), "no_gate_closed": True, "real_world_action_count": 0, "x2_execution_present": False, "boundary": d.TRUTH_BOUNDARY})
    write_json("phase-truth.json", {"schema": "ghc.family.v647-v4.phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "source_revision": d.SOURCE_REVISION, "lifecycle": "x1_frozen_uncommitted", "strict_x1_before_x2": True, "prior_frozen_proposals": len(prior), "new_frozen_proposals": len(d.PROPOSALS), "frozen_after_x1": len(prior) + len(d.PROPOSALS), "expected_distribution": distribution, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "x2_execution_present": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": d.TRUTH_BOUNDARY})
    write_json("environment/startup-receipt.json", {"schema": "ghc.family.v647-v4.startup.v1", "source_branch": d.SOURCE_BRANCH, "source_revision": d.SOURCE_REVISION, "source_x1_revision": d.SOURCE_X1_REVISION, "source_evidence_revision": d.SOURCE_EVIDENCE_REVISION, "source_clean_and_remote_equal": True, "sylven_lane_fast_forward_only": True, "d_drive_first": True, "d_free_bytes_at_start": 585794584576, "host_mutation": False})
    write_json("environment/version-receipt.json", {"schema": "ghc.family.v647-v4.versions.v1", "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0", "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8875", "windows_sandbox_available_to_ordinary_process": False, "verified_only": True, "updates_or_installs": 0, "elevation": False, "security_or_feature_changes": 0, "reboot": False})
    write_json("environment/rotation-guard.json", {"schema": "ghc.family.v647-v4.rotation.v1", "threshold": 15000, "scope": "new Sylven v647-v4 owner-generated files only", "inherited_files_counted": False, "rotation_required": False})
    write_json("orchestration/memory-review-receipt.json", {"schema": "ghc.family.v647-v4.memory-review.v1", "newest_same_day_tamar_v647_v3_note_reviewed": True, "live_baton_authoritative": True, "older_memory_used_as_context_only": True, "private_material_published": False})
    write_json("orchestration/phase-update.json", {"schema": "ghc.family.v647-v4.phase-update.v1", "state": "ACTIVE_X1", "owner": d.OWNER, "active_siblings": [d.OWNER], "standby_siblings": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey"], "terminal_route": "PREPARED_NOT_SENT", "task_created": False, "subagents_spawned": 0})
    write_json("tooling/selected-toolchain.json", {"schema": "ghc.family.v647-v4.toolchain.v1", "selected": ["ghc-family-index", "ghc-family-method-flow-state", "ghc_family_method_flow_state.py"], "selection_reason": "Current family index and append-only Method Flow are the minimum startup toolchain; phase-local builders preserve caller compatibility.", "historical_tools_are_compatibility_only": True})
    write_json("threat-model.json", {"schema": "ghc.family.v647-v4.threat-model.v1", "assets": ["x1/x2 separation", "proposal novelty", "retained negatives", "authority gates", "privacy exclusions", "manifest integrity", "remote equality"], "threats": ["x2 leakage into x1", "proposal relabeling", "failed-witness erasure", "source-as-observation conversion", "synthetic-to-production promotion", "private material publication", "authority substitution", "line-ending hash drift", "sibling lane mutation"], "controls": ["dedicated x1 commit", "500-title collision audit", "append-only Method Flow", "zero-row counters", "five-class scan", "commit-local manifests", "fast-forward-only owned lane", "one-shot route gate"], "residual_risk": "Manual, participant, professional, legal, cultural, Māori-authority, accessibility, security, production, empirical, independent-reproduction, and Stage 20 work remains open or exact-gated.", "boundary": d.TRUTH_BOUNDARY})
    write_json("wellbeing-check.json", {"schema": "ghc.family.v647-v4.wellbeing.v1", "owner": d.OWNER, "pace": "bounded and evidence-first", "pressure_to_overclaim": "rejected", "permission_to_pause_or_stop": True, "failure_retention": "one startup negative retained with one bounded passing witness", "identity_boundary": d.IDENTITY_BOUNDARY})
    write_text("wellbeing-check.md", "# Sylven Arc v647-v4 wellbeing check\n\nWork remains bounded, corrigible, and pauseable. One startup parser failure is retained rather than hidden. Warmth or continuity language grants no authority, and no missing evidence is converted into completion credit.")
    build_method_flow()
    owner_files = sum(path.is_file() for path in PHASE.rglob("*"))
    write_json("environment/owner-file-count.json", {"schema": "ghc.family.v647-v4.owner-files.v1", "owner_files_after_preregistration": owner_files + 1, "threshold": 15000, "under_threshold": owner_files + 1 < 15000, "inherited_files_counted": False})
    print(json.dumps({"phase": d.PHASE_SHORT, "proposals": len(d.PROPOSALS), "prior": len(prior), "safe": len(safe), "candidates": len(candidates), "skills": len(skills), "runners": len(runners), "cleanup": len(cleanup), "synthetic_planned": len(mutations), "x1_negatives": len(d.X1_NEGATIVES), "result": "pass"}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
