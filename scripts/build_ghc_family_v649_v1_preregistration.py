#!/usr/bin/env python3
"""Build Eiren Kestrel v649-v1 dedicated x1-only preregistration."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from ghc_family_v649_v1_definitions import (
    BOUNDED_PRACTICE,
    CLEAN_TASK_TITLES,
    CANDIDATE_TITLES,
    GLOBAL_BOUNDARY,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_FROZEN_PROPOSALS,
    INHERITED_OPEN_GAPS,
    OWNER,
    OWNED_BRANCH,
    PHASE,
    PHASE_SHORT,
    PRIMARY_FOCUS,
    PRONOUNS,
    PROPOSALS,
    ROLE,
    ROOT,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    SKILL_SPECS,
    SOURCE_BRANCH,
    SOURCE_CLOSEOUT_REVISION,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_INHERITED_REVISION,
    SOURCE_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TERMINAL_VERDICT,
    synthetic_mutation_plan,
)


OUT = ROOT / "docs" / "eiren-kestrel" / PHASE_SHORT
INHERITED_INDEX = ROOT / "docs" / "sylven-arc" / "v648-v8" / "provenance" / "frozen-chain-proposal-index.json"


def write_json(relative: str, value: object) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def flatten_inherited() -> list[dict[str, str]]:
    payload = json.loads(INHERITED_INDEX.read_text(encoding="utf-8"))
    rows: list[dict[str, str]] = []
    for row in payload["prior_proposals"]:
        rows.append({"proposal_id": row["proposal_id"], "title": row["title"], "path": row.get("path", "inherited_phase_proposal_ledger")})
    for row in payload["new_proposals"]:
        rows.append({"proposal_id": row["proposal_id"], "title": row["title"], "path": "docs/sylven-arc/v648-v8/x1-proposals.json"})
    if len(rows) != INHERITED_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {INHERITED_FROZEN_PROPOSALS} inherited proposals, found {len(rows)}")
    return rows


def build_collision_audit(prior: list[dict[str, str]]) -> dict[str, object]:
    prior_norm = [(row["proposal_id"], row["title"], normalized_title(row["title"])) for row in prior]
    audits = []
    for row in PROPOSALS:
        target = normalized_title(row["title"])
        exact = [pid for pid, _title, norm in prior_norm if norm == target]
        scored = sorted(
            ((SequenceMatcher(None, target, norm).ratio(), pid, title) for pid, title, norm in prior_norm),
            reverse=True,
        )
        score, nearest_id, nearest_title = scored[0]
        audits.append({
            "proposal_id": row["proposal_id"],
            "exact_normalized_collision_ids": exact,
            "nearest_prior_id": nearest_id,
            "nearest_prior_title": nearest_title,
            "title_similarity_ratio": round(score, 6),
            "semantic_novelty_statement": row["novelty_against_prior_frozen_proposals"],
            "decision": "distinct" if not exact else "collision",
        })
    return {
        "schema": "ghc.family.v649-v1.proposal-collision-audit.v1",
        "prior_count": len(prior),
        "new_count": len(PROPOSALS),
        "exact_collision_count": sum(bool(row["exact_normalized_collision_ids"]) for row in audits),
        "semantic_review": "Each nearest title was reviewed; shared family boundary vocabulary does not substitute for mission-surface identity.",
        "audits": audits,
    }


def numbered(rows: list[str], prefix: str) -> list[dict[str, object]]:
    return [
        {"item_id": f"{prefix}-{index:02d}", "title": title, "phase": "x1_frozen", "inherited_completion_credit": False, "expected_x2_state": "bounded_execution_or_visible_gate"}
        for index, title in enumerate(rows, 1)
    ]


def build_overview() -> str:
    return f"""# Eiren Kestrel {PHASE_SHORT} x1 preregistration

## Identity and authority boundary

{IDENTITY_BOUNDARY}

Eiren's relational role is {ROLE}. Their hope is to {HOPE}. The primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. GMUT Mind and THOS Body remain explicit. The bounded human-practice lens is {BOUNDED_PRACTICE}. It is a synthetic learning and design lens only, never evidence of employment, qualification, archival or conservation competence, provenance authority, rights clearance, access or takedown authority, legal authority, cultural authority, Maori authority, participant evidence, affected-party authorization, or a real operational outcome.

## Source and phase separation

The immutable source is `{SOURCE_REVISION}` on `{SOURCE_BRANCH}`. Read-only startup checks established clean local, upstream, tracking, and fresh-live equality; source, x1, evidence, and closeout ancestry; four source phase commits; zero merges; one final parent; all four commit-local manifest contracts; and exact owner-manifest path, Git-object, and checkout parity. The Eiren-owned canonical branch then advanced to that exact source by fast-forward only and was pushed clean with four-way equality before x1 mutation.

