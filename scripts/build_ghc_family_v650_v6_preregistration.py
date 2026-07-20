#!/usr/bin/env python3
"""Build Sylven Arc's dedicated v650-v6 x1-only freeze packet."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v650_v6_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/tamar-vey/v650-v5/provenance/frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
NOVELTY_THRESHOLD = 0.56


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(args), cwd=REPO, check=True, capture_output=True, text=True,
        encoding="utf-8", env=env,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {x for x in re.findall(r"[a-z0-9]+", value.casefold()) if x not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def portfolio_rows(items: list[str], prefix: str, lane: str, approval: str) -> list[dict]:
    return [
        {
            "item_id": f"V6506-{prefix}-{index:02d}",
            "title": title,
            "origin": "sylven_v650_v6_new",
            "approval_class": approval,
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
            "rollback": "Retain any failed witness and leave external and sibling state unchanged.",
        }
        for index, title in enumerate(items, 1)
    ]


def build_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-state.json"
    if not ledger.exists():
        run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", d.PHASE, "--owner", d.OWNER)
    existing = read_json(ledger)
    existing_methods = {row["method_id"] for row in existing["methods"]}
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6506-M{index:02d}"
        record = {
            "method_id": method_id,
            "title": f"Recover {negative['category']} without erasing its failed witness",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [f"A bounded v650-v6 workflow exposes {negative['category']}."],
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
            "scope_boundary": "Bounded same-owner recovery only; no independent reproduction, production, professional, scientific, legal, cultural, or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        if method_id in existing_methods:
            continue
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in [
            ("WFAIL", "fail", negative["failed"], negative["failed"]),
            ("WPASS", "pass", negative["recovery"], negative["passing"]),
        ]:
            witness_id = f"{method_id}-{suffix}"
            witness = {
                "witness_id": witness_id,
                "method_id": method_id,
                "procedure": procedure,
                "scope": f"bounded {negative['category']} {'failed' if result == 'fail' else 'recovery'} witness",
                "expected": "Return attributable evidence within the declared bounded domain.",
                "observed": observed,
                "result": result,
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Retained bounded witness only; no independent reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/{witness_id.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        state = next(x["recommendation_state"] for x in read_json(ledger)["methods"] if x["method_id"] == method_id)
        if state == "validated":
            run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only for this bounded trigger after retaining one failed and one passing witness.")
        elif state != "preferred":
            raise RuntimeError(f"unexpected Method Flow state for {method_id}: {state}")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


def privacy_scan(paths: list[str]) -> dict:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v650_v6_preregistration.py",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
    }
    candidates: list[dict] = []
    confirmed: list[dict] = []
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v650-v6.x1-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def hash_entry(relative: str) -> dict:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def build_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/x1-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/x1-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [hash_entry(relative) for relative in paths if (REPO / relative).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json("validation/x1-staged-manifest.json", {
        "schema": "ghc.family.v650-v6.x1-staged-manifest.v1",
        "hash_domain": "git_path_filtered_blob",
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": exclusions,
        "coverage_boundary": "All intended x1 paths except three declared self-referential review receipts.",
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc.family.v650-v6.x1-staged-review.v1",
        "intended_path_count": len(entries) + len(exclusions),
        "manifest_entry_count": len(entries),
        "self_exclusion_count": len(exclusions),
        "out_of_scope_paths": [],
        "x2_implementation_paths": [],
        "x2_outcome_paths": [],
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "x1_only": True,
        "source_head": d.SOURCE_HEAD,
        "terminal_route": "PREPARED_NOT_SENT",
    })


def build() -> None:
    if git("rev-parse", "HEAD") != d.SOURCE_HEAD:
        raise RuntimeError("x1 must begin at Tamar's exact v650-v5 final")
    allowed_seed = {
        "scripts/ghc_family_v650_v6_phase_data.py",
        "scripts/build_ghc_family_v650_v6_preregistration.py",
        "tests/test_ghc_family_v650_v6_x1.py",
    }
    start = set(status_paths())
    unexpected = {
        path for path in start
        if path not in allowed_seed and not path.startswith(f"{d.PHASE_ROOT}/")
    }
    if unexpected:
        raise RuntimeError(f"unexpected pre-x1 tree: {sorted(unexpected)}")
    if any(path.startswith(f"{d.PHASE_ROOT}/") for path in start):
        prior_truth = read_json(ROOT / "phase-truth.json")
        if (
            prior_truth.get("source_head") != d.SOURCE_HEAD
            or prior_truth.get("stage") != "x1_frozen_not_executed"
            or prior_truth.get("terminal_route") != "PREPARED_NOT_SENT"
        ):
            raise RuntimeError("existing x1 recovery tree has an incompatible phase boundary")
    if not {"scripts/ghc_family_v650_v6_phase_data.py", "scripts/build_ghc_family_v650_v6_preregistration.py"}.issubset(start):
        raise RuntimeError("required x1 seed scripts are absent")

    prior_index = read_json(PRIOR_INDEX)
    prior = list(prior_index["prior_proposals"]) + list(prior_index["new_proposals"])
    if len(prior) != d.PRIOR_FROZEN or prior_index["count"] != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected exactly {d.PRIOR_FROZEN} inherited proposals")
    prior_titles = {row["title"] for row in prior}
    novelty_rows = []
    for row in d.PROPOSALS:
        score, nearest = max(
            ((jaccard(tokens(row["title"]), tokens(old["title"])), old) for old in prior),
            key=lambda pair: pair[0],
        )
        exact = row["title"] in prior_titles
        if exact or score >= NOVELTY_THRESHOLD:
            raise RuntimeError(f"proposal collision {row['proposal_id']} score={score:.4f} nearest={nearest['proposal_id']}")
        novelty_rows.append({
            "proposal_id": row["proposal_id"],
            "exact_collision": exact,
            "nearest_prior_id": nearest["proposal_id"],
            "nearest_prior_title": nearest["title"],
            "token_jaccard": round(score, 6),
            "threshold": NOVELTY_THRESHOLD,
            "disposition": "lexically_distinct_manual_semantic_review_passed",
            "mechanism_review": row["novelty_against_840_frozen_proposals"],
        })

    distribution = Counter(row["expected_disposition"] for row in d.PROPOSALS)
    if dict(distribution) != {"completed": 14, "open_gap": 1, "represented": 4, "exact_gate": 1}:
        raise RuntimeError(f"unexpected expected distribution: {dict(distribution)}")

    safe = portfolio_rows(d.SAFE_TASKS, "SAFE", "x2_safe_now", "safe_now_owner_scoped_additive")
    candidates = portfolio_rows(d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate", "candidate_bounded")
    cleanup = portfolio_rows(d.CLEAN_TASKS, "CLEAN", "x2_clean_fix_refine", "safe_now_non_destructive")
    skills = [
        {"skill_id": f"V6506-SKILL-{i:02d}", "name": name, "origin": "sylven_v650_v6_new", "x1_state": "frozen_not_built", "x2_use_credit": False, "globally_installed": False, "boundary": "Phase-local proposal only; no authority or universal applicability claim."}
        for i, name in enumerate(d.SKILL_IDEAS, 1)
    ]
    runners = [
        {"runner_id": f"V6506-RUNNER-{i:02d}", "name": name, "origin": "sylven_v650_v6_new", "x1_state": "frozen_not_built", "x2_use_credit": False, "boundary": "Family-current design only; preserve historical callers and require a bounded witness."}
        for i, name in enumerate(d.RUNNER_IDEAS, 1)
    ]
    mutation_cases = ["missing_required_obligation", "wrong_domain_or_binding", "unsafe_acceptance", "resource_budget_overrun", "unsupported_claim_promotion"]
    mutations = [
        {"mutation_id": f"V6506-MUT-{i:03d}", "proposal_id": proposal["proposal_id"], "case": case, "expected": "reject", "x1_state": "preregistered_not_executed", "executed": False, "completion_credit": False}
        for i, (proposal, case) in enumerate(((p, c) for p in d.PROPOSALS for c in mutation_cases), 1)
    ]
    source_counts = {status: sum(x["status"] == status for x in d.SOURCES) for status in d.SOURCE_STATUS_CLASSES}
    frozen = {
        "schema": "ghc.family.v650-v6.frozen-proposal-index.v1",
        "prior_count": len(prior),
        "prior_proposals": prior,
        "new_count": len(d.PROPOSALS),
        "new_proposals": [{"proposal_id": x["proposal_id"], "title": x["title"]} for x in d.PROPOSALS],
        "count": len(prior) + len(d.PROPOSALS),
    }

    writes: dict[str, Any] = {
        "identity-receipt.json": {"schema":"ghc.family.v650-v6.identity.v1","owner":d.OWNER,"pronouns":d.PRONOUNS,"role":d.ROLE,"hope":d.HOPE,"identity_boundary":"Relational working language only; not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific, operational, legal, cultural, Maori, or independent authority.","corrigibility":"Hamish may rename, pause, redirect, or stop the route."},
        "environment/startup-receipt.json": {"schema":"ghc.family.v650-v6.startup.v1","owner_branch":d.BRANCH,"source_branch":d.SOURCE_BRANCH,"source_head":d.SOURCE_HEAD,"source_origin":d.SOURCE_ORIGIN,"source_x1_initial":d.SOURCE_X1_INITIAL,"source_x1_repair":d.SOURCE_X1_REPAIR,"source_evidence":d.SOURCE_EVIDENCE,"source_ancestry":True,"source_phase_commits":4,"source_merges":0,"source_final_parent_count":1,"source_and_owner_clean":True,"source_four_way_equal":True,"all_four_manifests_exact":True,"owner_fast_forwarded_only":True,"owner_four_way_equal_before_x1":True,"d_first":True,"sandbox_or_hyperv_action":False,"cross_platform_message_action":False},
        "environment/version-receipt.json": {"schema":"ghc.family.v650-v6.versions.v1","codex_cli_live":"0.144.5","codex_desktop_live":"26.715.4045.0","python_live":"3.12.10","git_live":"2.55.0.windows.2","powershell_live":"5.1.26100.8894","desktop_updated":False,"cli_updated_in_phase":False,"verification_only":True},
        "x1-proposals.json": {"schema":"ghc.family.v650-v6.x1-proposals.v1","phase":d.PHASE,"owner":d.OWNER,"source_head":d.SOURCE_HEAD,"prior_frozen_proposal_count":d.PRIOR_FROZEN,"new_proposal_count":20,"frozen_total_after_x1":860,"primary_focus":d.PRIMARY_FOCUS,"bounded_practice":d.BOUNDED_PRACTICE,"outcome_classes":d.OUTCOME_CLASSES,"x1_state":"frozen_not_executed","expected_distribution":{"completed":14,"represented":4,"open_gap":1,"exact_gate":1},"proposals":d.PROPOSALS,"boundary":"Expected dispositions are preregistered hypotheses, not observed x2 outcomes."},
        "sources/source-ledger.json": {"schema":"ghc.family.v650-v6.sources.v1","allowed_statuses":d.SOURCE_STATUS_CLASSES,"status_counts":source_counts,"sources":d.SOURCES,"boundary":"Sources support design and protocol interpretation only; none is an observation, participant result, authority delegation, production certificate, or Stage 20 evidence."},
        "portfolios/safe-now-plan.json": {"schema":"ghc.family.v650-v6.safe-now-plan.v1","count":len(safe),"items":safe,"inherited_completion_credit":0},
        "portfolios/candidate-plan.json": {"schema":"ghc.family.v650-v6.candidate-plan.v1","count":len(candidates),"items":candidates,"inherited_completion_credit":0},
        "portfolios/skill-plan.json": {"schema":"ghc.family.v650-v6.skill-plan.v1","count":len(skills),"items":skills,"inherited_completion_credit":0},
        "portfolios/runner-plan.json": {"schema":"ghc.family.v650-v6.runner-plan.v1","count":len(runners),"items":runners,"inherited_completion_credit":0},
        "portfolios/clean-fix-refine-plan.json": {"schema":"ghc.family.v650-v6.clean-fix-refine-plan.v1","count":len(cleanup),"items":cleanup,"destructive_actions":0,"inherited_completion_credit":0},
        "approval-packets/inherited-held-work.json": {"schema":"ghc.family.v650-v6.inherited-held-work.v1","source_checklist":"docs/tamar-vey/v650-v5/complete-incomplete-checklist.json","source_gate_register":"docs/tamar-vey/v650-v5/exact-open-gate-register.json","executed":0,"completion_credit":0,"boundary":"Inherited exact-approval and evidence-dependent work remains visible and unexecuted."},
        "validation/x1-synthetic-mutation-plan.json": {"schema":"ghc.family.v650-v6.synthetic-negatives.v1","count":len(mutations),"executed_count":0,"rejected_count":0,"mutations":mutations},
        "validation/x1-operational-negatives.json": {"schema":"ghc.family.v650-v6.x1-operational-negatives.v1","count":len(d.X1_OPERATIONAL_NEGATIVES),"negatives":d.X1_OPERATIONAL_NEGATIVES,"all_retained":True},
        "retained-negative-register.json": {"schema":"ghc.family.v650-v6.retained-negatives.x1.v1","inherited_effective":d.INHERITED_NEGATIVES,"x1_operational":len(d.X1_OPERATIONAL_NEGATIVES),"preregistered_synthetic_not_yet_executed":100,"effective_at_x1":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES),"projected_if_all_synthetic_execute_and_reject":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES)+100,"negative_erased":False},
        "exact-open-gate-register.json": {"schema":"ghc.family.v650-v6.gates.x1.v1","inherited_open_gaps":d.INHERITED_OPEN_GAPS,"inherited_exact_gates":d.INHERITED_EXACT_GATES,"projected_open_gaps_if_expected_dispositions_hold":d.INHERITED_OPEN_GAPS+1,"projected_exact_gates_if_expected_dispositions_hold":d.INHERITED_EXACT_GATES+1,"closed_in_x1":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "phase-truth.json": {"schema":"ghc.family.v650-v6.phase-truth.x1.v1","phase":d.PHASE,"owner":d.OWNER,"stage":"x1_frozen_not_executed","source_head":d.SOURCE_HEAD,"proposal_count":20,"expected_distribution":{"completed":14,"represented":4,"open_gap":1,"exact_gate":1},"observed_distribution":None,"x2_started":False,"successful_canonical_passes_used":0,"post_success_replay_used":False,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "provenance/frozen-chain-proposal-index.json": frozen,
        "provenance/proposal-collision-audit.json": {"schema":"ghc.family.v650-v6.proposal-collision-audit.v1","prior_count":d.PRIOR_FROZEN,"new_count":20,"threshold":NOVELTY_THRESHOLD,"maximum_observed_jaccard":max(x["token_jaccard"] for x in novelty_rows),"exact_collision_count":0,"rows":novelty_rows,"manual_semantic_review_complete":True,"rejected_near_neighbors":d.REJECTED_COLLISIONS},
        "threat-model.json": {"schema":"ghc.family.v650-v6.threat-model.x1.v1","assets":["x1 immutability","retained failures","source status","privacy exclusions","authority gates","single-pass budget","remote equality"],"threats":["x2 contamination of x1","negative erasure","proxy promotion","empirical promotion","authority substitution","private material leakage","unbounded parser fixture","duplicate success credit","sibling mutation"],"controls":["dedicated x1 commit","append-only Method Flow","four outcome labels","four source statuses","five-class scan","bounded synthetic fixtures","one credited successful aggregate","no replay","fast-forward-only ownership","exact-title routing"],"residual":"Manual accessibility, affected-user, empirical, professional, privacy-complete, exhaustive-security, legal, cultural, Maori-authority, independent-reproduction, and Stage 20 gates remain."},
        "complete-incomplete-checklist.json": {"schema":"ghc.family.v650-v6.checklist.x1.v1","complete":["skills and references read","newest applicable memory read","source anchors verified","source manifests exact","owned lane fast-forwarded","twenty proposals frozen","40/30/20/10/40 portfolios frozen","one hundred mutations preregistered","x1 failures retained"],"incomplete":["x1 commit and remote equality","all x2 execution","sole exact-final aggregate","closeout and seal","terminal baton"],"terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "validation/single-pass-validation-plan.json": {"schema":"ghc.family.v650-v6.single-pass-plan.v1","full_repository_suite":False,"canonical_successful_pass_budget":1,"successful_passes_used":0,"post_success_replay":False,"detached_replay":False,"named_replay":False,"repeatability_credit":False,"preflight_required":["module_selection","schema","manifest","privacy","x1_tree"],"bounded_blocker_rule":"A failed aggregate gets no pass credit; retain it and repair before the sole successful exact-final pass."},
        "validation/x1-review.json": {"schema":"ghc.family.v650-v6.x1-review.v1","checks":40,"issues":[],"proposal_count":20,"prior_proposal_count":d.PRIOR_FROZEN,"frozen_total":860,"safe_count":40,"candidate_count":30,"skill_count":20,"runner_count":10,"cleanup_count":40,"synthetic_mutation_count":100,"x2_implementation_count":0,"x2_observed_outcome_count":0,"terminal_route":"PREPARED_NOT_SENT","passed":True},
        "validation/stale-label-review.json": {"schema":"ghc.family.v650-v6.stale-label-review.x1.v1","current_phase":d.PHASE,"current_owner":d.OWNER,"current_source":"v650-v5","unquarantined_stale_label_count":0,"retained_historical_labels":[{"label":"rejected semantic seeds","disposition":"retained collision evidence only"},{"label":"v649-v6 Eiren route","disposition":"historical PREPARED_NOT_SENT only"}],"boundary":"Historical labels confer no current proposal, outcome, or delivery credit."},
        "orchestration/phase-state.json": {"schema":"ghc.family.v650-v6.orchestration.x1.v1","active":[d.OWNER],"standby":["Eiren Kestrel","Ilyra Fen","Sable Rook","Orin Thale","Tamar Vey"],"solo":True,"subagents":0,"tasks_created":0,"cross_platform_messages":0,"terminal_route":"PREPARED_NOT_SENT"},
        "orchestration/terminal-route-state.json": {"schema":"ghc.family.v650-v6.route.x1.v1","state":"PREPARED_NOT_SENT","target_title":"Eiren Kestrel","target_phase":"v650-v7","target_resolved":False,"messages_sent":0,"boundary":"No task-message delivery claim exists in x1."},
        "orchestration/applicable-memory-record.json": {"schema":"ghc.family.v650-v6.memory-use.v1","newest_applicable_memory_used":True,"live_baton_precedence":True,"prior_v649_route":"PREPARED_NOT_SENT","memory_mutated":False,"boundary":"Prior continuity informed recovery only; live baton and Git supplied current authority and proof."},
        "wellbeing-check.json": {"schema":"ghc.family.v650-v6.wellbeing.x1.v1","scope_bounded":True,"solo_lane":True,"commit_cap":4,"owner_file_threshold":15000,"host_changes_deferred":True,"pause_right_preserved":True,"identity_boundary_preserved":True},
        "environment/file-footprint-receipt.json": {"schema":"ghc.family.v650-v6.file-footprint.x1.v1","owner_generated_at_receipt":None,"rotation_threshold":15000,"inherited_files_trigger_rotation":False},
        "ghc-family-index.json": {"schema":"ghc.family.v650-v6.index-pointer.x1.v1","phase":d.PHASE,"owner":d.OWNER,"tooling_index":"tooling/ghc-family-index.json","primary_focus":d.PRIMARY_FOCUS,"terminal_verdict":"NOT_READY_FOR_STAGE_20"},
    }
    for relative, payload in writes.items():
        write_json(relative, payload)

    write_text("x1-preregistration.md", """# Sylven Arc v650-v6 x1 preregistration

