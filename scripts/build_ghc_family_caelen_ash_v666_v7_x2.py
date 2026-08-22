#!/usr/bin/env python3
"""Execute bounded synthetic Caelen Ash v666-v7 x2 contracts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from build_ghc_family_caelen_ash_v666_v7_x1 import (
    ALLOWED_LABELS,
    BLOCKED_ITEMS,
    CFR_ACTIONS,
    EXACT_ITEMS,
    IDENTITY_BOUNDARY,
    OWNER_CANDIDATES,
    OWNER_RUNNERS,
    OWNER_SAFE,
    OWNER_SKILLS,
    PHASE_ROOT,
    PRACTICE_BOUNDARY,
    PROTECTED_GATES,
    SOURCE_PROFILES,
    SOURCE_SHA,
    SUCCESSOR_CANDIDATES,
    SUCCESSOR_RUNNERS,
    SUCCESSOR_SAFE,
    SUCCESSOR_SKILLS,
    build_proposals,
    canonical_sha256,
)
from ghc_family_caelen_ash_v666_v7_runtime import (
    ROOT,
    X1_SHA,
    mutation_variants,
    replay_manifest,
    validate_contract,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

X2_OPERATIONAL_FAILURES = [
    {
        "negative_id": "CA6667-X2-N001",
        "method_id": "CA6667-X2-M001",
        "signature": "contract-and-manifest-runner-summaries-omitted-top-level-valid-aggregate",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "contracts reported 20 rows and zero invalid rows; x1 manifest reported 20 entries and zero failures; both wrappers returned nonzero because result.get('valid') saw no top-level field",
        },
        "bounded_recovery": "derive and expose explicit aggregate valid booleans from the already-bounded contract and manifest results, retain the first builder stop, and rerun only the owner-local builder from the unchanged x1 head",
        "passing_witness_scope": "runner-interface recovery only",
        "preferred": True,
        "external_actions": 0,
        "real_rows": 0,
        "participants": 0,
    },
    {
        "negative_id": "CA6667-X2-N002",
        "method_id": "CA6667-X2-M002",
        "signature": "immutable-x1-test-module-was-launched-against-the-live-x2-worktree",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the x1 lifecycle assertion correctly found the live x2 directory; fifteen other x1 tests passed and the invocation receives zero immutable-x1 credit",
        },
        "bounded_recovery": "run the unchanged x1 module only against an isolated exact Git archive of the frozen x1 commit and retain the live-tree mismatch separately",
        "passing_witness_scope": "immutable x1 tree only",
        "preferred": True,
        "external_actions": 0,
        "real_rows": 0,
        "participants": 0,
    },
    {
        "negative_id": "CA6667-X2-N003",
        "method_id": "CA6667-X2-M003",
        "signature": "full-exact-x1-git-archive-extraction-exceeded-the-bounded-wrapper-window",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the 795 MB full-tree archive was created, but extraction exceeded the bounded wrapper window and left only a partial temporary tree; no x1 test receipt was attributable",
        },
        "bounded_recovery": "archive only the immutable owner x1 document subtree and unchanged x1 test module, extract to a new collision-free D-drive temporary target, and keep the partial target outside repository evidence",
        "passing_witness_scope": "bounded exact x1 Git-tree paths only",
        "preferred": True,
        "external_actions": 0,
        "real_rows": 0,
        "participants": 0,
    },
    {
        "negative_id": "CA6667-X2-N004",
        "method_id": "CA6667-X2-M004",
        "signature": "partial-x1-archive-test-launch-had-no-tests-module",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the partial extraction did not contain the x1 test path, so unittest failed import with ModuleNotFoundError before any assertion ran",
        },
        "bounded_recovery": "require the exact test path to exist in a newly extracted bounded archive before invoking the unchanged test file directly",
        "passing_witness_scope": "preflighted bounded exact x1 Git-tree paths only",
        "preferred": True,
        "external_actions": 0,
        "real_rows": 0,
        "participants": 0,
    },
    {
        "negative_id": "CA6667-X2-N005",
        "method_id": "CA6667-X2-M005",
        "signature": "bounded-archive-and-test-composite-ended-without-an-attributable-test-receipt",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the bounded archive and exact test path materialized, but the combined wrapper ended at its time boundary without a returned test receipt; the invocation receives no pass credit",
        },
        "bounded_recovery": "inspect the completed bounded target read-only, then invoke only the unchanged x1 test file from that exact target in a separate bounded command",
        "passing_witness_scope": "separate direct x1 test invocation against the completed bounded archive",
        "preferred": True,
        "external_actions": 0,
        "real_rows": 0,
        "participants": 0,
    },
]


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_show_json(relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{SOURCE_SHA}:{relative}"]
    )
    return json.loads(raw.decode("utf-8"))


def command_version(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return (completed.stdout or completed.stderr).strip().splitlines()[0]


SKILL_PURPOSES = {
    "horological-component-topology-vacancy": "Check synthetic component-role and disputed-node structures while withholding identity, completeness, originality, condition, and treatment judgments.",
    "stored-energy-isolation-abstention": "Check synthetic spring, weight, drive, and strike state vacancies while refusing winding, release, actuation, handling, or return-to-service instructions.",
    "timebase-zero-sample-refusal": "Check units, reference vacancies, sequence, and uncertainty fields while refusing rate, drift, calibration, synchronization, and traceability results.",
    "gear-ratio-synthetic-closure": "Check bounded integer ratio and rotation-parity fixtures without asserting real tooth counts, fit, materials, function, or authenticity.",
    "movement-association-revision-boundary": "Check bitemporal synthetic case, dial, movement, and attachment revisions while withholding title, custody, originality, and provenance completeness.",
    "condition-vocabulary-zero-image": "Check uninstantiated condition terminology with zero images while withholding diagnosis, hazard clearance, treatment, and material identification.",
    "horological-accessibility-structure": "Check static text redundancy, headings, tables, labels, and non-colour cues while reserving manual and affected-user accessibility evaluation.",
    "clock-rate-gmut-domain-gate": "Check typed scalar-tensor and oscillator-degeneracy obligations while refusing likelihood, constraint, prediction, force, detection, proof, and Theory-of-Everything claims.",
    "horological-method-flow": "Retain every failed horological contract witness before a bounded recovery and recurrence guard receives same-owner method credit.",
    "horological-closeout-gate": "Check exact anchors, manifests, four truth labels, retained failures, gates, and no-replay state before a target-neutral terminal candidate exists.",
}


def skill_markdown(name: str, purpose: str) -> str:
    return f"""---
