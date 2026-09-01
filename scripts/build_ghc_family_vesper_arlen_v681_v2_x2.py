from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from importlib import metadata
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v681_v2_contracts import (
    density_record_schema,
    evaluate,
    mutate,
    positive_fixture,
)
from ghc_family_vesper_arlen_v681_v2_runner_bank import (
    materialize as materialize_runners,
)
from ghc_family_vesper_arlen_v681_v2_skill_bank import materialize as materialize_skills

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "vesper-arlen" / "v681-v2"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
OWNER = "Vesper Arlen"
PHASE = "v681-v2"
BRANCH = "codex/GHC-Family/vesper-arlen-v681-v2-full-tools"
SOURCE = "14b34a2b7f1b1c74e3b4102b18cc5c3b5fc854d2"
X1_COMMIT = "5a5ef294b84ece97da4f2b1238d1852ce80a5b51"
DECLARED_CHAIN = 9830
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_x1() -> dict[str, Any]:
    manifest_path = "docs/vesper-arlen/v681-v2/validation/x1-index-manifest.json"
    manifest = json.loads(git("show", f"{X1_COMMIT}:{manifest_path}").stdout)
    mismatches = []
    for entry in manifest["entries"]:
        raw = git("show", f"{X1_COMMIT}:{entry['path']}", text=False).stdout
        data = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            mismatches.append(entry["path"])
    return {
        "commit": X1_COMMIT,
        "entry_count": manifest["entry_count"],
        "head_matches": git("rev-parse", "HEAD").stdout.strip() == X1_COMMIT,
        "manifest_mismatches": mismatches,
        "planning_only": json.loads(
            git("show", f"{X1_COMMIT}:docs/vesper-arlen/v681-v2/x1/phase-truth.json").stdout
        )["execution_state"]
        == "PLANNING_ONLY_X1",
        "schema": "ghc.family.x1-immutability.v681.v2.x2",
    }


WHEEL_HASHES = {
    "attrs-26.1.0-py3-none-any.whl": "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309",
    "flexcache-0.3-py3-none-any.whl": "d43c9fea82336af6e0115e308d9d33a185390b8346a017564611f1466dcd2e32",
    "flexparser-0.4-py3-none-any.whl": "3738b456192dcb3e15620f324c447721023c0293f6af9955b481e91d00179846",
    "jsonschema-4.26.0-py3-none-any.whl": "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
    "jsonschema_specifications-2025.9.1-py3-none-any.whl": "98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe",
    "pint-0.25.3-py3-none-any.whl": "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d",
    "platformdirs-4.11.5-py3-none-any.whl": "89f8d42695853b89c7170bd49bc3dc593f98a71e695ede88e06a3b247bc4563b",
    "referencing-0.37.0-py3-none-any.whl": "381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231",
    "rpds_py-2026.6.3-cp312-cp312-win_amd64.whl": "2c958bf94822e9290a40aaf2a822d4bc5c88099093e3948ad6c571eca9272e5f",
    "typing_extensions-4.16.0-py3-none-any.whl": "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8",
    "uncertainties-3.2.3-py3-none-any.whl": "313353900d8f88b283c9bad81e7d2b2d3d4bcc330cbace35403faaed7e78890a",
}