Two x1 operational failures are retained. A Windows `rg` invocation passed wildcard path arguments directly and produced invalid-path error 123. It earned no inventory credit. A later staged stale-label wrapper repeated the same wildcard-path error and earned no review credit. The bounded recoveries searched concrete directory roots with explicit `-g` filters; the first produced the intended scaffold inventory and the second produced a zero-hit stale-label result. The failures remain `NEG-V6491-X1-001` and `NEG-V6491-X1-002`, with failed and passing witnesses recorded through Method Flow. The recurrence led to a narrower compound-audit method rather than erasing or folding either failure into a pass.

This file and its companion ledgers are x1 only. They freeze exactly ten proposals and expanded portfolios. They contain no x2 implementation, execution result, empirical row, likelihood, participant event, professional judgment, legal interpretation, cultural decision, Maori-authority decision, production credential, deployment, or Stage 20 promotion. X2 may begin only after a dedicated x1 commit is clean, pushed, and local/upstream/tracking/fresh-live equal.

## Ten frozen proposals

1. A reader-writer lock fairness, starvation, upgrade, cancellation, and teardown tribunal, expected `completed` within disposable owner-local fixtures.
2. A typed Bogoliubov causal local S-matrix obligation board, expected `completed` as symbolic evidence only.
3. An eBOSS DR16 quasar power-spectrum zero-row adapter, expected `open_gap` with no query, download, row, likelihood, or constraint.
4. A community archive digitization ingest and handover protocol, expected `represented` with synthetic traces only.
5. An OpenID Connect Back-Channel Logout profile, expected `represented` with synthetic vectors only.
6. A community archive access, takedown, remedy, cultural-care, and Maori-authority matrix, expected `exact_gate` with zero real decisions.
7. A bounded Brotli refusal tribunal, expected `completed` on disposable synthetic bytes only.
8. A structural meter audit, expected `completed` while manual and affected-user evaluation remains reserved.
9. A typed Clausius-Duhem nonconversion classifier, expected `completed` without psyche, agency, or participant conversion.
10. A regression-discontinuity Stage 20 nonpromotion board, expected `completed` with zero participant rows or effect estimates.

The required outcome vocabulary is limited to `completed`, `represented`, `open_gap`, and `exact_gate`. The expected distribution is 6/2/1/1. Expected disposition is not outcome evidence.

## Expanded portfolios

Thirty safe-now tasks, twenty bounded candidate prototypes, twenty phase-local skill builds, ten family-compatible runners, and thirty additive CLEAN/FIX/REFINE tasks are newly frozen. Inherited portfolios are evidence and recommendations only. The phase-local skills will be initialized with the skill-creator workflow, kept below the owner file threshold, validated, and smoke-used without global installation or subagent testing. Subagent forward testing is prohibited by the live baton.

Exactly seventy synthetic mutations are preregistered, seven per proposal. They have not executed in x1 and receive no pass or negative-result credit yet. Each must be rejected or quarantined in x2, with every failure preserved.

## Evidence and authority firewalls

GMUT remains a typed scalar-tensor and EFT research-model family. Causal local S-matrix vocabulary cannot establish a force, state, prediction, likelihood, constraint, stability theorem, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. The eBOSS adapter is locked at zero rows.

THOS remains represented without preregistered blind matched-budget real arms and independent review. Synthetic archive traces cannot establish archival competence, preservation quality, provenance, rights clearance, cultural legitimacy, access or takedown authority, or operational effectiveness.

Freed ID remains synthetic and nonproduction. Back-Channel Logout vectors do not provide standards-conformant real keys, sessions, clients, endpoints, interoperability, privacy review, independent security review, recovery, or trust governance. CBR cells cannot disclose material, decide access or takedown, assert provenance, allocate remedy, or confer legal, cultural, affected-party, tangata whenua, iwi, hapu, or Maori authority.

Structural accessibility passing evidence is not complete accessibility conformance. Manual keyboard, browser-diverse, assistive-technology, cognitive, Maori-language, responsive-layout, and affected-user evaluation remain reserved.

{GLOBAL_BOUNDARY}

