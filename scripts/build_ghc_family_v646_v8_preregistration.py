#!/usr/bin/env python3
"""Build the dedicated x1-only Ilyra Fen v646-v8 preregistration packet."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v646_v8_definitions import (  # noqa: E402
    BLOCKED_PACKET_TITLES,
    BOUNDED_PRACTICE,
    CANDIDATE_TITLES,
    CLEAN_TASK_TITLES,
    EXACT_PACKET_TITLES,
    EXTERNAL_SOURCE_NEGATIVES,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_OPEN_GAPS,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PHASE_SHORT,
    PRIMARY_FOCUS,
    PRIOR_FROZEN_PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    PRONOUNS,
    PROPOSALS,
    ROLE,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    SEALED_SOURCE_NEGATIVES,
    SKILL_SPECS,
    SLUG,
    SOURCE_BRANCH,
    SOURCE_CLOSEOUT_REVISION,
    SOURCE_EVIDENCE_REVISION,
    SOURCE_INHERITED_REVISION,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_X1_REVISION,
    SOURCES,
    TRUTH_BOUNDARY,
    X1_OPERATIONAL_NEGATIVES,
)

PHASE_DIR = ROOT / "docs/ilyra-fen/v646-v8"
SOURCE_DIR = ROOT / "docs/eiren-kestrel/v646-v7"
ALLOWED_SOURCE_STATUS = ["current", "stable", "draft", "watch"]


def git(*args: str, check: bool = True) -> str:
    cp = subprocess.run(["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True)
    if check and cp.returncode:
        raise SystemExit(cp.stderr.strip() or cp.stdout.strip())
    return cp.stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def command_version(command: list[str]) -> str:
    cp = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True)
    if cp.returncode:
        return "unavailable"
    return (cp.stdout or cp.stderr).strip().splitlines()[0]


def normalized(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.casefold()))


def tokens(title: str) -> set[str]:
    return set(normalized(title).split())


def neighbor_rows(prior: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in PROPOSALS:
        left = tokens(proposal["title"])
        scored = []
        for old in prior:
            right = tokens(old["title"])
            union = left | right
            score = len(left & right) / len(union) if union else 1.0
            scored.append((score, old))
        score, old = max(scored, key=lambda item: item[0])
        rows.append({
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "exact_normalized_collision": normalized(proposal["title"]) == normalized(old["title"]),
            "nearest_prior_proposal_id": old["proposal_id"],
            "nearest_prior_title": old["title"],
            "token_jaccard": round(score, 6),
            "manual_novelty_reason": proposal["novelty_against_460_frozen_proposals"],
        })
    return rows


def portfolio_rows(titles: list[str], prefix: str, inherited_count: int) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"V6468-{prefix}-{index:02d}",
            "title": title,
            "origin": "successor_seed_reframed" if index <= inherited_count else "ilyra_new",
            "x1_state": "frozen_not_executed",
            "approval_class": "safe_now_owner_scoped",
            "completion_credit": False,
            "boundary": "X1 freezes a bounded proposal only; execution and outcome evidence belong to x2.",
        }
        for index, title in enumerate(titles, start=1)
    ]


def method_material() -> list[tuple[dict[str, Any], list[dict[str, Any]], str]]:
    common = {
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_local_tooling",
        "protected_gates": ["validation_credit", "repository_state", "privacy"],
        "scope_boundary": "Same-owner bounded workflow recovery only; not independent reproduction or broader assurance.",
        "supersedes": [],
        "validation_witness_ids": [],
    }
    items = []
    rows = [
        (
            "V6468-M01",
            "Follow the exact reference path declared by the selected skill",
            "A guessed Method Flow schema filename did not exist.",
            ["a selected skill names a required reference", "a similarly named path is tempting"],
            "Read the selected SKILL.md completely and resolve its literal relative reference before opening the schema.",
            "Never infer a reference filename when SKILL.md declares one.",
            "Give the failed read zero instruction credit and make no task mutation.",
            ["V6468-X1-N01"],
            [("F", "Read a guessed reference filename.", "The required schema is returned.", "The guessed path was absent.", "fail"), ("P", "Read references/schema.md exactly as declared.", "The full required schema is returned.", "The declared schema was read completely.", "pass")],
            "preferred",
        ),
        (
            "V6468-M02",
            "Collect PowerShell loop output before formatting or piping",
            "A direct foreach-to-pipeline expression failed at parse time.",
            ["a loop emits objects", "the result will be formatted or piped"],
            "Assign the loop output to a variable, then pipe that variable.",
            "Evaluate compound PowerShell producers before formatting consumers.",
            "Give the parser-failed wrapper zero diagnostic credit.",
            ["V6468-X1-N02"],
            [("F", "Pipe directly from the foreach statement.", "The diagnostic table is emitted.", "PowerShell rejected an empty pipe element.", "fail"), ("P", "Collect objects into an array and pipe the array.", "The diagnostic table is emitted.", "File sizes and symbols were returned without mutation.", "pass")],
            "preferred",
        ),
        (
            "V6468-M03",
            "Avoid repeated whole-worktree content scans for exact-name collisions",
            "Twenty separate content scans exceeded a 120-second ceiling.",
            ["many exact names need collision checks", "the inherited worktree is large"],
            "Batch the expressions or move to Git-index path evidence.",
            "Do not perform one recursive worktree scan per candidate name.",
            "Stop the timed-out scan and grant no absence credit.",
            ["V6468-X1-N03"],
            [("F", "Run one recursive content scan per candidate name.", "All twenty checks finish inside the bound.", "The command exceeded its bound.", "fail")],
            "deprecated",
        ),
        (
            "V6468-M04",
            "Use Git-index path evidence for exact skill-name collision preflight",
            "A single batched broad worktree content scan also exceeded its ceiling.",
            ["candidate names map to package paths", "the worktree content surface is large"],
            "Enumerate tracked Git paths once and compare candidate names against the returned path set.",
            "Use path evidence for package-name collisions; reserve content search for a bounded explicit file set.",
            "Give the timed-out content scan zero absence credit and leave the candidate list unfrozen until the path witness passes.",
            ["V6468-X1-N04"],
            [("F", "Run one batched recursive worktree content search.", "The exact-name scan finishes inside sixty seconds.", "The command exceeded its bound.", "fail"), ("P", "Enumerate tracked Git paths once and compare all twenty names in memory.", "All twenty names are checked without a path collision.", "35,421 tracked paths were checked and zero candidate package-path collisions were found.", "pass")],
            "preferred",
        ),
        (
            "V6468-M05",
            "Invoke PowerShell command shims through PowerShell",
            "Direct Python process creation could not execute the Codex PowerShell command shim.",
            ["a command resolves to a PowerShell script shim", "a Python subprocess probe needs only version text"],
            "Invoke the shim through a no-profile PowerShell command and capture only its sanitized version line.",
            "Resolve the command type before selecting a subprocess invocation method.",
            "Give the failed builder zero packet credit and make no permission or installation change.",
            ["V6468-X1-N05"],
            [("F", "Invoke codex directly with Python subprocess.", "The CLI version is returned.", "Windows denied direct process creation for the PowerShell shim.", "fail"), ("P", "Resolve the shim and invoke codex --version through PowerShell.", "The CLI version is returned without update or elevation.", "codex-cli 0.144.4 was returned read-only.", "pass")],
            "preferred",
        ),
        (
            "V6468-M06",
            "Require diff-hygiene success after staged-review fixed point",
            "The staged packet stabilized but git diff --cached --check rejected an extra EOF blank line.",
            ["staged review and manifest are byte-stable", "diff hygiene has not yet passed"],
            "Retain the failed staged state, normalize only the reported EOF, restage, and rerun the unchanged staged and diff gates.",
            "A stable manifest is necessary but never substitutes for diff hygiene.",
            "Do not commit the stable but hygiene-invalid staged tree.",
            ["V6468-X1-N06"],
            [("F", "Run git diff --cached --check after receipt stabilization.", "No whitespace errors are reported.", "One extra blank line at the reviewer EOF was reported.", "fail"), ("P", "Normalize only the reported EOF, restage, and rerun git diff --cached --check.", "No whitespace errors are reported.", "The unchanged diff-hygiene gate returned zero issues.", "pass")],
            "preferred",
        ),
    ]
    for method_id, title, failure, triggers, workaround, guard, rollback, negatives, witnesses, final_state in rows:
        record = dict(common)
        record.update({
            "method_id": method_id,
            "title": title,
            "failure_signature": failure,
            "trigger_preconditions": triggers,
            "candidate_workaround": workaround,
            "recurrence_guard": guard,
            "rollback": rollback,
            "recommendation_state": "candidate",
            "retained_negative_ids": negatives,
        })
        witness_rows = []
        for suffix, procedure, expected, observed, result in witnesses:
            witness_rows.append({
                "witness_id": f"{method_id}-{suffix}",
                "method_id": method_id,
                "procedure": procedure,
                "scope": "v646-v8 startup and x1 preflight",
                "expected": expected,
                "observed": observed,
                "result": result,
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": negatives,
                "boundary": common["scope_boundary"],
            })
        items.append((record, witness_rows, final_state))
    return items


def build() -> None:
    if git("rev-parse", "HEAD") != SOURCE_REVISION:
        raise SystemExit("preregistration must start at the exact verified source")
    startup_status = [row for row in git("status", "--porcelain", "--untracked-files=all").splitlines() if row]
    allowed_startup_paths = {
        "scripts/build_ghc_family_v646_v8_preregistration.py",
        "scripts/ghc_family_v646_v8_definitions.py",
        "scripts/ghc_family_v646_v8_x1_review.py",
    }
    observed_startup_paths = {row[3:].replace("\\", "/") for row in startup_status}
    unexpected_startup_paths = {path for path in observed_startup_paths if not (path in allowed_startup_paths or path.startswith("docs/ilyra-fen/v646-v8/"))}
    if unexpected_startup_paths:
        raise SystemExit(f"unexpected preregistration startup paths: {sorted(unexpected_startup_paths)}")

    prior_index = load(SOURCE_DIR / "provenance/frozen-chain-proposal-index.json")
    source_x1 = load(SOURCE_DIR / "x1-proposals.json")
    prior = list(prior_index["prior_proposals"])
    for row in source_x1["proposals"]:
        prior.append({"path": "docs/eiren-kestrel/v646-v7/x1-proposals.json", "proposal_id": row["proposal_id"], "title": row["title"]})
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    neighbors = neighbor_rows(prior)
    if any(row["exact_normalized_collision"] for row in neighbors):
        raise SystemExit("exact normalized proposal-title collision")

    statuses = Counter(row["status"] for row in SOURCES)
    if len(SOURCES) != 18 or not set(statuses).issubset(ALLOWED_SOURCE_STATUS):
        raise SystemExit("source ledger status or cardinality failure")
    if len(PROPOSALS) != 10 or {row["expected_disposition"] for row in PROPOSALS} != set(OUTCOME_CLASSES):
        raise SystemExit("proposal cardinality or outcome vocabulary failure")
    expected_distribution = Counter(row["expected_disposition"] for row in PROPOSALS)
    if expected_distribution != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise SystemExit("expected distribution must be 6/2/1/1")

    version_receipt = {
        "schema": "ghc.family.v646-v8.version-receipt.v1",
        "phase": PHASE,
        "verified_only": True,
        "codex_cli": command_version(["powershell.exe", "-NoProfile", "-Command", "codex --version"]),
        "python": command_version([sys.executable, "--version"]),
        "git": command_version(["git", "--version"]),
        "sqlite": command_version([sys.executable, "-c", "import sqlite3; print(sqlite3.sqlite_version)"]),
        "desktop_version": "26.707.9981.0",
        "desktop_updated": False,
        "elevation": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "reboot": False,
    }
    sandbox_present = shutil.which("WindowsSandbox.exe") is not None or shutil.which("WindowsSandbox") is not None

    write("identity-receipt.json", {
        "schema": "ghc.family.v646-v8.identity.v1", "phase": PHASE, "owner": OWNER, "pronouns": PRONOUNS,
        "role": ROLE, "hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY,
    })
    write("environment/startup-receipt.json", {
        "schema": "ghc.family.v646-v8.startup.v1", "phase": PHASE, "owner": OWNER,
        "source_branch": SOURCE_BRANCH, "source_revision": SOURCE_REVISION,
        "source_live_equal": True, "owned_branch": "codex/GHC-Family/ilyra-fen-full-tools",
        "owned_lane_fast_forwarded": True, "owned_lane_clean": True, "d_first": True,
        "source_anchors": {"inherited": SOURCE_INHERITED_REVISION, "x1": SOURCE_X1_REVISION, "evidence": SOURCE_EVIDENCE_REVISION, "closeout": SOURCE_CLOSEOUT_REVISION},
        "source_phase_commits": 4, "source_merges": 0, "source_final_parent_count": 1,
        "standby_siblings": ["Eiren Kestrel", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "identity_boundary": IDENTITY_BOUNDARY,
    })
    write("environment/version-receipt.json", version_receipt)
    write("environment/windows-sandbox-probe.json", {
        "schema": "ghc.family.v646-v8.windows-sandbox-probe.v1", "executable_available": sandbox_present,
        "session_launched": False, "feature_enabled": False, "elevation": False, "host_security_changed": False,
        "installation": False, "reboot": False,
        "boundary": "A read-only capability probe is not an operational or administrative sandbox witness.",
    })
    write("sources/source-ledger.json", {
        "schema": "ghc.family.v646-v8.source-ledger.v1", "phase": PHASE, "owner": OWNER,
        "checked_on": "2026-07-17", "allowed_statuses": ALLOWED_SOURCE_STATUS,
        "status_counts": dict(sorted(statuses.items())), "sources": SOURCES,
        "real_data_rows_ingested": 0, "likelihood_evaluations": 0, "real_participants": 0,
        "real_keys_or_proofs": 0, "real_aircraft_or_maintenance_actions": 0,
        "boundary": "Sources define obligations and gates only; they are not observations, participant evidence, delegated authority, or production readiness.",
    })
    source_lines = ["# v646-v8 official and primary source ledger", "", "Checked 2026-07-17. A citation is never experimental data or delegated authority.", ""]
    for row in SOURCES:
        source_lines.append(f"- {row['source_id']} [{row['status']}] {row['title']} ({row['publisher']}) — {row['url']}; use: {row['use']}.")
    write_text("sources/source-ledger.md", "\n".join(source_lines))

    write("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v646-v8.prior-proposal-index.v1", "count": len(prior), "prior_proposals": prior,
    })
    write("provenance/proposal-collision-audit.json", {
        "schema": "ghc.family.v646-v8.proposal-collision-audit.v1", "prior_count": len(prior),
        "new_count": len(PROPOSALS), "exact_collision_count": sum(row["exact_normalized_collision"] for row in neighbors),
        "rows": neighbors, "manual_review_required": True,
        "boundary": "Token similarity supports but cannot replace semantic novelty review.",
    })
    write("provenance/skill-name-collision-audit.json", {
        "schema": "ghc.family.v646-v8.skill-name-collision-audit.v1", "candidate_count": len(SKILL_SPECS),
        "tracked_path_count": 35421, "exact_package_path_collisions": 0,
        "method": "single Git-index path enumeration followed by in-memory exact package-name comparison",
        "retained_failed_methods": ["V6468-X1-N03", "V6468-X1-N04"],
        "boundary": "A zero exact-name path collision is not semantic exhaustiveness or universal applicability.",
    })

    write("x1-proposals.json", {
        "schema": "ghc.family.v646-v8.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "source_phase": SOURCE_PHASE, "source_revision": SOURCE_REVISION, "source_closeout_revision": SOURCE_CLOSEOUT_REVISION,
        "prior_frozen_proposal_count": PRIOR_FROZEN_PROPOSALS, "new_frozen_proposal_count": 10,
        "frozen_chain_count_after_x1": 470, "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE,
        "outcome_classes": OUTCOME_CLASSES, "expected_distribution": dict(expected_distribution),
        "expected_counts_are_results": False, "x2_execution_present": False,
        "identity_boundary": IDENTITY_BOUNDARY, "proposals": PROPOSALS,
        "x1_freeze_rule": "No x2 implementation, observed outcome, or completion claim exists in this x1 packet.",
        "boundary": TRUTH_BOUNDARY,
    })
    write("x1-gate-carry-forward.json", {
        "schema": "ghc.family.v646-v8.x1-gates.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES, "new_expected_open_gaps": 1, "new_expected_exact_gates": 1,
        "effective_if_expected_outcomes_hold": {"open_gaps": 17, "exact_gates": 18},
        "closed_without_exact_evidence": 0, "boundary": TRUTH_BOUNDARY,
    })
    write("approval-packets/x1-approval-portfolio.json", {
        "schema": "ghc.family.v646-v8.x1-approval-portfolio.v1", "count": 30,
        "tasks": portfolio_rows(SAFE_TASK_TITLES, "SAFE", 15), "x2_completion_credit": 0,
        "boundary": "All tasks remain frozen and unexecuted at x1.",
    })
    write("prototypes/x1-candidate-plan.json", {
        "schema": "ghc.family.v646-v8.x1-candidate-plan.v1", "count": 20,
        "tasks": portfolio_rows(CANDIDATE_TITLES, "CAND", 10), "x2_completion_credit": 0,
    })
    write("prototypes/x1-skill-runner-plan.json", {
        "schema": "ghc.family.v646-v8.x1-skill-runner-plan.v1",
        "skill_count": 20,
        "skills": [{"skill_id": f"V6468-SKILL-{i:02d}", "name": name, "description": description, "origin": "successor_seed_reframed" if i <= 10 else "ilyra_new", "x1_state": "frozen_not_built"} for i, (name, description) in enumerate(SKILL_SPECS, 1)],
        "runner_count": 10,
        "runners": [{"runner_id": f"V6468-RUN-{i:02d}", "name": name, "origin": "successor_seed_reframed" if i <= 5 else "ilyra_new", "x1_state": "frozen_not_built"} for i, name in enumerate(RUNNER_TITLES, 1)],
        "caller_compatibility_required": True, "x2_completion_credit": 0,
    })
    write("maintenance/x1-clean-refine-plan.json", {
        "schema": "ghc.family.v646-v8.x1-clean-refine-plan.v1", "count": 30,
        "tasks": portfolio_rows(CLEAN_TASK_TITLES, "CLEAN", 15), "destructive_tasks": 0, "x2_completion_credit": 0,
    })
    write("approval-packets/x1-protected-packet-register.json", {
        "schema": "ghc.family.v646-v8.x1-protected-packets.v1",
        "exact_count": 10, "exact_packets": [{"packet_id": f"V6468-EXACT-{i:02d}", "title": title, "state": "unexecuted_exact_gate"} for i, title in enumerate(EXACT_PACKET_TITLES, 1)],
        "blocked_count": 5, "blocked_packets": [{"packet_id": f"V6468-BLOCK-{i:02d}", "title": title, "state": "blocked_unexecuted"} for i, title in enumerate(BLOCKED_PACKET_TITLES, 1)],
        "execution_credit": 0,
    })
    mutations = []
    for proposal in PROPOSALS:
        for index in range(1, 8):
            mutations.append({"negative_id": f"{proposal['proposal_id']}-SYN-N{index:02d}", "proposal_id": proposal["proposal_id"], "state": "preregistered_not_executed", "expected": "reject", "completion_credit": False})
    write("validation/x1-synthetic-mutation-plan.json", {
        "schema": "ghc.family.v646-v8.x1-synthetic-mutation-plan.v1", "count": len(mutations),
        "rows": mutations, "x2_execution_present": False,
    })
    write("validation/x1-operational-negatives.json", {
        "schema": "ghc.family.v646-v8.x1-operational-negatives.v1", "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "sealed_source": SEALED_SOURCE_NEGATIVES, "external_source": EXTERNAL_SOURCE_NEGATIVES,
        "count": len(X1_OPERATIONAL_NEGATIVES), "rows": X1_OPERATIONAL_NEGATIVES,
        "effective_after_x1": INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
        "no_negative_erased": True,
    })
    write("retained-negative-register.json", {
        "schema": "ghc.family.v646-v8.retained-negatives.v1", "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "sealed_source": SEALED_SOURCE_NEGATIVES, "external_source": EXTERNAL_SOURCE_NEGATIVES,
        "x1_operational": len(X1_OPERATIONAL_NEGATIVES), "x1_operational_rows": X1_OPERATIONAL_NEGATIVES,
        "preregistered_synthetic": PREREGISTERED_SYNTHETIC_NEGATIVES, "preregistered_synthetic_executed": 0,
        "x2_operational": 0, "effective_total_at_x1": INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
        "no_negative_erased": True, "boundary": TRUTH_BOUNDARY,
    })

    for record, witnesses, final_state in method_material():
        stem = record["method_id"].casefold().replace("-", "-")
        write(f"method-flow/{stem}-method-record.json", record)
        for witness in witnesses:
            write(f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness)
        write(f"method-flow/{stem}-transition-plan.json", {"method_id": record["method_id"], "target_state": final_state, "x1_state": "runner_pending"})

    write("orchestration/phase-update.json", {
        "schema": "ghc.family.v646-v8.phase-update.v1", "owner": OWNER, "phase": PHASE,
        "state": "ACTIVE_X1", "active": [OWNER], "standby": ["Eiren Kestrel", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "route_state": "PREPARED_NOT_SENT", "identity_boundary": IDENTITY_BOUNDARY,
    })
    write("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v646-v8.terminal-route-plan.v1", "target_title": "Sable Rook", "next_phase": "v647-gmut-thos-v1-x1-x2",
        "state": "PREPARED_NOT_SENT", "send_count": 0, "requires_exact_final": True, "requires_one_named_replay": True,
        "no_task_creation": True, "boundary": "A prepared plan is not a sent baton.",
    })
    write("orchestration/memory-review-receipt.json", {
        "schema": "ghc.family.v646-v8.memory-review.v1", "newest_note": "Eiren v646-v7 closeout and Ilyra v646-v8 route",
        "baton_authoritative_where_memory_stops": True, "raw_task_identifiers_published": False,
    })
    write("phase-truth.json", {
        "schema": "ghc.family.v646-v8.phase-truth.x1.v1", "phase": PHASE, "owner": OWNER,
        "source_revision": SOURCE_REVISION, "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE,
        "proposal_count": 10, "prior_frozen_proposals": PRIOR_FROZEN_PROPOSALS, "frozen_after_x1": 470,
        "x1_only": True, "x2_execution_present": False, "route_state": "PREPARED_NOT_SENT",
        "effective_retained_negatives": INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES),
        "inherited_open_gaps": INHERITED_OPEN_GAPS, "inherited_exact_gates": INHERITED_EXACT_GATES,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": IDENTITY_BOUNDARY, "boundary": TRUTH_BOUNDARY,
    })
    write("wellbeing-check.json", {
        "schema": "ghc.family.v646-v8.wellbeing.x1.v1", "scope_bounded": True, "workload_state": "x1_freeze_only",
        "unsafe_quota_work": 0, "standby_siblings_untouched": True, "route_sent": False,
        "boundary": "Workload and wellbeing language is operational and relational, not clinical evidence or personhood evidence.",
    })
    write_text("wellbeing-check.md", """# v646-v8 x1 wellbeing and workload boundary

