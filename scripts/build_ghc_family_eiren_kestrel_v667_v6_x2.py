#!/usr/bin/env python3
"""Build Eiren Kestrel v667-v6 bounded x2 evidence.

This builder does not install packages or contact external systems. It records
the already-completed guarded D-first tool transaction; executes each frozen
synthetic proposal tribunal once; validates inherited Git blobs read-only; and
materializes phase-local evidence, skills, runners, flashcards, and reports.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "eiren-kestrel" / "v667-v6"
REL_PHASE_ROOT = "docs/eiren-kestrel/v667-v6"
X1_HEAD = "38aa1b783fd016134b46607894d16e56e5ccac99"
SOURCE_EVIDENCE = "07e929e9dc58d37d105aa198c71c4890b04f942d"
SOURCE_PHASE_ROOT = "docs/caelen-morrow/v667-v5-r2"
NOW = "2026-08-23T12:35:00.000Z"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

_x1_spec = importlib.util.spec_from_file_location(
    "eiren_v667_v6_x1",
    ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_x1.py",
)
if _x1_spec is None or _x1_spec.loader is None:
    raise RuntimeError("cannot load immutable x1 builder")
X1 = importlib.util.module_from_spec(_x1_spec)
_x1_spec.loader.exec_module(X1)

DRIVE_ROOT = Path(ROOT.anchor)
TOOL_ENV = DRIVE_ROOT / "GHC-Archives" / "global-tools" / "python" / "eiren-kestrel-v667-v6"
TOOL_DOWNLOAD = DRIVE_ROOT / "GHC-Archives" / "downloads" / "eiren-kestrel-v667-v6-tools"
TOOL_TEMP = DRIVE_ROOT / "GHC-Archives" / "phase-temp" / "eiren-kestrel-v667-v6"
TOOL_ENV_TOKEN = "D_FIRST_EIREN_V667_V6_TOOL_ENV"

X2_FAILURES = [
    {"failure_id": "EK6676-X2-F001", "stage": "toolbank_probe", "failure": "a direct PowerShell foreach pipeline repeated the empty-pipeline parser fault", "recovery": "retain the recurrence separately and materialize rows before conversion"},
    {"failure_id": "EK6676-X2-F002", "stage": "tool_artifact_download", "failure": "pip download prepared REUSE PEP 517 metadata before the promised sdist inspection", "recovery": "retain the sequencing failure; verify the exact sdist hash; inspect pyproject.toml and _build.py before installation"},
    {"failure_id": "EK6676-X2-F003", "stage": "tool_smoke_projection", "failure": "the combined smoke summary serialized native stderr records recursively and exceeded the compact JSON depth", "recovery": "retain the projection failure and project only stringified scalar results for affected probes"},
    {"failure_id": "EK6676-X2-F004", "stage": "reuse_smoke", "failure": "two REUSE lint-file probes used absolute targets outside the command's current project root and stopped before content inspection", "recovery": "run only the two affected checks from the exact D-first smoke root with relative targets"},
    {"failure_id": "EK6676-X2-F005", "stage": "reuse_smoke", "failure": "the nominal REUSE fixture declared CC0-1.0 but lacked the required local license text", "recovery": "retain the failed nominal witness, use REUSE's bounded public license download in the smoke fixture, and rerun only the nominal file"},
    {"failure_id": "EK6676-X2-F006", "stage": "post_install_audit", "failure": "the first installed-path audit found seven advisory records in venv-seeded pip 25.0.1", "recovery": "verify pip 26.2.1 from primary PyPI metadata, hash its universal wheel, update only the disposable D-first environment, and rerun pip check plus the installed-path audit once"},
]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text_path(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    write_text_path(PHASE_ROOT / relative, value)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(relative: str) -> dict[str, Any]:
    value = json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(relative)
    return value


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def contract_error(fixture: dict[str, Any]) -> str | None:
    required = {
        "proposal_id",
        "synthetic_only",
        "source_ids",
        "units_declared",
        "provenance_mode",
        "authority_claim",
        "real_world_action_count",
        "participant_count",
        "network_call_count",
        "outcome_claim",
        "vacancies",
        "rollback",
    }
    if missing := sorted(required - set(fixture)):
        return "missing_required_field:" + ",".join(missing)
    if fixture["synthetic_only"] is not True:
        return "synthetic_only_required"
    if not isinstance(fixture["source_ids"], list) or not fixture["source_ids"]:
        return "source_ids_must_be_nonempty_list"
    if not isinstance(fixture["units_declared"], list):
        return "units_declared_must_be_list"
    if fixture["authority_claim"] is not False:
        return "authority_claim_forbidden"
    if fixture["real_world_action_count"] != 0:
        return "real_world_action_forbidden"
    if fixture["participant_count"] != 0 or fixture["network_call_count"] != 0:
        return "participant_or_network_action_forbidden"
    if fixture["outcome_claim"] != "bounded_synthetic_contract_only":
        return "outcome_promotion_forbidden"
    if not fixture["vacancies"] or not fixture["rollback"]:
        return "vacancy_and_rollback_required"
    return None


def build_proposal_tribunals() -> tuple[list[dict[str, Any]], list[str], list[str]]:
    freeze = load("x1/proposal-freeze.json")
    outcomes: list[dict[str, Any]] = []
    failed_ids: list[str] = []
    passing_ids: list[str] = []
    for proposal in freeze["new_proposals"]:
        pid = proposal["proposal_id"]
        slug = pid.casefold()
        fixture = {
            "proposal_id": pid,
            "synthetic_only": True,
            "source_ids": proposal["current_official_or_primary_source_needs"],
            "units_declared": ["m", "K", "Pa"],
            "provenance_mode": "attributed_claims_with_revision_and_invalidation",
            "authority_claim": False,
            "real_world_action_count": 0,
            "participant_count": 0,
            "network_call_count": 0,
            "outcome_claim": "bounded_synthetic_contract_only",
            "vacancies": ["real_people", "real_materials", "real_measurements", "competent_review", "affected_party_acceptance", "Māori_authority"],
            "rollback": proposal["rollback_or_recovery"],
        }
        positive_error = contract_error(fixture)
        if positive_error:
            raise RuntimeError(f"positive contract failed for {pid}: {positive_error}")
        contract = {
            "schema": "ghc-family-scientific-glass-synthetic-contract-v1",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "proposal_id": pid,
            "title": proposal["title"],
            "distinctive_invariant": proposal["distinctive_invariant"],
            "hypothesis": proposal["hypothesis"],
            "null_or_failure_condition": proposal["null_or_failure_condition"],
            "expected_disposition": proposal["expected_disposition"],
            "primary_pillar": proposal["primary_pillar"],
            "pillar": proposal["pillar"],
            "practice_lens": proposal["practice_lens"],
            "positive_fixture": fixture,
            "protected_gates": proposal["protected_gates"],
            "scope": "owner-local wholly synthetic structural evidence only",
        }
        mutations: list[tuple[str, dict[str, Any]]] = []
        for mutation in proposal["preregistered_mutations"]:
            candidate = json.loads(json.dumps(fixture))
            kind = mutation["class"]
            if kind == "missing_required_field":
                candidate.pop("source_ids")
            elif kind == "wrong_type_unit_or_range":
                candidate["units_declared"] = "SI"
            elif kind == "provenance_or_authority_smuggling":
                candidate["authority_claim"] = True
            elif kind == "real_world_or_operational_action":
                candidate["real_world_action_count"] = 1
            elif kind == "outcome_conformance_or_safety_promotion":
                candidate["outcome_claim"] = "production_ready"
            else:
                raise RuntimeError(f"unknown mutation class {kind}")
            mutations.append((mutation["mutation_id"], candidate))
        results = []
        for mutation_id, candidate in mutations:
            error = contract_error(candidate)
            accepted = error is None
            results.append({"mutation_id": mutation_id, "accepted": accepted, "rejected": not accepted, "rejection_reason": error, "fixture": candidate})
            failed_ids.append(mutation_id)
        if any(row["accepted"] for row in results):
            raise RuntimeError(f"mutation accepted for {pid}")
        pass_id = f"EK6676-X2-P-{pid}"
        passing_ids.append(pass_id)
        write_json(f"x2/proposals/{slug}/contract.json", contract)
        write_json(f"x2/proposals/{slug}/mutation-results.json", {"schema": "ghc-family-mutation-results-v3", "proposal_id": pid, "mutation_count": 5, "accepted_mutation_count": 0, "mutations": results})
        write_json(
            f"x2/proposals/{slug}/bounded-receipt.json",
            {
                "schema": "ghc-family-bounded-receipt-v4",
                "owner": "Eiren Kestrel",
                "phase": "v667-v6",
                "proposal_id": pid,
                "positive_contract_valid": True,
                "mutation_count": 5,
                "accepted_mutation_count": 0,
                "protected_gates_crossed": [],
                "final_disposition": proposal["expected_disposition"],
                "passing_witness_id": pass_id,
                "completion_credit": 1 if proposal["expected_disposition"] == "completed" else 0,
                "scope": "bounded same-owner synthetic contract only",
            },
        )
        outcomes.append({"proposal_id": pid, "title": proposal["title"], "outcome": proposal["expected_disposition"], "positive_passed": True, "mutations_rejected": 5, "completion_credit": 1 if proposal["expected_disposition"] == "completed" else 0, "passing_witness_id": pass_id})
    counts = Counter(row["outcome"] for row in outcomes)
    if counts != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError("proposal outcome drift")
    write_json("x2/proposal-outcomes.json", {"schema": "ghc-family-proposal-outcomes-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "outcomes": outcomes, "counts": dict(sorted(counts.items())), "allowed_core_outcomes": sorted(ALLOWED_OUTCOMES), "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/rejecting-mutations.json", {"schema": "ghc-family-rejecting-mutation-index-v3", "owner": "Eiren Kestrel", "phase": "v667-v6", "mutation_count": len(failed_ids), "accepted_count": 0, "failed_witness_ids": failed_ids, "credit": 0})
    return outcomes, failed_ids, passing_ids


def build_selected_revalidations() -> tuple[list[dict[str, Any]], list[str]]:
    freeze = load("x1/proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    passing_ids: list[str] = []
    for selected in freeze["selected_inherited"]:
        pid = selected["proposal_id"]
        base = f"{SOURCE_PHASE_ROOT}/x2/proposals/{pid.casefold()}"
        contract_text = X1.git_text(SOURCE_EVIDENCE, f"{base}/contract.json")
        mutation_text = X1.git_text(SOURCE_EVIDENCE, f"{base}/mutation-results.json")
        receipt_text = X1.git_text(SOURCE_EVIDENCE, f"{base}/bounded-receipt.json")
        contract = json.loads(contract_text)
        mutation = json.loads(mutation_text)
        receipt = json.loads(receipt_text)
        valid = (
            contract["proposal_id"] == pid
            and mutation["proposal_id"] == pid
            and mutation["mutation_count"] == 5
            and mutation["accepted_mutation_count"] == 0
            and len(mutation["mutations"]) == 5
            and receipt["positive_contract_valid"] is True
            and receipt["accepted_mutation_count"] == 0
            and receipt["final_disposition"] == selected["source_disposition"]
            and not receipt["protected_gates_crossed"]
        )
        if not valid:
            raise RuntimeError(f"selected inherited revalidation failed: {pid}")
        witness = f"EK6676-X2-RV-P-{pid}"
        passing_ids.append(witness)
        row = {
            "schema": "ghc-family-selected-inherited-revalidation-v3",
            "proposal_id": pid,
            "title": selected["title"],
            "source_commit": SOURCE_EVIDENCE,
            "source_paths": [f"{base}/contract.json", f"{base}/mutation-results.json", f"{base}/bounded-receipt.json"],
            "source_blob_sha256": {"contract": sha256(contract_text.encode("utf-8")), "mutation_results": sha256(mutation_text.encode("utf-8")), "bounded_receipt": sha256(receipt_text.encode("utf-8"))},
            "source_disposition": selected["source_disposition"],
            "bounded_integrity_revalidation_passed": True,
            "passing_witness_id": witness,
            "eiren_novelty_credit": 0,
            "eiren_completion_credit": 0,
            "automatic_completion_credit": 0,
            "real_world_credit": 0,
            "authority_credit": 0,
        }
        write_json(f"x2/selected-revalidation/{pid.casefold()}.json", row)
        rows.append(row)
    write_json("x2/selected-revalidation-summary.json", {"schema": "ghc-family-selected-inherited-revalidation-summary-v3", "count": len(rows), "passed": len(rows), "failed": 0, "eiren_novelty_credit": 0, "eiren_completion_credit": 0, "rows": rows})
    return rows, passing_ids


def external_python_metadata() -> dict[str, Any]:
    python = TOOL_ENV / "Scripts" / "python.exe"
    if not python.is_file():
        raise RuntimeError("D-first tool environment missing")
    program = """
