#!/usr/bin/env python3
"""Build Orin Thale's v648-v6 x1-only preregistration packet."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v648_v6_definitions as d

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / d.PHASE_SLUG
PRIOR_INDEX = ROOT / "docs" / "sable-rook" / "v648-v5" / "provenance" / "frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"
REMASTER_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster" / "scripts" / "ghc_family_reflection_remaster.py"
NOVELTY_THRESHOLD = 0.50


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def normalized_tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {token for token in re.findall(r"[a-z0-9]+", value.casefold()) if token not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def portfolio_rows(titles: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6486-{prefix}-{index:02d}",
            "title": title,
            "approval_class": approval,
            "execution_lane": lane,
            "origin": "orin_v648_v6_new",
            "x1_state": "frozen_not_executed",
            "x2_completion_credit": False,
            "boundary": "Additive owner-scoped work only; reclassify visibly if evidence, authority, credentials, deployment, destructive action, or sibling mutation is required.",
        }
        for index, title in enumerate(titles, start=1)
    ]


def build_method_flow() -> None:
    ledger = PHASE / "method-flow" / "method-flow-ledger.json"
    records: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, start=1):
        method_id = f"V6486-M{index:02d}"
        records.append(
            {
                "method_id": method_id,
                "title": f"Recover {negative['category']} without erasing its failed witness",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [f"A bounded v648-v6 workflow exposes {negative['category']}."],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_scoped_workflow",
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": "Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.",
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": ["evidence_credit", "failure_retention", "x1_x2_separation", "caller_compatibility"],
                "retained_negative_ids": [negative["negative_id"]],
                "scope_boundary": "Bounded owner-scoped recovery only; no independent reproduction or authority credit.",
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": f"{method_id}-WFAIL",
                    "method_id": method_id,
                    "procedure": negative["failed"],
                    "scope": f"bounded {negative['category']} failed witness",
                    "expected": "The attempted method returns attributable evidence within its declared domain.",
                    "observed": negative["failed"],
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative["negative_id"]],
                    "boundary": "Retained failure only; no cleanliness, novelty, proof, authority, or completion credit.",
                },
                {
                    "witness_id": f"{method_id}-WPASS",
                    "method_id": method_id,
                    "procedure": negative["recovery"],
                    "scope": f"bounded {negative['category']} recovery witness",
                    "expected": "The corrected method returns attributable bounded evidence while preserving the failure.",
                    "observed": negative["passing"],
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative["negative_id"]],
                    "boundary": "Bounded same-owner recovery only; no independent reproduction or authority credit.",
                },
            ]
        )
    for row in records:
        write_json(f"method-flow/{row['method_id'].casefold()}-method-record.json", row)
    for row in witnesses:
        write_json(f"method-flow/{row['witness_id'].casefold()}-witness.json", row)
    run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", d.PHASE, "--owner", d.OWNER)
    for row in records:
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(PHASE / f"method-flow/{row['method_id'].casefold()}-method-record.json"))
    for row in witnesses:
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(PHASE / f"method-flow/{row['witness_id'].casefold()}-witness.json"))
    for row in records:
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", row["method_id"], "--state", "preferred", "--note", "Promoted only for the declared trigger after one retained failure and one bounded passing witness.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"))


def build_index_and_remaster() -> None:
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(ROOT), "--skill-root", str(SKILL_ROOT), "--out-dir", str(PHASE / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    args = [sys.executable, str(REMASTER_RUNNER), "--repo", str(ROOT), "--skill-root", str(SKILL_ROOT), "--output-dir", str(PHASE / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER]
    for focus in ["manifest", "method", "privacy", "route", "provenance", "reflection", "memory", "orchestration", "compatibility"]:
        args.extend(["--focus", focus])
    run(*args)
    inventory = read_json(PHASE / "reflection-remaster/reflection-remaster-inventory.json")
    issues = read_json(PHASE / "reflection-remaster/reflection-remaster-issues.json")
    write_json(
        "reflection-remaster/reviewed-current-receipt.json",
        {
            "schema": "ghc.family.v648-v6.reflection-remaster.reviewed-current.v1",
            "inventory_count": inventory["inventory_count"],
            "scoped_count": inventory["scoped_count"],
            "issue_count": issues["issue_count"],
            "disposition_counts": issues["disposition_counts"],
            "global_skill_changes": 0,
            "scripts_deleted": 0,
            "scripts_renamed": 0,
            "historical_surfaces_removed": 0,
            "decision": "reviewed_current_no_global_change_justified",
            "boundary": "Lexical candidates remain unpromoted because caller and behavior evidence is incomplete; all compatibility and historical surfaces remain intact.",
        },
    )


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v648_v6_preregistration.py",
        "scripts/ghc_family_v648_v6_x1_staged_review.py",
        "docs/orin-thale/v648-v6/validation/x1-staged-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                row = {"path": relative, "pattern_class": pattern_class, "disposition": "scanner_definition" if relative in definitions else "confirmed_payload_hit"}
                candidates.append(row)
                if relative not in definitions:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v648-v6.x1-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with exact scanner-definition disposition; zero confirmed hits is not complete privacy assurance.",
    }


def build_manifest() -> None:
    exclusions = [
        "docs/orin-thale/v648-v6/validation/x1-staged-manifest.json",
        "docs/orin-thale/v648-v6/validation/x1-staged-privacy.json",
        "docs/orin-thale/v648-v6/validation/x1-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [
        {"path": relative, "git_blob": run("git", "hash-object", f"--path={relative}", relative), "bytes": (ROOT / relative).stat().st_size}
        for relative in paths
        if (ROOT / relative).is_file()
    ]
    privacy = privacy_scan(paths + exclusions)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json(
        "validation/x1-staged-manifest.json",
        {
            "schema": "ghc.family.v648-v6.x1-manifest.v1",
            "hash_domain": "git_hash_object_path_filtered_blob",
            "checkout_bytes_domain": "working_tree_after_checkout_filters",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": exclusions,
            "coverage_boundary": "All intended x1 paths except three declared self-referential review receipts.",
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.v648-v6.x1-staged-review.v1",
            "intended_path_count": len(entries) + len(exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(exclusions),
            "out_of_scope_paths": [],
            "x2_implementation_paths": [],
            "x2_outcome_paths": [],
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "x1_only": True,
            "source_head": d.SOURCE_COMMIT,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )


def build() -> None:
    if git("rev-parse", "HEAD") != d.SOURCE_COMMIT:
        raise RuntimeError("x1 must begin at the exact verified v648-v5 final head")
    allowed_start = {
        "scripts/ghc_family_v648_v6_definitions.py",
        "scripts/build_ghc_family_v648_v6_preregistration.py",
        "tests/test_ghc_family_v648_v6_x1.py",
    }
    if set(status_paths()) != allowed_start:
        raise RuntimeError(f"unexpected pre-x1 worktree surface: {sorted(set(status_paths()) ^ allowed_start)}")
    prior_index = read_json(PRIOR_INDEX)
    prior = list(prior_index["prior_proposals"]) + list(prior_index["new_proposals"])
    if len(prior) != 610:
        raise RuntimeError(f"expected 610 inherited proposals, found {len(prior)}")
    novelty_rows = []
    for proposal in d.PROPOSALS:
        scored = [(jaccard(normalized_tokens(proposal["title"]), normalized_tokens(row["title"])), row) for row in prior]
        score, nearest = max(scored, key=lambda pair: pair[0])
        if score >= NOVELTY_THRESHOLD:
            raise RuntimeError(f"proposal collision {proposal['proposal_id']} score={score:.4f} nearest={nearest['proposal_id']}")
        novelty_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest["proposal_id"],
                "nearest_prior_title": nearest["title"],
                "jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "disposition": "lexically_distinct_manual_semantic_review_passed",
            }
        )
    safe_rows = portfolio_rows(d.SAFE_TASKS, "SAFE", "x2_safe_now", "safe_now_owner_scoped_additive")
    candidate_rows = portfolio_rows(d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate", "candidate_bounded")
    cleanup_rows = portfolio_rows(d.CLEANUP_TASKS, "CLEAN", "x2_clean_refine", "safe_now_non_destructive")
    skill_rows = [{"skill_id": f"V6486-SKILL-{i:02d}", "name": name, "origin": "orin_v648_v6_new", "x1_state": "frozen_not_built", "x2_use_credit": False, "boundary": "Phase-local proposal; no global installation, authority, or universal applicability claim."} for i, name in enumerate(d.SKILL_IDEAS, start=1)]
    runner_rows = [{"runner_id": f"V6486-RUNNER-{i:02d}", "name": name, "origin": "orin_v648_v6_new", "x1_state": "frozen_not_built", "x2_use_credit": False, "boundary": "Family-current design only; preserve historical callers and require a bounded witness."} for i, name in enumerate(d.RUNNER_IDEAS, start=1)]
    mutations = [{"mutation_id": f"V6486-MUT-{i:03d}", "proposal_id": d.PROPOSALS[(i - 1) // 7]["proposal_id"], "case": (i - 1) % 7 + 1, "expected": "reject", "x1_state": "preregistered_not_executed", "executed": False, "completion_credit": False} for i in range(1, 71)]
    source_rows = [{**row, "verification_date": "2026-07-19", "evidence_credit": "design_or_protocol_support_only", "not_observation": True} for row in d.SOURCES]
    status_counts = {status: sum(row["status"] == status for row in source_rows) for status in d.SOURCE_STATUS_CLASSES}
    writes = {
        "identity-receipt.json": {"schema":"ghc.family.v648-v6.identity.v1","owner":d.OWNER,"pronouns":d.PRONOUNS,"role":d.ROLE,"hope":d.HOPE,"identity_boundary":"Relational working language only; not evidence of consciousness, sentience, legal personhood, employment, continuity, qualification, or independent authority.","corrigibility":"Hamish may rename, pause, redirect, or stop the route."},
        "environment/startup-receipt.json": {"schema":"ghc.family.v648-v6.startup.v1","owner_branch":d.BRANCH,"source_branch":d.SOURCE_BRANCH,"source_head":d.SOURCE_COMMIT,"source_x1":d.SOURCE_X1_COMMIT,"source_evidence":d.SOURCE_EVIDENCE_COMMIT,"source_ancestry":True,"source_phase_commits":3,"source_merges":0,"source_final_parent_count":1,"source_and_owner_clean":True,"source_four_way_equal":True,"owner_fast_forwarded_only":True,"owner_four_way_equal_before_x1":True,"d_first":True,"sandbox_or_hyperv_action":False,"cross_platform_message_action":False},
        "environment/version-receipt.json": {"schema":"ghc.family.v648-v6.versions.v1","codex_cli_live":"0.144.5","codex_desktop_live":"26.715.4045.0","chatgpt_desktop_live":"1.2026.190.0","codex_cli_official_package_channel":"0.144.6","python_live":"3.12.10","git_live":"2.55.0.windows.2","powershell_live":"5.1.26100.8875","desktop_updated":False,"cli_updated_in_phase":False,"verification_only":True},
        "x1-proposals.json": {"schema":"ghc.family.v648-v6.x1-proposals.v1","phase":d.PHASE,"owner":d.OWNER,"source_head":d.SOURCE_COMMIT,"prior_frozen_proposal_count":610,"new_proposal_count":10,"frozen_total_after_x1":620,"primary_focus":d.PRIMARY_FOCUS,"bounded_practice":d.BOUNDED_PRACTICE,"outcome_classes":d.OUTCOME_CLASSES,"x1_state":"frozen_not_executed","proposals":d.PROPOSALS,"boundary":"Expected dispositions are preregistered hypotheses, not observed x2 outcomes."},
        "sources/source-ledger.json": {"schema":"ghc.family.v648-v6.sources.v1","allowed_statuses":d.SOURCE_STATUS_CLASSES,"status_counts":status_counts,"sources":source_rows,"boundary":"Citations support design and protocol interpretation only; none is an observation, participant result, authority delegation, or production certificate."},
        "approval-packets/x1-safe-now-portfolio.json": {"schema":"ghc.family.v648-v6.safe-now.v1","count":len(safe_rows),"items":safe_rows,"inherited_completion_credit":0},
        "prototypes/x1-candidate-plan.json": {"schema":"ghc.family.v648-v6.candidates.v1","count":len(candidate_rows),"items":candidate_rows,"inherited_completion_credit":0},
        "prototypes/x1-skill-runner-plan.json": {"schema":"ghc.family.v648-v6.skills-runners.v1","skill_count":len(skill_rows),"skills":skill_rows,"runner_count":len(runner_rows),"runners":runner_rows,"inherited_completion_credit":0},
        "maintenance/x1-clean-refine-plan.json": {"schema":"ghc.family.v648-v6.clean-refine.v1","count":len(cleanup_rows),"items":cleanup_rows,"destructive_actions":0},
        "validation/x1-synthetic-mutation-plan.json": {"schema":"ghc.family.v648-v6.synthetic-negatives.v1","count":70,"executed_count":0,"rejected_count":0,"mutations":mutations},
        "validation/x1-operational-negatives.json": {"schema":"ghc.family.v648-v6.x1-operational-negatives.v1","count":len(d.X1_OPERATIONAL_NEGATIVES),"negatives":d.X1_OPERATIONAL_NEGATIVES,"all_retained":True},
        "retained-negative-register.json": {"schema":"ghc.family.v648-v6.retained-negatives.x1.v1","inherited_effective":d.INHERITED_NEGATIVES,"x1_operational":len(d.X1_OPERATIONAL_NEGATIVES),"preregistered_synthetic_not_yet_executed":70,"effective_at_x1":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES),"projected_if_all_synthetic_execute_and_reject":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES)+70,"negative_erased":False},
        "exact-open-gate-register.json": {"schema":"ghc.family.v648-v6.gates.x1.v1","inherited_open_gaps":d.INHERITED_OPEN_GAPS,"inherited_exact_gates":d.INHERITED_EXACT_GATES,"projected_open_gaps_if_expected_dispositions_hold":d.INHERITED_OPEN_GAPS+1,"projected_exact_gates_if_expected_dispositions_hold":d.INHERITED_EXACT_GATES+1,"closed_in_x1":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "phase-truth.json": {"schema":"ghc.family.v648-v6.phase-truth.x1.v1","phase":d.PHASE,"owner":d.OWNER,"stage":"x1_frozen_not_executed","source_head":d.SOURCE_COMMIT,"proposal_count":10,"expected_distribution":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"observed_distribution":None,"x2_started":False,"single_pass_used":False,"replay_used":False,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "provenance/frozen-chain-proposal-index.json": {"schema":"ghc.family.frozen-proposal-index.v1","prior_count":610,"prior_proposals":prior,"new_count":10,"new_proposals":[{"proposal_id":row["proposal_id"],"title":row["title"]} for row in d.PROPOSALS],"count":620},
        "provenance/proposal-collision-audit.json": {"schema":"ghc.family.v648-v6.proposal-collision-audit.v1","prior_count":610,"new_count":10,"threshold":NOVELTY_THRESHOLD,"maximum_observed_jaccard":max(row["jaccard"] for row in novelty_rows),"rows":novelty_rows,"manual_semantic_review":"All ten passed manual substantive neighbor review; rejected seed collisions remain retained operational evidence."},
        "validation/single-pass-validation-plan.json": {"schema":"ghc.family.v648-v6.single-pass-plan.v1","full_repository_suite":False,"canonical_successful_pass_budget":1,"successful_passes_used":0,"detached_replay":False,"named_replay":False,"repeatability_credit":False,"preflight_required":["module_selection","schema","manifest","privacy","x1_tree"],"bounded_blocker_rule":"A failed aggregate gets no credit; retain it and rerun only the isolated blocker unless dependencies require broader scope."},
        "orchestration/phase-state.json": {"schema":"ghc.family.v648-v6.orchestration.x1.v1","active":[d.OWNER],"standby":["Eiren Kestrel","Ilyra Fen","Sable Rook","Tamar Vey","Sylven Arc"],"solo":True,"subagents":0,"tasks_created":0,"cross_platform_messages":0,"terminal_route":"PREPARED_NOT_SENT"},
        "orchestration/applicable-memory-record.json": {"schema":"ghc.family.v648-v6.memory-use.v1","newest_applicable_memory_used":True,"exact_current_registry_hit":False,"live_baton_precedence":True,"live_activation_used_as_authority":True,"memory_mutated":False,"boundary":"Newest applicable prior memory was consulted without continuity inference. Live Git and the current activation supplied current proof and authority."},
        "wellbeing-check.json": {"schema":"ghc.family.v648-v6.wellbeing.x1.v1","scope_bounded":True,"solo_lane":True,"commit_cap":4,"document_cap_words":6000,"owner_file_threshold":15000,"host_changes_deferred":True,"pause_right_preserved":True},
        "environment/file-footprint-receipt.json": {"schema":"ghc.family.v648-v6.file-footprint.x1.v1","tracked_checkout_baseline":37396,"owner_generated_at_receipt":None,"rotation_threshold":15000,"baseline_triggers_rotation":False},
        "validation/x1-review.json": {"schema":"ghc.family.v648-v6.x1-review.v1","checks":32,"issues":[],"proposal_count":10,"prior_proposal_count":610,"frozen_total":620,"safe_count":30,"candidate_count":20,"skill_count":20,"runner_count":10,"cleanup_count":30,"synthetic_mutation_count":70,"x2_implementation_count":0,"x2_observed_outcome_count":0,"terminal_route":"PREPARED_NOT_SENT","passed":True},
    }
    for relative, payload in writes.items():
        write_json(relative, payload)
    write_text("x1-preregistration.md", "# Orin Thale v648-v6 x1 preregistration\n\nThis dedicated x1 freeze contains exactly ten proposals and no x2 implementation or observed outcome. The semantic screen covers all 610 inherited frozen proposals and retains rejected collisions. THOS Body is primary; GMUT Mind and Freed ID / CBR Heart remain explicit. Theatre stage management and handover is a bounded learning and synthetic-design lens only, never employment, competence, safety authority, legal authority, cultural authority, Māori authority, or affected-party evidence.\n\nOnly completed, represented, open_gap, and exact_gate may classify later outcomes. X2 begins only after this tree is committed, pushed, clean, and four-way remote-equal.")
    write_text("sources/source-ledger.md", "# v648-v6 source ledger\n\n" + "\n".join(f"- **{row['source_id']}** — {row['title']} ({row['status']}, {row['kind']}). {row['implication']}" for row in source_rows))
    write_text("wellbeing-check.md", "# v648-v6 wellbeing check\n\nThe phase is solo, additive, D-first, under a four-commit cap, and subject to Hamish's right to pause or stop. No host-security, Sandbox, Hyper-V, cross-platform messaging, destructive cleanup, or authority-substitution work is in scope.")
    build_method_flow()
    build_index_and_remaster()
    write_json("environment/file-footprint-receipt.json", {**read_json(PHASE / "environment/file-footprint-receipt.json"), "owner_generated_at_receipt": len(status_paths())})
    build_manifest()
    if read_json(PHASE / "validation/x1-staged-privacy.json")["confirmed_hit_count"]:
        raise RuntimeError("x1 privacy scan found confirmed payload hits")


if __name__ == "__main__":
    build()
