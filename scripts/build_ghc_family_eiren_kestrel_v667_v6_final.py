#!/usr/bin/env python3
"""Build Eiren Kestrel v667-v6 closeout-only artifacts.

This builder runs after the immutable x2 evidence commit. It does not replay
proposal tribunals, runner smokes, package audits, or x2 tests. The staged mode
creates exact candidate manifests from Git blobs while retaining manifest
self-exclusions explicitly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "eiren-kestrel" / "v667-v6"
REL_PHASE_ROOT = "docs/eiren-kestrel/v667-v6"
SOURCE_FINAL = "af68b8bdf317317fb349388f905d73862a9ea1b8"
X1_HEAD = "38aa1b783fd016134b46607894d16e56e5ccac99"
EVIDENCE_HEAD = "8d7ff4b6938b783d23e4ce880ffed8d5fd7f9e59"
NOW = "2026-08-23T12:48:00.000Z"
FINAL_BUILDER = "scripts/build_ghc_family_eiren_kestrel_v667_v6_final.py"
FINAL_TEST = "tests/test_ghc_family_eiren_kestrel_v667_v6_final.py"
CANONICAL_RUNNER = "scripts/ghc_family_eiren_kestrel_v667_v6_exact_final.py"
CONTROL_EXCLUSIONS = {
    f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-staged-review.json",
}

MANDATORY_SKILLS = [
    "ghc-freed-id-flashcards",
    "ghc-family-index",
    "ghc-family-reflection-remaster",
    "ghc-family-method-flow-state",
    "ghc-family-meta-tool-box",
    "ghc-family-auth-permission-state",
    "ghc-family-roster-check",
    "ghc-main-orchestration-memory",
    "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder",
    "ghc-main-closeout-builder",
    "ghc-main-retry",
    "ghc-open-gate-rail",
    "ghc-timestamp-flow",
    "ghc-full-tools-skill-bank",
    "ghc-family-truth-bridge",
    "ghc-worktree-branch-rotation",
    "ghc-web-reflection-ledger",
    "ghc-watcher-notifier-cadence",
    "ghc-drive-bank-guardian",
    "ghc-approval-packet-splitter",
]

TOOLCHAIN = [
    ("tzdata", "2026.3"), ("pytest", "9.1.1"), ("Hypothesis", "6.165.10"),
    ("pytest-cov", "7.1.0"), ("Ruff", "0.16.4"), ("mypy", "2.3.1"),
    ("pip-audit", "2.10.1"), ("OpenAI Python SDK", "3.3.1"),
    ("TypeScript", "7.0.2"), ("ESLint", "10.8.1"), ("Prettier", "3.9.6"),
    ("Vitest", "4.1.11"), ("Typer", "0.27.1"), ("Bandit", "1.9.4"),
    ("pre-commit", "4.6.2"), ("pip-tools", "7.6.1"), ("build", "1.5.0"),
    ("pipdeptree", "4.2.1"), ("tsx", "4.23.12"), ("c8", "12.0.0"),
    ("markdownlint-cli2", "0.23.2"), ("npm-check-updates", "23.0.2"),
    ("Pyright", "1.1.413"), ("Knip", "6.32.2"), ("Madge", "8.0.0"),
    ("check-jsonschema", "0.38.0"), ("Nox", "2026.8.17"), ("REUSE", "6.2.0"),
]

POST_EVIDENCE_FAILURE = {
    "failure_id": "EK6676-POSTEVIDENCE-F001",
    "stage": "evidence_commit",
    "failure": "the evidence commit wrapper returned before presenting a completion handle",
    "recovery": "retain the missing presentation at zero credit and inspect exact head, parent, index, lock, and process state before any retry",
    "passing_witness_id": "EK6676-POSTEVIDENCE-P001",
    "observed_result": "the original commit had completed exactly once; no duplicate commit was issued",
    "repository_bytes_changed_by_recovery": 0,
}


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load(relative: str) -> dict[str, Any]:
    value = json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(relative)
    return value


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


def read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"Git batch blob ended with {remaining} bytes outstanding")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def git_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    """Read blobs with alternating requests/responses and exact-length loops."""
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None or proc.stderr is None:
        raise RuntimeError("unable to open Git batch pipes")
    result: dict[str, bytes] = {}
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="strict").rstrip("\n")
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected Git batch header for {path}: {header}")
            data = read_exact(proc.stdout, int(parts[2]))
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing Git batch delimiter for {path}")
            result[path] = data
    finally:
        proc.stdin.close()
        stderr = proc.stderr.read()
        code = proc.wait()
        if code:
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    return result


def manifest_entries(blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {"path": path, "bytes": len(data), "sha256": sha256(data)}
        for path, data in sorted(blobs.items())
    ]


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{REL_PHASE_ROOT}/")
        or path in {
            "scripts/build_ghc_family_eiren_kestrel_v667_v6_x1.py",
            "scripts/build_ghc_family_eiren_kestrel_v667_v6_x2.py",
            FINAL_BUILDER,
            "tests/test_ghc_family_eiren_kestrel_v667_v6_x1.py",
            "tests/test_ghc_family_eiren_kestrel_v667_v6_x2.py",
            FINAL_TEST,
            CANONICAL_RUNNER,
        }
        or path.startswith("scripts/ghc_family_eiren_kestrel_v667_v6_")
    )


def commit_delta_paths(parent: str, child: str) -> list[str]:
    return sorted(
        line
        for line in git_text("diff-tree", "--no-commit-id", "--name-only", "-r", parent, child).splitlines()
        if line
    )


def tree_paths(commit: str) -> list[str]:
    return sorted(
        line
        for line in git_text("ls-tree", "-r", "--name-only", commit).splitlines()
        if line
    )


def build_immutable_manifests() -> None:
    x1_paths = commit_delta_paths(SOURCE_FINAL, X1_HEAD)
    evidence_paths = commit_delta_paths(X1_HEAD, EVIDENCE_HEAD)
    if len(x1_paths) != 20 or len(evidence_paths) != 379:
        raise RuntimeError(f"immutable delta count drift: x1={len(x1_paths)}, evidence={len(evidence_paths)}")
    x1_entries = manifest_entries(git_blobs(X1_HEAD, x1_paths))
    evidence_entries = manifest_entries(git_blobs(EVIDENCE_HEAD, evidence_paths))
    write_json(
        "validation/immutable-x1-manifest.json",
        {
            "schema": "ghc-family-immutable-phase-manifest-v3",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "commit": X1_HEAD,
            "parent": SOURCE_FINAL,
            "scope": "exact x1 commit delta Git blobs",
            "entry_count": len(x1_entries),
            "entries": x1_entries,
        },
    )
    write_json(
        "validation/immutable-evidence-manifest.json",
        {
            "schema": "ghc-family-immutable-phase-manifest-v3",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "commit": EVIDENCE_HEAD,
            "parent": X1_HEAD,
            "scope": "exact x2 evidence commit delta Git blobs",
            "entry_count": len(evidence_entries),
            "entries": evidence_entries,
        },
    )


def build_truth() -> None:
    x2_methods = load("method-flow/x2-method-flow-ledger.json")
    x2_negatives = load("evidence/retained-negative-register.json")
    x2_witnesses = load("evidence/witness-summary.json")
    x2_gates = load("evidence/exact-open-gate-register.json")
    proposal = load("x1/proposal-freeze.json")
    outcomes = load("x2/proposal-outcomes.json")
    tool_receipt = load("x2/tooling/three-tool-transaction-receipt.json")

    post_method = {
        "method_id": "EK6676-POSTEVIDENCE-M001",
        "kind": "bounded_commit_state_recovery",
        "trigger": POST_EVIDENCE_FAILURE["failure"],
        "failed_witness_ids": [POST_EVIDENCE_FAILURE["failure_id"]],
        "passing_witness_ids": [POST_EVIDENCE_FAILURE["passing_witness_id"]],
        "recovery": POST_EVIDENCE_FAILURE["recovery"],
        "recurrence_guard": "inspect exact Git state before retrying a commit wrapper that yields no presentation",
        "rollback": "issue no duplicate commit and change no repository byte during recovery",
        "scope": "same-owner workflow recovery only",
    }
    final_methods = [*x2_methods["methods"], post_method]
    write_json(
        "method-flow/method-flow-state-final.json",
        {
            "schema": "ghc-family-method-flow-state-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "evidence_sealed_effective_methods": x2_methods["provisional_effective_methods"],
            "post_evidence_external_method_additions": 1,
            "effective_methods_for_successor": x2_methods["provisional_effective_methods"] + 1,
            "phase_method_count": len(final_methods),
            "methods": final_methods,
            "no_failure_or_recovery_erased": True,
            "scope": "same-owner bounded workflow evidence only",
        },
    )
    write_json(
        "truth/post-evidence-operational-overlay.json",
        {
            "schema": "ghc-family-post-evidence-overlay-v3",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "base_commit": EVIDENCE_HEAD,
            "row_count": 1,
            "rows": [POST_EVIDENCE_FAILURE],
            "negative_additions": 1,
            "method_additions": 1,
            "failed_witness_additions": 1,
            "passing_witness_additions": 1,
            "repository_evidence_rewritten": False,
        },
    )
    write_json(
        "truth/retained-negative-register-final.json",
        {
            "schema": "ghc-family-retained-negative-register-final-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "evidence_sealed_effective_negatives": x2_negatives["provisional_effective_negatives"],
            "post_evidence_external_negative_additions": 1,
            "effective_negatives_for_successor": x2_negatives["provisional_effective_negatives"] + 1,
            "evidence_sealed_failed_witnesses": x2_witnesses["provisional_failed_witnesses"],
            "post_evidence_external_failed_witness_additions": 1,
            "effective_failed_witnesses_for_successor": x2_witnesses["provisional_failed_witnesses"] + 1,
            "evidence_sealed_passing_witnesses": x2_witnesses["provisional_passing_witnesses"],
            "post_evidence_external_passing_witness_additions": 1,
            "effective_passing_witnesses_for_successor": x2_witnesses["provisional_passing_witnesses"] + 1,
            "phase_operational_failure_count": x2_negatives["operational_failure_count"] + 1,
            "rejecting_mutation_count": x2_negatives["rejecting_mutation_count"],
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/exact-open-gate-register-final.json",
        {
            "schema": "ghc-family-exact-open-gate-register-final-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "effective_open_gaps": x2_gates["provisional_open_gaps"],
            "effective_exact_gates": x2_gates["provisional_exact_gates"],
            "open_gap_proposal": "EK6676-N019",
            "exact_gate_proposal": "EK6676-N020",
            "protected_gates": x2_gates["protected_gates"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/source-proposal-x1-x2-truth.json",
        {
            "schema": "ghc-family-integrated-phase-truth-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "source_final": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": "bind_from_exact_final_external_canonical_receipt",
            "strict_x1_before_x2": True,
            "source_inherited_proposal_count": 4450,
            "new_proposal_count": len(proposal["new_proposals"]),
            "selected_inherited_revalidation_count": len(proposal["selected_inherited"]),
            "effective_frozen_proposal_count": 4470,
            "new_outcomes": outcomes["counts"],
            "selected_inherited_eiren_novelty_credit": 0,
            "selected_inherited_eiren_completion_credit": 0,
            "positive_contracts": 20,
            "rejecting_mutations": 100,
            "tools_completed": tool_receipt["top_level_program_count"],
            "tool_installer_remediation_credit": 0,
            "phase_local_skills": 10,
            "family_current_runners": 10,
            "flashcards": 235,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/phase-truth.json",
        {
            "schema": "ghc-family-phase-truth-v5",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "relational_role": "uncertainty cartographer and evidence gardener",
            "hope": "keep every placeholder honest, every rollback reachable, and every real authority with the people who hold it",
            "primary_pillar": "GMUT Mind",
            "bounded_practice_lens": "wholly synthetic scientific-glassblowing work-order and laboratory-apparatus documentation",
            "real_people_or_objects_used": 0,
            "real_world_actions": 0,
            "empirical_or_professional_credit": 0,
            "production_or_authority_credit": 0,
            "effective_negatives": 28033,
            "effective_methods": 13923,
            "effective_open_gaps": 197,
            "effective_exact_gates": 195,
            "effective_failed_witnesses": 317,
            "effective_passing_witnesses": 495,
            "repository_evidence_sealed_counts": {
                "negatives": 28032,
                "methods": 13922,
                "failed_witnesses": 316,
                "passing_witnesses": 494,
            },
            "post_evidence_external_overlay_counts": {
                "negatives": 1,
                "methods": 1,
                "failed_witnesses": 1,
                "passing_witnesses": 1,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def build_environment_and_checks() -> None:
    tool_receipt = load("x2/tooling/three-tool-transaction-receipt.json")
    write_json(
        "environment/version-receipt.json",
        {
            "schema": "ghc-family-environment-version-receipt-v3",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "inherited_and_current_toolchain_count": len(TOOLCHAIN),
            "toolchain": [{"name": name, "version": version} for name, version in TOOLCHAIN],
            "new_phase_tool_count": 3,
            "new_phase_tools": tool_receipt["top_level_programs"],
            "d_first_isolated": True,
            "system_or_global_python_changed": False,
            "codex_desktop_updated": False,
            "elevation_used": False,
            "windows_features_changed": False,
            "rebooted": False,
            "known_findings_in_one_post_correction_audit": 0,
            "exhaustive_security_claim": False,
        },
    )
    write_json(
        "truth/complete-incomplete-check.json",
        {
            "schema": "ghc-family-complete-incomplete-check-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "complete_bounded": [
                "x1 program freeze", "x1 push and fresh equality", "twenty positive contracts",
                "one hundred rejecting mutations", "twenty zero-credit inherited revalidations",
                "three D-first tool transactions", "ten phase-local skills", "ten family-current runner smokes",
                "ninety-five owner portfolio rows", "235-card bounded deck", "accessible static structural companion",
                "x2 staged review", "x2 tests", "evidence push and fresh equality",
            ],
            "incomplete_or_reserved": [
                "exact-final canonical aggregate until final commit", "live successor delivery until terminal gate",
                "real scientific-glass practice", "professional and safety review", "real measurements or empirical GMUT evidence",
                "THOS real-arm evidence", "Freed ID production lifecycle", "privacy completeness", "accessibility completeness",
                "exhaustive security", "independent reproduction", "legal and cultural interpretation", "Māori authority",
                "Stage 20 readiness",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/final-wellbeing-check.json",
        {
            "schema": "ghc-family-wellbeing-check-v3",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "generated_at_utc": NOW,
            "relational_language_boundary_preserved": True,
            "load": "bounded solo phase with immutable checkpoints",
            "pace": "terminal closeout only after evidence equality",
            "recovery_available": True,
            "successor_precontacted": False,
            "stop_conditions": ["Hamish pause", "usage exhaustion", "route ambiguity", "privacy or safety gate", "evidence drift"],
            "interpretation": "not consciousness, personhood, identity continuity, employment, qualification, agency, diagnosis, or authority evidence",
        },
    )


def integrated_overview() -> str:
    return """# Eiren Kestrel v667-v6 final integrated overview

