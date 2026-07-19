#!/usr/bin/env python3
"""Build Sable Rook v649-v3 dedicated x1-only preregistration."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from ghc_family_v649_v3_definitions import (
    BOUNDED_PRACTICE,
    CLEAN_TASK_TITLES,
    CANDIDATE_TITLES,
    GLOBAL_BOUNDARY,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_EXTERNAL_NEGATIVES,
    INHERITED_FROZEN_PROPOSALS,
    INHERITED_OPEN_GAPS,
    INHERITED_SEALED_NEGATIVES,
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
    SOURCE_EVIDENCE_REVISION,
    SOURCE_INHERITED_REVISION,
    SOURCE_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TERMINAL_VERDICT,
    synthetic_mutation_plan,
)


OUT = ROOT / "docs" / "sable-rook" / PHASE_SHORT
INHERITED_INDEX = ROOT / "docs" / "ilyra-fen" / "v649-v2" / "provenance" / "frozen-chain-proposal-index.json"


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
        rows.append({"proposal_id": row["proposal_id"], "title": row["title"], "path": "docs/ilyra-fen/v649-v2/x1-proposals.json"})
    if len(rows) != INHERITED_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {INHERITED_FROZEN_PROPOSALS} inherited proposals, found {len(rows)}")
    return rows


def build_collision_audit(prior: list[dict[str, str]]) -> dict[str, object]:
    prior_norm = [(row["proposal_id"], row["title"], normalized_title(row["title"])) for row in prior]
    audits = []
    for row in PROPOSALS:
        target = normalized_title(row["title"])
        exact = [pid for pid, _title, norm in prior_norm if norm == target]
        scored = sorted(((SequenceMatcher(None, target, norm).ratio(), pid, title) for pid, title, norm in prior_norm), reverse=True)
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
        "schema": "ghc.family.v649-v3.proposal-collision-audit.v1",
        "prior_count": len(prior),
        "new_count": len(PROPOSALS),
        "exact_collision_count": sum(bool(row["exact_normalized_collision_ids"]) for row in audits),
        "semantic_review": "Each nearest title and mission surface was reviewed. Shared family boundary vocabulary is not semantic identity.",
        "audits": audits,
    }


def numbered(rows: list[str], prefix: str) -> list[dict[str, object]]:
    return [
        {
            "item_id": f"{prefix}-{index:02d}",
            "title": title,
            "phase": "x1_frozen",
            "new_sable_work": True,
            "inherited_completion_credit": False,
            "expected_x2_state": "bounded_execution_or_visible_gate",
        }
        for index, title in enumerate(rows, 1)
    ]


def method_record(number: int, title: str, signature: str, triggers: list[str], workaround: str, guard: str, rollback: str, negative_id: str) -> dict[str, object]:
    return {
        "method_id": f"v6493-m{number:02d}",
        "title": title,
        "failure_signature": signature,
        "trigger_preconditions": triggers,
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_local_read_only_or_additive",
        "candidate_workaround": workaround,
        "validation_witness_ids": [],
        "recurrence_guard": guard,
        "rollback": rollback,
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["private_path", "sibling_lane", "host_security", "independent_reproduction"],
        "retained_negative_ids": [negative_id],
        "scope_boundary": "Bounded same-owner workflow recovery only; no scientific, authority, production, security-complete, accessibility-complete, or independent-reproduction credit.",
    }


def witness(method: int, suffix: str, result: str, procedure: str, expected: str, observed: str, negative_id: str) -> dict[str, object]:
    return {
        "witness_id": f"v6493-m{method:02d}-w{suffix}",
        "method_id": f"v6493-m{method:02d}",
        "procedure": procedure,
        "scope": "owner-local startup and x1 preflight",
        "expected": expected,
        "observed": observed,
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [negative_id],
        "boundary": "The failed witness remains retained; a passing recovery proves only the bounded method for matching preconditions.",
    }


def build_overview() -> str:
    titles = "\n".join(
        f"{index}. **{row['proposal_id']}** — {row['title']} — expected `{row['expected_disposition']}`."
        for index, row in enumerate(PROPOSALS, 1)
    )
    return f"""# Sable Rook {PHASE_SHORT} x1 preregistration