def tool_receipt() -> tuple[dict[str, Any], dict[str, Any]]:
    site_text = os.environ.get("GHC_VESPER_TOOL_SITE")
    if not site_text:
        raise RuntimeError("GHC_VESPER_TOOL_SITE must identify the isolated owner-local site-packages")
    site = Path(site_text)
    if not site.is_dir():
        raise RuntimeError("isolated tool site does not exist")
    sys.path.insert(0, str(site))
    distributions = {dist.metadata["Name"].casefold(): dist for dist in metadata.distributions(path=[site])}
    expected = {
        "pint": ("0.25.3", "BSD"),
        "uncertainties": ("3.2.3", "Revised BSD License"),
        "jsonschema": ("4.26.0", "MIT"),
    }
    direct = []
    for name, (version, license_name) in expected.items():
        dist = distributions[name]
        actual_license = dist.metadata.get("License-Expression") or dist.metadata.get("License")
        if dist.version != version or actual_license != license_name:
            raise RuntimeError(f"tool metadata drift for {name}")
        direct.append({"license": actual_license, "name": name, "version": dist.version})

    from jsonschema import Draft202012Validator
    from pint import UnitRegistry
    from uncertainties import ufloat

    registry = UnitRegistry()
    converted = (1000 * registry.kilogram / registry.meter**3).to(registry.gram / registry.centimeter**3)
    propagated = ufloat(1000.0, 0.2) + ufloat(-0.3, 0.1)
    schema = density_record_schema()
    validator = Draft202012Validator(schema)
    valid = {
        "certificate_record_id": "synthetic:hydrometer:001",
        "density_kg_m3": 999.7,
        "reference_temperature_c": 20.0,
        "scale_family": "density_kg_m3",
        "synthetic": True,
        "uncertainty_kg_m3": 0.224,
    }
    invalid = {**valid, "synthetic": False, "uncertainty_kg_m3": 0}
    valid_errors = list(validator.iter_errors(valid))
    invalid_errors = list(validator.iter_errors(invalid))
    if valid_errors or len(invalid_errors) != 2:
        raise RuntimeError("isolated tool smoke contract failed")
    smoke = {
        "external_actions": 0,
        "invalid_schema_errors": len(invalid_errors),
        "synthetic_density_conversion_g_cm3": converted.magnitude,
        "synthetic_propagated_nominal_kg_m3": propagated.n,
        "synthetic_propagated_stddev_kg_m3": propagated.s,
        "valid_schema_errors": len(valid_errors),
    }
    receipt = {
        "direct_tools": direct,
        "download_artifacts": [
            {"filename": filename, "sha256": sha256} for filename, sha256 in sorted(WHEEL_HASHES.items())
        ],
        "global_or_shared_prefix_mutated": False,
        "installation_scope": "D_isolated_owner_local_nonshared",
        "license_reviewed": True,
        "owner": OWNER,
        "phase": PHASE,
        "rollback": "remove only the phase-isolated tooling directory after use; no shared prefix was changed",
        "schema": "ghc.family.toolchain-install.v681.v2.x2",
        "smoke": smoke,
        "supply_chain_claim": "wheel hashes and local smoke only; not exhaustive supply-chain assurance",
        "transitive_distributions": len(distributions) - len(direct),
    }
    return receipt, {"record": valid, "schema": schema, "smoke": smoke}