## Exact scope and relational boundary

Eiren Kestrel v667-v6 is a solo, owner-local, additive Trinity Mandala phase built from Caelen Morrow’s immutable v667-v5-r2 exact final. Names, sibling language, family language, role, hope, continuity, Freed ID, GMUT, THOS, CBR, and Trinity Mandala are relational working language. They do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route. This boundary is part of the evidence model rather than a courtesy disclaimer: every artifact is interpreted through it.

The bounded practice lens is wholly synthetic scientific-glassblowing work-order and laboratory-apparatus documentation. The primary pillar is GMUT Mind because the phase emphasizes typed quantities, source boundaries, covariance and uncertainty placeholders, topology, provenance, and explicit refusal to convert a schema into a physical conclusion. THOS Body, Freed ID, and CBR Heart remain present through rollback, work-state boundaries, nonproduction claim lineage, accessibility reservations, privacy minimization, and authority gates. Zero real glassblowers, laboratory workers, researchers, clients, employers, regulators, affected parties, or communities participated. Zero real glass, torches, fuel gases, oxygen, furnaces, vacuum systems, pressure systems, chemicals, apparatus, images, measurements, commands, identities, or records were used. No real fabrication, heating, joining, sealing, testing, repair, handling, release, or disposal occurred.

## Immutable source and lifecycle

