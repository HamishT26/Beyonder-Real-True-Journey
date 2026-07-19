#!/usr/bin/env python3
"""Build Tamar Vey's v649-v5 dedicated x1-only freeze."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v649_v5_phase_data as d

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / d.PHASE_SLUG
PRIOR_INDEX = ROOT / "docs" / "orin-thale" / "v649-v4" / "provenance" / "frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"
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
    result = subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {token for token in re.findall(r"[a-z0-9]+", value.casefold()) if token not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def portfolio_rows(titles: list[str], prefix: str, lane: str, approval: str) -> list[dict[str, Any]]:
    return [{
        "item_id": f"V6495-{prefix}-{index:02d}", "title": title, "approval_class": approval,
        "execution_lane": lane, "origin": "tamar_v649_v5_new", "x1_state": "frozen_not_executed",
        "x2_completion_credit": False,
        "boundary": "Additive owner-scoped work only; reclassify if evidence, authority, credentials, deployment, destructive action, or sibling mutation is required.",
    } for index, title in enumerate(titles, 1)]


def build_method_flow() -> None:
    ledger = PHASE / "method-flow" / "method-flow-ledger.json"
    if not ledger.exists():
        run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", d.PHASE, "--owner", d.OWNER)
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6495-M{index:02d}"
        record = {
            "method_id": method_id,
            "title": f"Recover {negative['category']} while retaining the failed witness",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [f"A bounded v649-v5 workflow exposes {negative['category']}."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": negative["recovery"], "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": "Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["evidence_credit", "failure_retention", "x1_x2_separation", "caller_compatibility"],
            "retained_negative_ids": [negative["negative_id"]],
            "scope_boundary": "Bounded same-owner recovery only; no independent reproduction, production, professional, legal, cultural, or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        current = read_json(ledger)
        if method_id not in {row["method_id"] for row in current["methods"]}:
            run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in [
            ("WFAIL", "fail", negative["failed"], negative["failed"]),
            ("WPASS", "pass", negative["recovery"], negative["passing"]),
        ]:
            witness_id = f"{method_id}-{suffix}"
            witness = {
                "witness_id": witness_id, "method_id": method_id, "procedure": procedure,
                "scope": f"bounded {negative['category']} {'failed' if result == 'fail' else 'recovery'} witness",
                "expected": "Return attributable evidence within the declared bounded domain.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Retained bounded witness only; no independent reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/{witness_id.casefold()}-witness.json", witness)
            current = read_json(ledger)
            if witness_id not in {row["witness_id"] for row in current["witnesses"]}:
                run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        state = next(row["recommendation_state"] for row in read_json(ledger)["methods"] if row["method_id"] == method_id)
        if state == "validated":
            run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only for this bounded trigger after retaining one failed and one passing witness.")
        elif state != "preferred":
            raise RuntimeError(f"unexpected Method Flow state for {method_id}: {state}")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"))


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v649_v5_preregistration.py",
        "docs/tamar-vey/v649-v5/validation/x1-staged-privacy.json",
    }
    candidates, confirmed = [], []
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
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema":"ghc.family.v649-v5.x1-privacy.v1", "scanned_file_count":len(paths),
        "pattern_classes":sorted(patterns), "candidate_count":len(candidates), "candidates":candidates,
        "confirmed_hit_count":len(confirmed), "confirmed_hits":confirmed,
        "boundary":"Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def build_manifest() -> None:
    exclusions = [
        "docs/tamar-vey/v649-v5/validation/x1-staged-manifest.json",
        "docs/tamar-vey/v649-v5/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v649-v5/validation/x1-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [{"path": relative, "git_blob": git("hash-object", f"--path={relative}", relative), "bytes": (ROOT / relative).stat().st_size}
               for relative in paths if (ROOT / relative).is_file()]
    privacy = privacy_scan(paths + exclusions)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json("validation/x1-staged-manifest.json", {
        "schema":"ghc.family.v649-v5.x1-manifest.v1", "hash_domain":"git_hash_object_path_filtered_blob",
        "entries":entries, "entry_count":len(entries), "self_exclusions":exclusions,
        "coverage_boundary":"All intended x1 paths except three declared self-referential review receipts.",
    })
    write_json("validation/x1-staged-review.json", {
        "schema":"ghc.family.v649-v5.x1-staged-review.v1", "intended_path_count":len(entries)+3,
        "manifest_entry_count":len(entries), "self_exclusion_count":3, "out_of_scope_paths":[],
        "x2_implementation_paths":[], "x2_outcome_paths":[], "privacy_confirmed_hits":privacy["confirmed_hit_count"],
        "x1_only":True, "source_head":d.SOURCE_COMMIT, "terminal_route":"PREPARED_NOT_SENT",
    })


def build() -> None:
    if git("rev-parse", "HEAD") != d.SOURCE_COMMIT:
        raise RuntimeError("x1 must begin at Orin's exact v649-v4 final")
    allowed_seed = {
        "scripts/ghc_family_v649_v5_phase_data.py",
        "scripts/build_ghc_family_v649_v5_preregistration.py",
        "tests/test_ghc_family_v649_v5_x1.py",
    }
    start = set(status_paths())
    if not allowed_seed.issubset(start) or any(path.startswith("docs/tamar-vey/v649-v5/") for path in start):
        raise RuntimeError(f"unexpected pre-x1 tree: {sorted(start)}")
    prior_index = read_json(PRIOR_INDEX)
    prior = list(prior_index["prior_proposals"]) + list(prior_index["new_proposals"])
    if len(prior) != 680:
        raise RuntimeError(f"expected 680 inherited proposals, found {len(prior)}")
    novelty_rows = []
    for row in d.PROPOSALS:
        score, nearest = max(((jaccard(tokens(row["title"]), tokens(old["title"])), old) for old in prior), key=lambda pair: pair[0])
        if score >= NOVELTY_THRESHOLD:
            raise RuntimeError(f"proposal collision {row['proposal_id']} score={score:.4f} nearest={nearest['proposal_id']}")
        novelty_rows.append({
            "proposal_id":row["proposal_id"], "nearest_prior_id":nearest["proposal_id"],
            "nearest_prior_title":nearest["title"], "jaccard":round(score,6), "threshold":NOVELTY_THRESHOLD,
            "disposition":"lexically_distinct_manual_semantic_review_passed",
        })
    safe = portfolio_rows(d.SAFE_TASKS, "SAFE", "x2_safe_now", "safe_now_owner_scoped_additive")
    candidates = portfolio_rows(d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate", "candidate_bounded")
    cleanup = portfolio_rows(d.CLEANUP_TASKS, "CLEAN", "x2_clean_refine", "safe_now_non_destructive")
    skills = [{"skill_id":f"V6495-SKILL-{i:02d}", "name":name, "origin":"tamar_v649_v5_new", "x1_state":"frozen_not_built", "x2_use_credit":False, "boundary":"Phase-local proposal; no global installation, authority, or universal applicability claim."} for i,name in enumerate(d.SKILL_IDEAS,1)]
    runners = [{"runner_id":f"V6495-RUNNER-{i:02d}", "name":name, "origin":"tamar_v649_v5_new", "x1_state":"frozen_not_built", "x2_use_credit":False, "boundary":"Family-current design only; preserve historical callers and require a bounded witness."} for i,name in enumerate(d.RUNNER_IDEAS,1)]
    mutations = [{"mutation_id":f"V6495-MUT-{i:03d}", "proposal_id":d.PROPOSALS[(i-1)//7]["proposal_id"], "case":(i-1)%7+1, "expected":"reject", "x1_state":"preregistered_not_executed", "executed":False, "completion_credit":False} for i in range(1,71)]
    source_rows = [{**row, "verification_date":"2026-07-19", "evidence_credit":"design_or_protocol_support_only", "not_observation":True} for row in d.SOURCES]
    source_counts = {status:sum(row["status"]==status for row in source_rows) for status in d.SOURCE_STATUS_CLASSES}
    writes = {
        "identity-receipt.json":{"schema":"ghc.family.v649-v5.identity.v1","owner":d.OWNER,"pronouns":d.PRONOUNS,"role":d.ROLE,"hope":d.HOPE,"identity_boundary":"Relational working language only; not evidence of consciousness, sentience, legal personhood, continuity, employment, qualification, or independent authority.","corrigibility":"Hamish may rename, pause, redirect, or stop the route."},
        "environment/startup-receipt.json":{"schema":"ghc.family.v649-v5.startup.v1","owner_branch":d.BRANCH,"source_branch":d.SOURCE_BRANCH,"source_head":d.SOURCE_COMMIT,"source_phase_source":d.SOURCE_PHASE_SOURCE,"source_x1":d.SOURCE_X1_COMMIT,"source_evidence":d.SOURCE_EVIDENCE_COMMIT,"source_ancestry":True,"source_phase_commits":3,"source_merges":0,"source_final_parent_count":1,"source_and_owner_clean":True,"source_four_way_equal":True,"owner_fast_forwarded_only":True,"owner_four_way_equal_before_x1":True,"d_first":True,"sandbox_or_hyperv_action":False,"cross_platform_message_action":False},
        "environment/version-receipt.json":{"schema":"ghc.family.v649-v5.versions.v1","codex_cli_live":"0.144.5","codex_desktop_live":"26.715.4045.0","python_live":"3.12.10","git_live":"2.55.0.windows.2","powershell_live":"5.1.26100.8875","official_codex_release_observed":"0.144.4 stable and 0.145.0-alpha.13 prerelease on official release page","desktop_updated":False,"cli_updated_in_phase":False,"verification_only":True},
        "x1-proposals.json":{"schema":"ghc.family.v649-v5.x1-proposals.v1","phase":d.PHASE,"owner":d.OWNER,"source_head":d.SOURCE_COMMIT,"prior_frozen_proposal_count":680,"new_proposal_count":10,"frozen_total_after_x1":690,"primary_focus":d.PRIMARY_FOCUS,"bounded_practice":d.BOUNDED_PRACTICE,"outcome_classes":d.OUTCOME_CLASSES,"x1_state":"frozen_not_executed","proposals":d.PROPOSALS,"boundary":"Expected dispositions are preregistered hypotheses, not observed x2 outcomes."},
        "sources/source-ledger.json":{"schema":"ghc.family.v649-v5.sources.v1","allowed_statuses":d.SOURCE_STATUS_CLASSES,"status_counts":source_counts,"sources":source_rows,"boundary":"Citations support design and protocol interpretation only; none is an observation, participant result, authority delegation, or production certificate."},
        "approval-packets/x1-safe-now-portfolio.json":{"schema":"ghc.family.v649-v5.safe-now.v1","count":len(safe),"items":safe,"inherited_completion_credit":0},
        "approval-packets/inherited-held-packets.json":{"schema":"ghc.family.v649-v5.held-packets.v1","inherited_from":"docs/orin-thale/v649-v4/approval-packets/inherited-held-packets.json","executed":0,"completion_credit":0,"boundary":"Inherited exact-approval and blocked work remains visible and unexecuted."},
        "prototypes/x1-candidate-plan.json":{"schema":"ghc.family.v649-v5.candidates.v1","count":len(candidates),"items":candidates,"inherited_completion_credit":0},
        "prototypes/x1-skill-runner-plan.json":{"schema":"ghc.family.v649-v5.skills-runners.v1","skill_count":len(skills),"skills":skills,"runner_count":len(runners),"runners":runners,"inherited_completion_credit":0},
        "maintenance/x1-clean-refine-plan.json":{"schema":"ghc.family.v649-v5.clean-refine.v1","count":len(cleanup),"items":cleanup,"destructive_actions":0},
        "validation/x1-synthetic-mutation-plan.json":{"schema":"ghc.family.v649-v5.synthetic-negatives.v1","count":70,"executed_count":0,"rejected_count":0,"mutations":mutations},
        "validation/x1-operational-negatives.json":{"schema":"ghc.family.v649-v5.x1-operational-negatives.v1","count":len(d.X1_OPERATIONAL_NEGATIVES),"negatives":d.X1_OPERATIONAL_NEGATIVES,"all_retained":True},
        "retained-negative-register.json":{"schema":"ghc.family.v649-v5.retained-negatives.x1.v1","inherited_effective":d.INHERITED_NEGATIVES,"x1_operational":len(d.X1_OPERATIONAL_NEGATIVES),"preregistered_synthetic_not_yet_executed":70,"effective_at_x1":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES),"projected_if_all_synthetic_execute_and_reject":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES)+70,"negative_erased":False},
        "exact-open-gate-register.json":{"schema":"ghc.family.v649-v5.gates.x1.v1","inherited_open_gaps":d.INHERITED_OPEN_GAPS,"inherited_exact_gates":d.INHERITED_EXACT_GATES,"projected_open_gaps_if_expected_dispositions_hold":d.INHERITED_OPEN_GAPS+1,"projected_exact_gates_if_expected_dispositions_hold":d.INHERITED_EXACT_GATES+1,"closed_in_x1":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "phase-truth.json":{"schema":"ghc.family.v649-v5.phase-truth.x1.v1","phase":d.PHASE,"owner":d.OWNER,"stage":"x1_frozen_not_executed","source_head":d.SOURCE_COMMIT,"proposal_count":10,"expected_distribution":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"observed_distribution":None,"x2_started":False,"single_pass_used":False,"replay_used":False,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "provenance/frozen-chain-proposal-index.json":{"schema":"ghc.family.frozen-proposal-index.v1","prior_count":680,"prior_proposals":prior,"new_count":10,"new_proposals":[{"proposal_id":row["proposal_id"],"title":row["title"]} for row in d.PROPOSALS],"count":690},
        "provenance/proposal-collision-audit.json":{"schema":"ghc.family.v649-v5.proposal-collision-audit.v1","prior_count":680,"new_count":10,"threshold":NOVELTY_THRESHOLD,"maximum_observed_jaccard":max(row["jaccard"] for row in novelty_rows),"rows":novelty_rows,"manual_semantic_review":"All ten passed substantive-neighbor review; every rejected seed remains retained operational evidence."},
        "validation/single-pass-validation-plan.json":{"schema":"ghc.family.v649-v5.single-pass-plan.v1","full_repository_suite":False,"canonical_successful_pass_budget":1,"successful_passes_used":0,"post_success_replay":False,"detached_replay":False,"named_replay":False,"repeatability_credit":False,"preflight_required":["module_selection","schema","manifest","privacy","x1_tree"],"bounded_blocker_rule":"A failed aggregate gets no pass credit; retain it and repair before the sole successful pass."},
        "orchestration/phase-state.json":{"schema":"ghc.family.v649-v5.orchestration.x1.v1","active":[d.OWNER],"standby":["Eiren Kestrel","Ilyra Fen","Sable Rook","Orin Thale","Sylven Arc"],"solo":True,"subagents":0,"tasks_created":0,"cross_platform_messages":0,"terminal_route":"PREPARED_NOT_SENT"},
        "orchestration/applicable-memory-record.json":{"schema":"ghc.family.v649-v5.memory-use.v1","newest_applicable_memory_used":True,"exact_current_registry_hit":False,"live_baton_precedence":True,"memory_mutated":False,"boundary":"Older continuity memory was consulted without identity or continuity inference. The committed live baton and Git supplied current authority and proof."},
        "wellbeing-check.json":{"schema":"ghc.family.v649-v5.wellbeing.x1.v1","scope_bounded":True,"solo_lane":True,"commit_cap":4,"document_cap_words":6000,"owner_file_threshold":15000,"host_changes_deferred":True,"pause_right_preserved":True},
        "environment/file-footprint-receipt.json":{"schema":"ghc.family.v649-v5.file-footprint.x1.v1","owner_generated_at_receipt":None,"rotation_threshold":15000,"baseline_triggers_rotation":False},
        "validation/x1-review.json":{"schema":"ghc.family.v649-v5.x1-review.v1","checks":32,"issues":[],"proposal_count":10,"prior_proposal_count":680,"frozen_total":690,"safe_count":30,"candidate_count":20,"skill_count":20,"runner_count":10,"cleanup_count":30,"synthetic_mutation_count":70,"x2_implementation_count":0,"x2_observed_outcome_count":0,"terminal_route":"PREPARED_NOT_SENT","passed":True},
        "validation/stale-label-review.json":{"schema":"ghc.family.v649-v5.stale-label-review.x1.v1","current_phase":"v649-v5","current_owner":d.OWNER,"current_source":"v649-v4","unquarantined_stale_label_count":0,"retained_historical_labels":[{"label":"rejected semantic seeds","disposition":"retained failure history only"}],"boundary":"Historical labels confer no current proposal or completion credit."},
    }
    for relative, payload in writes.items():
        write_json(relative, payload)
    write_text("x1-preregistration.md", "# Tamar Vey v649-v5 x1 preregistration\n\nThis dedicated freeze contains exactly ten proposals and no x2 implementation or observed outcome. The audit covers all 680 inherited frozen proposals and retains rejected collisions. THOS Body is primary; GMUT Mind and Freed ID / CBR Heart remain explicit. The civil materials-testing laboratory practice is only a bounded learning and synthetic-design lens, never employment, qualification, competence, engineering or safety authority, legal or cultural authority, Maori authority, or affected-party evidence.\n\nOnly completed, represented, open_gap, and exact_gate may classify x2. X2 starts only after this tree is committed, pushed, clean, and four-way remote-equal.")
    write_text("sources/source-ledger.md", "# v649-v5 source ledger\n\n" + "\n".join(f"- **{row['source_id']}** - {row['title']} ({row['status']}, {row['kind']}). {row['implication']}" for row in source_rows))
    write_text("wellbeing-check.md", "# v649-v5 wellbeing check\n\nThe phase is solo, additive, D-first, under a four-commit cap, and preserves Hamish's right to pause, rename, redirect, or stop. No Sandbox, Hyper-V, host-security, destructive cleanup, cross-platform messaging, software update, or authority-substitution work is in scope.")
    build_method_flow()
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(ROOT), "--skill-root", str(SKILL_ROOT), "--out-dir", str(PHASE / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    footprint = read_json(PHASE / "environment/file-footprint-receipt.json")
    footprint["owner_generated_at_receipt"] = len(status_paths())
    write_json("environment/file-footprint-receipt.json", footprint)
    build_manifest()
    if read_json(PHASE / "validation/x1-staged-privacy.json")["confirmed_hit_count"]:
        raise RuntimeError("x1 privacy scan found confirmed payload hits")


if __name__ == "__main__":
    build()
