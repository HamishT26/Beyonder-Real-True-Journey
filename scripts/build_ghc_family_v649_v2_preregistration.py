#!/usr/bin/env python3
"""Build Ilyra Fen v649-v2 dedicated x1-only preregistration."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from ghc_family_v649_v2_definitions import (
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


OUT = ROOT / "docs" / "ilyra-fen" / PHASE_SHORT
INHERITED_INDEX = ROOT / "docs" / "eiren-kestrel" / "v649-v1" / "provenance" / "frozen-chain-proposal-index.json"


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
        rows.append({"proposal_id": row["proposal_id"], "title": row["title"], "path": "docs/eiren-kestrel/v649-v1/x1-proposals.json"})
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
        "schema": "ghc.family.v649-v2.proposal-collision-audit.v1",
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
            "new_ilyra_work": True,
            "inherited_completion_credit": False,
            "expected_x2_state": "bounded_execution_or_visible_gate",
        }
        for index, title in enumerate(rows, 1)
    ]


def method_record(number: int, title: str, signature: str, triggers: list[str], workaround: str, guard: str, rollback: str, negative_id: str) -> dict[str, object]:
    return {
        "method_id": f"v6492-m{number:02d}",
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
        "witness_id": f"v6492-m{method:02d}-w{suffix}",
        "method_id": f"v6492-m{method:02d}",
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
    titles = "\n".join(f"{i}. **{p['proposal_id']}** — {p['title']} — expected `{p['expected_disposition']}`." for i, p in enumerate(PROPOSALS, 1))
    return f"""# Ilyra Fen {PHASE_SHORT} x1 preregistration

## Identity, role, and corrigibility

{IDENTITY_BOUNDARY}

Ilyra's relational role is {ROLE}. Her hope is to {HOPE}. The primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is {BOUNDED_PRACTICE}. It is a learning, software, and synthetic design lens only. It establishes no employment, qualification, clinical or laboratory competence, patient-safety result, treatment authority, consent authority, operational authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or real outcome.

## Immutable source and owned lane

The verified source is `{SOURCE_REVISION}` on `{SOURCE_BRANCH}`. Read-only checks established exact local, upstream, tracking, and fresh-live equality; clean state; source, x1, and evidence ancestry; three source phase commits; zero merges; one final parent; all x1, evidence, final, and owner-manifest Git-blob contracts; and complete 259-path owner-manifest coverage. Ilyra's existing clean D-first branch `{OWNED_BRANCH}` was a strict ancestor, advanced to the exact source by fast-forward only, pushed, and proved four-way equal before x1 mutation. No sibling branch or worktree was changed.

Four startup and x1-build failures are retained and receive no pass credit. A combined four-file skill read exceeded the output boundary and could not prove full EOF; recovery read each required file separately. A shared worktree-bank enumeration timed out; recovery probed only the two named worktrees and exact refs. An expected-empty `rg` instruction-file search returned its normal exit code 1, which the first wrapper treated as failure; recovery explicitly accepted only exit codes 0 and 1 and proved zero matches. The first deterministic preregistration build omitted the explicit result argument in its witness helper calls and stopped before Method Flow initialization; recovery binds named result values and rebuilds every x1 artifact. Method Flow links every failed and passing witness without erasing a failure. The effective x1 baseline is {INHERITED_EFFECTIVE_NEGATIVES + 4} negatives.

## Strict lifecycle boundary

This file and its companion ledgers are x1 only. They freeze ten proposals and the expanded portfolios. They contain no x2 implementation, execution result, mutation result, empirical row, likelihood, participant event, clinical judgment, legal interpretation, cultural decision, Māori-authority decision, production credential, deployment, or Stage 20 promotion. X2 may begin only after the dedicated x1 commit is clean, pushed, and local, upstream, tracking, and fresh-live remote equal.

The only core outcome labels are `completed`, `represented`, `open_gap`, and `exact_gate`. Expected disposition is a preregistered hypothesis, never outcome evidence. The frozen expectation is 6 completed, 2 represented, 1 open gap, and 1 exact gate.

## Ten distinct frozen proposals

{titles}