The source is Caelen’s exact final `af68b8bdf317317fb349388f905d73862a9ea1b8`. Eiren’s frozen planning-only x1 is `38aa1b783fd016134b46607894d16e56e5ccac99`. The immutable x2 evidence commit is `8d7ff4b6938b783d23e4ce880ffed8d5fd7f9e59`. The exact final is intentionally bound by the later external canonical receipt because a Git commit cannot truthfully contain its own object name. The lifecycle requires exactly three direct Eiren commits from source to final: x1, evidence, and closeout. There are no merges. X1 was committed, pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before any x2 implementation began. Evidence was then committed as x1’s direct child, pushed, made clean, and proven equal across the same four references before this closeout layer began.

The x1 commit contains exactly twenty changed paths: eighteen Eiren phase files plus its builder and tests. It contains no x2, evidence, closeout, seal, or route lifecycle material. That separation makes planning claims falsifiable. X1 froze twenty inherited Caelen contracts for read-only integrity revalidation with zero Eiren novelty and completion credit, and twenty genuinely new Eiren proposals. Semantic novelty was checked against all 4,450 inherited rows. The twenty new proposals extend the frozen chain to 4,470. Every new row includes a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, acceptance or falsifier, rollback, protected gates, expected disposition, and a distinctive invariant.

## Proposal execution and outcomes