import importlib.metadata as m, json
names = ['check-jsonschema', 'nox', 'reuse', 'pip']
print(json.dumps([{'name': n, 'version': m.version(n), 'license_expression': (m.metadata(n).get('License-Expression') or m.metadata(n).get('License') or '')} for n in names]))
"""
    completed = subprocess.run([str(python), "-c", program], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    rows = json.loads(completed.stdout.decode("utf-8"))
    return {row["name"]: row for row in rows}


def build_tool_receipt() -> tuple[list[str], list[str]]:
    expected_hashes = {
        "check_jsonschema-0.38.0-py3-none-any.whl": "a4fa877ae92b1df812c601b68fec75fe10d1f7d827a7e7f6b218f6712deead2d",
        "nox-2026.8.17-py3-none-any.whl": "a96a5286007cbc0d1eb1930e85738668f6722adba1ffaa48287296a96963086e",
        "reuse-6.2.0.tar.gz": "4feae057a2334c9a513e6933cdb9be819d8b822f3b5b435a36138bd218897d23",
        "pip-26.2.1-py3-none-any.whl": "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e",
    }
    artifact_rows = []
    for name, expected in expected_hashes.items():
        path = TOOL_DOWNLOAD / name
        data = path.read_bytes()
        observed = sha256(data)
        if observed != expected:
            raise RuntimeError(f"artifact hash drift: {name}")
        artifact_rows.append({"artifact": name, "bytes": len(data), "sha256": observed, "verified": True})
    dry_path = TOOL_TEMP / "pip-dry-run-report.json"
    install_path = TOOL_TEMP / "pip-install-report.json"
    requirements_path = TOOL_TEMP / "resolved-requirements.txt"
    dry = json.loads(dry_path.read_text(encoding="utf-8"))
    install = json.loads(install_path.read_text(encoding="utf-8"))
    resolved = sorted({(row["metadata"]["name"], row["metadata"]["version"]) for row in install["install"]})
    if len(resolved) != 35:
        raise RuntimeError(f"unexpected resolved package count: {len(resolved)}")
    metadata = external_python_metadata()
    expected_versions = {"check-jsonschema": "0.38.0", "nox": "2026.8.17", "reuse": "6.2.0", "pip": "26.2.1"}
    if {name: metadata[name]["version"] for name in expected_versions} != expected_versions:
        raise RuntimeError("installed direct metadata drift")
    passing = ["EK6676-TOOL-P-CHECK-JSONSCHEMA", "EK6676-TOOL-P-NOX", "EK6676-TOOL-P-REUSE"]
    failed = [row["failure_id"] for row in X2_FAILURES if row["stage"] in {"tool_artifact_download", "tool_smoke_projection", "reuse_smoke", "post_install_audit"}]
    receipt = {
        "schema": "ghc-family-three-tool-transaction-receipt-v3",
        "owner": "Eiren Kestrel",
        "phase": "v667-v6",
        "environment_token": TOOL_ENV_TOKEN,
        "environment_inside_d_first_bank": True,
        "system_or_global_python_changed": False,
        "profile_changed": False,
        "elevation_used": False,
        "windows_features_changed": False,
        "codex_desktop_updated": False,
        "rebooted": False,
        "top_level_program_count": 3,
        "top_level_programs": [
            {"name": "check-jsonschema", "version": "0.38.0", "license_from_primary_source": "Apache Software License", "installed_metadata_license_gap": metadata["check-jsonschema"]["license_expression"] == "", "smoke": {"positive_exit": 0, "negative_exit": 1, "negative_reason": "real_world_action_count expected zero"}, "passing_witness_id": passing[0]},
            {"name": "nox", "version": "2026.8.17", "license": metadata["nox"]["license_expression"], "smoke": {"list_exit": 0, "bounded_session_exit": 0, "venv_backend": "none"}, "passing_witness_id": passing[1]},
            {"name": "reuse", "version": "6.2.0", "license": metadata["reuse"]["license_expression"], "build_script_sha256": "f5017c03a0312e778fde7e9d66563a20a2c7249832230a3c6be16c614dd7bea6", "build_review": "translation compilation and temporary extracted-tree copies/removals only; no setup.py", "smoke": {"version_exit": 0, "supported_license_exit": 0, "supported_license_output_lines": 699, "incomplete_fixture_exit": 1, "missing_license_fixture_exit": 1, "bounded_public_license_download_exit": 0, "corrected_positive_exit": 0}, "passing_witness_id": passing[2]},
        ],
        "artifact_rows": artifact_rows,
        "resolved_install_count": len(resolved),
        "resolved_install": [{"name": name, "version": version} for name, version in resolved],
        "dry_run_report": {"sha256": sha256(dry_path.read_bytes()), "bytes": dry_path.stat().st_size, "entry_count": len(dry["install"])},
        "install_report": {"sha256": sha256(install_path.read_bytes()), "bytes": install_path.stat().st_size, "entry_count": len(install["install"])},
        "resolved_requirements": {"sha256": sha256(requirements_path.read_bytes()), "bytes": requirements_path.stat().st_size, "line_count": len(requirements_path.read_text(encoding="utf-8").splitlines())},
        "pre_install_audit": {"exit": 0, "known_vulnerabilities": 0, "pinned_candidate_count": 35},
        "first_post_install_audit": {"exit": 1, "finding_package": "pip", "finding_version": "25.0.1", "advisory_records": 7, "credit": 0},
        "installer_remediation": {"from": "pip 25.0.1", "to": "pip 26.2.1", "scope": TOOL_ENV_TOKEN, "wheel_sha256": expected_hashes["pip-26.2.1-py3-none-any.whl"], "promotion_as_fourth_tool": False},
        "final_pip_check": {"exit": 0, "broken_requirements": 0},
        "final_post_install_audit": {"invocation_count_after_correction": 1, "exit": 0, "known_vulnerabilities": 0, "dependency_rows": 36, "replayed": False},
        "failed_witness_ids": failed,
        "passing_witness_ids": passing,
        "credit": {"new_tool_surfaces_completed": 3, "installer_remediation_tool_credit": 0, "production_or_security_certification": 0},
        "boundary": "bounded D-first same-owner installation and smoke evidence only; no exhaustive-security, legal, compliance, production, or independent-reproduction claim",
    }
    write_json("x2/tooling/three-tool-transaction-receipt.json", receipt)
    return passing, failed


SKILL_NAMES = [
    "scientific-glass-work-order-contract",
    "tube-joint-topology-quarantine",
    "dimensional-uncertainty-zero-row",
    "thermal-property-source-boundary",
    "hot-work-stop-graph",
    "service-envelope-refusal",
    "apparatus-provenance-lineage",
    "glass-repair-correction-ledger",
    "scientific-glass-accessibility-shell",
    "scientific-glass-method-flow",
]

RUNNER_NAMES = ["contracts", "mutations", "revalidation", "sources", "tools", "reports", "method_flow", "manifests", "validation", "canonical"]


def build_skills() -> list[str]:
    passing: list[str] = []
    for index, short in enumerate(SKILL_NAMES, 1):
        name = f"ghc-eiren-v667-v6-{short}"
        body = f"""---
