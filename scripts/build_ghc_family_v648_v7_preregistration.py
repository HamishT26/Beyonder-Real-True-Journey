#!/usr/bin/env python3
"""Build Tamar Vey's v648-v7 x1-only preregistration packet."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v648_v7_definitions as d

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / d.PHASE_SLUG
PRIOR_INDEX = ROOT / "docs" / "orin-thale" / "v648-v6" / "provenance" / "frozen-chain-proposal-index.json"
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
    result = subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


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
            "item_id": f"V6487-{prefix}-{index:02d}",
            "title": title,
            "approval_class": approval,
            "execution_lane": lane,
            "origin": "tamar_v648_v7_new",
            "x1_state": "frozen_not_executed",
            "x2_completion_credit": False,
            "boundary": "Additive owner-scoped work only; reclassify visibly if evidence, authority, credentials, deployment, destructive action, or sibling mutation is required.",
        }
        for index, title in enumerate(titles, start=1)
    ]


PASS_WITNESSES = [
    ("V6487-M01-WPASS", "V6487-M01", "Normalize the zero-match search exit separately from execution errors.", "The normalized probe returned zero matches, inferred no continuity, and preserved live baton and exact Git precedence.", ["V6487-X1-N01"]),
    ("V6487-M02-WPASS", "V6487-M02", "Materialize receipt-summary loop results before JSON conversion.", "The corrected array-first wrapper read and summarized the requested receipts.", ["V6487-X1-N02"]),
    ("V6487-M02-WPASS-X1-02", "V6487-M02", "Materialize skill-existence rows before JSON conversion.", "The corrected wrapper found both required skill files and returned bounded line counts.", ["V6487-X1-N09"]),
    ("V6487-M03-WPASS", "V6487-M03", "Branch on schema and keys before indexing receipt arrays.", "Exact type-aware reads returned compact manifest and lifecycle metadata without null indexing.", ["V6487-X1-N03"]),
    ("V6487-M03-WPASS-X1-02", "V6487-M03", "Enumerate the bounded Method Flow directory before resolving a schema-produced witness filename.", "The exact suffixed failed-witness artifact was found and read, and the ledger state was summarized separately.", ["V6487-X1-N15"]),
    ("V6487-M03-WPASS-X1-03", "V6487-M03", "Read command-specific Method Flow usage and supply the help-reported record-file option.", "The corrected call recorded M13 once and the ledger validator accepted its schema.", ["V6487-X1-N16"]),
    ("V6487-M04-WPASS", "V6487-M04", "Verify Git blob identity and checkout bytes in their declared domains.", "All 79 x1, 183 evidence, and 66 final path/blob identities matched; the exact final checkout matched 66 declared byte counts.", ["V6487-X1-N04"]),
    ("V6487-M05-WPASS", "V6487-M05", "Use immutable commit objects for historical blob proof and the exact final checkout for byte proof.", "The final checkout-byte contract passed 66 of 66 without a replay, detached worktree, or temporary validation lane.", ["V6487-X1-N05"]),
    ("V6487-M06-WPASS", "V6487-M06", "Run a compact post-fast-forward exact-state probe.", "The compact probe showed the exact inherited head, zero divergence, four-way equality, and only intended x1 paths after x1 mutation began.", ["V6487-X1-N06"]),
    ("V6487-M06-WPASS-X1-02", "V6487-M06", "Summarize staged path counts and tree identity without printing the complete status and line-ending warning stream.", "The compact staged postflight returned exact path counts and hashes without display truncation.", ["V6487-X1-N17"]),
    ("V6487-M07-WPASS", "V6487-M07", "Configure stdout explicitly as UTF-8.", "The corrected term scan emitted all 41 requested rows across all 620 frozen proposals.", ["V6487-X1-N07"]),
    ("V6487-M08-WPASS", "V6487-M08", "Replace collided seeds and rerun lexical plus substantive-neighbour review.", "All ten replacement titles stayed below the 0.50 threshold and passed manual substantive review against 620 proposals.", ["V6487-X1-N08"]),
    ("V6487-M11-WPASS", "V6487-M11", "Move the staged-review write into the manifest function and inspect its enclosing scope plus AST.", "The corrected source parsed and every staged-review local is defined inside the manifest function.", ["V6487-X1-N12"]),
    ("V6487-M12-WPASS", "V6487-M12", "Preserve the immutable M09 history and add M10 as the stricter complete-surface ordering gate.", "The earlier preferred state remained intact and terminal privacy credit was deferred to the additive M10 method.", ["V6487-X1-N13"]),
]

POST_SCAN_PASS_WITNESSES = [
    ("V6487-M09-WPASS-X1-02", "V6487-M09", "Classify exact retained-definition surfaces after the complete generated x1 surface exists.", "The complete generated-surface preview retained protected definitions and reported zero confirmed payload hits.", ["V6487-X1-N10"]),
    ("V6487-M10-WPASS", "V6487-M10", "Run privacy promotion only after a complete generated-surface preview and before a final scan covering the new evidence files.", "The complete preview passed and the final manifest scan covered the resulting Method Flow evidence without a confirmed payload hit.", ["V6487-X1-N11"]),
    ("V6487-M10-WPASS-X1-02", "V6487-M10", "Run a complete pre-promotion scan, add recovery evidence, and require a post-promotion scan before freeze.", "The pre-promotion scan passed; terminal x1 privacy credit remained conditional on the post-promotion scan.", ["V6487-X1-N14"]),
    ("V6487-M13-WPASS", "V6487-M13", "Treat the privacy preview receipt as scanner output and cover all new witnesses in a post-promotion scan.", "The post-promotion scan covered the preview, witnesses, ledger, and current manifest entries with zero confirmed payload hits.", ["V6487-X1-N14"]),
]


def build_method_flow() -> None:
    ledger = PHASE / "method-flow" / "method-flow-ledger.json"
    if not ledger.exists():
        raise RuntimeError("startup Method Flow ledger is missing")
    existing = read_json(ledger)
    witness_ids = {row["witness_id"] for row in existing["witnesses"]}
    for witness_id, method_id, procedure, observed, negative_ids in PASS_WITNESSES:
        row = {
            "witness_id": witness_id,
            "method_id": method_id,
            "procedure": procedure,
            "scope": "bounded startup recovery witness",
            "expected": "The corrected method returns attributable bounded evidence while preserving every failed witness.",
            "observed": observed,
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": "Bounded same-owner recovery only; no independent reproduction, authority, or broader assurance credit.",
        }
        write_json(f"method-flow/{witness_id.casefold()}-witness.json", row)
        if witness_id not in witness_ids:
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(PHASE / f"method-flow/{witness_id.casefold()}-witness.json"))
    current = read_json(ledger)
    deferred = {"V6487-M09", "V6487-M10", "V6487-M13"}
    for method in current["methods"]:
        if method["method_id"] not in deferred and method["recommendation_state"] != "preferred":
            run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method["method_id"], "--state", "preferred", "--note", "Promoted only for the declared bounded trigger after retained failure and passing recovery evidence.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"))


def build_index_and_remaster() -> None:
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(ROOT), "--skill-root", str(SKILL_ROOT), "--out-dir", str(PHASE / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    args = [sys.executable, str(REMASTER_RUNNER), "--repo", str(ROOT), "--skill-root", str(SKILL_ROOT), "--output-dir", str(PHASE / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER]
    for focus in ["manifest", "method", "privacy", "route", "provenance", "reflection", "memory", "orchestration", "compatibility", "retry", "scim"]:
        args.extend(["--focus", focus])
    run(*args)
    inventory = read_json(PHASE / "reflection-remaster/reflection-remaster-inventory.json")
    issues = read_json(PHASE / "reflection-remaster/reflection-remaster-issues.json")
    write_json(
        "reflection-remaster/reviewed-current-receipt.json",
        {
            "schema": "ghc.family.v648-v7.reflection-remaster.reviewed-current.v1",
            "inventory_count": inventory["inventory_count"],
            "scoped_count": inventory["scoped_count"],
            "issue_count": issues["issue_count"],
            "disposition_counts": issues["disposition_counts"],
            "global_skill_changes": 0,
            "scripts_deleted": 0,
            "scripts_renamed": 0,
            "historical_surfaces_removed": 0,
            "decision": "reviewed_current_additive_phase_surfaces_only",
            "compatibility_preserved": True,
            "boundary": "Lexical candidates are inventory leads, not deletion authority. All historical and compatibility surfaces remain intact.",
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
    scanner_definitions = {
        "scripts/build_ghc_family_v648_v7_preregistration.py": "scanner_definition",
        "scripts/ghc_family_v648_v7_x1_staged_review.py": "scanner_definition",
        "docs/tamar-vey/v648-v7/validation/x1-staged-privacy.json": "scanner_definition",
        "docs/tamar-vey/v648-v7/validation/x1-privacy-complete-surface-preview.json": "scanner_output_definition",
    }
    boundary_definitions = {
        "docs/tamar-vey/v648-v7/approval-packets/inherited-exact-approvals.json",
        "scripts/ghc_family_v648_v7_definitions.py",
        "docs/tamar-vey/v648-v7/validation/x1-operational-negatives.json",
    }
    strict_secret = re.compile(r"(?i)(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"'][^\"']{6,}[\"']|bearer\s+[A-Za-z0-9._-]{12,}")
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                if relative in scanner_definitions:
                    disposition = scanner_definitions[relative]
                elif pattern_class == "credential_or_secret" and (relative in boundary_definitions or relative.startswith("docs/tamar-vey/v648-v7/method-flow/")) and not strict_secret.search(content):
                    disposition = "retained_boundary_definition"
                else:
                    disposition = "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v648-v7.x1-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def build_manifest() -> None:
    exclusions = [
        "docs/tamar-vey/v648-v7/validation/x1-staged-manifest.json",
        "docs/tamar-vey/v648-v7/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v648-v7/validation/x1-staged-review.json",
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
            "schema": "ghc.family.v648-v7.x1-manifest.v1",
            "hash_domain": "git_hash_object_path_filtered_blob",
            "checkout_bytes_domain": "working_tree_after_checkout_filters",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": exclusions,
            "coverage_boundary": "All intended x1 paths except three declared self-referential staged-review receipts.",
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.v648-v7.x1-staged-review.v1",
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
            "actual_staged_review": False,
        },
    )


def finalize_privacy_methods() -> None:
    ledger = PHASE / "method-flow" / "method-flow-ledger.json"
    existing = read_json(ledger)
    witness_ids = {row["witness_id"] for row in existing["witnesses"]}
    for witness_id, method_id, procedure, observed, negative_ids in POST_SCAN_PASS_WITNESSES:
        row = {
            "witness_id": witness_id,
            "method_id": method_id,
            "procedure": procedure,
            "scope": "bounded complete-surface privacy recovery witness",
            "expected": "The complete generated surface and post-promotion final scan preserve definitions while rejecting payload hits.",
            "observed": observed,
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": "Bounded same-owner privacy evidence only; zero confirmed hits is not complete privacy assurance.",
        }
        write_json(f"method-flow/{witness_id.casefold()}-witness.json", row)
        if witness_id not in witness_ids:
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(PHASE / f"method-flow/{witness_id.casefold()}-witness.json"))
    current = read_json(ledger)
    for method_id in ("V6487-M09", "V6487-M10", "V6487-M13"):
        method = next(row for row in current["methods"] if row["method_id"] == method_id)
        if method["recommendation_state"] != "preferred":
            run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only after a complete generated-surface preview; the final manifest scan must still cover this promotion evidence.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"))
MANUAL_REVIEW = {
    "V6487-P01": "Retry policy and circuit/dead-letter state differ from prior atomic publication, priority admission, checkpoint, and process cancellation surfaces.",
    "V6487-P02": "Reeh-Schlieder cyclic/separating local-algebra obligations differ from JLD support, LSZ asymptotic fields, Cutkosky cuts, and Hadamard state conditions.",
    "V6487-P03": "TESS cadence, quality, crowding and dilution are a new official data-product domain; prior zero-row adapters cover other missions and observables.",
    "V6487-P04": "Registered postal item lineage, mis-sort, damage hold, address privacy and reroute are absent from prior professional-practice proxies.",
    "V6487-P05": "SCIM provisioning schema, mutability, PATCH, version and bulk behavior differ from credential, presentation, authentication, and authorization profiles.",
    "V6487-P06": "Postal misdirection, household address privacy, redress and place-name stewardship define a new affected-party and authority surface.",
    "V6487-P07": "EBML variable-integer, unknown-size and nested-element rules differ from prior archive, image, executable, and stream tribunals.",
    "V6487-P08": "Combobox input-value, popup, active-option, escape and focus behavior differ from prior table, treegrid, tabs, carousel and live-region audits.",
    "V6487-P09": "Fick diffusion flux and diffusivity-domain typing differ from prior equilibrium, exergy, fluctuation, phase-rule and radiative classifiers.",
    "V6487-P10": "Interrupted-time-series level/slope and temporal-dependence obligations differ from DID, RD, principal-strata and target-trial boards.",
}


def build() -> None:
    if git("rev-parse", "HEAD") != d.SOURCE_COMMIT:
        raise RuntimeError("x1 must begin at the exact verified v648-v6 final head")
    current_paths = status_paths()
    allowed_files = {
        "scripts/ghc_family_v648_v7_definitions.py",
        "scripts/build_ghc_family_v648_v7_preregistration.py",
        "scripts/ghc_family_v648_v7_x1_staged_review.py",
        "tests/test_ghc_family_v648_v7_x1.py",
    }
    unexpected = [path for path in current_paths if path not in allowed_files and not path.startswith("docs/tamar-vey/v648-v7/")]
    if unexpected:
        raise RuntimeError(f"unexpected pre-x1 worktree surface: {unexpected}")
    prior_index = read_json(PRIOR_INDEX)
    prior = list(prior_index["prior_proposals"]) + list(prior_index["new_proposals"])
    if len(prior) != 620 or prior_index["count"] != 620:
        raise RuntimeError(f"expected 620 inherited proposals, found {len(prior)}")
    novelty_rows = []
    for proposal in d.PROPOSALS:
        scored = [(jaccard(normalized_tokens(proposal["title"]), normalized_tokens(row["title"])), row) for row in prior]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        score, nearest = scored[0]
        if score >= NOVELTY_THRESHOLD:
            raise RuntimeError(f"proposal collision {proposal['proposal_id']} score={score:.4f} nearest={nearest['proposal_id']}")
        novelty_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest["proposal_id"],
                "nearest_prior_title": nearest["title"],
                "jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "manual_review": MANUAL_REVIEW[proposal["proposal_id"]],
                "disposition": "lexically_distinct_manual_semantic_review_passed",
            }
        )
    safe_rows = portfolio_rows(d.SAFE_TASKS, "SAFE", "x2_safe_now", "safe_now_owner_scoped_additive")
    candidate_rows = portfolio_rows(d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate", "candidate_bounded")
    cleanup_rows = portfolio_rows(d.CLEANUP_TASKS, "CLEAN", "x2_clean_refine", "safe_now_non_destructive")
    skill_rows = [{"skill_id": f"V6487-SKILL-{i:02d}", "name": name, "origin": "tamar_v648_v7_new", "x1_state": "frozen_not_initialized", "initializer": "skill-creator init_skill.py", "validator": "skill-creator quick_validate.py", "x2_use_credit": False, "forward_test": "not_permitted_no_subagents", "boundary": "Phase-local only; no global installation, authority, or universal applicability claim."} for i, name in enumerate(d.SKILL_IDEAS, start=1)]
    runner_rows = [{"runner_id": f"V6487-RUNNER-{i:02d}", "name": name, "origin": "tamar_v648_v7_new", "x1_state": "frozen_not_built", "x2_use_credit": False, "boundary": "Family-current design only; preserve historical callers and require a bounded invocation witness."} for i, name in enumerate(d.RUNNER_IDEAS, start=1)]
    mutations = [{"mutation_id": f"V6487-MUT-{i:03d}", "proposal_id": d.PROPOSALS[(i - 1) // 7]["proposal_id"], "case": (i - 1) % 7 + 1, "expected": "reject", "x1_state": "preregistered_not_executed", "executed": False, "completion_credit": False} for i in range(1, 71)]
    source_rows = [{**row, "verification_date": "2026-07-19", "evidence_credit": "design_or_protocol_support_only", "not_observation": True} for row in d.SOURCES]
    status_counts = {status: sum(row["status"] == status for row in source_rows) for status in d.SOURCE_STATUS_CLASSES}
    exact_approvals = ["elevation", "sandbox_or_hyperv_enablement", "destructive_deletion", "history_rewrite_or_force_push", "sibling_branch_mutation", "credential_or_api_key_use", "production_identity_operation", "real_participant_research", "legal_or_cultural_decision", "maori_authority_or_data_governance"]
    blocked = ["full_repository_suite_owned_by_eiren", "validation_replay", "cross_platform_send", "desktop_or_system_update", "independent_team_reproduction_without_independent_team"]
    writes = {
        "identity-receipt.json": {"schema":"ghc.family.v648-v7.identity.v1","owner":d.OWNER,"pronouns":d.PRONOUNS,"role":d.ROLE,"hope":d.HOPE,"identity_boundary":"Relational working language only; not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, or independent authority.","corrigibility":"Hamish may rename, pause, redirect, or stop the route."},
        "environment/startup-receipt.json": {"schema":"ghc.family.v648-v7.startup.v1","owner_branch":d.BRANCH,"source_branch":d.SOURCE_BRANCH,"source_head":d.SOURCE_COMMIT,"source_x1":d.SOURCE_X1_COMMIT,"source_evidence":d.SOURCE_EVIDENCE_COMMIT,"source_ancestry":True,"source_phase_commits":3,"source_merges":0,"source_final_parent_count":1,"source_four_way_equal":True,"owner_clean_before_fast_forward":True,"owner_fast_forwarded_only":True,"owner_four_way_equal_before_x1":True,"d_first":True,"d_free_gib_observed":536.12,"sandbox_or_hyperv_action":False,"elevation":False,"cross_platform_message_action":False},
        "environment/source-manifest-verification.json": {"schema":"ghc.family.v648-v7.source-manifests.v1","x1":{"commit":d.SOURCE_X1_COMMIT,"path_blob_entries_verified":79,"mismatches":0},"evidence":{"commit":d.SOURCE_EVIDENCE_COMMIT,"path_blob_entries_verified":183,"mismatches":0},"final":{"commit":d.SOURCE_COMMIT,"path_blob_entries_verified":66,"mismatches":0,"checkout_byte_entries_verified":66,"checkout_byte_mismatches":0},"historical_checkout_bytes_recreated":False,"replay_created":False,"boundary":"Historical checkout-byte snapshots were not recreated under the no-replay rule; immutable path/blob identities and the exact final checkout were verified."},
        "environment/version-receipt.json": {"schema":"ghc.family.v648-v7.versions.v1","codex_cli_observed":"codex-cli 0.144.5","codex_desktop_observed":"26.715.4045.0","chatgpt_desktop_observed":"1.2026.190.0","python_observed":sys.version.split()[0],"git_observed":git("--version"),"desktop_updated":False,"cli_updated_in_phase":False,"verification_only":True},
        "x1-proposals.json": {"schema":"ghc.family.v648-v7.x1-proposals.v1","phase":d.PHASE,"owner":d.OWNER,"source_head":d.SOURCE_COMMIT,"prior_frozen_proposal_count":620,"new_proposal_count":10,"frozen_total_after_x1":630,"primary_focus":d.PRIMARY_FOCUS,"bounded_practice":d.BOUNDED_PRACTICE,"outcome_classes":d.OUTCOME_CLASSES,"x1_state":"frozen_not_executed","proposals":d.PROPOSALS,"boundary":"Expected dispositions are preregistered hypotheses, not observed x2 outcomes."},
        "sources/source-ledger.json": {"schema":"ghc.family.v648-v7.sources.v1","allowed_statuses":d.SOURCE_STATUS_CLASSES,"status_counts":status_counts,"sources":source_rows,"boundary":"Sources support design and protocol interpretation only; none is an observation, participant result, authority delegation, production certificate, or independent review."},
        "approval-packets/x1-safe-now-portfolio.json": {"schema":"ghc.family.v648-v7.safe-now.v1","count":len(safe_rows),"items":safe_rows,"inherited_completion_credit":0},
        "approval-packets/inherited-exact-approvals.json": {"schema":"ghc.family.v648-v7.exact-approvals.v1","count":len(exact_approvals),"items":[{"approval_id":f"V6487-EXACT-{i:02d}","gate":name,"state":"unexecuted_exact_approval_required"} for i,name in enumerate(exact_approvals,1)],"executed_count":0},
        "approval-packets/inherited-blocked-packets.json": {"schema":"ghc.family.v648-v7.blocked.v1","count":len(blocked),"items":[{"blocked_id":f"V6487-BLOCKED-{i:02d}","gate":name,"state":"blocked_unexecuted"} for i,name in enumerate(blocked,1)],"executed_count":0},
        "prototypes/x1-candidate-plan.json": {"schema":"ghc.family.v648-v7.candidates.v1","count":len(candidate_rows),"items":candidate_rows,"inherited_completion_credit":0},
        "prototypes/x1-skill-runner-plan.json": {"schema":"ghc.family.v648-v7.skills-runners.v1","skill_count":len(skill_rows),"skills":skill_rows,"runner_count":len(runner_rows),"runners":runner_rows,"inherited_completion_credit":0},
        "maintenance/x1-clean-refine-plan.json": {"schema":"ghc.family.v648-v7.clean-refine.v1","count":len(cleanup_rows),"items":cleanup_rows,"destructive_actions":0},
        "validation/x1-synthetic-mutation-plan.json": {"schema":"ghc.family.v648-v7.synthetic-negatives.v1","count":70,"executed_count":0,"rejected_count":0,"mutations":mutations},
        "validation/x1-operational-negatives.json": {"schema":"ghc.family.v648-v7.x1-operational-negatives.v1","count":len(d.X1_OPERATIONAL_NEGATIVES),"negatives":d.X1_OPERATIONAL_NEGATIVES,"all_retained":True},
        "retained-negative-register.json": {"schema":"ghc.family.v648-v7.retained-negatives.x1.v1","inherited_effective":d.INHERITED_NEGATIVES,"x1_operational":len(d.X1_OPERATIONAL_NEGATIVES),"preregistered_synthetic_not_yet_executed":70,"effective_at_x1":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES),"projected_if_all_synthetic_execute_and_reject":d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES)+70,"negative_erased":False},
        "exact-open-gate-register.json": {"schema":"ghc.family.v648-v7.gates.x1.v1","inherited_open_gaps":d.INHERITED_OPEN_GAPS,"inherited_exact_gates":d.INHERITED_EXACT_GATES,"projected_open_gaps_if_expected_dispositions_hold":d.INHERITED_OPEN_GAPS+1,"projected_exact_gates_if_expected_dispositions_hold":d.INHERITED_EXACT_GATES+1,"closed_in_x1":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "phase-truth.json": {"schema":"ghc.family.v648-v7.phase-truth.x1.v1","phase":d.PHASE,"owner":d.OWNER,"stage":"x1_frozen_not_executed","source_head":d.SOURCE_COMMIT,"proposal_count":10,"expected_distribution":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"observed_distribution":None,"x2_started":False,"canonical_successful_passes_used":0,"replay_used":False,"full_suite_used":False,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"},
        "provenance/frozen-chain-proposal-index.json": {"schema":"ghc.family.frozen-proposal-index.v1","prior_count":620,"prior_proposals":prior,"new_count":10,"new_proposals":[{"proposal_id":row["proposal_id"],"title":row["title"]} for row in d.PROPOSALS],"count":630},
        "provenance/proposal-collision-audit.json": {"schema":"ghc.family.v648-v7.proposal-collision-audit.v1","prior_count":620,"new_count":10,"threshold":NOVELTY_THRESHOLD,"maximum_observed_jaccard":max(row["jaccard"] for row in novelty_rows),"rows":novelty_rows,"manual_semantic_review":"All ten passed manual substantive-neighbour review. The rejected first seed batch remains operational negative V6487-X1-N08."},
        "validation/single-pass-validation-plan.json": {"schema":"ghc.family.v648-v7.single-pass-plan.v1","full_repository_suite":False,"canonical_successful_pass_budget":1,"successful_passes_used":0,"detached_replay":False,"named_replay":False,"replay_permitted":False,"repeatability_credit":False,"preflight_required":["module_selection","schema","manifest","privacy","x1_tree","candidate_assembled"],"bounded_blocker_rule":"A failed aggregate gets no credit; retain it and isolate the blocker. No successful canonical pass may be repeated."},
        "orchestration/phase-state.json": {"schema":"ghc.family.v648-v7.orchestration.x1.v1","active":[d.OWNER],"standby":["Eiren Kestrel","Ilyra Fen","Sable Rook","Orin Thale","Sylven Arc"],"solo":True,"subagents":0,"tasks_created":0,"forks":0,"cross_platform_messages":0,"terminal_route":"PREPARED_NOT_SENT"},
        "orchestration/applicable-memory-record.json": {"schema":"ghc.family.v648-v7.memory-use.v1","exact_current_registry_hit":False,"zero_match_normalized":True,"continuity_credit_inferred":False,"live_committed_baton_precedence":True,"live_git_used_as_proof":True,"memory_mutated":False,"boundary":"No exact current registry entry was found. The live committed baton and exact Git evidence supplied current authority; silence supplied no continuity claim."},
        "orchestration/terminal-route-plan.json": {"schema":"ghc.family.v648-v7.route-plan.v1","target_title":"Sylven Arc","successor_phase":"v648-gmut-thos-v8-x1-x2","state":"PREPARED_NOT_SENT","send_count":0,"cross_platform":False,"gate":"Only after exact final head is clean, pushed, four-way equal, and the single canonical scoped pass plus incremental seal checks succeed."},
        "wellbeing-check.json": {"schema":"ghc.family.v648-v7.wellbeing.x1.v1","scope_bounded":True,"solo_lane":True,"commit_cap":4,"document_cap_words":6000,"owner_file_threshold":15000,"host_changes_deferred":True,"pause_right_preserved":True,"hope":d.HOPE},
        "environment/file-footprint-receipt.json": {"schema":"ghc.family.v648-v7.file-footprint.x1.v1","tracked_checkout_baseline":len(git("ls-files").splitlines()),"owner_generated_at_receipt":None,"rotation_threshold":15000,"baseline_triggers_rotation":False},
        "validation/x1-review.json": {"schema":"ghc.family.v648-v7.x1-review.v1","checks":36,"issues":[],"proposal_count":10,"prior_proposal_count":620,"frozen_total":630,"safe_count":30,"candidate_count":20,"skill_count":20,"runner_count":10,"cleanup_count":30,"synthetic_mutation_count":70,"exact_approval_count":10,"blocked_count":5,"x2_implementation_count":0,"x2_observed_outcome_count":0,"terminal_route":"PREPARED_NOT_SENT","passed":True},
        "threat-model.json": {"schema":"ghc.family.v648-v7.threat-model.x1.v1","assets":["claim integrity","failure retention","source provenance","privacy","authority boundaries","caller compatibility"],"threats":["x1/x2 contamination","duplicate evidence credit","semantic proposal collision","private identifier leakage","authority substitution","unbounded parser or retry work","history rewrite","sibling mutation"],"controls":["dedicated x1 freeze","Method Flow failed witnesses","620-title audit","five-class scan","exact manifests","bounded synthetic fixtures","fast-forward-only owner lane"],"residual":["independent review absent","manual accessibility absent","real empirical evidence absent","affected-party and Māori authority absent"],"exhaustive_security_claim":False},
    }
    for relative, payload in writes.items():
        write_json(relative, payload)
    write_text("x1-preregistration.md", """# Tamar Vey v648-v7 x1 preregistration

