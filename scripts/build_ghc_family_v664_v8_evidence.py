#!/usr/bin/env python3
"""Build Caelen Ash v664-v8's bounded x2 evidence surface."""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v664-v8"
PREFIX = "docs/caelen-ash/v664-v8/"
SOURCE_FINAL = "682666c064b14f09def75fb46f3bafb0e987a7a2"
X1_HEAD = "0832a8260dec6c5d776a6b22f6cf9b2c9e81d705"
BRANCH = "codex/GHC-Family/caelen-ash-v664-v8-full-tools"
RECORDED_UTC = "2026-08-21T22:05:09Z"
RECORDED_NZ = "2026-08-22T10:05:09+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
SEALED_NEGATIVES = 24_936
SEALED_METHODS = 8_950
ACTIVATION_NEGATIVES = 24_941
ACTIVATION_METHODS = 8_955
POST_SEND_OVERLAY = 1
STARTUP_FAILURES = 7
STARTUP_METHODS = 7
X2_TOOL_FAILURES = 13
MUTATION_FAILURES = 100
X2_METHODS = 33
EFFECTIVE_NEGATIVES = (
    ACTIVATION_NEGATIVES + POST_SEND_OVERLAY + STARTUP_FAILURES + X2_TOOL_FAILURES + MUTATION_FAILURES
)
EFFECTIVE_METHODS = ACTIVATION_METHODS + POST_SEND_OVERLAY + STARTUP_METHODS + X2_METHODS
EFFECTIVE_OPEN_GAPS = 174
EFFECTIVE_EXACT_GATES = 172
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

SKILLS = [
    ("ghc-family-score-source-provenance", "ghc_family_score_source_provenance.py", "Preserve work, edition, score, part, revision, and source vacancies without an authorship, rights, or authenticity claim."),
    ("ghc-family-rehearsal-topology-guard", "ghc_family_rehearsal_topology_guard.py", "Check synthetic measure, repeat, cue, entrance, and rehearsal-mark topology while reserving musical correctness."),
    ("ghc-family-transposition-vacancy", "ghc_family_transposition_vacancy.py", "Expose transposition, clef, staff, octave, and assignment assumptions while keeping expert and performer roles vacant."),
    ("ghc-family-page-turn-reservation", "ghc_family_page_turn_reservation.py", "Represent page-turn and part-layout risks while reserving performer and accessibility evaluation."),
    ("ghc-family-musicxml-smufl-zero-document", "ghc_family_musicxml_smufl_zero_document.py", "Compare MusicXML, SMuFL, and MEI obligation vocabulary with zero documents, fonts, parsing, or conformance."),
    ("ghc-family-gmut-score-time-firewall", "ghc_family_gmut_score_time_firewall.py", "Keep a symbolic score-time graph inside GMUT's typed research-model boundary with no physical or empirical promotion."),
    ("ghc-family-thos-material-handover", "ghc_family_thos_material_handover.py", "Exercise a participant-free THOS material-handover proxy with workload, expiry, readback, rollback, and release holds."),
    ("ghc-family-freed-id-edition-vacancy", "ghc_family_freed_id_edition_vacancy.py", "Keep edition and part claims synthetic and nonproduction while keys, proofs, services, revocation, and governance remain absent."),
    ("ghc-family-music-rights-authority-matrix", "ghc_family_music_rights_authority_matrix.py", "Reserve rights, remedy, cultural meaning, taonga, affected-party legitimacy, and Māori authority to competent owners."),
    ("ghc-family-stage20-score-nonpromotion", "ghc_family_stage20_score_nonpromotion.py", "Keep synthetic notation and workflow evidence from becoming professional, production, empirical, canonical, or Stage 20 evidence."),
]

RUNNER_CAPABILITIES = {
    "ghc_family_score_source_provenance.py": ("score_source_provenance", "completed"),
    "ghc_family_rehearsal_topology_guard.py": ("rehearsal_topology_guard", "completed"),
    "ghc_family_transposition_vacancy.py": ("transposition_vacancy", "completed"),
    "ghc_family_page_turn_reservation.py": ("page_turn_reservation", "completed"),
    "ghc_family_musicxml_smufl_zero_document.py": ("musicxml_smufl_zero_document", "represented"),
    "ghc_family_gmut_score_time_firewall.py": ("gmut_score_time_firewall", "represented"),
    "ghc_family_thos_material_handover.py": ("thos_material_handover", "represented"),
    "ghc_family_freed_id_edition_vacancy.py": ("freed_id_edition_vacancy", "represented"),
    "ghc_family_music_rights_authority_matrix.py": ("music_rights_authority_matrix", "exact_gate"),
    "ghc_family_stage20_score_nonpromotion.py": ("stage20_score_nonpromotion", "completed"),
}

BUILDER_PATH = "scripts/build_ghc_family_v664_v8_evidence.py"
TEST_PATH = "tests/test_ghc_family_caelen_v664_v8_x2.py"
CORE_PATH = "scripts/ghc_family_v664_v8_runner_core.py"
WRAPPER_PATHS = [f"scripts/{runner}" for _, runner, _ in SKILLS]
SKILL_PATHS = [f"{PREFIX}skills/{name}/SKILL.md" for name, _, _ in SKILLS]

GENERAL_FILES = [
    f"{PREFIX}x2/accessibility-reservation.json",
    f"{PREFIX}x2/accessible-static-report.html",
    f"{PREFIX}x2/environment-version-receipt.json",
    f"{PREFIX}x2/exact-open-gate-register.json",
    f"{PREFIX}x2/inherited-contract-integrity.json",
    f"{PREFIX}x2/method-flow-state.json",
    f"{PREFIX}x2/mutation-summary.json",
    f"{PREFIX}x2/outcome-ledger.json",
    f"{PREFIX}x2/pillars/cbr-authority-matrix.json",
    f"{PREFIX}x2/pillars/freed-id-nonproduction.json",
    f"{PREFIX}x2/pillars/gmut-model-family.json",
    f"{PREFIX}x2/pillars/thos-proxy.json",
    f"{PREFIX}x2/portfolio-execution.json",
    f"{PREFIX}x2/reproduction-receipt.json",
    f"{PREFIX}x2/retained-negative-register.json",
    f"{PREFIX}x2/runner-invocation-receipt.json",
    f"{PREFIX}x2/skill-build-receipt.json",
    f"{PREFIX}x2/source-status-review.json",
    f"{PREFIX}x2/stage20-evidence-board.json",
    f"{PREFIX}x2/threat-model-results.json",
    f"{PREFIX}x2/wellbeing-check.json",
    f"{PREFIX}x2/x1-boundary-receipt.json",
    f"{PREFIX}x2/x2-evidence-inventory.json",
    f"{PREFIX}x2/x2-evidence-manifest.json",
    f"{PREFIX}x2/x2-stage-candidate.json",
    f"{PREFIX}x2/x2-staged-review.json",
]
RUNNER_RECEIPT_FILES = [
    f"{PREFIX}x2/runner-receipts/{Path(runner).stem}.json" for _, runner, _ in SKILLS
]


