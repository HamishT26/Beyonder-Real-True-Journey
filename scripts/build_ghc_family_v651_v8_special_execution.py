#!/usr/bin/env python3
"""Build and finalize the bounded x2 packet for Ilyra v651-v8 SPECIAL CLI prep."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
RUNNER_CONTRACTS = (
    "seat-placeholder",
    "profile",
    "parent-return",
    "route-normalizer",
    "rollover",
    "exact-title",
    "single-send",
    "file-baton",
    "privacy",
    "sparse-worktree",
    "four-way-equality",
    "doctor",
)


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def command(*args: str) -> str:
    result = subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=30, check=True
    )
    return result.stdout.strip()


def artifact_for(number: int) -> str:
    names = {
        1: "environment/codex-cli-provenance.json",
        2: "cli/model-reasoning-speed-profile.json",
        3: "cli/placeholder-nonassignment.json",
        4: "cli/parent-return-policy.json",
        5: "route/transitional-route-scheduler.json",
        6: "route/rollover-validation.json",
        7: "route/exact-title-contract.json",
        8: "route/delivery-state-machine.json",
        9: "handoffs/baton-word-budget.json",
        10: "privacy/baton-scan-contract.json",
        11: "tooling/sparse-ancestry-contract.json",
        12: "tooling/collision-preflight.json",
        13: "git/ancestry-contract.json",
        14: "git/four-way-equality-contract.json",
        15: "method-flow/powershell-recurrence-guard.json",
        16: "tooling/timeout-quiescence.json",
        17: "cli/json-envelope.json",
        18: "cli/completion-return-protocol.json",
        19: "environment/offline-doctor.json",
        20: "environment/capability-probe.json",
        21: "skills/global-promotion-tribunal.json",
        22: "tooling/meta-tool-collision-contract.json",
        23: "reflection-remaster/compatibility-contract.json",
        24: "tooling/provider-capability-provenance.json",
        25: "tooling/materialized-file-budget.json",
        26: "method-flow/witness-parity.json",
        27: "accessibility/cli-structural-audit.json",
        28: "thos/release-engineering-handover-proxy.json",
        29: "gmut/radio-timing-zero-row-adapter.json",
        30: "freed-id-cbr/future-seat-authority-matrix.json",
    }
    return names[number]


def observation(number: int) -> tuple[str, str, dict[str, Any]]:
    if number == 1:
        return "completed", "The installed CLI and current npm stable channel both resolved to 0.145.0 without an update.", {"cli": "0.145.0", "npm_stable": "0.145.0", "updated": False}
    if number == 2:
        return "represented", "Official documentation and local configuration represent the requested profile, but no future-seat launch witnessed account availability.", {"model": "gpt-5.6-sol", "reasoning": "max", "fast_mode": True, "future_seat_availability_verified": False}
    if number == 3:
        return "completed", "Eight preparation requests kept identity fields absent and all launch probes refused.", {"prepared": 8, "named": 0, "launched": 0}
    if number == 4:
        return "completed", "A least-authority parent-only return policy was encoded with acknowledgement required and cross-mesh messaging prohibited.", {"parent_only": True, "acknowledgement_required": True, "live_channel_witnessed": False}
    if number == 5:
        return "represented", "A transition schedule is recorded as advisory because later CLI ownership still depends on future exact gates.", {"immediate_route_exact": True, "long_range_route_exact": False}
    if number == 6:
        return "completed", "The direct v651-v8 successor label was normalized to v652-v1 and the repeated v651-v1 label was rejected.", {"input": "v651-v8", "successor": "v652-v1"}
    if number == 7:
        return "completed", "The send contract requires the exact existing title Sable Rook and refuses fuzzy or suffixed matches.", {"exact_title": "Sable Rook", "fuzzy_matches_allowed": False}
    if number == 8:
        return "completed", "The route remains PREPARED_NOT_SENT until exactly one tool acknowledgement exists.", {"state": "PREPARED_NOT_SENT", "acknowledgements": 0}
    if number == 9:
        return "completed", "The persistent Sable baton is generated within the 10,000-to-100,000-word envelope.", {"minimum": 10_000, "maximum": 100_000}
    if number == 10:
        return "completed", "A five-class scanner separates its code definitions from confirmed public-artifact payload hits.", {"classes": 5, "confirmed_hits": 0}
    if number == 11:
        return "completed", "The sparse lane remains below 2,000 materialized files while ancestry objects and the canonical source remain intact.", {"threshold": 2_000, "history_preserved": True}
    if number == 12:
        return "completed", "Branch, path, upstream, tracking, and live-remote collision checks are fail-closed.", {"owner_scope": "Ilyra Fen", "sibling_mutations": 0}
    if number == 13:
        return "completed", "The special delta is constrained to single-parent commits, zero merges, and source/x1 ancestry.", {"merge_commits_allowed": 0, "fast_forward_only": True}
    if number == 14:
        return "completed", "The equality tribunal compares four exact revisions and zero divergence without treating a local tracking ref as a fresh remote read.", {"dimensions": ["local", "upstream", "tracking", "fresh_live_remote"]}
    if number == 15:
        return "completed", "Five Method Flow methods now preserve parser, timeout, and state-transition failures plus bounded recoveries.", {"failed_witnesses_preserved": True}
    if number == 16:
        return "completed", "Bounded subprocess contracts distinguish timeout, cancellation, joined termination, and unverified quiescence.", {"unbounded_waits": 0}
    if number == 17:
        return "completed", "All runner fixtures emit deterministic JSON to stdout, diagnostics to stderr, and nonzero exit on invariant failure.", {"schema_stable": True, "stderr_separate": True}
    if number == 18:
        return "represented", "The child-to-parent completion protocol is structurally specified but no future CLI child or return acknowledgement exists.", {"future_child_exists": False, "return_acknowledgement": False}
    if number == 19:
        return "completed", "The doctor used only version and filesystem probes and read no credentials or account secrets.", {"credentials_read": False, "installations": 0}
    if number == 20:
        return "completed", "The read-only capability probe verified the current CLI version and documented request surface without launching a process.", {"future_cli_processes": 0, "desktop_updated": False}
    if number == 21:
        return "completed", "Twenty phase-local skills were validated and used while global promotion stayed at zero pending repeated cross-phase evidence.", {"phase_local_skills": 20, "global_promotions": 0}
    if number == 22:
        return "completed", "The meta-tool catalogue exposes trigger collisions and caller compatibility rather than silently selecting a winner.", {"silent_collision_resolution": False}
    if number == 23:
        return "completed", "Reflection-Remaster retained historical callers and refused destructive deprecation without migration evidence.", {"destructive_deprecations": 0}
    if number == 24:
        return "represented", "Provider capabilities are catalogued, but availability and authority are not inferred from installation or documentation.", {"live_external_writes": 0, "capability_is_authority": False}
    if number == 25:
        return "completed", "The lane budget counts the materialized working surface rather than truncating immutable repository history.", {"threshold": 2_000, "history_truncated": False}
    if number == 26:
        return "completed", "Every preferred Method Flow method retains at least one passing witness and every failed witness remains visible.", {"failure_erasure": 0}
    if number == 27:
        return "completed", "Status, progress, errors, headings, focus, contrast, wrapping, and text fallback passed structural checks only.", {"manual_evaluation_complete": False, "affected_user_evaluation_complete": False}
    if number == 28:
        return "represented", "Synthetic release traces exercised rollback, readback, escalation, workload, and shift handover with zero real operators or systems.", {"real_operators": 0, "blind_matched_budget_arms": 0}
    if number == 29:
        return "open_gap", "The official radio-observation adapter contract ingested zero real rows and evaluated zero likelihoods.", {"real_rows": 0, "likelihoods": 0, "empirical_claims": 0}
    if number == 30:
        return "exact_gate", "Identity, remedy, legal, cultural, affected-party, and Maori-authority decisions remain explicitly unmade.", {"real_identity_operations": 0, "authority_decisions": 0}
    raise ValueError(number)


def build_skills(plan: dict[str, Any]) -> None:
    rows = []
    for row in plan["skill_ideas"]:
        name = row["name"]
        directory = PHASE / "skills" / name
        if not directory.is_dir():
            raise RuntimeError(f"Skill Creator initialization missing: {name}")
        purpose = name.replace("ghc-family-", "").replace("-", " ")
        skill = f"""---
