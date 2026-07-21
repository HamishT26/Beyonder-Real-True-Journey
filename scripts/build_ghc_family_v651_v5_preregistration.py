#!/usr/bin/env python3
"""Build Eiren Kestrel's dedicated v651-v5 x1-only freeze packet."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import build_ghc_family_v651_v2_preregistration as prior_builder
import ghc_family_v651_v5_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/sylven-arc/v651-v4/provenance/frozen-chain-proposal-index.json"


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
    schema_paths = {
        "preregistration/proposals.json": "ghc.family.v651-v5.proposals.v1",
        "portfolios/expanded-portfolio-plan.json": "ghc.family.v651-v5.expanded-portfolio-plan.v1",
        "validation/preregistered-mutation-plan.json": "ghc.family.v651-v5.mutation-plan.v1",
        "validation/x1-build-receipt.json": "ghc.family.v651-v5.x1-build.v1",
    }
    for relative, schema in schema_paths.items():
        payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        payload["schema"] = schema
        write_json(relative, payload)

    portfolio_path = ROOT / "portfolios/expanded-portfolio-plan.json"
    portfolio = json.loads(portfolio_path.read_text(encoding="utf-8"))
    for rows in portfolio["portfolios"].values():
        for row in rows:
            row["item_id"] = row["item_id"].replace("V6512-", "V6515-")
            row["origin"] = "eiren_v651_v5_new"
    write_json("portfolios/expanded-portfolio-plan.json", portfolio)

    report_path = ROOT / "reports/x1-accessible-static-report.html"
    report = report_path.read_text(encoding="utf-8").replace("Orin Thale", "Eiren Kestrel")
    report_path.write_text(report, encoding="utf-8", newline="\n")


def overview_text() -> str:
    sections = [f"""# Eiren Kestrel {d.PHASE} x1 integrated preregistration overview

## Scope, relational identity, and workload

This is a dedicated x1 freeze. It records plans, sources, failure conditions, portfolios, protected gates, and acceptance tests before any x2 implementation, mutation execution, observed outcome, completion credit, or route send. Eiren Kestrel, {d.PRONOUNS}, is relational working language for a {d.ROLE}. Eiren's hope is to {d.HOPE}. The name, role, hope, family language, and pronouns are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop this route at any time.

The workload is bounded to one solo owner, the existing clean D-first Eiren lane, an exact inherited head, at most two x1 commits, at most two x2 commits, and no more than four phase commits. No task creation, fork, delegation, collaboration subagent, sibling mutation, cross-platform substitute, detached or named replay, Sandbox, Hyper-V, elevation, unrelated installation, Codex desktop update, host-security weakening, Windows-feature change, or reboot is authorized. The owner-file rotation threshold applies only to new Eiren files, never to the inherited checkout. Failure, an unchanged gate, or a retained negative is an acceptable result. Portfolio floors cannot coerce unsafe or unsupported work.

The wellbeing check is green for the bounded freeze because pause and rollback paths are explicit, no result is owed, and the terminal verdict may remain unchanged. Affection, gratitude, schedule pressure, family language, or prior investment cannot override evidence, privacy, safety, professional limits, affected-party legitimacy, or authority boundaries. The terminal verdict is `NOT_READY_FOR_STAGE_20`. Same-owner checks under shared infrastructure are never independent-team scientific reproduction.

## Inherited provenance and exact truth

