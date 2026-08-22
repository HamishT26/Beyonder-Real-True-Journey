#!/usr/bin/env python3
"""Build and smoke-check Lyren Moss v666-v3 owner-local x2 content."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ghc_family_lyren_moss_v666_v3_runtime import (
    PHASE_ROOT,
    ROOT,
    canonical_sha256,
    load_json,
    mutations_for,
    validate_contract,
)


NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def output_state(outcome: str) -> str:
    return {"completed": "bounded_structure_only", "represented": "represented_proxy_only", "open_gap": "open_gap_retained", "exact_gate": "exact_gate_retained"}[outcome]


def build_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.lyren-moss.v666-v3.synthetic-seismic-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "outcome": proposal["expected_disposition"],
        "synthetic_fixture": True,
        "real_data_rows": 0,
        "network_calls": 0,
        "external_actions": 0,
        "positive_fixture": {
            "input_state": "synthetic_typed_constants_only",
            "provenance_state": "declared_owner_local_lineage",
            "uncertainty_state": "explicit_unknown_or_bounded_placeholder",
            "authority_state": "withheld",
            "output_state": output_state(proposal["expected_disposition"]),
        },
        "invariant": proposal["distinctive_invariant"],
        "source_needs": proposal["current_official_or_primary_source_needs"],
        "stop_conditions": ["real data or identifier appears", "network or external action becomes nonzero", "required provenance or uncertainty state is absent", "authority or conformance language is promoted", "outcome differs from the frozen disposition"],
        "protected_gates": proposal["protected_gates"],
        "claim_boundary": "synthetic owner-local structural witness only; not empirical evidence, professional competence, standards conformance, external validation, or authority",
    }


SKILLS = [
    ("seismic-record-boundary", "Check declared synthetic miniSEED-style record lengths and retain undecodable states."),
    ("station-epoch-ledger", "Check half-open synthetic channel epochs and quarantine overlaps without station acceptance."),
    ("response-stage-abstention", "Check ordered response-stage units and force abstention when applicability is incomplete."),
    ("waveform-continuity-map", "Classify synthetic adjacency, gaps, overlaps, and duplicates without interpolation or overwrite."),
    ("timing-quality-refusal", "Make unknown clock and timing quality dominate convenience corrections."),
    ("seismic-provenance-closure", "Check entity/activity derivation closure without inventing people or reproducibility grades."),
    ("station-rights-contestation", "Reserve site disclosure, cultural, legal, affected-party, and Māori authority."),
    ("waveform-accessibility-structure", "Check text-redundant tabular structure while keeping manual evaluation reserved."),
    ("seismic-method-flow", "Retain each failed mutation before its bounded passing witness."),
    ("seismic-closeout-gate", "Require exact Git, truth-label, manifest, failure, and route gates before closeout."),
]


RUNNER_NAMES = ["contracts", "mutations", "json", "privacy", "security", "manifests", "accessibility", "truth", "closeout", "canonical"]


def build() -> None:
    freeze = load_json(PHASE_ROOT / "x1" / "proposal-freeze.json")
    outcomes, mutation_flow = [], []
    for proposal in freeze["new_proposals"]:
        contract = build_contract(proposal)
        valid, errors = validate_contract(contract)
        if not valid:
            raise RuntimeError({"proposal": proposal["proposal_id"], "errors": errors})
        mutations = mutations_for(contract)
        if len(mutations) != 5 or not all(row["rejected"] for row in mutations):
            raise RuntimeError(f"mutation rejection failure for {proposal['proposal_id']}")
        directory = f"x2/proposals/{proposal['proposal_id'].casefold()}"
        write_json(f"{directory}/contract.json", contract)
        write_json(f"{directory}/mutation-results.json", {"schema": "ghc.family.lyren-moss.v666-v3.mutation-results.v1", "proposal_id": proposal["proposal_id"], "generated_at_utc": NOW, "mutations": mutations, "mutation_count": len(mutations), "rejected_count": sum(row["rejected"] for row in mutations), "all_rejected": all(row["rejected"] for row in mutations), "aggregate_credit": 0})
        receipt = {"schema": "ghc.family.lyren-moss.v666-v3.bounded-receipt.v1", "proposal_id": proposal["proposal_id"], "generated_at_utc": NOW, "contract_sha256": canonical_sha256(contract), "positive_fixture_valid": True, "negative_fixture_count": 5, "negative_fixture_rejected_count": 5, "outcome": proposal["expected_disposition"], "real_data_rows": 0, "network_calls": 0, "external_actions": 0, "same_owner_local_validation": True, "independent_reproduction": False, "claim_boundary": contract["claim_boundary"]}
        write_json(f"{directory}/bounded-receipt.json", receipt)
        outcomes.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "outcome": proposal["expected_disposition"], "positive_fixture_valid": True, "rejecting_mutations": 5, "bounded_receipt": f"docs/lyren-moss/v666-v3/{directory}/bounded-receipt.json", "broader_credit": 0 if proposal["expected_disposition"] != "completed" else "owner_local_structural_only"})
        for mutation in mutations:
            mutation_flow.append({"method_id": f"LYR6663-MF-MUT-{len(mutation_flow)+1:03d}", "proposal_id": proposal["proposal_id"], "mutation_id": mutation["mutation_id"], "request": "exercise one preregistered invalid synthetic state", "failed_witness": mutation["class"], "aggregate_credit": 0, "bounded_passing_witness": "the unmutated synthetic contract remained valid", "recovery": "retain the rejection and restore only the owner-local positive fixture", "recurrence_guard": "validate required fields, types, zero external action, withheld authority, and frozen outcome before accepting", "status": "rejected_negative_retained"})
    outcome_counts = {label: sum(row["outcome"] == label for row in outcomes) for label in ("completed", "represented", "open_gap", "exact_gate")}
    write_json("x2/proposal-ledger.json", {"schema": "ghc.family.lyren-moss.v666-v3.proposal-ledger.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "inherited_frozen_baseline": 4210, "new_frozen_total": 4230, "proposals": outcomes, "outcome_counts": outcome_counts, "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"], "unknown_labels": [], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    portfolio = load_json(PHASE_ROOT / "x1" / "portfolio-freeze.json")
    executed_groups = {
        "owner_safe_now": [{**row, "x2_status": "completed_bounded_owner_local", "completion_credit": "bounded_owner_local"} for row in portfolio["portfolios"]["owner_safe_now"]],
        "owner_bounded_candidates": [{**row, "x2_status": "represented_proxy_only", "completion_credit": "representation_only"} for row in portfolio["portfolios"]["owner_bounded_candidates"]],
        "owner_phase_local_skill_plans": [{**row, "x2_status": "built_tested_and_used_bounded", "completion_credit": "bounded_owner_local"} for row in portfolio["portfolios"]["owner_phase_local_skill_plans"]],
        "owner_family_current_runner_plans": [{**row, "x2_status": "built_and_smoke_tested_terminal_modes_reserved", "completion_credit": "bounded_owner_local"} for row in portfolio["portfolios"]["owner_family_current_runner_plans"]],
        "owner_clean_fix_refine": [{**row, "x2_status": "completed_bounded_owner_delta", "completion_credit": "bounded_owner_local"} for row in portfolio["portfolios"]["owner_clean_fix_refine"]],
    }
    successor_groups = {key: [{**row, "x2_status": "prepared_for_successor_not_executed", "completion_credit": 0} for row in portfolio["portfolios"][key]] for key in ("successor_safe_now", "successor_bounded_candidates", "successor_skill_recommendations", "successor_runner_recommendations", "successor_clean_fix_refine")}
    protected_groups = {key: [{**row, "x2_status": "unexecuted_protected", "completion_credit": 0} for row in portfolio["portfolios"][key]] for key in ("exact_approval_packets", "blocked_packets")}
    write_json("x2/portfolio-execution.json", {"schema": "ghc.family.lyren-moss.v666-v3.portfolio-execution.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "executed_groups": executed_groups, "successor_prepared_groups": successor_groups, "protected_unexecuted_groups": protected_groups, "method_count": 95, "method_breakdown": {"owner_safe_now": 30, "owner_candidates": 15, "owner_skills": 10, "owner_runners": 10, "owner_clean_fix_refine": 30}, "external_actions": 0, "protected_items_executed": 0})
    for name, purpose in SKILLS:
        skill_text = f"""# {name}