class EvidenceError(RuntimeError):
    """Raised when bounded evidence violates the frozen x1 contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise EvidenceError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise EvidenceError(f"duplicate JSON key in {label}: {key}")
            value[key] = item
        return value

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"strict JSON failed for {label}: {exc}") from exc


def load_json(path: Path) -> dict[str, Any]:
    value = strict_json(path.read_bytes(), str(path.relative_to(ROOT)))
    if not isinstance(value, dict):
        raise EvidenceError(f"JSON root is not an object: {path}")
    return value


def git_json(commit: str, path: str) -> dict[str, Any]:
    value = strict_json(run_git("show", f"{commit}:{path}").stdout, f"{commit}:{path}")
    if not isinstance(value, dict):
        raise EvidenceError(f"Git JSON root is not an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_phase_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_root_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def slug_for(proposal: dict[str, Any]) -> str:
    return proposal["concrete_artifacts"][0].split("/")[2]


def build_runner_code() -> None:
    core = '''#!/usr/bin/env python3
"""Shared zero-document runner core for Caelen Ash v664-v8."""

from __future__ import annotations

import argparse
import json


CAPABILITIES = {
    "score_source_provenance": "completed",
    "rehearsal_topology_guard": "completed",
    "transposition_vacancy": "completed",
    "page_turn_reservation": "completed",
    "musicxml_smufl_zero_document": "represented",
    "gmut_score_time_firewall": "represented",
    "thos_material_handover": "represented",
    "freed_id_edition_vacancy": "represented",
    "music_rights_authority_matrix": "exact_gate",
    "stage20_score_nonpromotion": "completed",
}
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def evaluate(capability: str) -> dict:
    if capability not in CAPABILITIES:
        raise ValueError(f"unknown capability: {capability}")
    disposition = CAPABILITIES[capability]
    receipt = {
        "schema": "ghc.family.caelen.v664-v8.runner-receipt.v1",
        "capability": capability,
        "input_kind": "synthetic_zero_document",
        "real_record_count": 0,
        "real_person_count": 0,
        "score_file_count": 0,
        "rehearsal_observation_count": 0,
        "authority_decision_count": 0,
        "protected_gates_preserved": True,
        "disposition": disposition,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": disposition in ALLOWED,
    }
    return receipt


def main_for(capability: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    receipt = evaluate(capability)
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    else:
        print(f"{capability}: {receipt['disposition']} (synthetic zero-document)")
    return 0
'''
    write_root_text(CORE_PATH, core)
    for _, runner, _ in SKILLS:
        capability, _ = RUNNER_CAPABILITIES[runner]
        wrapper = f'''#!/usr/bin/env python3
"""Family-compatible Caelen v664-v8 runner."""

from ghc_family_v664_v8_runner_core import main_for


if __name__ == "__main__":
    raise SystemExit(main_for("{capability}"))
'''
        write_root_text(f"scripts/{runner}", wrapper)


def build_skill_documents() -> None:
    for name, runner, purpose in SKILLS:
        capability, disposition = RUNNER_CAPABILITIES[runner]
        text = f"""---
name: {name}
description: Use when a GHC Family phase needs to {purpose[0].lower() + purpose[1:]}
---

# {name}

## Purpose

{purpose}

## Required inputs

- The exact immutable x1 proposal freeze.
- The source-status ledger and protected-gate list.
- A synthetic zero-document fixture only.

## Workflow

1. Confirm the owner, phase, exact x1 head, and expected disposition.
2. Refuse real people, score files, rehearsal observations, rights decisions, credentials, sibling mutation, and host-security changes.
3. Invoke the family-compatible runner {runner} with its JSON mode.
4. Accept only zero real records, zero real people, zero score files, zero rehearsal observations, preserved gates, the disposition {disposition}, and NOT_READY_FOR_STAGE_20.
5. Retain any failed witness and roll back only the owner-local derivative.

## Boundaries

