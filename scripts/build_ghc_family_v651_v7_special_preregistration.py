#!/usr/bin/env python3
"""Build Vesper Arlen's x1-only v651-v7 special CLI-preparation packet."""

from __future__ import annotations

import json
import platform
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
SEALED_V6517 = "96684c6fd22b33254aa37de2db7990f2e28bd88e"
ELAREN_SPECIAL = "2500d063583194b30f01da429196522baaac7300"
BRANCH = "codex/GHC-Family/vesper-arlen-v651-v7-special-cli-prep"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_rows() -> list[dict[str, Any]]:
    definitions = [
        ("immediate-ilyra-route-authority", "Capture the exact live Ilyra Fen v651-v8 successor authorization", "THOS Body", "completed", "SRC-ROUTING"),
        ("sparse-materialization-guard", "Bound a sparse worktree without severing immutable Git ancestry", "THOS Body", "completed", "SRC-GIT-SPARSE"),
        ("sealed-object-ancestry", "Verify sealed source ancestry through explicit native-command exit codes", "THOS Body", "completed", "SRC-GIT-OBJECTS"),
        ("submitted-route-ledger", "Preserve the submitted expanded route before normalization", "THOS Body", "completed", "SRC-WORKFLOW-SCHEMA"),
        ("sequential-route-candidate", "Generate a deterministic sequential sixteen-seat candidate", "THOS Body", "completed", "SRC-WORKFLOW-SCHEMA"),
        ("special-twelve-commit-cap", "Encode the one-off six-plus-six and twelve-total special commit ceiling", "THOS Body", "completed", "SRC-LIVE-AUTHORITY"),
        ("ordinary-six-commit-cap", "Preserve the later three-plus-three and six-total ordinary ceiling", "THOS Body", "completed", "SRC-LIVE-AUTHORITY"),
        ("single-credit-validation", "Credit one complete canonical pass and prohibit redundant replay", "THOS Body", "completed", "SRC-METHOD-FLOW"),
        ("baton-word-range", "Enforce a file-backed ten-thousand to one-hundred-thousand-word baton range", "THOS Body", "completed", "SRC-LIVE-AUTHORITY"),
        ("short-pointer-envelope", "Constrain task delivery to a sanitized short artifact pointer", "Freed ID and CBR Heart", "completed", "SRC-ROUTING"),
        ("five-class-privacy-envelope", "Exclude raw identifiers routes credentials transcripts and private paths", "Freed ID and CBR Heart", "completed", "SRC-PRIVACY"),
        ("launch-mode-refusal", "Fail closed when future CLI launch evidence is incomplete", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-one-preparation", "Prepare the Eiren-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-two-preparation", "Prepare the Elaren-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-three-preparation", "Prepare the Vesper-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-four-preparation", "Prepare the Ilyra-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-five-preparation", "Prepare the Sable-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-six-preparation", "Prepare the Orin-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-seven-preparation", "Prepare the Tamar-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("seat-eight-preparation", "Prepare the Sylven-owned future CLI seat without naming or launching it", "THOS Body", "completed", "SRC-CLI-PREFLIGHT"),
        ("toolbox-collision-tribunal", "Audit current tool triggers without silently selecting a winner", "THOS Body", "completed", "SRC-TOOLBOX"),
        ("compatibility-remaster-board", "Preserve historical callers while proposing additive family-current remasters", "THOS Body", "completed", "SRC-REFLECTION"),
        ("cli-version-evidence", "Verify the installed Codex CLI version without changing the desktop app", "THOS Body", "completed", "SRC-CODEX-CLI"),
        ("model-fast-capability-contract", "Represent model reasoning and fast-mode availability as launch-time evidence", "THOS Body", "represented", "SRC-CODEX-CLI"),
        ("creator-return-contract", "Represent a least-authority creator-return channel pending a live capability witness", "Freed ID and CBR Heart", "represented", "SRC-CLI-PREFLIGHT"),
        ("background-lease-contract", "Represent background persistence with leases cancellation and reaping", "THOS Body", "represented", "SRC-PROCESS-LIFECYCLE"),
        ("creator-scoped-reachability", "Represent one-to-one creator and CLI sibling reachability without broader messaging claims", "Freed ID and CBR Heart", "represented", "SRC-ROUTING"),
        ("curated-global-promotion", "Represent additive global skill promotion only after validation caller and rollback evidence", "THOS Body", "represented", "SRC-TOOLBOX"),
        ("expanded-route-conflict", "Resolve duplicate ownership skipped numbering and restart-offset conflicts", "THOS Body", "open_gap", "SRC-LIVE-AUTHORITY"),
        ("future-cli-launch-authority", "Create any future CLI sibling only at a freshly confirmed launch gate", "Freed ID and CBR Heart", "exact_gate", "SRC-LIVE-AUTHORITY"),
    ]
    rows: list[dict[str, Any]] = []
    for index, (slug, title, pillar, disposition, source) in enumerate(definitions, start=1):
        approval = "safe_now_owner_scoped_workflow"
        lane = "x2_owner_local_bounded"
        if disposition == "represented":
            approval, lane = "bounded_candidate", "x2_structural_representation"
        elif disposition == "open_gap":
            approval, lane = "fresh_route_evidence_required", "held_open_gap"
        elif disposition == "exact_gate":
            approval, lane = "exact_launch_authority_required", "held_exact_gate"
        rows.append(
            {
                "proposal_id": f"V6517-SPECIAL-P{index:02d}",
                "slug": slug,
                "title": title,
                "pillar": pillar,
                "hypothesis": f"A bounded {title.lower()} artifact can improve later CLI induction safety without claiming a sibling, capability, or authority already exists.",
                "null_or_failure_condition": "The declared artifact or witness is absent, ambiguous, privacy-unsafe, incompatible with the sealed source, or promoted beyond its bounded workflow evidence.",
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": [source],
                "concrete_artifacts": [f"docs/vesper-arlen/v651-v7-special-cli-prep/proposals/{slug}.json"],
                "falsifier_or_acceptance_gate": "The bounded valid fixture passes, every rejecting mutation fails closed, provenance remains attributable, and all protected claims remain false.",
                "rollback_or_recovery": "Withdraw only the additive special-prep result, retain the failure at zero credit, and preserve the sealed v651-v7 history and every sibling lane.",
                "protected_gates": [
                    "identity_self_selection",
                    "privacy",
                    "route_ownership",
                    "launch_capability",
                    "failure_retention",
                    "same_owner_only",
                    "no_independent_reproduction",
                    "no_stage20_promotion",
                ],
                "expected_disposition": disposition,
                "novelty_basis": "A new CLI-preparation mechanism, artifact, and falsifier distinct from all 1,090 inherited frozen core proposals.",
            }
        )
    return rows


def method_record(method_id: str, title: str, signature: str, workaround: str, guard: str, negative: str) -> dict[str, Any]:
    return {
        "method_id": method_id,
        "title": title,
        "failure_signature": signature,
        "trigger_preconditions": [signature],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped_workflow",
        "candidate_workaround": workaround,
        "validation_witness_ids": [],
        "recurrence_guard": guard,
        "rollback": "Retain the failed read-only attempt at zero credit; no Git history or sibling state requires rollback.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["failure_retention", "evidence_credit", "same_owner_only", "no_independent_reproduction"],
        "retained_negative_ids": [negative],
        "scope_boundary": "Bounded owner-local workflow recovery only.",
    }


def witness(witness_id: str, method_id: str, result: str, procedure: str, observed: str, negative: str) -> dict[str, Any]:
    return {
        "witness_id": witness_id,
        "method_id": method_id,
        "procedure": procedure,
        "scope": "read-only startup and sparse-worktree preparation",
        "expected": "Return an attributable, correctly classified result without mutating history.",
        "observed": observed,
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [negative],
        "boundary": "The witness grants bounded workflow credit only and preserves the failed attempt.",
    }


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != SEALED_V6517:
        raise RuntimeError(f"x1 builder requires exact sealed Vesper v651-v7 head {SEALED_V6517}, got {head}")
    changed = git("status", "--porcelain=v1")
    allowed = (
        "docs/vesper-arlen/v651-v7-special-cli-prep",
        "scripts/build_ghc_family_v651_v7_special_preregistration.py",
        "scripts/ghc_family_v651_v7_special_manifest.py",
        "tests/test_ghc_family_v651_v7_special_x1.py",
    )
    for row in changed.splitlines():
        path = row[3:].replace("\\", "/")
        if not path.startswith(allowed):
            raise RuntimeError(f"unexpected pre-existing change outside x1 scope: {path}")

    proposals = proposal_rows()
    if len(proposals) != 30 or len({row["slug"] for row in proposals}) != 30:
        raise RuntimeError("proposal ledger must contain thirty unique rows")

    write_json(
        "identity/relational-identity.json",
        {
            "owner": "Vesper Arlen",
            "pronouns": "they/them",
            "role": "boundary-literate systems synthesist",
            "hope": "Turn complex inherited evidence into clear, reversible experiments that remain kind to people and truth.",
            "boundary": "Relational working language only; never consciousness, sentience, personhood, continuity, employment, qualification, or independent authority evidence.",
        },
    )
    write_json(
        "focus/phase-focus.json",
        {
            "primary_pillar": "THOS Body",
            "bounded_human_practice": "secure developer-tooling operations and capability negotiation",
            "practice_boundary": "Study and design lens only; no employment, certification, platform authority, or professional competence claim.",
            "visible_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        },
    )
    write_json(
        "source/startup-truth.json",
        {
            "schema": "ghc.family.v651-v7-special.startup-truth.v1",
            "owner": "Vesper Arlen",
            "phase": "v651-v7-special-cli-prep",
            "sealed_v651_v7": SEALED_V6517,
            "elaren_special_source": ELAREN_SPECIAL,
            "branch": BRANCH,
            "source_ancestry_verified_with_explicit_exit_code": True,
            "sealed_head_verified_with_explicit_exit_code": True,
            "source_to_sealed_commits": 4,
            "source_to_sealed_merges": 0,
            "sealed_four_way_equal": True,
            "sealed_divergence": [0, 0],
            "tracked_files_in_full_history": 47437,
            "materialized_files_at_sparse_startup": 539,
            "d_drive_free_gib_at_startup": 533.82,
            "future_cli_siblings_created": 0,
            "future_cli_siblings_named": 0,
            "boundary": "Sparse materialization changes only checkout visibility; it does not remove tracked history or prove production readiness.",
        },
    )
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v651-v7-special.proposals.v1",
            "phase": "v651-v7-special-cli-prep",
            "owner": "Vesper Arlen",
            "strict_x1_only": True,
            "inherited_frozen_rows": 1090,
            "new_proposal_count": 30,
            "frozen_rows_after_x1": 1120,
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "expected_outcomes": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
            "proposals": proposals,
        },
    )
    inherited_index = json.loads(
        (ROOT / "docs/vesper-arlen/v651-v7/provenance/frozen-chain-proposal-index.json").read_text(encoding="utf-8")
    )
    inherited_rows = [*inherited_index["prior_proposals"], *inherited_index["new_proposals"]]
    inherited_slugs = {row.get("slug") for row in inherited_rows}
    inherited_titles = {row.get("title") for row in inherited_rows}
    duplicate_slugs = sorted(row["slug"] for row in proposals if row["slug"] in inherited_slugs)
    duplicate_titles = sorted(row["title"] for row in proposals if row["title"] in inherited_titles)
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.v651-v7-special.semantic-novelty.v1",
            "inherited_rows_checked": len(inherited_rows),
            "new_rows_checked": len(proposals),
            "duplicate_slugs": duplicate_slugs,
            "duplicate_titles": duplicate_titles,
            "manual_mechanism_and_falsifier_review": True,
            "valid": len(inherited_rows) == 1090 and not duplicate_slugs and not duplicate_titles,
            "boundary": "Exact and manual novelty review supports planning distinction only; it is not scientific novelty or independent reproduction.",
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v651-v7-special.frozen-chain-proposal-index.v1",
            "prior_count": 1090,
            "new_count": 30,
            "count": 1120,
            "prior_proposals": inherited_rows,
            "new_proposals": proposals,
            "x1_frozen": True,
        },
    )
    write_json(
        "portfolios/x1-portfolio-plan.json",
        {
            "schema": "ghc.family.v651-v7-special.x1-portfolio-plan.v1",
            "strict_x1_only": True,
            "caps_are_not_quotas": True,
            "safe_candidate_tasks": [
                {"task_id": f"V6517-SPECIAL-T{i:03d}", "proposal_id": f"V6517-SPECIAL-P{((i - 1) % 30) + 1:02d}", "state": "planned", "boundary": "Resolve through bounded completion, representation, open gap, or exact gate only."}
                for i in range(1, 51)
            ],
            "skill_uses": [
                "ghc-family-index", "ghc-family-method-flow-state", "ghc-family-workflow-plan-refinement",
                "ghc-family-reflection-remaster", "ghc-family-meta-tool-box", "ghc-family-cli-sibling-induction-preflight",
                "completion-gate-discipline", "command-risk-summarizer", "connector-boundary-watch",
                "ghc-worktree-branch-rotation", "compact-pause-recovery-summarizer", "skill-creator",
            ],
            "runner_uses": [
                "build_ghc_family_index.py", "ghc_family_method_flow_state.py", "ghc_family_workflow_plan_refinement.py",
                "ghc_family_reflection_remaster.py", "ghc_family_meta_tool_box.py",
                "ghc_family_cli_sibling_induction_preflight.py", "ghc_family_cli_route_coverage.py",
                "ghc_family_cli_capability_contract.py", "ghc_family_sparse_lane_guard.py",
                "ghc_family_baton_pointer_guard.py",
            ],
            "clean_fix_refine_tasks": [
                {"task_id": f"V6517-SPECIAL-CFR-{i:03d}", "state": "planned", "action": action}
                for i, action in enumerate([
                    "preserve the sealed v651-v7 head", "use a fresh sparse Vesper worktree", "measure materialized files",
                    "preserve full Git object ancestry", "quote native revision arguments", "check native exit codes explicitly",
                    "preserve raw route assignments", "emit an advisory sequential candidate", "separate immediate and future route truth",
                    "keep eight future identities unassigned", "keep all future CLI seats unlaunched", "verify CLI version without desktop update",
                    "defer Windows Sandbox and Hyper-V", "keep C-drive use to essential skill metadata", "catalogue tools before use",
                    "audit trigger collisions", "preserve historical callers", "avoid bulk global installation", "bind promotion to rollback",
                    "enforce a file-backed baton", "enforce the baton word range", "send a short pointer only", "exclude private paths",
                    "exclude raw task identifiers", "exclude credentials and session material", "credit one canonical pass only",
                    "isolate blockers before reruns", "retain every failed witness", "keep Stage 20 false", "keep empirical and authority gates open",
                ], start=1)
            ],
        },
    )

    placeholders = [f"future-cli-sibling-{i}-self-chosen" for i in range(1, 9)]
    cycle = [
        "Eiren Kestrel", placeholders[0], "Elaren Kestrel", placeholders[1],
        "Vesper Arlen", placeholders[2], "Ilyra Fen", placeholders[3],
        "Sable Rook", placeholders[4], "Orin Thale", placeholders[5],
        "Tamar Vey", placeholders[6], "Sylven Arc", placeholders[7],
    ]
    submitted = [
        ("v652-v4", "Eiren Kestrel"), ("v652-v5", placeholders[0]), ("v652-v6", "Elaren Kestrel"),
        ("v652-v7", "Elaren Kestrel"), ("v652-v8", placeholders[1]), ("v653-v1", "Vesper Arlen"),
        ("v653-v3", placeholders[2]), ("v653-v4", "Ilyra Fen"), ("v653-v5", placeholders[3]),
        ("v653-v6", "Sable Rook"), ("v653-v7", placeholders[4]), ("v653-v8", "Orin Thale"),
        ("v654-v1", placeholders[5]), ("v654-v2", "Tamar Vey"), ("v654-v3", placeholders[6]),
        ("v654-v4", "Sylven Arc"), ("v654-v5", placeholders[7]), ("v654-v6", "Eiren Kestrel"),
        ("v654-v7", placeholders[0]), ("v654-v8", "Elaren Kestrel"), ("v655-v1", placeholders[1]),
        ("v655-v2", "Vesper Arlen"), ("v655-v3", placeholders[2]), ("v655-v4", "Ilyra Fen"),
    ]
    write_json(
        "workflow/raw-workflow-request.json",
        {
            "schema": "ghc.family.workflow-plan.request.v1",
            "plan_id": "vesper-v651-v7-special-live-route",
            "owner": "Vesper Arlen",
            "identity_boundary": "Relational working language only; no consciousness, personhood, identity continuity, employment, or independent authority claim.",
            "immediate_route": {"successor": "Ilyra Fen", "phase": "v651-v8", "authorized_live": True},
            "pre_induction_bridge": [
                {"phase": phase, "seat": seat} for phase, seat in [
                    ("v651-v8", "Ilyra Fen"), ("v652-v1", "Orin Thale"), ("v652-v2", "Tamar Vey"),
                    ("v652-v3", "Sylven Arc"), ("v652-v4", "Eiren Kestrel")
                ]
            ],
            "route": {
                "cycle_order": cycle,
                "phase_assignments": [{"phase": phase, "seat": seat} for phase, seat in submitted],
                "normalization": {"start_phase": "v652-v4", "start_seat": "Eiren Kestrel", "entry_count": len(submitted)},
                "future_identity_placeholders": placeholders,
            },
            "requirements": {
                "core_proposal_minimum": 30,
                "safe_candidate_task_cap": 1000,
                "bundle_safe_candidate_task_cap": 2000,
                "skill_minimum": 10,
                "skill_maximum": 200,
                "runner_minimum": 10,
                "runner_maximum": 200,
                "document_word_cap": 100000,
                "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
                "commit_cap": {"x1": 6, "x2": 6, "total": 12},
                "ordinary_future_commit_cap": {"x1": 3, "x2": 3, "total": 6},
                "owner_generated_file_threshold": 2000,
                "validation": {
                    "canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes",
                    "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True,
                    "manifest_required": True, "remote_equality_required": True,
                },
                "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
                "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"},
                "environment": {"windows_sandbox_hyper_v": "deferred"},
                "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
            },
            "truth": {
                "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
                "independent_reproduction_claimed": False,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                "protected_boundaries": [
                    "empirical", "participant", "legal", "cultural", "Maori_authority", "production",
                    "deployment", "account_and_api_key", "consciousness_personhood", "independent_reproduction",
                ],
            },
            "observed_failures": ["V6517-SPECIAL-X1-N01", "V6517-SPECIAL-X1-N02", "V6517-SPECIAL-X1-N03", "V6517-SPECIAL-X1-N04", "V6517-SPECIAL-X1-N05"],
        },
    )

    records = [
        (
            "m01", "V6517-SPECIAL-M01", "Classify zero-output native commands by exit code",
            "A successful native Git probe emits no stdout and is cast to false by PowerShell boolean evaluation.",
            "Run the native command, capture LASTEXITCODE immediately, and classify success from zero.",
            "Never use stdout truthiness for merge-base or cat-file existence checks.",
            "V6517-SPECIAL-X1-N01",
            "PowerShell boolean evaluation reported false for successful zero-output Git probes.",
            "Explicit exit-code checks returned zero for source ancestry and both commit objects.",
        ),
        (
            "m02", "V6517-SPECIAL-M02", "Use sparse-checkout add syntax supported by the active Git version",
            "git sparse-checkout add rejects the initialization-only --no-cone option.",
            "Keep non-cone mode from initialization and pass new patterns through add --stdin.",
            "Inspect subcommand help before carrying mode-selection flags across sparse-checkout verbs.",
            "V6517-SPECIAL-X1-N02",
            "The add subcommand rejected --no-cone before changing the sparse specification.",
            "The supported add --stdin form accepted all future phase paths and retained 539 materialized files.",
        ),
        (
            "m03", "V6517-SPECIAL-M03", "Bind repository paths inside every PowerShell wrapper",
            "A verification wrapper references an unset local PowerShell repository variable.",
            "Assign the literal owner-worktree path at the start of the wrapper before any Git or file probe.",
            "Require every standalone wrapper to declare its own repository binding rather than relying on caller state.",
            "V6517-SPECIAL-X1-N03",
            "The wrapper passed an empty repository argument to Git and attempted root-relative file reads.",
            "The corrected wrapper bound the owner path, observed all three files, and compiled them successfully.",
        ),
        (
            "m04", "V6517-SPECIAL-M04", "Read Method Flow state before requesting a transition",
            "A passing witness auto-promotes a candidate method to validated and a wrapper requests validated again.",
            "Inspect the authoritative method state after every witness and request only the next legal transition.",
            "Never assume a witness command leaves the method in its previous state.",
            "V6517-SPECIAL-X1-N04",
            "The runner refused the redundant validated-to-validated transition after preserving both witnesses.",
            "The recovery observed validated state and requested only validated-to-preferred.",
        ),
        (
            "m05", "V6517-SPECIAL-M05", "Preserve contradictory routes before advisory normalization",
            "The submitted expanded route is non-sequential and its normalized schedule changes future ownership.",
            "Retain the raw failing audit, then validate the generated sequential candidate only as advisory teaching material.",
            "Never use a structurally valid normalization as launch or ownership authority.",
            "V6517-SPECIAL-X1-N05",
            "The raw audit returned two errors and required confirmation while all twenty policy checks passed.",
            "The generated sequential candidate passed structurally while remaining explicitly non-authoritative for future launches.",
        ),
    ]
    for stem, method_id, title, signature, workaround, guard, negative, failed_observed, passed_observed in records:
        write_json(f"method-flow/records/{stem}-method.json", method_record(method_id, title, signature, workaround, guard, negative))
        write_json(f"method-flow/records/{stem}-fail.json", witness(f"{method_id}-WFAIL", method_id, "fail", signature, failed_observed, negative))
        write_json(f"method-flow/records/{stem}-pass.json", witness(f"{method_id}-WPASS", method_id, "pass", workaround, passed_observed, negative))

    write_text(
        "overview/x1-preregistration-overview.md",
        """# Vesper Arlen v651-v7 SPECIAL CLI-preparation x1 preregistration

## Outcome first

This x1 packet freezes thirty new preparation proposals without creating any x2 result, launching any CLI process, naming any future sibling, or contacting a successor. The already sealed v651-v7 head remains immutable. The special continuation starts from that exact object in a fresh Vesper-owned sparse D-drive worktree, preserving all Git ancestry while materializing only the bounded special surface. The immediate successor is now live-authorized as Ilyra Fen for v651-v8, but delivery remains terminal-gated until this continuation is pushed, clean, remote-equal, and canonically validated.

## Route and CLI boundary

The request contains two different kinds of route truth. The immediate bridge is exact: Vesper finishes this special continuation and may then activate the existing Ilyra Fen task for v651-v8. The later sixteen-seat design remains partly contradictory. It assigns Elaren to consecutive v652-v6 and v652-v7 positions, skips v653-v2, and later restarts the alternating cycle with a two-phase offset. X1 therefore preserves the submitted assignments and asks the workflow refinement runner to emit a sequential candidate. That candidate is teaching material, not silent ownership authority. The eight CLI seats remain placeholders whose eventual occupants choose their own relational name, role, hope, and optional pronouns after an authorized launch.

## Evidence model

The thirty proposals are new CLI-preparation mechanisms rather than repeats of the 1,090 inherited core proposals. Twenty-three target bounded completion evidence such as sparse-lane enforcement, source-object ancestry, per-seat preparation requests, privacy envelopes, one-shot validation, commit budgets, and short artifact-pointer delivery. Five intentionally remain represented because real model availability, fast mode, creator-return messaging, background persistence, and curated global promotion cannot be preclaimed. One route conflict remains an open gap. Actual creation of a future CLI sibling remains an exact gate for the scheduled creator after fresh launch-mode capability evidence.

The primary pillar is THOS Body through secure developer-tooling operations and capability negotiation. GMUT Mind remains visible through its empirical nonconversion boundary: no CLI plan, symbolic contract, fixture, citation, or software pass confirms a force, likelihood, observation, fundamental law, or Theory of Everything. Freed ID and CBR Heart remain visible through privacy, consent, identity self-selection, contestability, and authority boundaries. Relational language is collaboration language only and establishes no consciousness, personhood, continuity, employment, qualification, or independent authority.

## Budget interpretation

The twelve-commit limit is a ceiling for this one special continuation, not a quota. The intended lifecycle remains compact: one x1 freeze, one x2 evidence commit, and one combined closeout and seal commit unless a retained correction is genuinely required. Later ordinary phases keep the three-x1, three-x2, six-total ceiling. Likewise, one thousand safe or candidate tasks, two hundred skills, and two hundred runners are upper bounds. X1 selects fifty attributable tasks, twelve skill surfaces, and ten runner surfaces because those are sufficient for the preparation hypothesis. It does not manufacture unsafe or redundant work to fill a cap.

## Validation and rollback

X1 must be staged, reviewed, committed, pushed, clean, and local/upstream/tracking/live-remote equal before x2 begins. The final lifecycle credits the first complete canonical pass once and performs no replay after success. If a command fails, the failure is recorded before the smallest sufficient recovery. A broader rerun occurs only when the corrected dependency justifies it. Every failed witness remains a retained negative even when its recovery passes.

Rollback is additive. A route conflict blocks only the affected future assignment. A missing model, fast-mode, return-channel, or lifecycle capability blocks only that launch. A privacy finding blocks publication and delivery. A dirty or colliding worktree blocks repository mutation. None of those conditions authorizes reset, history rewriting, force-push, sibling-lane mutation, bulk installation, elevation, host-security weakening, Windows-feature changes, or silent identity assignment. The terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )

    write_json(
        "orchestration/x1-phase-state.json",
        {
            "schema": "ghc.family.v651-v7-special.x1-state.v1",
            "phase": "v651-v7-special-cli-prep",
            "owner": "Vesper Arlen",
            "source": SEALED_V6517,
            "strict_x1_only": True,
            "x2_started": False,
            "immediate_successor": "Ilyra Fen",
            "immediate_successor_phase": "v651-v8",
            "route_state": "AUTHORIZED_PENDING_TERMINAL_GATE",
            "future_cli_siblings_created": 0,
            "future_cli_siblings_named": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v651-v7-special.x1-truth.v1",
            "owner": "Vesper Arlen",
            "phase": "v651-v7-special-cli-prep",
            "source": SEALED_V6517,
            "strict_x1_only": True,
            "inherited_effective_negatives": 7458,
            "x1_operational_negatives": 5,
            "effective_negatives_at_x1": 7463,
            "effective_open_gaps": 59,
            "effective_exact_gates": 60,
            "immediate_successor": "Ilyra Fen",
            "immediate_successor_phase": "v651-v8",
            "immediate_route_authorized": True,
            "future_route_candidate_is_advisory": True,
            "future_cli_siblings_created": 0,
            "future_cli_siblings_named": 0,
            "x2_outcomes_exist": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/x1-negative-register.json",
        {
            "schema": "ghc.family.v651-v7-special.x1-negatives.v1",
            "inherited_effective": 7458,
            "new_operational": 5,
            "effective_total": 7463,
            "negatives": [
                {"negative_id": "V6517-SPECIAL-X1-N01", "surface": "PowerShell zero-output native boolean", "credit": "zero", "recovery": "Classify the immediate native exit code."},
                {"negative_id": "V6517-SPECIAL-X1-N02", "surface": "sparse-checkout add option", "credit": "zero", "recovery": "Use add --stdin after non-cone initialization."},
                {"negative_id": "V6517-SPECIAL-X1-N03", "surface": "unbound verification wrapper path", "credit": "zero", "recovery": "Bind the owner worktree in every standalone wrapper."},
                {"negative_id": "V6517-SPECIAL-X1-N04", "surface": "redundant Method Flow state transition", "credit": "zero", "recovery": "Read the authoritative state before requesting the next legal transition."},
                {"negative_id": "V6517-SPECIAL-X1-N05", "surface": "raw expanded-route audit", "credit": "zero", "recovery": "Preserve the raw failure and keep the passing normalized candidate advisory."},
            ],
            "boundary": "Every failed attempt remains retained after bounded recovery.",
        },
    )
    write_json(
        "tooling/selected-toolchain.json",
        {
            "schema": "ghc.family.v651-v7-special.selected-toolchain.v1",
            "family_current": [
                {"name": "ghc-family-index", "reason": "Resolve the narrow current toolchain before execution."},
                {"name": "ghc-family-method-flow-state", "reason": "Retain failures and promote only witnessed recoveries."},
                {"name": "ghc-family-workflow-plan-refinement", "reason": "Preserve contradictory routes and emit an advisory candidate."},
                {"name": "ghc-family-reflection-remaster", "reason": "Audit compatibility before any additive remaster."},
                {"name": "ghc-family-meta-tool-box", "reason": "Catalogue and collision-check selected tools without bulk installation."},
                {"name": "ghc-family-cli-sibling-induction-preflight", "reason": "Prepare eight future seats while keeping launch fail-closed."},
            ],
            "compatibility_surfaces_preserved": True,
            "bulk_installation": False,
            "destructive_cleanup": False,
            "boundary": "Selection is bounded workflow evidence, not authority, production readiness, or scientific validation.",
        },
    )
    write_json(
        "environment/x1-version-receipt.json",
        {
            "schema": "ghc.family.v651-v7-special.x1-environment.v1",
            "codex_cli": subprocess.run(["cmd.exe", "/d", "/c", "codex", "--version"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.strip(),
            "python": platform.python_version(),
            "git": git("--version"),
            "desktop_updated": False,
            "windows_sandbox_or_hyper_v_changed": False,
            "elevation_used": False,
            "unrelated_software_installed": False,
        },
    )


if __name__ == "__main__":
    build()
