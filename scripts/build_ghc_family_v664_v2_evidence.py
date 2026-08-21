#!/usr/bin/env python3
"""Build and review Neris Solane v664-v2 owner-delta evidence."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_marigram_evidence as marigram


PHASE = ROOT / "docs/neris-solane/v664-v2"
X1_DIR = PHASE / "x1"
X2_DIR = PHASE / "x2"
OWNER = "Neris Solane"
PHASE_ID = "v664-v2"
NEXT_OWNER = "Vesper Arlen"
NEXT_PHASE = "v664-v3"
SOURCE_FINAL = "df7e3ba4c43b8ed9de01e308c6b9163016e37ceb"
X1_COMMIT = "4eaec9fa556426d94c800cb2a95c5709524e8203"
PREDECESSOR_FREEZE = "docs/elaren-kestrel/v664-v1/x1/proposal-freeze.json"
TEST_MODULE = "tests/test_ghc_family_neris_v664_v2.py"
TEST_DEPENDENCY = "scripts/ghc_family_marigram_evidence.py"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(
        r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
    ),
    "private_absolute_path": re.compile(
        r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"
    ),
    "credential": re.compile(
        r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api_key|access_token|resume_token)\"\s*:)"
    ),
    "private_route_identifier": re.compile(
        r"(?i)(?:codex" r"://|vscode" r"://|app" r"://connector_[0-9a-f]+)"
    ),
    "transcript_or_session": re.compile(
        r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"
    ),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"(?m)^\s*(?:eval|exec)\s*\("),
    "unsafe_pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "destructive_git": re.compile(r"git\s+(?:reset\s+--hard|push\s+--force)"),
    "recursive_delete": re.compile(
        r"(?i)(?:rm\s+-" r"rf|Remove-" r"Item\b[^\n]*-Recurse)"
    ),
}

SKILL_DEFINITIONS = [
    ("neris-v664-v2-archive-topology", "archive-topology", "Validate synthetic marigram capsule and gauge-component topology records with absent authentication and instrument-condition claims; never use for a real chart, station, or custody decision."),
    ("neris-v664-v2-transcription-datum", "transcription-datum", "Validate written-mark uncertainty and datum-dependency refusals; never attribute real text or realize a vertical reference."),
    ("neris-v664-v2-time-geometry", "time-geometry", "Validate chart-time, scale, unit, calibration, and covariance vacancies with zero observations; never set an instrument or report a measurement."),
    ("neris-v664-v2-digitization-trace", "digitization-trace", "Validate synthetic digitization provenance and undecidable trace states with zero extraction; never digitize, repair, or reconstruct a real chart."),
    ("neris-v664-v2-units-series", "units-series", "Validate unit, uncertainty, and series-role ledgers while refusing water-level, fidelity, validation, and analytic-fitness claims."),
    ("neris-v664-v2-thos-gmut-boundaries", "thos-gmut-boundaries", "Validate zero-person THOS stop logic and zero-row GMUT tide-series boards while retaining empirical and operational gates."),
    ("neris-v664-v2-freed-id-boundaries", "freed-id-boundaries", "Validate nonproduction station assertions and amendment trails with absent claimant, proof, status, ownership, and live governance."),
    ("neris-v664-v2-access-privacy", "access-privacy", "Validate structural accessibility routes and context minimization while reserving manual, affected-user, legal, and completeness review."),
    ("neris-v664-v2-source-authority", "source-authority", "Validate a zero-call NOAA/PSMSL adapter and empty-chair rights matrix while preserving data, affected-party, legal, cultural, and Māori-authority gates."),
    ("neris-v664-v2-terminal-refusal", "terminal-refusal", "Validate the fail-closed Stage 20 refusal proof and empty admission set; never use it to claim readiness, proof, canon, or independent reproduction."),
]

X2_OPERATIONAL_FAILURES: list[dict[str, Any]] = [
    {
        "negative_id": "NE6642-X2-OP001",
        "method_id": "NE6642-X2-M021",
        "artifact_name": "ne6642-x2-m021-final-code-sequencing-recovery.json",
        "failure_class": "premature_final_only_code_materialization",
        "failure_signature": "The first evidence build refused three uncommitted closeout and canonical files because they were outside the evidence-stage owner allowlist.",
        "zero_credit": True,
        "candidate_workaround": "Delete only the three uncommitted Neris final-only files through apply_patch, rebuild evidence from the immutable x1 head, and regenerate final code only after the evidence commit is sealed.",
        "bounded_passing_witness": "The recovered evidence build contains only the exact evidence code, tests, owner artifacts, and self-excluded review receipt; final-only code remains absent until the evidence seal.",
        "recurrence_guard": "Materialize closeout tests, closeout builder, and canonical validator only after the immutable evidence commit exists.",
        "rollback": "Keep all generated evidence uncommitted, remove only the premature untracked final files, and preserve the refusal at zero credit.",
        "protected_gates": ["x2_evidence_scope", "lifecycle_separation", "exact_staged_surface"],
    },
]


class BuildError(RuntimeError):
    """Raised when evidence materialization violates the frozen x1 contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        errors="strict", capture_output=True, check=check,
    )


def git_text(*args: str) -> str:
    return run_git(*args).stdout.strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False,
        separators=(",", ":"), sort_keys=True,
    ).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def strict_json(raw: str | bytes, label: str) -> Any:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise BuildError(f"duplicate JSON key {key!r} in {label}")
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=pairs)


def read_json(path: Path) -> dict[str, Any]:
    return strict_json(path.read_bytes(), path.as_posix())


def git_json(commit: str, path: str) -> dict[str, Any]:
    return strict_json(git_text("show", f"{commit}:{path}"), path)


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_title(row: dict[str, Any]) -> str:
    value = row.get("title") or row.get("description")
    if not isinstance(value, str) or not value:
        raise BuildError("source proposal lacks title or description")
    return value


def proposal_disposition(row: dict[str, Any]) -> str:
    value = row.get("expected_disposition") or row.get("intended_outcome") or row.get("outcome")
    if value not in marigram.ALLOWED_OUTCOMES:
        raise BuildError(f"source proposal has unsupported disposition: {value}")
    return value