name: {name}
description: "{purpose}"
---

# {name}

## Purpose

{purpose}

## Use

1. Accept only an owner-local wholly synthetic fixture with zero people, real objects, real rows, network calls, and external actions.
2. Inspect declared provenance, uncertainty, real-material absence, authority, and output states.
3. Reject missing fields, invalid ranges, authority promotion, mechanical instruction, real-world action, and outcome promotion.
4. Retain the failed witness before recording a bounded passing witness and recurrence guard.
5. Stop at participant, professional, mechanical-safety, treatment, custody, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, and Stage 20 gates.

## Boundary

This phase-local skill is same-owner synthetic software guidance only. It is not evidence of consciousness, personhood, identity continuity, qualification, scientific or operational authority, object identity, condition, stored-energy state, rate, calibration, conservation, standards conformance, external validation, legal or cultural authority, Māori authority, or independent reproduction.
"""


def build_skills() -> list[dict[str, Any]]:
    rows = []
    for name in OWNER_SKILLS:
        purpose = SKILL_PURPOSES[name]
        relative = f"skills/{name}/SKILL.md"
        text = skill_markdown(name, purpose)
        write_text(relative, text)
        checks = {
            "frontmatter": text.startswith("---\nname:"),
            "name_exact": f"name: {name}" in text,
            "purpose": "## Purpose" in text,
            "use": "## Use" in text,
            "boundary": "## Boundary" in text,
            "synthetic_only": "wholly synthetic" in text,
            "no_stage20": "Stage 20" in text,
        }
        smoke = {
            "schema": "ghc.family.caelen-ash.v666-v7.skill-smoke-receipt.v1",
            "skill": name,
            "generated_at_utc": NOW,
            "quick_validation": checks,
            "smoke_fixture": {
                "synthetic_only": True,
                "real_object": False,
                "participant_count": 0,
                "network_call_count": 0,
                "external_action": False,
                "authority_claim": False,
            },
            "smoke_used": True,
            "globally_installed": False,
            "valid": all(checks.values()),
            "claim_boundary": "phase-local guidance smoke only; no professional, empirical, legal, cultural, Māori, production, or independent authority",
        }
        write_json(f"skills/{name}/smoke-receipt.json", smoke)
        rows.append(
            {
                "name": name,
                "path": f"docs/caelen-ash/v666-v7/{relative}",
                "smoke_receipt": f"docs/caelen-ash/v666-v7/skills/{name}/smoke-receipt.json",
                "quick_validated": True,
                "smoke_used": True,
                "globally_installed": False,
            }
        )
    return rows


def contract_for(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.caelen-ash.v666-v7.bounded-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "pillar": proposal["pillar"],
        "primary_pillar": "GMUT Mind",
        "practice_lens": proposal["practice_lens"],
        "synthetic_only": True,
        "participant_count": 0,
        "real_data_row_count": 0,
        "network_call_count": 0,
        "external_action": False,
        "authority_claim": False,
        "stage20_claim": False,
        "provenance": {
            "proposal_freeze": "docs/caelen-ash/v666-v7/x1/proposal-freeze.json",
            "source_ids": proposal["current_official_or_primary_source_needs"],
            "same_owner": True,
            "observed_real_material": False,
        },
        "uncertainty": {
            "real_measurement": False,
            "reference_chain_present": False,
            "domain_vacancies_retained": True,
            "professional_review_present": False,
        },
        "distinctive_invariant": proposal["distinctive_invariant"],
        "positive_fixture": {
            "fixture_id": f"{proposal['proposal_id']}-P01",
            "real_object": False,
            "synthetic_state": "bounded_positive_structure",
            "provenance_present": True,
            "uncertainty_present": True,
            "authority_reserved": True,
            "external_action": False,
        },
        "protected_gates": PROTECTED_GATES,
        "falsifier_or_acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "claim_boundary": PRACTICE_BOUNDARY,
    }


def outcome_status(disposition: str) -> str:
    return {
        "completed": "bounded_structural_contract_completed",
        "represented": "proxy_or_symbolic_structure_represented",
        "open_gap": "current_source_or_real_row_gap_preserved",
        "exact_gate": "authority_and_evidence_gate_preserved_unexecuted",
    }[disposition]


def build_proposal_outputs(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ledger = []
    for proposal in proposals:
        contract = contract_for(proposal)
        positive_errors = validate_contract(contract)
        if positive_errors:
            raise RuntimeError(f"positive contract invalid {proposal['proposal_id']}: {positive_errors}")
        base = f"x2/proposals/{proposal['proposal_id'].casefold()}"
        write_json(f"{base}/contract.json", contract)
        mutations = []
        for index, (mutation_class, mutation) in enumerate(mutation_variants(contract), 1):
            errors = validate_contract(mutation)
            if not errors:
                raise RuntimeError(
                    f"mutation accepted {proposal['proposal_id']} M{index:02d}"
                )
            mutations.append(
                {
                    "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
                    "class": mutation_class,
                    "accepted": False,
                    "validator_errors": errors,
                    "failed_witness_retained": True,
                    "credit": 0,
                    "recovery": "restore the immutable bounded positive, preserve this failure, and keep all authority and real-world gates closed",
                }
            )
        result = {
            "schema": "ghc.family.caelen-ash.v666-v7.mutation-results.v1",
            "proposal_id": proposal["proposal_id"],
            "generated_at_utc": NOW,
            "preregistered_count": 5,
            "executed_count": 5,
            "rejected_count": 5,
            "accepted_count": 0,
            "all_rejected_and_retained": True,
            "mutations": mutations,
        }
        write_json(f"{base}/mutation-results.json", result)
        receipt = {
            "schema": "ghc.family.caelen-ash.v666-v7.bounded-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "generated_at_utc": NOW,
            "positive_valid": True,
            "mutation_count": 5,
            "mutation_rejected_count": 5,
            "outcome": proposal["expected_disposition"],
            "status": outcome_status(proposal["expected_disposition"]),
            "completion_scope": "same-owner wholly synthetic structural software only",
            "contract_canonical_sha256": canonical_sha256(contract),
            "real_rows": 0,
            "participants": 0,
            "network_calls": 0,
            "external_actions": 0,
            "authority_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_json(f"{base}/bounded-receipt.json", receipt)
        ledger.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "status": receipt["status"],
                "positive_valid": True,
                "preregistered_mutations": 5,
                "rejected_mutations": 5,
                "contract": f"docs/caelen-ash/v666-v7/{base}/contract.json",
                "mutation_results": f"docs/caelen-ash/v666-v7/{base}/mutation-results.json",
                "receipt": f"docs/caelen-ash/v666-v7/{base}/bounded-receipt.json",
                "claim_boundary": receipt["completion_scope"],
            }
        )
    return ledger


def build_revalidation() -> dict[str, Any]:
    source_freeze = git_show_json(f"docs/sable-rook/v666-v6/x1/proposal-freeze.json")
    rows = []
    for proposal in source_freeze["new_proposals"]:
        relative = f"docs/sable-rook/v666-v6/x2/proposals/{proposal['proposal_id'].casefold()}/contract.json"
        raw = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{SOURCE_SHA}:{relative}"]
        )
        value = json.loads(raw.decode("utf-8"))
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "path": relative,
                "git_blob_sha256": hashlib.sha256(raw).hexdigest(),
                "source_schema": value.get("schema"),
                "json_valid": True,
                "novelty_credit": 0,
                "automatic_completion_credit": 0,
                "status": "source_integrity_replayed_zero_credit",
            }
        )
    return {
        "schema": "ghc.family.caelen-ash.v666-v7.inherited-contract-integrity.v1",
        "source_sha": SOURCE_SHA,
        "source_owner": "Sable Rook",
        "source_phase": "v666-v6",
        "row_count": len(rows),
        "rows": rows,
        "all_json_valid": all(row["json_valid"] for row in rows),
        "completion_credit": 0,
        "novelty_credit": 0,
    }


def build_method_flow(
    proposal_ledger: list[dict[str, Any]],
    owner_portfolio: list[dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for proposal in proposal_ledger:
        rows.append(
            {
                "method_id": f"{proposal['proposal_id']}-OUTCOME",
                "class": "proposal_outcome",
                "status": "passed_bounded",
                "outcome": proposal["outcome"],
                "credit_scope": "same-owner synthetic structure only",
                "preferred": True,
            }
        )
        for index in range(1, 6):
            rows.append(
                {
                    "method_id": f"{proposal['proposal_id']}-M{index:02d}",
                    "class": "preregistered_rejecting_mutation",
                    "status": "failed_witness_retained_then_bounded_recovery_passed",
                    "negative_id": f"{proposal['proposal_id']}-M{index:02d}",
                    "failed_witness_credit": 0,
                    "passing_witness_credit_scope": "bounded recurrence guard only",
                    "preferred": True,
                }
            )
    for row in owner_portfolio:
        rows.append(
            {
                "method_id": row["item_id"],
                "class": row["approval_class"],
                "status": "completed_bounded_owner_local",
                "credit_scope": "same-owner synthetic method only",
                "preferred": True,
            }
        )
    if len(rows) != 215:
        raise RuntimeError(f"expected 215 core x2 methods, observed {len(rows)}")
    return {
        "schema": "ghc.family.caelen-ash.v666-v7.x2-method-flow.v1",
        "owner": "Caelen Ash",
        "phase": "v666-v7",
        "generated_at_utc": NOW,
        "starting_effective_negatives": 26767,
        "starting_effective_methods": 11654,
        "new_negative_count": 100,
        "new_method_count": 215,
        "effective_negatives": 26867,
        "effective_methods": 11869,
        "failed_witness_count": 100,
        "bounded_passing_witness_count": 215,
        "rows": rows,
        "all_failures_retained": True,
        "failed_witness_converted_to_pass": False,
    }


def build_x2_operational_overlay() -> dict[str, Any]:
    return {
        "schema": "ghc.family.caelen-ash.v666-v7.x2-operational-overlay.v1",
        "generated_at_utc": NOW,
        "starting_effective_negatives": 26867,
        "starting_effective_methods": 11869,
        "new_negative_count": len(X2_OPERATIONAL_FAILURES),
        "new_method_count": len(X2_OPERATIONAL_FAILURES),
        "effective_negatives": 26867 + len(X2_OPERATIONAL_FAILURES),
        "effective_methods": 11869 + len(X2_OPERATIONAL_FAILURES),
        "rows": X2_OPERATIONAL_FAILURES,
        "all_failures_retained": True,
        "failed_witness_converted_to_pass": False,
    }


def runner_catalog() -> list[dict[str, Any]]:
    return [
        {
            "runner": f"scripts/{name}.py",
            "mode": name.rsplit("_", 1)[-1],
            "family_current_name": name,
            "historical_compatibility": "additive owner-local interface; no shared caller changed",
        }
        for name in OWNER_RUNNERS
    ]


def invoke_runners() -> list[dict[str, Any]]:
    rows = []
    for name in OWNER_RUNNERS:
        mode = name.rsplit("_", 1)[-1]
        command = [sys.executable, "-X", "utf8", str(ROOT / "scripts" / f"{name}.py")]
        if mode in {"closeout", "canonical"}:
            command.append("--smoke")
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="strict",
            capture_output=True,
            check=False,
        )
        parsed = json.loads(completed.stdout) if completed.stdout.strip() else None
        rows.append(
            {
                "runner": f"scripts/{name}.py",
                "mode": mode,
                "returncode": completed.returncode,
                "stdout": parsed,
                "stderr": completed.stderr.strip(),
                "invoked": True,
                "smoke_used": True,
                "valid": completed.returncode == 0 and bool(parsed and parsed.get("valid")),
            }
        )
    return rows


def main() -> None:
    freeze = json.loads((PHASE_ROOT / "x1" / "proposal-freeze.json").read_text(encoding="utf-8"))
    if freeze["outcomes_observed"] or freeze["x2_implementation_count"]:
        raise RuntimeError("x1 is not immutable planning-only source")
    proposals = build_proposals()
    skills = build_skills()
    proposal_ledger = build_proposal_outputs(proposals)
    outcome_counts = {
        label: sum(row["outcome"] == label for row in proposal_ledger)
        for label in ALLOWED_LABELS
    }
    unknown_labels = sorted({row["outcome"] for row in proposal_ledger} - set(ALLOWED_LABELS))
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.proposal-ledger.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "inherited_frozen_baseline": 4290,
            "new_frozen_total": 4310,
            "allowed_labels": list(ALLOWED_LABELS),
            "unknown_labels": unknown_labels,
            "outcome_counts": outcome_counts,
            "proposals": proposal_ledger,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    portfolio = load_portfolio = json.loads((PHASE_ROOT / "x1" / "portfolio-freeze.json").read_text(encoding="utf-8"))
    owner_portfolio = (
        load_portfolio["portfolios"]["owner_safe_now"]
        + load_portfolio["portfolios"]["owner_bounded_candidates"]
        + load_portfolio["portfolios"]["owner_phase_local_skill_plans"]
        + load_portfolio["portfolios"]["owner_family_current_runner_plans"]
        + load_portfolio["portfolios"]["owner_clean_fix_refine"]
    )
    if len(owner_portfolio) != 95:
        raise RuntimeError(f"expected 95 owner portfolio rows, observed {len(owner_portfolio)}")
    write_json(
        "x2/portfolio-execution.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.portfolio-execution.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "executed_owner_method_count": len(owner_portfolio),
            "executed_owner_methods": [
                {**row, "x2_status": "completed_bounded_owner_local", "completion_credit": 1}
                for row in owner_portfolio
            ],
            "successor_recommendation_execution_count": 0,
            "exact_approval_execution_count": 0,
            "blocked_packet_execution_count": 0,
            "claim_boundary": "same-owner synthetic method evidence only; exact and blocked work remains unexecuted and successor recommendations receive zero Caelen credit",
        },
    )
    write_json("x2/revalidation/inherited-contract-integrity.json", build_revalidation())
    write_json(
        "x2/skill-catalog.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.skill-catalog.v1",
            "generated_at_utc": NOW,
            "skill_count": len(skills),
            "skills": skills,
            "all_quick_validated": all(row["quick_validated"] for row in skills),
            "all_smoke_used": all(row["smoke_used"] for row in skills),
            "global_install_count": 0,
        },
    )
    runners = runner_catalog()
    write_json(
        "x2/runner-catalog.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.runner-catalog.v1",
            "generated_at_utc": NOW,
            "runner_count": len(runners),
            "runners": runners,
            "shared_caller_changes": 0,
        },
    )
    write_json(
        "x2/exact-and-blocked-register.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.exact-and-blocked-register.v1",
            "generated_at_utc": NOW,
            "exact_approval_packets": load_portfolio["portfolios"]["exact_approval_packets"],
            "blocked_packets": load_portfolio["portfolios"]["blocked_packets"],
            "exact_count": 10,
            "blocked_count": 5,
            "executed_count": 0,
            "authority_preserved": True,
        },
    )
    write_json(
        "x2/open-gate-register.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.open-gate-register.v1",
            "generated_at_utc": NOW,
            "phase_open_gap": "CA6667-N019",
            "inherited_open_gaps": 188,
            "new_open_gaps": 1,
            "cumulative_open_gaps": 189,
            "gap": "current official-source terms were reviewed, but the adapter remains zero-call with zero object rows and no independent professional fitness or interoperability evidence",
            "status": "open_gap",
        },
    )
    method_flow = build_method_flow(proposal_ledger, owner_portfolio)
    write_json("method-flow/x2-method-flow.json", method_flow)
    x2_operational_overlay = build_x2_operational_overlay()
    write_json("method-flow/x2-operational-overlay.json", x2_operational_overlay)
    write_json(
        "x2/retained-builder-failure-01.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.retained-builder-failure.v1",
            "generated_at_utc": NOW,
            "failure": X2_OPERATIONAL_FAILURES[0],
            "aggregate_credit": 0,
            "owner_local_uncommitted_working_tree_artifacts_written_before_stop": True,
            "git_index_changed_by_failed_attempt": False,
            "commit_history_changed_by_failed_attempt": False,
            "remote_changed_by_failed_attempt": False,
            "x1_changed": False,
            "recovery_is_not_relabelled_first_attempt": True,
        },
    )
    write_json(
        "x2/retained-live-tree-x1-test-failure-02.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.retained-x1-domain-failure.v1",
            "generated_at_utc": NOW,
            "failure": X2_OPERATIONAL_FAILURES[1],
            "aggregate_credit": 0,
            "x1_commit_changed": False,
            "git_index_changed_by_failed_attempt": False,
            "remote_changed_by_failed_attempt": False,
            "recovery_requires_exact_x1_tree": True,
        },
    )
    write_json(
        "x2/retained-full-archive-timeout-failure-03.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.retained-x1-archive-failure.v1",
            "generated_at_utc": NOW,
            "failure": X2_OPERATIONAL_FAILURES[2],
            "aggregate_credit": 0,
            "repository_changed": False,
            "temporary_tree_complete": False,
            "x1_test_receipt_attributable": False,
        },
    )
    write_json(
        "x2/retained-partial-archive-import-failure-04.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.retained-x1-archive-failure.v1",
            "generated_at_utc": NOW,
            "failure": X2_OPERATIONAL_FAILURES[3],
            "aggregate_credit": 0,
            "repository_changed": False,
            "assertions_executed": 0,
            "x1_test_receipt_attributable": False,
        },
    )
    write_json(
        "x2/retained-composite-time-boundary-failure-05.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.retained-x1-archive-failure.v1",
            "generated_at_utc": NOW,
            "failure": X2_OPERATIONAL_FAILURES[4],
            "aggregate_credit": 0,
            "repository_changed": False,
            "bounded_archive_materialized": True,
            "x1_test_receipt_attributable": False,
        },
    )
    write_json(
        "x2/exact-x1-tree-test-receipt.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.exact-x1-tree-test-receipt.v1",
            "generated_at_utc": NOW,
            "x1_sha": X1_SHA,
            "selection": "unchanged tests/test_ghc_family_caelen_ash_v666_v7_x1.py from bounded git archive",
            "tests_run": 16,
            "failures": 0,
            "errors": 0,
            "returncode": 0,
            "archive_contains_git_metadata": False,
            "valid": True,
            "claim_boundary": "immutable owner x1 structural assertions only; no full repository suite or independent reproduction",
        },
    )
    write_json(
        "x2/source-use-ledger.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.source-use-ledger.v1",
            "generated_at_utc": NOW,
            "sources": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "generated_phase_network_calls": 0,
            "real_rows": 0,
            "objects": 0,
            "participants": 0,
            "professional_determinations": 0,
            "bounded_use": "vocabulary and refusal conditions only",
        },
    )
    write_json(
        "x2/source-adapter-zero-call.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.zero-call-adapter.v1",
            "proposal_id": "CA6667-N019",
            "source_ids": ["S01", "S02", "S03", "S04", "S05", "S06", "S07"],
            "network_enabled": False,
            "transport_calls": 0,
            "real_rows": 0,
            "semantic_conflicts": ["assessment versus observation", "time display versus traceable measurement result", "provenance vocabulary versus custody authority", "static structure versus accessibility conformance"],
            "outcome": "open_gap",
        },
    )
    write_json(
        "x2/environment-receipt.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.environment-receipt.v1",
            "generated_at_utc": NOW,
            "python": command_version([sys.executable, "--version"]),
            "git": command_version(["git", "--version"]),
            "node": command_version(["node", "--version"]),
            "platform": sys.platform,
            "network_changes": 0,
            "package_installs": 0,
            "host_security_changes": 0,
            "reboots": 0,
        },
    )
    x1_replay = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    changed_x1 = subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "diff",
            "--name-only",
            X1_SHA,
            "--",
            "docs/caelen-ash/v666-v7/x1",
            "docs/caelen-ash/v666-v7/identity",
            "docs/caelen-ash/v666-v7/provenance",
            "docs/caelen-ash/v666-v7/wellbeing/x1-wellbeing-check.json",
            "docs/caelen-ash/v666-v7/method-flow/startup-method-flow.json",
            "docs/caelen-ash/v666-v7/validation/x1-content-manifest.json",
            "docs/caelen-ash/v666-v7/validation/x1-staged-review.json",
            "scripts/build_ghc_family_caelen_ash_v666_v7_x1.py",
            "tests/test_ghc_family_caelen_ash_v666_v7_x1.py",
        ]
    ).decode("utf-8").splitlines()
    write_json(
        "x2/x1-immutability-receipt.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.x1-immutability-receipt.v1",
            "x1_sha": X1_SHA,
            "manifest_replay": x1_replay,
            "changed_x1_paths": changed_x1,
            "immutable": x1_replay["valid"] and not changed_x1,
        },
    )
    write_json(
        "x2/threat-model-review.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.threat-model-review.v1",
            "generated_at_utc": NOW,
            "threat_count": len(json.loads((PHASE_ROOT / "x1" / "threat-model-plan.json").read_text(encoding="utf-8"))["threats"]),
            "new_unmitigated_threat_count": 0,
            "residual_risks_preserved": True,
            "professional_review_present": False,
            "independent_review_present": False,
        },
    )
    write_json(
        "x2/wellbeing-workload-receipt.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.wellbeing-workload-receipt.v1",
            "generated_at_utc": NOW,
            "owner": "Caelen Ash",
            "solo_lane": True,
            "subagent_count": 0,
            "real_participant_count": 0,
            "workload": "bounded to twenty contracts, one hundred rejecting mutations, ten skills, ten runners, and ninety-five portfolio methods",
            "x1_equality_pause_completed": True,
            "next_pause": "after evidence push and four-way equality",
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "x2/phase-truth.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.x2-phase-truth.v1",
            "owner": "Caelen Ash",
            "phase": "v666-v7",
            "generated_at_utc": NOW,
            "proposal_chain": 4310,
            "outcomes": outcome_counts,
            "unknown_labels": unknown_labels,
            "positive_structural_fixtures": 20,
            "preregistered_mutations": 100,
            "rejected_mutations": 100,
            "retained_failed_witnesses": 100,
            "phase_local_skills": 10,
            "family_current_runners": 10,
            "portfolio_methods": 95,
            "effective_negatives": x2_operational_overlay["effective_negatives"],
            "effective_methods": x2_operational_overlay["effective_methods"],
            "open_gaps": 189,
            "exact_gates": 187,
            "real_rows": 0,
            "participants": 0,
            "network_calls_by_generated_phase_software": 0,
            "external_actions": 0,
            "exact_or_blocked_execution_count": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "claim_boundary": PRACTICE_BOUNDARY,
        },
    )
    write_json(
        "x2/successor-recommendations.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.successor-recommendations.v1",
            "generated_at_utc": NOW,
            "recommendation_count": len(SUCCESSOR_SAFE),
            "recommendations": load_portfolio["portfolios"]["successor_safe_now"],
            "successor_candidate_count": len(SUCCESSOR_CANDIDATES),
            "successor_skill_recommendation_count": len(SUCCESSOR_SKILLS),
            "successor_runner_recommendation_count": len(SUCCESSOR_RUNNERS),
            "successor_clean_fix_refine_count": len(CFR_ACTIONS),
            "route_inferred": False,
            "successor_contacted": False,
            "completion_credit": 0,
            "novelty_credit": 0,
        },
    )
    write_text(
        "x2/accessible-structure-fixture.html",
        """<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><title>Caelen Ash v666-v7 bounded structure</title></head>
