#!/usr/bin/env python3
"""Build the x1-only Eiren v651-v5 (2) remaster preregistration packet."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5-2-remaster"
SOURCE = "2bb6aa2d5e8003c4cb522f798d59e7b7f123742c"
PHASE = "v651-v5-2-remaster"
OWNER = "Eiren Kestrel"


PROPOSAL_SPECS = [
    ("meta-toolbox-catalogue-contract", "THOS Body", "Build a deterministic family-current catalogue that ranks reusable skills, runners, commands, methods, and workflows without executing every discovered surface.", "completed"),
    ("meta-toolbox-query-runner", "THOS Body", "Build a read-only query runner that filters the catalogue by kind, status, trigger, owner scope, and evidence state.", "completed"),
    ("skill-trigger-collision-board", "THOS Body", "Detect overlapping skill descriptions and preserve collisions as review issues rather than selecting silently.", "completed"),
    ("runner-caller-compatibility-map", "THOS Body", "Map repository callers before any reusable runner is merged, deprecated, or promoted.", "completed"),
    ("global-promotion-readiness-tribunal", "THOS Body", "Classify global promotion as ready, candidate, or exact-gated from validation, caller, rollback, and ownership evidence.", "completed"),
    ("tool-staleness-scorecard", "THOS Body", "Score candidate staleness from naming, caller, validation, and supersession evidence without deleting history.", "completed"),
    ("method-flow-recommendation-index", "THOS Body", "Index preferred Method Flow recommendations by trigger and protected gate while retaining failed witnesses.", "completed"),
    ("d-first-rotation-receipt", "THOS Body", "Bind additive D-first rotation to exact source, clean state, owner-growth threshold, and no destructive cleanup.", "completed"),
    ("commit-budget-state-machine", "THOS Body", "Enforce separate x1 and x2 commit ceilings and fail closed on mixed lifecycle content.", "completed"),
    ("single-pass-validation-planner", "THOS Body", "Reserve one successful canonical pass while retaining failed attempts and allowing isolated blocker diagnosis.", "completed"),
    ("plugin-capability-inventory", "THOS Body", "Record available plugin capability surfaces without treating availability as permission or installing unrelated plugins.", "completed"),
    ("cli-sibling-readiness-contract", "THOS Body", "Represent the future CLI sibling induction boundary without creating a sibling before the scheduled phase.", "represented"),
    ("cli-return-route-contract", "THOS Body", "Represent a parent-return routing contract without claiming unsupported peer-to-peer communication.", "represented"),
    ("document-volume-budget-board", "THOS Body", "Enforce ordinary document readability and a bounded large-baton exception without turning word caps into quotas.", "completed"),
    ("five-class-private-material-scan", "Freed ID and CBR Heart", "Scan owner artifacts for raw identifiers, private paths, private URIs, delegation markup, and credential assignments.", "completed"),
    ("accessible-catalogue-report", "Freed ID and CBR Heart", "Build a structurally accessible static catalogue report while reserving manual and affected-user evaluation.", "completed"),
    ("capability-card-manifest", "THOS Body", "Bind every promoted catalogue card to source path, content hash, evidence state, and rollback note.", "completed"),
    ("workflow-route-conflict-ledger", "Freed ID and CBR Heart", "Preserve conflicting long-route assignments while allowing only the unambiguous immediate successor transition.", "completed"),
    ("tool-provenance-chain", "Freed ID and CBR Heart", "Preserve owner, source commit, compatibility status, and validation provenance for each selected tool.", "completed"),
    ("meta-toolbox-mutation-tribunal", "THOS Body", "Reject malformed catalogue entries, unsafe install requests, missing rollback fields, and unproven deletion requests.", "completed"),
    ("gmut-coefficient-identifiability-board", "GMUT Mind", "Classify symbolic coefficient identifiability obligations without converting typed structure into empirical evidence.", "completed"),
    ("gmut-dimensional-domain-board", "GMUT Mind", "Check typed dimensional and domain obligations for a bounded Mandala equation representation without a force or Theory-of-Everything claim.", "completed"),
    ("gmut-real-data-adapter", "GMUT Mind", "Reserve a current primary-source observational adapter and refuse likelihood or constraint claims when zero real rows are ingested.", "open_gap"),
    ("thos-digital-preservation-handover", "THOS Body", "Represent checksum, fixity, quarantine, escalation, workload, and shift-handover states on synthetic archive fixtures only.", "represented"),
    ("thos-format-migration-stop-work", "THOS Body", "Represent format-migration stop-work and rollback decisions on synthetic fixtures with no real collection authority.", "represented"),
    ("freed-id-tool-attestation-profile", "Freed ID and CBR Heart", "Represent signed catalogue-attestation fields with synthetic vectors and no production keys or trust governance.", "represented"),
    ("cbr-tool-lifecycle-authority-matrix", "Freed ID and CBR Heart", "Reserve deletion, global installation, legal, cultural, affected-party, data-governance, and Maori-authority decisions.", "exact_gate"),
    ("landauer-nonconversion-classifier", "GMUT Mind", "Classify Landauer information-erasure assumptions while rejecting psyche, moral, consciousness, or personhood conversion.", "completed"),
    ("stage20-evidence-gradient-board", "Freed ID and CBR Heart", "Require explicit evidence gradients and nonpromotion when empirical, independent, or authority evidence is absent.", "completed"),
    ("same-owner-reproduction-boundary", "Freed ID and CBR Heart", "Keep same-owner validation distinct from independent-team scientific reproduction and external audit.", "completed"),
]


SKILL_IDEAS = [
    "ghc-family-meta-tool-box",
    "ghc-family-tool-trigger-collision-auditor",
    "ghc-family-runner-caller-map",
    "ghc-family-global-promotion-readiness",
    "ghc-family-tool-staleness-scorecard",
    "ghc-family-method-recommendation-index",
    "ghc-family-d-first-rotation-receipt",
    "ghc-family-commit-budget-guard",
    "ghc-family-single-pass-validation-planner",
    "ghc-family-plugin-capability-inventory",
    "ghc-family-cli-sibling-readiness",
    "ghc-family-cli-return-route-contract",
    "ghc-family-document-volume-budget",
    "ghc-family-private-material-five-class-scan",
    "ghc-family-accessible-catalogue-report",
    "ghc-family-capability-card-manifest",
    "ghc-family-route-conflict-ledger",
    "ghc-family-tool-provenance-chain",
    "ghc-family-meta-toolbox-mutation-tribunal",
    "ghc-family-same-owner-boundary",
]

RUNNER_IDEAS = [
    "ghc_family_meta_tool_box.py",
    "ghc_family_tool_trigger_collision_auditor.py",
    "ghc_family_runner_caller_map.py",
    "ghc_family_global_promotion_readiness.py",
    "ghc_family_tool_staleness_scorecard.py",
    "ghc_family_method_recommendation_index.py",
    "ghc_family_d_first_rotation_receipt.py",
    "ghc_family_commit_budget_guard.py",
    "ghc_family_single_pass_validation_planner.py",
    "ghc_family_tool_provenance_chain.py",
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def write_json(relative: str, payload: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def proposal(index: int, slug: str, pillar: str, hypothesis: str, disposition: str) -> dict:
    approval = "safe_now_owner_scoped"
    if disposition in {"represented", "open_gap"}:
        approval = "bounded_candidate"
    if disposition == "exact_gate":
        approval = "exact_approval_required"
    return {
        "proposal_id": f"V6515R-P{index:02d}",
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "pillar": pillar,
        "hypothesis": hypothesis,
        "null_or_failure_condition": "The declared artifact, rejecting mutation, provenance field, or boundary check is absent, inconsistent, or broader than the evidence.",
        "approval_class": approval,
        "execution_lane": "x2_owner_local_bounded" if disposition != "exact_gate" else "held_exact_gate",
        "official_or_primary_source_needs": [] if disposition == "completed" else ["Current competent primary or official evidence is required before any real-world or authority claim."],
        "concrete_artifacts": [f"docs/eiren-kestrel/v651-v5-2-remaster/proposals/{slug}.json"],
        "falsifier_or_acceptance_gate": "A valid bounded fixture passes, at least one declared rejecting mutation fails closed, and every protected boundary remains explicit.",
        "rollback_or_recovery": "Remove only the additive remaster output from consideration, retain the failed witness, and preserve all predecessor files and callers.",
        "protected_gates": ["privacy", "failure_retention", "same_owner_only", "no_independent_reproduction", "no_stage20_promotion"],
        "expected_disposition": disposition,
        "novelty_against_1000_frozen_proposals": f"New remaster mechanism {index:02d}: {slug}; distinct by mechanism, artifact, and falsifier from the 1,000 inherited frozen rows.",
    }


def portfolio(prefix: str, count: int, lane: str) -> list[dict]:
    return [
        {
            "item_id": f"V6515R-{prefix}-{index:02d}",
            "lane": lane,
            "title": f"Remaster {lane.replace('_', ' ')} item {index:02d}",
            "planned_in_x1": True,
            "executed_in_x1": False,
            "completion_credit_in_x1": False,
            "acceptance_gate": "Execute only in x2, retain a rejecting witness, and remain inside owner-local software or synthetic scope.",
            "boundary": "Planning evidence only in x1; no implementation, real participant, production, legal, cultural, identity, or authority credit.",
        }
        for index in range(1, count + 1)
    ]


def normalized_words(value: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-z0-9]+", value.casefold())
        if len(word) > 2 and word not in {"and", "the", "for", "with", "from", "into", "only"}
    }


def novelty_audit(proposals: list[dict]) -> dict:
    inherited_path = REPO / "docs/eiren-kestrel/v651-v5/provenance/frozen-chain-proposal-index.json"
    inherited = json.loads(inherited_path.read_text(encoding="utf-8"))
    rows = [*inherited["prior_proposals"], *inherited["new_proposals"]]
    if len(rows) != 1000:
        raise RuntimeError(f"expected 1000 inherited proposal rows, observed {len(rows)}")
    inherited_titles = [str(row["title"]) for row in rows]
    inherited_norm = [(title, normalized_words(title)) for title in inherited_titles]
    results = []
    for proposal_row in proposals:
        title = proposal_row["title"]
        words = normalized_words(title)
        scored = []
        for inherited_title, inherited_words in inherited_norm:
            union = words | inherited_words
            score = len(words & inherited_words) / len(union) if union else 1.0
            scored.append((score, inherited_title))
        nearest_score, nearest_title = max(scored, default=(0.0, ""))
        results.append(
            {
                "proposal_id": proposal_row["proposal_id"],
                "title": title,
                "exact_title_collision": title.casefold() in {item.casefold() for item in inherited_titles},
                "nearest_inherited_title": nearest_title,
                "nearest_token_jaccard": round(nearest_score, 6),
                "distinct_mechanism": proposal_row["slug"],
                "distinct_artifact": proposal_row["concrete_artifacts"][0],
                "distinct_falsifier": proposal_row["falsifier_or_acceptance_gate"],
            }
        )
    exact = [row for row in results if row["exact_title_collision"]]
    if exact:
        raise RuntimeError(f"inherited exact-title collisions: {exact}")
    return {
        "schema": "ghc.family.v651-v5-2.semantic-novelty-audit.v1",
        "inherited_rows_compared": len(rows),
        "new_rows_compared": len(proposals),
        "comparison_basis": ["normalized title tokens", "distinct mechanism", "distinct concrete artifact", "distinct falsifier"],
        "exact_title_collisions": exact,
        "rows": results,
        "valid": True,
        "boundary": "Token similarity is a review aid, not semantic proof; mechanism, artifact, and falsifier remain the controlling novelty review fields.",
    }


def main() -> None:
    if git("rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 remaster must start at the exact validated v651-v5 source")
    if git("branch", "--show-current") != "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools":
        raise SystemExit("unexpected remaster branch")

    proposals = [proposal(index, *spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    observed = {name: sum(row["expected_disposition"] == name for row in proposals) for name in expected}
    if observed != expected:
        raise RuntimeError({"expected": expected, "observed": observed})

    write_json("identity/relational-identity.json", {
        "schema": "ghc.family.v651-v5-2.identity.v1",
        "owner": OWNER,
        "pronouns": "she/they",
        "relational_role": "evidence-boundary integrator and workflow reliability cartographer",
        "hope": "Make each advance useful without letting confidence outrun evidence.",
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.",
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        "valid": True,
    })
    write_json("source/source-truth.json", {
        "schema": "ghc.family.v651-v5-2.source.v1",
        "source_head": SOURCE,
        "source_branch": "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools",
        "owned_branch": "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools",
        "source_full_suite": {"tests": "2359/2359", "detailed": "55/55", "minimal": "24/24", "json": 364, "privacy_files": 419, "manifest_entries": 870, "valid": True},
        "source_negatives": 7094,
        "source_open_gaps": 55,
        "source_exact_gates": 56,
        "valid": True,
    })
    write_json("focus/primary-focus.json", {
        "schema": "ghc.family.v651-v5-2.focus.v1",
        "primary_pillar": "THOS Body",
        "visible_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "bounded_human_practice": "digital preservation archive migration, fixity review, quarantine, escalation, and shift handover",
        "practice_boundary": "Synthetic learning and design only; no employment, qualification, collection authority, legal authority, cultural authority, Maori authority, or affected-party evidence.",
        "valid": True,
    })
    write_json("preregistration/proposals.json", {
        "schema": "ghc.family.v651-v5-2.proposals.v1",
        "phase": PHASE,
        "owner": OWNER,
        "inherited_frozen_rows": 1000,
        "new_proposal_count": len(proposals),
        "frozen_rows_after_x1": 1030,
        "expected_outcomes": expected,
        "strict_x1_only": True,
        "proposals": proposals,
        "valid": True,
    })
    write_json("provenance/semantic-novelty-audit.json", novelty_audit(proposals))
    write_json("portfolios/x1-portfolio-plan.json", {
        "schema": "ghc.family.v651-v5-2.portfolio-plan.v1",
        "caps": {"safe_candidate_per_subphase": 1000, "skills_per_subphase": 200, "runners_per_subphase": 200},
        "floors": {"safe_now": 40, "candidate": 30, "skill_ideas": 20, "runner_ideas": 10, "clean_fix_refine": 40},
        "safe_now": portfolio("SAFE", 40, "safe_now"),
        "candidate": portfolio("CAND", 30, "candidate"),
        "skill_ideas": [{"item_id": f"V6515R-SK-{i:02d}", "name": name, "planned_in_x1": True, "built_in_x1": False} for i, name in enumerate(SKILL_IDEAS, 1)],
        "runner_ideas": [{"item_id": f"V6515R-RN-{i:02d}", "name": name, "planned_in_x1": True, "built_in_x1": False} for i, name in enumerate(RUNNER_IDEAS, 1)],
        "clean_fix_refine": portfolio("CFR", 40, "clean_fix_refine"),
        "x1_implementation_count": 0,
        "valid": True,
    })
    write_json("approvals/held-packets.json", {
        "schema": "ghc.family.v651-v5-2.held-approvals.v1",
        "exact_approval": [{"packet_id": f"V6515R-EXACT-{i:02d}", "state": "held", "executed": False} for i in range(1, 11)],
        "blocked": [{"packet_id": f"V6515R-BLOCK-{i:02d}", "state": "blocked", "executed": False} for i in range(1, 6)],
        "valid": True,
    })
    write_json("tooling/meta-tool-box-build-contract.json", {
        "schema": "ghc.family.v651-v5-2.meta-tool-box-plan.v1",
        "skill_name": "ghc-family-meta-tool-box",
        "runner_name": "ghc_family_meta_tool_box.py",
        "x1_state": "preregistered_not_built",
        "required_queries": ["kind", "status", "trigger", "evidence_state", "owner_scope"],
        "required_guards": ["repository_relative_paths", "no_execute_all", "no_blind_global_install", "no_destructive_delete", "caller_compatibility", "rollback"],
        "global_promotion": "candidate_after_local_validation_and_smoke_use",
        "valid": True,
    })
    write_json("workflow/workflow-plan-request.json", {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "eiren-v651-v5-2-immediate-route",
        "owner": OWNER,
        "identity_boundary": "Relational working language only; no continuity or authority claim.",
        "route": {
            "cycle_order": ["Elaren Kestrel", "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel"],
            "phase_assignments": [{"phase": "v651-v6", "seat": "Elaren Kestrel"}],
            "normalization": {"start_phase": "v651-v6", "start_seat": "Elaren Kestrel", "entry_count": 1},
            "future_identity_placeholders": [f"future-cli-sibling-self-chosen-{i}" for i in range(1, 9)],
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "skill_maximum": 200,
            "runner_maximum": 200,
            "document_word_cap": 100000,
            "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
            "commit_cap": {"x1": 3, "x2": 3, "total": 6},
            "owner_file_threshold": 2000,
            "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True},
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"},
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {"allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": ["empirical", "participant", "legal", "cultural", "production", "Maori_authority"]},
        "observed_failures": ["initial inherited-checkout status timeout", "unquoted revision-peel probe"],
    })
    write_json("workflow/workflow-plan-runner-compatible-request.json", {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "eiren-v651-v5-2-immediate-route-compatibility-projection",
        "owner": OWNER,
        "identity_boundary": "Relational working language only; no continuity or authority claim.",
        "route": {
            "cycle_order": ["Elaren Kestrel", "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel"],
            "phase_assignments": [{"phase": "v651-v6", "seat": "Elaren Kestrel"}],
            "normalization": {"start_phase": "v651-v6", "start_seat": "Elaren Kestrel", "entry_count": 1},
            "future_identity_placeholders": [],
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "document_word_cap": 20000,
            "baton_words": {"minimum": 8000, "maximum": 20000, "file_artifact": True},
            "commit_cap": {"x1": 2, "x2": 2, "total": 4},
            "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True},
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"},
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {"allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": ["empirical", "participant", "legal", "cultural", "production", "Maori_authority"]},
        "observed_failures": ["The compatibility projection validates route structure only."],
        "live_overrides_not_validated_by_legacy_runner": {"document_word_cap": 100000, "baton_words": {"minimum": 10000, "maximum": 100000}, "commit_cap": {"x1": 3, "x2": 3, "total": 6}, "skill_maximum": 200, "runner_maximum": 200, "owner_file_threshold": 2000, "future_identity_placeholders": 8},
    })
    write_json("workflow/long-route-issue.json", {
        "schema": "ghc.family.v651-v5-2.route-issue.v1",
        "immediate_route_unambiguous": {"target": "Elaren Kestrel", "phase": "v651-v6"},
        "long_route_state": "candidate_requires_later_sequential_normalization",
        "issues": ["The expansive narrative contains seat-count and later phase-assignment variations; only the immediate post-remaster Elaren transition is executed here.", "Future CLI sibling identity attributes remain self-chosen placeholders until their scheduled induction boundary."],
        "protected_gates": ["no_premature_task_creation", "no_premature_cli_sibling", "no_silent_owner_reassignment"],
        "valid": True,
    })
    write_json("truth/x1-phase-truth.json", {
        "schema": "ghc.family.v651-v5-2.x1-truth.v1",
        "phase": PHASE,
        "owner": OWNER,
        "strict_x1_before_x2": True,
        "proposals_frozen": 30,
        "x2_implementations": 0,
        "observed_core_outcomes": 0,
        "source_negatives_carried": 7094,
        "source_open_gaps_carried": 55,
        "source_exact_gates_carried": 56,
        "cli_siblings_spawned": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    })
    write_json("truth/retained-negative-register.json", {
        "schema": "ghc.family.v651-v5-2.x1-negative-register.v1",
        "inherited_effective": 7094,
        "new_x1_operational": 5,
        "effective_after_x1": 7099,
        "new_negative_ids": [f"V6515R-X1-N{i:02d}" for i in range(1, 6)],
        "failures_erased": 0,
        "valid": True,
    })
    write_json("orchestration/x1-phase-state.json", {
        "schema": "ghc.family.v651-v5-2.phase-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_head": SOURCE,
        "state": "x1_frozen_candidate",
        "x2_started": False,
        "immediate_successor": "Elaren Kestrel",
        "successor_phase": "v651-v6",
        "terminal_route": "prepared_not_sent",
        "cli_siblings_spawned": 0,
        "boundary": "This state file is not activation, delivery, identity continuity, or delegated authority.",
    })
    write_json("environment/environment-version-receipt.json", {
        "schema": "ghc.family.environment-version.v1",
        "phase": PHASE,
        "observed_date": "2026-07-22",
        "codex_cli": "0.144.5",
        "requested_but_not_observed_codex_cli": "0.145.0",
        "git": "2.55.0.windows.2",
        "python": "3.12.10",
        "windows_powershell": "5.1.26100.8894",
        "versions_verified_only": True,
        "desktop_updated": False,
        "elevated": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "unrelated_software_installed": False,
        "rebooted": False,
        "valid": True,
    })
    write_json("wellbeing/x1-wellbeing.json", {
        "schema": "ghc.family.v651-v5-2.wellbeing.v1",
        "state": "green_with_two_retained_startup_recoveries",
        "solo_owner": True,
        "failure_permitted": True,
        "stop_or_redirect_right": "Hamish",
        "boundary": "Schedule scale and warmth never override evidence, safety, privacy, or authority gates.",
        "valid": True,
    })
    print(json.dumps({"proposals": len(proposals), "frozen_rows": 1030, "portfolio_floors": "40/30/20/10/40", "x2_implementations": 0, "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