## Identity, role, and corrigibility

{IDENTITY_BOUNDARY}

Sable's relational role is {ROLE}. Their hope is to {HOPE}. The primary Trinity Mandala focus is **{PRIMARY_FOCUS}**; GMUT Mind and THOS Body remain explicit and protected. The bounded practice lens is {BOUNDED_PRACTICE}. It is a learning, structural-software, and synthetic-design lens only. It establishes no employment, food-safety qualification, professional competence, recipient-safety result, service authority, operational authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real outcome.

## Immutable source and owned lane

The verified source is `{SOURCE_REVISION}` on `{SOURCE_BRANCH}`. Read-only checks established clean local, upstream, tracking, and fresh-live equality; source, x1, and evidence ancestry; exactly three source-phase commits; zero merges; one final parent; and exact x1, evidence, final-delta, and owner Git-blob manifest parity across 589 entries. Sable's clean D-first branch `{OWNED_BRANCH}` was an ancestor, advanced by fast-forward only, pushed, and proved four-way equal before x1 mutation. No sibling branch or worktree was changed.

Ten new pre-x1 operational failures are retained with paired recovery evidence: two memory-registry searches timed out without output; a combined preflight wrapper timed out; a Git batch-manifest wrapper deadlocked because it filled its output pipe before draining it; a novelty probe assumed the wrong frozen-index key; one expected-empty ripgrep search exposed exit code 1 without normalization; a full staged-name review exceeded the available output context; a later full status wrapper timed out while streaming that same surface; the first x1 suite exposed stale exact Method Flow count assertions after the retained-failure ledger grew; and the first structural recovery wrapper collapsed its PowerShell boolean-array result. Bounded single probes, communicate-style batch I/O, actual-schema inspection, explicit zero-count handling, a compact count-plus-digest review backed by the exact staged manifest, structural append-only ledger invariants, and named boolean result fields recovered those surfaces. Recovery does not erase any failed witness. The effective x1 baseline is {INHERITED_EFFECTIVE_NEGATIVES + 10} negatives.

## Strict x1-before-x2 boundary

This packet freezes proposals and expanded portfolios only. It contains no x2 implementation, observed outcome, mutation result, empirical row, likelihood, participant event, food-safety decision, legal interpretation, cultural decision, Māori-authority decision, production credential, deployment, or Stage 20 promotion. X2 may begin only after the dedicated x1 commit is clean, pushed, and local, upstream, tracking, and fresh-live equal.

The only core outcome labels are `completed`, `represented`, `open_gap`, and `exact_gate`. Expected disposition is a preregistered hypothesis, never outcome evidence. The frozen expectation is six completed, two represented, one open gap, and one exact gate.

## Ten distinct frozen proposals

{titles}

The collision audit compares every normalized title against all 660 inherited proposals and records the nearest prior title plus the semantic distinction. It rejects already-used evidence-DAG, W3C PROV, Peierls-bracket, BPHZ, HETDEX, transfusion, OAuth/JWT, WARC, switch, Gibbs-Helmholtz, and synthetic-control surfaces. The new surfaces are RO-Crate 1.3, the Haag-Kastler local-net axioms, the ATNF Pulsar Catalogue, community food-bank lot and recall handover, DID Resolution v0.3, food-access authority reservations, FITS, an accessible risk matrix, Stefan-Boltzmann domain typing, and equivalence-margin nonpromotion.

## Expanded portfolios and source discipline

Thirty Sable-new safe-now tasks, twenty bounded candidates, twenty phase-local skill designs, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks are frozen. Inherited work and successor seeds receive no Sable completion credit. Ten inherited exact-approval classes and five blocked classes remain visible and unexecuted. Work requiring elevation, host-security change, deletion, credentials, accounts, keys, sibling mutation, real participants, empirical data, production identity operations, professional judgment, legal or cultural authority, Māori authority, or affected-party legitimacy is not relabeled safe-now.