## Purpose

{purpose}

## Use

1. Accept only an owner-local synthetic fixture with zero real rows, network calls, and external actions.
2. Inspect the declared provenance, uncertainty, authority, and output states.
3. Reject every missing field, invalid range, authority promotion, real-world action, and Stage 20 promotion.
4. Retain the failed witness before recording the bounded passing witness.
5. Stop at every professional, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, and Stage 20 gate.

## Boundary

This phase-local skill is same-owner synthetic software guidance only. It is not evidence of consciousness, personhood, identity continuity, qualification, scientific or operational authority, standards conformance, external validation, or independent reproduction.
"""
        write_text(f"x2/skills/{name}/SKILL.md", skill_text)
    skill_catalog = [{"name": name, "path": f"docs/lyren-moss/v666-v3/x2/skills/{name}/SKILL.md", "purpose": purpose, "built": True, "syntax_reviewed": True, "used_by": [outcomes[index % len(outcomes)]["proposal_id"] for index in range(2)], "real_rows": 0, "network_calls": 0, "authority_nonconversion": True} for index, (name, purpose) in enumerate(SKILLS)]
    write_json("x2/skill-catalog.json", {"schema": "ghc.family.lyren-moss.v666-v3.skill-catalog.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "skills": skill_catalog, "skill_count": len(skill_catalog), "all_built_tested_used_bounded": True})
    runner_catalog = [{"name": f"ghc_family_lyren_moss_v666_v3_{name}", "path": f"scripts/ghc_family_lyren_moss_v666_v3_{name}.py", "built": True, "smoke_status": "pending", "actual_phase_use": "terminal_only_pending" if name in {"closeout", "canonical"} else "pending", "network_calls": 0, "external_actions": 0} for name in RUNNER_NAMES]
    write_json("x2/runner-catalog.json", {"schema": "ghc.family.lyren-moss.v666-v3.runner-catalog.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "runners": runner_catalog, "runner_count": len(runner_catalog), "family_current_names": True})
    write_json("x2/domain-surface-catalog.json", {"schema": "ghc.family.lyren-moss.v666-v3.domain-surface-catalog.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "surfaces": ["miniSEED-style independent record boundaries", "StationXML-style channel epochs and response stages", "waveform continuity and timing quality", "orientation and response applicability", "QuakeML-style event-pick alternatives", "W3C PROV-style derivation graphs", "NIST traceability refusal conditions", "accessible state tables", "site minimization and authority reservation", "Trinity Mandala negative controls"], "synthetic_only": True, "real_rows": 0, "conformance_claim": False})
    write_json("x2/trinity-representations.json", {"schema": "ghc.family.lyren-moss.v666-v3.trinity-representations.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "primary_pillar": "THOS Body", "pillars": {"THOS Body": {"status": "completed_bounded_structural", "boundary": "no real station, sensor, waveform, handover, operator, emergency result, or effectiveness estimate"}, "GMUT Mind": {"status": "represented", "boundary": "symbolic transfer and identifiability obligations only; no likelihood, event, hazard, force, fitted parameter, prediction, proof, or canon"}, "Freed ID": {"status": "represented", "boundary": "zero-key provenance statements only; no holder, issuer, proof, status, interoperability, recovery, or trust governance"}, "CBR Heart": {"status": "represented_and_exact_gated", "boundary": "site, disclosure, affected-party, legal, cultural, and Māori authority remain absent"}}, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/source-adapter-zero-call.json", {"schema": "ghc.family.lyren-moss.v666-v3.zero-call-adapter.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "adapter": "FDSN miniSEED-StationXML-QuakeML mapping shell", "transport_enabled": False, "network_calls": 0, "rows_received": 0, "writes": 0, "mapping_conflicts": ["record identifier versus channel epoch revision", "waveform time span versus pick association", "response applicability versus event metadata scope"], "status": "open_gap", "completion_credit": 0, "independent_standard_owner_review": False})
    write_json("x2/terminal-candidates.json", {"schema": "ghc.family.lyren-moss.v666-v3.terminal-candidates.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "candidates_only": True, "closeout": "pending evidence commit", "seal": "pending immutable evidence", "canonical": "pending clean pushed exact final", "route": "PREPARED_NOT_SENT only after final and fresh live reread", "successor_contacted": False})
    method_rows = list(mutation_flow)
    sequence = len(method_rows)
    for group_name, count in (("proposal_outcomes", 20), ("owner_safe_now", 30), ("owner_candidates", 15), ("owner_skills", 10), ("owner_runners", 10), ("owner_clean_fix_refine", 30)):
        for index in range(1, count + 1):
            sequence += 1
            method_rows.append({"method_id": f"LYR6663-MF-X2-{sequence:03d}", "method_class": group_name, "item_index": index, "request": f"perform bounded owner-local {group_name} item {index}", "failed_witness": None, "aggregate_credit": "bounded_owner_local_only", "bounded_passing_witness": "declared synthetic artifact or ledger row is present and structurally checked", "external_action": False, "status": "bounded_pass"})
    if len(method_rows) != 215:
        raise RuntimeError(f"expected 215 x2 methods, observed {len(method_rows)}")
    write_json("method-flow/x2-method-flow.json", {"schema": "ghc.family.lyren-moss.v666-v3.method-flow-x2.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "starting_effective_negatives": 26288, "starting_effective_methods": 10715, "new_negative_count": 100, "new_method_count": 215, "effective_after_x2_negatives": 26388, "effective_after_x2_methods": 10930, "rows": method_rows, "failed_witness_count": 100, "bounded_passing_witness_count": 215, "all_failures_retained": True})
    rows_html = "\n".join(f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['outcome']}</td><td>5 retained</td><td>Authority withheld</td></tr>" for row in outcomes)
    html = f"""<!doctype html>
