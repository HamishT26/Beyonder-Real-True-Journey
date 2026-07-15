#!/usr/bin/env python3
"""Build the Tamar Vey v645-v7 x1-only preregistration packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from ghc_family_v645_v7_definitions import (
    BATON_TIME_INHERITED_NEGATIVES,
    BOUNDED_PRACTICE,
    CANDIDATES,
    CLEAN_TASKS,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    POST_BATON_INHERITED_NEGATIVES,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    PRONOUNS,
    PROPOSALS,
    ROLE,
    RUNNERS,
    SAFE_NOW,
    SKILLS,
    SOURCE_BRANCH,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_INHERITED_REVISION,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_SEAL_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TRUTH_BOUNDARY,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/tamar-vey/v645-v7")
PHASE_DIR = ROOT / PHASE_REL
SOURCE_DIR = ROOT / "docs/orin-thale/v645-v6"
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE_DIR / relative
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
    active = (PHASE_DIR / "x1-proposals.json").resolve()
    for path in ROOT.glob("docs/**/x1-proposals.json"):
        if path.resolve() == active:
            continue
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for item in data.get("proposals", []):
            if isinstance(item, dict) and item.get("title"):
                rows.append({"proposal_id": str(item.get("proposal_id", "unknown")), "title": str(item["title"]), "path": path.relative_to(ROOT).as_posix()})
    return rows


def collect_prior_portfolios() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    patterns = [
        ("docs/**/approval-packets/x1-approval-portfolio.json", ("safe_now", "candidates")),
        ("docs/**/prototypes/x1-skill-runner-plan.json", ("skills", "runners")),
        ("docs/**/maintenance/x1-clean-refine-plan.json", ("tasks",)),
    ]
    for pattern, categories in patterns:
        for path in ROOT.glob(pattern):
            if PHASE_DIR in path.parents:
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
                        rows.append({"kind": category, "title": str(title), "path": path.relative_to(ROOT).as_posix()})
    return rows


INCIDENTS = [
    {
        "negative_id": "V6457-START-N01",
        "title": "Increase only the schema-read envelope after retaining the first timeout",
        "failure": "The first complete Method Flow schema read timed out after ten seconds and returned no schema content.",
        "fail_procedure": "Read the complete schema through a ten-second shell wrapper.",
        "fail_observed": "The wrapper timed out with no schema evidence.",
        "pass_procedure": "Use a thirty-second bounded file API read and require the full file plus metadata.",
        "pass_observed": "The complete 2,633-byte schema and file metadata were returned without changing the file.",
        "method": "Retain the timeout, widen only the read envelope, and require complete content before task action.",
        "guard": "Never infer schema content from silence or discard the first timed-out attempt.",
        "rollback": "Keep task action paused until a complete read succeeds.",
        "preconditions": ["required local schema", "first bounded read returned no content"],
    },
    {
        "negative_id": "V6457-START-N02",
        "title": "Split D-drive and worktree inventory after a silent composite timeout",
        "failure": "The combined drive, path, and worktree inventory exceeded thirty seconds and returned no output.",
        "fail_procedure": "Enumerate drive capacity, owned paths, and all linked worktrees in one shell call.",
        "fail_observed": "The wrapper timed out with no inventory evidence.",
        "pass_procedure": "Probe path and drive truth first, then source and owner Git state through separately bounded commands.",
        "pass_observed": "Both owned paths, D-drive headroom, clean branches, ancestry, and live equality were returned separately.",
        "method": "Decompose slow startup inventory into independently evidenced read-only probes.",
        "guard": "Do not rerun broad worktree enumeration when exact owned paths are already known.",
        "rollback": "Make no branch change until all required split probes pass.",
        "preconditions": ["large linked-worktree repository", "composite inventory returned no evidence"],
    },
    {
        "negative_id": "V6457-X1-N01",
        "title": "Avoid the PowerShell automatic Matches table in proposal-audit collections",
        "failure": "A proposal audit used the case-insensitive reserved Matches variable and could not append proposal objects.",
        "fail_procedure": "Accumulate matching proposal objects in a variable named matches.",
        "fail_observed": "PowerShell treated the automatic regular-expression hash table as the target and rejected object addition.",
        "pass_procedure": "Use a distinct foundRows collection and rerun the exact read-only proposal lookup.",
        "pass_observed": "Both prior constraint-propagation proposals were returned for semantic review.",
        "method": "Reserve automatic PowerShell variables and use explicit collection names in structured audits.",
        "guard": "Never use Matches as an accumulator after a regex condition.",
        "rollback": "Withdraw the failed query and rerun without changing repository artifacts.",
        "preconditions": ["Windows PowerShell", "regex-driven structured audit"],
    },
    {
        "negative_id": "V6457-X1-N02",
        "title": "Use search-discovered official pages after a direct URL safety rejection",
        "failure": "A direct Waitangi Tribunal URL open was rejected by the browser safety resolver and supplied no source evidence.",
        "fail_procedure": "Open an unverified direct official path through the browser resolver.",
        "fail_observed": "The resolver marked the URL unsafe to open and returned no page content.",
        "pass_procedure": "Search the official domain, select the indexed Wai 262 publication or release page, and preserve the authority boundary.",
        "pass_observed": "Official search results identified Ko Aotearoa Tenei and its culture, identity, taonga, and authority scope without a case decision.",
        "method": "Prefer search-discovered official pages when direct URL canonicalization is rejected.",
        "guard": "A rejected direct open is not evidence and must not be silently replaced by an assumed URL.",
        "rollback": "Retain the failed open and use no source claim until an official result is returned.",
        "preconditions": ["official public source needed", "direct browser open rejected"],
    },
    {
        "negative_id": "V6457-X1-N03",
        "title": "Inspect runner subcommand help after a zero-match source-code search",
        "failure": "A narrow source search assumed argparse labels that were not present in the repository wrapper and exited with no matches.",
        "fail_procedure": "Infer runner CLI structure from a narrow text pattern over the compatibility wrapper.",
        "fail_observed": "The search returned no lines and no CLI evidence.",
        "pass_procedure": "Invoke bounded help for init, record, witness, set-state, validate, and summarize subcommands.",
        "pass_observed": "All required arguments and allowed states were returned by the canonical runner itself.",
        "method": "Use executable help as the source of truth when a compatibility wrapper delegates implementation.",
        "guard": "Do not treat zero text matches as proof that a delegated CLI lacks a capability.",
        "rollback": "Withdraw the source-search inference and make no ledger call until help succeeds.",
        "preconditions": ["delegating compatibility wrapper", "narrow implementation search returned no matches"],
    },
    {
        "negative_id": "V6457-X1-N04",
        "title": "Let the passing-witness transition stand before preferred promotion",
        "failure": "The first x1 builder run recorded a passing witness that automatically promoted its method to validated, then attempted the invalid transition from validated to validated.",
        "fail_procedure": "Record a passing witness and then explicitly set the same method to validated again.",
        "fail_observed": "The canonical runner rejected the duplicate state transition and stopped the partial x1 build.",
        "pass_procedure": "Resume the retained partial ledger, recognize the runner-applied validated state, and transition directly to preferred before adding later methods.",
        "pass_observed": "The existing failure and passing witness remained intact, the method reached preferred once, and the remaining methods were appended without duplicate records.",
        "method": "Treat a passing witness as the validated transition and request only the next legal state.",
        "guard": "Re-read method state after every witness command before issuing an explicit transition.",
        "rollback": "Stop the builder, preserve the partial ledger, and resume without deleting or duplicating evidence.",
        "preconditions": ["canonical runner auto-promotes on passing witness", "builder requests an explicit state transition"],
    },
    {
        "negative_id": "V6457-X1-N05",
        "title": "Normalize only phase-local family-index checkout text after CRLF detection",
        "failure": "The family-index builder emitted its two owner-scoped outputs with CRLF checkout bytes, so x1 structural validation failed.",
        "fail_procedure": "Accept generated family-index checkout bytes without a post-generation byte audit.",
        "fail_observed": "The x1 reviewer reported CRLF in the JSON and Markdown index files while privacy and stale-label checks remained clean.",
        "pass_procedure": "Rewrite only those two phase-local files as UTF-8 LF with unchanged decoded text and rerun structural validation.",
        "pass_observed": "Both index files retained their decoded content and passed LF, UTF-8, privacy, and structural checks.",
        "method": "Audit generated owner-scoped text bytes and normalize line endings without changing semantic content.",
        "guard": "Never stage family-index outputs on Windows before checking CRLF and visible encoding.",
        "rollback": "Restore the generated phase-local outputs if normalization changes decoded text and retain the failure.",
        "preconditions": ["Windows family-index generation", "owner-scoped UTF-8 LF requirement"],
    },
    {
        "negative_id": "V6457-X1-N06",
        "title": "Return validation evidence from separate commands when one parallel child may fail",
        "failure": "A parallel wrapper launched reviewer and x1 tests, but the reviewer's nonzero result prevented the wrapper from returning the test output.",
        "fail_procedure": "Use a fail-fast parallel wrapper for two evidence-producing validation commands.",
        "fail_observed": "Only the failing reviewer output returned; the test result was unavailable and received no evidence credit.",
        "pass_procedure": "Run reviewer and dependency-free x1 tests as separately captured bounded commands after recovery.",
        "pass_observed": "Each command returned its own complete result and exit status, allowing independent bounded credit.",
        "method": "Separate evidence-producing validation commands when one expected failure could suppress another result.",
        "guard": "Parallelize only when the orchestration layer preserves every child result on partial failure.",
        "rollback": "Assign no credit to the suppressed run and rerun only the bounded validations independently.",
        "preconditions": ["multiple evidence-producing child commands", "wrapper may fail fast on one nonzero exit"],
    },
    {
        "negative_id": "V6457-X1-N07",
        "title": "Select the predecessor final test after its x2 artifacts exist",
        "failure": "The v645-v6 x1-stage test was run against Orin's completed x2 packet and correctly failed its no-x2-files assertion.",
        "fail_procedure": "Use a predecessor's historical x1-only test as a current final-packet validation entrypoint.",
        "fail_observed": "Nine of ten tests passed; the x1 separation test rejected the expected v645-v6 x2 files.",
        "pass_procedure": "Keep the historical x1 test unchanged and invoke the predecessor's final scoped test entrypoint for inherited-packet validation.",
        "pass_observed": "The final v645-v6 scoped tests ran against the completed predecessor packet without weakening x1 history.",
        "method": "Match a validation entrypoint to the artifact stage it was designed to test.",
        "guard": "Before invoking inherited tests, inspect whether the entrypoint asserts x1-only absence or final-packet presence.",
        "rollback": "Assign no credit to the stage-mismatched run and preserve both the test and completed predecessor artifacts.",
        "preconditions": ["completed predecessor x2 packet", "both x1-only and final scoped tests exist"],
    },
]


def method_record(index: int, incident: dict[str, Any]) -> dict[str, Any]:
    return {
        "method_id": f"V6457-M{index:02d}",
        "title": incident["title"],
        "failure_signature": incident["failure"],
        "trigger_preconditions": incident["preconditions"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_local_tooling",
        "candidate_workaround": incident["method"],
        "validation_witness_ids": [],
        "recurrence_guard": incident["guard"],
        "rollback": incident["rollback"],
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["private_material", "destructive_action", "sibling_lane", "host_change"],
        "retained_negative_ids": [incident["negative_id"]],
        "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
    }


def witness(index: int, incident: dict[str, Any], result: str) -> dict[str, Any]:
    passed = result == "pass"
    return {
        "witness_id": f"V6457-W{index:02d}-{'P' if passed else 'F'}",
        "method_id": f"V6457-M{index:02d}",
        "procedure": incident["pass_procedure"] if passed else incident["fail_procedure"],
        "scope": "single owner-local operational diagnostic",
        "expected": "bounded diagnostic or recovery completes without crossing protected gates",
        "observed": incident["pass_observed"] if passed else incident["fail_observed"],
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [incident["negative_id"]],
        "boundary": TRUTH_BOUNDARY,
    }


def method_call(*args: str) -> None:
    subprocess.run([sys.executable, str(METHOD_RUNNER), *args], cwd=ROOT, check=True)


def build_method_flow() -> None:
    ledger = PHASE_DIR / "method-flow/method-flow-state.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    if not ledger.exists():
        method_call("init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER)
    negatives: list[dict[str, Any]] = []
    for index, incident in enumerate(INCIDENTS, 1):
        record = method_record(index, incident)
        failed = witness(index, incident, "fail")
        passed = witness(index, incident, "pass")
        record_path = PHASE_DIR / f"method-flow/v6457-m{index:02d}-method-record.json"
        failed_path = PHASE_DIR / f"method-flow/v6457-w{index:02d}-f-witness.json"
        passed_path = PHASE_DIR / f"method-flow/v6457-w{index:02d}-p-witness.json"
        write_json(record_path.relative_to(PHASE_DIR), record)
        write_json(failed_path.relative_to(PHASE_DIR), failed)
        write_json(passed_path.relative_to(PHASE_DIR), passed)
        state = read_json(ledger)
        existing = {item["method_id"]: item for item in state.get("methods", [])}
        if record["method_id"] not in existing:
            method_call("record", "--ledger", str(ledger), "--record-file", str(record_path))
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(failed_path))
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(passed_path))
        state = read_json(ledger)
        current = next(item["recommendation_state"] for item in state["methods"] if item["method_id"] == record["method_id"])
        if current == "validated":
            method_call("set-state", "--ledger", str(ledger), "--method-id", record["method_id"], "--state", "preferred", "--note", "Preferred only for the declared trigger and same-owner operational scope")
        elif current != "preferred":
            raise SystemExit(f"unexpected Method Flow state for {record['method_id']}: {current}")
        negatives.append({
            "negative_id": incident["negative_id"],
            "stage": "startup_or_x1",
            "class": "operational",
            "summary": incident["failure"],
            "retained": True,
            "recovered": True,
            "method_id": record["method_id"],
            "failed_witness_id": failed["witness_id"],
            "passing_witness_id": passed["witness_id"],
            "independent_reproduction": False,
        })
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE_DIR / "method-flow/runner-validation.json"))
    method_call("summarize", "--ledger", str(ledger), "--json-output", str(PHASE_DIR / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE_DIR / "method-flow/method-flow-summary.md"))
    write_json("validation/x1-operational-negatives.json", {
        "schema": "ghc.family.v645-v7.operational-negatives.v1",
        "phase": PHASE,
        "stage": "x1",
        "baton_time_inherited": BATON_TIME_INHERITED_NEGATIVES,
        "post_baton_inherited": POST_BATON_INHERITED_NEGATIVES,
        "post_baton_inherited_ids": ["V6456-MEM-N01"],
        "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "preregistered_synthetic": PREREGISTERED_SYNTHETIC_NEGATIVES,
        "new_operational_count": len(negatives),
        "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + PREREGISTERED_SYNTHETIC_NEGATIVES + len(negatives),
        "negatives": negatives,
        "boundary": "Recovered failures remain retained. The later inherited read-only negative does not alter Orin's immutable final commit or permit a second route message.",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume-partial", action="store_true", help="Resume the retained partial x1 build after V6457-X1-N04")
    args = parser.parse_args()
    if PHASE_DIR.exists() and any(PHASE_DIR.rglob("*")) and not args.resume_partial:
        raise SystemExit("v645-v7 phase directory already contains files")
    if args.resume_partial and any((PHASE_DIR / name).exists() for name in ("phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json")):
        raise SystemExit("resume-partial refuses any x2 or closeout artifact")
    if not METHOD_RUNNER.is_file():
        raise SystemExit("family-current Method Flow runner is missing")

    prior = collect_prior_proposals()
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    prior_by_normal = {normalized(row["title"]): row for row in prior}
    comparisons: list[dict[str, Any]] = []
    exact: list[dict[str, Any]] = []
    for item in PROPOSALS:
        prior_hit = prior_by_normal.get(normalized(item["title"]))
        if prior_hit:
            exact.append({"proposal_id": item["proposal_id"], "prior": prior_hit})
        ranked = sorted(
            ({"proposal_id": row["proposal_id"], "title": row["title"], "score": round(overlap(item["title"], row["title"]), 3)} for row in prior),
            key=lambda row: (-row["score"], row["proposal_id"]),
        )[:5]
        comparisons.append({
            "proposal_id": item["proposal_id"],
            "title": item["title"],
            "exact_collision": bool(prior_hit),
            "top_token_overlaps": ranked,
            "mission_falsifier_evidence_recovery_review": "accepted_as_distinct_after_manual_review",
            "novelty_statement": item["novelty_against_370_frozen_proposals"],
        })
    if exact:
        raise SystemExit(f"proposal title collision: {exact}")

    portfolio_prior = collect_prior_portfolios()
    new_portfolio = [
        *[("safe_now", item["title"]) for item in SAFE_NOW],
        *[("candidates", item["title"]) for item in CANDIDATES],
        *[("skills", item[0]) for item in SKILLS],
        *[("runners", item[0]) for item in RUNNERS],
        *[("clean", item["title"]) for item in CLEAN_TASKS],
    ]
    prior_norm = {normalized(item["title"]): item for item in portfolio_prior}
    collisions = [{"kind": kind, "title": title, "prior": prior_norm[normalized(title)]} for kind, title in new_portfolio if normalized(title) in prior_norm]
    if collisions:
        raise SystemExit(f"portfolio title collision: {collisions}")

    source_portfolio = read_json(SOURCE_DIR / "approval-packets/x1-approval-portfolio.json")
    inherited_exact = deepcopy(source_portfolio["inherited_exact_packets"])
    inherited_blocked = deepcopy(source_portfolio["inherited_blocked_packets"])
    if len(inherited_exact) != 10 or len(inherited_blocked) != 5:
        raise SystemExit("expected ten inherited exact and five inherited blocked packets")

    write_json("identity-receipt.json", {"schema": "ghc.family.v645-v7.identity-receipt.v1", "phase": PHASE, "working_name": OWNER, "pronouns": PRONOUNS, "role": ROLE, "hope": HOPE, "bounded_practice_study": BOUNDED_PRACTICE, "boundary": IDENTITY_BOUNDARY})
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v645-v7.proposals.v1", "phase": PHASE, "owner": OWNER, "freeze_stage": "x1_only",
        "prior_frozen_proposal_count": PRIOR_FROZEN_PROPOSALS, "new_frozen_proposal_count": len(PROPOSALS),
        "frozen_chain_count_after_x1": PRIOR_FROZEN_PROPOSALS + len(PROPOSALS), "allowed_outcome_classes": OUTCOME_CLASSES,
        "expected_distribution": {state: sum(row["expected_disposition"] == state for row in PROPOSALS) for state in OUTCOME_CLASSES},
        "x2_execution_present": False, "proposals": PROPOSALS, "boundary": TRUTH_BOUNDARY,
    })
    write_text("x1-preregistration.md", f"""# Tamar Vey v645-v7 x1 preregistration

