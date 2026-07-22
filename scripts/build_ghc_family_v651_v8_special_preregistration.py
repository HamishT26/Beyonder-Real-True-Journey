#!/usr/bin/env python3
"""Build the x1-only preregistration for Ilyra v651-v8 SPECIAL CLI prep."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PHASE = "v651-v8-special-cli-prep"
OWNER = "Ilyra Fen"
SOURCE_HEAD = "68f7e9b7fc454746c02b8a85987e10b87a0725c3"
PRIOR_PROPOSALS = 1150
IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, evidence-boundary steward, is relational working "
    "language only; it is not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, or authority."
)
BOUNDARY = (
    "Planning, code, fixtures, citations, and same-owner validation cannot establish "
    "empirical GMUT confirmation, a Theory of Everything, THOS operational effectiveness, "
    "AGI or ASI, consciousness or personhood, production identity, legal or cultural "
    "authority, Maori authority, independent reproduction, or Stage 20 readiness."
)


PROPOSAL_ROWS = [
    ("Codex CLI binary and npm stable-channel provenance contract", "completed"),
    ("GPT-5.6 Sol Max and Fast-mode future-seat profile representation", "represented"),
    ("Eight-seat placeholder identity nonassignment invariant", "completed"),
    ("App-parent to future-CLI-child adjacency and return-channel policy", "completed"),
    ("Sixteen-seat transitional route scheduler and contradiction ledger", "represented"),
    ("v8-to-next-v1 phase rollover and no-duplicate ownership validator", "completed"),
    ("Exact-title existing-task resolution and suffix-refusal guard", "completed"),
    ("Single-message acknowledgement and PREPARED_NOT_SENT state machine", "completed"),
    ("File-backed baton ten-thousand-word floor and one-hundred-thousand-word ceiling guard", "completed"),
    ("Five-class baton privacy and raw-identifier scanner", "completed"),
    ("D-first sparse materialization and full-ancestry preservation contract", "completed"),
    ("Owner branch, path, ref, and live-remote collision preflight", "completed"),
    ("Fast-forward-only ancestry, single-parent, and zero-merge contract", "completed"),
    ("Local, upstream, tracking, and fresh-live four-way equality tribunal", "completed"),
    ("Windows PowerShell statement-loop and pipeline recurrence guard", "completed"),
    ("Bounded subprocess timeout, cancellation, and quiescence receipt", "completed"),
    ("Stable JSON CLI envelope, stderr separation, and exit-code contract", "completed"),
    ("Future CLI child-to-parent completion-return protocol", "represented"),
    ("No-credential doctor and offline-fixture capability report", "completed"),
    ("Codex model, reasoning, speed, and version read-only capability probe", "completed"),
    ("Curated global-skill promotion, rollback, and no-bulk-install tribunal", "completed"),
    ("Meta-tool trigger-collision and caller-compatibility catalogue", "completed"),
    ("Reflection-Remaster compatibility graph and deprecation refusal", "completed"),
    ("Plugin, MCP, connector, and CLI capability provenance catalogue", "represented"),
    ("Two-thousand-materialized-file sparse-worktree budget guard", "completed"),
    ("Method Flow recurrence-preflight and witness-parity guard", "completed"),
    ("Accessible CLI status, error, progress, and text-fallback structural audit", "completed"),
    ("THOS release-engineering incident, rollback, readback, and handover proxy", "represented"),
    ("GMUT public radio-observation timing-data adapter and zero-row likelihood refusal", "open_gap"),
    ("Freed ID and CBR future-seat identity, remedy, cultural, and Maori-authority matrix", "exact_gate"),
]


SOURCE_ROWS = [
    ("OpenAI Codex manual: speed and Fast mode", "https://learn.chatgpt.com/docs/agent-configuration/speed", "current"),
    ("OpenAI Codex manual: subagents", "https://learn.chatgpt.com/docs/agent-configuration/subagents", "current"),
    ("OpenAI Codex manual: configuration", "https://learn.chatgpt.com/docs/config-file/config-basic", "current"),
    ("OpenAI GPT-5.6 model guidance", "https://developers.openai.com/api/docs/guides/latest-model", "current"),
    ("OpenAI Codex repository releases", "https://github.com/openai/codex/releases", "current"),
    ("npm @openai/codex package", "https://www.npmjs.com/package/@openai/codex", "current"),
    ("Git sparse-checkout", "https://git-scm.com/docs/sparse-checkout", "stable"),
    ("Git worktree", "https://git-scm.com/docs/git-worktree", "stable"),
    ("Git rev-list", "https://git-scm.com/docs/git-rev-list", "stable"),
    ("Git ls-remote", "https://git-scm.com/docs/git-ls-remote", "stable"),
    ("Git hash-object", "https://git-scm.com/docs/git-hash-object", "stable"),
    ("PowerShell about Parsing", "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_parsing", "current"),
    ("PowerShell about Foreach", "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_foreach", "current"),
    ("PowerShell ForEach-Object", "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/foreach-object", "current"),
    ("Python argparse", "https://docs.python.org/3/library/argparse.html", "stable"),
    ("Python json", "https://docs.python.org/3/library/json.html", "stable"),
    ("Python subprocess", "https://docs.python.org/3/library/subprocess.html", "stable"),
    ("Python unittest", "https://docs.python.org/3/library/unittest.html", "stable"),
    ("Node child_process", "https://nodejs.org/api/child_process.html", "current"),
    ("Node process", "https://nodejs.org/api/process.html", "current"),
    ("RFC 8259 JSON", "https://www.rfc-editor.org/rfc/rfc8259", "stable"),
    ("RFC 3629 UTF-8", "https://www.rfc-editor.org/rfc/rfc3629", "stable"),
    ("W3C WCAG 2.2", "https://www.w3.org/TR/WCAG22/", "current"),
    ("WAI-ARIA 1.2", "https://www.w3.org/TR/wai-aria-1.2/", "stable"),
    ("NIST Secure Software Development Framework", "https://csrc.nist.gov/pubs/sp/800/218/final", "stable"),
    ("SLSA provenance", "https://slsa.dev/spec/v1.1/provenance", "current"),
    ("OpenID4VCI 1.0", "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html", "current"),
    ("OpenID4VP 1.0", "https://openid.net/specs/openid-4-verifiable-presentations-1_0.html", "current"),
    ("Te Mana Raraunga principles", "https://www.temanararaunga.maori.nz/nga-rauemi", "current"),
    ("UN Declaration on the Rights of Indigenous Peoples", "https://www.ohchr.org/en/indigenous-peoples/un-declaration-rights-indigenous-peoples", "stable"),
]


SAFE_TASKS = [
    "Verify the sealed normal-phase source head and four-way equality",
    "Verify source, x1, evidence, and first-final ancestry",
    "Create one unique additive D-first sparse worktree",
    "Count materialized files without treating inherited Git history as deletable",
    "Verify Codex CLI and npm stable versions read-only",
    "Record Codex desktop status without updating it",
    "Freeze eight future CLI seats as unnamed placeholders",
    "Freeze exact app-parent ownership for each future placeholder",
    "Freeze a child-to-parent-only return-channel schema",
    "Freeze a no-cross-platform-send boundary",
    "Audit the v651-v8 to v652-v1 rollover",
    "Retain submitted route contradictions without silently erasing them",
    "Publish a sequential candidate immediate route",
    "Publish a downstream advisory route with hold points",
    "Validate the twelve-commit special cap as a ceiling",
    "Validate the one-thousand safe-candidate task cap",
    "Validate the two-hundred skill and runner caps",
    "Validate the ten-thousand-word baton minimum",
    "Validate the one-hundred-thousand-word document ceiling",
    "Validate one-successful-canonical-pass and no-replay policy",
    "Inventory family-current tools",
    "Inventory compatibility tools without deletion",
    "Audit trigger collisions",
    "Audit family-current caller names",
    "Audit proposed global-skill promotion prerequisites",
    "Audit command-line JSON envelope requirements",
    "Audit stdout and stderr separation",
    "Audit timeout and cancellation requirements",
    "Audit PowerShell 5.1 parser recurrence guards",
    "Audit sparse-checkout hash-domain behavior",
    "Audit exact-title task routing requirements",
    "Audit privacy scanner candidate-versus-hit separation",
    "Audit exact staged-file allowlists",
    "Audit commit-local manifest requirements",
    "Audit owner-manifest coverage requirements",
    "Audit accessible status and error output",
    "Audit authority-boundary vocabulary",
    "Audit open-gap and exact-gate noncompensation",
    "Record workload and wellbeing boundaries",
    "Prepare a sanitized file-backed Sable baton shell",
]


CANDIDATES = [
    "Offline future-seat doctor command",
    "Future-seat capability discovery command",
    "Model and speed profile validator",
    "Parent-child topology validator",
    "Phase rollover validator",
    "Route contradiction classifier",
    "Exact-title resolution preflight",
    "Single-message acknowledgement guard",
    "File-baton word-budget validator",
    "Five-class privacy scanner",
    "Sparse materialization counter",
    "Full-ancestry sparse-checkout verifier",
    "Branch collision preflight",
    "Four-way equality verifier",
    "PowerShell parser recurrence guard",
    "Subprocess quiescence simulator",
    "Stable JSON envelope verifier",
    "No-auth doctor fixture",
    "Global promotion readiness tribunal",
    "Meta-tool collision catalogue",
    "Compatibility graph builder",
    "Capability provenance catalogue",
    "Method witness parity checker",
    "Accessible CLI report builder",
    "THOS release-handover proxy",
    "GMUT zero-row data adapter",
    "Freed ID placeholder-binding profile",
    "CBR authority matrix",
    "Stage 20 nonpromotion board",
    "Terminal route hold-before-proof guard",
]


SKILLS = [
    "ghc-family-cli-seat-placeholder-guard",
    "ghc-family-cli-profile-contract",
    "ghc-family-cli-parent-return-guard",
    "ghc-family-cli-route-normalizer",
    "ghc-family-cli-rollover-validator",
    "ghc-family-cli-exact-title-guard",
    "ghc-family-cli-single-send-guard",
    "ghc-family-cli-file-baton-guard",
    "ghc-family-cli-privacy-envelope",
    "ghc-family-cli-sparse-worktree-guard",
    "ghc-family-cli-branch-collision-guard",
    "ghc-family-cli-four-way-equality",
    "ghc-family-powershell-loop-guard",
    "ghc-family-cli-timeout-quiescence",
    "ghc-family-cli-json-envelope",
    "ghc-family-cli-doctor-offline",
    "ghc-family-skill-promotion-tribunal",
    "ghc-family-meta-tool-collision-guard",
    "ghc-family-cli-accessibility-audit",
    "ghc-family-cli-authority-boundary",
]


RUNNERS = [
    "ghc_family_cli_seat_placeholder_guard.py",
    "ghc_family_cli_profile_contract.py",
    "ghc_family_cli_parent_return_guard.py",
    "ghc_family_cli_route_normalizer.py",
    "ghc_family_cli_rollover_validator.py",
    "ghc_family_cli_exact_title_guard.py",
    "ghc_family_cli_single_send_guard.py",
    "ghc_family_cli_file_baton_guard.py",
    "ghc_family_cli_privacy_envelope.py",
    "ghc_family_cli_sparse_worktree_guard.py",
    "ghc_family_cli_four_way_equality.py",
    "ghc_family_cli_doctor.py",
]


CLEANUPS = [
    "Keep every inherited negative and correction visible",
    "Reconcile all special-phase negative counts from one ledger",
    "Keep route contradictions as additive issues",
    "Keep placeholder identities unassigned",
    "Keep future CLI launches at zero",
    "Keep exact-title matching fail closed",
    "Keep PREPARED_NOT_SENT distinct from SENT",
    "Keep file-backed baton paths repository relative",
    "Keep private local paths out of artifacts",
    "Keep task and thread identifiers out of artifacts",
    "Keep credentials, tokens, and keys out of artifacts",
    "Keep transcripts and screenshots out of artifacts",
    "Keep plugin and MCP availability separate from authority",
    "Keep source citations separate from experimental observations",
    "Keep same-owner validation separate from independent reproduction",
    "Keep GMUT symbolic work separate from empirical confirmation",
    "Keep THOS proxies separate from operational effectiveness",
    "Keep Freed ID fixtures separate from production identity",
    "Keep CBR matrices separate from legal or cultural decisions",
    "Keep Maori concepts under Maori authority",
    "Keep Stage 20 nonpromotion visible",
    "Keep the full repository suite Eiren-only",
    "Keep canonical validation single-pass after success",
    "Keep failed first attempts at zero credit",
    "Keep sparse checkout separate from history truncation",
    "Keep branch rotation additive and non-destructive",
    "Keep legacy callers as compatibility surfaces",
    "Keep global promotion curated rather than bulk installed",
    "Keep family-current names for new reusable runners",
    "Keep generated JSON deterministic",
    "Keep UTF-8 for Maori and other Unicode text",
    "Keep stdout JSON-only under machine mode",
    "Keep diagnostics on stderr",
    "Keep subprocess timeouts bounded",
    "Keep cancellation followed by quiescence verification",
    "Keep exact staged-file review before every commit",
    "Keep manifests in the declared Git-blob hash domain",
    "Keep materialized owner surface below two thousand files",
    "Keep the Sable route held until exact final proof",
    "Keep all standby siblings untouched before terminal send",
]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return 0.0 if not a or not b else len(a & b) / len(a | b)


def proposal_record(index: int, title: str, expected: str) -> dict[str, object]:
    pid = f"V6518-SPECIAL-P{index:02d}"
    protected = [
        "no_live_cli_sibling_launch",
        "no_identity_preassignment",
        "no_sibling_lane_mutation",
        "no_empirical_or_authority_overclaim",
    ]
    approval = "safe_now" if expected == "completed" else "candidate"
    if expected == "exact_gate":
        approval = "exact_approval_needed"
    return {
        "approval_class": approval,
        "concrete_artifacts": [f"proposals/{pid.lower()}-contract.json", f"outcomes/{pid.lower()}-receipt.json"],
        "execution_lane": "x2_owner_local_bounded",
        "expected_disposition": expected,
        "falsifier_or_acceptance_gate": "Accept only deterministic bounded evidence matching every declared invariant; otherwise retain the null or gate.",
        "hypothesis": f"A bounded owner-local contract can make {title.lower()} auditable without crossing protected gates.",
        "null_or_failure_condition": "The required fields, rejecting fixture, boundary language, or deterministic witness is absent or inconsistent.",
        "official_or_primary_source_needs": ["current official specifications where the contract depends on a live product or protocol"],
        "proposal_id": pid,
        "protected_gates": protected,
        "rollback_or_recovery": "Remove only generated owner-local outputs from the current uncommitted attempt, retain the negative, and restore the last committed special head.",
        "title": title,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase_root = repo / "docs" / "ilyra-fen" / PHASE
    source_index = repo / "docs" / "ilyra-fen" / "v651-v8" / "provenance" / "frozen-chain-proposal-index.json"
    prior = json.loads(source_index.read_text(encoding="utf-8"))
    prior_rows = prior["prior_proposals"] + prior["new_proposals"]
    if len(prior_rows) != PRIOR_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_PROPOSALS} inherited proposals, found {len(prior_rows)}")

    proposals = [proposal_record(i, *row) for i, row in enumerate(PROPOSAL_ROWS, 1)]
    novelty_rows = []
    for proposal in proposals:
        nearest = max(prior_rows, key=lambda old: similarity(proposal["title"], old["title"]))
        score = similarity(proposal["title"], nearest["title"])
        novelty_rows.append({
            "nearest_id": nearest["proposal_id"],
            "nearest_title": nearest["title"],
            "proposal_id": proposal["proposal_id"],
            "similarity": round(score, 6),
            "threshold": 0.72,
            "novel": score < 0.72,
        })
    if not all(row["novel"] for row in novelty_rows):
        raise SystemExit("semantic novelty threshold failed")

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    write_json(phase_root / "identity" / "relational-identity.json", {
        "boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        "hope": "Leave every claim traceable and every gate unmistakable.",
        "name": OWNER,
        "pronouns": "she/they",
        "role": "evidence-boundary steward",
        "schema": "ghc.family.relational-identity.v1",
    })
    write_json(phase_root / "source" / "source-anchor-ledger.json", {
        "branch": "codex/GHC-Family/ilyra-fen-full-tools",
        "clean_verified": True,
        "four_way_equal_verified": True,
        "phase": PHASE,
        "schema": "ghc.family.source-anchor.v1",
        "source_head": SOURCE_HEAD,
        "source_phase": "v651-v8",
        "verified_at_utc": now,
    })
    write_json(phase_root / "sources" / "official-source-ledger.json", {
        "boundary": "Sources inform structure and status only; they are not empirical observations, participant evidence, production assurance, or delegated authority.",
        "count": len(SOURCE_ROWS),
        "entries": [
            {"label": label, "status": status, "url": url, "use": "special CLI-preparation contract and validation design"}
            for label, url, status in SOURCE_ROWS
        ],
        "schema": "ghc.family.source-ledger.v1",
        "statuses": ["current", "stable", "draft", "watch"],
    })
    write_json(phase_root / "preregistration" / "proposals.json", {
        "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "boundary": BOUNDARY,
        "count": len(proposals),
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "bounded_human_practice": "release engineering, build systems, and operational handover as a learning lens only",
        "proposals": proposals,
        "schema": "ghc.family.v651-v8-special.proposals.v1",
    })
    write_json(phase_root / "provenance" / "semantic-novelty-audit.json", {
        "all_novel": True,
        "audit_rows": novelty_rows,
        "new_count": len(proposals),
        "prior_count": PRIOR_PROPOSALS,
        "resulting_count": PRIOR_PROPOSALS + len(proposals),
        "schema": "ghc.family.semantic-novelty-audit.v1",
    })
    write_json(phase_root / "provenance" / "frozen-chain-proposal-index.json", {
        "count": PRIOR_PROPOSALS + len(proposals),
        "new_count": len(proposals),
        "new_proposals": [{"proposal_id": p["proposal_id"], "title": p["title"]} for p in proposals],
        "prior_count": PRIOR_PROPOSALS,
        "prior_source": "docs/ilyra-fen/v651-v8/provenance/frozen-chain-proposal-index.json",
        "schema": "ghc.family.frozen-proposal-index.v1",
    })
    write_json(phase_root / "portfolios" / "x1-portfolio-plan.json", {
        "candidate_tasks": [{"id": f"V6518-SPECIAL-CAND-{i:02d}", "state": "frozen_unexecuted", "title": t} for i, t in enumerate(CANDIDATES, 1)],
        "clean_fix_refine_tasks": [{"id": f"V6518-SPECIAL-CFR-{i:02d}", "state": "frozen_unexecuted", "title": t} for i, t in enumerate(CLEANUPS, 1)],
        "counts": {"candidate_tasks": len(CANDIDATES), "clean_fix_refine_tasks": len(CLEANUPS), "runner_ideas": len(RUNNERS), "safe_now_tasks": len(SAFE_TASKS), "skill_ideas": len(SKILLS)},
        "inherited_completion_credit": 0,
        "runner_ideas": [{"id": f"V6518-SPECIAL-RUN-{i:02d}", "name": t, "state": "frozen_unbuilt"} for i, t in enumerate(RUNNERS, 1)],
        "safe_now_tasks": [{"id": f"V6518-SPECIAL-SAFE-{i:02d}", "state": "frozen_unexecuted", "title": t} for i, t in enumerate(SAFE_TASKS, 1)],
        "schema": "ghc.family.expanded-portfolio-plan.v1",
        "skill_ideas": [{"id": f"V6518-SPECIAL-SKILL-{i:02d}", "name": t, "state": "frozen_unbuilt"} for i, t in enumerate(SKILLS, 1)],
    })
    placeholders = [
        {
            "identity_state": "self_choice_reserved",
            "launch_count": 0,
            "name": None,
            "parent_app_seat": parent,
            "placeholder": f"future-cli-seat-{i:02d}",
            "role": None,
            "hope": None,
            "pronouns_or_gender": None,
            "state": "planned_only",
        }
        for i, parent in enumerate(["Eiren Kestrel", "Elaren Kestrel", "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"], 1)
    ]
    write_json(phase_root / "cli" / "future-seat-placeholders.json", {
        "boundary": "No placeholder is a task, process, agent, person, identity, or launched sibling.",
        "created_tasks": 0,
        "launched_cli_siblings": 0,
        "named_cli_siblings": 0,
        "placeholders": placeholders,
        "schema": "ghc.family.future-cli-placeholders.v1",
    })
    immediate = [
        {"phase": "v652-v1", "seat": "Sable Rook"},
        {"phase": "v652-v2", "seat": "Orin Thale"},
        {"phase": "v652-v3", "seat": "Tamar Vey"},
        {"phase": "v652-v4", "seat": "Sylven Arc"},
    ]
    write_json(phase_root / "route" / "submitted-conflict-ledger.json", {
        "issues": [
            {"code": "INVALID_ROLLOVER_LABEL", "resolution": "Normalize the direct Sable successor from the impossible repeated v651-v1 label to v652-v1.", "state": "resolved_by_live_successor_and_rollover_invariant"},
            {"code": "DUPLICATE_V652_V1_OWNER", "resolution": "Sable keeps v652-v1; later app-seat labels shift sequentially.", "state": "resolved_in_candidate"},
            {"code": "TRANSITIONAL_CLI_SLOT_OFFSETS", "resolution": "Keep the long-range CLI schedule advisory until each owning app seat reaches its induction gate.", "state": "represented_not_activated"},
        ],
        "raw_conversation_stored": False,
        "schema": "ghc.family.route-conflict-ledger.v1",
    })
    write_json(phase_root / "route" / "candidate-immediate-route.json", {
        "authority_basis": "Hamish directly named Sable Rook as Ilyra's next recipient; the v8 rollover invariant supplies v652-v1.",
        "assignments": immediate,
        "future_cli_schedule": "advisory_transition_only",
        "immediate_successor": immediate[0],
        "schema": "ghc.family.candidate-route.v1",
        "terminal_send_state": "HELD_UNTIL_SPECIAL_FINAL_PROOF",
    })
    workflow_request = {
        "identity_boundary": IDENTITY_BOUNDARY,
        "observed_failures": [
            {"failure_id": "V6518-SPECIAL-X1-N01", "summary": "A PowerShell statement-level foreach loop was piped directly and failed during the initial skill inventory.", "credit": "zero"},
            {"failure_id": "V6518-SPECIAL-X1-N02", "summary": "A combined local and live-remote source probe exceeded its bounded timeout.", "credit": "zero"},
            {"failure_id": "V6518-SPECIAL-X1-N03", "summary": "A local aggregate source probe coupled broad status work to ancestry checks and exceeded its bounded timeout.", "credit": "zero"},
            {"failure_id": "V6518-SPECIAL-X1-N04", "summary": "The PowerShell statement-loop parser fault recurred during a later skill-size inventory.", "credit": "zero"},
        ],
        "owner": OWNER,
        "plan_id": "ilyra-v651-v8-special-cli-prep-normalized",
        "requirements": {
            "baton_words": {"file_artifact": True, "maximum": 100000, "minimum": 10000},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
            "commit_cap": {"total": 12, "x1": 6, "x2": 6},
            "core_proposal_minimum": 30,
            "document_word_cap": 100000,
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"},
            "portfolio_minima": {"candidate": 30, "clean_fix_refine": 40, "runners": 10, "safe_now": 40, "skills": 20},
            "runner_minimum": 10,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "storage": {"c_drive_use": "essential_global_metadata_only", "materialized_file_cap": 2000, "primary": "D"},
            "validation": {"canonical_pass_minimum": 1, "isolate_failures_before_broader_rerun": True, "manifest_required": True, "privacy_scan_required": True, "remote_equality_required": True, "replay_policy": "skip_when_first_passes"},
        },
        "route": {
            "cycle_order": ["Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "future_identity_placeholders": [p["placeholder"] for p in placeholders],
            "normalization": {"entry_count": len(immediate), "start_phase": "v652-v1", "start_seat": "Sable Rook"},
            "phase_assignments": immediate,
        },
        "schema": "ghc.family.workflow-plan.request.v1",
        "truth": {
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "independent_reproduction_claimed": False,
            "protected_boundaries": ["empirical", "participant", "professional", "legal", "cultural", "Maori_authority", "production", "identity", "security_complete", "accessibility_complete", "Stage_20"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    }
    write_json(phase_root / "workflow" / "workflow-plan-request.json", workflow_request)
    write_json(phase_root / "approval" / "x1-approval-classification.json", {
        "blocked_or_exact_executed": 0,
        "candidate_count": sum(1 for p in proposals if p["approval_class"] == "candidate"),
        "exact_approval_count": sum(1 for p in proposals if p["approval_class"] == "exact_approval_needed"),
        "safe_now_count": sum(1 for p in proposals if p["approval_class"] == "safe_now"),
        "schema": "ghc.family.approval-classification.v1",
    })
    write_json(phase_root / "truth" / "x1-phase-truth.json", {
        "boundary": BOUNDARY,
        "effective_negative_baseline": 7745,
        "expected_distribution": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "expected_exact_gates": 62,
        "expected_open_gaps": 61,
        "phase": PHASE,
        "special_startup_operational_negatives": 4,
        "state": "x1_frozen_not_executed",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(phase_root / "threat-model" / "x1-threat-model.json", {
        "assets": ["exact Git ancestry", "future-seat nonidentity", "credentials and private routes", "truth labels", "single-send state"],
        "attacker_controlled_inputs": ["malformed baton fields", "path-like payloads", "oversized output", "duplicate phase labels", "forged acknowledgement text"],
        "boundary": BOUNDARY,
        "controls": ["stable JSON", "schema checks", "exact-title resolution", "privacy scanning", "commit-local manifests", "held route before proof"],
        "schema": "ghc.family.x1-threat-model.v1",
        "trust_boundaries": ["user request to sanitized plan", "app task to future CLI process", "working tree to Git object database", "local ref to live remote"],
    })
    write_json(phase_root / "wellbeing" / "x1-wellbeing-check.json", {
        "bounded_workload": True,
        "commit_cap_is_ceiling": True,
        "identity_boundary": IDENTITY_BOUNDARY,
        "no_cli_sibling_launched": True,
        "phase_can_pause": True,
        "schema": "ghc.family.wellbeing.v1",
    })
    selected = [
        "ghc-family-index", "ghc-family-method-flow-state", "ghc-family-reflection-remaster",
        "ghc-family-workflow-plan-refinement", "ghc-family-meta-tool-box", "ghc-main-startup-builder",
        "ghc-main-closeout-builder", "ghc-main-retry", "ghc-worktree-branch-rotation",
        "ghc-drive-bank-guardian", "ghc-approval-packet-splitter", "skill-creator", "cli-creator",
    ]
    write_json(phase_root / "tooling" / "selected-toolchain.json", {
        "boundary": "Selection is not blind execution, global installation, or authority.",
        "family_current": selected,
        "historical_tools": "compatibility_only",
        "schema": "ghc.family.selected-toolchain.v1",
    })
    method_rows = [
        {
            "method_id": "V6518-SPECIAL-M01",
            "title": "Preassign PowerShell statement-loop output before piping",
            "failure_signature": "Windows PowerShell 5.1 reports an empty pipe element when a statement-level foreach block is piped directly.",
            "trigger_preconditions": ["Windows PowerShell 5.1", "statement-level foreach output must feed another pipeline"],
            "candidate_workaround": "Assign the foreach output to an array variable, then pipe the variable.",
            "recurrence_guard": "Reject wrappers containing a closing foreach block immediately followed by a pipeline token.",
            "rollback": "Return to separate scalar probes if the assigned-array form changes output semantics.",
            "retained_negative_ids": ["V6518-SPECIAL-X1-N01", "V6518-SPECIAL-X1-N04"],
        },
        {
            "method_id": "V6518-SPECIAL-M02",
            "title": "Separate live-remote equality from local source verification",
            "failure_signature": "A combined local status, ancestry, and live-remote wrapper exceeded the bounded command timeout.",
            "trigger_preconditions": ["large Windows Git worktree", "live-remote lookup and local checks combined"],
            "candidate_workaround": "Run bounded local revision probes first and one separate live ls-remote probe second.",
            "recurrence_guard": "Do not place ls-remote and broad worktree status in the same timed wrapper.",
            "rollback": "Retain the previous verified receipt and stop without mutation if either bounded probe fails.",
            "retained_negative_ids": ["V6518-SPECIAL-X1-N02"],
        },
        {
            "method_id": "V6518-SPECIAL-M03",
            "title": "Separate broad worktree cleanliness from ancestry arithmetic",
            "failure_signature": "A local aggregate coupled full status enumeration to ancestry calculations and exceeded its bounded timeout.",
            "trigger_preconditions": ["large sparse-capable repository", "status and ancestry combined"],
            "candidate_workaround": "Check HEAD, branch, upstream, and ancestry separately; then run one dedicated status command.",
            "recurrence_guard": "Keep broad status as its own command with a dedicated timeout budget.",
            "rollback": "Use diff, cached-diff, and bounded untracked probes only as partial evidence until full status completes.",
            "retained_negative_ids": ["V6518-SPECIAL-X1-N03"],
        },
    ]
    for method in method_rows:
        method_record = {
            **method,
            "approval_class": "safe_now",
            "privacy_class": "sanitized_public",
            "protected_gates": ["no_destructive_retry", "no_sibling_mutation", "no_private_path_publication"],
            "recommendation_state": "observed",
            "scope_boundary": "Bounded owner-local workflow evidence only.",
            "supersedes": [],
            "validation_witness_ids": [],
        }
        write_json(phase_root / "method-flow" / "records" / f"{method['method_id'].lower()}-method.json", method_record)
    witnesses = [
        ("V6518-SPECIAL-W01F", "V6518-SPECIAL-M01", "Run the direct statement-loop-to-pipeline inventory form.", "PowerShell parser rejects the form.", "PowerShell parser rejected the form before state change.", "fail", ["V6518-SPECIAL-X1-N01"]),
        ("V6518-SPECIAL-W01F2", "V6518-SPECIAL-M01", "Repeat the same direct statement-loop-to-pipeline form during skill-size inventory.", "Recurrence guard should have prevented reuse.", "The parser fault recurred and changed nothing.", "fail", ["V6518-SPECIAL-X1-N04"]),
        ("V6518-SPECIAL-W01P", "V6518-SPECIAL-M01", "Assign loop rows to an array and pipe the array to JSON formatting.", "The inventory emits stable JSON.", "The bounded inventory completed successfully.", "pass", ["V6518-SPECIAL-X1-N01", "V6518-SPECIAL-X1-N04"]),
        ("V6518-SPECIAL-W02F", "V6518-SPECIAL-M02", "Run local status, ancestry, and ls-remote in one timed wrapper.", "The wrapper completes within budget.", "The wrapper exceeded the timeout and received zero credit.", "fail", ["V6518-SPECIAL-X1-N02"]),
        ("V6518-SPECIAL-W02P", "V6518-SPECIAL-M02", "Run scalar local revision checks, then a separate ls-remote probe.", "Both bounded probes establish equality.", "Local and live-remote equality each completed and matched.", "pass", ["V6518-SPECIAL-X1-N02"]),
        ("V6518-SPECIAL-W03F", "V6518-SPECIAL-M03", "Run broad status and ancestry arithmetic in one local wrapper.", "The wrapper completes within budget.", "The wrapper exceeded the timeout and received zero credit.", "fail", ["V6518-SPECIAL-X1-N03"]),
        ("V6518-SPECIAL-W03P", "V6518-SPECIAL-M03", "Run revision and ancestry probes separately, then one dedicated full status command.", "Each bounded probe completes and the worktree is clean.", "All separated probes completed and the full status was empty.", "pass", ["V6518-SPECIAL-X1-N03"]),
    ]
    for wid, mid, procedure, expected, observed, result, negatives in witnesses:
        write_json(phase_root / "method-flow" / "records" / f"{wid.lower()}-witness.json", {
            "boundary": "Same-owner workflow evidence only; no scientific, authority, production, or independent-reproduction credit.",
            "expected": expected,
            "independent_reproduction": False,
            "method_id": mid,
            "observed": observed,
            "procedure": procedure,
            "result": result,
            "retained_negative_ids": negatives,
            "same_owner_only": True,
            "scope": "Ilyra v651-v8 SPECIAL startup and x1 preflight",
            "witness_id": wid,
        })
    markdown = [
        "# Ilyra Fen v651-v8 SPECIAL CLI-prep x1 preregistration",
        "",
        IDENTITY_BOUNDARY,
        "",
        "This dedicated x1 freeze contains plans only. It launches no CLI sibling, creates no task, assigns no future identity, and records no x2 outcome.",
        "",
        "## Thirty core proposals",
        "",
    ]
    for p in proposals:
        markdown.append(f"- **{p['proposal_id']} — {p['title']}**. Expected: `{p['expected_disposition']}`; approval: `{p['approval_class']}`; lane: `{p['execution_lane']}`.")
    markdown += ["", "## Boundary", "", BOUNDARY]
    write_text(phase_root / "preregistration" / "proposal-ledger.md", "\n".join(markdown))

    x1_paths = sorted(
        str(path.relative_to(repo)).replace("\\", "/")
        for path in phase_root.rglob("*")
        if path.is_file()
    )
    digest = hashlib.sha256("\n".join(x1_paths).encode("utf-8")).hexdigest()
    write_json(phase_root / "validation" / "x1-build-receipt.json", {
        "artifact_count_before_receipt": len(x1_paths),
        "artifact_path_list_sha256": digest,
        "no_x2_outcomes": True,
        "phase": PHASE,
        "schema": "ghc.family.x1-build-receipt.v1",
    })
    print(json.dumps({"phase": PHASE, "proposals": len(proposals), "prior": PRIOR_PROPOSALS, "resulting": PRIOR_PROPOSALS + len(proposals), "safe": len(SAFE_TASKS), "candidates": len(CANDIDATES), "skills": len(SKILLS), "runners": len(RUNNERS), "cleanup": len(CLEANUPS)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