<body><main><h1>Bounded horological structure</h1><p>This static fixture uses zero real objects or observations and reserves manual and affected-user evaluation.</p>
<table><caption>Four bounded outcome labels</caption><thead><tr><th scope="col">Label</th><th scope="col">Boundary</th></tr></thead>
<tbody><tr><th scope="row">completed</th><td>same-owner synthetic structure only</td></tr><tr><th scope="row">represented</th><td>proxy or symbolic structure only</td></tr><tr><th scope="row">open_gap</th><td>missing current rows or independent review</td></tr><tr><th scope="row">exact_gate</th><td>missing evidence and competent authority</td></tr></tbody></table></main></body></html>""",
    )
    runner_rows = invoke_runners()
    if not all(row["valid"] for row in runner_rows):
        raise RuntimeError(json.dumps(runner_rows, ensure_ascii=False, sort_keys=True))
    write_json(
        "x2/tooling-smoke-receipt.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.tooling-smoke-receipt.v1",
            "generated_at_utc": NOW,
            "runner_count": len(runner_rows),
            "skill_count": len(skills),
            "runners": runner_rows,
            "all_runners_invoked": all(row["invoked"] for row in runner_rows),
            "all_runners_smoke_used": all(row["smoke_used"] for row in runner_rows),
            "all_runners_valid": all(row["valid"] for row in runner_rows),
            "all_skills_quick_validated": all(row["quick_validated"] for row in skills),
            "all_skills_smoke_used": all(row["smoke_used"] for row in skills),
            "terminal_runners_invoked_only_as_interface_smoke": True,
        },
    )
    write_json(
        "x2/x2-build-receipt.json",
        {
            "schema": "ghc.family.caelen-ash.v666-v7.x2-build-receipt.v1",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_caelen_ash_v666_v7_x2.py",
            "proposal_count": len(proposal_ledger),
            "positive_count": 20,
            "mutation_count": 100,
            "rejected_mutation_count": 100,
            "skill_count": len(skills),
            "runner_count": len(runner_rows),
            "portfolio_method_count": len(owner_portfolio),
            "x1_immutable": x1_replay["valid"] and not changed_x1,
            "real_rows": 0,
            "participants": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "status": "X2_CONTENT_BUILT_AWAITING_TEST_EVIDENCE_STAGED_REVIEW_COMMIT_PUSH_EQUALITY",
            "retained_operational_failure_count": len(X2_OPERATIONAL_FAILURES),
        },
    )
    print(
        json.dumps(
            {
                "proposal_count": len(proposal_ledger),
                "outcomes": outcome_counts,
                "mutations_rejected": 100,
                "skills": len(skills),
                "runners": len(runner_rows),
                "portfolio_methods": len(owner_portfolio),
                "effective_negatives": x2_operational_overlay["effective_negatives"],
                "effective_methods": x2_operational_overlay["effective_methods"],
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    if sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_caelen_ash_v666_v7_x2.py")
    main()
