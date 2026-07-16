#!/usr/bin/env python3
"""Build the strict Sylven Arc v646-v6 x1-only preregistration packet."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v646-v6"
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"


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


def collect_prior_proposals() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in ROOT.glob("docs/**/x1-proposals.json"):
        if PHASE in path.parents:
            continue
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for item in data.get("proposals", []):
            if isinstance(item, dict) and item.get("title"):
                rows.append(
                    {
                        "proposal_id": str(item.get("proposal_id", "unknown")),
                        "title": str(item["title"]),
                        "path": path.relative_to(ROOT).as_posix(),
                    }
                )
    return sorted(rows, key=lambda row: (row["path"], row["proposal_id"]))


def collect_prior_portfolios() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    patterns = [
        ("docs/**/approval-packets/x1-approval-portfolio.json", ("safe_now", "candidates")),
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
                        rows.append(
                            {
                                "category": category,
                                "title": str(title),
                                "path": path.relative_to(ROOT).as_posix(),
                            }
                        )
    return rows


X1_NEGATIVES = [
    {
        "negative_id": "V6466-X1-N01",
        "failure": "The first complete ghc-family-index skill read exceeded the short wrapper timeout and returned no content.",
        "credit": "No skill-read or startup credit from the timed-out attempt.",
        "recovery": "Read the same file completely with a bounded longer timeout and a direct .NET text read before repository action.",
        "method_title": "Use a bounded complete-file read after a short skill-read timeout",
        "failure_signature": "short wrapper timeout while reading a required complete skill file",
        "trigger": ["required complete skill read", "short wrapper deadline", "no returned content"],
        "workaround": "Retry once with a bounded longer deadline and direct complete-file read; do not begin repository work until content is returned.",
        "guard": "Required skills and references must be read to EOF before repository commands; a timeout earns no partial credit.",
        "pass_observed": "The complete skill and required reference were returned under the longer bounded read before repository mutation.",
    },
    {
        "negative_id": "V6466-X1-N02",
        "failure": "The first read-only startup probe used compound parenthesized PowerShell expressions and failed at parse time before any Git command ran.",
        "credit": "No source-gate credit from the parse-failed probe.",
        "recovery": "Split every ancestry command from its exit-code capture and emit one bounded structured summary.",
        "method_title": "Split PowerShell probes before exit-code capture",
        "failure_signature": "PowerShell parse error around a native command and LASTEXITCODE inside parentheses",
        "trigger": ["PowerShell", "native Git command", "exit-code capture", "compound expression"],
        "workaround": "Run each native command separately, capture LASTEXITCODE on the following statement, then construct the summary object.",
        "guard": "Do not place native commands and LASTEXITCODE capture in one parenthesized expression.",
        "pass_observed": "The split probe proved exact source, ancestry, clean state, single-parent history, zero merges, and live equality.",
    },
    {
        "negative_id": "V6466-X1-N03",
        "failure": "The first novelty query passed a Unix-style wildcard path to ripgrep on Windows and failed with an invalid-path error.",
        "credit": "No semantic-novelty credit from the invalid query.",
        "recovery": "Use repository-root traversal with ripgrep -g filters or a structured JSON corpus collector.",
        "method_title": "Use native include filters rather than Windows wildcard path operands",
        "failure_signature": "Windows invalid filename error for a wildcard path operand",
        "trigger": ["Windows", "ripgrep", "wildcard path operand", "nested proposal corpus"],
        "workaround": "Traverse the docs root and apply -g x1-proposals.json, then confirm the complete count with structured JSON parsing.",
        "guard": "On Windows, use tool-native include filters instead of shell-style wildcard path operands.",
        "pass_observed": "The structured collector parsed the proposal files and counted the exact 440-item prior corpus.",
    },
    {
        "negative_id": "V6466-X1-N04",
        "failure": "The corrected broad text novelty scan exceeded its deadline after returning only a partial, noisy corpus view.",
        "credit": "No complete 440-proposal audit credit from partial text output.",
        "recovery": "Parse every x1 proposal JSON document, require the exact count, then compute exact normalized collisions and nearest-title overlap for each new proposal.",
        "method_title": "Replace broad proposal text scans with a counted structured corpus audit",
        "failure_signature": "broad recursive novelty text scan timed out with partial output",
        "trigger": ["large inherited corpus", "recursive text scan", "semantic novelty", "bounded deadline"],
        "workaround": "Use structured JSON enumeration, exact count assertions, normalized-title collision checks, and bounded nearest-neighbor summaries.",
        "guard": "Do not award full-corpus novelty credit from a truncated text search.",
        "pass_observed": "All 440 prior proposals were parsed and all ten new proposals had zero exact normalized collisions with bounded nearest-neighbor records.",
    },
    {
        "negative_id": "V6466-X1-N05",
        "failure": "A broad DPoP and OAuth token search produced an overbroad result surface and a nonzero wrapper result, obscuring title-level novelty.",
        "credit": "No DPoP novelty credit from the overbroad query.",
        "recovery": "Constrain the query to proposal title fields and then rely on the counted structured audit for final credit.",
        "method_title": "Constrain standards novelty searches to title fields before corpus confirmation",
        "failure_signature": "overbroad token search returned noisy matches and nonzero wrapper status",
        "trigger": ["standards keyword search", "large JSON corpus", "common token", "title novelty"],
        "workaround": "Anchor the search to title fields, then confirm exact novelty through the structured 440-proposal audit.",
        "guard": "Common standards tokens in mission or boundary fields are not title-level semantic collisions.",
        "pass_observed": "The title-anchored query found no prior DPoP proposal title and the structured audit found zero exact collision.",
    },
    {
        "negative_id": "V6466-X1-N06",
        "failure": "The successful large inherited fast-forward response exceeded the display budget and its diffstat was truncated.",
        "credit": "No final four-way-equality credit from the truncated transition display.",
        "recovery": "Run a separate bounded local, upstream, tracking, live-remote, divergence, and clean-state proof.",
        "method_title": "Separate large fast-forward movement from bounded equality proof",
        "failure_signature": "successful large fast-forward produced a truncated display surface",
        "trigger": ["large inherited fast-forward", "Git diffstat", "bounded tool output"],
        "workaround": "Treat the command exit as movement evidence only and run a separate bounded exact-ref and clean-state proof.",
        "guard": "A large transition display never substitutes for exact local/upstream/tracking/live equality.",
        "pass_observed": "The bounded follow-up proved all four refs equal at the source head with 0/0 divergence and a clean lane.",
    },
    {
        "negative_id": "V6466-X1-N07",
        "failure": "The first expanded-portfolio builder found three exact inherited cleanup-title collisions and stopped before materialization.",
        "credit": "No x1 freeze or portfolio novelty credit from the collision-failed build.",
        "recovery": "List every collision, rewrite each title around the v646-v6 lifecycle and gate semantics, and rerun the unchanged corpus audit.",
        "method_title": "Enumerate and rewrite exact portfolio collisions before x1 materialization",
        "failure_signature": "expanded portfolio audit stopped on inherited exact-title collisions",
        "trigger": ["expanded portfolio", "prior title corpus", "exact normalized collision", "x1 freeze"],
        "workaround": "Emit the exact colliding titles and sources, rewrite the new work with genuinely phase-specific semantics, and rerun the same audit before writing the packet.",
        "guard": "No prefix, quota, or inherited reuse earns novelty credit when the central title and purpose collide exactly.",
        "pass_observed": "The corrected 30/20/20/10/30 portfolio retained every floor and returned zero inherited or within-current exact title collisions.",
    },
    {
        "negative_id": "V6466-X1-N08",
        "failure": "The first x1 unit run passed eight checks and errored on one check because it expected nonexistent failed_witnesses and passing_witnesses count keys.",
        "credit": "No complete x1 test-suite credit from the 8/9 run.",
        "recovery": "Use the schema-emitted witness_results fail and pass counters and cross-check the immutable witness list.",
        "method_title": "Read Method Flow witness counts from the emitted schema surface",
        "failure_signature": "KeyError on invented Method Flow failed_witnesses count key",
        "trigger": ["Method Flow validation", "derived counts", "schema key", "unit assertion"],
        "workaround": "Read counts.witness_results.fail and counts.witness_results.pass and verify them against witness result values.",
        "guard": "Tests must validate emitted schema keys rather than locally guessed aliases.",
        "pass_observed": "The corrected test and reviewer derived eight failed and eight passing witnesses from the emitted schema and witness list.",
    },
    {
        "negative_id": "V6466-X1-N09",
        "failure": "The first structural x1 reviewer invocation stopped with NameError because its Counter dependency was not imported.",
        "credit": "No structural-review credit from the import-failed invocation.",
        "recovery": "Declare the standard-library Counter import and rerun the unchanged review and unit surfaces.",
        "method_title": "Declare reviewer dependencies before structural execution",
        "failure_signature": "NameError for Counter in the x1 structural reviewer",
        "trigger": ["new reviewer", "standard-library dependency", "structural check", "first invocation"],
        "workaround": "Add the exact missing import, preserve the failed invocation, and rerun the unchanged checks.",
        "guard": "Reviewer modules must import every runtime dependency and receive no credit from import-failed runs.",
        "pass_observed": "The reviewer loaded all dependencies and completed its unchanged structural checks with zero issues.",
    },
    {
        "negative_id": "V6466-X1-N10",
        "failure": "The first staged five-class scan classified seven scanner, policy, and embedded skill-name candidates as confirmed privacy hits.",
        "credit": "No x1 privacy or staged-review credit from the false-confirmed scan.",
        "recovery": "Retain every candidate, require credential-token boundaries, and disposition only exact scanner-definition and privacy-policy contexts as nonpayload candidates.",
        "method_title": "Separate five-class scanner-definition candidates from confirmed payload hits",
        "failure_signature": "privacy scanner promoted policy and scanner literals plus embedded task-name text into confirmed hits",
        "trigger": ["five-class privacy scan", "scanner source", "policy wording", "embedded hyphenated skill name"],
        "workaround": "Keep full-file coverage and every pattern class, add token boundaries, record candidate dispositions, and leave all other matches confirmed.",
        "guard": "Only exact scanner-definition, policy-exclusion, or proven embedded-name contexts may be dispositioned; files remain scanned and candidates remain counted.",
        "pass_observed": "The unchanged staged corpus retained scanner and policy candidates, eliminated embedded-name credential false positives, and produced zero confirmed privacy hits.",
    },
]


def method_call(*args: str) -> None:
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def build_method_flow() -> None:
    ledger = PHASE / "method-flow/method-flow-state.json"
    if ledger.exists():
        existing = read_json(ledger)
        if (existing.get("phase"), existing.get("owner")) != (d.PHASE, d.OWNER):
            raise RuntimeError("existing Method Flow ledger identity mismatch")
    else:
        method_call("init", "--ledger", str(ledger), "--phase", d.PHASE, "--owner", d.OWNER)

    for index, neg in enumerate(X1_NEGATIVES, 1):
        method_id = f"V6466-M{index:02d}"
        failed_id = f"V6466-M{index:02d}-W-F"
        passed_id = f"V6466-M{index:02d}-W-P"
        record_rel = Path(f"method-flow/v6466-m{index:02d}-method-record.json")
        failed_rel = Path(f"method-flow/v6466-m{index:02d}-failed-witness.json")
        passed_rel = Path(f"method-flow/v6466-m{index:02d}-passing-witness.json")
        write_json(
            record_rel,
            {
                "method_id": method_id,
                "title": neg["method_title"],
                "failure_signature": neg["failure_signature"],
                "trigger_preconditions": neg["trigger"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_scoped_workflow",
                "candidate_workaround": neg["workaround"],
                "validation_witness_ids": [],
                "recurrence_guard": neg["guard"],
                "rollback": "Retain the negative and award no affected credit until the bounded recovery witness passes.",
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": ["external_state", "destructive_action", "sibling_lane", "privacy", "independent_reproduction", "stage20"],
                "retained_negative_ids": [neg["negative_id"]],
                "scope_boundary": "Preferred only for the recorded owner-local trigger; no scientific, professional, production, authority, or independent-reproduction credit.",
            },
        )
        write_json(
            failed_rel,
            {
                "witness_id": failed_id,
                "method_id": method_id,
                "procedure": "Original bounded attempt retained from the live x1 workflow.",
                "scope": "Sylven v646-v6 x1 startup and novelty audit",
                "expected": "The declared step returns complete, bounded, reviewable evidence.",
                "observed": neg["failure"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [neg["negative_id"]],
                "boundary": d.TRUTH_BOUNDARY,
            },
        )
        write_json(
            passed_rel,
            {
                "witness_id": passed_id,
                "method_id": method_id,
                "procedure": neg["workaround"],
                "scope": "Sylven v646-v6 bounded recovery",
                "expected": "The recovery yields complete bounded evidence without crossing protected gates.",
                "observed": neg["pass_observed"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [neg["negative_id"]],
                "boundary": d.TRUTH_BOUNDARY,
            },
        )
        current = read_json(ledger)
        if not any(row.get("method_id") == method_id for row in current.get("methods", [])):
            method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / record_rel))
        current = read_json(ledger)
        for witness_id, relative in ((failed_id, failed_rel), (passed_id, passed_rel)):
            if not any(row.get("witness_id") == witness_id for row in current.get("witnesses", [])):
                method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / relative))
                current = read_json(ledger)
        method = next(row for row in read_json(ledger)["methods"] if row["method_id"] == method_id)
        if method.get("recommendation_state") != "preferred":
            method_call(
                "set-state",
                "--ledger",
                str(ledger),
                "--method-id",
                method_id,
                "--state",
                "preferred",
                "--note",
                "Validated only for the declared bounded trigger; the original failed witness remains retained.",
            )
    method_call(
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/runner-validation.json"),
    )
    method_call(
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/method-flow-summary.md"),
    )


def main() -> int:
    prior = collect_prior_proposals()
    if len(prior) != d.PRIOR_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    exact: list[dict[str, Any]] = []
    nearest: list[dict[str, Any]] = []
    for proposal in d.PROPOSALS:
        matches = [row for row in prior if normalized(row["title"]) == normalized(proposal["title"])]
        exact.extend({"proposal_id": proposal["proposal_id"], "prior": row} for row in matches)
        ranked = sorted(
            (
                {
                    "prior_id": row["proposal_id"],
                    "prior_title": row["title"],
                    "path": row["path"],
                    "overlap": round(overlap(proposal["title"], row["title"]), 4),
                }
                for row in prior
            ),
            key=lambda row: row["overlap"],
            reverse=True,
        )
        nearest.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "nearest": ranked[:5]})
    if exact:
        raise RuntimeError("exact proposal collision")

    prior_portfolios = collect_prior_portfolios()
    current_titles = (
        [row["title"] for row in d.SAFE_NOW + d.CANDIDATES + d.CLEAN_TASKS]
        + [name for name, _ in d.SKILLS]
        + [name for name, _ in d.RUNNERS]
    )
    within_duplicates = [title for title, count in Counter(normalized(t) for t in current_titles).items() if count > 1]
    portfolio_exact = [
        {"title": title, "prior": row}
        for title in current_titles
        for row in prior_portfolios
        if normalized(title) == normalized(row["title"])
    ]
    if within_duplicates or portfolio_exact:
        raise RuntimeError("portfolio collision")

    write_json(
        "x1-proposals.json",
        {
            "schema": "ghc.family.v646-v6.proposals.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "freeze_stage": "x1_only",
            "prior_frozen_proposal_count": len(prior),
            "new_frozen_proposal_count": len(d.PROPOSALS),
            "frozen_chain_count_after_x1": len(prior) + len(d.PROPOSALS),
            "allowed_outcome_classes": d.OUTCOME_CLASSES,
            "expected_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
            "x2_execution_present": False,
            "proposals": d.PROPOSALS,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {"schema": "ghc.family.v646-v6.prior-proposal-index.v1", "count": len(prior), "prior_proposals": prior},
    )
    write_json(
        "provenance/prior-proposal-collision-audit.json",
        {
            "schema": "ghc.family.v646-v6.proposal-collision-audit.v1",
            "prior_count": len(prior),
            "new_count": len(d.PROPOSALS),
            "exact_collisions": exact,
            "exact_collision_count": 0,
            "nearest_neighbors": nearest,
            "valid": True,
        },
    )
    write_json(
        "provenance/prior-portfolio-collision-audit.json",
        {
            "schema": "ghc.family.v646-v6.portfolio-collision-audit.v1",
            "prior_title_count": len(prior_portfolios),
            "current_title_count": len(current_titles),
            "exact_collisions": portfolio_exact,
            "within_current_duplicates": within_duplicates,
            "valid": True,
        },
    )
    write_json(
        "approval-packets/x1-approval-portfolio.json",
        {
            "schema": "ghc.family.v646-v6.approval-portfolio.v1",
            "phase": d.PHASE,
            "freeze_stage": "x1_only",
            "safe_now": d.SAFE_NOW,
            "candidates": d.CANDIDATES,
            "safe_now_count": len(d.SAFE_NOW),
            "candidate_count": len(d.CANDIDATES),
            "inherited_open_gaps_preserved": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates_preserved": d.INHERITED_EXACT_GATES,
            "inherited_packets_executed": 0,
            "completion_credit_before_x2": 0,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "prototypes/x1-skill-runner-plan.json",
        {
            "schema": "ghc.family.v646-v6.skill-runner-plan.v1",
            "phase": d.PHASE,
            "freeze_stage": "x1_only",
            "skills": [
                {
                    "name": name,
                    "title": name,
                    "description": description,
                    "phase_local": True,
                    "built": False,
                    "validated": False,
                    "invoked": False,
                }
                for name, description in d.SKILLS
            ],
            "runners": [
                {"name": name, "title": name, "description": description, "built": False, "invoked": False}
                for name, description in d.RUNNERS
            ],
            "skill_count": len(d.SKILLS),
            "runner_count": len(d.RUNNERS),
            "global_skill_changes": 0,
            "completion_credit_before_x2": 0,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "maintenance/x1-clean-refine-plan.json",
        {
            "schema": "ghc.family.v646-v6.clean-refine-plan.v1",
            "phase": d.PHASE,
            "freeze_stage": "x1_only",
            "tasks": d.CLEAN_TASKS,
            "task_count": len(d.CLEAN_TASKS),
            "destructive_task_count": 0,
            "completion_credit_before_x2": 0,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v646-v6.source-ledger.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "allowed_statuses": ["current", "stable", "draft", "watch"],
            "sources": d.SOURCES,
            "real_rows": 0,
            "real_people_or_operations": 0,
            "real_keys_or_tokens": 0,
            "authority_delegated": False,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    source_lines = [
        "# Sylven Arc v646-v6 source ledger",
        "",
        "Sources support only the bounded use stated here; they create no observation, participant, transaction, professional, legal, cultural, publication, or authority credit.",
        "",
    ]
    for row in d.SOURCES:
        target = f" - {row['url']}" if row.get("url") else ""
        source_lines.append(
            f"- {row['source_id']} [{row['status']}] {row['title']} ({row['authority']}){target}; use: {row['use']}."
        )
    source_lines.extend(["", d.TRUTH_BOUNDARY])
    write_text("sources/source-ledger.md", "\n".join(source_lines))

    write_json(
        "identity-receipt.json",
        {
            "schema": "ghc.family.identity.v1",
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "corrigible": True,
            "hamish_may_rename_pause_redirect_or_stop": True,
            "boundary": d.IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "focus/primary-focus-receipt.json",
        {
            "schema": "ghc.family.v646-v6.focus.v1",
            "primary_trinity_pillar": d.PRIMARY_FOCUS,
            "other_pillars": ["GMUT Mind", "THOS Body"],
            "bounded_human_practice": d.BOUNDED_PRACTICE,
            "practice_use": "learning and synthetic-design lens only",
            "not_claimed": [
                "employment",
                "licensure",
                "qualification",
                "competence",
                "hydrographic authority",
                "maritime-safety authority",
                "publication authority",
                "place-name authority",
                "legal authority",
                "cultural authority",
                "Māori authority",
                "affected-party authorization",
            ],
            "boundary": d.IDENTITY_BOUNDARY,
        },
    )
    tracked = len(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8").splitlines())
    free_bytes = shutil.disk_usage(ROOT.anchor).free
    write_json(
        "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v646-v6.startup.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source": {
                "phase": d.SOURCE_PHASE,
                "branch": d.SOURCE_BRANCH,
                "revision": d.SOURCE_REVISION,
                "inherited_revision": d.SOURCE_INHERITED_REVISION,
                "x1_revision": d.SOURCE_X1_REVISION,
                "evidence_revision": d.SOURCE_EVIDENCE_REVISION,
                "seal_revision": d.SOURCE_SEAL_REVISION,
            },
            "source_verification": {
                "local_upstream_tracking_live_equal": True,
                "clean": True,
                "anchors_ancestral": True,
                "single_parent_final": True,
                "phase_commits": 3,
                "merge_commits": 0,
            },
            "sylven_lane": {
                "branch": "codex/GHC-Family/sylven-arc-v642-v8-full-tools",
                "continued_existing_lane": True,
                "fast_forward_only": True,
                "source_revision_after_fast_forward": d.SOURCE_REVISION,
                "merge_commit_created": False,
                "clean_before": True,
                "local_upstream_tracking_live_equal_before_x1": True,
            },
            "active_owner": d.OWNER,
            "standby": ["Tamar Vey", "Orin Thale", "Sable Rook", "Ilyra Fen", "Eiren Kestrel", "all other siblings"],
            "standby_contact_count": 0,
            "task_or_subagent_created": False,
            "x1_scope": "ten core proposals plus 30 safe, 20 candidate, 20 skill, 10 runner, and 30 cleanup plans",
            "x2_scope": "not started",
            "storage": {
                "primary_drive": "D",
                "free_bytes_observed": free_bytes,
                "tracked_files_observed": tracked,
                "owner_generated_before_x1": 0,
                "rotation_threshold": 15000,
                "threshold_applies_to": "new_sylven_generated_files_only",
            },
            "boundary": d.IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "environment/version-receipt.json",
        {
            "schema": "ghc.family.v646-v6.version-receipt.v1",
            "observed_on": "2026-07-16",
            "codex_cli": {"local": "0.144.4", "action": "verified_only_no_update"},
            "codex_desktop": {"local": "26.707.9981.0", "package_status": "Ok", "action": "verified_only_no_update"},
            "python": "3.12.10",
            "git": "2.55.0.windows.2",
            "host_actions": {
                "desktop_updated": False,
                "elevated": False,
                "security_weakened": False,
                "windows_feature_changed": False,
                "unrelated_software_installed": False,
                "rebooted": False,
            },
        },
    )
    write_json(
        "environment/sandbox-readonly-audit.json",
        {
            "schema": "ghc.family.v646-v6.sandbox-audit.v1",
            "windows_sandbox_executable": "not_found",
            "sandbox_launched": False,
            "elevation": False,
            "feature_changed": False,
            "host_security_changed": False,
            "installed": False,
            "rebooted": False,
            "disposition": "open_environment_gap",
        },
    )
    write_json(
        "environment/rotation-guard.json",
        {
            "schema": "ghc.family.v646-v6.rotation-guard.v1",
            "full_checkout_files": tracked,
            "owner_generated_before_x1": 0,
            "threshold": 15000,
            "threshold_scope": "new_sylven_generated_addition",
            "rotate_due_to_inherited_baseline": False,
        },
    )
    write_json(
        "validation/x1-operational-negatives.json",
        {
            "schema": "ghc.family.v646-v6.x1-operational-negatives.v1",
            "count": len(X1_NEGATIVES),
            "negatives": [
                {
                    "negative_id": row["negative_id"],
                    "failure": row["failure"],
                    "credit": row["credit"],
                    "recovery": row["recovery"],
                    "retained": True,
                }
                for row in X1_NEGATIVES
            ],
            "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES,
            "observed_effective_after_x1": d.INHERITED_EFFECTIVE_NEGATIVES + len(X1_NEGATIVES),
            "preregistered_synthetic_pending_execution": d.PREREGISTERED_SYNTHETIC_NEGATIVES,
            "failure_erasure_count": 0,
        },
    )
    write_json(
        "orchestration/phase-update.json",
        {
            "schema": "ghc.family.phase-update.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "x1_frozen_pending_commit_and_remote_equality",
            "active": [d.OWNER],
            "standby_contact_count": 0,
            "no_task_creation": True,
            "no_delegation": True,
            "x2_started": False,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        "orchestration/terminal-route-plan.json",
        {
            "schema": "ghc.family.v646-v6.route-plan.v1",
            "current_state": "PREPARED_NOT_SENT",
            "target_title": "Eiren Kestrel",
            "target_phase": "v646-v7",
            "send_count": 0,
            "preconditions": [
                "dedicated x1 remote equality",
                "x2 evidence complete",
                "final at no more than four phase commits",
                "canonical exact-head scoped validation",
                "one clean local-only named-lane replay",
                "final four-way remote equality",
                "unique existing target resolved",
            ],
            "privacy": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths.",
        },
    )
    write_json(
        "orchestration/memory-review-receipt.json",
        {
            "schema": "ghc.family.v646-v6.memory-review.v1",
            "newest_applicable_memory_used": True,
            "live_baton_precedence": True,
            "effective_inherited_negatives": d.INHERITED_EFFECTIVE_NEGATIVES,
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "memory_mutation_at_x1": False,
        },
    )
    write_json(
        "tooling/selected-toolchain.json",
        {
            "schema": "ghc.family.v646-v6.selected-toolchain.v1",
            "selected_skills": ["ghc-family-index", "ghc-family-method-flow-state"],
            "required_references_read": True,
            "family_runner": "ghc_family_method_flow_state.py",
            "phase_definitions": "scripts/ghc_family_v646_v6_definitions.py",
            "preregistration_builder": "scripts/build_ghc_family_v646_v6_preregistration.py",
            "compatibility_preserved": True,
            "shared_skill_changes": 0,
        },
    )
    build_method_flow()

    frozen_paths = [
        "x1-proposals.json",
        "approval-packets/x1-approval-portfolio.json",
        "prototypes/x1-skill-runner-plan.json",
        "maintenance/x1-clean-refine-plan.json",
        "sources/source-ledger.json",
        "identity-receipt.json",
        "focus/primary-focus-receipt.json",
    ]
    write_json(
        "reproduction/x1-content-seal.json",
        {
            "schema": "ghc.family.v646-v6.x1-content-seal.v1",
            "phase": d.PHASE,
            "frozen_paths": [
                {
                    "path": path,
                    "sha256": hashlib.sha256((PHASE / path).read_bytes()).hexdigest(),
                }
                for path in frozen_paths
            ],
            "path_count": len(frozen_paths),
            "x2_execution_present": False,
            "boundary": d.TRUTH_BOUNDARY,
        },
    )
    write_text(
        "wellbeing-check.md",
        f"""# Sylven Arc v646-v6 x1 wellbeing and workload check