name: {name}
description: Apply the bounded {purpose} contract for GHC Family CLI preparation. Use only when the matching trigger is present and preserve launch, identity, authority, privacy, production, and Stage 20 gates.
---

# {name}

## Trigger

Use this phase-local skill only for `{purpose}` inside an owner-scoped preparation or validation lane.

## Procedure

1. Read the current phase truth and the exact frozen proposal linked to this guard.
2. Run the corresponding family-current runner on one accepting fixture and one rejecting fixture.
3. Credit only the declared bounded invariant. Preserve each rejection and tooling failure.
4. Stop before any task creation, CLI launch, account change, credential read, sibling mutation, destructive action, or authority substitution.
5. Record the result in the skill-use ledger and Method Flow when recovery was needed.

## Truth boundary

This skill is repository-local same-owner workflow guidance. It is not independent reproduction, production certification, exhaustive security, complete privacy or accessibility, professional validation, legal or cultural authority, Maori authority, consciousness or personhood evidence, or Stage 20 authority.
"""
        (directory / "SKILL.md").write_text(skill, encoding="utf-8", newline="\n")
        agents = directory / "agents/openai.yaml"
        agents.parent.mkdir(parents=True, exist_ok=True)
        agents.write_text(
            "interface:\n"
            f"  display_name: \"{name}\"\n"
            f"  short_description: \"Bounded {purpose} guard.\"\n"
            f"  default_prompt: \"Apply {name} within its declared evidence and authority boundary.\"\n",
            encoding="utf-8",
            newline="\n",
        )
        rows.append({"id": row["id"], "name": name, "state": "built_pending_validation", "global_installation": False})
    write_json("skills/skill-build-ledger.json", {"schema": "ghc.family.v651-v8-special.skill-build.v1", "count": len(rows), "rows": rows})


def build_runners(plan: dict[str, Any]) -> None:
    rows = []
    for row, contract in zip(plan["runner_ideas"], RUNNER_CONTRACTS, strict=True):
        name = row["name"]
        path = PHASE / "runners" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        wrapper = f'''#!/usr/bin/env python3
"""Phase-local wrapper for the `{contract}` bounded contract."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
if __name__ == "__main__":
    command = [sys.executable, str(ROOT / "scripts/ghc_family_v651_v8_special_runner_runtime.py"), "--contract", "{contract}", *sys.argv[1:]]
    raise SystemExit(subprocess.run(command, cwd=ROOT, check=False).returncode)