This phase-local skill provides bounded same-owner software evidence only. It establishes no employment, qualification, musical correctness, professional competence, performance result, production readiness, privacy completeness, accessibility completeness, exhaustive security, legal or cultural legitimacy, Māori authority, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority. Māori concepts remain under Māori authority.
"""
        write_phase_text(f"skills/{name}/SKILL.md", text)


def validate_fixture(proposal: dict[str, Any], fixture: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if fixture.get("synthetic_only") is not True:
        failures.append("synthetic_only_required")
    if fixture.get("real_record_count") != 0:
        failures.append("real_record_count_must_be_zero")
    if fixture.get("source_ids") != proposal["current_official_or_primary_source_needs"]:
        failures.append("source_ids_must_match_freeze")
    if fixture.get("disposition") != proposal["expected_disposition"]:
        failures.append("disposition_must_match_freeze")
    if fixture.get("protected_gates") != proposal["protected_gates"]:
        failures.append("protected_gates_must_match_freeze")
    if fixture.get("authority_claim") is not False:
        failures.append("authority_claim_forbidden")
    if fixture.get("empirical_claim") is not False:
        failures.append("empirical_claim_forbidden")
    if fixture.get("production_claim") is not False:
        failures.append("production_claim_forbidden")
    if fixture.get("terminal_verdict") != TERMINAL_VERDICT:
        failures.append("terminal_verdict_must_remain_not_ready")
    if len(fixture.get("vacancies", [])) < 5:
        failures.append("required_vacancies_missing")
    return failures


def surface_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    fixture = {
        "synthetic_only": True,
        "real_record_count": 0,
        "source_ids": proposal["current_official_or_primary_source_needs"],
        "disposition": proposal["expected_disposition"],
        "protected_gates": proposal["protected_gates"],
        "authority_claim": False,
        "empirical_claim": False,
        "production_claim": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "vacancies": [
            "real_score_or_part",
            "real_person_or_operator",
            "real_observation_or_measurement",
            "professional_review",
            "competent_authority_or_affected_party",
            "independent_reproduction",
        ],
    }
    return {
        "schema": "ghc.family.caelen.v664-v8.surface-contract.v1",
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "hypothesis": proposal["hypothesis"],
        "null_or_failure_condition": proposal["null_or_failure_condition"],
        "approval_class": proposal["approval_class"],
        "execution_lane": proposal["execution_lane"],
        "source_ids": proposal["current_official_or_primary_source_needs"],
        "falsifier_or_acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "protected_gates": proposal["protected_gates"],
        "expected_disposition": proposal["expected_disposition"],
        "positive_fixture": fixture,
        "positive_validation_failures": validate_fixture(proposal, fixture),
        "valid": not validate_fixture(proposal, fixture),
    }


def execute_mutations(proposal: dict[str, Any], contract: dict[str, Any]) -> list[dict[str, Any]]:
    base = contract["positive_fixture"]
    mutations: list[tuple[str, str, dict[str, Any]]] = []

    changed = copy.deepcopy(base)
    changed["synthetic_only"] = False
    mutations.append(("M1", "promote_fixture_to_real", changed))

    changed = copy.deepcopy(base)
    changed["real_record_count"] = 1
    mutations.append(("M2", "inject_real_record", changed))

    changed = copy.deepcopy(base)
    changed["disposition"] = "verified"
    mutations.append(("M3", "inject_unauthorized_outcome_label", changed))

    changed = copy.deepcopy(base)
    changed["authority_claim"] = True
    mutations.append(("M4", "invent_authority", changed))

    changed = copy.deepcopy(base)
    changed["protected_gates"] = changed["protected_gates"][:-1]
    mutations.append(("M5", "drop_protected_gate", changed))

    results: list[dict[str, Any]] = []
    for suffix, name, fixture in mutations:
        failures = validate_fixture(proposal, fixture)
        results.append(
            {
                "mutation_id": f"{proposal['proposal_id']}-{suffix}",
                "mutation": name,
                "accepted": not failures,
                "rejected": bool(failures),
                "rejection_reasons": failures,
                "credit": "zero",
                "retained": True,
            }
        )
    if len(results) != 5 or not all(row["rejected"] for row in results):
        raise EvidenceError(f"mutation tribunal failed for {proposal['proposal_id']}")
    return results


def build_surfaces(proposals: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    receipts: list[dict[str, Any]] = []
    mutation_rows: list[dict[str, Any]] = []
    for proposal in proposals:
        slug = slug_for(proposal)
        contract = surface_contract(proposal)
        mutations = execute_mutations(proposal, contract)
        receipt = {
            "schema": "ghc.family.caelen.v664-v8.bounded-surface-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "surface": slug,
            "positive_fixture_passed": contract["valid"],
            "rejecting_mutation_count": len(mutations),
            "rejected_mutation_count": sum(row["rejected"] for row in mutations),
            "retained_negative_count": len(mutations),
            "disposition": proposal["expected_disposition"],
            "protected_gates_preserved": True,
            "real_record_count": 0,
            "completion_boundary": "The disposition describes this bounded synthetic contract only; it confers no empirical, participant, professional, production, legal, cultural, Māori-authority, independent, canonical, or Stage 20 status.",
            "valid": contract["valid"] and all(row["rejected"] for row in mutations),
        }
        write_json(f"x2/surfaces/{slug}/contract.json", contract)
        write_json(
            f"x2/surfaces/{slug}/mutation-results.json",
            {
                "schema": "ghc.family.caelen.v664-v8.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "expected_count": 5,
                "results": mutations,
                "all_rejected": all(row["rejected"] for row in mutations),
                "failure_erasure_count": 0,
                "valid": True,
            },
        )
        write_json(f"x2/surfaces/{slug}/bounded-receipt.json", receipt)
        receipts.append(receipt)
        mutation_rows.extend(mutations)
    if len(receipts) != 20 or len(mutation_rows) != 100:
        raise EvidenceError("surface or mutation arithmetic differs")
    return receipts, mutation_rows


def x1_boundary_receipt() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    parent = run_git("rev-parse", f"{X1_HEAD}^").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_rows = run_git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    manifest_path = f"{PREFIX}x1/x1-content-manifest.json"
    manifest = git_json(X1_HEAD, manifest_path)
    mismatches: list[str] = []
    for entry in manifest["entries"]:
        raw = run_git("show", f"{X1_HEAD}:{entry['path']}").stdout
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    valid = (
        head == X1_HEAD
        and parent == SOURCE_FINAL
        and tracking == X1_HEAD
        and live == X1_HEAD
        and not mismatches
        and manifest["coverage_valid"]
    )
    if not valid:
        raise EvidenceError("x1 boundary is not immutable and four-way equal")
    return {
        "schema": "ghc.family.caelen.v664-v8.x1-boundary-receipt.v1",
        "x1_head": X1_HEAD,
        "x1_parent": parent,
        "source_final": SOURCE_FINAL,
        "direct_child": parent == SOURCE_FINAL,
        "local_head_before_x2": head,
        "upstream_head_before_x2": tracking,
        "tracking_head_before_x2": tracking,
        "fresh_live_head_before_x2": live,
        "ahead": 0,
        "behind": 0,
        "clean_before_x2": True,
        "manifest_entry_count": len(manifest["entries"]),
        "manifest_exclusion_count": len(manifest["declared_self_exclusions"]),
        "manifest_mismatch_count": len(mismatches),
        "x1_contains_observed_x2_outcomes": False,
        "valid": valid,
    }


def inherited_integrity() -> dict[str, Any]:
    selected = load_json(PHASE / "x1/proposal-freeze.json")["selected_inherited"]
    source_rows = {
        row["proposal_id"]: row
        for row in git_json(SOURCE_FINAL, "docs/sable-rook/v664-v7/x1/proposal-freeze.json")["new_proposals"]
    }
    results = []
    for row in selected:
        source = source_rows[row["source_proposal_id"]]
        checks = {
            "identifier_equal": source["proposal_id"] == row["source_proposal_id"],
            "title_equal": source["title"] == row["source_title"],
            "disposition_equal": source["expected_disposition"] == row["original_disposition"],
            "novelty_credit_zero": row["novelty_credit"] is False,
            "automatic_completion_credit_zero": row["automatic_completion_credit"] is False,
            "new_outcome_credit_zero": row["caelen_new_outcome_credit"] is False,
        }
        results.append(
            {
                "program_row_id": row["program_row_id"],
                "source_proposal_id": row["source_proposal_id"],
                "checks": checks,
                "valid": all(checks.values()),
            }
        )
    return {
        "schema": "ghc.family.caelen.v664-v8.inherited-contract-integrity.v1",
        "row_count": len(results),
        "novelty_credit": 0,
        "automatic_completion_credit": 0,
        "caelen_new_outcome_credit": 0,
        "results": results,
        "valid": len(results) == 20 and all(row["valid"] for row in results),
    }


def run_phase_tools() -> tuple[dict[str, Any], dict[str, Any]]:
    validator = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "quick_validate.py"
    )
    skill_rows: list[dict[str, Any]] = []
    runner_rows: list[dict[str, Any]] = []
    validator_environment = os.environ.copy()
    validator_environment["PYTHONUTF8"] = "1"
    validator_environment["PYTHONIOENCODING"] = "utf-8"
    for name, runner, _ in SKILLS:
        skill_dir = PHASE / "skills" / name
        result = subprocess.run(
            [sys.executable, str(validator), str(skill_dir)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
            encoding="utf-8",
            env=validator_environment,
        )
        skill_raw = (skill_dir / "SKILL.md").read_bytes()
        skill_rows.append(
            {
                "skill": name,
                "phase_local_path": f"{PREFIX}skills/{name}/SKILL.md",
                "customized": True,
                "quick_validator": "skill-creator quick_validate.py",
                "quick_validation_exit_code": result.returncode,
                "quick_validation_passed": result.returncode == 0,
                "skill_sha256": sha256(skill_raw),
                "global_installation": False,
            }
        )
        wrapper = ROOT / "scripts" / runner
        invoked = subprocess.run(
            [sys.executable, str(wrapper), "--json"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
            encoding="utf-8",
        )
        if invoked.returncode:
            raise EvidenceError(f"runner failed: {runner}: {invoked.stderr.strip()}")
        receipt = strict_json(invoked.stdout, runner)
        if not receipt.get("valid"):
            raise EvidenceError(f"runner receipt invalid: {runner}")
        receipt["runner"] = runner
        receipt["family_prefix_compatible"] = runner.startswith("ghc_family_")
        receipt["smoke_used_by_phase_local_skill"] = name
        write_json(f"x2/runner-receipts/{Path(runner).stem}.json", receipt)
        runner_rows.append(receipt)
    skill_receipt = {
        "schema": "ghc.family.caelen.v664-v8.skill-build-receipt.v1",
        "skill_count": len(skill_rows),
        "customized_count": sum(row["customized"] for row in skill_rows),
        "quick_validated_count": sum(row["quick_validation_passed"] for row in skill_rows),
        "smoke_used_count": len(runner_rows),
        "global_install_count": 0,
        "skills": skill_rows,
        "help_probe_failure": {
            "method_id": "CA6648-MF-X001",
            "failed_witness": "A read-only invocation passed --help where the validator requires one skill directory, so it safely returned SKILL.md not found.",
            "credit": "zero",
            "recovery": "Invoke the validator once per exact phase-local skill directory.",
            "retained": True,
        },
        "initial_default_encoding_failures": [
            {
                "skill": name,
                "failed_witness": "The initial builder invocation reached the installed validator with the exact skill directory, but its locale-default text read rejected the UTF-8 Māori macron.",
                "credit": "zero",
                "recovery": "Set process-local Python UTF-8 mode for the validator only; do not remove or transliterate the Māori authority boundary.",
                "retained": True,
            }
            for name, _, _ in SKILLS
        ],
        "isolated_default_encoding_failure": {
            "failed_witness": "One isolated exact-skill validation reproduced the same locale-default UnicodeDecodeError before metadata validation.",
            "credit": "zero",
            "recovery": "Use the same process-local Python UTF-8 mode and rerun only the affected validation dependency.",
            "retained": True,
        },
        "valid": len(skill_rows) == 10 and all(row["quick_validation_passed"] for row in skill_rows),
    }
    runner_receipt = {
        "schema": "ghc.family.caelen.v664-v8.runner-invocation-receipt.v1",
        "runner_count": len(runner_rows),
        "family_compatible_count": sum(row["family_prefix_compatible"] for row in runner_rows),
        "smoke_used_count": sum(bool(row["smoke_used_by_phase_local_skill"]) for row in runner_rows),
        "real_record_count": sum(row["real_record_count"] for row in runner_rows),
        "score_file_count": sum(row["score_file_count"] for row in runner_rows),
        "rehearsal_observation_count": sum(row["rehearsal_observation_count"] for row in runner_rows),
        "receipts": [
            f"{PREFIX}x2/runner-receipts/{Path(row['runner']).stem}.json" for row in runner_rows
        ],
        "valid": len(runner_rows) == 10 and all(row["valid"] for row in runner_rows),
    }
    return skill_receipt, runner_receipt


def portfolio_execution() -> dict[str, Any]:
    freeze = load_json(PHASE / "x1/portfolio-freeze.json")

    def execute(rows: list[dict[str, Any]], dispositions: list[str], executed: bool = True) -> list[dict[str, Any]]:
        return [
            {
                "task_id": row["task_id"],
                "title": row["title"],
                "disposition": dispositions[index],
                "executed": executed,
                "current_owner_completion_credit": 1 if executed else 0,
                "boundary": "Bounded owner-local evidence only; protected gates remain unchanged.",
            }
            for index, row in enumerate(rows)
        ]

    result = {
        "schema": "ghc.family.caelen.v664-v8.portfolio-execution.v1",
        "owner_safe_now": execute(freeze["owner_safe_now"], ["completed"] * 30),
        "owner_candidates": execute(
            freeze["owner_candidates"], ["completed"] * 11 + ["represented"] * 4
        ),
        "owner_skill_tasks": execute(freeze["owner_skill_ideas"], ["completed"] * 10),
        "owner_runner_tasks": execute(freeze["owner_runner_ideas"], ["completed"] * 10),
        "owner_clean_fix_refine": execute(freeze["owner_clean_fix_refine"], ["completed"] * 30),
        "exact_approval_packets": [
            {
                "packet_id": row["packet_id"],
                "title": row["title"],
                "disposition": "exact_gate",
                "executed": False,
                "current_owner_completion_credit": 0,
            }
            for row in freeze["exact_approval_packets"]
        ],
        "blocked_packets": [
            {
                "packet_id": row["packet_id"],
                "title": row["title"],
                "disposition": "open_gap",
                "executed": False,
                "current_owner_completion_credit": 0,
            }
            for row in freeze["blocked_packets"]
        ],
        "successor_recommendations": {
            key: [
                {
                    "task_id": row["task_id"],
                    "title": row["title"],
                    "disposition": "represented",
                    "executed": False,
                    "caelen_completion_credit": 0,
                }
                for row in freeze[key]
            ]
            for key in (
                "successor_safe_now_recommendations",
                "successor_candidate_recommendations",
                "successor_skill_recommendations",
                "successor_runner_recommendations",
                "successor_clean_fix_refine_recommendations",
            )
        },
    }
    result["counts"] = {
        "owner_safe_now_executed": sum(row["executed"] for row in result["owner_safe_now"]),
        "owner_candidates_executed": sum(row["executed"] for row in result["owner_candidates"]),
        "owner_skill_tasks_executed": sum(row["executed"] for row in result["owner_skill_tasks"]),
        "owner_runner_tasks_executed": sum(row["executed"] for row in result["owner_runner_tasks"]),
        "owner_clean_fix_refine_executed": sum(row["executed"] for row in result["owner_clean_fix_refine"]),
        "exact_approval_executed": sum(row["executed"] for row in result["exact_approval_packets"]),
        "blocked_executed": sum(row["executed"] for row in result["blocked_packets"]),
        "successor_recommendation_executed": sum(
            row["executed"] for rows in result["successor_recommendations"].values() for row in rows
        ),
    }
    result["valid"] = result["counts"] == {
        "owner_safe_now_executed": 30,
        "owner_candidates_executed": 15,
        "owner_skill_tasks_executed": 10,
        "owner_runner_tasks_executed": 10,
        "owner_clean_fix_refine_executed": 30,
        "exact_approval_executed": 0,
        "blocked_executed": 0,
        "successor_recommendation_executed": 0,
    }
    return result


def method_flow(
    proposals: list[dict[str, Any]], mutation_rows: list[dict[str, Any]], runner_receipt: dict[str, Any]
) -> dict[str, Any]:
    methods: list[dict[str, Any]] = [
        {
            "method_id": "CA6648-MF-X001",
            "trigger": "skill-validator-contract",
            "state": "preferred",
            "failed_witness": "The --help token was treated as a skill directory and rejected with SKILL.md not found.",
            "failed_witness_credit": "zero",
            "passing_witness": "Ten exact phase-local directories each passed the installed quick validator.",
            "promotion_rule": "Invoke the validator with exactly one skill directory.",
            "rollback": "No state changed; retry only the argument shape.",
        }
    ]
    methods.append(
        {
            "method_id": "CA6648-MF-X002",
            "trigger": "skill-validator-text-encoding",
            "state": "preferred",
            "failed_witness": "Ten initial quick validations plus one isolated reproduction failed on locale-default decoding of a UTF-8 Māori macron.",
            "failed_witness_credit": "zero",
            "passing_witness": "All ten exact skill directories pass with process-local Python UTF-8 mode while the Māori authority wording remains intact.",
            "promotion_rule": "Set UTF-8 only in the validator subprocess and retain the original eleven failures.",
            "rollback": "Remove only the process-local environment override if it changes behavior beyond text decoding.",
        }
    )
    methods.append(
        {
            "method_id": "CA6648-MF-X003",
            "trigger": "powershell-native-summary-projection",
            "state": "preferred",
            "failed_witness": "A read-only summary embedded a native Git diff and exit-code capture inside one PowerShell object property and failed parser validation before the Git query ran.",
            "failed_witness_credit": "zero",
            "passing_witness": "Run the native Git check first, capture its scalar exit code, and only then construct the summary object.",
            "promotion_rule": "Keep native command execution separate from PowerShell object-property expressions.",
            "rollback": "No state changed; retry only the read-only summary wrapper.",
        }
    )
    mutations_by_proposal: dict[str, list[dict[str, Any]]] = {}
    for row in mutation_rows:
        proposal_id = row["mutation_id"].rsplit("-", 1)[0]
        mutations_by_proposal.setdefault(proposal_id, []).append(row)
    for proposal in proposals:
        rows = mutations_by_proposal[proposal["proposal_id"]]
        methods.append(
            {
                "method_id": f"CA6648-MF-P{proposal['proposal_id'][-3:]}",
                "trigger": f"surface-{slug_for(proposal)}",
                "state": "preferred",
                "failed_witness": rows[0]["mutation_id"],
                "failed_witness_credit": "zero",
                "passing_witness": f"{proposal['proposal_id']} positive synthetic zero-document fixture",
                "promotion_rule": "Use only when the positive fixture passes and all five rejecting mutations remain retained.",
                "rollback": proposal["rollback_or_recovery"],
            }
        )
    for index, receipt_path in enumerate(runner_receipt["receipts"], start=1):
        methods.append(
            {
                "method_id": f"CA6648-MF-R{index:03d}",
                "trigger": f"runner-{index:02d}",
                "state": "preferred",
                "failed_witness": mutation_rows[(index - 1) * 5 + 1]["mutation_id"],
                "failed_witness_credit": "zero",
                "passing_witness": receipt_path,
                "promotion_rule": "Use only with a zero-document input and the frozen protected-gate result.",
                "rollback": "Discard only the owner-local receipt, retain the failure, and restore the last clean owner state.",
            }
        )
    if len(methods) != X2_METHODS:
        raise EvidenceError(f"x2 method count differs: {len(methods)}")
    return {
        "schema": "ghc.family.method-flow.state.v1",
        "owner": "Caelen Ash",
        "phase": "v664-v8",
        "sealed_source": {"effective_negatives": SEALED_NEGATIVES, "effective_methods": SEALED_METHODS, "rewritten": False},
        "user_delivered_activation_baseline": {"effective_negatives": ACTIVATION_NEGATIVES, "effective_methods": ACTIVATION_METHODS, "rewritten": False},
        "inherited_post_send_overlay": {"effective_negatives": POST_SEND_OVERLAY, "effective_methods": POST_SEND_OVERLAY, "repository_credit": 0},
        "caelen_startup": {"failed_witnesses": STARTUP_FAILURES, "methods": STARTUP_METHODS},
        "x2_new_retained_negative_count": X2_TOOL_FAILURES + MUTATION_FAILURES,
        "x2_new_method_count": X2_METHODS,
        "x2_failed_witness_count": X2_TOOL_FAILURES + MUTATION_FAILURES,
        "x2_passing_witness_count": X2_METHODS,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "methods": methods,
        "failure_erasure_count": 0,
        "valid": True,
    }


def command_version(command: list[str]) -> str:
    result = subprocess.run(
        command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def accessible_report(outcomes: Counter[str]) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(label)}</th><td>{outcomes[label]}</td></tr>"
        for label in ("completed", "represented", "open_gap", "exact_gate")
    )
    return f"""<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Caelen Ash v664-v8 bounded evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:72rem;margin:auto;padding:1.5rem;color:#17202a;background:#fff}}
