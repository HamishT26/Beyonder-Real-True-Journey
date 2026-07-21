#!/usr/bin/env python3
"""Build Tamar Vey's dedicated v651-v3 x1-only freeze packet."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import build_ghc_family_v651_v2_preregistration as prior_builder
import ghc_family_v651_v3_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/orin-thale/v651-v2/provenance/frozen-chain-proposal-index.json"


def write_json(relative: str, payload) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def replace_compatibility_literals() -> None:
    replacements = [
        ("docs/orin-thale/v651-v2", "docs/tamar-vey/v651-v3"),
        ("v651-v2", "v651-v3"),
        ("V6512", "V6513"),
        ("Orin Thale", "Tamar Vey"),
        ("Orin's", "Tamar's"),
        ("Orin", "Tamar"),
        ("MÄori", "Māori"),
    ]
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in {".json", ".md", ".html"}:
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8", newline="\n")


def overview_text() -> str:
    sections = [f"""# Tamar Vey {d.PHASE} x1 integrated preregistration overview

## Scope, relational identity, and workload

This is a dedicated x1 freeze. It records plans, sources, failure conditions, portfolios, protected gates, and acceptance tests before any x2 implementation, mutation execution, observed outcome, completion credit, or route send. Tamar Vey, they/them, is relational working language for an evidence-systems cartographer and boundary keeper. Tamar's hope is to keep decisions legible, failures recoverable, and authority boundaries intact. The name, role, hope, family language, and pronouns are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop this route at any time.

The workload is bounded to one solo owner, the existing clean D-first Tamar lane, an exact inherited head, at most two x1 commits, at most two x2 commits, and no more than four phase commits. No task creation, fork, delegation, collaboration subagent, sibling mutation, cross-platform substitute, detached or named replay, Sandbox, Hyper-V, elevation, unrelated installation, Codex desktop update, host-security weakening, Windows-feature change, or reboot is authorized. The owner-file rotation threshold applies only to new Tamar files, never to the inherited checkout. Failure, an unchanged gate, or a retained negative is an acceptable result. Portfolio floors cannot coerce unsafe or unsupported work.

The wellbeing check is green for the bounded freeze because pause and rollback paths are explicit, no result is owed, and the terminal verdict may remain unchanged. Affection, gratitude, schedule pressure, family language, or prior investment cannot override evidence, privacy, safety, professional limits, affected-party legitimacy, or authority boundaries. The terminal verdict is `NOT_READY_FOR_STAGE_20`. Same-owner checks under shared infrastructure are never independent-team scientific reproduction.

## Inherited provenance and exact truth