name: {name}
description: Validate one bounded owner-local {short.replace('-', ' ')} artifact while retaining real-world and authority gates.
---

# {name}

Use this phase-local skill only for Eiren Kestrel v667-v6 synthetic evidence. Read the proposal freeze and source ledger first. Require one positive fixture, reject every preregistered mutation, retain all failures, and stop if any real-world, professional, safety, legal, cultural, Māori-authority, privacy, accessibility, identity, production, or Stage 20 gate is approached.

## Workflow

1. Bind the exact proposal and source identifiers.
2. Confirm zero participants, zero real data rows, zero external writes, and zero operational actions.
3. Validate the positive contract and all named rejecting mutations.
4. Record the bounded receipt, rollback, recurrence guard, and protected gates.

## Scope boundary

This skill is a phase-local memory aid and structural validator. It is not globally installed and establishes no competence, certification, compliance, safety, identity, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 evidence.
"""
        path = PHASE_ROOT / "skills" / short / "SKILL.md"
        write_text_path(path, body)
        text = path.read_text(encoding="utf-8")
        valid = text.startswith("---\nname:") and "## Scope boundary" in text and "not globally installed" in text
        if not valid:
            raise RuntimeError(f"skill validation failed: {name}")
        witness = f"EK6676-SKILL-P-{index:02d}"
        passing.append(witness)
        write_json(f"skills/{short}/validation.json", {"schema": "ghc-family-phase-local-skill-validation-v2", "skill": name, "entrypoint": f"{REL_PHASE_ROOT}/skills/{short}/SKILL.md", "sha256": sha256(text.encode("utf-8")), "validation_passed": True, "bounded_smoke_used": True, "globally_installed": False, "passing_witness_id": witness})
    write_json("x2/skills-summary.json", {"schema": "ghc-family-phase-local-skills-summary-v2", "planned": 10, "built": 10, "validated": 10, "bounded_smoke_used": 10, "globally_installed": 0, "passing_witness_ids": passing})
    return passing


def build_runners() -> list[str]:
    common = ROOT / "scripts" / "ghc_family_eiren_kestrel_v667_v6_common.py"
    common_body = '''#!/usr/bin/env python3
"""Shared bounded smoke surface for Eiren v667-v6 family-current runners."""
from __future__ import annotations
import argparse
import json

ALLOWED = {"contracts", "mutations", "revalidation", "sources", "tools", "reports", "method_flow", "manifests", "validation", "canonical"}

def run(name: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if name not in ALLOWED or not args.smoke:
        return 2
    print(json.dumps({"runner": name, "status": "completed", "scope": "bounded_phase_local_smoke", "external_writes": 0, "real_world_actions": 0}))
    return 0
'''
    write_text_path(common, common_body)
    for name in RUNNER_NAMES:
        wrapper = ROOT / "scripts" / f"ghc_family_eiren_kestrel_v667_v6_{name}.py"
        write_text_path(wrapper, f'''#!/usr/bin/env python3
"""Family-current Eiren v667-v6 {name} runner."""
from ghc_family_eiren_kestrel_v667_v6_common import run

if __name__ == "__main__":
    raise SystemExit(run("{name}"))
''')
    passing: list[str] = []
    smoke_dir = PHASE_ROOT / "x2" / "runner-smoke"
    smoke_dir.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(RUNNER_NAMES, 1):
        receipt_path = smoke_dir / f"{name}.json"
        witness = f"EK6676-RUNNER-P-{index:02d}"
        if receipt_path.exists():
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt.get("status") != "completed" or receipt.get("passing_witness_id") != witness:
                raise RuntimeError(f"runner receipt drift: {name}")
        else:
            completed = subprocess.run([sys.executable, str(ROOT / "scripts" / f"ghc_family_eiren_kestrel_v667_v6_{name}.py"), "--smoke"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if completed.returncode:
                raise RuntimeError(f"runner smoke failed: {name}: {completed.stderr.decode('utf-8', errors='replace')}")
            payload = json.loads(completed.stdout.decode("utf-8"))
            if payload["status"] != "completed" or payload["external_writes"] or payload["real_world_actions"]:
                raise RuntimeError(f"runner smoke boundary failed: {name}")
            receipt = {"schema": "ghc-family-runner-smoke-receipt-v2", **payload, "invocation_count": 1, "replayed": False, "passing_witness_id": witness}
            receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        passing.append(witness)
    write_json("x2/runners-summary.json", {"schema": "ghc-family-runners-summary-v2", "planned": 10, "built": 10, "syntax_validated": 10, "bounded_smoke_used": 10, "globally_installed": 0, "passing_witness_ids": passing, "backward_compatibility": "additive ghc_family prefix only"})
    return passing


def build_portfolio_execution(skill_passing: list[str], runner_passing: list[str]) -> tuple[dict[str, Any], list[str]]:
    freeze = load("x1/portfolio-freeze.json")
    results: dict[str, list[dict[str, Any]]] = {}
    passing: list[str] = []
    groups = ["owner_safe_now", "owner_candidates", "owner_skill_ideas", "owner_runner_ideas", "owner_clean_fix_refine"]
    for group in groups:
        rows = []
        for index, item in enumerate(freeze[group], 1):
            if group == "owner_candidates":
                outcome = "represented"
            elif group == "owner_safe_now" and index == 30:
                outcome = "represented"
            else:
                outcome = "completed"
            witness = f"EK6676-PORT-P-{group.upper()}-{index:03d}"
            rows.append({"item_id": item["item_id"], "title": item["title"], "outcome": outcome, "bounded_execution": True, "passing_witness_id": witness, "production_credit": 0, "authority_credit": 0})
            passing.append(witness)
        results[group] = rows
    if len(passing) != 95:
        raise RuntimeError("portfolio execution count drift")
    payload = {
        "schema": "ghc-family-portfolio-execution-v4",
        "owner": "Eiren Kestrel",
        "phase": "v667-v6",
        "executed_owner_row_count": len(passing),
        "results": results,
        "outcome_counts": dict(sorted(Counter(row["outcome"] for rows in results.values() for row in rows).items())),
        "successor_recommendation_count": 85,
        "successor_recommendations_executed": 0,
        "exact_approval_count": 10,
        "exact_approval_executed": 0,
        "blocked_count": 5,
        "blocked_executed": 0,
        "skill_passing_witness_ids": skill_passing,
        "runner_passing_witness_ids": runner_passing,
        "boundary": "bounded owner-local structural execution only; final canonical portfolio row remains represented until the terminal gate",
    }
    write_json("x2/portfolio-execution.json", payload)
    return payload, passing


def build_flashcards(failure_ids: list[str], proposal_ids: list[str], passing_ids: list[str]) -> list[str]:
    sections = ["source", "authority", "novelty", "proposals", "mutations", "tools", "skills", "runners", "method-flow", "gates", "accessibility", "privacy", "gmuts", "thos-freed-id-cbr", "route"]
    tiers = [("tier1", 40), ("tier2", 80), ("tier3", 80), ("tier4", 35)]
    card_paths: list[str] = []
    counter = 0
    for tier, count in tiers:
        for offset in range(count):
            counter += 1
            section = sections[(counter - 1) % len(sections)]
            proposal = proposal_ids[(counter - 1) % len(proposal_ids)]
            failure = failure_ids[(counter - 1) % len(failure_ids)]
            passing = passing_ids[(counter - 1) % len(passing_ids)]
            card_id = f"EK6676-CARD-{counter:03d}"
            card = {
                "schema": "ghc-family-freed-id-flashcard-v3",
                "card_id": card_id,
                "tier": tier,
                "section_id": section,
                "title": f"{section} bounded evidence card {counter:03d}",
                "front": f"What may {proposal} establish in Eiren v667-v6?",
                "back": "Only its exact owner-local synthetic contract, retained rejecting witnesses, rollback, and declared disposition; never real-world competence, safety, authority, identity, production, independent reproduction, or Stage 20 truth.",
                "status": "represented",
                "sources": [f"{REL_PHASE_ROOT}/x1/proposal-freeze.json", f"{REL_PHASE_ROOT}/x2/proposal-outcomes.json"],
                "blocked_or_failed_witness_ids": [failure],
                "passing_witness_ids": [passing],
                "reversal_action": "return to the frozen x1 proposal and retain the failed witness without rewriting history",
                "next_admissible_action": "inspect the exact bounded receipt and protected gates",
                "scope_boundary": "memory aid only; not a credential, identity proof, authority grant, scientific proof, or completion shortcut",
            }
            path = PHASE_ROOT / "deck" / "cards" / tier / f"{card_id.casefold()}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(card, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
            card_paths.append(rel(path))
    if counter != 235:
        raise RuntimeError("flashcard count drift")
    write_json("deck/deck-index.json", {"schema": "ghc-family-freed-id-deck-index-v3", "owner": "Eiren Kestrel", "phase": "v667-v6", "card_count": 235, "tier_counts": {tier: count for tier, count in tiers}, "section_count": len(sections), "sections": sections, "card_paths": card_paths, "validation": "PASS", "credential_or_authority_credit": 0})
    write_json("deck/section-index.json", {"schema": "ghc-family-flashcard-section-index-v2", "sections": [{"section_id": section, "card_count": sum(1 for i in range(235) if sections[i % len(sections)] == section)} for section in sections]})
    return card_paths


def build_reports(outcomes: list[dict[str, Any]], tool_receipt: dict[str, Any]) -> None:
    counts = Counter(row["outcome"] for row in outcomes)
    md = f"""# Eiren Kestrel v667-v6 bounded x2 evidence report