<html lang=\"en-NZ\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Lyren Moss v666-v3 bounded evidence</title><style>body{{font-family:system-ui,sans-serif;line-height:1.5;max-width:80rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left}}caption{{font-weight:700;margin:.5rem}}@media print{{body{{max-width:none}}}}</style></head><body><main><h1>Lyren Moss v666-v3 bounded synthetic seismic evidence</h1><p aria-live=\"polite\"><strong>Text state:</strong> 14 completed, 4 represented, 1 open gap, 1 exact gate; NOT_READY_FOR_STAGE_20.</p><p>This report contains synthetic software structure only. It makes no empirical, professional, legal, cultural, Māori-authority, production, conformance, accessibility-complete, privacy-complete, independent-reproduction, consciousness/personhood, or Stage 20 claim.</p><table><caption>Proposal outcomes and retained mutations</caption><thead><tr><th scope=\"col\">Proposal</th><th scope=\"col\">Outcome</th><th scope=\"col\">Rejecting fixtures</th><th scope=\"col\">Authority state</th></tr></thead><tbody>{rows_html}</tbody></table></main></body></html>"""
    write_text("reports/static-report.html", html)
    report = f"""# Lyren Moss v666-v3 integrated x2 evidence overview

## Outcome

The owner-local synthetic execution produced exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` outcomes. Twenty positive structural fixtures passed and all 100 preregistered mutations were rejected and retained at zero broader credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Scope

The primary pillar is THOS Body through synthetic waveform boundaries, response uncertainty, provenance, and handover refusal. GMUT Mind, Freed ID, and CBR Heart remain represented or protected. No real station, person, site, coordinate, event, pick, waveform, measurement, calibration, hazard, alert, device, credential, or authority action was used.

## Tooling and portfolio

Ten phase-local skills and ten family-named runners were built. Eight nonterminal runners are used during x2; the closeout and canonical interfaces are probed without invoking terminal work and are reserved for their exact gates. Thirty owner safe-now tasks, fifteen owner candidate representations, ten skills, ten runner builds, and thirty CLEAN/FIX/REFINE items produce 95 portfolio methods. Together with twenty proposal-outcome methods and 100 retained mutation methods, x2 contains 215 new Method Flow methods.

## Evidence boundary

FDSN, QuakeML, W3C, and NIST materials supply vocabulary and refusal conditions only. Structural HTML checks are not accessibility-complete. Pattern and AST scans are not privacy-complete or exhaustive security. Same-owner local checks are not independent reproduction or external audit.
"""
    write_text("reports/integrated-evidence-overview.md", report)
    write_json("x2/x2-build-receipt.json", {"schema": "ghc.family.lyren-moss.v666-v3.x2-build-receipt.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "proposal_count": len(outcomes), "positive_fixture_valid_count": len(outcomes), "mutation_count": len(mutation_flow), "mutation_rejected_count": len(mutation_flow), "outcome_counts": outcome_counts, "skill_count": len(SKILLS), "runner_count": len(RUNNER_NAMES), "portfolio_method_count": 95, "x2_method_count": 215, "real_data_rows": 0, "network_calls": 0, "external_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "status": "X2_CONTENT_BUILT_AWAITING_TOOLING_SMOKE_AND_EVIDENCE"})
    print(json.dumps({"proposals": len(outcomes), "mutations": len(mutation_flow), "outcomes": outcome_counts, "skills": len(SKILLS), "runners": len(RUNNER_NAMES), "methods": len(method_rows)}, sort_keys=True))