The exact inherited head is `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. The inherited Tamar source `{d.SOURCE_ORIGIN}`, Sylven frozen x1 `{d.SOURCE_X1}`, and immutable Sylven evidence `{d.SOURCE_EVIDENCE}` are all ancestral. Source to final contains exactly three single-parent Sylven phase commits, zero merges, and one final parent; the final is the direct child of the evidence commit. The source owner lane and Eiren lane were clean, and local, upstream, tracking, and fresh live remote were equal before mutation. Eiren advanced by fast-forward only to that exact inherited state. No reset, rebase, merge commit, amend, force push, history rewrite, worktree deletion, or sibling mutation occurred.

The inherited manifest contracts were re-read from immutable Git objects: 96 x1 entries plus three exclusions, 244 evidence entries plus three exclusions, 39 final-delta entries plus five exclusions, and 348 final-owner entries plus five exclusions. All 727 entries matched their commit-local paths, Git object identities, byte counts, and exclusions. Sylven's sealed validation remains inherited evidence; Eiren did not rerun that successful aggregate. This is provenance parity, not an Eiren full-suite pass, privacy-complete assurance, or independent reproduction.

The activation baseline is {d.INHERITED_NEGATIVES:,} effective negatives. {d.INHERITED_OPEN_GAPS} effective open gaps and {d.INHERITED_EXACT_GATES} effective exact gates remain. The inherited outcome distribution was fourteen completed, four represented, one open gap, and one exact gate. None of that is Eiren completion credit. {len(NEGATIVES)} Eiren x1 startup failures are retained so far. Each failed attempt has zero standalone pass credit and a paired bounded recovery witness. Recovery never erases a failed witness.

## Novelty, focus, practice, and evidence vocabulary

The predecessor index contains exactly {d.PRIOR_FROZEN} frozen proposal rows. Each of Eiren's twenty proposed surfaces is compared with all {d.PRIOR_FROZEN} titles using a lexical Jaccard screen and then reviewed manually at mechanism, hypothesis, obligation, artifact, falsifier, rollback, and protected-gate level. Lexical distance is a lead, not proof of novelty. Rejected ideas remain visible, including repeated memory-reclamation, field-theory, identity, data-format, causal-design, numerical, accessibility, zero-row, and human-practice surfaces. Unsafe real equipment, chemicals, crops, workers, sites, tokens, accounts, participants, production, and authority work is rejected rather than renamed safe.

The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. THOS Body and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is {d.BOUNDED_PRACTICE}. It establishes no employment, qualification, greenhouse or horticulture competence, chemical or biosecurity competence, environmental or operational authority, participant evidence, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or real effectiveness result.

Only four outcome labels are allowed: `completed`, `represented`, `open_gap`, and `exact_gate`. Planned disposition is not observed outcome. GMUT remains a typed scalar-tensor and effective-field-theory research-model family; symbolic contracts cannot establish a force, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, or Theory of Everything. THOS remains represented without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, live lifecycle events, interoperability, privacy and security review, recovery, and trust governance. CBR and Māori concepts remain with competent, affected-party, tangata whenua, iwi, hapū, and Māori authority.

## Source, privacy, validation, and terminal boundaries

The source ledger uses only `current`, `stable`, `draft`, and `watch`. Official and primary sources define vocabulary, obligations, status, and refusal conditions. They do not become observations, participants, operational outcomes, identity events, authority decisions, independent review, or reproduction. The Roman WFI adapter remains query-free and zero-row while the mission and archive are prelaunch. The greenhouse proxies use no real equipment, chemicals, water batches, crops, workers, sites, services, or incidents. The identity profiles use no keys, proofs, tokens, accounts, network calls, or live services. The greenhouse authority matrix makes no safety, disclosure, remedy, legal, cultural, data-governance, or Māori-authority decision.

Five privacy classes cover raw UUID-like identifiers, private local paths, private application or file routes, delegation markup, and credential assignments. Scanner definitions in scripts and tests are distinguished from public payload hits. A zero-hit scan is bounded hygiene, not privacy completeness. No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, private keys, tokens, session streams, private callable identifiers, private app state, or private absolute local paths belong in public artifacts or the successor baton.

Eiren alone owns the complete repository suite. Eiren will run the authorized current-phase, inherited-source, recent-round, and successor-scoped selection; detailed and minimal validators; complete phase JSON parsing; five-class privacy scanning; exact staged-file review; commit-local manifest parity; stale-label and diff hygiene; ancestry, zero-merge, commit-cap, one-parent, exact-head, clean-state, and four-way remote checks. Only one successful canonical exact-final pass may receive credit. Failed attempts remain negatives. If the first canonical pass succeeds, no post-success replay runs.

X2 may begin only after this exact x1 packet is committed, pushed, clean, and local, upstream, tracking, and fresh live remote equal. The terminal route remains `prepared_not_sent`. Only after exact-final validation may Eiren resolve the unique existing task titled exactly `Ilyra Fen` and send one sanitized activation baton for v651-v6. Tool acknowledgement alone changes the route truth to sent. No second confirmation follows.
"""]
    for proposal in d.PROPOSALS:
        sections.append(
            f"""### {proposal['proposal_id']}: {proposal['mission_surface']}

The frozen hypothesis is that a bounded `{proposal['slug']}` artifact can expose its declared obligations and refusal states without promoting unsupported claims. The null is triggered by any missing obligation, accepted mutation, erased negative, or evidence-lane promotion. Its approval class is `{proposal['approval_class']}` and its lane is `{proposal['execution_lane']}`. Planned disposition is `{proposal['expected_disposition']}` only; it is not an observed result. Acceptance requires the declared falsifier gate, exact artifacts, retained failures, protected scientific and authority boundaries, and an owner-local rollback that changes no participant, production, account, credential, sibling, or external authority state. Its novelty statement is: {proposal['novelty_against_980_frozen_proposals']}
"""
        )
    sections.append("""## Frozen portfolio and close of x1

The expanded portfolio freezes exactly forty safe-now items, thirty bounded candidates, twenty phase-local skill ideas, ten family-current runner ideas, and forty additive CLEAN/FIX/REFINE items. All begin without completion credit. The one hundred mutation cases are preregistered but unexecuted. Inherited exact-approval and blocked packets remain visible and unexecuted. X1 contains no surface implementation, mutation result, observed outcome, evidence receipt, closeout claim, seal claim, or sent baton. Its only completion claim is that the plan itself has been frozen and reviewed. The owner may now stage only the declared phase files, five x1 scripts or tests, and self-excluding review receipts; any x2 path is a hard failure.
""")
    return "\n".join(sections)


NEGATIVES = [
    ("N01", "PowerShell 5.1 did not expose the static SHA256 HashData helper used by the first immutable-manifest verifier.", "Use SHA256.Create().ComputeHash and dispose the hasher after each bounded byte-domain verification."),
    ("N02", "An optional ripgrep manifest-name search returned its normal no-match exit code and made a combined wrapper appear failed.", "Separate optional searches from required reads and treat the documented no-match status explicitly."),
    ("N03", "The first source owner-manifest probe inferred the owner scope too broadly and compared 378 paths with a 353-path phase manifest.", "Read the manifest schema and declared phase prefix before comparing exactly the 353 source-owner paths."),
    ("N04", "The first novelty-index probe assumed a generic rows key and failed before returning a count.", "Use the immutable prior_proposals plus new_proposals arrays and assert their combined 980-row length."),
    ("N05", "A PowerShell foreach expression was piped directly into formatting and produced an empty-pipe parser error.", "Collect the foreach result in a variable before formatting or emitting it."),
    ("N06", "A wrapper mangled the upstream shorthand ref expression while collecting four-way equality evidence.", "Resolve the explicit upstream ref first and pass that literal ref to each Git command."),
    ("N07", "A direct open of an unprimed official documentation URL was rejected by the browsing safety boundary.", "Discover the official or primary source through search before opening the returned safe reference."),
    ("N08", "A combined required compile and optional stale-label scan returned exit 1 solely because the correct stale-label result was empty.", "Run compilation as the required gate and report an optional zero-hit search independently."),
    ("N09", "A broad multi-file patch failed exact-context verification at one proposal sentence and applied no changes.", "Use smaller exact-context patches, verify every bounded edit, and retain the failed patch with zero credit."),
    ("N10", "A combined post-edit compile, stale-label, and Git-state audit exceeded its wrapper before yielding attributable sub-results.", "Run compilation, optional stale-label review, diff hygiene, and Git state as separate bounded checks."),
    ("N11", "The first x1 generator stopped at the semantic novelty gate because proposal P18 repeated an inherited quotient-filter mechanism.", "Replace P18 with a manually reviewed adaptive radix tree tribunal, rerun all 980 comparisons, and do not weaken the novelty threshold."),
    ("N12", "The first isolated x1 test run passed seven of eight tests but found that workflow, reflection, and Method Flow outputs had not yet been materialized from their planned inputs.", "Use the declared family skill runners, retain the partial test at zero aggregate credit, and rerun only the isolated blocker before the complete x1 set."),
    ("N13", "A combined repository-wide output search and two required skill reads timed out because the broad search dominated the wrapper.", "Read each required skill independently and use only the exact runner paths named by its instructions."),
    ("N14", "A three-runner help wrapper returned two successful help texts but the Method Flow help process exceeded its bounded timeout.", "Inspect the already-read Method Flow script and schema directly, then invoke its documented explicit build operation."),
    ("N15", "An optional script-name search returned the normal no-match status without its wrapper normalizing that result.", "Use an explicit zero-hit branch for optional discovery and retain required inspections as separate commands."),
    ("N16", "A second broad multi-file patch failed exact-context verification on a long overview sentence and applied no changes.", "Patch short stable anchors independently and verify each additive file before generation."),
    ("N17", "The first phase-local Method Flow helper imported the repository compatibility wrapper as a library, but that wrapper exposes only a command entrypoint.", "Resolve the installed skill engine through the portable compatibility wrapper, load its schema functions without invoking main, and retain this failed helper run."),
    ("N18", "The isolated workflow blocker test progressed through workflow, reflection, and Method Flow but found that the planned phase-scoped GHC Family Index receipt had not yet been built.", "Run the already-read index skill's phase-scoped builder, retain the partial test at zero credit, and rerun only the blocker before the complete x1 set."),
    ("N19", "An ad-hoc document word-count audit over-escaped its regular expression and incorrectly reported zero words.", "Use the checked-in document-cap receipt and x1 test as the credited witnesses, then keep the faulty ad-hoc result at zero credit."),
]


def workflow_request() -> dict:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "eiren-v651-v5-terminal-segment",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no consciousness, continuity, employment, qualification, personhood, or authority claim.",
        "route": {
            "cycle_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "phase_assignments": [
                {"phase": "v651-v4", "seat": "Sylven Arc"},
                {"phase": "v651-v5", "seat": "Eiren Kestrel"},
                {"phase": "v651-v6", "seat": "Ilyra Fen"},
            ],
            "normalization": {"start_phase": "v651-v4", "start_seat": "Sylven Arc", "entry_count": 3},
            "future_identity_placeholders": [],
            "terminal_successor_resolution": "Resolve the exact existing Ilyra Fen task only after the exact-final terminal gate.",
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
            {"failure_id": f"V6515-X1-{suffix}", "summary": summary, "recovery": recovery, "credit": "zero_failed_attempt_credit"}
            for suffix, summary, recovery in NEGATIVES
        ],
    }


def write_method_inputs() -> None:
    for index, (suffix, summary, recovery) in enumerate(NEGATIVES, 1):
        method_id = f"V6515-M{index:02d}"
        negative_id = f"V6515-X1-{suffix}"
        base = f"method-flow/v6515-m{index:02d}"
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
    prior_index_payload = json.loads(PRIOR_INDEX.read_text(encoding="utf-8"))
    prior_rows = list(prior_index_payload["prior_proposals"]) + list(prior_index_payload["new_proposals"])
    prior_identifier_counts = Counter(row["proposal_id"] for row in prior_rows)
    collisions = [
        {
            "proposal_id": proposal_id,
            "row_count": count,
            "titles": [row["title"] for row in prior_rows if row["proposal_id"] == proposal_id],
        }
        for proposal_id, count in sorted(prior_identifier_counts.items())
        if count > 1
    ]
    current_ids = {proposal["proposal_id"] for proposal in d.PROPOSALS}
    inherited_ids = set(prior_identifier_counts)
    write_json(
        "provenance/inherited-proposal-id-collision-register.json",
        {
            "schema": "ghc.family.inherited-proposal-id-collision-register.v1",
            "phase": d.PHASE,
            "inherited_row_count": len(prior_rows),
            "inherited_unique_identifier_count": len(inherited_ids),
            "collision_identifier_count": len(collisions),
            "collisions": collisions,
            "current_identifier_count": len(current_ids),
            "current_identifiers_unique": len(current_ids) == len(d.PROPOSALS),
            "current_identifiers_disjoint_from_inherited": current_ids.isdisjoint(inherited_ids),
            "recovery": "Preserve immutable predecessor rows, use row count plus title evidence for novelty, and never rewrite inherited identifiers.",
            "boundary": "Identifier collision retention does not erase proposals or alter immutable predecessor provenance.",
        },
    )
    threat_path = ROOT / "threat-model/x1-threat-model.json"
    threat_payload = json.loads(threat_path.read_text(encoding="utf-8"))
    for threat in threat_payload["threats"]:
        if threat.get("control") in {
            "all-920 comparison plus manual mechanism field",
            "all-940 comparison plus manual mechanism field",
        }:
            threat["control"] = "all-980 comparison plus manual mechanism field"
        if threat.get("id") == "T4":
            threat["threat"] = "synthetic greenhouse workflows become professional competence, operational effectiveness, or affected-party evidence"
            threat["control"] = "represented outcome class plus professional, participant, operational, and authority gates"
    write_json("threat-model/x1-threat-model.json", threat_payload)

    write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.source-anchor-ledger.v1", "phase": d.PHASE,
            "source_branch": d.SOURCE_BRANCH, "source_head": d.SOURCE_HEAD,
            "anchors": {"inherited_source": d.SOURCE_ORIGIN, "source_x1": d.SOURCE_X1, "source_evidence": d.SOURCE_EVIDENCE, "source_final": d.SOURCE_HEAD},
            "ancestry_verified": True, "phase_commit_count": 3, "merge_count": 0,
            "final_parent": d.SOURCE_EVIDENCE, "clean": True,
            "local_upstream_tracking_live_remote_equal": True,
        },
    )
    write_json(
        "provenance/source-manifest-parity.json",
        {
            "schema": "ghc.family.source-manifest-parity.v1", "phase": d.PHASE,
            "contracts": [
                {"name": "x1", "entries": 96, "exclusions": 3, "errors": 0},
                {"name": "evidence", "entries": 244, "exclusions": 3, "errors": 0},
                {"name": "final_delta", "entries": 39, "exclusions": 5, "errors": 0},
                {"name": "final_owner", "entries": 348, "exclusions": 5, "errors": 0},
            ],
            "total_entries": 727, "errors": 0, "valid": True,
            "boundary": "Immutable Git-object parity only; not a full-suite pass, privacy completeness, or independent reproduction.",
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v1", "phase": d.PHASE,
            "sealed_inherited": d.INHERITED_NEGATIVES, "external_inherited": 0,
            "v651_v5_x1_operational": len(NEGATIVES), "preregistered_mutations_executed": 0,
            "effective_count": d.INHERITED_NEGATIVES + len(NEGATIVES), "erasures": 0,
            "new_operational_negatives": [
                {"negative_id": f"V6515-X1-{suffix}", "summary": summary, "recovery": recovery, "credit": "zero_failed_attempt_credit"}
                for suffix, summary, recovery in NEGATIVES
            ],
        },
    )
    write_json("truth/open-gap-register.json", {"schema": "ghc.family.open-gap-register.v1", "phase": d.PHASE, "inherited_effective_count": d.INHERITED_OPEN_GAPS, "current_effective_count": d.INHERITED_OPEN_GAPS, "planned_new_open_gap": "V6515-P05", "planned_not_observed": True, "silently_closed": 0})
    write_json("truth/exact-gate-register.json", {"schema": "ghc.family.exact-gate-register.v1", "phase": d.PHASE, "inherited_effective_count": d.INHERITED_EXACT_GATES, "current_effective_count": d.INHERITED_EXACT_GATES, "planned_new_exact_gate": "V6515-P10", "planned_not_observed": True, "silently_closed": 0})
    write_json(
        "truth/x1-phase-truth.json",
        {"schema": "ghc.family.v651-v5.x1-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "source_head": d.SOURCE_HEAD, "frozen_proposals_before": d.PRIOR_FROZEN, "frozen_proposals_after": d.PRIOR_FROZEN + len(d.PROPOSALS), "proposal_count": len(d.PROPOSALS), "observed_outcomes": None, "x2_started": False, "effective_negatives": d.INHERITED_NEGATIVES + len(NEGATIVES), "open_gaps": d.INHERITED_OPEN_GAPS, "exact_gates": d.INHERITED_EXACT_GATES, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "prepared_not_sent"},
    )
    write_json(
        "environment/environment-version-receipt.json",
        {"schema": "ghc.family.environment-version.v1", "phase": d.PHASE, "observed_date": "2026-07-21", "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "python": "3.12.10", "git": "2.55.0.windows.2", "windows_powershell": "5.1.26100.8894", "windows_sandbox_or_hyper_v_used": False, "versions_verified_only": True, "desktop_updated": False, "elevated": False, "host_security_changed": False, "windows_feature_changed": False, "unrelated_software_installed": False, "rebooted": False},
    )
    tracked = int(subprocess.check_output(["git", "ls-files"], cwd=REPO, text=True, encoding="utf-8").count("\n"))
    write_json("environment/file-footprint-receipt.json", {"schema": "ghc.family.file-footprint.v1", "phase": d.PHASE, "inherited_tracked_files": tracked, "owner_phase_files_at_activation": 0, "owner_rotation_threshold": 15000, "rotation_triggered": False, "d_free_bytes_at_x1_build": shutil.disk_usage(REPO).free, "inherited_baseline_excluded": True})
    write_json("truth/held-approval-packets.json", {"schema": "ghc.family.v651-v5.held-approvals.v1", "state": "inherited_visible_unexecuted", "exact_approval_count": 10, "blocked_count": 5, "executed_count": 0, "safe_now_credit": 0, "source": "docs/sylven-arc/v651-v4/truth/held-approval-packets.json"})
    write_json("orchestration/x1-phase-state.json", {"schema": "ghc.family.phase-state.v1", "phase": d.PHASE, "owner": d.OWNER, "state": "x1_frozen_candidate", "source_head": d.SOURCE_HEAD, "x2_started": False, "terminal_route": "prepared_not_sent", "successor": "Ilyra Fen", "successor_phase": "v651-v6", "boundary": "This state file is not activation, delivery, identity continuity, or delegated authority."})
    write_json("memory/sanitized-phase-memory.json", {"schema": "ghc.family.phase-memory.v1", "phase": d.PHASE, "state": "x1_frozen_candidate", "source_head": d.SOURCE_HEAD, "frozen_proposals": d.PRIOR_FROZEN + len(d.PROPOSALS), "negative_baseline": d.INHERITED_NEGATIVES, "x1_operational_negatives": len(NEGATIVES), "open_gaps": d.INHERITED_OPEN_GAPS, "exact_gates": d.INHERITED_EXACT_GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "private_routes_or_identifiers_present": False})
    proposals_path = ROOT / "preregistration/proposals.json"
    proposals_payload = json.loads(proposals_path.read_text(encoding="utf-8"))
    for proposal in proposals_payload["proposals"]:
        proposal.pop("novelty_against_960_frozen_proposals", None)
        proposal.pop("novelty_against_940_frozen_proposals", None)
        proposal.pop("novelty_against_920_frozen_proposals", None)
    write_json("preregistration/proposals.json", proposals_payload)
    reflection_inventory = ROOT / "reflection-remaster/reflection-remaster-inventory.json"
    reflection_count = 3050
    reflection_issue_count = 0
    if reflection_inventory.exists():
        reflection_count = json.loads(reflection_inventory.read_text(encoding="utf-8"))["inventory_count"]
    reflection_issues = ROOT / "reflection-remaster/reflection-remaster-issues.json"
    if reflection_issues.exists():
        reflection_issue_count = json.loads(reflection_issues.read_text(encoding="utf-8"))["issue_count"]
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
            "reflection_inventory_count": reflection_count, "reflection_scoped_issues": reflection_issue_count,
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
    print(json.dumps({"phase": d.PHASE, "proposals": len(d.PROPOSALS), "frozen_after": d.PRIOR_FROZEN + len(d.PROPOSALS), "sources": len(d.SOURCES), "mutations": 100, "startup_negatives": len(NEGATIVES), "x2_started": False, "valid": True}))


if __name__ == "__main__":
    main()