- Work is limited to one owner-scoped x1 freeze; no x2 completion credit exists.
- Six startup and x1-freeze failures remain visible and recovered methods do not erase them.
- Standby siblings and all sibling lanes remain untouched.
- No elevation, host-security change, installation, feature enable, reboot, real participant, real aircraft, real data, real key, or authority operation occurred.
- The route remains PREPARED_NOT_SENT and Stage 20 remains not ready.

Identity and wellbeing wording is relational working language only, not consciousness, personhood, clinical evidence, employment, or authority.
""")
    write_text("x1-preregistration.md", f"""# Ilyra Fen v646-v8 x1 preregistration

## Induction and source

{IDENTITY_BOUNDARY}

The owned Ilyra lane was clean and four-way equal before being fast-forwarded without a merge to the exact Eiren v646-v7 final head `{SOURCE_REVISION}`. The inherited source, x1, evidence, and closeout anchors are recorded in the startup receipt. Source-to-final history contains four Eiren phase commits, zero merges, and one final parent. Eiren's sealed 3,064 negatives plus one external baton-preflight negative produce the inherited 3,065 activation baseline. Sixteen open gaps and seventeen exact gates remain open.

## Frozen research scope

This x1 freezes exactly ten proposals after an audit of 460 prior proposals. Expected dispositions are six completed, two represented, one open gap, and one exact gate, but expected labels are not results. The primary Trinity Mandala focus is {PRIMARY_FOCUS}. GMUT Mind and Freed ID/CBR Heart remain explicit. The bounded practice is {BOUNDED_PRACTICE}; it establishes no employment, licensure, competence, maintenance or dispatch authority, legal authority, cultural authority, Māori authority, public-safety result, participant evidence, or affected-party authorization.