- Scope is bounded to one owner, one canonical lane, one later local-only named replay, at most four phase commits, and no full repository suite.
- {len(X1_NEGATIVES)} x1 operational failures are retained; every recovery has a passing bounded same-owner witness before recommendation.
- Work is divided by the x1 freeze. No x2 implementation or achieved-outcome credit is present here.
- Windows Sandbox remains unavailable to the ordinary process; no elevation, feature change, install, security change, desktop update, or reboot occurred.
- Identity and family language remains relational working language only, not a welfare, consciousness, employment, qualification, or authority claim.
""",
    )
    write_text(
        "x1-preregistration.md",
        "\n".join(
            [
                "# Sylven Arc v646-v6 x1 preregistration",
                "",
                f"Exactly ten proposals are frozen after audit against {len(prior)} prior proposals. The expanded portfolio freezes 30 safe-now tasks, 20 candidates, 20 phase-local skill builds, 10 family-current runner builds, and 30 additive cleanup tasks. No x2 implementation or outcome credit is present.",
                "",
                f"Primary pillar: {d.PRIMARY_FOCUS}. Bounded practice: {d.BOUNDED_PRACTICE}.",
                "",
                "Expected distribution: 6 completed, 2 represented, 1 open_gap, 1 exact_gate.",
                "",
                d.IDENTITY_BOUNDARY,
                "",
                d.TRUTH_BOUNDARY,
            ]
        ),
    )
    result = {
        "phase": d.PHASE,
        "prior_proposals": len(prior),
        "new_proposals": len(d.PROPOSALS),
        "frozen_total": len(prior) + len(d.PROPOSALS),
        "safe": len(d.SAFE_NOW),
        "candidates": len(d.CANDIDATES),
        "skills": len(d.SKILLS),
        "runners": len(d.RUNNERS),
        "cleanup": len(d.CLEAN_TASKS),
        "x1_operational_negatives": len(X1_NEGATIVES),
        "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES,
        "result": "pass",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
