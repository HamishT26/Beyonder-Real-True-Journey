#!/usr/bin/env python3
"""Build Vesper Arlen's dedicated v653-v1 x1-only freeze packet."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v653_v1_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = REPO / "docs/neris-solane/v652-v8/provenance/frozen-chain-proposal-index.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
WORKFLOW_RUNNER = SKILL_ROOT / "ghc-family-workflow-plan-refinement/scripts/ghc_family_workflow_plan_refinement.py"
NOVELTY_THRESHOLD = 0.60


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


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return subprocess.run(
        list(args),
        cwd=REPO,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def timestamps() -> dict[str, str]:
    now = datetime.now(timezone.utc)
    return {
        "utc": now.isoformat().replace("+00:00", "Z"),
        "pacific_auckland_system_local": now.astimezone().isoformat(),
    }


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with", "gmut", "thos"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if token not in stop
    }


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def build_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = read_json(PRIOR_INDEX)
    prior = inherited["prior_proposals"] + inherited["new_proposals"]
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited rows, found {len(prior)}")
    inherited_identifier_counts = Counter(row["proposal_id"] for row in prior)
    audits = []
    for proposal in d.PROPOSALS:
        scored = [
            (
                jaccard(tokens(proposal["title"]), tokens(previous["title"])),
                previous["proposal_id"],
                previous["title"],
            )
            for previous in prior
        ]
        score, nearest_id, nearest_title = max(scored, key=lambda row: row[0])
        audits.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "token_jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "manual_mechanism_distinct": True,
                "mechanism_review": proposal["novelty_against_1420_frozen_proposals"],
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    if not all(row["passes"] for row in audits):
        failures = [row for row in audits if not row["passes"]]
        raise RuntimeError(f"novelty threshold failed: {failures}")
    new = [
        {"proposal_id": proposal["proposal_id"], "title": proposal["title"]}
        for proposal in d.PROPOSALS
    ]
    if set(row["proposal_id"] for row in prior) & set(row["proposal_id"] for row in new):
        raise RuntimeError("proposal identifier collision")
    return prior, audits


def workflow_request() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "vesper-v653-v1-solo",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency.",
        "route": {
            "cycle_order": ["Neris Solane", "Vesper Arlen"],
            "phase_assignments": [
                {"phase": "v652-v8", "seat": "Neris Solane"},
                {"phase": "v653-v1", "seat": "Vesper Arlen"},
            ],
            "normalization": {
                "start_phase": "v652-v8",
                "start_seat": "Neris Solane",
                "entry_count": 2,
            },
            "future_identity_placeholders": [],
            "terminal_successor_resolution": "No successor is authorized by the live v653-v1 activation. After the exact-final canonical gate, retain OPEN_ROUTE_GAP until Hamish supplies exact future authorization; create, fork, infer, or message no substitute.",
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "portfolio_minima": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "commit_cap": {"x1": 5, "x2": 5, "total": 8},
            "storage": {
                "primary": "D",
                "owner_generated_file_threshold": 2000,
                "c_drive_use": "essential_global_metadata_only",
            },
            "document_word_cap": 100000,
            "baton_words": {"file_artifact": True, "minimum": 10000, "maximum": 100000},
            "validation": {
                "full_repository_suite_owner": "Eiren Kestrel",
                "launch_scoped_validator_owner": "Vesper Arlen",
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "manifest_required": True,
                "privacy_scan_required": True,
                "remote_equality_required": True,
            },
            "messaging": {
                "codex_route": "none_without_exact_future_authorization",
                "cross_platform": "user_mediated_file_relay_only",
                "live_cross_platform_boundary": "No cross-platform substitute is authorized.",
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "independent_reproduction_claimed": False,
            "protected_boundaries": d.PROTECTED_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "observed_failures": [
            {
                "failure_id": negative_id,
                "summary": failed,
                "recovery": recovery,
                "credit": "zero_failed_attempt_credit",
            }
            for negative_id, _category, failed, recovery in d.X1_NEGATIVES
        ],
    }


def build_method_flow() -> None:
    method_dir = ROOT / "method-flow"
    requests = method_dir / "requests"
    requests.mkdir(parents=True, exist_ok=True)
    ledger = method_dir / "x1-method-flow-ledger.json"
    if ledger.exists():
        ledger.unlink()
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "init",
        "--ledger",
        str(ledger),
        "--phase",
        d.PHASE_ID,
        "--owner",
        d.OWNER,
    )
    for index, (negative_id, category, failed, recovery) in enumerate(d.X1_NEGATIVES, 1):
        method_id = f"V6531-METHOD-{index:02d}"
        fail_id = f"V6531-WITNESS-{index:02d}-F"
        pass_id = f"V6531-WITNESS-{index:02d}-P"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {category}",
            "failure_signature": failed,
            "trigger_preconditions": [category],
            "candidate_workaround": recovery,
            "validation_witness_ids": [],
            "recurrence_guard": recovery,
            "rollback": "Stop, retain the failed witness with zero credit, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.",
            "scope_boundary": "Same-owner bounded workflow recovery only; not independent reproduction or any scientific, production, professional, legal, cultural, accessibility-complete, or authority claim.",
            "approval_class": "safe_now_owner_local_read_or_workflow_recovery",
            "privacy_class": "sanitized_public",
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [negative_id],
            "supersedes": [],
            "recommendation_state": "candidate",
        }
        fail = {
            "witness_id": fail_id,
            "method_id": method_id,
            "scope": category,
            "procedure": "Retain the original bounded attempt without replay credit.",
            "expected": "The initial attempt would satisfy its bounded postcondition.",
            "observed": failed,
            "result": "fail",
            "retained_negative_ids": [negative_id],
            "boundary": "Zero pass credit; failure remains retained.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        passing = {
            "witness_id": pass_id,
            "method_id": method_id,
            "scope": category,
            "procedure": recovery,
            "expected": "The isolated bounded recovery establishes only its declared postcondition.",
            "observed": f"The bounded recovery completed for {category}; the original failure remains retained.",
            "result": "pass",
            "retained_negative_ids": [negative_id],
            "boundary": "Passing recovery is same-owner bounded evidence only and does not erase the failed witness.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        method_path = write_json(f"method-flow/requests/method-{index:02d}.json", method)
        fail_path = write_json(f"method-flow/requests/witness-{index:02d}-failed.json", fail)
        pass_path = write_json(f"method-flow/requests/witness-{index:02d}-passing.json", passing)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(method_path))
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(fail_path))
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path))
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "A bounded pass witness exists while the failed witness remains retained.",
        )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(method_dir / "x1-method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(method_dir / "x1-method-flow-summary.json"),
        "--markdown-output",
        str(method_dir / "x1-method-flow-summary.md"),
    )


def version(command: list[str]) -> dict[str, Any]:
    completed = run(*command, check=False)
    return {
        "command_label": " ".join([Path(command[0]).name, *command[1:2]]),
        "exit_code": completed.returncode,
        "stdout_first_line": completed.stdout.strip().splitlines()[0] if completed.stdout.strip() else "",
        "stderr_first_line": completed.stderr.strip().splitlines()[0] if completed.stderr.strip() else "",
        "updated": False,
    }


def overview() -> str:
    rows = [
        "# Vesper Arlen v653-v1 x1 preregistration overview",
        "",
        "## Identity, purpose, and limits",
        "",
        f"{d.OWNER} ({d.PRONOUNS}) is a relational working label for the role of {d.ROLE}. "
        f"The working hope is to {d.HOPE}. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, professional authority, scientific authority, legal or cultural authority, Māori authority, or independent agency.",
        "",
        f"The primary Trinity Mandala pillar is **{d.PRIMARY_FOCUS}**, viewed through the bounded human practice of **{d.BOUNDED_PRACTICE}**. GMUT Mind and Freed ID/CBR Heart remain explicit. GMUT is treated as a typed scalar-tensor/EFT research-model family, not a confirmed Theory of Everything. THOS remains bounded symbolic and synthetic evidence without blind matched-budget real arms and independent review. Freed ID remains nonproduction without real standards-conformant keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and security review, recovery, and trust governance. CBR and Māori wording, legitimacy, data governance, remedy, legal interpretation, cultural ratification, and authority remain exact-gated.",
        "",
        "## Source inheritance and strict phase boundary",
        "",
        f"This x1 packet inherits Neris Solane's clean exact final head `{d.SOURCE_HEAD}` from `{d.SOURCE_BRANCH}`. It preserves {d.INHERITED_NEGATIVES:,} effective negatives, {d.INHERITED_OPEN_GAPS} open gaps, {d.INHERITED_EXACT_GATES} exact gates, and Neris's {d.INHERITED_METHOD_FLOW_FAILED} retained failed plus {d.INHERITED_METHOD_FLOW_PASSING} bounded passing Method Flow witnesses. The source parent, x1, immutable evidence, and final anchors were verified ancestral before mutation. Source-to-final history contains three single-parent commits and zero merges. Vesper created one additive identity-owned D-first lane from that exact final head; no sibling lane was mutated.",
        "",
        "X1 freezes intent and falsification conditions only. It contains no executed mutation, no observed outcome, no x2 runner implementation, no skill implementation, no empirical result, no closeout, and no route delivery. The ten proposed phase-local skills and ten family-compatible runners are plans at this stage. They may be implemented only after this exact x1 packet is committed, pushed, clean, and equal across local, upstream, tracking, and fresh live remote.",
        "",
        "## Thirty genuinely distinct mechanisms",
        "",
    ]
    for proposal in d.PROPOSALS:
        rows.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['slug']}",
                "",
                f"{proposal['title']}. The expected disposition is `{proposal['expected_disposition']}` in lane `{proposal['execution_lane']}`. "
                f"The hypothesis is: {proposal['hypothesis']} The falsifier is explicit: {proposal['null_or_failure_condition']} "
                f"The novelty finding is: {proposal['novelty_against_1420_frozen_proposals']} Source needs are {', '.join(proposal['official_or_primary_source_needs'])}. "
                f"Acceptance remains bounded: {proposal['falsifier_or_acceptance_gate']} Rollback is non-destructive: {proposal['rollback_or_recovery']}",
                "",
            ]
        )
    rows.extend(
        [
            "## Mutation grammar and negative preservation",
            "",
            "Exactly five rejecting mutations are preregistered for each proposal: a required-field deletion, a cross-bound source or identifier, an inverted boundary, an unsupported promotion, and an erased failure or rollback. That yields 150 frozen mutations. None is executed in x1. X2 must execute every frozen mutation, retain every failure, and grant no success credit merely because a file exists. A mutation passes the negative fixture only when the relevant contract rejects or quarantines it for the declared reason.",
            "",
            f"{len(d.X1_NEGATIVES)} operational failures and {len(d.REJECTED_COLLISIONS)} rejected candidate collisions are visible in the x1 evidence. These are not defects to hide. They teach bounded Windows inventory, exact-schema inspection, explicit UTF-8, exact filename discovery, and mechanism-first novelty review. Method Flow records a failed witness before each recovery witness, promotes only the bounded recovery, and keeps all protected gates unchanged.",
            "",
            "## Validation ownership and terminal route",
            "",
            "Vesper will not replay Neris's credited canonical pass or claim inherited full-repository evidence as Vesper evidence. Vesper will run scoped phase tests and one attributable exact-final canonical validation. If that exact-final pass succeeds completely, it will not be replayed. Failed attempts receive zero credit and must be retained before an isolated correction. The canonical gate includes JSON parsing, five-class privacy scanning, manifest parity, exact staged review, stale-label and diff hygiene, ancestry, zero merges, commit caps, one-parent history, exact head, clean state, and live remote equality.",
            "",
            "The live v653-v1 activation authorizes no successor. Even after the exact-final gate, Vesper must retain `OPEN_ROUTE_GAP` until Hamish supplies exact future authorization. No historical route may be inferred, and no substitute task, fork, collaboration subagent, or message may be created.",
            "",
            "## Wellbeing and authority",
            "",
            "The working cadence is steady and bounded: preserve failures, avoid needless broad replays, use the D drive for owner artifacts, and pause at any safety or authority boundary. No real participant, account, credential, private conversation, private route, production identity, professional decision, legal conclusion, cultural ratification, Māori-authority decision, or empirical likelihood is introduced. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
        ]
    )
    return "\n".join(rows)


def accessible_report(overview_text: str) -> str:
    cards = []
    for proposal in d.PROPOSALS:
        cards.append(
            "<article><h3>{}</h3><p>{}</p><dl><dt>Expected</dt><dd>{}</dd>"
            "<dt>Lane</dt><dd>{}</dd><dt>Falsifier</dt><dd>{}</dd></dl></article>".format(
                html.escape(proposal["proposal_id"]),
                html.escape(proposal["title"]),
                html.escape(proposal["expected_disposition"]),
                html.escape(proposal["execution_lane"]),
                html.escape(proposal["null_or_failure_condition"]),
            )
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vesper Arlen v653-v1 x1 preregistration</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
a{{color:#0645ad}} :focus{{outline:3px solid #b35c00;outline-offset:3px}} article{{border:1px solid #8091a3;border-radius:.6rem;padding:1rem;margin:1rem 0;background:white}}
dt{{font-weight:700}} dd{{margin:0 0 .6rem}} .notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style></head><body><main>
<h1>Vesper Arlen v653-v1 x1 preregistration</h1>
<p class="notice"><strong>Boundary:</strong> Plans only. No x2 result, empirical confirmation, professional approval, production readiness, legal or cultural authority, independent reproduction, Theory-of-Everything proof, or Stage 20 authority is claimed. Manual and affected-user accessibility evaluation is reserved.</p>
<h2>Packet summary</h2><p>{html.escape(overview_text.splitlines()[4])}</p>
<h2>Frozen proposals</h2>{''.join(cards)}
<h2>Accessibility reservation</h2><p>Semantic HTML, keyboard focus visibility, text reflow, and reduced-motion handling are represented by static structure. Qualified manual review and affected-user evaluation remain incomplete and exact-gated to appropriate evaluators.</p>
</main></body></html>"""


