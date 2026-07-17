#!/usr/bin/env python3
"""Build Ilyra Fen v647-v6 strict x1-only preregistration artifacts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v647_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"
SOURCE_PHASE = ROOT / "docs/eiren-kestrel/v647-v5"
METHOD_RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def overlap(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 0.0


def prior_proposals() -> list[dict[str, str]]:
    inherited = read_json(SOURCE_PHASE / "provenance/frozen-chain-proposal-index.json")
    rows = list(inherited.get("prior_proposals", []))
    if len(rows) != 510:
        raise RuntimeError(f"expected 510 indexed proposals, found {len(rows)}")
    source_rows = read_json(SOURCE_PHASE / "x1-proposals.json").get("proposals", [])
    if len(source_rows) != 10:
        raise RuntimeError(f"expected ten Eiren proposals, found {len(source_rows)}")
    source_path = "docs/eiren-kestrel/v647-v5/x1-proposals.json"
    rows.extend(
        {"path": source_path, "proposal_id": row["proposal_id"], "title": row["title"]}
        for row in source_rows
    )
    if len(rows) != d.PRIOR_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(rows)}")
    return rows


def prior_portfolio_titles() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    patterns = [
        ("docs/**/approval-packets/x1-approval-portfolio.json", ("safe_now", "candidates", "exact_approval", "blocked")),
        ("docs/**/prototypes/x1-skill-runner-plan.json", ("skills", "runners")),
        ("docs/**/maintenance/x1-clean-refine-plan.json", ("tasks",)),
    ]
    for pattern, categories in patterns:
        for path in ROOT.glob(pattern):
            if PHASE in path.parents:
                continue
            try:
                data = read_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            for category in categories:
                for item in data.get(category, []):
                    if not isinstance(item, dict):
                        continue
                    title = item.get("title") or item.get("name")
                    if title:
                        rows.append({"category": category, "title": str(title), "path": path.relative_to(ROOT).as_posix()})
    return rows


def proposal_audit(prior: list[dict[str, str]]) -> dict[str, Any]:
    by_norm: dict[str, list[dict[str, str]]] = {}
    for row in prior:
        by_norm.setdefault(normalized(row["title"]), []).append(row)
    collisions = []
    nearest = []
    for proposal in d.PROPOSALS:
        norm = normalized(proposal["title"])
        for row in by_norm.get(norm, []):
            collisions.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "prior": row})
        ranked = sorted(
            (
                {"overlap": round(overlap(proposal["title"], row["title"]), 4), "prior_id": row["proposal_id"], "prior_title": row["title"], "path": row["path"]}
                for row in prior
            ),
            key=lambda row: (-row["overlap"], row["path"], row["prior_id"]),
        )[:5]
        nearest.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "nearest": ranked})
    return {
        "schema": "ghc.family.v647-v6.prior-proposal-collision-audit.v1",
        "prior_count": len(prior),
        "new_count": len(d.PROPOSALS),
        "exact_collision_count": len(collisions),
        "exact_collisions": collisions,
        "nearest_neighbors": nearest,
        "valid": not collisions and len(prior) == d.PRIOR_FROZEN_PROPOSALS,
        "boundary": "Exact-title and bounded token-overlap review supports preregistration novelty only; it is not scientific originality, patent review, or independent reproduction.",
    }


def current_portfolio_rows() -> list[dict[str, str]]:
    rows = []
    for category, titles in (
        ("safe_now", d.SAFE_TASK_TITLES),
        ("candidates", d.CANDIDATE_TITLES),
        ("skills", [name for name, _ in d.SKILL_SPECS]),
        ("runners", d.RUNNER_TITLES),
        ("tasks", d.CLEAN_TASK_TITLES),
        ("exact_approval", d.EXACT_PACKET_TITLES),
        ("blocked", d.BLOCKED_PACKET_TITLES),
    ):
        rows.extend({"category": category, "title": title} for title in titles)
    return rows


def portfolio_audit(prior: list[dict[str, str]]) -> dict[str, Any]:
    current = current_portfolio_rows()
    prior_by_norm: dict[str, list[dict[str, str]]] = {}
    for row in prior:
        prior_by_norm.setdefault(normalized(row["title"]), []).append(row)
    collisions = []
    for row in current:
        for earlier in prior_by_norm.get(normalized(row["title"]), []):
            collisions.append({"current": row, "prior": earlier})
    norms = Counter(normalized(row["title"]) for row in current)
    within = sorted(key for key, count in norms.items() if count > 1)
    return {
        "schema": "ghc.family.v647-v6.prior-portfolio-collision-audit.v1",
        "prior_title_count": len(prior),
        "current_title_count": len(current),
        "exact_collision_count": len(collisions),
        "exact_collisions": collisions,
        "within_current_duplicates": within,
        "valid": not collisions and not within,
        "boundary": "Exact normalized-title review is a bounded novelty gate, not a claim that broader concepts have no predecessors.",
    }


def task_rows(prefix: str, titles: list[str], approval_class: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"V6476-{prefix}-{index:02d}",
            "title": title,
            "approval_class": approval_class,
            "x1_state": "preregistered_no_completion_credit",
            "x2_completion_credit": False,
            "protected_gates": ["external_state", "sibling_lane", "destructive_action", "authority", "stage20"],
        }
        for index, title in enumerate(titles, 1)
    ]


def method_record(method_id: str, title: str, signature: str, trigger: str, workaround: str, guard: str, negatives: list[str]) -> dict[str, Any]:
    return {
        "method_id": method_id,
        "title": title,
        "failure_signature": signature,
        "trigger_preconditions": [trigger],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped_workflow",
        "candidate_workaround": workaround,
        "validation_witness_ids": [],
        "recurrence_guard": guard,
        "rollback": "Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["private_paths", "sibling_lane", "destructive_action", "external_state", "independent_reproduction"],
        "retained_negative_ids": negatives,
        "scope_boundary": "Preferred only for the declared local workflow trigger; it grants no scientific, professional, authority, production, or independent-reproduction credit.",
    }


def witness(witness_id: str, method_id: str, procedure: str, expected: str, observed: str, result: str, negatives: list[str]) -> dict[str, Any]:
    return {
        "witness_id": witness_id,
        "method_id": method_id,
        "procedure": procedure,
        "scope": "bounded owner-local read-only startup or parsing probe",
        "expected": expected,
        "observed": observed,
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": negatives,
        "boundary": "Workflow evidence only; no broader scientific, security, accessibility, identity, production, or authority conclusion.",
    }


def run_method_flow() -> None:
    ledger = PHASE / "method-flow/method-flow-state.json"
    methods = [
        method_record(
            "V6476-M01",
            "Bounded full skill read after short-wrapper timeout",
            "Required full skill or metadata read exceeds a short process wrapper before content returns.",
            "A required local instruction file has not yet been read to EOF and the short wrapper timed out.",
            "Inventory the exact file with a bounded fast probe, then read the unchanged file in full with a 60-second wrapper.",
            "Do not repeat the same short wrapper; preserve every timeout and verify EOF content before task action.",
            ["V6476-X1-N01", "V6476-X1-N02"],
        ),
        method_record(
            "V6476-M02",
            "Explicit remote-ref revision-range equality",
            "PowerShell transforms an upstream expression embedded in a Git revision range.",
            "A Git equality range uses an upstream expression inside PowerShell command text.",
            "Resolve or name the full remote-tracking ref explicitly and pass that ref to Git revision-range commands.",
            "Never embed an unquoted upstream hashtable-like expression in a PowerShell revision range.",
            ["V6476-X1-N03"],
        ),
        method_record(
            "V6476-M03",
            "Built-in JSON parser fallback without installation",
            "An optional command-line JSON utility is unavailable in the ordinary process.",
            "JSON inspection is required and the optional utility is not already installed.",
            "Use the platform built-in JSON parser under explicit UTF-8 and deterministic output; do not install unrelated software.",
            "Probe utility availability once, then select the built-in parser and retain the missing-tool event.",
            ["V6476-X1-N04"],
        ),
        method_record(
            "V6476-M04",
            "Exact portfolio collision quarantine before materialization",
            "A preregistration plan reuses normalized titles from inherited portfolio ledgers.",
            "Current safe-task skill runner cleanup exact or blocked titles are audited against inherited portfolios.",
            "Stop before materialization, rename or rewrite exact collisions, and rerun the unchanged normalized-title audit.",
            "Require zero inherited and zero within-current exact collisions before generating phase artifacts.",
            ["V6476-X1-N05"],
        ),
        method_record(
            "V6476-M05",
            "Non-self-matching forbidden-credit scanner definition",
            "A staged scanner matches the literal forbidden byte sequence embedded in its own source definition.",
            "The scanner source is included in the staged surface it reviews.",
            "Construct the same forbidden sequence from adjacent byte fragments while leaving target matching unchanged.",
            "Forward-test every literal scanner needle against its own source before staged review credit.",
            ["V6476-X1-N06"],
        ),
    ]
    witness_sets = [
        (
            witness("V6476-M01-WFAIL", "V6476-M01", "Short-wrapper full-read attempt", "Return complete content", "Timed out before content returned", "fail", ["V6476-X1-N01", "V6476-X1-N02"]),
            witness("V6476-M01-WPASS", "V6476-M01", "Bounded inventory plus 60-second direct full read", "Return complete content through EOF", "Both required skills and references returned completely", "pass", ["V6476-X1-N01", "V6476-X1-N02"]),
        ),
        (
            witness("V6476-M02-WFAIL", "V6476-M02", "Equality range using upstream expression", "Return zero divergence", "Git rejected the transformed revision token", "fail", ["V6476-X1-N03"]),
            witness("V6476-M02-WPASS", "V6476-M02", "Equality range using explicit remote-tracking ref", "Return zero divergence", "Returned zero ahead and zero behind", "pass", ["V6476-X1-N03"]),
        ),
        (
            witness("V6476-M03-WFAIL", "V6476-M03", "Invoke optional JSON utility", "Parse keys", "Utility was not present", "fail", ["V6476-X1-N04"]),
            witness("V6476-M03-WPASS", "V6476-M03", "Use built-in JSON parser", "Parse required proposal documents", "Parsed proposal schemas and titles without installation", "pass", ["V6476-X1-N04"]),
        ),
        (
            witness("V6476-M04-WFAIL", "V6476-M04", "Run normalized portfolio-title audit", "Return zero exact collisions", "Found one safe-task and two skill-name collisions", "fail", ["V6476-X1-N05"]),
            witness("V6476-M04-WPASS", "V6476-M04", "Rename collided surfaces and rerun the unchanged audit", "Return zero exact collisions", "Returned zero inherited and zero within-current collisions", "pass", ["V6476-X1-N05"]),
        ),
        (
            witness("V6476-M05-WFAIL", "V6476-M05", "Scan staged x1 bytes including scanner source", "Return zero x2-credit hits", "Matched the scanner source literal", "fail", ["V6476-X1-N06"]),
            witness("V6476-M05-WPASS", "V6476-M05", "Build the same target needle from byte fragments and rescan", "Return zero x2-credit hits", "Scanner source no longer self-matched and target semantics were unchanged", "pass", ["V6476-X1-N06"]),
        ),
    ]
    if not ledger.exists():
        subprocess.run([sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", d.PHASE, "--owner", d.OWNER], check=True)
    existing_ids = {row["method_id"] for row in read_json(ledger).get("methods", [])}
    for method, (failed, passed) in zip(methods, witness_sets):
        if method["method_id"] in existing_ids:
            continue
        record_path = PHASE / f"method-flow/{method['method_id'].lower()}-method-record.json"
        fail_path = PHASE / f"method-flow/{failed['witness_id'].lower()}-witness.json"
        pass_path = PHASE / f"method-flow/{passed['witness_id'].lower()}-witness.json"
        write_json(record_path.relative_to(PHASE), method)
        write_json(fail_path.relative_to(PHASE), failed)
        write_json(pass_path.relative_to(PHASE), passed)
        subprocess.run([sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path)], check=True)
        subprocess.run([sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(fail_path)], check=True)
        subprocess.run([sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path)], check=True)
        subprocess.run([sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method["method_id"], "--state", "preferred", "--note", "Validated for the declared bounded trigger only"], check=True)
    subprocess.run([sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/method-flow-validation.json")], check=True)
    subprocess.run([sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md")], check=True)


def build() -> None:
    prior = prior_proposals()
    proposal_review = proposal_audit(prior)
    portfolio_review = portfolio_audit(prior_portfolio_titles())
    if not proposal_review["valid"]:
        raise RuntimeError(f"proposal collisions: {proposal_review['exact_collisions']}")
    if not portfolio_review["valid"]:
        raise RuntimeError(f"portfolio collisions: {portfolio_review['exact_collisions'][:10]} duplicates={portfolio_review['within_current_duplicates']}")

    run_method_flow()
    method_state = read_json(PHASE / "method-flow/method-flow-state.json")
    if method_state.get("counts", {}).get("methods") != 5:
        raise RuntimeError("Method Flow method count is not five")
    if method_state.get("counts", {}).get("witness_results") != {"fail": 5, "pass": 5}:
        raise RuntimeError("Method Flow failed/passing witness parity is incomplete")

    write_json("identity-receipt.json", {
        "schema": "ghc.family.v647-v6.identity.v1", "phase": d.PHASE, "owner": d.OWNER,
        "pronouns": d.PRONOUNS, "relational_working_role": d.ROLE, "hope": d.HOPE,
        "identity_boundary": d.IDENTITY_BOUNDARY, "independent_authority": False,
    })
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v647-v6.startup.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source_phase": d.SOURCE_PHASE, "source_branch": d.SOURCE_BRANCH, "source_revision": d.SOURCE_REVISION,
        "source_inherited_revision": d.SOURCE_INHERITED_REVISION, "source_x1_revision": d.SOURCE_X1_REVISION,
        "source_evidence_revision": d.SOURCE_EVIDENCE_REVISION, "source_ancestry_verified": True,
        "source_remote_equality_verified": True, "source_clean": True, "source_phase_commit_count": 3,
        "source_merge_count": 0, "source_final_parent_count": 1, "source_current_validation": {"tests": 33, "detailed": 46, "minimal": 20, "json": 123, "privacy_files": 172, "privacy_hits": 0},
        "ilyra_fast_forward_only": True, "ilyra_remote_equality_after_fast_forward": True,
        "no_merge": True, "no_reset": True, "no_force_push": True, "no_sibling_mutation": True,
        "validation_mode": "canonical plus exactly one later local-only named replay; never detached",
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v647-v6.versions.v1", "verification_only": True,
        "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0", "chatgpt_desktop": "1.2026.190.0",
        "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8875",
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "windows_feature_changed": False, "unrelated_software_installed": False, "rebooted": False,
    })
    write_json("environment/rotation-guard.json", {
        "schema": "ghc.family.v647-v6.rotation.v1", "owner_generated_threshold": 15000,
        "scope": "new Ilyra owner-generated files only", "inherited_files_are_trigger": False,
        "replacement_required_at_x1": False, "decision": "continue_existing_clean_canonical_lane",
    })
    write_json("focus/primary-focus-receipt.json", {
        "schema": "ghc.family.v647-v6.focus.v1", "primary_focus": d.PRIMARY_FOCUS,
        "bounded_human_practice": d.BOUNDED_PRACTICE,
        "practice_boundary": "Synthetic learning and design lens only; no employment, qualification, forecasting competence, meteorological authority, warning authority, emergency authority, public-safety authority, legal authority, cultural authority, Māori authority, participant evidence, or affected-party authorization.",
        "other_pillars_visible": ["THOS Body", "Freed ID/CBR Heart"],
    })
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v647-v6.source-ledger.v1", "phase": d.PHASE, "source_count": len(d.SOURCES),
        "status_counts": dict(Counter(row["status"] for row in d.SOURCES)), "sources": d.SOURCES,
        "real_rows": 0, "real_people_or_operations": 0, "real_keys_or_tokens": 0,
        "authority_delegated": False, "network_execution_credit": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    source_lines = ["# v647-v6 source ledger", "", "Official and primary sources bound the x1 designs; they do not supply real observations, participants, keys, authority, or outcome evidence.", ""]
    source_lines.extend(f"- **{row['source_id']} — {row['title']}** ({row['status']}): {row['url']} — {row['use']}" for row in d.SOURCES)
    write_text("sources/source-ledger.md", "\n".join(source_lines))

    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v647-v6.prior-proposal-index.v1", "count": len(prior), "prior_proposals": prior})
    write_json("provenance/prior-proposal-collision-audit.json", proposal_review)
    write_json("provenance/prior-portfolio-collision-audit.json", portfolio_review)
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v647-v6.x1-proposals.v1", "phase": d.PHASE, "owner": d.OWNER,
        "freeze_stage": "x1_only", "x2_execution_present": False,
        "prior_frozen_proposal_count": d.PRIOR_FROZEN_PROPOSALS, "new_frozen_proposal_count": 10,
        "frozen_chain_count_after_x1": d.PRIOR_FROZEN_PROPOSALS + 10,
        "allowed_outcome_classes": d.OUTCOME_CLASSES,
        "expected_distribution": dict(Counter(row["expected_disposition"] for row in d.PROPOSALS)),
        "primary_focus": d.PRIMARY_FOCUS, "bounded_human_practice": d.BOUNDED_PRACTICE,
        "proposals": d.PROPOSALS, "boundary": d.TRUTH_BOUNDARY,
    })

    safe = task_rows("SAFE", d.SAFE_TASK_TITLES, "safe_now_owner_scoped")
    candidates = task_rows("CAND", d.CANDIDATE_TITLES, "candidate_bounded_prototype")
    exact = task_rows("EXACT", d.EXACT_PACKET_TITLES, "exact_approval_not_granted")
    blocked = task_rows("BLOCK", d.BLOCKED_PACKET_TITLES, "blocked_prohibited")
    write_json("approval-packets/x1-approval-portfolio.json", {
        "schema": "ghc.family.v647-v6.x1-approval-portfolio.v1", "phase": d.PHASE,
        "safe_now_count": len(safe), "candidate_count": len(candidates),
        "exact_approval_count": len(exact), "blocked_count": len(blocked),
        "safe_now": safe, "candidates": candidates, "exact_approval": exact, "blocked": blocked,
        "x2_completion_credit": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    skills = [
        {"skill_id": f"V6476-SKILL-{index:02d}", "name": name, "purpose": purpose, "x1_state": "planned_not_built", "x2_used": False}
        for index, (name, purpose) in enumerate(d.SKILL_SPECS, 1)
    ]
    runners = [
        {"runner_id": f"V6476-RUNNER-{index:02d}", "name": name, "x1_state": "planned_not_built", "x2_used": False}
        for index, name in enumerate(d.RUNNER_TITLES, 1)
    ]
    write_json("prototypes/x1-skill-runner-plan.json", {
        "schema": "ghc.family.v647-v6.x1-skill-runner-plan.v1", "skill_count": len(skills),
        "runner_count": len(runners), "skills": skills, "runners": runners,
        "skill_creator_used": True, "skill_creator_forward_testing": "not_used_because_user_prohibited_subagents",
        "x2_completion_credit": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    clean = task_rows("CLEAN", d.CLEAN_TASK_TITLES, "safe_now_additive_cleanup")
    write_json("maintenance/x1-clean-refine-plan.json", {
        "schema": "ghc.family.v647-v6.x1-clean-refine-plan.v1", "task_count": len(clean),
        "tasks": clean, "destructive_tasks": 0, "x2_completion_credit": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v647-v6.x1-gates.v1", "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
        "inherited_exact_gates": d.INHERITED_EXACT_GATES, "planned_new_open_gaps": 1,
        "planned_new_exact_gates": 1, "closed_in_x1": 0,
        "expected_after_x2_if_classified": {"open_gaps": d.INHERITED_OPEN_GAPS + 1, "exact_gates": d.INHERITED_EXACT_GATES + 1},
        "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v647-v6.x1-retained-negatives.v1", "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational_negative_count": len(d.X1_OPERATIONAL_NEGATIVES),
        "effective_x1_total": d.INHERITED_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES),
        "x1_operational_negatives": d.X1_OPERATIONAL_NEGATIVES, "erased_negative_count": 0,
        "synthetic_mutations_preregistered_for_x2": d.PREREGISTERED_SYNTHETIC_NEGATIVES,
        "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("orchestration/phase-update.json", {
        "schema": "ghc.family.v647-v6.phase-update.v1", "state": "X1_FREEZE_PENDING",
        "active_owner": d.OWNER, "standby_siblings": ["Eiren Kestrel", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "successor": "Sable Rook", "route_state": "PREPARED_NOT_SENT", "task_created": False,
        "subagent_spawned": False, "standby_sibling_messaged": False,
    })
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v647-v6.terminal-route-plan.v1", "target_existing_task_title": "Sable Rook",
        "target_phase": "v647-gmut-thos-v7-x1-x2", "state": "PREPARED_NOT_SENT",
        "send_gate": ["exact_final_clean", "commit_cap", "four_way_remote_equality", "one_named_replay_pass", "privacy_scan_zero_confirmed_hits"],
        "task_creation_authorized": False, "extra_confirmation_authorized": False,
    })
    write_json("reproduction/x1-freeze-contract.json", {
        "schema": "ghc.family.v647-v6.x1-freeze-contract.v1", "x1_only": True,
        "x2_implementation_present": False, "x2_outcome_present": False, "same_owner_replay_only": True,
        "independent_reproduction": False, "expected_frozen_proposal_count": 10,
    })
    prereg = [
        "# Ilyra Fen v647-v6 x1 preregistration",
        "",
        "This x1 freeze contains exactly ten proposal plans and the expanded portfolios. It contains no x2 implementation, outcome, completion credit, empirical observation, real participant evidence, production key, or delegated authority.",
        "",
        f"Primary Trinity Mandala focus: **{d.PRIMARY_FOCUS}**.",
        f"Bounded practice: **{d.BOUNDED_PRACTICE}**. This is a learning and synthetic-design lens only, not employment, qualification, competence, operational authority, warning authority, legal authority, cultural authority, Māori authority, or affected-party evidence.",
        "",
        "Expected core distribution after evidence: 6 completed, 2 represented, 1 open_gap, 1 exact_gate. These are expectations, not x1 outcomes.",
        "",
        d.TRUTH_BOUNDARY,
    ]
    write_text("x1-preregistration.md", "\n".join(prereg))

    write_json("validation/x1-operational-negatives.json", {
        "schema": "ghc.family.v647-v6.x1-operational-negatives.v1", "count": len(d.X1_OPERATIONAL_NEGATIVES),
        "negatives": d.X1_OPERATIONAL_NEGATIVES, "all_retained": True,
    })
    write_json("validation/x1-source-verification.json", {
        "schema": "ghc.family.v647-v6.x1-source-verification.v1", "expected_head": d.SOURCE_REVISION,
        "source_branch": d.SOURCE_BRANCH, "canonical_clean": True, "local_equals_upstream": True,
        "tracking_equals_local": True, "live_remote_equals_local": True, "divergence": {"ahead": 0, "behind": 0},
        "ancestry": {"source": True, "x1": True, "evidence": True}, "phase_commits": 3, "merge_commits": 0,
        "final_parent_count": 1, "current_validation_passed": True,
    })

    if len(d.PROPOSALS) != 10 or Counter(row["expected_disposition"] for row in d.PROPOSALS) != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError("proposal cardinality or expected distribution mismatch")
    if (len(d.SAFE_TASK_TITLES), len(d.CANDIDATE_TITLES), len(d.SKILL_SPECS), len(d.RUNNER_TITLES), len(d.CLEAN_TASK_TITLES)) != (30, 20, 20, 10, 30):
        raise RuntimeError("portfolio cardinality mismatch")


if __name__ == "__main__":
    build()