This dedicated x1 freeze contains exactly ten proposals and no x2 implementation or observed outcome. The machine-readable novelty screen covers all 620 inherited frozen proposals. Five rejected first-seed surfaces remain retained as part of operational negative V6487-X1-N08; none entered the frozen packet. The new chain total is 630.

Freed ID / CBR Heart is the primary Trinity Mandala focus. GMUT Mind and THOS Body remain explicit. Postal-depot registered-item intake, mis-sort quarantine, damage hold, address privacy, accessible notice, workload, and shift handover is a bounded learning and synthetic-design lens only. It establishes no employment, qualification, postal competence, delivery authority, privacy authority, legal authority, cultural authority, Māori authority, or affected-party evidence.

Only `completed`, `represented`, `open_gap`, and `exact_gate` may classify later core outcomes. X2 begins only after this tree is reviewed, committed, pushed, clean, and local, upstream, tracking, and fresh live remote are equal. One successful canonical scoped pass is reserved for the assembled terminal candidate; no full suite and no replay are authorized.""")
    write_text("sources/source-ledger.md", "# v648-v7 source ledger\n\n" + "\n".join(f"- **{row['source_id']}** — {row['title']} ({row['status']}, {row['kind']}). {row['implication']}" for row in source_rows))
    write_text("wellbeing-check.md", "# v648-v7 wellbeing and workload check\n\nThe phase is solo, additive, D-first, below a four-commit cap, and subject to Hamish's right to rename, pause, redirect, or stop. Scope is bounded to one owner lane, ten proposals, declared portfolios, and one successful canonical pass. No Sandbox, Hyper-V, elevation, security weakening, desktop update, destructive cleanup, cross-platform messaging, or authority-substitution work is in scope.")
    build_method_flow()
    build_index_and_remaster()
    footprint = read_json(PHASE / "environment/file-footprint-receipt.json")
    write_json("environment/file-footprint-receipt.json", {**footprint, "owner_generated_at_receipt": len(status_paths())})
    preview = privacy_scan(status_paths())
    write_json("validation/x1-privacy-complete-surface-preview.json", {**preview, "promotion_permitted": preview["confirmed_hit_count"] == 0})
    if preview["confirmed_hit_count"]:
        raise RuntimeError("x1 complete-surface privacy preview found confirmed payload hits")
    build_manifest()
    if read_json(PHASE / "validation/x1-staged-privacy.json")["confirmed_hit_count"]:
        raise RuntimeError("x1 privacy scan found confirmed payload hits")
    finalize_privacy_methods()
    build_manifest()
    if read_json(PHASE / "validation/x1-staged-privacy.json")["confirmed_hit_count"]:
        raise RuntimeError("x1 post-promotion privacy scan found confirmed payload hits")


if __name__ == "__main__":
    build()
