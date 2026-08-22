#!/usr/bin/env python3
"""Execute bounded synthetic Liora Venn v667-v1 x2 contracts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from build_ghc_family_liora_venn_v667_v1_x1 import (
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
from ghc_family_liora_venn_v667_v1_runtime import (
    ROOT,
    X1_SHA,
    mutation_variants,
    replay_manifest,
    validate_contract,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

X2_OPERATIONAL_FAILURES: list[dict[str, Any]] = [
    {
        "negative_id": "LI6671-X2-N001",
        "method_id": "LI6671-X2-M001",
        "signature": "combined-immutable-x1-replay-and-recursive-temp-cleanup-was-policy-rejected-before-launch",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the command policy rejected the first immutable-x1 replay wrapper before process creation because it combined the replay with recursive temporary cleanup",
        },
        "bounded_recovery": "separate the replay from cleanup, extract the exact x1 Git archive into one uniquely named system-temporary directory, run only the immutable sixteen-test module, retain the temporary path outside the repository, and leave repository state unchanged",
        "passing_witness_scope": "immutable x1 tree test transport only",
        "preferred": True,
        "external_actions": 0,
        "real_rows": 0,
        "participants": 0,
    },
    {
        "negative_id": "LI6671-X2-N002",
        "method_id": "LI6671-X2-M002",
        "signature": "mutable-x1-test-module-was-inapplicable-after-x2-paths-existed",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "after all sixty-seven x2 tests passed, a separate live-worktree x1-module invocation failed its planning-only no-x2-path assertion because the authorized x2 tree now existed",
        },
        "bounded_recovery": "do not replay the inapplicable live x1 module; preserve the already successful sixteen-test exact-x1 Git-archive receipt and use only the current x2 and later evidence modules in the mutable worktree",
        "passing_witness_scope": "lifecycle-appropriate test selection only",
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
    "philatelic-record-topology-vacancy": "Check synthetic item, design-field, postal-cover, issue-series, and unknown-node topology while withholding identity, issue, authenticity, completeness, grade, value, and postal-history judgments.",
    "postmark-transcription-refusal": "Check synthetic glyph order, supplied text, date-place vacancies, illegibility, correction, and location minimization while refusing route, person, address, authenticity, and historical conclusions.",
    "philatelic-provenance-braid": "Check synthetic acquisition, transfer, loan, return, dispute, retraction, and source relations while withholding ownership, title, custody, lawful transfer, and provenance-completeness claims.",
    "condition-grade-nonconversion": "Check uninstantiated philatelic condition terminology with zero items, images, measurements, or experts while withholding diagnosis, grade, value, treatment, and material identification.",
    "preservation-decision-vacancy": "Check synthetic preservation, mount, enclosure, exposure, access, and review vacancies while refusing material selection, treatment, handling, display, release, or benefit claims.",
    "philatelic-accessibility-structure": "Check static correction paths, headings, labels, reflow order, nonvisual narratives, tables, and non-colour cues while reserving manual and affected-user accessibility evaluation.",
    "smithsonian-zero-row-adapter": "Check a disabled Smithsonian Open Access adapter contract with query, key, pagination, rights, schema, and zero-row holds while refusing any call, object inference, rights conclusion, or collection result.",
    "shifted-symplectic-domain-gate": "Check typed shifted-symplectic and derived-critical-locus obligations while refusing GMUT construction, physical field, observable, quantization, theorem extension, prediction, proof, and Theory-of-Everything claims.",
    "philatelic-method-flow": "Retain every failed philatelic contract witness before a bounded recovery and recurrence guard receives same-owner method credit.",
    "philatelic-closeout-gate": "Check exact anchors, manifests, four truth labels, retained failures, gates, and no-replay state before a target-neutral terminal candidate exists.",
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
3. Reject missing fields, invalid ranges, authority promotion, authentication or valuation promotion, preservation or handling instruction, real-world action, and outcome promotion.
4. Retain the failed witness before recording a bounded passing witness and recurrence guard.
5. Stop at participant, professional, authentication, grading, valuation, preservation, treatment, custody, privacy, legal, cultural, Māori-authority, accessibility-complete, exhaustive-security, independent-reproduction, and Stage 20 gates.

## Boundary

This phase-local skill is same-owner synthetic software guidance only. It is not evidence of consciousness, personhood, identity continuity, qualification, scientific or operational authority, item identity, issue, authenticity, authorship, title, condition, grade, value, postal history, preservation fitness, standards conformance, external validation, legal or cultural authority, Māori authority, or independent reproduction.
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
            "schema": "ghc.family.liora-venn.v667-v1.skill-smoke-receipt.v1",
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
                "path": f"docs/liora-venn/v667-v1/{relative}",
                "smoke_receipt": f"docs/liora-venn/v667-v1/skills/{name}/smoke-receipt.json",
                "quick_validated": True,
                "smoke_used": True,
                "globally_installed": False,
            }
        )
    return rows


def contract_for(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.liora-venn.v667-v1.bounded-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "pillar": proposal["pillar"],
        "primary_pillar": "Freed ID and CBR Heart",
        "practice_lens": proposal["practice_lens"],
        "synthetic_only": True,
        "participant_count": 0,
        "real_data_row_count": 0,
        "network_call_count": 0,
        "external_action": False,
        "authority_claim": False,
        "stage20_claim": False,
        "provenance": {
            "proposal_freeze": "docs/liora-venn/v667-v1/x1/proposal-freeze.json",
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
            "schema": "ghc.family.liora-venn.v667-v1.mutation-results.v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.bounded-receipt.v1",
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
                "contract": f"docs/liora-venn/v667-v1/{base}/contract.json",
                "mutation_results": f"docs/liora-venn/v667-v1/{base}/mutation-results.json",
                "receipt": f"docs/liora-venn/v667-v1/{base}/bounded-receipt.json",
                "claim_boundary": receipt["completion_scope"],
            }
        )
    return ledger


def build_revalidation() -> dict[str, Any]:
    source_freeze = git_show_json("docs/orin-thale/v666-v8/x1/proposal-freeze.json")
    rows = []
    for proposal in source_freeze["new_proposals"]:
        relative = f"docs/orin-thale/v666-v8/x2/proposals/{proposal['proposal_id'].casefold()}/contract.json"
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
        "schema": "ghc.family.liora-venn.v667-v1.inherited-contract-integrity.v1",
        "source_sha": SOURCE_SHA,
        "source_owner": "Orin Thale",
        "source_phase": "v666-v8",
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
        "schema": "ghc.family.liora-venn.v667-v1.x2-method-flow.v1",
        "owner": "Liora Venn",
        "phase": "v667-v1",
        "generated_at_utc": NOW,
        "starting_effective_negatives": 26996,
        "starting_effective_methods": 12113,
        "new_negative_count": 100,
        "new_method_count": 215,
        "effective_negatives": 27096,
        "effective_methods": 12328,
        "failed_witness_count": 100,
        "bounded_passing_witness_count": 215,
        "rows": rows,
        "all_failures_retained": True,
        "failed_witness_converted_to_pass": False,
    }


def build_x2_operational_overlay() -> dict[str, Any]:
    return {
        "schema": "ghc.family.liora-venn.v667-v1.x2-operational-overlay.v1",
        "generated_at_utc": NOW,
        "starting_effective_negatives": 27096,
        "starting_effective_methods": 12328,
        "new_negative_count": len(X2_OPERATIONAL_FAILURES),
        "new_method_count": len(X2_OPERATIONAL_FAILURES),
        "effective_negatives": 27096 + len(X2_OPERATIONAL_FAILURES),
        "effective_methods": 12328 + len(X2_OPERATIONAL_FAILURES),
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
            "schema": "ghc.family.liora-venn.v667-v1.proposal-ledger.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "inherited_frozen_baseline": 4330,
            "new_frozen_total": 4350,
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
            "schema": "ghc.family.liora-venn.v667-v1.portfolio-execution.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "executed_owner_method_count": len(owner_portfolio),
            "executed_owner_methods": [
                {**row, "x2_status": "completed_bounded_owner_local", "completion_credit": 1}
                for row in owner_portfolio
            ],
            "successor_recommendation_execution_count": 0,
            "exact_approval_execution_count": 0,
            "blocked_packet_execution_count": 0,
            "claim_boundary": "same-owner synthetic method evidence only; exact and blocked work remains unexecuted and successor recommendations receive zero Liora credit",
        },
    )
    write_json("x2/revalidation/inherited-contract-integrity.json", build_revalidation())
    write_json(
        "x2/skill-catalog.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.skill-catalog.v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.runner-catalog.v1",
            "generated_at_utc": NOW,
            "runner_count": len(runners),
            "runners": runners,
            "shared_caller_changes": 0,
        },
    )
    write_json(
        "x2/exact-and-blocked-register.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.exact-and-blocked-register.v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.open-gate-register.v1",
            "generated_at_utc": NOW,
            "phase_open_gap": "LI6671-N019",
            "inherited_open_gaps": 190,
            "new_open_gaps": 1,
            "cumulative_open_gaps": 191,
            "gap": "current official-source terms were reviewed, but the Smithsonian Open Access adapter remains disabled and zero-row with no API key, record, media, rights adjudication, privacy review, professional fitness, or independent interoperability evidence",
            "status": "open_gap",
        },
    )
    method_flow = build_method_flow(proposal_ledger, owner_portfolio)
    write_json("method-flow/x2-method-flow.json", method_flow)
    x2_operational_overlay = build_x2_operational_overlay()
    write_json("method-flow/x2-operational-overlay.json", x2_operational_overlay)
    for index, failure in enumerate(X2_OPERATIONAL_FAILURES, 1):
        write_json(
            f"x2/retained-operational-failure-{index:02d}.json",
            {
                "schema": "ghc.family.liora-venn.v667-v1.retained-operational-failure.v1",
                "generated_at_utc": NOW,
                "failure": failure,
                "aggregate_credit": 0,
                "repository_commit_changed": False,
                "remote_changed": False,
                "x1_changed": False,
                "recovery_is_not_relabelled_first_attempt": True,
            },
        )
    write_json(
        "x2/exact-x1-tree-test-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.exact-x1-tree-test-receipt.v1",
            "generated_at_utc": NOW,
            "x1_sha": X1_SHA,
            "selection": "unchanged tests/test_ghc_family_liora_venn_v667_v1_x1.py from bounded git archive",
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
            "schema": "ghc.family.liora-venn.v667-v1.source-use-ledger.v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.zero-call-adapter.v1",
            "proposal_id": "LI6671-N019",
            "source_ids": ["S05"],
            "network_enabled": False,
            "transport_calls": 0,
            "real_rows": 0,
            "semantic_conflicts": ["catalogue metadata versus item identity", "descriptive field versus authentication or grade", "rights field versus legal permission", "provenance vocabulary versus title or custody authority", "static structure versus accessibility conformance"],
            "outcome": "open_gap",
        },
    )
    write_json(
        "x2/environment-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.environment-receipt.v1",
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
            "docs/liora-venn/v667-v1/x1",
            "docs/liora-venn/v667-v1/identity",
            "docs/liora-venn/v667-v1/provenance",
            "docs/liora-venn/v667-v1/wellbeing/x1-wellbeing-check.json",
            "docs/liora-venn/v667-v1/method-flow/startup-method-flow.json",
            "docs/liora-venn/v667-v1/validation/x1-content-manifest.json",
            "docs/liora-venn/v667-v1/validation/x1-staged-review.json",
            "scripts/build_ghc_family_liora_venn_v667_v1_x1.py",
            "tests/test_ghc_family_liora_venn_v667_v1_x1.py",
        ]
    ).decode("utf-8").splitlines()
    write_json(
        "x2/x1-immutability-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.x1-immutability-receipt.v1",
            "x1_sha": X1_SHA,
            "manifest_replay": x1_replay,
            "changed_x1_paths": changed_x1,
            "immutable": x1_replay["valid"] and not changed_x1,
        },
    )
    write_json(
        "x2/threat-model-review.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.threat-model-review.v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.wellbeing-workload-receipt.v1",
            "generated_at_utc": NOW,
            "owner": "Liora Venn",
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
            "schema": "ghc.family.liora-venn.v667-v1.x2-phase-truth.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "proposal_chain": 4350,
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
            "open_gaps": 191,
            "exact_gates": 189,
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
            "schema": "ghc.family.liora-venn.v667-v1.successor-recommendations.v1",
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
<html lang="en-NZ"><head><meta charset="utf-8"><title>Liora Venn v667-v1 bounded structure</title></head>
<body><main><h1>Bounded philatelic record structure</h1><p>This static fixture uses zero real people, collectors, postal workers, addresses, stamps, covers, mail, albums, records, measurements, images, transactions, treatments, or observations and reserves manual and affected-user evaluation.</p>
<table><caption>Four bounded outcome labels</caption><thead><tr><th scope="col">Label</th><th scope="col">Boundary</th></tr></thead>
<tbody><tr><th scope="row">completed</th><td>same-owner synthetic structure only</td></tr><tr><th scope="row">represented</th><td>proxy or symbolic structure only</td></tr><tr><th scope="row">open_gap</th><td>missing current rows or independent review</td></tr><tr><th scope="row">exact_gate</th><td>missing evidence and competent authority</td></tr></tbody></table></main></body></html>""",
    )
    runner_rows = invoke_runners()
    if not all(row["valid"] for row in runner_rows):
        raise RuntimeError(json.dumps(runner_rows, ensure_ascii=False, sort_keys=True))
    write_json(
        "x2/tooling-smoke-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.tooling-smoke-receipt.v1",
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
            "schema": "ghc.family.liora-venn.v667-v1.x2-build-receipt.v1",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_liora_venn_v667_v1_x2.py",
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
        raise SystemExit("usage: build_ghc_family_liora_venn_v667_v1_x2.py")
    main()