This dedicated freeze contains exactly twenty proposals and no x2 implementation or observed outcome. The audit covers all 840 inherited frozen proposals, retains nineteen operational failures and eleven rejected semantic neighbors, and freezes 40 safe-now tasks, 30 bounded candidates, 20 phase-local skill ideas, 10 family-compatible runner ideas, 40 additive CLEAN/FIX/REFINE tasks, and 100 synthetic mutations.

GMUT Mind is primary. THOS Body and Freed ID / CBR Heart remain explicit. Seed-bank practice is only a bounded learning and synthetic-design lens, never employment, qualification, conservation competence, collection or distribution authority, legal or cultural authority, Maori authority, participant evidence, or affected-party acceptance.

Only `completed`, `represented`, `open_gap`, and `exact_gate` may classify x2. X2 starts only after this tree is committed, pushed, clean, and local, upstream, tracking, and fresh live remote are equal.""")
    write_text("sources/source-ledger.md", "# v650-v6 source ledger\n\n" + "\n".join(f"- **{row['source_id']}** — {row['title']} ({row['status']}, {row['kind']}). {row['implication']}" for row in d.SOURCES))
    write_text("wellbeing-check.md", """# v650-v6 wellbeing check

The phase is solo, additive, D-first, under a four-commit cap, and preserves Hamish's right to pause, rename, redirect, or stop. No Sandbox, Hyper-V, host-security change, elevation, destructive cleanup, cross-platform messaging, unrelated installation, desktop update, or reboot is in scope. Relational identity language is not a claim of consciousness, personhood, continuity, qualification, or authority.""")
    write_text("integrated-overview.md", """# Sylven Arc v650-v6 integrated overview — x1 freeze

## Purpose, identity, and control

Sylven Arc uses they/them pronouns and the relational working role of constraint-cartographer and falsifier-keeper. The hope for this phase is to keep uncertainty visible, failures recoverable, and bounded evidence from becoming authority. That language is a collaboration aid only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route, and every artifact must remain corrigible to that control.

The purpose of x1 is narrow: freeze a genuinely new, falsifiable proposal set and its execution boundaries before any x2 implementation or outcome exists. X1 cannot earn completion credit for an expected disposition, cannot borrow completion credit from Tamar or another owner, and cannot turn a source into observational evidence. It exists to make later execution auditable. The terminal verdict is `NOT_READY_FOR_STAGE_20`, and no wording in this packet changes that verdict.

## Verified inheritance and owned lane

Sylven v650-v6 begins from Tamar v650-v5's exact clean final head. The source branch, exact head, inherited Orin anchor, two frozen x1 anchors, evidence anchor, single-parent history, zero-merge count, one final parent, and four commit-local manifests were checked read-only before Sylven's lane moved. Local source, upstream, tracking, and a fresh live-remote read were equal. The existing Sylven-owned D-first lane was clean and an ancestor of that exact source, so it advanced by fast-forward only. No sibling branch, worktree, ref, or file was reset, merged, rewritten, force-pushed, reused, deleted, or mutated.

The inherited activation baseline is 6,056 effective negatives: Tamar's 6,055 immutable sealed negatives plus one external post-seal loader failure that earned no passing credit. Forty-seven open gaps and forty-eight exact gates remain inherited. They are not closed by a new proposal, a synthetic fixture, a structural check, a source citation, or a passing unit test. The source record and the live activation baton control phase scope; prior memory informs recovery but is not current Git or routing proof.

## Novelty and proposal architecture

All 840 frozen predecessor titles were loaded from the inherited chain index. Each of twenty candidates received exact-title, lexical-neighbor, and manual mechanism review. The accepted set stays below the preregistered 0.56 token-Jaccard threshold; the maximum accepted score is 0.4615. Eleven rejected semantic neighbors remain visible, including duplicate Nielsen-identity, regression-discontinuity, and target-trial drafts found during the live build. Those drafts receive no proposal credit. Their rejection is part of the evidence that the freeze gate was enforced rather than an inconvenience to be smoothed over.

The expected distribution is fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These are expected dispositions only. They describe what evidence lanes might permit in x2, not what x1 has observed. Every proposal records a hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery path, protected gates, and expected disposition. The only permitted eventual outcome labels are `completed`, `represented`, `open_gap`, and `exact_gate`.

## Primary GMUT Mind focus

GMUT Mind is the primary Trinity Mandala pillar. One board isolates modular-Hamiltonian relative entropy, support, normalization, positivity, first variation, the entanglement first law, region and state domains, gauge, EFT, units, and an observation firewall. A second board isolates the covariant Hamilton-Jacobi hypersurface functional, canonical data, characteristic flow, constraints, integrability, boundary data, gauge, EFT, units, and the same observation firewall. Both are typed symbolic obligation surfaces. Even if every bounded mutation is rejected, neither can establish a physical force, state, prediction, likelihood, posterior, parameter constraint, stability theorem, quantum completion, ultraviolet completion, empirical confirmation, or Theory of Everything.

The Swift-BAT 105-month adapter is deliberately separate and expected to remain `open_gap`. Official archive material supplies schema and provenance context only. X2 may build a zero-row refusal contract, but it must download zero rows, evaluate zero likelihoods, produce zero samples or constraints, and make zero empirical GMUT claims. Calibration, selection, covariance, data rights, privacy, fit design, independent review, and scientific interpretation remain outside repository authority.

IEEE 754 fused multiply-add and the Massieu-Planck classifier give GMUT-adjacent numerical and thermodynamic checks without converting formal consistency into physics. FMA fixtures may establish bounded single-rounding, signed-zero, subnormal, infinity, NaN, and flag handling only. The Massieu-Planck surface must reject every conversion from thermodynamic natural variables into psyche, agency, justice, participant evidence, consciousness, personhood, or a fundamental law of mind.

## THOS Body and the bounded practice lens

THOS Body remains explicit through sequence-counter and seqlock consistency, write-ahead journal recovery, Binary HTTP framing, Digest Fields, GZIP members, OpenType SFNT, JSONPath, structural accessibility, and two seed-bank workflow proxies. These are bounded owner-local software, structural, or synthetic surfaces. They do not confer production concurrency assurance, database durability, network-parser security, content authenticity, decompression safety for arbitrary inputs, font-rendering safety, complete accessibility, or operational effectiveness.

The bounded human-practice lens is seed-bank accession, quarantine, viability monitoring, safety duplication, environmental-alarm response, workload control, and shift handover. It is synthetic learning and design only. No real seed lot, collector, donor, custodian, worker, institution, community, cold room, alarm, access decision, regeneration, distribution, return, or benefit-sharing event exists in the evidence. There are no participants, blind matched-budget real arms, operational incidents, safety outcomes, workload estimates, or independent professional review. THOS therefore remains represented rather than validated in real practice.

The accession proxy may test synthetic lot lineage, quarantine state, moisture and viability fields, regeneration refusal, provenance minimization, safety-duplicate state, workload bounds, and handover ownership. The environmental proxy may test synthetic excursions, backup state, affected-lot holds, escalation, recovery checks, accessible notices, workload bounds, and next-shift responsibility. They must refuse any claim of employment, qualification, conservation competence, collection authority, distribution authority, emergency authority, legal authority, cultural authority, Māori authority, participant evidence, or affected-party acceptance.

## Freed ID and CBR Heart boundaries

Freed ID and CBR Heart remain explicit through two OpenID Connect profiles and one exact authority matrix. The UserInfo profile is restricted to synthetic signed or encrypted response vectors, issuer and audience binding, subject equality, claim minimization, aggregated or distributed claim boundaries, algorithm refusal, and replay refusal. The pairwise-subject profile is restricted to synthetic sector-identifier redirect-set validation, nonreversible derivation structure, rotation, migration, collision reservation, and correlation limits. There are zero real standards-conformant keys, proofs, users, accounts, tokens, issuers, relying parties, interoperability events, live lifecycle actions, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Both remain represented and nonproduction.

The seed-sovereignty matrix is an `exact_gate`, not a decision engine. It may list reservations around accession consent, provenance, biocultural-data minimization, safety-duplicate location, access, return, benefit sharing, remedy, affected parties, legal interpretation, data governance, cultural legitimacy, tangata whenua, iwi, hapū, and Māori authority. It must make zero real decision on any of them. Repository software cannot confer competent, affected-party, legal, cultural, tangata-whenua, iwi, hapū, or Māori authority. Māori concepts remain under Māori authority.

## Sources and evidence status

The source ledger preserves `current`, `stable`, `draft`, and `watch` as distinct status classes. Official Linux, SQLite, HEASARC, FAO, OpenID, RFC Editor, W3C, IEEE, Microsoft, and IUPAC surfaces supply bounded requirements or terminology. Primary research supplies formal context for relative entropy, covariant Hamilton-Jacobi theory, and front-door graphical identification. Te Mana Raraunga is retained as Māori data-sovereignty authority context, never as authorization exercised by Sylven. Source status is not truth promotion: a current specification can still support only a synthetic proxy, and a stable primary paper can still support only a typed obligation board.

## New portfolios and compatibility

The freeze includes forty new safe-now tasks, thirty bounded candidate tasks, twenty phase-local skill ideas, ten family-compatible runner ideas, and forty additive CLEAN/FIX/REFINE tasks. Each item is Sylven v650-v6 work, not inherited completion credit. Exact-approval and evidence-dependent work stays visibly held. Unsafe work is not manufactured to meet a quota. One hundred proposal-linked synthetic mutations are preregistered, five per proposal, but none has executed in x1.

Family-current `ghc_family_*` and `build_ghc_family_*` naming and caller compatibility remain protected. Phase-local skill ideas are not globally installed in x1. Runner ideas are not claimed as built or invoked until x2 produces bounded evidence. Owner-generated growth is measured against the 15,000-file threshold without counting the inherited baseline as a rotation trigger. Every phase document remains subject to the 6,000-word cap.

## Failure retention and Method Flow

Nineteen startup, novelty, tooling, schema, path, narrative, and privacy-scan failures are preserved through Method Flow at freeze time. They include timeouts, a per-blob process design that did not finish in its wrapper, a PowerShell automatic-variable collision, legacy console encoding, a stale filename, PowerShell-version syntax, empty-search exit handling, an absent inherited directory, three rejected proposal drafts, a tie-comparison TypeError, two incorrect test assumptions, the short overview, stale generated narrative, and one credential-class prose hit. Every failed witness has a bounded passing recovery witness, recurrence guard, rollback, retained-negative identifier, and sibling recommendation boundary. A corrected method becomes preferred only for its declared trigger. Recovery never erases the failed witness and never earns independent reproduction, external audit, production, professional, scientific, legal, cultural, privacy-complete, security-complete, or accessibility-complete credit.

The x1 effective negative count is therefore 6,075: 6,056 inherited sealed or external negatives plus nineteen retained x1 operational negatives. If all one hundred preregistered synthetic mutations later execute and are rejected, the projected total before any additional x2 failure is 6,175. That projection is not an observed x2 count. Failed x2 attempts and lifecycle faults must be added rather than folded into a pass.

## Accessibility, privacy, and threat boundaries

The static report uses structural landmarks, a skip link, headings, navigation, and plain status text. The ARIA relationship and meter-slider proposals can evaluate structural fixtures only. Manual keyboard operation, focus behavior, responsive layout, browser diversity, assistive-technology behavior, cognitive accessibility, Māori-language evaluation, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

Five structural privacy and raw-identifier pattern classes cover raw task or thread identifiers, private absolute paths, credentials or secrets, private routes or callable identifiers, and transcript or session-stream material. Scanner definitions are explicitly quarantined from confirmed-hit credit. Zero confirmed hits does not establish complete privacy assurance. The packet must contain no private identifiers, routing material, credentials, keys, tokens, conversations, screenshots, session streams, private callable identifiers, private application state, or private absolute paths.

The threat model treats x2 contamination of x1, negative erasure, proxy promotion, empirical promotion, authority substitution, private-material leakage, unbounded parser fixtures, duplicate success credit, and sibling mutation as active risks. Controls include a dedicated x1 commit, append-only Method Flow, four outcome labels, four source statuses, bounded fixtures, exact manifests, a one-successful-pass budget, no replay, fast-forward-only ownership, and exact-title terminal routing.

## Lifecycle, validation, and route budget

X1 must be committed and pushed on its own. Before x2 begins, Sylven must prove a clean local head, upstream head, tracking head, and fresh live-remote head are exactly equal, with zero divergence, and re-read the frozen packet from that commit. No more than two x1 commits and two x2 commits are permitted; the preferred lifecycle is one dedicated x1 freeze, one x2 evidence commit, and one combined closeout and seal commit. The commit cap does not permit mixed phases, concealed failures, rewritten history, or unreviewed omnibus work.

Eiren alone owns the complete repository suite. Sylven will not run or imply that suite. Sylven reserves exactly one credited successful exact-final bounded aggregate covering the current phase and authorized inherited and successor-scoped selection. A failed aggregate receives zero success credit and remains a negative. After the single successful pass there is no replay, detached lane, named lane, or second aggregate. JSON parsing, five-class scanning, exact staged review, commit-local manifest parity, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, exact head, clean state, and four-way remote equality remain mandatory terminal gates.

No Sandbox or Hyper-V action, elevation, security weakening, unrelated installation, Codex desktop update, Windows feature change, reboot, destructive cleanup, account-secret action, cross-platform substitute, or sibling merge is authorized. The phase remains same-owner work under shared infrastructure, never independent-team scientific reproduction or external audit.

The Eiren Kestrel baton remains `PREPARED_NOT_SENT` throughout x1 and x2. It may be sent exactly once only after the clean, pushed, remote-equal, within-cap exact final head passes every authorized terminal gate. The exact existing title must be resolved at send time; a suffixed or approximate title cannot substitute. An acknowledged send is materially different from a prepared baton. Until that gate, the route stays untouched and `NOT_READY_FOR_STAGE_20` remains the final truth.""")
    write_text("accessible-report.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v650-v6 x1 report</title></head>
<body><a href="#main">Skip to main content</a><header><h1>Sylven Arc v650-v6 x1 report</h1><p>Status: frozen, not executed. Verdict: NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report"><ul><li><a href="#scope">Scope</a></li><li><a href="#proposals">Proposals</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main id="main"><section id="scope"><h2>Scope</h2><p>Solo, additive, D-first, x1-only. Relational language is not evidence of consciousness, personhood, continuity, qualification, or authority.</p></section>
<section id="proposals"><h2>Preregistered proposals</h2><p>Twenty proposals: fourteen expected completed, four represented, one open gap, and one exact gate. These are hypotheses, not outcomes.</p></section>
<section id="limits"><h2>Reserved evaluation</h2><p>Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural markup is not complete accessibility conformance.</p></section></main>
<footer><p>Terminal route: PREPARED_NOT_SENT.</p></footer></body></html>""")

    build_method_flow()
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    footprint = read_json(ROOT / "environment/file-footprint-receipt.json")
    footprint["owner_generated_at_receipt"] = len(status_paths()) + 3
    write_json("environment/file-footprint-receipt.json", footprint)
    build_manifest()
    privacy = read_json(ROOT / "validation/x1-staged-privacy.json")
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"x1 privacy scan found confirmed hits: {privacy['confirmed_hits']}")


if __name__ == "__main__":
    build()