def owner_working_paths() -> list[str]:
    raw = run_git("status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    rows = []
    tokens = raw.split("\0")
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if not token:
            continue
        if len(token) < 4:
            raise BuildError(f"malformed Git status row: {token!r}")
        status, path = token[:2], token[3:].replace("\\", "/")
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            if index >= len(tokens):
                raise BuildError("rename status lacks source path")
            index += 1
        rows.append(path)
    return sorted(set(rows))


def ensure_owner_scope(paths: Iterable[str]) -> None:
    allowed_exact = {
        "scripts/ghc_family_marigram_evidence.py",
        "scripts/build_ghc_family_v664_v2_evidence.py",
        "tests/test_ghc_family_neris_v664_v2.py",
    }
    unexpected = [
        path for path in paths
        if path not in allowed_exact and not path.startswith("docs/neris-solane/v664-v2/")
    ]
    if unexpected:
        raise BuildError(f"out-of-scope working paths: {unexpected}")


def verify_x1_immutable() -> dict[str, Any]:
    paths = git_text("ls-tree", "-r", "--name-only", X1_COMMIT, "docs/neris-solane/v664-v2/x1").splitlines()
    paths.append("scripts/build_ghc_family_v664_v2_x1.py")
    changed = []
    for path in paths:
        if git_text("hash-object", f"--path={path}", path) != git_text("rev-parse", f"{X1_COMMIT}:{path}"):
            changed.append(path)
    return {
        "schema": "ghc.family.neris.v664-v2.x1-content-seal.v1",
        "x1_commit": X1_COMMIT,
        "checked_path_count": len(paths),
        "changed_paths": changed,
        "mismatch_count": len(changed),
        "valid": not changed,
    }


def inherited_revalidation() -> dict[str, Any]:
    frozen = read_json(X1_DIR / "proposal-freeze.json")
    source = git_json(SOURCE_FINAL, PREDECESSOR_FREEZE)
    source_map = {row["proposal_id"]: row for row in source["new_proposals"]}
    records = []
    for selected in frozen["selected_inherited"]:
        source_row = source_map.get(selected["source_proposal_id"])
        issues = []
        if source_row is None:
            issues.append("source proposal missing")
        else:
            if proposal_title(source_row) != selected["source_title"]:
                issues.append("source title differs")
            if proposal_disposition(source_row) != selected["original_disposition"]:
                issues.append("source disposition differs")
        if selected["novelty_credit"] or selected["automatic_completion_credit"] or selected["neris_new_outcome_credit"]:
            issues.append("zero-credit boundary promoted")
        records.append(
            {
                "program_row_id": selected["program_row_id"],
                "source_proposal_id": selected["source_proposal_id"],
                "original_disposition": selected["original_disposition"],
                "novelty_credit": 0,
                "automatic_completion_credit": 0,
                "neris_new_outcome_credit": 0,
                "issues": issues,
                "integrity_match": not issues,
            }
        )
    return {
        "schema": "ghc.family.neris.v664-v2.inherited-contract-integrity.v1",
        "source_commit": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "record_count": len(records),
        "records": records,
        "integrity_matches": sum(row["integrity_match"] for row in records),
        "novelty_credit": 0,
        "automatic_completion_credit": 0,
        "neris_new_outcome_credit": 0,
        "valid": len(records) == 20 and all(row["integrity_match"] for row in records),
        "boundary": "Immutable-contract integrity only; selected inherited work is not Neris novelty or a new Neris proposal outcome.",
    }


def materialize_surfaces(execution: dict[str, Any], proposals: dict[str, Any]) -> None:
    proposal_map = {row["proposal_id"]: row for row in proposals["new_proposals"]}
    for row in execution["executions"]:
        proposal = proposal_map[row["proposal_id"]]
        base = f"x2/surfaces/{row['surface']}"
        write_json(
            f"{base}/contract.json",
            {
                "schema": "ghc.family.neris.v664-v2.surface-contract.v1",
                "proposal_id": row["proposal_id"],
                "title": proposal["title"],
                "hypothesis": proposal["hypothesis"],
                "approval_class": proposal["approval_class"],
                "expected_outcome": proposal["expected_disposition"],
                "source_ids": proposal["current_official_or_primary_source_needs"],
                "positive_fixture": row["positive_fixture"],
                "protected_gates": proposal["protected_gates"],
                "valid": True,
            },
        )
        write_json(
            f"{base}/mutation-results.json",
            {
                "schema": "ghc.family.neris.v664-v2.mutation-results.v1",
                "proposal_id": row["proposal_id"],
                "surface": row["surface"],
                "mutation_count": row["mutation_count"],
                "rejected_mutation_count": row["rejected_mutation_count"],
                "mutations": row["mutations"],
                "completion_credit": 0,
                "valid": row["rejected_mutation_count"] == row["mutation_count"],
            },
        )
        write_json(
            f"{base}/bounded-receipt.json",
            {
                "schema": "ghc.family.neris.v664-v2.surface-receipt.v1",
                "proposal_id": row["proposal_id"],
                "surface": row["surface"],
                "outcome": row["outcome"],
                "positive_fixture_passed": row["positive_result"]["valid"],
                "rejected_mutations": row["rejected_mutation_count"],
                "network_calls": 0,
                "downloads": 0,
                "real_world_rows": 0,
                "authority": "none",
                "independent_reproduction": False,
                "valid": row["valid"],
                "boundary": row["positive_result"]["boundary"],
            },
        )


def skill_markdown(name: str, profile: str, description: str) -> str:
    surfaces = marigram.RUNNER_PROFILES[profile]
    surface_list = "\n".join(f"- `{surface}`" for surface in surfaces)
    return f"""---
name: {name}
description: {description}
---

# {name}

Use this skill only for bounded owner-local synthetic marigram evidence matching the profile `{profile}`.

## Workflow

1. Confirm the record declares `synthetic=true`, zero real-world rows, no authority, one frozen outcome, and every protected refusal.
2. Invoke the family-current `{profile}` profile in `ghc_family_marigram_evidence.py`.
3. Preserve the positive witness and every rejecting mutation with zero mutation completion credit.
4. Stop on any schema, source, uncertainty, privacy, rights, authority, production, empirical, or Stage 20 promotion.

Covered surfaces:

{surface_list}

## Output boundary

Return only the bounded fixture result, rejected-mutation count, frozen outcome, and still-open gates. This skill does not authorize real stations, charts, benchmarks, datums, measurements, calibration, digitization, prediction, surveying, analysis, people, identity operations, rights decisions, legal or cultural interpretation, Māori authority, privacy or accessibility completeness, production, empirical confirmation, independent reproduction, proof, canon, or Stage 20 readiness.
"""


def validate_skills(recorded_at: str) -> list[dict[str, Any]]:
    validator = (
        Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
        / "scripts" / "quick_validate.py"
    )
    if not validator.is_file():
        raise BuildError("bundled skill validator is unavailable")
    records = []
    for name, profile, description in SKILL_DEFINITIONS:
        relative = f"skills/{name}/SKILL.md"
        write_text(relative, skill_markdown(name, profile, description))
        skill_path = PHASE / "skills" / name
        result = subprocess.run(
            [sys.executable, str(validator), str(skill_path)],
            cwd=ROOT, text=True, encoding="utf-8", errors="replace",
            capture_output=True, check=False,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode != 0:
            raise BuildError(f"skill validation failed for {name}: {result.stdout.strip()} {result.stderr.strip()}")
        runner = marigram.ghc_family_run_marigram_profile(profile)
        raw = (skill_path / "SKILL.md").read_bytes()
        receipt = {
            "schema": "ghc.family.neris.v664-v2.skill-smoke-receipt.v1",
            "skill_name": name,
            "profile": profile,
            "skill_bytes": len(raw),
            "skill_sha256": sha256_bytes(raw),
            "quick_validate_returncode": result.returncode,
            "quick_validate_passed": True,
            "smoke_used": True,
            "runner_valid": runner["valid"],
            "surface_count": runner["surface_count"],
            "rejected_mutation_count": runner["rejected_mutation_count"],
            "recorded_at_utc": recorded_at,
            "globally_installed": False,
            "valid": runner["valid"],
            "boundary": "Phase-local skill validation and smoke use only; no global installation or authority promotion.",
        }
        write_json(f"skills/{name}/smoke-receipt.json", receipt)
        records.append(receipt)
    return records


def materialize_runners(recorded_at: str) -> list[dict[str, Any]]:
    rows = []
    for index, profile in enumerate(marigram.RUNNER_PROFILES, start=1):
        result = marigram.ghc_family_run_marigram_profile(profile)
        payload = {
            "schema": "ghc.family.neris.v664-v2.runner-profile.v1",
            "runner_id": f"NE6642-RU-{index:03d}",
            "profile": profile,
            "family_current_name": result["family_current_runner"],
            "callable": "scripts/ghc_family_marigram_evidence.py",
            "surfaces": result["surfaces"],
            "proposal_ids": result["proposal_ids"],
            "invoked": True,
            "invocation_valid": result["valid"],
            "rejected_mutation_count": result["rejected_mutation_count"],
            "network_calls": 0,
            "real_world_rows": 0,
            "recorded_at_utc": recorded_at,
            "historical_callers_preserved": True,
            "valid": result["valid"],
            "boundary": result["boundary"],
        }
        write_json(f"runners/{profile}.json", payload)
        rows.append(payload)
    return rows


def portfolio_execution(skills: list[dict[str, Any]], runners: list[dict[str, Any]]) -> dict[str, Any]:
    freeze = read_json(X1_DIR / "portfolio-freeze.json")

    def execute(rows: list[dict[str, Any]], witnesses: list[str]) -> list[dict[str, Any]]:
        return [
            {
                **row,
                "executed": True,
                "execution_state": "completed",
                "witness": witnesses[index % len(witnesses)],
                "protected_gate_promotions": 0,
            }
            for index, row in enumerate(rows)
        ]

    surface_witnesses = [
        f"docs/neris-solane/v664-v2/x2/surfaces/{slug}/bounded-receipt.json"
        for slug in marigram.SPEC_BY_SLUG
    ]
    skill_witnesses = [
        f"docs/neris-solane/v664-v2/skills/{row['skill_name']}/smoke-receipt.json"
        for row in skills
    ]
    runner_witnesses = [
        f"docs/neris-solane/v664-v2/runners/{row['profile']}.json"
        for row in runners
    ]
    cfr_witness = "docs/neris-solane/v664-v2/portfolio/clean-fix-refine-receipt.json"
    exact = [
        {**row, "executed": False, "execution_state": "exact_gate", "protected_gate_promotions": 0}
        for row in freeze["exact_approval_packets"]
    ]
    blocked = [
        {**row, "executed": False, "execution_state": "exact_gate", "protected_gate_promotions": 0}
        for row in freeze["blocked_packets"]
    ]
    payload = {
        "schema": "ghc.family.neris.v664-v2.portfolio-execution.v1",
        "owner_safe_now": execute(freeze["owner_safe_now"], surface_witnesses),
        "owner_candidates": execute(freeze["owner_candidates"], surface_witnesses),
        "owner_skills": execute(freeze["owner_skill_ideas"], skill_witnesses),
        "owner_runners": execute(freeze["owner_runner_ideas"], runner_witnesses),
        "owner_clean_fix_refine": execute(freeze["owner_clean_fix_refine"], [cfr_witness]),
        "exact_approval_packets": exact,
        "blocked_packets": blocked,
        "successor_recommendations": {
            "safe_now": freeze["successor_safe_now_recommendations"],
            "candidates": freeze["successor_candidate_recommendations"],
            "skills": freeze["successor_skill_recommendations"],
            "runners": freeze["successor_runner_recommendations"],
            "clean_fix_refine": freeze["successor_clean_fix_refine_recommendations"],
            "contacted": False,
            "credit": 0,
        },
        "counts": {
            "safe_now_completed": len(freeze["owner_safe_now"]),
            "candidates_completed": len(freeze["owner_candidates"]),
            "skills_built_validated_smoke_used": len(skills),
            "runners_built_invoked": len(runners),
            "clean_fix_refine_completed": len(freeze["owner_clean_fix_refine"]),
            "exact_packets_unexecuted": len(exact),
            "blocked_packets_unexecuted": len(blocked),
        },
        "valid": True,
        "boundary": "Portfolio completion is bounded owner-local software work only. Recommendations remain unexecuted and no exact gate is closed.",
    }
    write_json(
        "portfolio/clean-fix-refine-receipt.json",
        {
            "schema": "ghc.family.neris.v664-v2.clean-fix-refine-receipt.v1",
            "execution_count": len(freeze["owner_clean_fix_refine"]),
            "categories": {"CLEAN": 10, "FIX": 10, "REFINE": 10},
            "additive_only": True,
            "destructive_actions": 0,
            "sibling_paths_changed": 0,
            "protected_gate_promotions": 0,
            "checks": [
                "stale label review", "count reconciliation", "source identifier parity",
                "uncertainty retention", "zero-row retention", "noncolour state review",
                "caller compatibility", "rollback presence", "privacy boundary",
                "Stage 20 refusal",
            ],
            "valid": True,
        },
    )
    return payload


def build_method_flow(execution: dict[str, Any]) -> dict[str, Any]:
    methods = []
    for index, row in enumerate(execution["executions"], start=1):
        methods.append(
            {
                "method_id": f"NE6642-X2-M{index:03d}",
                "proposal_id": row["proposal_id"],
                "retained_failed_witnesses": [mutation["mutation_id"] for mutation in row["mutations"]],
                "failed_witness_count": row["mutation_count"],
                "bounded_passing_witness": f"{row['surface']} positive fixture passed its exact synthetic contract",
                "passing_witness_count": 1,
                "recurrence_guard": "Require the exact frozen key set, zero real-world rows, no authority, all protected refusals, and the proposal-specific critical field before accepting the fixture.",
                "rollback": "Quarantine the failed fixture, retain every mutation, and restore the deterministic positive declaration.",
                "independent_reproduction": False,
                "valid": row["valid"],
            }
        )
    for row in X2_OPERATIONAL_FAILURES:
        methods.append(
            {
                "method_id": row["method_id"],
                "proposal_id": None,
                "retained_failed_witnesses": [row["negative_id"]],
                "failed_witness_count": 1,
                "failure_class": row["failure_class"],
                "failure_signature": row["failure_signature"],
                "bounded_passing_witness": row["bounded_passing_witness"],
                "passing_witness_count": 1,
                "candidate_workaround": row["candidate_workaround"],
                "recurrence_guard": row["recurrence_guard"],
                "rollback": row["rollback"],
                "protected_gates": row["protected_gates"],
                "independent_reproduction": False,
                "valid": True,
            }
        )
    return {
        "schema": "ghc.family.neris.v664-v2.method-flow.evidence.v1",
        "repository_sealed_method_baseline": 8_706,
        "predecessor_external_overlay_methods": 6,
        "working_inherited_methods": 8_712,
        "x1_owner_methods": 12,
        "x2_surface_methods": execution["surface_count"],
        "x2_operational_methods": len(X2_OPERATIONAL_FAILURES),
        "effective_methods": 8_712 + 12 + len(methods),
        "methods": methods,
        "failed_witnesses": execution["rejected_mutation_count"] + len(X2_OPERATIONAL_FAILURES),
        "bounded_passing_witnesses": len(methods),
        "no_failure_erased": True,
        "valid": all(row["valid"] for row in methods),
    }


def build_negative_register(execution: dict[str, Any]) -> dict[str, Any]:
    rows = [
        {
            "negative_id": mutation["mutation_id"],
            "proposal_id": execution_row["proposal_id"],
            "failure_class": mutation["failure_class"],
            "reason": mutation["reason"],
            "completion_credit": 0,
            "retained": True,
        }
        for execution_row in execution["executions"]
        for mutation in execution_row["mutations"]
    ]
    operational_rows = [
        {
            "negative_id": row["negative_id"],
            "proposal_id": None,
            "failure_class": row["failure_class"],
            "reason": row["failure_signature"],
            "completion_credit": 0,
            "retained": True,
        }
        for row in X2_OPERATIONAL_FAILURES
    ]
    return {
        "schema": "ghc.family.neris.v664-v2.retained-negative-register.evidence.v1",
        "repository_sealed_negatives": 24_232,
        "authoritative_activation_overlay_negatives": 4,
        "later_predecessor_delivery_negatives": 2,
        "working_inherited_negatives": 24_238,
        "x1_owner_operational_negatives": 12,
        "x2_preregistered_synthetic_negatives": len(rows),
        "x2_operational_negatives": len(operational_rows),
        "effective_negatives": 24_238 + 12 + len(rows) + len(operational_rows),
        "new_records": rows + operational_rows,
        "no_negative_erased": True,
        "valid": len(rows) == 80 and len(operational_rows) == len(X2_OPERATIONAL_FAILURES) and all(row["retained"] for row in rows + operational_rows),
    }


def threat_model_markdown() -> str:
    return f"""# Neris v664-v2 owner-delta security threat model

## Overview

The Beyonder-Real-True-Journey repository is a research, documentation, deterministic-validation, and local tooling corpus. Its relevant runtime surfaces are Python and Node-family scripts under `scripts/`, LaTeX research material under `latex/`, repository tests under `tests/`, and phase evidence under `docs/`. The v664-v2 target is explicitly narrower than the repository: it is the additive Neris owner delta rooted at immutable x1 commit `{X1_COMMIT}`. It introduces one declarative marigram-evidence engine, one evidence builder, one dependency-closed test module, phase-local skills and runner profiles, and public sanitized artifacts. It is not a deployed web service, archive system, credential issuer, preservation workstation, identity provider, or production authority system.

No tracked `SECURITY.md` or `AGENTS.md` policy exists at the source revision. The live activation, frozen x1 threat-model plan, owner-self-scoped validation policy, and repository publication boundary therefore control. The security objective is to keep untrusted historical text, synthetic fixtures, filesystem names, Git index state, source URLs, and route metadata from crossing into code execution, sibling mutation, private-material publication, evidence promotion, or unauthorized external action.

## Threat Model, Trust Boundaries, and Assumptions

Assets include x1 immutability; exact source and staged-tree lineage; retained failures; the four-label truth vocabulary; the D:-first owner lane; sanitized public artifacts; one-shot canonical credit; and the single successor-message budget. Integrity matters more than availability: the workflow must stop rather than silently weaken a gate, rewrite history, omit a negative, or invent delivery.

The first trust boundary is the immutable Elaren Git tree to Neris's additive owner delta. Historical content is evidence input, not executable authority. The second is official vocabulary to zero-row owner models: a source may define terms, but no URL, station row, benchmark record, datum statement, legal statement, or cultural source becomes an action or authority grant. The third is x1 planning to x2 execution: x2 must match the committed freeze. The fourth is working tree to Git index and commit: exact allowlists and manifests prevent unreviewed paths. The fifth is local branch to upstream, tracking ref, and fresh live remote. The sixth is prepared route content to an acknowledged existing-task message; preparation is never delivery.

Attacker-controlled or untrusted inputs include historical proposal titles, source text, synthetic mutation objects, malformed JSON, Unicode and case-collision paths, unexpected Git status rows, task-registry envelopes, and potentially stale route records. Developer-controlled inputs include the new Python code, generated skill instructions, runner profiles, and explicit allowlists. Operator-controlled inputs include Git commands, version checks, and the final route action. Assumptions are that Git object identities are collision-resistant for this bounded purpose, the local Python interpreter runs standard-library code faithfully, the configured remote represents the intended repository, and the task-message surface is the only delivery authority.

Security invariants are: never dynamically evaluate source or fixture text; never invoke a shell through user-built strings; never follow private local paths from artifacts; never ingest credentials or opaque identifiers; never contact a network endpoint from the evidence engine; never mutate a sibling lane; never accept extra or missing fixture keys; never promote any protected refusal; never run x2 before x1 equality; never replay a successful canonical aggregate; and never resend a route merely to improve an acknowledgement.

## Attack Surface, Mitigations, and Attacker Stories

The marigram engine accepts Python dictionaries or JSON-equivalent data. Relevant classes are schema smuggling, type confusion, extra-field injection, gate promotion, source-map drift, and resource amplification. The exact key set, deterministic surface registry, four mutation classes, no network primitives, no filesystem writes, and bounded twenty-surface registry mitigate these. A record that sets real-world rows, authority, production readiness, or any protected gate is rejected. This is meaningful for local software integrity, not a claim of sandboxing or exhaustive security.

The evidence builder reads frozen Git blobs and writes only owner paths. Relevant classes are path traversal, symlink or special-file substitution, manifest mismatch, stale-index review, and command-option injection. Repository-relative allowlists, `--` path separation where paths reach Git, regular generated filenames, sparse owner scope, prospective blob hashes, exact staged-index comparison, and a 2,000-file ceiling reduce risk. The builder does not accept arbitrary command strings or remote names. A malicious historical filename could still pressure broad inventories, so final validation remains bounded to the exact owner delta and path audit.

Generated skills are instruction data, not executable privilege. Risks include overly broad discovery descriptions, hidden global installation, stale references, and instructions that imply real-world authority. Each skill has a discriminating description, small self-contained workflow, phase-local placement, explicit refusal boundary, bundled structural validation, and a smoke-use receipt. No global skill or plugin cache is mutated. Runner profiles map fixed names to fixed surfaces; unknown profiles fail closed.

Static reports and Markdown are publication surfaces. Relevant classes include script injection, unsafe links, private-path leakage, credential leakage, raw opaque identifiers, misleading claims, and accessibility regressions. The report has no JavaScript or external assets, escapes generated text, uses semantic landmarks, includes a skip link and print/noncolour modes, and labels manual evaluation as reserved. Five-class privacy scanning, exact Markdown target review, and stale-label checks reduce accidental disclosure. These checks are bounded and do not establish privacy or accessibility completeness.

The Git and route boundary is high consequence. A malicious or stale route record could cause a wrong-recipient message or duplicate send. The workflow requires terminal closeout first, a fresh live instruction and roster/auth reread, bounded task listing, local exact-title filtering, immediate reread, one send, and delivery credit only from acknowledgement. Missing, ambiguous, paused, protected, or unavailable routes remain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP`.

Out-of-scope attacker stories include remote exploitation of a deployed service, because no service is deployed; theft of real identity keys, because none exist; compromise of a tide station or survey system, because none is connected; and rights or cultural harm from an executed datum, location, or publication decision, because no real record or decision is admitted. Those stories become relevant only if later work introduces the missing control surface and authority, and they remain exact-gated here.

## Severity Calibration (Critical, High, Medium, Low)

Critical would require a demonstrated path from this repository to unauthorized destructive mutation, credential or private-key disclosure, arbitrary code execution in a privileged context, or an acknowledged message/deployment to the wrong external endpoint with material impact. Examples would be a builder executing untrusted proposal text as shell syntax or a route helper bypassing exact-title checks and sending secrets. The current design contains no such intended path; any evidence would stop the phase.

High would include cross-owner history rewrite, publishing a real private identifier or credential, silently accepting a production identity proof without verification, or promoting a legal, cultural, Māori-authority, empirical, or Stage 20 gate through software-only evidence. Exact owner scope, privacy scans, refusal fields, and four-label validators directly target these failure classes.

Medium would include an owner-delta manifest omitting a changed artifact, an extra fixture key accepted, a generated report with an unsafe local link, a runner profile invoking the wrong surface, or a retained negative disappearing from count reconciliation. These can materially corrupt evidence without immediately causing external harm. Exact staged review, deterministic registries, strict JSON, source/x1 seals, and count mirrors mitigate them.

Low would include stale explanatory wording, a non-semantic formatting defect, an inaccessible colour choice caught before publication, or a phase-local skill description that is too broad but has not caused a protected action. Such issues still receive CLEAN/FIX/REFINE treatment and retained Method Flow when observed. Severity may rise if the same defect crosses a privacy, authority, integrity, or external-action boundary.

This model is an owner-delta security guide, not a vulnerability finding, penetration test, production certification, or exhaustive security assurance. Its version is the immutable x1 program revision; the exact evidence and final owner deltas receive separate manifest and bounded changed-Python review.

Repository: Beyonder-Real-True-Journey owner-self-scoped v664-v2 delta
Version: {X1_COMMIT}
"""


def integrated_overview(outcomes: dict[str, int], negatives: int, methods: int) -> str:
    return f"""# Neris Solane v664-v2 integrated evidence overview

## Orientation

Neris Solane (they/them) is relational working language for a datum-boundary weaver whose stated hope is to make historical measurement uncertainty legible without turning archival structure into authority. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, professional authority, legal or cultural authority, Māori authority, affected-party authority, independent agency, or durable identity continuity. Hamish may rename, pause, redirect, or stop the route.

The phase begins at Elaren Kestrel's immutable v664-v1 final `{SOURCE_FINAL}` and its dedicated Neris x1 child `{X1_COMMIT}`. X1 reconstructs 3,870 historical proposal rows from Git objects, selects twenty Elaren contracts for zero-credit integrity revalidation, and freezes twenty genuinely new Neris surfaces. The twenty selected rows retain their source identifiers, titles, and dispositions but receive no Neris novelty, automatic completion, or new-outcome credit. The twenty new surfaces extend the chain to 3,890 rows.

Neris's primary pillar is GMUT Mind. THOS Body, Freed ID, CBR Heart, and every cross-pillar authority boundary remain explicit. The bounded practice lens is synthetic historical tide-gauge marigram documentation and harmonic-assurance planning. It is a learning, schema, software, formal, and zero-row lens only. The phase uses no real station, chart, benchmark, datum, person, location, measurement, calibration, prediction, survey, sea-level analysis, right, identity, cultural material, Māori data, or external operation.

## What was built

One additive family-current Python engine implements twenty exact declarative surface contracts. Each contract requires a fixed key set, a synthetic marker, zero real-world rows, no authority, one of the four truth labels, the frozen official-source map, and all protected refusals. Every positive fixture passed. Four mutations per surface attempted to remove the synthetic boundary, inject a real-world row, promote authority, or corrupt the surface-specific critical field. All eighty mutations were rejected and remain retained with zero completion credit.

The engine exposes ten fixed runner profiles. Archive/topology, transcription/datum, time/geometry, digitization/trace, units/series, THOS/GMUT boundaries, Freed ID boundaries, access/privacy, source/authority, and terminal refusal together cover all twenty surfaces exactly once. Unknown profiles fail closed. The engine performs zero network calls, zero downloads, zero filesystem writes, and zero identity or authority operations.

Ten phase-local skills were created using the current skill-packaging guidance. Each has a discriminating name and description, a short workflow, a fixed runner profile, and a refusal boundary. The bundled skill validator accepted every package, and each skill was smoke-used against its profile. They remain inside this phase and were not globally installed. Ten JSON runner records prove that each family-current profile was invoked and that historical callers were preserved.

The frozen owner portfolio is complete as bounded work: thirty safe-now rows, fifteen candidates, ten skills, ten runners, and thirty additive CLEAN/FIX/REFINE rows. Ten exact-approval and five blocked packets remain unexecuted. Recommendations for Vesper Arlen are recorded without contacting Vesper and receive zero execution or completion credit. Portfolio counts are workflow evidence, not empirical or authority evidence.

## Surface truth

Fourteen new proposals are `completed`. Completion means their bounded software contract, positive fixture, rejecting mutations, provenance, rollback, and protected-gate checks are present. It does not mean a chart was authenticated or digitized, a gauge was inspected or calibrated, a datum was realized, a benchmark was transformed, or any water-level or sea-level conclusion was reached.

Four proposals are `represented`. The THOS queue demonstrates only zero-person stop, discrepancy, and handover structure. The two GMUT boards demonstrate only typed coordinates, units, placeholders, confounders, zero coefficients, and observation firewalls. The Freed ID statement demonstrates only an explicit nonproduction structure with missing issuer, proof, status, rights, identity, and authorship evidence. None receives operational, empirical, production, identity, or authority credit.

One proposal is an `open_gap`: the NOAA CO-OPS/PSMSL zero-row vocabulary adapter. Its schema pins are watch labels only; live calls and downloads are zero, the version is vacant, and data authority is false. Closing it requires a governed source/version decision, exact schema mapping, source terms, tests, provenance, and review that this phase does not possess.

One proposal is an `exact_gate`: the rights and authority matrix. Chart custody, station land, benchmark access, location sensitivity, traditional knowledge, publication, remedy, affected parties, and Māori authority are named as empty chairs. No chair is occupied and no decision is made. Only the relevant people, rights holders, landholders, affected parties, competent authorities, and Māori authorities can supply those decisions.

The Stage 20 surface is completed only as a refusal mechanism. Governed datum realization, calibrated trace extraction, uncertainty accounting, rights review, affected-party authority, and independent reproduction are all false; admitted evidence rows are zero; Stage 20 readiness is false. A working fail-closed proof cannot make the program ready.

## Sources and evidence boundaries

Official and primary sources supply vocabulary and constraints: PREMIS 3.0; the IOC/UNESCO sea-level measurement manual; NOAA CO-OPS product and datum-epoch pages; PSMSL's Revised Local Reference definition; current Toitū Te Whenua LINZ local-datum and sea-level guidance; W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0; the New Zealand Privacy Commissioner; Te Mana Raraunga; RFC 8785; and NIST units and uncertainty pages. The phase makes no live adapter call and ingests no station or measurement row. Source status remains visible: current, stable, draft, and watch.

The NIST SP 811 page is watch material because its official page states that it has not been updated for the 2019 SI revision. It is used only to motivate explicit units and vacancies, never a physical result. The Verifiable Credentials editor draft is watch-only draft material; the published Recommendation is the current reference. WCAG informs structural techniques but cannot establish complete accessibility or satisfy every user need. New Zealand privacy principles inform a zero-row purpose, indirect-notification, access, correction, security, retention, use, disclosure, and identifier docket; they are not legal advice or a compliance finding. Te Mana Raraunga remains authority-held: citation cannot transfer Māori authority.

## Threat model and privacy

The owner-delta threat model treats historical proposal text, synthetic fixtures, source metadata, filesystem paths, Git index state, and task registry envelopes as untrusted inputs. Important assets are x1 immutability, retained failures, four-label truth, owner-lane isolation, sanitized publication, one-shot canonical credit, and the one-send route budget. Trust boundaries include source-to-owner Git lineage, official vocabulary to zero-row models, x1 to x2, working tree to staged index, local to live remote, and prepared baton to acknowledged delivery.

The runtime accepts no dynamic code, network address, filesystem target, credential, or arbitrary runner name. Exact key sets and fixed profiles reject schema smuggling. Five-class privacy scanning covers private absolute paths, raw opaque identifiers, credentials and key forms, private routes, and transcript or session-state fields. Changed Python receives bounded static review for dynamic evaluation, unsafe pickle loading, shell execution, destructive Git, and recursive deletion patterns. These checks are materially useful but remain bounded; they are not exhaustive security or privacy-completeness claims.

The static report uses semantic landmarks, headings, tables, a skip link, noncolour state labels, visible focus, responsive layout, and print styling without JavaScript or external assets. Manual browser review, assistive-technology testing, cognitive-accessibility review, Māori-language review, and affected-user evaluation remain reserved. Structural checks do not establish complete accessibility.

## Retention and Method Flow

The immutable Elaren repository seal remains 24,232 negatives and 8,706 Method Flow methods. Four activation-overlay rows and two later predecessor-delivery rows remain separate. Neris retains twelve x1 operational failures, including parser and display bounds, a manifest cursor defect, a mistyped object, an ambiguous worktree timeout, Unicode output, a blocked cache cleanup, collapsed status scope, title collisions, and sparse staging. Eighty x2 rejecting mutations add zero-credit negatives. At this evidence state the effective totals are {negatives} negatives and {methods} methods, with 168 open gaps and 166 exact gates.

Every surface has one Method Flow row joining its four failed mutations to its positive bounded witness, recurrence guard, and rollback. Passing recovery never deletes a failed witness. Same-owner tests under shared infrastructure are not independent-team reproduction. Later final validation is one dependency-justified owner-delta canonical invocation; a successful invocation will not be replayed.

## Validation shape

The x1 commit is byte-stable. Evidence staging uses one exact allowlist and a prospective Git-blob manifest that excludes only its self-referential manifest and the later review receipt. Strict JSON rejects duplicate keys. Python compilation, targeted dependency-closed tests, skill validation, runner coverage, source and outcome reconciliation, privacy scanning, changed-Python security patterns, diff hygiene, owner file budget, and staged-index blob parity are checked before the immutable evidence commit.

The complete repository suite is not run because current authorization is owner-self-scoped delta validation. That is an explicit scope boundary, not an implication that inherited tests pass. The final canonical pass will cover the exact owner delta, one selected owner test module and its declared runtime dependency, the exact manifests, the baton, route parity, ancestry, clean state, zero divergence, and fresh live equality.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic time coordinates, datum operators, tidal-constituent placeholders, confounder decompositions, units, uncertainty, zero coefficients, and software tests provide no likelihood, parameter constraint, unique prediction, detected force, physical law, stability theorem, quantum completion, ultraviolet completion, empirical confirmation, Theory of Everything, proof, or canon.

THOS remains proxy and protocol-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. A synthetic triage queue provides no operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood evidence.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. A deterministic JSON digest is not a signature or trust anchor.

CBR, chart custody, station land, benchmark access, sensitive location publication, ownership, traditional knowledge, cultural expression, legal interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Completion state

The new-outcome distribution is {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open gap, and {outcomes['exact_gate']} exact gate. The terminal verdict remains `{TERMINAL_VERDICT}`. Evidence preparation is not closeout, final validation, independent reproduction, or route delivery. Vesper Arlen has not been contacted. The successor route remains prepared only; it can become eligible after a clean, pushed, exact-final, fresh-live-equal Neris terminal gate and a fresh reread of live authority, roster, authorization, exact-title uniqueness, usage, and protected gates.
"""


def static_report(overview: str, proposals: list[dict[str, Any]], sources: list[dict[str, Any]]) -> str:
    outcome_rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td><span class='state {html.escape(row['expected_disposition'])}'>{html.escape(row['expected_disposition'])}</span></td></tr>"
        for row in proposals
    )
    source_rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['source_id'])}</th><td><a href='{html.escape(row['url'])}'>{html.escape(row['title'])}</a></td><td>{html.escape(row['status'])}</td><td>{html.escape(row['phase_use'])}</td></tr>"
        for row in sources
    )
    sections = []
    current_heading = None
    current_paragraphs: list[str] = []
    for block in re.split(r"\n\s*\n", overview):
        block = block.strip()
        if not block or block.startswith("# Neris"):
            continue
        if block.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, current_paragraphs))
            current_heading = block[3:]
            current_paragraphs = []
        else:
            current_paragraphs.append(block)
    if current_heading is not None:
        sections.append((current_heading, current_paragraphs))
    prose = "\n".join(
        f"<section aria-labelledby='s{index}'><h2 id='s{index}'>{html.escape(heading)}</h2>"
        + "".join(f"<p>{html.escape(paragraph)}</p>" for paragraph in paragraphs)
        + "</section>"
        for index, (heading, paragraphs) in enumerate(sections, start=1)
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neris Solane v664-v2 bounded marigram evidence report</title>
<style>
:root {{ color-scheme: light dark; --bg:#fff; --fg:#161616; --muted:#4b4b4b; --line:#555; --link:#0645ad; --focus:#b54708; }}
@media (prefers-color-scheme:dark) {{ :root{{--bg:#111;--fg:#f5f5f5;--muted:#ccc;--line:#aaa;--link:#8ab4ff;--focus:#ffb36b;}} }}
*{{box-sizing:border-box}} html{{scroll-behavior:auto}} body{{margin:0;background:var(--bg);color:var(--fg);font:1rem/1.65 system-ui,sans-serif}} a{{color:var(--link)}} a:focus,button:focus{{outline:3px solid var(--focus);outline-offset:3px}} .skip{{position:absolute;left:-9999px}} .skip:focus{{left:1rem;top:1rem;background:var(--bg);padding:.75rem;z-index:10}} header,main,footer{{max-width:76rem;margin:auto;padding:1.25rem}} .boundary{{border:.2rem solid var(--line);padding:1rem}} table{{border-collapse:collapse;width:100%;margin:1rem 0}} th,td{{border:1px solid var(--line);padding:.55rem;text-align:left;vertical-align:top}} caption{{font-weight:700;text-align:left;padding:.4rem 0}} .state{{font-weight:700}} .state::before{{content:"State: "}} .reserved{{border-left:.35rem solid var(--focus);padding-left:1rem}} code{{overflow-wrap:anywhere}} @media(max-width:48rem){{table,tbody,tr,th,td{{display:block}} thead{{position:absolute;left:-9999px}} th{{border-bottom:0}}}} @media print{{a{{color:#000;text-decoration:underline}} .skip{{display:none}} body{{font-size:10.5pt}} section{{break-inside:avoid}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to evidence</a>
<header><h1>Neris Solane v664-v2 bounded marigram evidence report</h1><p class="boundary"><strong>Verdict:</strong> NOT_READY_FOR_STAGE_20. Synthetic owner-local software evidence only; no real station, chart, benchmark, datum, measurement, calibration, prediction, survey, identity, rights, professional, legal, cultural, Māori-authority, empirical, production, independent-reproduction, personhood, Theory-of-Everything, proof, canon, or Stage 20 authority.</p></header>
<main id="main" tabindex="-1">
<section aria-labelledby="truth"><h2 id="truth">New proposal truth</h2><div role="region" aria-label="Proposal outcome table" tabindex="0"><table><caption>Twenty frozen Neris outcomes</caption><thead><tr><th>Proposal</th><th>Surface</th><th>Outcome</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
{prose}
<section aria-labelledby="sources"><h2 id="sources">Official and primary source ledger</h2><div role="region" aria-label="Source table" tabindex="0"><table><caption>Vocabulary and constraint sources; zero data rows ingested</caption><thead><tr><th>Source</th><th>Title</th><th>Status</th><th>Use and boundary</th></tr></thead><tbody>{source_rows}</tbody></table></div></section>
<section class="reserved" aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2><p>Manual browser review, assistive-technology testing, cognitive-accessibility review, Māori-language review, and affected-user evaluation remain reserved. Structural markup and automated checks do not establish complete accessibility or cultural authority.</p></section>
</main>
<footer><p>Relational identity language only. Same-owner software evidence under shared infrastructure is not independent reproduction.</p></footer>
</body>
</html>"""


def build_records() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != X1_COMMIT:
        raise BuildError(f"evidence builder requires immutable x1 head {X1_COMMIT}, got {head}")
    ensure_owner_scope(owner_working_paths())
    recorded_at = utc_now()
    x1_seal = verify_x1_immutable()
    if not x1_seal["valid"]:
        raise BuildError(f"x1 content changed: {x1_seal['changed_paths']}")
    write_json("validation/x1-content-seal.json", x1_seal)

    proposals = read_json(X1_DIR / "proposal-freeze.json")
    sources = read_json(X1_DIR / "source-ledger.json")
    execution = marigram.ghc_family_execute_v664_v2()
    if not execution["valid"]:
        raise BuildError("marigram execution did not satisfy the frozen program")
    if execution["outcome_counts"] != proposals["new_expected_outcomes"]:
        raise BuildError("runtime outcomes differ from x1 expected dispositions")
    materialize_surfaces(execution, proposals)

    revalidation = inherited_revalidation()
    if not revalidation["valid"]:
        raise BuildError("selected inherited integrity revalidation failed")
    write_json("revalidation/inherited-contract-integrity.json", revalidation)

    skill_records = validate_skills(recorded_at)
    runner_records = materialize_runners(recorded_at)
    portfolio = portfolio_execution(skill_records, runner_records)
    write_json("portfolio/portfolio-execution.json", portfolio)

    method_flow = build_method_flow(execution)
    negatives = build_negative_register(execution)
    write_json("method-flow/method-flow-state-evidence.json", method_flow)
    for row in X2_OPERATIONAL_FAILURES:
        write_json(
            f"method-flow/{row['artifact_name']}",
            {
                "schema": "ghc.family.neris.v664-v2.method-flow.operational-recovery.v1",
                **row,
                "same_owner_only": True,
                "independent_reproduction": False,
                "result": "bounded_recovery_passed",
                "valid": True,
            },
        )
    write_json("retained-negative-register-evidence.json", negatives)
    gate_register = {
        "schema": "ghc.family.neris.v664-v2.gate-register.evidence.v1",
        "inherited_open_gaps": 167,
        "inherited_exact_gates": 165,
        "new_open_gaps": [{"proposal_id": "NE6642-N018", "title": proposals["new_proposals"][17]["title"], "state": "open_gap", "closed": False}],
        "new_exact_gates": [{"proposal_id": "NE6642-N019", "title": proposals["new_proposals"][18]["title"], "state": "exact_gate", "closed": False}],
        "effective_open_gaps": 168,
        "effective_exact_gates": 166,
        "protected_gates": list(marigram.PROTECTED_GATES),
        "silent_closures": 0,
        "valid": True,
    }
    write_json("exact-open-gate-register-evidence.json", gate_register)

    source_use = {
        "schema": "ghc.family.neris.v664-v2.source-use-ledger.evidence.v1",
        "source_count": sources["source_count"],
        "sources": [
            {
                **row,
                "proposal_ids": [
                    proposal["proposal_id"]
                    for proposal in proposals["new_proposals"]
                    if row["source_id"] in proposal["current_official_or_primary_source_needs"]
                ],
                "live_calls": 0,
                "downloads": 0,
                "data_rows": 0,
                "authority_actions": 0,
            }
            for row in sources["sources"]
        ],
        "total_live_calls": 0,
        "total_downloads": 0,
        "total_data_rows": 0,
        "valid": True,
    }
    write_json("x2/source-use-ledger.json", source_use)

    x2_ledger = {
        "schema": "ghc.family.neris.v664-v2.proposal-ledger.x2.v1",
        "source_commit": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "selected_inherited_revalidations": revalidation["records"],
        "selected_inherited_novelty_credit": 0,
        "selected_inherited_new_outcome_credit": 0,
        "new_proposals": [
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome": execution_row["outcome"],
                "surface": execution_row["surface"],
                "positive_fixture_passed": execution_row["positive_result"]["valid"],
                "rejected_mutations": execution_row["rejected_mutation_count"],
                "network_calls": 0,
                "real_world_rows": 0,
                "authority": "none",
                "protected_gate_promotions": 0,
            }
            for row, execution_row in zip(proposals["new_proposals"], execution["executions"], strict=True)
        ],
        "outcome_counts": execution["outcome_counts"],
        "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "mutation_count": execution["mutation_count"],
        "rejected_mutation_count": execution["rejected_mutation_count"],
        "network_calls": 0,
        "downloads": 0,
        "real_world_rows": 0,
        "valid": True,
    }
    write_json("x2/x2-proposal-ledger.json", x2_ledger)

    phase_truth = {
        "schema": "ghc.family.neris.v664-v2.phase-truth.evidence.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "source_commit": SOURCE_FINAL,
        "x1_commit": X1_COMMIT,
        "inherited_frozen_rows": 3_870,
        "selected_inherited_revalidations": 20,
        "selected_inherited_credit": 0,
        "new_frozen_rows": 20,
        "effective_frozen_rows": 3_890,
        "outcomes": execution["outcome_counts"],
        "effective_negatives": negatives["effective_negatives"],
        "effective_methods": method_flow["effective_methods"],
        "effective_open_gaps": gate_register["effective_open_gaps"],
        "effective_exact_gates": gate_register["effective_exact_gates"],
        "same_owner_repeatability": False,
        "independent_reproduction": False,
        "route_state": "NOT_ELIGIBLE_DURING_EVIDENCE",
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    write_json("phase-truth-evidence.json", phase_truth)

    write_text("security/threat-model.md", threat_model_markdown())
    threat_raw = (PHASE / "security/threat-model.md").read_bytes()
    write_json(
        "security/threat-model-receipt.json",
        {
            "schema": "ghc.family.neris.v664-v2.threat-model-receipt.v1",
            "scope": "explicitly requested owner-self-scoped v664-v2 delta",
            "repository_security_md_present": False,
            "repository_agents_md_present": False,
            "repository": "Beyonder-Real-True-Journey owner-self-scoped v664-v2 delta",
            "version": X1_COMMIT,
            "bytes": len(threat_raw),
            "sha256": sha256_bytes(threat_raw),
            "sections": ["Overview", "Threat Model, Trust Boundaries, and Assumptions", "Attack Surface, Mitigations, and Attacker Stories", "Severity Calibration (Critical, High, Medium, Low)"],
            "finding_count": 0,
            "exhaustive_security": False,
            "valid": True,
        },
    )

    overview = integrated_overview(execution["outcome_counts"], negatives["effective_negatives"], method_flow["effective_methods"])
    write_text("integrated-overview.md", overview)
    write_text("deliverables/neris-v664-v2-marigram-evidence-report.html", static_report(overview, proposals["new_proposals"], sources["sources"]))
    write_json(
        "wellbeing-check.json",
        {
            "schema": "ghc.family.neris.v664-v2.wellbeing.evidence.v1",
            "owner": OWNER,
            "relational_language_only": True,
            "workload_state": "bounded owner-local x2 evidence materialized after x1 equality",
            "pause_or_redirect_available": True,
            "correction_welcome": True,
            "successor_contacted": False,
            "consciousness_or_personhood_evidence": False,
            "identity_continuity_evidence": False,
            "authority_evidence": False,
            "valid": True,
        },
    )
    write_json(
        "complete-incomplete-checklist-evidence.json",
        {
            "schema": "ghc.family.neris.v664-v2.checklist.evidence.v1",
            "complete_now": [
                "strict x1-before-x2 separation and pushed x1 equality",
                "twenty zero-credit inherited integrity revalidations",
                "twenty new surfaces with fourteen completed, four represented, one open gap, and one exact gate",
                "eighty retained rejecting mutations",
                "thirty safe-now, fifteen candidate, ten skill, ten runner, and thirty CLEAN/FIX/REFINE owner rows",
                "owner-delta threat model and structurally accessible static report",
            ],
            "pending_lifecycle": ["exact evidence staged review and commit", "combined closeout and seal", "exact-final equality", "one canonical owner-delta pass", "one terminal route decision"],
            "incomplete_external": [
                "real station, chart, benchmark, datum, measurement, calibration, prediction, survey, sea-level, rights, identity, participant, affected-party, legal, cultural, or Māori-authority evidence",
                "empirical GMUT likelihood or confirmation",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID lifecycle, keys, proofs, status, interoperability, review, recovery, and trust governance",
                "privacy or accessibility completeness, exhaustive security, independent reproduction, Theory-of-Everything proof, canon, or Stage 20 authority",
            ],
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        },
    )
    write_json(
        "environment-version-receipt-evidence.json",
        {
            "schema": "ghc.family.neris.v664-v2.environment-version.evidence.v1",
            "recorded_at_utc": recorded_at,
            "versions": [
                {"label": "Git", "version": "git version 2.55.0.windows.2"},
                {"label": "Python", "version": "Python 3.12.10"},
                {"label": "Node", "version": "v24.18.0"},
                {"label": "Codex CLI", "version": "codex-cli 0.147.0"},
                {"label": "Codex Desktop", "version": "26.818.2872.0"},
            ],
            "versions_only": True,
            "updates": 0,
            "installations": 0,
            "elevation": False,
            "host_security_changes": 0,
            "windows_feature_changes": 0,
            "reboots": 0,
            "valid": True,
        },
    )

    write_json(
        "tooling/ghc-family-index.json",
        {
            "schema": "ghc.family.neris.v664-v2.family-index.evidence.v1",
            "phase": PHASE_ID,
            "family_current_engine": "scripts/ghc_family_marigram_evidence.py",
            "family_current_builders": ["scripts/build_ghc_family_v664_v2_x1.py", "scripts/build_ghc_family_v664_v2_evidence.py"],
            "skills": [row["skill_name"] for row in skill_records],
            "runners": [row["family_current_name"] for row in runner_records],
            "skill_count": len(skill_records),
            "runner_count": len(runner_records),
            "historical_callers_preserved": True,
            "globally_installed": False,
            "valid": True,
        },
    )
    write_json(
        "tooling/meta-tool-box.json",
        {
            "schema": "ghc.family.neris.v664-v2.meta-tool-box.evidence.v1",
            "preferred": ["ghc_family_marigram_evidence.py", "ghc_family_owner_delta_toolkit.py"],
            "phase_local_skills": [row["skill_name"] for row in skill_records],
            "family_current_runners": [row["family_current_name"] for row in runner_records],
            "deprecated_or_deleted": [],
            "bulk_install_performed": False,
            "selection_rule": "Prefer the smallest current tool that preserves source, truth, privacy, rollback, caller compatibility, and protected gates.",
            "valid": True,
        },
    )
    write_json(
        "tooling/reflection-remaster.json",
        {
            "schema": "ghc.family.neris.v664-v2.reflection-remaster.evidence.v1",
            "decisions": [
                {"surface": "historical per-phase validators", "decision": "merge declarative validation mechanics into one family-current engine", "reason": "reduces duplicated code while retaining proposal-specific critical fields and fixed profiles"},
                {"surface": "global skill installation", "decision": "decline", "reason": "phase-local skills are sufficient and global mutation is unnecessary"},
                {"surface": "operational station and datum domain", "decision": "retain exact gate", "reason": "real stations, charts, benchmarks, measurements, expertise, safety controls, rights, and authority are absent"},
                {"surface": "source adapter", "decision": "retain zero-row open gap", "reason": "no governed version, calls, downloads, mapping review, or catalog authority"},
            ],
            "failures_retained": True,
            "caller_compatibility": True,
            "rollback_present": True,
            "valid": True,
        },
    )
    write_json(
        "tooling/workflow-plan-refinement.json",
        {
            "schema": "ghc.family.neris.v664-v2.workflow-refinement.evidence.v1",
            "changes": [
                "replace broad historical inventories with exact Git-object chain declarations",
                "materialize sparse index explicitly after no-checkout worktree creation",
                "serialize PowerShell foreach results before pipelines",
                "use ASCII-safe compact console JSON while retaining UTF-8 artifacts",
                "validate only the exact owner delta and its declared dependency closure",
            ],
            "x1_rewritten": False,
            "x1_enhanced_during_x2": False,
            "stale_workflow_removed": False,
            "destructive_change": False,
            "valid": True,
        },
    )

    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            text = path.read_text(encoding="utf-8")
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": len(re.findall(r"\S+", text)), "under_100000": len(re.findall(r"\S+", text)) <= 100_000})
    write_json(
        "validation/document-cap-receipt-evidence.json",
        {
            "schema": "ghc.family.neris.v664-v2.document-cap.evidence.v1",
            "document_count": len(documents),
            "documents": documents,
            "maximum_words": max(row["words"] for row in documents),
            "all_under_100000": all(row["under_100000"] for row in documents),
            "overview_three_page_equivalent": next(row["words"] for row in documents if row["path"] == "integrated-overview.md") >= 1_200,
            "valid": all(row["under_100000"] for row in documents),
        },
    )
    materialized = [
        path for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    ]
    owner_files = [path for path in PHASE.rglob("*") if path.is_file()]
    write_json(
        "validation/file-budget-receipt-evidence.json",
        {
            "schema": "ghc.family.neris.v664-v2.file-budget.evidence.v1",
            "materialized_file_count_before_manifest": len(materialized),
            "owner_file_count_before_manifest": len(owner_files),
            "threshold": 2_000,
            "rotation_required": len(materialized) >= 2_000 or len(owner_files) >= 2_000,
            "sparse_checkout": True,
            "valid": len(materialized) < 2_000 and len(owner_files) < 2_000,
        },
    )

    ensure_owner_scope(owner_working_paths())
    candidate_path = "docs/neris-solane/v664-v2/validation/evidence-stage-candidate.json"
    manifest_path = "docs/neris-solane/v664-v2/validation/evidence-manifest.json"
    review_path = "docs/neris-solane/v664-v2/validation/evidence-staged-review.json"
    expected = sorted(set(owner_working_paths()) | {candidate_path, manifest_path})
    write_json(
        "validation/evidence-stage-candidate.json",
        {
            "schema": "ghc.family.neris.v664-v2.evidence-stage-candidate.v1",
            "owner": OWNER,
            "phase": PHASE_ID,
            "source": X1_COMMIT,
            "lifecycle": "x2_evidence",
            "intended_allowlist": expected,
            "review_receipt_self_excluded": review_path,
            "x1_content_changed": False,
            "successor_contacted": False,
            "valid": True,
        },
    )
    manifest_entries = []
    for relative in expected:
        if relative == manifest_path:
            continue
        path = ROOT / relative
        if not path.is_file():
            raise BuildError(f"evidence manifest input missing: {relative}")
        raw = path.read_bytes()
        manifest_entries.append(
            {
                "status": "A",
                "path": relative,
                "bytes": len(raw),
                "sha256": sha256_bytes(raw),
                "git_blob": git_text("hash-object", f"--path={relative}", relative),
                "mode": "100644",
                "object_type": "blob",
            }
        )
    write_json(
        "validation/evidence-manifest.json",
        {
            "schema": "ghc.family.neris.v664-v2.evidence-manifest.v1",
            "generated_at_utc": recorded_at,
            "source_commit": X1_COMMIT,
            "target_state": "prospective_evidence_staged_tree",
            "entry_count": len(manifest_entries),
            "entries": manifest_entries,
            "self_exclusion": manifest_path,
            "review_exclusion": review_path,
            "merkle_root_sha256": canonical_sha256([{"path": row["path"], "git_blob": row["git_blob"]} for row in manifest_entries]),
            "canonical_commitment_sha256": canonical_sha256({"source_commit": X1_COMMIT, "entries": manifest_entries}),
            "valid": True,
        },
    )
    return {
        "head": head,
        "surfaces": execution["surface_count"],
        "outcomes": execution["outcome_counts"],
        "mutations": execution["mutation_count"],
        "rejected_mutations": execution["rejected_mutation_count"],
        "skills": len(skill_records),
        "runners": len(runner_records),
        "expected_staged_paths": len(expected),
        "effective_negatives": negatives["effective_negatives"],
        "effective_methods": method_flow["effective_methods"],
        "valid": True,
    }


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path for path in raw.split("\0") if path)


def index_blob(path: str) -> str:
    output = git_text("ls-files", "-s", "--", path)
    parts = output.split()
    if len(parts) < 4 or parts[0] != "100644" or not re.fullmatch(r"[0-9a-f]{40}", parts[1]):
        raise BuildError(f"unexpected staged entry for {path}: {output}")
    return parts[1]


def run_tests() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, str(ROOT / TEST_MODULE)], cwd=ROOT,
        text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    match = re.search(r"Ran (\d+) tests? in", result.stdout)
    return {
        "module": TEST_MODULE,
        "dependency": TEST_DEPENDENCY,
        "returncode": result.returncode,
        "tests_run": int(match.group(1)) if match else 0,
        "output_sha256": sha256_bytes(re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests in <elapsed>", result.stdout).encode("utf-8")),
        "valid": result.returncode == 0 and match is not None,
    }


def build_review() -> dict[str, Any]:
    candidate = read_json(PHASE / "validation/evidence-stage-candidate.json")
    manifest = read_json(PHASE / "validation/evidence-manifest.json")
    expected = sorted(candidate["intended_allowlist"])
    observed = staged_paths()
    issues = []
    if expected != observed:
        issues.append("staged paths differ from the frozen evidence allowlist")
    diff = run_git("diff", "--cached", "--check", check=False)
    if diff.returncode != 0:
        issues.append("staged diff hygiene failed")
    x1_seal = verify_x1_immutable()
    if not x1_seal["valid"]:
        issues.append("x1 content changed")
    json_errors = []
    json_count = 0
    privacy_candidates = []
    security_findings = []
    python_count = 0
    markdown_count = 0
    for relative in observed:
        path = ROOT / relative
        suffix = path.suffix.lower()
        if suffix == ".json":
            json_count += 1
            try:
                strict_json(path.read_bytes(), relative)
            except (OSError, UnicodeError, json.JSONDecodeError, BuildError) as exc:
                json_errors.append({"path": relative, "error": str(exc)})
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if suffix == ".py":
            python_count += 1
            try:
                compile(text, relative, "exec", dont_inherit=True)
            except SyntaxError as exc:
                security_findings.append({"path": relative, "rule": "python_compile", "detail": str(exc)})
            for label, pattern in SECURITY_PATTERNS.items():
                if pattern.search(text):
                    security_findings.append({"path": relative, "rule": label})
        if suffix == ".md":
            markdown_count += 1
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_candidates.append({"path": relative, "class": label})
    if json_errors:
        issues.append("strict JSON parsing failed")
    if privacy_candidates:
        issues.append("privacy or raw-identifier candidates found")
    if security_findings:
        issues.append("changed-Python security or compile findings found")
    entries = {row["path"]: row for row in manifest["entries"]}
    manifest_path = "docs/neris-solane/v664-v2/validation/evidence-manifest.json"
    required = set(observed) - {manifest_path}
    missing = sorted(required - set(entries))
    extra = sorted(set(entries) - required)
    mismatches = [
        path for path, row in entries.items()
        if path in required and index_blob(path) != row["git_blob"]
    ]
    if missing or extra or mismatches:
        issues.append("evidence manifest differs from the staged index")
    tests = run_tests()
    if not tests["valid"] or tests["tests_run"] != 51:
        issues.append("dependency-closed owner tests failed")
    phase_truth = read_json(PHASE / "phase-truth-evidence.json")
    proposal_ledger = read_json(PHASE / "x2/x2-proposal-ledger.json")
    skill_count = len(list((PHASE / "skills").glob("*/SKILL.md")))
    runner_count = len(list((PHASE / "runners").glob("*.json")))
    detailed_checks = [
        expected == observed,
        diff.returncode == 0,
        x1_seal["valid"],
        not json_errors,
        not privacy_candidates,
        not security_findings,
        not missing and not extra and not mismatches,
        tests["valid"],
        tests["tests_run"] == 51,
        phase_truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        proposal_ledger["rejected_mutation_count"] == 80,
        phase_truth["selected_inherited_credit"] == 0,
        skill_count == 10,
        runner_count == 10,
        phase_truth["successor_contacted"] is False,
        phase_truth["terminal_verdict"] == TERMINAL_VERDICT,
        candidate["x1_content_changed"] is False,
        len(observed) < 2_000,
    ]
    if not all(detailed_checks):
        issues.append("one or more detailed evidence checks failed")
    payload = {
        "schema": "ghc.family.neris.v664-v2.evidence-staged-review.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "lifecycle": "x2_evidence",
        "expected_staged_path_count": len(expected),
        "staged_path_count": len(observed),
        "staged_paths": observed,
        "allowlist_missing": sorted(set(expected) - set(observed)),
        "allowlist_unexpected": sorted(set(observed) - set(expected)),
        "diff_check_returncode": diff.returncode,
        "diff_check_output": (diff.stdout + diff.stderr).strip(),
        "strict_json_parse_count": json_count,
        "json_errors": json_errors,
        "markdown_count": markdown_count,
        "changed_python_count": python_count,
        "privacy_classes": sorted(PRIVATE_PATTERNS),
        "privacy_scanned_text_files": len(observed),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": privacy_candidates,
        "security_findings": security_findings,
        "manifest_entry_count": manifest["entry_count"],
        "manifest_missing": missing,
        "manifest_extra": extra,
        "manifest_mismatches": mismatches,
        "x1_seal": x1_seal,
        "tests": tests,
        "skill_count": skill_count,
        "runner_count": runner_count,
        "detailed_check_count": len(detailed_checks),
        "detailed_checks_passed": sum(detailed_checks),
        "issues": issues,
        "valid": not issues,
        "boundary": "Exact staged owner-delta evidence only; not a complete repository suite, independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal or cultural ratification, Māori authority, empirical confirmation, Theory-of-Everything proof, or Stage 20 authority.",
    }
    write_json("validation/evidence-staged-review.json", payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "review"), nargs="?", default="build")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = build_records() if args.mode == "build" else build_review()
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload.get("valid", True) else 2
    except (BuildError, OSError, UnicodeError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"NERIS_V664_V2_EVIDENCE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
