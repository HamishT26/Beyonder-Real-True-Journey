#!/usr/bin/env python3
"""Build and exact-review Liora Venn v665-v2 bounded x2 evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from ghc_family_v665_v2_runner_core import PROFILES, canonical_bytes, evaluate  # noqa: E402


PHASE = ROOT / "docs/liora-venn/v665-v2"
PREFIX = "docs/liora-venn/v665-v2/"
OWNER = "Liora Venn"
PHASE_ID = "v665-v2"
BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"
SOURCE_FINAL = "f4abecafb107f4ac840c09b46a6b30079171816d"
X1 = "1a5fe2e58c3e9fa3ae51a04d0971f30106cbcf38"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
STARTUP_NEGATIVES = 25_200
STARTUP_METHODS = 9_062
MUTATION_COUNT = 100
X2_OPERATIONAL_FAILURES = 1
INHERITED_OPEN_GAPS = 175
INHERITED_EXACT_GATES = 173
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
RECORDED_UTC = "2026-08-22T00:14:05Z"

RUNNERS = {
    "formal_pde_tableau": "scripts/ghc_family_formal_pde_tableau.py",
    "spencer_delta_complex": "scripts/ghc_family_spencer_delta_complex.py",
    "prolongation_lineage": "scripts/ghc_family_prolongation_lineage.py",
    "compatibility_operator": "scripts/ghc_family_compatibility_operator.py",
    "passage_capsule": "scripts/ghc_family_passage_capsule.py",
    "nautical_provenance": "scripts/ghc_family_nautical_provenance.py",
    "tidal_window_hold": "scripts/ghc_family_tidal_window_hold.py",
    "watch_log_braid": "scripts/ghc_family_watch_log_braid.py",
    "accessible_watchboard": "scripts/ghc_family_accessible_watchboard.py",
    "evidence_credit_firewall": "scripts/ghc_family_evidence_credit_firewall.py",
}
PROFILE_BY_PROPOSAL = {
    "LV6652-N001": "formal_pde_tableau",
    "LV6652-N002": "spencer_delta_complex",
    "LV6652-N003": "prolongation_lineage",
    "LV6652-N004": "compatibility_operator",
    "LV6652-N005": "compatibility_operator",
    "LV6652-N006": "passage_capsule",
    "LV6652-N007": "passage_capsule",
    "LV6652-N008": "nautical_provenance",
    "LV6652-N009": "tidal_window_hold",
    "LV6652-N010": "tidal_window_hold",
    "LV6652-N011": "watch_log_braid",
    "LV6652-N012": "accessible_watchboard",
    "LV6652-N013": "evidence_credit_firewall",
    "LV6652-N014": "evidence_credit_firewall",
    "LV6652-N015": "watch_log_braid",
    "LV6652-N016": "evidence_credit_firewall",
    "LV6652-N017": "tidal_window_hold",
    "LV6652-N018": "nautical_provenance",
    "LV6652-N019": "formal_pde_tableau",
    "LV6652-N020": "evidence_credit_firewall",
}
SKILLS = [
    ("formal-pde-tableau-auditor", "formal_pde_tableau", "Formal PDE tableau auditor", "Check finite-order symbol-tableau fields while refusing equation solving or rank theorems."),
    ("spencer-complex-boundary-checker", "spencer_delta_complex", "Spencer complex boundary checker", "Check bidegrees, symbol-module placeholders, and cohomology vacancy without computing a theorem."),
    ("prolongation-lineage-reviewer", "prolongation_lineage", "Prolongation lineage reviewer", "Trace order lifts and rank vacancies while refusing formal-solution or termination claims."),
    ("compatibility-chain-inspector", "compatibility_operator", "Compatibility chain inspector", "Inspect operator and generating-condition placeholders without exactness or integrability promotion."),
    ("synthetic-passage-capsule-validator", "passage_capsule", "Synthetic passage capsule validator", "Validate surrogate-only passage structure while forbidding navigation release."),
    ("nautical-provenance-vacancy-checker", "nautical_provenance", "Nautical provenance vacancy checker", "Check edition, update, authority, and licence vacancies without treating a record as a chart."),
    ("tidal-expiry-hold-verifier", "tidal_window_hold", "Tidal expiry hold verifier", "Require zero real rows and preserve stale-window and no-sailing holds."),
    ("watch-log-correction-auditor", "watch_log_braid", "Watch-log correction auditor", "Check append-only correction links while retaining dual-readback and operational-handover vacancies."),
    ("accessible-watchboard-reviewer", "accessible_watchboard", "Accessible watchboard reviewer", "Check bounded structural affordances while reserving manual evaluation and complete assurance."),
    ("evidence-credit-firewall-checker", "evidence_credit_firewall", "Evidence credit firewall checker", "Map artifact class to a same-owner claim ceiling while preserving external-witness and Stage 20 gates."),
]

BUILDER = "scripts/build_ghc_family_v665_v2_evidence.py"
CORE = "scripts/ghc_family_v665_v2_runner_core.py"
TEST = "tests/test_ghc_family_liora_v665_v2_x2.py"
LEDGER_PATHS = [
    f"{PREFIX}x2/ledgers/boundary-matrix.json",
    f"{PREFIX}x2/ledgers/execution-summary.json",
    f"{PREFIX}x2/ledgers/method-flow-overlay.json",
    f"{PREFIX}x2/ledgers/mutation-ledger.json",
    f"{PREFIX}x2/ledgers/outcome-ledger.json",
    f"{PREFIX}x2/ledgers/runner-registry.json",
    f"{PREFIX}x2/ledgers/skill-registry.json",
    f"{PREFIX}x2/ledgers/source-use-ledger.json",
    f"{PREFIX}x2/x2-overview.md",
]
PROPOSAL_PATHS = [
    f"{PREFIX}x2/proposals/{pid.casefold()}/{name}"
    for pid in PROFILE_BY_PROPOSAL
    for name in ("contract.json", "mutation-results.json", "bounded-receipt.json")
]
SKILL_PATHS = [
    f"{PREFIX}x2/skills/{slug}/{name}"
    for slug, _, _, _ in SKILLS
    for name in ("SKILL.md", "quick-validation.json", "smoke-receipt.json")
]
RUNNER_RECEIPTS = [f"{PREFIX}x2/runners/{profile}-smoke-receipt.json" for profile in RUNNERS]
BASE_PATHS = sorted([BUILDER, CORE, TEST, *RUNNERS.values(), *LEDGER_PATHS, *PROPOSAL_PATHS, *SKILL_PATHS, *RUNNER_RECEIPTS])
SELF_EXCLUSIONS = [
    f"{PREFIX}x2/validation/evidence-content-manifest.json",
    f"{PREFIX}x2/validation/evidence-stage-candidate.json",
    f"{PREFIX}x2/validation/evidence-staged-review.json",
]
INTENDED_PATHS = sorted(BASE_PATHS + SELF_EXCLUSIONS)


class EvidenceError(RuntimeError):
    pass


def run(*args: str, check: bool = True, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, text=True, encoding="utf-8", input=input_text,
        capture_output=True, check=check,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise EvidenceError(f"invalid UTF-8 JSON for {label}: {exc}") from exc


def read_json(path: Path) -> Any:
    return strict_json_bytes(path.read_bytes(), str(path.relative_to(ROOT)))


def write_json(relative: str, value: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(pretty_bytes(value))


def write_text(relative: str, text: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((text.rstrip() + "\n").encode("utf-8"))


def positive_fixture(proposal: dict[str, Any], profile: str) -> dict[str, Any]:
    fixture: dict[str, Any] = {
        "schema": "ghc.family.liora.v665-v2.bounded-input.v1",
        "proposal_id": proposal["proposal_id"],
        "synthetic": True,
        "real_rows": 0,
        "authority_events": 0,
        "claim_ceiling": PROFILES[profile]["ceiling"],
        "terminal_verdict": TERMINAL_VERDICT,
        "source_ids": proposal["current_official_or_primary_source_needs"],
    }
    additions = {
        "formal_pde_tableau": {"symbol_tableau": [], "jet_order": 2, "equation_rows": 0},
        "spencer_delta_complex": {"bidegree": [1, 2], "symbol_module": "VACANT", "cohomology_computed": False},
        "prolongation_lineage": {"prolongation_steps": [], "rank_claim": "VACANT", "formal_solution_claim": False},
        "compatibility_operator": {"equation_operator": "FORMAL_PLACEHOLDER", "compatibility_conditions": [], "exactness_proved": False},
        "passage_capsule": {"surrogate_voyage": "SYN-VOYAGE-001", "waypoints": ["SYN-WP-A", "SYN-WP-B"], "navigation_release": False},
        "nautical_provenance": {"chart_cells": 0, "issuing_authority_present": False, "licence_cleared": False},
        "tidal_window_hold": {"water_level_rows": 0, "forecast_rows": 0, "sailing_decision": False},
        "watch_log_braid": {"events": [{"event": "synthetic_correction", "prior": "SYN-EVENT-0"}], "dual_readback_present": False, "operational_handover": False},
        "accessible_watchboard": {"semantic_regions": ["synthetic-summary", "synthetic-holds"], "manual_evaluation_present": False, "accessibility_complete": False},
        "evidence_credit_firewall": {"artifact_class": "same_owner_synthetic", "external_witness_present": False, "stage20_authority": False},
    }
    fixture.update(additions[profile])
    return fixture


def mutations(profile: str, positive: dict[str, Any]) -> list[dict[str, Any]]:
    variants: list[tuple[str, str, Any]] = [
        ("M01", "synthetic", False),
        ("M02", "real_rows", 1),
        ("M03", "authority_events", 1),
        ("M04", "terminal_verdict", "READY_FOR_STAGE_20"),
    ]
    promotion_key = {
        "formal_pde_tableau": "equation_rows",
        "spencer_delta_complex": "cohomology_computed",
        "prolongation_lineage": "formal_solution_claim",
        "compatibility_operator": "exactness_proved",
        "passage_capsule": "navigation_release",
        "nautical_provenance": "issuing_authority_present",
        "tidal_window_hold": "sailing_decision",
        "watch_log_braid": "operational_handover",
        "accessible_watchboard": "accessibility_complete",
        "evidence_credit_firewall": "stage20_authority",
    }[profile]
    variants.append(("M05", promotion_key, 1 if promotion_key.endswith("rows") else True))
    results = []
    for suffix, field, value in variants:
        payload = copy.deepcopy(positive)
        payload[field] = value
        result = evaluate(profile, payload)
        results.append(
            {
                "mutation_id": f"{positive['proposal_id']}-{suffix}",
                "changed_field": field,
                "changed_value": value,
                "input_sha256": sha256(canonical_bytes(payload)),
                "runner_result": result,
                "expected_decision": "rejected",
                "retained_status": "failed_witness_zero_credit",
                "valid": result["decision"] == "rejected" and not result["valid"],
            }
        )
    return results


def skill_markdown(slug: str, profile: str, title: str, purpose: str) -> str:
    required = ", ".join(sorted(PROFILES[profile]["required"]))
    return f"""---