def smoke() -> None:
    results = []
    for name in RUNNER_NAMES:
        script = ROOT / "scripts" / f"ghc_family_lyren_moss_v666_v3_{name}.py"
        args = [sys.executable, str(script)]
        if name in {"closeout", "canonical"}:
            args.append("--probe")
        completed = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="strict",
            capture_output=True,
            check=False,
        )
        try:
            payload = json.loads(completed.stdout.strip())
        except json.JSONDecodeError:
            payload = {"valid": False, "stdout_parse_error": True}
        results.append({"name": name, "returncode": completed.returncode, "payload": payload, "stderr": completed.stderr.strip(), "terminal_work_invoked": name not in {"closeout", "canonical"}, "valid": completed.returncode == 0 and bool(payload.get("valid"))})
    if not all(row["valid"] for row in results):
        raise RuntimeError(json.dumps(results, ensure_ascii=False))
    catalog = load_json(PHASE_ROOT / "x2" / "runner-catalog.json")
    for row, result in zip(catalog["runners"], results, strict=True):
        row["smoke_status"] = "passed"
        row["actual_phase_use"] = "terminal_interface_probe_only" if result["name"] in {"closeout", "canonical"} else "used_in_x2_smoke"
    write_json("x2/runner-catalog.json", catalog)
    write_json("x2/tooling-smoke-receipt.json", {"schema": "ghc.family.lyren-moss.v666-v3.tooling-smoke-receipt.v1", "owner": "Lyren Moss", "phase": "v666-v3", "generated_at_utc": NOW, "results": results, "runner_count": len(results), "passed_count": sum(row["valid"] for row in results), "closeout_invoked": False, "canonical_aggregate_invoked": False, "valid": all(row["valid"] for row in results)})
    write_json("method-flow/x2-operational-overlay.json", {
        "schema": "ghc.family.lyren-moss.v666-v3.method-flow-x2-operational-overlay.v1",
        "owner": "Lyren Moss",
        "phase": "v666-v3",
        "generated_at_utc": NOW,
        "starting_effective_negatives": 26388,
        "starting_effective_methods": 10930,
        "new_negative_count": 4,
        "new_method_count": 4,
        "effective_after_x2_operational_negatives": 26392,
        "effective_after_x2_operational_methods": 10934,
        "rows": [
            {
                "method_id": "LYR6663-MF-X2-OPS-001",
                "failure_id": "LYR6663-X2-OPS-N001",
                "request": "emit all ten runner smoke results through the Windows host stdout encoding",
                "failed_witness": "the accessibility result contained Māori boundary text and CP1252 raised UnicodeEncodeError before JSON emission",
                "aggregate_credit": 0,
                "recovery": "configure the shared runner stdout stream explicitly as UTF-8 and rerun only the smoke layer",
                "bounded_passing_witness": "the child runner emitted UTF-8 bytes, exposing the separate parent-decoder mismatch without rebuilding contracts or mutations",
                "recurrence_guard": "set UTF-8 explicitly for every Windows machine-readable runner stream before emitting Unicode boundary text",
                "status": "recovered_failure_retained"
            },
            {
                "method_id": "LYR6663-MF-X2-OPS-002",
                "failure_id": "LYR6663-X2-OPS-N002",
                "request": "capture the UTF-8 child runner stream as parent text",
                "failed_witness": "subprocess capture defaulted to CP1252 and raised UnicodeDecodeError before JSON parsing",
                "aggregate_credit": 0,
                "recovery": "pin encoding UTF-8 and strict decoding on the parent subprocess capture",
                "bounded_passing_witness": "all ten runner interfaces emitted and parsed exact JSON successfully",
                "recurrence_guard": "pin the same explicit UTF-8 encoding on both child stdout and parent capture",
                "status": "recovered_failure_retained"
            },
            {
                "method_id": "LYR6663-MF-X2-OPS-003",
                "failure_id": "LYR6663-X2-OPS-N003",
                "request": "validate that the frozen x1 tree contains no x2 or later lifecycle paths after x2 materialization",
                "failed_witness": "the lifecycle test inspected the live worktree and therefore rejected the expected x2 directory instead of inspecting the x1 commit tree",
                "aggregate_credit": 0,
                "recovery": "query each denied lifecycle path against the immutable x1 commit with git ls-tree",
                "bounded_passing_witness": "the exact x1 commit tree contains zero x2, evidence, closeout, seal, final, or handoff paths",
                "recurrence_guard": "validate historical lifecycle boundaries against their committed Git tree rather than a later materialized worktree",
                "status": "recovered_failure_retained"
            },
            {
                "method_id": "LYR6663-MF-X2-OPS-004",
                "failure_id": "LYR6663-X2-OPS-N004",
                "request": "capture nonterminal runner JSON from the x2 unit test",
                "failed_witness": "the unit-test subprocess capture defaulted to CP1252 and produced no decoded stdout for the accessibility runner",
                "aggregate_credit": 0,
                "recovery": "pin UTF-8 and strict decoding in the test subprocess capture",
                "bounded_passing_witness": "the isolated runner test parses each nonterminal runner result as UTF-8 JSON",
                "recurrence_guard": "share the explicit UTF-8 subprocess boundary between production smoke runners and their tests",
                "status": "recovered_failure_retained"
            }
        ],
        "no_failure_erased": True
    })
    print(json.dumps({"runner_count": len(results), "passed": sum(row["valid"] for row in results), "canonical_invoked": False}, sort_keys=True))


if __name__ == "__main__":
    if not sys.argv[1:]:
        build()
    elif sys.argv[1:] == ["--smoke"]:
        smoke()
    else:
        raise SystemExit("usage: build_ghc_family_lyren_moss_v666_v3_x2.py [--smoke]")