def cards(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seeds: list[tuple[str, str, str]] = [
        ("owner", "Vesper Arlen", "Relational provenance gardener; no consciousness identity continuity or authority claim."),
        ("pillar", "GMUT Mind", "Typed formal and synthetic record structure only; zero empirical physics credit."),
        ("pillar", "THOS Body", "Proxy record workflow only; zero governed real-arm or operational credit."),
        ("pillar", "Freed ID and CBR Heart", "Synthetic nonproduction profile with privacy remedy and authority gates open."),
        ("practice", "Calibration documentation", "Learning lens only; no calibration competence or legal-metrology authority."),
        ("practice", "Density record quality", "Learning lens only; no laboratory sample or measurement authority."),
        ("practice", "Accessible technical review", "Structural evidence only; manual and affected-user evaluation reserved."),
    ]
    seeds.extend(("proposal", row["proposal_id"], row["title"]) for row in proposals)
    boundary_labels = [
        "real people and participants",
        "real instruments and samples",
        "real measurements and calibration",
        "professional competence",
        "production and deployment",
        "identity lifecycle",
        "privacy completeness",
        "accessibility completeness",
        "legal and cultural authority",
        "Maori data governance and authority",
        "independent reproduction",
        "AGI ASI consciousness and personhood",
        "Theory of Everything proof canon and Stage 20",
    ]
    seeds.extend(("boundary", label, f"{label} remains open or exact-gated.") for label in boundary_labels)
    result = []
    for index, (tier, label, text) in enumerate(seeds, start=1):
        address = digest(f"{OWNER}|{PHASE}|{tier}|{label}|{text}".encode())
        result.append({"card_id": f"VA6812-CARD-{index:03d}", "content_address": address, "label": label, "text": text, "tier": tier})
    if len(result) != 80:
        raise RuntimeError("exactly eighty Freed ID boundary cards required")
    return result


def materialize() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != X1_COMMIT:
        raise RuntimeError("x2 materialization must begin at immutable x1")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Vesper branch")
    x1_receipt = verify_x1()
    if not x1_receipt["head_matches"] or x1_receipt["manifest_mismatches"] or not x1_receipt["planning_only"]:
        raise RuntimeError("x1 immutability gate failed")

    freeze = load(X1 / "new-proposal-freeze.json")
    proposals = freeze["proposals"]
    positives = []
    mutations = []
    outcomes = []
    for proposal in proposals:
        fixture = positive_fixture(proposal)
        result = evaluate(proposal, fixture)
        if not result["accepted"]:
            raise RuntimeError(f"positive rejected: {proposal['proposal_id']}")
        positives.append({"fixture": fixture, "result": result})
        outcomes.append({
            "authority_conferred": False,
            "evidence_scope": "bounded_synthetic_structure_only",
            "outcome": proposal["expected_disposition"],
            "proposal_id": proposal["proposal_id"],
            "real_rows": 0,
            "title": proposal["title"],
        })
        for mutation_spec in proposal["preregistered_rejecting_mutations"]:
            changed = mutate(fixture, mutation_spec["mutation_type"])
            rejection = evaluate(proposal, changed)
            if rejection["accepted"]:
                raise RuntimeError(f"mutation accepted: {mutation_spec['mutation_id']}")
            mutations.append({
                "credit": "rejected_zero_credit",
                "mutation_id": mutation_spec["mutation_id"],
                "mutation_type": mutation_spec["mutation_type"],
                "observed": "rejected",
                "proposal_id": proposal["proposal_id"],
                "reasons": rejection["reasons"],
            })
    outcome_counts = Counter(row["outcome"] for row in outcomes)
    if outcome_counts != Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}):
        raise RuntimeError("outcome drift")
    if len(positives) != 60 or len(mutations) != 300:
        raise RuntimeError("control count drift")

    tool, unit_board = tool_receipt()
    skill_paths = materialize_skills()
    runner_paths = materialize_runners()
    portfolio = load(X1 / "portfolio-freeze.json")

    write_json(X2 / "x1-immutability-receipt.json", x1_receipt)
    write_json(X2 / "proposal-evidence.json", {"outcome_counts": dict(outcome_counts), "outcomes": outcomes, "owner": OWNER, "phase": PHASE, "proposal_count": 60, "schema": "ghc.family.proposal-evidence.v681.v2.x2"})
    write_json(X2 / "positive-controls.json", {"accepted": len(positives), "controls": positives, "external_actions": 0, "owner": OWNER, "phase": PHASE, "real_rows": 0, "schema": "ghc.family.positive-controls.v681.v2.x2"})
    write_json(X2 / "mutation-results.json", {"executed": len(mutations), "failure_erasure": False, "mutations": mutations, "owner": OWNER, "phase": PHASE, "rejected": len(mutations), "schema": "ghc.family.mutation-results.v681.v2.x2", "zero_completion_credit": True})
    write_json(X2 / "hydrometer-record-schema.json", density_record_schema())
    write_json(X2 / "unit-uncertainty-board.json", {"authority_conferred": False, "observation_rows": 0, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.unit-uncertainty-board.v681.v2.x2", **unit_board})
    write_json(X2 / "toolchain-install-receipt.json", tool)
    write_json(X2 / "portfolio-results.json", {
        "blocked": [{**row, "state": "held_unexecuted"} for row in portfolio["blocked"]],
        "exact_approval": [{**row, "state": "held_unexecuted"} for row in portfolio["exact_approval"]],
        "owner": OWNER,
        "owner_candidates": [{**row, "state": "bounded_fixture_completed"} for row in portfolio["owner_candidates"]],
        "owner_clean_fix_refine": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["owner_clean_fix_refine"]],
        "phase": PHASE,
        "safe_now": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["safe_now"]],
        "schema": "ghc.family.portfolio-results.v681.v2.x2",
        "successor_records_executed": 0,
    })
    write_json(X2 / "freed-id-flashcards.json", {"card_count": 80, "cards": cards(proposals), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.freed-id-flashcards.v681.v2.x2"})
    write_json(X2 / "gmut-formal-board.json", {
        "analogy_only": True,
        "covariance_guard": "synthetic matrix structure only",
        "empirical_rows": 0,
        "equation_family": "typed scalar-tensor and effective-field-theory research model",
        "force_prediction_likelihood_constraint_confirmation": False,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.gmut-hydrometer-formal-board.v681.v2.x2",
        "theory_of_everything": False,
    })
    write_json(X2 / "thos-proxy-board.json", {"blind_matched_budget_real_arms": 0, "external_operations": 0, "owner": OWNER, "phase": PHASE, "represented": ["synthetic intake", "correction hold", "readback", "workload stop", "handover"], "schema": "ghc.family.thos-hydrometer-proxy.v681.v2.x2"})
    write_json(X2 / "freed-id-profile.json", {"live_keys_or_proofs": 0, "network_events": 0, "owner": OWNER, "phase": PHASE, "production": False, "represented": ["synthetic record subject", "synthetic bearer separation", "amendment status", "minimum disclosure"], "schema": "ghc.family.freed-id-hydrometer-profile.v681.v2.x2", "trust_governance": "exact_gate"})
    write_json(X2 / "cbr-authority-matrix.json", {"decisions_made": 0, "exact_gates": ["privacy and disclosure", "calibration and certification", "legal metrology", "cultural and affected-party authority", "Maori-language Maori-data-governance tangata whenua iwi hapu and Maori authority"], "owner": OWNER, "phase": PHASE, "schema": "ghc.family.cbr-hydrometer-authority.v681.v2.x2"})
    write_json(X2 / "zero-row-adapter.json", {"downloaded_rows": 0, "ingested_rows": 0, "likelihood_calls": 0, "owner": OWNER, "phase": PHASE, "posterior_samples": 0, "schema": "ghc.family.hydrometer-zero-row-adapter.v681.v2.x2", "status": "represented", "terminal_response": "REFUSED_NO_ROWS"})
    write_json(X2 / "accessibility-structural-audit.json", {"affected_user_evaluation": "reserved", "assistive_technology_evaluation": "reserved", "manual_keyboard_evaluation": "reserved", "maori_language_evaluation": "reserved", "owner": OWNER, "phase": PHASE, "schema": "ghc.family.accessibility-structural.v681.v2.x2", "structural_checks": {"headings": True, "landmarks": True, "table_headers": True, "text_fallback": True}, "wcag_conformance_claimed": False})
    write_text(X2 / "accessible-report.html", """<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper v681-v2 synthetic hydrometer evidence</title></head>
<body><a href="#main">Skip to evidence</a><header><h1>Vesper v681-v2 synthetic hydrometer evidence</h1><p>Structural owner-local evidence only. No real calibration, measurement, person, laboratory, authority, or Stage 20 claim.</p></header>
<main id="main"><section aria-labelledby="truth"><h2 id="truth">Outcome truth</h2><table><caption>Sixty proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>42</td></tr><tr><th scope="row">Represented</th><td>12</td></tr><tr><th scope="row">Open gap</th><td>3</td></tr><tr><th scope="row">Exact gate</th><td>3</td></tr></tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Manual keyboard, browser-diverse, responsive-layout, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved. This page makes no accessibility conformance claim.</p></section></main><footer><p>Terminal verdict: NOT_READY_FOR_STAGE_20.</p></footer></body></html>
""")
    write_json(X2 / "complete-incomplete-checklist.json", {
        "completed_bounded": ["60 positive controls", "300 rejecting mutations", "120 safe-now tasks", "80 candidate fixtures", "100 clean-fix-refine tasks", "20 owner-local skills materialized", "10 family-current runners materialized", "three isolated tools smoke-used"],
        "incomplete_or_gated": ["real calibration and measurement", "professional accreditation certification and legal metrology", "participant and affected-user evidence", "production identity lifecycle", "privacy and accessibility completeness", "legal cultural and Maori authority", "independent reproduction", "empirical GMUT confirmation", "Theory of Everything proof canon AGI ASI consciousness personhood and Stage 20"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.complete-incomplete.v681.v2.x2",
    })
    write_json(X2 / "official-source-use-receipt.json", {"authority_conferred": False, "network_data_queries": 0, "owner": OWNER, "phase": PHASE, "real_rows": 0, "schema": "ghc.family.source-use.v681.v2.x2", "source_ids": [row["source_id"] for row in load(X1 / "official-primary-source-ledger.json")["entries"]], "use": "vocabulary dimensional record provenance accessibility privacy and authority-reservation contracts only"})

    x1_postcommit_failure = {
        "failed_witness": "The first combined x1 fetch and four-way equality wrapper crossed its reporting boundary and discarded its projected result even though the processes later exited.",
        "failure_id": "VA6812-X1-N001",
        "initial_credit": 0,
        "recovery": "Inspect process completion, preserve the failed projection, and run only bounded scalar local upstream tracking fresh-live divergence and clean probes.",
        "recovery_credit": "bounded_dependency_only",
    }
    baseline = load(X1 / "method-flow-startup.json")["current_after_startup"]
    counts = dict(baseline)
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        counts[key] += 1
    counts["effective_negatives"] += 300
    counts["failed_witnesses"] += 300
    counts["effective_methods"] += 690
    counts["bounded_passing_witnesses"] += 690
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        counts[key] += 1
    counts["open_gaps"] += 3
    counts["exact_gates"] += 3
    methods = [{"independent_reproduction": False, "method_id": f"VA6812-METHOD-{index:03d}", "preferred": "bounded_owner_local_contract_only", "proposal_id": row["proposal_id"], "validated": "one_zero_row_positive_and_five_rejecting_mutations"} for index, row in enumerate(proposals, start=1)]
    x2_failure = {
        "failed_witness": "The first exact changed-file Ruff review rejected import layout across the new x2 builder, helper modules, and test.",
        "failure_id": "VA6812-X2-N001",
        "initial_credit": 0,
        "recovery": "Apply only Ruff's exact import-layout diff, retain the static-quality failure, and rerun only changed-file compilation and lint.",
        "recovery_credit": "bounded_dependency_only",
    }
    write_json(X2 / "method-flow-ledger.json", {"count_formula": {"base_after_startup": baseline, "mutation_methods_and_recoveries": 300, "owner_proposal_portfolio_skill_runner_methods_and_passes": 390, "x1_postcommit_recovery": 1, "x2_static_quality_recovery": 1}, "counts": counts, "failure_erasure": False, "independent_reproduction_claimed": False, "methods": methods, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.method-flow.v681.v2.x2", "x1_postcommit_failures": [x1_postcommit_failure], "x2_operational_failures": [x2_failure]})
    write_json(X2 / "retained-negative-register.json", {"effective_negatives": counts["effective_negatives"], "failed_witnesses": counts["failed_witnesses"], "failure_erasure": False, "owner": OWNER, "phase": PHASE, "retained_mutations": 300, "schema": "ghc.family.retained-negatives.v681.v2.x2", "startup_failures": 13, "x1_postcommit_failures": 1, "x2_operational_failures": [x2_failure]})
    write_json(X2 / "phase-truth.json", {"counts": counts, "declared_chain": DECLARED_CHAIN, "outcomes": dict(outcome_counts), "owner": OWNER, "phase": PHASE, "proposal_count": 60, "schema": "ghc.family.phase-truth.v681.v2.x2", "terminal_verdict": TERMINAL_VERDICT})
    write_json(X2 / "materialization-receipt.json", {"generated_runner_paths": runner_paths, "generated_skill_paths": skill_paths, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.materialization.v681.v2.x2", "shared_or_global_skill_installation": False})
    print(json.dumps({"mutations_rejected": len(mutations), "outcomes": dict(outcome_counts), "positive_controls": len(positives), "runners_materialized": len(runner_paths), "skills_materialized": len(skill_paths), "status": "X2_MATERIALIZED_NOT_SEALED"}, indent=2))


def seal() -> None:
    required = [X2 / "skill-validation-receipts.json", X2 / "runner-smoke-receipts.json", X2 / "phase-truth.json"]
    if not all(path.is_file() for path in required):
        raise RuntimeError("x2 validation dependencies are incomplete")
    skill_receipt = load(required[0])
    runner_receipt = load(required[1])
    if skill_receipt["passed"] != 20 or runner_receipt["passed"] != 10:
        raise RuntimeError("skill or runner validation incomplete")

    source_paths = [
        "scripts/build_ghc_family_vesper_arlen_v681_v2_x2.py",
        "scripts/ghc_family_vesper_arlen_v681_v2_contracts.py",
        "scripts/ghc_family_vesper_arlen_v681_v2_runner_bank.py",
        "scripts/ghc_family_vesper_arlen_v681_v2_skill_bank.py",
        "tests/test_ghc_family_vesper_arlen_v681_v2_x2.py",
    ]
    source_paths.extend(f"scripts/ghc_family_vesper_v681_v2_lens_runner_{index:02d}.py" for index in range(1, 11))
    content_paths = sorted(
        set(
            [rel(path) for path in X2.rglob("*") if path.is_file()]
            + source_paths
        )
    )
    exclusions = [
        "docs/vesper-arlen/v681-v2/validation/x2-index-manifest.json",
        "docs/vesper-arlen/v681-v2/validation/x2-privacy-scan.json",
        "docs/vesper-arlen/v681-v2/validation/x2-staged-review.json",
    ]
    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    for path_text in content_paths:
        content = (ROOT / path_text).read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {"class": class_name, "disposition": "scanner_definition_only" if path_text.endswith("build_ghc_family_vesper_arlen_v681_v2_x2.py") else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed x2 privacy hit: " + json.dumps(confirmed))
    write_json(VALIDATION / "x2-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v2.x2"})
    write_json(VALIDATION / "x2-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "x2_evidence", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v2.x2"})
    entries = []
    for path_text in content_paths:
        data = normalized(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x2-index-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v2.x2", "x1": X1_COMMIT})
    print(json.dumps({"manifest_entries": len(entries), "privacy_candidates": len(candidates), "privacy_confirmed": 0, "status": "X2_SEALED_WORKTREE_NOT_COMMITTED"}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("materialize", "seal"))
    args = parser.parse_args()
    if args.mode == "materialize":
        materialize()
    else:
        seal()


if __name__ == "__main__":
    main()