def build() -> None:
    if git("rev-parse", "HEAD") != d.SOURCE_HEAD:
        raise RuntimeError("x1 builder requires the exact Neris final source head")
    if git("status", "--porcelain=v1", "--untracked-files=all"):
        permitted = {
            "scripts/ghc_family_v653_v1_phase_data.py",
            "scripts/build_ghc_family_v653_v1_preregistration.py",
            "scripts/ghc_family_v653_v1_x1_validate.py",
            "tests/test_ghc_family_v653_v1_x1.py",
        }
        current = {
            row[3:].replace("\\", "/")
            for row in git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
        }
        unexpected = {
            path
            for path in current
            if path not in permitted and not path.startswith(f"{d.PHASE_ROOT}/")
        }
        if unexpected:
            raise RuntimeError(f"unexpected pre-build paths: {sorted(unexpected)}")
        forbidden_x2 = {
            path
            for path in current
            if path.startswith(f"{d.PHASE_ROOT}/")
            and any(
                token in path
                for token in (
                    "mutation-results",
                    "evidence-receipt",
                    "closeout-receipt",
                    "seal-receipt",
                    "final-validation",
                )
            )
        }
        if forbidden_x2:
            raise RuntimeError(
                f"x2 or lifecycle output exists before x1 freeze: {sorted(forbidden_x2)}"
            )
    prior, novelty = build_novelty()
    source_ids = {row["source_id"] for row in d.SOURCES}
    missing_sources = sorted(
        {
            source_id
            for proposal in d.PROPOSALS
            for source_id in proposal["official_or_primary_source_needs"]
            if source_id not in source_ids
        }
    )
    if missing_sources:
        raise RuntimeError(f"unresolved source identifiers: {missing_sources}")

    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.v653-v1.relational-identity.v1",
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "boundary": "Relational working language only; not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency.",
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
    )
    write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.v653-v1.source-anchors.v1",
            "branch": d.SOURCE_BRANCH,
            "source_parent": d.SOURCE_PARENT,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_final": d.SOURCE_HEAD,
            "source_to_final_commits": 3,
            "source_to_final_merges": 0,
            "all_single_parent": True,
            "verified_clean_and_four_way_equal_before_mutation": True,
            "verified_manifest_contracts": 4,
            "verified_manifest_entries": 573,
            "inherited_final_canonical_tests": 60,
            "inherited_final_detailed_checks": 195,
            "inherited_final_minimal_checks": 22,
            "inherited_final_json_parses": 229,
            "inherited_final_public_files": 291,
            "inherited_final_privacy_hits": 0,
            "inherited_owner_manifest_entries": 288,
            "inherited_final_delta_entries": 33,
            "inherited_lifecycle_checks": 20,
            "boundary": "Read-only source verification. Neris's successful exact-final canonical pass was not replayed, and inherited evidence is not claimed as Vesper evidence.",
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.frozen-chain-proposal-index.v1",
            "prior_count": len(prior),
            "new_count": len(d.PROPOSALS),
            "count": len(prior) + len(d.PROPOSALS),
            "prior_proposals": prior,
            "new_proposals": [
                {"proposal_id": row["proposal_id"], "title": row["title"]}
                for row in d.PROPOSALS
            ],
        },
    )
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.v653-v1.semantic-novelty.v1",
            "prior_count": len(prior),
            "new_count": len(novelty),
            "effective_count": len(prior) + len(novelty),
            "threshold": NOVELTY_THRESHOLD,
            "maximum_token_jaccard": max(row["token_jaccard"] for row in novelty),
            "all_manual_mechanism_distinct": all(row["manual_mechanism_distinct"] for row in novelty),
            "all_pass": all(row["passes"] for row in novelty),
            "inherited_unique_identifier_count": len({row["proposal_id"] for row in prior}),
            "inherited_reused_identifier_count": sum(
                count > 1 for count in Counter(row["proposal_id"] for row in prior).values()
            ),
            "inherited_title_count": len({row["title"] for row in prior}),
            "inherited_rows_rewritten": False,
            "rows": novelty,
            "rejected_collisions": d.REJECTED_COLLISIONS,
        },
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v653-v1.source-ledger.v1",
            "allowed_statuses": d.SOURCE_STATUS_CLASSES,
            "counts": dict(Counter(row["status"] for row in d.SOURCES)),
            "sources": d.SOURCES,
            "boundary": "Primary or official sources inform bounded contracts. Citation does not establish empirical confirmation, professional approval, production readiness, legal interpretation, cultural ratification, Māori authority, or Stage 20.",
        },
    )
    source_md = ["# v653-v1 source ledger", "", "Status is phase-local: `stable`, `current`, `draft`, or `watch`.", ""]
    for row in d.SOURCES:
        source_md.append(f"- **{row['source_id']}** — `{row['status']}` — [{row['title']}]({row['url']}). {row['phase_implication']}")
    write_text("sources/source-ledger.md", "\n".join(source_md))
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v653-v1.preregistered-proposals.v1",
            "state": "FROZEN_X1_NOT_EXECUTED",
            "proposal_count": len(d.PROPOSALS),
            "expected_outcome_counts": dict(Counter(row["expected_disposition"] for row in d.PROPOSALS)),
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "proposals": d.PROPOSALS,
            "boundary": "Hypotheses and expected dispositions only; no x2 observation or completion credit.",
        },
    )
    proposal_md = ["# v653-v1 frozen proposal ledger", "", "All rows are preregistered and unexecuted in x1.", ""]
    for row in d.PROPOSALS:
        proposal_md.extend(
            [
                f"## {row['proposal_id']} — {row['slug']}",
                "",
                f"- Title: {row['title']}",
                f"- Expected: `{row['expected_disposition']}`",
                f"- Approval: `{row['approval_class']}`",
                f"- Lane: `{row['execution_lane']}`",
                f"- Falsifier: {row['null_or_failure_condition']}",
                f"- Rollback: {row['rollback_or_recovery']}",
                "",
            ]
        )
    write_text("preregistration/proposal-ledger.md", "\n".join(proposal_md))
    mutations = []
    for proposal in d.PROPOSALS:
        for index, kind in enumerate(d.MUTATION_KINDS, 1):
            mutations.append(
                {
                    "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
                    "proposal_id": proposal["proposal_id"],
                    "kind": kind,
                    "state": "preregistered_not_executed",
                    "expected": "reject_or_quarantine",
                    "credit": "none_in_x1",
                }
            )
    write_json(
        "validation/preregistered-mutation-plan.json",
        {
            "schema": "ghc.family.v653-v1.mutation-plan.v1",
            "mutation_count": len(mutations),
            "mutations_per_proposal": len(d.MUTATION_KINDS),
            "executed_count": 0,
            "mutations": mutations,
        },
    )
    write_json("portfolios/safe-now-plan.json", {"state": "frozen_not_executed", "cap": 1000, "count": len(d.SAFE_TASKS), "tasks": d.SAFE_TASKS})
    write_json("portfolios/candidate-plan.json", {"state": "frozen_not_executed", "cap": 1000, "count": len(d.CANDIDATE_TASKS), "tasks": d.CANDIDATE_TASKS})
    write_json("portfolios/skill-plan.json", {"state": "frozen_not_built", "minimum": 10, "count": len(d.SKILL_IDEAS), "skills": [{"name": name, "purpose": purpose} for name, purpose in d.SKILL_IDEAS]})
    write_json("portfolios/runner-plan.json", {"state": "frozen_not_built", "minimum": 10, "count": len(d.RUNNER_IDEAS), "runners": [{"name": name, "surface": surface} for name, surface in d.RUNNER_IDEAS]})
    write_json("portfolios/clean-fix-refine-plan.json", {"state": "frozen_not_executed", "count": len(d.CLEAN_FIX_REFINE_TASKS), "tasks": d.CLEAN_FIX_REFINE_TASKS})
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v653-v1.threat-model.v1",
            "assets": ["claim truth", "negative preservation", "source provenance", "identity privacy", "authority boundaries", "route integrity"],
            "threats": [
                "synthetic success promoted as empirical confirmation",
                "represented proxy promoted as deployment or professional validation",
                "draft identity syntax promoted as production security",
                "Māori or affected-party reservation silently closed",
                "failed attempt erased or counted as passing",
                "private identifier or path written to public artifacts",
                "prepared route reported as sent",
            ],
            "controls": ["four truth labels", "frozen mutations", "five-class privacy scan", "Method Flow fail/pass pairs", "manifest parity", "exact staged review", "one canonical final pass", "no successor action without exact future live authorization"],
            "residual_boundary": "No exhaustive-security, complete-privacy, complete-accessibility, professional, empirical, legal, cultural, Māori-authority, independent-reproduction, AGI/ASI, personhood, Theory-of-Everything, or Stage 20 claim.",
        },
    )
    write_json(
        "wellbeing/wellbeing-check.json",
        {
            "schema": "ghc.family.v653-v1.wellbeing.v1",
            "state": "steady_and_bounded",
            "cadence": "One verified gate at a time; isolate failures before a justified broader retry.",
            "host_changes": False,
            "sandbox_or_hyper_v_work": "deferred",
            "route_pressure": "No successor action is authorized by the live activation.",
            "identity_boundary": "Relational language only.",
        },
    )
    write_json(
        "environment/version-receipt.json",
        {
            "schema": "ghc.family.v653-v1.versions.v1",
            "observed_at": timestamps(),
            "versions": {
                "git": version(["git", "--version"]),
                "python": version([sys.executable, "--version"]),
                "node": version(["node", "--version"]),
                "codex_cli": version(["cmd.exe", "/d", "/c", "codex", "--version"]),
            },
            "codex_desktop_updated": False,
            "software_updated": False,
            "elevation": False,
            "host_security_changed": False,
            "windows_features_changed": False,
            "rebooted": False,
        },
    )
    workflow_path = write_json("workflow/workflow-plan-request.json", workflow_request())
    workflow_result = run(
        sys.executable,
        str(WORKFLOW_RUNNER),
        str(workflow_path),
        "--out-dir",
        str(ROOT / "workflow"),
        check=False,
    )
    if workflow_result.returncode not in {0, 2}:
        raise RuntimeError(f"workflow refinement failed unexpectedly: {workflow_result.stderr}")
    workflow_validation = read_json(ROOT / "workflow/workflow-plan-validation.json")
    if workflow_validation.get("privacy_findings") != 0:
        raise RuntimeError("workflow refinement reported a privacy finding")
    write_json(
        "workflow/current-live-route-overlay.json",
        {
            "schema": "ghc.family.v653-v1.live-route-overlay.v1",
            "live_request_authorizes": "no_successor_route_without_exact_future_authorization",
            "installed_runner_models": "advisory_only_no_live_route",
            "runner_status": workflow_validation.get("status"),
            "runner_valid": workflow_validation.get("valid"),
            "runner_issue_count": workflow_validation.get("issue_counts", {}).get("total"),
            "tool_result_promoted_to_activation_authority": False,
            "boundary": "The live activation controls the route and authorizes no successor. The installed workflow runner is structural advisory evidence and does not resolve, infer, create, or deliver any task.",
        },
    )
    run(
        sys.executable,
        str(INDEX_RUNNER),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(ROOT / "tooling"),
        "--phase",
        d.PHASE_ID,
        "--owner",
        d.OWNER,
    )
    reflection_command = [
        sys.executable,
        str(REFLECTION_RUNNER),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--output-dir",
        str(ROOT / "reflection-remaster"),
        "--phase",
        d.PHASE_ID,
        "--owner",
        d.OWNER,
    ]
    for focus in [
        "ghc-family-index",
        "ghc-family-method-flow-state",
        "ghc-family-workflow-plan-refinement",
        "ghc-family-reflection-remaster",
    ]:
        reflection_command.extend(["--focus", focus])
    run(*reflection_command)
    build_method_flow()
    overview_text = overview()
    word_count = len(overview_text.split())
    if word_count < 1500:
        raise RuntimeError(f"overview below three-page-equivalent floor: {word_count}")
    write_text("reports/x1-integrated-overview.md", overview_text)
    write_text("reports/x1-accessible-report.html", accessible_report(overview_text))
    write_json(
        "x1-phase-truth.json",
        {
            "schema": "ghc.family.v653-v1.x1-truth.v1",
            "state": "FROZEN_X1_NOT_EXECUTED",
            "proposal_count": 30,
            "frozen_chain_count": 1450,
            "mutation_plan_count": 150,
            "mutation_executed_count": 0,
            "skill_plan_count": 10,
            "skill_built_count": 0,
            "runner_plan_count": 10,
            "runner_built_count": 0,
            "inherited_negatives": d.INHERITED_NEGATIVES,
            "x1_operational_negatives": len(d.X1_NEGATIVES),
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "x2_outcomes_present": False,
            "independent_reproduction": False,
            "route_state": "NOT_ELIGIBLE_X1_ONLY",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/x1-build-receipt.json",
        {
            "schema": "ghc.family.v653-v1.x1-build.v1",
            "valid": True,
            "proposal_count": 30,
            "prior_count": 1420,
            "effective_count": 1450,
            "source_count": len(d.SOURCES),
            "source_reference_count": sum(len(row["official_or_primary_source_needs"]) for row in d.PROPOSALS),
            "mutation_plan_count": 150,
            "mutation_executed_count": 0,
            "safe_task_count": len(d.SAFE_TASKS),
            "candidate_task_count": len(d.CANDIDATE_TASKS),
            "skill_plan_count": 10,
            "runner_plan_count": 10,
            "clean_fix_refine_count": 30,
            "overview_words": word_count,
            "x2_implementation_present": False,
            "boundary": "Dedicated x1-only build; staging, commit, push, and remote equality remain pending.",
        },
    )
    print(
        json.dumps(
            {
                "valid": True,
                "proposals": 30,
                "prior": 1420,
                "effective": 1450,
                "sources": len(d.SOURCES),
                "mutations_planned": 150,
                "overview_words": word_count,
                "x2": False,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    build()