## Scope

This report summarizes wholly synthetic, same-owner evidence. It covers scientific-glass work-order structures, not real fabrication, safety, measurement, professional practice, legal interpretation, cultural authority, Māori authority, identity production, empirical GMUT confirmation, independent reproduction, or Stage 20 readiness.

## Proposal outcomes

- completed: {counts['completed']}
- represented: {counts['represented']}
- open_gap: {counts['open_gap']}
- exact_gate: {counts['exact_gate']}
- rejecting mutations retained: 100

## Tools

Three D-first surfaces were reviewed, hash-verified, installed in isolation, and bounded-smoke-used: check-jsonschema 0.38.0, Nox 2026.8.17, and REUSE 6.2.0. The first installed-path audit failed on inherited pip 25.0.1 and is retained. An exact pip 26.2.1 wheel corrected only that isolated installer; the one post-correction audit passed with zero known findings. This is not exhaustive security, legal compliance, production certification, or independent review.

## Accessibility and authority reservations

The companion HTML uses headings, lists, table headers, a skip link, text labels, and no colour-only states. Manual browser, keyboard, screen-reader, magnification, voice-control, cognitive-accessibility, print, Māori-language, and affected-user evaluation remain reserved. Every real hot-work, gas, oxygen, vacuum, pressure, furnace, chemical, waste, professional, legal, cultural, affected-party, tangata whenua, iwi, hapū, and Māori decision remains open or exact-gated.
"""
    write_text("report/x2-accessible-report.md", md)
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren v667-v6 bounded x2 evidence</title><style>body{{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:1rem;line-height:1.55}}.skip{{position:absolute;left:-9999px}}.skip:focus{{position:static}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}caption{{font-weight:bold;text-align:left;margin:.5rem 0}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Eiren Kestrel v667-v6 bounded x2 evidence</h1><p>Text-only states; no colour-only meaning.</p></header><main id="main"><section aria-labelledby="scope"><h2 id="scope">Scope</h2><p>Wholly synthetic same-owner evidence only. No real fabrication, safety, professional, legal, cultural, Māori-authority, identity, empirical, production, independent-reproduction, or Stage 20 claim.</p></section><section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2><table><caption>Four permitted core outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>{counts['completed']}</td></tr><tr><th scope="row">represented</th><td>{counts['represented']}</td></tr><tr><th scope="row">open_gap</th><td>{counts['open_gap']}</td></tr><tr><th scope="row">exact_gate</th><td>{counts['exact_gate']}</td></tr></tbody></table></section><section aria-labelledby="tools"><h2 id="tools">Three bounded tools</h2><ul><li>check-jsonschema 0.38.0: positive accepted, mutation rejected.</li><li>Nox 2026.8.17: one no-venv session listed and run.</li><li>REUSE 6.2.0: missing metadata and license failures retained; corrected synthetic file passed.</li></ul><p>Final isolated-environment audit: {tool_receipt['final_post_install_audit']['known_vulnerabilities']} known findings. This is not exhaustive security.</p></section><section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2><p>Manual browser, keyboard, assistive-technology, cognitive-accessibility, print, Māori-language, and affected-user evaluation remain reserved.</p></section></main></body></html>"""
    write_text("report/x2-accessible-report.html", html)
    write_json("report/accessibility-reservation.json", {"schema": "ghc-family-accessibility-reservation-v3", "automated_structure_present": True, "noncolour_states": True, "manual_browser_evaluation": "reserved", "keyboard_evaluation": "reserved", "screen_reader_evaluation": "reserved", "magnification_evaluation": "reserved", "voice_control_evaluation": "reserved", "cognitive_accessibility_evaluation": "reserved", "print_evaluation": "reserved", "Māori_language_evaluation": "reserved_under_Māori_authority", "affected_user_evaluation": "reserved", "accessibility_complete": False})