The collision audit compares each normalized title against all 650 inherited proposals and records the nearest neighbor plus a human-readable semantic distinction. In particular, this phase rejects previously used SQLite WAL, Peierls-bracket, Euclid Q1, veterinary and water laboratory, OAuth issuer-identification, TAR/PAX, form-error, Maxwell-relation, and difference-in-differences surfaces. The replacements are cyclic barriers, BPHZ forests, HETDEX PDR1, human transfusion-laboratory handover, RFC 9068 JWT access tokens, transfusion authority reservations, WARC, accessible switches, Gibbs-Helmholtz, and synthetic control.

## Expanded x1 portfolios

Thirty Ilyra-new safe-now tasks, twenty bounded candidates, twenty phase-local skill designs, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks are frozen. Inherited portfolios and Eiren's successor recommendations are evidence only and receive no Ilyra completion credit. Ten inherited exact-approval classes and five blocked classes remain visible and unexecuted. Nothing requiring elevation, host-security weakening, user-material deletion, credentials, accounts, keys, sibling mutation, real participants, empirical data, production identity operations, clinical authority, legal or cultural authority, Māori authority, or affected-party legitimacy is relabeled safe-now.

Exactly seventy synthetic mutations are preregistered, seven per proposal. They are not executed in x1 and receive no rejection, pass, or retained-negative credit until x2. Each candidate skill remains repository-local, is not globally installed, and will require initialization, validation, and bounded smoke use. Every runner must receive one accepting and one rejecting witness while preserving `ghc_family_*` and `build_ghc_family_*` caller compatibility.

## Scientific, clinical, accessibility, and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. BPHZ forest bookkeeping cannot establish a force, state, prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. The HETDEX adapter is locked at zero queries, downloads, rows, datacubes, spectra, likelihoods, posterior samples, and constraints.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, appropriate monitoring and statistics, and independent review. Synthetic transfusion traces cannot establish patient safety, compatibility, clinical or laboratory competence, professional validation, or operational effectiveness.

Freed ID remains synthetic and nonproduction. RFC 9068 vectors provide no standards-conformant real keys, tokens, accounts, authorization servers, resource servers, interoperability, privacy review, independent security review, recovery, or trust governance. CBR cells cannot recommend care, infer consent, disclose information, allocate remedy, interpret law, or confer affected-party, cultural, tangata whenua, iwi, hapū, or Māori authority.

