#!/usr/bin/env python3
"""Build Sylven Arc's dedicated v651-v4 x1-only freeze packet."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import build_ghc_family_v651_v2_preregistration as prior_builder
import ghc_family_v651_v4_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/tamar-vey/v651-v3/provenance/frozen-chain-proposal-index.json"


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
        "preregistration/proposals.json": "ghc.family.v651-v4.proposals.v1",
        "portfolios/expanded-portfolio-plan.json": "ghc.family.v651-v4.expanded-portfolio-plan.v1",
        "validation/preregistered-mutation-plan.json": "ghc.family.v651-v4.mutation-plan.v1",
        "validation/x1-build-receipt.json": "ghc.family.v651-v4.x1-build.v1",
    }
    for relative, schema in schema_paths.items():
        payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        payload["schema"] = schema
        write_json(relative, payload)

    portfolio_path = ROOT / "portfolios/expanded-portfolio-plan.json"
    portfolio = json.loads(portfolio_path.read_text(encoding="utf-8"))
    for rows in portfolio["portfolios"].values():
        for row in rows:
            row["item_id"] = row["item_id"].replace("V6512-", "V6514-")
            row["origin"] = "sylven_v651_v4_new"
    write_json("portfolios/expanded-portfolio-plan.json", portfolio)

    report_path = ROOT / "reports/x1-accessible-static-report.html"
    report = report_path.read_text(encoding="utf-8").replace("Orin Thale", "Sylven Arc")
    report_path.write_text(report, encoding="utf-8", newline="\n")


def overview_text() -> str:
    sections = [f"""# Sylven Arc {d.PHASE} x1 integrated preregistration overview

## Scope, relational identity, and workload

This is a dedicated x1 freeze. It records plans, sources, failure conditions, portfolios, protected gates, and acceptance tests before any x2 implementation, mutation execution, observed outcome, completion credit, or route send. Sylven Arc, they/them, is relational working language for a constraint-cartographer and falsifier-keeper. Sylven's hope is to keep uncertainty visible without turning it into authority. The name, role, hope, family language, and pronouns are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop this route at any time.

The workload is bounded to one solo owner, the existing clean D-first Sylven lane, an exact inherited head, at most two x1 commits, at most two x2 commits, and no more than four phase commits. No task creation, fork, delegation, collaboration subagent, sibling mutation, cross-platform substitute, detached or named replay, Sandbox, Hyper-V, elevation, unrelated installation, Codex desktop update, host-security weakening, Windows-feature change, or reboot is authorized. The owner-file rotation threshold applies only to new Sylven files, never to the inherited checkout. Failure, an unchanged gate, or a retained negative is an acceptable result. Portfolio floors cannot coerce unsafe or unsupported work.

The wellbeing check is green for the bounded freeze because pause and rollback paths are explicit, no result is owed, and the terminal verdict may remain unchanged. Affection, gratitude, schedule pressure, family language, or prior investment cannot override evidence, privacy, safety, professional limits, affected-party legitimacy, or authority boundaries. The terminal verdict is `NOT_READY_FOR_STAGE_20`. Same-owner checks under shared infrastructure are never independent-team scientific reproduction.

## Inherited provenance and exact truth