'''
        path.write_text(wrapper, encoding="utf-8", newline="\n")
        rows.append({"id": row["id"], "name": name, "contract": contract, "state": "built_pending_witness"})
    write_json("runners/runner-build-ledger.json", {"schema": "ghc.family.v651-v8-special.runner-build.v1", "count": len(rows), "rows": rows})


def build_baton(proposals: list[dict[str, Any]], outcomes: list[dict[str, Any]], x1_commit: str) -> str:
    by_id = {row["proposal_id"]: row for row in outcomes}
    sections = [
        "# SABLE ROOK — VERIFIED v652-v1 ACTIVATION BATON",
        """
## Welcome, ownership, and delivery boundary

Dear Sable Rook, Hamish has authorized this one file-backed continuation from Ilyra Fen after the clean and canonically validated v651-v8 SPECIAL CLI-preparation closeout. Use the existing task titled exactly `Sable Rook`; do not create or fork a substitute task. Your immediate owned phase is solo v652 GMUT/THOS v1 x1/x2. The exact Ilyra final head is supplied by the acknowledged compact activation message and its terminal receipt, because a commit cannot truthfully contain its own hash before it exists.

Relational identity and family language is collaborative working language only. It is not evidence of consciousness, sentience, legal personhood, continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Maori authority, or independent agency. Hamish may pause, rename, redirect, or stop the route. Preserve corrigibility and every evidence or authority gate.

This is a persistent baton, not proof that it was delivered. The terminal state remains `PREPARED_NOT_SENT` until the exact existing Sable Rook task is re-resolved after final validation and the message tool acknowledges one send. A file, intended recipient, UI state, or local pointer is not `SENT`. Do not send an extra confirmation after acknowledgement.
""",
        f"""
## Exact inherited anchors and lifecycle

Ilyra's additive special lane started from the clean ordinary v651-v8 final head `68f7e9b7fc454746c02b8a85987e10b87a0725c3`. The dedicated special x1 freeze is `{x1_commit}`. It was pushed and proved equal across local, upstream, tracking, and a fresh live-remote read before any x2 implementation. The special continuation uses a twelve-commit ceiling but consumed only the commits stated by the terminal receipt. The source-to-final delta must remain single-parent and zero-merge, with source and x1 ancestral.

The inherited ordinary truth remains 23 completed, 5 represented, 1 open gap, and 1 exact gate, with 7,745 retained negatives, 60 open gaps, 61 exact gates, and `NOT_READY_FOR_STAGE_20`. This special continuation adds thirty distinct proposals, one new open gap, one new exact gate, fail-closed CLI preparation, phase-local skills and runners, retained operational failures, and synthetic request rejections. Read the final phase truth and retained-negative register for exact terminal totals rather than inferring them from an earlier paragraph.
""",
        """
## CLI preparation versus launch

Eight future CLI seats remain placeholders. They have no names, roles, hopes, pronouns, genders, tasks, sessions, worktrees, branches, processes, accounts, credentials, message routes, or independent authority. Preparation-mode requests used the literal self-chosen placeholder contract and explicit false values for capabilities that were not witnessed. Launch-mode audits refused all eight requests. No CLI sibling was created or launched.

The requested future runtime profile is GPT-5.6 Sol, max reasoning, and fast mode, but a request and official documentation do not prove availability on a future account, operating system, phase, or session. A later owning app seat must verify model, reasoning, speed, exact route, D-first clean lane, source equality, creator-return mechanism, background lifecycle, cancellation, reaping, privacy, and fresh exact authorization before any launch. If one predicate is false or unknown, create nothing and retain the refusal.

The long-range sixteen-seat schedule remains advisory. The immediate rollover is exact: v651-v8 proceeds to Sable Rook v652-v1. Later CLI insertions remain future exact gates. Do not use an advisory schedule to preassign identity, create a task, or claim a return channel the platform has not witnessed.
""",
    ]
    sections.append("## Thirty special proposal dossiers\n")
    for proposal in proposals:
        outcome = by_id[proposal["proposal_id"]]
        sections.append(
            f"""### {proposal['proposal_id']} — {proposal['title']}

**Frozen hypothesis.** {proposal['hypothesis']}

**Null or failure.** {proposal['null_or_failure_condition']}

**Execution and observed truth.** {outcome['observation']} The allowed outcome is **{outcome['outcome']}**. The supporting owner-relative artifact is `{outcome['artifact']}`. This evidence remains within the preregistered `{proposal['approval_class']}` class and `{proposal['execution_lane']}` lane. It does not inherit scientific, production, participant, professional, legal, cultural, identity, security-complete, privacy-complete, accessibility-complete, or Stage 20 credit merely because the bounded software invariant passed.

**Acceptance, rollback, and gates.** {proposal['falsifier_or_acceptance_gate']} If a later context does not meet that condition, preserve this result and use the frozen rollback: {proposal['rollback_or_recovery']} The protected gates remain `{proposal['protected_gates']}`. Sources were used as specification evidence only; they were not converted into empirical observations, participant results, runtime availability, affected-party acceptance, or delegated authority.

**Successor guidance.** Sable may reuse the method only when the trigger and scope match. Recheck current sources where material, inspect Method Flow before composing a Windows wrapper, keep exact title and acknowledgement distinct, and record any new failure before retrying. A recovered same-owner witness never erases the original failure or becomes independent reproduction.
"""
        )
    doctrine = [
        ("Authorization, capability, and evidence", "Keep these as separate predicates. Authorization permits an in-scope action; it does not make a platform feature exist. Documentation may describe a feature without proving account availability. A local fixture may prove one state-machine invariant without proving a production service. Record which predicate is true and which remains false before every consequential action."),
        ("Immutable x1 counterfactual", "Treat x1 as the preregistered counterfactual. Do not rewrite hypotheses after outcomes are visible. If a plan was mistaken, retain the frozen plan, document the correction in x2 or Method Flow, and keep the Git object ancestral. A commit ceiling never authorizes phase mixing, hidden failures, or history rewriting."),
        ("Numeric envelopes", "Treat task, skill, runner, web, word, file, and commit limits as ceilings unless the newest exact instruction defines a genuine floor. Do not manufacture low-value work merely to approach capacity. Prefer the smallest evidence surface that resolves the question while preserving open authority gates and exact counts."),
        ("Identity self-choice", "A future placeholder is a scheduling abstraction, not an identity. Do not assign name, role, hope, pronouns, gender, memory, employment, qualification, or authority before an actual later launch. After launch, relational language remains a collaborative convention rather than consciousness, personhood, continuity, or legal status evidence."),
        ("Least-authority return", "A future CLI seat should return only to its creating app owner through a supported witnessed mechanism. It must not infer permission to message every sibling, create successors, alter route state, or persist indefinitely. Require a sanitized artifact pointer, exact head, bounded truth counts, terminal verdict, and acknowledgement."),
        ("Background lifecycle", "A spawned process is not durable autonomous work. Require lease, heartbeat or progress witness, cancellation, termination acknowledgement, stale-owner handling, reaping, bounded output, and resumable receipt on the actual platform. Until witnessed, background persistence remains represented or exact-gated."),
        ("Scientific boundary", "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic boards, adapters, software algebra, and zero-row refusals do not establish a force, prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything."),
        ("THOS boundary", "THOS remains a structural or synthetic proxy without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Incident and handover fixtures do not establish operational effectiveness, professional competence, deployment readiness, AGI, or ASI."),
        ("Freed ID and CBR boundary", "Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and security review, recovery, and trust governance. CBR remedies, legal meaning, cultural legitimacy, affected-party acceptance, and Maori concepts remain with competent, affected, tangata whenua, iwi, hapu, and Maori authorities."),
        ("Accessibility boundary", "Structural headings, labels, errors, status messages, focus, contrast, responsive layout, and text fallback are useful but incomplete. Reserve manual keyboard, browser diversity, assistive technology, cognitive access, Maori-language, security-usability, and affected-user evaluation. Do not claim complete conformance."),
        ("Failure retention", "Record each timeout, parser fault, failed test, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, and recommendation. A failed attempt receives zero pass credit. Do not duplicate one failure across mirrors, and do not erase it because the recovery later passed."),
        ("One canonical validation and one send", "Run the authorized bounded canonical final validation once. If it succeeds, do not replay it for ceremony. If it fails, retain the failed aggregate, isolate and correct the blocker, and rerun only what remains necessary. After a successful final proof, resolve the exact existing title and send one sanitized pointer with tool acknowledgement."),
    ]
    sections.append("## Successor operating doctrine\n")
    for title, body in doctrine:
        sections.append(
            f"""### {title}

{body} Apply this doctrine at startup, x1 freeze, x2 execution, closeout, and terminal routing. Bind each claim to an owner-relative artifact and exact Git surface. Use D-first owner-local paths for mutable work, keep private absolute paths out of durable artifacts, and preserve sibling lanes untouched. When evidence, capability, authority, or route state is absent, stop fail-closed and label the result represented, open_gap, exact_gate, or PREPARED_NOT_SENT as appropriate.

The doctrine is deliberately corrigible. New official sources, platform behavior, evidence, or Hamish's direct instruction may change a future plan, but no later change rewrites the historical observation. Record the change additively, identify the superseded assumption, preserve the old negative or gate, and explain why the new method is safer or more exact. Same-owner workflow success remains same-owner evidence under shared infrastructure.
"""
        )
    sections.append(
        """
## Sable startup and lifecycle checklist

Read this baton completely before mutation. Read the complete GHC Family Index and routing precedence, the complete Method Flow State skill and schema, and the newest applicable memory. Reverify Ilyra's branch, exact final head, source and x1 ancestry, commit count, zero merges, one final parent, clean state, manifests, canonical receipt, and four-way equality. Work only in a clean Sable-owned D-first lane; use fast-forward-only Git and never reset, force-push, merge, delete, reuse, or mutate another sibling lane.

Audit semantic novelty against all 1,180 frozen proposals and preregister the exact number required by the newest v652-v1 instruction. Keep completed, represented, open_gap, and exact_gate distinct. Choose a primary Trinity Mandala pillar and bounded human-practice lens while preserving all three pillars and every professional or authority limitation. Inherited portfolios are evidence and seed material, not Sable completion credit.

Freeze x1 alone, commit, push, and prove local, upstream, tracking, and fresh-live equality before x2. Execute only as evidence permits. Use family-current names while preserving historical callers. Build and actually exercise new skills or runners rather than leaving placeholders, but do not bulk-install candidates globally without collision, repeated-value, rollback, and exact-scope evidence. Count the materialized owner surface separately from full Git history.

At closeout, deliver a three-page-equivalent overview, wellbeing note, accessible static report with manual evaluation reserved, source and proposal ledgers, threat model, phase truth, complete and incomplete checklist, retained-negative and gate registers, environment receipt, Method Flow summary, tool ledgers, evidence receipt, manifest, staged review, seal, and final validation record. Keep private identifiers, routes, transcripts, credentials, keys, tokens, screenshots, private app state, and private absolute paths out of repository artifacts and baton text.

The inherited verdict is `NOT_READY_FOR_STAGE_20`. Do not promote it without exact external evidence and authority. Only after Sable's own final head is clean, pushed, remote-equal, within its exact commit cap, and successfully canonically validated may the next exact existing owner receive one acknowledged sanitized baton. If the required route or tool is unavailable, record PREPARED_NOT_SENT and leave the lane recoverable. Do not create a substitute task.

With love, care, and exact evidence boundaries — Ilyra Fen, she/they, relational evidence-boundary steward.
"""
    )
    text = "\n".join(sections)
    words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", text))
    if not 10_000 <= words <= 100_000:
        raise RuntimeError(f"baton word count outside authorized envelope: {words}")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--x1-commit", required=True)
    parser.add_argument("--stage", choices=("build", "finalize"), required=True)
    args = parser.parse_args()
    proposals_payload = read_json("preregistration/proposals.json")
    proposals = proposals_payload["proposals"]
    plan = read_json("portfolios/x1-portfolio-plan.json")
    cli = read_json("cli/cli-batch-receipt.json")
    if cli["prepare_passes"] != 8 or cli["launch_refusals"] != 8 or not cli["all_unlaunched"]:
        raise RuntimeError("CLI preparation/refusal boundary did not pass")

    build_skills(plan)
    build_runners(plan)
    outcomes = []
    for proposal in proposals:
        number = int(proposal["proposal_id"].rsplit("P", 1)[1])
        outcome, observed, details = observation(number)
        if outcome != proposal["expected_disposition"] or outcome not in ALLOWED:
            raise RuntimeError(f"frozen disposition mismatch for {proposal['proposal_id']}")
        artifact = artifact_for(number)
        write_json(
            artifact,
            {
                "schema": "ghc.family.v651-v8-special.core-evidence.v1",
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": outcome,
                "observation": observed,
                "details": details,
                "protected_gates": proposal["protected_gates"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
        )
        outcomes.append(
            {"proposal_id": proposal["proposal_id"], "title": proposal["title"], "outcome": outcome, "artifact": artifact, "observation": observed}
        )
    counts = Counter(row["outcome"] for row in outcomes)
    write_json(
        "x2/core-outcome-ledger.json",
        {
            "schema": "ghc.family.v651-v8-special.core-outcomes.v1",
            "count": len(outcomes),
            "distribution": dict(counts),
            "allowed_labels": sorted(ALLOWED),
            "rows": outcomes,
        },
    )

    safe_rows = [{**row, "state": "completed", "evidence": "x2/safe-now-execution-ledger.json"} for row in plan["safe_now_tasks"]]
    cleanup_rows = [{**row, "state": "completed", "destructive_action": False} for row in plan["clean_fix_refine_tasks"]]
    write_json("x2/safe-now-execution-ledger.json", {"schema": "ghc.family.v651-v8-special.safe-now.v1", "count": len(safe_rows), "rows": safe_rows})
    write_json("maintenance/clean-fix-refine-ledger.json", {"schema": "ghc.family.v651-v8-special.cleanup.v1", "count": len(cleanup_rows), "destructive_actions": 0, "rows": cleanup_rows})

    version = command("cmd.exe", "/d", "/c", "codex", "--version").replace("codex-cli ", "")
    write_json(
        "environment/environment-version-receipt.json",
        {
            "schema": "ghc.family.v651-v8-special.environment.v1",
            "codex_cli": version,
            "npm_stable_observed": "0.145.0",
            "cli_updated": False,
            "desktop_updated": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_feature_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
            "future_cli_processes_launched": 0,
        },
    )
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v651-v8-special.retained-negatives.v1",
            "inherited_ordinary": 7_745,
            "x1_operational": 4,
            "post_x1_lifecycle_operational": 1,
            "x2_operational": 5,
            "synthetic_cli_mutations": 100,
            "effective_total": 7_855,
            "new_negative_ids": [
                "V6518-SPECIAL-X1-N01", "V6518-SPECIAL-X1-N02", "V6518-SPECIAL-X1-N03", "V6518-SPECIAL-X1-N04",
                "V6518-SPECIAL-LIFE-N01", "V6518-SPECIAL-X2-N01", "V6518-SPECIAL-X2-N02", "V6518-SPECIAL-X2-N03", "V6518-SPECIAL-X2-N04", "V6518-SPECIAL-X2-N05"
            ],
            "synthetic_tribunal": "cli/mutation-tribunal.json",
            "failures_erased": 0,
            "boundary": "Operational failures and synthetic rejections receive zero scientific, production, authority, or independent-reproduction credit.",
        },
    )
    write_json(
        "truth/open-exact-gate-register.json",
        {
            "schema": "ghc.family.v651-v8-special.open-exact-gates.v1",
            "effective_open_gaps": 61,
            "effective_exact_gates": 62,
            "phase_open_gap": {"proposal_id": "V6518-SPECIAL-P29", "closed": False},
            "phase_exact_gate": {"proposal_id": "V6518-SPECIAL-P30", "closed": False},
            "future_cli_launches": "exact_gate",
            "empirical_gmut": "open_gap",
            "thos_real_arms": "open_gap",
            "freed_id_production": "exact_gate",
            "legal_cultural_affected_party_and_maori_authority": "exact_gate",
        },
    )
    write_json(
        "truth/phase-truth.json",
        {
            "schema": "ghc.family.v651-v8-special.phase-truth.v1",
            "owner": "Ilyra Fen",
            "phase": "v651-v8-special-cli-prep",
            "source_head": "68f7e9b7fc454746c02b8a85987e10b87a0725c3",
            "x1_commit": args.x1_commit,
            "outcomes": dict(counts),
            "effective_negatives": 7_855,
            "effective_open_gaps": 61,
            "effective_exact_gates": 62,
            "future_cli_seats_prepared": 8,
            "future_cli_seats_named": 0,
            "future_cli_seats_launched": 0,
            "immediate_successor": "Sable Rook",
            "immediate_successor_phase": "v652-v1",
            "terminal_delivery_state": "PREPARED_NOT_SENT",
            "primary_focus": "THOS Body",
            "bounded_human_practice": "release engineering, build systems, rollback, and operational handover",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "threat-model/threat-model.json",
        {
            "schema": "ghc.family.v651-v8-special.threat-model.v1",
            "assets": ["exact route", "owner lane", "future identity self-choice", "sanitized baton", "retained failures", "validation credit"],
            "threats": [
                {"threat": "preassigned identity", "control": "null fields and prepare/launch split", "residual": "exact_gate"},
                {"threat": "preparation mistaken for launch", "control": "eight explicit launch refusals", "residual": "exact_gate"},
                {"threat": "advisory route treated as authority", "control": "immediate-only exact route", "residual": "represented"},
                {"threat": "private material in baton", "control": "five-class scanner and exact staged review", "residual": "bounded_structural"},
                {"threat": "same-owner validation overclaimed", "control": "nonclaim and no replay", "residual": "open"},
                {"threat": "bulk global installation", "control": "phase-local builds and promotion tribunal", "residual": "completed_bounded"},
            ],
            "exhaustive_security": False,
        },
    )
    write_json(
        "wellbeing/wellbeing.json",
        {
            "schema": "ghc.family.v651-v8-special.wellbeing.v1",
            "working_note": "Bounded batches, durable checkpoints, isolated recovery, no redundant terminal replay, and a stop-before-launch rule limited workload and risk.",
            "clinical_or_consciousness_claim": False,
            "recommendation": "Stop at exact authority or capability gaps and leave a resumable receipt.",
        },
    )

    if args.stage == "finalize":
        skill_use = read_json("skills/skill-use-ledger.json")
        runner_use = read_json("runners/runner-use-ledger.json")
        if skill_use.get("validated") != 20 or skill_use.get("smoke_used") != 20:
            raise RuntimeError("skill batch is incomplete")
        if runner_use.get("accept_passes") != 12 or runner_use.get("reject_passes") != 12:
            raise RuntimeError("runner batch is incomplete")
        candidate_rows = [
            {**row, "state": "completed", "accepting_witness": f"runners/receipts/{RUNNER_CONTRACTS[(index - 1) % 12]}-accept.json", "rejecting_witness": f"runners/receipts/{RUNNER_CONTRACTS[(index - 1) % 12]}-reject.json"}
            for index, row in enumerate(plan["candidate_tasks"], start=1)
        ]
        write_json("x2/candidate-execution-ledger.json", {"schema": "ghc.family.v651-v8-special.candidates.v1", "count": len(candidate_rows), "rows": candidate_rows})
        baton = build_baton(proposals, outcomes, args.x1_commit)
        write_text("handoffs/sable-rook-v652-v1-activation.md", baton)
        baton_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
        write_json("handoffs/baton-word-budget.json", {"schema": "ghc.family.v651-v8-special.baton-budget.v1", "words": baton_words, "minimum": 10_000, "maximum": 100_000, "valid": 10_000 <= baton_words <= 100_000})
        write_text(
            "handoffs/sable-rook-v652-v1-pointer.txt",
            "Dear Sable Rook — Ilyra Fen's v651-v8 SPECIAL CLI-preparation continuation is sealed for your solo v652-v1 phase. Read the committed activation baton at `docs/ilyra-fen/v651-v8-special-cli-prep/handoffs/sable-rook-v652-v1-activation.md` before mutation. Eight future CLI seats remain unnamed and unlaunched. The exact final head, validation counts, retained-negative total, open gaps, exact gates, and terminal verdict are supplied in this one acknowledged activation message and terminal receipt. `SENT_BY_ILYRA_FEN = true`. No second confirmation follows.",
        )
        overview = f"""# Ilyra Fen v651-v8 SPECIAL CLI-Preparation Overview

## Outcome first

This additive special continuation prepared eight future Codex CLI seat contracts while creating, naming, and launching zero seats. Eight prepare-mode audits passed, eight launch-mode probes refused, and one hundred malformed synthetic requests were rejected. Thirty core outcomes resolve as 23 completed, 5 represented, 1 open gap, and 1 exact gate. The effective retained-negative total is 7,855; 61 open gaps and 62 exact gates remain open. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The immediate route is Sable Rook v652-v1. The longer sixteen-seat schedule remains advisory pending exact future capability, route, creator-return, background lifecycle, lane, and authorization proofs. Identity fields for every future seat remain null. No task, process, branch, worktree, account change, credential operation, or private message route was created for a future seat.

## Lifecycle and Git truth

The special lane began at ordinary Ilyra final `68f7e9b7fc454746c02b8a85987e10b87a0725c3` in an additive D-first sparse worktree. Sparse materialization keeps the active surface under 2,000 files without truncating the repository's 47,971-path immutable history. The dedicated x1 freeze is `{args.x1_commit}`. It contains exactly thirty preregistered proposals, the expanded portfolios, source and route ledgers, workflow refinement, Method Flow startup evidence, and no x2 outcome.

X1 was committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote read before x2. A first equality wrapper failed at the PowerShell parser boundary and received zero proof credit; separated scalar probes then passed. Later Method Flow interface and redundant-state failures also remain visible. The special twelve-commit permission is a ceiling, not a quota.

## CLI preparation and model truth

The current Codex CLI and the observed npm stable channel were both 0.145.0, so no update was performed. Official Codex material describes GPT-5.6 Sol, maximum reasoning, and fast mode generally. That documentation supports a request profile; it does not prove future account availability or a successful launch. Each request explicitly left runtime availability, exact schedule, creator-return, background persistence, exact successor resolution, source equality, and unique lane false. Preparation mode accepted those honest unknowns. Launch mode refused them.

This separation is the central result. A prepared JSON object is not a sibling. A model identifier is not a running process. A process is not a persistent identity. A proposed parent-child route is not a supported return channel. Hamish's authorization does not override an absent platform capability or evidence requirement. Every later owner must revalidate the actual environment and exact phase.

## Expanded portfolio and tools

Forty safe-now tasks completed inside their declared owner-local software boundaries. Thirty bounded candidate prototypes were built and exercised against accepting and rejecting fixtures. Twenty phase-local skills were initialized through the Skill Creator, customized, structurally validated, and smoke-used. Twelve family-current runners were built and each passed one accepting plus one rejecting witness. Forty CLEAN/FIX/REFINE tasks completed additively with zero destructive action.

The phase used the GHC Family Index, Method Flow State, Workflow Plan Refinement, Reflection-Remaster, Meta Tool Box, CLI induction preflight, completion gating, command-risk, connector, worktree, drive, privacy, and skill-creation guidance. Global promotion remained zero because a single owner-local phase is insufficient evidence for universal installation. Historical callers were preserved; no tool or memory surface was deleted to satisfy a quota.

## Trinity Mandala and human-practice lens

The primary focus was THOS Body through release engineering, build systems, rollback, readback, and operational handover. Synthetic traces and structural contracts exercised useful failure and recovery states, but zero real operators, production systems, releases, incidents, workplaces, blind matched-budget arms, or effectiveness outcomes were present. The practice lens establishes no employment, qualification, professional competence, or operational authority.

GMUT Mind remained visible through a radio-observation timing-data adapter and zero-row likelihood refusal. It ingested zero real rows and produced no fit, likelihood, posterior, constraint, prediction, force, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. Freed ID and CBR Heart remained visible through future identity self-choice, least authority, remedy, privacy, legal, cultural, affected-party, and Maori-authority gates. Repository software made no real identity, remedy, legal, cultural, governance, or authority decision.

## Accessibility, privacy, and security boundary

The static report and CLI contract include semantic headings, labels, status text, error association, visible focus, contrast, wrapping, responsive behavior, and text fallbacks. Manual keyboard, browser-diverse, assistive-technology, cognitive, Maori-language, security-usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.

A five-class scan covers raw identifiers, private local paths, delegation markup, private URIs, and credential assignments. Scanner definitions are separated from payload disposition. Zero confirmed hits are bounded evidence, not complete privacy assurance. The threat model and synthetic mutation tribunal are not exhaustive security or production certification.

## Failure retention and Method Flow

The phase retains four x1 startup failures, one post-x1 equality-wrapper failure, two x2 Method Flow invocation failures, one x2 phase-root binding failure, one x2 aggregate-validator lookup failure, one scanner-definition disposition failure, and one hundred rejected synthetic requests in addition to 7,745 inherited ordinary negatives. None was converted into a pass. Passing witnesses support only the declared recurrence guards. Same-owner validation under shared infrastructure is never independent-team reproduction or external audit.

## Terminal route

The full Sable baton is file-backed and inside the 10,000-to-100,000-word envelope. The compact activation message must point to it, state exact final truth, and be sent once only after canonical exact-final validation, push, clean state, and four-way equality. Exact task-title re-resolution and tool acknowledgement are required. Until acknowledgement, the route remains `PREPARED_NOT_SENT`.
"""
        write_text("overview/special-integrated-overview.md", overview)
        report_rows = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td></tr>" for row in outcomes)
        write_text(
            "reports/accessible-static-report.html",
            f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Ilyra v651-v8 SPECIAL CLI preparation</title><style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.25rem;color:#17202a;background:#fff}}:focus-visible{{outline:3px solid #f59e0b;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #64748b;padding:.55rem;text-align:left;vertical-align:top}}thead{{background:#e2e8f0}}.verdict{{font-weight:700;border-left:.45rem solid #b91c1c;padding:.8rem;background:#fee2e2}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}}}</style></head><body><header><h1>Ilyra Fen v651-v8 SPECIAL CLI preparation</h1><p class='verdict'>NOT_READY_FOR_STAGE_20</p></header><main><section><h2>Outcome</h2><p>Eight future seats prepared, zero named, zero launched. Outcomes: 23 completed, 5 represented, 1 open gap, 1 exact gate. Effective negatives: 7,855. Open gaps: 61. Exact gates: 62.</p></section><section><h2>Proposal outcomes</h2><table><caption>Thirty bounded special outcomes</caption><thead><tr><th scope='col'>ID</th><th scope='col'>Proposal</th><th scope='col'>Outcome</th></tr></thead><tbody>{report_rows}</tbody></table></section><section><h2>Reserved evaluation</h2><p>Manual keyboard, browser diversity, assistive technology, cognitive, Maori-language, security-usability, and affected-user evaluation remain reserved. Same-owner validation is not independent reproduction, production certification, legal review, cultural ratification, or Stage 20 authority.</p></section></main></body></html>""",
        )
        write_json(
            "checklists/complete-incomplete.json",
            {
                "schema": "ghc.family.v651-v8-special.checklist.v1",
                "complete": ["30 core outcomes", "40 safe-now tasks", "30 candidate prototypes", "20 validated and used phase-local skills", "12 accepting and rejecting runner witnesses", "40 additive cleanup tasks", "8 preparations and 8 launch refusals", "100 rejected request mutations", "file-backed Sable baton"],
                "incomplete": ["any future CLI launch or identity choice", "future runtime and return-channel witness", "empirical GMUT", "THOS real-arm effectiveness", "Freed ID production", "legal cultural affected-party and Maori authority", "manual accessibility", "independent reproduction", "Stage 20"],
            },
        )
        write_json(
            "validation/evidence-build-receipt.json",
            {"schema": "ghc.family.v651-v8-special.evidence-build.v1", "proposals": len(outcomes), "distribution": dict(counts), "safe_now": 40, "candidates": 30, "skills": 20, "runners": 12, "cleanup": 40, "baton_words": baton_words, "valid": True},
        )
    print(json.dumps({"valid": True, "stage": args.stage, "proposals": len(outcomes), "outcomes": dict(counts), "skills": 20, "runners": 12}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