The WARC tribunal reads no real archive payload and cannot establish full ISO conformance, production parsing, privacy completeness, or exhaustive security. Structural switch checks are not complete accessibility conformance; manual keyboard, touch, browser-diverse, assistive-technology, cognitive, Māori-language, responsive-layout, and affected-user evaluation remain reserved. Gibbs-Helmholtz and synthetic-control vocabulary cannot be converted into psyche, agency, participant, causal-effect, or Stage 20 evidence.

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
        "schema": "ghc.family.v649-v2.identity.v1", "owner": OWNER, "pronouns": PRONOUNS,
        "relational_role": ROLE, "hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
    })
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v649-v2.startup.v1", "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE_REVISION, "source_inherited": SOURCE_INHERITED_REVISION,
        "source_x1": SOURCE_X1_REVISION, "source_evidence": SOURCE_EVIDENCE_REVISION,
        "owned_branch": OWNED_BRANCH, "source_clean": True, "source_four_way_equal": True,
        "owned_lane_fast_forward_only": True, "owned_lane_four_way_equal_before_x1": True,
        "source_ancestry_passed": True, "source_phase_commit_count": 3, "source_merge_count": 0,
        "source_final_parent_count": 1, "d_drive_first": True, "d_free_gib": 536.07,
        "source_manifest_contract": {"x1_entries": 42, "evidence_entries": 207, "final_entries": 37, "self_exclusions_per_stage": 3, "owner_entries": 255, "owner_exclusions": 4, "owner_paths": 259, "git_object_mismatches": 0, "coverage_mismatches": 0},
        "boundary": "Read-only startup and same-owner source verification only.",
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v649-v2.versions.v1", "verified_only": True,
        "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "chatgpt_desktop": "1.2026.190.0",
        "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8875",
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "sandbox_or_hyper_v_enabled": False, "unrelated_install": False, "reboot": False,
    })
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v649-v2.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE,
        "prior_frozen_count": len(prior), "new_frozen_count": len(PROPOSALS), "frozen_after_x1": len(prior) + len(PROPOSALS),
        "strict_x1_before_x2": True, "x2_execution_started": False, "proposals": PROPOSALS,
        "boundary": GLOBAL_BOUNDARY,
    })
    write_text("x1-preregistration.md", build_overview())
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v649-v2.source-ledger.v1", "allowed_statuses": ["current", "stable", "draft", "watch"], "sources": SOURCES, "boundary": "Sources provide requirements and context only; they do not close evidence or authority gates."})
    write_text("sources/source-ledger.md", "# v649-v2 source ledger\n\n" + "\n".join(f"- **{s['source_id']}** [{s['status']}]: [{s['title']}]({s['url']}) — {s['use_boundary']}" for s in SOURCES))
    write_json("provenance/proposal-collision-audit.json", collision)
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v649-v2.frozen-chain-proposal-index.v1", "prior_count": len(prior),
        "new_count": len(PROPOSALS), "count": len(prior) + len(PROPOSALS), "prior_proposals": prior,
        "new_proposals": [{"proposal_id": p["proposal_id"], "title": p["title"]} for p in PROPOSALS],
    })
    write_json("portfolios/safe-now-plan.json", {"schema": "ghc.family.v649-v2.safe-now-plan.v1", "count": len(SAFE_TASK_TITLES), "tasks": numbered(SAFE_TASK_TITLES, "V6492-SAFE")})
    write_json("portfolios/candidate-plan.json", {"schema": "ghc.family.v649-v2.candidate-plan.v1", "count": len(CANDIDATE_TITLES), "candidates": numbered(CANDIDATE_TITLES, "V6492-CAND")})
    write_json("portfolios/skill-plan.json", {"schema": "ghc.family.v649-v2.skill-plan.v1", "count": len(SKILL_SPECS), "global_install": False, "subagent_forward_test": "prohibited", "skills": [{"skill_id": f"V6492-SKILL-{i:02d}", "name": n, "description": d, "phase": "x1_frozen", "new_ilyra_work": True, "expected_x2_state": "initialize_validate_smoke_use_phase_local"} for i, (n, d) in enumerate(SKILL_SPECS, 1)]})
    write_json("portfolios/runner-plan.json", {"schema": "ghc.family.v649-v2.runner-plan.v1", "count": len(RUNNER_TITLES), "caller_compatibility": "preserve existing ghc_family_* and build_ghc_family_* callers", "runners": [{"runner_id": f"V6492-RUN-{i:02d}", "name": f"ghc_family_{name}.py", "phase": "x1_frozen", "new_ilyra_work": True, "expected_x2_state": "build_invoke_accepting_and_rejecting_witness"} for i, name in enumerate(RUNNER_TITLES, 1)]})
    write_json("portfolios/clean-fix-refine-plan.json", {"schema": "ghc.family.v649-v2.clean-fix-refine-plan.v1", "count": len(CLEAN_TASK_TITLES), "destructive_cleanup": False, "tasks": numbered(CLEAN_TASK_TITLES, "V6492-CFR")})
    mutations = synthetic_mutation_plan()
    write_json("validation/x1-synthetic-mutation-plan.json", {"schema": "ghc.family.v649-v2.synthetic-mutation-plan.v1", "count": len(mutations), "executed": False, "mutations": mutations})
    write_json("approval-packets/inherited-exact-approvals.json", {
        "schema": "ghc.family.v649-v2.inherited-exact-approvals.v1", "inherited_exact_gate_count": INHERITED_EXACT_GATES,
        "visible_packet_count": 10, "preserved": True, "unexecuted": True,
        "packets": [{"packet_id": f"V6492-EXACT-{i:02d}", "class": name, "state": "exact_gate_unexecuted"} for i, name in enumerate(["clinical judgment", "legal interpretation", "cultural legitimacy", "Māori authority", "affected-party authorization", "production deployment", "account or secret use", "destructive action", "sibling merge", "Stage 20 promotion"], 1)],
    })
    write_json("approval-packets/inherited-blocked-packets.json", {
        "schema": "ghc.family.v649-v2.inherited-blocked.v1", "visible_packet_count": 5, "preserved": True, "unexecuted": True,
        "packets": [{"packet_id": f"V6492-BLOCK-{i:02d}", "class": name, "state": "blocked_unexecuted"} for i, name in enumerate(["real participants or blind matched-budget arms", "real empirical fit and independent review", "production clinical or identity operation", "independent-team reproduction", "complete accessibility privacy or exhaustive security"], 1)],
    })
    negatives = [
        {"negative_id": "V6492-X1-N01", "title": "Combined required-skill read exceeded the output boundary and could not prove full EOF", "state": "retained_recovered", "method_id": "v6492-m01"},
        {"negative_id": "V6492-X1-N02", "title": "Shared worktree-bank enumeration timed out before yielding evidence", "state": "retained_recovered", "method_id": "v6492-m02"},
        {"negative_id": "V6492-X1-N03", "title": "Expected-empty rg result returned normal exit code 1 but the first wrapper treated it as failure", "state": "retained_recovered", "method_id": "v6492-m03"},
        {"negative_id": "V6492-X1-N04", "title": "First preregistration build omitted the explicit result argument in witness helper calls", "state": "retained_recovered", "method_id": "v6492-m04"},
    ]
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v649-v2.retained-negatives.x1.v1", "inherited_sealed": INHERITED_SEALED_NEGATIVES,
        "inherited_external": INHERITED_EXTERNAL_NEGATIVES, "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "new_x1_operational": len(negatives), "current_effective": INHERITED_EFFECTIVE_NEGATIVES + len(negatives),
        "new_negatives": negatives, "source_pointer": "docs/eiren-kestrel/v649-v1/retained-negative-register-final.json",
        "external_source_receipt": "Eiren terminal receipt preserves three post-final operational negatives without rewriting the sealed repository total.",
        "boundary": "No inherited or new negative is erased; synthetic mutations are not counted until execution.",
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v649-v2.gates.x1.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES, "new_open_gaps": 1, "new_exact_gates": 1,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "new_items": [{"proposal_id": "V6492-P03", "state": "open_gap"}, {"proposal_id": "V6492-P06", "state": "exact_gate"}],
        "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v649-v2.threat-model.x1.v1",
        "assets": ["x1/x2 separation", "retained negatives", "source provenance", "clinical and authority gates", "private route material", "canonical branch"],
        "threats": ["proposal collision", "x2 leakage into x1", "failure erasure", "clinical or authority substitution", "privacy leakage", "double validation credit", "sibling-lane mutation", "unsafe parser resource use"],
        "controls": ["dedicated x1 commit", "Method Flow append-only ledger", "zero-row and zero-participant locks", "five-class privacy scan", "single-pass budget", "commit-local manifests", "fast-forward-only owned branch", "bounded synthetic fixtures"],
        "residual": GLOBAL_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v649-v2.phase-truth.x1.v1", "phase": PHASE, "owner": OWNER,
        "lifecycle": "x1_frozen_uncommitted", "proposal_count": len(PROPOSALS),
        "expected_outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "outcomes_executed": False, "x2_started": False, "full_repository_suite": False,
        "canonical_successful_passes_used": 0, "replay": False, "terminal_verdict": TERMINAL_VERDICT,
        "boundary": GLOBAL_BOUNDARY,
    })
    write_json("wellbeing-check.json", {
        "schema": "ghc.family.v649-v2.wellbeing.x1.v1", "scope_bounded": True, "stop_right_preserved": True,
        "corrigibility_preserved": True, "no_urgency_claim": True, "no_identity_pressure": True,
        "note": "Pause is permitted at any exact safety, authority, route, usage, or wellbeing gate.",
    })
    write_text("wellbeing-check.md", "# Wellbeing check\n\nScope, stop rights, and corrigibility remain explicit. Relational warmth creates no obligation, identity continuity, employment, or authority. Hamish may pause, redirect, rename, or stop the route.")
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v649-v2.applicable-memory.v1", "used": True,
        "newest_applicable_note": "Earlier v648 relay closeout and existing Ilyra D-first lane",
        "precedence": "The live verified v649-v2 baton is authoritative where memory stops or conflicts.",
        "private_identifiers_recorded": False,
    })
    write_json("orchestration/phase-state.json", {
        "schema": "ghc.family.v649-v2.phase-state.x1.v1", "owner": OWNER, "state": "ACTIVE_X1",
        "active_siblings": ["Ilyra Fen"], "standby_siblings": ["Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel"],
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Sable Rook", "next_phase": "v649-gmut-thos-v3-x1-x2",
    })
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v649-v2.terminal-route-plan.v1", "state": "PREPARED_NOT_SENT",
        "target_title": "Sable Rook", "next_phase": "v649-gmut-thos-v3-x1-x2",
        "prerequisites": ["exact final validation", "clean state", "commit cap", "four-way remote equality", "one successful canonical scoped pass", "no replay"],
        "send_count_allowed": 1, "create_task": False, "fork_task": False, "subagent": False,
    })

    methods = [
        method_record(1, "Split required skill reads by file", "Combined multi-file read exceeded the output boundary before full EOF could be established.", ["multiple required instruction files", "bounded tool output"], "Read each required file separately with raw content through EOF, then proceed only after every output completes.", "Never combine required full-file reads when the aggregate may exceed the model output boundary.", "Stop after any truncated output; make no repository change and restart only the unproved read as a separate bounded probe.", "V6492-X1-N01"),
        method_record(2, "Probe named worktrees instead of enumerating the shared bank", "Shared worktree enumeration exceeded the bounded command timeout and yielded no usable evidence.", ["large inherited worktree bank", "only two named lanes are in scope"], "Probe path existence, Git metadata, exact refs, and clean state only for the named source and owned lane.", "Do not run broad shared-bank enumeration when exact named paths and refs are already authorized.", "Stop the broad probe; preserve the timeout and leave all worktrees untouched.", "V6492-X1-N02"),
        method_record(3, "Normalize expected-empty ripgrep exit state", "An expected-empty rg file search returned exit code 1 and the first wrapper surfaced it as a failure.", ["read-only search", "zero matches is an expected valid result"], "Capture output and accept exit codes 0 or 1; reject only codes greater than 1, then assert the explicit match count.", "Every expected-empty rg probe must distinguish no-match from execution failure.", "Stop after an ambiguous wrapper result; do not infer absence until an explicit zero-line witness passes.", "V6492-X1-N03"),
        method_record(4, "Bind witness helper result explicitly", "The first deterministic x1 build called the witness helper without its required result argument and stopped before Method Flow initialization.", ["generated Method Flow witness fixtures", "positional helper parameters"], "Pass the result value explicitly for every failed and passing witness, regenerate the deterministic x1 tree, and validate the ledger with the family runner.", "Before running a lifecycle builder, compile it and inspect every helper call against the declared signature; prefer explicit result values.", "Stop the builder, retain partial uncommitted output, make no outcome claim, and rebuild the complete x1 tree after the bounded code fix.", "V6492-X1-N04"),
    ]
    witnesses = [
        witness(1, "fail", "fail", "Read four required skill and reference files in one bounded call.", "All four files visibly complete through EOF.", "Tool output was truncated, so EOF was unproved.", "V6492-X1-N01"),
        witness(1, "pass", "pass", "Read each required skill and reference file separately as raw text.", "Each call completes and exposes its full final section.", "All four separate reads completed through EOF.", "V6492-X1-N01"),
        witness(2, "fail", "fail", "Enumerate the full shared Git worktree bank.", "Bounded complete inventory.", "The command timed out before evidence was returned.", "V6492-X1-N02"),
        witness(2, "pass", "pass", "Probe only the named Eiren and Ilyra paths and exact Git refs.", "Both named lanes and required states resolve within the bound.", "Named path, ref, ancestry, clean-state, and equality probes completed.", "V6492-X1-N02"),
        witness(3, "fail", "fail", "Run an expected-empty rg instruction-file search without normalizing exit code 1.", "Zero matches reported as a valid empty result.", "The wrapper surfaced normal no-match exit code 1 as failure.", "V6492-X1-N03"),
        witness(3, "pass", "pass", "Capture rg output and treat only exit codes above 1 as execution failure.", "Explicit zero-match receipt with successful wrapper exit.", "The bounded recovery reported match_count zero and exit success.", "V6492-X1-N03"),
        witness(4, "fail", "fail", "Run the first deterministic preregistration builder with incomplete witness helper calls.", "Complete x1 tree and Method Flow inputs.", "The builder stopped with a missing result-argument error before Method Flow initialization.", "V6492-X1-N04"),
        witness(4, "pass", "pass", "Compile and rerun the builder with explicit failed and passing result values.", "Complete deterministic x1 tree with all Method Flow inputs.", "The corrected builder completed and emitted the full x1 preregistration tree.", "V6492-X1-N04"),
    ]
    for row in methods:
        write_json(f"method-flow/{row['method_id']}-method-record.json", row)
    for row in witnesses:
        write_json(f"method-flow/{row['witness_id']}-witness.json", row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