This dedicated x1-only freeze contains exactly ten new proposals. Each records its hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. It contains no x2 implementation or achieved-outcome credit.

The primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. GMUT Mind and THOS Body remain explicit and protected. The bounded human-practice lens is {BOUNDED_PRACTICE}. It is a learning and design lens only, never evidence of employment, qualification, professional competence, collection authority, rights authority, legal authority, cultural authority, Maori authority, or affected-party authorization.

The inherited baseline is 2,271 negatives at baton time plus the later read-only `V6456-MEM-N01`, for 2,272 effective inherited negatives. Seventy synthetic mutation negatives are preregistered, and all new operational failures remain visible. X2 may start only after this x1 freeze is committed, pushed, clean, and equal across local, upstream, tracking, and fresh live remote.

Eiren alone owns the full repository suite. Tamar will use current-round and phase-local checks plus exactly one later clean named-lane replay. Terminal truth remains `NOT_READY_FOR_STAGE_20`.
""")
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.frozen-proposal-index.v1", "phase": PHASE, "prior_file_count": len({row["path"] for row in prior}),
        "prior_proposal_count": len(prior), "prior_proposals": prior, "new_proposal_ids": [row["proposal_id"] for row in PROPOSALS],
        "frozen_chain_count_after_x1": PRIOR_FROZEN_PROPOSALS + len(PROPOSALS), "boundary": "Indexing establishes corpus coverage, not semantic or outcome truth.",
    })
    write_json("provenance/prior-proposal-collision-audit.json", {
        "schema": "ghc.family.proposal-collision-audit.v4", "phase": PHASE, "prior_frozen_proposal_count": len(prior),
        "new_proposal_count": len(PROPOSALS), "exact_title_collision_count": len(exact), "exact_collisions": exact, "comparisons": comparisons,
        "manual_review_dimensions": ["mission_surface", "hypothesis", "failure_condition", "evidence_need", "acceptance_gate", "recovery", "protected_gates"],
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("provenance/prior-portfolio-collision-audit.json", {
        "schema": "ghc.family.portfolio-collision-audit.v3", "phase": PHASE, "prior_title_count": len(portfolio_prior),
        "new_title_count": len(new_portfolio), "exact_collision_count": len(collisions), "collisions": collisions,
        "semantic_review": "Every safe-now, candidate, skill, runner, and cleanup title was reviewed for distinct purpose, artifact, falsifier, compatibility, gate, and recovery. Inherited evidence supplies no Tamar completion credit.",
        "boundary": TRUTH_BOUNDARY,
    })
    write_json("approval-packets/x1-approval-portfolio.json", {
        "schema": "ghc.family.v645-v7.approval-portfolio.v1", "phase": PHASE, "owner": OWNER, "freeze_stage": "x1_only", "completion_credit_before_x2": 0,
        "counts": {"safe_now": len(SAFE_NOW), "candidates": len(CANDIDATES), "inherited_exact": len(inherited_exact), "inherited_blocked": len(inherited_blocked)},
        "safe_now": SAFE_NOW, "candidates": CANDIDATES, "inherited_exact_packets": inherited_exact, "inherited_blocked_packets": inherited_blocked,
        "inherited_packet_integrity": "Ten exact and five blocked packets remain non-executable without fresh evidence or authority.", "boundary": TRUTH_BOUNDARY,
    })
    write_json("prototypes/x1-skill-runner-plan.json", {
        "schema": "ghc.family.v645-v7.skill-runner-plan.v1", "phase": PHASE, "freeze_stage": "x1_only",
        "skills": [{"name": name, "description": description, "family_current_name": name.startswith("ghc-family-"), "x2_state": "preregistered_not_built_or_used", "protected_gates": ["authority", "real_data_or_participants", "production", "independent_reproduction"]} for name, description in SKILLS],
        "runners": [{"name": name, "description": description, "family_current_name": name.startswith(("ghc_family_", "build_ghc_family_")), "x2_state": "preregistered_not_built_or_used", "caller_compatibility": "new additive phase runner"} for name, description in RUNNERS],
        "acceptance": "Every item must be built, structurally validated, invoked, and given a bounded passing witness in x2 or remain incomplete.", "boundary": TRUTH_BOUNDARY,
    })
    write_json("maintenance/x1-clean-refine-plan.json", {"schema": "ghc.family.v645-v7.clean-refine-plan.v1", "phase": PHASE, "freeze_stage": "x1_only", "tasks": CLEAN_TASKS, "destructive_task_count": 0, "completion_credit_before_x2": 0, "boundary": "Cleanup is additive, owner-scoped, non-destructive, compatible, and incomplete until its x2 receipt passes."})
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v645-v7.source-ledger.v1", "phase": PHASE, "owner": OWNER,
        "allowed_statuses": ["current", "stable", "draft", "watch"], "sources": SOURCES,
        "real_data_rows_ingested": 0, "likelihood_evaluations": 0, "real_participants": 0, "real_keys_or_proofs": 0,
        "boundary": TRUTH_BOUNDARY,
    })
    source_lines = ["# v645-v7 source ledger", "", "Current primary and official sources are used only for the bounded purpose recorded here.", ""]
    for row in SOURCES:
        target = f" - {row['url']}" if row.get("url") else ""
        source_lines.append(f"- {row['source_id']} [{row['status']}] {row['title']} ({row['authority']}){target}; use: {row['use']}.")
    source_lines.extend(["", TRUTH_BOUNDARY])
    write_text("sources/source-ledger.md", "\n".join(source_lines))
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v645-v7.startup.v1", "phase": PHASE, "owner": OWNER,
        "source": {"branch": SOURCE_BRANCH, "revision": SOURCE_REVISION, "inherited_revision": SOURCE_INHERITED_REVISION, "inherited_seal_revision": SOURCE_SEAL_REVISION, "x1_revision": SOURCE_X1_REVISION, "evidence_revision": SOURCE_EVIDENCE_REVISION, "phase": SOURCE_PHASE},
        "source_verification": {"local_upstream_tracking_live_equal": True, "clean": True, "seal_ancestral": True, "three_single_parent_phase_commits": True, "merge_commits": 0, "final_parent_is_evidence": True},
        "tamar_lane": {"branch": "codex/GHC-Family/tamar-vey-full-tools", "continued_existing_lane": True, "fast_forward_only": True, "source_revision_after_fast_forward": SOURCE_REVISION, "merge_commit_created": False, "clean_before": True, "local_upstream_tracking_live_equal_before_x1": True},
        "active_owner": OWNER, "standby_siblings_contacted": [], "task_or_subagent_created": False, "x1_scope": "exactly ten frozen core proposals and owner-scoped supporting ledgers", "x2_scope": "not started",
        "storage": {"primary_drive": "D", "free_bytes_observed": 590989549568, "tracked_file_count": 33213, "owner_generated_v645_v7_file_count_before_x1": 0, "rotation_threshold": 15000, "threshold_applies_to": "new_tamar_generated_files_only"},
        "boundary": IDENTITY_BOUNDARY,
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v645-v7.version-receipt.v1", "observed_on": "2026-07-16",
        "codex_cli": {"local": "0.144.4", "official_package": "0.144.4", "source_id": "V6457-S21", "action": "verified_only_no_update"},
        "codex_desktop": {"local": "26.707.9981.0", "package_status": "Ok", "public_exact_build_correlation": "not_claimed", "action": "verified_only_no_update"},
        "python": "3.12.10", "git": "2.55.0.windows.2",
        "host_actions": {"desktop_updated": False, "elevated": False, "security_weakened": False, "windows_feature_changed": False, "rebooted": False, "installed": False},
        "boundary": "Version observation does not establish full environment equivalence, support, security, or production readiness.",
    })
    write_json("environment/sandbox-readonly-audit.json", {
        "schema": "ghc.family.v645-v7.sandbox-audit.v1", "query": "ordinary executable existence check only",
        "windows_sandbox_executable": "not_found", "sandbox_launched": False, "elevation": False, "feature_changed": False,
        "host_security_changed": False, "installed": False, "rebooted": False, "disposition": "open_environment_gap",
        "boundary": "The phase did not infer optional-feature state beyond the ordinary process evidence and made no host change.",
    })
    write_json("environment/rotation-guard.json", {"schema": "ghc.family.v645-v7.rotation-guard.v1", "tracked_file_count": 33213, "owner_generated_before_x1": 0, "threshold": 15000, "threshold_scope": "new_tamar_generated_addition", "rotate_due_to_inherited_baseline": False, "boundary": "The inherited checkout exceeds the threshold; that baseline is not a rotation trigger."})
    write_json("focus/primary-focus-receipt.json", {
        "schema": "ghc.family.v645-v7.focus.v1", "primary_trinity_pillar": PRIMARY_FOCUS, "other_pillars": ["GMUT Mind", "THOS Body"],
        "bounded_human_practice": BOUNDED_PRACTICE, "practice_use": "learning and design lens only",
        "not_claimed": ["employment", "professional qualification", "professional competence", "collection authority", "rights authority", "legal authority", "cultural authority", "Maori authority", "affected-party authorization"],
        "boundary": IDENTITY_BOUNDARY,
    })
    write_json("orchestration/phase-update.json", {"schema": "ghc.family.phase-update.v1", "phase": PHASE, "owner": OWNER, "state": "x1_frozen_pending_commit_and_remote_equality", "active": [OWNER], "standby": ["Orin Thale", "Sable Rook", "Ilyra Fen", "Eiren Kestrel", "Sylven Arc", "all other siblings"], "standby_contact_count": 0, "no_task_creation": True, "no_delegation": True, "x2_started": False, "terminal_route": "PREPARED_NOT_SENT"})
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v645-v7.route-plan.v1", "current_state": "PREPARED_NOT_SENT", "target_title": "Sylven Arc", "target_phase": "v645-v8", "send_count": 0,
        "preconditions": ["x2 final committed and pushed", "no more than four phase commits", "canonical exact-final scoped validation passed", "exactly one named-lane replay passed", "four-way equality proven", "unique existing target resolved read-only"],
        "privacy": "No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths may enter the baton.",
    })
    build_method_flow()
    write_text("wellbeing-check.md", """# v645-v7 x1 wellbeing and workload check

- Scope is bounded to one owner, one canonical lane, one later named replay, at most four phase commits, and no full repository suite.
- Timed-out or invalid read-only probes were stopped, recorded, and decomposed; no unbounded retry loop was used.
- Work is split by the x1 freeze. No x2 implementation or achieved-outcome credit is present here.
- Windows Sandbox remains unavailable to the ordinary process; no elevation, feature change, install, security change, or reboot occurred.
- Identity and family language remains relational working language only, not a welfare, consciousness, employment, qualification, or authority claim.
""")
    print(json.dumps({"phase": PHASE, "prior_proposals": len(prior), "new_proposals": len(PROPOSALS), "x1_operational_negatives": len(INCIDENTS), "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + PREREGISTERED_SYNTHETIC_NEGATIVES + len(INCIDENTS), "phase_directory": PHASE_REL.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