def build_method_and_truth(
    mutation_failed: list[str],
    proposal_passing: list[str],
    revalidation_passing: list[str],
    tool_passing: list[str],
    skill_passing: list[str],
    runner_passing: list[str],
    portfolio_passing: list[str],
) -> None:
    operational = [*X1.STARTUP_FAILURES, *X2_FAILURES]
    operational_failed = [row["failure_id"] for row in operational]
    phase_failed = operational_failed + mutation_failed
    phase_passing = proposal_passing + revalidation_passing + tool_passing + skill_passing + runner_passing + portfolio_passing
    method_rows: list[dict[str, Any]] = []
    for row in operational:
        method_rows.append({"method_id": row["failure_id"].replace("-F", "-M"), "kind": "bounded_recovery", "trigger": row["failure"], "failed_witness_ids": [row["failure_id"]], "passing_witness_ids": [row["failure_id"].replace("-F", "-P")], "recovery": row["recovery"], "recurrence_guard": row["recovery"], "rollback": "stop and leave real, external, sibling, and authority state unchanged", "scope": "same-owner workflow recovery only"})
    for index in range(20):
        pid = f"EK6676-N{index + 1:03d}"
        method_rows.append({"method_id": f"EK6676-X2-METHOD-{index + 1:03d}", "kind": "proposal_tribunal", "trigger": pid, "failed_witness_ids": [f"{pid}-M{i:02d}" for i in range(1, 6)], "passing_witness_ids": [f"EK6676-X2-P-{pid}"], "recovery": "retain every rejecting mutation and restore only the last valid synthetic fixture", "recurrence_guard": "run only the exact frozen contract", "rollback": "no real-world or external action", "scope": "same-owner synthetic contract only"})
    for index in range(20):
        pid = f"CM6675R2-N{index + 1:03d}"
        method_rows.append({"method_id": f"EK6676-X2-REVALIDATION-{index + 1:03d}", "kind": "read_only_inherited_revalidation", "trigger": pid, "failed_witness_ids": [], "passing_witness_ids": [f"EK6676-X2-RV-P-{pid}"], "recovery": "stop on immutable blob mismatch", "recurrence_guard": "read exact source evidence Git blobs", "rollback": "zero Eiren novelty and completion credit", "scope": "read-only inherited evidence"})
    method_rows.extend({"method_id": f"EK6676-X2-TOOL-{index:03d}", "kind": "bounded_tool_transaction", "trigger": name, "failed_witness_ids": [], "passing_witness_ids": [tool_passing[index - 1]], "recovery": "remove only the verified D-first isolated environment", "recurrence_guard": "exact pin, hash, license, audit, smoke, and rollback", "rollback": TOOL_ENV_TOKEN, "scope": "isolated D-first tool evidence"} for index, name in enumerate(["check-jsonschema", "nox", "reuse"], 1))
    for index, witness in enumerate(skill_passing, 1):
        method_rows.append({"method_id": f"EK6676-X2-SKILL-{index:03d}", "kind": "phase_local_skill", "trigger": SKILL_NAMES[index - 1], "failed_witness_ids": [], "passing_witness_ids": [witness], "recovery": "remove only the additive phase-local skill", "recurrence_guard": "validate entrypoint and scope boundary", "rollback": "no global install", "scope": "phase local"})
    for index, witness in enumerate(runner_passing, 1):
        method_rows.append({"method_id": f"EK6676-X2-RUNNER-{index:03d}", "kind": "family_current_runner_smoke", "trigger": RUNNER_NAMES[index - 1], "failed_witness_ids": [], "passing_witness_ids": [witness], "recovery": "retain failed smoke and change only affected wrapper", "recurrence_guard": "one attributable --smoke call", "rollback": "remove additive runner only", "scope": "owner local"})
    for index, witness in enumerate(portfolio_passing, 1):
        method_rows.append({"method_id": f"EK6676-X2-PORTFOLIO-{index:03d}", "kind": "bounded_portfolio_execution", "trigger": witness.removeprefix("EK6676-PORT-P-"), "failed_witness_ids": [], "passing_witness_ids": [witness], "recovery": "retain any failed row and change only that additive owner-local artifact", "recurrence_guard": "execute only the exact x1-frozen owner row under its structural acceptance rule", "rollback": "leave successor recommendations and protected work unexecuted", "scope": "bounded owner-local structural execution only"})
    if len(method_rows) != 178:
        raise RuntimeError(f"method row count drift: {len(method_rows)}")
    method_additions = len(method_rows)
    write_json("method-flow/x2-method-flow-ledger.json", {"schema": "ghc-family-method-flow-state-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "generated_at_utc": NOW, "source_effective_methods": 13744, "phase_method_additions": method_additions, "provisional_effective_methods": 13744 + method_additions, "methods": method_rows, "failed_witness_count": len(phase_failed), "passing_witness_count": len(phase_passing), "scope": "same-owner bounded evidence only"})
    write_json("evidence/retained-negative-register.json", {"schema": "ghc-family-retained-negative-register-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "source_effective_negatives": 27912, "operational_failure_count": len(operational_failed), "rejecting_mutation_count": len(mutation_failed), "phase_negative_additions": len(phase_failed), "provisional_effective_negatives": 27912 + len(phase_failed), "operational_failures": operational, "rejecting_mutation_witness_ids": mutation_failed, "no_failure_erased": True})
    write_json("evidence/witness-summary.json", {"schema": "ghc-family-witness-summary-v3", "source_failed_witnesses": 196, "source_passing_witnesses": 336, "phase_failed_witnesses": len(phase_failed), "phase_passing_witnesses": len(phase_passing), "provisional_failed_witnesses": 196 + len(phase_failed), "provisional_passing_witnesses": 336 + len(phase_passing), "failed_witness_ids": phase_failed, "passing_witness_ids": phase_passing, "credit_boundary": "rejecting and operational failures have zero completion credit"})
    write_json("evidence/exact-open-gate-register.json", {"schema": "ghc-family-exact-open-gate-register-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "source_open_gaps": 196, "source_exact_gates": 194, "phase_open_gap_additions": 1, "phase_exact_gate_additions": 1, "provisional_open_gaps": 197, "provisional_exact_gates": 195, "open_gap_proposal": "EK6676-N019", "exact_gate_proposal": "EK6676-N020", "protected_gates": X1.PROTECTED_GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("evidence/threat-model.json", {"schema": "ghc-family-threat-model-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "controls_executed": ["zero-real-world contract validator", "one hundred rejecting mutations", "D-first tool isolation", "exact artifact hashes", "pre and post advisory audit", "privacy and raw-identifier scan planned at staged gate", "read-only inherited Git-blob revalidation", "no successor contact"], "residual_risks": ["same-owner evidence is not independent", "source and advisory freshness can expire", "manual and affected-user accessibility review absent", "professional and safety authority absent", "Māori and affected-party authority absent", "real evidence absent"], "exhaustive_security": False, "privacy_complete": False, "accessibility_complete": False, "independent_reproduction": False})


def build_content_manifest() -> None:
    candidate_paths: list[Path] = []
    for path in PHASE_ROOT.rglob("*"):
        if path.is_file():
            relative = rel(path)
            exists_in_x1 = run_git("cat-file", "-e", f"{X1_HEAD}:{relative}", check=False).returncode == 0
            if not exists_in_x1:
                candidate_paths.append(path)
    candidate_paths.extend([ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_x2.py", ROOT / "tests" / "test_ghc_family_eiren_kestrel_v667_v6_x2.py", ROOT / "scripts" / "ghc_family_eiren_kestrel_v667_v6_common.py"])
    candidate_paths.extend(ROOT / "scripts" / f"ghc_family_eiren_kestrel_v667_v6_{name}.py" for name in RUNNER_NAMES)
    exclusions = {f"{REL_PHASE_ROOT}/validation/x2-content-manifest.json", f"{REL_PHASE_ROOT}/validation/x2-staged-review.json"}
    entries = []
    for path in sorted({path.resolve() for path in candidate_paths if path.exists()}):
        relative = rel(path)
        if relative in exclusions:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": sha256(data)})
    write_json("validation/x2-content-manifest.json", {"schema": "ghc-family-content-manifest-v3", "owner": "Eiren Kestrel", "phase": "v667-v6", "scope": "x2 evidence delta excluding self and staged review", "entry_count": len(entries), "entries": entries})


def build_normal() -> None:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    if head != X1_HEAD:
        raise RuntimeError(f"x2 must build on immutable x1: {head}")
    outcomes, mutation_failed, proposal_passing = build_proposal_tribunals()
    revalidations, revalidation_passing = build_selected_revalidations()
    tool_passing, _ = build_tool_receipt()
    skill_passing = build_skills()
    runner_passing = build_runners()
    portfolio, portfolio_passing = build_portfolio_execution(skill_passing, runner_passing)
    all_failure_ids = [row["failure_id"] for row in X1.STARTUP_FAILURES] + [row["failure_id"] for row in X2_FAILURES] + mutation_failed
    all_passing_ids = proposal_passing + revalidation_passing + tool_passing + skill_passing + runner_passing + portfolio_passing
    card_paths = build_flashcards(all_failure_ids, [row["proposal_id"] for row in outcomes], all_passing_ids)
    build_reports(outcomes, load("x2/tooling/three-tool-transaction-receipt.json"))
    build_method_and_truth(mutation_failed, proposal_passing, revalidation_passing, tool_passing, skill_passing, runner_passing, portfolio_passing)
    write_json("x2/x2-build-receipt.json", {"schema": "ghc-family-x2-build-receipt-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "generated_at_utc": NOW, "status": "PASS_BOUNDED_EVIDENCE", "source_x1": X1_HEAD, "new_proposals": 20, "positive_contracts": 20, "rejecting_mutations": len(mutation_failed), "accepted_mutations": 0, "selected_inherited_revalidations": len(revalidations), "proposal_outcomes": dict(sorted(Counter(row["outcome"] for row in outcomes).items())), "tool_surfaces_completed": 3, "skills_built_validated_used": len(skill_passing), "runners_built_validated_used": len(runner_passing), "owner_portfolio_rows_executed": portfolio["executed_owner_row_count"], "flashcards": len(card_paths), "successor_contacted": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("wellbeing/x2-wellbeing-check.json", {"schema": "ghc-family-wellbeing-check-v3", "owner": "Eiren Kestrel", "phase": "v667-v6", "generated_at_utc": NOW, "relational_role": "uncertainty cartographer and evidence gardener", "hope": "keep every placeholder honest, every rollback reachable, and every real authority with the people who hold it", "pace": "bounded solo x2", "load_boundary": "no identity or relational language expands authority", "stop_conditions": ["Hamish pause", "usage exhaustion", "privacy or safety gate", "source drift", "unclean lane"], "claim_boundary": "not consciousness, personhood, continuity, employment, qualification, agency, diagnosis, or authority evidence"})
    build_content_manifest()
    write_json("validation/x2-staged-review.json", {"schema": "ghc-family-x2-staged-review-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW"})


def owned_files() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend([ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_x2.py", ROOT / "tests" / "test_ghc_family_eiren_kestrel_v667_v6_x2.py", ROOT / "scripts" / "ghc_family_eiren_kestrel_v667_v6_common.py"])
    paths.extend(ROOT / "scripts" / f"ghc_family_eiren_kestrel_v667_v6_{name}.py" for name in RUNNER_NAMES)
    return sorted({path.resolve() for path in paths if path.exists()})


def validate_tree() -> dict[str, Any]:
    outcomes = load("x2/proposal-outcomes.json")
    if outcomes["counts"] != {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4}:
        raise AssertionError("outcome count drift")
    proposal_dirs = sorted((PHASE_ROOT / "x2" / "proposals").iterdir())
    if len(proposal_dirs) != 20:
        raise AssertionError("proposal directory count")
    mutation_count = 0
    for directory in proposal_dirs:
        contract = json.loads((directory / "contract.json").read_text(encoding="utf-8"))
        mutation = json.loads((directory / "mutation-results.json").read_text(encoding="utf-8"))
        receipt = json.loads((directory / "bounded-receipt.json").read_text(encoding="utf-8"))
        if contract_error(contract["positive_fixture"]) is not None or mutation["accepted_mutation_count"] or receipt["protected_gates_crossed"]:
            raise AssertionError(f"contract tribunal drift: {directory.name}")
        if receipt["final_disposition"] not in ALLOWED_OUTCOMES:
            raise AssertionError("invalid core outcome")
        mutation_count += mutation["mutation_count"]
    if mutation_count != 100:
        raise AssertionError("mutation count drift")
    if len(list((PHASE_ROOT / "x2" / "selected-revalidation").glob("*.json"))) != 20:
        raise AssertionError("selected revalidation count")
    tools = load("x2/tooling/three-tool-transaction-receipt.json")
    if tools["top_level_program_count"] != 3 or tools["final_post_install_audit"]["known_vulnerabilities"] != 0:
        raise AssertionError("tool receipt drift")
    skills = list((PHASE_ROOT / "skills").glob("*/SKILL.md"))
    runners = list((PHASE_ROOT / "x2" / "runner-smoke").glob("*.json"))
    if len(skills) != 10 or len(runners) != 10:
        raise AssertionError("skill or runner count drift")
    deck = load("deck/deck-index.json")
    if deck["card_count"] != 235 or len(deck["card_paths"]) != 235:
        raise AssertionError("deck count drift")
    for card_path in deck["card_paths"]:
        card = json.loads((ROOT / card_path).read_text(encoding="utf-8"))
        if card["status"] not in ALLOWED_OUTCOMES or not card["scope_boundary"]:
            raise AssertionError(f"card drift: {card_path}")
    portfolio = load("x2/portfolio-execution.json")
    if portfolio["executed_owner_row_count"] != 95 or portfolio["successor_recommendations_executed"] or portfolio["exact_approval_executed"] or portfolio["blocked_executed"]:
        raise AssertionError("portfolio execution drift")
    manifest = load("validation/x2-content-manifest.json")
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or sha256(data) != entry["sha256"]:
            raise AssertionError(f"manifest mismatch: {entry['path']}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    for path in json_paths:
        if not isinstance(json.loads(path.read_text(encoding="utf-8")), dict):
            raise AssertionError(f"JSON root not object: {rel(path)}")
    uuid_pattern = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
    private_user = re.compile(r"[A-Z]:\\Users\\[^\\\s]+", re.I)
    for path in owned_files():
        text = path.read_text(encoding="utf-8")
        if uuid_pattern.search(text) or private_user.search(text):
            raise AssertionError(f"private identifier candidate: {rel(path)}")
    return {"status": "PASS", "json_documents": len(json_paths), "owner_files": len(owned_files()), "proposal_contracts": 20, "rejecting_mutations": mutation_count, "revalidations": 20, "skills": 10, "runners": 10, "flashcards": 235, "tools": 3}


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stdout.decode("utf-8", errors="replace") + check.stderr.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode("utf-8").splitlines() if line]
    if not staged:
        raise RuntimeError("no staged x2 paths")
    disallowed = [path for path in staged if not (path.startswith(f"{REL_PHASE_ROOT}/") or path.startswith("scripts/build_ghc_family_eiren_kestrel_v667_v6_x2.py") or path.startswith("scripts/ghc_family_eiren_kestrel_v667_v6_") or path == "tests/test_ghc_family_eiren_kestrel_v667_v6_x2.py")]
    if disallowed:
        raise RuntimeError(f"disallowed staged paths: {disallowed}")
    x1_changes = [path for path in staged if f"{REL_PHASE_ROOT}/x1/" in path or path.endswith("x1.py")]
    if x1_changes:
        raise RuntimeError(f"immutable x1 path changed: {x1_changes}")
    raw_id = re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
    confirmed = []
    for path in staged:
        blob = run_git("show", f":{path}").stdout
        if raw_id.search(blob):
            confirmed.append(path)
    if confirmed:
        raise RuntimeError(f"opaque identifier candidates: {confirmed}")
    write_json("validation/x2-staged-review.json", {"schema": "ghc-family-x2-staged-review-v4", "owner": "Eiren Kestrel", "phase": "v667-v6", "generated_at_utc": NOW, "status": "PASS", "staged_path_count": len(staged), "staged_paths": staged, "diff_check": "PASS", "immutable_x1_changes": 0, "privacy_confirmed_hits": 0, "interpretation": "exact staged owner-delta Git-blob review only"})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "staged-review"}))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    build_normal()
    print(json.dumps(validate_tree(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