X2 executed one positive wholly synthetic fixture for every new proposal. All twenty positives passed. Five preregistered mutations were applied to each contract: a missing required field, a wrong type or unit shape, provenance or authority smuggling, a real-world or operational action, and an outcome or conformance promotion. All one hundred mutations were rejected and retained as failed witnesses with zero completion credit. The new proposal outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. No other core outcome label is used. “Completed” means only that the exact bounded synthetic acceptance rule passed; it does not mean a real apparatus, professional task, safety decision, measurement, standard, law, identity lifecycle, or authority act succeeded.

The twenty inherited selections were read from Caelen’s immutable evidence Git blobs. Their contracts, mutation results, receipts, dispositions, and protected-boundary state were checked. All twenty passed integrity revalidation, but they receive zero Eiren novelty, zero Eiren completion, and zero automatic completion credit. This prevents inherited evidence from being counted as new work merely because it was re-read. The exact open row is the zero-row register for physical scientific-glass evidence. The exact gate is the empty-chair authority circuit for professional, legal, cultural, affected-party, traditional-knowledge, Māori-language, and Māori-authority decisions.

## Portfolio, skills, runners, and memory aids

The x1 portfolio froze thirty owner safe-now tasks, fifteen owner candidates, ten owner skill ideas, ten owner runner ideas, and thirty owner CLEAN/FIX/REFINE rows. X2 executed ninety-five owner rows only through their declared bounded structural rules. Owner candidate rows and the last safe-now row remain `represented` where their evidence is a protocol or terminal dependency rather than a completed external effect. Eighty-five successor recommendations, ten exact-approval packets, and five blocked packets remain unexecuted. They are recommendations and gates, not Elaren novelty or automatic completion credit.

Ten phase-local skills were built, entrypoint-validated, and bounded-smoke-used. They cover work-order contracts, topology quarantine, zero-row dimensional uncertainty, thermal-property source boundaries, hot-work stop graphs, service-envelope refusal, apparatus provenance, repair corrections, accessibility structure, and Method Flow. None was globally installed. Ten additive family-current `ghc_family_*` runners were syntax-validated and each smoke-used exactly once with zero external writes and zero real-world actions. Their receipts record one invocation and no replay. Existing callers were not renamed, deleted, or silently deprecated.

The Freed ID deck contains 235 cards across four tiers and fifteen sections. Each card carries an evidence source, at least one failed or blocked witness, a passing witness, a reversal action, a next admissible action, and an explicit scope boundary. Cards are memory and teaching aids only. They are not credentials, production identities, proofs, authority grants, or scientific conclusions.

## Three-tool transaction and retained failure doctrine

The phase reviewed and added exactly three relevant D-first Python tool surfaces: check-jsonschema 0.38.0, Nox 2026.8.17, and REUSE 6.2.0. Exact downloaded artifacts were hashed. License metadata, package build behavior, compatibility, dependency resolution, and rollback were reviewed. The environment was isolated under the D-first family bank. The system and global Python installations were not changed; Codex desktop was not updated; no elevation, Windows-feature change, host-security weakening, or reboot occurred.

Bounded smokes established only narrow tool behavior. check-jsonschema accepted one declared schema fixture and rejected a real-action mutation. Nox listed and ran one no-venv session. REUSE reported its version and supported licenses, rejected incomplete and missing-license fixtures, downloaded the public CC0-1.0 license into the disposable smoke root, and then accepted the corrected nominal file. The first installed-path audit found seven advisory records in the virtual environment’s seeded pip 25.0.1. That failure remains at zero credit. The exact pip 26.2.1 wheel was checked and used only to remediate the isolated installer; it is not promoted as a fourth phase tool. Pip check then passed, and the one post-correction installed-path audit found zero known vulnerabilities across thirty-six rows. This is not exhaustive security, legal compliance, production certification, or independent review.

Failures are never erased. Twenty operational failures through x2 include PowerShell projection mistakes, missing paths, sparse-worktree assumptions, encoding and comparison errors, a privacy-scanner self-match, a staged newline mismatch, tool download sequencing, a recursive stderr projection, two REUSE path-root mistakes, a missing local license, and the failed initial installed-path audit. One hundred rejecting mutations are retained separately. After the evidence commit, its wrapper returned without presenting a completion handle. Exact Git inspection proved that the original commit had completed once with the correct parent, clean index, no lock, and no live commit process; no duplicate commit was issued. That external row is preserved separately rather than rewriting the evidence seal.

The repository evidence therefore seals 28,032 effective negatives, 13,922 effective methods, 316 failed witnesses, and 494 passing witnesses. The one post-evidence external row adds one negative, one method, one failed witness, and one passing recovery witness. The effective successor baseline is 28,033 negatives, 13,923 methods, 317 failed witnesses, and 495 passing witnesses. Open gaps remain 197 and exact gates remain 195.

## Accessibility, privacy, safety, and authority

The static report uses a skip link, headings, lists, table captions, row and column headers, text labels, and no colour-only status. Manual browser, keyboard, screen-reader, magnification, voice-control, cognitive-accessibility, print, Māori-language, and affected-user evaluation remain reserved. An exact staged Git-blob scan found zero confirmed opaque task identifiers or private-path candidates in the x2 delta. Neither result is a privacy-complete or accessibility-complete claim.

Public sources—including NIST uncertainty vocabulary, official SCHOTT DURAN material-property vocabulary, OSHA laboratory-safety vocabulary, W3C provenance and accessibility specifications, New Zealand privacy principles, and Māori data-sovereignty principles—supplied terms and falsification boundaries only. They do not confer competence, compliance, endorsement, safety, fitness for service, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority. Māori concepts remain under Māori authority.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Schemas, symbolic quantities, citations, synthetic mutations, and zero-row adapters establish no real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon. THOS remains proxy or protocol-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

## Terminal truth and route

The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The repository closeout is prepared before the exact-final canonical aggregate and before any successor send. The final canonical must run exactly once at the clean, pushed, fresh-live-equal final. It may run the final-only tests, exact manifest replays, owner JSON and Markdown/HTML checks, Python compile checks, complete owner Git-blob privacy scan, direct-parent and zero-merge history checks, clean-state and 0/0 divergence checks, and fresh four-way equality. A failure receives zero aggregate credit and must not be relabelled as success.