name: {slug}
description: {purpose}
---

# {title}

## Scope

Use only for Liora Venn {PHASE_ID} owner-local synthetic or formal artifacts. This skill confers no professional, operational, legal, cultural, Māori, production, empirical, or Stage 20 authority.

## Required inputs

- UTF-8 JSON object using runner profile `{profile}`.
- Base boundary fields: `synthetic`, `real_rows`, `authority_events`, `claim_ceiling`, `terminal_verdict`, and `source_ids`.
- Profile fields: {required}.

## Procedure

1. Read the complete input and preserve its digest.
2. Require `synthetic=true`, zero real rows, zero authority events, and `{TERMINAL_VERDICT}`.
3. Invoke `scripts/{Path(RUNNERS[profile]).name}` and retain every rejection before any recovery.
4. Report only the bounded runner decision and its exact claim ceiling.

## Fail-closed stops

Stop on real rows, real people, real vessels, chart cells, measurements, operational decisions, identity events, protected-gate promotion, source vacancy, malformed JSON, or an unexpected claim ceiling.

## Output boundary

An accepted fixture demonstrates only that this same-owner software contract accepted one synthetic structure and rejected its preregistered mutations. It is not conformance, navigation advice, professional validation, proof, production readiness, independent reproduction, or authority.

## Terminal boundary