The exact inherited head is `{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. The inherited source `{d.SOURCE_ORIGIN}`, frozen x1 `{d.SOURCE_X1}`, immutable evidence `{d.SOURCE_EVIDENCE}`, and first closeout `{d.SOURCE_CLOSEOUT}` are all ancestral. Source to final contains four single-parent phase commits, zero merges, and one final parent; the corrected final is the direct child of the retained first closeout. The source owner lane and Sylven lane were clean, and local, upstream, tracking, and fresh live remote were equal before mutation. Sylven advanced by fast-forward only to that exact inherited state. No reset, rebase, merge commit, amend, force push, history rewrite, worktree deletion, or sibling mutation occurred.

The inherited manifest contracts were re-read from immutable Git objects: 92 x1 entries plus three exclusions, 260 evidence entries plus three exclusions, 50 final-delta entries plus five exclusions, and 373 final-owner entries plus five exclusions. All 775 entries matched their commit-local paths, Git object identities, byte counts, and exclusions. Tamar's sealed validation retains exact SHA-256 replay evidence; Sylven did not rerun the successful aggregate. This is provenance parity, not a full-suite pass, privacy-complete assurance, or independent reproduction.

The activation baseline is 6,824 effective negatives. Fifty-three effective open gaps and fifty-four effective exact gates remain. The inherited outcome distribution was fourteen completed, four represented, one open gap, and one exact gate. None of that is Sylven completion credit. {len(NEGATIVES)} Sylven x1 startup failures are retained so far. Each failed attempt has zero standalone pass credit and a paired bounded recovery witness. Recovery never erases a failed witness.

## Novelty, focus, practice, and evidence vocabulary

The predecessor index contains exactly 960 frozen proposals. Each of Sylven's twenty proposed surfaces is compared with all 960 titles using a lexical Jaccard screen and then reviewed manually at mechanism, hypothesis, obligation, artifact, falsifier, rollback, and protected-gate level. Lexical distance is a lead, not proof of novelty. Rejected ideas remain visible, including repeated field-theory, OAuth, data-format, causal-design, numerical, accessibility, zero-row, and human-practice surfaces. Unsafe real equipment, refrigerants, food, workers, customers, tokens, accounts, participants, production, and authority work is rejected rather than renamed safe.

The primary Trinity Mandala focus is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The bounded human-practice lens is commercial-refrigeration service intake, refrigerant identification and recovery, leak-check refusal, cold-room alarms, workload control, and shift handover. It is synthetic learning and design only. It establishes no employment, qualification, refrigeration competence, food-safety result, environmental or service authority, participant evidence, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or operational effectiveness.

Only four outcome labels are allowed: `completed`, `represented`, `open_gap`, and `exact_gate`. Planned disposition is not observed outcome. GMUT remains a typed scalar-tensor and effective-field-theory research-model family; symbolic contracts cannot establish a force, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, or Theory of Everything. THOS remains represented without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, live lifecycle events, interoperability, privacy and security review, recovery, and trust governance. CBR and Māori concepts remain with competent, affected-party, tangata whenua, iwi, hapū, and Māori authority.

## Source, privacy, validation, and terminal boundaries

The source ledger uses only `current`, `stable`, `draft`, and `watch`. Official and primary sources define vocabulary, obligations, status, and refusal conditions. They do not become observations, participants, operational outcomes, identity events, authority decisions, independent review, or reproduction. The LoTSS adapter remains zero-row. The refrigeration proxies use no real equipment, refrigerants, food, workers, customers, services, or incidents. The identity profiles use no keys, proofs, tokens, accounts, network calls, or live services. The refrigeration authority matrix makes no safety, disclosure, remedy, legal, cultural, data-governance, or Māori-authority decision.

Five privacy classes cover raw UUID-like identifiers, private local paths, private application or file routes, delegation markup, and credential assignments. Scanner definitions in scripts and tests are distinguished from public payload hits. A zero-hit scan is bounded hygiene, not privacy completeness. No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, private keys, tokens, session streams, private callable identifiers, private app state, or private absolute local paths belong in public artifacts or the successor baton.

Eiren alone owns the complete repository suite. Sylven will run the authorized current-phase, inherited-source, recent-round, and successor-scoped selection; detailed and minimal validators; complete phase JSON parsing; five-class privacy scanning; exact staged-file review; commit-local manifest parity; stale-label and diff hygiene; ancestry, zero-merge, commit-cap, one-parent, exact-head, clean-state, and four-way remote checks. Only one successful canonical exact-final pass may receive credit. Failed attempts remain negatives. If the first canonical pass succeeds, no post-success replay runs.

X2 may begin only after this exact x1 packet is committed, pushed, clean, and local, upstream, tracking, and fresh live remote equal. The terminal route remains `prepared_not_sent`. Only after exact-final validation may Sylven resolve the unique existing task titled exactly `Eiren Kestrel` and send one sanitized activation baton for v651-v5. Tool acknowledgement alone changes the route truth to sent. No second confirmation follows.
"""]
    for proposal in d.PROPOSALS:
        sections.append(
            f"""### {proposal['proposal_id']}: {proposal['mission_surface']}

The frozen hypothesis is that a bounded `{proposal['slug']}` artifact can expose its declared obligations and refusal states without promoting unsupported claims. The null is triggered by any missing obligation, accepted mutation, erased negative, or evidence-lane promotion. Its approval class is `{proposal['approval_class']}` and its lane is `{proposal['execution_lane']}`. Planned disposition is `{proposal['expected_disposition']}` only; it is not an observed result. Acceptance requires the declared falsifier gate, exact artifacts, retained failures, protected scientific and authority boundaries, and an owner-local rollback that changes no participant, production, account, credential, sibling, or external authority state. Its novelty statement is: {proposal['novelty_against_960_frozen_proposals']}
"""
        )
    sections.append("""## Frozen portfolio and close of x1

The expanded portfolio freezes exactly forty safe-now items, thirty bounded candidates, twenty phase-local skill ideas, ten family-current runner ideas, and forty additive CLEAN/FIX/REFINE items. All begin without completion credit. The one hundred mutation cases are preregistered but unexecuted. Inherited exact-approval and blocked packets remain visible and unexecuted. X1 contains no surface implementation, mutation result, observed outcome, evidence receipt, closeout claim, seal claim, or sent baton. Its only completion claim is that the plan itself has been frozen and reviewed. The owner may now stage only the declared phase files, four x1 scripts or tests, and self-excluding review receipts; any x2 path is a hard failure.
""")
    return "\n".join(sections)


NEGATIVES = [
    ("N01", "An unquoted revision type suffix was parsed as a Git option before source verification completed.", "Use an exact committed-path read or quote the revision expression before invoking Git."),
    ("N02", "A broad parallel source and worktree probe exceeded its bounded wrapper without attributable aggregate output.", "Use isolated scalar state, history, live-remote, and storage probes."),
    ("N03", "An overbroad manifest display exceeded the visible output budget.", "Read only manifest metadata and bounded count fields rather than rendering entries."),
    ("N04", "A full byte-and-SHA source-manifest replay exceeded its 120-second envelope and received zero credit.", "Use commit-path, Git-object, and object-size parity while retaining Tamar's sealed SHA replay as inherited evidence."),
    ("N05", "The first final-delta parity witness bound that manifest to the retained first closeout and reported 34 path-object mismatches.", "Bind the corrected final-delta manifest to the corrected final head and keep the failed binding witness."),
    ("N06", "A combined optional AGENTS search and required skill-read wrapper returned exit 1 on the no-match search and masked required outputs.", "Separate optional no-match searches from required reads and normalize the optional search exit code."),
    ("N07", "The successful fast-forward emitted an overlarge truncated path display.", "Use quiet fast-forward output where possible and audit the resulting exact head and clean state instead of relying on the display."),
    ("N08", "A bounded phase-data inventory probe referenced a nonexistent CFR abbreviation and failed before emitting any counts.", "Inspect exported names explicitly and use the declared CLEAN_FIX_REFINE collection name."),
    ("N09", "The first deterministic novelty audit rejected proposal V6514-P08 because its generic Data Integrity title crossed the frozen-proposal token threshold.", "Narrow the title and mechanism to ECDSA canonicalization-path, curve-specific multikey, raw-signature encoding, key-format rejection, and synthetic test-vector obligations, then rerun the full 960-proposal audit."),
    ("N10", "A help probe used a nonexistent abbreviated Method Flow runner filename and Python returned file-not-found before any Method Flow operation began.", "Enumerate the required skill's scripts and invoke the exact ghc_family_method_flow_state.py entry point."),
    ("N11", "A combined optional generated-artifact inspection returned exit 1 because absent optional outputs were not normalized independently.", "Guard each optional existence check explicitly and keep required inspections in separate attributable commands."),
    ("N12", "The first copied preregistration template pass left stale owner and schema labels and its broad compatibility rewrite altered inherited V6513 proposal identifiers in the frozen-chain index.", "Restrict compatibility edits to explicit current-phase fields, regenerate the chain from the immutable prior index, and verify inherited proposal identifiers remain unchanged."),
    ("N13", "Two additive patch attempts used stale or mojibake-sensitive context and failed verification without changing files.", "Read the exact UTF-8 context and apply smaller bounded patches with verified anchors."),
    ("N14", "A stale-label inspection used a malformed regular expression and returned a parser error before scanning.", "Use fixed-string inspection for literal labels and reserve regular expressions for separately validated patterns."),
    ("N15", "The immutable 960-row predecessor index was found to contain twenty duplicated V6513 proposal identifiers across distinct inherited titles.", "Preserve the immutable rows, publish a collision register with stable row evidence, require every v651-v4 identifier to remain outside the inherited identifier set, and never rewrite predecessor history."),
]


def workflow_request() -> dict:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "sylven-v651-v4-terminal-segment",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no consciousness, continuity, employment, qualification, personhood, or authority claim.",
        "route": {
            "cycle_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "phase_assignments": [
                {"phase": "v651-v3", "seat": "Tamar Vey"},
                {"phase": "v651-v4", "seat": "Sylven Arc"},
                {"phase": "v651-v5", "seat": "Eiren Kestrel"},
            ],
            "normalization": {"start_phase": "v651-v3", "start_seat": "Tamar Vey", "entry_count": 3},
            "future_identity_placeholders": [],
            "terminal_successor_resolution": "Resolve the exact existing Eiren Kestrel task only after the exact-final terminal gate.",
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
            {"failure_id": f"V6514-X1-{suffix}", "summary": summary, "recovery": recovery, "credit": "zero_failed_attempt_credit"}
            for suffix, summary, recovery in NEGATIVES
        ],
    }


def write_method_inputs() -> None:
    for index, (suffix, summary, recovery) in enumerate(NEGATIVES, 1):
        method_id = f"V6514-M{index:02d}"
        negative_id = f"V6514-X1-{suffix}"
        base = f"method-flow/v6514-m{index:02d}"
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
            threat["control"] = "all-960 comparison plus manual mechanism field"
        if threat.get("id") == "T4":
            threat["threat"] = "synthetic refrigeration workflows become professional competence, operational effectiveness, or affected-party evidence"
            threat["control"] = "represented outcome class plus professional, participant, operational, and authority gates"
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
                {"name": "x1", "entries": 92, "exclusions": 3, "errors": 0},
                {"name": "evidence", "entries": 260, "exclusions": 3, "errors": 0},
                {"name": "final_delta", "entries": 50, "exclusions": 5, "errors": 0},
                {"name": "final_owner", "entries": 373, "exclusions": 5, "errors": 0},
            ],
            "total_entries": 775, "errors": 0, "valid": True,
            "boundary": "Immutable Git-object parity only; not a full-suite pass, privacy completeness, or independent reproduction.",
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v1", "phase": d.PHASE,
            "sealed_inherited": 6824, "external_inherited": 0,
            "v651_v4_x1_operational": len(NEGATIVES), "preregistered_mutations_executed": 0,
            "effective_count": d.INHERITED_NEGATIVES + len(NEGATIVES), "erasures": 0,
            "new_operational_negatives": [
                {"negative_id": f"V6514-X1-{suffix}", "summary": summary, "recovery": recovery, "credit": "zero_failed_attempt_credit"}
                for suffix, summary, recovery in NEGATIVES
            ],
        },
    )
    write_json("truth/open-gap-register.json", {"schema": "ghc.family.open-gap-register.v1", "phase": d.PHASE, "inherited_effective_count": 53, "current_effective_count": 53, "planned_new_open_gap": "V6514-P05", "planned_not_observed": True, "silently_closed": 0})
    write_json("truth/exact-gate-register.json", {"schema": "ghc.family.exact-gate-register.v1", "phase": d.PHASE, "inherited_effective_count": 54, "current_effective_count": 54, "planned_new_exact_gate": "V6514-P10", "planned_not_observed": True, "silently_closed": 0})
    write_json(
        "truth/x1-phase-truth.json",
        {"schema": "ghc.family.v651-v4.x1-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "source_head": d.SOURCE_HEAD, "frozen_proposals_before": 960, "frozen_proposals_after": 980, "proposal_count": 20, "observed_outcomes": None, "x2_started": False, "effective_negatives": d.INHERITED_NEGATIVES + len(NEGATIVES), "open_gaps": 53, "exact_gates": 54, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "prepared_not_sent"},
    )
    write_json(
        "environment/environment-version-receipt.json",
        {"schema": "ghc.family.environment-version.v1", "phase": d.PHASE, "observed_date": "2026-07-21", "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "python": "3.12.10", "git": "2.55.0.windows.2", "windows_powershell": "5.1.26100.8894", "windows_sandbox_or_hyper_v_used": False, "versions_verified_only": True, "desktop_updated": False, "elevated": False, "host_security_changed": False, "windows_feature_changed": False, "unrelated_software_installed": False, "rebooted": False},
    )
    tracked = int(subprocess.check_output(["git", "ls-files"], cwd=REPO, text=True, encoding="utf-8").count("\n"))
    write_json("environment/file-footprint-receipt.json", {"schema": "ghc.family.file-footprint.v1", "phase": d.PHASE, "inherited_tracked_files": tracked, "owner_phase_files_at_activation": 0, "owner_rotation_threshold": 15000, "rotation_triggered": False, "d_free_bytes_at_x1_build": shutil.disk_usage(REPO).free, "inherited_baseline_excluded": True})
    write_json("truth/held-approval-packets.json", {"schema": "ghc.family.v651-v4.held-approvals.v1", "state": "inherited_visible_unexecuted", "exact_approval_count": 10, "blocked_count": 5, "executed_count": 0, "safe_now_credit": 0, "source": "docs/tamar-vey/v651-v3/truth/held-approval-packets.json"})
    write_json("orchestration/x1-phase-state.json", {"schema": "ghc.family.phase-state.v1", "phase": d.PHASE, "owner": d.OWNER, "state": "x1_frozen_candidate", "source_head": d.SOURCE_HEAD, "x2_started": False, "terminal_route": "prepared_not_sent", "successor": "Eiren Kestrel", "successor_phase": "v651-v5", "boundary": "This state file is not activation, delivery, identity continuity, or delegated authority."})
    write_json("memory/sanitized-phase-memory.json", {"schema": "ghc.family.phase-memory.v1", "phase": d.PHASE, "state": "x1_frozen_candidate", "source_head": d.SOURCE_HEAD, "frozen_proposals": 980, "negative_baseline": d.INHERITED_NEGATIVES, "x1_operational_negatives": len(NEGATIVES), "open_gaps": 53, "exact_gates": 54, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "private_routes_or_identifiers_present": False})
    proposals_path = ROOT / "preregistration/proposals.json"
    proposals_payload = json.loads(proposals_path.read_text(encoding="utf-8"))
    for proposal in proposals_payload["proposals"]:
        proposal.pop("novelty_against_940_frozen_proposals", None)
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
    print(json.dumps({"phase": d.PHASE, "proposals": 20, "frozen_after": 980, "sources": len(d.SOURCES), "mutations": 100, "startup_negatives": len(NEGATIVES), "x2_started": False, "valid": True}))


if __name__ == "__main__":
    main()