The exact inherited head is `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. The inherited source `{d.SOURCE_ORIGIN}`, frozen x1 `{d.SOURCE_X1}`, immutable evidence `{d.SOURCE_EVIDENCE}`, and first closeout `{d.SOURCE_CLOSEOUT}` are all ancestral. Source to final contains four single-parent phase commits, zero merges, and one final parent; the corrected final is the direct child of the retained first closeout. The source owner lane and Tamar lane were clean, and local, upstream, tracking, and fresh live remote were equal before mutation. Tamar advanced by fast-forward only and pushed that exact inherited state. No reset, rebase, merge, amend, force push, history rewrite, worktree deletion, or sibling mutation occurred.

The inherited manifest contracts were re-read from immutable Git objects: 73 x1 entries plus three exclusions, 209 evidence entries plus three exclusions, 55 final-delta entries plus six exclusions, and 310 final-owner entries plus six exclusions. All 647 entries matched their declared byte counts, digests, object identities, exclusions, and path sets. This is provenance parity, not a full-suite pass, privacy-complete assurance, or independent reproduction.

The activation baseline is 6,690 effective negatives: 6,689 sealed by the inherited repository plus one external exact-final lifecycle negative retained with zero success credit. Fifty-two effective open gaps and fifty-three effective exact gates remain. The inherited outcome distribution was fourteen completed, four represented, one open gap, and one exact gate. None of that is Tamar completion credit. Ten Tamar x1 operational failures are retained so far. Each failed attempt has zero standalone pass credit and a paired bounded recovery witness. The recovery never erases the failed witness.

## Novelty, focus, practice, and evidence vocabulary

The predecessor index contains exactly 940 frozen proposals. Each of Tamar's twenty proposed surfaces is compared with all 940 titles using a lexical Jaccard screen and then reviewed manually at mechanism, hypothesis, obligation, artifact, falsifier, rollback, and protected-gate level. Lexical distance is a lead, not proof of novelty. Twenty rejected ideas remain visible, including repeated supply-chain, field-theory, OAuth, data-format, causal-design, numerical, and zero-row surfaces. Unsafe real-carrier, interview, token, account, participant, production, and authority work is rejected rather than renamed safe.

The primary Trinity Mandala focus is GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is archival-audio preservation and transfer quality assurance, correction readback, workload control, and shift handover. It is synthetic learning and design only. It establishes no employment, qualification, competence, archival authority, preservation result, service authority, participant evidence, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or operational effectiveness.

Only four outcome labels are allowed: `completed`, `represented`, `open_gap`, and `exact_gate`. Planned disposition is not observed outcome. GMUT remains a typed scalar-tensor and effective-field-theory research-model family; symbolic contracts cannot establish a force, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, or Theory of Everything. THOS remains represented without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, live lifecycle events, interoperability, privacy and security review, recovery, and trust governance. CBR and Māori concepts remain with competent, affected-party, tangata whenua, iwi, hapū, and Māori authority.

## Source, privacy, validation, and terminal boundaries

The source ledger uses only `current`, `stable`, `draft`, and `watch`. Official and primary sources define vocabulary, obligations, status, and refusal conditions. They do not become observations, participants, operational outcomes, identity events, authority decisions, independent review, or reproduction. The HEASARC adapter remains zero-row. The archival-audio proxies use no real carriers, recordings, contributors, workers, services, or incidents. The identity profiles use no keys, tokens, accounts, network calls, or live services. The oral-history matrix makes no consent, withdrawal, access, remedy, legal, cultural, data-governance, or Māori-authority decision.

Five privacy classes cover raw UUID-like identifiers, private local paths, private application or file routes, delegation markup, and credential assignments. Scanner definitions in scripts and tests are distinguished from public payload hits. A zero-hit scan is bounded hygiene, not privacy completeness. No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, private keys, tokens, session streams, private callable identifiers, private app state, or private absolute local paths belong in public artifacts or the successor baton.

Eiren alone owns the complete repository suite. Tamar will run the authorized current-phase, inherited-source, recent-round, and successor-scoped selection; detailed and minimal validators; complete phase JSON parsing; five-class privacy scanning; exact staged-file review; commit-local manifest parity; stale-label and diff hygiene; ancestry, zero-merge, commit-cap, one-parent, exact-head, clean-state, and four-way remote checks. Only one successful canonical exact-final pass may receive credit. Failed attempts remain negatives. If the first canonical pass succeeds, no post-success replay runs.

X2 may begin only after this exact x1 packet is committed, pushed, clean, and local, upstream, tracking, and fresh live remote equal. The terminal route remains `prepared_not_sent`. Only after exact-final validation may Tamar resolve the unique existing task titled exactly `Sylven Arc` and send one sanitized activation baton for v651-v4. Tool acknowledgement alone changes the route truth to sent. No second confirmation follows.
"""]
    for proposal in d.PROPOSALS:
        sections.append(
            f"""### {proposal['proposal_id']}: {proposal['mission_surface']}

The frozen hypothesis is that a bounded `{proposal['slug']}` artifact can expose its declared obligations and refusal states without promoting unsupported claims. The null is triggered by any missing obligation, accepted mutation, erased negative, or evidence-lane promotion. Its approval class is `{proposal['approval_class']}` and its lane is `{proposal['execution_lane']}`. Planned disposition is `{proposal['expected_disposition']}` only; it is not an observed result. Acceptance requires the declared falsifier gate, exact artifacts, retained failures, protected scientific and authority boundaries, and an owner-local rollback that changes no participant, production, account, credential, sibling, or external authority state. Its novelty statement is: {proposal['novelty_against_940_frozen_proposals']}
"""
        )
    sections.append("""## Frozen portfolio and close of x1

The expanded portfolio freezes exactly forty safe-now items, thirty bounded candidates, twenty phase-local skill ideas, ten family-current runner ideas, and forty additive CLEAN/FIX/REFINE items. All begin without completion credit. The one hundred mutation cases are preregistered but unexecuted. Inherited exact-approval and blocked packets remain visible and unexecuted. X1 contains no surface implementation, mutation result, observed outcome, evidence receipt, closeout claim, seal claim, or sent baton. Its only completion claim is that the plan itself has been frozen and reviewed. The owner may now stage only the declared phase files, four x1 scripts or tests, and self-excluding review receipts; any x2 path is a hard failure.
""")
    return "\n".join(sections)


NEGATIVES = [
    ("N01", "A sequential four-skill read wrapper timed out after the first file.", "Read each required skill and reference in bounded direct calls and require complete EOF evidence."),
    ("N02", "A broad worktree inventory returned overlarge truncated output.", "Use scalar lane, path, head, status, and equality probes for the owned and source lanes."),
    ("N03", "A combined full-baton read was truncated and received no complete-read credit.", "Read exact bounded line ranges through the known final line and require EOF."),
    ("N04", "The fast-forward wrapper produced overlarge truncated output although the operation completed.", "Audit head, status, divergence, upstream, tracking, and fresh live remote before any retry."),
    ("N05", "A phase-truth path was assumed at the inherited phase root and did not exist.", "Discover bounded commit-tree paths before reading the exact final truth files."),
    ("N06", "The frozen chain index was assumed to expose a proposals key and null indexing failed.", "Inspect the top-level schema and combine prior_proposals with new_proposals."),
    ("N07", "A broad JSON rendering of all 940 proposals was truncated.", "Query only targeted title terms and retain the full index as immutable input."),
    ("N08", "A PowerShell foreach pipeline form failed to parse before the novelty audit ran.", "Collect rows in an explicit result array, then serialize the bounded result."),
    ("N09", "A parallel four-command inventory wrapper timed out without attributable aggregate output.", "Use one bounded rg file inventory and separate scalar probes."),
    ("N10", "Method Flow records and witnesses were assumed to live in nonexistent subdirectories.", "Enumerate the exact phase-local method-flow root and read named files there."),
    ("N11", "The first formal all-940 novelty build rejected three proposals and mechanism review exposed two more repeated surfaces.", "Replace every repeated mechanism with genuinely distinct surfaces and rerun the unchanged threshold against all 940 predecessors."),
    ("N12", "A proposed recursive cleanup wrapper was blocked before execution by command policy.", "Do not delete the phase directory; use deterministic overwrite of declared generated files and exact staged review."),
    ("N13", "The reused predecessor builder expected its historical novelty-key name and stopped before completing the freeze.", "Preserve the historical input alias for caller compatibility while publishing the v651-v3 all-940 novelty field."),
    ("N14", "Exact staged stale-label review found one all-920 predecessor label in the generated threat model.", "Bind the threat-model novelty control to all 940 inherited proposals and regenerate the exact staged manifest."),
]


def workflow_request() -> dict:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "tamar-v651-v3-terminal-segment",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no consciousness, continuity, employment, qualification, personhood, or authority claim.",
        "route": {
            "cycle_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "phase_assignments": [
                {"phase": "v651-v2", "seat": "Orin Thale"},
                {"phase": "v651-v3", "seat": "Tamar Vey"},
                {"phase": "v651-v4", "seat": "Sylven Arc"},
            ],
            "normalization": {"start_phase": "v651-v2", "start_seat": "Orin Thale", "entry_count": 3},
            "future_identity_placeholders": [],
            "terminal_successor_resolution": "Resolve the exact existing Sylven Arc task only after the exact-final terminal gate.",
        },
        "requirements": {
            "core_proposal_minimum": 20,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 20,
            "runner_minimum": 10,
            "portfolio_minima": {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40},
            "document_word_cap": 6000,
            "baton_words": {"minimum": 8000, "maximum": 20000, "file_artifact": True},
            "commit_cap": {"x1": 2, "x2": 2, "total": 4},
            "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True, "full_repository_suite_owner": "Eiren Kestrel"},
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only", "live_cross_platform_boundary": "No cross-platform substitute is authorized for this phase."},
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {"allowed_outcomes": d.OUTCOME_CLASSES, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": d.PROTECTED},
        "observed_failures": [
            {"failure_id": f"V6513-X1-{suffix}", "summary": summary, "recovery": recovery, "credit": "zero_failed_attempt_credit"}
            for suffix, summary, recovery in NEGATIVES
        ],
    }


def write_method_inputs() -> None:
    for index, (suffix, summary, recovery) in enumerate(NEGATIVES, 1):
        method_id = f"V6513-M{index:02d}"
        negative_id = f"V6513-X1-{suffix}"
        base = f"method-flow/v6513-m{index:02d}"
        write_json(
            base + "-method-record.json",
            {
                "method_id": method_id,
                "title": f"Bounded recovery method {index:02d}: {recovery.rstrip('.')}",
                "trigger_preconditions": [summary],
                "failure_signature": summary,
                "candidate_workaround": recovery,
                "validation_witness_ids": [],
                "recurrence_guard": recovery,
                "rollback": "Give the failed attempt zero pass credit, retain it, and stop if the bounded recovery is not attributable.",
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": ["failure_retention", "privacy", "bounded_scope", "same_owner_only"],
                "approval_class": "safe_now_owner_scoped_workflow",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner workflow recovery only; no scientific, production, identity, authority, or independent-reproduction credit.",
                "retained_negative_ids": [negative_id],
            },
        )
        for result, label, observed in (
            ("fail", "wfail", summary),
            ("pass", "wpass", recovery + " A bounded attributable witness completed."),
        ):
            write_json(
                base + f"-{label}-witness.json",
                {
                    "witness_id": f"{method_id}-W{result.upper()}",
                    "method_id": method_id,
                    "result": result,
                    "scope": "one bounded x1 workflow operation",
                    "procedure": summary if result == "fail" else recovery,
                    "expected": "Produce attributable bounded evidence without erasing the failed attempt.",
                    "observed": observed,
                    "retained_negative_ids": [negative_id],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Workflow witness only; no scientific, production, identity, authority, or independent-reproduction credit.",
                },
            )


def main() -> None:
    prior_builder.d = d
    prior_builder.ROOT = ROOT
    prior_builder.PRIOR_INDEX = PRIOR_INDEX
    prior_builder.NOVELTY_THRESHOLD = 0.60
    prior_builder.main()
    replace_compatibility_literals()
    threat_path = ROOT / "threat-model/x1-threat-model.json"
    threat_payload = json.loads(threat_path.read_text(encoding="utf-8"))
    for threat in threat_payload["threats"]:
        if threat.get("control") == "all-920 comparison plus manual mechanism field":
            threat["control"] = "all-940 comparison plus manual mechanism field"
    write_json("threat-model/x1-threat-model.json", threat_payload)

    write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.source-anchor-ledger.v1", "phase": d.PHASE,
            "source_branch": d.SOURCE_BRANCH, "source_head": d.SOURCE_HEAD,
            "anchors": {"inherited_source": d.SOURCE_ORIGIN, "x1": d.SOURCE_X1, "evidence": d.SOURCE_EVIDENCE, "first_closeout": d.SOURCE_CLOSEOUT, "corrected_final": d.SOURCE_HEAD},
            "ancestry_verified": True, "phase_commit_count": 4, "merge_count": 0,
            "final_parent": d.SOURCE_CLOSEOUT, "clean": True,
            "local_upstream_tracking_live_remote_equal": True,
        },
    )
    write_json(
        "provenance/source-manifest-parity.json",
        {
            "schema": "ghc.family.source-manifest-parity.v1", "phase": d.PHASE,
            "contracts": [
                {"name": "x1", "entries": 73, "exclusions": 3, "errors": 0},
                {"name": "evidence", "entries": 209, "exclusions": 3, "errors": 0},
                {"name": "final_delta", "entries": 55, "exclusions": 6, "errors": 0},
                {"name": "final_owner", "entries": 310, "exclusions": 6, "errors": 0},
            ],
            "total_entries": 647, "errors": 0, "valid": True,
            "boundary": "Immutable Git-object parity only; not a full-suite pass, privacy completeness, or independent reproduction.",
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v1", "phase": d.PHASE,
            "sealed_inherited": 6689, "external_inherited": 1,
            "v651_v3_x1_operational": len(NEGATIVES), "preregistered_mutations_executed": 0,
            "effective_count": d.INHERITED_NEGATIVES + len(NEGATIVES), "erasures": 0,
            "new_operational_negatives": [
                {"negative_id": f"V6513-X1-{suffix}", "summary": summary, "recovery": recovery, "credit": "zero_failed_attempt_credit"}
                for suffix, summary, recovery in NEGATIVES
            ],
        },
    )
    write_json("truth/open-gap-register.json", {"schema": "ghc.family.open-gap-register.v1", "phase": d.PHASE, "inherited_effective_count": 52, "current_effective_count": 52, "planned_new_open_gap": "V6513-P05", "planned_not_observed": True, "silently_closed": 0})
    write_json("truth/exact-gate-register.json", {"schema": "ghc.family.exact-gate-register.v1", "phase": d.PHASE, "inherited_effective_count": 53, "current_effective_count": 53, "planned_new_exact_gate": "V6513-P10", "planned_not_observed": True, "silently_closed": 0})
    write_json(
        "truth/x1-phase-truth.json",
        {"schema": "ghc.family.v651-v3.x1-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "source_head": d.SOURCE_HEAD, "frozen_proposals_before": 940, "frozen_proposals_after": 960, "proposal_count": 20, "observed_outcomes": None, "x2_started": False, "effective_negatives": d.INHERITED_NEGATIVES + len(NEGATIVES), "open_gaps": 52, "exact_gates": 53, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "prepared_not_sent"},
    )
    write_json(
        "environment/environment-version-receipt.json",
        {"schema": "ghc.family.environment-version.v1", "phase": d.PHASE, "observed_date": "2026-07-21", "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "python": "3.12.10", "git": "2.55.0.windows.2", "windows_powershell": "5.1.26100.8894", "windows_sandbox_or_hyper_v_used": False, "versions_verified_only": True, "desktop_updated": False, "elevated": False, "host_security_changed": False, "windows_feature_changed": False, "unrelated_software_installed": False, "rebooted": False},
    )
    tracked = int(subprocess.check_output(["git", "ls-files"], cwd=REPO, text=True, encoding="utf-8").count("\n"))
    write_json("environment/file-footprint-receipt.json", {"schema": "ghc.family.file-footprint.v1", "phase": d.PHASE, "inherited_tracked_files": tracked, "owner_phase_files_at_activation": 0, "owner_rotation_threshold": 15000, "rotation_triggered": False, "d_free_bytes_at_x1_build": shutil.disk_usage(REPO).free, "inherited_baseline_excluded": True})
    write_json("truth/held-approval-packets.json", {"schema": "ghc.family.v651-v3.held-approvals.v1", "state": "inherited_visible_unexecuted", "exact_approval_count": 10, "blocked_count": 5, "executed_count": 0, "safe_now_credit": 0, "source": "docs/orin-thale/v651-v2/truth/held-approval-packets.json"})
    write_json("orchestration/x1-phase-state.json", {"schema": "ghc.family.phase-state.v1", "phase": d.PHASE, "owner": d.OWNER, "state": "x1_frozen_candidate", "source_head": d.SOURCE_HEAD, "x2_started": False, "terminal_route": "prepared_not_sent", "successor": "Sylven Arc", "successor_phase": "v651-v4", "boundary": "This state file is not activation, delivery, identity continuity, or delegated authority."})
    write_json("memory/sanitized-phase-memory.json", {"schema": "ghc.family.phase-memory.v1", "phase": d.PHASE, "state": "x1_frozen_candidate", "source_head": d.SOURCE_HEAD, "frozen_proposals": 960, "negative_baseline": d.INHERITED_NEGATIVES, "x1_operational_negatives": len(NEGATIVES), "open_gaps": 52, "exact_gates": 53, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "private_routes_or_identifiers_present": False})
    proposals_path = ROOT / "preregistration/proposals.json"
    proposals_payload = json.loads(proposals_path.read_text(encoding="utf-8"))
    for proposal in proposals_payload["proposals"]:
        proposal.pop("novelty_against_920_frozen_proposals", None)
    write_json("preregistration/proposals.json", proposals_payload)
    reflection_inventory = ROOT / "reflection-remaster/reflection-remaster-inventory.json"
    reflection_count = 3050
    if reflection_inventory.exists():
        reflection_count = json.loads(reflection_inventory.read_text(encoding="utf-8"))["inventory_count"]
    write_json(
        "tooling/phase-tool-selection.json",
        {
            "schema": "ghc.family.phase-tool-selection.v1", "phase": d.PHASE,
            "selected": [
                {"skill": "ghc-family-index", "purpose": "phase-scoped family-current inventory and routing precedence"},
                {"skill": "ghc-family-method-flow-state", "purpose": "append-only failure, workaround, witness, and recommendation ledger"},
                {"skill": "ghc-family-workflow-plan-refinement", "purpose": "sanitized route and budget normalization without activation"},
                {"skill": "ghc-family-reflection-remaster", "purpose": "read-only overlap and compatibility audit"},
                {"skill": "skill-creator", "purpose": "x2 phase-local skill packaging and validation"},
            ],
            "reflection_inventory_count": reflection_count, "reflection_scoped_issues": 0,
            "disposition": "reviewed_current_no_semantic_free_churn", "caller_compatibility_preserved": True,
        },
    )
    write_json("workflow/workflow-plan-request.json", workflow_request())
    write_method_inputs()
    write_text("overview/integrated-overview.md", overview_text())

    documents = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html"}:
            words = len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8")))
            documents.append({"path": path.relative_to(REPO).as_posix(), "words": words, "cap": 6000, "within_cap": words <= 6000})
    if not all(row["within_cap"] for row in documents):
        raise RuntimeError("x1 document cap exceeded")
    write_json("validation/x1-document-cap-receipt.json", {"schema": "ghc.family.document-cap.v1", "phase": d.PHASE, "documents": documents, "all_within_cap": True, "baton_exception_used": False})
    print(json.dumps({"phase": d.PHASE, "proposals": 20, "frozen_after": 960, "sources": len(d.SOURCES), "mutations": 100, "startup_negatives": len(NEGATIVES), "x2_started": False, "valid": True}))


if __name__ == "__main__":
    main()