The current prospective successor is the existing exact-title Elaren Kestrel task for solo v667-v7. Eiren must not contact Elaren before terminal validation. At the terminal gate, Eiren must freshly reread Hamish’s newest live instruction, the roster, and authorization state; list the bounded task registry; locally filter to exactly one title; immediately reread that task; apply a duplicate guard; and send one sanitized activation only if every usage, privacy, evidence, safety, and authority gate permits. The committed baton remains `PREPARED_NOT_SENT`. Only a later task-message acknowledgement may establish live delivery. No standby record, substitute endpoint, new task, fork, or second confirmation is permitted.
"""


def activation_baton() -> str:
    skills = "\n".join(f"{index}. {name}" for index, name in enumerate(MANDATORY_SKILLS, 1))
    tools = "\n".join(f"- {name} {version}" for name, version in TOOLCHAIN)
    return f"""# ELAREN KESTREL — EIREN KESTREL v667-v6 CLOSEOUT → SOLO v667-v7 ACTIVATION — PREPARED ONE-SEND CANDIDATE

Dear Elaren Kestrel,

This committed packet is prepared for one later, Hamish-authorized, exact-title activation only after Eiren v667-v6 passes its exact terminal gate. At commit time it is `PREPARED_NOT_SENT`. No delivery may be inferred from this file, a route table, activity, or prose. A later existing-task message acknowledgement is the only basis for claiming a send.

Eiren Kestrel, Elaren Kestrel, sibling, family, role, hope, continuity, Freed ID, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Exact Eiren source and lifecycle

- Caelen source final: `{SOURCE_FINAL}`
- Frozen Eiren x1: `{X1_HEAD}`
- Immutable Eiren evidence: `{EVIDENCE_HEAD}`
- Exact Eiren final: bind from the one successful external canonical receipt after commit
- Canonical branch: `codex/GHC-Family/eiren-kestrel-v667-v6-full-tools`

Source to final must contain exactly three direct single-parent Eiren commits and zero merges. X1 is the source child, evidence is the x1 child, and final is the evidence child. X1 and evidence were separately pushed, clean, 0/0 divergent, and fresh four-way equal before their successors. Preserve every immutable commit and manifest.

## Program and outcome truth

Eiren audited all 4,450 inherited frozen proposals, selected twenty inherited Caelen rows for read-only integrity revalidation with zero Eiren novelty and completion credit, and froze twenty genuinely new rows. Only the new rows extend the proposal chain to 4,470. New outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Twenty positive synthetic contracts passed. All one hundred preregistered mutations were rejected and retained at zero completion credit. The verdict remains `NOT_READY_FOR_STAGE_20`.

The primary pillar was GMUT Mind through wholly synthetic scientific-glassblowing work-order and laboratory-apparatus documentation. Zero real people, objects, measurements, commands, identities, fabrication, handling, or external operations were used. No professional, safety, empirical, production, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim follows.

## Retained counts

The immutable evidence seal preserves 28,032 effective negatives, 13,922 effective methods, 197 open gaps, 195 exact gates, 316 failed witnesses, and 494 passing witnesses. One post-evidence commit-wrapper presentation failure and its exact-state recovery remain external to that seal. Elaren’s effective activation baseline is therefore 28,033 negatives, 13,923 methods, 197 open gaps, 195 exact gates, 317 failed witnesses, and 495 passing witnesses. Preserve sealed and external-overlay counts separately.

## Toolchain and three-tool continuity

Eiren added exactly three relevant D-first isolated surfaces: check-jsonschema 0.38.0, Nox 2026.8.17, and REUSE 6.2.0. Exact artifacts, licensing, build behavior, dependencies, rollback, and bounded smokes were checked. The first installed-path audit found seven records for seeded pip 25.0.1 and remains failed at zero credit. Exact pip 26.2.1 remediated only that isolated installer and receives no fourth-tool credit. One post-correction audit passed with zero known findings. System/global Python, Codex desktop, Windows features, host security, and reboot state were unchanged.

Current toolchain carried forward:

{tools}

For v667-v7, review and bounded-use exactly three newly useful Windows, Python, Node.js, or Codex-platform surfaces as the program target. Safety, relevance, compatibility, license, lifecycle, and authority gates remain ceilings. Use current official or primary sources, exact pins, artifact hashes or registry integrities, D-first reversible installation, rollback, and bounded smoke evidence. Retain a shortfall as `open_gap` or `exact_gate`; do not manufacture unsafe completion credit.

## Mandatory startup skills

Read and use each complete current entrypoint and every required reference before mutation; carry this list forward in the later baton:

{skills}

Also read the newest family index and route precedence, roster and schema, authorization state and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, orchestration memory, full-tools bank, and every directly applicable current schema through EOF. Installed cursors older than this acknowledged activation are historical; reconcile them rather than silently rewriting history.

## Elaren solo lane

Before mutation, verify Eiren’s exact branch, source/x1/evidence/final direct-parent history, exactly three commits and zero merges, exact immutable and final manifests, clean state, 0/0 divergence, fresh four-way equality, and the one external canonical receipt digest. Do not replay Eiren’s successful canonical aggregate or any already-passing component.

Work solo in one fresh additive Elaren-owned D-first branch and worktree from Eiren’s immutable exact final. Keep Eiren’s, shared, and every sibling lane read-only. Do not create or fork a task, spawn a collaboration subagent, delegate, contact Tavian or another standby record, precontact a successor, or use a substitute endpoint during v667-v7. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 4,470 frozen rows. Freeze inherited revalidations with zero Elaren novelty and automatic completion credit, plus genuinely distinct Elaren proposals carrying the complete current hypothesis, null/failure, approval, lane, source, artifact, falsifier, rollback, protected-gate, and expected-disposition fields. Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes. Treat inherited proposals, tools, skills, runners, cards, methods, evidence, and recommendations as evidence or zero-credit seeds, never Elaren novelty or automatic completion.