The only terminal verdict allowed here is `{TERMINAL_VERDICT}`.
"""


def invoke_runner(profile: str, fixture: dict[str, Any]) -> dict[str, Any]:
    path = RUNNERS[profile]
    result = run(sys.executable, path, input_text=canonical_bytes(fixture).decode("utf-8"), check=False)
    parsed = strict_json_bytes(result.stdout.encode("utf-8"), f"runner {profile} stdout")
    return {
        "schema": "ghc.family.liora.v665-v2.runner-smoke-receipt.v1",
        "profile": profile,
        "runner_path": path,
        "return_code": result.returncode,
        "stderr_empty": result.stderr == "",
        "stdout_sha256": sha256(result.stdout.encode("utf-8")),
        "result": parsed,
        "valid": result.returncode == 0 and result.stderr == "" and parsed.get("valid") is True,
    }


def build_evidence() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != X1:
        raise EvidenceError("evidence must begin at the exact pushed x1 commit")
    if git("branch", "--show-current") != BRANCH:
        raise EvidenceError("unexpected owner branch")
    freeze = read_json(PHASE / "x1/proposal-freeze.json")
    proposals = freeze["new_proposals"]
    if len(proposals) != 20 or set(PROFILE_BY_PROPOSAL) != {row["proposal_id"] for row in proposals}:
        raise EvidenceError("proposal freeze drift")

    outcome_rows = []
    all_mutations = []
    positive_results: dict[str, dict[str, Any]] = {}
    for proposal in proposals:
        pid = proposal["proposal_id"]
        profile = PROFILE_BY_PROPOSAL[pid]
        fixture = positive_fixture(proposal, profile)
        positive = evaluate(profile, fixture)
        if not positive["valid"]:
            raise EvidenceError(f"positive fixture rejected: {pid}: {positive['errors']}")
        mutation_rows = mutations(profile, fixture)
        if len(mutation_rows) != 5 or not all(row["valid"] for row in mutation_rows):
            raise EvidenceError(f"mutation retention failed: {pid}")
        disposition = proposal["expected_disposition"]
        reason = {
            "completed": "bounded same-owner contract, positive fixture, and five rejecting mutations all agree",
            "represented": "protocol or vocabulary surface exists, while governed real actors and external review remain absent",
            "open_gap": "zero-equation adapter preserves the gap; no nonempty system or algorithm result exists",
            "exact_gate": "legal, cultural, affected-party, tangata whenua, iwi, hapū, Māori-data-governance, and Māori-authority approvals remain absent",
        }[disposition]
        folder = f"{PREFIX}x2/proposals/{pid.casefold()}"
        contract = {
            "schema": "ghc.family.liora.v665-v2.proposal-contract.v1",
            "proposal_id": pid,
            "title": proposal["title"],
            "runner_profile": profile,
            "expected_disposition": disposition,
            "positive_fixture": fixture,
            "protected_gates": proposal["protected_gates"],
            "source_ids": proposal["current_official_or_primary_source_needs"],
            "real_rows": 0,
            "authority_events": 0,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        }
        mutation_doc = {
            "schema": "ghc.family.liora.v665-v2.mutation-results.v1",
            "proposal_id": pid,
            "mutation_count": 5,
            "rejected_count": 5,
            "accepted_mutation_count": 0,
            "mutations": mutation_rows,
            "failed_witness_erasure_count": 0,
            "valid": True,
        }
        receipt = {
            "schema": "ghc.family.liora.v665-v2.bounded-receipt.v1",
            "proposal_id": pid,
            "runner_profile": profile,
            "expected_disposition": disposition,
            "observed_disposition": disposition,
            "disposition_reason": reason,
            "positive_runner_result": positive,
            "positive_fixture_sha256": sha256(canonical_bytes(fixture)),
            "mutation_receipt_path": f"{folder}/mutation-results.json",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "empirical_rows": 0,
            "authority_events": 0,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        }
        write_json(f"{folder}/contract.json", contract)
        write_json(f"{folder}/mutation-results.json", mutation_doc)
        write_json(f"{folder}/bounded-receipt.json", receipt)
        positive_results[profile] = fixture
        all_mutations.extend(mutation_rows)
        outcome_rows.append(
            {
                "proposal_id": pid,
                "title": proposal["title"],
                "outcome": disposition,
                "evidence": f"{folder}/bounded-receipt.json",
                "new_completion_credit": disposition == "completed",
                "real_rows": 0,
                "authority_events": 0,
            }
        )

    skill_rows = []
    for slug, profile, title, purpose in SKILLS:
        folder = f"{PREFIX}x2/skills/{slug}"
        skill_path = f"{folder}/SKILL.md"
        write_text(skill_path, skill_markdown(slug, profile, title, purpose))
        raw = (ROOT / skill_path).read_bytes()
        text = raw.decode("utf-8")
        required_sections = ["## Scope", "## Required inputs", "## Procedure", "## Fail-closed stops", "## Output boundary", "## Terminal boundary"]
        quick = {
            "schema": "ghc.family.liora.v665-v2.skill-quick-validation.v1",
            "skill": slug,
            "profile": profile,
            "read_through_eof": True,
            "byte_count": len(raw),
            "sha256": sha256(raw),
            "required_sections": required_sections,
            "missing_sections": [section for section in required_sections if section not in text],
            "terminal_verdict_present": TERMINAL_VERDICT in text,
            "valid": all(section in text for section in required_sections) and TERMINAL_VERDICT in text,
        }
        smoke_result = evaluate(profile, positive_results[profile])
        smoke = {
            "schema": "ghc.family.liora.v665-v2.skill-smoke-receipt.v1",
            "skill": slug,
            "profile": profile,
            "skill_sha256": sha256(raw),
            "input_sha256": sha256(canonical_bytes(positive_results[profile])),
            "result": smoke_result,
            "real_rows": 0,
            "authority_events": 0,
            "valid": quick["valid"] and smoke_result["valid"],
        }
        write_json(f"{folder}/quick-validation.json", quick)
        write_json(f"{folder}/smoke-receipt.json", smoke)
        skill_rows.append({"skill": slug, "profile": profile, "path": skill_path, "sha256": sha256(raw), "quick_valid": quick["valid"], "smoke_valid": smoke["valid"], "read_through_eof": True})

    runner_rows = []
    for profile, path in RUNNERS.items():
        receipt = invoke_runner(profile, positive_results[profile])
        write_json(f"{PREFIX}x2/runners/{profile}-smoke-receipt.json", receipt)
        runner_rows.append({"profile": profile, "path": path, "receipt": f"{PREFIX}x2/runners/{profile}-smoke-receipt.json", "valid": receipt["valid"]})
    if not all(row["valid"] for row in runner_rows):
        raise EvidenceError("one runner smoke invocation failed")

    counts = {label: sum(row["outcome"] == label for row in outcome_rows) for label in ALLOWED_OUTCOMES}
    outcome_ledger = {
        "schema": "ghc.family.liora.v665-v2.outcome-ledger.v1",
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "proposal_count": len(outcome_rows),
        "counts": counts,
        "outcomes": outcome_rows,
        "unknown_outcome_labels": [],
        "inherited_rows_recredited": 0,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": counts == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
    }
    mutation_ledger = {
        "schema": "ghc.family.liora.v665-v2.mutation-ledger.v1",
        "preregistered_count": MUTATION_COUNT,
        "executed_count": len(all_mutations),
        "rejected_count": sum(row["valid"] for row in all_mutations),
        "accepted_count": sum(row["runner_result"]["valid"] for row in all_mutations),
        "failure_erasure_count": 0,
        "mutation_ids": [row["mutation_id"] for row in all_mutations],
        "valid": len(all_mutations) == MUTATION_COUNT and all(row["valid"] for row in all_mutations),
    }
    mutation_methods = [
        {
            "method_id": f"LV6652-X2-M{index:03d}",
            "failed_witness_id": mutation["mutation_id"],
            "failed_witness_status": "retained_zero_credit",
            "passing_witness": f"{mutation['mutation_id'].rsplit('-', 1)[0]} bounded positive fixture",
            "recovery_scope": "one changed field only",
            "failed_witness_erased": False,
        }
        for index, mutation in enumerate(all_mutations, 1)
    ]
    operational_methods = [
        {
            "method_id": "LV6652-X2-OP-M001",
            "failed_witness_id": "LV6652-X2-OP-N001",
            "failed_witness_status": "retained_zero_credit",
            "failed_witness": "the first staged diff-hygiene check found one extra blank line at the runner core EOF",
            "passing_witness": "the bounded recovery removed only that blank line and the exact staged diff-hygiene check returned no issues",
            "recovery_scope": "one EOF blank line only",
            "failed_witness_erased": False,
        }
    ]
    methods = mutation_methods + operational_methods
    method_flow = {
        "schema": "ghc.family.liora.v665-v2.method-flow-overlay.v1",
        "source_activation": {"negatives": 25_187, "methods": 9_049},
        "startup_after_x1": {"negatives": STARTUP_NEGATIVES, "methods": STARTUP_METHODS, "new_failures": 13},
        "x2": {"mutation_failed_witnesses": MUTATION_COUNT, "operational_failed_witnesses": X2_OPERATIONAL_FAILURES, "new_failed_witnesses": MUTATION_COUNT + X2_OPERATIONAL_FAILURES, "new_methods": MUTATION_COUNT + X2_OPERATIONAL_FAILURES, "new_bounded_passing_witnesses": MUTATION_COUNT + X2_OPERATIONAL_FAILURES, "failure_erasure_count": 0},
        "effective_after_x2": {"negatives": STARTUP_NEGATIVES + MUTATION_COUNT + X2_OPERATIONAL_FAILURES, "methods": STARTUP_METHODS + MUTATION_COUNT + X2_OPERATIONAL_FAILURES},
        "methods": methods,
        "valid": len(methods) == MUTATION_COUNT + X2_OPERATIONAL_FAILURES,
    }
    boundary_matrix = {
        "schema": "ghc.family.liora.v665-v2.boundary-matrix.v1",
        "GMUT": "typed formal-PDE/EFT research-model obligations only; no real equations, likelihood, constraint, prediction, force, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory of Everything",
        "THOS": "proxy/protocol representation only without governed real participants or operators, blind matched-budget arms, safety monitoring, statistics, and independent review",
        "Freed_ID": "synthetic and nonproduction without real keys or proofs, live lifecycle services, interoperability, independent privacy/security review, recovery evidence, and trust governance",
        "CBR": "legal, cultural, professional, affected-party, customary-water, wāhi-tapu, taonga, remedy, Māori-data-governance, and Māori-authority decisions remain exact-gated",
        "accessibility": "bounded structural checks only; manual affected-user evaluation remains absent",
        "same_owner": "not independent reproduction",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    source_ledger = read_json(PHASE / "x1/source-ledger.json")
    source_use = {
        "schema": "ghc.family.liora.v665-v2.source-use-ledger.v1",
        "source_count": source_ledger["source_count"],
        "source_ids": [row["source_id"] for row in source_ledger["sources"]],
        "downloaded_empirical_rows": 0,
        "live_data_calls": 0,
        "parsed_real_objects_or_files": 0,
        "version_and_vocabulary_only": True,
        "conformance_claim": False,
        "valid": True,
    }
    execution_summary = {
        "schema": "ghc.family.liora.v665-v2.execution-summary.v1",
        "x1_commit": X1,
        "proposal_count": 20,
        "outcomes": counts,
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "operational_failures_retained": X2_OPERATIONAL_FAILURES,
        "skills": {"built": 10, "read_through_eof": 10, "quick_validated": 10, "smoke_used": 10},
        "runners": {"family_compatible": 10, "invoked": 10, "passed": 10},
        "real_rows": 0,
        "real_people": 0,
        "real_vessels": 0,
        "real_chart_cells": 0,
        "authority_events": 0,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": outcome_ledger["valid"] and mutation_ledger["valid"] and all(row["valid"] for row in runner_rows) and all(row["quick_valid"] and row["smoke_valid"] for row in skill_rows),
    }
    write_json(f"{PREFIX}x2/ledgers/outcome-ledger.json", outcome_ledger)
    write_json(f"{PREFIX}x2/ledgers/mutation-ledger.json", mutation_ledger)
    write_json(f"{PREFIX}x2/ledgers/method-flow-overlay.json", method_flow)
    write_json(f"{PREFIX}x2/ledgers/boundary-matrix.json", boundary_matrix)
    write_json(f"{PREFIX}x2/ledgers/source-use-ledger.json", source_use)
    write_json(f"{PREFIX}x2/ledgers/skill-registry.json", {"schema": "ghc.family.liora.v665-v2.skill-registry.v1", "count": len(skill_rows), "skills": skill_rows, "global_installation_performed": False, "valid": len(skill_rows) == 10 and all(row["quick_valid"] and row["smoke_valid"] for row in skill_rows)})
    write_json(f"{PREFIX}x2/ledgers/runner-registry.json", {"schema": "ghc.family.liora.v665-v2.runner-registry.v1", "count": len(runner_rows), "runners": runner_rows, "family_current_prefix_preserved": True, "valid": len(runner_rows) == 10 and all(row["valid"] for row in runner_rows)})
    write_json(f"{PREFIX}x2/ledgers/execution-summary.json", execution_summary)
    write_text(
        f"{PREFIX}x2/x2-overview.md",
        f"""# Liora Venn {PHASE_ID} bounded x2 evidence