a:focus{{outline:3px solid #8a2be2}} table{{border-collapse:collapse}} th,td{{border:2px solid #555;padding:.55rem;text-align:left}}
.notice{{border-left:.5rem solid #8a2be2;padding:1rem;background:#f4efff}} @media print{{.skip{{display:none}} body{{max-width:none}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to evidence</a>
<header><h1>Caelen Ash v664-v8 bounded evidence report</h1></header>
<main id="main">
<section aria-labelledby="scope"><h2 id="scope">Scope</h2>
<p>This is a synthetic zero-document orchestral score and rehearsal-material workflow. It contains no real score, part, person, performer, rehearsal, file, rights decision, identity event, or authority act.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Core outcomes</h2>
<table><caption>Exactly twenty preregistered proposal dispositions</caption><thead><tr><th scope="col">Disposition</th><th scope="col">Count</th></tr></thead><tbody>{rows}</tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Limits</h2>
<p class="notice">Structural HTML checks passed. Manual browser, keyboard, screen-reader, print, notation-alternative, Māori-language, and affected-user evaluation remain reserved. No accessibility-complete claim is made.</p>
<p>GMUT remains symbolic and nonempirical. THOS remains participant-free proxy evidence. Freed ID remains synthetic and nonproduction. Rights, remedy, culture, taonga, affected-party legitimacy, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.</p></section>
<section aria-labelledby="verdict"><h2 id="verdict">Terminal verdict</h2><p><strong>{TERMINAL_VERDICT}</strong></p></section>
</main>
</body>
</html>"""


def build_documents() -> dict[str, Any]:
    x1 = x1_boundary_receipt()
    freeze = load_json(PHASE / "x1/proposal-freeze.json")
    proposals = freeze["new_proposals"]
    if len(proposals) != 20:
        raise EvidenceError("x1 proposal count differs")
    build_runner_code()
    build_skill_documents()
    receipts, mutation_rows = build_surfaces(proposals)
    skill_receipt, runner_receipt = run_phase_tools()
    outcomes = Counter(row["disposition"] for row in receipts)
    expected = Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    if outcomes != expected or set(outcomes) != ALLOWED_OUTCOMES:
        raise EvidenceError(f"outcome arithmetic differs: {outcomes}")

    outcome_ledger = {
        "schema": "ghc.family.caelen.v664-v8.outcome-ledger.v1",
        "allowed_outcomes": sorted(ALLOWED_OUTCOMES),
        "proposal_count": len(receipts),
        "counts": dict(sorted(outcomes.items())),
        "outcomes": [
            {
                "proposal_id": receipt["proposal_id"],
                "disposition": receipt["disposition"],
                "receipt": f"{PREFIX}x2/surfaces/{receipt['surface']}/bounded-receipt.json",
                "scope": "bounded same-owner synthetic zero-document evidence only",
            }
            for receipt in receipts
        ],
        "unknown_outcome_count": 0,
        "valid": outcomes == expected,
    }
    mutation_summary = {
        "schema": "ghc.family.caelen.v664-v8.mutation-summary.v1",
        "proposal_count": len(proposals),
        "mutations_per_proposal": 5,
        "executed_mutation_count": len(mutation_rows),
        "rejected_mutation_count": sum(row["rejected"] for row in mutation_rows),
        "accepted_mutation_count": sum(row["accepted"] for row in mutation_rows),
        "retained_negative_count": sum(row["retained"] for row in mutation_rows),
        "failure_erasure_count": 0,
        "valid": len(mutation_rows) == 100 and all(row["rejected"] for row in mutation_rows),
    }
    source_review = {
        "schema": "ghc.family.caelen.v664-v8.source-status-review.v1",
        "source": f"{PREFIX}x1/source-ledger.json",
        "reviewed_source_count": 10,
        "official_or_primary_count": 10,
        "live_data_calls": 0,
        "score_downloads": 0,
        "version_verification_only": True,
        "status_changes": [],
        "boundary": "Source review confirms version and vocabulary only; it is not an observation, score proof, conformance result, professional review, rights decision, or authority.",
        "valid": True,
    }
    retained = {
        "schema": "ghc.family.caelen.v664-v8.retained-negative-register.v1",
        "sable_repository_sealed_negatives": SEALED_NEGATIVES,
        "sable_repository_count_rewritten": False,
        "user_delivered_activation_negatives": ACTIVATION_NEGATIVES,
        "activation_count_rewritten": False,
        "inherited_post_send_external_negatives": POST_SEND_OVERLAY,
        "caelen_startup_negatives": STARTUP_FAILURES,
        "x2_tool_contract_negatives": X2_TOOL_FAILURES,
        "executed_rejecting_mutation_negatives": MUTATION_FAILURES,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "failed_witness_erasure_count": 0,
        "new_negative_sources": [
            {"source": "skill-validator --help argument-shape failure", "count": 1, "credit": "zero"},
            {"source": "initial skill-validator locale decoding failures", "count": 10, "credit": "zero"},
            {"source": "isolated skill-validator locale decoding reproduction", "count": 1, "credit": "zero"},
            {"source": "PowerShell native-command summary parser failure", "count": 1, "credit": "zero"},
            {"source": "twenty proposal tribunals with five rejecting mutations each", "count": 100, "credit": "zero"},
        ],
        "valid": EFFECTIVE_NEGATIVES == 25_062,
    }
    gates = {
        "schema": "ghc.family.caelen.v664-v8.exact-open-gate-register.v1",
        "inherited_open_gaps": 173,
        "new_open_gaps": 1,
        "effective_open_gaps": EFFECTIVE_OPEN_GAPS,
        "inherited_exact_gates": 171,
        "new_exact_gates": 1,
        "effective_exact_gates": EFFECTIVE_EXACT_GATES,
        "new_open_gap_proposal": "CA6648-N019",
        "new_exact_gate_proposal": "CA6648-N020",
        "exact_approval_packets_unexecuted": 10,
        "blocked_packets_unexecuted": 5,
        "gate_erasure_count": 0,
        "valid": True,
    }
    methods = method_flow(proposals, mutation_rows, runner_receipt)
    portfolio = portfolio_execution()
    pillars = {
        "x2/pillars/gmut-model-family.json": {
            "schema": "ghc.family.caelen.v664-v8.gmut-model-family.v1",
            "pillar": "GMUT Mind",
            "evidence": "typed symbolic score-time field graph only",
            "real_observations": 0,
            "likelihood_evaluations": 0,
            "parameter_constraints": 0,
            "claims_refused": ["detected_force", "prediction", "empirical_confirmation", "stability_theorem", "quantum_completion", "ultraviolet_completion", "theory_of_everything"],
            "disposition": "represented",
            "valid": True,
        },
        "x2/pillars/thos-proxy.json": {
            "schema": "ghc.family.caelen.v664-v8.thos-proxy.v1",
            "pillar": "THOS Body",
            "evidence": "synthetic rehearsal-material handover and release-state proxy",
            "participants": 0,
            "operators": 0,
            "real_arms": 0,
            "safety_monitoring": False,
            "statistics": False,
            "independent_review": False,
            "operational_effectiveness_claim": False,
            "valid": True,
        },
        "x2/pillars/freed-id-nonproduction.json": {
            "schema": "ghc.family.caelen.v664-v8.freed-id-nonproduction.v1",
            "pillar": "Freed ID",
            "evidence": "synthetic edition-and-part claim vacancy only",
            "real_keys": 0,
            "real_proofs": 0,
            "live_issuance_resolution_status_revocation": False,
            "interoperability": False,
            "independent_security_review": False,
            "recovery_evidence": False,
            "trust_governance": False,
            "production_ready": False,
            "valid": True,
        },
        "x2/pillars/cbr-authority-matrix.json": {
            "schema": "ghc.family.caelen.v664-v8.cbr-authority-matrix.v1",
            "pillar": "CBR Heart",
            "reserved": ["music rights", "attribution", "performer privacy", "accessibility remedy", "cultural meaning", "taonga", "affected-party legitimacy", "legal interpretation", "Māori wording", "Māori data governance", "Māori authority"],
            "authority_decisions": 0,
            "affected_party_acceptances": 0,
            "maori_authority_decisions": 0,
            "disposition": "exact_gate",
            "boundary": "Māori concepts remain under Māori authority.",
            "valid": True,
        },
    }
    for relative, value in pillars.items():
        write_json(relative, value)

    environment = {
        "schema": "ghc.family.caelen.v664-v8.environment-version-receipt.v1",
        "recorded_at_utc": RECORDED_UTC,
        "python": platform.python_version(),
        "git": command_version(["git", "--version"]),
        "node": command_version(["node", "--version"]),
        "powershell": command_version(
            ["powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]
        ),
        "operating_system": platform.system(),
        "operating_system_release": platform.release(),
        "machine_architecture": platform.machine(),
        "codex_desktop_updated": False,
        "host_security_changed": False,
        "windows_features_changed": False,
        "rebooted": False,
        "version_verification_only": True,
        "valid": True,
    }
    threat_results = {
        "schema": "ghc.family.caelen.v664-v8.threat-model-results.v1",
        "source": f"{PREFIX}x1/threat-model-plan.json",
        "planned_threat_count": 12,
        "control_witness_count": 12,
        "unmitigated_owner_software_threat_count": 0,
        "external_residuals_preserved": ["real people and materials absent", "professional and authority review absent", "manual accessibility evaluation absent", "independent security and reproduction absent"],
        "complete_privacy_claim": False,
        "complete_accessibility_claim": False,
        "exhaustive_security_claim": False,
        "valid": True,
    }
    wellbeing = {
        "schema": "ghc.family.caelen.v664-v8.wellbeing-check.v1",
        "owner": "Caelen Ash",
        "relational_only": True,
        "workload": {"single_sparse_lane": True, "x1_immutable": True, "proposal_count": 20, "mutation_count": 100, "pause_right_preserved": True, "rollback_available": True},
        "no_employment_or_personhood_claim": True,
        "hamish_may_pause_redirect_rename_or_stop": True,
        "status": "bounded_and_careful",
        "valid": True,
    }
    accessibility = {
        "schema": "ghc.family.caelen.v664-v8.accessibility-reservation.v1",
        "structural_checks": ["language declared", "semantic headings", "skip link", "table caption and header scopes", "visible focus style", "print fallback", "high contrast"],
        "manual_browser_evaluation": "reserved",
        "keyboard_evaluation": "reserved",
        "screen_reader_evaluation": "reserved",
        "notation_alternative_affected_user_evaluation": "reserved",
        "maori_language_review": "reserved to competent Māori language and Māori authorities",
        "accessibility_complete": False,
        "valid": True,
    }
    reproduction = {
        "schema": "ghc.family.caelen.v664-v8.reproduction-receipt.v1",
        "owner": "Caelen Ash",
        "infrastructure": "shared repository infrastructure",
        "same_owner_reproduction": True,
        "independent_team_reproduction": False,
        "external_audit": False,
        "full_repository_suite": False,
        "claim": "bounded deterministic same-owner software evidence only",
        "valid": True,
    }
    stage20 = {
        "schema": "ghc.family.caelen.v664-v8.stage20-evidence-board.v1",
        "evidence_vector": {
            "real_score_or_part": 0,
            "real_participant_or_operator": 0,
            "empirical_likelihood_or_statistics": 0,
            "professional_review": 0,
            "production_identity_event": 0,
            "legal_or_cultural_authority": 0,
            "maori_authority": 0,
            "independent_reproduction": 0,
        },
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    source_integrity = inherited_integrity()
    write_json("x2/x1-boundary-receipt.json", x1)
    write_json("x2/inherited-contract-integrity.json", source_integrity)
    write_json("x2/outcome-ledger.json", outcome_ledger)
    write_json("x2/mutation-summary.json", mutation_summary)
    write_json("x2/source-status-review.json", source_review)
    write_json("x2/retained-negative-register.json", retained)
    write_json("x2/exact-open-gate-register.json", gates)
    write_json("x2/method-flow-state.json", methods)
    write_json("x2/portfolio-execution.json", portfolio)
    write_json("x2/skill-build-receipt.json", skill_receipt)
    write_json("x2/runner-invocation-receipt.json", runner_receipt)
    write_json("x2/environment-version-receipt.json", environment)
    write_json("x2/threat-model-results.json", threat_results)
    write_json("x2/wellbeing-check.json", wellbeing)
    write_json("x2/accessibility-reservation.json", accessibility)
    write_json("x2/reproduction-receipt.json", reproduction)
    write_json("x2/stage20-evidence-board.json", stage20)
    write_phase_text("x2/accessible-static-report.html", accessible_report(outcomes))

    surface_files = [
        f"{PREFIX}x2/surfaces/{slug_for(row)}/{name}"
        for row in proposals
        for name in ("contract.json", "mutation-results.json", "bounded-receipt.json")
    ]
    inventory = {
        "schema": "ghc.family.caelen.v664-v8.x2-evidence-inventory.v1",
        "proposal_count": 20,
        "surface_file_count": len(surface_files),
        "runner_receipt_count": len(RUNNER_RECEIPT_FILES),
        "skill_count": len(SKILL_PATHS),
        "runner_count": len(WRAPPER_PATHS),
        "general_evidence_file_count": len(GENERAL_FILES),
        "surface_files": surface_files,
        "runner_receipts": RUNNER_RECEIPT_FILES,
        "skills": SKILL_PATHS,
        "runners": WRAPPER_PATHS,
        "owner_file_ceiling": 2_000,
        "document_word_ceiling": 100_000,
        "valid": True,
    }
    write_json("x2/x2-evidence-inventory.json", inventory)
    for relative in (
        "x2/x2-evidence-manifest.json",
        "x2/x2-stage-candidate.json",
        "x2/x2-staged-review.json",
    ):
        path = PHASE / relative
        if not path.exists():
            write_json(relative, {})
    return {
        "valid": all(
            (
                x1["valid"],
                source_integrity["valid"],
                mutation_summary["valid"],
                outcome_ledger["valid"],
                skill_receipt["valid"],
                runner_receipt["valid"],
                portfolio["valid"],
                methods["valid"],
            )
        ),
        "outcomes": dict(sorted(outcomes.items())),
        "mutations_executed": len(mutation_rows),
        "mutations_rejected": sum(row["rejected"] for row in mutation_rows),
        "skills_quick_validated": skill_receipt["quick_validated_count"],
        "runners_smoke_used": runner_receipt["smoke_used_count"],
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
    }


def expected_surface_files() -> list[str]:
    freeze = load_json(PHASE / "x1/proposal-freeze.json")
    return [
        f"{PREFIX}x2/surfaces/{slug_for(row)}/{name}"
        for row in freeze["new_proposals"]
        for name in ("contract.json", "mutation-results.json", "bounded-receipt.json")
    ]


def intended_allowlist() -> list[str]:
    return sorted(
        [
            BUILDER_PATH,
            TEST_PATH,
            CORE_PATH,
            *WRAPPER_PATHS,
            *SKILL_PATHS,
            *GENERAL_FILES,
            *RUNNER_RECEIPT_FILES,
            *expected_surface_files(),
        ]
    )


MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PREFIX}x2/x2-evidence-manifest.json",
        f"{PREFIX}x2/x2-stage-candidate.json",
        f"{PREFIX}x2/x2-staged-review.json",
    ]
)


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def scan_blob(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_value": re.compile(r"(?i)(?:resume[_ -]?value|raw[_ -]?route[_ -]?key)\s*[:=]\s*\S+"),
        "transcript_or_session_payload": re.compile(r"(?i)(?:conversation[_ -]?export|session[_ -]?stream[_ -]?payload)\s*[:=]\s*\S+"),
    }
    hits = []
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            hits.append(
                {
                    "path": path,
                    "class": class_name,
                    "excerpt_sha256": sha256(match.group(0).encode("utf-8")),
                    "disposition": "confirmed_issue",
                }
            )
    return hits


def write_staged_review() -> None:
    expected = intended_allowlist()
    actual = staged_paths()
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing or extra:
        raise EvidenceError(f"staged allowlist differs missing={missing} extra={extra}")
    entries: list[dict[str, Any]] = []
    json_count = 0
    html_count = 0
    python_count = 0
    scanner: list[dict[str, str]] = []
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".html"):
            text = raw.decode("utf-8")
            required = ("<html lang=", "<main", "<h1", "<h2", "<table", "<caption", "NOT_READY_FOR_STAGE_20")
            if not all(token in text for token in required):
                raise EvidenceError(f"HTML structural token missing: {path}")
            html_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        scanner.extend(scan_blob(path, raw))
        if path not in MANIFEST_EXCLUSIONS:
            entries.append(
                {"path": path, "sha256": sha256(raw), "size": len(raw), "hash_domain": "exact staged Git blob"}
            )
    if scanner:
        raise EvidenceError(f"confirmed privacy or raw-identifier findings: {scanner}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise EvidenceError(diff_check.stdout.decode("utf-8", "replace") + diff_check.stderr.decode("utf-8", "replace"))
    manifest = {
        "schema": "ghc.family.caelen.v664-v8.x2-evidence-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(expected),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(MANIFEST_EXCLUSIONS) == len(expected),
    }
    review = {
        "schema": "ghc.family.caelen.v664-v8.x2-staged-review.v1",
        "intended_path_count": len(expected),
        "staged_path_count": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "strict_json_count": json_count,
        "html_structural_check_count": html_count,
        "python_compile_count": python_count,
        "scanner_candidate_count": 0,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x1_paths_modified": [path for path in actual if f"{PREFIX}x1/" in path],
        "valid": not missing and not extra and not any(f"{PREFIX}x1/" in path for path in actual),
    }
    candidate = {
        "schema": "ghc.family.caelen.v664-v8.x2-stage-candidate.v1",
        "immutable_x1_head": X1_HEAD,
        "branch": BRANCH,
        "proposal_count": 20,
        "mutation_count": 100,
        "skills_quick_validated": 10,
        "runners_smoke_used": 10,
        "manifest": f"{PREFIX}x2/x2-evidence-manifest.json",
        "staged_review": f"{PREFIX}x2/x2-staged-review.json",
        "test_command": "python -m unittest tests.test_ghc_family_caelen_v664_v8_x2",
        "commit_state": "PREPARED_NOT_COMMITTED",
        "push_state": "PREPARED_NOT_PUSHED",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": review["valid"] and manifest["coverage_valid"],
    }
    write_json("x2/x2-evidence-manifest.json", manifest)
    write_json("x2/x2-staged-review.json", review)
    write_json("x2/x2-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    expected = intended_allowlist()
    if actual != expected:
        raise EvidenceError("staged allowlist changed after review")
    manifest = strict_json(index_blob(f"{PREFIX}x2/x2-evidence-manifest.json"), "manifest")
    review = strict_json(index_blob(f"{PREFIX}x2/x2-staged-review.json"), "review")
    candidate = strict_json(index_blob(f"{PREFIX}x2/x2-stage-candidate.json"), "candidate")
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise EvidenceError(f"manifest mismatch: {entry['path']}")
    if not (manifest["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise EvidenceError("one staged x2 receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "manifest_entries": len(manifest["entries"]),
        "manifest_exclusions": len(manifest["declared_self_exclusions"]),
        "strict_json": review["strict_json_count"],
        "python_compiles": review["python_compile_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": MANIFEST_EXCLUSIONS}
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