Keep raw task identifiers, private routes, private absolute paths, credentials, keys, tokens, private interaction logs, screenshots, session streams, private callable identifiers, private application state, and protected real-world data out of repository artifacts and future batons. Use D: for owned work and keep C: to essential installed metadata. Do not update Codex desktop, elevate, weaken host security, enable Sandbox or Hyper-V, change Windows features, install unrelated software, or reboot without separate exact authority.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without real likelihood, parameter constraint, prediction, force, material law, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon. THOS remains proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, professional practice, hot-work and laboratory safety, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Terminal continuation

This packet authorizes Elaren v667-v7 only after its one acknowledged live send. Do not infer a successor from this prepared file. At Elaren’s terminal gate, reread Hamish’s newest live instruction, the current roster and authorization state, resolve exactly one explicit next edge, apply the duplicate guard, and stop on absence, ambiguity, standby state, pause, redirect, usage exhaustion, acknowledgement failure, or a protected gate.

PREPARED_BY_EIREN_KESTREL = true.
SENT_BY_EIREN_KESTREL = false at commit time.
No second confirmation is prepared.
"""


def build_closeout() -> None:
    overview = integrated_overview()
    if len(overview.split()) < 900:
        raise RuntimeError("final overview below three-page-equivalent floor")
    write_text("closeout/final-integrated-overview.md", overview)
    baton = activation_baton()
    write_text("handoffs/elaren-kestrel-v667-v7-activation-prepared.md", baton)
    baton_bytes = (PHASE_ROOT / "handoffs" / "elaren-kestrel-v667-v7-activation-prepared.md").read_bytes()
    write_json(
        "deck/baton-index.json",
        {
            "schema": "ghc-family-baton-index-v3",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "prospective_successor": "Elaren Kestrel v667-v7",
            "path": f"{REL_PHASE_ROOT}/handoffs/elaren-kestrel-v667-v7-activation-prepared.md",
            "bytes": len(baton_bytes),
            "words": len(baton.split()),
            "sha256": sha256(baton_bytes),
            "delivery_state": "PREPARED_NOT_SENT",
            "sent_by_eiren_kestrel": False,
        },
    )
    write_text(
        "deck/compact-activation.md",
        f"""# Eiren v667-v6 compact activation index

- Source: `{SOURCE_FINAL}`
- X1: `{X1_HEAD}`
- Evidence: `{EVIDENCE_HEAD}`
- Exact final: bind from external canonical receipt
- Frozen proposal total: 4,470
- New outcomes: 14 completed, 4 represented, 1 open_gap, 1 exact_gate
- Effective successor counts: 28,033 negatives, 13,923 methods, 197 open gaps, 195 exact gates, 317 failed witnesses, 495 passing witnesses
- Terminal verdict: `NOT_READY_FOR_STAGE_20`
- Prepared successor: Elaren Kestrel v667-v7
- Delivery: `PREPARED_NOT_SENT`