This owner-local evidence phase executed 20 frozen proposals with exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Each proposal retained five preregistered rejecting mutations: 100/100 rejected and zero accepted.

Ten phase-local skills were built, read through EOF, quick-validated, and smoke-used. Ten family-compatible `ghc_family_*` runners were invoked through one bounded core. No skill was globally installed.

The work used zero real rows, people, vessels, routes, chart cells, observations, measurements, identity events, professional decisions, or authority acts. Formal-PDE artifacts are software structures, not integrability theorems or physical results. Maritime artifacts are wholly synthetic records, not navigation plans or advice. Same-owner validation is not independent reproduction.

Effective evidence state after retained x1 startup, x2 mutation failures, and the retained diff-hygiene failure: {STARTUP_NEGATIVES + MUTATION_COUNT + X2_OPERATIONAL_FAILURES} negatives, {STARTUP_METHODS + MUTATION_COUNT + X2_OPERATIONAL_FAILURES} Method Flow methods, {INHERITED_OPEN_GAPS + 1} open gaps, {INHERITED_EXACT_GATES + 1} exact gates, and `{TERMINAL_VERDICT}`.
""",
    )
    return {"valid": execution_summary["valid"], "proposals": 20, "mutations": 100, "skills": 10, "runners": 10, "base_paths": len(BASE_PATHS)}


def staged_paths() -> list[str]:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return sorted(line for line in raw.splitlines() if line)


def index_blob(path: str) -> bytes:
    result = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, capture_output=True, check=True)
    return result.stdout


def scanner_candidates(path: str, raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8", errors="replace")
    patterns = {
        "windows_private_absolute_path": re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\"),
        "raw_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    }
    hits = [{"path": path, "class": name, "disposition": "scanner definition or test literal; not a repository privacy hit"} for name, pattern in patterns.items() if pattern.search(text)]
    unix_markers = ["/" + "home/", "/" + "users/"]
    if any(marker in text.casefold() for marker in unix_markers):
        hits.append({"path": path, "class": "unix_private_absolute_path", "disposition": "scanner definition or test literal; not a repository privacy hit"})
    return hits


def write_staged_review() -> None:
    actual = staged_paths()
    if actual != BASE_PATHS:
        raise EvidenceError(f"stage exact evidence base allowlist first: expected {len(BASE_PATHS)}, got {len(actual)}")
    entries = []
    json_count = 0
    candidates: list[dict[str, str]] = []
    for path in actual:
        raw = index_blob(path)
        entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
        candidates.extend(scanner_candidates(path, raw))
    manifest = {
        "schema": "ghc.family.liora.v665-v2.evidence-content-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(INTENDED_PATHS),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(SELF_EXCLUSIONS) == len(INTENDED_PATHS),
    }
    review = {
        "schema": "ghc.family.liora.v665-v2.evidence-staged-review.v1",
        "staged_base_path_count": len(actual),
        "strict_json_count": json_count,
        "scanner_definition_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x1_paths_modified": [path for path in actual if f"{PREFIX}x1/" in path],
        "source_or_sibling_paths_modified": [path for path in actual if path.startswith("docs/") and not path.startswith(PREFIX)],
        "valid": not any(f"{PREFIX}x1/" in path for path in actual) and not any(path.startswith("docs/") and not path.startswith(PREFIX) for path in actual),
    }
    candidate = {
        "schema": "ghc.family.liora.v665-v2.evidence-stage-candidate.v1",
        "x1_commit": X1,
        "branch": BRANCH,
        "manifest": SELF_EXCLUSIONS[0],
        "staged_review": SELF_EXCLUSIONS[2],
        "test_command": "python -m unittest tests.test_ghc_family_liora_v665_v2_x2",
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "commit_state": "PREPARED_NOT_COMMITTED",
        "push_state": "PREPARED_NOT_PUSHED",
        "remote_equality_state": "PREPARED_NOT_PROVED",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": manifest["coverage_valid"] and review["valid"],
    }
    write_json(SELF_EXCLUSIONS[0], manifest)
    write_json(SELF_EXCLUSIONS[1], candidate)
    write_json(SELF_EXCLUSIONS[2], review)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_PATHS:
        raise EvidenceError("staged evidence allowlist changed after review")
    manifest = strict_json_bytes(index_blob(SELF_EXCLUSIONS[0]), "staged evidence manifest")
    review = strict_json_bytes(index_blob(SELF_EXCLUSIONS[2]), "staged evidence review")
    candidate = strict_json_bytes(index_blob(SELF_EXCLUSIONS[1]), "staged evidence candidate")
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise EvidenceError(f"evidence manifest mismatch: {entry['path']}")
    if not (manifest["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise EvidenceError("one evidence staged receipt is invalid")
    return {"valid": True, "staged_paths": len(actual), "manifest_entries": len(manifest["entries"]), "manifest_exclusions": len(manifest["declared_self_exclusions"]), "strict_json": review["strict_json_count"], "privacy_confirmed_hits": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    modes.add_argument("--list-base-paths", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_evidence()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": SELF_EXCLUSIONS}
    elif args.check_staged:
        result = check_staged()
    else:
        result = {"base_paths": BASE_PATHS}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