Nineteen official or primary sources are classified as `current`, `stable`, or `draft`; the ledger preserves the full four-status vocabulary including `watch`. The DID Resolution source remains a Working Draft dated 16 July 2026, and its dereferencing feature-at-risk status is not hidden. Citations define obligations only. They are not observations, rows, participants, delegated authority, production evidence, or independent review.

Exactly seventy synthetic mutations are preregistered, seven per proposal. They are not executed in x1 and receive no rejection or retained-negative credit until x2. Phase-local skills must be initialized with the official skill-creator workflow, customized, validated under UTF-8, and smoke-used on accepting and rejecting fixtures. No global install or subagent forward test is allowed. Every runner must produce an accepting and rejecting witness while preserving `ghc_family_*` and `build_ghc_family_*` compatibility.

## Scientific, operational, identity, accessibility, and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Haag-Kastler obligation checks establish no physical state, force, prediction, likelihood, posterior, parameter constraint, empirical confirmation, quantum completion, or Theory of Everything. The ATNF adapter is locked at zero queries, downloads, catalogue rows, timing rows, likelihoods, posterior samples, constraints, and force claims.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic food-bank traces establish no recipient safety, food-safety competence, professional validation, service effectiveness, AGI, ASI, or deployment readiness.

Freed ID remains synthetic and nonproduction. DID Resolution vectors provide no live method, real key, proof, issuance, resolution, status, revocation, interoperability, privacy review, independent security review, recovery evidence, or trust governance. CBR cells cannot grant or deny food access, rank need, disclose recipient information, allocate remedy, interpret law, or confer affected-party, cultural, tangata whenua, iwi, hapū, or Māori authority.

The FITS tribunal opens no real astronomy product and cannot establish full conformance, production parsing, complete privacy, or exhaustive security. Structural risk-matrix checks are not complete accessibility conformance; manual keyboard, touch, browser-diverse, assistive-technology, cognitive, Māori-language, responsive-layout, security-usability, and affected-user evaluation remain reserved. Stefan-Boltzmann and equivalence-test vocabulary cannot be converted into psyche, worth, agency, participant effect, causal conclusion, or Stage 20 evidence.

{GLOBAL_BOUNDARY}