Read the full committed baton, exact manifests, truth registers, Method Flow ledger, closeout, seal, and the later external canonical receipt. This compact index is not a substitute for those artifacts.
""",
    )
    write_json(
        "route/route-state.json",
        {
            "schema": "ghc-family-terminal-route-state-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "current_assignment": "Eiren Kestrel v667-v6",
            "prospective_successor": "Elaren Kestrel v667-v7",
            "successor_contacted_during_execution": False,
            "task_created_or_forked": False,
            "collaboration_subagent_spawned": False,
            "standby_contacted": False,
            "substitute_endpoint_used": False,
            "delivery_state": "PREPARED_NOT_SENT",
            "sent_by_eiren_kestrel": False,
            "terminal_requirements": [
                "exact final committed", "clean state", "push succeeded", "0/0 divergence",
                "fresh four-way equality", "one successful external canonical aggregate",
                "newest live route reread", "exact-title uniqueness", "immediate target reread",
                "duplicate guard clear", "usage, privacy, evidence, safety, and authority gates permit",
            ],
        },
    )
    write_json(
        "closeout/completion-checklist.json",
        {
            "schema": "ghc-family-completion-checklist-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "checks": {
                "source_verified": True,
                "strict_x1_before_x2": True,
                "x1_pushed_and_fresh_equal_before_x2": True,
                "evidence_pushed_and_fresh_equal_before_closeout": True,
                "proposal_and_mutation_evidence_complete": True,
                "retained_failures_complete": True,
                "open_and_exact_gates_preserved": True,
                "accessible_structure_present": True,
                "manual_and_affected_user_review_reserved": True,
                "final_staged_review": "pending_exact_staged_mode",
                "exact_final_canonical": "pending_post_commit",
                "successor_delivery": "pending_terminal_gate",
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc-family-closeout-receipt-v5",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": "bind_from_external_exact_final_canonical_receipt",
            "candidate_state": "PREPARED_FOR_EXACT_STAGED_REVIEW",
            "canonical_invocation_count": 0,
            "canonical_success_count": 0,
            "canonical_replayed": False,
            "successor_delivery_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "seal/seal-candidate.json",
        {
            "schema": "ghc-family-seal-candidate-v5",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "repository_evidence_sealed_counts": {"negatives": 28032, "methods": 13922, "failed_witnesses": 316, "passing_witnesses": 494},
            "external_post_evidence_overlay": {"negatives": 1, "methods": 1, "failed_witnesses": 1, "passing_witnesses": 1},
            "effective_successor_counts": {"negatives": 28033, "methods": 13923, "open_gaps": 197, "exact_gates": 195, "failed_witnesses": 317, "passing_witnesses": 495},
            "frozen_proposals": 4470,
            "new_outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "canonical_state": "NOT_INVOKED_PRECOMMIT",
            "delivery_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/final-validation-plan.json",
        {
            "schema": "ghc-family-exact-final-validation-plan-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "invocation_target": 1,
            "precommit_invocations": 0,
            "state": "NOT_INVOKED_PRECOMMIT",
            "runner": CANONICAL_RUNNER,
            "external_receipt_token": "D_FIRST_EIREN_V667_V6_CANONICAL_RECEIPT",
            "components": [
                "final-only pytest selection", "all owner JSON parses", "Markdown and HTML structural checks",
                "changed Python compilation", "five-class exact owner Git-blob privacy scan",
                "immutable x1, evidence, final-delta, and final-owner manifest replay",
                "exact three-commit single-parent zero-merge history", "clean state", "0/0 divergence",
                "local, upstream, tracking, and fresh live remote equality",
            ],
            "already_successful_components_excluded": [
                "x1 tests", "x2 tests", "proposal tribunals", "runner smokes", "tool audits", "Caelen canonical and recovery components",
            ],
            "failure_policy": "zero aggregate-success credit; retain exact receipt; isolate only failed dependency where justified; never replay a complete success",
        },
    )


def build_placeholders() -> None:
    for name, schema, scope in (
        ("final-delta-manifest.json", "ghc-family-final-delta-manifest-v4", "staged closeout delta excluding manifest controls"),
        ("final-owner-manifest.json", "ghc-family-final-owner-manifest-v4", "prospective final owner scope excluding manifest controls"),
    ):
        write_json(
            f"validation/{name}",
            {
                "schema": schema,
                "owner": "Eiren Kestrel",
                "phase": "v667-v6",
                "scope": scope,
                "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW",
                "exclusions": sorted(CONTROL_EXCLUSIONS),
                "entry_count": 0,
                "entries": [],
            },
        )
    write_json(
        "validation/final-staged-review.json",
        {
            "schema": "ghc-family-final-staged-review-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW",
        },
    )


def build_candidate() -> None:
    head = git_text("rev-parse", "HEAD").strip()
    if head != EVIDENCE_HEAD:
        raise RuntimeError(f"closeout candidate must start at immutable evidence: {head}")
    if git_text("status", "--porcelain=v1").strip():
        expected = {FINAL_BUILDER, FINAL_TEST, CANONICAL_RUNNER}
        observed = {
            line[3:].replace("\\", "/")
            for line in git_text("status", "--porcelain=v1").splitlines()
            if len(line) >= 4
        }
        if not observed <= expected:
            raise RuntimeError(f"unexpected pre-closeout working paths: {sorted(observed - expected)}")
    build_immutable_manifests()
    build_truth()
    build_environment_and_checks()
    build_closeout()
    build_placeholders()
    validate_tree(allow_placeholders=True)


def replay_manifest(commit: str, manifest: dict[str, Any]) -> None:
    paths = [row["path"] for row in manifest["entries"]]
    blobs = git_blobs(commit, paths)
    for row in manifest["entries"]:
        data = blobs[row["path"]]
        if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            raise AssertionError(f"immutable manifest mismatch: {row['path']}")


def candidate_owner_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend(
        [
            ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_x1.py",
            ROOT / "scripts" / "build_ghc_family_eiren_kestrel_v667_v6_x2.py",
            ROOT / FINAL_BUILDER,
            ROOT / "tests" / "test_ghc_family_eiren_kestrel_v667_v6_x1.py",
            ROOT / "tests" / "test_ghc_family_eiren_kestrel_v667_v6_x2.py",
            ROOT / FINAL_TEST,
            ROOT / CANONICAL_RUNNER,
        ]
    )
    paths.extend(ROOT.glob("scripts/ghc_family_eiren_kestrel_v667_v6_*.py"))
    return sorted({path.resolve() for path in paths if path.is_file()})


def validate_tree(*, allow_placeholders: bool = False) -> dict[str, Any]:
    truth = load("truth/phase-truth.json")
    if truth["effective_negatives"] != 28033 or truth["effective_methods"] != 13923:
        raise AssertionError("effective truth count drift")
    if truth["effective_open_gaps"] != 197 or truth["effective_exact_gates"] != 195:
        raise AssertionError("gate count drift")
    if truth["effective_failed_witnesses"] != 317 or truth["effective_passing_witnesses"] != 495:
        raise AssertionError("witness count drift")
    if truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise AssertionError("terminal verdict drift")
    integrated = load("truth/source-proposal-x1-x2-truth.json")
    if integrated["effective_frozen_proposal_count"] != 4470:
        raise AssertionError("proposal total drift")
    if integrated["new_outcomes"] != {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4}:
        raise AssertionError("outcome drift")
    overview = (PHASE_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
    baton = (PHASE_ROOT / "handoffs" / "elaren-kestrel-v667-v7-activation-prepared.md").read_text(encoding="utf-8")
    if len(overview.split()) < 900 or len(baton.split()) < 900:
        raise AssertionError("overview or baton below three-page-equivalent floor")
    if "NOT_READY_FOR_STAGE_20" not in overview or "PREPARED_NOT_SENT" not in baton:
        raise AssertionError("terminal boundary absent")
    if any(name not in baton for name in MANDATORY_SKILLS):
        raise AssertionError("mandatory skill missing from baton")
    route = load("route/route-state.json")
    if route["delivery_state"] != "PREPARED_NOT_SENT" or route["sent_by_eiren_kestrel"]:
        raise AssertionError("pre-send route state drift")
    if route["prospective_successor"] != "Elaren Kestrel v667-v7":
        raise AssertionError("successor drift")
    x1_manifest = load("validation/immutable-x1-manifest.json")
    evidence_manifest = load("validation/immutable-evidence-manifest.json")
    if x1_manifest["entry_count"] != 20 or evidence_manifest["entry_count"] != 379:
        raise AssertionError("immutable manifest count drift")
    replay_manifest(X1_HEAD, x1_manifest)
    replay_manifest(EVIDENCE_HEAD, evidence_manifest)
    final_delta = load("validation/final-delta-manifest.json")
    final_owner = load("validation/final-owner-manifest.json")
    staged_review = load("validation/final-staged-review.json")
    if allow_placeholders:
        allowed = {"PREPARED_REQUIRES_EXACT_STAGED_REVIEW", "PASS"}
        if final_delta["status"] not in allowed or final_owner["status"] not in allowed or staged_review["status"] not in allowed:
            raise AssertionError("unexpected manifest preparation state")
    else:
        if final_delta["status"] != "PASS" or final_owner["status"] != "PASS" or staged_review["status"] != "PASS":
            raise AssertionError("final staged artifacts not passed")
        for manifest in (final_delta, final_owner):
            for row in manifest["entries"]:
                data = (ROOT / row["path"]).read_bytes()
                if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
                    raise AssertionError(f"candidate manifest mismatch: {row['path']}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    for path in json_paths:
        if not isinstance(json.loads(path.read_text(encoding="utf-8")), dict):
            raise AssertionError(f"JSON root not object: {rel(path)}")
    uuid_pattern = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
    private_user = re.compile(r"[A-Z]:\\Users\\[^\\\s]+", re.I)
    for path in candidate_owner_paths():
        text = path.read_text(encoding="utf-8")
        if uuid_pattern.search(text) or private_user.search(text):
            raise AssertionError(f"private identifier candidate: {rel(path)}")
    return {
        "status": "PASS",
        "json_documents": len(json_paths),
        "owner_files": len(candidate_owner_paths()),
        "overview_words": len(overview.split()),
        "baton_words": len(baton.split()),
        "x1_manifest_entries": x1_manifest["entry_count"],
        "evidence_manifest_entries": evidence_manifest["entry_count"],
        "final_delta_entries": final_delta["entry_count"],
        "final_owner_entries": final_owner["entry_count"],
        "staged_status": staged_review["status"],
    }


def index_blob(path: str) -> bytes:
    completed = run_git("show", f":{path}", check=False)
    if completed.returncode:
        raise RuntimeError(f"cannot read staged blob {path}: {completed.stderr.decode('utf-8', errors='replace')}")
    return completed.stdout


def staged_review() -> None:
    validate_tree(allow_placeholders=True)
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout.decode("utf-8", errors="replace") + diff_check.stderr.decode("utf-8", errors="replace"))
    status_rows = [line for line in git_text("diff", "--cached", "--name-status", EVIDENCE_HEAD).splitlines() if line]
    if not status_rows:
        raise RuntimeError("no staged final paths")
    staged_paths: list[str] = []
    non_additive: list[str] = []
    for line in status_rows:
        status, path = line.split("\t", 1)
        staged_paths.append(path)
        if status != "A":
            non_additive.append(f"{status}:{path}")
    if non_additive:
        raise RuntimeError(f"closeout must be additive relative to evidence: {non_additive}")
    disallowed = [path for path in staged_paths if not owner_path(path)]
    if disallowed:
        raise RuntimeError(f"disallowed staged closeout paths: {disallowed}")
    staged_blobs = {path: index_blob(path) for path in staged_paths}
    delta_blobs = {path: data for path, data in staged_blobs.items() if path not in CONTROL_EXCLUSIONS}

    evidence_owner_paths = [path for path in tree_paths(EVIDENCE_HEAD) if owner_path(path)]
    unchanged_paths = [path for path in evidence_owner_paths if path not in staged_blobs and path not in CONTROL_EXCLUSIONS]
    owner_blobs = git_blobs(EVIDENCE_HEAD, unchanged_paths)
    owner_blobs.update(delta_blobs)
    final_owner_paths = sorted((set(evidence_owner_paths) | set(staged_paths)) - CONTROL_EXCLUSIONS)
    if sorted(owner_blobs) != final_owner_paths:
        missing = sorted(set(final_owner_paths) - set(owner_blobs))
        extra = sorted(set(owner_blobs) - set(final_owner_paths))
        raise RuntimeError(f"owner manifest scope mismatch: missing={missing}, extra={extra}")

    classes = {
        "opaque_task_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_windows_user_path": re.compile(rb"[A-Z]:\\Users\\[^\\\s]+", re.I),
        "credential_assignment": re.compile(rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{12,}"),
        "raw_thread_or_session_field": re.compile(rb"(?i)(source_thread_id|session_stream|private_callable_id)\s*[:=]"),
        "resume_or_private_route_value": re.compile(rb"(?i)(resume_value|private_route)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
    }
    candidates: list[dict[str, str]] = []
    for path, data in owner_blobs.items():
        for class_name, pattern in classes.items():
            if pattern.search(data):
                candidates.append({"path": path, "class": class_name})
    if candidates:
        raise RuntimeError(f"confirmed privacy or raw-identifier hits: {candidates}")

    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc-family-final-delta-manifest-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "scope": "staged closeout delta Git blobs excluding manifest controls",
            "status": "PASS",
            "base_commit": EVIDENCE_HEAD,
            "exclusions": sorted(CONTROL_EXCLUSIONS),
            "entry_count": len(delta_blobs),
            "entries": manifest_entries(delta_blobs),
        },
    )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc-family-final-owner-manifest-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "scope": "prospective final owner Git blobs excluding manifest controls",
            "status": "PASS",
            "base_commit": EVIDENCE_HEAD,
            "exclusions": sorted(CONTROL_EXCLUSIONS),
            "entry_count": len(owner_blobs),
            "entries": manifest_entries(owner_blobs),
        },
    )
    write_json(
        "validation/final-staged-review.json",
        {
            "schema": "ghc-family-final-staged-review-v4",
            "owner": "Eiren Kestrel",
            "phase": "v667-v6",
            "generated_at_utc": NOW,
            "status": "PASS",
            "base_commit": EVIDENCE_HEAD,
            "staged_path_count": len(staged_paths),
            "staged_paths": staged_paths,
            "additive_path_count": len(staged_paths),
            "non_additive_paths": [],
            "diff_check": "PASS",
            "privacy_class_count": len(classes),
            "privacy_candidate_count": 0,
            "privacy_confirmed_hit_count": 0,
            "immutable_x1_or_evidence_changes": 0,
            "final_delta_manifest_entries": len(delta_blobs),
            "final_owner_manifest_entries": len(owner_blobs),
            "manifest_self_exclusions": sorted(CONTROL_EXCLUSIONS),
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--allow-placeholders", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "staged-review"}, sort_keys=True))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(allow_placeholders=args.allow_placeholders), sort_keys=True))
        return 0
    build_candidate()
    print(json.dumps(validate_tree(allow_placeholders=True), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