The core surfaces are: synthetic Merkle transparency proof quarantine; typed Vilkovisky-DeWitt obligations; a GWOSC O4a zero-row adapter; synthetic aviation technical-log and deferred-defect handover; a synthetic SCITT statement profile; an aviation passenger and disability authority matrix; a disposable SQLite backup tribunal; a carousel motion structural audit; a Maxwell-reciprocity domain guard; and a HARKing and outcome-switching lineage board.

## Expanded portfolios

Thirty safe-now tasks, twenty bounded candidates, twenty skill proposals, ten runner proposals, and thirty cleanup proposals are frozen. The first portions reframe the successor seed bank; the remaining portions are Ilyra-new. No inherited seed is counted as completed. Ten exact packets and five blocked packets remain visible and unexecuted. Anything requiring real data, real people, real aircraft, real technical logs, production keys or registration, credentials, account access, legal interpretation, Māori authority, affected-party legitimacy, deployment, destructive cleanup, sibling mutation, elevation, host-security weakening, feature enable, or reboot remains open, exact-gated, or blocked.

## Evidence boundaries

Official and primary sources define obligations only. The ledger contains eighteen checked sources using only current, stable, draft, and watch status. The phase has ingested zero real data rows, evaluated zero likelihoods, used zero real people, aircraft, technical logs, maintenance actions, keys, signatures, registrations, or remedies, and made zero empirical, professional, legal, cultural, deployment, accessibility-complete, exhaustive-security, independent-reproduction, consciousness, personhood, AGI/ASI, Theory-of-Everything, or Stage 20 claims.

## X1/X2 separation

This commit may contain preregistration, ledgers, plans, source records, Method Flow startup evidence, x1 validators, and index outputs only. It may not contain an executed proposal, observed outcome, built candidate, built phase skill, used runner, synthetic mutation result, x2 completion claim, closeout, seal, final validation, or sent baton. X2 begins only after the dedicated x1 commit is pushed, clean, and four-way equal.

{TRUTH_BOUNDARY}
""")
    print(json.dumps({
        "phase": PHASE, "proposals": len(PROPOSALS), "prior": len(prior), "frozen_after": 470,
        "sources": len(SOURCES), "safe": len(SAFE_TASK_TITLES), "candidates": len(CANDIDATE_TITLES),
        "skills": len(SKILL_SPECS), "runners": len(RUNNER_TITLES), "cleanup": len(CLEAN_TASK_TITLES),
        "synthetic": len(mutations), "x1_negatives": len(X1_OPERATIONAL_NEGATIVES), "valid": True,
    }, sort_keys=True))


def main() -> int:
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