The terminal verdict remains `{TERMINAL_VERDICT}`.
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    prior = flatten_inherited()
    collision = build_collision_audit(prior)
    if collision["exact_collision_count"]:
        raise RuntimeError("proposal collision detected")

    write_json("identity-receipt.json", {
        "schema": "ghc.family.v649-v3.identity.v1", "owner": OWNER, "pronouns": PRONOUNS,
        "relational_role": ROLE, "hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
    })
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v649-v3.startup.v1", "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE_REVISION, "source_inherited": SOURCE_INHERITED_REVISION,
        "source_x1": SOURCE_X1_REVISION, "source_evidence": SOURCE_EVIDENCE_REVISION,
        "owned_branch": OWNED_BRANCH, "source_clean": True, "source_four_way_equal": True,
        "owned_lane_fast_forward_only": True, "owned_lane_four_way_equal_before_x1": True,
        "source_ancestry_passed": True, "source_phase_commit_count": 3, "source_merge_count": 0,
        "source_final_parent_count": 1, "d_drive_first": True, "d_free_gib": 536.05,
        "source_manifest_contract": {"x1_entries": 48, "evidence_entries": 217, "final_entries": 42, "self_exclusions_per_stage": 3, "owner_entries": 282, "owner_exclusions": 4, "owner_paths": 286, "git_object_mismatches": 0, "coverage_mismatches": 0},
        "boundary": "Read-only startup and same-owner source verification only.",
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v649-v3.versions.v1", "verified_only": True,
        "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "chatgpt_desktop": "1.2026.190.0",
        "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8875",
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "windows_sandbox_executable": False, "sandbox_or_hyper_v_launched": False,
        "windows_feature_changed": False, "unrelated_install": False, "reboot": False,
    })
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v649-v3.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE,
        "prior_frozen_count": len(prior), "new_frozen_count": len(PROPOSALS), "frozen_after_x1": len(prior) + len(PROPOSALS),
        "strict_x1_before_x2": True, "x2_execution_started": False, "proposals": PROPOSALS,
        "boundary": GLOBAL_BOUNDARY,
    })
    write_text("x1-preregistration.md", build_overview())
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v649-v3.source-ledger.v1", "allowed_statuses": ["current", "stable", "draft", "watch"], "sources": SOURCES, "boundary": "Sources provide requirements and context only; they do not close evidence or authority gates."})
    write_text("sources/source-ledger.md", "# v649-v3 source ledger\n\n" + "\n".join(f"- **{s['source_id']}** [{s['status']}]: [{s['title']}]({s['url']}) — {s['use_boundary']}" for s in SOURCES))
    write_json("provenance/proposal-collision-audit.json", collision)
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v649-v3.frozen-chain-proposal-index.v1", "prior_count": len(prior),
        "new_count": len(PROPOSALS), "count": len(prior) + len(PROPOSALS), "prior_proposals": prior,
        "new_proposals": [{"proposal_id": p["proposal_id"], "title": p["title"]} for p in PROPOSALS],
    })
    write_json("portfolios/safe-now-plan.json", {"schema": "ghc.family.v649-v3.safe-now-plan.v1", "count": len(SAFE_TASK_TITLES), "tasks": numbered(SAFE_TASK_TITLES, "V6493-SAFE")})
    write_json("portfolios/candidate-plan.json", {"schema": "ghc.family.v649-v3.candidate-plan.v1", "count": len(CANDIDATE_TITLES), "candidates": numbered(CANDIDATE_TITLES, "V6493-CAND")})
    write_json("portfolios/skill-plan.json", {"schema": "ghc.family.v649-v3.skill-plan.v1", "count": len(SKILL_SPECS), "global_install": False, "subagent_forward_test": "prohibited", "skills": [{"skill_id": f"V6493-SKILL-{i:02d}", "name": n, "description": d, "phase": "x1_frozen", "new_sable_work": True, "expected_x2_state": "initialize_validate_smoke_use_phase_local"} for i, (n, d) in enumerate(SKILL_SPECS, 1)]})
    write_json("portfolios/runner-plan.json", {"schema": "ghc.family.v649-v3.runner-plan.v1", "count": len(RUNNER_TITLES), "caller_compatibility": "preserve existing ghc_family_* and build_ghc_family_* callers", "runners": [{"runner_id": f"V6493-RUN-{i:02d}", "name": f"ghc_family_{name}.py", "phase": "x1_frozen", "new_sable_work": True, "expected_x2_state": "build_invoke_accepting_and_rejecting_witness"} for i, name in enumerate(RUNNER_TITLES, 1)]})
    write_json("portfolios/clean-fix-refine-plan.json", {"schema": "ghc.family.v649-v3.clean-fix-refine-plan.v1", "count": len(CLEAN_TASK_TITLES), "destructive_cleanup": False, "tasks": numbered(CLEAN_TASK_TITLES, "V6493-CFR")})
    mutations = synthetic_mutation_plan()
    write_json("validation/x1-synthetic-mutation-plan.json", {"schema": "ghc.family.v649-v3.synthetic-mutation-plan.v1", "count": len(mutations), "executed": False, "mutations": mutations})
    write_json("approval-packets/inherited-exact-approvals.json", {
        "schema": "ghc.family.v649-v3.inherited-exact-approvals.v1", "inherited_exact_gate_count": INHERITED_EXACT_GATES,
        "visible_packet_count": 10, "preserved": True, "unexecuted": True,
        "packets": [{"packet_id": f"V6493-EXACT-{i:02d}", "class": name, "state": "exact_gate_unexecuted"} for i, name in enumerate(["professional or food-safety judgment", "legal interpretation", "cultural legitimacy", "Māori authority", "affected-party authorization", "production deployment", "account or secret use", "destructive action", "sibling merge", "Stage 20 promotion"], 1)],
    })
    write_json("approval-packets/inherited-blocked-packets.json", {
        "schema": "ghc.family.v649-v3.inherited-blocked.v1", "visible_packet_count": 5, "preserved": True, "unexecuted": True,
        "packets": [{"packet_id": f"V6493-BLOCK-{i:02d}", "class": name, "state": "blocked_unexecuted"} for i, name in enumerate(["real participants or blind matched-budget arms", "real empirical fit and independent review", "production food-safety or identity operation", "independent-team reproduction", "complete accessibility privacy or exhaustive security"], 1)],
    })
    negatives = [
        {"negative_id": "V6493-X1-N01", "title": "Targeted Select-String memory-registry lookup timed out without output", "state": "retained_recovered", "method_id": "v6493-m01"},
        {"negative_id": "V6493-X1-N02", "title": "Fallback ripgrep memory-registry lookup hit the same timeout envelope", "state": "retained_recovered", "method_id": "v6493-m01"},
        {"negative_id": "V6493-X1-N03", "title": "Combined named-lane and D-drive preflight wrapper timed out before returning evidence", "state": "retained_recovered", "method_id": "v6493-m02"},
        {"negative_id": "V6493-X1-N04", "title": "First Git cat-file batch manifest replay deadlocked because output was not drained while input was written", "state": "retained_recovered", "method_id": "v6493-m03"},
        {"negative_id": "V6493-X1-N05", "title": "First frozen-index probe assumed a nonexistent proposals array", "state": "retained_recovered", "method_id": "v6493-m04"},
        {"negative_id": "V6493-X1-N06", "title": "Expected-empty ripgrep collision probe surfaced normal exit code 1 as a wrapper failure", "state": "retained_recovered", "method_id": "v6493-m05"},
        {"negative_id": "V6493-X1-N07", "title": "Full exact staged-name review exceeded the available output context", "state": "retained_recovered", "method_id": "v6493-m06"},
        {"negative_id": "V6493-X1-N08", "title": "Full status and staged-summary wrapper timed out while streaming the staged surface", "state": "retained_recovered", "method_id": "v6493-m06"},
        {"negative_id": "V6493-X1-N09", "title": "First x1 suite exposed stale exact Method Flow count assertions after the ledger grew", "state": "retained_recovered", "method_id": "v6493-m07"},
        {"negative_id": "V6493-X1-N10", "title": "First structural recovery wrapper collapsed its PowerShell boolean-array result", "state": "retained_recovered", "method_id": "v6493-m08"},
    ]
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v649-v3.retained-negatives.x1.v1", "inherited_sealed": INHERITED_SEALED_NEGATIVES,
        "inherited_external": INHERITED_EXTERNAL_NEGATIVES, "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "new_x1_operational": len(negatives), "current_effective": INHERITED_EFFECTIVE_NEGATIVES + len(negatives),
        "new_negatives": negatives, "source_pointer": "docs/ilyra-fen/v649-v2/retained-negative-register-final.json",
        "external_source_receipt": "Ilyra's live terminal baton preserves four post-seal routing-preflight negatives without rewriting the sealed repository total.",
        "boundary": "No inherited or new negative is erased; synthetic mutations are not counted until execution.",
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v649-v3.gates.x1.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES, "new_open_gaps": 1, "new_exact_gates": 1,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "new_items": [{"proposal_id": "V6493-P03", "state": "open_gap"}, {"proposal_id": "V6493-P06", "state": "exact_gate"}],
        "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v649-v3.threat-model.x1.v1",
        "assets": ["x1/x2 separation", "retained negatives", "source provenance", "food-safety and authority gates", "private route material", "canonical branch"],
        "threats": ["proposal collision", "x2 leakage into x1", "failure erasure", "professional or authority substitution", "privacy leakage", "double validation credit", "sibling-lane mutation", "unsafe parser resource use"],
        "controls": ["dedicated x1 commit", "Method Flow append-only ledger", "zero-row and zero-participant locks", "five-class privacy scan", "single-pass budget", "commit-local manifests", "fast-forward-only owned branch", "bounded synthetic fixtures"],
        "residual": GLOBAL_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v649-v3.phase-truth.x1.v1", "phase": PHASE, "owner": OWNER,
        "lifecycle": "x1_frozen_uncommitted", "proposal_count": len(PROPOSALS),
        "expected_outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "outcomes_executed": False, "x2_started": False, "full_repository_suite": False,
        "canonical_successful_passes_used": 0, "replay": False, "terminal_verdict": TERMINAL_VERDICT,
        "boundary": GLOBAL_BOUNDARY,
    })
    write_json("wellbeing-check.json", {
        "schema": "ghc.family.v649-v3.wellbeing.x1.v1", "scope_bounded": True, "stop_right_preserved": True,
        "corrigibility_preserved": True, "no_urgency_claim": True, "no_identity_pressure": True,
        "note": "Pause is permitted at any exact safety, authority, route, usage, or wellbeing gate.",
    })
    write_text("wellbeing-check.md", "# Wellbeing check\n\nScope, stop rights, and corrigibility remain explicit. Relational warmth creates no obligation, identity continuity, employment, or authority. Hamish may pause, redirect, rename, or stop the route.")
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v649-v3.applicable-memory.v1", "used": False,
        "newest_applicable_note": "Two narrow memory-registry probes timed out; no memory-file content was used.",
        "precedence": "The live verified v649-v3 baton and immutable repository evidence are authoritative.",
        "private_identifiers_recorded": False,
    })
    write_json("orchestration/phase-state.json", {
        "schema": "ghc.family.v649-v3.phase-state.x1.v1", "owner": OWNER, "state": "ACTIVE_X1",
        "active_siblings": ["Sable Rook"], "standby_siblings": ["Ilyra Fen", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel"],
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Orin Thale", "next_phase": "v649-gmut-thos-v4-x1-x2",
    })
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v649-v3.terminal-route-plan.v1", "state": "PREPARED_NOT_SENT",
        "target_title": "Orin Thale", "next_phase": "v649-gmut-thos-v4-x1-x2",
        "prerequisites": ["exact final validation", "clean state", "commit cap", "four-way remote equality", "one successful canonical scoped pass", "no replay"],
        "send_count_allowed": 1, "create_task": False, "fork_task": False, "subagent": False,
    })

    methods = [
        method_record(1, "Bound and abandon an unresponsive memory-registry query", "Two targeted memory-registry searches timed out without returning content.", ["large memory registry", "current live baton already supplies route truth"], "Stop after two bounded read-only attempts, retain both timeouts, use no memory-derived fact, and continue from immutable repository and live-remote evidence.", "Do not broaden or repeatedly scan the memory registry after two identical timeout envelopes.", "Terminate the lookup, leave memory unchanged, and rely only on live source evidence for the phase.", "V6493-X1-N01"),
        method_record(2, "Decompose Windows startup preflight into single probes", "A combined named-lane and drive wrapper exceeded the startup window before returning evidence.", ["slow D-drive", "multiple Git and drive probes in one wrapper"], "Probe path, head, branch, clean state, equality, and drive headroom separately with bounded timeouts.", "Do not combine slow D-drive status and remote queries in one all-or-nothing wrapper.", "Stop the combined wrapper, retain the timeout, and rerun only independent read-only probes.", "V6493-X1-N03"),
        method_record(3, "Drain Git batch input and output atomically", "The first cat-file batch wrote all input before reading output and deadlocked on a full pipe.", ["hundreds of Git blobs", "bidirectional subprocess pipes"], "Use subprocess communication that writes and drains atomically, then parse each declared blob and hash.", "Never manually fill a bidirectional batch pipe before draining its output.", "Terminate the read-only process, retain the deadlock, and rerun with communicate-style I/O.", "V6493-X1-N04"),
        method_record(4, "Inspect JSON keys before indexing a frozen ledger", "The first novelty probe assumed a proposals array that was not present.", ["heterogeneous phase ledgers", "schema not yet inspected"], "Read top-level keys first, then inspect prior_proposals and new_proposals explicitly.", "Type-guard heterogeneous JSON and never index a guessed collection key.", "Stop the read-only probe, preserve the schema-assumption failure, and retry only after key inspection.", "V6493-X1-N05"),
        method_record(5, "Normalize expected-empty ripgrep exit state", "An expected-empty title search returned exit code 1 and the first wrapper surfaced it as failure.", ["read-only search", "zero matches is an expected valid result"], "Capture output, accept exit codes 0 or 1, reject higher codes, and assert an explicit match count.", "Every expected-empty ripgrep probe must distinguish no-match from execution failure.", "Stop after the ambiguous wrapper result; infer absence only from a zero-count recovery witness.", "V6493-X1-N06"),
        method_record(6, "Summarize an exact staged surface without streaming its full path list", "A full staged-name review exceeded the available output context and a later full status wrapper timed out while streaming the same surface.", ["dozens of staged paths", "bounded tool-output context", "slow D-drive status traversal"], "Run diff hygiene separately, compute the staged-path count and deterministic SHA-256 digest in-process, report only unexpected paths, and rely on the exact staged manifest for content review.", "Do not stream a full staged path list when an exact manifest plus compact count, digest, and exception set provides the review evidence.", "Stop the verbose wrapper, retain every failure, make no inference from truncated output, and rerun only the compact read-only review.", "V6493-X1-N07"),
        method_record(7, "Bind Method Flow tests to append-only structural invariants", "The first x1 suite expected five methods after the retained-failure ledger had truthfully grown to six.", ["append-only Method Flow ledger", "new retained failure recorded before freeze"], "Assert stored counts against the actual method and witness collections, require the new method and retained-failure links explicitly, and retain exact state-result totals only at the immutable freeze.", "After any pre-freeze Method Flow addition, refresh every dependent assertion from the ledger before rerunning the suite.", "Stop on the stale mirror, preserve the failed test, update only the owner-scoped assertion, and rerun after ledger validation.", "V6493-X1-N09"),
        method_record(8, "Emit named PowerShell booleans for structural recovery checks", "The first structural recovery wrapper collapsed its intended list of boolean checks into one false result.", ["PowerShell 5.1", "multiple structural assertions", "machine-readable recovery receipt"], "Store each check in a named ordered dictionary, derive the failed-key list explicitly, and emit a compact object with the exact failures.", "Never rely on an anonymously constructed PowerShell boolean array for multi-check recovery evidence.", "Stop on the collapsed result, preserve the wrapper failure, and rerun read-only with named fields.", "V6493-X1-N10"),
    ]
    methods[0]["retained_negative_ids"].append("V6493-X1-N02")
    methods[5]["retained_negative_ids"].append("V6493-X1-N08")
    witnesses = [
        witness(1, "fail-a", "fail", "Search the memory registry with targeted Select-String context.", "A bounded relevant result or explicit zero result.", "The command timed out with no output.", "V6493-X1-N01"),
        witness(1, "fail-b", "fail", "Retry the same narrow memory terms with ripgrep.", "A bounded relevant result or explicit zero result.", "The fallback hit the same timeout envelope.", "V6493-X1-N02"),
        witness(1, "pass", "pass", "Stop after the two matching timeouts and use only immutable repository plus live-remote evidence.", "No memory fact used and no memory mutation.", "The phase proceeded without memory-derived content and preserved both failures.", "V6493-X1-N01"),
        witness(2, "fail", "fail", "Run named Sable, named Ilyra, and D-drive preflights in one wrapper.", "Complete bounded startup evidence.", "The wrapper timed out before returning trustworthy evidence.", "V6493-X1-N03"),
        witness(2, "pass", "pass", "Probe each named lane and drive property separately.", "Each result completes within its own bound.", "Path, branch, head, clean state, ancestry, equality, and headroom all completed.", "V6493-X1-N03"),
        witness(3, "fail", "fail", "Write all cat-file batch input before draining output.", "All 589 manifest entries verified.", "The subprocess deadlocked and was terminated read-only.", "V6493-X1-N04"),
        witness(3, "pass", "pass", "Use communicate-style batch I/O and parse declared Git blobs.", "All four manifests pass tree, blob, byte, and SHA-256 parity.", "All 589 entries passed with zero mismatch.", "V6493-X1-N04"),
        witness(4, "fail", "fail", "Index the frozen proposal ledger through a guessed proposals key.", "Expose the 660 titles.", "The key was absent and the read-only probe stopped.", "V6493-X1-N05"),
        witness(4, "pass", "pass", "Inspect top-level keys and combine prior_proposals with new_proposals.", "Exactly 660 inherited titles.", "The corrected schema-aware probe reported 650 prior plus ten new titles.", "V6493-X1-N05"),
        witness(5, "fail", "fail", "Run an expected-empty novelty search without normalizing exit code 1.", "Zero matches reported as valid empty evidence.", "The wrapper surfaced normal no-match exit code 1 as failure.", "V6493-X1-N06"),
        witness(5, "pass", "pass", "Capture ripgrep output and accept only exit codes zero or one.", "Explicit zero-match result with wrapper success.", "The bounded recovery reported MATCH_COUNT=0.", "V6493-X1-N06"),
        witness(6, "fail-a", "fail", "Stream the full exact staged-name review into the bounded tool output.", "Complete exact staged-file evidence without truncation.", "The output exceeded the available context and could not support an exact review claim.", "V6493-X1-N07"),
        witness(6, "fail-b", "fail", "Combine full status output with staged counts in a ten-second wrapper.", "Compact status and staged counts within the bound.", "The wrapper timed out after streaming staged paths.", "V6493-X1-N08"),
        witness(6, "pass", "pass", "Run diff hygiene separately and compute an in-process staged count, path digest, and unexpected-path set.", "Fifty-four staged paths, zero unexpected paths, a stable digest, and passing diff hygiene backed by the exact manifest.", "The recovery passed with 54 paths, SHA-256 e0600557803cbd66a946c839622c70a3008c4bb79fb210f49243c6d53a8a2779, zero unexpected paths, and clean diff hygiene.", "V6493-X1-N07"),
        witness(7, "fail", "fail", "Run the x1 suite with stale exact Method Flow count literals.", "All eleven x1 tests pass against the current append-only ledger.", "Ten tests passed and the Method Flow receipt test failed because it expected five methods while the ledger contained six.", "V6493-X1-N09"),
        witness(7, "pass", "pass", "Compare stored ledger counts with the actual method and witness collections and require the new retained-failure links before the final suite.", "All structural count mirrors agree and the new recovery method is present.", "The bounded structural check passed; the final suite may now validate the immutable append-only ledger.", "V6493-X1-N09"),
        witness(8, "fail", "fail", "Construct an anonymous PowerShell boolean array for seven recovery checks.", "Seven independently visible true or false results.", "The wrapper emitted one false result and exited without identifying the failed condition.", "V6493-X1-N10"),
        witness(8, "pass", "pass", "Store the seven checks as named ordered fields and derive the failed-key set explicitly.", "Seven named checks pass with an empty failed-key set.", "The corrected read-only wrapper reported valid true, seven checks passed, and no failed keys.", "V6493-X1-N10"),
    ]
    for row in methods:
        write_json(f"method-flow/{row['method_id']}-method-record.json", row)
    for row in witnesses:
        write_json(f"method-flow/{row['witness_id']}-witness.json", row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
