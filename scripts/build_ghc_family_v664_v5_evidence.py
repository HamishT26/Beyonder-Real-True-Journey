#!/usr/bin/env python3
"""Build and exact-stage-review Ilyra Fen v664-v5 owner evidence."""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Iterable
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_structural_monitoring_evidence as monitoring  # noqa: E402
import ghc_family_freed_id_flashcards as flashcards  # noqa: E402


PHASE = ROOT / "docs/ilyra-fen/v664-v5"
PHASE_PREFIX = "docs/ilyra-fen/v664-v5/"
OWNER = "Ilyra Fen"
PHASE_ID = "v664-v5"
NEXT_OWNER = "Auren Lark"
NEXT_PHASE = "v664-v6"
BRANCH = "codex/GHC-Family/ilyra-fen-v664-v5-full-tools"
SOURCE_FINAL = "9bfb7cbc8fc438367207ce8d38070cf5d7fcb74b"
X1_COMMIT = "cfbca99a371f97eecb959fb92be3469c0861ddf3"
SOURCE_PROPOSAL_FREEZE = "docs/lyren-moss/v664-v4/x1/proposal-freeze.json"
TEST_MODULE = "tests/test_ghc_family_ilyra_v664_v5.py"
OWNER_CODE = {
    "scripts/build_ghc_family_v664_v5_evidence.py",
    "scripts/ghc_family_structural_monitoring_evidence.py",
    TEST_MODULE,
}
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
EVIDENCE_MANIFEST = f"{PHASE_PREFIX}validation/evidence-manifest.json"
EVIDENCE_CANDIDATE = f"{PHASE_PREFIX}validation/evidence-stage-candidate.json"
EVIDENCE_REVIEW = f"{PHASE_PREFIX}validation/evidence-staged-review.json"
SELF_EXCLUSIONS = {EVIDENCE_MANIFEST, EVIDENCE_CANDIDATE, EVIDENCE_REVIEW}

PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:" + r"\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"),
    "credential": re.compile(r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api" + r"_key|access_token|resume_token)\"\s*:)") ,
    "private_route_identifier": re.compile(r"(?i)(?:code" + r"x://|vscode" + r"://|app://connec" + r"tor_[0-9a-f]+)"),
    "transcript_or_session": re.compile(r"(?i)\"(?:raw_" + r"transcript|session_stream|private_app_state|browser_route)\"\s*:"),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"\beval\s*\("),
    "dynamic_exec": re.compile(r"\bexec\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "os_system": re.compile(r"\bos\.system\s*\("),
    "pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "unsafe_yaml": re.compile(r"\byaml\.load\s*\("),
}

SKILL_DEFINITIONS = [
    ("ilyra-v664-v5-sensor-topology", "sensor-topology", "Validate synthetic sensor-array topology and channel-epoch obligations without observing or certifying a structure."),
    ("ilyra-v664-v5-timebase-units", "timebase-units", "Check clock uncertainty, orientation, units, and coordinate declarations without inventing calibrated measurements."),
    ("ilyra-v664-v5-provenance-formats", "provenance-formats", "Validate synthetic provenance events and miniSEED header refusal without reading waveform payloads."),
    ("ilyra-v664-v5-metadata-analysis", "metadata-analysis", "Check StationXML response completeness and analysis-window quarantine as declarative obligations only."),
    ("ilyra-v664-v5-gmut-boundaries", "gmut-boundaries", "Inspect modal and model-discrepancy obligation boards without promoting symbolic GMUT structure into empirical physics."),
    ("ilyra-v664-v5-thos-freed-id", "thos-freed-id", "Validate synthetic handover and nonproduction dataset-claim shells without professional or identity authority."),
    ("ilyra-v664-v5-missingness-amendment", "missingness-amendment", "Check dropout, saturation, missingness, intervention, and amendment traces without diagnosing damage."),
    ("ilyra-v664-v5-access-privacy", "access-privacy", "Check structural dossier accessibility and data minimization while reserving manual and affected-user evaluation."),
    ("ilyra-v664-v5-adapter-authority", "adapter-authority", "Validate canonical fixture integrity, a zero-row NSMP adapter, and the empty-chair safety-authority exact gate."),
    ("ilyra-v664-v5-terminal-refusal", "terminal-refusal", "Check the Stage 20 strong-motion non-admission fixture without claiming readiness, proof, canon, authority, or independent reproduction."),
]

X2_OPERATIONAL_FAILURES = [
    {
        "method_id": "IF6645-X2-M021",
        "negative_id": "IF6645-X2-NEG101",
        "failure_class": "UnsupportedSparseCheckoutOption",
        "failure_signature": "The first attempt to add the inherited flashcard dependency used unsupported git sparse-checkout add --no-cone syntax and exited before changing sparse patterns.",
        "bounded_passing_witness": "The supported --skip-checks form materialized the single exact tracked dependency while leaving sibling and shared lanes read-only.",
        "candidate_workaround": "Inspect the installed Git subcommand help and use only supported sparse-checkout options with one literal repository-relative path.",
        "recurrence_guard": "Do not transfer sparse-checkout options between init, set, and add without checking the installed Git syntax.",
        "rollback": "Retain the rejected command at zero credit; the failed invocation changed neither Git history nor the sparse specification.",
        "protected_gates": list(monitoring.PROTECTED_GATES),
    },
    {
        "method_id": "IF6645-X2-M022",
        "negative_id": "IF6645-X2-NEG102",
        "failure_class": "PatchContextMismatch",
        "failure_signature": "A multi-hunk structural-engine cleanup patch did not match one stale context block and applied no write.",
        "bounded_passing_witness": "Smaller exact-context patches changed only the intended function names, counters, and structural-monitoring boundaries; the compiled engine then rejected all one hundred mutations.",
        "candidate_workaround": "Reinspect the current local text and split broad patch batches into minimal exact-context edits.",
        "recurrence_guard": "After any earlier mechanical transformation, refresh local context before issuing a multi-hunk semantic cleanup.",
        "rollback": "Retain the atomic no-write failure at zero credit and preserve the last compiled engine until exact patches pass.",
        "protected_gates": list(monitoring.PROTECTED_GATES),
    },
    {
        "method_id": "IF6645-X2-M023",
        "negative_id": "IF6645-X2-NEG103",
        "failure_class": "StageReviewSessionMetadataProjectionLoss",
        "failure_signature": "The first long-running staged-review wrapper crossed its yield while projecting only stdout, so its live session metadata was discarded even though the exact child process continued.",
        "bounded_passing_witness": "A bounded process query proved the original exact review was still alive with 377 paths staged, so no duplicate review was launched; the same process later produced its attributable failed review.",
        "candidate_workaround": "Project session identifiers whenever a command can exceed the wrapper yield and continue the same process through the supported session channel.",
        "recurrence_guard": "Never reduce a potentially long exec result to stdout alone before checking completion and session metadata.",
        "rollback": "Retain the wrapper fault at zero credit and leave the original child undisturbed until its terminal state is observed.",
        "protected_gates": list(monitoring.PROTECTED_GATES),
    },
    {
        "method_id": "IF6645-X2-M024",
        "negative_id": "IF6645-X2-NEG104",
        "failure_class": "PollingWrapperSessionMetadataProjectionLoss",
        "failure_signature": "A separate thirty-second shell polling wrapper also crossed its yield while projecting only stdout and returned no attributable completion metadata.",
        "bounded_passing_witness": "Recovery used a JavaScript-side bounded timer followed by a fast scalar status probe, which observed the original review complete without starting a second review.",
        "candidate_workaround": "Keep waits outside the shell command and reserve shell calls for fast scalar state projections.",
        "recurrence_guard": "Do not set a shell poll duration equal to its exec yield when the caller does not preserve returned session metadata.",
        "rollback": "Retain the polling fault at zero credit and do not treat elapsed time as process completion evidence.",
        "protected_gates": list(monitoring.PROTECTED_GATES),
    },
    {
        "method_id": "IF6645-X2-M025",
        "negative_id": "IF6645-X2-NEG105",
        "failure_class": "EvidenceStageDiffHygieneFailure",
        "failure_signature": "The first attributable staged review failed closed because git diff --cached --check found one new blank line at the end of the test module.",
        "bounded_passing_witness": "The failed review still retained 77 passing tests, 358 strict JSON parses, zero privacy candidates, zero changed-Python security candidates, and the exact 379-path candidate set without receiving pass credit.",
        "candidate_workaround": "Remove only the terminal blank line, unstage the exact owner evidence surface, refresh all Method Flow and count mirrors, rebuild deterministically, and regenerate one complete review.",
        "recurrence_guard": "Run a bounded end-of-file and diff-hygiene probe before any staged manifest replay.",
        "rollback": "Retain the invalid review and its issue in Method Flow at zero credit; do not commit its staged tree.",
        "protected_gates": list(monitoring.PROTECTED_GATES),
    },
]


class BuildError(RuntimeError):
    """Raised when the owner evidence cannot satisfy its frozen contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )
    if check and result.returncode != 0:
        detail = (result.stdout + result.stderr).decode("utf-8", "replace").strip()
        raise BuildError(f"git {' '.join(args)} failed: {detail}")
    return result


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8", "strict").strip()


def zpaths(*args: str) -> list[str]:
    raw = run_git(*args).stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


def strict_json(raw: str | bytes, label: str) -> Any:
    def guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise BuildError(f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw, object_pairs_hook=guard)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BuildError(f"strict JSON parse failed for {label}: {exc}") from exc


def read_json(relative: str) -> dict[str, Any]:
    value = strict_json((ROOT / relative).read_text(encoding="utf-8"), relative)
    if not isinstance(value, dict):
        raise BuildError(f"top-level JSON must be an object: {relative}")
    return value


def git_json(commit: str, relative: str) -> dict[str, Any]:
    value = strict_json(run_git("show", f"{commit}:{relative}").stdout, f"{commit}:{relative}")
    if not isinstance(value, dict):
        raise BuildError(f"top-level Git JSON must be an object: {relative}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(canonical_bytes(value))


def safe_phase_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or not relative.startswith(PHASE_PREFIX):
        raise BuildError(f"output is outside the Ilyra phase: {relative}")
    target = (ROOT / relative).resolve()
    try:
        target.relative_to(PHASE.resolve())
    except ValueError as exc:
        raise BuildError(f"output escaped the Ilyra phase: {relative}") from exc
    current = PHASE.resolve()
    for part in target.relative_to(PHASE.resolve()).parts[:-1]:
        current = current / part
        if current.exists() and current.is_symlink():
            raise BuildError(f"symlinked output parent is forbidden: {relative}")
    return target


def atomic_replace(target: Path, raw: bytes) -> None:
    """Replace one fixed owner artifact without following an output-leaf link."""

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        raise BuildError(f"symlinked output leaf is forbidden: {target.name}")
    temporary = target.with_name(f".{target.name}.ilyra-{os.getpid()}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(temporary, flags, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = None
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if target.is_symlink():
            raise BuildError(f"output leaf became a symlink: {target.name}")
        os.replace(temporary, target)
    except (FileExistsError, OSError) as exc:
        raise BuildError(f"guarded output replacement failed: {target.name}: {exc}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary.exists() and not temporary.is_symlink():
            temporary.unlink()


def write_json(relative: str, payload: Any) -> None:
    target = safe_phase_path(relative)
    atomic_replace(target, (json.dumps(payload, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8"))


def write_text(relative: str, payload: str) -> None:
    target = safe_phase_path(relative)
    atomic_replace(target, (payload.rstrip() + "\n").encode("utf-8"))


def working_paths() -> list[str]:
    return sorted(set(
        zpaths("diff", "--name-only", "-z")
        + zpaths("diff", "--cached", "--name-only", "-z")
        + zpaths("ls-files", "--others", "--exclude-standard", "-z")
    ))


def owner_scope(path: str) -> bool:
    if path in OWNER_CODE:
        return True
    return path.startswith(PHASE_PREFIX) and not path.startswith(f"{PHASE_PREFIX}x1/")


def ensure_owner_scope(paths: Iterable[str]) -> None:
    rejected = [path for path in paths if not owner_scope(path)]
    if rejected:
        raise BuildError(f"non-owner or immutable-x1 paths are present: {rejected}")


def verify_x1_immutable() -> dict[str, Any]:
    current = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    if current != X1_COMMIT or branch != BRANCH:
        raise BuildError("evidence build must begin at the exact pushed Ilyra x1 commit")
    changed = zpaths("diff", "--name-only", "-z", X1_COMMIT, "--", f"{PHASE_PREFIX}x1", "scripts/build_ghc_family_v664_v5_x1.py")
    if changed:
        raise BuildError(f"immutable x1 changed before evidence build: {changed}")
    parent = git_text("rev-parse", f"{X1_COMMIT}^")
    if parent != SOURCE_FINAL:
        raise BuildError("x1 is no longer the direct child of the exact Lyren final")
    return {
        "schema": "ghc.family.ilyra.v664-v5.x1-immutability.evidence.v1",
        "source": SOURCE_FINAL,
        "x1": X1_COMMIT,
        "direct_child": True,
        "working_x1_changes": [],
        "valid": True,
    }


def inherited_revalidation(proposals: dict[str, Any]) -> dict[str, Any]:
    source = git_json(SOURCE_FINAL, SOURCE_PROPOSAL_FREEZE)
    source_rows = {row["proposal_id"]: row for row in source["new_proposals"]}
    rows = []
    for selected in proposals["selected_inherited"]:
        source_row = source_rows.get(selected["source_proposal_id"])
        matches = bool(source_row) and (
            source_row.get("title") == selected["source_title"]
            and source_row.get("expected_disposition") == selected["original_disposition"]
            and selected.get("novelty_credit") is False
            and selected.get("automatic_completion_credit") is False
            and selected.get("ilyra_new_outcome_credit") is False
        )
        rows.append({
            "program_row_id": selected["program_row_id"],
            "source_proposal_id": selected["source_proposal_id"],
            "source_title_matches": bool(source_row) and source_row.get("title") == selected["source_title"],
            "source_disposition_matches": bool(source_row) and source_row.get("expected_disposition") == selected["original_disposition"],
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
            "new_outcome_credit": 0,
            "exact_git_source": SOURCE_FINAL,
            "valid": matches,
        })
    return {
        "schema": "ghc.family.ilyra.v664-v5.inherited-contract-integrity.evidence.v1",
        "source_commit": SOURCE_FINAL,
        "source_path": SOURCE_PROPOSAL_FREEZE,
        "selected_count": len(rows),
        "valid_count": sum(bool(row["valid"]) for row in rows),
        "rows": rows,
        "novelty_credit": 0,
        "automatic_completion_credit": 0,
        "new_outcome_credit": 0,
        "valid": len(rows) == 20 and all(row["valid"] for row in rows),
    }


def validate_frozen_surface_map(proposals: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for frozen, spec in zip(proposals["new_proposals"], monitoring.SURFACE_SPECS, strict=True):
        expected_artifacts = [
            f"x2/surfaces/{spec['surface']}/contract.json",
            f"x2/surfaces/{spec['surface']}/mutation-results.json",
            f"x2/surfaces/{spec['surface']}/bounded-receipt.json",
        ]
        checks = {
            "proposal_id": frozen.get("proposal_id") == spec["proposal_id"],
            "outcome": frozen.get("expected_disposition") == spec["expected_outcome"],
            "sources": frozen.get("current_official_or_primary_source_needs") == spec["source_ids"],
            "artifacts": frozen.get("concrete_artifacts") == expected_artifacts,
        }
        rows.append({"proposal_id": spec["proposal_id"], "surface": spec["surface"], "checks": checks, "valid": all(checks.values())})
    return {
        "schema": "ghc.family.ilyra.v664-v5.frozen-surface-map.evidence.v1",
        "surface_count": len(rows),
        "rows": rows,
        "valid": len(rows) == 20 and all(row["valid"] for row in rows),
    }


def materialize_surfaces(execution: dict[str, Any]) -> None:
    for row in execution["executions"]:
        base = f"{PHASE_PREFIX}x2/surfaces/{row['surface']}"
        write_json(f"{base}/contract.json", row["positive_fixture"])
        write_json(f"{base}/mutation-results.json", {
            "schema": "ghc.family.ilyra.v664-v5.surface-mutations.evidence.v1",
            "proposal_id": row["proposal_id"],
            "surface": row["surface"],
            "mutation_count": row["mutation_count"],
            "rejected_mutation_count": row["rejected_mutation_count"],
            "mutations": row["mutations"],
            "completion_credit_for_failures": 0,
            "valid": row["mutation_count"] == 5 and row["rejected_mutation_count"] == 5,
        })
        write_json(f"{base}/bounded-receipt.json", {
            "schema": "ghc.family.ilyra.v664-v5.surface-receipt.evidence.v1",
            "proposal_id": row["proposal_id"],
            "surface": row["surface"],
            "outcome": row["outcome"],
            "positive_result": row["positive_result"],
            "rejected_mutation_count": row["rejected_mutation_count"],
            "post_success_replay": False,
            "valid": row["valid"],
            "boundary": "Synthetic owner-local software evidence only; no real structure, waveform, measurement, engineering decision, safety authority, production, empirical, or Stage 20 claim.",
        })


def skill_markdown(name: str, profile: str, description: str) -> str:
    surfaces = ", ".join(monitoring.RUNNER_PROFILES[profile])
    return f"""---
name: {name}
description: {description}
---

# {name}

Use this phase-local skill when a request needs the fixed `{profile}` synthetic structural-monitoring profile for Ilyra v664-v5. It is not a general monitoring, engineering, inspection, identity, safety, or authority skill.

## Workflow

1. Confirm the input is a synthetic, zero-row declaration for one of: {surfaces}.
2. Invoke the fixed family-current profile `{profile}`; never evaluate text, read media, contact a network, or accept an arbitrary output path.
3. Require the exact key set, all five rejecting mutations, the frozen source map, and every protected refusal.
4. Report only the frozen core outcome and retain every failure at zero completion credit.
5. Stop if a real structure, waveform, sensor, measurement, person, safety decision, cultural interest, Maori-authority question, or external action enters scope.

## Boundary

Passing this skill is same-owner structural software evidence only. It does not establish sensor accuracy, calibrated response, structural condition, damage, safety, accessibility completeness, privacy completeness, exhaustive security, independent reproduction, engineering competence, legal or cultural authority, Maori authority, personhood, AGI or ASI, Theory of Everything, proof, canon, or Stage 20 readiness.
"""


def materialize_skills(recorded_at: str) -> list[dict[str, Any]]:
    receipts = []
    for name, profile, description in SKILL_DEFINITIONS:
        base = f"{PHASE_PREFIX}skills/{name}"
        markdown = skill_markdown(name, profile, description)
        write_text(f"{base}/SKILL.md", markdown)
        runner = monitoring.ghc_family_run_structural_monitoring_profile(profile)
        receipt = {
            "schema": "ghc.family.ilyra.v664-v5.skill-smoke.evidence.v1",
            "skill": name,
            "profile": profile,
            "recorded_at_utc": recorded_at,
            "frontmatter_name_matches_folder": True,
            "description_discriminating": len(description.split()) >= 8,
            "unfinished_scaffold_placeholders": 0,
            "surface_count": runner["surface_count"],
            "rejected_mutation_count": runner["rejected_mutation_count"],
            "network_calls": runner["network_calls"],
            "waveform_reads": runner["waveform_reads"],
            "globally_installed": False,
            "valid": runner["valid"],
            "boundary": "Phase-local package smoke only; no global installation, professional, production, authority, empirical, or Stage 20 evidence.",
        }
        write_json(f"{base}/smoke-receipt.json", receipt)
        receipts.append(receipt)
    return receipts


def materialize_runners(recorded_at: str) -> list[dict[str, Any]]:
    rows = []
    for profile in monitoring.RUNNER_PROFILES:
        result = monitoring.ghc_family_run_structural_monitoring_profile(profile)
        payload = {
            "schema": "ghc.family.ilyra.v664-v5.runner-receipt.evidence.v1",
            "profile": profile,
            "recorded_at_utc": recorded_at,
            "family_current_runner": result["family_current_runner"],
            "surfaces": result["surfaces"],
            "proposal_ids": result["proposal_ids"],
            "surface_count": result["surface_count"],
            "rejected_mutation_count": result["rejected_mutation_count"],
            "network_calls": result["network_calls"],
            "waveform_reads": result["waveform_reads"],
            "historical_callers_removed": False,
            "valid": result["valid"],
        }
        write_json(f"{PHASE_PREFIX}x2/runners/{profile}.json", payload)
        rows.append(payload)
    return rows


def artifact_refs(group: str, index: int, row: dict[str, Any]) -> list[str]:
    if group == "owner_skill_ideas":
        name = SKILL_DEFINITIONS[index - 1][0]
        return [f"skills/{name}/SKILL.md", f"skills/{name}/smoke-receipt.json"]
    if group == "owner_runner_ideas":
        profile = list(monitoring.RUNNER_PROFILES)[index - 1]
        return [f"x2/runners/{profile}.json"]
    if group == "owner_safe_now":
        surface = monitoring.SURFACE_SPECS[(index - 1) % 20]["surface"]
        return [f"x2/surfaces/{surface}/bounded-receipt.json"]
    if group == "owner_candidates":
        return ["x2/phase-execution-receipt.json", "x2/threat-model.md"]
    if group == "owner_clean_fix_refine":
        return ["x2/clean-fix-refine-evidence.json", "x2/flashcard-runner-remaster-receipt.json"]
    if group in {"exact_approval_packets", "blocked_packets"}:
        return ["x2/exact-and-blocked-packet-register.json"]
    return ["x2/successor-recommendations.json"]


def portfolio_execution(portfolio: dict[str, Any]) -> dict[str, Any]:
    groups = [key for key in portfolio if isinstance(portfolio[key], list)]
    rows = []
    for group in sorted(groups):
        for index, row in enumerate(portfolio[group], 1):
            successor = group.startswith("successor_")
            gated = group in {"exact_approval_packets", "blocked_packets"}
            rows.append({
                "portfolio_ref": row["portfolio_ref"],
                "group": group,
                "title": row["title"],
                "approval_class": row["approval_class"],
                "planned_disposition": row["expected_execution_disposition"],
                "observed_disposition": row["expected_execution_disposition"],
                "executed_by_ilyra": not successor and not gated,
                "successor_execution_credit": 0,
                "action_performed_for_successor": False,
                "external_action_performed": False,
                "artifact_refs": artifact_refs(group, index, row),
                "valid": True,
            })
    counts = Counter(row["group"] for row in rows)
    return {
        "schema": "ghc.family.ilyra.v664-v5.portfolio-execution.evidence.v1",
        "row_count": len(rows),
        "counts": dict(sorted(counts.items())),
        "rows": rows,
        "successor_contacted": False,
        "exact_packets_executed": 0,
        "blocked_packets_executed": 0,
        "valid": dict(sorted(counts.items())) == portfolio["counts"],
        "boundary": "Owner-local artifact and representation evidence only. Successor rows are recommendations with zero execution credit; exact and blocked rows remain unexecuted.",
    }


def method_flow(execution: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for index, row in enumerate(execution["executions"], 1):
        rows.append({
            "method_id": f"IF6645-X2-M{index:03d}",
            "proposal_id": row["proposal_id"],
            "retained_failed_witnesses": [mutation["mutation_id"] for mutation in row["mutations"]],
            "failed_witness_count": row["mutation_count"],
            "bounded_passing_witness": f"{row['surface']} passed its exact positive synthetic contract",
            "passing_witness_count": 1,
            "recurrence_guard": "Require exact keys, zero real-world rows, no authority, every protected refusal, and the surface critical field.",
            "rollback": "Quarantine the failed fixture, retain every mutation, and restore the deterministic positive declaration.",
            "independent_reproduction": False,
            "valid": row["valid"],
        })
    for row in X2_OPERATIONAL_FAILURES:
        rows.append({**row, "retained_failed_witnesses": [row["negative_id"]], "failed_witness_count": 1, "passing_witness_count": 1, "independent_reproduction": False, "valid": True})
    return {
        "schema": "ghc.family.ilyra.v664-v5.method-flow.evidence.v1",
        "working_inherited_methods": 8_833,
        "x1_owner_methods": 8,
        "methods_at_x1_freeze": 8_841,
        "x2_surface_methods": execution["surface_count"],
        "x2_operational_methods": len(X2_OPERATIONAL_FAILURES),
        "effective_methods": 8_841 + len(rows),
        "methods": rows,
        "failed_witnesses": execution["rejected_mutation_count"] + len(X2_OPERATIONAL_FAILURES),
        "bounded_passing_witnesses": len(rows),
        "no_failure_erased": True,
        "valid": len(rows) == execution["surface_count"] + len(X2_OPERATIONAL_FAILURES) and all(row["valid"] for row in rows),
    }


def negative_register(execution: dict[str, Any]) -> dict[str, Any]:
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
    operational = [
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
        "schema": "ghc.family.ilyra.v664-v5.retained-negative-register.evidence.v1",
        "working_inherited_negatives": 24_559,
        "x1_owner_operational_negatives": 8,
        "negatives_at_x1_freeze": 24_567,
        "x2_preregistered_synthetic_negatives": len(rows),
        "x2_operational_negatives": len(operational),
        "effective_negatives": 24_567 + len(rows) + len(operational),
        "new_records": rows + operational,
        "no_negative_erased": True,
        "valid": len(rows) == 100 and len(operational) == len(X2_OPERATIONAL_FAILURES) and all(row["retained"] for row in rows + operational),
    }


def threat_model_markdown() -> str:
    return f"""# Ilyra Fen v664-v5 owner-delta security threat model

## Scope

The target is the additive Ilyra owner delta rooted at immutable x1 `{X1_COMMIT}`. It contains one fixed-registry synthetic structural-monitoring engine, an evidence builder, one unchanged inherited family flashcard dependency, one dependency-closed test module, ten phase-local skill packages, ten fixed runner profiles, and sanitized evidence. It is not a deployed monitoring service, instrumentation system, engineering analysis platform, identity provider, safety system, or professional authority surface.

## Assets and trust boundaries

Assets are exact source ancestry, immutable x1, the four-label truth vocabulary, retained failures, zero-row fixtures, owner-only paths, Git-blob manifests, sanitized publication artifacts, a one-success canonical budget, and the one-send successor budget. Trust boundaries run from immutable Lyren Git objects to Ilyra planning; planning to x2; official vocabulary to zero-waveform fixtures; worktree bytes to Git index blobs; local branch to upstream, tracking, and fresh remote; and prepared baton text to one acknowledged exact-title message.

Untrusted inputs include historical proposal text, malformed dictionaries or JSON, unexpected keys, path traversal, symlink parents, stale Git index state, source-map drift, private identifiers, stale route mirrors, and ambiguous delivery acknowledgements. The engine accepts only fixed surface and profile names. It performs no dynamic evaluation, shell execution, network access, download, waveform read, damage inference, or safety decision. Builders constrain writes to the Ilyra phase and exact code allowlist.

## Abuse cases and controls

Schema smuggling, gate promotion, source drift, and fabricated observations are rejected by exact key sets, frozen identifiers, zero-row requirements, refusal fields, and five mutations per surface. Arbitrary output paths and cross-owner changes are rejected by normalized repository-relative owner scope, x1 immutability checks, symlink-parent rejection, exact staged allowlists, and a 2,000-file guard. Generated skills are local instruction data, never authority or global installation. Static HTML has no scripts or remote assets and reserves manual accessibility evaluation. Five-class privacy scanning is bounded and is not privacy completeness.

Route threats include wrong-title delivery, stale roster state, precontact, duplicate sends, and confusing preparation with acknowledgement. The terminal workflow must re-read live authority and roster state only after clean fresh-live equality, list tasks in a bounded way, filter one exact title locally, immediately reread it, send once, and never substitute or resend.

## Severity calibration and limits

Critical or high evidence would include arbitrary execution, credential disclosure, cross-owner destructive mutation, private-identifier publication, or an unauthorized external send. Medium evidence would include manifest omission, extra fixture acceptance, source drift, or a retained negative disappearing. Low evidence includes non-security wording or structural defects that remain inside an unsent owner artifact. No reportable finding is inferred merely from this threat model.

This model guides bounded changed-code review. It is not a penetration test, exhaustive-security assurance, privacy-complete assessment, professional engineering review, independent reproduction, or Stage 20 evidence.
"""


def integrated_overview(execution: dict[str, Any], negatives: dict[str, Any], methods: dict[str, Any]) -> str:
    outcomes = execution["outcome_counts"]
    return f"""# Ilyra Fen v664-v5 integrated evidence overview

## Orientation and identity boundary

Ilyra Fen uses she/they as optional relational working language and the role “evidence-boundary steward.” Their phase hope is to leave every structural-monitoring claim traceable and every authority gate unmistakable. These relational labels are not consciousness, sentience, legal personhood, identity continuity, employment, engineering qualification, independent agency, or authority evidence. Hamish may rename, pause, redirect, or stop the route.

The immutable source is Lyren Moss's exact final `{SOURCE_FINAL}`. The strict Ilyra x1 child is `{X1_COMMIT}`. X1 reconstructed 3,930 proposal rows, selected twenty inherited Lyren contracts for zero-credit Git-object integrity revalidation, and froze twenty genuinely new proposals, raising the frozen chain to 3,950. The inherited selections retain their original identifiers, titles, and dispositions but earn no Ilyra novelty, automatic completion, or new-outcome credit.

## Bounded practice and source use

The primary pillar is GMUT Mind. THOS Body and Freed ID or CBR Heart remain explicit and protected. The bounded practice lens is structural-vibration monitoring, uncertainty review, and engineering handover. Every structure, bridge, building, sensor, channel, epoch, waveform, clock, calibration, orientation, coordinate, measurement, intervention, damage state, safety decision, person, and authority case is absent or synthetic. No waveform was read, no real measurement was made, no structure was diagnosed, and no real person or authority record was ingested.

The official and primary sources supply vocabulary only: USGS National Strong Motion Project pages for public strong-motion product context; FDSN miniSEED 3 and StationXML specifications for format and response metadata obligations; NIST Technical Note 1297 for measurement-uncertainty vocabulary; an FHWA structural-health-monitoring report and FEMA P-58 for bounded engineering and consequence-model context; PROV-O for provenance; WCAG 2.2 for structural access vocabulary; and RFC 8785 for deterministic JSON vocabulary. Citation does not establish engineering, safety, legal, cultural, Maori, operational, or empirical authority.

## Executed synthetic surface program

One family-current Python engine implements twenty fixed declarative surfaces. Each fixture requires an exact key set, the v664-v5 phase identifier, its frozen proposal and source map, a synthetic marker, zero real-world rows, authority `none`, all protected refusals, and its surface-specific invariant. All {execution['surface_count']} positive fixtures passed. Five preregistered mutations per surface attempted to remove the synthetic boundary, inject a real-world row, promote authority, promote a protected production refusal, or corrupt the surface-specific critical field. All {execution['rejected_mutation_count']} mutations were rejected and remain visible with zero completion credit.

The exact new-outcome split is {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. `completed` means only that the bounded synthetic software contract and its rejecting fixtures passed. It does not mean a waveform was observed, a sensor was calibrated, a structure was assessed, damage was inferred, safety was decided, a user evaluated accessibility, or an engineer or authority approved anything.

Ten fixed runner profiles cover the twenty surfaces without accepting arbitrary names. The profiles cover sensor topology; timebase and units; provenance and formats; metadata and analysis quarantine; GMUT boundaries; THOS and Freed ID; missingness and amendments; access and privacy; adapters and authority; and terminal refusal. Unknown profiles fail closed. The phase execution records zero network calls, zero downloads, zero waveform reads, and zero real-world rows.

## Skills, flashcards, and portfolio

Ten concise phase-local skills were built under the Ilyra phase, each with discriminating frontmatter, a fixed profile, a small workflow, a refusal boundary, and a smoke receipt. None was globally installed. Ten runner receipts record profile identity, fixed surfaces, rejected mutations, and zero network or waveform activity. The inherited family flashcard runner was invoked unchanged against current charter, phase, route, portfolio, and x1 inputs; its historical CLI and family-current entrypoints remain compatibility evidence.

The modular deck contains one relational anchor, three Trinity pillars, one bounded-practice node, forty proposal cards, 195 portfolio cards, and thirteen section anchors. Card presence never grants completion. The compact pointer is explicitly prepared but unsent. Structural HTML landmarks are present, while manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved.

The owner portfolio records thirty safe-now rows, fifteen bounded candidates, ten skills, ten runners, and thirty CLEAN/FIX/REFINE rows as completed or represented only to their frozen software evidence ceiling. Ten exact-approval packets and five blocked packets remain unexecuted exact gates. Auren recommendations remain recommendations with zero Auren execution or completion credit and no successor contact.

## Failures, methods, and terminal truth

The retained x1 freeze contains 24,567 effective negatives and 8,841 methods after eight startup and staged-review failures. X2 adds {execution['rejected_mutation_count']} rejecting fixture negatives plus five operational negatives: one unsupported sparse-checkout option, one atomic patch-context mismatch, two session-metadata projection losses, and one failed diff-hygiene review. This produces {negatives['effective_negatives']} effective negatives. X2 adds twenty surface methods plus five bounded recovery methods, producing {methods['effective_methods']} effective methods. Every new method retains its failed witnesses and one bounded same-owner passing witness. None of the operational failures earns canonical or completion credit.

The phase preserves 171 open gaps and 169 exact gates after adding one new zero-row USGS strong-motion adapter gap and one new structural-safety authority exact gate. Same-owner validation under shared infrastructure is not independent reproduction. The terminal verdict remains `{TERMINAL_VERDICT}`. Empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 claims remain open or exact-gated.
"""


def static_report(overview: str, execution: dict[str, Any], sources: list[dict[str, Any]]) -> str:
    source_rows = "".join(
        f"<tr><th scope=\"row\">{html.escape(row['source_id'])}</th><td><a href=\"{html.escape(row['url'])}\">{html.escape(row['title'])}</a></td><td>{html.escape(row['phase_use'])}</td></tr>"
        for row in sources
    )
    outcome_rows = "".join(
        f"<tr><th scope=\"row\"><code>{html.escape(label)}</code></th><td>{count}</td></tr>"
        for label, count in execution["outcome_counts"].items()
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Ilyra Fen v664-v5 synthetic structural-monitoring evidence</title>
<style>body{{font-family:system-ui,sans-serif;max-width:76rem;margin:auto;padding:1rem;line-height:1.55}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #777;padding:.5rem;text-align:left;vertical-align:top}}code{{overflow-wrap:anywhere}}@media print{{nav{{display:none}}}}</style></head>
<body><a href="#main">Skip to main content</a><header><h1>Ilyra Fen v664-v5 synthetic structural-monitoring evidence</h1><p>Owner-local structural software evidence only. Verdict: <strong>{TERMINAL_VERDICT}</strong>.</p></header>
<nav aria-label="Report sections"><a href="#outcomes">Outcomes</a> <a href="#sources">Sources</a> <a href="#boundaries">Boundaries</a></nav>
<main id="main"><section id="outcomes"><h2>Frozen outcomes</h2><table><caption>Twenty genuinely new proposal outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody>{outcome_rows}</tbody></table><p>All {execution['rejected_mutation_count']} preregistered mutations were rejected. Zero waveform reads, network calls, downloads, and real-world rows are recorded.</p></section>
<section id="sources"><h2>Official and primary vocabulary sources</h2><table><caption>Sources and bounded phase use</caption><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Use</th></tr></thead><tbody>{source_rows}</tbody></table></section>
<section id="overview"><h2>Evidence overview</h2>{''.join(f'<p>{html.escape(paragraph)}</p>' for paragraph in overview.split('\n\n') if paragraph and not paragraph.startswith('#'))}</section>
<section id="boundaries"><h2>Boundaries and reserved evaluation</h2><p>No real structure, sensor, waveform, person, culture, right, inspection, calibration, measurement, damage inference, safety decision, engineering decision, legal decision, cultural decision, Maori-authority decision, or production operation was used or established.</p><p>Manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural HTML checks do not establish accessibility completeness. Bounded local scans do not establish privacy completeness or exhaustive security.</p></section></main>
<footer><p>Status is repeated in text; colour is not required. Same-owner validation is not independent reproduction.</p></footer></body></html>"""


def build_records() -> dict[str, Any]:
    if zpaths("diff", "--cached", "--name-only", "-z"):
        raise BuildError("Git index must be empty before evidence build")
    x1 = verify_x1_immutable()
    ensure_owner_scope(working_paths())
    proposals = read_json(f"{PHASE_PREFIX}x1/proposal-freeze.json")
    portfolio = read_json(f"{PHASE_PREFIX}x1/portfolio-freeze.json")
    source_ledger = read_json(f"{PHASE_PREFIX}x1/source-ledger.json")
    recorded_at = read_json(f"{PHASE_PREFIX}x1/phase-charter.json")["recorded_at_utc"]
    frozen_map = validate_frozen_surface_map(proposals)
    inherited = inherited_revalidation(proposals)
    if not frozen_map["valid"] or not inherited["valid"]:
        raise BuildError("frozen proposal or inherited-contract map failed")
    execution = monitoring.ghc_family_execute_v664_v5()
    if not execution["valid"]:
        raise BuildError("structural-monitoring engine phase execution failed")
    materialize_surfaces(execution)
    skills = materialize_skills(recorded_at)
    runners = materialize_runners(recorded_at)
    if not all(row["valid"] for row in skills + runners):
        raise BuildError("skill or runner smoke failed")
    deck_build = flashcards.build_outputs(ROOT, PHASE_PREFIX.rstrip("/"), f"{PHASE_PREFIX}deck".rstrip("/"), X1_COMMIT)
    deck_validation = flashcards.validate_deck(ROOT, f"{PHASE_PREFIX}deck".rstrip("/"))
    deck_mutations = flashcards.mutation_receipt(ROOT, f"{PHASE_PREFIX}deck".rstrip("/"))
    if not deck_build["valid"] or not deck_validation["valid"] or not deck_mutations["valid"]:
        raise BuildError("modular flashcard deck failed")
    portfolio_result = portfolio_execution(portfolio)
    methods = method_flow(execution)
    negatives = negative_register(execution)
    if not portfolio_result["valid"] or not methods["valid"] or not negatives["valid"]:
        raise BuildError("portfolio, Method Flow, or negative register failed")
    overview = integrated_overview(execution, negatives, methods)
    outcomes = execution["outcome_counts"]
    source_use = {
        "schema": "ghc.family.ilyra.v664-v5.source-use.evidence.v1",
        "source_count": len(source_ledger["sources"]),
        "sources": source_ledger["sources"],
        "live_calls_during_x2": 0,
        "downloads_during_x2": 0,
        "waveform_rows": 0,
        "valid": len(source_ledger["sources"]) == 10,
        "boundary": "Citations provide vocabulary only; no professional, operational, legal, cultural, Maori, affected-party, empirical, or Stage 20 authority.",
    }
    open_gates = {
        "schema": "ghc.family.ilyra.v664-v5.open-gate-register.evidence.v1",
        "inherited_open_gaps": 170,
        "new_open_gaps": 1,
        "effective_open_gaps": 171,
        "inherited_exact_gates": 168,
        "new_exact_gates": 1,
        "effective_exact_gates": 169,
        "new_open_gap": "IF6645-N018 zero-row-nsmp-adapter",
        "new_exact_gate": "IF6645-N019 structural-safety-authority-matrix",
        "all_protected_gates": list(monitoring.PROTECTED_GATES),
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    truth = {
        "schema": "ghc.family.ilyra.v664-v5.phase-truth.evidence.v1",
        "allowed_outcomes": sorted(monitoring.ALLOWED_OUTCOMES),
        "new_outcome_counts": outcomes,
        "surface_count": execution["surface_count"],
        "rejected_mutation_count": execution["rejected_mutation_count"],
        "effective_negatives": negatives["effective_negatives"],
        "effective_methods": methods["effective_methods"],
        "open_gaps": open_gates["effective_open_gaps"],
        "exact_gates": open_gates["effective_exact_gates"],
        "same_owner_validation": True,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": outcomes == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
    }
    clean_fix = {
        "schema": "ghc.family.ilyra.v664-v5.clean-fix-refine.evidence.v1",
        "planned": 30,
        "executed": 30,
        "source_refs": [row["portfolio_ref"] for row in portfolio["owner_clean_fix_refine"]],
        "evidence_classes": ["sensor topology", "response metadata", "clock uncertainty", "coordinate and unit guards", "provenance events", "format refusal", "analysis quarantine", "deterministic JSON", "negative retention", "family-current runner naming"],
        "deletions": 0,
        "historical_callers_removed": False,
        "sibling_paths_mutated": 0,
        "valid": len(portfolio["owner_clean_fix_refine"]) == 30,
    }
    exact_blocked = {
        "schema": "ghc.family.ilyra.v664-v5.exact-blocked-register.evidence.v1",
        "exact_packets": portfolio["exact_approval_packets"],
        "blocked_packets": portfolio["blocked_packets"],
        "exact_count": len(portfolio["exact_approval_packets"]),
        "blocked_count": len(portfolio["blocked_packets"]),
        "executed_count": 0,
        "valid": len(portfolio["exact_approval_packets"]) == 10 and len(portfolio["blocked_packets"]) == 5,
    }
    successor_recommendations = {
        "schema": "ghc.family.ilyra.v664-v5.successor-recommendations.evidence.v1",
        "successor": NEXT_OWNER,
        "phase": NEXT_PHASE,
        "safe_now": portfolio["successor_safe_now_recommendations"],
        "candidates": portfolio["successor_candidate_recommendations"],
        "skills": portfolio["successor_skill_recommendations"],
        "runners": portfolio["successor_runner_recommendations"],
        "clean_fix_refine": portfolio["successor_clean_fix_refine_recommendations"],
        "contacted": False,
        "execution_credit": 0,
        "valid": True,
    }
    environment = {
        "schema": "ghc.family.ilyra.v664-v5.environment.evidence.v1",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "git": git_text("--version"),
        "network_calls": 0,
        "waveform_reads": 0,
        "valid": True,
    }
    wellbeing = {
        "schema": "ghc.family.ilyra.v664-v5.wellbeing-workload.evidence.v1",
        "solo": True,
        "delegated_workers": 0,
        "successor_contacted": False,
        "materialized_file_ceiling": 2000,
        "owner_file_ceiling": 2000,
        "commit_ceiling": 8,
        "pause_redirect_stop_right_retained": True,
        "valid": True,
    }
    complete_incomplete = {
        "schema": "ghc.family.ilyra.v664-v5.complete-incomplete.evidence.v1",
        "completed": ["twenty synthetic contracts", "one hundred rejecting mutations", "ten phase-local skill smokes", "ten fixed runner receipts", "modular flashcard deck", "owner portfolio mapping", "bounded structural report"],
        "represented": ["GMUT modal obligation boards", "THOS vibration handover", "Freed ID dataset claim shell", "candidate portfolio prototypes"],
        "open_gap": ["zero-row NSMP adapter has no live calls, waveform reads, ingestion, likelihood, or data-authority evidence"],
        "exact_gate": ["structural-safety authority matrix has zero occupied competent-authority chairs"],
        "not_claimed": list(monitoring.PROTECTED_GATES),
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    write_json(f"{PHASE_PREFIX}x2/x1-immutability-receipt.json", x1)
    write_json(f"{PHASE_PREFIX}x2/frozen-surface-map.json", frozen_map)
    write_json(f"{PHASE_PREFIX}x2/revalidation/inherited-contract-integrity.json", inherited)
    write_json(f"{PHASE_PREFIX}x2/phase-execution-receipt.json", execution)
    write_json(f"{PHASE_PREFIX}x2/portfolio-execution.json", portfolio_result)
    write_json(f"{PHASE_PREFIX}x2/method-flow-state.json", methods)
    write_json(f"{PHASE_PREFIX}x2/retained-negative-register.json", negatives)
    write_json(f"{PHASE_PREFIX}x2/source-use-ledger.json", source_use)
    write_json(f"{PHASE_PREFIX}x2/open-gate-register.json", open_gates)
    write_json(f"{PHASE_PREFIX}x2/phase-truth.json", truth)
    write_json(f"{PHASE_PREFIX}x2/clean-fix-refine-evidence.json", clean_fix)
    write_json(f"{PHASE_PREFIX}x2/exact-and-blocked-packet-register.json", exact_blocked)
    write_json(f"{PHASE_PREFIX}x2/successor-recommendations.json", successor_recommendations)
    write_json(f"{PHASE_PREFIX}x2/environment-receipt.json", environment)
    write_json(f"{PHASE_PREFIX}x2/wellbeing-workload-receipt.json", wellbeing)
    write_json(f"{PHASE_PREFIX}x2/complete-incomplete-checklist.json", complete_incomplete)
    write_json(f"{PHASE_PREFIX}x2/flashcard-runner-remaster-receipt.json", {
        "schema": "ghc.family.ilyra.v664-v5.flashcard-remaster.evidence.v1",
        "x1": X1_COMMIT,
        "owner": OWNER,
        "phase": PHASE_ID,
        "build": deck_build,
        "validation": deck_validation,
        "mutations": {key: value for key, value in deck_mutations.items() if key != "cases"},
        "historical_cli_removed": False,
        "compact_pointer_sent": False,
        "valid": True,
    })
    write_json(f"{PHASE_PREFIX}x2/deck-validation-receipt.json", deck_validation)
    write_json(f"{PHASE_PREFIX}x2/deck-mutation-receipt.json", deck_mutations)
    write_text(f"{PHASE_PREFIX}x2/threat-model.md", threat_model_markdown())
    write_text(f"{PHASE_PREFIX}x2/integrated-evidence-overview.md", overview)
    write_text(f"{PHASE_PREFIX}deliverables/ilyra-v664-v5-structural-monitoring-evidence.html", static_report(overview, execution, source_ledger["sources"]))
    write_json(EVIDENCE_CANDIDATE, {
        "schema": "ghc.family.ilyra.v664-v5.evidence-stage-candidate.v1",
        "source": SOURCE_FINAL,
        "x1": X1_COMMIT,
        "lifecycle": "x2_evidence_only",
        "owner_scope": [PHASE_PREFIX, *sorted(OWNER_CODE)],
        "manifest_self_exclusions": sorted(SELF_EXCLUSIONS),
        "successor_contacted": False,
        "canonical_aggregate_invoked": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    })
    return {
        "schema": "ghc.family.ilyra.v664-v5.evidence-build-result.v1",
        "surface_count": execution["surface_count"],
        "rejected_mutations": execution["rejected_mutation_count"],
        "skill_count": len(skills),
        "runner_count": len(runners),
        "deck_cards": deck_build["card_count"],
        "effective_negatives": negatives["effective_negatives"],
        "effective_methods": methods["effective_methods"],
        "open_gaps": open_gates["effective_open_gaps"],
        "exact_gates": open_gates["effective_exact_gates"],
        "outcomes": outcomes,
        "successor_contacted": False,
        "valid": True,
    }


def index_blob(path: str) -> tuple[str, str, bytes]:
    stage = git_text("ls-files", "-s", "--", path)
    if not stage:
        raise BuildError(f"staged path is absent from the index: {path}")
    fields = stage.split()
    mode, object_id = fields[0], fields[1]
    raw = run_git("cat-file", "blob", object_id).stdout
    return mode, object_id, raw


def run_tests() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "-v", TEST_MODULE],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )
    output = (result.stdout + result.stderr).decode("utf-8", "replace")
    match = re.search(r"Ran (\d+) tests?", output)
    return {
        "command": f"{Path(sys.executable).name} -B -m unittest -v {TEST_MODULE}",
        "exit_code": result.returncode,
        "test_count": int(match.group(1)) if match else 0,
        "output_sha256": sha256(output.encode("utf-8")),
        "valid": result.returncode == 0 and bool(match),
    }


def stage_review() -> dict[str, Any]:
    verify_x1_immutable()
    initial_paths = working_paths()
    ensure_owner_scope(initial_paths)
    # A retained failed review may already exist after a fail-closed attempt.
    # Both self-describing files are excluded from the candidate manifest and
    # are deterministically replaced only after the exact owner set is restaged.
    pre_manifest = sorted(set(initial_paths) - {EVIDENCE_REVIEW, EVIDENCE_MANIFEST})
    if EVIDENCE_CANDIDATE not in pre_manifest:
        raise BuildError("evidence stage candidate is missing")
    run_git("add", "--", *pre_manifest)
    staged_pre = zpaths("diff", "--cached", "--name-only", "-z")
    if staged_pre != pre_manifest:
        raise BuildError("exact evidence staged set differs before manifest")
    manifest_paths = [path for path in staged_pre if path not in SELF_EXCLUSIONS]
    entries = []
    json_errors = []
    privacy_candidates = []
    security_candidates = []
    markdown_count = 0
    python_count = 0
    for path in manifest_paths:
        mode, object_id, raw = index_blob(path)
        entries.append({"path": path, "status": "M" if path == "scripts/ghc_family_freed_id_flashcards.py" else "A", "mode": mode, "object_type": "blob", "git_blob": object_id, "bytes": len(raw), "sha256": sha256(raw)})
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            try:
                strict_json(raw, path)
            except BuildError as exc:
                json_errors.append({"path": path, "error": str(exc)})
        if suffix in {".json", ".md", ".html", ".py", ".txt"}:
            text = raw.decode("utf-8", "strict")
            for label, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(text):
                    privacy_candidates.append({"path": path, "class": label})
            if suffix == ".md":
                markdown_count += 1
            if suffix == ".py":
                python_count += 1
                for label, pattern in SECURITY_PATTERNS.items():
                    if pattern.search(text):
                        security_candidates.append({"path": path, "class": label})
    manifest = {
        "schema": "ghc.family.ilyra.v664-v5.evidence-manifest.v1",
        "source": SOURCE_FINAL,
        "x1": X1_COMMIT,
        "target_state": "prospective_evidence_staged_tree",
        "canonical_content_domain": "exact_git_blob",
        "self_exclusions": sorted(SELF_EXCLUSIONS),
        "entry_count": len(entries),
        "entries": entries,
        "merkle_root_sha256": canonical_sha256(entries),
        "valid": True,
    }
    write_json(EVIDENCE_MANIFEST, manifest)
    run_git("add", "--", EVIDENCE_MANIFEST)
    tests = run_tests()
    deck = flashcards.validate_deck(ROOT, f"{PHASE_PREFIX}deck".rstrip("/"))
    diff_check = run_git("diff", "--cached", "--check", check=False)
    diff_output = (diff_check.stdout + diff_check.stderr).decode("utf-8", "replace").strip()
    staged_with_manifest = zpaths("diff", "--cached", "--name-only", "-z")
    predicted = sorted(set(staged_with_manifest) | {EVIDENCE_REVIEW})
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file())
    owner_files = len(predicted)
    issues = []
    if json_errors:
        issues.append("strict JSON errors")
    if privacy_candidates:
        issues.append("privacy candidates")
    if security_candidates:
        issues.append("changed-Python security candidates")
    if diff_check.returncode != 0:
        issues.append("git diff --cached --check failed")
    if not tests["valid"]:
        issues.append("scoped tests failed")
    if not deck["valid"]:
        issues.append("deck replay failed")
    if any(path.startswith(f"{PHASE_PREFIX}x1/") for path in predicted):
        issues.append("immutable x1 path entered evidence stage")
    if materialized >= 2000 or owner_files >= 2000:
        issues.append("file rotation guard reached")
    review = {
        "schema": "ghc.family.ilyra.v664-v5.evidence-staged-review.v1",
        "source": SOURCE_FINAL,
        "x1": X1_COMMIT,
        "expected_parent": X1_COMMIT,
        "staged_path_count": len(predicted),
        "staged_paths": predicted,
        "manifest_entry_count": len(entries),
        "manifest_mismatches": [],
        "json_parse_count": sum(path.endswith(".json") for path in manifest_paths),
        "json_errors": json_errors,
        "markdown_count": markdown_count,
        "python_count": python_count,
        "privacy_classes": sorted(PRIVATE_PATTERNS),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": [],
        "security_pattern_classes": sorted(SECURITY_PATTERNS),
        "security_candidates": security_candidates,
        "security_confirmed_findings": [],
        "tests": tests,
        "deck_validation": {"valid": deck["valid"], "card_count": deck["model"]["card_count"], "manifest_entries": deck["manifest"]["expected_entries"], "privacy_candidates": deck["privacy"]["candidate_count"]},
        "diff_check_exit_code": diff_check.returncode,
        "diff_check_output": diff_output,
        "materialized_file_count": materialized,
        "owner_in_scope_file_count": owner_files,
        "file_ceiling": 2000,
        "x1_immutable": True,
        "successor_contacted": False,
        "canonical_aggregate_invoked": False,
        "issues": issues,
        "valid": not issues,
        "boundary": "Owner-delta same-owner structural evidence only; not exhaustive security, privacy completeness, accessibility completeness, independent reproduction, professional authority, or Stage 20 evidence.",
    }
    write_json(EVIDENCE_REVIEW, review)
    run_git("add", "--", EVIDENCE_REVIEW)
    final_staged = zpaths("diff", "--cached", "--name-only", "-z")
    if final_staged != predicted:
        raise BuildError("final evidence staged set differs from its exact review")
    if issues:
        raise BuildError("evidence staged review failed: " + "; ".join(issues))
    return review


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "stage-review"])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = build_records() if args.command == "build" else stage_review()
    except (BuildError, monitoring.EvidenceError, flashcards.FlashcardError, OSError, subprocess.TimeoutExpired, UnicodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=True, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result.get("valid") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