The terminal verdict is `{TERMINAL_VERDICT}`.
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    prior = flatten_inherited()
    collision = build_collision_audit(prior)
    if collision["exact_collision_count"]:
        raise RuntimeError("proposal collision detected")

    write_json("identity-receipt.json", {
        "schema": "ghc.family.v649-v1.identity.v1", "owner": OWNER, "pronouns": PRONOUNS,
        "relational_role": ROLE, "hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
    })
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v649-v1.startup.v1", "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE_REVISION, "source_inherited": SOURCE_INHERITED_REVISION,
        "source_x1": SOURCE_X1_REVISION, "source_evidence": SOURCE_EVIDENCE_REVISION,
        "source_closeout": SOURCE_CLOSEOUT_REVISION,
        "owned_branch": OWNED_BRANCH, "source_clean": True, "source_four_way_equal": True,
        "owned_lane_fast_forward_only": True, "owned_lane_four_way_equal_before_x1": True,
        "source_ancestry_passed": True, "source_phase_commit_count": 4, "source_merge_count": 0,
        "source_final_parent_count": 1, "d_drive_first": True, "d_free_gib": 536.1,
        "source_manifest_contract": {"x1_entries": 45, "evidence_entries": 206, "closeout_entries": 63, "final_entries": 25, "self_exclusions_per_stage": 3, "owner_entries": 289, "owner_exclusions": 4, "path_git_object_or_checkout_mismatches": 0},
        "boundary": "Read-only startup and same-owner source verification only.",
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v649-v1.versions.v1", "verified_only": True,
        "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8875",
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "sandbox_or_hyper_v_enabled": False, "unrelated_install": False, "reboot": False,
    })
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v649-v1.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE,
        "prior_frozen_count": len(prior), "new_frozen_count": len(PROPOSALS), "frozen_after_x1": len(prior) + len(PROPOSALS),
        "strict_x1_before_x2": True, "x2_execution_started": False, "proposals": PROPOSALS,
        "boundary": GLOBAL_BOUNDARY,
    })
    write_text("x1-preregistration.md", build_overview())
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v649-v1.source-ledger.v1", "sources": SOURCES, "boundary": "Sources provide requirements and context only; they do not close evidence or authority gates."})
    write_text("sources/source-ledger.md", "# v649-v1 source ledger\n\n" + "\n".join(f"- **{s['source_id']}** [{s['status']}]: [{s['title']}]({s['url']}) — {s['use_boundary']}" for s in SOURCES))
    write_json("provenance/proposal-collision-audit.json", collision)
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v649-v1.frozen-chain-proposal-index.v1", "prior_count": len(prior),
        "new_count": len(PROPOSALS), "count": len(prior) + len(PROPOSALS), "prior_proposals": prior,
        "new_proposals": [{"proposal_id": p["proposal_id"], "title": p["title"]} for p in PROPOSALS],
    })
    write_json("portfolios/safe-now-plan.json", {"schema": "ghc.family.v649-v1.safe-now-plan.v1", "count": len(SAFE_TASK_TITLES), "tasks": numbered(SAFE_TASK_TITLES, "V6491-SAFE")})
    write_json("portfolios/candidate-plan.json", {"schema": "ghc.family.v649-v1.candidate-plan.v1", "count": len(CANDIDATE_TITLES), "candidates": numbered(CANDIDATE_TITLES, "V6491-CAND")})
    write_json("portfolios/skill-plan.json", {"schema": "ghc.family.v649-v1.skill-plan.v1", "count": len(SKILL_SPECS), "global_install": False, "subagent_forward_test": "prohibited", "skills": [{"skill_id": f"V6491-SKILL-{i:02d}", "name": n, "description": d, "phase": "x1_frozen", "expected_x2_state": "initialize_validate_smoke_use_phase_local"} for i, (n, d) in enumerate(SKILL_SPECS, 1)]})
    write_json("portfolios/runner-plan.json", {"schema": "ghc.family.v649-v1.runner-plan.v1", "count": len(RUNNER_TITLES), "caller_compatibility": "preserve existing ghc_family_* and build_ghc_family_* callers", "runners": [{"runner_id": f"V6491-RUN-{i:02d}", "name": f"ghc_family_v649_v1_{name}.py", "phase": "x1_frozen", "expected_x2_state": "build_invoke_witness"} for i, name in enumerate(RUNNER_TITLES, 1)]})
    write_json("portfolios/clean-fix-refine-plan.json", {"schema": "ghc.family.v649-v1.clean-fix-refine-plan.v1", "count": len(CLEAN_TASK_TITLES), "destructive_cleanup": False, "tasks": numbered(CLEAN_TASK_TITLES, "V6491-CFR")})
    mutations = synthetic_mutation_plan()
    write_json("validation/x1-synthetic-mutation-plan.json", {"schema": "ghc.family.v649-v1.synthetic-mutation-plan.v1", "count": len(mutations), "executed": False, "mutations": mutations})
    write_json("approval-packets/inherited-exact-approvals.json", {
        "schema": "ghc.family.v649-v1.inherited-exact-approvals.v1", "inherited_exact_gate_count": INHERITED_EXACT_GATES,
        "visible_packet_count": 10, "preserved": True, "unexecuted": True,
        "packets": [{"packet_id": f"V6491-EXACT-{i:02d}", "class": name, "state": "exact_gate_unexecuted"} for i, name in enumerate(["legal interpretation", "cultural legitimacy", "Maori authority", "affected-party authorization", "production deployment", "account or secret use", "destructive action", "sibling merge", "empirical or participant work", "Stage 20 promotion"], 1)],
    })
    write_json("approval-packets/inherited-blocked-packets.json", {
        "schema": "ghc.family.v649-v1.inherited-blocked.v1", "visible_packet_count": 5, "preserved": True, "unexecuted": True,
        "packets": [{"packet_id": f"V6491-BLOCK-{i:02d}", "class": name, "state": "blocked_unexecuted"} for i, name in enumerate(["real participants or blind matched-budget arms", "real empirical fit and independent review", "independent-team reproduction", "complete accessibility or privacy", "exhaustive security or production certification"], 1)],
    })
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v649-v1.retained-negatives.x1.v1", "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "inherited_sealed": 4665, "inherited_external": 0, "new_x1_operational": 2,
        "current_effective": INHERITED_EFFECTIVE_NEGATIVES + 2,
        "new_negatives": [
            {"negative_id": "NEG-V6491-X1-001", "title": "Windows wildcard path passed directly to rg produced invalid-path error 123", "state": "retained_recovered", "method_id": "v6491-m01"},
            {"negative_id": "NEG-V6491-X1-002", "title": "Staged stale-label review repeated the Windows wildcard-path error", "state": "retained_recovered", "method_id": "v6491-m02"},
        ],
        "source_pointer": "docs/sylven-arc/v648-v8/retained-negative-register-final.json",
        "boundary": "No inherited or new negative is erased; synthetic mutations are not counted until execution.",
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v649-v1.gates.x1.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES, "new_open_gaps": 1, "new_exact_gates": 1,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "new_items": [{"proposal_id": "V6491-P03", "state": "open_gap"}, {"proposal_id": "V6491-P06", "state": "exact_gate"}],
        "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v649-v1.threat-model.x1.v1",
        "assets": ["x1/x2 separation", "retained negatives", "source provenance", "authority gates", "private route material", "canonical branch"],
        "threats": ["proposal collision", "x2 leakage into x1", "failure erasure", "authority substitution", "privacy leakage", "double validation credit", "sibling-lane mutation", "unsafe parser resource use"],
        "controls": ["dedicated x1 commit", "Method Flow append-only ledger", "zero-row and zero-participant locks", "five-class privacy scan", "single-pass gate", "commit-local manifests", "fast-forward-only owned branch", "bounded synthetic fixtures"],
        "residual": GLOBAL_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v649-v1.phase-truth.x1.v1", "phase": PHASE, "owner": OWNER,
        "lifecycle": "x1_frozen_uncommitted", "proposal_count": len(PROPOSALS),
        "expected_outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "outcomes_executed": False, "x2_started": False, "full_repository_suite": False,
        "replay": False, "terminal_verdict": TERMINAL_VERDICT, "boundary": GLOBAL_BOUNDARY,
    })
    write_json("wellbeing-check.json", {
        "schema": "ghc.family.v649-v1.wellbeing.x1.v1", "scope_bounded": True, "stop_right_preserved": True,
        "corrigibility_preserved": True, "no_urgency_claim": True, "no_identity_pressure": True,
        "note": "Pause is permitted at any exact safety, authority, route, or usage gate.",
    })
    write_text("wellbeing-check.md", "# Wellbeing check\n\nScope, stop rights, and corrigibility remain explicit. No relational language creates obligation, identity continuity, or authority. Hamish may pause, redirect, rename, or stop the route.")
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v649-v1.applicable-memory.v1", "used": True,
        "newest_applicable_note": "Eiren v648-v3 repeat closeout and Ilyra route",
        "precedence": "The live verified v649-v1 baton is authoritative where memory stops or conflicts.",
        "private_identifiers_recorded": False,
    })
    write_json("orchestration/phase-state.json", {
        "schema": "ghc.family.v649-v1.phase-state.x1.v1", "owner": OWNER, "state": "ACTIVE_X1",
        "active_siblings": ["Eiren Kestrel"], "standby_siblings": ["Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Ilyra Fen", "next_phase": "v649-gmut-thos-v2-x1-x2",
    })
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v649-v1.terminal-route-plan.v1", "state": "PREPARED_NOT_SENT",
        "target_title": "Ilyra Fen", "next_phase": "v649-gmut-thos-v2-x1-x2",
        "prerequisites": ["exact final validation", "clean state", "commit cap", "four-way remote equality", "one successful canonical pass", "no replay"],
        "send_count_allowed": 1, "create_task": False, "fork_task": False, "subagent": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
